import AppKit

struct Appearance {
    var face = "normal"
    var arms = "down"
    var legs = "stand"
    var walkStep: Int?
    var breath = 0
}

extension Mascot {
    func start(_ a: MascotAction?) {
        guard let a else {
            state = .idle(ticks: Int.random(in: Self.restRange))
            return
        }
        if manualSit && !a.name.hasPrefix("sit") {
            reaction = (a, 0, a.randomLength())
            return
        }
        if a.walk {
            direction = Bool.random() ? 1 : -1
            state = .walking(ticks: a.randomLength())
        } else {
            state = .acting(a, t: 0, length: a.randomLength())
        }
    }

    var onWindow: Bool {
        standingOn != nil || ground(below: y).window != nil
    }

    func sitAgain() -> MascotAction? {
        if manualSit {
            return character.action(named: "sitTop")
        }
        return sitForever && onWindow ? character.action(named: "sitTop") : nil
    }

    func toggleSit() {
        if manualSit {
            manualSit = false
            reaction = nil
            state = .idle(ticks: Int.random(in: Self.restRange))
            return
        }
        switch state {
        case .idle, .walking, .acting, .falling, .thrown:
            guard let a = character.action(named: "sitTop") else { return }
            start(a)
            manualSit = true
        default:
            break
        }
    }

