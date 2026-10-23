#!/usr/bin/env python3
"""Render the BeautifulRust banner: a painter at an easel painting a crab.

Pixel art is defined as text grids below. Run `python3 assets/banner.py` to
regenerate assets/banner.png. No dependencies beyond the standard library.
"""
import struct
import zlib
from pathlib import Path

SCALE = 10
WIDTH, HEIGHT = 112, 48

PALETTE = {
    "_": (0xF7, 0xF0, 0xE4),  # background cream
    "f": (0xD9, 0xCB, 0xAE),  # floor
    "F": (0xC4, 0xB3, 0x92),  # floor shadow line
    "B": (0x2F, 0x3A, 0x6E),  # beret
    "S": (0xF3, 0xC9, 0xA4),  # skin
    "s": (0xD8, 0xA5, 0x7E),  # skin shadow
    "K": (0x1E, 0x1E, 0x2A),  # dark (eyes, pants)
    "M": (0x4A, 0x32, 0x24),  # mustache / hair
    "G": (0x6F, 0x92, 0xC2),  # smock
    "g": (0x53, 0x72, 0x9E),  # smock shadow
    "W": (0xFF, 0xFF, 0xFF),  # white
    "w": (0xFB, 0xF9, 0xF3),  # canvas
    "N": (0x8E, 0x5B, 0x2C),  # wood
    "n": (0x5C, 0x39, 0x1A),  # dark wood
    "T": (0xDF, 0xB8, 0x80),  # palette wood
    "O": (0xF5, 0x6D, 0x1F),  # crab orange
    "o": (0xFF, 0x9E, 0x5E),  # crab highlight
    "r": (0xC2, 0x4E, 0x12),  # crab shadow
    "R": (0xD6, 0x33, 0x3A),  # red paint
    "Y": (0xF2, 0xC9, 0x3B),  # yellow paint
    "L": (0x3B, 0x7D, 0xD8),  # blue paint
    "V": (0x4C, 0xA8, 0x5A),  # green paint
    "p": (0xC9, 0xC2, 0xB6),  # pencil sketch on canvas
    "b": (0xBF, 0xE3, 0xF5),  # window sky
    "c": (0xFF, 0xFF, 0xFF),  # cloud
}

# Painter, facing right. Hand, brush handle and tip extend to the right edge.
PAINTER = [
    "....BBBBBBB.........",
    "..BBBBBBBBBBB.......",
    ".BBBBBBBBBBBBBB.....",
    "...SSSSSSSSS........",
    "...SSSSSSSSS........",
    "...SSKSSSKSS........",
    "...SSSSSSSSSs.......",
    "...SSMMMMMSS........",
    "....SSSSSSS.........",
    ".....sSSSs..........",
    "....GGGGGGG.........",
    "..GGGGGGGGGGG.......",
    ".GGGGGGGGGGGGGGGG.......",
    ".GGGGGGGGGGGGGGGGSS.....",
    ".GGGGGGGGGGGGGGGGSSnnnnO",
    ".GgGGGGGGGGGGGG.....",
    ".GgGGGGGGGGGG.......",
    ".GgGGGGGGGGGG.......",
    ".GgGGGGGGGGGG.......",
    "..GGGGGGGGGGG.......",
    "..GGGGGGGGGGG.......",
    "..GGGGGGGGGGG.......",
    "..ggggggggggg.......",
    "...KKK...KKK........",
    "...KKK...KKK........",
    "...KKK...KKK........",
    "...KKK...KKK........",
    "..nnnn..nnnn........",
]

# Palette held in the left hand.
PAINT_PALETTE = [
    "..TTTTTT..",
    ".TRTTYTTLT",
    "TTTTTTTTTT",
    ".TVTTOTTTT",
    "..TTTTTT..",
]

# Canvas with frame. The painting is blitted onto it.
CANVAS_W, CANVAS_H = 28, 22

# Small crab, painted on the canvas (unfinished on the right: that's where the brush is).
CRAB_SMALL = [
    "pp.....O..O.....OO",
    "ppp...OOOOOO...OOO",
    ".pp..OOOOOOOO..OO.",
    "..p.OOOOOOOOOO.O..",
    "....OOWKOOWKOO....",
    "....OOKKOOKKOO....",
    "....OOrOOOOrOO....",
    "...OOOOrrrrOOOO...",
    "....r.r.r.r.r.r...",
    "...r..r..r..r..r..",
]

