# What to send me, and how

Two sets of files. Both are optional — the site works without them and picks
them up the moment they land.

---

## 1. The coins

**Done.** All six are in `coins/`, generated from
[`COIN-PROMPTS.md`](COIN-PROMPTS.md) and processed by
`tools/prepare_coins.py`. The originals are kept in `coins/originals/` (not
deployed — see `.vercelignore`) in case any needs redoing.

To replace one: generate it, drop it in a folder, and run

    python3 tools/prepare_coins.py that-folder --out coins/

Don't worry about file format, size, naming or transparency — I handle all of
it. `tools/prepare_coins.py` cuts out the background, punches the holes in the
Papua New Guinea and Denmark coins, squares each one up, centres it and writes
`coins/<country>.png` at 1024 × 1024 with real alpha.

**Filenames don't matter either.** Each image says which coin it is: a hole
through the middle means Papua New Guinea or Denmark (the darker one is PNG),
two metals means Thailand or Germany (gold core is Thailand), one metal and no
hole means Jordan or Philippines (gold is Jordan). Six files called
`ChatGPT Image Sep 5, 2026, 03_39_06 PM.png` sort themselves out.

The one thing that does matter: **no drop shadow.** A shadow bleeds into the
cutout and leaves a grey halo. The prompts say so three times; if one comes
back with a shadow anyway, ask for it again.

If a coin never lands, nothing breaks — that country keeps the SVG drawing
already on the page. They can arrive one at a time.

## 2. The photographs

**Upload them to [`photos/`](https://github.com/alexanderavanth-afk/reunion12sept/upload/main/photos)
and tell me.** Straight off a phone is fine — `tools/prepare_photos.py` resizes
each one to 1600px and saves it as WebP, which takes a set of eight from about
thirty megabytes down to one or two.

Name them `place-year.jpg` where you can — `amman-2019.jpg`,
`port-moresby-2021.jpg` — and the place and year fill themselves in. Anything
called `IMG_4471.jpg` still works; I just have to be told what it is.

**Captions I can't guess.** One line each, and shorter is better — they read as
marginalia beside the picture, not as an album. A fact, a date, a private joke.
Send them as a list:

```
amman-2019      | The winter we learned to make proper coffee
port-moresby    | Lisa's road to school, more or less
```

Six to nine sits best in the grid. The section stays hidden until the first one
lands, and the section numbering closes up around it, so there is no harm in
taking your time.
