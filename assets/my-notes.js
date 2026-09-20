import { textMatches } from "./search-words.js";

const PROGRESS_PREFIX = "dewlab:progress:";
const HIGHLIGHT_COLORS = { green: "green", blue: "blue", pink: "pink" };

/* This page's own titles map -- {slug: title}, one entry per live
 * tutorial, baked in at build time (write_all_notes_page(), build.py)
 * the same way tree.js reads dewlab-tree. Nothing here can read a title
 * out of localStorage; only the saved record's own tutorial-slug and
 * tutorial-id survive a save. */
function readTitles() {
  const el = document.getElementById("dewlab-titles");
  if (!el) return {};
  try {
    return JSON.parse(el.textContent) || {};
  } catch (err) {
    return {};
  }
}

/* Every saved-progress record this browser holds, across every tutorial
 * ever opened here -- localStorage is shared per origin, not per page, so
 * a page that never ran any of these tutorials' own boot code can still
 * read what they saved. A record that fails to parse (corrupted, or
 * something else entirely using a similar-looking key) is skipped rather
 * than shown broken. */
function readAllRecords() {
  const records = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (!key || !key.startsWith(PROGRESS_PREFIX)) continue;
    try {
      const record = JSON.parse(localStorage.getItem(key));
      if (record && typeof record === "object") records.push(record);
    } catch (err) {
      /* Not a record this page can read. */
    }
  }
  return records;
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[ch]));
}

function highlightRowHtml(slug, highlight) {
  const colorAttr = HIGHLIGHT_COLORS[highlight.color] ? ` data-highlight-color="${highlight.color}"` : "";
  const note = highlight.note
    ? `<span class="dl-highlight-note">${escapeHtml(highlight.note)}</span>` : "";
  return (
    `<a class="dl-highlight-row" href="tutorials/${encodeURIComponent(slug)}.html`
    + `#dl-highlight-${encodeURIComponent(highlight.id)}">`
    + `<span class="dl-highlight-dot" aria-hidden="true"${colorAttr}></span>`
    + '<span class="dl-highlight-text">'
    + `<span class="dl-highlight-quote">"${escapeHtml(highlight.quote)}"</span>`
    + note
    + "</span></a>"
  );
}

/* One card per tutorial with something saved -- its own notes textarea
 * (if not blank) plus every highlight, in the order they were made. A
 * tutorial with cells but neither is skipped entirely rather than shown
 * as an empty card; My Notes is a review surface, not a list of every
 * tutorial ever opened. */
function cardHtml(record, titles) {
  const slug = record["tutorial-slug"] || record["tutorial-id"];
  const title = titles[slug] || slug;
  const highlights = Array.isArray(record.highlights) ? record.highlights : [];
  const notes = typeof record.notes === "string" ? record.notes.trim() : "";
  if (!notes && highlights.length === 0) return "";

  const notesHtml = notes
    ? `<p class="dl-my-notes-freeform">${escapeHtml(notes)}</p>` : "";
  const highlightsHtml = highlights.length
    ? `<div class="dl-highlight-list">${highlights.map((h) => highlightRowHtml(slug, h)).join("")}</div>`
    : "";

  return (
    '<section class="dl-my-notes-card" data-slug="' + escapeHtml(slug) + '">'
    + `<h2><a href="tutorials/${encodeURIComponent(slug)}.html">${escapeHtml(title)}</a></h2>`
    + notesHtml + highlightsHtml
    + "</section>"
  );
}

/* A plain-text study sheet, not the raw JSON each tutorial's own Notes
 * panel already exports -- the same data, but meant to be read rather
 * than reloaded. Grouped and ordered the same way the on-page cards are,
 * so the two never say different things about what "your notes" means. */
function asStudySheet(records, titles) {
  const lines = [];
  for (const record of records) {
    const slug = record["tutorial-slug"] || record["tutorial-id"];
    const title = titles[slug] || slug;
    const highlights = Array.isArray(record.highlights) ? record.highlights : [];
    const notes = typeof record.notes === "string" ? record.notes.trim() : "";
    if (!notes && highlights.length === 0) continue;
    lines.push(`# ${title}`, "");
    if (notes) lines.push(notes, "");
    for (const h of highlights) {
      lines.push(`- "${h.quote}"${h.note ? ` — ${h.note}` : ""}`);
    }
    if (highlights.length) lines.push("");
  }
  return lines.join("\n");
}

function init() {
  const list = document.getElementById("dl-my-notes-list");
  const empty = document.getElementById("dl-my-notes-empty");
  const search = document.getElementById("dl-my-notes-search");
  const download = document.getElementById("dl-my-notes-download");
  if (!list || !empty) return;

  const titles = readTitles();
  const records = readAllRecords().sort((a, b) => {
    const ta = titles[a["tutorial-slug"] || a["tutorial-id"]] || "";
    const tb = titles[b["tutorial-slug"] || b["tutorial-id"]] || "";
    return ta.localeCompare(tb);
  });

  const NOTHING_SAVED = "Nothing saved here yet. Select any passage of text "
    + "on a tutorial page to highlight it, or write in a tutorial's own "
    + "Notes panel — it'll show up here.";

  const cardsHtml = records.map((r) => cardHtml(r, titles)).filter(Boolean);
  if (cardsHtml.length === 0) {
    empty.hidden = false;
    empty.textContent = NOTHING_SAVED;
    if (search) search.hidden = true;
    if (download) download.hidden = true;
    return;
  }
  list.innerHTML = cardsHtml.join("");

  function runFilter() {
    const query = search ? search.value : "";
    let visible = 0;
    for (const card of list.querySelectorAll(".dl-my-notes-card")) {
      const matches = !query || textMatches(card.textContent, query);
      card.hidden = !matches;
      if (matches) visible += 1;
    }
    empty.hidden = visible > 0;
    empty.textContent = query ? "Nothing here matches that." : NOTHING_SAVED;
  }
  if (search) search.addEventListener("input", runFilter);

  if (download) {
    download.addEventListener("click", () => {
      const blob = new Blob([asStudySheet(records, titles)], { type: "text/plain" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "my-dewlab-notes.txt";
      link.click();
      URL.revokeObjectURL(link.href);
    });
  }
}

init();
