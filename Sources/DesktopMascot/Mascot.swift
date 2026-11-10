import AppKit

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
    static let sitKey = "sitForever"
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
    let sitItem = NSMenuItem(title: "ウィンドウの上でずっと座る", action: #selector(toggleSitForever), keyEquivalent: "")
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
    var standingOn: Int?
    var manualSit = false
    var reaction: (action: MascotAction, t: Int, length: Int)?
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

        buildMenu()
        bindView()
        updatePosition()
        window.orderFrontRegardless()
        startTimers()

        NotificationCenter.default.addObserver(forName: NSApplication.didChangeScreenParametersNotification, object: nil, queue: .main) { [weak self] _ in
            MainActor.assumeIsolated { self?.screensChanged() }
        }
    }

    func bindView() {
        view.onHide = { [weak self] in self?.setVisible(false) }
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
        Timer.scheduledTimer(withTimeInterval: 1 / Self.fps, repeats: true) { [weak self] _ in
            MainActor.assumeIsolated { self?.step() }
        }

        Timer.scheduledTimer(withTimeInterval: 1 / Self.glideFps, repeats: true) { [weak self] _ in
            MainActor.assumeIsolated { self?.stepGlide() }
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
