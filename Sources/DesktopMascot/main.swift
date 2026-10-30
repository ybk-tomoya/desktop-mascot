import AppKit

@MainActor
final class MascotView: NSView {
    static let scale: CGFloat = 2
    static let headroom: CGFloat = 48

    var character: MascotCharacter
    var sprite: [String]
    var lift: CGFloat = 0
    var effect: (glyph: [String], progress: CGFloat, dx: CGFloat)?
    var onClick: (() -> Void)?
    var onDrag: ((CGFloat, CGFloat) -> Void)?
    var onDrop: (() -> Void)?
    var onHide: (() -> Void)?
    private var dragOrigin: NSPoint?
    private var dragged = false

    init(character: MascotCharacter) {
        self.character = character
        sprite = character.frame(face: "normal", arms: "down", legs: "stand")
        super.init(frame: NSRect(origin: .zero, size: Self.size(for: character)))
    }

    required init?(coder: NSCoder) {
        fatalError()
    }

    static func size(for character: MascotCharacter) -> NSSize {
        NSSize(width: CGFloat(character.width) * scale, height: CGFloat(character.height) * scale + headroom)
    }

    override var isFlipped: Bool { true }

    override func draw(_ dirtyRect: NSRect) {
        let s = Self.scale
        let top = bounds.height - CGFloat(sprite.count) * s - (lift / s).rounded() * s
        for (y, row) in sprite.enumerated() {
            for (x, c) in row.enumerated() {
                guard let color = character.palette[c] else { continue }
                color.setFill()
                NSRect(x: CGFloat(x) * s, y: top + CGFloat(y) * s, width: s, height: s).fill()
            }
        }

        guard let (glyph, p, dx) = effect else { return }
        let hs: CGFloat = 3
        let originX = (bounds.midX + dx - CGFloat(glyph[0].count) * hs / 2).rounded()
        let originY = top - 6 - (p * 30 / hs).rounded() * hs - CGFloat(glyph.count) * hs
        for (y, row) in glyph.enumerated() {
            for (x, c) in row.enumerated() {
                guard let color = character.glyphPalette[c] else { continue }
                color.withAlphaComponent(1 - p).setFill()
                NSRect(x: originX + CGFloat(x) * hs, y: originY + CGFloat(y) * hs, width: hs, height: hs).fill()
            }
        }
    }

    override func mouseDown(with event: NSEvent) {
        dragOrigin = NSEvent.mouseLocation
        dragged = false
    }

    override func mouseDragged(with event: NSEvent) {
        guard let origin = dragOrigin else { return }
        let p = NSEvent.mouseLocation
        if !dragged && hypot(p.x - origin.x, p.y - origin.y) < 3 { return }
        dragged = true
        onDrag?(p.x - origin.x, p.y - origin.y)
        dragOrigin = p
    }

    override func mouseUp(with event: NSEvent) {
        dragOrigin = nil
        if dragged { onDrop?() } else { onClick?() }
    }

    override func rightMouseDown(with event: NSEvent) {
        let menu = NSMenu()
        menu.addItem(withTitle: "隠す", action: #selector(hide), keyEquivalent: "").target = self
        menu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "")
        NSMenu.popUpContextMenu(menu, with: event, for: self)
    }

    @objc func hide() {
        onHide?()
    }
}

@MainActor
final class Mascot: NSObject {
    enum State {
        case idle(ticks: Int)
        case walking(ticks: Int)
        case acting(MascotAction, t: Int, length: Int)
        case dragging(MascotAction?, t: Int)
        case falling(MascotAction?, velocity: CGFloat, t: Int)
        case thrown(MascotAction?, vx: CGFloat, vy: CGFloat, t: Int, hard: Bool)
        case fetching
    }

