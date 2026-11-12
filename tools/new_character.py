import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import sprite_engine as engine
from gen_sprites import check, load, palette_of
from preview import write_previews
from sprite_lint import lint

HAIR = {
    "bob": '''BANGS = [(36.5, 9), (11.5, 9), (11.5, 15), (13.5, 13), (15.5, 16.5), (17.5, 13), (20, 17), (22, 13.5), (24.5, 17.5), (26.5, 13.5),
         (29, 17), (31, 13), (33, 16.5), (35, 13), (36.5, 15)]


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10, 15), (38, 15), (38.5, 22), (38, 28), (36.5, 31), (11.5, 31), (10, 28), (9.5, 22)]), "H", "hairback")
    L.shade(line((11.5, 22), (12, 30), 0.5) + line((36.5, 22), (36, 30), 0.5), "G", {"hairback"})
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly([(10.5, 15), (14, 11), (16, 27), (14.5, 31), (10.5, 29.5)]), "H", "lock")
    L.paint(poly([(37.5, 15), (34, 11), (32, 27), (33.5, 31), (37.5, 29.5)]), "H", "lock")
    L.shade(line((13, 20), (14, 29), 0.6), "G", {"lock"})
    L.shade(line((35, 20), (34, 29), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    shade_under_bangs(L)
    return L.outline().rows()


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (22.5, 29), (20, 31.5), (13, 31.5), (10.5, 28), (10, 22)])), "H", "hairback")
    L.shade(hs(line((13, 21), (14, 30), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    L.paint(hs(poly([(21, 12), (25.5, 12), (27, 19), (26.5, 26), (25.5, 30), (23, 31.5), (21.5, 25)])), "H", "sidelock")
    L.shade(hs(line((23.2, 15), (24, 29), 0.5)), "G", {"sidelock"})
    L.shade(hs(line((25.5, 15), (26, 22), 0.4)), "h", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16.5), (29.5, 12.5), (27, 16.5), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    return L.outline().rows()
''',
    "long": '''PART_X = 18.2
BANGS = [(37.5, 9), (17.5, 9), (17.5, 14.5), (20.5, 16.5), (22.5, 13), (25.5, 17), (27, 13.5), (30, 17.5), (31.5, 14), (35, 18.5), (37, 21), (37.5, 21)]
BANGS_SIDE = [(18, 9), (10.5, 9), (10.5, 21), (12, 17), (13, 14), (14.5, 16.5), (15.7, 13.5), (18, 15.5)]


def front_body(outfit):
    L = Layer()
    L.paint(ellipse(*HEAD) + poly([(10.5, 15), (37.5, 15), (39, 30), (38.5, 44), (36, 48), (12, 48), (9.5, 44), (9, 30)]), "H", "hairback")
    L.shade(line((11.5, 31), (12, 46), 0.5) + line((36.5, 31), (36, 46), 0.5), "G", {"hairback"})
    front_clothes(L, outfit)
    paint_face(L)
    L.paint(poly([(10.5, 16), (14, 12), (16.5, 34), (13, 37), (10.5, 30)]), "H", "lock")
    L.paint(poly([(37.5, 16), (34, 12), (31.5, 34), (35, 37), (37.5, 30)]), "H", "lock")
    L.shade(line((13, 22), (14, 34), 0.6), "G", {"lock"})
    L.shade(line((35, 22), (34, 34), 0.6), "G", {"lock"})
    bangs = where(ellipse(CX, 14, 13.5, 12), lambda x, y: y <= 10)
    bangs += poly(BANGS) + poly(BANGS_SIDE)
    L.paint(bangs, "H", "bangs")
    L.shade(ellipse(CX, 7.5, 10, 2.2), "h", {"bangs", "hairback"})
    L.shade(line((PART_X + 1.5, 2.5), (PART_X, 9.5), 0.5) + line((PART_X, 9.5), (PART_X - 0.3, 14), 0.5), "G", {"bangs", "hairback"})
    shade_under_bangs(L)
    return L.outline().rows()


def side_body(outfit, left=False):
    L = Layer()
    L.paint(hs(ellipse(SX, 15, 13, 13) + poly([(10, 15), (22, 15), (22, 32), (18.5, 46), (13.5, 48.5), (10, 40), (9.5, 24)])), "H", "hairback")
    L.shade(hs(line((13.5, 21), (15, 44), 0.6)), "G", {"hairback"})
    side_clothes(L, outfit)
    paint_side_face(L)
    L.paint(hs(poly([(21, 12), (25.5, 12), (27, 19), (26.5, 26), (24.5, 31), (22.5, 34), (22.5, 26), (21, 19)])), "H", "sidelock")
    L.shade(hs(line((23.2, 15), (24, 30), 0.5)), "G", {"sidelock"})
    L.shade(hs(line((25.5, 15), (26, 22), 0.4)), "h", {"sidelock"})
    bangs = where(ellipse(SX, 14, 13, 12), lambda x, y: y <= 10 or x <= 22)
    bangs += poly([(21, 9), (36.5, 9), (36.5, 13.5), (35, 16.5), (33.5, 12.5), (31.5, 16), (29.5, 12), (27, 16), (25, 12.5), (23, 16), (21, 13)])
    L.paint(hs(bangs), "H", "bangs")
    L.shade(hs(ellipse(SX - 1, 7.5, 9, 2.2)), "h", {"bangs", "hairback"})
    shade_side_under_bangs(L)
    return L.outline().rows()
''',
}

