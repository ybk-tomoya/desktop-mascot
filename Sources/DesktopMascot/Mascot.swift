import AppKit

@MainActor
final class Mascot: NSObject {
    enum State {
        case idle(ticks: Int)
        case walking(ticks: Int)
        case acting(MascotAction, t: Int, length: Int)
        case dragging(MascotAction?, t: Int)
        case falling(MascotAction?, velocity: CGFloat, t: Int)
        case thrown(MascotAction?, vx: CGFloat, vy: CGFloat, t: Int, strength: CGFloat)
        case fetching
    }

    static let fps = 20.0
    static let speed: CGFloat = 2
    static let gravity: CGFloat = 1.2
    static let lookDistance: CGFloat = 300
    static let restRange = 200...500
    static let characterKey = "character"
    static let throwSpeed: CGFloat = 6
    static let bounceSpeed: CGFloat = 8
    static let petTurns = 3
    static let ledgeMargin: CGFloat = 12

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
    let snackItem = NSMenuItem(title: "おやつをあげる", action: #selector(giveSnack), keyEquivalent: "")
    var snack: Snack?
    var dragDelta = CGVector.zero
    var dragVelocity = CGVector.zero
    var petX: CGFloat?
    var petDirection: CGFloat = 0
    var petTurnTicks: [Int] = []
    var desktopWindows: [DesktopWindow] = []
    var sink: CGFloat = 0
    var appearance = Appearance()

    override init() {
        character = MascotCharacter.named(UserDefaults.standard.string(forKey: Self.characterKey))
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

        statusItem.button?.image = NSImage(systemSymbolName: "music.note", accessibilityDescription: "DesktopMascot")
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
        snackItem.target = self
        menu.addItem(snackItem)
        menu.autoenablesItems = false
        snackItem.isEnabled = character.snack != nil
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

        NotificationCenter.default.addObserver(forName: NSApplication.didChangeScreenParametersNotification, object: nil, queue: .main) { [weak self] _ in
            MainActor.assumeIsolated { self?.screensChanged() }
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

    func setCharacter(_ c: MascotCharacter) {
        character = c
        view.character = c
        state = .idle(ticks: Int.random(in: Self.restRange))
        let size = MascotView.size(for: c)
        window.setContentSize(size)
        view.frame = NSRect(origin: .zero, size: size)
        UserDefaults.standard.set(c.id, forKey: Self.characterKey)
        snackItem.isEnabled = c.snack != nil
        for item in characterMenu.items {
            item.state = item.representedObject as? String == c.id ? .on : .off
        }
        updatePosition()
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
        window.setFrameOrigin(NSPoint(x: x, y: y + sink))
    }
}
