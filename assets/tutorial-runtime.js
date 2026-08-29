/* dewlab tutorial runtime.
 *
 * Owns three things on a generated tutorial page:
 *   1. the settings panel — the reader's work, the download, and the reading
 *      texture (theme/font/size/width/link colour -> CSS variables),
 *   2. the CodeMirror editors for `exec` cells, and read-only CodeMirror over
 *      the illustrative blocks build.py marked as `pre.dl-static`,
 *   3. booting Pyodide and running a cell's code.
 *
 * Deliberately thin on rendering: everything a cell produces is turned into
 * markup by tutorial_tools.py, inside Python, so the output rules live in one
 * place and stay unit-testable without a browser. This file starts the work
 * and gets out of the way.
 *
 * Phase 0 scope. Save/load and version-compare (Phase 2) and the series
 * navigation (Phase 3) are not here yet.
 */

import { createCodeEditor, createReadOnlyCode, setEditorTheme } from "./vendor/codemirror.bundle.js";

/* ------------------------------------------------------------------ config */

/* Pyodide is loaded from the public CDN by default. `DEWLAB_PYODIDE_BASE` lets
 * a page point at a self-hosted copy instead — used by the e2e tests, and the
 * escape hatch if a school network ever blocks the CDN (OPEN_QUESTIONS.md 32).
 * Switching the whole site over is a one-line change here, not a redesign. */
const PYODIDE_VERSION = "0.28.3";
/* Resolved against the page, so a relative base ("../assets/pyodide/") works
 * as a module specifier. A bare relative path is not one, and `import()` would
 * reject it. */
const PYODIDE_BASE = new URL(
  globalThis.DEWLAB_PYODIDE_BASE ||
    `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`,
  document.baseURI
).href;

/* The baseline three, per DECISIONS.md. All are official Pyodide packages, so
 * this is one loadPackage call with no micropip step. A tutorial can widen the
 * list via `packages:` in its frontmatter (that is how scipy would arrive). */
const DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib"];

const TEXTURE_KEY = "dewlab:texture";
const PROGRESS_PREFIX = "dewlab:progress:";
const PROGRESS_BADGES_KEY = "dewlab:progress-badges";
/* planning/STUDENT_NOTES.md §4's staleness marker: how many new characters
 * of notes text, since the last export, before the export button gets a
 * marker. Rough on purpose — a heuristic, not a promise. */
const NOTES_EXPORT_PREFIX = "dewlab:notes-exported-len:";
const NOTES_NUDGE_KEY = "dewlab:notes-nudge";
const NOTES_NUDGE_THRESHOLD = 120;
const AUTOSAVE_DELAY = 500;
/* The three build.py write_*_page() slugs that are not a tutorial at all —
 * nothing here has "your work" to save, cells or notes alike, the way an
 * actual tutorial page does. */
const NON_TUTORIAL_PAGES = new Set(["index", "tree", "about"]);
const TEXTURE_DEFAULTS = {
  theme: "system", font: "serif", size: 18, width: 34,
  link: "#d4692a", header: "full",
};

/* -------------------------------------------------------------- manifest */

/* Every tutorial page build.py generates carries a <script id="dewlab-manifest">
 * tag holding one JSON object describing that specific page: its cells'
 * starter code, which Python packages it needs, where its data files
 * live, and so on. This function is how that JSON gets from "text on the
 * page" into a real JavaScript object the rest of this file can use —
 * with sensible defaults filled in if the tag is missing or somehow not
 * valid JSON, so a broken manifest degrades gracefully (an empty page
 * with no cells) instead of crashing this entire script. */
function readManifest() {
  const el = document.getElementById("dewlab-manifest");
  if (!el) return { cells: [], assetBase: "", dataBase: "", packages: DEFAULT_PACKAGES };
  let m;
  try {
    m = JSON.parse(el.textContent);
  } catch (err) {
    console.error("dewlab: manifest is not valid JSON", err);
    return { cells: [], assetBase: "", dataBase: "", packages: DEFAULT_PACKAGES };
  }
  m.cells = m.cells || [];
  m.packages = m.packages && m.packages.length ? m.packages : DEFAULT_PACKAGES;
  m.assetBase = m.assetBase || "";
  m.dataBase = m.dataBase || "";
  m.assetVersions = m.assetVersions || {};
  return m;
}

/* An asset the runtime fetches for itself, with the version build.py hashed for
 * it. The page's own <link> and <script> tags are versioned in the markup; these
 * two are not in the markup, so they would otherwise be the only files a
 * returning visitor could be served a stale copy of. */
function assetUrl(manifest, name) {
  const version = manifest.assetVersions[name];
  return manifest.assetBase + name + (version ? `?v=${version}` : "");
}

/* ---------------------------------------------------------------- chrome */

/* The sticky masthead and navigation are one group, and everything below has
 * to clear it: the status line, the settings panel, and an anchored jump, which
 * would otherwise land its heading underneath. Its height is not a constant —
 * it depends on how far the neighbouring tutorials' titles wrap, which depends
 * on the window and on the reader's text size — so it is measured rather than
 * guessed, and measured again whenever it changes. */
function trackChromeHeight() {
  const chrome = document.getElementById("dl-chrome");
  if (!chrome) return;

  /* Measures the header's actual on-screen height right now and writes it
   * into a CSS custom property (--dl-chrome-h), which tutorial-style.css
   * then uses wherever something needs to sit below the header. This is
   * "measure, don't guess": the header's height genuinely isn't a fixed
   * number, since it depends on how the neighbouring tutorial titles wrap. */
  const publish = () => {
    document.documentElement.style.setProperty(
      "--dl-chrome-h", `${Math.round(chrome.getBoundingClientRect().height)}px`
    );
  };
  publish();

  /* ResizeObserver is a browser API that calls a function whenever a
   * specific element's size changes, for any reason — not just a window
   * resize, but also (for instance) the header wrapping differently
   * because its content changed. It's the more precise tool for "watch
   * this one element," and is preferred here over listening for the
   * window's own resize event, which only catches one of the ways the
   * header's height can actually change. */
  if (typeof ResizeObserver === "function") {
    new ResizeObserver(publish).observe(chrome);
  } else {
    /* No observer: the window changing size is the case that matters most. */
    window.addEventListener("resize", publish);
  }
}

/* -------------------------------------------------------- settings panel */

/* Settings, the cheat sheet (initCheatSheet(), below), and the navigation
 * panel (initSeriesNav()) are three open/close behaviours on the page
 * rather than one — opening any one closes the other two, so a reader is
 * never juggling more than one at a time. That matters most for the
 * cheat sheet and the navigation panel, which anchor to the same left
 * corner (tutorial-style.css) and would sit on top of each other
 * otherwise; Settings keeps the right, but stays in the same
 * mutual-exclusion group for one consistent rule rather than a special
 * case. Escape and a click outside all three close whichever is open: a
 * panel that can only be dismissed by finding the same small button
 * again is the kind of thing that gets left open. */
/* The three functions below (closeCheatSheet, closeSettings,
 * closeSeriesNav) and the three init*() functions further down that use
 * them all share one repeated shape: a toggle button, a panel, and a
 * setOpen(open) function that shows/hides the panel and calls the *other
 * two* close functions whenever it opens. That's the actual mechanism
 * behind "opening any one panel closes the other two" — there's no
 * central manager keeping track of which panel is open; each panel just
 * closes its two siblings the moment it opens itself. `aria-expanded` is
 * set alongside the plain `hidden` attribute so a screen reader also
 * knows the toggle button's current state, not just a sighted reader
 * looking at whether the panel is visible. */
function closeCheatSheet() {
  const toggle = document.getElementById("dl-cheatsheet-toggle");
  const panel = document.getElementById("dl-cheatsheet");
  if (!panel || panel.hasAttribute("hidden")) return;
  panel.setAttribute("hidden", "");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}

function closeSettings() {
  const toggle = document.getElementById("dl-settings-toggle");
  const panel = document.getElementById("dl-settings");
  if (!panel || panel.hasAttribute("hidden")) return;
  panel.setAttribute("hidden", "");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}

function closeSeriesNav() {
  const toggle = document.getElementById("dl-seriesnav-toggle");
  const panel = document.getElementById("dl-seriesnav");
  if (!panel || panel.hasAttribute("hidden")) return;
  panel.setAttribute("hidden", "");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}

function initSettingsPanel() {
  const toggle = document.getElementById("dl-settings-toggle");
  const panel = document.getElementById("dl-settings");
  if (!toggle || !panel) return;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    if (open) {
      closeCheatSheet();
      closeSeriesNav();
    }
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  const close = document.getElementById("dl-settings-close");
  if (close) close.addEventListener("click", () => { setOpen(false); toggle.focus(); });

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || panel.hasAttribute("hidden")) return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (ev) => {
    if (panel.hasAttribute("hidden")) return;
    if (panel.contains(ev.target) || toggle.contains(ev.target)) return;
    setOpen(false);
  });

  /* A section with nothing in it is a heading over a gap. build.py leaves the
   * download section empty on the contents page, which has nothing to
   * download, and on a downloadable copy, which is already the file. */
  for (const section of panel.querySelectorAll(".dl-settings-section")) {
    if (!section.textContent.trim()) section.hidden = true;
  }
}

/* -------------------------------------------------------- cheat sheet */

/* build.py's own kind list — GLOSSARY_KINDS — in the order a reader would
 * find most useful to scan: what a thing *is* before what you *do* with it. */
const GLOSSARY_GROUP_LABELS = {
  concept: "Concepts",
  function: "Functions",
  operator: "Operators",
  formula: "Formulas",
  keyword: "Keywords",
};

