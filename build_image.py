#!/usr/bin/env python3
"""Deterministic builder for the news-image-20261121 entry image.

Draws a one-page newspaper front page summarising verified world news of
Saturday 21 November 2026. No randomness, no network, no timestamps in the
output: running this script twice produces byte-identical files.

Output: entry.png (JPEG bytes inside a .png name, as the kit allows).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SEED = 20261121  # fixed; no randomness is actually used

# --- palette ---
PAPER = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (18, 35, 63)
NAVY2 = (28, 52, 88)
GOLD = (201, 162, 39)
GOLD_LT = (226, 196, 94)
RED = (179, 38, 30)
TEAL = (14, 110, 107)
DARKRED = (140, 30, 30)
AMBER = (176, 112, 16)
BROWN = (122, 79, 40)
GREEN = (32, 120, 66)
WHITE = (255, 255, 255)
CARD = (255, 253, 247)
GREY = (90, 90, 86)
LINE = (200, 192, 170)

FONT_DIR = "/usr/share/fonts/truetype/"
SERIF_B = FONT_DIR + "dejavu/DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "dejavu/DejaVuSerif.ttf"
SANS_B = FONT_DIR + "dejavu/DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_star(draw, cx, cy, r, color, rot=-math.pi / 2):
    pts = []
    for i in range(10):
        ang = rot + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.382
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)


def flag_usa(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=(178, 34, 52))
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            sx = x + cw * (c + 0.5) / 6
            sy = y + ch * (r + 0.5) / 5
            draw.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=WHITE)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw_star(draw, x + w * 0.22, y + h * 0.28, h * 0.17, (255, 222, 0))
    for sx, sy in [(0.42, 0.12), (0.50, 0.25), (0.50, 0.42), (0.42, 0.52)]:
        draw_star(draw, x + w * sx, y + h * sy, h * 0.06, (255, 222, 0))


def flag_russia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


# ---------------------------------------------------------------- icons ---
def icon_ukraine(draw, x, y, s):
    # night sky, skyline, missile arcs, explosions
    draw.rectangle([x, y, x + s, y + s], fill=(24, 32, 52))
    draw.rectangle([x, y + s * 0.72, x + s, y + s], fill=(12, 16, 28))
    for bx, bw, bh in [(0.05, 0.16, 0.28), (0.26, 0.14, 0.38),
                       (0.45, 0.18, 0.24), (0.68, 0.13, 0.34),
                       (0.85, 0.12, 0.22)]:
        draw.rectangle([x + s * bx, y + s * (1 - bh), x + s * (bx + bw),
                        y + s], fill=(52, 60, 80))
    for ex, ey, r in [(0.22, 0.30, 0.13), (0.72, 0.22, 0.16)]:
        draw_star(draw, x + s * ex, y + s * ey, s * r, (255, 176, 32))
        draw_star(draw, x + s * ex, y + s * ey, s * r * 0.55, (255, 90, 30))
    draw.arc([x + s * 0.05, y + s * 0.05, x + s * 0.95, y + s * 0.85],
             start=200, end=330, fill=(255, 220, 120), width=3)
    draw.ellipse([x + s * 0.80, y + s * 0.10, x + s * 0.86, y + s * 0.16],
                 fill=(255, 220, 120))


def icon_justice(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(232, 243, 241))
    cx, top = x + s * 0.5, y + s * 0.12
    draw.line([cx, top, cx, y + s * 0.82], fill=TEAL, width=4)
    draw.line([x + s * 0.16, top + s * 0.08, x + s * 0.84, top + s * 0.08],
              fill=TEAL, width=4)
    draw.ellipse([cx - 4, top - 4, cx + 4, top + 4], fill=GOLD)
    for px in (0.16, 0.84):
        px = x + s * px
        py = top + s * 0.08
        draw.line([px, py, px - s * 0.11, py + s * 0.30], fill=TEAL, width=3)
        draw.line([px, py, px + s * 0.11, py + s * 0.30], fill=TEAL, width=3)
        draw.arc([px - s * 0.11, py + s * 0.22, px + s * 0.11, py + s * 0.44],
                 start=0, end=180, fill=TEAL, width=3)
    draw.rectangle([cx - s * 0.16, y + s * 0.82, cx + s * 0.16, y + s * 0.88],
                   fill=TEAL)


def icon_markets(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 238, 236))
    for i in range(1, 4):
        gy = y + s * i / 4
        draw.line([x + 4, gy, x + s - 4, gy], fill=(230, 200, 196), width=1)
    pts = [(0.08, 0.22), (0.26, 0.30), (0.38, 0.26), (0.55, 0.52),
           (0.68, 0.48), (0.92, 0.80)]
    pts = [(x + s * px, y + s * py) for px, py in pts]
    draw.line(pts, fill=DARKRED, width=5, joint="curve")
    ax, ay = pts[-1]
    draw.polygon([(ax, ay + 10), (ax - 11, ay - 4), (ax + 2, ay - 8)],
                 fill=DARKRED)


def icon_riyadh(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 243, 224))
    cx, cy = x + s * 0.5, y + s * 0.52
    draw.polygon([(cx, y + s * 0.10), (x + s * 0.86, y + s * 0.24),
                  (x + s * 0.86, y + s * 0.52), (cx, y + s * 0.90),
                  (x + s * 0.14, y + s * 0.52), (x + s * 0.14, y + s * 0.24)],
                 fill=AMBER)
    draw.polygon([(cx, y + s * 0.18), (x + s * 0.78, y + s * 0.29),
                  (x + s * 0.78, y + s * 0.51), (cx, y + s * 0.80),
                  (x + s * 0.22, y + s * 0.51), (x + s * 0.22, y + s * 0.29)],
                 fill=(250, 243, 224))
    draw.line([x + s * 0.36, cy, x + s * 0.47, cy + s * 0.12], fill=GREEN,
              width=6)
    draw.line([x + s * 0.47, cy + s * 0.12, x + s * 0.66, cy - s * 0.12],
              fill=GREEN, width=6)
    for mx, my in [(0.10, 0.14), (0.90, 0.10)]:
        draw.line([x + s * mx, y + s * my, x + s * (mx + 0.06),
                   y + s * (my + 0.10)], fill=RED, width=3)


def icon_quake(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(243, 236, 224))
    draw.polygon([(x, y + s), (x + s * 0.25, y + s * 0.30),
                  (x + s * 0.45, y + s * 0.62), (x + s * 0.65, y + s * 0.22),
                  (x + s, y + s * 0.70), (x + s, y + s)], fill=BROWN)
    draw.polygon([(x + s * 0.25, y + s * 0.30), (x + s * 0.32, y + s * 0.44),
                  (x + s * 0.18, y + s * 0.44)], fill=WHITE)
    draw.polygon([(x + s * 0.65, y + s * 0.22), (x + s * 0.72, y + s * 0.38),
                  (x + s * 0.58, y + s * 0.38)], fill=WHITE)
    pts = [(0.06, 0.52), (0.20, 0.52), (0.28, 0.30), (0.38, 0.72),
           (0.48, 0.38), (0.58, 0.62), (0.68, 0.48), (0.80, 0.52),
           (0.94, 0.52)]
    pts = [(x + s * px, y + s * py) for px, py in pts]
    draw.line(pts, fill=RED, width=4, joint="curve")


def icon_health(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(232, 245, 234))
    # horizontal capsule: left half green, right half white
    cx, cy = x + s * 0.46, y + s * 0.54
    r = s * 0.19
    hw = s * 0.30
    draw.rounded_rectangle([cx - hw, cy - r, cx + hw, cy + r], radius=r,
                           fill=WHITE, outline=GREEN, width=3)
    draw.rounded_rectangle([cx - hw, cy - r, cx, cy + r], radius=r,
                           fill=GREEN)
    draw.rectangle([cx - r, cy - r, cx, cy + r], fill=GREEN)
    draw.line([cx, cy - r, cx, cy + r], fill=GREEN, width=3)
    # plus sign
    px, py = x + s * 0.80, y + s * 0.18
    draw.line([px - 8, py, px + 8, py], fill=GREEN, width=5)
    draw.line([px, py - 8, px, py + 8], fill=GREEN, width=5)


ICONS = {
    "ukraine": icon_ukraine,
    "justice": icon_justice,
    "markets": icon_markets,
    "riyadh": icon_riyadh,
    "quake": icon_quake,
    "health": icon_health,
}

CARDS = [
    ("ukraine", "UKRAINE · WAR", RED,
     "Russia's biggest strikes of 2026",
     "400+ drones and 110+ missiles hit Ukraine; 8+ killed in Kyiv. "
     "Missiles land in Poland \u2014 Warsaw calls it a \u201cprovocation\u201d."),
    ("justice", "THE HAGUE · JUSTICE", TEAL,
     "Myanmar guilty of genocide",
     "The World Court rules Myanmar committed genocide against the "
     "Rohingya \u2014 the first time it has held a state responsible."),
    ("markets", "WALL STREET · MARKETS", DARKRED,
     "AI rout drags S&P 500 into correction",
     "Nasdaq wipes out all its 2026 gains in tech's worst week since "
     "Covid; Anthropic slides after its IPO debut."),
    ("riyadh", "RIYADH · GULF", AMBER,
     "Three Houthi missiles downed over Riyadh",
     "The Saudi-led coalition intercepts missiles for a third night "
     "running, as the Houthis threaten ports and a power station."),
    ("quake", "PERU · EARTHQUAKE", BROWN,
     "Magnitude 6.8 quake shakes central Peru",
     "The quake strikes the Jun\u00edn region in the Andes; tremors are "
     "felt in Lima, about 320 km away."),
    ("health", "LONDON · HEALTH", GREEN,
     "Pill makes pancreatic tumours vanish",
     "Trial drug daraxonrasib leaves cancer undetectable on scans in "
     "one in 12 patients."),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ================= masthead =================
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    f_title = font(SERIF_B, 50)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 12), title,
           font=f_title, fill=WHITE)
    f_date = font(SANS_B, 25)
    date = "SATURDAY  \u00b7  21 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 72), date,
           font=f_date, fill=GOLD_LT)
    d.text((24, 78), "WORLD NEWS", font=font(SANS_B, 15), fill=(150, 170, 205))
    tag = "ONE IMAGE \u00b7 SIX STORIES"
    d.text((W - 24 - d.textlength(tag, font=font(SANS_B, 15)), 78), tag,
           font=font(SANS_B, 15), fill=(150, 170, 205))

    # ================= lead story =================
    d.rectangle([24, 136, 1000, 392], fill=CARD, outline=LINE, width=2)
    d.rectangle([24, 136, 30, 392], fill=RED)
    d.text((48, 152), "SHENZHEN, CHINA  \u00b7  DIPLOMACY",
           font=font(SANS_B, 16), fill=RED)
    f_head = font(SERIF_B, 37)
    head = "Trump, Xi and Putin wrap historic three-way summit"
    lines = wrap(d, head, f_head, 560)
    yy = 180
    for ln in lines:
        d.text((48, yy), ln, font=f_head, fill=INK)
        yy += 46
    f_body = font(SANS, 18)
    body = ("The three leaders issue a joint declaration pledging UN reform, "
            "bigger oil supplies and talks to cut nuclear risk. Trump calls "
            "Putin a \u201cfriend\u201d; Zelenskyy answers: \u201ckiller\u201d.")
    lines = wrap(d, body, f_body, 560)
    yy += 8
    for ln in lines:
        d.text((48, yy), ln, font=f_body, fill=(60, 60, 58))
        yy += 25

    # lead illustration: three flags + skyline
    ix, iy = 648, 156
    fw, fh = 100, 66
    gap = 12
    flag_usa(d, ix, iy, fw, fh)
    flag_china(d, ix + fw + gap, iy, fw, fh)
    flag_russia(d, ix + 2 * (fw + gap), iy, fw, fh)
    for i in range(3):
        d.rectangle([ix + i * (fw + gap), iy, ix + i * (fw + gap) + fw,
                     iy + fh], outline=LINE, width=1)
    f_flag = font(SANS_B, 15)
    for i, name in enumerate(["USA", "CHINA", "RUSSIA"]):
        cx = ix + i * (fw + gap) + fw / 2
        d.text((cx - d.textlength(name, font=f_flag) / 2, iy + fh + 8),
               name, font=f_flag, fill=INK)
    # skyline silhouette
    sy = iy + fh + 44
    d.rectangle([ix, sy + 44, ix + 3 * fw + 2 * gap, sy + 96], fill=NAVY2)
    skyline = [(0, 52, 30), (36, 30, 26), (68, 62, 34), (108, 40, 28),
               (142, 66, 30), (178, 34, 26), (210, 56, 32), (248, 44, 28),
               (282, 60, 30), (316, 36, 8)]
    for bx, bh, bw in skyline:
        d.rectangle([ix + bx, sy + 96 - bh, ix + bx + bw, sy + 96],
                    fill=NAVY)
    for wx in range(ix + 8, ix + 320, 22):
        for wy in range(sy + 52, sy + 92, 12):
            d.rectangle([wx, wy, wx + 4, wy + 5], fill=GOLD_LT)
    d.rectangle([ix, sy + 96, ix + 3 * fw + 2 * gap, sy + 100], fill=GOLD)
    rib = "JOINT DECLARATION SIGNED"
    d.text((ix + (3 * fw + 2 * gap - d.textlength(rib, font=font(SANS_B, 14))) / 2,
            sy + 108), rib, font=font(SANS_B, 14), fill=NAVY)

    # ================= story cards =================
    cw, ch = 320, 246
    xs = [24, 352, 680]
    ys = [408, 666]
    for i, (key, kicker, accent, headline, body) in enumerate(CARDS):
        x, y = xs[i % 3], ys[i // 3]
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=LINE, width=2)
        d.rectangle([x, y, x + cw, y + 6], fill=accent)
        ICONS[key](d, x + 16, y + 20, 64)
        d.text((x + 96, y + 24), kicker, font=font(SANS_B, 13), fill=accent)
        f_ch = font(SERIF_B, 21)
        lines = wrap(d, headline, f_ch, cw - 32)
        yy = y + 96
        for ln in lines[:3]:
            d.text((x + 16, yy), ln, font=f_ch, fill=INK)
            yy += 27
        f_cb = font(SANS, 15)
        lines = wrap(d, body, f_cb, cw - 32)
        yy += 4
        for ln in lines[:4]:
            d.text((x + 16, yy), ln, font=f_cb, fill=(60, 60, 58))
            yy += 21

    # ================= footer =================
    d.rectangle([0, 928, W, H], fill=NAVY)
    d.rectangle([0, 928, W, 931], fill=GOLD)
    f_f2 = font(SANS, 15)
    foot_lines = []
    line1 = ("ALSO TODAY \u2014 UK and EU strike a landmark post-Brexit deal: "
             "food trade, emissions trading and youth mobility for 100,000 "
             "young Britons.")
    line2 = ("Cyclone Akvan crosses India's Odisha coast  \u00b7  Israel's "
             "president asks Eisenkot to form a government, bypassing Netanyahu.")
    foot_lines += wrap(d, line1, f_f2, W - 48)
    foot_lines += wrap(d, line2, f_f2, W - 48)
    yy = 938
    for ln in foot_lines:
        d.text((24, yy), ln, font=f_f2, fill=WHITE)
        yy += 21
    src = ("Sources: AP  \u00b7  BBC News  \u00b7  Al Jazeera  \u00b7  Financial Times  "
           "\u00b7  The Guardian  \u00b7  Reuters      News verified 21 Nov 2026, "
           "13:15 WIB")
    d.text((24, 1002), src, font=font(SANS, 12), fill=GOLD_LT)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    # JPEG bytes in a .png name (allowed by the kit); deterministic encoder.
    img.save(out, format="JPEG", quality=90, optimize=True, progressive=False)
    print(out)
