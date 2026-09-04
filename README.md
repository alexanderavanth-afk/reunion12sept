# Genforeningsmiddag — 12. september

RSVP page for the reunion dinner at Restaurant Norrlyst: who's coming, how many
they are, which of the two four-course menus each person wants, and any
allergies.

`index.html` is the whole site — no build step, no framework, no dependencies.
Danish by default with an EN toggle; light and dark themes both designed.

**Live:** _(paste the Vercel URL here once deployed)_

---

## Where the replies go

Submissions `POST` as JSON to Formspree, configured in the `CONFIG` block at the
top of `index.html`:

```js
endpoint: "https://formspree.io/f/mljeljaa",
```

Replies arrive by email and collect in the Formspree dashboard, where they can
be exported to CSV. If the request ever fails, the page offers the guest a
pre-filled email to `CONFIG.hostEmail` as a fallback, so nobody hits a dead end.

Each submission looks like this:

```json
{
  "attending": "yes",
  "name": "Maja Jensen",
  "party": 2,
  "guests": [
    { "seat": 1, "name": "Maja Jensen", "menu": "klassisk", "menuLabel": "Norrlyst-menuen" },
    { "seat": 2, "name": "Anders Holm", "menu": "gron", "menuLabel": "Den grønne Norrlyst-menu" }
  ],
  "tally": { "klassisk": 1, "gron": 1 },
  "diet": "Anders: nødder",
  "note": "",
  "summary": "…plain-text version of the above…"
}
```

`summary` is the readable one — it's what shows up in the notification email.

## Editing the evening

Everything editable lives in `CONFIG` at the top of `index.html`.

| Key | What it does |
| --- | --- |
| `endpoint` | Where RSVPs are sent |
| `hostEmail`, `hostName` | Footer contact; used by the email fallback |
| `date`, `time`, `venue`, `venueUrl` | The facts strip under the headline |
| `deadline` | The reply-by date in the footer |
| `maxGuests` | Upper limit on the party-size stepper |
| `price` | Printed under the menus |
| `menus[]` | The two menus and their courses |

### The menu

Norrlyst serves a set four-course menu in the evening in two versions: the
Norrlyst menu (meat, fish and shellfish) and the green Norrlyst menu
(vegetarian). The dishes are seasonal, so the page ships with the course
structure rather than invented dish names.

To print the actual dishes, replace the `courses` entries with the current text
from <https://norrlyst.dk/restaurantnorrlyst/aften/>:

```js
courses: [
  { da: "Dansk makrel, tomat og basilikum", en: "Danish mackerel, tomato and basil" },
  …
]
```

Any number of courses works; each is numbered automatically.

## Deploy

Connected to Vercel from this repository — pushing to `main` redeploys.

To preview locally: `python3 -m http.server 4000`, then open
<http://localhost:4000>. Opening `index.html` directly with `file://` also
works.

`vercel.json` only sets `cleanUrls` and two security headers; the folder drops
onto Netlify, Cloudflare Pages or GitHub Pages unchanged.

## Notes

- The language toggle is remembered per viewer in `localStorage`. Every string
  lives in a `data-da` / `data-en` attribute or in `CONFIG`.
- **No contact details are collected** beyond a name, deliberately — nothing
  sensitive sits in the payload or in a third-party dashboard. To collect a
  phone number, add a field to the form and a line to `payload()`.
- Guests can revise their answer with "Ret min tilmelding", which sends a second
  submission — the later timestamp wins.
