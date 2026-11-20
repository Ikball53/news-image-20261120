#!/usr/bin/env python3
"""The World in One Picture — 20 November 2026.

Renders a single 1024x1024 news poster with Pillow: eight illustrated
story cards on the left two-thirds and a simplified world map on the
right third carrying nothing but red location dots.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
OUT_PATH = Path(__file__).resolve().parent / "news-2026-11-20.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
REGULAR = str(FONT_DIR / "DejaVuSans.ttf")

INK = (18, 22, 38)
PAPER = (244, 241, 234)
GOLD = (201, 162, 39)
RED = (214, 40, 40)
MUTED = (110, 114, 128)

STORIES = [
    {
        "kicker": "DIPLOMACY · SHENZHEN",
        "headline": "Trump, Putin and Xi hold first-ever trilateral summit",
        "body": "Ukraine tops the agenda as the three leaders adopt a joint peace declaration on the APEC sidelines.",
        "accent": (38, 70, 160),
        "flags": ["US", "CN", "RU"],
        "icon": "summit",
        "map_xy": (0.78, 0.34),
        "source": "TASS via Stockbiz, 20 Nov",
    },
    {
        "kicker": "JUSTICE · THE HAGUE",
        "headline": "World Court: Myanmar committed genocide against Rohingya",
        "body": "A 9–6 ICJ vote establishes state responsibility for genocide in northern Rakhine.",
        "accent": (110, 60, 160),
        "flags": ["MM", "UN"],
        "icon": "scales",
        "map_xy": (0.74, 0.40),
        "source": "Le Monde, 20 Nov",
    },
    {
        "kicker": "MARKETS · NEW YORK",
        "headline": "Anthropic soars on Nasdaq debut",
        "body": "The AI firm's shares jump 17% in their first session, closing near $97 amid a record IPO.",
        "accent": (20, 130, 90),
        "flags": ["US"],
        "icon": "chart",
        "map_xy": (0.24, 0.32),
        "source": "AFP via Stockbiz, 20 Nov",
    },
    {
        "kicker": "WAR · KYIV",
        "headline": "Kyiv hit by four ballistic missiles",
        "body": "Ukraine's capital is struck in an early-morning attack as the war grinds on.",
        "accent": (180, 60, 40),
        "flags": ["UA"],
        "icon": "burst",
        "map_xy": (0.57, 0.26),
        "source": "Daily Baku, 20 Nov 04:07",
    },
    {
        "kicker": "MIDDLE EAST · RIYADH",
        "headline": "Houthis claim strikes on four Saudi targets",
        "body": "Drone and missile attacks reported across the kingdom; foreign investors warned to leave.",
        "accent": (190, 120, 30),
        "flags": ["SA", "YE"],
        "icon": "drone",
        "map_xy": (0.62, 0.40),
        "source": "TASS / News.Az, 20 Nov",
    },
    {
        "kicker": "WEATHER · BAY OF BENGAL",
        "headline": "Cyclone Akvan bears down on India's east coast",
        "body": "Odisha and Andhra Pradesh brace for landfall; trains cancelled, evacuations under way.",
        "accent": (30, 120, 170),
        "flags": ["IN"],
        "icon": "cyclone",
        "map_xy": (0.71, 0.42),
        "source": "Careerindia, 20 Nov",
    },
    {
        "kicker": "EUROPE · GENOA",
        "headline": "Genoa airport suspends flights after drone sightings",
        "body": "Unidentified drones over the airfield halt departures in northern Italy.",
        "accent": (70, 110, 90),
        "flags": ["IT"],
        "icon": "plane",
        "map_xy": (0.51, 0.28),
        "source": "Daily Baku, 20 Nov 04:22",
    },
    {
        "kicker": "ASIA · TOKYO",
        "headline": "13,000 protest in Tokyo against Takaichi government",
        "body": "Crowds march through the capital opposing the government's policies.",
        "accent": (160, 50, 90),
        "flags": ["JP"],
        "icon": "crowd",
        "map_xy": (0.84, 0.33),
        "source": "News.Az, 20 Nov",
    },
]

FLAG_PAINT = {
    "US": [(178, 34, 52), (255, 255, 255), (60, 59, 110)],
    "CN": [(222, 41, 16), (222, 41, 16), (255, 222, 0)],
    "RU": [(255, 255, 255), (0, 57, 166), (213, 43, 30)],
    "MM": [(254, 203, 0), (52, 183, 51), (234, 41, 57)],
    "UN": [(0, 149, 219), (255, 255, 255), (0, 149, 219)],
    "UA": [(0, 91, 187), (255, 213, 0), (255, 213, 0)],
    "SA": [(0, 108, 53), (0, 108, 53), (255, 255, 255)],
    "YE": [(206, 17, 38), (255, 255, 255), (0, 0, 0)],
    "IN": [(255, 153, 51), (255, 255, 255), (19, 136, 8)],
    "IT": [(0, 140, 69), (255, 255, 255), (205, 33, 42)],
    "JP": [(255, 255, 255), (188, 0, 45), (255, 255, 255)],
}


def load_font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def wrap_lines(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_flag(draw, code, x, y, w=26, h=18):
    colors = FLAG_PAINT.get(code, [(150, 150, 150)] * 3)
    band = h // 3
    for i, color in enumerate(colors):
        draw.rectangle([x, y + i * band, x + w, y + (i + 1) * band], fill=color)
    draw.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


def draw_icon(draw, kind, cx, cy, accent):
    if kind == "summit":
        draw.ellipse([cx - 16, cy - 12, cx - 2, cy + 2], fill=accent)
        draw.ellipse([cx - 7, cy - 18, cx + 7, cy - 4], fill=accent)
        draw.ellipse([cx + 2, cy - 12, cx + 16, cy + 2], fill=accent)
        draw.rectangle([cx - 20, cy + 6, cx + 20, cy + 12], fill=accent)
    elif kind == "scales":
        draw.line([cx, cy - 18, cx, cy + 14], fill=accent, width=3)
        draw.line([cx - 18, cy - 12, cx + 18, cy - 12], fill=accent, width=3)
        draw.polygon([(cx - 18, cy - 12), (cx - 24, cy + 2), (cx - 12, cy + 2)], fill=accent)
        draw.polygon([(cx + 18, cy - 12), (cx + 12, cy + 2), (cx + 24, cy + 2)], fill=accent)
        draw.rectangle([cx - 10, cy + 14, cx + 10, cy + 18], fill=accent)
    elif kind == "chart":
        pts = [(cx - 22, cy + 12), (cx - 10, cy + 2), (cx + 2, cy + 8), (cx + 18, cy - 14)]
        draw.line(pts, fill=accent, width=4)
        draw.polygon([(cx + 18, cy - 14), (cx + 8, cy - 12), (cx + 16, cy - 4)], fill=accent)
    elif kind == "burst":
        for dx, dy in [(-18, -14), (0, -20), (18, -14), (-22, 4), (22, 4), (-12, 16), (12, 16)]:
            draw.line([cx, cy, cx + dx, cy + dy], fill=accent, width=4)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=accent)
    elif kind == "drone":
        draw.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=accent)
        for dx, dy in [(-20, -14), (20, -14), (-20, 14), (20, 14)]:
            draw.line([cx, cy, cx + dx, cy + dy], fill=accent, width=3)
            draw.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], outline=accent, width=2)
    elif kind == "cyclone":
        for r in (20, 13, 6):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=30, end=320, fill=accent, width=4)
    elif kind == "plane":
        draw.polygon(
            [(cx - 22, cy + 4), (cx + 16, cy - 10), (cx + 24, cy - 6), (cx - 6, cy + 8)],
            fill=accent,
        )
        draw.polygon([(cx - 4, cy + 6), (cx - 14, cy + 18), (cx - 6, cy + 18)], fill=accent)
    elif kind == "crowd":
        for dx in (-18, 0, 18):
            draw.ellipse([cx + dx - 6, cy - 16, cx + dx + 6, cy - 4], fill=accent)
            draw.rectangle([cx + dx - 7, cy - 2, cx + dx + 7, cy + 16], fill=accent)


def draw_card(draw, story, x, y, w, h):
    accent = story["accent"]
    # soft drop shadow for a polished, printed-poster feel
    draw.rounded_rectangle([x + 3, y + 4, x + w + 3, y + h + 4], radius=10, fill=(214, 208, 194))
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(255, 255, 255), outline=(210, 205, 195), width=1)
    # faint accent wash behind the icon medallion
    draw.ellipse([x + 8, y + 26, x + 60, y + 78], fill=tuple(min(255, c + 170) for c in accent))
    draw.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=accent)
    draw_icon(draw, story["icon"], x + 34, y + 52, accent)

    fx = x + w - 34
    for code in reversed(story["flags"]):
        draw_flag(draw, code, fx, y + 18)
        fx -= 30

    kicker_font = load_font(11, bold=True)
    draw.text((x + 66, y + 16), story["kicker"], font=kicker_font, fill=accent)

    head_font = load_font(16, bold=True)
    head_lines = wrap_lines(draw, story["headline"], head_font, w - 78)[:3]
    hy = y + 34
    for line in head_lines:
        draw.text((x + 66, hy), line, font=head_font, fill=INK)
        hy += 19

    body_font = load_font(12)
    body_lines = wrap_lines(draw, story["body"], body_font, w - 24)[:3]
    by = hy + 6
    for line in body_lines:
        draw.text((x + 12, by), line, font=body_font, fill=(70, 74, 88))
        by += 15

    src_font = load_font(9)
    draw.text((x + 12, y + h - 14), story["source"], font=src_font, fill=MUTED)


def draw_world_map(draw, x, y, w, h):
    """Simplified continent silhouettes + red dots only."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(226, 236, 245), outline=(180, 198, 214), width=1)
    land = (150, 176, 140)

    def poly(points):
        draw.polygon([(x + px * w, y + py * h) for px, py in points], fill=land)

    poly([(0.06, 0.22), (0.30, 0.16), (0.34, 0.30), (0.26, 0.44), (0.14, 0.42), (0.08, 0.34)])  # N America
    poly([(0.20, 0.50), (0.30, 0.50), (0.32, 0.66), (0.25, 0.84), (0.20, 0.68)])  # S America
    poly([(0.45, 0.20), (0.58, 0.16), (0.60, 0.30), (0.50, 0.34), (0.45, 0.28)])  # Europe
    poly([(0.47, 0.38), (0.62, 0.36), (0.64, 0.58), (0.56, 0.78), (0.49, 0.62)])  # Africa
    poly([(0.60, 0.16), (0.92, 0.14), (0.95, 0.34), (0.84, 0.46), (0.68, 0.44), (0.60, 0.30)])  # Asia
    poly([(0.78, 0.58), (0.92, 0.58), (0.90, 0.72), (0.80, 0.70)])  # Australia

    for story in STORIES:
        mx, my = story["map_xy"]
        px, py = x + mx * w, y + my * h
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=2)

    label = load_font(11, bold=True)
    draw.text((x + 12, y + h - 24), "STORY LOCATIONS", font=label, fill=(70, 90, 110))


