import AppKit

final class GlyphView: NSView {
    let glyph: [String]
    let palette: [Character: NSColor]
    let scale: CGFloat

    init(glyph: [String], palette: [Character: NSColor], scale: CGFloat) {
        self.glyph = glyph
        self.palette = palette
        self.scale = scale
        super.init(frame: NSRect(x: 0, y: 0, width: CGFloat(glyph[0].count) * scale, height: CGFloat(glyph.count) * scale))
    }

    required init?(coder: NSCoder) {
        fatalError()
    }

    override var isFlipped: Bool { true }

    override func draw(_ dirtyRect: NSRect) {
        for (y, row) in glyph.enumerated() {
            for (x, c) in row.enumerated() {
                guard let color = palette[c] else { continue }
                color.setFill()
                NSRect(x: CGFloat(x) * scale, y: CGFloat(y) * scale, width: scale, height: scale).fill()
            }
        }
    }
}

@MainActor
final class Snack {
    let window: NSPanel
    var x: CGFloat
    var y: CGFloat
    var velocity: CGFloat = 0
    var landed = false

    var midX: CGFloat { x + window.frame.width / 2 }

    init(glyph: [String], palette: [Character: NSColor], x: CGFloat, top: CGFloat) {
        let view = GlyphView(glyph: glyph, palette: palette, scale: 3)
        window = NSPanel(contentRect: view.frame, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: false)
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = false
        window.sharingType = .none
        window.level = .floating
        window.ignoresMouseEvents = true
        window.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary]
        window.contentView = view
        self.x = x
        y = top - view.frame.height
        window.setFrameOrigin(NSPoint(x: x, y: y))
        window.orderFrontRegardless()
    }

    func step(floor: CGFloat, gravity: CGFloat) {
        guard !landed else { return }
        velocity -= gravity
        y += velocity
        if y <= floor {
            y = floor
            landed = true
        }
        window.setFrameOrigin(NSPoint(x: x, y: y))
    }

    func remove() {
        window.orderOut(nil)
    }
}
