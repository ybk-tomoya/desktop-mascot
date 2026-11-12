import AppKit

extension Mascot {
    var onWindow: Bool {
        standingOn != nil || ground(below: y).window != nil
    }

    var sitForever: Bool { UserDefaults.standard.bool(forKey: Self.sitKey) }

    func sitAgain() -> MascotAction? {
        manualSit || (sitForever && onWindow) ? character.sitAction : nil
    }

    func toggleSit() {
        if manualSit {
            stopSitting()
            rest()
            return
        }
        switch state {
        case .idle, .walking, .acting, .falling, .thrown:
            guard let a = character.sitAction else { return }
            start(a)
            manualSit = true
        default:
            break
        }
    }

    func stopSitting() {
        manualSit = false
        reaction = nil
    }

    func react(with a: MascotAction) {
        reaction = (a, 0, a.randomLength())
    }

    func stepSitting() {
        guard let (r, t, length) = reaction else {
            lookAround()
            return
        }
        if !r.frames.isEmpty {
            appearance.face = r.pose(at: t).face ?? appearance.face
        }
        showEffect(r, t: t, length: length)
        reaction = t + 1 >= length ? nil : (r, t + 1, length)
    }
}
