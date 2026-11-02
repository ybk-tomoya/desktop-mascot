import AppKit

struct SideSprites {
    let body: [String]
    let face: [String]
    let blink: [String]
    let legs: [[String]]
    let arms: [[String]]
}

struct MascotOutfit {
    let id: String
    let name: String
    let body: [String]
    let arms: [String: [String]]
    let legs: [String: [String]]
    let right: SideSprites
    let left: SideSprites
}

struct MascotAccessory {
    let id: String
    let name: String
    let front: [String]
    let right: [String]
    let left: [String]
}

struct MascotPose {
    let face: String?
    let arms: String
    let legs: String
    let ticks: Int
}

enum MascotLift {
    case jump(height: CGFloat)
    case hop(height: CGFloat, period: Int)
    case rise(height: CGFloat, from: Int, to: Int)
    case sink(height: CGFloat)
    case cling(height: CGFloat)

    func offset(t: Int, length: Int) -> CGFloat {
        switch self {
        case .jump(let h):
            let p = CGFloat(t) / CGFloat(length)
            return max(0, sin(min(p * 2, 1) * .pi) * h)
        case .hop(let h, let period):
            return sin(CGFloat(t % period) / CGFloat(period) * .pi) * h
        case .rise(let h, let from, let to):
            return t > from && t < to ? h : 0
        case .sink(let h), .cling(let h):
            return -h
        }
    }
}

struct MascotEffect {
    let glyph: String
    let period: Int?
    let until: Int?
    let dx: [CGFloat]

    func state(t: Int, length: Int) -> (progress: CGFloat, dx: CGFloat)? {
        if let until, t >= until { return nil }
        if let period {
            return (CGFloat(t % period) / CGFloat(period), dx[(t / period) % dx.count])
        }
        return (CGFloat(t) / CGFloat(until ?? length), dx[0])
    }
}

struct MascotSnack {
    let name: String
    let glyph: [String]
}

struct MascotAction {
    enum Trigger {
        case idle, click, drag, fall, pet, `throw`, land, eat, ledge, wall, top, chained
    }

    let name: String
    let trigger: Trigger
    let weight: Int
    let walk: Bool
    let duration: ClosedRange<Int>?
    let strength: ClosedRange<CGFloat>?
    let apps: [String]?
    let frames: [MascotPose]
    let lift: MascotLift?
    let effect: MascotEffect?
    let next: [(String, Double)]

    var cycle: Int { frames.reduce(0) { $0 + $1.ticks } }

    func randomLength() -> Int {
        duration.map { Int.random(in: $0) } ?? cycle
    }

    func pose(at t: Int) -> MascotPose {
        var r = t % cycle
        for f in frames {
            if r < f.ticks { return f }
            r -= f.ticks
        }
        return frames[0]
    }
}

@MainActor
struct MascotCharacter {
    let id: String
    let name: String
    let width: Int
    let palette: [Character: NSColor]
    let glyphPalette: [Character: NSColor]
    let faces: [String: [String]]
    let drops: [String: Int]
    let glyphs: [String: [String]]
    let actions: [MascotAction]
    let snack: MascotSnack?
    let outfits: [MascotOutfit]
    let accessories: [MascotAccessory]
    var outfitIndex = 0
    var worn: Set<String> = []

    var outfit: MascotOutfit { outfits[outfitIndex] }
    var body: [String] { outfit.body }
    var arms: [String: [String]] { outfit.arms }
    var legs: [String: [String]] { outfit.legs }
    var height: Int { body.count }

    private var wornAccessories: [MascotAccessory] {
        accessories.filter { worn.contains($0.id) }
    }

    func frame(face f: String, arms a: String, legs l: String) -> [String] {
        let upper = Sprites.overlay([body, arms[a] ?? arms["down"]!, faces[f] ?? faces["normal"]!] + wornAccessories.map(\.front))
        return Sprites.overlay([legs[l] ?? legs["stand"]!, Sprites.lowered(upper, by: drops[l] ?? 0)])
    }

    func walkFrame(blink: Bool, step: Int, facingLeft: Bool) -> [String] {
        let side = facingLeft ? outfit.left : outfit.right
        let upper = Sprites.overlay([side.body, side.arms[step], blink ? side.blink : side.face] + wornAccessories.map { facingLeft ? $0.left : $0.right })
        return Sprites.overlay([side.legs[step], step % 2 == 1 ? Sprites.raised(upper, by: 1) : upper])
    }

    func action(named name: String) -> MascotAction? {
        actions.first { $0.name == name }
    }

    func randomAction(_ trigger: MascotAction.Trigger, strength: CGFloat? = nil, app: String? = nil) -> MascotAction? {
        let candidates = actions.filter { a in
            a.trigger == trigger && (strength.map { s in a.strength?.contains(s) ?? true } ?? true)
                && (a.apps.map { apps in app.map(apps.contains) ?? false } ?? true)
        }
        var r = Int.random(in: 0..<max(1, candidates.reduce(0) { $0 + $1.weight }))
        for a in candidates {
            if r < a.weight { return a }
            r -= a.weight
        }
        return candidates.first
    }

    static func named(_ id: String?) -> MascotCharacter {
        all.first { $0.id == id } ?? all[0]
    }
}

@MainActor
enum Sprites {
    static func overlay(_ layers: [[String]]) -> [String] {
        var out = layers[0].map { Array($0) }
        for layer in layers.dropFirst() {
            for (y, row) in layer.enumerated() {
                for (x, c) in row.enumerated() where c != "." {
                    out[y][x] = c
                }
            }
        }
        return out.map { String($0) }
    }

    static func lowered(_ rows: [String], by n: Int) -> [String] {
        guard n > 0 else { return rows }
        return Array(repeating: String(repeating: ".", count: rows[0].count), count: n) + rows.dropLast(n)
    }

    static func raised(_ rows: [String], by n: Int) -> [String] {
        Array(rows.dropFirst(n)) + Array(repeating: String(repeating: ".", count: rows[0].count), count: n)
    }
}
