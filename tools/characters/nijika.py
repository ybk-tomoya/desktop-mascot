from sprite_engine import *
from base_character import *

ID = "nijika"
NAME = "伊地知虹夏"
W, H, OY = 48, 72, 4
ORDER = 0
OUTFITS = [("uniform", "制服"), ("casual", "私服")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "H": (0.97, 0.83, 0.40),
    "G": (0.80, 0.62, 0.27),
    "h": (1.00, 0.95, 0.70),
    "S": (1.00, 0.89, 0.80),
    "s": (0.92, 0.70, 0.64),
    "p": (1.00, 0.78, 0.80),
    "P": (1.00, 0.68, 0.72),
    "W": (1.00, 1.00, 1.00),
    "E": (0.80, 0.15, 0.20),
    "F": (0.43, 0.08, 0.12),
    "e": (0.94, 0.45, 0.41),
    "R": (0.92, 0.32, 0.42),
    "D": (0.20, 0.20, 0.27),
    "d": (0.12, 0.12, 0.17),
    "w": (0.84, 0.85, 0.92),
    "L": (0.97, 0.97, 0.99),
    "T": (0.66, 0.44, 0.24),
    "m": (0.78, 0.38, 0.40),
    "A": (0.97, 0.66, 0.22),
    "a": (0.86, 0.50, 0.16),
    "N": (0.30, 0.45, 0.72),
    "n": (0.22, 0.34, 0.58),
}


