/* Client-side search — assets/search.js, loaded by shell.html on every
 * page, and a no-op wherever it finds no `.dl-search` element at all. A
 * page can carry more than one: the small popover beside "All
 * tutorials" in every page's own top nav is always present, and a
 * handful of pages (the front page, "All tutorials", "Browse by topic")
 * also carry one of their own further down — each instance is wired up
 * independently, sharing only the one fetched index. No server, no
 * build-time query handling — just this file and
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

/** Where this page's own assets live, relative to it — "assets/" for a
 * root-level page, "../../assets/" for a tutorial two folders deep, and
 * so on. Read from the same manifest every tutorial page already
 * carries (readManifest() in tutorial-runtime.js reads the same
 * element; this is a separate script and small enough not to share the
 * function, just the one field it needs). Root-level pages with no
 * cells of their own still carry a manifest with assetBase set — see
 * write_index()'s own, for one. */
function assetBase() {
  const el = document.getElementById("dewlab-manifest");
  if (!el) return "assets/";
  try {
    return JSON.parse(el.textContent).assetBase || "assets/";
  } catch (e) {
    return "assets/";
  }
}

/** The same relative path back to the site root that assetBase() carries
 * (it is just assetBase() with "assets/" itself lopped off the end) —
 * every result's own `url` in the index is root-relative ("tutorials/
 * computational-methods/first-steps.html"), so a page that is not
 * itself at the root has to prefix it with this before using it. */
function rootBase() {
  return assetBase().replace(/assets\/$/, "");
}

/** Fetches and prepares the search index once — each document gets its
 * three token sets precomputed here rather than re-tokenized on every
 * keystroke, since the index itself never changes during a page visit. */
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

/** Wires up one `.dl-search` instance — everything that used to be the
 * whole of initSearch(), before a page could carry more than one at
 * once (the nav popover beside "All tutorials", present everywhere,
 * plus a handful of pages' own body copy). `documents`/`loadError` are
 * the one shared fetch every instance on the page reads from, not
 * fetched again per instance. */
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

/** Loads the index once, then wires up every `.dl-search` box the page
 * carries — the nav popover beside "All tutorials" is on every page, so
 * this always finds at least one. */
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
