/**
 * dewmini — a small, quiet notebook.
 *
 * Runs on the same tutorial_tools.py + run_cell() pipeline as every dewlab
 * tutorial page (fetched from ../assets/tutorial_tools.py at boot, never
 * duplicated here), so show()/show_table()/check()/widgets/matplotlib all
 * behave exactly as they do in a tutorial. What is new here is the page
 * around it: cell CRUD, drag reorder, downloads, and the Settings/Help/Notes
 * panels.
 */

import { createCodeEditor, setEditorTheme } from "../assets/vendor/codemirror.bundle.js";
import * as dfs from "./dewmini-fs.js";
import * as engine from "../assets/pyodide-engine.js";

const PYODIDE_VERSION = "0.28.3";
// The pre-tabs key: one notebook, stored as a bare array of cells. Still read
// once, by migrateLegacyCells() below, so a reader who left work here before
// tabs existed finds it again afterwards.
const LEGACY_CELLS_KEY = "dewmini:cells:v1";
const NOTEBOOKS_KEY = "dewmini:notebooks:v1";
const NOTES_KEY = "dewmini:notes";

// Beyond the curriculum's numpy/pandas/matplotlib baseline (DECISIONS.md
// "Core libraries"), dewmini also loads sqlite3 (an unvendored stdlib
// module in Pyodide, one extra loadPackage() entry — DECISIONS_LOG.md 7.78)
// and Pillow (what image_input() decodes a picked file into). A tutorial
// page stays on the narrower curriculum baseline; dewmini is a general
// notebook, not curriculum content, so it can afford the wider default.
const DM_PACKAGES = ["numpy", "pandas", "matplotlib", "sqlite3", "Pillow"];

// The browser-backed networking patch, for the exported standalone HTML —
// dewmini itself gets this from assets/pyodide-engine.js's own copy at boot,
// but an exported notebook boots its own Pyodide with none of that code, so
// it carries the patch inline. Without it, a notebook that read a URL
// perfectly well in dewmini would fail with "unknown url type: https" in the
// file the reader actually saved and sent to someone.
const DM_NETWORK_PATCH = "try:\n    import pyodide_http\n    pyodide_http.patch_all()\nexcept Exception:\n    pass\n";

const CELL_TYPES = { PYTHON: "python", TEXT: "text", HTML: "html", CSS: "css" };

/* The fixed little "page" a CSS cell's own preview renders — a heading, a
 * paragraph with a link, a button, a list: enough ordinary elements that a
 * reader's own selectors (h2, p, a, button, li, …) land on something real,
 * without asking them to write any HTML of their own first
 * (planning/CELL_IDENTITY.md §8's own reasoning for why a CSS cell doesn't
 * simply style the HTML cell above it — that would make its behaviour
 * depend on cell order, which nothing else in dewmini's model does). */
const CSS_PREVIEW_MARKUP = `<h2>Heading</h2>
<p>A paragraph of text, with a <a href="#">link</a> inside it.</p>
<button>A button</button>
<ul><li>One item</li><li>Another item</li></ul>`;
const IMPORTS_SNIPPET = "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n";

/* The cell types meant to be read, not run — rendered by default, with
 * an explicit Edit/View toggle and chrome that stays quiet until
 * touched (planning/CELL_IDENTITY.md §4/§8). Python is the one type
 * outside this set that still runs against the shared session; SQL and
 * JavaScript will join it once they exist. */
const READ_NOT_RUN_TYPES = new Set([CELL_TYPES.TEXT, CELL_TYPES.HTML, CELL_TYPES.CSS]);

/* Seeds the namespace for the *standalone export* only — a downloaded copy
 * carries its own tiny runtime rather than pyodide-engine.js, which is what
 * seeds the live page (its own copy of this, assets/pyodide-engine.js).
 *
 * __dewlab__ rather than __dewmini__ so that the same notebook answers
 * `__name__` the same way in the page and in the file a reader downloaded
 * from it. They disagreed once the live page moved onto the shared engine,
 * which is the kind of difference nobody finds until a cell behaves
 * differently after a download and there is no obvious reason why. */
const SEED_GLOBALS_CODE = `
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`;

// Every open notebook: [{ id, name, cells }]. `cells` below is not a copy of
// the active one's array — it *is* that array, the same object — so every
// function in this file that already worked on one notebook's cells keeps
// working unchanged, and switching tabs is a matter of re-pointing this one
// variable. setCells() exists because that link is easy to break: assigning
// `cells = something` alone would leave the notebook holding the old array.
let notebooks = [];
let activeNotebookId = null;
let cells = [];

/* The two ways a notebook can be shown. A notebook is a list of cells; a
 * file is one continuous piece of text. Because a percent-format Python
 * file is both of those at once, switching between them converts nothing
 * — it changes how the same work is displayed.
 *
 * Both views are kept because an empty file is harder to begin than an
 * empty cell. A blank page asks a beginner to decide what the whole
 * program will be before writing anything, and a cell asks for one line.
 * A student can start in cells and move to a file when they are ready. */
const VIEWS = { CELLS: "cells", FILE: "file" };

/* Output from a whole-file run is not any cell's, so it needs an id of
 * its own for the engine to route by. Prefixed like a real cell id and
 * impossible to collide with one, since generateId() always ends in
 * random base-36 rather than a word. */
const FILE_RUN_ID = "cell-file-run";

let fileEditor = null;
let fileRunOutputEl = null;
let fileParseTimer = null;
let cellsContainer, emptyEl, statusEl, tabsEl;
let statusClearTimer = null;

// The live Pyodide interpreter, cell execution, hover/signature-help, and
// filesystem mounting all go through the shared assets/pyodide-engine.js
// now (DECISIONS_LOG.md 7.89) — rather than this file holding its own
// `pyodide`/`tools`/`inspectModule` references and talking to Pyodide
// directly, the way its first version did.
// toolsSourceCache stays: downloadAsHtml()'s embedded bootstrap below
// still needs tutorial_tools.py's raw source text, independent of the
// live engine (a downloaded copy runs its own simple main-thread
// Pyodide, same as the live page's own file:// fallback would).
let toolsSourceCache = null;
let running = false;
let runningCellId = null;
/* How many cells have actually run since the interpreter last started or
 * was last reset from a clean namespace — the counter behind each cell's
 * "Ran Nth" (planning/CELL_IDENTITY.md §3). Reset to 0 by
 * resetRunSequence(), never decremented otherwise: a cell that runs twice
 * in the same session just gets a new, later ordinal each time. */
let runSequenceCounter = 0;

let draggedId = null;

// ---------------------------------------------------------------- storage

/* A unique id for a new cell: the current time in base 36 (so ids sort
 * roughly by creation order) plus a few random base-36 characters (so two
 * cells created in the same millisecond still don't collide). Nothing
 * here needs to be a "real" globally-unique id like a UUID — it only has
 * to be unique among this one notebook's own cells. */
function generateId() {
  return `cell-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

/* Turns whatever was stored into real cell objects. The `.filter(...)` step
 * matters: it drops anything that doesn't look like a real cell (a corrupted
 * entry, or one from some future version of this file with a cell type this
 * version doesn't know about) rather than trusting whatever was stored — a
 * cheap defense against a stray bad value crashing the whole notebook on
 * load. */
function readCells(saved) {
  if (!Array.isArray(saved)) return [];
  return saved
    .filter((c) => c && c.id && Object.values(CELL_TYPES).includes(c.type))
    .map((c) => ({ id: c.id, type: c.type, content: c.content || "", output: c.output || "", error: !!c.error, collapsed: !!c.collapsed }));
}

/* A notebook with nothing in it yet. Named rather than numbered-only so a
 * tab strip reads as a row of names, not a row of "Untitled". */
function makeNotebook(name, cellList = [], view = VIEWS.CELLS) {
  return { id: `nb-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
           name, cells: cellList, view };
}

/* Work saved before tabs existed lived under a different key, as a bare
 * array. Read it once, fold it into a first notebook, and leave the old key
 * alone rather than deleting it — if this migration ever turns out to be
 * wrong, the original is still sitting there to recover from, and a stale
 * key costs a few kilobytes of browser storage. */
function migrateLegacyCells() {
  let legacy = [];
  try {
    legacy = readCells(JSON.parse(localStorage.getItem(LEGACY_CELLS_KEY) || "[]"));
  } catch {
    legacy = [];
  }
  return legacy.length ? [makeNotebook("Notebook", legacy)] : [];
}

/* Reads every open notebook back out of localStorage on page load, falling
 * back through: saved notebooks, then pre-tabs work migrated into one, then
 * a single empty notebook. Always ends with at least one notebook and a
 * valid active id, so nothing downstream has to handle "no notebook". */
function loadSavedState() {
  let saved = null;
  try {
    saved = JSON.parse(localStorage.getItem(NOTEBOOKS_KEY) || "null");
  } catch {
    saved = null;
  }

  notebooks = [];
  if (saved && Array.isArray(saved.notebooks)) {
    notebooks = saved.notebooks
      .filter((nb) => nb && nb.id)
      .map((nb) => ({ id: nb.id, name: nb.name || "Notebook", cells: readCells(nb.cells),
                      view: nb.view === VIEWS.FILE ? VIEWS.FILE : VIEWS.CELLS,
                      // Which workspace file this tab is, when it is one.
                      // Without this a reload would quietly turn it into an
                      // ordinary notebook and stop saving the file.
                      ...(typeof nb.path === "string" && nb.path ? { path: nb.path } : {}) }));
  }
  if (!notebooks.length) notebooks = migrateLegacyCells();
  if (!notebooks.length) notebooks = [makeNotebook("Notebook")];

  const wanted = saved && saved.active;
  activeNotebookId = notebooks.some((nb) => nb.id === wanted) ? wanted : notebooks[0].id;
  cells = activeNotebook().cells;
}

function activeNotebook() {
  return notebooks.find((nb) => nb.id === activeNotebookId) || notebooks[0];
}

/* The one safe way to swap a notebook's cells wholesale. Assigning `cells`
 * on its own would break the "same array object" link this file relies on
 * (see the declaration above), leaving edits landing in an array no longer
 * attached to any notebook — visible on screen until a tab switch silently
 * reverted them. */
function setCells(next) {
  cells = next;
  activeNotebook().cells = next;
}

/* Cell ids whose output has been left out of storage because the whole
 * notebook would not fit otherwise — see saveState(). The output is still
 * on screen and still on the cell object; it is only the saved copy that
 * lacks it, so a reload shows the code with an empty output area. */
const outputsTooLargeToSave = new Set();

/* How many outputs had been dropped the last time the reader was told.
 * Kept so the warning appears when the situation gets worse rather than
 * on every keystroke, since saveState() runs on every edit. */
let warnedDroppedOutputs = 0;

/* One attempt at writing the whole of dewmini's work to localStorage.
 * Returns false when it did not fit (or when storage is unavailable at
 * all, as in a browser with site data blocked), true when it did.
 *
 * Note the `.map(({ id, type, content, output, error }) => ({...}))`
 * step: by the time a cell has been rendered, it also carries live things
 * like `.editor` (a CodeMirror instance) and `.outputEl` (a DOM element)
 * — objects that `JSON.stringify` can't handle (they contain circular
 * references back to themselves) and that don't belong in storage anyway,
 * since they get rebuilt fresh every time the notebook renders. This
 * picks out only the plain-data fields worth keeping — build a fresh
 * plain object rather than serializing the live one directly. */
function writeSavedState(skipOutputFor) {
  const plainCells = (list) => list.map(({ id, type, content, output, error, collapsed }) => ({
    id, type, content,
    output: skipOutputFor.has(id) ? "" : (output || ""),
    error: !!error,
    collapsed: !!collapsed
  }));
  try {
    localStorage.setItem(NOTEBOOKS_KEY, JSON.stringify({
      active: activeNotebookId,
      notebooks: notebooks.map((nb) => ({ id: nb.id, name: nb.name, view: nb.view || VIEWS.CELLS,
                                         ...(nb.path ? { path: nb.path } : {}),
                                         cells: plainCells(nb.cells) })),
    }));
    return true;
  } catch {
    return false;
  }
}

/* Saves every open notebook, giving up outputs before it gives up code.
 *
 * A browser allows an origin somewhere around 5 MB of localStorage, and a
 * cell's output is stored as the HTML the output area is showing — which
 * for a matplotlib figure is a base64 PNG of tens of kilobytes. A few
 * plots across a few notebooks reaches the limit, and `setItem` then
 * throws a QuotaExceededError.
 *
 * This function used to wrap that single write in a `try` with an empty
 * `catch`, which meant crossing the limit stopped the work being saved
 * with no error, no message, and no sign anything had changed — until a
 * reload, which brought back whatever had been stored before the first
 * failed write. Losing an afternoon that way is the worst outcome this
 * file can produce, so it is worth some care.
 *
 * Code is small and cannot be recovered by any other means. An output is
 * large and can be recovered by running the cell again. So when the full
 * save does not fit, outputs are dropped — largest first, since the
 * largest one is usually the whole problem — and the write is tried
 * again after each. Only if every output is gone and it still does not
 * fit is anything actually lost, and then the reader is told plainly.
 *
 * Once an output has been dropped, its cell id stays in
 * `outputsTooLargeToSave`, so the following keystroke does not repeat the
 * search. The id comes back out when that cell runs again or its output
 * is cleared, which is when its size has changed and it deserves another
 * try. */
function saveState() {
  scheduleWorkspaceWrite(activeNotebook());
  pruneDroppedOutputs();
  if (writeSavedState(outputsTooLargeToSave)) {
    if (outputsTooLargeToSave.size > warnedDroppedOutputs) warnAboutDroppedOutputs();
    else if (!outputsTooLargeToSave.size) showStorageNotice("");
    return;
  }

  const candidates = [];
  for (const nb of notebooks) {
    for (const cell of nb.cells) {
      if (cell.output && !outputsTooLargeToSave.has(cell.id)) candidates.push(cell);
    }
  }
  candidates.sort((a, b) => b.output.length - a.output.length);

  for (const cell of candidates) {
    outputsTooLargeToSave.add(cell.id);
    if (writeSavedState(outputsTooLargeToSave)) {
      warnAboutDroppedOutputs();
      return;
    }
  }

  // Nothing left to give up: even the code alone will not fit. This is
  // the one case where work really is at risk, so it says so plainly and
  // names the one action that keeps the work regardless of storage.
  showStorageNotice(
    "This browser's storage is full, so your work is no longer being saved. "
    + "Use Download to keep it — a reload from here would lose it."
  );
}

/* Says how many outputs are being left out of the save, and why that is
 * survivable. Deliberately not phrased as a failure: the code — the part
 * that cannot be regenerated — is safely stored. */
function warnAboutDroppedOutputs() {
  const n = outputsTooLargeToSave.size;
  warnedDroppedOutputs = n;
  showStorageNotice(
    `Your code is saved. ${n === 1 ? "One output was" : `${n} outputs were`} too large for this `
    + `browser's storage, so ${n === 1 ? "it" : "they"} will be empty after a reload — `
    + `run ${n === 1 ? "that cell" : "those cells"} again to see ${n === 1 ? "it" : "them"}, `
    + "or use Download to keep everything."
  );
}

/* Puts a message in the standing storage notice, or takes it away when
 * `message` is empty. Not updateStatus(): that line is wiped by the very
 * next thing to report, and a run reports "Ran." immediately after the
 * save that produced this — so a reader would never see it. */
function showStorageNotice(message) {
  const notice = document.getElementById("storage-notice");
  const text = document.getElementById("storage-notice-text");
  if (!notice || !text) return;
  if (!message) {
    notice.hidden = true;
    text.textContent = "";
    return;
  }
  text.textContent = message;
  notice.hidden = false;
}

/* Forgets ids for cells that no longer exist, so the number in the
 * warning stays honest after a cell is deleted or a notebook closed.
 * Guarded on the set being non-empty, which it is in every ordinary
 * session, so the usual save costs one comparison rather than a walk. */
function pruneDroppedOutputs() {
  if (!outputsTooLargeToSave.size) return;
  const live = new Set();
  for (const nb of notebooks) for (const cell of nb.cells) live.add(cell.id);
  for (const id of outputsTooLargeToSave) {
    if (!live.has(id)) outputsTooLargeToSave.delete(id);
  }
  warnedDroppedOutputs = Math.min(warnedDroppedOutputs, outputsTooLargeToSave.size);
}

/* Lets a cell's output be tried again on the next save. Called wherever
 * an output is replaced or emptied, since a new output may well fit
 * where the old one did not. */
function allowOutputToSaveAgain(cellId) {
  if (!outputsTooLargeToSave.delete(cellId)) return;
  warnedDroppedOutputs = Math.min(warnedDroppedOutputs, outputsTooLargeToSave.size);
}

// --------------------------------------------------------------- notebooks

/* Switches which notebook the page is showing. Every open editor belongs to
 * the notebook leaving the screen, so they are destroyed here rather than
 * left behind: a CodeMirror instance holds its own DOM and listeners, and
 * renderCells() below builds fresh ones for the notebook arriving. */
function showNotebook(id) {
  if (id === activeNotebookId) return;
  const target = notebooks.find((nb) => nb.id === id);
  if (!target) return;
  flushFileEditor();
  cells.forEach((c) => c.editor?.destroy());
  activeNotebookId = id;
  cells = target.cells;
  saveState();
  renderTabs();
  renderCells();
  updateFilenameField();
  updateViewSwitch();
  updateStatus(`Switched to ${target.name}.`);
}

/* Adds a notebook and switches to it — the shared tail of "+ New", an
 * import, and anything else that arrives as a whole notebook. */
function openNotebook(notebook) {
  cells.forEach((c) => c.editor?.destroy());
  notebooks.push(notebook);
  activeNotebookId = notebook.id;
  cells = notebook.cells;
  saveState();
  renderTabs();
  renderCells();
  updateFilenameField();
}

/* Closes a tab. The last one is never closed — a dewmini with no notebook
 * at all has no meaningful state to be in, and "close" quietly becoming
 * "clear" would be worse than the button simply not being there. Asks first
 * only when there is something to lose, so closing an empty scratch tab
 * stays a single click. */
function closeNotebook(id) {
  if (notebooks.length < 2) return;
  const index = notebooks.findIndex((nb) => nb.id === id);
  if (index === -1) return;
  const notebook = notebooks[index];
  if (notebook.cells.length && !confirm(`Close "${notebook.name}"? Its ${notebook.cells.length} cell${notebook.cells.length === 1 ? "" : "s"} will be gone.`)) return;

  if (id === activeNotebookId) cells.forEach((c) => c.editor?.destroy());
  notebooks.splice(index, 1);
  if (id === activeNotebookId) {
    const next = notebooks[Math.min(index, notebooks.length - 1)];
    activeNotebookId = next.id;
    cells = next.cells;
    renderCells();
    updateFilenameField();
  }
  saveState();
  renderTabs();
  updateStatus(`Closed ${notebook.name}.`);
}

/* Renames a tab through a prompt. Deliberately the plainest possible
 * mechanism: an inline-editable tab is nicer and is a genuine pile of
 * focus/blur/Escape handling for something a reader does rarely. */
function renameNotebook(id) {
  const notebook = notebooks.find((nb) => nb.id === id);
  if (!notebook) return;
  const next = prompt("Name for this notebook:", notebook.name);
  if (next === null) return;
  notebook.name = next.trim().slice(0, 40) || notebook.name;
  saveState();
  renderTabs();
  updateFilenameField();
}

/* Draws the tab strip. Hidden entirely while there is only one notebook —
 * a row of tabs containing one tab is chrome that explains nothing, and a
 * reader who never opens a second notebook should never have to look at it
 * (the "+" lives in the toolbar, so there is still a way to get a second
 * one). */
function renderTabs() {
  if (!tabsEl) return;
  tabsEl.replaceChildren();
  tabsEl.hidden = notebooks.length < 2;
  if (notebooks.length < 2) return;

  for (const notebook of notebooks) {
    const tab = document.createElement("div");
    tab.className = "dm-tab";
    if (notebook.id === activeNotebookId) tab.classList.add("dm-tab-active");

    const label = document.createElement("button");
    label.type = "button";
    label.className = "dm-tab-label";
    label.textContent = notebook.name;
    if (notebook.view === VIEWS.FILE) {
      const badge = document.createElement("span");
      badge.className = "dm-tab-view";
      badge.textContent = "file";
      label.append(" ", badge);
    }
    const shown = notebook.view === VIEWS.FILE ? "shown as a file" : "shown as cells";
    label.title = `${notebook.name}, ${shown} — ${notebook.cells.length} cell${notebook.cells.length === 1 ? "" : "s"} (double-click to rename)`;
    label.setAttribute("aria-current", String(notebook.id === activeNotebookId));
    label.addEventListener("click", () => showNotebook(notebook.id));
    label.addEventListener("dblclick", () => renameNotebook(notebook.id));

    const close = document.createElement("button");
    close.type = "button";
    close.className = "dm-tab-close";
    close.textContent = "×";
    close.title = `Close ${notebook.name}`;
    close.setAttribute("aria-label", `Close ${notebook.name}`);
    close.addEventListener("click", (e) => { e.stopPropagation(); closeNotebook(notebook.id); });

    tab.append(label, close);
    tabsEl.appendChild(tab);
  }
}

// ------------------------------------------------------------------- cells

/* Inserts a new, empty cell at a specific position in the notebook (used
 * by the "insert here" dividers between cells) and follows the pattern
 * used everywhere in this file that changes `cells`: update the array,
 * save it, re-render the page to match, then focus the thing that
 * changed. */
function insertCellAt(index, type, content = "") {
  const cell = { id: generateId(), type, content, output: "", error: false };
  cells.splice(index, 0, cell);
  saveState();
  renderCells();
  focusCell(cell.id);
}

/* Adds a cell at the very end — what the toolbar's own "+ Python"/"+ Text"
 * buttons call, as opposed to insertCellAt() directly for an in-between
 * insert. */
function addCell(type, content = "") {
  insertCellAt(cells.length, type, content);
}

/* A small, real tour rather than placeholder text — print, an expression,
 * numpy, a rendered documentation cell, a plot, and check() — run
 * immediately on load so "see it work" actually shows it working rather
 * than leaving a first-time reader to press Run themselves. */
const EXAMPLE_CELLS = [
  { type: CELL_TYPES.PYTHON, content: 'print("Hello from dewmini!")\nanswer = 6 * 7\nanswer' },
  { type: CELL_TYPES.PYTHON, content: "import numpy as np\nreadings = np.array([4, 8, 15, 16, 23, 42])\nreadings.mean()" },
  {
    type: CELL_TYPES.TEXT,
    content:
      "## This is a documentation cell\n\nClick away and it **renders** — click it again to edit.\n\n- Great for notes beside your code\n- Supports `code`, *italic*, and headings",
  },
  {
    type: CELL_TYPES.PYTHON,
    content: 'import matplotlib.pyplot as plt\n\nplt.plot(readings)\nplt.title("Readings")\n\ncheck(answer, 42)',
  },
];

async function loadExampleCells() {
  if (cells.length && !confirm("Replace the current cells with the example? This can't be undone.")) return;
  cells.forEach((c) => c.editor?.destroy());
  setCells(EXAMPLE_CELLS.map((c) => ({ id: generateId(), type: c.type, content: c.content, output: "", error: false })));
  saveState();
  renderCells();
  updateStatus("Example loaded — running it now…");
  await runAllCells();
}

/* Turns a delete button's click into "press once to arm, press again to
 * actually delete". An armed button auto-disarms after a few seconds, on blur, or the moment
 * anything else on the page is clicked, so a stale "one more click
 * deletes this" state never lingers into an accidental delete later. */
