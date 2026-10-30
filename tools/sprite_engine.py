import math

W, H, OY = 0, 0, 0
YR = range(0)

FACES = ("normal", "blink", "happy", "panic", "wink", "yawn", "lookLeft", "lookRight")
ARMS = ("down", "drumLeft", "drumRight", "flailLeft", "flailRight", "bothUp", "peace")
LEGS = ("stand", "together", "sit", "kickLeft", "kickRight")
WALK_STEPS = 4


def configure(w, h, oy):
    global W, H, OY, YR
    W, H, OY = w, h, oy
    YR = range(-oy, h - oy)


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
