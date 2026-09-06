#!/usr/bin/env python3
"""
Turn phone photographs into the web-sized files the gallery wants, and print
the CONFIG.photos block to paste into index.html.

    python3 tools/prepare_photos.py photos/originals --out photos/

A photo straight off a phone is three to six megabytes. Eight of those would
be thirty megabytes on a page built for phones, so each one is resized to
1600px on the long edge and saved as WebP — usually under 200 KB, and no
visible difference at the size the page draws it.

Place and year are read from the filename where they are there:

    amman-2019.jpg        → Amman, 2019
    port-moresby-2021.jpg → Port Moresby, 2021
    IMG_4471.jpg          → left blank for you to fill in

Captions can't be guessed, so the printed block leaves them empty. Write one
line each — they read as marginalia, not as an album.
"""

import argparse
import pathlib
import re
import sys

from PIL import Image, ImageOps

# iPhones shoot HEIC by default and Pillow cannot read it unaided. This is
# optional so the tool still runs without it — it just skips .heic files.
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

LONG_EDGE = 1600
QUALITY = 82

# Words that shouldn't be capitalised in the middle of a place name.
SMALL = {"of", "the", "and", "upon", "de", "del", "la", "le", "van", "den"}


def read_name(stem):
    """Pull a place and a year out of a filename, where they are in there."""
    slug = re.sub(r"[_\s]+", "-", stem.strip().lower())
    year = ""
    m = re.search(r"(?:^|-)((?:19|20)\d{2}(?:-\d{2})?)(?:-|$)", slug)
    if m:
        year = m.group(1).replace("-", "–")
        slug = (slug[:m.start()] + "-" + slug[m.end():]).strip("-")

    words = [w for w in slug.split("-") if w and not w.isdigit()]
    if not words or re.fullmatch(r"(img|dsc|photo|image|pxl)\d*", words[0]):
        return "", year

    place = " ".join(
        w if (i and w in SMALL) else w.capitalize() for i, w in enumerate(words)
    )
    return place, year


def main():
    ap = argparse.ArgumentParser(description="Prepare photographs for the gallery.")
    ap.add_argument("src", help="folder of original photographs")
    ap.add_argument("--out", default="photos", help="where the web-sized files go")
    ap.add_argument("--size", type=int, default=LONG_EDGE, help="long edge, px")
    ap.add_argument("--format", choices=["webp", "jpg"], default="webp")
    args = ap.parse_args()

    src = pathlib.Path(args.src)
    files = sorted(
        p for p in src.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".heic"}
    ) if src.is_dir() else [src]
    if not files:
        raise SystemExit("No photographs found in " + str(src))

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    entries, total = [], 0
    for path in files:
        try:
            im = Image.open(path)
        except Exception as e:
            print("  skipped {} — {}".format(path.name, e))
            continue

        # Phones record orientation in EXIF rather than in the pixels.
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((args.size, args.size), Image.LANCZOS)

        place, year = read_name(path.stem)
        slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-") or "photo"
        dest = out_dir / (slug + "." + args.format)

        if args.format == "webp":
            im.save(dest, "WEBP", quality=QUALITY, method=6)
        else:
            im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)

        kb = dest.stat().st_size // 1024
        total += kb
        print("  {:<34} {} · {} KB".format(dest.name, "×".join(map(str, im.size)), kb))
        entries.append((dest.as_posix(), place, year))

    if not entries:
        sys.exit(1)

    print("\n  {} photographs, {} KB in all\n".format(len(entries), total))
    print("Paste this into CONFIG.photos in index.html:\n")
    print("  photos: [")
    for src_path, place, year in entries:
        print('    {{ src: "{}", place: "{}", year: "{}",\n'
              '      caption: "" }},'.format(src_path, place, year))
    print("  ],")


if __name__ == "__main__":
    main()
