import AppKit

struct Chat {
    weak var partner: Mascot?
    var turns: Int
}

extension Mascot {
    var isChatting: Bool {
        if reaction?.action.isChat == true { return true }
        if case .acting(let a, _, _) = state { return a.isChat }
        return false
    }

    var isIdle: Bool {
        if case .idle = state { return true }
        return false
    }

    var canChat: Bool {
        replyDelay == nil && (isIdle || (isSitting && reaction == nil))
    }

    func nearPeer() -> Mascot? {
        let me = window.frame
        return peers().first {
            $0 !== self && $0.window.isVisible
                && abs($0.window.frame.midX - me.midX) < Self.chatDistance && abs($0.window.frame.midY - me.midY) < Self.chatDistance
        }
    }

    func startChat(with p: Mascot) -> Bool {
        guard canChat, p.canChat, let talk = character.randomAction(.talk), let listen = p.character.listenAction(for: talk) else { return false }
        let turns = Int.random(in: 4...6)
        chat = Chat(partner: p, turns: turns)
        p.chat = Chat(partner: self, turns: turns)
        start(talk)
        p.start(listen)
        return true
    }

    func passTurn(after said: MascotAction) {
        guard let c = chat, let p = c.partner else {
            stopChatting()
            return
        }
        let asked = said.mood == "question"
        guard c.turns > 1 || asked, let talk = p.character.randomAction(.talk, where: { !asked || $0.mood != "question" }),
              let listen = character.listenAction(for: talk) else {
            endChat()
            return
        }
        chat?.turns = c.turns - 1
        p.chat?.turns = c.turns - 1
        p.start(talk)
        start(listen)
    }

    func endChat() {
        let p = chat?.partner
        chat = nil
        p?.chat = nil
        if isSitting {
            reaction = nil
        }
        start(character.randomAction(.near))
        p?.answerChat()
    }

    func leaveChat() {
        if let p = chat?.partner, p.chat?.partner === self {
            p.stopChatting()
        }
        stopChatting()
    }

    func stopChatting() {
        chat = nil
        if reaction?.action.isChat == true {
            reaction = nil
        } else if case .acting(let a, _, _) = state, a.isChat {
            rest()
        }
    }

    func stepChat(_ a: MascotAction, t: Int) -> Bool {
        guard let p = chat?.partner, p.isChatting else {
            stopChatting()
            return false
        }
        look(toward: NSPoint(x: p.window.frame.midX, y: p.window.frame.midY), within: .infinity)
        let dx = p.window.frame.midX - window.frame.midX
        if appearance.face == "talk", abs(dx) > 30 {
            let side = dx < 0 ? "talkLeft" : "talkRight"
            if character.faces[side] != nil {
                appearance.face = side
            }
        }
        if a.trigger == .listen {
            appearance.breath = t % 70 >= 60 ? 1 : 0
        }
        return true
    }

    func answerChat() {
        stopChatting()
        replyDelay = 15
    }

    func stepReply() {
        guard let d = replyDelay else { return }
        guard isIdle || isSitting else {
            replyDelay = nil
            return
        }
        if d > 0 {
            replyDelay = d - 1
            if isIdle {
                state = .idle(ticks: max(d, 1))
            }
        } else {
            replyDelay = nil
            start(character.randomAction(.near))
        }
    }
}