/* Builds the cheat sheet's content from scratch out of the manifest's
 * glossary/notes/dataset entries, using document.createElement rather
 * than building an HTML string — safer by construction, since
 * `.textContent = entry.term` can never accidentally turn a term's text
 * into markup, the way concatenating it into an HTML string could if the
 * term ever contained something like "<" without careful escaping. */
function renderCheatSheet(manifest) {
  const container = document.getElementById("dl-cheatsheet-groups");
  if (!container) return;
  container.replaceChildren();

  const byKind = new Map();
  for (const entry of manifest.glossary || []) {
    if (!byKind.has(entry.kind)) byKind.set(entry.kind, []);
    byKind.get(entry.kind).push(entry);
  }

  for (const [kind, label] of Object.entries(GLOSSARY_GROUP_LABELS)) {
    const group = byKind.get(kind);
    if (!group || !group.length) continue;

    const section = document.createElement("div");
    section.className = "dl-cheatsheet-group";
    const heading = document.createElement("h3");
    heading.textContent = label;
    section.append(heading);

    const dl = document.createElement("dl");
    for (const entry of group) {
      const dt = document.createElement("dt");
      dt.textContent = entry.term;
      const dd = document.createElement("dd");
      dd.append(document.createTextNode(entry.definition));
      if (entry.example) {
        const code = document.createElement("code");
        code.textContent = entry.example;
        dd.append(code);
      }
      dl.append(dt, dd);
    }
    section.append(dl);
    container.append(section);
  }

  const notes = manifest.notes || [];
  if (notes.length) {
    const section = document.createElement("div");
    section.className = "dl-cheatsheet-group";
    const heading = document.createElement("h3");
    heading.textContent = "Notes";
    section.append(heading);
    for (const note of notes) {
      // note.html is build.py's own markdown-to-HTML output for this
      // tutorial's own aside — the same trust level as the rest of the
      // page body, which the shell already writes as raw HTML.
      const div = document.createElement("div");
      div.className = "dl-note";
      div.id = note.id;
      div.innerHTML = note.html;
      section.append(div);
    }
    container.append(section);
  }

  const datasets = manifest.datasets || [];
  if (datasets.length) {
    const section = document.createElement("div");
    section.className = "dl-cheatsheet-group";
    const heading = document.createElement("h3");
    heading.textContent = "Datasets used here";
    section.append(heading);

    const dl = document.createElement("dl");
    for (const dataset of datasets) {
      const dt = document.createElement("dt");
      dt.textContent = dataset.name;
      const dd = document.createElement("dd");
      dd.append(document.createTextNode(
        `${dataset.description} — ${dataset.source} (${dataset.license})`));
      dl.append(dt, dd);
    }
    section.append(dl);
    container.append(section);
  }
}

/* Same open/close mechanics as initSettingsPanel(), and the two stay in sync
 * (closeCheatSheet()/closeSettings(), above) so only one is ever open at a
 * time. The one real difference: this toggle starts `hidden` in
 * shell.html, and stays that way — offering nothing at all — unless this
 * page's own manifest actually carries a glossary, a note, or a dataset
 * (planning/SIDEBAR_CONTENT.md §4 — none of the three is cumulative the
 * same way, but all three share this one panel). A tutorial with nothing
 * accumulated yet (planning/CHEAT_SHEETS.md §6) is not a rare case early on:
 * it is every tutorial before the skill has been run on anything ahead of
 * it in its series. */
function initCheatSheet(manifest) {
  const toggle = document.getElementById("dl-cheatsheet-toggle");
  const panel = document.getElementById("dl-cheatsheet");
  const hasContent = (manifest.glossary && manifest.glossary.length)
    || (manifest.notes && manifest.notes.length)
    || (manifest.datasets && manifest.datasets.length);
  if (!toggle || !panel || !hasContent) return;

  renderCheatSheet(manifest);
  toggle.hidden = false;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    if (open) {
      closeSettings();
      closeSeriesNav();
    }
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  const close = document.getElementById("dl-cheatsheet-close");
  if (close) close.addEventListener("click", () => { setOpen(false); toggle.focus(); });

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || panel.hasAttribute("hidden")) return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (ev) => {
    if (panel.hasAttribute("hidden")) return;
    if (panel.contains(ev.target) || toggle.contains(ev.target)) return;
    setOpen(false);
  });
}

/* --------------------------------------------------------- navigation panel */

/* Same open/close mechanics as initSettingsPanel()/initCheatSheet(), and
 * all three stay in sync (closeCheatSheet()/closeSettings()/
 * closeSeriesNav(), above) so only one is ever open at a time. Unlike the
 * cheat sheet, this panel's content is static per page — build.py's
 * render_series_nav() already rendered it server-side into {{SERIES_NAV}}
 * — so there is nothing here to assemble from a manifest, only whether
 * it ended up with anything in it. A tutorial with no series position
 * (archived, or a practice page) gets an empty <nav>, the same "nothing
 * to show, nothing to click" rule the cheat sheet's toggle already
 * follows for a tutorial with nothing accumulated yet. */
function initSeriesNav() {
  const toggle = document.getElementById("dl-seriesnav-toggle");
  const panel = document.getElementById("dl-seriesnav");
  if (!toggle || !panel) return;
  if (!panel.querySelector(".dl-seriesnav-series")) return;

  toggle.hidden = false;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    if (open) {
      closeSettings();
      closeCheatSheet();
    }
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  const close = document.getElementById("dl-seriesnav-close");
  if (close) close.addEventListener("click", () => { setOpen(false); toggle.focus(); });

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || panel.hasAttribute("hidden")) return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (ev) => {
    if (panel.hasAttribute("hidden")) return;
    if (panel.contains(ev.target) || toggle.contains(ev.target)) return;
    setOpen(false);
  });
}

/* --------------------------------------------------------- texture panel */

function isDarkNow() {
  const explicit = document.documentElement.getAttribute("data-theme");
  if (explicit === "dark") return true;
  if (explicit === "light") return false;
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

/* Reads whatever reading-preference choices this reader has made before
 * (theme, font, text size, and so on) out of localStorage, layered on
 * top of TEXTURE_DEFAULTS. The `{ ...a, ...b }` spread syntax merges two
 * objects, with `b`'s keys overriding `a`'s — so a reader's stored
 * choices override the defaults, but any key they've never set (or that
 * didn't exist yet when they last saved) still falls back to the
 * default. This is a pattern repeated throughout this file for every
 * piece of per-reader state (progress, notes, version pins): wrap the
 * read in try/catch, because localStorage can throw (private browsing,
 * a browser setting that blocks it entirely) rather than just returning
 * nothing, and a broken preference should never be able to crash the
 * whole page. */
function loadTexture() {
  try {
    return { ...TEXTURE_DEFAULTS, ...JSON.parse(localStorage.getItem(TEXTURE_KEY) || "{}") };
  } catch (err) {
    return { ...TEXTURE_DEFAULTS };
  }
}

/* The write side of loadTexture — same try/catch-and-shrug shape, since a
 * reader whose browser refuses to store this should still get to read
 * the page, just without a preference that survives the page closing. */
function saveTexture(state) {
  try {
    localStorage.setItem(TEXTURE_KEY, JSON.stringify(state));
  } catch (err) {
    /* Private mode or blocked storage. Preferences apply for this page view
     * only; nothing else about the page depends on them persisting. */
  }
}

/* Turns a texture state object into the actual visual change: setting
 * (or removing) a `data-*` attribute on `<html>` for theme/font/header —
 * the CSS in tutorial-style.css keys off of exactly these attributes —
 * and setting CSS custom properties directly for the numeric/free-form
 * ones (size, width, link colour). Removing an attribute rather than
 * setting it to a "default" value, when the choice is the default, keeps
 * the CSS simpler: it can assume "no attribute" means default, rather
 * than needing an explicit rule for every possible default value too. */
function applyTexture(state) {
  const root = document.documentElement;
  if (state.theme === "system") root.removeAttribute("data-theme");
  else root.setAttribute("data-theme", state.theme);
  if (state.font === "serif") root.removeAttribute("data-font");
  else root.setAttribute("data-font", state.font);
  if (state.header === "full") root.removeAttribute("data-header");
  else root.setAttribute("data-header", state.header);
  root.style.setProperty("--dl-font-size", state.size + "px");
  root.style.setProperty("--dl-line-width", state.width + "rem");
  root.style.setProperty("--dl-link", state.link);
}

/* Wires up every control in the Texture settings section: the segmented
 * button groups (theme/font/width presets), the two sliders (size,
 * width), the colour picker (link), and the reset button. `state` is
 * plain mutable object shared by every one of these listeners through
 * closures — each listener just changes the one property it's
 * responsible for and calls commit(), which re-applies, re-saves, and
 * re-syncs every control's own displayed state to match. `onThemeChange`
 * is a callback the caller (the bottom of this file) provides, since this
 * function doesn't know about CodeMirror editors itself — it just reports
 * "the effective theme changed" and lets the caller decide what to do
 * with that. */
function initTexture(onThemeChange) {
  const state = loadTexture();
  applyTexture(state);

  const panel = document.getElementById("dl-settings-texture");
  if (!panel) return state;

  const sizeEl = document.getElementById("dl-texture-size");
  const widthEl = document.getElementById("dl-texture-width");
  const linkEl = document.getElementById("dl-texture-link");

  function sync() {
    for (const group of panel.querySelectorAll(".dl-seg")) {
      const key = group.dataset.texture;
      /* Width is a number with three named presets and a slider behind them.
       * Setting it to something between the presets is allowed and leaves none
       * of the three pressed, which is the honest way to show it. */
      const current = group.hasAttribute("data-number") ? String(state[key]) : state[key];
      for (const btn of group.querySelectorAll("button")) {
        btn.setAttribute("aria-pressed", String(btn.dataset.value === current));
      }
    }
    sizeEl.value = state.size;
    widthEl.value = state.width;
    linkEl.value = state.link;
  }

  function commit() {
    applyTexture(state);
    saveTexture(state);
    sync();
    onThemeChange(isDarkNow());
  }

  for (const group of panel.querySelectorAll(".dl-seg")) {
    group.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      state[group.dataset.texture] = group.hasAttribute("data-number")
        ? Number(btn.dataset.value)
        : btn.dataset.value;
      commit();
    });
  }
  sizeEl.addEventListener("input", () => { state.size = Number(sizeEl.value); commit(); });
  widthEl.addEventListener("input", () => { state.width = Number(widthEl.value); commit(); });
  linkEl.addEventListener("input", () => { state.link = linkEl.value; commit(); });

  document.getElementById("dl-texture-reset").addEventListener("click", () => {
    Object.assign(state, TEXTURE_DEFAULTS);
    commit();
  });

  /* Following the system theme means reacting when the system changes. */
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      if (state.theme === "system") onThemeChange(isDarkNow());
    });
  }

  sync();
  return state;
}

