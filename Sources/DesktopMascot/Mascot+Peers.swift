import AppKit

extension Mascot {
    func nearPeer() -> Mascot? {
        let me = window.frame
        return peers().first {
            $0 !== self && $0.window.isVisible
                && abs($0.window.frame.midX - me.midX) < Self.chatDistance && abs($0.window.frame.midY - me.midY) < Self.chatDistance
        }
    }

    func answerChat() {
        guard case .idle = state else { return }
        replyingToChat = true
        state = .idle(ticks: 15)
    }
}
