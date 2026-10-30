import AppKit

enum Face {
    case normal, blink, happy, panic, wink, yawn, lookLeft, lookRight
}

enum Legs {
    case stand, together, sit, kickLeft, kickRight
}

enum Arms {
    case down, drumLeft, drumRight, flailLeft, flailRight, bothUp, peace
}

struct SideSprites {
    let body: [String]
    let face: [String]
    let blink: [String]
    let legs: [[String]]
    let arms: [[String]]
}

@MainActor
struct MascotCharacter {
    let id: String
    let name: String
    let width: Int
    let sitDrop: Int
    let palette: [Character: NSColor]
    let body: [String]
    let face: (Face) -> [String]
    let arms: (Arms) -> [String]
    let legs: (Legs) -> [String]
    let right: SideSprites
    let left: SideSprites

    var height: Int { body.count }

    func frame(face f: Face, arms a: Arms = .down, legs l: Legs) -> [String] {
        let upper = Sprites.overlay([body, arms(a), face(f)])
        return Sprites.overlay([legs(l), l == .sit ? Sprites.lowered(upper, by: sitDrop) : upper])
    }

    func walkFrame(face f: Face, step: Int, facingLeft: Bool) -> [String] {
        let side = facingLeft ? left : right
        let upper = Sprites.overlay([side.body, side.arms[step], f == .blink ? side.blink : side.face])
        return Sprites.overlay([side.legs[step], step % 2 == 1 ? Sprites.raised(upper, by: 1) : upper])
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
        Array(repeating: String(repeating: ".", count: rows[0].count), count: n) + rows.dropLast(n)
    }

    static func raised(_ rows: [String], by n: Int) -> [String] {
        Array(rows.dropFirst(n)) + Array(repeating: String(repeating: ".", count: rows[0].count), count: n)
    }

    static let effectPalette: [Character: NSColor] = [
        "K": NSColor(srgbRed: 0.20, green: 0.13, blue: 0.17, alpha: 1),
        "R": NSColor(srgbRed: 0.92, green: 0.32, blue: 0.42, alpha: 1),
        "W": NSColor(srgbRed: 1.00, green: 1.00, blue: 1.00, alpha: 1),
        "D": NSColor(srgbRed: 0.24, green: 0.29, blue: 0.52, alpha: 1),
    ]

    static let note = [
        "..KK.",
        "..KKK",
        "..K.K",
        "KKK..",
        "KKK..",
    ]

    static let zzz = [
        "DDDDD",
        "...D.",
        "..D..",
        ".D...",
        "DDDDD",
    ]

    static let heart = [
        ".KK.KK.",
        "KRRKRRK",
        "KRWRRRK",
        ".KRRRK.",
        "..KRK..",
        "...K...",
    ]
}