/* ---------------------------------------------------------------- status */

const statusEl = document.getElementById("dl-status");

function setStatus(text, kind) {
  if (!statusEl) return;
  if (!text) {
    statusEl.hidden = true;
    statusEl.textContent = "";
    return;
  }
  statusEl.hidden = false;
  statusEl.textContent = text;
  statusEl.classList.toggle("dl-status-error", kind === "error");
}

/* ----------------------------------------------------------------- cells */

/* One entry per `exec` cell on the page, in document order. */
const cells = [];

/* Turns the manifest's plain-data cell descriptions into real, working
 * cells on the page: finds each cell's DOM elements (already present in
 * the HTML build.py generated — this doesn't create the cell's markup,
 * only makes it interactive), creates a CodeMirror editor inside it, and
 * wires up its Run button, Reset button, hint toggle, and keyboard
 * shortcut. Each cell's info (its editor, output element, starter code)
 * is collected into a plain object and pushed onto the shared `cells`
 * array, which is what every other function in this file (runCell,
 * saveNow, restoreSaved, and so on) iterates over or looks a cell up in. */
function buildCells(manifest) {
  const dark = isDarkNow();

  for (const spec of manifest.cells) {
    const host = document.querySelector(`.dl-cell[data-cell-id="${CSS.escape(spec.id)}"]`);
    if (!host) {
      console.warn(`dewlab: manifest lists cell "${spec.id}" but the page has no such element`);
      continue;
    }

    const editorHost = host.querySelector(".dl-editor");
    const outputEl = host.querySelector(".dl-output");
    const runBtn = host.querySelector(".dl-btn-run");
    const resetBtn = host.querySelector(".dl-btn-reset");

    const editor = createCodeEditor(editorHost, spec.code || "", {
      dark,
      onChange: () => scheduleSave(),
      completeNames: pageNamesCompletion,
      getDoc: hoverDoc,
      getSignature: signatureHelp,
    });

    const cell = {
      id: spec.id,
      starter: spec.code || "",
      editor,
      outputEl,
      runBtn,
      element: host,
      getCode: () => editor.getValue(),
    };
    cells.push(cell);

    runBtn.addEventListener("click", () => runCell(cell));
    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        editor.setValue(cell.starter);
        outputEl.replaceChildren();
      });
    }

    /* A cell's own hint, if it has one: a plain click toggle, not hover — see
     * the CSS comment on .dl-hint-icon for why. Opening it is a real state
     * change (aria-expanded, the [hidden] attribute), not a display trick, so
     * a screen reader announces it the same way any other disclosure widget
     * would. */
    const hintIcon = host.querySelector(".dl-hint-icon");
    const hintText = host.querySelector(".dl-hint-text");
    if (hintIcon && hintText) {
      hintIcon.addEventListener("click", () => {
        const open = hintIcon.getAttribute("aria-expanded") === "true";
        hintIcon.setAttribute("aria-expanded", String(!open));
        hintText.hidden = open;
      });
    }

    /* Ctrl/Cmd+Enter runs the cell, the shortcut every notebook user reaches
     * for first. Registered on the host rather than inside CodeMirror's keymap
     * so it also fires from the Run button's own focus. */
    host.addEventListener("keydown", (ev) => {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
        ev.preventDefault();
        runCell(cell);
      }
    });
  }
}

/* Enables or disables every cell's Run button at once, with a shared
 * label — used while Python is still booting ("…") or has failed
 * ("unavailable"), so a student can't click Run before there's anything
 * to run against. */
function setRunnable(enabled, label) {
  for (const cell of cells) {
    cell.runBtn.disabled = !enabled;
    cell.runBtn.textContent = label || (enabled ? "Run" : "…");
  }
}

/* --------------------------------------------------------------- Pyodide
 *
 * Two execution paths from here down. The hosted site runs Pyodide inside
 * assets/pyodide-worker.js, off the main thread, so a genuine Stop button
 * is possible (planning/CELL_CONTROLS.md §2). The standalone/offline
 * export keeps Pyodide on the main thread exactly as this file always ran
 * it, unchanged below beyond a name — DECISIONS_LOG.md 7.77: a `file://`
 * page can hit real restrictions loading a module Worker at all, and the
 * offline story does not also need a genuine Stop button to be worth
 * having. `currentManifest.standalone` decides which; nothing past
 * ensureBooted()/runCell() needs to know or care which one is live. */

let bootPromise = null;
let running = null; // null, or the cell object currently running

/* ---- standalone / main-thread path — pre-Worker, unchanged below ---- */

/* Everything with an "MT" suffix from here down belongs to the
 * main-thread path: Pyodide running directly in this script, rather than
 * inside a Worker. This is a near-exact twin of mini-ide-engine.js's own
 * main-thread fallback (that file's own comments go into more line-by-line
 * detail on the same functions, if this section moves too fast) — the
 * pattern is: `lookupLiveNameMT`/`docForMT`/`signatureForMT` answer
 * questions about names that have already run, by asking Python's own
 * `inspect` module; `jediDocMT`/`jediSignatureMT` answer the same
 * questions for code that *hasn't* run yet, using the Jedi static-analysis
 * library instead. */
let pyodideMT = null;
let toolsMT = null;
let inspectModuleMT = null;
let builtinsModuleMT = null;
let jediHoverFnMT = null;
let jediSignatureFnMT = null;

function lookupLiveNameMT(name) {
  if (!toolsMT || !/^[A-Za-z_]\w*$/.test(name)) return undefined;
  try {
    const local = toolsMT._page_globals.get(name);
    if (local !== undefined) return local;
  } catch {
    /* fall through to builtins */
  }
  if (!builtinsModuleMT) return undefined;
  try {
    return builtinsModuleMT[name];
  } catch {
    return undefined;
  }
}

