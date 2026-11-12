from sprite_engine import *
from base_character import *

ID = "ibuki"
NAME = "砺波いぶき"
W, H, OY = 48, 72, 4
ORDER = 2
OUTFITS = [("room", "部屋着"), ("zip", "ハーフジップ"), ("shirt", "シャツ")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {
    "K": (0.20, 0.15, 0.17),
    "H": (0.80, 0.73, 0.63),
    "G": (0.63, 0.56, 0.48),
    "h": (0.91, 0.87, 0.80),
    "S": (1.00, 0.91, 0.84),
    "s": (0.93, 0.73, 0.66),
    "p": (1.00, 0.80, 0.80),
    "P": (0.96, 0.58, 0.64),
    "W": (1.00, 1.00, 1.00),
    "E": (0.58, 0.44, 0.72),
    "F": (0.30, 0.20, 0.45),
    "e": (0.80, 0.70, 0.92),
    "R": (0.92, 0.38, 0.42),
    "m": (0.78, 0.38, 0.40),
    "a": (0.86, 0.86, 0.90),
    "I": (0.58, 0.56, 0.56),
    "T": (0.64, 0.84, 0.80),
    "t": (0.47, 0.68, 0.66),
    "L": (0.22, 0.22, 0.25),
    "l": (0.15, 0.15, 0.18),
    "A": (0.76, 0.78, 0.82),
    "c": (0.60, 0.62, 0.68),
    "N": (0.42, 0.58, 0.78),
    "n": (0.32, 0.45, 0.64),
    "Y": (0.90, 0.78, 0.45),
    "J": (0.78, 0.88, 0.96),
    "Q": (0.95, 0.55, 0.62),
    "V": (0.62, 0.74, 0.62),
    "v": (0.48, 0.60, 0.50),
    "D": (0.40, 0.48, 0.64),
    "d": (0.30, 0.37, 0.52),
    "u": (0.32, 0.29, 0.29),
}


# ---------- front ----------
BANGS = [(36.5, 9), (11.5, 9), (11.5, 15), (13.5, 13), (15.5, 16.5), (17.5, 13), (20, 17), (22, 13.5), (24.5, 17.5), (26.5, 13.5),
         (29, 17), (31, 13), (33, 16.5), (35, 13), (36.5, 15)]


def front_clothes(L, outfit):
    if outfit == "zip":
        L.paint(poly([(15.5, 43), (32.5, 43), (34.5, 51), (13.5, 51)]), "N", "skirt")
        L.shade(line((29, 44), (25, 51), 0.5) + rect(13, 50, 35, 50), "n", {"skirt"})
        L.shade([(30, 46), (29, 48)], "Y", {"skirt"})
        L.paint(poly([(16.5, 29), (31.5, 29), (34, 33), (35, 44.5), (13, 44.5), (14, 33)]), "A", "hoodie")
        L.shade(rect(13, 37, 35, 41), "W", {"hoodie"})
        L.shade(rect(13, 44, 35, 44), "c", {"hoodie"})
        L.paint(rect(20, 25, 28, 30), "A", "collar")
        L.shade(line((24, 25), (24, 31), 0.4), "c", {"collar", "hoodie"})
    elif outfit == "shirt":
        L.paint(poly([(15.5, 44), (32.5, 44), (34, 50), (14, 50)]), "D", "shorts")
        L.shade(rect(13, 49, 35, 49), "d", {"shorts"})
        L.paint(poly([(17, 29), (31, 29), (33, 32), (35, 46), (13, 46), (15, 32)]), "W", "tee")
        L.shade(rect(13, 45, 35, 45), "a", {"tee"})
        L.paint(rect(22, 25, 26, 28) + rect(20, 28, 28, 30), "S", "throat")
        L.shade(rect(22, 29, 26, 29), "s", {"throat"})
        L.paint(poly([(15, 29), (20.5, 29.5), (20.5, 47), (13, 47), (12, 38)]), "V", "cardigan")
        L.paint(poly([(33, 29), (27.5, 29.5), (27.5, 47), (35, 47), (36, 38)]), "V", "cardigan")
        L.shade(line((19.5, 31), (19.5, 46), 0.4) + line((28.5, 31), (28.5, 46), 0.4) + rect(13, 46, 20, 46) + rect(28, 46, 35, 46), "v", {"cardigan"})
        L.paint(poly([(17, 27.5), (20.5, 29), (20.5, 32), (17.5, 31)]) + poly([(31, 27.5), (27.5, 29), (27.5, 32), (30.5, 31)]), "V", "collar")
    else:
        L.paint(poly([(16.5, 29), (31.5, 29), (34, 33), (36, 49.5), (12, 49.5), (14, 33)]), "T", "hoodie")
        L.shade(rect(12, 48, 36, 49), "t", {"hoodie"})
        L.shade(line((19.5, 35), (18, 46), 0.5) + line((28.5, 35), (30, 46), 0.5), "t", {"hoodie"})
        L.paint(rect(19, 24, 29, 30), "T", "turtle")
        L.shade(rect(19, 27, 29, 27) + [(21, 25), (24, 25), (27, 25), (21, 29), (24, 29), (27, 29)], "t", {"turtle"})


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10, 15), (38, 15), (38.5, 22), (38, 28), (36.5, 31), (11.5, 31), (10, 28), (9.5, 22)]), "H", "hairback")
    L.shade(line((11.5, 22), (12, 30), 0.5) + line((36.5, 22), (36, 30), 0.5), "G", {"hairback"})
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly([(10.5, 15), (14, 11), (16, 27), (14.5, 31), (10.5, 29.5)]), "H", "lock")
    L.paint(poly([(37.5, 15), (34, 11), (32, 27), (33.5, 31), (37.5, 29.5)]), "H", "lock")
    L.shade(line((13, 20), (14, 29), 0.6), "G", {"lock"})
    L.shade(line((35, 20), (34, 29), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    shade_under_bangs(L)
    return L.outline().rows()


# ---------- side (facing right) ----------
def side_clothes(L, outfit):
    if outfit == "zip":
        L.paint(poly([(18.5, 43), (29, 43), (30.5, 51), (17, 51)]), "N", "skirt")
        L.shade(rect(16, 50, 31, 50), "n", {"skirt"})
        L.shade([(28, 46), (28, 48)], "Y", {"skirt"})
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29.5, 44.5), (18.5, 44.5), (19.5, 32)]), "A", "hoodie")
        L.shade(rect(17, 37, 31, 41), "W", {"hoodie"})
        L.shade(rect(17, 44, 31, 44), "c", {"hoodie"})
        L.paint(rect(21, 25, 26, 30), "A", "collar")
    elif outfit == "shirt":
        L.paint(poly([(19, 44), (28.5, 44), (29.5, 50), (18, 50)]), "D", "shorts")
        L.shade(rect(17, 49, 30, 49), "d", {"shorts"})
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29.5, 46), (18.5, 46), (19.5, 32)]), "W", "tee")
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
        L.shade(rect(23, 28, 26, 28), "s", {"throat"})
        L.paint(poly([(18, 29), (26, 29), (27, 32), (28.5, 47), (16.5, 47), (17.5, 33)]), "V", "cardigan")
        L.shade(line((26.5, 31), (27.5, 46), 0.4) + rect(17, 46, 28, 46), "v", {"cardigan"})
    else:
        L.paint(poly([(19.5, 29), (27.5, 29), (29, 32), (30.5, 49.5), (17.5, 49.5), (19, 32)]), "T", "hoodie")
        L.shade(rect(17, 48, 31, 49), "t", {"hoodie"})
        L.shade(line((26.5, 35), (28, 46), 0.5), "t", {"hoodie"})
        L.paint(rect(20, 24, 27, 30), "T", "turtle")
        L.shade(rect(20, 27, 27, 27), "t", {"turtle"})


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (22.5, 29), (20, 31.5), (13, 31.5), (10.5, 28), (10, 22)])), "H", "hairback")
    L.shade(hs(line((13, 21), (14, 30), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    L.paint(hs(poly([(21, 12), (25.5, 12), (27, 19), (26.5, 26), (25.5, 30), (23, 31.5), (21.5, 25)])), "H", "sidelock")
    L.shade(hs(line((23.2, 15), (24, 29), 0.5)), "G", {"sidelock"})
    L.shade(hs(line((25.5, 15), (26, 22), 0.4)), "h", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16.5), (29.5, 12.5), (27, 16.5), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    return L.outline().rows()


SLEEVES = {
    "room": [("T", "t", 1.6, 2.5, "sleeve")],
    "zip": [("A", "c", 1.6, 2.4, "sleeve")],
    "shirt": [("V", "v", 1.5, 2.5, "cardigan")],
}

LEGWEAR = {
    "room": legwear(hip=49, tights=("L", "l"), shoe=("slipper", "I", None)),
    "zip": legwear(hip=51, sock="J", shoe=("sneaker", "W", "Q")),
    "shirt": legwear(hip=50, shoe=("boot", "u")),
}


def build(outfit):
    return build_standard(outfit, front_body=front_body, side_body=side_body, sleeves=SLEEVES, legwear=LEGWEAR,
                          faces=standard_faces("tipsy", "hic"), arms=STANDARD_ARMS + ("cheers",),
                          props={"cheers": cup([(36, 14.5), (41, 14.5), (40.5, 18.5), (36.5, 18.5)])})


ACTIONS = standard_actions(
    drop=("sneeze", "sneezeBurst", "sneezeSniff", "cheer", "heart", "chatHeart"),
    change={
        "hop": {"weight": 4},
        "petLove": {"frames": [{"face": "shy"}]},
        "happy": {"lift": {"type": "jump", "height": 12}},
        "wheee": {"frames": [{"face": "surprised", "arms": "bothUp", "legs": "together"}]},
        "landHappy": {"lift": {"type": "jump", "height": 8}},
        "eat": {"duration": (70, 70), "frames": [{"face": "tipsy", "arms": "cheers"}],
                "lift": {"type": "hop", "height": 4, "period": 20},
                "effect": {"glyph": "heart", "period": 35, "dx": [14]},
                "next": {"hiccup": 0.8}},
    },
    add=[
        {"name": "hiccup", "trigger": "idle", "weight": 2, "duration": (12, 12),
         "frames": [{"face": "hic", "legs": "together"}],
         "lift": {"type": "jump", "height": 5},
         "effect": {"glyph": "hic", "until": 10, "dx": [14]},
         "next": {"hiccupAfter": 1}},
        {"name": "hiccupAfter", "trigger": "chained", "duration": (24, 40),
         "frames": [{"face": "shy", "legs": "together"}],
         "next": {"hiccup": 0.5}},
        {"name": "cheers", "trigger": "idle", "weight": 2, "duration": (60, 60),
         "frames": [{"face": "tipsy", "arms": "cheers"}],
         "lift": {"type": "hop", "height": 4, "period": 20},
         "effect": {"glyph": "heart", "period": 30, "dx": [14]},
         "next": {"hiccup": 1 / 2}},
        {"name": "chatSake", "trigger": "near", "duration": (60, 60),
         "frames": [{"face": "tipsy", "arms": "cheers"}],
         "effect": {"glyph": "heart", "period": 30, "dx": [14]},
         "next": {"hiccup": 1 / 3}},
        {"name": "talkSake", "trigger": "talk", "weight": 2, "mood": "fun", "duration": (50, 90),
         "frames": [{"face": "tipsy", "arms": "cheers", "ticks": 7}, {"face": "shy", "arms": "cheers", "ticks": 7}],
         "effect": {"glyph": "talkSake", "period": 45, "dx": [14]}},
    ],
)

GLYPHS = {
    **bubbles("talkSake", ["..K..", ".KwK.", ".KwK.", "KwwwK", "KbbbK", "KwwwK", ".KKK."]),
    "hic": [".KKK.", "KWWWK", "KWWWK", "KWWWK", ".KKK.", "....K", "...KK"],
}

GLYPH_PALETTE = {"w": (0.95, 0.93, 0.86), "b": (0.30, 0.42, 0.75)}

SNACK = {
    "name": "日本酒",
    "glyph": [
        "..KK..",
        "..KK..",
        ".KwwK.",
        ".KwwK.",
        "KwwwwK",
        "KbbbbK",
        "KwwwwK",
        ".KKKK.",
    ],
}