function armDeleteButton(btn, onConfirm) {
  if (btn.classList.contains("dm-armed")) {
    clearTimeout(btn._disarmTimer);
    disarmDeleteButton(btn);
    onConfirm();
    return;
  }
  btn.classList.add("dm-armed");
  btn.title = "Click again to delete this cell";
  btn._disarmTimer = setTimeout(() => disarmDeleteButton(btn), 3000);
  const disarmOnOutsideClick = (e) => {
    if (e.target !== btn) disarmDeleteButton(btn);
  };
  // Added after this very click has already finished bubbling —
  // otherwise the same click that arms the button would immediately
  // reach this listener and disarm it again.
  setTimeout(() => document.addEventListener("click", disarmOnOutsideClick, { capture: true, once: true }), 0);
  btn.addEventListener("blur", () => disarmDeleteButton(btn), { once: true });
}

/* Restores a delete button to its normal, unarmed state. */
function disarmDeleteButton(btn) {
  clearTimeout(btn._disarmTimer);
  btn.classList.remove("dm-armed");
  btn.title = "Delete this cell";
}

/* Removes a cell. `.editor?.destroy()` matters: CodeMirror editors hold
 * their own internal state and DOM listeners, and simply removing the
 * wrapping element from the page wouldn't clean those up on its own —
 * calling `.destroy()` first releases them properly. */
function deleteCell(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  cells[idx].editor?.destroy();
  cells.splice(idx, 1);
  saveState();
  renderCells();
  updateStatus("Cell deleted.");
}

/* Inserts a copy of a cell right after itself — the same type and code,
 * but a fresh id and no run history: a duplicate is a starting point for
 * a variation, not a claim that it already ran (planning/CELL_IDENTITY.md
 * §2's header-end group, alongside Delete). */
function duplicateCell(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const original = cells[idx];
  const copy = {
    id: generateId(),
    type: original.type,
    content: original.content,
    output: "",
    error: false,
    collapsed: !!original.collapsed,
  };
  cells.splice(idx + 1, 0, copy);
  saveState();
  renderCells();
  focusCell(copy.id);
  updateStatus("Cell duplicated.");
}

/* Scrolls to a cell, briefly highlights it (the `dm-focused` class, added
 * then removed after 900ms), and puts the cursor in it — used after
 * creating or restoring a cell so a student's eye is drawn to the thing
 * that just changed. Which "put the cursor in it" call happens depends on
 * the cell's current state: a live CodeMirror editor, a live text-cell
 * textarea, or (if the text cell is currently showing its *rendered*
 * form rather than the raw textarea) `showTextEditor()`, which switches
 * it back to editable first. */
function focusCell(id) {
  const el = cellsContainer?.querySelector(`.dm-cell[data-id="${id}"]`);
  const cell = cells.find((c) => c.id === id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "center" });
    el.classList.add("dm-focused");
    setTimeout(() => el.classList.remove("dm-focused"), 900);
  }
  if (cell?.editor) cell.editor.focus();
  else if (cell?.showTextEditor) cell.showTextEditor();
  else if (cell?.textarea) cell.textarea.focus();
}

/* Moves the cursor to the cell after `id` — what Shift+Enter does once the
 * run finishes, so holding it works down a notebook the way it does in
 * Jupyter. At the last cell there is nowhere to advance to, and adding a
 * cell automatically would quietly fill a notebook with empty ones, so it
 * simply stays where it is. */
function focusNextCellAfter(id) {
  const index = cells.findIndex((c) => c.id === id);
  if (index === -1 || index === cells.length - 1) return;
  focusCell(cells[index + 1].id);
}

/* A small, deliberately shallow markdown for documentation cells — headings,
 * bold/italic, inline code, bullets, paragraphs. Not CommonMark: a text
 * cell is a note beside the code, not a document, and the whole point is
 * that a student can read the syntax in the raw textarea at a glance. */
function escapeHtml(text) {
  // Quotes too, not just angle brackets: renderDocInline() below places
  // escaped text inside double-quoted attributes (an image's alt/src), so
  // a raw " in, say, an imported notebook's markdown could otherwise
  // close the attribute early and smuggle in an attribute of its own.
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

/* Handles the "inline" formatting that can appear inside one line of
 * text: `code`, **bold**, *italic*, and an attached image. Each
 * `.replace(regex, ...)` call scans the whole string for one pattern and
 * swaps in the matching HTML — chained one after another, so by the time
 * this returns, every recognized pattern has been turned into markup.
 * Order matters a little here (code before bold/italic, so something
 * inside backticks isn't accidentally read as bold markers), but this
 * function is deliberately simple: it's regex substitution, not a real
 * parser, which is exactly right for the small, fixed set of things a
 * documentation cell needs to format (see this section's own comment on
 * why a full Markdown implementation isn't the goal here). */
function renderDocInline(text) {
  return text
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    // Only a data: URL — the one thing the "insert image" button ever
    // writes — not an arbitrary remote image, which would need its own
    // loading and trust story this cell type has no reason to take on.
    .replace(/!\[([^\]]*)\]\((data:[^)\s]+)\)/g, '<img alt="$1" src="$2" loading="lazy">')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>")
    .replace(/(^|[^\w])_([^_\n]+)_(?!\w)/g, "$1<em>$2</em>");
}

// A modest cap on an attached image's raw file size — comfortably inside a
// browser's localStorage quota even after base64 inflates it by a third,
// since cells (images included) save to localStorage on every change.
const MAX_DOC_IMAGE_BYTES = 3 * 1024 * 1024;

/* Opens a native file picker limited to images, reads the pick as a data
 * URL, and hands it to `onDataUrl` — used by a documentation cell's
 * "insert image" button. A fresh, unattached `<input>` per call rather
 * than one kept around, so nothing lingers referencing a stale cell. */
function pickImageFile(onDataUrl) {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.addEventListener("change", () => {
    const file = input.files && input.files[0];
    if (!file) return;
    if (file.size > MAX_DOC_IMAGE_BYTES) {
      updateStatus(`That image is too large to attach (max ${Math.round(MAX_DOC_IMAGE_BYTES / (1024 * 1024))} MB).`, "error");
      return;
    }
    const reader = new FileReader();
    reader.onload = () => onDataUrl(String(reader.result));
    reader.onerror = () => updateStatus("Couldn't read that image.", "error");
    reader.readAsDataURL(file);
  });
  input.click();
}

// Mirrors build.py's DISPLAY_MATH_RE/INLINE_MATH_RE/ESCAPED_DOLLAR exactly
// (extract_math()'s own comment explains the constraints): display maths
// first so a $$…$$ block is never eaten piecewise by the inline pattern,
// inline maths barred from spanning a line or opening/closing against a
// space (what keeps "it cost $5 or $6" from being read as maths), and a
// literal "\$" escaped out before either regex runs so it survives as a
// plain dollar sign rather than becoming one half of a phantom pair.
const DM_MATH_ESCAPED_DOLLAR = "\0dldollar\0";
const DM_DISPLAY_MATH_RE = /\$\$([\s\S]+?)\$\$/g;
const DM_INLINE_MATH_RE = /\$(?!\s)([^$\n]+?)(?<!\s)\$/g;

/* Lifts $…$ and $$…$$ out of a text cell's raw markdown before any of
 * this file's own hand-written parsing below sees it, leaving a bare
 * alphanumeric placeholder (`dlmath0z`, `dlmath1z`, …) in their place —
 * the same extract-then-restore trick build.py's own extract_math()/
 * render_math() use for tutorial markdown (DECISIONS_LOG.md 7.107),
 * *ported* into JavaScript rather than merely called from it: this file's
 * markdown never goes anywhere near build.py's Python side, so there is
 * no function to reuse, only the pattern. Extracting first is what keeps
 * renderDocInline()'s own bold/italic rules from mangling raw TeX —
 * `$a_i$` losing its underscore to *emphasis*, `$x^2$` losing its caret
 * to nothing — the same failure build.py's own comment warns about for
 * python-markdown. A bare alphanumeric placeholder can't itself trigger
 * any of those rules, so nothing is left in the text for them to catch. */
function extractDocMath(text) {
  const found = [];
  let body = text.split("\\$").join(DM_MATH_ESCAPED_DOLLAR);
  body = body.replace(DM_DISPLAY_MATH_RE, (_match, tex) => {
    found.push({ tex: tex.trim(), display: true });
    return `dlmath${found.length - 1}z`;
  });
  body = body.replace(DM_INLINE_MATH_RE, (_match, tex) => {
    found.push({ tex: tex.trim(), display: false });
    return `dlmath${found.length - 1}z`;
  });
  return { body: body.split(DM_MATH_ESCAPED_DOLLAR).join("$"), found };
}

/* A marked span, the same shape build.py's own render_math() emits for a
 * tutorial. KaTeX replaces its contents in the browser once it has
 * loaded (renderMathsIn() below); until then, and permanently without
 * JavaScript, the span shows its own escaped source TeX — a far better
 * fallback than a blank gap. */
function renderDocMathSpan(item) {
  const classes = item.display ? "dl-math dl-math-display" : "dl-math";
  return `<span class="${classes}">${escapeHtml(item.tex)}</span>`;
}

/* Turns a whole text cell's raw content into rendered HTML, line by
 * line. This is a small hand-written line-based parser: it walks the
 * text one line at a time, keeping track of whether a bullet list or a
 * paragraph is currently "open," and decides what to do based on what
 * kind of line it just read (a heading, a bullet, a blank line, or plain
 * text to add to the current paragraph). `para` collects the lines of an
 * in-progress paragraph until something ends it (a blank line, a heading,
 * a bullet, or the end of the text), at which point `flushPara()` joins
 * them into one `<p>` and starts fresh. `closeList()` does the same job
 * for a `<ul>` that's currently open. Calling `escapeHtml()` on the whole
 * text *before* any of this runs is what keeps a student's literal `<` or
 * `&` in their notes from being misread as real HTML.
 *
 * Maths runs first, on the raw, unescaped `text` — extractDocMath() has
 * to see real "$" characters, which escapeHtml() never touches anyway,
 * but doing this before the line-by-line pass is what lets a display
 * `$$…$$` block spanning several lines collapse to one placeholder before
 * the parser ever gets a chance to read those lines as separate
 * paragraphs. The placeholders extractDocMath() leaves behind are restored
 * to real `<span>` markup only at the very end, after both escapeHtml()
 * and renderDocInline() have already run — see extractDocMath()'s own
 * comment for why that ordering is what keeps the TeX intact. */
function renderDocMarkdown(text) {
  const { body, found } = extractDocMath(text);
  const out = [];
  let listOpen = false;
  let para = [];
  const closeList = () => { if (listOpen) { out.push("</ul>"); listOpen = false; } };
  const flushPara = () => { if (para.length) { out.push(`<p>${renderDocInline(para.join(" "))}</p>`); para = []; } };

  for (const raw of escapeHtml(body).split("\n")) {
    const line = raw.trim();
    const heading = line.match(/^(#{1,3})\s+(.*)$/);
    if (heading) {
      flushPara();
      closeList();
      const level = heading[1].length + 3; // # -> h4 .. ### -> h6
      out.push(`<h${level}>${renderDocInline(heading[2])}</h${level}>`);
      continue;
    }
    const bullet = line.match(/^[-*]\s+(.*)$/);
    if (bullet) {
      flushPara();
      if (!listOpen) { out.push("<ul>"); listOpen = true; }
      out.push(`<li>${renderDocInline(bullet[1])}</li>`);
      continue;
    }
    if (!line) {
      flushPara();
      closeList();
      continue;
    }
    para.push(line);
  }
  flushPara();
  closeList();
  let html = out.join("\n") || '<p class="dm-doc-empty">Empty note.</p>';
  found.forEach((item, i) => { html = html.split(`dlmath${i}z`).join(renderDocMathSpan(item)); });
  return html;
}

// Loaded once, lazily, the first time any rendered text cell actually
// turns out to contain maths — never at boot, and never fetched again
// after the first successful load. The same trade tutorial pages make in
// assets/tutorial-runtime.js's own renderMaths() (DECISIONS_LOG.md 1.8),
// just gated differently: a tutorial page knows at build time, from its
// manifest, whether it has maths; dewmini doesn't know until a reader
// writes some, since a cell's content isn't decided until then. Kept as a
// promise, not a boolean, so two text cells rendering maths for the first
// time at once still share one fetch rather than racing two.
let katexRenderMathPromise = null;
function loadKatexRenderMath() {
  if (!katexRenderMathPromise) {
    katexRenderMathPromise = import("../assets/vendor/katex.bundle.js")
      .then((mod) => mod.renderMath)
      .catch((err) => {
        console.error("dewmini: KaTeX failed to load; maths stays as source TeX", err);
        katexRenderMathPromise = null; // let the next attempt (a later cell, a retry) try again
        throw err;
      });
  }
  return katexRenderMathPromise;
}

/* Renders every `.dl-math` span inside `container` in place, loading
 * KaTeX first if this is the first maths seen so far. Every caller below
 * fires this and moves on rather than awaiting it: a text cell already
 * reads fine as source TeX (render_math()'s own fallback) while this is
 * in flight, or if it fails outright — a blocked CDN, an offline copy
 * built without the bundle — so nothing here should ever hold up showing
 * the rest of a note. renderMath() itself (assets/vendor/katex.bundle.js)
 * never throws for a single bad expression; it marks that one span
 * `dl-math-error` and carries on, so one broken formula can't blank out
 * an otherwise-fine note. */
async function renderMathsIn(container) {
  const spans = container.querySelectorAll(".dl-math");
  if (!spans.length) return;
  let renderMath;
  try {
    renderMath = await loadKatexRenderMath();
  } catch {
    return;
  }
  for (const span of spans) {
    renderMath(span, span.textContent, span.classList.contains("dl-math-display"));
  }
}

/* Which view the active notebook is showing. */
/* Opens a file from the workspace in a tab of its own.
 *
 * A .py opens in the file view, because a file is what it is, and the
 * reader should see the thing they are learning to write. A .ipynb opens
 * as cells, because that format carries outputs and cells are what shows
 * them. Anything else stays where it is: dewmini would have to guess how
 * to read a .csv as code, and guessing wrong turns a data file into one
 * long broken cell.
 *
 * The tab remembers which file it came from, so editing it writes back to
 * the workspace rather than to a download. That is the difference between
 * a file manager and an import button. */
async function openWorkspaceFile(name) {
  const lower = name.toLowerCase();
  const isPy = lower.endsWith(".py");
  const isIpynb = lower.endsWith(".ipynb");
  if (!isPy && !isIpynb) {
    updateStatus(`dewmini opens .py and .ipynb files. ${name} stays in the workspace for a cell to read.`, "error");
    return;
  }

  const already = notebooks.find((nb) => nb.path === name);
  if (already) { showNotebook(already.id); return; }

  let text;
  try {
    text = await dfs.readFile(name, "utf8");
  } catch (err) {
    updateStatus(`Couldn't open ${name}: ${err.message}`, "error");
    return;
  }

  let imported;
  try {
    imported = isIpynb ? parseIpynbCells(text) : parsePyCells(text);
  } catch (err) {
    updateStatus(`Couldn't read ${name}: ${err.message}`, "error");
    return;
  }

  const notebook = makeNotebook(notebookNameFor(name), imported,
                                isPy ? VIEWS.FILE : VIEWS.CELLS);
  notebook.path = name;
  openNotebook(notebook);
  updateViewSwitch();
  updateStatus(`Opened ${name}. Edits here save back to the workspace.`, "ok");
}

/* Writes a tab that came from the workspace back to the file it came
 * from, in the format that file already is.
 *
 * Debounced, because saveState() runs on every keystroke and a filesystem
 * write is not free. Nothing here reports success: a save that worked is
 * not news, and the status line is where a run says what it did. */
let workspaceWriteTimer = null;
function scheduleWorkspaceWrite(notebook) {
  if (!notebook?.path) return;
  clearTimeout(workspaceWriteTimer);
  workspaceWriteTimer = setTimeout(() => writeNotebookToWorkspace(notebook), 600);
}

async function writeNotebookToWorkspace(notebook) {
  if (!notebook?.path) return;
  const text = notebook.path.toLowerCase().endsWith(".ipynb")
    ? JSON.stringify(cellsToIpynb(notebook.cells), null, 2)
    : cellsToPercentText(notebook.cells);
  try {
    await dfs.writeFile(notebook.path, text);
  } catch (err) {
    updateStatus(`Couldn't save ${notebook.path}: ${err.message}`, "error");
    return;
  }
  renderFileList();
}

function currentView() {
  return activeNotebook()?.view === VIEWS.FILE ? VIEWS.FILE : VIEWS.CELLS;
}

/* Parsed cells, carrying forward the id and output of every cell the edit
 * did not change.
 *
 * This is the whole reason editing in the file view is safe. parsePyCells()
 * mints a fresh id for every cell it reads, and a cell id is the key its
 * saved output lives under, so re-parsing naively would throw away every
 * result in the notebook each time a reader switched views. Matching first
 * at the same position and then anywhere means an unchanged cell keeps its
 * id, its output and its collapsed state, while a cell whose code the
 * reader actually edited starts clean — which is right, because its old
 * output no longer belongs to it. */
function mergeParsedCells(oldCells, parsed) {
  const spare = oldCells.map((cell, index) => ({ cell, index, used: false }));
  const same = (slot, next) => !slot.used && slot.cell.type === next.type
                               && slot.cell.content === next.content;
  return parsed.map((next, i) => {
    const hit = spare.find((slot) => slot.index === i && same(slot, next))
             || spare.find((slot) => same(slot, next));
    if (!hit) return next;
    hit.used = true;
    return { ...next, id: hit.cell.id, output: hit.cell.output,
             error: hit.cell.error, collapsed: hit.cell.collapsed };
  });
}

/* Turns what the file editor is showing back into cells. Deliberately does
 * not re-render: while the file view is open the editor owns the screen,
 * and redrawing it under the reader would take their cursor with it. */
function commitFileText(text) {
  clearTimeout(fileParseTimer);
  fileParseTimer = null;
  setCells(mergeParsedCells(cells, parsePyCells(text)));
  saveState();
}

/* Pulls whatever the file editor holds back into the cells before anything
 * reads them. Called by every path that leaves the file view or acts on
 * the notebook as a whole; a no-op in the cells view. */
function flushFileEditor() {
  if (fileEditor) commitFileText(fileEditor.getValue());
}

function destroyFileEditor() {
  if (!fileEditor) return;
  clearTimeout(fileParseTimer);
  fileParseTimer = null;
  fileEditor.destroy();
  fileEditor = null;
  fileRunOutputEl = null;
}

/* Switches the active notebook between the two views. */
function setView(view) {
  const notebook = activeNotebook();
  if (!notebook || notebook.view === view) return;
  flushFileEditor();
  notebook.view = view;
  saveState();
  renderCells();
  renderTabs();
  updateViewSwitch();
}

/* Keeps the toolbar's two buttons showing which view is on. */
function updateViewSwitch() {
  const view = currentView();
  const cellsBtn = document.getElementById("dm-view-cells");
  const fileBtn = document.getElementById("dm-view-file");
  cellsBtn?.setAttribute("aria-pressed", String(view === VIEWS.CELLS));
  fileBtn?.setAttribute("aria-pressed", String(view === VIEWS.FILE));
  cellsBtn?.classList.toggle("dm-viewswitch-on", view === VIEWS.CELLS);
  fileBtn?.classList.toggle("dm-viewswitch-on", view === VIEWS.FILE);
}

/* The notebook as one Python document: a single editor over the whole
 * percent-format text, with one output area beneath it for a whole-file
 * run. */
function renderFileView() {
  const wrap = document.createElement("div");
  wrap.className = "dm-fileview";

  const head = document.createElement("div");
  head.className = "dm-fileview-head";
  const note = document.createElement("p");
  note.className = "dm-fileview-note";
  note.textContent = "One Python file. The # %% lines mark where one cell "
    + "ends and the next begins. Run works through the whole file from the "
    + "top, the way running a file at a command line does.";
  const runBtn = document.createElement("button");
  runBtn.type = "button";
  runBtn.className = "dm-tool dm-tool-accent dm-fileview-run";
  runBtn.textContent = "Run the file";
  runBtn.addEventListener("click", () => runWholeFile());
  head.append(note, runBtn);

  const editorEl = document.createElement("div");
  editorEl.className = "dm-fileview-editor";

  const output = document.createElement("div");
  output.className = "dm-output dm-empty dm-fileview-output";
  fileRunOutputEl = output;

  wrap.append(head, editorEl, output);
  cellsContainer.appendChild(wrap);

  fileEditor = createCodeEditor(editorEl, cellsToPercentText(cells), {
    dark: isDarkNow(),
    /* Committed on a pause rather than on every keystroke. Parsing
     * half-typed text would churn the cells for no gain, and the editor
     * holds the text meanwhile, so nothing is lost if the reader keeps
     * going. Every path that needs the cells up to date calls
     * flushFileEditor() first. */
    onChange: (text) => {
      clearTimeout(fileParseTimer);
      fileParseTimer = setTimeout(() => commitFileText(text), 400);
    },
    completeNames: engine.pageNamesCompletion,
    getDoc: engine.hoverDoc,
    getSignature: engine.signatureHelp,
  });

  if (emptyEl) emptyEl.hidden = true;
}

/* Runs the whole document top to bottom as one unit, which is the point of
 * the file view: a file always runs in the order it is written, and a
 * notebook does not. */
async function runWholeFile() {
  if (running || !fileEditor) return;
  flushFileEditor();
  const source = fileEditor.getValue();
  if (!source.trim()) { updateStatus("Nothing to run.", "error"); return; }
  running = true;
  updateStatus("Running the file…");
  try {
    await ensurePyodide();
    fileRunOutputEl?.classList.remove("dm-empty");
    const { ok } = await engine.runCell(FILE_RUN_ID, source);
    if (fileRunOutputEl && !fileRunOutputEl.innerHTML.trim()) {
      fileRunOutputEl.classList.add("dm-empty");
    }
    updateStatus(ok ? "Ran the file." : "The file stopped on an error.", ok ? "ok" : "error");
  } finally {
    running = false;
    dfs.sync().catch((err) => console.warn("dewmini: filesystem sync after a file run failed", err));
    refreshVariables().catch((err) => console.warn("dewmini: refreshing variables failed", err));
  }
}

function renderCells() {
  if (!cellsContainer) return;
  destroyFileEditor();
  cellsContainer.innerHTML = "";
  if (currentView() === VIEWS.FILE) { renderFileView(); return; }
  // The first seam is drawn even over an empty notebook. It used to be
  // suppressed, because the toolbar carried its own Python/Text buttons and
  // a seam with nothing on either side of it looked like debris. Those
  // buttons are gone now, so suppressing it would leave no way at all to
  // start a *blank* cell — only "Start with imports", which arrives with
  // three lines already in it. Drawing it here also means the affordance a
  // reader will use for every cell after this one is the same affordance
  // they meet for the first.
  cellsContainer.appendChild(createInsertDivider(0));
  cells.forEach((cell, i) => {
    cellsContainer.appendChild(createCellElement(cell));
    cellsContainer.appendChild(createInsertDivider(i + 1));
  });
  if (emptyEl) emptyEl.hidden = cells.length > 0;
}

/* A tappable seam between cells (and before the first, after the last)
 * rather than only a bottom toolbar — the fast way to build a notebook is
 * inserting where you're already looking, not scrolling back down after
 * appending at the end. Full-height and always visible without hover on a
 * touch device, since hover isn't a thing to reveal it with there. */
function createInsertDivider(index) {
  const row = document.createElement("div");
  row.className = "dm-insert";

  const line = document.createElement("div");
  line.className = "dm-insert-line";

  const actions = document.createElement("div");
  actions.className = "dm-insert-actions";

  const addPy = document.createElement("button");
  addPy.type = "button";
  addPy.className = "dm-insert-btn";
  addPy.title = "Insert a Python cell here";
  addPy.innerHTML = '<span class="dm-tool-icon dm-tool-icon-python" aria-hidden="true"></span>Python';
  addPy.addEventListener("click", () => insertCellAt(index, CELL_TYPES.PYTHON));

  const addTxt = document.createElement("button");
  addTxt.type = "button";
  addTxt.className = "dm-insert-btn";
  addTxt.title = "Insert a text cell here";
  addTxt.innerHTML = '<span class="dm-tool-icon dm-tool-icon-text" aria-hidden="true"></span>Text';
  addTxt.addEventListener("click", () => insertCellAt(index, CELL_TYPES.TEXT));

  const addHtml = document.createElement("button");
  addHtml.type = "button";
  addHtml.className = "dm-insert-btn";
  addHtml.title = "Insert an HTML cell here";
  addHtml.innerHTML = '<span class="dm-tool-icon dm-tool-icon-html" aria-hidden="true"></span>HTML';
  addHtml.addEventListener("click", () => insertCellAt(index, CELL_TYPES.HTML));

  const addCss = document.createElement("button");
  addCss.type = "button";
  addCss.className = "dm-insert-btn";
  addCss.title = "Insert a CSS cell here";
  addCss.innerHTML = '<span class="dm-tool-icon dm-tool-icon-css" aria-hidden="true"></span>CSS';
  addCss.addEventListener("click", () => insertCellAt(index, CELL_TYPES.CSS));

  actions.append(addPy, addTxt, addHtml, addCss);
  row.append(line, actions);
  return row;
}

/* Whether a Python cell's output belongs to code that no longer exists on
 * screen: it has run at least once (`ranContent` is set — a cell that has
 * never run has nothing to be stale relative to) and its current content
 * no longer matches what actually produced that output. Any difference
 * counts, whitespace included — a deliberate starting position, not an
 * oversight: the alternative (ignoring whitespace-only edits) would need
 * this to understand what a *meaningful* change is, which is exactly the
 * judgement call it exists to avoid making on a reader's behalf. */
function isStale(cell) {
  return cell.type === CELL_TYPES.PYTHON && cell.ranContent !== undefined && cell.ranContent !== cell.content;
}

/* Updates a cell's on-page "chrome" — the error styling, and (for a
 * Python cell) the run-line — to match its data, without a full re-render
 * of the whole notebook. Called after running a cell (error and staleness
 * both just became current) and on every edit of a cell that has already
 * run once (staleness is the only thing an edit alone can change). */
function updateCellChrome(id) {
  const el = cellsContainer?.querySelector(`.dm-cell[data-id="${id}"]`);
  const cell = cells.find((c) => c.id === id);
  if (!el || !cell) return;
  el.classList.toggle("dm-error", !!cell.error);
  renderCellRunLine(cell);
}

/* Builds the "⋯" menu beside a Python cell's Run button, holding "Run
 * above" and "Run below" (DECISIONS_LOG.md 7.106). These didn't get their
 * own always-visible buttons: the footer bar already carries Run and
 * Clear output, and two more icons on every cell would crowd a row that
 * already earns its keep. A menu keeps the row the same width whether or
 * not a reader ever opens it, at the cost of one extra click to reach
 * either option.
 *
 * The open/close handling here mirrors armDeleteButton() above: a
 * document-level outside-click listener is added only while the menu is
 * open, and removed the moment it closes, rather than one listener kept
 * alive for the cell's whole lifetime — with a menu on every cell, a
 * listener nobody ever removes would be a real per-cell leak, not a
 * theoretical one. */
function createRunMoreMenu(cell) {
  const wrap = document.createElement("div");
  wrap.className = "dm-cell-more";

  const moreBtn = document.createElement("button");
  moreBtn.type = "button";
  moreBtn.className = "dm-icon-btn dm-icon-more";
  moreBtn.title = "More ways to run this cell";
  moreBtn.textContent = "⋯";
  moreBtn.setAttribute("aria-haspopup", "true");
  moreBtn.setAttribute("aria-expanded", "false");

  const menu = document.createElement("div");
  menu.className = "dm-cell-run-menu";
  menu.setAttribute("role", "menu");
  menu.hidden = true;

  let outsideHandler = null;
  const closeMenu = () => {
    menu.hidden = true;
    moreBtn.setAttribute("aria-expanded", "false");
    if (outsideHandler) {
      document.removeEventListener("click", outsideHandler, { capture: true });
      outsideHandler = null;
    }
  };
  const openMenu = () => {
    menu.hidden = false;
    moreBtn.setAttribute("aria-expanded", "true");
    outsideHandler = (e) => { if (!wrap.contains(e.target)) closeMenu(); };
    // Added after this click has finished bubbling, same trick
    // armDeleteButton() uses — otherwise the click that opens the menu
    // would immediately reach this listener and close it again.
    setTimeout(() => document.addEventListener("click", outsideHandler, { capture: true }), 0);
  };
  moreBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    if (menu.hidden) openMenu(); else closeMenu();
  });

  const addItem = (label, title, which, onRun) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "dm-cell-run-menu-item";
    item.setAttribute("role", "menuitem");
    item.dataset.runMenu = which;
    item.title = title;
    item.textContent = label;
    item.addEventListener("click", (e) => {
      e.stopPropagation();
      closeMenu();
      onRun();
    });
    menu.appendChild(item);
  };
  addItem("Run this cell and all above", "Run every cell from the top through this one, from a clean namespace", "above", () => runAbove(cell.id));
  addItem("Run this cell and all below", "Run this cell and every cell after it, keeping what earlier cells defined", "below", () => runBelow(cell.id));

  wrap.append(moreBtn, menu);
  return wrap;
}

