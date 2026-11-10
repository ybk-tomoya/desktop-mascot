import AppKit
import ServiceManagement

extension Mascot {
    func buildMenu() {
        updateStatusIcon()
        let menu = NSMenu()
        toggleItem.target = self
        menu.addItem(toggleItem)
        for c in MascotCharacter.all {
            let item = characterMenu.addItem(withTitle: c.name, action: #selector(selectCharacter(_:)), keyEquivalent: "")
            item.target = self
            item.representedObject = c.id
            item.state = c.id == character.id ? .on : .off
        }
        menu.addItem(withTitle: "キャラ", action: nil, keyEquivalent: "").submenu = characterMenu
        outfitItem.submenu = outfitMenu
        menu.addItem(outfitItem)
        accessoryItem.submenu = accessoryMenu
        menu.addItem(accessoryItem)
        snackItem.target = self
        menu.addItem(snackItem)
        menu.autoenablesItems = false
        snackItem.isEnabled = character.snack != nil
        refreshWardrobe()
        sitItem.target = self
        menu.addItem(sitItem)
        loginItem.target = self
        menu.addItem(loginItem)
        menu.delegate = self
        menu.addItem(.separator())
        menu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "")
        statusItem.menu = menu
    }

    func menuNeedsUpdate(_ menu: NSMenu) {
        sitItem.state = sitForever ? .on : .off
        loginItem.state = SMAppService.mainApp.status == .enabled ? .on : .off
    }

    var sitForever: Bool { UserDefaults.standard.bool(forKey: Self.sitKey) }

    @objc func toggleSitForever() {
        UserDefaults.standard.set(!sitForever, forKey: Self.sitKey)
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

    @objc func toggleVisible() {
        setVisible(!window.isVisible)
    }

    func setVisible(_ visible: Bool) {
        if visible {
            window.orderFrontRegardless()
        } else {
            window.orderOut(nil)
        }
        toggleItem.title = visible ? "隠す" : "表示する"
    }

    @objc func selectCharacter(_ sender: NSMenuItem) {
        setCharacter(MascotCharacter.named(sender.representedObject as? String))
    }

    func setCharacter(_ next: MascotCharacter) {
        let c = Self.dressed(next)
        character = c
        view.character = c
        resetFrames()
        rest()
        let size = MascotView.size(for: c)
        window.setContentSize(size)
        view.frame = NSRect(origin: .zero, size: size)
        UserDefaults.standard.set(c.id, forKey: Self.characterKey)
        snackItem.isEnabled = c.snack != nil
        for item in characterMenu.items {
            item.state = item.representedObject as? String == c.id ? .on : .off
        }
        refreshWardrobe()
        updateStatusIcon()
        updatePosition()
    }

    static func dressed(_ c: MascotCharacter) -> MascotCharacter {
        var c = c
        let defaults = UserDefaults.standard
        if let id = defaults.string(forKey: outfitKeyPrefix + c.id), let i = c.outfits.firstIndex(where: { $0.id == id }) {
            c.outfitIndex = i
        }
        c.worn = Set(defaults.stringArray(forKey: wornKeyPrefix + c.id) ?? []).intersection(c.accessories.map(\.id))
        return c
    }

    func updateStatusIcon() {
        statusItem.button?.image = NSImage(systemSymbolName: "sparkles", accessibilityDescription: "Desktop Mascot")
    }

    func refreshWardrobe() {
        outfitMenu.removeAllItems()
        for o in character.outfits {
            let item = outfitMenu.addItem(withTitle: o.name, action: #selector(selectOutfit(_:)), keyEquivalent: "")
            item.target = self
            item.representedObject = o.id
            item.state = o.id == character.outfit.id ? .on : .off
        }
        accessoryMenu.removeAllItems()
        for a in character.accessories {
            let item = accessoryMenu.addItem(withTitle: a.name, action: #selector(toggleAccessory(_:)), keyEquivalent: "")
            item.target = self
            item.representedObject = a.id
            item.state = character.worn.contains(a.id) ? .on : .off
        }
        outfitItem.isEnabled = character.outfits.count > 1
        accessoryItem.isEnabled = !character.accessories.isEmpty
    }

    @objc func selectOutfit(_ sender: NSMenuItem) {
        guard let i = character.outfits.firstIndex(where: { $0.id == sender.representedObject as? String }) else { return }
        character.outfitIndex = i
        view.character = character
        resetFrames()
        UserDefaults.standard.set(character.outfit.id, forKey: Self.outfitKeyPrefix + character.id)
        refreshWardrobe()
        updateStatusIcon()
    }

    @objc func toggleAccessory(_ sender: NSMenuItem) {
        guard let id = sender.representedObject as? String else { return }
        if character.worn.contains(id) {
            character.worn.remove(id)
        } else {
            character.worn.insert(id)
        }
        view.character = character
        resetFrames()
        UserDefaults.standard.set(Array(character.worn), forKey: Self.wornKeyPrefix + character.id)
        refreshWardrobe()
        updateStatusIcon()
    }

    @objc func giveSnack() {
        guard snack == nil, let s = character.snack else { return }
        let area = self.area
        snack = Snack(glyph: s.glyph, palette: character.glyphPalette, x: CGFloat.random(in: area.minX + 20...area.maxX - 60), top: area.maxY)
    }
}
