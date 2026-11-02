import math

W, H, OY = 0, 0, 0
YR = range(0)

WALK_STEPS = 4
REQUIRED = {"faces": ("normal", "blink"), "arms": ("down",), "legs": ("stand",)}
TRIGGERS = ("idle", "click", "drag", "fall", "pet", "throw", "land", "eat", "ledge", "wall", "top", "chained")
LIFTS = ("jump", "hop", "rise", "sink", "cling")

TERMINAL_APPS = ["com.apple.Terminal", "com.googlecode.iterm2", "com.mitchellh.ghostty", "com.github.wez.wezterm", "org.alacritty",
                 "net.kovidgoyal.kitty", "dev.warp.Warp-Stable", "com.cmuxterm.app", "com.microsoft.VSCode"]
BROWSER_APPS = ["com.apple.Safari", "com.google.Chrome", "company.thebrowser.Browser", "company.thebrowser.dia", "org.mozilla.firefox",
                "com.microsoft.edgemac", "com.brave.Browser", "com.openai.atlas"]
MUSIC_APPS = ["com.apple.Music", "com.spotify.client"]

GLYPH_PALETTE = {
    "K": (0.20, 0.13, 0.17),
    "R": (0.92, 0.32, 0.42),
    "W": (1.00, 1.00, 1.00),
    "D": (0.24, 0.29, 0.52),
}

ACCESSORY_PALETTE = {
    "1": (0.85, 0.25, 0.30),
    "2": (0.62, 0.14, 0.22),
    "3": (0.97, 0.95, 0.95),
    "4": (0.20, 0.13, 0.17),
    "5": (0.85, 0.93, 1.00),
    "6": (0.95, 0.50, 0.65),
    "7": (0.78, 0.30, 0.50),
}

GLYPHS = {
    "heart": [".KK.KK.", "KRRKRRK", "KRWRRRK", ".KRRRK.", "..KRK..", "...K..."],
    "note": ["..KK.", "..KKK", "..K.K", "KKK..", "KKK.."],
    "zzz": ["DDDDD", "...D.", "..D..", ".D...", "DDDDD"],
    "question": [".KKK.", "KK.KK", "...KK", "..KK.", "..K..", ".....", "..K.."],
    "exclaim": ["KK", "KK", "KK", "KK", "..", "KK"],
    "dizzy": ["..D..", ".DWD.", "DWWWD", ".DWD.", "..D.."],
    "sneeze": ["K..K..K", ".K.K.K.", "..KKK..", "KKK.KKK", "..KKK..", ".K.K.K.", "K..K..K"],
}


def configure(w, h, oy):
    global W, H, OY, YR
    W, H, OY = w, h, oy
    YR = range(-oy, h - oy)


CLASS = {
    "tail": "tail", "hairback": "hair", "bangs": "hair", "lock": "hair", "sidelock": "sidelock", "ahoge": "ahoge",
    "face": "skin", "neck": "skin", "leg": "skin", "hand": "skin", "arm": "skin",
    "shirt": "shirt", "sleeve": "shirt", "bow": "bow", "tie": "bow",
    "skirt": "skirt", "sock": "sock", "shoe": "shoe", "stick": "stick",
    "farleg": "skin", "farsock": "sock", "farshoe": "shoe", "fartail": "tail",
    "ribbon": "ribbon", "bunch": "bunch", "pajama": "pajama", "shorts": "shorts", "frill": "frill",
    "foot": "skin", "farfoot": "skin", "throat": "throat", "cup": "cup",
    "capdome": "cap", "capband": "capband", "brim": "brim", "frame": "frame", "glint": "glint",
    "loop": "loop", "knot": "knot", "tee": "shirt", "emblem": "shirt", "hoodie": "pajama", "hood": "hood", "pocket": "pocket",
    "denim": "shorts",
    "strap": "strap", "collar": "collar", "cardigan": "cardigan", "turtle": "turtle", "dress": "dress", "sash": "sash",
    "tights": "tights", "boot": "boot", "farboot": "boot", "sneaker": "shoe", "slipper": "slipper",
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


def taper(p, q, r1, r2):
    (x1, y1), (x2, y2) = p, q
    res = []
    L2 = (x2 - x1) ** 2 + (y2 - y1) ** 2 or 1
    for y in YR:
        for x in range(W):
            px, py = x + 0.5, y + 0.5
            t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / L2))
            r = r1 + (r2 - r1) * t
            if (px - x1 - t * (x2 - x1)) ** 2 + (py - y1 - t * (y2 - y1)) ** 2 <= r * r:
                res.append((x, y))
    return res


def where(pts, cond):
    return [(x, y) for x, y in pts if cond(x, y)]


def mirror(rows):
    return [r[::-1] for r in rows]


def front_accessories():
    cap = Layer()
    cap.paint(where(ellipse(24, 12, 14, 10), lambda x, y: y <= 10), "1", "capdome")
    cap.paint(rect(12, 9, 35, 10), "3", "capband")
    cap.paint(poly([(13, 10), (35, 10), (36, 12.5), (12, 12.5)]), "2", "brim")
    glasses = Layer()
    for cx in (18, 29):
        ring = [p for p in ellipse(cx, 20, 5, 4.6) if p not in ellipse(cx, 20, 3.6, 3.2)]
        glasses.paint(ring, "4", "frame")
    glasses.paint(rect(23, 19, 24, 19), "4", "frame")
    glasses.paint([(16, 17), (17, 17), (27, 17), (28, 17)], "5", "glint")
    ribbon = Layer()
    ribbon.paint(poly([(15, 6), (9, 2), (9, 10)]) + poly([(15, 6), (21, 2), (21, 10)]), "6", "loop")
    ribbon.paint(rect(14, 5, 16, 7), "7", "knot")
    return {"cap": cap, "glasses": glasses, "ribbon": ribbon}


def side_accessories(sx):
    cap = Layer()
    cap.paint(where(ellipse(sx, 12, 13.5, 10), lambda x, y: y <= 10), "1", "capdome")
    cap.paint(rect(sx - 12, 9, sx + 13, 10), "3", "capband")
    cap.paint(poly([(sx + 5, 10), (sx + 18, 10), (sx + 19, 13), (sx + 4, 13)]), "2", "brim")
    glasses = Layer()
    ring = [p for p in ellipse(sx + 7, 20, 5, 4.6) if p not in ellipse(sx + 7, 20, 3.6, 3.2)]
    glasses.paint(ring, "4", "frame")
    glasses.paint(rect(sx - 4, 19, sx + 2, 19), "4", "frame")
    glasses.paint([(sx + 5, 17), (sx + 6, 17)], "5", "glint")
    ribbon = Layer()
    ribbon.paint(poly([(sx - 6, 6), (sx - 12, 2), (sx - 12, 10)]) + poly([(sx - 6, 6), (sx, 2), (sx, 10)]), "6", "loop")
    ribbon.paint(rect(sx - 7, 5, sx - 5, 7), "7", "knot")
    return {"cap": cap, "glasses": glasses, "ribbon": ribbon}


ACCESSORY_NAMES = {"cap": "キャップ", "glasses": "メガネ", "ribbon": "リボン"}


def accessory(id, side_x):
    front = front_accessories()[id].outline().rows()
    right = side_accessories(side_x)[id].outline().rows()
    return {"front": front, "right": right, "left": mirror(right)}