// -------------------------------------------------------------- run line
//
// A Python cell's run-line (planning/CELL_IDENTITY.md §3) — one line,
// below the code, folding together whether it has run this session, in
// what order, how long it took, and whether it's stale, rather than the
// three separate signals (a stale badge, a duration line, no order at
// all) dewmini shipped first. A cell that never runs against the shared
// session — text — never gets one; `cell.runLineEl` is simply never set
// for it, and every function below already guards on that.

/* "1st", "2nd", "3rd", "4th", … — the ordinal a run-line reports. */
function formatOrdinal(n) {
  const rem100 = n % 100;
  if (rem100 >= 11 && rem100 <= 13) return `${n}th`;
  switch (n % 10) {
    case 1: return `${n}st`;
    case 2: return `${n}nd`;
    case 3: return `${n}rd`;
    default: return `${n}th`;
  }
}

/* Paints a cell's run-line from its stored state — cell.ranOrder (unset
 * until its first run this session), cell.lastRunMs, and isStale(cell).
 * Also the one place a live ticker gets cancelled: whatever this paints
 * is the truth, so anything still counting up on a stale timer has to
 * stop the moment a real state gets painted over it. */
function renderCellRunLine(cell) {
  const el = cell.runLineEl;
  if (!el) return;
  clearRunLineTicker(cell);
  el.classList.remove("dm-cell-runline-queued");

  if (cell.ranOrder == null) {
    el.textContent = "Not yet run this session";
    el.classList.add("dm-cell-runline-notrun");
    el.classList.remove("dm-cell-runline-stale");
    return;
  }
  el.classList.remove("dm-cell-runline-notrun");

  const showDuration = document.documentElement.getAttribute("data-dm-runstats") !== "off"
    && typeof cell.lastRunMs === "number";
  let html = `<span class="dm-run-order">Ran ${formatOrdinal(cell.ranOrder)}</span>`;
  if (showDuration) html += `<span class="dm-run-duration"> in ${formatRunDuration(cell.lastRunMs)}</span>`;
  const stale = isStale(cell);
  if (stale) html += '<span class="dm-run-flag"> — edited since</span>';
  el.classList.toggle("dm-cell-runline-stale", stale);
  el.innerHTML = html;
}

/* Every cell forgets when (and whether) it last ran — called wherever the
 * interpreter itself gets thrown away or the namespace gets cleared and
 * re-seeded (restartPython(), and runCellBatch() below whenever it's
 * asked to reset first): from that point on, nothing has run yet, in the
 * one sense that actually matters to a reader — this session, against
 * the namespace currently backing the page. */
function resetRunSequence() {
  runSequenceCounter = 0;
  for (const cell of cells) {
    delete cell.ranOrder;
    delete cell.ranContent;
    delete cell.lastRunMs;
    renderCellRunLine(cell);
  }
}

/* Starts (or restarts) a live "Running… Xs" display on a cell's run-line
 * for as long as it's actually executing — a plain setTimeout loop, not
 * an aria-live region: announcing a number changing ten times a second
 * would be noise, not news, to a screen reader. */
function startRunLineTicker(cell) {
  clearRunLineTicker(cell);
  const el = cell.runLineEl;
  if (!el) return;
  el.classList.remove("dm-cell-runline-notrun", "dm-cell-runline-stale", "dm-cell-runline-queued");
  el.classList.add("dm-cell-runline-active");
  const startedAt = performance.now();
  const tick = () => {
    el.textContent = `Running… ${formatRunDuration(performance.now() - startedAt)}`;
    cell._runTicker = setTimeout(tick, 100);
  };
  tick();
}

function clearRunLineTicker(cell) {
  if (cell._runTicker) {
    clearTimeout(cell._runTicker);
    delete cell._runTicker;
  }
  cell.runLineEl?.classList.remove("dm-cell-runline-active");
}

/* Marks a cell as next in line during a batch run (runCellBatch() below)
 * — only ever the one cell right after whichever is currently running,
 * updated as the batch moves along, not the whole remaining list at
 * once. */
function setRunLineQueued(cell) {
  if (!cell.runLineEl) return;
  clearRunLineTicker(cell);
  cell.runLineEl.classList.remove("dm-cell-runline-notrun", "dm-cell-runline-stale");
  cell.runLineEl.classList.add("dm-cell-runline-queued");
  cell.runLineEl.textContent = "Running next";
}

/* Builds one cell's entire DOM tree from a plain `cell` data object —
 * the header row (type pill, Run/Delete/image buttons), the editable
 * area (a CodeMirror editor for a Python cell, a textarea plus a
 * rendered-preview div for a text cell), and the output area. This is
 * the one function that turns "data" into "pixels"; nothing else in the
 * file builds a cell's markup directly. Everything it builds is wired
 * with real event listeners right here too, so a fresh call to this
 * function is enough to produce a fully working cell, ready to be
 * dropped into the page by renderCells(). */
function createCellElement(cell) {
  const wrap = document.createElement("div");
  wrap.className = `dm-cell dm-cell-${cell.type}`;
  wrap.dataset.id = cell.id;
  if (cell.error) wrap.classList.add("dm-error");

  const rail = document.createElement("div");
  rail.className = "dm-cell-rail";

  const main = document.createElement("div");
  main.className = "dm-cell-main";

  // ------------------------------------------------------------- header
  //
  // Identity pill (numbered, coloured by type) on the left; Edit (text
  // only), Duplicate, and Delete on the right (planning/CELL_IDENTITY.md
  // §2, §4). Nothing about running a cell lives here any more — that
  // moved to the footer bar below, next to the code (§5).

  const head = document.createElement("div");
  head.className = "dm-cell-head";
  head.dataset.id = cell.id;

  const cellNumber = cells.indexOf(cell) + 1;
  const pill = document.createElement("span");
  pill.className = "dm-cell-pill";
  // The pill itself is the drag target, not just the dots inside it — it
  // already shows exactly what would be picked up ("Cell 3, Python"), so
  // there's no reason the hit target should be smaller than the label.
  pill.draggable = true;
  pill.title = "Click, hold, and drag — or tap and hold, then drag — to move this cell.";
  const PILL_LABELS = {
    [CELL_TYPES.PYTHON]: "Python", [CELL_TYPES.TEXT]: "Text",
    [CELL_TYPES.HTML]: "HTML", [CELL_TYPES.CSS]: "CSS",
  };
  pill.innerHTML =
    '<span class="dm-cell-pill-dots" aria-hidden="true">&#8942;</span>' +
    `<span class="dm-cell-pill-num">Cell ${cellNumber}</span>` +
    `<span class="dm-cell-pill-type" data-type="${cell.type}">${PILL_LABELS[cell.type]}</span>`;

  const spacer = document.createElement("span");
  spacer.className = "dm-cell-spacer";

  const headerEnd = document.createElement("div");
  headerEnd.className = "dm-cell-header-end";

  // Filled in by the text-cell branch below, since attaching an image
  // needs the textarea/showEditor closures that only exist there. The
  // button itself is built here so it sits in the header row with the
  // rest of headerEnd regardless of where the text-cell branch runs.
  let insertDocImage = null;
  // Same reasoning, for the Edit/View toggle a text cell's header gets:
  // clicking a rendered note to get back to editing it works with a
  // mouse, but has no equivalent affordance on a touch device, which has
  // no hover to reveal that the note is clickable at all. Its label is
  // kept in sync by showEditor()/showRendered().
  let previewBtn = null;
  if (READ_NOT_RUN_TYPES.has(cell.type)) {
    previewBtn = document.createElement("button");
    previewBtn.type = "button";
    previewBtn.className = "dm-icon-btn dm-icon-preview";
    headerEnd.appendChild(previewBtn);
  }
  // Attaching an image from disk only makes sense for a Text cell's own
  // markdown-image syntax — an HTML cell's reader can already write an
  // <img> tag directly, so this stays Text-only.
  if (cell.type === CELL_TYPES.TEXT) {
    const imgBtn = document.createElement("button");
    imgBtn.type = "button";
    imgBtn.className = "dm-icon-btn dm-icon-image";
    imgBtn.title = "Attach an image from your device";
    imgBtn.innerHTML = '<span class="dm-tool-icon dm-tool-icon-image" aria-hidden="true"></span>';
    imgBtn.addEventListener("click", (e) => { e.stopPropagation(); insertDocImage?.(); });
    headerEnd.appendChild(imgBtn);
  }

  const dupBtn = document.createElement("button");
  dupBtn.type = "button";
  dupBtn.className = "dm-icon-btn dm-icon-duplicate";
  dupBtn.title = "Duplicate this cell";
  dupBtn.textContent = "⧉";
  dupBtn.addEventListener("click", (e) => { e.stopPropagation(); duplicateCell(cell.id); });
  headerEnd.appendChild(dupBtn);

  // Arm-then-confirm rather than a native confirm() dialog: a dialog
  // stops the whole page and needs a mouse trip to its own button,
  // where this just needs a second, deliberate press of the same one.
  const delBtn = document.createElement("button");
  delBtn.type = "button";
  delBtn.className = "dm-icon-btn dm-icon-delete";
  delBtn.title = "Delete this cell";
  delBtn.textContent = "×";
  delBtn.addEventListener("click", (e) => { e.stopPropagation(); armDeleteButton(delBtn, () => deleteCell(cell.id)); });
  headerEnd.appendChild(delBtn);

  head.append(pill, spacer, headerEnd);

  // -------------------------------------------------------------- body
  //
  // A collapse triangle beside the editable content — every cell type
  // gets one now, code and text alike: there's nothing type-specific
  // about wanting a long cell out of the way without deleting it. The
  // triangle's own box top-aligns with the first line beside it because
  // both are children of the same flex row (bodyRow), not because either
  // was nudged into place with a margin.

  const bodyRow = document.createElement("div");
  bodyRow.className = "dm-cell-body-row";

  const collapseCol = document.createElement("div");
  collapseCol.className = "dm-cell-collapse-col";
  const collapseBtn = document.createElement("button");
  collapseBtn.type = "button";
  collapseBtn.className = "dm-collapse-toggle";
  // One chevron, rotated by CSS rather than swapped between two glyphs —
  // a filled triangle here reads too much like the Run button's own ▶
  // once the two sit close together in the same corner of the cell.
  collapseBtn.innerHTML = '<span class="dm-collapse-caret" aria-hidden="true">&#8250;</span>';
  collapseCol.appendChild(collapseBtn);

  const contentRegion = document.createElement("div");
  contentRegion.className = "dm-cell-content";

  const collapsedSummary = document.createElement("div");
  collapsedSummary.className = "dm-cell-collapsed-summary";
  collapsedSummary.tabIndex = 0;
  collapsedSummary.addEventListener("click", () => setCollapsed(false));
  collapsedSummary.addEventListener("keydown", (e) => { if (e.key === "Enter") setCollapsed(false); });

  function setCollapsed(collapsed) {
    cell.collapsed = collapsed;
    contentRegion.hidden = collapsed;
    collapsedSummary.hidden = !collapsed;
    collapseBtn.setAttribute("aria-expanded", String(!collapsed));
    collapseBtn.title = collapsed ? "Expand this cell" : "Collapse this cell";
    collapseBtn.classList.toggle("dm-collapse-toggle-collapsed", collapsed);
    if (collapsed) {
      const firstLine = (cell.content.split("\n")[0] || "").trim();
      collapsedSummary.textContent = firstLine || "(empty)";
    }
    saveState();
  }
  collapseBtn.addEventListener("click", (e) => { e.stopPropagation(); setCollapsed(!cell.collapsed); });

  bodyRow.append(collapseCol, contentRegion, collapsedSummary);

  if (cell.type === CELL_TYPES.PYTHON) {
    const editorEl = document.createElement("div");
    editorEl.className = "dm-editor";
    contentRegion.appendChild(editorEl);

    const editor = createCodeEditor(editorEl, cell.content, {
      dark: isDarkNow(),
      onChange: (text) => {
        cell.content = text;
        saveState();
        // The only thing an edit alone can change about a cell's chrome —
        // whether it's now stale relative to its own last-run content
        // (isStale() inside updateCellChrome() reads cell.content fresh,
        // so this reflects every keystroke, not just the ones that
        // happen to trigger a run).
        updateCellChrome(cell.id);
      },
      completeNames: engine.pageNamesCompletion,
      getDoc: engine.hoverDoc,
      getSignature: engine.signatureHelp,
    });
    // Capture phase: CodeMirror's own handler sees Enter first on bubble,
    // so intercepting these has to happen before that, not after.
    //
    // Shift+Enter runs and moves to the next cell; Ctrl/Cmd+Enter runs and
    // stays put. That is the split every notebook tool a student will meet
    // later uses, and dewmini previously had only the first key doing the
    // second key's job — a small thing to relearn twice.
    editorEl.addEventListener("keydown", (e) => {
      if (e.key !== "Enter") return;
      if (e.shiftKey) {
        e.preventDefault();
        e.stopPropagation();
        runCell(cell.id).then(() => focusNextCellAfter(cell.id));
      } else if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        e.stopPropagation();
        runCell(cell.id);
      }
    }, true);
    cell.editor = editor;
  } else if (cell.type === CELL_TYPES.TEXT) {
    const textarea = document.createElement("textarea");
    textarea.className = "dm-textarea";
    textarea.value = cell.content;
    textarea.placeholder = "Notes for this section… (# heading, **bold**, - bullets)";

    const renderEl = document.createElement("div");
    renderEl.className = "dm-doc-render";
    renderEl.tabIndex = 0;
    renderEl.hidden = true;

    const syncPreviewBtn = () => {
      const editing = !textarea.hidden;
      previewBtn.textContent = editing ? "View" : "Edit";
      previewBtn.title = editing ? "Show this note rendered" : "Edit this note";
    };
    const showEditor = () => {
      textarea.hidden = false;
      renderEl.hidden = true;
      textarea.focus();
      syncPreviewBtn();
    };
    const showRendered = () => {
      if (!cell.content.trim()) return; // nothing to render — keep it open for typing
      renderEl.innerHTML = renderDocMarkdown(cell.content);
      // Not awaited: renderMathsIn() already reads fine mid-flight (its own
      // comment explains why), and awaiting it here would leave the rest of
      // the note waiting on a network fetch just to show text that isn't
      // maths at all.
      renderMathsIn(renderEl);
      renderEl.hidden = false;
      textarea.hidden = true;
      syncPreviewBtn();
    };

    textarea.addEventListener("input", (e) => { cell.content = e.target.value; saveState(); });
    textarea.addEventListener("blur", showRendered);
    renderEl.addEventListener("click", showEditor);
    // mousedown, not click, is where this has to happen: a click on
    // previewBtn while the textarea is focused blurs the textarea first
    // (triggering showRendered() above) and only then reaches this
    // handler — by which point textarea.hidden already flipped, so
    // reading it here would toggle straight back to editing instead of
    // landing on rendered. preventDefault() on mousedown stops the
    // textarea from blurring at all, so this handler still sees the
    // state as it was when the reader actually clicked.
    previewBtn.addEventListener("mousedown", (e) => e.preventDefault());
    previewBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (textarea.hidden) showEditor(); else showRendered();
    });

    insertDocImage = () => pickImageFile((dataUrl) => {
      const sep = cell.content && !cell.content.endsWith("\n") ? "\n\n" : "";
      cell.content = `${cell.content}${sep}![image](${dataUrl})\n`;
      textarea.value = cell.content;
      saveState();
      showEditor();
      textarea.setSelectionRange(textarea.value.length, textarea.value.length);
      updateStatus("Image attached.", "ok");
    });
    renderEl.addEventListener("keydown", (e) => { if (e.key === "Enter") showEditor(); });

    contentRegion.append(textarea, renderEl);
    cell.textarea = textarea;
    cell.showTextEditor = showEditor;

    if (cell.content.trim()) showRendered();
    else syncPreviewBtn();
  } else if (cell.type === CELL_TYPES.HTML) {
    const editorEl = document.createElement("div");
    editorEl.className = "dm-editor";
    contentRegion.appendChild(editorEl);

    const renderEl = document.createElement("div");
    renderEl.className = "dm-html-render";
    renderEl.hidden = true;
    contentRegion.appendChild(renderEl);

    // sandbox="allow-scripts" only — no allow-same-origin. Whatever this
    // cell's HTML does, including a <script> tag, it does inside an
    // opaque-origin document that cannot reach this page's own DOM,
    // localStorage, or any other cell — the same isolation a reader's
    // HTML deserves whether they wrote it themselves or it arrived
    // through Settings' "Load a shared cell/notebook" (planning/
    // CELL_IDENTITY.md §8). resize:vertical (see the stylesheet) rather
    // than measuring the frame's own content height: that would need a
    // postMessage handshake from inside the sandboxed document, not
    // worth the complexity for a first version.
    const iframe = document.createElement("iframe");
    iframe.className = "dm-html-frame";
    iframe.setAttribute("sandbox", "allow-scripts");
    iframe.title = `Cell ${cellNumber}'s rendered HTML`;
    renderEl.appendChild(iframe);

    const syncPreviewBtn = () => {
      const editing = !editorEl.hidden;
      previewBtn.textContent = editing ? "View" : "Edit";
      previewBtn.title = editing ? "Show this cell rendered" : "Edit this cell's HTML";
    };
    const showEditor = () => {
      editorEl.hidden = false;
      renderEl.hidden = true;
      editor.focus();
      syncPreviewBtn();
    };
    const showRendered = () => {
      if (!cell.content.trim()) return; // nothing to render — keep it open for typing
      iframe.srcdoc = cell.content;
      renderEl.hidden = false;
      editorEl.hidden = true;
      syncPreviewBtn();
    };

    const editor = createCodeEditor(editorEl, cell.content, {
      dark: isDarkNow(),
      language: "html",
      onChange: (text) => { cell.content = text; saveState(); },
    });
    cell.editor = editor;
    // focusout, not CodeMirror's own updateListener: it fires once focus
    // has actually left the editor's DOM subtree (relatedTarget is the
    // element gaining focus), the same "genuinely done editing" signal a
    // textarea's own blur gives Text cells — CodeMirror's editable
    // element does not dispatch a native blur/focusout of its own that
    // bubbles the way a textarea's does, so this listens one level up.
    editorEl.addEventListener("focusout", (e) => {
      if (!editorEl.contains(e.relatedTarget)) showRendered();
    });

    // No click-to-edit on the rendered view itself, unlike Text — a click
    // inside the iframe is a click inside a different document, and
    // cross-document clicks don't bubble out to this page's listeners.
    // The header's own Edit/View toggle (revealed by hover, same as any
    // other quiet chrome) is the one way in.
    previewBtn.addEventListener("mousedown", (e) => e.preventDefault());
    previewBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (editorEl.hidden) showEditor(); else showRendered();
    });

    if (cell.content.trim()) showRendered();
    else syncPreviewBtn();
  } else if (cell.type === CELL_TYPES.CSS) {
    // Same mechanism as HTML — a CodeMirror source editor, a sandboxed
    // iframe standing in for the rendered view, the same Edit/View
    // toggle — the only two differences are the language mode and what
    // goes in the iframe: CSS_PREVIEW_MARKUP (a fixed little "page") with
    // the reader's own rule in a <style> tag ahead of it, rather than the
    // reader's markup directly.
    const editorEl = document.createElement("div");
    editorEl.className = "dm-editor";
    contentRegion.appendChild(editorEl);

    const renderEl = document.createElement("div");
    renderEl.className = "dm-html-render";
    renderEl.hidden = true;
    contentRegion.appendChild(renderEl);

    const iframe = document.createElement("iframe");
    iframe.className = "dm-html-frame";
    iframe.setAttribute("sandbox", "allow-scripts");
    iframe.title = `Cell ${cellNumber}'s CSS preview`;
    renderEl.appendChild(iframe);

    const syncPreviewBtn = () => {
      const editing = !editorEl.hidden;
      previewBtn.textContent = editing ? "View" : "Edit";
      previewBtn.title = editing ? "Show the preview" : "Edit this cell's CSS";
    };
    const showEditor = () => {
      editorEl.hidden = false;
      renderEl.hidden = true;
      editor.focus();
      syncPreviewBtn();
    };
    const showRendered = () => {
      iframe.srcdoc = `<style>${cell.content}</style>${CSS_PREVIEW_MARKUP}`;
      renderEl.hidden = false;
      editorEl.hidden = true;
      syncPreviewBtn();
    };

    const editor = createCodeEditor(editorEl, cell.content, {
      dark: isDarkNow(),
      language: "css",
      onChange: (text) => { cell.content = text; saveState(); },
    });
    cell.editor = editor;
    editorEl.addEventListener("focusout", (e) => {
      if (!editorEl.contains(e.relatedTarget)) showRendered();
    });

    previewBtn.addEventListener("mousedown", (e) => e.preventDefault());
    previewBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (editorEl.hidden) showEditor(); else showRendered();
    });

    // A brand-new cell starts in the editor, same as HTML/Text — only a
    // cell with something in it already (restored from a save) opens
    // straight to its rendered preview.
    if (cell.content.trim()) showRendered();
    else syncPreviewBtn();
  }

  setCollapsed(!!cell.collapsed);

  // ------------------------------------------------------------ footer
  //
  // Run, clear-output, the "⋯" run-above/below menu, and the run-line —
  // Python only, since these are the only cells that run against the
  // shared session. Sits between the code and the output, at the
  // bottom-left of the cell: a reader's cursor is at the bottom of what
  // they just wrote, not back up at the top, so that's where the next
  // action should be waiting.

  let footbar = null;
  if (cell.type === CELL_TYPES.PYTHON) {
    footbar = document.createElement("div");
    footbar.className = "dm-cell-footbar";

    const runBtn = document.createElement("button");
    runBtn.type = "button";
    runBtn.className = "dm-icon-btn dm-icon-run";
    runBtn.title = "Run this cell (Shift+Enter)";
    runBtn.textContent = "▶";
    runBtn.addEventListener("click", (e) => { e.stopPropagation(); runCell(cell.id); });
    footbar.appendChild(runBtn);
    cell.runBtn = runBtn;

    // Clears this cell's own output without touching its code — the
    // non-destructive counterpart to Delete.
    const resetOutputBtn = document.createElement("button");
    resetOutputBtn.type = "button";
    resetOutputBtn.className = "dm-icon-btn dm-icon-reset-output";
    resetOutputBtn.title = "Clear this cell's output";
    resetOutputBtn.textContent = "↺";
    resetOutputBtn.addEventListener("click", (e) => { e.stopPropagation(); resetCellOutput(cell.id); });
    footbar.appendChild(resetOutputBtn);

    footbar.appendChild(createRunMoreMenu(cell));

    const footSpacer = document.createElement("span");
    footSpacer.className = "dm-cell-spacer";
    footbar.appendChild(footSpacer);

    const runLineEl = document.createElement("div");
    runLineEl.className = "dm-cell-runline";
    footbar.appendChild(runLineEl);
    cell.runLineEl = runLineEl;
    renderCellRunLine(cell);
  }

  const outputEl = document.createElement("div");
  outputEl.className = "dm-cell-output";
  if (cell.output) outputEl.innerHTML = cell.output;
  else outputEl.classList.add("dm-empty");
  cell.outputEl = outputEl;

  main.append(head, bodyRow);
  if (footbar) main.appendChild(footbar);
  main.appendChild(outputEl);
  wrap.append(rail, main);
  return wrap;
}

