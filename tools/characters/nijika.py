from sprite_engine import *

ID = "nijika"
NAME = "伊地知虹夏"
W, H, OY = 48, 72, 4
ORDER = 0
ARMS = ("down", "drumLeft", "drumRight", "flailLeft", "flailRight", "bothUp", "peace")
LEGS = ("stand", "together", "sit", "kickLeft", "kickRight")
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
}


# ---------- front ----------
CX = 24
HEAD = (CX, 15, 13.5, 13)
FACE_POLY = [(14, 10), (34, 10), (35, 17), (34, 22), (31, 26.5), (26.5, 29), (21.5, 29), (17, 26.5), (14, 22), (13, 17)]


def front_body():
    L = Layer()
    L.paint(ellipse(*HEAD), "H", "hairback")
    L.paint(poly([(35.5, 6), (41, 6.5), (44.5, 13), (45, 28), (44, 42), (41.5, 52), (39.5, 56), (39, 47), (38.5, 32), (37, 16)]), "H", "tail")
    L.shade(line((40, 10), (41.5, 46), 0.6), "h", {"tail"})
    L.shade(line((43.5, 18), (42.5, 46), 0.6), "G", {"tail"})
    L.paint(rect(22, 26, 26, 30), "S", "neck")
    L.shade(rect(22, 26, 26, 27), "s", {"neck"})
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


def arm_pts(shoulder, elbow, hand):
    upper = line(shoulder, elbow, 1.7)
    lower = line(elbow, hand, 1.5)
    sl = line(shoulder, (shoulder[0] + (elbow[0] - shoulder[0]) * 0.6, shoulder[1] + (elbow[1] - shoulder[1]) * 0.6), 2.2)
    return upper + lower, sl, ellipse(hand[0], hand[1], 1.8, 1.8)


def front_arms(kind):
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
    }
    sticks = {
        "drumLeft": [((12, 24), (9, 16)), ((30, 40), (24, 44))],
        "drumRight": [((36, 24), (39, 16)), ((18, 40), (24, 44))],
    }
    for s, e, hnd in poses[kind]:
        skin, sleeve, hand = arm_pts(s, e, hnd)
        L.paint(skin, "S", "arm")
        L.paint(sleeve, "W", "sleeve")
        L.paint(hand, "S", "hand")
    for p, q in sticks.get(kind, []):
        L.paint(line(p, q, 0.8), "T", "stick")
    if kind == "peace":
        L.paint(line((13, 24), (12, 20), 0.7) + line((14.5, 24), (15.5, 20), 0.7), "S", "hand")
    return L.outline().rows()


def shoe(L, foot, group="shoe"):
    fx, fy = foot
    L.paint(poly([(fx - 2, fy - 0.5), (fx + 2, fy - 0.5), (fx + 3, fy + 1), (fx + 3, fy + 2.5), (fx + 2, fy + 3), (fx - 2, fy + 3), (fx - 3, fy + 2.5), (fx - 3, fy + 1)]), "R", group)


def front_legs(kind):
    L = Layer()
    def leg(hip, knee, foot):
        L.paint(taper(hip, knee, 2.6, 2.3) + taper(knee, foot, 2.3, 2.0), "S", "leg")
        L.paint(where(taper(knee, foot, 2.4, 2.1), lambda x, y: y >= foot[1] - 6), "L", "sock")
        shoe(L, foot)
    if kind == "stand":
        leg((20.5, 50), (20.5, 57), (20.5, 64)); leg((27.5, 50), (27.5, 57), (27.5, 64))
    elif kind == "together":
        leg((20.5, 50), (20.9, 57), (21.2, 64)); leg((27.5, 50), (27.1, 57), (26.8, 64))
    elif kind == "kickLeft":
        leg((20.5, 50), (16, 55), (15, 61)); leg((27.5, 50), (27.5, 57), (27.5, 64))
    elif kind == "kickRight":
        leg((20.5, 50), (20.5, 57), (20.5, 64)); leg((27.5, 50), (32, 55), (33, 61))
    elif kind == "sit":
        L.paint(rect(19, 62, 22, 63) + rect(26, 62, 29, 63), "L", "sock")
        shoe(L, (20.5, 64)); shoe(L, (27.5, 64))
    return L.outline().rows()