def build_poster():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, CANVAS_W, 108], fill=INK)
    draw.rectangle([0, 108, CANVAS_W, 114], fill=GOLD)
    title_font = load_font(34, bold=True)
    draw.text((32, 22), "THE WORLD IN ONE PICTURE", font=title_font, fill=(255, 255, 255))
    sub_font = load_font(17, bold=True)
    draw.text((32, 66), "Friday · 20 November 2026 · eight stories that shaped the day", font=sub_font, fill=GOLD)

    margin = 24
    map_w = 320
    cards_x = margin
    cards_w = CANVAS_W - map_w - margin * 3
    top = 140
    card_h = 196
    gap = 14
    col_w = (cards_w - gap) // 2

    for idx, story in enumerate(STORIES):
        row, col = divmod(idx, 2)
        cx = cards_x + col * (col_w + gap)
        cy = top + row * (card_h + gap)
        draw_card(draw, story, cx, cy, col_w, card_h)

    map_x = CANVAS_W - margin - map_w
    map_y = top
    map_h = 4 * card_h + 3 * gap
    draw_world_map(draw, map_x, map_y, map_w, map_h)

    foot_font = load_font(11)
    draw.text(
        (margin, CANVAS_H - 30),
        "Sources verified 20 Nov 2026: TASS, AFP, Le Monde, News.Az, Daily Baku, Careerindia.",
        font=foot_font,
        fill=MUTED,
    )

    img.save(OUT_PATH, "PNG")
    print(f"saved {OUT_PATH} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    build_poster()
