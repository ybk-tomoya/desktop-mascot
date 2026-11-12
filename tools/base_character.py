import copy

import sprite_engine as engine
from sprite_engine import WALK_STEPS, Layer, ellipse, line, mirror, poly, rect, taper, where

# ---------- head and face ----------
CX = 24
HEAD = (CX, 15, 13.5, 13)
FACE_POLY = [(14, 10), (34, 10), (35, 17), (34, 22), (31, 26.5), (26.5, 29), (21.5, 29), (17, 26.5), (14, 22), (13, 17)]
SX, HX = 23, -2
SIDE_FACE_POLY = [(22, 9), (30, 9), (33.5, 11.5), (35, 14), (35.5, 17), (35.5, 19.5), (36.5, 21), (35.6, 22), (37, 23), (37, 24.5), (35, 25.5),
                  (32.5, 27), (29.5, 29), (26, 29), (23, 27)]


def hs(pts):
    return [(x + HX, y) for x, y in pts]


def paint_face(L):
    L.paint(poly(FACE_POLY), "S", "face")


def shade_under_bangs(L):
    L.shade(where(poly(FACE_POLY), lambda x, y: L.g[y - 1 + engine.OY][x] == "bangs"), "s", {"face"})


def paint_side_face(L):
    L.paint(hs(poly(SIDE_FACE_POLY)), "S", "face")


def shade_side_under_bangs(L):
    L.shade(where(hs(rect(23, 10, 37, 28)), lambda x, y: L.g[y - 1 + engine.OY][x] == "bangs"), "s", {"face"})


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
SEYE = ["...KK", "..KFF", "WWFWF", "WWFWF", "WWEFF", ".WEEF", "...EW", "....e"]
SCLOSED = ["....", "....", "....", "....", "....", "K..K", ".KK.", "...."]


def face_layer(left, right, mouth="normal", blush_color="p", eye_y=16, lx=15, rx=26, blush=((14, 24), (30, 24))):
    W, H, OY = engine.W, engine.H, engine.OY
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


FACES = {
    "normal": (EYE, EYE),
    "talk": (EYE, EYE, "open"),
    "talkLeft": (LOOK_LEFT, LOOK_LEFT, "open"),
    "talkRight": (LOOK_RIGHT, LOOK_RIGHT, "open"),
    "blink": (CLOSED, CLOSED),
    "happy": (HAPPY, HAPPY, "open"),
    "smile": (HAPPY, HAPPY),
    "panic": (GT, mirror(GT), "o"),
    "wink": (EYE, HAPPY, "open"),
    "surprised": (SURPRISED, SURPRISED, "o"),
    "shy": (HAPPY, HAPPY, "normal", "P"),
    "dizzy": (DIZZY, mirror(DIZZY), "o"),
    "yawn": (CLOSED, CLOSED, "o"),
    "lookLeft": (LOOK_LEFT, LOOK_LEFT),
    "lookRight": (LOOK_RIGHT, LOOK_RIGHT),
    "lookDown": (LOOK_DOWN, LOOK_DOWN),
    "lookUp": (LOOK_UP, LOOK_UP),
}
OPTIONAL_FACES = {
    "tipsy": (HAPPY, HAPPY, "open", "P"),
    "hic": (SURPRISED, SURPRISED, "o", "P"),
}


def standard_faces(*optional, **custom):
    specs = {**FACES, **{n: OPTIONAL_FACES[n] for n in optional}}
    return {**{n: face_layer(*s) for n, s in specs.items()}, **custom}


def side_face(pat):
    W, H, OY = engine.W, engine.H, engine.OY
    g = [["."] * W for _ in range(H)]
    for dy, r in enumerate(pat):
        for dx, ch in enumerate(r):
            if ch != ".":
                g[16 + dy + OY][27 + dx] = ch
    for x, y in ((25, 24), (26, 24), (27, 24), (28, 24), (26, 25), (27, 25)):
        if g[y + OY][x] == ".":
            g[y + OY][x] = "p"
    return ["".join(r) for r in g]