EYE = [".KKKKK.", "KWFFFWK", "WFWWFFW", "WEWWFEW", "WEFFFEW", "WEEFEEW", ".EeeWE.", "..eee.."]
CLOSED = [".......", ".......", ".......", ".......", ".......", "K.....K", ".KKKKK.", "......."]
HAPPY = [".......", ".......", ".......", ".KKKKK.", "K.....K", ".......", "......."]
LOOK_LEFT = [".KKKKK.", "KFFFWWK", "FWWFFWW", "EWWFEWW", "EFFFEWW", "EEFEEWW", "EeeWE..", ".eee..."]
LOOK_RIGHT = [".KKKKK.", "KWWFFFK", "WWFWWFF", "WWEWWFE", "WWEFFFE", "WWEEFEE", "..EeeWE", "...eee."]
GT = [".......", "KK.....", "..KK...", "....KKK", "..KK...", "KK.....", "......."]


def face_layer(left, right, mouth="normal", eye_y=16, lx=15, rx=26, blush=((14, 24), (31, 24))):
    g = [["."] * W for _ in range(H)]
    for pat, x0 in ((left, lx), (right, rx)):
        for dy, r in enumerate(pat):
            for dx, ch in enumerate(r):
                if ch != ".":
                    g[eye_y + dy + OY][x0 + dx] = ch
    for bx, by in blush:
        for x, y in [(bx + i, by) for i in range(4)] + [(bx + i, by + 1) for i in range(1, 3)]:
            if g[y + OY][x] == ".":
                g[y + OY][x] = "p"
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
        "blink": face_layer(CLOSED, CLOSED),
        "happy": face_layer(HAPPY, HAPPY, "open"),
        "panic": face_layer(GT, mirror(GT), "o"),
        "wink": face_layer(EYE, HAPPY, "open"),
        "yawn": face_layer(CLOSED, CLOSED, "o"),
        "lookLeft": face_layer(LOOK_LEFT, LOOK_LEFT),
        "lookRight": face_layer(LOOK_RIGHT, LOOK_RIGHT),
    }


# ---------- side (facing right) ----------
SX = 23


HX = -2


def hs(pts):
    return [(x + HX, y) for x, y in pts]


def side_body(near_tail):
    L = Layer()
    tail = hs(poly([(13, 8), (18, 9), (16, 20), (15, 36), (14, 48), (11, 53), (10, 46), (11, 32), (10, 18)]))
    if not near_tail:
        L.paint(tail, "G", "fartail")
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (21.5, 27), (17.5, 30.5), (12.5, 29), (10, 22)])), "H", "hairback")
    L.shade(hs(line((13.5, 21), (14.5, 28), 0.6)), "G", {"hairback"})
    L.paint(rect(21, 26, 25, 30), "S", "neck")
    L.shade(rect(21, 26, 25, 27), "s", {"neck"})
    L.paint(poly([(19, 29.5), (28, 29.5), (30, 32), (29, 41), (18, 41), (18, 32)]), "W", "shirt")
    L.shade(rect(18, 33, 19, 41), "w", {"shirt"})
    L.paint(poly([(18, 40), (29, 40), (32, 51), (15, 51)]), "D", "skirt")
    for x0 in (20, 23, 26):
        L.shade(line((x0 + 0.5, 42), (SX + (x0 + 0.5 - SX) * 1.5, 50), 0.5), "d", {"skirt"})
    L.paint(poly([(27, 29), (32, 30), (31, 34), (27, 33)]) + poly([(28, 32), (31, 38), (27.5, 36)]), "R", "bow")
    L.paint(hs(poly([(22, 9), (30, 9), (33.5, 11.5), (35, 14), (35.5, 17), (35.5, 19.5), (36.5, 21), (35.6, 22), (35.6, 23.5),
                     (34.8, 25), (33, 26.5), (30, 27.5), (26, 27.5), (23, 26)])), "S", "face")
    L.paint(hs(poly([(18, 13), (22, 12), (23, 22), (21.5, 30), (19, 31)])), "H", "lock")
    L.shade(hs(line((20.5, 18), (20.5, 29), 0.5)), "G", {"lock"})
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


