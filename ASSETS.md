# What to send me, and how

Two sets of files. Both are optional — the site works without them and picks
them up the moment they land in the repo.

---

## 1. The coins

**Six PNGs, one per country.** Drop them in `coins/` with exactly these names —
they're already wired into `CONFIG.countries[].image`:

```
coins/jordan.png
coins/philippines.png
coins/papua-new-guinea.png
coins/thailand.png
coins/germany.png
coins/denmark.png
```

### Format

| | |
| --- | --- |
| File type | **PNG with real alpha transparency** — not a white square |
| Size | **2048 × 2048**, square, one coin per file |
| Framing | Coin centred, filling **~92%** of the frame, edges not cropped |
| Angle | Straight-on, flat to camera — no perspective tilt |
| Shadow | **None baked in.** The page adds its own, and the coin flips in 3D |
| Weight | Under ~600 KB each after export; I'll compress further if needed |

The two holed coins — Papua New Guinea and Denmark — should have the centre
hole **transparent all the way through**, not filled with background.

If a file is missing or fails to load, that coin quietly falls back to the SVG
drawing already on the page. So you can send them one at a time.

### The prompt

One shared preamble, then a block per coin. Paste **preamble + coin block**
together as a single prompt.

**Preamble — use for all six:**

> Macro product photograph of a single circular coin, shot straight-on from
> directly above, perfectly centred and filling about 92% of a square frame.
> Completely transparent background — no backdrop, no surface, no shadow, no
> reflection. Soft diffuse studio light from the upper left: gentle specular
> highlights along the raised relief, shallow shading in the recessed areas.
> The coin has been in circulation: fine hairline scratches across the field,
> softened high points on the lettering, faint darkened patina settled into the
> engraving. Razor-sharp macro focus edge to edge. Shallow relief, struck not
> engraved. No text anywhere outside the coin itself.

**Jordan** → `coins/jordan.png`

> The coin is golden nickel-brass with a warm brassy tone and a finely reeded
> milled edge. Raised sans-serif capitals arch across the top of the face
> reading JORDAN, and across the bottom reading DINAR. In the centre, large and
> in high relief, the Eastern Arabic numeral ١٠. A plain raised circular border
> rings the inner field.

**Philippines** → `coins/philippines.png`

> The coin is bright nickel-plated steel, cool silver-white, with a smooth
> plain edge. Raised sans-serif capitals arch across the top reading
> PHILIPPINES, and across the bottom reading PISO. In the centre, large and in
> high relief, the numeral 1. A plain raised circular border rings the inner
> field.

**Papua New Guinea** → `coins/papua-new-guinea.png`

> The coin is aged silver-grey cupronickel, noticeably darker and more
> oxidised than a new coin, with a reeded edge. **A perfectly round hole is
> punched straight through the exact centre of the coin — the hole must be
> fully transparent, showing nothing behind it.** A raised rim surrounds the
> hole. Raised sans-serif capitals arch across the top reading PAPUA NEW
> GUINEA, and across the bottom reading KINA.

**Thailand** → `coins/thailand.png`

> The coin is bimetallic: a white cupronickel outer ring around a warm
> brass-gold centre disc, with a clean visible seam between the two metals.
> Raised sans-serif capitals arch across the white outer ring, reading THAILAND
> at the top and BAHT at the bottom. In the brass centre, large and in high
> relief, the Thai numeral ๑๐.

**Germany** → `coins/germany.png`

> The coin is bimetallic in the reverse arrangement: a gold-coloured
> nickel-brass outer ring around a silver cupronickel centre disc, with a clean
> visible seam. Raised sans-serif capitals arch across the gold outer ring,
> reading GERMANY at the top and EURO at the bottom. In the silver centre,
> large and in high relief, the numeral 2.

**Denmark** → `coins/denmark.png`

> The coin is silver cupronickel with a reeded edge. **A perfectly round hole
> is punched straight through the exact centre — the hole must be fully
> transparent, showing nothing behind it.** Above the hole sits a crowned royal
> monogram in raised relief: a simple heraldic crown over an entwined cipher.
> Raised sans-serif capitals arch across the top reading DENMARK, and across
> the bottom reading KRONE.

### If the lettering comes out wrong

Image models are unreliable with text, and the Arabic `١٠` and Thai `๑๐` are
the hardest parts. Two ways out:

1. **Regenerate.** Copy the glyphs from this file rather than retyping them,
   and say "the lettering must be spelled exactly as written".
2. **Skip the text.** Ask for the coin with *"a blank raised inner field and no
   lettering at all"* and send that. I'll overlay the legend and the
   denomination as crisp vector type on top — which will read better than
   anything a model letters by hand.

Option 2 is genuinely the stronger result if the first two attempts disappoint.

---

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
