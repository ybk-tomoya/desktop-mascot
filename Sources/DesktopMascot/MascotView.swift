import AppKit

@MainActor
final class MascotView: NSView {
    static let scale: CGFloat = 2
    static let headroom: CGFloat = 48

    var character: MascotCharacter
    var sprite: [String]
    var lift: CGFloat = 0
    var cutoff: CGFloat?
    var effect: (glyph: [String], progress: CGFloat, dx: CGFloat)?
    var onClick: (() -> Void)?
    var onDrag: ((CGFloat, CGFloat) -> Void)?
    var onDrop: (() -> Void)?
    var onHide: (() -> Void)?
    private var dragOrigin: NSPoint?
    private var dragged = false

    init(character: MascotCharacter) {
        self.character = character
        sprite = character.frame(face: "normal", arms: "down", legs: "stand")
        super.init(frame: NSRect(origin: .zero, size: Self.size(for: character)))
    }

    required init?(coder: NSCoder) {
        fatalError()
    }

    static func size(for character: MascotCharacter) -> NSSize {
        NSSize(width: CGFloat(character.width) * Self.scale, height: CGFloat(character.height) * Self.scale + headroom)
    }

    override var isFlipped: Bool { true }

    override func draw(_ dirtyRect: NSRect) {
        let s = Self.scale
        let top = bounds.height - CGFloat(sprite.count) * s - (lift / s).rounded() * s
        if let cutoff {
            NSRect(x: 0, y: 0, width: bounds.width, height: cutoff).clip()
        }
        for (y, row) in sprite.enumerated() {
            let chars = Array(row)
            var x = 0
            while x < chars.count {
                var end = x + 1
                while end < chars.count && chars[end] == chars[x] { end += 1 }
                if let color = character.palette[chars[x]] {
                    color.setFill()
                    NSRect(x: CGFloat(x) * s, y: top + CGFloat(y) * s, width: CGFloat(end - x) * s, height: s).fill()
                }
                x = end
            }
        }

        guard let (glyph, p, dx) = effect else { return }
        let hs: CGFloat = 3
        let originX = (bounds.midX + dx - CGFloat(glyph[0].count) * hs / 2).rounded()
        let originY = top - 6 - (p * 30 / hs).rounded() * hs - CGFloat(glyph.count) * hs
        for (y, row) in glyph.enumerated() {
            for (x, c) in row.enumerated() {
                guard let color = character.glyphPalette[c] else { continue }
                color.withAlphaComponent(1 - p).setFill()
                NSRect(x: originX + CGFloat(x) * hs, y: originY + CGFloat(y) * hs, width: hs, height: hs).fill()
            }
        }
    }

    override func updateTrackingAreas() {
        super.updateTrackingAreas()
        trackingAreas.forEach(removeTrackingArea)
        addTrackingArea(NSTrackingArea(rect: .zero, options: [.mouseEnteredAndExited, .mouseMoved, .activeAlways, .inVisibleRect], owner: self))
    }

    override func mouseMoved(with event: NSEvent) {
        updateCursor(at: convert(event.locationInWindow, from: nil))
    }

    override func mouseEntered(with event: NSEvent) {
        updateCursor(at: convert(event.locationInWindow, from: nil))
    }

    override func mouseExited(with event: NSEvent) {
        NSCursor.arrow.set()
    }

    func hitsSprite(at p: NSPoint) -> Bool {
        let s = Self.scale
        if let cutoff, p.y > cutoff { return false }
        let top = bounds.height - CGFloat(sprite.count) * s - (lift / s).rounded() * s
        let x = Int(p.x / s), y = Int((p.y - top) / s)
        let row = sprite.indices.contains(y) ? Array(sprite[y]) : []
        return row.indices.contains(x) && character.palette[row[x]] != nil
    }

    private func updateCursor(at p: NSPoint) {
        (hitsSprite(at: p) ? NSCursor.pointingHand : NSCursor.arrow).set()
    }

    override func mouseDown(with event: NSEvent) {
        dragOrigin = NSEvent.mouseLocation
        dragged = false
    }

    override func mouseDragged(with event: NSEvent) {
        guard let origin = dragOrigin else { return }
        let p = NSEvent.mouseLocation
        if !dragged && hypot(p.x - origin.x, p.y - origin.y) < 3 { return }
        dragged = true
        onDrag?(p.x - origin.x, p.y - origin.y)
        dragOrigin = p
    }

    override func mouseUp(with event: NSEvent) {
        dragOrigin = nil
        if dragged { onDrop?() } else { onClick?() }
    }

    override func rightMouseDown(with event: NSEvent) {
        let menu = NSMenu()
        menu.addItem(withTitle: "隠す", action: #selector(hide), keyEquivalent: "").target = self
        menu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "")
        NSMenu.popUpContextMenu(menu, with: event, for: self)
    }

    @objc func hide() {
        onHide?()
    }
}