# ---------- arms ----------
LS, RS = (18, 31), (30, 31)
_DOWN_L = (LS, (16, 37), (15.5, 43))
_DOWN_R = (RS, (32, 37), (32.5, 43))
_UP_L = (LS, (12, 25), (11, 18))
_UP_R = (RS, (36, 25), (37, 18))
ARM_POSES = {
    "down": (_DOWN_L, _DOWN_R),
    "drumLeft": ((LS, (12, 31), (12, 24)), (RS, (34, 37), (30, 40))),
    "drumRight": ((LS, (14, 37), (18, 40)), (RS, (36, 31), (36, 24))),
    "flailLeft": (_UP_L, (RS, (35, 37), (38, 42))),
    "flailRight": ((LS, (13, 37), (10, 42)), _UP_R),
    "bothUp": (_UP_L, _UP_R),
    "peace": ((LS, (12, 34), (13.5, 25)), _DOWN_R),
    "heart": ((LS, (12.5, 38), (22, 33.5)), (RS, (35.5, 38), (26, 33.5))),
    "behindHead": ((LS, (9.5, 23), (12.5, 12)), (RS, (38.5, 23), (35.5, 12))),
    "typeLeft": ((LS, (14.5, 38), (20.5, 38.5)), (RS, (33.5, 38), (27.5, 41))),
    "typeRight": ((LS, (14.5, 38), (20.5, 41)), (RS, (33.5, 38), (27.5, 38.5))),
    "grab": ((LS, (9, 22), (8.5, 4)), (RS, (39, 22), (39.5, 4))),
    "peek": ((LS, (11.5, 35), (9.5, 33)), (RS, (36.5, 35), (38.5, 33))),
    "cheers": (_DOWN_L, (RS, (38.5, 28), (38.5, 20))),
    "guitarUp": ((LS, (13, 38), (10, 34)), (RS, (34, 38), (28, 39))),
    "guitarDown": ((LS, (13, 38), (10, 34)), (RS, (34, 39), (29, 43))),
    "cheeks": ((LS, (11, 33.5), (15, 24.5)), (RS, (37, 33.5), (33, 24.5))),
}
STANDARD_ARMS = ("down", "flailLeft", "flailRight", "bothUp", "peace", "heart", "behindHead", "typeLeft", "typeRight", "grab", "peek")
CUP = [(35.5, 12.5), (41.5, 12.5), (40.5, 18.5), (36.5, 18.5)]


def cup(points=CUP):
    return lambda L: L.paint(poly(points), "W", "cup")


def front_arms(kind, paint_arm, props=None):
    L = Layer()
    for sh, e, hnd in ARM_POSES[kind]:
        paint_arm(L, sh, e, hnd)
    if props and kind in props:
        props[kind](L)
    if kind == "grab":
        for ex, hx in ((9, 8.5), (39, 39.5)):
            L.paint(line((ex, 22), (hx, 5), 1.9), "S", "arm")
            L.paint(ellipse(hx, 4, 3, 2.8), "S", "hand")
    if kind == "peace":
        L.paint(line((13, 24), (12, 20), 0.7) + line((14.5, 24), (15.5, 20), 0.7), "S", "hand")
    return L.outline().rows()


def side_arm(swing, paint_arm):
    L = Layer()
    paint_arm(L, (23, 31), (23 + swing * 0.5, 37), (23 + swing, 43))
    return L.outline().rows()


def _sleeve(shoulder, elbow, hand, reach, r):
    def lerp(p, q, t):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    if reach <= 1:
        end = lerp(shoulder, elbow, reach)
        pts = line(shoulder, end, r)
    else:
        end = lerp(elbow, hand, reach - 1)
        pts = line(shoulder, elbow, r) + line(elbow, end, r)
    return pts, line(end, end, r - 0.2)


def sleeved_arm(sleeves):
    """sleeves: [(色, 袖口の色, reach, 太さ, グループ)]。reach は 0〜1 が肩からひじ、1〜2 がひじから手（2 で手首まで）"""
    def paint(L, shoulder, elbow, hand):
        L.paint(line(shoulder, elbow, 1.6) + line(elbow, hand, 1.5), "S", "arm")
        L.paint(ellipse(hand[0], hand[1], 1.7, 1.7), "S", "hand")
        for color, cuff_color, reach, r, group in sleeves:
            sleeve, cuff = _sleeve(shoulder, elbow, hand, reach, r)
            L.paint(sleeve, color, group)
            L.shade(cuff, cuff_color, {group})
    return paint


