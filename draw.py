#!/usr/bin/env python3
"""Draw 'The World Today - 22 November 2026', a newspaper-style infographic.

The picture sums up Sunday 22 November 2026 in six stories plus a footer
of four more headlines. It is drawn from scratch with Pillow only: no
network, no photos, no copied artwork. Running this file always writes
the same bytes to entry.png next to it.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

PAGE = 1024
EDGE = 34
GAP = 20
INNER = PAGE - 2 * EDGE

PAPER = (247, 243, 232)
CARD = (255, 255, 255)
INK = (26, 26, 24)
MUTED = (96, 92, 84)
ACCENT = (176, 32, 32)
RULE = (208, 200, 184)
NAVY = (28, 49, 86)
SKY = (146, 190, 228)
LEAF = (74, 148, 78)
FLAME = (224, 92, 32)
EMBER = (240, 176, 40)
GRAPE = (104, 78, 160)
SAND = (232, 214, 160)

FONT_HOME = "/usr/share/fonts/truetype/dejavu"


def font(face, size):
    try:
        return ImageFont.truetype(f"{FONT_HOME}/{face}", size)
    except OSError:
        return ImageFont.load_default()


TITLE = font("DejaVuSerif-Bold.ttf", 66)
DATE = font("DejaVuSans-Bold.ttf", 25)
TAG = font("DejaVuSans-Bold.ttf", 19)
TAG_SMALL = font("DejaVuSans-Bold.ttf", 17)
HEAD_BIG = font("DejaVuSerif-Bold.ttf", 38)
HEAD_MID = font("DejaVuSerif-Bold.ttf", 26)
HEAD_WIDE = font("DejaVuSerif-Bold.ttf", 29)
BODY_BIG = font("DejaVuSans.ttf", 21)
BODY_MID = font("DejaVuSans.ttf", 19)
FOOT_HEAD = font("DejaVuSans-Bold.ttf", 20)
FOOT_ITEM = font("DejaVuSans.ttf", 18)


def split_lines(pen, text, face, width):
    """Break text into as few lines as fit inside width."""
    words = text.split()
    rows = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if pen.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                rows.append(current)
            current = word
    if current:
        rows.append(current)
    return rows


def block(pen, x, y, text, face, width, colour, step):
    """Draw wrapped text, return the y just below it."""
    for row in split_lines(pen, text, face, width):
        pen.text((x, y), row, font=face, fill=colour)
        y += step
    return y


def framed_card(pen, x, y, w, h):
    pen.rounded_rectangle([x, y, x + w, y + h], radius=10,
                          fill=CARD, outline=RULE, width=1)


def globe_mark(pen, cx, cy, r):
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=INK, width=3)
    pen.arc([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
            start=270, end=90, fill=INK, width=2)
    pen.arc([cx - r * 0.85, cy - r * 0.55, cx + r * 0.85, cy + r * 0.55],
            start=270, end=90, fill=INK, width=2)
    pen.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    pen.ellipse([cx - r * 0.55, cy - r * 0.62, cx - r * 0.05, cy - r * 0.18],
                fill=LEAF)
    pen.ellipse([cx + r * 0.02, cy + r * 0.12, cx + r * 0.58, cy + r * 0.58],
                fill=LEAF)


def flame_mark(pen, cx, cy, r):
    base = r * 1.05
    pen.rectangle([cx - base, cy + r * 0.45, cx + base, cy + r * 0.95],
                  fill=(52, 52, 54))
    pen.rectangle([cx - base * 0.55, cy - r * 0.05, cx - base * 0.05,
                   cy + r * 0.45], fill=(52, 52, 54))
    pen.rectangle([cx + base * 0.12, cy + r * 0.12, cx + base * 0.62,
                   cy + r * 0.45], fill=(52, 52, 54))
    pen.polygon([(cx - r * 0.52, cy + r * 0.42), (cx - r * 0.42, cy - r * 0.35),
                 (cx - r * 0.12, cy - r * 0.05), (cx + r * 0.05, cy - r * 0.62),
                 (cx + r * 0.28, cy - r * 0.18), (cx + r * 0.5, cy + r * 0.42)],
                fill=FLAME)
    pen.polygon([(cx - r * 0.26, cy + r * 0.42), (cx - r * 0.2, cy - r * 0.12),
                 (cx + r * 0.02, cy + r * 0.08), (cx + r * 0.22, cy - r * 0.28),
                 (cx + r * 0.3, cy + r * 0.42)], fill=EMBER)


def shield_mark(pen, cx, cy, r):
    pen.polygon([(cx - r * 0.78, cy - r * 0.62), (cx + r * 0.78, cy - r * 0.62),
                 (cx + r * 0.78, cy + r * 0.1), (cx, cy + r * 0.95),
                 (cx - r * 0.78, cy + r * 0.1)], fill=NAVY)
    pen.ellipse([cx - r * 0.2, cy - r * 0.38, cx + r * 0.2, cy + r * 0.02],
                fill=CARD)
    pen.polygon([(cx - r * 0.14, cy - r * 0.05), (cx + r * 0.14, cy - r * 0.05),
                 (cx + r * 0.3, cy + r * 0.55), (cx - r * 0.3, cy + r * 0.55)],
                fill=CARD)


def flag_mark(pen, cx, cy, r):
    pen.line([cx - r * 0.62, cy - r * 0.95, cx - r * 0.62, cy + r * 0.95],
             fill=INK, width=5)
    top = cy - r * 0.92
    left = cx - r * 0.55
    cell = r * 0.34
    for row in range(3):
        for col in range(4):
            if (row + col) % 2 == 0:
                pen.rectangle([left + col * cell, top + row * cell,
                               left + (col + 1) * cell, top + (row + 1) * cell],
                              fill=INK)
    pen.rectangle([left, top, left + 4 * cell, top + 3 * cell],
                  outline=INK, width=2)


def pad_mark(pen, cx, cy, r):
    pen.rounded_rectangle([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62],
                          radius=16, fill=GRAPE)
    pen.line([cx - r * 0.52, cy, cx - r * 0.22, cy], fill=CARD, width=6)
    pen.line([cx - r * 0.37, cy - r * 0.15, cx - r * 0.37, cy + r * 0.15],
             fill=CARD, width=6)
    for bx, by, shade in ((r * 0.3, -r * 0.18, EMBER),
                          (r * 0.52, r * 0.02, CARD),
                          (r * 0.3, r * 0.22, (120, 220, 130))):
        pen.ellipse([cx + bx - 7, cy + by - 7, cx + bx + 7, cy + by + 7],
                    fill=shade)


def tower_mark(pen, cx, cy, r):
    pen.rectangle([cx - r * 0.34, cy - r * 0.9, cx + r * 0.34, cy + r * 0.95],
                  fill=SAND, outline=INK, width=2)
    pen.polygon([(cx - r * 0.44, cy - r * 0.9), (cx, cy - r * 1.15),
                 (cx + r * 0.44, cy - r * 0.9)], fill=INK)
    pen.ellipse([cx - r * 0.27, cy - r * 0.78, cx + r * 0.27, cy - r * 0.24],
                fill=CARD, outline=INK, width=2)
    pen.line([cx, cy - r * 0.51, cx, cy - r * 0.62], fill=INK, width=3)
    pen.line([cx, cy - r * 0.51, cx + r * 0.13, cy - r * 0.44], fill=INK, width=3)
    for wy in (-0.08, 0.22, 0.52):
        pen.rectangle([cx - r * 0.16, cy + r * wy, cx + r * 0.16,
                       cy + r * (wy + 0.16)], fill=INK)


MARKS = {
    "globe": globe_mark,
    "flame": flame_mark,
    "shield": shield_mark,
    "flag": flag_mark,
    "pad": pad_mark,
    "tower": tower_mark,
}

LEAD = {
    "tag": "ANTALYA, TURKEY  —  CLIMATE",
    "mark": "globe",
    "head": "COP31 IN OVERTIME AS NEW DRAFT SEEKS TO SAVE TALKS",
    "body": "Climate talks run into a second day of overtime, split over "
            "fossil fuels and funding for poorer nations.",
}

GRID = [
    {
        "tag": "INDONESIA",
        "mark": "flame",
        "head": "36 MISSING AFTER CANDY FACTORY FIRE",
        "body": "Candy factory fire in Banten kills 3, injures 4; "
                "36 workers still missing.",
    },
    {
        "tag": "UNITED STATES",
        "mark": "shield",
        "head": "FBI PROBES REPORTED HACK",
        "body": "FBI investigates an apparent breach of the NCIC "
                "database used by police.",
    },
    {
        "tag": "SPORT — FORMULA 1",
        "mark": "flag",
        "head": "VERSTAPPEN WINS WILD LAS VEGAS GP",
        "body": "Norris and Piastri on the podium; Russell crashes "
                "and the Ferraris collide.",
    },
    {
        "tag": "UNITED STATES",
        "mark": "pad",
        "head": "TEEN GAMER HELPS FBI RESCUE GIRL",
        "body": "A 16-year-old met a girl in an online game, then "
                "helped the FBI rescue her.",
    },
]

WIDE = {
    "tag": "BRITAIN",
    "mark": "tower",
    "head": "MAY 'AGHAST' AT BURNHAM'S EU PLANS",
    "body": "The former PM tells the BBC 'Brexit is done' as Andy "
            "Burnham floats closer ties with the EU.",
}

ALSO = [
    "Alcaraz v Zverev in tonight's ATP Finals decider",
    "St. Johns River flood still at record levels",
    "BBC apologises for Strictly noise disruption",
    "Kate's new documentary leads the front pages",
]


def header(pen):
    title = "THE WORLD TODAY"
    pen.text(((PAGE - pen.textlength(title, font=TITLE)) / 2, 24),
             title, font=TITLE, fill=INK)
    dateline = "SUNDAY, 22 NOVEMBER 2026"
    pen.text(((PAGE - pen.textlength(dateline, font=DATE)) / 2, 106),
             dateline, font=DATE, fill=ACCENT)
    pen.line([EDGE, 150, PAGE - EDGE, 150], fill=INK, width=3)
    pen.line([EDGE, 156, PAGE - EDGE, 156], fill=INK, width=1)


def lead_story(pen, y, height):
    framed_card(pen, EDGE, y, INNER, height)
    pen.text((EDGE + 22, y + 14), LEAD["tag"], font=TAG, fill=ACCENT)
    text_w = INNER - 44 - 168
    block(pen, EDGE + 22, y + 46, LEAD["head"], HEAD_BIG, text_w, INK, 46)
    block(pen, EDGE + 22, y + 142, LEAD["body"], BODY_BIG, text_w, MUTED, 27)
    MARKS[LEAD["mark"]](pen, PAGE - EDGE - 22 - 72, y + height // 2, 66)


def grid_story(pen, x, y, w, h, story):
    framed_card(pen, x, y, w, h)
    pen.text((x + 16, y + 12), story["tag"], font=TAG_SMALL, fill=ACCENT)
    icon_y = y + 44
    MARKS[story["mark"]](pen, x + 16 + 38, icon_y + 38, 36)
    head_x = x + 110
    head_w = w - 110 - 16
    block(pen, head_x, y + 42, story["head"], HEAD_MID, head_w, INK, 31)
    block(pen, x + 16, y + 122, story["body"], BODY_MID, w - 32, MUTED, 24)


def wide_story(pen, y, height):
    framed_card(pen, EDGE, y, INNER, height)
    pen.text((EDGE + 22, y + 12), WIDE["tag"], font=TAG, fill=ACCENT)
    MARKS[WIDE["mark"]](pen, EDGE + 22 + 42, y + height // 2 + 16, 36)
    text_x = EDGE + 22 + 104
    text_w = INNER - 22 - 104 - 22
    block(pen, text_x, y + 40, WIDE["head"], HEAD_WIDE, text_w, INK, 35)
    block(pen, text_x, y + 78, WIDE["body"], BODY_MID, text_w, MUTED, 24)


def footer(pen, y, height):
    pen.rounded_rectangle([EDGE, y, PAGE - EDGE, y + height], radius=10,
                          fill=NAVY)
    pen.text((EDGE + 22, y + 12), "ALSO TODAY", font=FOOT_HEAD,
             fill=(255, 255, 255))
    col_w = (INNER - 44 - GAP) // 2
    for idx, item in enumerate(ALSO):
        col = idx % 2
        row = idx // 2
        ix = EDGE + 22 + col * (col_w + GAP)
        iy = y + 46 + row * 28
        pen.text((ix, iy), "▪", font=FOOT_ITEM, fill=(255, 255, 255))
        block(pen, ix + 20, iy, item, FOOT_ITEM, col_w - 20,
              (235, 238, 245), 22)


def paint():
    canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
    pen = ImageDraw.Draw(canvas)
    header(pen)
    lead_story(pen, 168, 196)
    cell_w = (INNER - GAP) // 2
    cell_h = 178
    for pos, story in enumerate(GRID):
        cx = EDGE + (pos % 2) * (cell_w + GAP)
        cy = 380 + (pos // 2) * (cell_h + GAP)
        grid_story(pen, cx, cy, cell_w, cell_h, story)
    wide_story(pen, 768, 118)
    footer(pen, 902, 102)
    return canvas


if __name__ == "__main__":
    paint().save(HERE / "entry.png")
    print("wrote", HERE / "entry.png")