function docForMT(name) {
  if (!toolsMT || !inspectModuleMT) return null;
  const obj = lookupLiveNameMT(name);
  if (obj === undefined || obj === null) return null;
  try {
    return inspectModuleMT.getdoc(obj) || null;
  } catch {
    return null;
  } finally {
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

function signatureForMT(name) {
  if (!toolsMT || !inspectModuleMT) return null;
  const obj = lookupLiveNameMT(name);
  if (obj === undefined || obj === null) return null;
  let sig;
  try {
    sig = inspectModuleMT.signature(obj);
    return name + sig.toString();
  } catch {
    return null;
  } finally {
    if (sig && typeof sig.destroy === "function") sig.destroy();
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

function jediDocMT(source, line, col) {
  if (!jediHoverFnMT) return null;
  try {
    return jediHoverFnMT(source, line, col) || null;
  } catch {
    return null;
  }
}

function jediSignatureMT(source, line, col) {
  if (!jediSignatureFnMT) return null;
  try {
    return jediSignatureFnMT(source, line, col) || null;
  } catch {
    return null;
  }
}

/* Shared with assets/pyodide-worker.js's own copy — genuinely two separate
 * JS execution contexts (a page never runs both), so this is the one place
 * a small duplication was cheaper than a shared-module import neither
 * bundle target (ESM here, IIFE for the standalone bundle) makes free. */
const JEDI_HELPER_SOURCE = `
import jedi

def _dewlab_hover_doc(source, line, col):
    try:
        for d in jedi.Script(source).help(line, col):
            doc = d.docstring()
            if doc:
                return doc
    except Exception:
        pass
    return None

def _dewlab_signature(source, line, col):
    try:
        sigs = jedi.Script(source).get_signatures(line, col)
        if sigs:
            return sigs[0].to_string()
    except Exception:
        pass
    return None
`;

async function loadJediMT() {
  try {
    await pyodideMT.loadPackage(["jedi", "parso"]);
    await pyodideMT.runPythonAsync(JEDI_HELPER_SOURCE);
    jediHoverFnMT = pyodideMT.globals.get("_dewlab_hover_doc");
    jediSignatureFnMT = pyodideMT.globals.get("_dewlab_signature");
  } catch (err) {
    console.warn("dewlab: Jedi failed to load; pre-run tooltips stay live-only", err);
  }
}

/* Downloads and starts Pyodide directly in this script, loads the
 * tutorial's packages, loads tutorial_tools.py, and sets up the shared
 * page namespace every cell runs against — the main-thread twin of
 * bootWorker() further down, used only for the standalone/offline
 * export (see this file's own module-level comment on "Two execution
 * paths" above for why the two exist at all). */
async function bootMainThread(manifest) {
  setStatus("Starting Python…");

  /* A page opened from a file cannot import a module. The standalone export
   * loads Pyodide's classic script first, which leaves loadPyodide on the
   * global. */
  if (!globalThis.loadPyodide) {
    const offline = new Error(
      "Python could not be downloaded. This file needs an internet connection " +
        "the first time you open it — the reading works without one."
    );
    offline.dewlabFinal = true; // already says everything useful; do not dress it up
    throw offline;
  }
  pyodideMT = await globalThis.loadPyodide({ indexURL: PYODIDE_BASE });

  setStatus(`Loading ${manifest.packages.join(", ")}…`);
  await pyodideMT.loadPackage(manifest.packages);

  setStatus("Preparing the notebook tools…");
  /* The standalone export carries this source inside the page, because
   * fetch cannot read a neighbouring file from disk either. */
  const source = manifest.toolsSource;
  pyodideMT.FS.writeFile("/home/pyodide/tutorial_tools.py", source, { encoding: "utf8" });
  toolsMT = pyodideMT.pyimport("tutorial_tools");
  inspectModuleMT = pyodideMT.pyimport("inspect");
  builtinsModuleMT = pyodideMT.pyimport("builtins");
  toolsMT.configure(manifest.dataBase);

  await pyodideMT.runPythonAsync(`
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`);

  setStatus("");
  setRunnable(true, "Run");
  loadJediMT();
}

/* Every name currently defined in the shared namespace, for autocomplete
 * — names starting with "_" (Python's convention for "internal, not for
 * outside use") are filtered out. */
function pageNamesMT() {
  if (!toolsMT) return [];
  return [...toolsMT._page_globals.keys()].filter((name) => !name.startsWith("_"));
}

/* Runs one cell directly on the main thread. tutorial_tools.py's own
 * run_cell() does essentially everything — running the code, capturing
 * output, rendering it into the cell's output element — so this is
 * mostly just "hand off to Python." */
async function runCellMainThread(cell) {
  await toolsMT.run_cell(cell.id, cell.outputEl, cell.getCode());
}

/* ---- hosted / Worker path (planning/CELL_CONTROLS.md §2) ---- */

let worker = null;
/* A SharedArrayBuffer once cross-origin isolation is up, null wherever it
 * is not — a blocked service worker, a browser that refuses one, private
 * browsing. Every caller checks this rather than assuming: a page without
 * it still runs cells in the Worker (still off the main thread, so the
 * rest of the page stays responsive through a runaway loop), it just
 * cannot offer a real Stop for one. */
let interruptBuffer = null;
let jediReadyWorker = false;
let nextRequestId = 1;
const pendingRequests = new Map(); // id -> resolve

/* Sends one message to the Worker and returns a Promise for its reply.
 * A Worker only talks over postMessage — there's no built-in "send this
 * and wait for the answer" — so this builds that: invent a unique `id`,
 * remember a {resolve, reject} pair for it, send the message, and let
 * `ensureWorker`'s onmessage handler resolve the matching pair once a
 * "response" message with the same id comes back. Every request this
 * script sends to `assets/pyodide-worker.js` goes through this one
 * function. */
function workerRequest(type, payload) {
  const id = nextRequestId++;
  return new Promise((resolve, reject) => {
    pendingRequests.set(id, { resolve, reject });
    worker.postMessage({ type, id, ...payload });
  });
}

/* Mirrors _DomSink's own create-or-append logic (assets/tutorial_tools.py)
 * exactly — one open <pre> per contiguous run of the same stream class —
 * relocated here because a Worker has no DOM to run that logic against. */
const openStreams = new Map(); // cellId -> {el, cssClass}

/* Turns one "something happened in Python" event — more printed text, a
 * finished block of markup (a table, an image), or "clear this cell's
 * output" — into the matching DOM change, for whichever cell it belongs
 * to. Called both from the Worker's onmessage handler below (for the
 * hosted path) and would be the same shape a main-thread DOM sink uses,
 * though the main-thread path here instead lets tutorial_tools.py write
 * straight into the DOM itself, since there's no postMessage boundary in
 * the way on that path. */
function applyOutputEvent(cellId, kind, cssClass, text, markup) {
  const cell = cells.find((c) => c.id === cellId);
  if (!cell) return;
  const el = cell.outputEl;
  if (kind === "stream") {
    let open = openStreams.get(cellId);
    if (!open || open.cssClass !== cssClass) {
      const pre = document.createElement("pre");
      pre.className = cssClass;
      el.appendChild(pre);
      open = { el: pre, cssClass };
      openStreams.set(cellId, open);
    }
    /* textContent, never innerHTML: printed output is data, not markup —
     * the same rule _DomSink itself always followed. */
    open.el.textContent += text;
  } else if (kind === "append") {
    openStreams.delete(cellId);
    const template = document.createElement("template");
    template.innerHTML = markup;
    el.appendChild(template.content);
  } else if (kind === "clear") {
    openStreams.delete(cellId);
    el.replaceChildren();
  }
}

/* Creates the Worker the first time it's needed (later calls do nothing
 * — that's the "ensure" in the name), and sets up the one place this
 * file listens for messages coming back from it: progress text
 * ("status"), the autocomplete library finishing its background load
 * ("jedi-ready"), a cell producing output ("output", handed to
 * applyOutputEvent above), and the reply to a specific workerRequest()
 * call ("response", matched up by id). */
function ensureWorker(manifest) {
  if (worker) return;
  worker = new Worker(new URL(assetUrl(manifest, "pyodide-worker.js"), document.baseURI), {
    type: "module",
  });
  worker.onmessage = (ev) => {
    const msg = ev.data;
    if (msg.type === "status") {
      setStatus(msg.text);
    } else if (msg.type === "jedi-ready") {
      jediReadyWorker = true;
    } else if (msg.type === "output") {
      applyOutputEvent(msg.cellId, msg.kind, msg.cssClass, msg.text, msg.markup);
    } else if (msg.type === "response") {
      const pending = pendingRequests.get(msg.id);
      if (!pending) return;
      pendingRequests.delete(msg.id);
      if ("error" in msg) pending.reject(new Error(msg.error));
      else pending.resolve(msg.result);
    }
  };
}

/* Creates the worker (if needed) and asks it to actually boot Python,
 * then — if the browser supports it — sets up the SharedArrayBuffer that
 * makes a genuine Stop button possible (see requestInterrupt() just
 * below for what that buffer is for). */
async function bootWorker(manifest) {
  ensureWorker(manifest);
  await workerRequest("boot", {
    pyodideBase: PYODIDE_BASE,
    packages: manifest.packages,
    /* Absolute: a relative fetch from inside the worker resolves against
     * the worker script's own location, not this page's. */
    toolsSourceUrl: new URL(assetUrl(manifest, "tutorial_tools.py"), document.baseURI).href,
    dataBase: new URL(manifest.dataBase, document.baseURI).href,
  });

  if (globalThis.crossOriginIsolated && typeof SharedArrayBuffer !== "undefined") {
    interruptBuffer = new SharedArrayBuffer(4);
    worker.postMessage({ type: "set-interrupt-buffer", buffer: interruptBuffer });
  }

  setRunnable(true, "Run");
}

/* How the Stop button actually stops a running cell. Two threads
 * normally can only talk by sending whole messages — but Python running
 * a tight loop isn't checking for new messages, it's just running.
 * SharedArrayBuffer is special: it's memory both threads can see and
 * write to instantly, and Pyodide checks it periodically while code
 * runs. Writing the number Pyodide treats as "this means Ctrl-C" into
 * that shared memory is enough to stop even a `while True: pass` cell.
 * If the browser never granted a SharedArrayBuffer (interruptBuffer
 * stays null), this just does nothing — Stop simply isn't offered in
 * that case; see `canStop` in the `globalThis.dewlab` block at the
 * bottom of this file. */
function requestInterrupt() {
  if (!interruptBuffer) return;
  /* 2 is SIGINT in Pyodide's own interrupt-buffer convention. */
  new Int32Array(interruptBuffer)[0] = 2;
}

/* Asks the worker to run one cell and waits for it to finish. The
 * cell's actual output arrives separately, as "output" messages handled
 * in ensureWorker's onmessage above, as the cell runs — not bundled into
 * this Promise's result. */
async function runCellWorker(cell) {
  await workerRequest("run-cell", { cellId: cell.id, code: cell.getCode() });
}

/* ---- code intelligence: what vendor-src/codemirror-entry.js actually calls ---- */

/* The live answer if there is one, Jedi's static one otherwise — live
 * always wins, Jedi only fills the gap live cannot reach
 * (planning/CELL_TOOLTIPS.md). On the standalone path both live entirely
 * on this thread; on the hosted path both live entirely in the Worker, so
 * one request there does the same live-then-Jedi composition
 * assets/pyodide-worker.js's own hoverDoc()/signatureHelp() already do,
 * rather than two round trips from here. */
async function hoverDoc(name, source, line, col) {
  if (currentManifest.standalone) return docForMT(name) || jediDocMT(source, line, col);
  if (!worker) return null;
  return workerRequest("hover-doc", { name, source, line, col });
}

async function signatureHelp(name, source, line, col, argIndex) {
  void argIndex; // not needed here — the CodeMirror side bolds the argument
  if (currentManifest.standalone) return signatureForMT(name) || jediSignatureMT(source, line, col);
  if (!worker) return null;
  return workerRequest("signature-help", { name, source, line, col });
}

/* ---- the one dispatcher everything else calls ---- */

/* Picks which of the two boot paths this page actually gets:
 * `manifest.standalone` is true only for the offline/downloadable export
 * (see this file's own top comment), everything else uses the Worker. */
function boot(manifest) {
  return manifest.standalone ? bootMainThread(manifest) : bootWorker(manifest);
}

/* The one function everything else calls to make sure Python is running
 * before doing anything that needs it. Booting is slow and must only
 * ever happen once per page, so the *Promise* itself is cached in
 * bootPromise — a second call while still booting gets back that same
 * Promise and just waits for the same boot, rather than starting a
 * second one. If booting fails, bootPromise resets to null so a later
 * retry gets a fresh attempt instead of replaying the same failure. */
function ensureBooted(manifest) {
  if (!bootPromise) {
    bootPromise = boot(manifest).catch((err) => {
      console.error("dewlab: Pyodide failed to start", err);
      setStatus(
        err.dewlabFinal
          ? err.message
          : `Python failed to start: ${err.message}. Reloading the page usually fixes it.`,
        "error"
      );
      setRunnable(false, "unavailable");
      throw err;
    });
  }
  return bootPromise;
}

/* Every name currently defined in the shared page namespace — the same
 * dict every cell actually runs against, tutorial_tools._page_globals
 * (run_cell's `globals=`) — so what is offered is exactly what a cell
 * could reference right now: a name from an earlier cell, or from this
 * tutorial's own setup cell, not a generic Python index. `__name__` and
 * anything else tutorial_tools itself seeds with a leading underscore are
 * filtered out. Async because the Worker path is a real round trip;
 * CodeMirror's autocomplete sources accept a Promise natively, the same
 * way its hover and signature-help sources do. */
async function pageNamesCompletion(context) {
  const word = context.matchBefore(/\w+/);
  if (!word || (word.from === word.to && !context.explicit)) return null;
  const names = currentManifest.standalone
    ? pageNamesMT()
    : worker
      ? await workerRequest("page-names", {})
      : [];
  if (!names.length) return null;
  return { from: word.from, options: names.map((label) => ({ label, type: "variable" })) };
}

/* ------------------------------------------------------------ running a cell */

async function runCell(cell) {
  /* A second click on the cell that is already running is a Stop request,
   * not a second Run — the same button does both, per
   * planning/CELL_CONTROLS.md §2. A click on any *other* cell while one is
   * running is ignored, same as it always was: one Pyodide, one thing
   * running in it at a time. */
  if (running === cell) {
    requestInterrupt();
    return;
  }
  if (running) return;
  running = cell;

  const previousLabel = cell.runBtn.textContent;
  const canStop = !currentManifest.standalone && interruptBuffer !== null;
  if (canStop) {
    cell.runBtn.disabled = false;
    cell.runBtn.textContent = "Stop";
    cell.runBtn.classList.add("dl-btn-stop");
  } else {
    cell.runBtn.disabled = true;
    cell.runBtn.textContent = "Running…";
  }

  try {
    await ensureBooted(currentManifest);

    /* Python owns the output area for the duration of the cell: stdout,
     * widgets, tables, figures and tracebacks all land through tutorial_tools,
     * so they appear in the order the code produced them. A student's error —
     * a Stop click included — is normal traffic and is rendered in the cell,
     * not thrown up here. */
    if (currentManifest.standalone) await runCellMainThread(cell);
    else await runCellWorker(cell);
    /* Saved after the run rather than during it, so what is stored is the
     * output the student actually ended up looking at. */
    saveNow();
  } catch (err) {
    /* Boot failure. Already surfaced in the status bar; nothing useful to add
     * inside the cell. */
  } finally {
    running = null;
    cell.runBtn.disabled = false;
    cell.runBtn.classList.remove("dl-btn-stop");
    cell.runBtn.textContent =
      previousLabel === "Running…" || previousLabel === "Stop" ? "Run" : previousLabel;
  }
}

/* ------------------------------------------------- illustrative code, maths */

const readOnlyBlocks = [];

/* An untagged fence. build.py leaves the escaped source inside <pre><code>, so
 * this is an upgrade of something already readable rather than the only way the
 * code ever appears — with JavaScript off, the page still shows it. */
function highlightIllustrativeCode() {
  const dark = isDarkNow();
  for (const pre of document.querySelectorAll("pre.dl-static")) {
    const code = pre.querySelector("code");
    if (!code) continue;
    const source = code.textContent.replace(/\n$/, "");
    const language = pre.dataset.lang || "";
    pre.textContent = "";
    readOnlyBlocks.push(createReadOnlyCode(pre, source, { dark, language }));
  }
}

/* KaTeX is fetched only when the manifest says the page has maths — 266 KB that
 * a prose-and-code tutorial never pays for (DECISIONS_LOG 1.8). Each span holds
 * its own source TeX, which is both the fallback and the input. */
async function renderMaths(manifest) {
  const spans = document.querySelectorAll(".dl-math");
  if (!manifest.math || spans.length === 0) return;
  let renderMath;
  try {
    /* Deliberately a plain string: the standalone export bundles this import
     * into one file, and it can only do that if the specifier is static. That
     * costs the maths bundle its cache-busting, which is the right trade — it
     * is vendored and pinned, so it changes only when we re-vendor on purpose,
     * whereas the stylesheet and the runtime change most weeks. */
    ({ renderMath } = await import("./vendor/katex.bundle.js"));
  } catch (err) {
    console.error("dewlab: KaTeX failed to load; maths stays as source TeX", err);
    return;
  }
  for (const span of spans) {
    renderMath(span, span.textContent, span.classList.contains("dl-math-display"));
  }
}


/* ------------------------------------------------------------- saved work */

/* Everything a student types is kept in their own browser, on their own
 * device, and goes nowhere else. VERSIONING_AND_PROGRESS.md sets the rules:
 * autosave is the real safety net, restore matches on cell id rather than
 * position, and a tutorial edited since they last saved restores anyway — with
 * a notice, never a block. Losing an afternoon's practice is an annoyance, not
 * a lost grade, and the design is sized to that.
 */

let saveTimer = null;
/* Set by initProgressSection() when this page has one; read by saveNow()
 * and restoreSaved() the same way `cells` already is. */
let notesEl = null;

function progressKey() {
  /* Module and slug, because a slug is only unique within its module — both
   * modules have a `first-steps`. Keyed on the slug alone, the two shared one
   * record and each overwrote the other's answers.
   *
   * This is the third time scoping slugs per module has left something keyed
   * on the slug alone: the built pages, the downloadable copies, and now the
   * saved work. */
  const manifest = currentManifest || {};
  return `${PROGRESS_PREFIX}${manifest.module || "unknown"}:${manifest.slug || "unknown"}`;
}

/* Reads this tutorial's saved-work record back out of localStorage, or
 * null if there isn't one (a first visit, private browsing, or storage
 * that refuses to cooperate — all treated the same way: nothing to
 * restore, not an error to show). */
function readSaved() {
  try {
    const raw = localStorage.getItem(progressKey());
    return raw ? JSON.parse(raw) : null;
  } catch (err) {
    /* Private browsing, blocked storage, or something that is not ours. */
    return null;
  }
}

function describeMismatch(record) {
  /* Whether a loaded file belongs to this tutorial, and if not, which one it
   * is. Slug always; module only when the record carries one, so a file saved
   * before the module was recorded still loads where it belongs.
   *
   * An empty string means it fits. */
  if (!record || typeof record !== "object" || !Array.isArray(record.cells)) {
    return "That file could not be read as saved dewlab work.";
  }
  const slug = record["tutorial-slug"];
  const module = record["tutorial-module"];
  const here = slug === currentManifest.slug
    && (!module || module === currentManifest.module);
  if (here) return "";
  const name = [module, slug].filter(Boolean).join(" / ") || "another tutorial";
  return `That file is saved work from ${name}, not this tutorial. `
    + "Nothing has been changed.";
}


function saveNow() {
  clearTimeout(saveTimer);
  saveTimer = null;
  /* Not "no cells": a prose-only tutorial has nothing executable to save
   * but can still have notes worth keeping. Only a page that is not a
   * tutorial at all — the contents page, the topic tree, about — truly has
   * nothing here to save. */
  if (NON_TUTORIAL_PAGES.has(currentManifest.slug)) return;
  const record = {
    "tutorial-slug": currentManifest.slug,
    /* The module too, because the slug alone does not say which tutorial this
     * came from — both modules have a `first-steps`. Written so an exported
     * file can be checked before it replaces anything. */
    "tutorial-module": currentManifest.module,
    "tutorial-version": currentManifest.version,
    saved_at: new Date().toISOString(),
    /* A student's own free-text notes (planning/STUDENT_NOTES.md) — distinct
     * from SIDEBAR_CONTENT.md's author-written pedagogical notes, which are
     * part of the tutorial itself and never travel in this record. */
    notes: notesEl ? notesEl.value : "",
    cells: cells.map((cell) => ({
      task_id: cell.id,
      student_code: cell.getCode(),
      output_html: cell.outputEl.innerHTML,
      /* Whether this cell's last run raised — tutorial_tools.py's stderr
       * stream and show_error() both write class="dl-error", so this is
       * already visible in output_html; captured once here as a plain
       * boolean rather than every reader (the contents page's progress
       * indicator, this page's own Settings summary) re-parsing HTML to
       * ask the same question. */
      errored: !!cell.outputEl.querySelector(".dl-error"),
    })),
  };
  try {
    localStorage.setItem(progressKey(), JSON.stringify(record));
    rememberVersion();
    showSaveState(record.saved_at);
  } catch (err) {
    /* Storage full or refused. Say so rather than pretending it saved. */
    showSaveState(null, "Your browser would not let this page save your work.");
  }
  updateProgressSummary();
}

/* "Debouncing": every call to this resets the timer, so a rapid burst of
 * calls (every keystroke while typing in a cell or the notes box) only
 * results in one real save, AUTOSAVE_DELAY milliseconds after the *last*
 * keystroke — not one save per keystroke, which would be wasteful and
 * would make typing feel laggy if saving is at all slow. */
function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, AUTOSAVE_DELAY);
}

/* Put the work back, and report honestly on what could not be put back. */
function restoreSaved() {
  const record = readSaved();
  if (!record || !Array.isArray(record.cells)) return null;

  if (notesEl && typeof record.notes === "string") notesEl.value = record.notes;

  /* new Map(cells.map(cell => [cell.id, cell])) builds a lookup table from
   * the `cells` array in one line: each cell becomes a [key, value] pair
   * keyed by its id, and Map takes an array of such pairs directly. This
   * turns "find the cell with this id" from a linear search through
   * `cells` (fine for one lookup, wasteful for one per saved cell) into a
   * single fast byId.get(id) call. */
  const byId = new Map(cells.map((cell) => [cell.id, cell]));
  const restored = [];
  const dropped = [];
  let widgets = false;

  for (const saved of record.cells) {
    const cell = byId.get(saved.task_id);
    if (!cell) {
      /* The tutorial no longer has this cell. Say so rather than discarding it
       * silently — a student who wrote something there deserves to know. */
      dropped.push(saved.task_id);
      continue;
    }
    if (typeof saved.student_code === "string") cell.editor.setValue(saved.student_code);
    if (typeof saved.output_html === "string" && saved.output_html) {
      cell.outputEl.innerHTML = saved.output_html;
      if (saved.output_html.includes("dl-widget")) widgets = true;
    }
    restored.push(cell.id);
  }

  return {
    restored,
    dropped,
    widgets,
    savedAt: record.saved_at,
    savedVersion: String(record["tutorial-version"]),
    versionChanged: String(record["tutorial-version"]) !== String(currentManifest.version),
  };
}

/* Shows a small notice box at the top of the page summarizing what
 * restoreSaved() above just did — but only if there's actually something
 * worth telling the reader about (some cells were restored, or some
 * couldn't be). Builds its own dismiss button rather than relying on any
 * shared "closeable box" component, since this is the only place in the
 * file that needs one. */
function announceRestore(summary) {
  if (!summary || (summary.restored.length === 0 && summary.dropped.length === 0)) return;

  const box = document.createElement("div");
  box.className = "dl-restored";
  box.setAttribute("role", "status");

  /* Where the tutorial has releases, both lines below can say what happened
   * rather than guess at it: which release the work came from, which one this
   * is, and that an answer with no cell to go in is still saved. Where it has
   * only one, the work was written against a file that has since been edited
   * in place, and "may not line up" is the honest thing to say (7.30). */
  const from = versionList().find((v) => v.version === summary.savedVersion);
  const here = thisVersion();

  const lines = [];
  if (summary.versionChanged && from && here) {
    lines.push(
      `Your work is back below. You wrote it in the ${from.date} version and ` +
        `you are reading the ${here.date} one.`
    );
  } else if (summary.versionChanged) {
    lines.push(
      "This tutorial has been updated since you last worked on it. Your work is " +
        "back below, but some of it may not line up with the new version."
    );
  } else {
    lines.push("Your work from last time is back below.");
  }
  if (summary.dropped.length) {
    const many = summary.dropped.length !== 1;
    lines.push(
      here
        ? (many
            ? `${summary.dropped.length} of your saved answers are in cells this `
              + "version does not have. They are still saved, and they come back "
              + "in a version that has those cells."
            : "One of your saved answers is in a cell this version does not "
              + "have. It is still saved, and it comes back in a version that "
              + "has the cell.")
        : `${summary.dropped.length} saved ${many ? "cells are" : "cell is"} `
          + "not in this tutorial any more, so there was nowhere to put it back."
    );
  }
  if (summary.widgets) {
    lines.push(
      "Cells with a box or a button in them need running again before they work."
    );
  }

  for (const text of lines) {
    const p = document.createElement("p");
    p.textContent = text;
    box.appendChild(p);
  }

  const dismiss = document.createElement("button");
  dismiss.type = "button";
  dismiss.className = "dl-restored-dismiss";
  dismiss.textContent = "Hide this";
  dismiss.addEventListener("click", () => box.remove());
  box.appendChild(dismiss);

  /* Below the page's own notice where there is one. Which release you are
   * reading is the thing to know first; what happened to your work only makes
   * sense once you know it. */
  const body = document.getElementById("dl-body");
  const notice = body.querySelector(".dl-archived");
  if (notice) notice.insertAdjacentElement("afterend", box);
  else body.insertBefore(box, body.firstChild);
}

function showSaveState(savedAt, problem) {
  const el = document.getElementById("dl-progress-state");
  if (!el) return;
  if (problem) {
    el.textContent = problem;
    return;
  }
  el.textContent = savedAt
    ? `Saved at ${new Date(savedAt).toLocaleTimeString()}. Saving as you go.`
    : "Saving as you go.";
}

function notesExportKey() {
  const manifest = currentManifest || {};
  return `${NOTES_EXPORT_PREFIX}${manifest.module || "unknown"}:${manifest.slug || "unknown"}`;
}

function readNotesNudge() {
  try {
    return localStorage.getItem(NOTES_NUDGE_KEY) !== "off";
  } catch (err) {
    return true;
  }
}

function writeNotesNudge(mode) {
  try {
    localStorage.setItem(NOTES_NUDGE_KEY, mode);
  } catch (err) {
    /* This reader's own choice only; forgotten after it, same as the rest of
     * this project's toggles when storage is refused. */
  }
}

/* planning/STUDENT_NOTES.md §4's staleness marker, the plain version's
 * larger proposal: a small dot on the export button once meaningful new
 * note text has piled up since the last export, and not before. Tracked
 * the same lightweight way rememberVersion()/writePin() track a small piece
 * of per-tutorial state — one number in its own key, not a new field on the
 * save record itself, since what matters here is "since the last export,"
 * not "as of the last save," and those are different moments. */
function updateNotesNudge() {
  const btn = document.getElementById("dl-progress-export");
  if (!btn) return;
  if (!notesEl || !readNotesNudge()) {
    btn.classList.remove("dl-nudge");
    return;
  }
  let exportedLen = 0;
  try {
    exportedLen = parseInt(localStorage.getItem(notesExportKey()) || "0", 10);
  } catch (err) {
    exportedLen = 0;
  }
  const grown = notesEl.value.length - exportedLen;
  btn.classList.toggle("dl-nudge", grown >= NOTES_NUDGE_THRESHOLD);
}

/* Called once notes are known to match what was just exported or imported —
 * both are "this text now exists outside this browser," which is the actual
 * question the marker asks. */
function markNotesExported() {
  if (!notesEl) return;
  try {
    localStorage.setItem(notesExportKey(), String(notesEl.value.length));
  } catch (err) {
    /* Nothing recorded; the marker may reappear sooner than it should — the
     * same "forgotten after it" shape storage refusal already has
     * everywhere else in this file. */
  }
}

function initProgressSection() {
  const section = document.getElementById("dl-settings-work");
  if (!section) return;

  /* Only a page that is not a tutorial at all has nothing here to save —
   * not "no cells": a prose-only tutorial has no code to run but can still
   * have notes worth keeping (planning/STUDENT_NOTES.md), so the section
   * now stays for it. */
  if (NON_TUTORIAL_PAGES.has(currentManifest.slug)) {
    section.remove();
    return;
  }

  notesEl = document.getElementById("dl-progress-notes");
  if (notesEl) notesEl.addEventListener("input", () => { scheduleSave(); updateNotesNudge(); });

  document.getElementById("dl-progress-export").addEventListener("click", () => {
    saveNow();
    const record = readSaved() || {};
    /* The standard trick for making the browser download a file that was
     * only ever built in memory, never fetched from a server: a Blob is
     * an in-memory file-like object, URL.createObjectURL gives it a
     * temporary URL the browser will treat as a real download link, and
     * a plain <a download> element with that URL, clicked
     * programmatically, triggers the download exactly as if a person had
     * clicked a real link. URL.revokeObjectURL below cleans up that
     * temporary URL once it's no longer needed. */
    const blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    /* Module in the filename: two files called first-steps-progress.json in a
     * downloads folder are indistinguishable, and they are from different
     * tutorials. */
    const from = [currentManifest.module, currentManifest.slug].filter(Boolean).join("-");
    link.download = `${from || "dewlab"}-progress.json`;
    link.click();
    URL.revokeObjectURL(link.href);
    markNotesExported();
    updateNotesNudge();
  });

  const file = document.getElementById("dl-progress-file");
  document.getElementById("dl-progress-import").addEventListener("click", () => file.click());
  file.addEventListener("change", async () => {
    const chosen = file.files && file.files[0];
    if (!chosen) return;
    try {
      const record = JSON.parse(await chosen.text());
      /* Check before writing. This used to overwrite whatever was already
       * saved and only then discover the cells did not match, which destroyed
       * the student's real work to make room for somebody else's. */
      const wrong = describeMismatch(record);
      if (wrong) {
        showSaveState(null, wrong);
        file.value = "";
        return;
      }
      localStorage.setItem(progressKey(), JSON.stringify(record));
      announceRestore(restoreSaved());
      showSaveState(record.saved_at);
      updateProgressSummary();
      /* An imported file's notes already exist outside this browser by
       * definition — that is what "import" means here — so this counts as
       * exported too, not as new unsaved text. */
      markNotesExported();
      updateNotesNudge();
    } catch (err) {
      showSaveState(null, "That file could not be read as saved dewlab work.");
    }
    file.value = "";
  });

  document.getElementById("dl-progress-clear").addEventListener("click", () => {
    if (!window.confirm("Clear your work on this tutorial and start again?")) return;
    try {
      localStorage.removeItem(progressKey());
      localStorage.removeItem(notesExportKey());
    } catch (err) {
      /* Nothing to remove, or storage refused. Reset the page either way. */
    }
    for (const cell of cells) {
      cell.editor.setValue(cell.starter);
      cell.outputEl.replaceChildren();
    }
    if (notesEl) notesEl.value = "";
    for (const box of document.querySelectorAll(".dl-restored")) box.remove();
    showSaveState(null);
    updateProgressSummary();
    updateNotesNudge();
  });
}

/* ------------------------------------------------------------- progress
 *
 * planning/PROGRESS_INDICATORS.md: how far a reader has gotten, read from
 * the same saved-progress record saveNow() already writes, nothing new
 * saved beyond the one `errored` boolean captured there. Two surfaces —
 * a plain summary line on this page's own Settings panel, and a small
 * badge next to each tutorial on the contents page, opt-out via a
 * Settings toggle since that one is ambient rather than something a
 * reader had to open a panel to see. */

function progressCounts(entries) {
  /* entries: [{started, errored}]. started means an output exists — run,
   * or restored from a save — not merely that the cell was edited. */
  let done = 0;
  let errored = 0;
  for (const entry of entries) {
    if (!entry.started) continue;
    if (entry.errored) errored++;
    else done++;
  }
  return { total: entries.length, done, errored };
}

function liveProgressCounts() {
  return progressCounts(
    cells.map((cell) => ({
      started: !!cell.outputEl.innerHTML,
      errored: !!cell.outputEl.querySelector(".dl-error"),
    }))
  );
}

function updateProgressSummary() {
  const el = document.getElementById("dl-progress-summary");
  if (!el) return;
  const { total, done, errored } = liveProgressCounts();
  const ran = done + errored;
  /* Nothing run yet is not different information from no cells at all, as
   * far as a reader opening Settings is concerned — same reasoning the
   * contents page's own badge uses (planning/PROGRESS_INDICATORS.md §2):
   * a "0 of 8" reads as a judgment on a page nobody has touched yet. */
  if (ran === 0) {
    el.hidden = true;
    return;
  }
  let text = `${ran} of ${total} cell${total === 1 ? "" : "s"} run`;
  if (errored) text += ` · ${errored} with an error`;
  el.textContent = text;
  el.hidden = false;
}

function readProgressBadges() {
  try {
    return localStorage.getItem(PROGRESS_BADGES_KEY) !== "off";
  } catch (err) {
    return true;
  }
}

function writeProgressBadges(mode) {
  try {
    localStorage.setItem(PROGRESS_BADGES_KEY, mode);
  } catch (err) {
    /* This page's own choice only; forgotten after it, same as the rest of
     * this project's texture/follow settings when storage is refused. */
  }
}

/* Every tutorial link on the contents page, each already carrying its own
 * total cell count (render_index(), build.py) — read at build time so no
 * fetch is needed to know it. A tutorial with no saved record, or one
 * where no cell has been run yet, gets no badge at all rather than a
 * "0/9" that reads as a judgment on a page nobody has opened. */
function renderContentsProgress() {
  for (const badge of document.querySelectorAll(".dl-progress-badge")) badge.remove();
  if (!readProgressBadges()) return;
  for (const link of document.querySelectorAll(".dl-contents a[data-cells]")) {
    const total = parseInt(link.dataset.cells, 10);
    if (!total) continue;
    let record;
    try {
      const key = `${PROGRESS_PREFIX}${link.dataset.module}:${link.dataset.slug}`;
      record = JSON.parse(localStorage.getItem(key) || "null");
    } catch (err) {
      record = null;
    }
    if (!record || !Array.isArray(record.cells)) continue;
    const { done, errored } = progressCounts(
      record.cells.map((cell) => ({ started: !!cell.output_html, errored: !!cell.errored }))
    );
    const ran = done + errored;
    if (ran === 0) continue;
    const badge = document.createElement("span");
    badge.className = "dl-progress-badge" + (errored ? " dl-progress-badge-errored" : "");
    badge.textContent = `${ran}/${total}`;
    link.insertAdjacentElement("afterend", badge);
  }
}

function initContentsProgress() {
  /* Not the contents page, or a build with no live tutorials listed. */
  if (!document.querySelector(".dl-contents a[data-cells]")) return;
  renderContentsProgress();
}

/* Present on every page, contents page included — unlike the summary line
 * above, this toggle is not gated on cells.length, since the page it
 * changes the ambient behaviour of (the contents page) has none. */
function initProgressBadgesToggle() {
  const group = document.querySelector("[data-progress-badges]");
  if (!group) return;

  function sync() {
    const on = readProgressBadges();
    for (const btn of group.querySelectorAll("button")) {
      btn.setAttribute("aria-pressed", String((btn.dataset.value === "on") === on));
    }
  }

  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    writeProgressBadges(btn.dataset.value);
    sync();
    renderContentsProgress();
  });

  sync();
}

