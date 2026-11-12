from sprite_engine import *

ID = "nijika"
NAME = "伊地知虹夏"
W, H, OY = 48, 72, 4
ORDER = 0
OUTFITS = [("uniform", "制服"), ("casual", "私服")]
ACCESSORIES = ["cap", "glasses", "ribbon"]
ARMS = ("down", "drumLeft", "drumRight", "flailLeft", "flailRight", "bothUp", "peace", "heart", "behindHead", "typeLeft", "typeRight", "grab", "peek")
LEGS = ("stand", "together", "sit", "kickLeft", "kickRight", "dangleLeft", "dangleRight")
configure(W, H, OY)

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
CX = 24
HEAD = (CX, 15, 13.5, 13)
FACE_POLY = [(14, 10), (34, 10), (35, 17), (34, 22), (31, 26.5), (26.5, 29), (21.5, 29), (17, 26.5), (14, 22), (13, 17)]


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
    L.paint(poly(FACE_POLY), "S", "face")
    L.paint(poly([(10.5, 16), (14, 12), (16.5, 34), (13, 36), (10.5, 30)]), "H", "lock")
    L.paint(poly([(37.5, 16), (34, 12), (31.5, 34), (35, 36), (37.5, 30)]), "H", "lock")
    L.shade(line((13, 22), (14, 34), 0.6), "G", {"lock"})
    L.shade(line((35, 22), (34, 34), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly([(10.5, 9), (37.5, 9), (37.5, 21), (35.5, 16.5), (33.5, 12.5), (31.5, 16), (29, 12), (26.5, 16.5),
                   (24, 12), (21.5, 16.5), (19, 12), (16.5, 16), (14.5, 12.5), (12.5, 16.5), (10.5, 21)])
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    L.shade(where(poly(FACE_POLY), lambda x, y: L.g[y - 1 + OY][x] == "bangs"), "s", {"face"})
    L.paint(poly([(21.5, 3.5), (21.5, -3.5), (28, 3.5)]), "H", "ahoge")
    L.shade(line((22.5, -1), (22.5, 2.5), 0.5), "h", {"ahoge"})
    L.paint(rect(35, 6, 38, 10), "R", "tie")
    return L.outline().rows()


def arm_pts(shoulder, elbow, hand, reach=0.6):
    upper = line(shoulder, elbow, 1.7)
    lower = line(elbow, hand, 1.5)
    sl = line(shoulder, (shoulder[0] + (elbow[0] - shoulder[0]) * reach, shoulder[1] + (elbow[1] - shoulder[1]) * reach), 2.2)
    return upper + lower, sl, ellipse(hand[0], hand[1], 1.8, 1.8)


def front_arms(kind, outfit):
    L = Layer()
    LS, RS = (18, 31), (30, 31)
    down_l = (LS, (16, 37), (15.5, 43))
    down_r = (RS, (32, 37), (32.5, 43))
    up_l = (LS, (12, 25), (11, 18))
    up_r = (RS, (36, 25), (37, 18))
    poses = {
        "down": (down_l, down_r),
        "drumLeft": ((LS, (12, 31), (12, 24)), (RS, (34, 37), (30, 40))),
        "drumRight": ((LS, (14, 37), (18, 40)), (RS, (36, 31), (36, 24))),
        "flailLeft": (up_l, (RS, (35, 37), (38, 42))),
        "flailRight": ((LS, (13, 37), (10, 42)), up_r),
        "bothUp": (up_l, up_r),
        "peace": ((LS, (12, 34), (13.5, 25)), down_r),
        "heart": ((LS, (12.5, 38), (22, 33.5)), (RS, (35.5, 38), (26, 33.5))),
        "behindHead": ((LS, (9.5, 23), (12.5, 12)), (RS, (38.5, 23), (35.5, 12))),
        "typeLeft": ((LS, (14.5, 38), (20.5, 38.5)), (RS, (33.5, 38), (27.5, 41))),
        "typeRight": ((LS, (14.5, 38), (20.5, 41)), (RS, (33.5, 38), (27.5, 38.5))),
        "grab": ((LS, (9, 22), (8.5, 4)), (RS, (30, 31), (39.5, 4)) if False else (RS, (39, 22), (39.5, 4))),
        "peek": ((LS, (11.5, 35), (9.5, 33)), (RS, (36.5, 35), (38.5, 33))),
    }
    sticks = {
        "drumLeft": [((12, 24), (9, 16)), ((30, 40), (24, 44))],
        "drumRight": [((36, 24), (39, 16)), ((18, 40), (24, 44))],
    }
    casual = outfit == "casual"
    for s, e, hnd in poses[kind]:
        skin, sleeve, hand = arm_pts(s, e, hnd, 0.4 if casual else 0.6)
        L.paint(skin, "S", "arm")
        L.paint(sleeve, "A" if casual else "W", "sleeve")
        L.paint(hand, "S", "hand")
    for p, q in sticks.get(kind, []):
        L.paint(line(p, q, 0.8), "T", "stick")
    if kind == "grab":
        for ex, hx in ((9, 8.5), (39, 39.5)):
            L.paint(line((ex, 22), (hx, 5), 1.9), "S", "arm")
            L.paint(ellipse(hx, 4, 3, 2.8), "S", "hand")
    if kind == "peace":
        L.paint(line((13, 24), (12, 20), 0.7) + line((14.5, 24), (15.5, 20), 0.7), "S", "hand")
    return L.outline().rows()


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


EYE = [".KKKKK.", "KWFFFWK", "WFWWFFW", "WEWWFEW", "WEFFFEW", "WEEFEEW", ".EeeWE.", "..eee.."]
CLOSED = [".......", ".......", ".......", ".......", ".......", "K.....K", ".KKKKK.", "......."]
HAPPY = [".......", ".......", ".......", ".KKKKK.", "K.....K", ".......", "......."]
LOOK_LEFT = [".KKKKK.", "KFFFWWK", "FWWFFWW", "EWWFEWW", "EFFFEWW", "EEFEEWW", "EeeWE..", ".eee..."]
LOOK_UP = [".KKKKK.", "KWFFFWK", "WFWWFFW", "WEWWFEW", "WEFFFEW", "WWEEEWW", ".WWWWW.", "..KKK.."]
LOOK_DOWN = [".......", ".KKKKK.", "KWWWWWK", "WFFWFFW", "WEFFFEW", "WEEFEEW", ".EeeEE.", "..eee.."]
LOOK_RIGHT = [".KKKKK.", "KWWFFFK", "WWFWWFF", "WWEWWFE", "WWEFFFE", "WWEEFEE", "..EeeWE", "...eee."]
SURPRISED = [".KKKKK.", "KWWWWWK", "WWFFFWW", "WWFWFWW", "WWFFFWW", "WWWWWWW", ".WWWWW.", "..KKK.."]
DIZZY = ["..KKK..", ".K...K.", "K..K..K", "K.K.K.K", "K.K..K.", ".K.KK..", "..K....", "......."]
GT = [".......", "KK.....", "..KK...", "....KKK", "..KK...", "KK.....", "......."]


def face_layer(left, right, mouth="normal", blush_color="p", eye_y=16, lx=15, rx=26, blush=((14, 24), (30, 24))):
    g = [["."] * W for _ in range(H)]
    for pat, x0 in ((left, lx), (right, rx)):
        for dy, r in enumerate(pat):
            for dx, ch in enumerate(r):
                if ch != ".":
                    g[eye_y + dy + OY][x0 + dx] = ch
    for bx, by in blush:
        for x, y in [(bx + i, by) for i in range(4)] + [(bx + i, by + 1) for i in range(1, 3)]:
            if g[y + OY][x] == ".":
                g[y + OY][x] = blush_color
    my = 26 + OY
    if mouth == "normal":
        g[my][23] = g[my][24] = "m"
    elif mouth == "open":
        g[my][23] = g[my][24] = "m"; g[my + 1][23] = g[my + 1][24] = "R"
    elif mouth == "o":
        for x, y in ((23, my), (24, my), (22, my + 1), (25, my + 1), (23, my + 2), (24, my + 2)):
            g[y][x] = "m"
        g[my + 1][23] = g[my + 1][24] = "R"
    return ["".join(r) for r in g]


def front_faces():
    return {
        "normal": face_layer(EYE, EYE),
        "talk": face_layer(EYE, EYE, "open"),
        "talkLeft": face_layer(LOOK_LEFT, LOOK_LEFT, "open"),
        "talkRight": face_layer(LOOK_RIGHT, LOOK_RIGHT, "open"),
        "blink": face_layer(CLOSED, CLOSED),
        "happy": face_layer(HAPPY, HAPPY, "open"),
        "panic": face_layer(GT, mirror(GT), "o"),
        "wink": face_layer(EYE, HAPPY, "open"),
        "surprised": face_layer(SURPRISED, SURPRISED, "o"),
        "shy": face_layer(HAPPY, HAPPY, "normal", blush_color="P"),
        "dizzy": face_layer(DIZZY, mirror(DIZZY), "o"),
        "yawn": face_layer(CLOSED, CLOSED, "o"),
        "lookLeft": face_layer(LOOK_LEFT, LOOK_LEFT),
        "lookRight": face_layer(LOOK_RIGHT, LOOK_RIGHT),
        "lookDown": face_layer(LOOK_DOWN, LOOK_DOWN),
        "lookUp": face_layer(LOOK_UP, LOOK_UP),
    }


# ---------- side (facing right) ----------
SX = 23


HX = -2


def hs(pts):
    return [(x + HX, y) for x, y in pts]


SIDELOCK = [
    ([(21, 12), (25.5, 12), (27, 19), (26.5, 26), (24.5, 31), (22.5, 34), (22.5, 26), (21, 19)],
     [((23.2, 15), (24, 30), "G", 0.5), ((25.5, 15), (26, 22), "h", 0.4)]),
]


def side_body(near_tail, outfit):
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
    L.paint(hs(poly([(22, 9), (30, 9), (33.5, 11.5), (35, 14), (35.5, 17), (35.5, 19.5), (36.5, 21), (35.6, 22), (37, 23), (37, 24.5), (35, 25.5),
                     (32.5, 27), (29.5, 29), (26, 29), (23, 27)])), "S", "face")
    for pts, shade in SIDELOCK:
        L.paint(hs(poly(pts)), "H", "sidelock")
        for p, q, color, w in shade:
            L.shade(hs(line(p, q, w)), color, {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16), (29.5, 12), (27, 16), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    L.shade(where(hs(rect(23, 10, 37, 28)), lambda x, y: L.g[y - 1 + OY][x] == "bangs"), "s", {"face"})
    L.paint(hs(poly([(20.5, 3.5), (20.5, -3.5), (27, 3.5)])), "H", "ahoge")
    L.shade(hs(line((21.5, -1), (21.5, 2.5), 0.5)), "h", {"ahoge"})
    if near_tail:
        L.paint(hs(rect(11, 6, 16, 11)), "R", "tie")
        L.paint(tail, "H", "tail")
        L.shade(hs(line((13, 13), (12.5, 46), 0.6)), "h", {"tail"})
    return L.outline().rows()


def side_arm(swing, outfit):
    L = Layer()
    s = (23, 31)
    e = (23 + swing * 0.5, 37)
    h = (23 + swing, 43)
    casual = outfit == "casual"
    skin, sleeve, hand = arm_pts(s, e, h, 0.4 if casual else 0.6)
    L.paint(skin, "S", "arm"); L.paint(sleeve, "A" if casual else "W", "sleeve"); L.paint(hand, "S", "hand")
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


SEYE = ["...KK", "..KFF", "WWFWF", "WWFWF", "WWEFF", ".WEEF", "...EW", "....e"]
SCLOSED = ["....", "....", "....", "....", "....", "K..K", ".KK.", "...."]


def side_face(pat):
    g = [["."] * W for _ in range(H)]
    for dy, r in enumerate(pat):
        for dx, ch in enumerate(r):
            if ch != ".":
                g[16 + dy + OY][27 + dx] = ch
    for x, y in ((25, 24), (26, 24), (27, 24), (28, 24), (26, 25), (27, 25)):
        if g[y + OY][x] == ".":
            g[y + OY][x] = "p"
    return ["".join(r) for r in g]


def build(outfit):
    sides = {}
    for name, near in (("right", False), ("left", True)):
        side = {
            "body": side_body(near, outfit),
            "face": side_face(SEYE),
            "blink": side_face(SCLOSED),
            "legs": [side_legs(i, outfit) for i in range(WALK_STEPS)],
            "arms": [side_arm(sw, outfit) for sw in (-5, 0, 5, 0)],
        }
        if name == "left":
            side = {k: [mirror(r) for r in v] if k in ("legs", "arms") else mirror(v) for k, v in side.items()}
        sides[name] = side
    return {
        "body": front_body(outfit),
        "faces": front_faces(),
        "arms": {k: front_arms(k, outfit) for k in ARMS},
        "legs": {k: front_legs(k, outfit) for k in LEGS},
        "drops": {"sit": 14},
        "right": sides["right"],
        "left": sides["left"],
    }


ACTIONS = [
    {"name": "walk", "trigger": "idle", "weight": 6, "walk": True, "duration": (40, 160)},
    {"name": "drum", "trigger": "idle", "weight": 3, "duration": (60, 140),
     "frames": [{"face": "happy", "arms": "drumLeft", "ticks": 3}, {"face": "happy", "arms": "drumRight", "ticks": 3}],
     "effect": {"glyph": "note", "period": 24, "dx": [-20, 20]}},
    {"name": "stretch", "trigger": "idle", "weight": 2, "duration": (50, 50),
     "frames": [{"face": "yawn", "arms": "bothUp"}],
     "lift": {"type": "rise", "height": 4, "from": 10, "to": 40},
     "next": {"sleep": 1 / 3}},
    {"name": "sneeze", "trigger": "idle", "weight": 2, "duration": (14, 14),
     "frames": [{"face": "blink", "legs": "together"}],
     "lift": {"type": "rise", "height": 2, "from": 4, "to": 14},
     "next": {"sneezeBurst": 1}},
    {"name": "sneezeBurst", "trigger": "chained", "duration": (12, 12),
     "frames": [{"face": "panic", "legs": "together"}],
     "lift": {"type": "jump", "height": 6},
     "effect": {"glyph": "sneeze", "until": 12, "dx": [18]},
     "next": {"sneezeSniff": 1}},
    {"name": "sneezeSniff", "trigger": "chained", "duration": (36, 36),
     "frames": [{"face": "shy", "legs": "together"}]},
    {"name": "jumpUp", "trigger": "jump", "frames": [{"face": "happy", "legs": "together"}], "next": {"hop": 1}},
    {"name": "hop", "trigger": "idle", "weight": 2, "duration": (45, 45),
     "frames": [{"face": "happy", "legs": "together"}],
     "lift": {"type": "hop", "height": 12, "period": 15}},
    {"name": "doze", "trigger": "idle", "weight": 2,
     "frames": [{"ticks": 10}, {"face": "blink", "ticks": 6}, {"ticks": 6}, {"face": "blink", "ticks": 10}, {"ticks": 4}, {"face": "blink", "ticks": 20}],
     "lift": {"type": "hop", "height": 2, "period": 28},
     "effect": {"glyph": "zzz", "period": 28, "dx": [16]},
     "next": {"dozeWake": 1}},
    {"name": "dozeWake", "trigger": "chained", "duration": (24, 24),
     "frames": [{"face": "surprised"}],
     "lift": {"type": "jump", "height": 8},
     "effect": {"glyph": "exclaim", "until": 18, "dx": [12]}},
    {"name": "dizzySpin", "trigger": "circle", "duration": (80, 80),
     "frames": [{"face": "dizzy", "legs": "together"}],
     "lift": {"type": "hop", "height": 2, "period": 20},
     "effect": {"glyph": "dizzy", "period": 8, "dx": [-14, 0, 14, 0]}},
    {"name": "cheer", "trigger": "idle", "weight": 2, "duration": (40, 40),
     "frames": [{"face": "happy", "arms": "bothUp", "legs": "together"}],
     "lift": {"type": "hop", "height": 10, "period": 10}},
    {"name": "stareSky", "trigger": "idle", "weight": 2, "duration": (68, 136),
     "frames": [{"face": "lookUp", "ticks": 30}, {"face": "blink", "ticks": 4}, {"face": "lookUp", "ticks": 30}, {"face": "blink", "ticks": 4}],
     "effect": {"glyph": "cloud", "period": 50, "dx": [14]}},
    {"name": "petLove", "trigger": "pet", "duration": (50, 50),
     "frames": [{"face": "happy"}],
     "effect": {"glyph": "heart", "period": 10, "dx": [-14, 0, 14, -7, 7]}},
    {"name": "sleep", "trigger": "idle", "weight": 1, "duration": (200, 400),
     "frames": [{"face": "blink", "legs": "sit"}],
     "effect": {"glyph": "zzz", "period": 40, "dx": [16]}},
    {"name": "happy", "trigger": "click", "weight": 1, "duration": (30, 30),
     "frames": [{"face": "happy"}],
     "lift": {"type": "jump", "height": 16},
     "effect": {"glyph": "heart", "dx": [0]}},
    {"name": "peace", "trigger": "click", "weight": 1, "duration": (40, 40),
     "frames": [{"face": "wink", "arms": "peace"}],
     "effect": {"glyph": "heart", "until": 20, "dx": [-16]}},
    {"name": "lookAround", "trigger": "idle", "weight": 2, "duration": (56, 56),
     "frames": [{"face": "lookLeft", "ticks": 10}, {"ticks": 4}, {"face": "lookRight", "ticks": 10}, {"ticks": 4}],
     "effect": {"glyph": "question", "dx": [14]}},
    {"name": "heart", "trigger": "idle", "weight": 1, "duration": (50, 50),
     "frames": [{"face": "happy", "arms": "heart"}],
     "effect": {"glyph": "heart", "period": 25, "dx": [0]}},
    {"name": "surprised", "trigger": "click", "weight": 1, "duration": (24, 24),
     "frames": [{"face": "surprised"}],
     "lift": {"type": "jump", "height": 10},
     "effect": {"glyph": "exclaim", "until": 18, "dx": [12]}},
    {"name": "pet", "trigger": "pet", "duration": (40, 40),
     "frames": [{"face": "shy"}],
     "effect": {"glyph": "heart", "period": 20, "dx": [-12, 12]}},
    {"name": "wheee", "trigger": "throw", "strength": (0, 20),
     "frames": [{"face": "happy", "arms": "bothUp", "legs": "together"}]},
    {"name": "thrown", "trigger": "throw", "strength": (20, 999),
     "frames": [{"face": "panic", "arms": "flailLeft", "legs": "kickRight", "ticks": 2},
                {"face": "panic", "arms": "flailRight", "legs": "kickLeft", "ticks": 2}]},
    {"name": "landHappy", "trigger": "land", "strength": (0, 20), "duration": (30, 30),
     "frames": [{"face": "happy"}],
     "lift": {"type": "jump", "height": 10},
     "effect": {"glyph": "heart", "dx": [0]}},
    {"name": "landSurprised", "trigger": "land", "strength": (20, 40), "duration": (30, 30),
     "frames": [{"face": "surprised", "legs": "together"}],
     "effect": {"glyph": "exclaim", "until": 24, "dx": [12]}},
    {"name": "dizzy", "trigger": "land", "strength": (40, 999), "duration": (60, 60),
     "frames": [{"face": "dizzy", "legs": "sit"}],
     "effect": {"glyph": "dizzy", "period": 8, "dx": [-14, 0, 14, 0]}},
    {"name": "eat", "trigger": "eat", "duration": (60, 60),
     "frames": [{"face": "happy", "ticks": 5}, {"face": "shy", "ticks": 5}],
     "effect": {"glyph": "heart", "period": 30, "dx": [12]}},
    {"name": "flail", "trigger": "drag",
     "frames": [{"face": "panic", "arms": "flailLeft", "legs": "kickRight", "ticks": 3},
                {"face": "panic", "arms": "flailRight", "legs": "kickLeft", "ticks": 3}]},
    {"name": "ledgeSit", "trigger": "ledge", "weight": 2, "duration": (100, 200),
     "frames": [{"legs": "dangleLeft", "ticks": 8}, {"legs": "dangleRight", "ticks": 8}],
     "lift": {"type": "sink", "height": 36}},
    {"name": "sitTop", "trigger": "top", "sit": True, "duration": (60, 200),
     "frames": [{"legs": "dangleLeft", "ticks": 8}, {"legs": "dangleRight", "ticks": 8}],
     "lift": {"type": "sink", "height": 36},
     "next": {"sitTopSmile": 0.3, "sitTopLook": 0.22, "sitTopBlink": 0.27, "sitTop": 0.75}},
    {"name": "sitTopSmile", "trigger": "chained", "sit": True, "duration": (70, 90),
     "frames": [{"face": "happy", "legs": "dangleLeft", "ticks": 8}, {"face": "happy", "legs": "dangleRight", "ticks": 8}],
     "lift": {"type": "sink", "height": 36},
     "next": {"sitTop": 1}},
    {"name": "sitTopLook", "trigger": "chained", "sit": True, "duration": (20, 20),
     "frames": [{"face": "lookLeft", "legs": "dangleLeft", "ticks": 10}, {"face": "lookRight", "legs": "dangleRight", "ticks": 10}],
     "lift": {"type": "sink", "height": 36},
     "next": {"sitTop": 1}},
    {"name": "sitTopBlink", "trigger": "chained", "sit": True, "duration": (8, 8),
     "frames": [{"face": "blink", "legs": "dangleLeft"}],
     "lift": {"type": "sink", "height": 36},
     "next": {"sitTop": 1}},
    {"name": "hang", "trigger": "ledge", "weight": 1, "duration": (80, 160),
     "frames": [{"face": "panic", "arms": "grab", "legs": "dangleLeft", "ticks": 6}, {"face": "panic", "arms": "grab", "legs": "dangleRight", "ticks": 6}],
     "lift": {"type": "sink", "height": 124}},
    {"name": "cling", "trigger": "ledge", "weight": 1, "duration": (60, 100),
     "frames": [{"arms": "grab", "ticks": 8}, {"arms": "grab", "ticks": 8}],
     "lift": {"type": "cling", "height": 117}},
    {"name": "clingTop", "trigger": "top", "duration": (120, 160),
     "frames": [{"arms": "peek"}],
     "lift": {"type": "cling", "height": 68}},
    {"name": "chatNote", "trigger": "near", "duration": (40, 40),
     "frames": [{"face": "happy"}],
     "effect": {"glyph": "note", "dx": [14]}},
    {"name": "chatHeart", "trigger": "near", "duration": (40, 40),
     "frames": [{"face": "happy"}],
     "effect": {"glyph": "heart", "dx": [14]}},
    {"name": "talk", "trigger": "talk", "duration": (30, 50),
     "frames": [{"face": "talk", "ticks": 4}, {"ticks": 4}],
     "effect": {"glyph": "talk", "period": 24, "dx": [14]}},
    {"name": "listen", "trigger": "listen", "duration": (2000, 2000),
     "frames": [{"ticks": 1}]},
    {"name": "ledgePeek", "trigger": "ledge", "weight": 1, "duration": (40, 40),
     "frames": [{"face": "lookDown"}],
     "effect": {"glyph": "question", "dx": [14]}},
    {"name": "lean", "trigger": "wall", "weight": 1, "duration": (80, 160),
     "frames": [{"face": "happy", "arms": "behindHead", "legs": "together"}]},
    {"name": "type", "trigger": "idle", "weight": 8, "apps": TERMINAL_APPS, "duration": (60, 140),
     "frames": [{"face": "lookDown", "arms": "typeLeft", "legs": "sit", "ticks": 2},
                {"face": "lookDown", "arms": "typeRight", "legs": "sit", "ticks": 2}]},
    {"name": "browse", "trigger": "idle", "weight": 6, "apps": BROWSER_APPS, "duration": (80, 80),
     "frames": [{"face": "lookLeft", "legs": "sit", "ticks": 20}, {"face": "lookRight", "legs": "sit", "ticks": 20}],
     "next": {"surprised": 1 / 4}},
    {"name": "groove", "trigger": "idle", "weight": 8, "apps": MUSIC_APPS, "duration": (80, 160),
     "frames": [{"face": "happy", "arms": "bothUp", "legs": "together", "ticks": 5}, {"face": "happy", "legs": "together", "ticks": 5}],
     "lift": {"type": "hop", "height": 6, "period": 10},
     "effect": {"glyph": "note", "period": 20, "dx": [-16, 16]}},
    {"name": "fall", "trigger": "fall", "frames": [{"legs": "together"}]},
]

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
