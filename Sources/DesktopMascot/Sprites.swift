import AppKit

@MainActor
enum Palette {
    static let colors: [Character: NSColor] = [
        "K": NSColor(srgbRed: 0.20, green: 0.13, blue: 0.17, alpha: 1),
        "H": NSColor(srgbRed: 0.97, green: 0.83, blue: 0.40, alpha: 1),
        "G": NSColor(srgbRed: 0.80, green: 0.62, blue: 0.27, alpha: 1),
        "h": NSColor(srgbRed: 1.00, green: 0.95, blue: 0.70, alpha: 1),
        "S": NSColor(srgbRed: 1.00, green: 0.89, blue: 0.80, alpha: 1),
        "s": NSColor(srgbRed: 0.92, green: 0.70, blue: 0.64, alpha: 1),
        "P": NSColor(srgbRed: 1.00, green: 0.68, blue: 0.72, alpha: 1),
        "W": NSColor(srgbRed: 1.00, green: 1.00, blue: 1.00, alpha: 1),
        "E": NSColor(srgbRed: 0.93, green: 0.36, blue: 0.22, alpha: 1),
        "e": NSColor(srgbRed: 1.00, green: 0.62, blue: 0.42, alpha: 1),
        "R": NSColor(srgbRed: 0.92, green: 0.32, blue: 0.42, alpha: 1),
        "D": NSColor(srgbRed: 0.24, green: 0.29, blue: 0.52, alpha: 1),
        "d": NSColor(srgbRed: 0.16, green: 0.20, blue: 0.40, alpha: 1),
        "w": NSColor(srgbRed: 0.84, green: 0.85, blue: 0.92, alpha: 1),
        "L": NSColor(srgbRed: 0.97, green: 0.97, blue: 0.99, alpha: 1),
        "T": NSColor(srgbRed: 0.66, green: 0.44, blue: 0.24, alpha: 1),
        "B": NSColor(srgbRed: 0.42, green: 0.23, blue: 0.21, alpha: 1),
    ]
}

enum Face {
    case normal, blink, happy, panic, wink, yawn, lookLeft, lookRight
}

enum Legs {
    case stand, together, sit, kickLeft, kickRight
}

enum Arms {
    case down, drumLeft, drumRight, flailLeft, flailRight, bothUp, peace
}

enum Sprites {
    static let width = 21

    static let head = [
        "..........K..........",
        "..........KK.........",
        "..........KhK........",
        "..........KhHK.......",
        ".......KKKKKKK.......",
        ".....KKHhhHHHHKK.....",
        "....KHhhHHHHHHHHKKK..",
        "....KHhHHHHHHHHHRRHK.",
        "...KHHHHHHHHHHHHHKHHK",
        "...KHHHHSHHHSHHHHKHHK",
    ]

