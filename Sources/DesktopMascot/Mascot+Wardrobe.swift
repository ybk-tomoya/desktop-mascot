import AppKit

extension Mascot {
    func setVisible(_ visible: Bool) {
        if visible {
            window.orderFrontRegardless()
        } else {
            window.orderOut(nil)
        }
    }

    func setCharacter(_ next: MascotCharacter) {
        let c = Self.dressed(next)
        character = c
        view.character = c
        resetFrames()
        rest()
        let size = MascotView.size(for: c)
        window.setContentSize(size)
        view.frame = NSRect(origin: .zero, size: size)
        updatePosition()
    }

    static func dressed(_ c: MascotCharacter) -> MascotCharacter {
        var c = c
        let defaults = UserDefaults.standard
        if let id = defaults.string(forKey: outfitKeyPrefix + c.id), let i = c.outfits.firstIndex(where: { $0.id == id }) {
            c.outfitIndex = i
        }
        c.worn = Set(defaults.stringArray(forKey: wornKeyPrefix + c.id) ?? []).intersection(c.accessories.map(\.id))
        return c
    }

    func setOutfit(_ id: String) {
        guard let i = character.outfits.firstIndex(where: { $0.id == id }) else { return }
        character.outfitIndex = i
        view.character = character
        resetFrames()
        UserDefaults.standard.set(character.outfit.id, forKey: Self.outfitKeyPrefix + character.id)
    }

    func toggleAccessory(_ id: String) {
        if character.worn.contains(id) {
            character.worn.remove(id)
        } else {
            character.worn.insert(id)
        }
        view.character = character
        resetFrames()
        UserDefaults.standard.set(Array(character.worn), forKey: Self.wornKeyPrefix + character.id)
    }

    func giveSnack() {
        guard snack == nil, let s = character.snack else { return }
        let area = self.area
        snack = Snack(glyph: s.glyph, palette: character.glyphPalette, x: CGFloat.random(in: area.minX + 20...area.maxX - 60), top: area.maxY)
    }
}
