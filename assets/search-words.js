// One idea of "does this word match that word", shared by every search
// box on the site: the search line on each page and the all-tutorials
// page (search.js), the Reference panel and the two Basics tabs
// (tutorial-runtime.js), dewmini's Library (compose/dewmini.js) and the
// authoring editor's link picker (editor.js). A reader who has learned
// that "loops" finds Loops and Lists in one box should not find that it
// does nothing in the next.
//
// Three things make a query word match a text word: the same word after
// stemming (loops → loop, sorting → sort), a synonym mapped to the same
// word (chance → probability), or a prefix of three letters or more
// (poly → polynomial). The filters — where a reader is narrowing a list
// they can already see — also keep plain substring matching, so a
// two-letter fragment or "print(" still narrows the way it always did.

// Small and common, not exhaustive — dropped from every field before
// matching so "the" or "of" in a title never counts as a real match.
export const STOPWORDS = new Set([
  "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is",
  "are", "with", "by", "at", "from", "your", "what", "how",
]);

// A deliberately modest set of common alternate words for
// programming/maths topics — not every synonym anyone could type, just
// the ones likely to come up. Each maps to the same normalized form a
// tutorial's own vocabulary would produce, so typing either word finds
// the same tutorials. Extend this list as a real search turns up a
// near-miss worth covering.
export const SYNONYMS = {
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

export function stem(word) {
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

export function normalizeWord(word) {
  const lower = word.toLowerCase();
  return stem(SYNONYMS[lower] || lower);
}

/** Splits free text into normalized, stopword-filtered tokens. */
export function tokenize(text) {
  const words = text.toLowerCase().match(/[a-z0-9]+/g) || [];
  return words.map(normalizeWord).filter((w) => w.length > 1 && !STOPWORDS.has(w));
}

// A query token counts as a hit against a document token if it matches
// exactly, or if it's a prefix of at least MIN_PREFIX_LENGTH characters —
// long enough to type in a hurry ("poly", "fun") without turning every
// one- or two-letter fragment into a blunt substring search.
export const MIN_PREFIX_LENGTH = 3;

export function tokenHits(docToken, queryToken) {
  return docToken === queryToken
    || (queryToken.length >= MIN_PREFIX_LENGTH && docToken.startsWith(queryToken));
}

export function fieldHasHit(docTokens, queryToken) {
  for (const docToken of docTokens) {
    if (tokenHits(docToken, queryToken)) return true;
  }
  return false;
}

/** Whether free text answers a filter query. True when the raw query is
 * a substring of the raw text (what every filter did before this
 * existed, kept so a fragment shorter than a word still narrows), or
 * when every word of the query, normalized, is a word of the text or a
 * prefix of one. An empty query matches everything. */
export function textMatches(text, query) {
  const needle = query.trim().toLowerCase();
  if (!needle) return true;
  const lower = text.toLowerCase();
  if (lower.includes(needle)) return true;
  const queryTokens = tokenize(needle);
  if (queryTokens.length === 0) return false;
  const textTokens = new Set(tokenize(lower));
  return queryTokens.every((token) => fieldHasHit(textTokens, token));
}
