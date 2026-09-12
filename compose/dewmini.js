
import { createCodeEditor, setEditorTheme } from "../assets/vendor/codemirror.bundle.js";
import * as dfs from "./dewmini-fs.js";
import * as engine from "../assets/pyodide-engine.js";
import * as jsEngine from "./js-cell-engine.js";
import { mountSitePreview } from "../assets/site-relay.js";

const PYODIDE_VERSION = "0.28.3";
// The pre-tabs key: one notebook, stored as a bare array of cells. Still read
// once, by migrateLegacyCells() below, so a reader who left work here before
// tabs existed finds it again afterwards.
const LEGACY_CELLS_KEY = "dewmini:cells:v1";
const NOTEBOOKS_KEY = "dewmini:notebooks:v1";
const NOTES_KEY = "dewmini:notes";

// Beyond the curriculum's numpy/pandas/matplotlib baseline (DECISIONS.md
// "Core libraries"), dewmini also loads sqlite3 (an unvendored stdlib
// module in Pyodide, one extra loadPackage() entry)
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

const CELL_TYPES = { PYTHON: "python", TEXT: "text", WEB: "web", SQL: "sql", JAVASCRIPT: "javascript" };

const CELL_TYPE_TOGGLES = [
  { type: CELL_TYPES.WEB, dm: "celltype-web", key: "dewmini:celltype-web", defaultOn: false },
  { type: CELL_TYPES.SQL, dm: "celltype-sql", key: "dewmini:celltype-sql", defaultOn: false },
  { type: CELL_TYPES.JAVASCRIPT, dm: "celltype-javascript", key: "dewmini:celltype-javascript", defaultOn: true },
];

let enabledCellTypes = new Set([CELL_TYPES.PYTHON, CELL_TYPES.TEXT]);

const CSS_PREVIEW_MARKUP = `<h2>Heading</h2>
<p>A paragraph of text, with a <a href="#">link</a> inside it.</p>
<button>A button</button>
<ul><li>One item</li><li>Another item</li></ul>`;
const IMPORTS_SNIPPET = "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n";

const READ_NOT_RUN_TYPES = new Set([CELL_TYPES.TEXT]);

const RUNS_AGAINST_SESSION = new Set([CELL_TYPES.PYTHON, CELL_TYPES.SQL, CELL_TYPES.JAVASCRIPT]);

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

const VIEWS = { CELLS: "cells", FILE: "file", SITE: "site" };

const FILE_RUN_ID = "cell-file-run";

let fileEditor = null;
let fileRunOutputEl = null;
let fileParseTimer = null;
// A site tab's three CodeMirror editors, live while it is the notebook on
// screen — destroyed and re-created on every tab switch the same as
// fileEditor above, for the same reason (a CodeMirror instance holds its
// own DOM and listeners; nothing here is meant to outlive its render).
let siteEditors = null;
let cellsContainer, emptyEl, statusEl, tabsEl;
let statusClearTimer = null;

// The live Pyodide interpreter, cell execution, hover/signature-help, and
// filesystem mounting all go through the shared assets/pyodide-engine.js
// now — rather than this file holding its own
// `pyodide`/`tools`/`inspectModule` references and talking to Pyodide
// directly, the way its first version did.
// toolsSourceCache stays: downloadAsHtml()'s embedded bootstrap below
// still needs tutorial_tools.py's raw source text, independent of the
// live engine (a downloaded copy runs its own simple main-thread
// Pyodide, same as the live page's own file:// fallback would).
let toolsSourceCache = null;
let running = false;
let runningCellId = null;
let runSequenceCounter = 0;

let draggedId = null;

function generateId() {
  return `cell-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

function readCells(saved) {
  if (!Array.isArray(saved)) return [];
  return saved
    .filter((c) => c && c.id)
    .map(migrateLegacyCellType)
    .filter((c) => Object.values(CELL_TYPES).includes(c.type))
    .map((c) => ({
      id: c.id, type: c.type, content: c.content || "", style: c.style || "",
      output: c.output || "", error: !!c.error, collapsed: !!c.collapsed,
      // A reader's own name for this cell — "a handle to hold on to"
      // (planning/CELL_IDENTITY.md §4) — optional, so most cells carry
      // none at all rather than an empty string round-tripping forever.
      name: c.name || undefined,
    }));
}

function migrateLegacyCellType(c) {
  if (c.type === "html") return { ...c, type: CELL_TYPES.WEB, content: c.content || "", style: "" };
  if (c.type === "css") return { ...c, type: CELL_TYPES.WEB, content: "", style: c.content || "" };
  return c;
}

/* A notebook with nothing in it yet. Named rather than numbered-only so a
 * tab strip reads as a row of names, not a row of "Untitled". */
function makeNotebook(name, cellList = [], view = VIEWS.CELLS) {
  return { id: `nb-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
           name, cells: cellList, view };
}

function migrateLegacyCells() {
  let legacy = [];
  try {
    legacy = readCells(JSON.parse(localStorage.getItem(LEGACY_CELLS_KEY) || "[]"));
  } catch {
    legacy = [];
  }
  return legacy.length ? [makeNotebook("Notebook", legacy)] : [];
}

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
                      view: nb.view === VIEWS.FILE ? VIEWS.FILE
                          : nb.view === VIEWS.SITE ? VIEWS.SITE : VIEWS.CELLS,
                      // Which workspace file this tab is, when it is one.
                      // Without this a reload would quietly turn it into an
                      // ordinary notebook and stop saving the file.
                      ...(typeof nb.path === "string" && nb.path ? { path: nb.path } : {}),
                      // A site tab's own three files, and where its CSS and
                      // JavaScript live when they exist. Restored here
                      // rather than re-read from disk on every reload —
                      // the same "localStorage is the fast-path cache, the
                      // real file is the debounced write" pattern every
                      // other workspace-backed tab already follows.
                      ...(nb.view === VIEWS.SITE ? {
                        siteCssPath: typeof nb.siteCssPath === "string" ? nb.siteCssPath : "",
                        siteJsPath: typeof nb.siteJsPath === "string" ? nb.siteJsPath : "",
                        siteHtml: typeof nb.siteHtml === "string" ? nb.siteHtml : "",
                        siteCss: typeof nb.siteCss === "string" ? nb.siteCss : "",
                        siteJs: typeof nb.siteJs === "string" ? nb.siteJs : "",
                      } : {}) }));
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

function setCells(next) {
  cells = next;
  activeNotebook().cells = next;
}

const outputsTooLargeToSave = new Set();

let warnedDroppedOutputs = 0;

function writeSavedState(skipOutputFor) {
  const plainCells = (list) => list.map(({ id, type, content, style, output, error, collapsed, name }) => ({
    id, type, content, style: style || "",
    output: skipOutputFor.has(id) ? "" : (output || ""),
    error: !!error,
    collapsed: !!collapsed,
    ...(name ? { name } : {}),
  }));
  try {
    localStorage.setItem(NOTEBOOKS_KEY, JSON.stringify({
      active: activeNotebookId,
      notebooks: notebooks.map((nb) => ({ id: nb.id, name: nb.name, view: nb.view || VIEWS.CELLS,
                                         ...(nb.path ? { path: nb.path } : {}),
                                         ...(nb.view === VIEWS.SITE ? {
                                           siteCssPath: nb.siteCssPath || "", siteJsPath: nb.siteJsPath || "",
                                           siteHtml: nb.siteHtml || "", siteCss: nb.siteCss || "", siteJs: nb.siteJs || "",
                                         } : {}),
                                         cells: plainCells(nb.cells) })),
    }));
    return true;
  } catch {
    return false;
  }
}

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

function pruneDroppedOutputs() {
  if (!outputsTooLargeToSave.size) return;
  const live = new Set();
  for (const nb of notebooks) for (const cell of nb.cells) live.add(cell.id);
  for (const id of outputsTooLargeToSave) {
    if (!live.has(id)) outputsTooLargeToSave.delete(id);
  }
  warnedDroppedOutputs = Math.min(warnedDroppedOutputs, outputsTooLargeToSave.size);
}