// -------------------------------------------------------------- execution

/* Whether the page currently reads as dark, taking the reader's explicit
 * theme choice first and falling back to their operating system's own
 * light/dark preference only when they've chosen "system" (no explicit
 * `data-theme` attribute at all). */
function isDarkNow() {
  const t = document.documentElement.getAttribute("data-theme");
  if (t === "dark") return true;
  if (t === "light") return false;
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

/* Fetches tutorial_tools.py's source once and keeps it in
 * `toolsSourceCache` — needed twice (booting Pyodide, and building a
 * standalone HTML export), and there's no reason to fetch the same file
 * over the network a second time within one page visit. */
async function getToolsSource() {
  if (toolsSourceCache) return toolsSourceCache;
  const res = await fetch("../assets/tutorial_tools.py");
  if (!res.ok) throw new Error(`tutorial_tools.py: HTTP ${res.status}`);
  toolsSourceCache = await res.text();
  return toolsSourceCache;
}

/* Wires the shared engine up to this page — getOutputEl looks a cell's
 * live output element up by id (the engine's own event stream addresses
 * cells by id, not by direct element reference, since worker-mode output
 * arrives asynchronously and a cell could in principle be gone by the
 * time it does), onStatus forwards boot/package-loading progress the same
 * way this file's own updateStatus() already shows it, and dataBase is
 * "../data/" rather than the engine's default empty string, since this
 * page lives one directory deeper (compose/, not the site root) and needs
 * the extra "../" to reach the same repo-root data/ folder. Called once, at
 * module load — configure() itself does no booting. */
engine.configure({
  getOutputEl: (cellId) => (cellId === FILE_RUN_ID
    ? fileRunOutputEl
    : cells.find((c) => c.id === cellId)?.outputEl ?? null),
  onStatus: updateStatus,
  packages: DM_PACKAGES,
  dataBase: "../data/",
});

/* Starts Pyodide the first time it's actually needed (the first Run
 * click), not when the page loads — downloading and starting a whole
 * Python interpreter is slow, and a student reading or writing notes
 * shouldn't have to wait for it if they never run a cell. engine.
 * ensureBooted() itself is idempotent and memoized (a second call while
 * still booting returns the same in-flight Promise), so this wrapper only
 * has to add two things on top: showing "Python ready." once, the first
 * time boot actually finishes (engineMode() is still null beforehand),
 * and mounting a filesystem right after — a nice-to-have, not something
 * Python readiness should ever hinge on, so a mount failure here (blocked
 * storage, an unsupported browser, running from file://) is caught and
 * surfaced through the Files section in Settings on its own, never
 * re-thrown. */
async function ensurePyodide() {
  const alreadyBooted = engine.engineMode() !== null;
  await engine.ensureBooted();
  if (!alreadyBooted) updateStatus("Python ready.", "ok");
  updateExecutionStatus();

  try {
    await dfs.init();
  } catch (err) {
    console.warn("dewmini: filesystem mount failed", err);
  }
}

/* Autocomplete, hover docs, and signature help all come straight from the
 * shared engine now (engine.pageNamesCompletion/hoverDoc/signatureHelp,
 * DECISIONS_LOG.md 7.89). New capability for dewmini as a side effect of
 * that move: Jedi-based static-analysis tooltips for code that hasn't run
 * yet, and a signature-help popup, neither of which its own previous
 * live-namespace-only implementation could offer without a Worker. */

/* Runs one cell's code through the shared engine's runCell() (dispatching
 * to tutorial_tools.py's own run_cell(), the same function every dewlab
 * tutorial cell runs through, wherever Pyodide actually lives) and
 * records what happened: the rendered output HTML (so it can be saved
 * and shown again without re-running), and whether it errored. Returns
 * whether the run succeeded, the same true/false run_cell() itself
 * returns.
 *
 * No "Running…" placeholder injected into the output area here anymore
 * (the previous main-thread-only version did) — engine.runCell() already
 * clears the cell's output the moment it starts, and the run/stop state
 * now shows on the cell's own Run button instead (setRunButtonRunning()
 * below). */
async function executeCell(cell) {
  await ensurePyodide();
  const outputEl = cell.outputEl;
  if (!outputEl) return true;
  outputEl.classList.remove("dm-empty");
  const startedAt = performance.now();
  // Captured before the run, not after: the whole point of the run-line's
  // "edited since" flag is "does this output belong to what the cell says
  // right now", so this has to be the content that was actually handed to
  // Python, even in the unusual case where an editor kept accepting
  // keystrokes while a slow cell was still running.
  cell.ranContent = cell.content;
  const { ok } = await engine.runCell(cell.id, cell.content);
  cell.lastRunMs = performance.now() - startedAt;
  cell.ranOrder = ++runSequenceCounter;
  cell.output = outputEl.innerHTML;
  cell.error = !ok;
  allowOutputToSaveAgain(cell.id);
  if (!outputEl.innerHTML.trim()) outputEl.classList.add("dm-empty");
  updateCellChrome(cell.id);
  saveState();
  // Fire-and-forget: a cell's own code may have written straight to the
  // mounted filesystem (dfs.sync()'s own docstring explains why that
  // needs this rather than relying on writeFile()'s debounced sync or
  // the best-effort unload flush alone) — not awaited, so a slow sync
  // never makes a fast cell feel slower than it is.
  dfs.sync()
    // A cell that wrote a file is exactly when the Files list is wrong, and
    // nothing else was redrawing it: a student could write shapes.py, open
    // Files, and not see it until some unrelated thing refreshed the panel.
    .then(() => renderFileList())
    .catch((err) => console.warn("dewmini: filesystem sync after cell run failed", err));
  // Same treatment for the Workbench's variable list: a run is exactly
  // when the namespace changed, so this is when it needs redrawing — but
  // it is a panel a reader may not even have open, and never worth making
  // a cell feel slower for.
  refreshVariables().catch((err) => console.warn("dewmini: refreshing variables failed", err));
  return ok;
}

/* Formats how long a cell's last run took, human-scale rather than raw
 * milliseconds: "340 ms" under a second, "2.4 s" at or above it. */
function formatRunDuration(ms) {
  return ms < 1000 ? `${Math.round(ms)} ms` : `${(ms / 1000).toFixed(1)} s`;
}

/* Clears one cell's output (and its run-line) without touching its code —
 * the non-destructive counterpart to deleting the cell outright. A no-op
 * while something is running, since clearing mid-run would fight the
 * output the running cell is actively writing. */
function resetCellOutput(id) {
  const cell = cells.find((c) => c.id === id);
  if (!cell || cell.type !== CELL_TYPES.PYTHON || running) return;
  const outputEl = cell.outputEl;
  if (outputEl) {
    outputEl.replaceChildren();
    outputEl.classList.add("dm-empty");
  }
  cell.output = "";
  cell.error = false;
  allowOutputToSaveAgain(cell.id);
  delete cell.lastRunMs;
  delete cell.ranContent;
  delete cell.ranOrder;
  updateCellChrome(id);
  saveState();
}

/* Toolbar-level "Clear output" — resets every Python cell's output,
 * keeping every cell and its code. Distinct from the existing "Clear"
 * button, which deletes every cell. */
function clearAllOutputs() {
  cells.forEach((cell) => { if (cell.type === CELL_TYPES.PYTHON) resetCellOutput(cell.id); });
  updateStatus("Output cleared.");
}

/* Toggles a cell's own Run button into its running/Stop state. When a
 * genuine interrupt buffer is available (worker mode, cross-origin
 * isolated — engine.canStop()) the button becomes a real Stop; otherwise
 * it just shows the cell is busy, since there is nothing to interrupt
 * (a main-thread fallback blocks this same thread completely once a
 * cell starts, with no opportunity for an interrupt to even be noticed). */
function setRunButtonRunning(runBtn) {
  if (!runBtn) return;
  if (engine.canStop()) {
    runBtn.disabled = false;
    runBtn.textContent = "■";
    runBtn.title = "Stop this cell";
    runBtn.classList.add("dm-icon-run-stop");
  } else {
    runBtn.disabled = true;
    runBtn.textContent = "…";
    runBtn.title = "Running…";
  }
}

/* Restores a cell's Run button once it finishes (or fails to) run. */
function resetRunButton(runBtn) {
  if (!runBtn) return;
  runBtn.disabled = false;
  runBtn.classList.remove("dm-icon-run-stop");
  runBtn.title = "Run this cell (Shift+Enter)";
  runBtn.textContent = "▶";
}

/* Runs a single cell by id, in response to its own Run button or
 * Shift+Enter. A second click on the cell that is already running sends
 * a Stop (interrupt) request instead of starting a new run — the same
 * button in its Stop state. `running` guards against
 * overlapping runs from two different cells: dewmini has one Python
 * interpreter, so only one cell can actually be executing at a time; a
 * click on a *different* cell while one is already running is ignored
 * rather than queued. */
async function runCell(id) {
  if (runningCellId === id) {
    engine.requestInterrupt();
    return;
  }
  if (running) return;
  const cell = cells.find((c) => c.id === id);
  if (!cell || cell.type !== CELL_TYPES.PYTHON) return;
  running = true;
  runningCellId = id;
  try {
    // Boot (or reconnect to an already-booted) engine *before* deciding
    // what the Run button should look like — engine.canStop(), which
    // setRunButtonRunning() reads, only knows worker-vs-main-thread once
    // ensureBooted() has actually resolved, so the await has to come
    // first, not only inside executeCell() below.
    // Skipping this step showed up as a real bug in testing: canStop()
    // read false (its pre-boot default) on every cell's first-ever run,
    // showing the *non-stoppable* "…" busy state even in worker mode.
    await ensurePyodide();
    await checkImportedFiles();
    setRunButtonRunning(cell.runBtn);
    startRunLineTicker(cell);
    const ok = await executeCell(cell);
    updateStatus(ok ? "Ran." : "Error — see the cell.", ok ? "ok" : "error");
  } catch (err) {
    updateStatus(`Python isn't available: ${err.message}`, "error");
  } finally {
    running = false;
    runningCellId = null;
    resetRunButton(cell.runBtn);
    clearRunLineTicker(cell);
  }
}

/* Runs a batch of Python cells in order — the shared engine behind "Run
 * all", "Run above", and "Run below" below, which differ only in *which*
 * cells they hand it and whether the namespace gets cleared first.
 *
 * `reset` matters more than it looks: "Run all" and "Run above" both
 * start from `engine.resetPageState()` (clearing and re-seeding the
 * shared namespace, cheaper than a full restart), because the whole point
 * of running from the top is that "what's on screen matches what the code
 * actually did" — without the reset, a stale value from a previous run
 * could linger and mask a cell that no longer defines something it used
 * to. "Run below" must *not* reset: its whole point is to keep what the
 * cells above it already defined, so resetting first would throw away
 * exactly the state it exists to preserve.
 *
 * Each cell's own Run button becomes a Stop button while it's its turn,
 * the same as running it individually, so a runaway cell partway through
 * a batch can still be interrupted without losing the cells that already
 * ran. */
async function runCellBatch(pythonCells, { reset, emptyMessage, describe }) {
  if (running) return;
  if (!pythonCells.length) { updateStatus(emptyMessage); return; }

  running = true;
  const btn = document.getElementById("run-all");
  if (btn) btn.disabled = true;

  try {
    await ensurePyodide();
    // Once for the whole batch, not once per cell: the answer would be
    // the same every time and each ask is a round trip.
    await checkImportedFiles();
    if (reset) {
      await engine.resetPageState();
      resetRunSequence();
    }
    updateStatus(describe(pythonCells.length));
    // Only ever the one cell right after whichever is about to run, kept
    // current as the batch moves along below — not the whole remaining
    // list marked "next" at once.
    if (pythonCells[1]) setRunLineQueued(pythonCells[1]);

    let errors = 0;
    for (let i = 0; i < pythonCells.length; i++) {
      const cell = pythonCells[i];
      runningCellId = cell.id;
      setRunButtonRunning(cell.runBtn);
      startRunLineTicker(cell);
      /* try/finally per cell: if a
       * run rejects rather than returning false — which is exactly what
       * restarting Python mid-batch now does, since restart() rejects what
       * was in flight — this cell's button would otherwise be left showing
       * "running" forever while the batch unwound past it. */
      try {
        const ok = await executeCell(cell);
        if (!ok) errors += 1;
      } finally {
        resetRunButton(cell.runBtn);
        clearRunLineTicker(cell);
      }
      const next = pythonCells[i + 1];
      if (next) setRunLineQueued(next);
    }
    updateStatus(
      errors ? `Done — ${errors} cell${errors === 1 ? "" : "s"} errored.` : "All cells ran cleanly.",
      errors ? "error" : "ok"
    );
  } catch (err) {
    updateStatus(`Python isn't available: ${err.message}`, "error");
  } finally {
    running = false;
    runningCellId = null;
    if (btn) btn.disabled = false;
  }
}

/* Runs every Python cell in order, top to bottom — "Run all." */
async function runAllCells() {
  // In the file view there are no cells on screen to run one at a time,
  // and the file runs top to bottom as one thing.
  if (currentView() === VIEWS.FILE) { await runWholeFile(); return; }
  await runCellBatch(cells.filter((c) => c.type === CELL_TYPES.PYTHON), {
    reset: true,
    emptyMessage: "No Python cells to run.",
    describe: (n) => `Running ${n} cell${n === 1 ? "" : "s"}…`,
  });
}

/* "Run above": every Python cell from the top through (and including)
 * `id`, from a clean namespace — the honest fix once a cell partway down
 * has been edited and everything before it needs re-proving, without
 * paying to re-run whatever comes after it too. */
async function runAbove(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const slice = cells.slice(0, idx + 1).filter((c) => c.type === CELL_TYPES.PYTHON);
  await runCellBatch(slice, {
    reset: true,
    emptyMessage: "No Python cells above this one to run.",
    describe: (n) => `Running the ${n} cell${n === 1 ? "" : "s"} above and including this one…`,
  });
}

/* "Run below": `id` and every Python cell after it, keeping whatever
 * earlier cells already defined — the way to redo a slow computation's
 * downstream steps without paying to redo the computation itself. See
 * runCellBatch()'s own comment for why this is the one caller that must
 * not reset the namespace first. */
async function runBelow(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const slice = cells.slice(idx).filter((c) => c.type === CELL_TYPES.PYTHON);
  await runCellBatch(slice, {
    reset: false,
    emptyMessage: "No Python cells here or below to run.",
    describe: (n) => `Running the ${n} cell${n === 1 ? "" : "s"} from here on…`,
  });
}

/* ------------------------------------------------- imported .py files
 *
 * A student who writes shapes.py in the workspace and imports it in a
 * cell meets a specific, confusing failure the first time they edit that
 * file. Python keeps every module it has imported in `sys.modules` and
 * hands back the remembered one rather than reading the file again, so
 * the corrected function is not the one that runs. The answer does not
 * change, and nothing on screen says why.
 *
 * dewmini tells them, and offers to re-read the files. It does not
 * re-read silently: module caching is real Python behaviour they will
 * meet in every other environment they ever use, and a student who has
 * met it here with an explanation is better placed than one for whom it
 * was quietly papered over. Restarting Python instead would be correct
 * and far too slow for a one-character edit. */

// Module names currently shown in the notice, so its button knows what to
// re-read without asking Python a second time.
let staleImportNames = [];

/* Asks whether any workspace file already imported has been edited since
 * Python read it, and shows the notice if so.
 *
 * Cheap to call and safe to call often: with nothing mounted there is no
 * import path to have imported from, so this returns without a round
 * trip at all. Never throws — it drives a notice, and a page that cannot
 * ask simply does not show one. */
async function checkImportedFiles() {
  if (!dfs.getBackend()) return;
  const changed = await engine.changedImportedModules(dfs.mountPoint());
  if (changed.length) showStaleImportsNotice(changed);
}

/* Names the edited files and says what to do about them. Deliberately
 * concrete about which files: "a module changed" would send a student
 * looking through everything they have open. */
function showStaleImportsNotice(names) {
  staleImportNames = names;
  const notice = document.getElementById("stale-imports-notice");
  const text = document.getElementById("stale-imports-text");
  if (!notice || !text) return;
  const files = names.map((n) => `${n}.py`).join(", ");
  text.textContent = names.length === 1
    ? `You have edited ${files} since Python read it. Python is still using the version it read first, so your change is not in what runs.`
    : `You have edited these since Python read them: ${files}. Python is still using the versions it read first, so your changes are not in what runs.`;
  notice.hidden = false;
}

function hideStaleImportsNotice() {
  staleImportNames = [];
  const notice = document.getElementById("stale-imports-notice");
  if (notice) notice.hidden = true;
}

/* Re-reads the edited modules, then says what happened.
 *
 * The warning about `from … import …` is not a footnote. Reloading
 * replaces what is inside the module object; a name the student imported
 * *out* of it still points at the old function, because that binding
 * lives in their own namespace. Someone who re-reads the file, runs the
 * cell, and still sees the old answer has been told nothing useful
 * unless this is said. */
async function reloadStaleImports() {
  const names = staleImportNames.slice();
  if (!names.length) { hideStaleImportsNotice(); return; }
  hideStaleImportsNotice();
  updateStatus("Re-reading…");
  let result;
  try {
    result = await engine.reloadModules(names);
  } catch (err) {
    updateStatus(`Couldn't re-read those files: ${err.message}`, "error");
    return;
  }
  if (result.failed.length) {
    const first = result.failed[0];
    updateStatus(`${first.name}.py could not be read: ${first.error}`, "error");
    return;
  }
  const many = result.reloaded.length !== 1;
  updateStatus(
    `Re-read ${result.reloaded.map((n) => `${n}.py`).join(", ")}. `
    + `If you wrote \`from ${result.reloaded[0]} import …\`, run that line again too — `
    + `${many ? "those names" : "that name"} still point at the old version.`,
    "ok"
  );
}

// -------------------------------------------------------------- downloads

/* Reads the reader's chosen filename from Settings, cleaned up for use
 * as an actual filename: any extension they typed is stripped (each
 * download function adds its own), and characters that aren't valid in
 * a filename on at least one common operating system (`\ / : * ? " < >
 * |`) are replaced with a dash, so the same name works whether the
 * download lands on Windows, macOS, or Linux. */
function getFilenameBase() {
  let name = (activeNotebook()?.name || "").trim();
  if (!name) name = "dewmini-notebook";
  name = name.replace(/\.(py|html?|ipynb)$/i, "");
  name = name.replace(/[\\/:*?"<>|]+/g, "-").trim();
  return name || "dewmini-notebook";
}

/* Keeps the Settings filename box, the browser tab title, and the tab strip
 * all saying the same thing — because since tabs, they are all one thing: a
 * notebook's name *is* its export filename. Two separate ideas (a tab called
 * one thing downloading as another) would be a small, permanent confusion
 * for no gain. */
function updateFilenameField() {
  const el = document.getElementById("dm-filename");
  if (el) el.value = activeNotebook()?.name || "";
  document.title = `${getFilenameBase()} — dewmini`;
}

/* Wires the filename box to rename the notebook it belongs to. */
function initFilename() {
  const el = document.getElementById("dm-filename");
  if (!el) return;
  updateFilenameField();
  el.addEventListener("input", () => {
    const notebook = activeNotebook();
    if (!notebook) return;
    notebook.name = el.value.trim().slice(0, 40) || notebook.name;
    document.title = `${getFilenameBase()} — dewmini`;
    saveState();
    renderTabs();
  });
}

/* The standard trick for making the browser download a file that only
 * ever existed in memory: a Blob wraps the content as an in-memory
 * file-like object, `URL.createObjectURL` gives it a temporary URL the
 * browser treats as a real download link, and a plain `<a download>`
 * clicked programmatically triggers the download exactly as a real click
 * would. `URL.revokeObjectURL` at the end releases that temporary URL
 * once it's no longer needed. Every download function below (Python,
 * ipynb, HTML) funnels through this one function. */
function triggerDownload(filename, content, mime) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

/* Joins every cell into one plain .py file: a Python cell's code goes in
 * as-is, and a text cell's content gets turned into `#`-prefixed comment
 * lines, so the whole notebook reads as one ordinary, runnable Python
 * script — no special notebook format needed to open it.
 *
 * The cell markers are the percent format: `# %%` before a code cell and
 * `# %% [markdown]` before a text cell. This replaces markers dewmini
 * invented for itself ("# ---- cell 1 ----"), which no other program
 * understood. Jupytext, Visual Studio Code, Spyder and PyCharm all read
 * the percent format, so a file written here opens as the same cells on
 * a machine that has never heard of dewlab — which is the only thing
 * that makes teaching a student to work in files worth doing.
 *
 * `# %%` explains nothing to a beginner, where the old markers almost
 * explained themselves. That is why the file opens with a few lines
 * saying what the markers are for, as a text cell the student can delete
 * once they no longer need it. Inside dewmini they never see a marker at
 * all: the cells are the markers.
 *
 * parsePyCells() reads exactly what this writes, so a downloaded .py
 * loads straight back into the same cells, notes included. */
const PY_CELL_MARKER = "# %%";
const PY_TEXT_MARKER = "# %% [markdown]";
// The first line of the header block below. parsePyCells() matches this
// exact opening to tell dewmini's own header from a leading comment a
// file written elsewhere came with — a licence notice, say, which must
// be kept. Change one and change the other.
const PY_HEADER_OPENING = "# dewmini export";

/* A list of cells as one percent-format Python document: `# %%` before a
 * code cell, `# %% [markdown]` before a text cell, whose lines are then
 * commented out.
 *
 * No explanatory header. downloadAsPython() adds one, because a file
 * leaving here is read by somebody who has never seen the convention. The
 * file *view* deliberately does without: its header would carry today's
 * date, so regenerating it on every switch between the two views would
 * look to the reader like an edit they did not make. */
function cellsToPercentText(cellList) {
  const parts = [];
  cellList.forEach((cell) => {
    if (cell.type === CELL_TYPES.TEXT) {
      parts.push(PY_TEXT_MARKER);
      cell.content.split("\n").forEach((line) => parts.push(`# ${line}`.trimEnd()));
    } else {
      parts.push(PY_CELL_MARKER, cell.content);
    }
    parts.push("");
  });
  return parts.join("\n");
}

function downloadAsPython() {
  flushFileEditor();
  if (!cells.length) { updateStatus("No cells to export.", "error"); return; }
  // The header sits *before* the first marker, so it is not a cell.
  // Written as a cell it would come back as one on the next import, and
  // then be written out again above a second copy of itself, growing by
  // one note every time a reader exported and reopened their work.
  const header = [
    `${PY_HEADER_OPENING} — ${new Date().toISOString().slice(0, 10)}`,
    "#",
    "# The \`# %%\` lines below mark where one cell ends and the next",
    "# begins. Python ignores them, so this file runs as an ordinary",
    "# script; editors that understand the convention show it as cells.",
    "# Delete these lines and nothing changes.",
    "",
  ].join("\n");
  triggerDownload(`${getFilenameBase()}.py`, `${header}\n${cellsToPercentText(cells)}`,
                  "text/x-python");
  updateStatus("Downloaded as Python. Outputs are not in a .py file — use .ipynb to keep those.", "ok");
}

/* The Jupyter notebook format (.ipynb) stores a cell's source as a list
 * of strings, one per line, where every line *except the last* keeps its
 * own trailing "\n" — that's simply the convention real Jupyter itself
 * uses when it saves a file. This function reproduces that exact shape:
 * split on newlines, then put the "\n" back on every line except the
 * final one, so a file downloaded from here looks the same, byte for
 * byte in this respect, as one saved by actual Jupyter. */
function splitLines(text) {
  const lines = text.split("\n");
  return lines.map((line, i) => (i < lines.length - 1 ? `${line}\n` : line));
}

/* ------------------------------------------------ outputs in a .ipynb
 *
 * dewmini keeps a cell's output as HTML — the contents of its output area
 * when the cell finished. The Jupyter notebook format keeps a list of
 * typed output objects instead: `stream` for text a cell printed, `error`
 * for an exception, and `display_data` or `execute_result` for a value,
 * carried as alternative representations labelled by MIME type.
 *
 * Neither direction used to be attempted. downloadAsIpynb() wrote
 * `outputs: []` for every code cell and parseIpynbCells() set every
 * imported cell's output to the empty string, so a student who imported
 * a notebook silently lost every result it arrived with. These two
 * functions are the translation that fixes it. */

/* dewmini's own output HTML, turned into nbformat output objects.
 *
 * Translated child by child rather than as one blob, because the output
 * area is already a sequence of separate things: applyOutputEvent() in
 * pyodide-engine.js appends a `<pre>` per run of printed text and
 * ready-made HTML for anything else. A figure therefore survives as a
 * real `image/png`, which is what any other notebook tool expects, while
 * a table stays HTML because that is genuinely what it is.
 *
 * An error becomes a `stderr` stream rather than an nbformat `error`
 * object. An `error` requires an exception name and value as separate
 * fields, and what dewmini has kept is the rendered message. Splitting
 * that back apart would be guessing, and a wrong exception name in a file
 * is worse than an honest stream of the text that was actually shown. */
function cellOutputsForIpynb(cell) {
  if (!cell.output) return [];
  const holder = document.createElement("template");
  holder.innerHTML = cell.output;

  const outputs = [];
  for (const node of holder.content.childNodes) {
    if (node.nodeType === Node.TEXT_NODE) {
      if (node.textContent.trim()) {
        outputs.push({ output_type: "stream", name: "stdout", text: splitLines(node.textContent) });
      }
      continue;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) continue;

    const classes = node.getAttribute("class") || "";
    if (node.tagName === "PRE") {
      outputs.push({
        output_type: "stream",
        name: classes.includes("dl-error") ? "stderr" : "stdout",
        text: splitLines(node.textContent),
      });
      continue;
    }

    const png = lonePngDataUrl(node);
    if (png) {
      outputs.push({
        output_type: "display_data",
        // The base64 payload only, without the "data:image/png;base64,"
        // prefix — nbformat stores the data, and every reader adds its
        // own prefix back when it builds an <img>.
        data: { "image/png": png },
        metadata: {},
      });
      continue;
    }

    outputs.push({
      output_type: "display_data",
      data: {
        "text/html": splitLines(node.outerHTML),
        // A plain-text alternative for any reader that will not show
        // HTML. Cheap, and the difference between a table appearing as
        // its numbers and appearing as nothing at all.
        "text/plain": splitLines(node.textContent),
      },
      metadata: {},
    });
  }
  return outputs;
}

/* The base64 of a PNG data URL when `node` is an image and nothing else
 * — either an <img> itself or a wrapper whose only content is one. Null
 * for anything more complicated, which then travels as HTML. */
function lonePngDataUrl(node) {
  const img = node.tagName === "IMG" ? node : node.querySelector("img");
  if (!img) return null;
  if (node !== img && (node.querySelectorAll("img").length !== 1 || node.textContent.trim())) return null;
  const match = /^data:image\/png;base64,(.+)$/.exec(img.getAttribute("src") || "");
  return match ? match[1] : null;
}

/* Elements an imported notebook's HTML output may keep. Everything else
 * is dropped, contents and all.
 *
 * An imported .ipynb is a file from anywhere — a classmate, a download, a
 * repository — and its outputs are HTML that would otherwise be put
 * straight into the page. An allow-list is the safe shape for this: a
 * list of things to remove is only ever as good as its author's
 * imagination, while a list of things to keep fails closed. */
const IMPORTED_HTML_TAGS = new Set([
  "P", "DIV", "SPAN", "PRE", "CODE", "BR", "HR", "EM", "STRONG", "B", "I", "U", "SMALL", "SUB", "SUP",
  "UL", "OL", "LI", "DL", "DT", "DD", "BLOCKQUOTE",
  "TABLE", "THEAD", "TBODY", "TFOOT", "TR", "TH", "TD", "CAPTION", "COLGROUP", "COL",
  "H1", "H2", "H3", "H4", "H5", "H6", "IMG",
]);

/* Rebuilds `html` keeping only the elements above, `class` as their only
 * attribute, and an <img> only when its source is an embedded image.
 *
 * Rebuilding rather than editing in place: every attribute is dropped by
 * default and the few that survive are copied across deliberately, so an
 * attribute nobody thought of — an event handler, a `style` carrying a
 * URL, an `srcset` — cannot survive by not having been considered.
 *
 * Parsing happens inside a <template>, whose contents are inert: no
 * script runs and no image is fetched while this is deciding what to
 * keep. */
function sanitizeImportedHtml(html) {
  const source = document.createElement("template");
  source.innerHTML = html;
  const out = document.createElement("div");

  const copy = (from, to) => {
    for (const node of from.childNodes) {
      if (node.nodeType === Node.TEXT_NODE) {
        to.appendChild(document.createTextNode(node.textContent));
        continue;
      }
      if (node.nodeType !== Node.ELEMENT_NODE) continue;
      if (!IMPORTED_HTML_TAGS.has(node.tagName)) continue;

      const clean = document.createElement(node.tagName.toLowerCase());
      const className = node.getAttribute("class");
      if (className) clean.setAttribute("class", className);
      if (node.tagName === "IMG") {
        const src = node.getAttribute("src") || "";
        // Only an embedded image. A remote URL would make opening a
        // notebook fetch from wherever its author chose, which is a
        // request the reader never made.
        if (!/^data:image\/(png|jpeg|gif|webp);base64,/.test(src)) continue;
        clean.setAttribute("src", src);
        const alt = node.getAttribute("alt");
        if (alt) clean.setAttribute("alt", alt);
      }
      copy(node, clean);
      to.appendChild(clean);
    }
  };

  copy(source.content, out);
  return out.innerHTML;
}

/* nbformat output objects, turned back into the HTML dewmini shows.
 *
 * `text/html` from a file is put through sanitizeImportedHtml() above.
 * `image/png` becomes an <img> built here rather than trusted as markup.
 * An `error` keeps its exception name and value, and its traceback with
 * the terminal colour codes real Jupyter leaves in it stripped out —
 * those are escape sequences meant for a terminal, and shown in a browser
 * they are line noise around the message a student needs to read. */
function htmlForIpynbOutputs(outputs) {
  if (!Array.isArray(outputs)) return "";
  const text = (value) => (Array.isArray(value) ? value.join("") : String(value ?? ""));
  const escape = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const parts = [];

  for (const output of outputs) {
    if (!output || typeof output !== "object") continue;
    if (output.output_type === "stream") {
      const cssClass = output.name === "stderr" ? "dl-error" : "dl-stdout";
      parts.push(`<pre class="${cssClass}">${escape(text(output.text))}</pre>`);
      continue;
    }
    if (output.output_type === "error") {
      const trace = text(Array.isArray(output.traceback) ? output.traceback.join("\n") : output.traceback);
      // eslint-disable-next-line no-control-regex
      const plain = trace.replace(/\u001b\[[0-9;]*m/g, "");
      const heading = [output.ename, output.evalue].filter(Boolean).join(": ");
      parts.push(`<pre class="dl-error">${escape(plain || heading)}</pre>`);
      continue;
    }
    const data = output.data || {};
    if (typeof data["image/png"] === "string" || Array.isArray(data["image/png"])) {
      const base64 = text(data["image/png"]).replace(/\s+/g, "");
      parts.push(`<img src="data:image/png;base64,${base64}" alt="">`);
      continue;
    }
    if (data["text/html"] !== undefined) {
      const clean = sanitizeImportedHtml(text(data["text/html"]));
      if (clean) parts.push(clean);
      continue;
    }
    if (data["text/plain"] !== undefined) {
      parts.push(`<pre class="dl-stdout">${escape(text(data["text/plain"]))}</pre>`);
    }
  }
  return parts.join("");
}

/* Builds a real Jupyter notebook (nbformat 4) file: a Python cell becomes
 * a "code" cell, a text cell becomes a "markdown" cell, in the exact JSON
 * shape Jupyter, JupyterLab, and Colab all expect — so the file this
 * produces opens correctly in any of them, and the same file loads back
 * into dewmini via handleImportFile() below. */
/* A list of cells as a Jupyter notebook object, ready to be serialised.
 * Shared by the download and by saving a .ipynb back to the workspace, so
 * the two can never write files that differ. */
function cellsToIpynb(cellList) {
  return {
    nbformat: 4,
    nbformat_minor: 5,
    metadata: {
      kernelspec: { display_name: "Python 3", language: "python", name: "python3" },
      language_info: { name: "python", pygments_lexer: "ipython3" },
    },
    cells: cellList.map((cell) => ({
      cell_type: cell.type === CELL_TYPES.PYTHON ? "code" : "markdown",
      // nbformat requires a tool to preserve metadata keys it does not
      // recognise rather than discard them, so a cell's metadata is where
      // dewmini's own information belongs. The file stays a valid Jupyter
      // notebook that Jupyter, JupyterLab, Colab and VS Code all open
      // normally — which is why dewlab needs no notebook format of its
      // own. Only what is read back on import is written: a name nothing
      // reads would be a claim in the file that nothing keeps true.
      metadata: typeof cell.lastRunMs === "number" ? { dewmini: { lastRunMs: cell.lastRunMs } } : {},
      source: splitLines(cell.content),
      ...(cell.type === CELL_TYPES.PYTHON
        // No execution_count: dewmini does not number runs, and writing a
        // number it did not measure would be a claim about the order this
        // notebook was run in that nothing here can support.
        ? { execution_count: null, outputs: cellOutputsForIpynb(cell) }
        : {}),
    })),
  };
}

function downloadAsIpynb() {
  flushFileEditor();
  if (!cells.length) { updateStatus("No cells to export.", "error"); return; }
  triggerDownload(`${getFilenameBase()}.ipynb`,
                  JSON.stringify(cellsToIpynb(cells), null, 2), "application/json");
  updateStatus("Downloaded as Jupyter Notebook.", "ok");
}

/* A small, self-contained stylesheet for the standalone HTML export
 * below — deliberately not reusing dewlab's own site CSS, since the
 * whole point of this export is one file that works completely on its
 * own, with nothing else to fetch. `dark` picks one of two small colour
 * palettes at build time, baking the reader's current theme choice into
 * the exported file rather than making the export theme-aware itself. */
function standaloneCss(dark) {
  const bg = dark ? "#14181f" : "#fdfcfa";
  const fg = dark ? "#e6e3dd" : "#1a1a1a";
  const muted = dark ? "#98a2b3" : "#5f6b7a";
  const rule = dark ? "#2a3140" : "#e2ddd5";
  const cellBg = dark ? "#1b2129" : "#f6f4f0";
  const outputBg = dark ? "#171c24" : "#fbfaf8";
  const navy = dark ? "#b9c8e6" : "#1b2a4a";
  const orange = "#d4692a";
  return `
    body { margin: 0; padding: 2rem 1.25rem 4rem; max-width: 40rem; margin-inline: auto;
      font-family: Georgia, "Times New Roman", serif; background: ${bg}; color: ${fg}; line-height: 1.6; }
    h1 { color: ${navy}; font-size: 1.5rem; }
    .status { font-family: ui-monospace, monospace; font-size: 0.85rem; color: ${muted}; margin-bottom: 1.5rem; }
    .cell { border-top: 1px solid ${rule}; padding: 1rem 0; }
    .cell:last-child { border-bottom: 1px solid ${rule}; }
    .cell-head { font-family: ui-monospace, monospace; font-size: 0.7rem; text-transform: uppercase;
      letter-spacing: 0.04em; color: ${muted}; margin-bottom: 0.5rem; }
    .code { background: ${cellBg}; border-radius: 4px; padding: 0.75rem 1rem; overflow-x: auto;
      font-family: ui-monospace, monospace; font-size: 0.85rem; white-space: pre-wrap; }
    .text-body { white-space: pre-wrap; }
    .output { margin-top: 0.6rem; padding: 0.65rem 0.8rem; border-radius: 4px; background: ${outputBg};
      font-family: ui-monospace, monospace; font-size: 0.85rem; overflow-x: auto; }
    .output:empty { display: none; }
    .output img { max-width: 100%; border-radius: 3px; }
    a { color: ${orange}; }
  `;
}

/* Builds and downloads a single .html file that can run this notebook
 * completely on its own, without dewmini itself — see buildStandaloneHtml
 * below for how that file actually works. */
async function downloadAsHtml() {
  flushFileEditor();
  if (!cells.length) { updateStatus("No cells to export.", "error"); return; }
  updateStatus("Building the standalone file…");
  try {
    const toolsSource = await getToolsSource();
    const cellsData = cells.map((c) => ({ id: c.id, type: c.type, content: c.content }));
    const name = getFilenameBase();
    const html = buildStandaloneHtml(toolsSource, cellsData, isDarkNow(), name);
    triggerDownload(`${name}.html`, html, "text/html");
    updateStatus("Downloaded as standalone HTML.", "ok");
  } catch (err) {
    updateStatus(`Couldn't build the HTML export: ${err.message}`, "error");
  }
}

/* Returns one complete HTML page, as a single big string, that can open
 * by itself (double-click, no server needed) and run this notebook's
 * cells the moment it opens. The trick that makes this possible: rather
 * than the downloaded page fetching tutorial_tools.py or the cell data
 * from anywhere, both are serialized with `JSON.stringify(...)` and
 * embedded directly into the page's own `<script>` tag as JavaScript
 * constants (`TOOLS_SRC`, `CELLS`). That's also why this needed
 * `toolsSource` fetched ahead of time by the caller (downloadAsHtml,
 * above) rather than fetched from inside this function — the exported
 * page has no access back to dewlab's own files once it's been saved
 * somewhere else on the reader's computer. Read this as a small, separate
 * standalone program: everything inside the outer template literal's own
 * `<script>...</script>` runs *in the downloaded file*, in the reader's
 * browser, at some point in the future — not here, not now. It boots its
 * own copy of Pyodide (the reason it needs an internet connection the
 * first time it opens, even though it needs none after that) and runs
 * every cell once, top to bottom, then stays exactly as it rendered —
 * this is a read-only snapshot, not an editable copy of dewmini. */
function buildStandaloneHtml(toolsSource, cellsData, dark, title) {
  const safeTitle = escapeHtml(title || "dewmini notebook");
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${safeTitle}</title>
<script src="https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js"><\/script>
<style>${standaloneCss(dark)}</style>
</head>
<body>
<h1>${safeTitle}</h1>
<p class="status" id="status">Loading Python… this file needs an internet connection the first time it opens.</p>
<div id="cells"></div>
<script>
const CELLS = ${JSON.stringify(cellsData)};
const TOOLS_SRC = ${JSON.stringify(toolsSource)};
const SEED = ${JSON.stringify(SEED_GLOBALS_CODE)};
const PACKAGES = ${JSON.stringify(DM_PACKAGES)};
const NETWORK_PATCH = ${JSON.stringify(DM_NETWORK_PATCH)};

async function main() {
  const statusEl = document.getElementById("status");
  const container = document.getElementById("cells");
  const runnable = [];

  for (const cell of CELLS) {
    const wrap = document.createElement("div");
    wrap.className = "cell cell-" + cell.type;
    const head = document.createElement("div");
    head.className = "cell-head";
    head.textContent = cell.type === "python" ? "Python" : "Text";
    wrap.appendChild(head);

    if (cell.type === "python") {
      const pre = document.createElement("pre");
      pre.className = "code";
      pre.textContent = cell.content;
      wrap.appendChild(pre);
      const out = document.createElement("div");
      out.className = "output";
      wrap.appendChild(out);
      runnable.push({ cell, out });
    } else {
      const body = document.createElement("div");
      body.className = "text-body";
      body.textContent = cell.content;
      wrap.appendChild(body);
    }
    container.appendChild(wrap);
  }

  try {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage(PACKAGES);
    // Browser-backed urllib, so a cell that read a URL in dewmini still
    // reads it here. Forgiving, like every other boot: a Pyodide without
    // the package must still start.
    try {
      await pyodide.loadPackage(["pyodide-http"]);
      await pyodide.runPythonAsync(NETWORK_PATCH);
    } catch (e) {}
    pyodide.FS.writeFile("/home/pyodide/tutorial_tools.py", TOOLS_SRC, { encoding: "utf8" });
    const tools = pyodide.pyimport("tutorial_tools");
    tools.configure("");
    await pyodide.runPythonAsync(SEED);

    statusEl.textContent = "Running…";
    for (const { cell, out } of runnable) {
      await tools.run_cell(cell.id, out, cell.content);
    }
    statusEl.textContent = "Ready — this is a read-only copy; edit the source cell in dewmini to change it.";
  } catch (err) {
    statusEl.textContent = "Python failed to load: " + err.message;
  }
}

main();
<\/script>
</body>
</html>`;
}

// --------------------------------------------------------------- reference

/* The five kinds a glossary entry can have, in the order the panel shows
 * them — the same order and labels tutorial pages use, so a reader who has
 * met the Reference there finds the same shape here. */
const REFERENCE_KINDS = [
  ["concept", "Concepts"],
  ["function", "Functions"],
  ["operator", "Operators"],
  ["formula", "Formulas"],
  ["keyword", "Keywords"],
];

/* Short labels for the topic groups, in the order
 * planning/curriculum/topic-groups.yaml lists them. This is a label
 * *override*, not the list of groups: the file's own names are written for a
 * page heading ("Trigonometry — triangles, circles, and waves") and are far
 * too long for a chip, so the curated short forms live here.
 *
 * The groups themselves are read off the data (referenceTopics() below), so
 * adding one to topic-groups.yaml gives it a chip on the next build whether
 * or not anyone remembers to come back here. That matters: everything else
 * about these filters re-derives itself when the curriculum data changes,
 * and a hand-kept list that silently drops new groups would be the one place
 * the two could quietly disagree. */
const REFERENCE_TOPIC_LABELS = [
  ["numbers-and-algebra", "Numbers & algebra"],
  ["polynomials-and-graphs", "Polynomials"],
  ["trigonometry", "Trigonometry"],
  ["rates-of-change", "Rates of change"],
  ["counting-and-chance", "Counting & chance"],
  ["logic-and-sets", "Logic & sets"],
  ["data-and-pictures", "Data"],
  ["matrices", "Matrices"],
  ["programming-foundations", "Programming"],
  ["chance-and-simulation", "Simulation"],
  ["big-picture", "Big picture"],
];

/* Every topic group the reference actually has terms for, curated ones first
 * in their own order and anything new after them, alphabetically. A group
 * with no short label gets its key turned back into words — plain, and
 * visibly a fallback, which is the right prompt to come and name it. */
function referenceTopics() {
  const labels = new Map(REFERENCE_TOPIC_LABELS);
  const present = new Set();
  for (const entry of referenceEntries || []) {
    for (const key of entry.groups || []) present.add(key);
  }
  const curated = REFERENCE_TOPIC_LABELS.filter(([key]) => present.has(key));
  const rest = [...present]
    .filter((key) => !labels.has(key))
    .sort()
    .map((key) => [key, key.replace(/-/g, " ").replace(/^./, (c) => c.toUpperCase())]);
  return [...curated, ...rest];
}

const REFERENCE_SUBJECTS = [["maths", "Maths"], ["computing", "Computing"]];
const REFERENCE_LEVELS = [
  ["beginner", "Beginner"],
  ["intermediate", "Intermediate"],
  ["advanced", "Advanced"],
];

let referenceEntries = null;

/* Every filter row is the same shape: a set of chosen values, empty meaning
 * "no filter on this facet". Four independent sets rather than four
 * variables so the render and the reset can loop over them. */
const referenceFilters = {
  subjects: new Set(),
  level: new Set(),
  groups: new Set(),
  kind: new Set(),
};

/* Fetches the cross-tutorial reference once (build.py's
 * write_reference_index()). Absent is not an error: a build with no
 * tutorials writes no index, and an offline bundle from such a build
 * should still open — the section says so and gets out of the way. */
async function loadReference() {
  const statusEl = document.getElementById("dm-reference-status");
  try {
    const response = await fetch("../assets/reference-index.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    referenceEntries = await response.json();
  } catch (err) {
    if (statusEl) statusEl.textContent = `The reference isn't available here (${err.message}).`;
    return;
  }
  renderReferenceFilters();
  renderReference();
}

/* Does one entry pass every filter row? A row with nothing chosen doesn't
 * filter; a row with choices passes an entry matching any of them (so
 * Maths + Computing means "either", not "both"). An entry missing the facet
 * entirely — a term from a tutorial claiming no outcomes — is filtered out
 * once that row is in use, which is why "Unfiled" is offered as a value of
 * its own rather than leaving those terms unreachable. */
function referenceEntryMatches(entry) {
  const rowPasses = (chosen, value) => {
    if (!chosen.size) return true;
    const values = Array.isArray(value) ? value : (value ? [value] : []);
    if (!values.length) return chosen.has("unfiled");
    return values.some((v) => chosen.has(v));
  };
  return rowPasses(referenceFilters.subjects, entry.subjects)
    && rowPasses(referenceFilters.level, entry.level)
    && rowPasses(referenceFilters.groups, entry.groups)
    && rowPasses(referenceFilters.kind, entry.kind);
}

/* One chip. Toggling is additive within its row — picking Maths then
 * Computing widens rather than replaces, which is what a reader expects of
 * something that looks like a set of switches. */
function referenceChip(row, value, label, count) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "dm-filter-chip";
  btn.textContent = count === undefined ? label : `${label} ${count}`;
  btn.setAttribute("aria-pressed", String(referenceFilters[row].has(value)));
  btn.addEventListener("click", () => {
    const chosen = referenceFilters[row];
    if (chosen.has(value)) chosen.delete(value); else chosen.add(value);
    renderReferenceFilters();
    renderReference();
  });
  return btn;
}

/* Draws all four filter rows, each chip carrying how many terms it would
 * leave — counted against the *other* rows' current choices, so the numbers
 * describe what would actually happen rather than a total that stops being
 * true the moment anything else is on. */
function renderReferenceFilters() {
  if (!referenceEntries) return;

  const countFor = (row, value) => {
    const saved = referenceFilters[row];
    referenceFilters[row] = new Set([value]);
    const n = referenceEntries.filter(referenceEntryMatches).length;
    referenceFilters[row] = saved;
    return n;
  };

  const fill = (id, row, values) => {
    const wrap = document.getElementById(id);
    if (!wrap) return;
    wrap.replaceChildren();
    for (const [value, label] of values) {
      const n = countFor(row, value);
      if (!n) continue; // a chip that would show nothing is noise
      wrap.appendChild(referenceChip(row, value, label, n));
    }
  };

  fill("dm-reference-subjects", "subjects",
       [...REFERENCE_SUBJECTS, ["unfiled", "Unfiled"]]);
  fill("dm-reference-levels", "level",
       [...REFERENCE_LEVELS, ["unfiled", "Unfiled"]]);
  fill("dm-reference-topics", "groups", referenceTopics());
  fill("dm-reference-kinds", "kind", REFERENCE_KINDS);

  // The collapsed summary has to say what is on inside it, or a reader who
  // scrolled past a narrowed list has no way to tell why.
  const summary = document.getElementById("dm-reference-topics-summary");
  const chosen = referenceFilters.groups.size;
  if (summary) summary.textContent = chosen ? `Topics · ${chosen} on` : "Topics";
  const wrap = document.getElementById("dm-reference-topics-wrap");
  if (wrap) wrap.classList.toggle("dm-filter-more-active", chosen > 0);
}

/* Draws the reference, filtered by the search box and all four chip rows.
 * Built with createElement rather than an HTML string throughout, for the
 * same reason tutorial-runtime.js's own renderReference() is: a term can
 * legitimately contain `<` (dewlab teaches operators), and textContent
 * cannot turn it into markup where innerHTML would. */
function renderReference() {
  const groupsEl = document.getElementById("dm-reference-groups");
  const statusEl = document.getElementById("dm-reference-status");
  if (!groupsEl || !referenceEntries) return;
  groupsEl.replaceChildren();

  const needle = (document.getElementById("dm-reference-search")?.value || "").trim().toLowerCase();
  const matches = referenceEntries.filter((entry) => {
    if (!referenceEntryMatches(entry)) return false;
    if (!needle) return true;
    return `${entry.term} ${entry.definition}`.toLowerCase().includes(needle);
  });

  if (statusEl) {
    statusEl.textContent = matches.length
      ? `${matches.length} of ${referenceEntries.length} terms, from every tutorial.`
      : "Nothing matches that.";
  }
  if (!matches.length) return;

  for (const [kind, label] of REFERENCE_KINDS) {
    const inKind = matches.filter((entry) => entry.kind === kind);
    if (!inKind.length) continue;

    const group = document.createElement("div");
    group.className = "dm-reference-group";
    const heading = document.createElement("h4");
    heading.textContent = label;
    group.appendChild(heading);

    const list = document.createElement("dl");
    for (const entry of inKind) {
      const term = document.createElement("dt");
      term.textContent = entry.term;
      const definition = document.createElement("dd");
      definition.textContent = entry.definition;
      if (entry.example) {
        const example = document.createElement("code");
        example.textContent = entry.example;
        definition.appendChild(example);
      }
      if (entry.origin) {
        const origin = document.createElement("p");
        origin.className = "dm-term-origin";
        origin.textContent = `Introduced in ${entry.origin}`;
        definition.appendChild(origin);
      }
      list.append(term, definition);
    }
    group.appendChild(list);
    groupsEl.appendChild(group);
  }
}

function initReferenceSection() {
  document.getElementById("dm-reference-search")?.addEventListener("input", renderReference);
  loadReference();
}

// -------------------------------------------------------------------- data

/* Fetches the dataset catalogue and draws it. Same "fetch a JSON sibling
 * once" shape as the practice bank, and it rides the same wholesale
 * compose/ copy into the offline bundle, so the catalogue works offline
 * even where the datasets it describes do not. */
async function loadDataCatalogue() {
  const listEl = document.getElementById("dm-data-list");
  const statusEl = document.getElementById("dm-data-status");
  if (!listEl) return;

  let catalogue;
  try {
    const response = await fetch("data-catalogue.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    catalogue = await response.json();
  } catch (err) {
    if (statusEl) statusEl.textContent = `The catalogue isn't available here (${err.message}).`;
    return;
  }

  if (statusEl) statusEl.hidden = true;
  listEl.replaceChildren();
  for (const dataset of catalogue) {
    listEl.appendChild(renderDataset(dataset));
  }
}

/* One dataset's card: what it is, where it came from, what licence it
 * carries, and a button that writes the code to load it.
 *
 * The attribution is on the card rather than buried in a repository file
 * because a student who uses someone's data should see whose it is at the
 * moment they use it — the same reasoning behind the dataset YAML the
 * tutorial pages' own Reference already shows. */
function renderDataset(dataset) {
  const card = document.createElement("div");
  card.className = "dm-dataset";

  const title = document.createElement("h4");
  title.textContent = dataset.title;
  if (dataset.remote) {
    const badge = document.createElement("span");
    badge.className = "dm-dataset-remote";
    badge.textContent = "from the web";
    badge.title = "Loaded from another website, so it needs a connection — and that site has to allow it";
    title.appendChild(badge);
  }
  card.appendChild(title);

  const description = document.createElement("p");
  description.textContent = dataset.description;
  card.appendChild(description);

  const meta = document.createElement("p");
  meta.className = "dm-dataset-meta";
  meta.textContent = `${dataset.source} — ${dataset.license}`;
  card.appendChild(meta);

  const use = document.createElement("button");
  use.type = "button";
  use.className = "dm-tool";
  use.textContent = "Add a cell that loads it";
  use.addEventListener("click", () => {
    addCell(CELL_TYPES.PYTHON, dataset.code);
    updateStatus(`Added a cell loading ${dataset.title}.`, "ok");
  });
  card.appendChild(use);

  return card;
}

// --------------------------------------------------------------- variables

/* Draws what is currently defined in the Python session. The engine
 * returns plain `{name, type, summary, kind}` objects
 * (tutorial_tools.describe_globals()), so nothing here has to know
 * anything about Python — this is presentation only.
 *
 * A student's own data goes first and unfolded; the functions and modules
 * that share the namespace fold away under a summary, because they are
 * almost always the same names every session (what the page seeded, what a
 * cell imported) and would otherwise bury the two variables the reader
 * actually wants to look at. */
async function refreshVariables() {
  const listEl = document.getElementById("dm-variables");
  const statusEl = document.getElementById("dm-variables-status");
  const sharedEl = document.getElementById("dm-variables-shared");
  if (!listEl) return;

  // Nothing to draw for a closed panel, and this is called after every
  // cell run — describing the namespace is a full round trip to the
  // worker, so "Run all" over fifty cells would otherwise pay fifty of
  // them to update something nobody is looking at. Opening the Workbench
  // refreshes it (initPanels()), so it is never stale when visible.
  const panel = document.getElementById("dm-workbench");
  if (panel && panel.hidden) return;

  if (engine.engineMode() === null) {
    listEl.replaceChildren();
    if (statusEl) statusEl.textContent = "Not started yet — run a cell to start Python.";
    if (sharedEl) sharedEl.hidden = true;
    return;
  }

  let described;
  try {
    described = await engine.describeGlobals();
  } catch (err) {
    listEl.replaceChildren();
    if (statusEl) statusEl.textContent = `Couldn't read the session: ${err.message}`;
    return;
  }

  const data = described.filter((entry) => entry.kind === "data");
  const other = described.filter((entry) => entry.kind !== "data");

  listEl.replaceChildren();
  if (statusEl) {
    statusEl.textContent = data.length
      ? `${data.length} variable${data.length === 1 ? "" : "s"} in your session.`
      : "Nothing defined yet — run a cell that makes a variable.";
  }
  if (sharedEl) sharedEl.hidden = notebooks.length < 2;

  for (const entry of data) listEl.appendChild(renderVariable(entry));

  if (other.length) {
    const details = document.createElement("details");
    details.className = "dm-variables-other";
    const summary = document.createElement("summary");
    summary.textContent = `${other.length} function${other.length === 1 ? "" : "s"} and module${other.length === 1 ? "" : "s"}`;
    details.appendChild(summary);
    for (const entry of other) details.appendChild(renderVariable(entry));
    listEl.appendChild(details);
  }
}

function renderVariable(entry) {
  const row = document.createElement("div");
  row.className = "dm-variable";

  const name = document.createElement("span");
  name.className = "dm-variable-name";
  name.textContent = entry.name;

  const type = document.createElement("span");
  type.className = "dm-variable-type";
  type.textContent = entry.type;

  const summary = document.createElement("span");
  summary.className = "dm-variable-summary";
  summary.textContent = entry.summary;

  row.append(name, type, summary);
  return row;
}

function initVariablesSection() {
  document.getElementById("dm-variables-refresh")?.addEventListener("click", () => refreshVariables());
}

// ---------------------------------------------------------------- practice

const PRACTICE_INDEX_KEY = "dewmini:practice-index";
const PRACTICE_ORDER_KEY = "dewmini:practice-order";
const PRACTICE_SHUFFLE_KEY = "dewmini:practice-shuffle";
let practiceBank = null;

/* Fetches dewlab's shared practice-problem bank once and caches it in
 * `practiceBank`, the same "fetch once, reuse" shape as getToolsSource()
 * above. */
async function loadPracticeBank() {
  if (practiceBank) return practiceBank;
  const res = await fetch("practice-bank.json");
  if (!res.ok) throw new Error(`practice-bank.json: HTTP ${res.status}`);
  practiceBank = await res.json();
  return practiceBank;
}

/* Which order Settings has this reader on: "sequential" (work through the
 * bank one problem at a time) or "random." */
function loadPracticeOrder() {
  try { return localStorage.getItem(PRACTICE_ORDER_KEY) === "random" ? "random" : "sequential"; } catch { return "sequential"; }
}

/* Builds an array [0, 1, 2, ..., n-1] and shuffles it into a random order
 * using the Fisher–Yates shuffle: walk backward from the end, and at each
 * position swap in a uniformly random earlier-or-equal element. This is
 * the standard way to shuffle an array with every possible ordering
 * equally likely — a naive "sort by Math.random()" approach, which might
 * seem simpler, doesn't actually produce a fair shuffle. */
function shuffledRange(n) {
  const arr = Array.from({ length: n }, (_, i) => i);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/* A shuffle bag rather than plain Math.random() each time — "random" should
 * still mean every problem turns up once before any repeats, not the
 * frustrating experience of the same one twice in a row. Reshuffles once
 * the bag empties, nudging away an immediate repeat of the last problem
 * served across the reshuffle boundary. */
function nextRandomPracticeIndex(total, lastIdx) {
  let bag = [];
  try { bag = JSON.parse(localStorage.getItem(PRACTICE_SHUFFLE_KEY) || "[]"); } catch {}
  if (!Array.isArray(bag) || !bag.length || bag.some((n) => !Number.isInteger(n) || n < 0 || n >= total)) {
    bag = shuffledRange(total);
  }
  if (bag.length > 1 && bag[bag.length - 1] === lastIdx) {
    [bag[bag.length - 1], bag[bag.length - 2]] = [bag[bag.length - 2], bag[bag.length - 1]];
  }
  const idx = bag.pop();
  try { localStorage.setItem(PRACTICE_SHUFFLE_KEY, JSON.stringify(bag)); } catch {}
  return idx;
}

/* Picks the next practice problem's index, in whichever order Settings
 * has chosen. The sequential branch's `((x % total) + total) % total` is
 * a common trick for "modulo that's always non-negative": JavaScript's
 * `%` operator can return a negative result for a negative input (unlike
 * the mathematical definition of modulo), so this adds `total` back and
 * takes `% total` a second time to guarantee a valid, non-negative index
 * even if `lastIdx` were somehow negative. */
function nextPracticeIndex(total) {
  let lastIdx = -1;
  try { lastIdx = parseInt(localStorage.getItem(PRACTICE_INDEX_KEY) || "-1", 10); } catch {}
  // A stored value that isn't a number parses to NaN, which would poison
  // every arithmetic step below — treat it as "never started" instead.
  if (!Number.isInteger(lastIdx)) lastIdx = -1;
  if (loadPracticeOrder() === "random") return nextRandomPracticeIndex(total, lastIdx);
  const idx = ((Math.max(lastIdx, -1) + 1) % total + total) % total;
  return idx;
}

/* Adds one problem from dewlab's own practice bank — the doc cell states
 * which one, and the code cell is exactly the function stub from the
 * source bank (docstring, Args/Returns/Example and all), so there is
 * nothing to duplicate or drift out of sync with. Order (sequential or
 * random, Settings → Practice) decides which comes next; either way it
 * remembers where a reader left off. */
async function addPracticeProblem() {
  try {
    const bank = await loadPracticeBank();
    if (!bank.length) { updateStatus("The practice bank is empty.", "error"); return; }

    const idx = nextPracticeIndex(bank.length);
    const problem = bank[idx];

    const docCell = {
      id: generateId(),
      type: CELL_TYPES.TEXT,
      content: `## Practice — Problem ${problem.number}\n*${problem.section}*\n\n${problem.title}`,
      output: "",
      error: false,
    };
    const codeCell = { id: generateId(), type: CELL_TYPES.PYTHON, content: problem.stub, output: "", error: false };

    cells.push(docCell, codeCell);
    saveState();
    renderCells();
    focusCell(codeCell.id);

    try { localStorage.setItem(PRACTICE_INDEX_KEY, String(idx)); } catch {}
    updateStatus(`Problem ${problem.number} of ${bank.length} added.`, "ok");
  } catch (err) {
    updateStatus(`Couldn't load the practice bank: ${err.message}`, "error");
  }
}

/* Modules with no Pyodide build at all, or that need something a browser
 * tab fundamentally cannot offer (a display to draw a GUI window in, a
 * separate OS process, a raw network socket, a real terminal) — not
 * every package Pyodide happens to lack, just the common, structurally
 * impossible ones worth telling a reader about before they go looking
 * for a bug in their own logic that was never there. */
const PYODIDE_INCOMPATIBLE_MODULES = {
  tkinter: "opens a GUI window — there is no display here to draw one on",
  turtle: "opens a GUI window — there is no display here to draw one on",
  pygame: "needs a real display and audio device Pyodide cannot offer",
  PyQt5: "opens a GUI window — there is no display here to draw one on",
  PyQt6: "opens a GUI window — there is no display here to draw one on",
  PySide2: "opens a GUI window — there is no display here to draw one on",
  PySide6: "opens a GUI window — there is no display here to draw one on",
  wx: "opens a GUI window — there is no display here to draw one on",
  kivy: "opens a GUI window — there is no display here to draw one on",
  cv2: "OpenCV has no Pyodide build",
  torch: "not available in Pyodide — too large, and needs native GPU code",
  tensorflow: "not available in Pyodide — too large, and needs native GPU code",
  keras: "not available in Pyodide — too large, and needs native GPU code",
  multiprocessing: "Pyodide runs on a single thread — there is no separate process to start",
  subprocess: "there is no operating system underneath to run a command in",
  socket: "the browser has no raw network socket access",
  // The network libraries a copied notebook arrives with. These are not
  // impossible the way the entries above are — Pyodide ships them, and
  // `pyodide_http.patch_all()` routes them through the browser's own
  // fetching — but they are not loaded by default, so an unprepared import
  // fails and the reason is worth saying before the cell runs.
  requests: "needs loading first (`await micropip.install(\"requests\")`) and `pyodide_http.patch_all()` to use the browser's connection — or use `await load_csv(url)`, which needs neither",
  httpx: "needs loading first with micropip, and `pyodide_http.patch_all()` to use the browser's connection — or use `await load_csv(url)`, which needs neither",
  aiohttp: "needs loading first with micropip, and cannot open its own connections here — `pyodide.http.pyfetch` is the browser-native equivalent",
  urllib3: "needs loading first with micropip, and `pyodide_http.patch_all()` to use the browser's connection",
  ctypes: "there are no native shared libraries here to load",
  serial: "the browser has no serial port access",
  pyaudio: "the browser has no direct audio device access",
  sounddevice: "the browser has no direct audio device access",
  selenium: "there is no separate browser process for it to drive",
  pty: "this needs a real terminal, which the browser has none of",
  curses: "this needs a real terminal, which the browser has none of",
  termios: "this needs a real terminal, which the browser has none of",
};

/* Best-effort scan of imported Python cells for things that will not
 * work once they actually run here — Jupyter magics, shell escapes, and
 * imports of the structurally impossible modules above — so the warning
 * reaches a reader before they go hunting for a bug in code they didn't
 * write. Line-based and deliberately shallow: a regex pass over each
 * line, not a Python parser, which is enough for the fixed set of
 * shapes it looks for. */
function scanPyodideCompatibility(importedCells) {
  const magicCells = [];
  const shellCells = [];
  const moduleCells = new Map();

  importedCells.forEach((cell, index) => {
    if (cell.type !== CELL_TYPES.PYTHON) return;
    const cellNumber = index + 1;
    for (const rawLine of cell.content.split("\n")) {
      const line = rawLine.trim();
      if (/^%{1,2}\S/.test(line)) magicCells.push(cellNumber);
      else if (/^!\S/.test(line)) shellCells.push(cellNumber);

      const importMatch = line.match(/^(?:import|from)\s+([A-Za-z_][\w.]*)/);
      if (importMatch) {
        const topLevelModule = importMatch[1].split(".")[0];
        if (Object.prototype.hasOwnProperty.call(PYODIDE_INCOMPATIBLE_MODULES, topLevelModule)) {
          if (!moduleCells.has(topLevelModule)) moduleCells.set(topLevelModule, new Set());
          moduleCells.get(topLevelModule).add(cellNumber);
        }
      }
    }
  });

  const describeCells = (numbers) => `cell${numbers.length === 1 ? "" : "s"} ${numbers.join(", ")}`;
  const warnings = [];
  for (const [moduleName, cellNumbers] of moduleCells) {
    warnings.push(`\`${moduleName}\` (${describeCells([...cellNumbers].sort((a, b) => a - b))}) ${PYODIDE_INCOMPATIBLE_MODULES[moduleName]}.`);
  }
  if (magicCells.length) {
    warnings.push(`Jupyter "magic" commands like \`%matplotlib\` or \`%%time\` (${describeCells(magicCells)}) aren't valid Python here and will raise an error if run as-is.`);
  }
  if (shellCells.length) {
    warnings.push(`Lines starting with \`!\` (${describeCells(shellCells)}) run a shell command in Jupyter — there's no shell here, and dewmini's packages are already loaded, so these aren't needed anyway.`);
  }
  return warnings;
}

/* Populates and shows (or hides, if there's nothing to say)
 * #import-compat-notice — checked before the scanned cells ever land in
 * the notebook so the warning, if any, is the first thing a reader
 * sees about this import. Every warning string is built entirely from
 * this file's own hardcoded strings and plain integers (never from the
 * imported file's actual text), so turning `backticks` into <code> and
 * dropping straight into innerHTML is safe. */
function showImportCompatNotice(warnings) {
  const notice = document.getElementById("import-compat-notice");
  const list = document.getElementById("import-compat-list");
  if (!notice || !list) return;
  if (!warnings.length) { notice.hidden = true; return; }
  const toHtml = (w) => `<li>${w.replace(/`([^`]+)`/g, "<code>$1</code>")}</li>`;
  list.innerHTML = warnings.map(toHtml).join("");
  notice.hidden = false;
}

/* Reads a chosen .ipynb or .py file and replaces the whole notebook with
 * its cells — a Jupyter "code" cell becomes a Python cell, anything else
 * (Jupyter's "markdown" cells) becomes a text cell. `Array.isArray(c.source)
 * ? c.source.join("") : c.source || ""` handles the fact that nbformat
 * allows a cell's source to be stored either as one string or as an
 * array of line-strings (see splitLines() above for why Jupyter itself
 * writes the array form) — this accepts either, so a file from any
 * real Jupyter tool imports correctly either way. Dispatches on the
 * file's own extension rather than sniffing content. */
async function handleImportFile(e) {
  const input = e.target;
  const file = input.files && input.files[0];
  input.value = "";
  if (!file) return;
  try {
    const text = await file.text();
    const imported = file.name.toLowerCase().endsWith(".py") ? parsePyCells(text) : parseIpynbCells(text);
    applyImportedCells(imported, file.name);
  } catch (err) {
    updateStatus(`Couldn't read that file: ${err.message}`, "error");
  }
}

/* Shared tail end of every import path (a picked file, or a built-in
 * example fetched by URL).
 *
 * Opens what was imported in a *new tab* rather than replacing the notebook
 * in front of you. Before tabs, this overwrote everything with no
 * confirmation and no undo — and since every change saves immediately, one
 * mis-picked file destroyed a session's work with nothing to recover from.
 * A new tab is a better answer than the confirmation dialog that was the
 * alternative: nothing is lost, so there is nothing to confirm, and the two
 * notebooks sit side by side if a reader wanted to compare them anyway. */
function applyImportedCells(imported, sourceLabel) {
  if (!imported.length) { updateStatus("That notebook has no cells.", "error"); return; }
  showImportCompatNotice(scanPyodideCompatibility(imported));
  openNotebook(makeNotebook(notebookNameFor(sourceLabel), imported));
  updateStatus(`Loaded ${imported.length} cell${imported.length === 1 ? "" : "s"} from ${sourceLabel} into a new tab.`, "ok");
}

/* A tab name from whatever the import was called — the file's own name
 * without its extension, trimmed to something a tab can actually show. */
function notebookNameFor(sourceLabel) {
  const base = String(sourceLabel || "Imported").replace(/\.(ipynb|py|html?|json)$/i, "").trim();
  if (!base) return "Imported";
  return base.length > 24 ? `${base.slice(0, 23)}…` : base;
}

/* Parses a .ipynb notebook's JSON into dewmini's cell shape — the same
 * mapping handleImportFile() applies to a picked file, factored out so
 * loadBuiltInExample() below can reuse it without duplicating it. */
function parseIpynbCells(text) {
  const notebook = JSON.parse(text);
  if (!Array.isArray(notebook.cells)) throw new Error("that file has no cells array");
  return notebook.cells.map((c) => {
    const output = c.cell_type === "code" ? htmlForIpynbOutputs(c.outputs) : "";
    const dewmini = (c.metadata && c.metadata.dewmini) || {};
    return {
      id: generateId(),
      type: c.cell_type === "code" ? CELL_TYPES.PYTHON : CELL_TYPES.TEXT,
      content: Array.isArray(c.source) ? c.source.join("") : c.source || "",
      output,
      // An imported cell has not been run here, so it has no code that
      // its output belongs to yet — `ranContent` stays unset and the
      // stale badge stays quiet until this cell is actually run.
      error: Array.isArray(c.outputs)
        && c.outputs.some((o) => o && (o.output_type === "error" || o.name === "stderr")),
      ...(typeof dewmini.lastRunMs === "number" ? { lastRunMs: dewmini.lastRunMs } : {}),
    };
  });
}

/* Parses a .py file in the percent format into dewmini's cell shape —
 * the counterpart to downloadAsPython() above.
 *
 * `# %%` starts a code cell and `# %% [markdown]` starts a text cell,
 * whose prose follows as ordinary `#` comment lines. A marker may carry
 * a title and options after it, which is what Jupytext and Visual Studio
 * Code write (`# %% A title [markdown] tags=["x"]`), so the kind is
 * decided by looking for a bracketed word rather than by matching the
 * whole line. `[raw]` is read as a text cell: its content is not Python,
 * and a text cell is the closer of the two things dewmini has.
 *
 * Code before the first marker is kept as a leading Python cell. In a
 * file written anywhere else that is real code — a shebang line, a block
 * of imports — and discarding it would lose part of the program.
 *
 * A file with no markers at all — a plain script — imports as a single
 * Python cell.
 *
 * @param {string} text - raw .py file contents
 * @returns {Array<Object>} new cell objects, same shape parseIpynbCells() returns
 */
function parsePyCells(text) {
  // Leading whitespace is allowed before the "#" because some editors
  // indent a marker inside a block; anything after the "%%" is the
  // marker's own title and options.
  const markerRe = /^\s*#\s*%%(.*)$/;
  const isTextMarker = (rest) => /\[(markdown|md|raw)\]/i.test(rest);
  const lines = text.split("\n");
  if (!lines.some((line) => markerRe.test(line))) {
    const trimmed = text.trim();
    return trimmed ? [{ id: generateId(), type: CELL_TYPES.PYTHON, content: trimmed, output: "", error: false }] : [];
  }

  // downloadAsPython() prefixes every note line with "# " (or a bare "#"
  // for a line that was empty) — this reverses exactly that, not a
  // general "#" comment stripper, so a genuine Python comment inside a
  // *code* cell is left alone (this only ever runs on a text block's
  // own lines).
  const unescapeNoteLine = (line) => {
    if (line === "#") return "";
    if (line.startsWith("# ")) return line.slice(2);
    if (line.startsWith("#")) return line.slice(1);
    return line;
  };

  const cells = [];
  // Null until the first marker is seen. Anything buffered before then is
  // code the file opened with — a shebang, a block of imports — so it is
  // flushed as a Python cell rather than dropped. The one exception is
  // dewmini's own header, recognised by its first line and discarded, so
  // that exporting and reopening a notebook returns the same cells
  // rather than one more note each time.
  let currentType = null;
  let buffer = [];
  const isOwnHeader = (lines) => {
    const first = lines.find((line) => line.trim());
    return first !== undefined && first.trim().startsWith(PY_HEADER_OPENING);
  };
  const flush = () => {
    if (currentType === null && isOwnHeader(buffer)) { buffer = []; return; }
    const type = currentType === null ? CELL_TYPES.PYTHON : currentType;
    const raw = type === CELL_TYPES.TEXT ? buffer.map(unescapeNoteLine).join("\n") : buffer.join("\n");
    const content = raw.replace(/\n+$/, "");
    if (content.trim()) cells.push({ id: generateId(), type, content, output: "", error: false });
    buffer = [];
  };
  for (const line of lines) {
    const marker = line.match(markerRe);
    if (marker) {
      flush();
      currentType = isTextMarker(marker[1]) ? CELL_TYPES.TEXT : CELL_TYPES.PYTHON;
      continue;
    }
    buffer.push(line);
  }
  flush();
  return cells;
}

/* Loads one of dewlab's own worked examples (assets/examples/*.ipynb) —
 * a real, runnable walkthrough (SQL over a real dataset, a data
 * investigation, a math simulation, text analysis). Replaces the
 * notebook outright, the same as picking a file already does here. */
async function loadBuiltInExample(path, label) {
  let imported;
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    imported = parseIpynbCells(await response.text());
  } catch (err) {
    updateStatus(`Couldn't load "${label}": ${err.message}`, "error");
    return;
  }
  applyImportedCells(imported, label);
}

// ------------------------------------------------------------- drag reorder

/* Removes the "drop indicator" styling (a highlighted top/bottom edge)
 * from whichever cell currently has it, before adding it to a new one —
 * called on every dragover so only one cell ever shows the indicator at
 * once. */
function clearDropMarkers() {
  cellsContainer?.querySelectorAll(".dm-drop-before,.dm-drop-after").forEach((el) => el.classList.remove("dm-drop-before", "dm-drop-after"));
}

/* Wires up reordering cells by dragging their header. This uses the
 * browser's built-in HTML5 Drag and Drop API, which works through four
 * events fired in sequence as a drag happens:
 *   - "dragstart" (on the thing being dragged): remembers which cell's
 *     id is being dragged, in the module-level `draggedId` variable.
 *   - "dragover" (fired repeatedly, on whatever the mouse is currently
 *     over): must call `e.preventDefault()` — the browser's default
 *     behavior is to *refuse* a drop unless something explicitly opts
 *     in, so this is what makes dropping onto a cell allowed at all.
 *     Also decides, from the mouse's vertical position within the
 *     hovered cell, whether to show the drop indicator above or below
 *     it (`before`, comparing the cursor's Y position to the cell's own
 *     vertical midpoint).
 *   - "dragend" (on the thing that was dragged, once the drag is over
 *     however it ended): cleanup, whether or not a drop actually
 *     happened.
 *   - "drop" (on whatever the mouse was over when released): does the
 *     actual reordering — removes the dragged cell from its old array
 *     position and re-inserts it at the new one, using the exact same
 *     "before or after the hovered cell" calculation dragover already
 *     made.
 */
function setupDragAndDrop() {
  if (!cellsContainer) return;

  cellsContainer.addEventListener("dragstart", (e) => {
    const head = e.target.closest(".dm-cell-head");
    if (!head) return;
    draggedId = head.dataset.id;
    head.closest(".dm-cell")?.classList.add("dm-dragging");
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", draggedId);
  });

  cellsContainer.addEventListener("dragend", () => {
    cellsContainer.querySelectorAll(".dm-dragging").forEach((el) => el.classList.remove("dm-dragging"));
    clearDropMarkers();
    draggedId = null;
  });

  cellsContainer.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    if (!draggedId) return;
    clearDropMarkers();
    const target = e.target.closest(".dm-cell");
    if (!target || target.dataset.id === draggedId) return;
    const rect = target.getBoundingClientRect();
    const before = e.clientY < rect.top + rect.height / 2;
    target.classList.add(before ? "dm-drop-before" : "dm-drop-after");
  });

  cellsContainer.addEventListener("drop", (e) => {
    e.preventDefault();
    if (!draggedId) return;
    const target = e.target.closest(".dm-cell");
    clearDropMarkers();

    const fromIdx = cells.findIndex((c) => c.id === draggedId);
    if (fromIdx === -1) { draggedId = null; return; }

    let toIdx = cells.length;
    if (target && target.dataset.id !== draggedId) {
      const rect = target.getBoundingClientRect();
      const before = e.clientY < rect.top + rect.height / 2;
      toIdx = cells.findIndex((c) => c.id === target.dataset.id);
      if (!before) toIdx += 1;
    }

    const [moved] = cells.splice(fromIdx, 1);
    if (toIdx > fromIdx) toIdx -= 1;
    cells.splice(toIdx, 0, moved);

    saveState();
    renderCells();
    draggedId = null;
    updateStatus("Reordered.");
  });
}

