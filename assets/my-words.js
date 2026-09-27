/* My words (#340): a reader's own word list.
 *
 * A reader selects a word on any page and keeps it with their own meaning
 * or translation. The list lives in this browser under one key for the
 * whole site, the way Notes live per page, so a word saved on one page is
 * known on every other. Where a word appears again, its first use in each
 * paragraph is marked quietly, and pointing at it, tapping it or tabbing
 * to it shows the reader's own meaning.
 *
 * Unlike term-definitions.js, this searches the prose for words. 7.94
 * withdrew that for glossary terms because a regex cannot tell "set a seed"
 * from a set. Here the reader chose the word and wrote its meaning, so a
 * mark in the other sense shows them their own words, which they can judge;
 * it never shows the site's definition as if it applied.
 *
 * A mark wraps the matched text in a <span>. Highlights anchor to text
 * offsets inside a block (tutorial-runtime.js, rangeForOffsets()), and a
 * span adds no text, so they are unaffected. Nothing is marked inside
 * code, cells, maths, headings, links, buttons, or a term the author
 * already marked for its definition. */

import { entryFor } from "./term-definitions.js";
import { textMatches } from "./search-words.js";

export const WORDS_KEY = "dewlab:my-words";
const MARKS_KEY = "dewlab:my-words-marks";
const SORT_KEY = "dewlab:my-words-sort";

const PROSE_BLOCKS = "p, li, td, th, blockquote, dt, dd";
const NEVER = [
  "pre", "code", ".dl-cell", ".dl-output", ".dl-editor", ".dl-math", ".katex",
  "h1", "h2", "h3", "h4", "h5", "h6", "a", "button", "summary", "label",
  "input", "textarea", "select", ".dl-reference", ".dl-compare", ".dl-def",
  ".dl-myword", ".dl-world-chooser", ".dl-challenge", ".dl-sr-only",
].join(", ");

/* How much of a selection counts as a word or a short phrase. */
const LONGEST_WORD = 60;
const MOST_WORDS = 5;
/* How much of the text around a word is kept with it. */
const LONGEST_SENTENCE = 300;
/* What an imported entry's fields may hold. */
const LIMITS = { word: LONGEST_WORD, meaning: 2000, sentence: LONGEST_SENTENCE, page: 200, title: 300, path: 500, term: 200, definition: 2000 };

export function readMarksSetting() {
  try { return localStorage.getItem(MARKS_KEY) !== "off"; } catch (err) { return true; }
}

export function writeMarksSetting(mode) {
  try { localStorage.setItem(MARKS_KEY, mode); } catch (err) { /* private mode */ }
}

export function readWords() {
  try {
    const parsed = JSON.parse(localStorage.getItem(WORDS_KEY) || "null");
    const list = parsed && Array.isArray(parsed.words) ? parsed.words : [];
    return list.map(clean).filter(Boolean);
  } catch (err) {
    return [];
  }
}

function writeWords(words) {
  try {
    localStorage.setItem(WORDS_KEY, JSON.stringify({ version: 1, words }));
    return true;
  } catch (err) {
    return false;
  }
}

/* An entry as stored, with every field a string of a sensible length, or
 * null if it has no word. Also what an imported file's entries go through,
 * so a file made by hand cannot put anything else into the list. */
function clean(raw) {
  if (!raw || typeof raw !== "object") return null;
  const entry = {};
  for (const [field, limit] of Object.entries(LIMITS)) {
    const value = raw[field];
    entry[field] = typeof value === "string" ? value.slice(0, limit) : "";
  }
  entry.word = tidyWord(entry.word);
  if (!entry.word) return null;
  entry.id = typeof raw.id === "string" && raw.id ? raw.id.slice(0, 60) : newId();
  entry.created = typeof raw.created === "string" ? raw.created.slice(0, 40) : new Date().toISOString();
  entry.updated = typeof raw.updated === "string" ? raw.updated.slice(0, 40) : entry.created;
  return entry;
}

