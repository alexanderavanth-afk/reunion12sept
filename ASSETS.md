# What to send me, and how

Two sets of files. Both are optional — the site works without them and picks
them up the moment they land.

---

## 1. The coins

**Open [`COIN-PROMPTS.md`](COIN-PROMPTS.md), paste each of the six blocks into
ChatGPT, and download what comes back.** Then send me the six images. That's
the whole job on your side.

Don't worry about file format, size, naming or transparency — I handle all of
it. `tools/prepare_coins.py` cuts out the background, punches the holes in the
Papua New Guinea and Denmark coins, squares each one up, centres it and writes
`coins/<country>.png` at 1024 × 1024 with real alpha. Files are matched to
countries by whatever is in the filename, so `image_04.png` just needs a word
like "denmark" or "krone" in it — or you tell me which is which.

The one thing that does matter: **no drop shadow.** A shadow bleeds into the
cutout and leaves a grey halo. The prompts say so three times; if one comes
back with a shadow anyway, ask for it again.

If a coin never lands, nothing breaks — that country keeps the SVG drawing
already on the page. They can arrive one at a time.

## 2. The photographs

**JPGs in `photos/`**, named by place and year in lowercase with hyphens:

```
photos/amman-2019.jpg
photos/port-moresby-2021.jpg
photos/bangkok-2023.jpg
```

### Format

| | |
| --- | --- |
| File type | **JPG** (photos, not PNG — a tenth of the size at the same quality) |
| Size | **1600 px on the long edge**, quality ~80 |
| Weight | Under ~400 KB each |
| Crop | Anything — they're displayed 4:3 and centre-cropped, so keep the subject away from the extreme edges |
| How many | Six to nine sits best in the grid |

Straight off a phone is fine; anything over ~1 MB I'll resize.

### What to send with them

For each photo, three lines:

```
photos/amman-2019.jpg | Amman | 2019 | The winter we learned to make proper coffee.
```

- **Place** — a city or a country, whatever reads better
- **Year** — or a range, "2019–20"
- **Caption** — one line. The shorter the better; these read as marginalia, not
  as an album. Anything from a fact to a private joke.

Send them as a list in chat and I'll wire them up, or paste them straight into
`CONFIG.photos` in `index.html` — the shape is commented in there.
