from sprite_engine import *
from base_character import *

ID = "kanade"
NAME = "郡上かなで"
W, H, OY = 48, 72, 4
ORDER = 3
OUTFITS = [("pinafore", "ジャンパースカート"), ("shirt", "シャツワンピ")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "H": (0.31, 0.28, 0.40),
    "G": (0.22, 0.20, 0.30),
    "h": (0.45, 0.42, 0.56),
    "S": (1.00, 0.91, 0.85),
    "s": (0.93, 0.73, 0.68),
    "p": (1.00, 0.80, 0.82),
    "P": (0.96, 0.58, 0.64),
    "W": (1.00, 1.00, 1.00),
    "E": (0.45, 0.52, 0.72),
    "F": (0.20, 0.24, 0.42),
    "e": (0.72, 0.78, 0.92),
    "R": (0.92, 0.38, 0.42),
    "m": (0.78, 0.40, 0.44),
    "Q": (0.94, 0.80, 0.87),
    "q": (0.82, 0.64, 0.74),
    "D": (0.34, 0.34, 0.37),
    "d": (0.24, 0.24, 0.27),
    "u": (0.34, 0.25, 0.23),
    "a": (0.86, 0.86, 0.90),
    "b": (0.22, 0.21, 0.25),
    "B": (0.15, 0.14, 0.18),
    "O": (0.35, 0.58, 0.40),
    "o": (0.55, 0.78, 0.58),
}


# ---------- front ----------
BANGS = [(37, 9), (11, 9), (11, 16), (14, 15), (17, 16.5), (20, 15.5), (23, 16.5), (26, 15.5), (29, 16.5), (32, 15.5), (35, 16.5), (37, 16)]


