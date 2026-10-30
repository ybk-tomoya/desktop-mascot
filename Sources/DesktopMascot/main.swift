import AppKit

@MainActor
final class MascotView: NSView {
    static let scale: CGFloat = 4
    static let headroom: CGFloat = 48

    var sprite = Sprites.frame(face: .normal, legs: .stand)
    var lift: CGFloat = 0
    var effect: (glyph: [String], progress: CGFloat, dx: CGFloat)?
    var onClick: (() -> Void)?
    var onDrag: ((CGFloat, CGFloat) -> Void)?
    var onDrop: (() -> Void)?
    var onHide: (() -> Void)?
    private var dragOrigin: NSPoint?
    private var dragged = false

    override var isFlipped: Bool { true }

    override func draw(_ dirtyRect: NSRect) {
        let s = Self.scale
        let top = bounds.height - CGFloat(sprite.count) * s - (lift / s).rounded() * s
        for (y, row) in sprite.enumerated() {
            for (x, c) in row.enumerated() {
                guard let color = Palette.colors[c] else { continue }
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
                guard let color = Palette.colors[c] else { continue }
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
        case happy(tick: Int)
        case dragging
        case falling(velocity: CGFloat)
        case drumming(ticks: Int)
        case sleeping(ticks: Int)
        case peace(tick: Int)
        case stretching(tick: Int)
        case hopping(tick: Int)
    }

    static let fps = 20.0
    static let speed: CGFloat = 2
    static let happyTicks = 30
    static let gravity: CGFloat = 1.2
    static let lookDistance: CGFloat = 300
    static let restRange = 200...500
    static let peaceTicks = 40
    static let stretchTicks = 50
    static let hopTicks = 45

    let window: NSPanel
    let view: MascotView
    var state = State.idle(ticks: 40)
    var direction: CGFloat = 1
    var tick = 0
    var x: CGFloat
    var y: CGFloat
    var screen: NSScreen
    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
    let toggleItem = NSMenuItem(title: "隠す", action: #selector(toggleVisible), keyEquivalent: "")

    override init() {
        let size = NSSize(
            width: CGFloat(Sprites.width) * MascotView.scale,
            height: CGFloat(Sprites.frame(face: .normal, legs: .stand).count) * MascotView.scale + MascotView.headroom
        )
        view = MascotView(frame: NSRect(origin: .zero, size: size))
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
        menu.addItem(.separator())
        menu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "")
        statusItem.menu = menu

        view.onHide = { [weak self] in self?.setVisible(false) }
        view.onClick = { [weak self] in self?.state = Bool.random() ? .happy(tick: 0) : .peace(tick: 0) }
        view.onDrag = { [weak self] dx, dy in
            guard let self else { return }
            state = .dragging
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
            state = .falling(velocity: 0)
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

    func screensChanged() {
        let id = screen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? NSNumber
        if let s = NSScreen.screens.first(where: { $0.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? NSNumber == id }) {
            screen = s
        } else {
            screen = NSScreen.main ?? NSScreen.screens[0]
            let area = screen.visibleFrame
            x = area.midX - window.frame.width / 2
            y = area.maxY - window.frame.height
            state = .falling(velocity: 0)
        }
        updatePosition()
    }

    var area: NSRect {
        screen.visibleFrame
    }

    func step() {
        tick += 1
        var face = tick % 70 < 3 ? Face.blink : Face.normal
        var legs = Legs.stand
        var arms = Arms.down
        var walkStep: Int?
        view.lift = 0
        view.effect = nil

        switch state {
        case .idle(let ticks):
            if ticks <= 0 {
                switch Int.random(in: 0..<14) {
                case 0..<6:
                    direction = Bool.random() ? 1 : -1
                    state = .walking(ticks: Int.random(in: 40...160))
                case 6..<9:
                    state = .drumming(ticks: Int.random(in: 60...140))
                case 9..<11:
                    state = .stretching(tick: 0)
                case 11..<13:
                    state = .hopping(tick: 0)
                default:
                    state = .sleeping(ticks: Int.random(in: 200...400))
                }
            } else {
                state = .idle(ticks: ticks - 1)
            }
            let m = NSEvent.mouseLocation
            let dx = m.x - window.frame.midX
            if face == .normal && hypot(dx, m.y - window.frame.midY) < Self.lookDistance {
                if abs(dx) > 30 {
                    face = dx < 0 ? .lookLeft : .lookRight
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

        case .happy(let t):
            face = .happy
            let p = CGFloat(t) / CGFloat(Self.happyTicks)
            view.lift = max(0, sin(min(p * 2, 1) * .pi) * 16)
            view.effect = (Sprites.heart, p, 0)
            state = t >= Self.happyTicks ? .idle(ticks: Int.random(in: Self.restRange)) : .happy(tick: t + 1)

        case .drumming(let ticks):
            face = .happy
            let beat = (tick / 3) % 2 == 0
            arms = beat ? .drumLeft : .drumRight
            let t = tick % 24
            view.effect = (Sprites.note, CGFloat(t) / 24, (tick / 24) % 2 == 0 ? -20 : 20)
            state = ticks <= 0 ? .idle(ticks: Int.random(in: Self.restRange)) : .drumming(ticks: ticks - 1)

        case .peace(let t):
            face = .wink
            arms = .peace
            if t < 20 {
                view.effect = (Sprites.heart, CGFloat(t) / 20, -16)
            }
            state = t >= Self.peaceTicks ? .idle(ticks: Int.random(in: Self.restRange)) : .peace(tick: t + 1)

        case .stretching(let t):
            face = .yawn
            arms = .bothUp
            view.lift = t > 10 && t < Self.stretchTicks - 10 ? MascotView.scale : 0
            if t >= Self.stretchTicks {
                state = Int.random(in: 0..<3) == 0 ? .sleeping(ticks: Int.random(in: 200...400)) : .idle(ticks: Int.random(in: Self.restRange))
            } else {
                state = .stretching(tick: t + 1)
            }

        case .hopping(let t):
            face = .happy
            legs = .together
            let p = CGFloat(t % 15) / 15
            view.lift = sin(p * .pi) * 12
            state = t >= Self.hopTicks ? .idle(ticks: Int.random(in: Self.restRange)) : .hopping(tick: t + 1)

        case .sleeping(let ticks):
            face = .blink
            legs = .sit
            let t = tick % 40
            view.effect = (Sprites.zzz, CGFloat(t) / 40, 16)
            state = ticks <= 0 ? .idle(ticks: Int.random(in: Self.restRange)) : .sleeping(ticks: ticks - 1)

        case .dragging:
            face = .panic
            let flip = (tick / 3) % 2 == 0
            arms = flip ? .flailLeft : .flailRight
            legs = flip ? .kickRight : .kickLeft

        case .falling(let v):
            legs = .together
            let area = self.area
            y -= v
            if y <= area.minY {
                y = area.minY
                state = .idle(ticks: Int.random(in: Self.restRange))
            } else {
                state = .falling(velocity: v + Self.gravity)
            }
        }

        view.sprite = walkStep.map { Sprites.walkFrame(face: face, step: $0, facingLeft: direction < 0) } ?? Sprites.frame(face: face, arms: arms, legs: legs)
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
