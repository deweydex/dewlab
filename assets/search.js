
// What a word is and when two words match — shared with every other
// search box on the site, so they all agree (search-words.js).
import { tokenize, tokenHits, fieldHasHit } from "./search-words.js";

function scoreDocument(doc, queryTokens) {
  if (queryTokens.length === 0) return 0;
  let score = 0;
  for (const token of queryTokens) {
    if (fieldHasHit(doc._titleTokens, token)) score += 3;
    if (fieldHasHit(doc._termTokens, token)) score += 2;
    if (fieldHasHit(doc._contextTokens, token)) score += 1;
  }
  return score;
}

function assetBase() {
  const el = document.getElementById("dewlab-manifest");
  if (!el) return "assets/";
  try {
    return JSON.parse(el.textContent).assetBase || "assets/";
  } catch (e) {
    return "assets/";
  }
}

function rootBase() {
  return assetBase().replace(/assets\/$/, "");
}

async function loadIndex() {
  const response = await fetch(assetBase() + "search-index.json");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const documents = await response.json();
  for (const doc of documents) {
    doc._titleTokens = new Set(tokenize(doc.title));
    doc._termTokens = new Set(doc.terms.flatMap(tokenize));
    doc._contextTokens = new Set(tokenize(`${doc.moduleTitle} ${doc.series}`));
  }
  return documents;
}

function renderResults(listEl, ranked, queryTokens, limit = 12) {
  if (ranked.length === 0) {
    listEl.innerHTML = '<li class="dl-search-empty">No tutorial matches that yet — try a different word.</li>';
    listEl.hidden = false;
    return;
  }
  const rows = ranked.slice(0, limit).map(({ doc }) => {
    const matchedTerms = doc.terms.filter((term) =>
      tokenize(term).some((t) => queryTokens.some((q) => tokenHits(t, q))));
    const subtitle = [doc.moduleTitle, doc.series].filter(Boolean).join(" — ");
    const matchNote = matchedTerms.length
      ? `<span class="dl-search-match">${matchedTerms.slice(0, 3).map(escapeHtml).join(", ")}</span>`
      : "";
    return (
      `<li><a href="${rootBase()}${doc.url}">` +
      `<span class="dl-search-title">${escapeHtml(doc.title)}</span>` +
      `<span class="dl-search-subtitle">${escapeHtml(subtitle)}</span>` +
      matchNote +
      "</a></li>"
    );
  });
  listEl.innerHTML = rows.join("");
  listEl.hidden = false;
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function wireSearchBox(root, documents, loadError) {
  const input = root.querySelector(".dl-search-input");
  const list = root.querySelector(".dl-search-results");
  if (!input || !list) return;

  const runSearch = () => {
    const query = input.value.trim();
    if (!query) {
      list.hidden = true;
      list.innerHTML = "";
      return;
    }
    if (loadError || !documents) {
      list.innerHTML = '<li class="dl-search-empty">Search isn\'t available right now.</li>';
      list.hidden = false;
      return;
    }
    const queryTokens = tokenize(query);
    const ranked = documents
      .map((doc) => ({ doc, score: scoreDocument(doc, queryTokens) }))
      .filter((entry) => entry.score > 0)
      .sort((a, b) => b.score - a.score || a.doc.title.localeCompare(b.doc.title));
    renderResults(list, ranked, queryTokens);
  };

  // Debounced, not on every raw keystroke — tokenizing and scoring
  // every document is cheap, but there is no reason to redo it for a
  // character that is about to be replaced by the next one anyway.
  let debounceTimer = null;
  input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(runSearch, 120);
  });

  // Enter jumps straight to the top result, the same shortcut a reader
  // would expect from any other search box.
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const firstLink = list.querySelector("a");
      if (firstLink) { e.preventDefault(); firstLink.click(); }
    } else if (e.key === "Escape") {
      input.value = "";
      list.hidden = true;
      list.innerHTML = "";
    }
  });

  // Closing on an outside click matches every other panel on the site
  // (Settings, Help) — a results list left open after a reader has
  // clicked elsewhere would be the odd one out.
  document.addEventListener("click", (e) => {
    if (root.contains(e.target)) return;
    list.hidden = true;
  });
  input.addEventListener("focus", () => { if (input.value.trim()) list.hidden = false; });
}

async function initSearch() {
  const roots = document.querySelectorAll(".dl-search");
  if (roots.length === 0) return;

  let documents = null;
  let loadError = null;
  try {
    documents = await loadIndex();
  } catch (error) {
    loadError = error;
  }

  for (const root of roots) wireSearchBox(root, documents, loadError);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSearch);
} else {
  initSearch();
}
