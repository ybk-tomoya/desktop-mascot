from sprite_engine import *
from base_character import *

ID = "akane"
NAME = "遊佐あかね"
W, H, OY = 48, 72, 4
ORDER = 4
OUTFITS = [("track", "ジャージ"), ("knit", "ニット＋ジーンズ")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "H": (0.80, 0.45, 0.33),
    "G": (0.62, 0.31, 0.24),
    "h": (0.93, 0.63, 0.48),
    "Y": (0.90, 0.58, 0.72),
    "S": (1.00, 0.90, 0.83),
    "s": (0.93, 0.72, 0.66),
    "p": (1.00, 0.78, 0.80),
    "P": (0.96, 0.58, 0.64),
    "W": (1.00, 1.00, 1.00),
    "E": (0.30, 0.48, 0.80),
    "F": (0.14, 0.22, 0.45),
    "e": (0.62, 0.76, 0.95),
    "R": (0.92, 0.38, 0.42),
    "m": (0.78, 0.38, 0.40),
    "N": (0.25, 0.29, 0.46),
    "n": (0.18, 0.21, 0.35),
    "a": (0.86, 0.86, 0.90),
    "D": (0.46, 0.47, 0.51),
    "d": (0.35, 0.36, 0.40),
    "Q": (0.90, 0.68, 0.64),
    "b": (0.20, 0.18, 0.21),
    "A": (0.92, 0.72, 0.32),
    "c": (0.78, 0.56, 0.22),
    "B": (0.18, 0.17, 0.22),
    "J": (0.62, 0.72, 0.86),
    "j": (0.48, 0.58, 0.74),
    "O": (0.82, 0.30, 0.28),
    "o": (0.62, 0.20, 0.20),
    "T": (0.40, 0.28, 0.22),
}


# ---------- front ----------
BANGS = [(37.5, 9), (10.5, 9), (10.5, 17), (13, 14), (15, 17), (17.5, 13.5), (20, 16.5), (22.5, 12), (23.5, 10), (24.5, 12),
         (27, 16.5), (29.5, 13.5), (32, 17), (34.5, 14), (37.5, 17)]


