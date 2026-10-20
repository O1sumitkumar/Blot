"""Generate Sora's pixel-art SVGs: one file per palette and expression.

Run:  python assets/sora/build_sprites.py
Out:  assets/sora/<palette>/<expression>.svg   (28x14 grid, crisp at any size)

Sora's body shape is modeled on "Animated Pixel Slime" by rvros
(https://rvros.itch.io/pixel-art-animated-slime, CC0 1.0), recolored and given new expressions.
"""

from __future__ import annotations

from pathlib import Path

BODY = [
    "..........HHHHHHH...........",
    ".......HHHLLLLLLLHHH........",
    ".....HHLLLMMMMMMMLLLHH......",
    "....HLLMMMMMMMMMMMMMLLH.....",
    "...HLMMMMMMMMMMMMMMMMMLH....",
    "..HLMMDDDMMMMMMMMMMMMMMLH...",
    "..HLMDDDDDMMMMMMMMMMMMMMLH..",
    ".HLMMDDDDDDMMMMMMMMMMMMMMLH.",
    ".HLMDDDDDDDDDDMMMMMMMMMMMML.",
    ".LMMDDDDDDDDDDDDDDDDDMMMMML.",
    "LLMMMDDDDDDDDDDDDDDDDDDMMMLL",
    "LLLMMMMMMMMMMMMMMMMMMMMMMLLL",
    "LLLLLLLLLLLLLLLLLLLLLLLLLLLL",
    ".SSSSSSSSSSSSSSSSSSSSSSSSSS.",
]

PALETTES = {
    "orange": {"H": "#F6D3A8", "L": "#E39A5B", "M": "#C4703A", "D": "#94491F", "E": "#3E1A10"},
    "sage": {"H": "#E1E8CF", "L": "#A9BC8E", "M": "#7F9668", "D": "#566A45", "E": "#6E2230"},
    "blue": {"H": "#B9C7E0", "L": "#6F86B8", "M": "#3F5689", "D": "#25345C", "E": "#D9663F"},
    "mustard": {"H": "#F4E2AE", "L": "#D9B45A", "M": "#B08A35", "D": "#7A5D22", "E": "#4A2414"},
}
FIXED = {"W": "#FFF6E8", "A": "#E8A33B", "T": "#9FC9DD", "S": "#000000"}

# (column, row, color key) drawn over the body; negative rows sit above Sora's head.
EYE = [(6, 6, "E"), (7, 6, "E"), (6, 7, "E"), (7, 7, "E"), (6, 6, "W")]
FACES = {
    "idle": EYE,
    "happy": [(5, 7, "E"), (6, 6, "E"), (7, 6, "E"), (8, 7, "E")],
    "alert": [(6, 5, "E"), (7, 5, "E"), *EYE, (6, 5, "W"),
              (4, -6, "A"), (4, -5, "A"), (4, -4, "A"), (4, -2, "A")],
    "worried": [*EYE, (5, 4, "E"), (6, 4, "E"), (7, 3, "E"),
                (11, 2, "T"), (11, 3, "T"), (12, 3, "T")],
    "sleepy": [(5, 7, "E"), (6, 7, "E"), (7, 7, "E"), (8, 7, "E"),
               (11, -6, "A"), (12, -6, "A"), (13, -6, "A"), (14, -6, "A"),
               (13, -5, "A"), (12, -4, "A"),
               (11, -3, "A"), (12, -3, "A"), (13, -3, "A"), (14, -3, "A")],
    "sad": [(6, 7, "E"), (7, 7, "E"), (6, 8, "E"), (7, 8, "E"), (6, 7, "W"),
            (5, 5, "E"), (6, 5, "E"), (7, 4, "E"), (6, 9, "T"), (6, 10, "T")],
}

TOP = 6  # rows of headroom for "!" and "z"


def svg(palette: dict[str, str], face: str) -> str:
    height = len(BODY) + TOP
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 {height}" '
        f'shape-rendering="crispEdges" role="img" aria-label="Sora, {face}">'
        + _rects(palette, face)
        + "</svg>\n"
    )