def front_clothes(L, outfit):
    if outfit == "shirt":
        L.paint(poly([(17, 29), (31, 29), (33, 32), (34.5, 50), (13.5, 50), (15, 32)]), "W", "shirt")
        L.shade(where(rect(13, 29, 35, 50), lambda x, y: x <= 16 or x >= 32) + rect(13, 49, 35, 49), "a", {"shirt"})
        L.shade(line((24, 31), (24, 49), 0.4), "a", {"shirt"})
        L.shade([(23, 34), (23, 39), (23, 44)], "a", {"shirt"})
        L.paint(rect(16, 38, 32, 39), "a", "sash")
        L.paint(rect(22, 25, 26, 28) + rect(21, 28, 27, 30), "S", "throat")
        L.paint(poly([(19, 27.5), (23.5, 30), (20, 31.5)]) + poly([(29, 27.5), (24.5, 30), (28, 31.5)]), "W", "collar")
    else:
        L.paint(poly([(17, 29), (31, 29), (33, 32), (34, 44), (14, 44), (15, 32)]), "Q", "tee")
        L.paint(rect(22, 25, 26, 28) + rect(20, 28, 28, 30), "S", "throat")
        L.shade(rect(22, 29, 26, 29), "s", {"throat"})
        L.paint(poly([(15.5, 29), (19, 29), (20, 34), (17, 34)]) + poly([(32.5, 29), (29, 29), (28, 34), (31, 34)]), "D", "strap")
        L.paint(poly([(19, 33), (29, 33), (30, 39), (18, 39)]), "D", "dress")
        L.paint(poly([(16.5, 38), (31.5, 38), (36, 60), (12, 60)]), "D", "skirt")
        for x0 in (19, 24, 29):
            L.shade(line((x0, 41), (CX + (x0 - CX) * 1.5, 59), 0.5), "d", {"skirt"})
        L.shade(rect(12, 59, 36, 59), "d", {"skirt"})


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10.5, 15), (37.5, 15), (38.5, 30), (38, 46), (36.5, 52), (11.5, 52), (10, 46), (9.5, 30)]), "H", "hairback")
    L.shade(line((11.5, 30), (12, 50), 0.5) + line((36.5, 30), (36, 50), 0.5), "G", {"hairback"})
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly([(10.5, 16), (14, 12), (16, 36), (13.5, 40), (10.5, 34)]), "H", "lock")
    L.paint(poly([(37.5, 16), (34, 12), (32, 36), (34.5, 40), (37.5, 34)]), "H", "lock")
    L.shade(line((13, 22), (13.5, 36), 0.6), "G", {"lock"})
    L.shade(line((35, 22), (34.5, 36), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    shade_under_bangs(L)
    return L.outline().rows()


# ---------- side (facing right) ----------
def side_clothes(L, outfit):
    if outfit == "shirt":
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29.5, 50), (18, 50), (19.5, 32)]), "W", "shirt")
        L.shade(rect(17, 49, 30, 49), "a", {"shirt"})
        L.paint(rect(18, 38, 29, 39), "a", "sash")
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
        L.paint(poly([(24, 27.5), (27.5, 29.5), (25, 31.5)]), "W", "collar")
    else:
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29, 44), (19, 44), (19.5, 32)]), "Q", "tee")
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
        L.shade(rect(23, 28, 26, 28), "s", {"throat"})
        L.paint(poly([(21, 29), (24, 29), (24.5, 34), (21.5, 34)]), "D", "strap")
        L.paint(poly([(20, 33), (28.5, 33), (29, 39), (19.5, 39)]), "D", "dress")
        L.paint(poly([(19, 38), (29, 38), (32, 60), (15.5, 60)]), "D", "skirt")
        L.shade(line((25, 41), (27, 59), 0.5) + rect(15, 59, 32, 59), "d", {"skirt"})


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (22.5, 32), (20, 48), (14, 52), (10, 44), (9.5, 24)])), "H", "hairback")
    L.shade(hs(line((13.5, 21), (15, 48), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    L.paint(hs(poly([(21, 12), (25.5, 12), (27, 19), (26.5, 27), (25, 34), (22.5, 38), (22.5, 27), (21, 19)])), "H", "sidelock")
    L.shade(hs(line((23.2, 15), (24, 34), 0.5)), "G", {"sidelock"})
    L.shade(hs(line((25.5, 15), (26, 22), 0.4)), "h", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 15.5), (34, 16.5), (31, 15.5), (28, 16.5), (25, 15.5), (22, 16.5), (21, 15)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    return L.outline().rows()


def bottle(L):
    L.paint(rect(38, 9, 39, 13) + poly([(36, 13), (41, 13), (41.5, 21), (35.5, 21)]), "O", "bottle")
    L.shade(rect(37, 15, 37, 19), "o", {"bottle"})


SLEEVES = {
    "pinafore": [("Q", "q", 1.6, 2.5, "sleeve")],
    "shirt": [("W", "a", 1.55, 2.4, "sleeve")],
}

LEGWEAR = {
    "pinafore": legwear(sock="W", shoe=("boot", "u")),
    "shirt": legwear(hip=50, tights=("b", "B"), shoe=("boot", "u")),
}


def build(outfit):
    return build_standard(outfit, front_body=front_body, side_body=side_body, sleeves=SLEEVES, legwear=LEGWEAR,
                          faces=standard_faces("tipsy"), arms=STANDARD_ARMS + ("cheers",), props={"cheers": bottle})


ACTIONS = standard_actions(
    drop=("cheer", "sneeze", "sneezeBurst", "sneezeSniff"),
    change={
        "hop": {"weight": 2},
        "happy": {"lift": {"type": "jump", "height": 10}},
        "eat": {"duration": (70, 70), "frames": [{"face": "tipsy", "ticks": 6}, {"face": "shy", "ticks": 6}],
                "effect": {"glyph": "heart", "period": 35, "dx": [14]}},
        "talkAsk": {"weight": 3},
    },
    add=[
        {"name": "showBottle", "trigger": "idle", "weight": 3, "duration": (60, 60),
         "frames": [{"face": "smile", "arms": "cheers"}],
         "effect": {"glyph": "heart", "from": 20, "until": 50, "dx": [14]}},
        {"name": "talkBottle", "trigger": "talk", "weight": 2, "mood": "fun", "duration": (50, 90),
         "frames": [{"face": "talk", "arms": "cheers", "ticks": 7}, {"face": "smile", "arms": "cheers", "ticks": 7}],
         "effect": {"glyph": "talkFun", "period": 45, "dx": [14]}},
    ],
)

GLYPH_PALETTE = {"w": (0.95, 0.93, 0.88), "u": (0.96, 0.72, 0.30), "g": (0.70, 0.80, 0.30)}

SNACK = {
    "name": "梅酒",
    "glyph": [
        "KKKKKK",
        "KwwwwK",
        "KuuuuK",
        "KugguK",
        "KugguK",
        ".KuuK.",
        "..KK..",
    ],
}