def front_clothes(L, outfit):
    if outfit == "knit":
        L.paint(poly([(15.5, 43), (32.5, 43), (33.5, 51), (14.5, 51)]), "J", "denim")
        L.shade(line((24, 44), (24, 50), 0.4), "j", {"denim"})
        L.paint(poly([(17, 29), (31, 29), (33, 32), (34, 45), (14, 45), (15, 32)]), "A", "tee")
        L.shade(rect(13, 44, 35, 44), "c", {"tee"})
        L.paint(rect(20, 24, 28, 30), "A", "turtle")
        L.shade(rect(20, 27, 28, 27), "c", {"turtle"})
        L.paint(poly([(18, 31), (30, 31), (31, 45), (17, 45)]), "B", "dress")
        L.paint(poly([(18, 29), (20, 29), (20, 32), (18, 32)]) + poly([(28, 29), (30, 29), (30, 32), (28, 32)]), "B", "strap")
    else:
        L.paint(poly([(16, 43), (32, 43), (34.5, 51), (13.5, 51)]), "D", "skirt")
        for x0 in (19, 24, 29):
            L.shade(line((x0, 45), (CX + (x0 - CX) * 1.3, 50), 0.5), "d", {"skirt"})
        L.paint(poly([(16.5, 29), (31.5, 29), (34, 33), (35, 45.5), (13, 45.5), (14, 33)]), "N", "hoodie")
        L.shade(rect(13, 44, 35, 45), "W", {"hoodie"})
        L.shade(line((24, 30), (24, 44), 0.4), "n", {"hoodie"})
        L.shade(rect(27, 34, 28, 35), "W", {"hoodie"})
        L.paint(rect(20, 24, 28, 30), "W", "collar")
        L.shade(line((24, 24), (24, 30), 0.4), "a", {"collar"})


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10, 15), (38, 15), (38.5, 22), (37, 27), (11, 27), (9.5, 22)]), "H", "hairback")
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly([(10.5, 15), (13.5, 11), (15.5, 25), (14.5, 30), (11, 28)]), "H", "lock")
    L.paint(poly([(37.5, 15), (34.5, 11), (32.5, 25), (33.5, 30), (37, 28)]), "H", "lock")
    L.shade(where(poly([(10.5, 15), (13.5, 11), (15.5, 25), (14.5, 30), (11, 28)]) + poly([(37.5, 15), (34.5, 11), (32.5, 25), (33.5, 30), (37, 28)]),
                  lambda x, y: y >= 28), "Y", {"lock"})
    L.shade(line((13, 18), (13.5, 24), 0.6) + line((35, 18), (34.5, 24), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    L.shade(line((24, 3), (23.5, 10), 0.5), "G", {"bangs"})
    shade_under_bangs(L)
    return L.outline().rows()


# ---------- side (facing right) ----------
def side_clothes(L, outfit):
    if outfit == "knit":
        L.paint(poly([(19, 43), (28.5, 43), (29, 51), (18.5, 51)]), "J", "denim")
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29.5, 45), (18.5, 45), (19.5, 32)]), "A", "tee")
        L.paint(rect(21, 24, 26, 30), "A", "turtle")
        L.paint(poly([(21, 31), (28, 31), (28.5, 45), (20.5, 45)]), "B", "dress")
    else:
        L.paint(poly([(18.5, 43), (29, 43), (30.5, 51), (17, 51)]), "D", "skirt")
        L.shade(line((25, 45), (26, 50), 0.5), "d", {"skirt"})
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29.5, 45.5), (18.5, 45.5), (19.5, 32)]), "N", "hoodie")
        L.shade(rect(17, 44, 31, 45), "W", {"hoodie"})
        L.paint(rect(21, 24, 26, 30), "W", "collar")


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (22.5, 26), (19.5, 28.5), (13, 28), (10, 24)])), "H", "hairback")
    L.shade(hs(line((13, 20), (14, 26), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    lock = hs(poly([(21, 12), (25.5, 12), (27, 19), (26.5, 25), (25, 29.5), (22.5, 30), (21.5, 24)]))
    L.paint(lock, "H", "sidelock")
    L.shade(where(lock, lambda x, y: y >= 28), "Y", {"sidelock"})
    L.shade(hs(line((23.2, 15), (24, 25), 0.5)), "G", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 14), (35, 17), (33.5, 12.5), (31.5, 16.5), (29.5, 12.5), (27, 16.5), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    return L.outline().rows()


def guitar(L, strum):
    L.paint(line((27, 40), (8, 32), 1.6), "T", "fret")
    L.paint(ellipse(29, 42, 5, 4) + ellipse(25.5, 40.5, 3, 2.6), "O", "guitar")
    L.shade(ellipse(28, 41.5, 1.2, 1.2), "o", {"guitar"})
    hx, hy = strum
    L.paint(ellipse(hx, hy, 1.7, 1.7), "S", "hand")
    L.paint(ellipse(10, 34, 1.7, 1.7), "S", "hand")


PROPS = {
    "guitarUp": lambda L: guitar(L, (28, 39)),
    "guitarDown": lambda L: guitar(L, (29, 43)),
}

SLEEVES = {
    "track": [("N", "W", 1.6, 2.5, "sleeve")],
    "knit": [("A", "c", 1.6, 2.5, "sleeve")],
}

LEGWEAR = {
    "track": legwear(shoe=("sneaker", "Q", "b")),
    "knit": legwear(hip=50, tights=("J", "j"), shoe=("boot", "b")),
}


def build(outfit):
    return build_standard(outfit, front_body=front_body, side_body=side_body, sleeves=SLEEVES, legwear=LEGWEAR,
                          faces=standard_faces(), arms=STANDARD_ARMS + ("guitarUp", "guitarDown"), props=PROPS)


GUITAR = [{"face": "smile", "arms": "guitarUp", "ticks": 5}, {"face": "smile", "arms": "guitarDown", "ticks": 5}]

ACTIONS = standard_actions(
    drop=("heart",),
    change={
        "groove": {"frames": [{"face": "happy", "arms": "guitarUp", "ticks": 4}, {"face": "happy", "arms": "guitarDown", "ticks": 4}],
                   "lift": {"type": "hop", "height": 4, "period": 16}},
        "lean": {"frames": [{"face": "smile", "arms": "behindHead", "legs": "together"}]},
        "talkFun": {"weight": 4},
    },
    add=[
        {"name": "guitar", "trigger": "idle", "weight": 4, "duration": (80, 160),
         "frames": GUITAR,
         "effect": {"glyph": "note", "period": 20, "dx": [-16, 16]}},
        {"name": "chatGuitar", "trigger": "near", "duration": (60, 60),
         "frames": GUITAR,
         "effect": {"glyph": "note", "period": 20, "dx": [14]}},
    ],
)

GLYPH_PALETTE = {"w": (0.97, 0.95, 0.88), "u": (0.90, 0.62, 0.22)}

SNACK = {
    "name": "クラフトビール",
    "glyph": [
        "KKKKKK",
        "KwwwwK",
        "KuuuuK",
        "KuuuuK",
        "KuuuuK",
        ".KuuK.",
        ".KKKK.",
    ],
}
