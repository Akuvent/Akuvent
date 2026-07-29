"""Generate Akuvent profile README slices from one continuous lofi canvas."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

W = 1400
CREAM = (242, 235, 228)
CREAM_DEEP = (220, 208, 196)
INK = (26, 28, 44)
INK_SOFT = (58, 60, 78)
LAVENDER = (168, 155, 176)
ROSE = (196, 164, 164)
ROSE_SOFT = (212, 190, 186)
CARD = (252, 247, 242)
CARD_EDGE = (198, 184, 174)

GAP = 100
PAD_TOP = 64
PAD_BOTTOM = 64
H_HEADER = 260
H_SKILLS = 190
H_SOCIAL = 120
H_WORKING = 230
H_FOOTER = 110

H = (
    PAD_TOP
    + H_HEADER
    + GAP
    + H_SKILLS
    + GAP
    + H_SOCIAL
    + GAP
    + H_WORKING
    + GAP
    + H_FOOTER
    + PAD_BOTTOM
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    if bold:
        for p in (r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"):
            if Path(p).exists():
                return ImageFont.truetype(p, size)
    for p in (
        r"C:\Windows\Fonts\seguisb.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def soft_serif(size: int) -> ImageFont.FreeTypeFont:
    for p in (r"C:\Windows\Fonts\constan.ttf", r"C:\Windows\Fonts\georgia.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return font(size)


def text_size(draw, text, fnt):
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def center_text(draw, xy, text, fnt, fill):
    tw, th = text_size(draw, text, fnt)
    draw.text((xy[0] - tw / 2, xy[1] - th / 2), text, font=fnt, fill=fill)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def paint_background(h: int) -> Image.Image:
    """Obvious paper/lofi background (not flat)."""
    img = Image.new("RGBA", (W, h), CREAM + (255,))
    draw = ImageDraw.Draw(img, "RGBA")

    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(CREAM[0] * (1 - t) + CREAM_DEEP[0] * t)
        g = int(CREAM[1] * (1 - t) + CREAM_DEEP[1] * t)
        b = int(CREAM[2] * (1 - t) + CREAM_DEEP[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    blobs = [
        (160, 160, 420, (*LAVENDER, 48)),
        (1240, 280, 460, (*ROSE, 52)),
        (720, 780, 380, (*ROSE_SOFT, 40)),
        (200, 1280, 340, (*LAVENDER, 44)),
        (1100, H - 160, 400, (*ROSE, 46)),
        (500, 420, 220, (255, 255, 255, 50)),
    ]
    for cx, cy, rad, col in blobs:
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col)
        img = Image.alpha_composite(img, overlay.filter(ImageFilter.GaussianBlur(90)))

    rng = random.Random(21)
    dot = ImageDraw.Draw(img, "RGBA")
    for _ in range(5200):
        x, y = rng.randrange(W), rng.randrange(h)
        rad = rng.choice((1, 1, 1, 2, 2, 3))
        col = rng.choice(
            (
                (*LAVENDER, 55),
                (*ROSE, 50),
                (120, 110, 100, 40),
                (255, 255, 255, 45),
            )
        )
        dot.ellipse([x - rad, y - rad, x + rad, y + rad], fill=col)

    px = img.load()
    for _ in range(W * h // 8):
        x, y = rng.randrange(W), rng.randrange(h)
        r, g, b, a = px[x, y]
        d = rng.randint(-22, 22)
        px[x, y] = (
            max(0, min(255, r + d)),
            max(0, min(255, g + d)),
            max(0, min(255, b + d)),
            a,
        )

    side = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(side)
    for x in range(120):
        a = int(40 * (1 - x / 120))
        sd.line([(x, 0), (x, h)], fill=(180, 160, 150, a))
        sd.line([(W - 1 - x, 0), (W - 1 - x, h)], fill=(180, 160, 150, a))
    return Image.alpha_composite(img, side)


def build() -> Image.Image:
    img = paint_background(H)
    draw = ImageDraw.Draw(img, "RGBA")
    y = PAD_TOP

    rounded(draw, (70, y, W - 70, y + H_HEADER), 36, (*CARD, 230), CARD_EDGE, 2)
    center_text(draw, (W // 2, y + 100), "akuvent", soft_serif(92), INK)
    draw.arc([W // 2 - 160, y + 136, W // 2 + 160, y + 178], 200, 340, fill=ROSE, width=3)
    center_text(
        draw,
        (W // 2, y + 195),
        "Devoting my youth to the eight gates of code.",
        font(28),
        INK_SOFT,
    )
    y += H_HEADER + GAP

    rounded(draw, (70, y, W - 70, y + H_SKILLS), 36, (*CARD, 230), CARD_EDGE, 2)
    draw.text((110, y + 28), "skills", font=font(22), fill=LAVENDER)
    chips = ["GDScript", "Python", "C#"]
    fnt = font(36, bold=True)
    chip_w, chip_h, gap = 280, 84, 28
    total = len(chips) * chip_w + (len(chips) - 1) * gap
    x = (W - total) // 2
    cy = y + 70
    for i, name in enumerate(chips):
        fill = (*ROSE_SOFT, 240) if i == 0 else (*CREAM, 235)
        outline = ROSE if i == 0 else CARD_EDGE
        rounded(draw, (x, cy, x + chip_w, cy + chip_h), 28, fill, outline, 2)
        tw, th = text_size(draw, name, fnt)
        draw.text((x + (chip_w - tw) / 2, cy + (chip_h - th) / 2 - 2), name, font=fnt, fill=INK)
        x += chip_w + gap
    y += H_SKILLS + GAP

    # YouTube / Discord / Steam — one card per equal-width tile (33/34/33)
    labels = ["YouTube", "Discord", "Steam"]
    tile_ws = (462, 476, 462)
    sf = font(28, bold=True)
    x0 = 0
    for label, tw in zip(labels, tile_ws):
        pad = 28
        rounded(
            draw,
            (x0 + pad, y, x0 + tw - pad, y + H_SOCIAL),
            28,
            (*CARD, 230),
            CARD_EDGE,
            2,
        )
        center_text(draw, (x0 + tw // 2, y + H_SOCIAL // 2), label, sf, INK)
        x0 += tw
    y += H_SOCIAL + GAP

    rounded(draw, (70, y, W - 70, y + H_WORKING), 36, (*CARD, 230), CARD_EDGE, 2)
    draw.text((110, y + 28), "currently around", font=font(22), fill=LAVENDER)
    draw.text((110, y + 78), "platformer_training", font=font(40, bold=True), fill=INK)
    draw.text(
        (110, y + 136),
        "Godot 4 · Mario-style training archive — player, enemies,",
        font=font(24),
        fill=INK_SOFT,
    )
    draw.text(
        (110, y + 168),
        "coins, checkpoints, moving platforms, SFX.",
        font=font(24),
        fill=INK_SOFT,
    )
    pill, pf = "GDScript", font(18, bold=True)
    tw, th = text_size(draw, pill, pf)
    px, py = W - 70 - tw - 56, y + 78
    rounded(draw, (px, py, px + tw + 36, py + th + 18), 18, (*ROSE_SOFT, 240), ROSE, 2)
    draw.text((px + 18, py + 8), pill, font=pf, fill=INK)
    y += H_WORKING + GAP

    rounded(draw, (70, y, W - 70, y + H_FOOTER), 36, (*CARD, 230), CARD_EDGE, 2)
    center_text(
        draw,
        (W // 2, y + H_FOOTER // 2),
        "thanks for stopping by — feel free to look around",
        font(24),
        INK_SOFT,
    )
    return img


def slice_bounds() -> dict[str, tuple[int, int]]:
    """Horizontal cut lines through mid-gaps so stacked slices stay continuous."""
    half = GAP // 2
    y = PAD_TOP + H_HEADER + half
    header = (0, y)
    y2 = y + H_SKILLS + GAP
    skills = (y, y2)
    y3 = y2 + H_SOCIAL + GAP
    social = (y2, y3)
    y4 = y3 + H_WORKING + GAP
    working = (y3, y4)
    footer = (y4, H)
    return {
        "header": header,
        "skills": skills,
        "social": social,
        "working": working,
        "footer": footer,
    }


def export_slices(master: Image.Image) -> None:
    rgb = master.convert("RGB")
    bounds = slice_bounds()

    def crop_y(name: str, y0: int, y1: int) -> Image.Image:
        return rgb.crop((0, y0, W, y1))

    crops = {
        "01_header.png": crop_y("header", *bounds["header"]),
        "02_skills.png": crop_y("skills", *bounds["skills"]),
        "04_working.png": crop_y("working", *bounds["working"]),
        "05_footer.png": crop_y("footer", *bounds["footer"]),
    }

    sy0, sy1 = bounds["social"]
    social_band = rgb.crop((0, sy0, W, sy1))
    # 33% / 34% / 33% of 1400
    x_yt, x_dc, x_st = 0, 462, 462 + 476
    crops["03a_youtube.png"] = social_band.crop((x_yt, 0, x_dc, social_band.height))
    crops["03b_discord.png"] = social_band.crop((x_dc, 0, x_st, social_band.height))
    crops["03c_steam.png"] = social_band.crop((x_st, 0, W, social_band.height))

    for old in ASSETS.iterdir():
        if old.is_file():
            old.unlink()

    for name, im in crops.items():
        path = ASSETS / name
        im.save(path, "PNG", optimize=True)
        print("wrote", path.name, im.size)


def main() -> None:
    master = build()
    export_slices(master)
    print("master", master.size)


if __name__ == "__main__":
    main()
