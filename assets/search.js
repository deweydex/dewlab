/* Client-side search for the contents page and "Browse by topic" —
 * assets/search.js, loaded by both (build.py's write_index() and
 * write_topics_page(), via {{PAGE_SCRIPT}}) and a no-op anywhere else,
 * since it only ever does anything once it finds #dl-search in the
 * page. No server, no build-time query handling — just this file and
 * assets/search-index.json (one row per live tutorial: title, module,
 * series, and the glossary terms that tutorial specifically introduces
 * — write_search_index() in build.py generates it fresh on every
 * build, so it can never drift from the tutorials actually shipped).
 *
 * Matching is deliberately simple, not a real search engine: normalize
 * every word (lower-case, a light suffix-stripping stemmer, a small
 * synonym table), then score each tutorial by how many of the query's
 * normalized words it shares, weighted by which field they matched in
 * (title counts for more than a glossary term, which counts for more
 * than the module/series name). Good enough for a few dozen to a few
 * hundred tutorials; not attempting to be good enough for the open web.
 */

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

/** A light, rule-based stemmer — not Porter's full algorithm, just the
 * common English suffixes worth stripping so "sorting"/"sorted"/"sorts"
 * all normalize to the same token as "sort". Deliberately conservative
 * (only touches words long enough that stripping a suffix is unlikely
 * to collide two unrelated words) rather than aggressive. */
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

/** Lower-case, apply the synonym table, then stem — the one normalizer
 * both the index (built once, at load) and every query (on every
 * keystroke) run every word through, so "Loops" in a query and
 * "iterating" in a tutorial's own glossary land on the same token. */
function normalizeWord(word) {
  const lower = word.toLowerCase();
  return stem(SYNONYMS[lower] || lower);
}

/** Splits free text into normalized, stopword-filtered tokens. */
function tokenize(text) {
  const words = text.toLowerCase().match(/[a-z0-9]+/g) || [];
  return words.map(normalizeWord).filter((w) => w.length > 1 && !STOPWORDS.has(w));
}

/** Scores one document against a query's already-tokenized words.
 * Three fields, three weights: a hit in the title counts for more than
 * a hit among the terms this tutorial specifically introduces, which
 * counts for more than a hit in its module or series name — a search
 * for "loop" should put a tutorial titled "Loops" ahead of one that
 * merely lives in a module called "Repeating Yourself". */
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

/** Fetches and prepares the search index once — each document gets its
 * three token sets precomputed here rather than re-tokenized on every
 * keystroke, since the index itself never changes during a page visit. */
async function loadIndex() {
  const response = await fetch("assets/search-index.json");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const documents = await response.json();
  for (const doc of documents) {
    doc._titleTokens = new Set(tokenize(doc.title));
    doc._termTokens = new Set(doc.terms.flatMap(tokenize));
    doc._contextTokens = new Set(tokenize(`${doc.moduleTitle} ${doc.series}`));
  }
  return documents;
}

/** Renders up to `limit` ranked results into the results <ul>. Each
 * result shows which of its own terms actually matched, when any did
 * — the part of a result that explains *why* it's here, not just that
 * it is. */
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
      `<li><a href="${doc.url}">` +
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

async function initSearch() {
  const root = document.getElementById("dl-search");
  if (!root) return; // this page has no search box — nothing to do

  const input = document.getElementById("dl-search-input");
  const list = document.getElementById("dl-search-results");
  if (!input || !list) return;

  let documents = null;
  let loadError = null;
  try {
    documents = await loadIndex();
  } catch (error) {
    loadError = error;
  }

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
  // clicked elsewhere would be the odd one out.
  document.addEventListener("click", (e) => {
    if (!root.contains(e.target)) { list.hidden = true; }
  });
  input.addEventListener("focus", () => { if (input.value.trim()) list.hidden = false; });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSearch);
} else {
  initSearch();
}
