from sprite_engine import *

ID = "botan"
NAME = "上伊那ぼたん"
W, H, OY = 48, 72, 4
ORDER = 1
ARMS = ("down", "flailLeft", "flailRight", "bothUp", "peace")
LEGS = ("stand", "together", "sit", "kickLeft", "kickRight")
configure(W, H, OY)

PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "H": (0.85, 0.52, 0.55),
    "G": (0.68, 0.36, 0.42),
    "h": (0.96, 0.74, 0.74),
    "S": (1.00, 0.90, 0.83),
    "s": (0.93, 0.72, 0.66),
    "p": (1.00, 0.78, 0.80),
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
}


# ---------- front ----------
CX = 24
HEAD = (CX, 15, 13.5, 13)
FACE_POLY = [(14, 10), (34, 10), (35, 17), (34, 22), (31, 26.5), (26.5, 29), (21.5, 29), (17, 26.5), (14, 22), (13, 17)]


def ribbon(L, x, y, flip):
    d = -1 if flip else 1
    L.paint(poly([(x, y), (x - 3.5 * d, y - 2.5), (x - 3.5 * d, y + 2.5)]) + poly([(x, y), (x + 2.5 * d, y - 2), (x + 2.5 * d, y + 2)])
            + line((x, y), (x - 1.5 * d, y + 7), 0.8), "B", "ribbon")