# The live model: a bigger crab, posing on a stool.
CRAB_BIG = [
    "..OOO.......O......O.......OOO..",
    ".OOOOO.....OOO....OOO.....OOOOO.",
    ".OO.OO....OOOOOOOOOOOO....OO.OO.",
    "..OOOO...OOOOOOOOOOOOOO...OOOO..",
    "...OOO..OOOOOOOOOOOOOOOO..OOO...",
    "....OOOOOOWKKOOOOOOWKKOOOOOO....",
    ".....OOOOOKKKOOOOOOKKKOOOOO.....",
    "......OOOOKKKOOOOOOKKKOOOO......",
    "......OOOOOOrOOOOOOrOOOOOO......",
    ".......OOOOOOrrrrrrOOOOOO.......",
    "........OOOOOOOOOOOOOOOO........",
    ".........r.r.r....r.r.r.........",
    "........r..r..r..r..r..r........",
]

STOOL = [
    "nnnnnnnnnnnnnnnnnnnn",
    ".NN..............NN.",
    ".NN..............NN.",
    ".NN..............NN.",
    ".NN..............NN.",
]


WINDOW = [
    "nnnnnnnnnnnnnnn",
    "nbbbbbbnbbbbbbn",
    "nbbbbbbnbbbbbbn",
    "nbbccbbnbbbbbbn",
    "nbccccbnbbbbbbn",
    "nbbbbbbnbbbbbbn",
    "nnnnnnnnnnnnnnn",
    "nbbbbbbnbbbbbbn",
    "nbbbbbbnbbbbbbn",
    "nbbbbbbnbbbcbbn",
    "nbbbbbbnbbcccbn",
    "nbbbbbbnbbbbbbn",
    "nnnnnnnnnnnnnnn",
]


def blit(grid, sprite, x0, y0):
    for dy, row in enumerate(sprite):
        for dx, ch in enumerate(row):
            if ch == ".":
                continue
            x, y = x0 + dx, y0 + dy
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                grid[y][x] = ch


def rect(grid, x0, y0, w, h, ch):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                grid[y][x] = ch


def build():
    grid = [["_"] * WIDTH for _ in range(HEIGHT)]
    floor_y = 42
    rect(grid, 0, floor_y, WIDTH, HEIGHT - floor_y, "f")
    rect(grid, 0, floor_y, WIDTH, 1, "F")

    blit(grid, WINDOW, 92, 5)

    # Easel: canvas on three legs with a ledge and a top peg.
    cx, cy = 38, 15
    rect(grid, cx, cy, CANVAS_W, CANVAS_H, "n")                   # frame
    rect(grid, cx + 1, cy + 1, CANVAS_W - 2, CANVAS_H - 2, "w")   # canvas
    blit(grid, CRAB_SMALL, cx + 5, cy + 8)
    leg_top = cy + CANVAS_H
    rect(grid, cx + 3, leg_top, 2, floor_y - leg_top, "N")
    rect(grid, cx + CANVAS_W - 5, leg_top, 2, floor_y - leg_top, "N")
    rect(grid, cx + CANVAS_W // 2 - 1, leg_top, 2, floor_y - leg_top, "n")
    rect(grid, cx + 1, leg_top, CANVAS_W - 2, 1, "n")              # ledge
    rect(grid, cx + CANVAS_W // 2 - 1, cy - 3, 2, 3, "N")          # top peg

    # Painter beside the easel. The brush tip lands on the sketched claw.
    px, py = cx - 16, floor_y - len(PAINTER)
    blit(grid, PAINTER, px, py)
    blit(grid, PAINT_PALETTE, px - 5, py + 14)

    # The model, posing on a stool.
    sx, sy = 76, floor_y - len(STOOL)
    blit(grid, STOOL, sx, sy)
    blit(grid, CRAB_BIG, sx - 6, sy - len(CRAB_BIG))

    return grid


def write_png(path, grid):
    raw = bytearray()
    for row in grid:
        line = bytearray()
        for ch in row:
            line += bytes(PALETTE[ch]) * SCALE
        for _ in range(SCALE):
            raw += b"\x00" + line

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    w, h = WIDTH * SCALE, HEIGHT * SCALE
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    Path(path).write_bytes(png)
    return w, h


if __name__ == "__main__":
    out = Path(__file__).with_name("banner.png")
    w, h = write_png(out, build())
    print(f"wrote {out} ({w}x{h})")
