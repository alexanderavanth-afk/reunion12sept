# Living Life on a Coin Toss

RSVP page for the reunion dinner at Restaurant Norrlyst on 12 September.
Six countries, six coins, one table.

`index.html` is the whole site — no build step, no framework, no dependencies.
Deployed on Vercel from `main`; pushing redeploys.

**Live:** _(paste the Vercel URL here)_

---

## The design

A single committed visual world: bone paper, ink, and struck metal. Archivo for
the display and interface, Newsreader for the menu prose, IBM Plex Mono for
prices and labels. Danish by default, English on the toggle.

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
tapped, cycling back to the dinner's own coin. `prefers-reduced-motion` skips
the animation and just paints the result.

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

## Editing the evening

Everything editable lives in `CONFIG` at the top of `index.html`.

| Key | What it does |
| --- | --- |
| `endpoint` | Where RSVPs are sent |
| `hostEmail`, `hostName` | Footer contact; used by the email fallback |
| `date`, `time`, `venue`, `venueUrl`, `city` | The facts ledger under the headline |
| `deadline` | The reply-by date |
| `maxGuests` | Upper limit on the party-size stepper |
| `countries[]` | The six coins — name, unit, denomination, metal, `ring`, `hole`, and the one-line fact |
| `courses[]` | The menu: course groups, each with its dishes |

### A dish

```js
{ id: "tatar", name: "Norrlyst signatur tatar",
  desc: "Af okse, fløde-kefir, peberrod, aromatiske urter og røgede mandler",
  price: 110, supp: 75, label: "110 / 150" }
```

`price` is the à la carte price. `supp` is optional and prints as the `+75` chip
beside the name. `label` overrides the printed price where it isn't a single
number (the cheese course). Adding, removing or reordering dishes needs no other
change — the menu and every guest's dropdown are both generated from this list.

Dish names and descriptions stay in Danish in both languages: a chef's menu
reads as written. Only the interface around it translates.

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
- The language choice is remembered per viewer in `localStorage`.
