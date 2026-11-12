from sprite_engine import *
from base_character import *

ID = "botan"
NAME = "上伊那ぼたん"
W, H, OY = 48, 72, 4
ORDER = 1
OUTFITS = [("pajama", "パジャマ"), ("casual", "私服"), ("cami", "キャミ＋短パン"), ("cardigan", "カーディガン"), ("dress", "ワンピース")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "H": (0.85, 0.52, 0.55),
    "G": (0.68, 0.36, 0.42),
    "h": (0.96, 0.74, 0.74),
    "S": (1.00, 0.90, 0.83),
    "s": (0.93, 0.72, 0.66),
    "p": (1.00, 0.78, 0.80),
    "P": (0.96, 0.58, 0.64),
    "W": (1.00, 1.00, 1.00),
    "E": (0.32, 0.45, 0.78),
    "F": (0.15, 0.20, 0.45),
    "e": (0.60, 0.72, 0.93),
    "R": (0.92, 0.38, 0.42),
    "Q": (0.98, 0.76, 0.80),
    "q": (0.90, 0.60, 0.67),
    "M": (0.80, 0.40, 0.50),
    "Z": (1.00, 0.90, 0.92),
    "B": (0.25, 0.22, 0.28),
    "m": (0.78, 0.38, 0.40),
    "J": (0.68, 0.72, 0.92),
    "j": (0.52, 0.57, 0.82),
    "N": (0.36, 0.40, 0.55),
    "n": (0.27, 0.30, 0.43),
    "a": (0.86, 0.84, 0.92),
    "b": (0.14, 0.13, 0.16),
    "C": (0.80, 0.66, 0.56),
    "c": (0.64, 0.50, 0.42),
    "Y": (0.98, 0.86, 0.40),
    "D": (0.86, 0.74, 0.58),
    "d": (0.72, 0.60, 0.46),
    "V": (0.96, 0.93, 0.88),
    "v": (0.82, 0.78, 0.72),
    "t": (0.52, 0.38, 0.42),
    "u": (0.42, 0.30, 0.34),
    "g": (0.28, 0.28, 0.31),
    "I": (0.58, 0.58, 0.64),
}


# ---------- front ----------
PART_X = 18.2
BANGS = [(37.5, 9), (17.5, 9), (17.5, 14.5), (20.5, 16.5), (22.5, 13), (25.5, 17), (27, 13.5), (30, 17.5), (31.5, 14), (35, 18.5), (37, 21), (37.5, 21)]
BANGS_SIDE = [(18, 9), (10.5, 9), (10.5, 21), (12, 17), (13, 14), (14.5, 16.5), (15.7, 13.5), (18, 15.5)]


def ribbon(L, x, y, flip):
    d = -1 if flip else 1
    L.paint(poly([(x, y), (x - 3.5 * d, y - 2.5), (x - 3.5 * d, y + 2.5)]) + poly([(x, y), (x + 2.5 * d, y - 2), (x + 2.5 * d, y + 2)])
            + line((x, y), (x - 1.5 * d, y + 7), 0.8), "B", "ribbon")


