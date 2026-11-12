import struct
import zlib
from pathlib import Path

SCALE = 4
GAP = 4
BACKGROUND = (236, 240, 244)
POSES = [("normal", "down", "stand"), ("happy", "bothUp", "together"), ("shy", "heart", "sit"), ("panic", "flailLeft", "kickRight")]


def overlay(layers):
    out = [list(r) for r in layers[0]]
    for layer in layers[1:]:
        for y, row in enumerate(layer):
            for x, c in enumerate(row):
                if c != ".":
                    out[y][x] = c
    return out


def lowered(rows, n):
    return [["."] * len(rows[0])] * n + rows[:len(rows) - n] if n > 0 else rows


def front(data, face, arms, legs):
    arms = arms if arms in data["arms"] else "down"
    legs = legs if legs in data["legs"] else "stand"
    upper = overlay([data["body"], data["arms"][arms], data["faces"].get(face, data["faces"]["normal"])])
    return overlay([data["legs"][legs], lowered(upper, data["drops"].get(legs, 0))])


def side(data, name, step):
    s = data[name]
    upper = overlay([s["body"], s["arms"][step], s["face"]])
    return overlay([s["legs"][step], upper if step % 2 == 0 else upper[1:] + [["."] * len(upper[0])]])


def tiles(data):
    return [front(data, *p) for p in POSES] + [side(data, "right", 0), side(data, "left", 1)]


def sheet(rows_of_tiles):
    tw = max(len(tile[0]) for row in rows_of_tiles for tile, _ in row)
    th = max(len(tile) for row in rows_of_tiles for tile, _ in row)
    cols = max(len(row) for row in rows_of_tiles)
    width, height = cols * (tw + GAP) * SCALE, len(rows_of_tiles) * (th + GAP) * SCALE
    img = [[BACKGROUND] * width for _ in range(height)]
    for r, row in enumerate(rows_of_tiles):
        for c, (tile, pal) in enumerate(row):
            ox, oy = c * (tw + GAP) * SCALE, r * (th + GAP) * SCALE
            for y, line in enumerate(tile):
                for x, ch in enumerate(line):
                    if ch == ".":
                        continue
                    color = tuple(int(v * 255) for v in pal[ch])
                    for yy in range(SCALE):
                        img[oy + y * SCALE + yy][ox + x * SCALE:ox + (x + 1) * SCALE] = [color] * SCALE
    return img


def write_png(path, img):
    raw = b"".join(b"\0" + bytes(v for px in row for v in px) for row in img)

    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    header = struct.pack(">IIBBBBB", len(img[0]), len(img), 8, 2, 0, 0, 0)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def write_previews(characters, out_dir, compare=True):
    """characters: [(mod, palette, [(outfit, data)])]。キャラごとの一覧と、全キャラの全衣装を並べた比較画像を書き出す"""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    everyone = []
    for mod, palette, outfits in characters:
        rows = [[(t, palette) for t in tiles(data)] for _, data in outfits]
        faces = outfits[0][1]["faces"]
        head = len(faces["normal"]) // 2
        face_rows = [[(overlay([outfits[0][1]["body"], f])[:head], palette) for f in faces.values()]]
        write_png(out / f"{mod.ID}.png", sheet(rows))
        write_png(out / f"{mod.ID}-faces.png", sheet(face_rows))
        everyone.append([(front(data, *POSES[0]), palette) for _, data in outfits])
    if compare:
        write_png(out / "all.png", sheet(everyone))
