from sprite_engine import *

ID = "botan"
NAME = "上伊那ぼたん"
W, H, OY = 48, 72, 4
ORDER = 1
OUTFITS = [("pajama", "パジャマ"), ("casual", "私服"), ("cami", "キャミ＋短パン"), ("cardigan", "カーディガン"), ("dress", "ワンピース")]
ACCESSORIES = ["cap", "glasses", "ribbon"]
ARMS = ("down", "flailLeft", "flailRight", "bothUp", "peace", "heart", "cheers", "behindHead", "typeLeft", "typeRight", "grab", "peek")
LEGS = ("stand", "together", "sit", "kickLeft", "kickRight", "dangleLeft", "dangleRight")
configure(W, H, OY)

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
CX = 24
HEAD = (CX, 15, 13.5, 13)
FACE_POLY = [(14, 10), (34, 10), (35, 17), (34, 22), (31, 26.5), (26.5, 29), (21.5, 29), (17, 26.5), (14, 22), (13, 17)]


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
    L.paint(poly(FACE_POLY), "S", "face")
    L.paint(poly([(10.5, 16), (14, 12), (16.5, 34), (13, 37), (10.5, 30)]), "H", "lock")
    L.paint(poly([(37.5, 16), (34, 12), (31.5, 34), (35, 37), (37.5, 30)]), "H", "lock")
    L.shade(line((13, 22), (14, 34), 0.6), "G", {"lock"})
    L.shade(line((35, 22), (34, 34), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS) + poly(BANGS_SIDE)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    L.shade(line((PART_X + 1.5, 2.5), (PART_X, 9.5), 0.5) + line((PART_X, 9.5), (PART_X - 0.3, 14), 0.5), "G", {"bangs", "hairback"})
    L.shade(where(poly(FACE_POLY), lambda x, y: L.g[y - 1 + OY][x] == "bangs"), "s", {"face"})
    L.paint(poly([(23, 3.5), (25, -1.5), (27.5, 3.5)]), "H", "ahoge")
    L.paint(poly([(8.5, 9), (12.5, 8), (13, 14), (9.5, 15)]) + poly([(39.5, 9), (35.5, 8), (35, 14), (38.5, 15)]), "H", "bunch")
    ribbon(L, 11, 10, False)
    ribbon(L, 37, 10, True)
    return L.outline().rows()


SLEEVES = {
    "pajama": [("Q", "M", 0.65, 2.4, "sleeve")],
    "casual": [("J", "j", 0.95, 2.4, "sleeve")],
    "cami": [],
    "cardigan": [("C", "c", 1.6, 2.5, "cardigan")],
    "dress": [("b", "g", 1.9, 2.0, "sleeve"), ("V", "v", 1.5, 2.5, "cardigan")],
}


def arm_pts(shoulder, elbow, hand):
    skin = line(shoulder, elbow, 1.6) + line(elbow, hand, 1.5)
    return skin, ellipse(hand[0], hand[1], 1.7, 1.7)


def sleeve_pts(shoulder, elbow, hand, reach, r):
    def lerp(p, q, t):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    if reach <= 1:
        end = lerp(shoulder, elbow, reach)
        pts = line(shoulder, end, r)
    else:
        end = lerp(elbow, hand, reach - 1)
        pts = line(shoulder, elbow, r) + line(elbow, end, r)
    return pts, line(end, end, r - 0.2)


def paint_arm(L, outfit, shoulder, elbow, hand):
    skin, palm = arm_pts(shoulder, elbow, hand)
    L.paint(skin, "S", "arm")
    L.paint(palm, "S", "hand")
    for color, cuff_color, reach, r, group in SLEEVES[outfit]:
        sleeve, cuff = sleeve_pts(shoulder, elbow, hand, reach, r)
        L.paint(sleeve, color, group)
        L.shade(cuff, cuff_color, {group})


def front_arms(kind, outfit):
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
        "heart": ((LS, (12.5, 38), (22, 33.5)), (RS, (35.5, 38), (26, 33.5))),
        "behindHead": ((LS, (9.5, 23), (12.5, 12)), (RS, (38.5, 23), (35.5, 12))),
        "typeLeft": ((LS, (14.5, 38), (20.5, 38.5)), (RS, (33.5, 38), (27.5, 41))),
        "typeRight": ((LS, (14.5, 38), (20.5, 41)), (RS, (33.5, 38), (27.5, 38.5))),
        "grab": ((LS, (9, 22), (8.5, 4)), (RS, (30, 31), (39.5, 4)) if False else (RS, (39, 22), (39.5, 4))),
        "peek": ((LS, (11.5, 35), (9.5, 33)), (RS, (36.5, 35), (38.5, 33))),
        "cheers": (down_l, (RS, (38.5, 28), (38.5, 20))),
    }
    for sh, e, hnd in poses[kind]:
        paint_arm(L, outfit, sh, e, hnd)
    if kind == "cheers":
        L.paint(poly([(35.5, 12.5), (41.5, 12.5), (40.5, 18.5), (36.5, 18.5)]), "W", "cup")
    if kind == "grab":
        for ex, hx in ((9, 8.5), (39, 39.5)):
            L.paint(line((ex, 22), (hx, 5), 1.9), "S", "arm")
            L.paint(ellipse(hx, 4, 3, 2.8), "S", "hand")
    if kind == "peace":
        L.paint(line((13, 24), (12, 20), 0.7) + line((14.5, 24), (15.5, 20), 0.7), "S", "hand")
    return L.outline().rows()