def front_body():
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10.5, 15), (37.5, 15), (39, 30), (38.5, 44), (36, 48), (12, 48), (9.5, 44), (9, 30)]), "H", "hairback")
    L.shade(line((11.5, 31), (12, 46), 0.5) + line((36.5, 31), (36, 46), 0.5), "G", {"hairback"})
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
    L.paint(poly(FACE_POLY), "S", "face")
    L.paint(poly([(10.5, 16), (14, 12), (16.5, 34), (13, 37), (10.5, 30)]), "H", "lock")
    L.paint(poly([(37.5, 16), (34, 12), (31.5, 34), (35, 37), (37.5, 30)]), "H", "lock")
    L.shade(line((13, 22), (14, 34), 0.6), "G", {"lock"})
    L.shade(line((35, 22), (34, 34), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly([(10.5, 9), (37.5, 9), (37.5, 21), (35, 16), (33, 12), (31, 16.5), (28, 11.5), (26.5, 17), (23, 11.5),
                   (20, 16.5), (18.5, 11.5), (16, 16), (14, 12.5), (12.5, 17), (10.5, 21)])
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    L.shade(where(poly(FACE_POLY), lambda x, y: L.g[y - 1 + OY][x] == "bangs"), "s", {"face"})
    L.paint(poly([(23, 3.5), (25, -1.5), (27.5, 3.5)]), "H", "ahoge")
    L.paint(poly([(8.5, 9), (12.5, 8), (13, 14), (9.5, 15)]) + poly([(39.5, 9), (35.5, 8), (35, 14), (38.5, 15)]), "H", "bunch")
    ribbon(L, 11, 10, False)
    ribbon(L, 37, 10, True)
    return L.outline().rows()


def arm_pts(shoulder, elbow, hand):
    skin = line(shoulder, elbow, 1.6) + line(elbow, hand, 1.5)
    mid = (shoulder[0] + (elbow[0] - shoulder[0]) * 0.65, shoulder[1] + (elbow[1] - shoulder[1]) * 0.65)
    return skin, line(shoulder, mid, 2.4), line(mid, mid, 2.2), ellipse(hand[0], hand[1], 1.7, 1.7)


def front_arms(kind):
    L = Layer()
    LS, RS = (18, 31), (30, 31)
    down_l = (LS, (16, 37), (15.5, 43))
    down_r = (RS, (32, 37), (32.5, 43))
    up_l = (LS, (12, 25), (11, 18))
    up_r = (RS, (36, 25), (37, 18))
    poses = {
        "down": (down_l, down_r),
        "flailLeft": (up_l, (RS, (35, 37), (38, 42))),
        "flailRight": ((LS, (13, 37), (10, 42)), up_r),
        "bothUp": (up_l, up_r),
        "peace": ((LS, (12, 34), (13.5, 25)), down_r),
    }
    for s, e, hnd in poses[kind]:
        skin, sleeve, cuff, hand = arm_pts(s, e, hnd)
        L.paint(skin, "S", "arm")
        L.paint(hand, "S", "hand")
        L.paint(sleeve, "Q", "sleeve")
        L.shade(cuff, "M", {"sleeve"})
    if kind == "peace":
        L.paint(line((13, 24), (12, 20), 0.7) + line((14.5, 24), (15.5, 20), 0.7), "S", "hand")
    return L.outline().rows()


def foot(L, pos, group="foot"):
    fx, fy = pos
    L.paint(ellipse(fx, fy + 2, 3, 1.7), "S", group)
    L.shade([(int(fx - 1), int(fy + 3)), (int(fx + 1), int(fy + 3))], "s", {group})


def front_legs(kind):
    L = Layer()
    def leg(hip, knee, ft):
        straight = abs((knee[0] - hip[0]) * (ft[1] - hip[1]) - (knee[1] - hip[1]) * (ft[0] - hip[0])) < 8
        L.paint(taper(hip, ft, 2.7, 2.0) if straight else taper(hip, knee, 2.7, 2.3) + taper(knee, ft, 2.3, 2.0), "S", "leg")
        foot(L, ft)
    if kind == "stand":
        leg((20.5, 50), (20.5, 57), (20.5, 64)); leg((27.5, 50), (27.5, 57), (27.5, 64))
    elif kind == "together":
        leg((21, 50), (21, 57), (21, 64)); leg((27, 50), (27, 57), (27, 64))
    elif kind == "kickLeft":
        leg((20.5, 50), (16, 55), (15, 61)); leg((27.5, 50), (27.5, 57), (27.5, 64))
    elif kind == "kickRight":
        leg((20.5, 50), (20.5, 57), (20.5, 64)); leg((27.5, 50), (32, 55), (33, 61))
    elif kind == "sit":
        foot(L, (20.5, 64)); foot(L, (27.5, 64))
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


def side_body():
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (21, 32), (18.5, 46), (13.5, 48.5), (10, 40), (9.5, 24)])), "H", "hairback")
    L.shade(hs(line((13.5, 21), (15, 44), 0.6)), "G", {"hairback"})
    L.paint(poly([(17.5, 44), (29.5, 44), (31, 51), (16, 51)]), "Q", "shorts")
    L.shade(rect(15, 50, 32, 50), "M", {"shorts"})
    L.paint(poly([(19, 29), (28, 29), (30, 32), (31.5, 45.5), (16.5, 45.5), (18, 32)]), "Q", "pajama")
    L.shade(rect(15, 45, 33, 45), "M", {"pajama"})
    L.shade(line((22, 35), (21, 44), 0.5) + line((27.5, 35), (29, 44), 0.5), "q", {"pajama"})
    L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
    L.shade(rect(23, 28, 26, 28), "s", {"throat"})
    L.paint(where(rect(23, 28, 28, 31), lambda x, y: x == 28 or y == 31), "Z", "frill")
    L.paint(hs(poly([(22, 9), (30, 9), (33.5, 11.5), (35, 14), (35.5, 17), (35.5, 19.5), (36.5, 21), (35.6, 22), (35.6, 23.5),
                     (34.8, 25), (33, 26.5), (30, 27.5), (26, 27.5), (23, 26)])), "S", "face")
    L.paint(hs(poly([(18, 13), (22, 12), (23, 22), (21.5, 31), (19, 32)])), "H", "lock")
    L.shade(hs(line((20.5, 18), (20.5, 30), 0.5)), "G", {"lock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16), (29.5, 12), (27, 16), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    L.shade(where(hs(rect(23, 10, 37, 28)), lambda x, y: L.g[y - 1 + OY][x] == "bangs"), "s", {"face"})
    L.paint(hs(poly([(22, 3.5), (24, -1.5), (26.5, 3.5)])), "H", "ahoge")
    L.paint(hs(poly([(9.5, 9), (14, 8), (14.5, 14), (10.5, 15)])), "H", "bunch")
    ribbon(L, 12.5 + HX, 10, False)
    return L.outline().rows()


def side_arm(swing):
    L = Layer()
    s = (23, 31)
    e = (23 + swing * 0.5, 37)
    h = (23 + swing, 43)
    skin, sleeve, cuff, hand = arm_pts(s, e, h)
    L.paint(skin, "S", "arm"); L.paint(hand, "S", "hand"); L.paint(sleeve, "Q", "sleeve"); L.shade(cuff, "M", {"sleeve"})
    return L.outline().rows()


def side_legs(step):
    L = Layer()
    def leg(hip, knee, foot, far):
        L.paint(taper(hip, knee, 2.3, 2.0) + taper(knee, foot, 2.0, 1.7), "s" if far else "S", "farleg" if far else "leg")
        fx, fy = foot
        L.paint(poly([(fx - 1.5, fy - 1.5), (fx + 1, fy - 1.5), (fx + 4, fy + 1.5), (fx + 4, fy + 3), (fx - 2, fy + 3)]), "s" if far else "S", "farfoot" if far else "foot")
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
    for name in ("right", "left"):
        side = {
            "body": side_body(),
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
    {"name": "stretch", "trigger": "idle", "weight": 2, "duration": (50, 50),
     "frames": [{"face": "yawn", "arms": "bothUp"}],
     "lift": {"type": "rise", "height": 4, "from": 10, "to": 40},
     "next": {"sleep": 1 / 3}},
    {"name": "hop", "trigger": "idle", "weight": 5, "duration": (45, 45),
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