    static let fps = 20.0
    static let speed: CGFloat = 2
    static let gravity: CGFloat = 1.2
    static let lookDistance: CGFloat = 300
    static let restRange = 200...500
    static let characterKey = "character"
    static let throwSpeed: CGFloat = 6
    static let hardLanding: CGFloat = 8
    static let petTurns = 3

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
            if hypot(dragVelocity.dx, dragVelocity.dy) > Self.throwSpeed {
                state = .thrown(character.randomAction(.throw), vx: dragVelocity.dx, vy: dragVelocity.dy, t: 0, hard: false)
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

    func start(_ a: MascotAction?) {
        guard let a else {
            state = .idle(ticks: Int.random(in: Self.restRange))
            return
        }
        if a.walk {
            direction = Bool.random() ? 1 : -1
            state = .walking(ticks: a.randomLength())
        } else {
            state = .acting(a, t: 0, length: a.randomLength())
        }
    }

    func finish(_ a: MascotAction) {
        for (name, chance) in a.next where Double.random(in: 0..<1) < chance {
            if let n = character.action(named: name) {
                start(n)
                return
            }
        }
        state = .idle(ticks: Int.random(in: Self.restRange))
    }

    @objc func giveSnack() {
        guard snack == nil, let s = character.snack else { return }
        let area = self.area
        snack = Snack(glyph: s.glyph, palette: character.glyphPalette, x: CGFloat.random(in: area.minX + 20...area.maxX - 60), top: area.maxY)
    }

    func isPetting() -> Bool {
        let m = NSEvent.mouseLocation
        let f = window.frame
        let spriteHeight = CGFloat(character.height) * MascotView.scale
        let head = NSRect(x: f.minX, y: f.minY + spriteHeight * 0.55, width: f.width, height: spriteHeight * 0.45 + 8)
        guard head.contains(m), NSEvent.pressedMouseButtons == 0 else {
            petX = nil
            petDirection = 0
            return false
        }
        defer { petX = m.x }
        guard let last = petX, abs(m.x - last) > 1.5 else { return false }
        let d: CGFloat = m.x > last ? 1 : -1
        if petDirection != 0 && d != petDirection {
            petTurnTicks.append(tick)
        }
        petDirection = d
        petTurnTicks.removeAll { tick - $0 > 30 }
        guard petTurnTicks.count >= Self.petTurns else { return false }
        petTurnTicks.removeAll()
        return true
    }

    func fall() {
        state = .falling(character.randomAction(.fall), velocity: 0, t: 0)
    }

    func step() {
        tick += 1
        let blink = tick % 70 < 3
        var face = blink ? "blink" : "normal"
        var arms = "down"
        var legs = "stand"
        var walkStep: Int?
        view.lift = 0
        view.effect = nil

        func perform(_ a: MascotAction?, t: Int, length: Int) {
            guard let a, !a.frames.isEmpty else { return }
            let pose = a.pose(at: t)
            face = pose.face ?? face
            arms = pose.arms
            legs = pose.legs
            view.lift = a.lift?.offset(t: t, length: length) ?? 0
            if let e = a.effect, let glyph = character.glyphs[e.glyph], let (progress, dx) = e.state(t: t, length: length) {
                view.effect = (glyph, progress, dx)
            }
        }

        snack?.step(floor: area.minY, gravity: Self.gravity)

        switch state {
        case .idle, .walking, .acting:
            if isPetting() {
                if case .acting(let a, _, let length) = state, a.trigger == .pet {
                    state = .acting(a, t: 0, length: length)
                } else if let a = character.randomAction(.pet) {
                    start(a)
                }
            }
        default:
            break
        }

        switch state {
        case .idle(let ticks):
            if snack?.landed == true {
                state = .fetching
            } else if ticks <= 0 {
                start(character.randomAction(.idle))
            } else {
                state = .idle(ticks: ticks - 1)
            }
            let m = NSEvent.mouseLocation
            let dx = m.x - window.frame.midX
            if face == "normal" && abs(dx) > 30 && hypot(dx, m.y - window.frame.midY) < Self.lookDistance {
                let look = dx < 0 ? "lookLeft" : "lookRight"
                if character.faces[look] != nil {
                    face = look
                }
            }

        case .walking(let ticks):
            let area = self.area
            let maxX = area.maxX - window.frame.width
            x += direction * Self.speed
            if x <= area.minX || x >= maxX {
                x = min(max(x, area.minX), maxX)
                direction *= -1
            }
            walkStep = (tick / 4) % 4
            state = ticks <= 0 ? .idle(ticks: Int.random(in: Self.restRange)) : .walking(ticks: ticks - 1)

        case .acting(let a, let t, let length):
            perform(a, t: t, length: length)
            if t + 1 >= length {
                finish(a)
            } else {
                state = .acting(a, t: t + 1, length: length)
            }

        case .dragging(let a, let t):
            perform(a, t: t, length: 1)
            dragVelocity = CGVector(dx: dragVelocity.dx * 0.5 + dragDelta.dx * 0.5, dy: dragVelocity.dy * 0.5 + dragDelta.dy * 0.5)
            dragDelta = .zero
            state = .dragging(a, t: t + 1)

        case .thrown(let a, var vx, var vy, let t, var hard):
            perform(a, t: t, length: 1)
            let area = self.area
            let size = window.frame.size
            x += vx
            y += vy
            vy -= Self.gravity
            if x < area.minX || x > area.maxX - size.width {
                x = min(max(x, area.minX), area.maxX - size.width)
                vx = -vx * 0.7
            }
            if y > area.maxY - size.height {
                y = area.maxY - size.height
                vy = -abs(vy) * 0.5
            }
            if y <= area.minY {
                y = area.minY
                if -vy > Self.hardLanding {
                    vy = -vy * 0.45
                    vx *= 0.7
                    hard = true
                } else {
                    if hard, let land = character.randomAction(.land) {
                        start(land)
                    } else {
                        state = .idle(ticks: Int.random(in: Self.restRange))
                    }
                    break
                }
            }
            state = .thrown(a, vx: vx, vy: vy, t: t + 1, hard: hard)

        case .fetching:
            guard let s = snack else {
                state = .idle(ticks: Int.random(in: Self.restRange))
                break
            }
            let target = s.midX - window.frame.width / 2
            if abs(target - x) <= Self.speed * 2 {
                s.remove()
                snack = nil
                start(character.randomAction(.eat))
            } else {
                direction = target < x ? -1 : 1
                x += direction * Self.speed * 1.5
                walkStep = (tick / 3) % 4
            }

        case .falling(let a, let v, let t):
            perform(a, t: t, length: 1)
            let area = self.area
            y -= v
            if y <= area.minY {
                y = area.minY
                state = .idle(ticks: Int.random(in: Self.restRange))
            } else {
                state = .falling(a, velocity: v + Self.gravity, t: t + 1)
            }
        }

        view.sprite = walkStep.map { character.walkFrame(blink: blink, step: $0, facingLeft: direction < 0) }
            ?? character.frame(face: face, arms: arms, legs: legs)
        view.needsDisplay = true
        updatePosition()
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
        window.setFrameOrigin(NSPoint(x: x, y: y))
    }
}

MainActor.assumeIsolated {
    let app = NSApplication.shared
    app.setActivationPolicy(.accessory)
    let mascot = Mascot()
    withExtendedLifetime(mascot) { app.run() }
}
