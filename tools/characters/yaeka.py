from sprite_engine import *
from base_character import *

ID = "yaeka"
NAME = "北杜やえか"
W, H, OY = 48, 72, 4
ORDER = 5
OUTFITS = [("tiered", "ティアードブラウス"), ("vneck", "Vネックワンピ")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "H": (0.97, 0.85, 0.56),
    "G": (0.83, 0.67, 0.40),
    "h": (1.00, 0.95, 0.80),
    "S": (1.00, 0.91, 0.84),
    "s": (0.93, 0.73, 0.66),
    "p": (1.00, 0.78, 0.80),
    "P": (0.96, 0.58, 0.64),
    "W": (1.00, 1.00, 1.00),
    "E": (0.30, 0.62, 0.48),
    "F": (0.12, 0.32, 0.24),
    "e": (0.62, 0.86, 0.72),
    "R": (0.92, 0.38, 0.42),
    "m": (0.78, 0.38, 0.40),
    "Q": (0.95, 0.75, 0.75),
    "q": (0.84, 0.59, 0.61),
    "J": (0.62, 0.72, 0.84),
    "j": (0.48, 0.58, 0.72),
    "V": (0.97, 0.93, 0.81),
    "v": (0.86, 0.80, 0.65),
    "c": (0.62, 0.45, 0.35),
    "x": (0.82, 0.72, 0.64),
    "u": (0.45, 0.32, 0.25),
}


# ---------- front ----------
SWEEP_L = [(19, 3), (13, 6), (10.5, 12), (10.5, 22), (12.5, 16), (14.5, 11), (18, 8.5)]
SWEEP_R = [(19, 3), (30, 3.5), (35, 6.5), (37.5, 12), (37.5, 22), (35.5, 17.5), (33, 14), (29.5, 12.5), (25, 11.5), (21, 9.5)]
LOCK_L = [(10.5, 16), (13.5, 13), (15.5, 24), (16.5, 32), (15, 38), (16, 44), (13, 47.5), (10.5, 41), (9.5, 30)]
LOCK_R = [(48 - x, y) for x, y in LOCK_L]
BROWS = [(16, 14), (17, 13), (18, 13), (19, 13), (20, 13)]
SIDE_BROW = [(28, 13), (29, 13), (30, 13), (31, 13)]


def brows(rows, pts):
    rows = [list(r) for r in rows]
    for x, y in pts:
        rows[y + OY][x] = "G"
    return ["".join(r) for r in rows]


def front_clothes(L, outfit):
    if outfit == "vneck":
        L.paint(poly([(17, 29), (31, 29), (33, 32), (33, 44), (36, 54), (12, 54), (15, 44), (15, 32)]), "V", "dress")
        L.shade(rect(15, 43, 33, 43) + rect(12, 53, 36, 53), "v", {"dress"})
        L.paint(rect(22, 25, 26, 28) + poly([(19, 28), (29, 28), (24, 34)]), "S", "throat")
        L.paint(line((19, 28.5), (24, 34), 0.6) + line((29, 28.5), (24, 34), 0.6), "c", "collar")
    else:
        L.paint(poly([(17, 29), (31, 29), (33, 32), (34, 40), (36, 48), (12, 48), (14, 40), (15, 32)]), "Q", "pajama")
        L.shade(rect(14, 39, 34, 39) + rect(12, 47, 36, 47) + rect(16, 33, 32, 33), "q", {"pajama"})
        L.shade([(24, 30), (24, 32)], "W", {"pajama"})
        L.paint(rect(22, 25, 26, 28) + rect(20, 28, 28, 30), "S", "throat")
        L.shade(rect(22, 29, 26, 29), "s", {"throat"})


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10.5, 15), (37.5, 15), (39.5, 28), (40, 40), (38.5, 50), (35, 52), (13, 52), (9.5, 50), (8, 40), (8.5, 28)]),
            "H", "hairback")
    L.shade(line((11, 30), (10.5, 48), 0.5) + line((37, 30), (37.5, 48), 0.5), "G", {"hairback"})
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly(LOCK_L) + poly(LOCK_R), "H", "lock")
    L.shade(line((12.5, 20), (13.5, 40), 0.6) + line((35.5, 20), (34.5, 40), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 7.5)
    bangs += poly(SWEEP_L) + poly(SWEEP_R)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 5, 9, 1.8), "h", {"bangs", "hairback"})
    L.shade(line((19, 2.5), (19, 8.5), 0.5) + line((22, 7.5), (33, 10.5), 0.4), "G", {"bangs"})
    shade_under_bangs(L)
    return brows(L.outline().rows(), BROWS + [(47 - x, y) for x, y in BROWS])


