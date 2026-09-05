# Planning Life on a Coin Toss

RSVP page for the reunion dinner at Restaurant Norrlyst on 12 September.
Six countries, six coins, one table.

Two pages, no build step, no framework, no dependencies:

- `index.html` — the invitation and RSVP form guests fill in.
- `overview.html` — a host-only tool that turns the collected replies into one
  sheet the restaurant can read. Nothing links to it from the invitation.

Deployed on Vercel from `main`; pushing redeploys.

**Live:** _(paste the Vercel URL here)_

---

## The design

A single committed visual world: bone paper, ink, and struck metal. Archivo for
the display and interface, Newsreader for the menu prose, IBM Plex Mono for
labels. English throughout — everyone at this table reads it.

**The coins are drawn, not photographed** — SVG built in `coinSVG()`: a struck
disc, a generated reeded rim, the legend set on an arc, and either a hole or a
denomination in the country's own script. The structural details are real:

| | Coin | Detail encoded |
| --- | --- | --- |
| Jordan | Dinar | Arabic-Indic numerals (`١٠`) |
| Philippines | Piso | Plain nickel strike |
| Papua New Guinea | Kina | Holed through the centre |
| Thailand | Baht | Bimetal — brass core, white ring |
| Germany | Euro | Bimetal — the inverse arrangement |
| Denmark | Krone | Holed, with a crowned monogram |

The metals are stylised; the holes, rings and scripts are not. The Arabic and
Thai numerals load as `text=`-subsetted Noto faces (a few hundred bytes) with
system fallbacks behind them.

The hero coin flips once on load and lands on a new country each time it's
tapped. Landing does three things at once: the coin is restruck, the whole page
washes to that country's palette, and its line on life appears beneath —
H.C. Andersen for Denmark, a Dhammapada verse for Thailand, a Tagalog proverb
for the Philippines, a hadith in Arabic for Jordan, Goethe for Germany, and a
Tok Pisin saying for Papua New Guinea. `prefers-reduced-motion` skips the
animation and paints the result directly.

Each country's `palette` (seven colours) and `quote` live beside it in
`CONFIG.countries`, so both are edited in one place.

## The page, in order

The invitation is only sent to people who are already coming, so the page is
built to be acted on, not read: coin, headline, **the button**, and then the
form. Everything else — the running order, the coins, the photographs — sits
below the form for whoever wants it. There is no "can't make it" option and no
way to skip a course; both were decisions nobody needed to make.

## The RSVP flow

Three numbered steps on one page — no wizard, nothing to lose on a refresh:

1. **Who's coming?** — your name, a party-size stepper, and
   (as soon as the party is more than one) a name field per extra guest.
2. **The dishes** — one box that asks one question at a time. Tap a dish and it
   advances to the next course; after the last course it moves to the next
   person and starts again. A **Back** button, four pips for the courses, and a
   `3 / 8` counter say where you are. When a plus-one exists, a tab strip names
   each person with their progress (`02 1/4 Maja`) and the header reads
   `MAJA · 2 OF 2`, so whose dinner you're choosing is never in doubt. Tabs are
   clickable — they jump to that person's first unanswered course. At the end
   the box turns into a summary with a **Change** link on every line.
3. **Confirm** — a live reading of exactly what the send button will post.

## Phones

Most people will open this on one, so it is checked rather than assumed: no
horizontal overflow at 320, 360, 390 or 430 px, the call to action about 650 px
down (one short scroll), the facts ledger two-up instead of four-down, the
picker header wrapping rather than truncating, and every control at least 44 px
tall. Inputs are 16 px so iOS doesn't zoom on focus.

The vegetarian dish in each course carries a `VEG` mark, set by `veg: true` on
the dish.

The room seats fifteen, and the page says so twice: once under the headline
where nobody can miss it, and again beside the party stepper where it bears on
what someone is about to type. `CONFIG.seats` sets the number in both places,
and the overview page counts down from it.

## Coins and photographs

Both are optional files the page picks up if they exist.

**Coins** — a transparent square PNG per country in `coins/`, named in
`CONFIG.countries[].image`. Without one, or if the file 404s, the coin falls
back to the SVG drawing, so the page never shows an empty box.

**Photographs** — JPGs in `photos/`, listed in `CONFIG.photos` with a `place`,
`year` and `caption`. The whole section stays hidden while that array is empty,
and the section numbering closes up around it.

## Where the replies go

Submissions `POST` as JSON to Formspree, set in the `CONFIG` block at the top of
`index.html`:

```js
endpoint: "https://formspree.io/f/mljeljaa",
```

