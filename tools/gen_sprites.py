import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import sprite_engine as engine
from preview import write_previews
from sprite_lint import lint

OUT = ROOT.parent / "Sources/DesktopMascot/Characters"
PREVIEWS = ROOT.parent / "build/previews"


def load(path):
    spec = importlib.util.spec_from_file_location(f"characters.{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def glyphs_of(mod):
    return {**engine.GLYPHS, **getattr(mod, "GLYPHS", {})}


def palette_of(mod):
    return {**mod.PALETTE, **(engine.ACCESSORY_PALETTE if getattr(mod, "ACCESSORIES", None) else {})}


def check(mod, data, outfit):
    def fail(msg):
        raise SystemExit(f"{mod.ID}/{outfit}: {msg}")

    layers = [data["body"], *data["faces"].values(), *data["arms"].values(), *data["legs"].values()]
    for side in ("right", "left"):
        s = data[side]
        layers += [s["body"], s["face"], s["blink"], *s["legs"], *s["arms"]]
        if not len(s["legs"]) == len(s["arms"]) == engine.WALK_STEPS:
            fail(f"{side} walk needs {engine.WALK_STEPS} legs and arms frames")
    for r in layers:
        if len(r) != mod.H or any(len(x) != mod.W for x in r):
            fail(f"every layer must be {mod.W}x{mod.H}")
    for kind, names in engine.REQUIRED.items():
        for n in names:
            if n not in data[kind]:
                fail(f"{kind} must include '{n}'")
    missing = {c for r in layers for line in r for c in line} - {"."} - set(palette_of(mod))
    if missing:
        fail(f"colors missing from PALETTE: {sorted(missing)}")

    glyphs = glyphs_of(mod)
    names = {a["name"] for a in mod.ACTIONS}
    for a in mod.ACTIONS:
        where = f"action '{a['name']}'"
        if a["trigger"] not in engine.TRIGGERS:
            fail(f"{where}: trigger must be one of {engine.TRIGGERS}")
        if not a.get("walk") and not a.get("frames"):
            fail(f"{where}: needs frames (or walk: True)")
        for f in a.get("frames", []):
            for kind, key in (("faces", "face"), ("arms", "arms"), ("legs", "legs")):
                if key in f and f[key] not in data[kind]:
                    fail(f"{where}: unknown {key} '{f[key]}'")
        if "strength" in a and not (len(a["strength"]) == 2 and a["strength"][0] <= a["strength"][1]):
            fail(f"{where}: strength must be (min, max)")
        if "apps" in a and not (isinstance(a["apps"], list) and all(isinstance(x, str) for x in a["apps"])):
            fail(f"{where}: apps must be a list of bundle identifiers")
        if "lift" in a and a["lift"]["type"] not in engine.LIFTS:
            fail(f"{where}: lift type must be one of {engine.LIFTS}")
        if "effect" in a and a["effect"]["glyph"] not in glyphs:
            fail(f"{where}: unknown glyph '{a['effect']['glyph']}'")
        for n in a.get("next", {}):
            if n not in names:
                fail(f"{where}: next action '{n}' does not exist")
    for id in getattr(mod, "ACCESSORIES", []):
        if id not in engine.ACCESSORY_NAMES:
            fail(f"unknown accessory '{id}'")
    if not any(a["trigger"] == "idle" for a in mod.ACTIONS):
        fail("needs at least one idle action")
    if any(a.get("sit") for a in mod.ACTIONS) and not any(a.get("sit") and a["trigger"] == "top" for a in mod.ACTIONS):
        fail("sit actions need one with trigger 'top'")
    glyph_palette = {**engine.GLYPH_PALETTE, **getattr(mod, "GLYPH_PALETTE", {})}
    for name, rows in [*glyphs.items(), *([("SNACK", mod.SNACK["glyph"])] if hasattr(mod, "SNACK") else [])]:
        missing = {c for r in rows for c in r} - {"."} - set(glyph_palette)
        if missing:
            fail(f"glyph '{name}' uses colors missing from GLYPH_PALETTE: {sorted(missing)}")


def s(v):
    return json.dumps(v, ensure_ascii=False)


def arr(rows, ind):
    return "\n".join(f"{ind}{s(r)}," for r in rows)


def table(name, layers):
    body = "".join(f"        {s(k)}: [\n{arr(v, '            ')}\n        ],\n" for k, v in layers.items())
    return f"    static let {name}: [String: [String]] = [\n{body}    ]\n"


def nested(name, layers):
    body = "".join(f"        [\n{arr(v, '            ')}\n        ],\n" for v in layers)
    return f"    static let {name} = [\n{body}    ]\n"


def palette(name, colors):
    rows = "".join(f'        "{k}": NSColor(srgbRed: {r:.2f}, green: {g:.2f}, blue: {b:.2f}, alpha: 1),\n' for k, (r, g, b) in colors.items())
    return f"    static let {name}: [Character: NSColor] = [\n{rows}    ]\n"


def action(a):
    frames = ", ".join(
        f"MascotPose(face: {s(f['face']) if 'face' in f else 'nil'}, arms: {s(f.get('arms', 'down'))}, legs: {s(f.get('legs', 'stand'))}, ticks: {f.get('ticks', 1)})"
        for f in a.get("frames", [])
    )
    lift = "nil"
    if "lift" in a:
        l = a["lift"]
        lift = {
            "jump": lambda: f".jump(height: {l['height']})",
            "hop": lambda: f".hop(height: {l['height']}, period: {l['period']})",
            "rise": lambda: f".rise(height: {l['height']}, from: {l['from']}, to: {l['to']})",
            "sink": lambda: f".sink(height: {l['height']})",
            "cling": lambda: f".cling(height: {l['height']})",
        }[l["type"]]()
    effect = "nil"
    if "effect" in a:
        e = a["effect"]
        effect = f"MascotEffect(glyph: {s(e['glyph'])}, period: {e.get('period', 'nil')}, from: {e.get('from', 'nil')}, until: {e.get('until', 'nil')}, dx: {e.get('dx', [0])})"
    duration = f"{a['duration'][0]}...{a['duration'][1]}" if "duration" in a else "nil"
    strength = f"{a['strength'][0]}...{a['strength'][1]}" if "strength" in a else "nil"
    apps = s(a["apps"]) if "apps" in a else "nil"
    nxt = "[" + ", ".join(f"({s(k)}, {v})" for k, v in a.get("next", {}).items()) + "]" if a.get("next") else "[]"
    return (f"        MascotAction(name: {s(a['name'])}, trigger: .{a['trigger']}, weight: {a.get('weight', 1)}, "
            f"walk: {str(a.get('walk', False)).lower()}, sit: {str(a.get('sit', False)).lower()}, duration: {duration}, strength: {strength}, apps: {apps},\n"
            f"                     mood: {s(a['mood']) if 'mood' in a else 'nil'}, moods: {s(a.get('moods', []))},\n"
            f"                     frames: [{frames}],\n"
            f"                     lift: {lift}, effect: {effect}, next: {nxt}),\n")


def outfit_block(i, data):
    out = f"    static let body{i} = [\n{arr(data['body'], '        ')}\n    ]\n\n"
    out += table(f"arms{i}", data["arms"]) + "\n" + table(f"legs{i}", data["legs"]) + "\n"
    for side in ("right", "left"):
        sd = data[side]
        out += f"""    static let {side}Body{i} = [
{arr(sd["body"], "        ")}
    ]

    static let {side}Face{i} = [
{arr(sd["face"], "        ")}
    ]

    static let {side}Blink{i} = [
{arr(sd["blink"], "        ")}
    ]

{nested(side + "Legs" + str(i), sd["legs"])}
{nested(side + "Arms" + str(i), sd["arms"])}
"""
    return out


def accessory_block(id, acc):
    return "".join(f"    static let {side}{id.capitalize()} = [\n{arr(acc[side], '        ')}\n    ]\n\n" for side in ("front", "right", "left"))


def emit(mod, outfits, accessories):
    t = mod.ID[0].upper() + mod.ID[1:] + "Sprites"
    first = outfits[0][2]
    glyph_palette = {**engine.GLYPH_PALETTE, **getattr(mod, "GLYPH_PALETTE", {})}
    out = f'''// Generated by tools/gen_sprites.py from tools/characters/{mod.ID}.py. Do not edit.
import AppKit

@MainActor
enum {t} {{
{palette("palette", palette_of(mod))}
{palette("glyphPalette", glyph_palette)}
{table("faces", first["faces"])}
{table("glyphs", glyphs_of(mod))}
    static let actions = [
{"".join(action(a) for a in mod.ACTIONS)}    ]

'''
    for i, (_, _, data) in enumerate(outfits):
        out += outfit_block(i, data)
    for id, acc in accessories:
        out += accessory_block(id, acc)
    out = out.rstrip() + "\n}\n"
    side = lambda x, i: f"SideSprites(body: {t}.{x}Body{i}, face: {t}.{x}Face{i}, blink: {t}.{x}Blink{i}, legs: {t}.{x}Legs{i}, arms: {t}.{x}Arms{i})"
    outfit_exprs = ",\n".join(
        f"            MascotOutfit(id: {s(id)}, name: {s(name)}, body: {t}.body{i}, arms: {t}.arms{i}, legs: {t}.legs{i}, right: {side('right', i)}, left: {side('left', i)})"
        for i, (id, name, _) in enumerate(outfits))
    accessory_exprs = ",\n".join(
        f"            MascotAccessory(id: {s(id)}, name: {s(engine.ACCESSORY_NAMES[id])}, front: {t}.front{id.capitalize()}, right: {t}.right{id.capitalize()}, left: {t}.left{id.capitalize()})"
        for id, _ in accessories)
    snack = "nil"
    if hasattr(mod, "SNACK"):
        snack = f"MascotSnack(name: {s(mod.SNACK['name'])}, glyph: {s(mod.SNACK['glyph'])})"
    drops = "[" + ", ".join(f"{s(k)}: {v}" for k, v in first.get("drops", {}).items()) + "]" if first.get("drops") else "[:]"
    out += f'''
extension MascotCharacter {{
    static let {mod.ID} = MascotCharacter(
        id: {s(mod.ID)},
        name: {s(mod.NAME)},
        width: {mod.W},
        palette: {t}.palette,
        glyphPalette: {t}.glyphPalette,
        faces: {t}.faces,
        drops: {drops},
        glyphs: {t}.glyphs,
        actions: {t}.actions,
        snack: {snack},
        outfits: [
{outfit_exprs}
        ],
        accessories: [
{accessory_exprs}
        ]
    )
}}
'''
    (OUT / f"{t}.swift").write_text(out)


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.swift"):
        old.unlink()
    mods = sorted((load(p) for p in (ROOT / "characters").glob("*.py")), key=lambda m: (m.ORDER, m.ID))
    previews, warnings = [], []
    for mod in mods:
        engine.configure(mod.W, mod.H, mod.OY)
        outfits = [(id, name, mod.build(id)) for id, name in getattr(mod, "OUTFITS", [("default", "標準")])]
        for id, _, data in outfits:
            check(mod, data, id)
            warnings += lint(mod, id, data)
        accessories = [(id, engine.accessory(id, mod.SX + mod.HX)) for id in getattr(mod, "ACCESSORIES", [])]
        emit(mod, outfits, accessories)
        previews.append((mod, palette_of(mod), [(id, data) for id, _, data in outfits]))
    ids = ", ".join(f".{m.ID}" for m in mods)
    (OUT / "AllCharacters.swift").write_text(
        "// Generated by tools/gen_sprites.py. Do not edit.\n\n"
        f"extension MascotCharacter {{\n    static let all: [MascotCharacter] = [{ids}]\n}}\n"
    )
    write_previews(previews, PREVIEWS)
    for w in warnings:
        print("warning:", w)
    print("generated:", ", ".join(m.ID for m in mods))
    print("previews:", PREVIEWS)


if __name__ == "__main__":
    main()