/* Only on a page with notes at all — unlike the badges toggle above, there
 * is nothing here to switch off on the contents page, which has no notes
 * field of its own. */
function initNotesNudgeToggle() {
  const group = document.querySelector("[data-notes-nudge]");
  if (!group) return;

  function sync() {
    const on = readNotesNudge();
    for (const btn of group.querySelectorAll("button")) {
      btn.setAttribute("aria-pressed", String((btn.dataset.value === "on") === on));
    }
  }

  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    writeNotesNudge(btn.dataset.value);
    sync();
    updateNotesNudge();
  });

  sync();
}

/* -------------------------------------------------------------- versions */
/*
 * A tutorial can have more than one release, and two different questions
 * decide which one a reader gets:
 *
 *   the build  — what the plain URL serves, for somebody arriving for the
 *                first time. The newest live release.
 *   this file  — what somebody who has already worked here gets. The release
 *                they last worked in, unless they have said otherwise.
 *
 * Saved work is keyed by tutorial rather than by release, and restore matches
 * on cell id, so answers move between releases on their own. That is what lets
 * this list say what will happen rather than warn that something might: the
 * manifest carries every release's cell ids, so the page can count the answers
 * that survive a move before the reader makes it.
 */

const VERSION_PIN_PREFIX = "dewlab:version:";
const FOLLOW_KEY = "dewlab:versions-follow";