// ------------------------------------------------------------------ status

/* Shows a short status message ("Ran.", "Cell deleted.", an error) in the
 * small status line, and — unless it's an error, which stays until
 * something else happens — clears it again after 3.5 seconds. The
 * `if (statusEl.textContent === message)` check inside the timeout
 * guards against a subtle bug: if a second status message arrives before
 * the first one's timer fires, the first timer would otherwise clear the
 * *second* message instead of leaving it alone. */
function updateStatus(message, kind = "") {
  if (!statusEl) return;
  statusEl.textContent = message;
  statusEl.className = "dm-status" + (kind ? ` dm-status-${kind}` : "");
  clearTimeout(statusClearTimer);
  if (kind !== "error") {
    statusClearTimer = setTimeout(() => {
      if (statusEl.textContent === message) { statusEl.textContent = ""; statusEl.className = "dm-status"; }
    }, 3500);
  }
}

// -------------------------------------------------------------- storage

/* Human-sized file size — bytes, then one-decimal KB and MB. */
function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

/* Reflects engine.engineMode()/canStop() into Settings' "Python" section
 * — the same two things the engine itself reports: which path booted,
 * and whether Stop can actually do anything in it. */
function updateExecutionStatus() {
  const el = document.getElementById("settings-execution-status");
  if (!el) return;
  const mode = engine.engineMode();
  if (!mode) {
    el.textContent = "Not started yet — run a cell to start Python.";
    return;
  }
  const where = mode === "worker"
    ? "a background worker, so the page stays responsive"
    : "the main thread (no background worker available here) — a runaway cell will freeze the page until it finishes";
  const stop = engine.canStop()
    ? "Stop can genuinely interrupt a running cell."
    : "Stop can't interrupt a running cell in this mode.";
  el.textContent = `Running in ${where}. ${stop}`;
}

