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
        case toCorner
        case jumping(MascotAction?, from: NSPoint, to: NSPoint, t: Int, length: Int)
    }

    static let fps = 20.0
    static let glideFps = 60.0
    static let glideJump: CGFloat = 150
    static let speed: CGFloat = 2
    static let gravity: CGFloat = 1.2
    static let lookDistance: CGFloat = 300
    static let chatDistance: CGFloat = 200
    static let personalSpace: CGFloat = 60
    static let restRange = 900...2000
    static let outfitKeyPrefix = "outfit."
    static let wornKeyPrefix = "worn."
    static let sitKey = "sitForever"
    static let cornerKey = "cornerSit"
    static let cornerOrderKey = "cornerOrder"
    static let cornerSpacing: CGFloat = 64
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
    var snack: Snack?
    var dragDelta = CGVector.zero
    var dragVelocity = CGVector.zero
    var pet = PetDetector()
    var circle = CircleDetector()
    var desktopWindows: [DesktopWindow] = []
    var standingOn: Int?
    var manualSit = false
    var corner: (side: Corner, slot: Int)?
    var replyDelay: Int?
    var chat: Chat?
    var reaction: (action: MascotAction, t: Int, length: Int)?
    var sink: CGFloat = 0
    var appearance = Appearance()
    var overMascot = false
    var glide: (from: NSPoint, to: NSPoint, start: TimeInterval)?
    var frames = FrameCache()
    var peers: () -> [Mascot] = { [] }
    var onHide: (() -> Void)?
    var onCornerDrop: (() -> Void)?
    var timers: [Timer] = []
    var screenObserver: NSObjectProtocol?

    init(character: MascotCharacter, at fraction: CGFloat = 0.5) {
        self.character = character
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
        x = area.minX + area.width * fraction
        y = area.minY
        super.init()

        bindView()
        updatePosition()
        window.orderFrontRegardless()
        startTimers()

        screenObserver = NotificationCenter.default.addObserver(forName: NSApplication.didChangeScreenParametersNotification, object: nil, queue: .main) { [weak self] _ in
            MainActor.assumeIsolated { self?.screensChanged() }
        }
    }

    func stop() {
        timers.forEach { $0.invalidate() }
        timers = []
        if let screenObserver {
            NotificationCenter.default.removeObserver(screenObserver)
        }
        window.orderOut(nil)
    }

    func bindView() {
        view.onHide = { [weak self] in self?.onHide?() }
        view.onSit = { [weak self] in self?.toggleSit() }
        view.isSitting = { [weak self] in self?.manualSit ?? false }
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
            if corner != nil {
                onCornerDrop?()
            }
            let strength = hypot(dragVelocity.dx, dragVelocity.dy)
            if manualSit, let sit = sitAgain() {
                start(sit)
            } else if strength > Self.throwSpeed {
                state = .thrown(character.randomAction(.throw, strength: strength), vx: dragVelocity.dx, vy: dragVelocity.dy, t: 0, strength: strength)
            } else {
                fall()
            }
        }
    }

    func startTimers() {
        timers = [
            Timer.scheduledTimer(withTimeInterval: 1 / Self.fps, repeats: true) { [weak self] _ in
                MainActor.assumeIsolated { self?.step() }
            },
            Timer.scheduledTimer(withTimeInterval: 1 / Self.glideFps, repeats: true) { [weak self] _ in
                MainActor.assumeIsolated { self?.stepGlide() }
            },
        ]
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
            stopSitting()
            fall()
        }
        updatePosition()
    }

    var area: NSRect {
        screen.visibleFrame
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