Replies arrive by email and collect in the dashboard for CSV export. If the
request fails, the page offers the guest a pre-filled email to `CONFIG.hostEmail`
instead, so nobody hits a dead end.

Each submission carries the whole party, dish by dish, plus a tally the kitchen
can read directly:

```json
{
  "attending": "yes",
  "name": "Maja Jensen",
  "party": 2,
  "guests": [
    { "seat": 1, "name": "Maja Jensen",
      "order": { "forret": "Løgtærte", "mellemret": "Stegte hvide asparges",
                 "hovedret": "Stegt kål", "dessert": "Rabarber “Baked Alaska”" } },
    { "seat": 2, "name": "Anders Holm",
      "order": { "forret": "Hummersalat", "mellemret": "Ingen tak",
                 "hovedret": "Striploin af krondyr", "dessert": "3 / 5 oste" } }
  ],
  "kitchen": { "Løgtærte": 1, "Hummersalat": 1, "Stegt kål": 1, "…": 1 },
  "diet": "Anders: nødder",
  "note": "",
  "summary": "…plain-text version of all of the above…"
}
```

`summary` is the readable one — it's what lands in the notification email.
`rows` is one flat line per guest (`Name | forret | mellemret | hovedret |
dessert`), which is what survives a CSV round-trip when the nested `guests`
array doesn't.

## The restaurant overview

Open `overview.html` and paste the replies in — whichever form is to hand:

- **the notification emails**, copied from `ATTENDING` down, several in a row;
- **Export → JSON** from the Formspree dashboard;
- **CSV**, which falls back to the flat `rows` field.

Each submission is only ever its own party. The aggregating across everybody
happens here, in the browser, on whatever you paste. It produces:

- **Optælling** — covers, parties, regrets, dishes chosen.
- **Til køkkenet** — every dish with a count, grouped by course. This is the
  number the kitchen actually needs.
- **Bordet** — one row per person with all four courses.
- **Allergier** and **Afbud**.

Everything is computed in the browser; nothing is uploaded. **Print** gives a
clean sheet to hand over, and **Kopiér som regneark** puts a tab-separated
table on the clipboard for Excel or Sheets. Duplicate answers from the same
name are collapsed, keeping the later one — so someone who changes their mind
is counted once. "Vis et eksempel" loads sample data
if you want to see the shape before the real replies arrive.

Its `COURSES` list must stay in step with `CONFIG.courses` in `index.html` —
that's the one place the two files have to agree.

## Editing the evening

Everything editable lives in `CONFIG` at the top of `index.html`.

| Key | What it does |
| --- | --- |
| `endpoint` | Where RSVPs are sent |
| `maxGuests` | Upper limit on the party-size stepper |
| `hostEmail`, `hostName` | Footer contact; used by the email fallback |
| `date`, `time`, `venue`, `venueUrl`, `city` | The facts ledger under the headline |
| `agenda[]` | The running order — time, label, and an optional `aside` printed in the accent |
| `seats` | The size of the room: shown in the notice and the stepper hint, counted down in the overview |
| `host` | The resting coin's palette and line, before anything is tossed |
| `deadline` | The reply-by date |
| `countries[]` | The six coins — name, unit, denomination, metal, `ring`, `hole`, the one-line fact, the `palette` and the `quote` |
| `courses[]` | The menu: course groups, each with its dishes |

### A dish

```js
{ id: "tatar",
  name: "Norrlyst signatur tatar",
  en:   "Norrlyst signature tartare",
  desc: "Beef, cream kefir, horseradish, aromatic herbs and smoked almonds" }
```

Adding, removing or reordering dishes needs no other change — the printed card
and every guest's tick list are both generated from this list.

**No prices anywhere.** The hosts are paying, and a price list only makes
people order politely.

Each dish carries three strings: `name` is the dish as Norrlyst writes it,
`en` is the English name guests read, and `desc` is the English description.
The page shows the English with the Danish original set small beneath it — so
a guest can point at the right line in the restaurant — and **the payload sends
the Danish `name`**, because that's the wording the kitchen works from. The
overview page therefore tallies in Danish, which is correct.

## Deploy

Connected to Vercel from this repository. To preview locally:
`python3 -m http.server 4000`, then <http://localhost:4000>. Opening
`index.html` with `file://` works too.

`vercel.json` only sets `cleanUrls` and two security headers; the folder drops
onto Netlify, Cloudflare Pages or GitHub Pages unchanged.

## Notes

- **No contact details are collected** beyond names, deliberately — nothing
  sensitive sits in the payload or a third-party dashboard. To collect a phone
  number, add a field and a line to `payload()`.
- Guests can revise with "Ret min tilmelding", which sends a second submission —
  the later timestamp wins.