def foot(L, pos, group="foot", rx=3):
    fx, fy = pos
    L.paint(ellipse(fx, fy + 2, rx, 1.7), "S", group)
    L.shade([(int(fx - 1), int(fy + 3)), (int(fx + 1), int(fy + 3))], "s", {group})


def sneaker(L, ft):
    fx, fy = ft
    L.paint(ellipse(fx, fy + 2, 3.4, 2.2), "b", "sneaker")
    L.shade(where(ellipse(fx, fy + 2, 3.4, 2.2), lambda x, y: y >= fy + 3), "W", {"sneaker"})


def boot(L, ft):
    fx, fy = ft
    L.paint(rect(int(fx - 2), int(fy - 4), int(fx + 2), int(fy + 1)) + ellipse(fx, fy + 2, 3.2, 1.9), "g", "boot")


def slipper(L, ft):
    fx, fy = ft
    L.paint(ellipse(fx, fy + 2.3, 3.4, 2.0), "I", "slipper")
    L.shade(rect(int(fx - 2), int(fy + 1), int(fx + 2), int(fy + 1)), "W", {"slipper"})


def front_legs(kind, outfit):
    L = Layer()
    close = kind == "together"
    hy = 50 if outfit == "dress" else 52
    tone, group = ("t", "tights") if outfit == "dress" else ("S", "leg")

    def wear(ft):
        if outfit == "cardigan":
            sneaker(L, ft)
        elif outfit == "dress":
            boot(L, ft)
        elif outfit == "cami":
            slipper(L, ft)

    def leg(hip, knee, ft):
        straight = abs((knee[0] - hip[0]) * (ft[1] - hip[1]) - (knee[1] - hip[1]) * (ft[0] - hip[0])) < 8
        if straight:
            pts = taper(hip, ft, 2.6 if close else 2.7, 2.0)
        else:
            pts = taper(hip, knee, 2.7, 2.3) + taper(knee, ft, 2.3, 2.0) + ellipse(ft[0], ft[1], 2.3, 2.3)
        L.paint(pts, tone, group)
        if outfit == "cardigan":
            L.paint(where(pts, lambda x, y: y >= ft[1] - 4), "Y", "sock")
        if straight and outfit in ("pajama", "casual", "cami"):
            foot(L, ft, rx=2.6 if close else 3)
        wear(ft)
    if kind == "stand":
        leg((20.5, hy), (20.5, 57), (20.5, 64)); leg((27.5, hy), (27.5, 57), (27.5, 64))
    elif kind == "together":
        leg((20.7, hy), (20.7, 57), (20.7, 64)); leg((27.3, hy), (27.3, 57), (27.3, 64))
    elif kind == "kickLeft":
        leg((20.5, hy), (15.5, 55.5), (13.5, 60)); leg((27.5, hy), (27.5, 57), (27.5, 64))
    elif kind == "kickRight":
        leg((20.5, hy), (20.5, 57), (20.5, 64)); leg((27.5, hy), (32.5, 55.5), (34.5, 60))
    elif kind == "dangleLeft":
        leg((20.5, hy), (19.5, 54), (19, 59)); leg((27.5, hy), (27.5, 55), (27.5, 62))
    elif kind == "dangleRight":
        leg((20.5, hy), (20.5, 55), (20.5, 62)); leg((27.5, hy), (28.5, 54), (29, 59))
    elif kind == "sit":
        for ft in ((20.5, 64), (27.5, 64)):
            if outfit in ("pajama", "casual", "cami"):
                foot(L, ft)
            wear(ft)
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
        "blink": face_layer(CLOSED, CLOSED),
        "happy": face_layer(HAPPY, HAPPY, "open"),
        "panic": face_layer(GT, mirror(GT), "o"),
        "wink": face_layer(EYE, HAPPY, "open"),
        "surprised": face_layer(SURPRISED, SURPRISED, "o"),
        "shy": face_layer(HAPPY, HAPPY, "normal", blush_color="P"),
        "dizzy": face_layer(DIZZY, mirror(DIZZY), "o"),
        "tipsy": face_layer(HAPPY, HAPPY, "open", blush_color="P"),
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