function versionList() {
  /* Absent on a tutorial with one release, which is most of them. */
  const list = currentManifest && currentManifest.versions;
  return Array.isArray(list) ? list : [];
}

function versionPinKey() {
  const manifest = currentManifest || {};
  return `${VERSION_PIN_PREFIX}${manifest.module || "unknown"}:${manifest.slug || "unknown"}`;
}

/* Which release this reader is on: the one they picked, or failing that the
 * one their saved work was written against.
 *
 * The fallback is what makes this work for somebody who was here before a
 * second release existed — there was nothing to pick then, but the record
 * says where they were. */
function readPin() {
  try {
    const picked = localStorage.getItem(versionPinKey());
    if (picked) return picked;
  } catch (err) {
    /* Private browsing or blocked storage. Fall through to the record, which
     * has its own guard and will return null under the same conditions. */
  }
  const record = readSaved();
  const worked = record && record["tutorial-version"];
  return worked ? String(worked) : null;
}

function writePin(version) {
  try {
    localStorage.setItem(versionPinKey(), version);
  } catch (err) {
    /* The reader still gets where they clicked; they just will not land there
     * again by themselves. */
  }
}

function rememberVersion() {
  /* Working in a release is a reader saying that is the one they are on, and
   * it has to outrank an older pick or a stale pick would keep pulling them
   * back off the page they are working on.
   *
   * Nothing to remember where there is no choice. */
  if (versionList().length < 2) return;
  writePin(currentManifest.version);
}