# ---------- legs ----------
LEG_POSES = {
    "stand": ((20.5, (20.5, 57), (20.5, 64)), (27.5, (27.5, 57), (27.5, 64))),
    "together": ((20.7, (20.7, 57), (20.7, 64)), (27.3, (27.3, 57), (27.3, 64))),
    "kickLeft": ((20.5, (15.5, 55.5), (13.5, 60)), (27.5, (27.5, 57), (27.5, 64))),
    "kickRight": ((20.5, (20.5, 57), (20.5, 64)), (27.5, (32.5, 55.5), (34.5, 60))),
    "dangleLeft": ((20.5, (19.5, 54), (19, 59)), (27.5, (27.5, 55), (27.5, 62))),
    "dangleRight": ((20.5, (20.5, 55), (20.5, 62)), (27.5, (28.5, 54), (29, 59))),
}
STANDARD_LEGS = ("stand", "together", "sit", "kickLeft", "kickRight", "dangleLeft", "dangleRight")


def legwear(hip=52, side_hip=None, tights=None, sock=None, feet=False, shoe=None):
    """tights: (色, 奥の脚の色)。sock: 色。feet: 素足を描く。shoe: ("sneaker", 色, 底の色) / ("boot", 色) / ("slipper", 色, ふちの色 or None)"""
    return {"hip": hip, "side_hip": side_hip or hip, "tights": tights, "sock": sock, "feet": feet, "shoe": shoe}


def _foot(L, pos, rx=3):
    fx, fy = pos
    L.paint(ellipse(fx, fy + 2, rx, 1.7), "S", "foot")
    L.shade([(int(fx - 1), int(fy + 3)), (int(fx + 1), int(fy + 3))], "s", {"foot"})


def _front_shoe(L, ft, shoe):
    fx, fy = ft
    kind = shoe[0]
    if kind == "sneaker":
        L.paint(ellipse(fx, fy + 2, 3.4, 2.2), shoe[1], "sneaker")
        L.shade(where(ellipse(fx, fy + 2, 3.4, 2.2), lambda x, y: y >= fy + 3), shoe[2], {"sneaker"})
    elif kind == "boot":
        L.paint(rect(int(fx - 2), int(fy - 4), int(fx + 2), int(fy + 1)) + ellipse(fx, fy + 2, 3.2, 1.9), shoe[1], "boot")
    elif kind == "slipper":
        L.paint(ellipse(fx, fy + 2.3, 3.4, 2.0), shoe[1], "slipper")
        if shoe[2]:
            L.shade(rect(int(fx - 2), int(fy + 1), int(fx + 2), int(fy + 1)), shoe[2], {"slipper"})


def front_legs(kind, wear):
    L = Layer()
    close = kind == "together"
    hy = wear["hip"]
    tone, group = (wear["tights"][0], "tights") if wear["tights"] else ("S", "leg")

    def leg(hip, knee, ft):
        straight = abs((knee[0] - hip[0]) * (ft[1] - hip[1]) - (knee[1] - hip[1]) * (ft[0] - hip[0])) < 8
        if straight:
            pts = taper(hip, ft, 2.6 if close else 2.7, 2.0)
        else:
            pts = taper(hip, knee, 2.7, 2.3) + taper(knee, ft, 2.3, 2.0) + ellipse(ft[0], ft[1], 2.3, 2.3)
        L.paint(pts, tone, group)
        if wear["sock"]:
            L.paint(where(pts, lambda x, y: y >= ft[1] - 4), wear["sock"], "sock")
        if straight and wear["feet"]:
            _foot(L, ft, rx=2.6 if close else 3)
        if wear["shoe"]:
            _front_shoe(L, ft, wear["shoe"])
    if kind == "sit":
        for ft in ((20.5, 64), (27.5, 64)):
            if wear["feet"]:
                _foot(L, ft)
            if wear["shoe"]:
                _front_shoe(L, ft, wear["shoe"])
    else:
        for hx, knee, ft in LEG_POSES[kind]:
            leg((hx, hy), knee, ft)
    return L.outline().rows()