/* Tears the engine down entirely (engine.restart()) and forgets that a
 * filesystem was ever mounted (dfs.reset(), since a fresh interpreter has
 * nothing mounted into it yet), then boots a clean one right away so
 * Settings reflects real status immediately rather than waiting for the
 * next Run click. Shared by both "Restart Python" and "Restart & run
 * all" below — the run-all button needs exactly this same teardown before
 * its own extra step. Returns whether the restart itself succeeded, so a
 * caller that runs cells afterwards knows whether to bother. */
async function restartPython() {
  engine.restart();
  dfs.reset();
  resetRunSequence();
  updateStatus("Restarting Python…");
  updateExecutionStatus();
  updateStorageStatus();
  let ok = true;
  try {
    await ensurePyodide();
    updateStatus("Python restarted.", "ok");
  } catch (err) {
    updateStatus(`Python failed to restart: ${err.message}`, "error");
    ok = false;
  }
  updateExecutionStatus();
  updateStorageStatus();
  return ok;
}

/* Wires the "Restart Python" and "Restart & run all" buttons
 * (DECISIONS_LOG.md 7.108). The second is a reproducibility check: if a
 * notebook does not survive throwing the interpreter away and running
 * every cell fresh, it did not really work — it only looked like it did,
 * because of whatever state a stale namespace was quietly carrying.
 * runAllCells() already resets the *namespace* (resetPageState, the cheap
 * version) before it runs; going through a full restart() first
 * additionally clears anything only a real interpreter restart would —
 * Jedi's completion cache and the mounted filesystem handle among them —
 * so this button is a stronger guarantee than "Run all" alone, not merely
 * its label. */
