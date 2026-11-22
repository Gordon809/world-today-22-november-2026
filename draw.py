#!/usr/bin/env python3
"""Draws THE WORLD TODAY — Sunday 22 November 2026.

A 1024x1024 newspaper-style infographic, drawn with PIL only, no network.
Stories are the events of Sunday 22 November 2026, as reported that day.
Run:  python3 draw.py   -> writes entry.png next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 247, 238)   # newsprint cream
CARD = (255, 255, 255)
INK = (22, 22, 22)
MUTED = (80, 80, 80)
RED = (178, 34, 34)
NAVY = (30, 58, 95)
GOLD = (198, 142, 30)
TEAL = (14, 116, 144)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------- icons: small drawings inside a square badge ----------------

def icon_globe(d, x, y, s):
    # planet earth: blue disc, green land, sun in the corner
    d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=(147, 197, 253),
              outline=NAVY, width=3)
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 26, cy - 26, cx - 2, cy - 4], fill=(34, 139, 34))
    d.ellipse([cx + 2, cy + 2, cx + 26, cy + 24], fill=(34, 139, 34))
    d.ellipse([cx - 8, cy + 12, cx + 10, cy + 28], fill=(34, 139, 34))
    for k in range(8):
        ang = math.pi * k / 4
        d.line([cx + 34 * math.cos(ang), cy + 34 * math.sin(ang),
                cx + 42 * math.cos(ang), cy + 42 * math.sin(ang)],
               fill=GOLD, width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD, outline=INK, width=1)


def icon_flame(d, x, y, s):
    # factory fire: orange flame over a small building
    d.rounded_rectangle([x + 4, y + 4, x + s - 4, y + s - 4], radius=10,
                        fill=(254, 226, 226))
    cx = x + s // 2
    d.rectangle([cx - 26, y + s - 34, cx + 26, y + s - 10], fill=(68, 64, 60))
    d.rectangle([cx - 26, y + s - 34, cx + 26, y + s - 28], fill=(120, 113, 108))
    for wx in (cx - 18, cx - 2, cx + 14):
        d.rectangle([wx, y + s - 22, wx + 8, y + s - 14], fill=(254, 202, 202))
    # flame: three stacked ellipses, red outside, gold inside
    d.ellipse([cx - 16, y + 10, cx + 16, y + 48], fill=(220, 38, 38))
    d.ellipse([cx - 10, y + 20, cx + 10, y + 48], fill=(249, 115, 22))
    d.ellipse([cx - 5, y + 30, cx + 5, y + 48], fill=(253, 224, 71))


def icon_shield(d, x, y, s):
    # shield with a keyhole: the hacked database
    d.rounded_rectangle([x + 4, y + 4, x + s - 4, y + s - 4], radius=10,
                        fill=(239, 246, 255))
    cx = x + s // 2
    pts = [(cx, y + 10), (cx + 26, y + 20), (cx + 26, y + 44),
           (cx, y + s - 10), (cx - 26, y + 44), (cx - 26, y + 20)]
    d.polygon(pts, fill=NAVY, outline=INK)
    d.ellipse([cx - 7, y + 28, cx + 7, y + 42], fill=(255, 255, 255))
    d.polygon([(cx - 4, y + 40), (cx + 4, y + 40), (cx + 7, y + 56),
               (cx - 7, y + 56)], fill=(255, 255, 255))
    d.text((x + s - 8, y + 8), "!", font=font(SANS_B, 24), fill=RED, anchor="ra")


def icon_flag(d, x, y, s):
    # chequered flag: the Grand Prix
    d.rounded_rectangle([x + 4, y + 4, x + s - 4, y + s - 4], radius=10,
                        fill=(243, 244, 246))
    d.line([x + 14, y + 10, x + 14, y + s - 8], fill=INK, width=4)
    bx, by = x + 16, y + 14
    cw, ch = 13, 12
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([bx + c * cw, by + r * ch,
                             bx + (c + 1) * cw, by + (r + 1) * ch],
                            fill=INK)
            else:
                d.rectangle([bx + c * cw, by + r * ch,
                             bx + (c + 1) * cw, by + (r + 1) * ch],
                            fill=(255, 255, 255), outline=INK)
    d.line([bx, by, bx + 4 * cw, by], fill=INK, width=2)
    d.line([bx, by + 4 * ch, bx + 4 * cw, by + 4 * ch], fill=INK, width=2)


def icon_controller(d, x, y, s):
    # game controller: the teen gamer
    d.rounded_rectangle([x + 4, y + 4, x + s - 4, y + s - 4], radius=10,
                        fill=(237, 233, 254))
    cx, cy = x + s // 2, y + s // 2 + 6
    d.rounded_rectangle([cx - 30, cy - 16, cx + 30, cy + 16], radius=14,
                        fill=(76, 29, 149), outline=INK, width=2)
    d.rectangle([cx - 22, cy - 4, cx - 10, cy + 4], fill=(255, 255, 255))
    d.rectangle([cx - 18, cy - 8, cx - 14, cy + 8], fill=(255, 255, 255))
    for dx, dy, col in ((16, -7, (253, 224, 71)), (22, 0, (220, 38, 38)),
                        (16, 7, (34, 139, 34)), (10, 0, (37, 99, 235))):
        d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3],
                  fill=col, outline=(255, 255, 255))
    d.text((cx, y + 8), "16", font=font(SANS_B, 20), fill=INK, anchor="ma")


def icon_bigben(d, x, y, s):
    # Big Ben: the Brexit row
    d.rounded_rectangle([x + 4, y + 4, x + s - 4, y + s - 4], radius=10,
                        fill=(254, 243, 199))
    cx = x + s // 2
    d.polygon([(cx - 12, y + 12), (cx + 12, y + 12), (cx, y + 2)],
              fill=(68, 64, 60))
    d.rectangle([cx - 12, y + 12, cx + 12, y + s - 8], fill=(120, 113, 108),
                outline=INK, width=2)
    d.ellipse([cx - 13, y + 16, cx + 13, y + 42], fill=(255, 255, 255),
              outline=INK, width=2)
    d.line([cx, y + 29, cx, y + 20], fill=INK, width=2)
    d.line([cx, y + 29, cx + 7, y + 32], fill=INK, width=2)
    for wy in range(y + 50, y + s - 12, 12):
        d.rectangle([cx - 7, wy, cx + 7, wy + 5], fill=(254, 243, 199))


ICONS = {
    "globe": icon_globe,
    "flame": icon_flame,
    "shield": icon_shield,
    "flag": icon_flag,
    "controller": icon_controller,
    "bigben": icon_bigben,
}


# ---------------- cards ----------------

def card(d, x, y, w, h, kicker, headline, summary, icon, icon_size=84):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                        outline=(200, 196, 188), width=1)
    ix, iy = x + 14, y + (h - icon_size) // 2
    ICONS[icon](d, ix, iy, icon_size)
    tx = x + 14 + icon_size + 14
    tw = x + w - 14 - tx
    cy = y + 12
    d.text((tx, cy), kicker, font=font(SANS_B, 15), fill=RED)
    cy += 24
    hl = wrap(d, headline, font(SERIF_B, 26), tw)
    cy = text_block(d, tx, cy, hl[:2], font(SERIF_B, 26), INK, 31)
    cy += 4
    sm = wrap(d, summary, font(SANS, 17), tw)
    text_block(d, tx, cy, sm[:2], font(SANS, 17), MUTED, 21)


def wide_card(d, x, y, w, h, kicker, headline, summary, icon):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                        outline=(200, 196, 188), width=1)
    ix, iy = x + 16, y + (h - 110) // 2
    ICONS[icon](d, ix, iy, 110)
    tx = x + 16 + 110 + 18
    tw = x + w - 16 - tx
    cy = y + 14
    d.text((tx, cy), kicker, font=font(SANS_B, 16), fill=RED)
    cy += 26
    hl = wrap(d, headline, font(SERIF_B, 30), tw)
    cy = text_block(d, tx, cy, hl[:2], font(SERIF_B, 30), INK, 36)
    cy += 4
    sm = wrap(d, summary, font(SANS, 19), tw)
    text_block(d, tx, cy, sm[:2], font(SANS, 19), MUTED, 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD TODAY"
    d.text((W // 2, 58), title, font=font(SERIF_B, 66), fill=INK, anchor="mm")
    d.text((W // 2, 108), "SUNDAY, 22 NOVEMBER 2026",
           font=font(SANS_B, 23), fill=RED, anchor="mm")
    d.line([28, 128, W - 28, 128], fill=INK, width=3)
    d.line([28, 134, W - 28, 134], fill=INK, width=1)

    # lead story
    lx, ly, lw, lh = 28, 144, 968, 216
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=8, fill=CARD,
                        outline=(200, 196, 188), width=1)
    d.text((48, ly + 14), "ANTALYA, TURKEY  —  CLIMATE", font=font(SANS_B, 17),
           fill=RED)
    ICONS["globe"](d, lx + lw - 176, ly + 32, 150)
    hl = wrap(d, "COP31 IN OVERTIME AS NEW DRAFT SEEKS TO SAVE TALKS",
              font(SERIF_B, 40), lw - 40 - 190)
    y = text_block(d, 48, ly + 42, hl, font(SERIF_B, 40), INK, 48)
    sm = wrap(d, "Climate talks run into a second day of overtime, split over "
                 "fossil fuels and funding for poorer nations.",
              font(SANS, 21), lw - 40 - 190)
    text_block(d, 48, y + 6, sm, font(SANS, 21), MUTED, 26)

    # grid rows
    gy, gh, gap = 372, 158, 10
    cw = 478
    card(d, 28, gy, cw, gh, "INDONESIA",
         "36 MISSING AFTER CANDY FACTORY FIRE",
         "Candy factory fire in Banten kills 3, injures 4; "
         "36 workers still missing.",
         "flame")
    card(d, 518, gy, cw, gh, "UNITED STATES",
         "FBI PROBES REPORTED HACK",
         "FBI investigates an apparent breach of the NCIC database "
         "used by police.",
         "shield")
    card(d, 28, gy + gh + gap, cw, gh, "SPORT — FORMULA 1",
         "VERSTAPPEN WINS WILD LAS VEGAS GP",
         "Norris and Piastri on the podium; Russell crashes and the "
         "Ferraris collide.",
         "flag")
    card(d, 518, gy + gh + gap, cw, gh, "UNITED STATES",
         "TEEN GAMER HELPS FBI RESCUE GIRL",
         "A 16-year-old met a girl in an online game, then helped "
         "the FBI rescue her.",
         "controller")
    wide_card(d, 28, gy + 2 * (gh + gap), 968, gh, "BRITAIN",
              "MAY 'AGHAST' AT BURNHAM'S EU PLANS",
              "The former PM tells the BBC 'Brexit is done' as Andy Burnham "
              "floats closer ties with the EU.",
              "bigben")

    # footer: also today
    fx, fy, fw, fh = 28, 878, 968, 130
    d.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=8, fill=NAVY)
    d.text((fx + 18, fy + 12), "ALSO TODAY", font=font(SANS_B, 19),
           fill=(255, 255, 255))
    items = [
        "Alcaraz v Zverev in tonight's ATP Finals decider",
        "St. Johns River flood still at record levels",
        "BBC apologises for Strictly noise disruption",
        "Kate's new documentary leads the front pages",
    ]
    fnt = font(SANS, 17)
    col_w = (fw - 36) // 2
    for i, item in enumerate(items):
        cx = fx + 18 + (i % 2) * col_w
        cy = fy + 44 + (i // 2) * 38
        d.text((cx, cy), "\u25aa  " + item, font=fnt, fill=(226, 232, 240))

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
