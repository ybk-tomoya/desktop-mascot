import math, re
from pathlib import Path

W, H = 48, 72
OY = 4
YR = range(-OY, H - OY)
SRC = Path(__file__).resolve().parent.parent / "Sources/DesktopMascot/Sprites.swift"

CLASS = {
    "tail": "tail", "hairback": "hair", "bangs": "hair", "lock": "hair", "ahoge": "ahoge",
    "face": "skin", "neck": "skin", "leg": "skin", "hand": "skin", "arm": "skin",
    "shirt": "shirt", "sleeve": "shirt", "bow": "bow", "tie": "bow",
    "skirt": "skirt", "sock": "sock", "shoe": "shoe", "stick": "stick",
    "farleg": "skin", "farsock": "sock", "farshoe": "shoe", "fartail": "tail",
}


class Layer:
    def __init__(self):
        self.c = [[None] * W for _ in range(H)]
        self.g = [[None] * W for _ in range(H)]
        self.d = [[0] * W for _ in range(H)]
        self.depth = 0

    def paint(self, pts, color, group):
        self.depth += 1
        for x, y in pts:
            y += OY
            if 0 <= x < W and 0 <= y < H:
                self.c[y][x] = color
                self.g[y][x] = group
                self.d[y][x] = self.depth

    def shade(self, pts, color, groups):
        for x, y in pts:
            y += OY
            if 0 <= x < W and 0 <= y < H and self.g[y][x] in groups:
                self.c[y][x] = color

    def outline(self):
        out = [row[:] for row in self.c]
        for y in range(H):
            for x in range(W):
                if self.c[y][x] is None:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < W and 0 <= ny < H) or self.c[ny][nx] is None:
                        out[y][x] = "K"
                        break
                    if CLASS[self.g[ny][nx]] != CLASS[self.g[y][x]] and self.d[y][x] > self.d[ny][nx]:
                        out[y][x] = "K"
                        break
        self.c = out
        return self

    def rows(self):
        return ["".join(ch or "." for ch in row) for row in self.c]


def ellipse(cx, cy, rx, ry):
    return [(x, y) for y in YR for x in range(W)
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1]


def poly(points):
    res = []
    n = len(points)
    for y in YR:
        yc = y + 0.5
        xs = []
        for i in range(n):
            (x1, y1), (x2, y2) = points[i], points[(i + 1) % n]
            if (y1 <= yc < y2) or (y2 <= yc < y1):
                xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            for x in range(W):
                if a <= x + 0.5 <= b:
                    res.append((x, y))
    return res


def rect(x0, y0, x1, y1):
    return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]


def line(p, q, r):
    (x1, y1), (x2, y2) = p, q
    res = []
    L2 = (x2 - x1) ** 2 + (y2 - y1) ** 2 or 1
    for y in YR:
        for x in range(W):
            px, py = x + 0.5, y + 0.5
            t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / L2))
            if (px - x1 - t * (x2 - x1)) ** 2 + (py - y1 - t * (y2 - y1)) ** 2 <= r * r:
                res.append((x, y))
    return res


def where(pts, cond):
    return [(x, y) for x, y in pts if cond(x, y)]


def mirror(rows):
    return [r[::-1] for r in rows]


# ---------- front ----------
CX = 24
HEAD = (CX, 15, 13.5, 13)
FACE_POLY = [(14, 10), (34, 10), (35, 17), (34, 22), (31, 26.5), (26.5, 29), (21.5, 29), (17, 26.5), (14, 22), (13, 17)]


def front_body():
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10.5, 15), (37.5, 15), (37, 32), (11, 32)]), "H", "hairback")
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
    L.paint(poly([(fx - 2.5, fy - 0.5), (fx + 2.5, fy - 0.5), (fx + 3, fy + 1), (fx + 3, fy + 3), (fx - 3, fy + 3), (fx - 3, fy + 1)]), "R", group)


def front_legs(kind):
    L = Layer()
    def leg(hip, knee, foot):
        L.paint(line(hip, knee, 2.0) + line(knee, foot, 1.8), "S", "leg")
        L.paint(where(line(knee, foot, 1.9), lambda x, y: y >= foot[1] - 4), "L", "sock")
        shoe(L, foot)
    if kind == "stand":
        leg((20.5, 50), (20.5, 57), (20.5, 64)); leg((27.5, 50), (27.5, 57), (27.5, 64))
    elif kind == "together":
        leg((21, 50), (21.5, 57), (21.5, 64)); leg((27, 50), (26.5, 57), (26.5, 64))
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
GT = [".......", "KK.....", "..KK...", "....KKK", "..KK...", "KK.....", "......."]