function initExecutionSection() {
  document.getElementById("settings-restart-python")?.addEventListener("click", async () => {
    if (!confirm("Restart Python? Anything defined in the current session will be lost.")) return;
    await restartPython();
  });
  document.getElementById("settings-restart-run-all")?.addEventListener("click", async () => {
    if (!confirm("Restart Python and run every cell from the top? Anything defined in the current session will be lost.")) return;
    if (await restartPython()) await runAllCells();
  });
}

/* Reflects dfs.getBackend() into Settings' "Files" section: the status
 * line (one message per possible backend), and the
 * choose/reconnect/forget buttons' own visibility and label. Also
 * re-renders the file list, since a backend change always means "what's
 * actually in the mount" just changed too. */
async function updateStorageStatus() {
  const statusEl = document.getElementById("settings-storage-status");
  const chooseBtn = document.getElementById("settings-choose-folder");
  const forgetBtn = document.getElementById("settings-forget-folder");

  const backend = dfs.getBackend();
  const labels = {
    native: "Using a real folder on your computer.",
    opfs: "Using this browser's private storage (fast; not visible in your file browser).",
    idbfs: "Using this browser's private storage (compatibility mode).",
  };
  if (statusEl) statusEl.textContent = backend ? labels[backend] : "Not started yet — run a cell to start Python.";

  if (chooseBtn) {
    const supported = typeof window.showDirectoryPicker === "function";
    if (!supported || backend === "native") {
      chooseBtn.hidden = true;
    } else {
      chooseBtn.hidden = false;
      const hasStored = await dfs.hasStoredFolder();
      chooseBtn.textContent = hasStored ? "Reconnect my folder" : "Use a folder on my computer";
      chooseBtn.dataset.action = hasStored ? "reconnect" : "choose";
    }
  }
  if (forgetBtn) forgetBtn.hidden = backend !== "native";

  renderFileList();
}

/* Re-lists the mounted filesystem's root and redraws the "Files" list —
 * root only, not a full recursive tree with browsable subfolders:
 * a compact Settings section is the wrong place for
 * that (DECISIONS_LOG.md 7.88), and dewmini's own use of the mount
 * (a saved .db file, a dataset a cell downloaded) rarely goes more than
 * one level deep in practice. */
/* Which call to renderFileList() is the current one.
 *
 * The function clears the list, then awaits a directory listing, then
 * appends. Two calls overlapping in that await therefore both clear an
 * already-empty list and then both append, so every file shows twice.
 * Reachable now that a cell run and opening the panel each ask for a
 * redraw, and found by a rename test that suddenly saw three copies of
 * one name. Each call takes a ticket; a call whose ticket is no longer
 * the newest stops before it writes anything. */
let fileListRender = 0;

async function renderFileList() {
  const listEl = document.getElementById("settings-file-list");
  const noteEl = document.getElementById("settings-file-note");
  if (!listEl || !noteEl) return;
  const ticket = ++fileListRender;

  // Cleared unconditionally, not just in the loop below that repopulates
  // it: every early-return branch below also hides this list, but
  // "hidden" only means invisible, not empty — without this, a file
  // deleted down to zero would leave its own stale <li> sitting in the
  // (hidden) list, found by an actual delete-then-recount test, not
  // assumed fine from reading the branches alone.
  listEl.replaceChildren();

  if (!dfs.getBackend()) {
    listEl.hidden = true;
    noteEl.hidden = false;
    noteEl.textContent = "Files appear here once Python starts — run any cell.";
    return;
  }

  let entries;
  try {
    entries = await dfs.listDir("");
    if (ticket !== fileListRender) return;
  } catch (err) {
    if (ticket !== fileListRender) return;
    listEl.hidden = true;
    noteEl.hidden = false;
    noteEl.textContent = `Couldn't list files: ${err.message}`;
    return;
  }

  if (entries.length === 0) {
    listEl.hidden = true;
    noteEl.hidden = false;
    noteEl.textContent = "No files yet. Files a cell writes, or that you upload, will show up here.";
    return;
  }

  noteEl.hidden = true;
  listEl.hidden = false;
  // Cleared again here, not only at the top: this is the first point past
  // every await, so it is the only place a clear cannot be undone by a
  // call that overtook this one.
  listEl.replaceChildren();

  for (const entry of entries) {
    const item = document.createElement("li");
    item.className = "dm-filelist-item";

    /* The name is a button, not a label. A list that shows what exists
     * and offers no way to open any of it is an inventory; being able to
     * open one is what makes this a file manager. A folder stays a plain
     * label, since dewmini has nothing to show for one yet. */
    let nameEl;
    if (entry.isDir) {
      nameEl = document.createElement("span");
      nameEl.textContent = `${entry.name}/`;
    } else {
      nameEl = document.createElement("button");
      nameEl.type = "button";
      nameEl.textContent = entry.name;
      nameEl.addEventListener("click", () => openWorkspaceFile(entry.name));
    }
    nameEl.className = "dm-filelist-item-name";
    nameEl.title = entry.isDir ? entry.name : `Open ${entry.name}`;

    const sizeEl = document.createElement("span");
    sizeEl.className = "dm-filelist-item-size";
    sizeEl.textContent = entry.isDir ? "" : formatFileSize(entry.size);

    const renameBtn = document.createElement("button");
    renameBtn.type = "button";
    renameBtn.className = "dm-filelist-item-rename";
    renameBtn.textContent = "Rename";
    renameBtn.title = `Rename ${entry.name}`;
    renameBtn.addEventListener("click", () => renameFsFile(entry.name));

    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "dm-filelist-item-delete";
    deleteBtn.textContent = "×";
    deleteBtn.title = `Delete ${entry.name}`;
    deleteBtn.setAttribute("aria-label", `Delete ${entry.name}`);
    deleteBtn.addEventListener("click", () => deleteFsFile(entry.name));

    item.append(nameEl, sizeEl, renameBtn, deleteBtn);
    listEl.append(item);
  }
}

/* Renames a file in the workspace, and follows the tab that is showing it.
 *
 * A copy-then-delete, because the filesystem interface has no rename of
 * its own across all three backends. The delete only happens once the copy
 * is written, so a failure halfway leaves the original where it was rather
 * than losing it. */
async function renameFsFile(name) {
  const next = prompt(`Rename "${name}" to:`, name);
  if (next === null) return;
  const target = next.trim();
  if (!target || target === name) return;
  if (target.includes("/")) {
    updateStatus("A name cannot contain a slash.", "error");
    return;
  }

  try {
    const existing = await dfs.listDir("");
    if (existing.some((entry) => entry.name === target)) {
      updateStatus(`${target} already exists.`, "error");
      return;
    }
    const contents = await dfs.readFile(name, "utf8");
    await dfs.writeFile(target, contents);
    await dfs.deleteFile(name);
  } catch (err) {
    updateStatus(`Couldn't rename ${name}: ${err.message}`, "error");
    return;
  }

  // A tab open on the old name would otherwise keep saving to a file that
  // no longer exists, quietly recreating it on the next keystroke.
  const open = notebooks.find((nb) => nb.path === name);
  if (open) {
    open.path = target;
    open.name = notebookNameFor(target);
    saveState();
    renderTabs();
  }
  renderFileList();
  updateStatus(`Renamed ${name} to ${target}.`, "ok");
}

/* Starts a new, empty Python file in the workspace and opens it. Python
 * needs the file to exist before anything can import it, so this writes
 * it rather than only opening an empty tab. */
async function newFsFile() {
  await ensurePyodide();
  const asked = prompt("Name for the new file:", "shapes.py");
  if (asked === null) return;
  let name = asked.trim();
  if (!name) return;
  if (name.includes("/")) { updateStatus("A name cannot contain a slash.", "error"); return; }
  if (!/\.(py|ipynb)$/i.test(name)) name += ".py";

  try {
    const existing = await dfs.listDir("");
    if (existing.some((entry) => entry.name === name)) {
      updateStatus(`${name} already exists. Open it from the list.`, "error");
      return;
    }
    await dfs.writeFile(name, name.toLowerCase().endsWith(".ipynb")
      ? JSON.stringify(cellsToIpynb([]), null, 2)
      : "");
  } catch (err) {
    updateStatus(`Couldn't create ${name}: ${err.message}`, "error");
    return;
  }
  await renderFileList();
  await openWorkspaceFile(name);
}

async function deleteFsFile(name) {
  if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
  try {
    await dfs.deleteFile(name);
  } catch (err) {
    updateStatus(`Couldn't delete ${name}: ${err.message}`, "error");
    return;
  }
  renderFileList();
}

/* Writes one or more picked files into the mounted filesystem's root.
 * Starts Python first if it hasn't already — uploading a file is itself
 * a reasonable first action for a student to take, so it boots Python
 * the same way clicking Run does rather than refusing until a cell has
 * been run. */
async function uploadFsFiles(fileList) {
  const files = fileList ? Array.from(fileList) : [];
  if (!files.length) return;

  try {
    await ensurePyodide();
  } catch (err) {
    /* Says so, rather than returning quietly. ensurePyodide() used to report
     * a boot failure itself and this comment used to say so; it now lets the
     * error out (only the filesystem mount inside it is caught), so without
     * this an upload after a failed boot did nothing at all and explained
     * nothing either. */
    updateStatus(`Python isn't available, so the upload can't go anywhere: ${err.message}`,
                 "error");
    return;
  }

  let uploaded = 0;
  for (const file of files) {
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      await dfs.writeFile(file.name, bytes);
      uploaded++;
    } catch (err) {
      updateStatus(`Couldn't upload ${file.name}: ${err.message}`, "error");
    }
  }

  renderFileList();
  if (uploaded > 0) updateStatus(`Uploaded ${uploaded} file${uploaded === 1 ? "" : "s"}.`, "ok");
}

function initStorageSection() {
  dfs.configure({ onBackendChange: () => updateStorageStatus() });

  document.getElementById("settings-choose-folder")?.addEventListener("click", async (e) => {
    const action = e.currentTarget.dataset.action || "choose";
    try {
      if (action === "reconnect") await dfs.reconnectFolder();
      else await dfs.chooseFolder();
      updateStatus("Now using a folder on your computer for files.");
    } catch (err) {
      updateStatus(`Couldn't use that folder: ${err.message}`, "error");
    }
    updateStorageStatus();
  });

  document.getElementById("settings-forget-folder")?.addEventListener("click", async () => {
    if (!confirm("Stop using that folder? dewmini switches back to this browser's private storage — nothing in the folder itself is deleted.")) return;
    await dfs.forgetFolder();
    updateStatus("Stopped using that folder. Reload the page to switch storage.");
    updateStorageStatus();
  });

  document.getElementById("settings-new-file")?.addEventListener("click", () => newFsFile());
  document.getElementById("settings-upload-file")?.addEventListener("click", () => document.getElementById("settings-upload-file-input")?.click());
  document.getElementById("settings-upload-file-input")?.addEventListener("change", (e) => {
    uploadFsFiles(e.target.files);
    e.target.value = "";
  });

  updateStorageStatus();
}

// ------------------------------------------------------------------ panels

/**
 * A draggable strip along the edge a docked panel grows *into* — its left
 * edge when docked right, its right edge when docked left.
 *
 * This replaces native CSS `resize: horizontal` on both, for two separate
 * reasons. On a right-docked panel the native handle is unusable: it sits
 * at the box's bottom-right corner, flush with the browser window's own
 * right edge, with no room to drag further right and grow it — found by an
 * actual drag test, not assumed from the CSS (DECISIONS_LOG.md 7.84). On a
 * left-docked panel it *works*, which is why it was left alone — but it is
 * a small corner triangle facing a full-height strip on the panel opposite.
 * Two rails, two affordances, only one of them findable: that asymmetry is
 * why this is now shared rather than right-docked only.
 *
 * `side` is the edge the panel is docked to, so the drag maths runs the
 * right way round: a right-docked panel grows as the pointer moves left,
 * a left-docked one as it moves right. `min`/`max` mirror the panel's own
 * CSS `min-width`/`max-width`, kept in sync by hand — the constants are
 * already known and simpler than parsing them back out of the DOM.
 * `onResize` fires once per drag, on release rather than per frame, for a
 * caller that wants to persist the new width.
 */
