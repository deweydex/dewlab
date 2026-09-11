
// Small and common, not exhaustive — dropped from every field before
// matching so "the" or "of" in a title never counts as a real match.
const STOPWORDS = new Set([
  "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is",
  "are", "with", "by", "at", "from", "your", "what", "how",
]);

// A deliberately modest set of common alternate words for
// programming/maths topics — not every synonym anyone could type, just
// the ones likely to come up. Each maps to the same normalized form a
// tutorial's own vocabulary would produce, so typing either word finds
// the same tutorials. Extend this list as a real search turns up a
// near-miss worth covering.
const SYNONYMS = {
  loop: "iterate", loops: "iterate", looping: "iterate", iteration: "iterate", iterating: "iterate",
  func: "function", funcs: "function", method: "function", methods: "function",
  array: "list", arrays: "list",
  chance: "probability", odds: "probability", likelihood: "probability",
  avg: "average", mean: "average",
  add: "addition", adding: "addition", plus: "addition", sum: "addition",
  subtract: "subtraction", subtracting: "subtraction", minus: "subtraction",
  multiply: "multiplication", multiplying: "multiplication", times: "multiplication",
  divide: "division", dividing: "division",
  graph: "plot", chart: "plot", graphing: "plot", charting: "plot",
  db: "database", sql: "database",
  sort: "sort", sorted: "sort", sorting: "sort",
  condition: "conditional", conditions: "conditional",
  dict: "dictionary", dicts: "dictionary",
  regex: "regularexpression", regexp: "regularexpression",
  matrices: "matrix",
};

function stem(word) {
  if (word.length > 5) {
    if (word.endsWith("ing")) return word.slice(0, -3);
    if (word.endsWith("ies")) return word.slice(0, -3) + "y";
    if (word.endsWith("ied")) return word.slice(0, -3) + "y";
    if (word.endsWith("ers")) return word.slice(0, -3);
    if (word.endsWith("es")) return word.slice(0, -2);
    if (word.endsWith("ed")) return word.slice(0, -2);
  }
  if (word.length > 4 && word.endsWith("s") && !word.endsWith("ss")) return word.slice(0, -1);
  return word;
}

function normalizeWord(word) {
  const lower = word.toLowerCase();
  return stem(SYNONYMS[lower] || lower);
}

/** Splits free text into normalized, stopword-filtered tokens. */
function tokenize(text) {
  const words = text.toLowerCase().match(/[a-z0-9]+/g) || [];
  return words.map(normalizeWord).filter((w) => w.length > 1 && !STOPWORDS.has(w));
}

function scoreDocument(doc, queryTokens) {
  if (queryTokens.length === 0) return 0;
  let score = 0;
  for (const token of queryTokens) {
    if (doc._titleTokens.has(token)) score += 3;
    if (doc._termTokens.has(token)) score += 2;
    if (doc._contextTokens.has(token)) score += 1;
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
    const matchedTerms = doc.terms.filter((term) => tokenize(term).some((t) => queryTokens.includes(t)));
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
  // (Settings, Help) — a search box left open after a reader has
  // clicked elsewhere would be the odd one out. The nav popover is a
  // <details> rather than one of those panels, so it gets the same
  // treatment applied to itself, not just to its results list: native
  // <details> has no built-in "close on outside click" or Escape of its
  // own, and leaving those out here would make this the one panel on
  // the page that does not behave like the rest.
  const popover = root.closest("details.dl-nav-search");
  document.addEventListener("click", (e) => {
    if (root.contains(e.target)) return;
    list.hidden = true;
    if (popover && !popover.contains(e.target)) popover.open = false;
  });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape" || !popover || !popover.open) return;
    popover.open = false;
    popover.querySelector("summary").focus();
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
