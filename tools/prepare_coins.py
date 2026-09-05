#!/usr/bin/env python3
"""
Turn raw generated coin images into the transparent PNGs the site wants.

Image models in a chat window hand back a coin sitting on a flat background,
usually white, at whatever size they feel like. The site needs a transparent
square PNG with the coin centred and filling most of the frame — and, for the
two holed currencies, the centre hole punched through as well.

    python3 tools/prepare_coins.py raw/ --out coins/

Files are matched to countries by name: any file whose name contains "jordan"
becomes coins/jordan.png, and so on. Anything unmatched is reported and left
alone. Use --map to place a file explicitly:

    python3 tools/prepare_coins.py raw/ --map raw/image_04.png=denmark

The background is found by flood-filling inward from the four corners, so it
has to be flat — a gradient or a drop shadow will leave a halo. Papua New
Guinea and Denmark also get a second fill from the centre, which is what opens
their hole. Pass --no-hole NAME to turn that off for one coin.
"""

import argparse
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFilter

# The six coins, and which of them are struck with a hole through the middle.
COUNTRIES = {
    "jordan": False,
    "philippines": False,
    "papua-new-guinea": True,
    "thailand": False,
    "germany": False,
    "denmark": True,
}

# Words that identify a country in a filename, beyond the country name itself.
ALIASES = {
    "papua-new-guinea": ["papua", "guinea", "png-coin", "kina"],
    "jordan": ["jordan", "dinar"],
    "philippines": ["philippines", "piso", "peso"],
    "thailand": ["thailand", "baht"],
    "germany": ["germany", "euro", "deutsch"],
    "denmark": ["denmark", "krone", "danmark"],
}

SENTINEL = (255, 0, 255)   # a colour no coin will contain
OUT_SIZE = 1024            # final square, px
COIN_FILL = 0.92           # how much of the frame the coin spans


def match_country(path):
    stem = path.stem.lower().replace("_", "-").replace(" ", "-")
    for country, words in ALIASES.items():
        if any(w in stem for w in words):
            return country
    return None


def is_close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a[:3], b[:3]))


def cut_background(im, tol, hole):
    """Flood-fill the flat background away and return an alpha mask."""
    work = im.convert("RGB")
    w, h = work.size
    px = work.load()

    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    bg = px[0, 0]
    filled = False
    for seed in corners:
        if is_close(px[seed], bg, tol):
            ImageDraw.floodfill(work, seed, SENTINEL, thresh=tol)
            filled = True
    if not filled:
        raise SystemExit("The corners are not a flat background — is this the right file?")

    # The hole is enclosed by the coin, so the corner fills never reach it.
    if hole:
        cx, cy = w // 2, h // 2
        if px[cx, cy] != SENTINEL and is_close(px[cx, cy], bg, tol):
            ImageDraw.floodfill(work, (cx, cy), SENTINEL, thresh=tol)

    mask = Image.new("L", (w, h), 255)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == SENTINEL:
                mp[x, y] = 0

    # Pull the edge in by a pixel to drop the anti-aliased fringe that still
    # carries the old background colour, then soften what is left.
    mask = mask.filter(ImageFilter.MinFilter(3))
    mask = mask.filter(ImageFilter.GaussianBlur(0.7))
    return mask


def square_up(im, mask):
    """Crop to the coin, centre it in a square, scale it to fill the frame."""
    box = mask.getbbox()
    if not box:
        raise SystemExit("Nothing left after cutting the background out.")

    im = im.convert("RGBA")
    im.putalpha(mask)
    coin = im.crop(box)

    side = max(coin.size)
    target = int(OUT_SIZE * COIN_FILL)
    scale = target / side
    coin = coin.resize(
        (max(1, round(coin.width * scale)), max(1, round(coin.height * scale))),
        Image.LANCZOS,
    )

    out = Image.new("RGBA", (OUT_SIZE, OUT_SIZE), (0, 0, 0, 0))
    out.paste(coin, ((OUT_SIZE - coin.width) // 2, (OUT_SIZE - coin.height) // 2), coin)
    return out


def main():
    ap = argparse.ArgumentParser(description="Prepare coin PNGs for the RSVP page.")
    ap.add_argument("src", help="folder of raw images, or a single image file")
    ap.add_argument("--out", default="coins", help="where the finished PNGs go")
    ap.add_argument("--tol", type=int, default=32,
                    help="how far a pixel may stray from the corner colour and still "
                         "count as background (default 32; raise it for a slightly "
                         "uneven background, lower it if the coin loses its edge)")
    ap.add_argument("--map", action="append", default=[],
                    help="place a file explicitly, as path=country")
    ap.add_argument("--no-hole", action="append", default=[],
                    help="skip the centre punch for this country")
    args = ap.parse_args()

    src = pathlib.Path(args.src)
    files = [src] if src.is_file() else sorted(
        p for p in src.iterdir()
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    if not files:
        raise SystemExit("No images found in " + str(src))

    explicit = {}
    for pair in args.map:
        path, _, country = pair.partition("=")
        if country not in COUNTRIES:
            raise SystemExit("Unknown country in --map: " + country)
        explicit[pathlib.Path(path).name] = country

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    done, skipped = [], []
    for path in files:
        country = explicit.get(path.name) or match_country(path)
        if not country:
            skipped.append(path.name)
            continue

        hole = COUNTRIES[country] and country not in args.no_hole
        im = Image.open(path)
        mask = cut_background(im, args.tol, hole)
        out = square_up(im, mask)

        dest = out_dir / (country + ".png")
        out.save(dest, "PNG", optimize=True)
        done.append((country, dest, dest.stat().st_size // 1024, hole))

    for country, dest, kb, hole in done:
        print("  {:<18} {}  ({} KB{})".format(
            country, dest, kb, ", hole punched" if hole else ""))

    if skipped:
        print("\nCouldn't tell which coin these are — rename them, or use --map:")
        for name in skipped:
            print("  " + name)

    missing = [c for c in COUNTRIES if c not in {d[0] for d in done}]
    if missing:
        print("\nStill to come: " + ", ".join(missing))

    if not done:
        sys.exit(1)


if __name__ == "__main__":
    main()