function newId() {
  return `w-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

/* The word without the punctuation a drag picks up at either end. */
function tidyWord(text) {
  return String(text || "")
    .replace(/\s+/g, " ")
    .replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "")
    .trim();
}

function sameWord(a, b) {
  return a.toLocaleLowerCase() === b.toLocaleLowerCase();
}

/* A selection worth offering to save: a word or a short phrase. */
export function wordFromSelection(text) {
  const word = tidyWord(text);
  if (word.length < 2 || word.length > LONGEST_WORD) return "";
  if (word.split(" ").length > MOST_WORDS) return "";
  return word;
}

/* The sentence around a selection, from its block's own text. */
export function sentenceAround(block, range) {
  const before = document.createRange();
  before.selectNodeContents(block);
  before.setEnd(range.startContainer, range.startOffset);
  const start = before.toString().length;
  const end = start + range.toString().length;
  const text = block.textContent;
  let from = 0;
  const enders = /[.!?](?=\s)/g;
  let match;
  while ((match = enders.exec(text)) && match.index < start) from = match.index + 1;
  enders.lastIndex = end;
  const after = enders.exec(text);
  let sentence = text.slice(from, after ? after.index + 1 : text.length).replace(/\s+/g, " ").trim();
  if (sentence.length > LONGEST_SENTENCE) {
    const at = Math.max(0, start - from - 120);
    sentence = `…${sentence.slice(at, at + LONGEST_SENTENCE - 2).trim()}…`;
  }
  return sentence;
}

function escapeRegex(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/* One pattern for every saved word, longest first, so a phrase wins over a
 * word inside it. A word matches whole, in any case, and a plain plural
 * of its last word counts, as the Reference allows. */
function patternFor(entries) {
  const sorted = [...entries].sort((a, b) => b.word.length - a.word.length);
  if (!sorted.length) return null;
  const groups = sorted.map((entry) => {
    const parts = entry.word.split(" ").map(escapeRegex);
    return `(${parts.join("\\s+")}(?:e?s)?)`;
  });
  return { sorted, regex: new RegExp(`(?<![\\p{L}\\p{N}_])(?:${groups.join("|")})(?![\\p{L}\\p{N}_])`, "giu") };
}

/* Sets up the list, its section in the Notes panel, the marks on the page,
 * the file export and import, and the popover a mark opens. Returns
 * { add(word, sentence), refresh() }. */
export function initMyWords({ body, manifest, openPanel }) {
  const glossary = ((manifest && manifest.glossary) || []).filter((entry) => entry.term && entry.definition);
  const page = pageInfo(manifest);

  const section = document.getElementById("dl-settings-words");
  const form = document.getElementById("dl-word-form");
  const wordInput = document.getElementById("dl-word-input");
  const meaningInput = document.getElementById("dl-word-meaning");
  const sentenceEl = document.getElementById("dl-word-sentence");
  const definitionEl = document.getElementById("dl-word-definition");
  const formNote = document.getElementById("dl-word-form-note");
  const cancel = document.getElementById("dl-word-cancel");
  const search = document.getElementById("dl-words-search");
  const sortControl = document.querySelector("[data-words-sort]");
  const status = document.getElementById("dl-words-status");
  const list = document.getElementById("dl-words-list");

  let editing = null;   // the entry the form is changing, or a new one

  /* ---------- the form ---------- */

  function openForm(entry, note) {
    if (!form) return;
    editing = entry;
    wordInput.value = entry.word;
    meaningInput.value = entry.meaning || "";
    sentenceEl.hidden = !entry.sentence;
    sentenceEl.textContent = entry.sentence ? `“${entry.sentence}”` : "";
    definitionEl.hidden = !entry.definition;
    definitionEl.textContent = entry.definition ? `In the Reference: ${entry.definition}` : "";
    formNote.textContent = note || "";
    formNote.hidden = !note;
    form.hidden = false;
    if (openPanel) openPanel();
    form.scrollIntoView({ block: "nearest" });
    meaningInput.focus();
  }

  function closeForm() {
    if (!form) return;
    editing = null;
    form.hidden = true;
  }

  function add(text, sentence) {
    const word = wordFromSelection(text);
    if (!word) return;
    const existing = readWords().find((entry) => sameWord(entry.word, word));
    if (existing) {
      const where = existing.title ? ` on “${existing.title}”` : "";
      openForm(existing, `You saved this word before${where}. You can change your meaning here.`);
      return;
    }
    const found = glossary.length ? entryFor(word, glossary) : null;
    // A table cell or a list item can hold only the word, and a sentence
    // that says the word again adds nothing.
    const context = sentence && !sameWord(tidyWord(sentence), word) ? sentence : "";
    openForm({
      id: "",
      word,
      meaning: "",
      sentence: context,
      page: page.slug,
      title: page.title,
      path: page.path,
      term: found ? found.term : "",
      definition: found ? String(found.definition).trim() : "",
    });
  }

  if (form) {
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      if (!editing) return;
      const word = tidyWord(wordInput.value);
      if (!word) { wordInput.focus(); return; }
      const now = new Date().toISOString();
      const words = readWords();
      const entry = clean({ ...editing, word, meaning: meaningInput.value.trim(), updated: now,
        created: editing.created || now, id: editing.id || newId() });
      const at = words.findIndex((other) => other.id === entry.id);
      if (at >= 0) words[at] = entry; else words.push(entry);
      if (!writeWords(words)) {
        formNote.textContent = "This browser would not save the word. Its storage may be full.";
        formNote.hidden = false;
        return;
      }
      closeForm();
      refresh();
    });
    cancel.addEventListener("click", closeForm);
  }

  /* ---------- the list ---------- */

  function readSort() {
    try { return localStorage.getItem(SORT_KEY) === "az" ? "az" : "page"; } catch (err) { return "page"; }
  }

  function syncSort() {
    if (!sortControl) return;
    const mode = readSort();
    for (const btn of sortControl.querySelectorAll("button")) {
      const on = btn.dataset.value === mode;
      btn.setAttribute("aria-checked", on ? "true" : "false");
      btn.tabIndex = on ? 0 : -1;
    }
  }

  function byWord(a, b) {
    return a.word.localeCompare(b.word, undefined, { sensitivity: "base" });
  }

  function pageHref(entry) {
    if (!entry.path) return "";
    try { return new URL(entry.path, page.root).href; } catch (err) { return ""; }
  }

  function renderItem(entry) {
    const item = document.createElement("li");
    item.className = "dl-word-item";
    item.dataset.wordId = entry.id;
    const head = document.createElement("p");
    head.className = "dl-word-head";
    const word = document.createElement("strong");
    word.textContent = entry.word;
    head.append(word);
    item.append(head);
    const meaning = document.createElement("p");
    meaning.className = "dl-word-meaning";
    meaning.textContent = entry.meaning || "No meaning written yet.";
    if (!entry.meaning) meaning.classList.add("dl-word-empty");
    item.append(meaning);
    if (entry.sentence) {
      const sentence = document.createElement("p");
      sentence.className = "dl-word-sentence";
      sentence.textContent = `“${entry.sentence}”`;
      item.append(sentence);
    }
    if (entry.definition) {
      const definition = document.createElement("p");
      definition.className = "dl-word-definition";
      definition.textContent = `In the Reference: ${entry.definition}`;
      item.append(definition);
    }
    const actions = document.createElement("p");
    actions.className = "dl-word-actions";
    const href = pageHref(entry);
    if (href && entry.title && readSort() === "az") {
      const link = document.createElement("a");
      link.href = href;
      link.textContent = entry.title;
      actions.append(link, " ");
    }
    const edit = document.createElement("button");
    edit.type = "button";
    edit.className = "dl-btn dl-word-edit";
    edit.textContent = "Change";
    edit.setAttribute("aria-label", `Change ${entry.word}`);
    edit.addEventListener("click", () => openForm(entry));
    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "dl-btn dl-word-delete";
    remove.textContent = "Delete";
    remove.setAttribute("aria-label", `Delete ${entry.word}`);
    remove.addEventListener("click", () => {
      writeWords(readWords().filter((other) => other.id !== entry.id));
      if (editing && editing.id === entry.id) closeForm();
      refresh();
    });
    actions.append(edit, " ", remove);
    item.append(actions);
    return item;
  }

  function renderList() {
    if (!list) return;
    const all = readWords();
    const query = search ? search.value : "";
    const shown = all.filter((entry) => !query.trim()
      || textMatches([entry.word, entry.meaning, entry.sentence, entry.title].join(" "), query));
    list.replaceChildren();
    if (!all.length) {
      status.textContent = "No words saved yet.";
    } else if (!shown.length) {
      status.textContent = "No word matches your search.";
    } else {
      status.textContent = all.length === 1 ? "1 word." : `${all.length} words.`;
    }
    if (readSort() === "az") {
      for (const entry of shown.sort(byWord)) list.append(renderItem(entry));
      return;
    }
    const groups = new Map();
    for (const entry of shown) {
      const key = entry.title || entry.page || "";
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(entry);
    }
    const titles = [...groups.keys()].sort((a, b) => a.localeCompare(b, undefined, { sensitivity: "base" }));
    for (const title of titles) {
      const entries = groups.get(title);
      const group = document.createElement("li");
      group.className = "dl-word-group";
      const heading = document.createElement("p");
      heading.className = "dl-word-page";
      const href = pageHref(entries[0]);
      if (href && title) {
        const link = document.createElement("a");
        link.href = href;
        link.textContent = title;
        heading.append(link);
      } else {
        heading.textContent = title || "A page with no title";
      }
      const inner = document.createElement("ul");
      inner.className = "dl-words-list";
      for (const entry of entries.sort((a, b) => a.created.localeCompare(b.created))) inner.append(renderItem(entry));
      group.append(heading, inner);
      list.append(group);
    }
  }

  if (search) search.addEventListener("input", renderList);
  if (sortControl) {
    sortControl.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      try { localStorage.setItem(SORT_KEY, btn.dataset.value); } catch (err) { /* private mode */ }
      syncSort();
      renderList();
    });
  }

  /* ---------- marks on the page ---------- */

  const texts = document.createElement("div");
  texts.hidden = true;
  texts.id = "dl-myword-texts";
  document.body.append(texts);

  const popover = document.createElement("div");
  popover.className = "dl-myword-popover";
  popover.hidden = true;
  popover.setAttribute("aria-hidden", "true");
  const popWord = document.createElement("strong");
  const popMeaning = document.createElement("p");
  const popChange = document.createElement("button");
  popChange.type = "button";
  popChange.tabIndex = -1;
  popChange.textContent = "Change it in My words";
  popover.append(popWord, popMeaning, popChange);
  document.body.append(popover);

  let shownFor = null;
  let hideTimer = null;

  function place(target) {
    const rect = target.getBoundingClientRect();
    const margin = 8;
    popover.style.left = "0px";
    popover.style.top = "0px";
    const width = popover.offsetWidth;
    const height = popover.offsetHeight;
    const left = Math.max(margin, Math.min(rect.left, window.innerWidth - width - margin));
    const below = rect.bottom + 6;
    const top = below + height + margin > window.innerHeight ? Math.max(margin, rect.top - height - 6) : below;
    popover.style.left = `${left}px`;
    popover.style.top = `${top}px`;
  }

  function show(span) {
    clearTimeout(hideTimer);
    const entry = span.dlWord;
    if (!entry) return;
    popWord.textContent = entry.word;
    popMeaning.textContent = entry.meaning || "No meaning written yet.";
    popover.hidden = false;
    shownFor = span;
    place(span);
  }

  function hide() {
    clearTimeout(hideTimer);
    popover.hidden = true;
    shownFor = null;
  }

  function hideSoon() {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(hide, 200);
  }

  popover.addEventListener("pointerenter", () => clearTimeout(hideTimer));
  popover.addEventListener("pointerleave", hideSoon);
  popChange.addEventListener("click", () => {
    const entry = shownFor && shownFor.dlWord;
    hide();
    if (entry) openForm(entry);
  });
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") hide(); });
  document.addEventListener("scroll", () => { if (shownFor && !popover.hidden) place(shownFor); }, { passive: true });
  document.addEventListener("pointerdown", (ev) => {
    if (shownFor && !shownFor.contains(ev.target) && !popover.contains(ev.target)) hide();
  });

  function wire(span) {
    span.addEventListener("pointerenter", (ev) => { if (ev.pointerType === "mouse") show(span); });
    span.addEventListener("pointerleave", (ev) => { if (ev.pointerType === "mouse") hideSoon(); });
    span.addEventListener("focus", () => show(span));
    span.addEventListener("blur", hideSoon);
    // A click inside a highlight belongs to the highlight's own popover.
    span.addEventListener("click", () => {
      if (!span.closest("mark.dl-highlight") && !span.querySelector("mark.dl-highlight")) show(span);
    });
    span.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") {
        ev.preventDefault();
        const entry = span.dlWord;
        hide();
        if (entry) openForm(entry);
      }
    });
  }

  function unmark() {
    for (const span of [...body.querySelectorAll("span.dl-myword")]) {
      const parent = span.parentNode;
      while (span.firstChild) parent.insertBefore(span.firstChild, span);
      parent.removeChild(span);
      parent.normalize();
    }
    texts.replaceChildren();
    hide();
  }

  function mark(entries) {
    const found = patternFor(entries);
    if (!found) return;
    const descriptions = new Map();
    found.sorted.forEach((entry, index) => {
      const p = document.createElement("p");
      p.id = `dl-myword-${index}`;
      p.textContent = entry.meaning ? `Your meaning: ${entry.meaning}` : "In My words, with no meaning written yet.";
      texts.append(p);
      descriptions.set(entry, p.id);
    });

    const nodes = [];
    const walker = document.createTreeWalker(body, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent || !node.data.trim()) return NodeFilter.FILTER_REJECT;
        if (parent.closest(NEVER) || !parent.closest(PROSE_BLOCKS)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    while (walker.nextNode()) nodes.push(walker.currentNode);

    const done = new Map();   // block -> the entries already marked in it
    for (const node of nodes) {
      const block = node.parentElement.closest(PROSE_BLOCKS);
      if (!done.has(block)) done.set(block, new Set());
      const marked = done.get(block);
      const hits = [];
      found.regex.lastIndex = 0;
      let match;
      while ((match = found.regex.exec(node.data))) {
        const group = match.slice(1).findIndex((value) => value !== undefined);
        const entry = found.sorted[group];
        if (!entry || marked.has(entry)) continue;
        marked.add(entry);
        hits.push({ start: match.index, end: match.index + match[0].length, entry });
      }
      // Last first, so the earlier offsets in this text node stay true.
      for (const hit of hits.reverse()) {
        const range = document.createRange();
        range.setStart(node, hit.start);
        range.setEnd(node, hit.end);
        const span = document.createElement("span");
        span.className = "dl-myword";
        span.tabIndex = 0;
        span.dlWord = hit.entry;
        span.setAttribute("aria-describedby", descriptions.get(hit.entry));
        range.surroundContents(span);
        wire(span);
      }
    }
  }

  function refresh() {
    unmark();
    const words = readWords();
    if (readMarksSetting() && words.length) mark(words);
    renderList();
  }

  /* ---------- export and import ---------- */

  const exportButton = document.getElementById("dl-words-export");
  const importButton = document.getElementById("dl-words-import");
  const fileInput = document.getElementById("dl-words-file");
  const ioStatus = document.getElementById("dl-words-io-status");

  function say(text) {
    if (ioStatus) ioStatus.textContent = text;
  }

  if (exportButton) {
    exportButton.addEventListener("click", () => {
      const words = readWords();
      const file = { dewlab: "my-words", version: 1, exported: new Date().toISOString(), words };
      const blob = new Blob([JSON.stringify(file, null, 2)], { type: "application/json" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "my-dewlab-words.json";
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(link.href), 1000);
      say(words.length === 1 ? "Exported 1 word." : `Exported ${words.length} words.`);
    });
  }

  if (importButton && fileInput) {
    importButton.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", async () => {
      const chosen = fileInput.files && fileInput.files[0];
      fileInput.value = "";
      if (!chosen) return;
      let incoming;
      try {
        const parsed = JSON.parse(await chosen.text());
        incoming = parsed && parsed.dewlab === "my-words" && Array.isArray(parsed.words) ? parsed.words : null;
      } catch (err) {
        incoming = null;
      }
      if (!incoming) {
        say("That file is not a copy of My words. Nothing was changed.");
        return;
      }
      const result = mergeWords(readWords(), incoming);
      if (!writeWords(result.words)) {
        say("This browser would not save the words. Its storage may be full.");
        return;
      }
      refresh();
      const parts = [];
      parts.push(result.added === 1 ? "Added 1 word" : `Added ${result.added} words`);
      if (result.updated) parts.push(result.updated === 1 ? "updated 1" : `updated ${result.updated}`);
      say(`${parts.join(" and ")}.`);
    });
  }

  /* Another tab changed the list: show it here too. */
  window.addEventListener("storage", (ev) => {
    if (ev.key === WORDS_KEY || ev.key === MARKS_KEY) refresh();
  });

  syncSort();
  refresh();
  if (section) section.hidden = false;
  return { add, refresh, renderList };
}

/* The words in a file, added to the list. A word already in the list,
 * with the same id, keeps whichever copy was changed last. */
export function mergeWords(current, incoming) {
  const words = [...current];
  let added = 0;
  let updated = 0;
  for (const raw of incoming) {
    const entry = clean(raw);
    if (!entry) continue;
    const at = words.findIndex((other) => other.id === entry.id);
    if (at < 0) {
      words.push(entry);
      added += 1;
    } else if (entry.updated > words[at].updated) {
      words[at] = entry;
      updated += 1;
    }
  }
  return { words, added, updated };
}

/* This page's id, title and address from the site's root, so the list can
 * link back to it from any other page. */
function pageInfo(manifest) {
  const slug = (manifest && (manifest.slug || manifest.id)) || "";
  const heading = document.querySelector("#dl-body h1") || document.querySelector("h1");
  const title = (heading ? heading.textContent : document.title.replace(/\s+—\s+dewlab$/, "")).replace(/\s+/g, " ").trim();
  let root;
  try {
    const assetBase = (manifest && manifest.assetBase) || "assets/";
    root = new URL(assetBase.replace(/assets\/?$/, "") || "./", location.href);
  } catch (err) {
    root = new URL("./", location.href);
  }
  const path = location.pathname.startsWith(root.pathname)
    ? location.pathname.slice(root.pathname.length)
    : location.pathname.replace(/^\//, "");
  return { slug, title, path, root };
}
