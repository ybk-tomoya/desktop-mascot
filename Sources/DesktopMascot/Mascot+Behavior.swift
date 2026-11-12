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
        if !(a?.isChat == true || (a?.sit == true && isSitting)) {
            replyDelay = nil
            leaveChat()
        }
        guard let a else {
            rest()
            return
        }
        if ((manualSit || isCornerSitting) && !a.sit) || (isSitting && (a.isChat || a.trigger == .near)) {
            react(with: a)
            return
        }
        if a.walk {
            direction = Bool.random() ? 1 : -1
            state = .walking(ticks: a.randomLength())
        } else {
            state = .acting(a, t: 0, length: a.randomLength())
        }
    }

    func rest() {
        state = .idle(ticks: Int.random(in: Self.restRange))
    }

    func finish(_ a: MascotAction) {
        if a.trigger == .talk {
            passTurn(after: a)
            return
        }
        if a.sit || manualSit || corner != nil || sitForever, let sit = sitAgain() {
            start(sit)
            if let p = nearPeer(), Int.random(in: 0..<30) == 0 {
                _ = startChat(with: p)
            }
            return
        }
        for (name, chance) in a.next where Double.random(in: 0..<1) < chance {
            if let n = character.action(named: name) {
                start(n)
                return
            }
        }
        rest()
    }

    func step() {
        guard window.isVisible else { return }
        tick += 1
        appearance = Appearance(face: isBlinking ? "blink" : "normal")
        view.lift = 0
        view.effect = nil
        view.cutoff = nil
        sink = 0
        stepReply()
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
        case .toCorner: stepToCorner()
        case .falling(let a, let v, let t): stepFalling(a, velocity: v, t: t)
        case .jumping(let a, let from, let to, let t, let length): stepJumping(a, from: from, to: to, t: t, length: length)
        }

        trackStandingWindow()
        render()
        updateCursor()
    }

    func stepIdle(_ ticks: Int) {
        if snack?.landed == true {
            state = .fetching
        } else if corner != nil, !atCorner {
            state = .toCorner
        } else if ticks <= 0 {
            if let sit = sitAgain() {
                start(sit)
            } else if let p = nearPeer(), Int.random(in: 0..<3) == 0, startChat(with: p) {
            } else {
                let onTop = ground(below: y).window != nil
                start(onTop && Int.random(in: 0..<3) == 0 ? character.randomAction(.top) : character.randomAction(.idle, app: appBehind()))
            }
        } else {
            state = .idle(ticks: ticks - 1)
        }
        appearance.breath = (60..<84).contains((tick + characterOrder * 100 / MascotCharacter.all.count) % 100) ? 1 : 0
        lookAround()
    }

    func stepActing(_ a: MascotAction, t: Int, length: Int) {
        perform(a, t: t, length: length)
        if a.isChat, !stepChat(a, t: t) {
            return
        }
        if a.sit {
            stepSitting()
        }
        if t + 1 >= length {
            finish(a)
        } else {
            state = .acting(a, t: t + 1, length: length)
        }
    }
}
