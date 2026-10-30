import AppKit

@MainActor
final class MascotView: NSView {
    static let scale: CGFloat = 4
    static let headroom: CGFloat = 48

    var sprite = Sprites.frame(face: .normal, legs: .stand)
    var lift: CGFloat = 0
    var heartProgress: CGFloat?
    var onClick: (() -> Void)?
    var onDrag: ((CGFloat, CGFloat) -> Void)?
    var onDrop: (() -> Void)?
    private var dragOrigin: NSPoint?
    private var dragged = false

    override var isFlipped: Bool { true }

    override func draw(_ dirtyRect: NSRect) {
        let s = Self.scale
        let top = bounds.height - CGFloat(sprite.count) * s - lift
        for (y, row) in sprite.enumerated() {
            for (x, c) in row.enumerated() {
                guard let color = Palette.colors[c] else { continue }
                color.setFill()
                NSRect(x: CGFloat(x) * s, y: top + CGFloat(y) * s, width: s, height: s).fill()
            }
        }

        guard let p = heartProgress else { return }
        let hs: CGFloat = 3
        let originX = bounds.midX - CGFloat(Sprites.heart[0].count) * hs / 2
        let originY = top - 6 - p * 30 - CGFloat(Sprites.heart.count) * hs
        for (y, row) in Sprites.heart.enumerated() {
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
        menu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "")
        NSMenu.popUpContextMenu(menu, with: event, for: self)
    }
}

@MainActor
final class Mascot {
    enum State {
        case idle(ticks: Int)
        case walking(ticks: Int)
        case happy(tick: Int)
        case dragging
        case falling(velocity: CGFloat)
    }

    static let fps = 20.0
    static let speed: CGFloat = 2
    static let happyTicks = 30
    static let gravity: CGFloat = 1.2

    let window: NSPanel
    let view: MascotView
    var state = State.idle(ticks: 40)
    var direction: CGFloat = 1
    var tick = 0
    var x: CGFloat
    var y: CGFloat
    var screen: NSScreen

    init() {
        let size = NSSize(
            width: CGFloat(Sprites.width) * MascotView.scale,
            height: CGFloat(Sprites.frame(face: .normal, legs: .stand).count) * MascotView.scale + MascotView.headroom
        )
        view = MascotView(frame: NSRect(origin: .zero, size: size))
        window = NSPanel(contentRect: view.frame, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: false)
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = false
        window.level = .floating
        window.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary]
        window.contentView = view

        screen = NSScreen.main ?? NSScreen.screens[0]
        let area = screen.visibleFrame
        x = area.midX
        y = area.minY
        view.onClick = { [weak self] in self?.state = .happy(tick: 0) }
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
        var walkStep: Int?
        view.lift = 0
        view.heartProgress = nil

        switch state {
        case .idle(let ticks):
            if ticks <= 0 {
                direction = Bool.random() ? 1 : -1
                state = .walking(ticks: Int.random(in: 40...160))
            } else {
                state = .idle(ticks: ticks - 1)
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
            state = ticks <= 0 ? .idle(ticks: Int.random(in: 40...200)) : .walking(ticks: ticks - 1)

        case .happy(let t):
            face = .happy
            let p = CGFloat(t) / CGFloat(Self.happyTicks)
            view.lift = max(0, sin(min(p * 2, 1) * .pi) * 16)
            view.heartProgress = p
            state = t >= Self.happyTicks ? .idle(ticks: 20) : .happy(tick: t + 1)

        case .dragging:
            face = .blink
            legs = .together

        case .falling(let v):
            legs = .together
            let area = self.area
            y -= v
            if y <= area.minY {
                y = area.minY
                state = .idle(ticks: 20)
            } else {
                state = .falling(velocity: v + Self.gravity)
            }
        }

        view.sprite = walkStep.map { Sprites.walkFrame(face: face, step: $0, facingLeft: direction < 0) } ?? Sprites.frame(face: face, legs: legs)
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
