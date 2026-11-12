import AppKit

enum Corner: String {
    case left, right
}

extension Mascot {
    var onWindow: Bool {
        standingOn != nil || ground(below: y).window != nil
    }

    var isSitting: Bool {
        if case .acting(let a, _, _) = state { return a.sit }
        return false
    }

    var sitForever: Bool { UserDefaults.standard.bool(forKey: Self.sitKey) }

    var isCornerSitting: Bool {
        if case .acting(let a, _, _) = state { return a.trigger == .corner }
        return false
    }

    var cornerTarget: CGFloat? {
        guard let corner else { return nil }
        let offset = CGFloat(corner.slot) * Self.cornerSpacing
        return corner.side == .left ? area.minX + offset : area.maxX - window.frame.width - offset
    }

    var atCorner: Bool {
        cornerTarget.map { abs($0 - x) <= Self.speed } ?? false
    }

    func sitAgain() -> MascotAction? {
        if corner != nil {
            return atCorner ? character.cornerSitAction : nil
        }
        if manualSit {
            return character.sitAction
        }
        return sitForever ? (onWindow ? character.sitAction : character.cornerSitAction) : nil
    }

    func updateSitForever() {
        guard corner == nil, !manualSit else { return }
        switch state {
        case .idle, .walking, .acting, .fetching:
            break
        default:
            return
        }
        if sitForever {
            if !isSitting {
                leaveChat()
                start(sitAgain())
            }
        } else if isSitting {
            rest()
        }
    }

    func standOrKeepSitting() {
        if sitForever, let sit = sitAgain() {
            start(sit)
        } else {
            rest()
        }
    }

    func setCorner(_ side: Corner?, slot: Int) {
        corner = side.map { ($0, slot) }
        switch state {
        case .idle, .walking, .acting, .fetching, .toCorner:
            break
        default:
            return
        }
        if corner != nil {
            leaveChat()
            stopSitting()
            state = .toCorner
        } else if case .toCorner = state {
            standOrKeepSitting()
        } else if case .acting(let a, _, _) = state, a.trigger == .corner {
            standOrKeepSitting()
        }
    }

    func toggleSit() {
        guard corner == nil else { return }
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
        if r.isChat, !stepChat(r, t: t) {
            return
        }
        showEffect(r, t: t, length: length)
        reaction = t + 1 >= length ? nil : (r, t + 1, length)
        if reaction == nil, r.trigger == .talk {
            passTurn(after: r)
        }
    }
}
