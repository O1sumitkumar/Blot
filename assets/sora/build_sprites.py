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
    colors = {**palette, **FIXED}
    cells: dict[tuple[int, int], str] = {}
    for y, row in enumerate(BODY):
        for x, key in enumerate(row):
            if key != ".":
                cells[(x, y + TOP)] = key
    for x, y, key in FACES[face]:
        cells[(x, y + TOP)] = key
    rects = []
    for (x, y), key in sorted(cells.items(), key=lambda c: (c[0][1], c[0][0])):
        extra = ' fill-opacity="0.18"' if key == "S" else ""
        rects.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{colors[key]}"{extra}/>')
    height = len(BODY) + TOP
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 {height}" '
        f'shape-rendering="crispEdges" role="img" aria-label="Sora, {face}">'
        + "".join(rects)
        + "</svg>\n"
    )


def main() -> None:
    root = Path(__file__).parent
    for name, palette in PALETTES.items():
        out = root / name
        out.mkdir(exist_ok=True)
        for face in FACES:
            (out / f"{face}.svg").write_text(svg(palette, face), encoding="utf-8")
    print(f"wrote {len(PALETTES) * len(FACES)} sprites to {root}")


if __name__ == "__main__":
    main()