def face_layer(left, right, mouth="normal", look=0, eye_y=16, lx=15, rx=26, blush=((14, 24), (31, 24))):
    g = [["."] * W for _ in range(H)]
    for pat, x0 in ((left, lx), (right, rx)):
        for dy, r in enumerate(pat):
            for dx, ch in enumerate(r):
                if ch != ".":
                    g[eye_y + dy + OY][x0 + dx + (look if pat is EYE else 0)] = ch
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
        "lookLeft": face_layer(EYE, EYE, look=-1),
        "lookRight": face_layer(EYE, EYE, look=1),
    }


# ---------- side (facing right) ----------
SX = 23


def side_body(near_tail):
    L = Layer()
    tail = poly([(13, 8), (18, 9), (16, 20), (15, 36), (14, 48), (11, 53), (10, 46), (11, 32), (10, 18)])
    if not near_tail:
        L.paint(tail, "G", "fartail")
    L.paint(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (21, 30), (16, 37), (11, 33), (9.5, 24)]), "H", "hairback")
    L.shade(line((13, 22), (14, 34), 0.6), "G", {"hairback"})
    L.paint(rect(22, 26, 26, 30), "S", "neck")
    L.shade(rect(22, 26, 26, 27), "s", {"neck"})
    L.paint(poly([(19, 29.5), (28, 29.5), (30, 32), (29, 41), (18, 41), (18, 32)]), "W", "shirt")
    L.shade(rect(18, 33, 19, 41), "w", {"shirt"})
    L.paint(poly([(18, 40), (29, 40), (32, 51), (15, 51)]), "D", "skirt")
    for x0 in (20, 23, 26):
        L.shade(line((x0 + 0.5, 42), (SX + (x0 + 0.5 - SX) * 1.5, 50), 0.5), "d", {"skirt"})
    L.paint(poly([(27, 29), (32, 30), (31, 34), (27, 33)]) + poly([(28, 32), (31, 38), (27.5, 36)]), "R", "bow")
    L.paint(poly([(22, 9), (30, 9), (34, 12), (35.5, 16), (35.5, 19.5), (36.6, 21.5), (35.8, 22.5), (36, 24.5), (34.5, 26.5), (31.5, 29), (27, 29), (23, 28)]), "S", "face")
    L.paint(poly([(18, 13), (22, 12), (23, 22), (21.5, 30), (19, 31)]), "H", "lock")
    L.shade(line((20.5, 18), (20.5, 29), 0.5), "G", {"lock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 11 or x <= 23)
    for i, x0 in enumerate(range(23, 35, 3)):
        bangs += poly([(x0 - 0.5, 10), (x0 + 3.5, 10), (x0 + 2.5, 16 if i % 2 == 0 else 14)])
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(SX - 1, 7.5, 9, 2.2), "h", {"bangs", "hairback"})
    L.shade(where(rect(23, 10, 37, 28), lambda x, y: y > 0 and L.g[y - 1 + OY][x] == "bangs"), "s", {"face"})
    L.paint(poly([(20.5, 3.5), (20.5, -3.5), (27, 3.5)]), "H", "ahoge")
    L.shade(line((21.5, -1), (21.5, 2.5), 0.5), "h", {"ahoge"})
    if near_tail:
        L.paint(rect(11, 6, 16, 11), "R", "tie")
        L.paint(tail, "H", "tail")
        L.shade(line((13, 13), (12.5, 46), 0.6), "h", {"tail"})
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


SEYE = [".KKK", "KWFF", "FWWW", "EWFW", "EFFW", "EEFW", "EeE.", ".ee."]
SCLOSED = ["....", "....", "....", "....", "K...", ".KKK", "...."]


def side_face(pat):
    g = [["."] * W for _ in range(H)]
    for dy, r in enumerate(pat):
        for dx, ch in enumerate(r):
            if ch != ".":
                g[16 + dy + OY][29 + dx] = ch
    for x, y in ((27, 24), (28, 24), (29, 24), (30, 24), (28, 25), (29, 25)):
        if g[y + OY][x] == ".":
            g[y + OY][x] = "p"
    g[26 + OY][34] = "m"
    return ["".join(r) for r in g]


def emit():
    def arr(rows, ind):
        return "\n".join(f'{ind}"{r}",' for r in rows)

    def cases(d, ind):
        return "".join(f"{ind}{'default' if k == 'default' else 'case .' + k}: [\n{arr(v, ind + '    ')}\n{ind}]\n" for k, v in d.items())

    faces = front_faces()
    arms = {k: front_arms(k) for k in ("down", "drumLeft", "drumRight", "flailLeft", "flailRight", "bothUp", "peace")}
    legs = {k: front_legs(k) for k in ("stand", "together", "sit", "kickLeft", "kickRight")}
    sides = {}
    for name, near in (("right", False), ("left", True)):
        body = side_body(near)
        face = {"blink": side_face(SCLOSED), "default": side_face(SEYE)}
        stepl = [side_legs(i) for i in range(4)]
        swings = [-5, 0, 5, 0]
        arml = [side_arm(sw) for sw in swings]
        if name == "left":
            body = mirror(body)
            face = {k: mirror(v) for k, v in face.items()}
            stepl = [mirror(v) for v in stepl]
            arml = [mirror(v) for v in arml]
        sides[name] = (body, face, stepl, arml)

    out = f'''enum Sprites {{
    static let width = {W}
    static let sitDrop = 14

    static func overlay(_ layers: [[String]]) -> [String] {{
        var out = layers[0].map {{ Array($0) }}
        for layer in layers.dropFirst() {{
            for (y, row) in layer.enumerated() {{
                for (x, c) in row.enumerated() where c != "." {{
                    out[y][x] = c
                }}
            }}
        }}
        return out.map {{ String($0) }}
    }}

    static func lowered(_ rows: [String], by n: Int) -> [String] {{
        Array(repeating: String(repeating: ".", count: width), count: n) + rows.dropLast(n)
    }}

    static let body = [
{arr(front_body(), "        ")}
    ]

    static func face(_ face: Face) -> [String] {{
        switch face {{
{cases(faces, "        ")}        }}
    }}

    static func arms(_ arms: Arms) -> [String] {{
        switch arms {{
{cases(arms, "        ")}        }}
    }}

    static func legs(_ legs: Legs) -> [String] {{
        switch legs {{
{cases(legs, "        ")}        }}
    }}

    static func frame(face f: Face, arms a: Arms = .down, legs l: Legs) -> [String] {{
        let upper = overlay([body, arms(a), face(f)])
        return overlay([legs(l), l == .sit ? lowered(upper, by: sitDrop) : upper])
    }}

'''
    for name, (body, face, stepl, arml) in sides.items():
        out += f'''    static let {name}Body = [
{arr(body, "        ")}
    ]

    static func {name}Face(_ face: Face) -> [String] {{
        switch face {{
{cases(face, "        ")}        }}
    }}

    static let {name}Legs = [
''' + "".join(f"        [\n{arr(v, '            ')}\n        ],\n" for v in stepl) + f'''    ]

    static let {name}Arms = [
''' + "".join(f"        [\n{arr(v, '            ')}\n        ],\n" for v in arml) + "    ]\n\n"

    out += '''    static func walkFrame(face f: Face, step: Int, facingLeft: Bool) -> [String] {
        let upper = facingLeft
            ? overlay([leftBody, leftArms[step], leftFace(f)])
            : overlay([rightBody, rightArms[step], rightFace(f)])
        let legs = facingLeft ? leftLegs[step] : rightLegs[step]
        return overlay([legs, step % 2 == 1 ? Array(upper.dropFirst()) + [String(repeating: ".", count: width)] : upper])
    }

'''
    s = open(SRC).read()
    a = s.index("enum Sprites {")
    b = s.index("    static let note = [")
    s = s[:a] + out + s[b:]
    for k, v in {"m": "0.78, green: 0.38, blue: 0.40", "T": "0.66, green: 0.44, blue: 0.24"}.items():
        if f'"{k}": NSColor' not in s:
            s = s.replace('        "B": NSColor', f'        "{k}": NSColor(srgbRed: {v}, alpha: 1),\n        "B": NSColor', 1)
    open(SRC, "w").write(s)


emit()
print("ok")
