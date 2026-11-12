import AppKit

@MainActor
struct PetDetector {
    var x: CGFloat?
    var direction: CGFloat = 0
    var turnTicks: [Int] = []

    mutating func stroked(mouse m: NSPoint, head: NSRect, tick: Int) -> Bool {
        guard head.contains(m), NSEvent.pressedMouseButtons == 0 else {
            x = nil
            direction = 0
            return false
        }
        defer { x = m.x }
        guard let last = x, abs(m.x - last) > 1.5 else { return false }
        let d: CGFloat = m.x > last ? 1 : -1
        if direction != 0 && d != direction {
            turnTicks.append(tick)
        }
        direction = d
        turnTicks.removeAll { tick - $0 > 30 }
        guard turnTicks.count >= Mascot.petTurns else { return false }
        turnTicks.removeAll()
        return true
    }
}

@MainActor
struct CircleDetector {
    var angle: CGFloat?
    var total: CGFloat = 0

    mutating func reset() {
        angle = nil
        total = 0
    }

    mutating func circled(mouse m: NSPoint, center: NSPoint) -> Bool {
        let dx = m.x - center.x, dy = m.y - center.y
        let r = hypot(dx, dy)
        guard r > Mascot.circleMinRadius, r < Mascot.circleMaxRadius, NSEvent.pressedMouseButtons == 0 else {
            reset()
            return false
        }
        let now = atan2(dy, dx)
        defer { angle = now }
        guard let last = angle else { return false }
        var delta = now - last
        if delta > .pi { delta -= 2 * .pi } else if delta < -.pi { delta += 2 * .pi }
        if delta * total < 0 { total = 0 }
        total = (total + delta) * Mascot.circleDecay
        guard abs(total) >= 2 * .pi * Mascot.circleTurns else { return false }
        total = 0
        return true
    }
}

extension Mascot {
    func isPetting() -> Bool {
        let f = window.frame
        let spriteHeight = CGFloat(character.height) * MascotView.scale
        let head = NSRect(x: f.minX, y: f.minY + spriteHeight * 0.55, width: f.width, height: spriteHeight * 0.45 + 8)
        return pet.stroked(mouse: NSEvent.mouseLocation, head: head, tick: tick)
    }

    func isCircling() -> Bool {
        let f = window.frame
        let center = NSPoint(x: f.midX, y: f.minY + CGFloat(character.height) * MascotView.scale / 2)
        return circle.circled(mouse: NSEvent.mouseLocation, center: center)
    }

    func dizzyIfCircled() {
        switch state {
        case .idle, .walking, .acting:
            let circled = isCircling()
            if case .acting(let a, _, _) = state, a.trigger == .circle { return }
            if circled, let a = character.randomAction(.circle) {
                start(a)
            }
        default:
            circle.reset()
        }
    }

    func petIfStroked() {
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
    }

    func lookAround() {
        let m = NSEvent.mouseLocation
        if hypot(m.x - window.frame.midX, m.y - window.frame.midY) >= Self.lookDistance, let p = nearPeer() {
            look(toward: NSPoint(x: p.window.frame.midX, y: p.window.frame.midY), within: .infinity)
        } else {
            look(toward: m, within: Self.lookDistance)
        }
    }

    func look(toward m: NSPoint, within distance: CGFloat) {
        let dx = m.x - window.frame.midX
        if appearance.face == "normal" && abs(dx) > 30 && hypot(dx, m.y - window.frame.midY) < distance {
            let look = dx < 0 ? "lookLeft" : "lookRight"
            if character.faces[look] != nil {
                appearance.face = look
            }
        }
    }

    func updateCursor() {
        let p = view.convert(window.convertPoint(fromScreen: NSEvent.mouseLocation), from: nil)
        let over = window.isVisible && view.hitsSprite(at: p)
        if over {
            NSCursor.pointingHand.set()
        } else if overMascot {
            NSCursor.arrow.set()
        }
        overMascot = over
    }
}