# Squished frame: the dome's top row pressed down into the body; the face drops one pixel with it.
SQUISH = ["." * 28] + BODY[1:]


def _rects(palette: dict[str, str], face: str, squish: bool = False, flip: bool = False, dx: int = 0) -> str:
    colors = {**palette, **FIXED}
    cells: dict[tuple[int, int], str] = {}
    for y, row in enumerate(SQUISH if squish else BODY):
        for x, key in enumerate(row):
            if key != ".":
                cells[(x, y + TOP)] = key
    for x, y, key in FACES[face]:
        cells[(x, y + TOP + (1 if squish and y >= 0 else 0))] = key
    rects = []
    for (x, y), key in sorted(cells.items(), key=lambda c: (c[0][1], c[0][0])):
        extra = ' fill-opacity="0.18"' if key == "S" else ""
        px = (27 - x if flip else x) + dx
        rects.append(f'<rect x="{px}" y="{y}" width="1" height="1" fill="{colors[key]}"{extra}/>')
    return "".join(rects)


def _toggle(index: int, count: int, dur: str) -> str:
    """SMIL: show this frame for 1/count of the cycle, hidden otherwise."""
    values = ";".join("1" if i == index else "0" for i in range(count))
    times = ";".join(f"{i / count:.4f}" for i in range(count))
    return (f'<animate attributeName="opacity" values="{values}" keyTimes="{times}" '
            f'calcMode="discrete" dur="{dur}" repeatCount="indefinite"/>')


def walk_svg(palette: dict[str, str], width: int = 120, seconds: float = 8.0) -> str:
    """Sora squish-slides right, turns around, slides back. Animated with SMIL (plays on GitHub)."""
    travel = width - 28
    height = len(BODY) + TOP
    groups = []
    for d, flip in enumerate((True, False)):  # 0: heading right (eye in front), 1: heading left
        frames = "".join(
            f'<g opacity="{1 if s == 0 else 0}">{_rects(palette, "idle", squish=bool(s), flip=flip)}{_toggle(s, 2, "0.6s")}</g>'
            for s in range(2)
        )
        groups.append(f'<g opacity="{1 if d == 0 else 0}">{frames}{_toggle(d, 2, f"{seconds}s")}</g>')
    move = (f'<animateTransform attributeName="transform" type="translate" values="0 0;{travel} 0;0 0" '
            f'dur="{seconds}s" repeatCount="indefinite"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'shape-rendering="crispEdges" role="img" aria-label="Sora the slime walking">'
        f'<g>{"".join(groups)}{move}</g></svg>\n'
    )


def faces_svg(palette: dict[str, str], each: float = 1.4) -> str:
    """Sora cycling through every expression, squishing gently in each."""
    height = len(BODY) + TOP
    names = list(FACES)
    groups = []
    for i, face in enumerate(names):
        frames = "".join(
            f'<g opacity="{1 if s == 0 else 0}">{_rects(palette, face, squish=bool(s))}{_toggle(s, 2, "0.7s")}</g>'
            for s in range(2)
        )
        groups.append(f'<g opacity="{1 if i == 0 else 0}">{frames}{_toggle(i, len(names), f"{each * len(names)}s")}</g>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 {height}" '
        f'shape-rendering="crispEdges" role="img" aria-label="Sora showing each expression">'
        + "".join(groups)
        + "</svg>\n"
    )


def main() -> None:
    root = Path(__file__).parent
    for name, palette in PALETTES.items():
        out = root / name
        out.mkdir(exist_ok=True)
        for face in FACES:
            (out / f"{face}.svg").write_text(svg(palette, face), encoding="utf-8")
        (out / "walk.svg").write_text(walk_svg(palette), encoding="utf-8")
        (out / "faces.svg").write_text(faces_svg(palette), encoding="utf-8")
    print(f"wrote {len(PALETTES) * (len(FACES) + 2)} sprites to {root}")


if __name__ == "__main__":
    main()