# ---------- side (facing right) ----------
def side_clothes(L, outfit):
    if outfit == "vneck":
        L.paint(poly([(19.5, 29), (27.5, 29), (29, 32), (29, 44), (31.5, 54), (16.5, 54), (18.5, 44), (19, 32)]), "V", "dress")
        L.shade(rect(16, 53, 32, 53), "v", {"dress"})
        L.paint(rect(21, 25, 25, 28) + poly([(24, 28), (28, 28), (27, 32)]), "S", "throat")
    else:
        L.paint(poly([(19.5, 29), (27.5, 29), (29, 32), (29.5, 40), (31, 48), (17, 48), (18, 40), (19, 32)]), "Q", "pajama")
        L.shade(rect(17, 39, 30, 39) + rect(16, 47, 32, 47), "q", {"pajama"})
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (22.5, 32), (20.5, 46), (15, 52), (10, 46), (8.5, 30)])), "H", "hairback")
    L.shade(hs(line((12.5, 22), (13.5, 46), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    L.paint(hs(poly([(21, 12), (25, 12), (26.5, 20), (27, 28), (25.5, 35), (26, 42), (23, 45), (22, 36), (21.5, 24)])), "H", "sidelock")
    L.shade(hs(line((23.2, 16), (24, 40), 0.5)), "G", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 7.5 or x <= 21)
    bangs += poly([(21, 7), (31, 6.5), (34, 9), (28, 9.5), (23.5, 13), (21, 14)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 2, 5.5, 8, 1.8)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    return brows(L.outline().rows(), SIDE_BROW)


SLEEVES = {
    "tiered": [("Q", "q", 1.6, 2.5, "sleeve")],
    "vneck": [("V", "v", 1.55, 2.5, "sleeve")],
}

LEGWEAR = {
    "tiered": legwear(hip=48, tights=("J", "j"), shoe=("sneaker", "Q", "W")),
    "vneck": legwear(sock="x", shoe=("sneaker", "u", "c")),
}


def build(outfit):
    return build_standard(outfit, front_body=front_body, side_body=side_body, sleeves=SLEEVES, legwear=LEGWEAR,
                          faces=standard_faces(pout=face_layer(GT, mirror(GT), "normal", "P")))


ACTIONS = standard_actions(
    change={
        "hop": {"weight": 6},
        "cheer": {"weight": 4},
        "happy": {"frames": [{"face": "happy", "arms": "bothUp"}]},
    },
    add=[
        {"name": "pout", "trigger": "idle", "weight": 2, "duration": (50, 50),
         "frames": [{"face": "pout", "legs": "together"}],
         "effect": {"glyph": "anger", "until": 36, "dx": [14]}},
        {"name": "chatPout", "trigger": "near", "duration": (40, 40),
         "frames": [{"face": "pout"}],
         "effect": {"glyph": "anger", "until": 30, "dx": [14]}},
    ],
)

GLYPHS = {
    "anger": ["RR.RR", "R...R", ".....", "R...R", "RR.RR"],
}

GLYPH_PALETTE = {"w": (0.86, 0.88, 0.92), "u": (0.92, 0.72, 0.25)}

SNACK = {
    "name": "缶ビール",
    "glyph": [
        ".KKKK.",
        "KwwwwK",
        "KuuuuK",
        "KuwwuK",
        "KuuuuK",
        "KwwwwK",
        ".KKKK.",
    ],
}
