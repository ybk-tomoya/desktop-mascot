import base_character as base

EYE_FACES = ("normal", "blink", "happy", "smile")
MAX_HOLE = 8


def eye_contact_rows(body, face, oy):
    rows = {"left": set(), "right": set()}
    width = len(face[0])
    for y, row in enumerate(face):
        if y < 18 + oy:
            continue
        for x, c in enumerate(row):
            if c != "K":
                continue
            if body[y][x] == "K" or any(0 <= nx < width and face[y][nx] == "." and body[y][nx] == "K" for nx in (x - 1, x + 1)):
                rows["left" if x < width / 2 else "right"].add(y)
    return rows


def holes(rows):
    h, w = len(rows), len(rows[0])
    outside = {(x, y) for y in range(h) for x in range(w) if (x in (0, w - 1) or y in (0, h - 1)) and rows[y][x] == "."}
    stack = list(outside)
    while stack:
        x, y = stack.pop()
        for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= p[0] < w and 0 <= p[1] < h and p not in outside and rows[p[1]][p[0]] == ".":
                outside.add(p)
                stack.append(p)
    inside = {(x, y) for y in range(h) for x in range(w) if rows[y][x] == "." and (x, y) not in outside}
    groups = []
    while inside:
        group = [inside.pop()]
        for x, y in group:
            for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if p in inside:
                    inside.remove(p)
                    group.append(p)
        groups.append(group)
    return groups


def lint(mod, outfit, data):
    oy = mod.OY
    warnings = []
    for name in EYE_FACES:
        if name in data["faces"]:
            for side, ys in eye_contact_rows(data["body"], data["faces"][name], oy).items():
                if len(ys) >= 2:
                    warnings.append(f"face '{name}': {side} eye touches the outline on rows {sorted(y - oy for y in ys)} (move the hair beside the face outward)")
    if "down" in data["arms"]:
        arms = data["arms"]["down"]
        for _, _, (hx, hy) in base.ARM_POSES["down"]:
            skin = sum(1 for y, row in enumerate(arms) for x, c in enumerate(row)
                       if c in "Ss" and (x + 0.5 - hx) ** 2 + (y - oy + 0.5 - hy) ** 2 <= 2.5 ** 2)
            if skin == 0:
                warnings.append(f"arms 'down': the hand at {(hx, hy)} is hidden (shorten the sleeve reach)")
    layers = {"body": data["body"], "right body": data["right"]["body"],
              **{f"arms '{k}'": v for k, v in data["arms"].items()}, **{f"legs '{k}'": v for k, v in data["legs"].items()}}
    for name, rows in layers.items():
        for group in holes(rows):
            if len(group) <= MAX_HOLE:
                x, y = min(group, key=lambda p: (p[1], p[0]))
                warnings.append(f"{name}: small closed gap of {len(group)}px at {(x, y - oy)} (it gets an inner outline)")
    return [f"{mod.ID}/{outfit}: {w}" for w in warnings]