function allowOutputToSaveAgain(cellId) {
  if (!outputsTooLargeToSave.delete(cellId)) return;
  warnedDroppedOutputs = Math.min(warnedDroppedOutputs, outputsTooLargeToSave.size);
}

function showNotebook(id) {
  if (id === activeNotebookId) return;
  const target = notebooks.find((nb) => nb.id === id);
  if (!target) return;
  flushFileEditor();
  cells.forEach(destroyCellEditors);
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
  cells.forEach(destroyCellEditors);
  notebooks.push(notebook);
  activeNotebookId = notebook.id;
  cells = notebook.cells;
  saveState();
  renderTabs();
  renderCells();
  updateFilenameField();
}

function closeNotebook(id) {
  if (notebooks.length < 2) return;
  const index = notebooks.findIndex((nb) => nb.id === id);
  if (index === -1) return;
  const notebook = notebooks[index];
  if (notebook.cells.length && !confirm(`Close "${notebook.name}"? Its ${notebook.cells.length} cell${notebook.cells.length === 1 ? "" : "s"} will be gone.`)) return;

  if (id === activeNotebookId) cells.forEach(destroyCellEditors);
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

function renderTabs() {
  // Every call site that redraws the tab strip is exactly when the
  // Files panel's own notebook list needs redrawing too — a notebook
  // opened, closed, or renamed changes both at once.
  renderNotebookList();

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
    if (notebook.view === VIEWS.FILE || notebook.view === VIEWS.SITE) {
      const badge = document.createElement("span");
      badge.className = "dm-tab-view";
      badge.textContent = notebook.view === VIEWS.SITE ? "site" : "file";
      label.append(" ", badge);
    }
    label.title = notebook.view === VIEWS.SITE
      ? `${notebook.name}, a small website (double-click to rename)`
      : `${notebook.name}, ${notebook.view === VIEWS.FILE ? "shown as a file" : "shown as cells"} — `
        + `${notebook.cells.length} cell${notebook.cells.length === 1 ? "" : "s"} (double-click to rename)`;
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

function insertCellAt(index, type, content = "", style = "") {
  const cell = { id: generateId(), type, content, style, output: "", error: false };
  cells.splice(index, 0, cell);
  saveState();
  renderCells();
  focusCell(cell.id);
}

function addCell(type, content = "", style = "") {
  insertCellAt(cells.length, type, content, style);
}

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

function destroyCellEditors(cell) {
  cell.editor?.destroy();
  cell.cssEditor?.destroy();
}

async function loadExampleCells() {
  if (cells.length && !confirm("Replace the current cells with the example? This can't be undone.")) return;
  cells.forEach(destroyCellEditors);
  setCells(EXAMPLE_CELLS.map((c) => ({ id: generateId(), type: c.type, content: c.content, style: c.style || "", output: "", error: false })));
  saveState();
  renderCells();
  updateStatus("Example loaded — running it now…");
  await runAllCells();
}

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

function deleteCell(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  destroyCellEditors(cells[idx]);
  cells.splice(idx, 1);
  saveState();
  renderCells();
  updateStatus("Cell deleted.");
}

function duplicateCell(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const original = cells[idx];
  const copy = {
    id: generateId(),
    type: original.type,
    content: original.content,
    style: original.style || "",
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

function focusNextCellAfter(id) {
  const index = cells.findIndex((c) => c.id === id);
  if (index === -1 || index === cells.length - 1) return;
  focusCell(cells[index + 1].id);
}

function escapeHtml(text) {
  // Quotes too, not just angle brackets: renderDocInline() below places
  // escaped text inside double-quoted attributes (an image's alt/src), so
  // a raw " in, say, an imported notebook's markdown could otherwise
  // close the attribute early and smuggle in an attribute of its own.
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function iconButton(cssClass, icon, label, title) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = `dm-icon-btn ${cssClass}`;
  if (title) btn.title = title;
  btn.innerHTML =
    `<span class="dl-btn-icon" aria-hidden="true">${icon}</span>`
    + `<span class="dl-btn-label">${escapeHtml(label)}</span>`;
  return btn;
}

function getBtnLabel(btn) {
  return (btn.querySelector(".dl-btn-label") || btn).textContent;
}
function setBtnLabel(btn, text) {
  (btn.querySelector(".dl-btn-label") || btn).textContent = text;
}

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

function renderDocMathSpan(item) {
  const classes = item.display ? "dl-math dl-math-display" : "dl-math";
  return `<span class="${classes}">${escapeHtml(item.tex)}</span>`;
}

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
// assets/tutorial-runtime.js's own renderMaths(),
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
async function openWorkspaceFile(name) {
  const lower = name.toLowerCase();
  const isPy = lower.endsWith(".py");
  const isIpynb = lower.endsWith(".ipynb");
  const isHtml = lower.endsWith(".html") || lower.endsWith(".htm");
  if (!isPy && !isIpynb && !isHtml) {
    updateStatus(`dewmini opens .py, .ipynb and .html files. ${name} stays in the workspace for a cell to read.`, "error");
    return;
  }

  const already = notebooks.find((nb) => nb.path === name);
  if (already) { showNotebook(already.id); return; }

  if (isHtml) { await openSiteFile(name); return; }

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

async function readFileIfExists(name) {
  try {
    return await dfs.readFile(name, "utf8");
  } catch {
    return "";
  }
}

async function openSiteFile(name) {
  let html;
  try {
    html = await dfs.readFile(name, "utf8");
  } catch (err) {
    updateStatus(`Couldn't open ${name}: ${err.message}`, "error");
    return;
  }

  const base = name.replace(/\.html?$/i, "");
  const cssPath = `${base}.css`;
  const jsPath = `${base}.js`;
  const [css, js] = await Promise.all([readFileIfExists(cssPath), readFileIfExists(jsPath)]);

  const notebook = makeNotebook(notebookNameFor(name), [], VIEWS.SITE);
  notebook.path = name;
  notebook.siteCssPath = cssPath;
  notebook.siteJsPath = jsPath;
  notebook.siteHtml = html;
  notebook.siteCss = css;
  notebook.siteJs = js;
  openNotebook(notebook);
  updateViewSwitch();
  updateStatus(`Opened ${name}. Edits here save back to the workspace.`, "ok");
}

let workspaceWriteTimer = null;
function scheduleWorkspaceWrite(notebook) {
  if (!notebook?.path) return;
  clearTimeout(workspaceWriteTimer);
  workspaceWriteTimer = setTimeout(() => writeNotebookToWorkspace(notebook), 600);
}

async function writeNotebookToWorkspace(notebook) {
  if (!notebook?.path) return;
  if (notebook.view === VIEWS.SITE) { await writeSiteToWorkspace(notebook); return; }
  const text = notebook.path.toLowerCase().endsWith(".ipynb")
    ? JSON.stringify(cellsToIpynb(notebook.cells), null, 2)
    : cellsToPercentText(notebook.cells, { bare: true });
  try {
    await dfs.writeFile(notebook.path, text);
  } catch (err) {
    updateStatus(`Couldn't save ${notebook.path}: ${err.message}`, "error");
    return;
  }
  renderFileList();
}

async function writeSiteToWorkspace(notebook) {
  try {
    await dfs.writeFile(notebook.path, notebook.siteHtml || "");
    if ((notebook.siteCss || "").trim()) await dfs.writeFile(notebook.siteCssPath, notebook.siteCss);
    if ((notebook.siteJs || "").trim()) await dfs.writeFile(notebook.siteJsPath, notebook.siteJs);
  } catch (err) {
    updateStatus(`Couldn't save ${notebook.path}: ${err.message}`, "error");
    return;
  }
  renderFileList();
}

function currentView() {
  const view = activeNotebook()?.view;
  return view === VIEWS.FILE ? VIEWS.FILE : view === VIEWS.SITE ? VIEWS.SITE : VIEWS.CELLS;
}

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

function commitFileText(text) {
  clearTimeout(fileParseTimer);
  fileParseTimer = null;
  setCells(mergeParsedCells(cells, parsePyCells(text)));
  saveState();
}

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

function updateViewSwitch() {
  const view = currentView();
  const cellsBtn = document.getElementById("dm-view-cells");
  const fileBtn = document.getElementById("dm-view-file");
  cellsBtn?.setAttribute("aria-pressed", String(view === VIEWS.CELLS));
  fileBtn?.setAttribute("aria-pressed", String(view === VIEWS.FILE));
  cellsBtn?.classList.toggle("dm-viewswitch-on", view === VIEWS.CELLS);
  fileBtn?.classList.toggle("dm-viewswitch-on", view === VIEWS.FILE);
  document.querySelectorAll(".dm-cellview-only").forEach((el) => { el.hidden = view === VIEWS.SITE; });
}

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

  fileEditor = createCodeEditor(editorEl, cellsToPercentText(cells, { bare: true }), {
    dark: isDarkNow(),
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

function renderSiteView() {
  const notebook = activeNotebook();
  const wrap = document.createElement("div");
  wrap.className = "dm-siteview";

  const note = document.createElement("p");
  note.className = "dm-siteview-note";
  note.textContent = `This site is ${notebook.path}`
    + (notebook.siteCssPath ? `, ${notebook.siteCssPath}` : "")
    + (notebook.siteJsPath ? ` and ${notebook.siteJsPath}` : "")
    + ". The preview updates as you type HTML and CSS. The JavaScript runs when you press Run.";
  wrap.appendChild(note);

  const split = document.createElement("div");
  split.className = "dm-siteview-split";
  wrap.appendChild(split);

  const editors = document.createElement("div");
  editors.className = "dm-siteview-editors";
  split.appendChild(editors);

  const previewCol = document.createElement("div");
  previewCol.className = "dm-siteview-preview";
  split.appendChild(previewCol);

  const iframe = document.createElement("iframe");
  iframe.className = "dm-siteview-frame";
  iframe.setAttribute("sandbox", "allow-scripts");
  iframe.title = `${notebook.name}'s rendered page`;
  previewCol.appendChild(iframe);

  const consoleEl = document.createElement("div");
  consoleEl.className = "dm-siteview-console";
  const consoleLabel = document.createElement("div");
  consoleLabel.className = "dm-web-pane-label";
  consoleLabel.textContent = "Console";
  const consoleOut = document.createElement("div");
  consoleOut.className = "dm-siteview-console-output";
  consoleOut.setAttribute("aria-live", "polite");
  consoleEl.append(consoleLabel, consoleOut);
  previewCol.appendChild(consoleEl);

  // The relay, the document assembly, and the in-flight-coalescing flush
  // all live in assets/site-relay.js now, shared with the tutorial-page
  // site editor — this closure only draws the
  // console and wires Run to it.
  const preview = mountSitePreview(iframe, {
    onReset: () => { consoleOut.textContent = ""; },
    onConsole: (level, text) => {
      const line = document.createElement("div");
      line.className = `dm-siteview-console-line dl-stdout dm-siteview-console-${level}`;
      line.textContent = text;
      consoleOut.appendChild(line);
    },
    onError: ({ message, where, hint }) => {
      const line = document.createElement("div");
      line.className = "dm-siteview-console-line dl-error";
      const text = document.createElement("span");
      text.textContent = where ? `${message} (${where.label}, line ${where.line})` : message;
      line.appendChild(text);
      if (where && siteEditors && siteEditors[where.lang]) {
        const go = document.createElement("button");
        go.type = "button";
        go.className = "dm-siteview-goto";
        go.textContent = "Go to line";
        go.addEventListener("click", () => selectEditorLine(siteEditors[where.lang], where.line));
        line.appendChild(go);
      }
      consoleOut.appendChild(line);
      if (hint) {
        const hintEl = document.createElement("div");
        hintEl.className = "dl-error-hint";
        hintEl.textContent = hint;
        consoleOut.appendChild(hintEl);
      }
    },
  });

  // Combines the three editors' own live text, not a fresh disk read —
  // the same choice the Web cell's own preview makes, so typing shows up
  // straight away rather than waiting on the debounced write to land.
  const render = () => preview.render(notebook.siteHtml, notebook.siteCss);
  const run = () => preview.run(notebook.siteHtml, notebook.siteCss, notebook.siteJs);

  const pane = (label, content, language, onChange, { live = true } = {}) => {
    const paneEl = document.createElement("div");
    paneEl.className = "dm-siteview-pane";
    const head = document.createElement("div");
    head.className = "dm-siteview-pane-head";
    const labelEl = document.createElement("div");
    labelEl.className = "dm-web-pane-label";
    labelEl.textContent = label;
    head.appendChild(labelEl);
    if (!live) {
      const runBtn = document.createElement("button");
      runBtn.type = "button";
      runBtn.className = "dm-icon-btn dm-icon-render dm-siteview-run";
      runBtn.textContent = "Run";
      runBtn.title = "Run this script (Ctrl+Enter or Cmd+Enter in the pane)";
      runBtn.addEventListener("mousedown", (e) => e.preventDefault());
      runBtn.addEventListener("click", run);
      head.appendChild(runBtn);
    }
    const editorEl = document.createElement("div");
    editorEl.className = "dm-editor";
    paneEl.append(head, editorEl);
    editors.appendChild(paneEl);
    if (!live) {
      // Capture phase, ahead of CodeMirror's own Enter — the same shape
      // a Python cell's editor uses for its Ctrl/Cmd+Enter.
      editorEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          e.stopPropagation();
          run();
        }
      }, true);
    }
    return createCodeEditor(editorEl, content, {
      dark: isDarkNow(), language,
      onChange: (text) => { onChange(text); saveState(); if (live) render(); },
    });
  };

  siteEditors = {
    html: pane("HTML", notebook.siteHtml, "html", (text) => { notebook.siteHtml = text; }),
    css: pane("CSS", notebook.siteCss, "css", (text) => { notebook.siteCss = text; }),
    js: pane("JavaScript", notebook.siteJs, "javascript", (text) => { notebook.siteJs = text; }, { live: false }),
    _preview: preview,
  };

  cellsContainer.appendChild(wrap);
  // run(), not render(): a reopened site should show its JavaScript as
  // already having run once, the same as before this view's engine moved
  // into assets/site-relay.js — mountSitePreview() starts with no
  // remembered script, and render() alone would leave the initial paint
  // showing HTML/CSS against a blank one.
  run();
}

/* Selects one whole line (1-based) of a CodeMirror editor and scrolls to
 * it: the console's Go to line. */
function selectEditorLine(editor, n) {
  const { view } = editor;
  const line = view.state.doc.line(Math.max(1, Math.min(n, view.state.doc.lines)));
  view.dispatch({ selection: { anchor: line.from, head: line.to }, scrollIntoView: true });
  view.focus();
}

function destroySiteEditors() {
  if (!siteEditors) return;
  siteEditors._preview?.destroy();
  siteEditors.html?.destroy();
  siteEditors.css?.destroy();
  siteEditors.js?.destroy();
  siteEditors = null;
}

function renderCells() {
  if (!cellsContainer) return;
  destroyFileEditor();
  destroySiteEditors();
  cellsContainer.innerHTML = "";
  if (emptyEl) emptyEl.hidden = true;
  if (currentView() === VIEWS.FILE) { renderFileView(); return; }
  if (currentView() === VIEWS.SITE) { renderSiteView(); return; }
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

  actions.append(addPy, addTxt);

  // Web, SQL and JavaScript only offer themselves here once their own
  // Settings → "Cell types" toggle is on (CELL_TYPE_TOGGLES) — Web and
  // SQL start off, JavaScript starts on.
  if (enabledCellTypes.has(CELL_TYPES.WEB)) {
    const addWeb = document.createElement("button");
    addWeb.type = "button";
    addWeb.className = "dm-insert-btn";
    addWeb.title = "Insert an HTML+CSS cell here";
    addWeb.innerHTML = '<span class="dm-tool-icon dm-tool-icon-html" aria-hidden="true"></span>Web';
    addWeb.addEventListener("click", () => insertCellAt(index, CELL_TYPES.WEB));
    actions.append(addWeb);
  }

  if (enabledCellTypes.has(CELL_TYPES.SQL)) {
    const addSql = document.createElement("button");
    addSql.type = "button";
    addSql.className = "dm-insert-btn";
    addSql.title = "Insert a SQL cell here";
    addSql.innerHTML = '<span class="dm-tool-icon dm-tool-icon-sql" aria-hidden="true"></span>SQL';
    addSql.addEventListener("click", () => insertCellAt(index, CELL_TYPES.SQL));
    actions.append(addSql);
  }

  if (enabledCellTypes.has(CELL_TYPES.JAVASCRIPT)) {
    const addJs = document.createElement("button");
    addJs.type = "button";
    addJs.className = "dm-insert-btn";
    addJs.title = "Insert a JavaScript cell here";
    addJs.innerHTML = '<span class="dm-tool-icon dm-tool-icon-js" aria-hidden="true"></span>JS';
    addJs.addEventListener("click", () => insertCellAt(index, CELL_TYPES.JAVASCRIPT));
    actions.append(addJs);
  }

  row.append(line, actions);
  return row;
}

function isStale(cell) {
  return RUNS_AGAINST_SESSION.has(cell.type) && cell.ranContent !== undefined && cell.ranContent !== cell.content;
}

function updateCellChrome(id) {
  const el = cellsContainer?.querySelector(`.dm-cell[data-id="${id}"]`);
  const cell = cells.find((c) => c.id === id);
  if (!el || !cell) return;
  el.classList.toggle("dm-error", !!cell.error);
  renderCellRunLine(cell);
}

function createRunMoreMenu(cell) {
  const wrap = document.createElement("div");
  wrap.className = "dm-cell-more";

  const moreBtn = iconButton("dm-icon-more", "&#8943;", "More", "More ways to run this cell");
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
    menu.classList.remove("dm-cell-run-menu-left");
    menu.hidden = false;
    // Anchored from the button's right edge by default (see the
    // stylesheet), which runs the menu off the left of the viewport once
    // the button sits close enough to it — reachable more often now that
    // Workbench docks left, but always possible
    // on a narrow screen. Measured after becoming visible, since a
    // hidden element's rect is always zero.
    if (menu.getBoundingClientRect().left < 0) menu.classList.add("dm-cell-run-menu-left");
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

function resetRunSequence() {
  runSequenceCounter = 0;
  for (const cell of cells) {
    delete cell.ranOrder;
    delete cell.ranContent;
    delete cell.lastRunMs;
    renderCellRunLine(cell);
  }
}

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

function setRunLineQueued(cell) {
  if (!cell.runLineEl) return;
  clearRunLineTicker(cell);
  cell.runLineEl.classList.remove("dm-cell-runline-notrun", "dm-cell-runline-stale");
  cell.runLineEl.classList.add("dm-cell-runline-queued");
  cell.runLineEl.textContent = "Running next";
}

function createCellElement(cell) {
  const wrap = document.createElement("div");
  wrap.className = `dm-cell dm-cell-${cell.type}`;
  wrap.dataset.id = cell.id;
  if (cell.error) wrap.classList.add("dm-error");

  const rail = document.createElement("div");
  rail.className = "dm-cell-rail";

  const main = document.createElement("div");
  main.className = "dm-cell-main";

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
    [CELL_TYPES.WEB]: "HTML/CSS", [CELL_TYPES.SQL]: "SQL",
    [CELL_TYPES.JAVASCRIPT]: "JavaScript",
  };
  pill.innerHTML =
    '<span class="dm-cell-pill-dots" aria-hidden="true">&#8942;</span>' +
    `<span class="dm-cell-pill-num">Cell ${cellNumber}</span>` +
    `<span class="dm-cell-pill-type" data-type="${cell.type}">${PILL_LABELS[cell.type]}</span>`;

  // A reader's own name for this cell, beside the pill rather than
  // replacing it — the pill still says where the cell sits, this is just
  // "a handle to hold on to" when talking about it later
  // (planning/CELL_IDENTITY.md §4). A plain text input, not
  // contenteditable: predictable focus/selection/paste behaviour matters
  // more here than matching a <span>'s box exactly, and dm-cell-name's
  // own rule below strips an input's usual chrome so it still reads as
  // text sitting on the header, not as a form field. Shares dl-cell-name
  // with a tutorial page's own (there, static) name span, so
  // tutorial-style.css's colour/size/ellipsis rule needs no dewmini copy.
  const nameEl = document.createElement("input");
  nameEl.type = "text";
  nameEl.className = "dm-cell-name dl-cell-name";
  nameEl.placeholder = "+ name";
  nameEl.value = cell.name || "";
  nameEl.setAttribute("aria-label", "This cell's own name, if you give it one");
  nameEl.addEventListener("mousedown", (e) => e.stopPropagation());
  nameEl.addEventListener("click", (e) => e.stopPropagation());
  nameEl.addEventListener("input", () => {
    cell.name = nameEl.value.trim() || undefined;
    saveState();
  });

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
    previewBtn = iconButton("dm-icon-preview", "&#128065;", "View");
    headerEnd.appendChild(previewBtn);
  }
  // A web cell's own explicit render trigger —
  // filled in by that branch below, same "built here so it sits in the
  // header row regardless of where the branch runs" reasoning as
  // insertDocImage above, since it needs closures that only exist there.
  let renderBtn = null;
  if (cell.type === CELL_TYPES.WEB) {
    renderBtn = iconButton(
      "dm-icon-render", "&#9655;", "Render",
      "Render this cell's HTML and CSS together",
    );
    headerEnd.appendChild(renderBtn);
  }
  // Attaching an image from disk only makes sense for a Text cell's own
  // markdown-image syntax — an HTML cell's reader can already write an
  // <img> tag directly, so this stays Text-only.
  if (cell.type === CELL_TYPES.TEXT) {
    const imgBtn = iconButton(
      "dm-icon-image", '<span class="dm-tool-icon dm-tool-icon-image" aria-hidden="true"></span>', "Image",
      "Attach an image from your device",
    );
    imgBtn.addEventListener("click", (e) => { e.stopPropagation(); insertDocImage?.(); });
    headerEnd.appendChild(imgBtn);
  }

  const dupBtn = iconButton("dm-icon-duplicate", "&#10697;", "Duplicate", "Duplicate this cell");
  dupBtn.addEventListener("click", (e) => { e.stopPropagation(); duplicateCell(cell.id); });
  headerEnd.appendChild(dupBtn);

  // Arm-then-confirm rather than a native confirm() dialog: a dialog
  // stops the whole page and needs a mouse trip to its own button,
  // where this just needs a second, deliberate press of the same one.
  const delBtn = iconButton("dm-icon-delete", "&#215;", "Delete", "Delete this cell");
  delBtn.addEventListener("click", (e) => { e.stopPropagation(); armDeleteButton(delBtn, () => deleteCell(cell.id)); });
  headerEnd.appendChild(delBtn);

  head.append(pill, nameEl, spacer, headerEnd);

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

    const previewIcon = previewBtn.querySelector(".dl-btn-icon");
    const syncPreviewBtn = () => {
      const editing = !textarea.hidden;
      previewIcon.innerHTML = editing ? "&#128065;" : "&#9998;";
      setBtnLabel(previewBtn, editing ? "View" : "Edit");
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
  } else if (cell.type === CELL_TYPES.WEB) {
    // The merged replacement for the old separate HTML and CSS cell
    // types — one cell, two source panels,
    // stacked, and a rendered preview below both. Unlike the types it
    // replaces, both editors are always visible and always editable —
    // nothing is ever swapped out for anything else — so there is no
    // Edit/View toggle here despite the shared quiet-until-touched
    // chrome (`.dm-cell-web` sits in that CSS rule alongside
    // `.dm-cell-text`). Rendering is instead the header's own explicit
    // Render button (renderBtn, built above): two editors both
    // auto-rendering on their own focusout, the way HTML and CSS used to
    // separately, would fire the same preview update twice for one edit,
    // and would mean a reader tabbing from one editor into the other
    // sees a half-finished render flash by in between.
    const split = document.createElement("div");
    split.className = "dm-web-split";

    const htmlLabel = document.createElement("div");
    htmlLabel.className = "dm-web-pane-label";
    htmlLabel.textContent = "HTML";
    const htmlEditorEl = document.createElement("div");
    htmlEditorEl.className = "dm-editor";

    const cssLabel = document.createElement("div");
    cssLabel.className = "dm-web-pane-label";
    cssLabel.textContent = "CSS";
    const cssEditorEl = document.createElement("div");
    cssEditorEl.className = "dm-editor";

    split.append(htmlLabel, htmlEditorEl, cssLabel, cssEditorEl);
    contentRegion.appendChild(split);

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
    iframe.title = `Cell ${cellNumber}'s rendered page`;
    renderEl.appendChild(iframe);

    // An empty HTML half falls back to CSS_PREVIEW_MARKUP — the same
    // fixed little "page" the old standalone CSS cell always rendered
    // against — so a reader who has only written a rule still has
    // something real to see it styling, before they've written any
    // markup of their own.
    const render = () => {
      const html = cell.content.trim() ? cell.content : CSS_PREVIEW_MARKUP;
      iframe.srcdoc = `<style>${cell.style}</style>${html}`;
      renderEl.hidden = false;
    };

    const htmlEditor = createCodeEditor(htmlEditorEl, cell.content, {
      dark: isDarkNow(),
      language: "html",
      onChange: (text) => { cell.content = text; saveState(); },
    });
    const cssEditor = createCodeEditor(cssEditorEl, cell.style, {
      dark: isDarkNow(),
      language: "css",
      onChange: (text) => { cell.style = text; saveState(); },
    });
    cell.editor = htmlEditor;
    cell.cssEditor = cssEditor;

    renderBtn.addEventListener("mousedown", (e) => e.preventDefault());
    renderBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      render();
    });

    // A brand-new cell shows no preview at all until the reader actually
    // asks for one — only a cell restored with existing content (from a
    // save, or a migrated old HTML/CSS cell) renders straight away, the
    // same "picks up where it left off" behaviour the types it replaces
    // already had.
    if (cell.content.trim() || cell.style.trim()) render();
  } else if (cell.type === CELL_TYPES.SQL) {
    // Python-shaped, not HTML/CSS-shaped: a SQL cell runs against the
    // same shared session a Python cell does (RUNS_AGAINST_SESSION), so
    // its editor is the only thing in contentRegion — no rendered/editor
    // toggle, no sandboxed preview, because there is nothing to preview
    // until it actually runs. executeCell() below is what turns this
    // cell's raw SQL into the tutorial_tools._run_sql_cell() call that
    // actually executes it.
    const editorEl = document.createElement("div");
    editorEl.className = "dm-editor";
    contentRegion.appendChild(editorEl);

    const editor = createCodeEditor(editorEl, cell.content, {
      dark: isDarkNow(),
      language: "sql",
      onChange: (text) => {
        cell.content = text;
        saveState();
        updateCellChrome(cell.id);
      },
    });
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
  } else if (cell.type === CELL_TYPES.JAVASCRIPT) {
    // Same shape as SQL just above — Python-shaped chrome, a bare
    // editor, nothing to preview until it runs — with the language mode
    // the only real difference. Unlike SQL, a JavaScript cell's own code
    // needs no wrapping before it runs: executeCell() hands it to
    // ./js-cell-engine.js's runCell() exactly as written.
    const editorEl = document.createElement("div");
    editorEl.className = "dm-editor";
    contentRegion.appendChild(editorEl);

    const editor = createCodeEditor(editorEl, cell.content, {
      dark: isDarkNow(),
      language: "javascript",
      onChange: (text) => {
        cell.content = text;
        saveState();
        updateCellChrome(cell.id);
      },
    });
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
  }

  setCollapsed(!!cell.collapsed);

  //
  // Run, clear-output, the "⋯" run-above/below menu, and the run-line —
  // RUNS_AGAINST_SESSION only (Python and SQL), since those are the only
  // cells that run against the shared session. Sits between the code and
  // the output, at the bottom-left of the cell: a reader's cursor is at
  // the bottom of what they just wrote, not back up at the top, so
  // that's where the next action should be waiting.

  let footbar = null;
  if (RUNS_AGAINST_SESSION.has(cell.type)) {
    footbar = document.createElement("div");
    footbar.className = "dm-cell-footbar";

    const runBtn = iconButton("dm-icon-run", "&#9654;", "Run", "Run this cell (Shift+Enter)");
    runBtn.addEventListener("click", (e) => { e.stopPropagation(); runCell(cell.id); });
    footbar.appendChild(runBtn);
    cell.runBtn = runBtn;

    // Clears this cell's own output without touching its code — the
    // non-destructive counterpart to Delete.
    // &#8634; (↺, counterclockwise) — deliberately not build.py's own
    // &#8635; (↻, clockwise) for its destructive "reset to starter"
    // button: a different-looking icon for a materially different action
    // (planning/CELL_IDENTITY.md §1), not a coincidence of two similar
    // buttons drifting to the same glyph.
    const resetOutputBtn = iconButton("dm-icon-reset-output", "&#8634;", "Clear", "Clear this cell's output");
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

function isDarkNow() {
  const t = document.documentElement.getAttribute("data-theme");
  if (t === "dark") return true;
  if (t === "light") return false;
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

async function getToolsSource() {
  if (toolsSourceCache) return toolsSourceCache;
  const res = await fetch("../assets/tutorial_tools.py");
  if (!res.ok) throw new Error(`tutorial_tools.py: HTTP ${res.status}`);
  toolsSourceCache = await res.text();
  return toolsSourceCache;
}

engine.configure({
  getOutputEl: (cellId) => (cellId === FILE_RUN_ID
    ? fileRunOutputEl
    : cells.find((c) => c.id === cellId)?.outputEl ?? null),
  onStatus: updateStatus,
  packages: DM_PACKAGES,
  dataBase: "../data/",
});

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

async function ensureJsSession() {
  const alreadyReady = jsEngine.sessionReady();
  await jsEngine.ensureSession();
  if (!alreadyReady) {
    updateStatus("JavaScript ready.", "ok");
    // Settings' own execution-status line only mentions the JS session
    // once sessionReady() is true (see updateExecutionStatus() below) —
    // ensurePyodide() already re-paints that line itself on every boot;
    // this is the JS-session equivalent, needed here too or the line
    // would sit stale until something Python-related happened to touch it.
    updateExecutionStatus();
  }
}

async function ensureSessionFor(cell) {
  if (cell.type === CELL_TYPES.JAVASCRIPT) { await ensureJsSession(); return; }
  await ensurePyodide();
}

function canStopFor(cell) {
  return cell.type === CELL_TYPES.JAVASCRIPT ? jsEngine.canStop() : engine.canStop();
}

function requestInterruptFor(cell) {
  if (cell.type === CELL_TYPES.JAVASCRIPT) jsEngine.requestInterrupt();
  else engine.requestInterrupt();
}

function buildSqlCellCode(sql) {
  return `import tutorial_tools as _dm_tt\n_ = _dm_tt._run_sql_cell(db, ${JSON.stringify(sql)})`;
}

async function executeCell(cell) {
  const outputEl = cell.outputEl;
  if (!outputEl) return true;
  outputEl.classList.remove("dm-empty");
  const startedAt = performance.now();
  // Captured before the run, not after: the whole point of the run-line's
  // "edited since" flag is "does this output belong to what the cell says
  // right now", so this has to be the content that was actually handed to
  // the engine, even in the unusual case where an editor kept accepting
  // keystrokes while a slow cell was still running.
  cell.ranContent = cell.content;
  let ok;
  // A reader's own name for this cell, if they gave it one, otherwise its
  // plain position — either way, a traceback's file line then names
  // something a reader chose or can already see, never this cell's own
  // opaque internal id (planning/CELL_IDENTITY.md).
  const label = cell.name || `Cell ${cells.indexOf(cell) + 1}`;
  if (cell.type === CELL_TYPES.JAVASCRIPT) {
    ({ ok } = await jsEngine.runCell(cell.id, cell.content));
  } else {
    const code = cell.type === CELL_TYPES.SQL ? buildSqlCellCode(cell.content) : cell.content;
    ({ ok } = await engine.runCell(cell.id, code, label));
  }
  cell.lastRunMs = performance.now() - startedAt;
  cell.ranOrder = ++runSequenceCounter;
  cell.output = outputEl.innerHTML;
  cell.error = !ok;
  allowOutputToSaveAgain(cell.id);
  if (!outputEl.innerHTML.trim()) outputEl.classList.add("dm-empty");
  updateCellChrome(cell.id);
  saveState();
  // Neither is meaningful for a JavaScript cell: its own sandboxed
  // session has no mounted filesystem to sync, and refreshVariables()
  // reads Pyodide's own namespace, which a JS cell's run never touches.
  if (cell.type !== CELL_TYPES.JAVASCRIPT) {
    // Fire-and-forget: a cell's own code may have written straight to
    // the mounted filesystem (dfs.sync()'s own docstring explains why
    // that needs this rather than relying on writeFile()'s debounced
    // sync or the best-effort unload flush alone) — not awaited, so a
    // slow sync never makes a fast cell feel slower than it is.
    dfs.sync()
      // A cell that wrote a file is exactly when the Files list is
      // wrong, and nothing else was redrawing it: a student could write
      // shapes.py, open Files, and not see it until some unrelated
      // thing refreshed the panel.
      .then(() => renderFileList())
      .catch((err) => console.warn("dewmini: filesystem sync after cell run failed", err));
    // Same treatment for the Workbench's variable list: a run is
    // exactly when the namespace changed, so this is when it needs
    // redrawing — but it is a panel a reader may not even have open,
    // and never worth making a cell feel slower for.
    refreshVariables().catch((err) => console.warn("dewmini: refreshing variables failed", err));
  }
  return ok;
}

/* Formats how long a cell's last run took, human-scale rather than raw
 * milliseconds: "340 ms" under a second, "2.4 s" at or above it. */
function formatRunDuration(ms) {
  return ms < 1000 ? `${Math.round(ms)} ms` : `${(ms / 1000).toFixed(1)} s`;
}

function resetCellOutput(id) {
  const cell = cells.find((c) => c.id === id);
  if (!cell || !RUNS_AGAINST_SESSION.has(cell.type) || running) return;
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

function clearAllOutputs() {
  cells.forEach((cell) => { if (RUNS_AGAINST_SESSION.has(cell.type)) resetCellOutput(cell.id); });
  updateStatus("Output cleared.");
}

function setRunButtonRunning(runBtn, canStop) {
  if (!runBtn) return;
  const icon = runBtn.querySelector(".dl-btn-icon");
  if (canStop) {
    runBtn.disabled = false;
    if (icon) icon.innerHTML = "&#9632;";
    setBtnLabel(runBtn, "Stop");
    runBtn.title = "Stop this cell";
    runBtn.classList.add("dm-icon-run-stop");
  } else {
    runBtn.disabled = true;
    setBtnLabel(runBtn, "…");
    runBtn.title = "Running…";
  }
}

/* Restores a cell's Run button once it finishes (or fails to) run. */
function resetRunButton(runBtn) {
  if (!runBtn) return;
  runBtn.disabled = false;
  runBtn.classList.remove("dm-icon-run-stop");
  runBtn.title = "Run this cell (Shift+Enter)";
  const icon = runBtn.querySelector(".dl-btn-icon");
  if (icon) icon.innerHTML = "&#9654;";
  setBtnLabel(runBtn, "Run");
}

async function runCell(id) {
  const cell = cells.find((c) => c.id === id);
  if (!cell || !RUNS_AGAINST_SESSION.has(cell.type)) return;
  if (runningCellId === id) {
    requestInterruptFor(cell);
    return;
  }
  if (running) return;
  running = true;
  runningCellId = id;
  try {
    // Boot (or reconnect to an already-booted) session *before* deciding
    // what the Run button should look like — canStopFor(), which
    // setRunButtonRunning() reads, only knows worker-vs-main-thread once
    // ensureBooted() has actually resolved, so the await has to come
    // first, not only inside executeCell() below.
    // Skipping this step showed up as a real bug in testing: canStop()
    // read false (its pre-boot default) on every cell's first-ever run,
    // showing the *non-stoppable* "…" busy state even in worker mode.
    await ensureSessionFor(cell);
    // Meaningless for a JavaScript cell: changedImportedModules() reads
    // Pyodide's own module registry, which a JS cell's session never
    // touches.
    if (cell.type !== CELL_TYPES.JAVASCRIPT) await checkImportedFiles();
    setRunButtonRunning(cell.runBtn, canStopFor(cell));
    startRunLineTicker(cell);
    const ok = await executeCell(cell);
    updateStatus(ok ? "Ran." : "Error — see the cell.", ok ? "ok" : "error");
  } catch (err) {
    updateStatus(`Couldn't run this cell: ${err.message}`, "error");
  } finally {
    running = false;
    runningCellId = null;
    resetRunButton(cell.runBtn);
    clearRunLineTicker(cell);
  }
}

async function runCellBatch(runnableCells, { reset, emptyMessage, describe }) {
  if (running) return;
  if (!runnableCells.length) { updateStatus(emptyMessage); return; }

  running = true;
  const btn = document.getElementById("run-all");
  if (btn) btn.disabled = true;

  try {
    // Skipped for a batch that is entirely JavaScript: forcing a Pyodide
    // boot (and a round trip only Python/SQL cells could ever answer)
    // for a batch that will never touch it is wasted work.
    if (runnableCells.some((c) => c.type !== CELL_TYPES.JAVASCRIPT)) {
      await ensurePyodide();
      // Once for the whole batch, not once per cell: the answer would be
      // the same every time and each ask is a round trip.
      await checkImportedFiles();
    }
    if (reset) {
      // resetPageState() itself assumes Pyodide has already booted at
      // least once, so that has to come first — unconditionally, even
      // if the batch turns out to be all JavaScript cells, the same cost
      // this already paid before JavaScript cells existed.
      await ensurePyodide();
      await engine.resetPageState();
      jsEngine.restart();
      resetRunSequence();
    }
    updateStatus(describe(runnableCells.length));
    // Only ever the one cell right after whichever is about to run, kept
    // current as the batch moves along below — not the whole remaining
    // list marked "next" at once.
    if (runnableCells[1]) setRunLineQueued(runnableCells[1]);

    let errors = 0;
    for (let i = 0; i < runnableCells.length; i++) {
      const cell = runnableCells[i];
      runningCellId = cell.id;
      await ensureSessionFor(cell);
      setRunButtonRunning(cell.runBtn, canStopFor(cell));
      startRunLineTicker(cell);
      try {
        const ok = await executeCell(cell);
        if (!ok) errors += 1;
      } finally {
        resetRunButton(cell.runBtn);
        clearRunLineTicker(cell);
      }
      const next = runnableCells[i + 1];
      if (next) setRunLineQueued(next);
    }
    updateStatus(
      errors ? `Done — ${errors} cell${errors === 1 ? "" : "s"} errored.` : "All cells ran cleanly.",
      errors ? "error" : "ok"
    );
  } catch (err) {
    updateStatus(`Couldn't run these cells: ${err.message}`, "error");
  } finally {
    running = false;
    runningCellId = null;
    if (btn) btn.disabled = false;
  }
}

/* Runs every cell that runs against the session, in order, top to bottom
 * — "Run all." */
async function runAllCells() {
  // In the file view there are no cells on screen to run one at a time,
  // and the file runs top to bottom as one thing.
  if (currentView() === VIEWS.FILE) { await runWholeFile(); return; }
  await runCellBatch(cells.filter((c) => RUNS_AGAINST_SESSION.has(c.type)), {
    reset: true,
    emptyMessage: "No cells to run.",
    describe: (n) => `Running ${n} cell${n === 1 ? "" : "s"}…`,
  });
}

async function runAbove(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const slice = cells.slice(0, idx + 1).filter((c) => RUNS_AGAINST_SESSION.has(c.type));
  await runCellBatch(slice, {
    reset: true,
    emptyMessage: "No cells above this one to run.",
    describe: (n) => `Running the ${n} cell${n === 1 ? "" : "s"} above and including this one…`,
  });
}

async function runBelow(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const slice = cells.slice(idx).filter((c) => RUNS_AGAINST_SESSION.has(c.type));
  await runCellBatch(slice, {
    reset: false,
    emptyMessage: "No cells here or below to run.",
    describe: (n) => `Running the ${n} cell${n === 1 ? "" : "s"} from here on…`,
  });
}

// Module names currently shown in the notice, so its button knows what to
// re-read without asking Python a second time.
let staleImportNames = [];

async function checkImportedFiles() {
  if (!dfs.getBackend()) return;
  const changed = await engine.changedImportedModules(dfs.mountPoint());
  if (changed.length) showStaleImportsNotice(changed);
}

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

function getFilenameBase() {
  let name = (activeNotebook()?.name || "").trim();
  if (!name) name = "dewmini-notebook";
  name = name.replace(/\.(py|html?|ipynb)$/i, "");
  name = name.replace(/[\\/:*?"<>|]+/g, "-").trim();
  return name || "dewmini-notebook";
}

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

function cellExportContent(cell) {
  if (cell.type !== CELL_TYPES.WEB) return cell.content;
  if (!cell.style.trim()) return cell.content;
  return `${cell.content}\n\n<style>\n${cell.style}\n</style>`;
}

const PY_CELL_MARKER = "# %%";
const PY_TEXT_MARKER = "# %% [markdown]";
// The first line of the header block below. parsePyCells() matches this
// exact opening to tell dewmini's own header from a leading comment a
// file written elsewhere came with — a licence notice, say, which must
// be kept. Change one and change the other.
const PY_HEADER_OPENING = "# dewmini export";

function cellsToPercentText(cellList, { bare = false } = {}) {
  // A lone Python cell writes as a plain script, no `# %%` marker, when
  // `bare` is set. The marker exists to tell two or more cells apart; on a
  // single cell it marks nothing, and parsePyCells()'s own "no markers
  // found" fallback already reads a markerless block back as one Python
  // cell, so nothing is lost by leaving it off. Leaving it *on* was the
  // actual bug this guards against: a plain .py a reader's own
  // open(name, "w") wrote, or one they brought in from outside dewmini,
  // has no marker in it — the moment it was so much as opened in the file
  // view, let alone edited and saved, it silently grew one, turning an
  // ordinary script into something that looks like a notebook export the
  // reader never asked for.
  //
  // downloadAsPython() asks for the marked form instead: its header sits
  // above the first marker so isOwnHeader() can recognise and strip it on
  // reimport, and that only works when a marker exists to bound it.
  if (bare && cellList.length === 1 && cellList[0].type === CELL_TYPES.PYTHON) {
    return cellExportContent(cellList[0]);
  }
  const parts = [];
  cellList.forEach((cell) => {
    if (cell.type === CELL_TYPES.TEXT) {
      parts.push(PY_TEXT_MARKER);
      cell.content.split("\n").forEach((line) => parts.push(`# ${line}`.trimEnd()));
    } else {
      parts.push(PY_CELL_MARKER, cellExportContent(cell));
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

function splitLines(text) {
  const lines = text.split("\n");
  return lines.map((line, i) => (i < lines.length - 1 ? `${line}\n` : line));
}

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

function lonePngDataUrl(node) {
  const img = node.tagName === "IMG" ? node : node.querySelector("img");
  if (!img) return null;
  if (node !== img && (node.querySelectorAll("img").length !== 1 || node.textContent.trim())) return null;
  const match = /^data:image\/png;base64,(.+)$/.exec(img.getAttribute("src") || "");
  return match ? match[1] : null;
}

const IMPORTED_HTML_TAGS = new Set([
  "P", "DIV", "SPAN", "PRE", "CODE", "BR", "HR", "EM", "STRONG", "B", "I", "U", "SMALL", "SUB", "SUP",
  "UL", "OL", "LI", "DL", "DT", "DD", "BLOCKQUOTE",
  "TABLE", "THEAD", "TBODY", "TFOOT", "TR", "TH", "TD", "CAPTION", "COLGROUP", "COL",
  "H1", "H2", "H3", "H4", "H5", "H6", "IMG",
]);

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
      source: splitLines(cellExportContent(cell)),
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

async function downloadAsHtml() {
  flushFileEditor();
  if (!cells.length) { updateStatus("No cells to export.", "error"); return; }
  updateStatus("Building the standalone file…");
  try {
    const toolsSource = await getToolsSource();
    const cellsData = cells.map((c) => ({ id: c.id, type: c.type, content: c.content, style: c.style || "" }));
    const name = getFilenameBase();
    const html = buildStandaloneHtml(toolsSource, cellsData, isDarkNow(), name);
    triggerDownload(`${name}.html`, html, "text/html");
    updateStatus("Downloaded as standalone HTML.", "ok");
  } catch (err) {
    updateStatus(`Couldn't build the HTML export: ${err.message}`, "error");
  }
}

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
      body.textContent = cell.type === "web" && cell.style
        ? cell.content + "\\n\\n<style>\\n" + cell.style + "\\n</style>"
        : cell.content;
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

const REFERENCE_KINDS = [
  ["concept", "Concepts"],
  ["function", "Functions"],
  ["operator", "Operators"],
  ["formula", "Formulas"],
  ["keyword", "Keywords"],
];

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

const referenceFilters = {
  subjects: new Set(),
  level: new Set(),
  groups: new Set(),
  kind: new Set(),
};

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

const PRACTICE_INDEX_KEY = "dewmini:practice-index";
const PRACTICE_ORDER_KEY = "dewmini:practice-order";
const PRACTICE_SHUFFLE_KEY = "dewmini:practice-shuffle";
let practiceBank = null;

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

function shuffledRange(n) {
  const arr = Array.from({ length: n }, (_, i) => i);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

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

function showImportCompatNotice(warnings) {
  const notice = document.getElementById("import-compat-notice");
  const list = document.getElementById("import-compat-list");
  if (!notice || !list) return;
  if (!warnings.length) { notice.hidden = true; return; }
  const toHtml = (w) => `<li>${w.replace(/`([^`]+)`/g, "<code>$1</code>")}</li>`;
  list.innerHTML = warnings.map(toHtml).join("");
  notice.hidden = false;
}

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
    // A blank stretch with its own `# %%` marker (currentType set) is a
    // real cell the reader left empty, or just inserted — keep it, the
    // same as a cell with content. Only the implicit segment before the
    // first marker is dropped when blank, since nothing asked for a cell
    // to exist there; dropping every blank cell here is what silently
    // deleted an empty one on a Cells-to-File-and-back round trip.
    if (content.trim() || currentType !== null) cells.push({ id: generateId(), type, content, output: "", error: false });
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

function clearDropMarkers() {
  cellsContainer?.querySelectorAll(".dm-drop-before,.dm-drop-after").forEach((el) => el.classList.remove("dm-drop-before", "dm-drop-after"));
}

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

function updateStatus(message, kind = "") {
  if (!statusEl) return;
  const className = "dm-status" + (kind ? ` dm-status-${kind}` : "");
  if (statusEl.textContent === message) {
    statusEl.textContent = "";
    setTimeout(() => { statusEl.textContent = message; }, 0);
  } else {
    statusEl.textContent = message;
  }
  statusEl.className = className;
  clearTimeout(statusClearTimer);
  if (kind !== "error") {
    statusClearTimer = setTimeout(() => {
      if (statusEl.textContent === message) { statusEl.textContent = ""; statusEl.className = "dm-status"; }
    }, 3500);
  }
}

/* Human-sized file size — bytes, then one-decimal KB and MB. */
function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function updateExecutionStatus() {
  const el = document.getElementById("settings-execution-status");
  if (!el) return;
  const mode = engine.engineMode();
  let text;
  if (!mode) {
    text = "Not started yet — run a cell to start Python.";
  } else {
    const where = mode === "worker"
      ? "a background worker, so the page stays responsive"
      : "the main thread (no background worker available here) — a runaway cell will freeze the page until it finishes";
    const stop = engine.canStop()
      ? "Stop can genuinely interrupt a running cell."
      : "Stop can't interrupt a running cell in this mode.";
    text = `Running in ${where}. ${stop}`;
  }
  // Only once a reader has actually run a JavaScript cell — mentioning a
  // second session nobody has touched yet would just be noise.
  if (jsEngine.sessionReady()) {
    text += " JavaScript cells run in their own sandboxed frame, on the same main thread — Stop can't interrupt one either.";
  }
  el.textContent = text;
}

async function restartPython() {
  engine.restart();
  jsEngine.restart();
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

function renderNotebookList() {
  const listEl = document.getElementById("settings-notebook-list");
  if (!listEl) return;
  listEl.replaceChildren();

  for (const nb of notebooks) {
    if (nb.path) continue;
    const item = document.createElement("li");
    item.className = "dm-filelist-item";

    const nameEl = document.createElement("button");
    nameEl.type = "button";
    nameEl.className = "dm-filelist-item-name";
    nameEl.textContent = nb.name;
    nameEl.title = `Switch to ${nb.name}`;
    nameEl.addEventListener("click", () => showNotebook(nb.id));

    const badge = document.createElement("span");
    badge.className = "dm-filelist-item-size";
    badge.textContent = "notebook";

    item.append(nameEl, badge);
    listEl.append(item);
  }
}

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

async function newFsFile() {
  await ensurePyodide();
  const asked = prompt("Name for the new file:", "shapes.py");
  if (asked === null) return;
  let name = asked.trim();
  if (!name) return;
  if (name.includes("/")) { updateStatus("A name cannot contain a slash.", "error"); return; }
  if (!/\.(py|ipynb|html?)$/i.test(name)) name += ".py";

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

async function uploadFsFiles(fileList) {
  const files = fileList ? Array.from(fileList) : [];
  if (!files.length) return;

  try {
    await ensurePyodide();
  } catch (err) {
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
  // no reason a reader could see. The min/max
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

function setSegChecked(btn, checked) {
  btn.setAttribute("aria-checked", String(checked));
}

function syncSegRoving(group) {
  const buttons = [...group.querySelectorAll("button")];
  const checked = buttons.find((btn) => btn.getAttribute("aria-checked") === "true");
  for (const btn of buttons) btn.tabIndex = btn === (checked || buttons[0]) ? 0 : -1;
}

function initSegKeyboardNav() {
  for (const group of document.querySelectorAll(".dl-seg")) {
    group.addEventListener("keydown", (ev) => {
      const buttons = [...group.querySelectorAll("button:not(:disabled)")];
      const i = buttons.indexOf(document.activeElement);
      if (i === -1) return;
      let next;
      if (ev.key === "ArrowRight" || ev.key === "ArrowDown") next = buttons[(i + 1) % buttons.length];
      else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") next = buttons[(i - 1 + buttons.length) % buttons.length];
      else if (ev.key === "Home") next = buttons[0];
      else if (ev.key === "End") next = buttons[buttons.length - 1];
      else return;
      ev.preventDefault();
      next.click();
      next.focus();
    });
  }
}

const TEXTURE_DEFAULTS = {
  theme: "system", font: "serif", size: 18, width: 34, link: "#d4692a", contrast: "normal",
  // Icons only, text only, or both, for every cell's Run/Reset/Duplicate/
  // Delete and the rest (planning/CELL_IDENTITY.md §9) — same key, same
  // default, and the same [data-button-labels] CSS rule (tutorial-style.css)
  // a tutorial page's own copy of this row uses, so the choice reads the
  // same on both.
  buttons: "both",
};

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
  if (state.contrast === "normal") root.removeAttribute("data-contrast"); else root.setAttribute("data-contrast", state.contrast);
  if (state.buttons === "both") root.removeAttribute("data-button-labels"); else root.setAttribute("data-button-labels", state.buttons);
  root.style.setProperty("--dl-font-size", `${state.size}px`);
  root.style.setProperty("--dl-line-width", `${state.width}rem`);
  // High contrast overrides a reader's own link colour the same way it
  // already overrides their font choice — but
  // font-family only ever comes from the stylesheet's [data-contrast]
  // rule, while link colour is normally also written here as an inline
  // style, and an inline style always wins over any stylesheet rule
  // regardless of selector specificity. Skipping the inline write while
  // high contrast is on lets that rule apply instead of being shadowed
  // by whatever the reader last picked (including dewlab's own default).
  // The same reasoning applies to the default colour itself. No single
  // inline value can serve both themes: the brand orange is 4.96:1 on the
  // dark background and 3.5:1 on the light one, and a value dark enough
  // for light (4.74:1) drops to 3.66:1 on dark. The stylesheet already
  // carries a value per theme, so a reader who has not picked a colour of
  // their own gets no inline write at all and the right one applies.
  const chosen = state.contrast === "normal" && state.link
                 && state.link.toLowerCase() !== TEXTURE_DEFAULTS.link.toLowerCase();
  if (chosen) root.style.setProperty("--dl-link", state.link);
  else root.style.removeProperty("--dl-link");
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
      for (const btn of group.querySelectorAll("button")) setSegChecked(btn, btn.dataset.value === current);
      syncSegRoving(group);
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
      for (const btn of group.querySelectorAll("button")) setSegChecked(btn, btn.dataset.value === current);
      syncSegRoving(group);
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
    for (const btn of group.querySelectorAll("button")) setSegChecked(btn, btn.dataset.value === mode);
    syncSegRoving(group);
  };
  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    try { localStorage.setItem(PRACTICE_ORDER_KEY, btn.dataset.value); } catch {}
    sync();
  });
  sync();
}

function loadCellTypeToggles() {
  enabledCellTypes = new Set([CELL_TYPES.PYTHON, CELL_TYPES.TEXT]);
  for (const t of CELL_TYPE_TOGGLES) {
    let on = t.defaultOn;
    try {
      const saved = localStorage.getItem(t.key);
      if (saved === "on") on = true;
      else if (saved === "off") on = false;
    } catch {}
    if (on) enabledCellTypes.add(t.type);
  }
}

function initCellTypeSettings() {
  loadCellTypeToggles();

  const panel = document.getElementById("dl-settings-cell-types");
  if (!panel) return;

  const sync = () => {
    for (const t of CELL_TYPE_TOGGLES) {
      const group = panel.querySelector(`.dl-seg[data-dm="${t.dm}"]`);
      if (!group) continue;
      const on = enabledCellTypes.has(t.type);
      for (const btn of group.querySelectorAll("button")) {
        setSegChecked(btn, btn.dataset.value === (on ? "on" : "off"));
      }
      syncSegRoving(group);
    }
  };

  for (const t of CELL_TYPE_TOGGLES) {
    const group = panel.querySelector(`.dl-seg[data-dm="${t.dm}"]`);
    group?.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      const on = btn.dataset.value === "on";
      if (on) enabledCellTypes.add(t.type); else enabledCellTypes.delete(t.type);
      try { localStorage.setItem(t.key, on ? "on" : "off"); } catch {}
      sync();
      renderCells();
    });
  }
  sync();
}

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
    for (const btn of group.querySelectorAll("button")) setSegChecked(btn, btn.dataset.value === (show ? "on" : "off"));
    syncSegRoving(group);
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

function observeThemeChanges() {
  const observer = new MutationObserver((mutations) => {
    if (!mutations.some((m) => m.attributeName === "data-theme")) return;
    const dark = isDarkNow();
    cells.forEach((c) => { if (c.editor) { try { setEditorTheme(c.editor, dark); } catch {} } });
    if (fileEditor) { try { setEditorTheme(fileEditor, dark); } catch {} }
    if (siteEditors) {
      for (const ed of Object.values(siteEditors)) { try { setEditorTheme(ed, dark); } catch {} }
    }
  });
  observer.observe(document.documentElement, { attributes: true });
}

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
    cells.forEach(destroyCellEditors);
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
    if (siteEditors) {
      for (const ed of Object.values(siteEditors)) { try { setEditorTheme(ed, dark); } catch {} }
    }
  });
  initEditorSettings();
  initNotes();
  initFilename();
  initPracticeOrderSettings();
  initRunStatsSetting();
  initCellTypeSettings();
  initSegKeyboardNav();
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
