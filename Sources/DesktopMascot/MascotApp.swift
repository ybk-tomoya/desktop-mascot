import AppKit
import ServiceManagement

@MainActor
final class MascotApp: NSObject, NSMenuDelegate {
    static let characterKey = "character"
    static let modeKey = "mode"
    static let everyoneMode = "all"
    static let excludedKey = "everyoneExcluded"

    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
    let toggleItem = NSMenuItem(title: "隠す", action: #selector(toggleVisible), keyEquivalent: "")
    let soloItem = NSMenuItem(title: "ひとり", action: #selector(selectMode(_:)), keyEquivalent: "")
    let everyoneItem = NSMenuItem(title: "みんな", action: #selector(selectMode(_:)), keyEquivalent: "")
    let characterItem = NSMenuItem(title: "キャラ", action: nil, keyEquivalent: "")
    let characterMenu = NSMenu()
    let outfitItem = NSMenuItem(title: "衣装", action: nil, keyEquivalent: "")
    let outfitMenu = NSMenu()
    let accessoryItem = NSMenuItem(title: "小物", action: nil, keyEquivalent: "")
    let accessoryMenu = NSMenu()
    let snackItem = NSMenuItem(title: "おやつをあげる", action: #selector(giveSnack), keyEquivalent: "")
    let sitItem = NSMenuItem(title: "ウィンドウの上でずっと座る", action: #selector(toggleSitForever), keyEquivalent: "")
    let loginItem = NSMenuItem(title: "ログイン時に起動", action: #selector(toggleLogin), keyEquivalent: "")
    var mascots: [Mascot] = []
    var visible = true

    var everyone: Bool {
        UserDefaults.standard.string(forKey: Self.modeKey) == Self.everyoneMode
    }

    var excluded: Set<String> {
        get { Set(UserDefaults.standard.stringArray(forKey: Self.excludedKey) ?? []) }
        set { UserDefaults.standard.set(Array(newValue), forKey: Self.excludedKey) }
    }

    override init() {
        super.init()
        buildMenu()
        applyMode()
    }

    func buildMenu() {
        statusItem.button?.image = NSImage(systemSymbolName: "sparkles", accessibilityDescription: "Desktop Mascot")
        let menu = NSMenu()
        menu.autoenablesItems = false
        toggleItem.target = self
        menu.addItem(toggleItem)
        let modeMenu = NSMenu()
        for item in [soloItem, everyoneItem] {
            item.target = self
            modeMenu.addItem(item)
        }
        menu.addItem(withTitle: "モード", action: nil, keyEquivalent: "").submenu = modeMenu
        for c in MascotCharacter.all {
            let item = characterMenu.addItem(withTitle: c.name, action: #selector(selectCharacter(_:)), keyEquivalent: "")
            item.target = self
            item.representedObject = c.id
        }
        characterItem.submenu = characterMenu
        menu.addItem(characterItem)
        outfitItem.submenu = outfitMenu
        menu.addItem(outfitItem)
        accessoryItem.submenu = accessoryMenu
        menu.addItem(accessoryItem)
        snackItem.target = self
        menu.addItem(snackItem)
        sitItem.target = self
        menu.addItem(sitItem)
        loginItem.target = self
        menu.addItem(loginItem)
        menu.delegate = self
        menu.addItem(.separator())
        menu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "")
        statusItem.menu = menu
    }

    func applyMode() {
        let primary = MascotCharacter.named(UserDefaults.standard.string(forKey: Self.characterKey))
        let wanted = everyone ? MascotCharacter.all.filter { !excluded.contains($0.id) } : [primary]
        let ids = wanted.map(\.id)
        mascots.filter { !ids.contains($0.character.id) }.forEach { $0.stop() }
        mascots.removeAll { !ids.contains($0.character.id) }
        for (i, c) in wanted.enumerated() where !mascots.contains(where: { $0.character.id == c.id }) {
            let m = Mascot(character: Mascot.dressed(c), at: CGFloat(i + 1) / CGFloat(wanted.count + 1))
            m.state = .idle(ticks: 40 + i * 60)
            m.peers = { [weak self] in self?.mascots ?? [] }
            m.onHide = { [weak self] in self?.setVisible(false) }
            m.setVisible(visible)
            mascots.append(m)
        }
        refreshMenu()
    }

    func refreshMenu() {
        soloItem.state = everyone ? .off : .on
        everyoneItem.state = everyone ? .on : .off
        let shown = everyone ? mascots.map(\.character.id) : mascots.prefix(1).map(\.character.id)
        for item in characterMenu.items {
            item.state = shown.contains(item.representedObject as? String ?? "") ? .on : .off
        }
        snackItem.isEnabled = mascots.contains { $0.character.snack != nil }
        refreshWardrobe()
    }

    func refreshWardrobe() {
        outfitMenu.removeAllItems()
        accessoryMenu.removeAllItems()
        for m in mascots {
            let c = m.character
            if mascots.count > 1 {
                for menu in [outfitMenu, accessoryMenu] {
                    menu.addItem(withTitle: c.name, action: nil, keyEquivalent: "").isEnabled = false
                }
            }
            for o in c.outfits {
                let item = outfitMenu.addItem(withTitle: o.name, action: #selector(selectOutfit(_:)), keyEquivalent: "")
                item.target = self
                item.representedObject = [c.id, o.id]
                item.state = o.id == c.outfit.id ? .on : .off
            }
            for a in c.accessories {
                let item = accessoryMenu.addItem(withTitle: a.name, action: #selector(toggleAccessory(_:)), keyEquivalent: "")
                item.target = self
                item.representedObject = [c.id, a.id]
                item.state = c.worn.contains(a.id) ? .on : .off
            }
        }
        outfitItem.isEnabled = mascots.contains { $0.character.outfits.count > 1 }
        accessoryItem.isEnabled = mascots.contains { !$0.character.accessories.isEmpty }
    }

    func menuNeedsUpdate(_ menu: NSMenu) {
        sitItem.state = UserDefaults.standard.bool(forKey: Mascot.sitKey) ? .on : .off
        loginItem.state = SMAppService.mainApp.status == .enabled ? .on : .off
    }

    @objc func selectMode(_ sender: NSMenuItem) {
        UserDefaults.standard.set(sender === everyoneItem ? Self.everyoneMode : "single", forKey: Self.modeKey)
        applyMode()
    }

    @objc func selectCharacter(_ sender: NSMenuItem) {
        let c = MascotCharacter.named(sender.representedObject as? String)
        if everyone {
            if excluded.contains(c.id) {
                excluded.remove(c.id)
            } else if mascots.count > 1 {
                excluded.insert(c.id)
            }
            applyMode()
            return
        }
        UserDefaults.standard.set(c.id, forKey: Self.characterKey)
        mascots.first?.setCharacter(c)
        refreshMenu()
    }

    @objc func selectOutfit(_ sender: NSMenuItem) {
        guard let ids = sender.representedObject as? [String], let m = mascots.first(where: { $0.character.id == ids[0] }) else { return }
        m.setOutfit(ids[1])
        refreshWardrobe()
    }

    @objc func toggleAccessory(_ sender: NSMenuItem) {
        guard let ids = sender.representedObject as? [String], let m = mascots.first(where: { $0.character.id == ids[0] }) else { return }
        m.toggleAccessory(ids[1])
        refreshWardrobe()
    }

    @objc func giveSnack() {
        mascots.forEach { $0.giveSnack() }
    }

    @objc func toggleVisible() {
        setVisible(!visible)
    }

    func setVisible(_ visible: Bool) {
        self.visible = visible
        mascots.forEach { $0.setVisible(visible) }
        toggleItem.title = visible ? "隠す" : "表示する"
    }

    @objc func toggleSitForever() {
        UserDefaults.standard.set(!UserDefaults.standard.bool(forKey: Mascot.sitKey), forKey: Mascot.sitKey)
    }

    @objc func toggleLogin() {
        let service = SMAppService.mainApp
        do {
            if service.status == .enabled {
                try service.unregister()
            } else {
                try service.register()
            }
        } catch {
            let alert = NSAlert()
            alert.messageText = "ログイン時の起動を変更できませんでした"
            alert.informativeText = error.localizedDescription
            alert.runModal()
        }
    }
}