    static func face(_ face: Face) -> [String] {
        switch face {
        case .normal: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSSEWSSSEWSSHKHHK",
            "...KHSSEESSSEESSHKHHK",
            "...KHSPeESSSeEPSHKHHK",
        ]
        case .blink: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSSSSSSSSSSSHKHHK",
            "...KHSSSSSSSSSSSHKHHK",
            "...KHSPKKSSSKKPSHKHHK",
        ]
        case .happy: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSSKSSSSSKSSHKHHK",
            "...KHSKSKSSSKSKSHKHHK",
            "...KHSPSSSSSSSPSHKHHK",
        ]
        case .panic: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSSKSSSSSKSSHKHHK",
            "...KHSSSKSSSKSSSHKHHK",
            "...KHSPKSSSSSKPSHKHHK",
        ]
        case .wink: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSSEWSSSSKSSHKHHK",
            "...KHSSEESSSKSKSHKHHK",
            "...KHSPeESSSSSPSHKHHK",
        ]
        case .yawn: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSSSSSSSSSSSHKHHK",
            "...KHSSSSSSSSSSSHKHHK",
            "...KHSPKKSSSKKPSHKHHK",
        ]
        case .lookLeft: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSEWSSSEWSSSHKHHK",
            "...KHSEESSSEESSSHKHHK",
            "...KHPeESSSeEPSSHKHHK",
        ]
        case .lookRight: [
            "...KHHSSSSSSSSSHHKHHK",
            "...KHSSSEWSSSEWSHKHHK",
            "...KHSSSEESSSEESHKHHK",
            "...KHSSPeESSSeEPHKHHK",
        ]
        }
    }

    static func body(_ arms: Arms) -> [String] {
        switch arms {
        case .down: [
            "....KHSSSSsSSSSHK.KHK",
            "....KHHKSSSSSKHHK.KHK",
            ".....KHKRRKRRKHK..KHK",
            "......KwRWWWRwK...KHK",
            ".....KwwWWWWWwwK..KHK",
            ".....KSwWWWWWwSK...K.",
            ".....KKDDDDDDDKK.....",
            "....KDDDDDDDDDDDK....",
            "....KdDdDdDdDdDdK....",
            ".....KKKKKKKKKKK.....",
        ]
        case .drumLeft: [
            "...TKHSSSSsSSSSHK.KHK",
            "...TKHHKSSSSSKHHK.KHK",
            "..KSKKHKRRKRRKHK..KHK",
            "...KwKKwRWWWRwK...KHK",
            "......KwWWWWWwwK..KHK",
            "......KwWWWWWwSKTT.K.",
            ".....KKDDDDDDDKK.....",
            "....KDDDDDDDDDDDK....",
            "....KdDdDdDdDdDdK....",
            ".....KKKKKKKKKKK.....",
        ]
        case .drumRight: [
            "....KHSSSSsSSSSHKTKHK",
            "....KHHKSSSSSKHHKTKHK",
            ".....KHKRRKRRKHKKSKHK",
            "......KwRWWWRwKwK.KHK",
            ".....KwwWWWWWwK...KHK",
            "...TTKSwWWWWWwK....K.",
            ".....KKDDDDDDDKK.....",
            "....KDDDDDDDDDDDK....",
            "....KdDdDdDdDdDdK....",
            ".....KKKKKKKKKKK.....",
        ]
        case .flailLeft: [
            "....KHSSSSsSSSSHK.KHK",
            "....KHHKSSSSSKHHK.KHK",
            "..KSKKHKRRKRRKHK..KHK",
            "...KwKKwRWWWRwK...KHK",
            "......KwWWWWWwwK..KHK",
            "......KwWWWWWwSK...K.",
            ".....KKDDDDDDDKK.....",
            "....KDDDDDDDDDDDK....",
            "....KdDdDdDdDdDdK....",
            ".....KKKKKKKKKKK.....",
        ]
        case .flailRight: [
            "....KHSSSSsSSSSHK.KHK",
            "....KHHKSSSSSKHHK.KHK",
            ".....KHKRRKRRKHKKSKHK",
            "......KwRWWWRwKwK.KHK",
            ".....KwwWWWWWwK...KHK",
            ".....KSwWWWWWwK....K.",
            ".....KKDDDDDDDKK.....",
            "....KDDDDDDDDDDDK....",
            "....KdDdDdDdDdDdK....",
            ".....KKKKKKKKKKK.....",
        ]
        case .bothUp: [
            ".KSKKHSSSSsSSSSHK.KHK",
            ".KwKKHHKSSSSSKHHK.KHK",
            "..KwKKHKRRKRRKHKKSKHK",
            "...KwKKwRWWWRwKwK.KHK",
            "......KwWWWWWwK...KHK",
            "......KwWWWWWwK....K.",
            ".....KKDDDDDDDKK.....",
            "....KDDDDDDDDDDDK....",
            "....KdDdDdDdDdDdK....",
            ".....KKKKKKKKKKK.....",
        ]
        case .peace: [
            "KSKSKHSSSSsSSSSHK.KHK",
            "KSSKKHHKSSSSSKHHK.KHK",
            "..KwKKHKRRKRRKHK..KHK",
            "...KwKKwRWWWRwK...KHK",
            "......KwWWWWWwwK..KHK",
            "......KwWWWWWwSK...K.",
            ".....KKDDDDDDDKK.....",
            "....KDDDDDDDDDDDK....",
            "....KdDdDdDdDdDdK....",
            ".....KKKKKKKKKKK.....",
        ]
        }
    }

    static func legs(_ legs: Legs) -> [String] {
        switch legs {
        case .stand: [
            ".......KLK.KLK.......",
            ".......KLK.KLK.......",
            "......KRRK.KRRK......",
        ]
        case .together: [
            ".........KLK.........",
            ".........KLK.........",
            "........KRRRK........",
        ]
        case .sit: [
            "......KRRK.KRRK......",
        ]
        case .kickLeft: [
            "......KLK..KLK.......",
            ".....KRRK..KLK.......",
            "...........KRRK......",
        ]
        case .kickRight: [
            ".......KLK..KLK......",
            ".......KLK..KRRK.....",
            "......KRRK...........",
        ]
        }
    }

    static func frame(face f: Face, arms a: Arms = .down, legs l: Legs) -> [String] {
        head + face(f) + body(a) + legs(l)
    }

    static let rightHead = [
        ".........K...........",
        ".........KK..........",
        ".........KhK.........",
        ".........KhHK........",
        "......KKKKKKKK.......",
        ".....KKHHhhhHHKK.....",
        "....KHHHhhHHHHHHK....",
        "....KHHhHHHHHHHHHK...",
        "....KHHHHHHHHHHHHHK..",
        "....KHHHHHHHHHHHHHK..",
    ]

    static func rightFace(_ face: Face) -> [String] {
        switch face {
        case .blink: [
            "....KHHHHHHHHHHSSSK..",
            "....KHHHHHHHHSSSSSK..",
            "....KHHHHHHHHSSSSSSK.",
            "....KHHHHHHHHSPKKSK..",
        ]
        default: [
            "....KHHHHHHHHHHSSSK..",
            "....KHHHHHHHHSSEWSK..",
            "....KHHHHHHHHSSEESSK.",
            "....KHHHHHHHHSPeESK..",
        ]
        }
    }

    static let rightBody = [
        "....KHHHHHHHKSSSsK...",
        ".....KGHHHHKKSSKK....",
        "...KGGK.KKWWKRRK.....",
        "...KGGK.KwWWWRRK.....",
        "...KGGK.KwWwWWWK.....",
        "....KGK.KwWwWWWK.....",
        "....K...KDDSDDDK.....",
        ".......KDDDDDDDDK....",
        ".......KdDdDdDdDK....",
        "........KKKKKKKK.....",
    ]

    static let rightLegs = [
        [
            ".........KLLLK.......",
            "........KwK.KLK......",
            ".......KRRK.KRRK.....",
        ],
        [
            "..........KLK........",
            "..........KLK........",
            "..........KLK........",
            "..........KRRK.......",
        ],
        [
            ".........KLLLK.......",
            "........KLK.KwK......",
            ".......KRRK.KRRK.....",
        ],
        [
            "..........KLK........",
            "..........KLK........",
            "..........KLK........",
            "..........KRRK.......",
        ],
    ]

    static let leftHead = [
        "...........K.........",
        "..........KK.........",
        ".........KhK.........",
        "........KHhK.........",
        ".......KKKKKKKK......",
        ".....KKHHhhhHHKKK....",
        "....KHHHHHHhhHHHHK...",
        "...KHHHHHHHHHhHKRRK..",
        "..KHHHHHHHHHHHHKHHK..",
        "..KHHHHHHHHHHHHKHHK..",
    ]

    static func leftFace(_ face: Face) -> [String] {
        switch face {
        case .blink: [
            "..KSSSHHHHHHHHHKHHK..",
            "..KSSSSSHHHHHHHKHHK..",
            ".KSSSSSSHHHHHHHKHHK..",
            "..KSKKPSHHHHHHHKHHK..",
        ]
        default: [
            "..KSSSHHHHHHHHHKHHK..",
            "..KSWESSHHHHHHHKHHK..",
            ".KSSEESSHHHHHHHKHHK..",
            "..KSEePSHHHHHHHKHHK..",
        ]
        }
    }

    static let leftBody = [
        "...KsSSSKHHHHHHKHK...",
        "....KKSSKKHHHKKHK....",
        ".....KRRKWWKK.KHHK...",
        ".....KRRWWWwK.KHHK...",
        ".....KWWWwWwK.KHHK...",
        ".....KWWWwWwK.KHK....",
        ".....KDDDSDDK...K....",
        "....KDDDDDDDDK.......",
        "....KDdDdDdDdK.......",
        ".....KKKKKKKK........",
    ]

    static let leftLegs = [
        [
            ".......KLLLK.........",
            "......KLK.KwK........",
            ".....KRRK.KRRK.......",
        ],
        [
            "........KLK..........",
            "........KLK..........",
            "........KLK..........",
            ".......KRRK..........",
        ],
        [
            ".......KLLLK.........",
            "......KwK.KLK........",
            ".....KRRK.KRRK.......",
        ],
        [
            "........KLK..........",
            "........KLK..........",
            "........KLK..........",
            ".......KRRK..........",
        ],
    ]

    static func walkFrame(face f: Face, step: Int, facingLeft: Bool) -> [String] {
        facingLeft
            ? leftHead + leftFace(f) + leftBody + leftLegs[step]
            : rightHead + rightFace(f) + rightBody + rightLegs[step]
    }

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
