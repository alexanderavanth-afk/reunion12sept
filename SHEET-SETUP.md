# One source of truth

Ten minutes, once. After this every reply writes itself into a Google Sheet,
the kitchen list and the allergy list keep themselves current, and
`/overview` reads the sheet each time you open it. Nothing to copy, ever.

You send the same link on Saturday and on Tuesday and it says something
different each time, because it is reading the sheet, not a snapshot.

---

## 1 · Make the sheet

Go to [sheets.new](https://sheets.new). Name it something like
**Reunion dinner — replies**. Leave it empty; the script builds its own tabs.

## 2 · Open the script editor

**Extensions → Apps Script**. A code editor opens in a new tab with a small
`function myFunction() {}` in it.

## 3 · Paste the code

Select everything in that editor and delete it. Open
[`tools/sheet-backend.gs`](tools/sheet-backend.gs) in this repository, copy the
whole file, paste it in. Press the save icon.

## 4 · Deploy it

**Deploy → New deployment**. Then:

| Field | What to choose |
| --- | --- |
| Select type (the ⚙ icon) | **Web app** |
| Description | anything |
| Execute as | **Me** |
| Who has access | **Anyone** |

Press **Deploy**. Google will ask you to authorise it — this is your own script
writing to your own sheet, so click through: *Review permissions* → your
account → **Advanced** → *Go to (project name) (unsafe)* → **Allow**. The
"unsafe" wording is what Google says about any unpublished personal script.

## 5 · Copy the URL

You get a **Web app URL** ending in `/exec`. Copy it. It looks like:

```
https://script.google.com/macros/s/AKfycb…long…/exec
```

**Treat it like a password.** Anyone with it can read the replies.

## 6 · Done — it's wired in

The URL is in `CONFIG.sheet` in `index.html` and `SHEET` in `overview.html`.
Send yourself one RSVP and watch it land in the sheet.

## Turning it off afterwards

When the dinner is over, shut it down in two places. Both take a minute.

**1 · Kill the URL.** In the Apps Script editor: **Deploy → Manage
deployments**, click the pencil, set **Version → New version** and **Who has
access → Only myself**, then **Deploy**. The URL immediately stops answering
anyone but you. (Archiving the deployment from the same screen does the same
thing more permanently.)

**2 · Withdraw the script's access to your account.** Go to
[myaccount.google.com/permissions](https://myaccount.google.com/permissions),
find the project in the list, and choose **Remove access**. This is what undoes
the scary screen you clicked through.

The sheet itself is untouched by either — it stays in your Drive with all the
replies in it. Nothing is deleted.

---

## What you get

**The sheet**, three tabs, rebuilt on every reply:

| Tab | What's in it |
| --- | --- |
| **Replies** | One row per guest — who, in whose party, and their four courses |
| **Kitchen** | Every dish with a count, grouped by course, and the cover total. **This is the tab you send the restaurant.** |
| **Allergies** | One row per party that flagged anything |

**`/overview`**, which reads the same data and lays it out to print or copy
into a spreadsheet. Open it whenever; it fetches fresh each time.

Someone who replies twice replaces their first answer, in the sheet and in the
overview both — so nobody is double-counted for changing their mind.

## Things worth knowing

**Formspree keeps working.** Replies go to both, so you still get an email the
moment someone answers. The sheet is the truth; the inbox is the notification.
If you'd rather drop Formspree, empty `CONFIG.endpoint`.

**Changing the code later** means redeploying: **Deploy → Manage deployments →
✏️ → Version: New version → Deploy**. The URL stays the same.

**If the overview says it can't reach the sheet**, the paste box comes back
automatically, so you are never stuck. Usually it means the deployment's *Who
has access* got set to something other than **Anyone**.

**Nothing here costs anything**, and the sheet is yours — export it, print it,
share it with the restaurant directly if that's easier.
