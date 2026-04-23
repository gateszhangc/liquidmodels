from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "brand"
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {
    "ink": (6, 17, 13, 255),
    "panel": (12, 33, 25, 255),
    "paper": (246, 248, 239, 255),
    "green": (25, 195, 125, 255),
    "blue": (72, 185, 255, 255),
    "coral": (255, 107, 74, 255),
    "chartreuse": (228, 210, 91, 255),
    "muted": (141, 166, 151, 255),
}


def font(size, weight="regular"):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if weight == "bold" else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if weight == "bold" else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def cubic(p0, p1, p2, p3, steps=80):
    points = []
    for index in range(steps + 1):
        t = index / steps
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points


def draw_grid(draw, size, spacing, color):
    width, height = size
    for x in range(0, width + spacing, spacing):
        draw.line([(x, 0), (x, height)], fill=color, width=1)
    for y in range(0, height + spacing, spacing):
        draw.line([(0, y), (width, y)], fill=color, width=1)


def draw_grid_box(draw, box, spacing, color):
    x0, y0, x1, y1 = box
    x = x0
    while x <= x1:
        draw.line([(x, y0), (x, y1)], fill=color, width=1)
        x += spacing
    y = y0
    while y <= y1:
        draw.line([(x0, y), (x1, y)], fill=color, width=1)
        y += spacing


def draw_mark(draw, box, stroke_scale=1.0):
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    cx = x0 + w / 2
    cy = y0 + h / 2

    draw.rounded_rectangle(box, radius=int(w * 0.18), fill=COLORS["ink"], outline=(25, 195, 125, 130), width=max(2, int(5 * stroke_scale)))
    draw_grid_box(draw, box, max(12, int(w / 8)), (246, 248, 239, 18))

    waves = [
        (COLORS["green"], 9, -0.18),
        (COLORS["blue"], 6, 0.02),
        (COLORS["coral"], 5, 0.19),
        (COLORS["chartreuse"], 3, 0.31),
    ]
    for color, width, offset in waves:
        points = cubic(
            (x0 + w * 0.18, cy + h * offset),
            (x0 + w * 0.38, y0 + h * (0.05 + offset)),
            (x0 + w * 0.57, y1 - h * (0.03 - offset)),
            (x0 + w * 0.82, cy + h * (0.02 - offset)),
            120,
        )
        draw.line(points, fill=color, width=max(2, int(width * stroke_scale)), joint="curve")

    for index, angle in enumerate([0.35, 1.5, 2.5, 3.55, 4.75, 5.7]):
        radius = w * (0.27 + 0.03 * (index % 2))
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        fill = [COLORS["green"], COLORS["blue"], COLORS["coral"]][index % 3]
        draw.ellipse((x - w * 0.025, y - w * 0.025, x + w * 0.025, y + w * 0.025), fill=fill)


def save_mark():
    image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_mark(draw, (32, 32, 480, 480), 1.5)
    image.save(OUT / "logo-mark.png")

    favicon = Image.new("RGBA", (256, 256), COLORS["ink"])
    draw = ImageDraw.Draw(favicon)
    draw_mark(draw, (16, 16, 240, 240), 0.9)
    favicon.save(OUT / "favicon.png")

    touch = Image.new("RGBA", (180, 180), COLORS["ink"])
    draw = ImageDraw.Draw(touch)
    draw_mark(draw, (14, 14, 166, 166), 0.7)
    touch.save(OUT / "apple-touch-icon.png")


def save_wordmark():
    image = Image.new("RGBA", (1500, 420), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_mark(draw, (34, 54, 346, 366), 1.0)
    draw.text((400, 98), "Liquid", font=font(128, "bold"), fill=COLORS["paper"])
    draw.text((400, 214), "Models", font=font(128, "bold"), fill=COLORS["green"])
    draw.line((408, 350, 1060, 350), fill=(25, 195, 125, 180), width=3)
    draw.text((1084, 326), "edge / cloud / hybrid", font=font(34), fill=COLORS["muted"])
    image.save(OUT / "logo-wordmark.png")


def save_social_card():
    width, height = 1200, 630
    image = Image.new("RGBA", (width, height), COLORS["ink"])
    draw = ImageDraw.Draw(image)
    draw_grid(draw, (width, height), 48, (246, 248, 239, 15))

    for y, color, line_width, phase in [
        (190, COLORS["green"], 13, 0.0),
        (260, COLORS["blue"], 8, 0.8),
        (335, COLORS["coral"], 7, 1.7),
        (415, COLORS["chartreuse"], 5, 2.5),
    ]:
        points = []
        for x in range(-40, width + 80, 8):
            wave = math.sin(x / 82 + phase) * 42 + math.sin(x / 157 + phase) * 22
            points.append((x, y + wave))
        draw.line(points, fill=color, width=line_width, joint="curve")

    for x in range(92, 1100, 94):
        for y in range(88, 542, 76):
            if (x + y) % 3 == 0:
                draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(246, 248, 239, 70))

    draw.rounded_rectangle((68, 70, 1132, 560), radius=8, outline=(246, 248, 239, 55), width=1)
    draw.text((96, 102), "LIQUID MODELS", font=font(34, "bold"), fill=COLORS["green"])
    draw.text((92, 202), "Efficient AI", font=font(94, "bold"), fill=COLORS["paper"])
    draw.text((92, 305), "models that", font=font(94, "bold"), fill=COLORS["paper"])
    draw.text((92, 408), "run anywhere", font=font(94, "bold"), fill=COLORS["paper"])

    labels = [("TEXT", COLORS["green"]), ("VISION", COLORS["blue"]), ("AUDIO", COLORS["coral"]), ("NANO", COLORS["chartreuse"])]
    for index, (label, color) in enumerate(labels):
        x = 764 + (index % 2) * 168
        y = 192 + (index // 2) * 118
        draw.rounded_rectangle((x, y, x + 124, y + 48), radius=8, fill=(12, 33, 25, 230), outline=color, width=2)
        draw.text((x + 20, y + 13), label, font=font(22, "bold"), fill=color)

    draw.text((764, 468), "edge / cloud / hybrid", font=font(34), fill=COLORS["muted"])
    image.convert("RGB").save(OUT / "social-card.png", quality=95)


if __name__ == "__main__":
    save_mark()
    save_wordmark()
    save_social_card()
