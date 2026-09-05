#!/usr/bin/env python3
"""
Turn raw generated coin images into the transparent PNGs the site wants.

Image models in a chat window hand back a coin sitting on a flat background,
usually white, at whatever size they feel like. The site needs a transparent
square PNG with the coin centred and filling most of the frame — and, for the
two holed currencies, the centre hole punched through as well.

    python3 tools/prepare_coins.py raw/ --out coins/

Filenames do not matter. Every pair among the six coins differs by something
measurable, so each image says which country it is: a hole through the middle
means Papua New Guinea or Denmark (the darker one is PNG), two metals means
Thailand or Germany (gold core is Thailand), and one metal with no hole means
Jordan or Philippines (gold is Jordan). A batch settles its own pairs, so six
files called "ChatGPT Image ….png" sort themselves out.

A country in the filename still wins if it is there, and --map beats both:

    python3 tools/prepare_coins.py raw/ --map "raw/image 4.png=denmark"
    python3 tools/prepare_coins.py raw/ --by-name    # ignore the images

The background is found by flood-filling inward from the four corners, so it
has to be flat — a gradient or a drop shadow will leave a halo. Raise --tol for
a slightly uneven background. The hole is a second fill from the centre, and
whether one opens is exactly what identifies a holed coin.
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
    """Flood-fill the flat background away.

    Returns (mask, hole_area). `hole` may be None, meaning "punch the centre
    if there is a centre to punch" — which is also how a holed coin gets
    recognised in the first place.
    """
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

    outer = sum(1 for y in range(h) for x in range(w) if px[x, y] == SENTINEL)

    # The hole is enclosed by the coin, so the corner fills never reach it.
    hole_area = 0
    if hole is not False:
        cx, cy = w // 2, h // 2
        if px[cx, cy] != SENTINEL and is_close(px[cx, cy], bg, tol):
            ImageDraw.floodfill(work, (cx, cy), SENTINEL, thresh=tol)
            hole_area = sum(1 for y in range(h) for x in range(w)
                            if px[x, y] == SENTINEL) - outer

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
    return mask, hole_area


# ── Reading the coin off the coin ────────────────────────────────────────
# Every pair among these six differs by something measurable, so a file called
# "ChatGPT Image Sep 5, 2026, 03_39_06 PM.png" can still identify itself:
#
#   a hole through the middle → Papua New Guinea or Denmark (darker = PNG)
#   two metals                → Thailand or Germany (gold core = Thailand)
#   one metal, no hole        → Jordan or Philippines (gold = Jordan)

def ring_of(im, mask, r_lo, r_hi):
    """Median colour of an annulus, so lettering doesn't skew it."""
    box = mask.getbbox()
    coin = im.convert("RGB").crop(box)
    w, h = coin.size
    cx, cy, rad = w / 2.0, h / 2.0, min(w, h) / 2.0
    px = coin.load()
    chans = ([], [], [])
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / rad
            if r_lo <= d <= r_hi:
                for i, v in enumerate(px[x, y]):
                    chans[i].append(v)
    if not chans[0]:
        return (0, 0, 0)
    return tuple(sorted(c)[len(c) // 2] for c in chans)


def features(im, mask, hole_area):
    core = ring_of(im, mask, 0.20, 0.40)
    edge = ring_of(im, mask, 0.72, 0.84)
    coin_area = sum(mask.histogram()[128:]) or 1
    return {
        "hole": hole_area > coin_area * 0.004,
        "bimetal": sum(abs(a - b) for a, b in zip(core, edge)) > 46,
        "core_warm": core[0] - core[2],
        "edge_warm": edge[0] - edge[2],
        "lum": sum(edge) / 3.0,
    }


def classify(seen):
    """Assign countries across the whole batch, so pairs settle each other."""
    out = {}
    holed = sorted([f for f in seen if f["hole"]], key=lambda f: f["lum"])
    if len(holed) >= 2:
        out[holed[0]["path"]] = "papua-new-guinea"
        out[holed[1]["path"]] = "denmark"
    elif holed:
        out[holed[0]["path"]] = "papua-new-guinea" if holed[0]["lum"] < 155 else "denmark"

    for f in seen:
        if f["path"] in out:
            continue
        if f["bimetal"]:
            out[f["path"]] = "thailand" if f["core_warm"] > f["edge_warm"] else "germany"
        else:
            out[f["path"]] = "jordan" if f["core_warm"] > 18 else "philippines"
    return out


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
    ap.add_argument("--by-name", action="store_true",
                    help="match on filenames only, instead of reading the coins")
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

    # First pass: cut every file, letting each one show whether it is holed.
    seen = []
    for path in files:
        im = Image.open(path)
        mask, hole_area = cut_background(im, args.tol, None)
        f = features(im, mask, hole_area)
        f.update(path=path, im=im, mask=mask)
        seen.append(f)

    read_names = {} if args.by_name else classify(seen)

    done, skipped = [], []
    for f in seen:
        path = f["path"]
        country = explicit.get(path.name) or match_country(path) or read_names.get(path)
        if not country:
            skipped.append(path.name)
            continue

        # Re-cut only if what the image suggested about the hole was wrong.
        want_hole = COUNTRIES[country] and country not in args.no_hole
        mask = f["mask"]
        if want_hole != f["hole"]:
            mask, _ = cut_background(f["im"], args.tol, want_hole)

        dest = out_dir / (country + ".png")
        square_up(f["im"], mask).save(dest, "PNG", optimize=True)
        by_name = bool(explicit.get(path.name) or match_country(path))
        done.append((country, dest, dest.stat().st_size // 1024, want_hole,
                     path.name, f, by_name))

    for country, dest, kb, hole, src, f, by_name in done:
        print("  {:<18} <- {}".format(country, src))
        print("  {:<18}    {} · {} KB{} · {} · {}{} · {}".format(
            "", dest, kb, ", hole punched" if hole else "",
            "by filename" if by_name else "read off the coin",
            "holed" if f["hole"] else "solid",
            ", bimetal" if f["bimetal"] else "",
            "warm metal" if f["core_warm"] > 18 else "cool metal"))

    names = [d[0] for d in done]
    clashes = sorted({c for c in names if names.count(c) > 1})
    if clashes:
        print("\nTwo files landed on the same country ({}) — one overwrote the "
              "other. Pin them with --map.".format(", ".join(clashes)))

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