    func finish(_ a: MascotAction) {
        if manualSit || a.name.hasPrefix("sit"), let sit = sitAgain() {
            start(sit)
            return
        }
        for (name, chance) in a.next where Double.random(in: 0..<1) < chance {
            if let n = character.action(named: name) {
                start(n)
                return
            }
        }
        state = .idle(ticks: Int.random(in: Self.restRange))
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

    func isCircling() -> Bool {
        let m = NSEvent.mouseLocation
        let f = window.frame
        let center = NSPoint(x: f.midX, y: f.minY + CGFloat(character.height) * MascotView.scale / 2)
        let dx = m.x - center.x, dy = m.y - center.y
        let r = hypot(dx, dy)
        guard r > Self.circleMinRadius, r < Self.circleMaxRadius, NSEvent.pressedMouseButtons == 0 else {
            circleAngle = nil
            circleTotal = 0
            return false
        }
        let angle = atan2(dy, dx)
        defer { circleAngle = angle }
        guard let last = circleAngle else { return false }
        var delta = angle - last
        if delta > .pi { delta -= 2 * .pi } else if delta < -.pi { delta += 2 * .pi }
        if delta * circleTotal < 0 { circleTotal = 0 }
        circleTotal = (circleTotal + delta) * Self.circleDecay
        guard abs(circleTotal) >= 2 * .pi * Self.circleTurns else { return false }
        circleTotal = 0
        return true
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
            circleAngle = nil
            circleTotal = 0
        }
    }

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
        manualSit = false
        state = .falling(character.randomAction(.fall), velocity: 0, t: 0)
    }

    func step() {
        guard window.isVisible else { return }
        tick += 1
        appearance = Appearance(face: isBlinking ? "blink" : "normal")
        view.lift = 0
        view.effect = nil
        view.cutoff = nil
        sink = 0
        if tick % (standingOn == nil ? 10 : 3) == 0 {
            desktopWindows = Desktop.windows()
            followStandingWindow()
        }

        snack?.step(floor: area.minY, gravity: Self.gravity)
        if standingOn == nil && !manualSit {
            fallIfUnsupported()
        }
        petIfStroked()
        dizzyIfCircled()

        switch state {
        case .idle(let ticks): stepIdle(ticks)
        case .walking(let ticks): stepWalking(ticks)
        case .acting(let a, let t, let length): stepActing(a, t: t, length: length)
        case .dragging(let a, let t): stepDragging(a, t: t)
        case .thrown(let a, let vx, let vy, let t, let strength): stepThrown(a, vx: vx, vy: vy, t: t, strength: strength)
        case .fetching: stepFetching()
        case .falling(let a, let v, let t): stepFalling(a, velocity: v, t: t)
        case .jumping(let a, let from, let to, let t, let length): stepJumping(a, from: from, to: to, t: t, length: length)
        }

        trackStandingWindow()
        render()
        updateCursor()
    }

    func trackStandingWindow() {
        switch state {
        case .idle, .walking, .acting:
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

    func fallIfUnsupported() {
        switch state {
        case .idle, .walking, .acting, .fetching:
            if y > ground(below: y).y + 0.5 {
                fall()
            }
        default:
            break
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

    func stepIdle(_ ticks: Int) {
        if snack?.landed == true {
            state = .fetching
        } else if ticks <= 0 {
            let onWindow = ground(below: y).window != nil
            if onWindow && sitForever, let sit = character.action(named: "sitTop") {
                start(sit)
            } else {
                start(onWindow && Int.random(in: 0..<3) == 0 ? character.randomAction(.top) : character.randomAction(.idle, app: appBehind()))
            }
        } else {
            state = .idle(ticks: ticks - 1)
        }
        appearance.breath = (60..<84).contains(tick % 100) ? 1 : 0
        lookAtMouse()
    }

    func lookAtMouse() {
        let m = NSEvent.mouseLocation
        let dx = m.x - window.frame.midX
        if appearance.face == "normal" && abs(dx) > 30 && hypot(dx, m.y - window.frame.midY) < Self.lookDistance {
            let look = dx < 0 ? "lookLeft" : "lookRight"
            if character.faces[look] != nil {
                appearance.face = look
            }
        }
    }

    func stepWalking(_ ticks: Int) {
        let g = ground(below: y)
        let w = window.frame.width
        let range = g.window == nil
            ? g.span.lowerBound...(g.span.upperBound - w)
            : (g.span.lowerBound + Self.ledgeMargin - w / 2)...(g.span.upperBound - Self.ledgeMargin - w / 2)
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

    func stepActing(_ a: MascotAction, t: Int, length: Int) {
        perform(a, t: t, length: length)
        if let (r, rt, rLength) = reaction {
            if !r.frames.isEmpty {
                appearance.face = r.pose(at: rt).face ?? appearance.face
            }
            showEffect(r, t: rt, length: rLength)
            reaction = rt + 1 >= rLength ? nil : (r, rt + 1, rLength)
        } else if a.name.hasPrefix("sit") {
            lookAtMouse()
        }
        if t + 1 >= length {
            finish(a)
        } else {
            state = .acting(a, t: t + 1, length: length)
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
                state = .idle(ticks: Int.random(in: Self.restRange))
            }
        } else {
            state = .jumping(a, from: from, to: to, t: t + 1, length: length)
        }
    }

    func stepFetching() {
        guard let s = snack else {
            state = .idle(ticks: Int.random(in: Self.restRange))
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
            state = .idle(ticks: Int.random(in: Self.restRange))
        } else {
            state = .falling(a, velocity: v + Self.gravity, t: t + 1)
        }
    }

    func render() {
        let a = appearance
        let key = a.walkStep.map { "walk\($0)\(direction < 0)\(isBlinking)" } ?? "\(a.face)|\(a.arms)|\(a.legs)|\(a.breath)"
        if let cached = frameCache[key] {
            view.sprite = cached
        } else {
            let sprite = a.walkStep.map { character.walkFrame(blink: isBlinking, step: $0, facingLeft: direction < 0) }
                ?? character.frame(face: a.face, arms: a.arms, legs: a.legs, breath: a.breath)
            frameCache[key] = sprite
            view.sprite = sprite
        }
        if key != lastFrameKey || view.lift != lastLift || view.cutoff != lastCutoff || view.effect != nil {
            view.needsDisplay = true
        }
        lastFrameKey = key
        lastLift = view.lift
        lastCutoff = view.cutoff
        updatePosition()
    }

    func resetFrames() {
        frameCache.removeAll()
        lastFrameKey = ""
    }
}
