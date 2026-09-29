"""Generate a 1200x630 Open Graph image for Duel 2048.

Run once after cloning. Output: ./assets/og.png

    pip install Pillow
    python make_og.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------- palette (must mirror style.css :root) ----------
BG          = (14, 17, 22)
SURFACE     = (22, 27, 34)
BORDER      = (33, 38, 45)
TEXT        = (230, 237, 243)
TEXT_DIM    = (139, 148, 158)
ACCENT      = (88, 166, 255)    # you
ACCENT_2    = (188, 140, 255)   # agent
TILE_2      = (238, 228, 218)
TILE_4      = (237, 224, 200)
TILE_8      = (242, 177, 121)

W, H = 1200, 630
TILE = 70
GAP  = 10
PAD  = 60


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Try a handful of common system fonts; fall back to PIL default."""
    candidates = (
        ["segoeuib.ttf", "segoeui.ttf"] if not bold else ["segoeuib.ttf"]
    ) + [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def draw_rounded_rect(d, xy, radius, fill, border=None):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=border, width=2 if border else 0)


def draw_tile(d, x, y, value, fill, fg=(255, 255, 255)):
    draw_rounded_rect(d, (x, y, x + TILE, y + TILE), 8, fill)
    if value:
        font = load_font(36, bold=True)
        bbox = d.textbbox((0, 0), str(value), font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(
            (x + (TILE - tw) // 2, y + (TILE - th) // 2 - 4),
            str(value), fill=fg, font=font,
        )


def draw_board(d, x, y, label, badge_color, cells):
    # label badge
    font = load_font(18, bold=True)
    d.text((x, y), label, fill=badge_color, font=font)
    # board bg
    board_w = 4 * TILE + 5 * GAP
    board_h = 4 * TILE + 5 * GAP
    board_x, board_y = x, y + 32
    draw_rounded_rect(d, (board_x, board_y, board_x + board_w, board_y + board_h), 12, SURFACE, BORDER)
    # cells
    for r in range(4):
        for c in range(4):
            v = cells[r][c]
            cx = board_x + GAP + c * (TILE + GAP)
            cy = board_y + GAP + r * (TILE + GAP)
            if v == 0:
                draw_rounded_rect(d, (cx, cy, cx + TILE, cy + TILE), 8, BG)
            elif v == 2:
                draw_tile(d, cx, cy, 2, TILE_2, fg=(90, 74, 54))
            elif v == 4:
                draw_tile(d, cx, cy, 4, TILE_4, fg=(90, 74, 54))
            elif v == 8:
                draw_tile(d, cx, cy, 8, TILE_8)
            elif v == 16:
                draw_tile(d, cx, cy, 16, (245, 149, 99))
            elif v == 32:
                draw_tile(d, cx, cy, 32, (246, 124, 95))
            else:
                draw_tile(d, cx, cy, v, (237, 204, 97))


def main():
    out = Path(__file__).parent / "assets" / "og.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # subtle gradient overlay
    for y in range(H):
        a = y / H
        c = (
            int(BG[0] * (1 - 0.3 * a)),
            int(BG[1] * (1 - 0.3 * a)),
            int(BG[2] * (1 - 0.2 * a)),
        )
        d.line([(0, y), (W, y)], fill=c)

    # eyebrow pill
    f_eyebrow = load_font(18, bold=True)
    pill_text = "AI · HUMAN  ·  SAME EVENT STREAM"
    pill_w = d.textlength(pill_text, f_eyebrow) + 24
    draw_rounded_rect(d, (PAD, PAD, PAD + pill_w, PAD + 32), 16, (88, 166, 255, 30), border=ACCENT)
    d.text((PAD + 12, PAD + 7), pill_text, fill=ACCENT, font=f_eyebrow)

    # title (two lines)
    f_title = load_font(72, bold=True)
    d.text((PAD, PAD + 60), "Same board.", fill=TEXT, font=f_title)
    d.text((PAD, PAD + 138), "Different solutions.", fill=ACCENT, font=f_title)

    # subtitle
    f_sub = load_font(24)
    sub = "You and an AI Agent play 2048 on the same event stream."
    d.text((PAD, PAD + 240), sub, fill=TEXT_DIM, font=f_sub)
    sub2 = "Watch the divergence, move by move."
    d.text((PAD, PAD + 272), sub2, fill=TEXT_DIM, font=f_sub)

    # dual boards on the right
    board_x = 700
    board_y = 80
    cells_you = [
        [0, 2, 0, 0],
        [0, 0, 4, 0],
        [2, 0, 8, 0],
        [0, 16, 0, 0],
    ]
    cells_ai = [
        [0, 0, 2, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 8, 0, 16],
    ]
    draw_board(d, board_x, 70, "YOU",    ACCENT,   cells_you)
    draw_board(d, board_x + 320, 70, "AGENT", ACCENT_2, cells_ai)

    # footer / URL
    f_url = load_font(18)
    d.text((PAD, H - 50), "plain-bar-aed1.leochenliu.workers.dev", fill=TEXT, font=f_url)
    f_dim = load_font(16)
    d.text((PAD, H - 28), "Browser-only  ·  No login  ·  5 sync modes", fill=TEXT_DIM, font=f_dim)

    img.save(out, format="PNG", optimize=True)
    print(f"Wrote {out}  ({W}x{H})")


if __name__ == "__main__":
    main()