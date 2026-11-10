import AppKit

struct FrameCache {
    var sprites: [String: [String]] = [:]
    var key = ""
    var lift: CGFloat = 0
    var cutoff: CGFloat?

    mutating func reset() {
        sprites.removeAll()
        key = ""
    }
}

extension Mascot {
    var isBlinking: Bool {
        tick % 70 < 3
    }

    func perform(_ a: MascotAction?, t: Int, length: Int) {
        guard let a, !a.frames.isEmpty else { return }
        let pose = a.pose(at: t)
        appearance.face = pose.face ?? appearance.face
        appearance.arms = pose.arms
        appearance.legs = pose.legs
        let offset = a.lift?.offset(t: t, length: length) ?? 0
        view.lift = max(0, offset)
        sink = min(0, offset)
        if case .cling = a.lift {
            view.cutoff = view.bounds.height + sink
        }
        showEffect(a, t: t, length: length)
    }

    func showEffect(_ a: MascotAction, t: Int, length: Int) {
        if let e = a.effect, let glyph = character.glyphs[e.glyph], let (progress, dx) = e.state(t: t, length: length) {
            view.effect = (glyph, progress, dx)
        }
    }

    func render() {
        let a = appearance
        let key = a.walkStep.map { "walk\($0)\(direction < 0)\(isBlinking)" } ?? "\(a.face)|\(a.arms)|\(a.legs)|\(a.breath)"
        if let cached = frames.sprites[key] {
            view.sprite = cached
        } else {
            let sprite = a.walkStep.map { character.walkFrame(blink: isBlinking, step: $0, facingLeft: direction < 0) }
                ?? character.frame(face: a.face, arms: a.arms, legs: a.legs, breath: a.breath)
            frames.sprites[key] = sprite
            view.sprite = sprite
        }
        if key != frames.key || view.lift != frames.lift || view.cutoff != frames.cutoff || view.effect != nil {
            view.needsDisplay = true
        }
        frames.key = key
        frames.lift = view.lift
        frames.cutoff = view.cutoff
        updatePosition()
    }

    func resetFrames() {
        frames.reset()
    }
}
