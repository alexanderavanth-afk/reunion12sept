/**
 * The source of truth for the reunion dinner.
 *
 * Paste this into a Google Sheet's Apps Script editor and deploy it as a web
 * app. The RSVP page then posts every reply straight into the sheet, and the
 * overview page reads it back — so there is one place that is always current,
 * and nothing to copy by hand.
 *
 * Three tabs, rebuilt on every submission:
 *
 *   Replies    one row per guest — who, in whose party, and their four courses
 *   Kitchen    every dish with a count, grouped by course. This is the list
 *              the restaurant needs.
 *   Allergies  one row per party that flagged anything
 *
 * Someone who replies twice replaces their earlier answer, so the sheet never
 * double-counts a guest who changes their mind.
 *
 * Setup is in SHEET-SETUP.md.
 */

/* Anyone may POST a reply — the invitation page has to be able to, and the
   worst a stranger can do is add a row you delete. Reading is different: the
   replies carry names and allergies, so doGet answers only when it is handed
   this key. It lives in the overview page's browser, never in the site — and
   not in this repository either, which is why the line below is a placeholder:
   put the real key in when you paste this into the script editor. */
var READ_KEY = 'PUT-YOUR-KEY-HERE';

var COURSES = [
  ['forret', 'Starters'],
  ['mellemret', 'Middle courses'],
  ['hovedret', 'Main courses'],
  ['dessert', 'Desserts & cheese']
];

var HEAD = ['Submitted', 'Party of', 'Guest', 'Starters', 'Middle courses',
            'Main courses', 'Desserts & cheese', 'Allergies', 'Note'];

/* ── Receiving a reply ────────────────────────────────────────────── */

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var d = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = tab(ss, 'Replies', HEAD);

    // A second reply from the same person replaces the first.
    dropRowsFor(sh, d.name);

    var now = new Date();
    var rows = (d.guests || []).map(function (g) {
      var order = g.order || {};
      return [now, d.name || '', g.name || ''].concat(
        COURSES.map(function (c) { return order[c[0]] || ''; }),
        [d.diet || '', d.note || '']
      );
    });

    if (rows.length) {
      sh.getRange(sh.getLastRow() + 1, 1, rows.length, HEAD.length).setValues(rows);
    }

    rebuild(ss);
    return json({ ok: true, guests: rows.length });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

/* ── Handing the replies back to the overview page ────────────────── */

function doGet(e) {
  var given = (e && e.parameter && e.parameter.key) || '';
  if (given !== READ_KEY) return json({ ok: false, error: 'unauthorised' });

  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Replies');
  if (!sh || sh.getLastRow() < 2) return json({ replies: [] });

  var values = sh.getRange(2, 1, sh.getLastRow() - 1, HEAD.length).getValues();
  var byParty = {};

  values.forEach(function (r) {
    var host = String(r[1] || '').trim();
    if (!host) return;
    var key = host.toLowerCase();
    if (!byParty[key]) {
      byParty[key] = {
        name: host, attending: 'yes', guests: [],
        diet: String(r[7] || ''), note: String(r[8] || ''),
        submittedAt: r[0] ? new Date(r[0]).toISOString() : ''
      };
    }
    var order = {};
    COURSES.forEach(function (c, i) { order[c[0]] = String(r[3 + i] || ''); });
    byParty[key].guests.push({
      seat: byParty[key].guests.length + 1,
      name: String(r[2] || ''),
      order: order
    });
  });

  var out = Object.keys(byParty).map(function (k) {
    var p = byParty[k];
    p.party = p.guests.length;
    return p;
  });
  return json({ replies: out });
}

/* ── The two summary tabs ─────────────────────────────────────────── */

function rebuild(ss) {
  var sh = ss.getSheetByName('Replies');
  var rows = sh.getLastRow() < 2 ? []
    : sh.getRange(2, 1, sh.getLastRow() - 1, HEAD.length).getValues();

  // Kitchen: every dish, counted, in the order the courses are served.
  var kitchen = [['Course', 'Dish', 'How many']];
  COURSES.forEach(function (c, i) {
    var counts = {};
    rows.forEach(function (r) {
      var dish = String(r[3 + i] || '').trim();
      if (dish) counts[dish] = (counts[dish] || 0) + 1;
    });
    Object.keys(counts)
      .sort(function (a, b) { return counts[b] - counts[a] || a.localeCompare(b); })
      .forEach(function (dish) { kitchen.push([c[1], dish, counts[dish]]); });
  });
  kitchen.push([]);
  kitchen.push(['Covers', rows.length, '']);
  write(ss, 'Kitchen', kitchen);

  // Allergies: one line per party that flagged something.
  var seen = {};
  var diets = [['Party of', 'Allergies and dietary needs']];
  rows.forEach(function (r) {
    var host = String(r[1] || '').trim();
    var diet = String(r[7] || '').trim();
    if (diet && !seen[host]) { seen[host] = true; diets.push([host, diet]); }
  });
  if (diets.length === 1) diets.push(['—', 'Nobody has flagged anything yet']);
  write(ss, 'Allergies', diets);
}

/* ── Small helpers ────────────────────────────────────────────────── */

function tab(ss, name, header) {
  var sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.getRange(1, 1, 1, header.length).setValues([header]).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  return sh;
}

function dropRowsFor(sh, name) {
  if (sh.getLastRow() < 2 || !name) return;
  var col = sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues();
  for (var i = col.length - 1; i >= 0; i--) {
    if (String(col[i][0]).trim().toLowerCase() === String(name).trim().toLowerCase()) {
      sh.deleteRow(i + 2);
    }
  }
}

function write(ss, name, values) {
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clear();
  if (!values.length) return;
  var width = Math.max.apply(null, values.map(function (r) { return r.length; })) || 1;
  var padded = values.map(function (r) {
    var row = r.slice();
    while (row.length < width) row.push('');
    return row;
  });
  sh.getRange(1, 1, padded.length, width).setValues(padded);
  sh.getRange(1, 1, 1, width).setFontWeight('bold');
  sh.setFrozenRows(1);
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