function makeEdgeResizable(panel, side = "right", min = 256, max = 640, onResize = null) {
  if (!panel || panel.querySelector(".dl-panel-resize-handle")) return;
  const handle = document.createElement("div");
  handle.className = "dl-panel-resize-handle"
    + (side === "left" ? " dl-panel-resize-handle-right" : "");
  handle.setAttribute("aria-hidden", "true");
  panel.prepend(handle);

  let startX = 0;
  let startWidth = 0;

  function onMove(ev) {
    const dx = side === "left" ? ev.clientX - startX : startX - ev.clientX;
    const next = Math.max(min, Math.min(startWidth + dx, Math.min(max, window.innerWidth)));
    panel.style.width = `${next}px`;
  }
  function onUp() {
    handle.classList.remove("dl-panel-resize-active");
    document.removeEventListener("pointermove", onMove);
    document.removeEventListener("pointerup", onUp);
    if (onResize) onResize();
  }
  handle.addEventListener("pointerdown", (ev) => {
    startX = ev.clientX;
    startWidth = panel.getBoundingClientRect().width;
    handle.classList.add("dl-panel-resize-active");
    document.addEventListener("pointermove", onMove);
    document.addEventListener("pointerup", onUp);
    ev.preventDefault();
  });
}

/* Opens and closes one docked panel, closing only the panels that would
 * otherwise sit on top of it — the ones docked to the same edge.
 *
 * `conflicts` rather than a single `otherPanel`: dewmini used to have two
 * panels on one edge, where "the other one" was unambiguous. With a rail on
 * each edge, closing every other panel would make the two rails fight — the
 * whole point of two rails is having a definition open beside your own
 * variables.
 *
 * A click outside no longer closes anything either. A docked rail is a
 * permanent pane, not a popover: dismiss-on-outside-click is right for
 * something floating over the page and actively wrong for something the
 * page has made room for, where every click on your own notebook would
 * close the reference you opened to read while writing it. Escape and the
 * close button remain, which are the deliberate ways out. */
function wirePanel(panel, toggle, closeBtn, conflicts = [], onOpen = null) {
  if (!panel) return;
  const setOpen = (open) => {
    panel.hidden = !open;
    toggle?.setAttribute("aria-expanded", String(open));
    if (!open) return;
    for (const other of conflicts) {
      if (other && !other.hidden) other.hidden = true;
    }
    // After the panel is visible, not before: a panel that only draws
    // itself while open (the variable inspector) needs its own "you are
    // open now" moment, and reading `hidden` from inside this callback
    // has to see the new value.
    onOpen?.();
  };
  toggle?.addEventListener("click", () => setOpen(panel.hidden));
  closeBtn?.addEventListener("click", () => {
    setOpen(false);
    toggle?.focus();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !panel.hidden) setOpen(false);
  });
}

/* Remembers what a reader left open on each edge, the same
 * localStorage-persisted-sidebar mechanism tutorial pages use (see
 * saveSidebarState()/restoreSidebarState() in tutorial-runtime.js,
 * DECISIONS_LOG.md 7.83) — a returning reader's rails come back open
 * rather than needing to be reopened, since they are meant to be
 * permanent panes, not popovers that happen to be open right now.
 *
 * A {left, right} pair rather than the single value dewmini stored while
 * both its panels shared one edge: with a rail on each side, "what is
 * open" is two independent answers. */
const SIDEBAR_KEY = "dewlab:dewmini:sidebar";

function saveSidebarState() {
  const openOn = (ids) => ids.find((id) => {
    const panel = document.getElementById(id);
    return panel && !panel.hidden;
  }) || null;
  // Widths as well as which panel is open. A rail dragged to half the
  // screen and back to its default on every reload is not a working split
  // screen, which is the whole reason someone widens one.
  const widthOf = (id) => {
    const px = document.getElementById(id)?.style.width;
    return px ? parseInt(px, 10) : null;
  };
  try {
    localStorage.setItem(SIDEBAR_KEY, JSON.stringify({
      left: openOn(["dm-workbench"]),
      right: openOn(["dm-library", "dl-settings"]),
      widths: {
        "dm-library": widthOf("dm-library"),
        "dm-workbench": widthOf("dm-workbench"),
        "dl-settings": widthOf("dl-settings"),
      },
    }));
  } catch (e) { /* private mode, blocked storage: nothing to remember */ }
}

/* The other half of saveSidebarState() — reopens whatever was left open
 * last time by clicking its toggle, reusing that toggle's own open logic
 * rather than duplicating it. Skipped below the phone breakpoint, where
 * a panel is a bottom sheet covering most of the screen rather than a
 * sidebar worth leaving open by default. */
const PANEL_TOGGLES = {
  "dm-library": "dm-library-toggle",
  "dm-workbench": "dm-workbench-toggle",
  "dl-settings": "dl-settings-toggle",
};

function restoreSidebarState() {
  if (!window.matchMedia("(min-width: 34rem)").matches) return;
  let state;
  try {
    state = JSON.parse(localStorage.getItem(SIDEBAR_KEY) || "{}");
  } catch (e) {
    return;
  }
  // Widths first, so a restored panel opens at the size it was left rather
  // than opening at its default and visibly jumping.
  for (const [id, px] of Object.entries(state.widths || {})) {
    if (typeof px === "number" && px > 0) {
      const panel = document.getElementById(id);
      if (panel) panel.style.width = `${px}px`;
    }
  }
  for (const panelId of [state.left, state.right]) {
    const toggleId = PANEL_TOGGLES[panelId];
    if (toggleId) document.getElementById(toggleId)?.click();
  }
}

/* Keeps `<html data-dl-panel-left>` / `data-dl-panel-right` in sync with
 * what is actually open on each edge, regardless of which of a panel's
 * several open/close paths (toggle click, close button, Escape, another
 * panel on the same edge opening) fired — a MutationObserver on each
 * panel's `hidden` property, rather than hooking every call site.
 *
 * These are the *shared* attributes tutorial-style.css has read since
 * DECISIONS_LOG.md 7.83, one per edge with its own width variable. dewmini
 * used to override them with a single `data-dl-panel-open` and one width,
 * which was a fair simplification while both its panels docked right
 * (7.84) and is exactly wrong with a rail on each side: one attribute
 * cannot say which edge to make room on, and one width cannot describe two
 * panels of different sizes open at once.
 *
 * A ResizeObserver keeps each side's width variable in step with its
 * panel's *real* rendered width rather than a guess, since a docked
 * sidebar can be dragged wider or narrower at any time. */
function watchPanelOverlap(sides) {
  const entries = Object.entries(sides)
    .map(([side, panels]) => [side, panels.filter(Boolean)])
    .filter(([, panels]) => panels.length);
  if (!entries.length) return;

  const updateAttrs = () => {
    for (const [side, panels] of entries) {
      document.documentElement.toggleAttribute(
        `data-dl-panel-${side}`, panels.some((p) => !p.hidden));
    }
  };

  for (const [, panels] of entries) {
    for (const panel of panels) {
      new MutationObserver(() => { updateAttrs(); saveSidebarState(); })
        .observe(panel, { attributes: true, attributeFilter: ["hidden"] });
    }
  }
  // The attributes only, not a persisted-state write: every panel is still
  // hidden at this point in startup, before restoreSidebarState() has had a
  // chance to reopen what was actually saved last time — persisting here
  // would overwrite a real saved preference with "everything closed" on
  // every single load.
  updateAttrs();

  const widthObserver = new ResizeObserver((observed) => {
    for (const entry of observed) {
      const panel = entry.target;
      if (panel.hidden) continue;
      const side = entries.find(([, panels]) => panels.includes(panel))?.[0];
      if (!side) continue;
      // offsetWidth, not the observer's own contentRect: the margin needs
      // to clear the panel's full border box (border + padding), plus a
      // small gutter so text doesn't sit flush against its edge.
      document.documentElement.style.setProperty(`--dl-panel-${side}-w`, `${panel.offsetWidth + 16}px`);
    }
  });
  for (const [, panels] of entries) {
    for (const panel of panels) widthObserver.observe(panel);
  }
}

function initPanels() {
  const settingsPanel = document.getElementById("dl-settings");
  const workbenchPanel = document.getElementById("dm-workbench");
  const libraryPanel = document.getElementById("dm-library");

  // Every docked panel gets the same full-height strip, on whichever edge
  // it grows into. The left rail used to rely on native `resize:
  // horizontal` instead — which works, but puts a small corner triangle
  // opposite a full-height strip, so the two rails behaved differently for
  // no reason a reader could see (DECISIONS_LOG.md 7.103). The min/max
  // mirror each panel's own CSS.
  // Left is the project: files, variables, notes. Right is everything
  // outside it: the reference, and settings.
  makeEdgeResizable(settingsPanel, "right", 256, 640, saveSidebarState);
  makeEdgeResizable(libraryPanel, "right", 256, 640, saveSidebarState);
  makeEdgeResizable(workbenchPanel, "left", 256, 640, saveSidebarState);

  // Same-edge panels close each other; opposite-edge ones coexist.
  wirePanel(settingsPanel, document.getElementById("dl-settings-toggle"),
            document.getElementById("dl-settings-close"), [libraryPanel]);
  wirePanel(libraryPanel, document.getElementById("dm-library-toggle"),
            document.getElementById("dm-library-close"), [settingsPanel]);
  wirePanel(workbenchPanel, document.getElementById("dm-workbench-toggle"),
            document.getElementById("dm-workbench-close"), [],
            () => { refreshVariables(); renderFileList(); });

  watchPanelOverlap({ left: [workbenchPanel], right: [libraryPanel, settingsPanel] });
  restoreSidebarState();

  // Hide any Settings section that ended up with nothing in it (mirrors the
  // rest of the site: an empty section is furniture, not a feature).
  settingsPanel?.querySelectorAll(".dl-settings-section").forEach((section) => {
    if (section.textContent.trim() === "") section.hidden = true;
  });
}

// ----------------------------------------------------------- shared texture

/* This whole section — loadTexture/saveTexture/applyTexture/initTexture —
 * is dewmini's own copy of the reading-preference settings (theme, font,
 * size, and so on) shared with every other dewlab page, reading and
 * writing the same "dewlab:texture" localStorage key so a choice made
 * here follows a reader to a tutorial page and back. See
 * docs/tutorial-runtime-explained.md's own notes on the identical
 * functions there (the try/catch-around-localStorage convention, the
 * `{...a, ...b}` merge-with-defaults pattern) for more detail than
 * repeated here — the code is close to line-for-line the same. */
const TEXTURE_DEFAULTS = { theme: "system", font: "serif", size: 18, width: 34, link: "#d4692a" };

function loadTexture() {
  try {
    return { ...TEXTURE_DEFAULTS, ...JSON.parse(localStorage.getItem("dewlab:texture") || "{}") };
  } catch {
    return { ...TEXTURE_DEFAULTS };
  }
}

function saveTexture(state) {
  try { localStorage.setItem("dewlab:texture", JSON.stringify(state)); } catch {}
}

function applyTexture(state) {
  const root = document.documentElement;
  if (state.theme === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", state.theme);
  if (state.font === "serif") root.removeAttribute("data-font"); else root.setAttribute("data-font", state.font);
  root.style.setProperty("--dl-font-size", `${state.size}px`);
  root.style.setProperty("--dl-line-width", `${state.width}rem`);
  root.style.setProperty("--dl-link", state.link);
}

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
      const current = group.hasAttribute("data-number") ? String(state[key]) : state[key];
      for (const btn of group.querySelectorAll("button")) btn.setAttribute("aria-pressed", String(btn.dataset.value === current));
    }
    if (sizeEl) sizeEl.value = state.size;
    if (widthEl) widthEl.value = state.width;
    if (linkEl) linkEl.value = state.link;
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
      state[group.dataset.texture] = group.hasAttribute("data-number") ? Number(btn.dataset.value) : btn.dataset.value;
      commit();
    });
  }
  sizeEl?.addEventListener("input", () => { state.size = Number(sizeEl.value); commit(); });
  widthEl?.addEventListener("input", () => { state.width = Number(widthEl.value); commit(); });
  linkEl?.addEventListener("input", () => { state.link = linkEl.value; commit(); });
  document.getElementById("dl-texture-reset")?.addEventListener("click", () => { Object.assign(state, TEXTURE_DEFAULTS); commit(); });

  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      if (state.theme === "system") onThemeChange(isDarkNow());
    });
  }

  sync();
  return state;
}

// ------------------------------------------------------------ editor prefs

/* Same load/save/apply/init shape as the texture section above, for a
 * different set of preferences: how code itself is displayed (its own
 * size, how roomy a cell feels, cursor thickness, gutter/current-line
 * visibility) rather than how the page's reading text looks. These are
 * dewmini-specific — a plain tutorial page has no code editor
 * settings of its own, since a tutorial's cells are meant to look
 * consistent between students, not customized per reader the way a
 * personal notebook's editor reasonably can be. */
const EDITOR_DEFAULTS = { codeSize: 15, density: "cozy", cursor: "medium", gutter: "on", activeLine: "on" };
const EDITOR_KEY_MAP = { density: "density", cursor: "cursor", gutter: "gutter", activeline: "activeLine" };

function loadEditorPrefs() {
  try {
    return { ...EDITOR_DEFAULTS, ...JSON.parse(localStorage.getItem("dewmini:editor") || "{}") };
  } catch {
    return { ...EDITOR_DEFAULTS };
  }
}

function saveEditorPrefs(state) {
  try { localStorage.setItem("dewmini:editor", JSON.stringify(state)); } catch {}
}

function applyEditorPrefs(state) {
  const root = document.documentElement;
  root.style.setProperty("--dm-code-size", `${state.codeSize}px`);
  root.setAttribute("data-dm-density", state.density);
  root.setAttribute("data-dm-cursor", state.cursor);
  if (state.gutter === "off") root.setAttribute("data-dm-gutter", "off"); else root.removeAttribute("data-dm-gutter");
  if (state.activeLine === "off") root.setAttribute("data-dm-activeline", "off"); else root.removeAttribute("data-dm-activeline");
}

function initEditorSettings() {
  const state = loadEditorPrefs();
  applyEditorPrefs(state);

  const panel = document.getElementById("dl-settings-editor");
  if (!panel) return state;

  const sizeEl = document.getElementById("dm-code-size");

  function sync() {
    for (const group of panel.querySelectorAll(".dl-seg")) {
      const stateKey = EDITOR_KEY_MAP[group.dataset.dm];
      const current = state[stateKey];
      for (const btn of group.querySelectorAll("button")) btn.setAttribute("aria-pressed", String(btn.dataset.value === current));
    }
    if (sizeEl) sizeEl.value = state.codeSize;
  }

  function commit() {
    applyEditorPrefs(state);
    saveEditorPrefs(state);
    sync();
  }

  for (const group of panel.querySelectorAll(".dl-seg")) {
    group.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      state[EDITOR_KEY_MAP[group.dataset.dm]] = btn.dataset.value;
      commit();
    });
  }
  sizeEl?.addEventListener("input", () => { state.codeSize = Number(sizeEl.value); commit(); });
  document.getElementById("dm-editor-reset")?.addEventListener("click", () => { Object.assign(state, EDITOR_DEFAULTS); commit(); });

  sync();
  return state;
}

// ------------------------------------------------------------------- notes

function initNotes() {
  const notesEl = document.getElementById("dm-notes");
  if (!notesEl) return;
  try { notesEl.value = localStorage.getItem(NOTES_KEY) || ""; } catch {}
  // Saved on every keystroke rather than debounced — a note is short enough
  // that the write is free, and a debounce risks losing the last few
  // characters if the panel closes or the page navigates before it fires.
  notesEl.addEventListener("input", () => {
    try { localStorage.setItem(NOTES_KEY, notesEl.value); } catch {}
  });
}

/* Pulses "See an example" on the very first time this page has ever loaded
 * in this browser, then never again — an invitation, not a nag. Still spent
 * only on an empty notebook: the button now lives in the toolbar and so is
 * always visible, but a reader arriving with cells already in it (an
 * imported .ipynb, say) has plainly not come here for the example. */
function maybeHighlightExample() {
  if (cells.length) return;
  const btn = document.getElementById("dm-show-example");
  if (!btn) return;
  try {
    if (localStorage.getItem("dewmini:visited") === "1") return;
    localStorage.setItem("dewmini:visited", "1");
  } catch {
    return;
  }
  btn.classList.add("dm-pulse");
  btn.addEventListener("animationend", () => btn.classList.remove("dm-pulse"), { once: true });
}

/* Wires up the Settings → Practice "in order / random" switch — the UI
 * counterpart of loadPracticeOrder()/nextPracticeIndex() above. */
function initPracticeOrderSettings() {
  const panel = document.getElementById("dl-settings-practice");
  const group = panel?.querySelector('.dl-seg[data-dm="practice-order"]');
  if (!group) return;
  const sync = () => {
    const mode = loadPracticeOrder();
    for (const btn of group.querySelectorAll("button")) btn.setAttribute("aria-pressed", String(btn.dataset.value === mode));
  };
  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    try { localStorage.setItem(PRACTICE_ORDER_KEY, btn.dataset.value); } catch {}
    sync();
  });
  sync();
}

/* Wires up the Settings → Run time "on / off" switch — applied as a
 * data-dm-runstats attribute on <html> (read by renderCellRunLine()),
 * re-painted on every already-rendered cell immediately on toggle, not
 * just future runs. Only the duration half of the run-line is gated by
 * this — order and staleness are core identity, not a "nice to know",
 * and stay visible either way. */
const RUN_STATS_KEY = "dewmini:show-run-stats";

function initRunStatsSetting() {
  let show = true;
  try { show = localStorage.getItem(RUN_STATS_KEY) !== "off"; } catch {}

  const apply = () => {
    document.documentElement.setAttribute("data-dm-runstats", show ? "on" : "off");
    cells.forEach(renderCellRunLine);
  };
  apply();

  const group = document.querySelector('#dl-settings-execution .dl-seg[data-dm="runstats"]');
  if (!group) return;
  const sync = () => {
    for (const btn of group.querySelectorAll("button")) btn.setAttribute("aria-pressed", String(btn.dataset.value === (show ? "on" : "off")));
  };
  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    show = btn.dataset.value === "on";
    try { localStorage.setItem(RUN_STATS_KEY, show ? "on" : "off"); } catch {}
    apply();
    sync();
  });
  sync();
}

// -------------------------------------------------------------- chrome/misc

/* Measures the header's real on-screen height and publishes it as a CSS
 * custom property, so other elements can reliably sit below it — same
 * function, same reasoning, as tutorial-runtime.js's own
 * trackChromeHeight() (see that file's explanation doc for the longer
 * version of why this is measured rather than assumed to be a fixed
 * number). */
function trackChromeHeight() {
  const chrome = document.getElementById("dl-chrome");
  if (!chrome) return;
  const publish = () => {
    document.documentElement.style.setProperty("--dl-chrome-h", `${Math.round(chrome.getBoundingClientRect().height)}px`);
  };
  publish();
  if (typeof ResizeObserver === "function") new ResizeObserver(publish).observe(chrome);
  else window.addEventListener("resize", publish);
}

/* Keeps every CodeMirror editor's own colour theme in sync with the
 * page's theme, even when the theme changes for a reason this file
 * didn't cause directly — a MutationObserver is a browser API that calls
 * a function whenever something about a specific element changes (here,
 * any attribute on `<html>`); this only reacts when the change was
 * specifically to `data-theme`, and re-applies the right editor theme to
 * every cell's editor when it was. This is a belt-and-braces safety net
 * on top of initTexture()'s own onThemeChange callback — that callback
 * already handles the normal case of a reader clicking a theme button in
 * Settings; this one exists in case the theme changes some other way. */
function observeThemeChanges() {
  const observer = new MutationObserver((mutations) => {
    if (!mutations.some((m) => m.attributeName === "data-theme")) return;
    const dark = isDarkNow();
    cells.forEach((c) => { if (c.editor) { try { setEditorTheme(c.editor, dark); } catch {} } });
    if (fileEditor) { try { setEditorTheme(fileEditor, dark); } catch {} }
  });
  observer.observe(document.documentElement, { attributes: true });
}

/* Wires up every toolbar and Settings button that doesn't already have
 * its own dedicated init*() function above — one line per button, each
 * just calling the one function that actually does the work. */
function wireToolbar() {
  document.getElementById("new-notebook")?.addEventListener("click", () => {
    openNotebook(makeNotebook(`Notebook ${notebooks.length + 1}`));
    updateStatus("New notebook.");
  });
  document.getElementById("add-practice")?.addEventListener("click", () => addPracticeProblem());
  document.getElementById("dm-add-imports")?.addEventListener("click", () => addCell(CELL_TYPES.PYTHON, IMPORTS_SNIPPET));
  document.getElementById("dm-show-example")?.addEventListener("click", () => loadExampleCells());
  document.getElementById("dm-help-example-link")?.addEventListener("click", (e) => {
    e.preventDefault();
    loadExampleCells();
  });
  document.getElementById("run-all")?.addEventListener("click", () => runAllCells());
  document.getElementById("clear-output")?.addEventListener("click", () => clearAllOutputs());
  document.getElementById("clear-all")?.addEventListener("click", () => {
    if (!cells.length) return;
    if (!confirm("Clear every cell? This can't be undone.")) return;
    cells.forEach((c) => c.editor?.destroy());
    setCells([]);
    saveState();
    renderCells();
    updateStatus("Cleared.");
  });
  document.getElementById("dm-view-cells")?.addEventListener("click", () => setView(VIEWS.CELLS));
  document.getElementById("dm-view-file")?.addEventListener("click", () => setView(VIEWS.FILE));
  document.getElementById("download-python")?.addEventListener("click", downloadAsPython);
  document.getElementById("download-html")?.addEventListener("click", downloadAsHtml);
  document.getElementById("download-ipynb")?.addEventListener("click", downloadAsIpynb);
  document.getElementById("import-ipynb")?.addEventListener("click", () => document.getElementById("import-ipynb-file")?.click());
  document.getElementById("import-ipynb-file")?.addEventListener("change", handleImportFile);
  document.getElementById("reload-stale-imports")?.addEventListener("click", reloadStaleImports);
  document.getElementById("dismiss-stale-imports")?.addEventListener("click", hideStaleImportsNotice);
  // Built-in worked examples — one listener for all four buttons, keyed
  // off the path/label already sitting in each button's own markup.
  for (const btn of document.querySelectorAll("#dl-settings-download [data-example]")) {
    btn.addEventListener("click", () => loadBuiltInExample(btn.dataset.example, btn.textContent.trim()));
  }
  document.getElementById("dismiss-import-compat")?.addEventListener("click", () => {
    const notice = document.getElementById("import-compat-notice");
    if (notice) notice.hidden = true;
  });
  document.getElementById("print-pdf")?.addEventListener("click", () => window.print());
}

// ------------------------------------------------------------------- start

let initialized = false;

async function init() {
  // A module script runs before DOMContentLoaded fires (it isn't "loading"
  // by the time this executes), so both the listener below and the direct
  // call would otherwise both fire and double up every listener this sets.
  if (initialized) return;
  initialized = true;

  cellsContainer = document.getElementById("cells-container");
  emptyEl = document.getElementById("dm-empty");
  statusEl = document.getElementById("dm-status");
  tabsEl = document.getElementById("dm-tabs");

  loadSavedState();
  initPanels();
  initTexture((dark) => {
    cells.forEach((c) => { if (c.editor) { try { setEditorTheme(c.editor, dark); } catch {} } });
    if (fileEditor) { try { setEditorTheme(fileEditor, dark); } catch {} }
  });
  initEditorSettings();
  initNotes();
  initFilename();
  initPracticeOrderSettings();
  initRunStatsSetting();
  initStorageSection();
  initExecutionSection();
  initReferenceSection();
  initVariablesSection();
  loadDataCatalogue();
  wireToolbar();
  setupDragAndDrop();
  renderTabs();
  renderCells();
  updateViewSwitch();
  maybeHighlightExample();
  trackChromeHeight();
  observeThemeChanges();
}

document.addEventListener("DOMContentLoaded", init);
if (document.readyState !== "loading") init();
