import AppKit
import ServiceManagement

@MainActor
final class Mascot: NSObject, NSMenuDelegate {
    enum State {
        case idle(ticks: Int)
        case walking(ticks: Int)
        case acting(MascotAction, t: Int, length: Int)
        case dragging(MascotAction?, t: Int)
        case falling(MascotAction?, velocity: CGFloat, t: Int)
        case thrown(MascotAction?, vx: CGFloat, vy: CGFloat, t: Int, strength: CGFloat)
        case fetching
        case jumping(MascotAction?, from: NSPoint, to: NSPoint, t: Int, length: Int)
    }

    static let fps = 20.0
    static let glideFps = 60.0
    static let glideJump: CGFloat = 150
    static let speed: CGFloat = 2
    static let gravity: CGFloat = 1.2
    static let lookDistance: CGFloat = 300
    static let restRange = 200...500
    static let characterKey = "character"
    static let outfitKeyPrefix = "outfit."
    static let wornKeyPrefix = "worn."
    static let throwSpeed: CGFloat = 6
    static let bounceSpeed: CGFloat = 8
    static let petTurns = 3
    static let circleTurns: CGFloat = 3
    static let circleMinRadius: CGFloat = 30
    static let circleMaxRadius: CGFloat = 400
    static let circleDecay: CGFloat = 0.985
    static let ledgeMargin: CGFloat = 12
    static let jumpHeightRatio: CGFloat = 2.5
    static let jumpReach: CGFloat = 36
    static let jumpChance = 0.02

    let window: NSPanel
    let view: MascotView
    var character: MascotCharacter
    var state = State.idle(ticks: 40)
    var direction: CGFloat = 1
    var tick = 0
    var x: CGFloat
    var y: CGFloat
    var screen: NSScreen
    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
    let toggleItem = NSMenuItem(title: "隠す", action: #selector(toggleVisible), keyEquivalent: "")
    let characterMenu = NSMenu()
    let outfitItem = NSMenuItem(title: "衣装", action: nil, keyEquivalent: "")
    let outfitMenu = NSMenu()
    let accessoryItem = NSMenuItem(title: "小物", action: nil, keyEquivalent: "")
    let accessoryMenu = NSMenu()
    let snackItem = NSMenuItem(title: "おやつをあげる", action: #selector(giveSnack), keyEquivalent: "")
    let loginItem = NSMenuItem(title: "ログイン時に起動", action: #selector(toggleLogin), keyEquivalent: "")
    var snack: Snack?
    var dragDelta = CGVector.zero
    var dragVelocity = CGVector.zero
    var petX: CGFloat?
    var petDirection: CGFloat = 0
    var petTurnTicks: [Int] = []
    var circleAngle: CGFloat?
    var circleTotal: CGFloat = 0
    var desktopWindows: [DesktopWindow] = []
    var sink: CGFloat = 0
    var appearance = Appearance()
    var overMascot = false
    var glide: (from: NSPoint, to: NSPoint, start: TimeInterval)?
    var frameCache: [String: [String]] = [:]
    var lastFrameKey = ""
    var lastLift: CGFloat = 0
    var lastCutoff: CGFloat?

    override init() {
        character = Self.dressed(MascotCharacter.named(UserDefaults.standard.string(forKey: Self.characterKey)))
        view = MascotView(character: character)
        window = NSPanel(contentRect: view.frame, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: false)
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = false
        window.sharingType = .none
        window.level = .floating
        window.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary]
        window.contentView = view

        screen = NSScreen.main ?? NSScreen.screens[0]
        let area = screen.visibleFrame
        x = area.midX
        y = area.minY
        super.init()

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
        loginItem.target = self
        menu.addItem(loginItem)
        menu.delegate = self
        menu.addItem(.separator())
        menu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "")
        statusItem.menu = menu

        view.onHide = { [weak self] in self?.setVisible(false) }
        view.onClick = { [weak self] in
            guard let self, let a = character.randomAction(.click) else { return }
            start(a)
        }
        view.onDrag = { [weak self] dx, dy in
            guard let self else { return }
            if case .dragging = state {} else {
                state = .dragging(character.randomAction(.drag), t: 0)
                dragVelocity = .zero
            }
            dragDelta.dx += dx
            dragDelta.dy += dy
            x += dx
            y += dy
            updatePosition()
        }
        view.onDrop = { [weak self] in
            guard let self else { return }
            let center = NSPoint(x: x + window.frame.width / 2, y: y + window.frame.height / 2)
            if let s = NSScreen.screens.first(where: { $0.frame.contains(center) }) {
                screen = s
            }
            let strength = hypot(dragVelocity.dx, dragVelocity.dy)
            if strength > Self.throwSpeed {
                state = .thrown(character.randomAction(.throw, strength: strength), vx: dragVelocity.dx, vy: dragVelocity.dy, t: 0, strength: strength)
            } else {
                fall()
            }
        }
        updatePosition()
        window.orderFrontRegardless()

        Timer.scheduledTimer(withTimeInterval: 1 / Self.fps, repeats: true) { [weak self] _ in
            MainActor.assumeIsolated { self?.step() }
        }

        Timer.scheduledTimer(withTimeInterval: 1 / Self.glideFps, repeats: true) { [weak self] _ in
            MainActor.assumeIsolated { self?.stepGlide() }
        }

        NotificationCenter.default.addObserver(forName: NSApplication.didChangeScreenParametersNotification, object: nil, queue: .main) { [weak self] _ in
            MainActor.assumeIsolated { self?.screensChanged() }
        }
    }

    func menuNeedsUpdate(_ menu: NSMenu) {
        loginItem.state = SMAppService.mainApp.status == .enabled ? .on : .off
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
        state = .idle(ticks: Int.random(in: Self.restRange))
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

    func screensChanged() {
        let id = screen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? NSNumber
        if let s = NSScreen.screens.first(where: { $0.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? NSNumber == id }) {
            screen = s
        } else {
            screen = NSScreen.main ?? NSScreen.screens[0]
            let area = screen.visibleFrame
            x = area.midX - window.frame.width / 2
            y = area.maxY - window.frame.height
            fall()
        }
        updatePosition()
    }

    var area: NSRect {
        screen.visibleFrame
    }

    @objc func giveSnack() {
        guard snack == nil, let s = character.snack else { return }
        let area = self.area
        snack = Snack(glyph: s.glyph, palette: character.glyphPalette, x: CGFloat.random(in: area.minX + 20...area.maxX - 60), top: area.maxY)
    }

    func updatePosition() {
        let area: NSRect
        if case .dragging = state {
            area = NSScreen.screens.reduce(NSRect.null) { $0.union($1.frame) }
        } else {
            area = self.area
        }
        x = min(max(x, area.minX), area.maxX - window.frame.width)
        y = min(max(y, area.minY), area.maxY - window.frame.height)
        let target = NSPoint(x: x, y: y + sink)
        var dragging = false
        if case .dragging = state { dragging = true }
        if dragging || hypot(target.x - window.frame.origin.x, target.y - window.frame.origin.y) > Self.glideJump {
            glide = nil
            window.setFrameOrigin(target)
        } else {
            glide = (window.frame.origin, target, ProcessInfo.processInfo.systemUptime)
        }
    }

    func stepGlide() {
        guard let g = glide else { return }
        let t = min(1, (ProcessInfo.processInfo.systemUptime - g.start) * Self.fps)
        window.setFrameOrigin(NSPoint(x: g.from.x + (g.to.x - g.from.x) * t, y: g.from.y + (g.to.y - g.from.y) * t))
        if t >= 1 { glide = nil }
    }
}