def side_arm(swing):
    L = Layer()
    s = (23, 31)
    e = (23 + swing * 0.5, 37)
    h = (23 + swing, 43)
    skin, sleeve, hand = arm_pts(s, e, h)
    L.paint(skin, "S", "arm"); L.paint(sleeve, "W", "sleeve"); L.paint(hand, "S", "hand")
    return L.outline().rows()


def side_legs(step):
    L = Layer()
    def leg(hip, knee, foot, far):
        L.paint(line(hip, knee, 2.0) + line(knee, foot, 1.8), "s" if far else "S", "farleg" if far else "leg")
        L.paint(where(line(knee, foot, 1.9), lambda x, y: y >= foot[1] - 4), "w" if far else "L", "farsock" if far else "sock")
        fx, fy = foot
        L.paint(poly([(fx - 2, fy - 1), (fx + 2, fy - 1), (fx + 4, fy + 1.5), (fx + 4, fy + 3), (fx - 2, fy + 3)]), "R", "farshoe" if far else "shoe")
    if step % 2 == 1:
        leg((23, 49), (23, 56), (23, 63), True); leg((23, 49), (24, 56), (23, 63), False)
    else:
        a, b = ((28, 64), (18, 64)) if step == 0 else ((18, 64), (28, 64))
        leg((23, 50), ((23 + b[0]) / 2, 57), b, True)
        leg((23, 50), ((23 + a[0]) / 2, 57), a, False)
    return L.outline().rows()


SEYE = [".KKKK", "KFFFK", "FWWFW", "EWWFW", "EFFFW", "EEFEW", ".EeE.", "..ee."]
SCLOSED = [".....", ".....", ".....", ".....", ".....", "K...K", ".KKK.", "....."]


def side_face(pat):
    g = [["."] * W for _ in range(H)]
    for dy, r in enumerate(pat):
        for dx, ch in enumerate(r):
            if ch != ".":
                g[16 + dy + OY][27 + dx] = ch
    for x, y in ((25, 24), (26, 24), (27, 24), (28, 24), (26, 25), (27, 25)):
        if g[y + OY][x] == ".":
            g[y + OY][x] = "p"
    g[24 + OY][32] = "m"
    return ["".join(r) for r in g]


def build():
    sides = {}
    for name, near in (("right", False), ("left", True)):
        side = {
            "body": side_body(near),
            "face": side_face(SEYE),
            "blink": side_face(SCLOSED),
            "legs": [side_legs(i) for i in range(WALK_STEPS)],
            "arms": [side_arm(sw) for sw in (-5, 0, 5, 0)],
        }
        if name == "left":
            side = {k: [mirror(r) for r in v] if k in ("legs", "arms") else mirror(v) for k, v in side.items()}
        sides[name] = side
    return {
        "body": front_body(),
        "faces": front_faces(),
        "arms": {k: front_arms(k) for k in ARMS},
        "legs": {k: front_legs(k) for k in LEGS},
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
    {"name": "hop", "trigger": "idle", "weight": 2, "duration": (45, 45),
     "frames": [{"face": "happy", "legs": "together"}],
     "lift": {"type": "hop", "height": 12, "period": 15}},
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
    {"name": "flail", "trigger": "drag",
     "frames": [{"face": "panic", "arms": "flailLeft", "legs": "kickRight", "ticks": 3},
                {"face": "panic", "arms": "flailRight", "legs": "kickLeft", "ticks": 3}]},
    {"name": "fall", "trigger": "fall", "frames": [{"legs": "together"}]},
]