def side_legs(step, wear):
    L = Layer()
    shoe_kind = wear["shoe"] and wear["shoe"][0]

    def leg(hip, knee, foot, far):
        hip, knee, foot = ((x + 1, y) for x, y in (hip, knee, foot))
        pts = taper(hip, knee, 2.3, 2.0) + taper(knee, foot, 2.0, 1.7)
        fx, fy = foot
        shoe = poly([(fx - 1.5, fy - 1.5), (fx + 1, fy - 1.5), (fx + 4, fy + 1.5), (fx + 4, fy + 3), (fx - 2, fy + 3)])
        if wear["tights"]:
            L.paint(pts, wear["tights"][1] if far else wear["tights"][0], "farleg" if far else "tights")
        else:
            L.paint(pts, "s" if far else "S", "farleg" if far else "leg")
            if wear["sock"]:
                L.paint(where(pts, lambda x, y: y >= fy - 4), wear["sock"], "sock")
        if shoe_kind == "boot":
            L.paint(rect(int(fx - 2), int(fy - 5), int(fx + 1), int(fy)) + shoe, wear["shoe"][1], "farboot" if far else "boot")
        elif shoe_kind == "sneaker":
            L.paint(shoe, wear["shoe"][1], "sneaker")
            L.shade(where(shoe, lambda x, y: y >= fy + 2.5), wear["shoe"][2], {"sneaker"})
        elif shoe_kind == "slipper":
            L.paint(shoe, wear["shoe"][1], "slipper")
        else:
            L.paint(shoe, "s" if far else "S", "farfoot" if far else "foot")
    hy = wear["side_hip"]
    if step % 2 == 1:
        leg((23, hy), (23, 56), (23, 63), True); leg((23, hy), (23, 56), (23, 63), False)
    else:
        a, b = ((28, 64), (18, 64)) if step == 0 else ((18, 64), (28, 64))
        leg((23, hy), ((23 + b[0]) / 2, 57), b, True)
        leg((23, hy), ((23 + a[0]) / 2, 57), a, False)
    return L.outline().rows()


# ---------- assembling ----------
def assemble(outfit, *, front_body, side_body, front_arms, front_legs, side_arm, side_legs, faces, arms, legs, drops=None):
    """side_body(outfit, left) は右向きの絵を返す（left は左向きに使うとき True。手前と奥で描き分けたいとき用）"""
    sides = {}
    for name in ("right", "left"):
        side = {
            "body": side_body(outfit, name == "left"),
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
        "faces": faces,
        "arms": {k: front_arms(k, outfit) for k in arms},
        "legs": {k: front_legs(k, outfit) for k in legs},
        "drops": drops or {"sit": 14},
        "right": sides["right"],
        "left": sides["left"],
    }


def build_standard(outfit, *, front_body, side_body, sleeves, legwear, faces=None, arms=STANDARD_ARMS, legs=STANDARD_LEGS, props=None):
    """sleeves・legwear は衣装 ID → 設定の辞書。props は腕のポーズ名 → 持ち物を描く関数"""
    paint = sleeved_arm(sleeves[outfit])
    return assemble(
        outfit, front_body=front_body, side_body=side_body,
        front_arms=lambda k, o: front_arms(k, paint, props),
        front_legs=lambda k, o: front_legs(k, legwear[o]),
        side_arm=lambda sw, o: side_arm(sw, paint),
        side_legs=lambda step, o: side_legs(step, legwear[o]),
        faces=faces or standard_faces(), arms=arms, legs=legs)