function readFollow() {
  /* "started" is the default because it is the one that does not move the
   * ground under somebody halfway through. */
  try {
    return localStorage.getItem(FOLLOW_KEY) === "newest" ? "newest" : "started";
  } catch (err) {
    return "started";
  }
}

function writeFollow(mode) {
  try {
    localStorage.setItem(FOLLOW_KEY, mode);
  } catch (err) {
    /* As above: the choice holds for this page and is forgotten after it. */
  }
}

function thisVersion() {
  return versionList().find((v) => v.version === currentManifest.version) || null;
}

function defaultVersion() {
  return versionList().find((v) => v.isDefault) || null;
}

/* Where a reader who has been here before is sent.
 *
 * Only ever away from the page the plain URL serves, and only to a release
 * that still exists — the first so this cannot bounce between two pages, the
 * second so a reader following a link to one particular release lands on the
 * release they asked for rather than on their own.
 */
function continuityTarget() {
  if (readFollow() !== "started") return null;
  const here = thisVersion();
  if (!here || !here.isDefault) return null;
  const pin = readPin();
  if (!pin || pin === currentManifest.version) return null;
  return versionList().find((v) => v.version === pin) || null;
}

function followTheVersionYouLeftOff() {
  const target = continuityTarget();
  if (!target) return false;
  /* replace rather than assign: Back should go where the reader came from, not
   * to a page that immediately sends them here again. */
  location.replace(target.url);
  return true;
}

/* The answers a reader has written, as opposed to the cells they happened to
 * have open. A starter left untouched is not an answer, and counting it would
 * inflate every number below — the point of these counts is that they are
 * true. */
function answeredCells() {
  const record = readSaved();
  if (!record || !Array.isArray(record.cells)) return [];
  const starters = new Map(cells.map((cell) => [cell.id, cell.starter]));
  return record.cells.filter((saved) => {
    const code = typeof saved.student_code === "string" ? saved.student_code.trim() : "";
    if (!code) return false;
    const starter = starters.get(saved.task_id);
    return starter === undefined || code !== String(starter).trim();
  });
}

/* How many of the reader's real answers (from answeredCells() above)
 * would still show up if they moved to a different release (`entry`).
 * `there` is built as a Set (rather than just using `entry.cells`, an
 * array, directly) specifically so `.has()` is a fast lookup rather than
 * a linear scan through the array for every single answer being checked
 * — the same reasoning as `byId` in restoreSaved() above, just with a
 * Set instead of a Map since only membership matters here, not an
 * associated value. */