def side_body(outfit):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (21, 32), (18.5, 46), (13.5, 48.5), (10, 40), (9.5, 24)])), "H", "hairback")
    L.shade(hs(line((13.5, 21), (15, 44), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    L.paint(hs(poly([(22, 9), (30, 9), (33.5, 11.5), (35, 14), (35.5, 17), (35.5, 19.5), (36.5, 21), (35.6, 22), (37, 23), (37, 24.5), (35, 25.5),
                     (32.5, 27), (29.5, 29), (26, 29), (23, 27)])), "S", "face")
    L.paint(hs(poly([(21, 12), (25.5, 12), (27, 19), (26.5, 26), (24.5, 31), (22.5, 34), (22.5, 26), (21, 19)])), "H", "sidelock")
    L.shade(hs(line((23.2, 15), (24, 30), 0.5)), "G", {"sidelock"})
    L.shade(hs(line((25.5, 15), (26, 22), 0.4)), "h", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16), (29.5, 12), (27, 16), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    L.shade(where(hs(rect(23, 10, 37, 28)), lambda x, y: L.g[y - 1 + OY][x] == "bangs"), "s", {"face"})
    L.paint(hs(poly([(22, 3.5), (24, -1.5), (26.5, 3.5)])), "H", "ahoge")
    L.paint(hs(poly([(9.5, 9), (14, 8), (14.5, 14), (10.5, 15)])), "H", "bunch")
    ribbon(L, 12.5 + HX, 10, False)
    return L.outline().rows()


def side_arm(swing, outfit):
    L = Layer()
    paint_arm(L, outfit, (23, 31), (23 + swing * 0.5, 37), (23 + swing, 43))
    return L.outline().rows()


def side_legs(step, outfit):
    L = Layer()
    dress = outfit == "dress"

    def leg(hip, knee, foot, far):
        hip, knee, foot = ((x + 1, y) for x, y in (hip, knee, foot))
        pts = taper(hip, knee, 2.3, 2.0) + taper(knee, foot, 2.0, 1.7)
        fx, fy = foot
        shoe = poly([(fx - 1.5, fy - 1.5), (fx + 1, fy - 1.5), (fx + 4, fy + 1.5), (fx + 4, fy + 3), (fx - 2, fy + 3)])
        if dress:
            L.paint(pts, "u" if far else "t", "farleg" if far else "tights")
            L.paint(rect(int(fx - 2), int(fy - 5), int(fx + 1), int(fy)) + shoe, "g", "farboot" if far else "boot")
            return
        L.paint(pts, "s" if far else "S", "farleg" if far else "leg")
        if outfit == "cardigan":
            L.paint(where(pts, lambda x, y: y >= fy - 4), "Y", "sock")
            L.paint(shoe, "b", "sneaker")
            L.shade(where(shoe, lambda x, y: y >= fy + 2.5), "W", {"sneaker"})
        elif outfit == "cami":
            L.paint(shoe, "I", "slipper")
        else:
            L.paint(shoe, "s" if far else "S", "farfoot" if far else "foot")
    hy = 50 if dress else 51 if outfit == "cami" else 52
    if step % 2 == 1:
        leg((23, hy), (23, 56), (23, 63), True); leg((23, hy), (23, 56), (23, 63), False)
    else:
        a, b = ((28, 64), (18, 64)) if step == 0 else ((18, 64), (28, 64))
        leg((23, hy), ((23 + b[0]) / 2, 57), b, True)
        leg((23, hy), ((23 + a[0]) / 2, 57), a, False)
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
    for name in ("right", "left"):
        side = {
            "body": side_body(outfit),
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
    {"name": "hop", "trigger": "idle", "weight": 5, "duration": (45, 45),
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
    {"name": "cheer", "trigger": "idle", "weight": 3, "duration": (40, 40),
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
    {"name": "cheers", "trigger": "idle", "weight": 2, "duration": (60, 60),
     "frames": [{"face": "tipsy", "arms": "cheers"}],
     "lift": {"type": "hop", "height": 4, "period": 20},
     "effect": {"glyph": "heart", "period": 30, "dx": [14]}},
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
    {"name": "eat", "trigger": "eat", "duration": (70, 70),
     "frames": [{"face": "tipsy", "arms": "cheers"}],
     "lift": {"type": "hop", "height": 4, "period": 20},
     "effect": {"glyph": "heart", "period": 35, "dx": [14]}},
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
