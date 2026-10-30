import AppKit

@MainActor
enum Palette {
    static let colors: [Character: NSColor] = [
        "K": NSColor(srgbRed: 0.20, green: 0.13, blue: 0.17, alpha: 1),
        "H": NSColor(srgbRed: 0.50, green: 0.31, blue: 0.26, alpha: 1),
        "h": NSColor(srgbRed: 0.74, green: 0.52, blue: 0.42, alpha: 1),
        "S": NSColor(srgbRed: 1.00, green: 0.89, blue: 0.80, alpha: 1),
        "s": NSColor(srgbRed: 0.92, green: 0.70, blue: 0.64, alpha: 1),
        "P": NSColor(srgbRed: 1.00, green: 0.68, blue: 0.72, alpha: 1),
        "W": NSColor(srgbRed: 1.00, green: 1.00, blue: 1.00, alpha: 1),
        "E": NSColor(srgbRed: 0.33, green: 0.24, blue: 0.55, alpha: 1),
        "R": NSColor(srgbRed: 0.92, green: 0.32, blue: 0.42, alpha: 1),
        "D": NSColor(srgbRed: 0.47, green: 0.50, blue: 0.80, alpha: 1),
        "d": NSColor(srgbRed: 0.37, green: 0.39, blue: 0.68, alpha: 1),
        "L": NSColor(srgbRed: 0.97, green: 0.97, blue: 0.99, alpha: 1),
        "B": NSColor(srgbRed: 0.42, green: 0.23, blue: 0.21, alpha: 1),
    ]
}

enum Face {
    case normal, blink, happy
}

enum Legs {
    case stand, stride, together
}

enum Sprites {
    static let width = 16

    static let head = [
        "....KKKKKKKK.RR.",
        "..KKHHHHHHHHKRRK",
        ".KHHHHHHHHHHHKRK",
        ".KHhhHHHHHHHHHK.",
        "KHhHHHHHHHHHHHHK",
        "KHHHHSHHHHSHHHHK",
    ]

    static func face(_ face: Face) -> [String] {
        switch face {
        case .normal: [
            "KHHSSSSSSSSSSHHK",
            "KHSSEWSSSSEWSSHK",
            "KHSSEESSSSEESSHK",
        ]
        case .blink: [
            "KHHSSSSSSSSSSHHK",
            "KHSSSSSSSSSSSSHK",
            "KHSKKKSSSSKKKSHK",
        ]
        case .happy: [
            "KHHSKSSSSSSKSHHK",
            "KHSKSKSSSSKSKSHK",
            "KHSSSSSSSSSSSSHK",
        ]
        }
    }

    static let body = [
        "KHSPSSSSSSSSPSHK",
        ".KHSSSSssSSSSHK.",
        ".KHHKSSSSSSKHHK.",
        "..KHKKWWWWKKHK..",
        "...KDDWRRWDDK...",
        "..KSDDDRRDDDSK..",
        "..KSDDDDDDDDSK..",
        "..KKDDDDDDDDKK..",
        ".KDDDDDDDDDDDDK.",
        ".KdDdDdDdDdDdDK.",
        "..KKKKKKKKKKKK..",
    ]

    static func legs(_ legs: Legs) -> [String] {
        switch legs {
        case .stand: [
            "....KLK..KLK....",
            "....KLK..KLK....",
            "...KBBK..KBBK...",
        ]
        case .stride: [
            "...KLK....KLK...",
            "..KLK......KLK..",
            ".KBBK......KBBK.",
        ]
        case .together: [
            "......KLLK......",
            "......KLLK......",
            ".....KBBBBK.....",
        ]
        }
    }

    static func frame(face f: Face, legs l: Legs) -> [String] {
        head + face(f) + body + legs(l)
    }

    static let heart = [
        ".KK.KK.",
        "KRRKRRK",
        "KRWRRRK",
        ".KRRRK.",
        "..KRK..",
        "...K...",
    ]
}