def front_clothes(L, outfit):
    if outfit == "casual":
        L.paint(poly([(15.5, 44), (32.5, 44), (34, 51), (25.5, 51), (24, 48.5), (22.5, 51), (14, 51)]), "N", "shorts")
        L.shade(rect(13, 50, 35, 50), "n", {"shorts"})
        L.shade(line((24, 45), (24, 48), 0.4), "n", {"shorts"})
        L.paint(poly([(16.5, 29), (31.5, 29), (34, 33), (36, 45.5), (12, 45.5), (14, 33)]), "J", "hoodie")
        L.shade(rect(12, 45, 36, 45), "j", {"hoodie"})
        L.paint(poly([(17, 26.5), (31, 26.5), (33.5, 31), (14.5, 31)]), "j", "hood")
        L.paint(poly([(17, 40), (31, 40), (32.5, 45), (15.5, 45)]), "j", "pocket")
        L.paint(rect(22, 25, 26, 28) + rect(20, 28, 28, 30), "S", "throat")
        L.shade(rect(22, 29, 26, 29), "s", {"throat"})
        L.paint(line((21.5, 31), (21, 38), 0.4) + line((26.5, 31), (27, 38), 0.4), "W", "frill")
    elif outfit == "cami":
        L.paint(poly([(15.5, 44), (32.5, 44), (34, 50), (25.5, 50), (24, 48), (22.5, 50), (14, 50)]), "W", "shorts")
        L.shade(rect(13, 49, 35, 49), "a", {"shorts"})
        L.paint(poly([(17, 29), (31, 29), (33, 32), (36, 46.5), (12, 46.5), (15, 32)]), "W", "pajama")
        L.shade(line((19, 33), (16.5, 45), 0.5) + line((29, 33), (31.5, 45), 0.5) + line((24, 34), (24, 45), 0.4) + rect(12, 46, 36, 46), "a", {"pajama"})
        L.paint(rect(22, 25, 26, 28) + rect(19, 28, 29, 31), "S", "throat")
        L.shade(rect(22, 29, 26, 29), "s", {"throat"})
        L.paint(poly([(17, 27.5), (20, 29.5), (17, 31.5)]) + poly([(31, 27.5), (28, 29.5), (31, 31.5)]), "W", "strap")
    elif outfit == "cardigan":
        L.paint(poly([(15.5, 44), (32.5, 44), (34, 51), (14, 51)]), "b", "shorts")
        L.paint(poly([(17, 29), (31, 29), (33, 32), (35, 46), (13, 46), (15, 32)]), "W", "pajama")
        L.shade(where(rect(13, 29, 35, 46), lambda x, y: x <= 17 or x >= 31), "a", {"pajama"})
        L.paint(rect(22, 25, 26, 28) + rect(20, 28, 28, 30), "S", "throat")
        L.shade(rect(22, 29, 26, 29), "s", {"throat"})
        L.paint(rect(20, 28, 28, 29), "b", "collar")
        L.paint(poly([(15, 29), (20.5, 29.5), (20.5, 47), (13, 47), (12, 38)]), "C", "cardigan")
        L.paint(poly([(33, 29), (27.5, 29.5), (27.5, 47), (35, 47), (36, 38)]), "C", "cardigan")
        L.shade(line((19.5, 31), (19.5, 46), 0.4) + line((28.5, 31), (28.5, 46), 0.4) + rect(13, 46, 20, 46) + rect(28, 46, 35, 46), "c", {"cardigan"})
        L.shade([(28, 35), (28, 40), (28, 44)], "c", {"cardigan"})
    elif outfit == "dress":
        L.paint(poly([(17, 29), (31, 29), (33, 32), (35, 45.5), (13, 45.5), (15, 32)]), "b", "turtle")
        L.paint(poly([(17.5, 31), (30.5, 31), (32.5, 36), (34.5, 47.5), (13.5, 47.5), (15.5, 36)]), "D", "dress")
        L.paint(poly([(21, 31), (24, 35), (27, 31)]), "b", "turtle")
        L.shade(where(rect(13, 31, 35, 47), lambda x, y: x <= 16 or x >= 32) + rect(13, 47, 35, 47), "d", {"dress"})
        L.paint(rect(16, 38, 32, 40), "d", "sash")
        L.paint(poly([(18.5, 40), (22, 40), (21, 46), (18, 46)]), "d", "sash")
        L.paint(rect(21, 25, 27, 29), "b", "turtle")
        L.paint(poly([(14.5, 29), (20, 29.5), (20, 49), (12.5, 49), (12, 38)]), "V", "cardigan")
        L.paint(poly([(33.5, 29), (28, 29.5), (28, 49), (35.5, 49), (36, 38)]), "V", "cardigan")
        L.shade(line((19, 31), (19, 48), 0.4) + line((29, 31), (29, 48), 0.4) + rect(12, 48, 20, 48) + rect(28, 48, 36, 48), "v", {"cardigan"})
    else:
        L.paint(poly([(15.5, 44), (32.5, 44), (34, 51), (25.5, 51), (24, 48.5), (22.5, 51), (14, 51)]), "Q", "shorts")
        L.shade(rect(13, 50, 35, 50), "M", {"shorts"})
        L.shade(line((24, 45), (24, 48), 0.4), "q", {"shorts"})
        L.paint(poly([(17, 29), (31, 29), (33, 32), (35, 45.5), (13, 45.5), (15, 32)]), "Q", "pajama")
        L.shade(rect(12, 45, 36, 45), "M", {"pajama"})
        L.shade(line((19.5, 35), (18, 44), 0.5) + line((28.5, 35), (30, 44), 0.5) + line((24, 36), (24, 44), 0.4), "q", {"pajama"})
        L.paint(rect(22, 25, 26, 28) + rect(20, 28, 28, 31), "S", "throat")
        L.shade(rect(22, 29, 26, 29), "s", {"throat"})
        L.paint(where(rect(19, 28, 29, 32), lambda x, y: x in (19, 29) or y == 32), "Z", "frill")
        L.paint([(23, 32), (24, 32), (22, 31), (25, 31), (23, 33), (24, 33)], "M", "bow")


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10.5, 15), (37.5, 15), (39, 30), (38.5, 44), (36, 48), (12, 48), (9.5, 44), (9, 30)]), "H", "hairback")
    L.shade(line((11.5, 31), (12, 46), 0.5) + line((36.5, 31), (36, 46), 0.5), "G", {"hairback"})
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly([(10.5, 16), (14, 12), (16.5, 34), (13, 37), (10.5, 30)]), "H", "lock")
    L.paint(poly([(37.5, 16), (34, 12), (31.5, 34), (35, 37), (37.5, 30)]), "H", "lock")
    L.shade(line((13, 22), (14, 34), 0.6), "G", {"lock"})
    L.shade(line((35, 22), (34, 34), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS) + poly(BANGS_SIDE)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    L.shade(line((PART_X + 1.5, 2.5), (PART_X, 9.5), 0.5) + line((PART_X, 9.5), (PART_X - 0.3, 14), 0.5), "G", {"bangs", "hairback"})
    shade_under_bangs(L)
    L.paint(poly([(23, 3.5), (25, -1.5), (27.5, 3.5)]), "H", "ahoge")
    L.paint(poly([(8.5, 9), (12.5, 8), (13, 14), (9.5, 15)]) + poly([(39.5, 9), (35.5, 8), (35, 14), (38.5, 15)]), "H", "bunch")
    ribbon(L, 11, 10, False)
    ribbon(L, 37, 10, True)
    return L.outline().rows()


# ---------- side (facing right) ----------
def side_clothes(L, outfit):
    if outfit == "casual":
        L.paint(poly([(19, 44), (28.5, 44), (29.5, 51), (18, 51)]), "N", "shorts")
        L.shade(rect(17, 50, 30, 50), "n", {"shorts"})
        L.paint(poly([(19.5, 29), (27.5, 29), (29, 32), (30.5, 45.5), (17.5, 45.5), (19, 32)]), "J", "hoodie")
        L.shade(rect(17, 45, 31, 45), "j", {"hoodie"})
        L.paint(poly([(15, 27), (23, 26.5), (23, 31), (17, 32)]), "j", "hood")
        L.paint(poly([(19.5, 40), (28, 40), (29.5, 45), (18, 45)]), "j", "pocket")
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
        L.shade(rect(23, 28, 26, 28), "s", {"throat"})
    elif outfit == "cami":
        L.paint(poly([(19, 44), (28.5, 44), (29.5, 50), (18, 50)]), "W", "shorts")
        L.shade(rect(17, 49, 30, 49), "a", {"shorts"})
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (30, 46.5), (18, 46.5), (19.5, 32)]), "W", "pajama")
        L.shade(line((22.5, 34), (21, 45), 0.5) + line((27, 34), (28.5, 45), 0.5) + rect(18, 46, 30, 46), "a", {"pajama"})
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
        L.shade(rect(23, 28, 26, 28), "s", {"throat"})
        L.paint(poly([(21.5, 27.5), (24.5, 29.5), (21.5, 31.5)]), "W", "strap")
    elif outfit == "cardigan":
        L.paint(poly([(19, 44), (28.5, 44), (29.5, 51), (18, 51)]), "b", "shorts")
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (30, 46), (18, 46), (19.5, 32)]), "W", "pajama")
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
        L.shade(rect(23, 28, 26, 28), "s", {"throat"})
        L.paint(rect(24, 28, 27, 29), "b", "collar")
        L.paint(poly([(18, 29), (26, 29), (27, 32), (28.5, 47), (16.5, 47), (17.5, 33)]), "C", "cardigan")
        L.shade(line((26.5, 31), (27.5, 46), 0.4) + rect(17, 46, 28, 46), "c", {"cardigan"})
    elif outfit == "dress":
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (30, 45.5), (18, 45.5), (19.5, 32)]), "b", "turtle")
        L.paint(poly([(19.5, 31), (27.5, 31), (28.5, 36), (30, 47.5), (17.5, 47.5), (18.5, 36)]), "D", "dress")
        L.shade(rect(17, 47, 30, 47), "d", {"dress"})
        L.paint(rect(19, 38, 29, 40), "d", "sash")
        L.paint(rect(23, 25, 26, 29), "b", "turtle")
        L.paint(poly([(18, 29), (25.5, 29), (26.5, 32), (28.5, 49), (16.5, 49), (17.5, 33)]), "V", "cardigan")
        L.shade(line((25.5, 31), (27, 48), 0.4) + rect(17, 48, 28, 48), "v", {"cardigan"})
    else:
        L.paint(poly([(19, 44), (28.5, 44), (29.5, 51), (18, 51)]), "Q", "shorts")
        L.shade(rect(17, 50, 30, 50), "M", {"shorts"})
        L.paint(poly([(20, 29), (27, 29), (28.5, 32), (30, 45.5), (18, 45.5), (19.5, 32)]), "Q", "pajama")
        L.shade(rect(17, 45, 31, 45), "M", {"pajama"})
        L.shade(line((22.5, 35), (21.5, 44), 0.5) + line((26.5, 35), (28, 44), 0.5), "q", {"pajama"})
        L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
        L.shade(rect(23, 28, 26, 28), "s", {"throat"})
        L.paint(where(rect(23, 28, 28, 31), lambda x, y: x == 28 or y == 31), "Z", "frill")


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (21, 32), (18.5, 46), (13.5, 48.5), (10, 40), (9.5, 24)])), "H", "hairback")
    L.shade(hs(line((13.5, 21), (15, 44), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    L.paint(hs(poly([(21, 12), (25.5, 12), (27, 19), (26.5, 26), (24.5, 31), (22.5, 34), (22.5, 26), (21, 19)])), "H", "sidelock")
    L.shade(hs(line((23.2, 15), (24, 30), 0.5)), "G", {"sidelock"})
    L.shade(hs(line((25.5, 15), (26, 22), 0.4)), "h", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16), (29.5, 12), (27, 16), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    L.paint(hs(poly([(22, 3.5), (24, -1.5), (26.5, 3.5)])), "H", "ahoge")
    L.paint(hs(poly([(9.5, 9), (14, 8), (14.5, 14), (10.5, 15)])), "H", "bunch")
    ribbon(L, 12.5 + HX, 10, False)
    return L.outline().rows()


SLEEVES = {
    "pajama": [("Q", "M", 0.65, 2.4, "sleeve")],
    "casual": [("J", "j", 0.95, 2.4, "sleeve")],
    "cami": [],
    "cardigan": [("C", "c", 1.6, 2.5, "cardigan")],
    "dress": [("b", "g", 1.9, 2.0, "sleeve"), ("V", "v", 1.5, 2.5, "cardigan")],
}

LEGWEAR = {
    "pajama": legwear(feet=True),
    "casual": legwear(feet=True),
    "cami": legwear(hip=51, feet=True, shoe=("slipper", "I", "W")),
    "cardigan": legwear(sock="Y", shoe=("sneaker", "b", "W")),
    "dress": legwear(hip=50, tights=("t", "u"), shoe=("boot", "g")),
}


def build(outfit):
    return build_standard(outfit, front_body=front_body, side_body=side_body, sleeves=SLEEVES, legwear=LEGWEAR,
                          faces=standard_faces("tipsy"), arms=STANDARD_ARMS + ("cheers",), props={"cheers": cup()})


ACTIONS = standard_actions(
    change={
        "eat": {"duration": (70, 70), "frames": [{"face": "tipsy", "arms": "cheers"}],
                "lift": {"type": "hop", "height": 4, "period": 20},
                "effect": {"glyph": "heart", "period": 35, "dx": [14]}},
    },
    add=[
        {"name": "cheers", "trigger": "idle", "weight": 2, "duration": (60, 60),
         "frames": [{"face": "tipsy", "arms": "cheers"}],
         "lift": {"type": "hop", "height": 4, "period": 20},
         "effect": {"glyph": "heart", "period": 30, "dx": [14]}},
        {"name": "talkTipsy", "trigger": "talk", "weight": 2, "mood": "fun", "duration": (50, 90),
         "frames": [{"face": "tipsy", "ticks": 7}, {"face": "shy", "ticks": 7}],
         "effect": {"glyph": "talkTipsy", "period": 45, "dx": [14]}},
    ],
)

GLYPHS = {
    **bubbles("talkTipsy", [".R.R.", "RRRRR", "RRRRR", ".RRR.", "..R.."]),
}

GLYPH_PALETTE = {"w": (0.92, 0.92, 0.88), "b": (0.30, 0.42, 0.75)}

SNACK = {
    "name": "お酒",
    "glyph": [
        "..KK..",
        "..KK..",
        ".KWWK.",
        "KWWWwK",
        "KbbbbK",
        "KWWWwK",
        "KWWWwK",
        ".KKKK.",
    ],
}
