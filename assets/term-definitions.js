/* Definitions on hover (#339; DECISIONS_LOG 7.272).
 *
 * A term shows its glossary definition on hover, tap or keyboard focus,
 * but only where the author marked it as the term. That means one of two
 * places: the italicised first use (docs/WRITING_TUTORIALS.md#marking-a-term),
 * or a later use marked `*term*{.term}`. Nothing here searches the prose
 * for a term's words. That was built once as prose-linking and withdrawn
 * (7.94), because a regex cannot tell the everyday "set a seed" from a set.
 * An italic the author wrote as the term is the term, in that sense.
 *
 * Marking adds attributes to the author's own <em> and never wraps text,
 * so highlights, which anchor to text offsets, are untouched. Only
 * `concept` entries are marked; formulas and function names live in maths
 * and code, which are never marked. */

import { tokenize } from "./search-words.js";

const SETTING_KEY = "dewlab:definitions";

/* Places an italic is not reading prose, or is already interactive. */
const NEVER = "pre, code, .dl-cell, .dl-output, .dl-math, .katex, h1, h2, h3, h4, h5, h6, a, button, summary, .dl-reference, .dl-compare";

export function readDefinitionsSetting() {
  try {
    return localStorage.getItem(SETTING_KEY) !== "off";
  } catch (err) {
    return true;
  }
}

export function writeDefinitionsSetting(mode) {
  try { localStorage.setItem(SETTING_KEY, mode); } catch (err) { /* private mode */ }
}

function normalise(text) {
  return String(text).toLowerCase().replace(/\s+/g, " ").trim();
}

/* The entry an italic names, or null: the whole italic, compared with a
 * term or with one part of a term that lists two ("transistor, Moore's
 * law"), exactly first, then word for word through the site's own
 * stemming, so *iterations* finds "iteration". Never a word inside a longer
 * italic, and never a prefix (*set* is not "setup"): either is where a
 * wrong sense gets in. */
export function entryFor(text, entries) {
  const needle = normalise(text);
  if (needle.length < 2) return null;
  const parts = entries.map((entry) => [entry, entry.term.split(",").map(normalise).filter(Boolean)]);
  for (const [entry, names] of parts) if (names.includes(needle)) return entry;
  const needleTokens = tokenize(needle);
  if (!needleTokens.length) return null;
  for (const [entry, names] of parts) {
    for (const name of names) {
      const tokens = tokenize(name);
      if (tokens.length === needleTokens.length
        && tokens.every((token, i) => token === needleTokens[i])) {
        return entry;
      }
    }
  }
  return null;
}

/* Marks the page's term italics and wires one shared popover. Returns an
 * object whose `refresh()` marks or unmarks to match the setting.
 * `openReference(term)` opens the Reference panel at an entry. */
export function initTermDefinitions({ body, glossary, openReference }) {
  const entries = (glossary || []).filter((entry) => entry.kind === "concept" && entry.term && entry.definition);
  if (!body || !entries.length) return { refresh() {} };

  /* One hidden description per entry, shared by every italic naming it,
   * for screen readers (aria-describedby reads hidden text). */
  const texts = document.createElement("div");
  texts.hidden = true;
  texts.id = "dl-def-texts";
  const descriptionIds = new Map();
  entries.forEach((entry, index) => {
    const p = document.createElement("p");
    p.id = `dl-def-${index}`;
    p.textContent = entry.definition.trim();
    texts.append(p);
    descriptionIds.set(entry, p.id);
  });
  document.body.append(texts);

  /* Visual only: a screen reader already has the definition through
   * aria-describedby, and the keyboard's way to the Reference is Enter on
   * the term itself, so the popover never takes focus. */
  const popover = document.createElement("div");
  popover.className = "dl-def-popover";
  popover.hidden = true;
  popover.setAttribute("aria-hidden", "true");
  const popTerm = document.createElement("strong");
  const popText = document.createElement("p");
  const popMore = document.createElement("button");
  popMore.type = "button";
  popMore.tabIndex = -1;
  popMore.textContent = "More in the Reference";
  popover.append(popTerm, popText, popMore);
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

  function show(target) {
    clearTimeout(hideTimer);
    const entry = target.dlEntry;
    if (!entry) return;
    popTerm.textContent = entry.term;
    popText.textContent = entry.definition.trim();
    popMore.dataset.term = entry.term;
    popover.hidden = false;
    shownFor = target;
    place(target);
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
  popMore.addEventListener("click", () => {
    const term = popMore.dataset.term;
    hide();
    openReference(term);
  });
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") hide(); });
  /* Moved with its word, not hidden: focusing or hovering a word scrolls
   * it into view, and that scroll arrives just after the popover opens. */
  document.addEventListener("scroll", () => { if (shownFor && !popover.hidden) place(shownFor); }, { passive: true });
  document.addEventListener("pointerdown", (ev) => {
    if (shownFor && !shownFor.contains(ev.target) && !popover.contains(ev.target)) hide();
  });

  const marked = [];

  function mark() {
    for (const em of body.querySelectorAll("em")) {
      if (em.closest(NEVER)) continue;
      const entry = entryFor(em.textContent, entries);
      if (!entry) continue;
      em.dlEntry = entry;
      em.classList.add("dl-def");
      em.tabIndex = 0;
      em.setAttribute("aria-describedby", descriptionIds.get(entry));
      if (!em.dlWired) {
        em.dlWired = true;
        em.addEventListener("pointerenter", (ev) => { if (ev.pointerType === "mouse" && em.dlEntry) show(em); });
        em.addEventListener("pointerleave", (ev) => { if (ev.pointerType === "mouse") hideSoon(); });
        em.addEventListener("focus", () => { if (em.dlEntry) show(em); });
        em.addEventListener("blur", hideSoon);
        // A tap (or a click) shows it. Not a toggle: a tap also focuses
        // the word, which has already opened it. A tap elsewhere, or
        // Escape, closes it.
        em.addEventListener("click", () => { if (em.dlEntry) show(em); });
        em.addEventListener("keydown", (ev) => {
          if (ev.key === "Enter" && em.dlEntry) {
            ev.preventDefault();
            hide();
            openReference(em.dlEntry.term);
          }
        });
      }
      marked.push(em);
    }
  }

  function unmark() {
    for (const em of marked) {
      delete em.dlEntry;
      em.classList.remove("dl-def");
      em.removeAttribute("tabindex");
      em.removeAttribute("aria-describedby");
    }
    marked.length = 0;
    hide();
  }

  function refresh() {
    unmark();
    if (readDefinitionsSetting()) mark();
  }

  refresh();
  return { refresh };
}
