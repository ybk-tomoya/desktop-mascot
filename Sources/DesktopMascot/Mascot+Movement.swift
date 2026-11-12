import AppKit

extension Mascot {
    func ground(below top: CGFloat, cx: CGFloat? = nil) -> (y: CGFloat, span: ClosedRange<CGFloat>, window: DesktopWindow?) {
        let area = self.area
        let cx = cx ?? x + window.frame.width / 2
        var best = (y: area.minY, span: area.minX...area.maxX, window: DesktopWindow?.none)
        for (i, w) in desktopWindows.enumerated() {
            let f = w.frame
            guard f.minX < cx, cx < f.maxX, f.maxY <= top + 0.5, f.maxY > best.y, f.maxY + window.frame.height <= area.maxY,
                  !desktopWindows[..<i].contains(where: { $0.frame.contains(NSPoint(x: cx, y: f.maxY + 2)) }) else { continue }
            best = (f.maxY, max(f.minX, area.minX)...min(f.maxX, area.maxX), w)
        }
        return best
    }

    func appBehind() -> String? {
        let center = NSPoint(x: x + window.frame.width / 2, y: y + CGFloat(character.height) * MascotView.scale / 2)
        return (desktopWindows.first { $0.frame.contains(center) } ?? ground(below: y).window)?.app
    }

    func fall() {
        state = .falling(character.randomAction(.fall), velocity: 0, t: 0)
    }

    func fallIfUnsupported() {
        switch state {
        case .idle, .walking, .acting, .fetching, .toCorner:
            if y > ground(below: y).y + 0.5 {
                fall()
            }
        default:
            break
        }
    }

    func trackStandingWindow() {
        switch state {
        case .idle, .walking, .acting, .toCorner:
            let g = ground(below: y)
            if let w = g.window, abs(y - g.y) < 0.5 {
                standingOn = w.id
            }
        default:
            standingOn = nil
        }
    }

    func followStandingWindow() {
        guard let id = standingOn else { return }
        let cx = x + window.frame.width / 2
        guard let f = desktopWindows.first(where: { $0.id == id })?.frame, f.minX < cx, cx < f.maxX else {
            standingOn = nil
            return
        }
        y = min(f.maxY, area.maxY - window.frame.height)
    }

    func stepWalking(_ ticks: Int) {
        let g = ground(below: y)
        let w = window.frame.width
        let range = g.window == nil
            ? g.span.lowerBound...(g.span.upperBound - w)
            : (g.span.lowerBound + Self.ledgeMargin - w / 2)...(g.span.upperBound - Self.ledgeMargin - w / 2)
        if peerAhead() != nil {
            direction *= -1
        }
        x += direction * Self.speed
        appearance.walkStep = (tick / 4) % 4
        state = ticks <= 0 ? .idle(ticks: Int.random(in: Self.restRange)) : .walking(ticks: ticks - 1)
        if let target = jumpTarget(), Double.random(in: 0..<1) < Self.jumpChance, let a = character.randomAction(.jump) {
            let length = min(36, max(14, Int(hypot(target.x - x, target.y - y) / 12)))
            appearance.walkStep = nil
            state = .jumping(a, from: NSPoint(x: x, y: y), to: target, t: 0, length: length)
            return
        }
        if !range.contains(x) {
            x = min(max(x, range.lowerBound), range.upperBound)
            if Bool.random(), let a = character.randomAction(g.window == nil ? .wall : .ledge) {
                appearance.walkStep = nil
                start(a)
            } else {
                direction *= -1
            }
        }
    }

    func stepDragging(_ a: MascotAction?, t: Int) {
        perform(a, t: t, length: 1)
        dragVelocity = CGVector(dx: dragVelocity.dx * 0.5 + dragDelta.dx * 0.5, dy: dragVelocity.dy * 0.5 + dragDelta.dy * 0.5)
        dragDelta = .zero
        state = .dragging(a, t: t + 1)
    }

    func stepThrown(_ a: MascotAction?, vx: CGFloat, vy: CGFloat, t: Int, strength: CGFloat) {
        var vx = vx, vy = vy
        perform(a, t: t, length: 1)
        let area = self.area
        let size = window.frame.size
        let floor = ground(below: y).y
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
        if y <= floor {
            y = floor
            if -vy > Self.bounceSpeed {
                vy = -vy * 0.45
                vx *= 0.7
            } else {
                start(character.randomAction(.land, strength: strength))
                return
            }
        }
        state = .thrown(a, vx: vx, vy: vy, t: t + 1, strength: strength)
    }

    func jumpTarget() -> NSPoint? {
        let w = window.frame.width
        let cx = x + w / 2
        let inset = Self.ledgeMargin + w / 2 + 8
        for win in desktopWindows {
            let f = win.frame
            let rise = f.maxY - y
            guard rise > 8, rise <= CGFloat(character.height) * MascotView.scale * Self.jumpHeightRatio, f.maxY + window.frame.height <= area.maxY,
                  f.width > inset * 2 else { continue }
            let edge = direction > 0 ? f.minX : f.maxX
            let distance = (edge - cx) * direction
            let landing: CGFloat
            if f.minX + inset <= cx, cx <= f.maxX - inset {
                landing = cx
            } else if distance >= 0, distance <= Self.jumpReach {
                landing = edge + direction * inset
            } else {
                continue
            }
            guard ground(below: f.maxY + 1, cx: landing).window?.frame == f else { continue }
            return NSPoint(x: landing - w / 2, y: f.maxY)
        }
        return nil
    }

    func stepJumping(_ a: MascotAction?, from: NSPoint, to: NSPoint, t: Int, length: Int) {
        perform(a, t: t, length: length)
        let p = CGFloat(t + 1) / CGFloat(length)
        x = from.x + (to.x - from.x) * p
        y = from.y + (to.y - from.y) * p + sin(p * .pi) * (24 + abs(to.y - from.y) * 0.3)
        if t + 1 >= length {
            x = to.x
            y = to.y
            if let a {
                finish(a)
            } else {
                rest()
            }
        } else {
            state = .jumping(a, from: from, to: to, t: t + 1, length: length)
        }
    }

    func stepFetching() {
        guard let s = snack else {
            rest()
            return
        }
        let target = s.midX - window.frame.width / 2
        if abs(target - x) <= Self.speed * 2 {
            s.remove()
            snack = nil
            start(character.randomAction(.eat))
        } else {
            direction = target < x ? -1 : 1
            x += direction * Self.speed * 1.5
            appearance.walkStep = (tick / 3) % 4
        }
    }

    func stepFalling(_ a: MascotAction?, velocity v: CGFloat, t: Int) {
        perform(a, t: t, length: 1)
        let floor = ground(below: y).y
        y -= v
        if y <= floor {
            y = floor
            rest()
        } else {
            state = .falling(a, velocity: v + Self.gravity, t: t + 1)
        }
    }

    func stepToCorner() {
        guard let target = cornerTarget else {
            rest()
            return
        }
        if abs(target - x) <= Self.speed {
            x = target
            start(character.sitAction)
        } else {
            direction = target < x ? -1 : 1
            x += direction * Self.speed
            appearance.walkStep = (tick / 4) % 4
        }
    }
}