function carryOver(entry) {
  const answers = answeredCells();
  if (answers.length === 0) return null;
  const there = new Set(Array.isArray(entry.cells) ? entry.cells : []);
  return {
    carried: answers.filter((saved) => there.has(saved.task_id)).length,
    total: answers.length,
  };
}

function describeCarry(entry) {
  const count = carryOver(entry);
  if (!count) return "";
  if (count.carried === count.total) {
    return count.total === 1
      ? "Your answer carries over."
      : `All ${count.total} of your answers carry over.`;
  }
  const missing = count.total - count.carried;
  const rest = missing === 1
    ? "1 cell is not in that version, so that answer stays saved but is not shown there."
    : `${missing} cells are not in that version, so those answers stay saved `
      + "but are not shown there.";
  return `${count.carried} of your ${count.total} answers carry over. ${rest}`;
}

function versionOption(entry) {
  const item = document.createElement("li");
  item.className = "dl-version";
  item.dataset.version = entry.version;

  const here = entry.version === currentManifest.version;
  if (here) item.dataset.current = "";

  const name = document.createElement(here ? "span" : "a");
  name.className = "dl-version-name";
  name.textContent = entry.date;
  if (!here) {
    name.href = entry.url;
    name.addEventListener("click", () => writePin(entry.version));
  }
  item.appendChild(name);

  const tags = [];
  if (here) tags.push("you are reading this");
  if (entry.isDefault && !here) tags.push("current");
  if (entry.status === "beta") tags.push("draft");
  if (entry.status === "archived") tags.push("retired");
  for (const text of tags) {
    const tag = document.createElement("span");
    tag.className = "dl-version-tag";
    tag.textContent = text;
    item.appendChild(tag);
  }

  const carry = here ? "" : describeCarry(entry);
  if (carry) {
    const line = document.createElement("p");
    line.className = "dl-version-carry";
    line.textContent = carry;
    item.appendChild(line);
  }
  return item;
}

function fillVersionList(list) {
  list.replaceChildren();
  for (const entry of versionList()) list.appendChild(versionOption(entry));
}

/* The control beside the title: nothing at all on a tutorial with one release,
 * something always visible on a tutorial with several.
 *
 * Not a control that appears on hover. Hover does not exist on a phone, and a
 * good share of these readers are on one — an affordance that only appears on
 * hover is not subtle to them, it is missing.
 */
function initVersionMarker() {
  if (versionList().length < 2) return;
  const here = thisVersion();
  const wrap = document.createElement("div");
  wrap.className = "dl-versions";
  wrap.id = "dl-versions";

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "dl-versions-toggle";
  toggle.id = "dl-versions-toggle";
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-controls", "dl-versions-list");
  toggle.append(here ? here.date : currentManifest.version);
  const caret = document.createElement("span");
  caret.className = "dl-versions-caret";
  caret.setAttribute("aria-hidden", "true");
  toggle.appendChild(caret);
  wrap.appendChild(toggle);

  const list = document.createElement("ul");
  list.className = "dl-versions-list";
  list.id = "dl-versions-list";
  list.hidden = true;
  wrap.appendChild(list);

  function setOpen(open) {
    /* Built on opening rather than at load, because the counts read saved work
     * and the reader may have written some since the page loaded. */
    if (open) fillVersionList(list);
    list.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  }

  toggle.addEventListener("click", () => setOpen(list.hidden));
  document.addEventListener("click", (ev) => {
    if (!list.hidden && !wrap.contains(ev.target)) setOpen(false);
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && !list.hidden) {
      setOpen(false);
      toggle.focus();
    }
  });

  /* Under the title where there is one, which is every tutorial that opens
   * with a `# Heading`. A tutorial that opens straight into a section is legal
   * and would otherwise get no marker at all, so it goes to the top of the
   * body instead — after the notice, which is the one thing that outranks it. */
  const heading = document.querySelector("#dl-body h1");
  if (heading) {
    heading.insertAdjacentElement("afterend", wrap);
    return;
  }
  const body = document.getElementById("dl-body");
  const notice = body.querySelector(".dl-archived");
  if (notice) notice.insertAdjacentElement("afterend", wrap);
  else body.insertBefore(wrap, body.firstChild);
}

/* build.py already writes the notice that says which release this is and links
 * to the current one. What it cannot know is how much of this reader's work
 * moves with them, so that is added here rather than duplicated as a second
 * box saying nearly the same thing. */
function annotateNotice() {
  const notice = document.querySelector("#dl-body .dl-archived");
  const home = defaultVersion();
  if (!notice || !home || home.version === currentManifest.version) return;

  for (const link of notice.querySelectorAll(`a[href="${CSS.escape(home.url)}"]`)) {
    link.addEventListener("click", () => writePin(home.version));
  }

  const lines = [];
  if (readPin() === currentManifest.version) {
    lines.push("You are on this one because it is where you left off.");
  }
  const carry = describeCarry(home);
  if (carry) lines.push(`Moving to the current version: ${carry[0].toLowerCase()}${carry.slice(1)}`);
  for (const text of lines) {
    const line = document.createElement("p");
    line.className = "dl-version-carry";
    line.textContent = text;
    notice.appendChild(line);
  }
}

function initVersionsSection() {
  const section = document.getElementById("dl-settings-versions");
  if (!section) return;
  if (versionList().length < 2) {
    section.remove();
    return;
  }

  const note = document.getElementById("dl-versions-note");
  if (note) {
    note.textContent =
      `This tutorial has ${versionList().length} releases. Your work is saved `
      + "against the tutorial rather than against one of them, so it moves with "
      + "you: an answer is there in every version whose cells it belongs to.";
  }

  const group = section.querySelector("[data-versions-follow]");
  const list = document.getElementById("dl-versions-settings");

  function sync() {
    const mode = readFollow();
    for (const btn of group.querySelectorAll("button")) {
      btn.setAttribute("aria-pressed", String(btn.dataset.value === mode));
    }
    fillVersionList(list);
  }

  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    writeFollow(btn.dataset.value);
    sync();
    /* Asking for the newest from an older release is a request to be on the
     * newest, not a preference to take effect the next time they visit. */
    const home = defaultVersion();
    if (btn.dataset.value === "newest" && home
        && home.version !== currentManifest.version) {
      location.href = home.url;
    }
  });

  sync();
}

/* ------------------------------------------------------------------ start
 *
 * Everything above this point was just defining functions — nothing
 * actually happened on the page yet. This section is where the file
 * really *runs*: top-level code in a JavaScript module executes
 * immediately, in order, the moment the module loads, so the sequence of
 * calls below is the real, literal order things happen in when a
 * tutorial page opens. This file is loaded as a module (`<script
 * type="module">` in the page's own HTML), which is what lets it use
 * `import` at the very top and guarantees it doesn't run until the page's
 * HTML has already been parsed — so every element these functions look
 * up with `document.getElementById(...)` is guaranteed to already exist.
 */

const currentManifest = readManifest();

/* Before anything is built or booted: a reader who has worked in an older
 * release goes back to it rather than being handed the newest one halfway
 * through. Everything below is skipped, because this page is about to be
 * replaced by another one. */
const leaving = followTheVersionYouLeftOff();

initTexture((dark) => {
  for (const cell of cells) setEditorTheme(cell.editor, dark);
  for (const block of readOnlyBlocks) setEditorTheme(block, dark);
});

buildCells(currentManifest);
initProgressSection();
initVersionsSection();
initVersionMarker();
initSettingsPanel();
initCheatSheet(currentManifest);
initSeriesNav();
initProgressBadgesToggle();
initNotesNudgeToggle();
initContentsProgress();
trackChromeHeight();
announceRestore(restoreSaved());
updateProgressSummary();
updateNotesNudge();
annotateNotice();
highlightIllustrativeCode();
const mathsRendered = renderMaths(currentManifest);

if (cells.length === 0 || leaving) {
  /* A prose-only tutorial is a normal tutorial, not a special case
   * (CONTENT_AND_FILE_ARCHITECTURE.md). No cells means no reason to pay for
   * Pyodide at all. */
  /* Nor is there a reason to pay for it on a page that is being replaced this
   * instant by the release the reader left off in. */
  setStatus("");
} else {
  setRunnable(false, "…");
  ensureBooted(currentManifest).catch(() => {});
}

/* Exposed for the e2e tests to await, and for debugging from the console.
 * `globalThis` is JavaScript's name for "the global object" in whatever
 * environment the code is running (the same thing `window` refers to in
 * a browser) — assigning to `globalThis.dewlab` makes this object
 * reachable from the browser's developer console as `dewlab.something`,
 * and from Playwright's end-to-end tests the same way, without either of
 * those needing to import anything from this file (which they couldn't
 * — this is a page script, not a library). */
globalThis.dewlab = {
  version: PYODIDE_VERSION,
  cells,
  saveNow,
  readSaved,
  progressKey,
  describeMismatch,
  versionList,
  readPin,
  writePin,
  readFollow,
  carryOver,
  describeCarry,
  ready: () =>
    Promise.all([
      mathsRendered,
      cells.length === 0 ? Promise.resolve() : ensureBooted(currentManifest),
    ]),
  runCell: (id) => {
    const cell = cells.find((c) => c.id === id);
    if (!cell) throw new Error(`no cell "${id}"`);
    return runCell(cell);
  },
  jediReady: () => (currentManifest.standalone ? jediHoverFnMT !== null : jediReadyWorker),
  hoverDoc,
  signatureHelp,
  canStop: () => !currentManifest.standalone && interruptBuffer !== null,
};