TEMPLATE = '''from sprite_engine import *
from base_character import *

ID = "{id}"
NAME = "{name}"
W, H, OY = 48, 72, 4
ORDER = {order}
OUTFITS = [("casual", "私服")]
ACCESSORIES = ["cap", "glasses", "ribbon"]

PALETTE = {{
    "K": (0.20, 0.13, 0.17),
    "H": (0.45, 0.32, 0.25),
    "G": (0.33, 0.22, 0.18),
    "h": (0.62, 0.48, 0.38),
    "S": (1.00, 0.90, 0.83),
    "s": (0.93, 0.72, 0.66),
    "p": (1.00, 0.78, 0.80),
    "P": (0.96, 0.58, 0.64),
    "W": (1.00, 1.00, 1.00),
    "E": (0.36, 0.52, 0.40),
    "F": (0.16, 0.26, 0.20),
    "e": (0.62, 0.80, 0.66),
    "R": (0.92, 0.38, 0.42),
    "m": (0.78, 0.38, 0.40),
    "A": (0.96, 0.82, 0.52),
    "a": (0.84, 0.66, 0.38),
    "N": (0.40, 0.48, 0.64),
    "n": (0.30, 0.37, 0.52),
    "B": (0.85, 0.30, 0.32),
}}


# ---------- front ----------
def front_clothes(L, outfit):
    L.paint(poly([(15.5, 44), (32.5, 44), (34, 51), (25.5, 51), (24, 48.5), (22.5, 51), (14, 51)]), "N", "shorts")
    L.shade(rect(13, 50, 35, 50), "n", {{"shorts"}})
    L.paint(poly([(17, 29), (31, 29), (33, 32), (34, 46), (14, 46), (15, 32)]), "A", "tee")
    L.shade(rect(13, 45, 35, 45), "a", {{"tee"}})
    L.paint(rect(22, 25, 26, 28) + rect(20, 28, 28, 30), "S", "throat")
    L.shade(rect(22, 29, 26, 29), "s", {{"throat"}})


# ---------- side (facing right) ----------
def side_clothes(L, outfit):
    L.paint(poly([(19, 44), (28.5, 44), (29.5, 51), (18, 51)]), "N", "shorts")
    L.shade(rect(17, 50, 30, 50), "n", {{"shorts"}})
    L.paint(poly([(20, 29), (27, 29), (28.5, 32), (29.5, 46), (18.5, 46), (19.5, 32)]), "A", "tee")
    L.paint(rect(21, 25, 25, 28) + rect(24, 28, 27, 30), "S", "throat")
    L.shade(rect(23, 28, 26, 28), "s", {{"throat"}})


# ---------- hair ----------
{hair}

SLEEVES = {{
    "casual": [("A", "a", 0.6, 2.4, "sleeve")],
}}

LEGWEAR = {{
    "casual": legwear(sock="W", shoe=("sneaker", "B", "W")),
}}


def build(outfit):
    return build_standard(outfit, front_body=front_body, side_body=side_body, sleeves=SLEEVES, legwear=LEGWEAR)


ACTIONS = standard_actions()
'''


def main():
    parser = argparse.ArgumentParser(description="新しいキャラのひな形を tools/characters/<id>.py に作る")
    parser.add_argument("id", help="英小文字の ID（ファイル名と Swift の名前に使う）")
    parser.add_argument("name", help="メニューに出す名前")
    parser.add_argument("--hair", choices=sorted(HAIR), default="bob", help="髪型のひな形")
    args = parser.parse_args()
    if not args.id.isidentifier() or not args.id.islower():
        raise SystemExit("id must be a lowercase identifier like 'kanade'")
    path = ROOT / "characters" / f"{args.id}.py"
    if path.exists():
        raise SystemExit(f"{path} already exists")
    order = max((load(p).ORDER for p in (ROOT / "characters").glob("*.py")), default=-1) + 1
    path.write_text(TEMPLATE.format(id=args.id, name=args.name, order=order, hair=HAIR[args.hair].rstrip() + "\n"))

    mod = load(path)
    engine.configure(mod.W, mod.H, mod.OY)
    outfits = [(oid, mod.build(oid)) for oid, _ in mod.OUTFITS]
    warnings = []
    for oid, data in outfits:
        check(mod, data, oid)
        warnings += lint(mod, oid, data)
    previews = ROOT.parent / "build/previews"
    write_previews([(mod, palette_of(mod), outfits)], previews, compare=False)
    for w in warnings:
        print("warning:", w)
    print(f"created {path}")
    print(f"preview: {previews / (args.id + '.png')}")


if __name__ == "__main__":
    main()