# ---------- front ----------
def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD), "H", "hairback")
    L.paint(poly([(35.5, 6), (41, 6.5), (44.5, 13), (45, 28), (44, 42), (41.5, 52), (39.5, 56), (39, 47), (38.5, 32), (37, 16)]), "H", "tail")
    L.shade(line((40, 10), (41.5, 46), 0.6), "h", {"tail"})
    L.shade(line((43.5, 18), (42.5, 46), 0.6), "G", {"tail"})
    L.paint(rect(22, 26, 26, 30), "S", "neck")
    L.shade(rect(22, 26, 26, 27), "s", {"neck"})
    if outfit == "casual":
        L.paint(poly([(16, 42), (32, 42), (33.5, 52), (25, 52), (24, 48.5), (23, 52), (14.5, 52)]), "N", "denim")
        L.shade(rect(14, 51, 34, 51), "n", {"denim"})
        L.shade(line((24, 44), (24, 48), 0.4), "n", {"denim"})
        L.paint(poly([(18, 29.5), (30, 29.5), (32, 32), (32, 44), (16, 44), (16, 32)]), "A", "tee")
        L.shade(where(rect(16, 29, 32, 44), lambda x, y: x <= 17 or x >= 31), "a", {"tee"})
        L.paint(ellipse(24, 37, 2.6, 2.6), "W", "emblem")
    else:
        L.paint(poly([(18, 29.5), (30, 29.5), (32, 32), (31, 41), (17, 41), (16, 32)]), "W", "shirt")
        L.shade(where(rect(16, 29, 32, 41), lambda x, y: x <= 17 or x >= 31), "w", {"shirt"})
        L.paint(poly([(17, 40), (31, 40), (34, 51), (14, 51)]), "D", "skirt")
        for x0 in (19, 22, 25, 28):
            L.shade(line((x0 + 0.5, 42), (CX + (x0 + 0.5 - CX) * 1.4, 50), 0.5), "d", {"skirt"})
        L.paint(poly([(17, 28.5), (24, 31), (17, 35)]) + poly([(31, 28.5), (24, 31), (31, 35)]) + rect(22, 29, 26, 33)
                + poly([(22, 32), (18.5, 39.5), (22.5, 40), (24, 33)]) + poly([(26, 32), (29.5, 39.5), (25.5, 40), (24, 33)]), "R", "bow")
    paint_face(L)
    L.paint(poly([(10.5, 16), (14, 12), (16.5, 34), (13, 36), (10.5, 30)]), "H", "lock")
    L.paint(poly([(37.5, 16), (34, 12), (31.5, 34), (35, 36), (37.5, 30)]), "H", "lock")
    L.shade(line((13, 22), (14, 34), 0.6), "G", {"lock"})
    L.shade(line((35, 22), (34, 34), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly([(10.5, 9), (37.5, 9), (37.5, 21), (35.5, 16.5), (33.5, 12.5), (31.5, 16), (29, 12), (26.5, 16.5),
                   (24, 12), (21.5, 16.5), (19, 12), (16.5, 16), (14.5, 12.5), (12.5, 16.5), (10.5, 21)])
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    shade_under_bangs(L)
    L.paint(poly([(21.5, 3.5), (21.5, -3.5), (28, 3.5)]), "H", "ahoge")
    L.shade(line((22.5, -1), (22.5, 2.5), 0.5), "h", {"ahoge"})
    L.paint(rect(35, 6, 38, 10), "R", "tie")
    return L.outline().rows()


def arm_painter(outfit):
    casual = outfit == "casual"
    reach = 0.4 if casual else 0.6

    def paint(L, shoulder, elbow, hand):
        L.paint(line(shoulder, elbow, 1.7) + line(elbow, hand, 1.5), "S", "arm")
        L.paint(line(shoulder, (shoulder[0] + (elbow[0] - shoulder[0]) * reach, shoulder[1] + (elbow[1] - shoulder[1]) * reach), 2.2),
                "A" if casual else "W", "sleeve")
        L.paint(ellipse(hand[0], hand[1], 1.8, 1.8), "S", "hand")
    return paint


def sticks(*pairs):
    def paint(L):
        for p, q in pairs:
            L.paint(line(p, q, 0.8), "T", "stick")
    return paint


STICKS = {
    "drumLeft": sticks(((12, 24), (9, 16)), ((30, 40), (24, 44))),
    "drumRight": sticks(((36, 24), (39, 16)), ((18, 40), (24, 44))),
}


def shoe(L, foot, group="shoe"):
    fx, fy = foot
    L.paint(poly([(fx - 2, fy - 0.5), (fx + 2, fy - 0.5), (fx + 3, fy + 1), (fx + 3, fy + 2.5), (fx + 2, fy + 3), (fx - 2, fy + 3), (fx - 3, fy + 2.5), (fx - 3, fy + 1)]), "R", group)


def front_legs(kind, outfit):
    L = Layer()
    def leg(hip, knee, foot):
        L.paint(taper(hip, knee, 2.6, 2.3) + taper(knee, foot, 2.3, 2.0), "S", "leg")
        L.paint(where(taper(knee, foot, 2.4, 2.1), lambda x, y: y >= foot[1] - (3 if outfit == "casual" else 6)), "L", "sock")
        shoe(L, foot)
    if kind == "stand":
        leg((20.5, 52), (20.5, 57), (20.5, 64)); leg((27.5, 52), (27.5, 57), (27.5, 64))
    elif kind == "together":
        leg((20.5, 52), (20.9, 57), (21.2, 64)); leg((27.5, 52), (27.1, 57), (26.8, 64))
    elif kind == "kickLeft":
        leg((20.5, 52), (16, 55), (15, 61)); leg((27.5, 52), (27.5, 57), (27.5, 64))
    elif kind == "kickRight":
        leg((20.5, 52), (20.5, 57), (20.5, 64)); leg((27.5, 52), (32, 55), (33, 61))
    elif kind == "dangleLeft":
        leg((20.5, 52), (19.5, 54), (19, 59)); leg((27.5, 52), (27.5, 55), (27.5, 62))
    elif kind == "dangleRight":
        leg((20.5, 52), (20.5, 55), (20.5, 62)); leg((27.5, 52), (28.5, 54), (29, 59))
    elif kind == "sit":
        L.paint(rect(19, 62, 22, 63) + rect(26, 62, 29, 63), "L", "sock")
        shoe(L, (20.5, 64)); shoe(L, (27.5, 64))
    return L.outline().rows()


# ---------- side (facing right) ----------
SIDELOCK = [
    ([(21, 12), (25.5, 12), (27, 19), (26.5, 26), (24.5, 31), (22.5, 34), (22.5, 26), (21, 19)],
     [((23.2, 15), (24, 30), "G", 0.5), ((25.5, 15), (26, 22), "h", 0.4)]),
]


def side_body(outfit, near_tail):
    L = Layer()
    tail = hs(poly([(13, 8), (18, 9), (16, 20), (15, 36), (14, 48), (11, 53), (10, 46), (11, 32), (10, 18)]))
    if not near_tail:
        L.paint(tail, "G", "fartail")
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (21.5, 27), (17.5, 30.5), (12.5, 29), (10, 22)])), "H", "hairback")
    L.shade(hs(line((13.5, 21), (14.5, 28), 0.6)), "G", {"hairback"})
    L.paint(rect(21, 26, 25, 30), "S", "neck")
    L.shade(rect(21, 26, 25, 27), "s", {"neck"})
    if outfit == "casual":
        L.paint(poly([(18, 42), (29, 42), (30.5, 52), (16.5, 52)]), "N", "denim")
        L.shade(rect(16, 51, 31, 51), "n", {"denim"})
        L.paint(poly([(19, 29.5), (28, 29.5), (30, 32), (30, 44), (18, 44), (18, 32)]), "A", "tee")
        L.shade(rect(18, 33, 19, 44), "a", {"tee"})
    else:
        L.paint(poly([(20, 29.5), (28, 29.5), (29, 32), (28.5, 41), (20, 41), (20, 32)]), "W", "shirt")
        L.shade(rect(20, 33, 21, 41), "w", {"shirt"})
        L.paint(poly([(19, 40), (28.5, 40), (31, 51), (17, 51)]), "D", "skirt")
        for x0 in (20, 23, 26):
            L.shade(line((x0 + 0.5, 42), (SX + (x0 + 0.5 - SX) * 1.5, 50), 0.5), "d", {"skirt"})
        L.paint(poly([(26.5, 29), (30.5, 30), (29.5, 33.5), (26.5, 33)]) + poly([(27, 32), (29.5, 37), (26.5, 36)]), "R", "bow")
    paint_side_face(L)
    for pts, shade in SIDELOCK:
        L.paint(hs(poly(pts)), "H", "sidelock")
        for p, q, color, w in shade:
            L.shade(hs(line(p, q, w)), color, {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16), (29.5, 12), (27, 16), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    L.paint(hs(poly([(20.5, 3.5), (20.5, -3.5), (27, 3.5)])), "H", "ahoge")
    L.shade(hs(line((21.5, -1), (21.5, 2.5), 0.5)), "h", {"ahoge"})
    if near_tail:
        L.paint(hs(rect(11, 6, 16, 11)), "R", "tie")
        L.paint(tail, "H", "tail")
        L.shade(hs(line((13, 13), (12.5, 46), 0.6)), "h", {"tail"})
    return L.outline().rows()


def side_legs(step, outfit):
    L = Layer()
    def leg(hip, knee, foot, far):
        hip, knee, foot = ((x + 1, y) for x, y in (hip, knee, foot))
        L.paint(line(hip, knee, 2.0) + line(knee, foot, 1.8), "s" if far else "S", "farleg" if far else "leg")
        L.paint(where(line(knee, foot, 1.9), lambda x, y: y >= foot[1] - (2 if outfit == "casual" else 4)), "w" if far else "L", "farsock" if far else "sock")
        fx, fy = foot
        L.paint(poly([(fx - 2, fy - 1), (fx + 2, fy - 1), (fx + 4, fy + 1.5), (fx + 4, fy + 3), (fx - 2, fy + 3)]), "R", "farshoe" if far else "shoe")
    if step % 2 == 1:
        leg((23, 52), (23, 57), (23, 63), True); leg((23, 52), (23, 57), (23, 63), False)
    else:
        a, b = ((28, 64), (18, 64)) if step == 0 else ((18, 64), (28, 64))
        leg((23, 52), ((23 + b[0]) / 2, 57), b, True)
        leg((23, 52), ((23 + a[0]) / 2, 57), a, False)
    return L.outline().rows()


def build(outfit):
    paint = arm_painter(outfit)
    return assemble(
        outfit, front_body=front_body, side_body=side_body,
        front_arms=lambda k, o: front_arms(k, paint, STICKS), front_legs=front_legs,
        side_arm=lambda sw, o: side_arm(sw, paint), side_legs=side_legs,
        faces=standard_faces(), arms=("down", "drumLeft", "drumRight") + STANDARD_ARMS[1:], legs=STANDARD_LEGS)


ACTIONS = standard_actions(
    change={"hop": {"weight": 2}, "cheer": {"weight": 2}, "talkFun": {"weight": 5}},
    add=[
        {"name": "drum", "trigger": "idle", "weight": 3, "duration": (60, 140),
         "frames": [{"face": "happy", "arms": "drumLeft", "ticks": 3}, {"face": "happy", "arms": "drumRight", "ticks": 3}],
         "effect": {"glyph": "note", "period": 24, "dx": [-20, 20]}},
    ],
)

GLYPH_PALETTE = {"O": (0.96, 0.62, 0.20), "o": (0.99, 0.80, 0.40)}

SNACK = {
    "name": "ドリトス",
    "glyph": [
        "....K....",
        "...KoK...",
        "...KOOK..",
        "..KOoOOK.",
        "..KOOOOOK",
        ".KOoOOKK.",
        ".KOOKK...",
        "KKK......",
    ],
}