# ---------- actions ----------
_SIT_LIFT = {"type": "sink", "height": 36}
STANDARD_ACTIONS = [
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
     "lift": _SIT_LIFT},
    {"name": "sitTop", "trigger": "top", "sit": True, "duration": (60, 200),
     "frames": [{"legs": "dangleLeft", "ticks": 8}, {"legs": "dangleRight", "ticks": 8}],
     "lift": _SIT_LIFT,
     "next": {"sitTopSmile": 0.3, "sitTopLook": 0.22, "sitTopBlink": 0.27, "sitTop": 0.75}},
    {"name": "sitTopSmile", "trigger": "chained", "sit": True, "duration": (70, 90),
     "frames": [{"face": "happy", "legs": "dangleLeft", "ticks": 8}, {"face": "happy", "legs": "dangleRight", "ticks": 8}],
     "lift": _SIT_LIFT,
     "next": {"sitTop": 1}},
    {"name": "sitTopLook", "trigger": "chained", "sit": True, "duration": (20, 20),
     "frames": [{"face": "lookLeft", "legs": "dangleLeft", "ticks": 10}, {"face": "lookRight", "legs": "dangleRight", "ticks": 10}],
     "lift": _SIT_LIFT,
     "next": {"sitTop": 1}},
    {"name": "sitTopBlink", "trigger": "chained", "sit": True, "duration": (8, 8),
     "frames": [{"face": "blink", "legs": "dangleLeft"}],
     "lift": _SIT_LIFT,
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
    {"name": "talk", "trigger": "talk", "weight": 4, "mood": "normal", "duration": (50, 90),
     "frames": [{"face": "talk", "ticks": 7}, {"ticks": 7}],
     "effect": {"glyph": "talk", "period": 45, "dx": [14]}},
    {"name": "talkFun", "trigger": "talk", "weight": 3, "mood": "fun", "duration": (50, 90),
     "frames": [{"face": "happy", "ticks": 7}, {"face": "smile", "ticks": 7}],
     "effect": {"glyph": "talkFun", "period": 45, "dx": [14]}},
    {"name": "talkAsk", "trigger": "talk", "weight": 2, "mood": "question", "duration": (50, 90),
     "frames": [{"face": "talk", "ticks": 7}, {"face": "lookUp", "ticks": 7}],
     "effect": {"glyph": "talkAsk", "period": 45, "dx": [14]}},
    {"name": "talkWow", "trigger": "talk", "weight": 1, "mood": "surprise", "duration": (50, 90),
     "frames": [{"face": "surprised"}],
     "lift": {"type": "hop", "height": 3, "period": 20},
     "effect": {"glyph": "talkWow", "period": 45, "dx": [14]}},
    {"name": "listen", "trigger": "listen", "weight": 3, "duration": (2000, 2000),
     "frames": [{"ticks": 1}]},
    {"name": "listenLaugh", "trigger": "listen", "weight": 3, "moods": ["fun"], "duration": (2000, 2000),
     "frames": [{"ticks": 20}, {"face": "happy", "ticks": 2000}],
     "lift": {"type": "hop", "height": 2, "period": 18}},
    {"name": "listenHeart", "trigger": "listen", "weight": 2, "moods": ["fun"], "duration": (2000, 2000),
     "frames": [{"ticks": 20}, {"face": "smile", "ticks": 2000}],
     "effect": {"glyph": "heart", "from": 20, "until": 60, "dx": [0]}},
    {"name": "listenWow", "trigger": "listen", "weight": 4, "moods": ["surprise"], "duration": (2000, 2000),
     "frames": [{"ticks": 20}, {"face": "surprised", "ticks": 2000}],
     "effect": {"glyph": "exclaim", "from": 20, "until": 60, "dx": [0]}},
    {"name": "listenThink", "trigger": "listen", "weight": 4, "moods": ["question"], "duration": (2000, 2000),
     "frames": [{"ticks": 20}, {"face": "lookUp", "ticks": 2000}],
     "effect": {"glyph": "question", "from": 20, "until": 60, "dx": [0]}},
    {"name": "ledgePeek", "trigger": "ledge", "weight": 1, "duration": (40, 40),
     "frames": [{"face": "lookDown"}],
     "effect": {"glyph": "question", "dx": [14]}},
    {"name": "lean", "trigger": "wall", "weight": 1, "duration": (80, 160),
     "frames": [{"face": "happy", "arms": "behindHead", "legs": "together"}]},
    {"name": "type", "trigger": "idle", "weight": 8, "apps": engine.TERMINAL_APPS, "duration": (60, 140),
     "frames": [{"face": "lookDown", "arms": "typeLeft", "legs": "sit", "ticks": 2},
                {"face": "lookDown", "arms": "typeRight", "legs": "sit", "ticks": 2}]},
    {"name": "browse", "trigger": "idle", "weight": 6, "apps": engine.BROWSER_APPS, "duration": (80, 80),
     "frames": [{"face": "lookLeft", "legs": "sit", "ticks": 20}, {"face": "lookRight", "legs": "sit", "ticks": 20}],
     "next": {"surprised": 1 / 4}},
    {"name": "groove", "trigger": "idle", "weight": 8, "apps": engine.MUSIC_APPS, "duration": (80, 160),
     "frames": [{"face": "happy", "arms": "bothUp", "legs": "together", "ticks": 5}, {"face": "happy", "legs": "together", "ticks": 5}],
     "lift": {"type": "hop", "height": 6, "period": 10},
     "effect": {"glyph": "note", "period": 20, "dx": [-16, 16]}},
    {"name": "fall", "trigger": "fall", "frames": [{"legs": "together"}]},
]


def standard_actions(drop=(), change=None, add=()):
    """drop: 使わない標準アクション名。change: {名前: {項目: 値}} で上書き。add: そのキャラだけのアクション"""
    names = {a["name"] for a in STANDARD_ACTIONS}
    for n in [*drop, *(change or {})]:
        if n not in names:
            raise SystemExit(f"standard_actions: unknown action '{n}'")
    actions = [copy.deepcopy(a) for a in STANDARD_ACTIONS if a["name"] not in drop]
    for a in actions:
        a.update(copy.deepcopy((change or {}).get(a["name"], {})))
    return actions + list(add)
