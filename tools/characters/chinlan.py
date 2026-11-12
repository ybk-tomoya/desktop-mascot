from sprite_engine import *
from base_character import *

ID = "chinlan"
NAME = "張景嵐"
W, H, OY = 48, 72, 4
ORDER = 6
OUTFITS = [("jacket", "ジャケット＋パーカー"), ("hoodie", "パーカー")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "H": (0.27, 0.28, 0.39),
    "G": (0.18, 0.18, 0.27),
    "h": (0.43, 0.45, 0.59),
    "S": (1.00, 0.91, 0.84),
    "s": (0.93, 0.73, 0.66),
    "p": (1.00, 0.78, 0.80),
    "P": (0.96, 0.58, 0.64),
    "W": (1.00, 1.00, 1.00),
    "E": (0.72, 0.47, 0.26),
    "F": (0.38, 0.20, 0.10),
    "e": (0.93, 0.74, 0.50),
    "R": (0.92, 0.38, 0.42),
    "m": (0.78, 0.38, 0.40),
    "V": (0.96, 0.93, 0.88),
    "v": (0.82, 0.78, 0.72),
    "N": (0.25, 0.28, 0.41),
    "n": (0.17, 0.19, 0.30),
    "O": (0.95, 0.58, 0.25),
    "L": (0.24, 0.24, 0.27),
    "l": (0.16, 0.16, 0.19),
    "X": (0.80, 0.30, 0.30),
    "b": (0.22, 0.20, 0.22),
    "D": (0.86, 0.22, 0.25),
}


# ---------- front ----------
BANGS = [(37.5, 9), (10.5, 9), (10.5, 18), (12.5, 15), (14.5, 18), (16.5, 14.5), (19, 17.5), (21.5, 13.5), (24.5, 16.5), (27, 13),
         (30, 15.5), (32.5, 12), (35, 14), (37.5, 12)]
LOCK_L = [(10.5, 15), (14, 11), (15.5, 21), (14.5, 26.5), (11, 25.5)]
LOCK_R = [(48 - x, y) for x, y in LOCK_L]


def front_clothes(L, outfit):
    L.paint(poly([(17, 29), (31, 29), (33, 32), (34, 50), (14, 50), (15, 32)]), "V", "hoodie")
    L.shade(rect(14, 49, 34, 49), "v", {"hoodie"})
    L.paint(poly([(19.5, 41), (28.5, 41), (29.5, 45.5), (18.5, 45.5)]), "v", "pocket")
    L.paint(rect(22, 25, 26, 28), "S", "throat")
    L.paint(poly([(17.5, 26.5), (30.5, 26.5), (32, 31), (16, 31)]), "v", "hood")
    if outfit == "jacket":
        L.paint(poly([(13.5, 31), (18, 31), (17.5, 48.5), (12, 48.5), (11.5, 38)]), "N", "cardigan")
        L.paint(poly([(34.5, 31), (30, 31), (30.5, 48.5), (36, 48.5), (36.5, 38)]), "N", "cardigan")
        L.shade(line((17, 32), (16.8, 47.5), 0.5) + line((31, 32), (31.2, 47.5), 0.5), "O", {"cardigan"})


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10, 15), (38, 15), (38.5, 22), (37.5, 25.5), (10.5, 25.5), (9.5, 22)]), "H", "hairback")
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly(LOCK_L) + poly(LOCK_R), "H", "lock")
    L.shade(line((12.5, 18), (13, 24), 0.6) + line((35.5, 18), (35, 24), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    shade_under_bangs(L)
    L.paint(rect(12, 25, 14, 29) + rect(34, 25, 36, 29), "D", "earring")
    return L.outline().rows()


# ---------- side (facing right) ----------
def side_clothes(L, outfit):
    L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29.5, 50), (18, 50), (19.5, 32)]), "V", "hoodie")
    L.shade(rect(17, 49, 30, 49), "v", {"hoodie"})
    L.paint(rect(21, 25, 25, 28), "S", "throat")
    L.paint(poly([(17, 26.5), (23, 26.5), (23, 31), (18, 31.5)]), "v", "hood")
    if outfit == "jacket":
        L.paint(poly([(17.5, 30), (22, 30), (21.5, 48.5), (16.5, 48.5)]), "N", "cardigan")
        L.shade(line((21, 31), (20.8, 47.5), 0.5), "O", {"cardigan"})


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (22.5, 25.5), (19.5, 27), (13, 26.5), (10, 23)])), "H", "hairback")
    L.shade(hs(line((13, 19), (14, 25), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    L.paint(hs(poly([(21, 12), (25.5, 12), (27, 19), (26, 25), (23, 27), (21.5, 22)])), "H", "sidelock")
    L.shade(hs(line((23.2, 15), (24, 24), 0.5)), "G", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 12.5), (35, 15), (33, 12), (31, 15.5), (29, 12.5), (26.5, 16.5), (24.5, 13), (22.5, 17), (21, 14)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    L.paint(hs(rect(24, 25, 26, 29)), "D", "earring")
    return L.outline().rows()


SLEEVES = {
    "jacket": [("N", "n", 1.6, 2.4, "sleeve")],
    "hoodie": [],
}

LEGWEAR = {
    "jacket": legwear(hip=49, tights=("L", "l"), shoe=("sneaker", "X", "b")),
    "hoodie": legwear(hip=49, tights=("L", "l"), shoe=("sneaker", "X", "b")),
}


def build(outfit):
    return build_standard(outfit, front_body=front_body, side_body=side_body, sleeves=SLEEVES, legwear=LEGWEAR,
                          faces=standard_faces("tipsy"), arms=STANDARD_ARMS + ("cheeks", "cheers"), props={"cheers": cup()})


ACTIONS = standard_actions(
    drop=("sneeze", "sneezeBurst", "sneezeSniff"),
    change={
        "talk": {"weight": 3},
        "talkAsk": {"weight": 3},
        "talkWow": {"weight": 2},
        "hop": {"weight": 3},
    },
    add=[
        {"name": "skincare", "trigger": "idle", "weight": 3, "duration": (60, 60),
         "frames": [{"face": "smile", "arms": "cheeks", "ticks": 10}, {"face": "blink", "arms": "cheeks", "ticks": 4}],
         "effect": {"glyph": "sparkle", "period": 30, "dx": [14, -14]}},
        {"name": "cheers", "trigger": "idle", "weight": 2, "duration": (60, 60),
         "frames": [{"face": "tipsy", "arms": "cheers"}],
         "lift": {"type": "hop", "height": 4, "period": 20},
         "effect": {"glyph": "heart", "period": 30, "dx": [14]}},
    ],
)

GLYPHS = {
    "sparkle": ["..y..", "..y..", "yyWyy", "..y..", "..y.."],
}

GLYPH_PALETTE = {"y": (0.98, 0.84, 0.35), "w": (0.95, 0.95, 0.92), "g": (0.30, 0.62, 0.42)}

SNACK = {
    "name": "台湾ビール",
    "glyph": [
        ".KKKK.",
        "KwwwwK",
        "KggggK",
        "KgwwgK",
        "KggggK",
        "KwwwwK",
        ".KKKK.",
    ],
}
