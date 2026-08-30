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

const PYODIDE_VERSION = "0.28.3";
const STORAGE_KEY = "dewmini:cells:v1";
const NOTES_KEY = "dewmini:notes";

// Beyond the curriculum's numpy/pandas/matplotlib baseline (DECISIONS.md
// "Core libraries"), dewmini also loads sqlite3 (an unvendored stdlib
// module in Pyodide, one extra loadPackage() entry — DECISIONS_LOG.md 7.78)
// and Pillow (what image_input() decodes a picked file into). A tutorial
// page stays on the narrower curriculum baseline; dewmini is a general
// notebook, not curriculum content, so it can afford the wider default.
const DM_PACKAGES = ["numpy", "pandas", "matplotlib", "sqlite3", "Pillow"];

const CELL_TYPES = { PYTHON: "python", TEXT: "text" };
const IMPORTS_SNIPPET = "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n";

const SEED_GLOBALS_CODE = `
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewmini__"
`;

let cells = [];
let cellsContainer, emptyEl, statusEl;
let statusClearTimer = null;

let pyodide = null;
let tools = null;
let inspectModule = null;
let toolsSourceCache = null;
let bootPromise = null;
let running = false;

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

/* Reads the notebook back out of localStorage on page load. The
 * `.filter(...)` step matters: it drops anything that doesn't look like
 * a real cell (a corrupted entry, or one from some future version of
 * this file with a cell type this version doesn't know about) rather
 * than trusting whatever was stored — a cheap defense against a stray
 * bad value crashing the whole notebook on load. */
function loadSavedState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    cells = saved
      .filter((c) => c && c.id && [CELL_TYPES.PYTHON, CELL_TYPES.TEXT].includes(c.type))
      .map((c) => ({ id: c.id, type: c.type, content: c.content || "", output: c.output || "", error: !!c.error, lastRunMs: typeof c.lastRunMs === "number" ? c.lastRunMs : undefined }));
  } catch {
    cells = [];
  }
}

/* Saves the notebook to localStorage. Note the `.map(({ id, type,
 * content, output, error }) => ({...}))` step: by the time a cell has
 * been rendered, it also carries live things like `.editor` (a CodeMirror
 * instance) and `.outputEl` (a DOM element) — objects that
 * `JSON.stringify` can't handle (they contain circular references back
 * to themselves) and that don't belong in storage anyway, since they get
 * rebuilt fresh every time the notebook renders. This picks out only the
 * five plain-data fields worth keeping, the same "build a fresh plain
 * object rather than serializing the live one directly" fix
 * `assets/mini-ide.js`'s own `saveState()` needed for the same reason. */
function saveState() {
  const plain = cells.map(({ id, type, content, output, error, lastRunMs }) => ({
    id, type, content, output: output || "", error: !!error,
    lastRunMs: typeof lastRunMs === "number" ? lastRunMs : undefined
  }));
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(plain));
  } catch {}
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
  cells = EXAMPLE_CELLS.map((c) => ({ id: generateId(), type: c.type, content: c.content, output: "", error: false }));
  saveState();
  renderCells();
  updateStatus("Example loaded — running it now…");
  await runAllCells();
}

/* Turns a delete button's click into "press once to arm, press again to
 * actually delete" — ported from Mini IDE's own armDeleteButton(). An
 * armed button auto-disarms after a few seconds, on blur, or the moment
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

/* A small, deliberately shallow markdown for documentation cells — headings,
 * bold/italic, inline code, bullets, paragraphs. Not CommonMark: a text
 * cell is a note beside the code, not a document, and the whole point is
 * that a student can read the syntax in the raw textarea at a glance. */
function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
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
 * `&` in their notes from being misread as real HTML. */
function renderDocMarkdown(text) {
  const out = [];
  let listOpen = false;
  let para = [];
  const closeList = () => { if (listOpen) { out.push("</ul>"); listOpen = false; } };
  const flushPara = () => { if (para.length) { out.push(`<p>${renderDocInline(para.join(" "))}</p>`); para = []; } };

  for (const raw of escapeHtml(text).split("\n")) {
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
  return out.join("\n") || '<p class="dm-doc-empty">Empty note.</p>';
}

function renderCells() {
  if (!cellsContainer) return;
  cellsContainer.innerHTML = "";
  // No dividers over an empty notebook — the empty state's own button is
  // the one way in until there is at least one cell to insert around.
  if (cells.length) {
    cellsContainer.appendChild(createInsertDivider(0));
    cells.forEach((cell, i) => {
      cellsContainer.appendChild(createCellElement(cell));
      cellsContainer.appendChild(createInsertDivider(i + 1));
    });
  }
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

  actions.append(addPy, addTxt);
  row.append(line, actions);
  return row;
}

/* Updates a cell's on-page "chrome" (right now, just whether it shows the
 * error styling) to match its data, without a full re-render of the
 * whole notebook — called after running a cell, when only that one
 * cell's error state could possibly have changed. */
function updateCellChrome(id) {
  const el = cellsContainer?.querySelector(`.dm-cell[data-id="${id}"]`);
  const cell = cells.find((c) => c.id === id);
  if (el && cell) el.classList.toggle("dm-error", !!cell.error);
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

  const head = document.createElement("div");
  head.className = "dm-cell-head";
  head.draggable = true;
  head.dataset.id = cell.id;

  const pill = document.createElement("span");
  pill.className = "dm-cell-pill";
  pill.textContent = cell.type === CELL_TYPES.PYTHON ? "Python" : "Text";

  const spacer = document.createElement("span");
  spacer.className = "dm-cell-spacer";

  const actions = document.createElement("div");
  actions.className = "dm-cell-actions";

  // Filled in by the text-cell branch below, since attaching an image
  // needs the textarea/showEditor closures that only exist there. The
  // button itself lives in the head, built here alongside Run/Delete so
  // all three sit in one row regardless of which branch runs.
  let insertDocImage = null;
  // Same reasoning, for the explicit Edit/View button a text cell's
  // header gets below: clicking a rendered note to get back to editing
  // it works with a mouse, but has no equivalent affordance on a touch
  // device, which has no hover to reveal that the note is clickable at
  // all. Its label is kept in sync by showEditor()/showRendered().
  let previewBtn = null;

  if (cell.type === CELL_TYPES.PYTHON) {
    const runBtn = document.createElement("button");
    runBtn.type = "button";
    runBtn.className = "dm-icon-btn dm-icon-run";
    runBtn.title = "Run this cell (Shift+Enter)";
    runBtn.textContent = "▶";
    runBtn.addEventListener("click", (e) => { e.stopPropagation(); runCell(cell.id); });
    actions.appendChild(runBtn);

    // Clears this cell's own output without touching its code — the
    // non-destructive counterpart to Delete, matching Mini IDE's own
    // per-cell reset button.
    const resetOutputBtn = document.createElement("button");
    resetOutputBtn.type = "button";
    resetOutputBtn.className = "dm-icon-btn dm-icon-reset-output";
    resetOutputBtn.title = "Clear this cell's output";
    resetOutputBtn.textContent = "↺";
    resetOutputBtn.addEventListener("click", (e) => { e.stopPropagation(); resetCellOutput(cell.id); });
    actions.appendChild(resetOutputBtn);
  } else {
    // Filled in below, once showEditor()/showRendered() exist to call —
    // built here so it sits in the header row with the other buttons
    // regardless of where in this function the text-cell branch runs.
    previewBtn = document.createElement("button");
    previewBtn.type = "button";
    previewBtn.className = "dm-icon-btn dm-icon-preview";
    actions.appendChild(previewBtn);

    const imgBtn = document.createElement("button");
    imgBtn.type = "button";
    imgBtn.className = "dm-icon-btn dm-icon-image";
    imgBtn.title = "Attach an image from your device";
    imgBtn.innerHTML = '<span class="dm-tool-icon dm-tool-icon-image" aria-hidden="true"></span>';
    imgBtn.addEventListener("click", (e) => { e.stopPropagation(); insertDocImage?.(); });
    actions.appendChild(imgBtn);
  }

  // Arm-then-confirm rather than a native confirm() dialog: a dialog
  // stops the whole page and needs a mouse trip to its own button,
  // where this just needs a second, deliberate press of the same one.
  const delBtn = document.createElement("button");
  delBtn.type = "button";
  delBtn.className = "dm-icon-btn dm-icon-delete";
  delBtn.title = "Delete this cell";
  delBtn.textContent = "×";
  delBtn.addEventListener("click", (e) => { e.stopPropagation(); armDeleteButton(delBtn, () => deleteCell(cell.id)); });
  actions.appendChild(delBtn);

  head.append(pill, spacer, actions);

  const content = document.createElement("div");
  content.className = "dm-cell-content";

  if (cell.type === CELL_TYPES.PYTHON) {
    const editorEl = document.createElement("div");
    editorEl.className = "dm-editor";
    content.appendChild(editorEl);

    const editor = createCodeEditor(editorEl, cell.content, {
      dark: isDarkNow(),
      onChange: (text) => { cell.content = text; saveState(); },
      completeNames: pageNamesCompletion,
      getDoc: (name) => getDocForName(name),
    });
    // Capture phase: CodeMirror's own handler sees Enter first on bubble,
    // so intercepting Shift+Enter has to happen before that, not after.
    editorEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && e.shiftKey) { e.preventDefault(); e.stopPropagation(); runCell(cell.id); }
    }, true);
    cell.editor = editor;
  } else {
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

    content.append(textarea, renderEl);
    cell.textarea = textarea;
    cell.showTextEditor = showEditor;

    if (cell.content.trim()) showRendered();
    else syncPreviewBtn();
  }

  const outputEl = document.createElement("div");
  outputEl.className = "dm-cell-output";
  if (cell.output) outputEl.innerHTML = cell.output;
  else outputEl.classList.add("dm-empty");
  cell.outputEl = outputEl;

  // Run time, under the output — see renderCellRunStats() below. Empty
  // (nothing to show, or the Settings toggle is off) collapses to
  // nothing via :empty, same as .dm-cell-output itself.
  const statsEl = document.createElement("div");
  statsEl.className = "dm-cell-stats";
  cell.statsEl = statsEl;
  if (cell.type === CELL_TYPES.PYTHON) renderCellRunStats(cell);

  main.append(head, content, outputEl, statsEl);
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

/* Starts Pyodide the first time it's actually needed (the first Run
 * click), not when the page loads — downloading and starting a whole
 * Python interpreter is slow, and a student reading or writing notes
 * shouldn't have to wait for it if they never run a cell. `bootPromise`
 * caches the boot *in progress*: a second call while still booting
 * returns that same Promise rather than starting a second, wasted boot;
 * once boot fails, the catch handler resets everything back to null so a
 * later retry (a later Run click) gets a fresh attempt. */
async function ensurePyodide() {
  if (pyodide && tools) return pyodide;
  if (bootPromise) return bootPromise;

  bootPromise = (async () => {
    updateStatus("Loading Python…");
    const pyodideUrl = new URL(`https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`, document.baseURI).href;
    const loader = globalThis.loadPyodide || (await import(/* @vite-ignore */ pyodideUrl + "pyodide.mjs")).loadPyodide;
    pyodide = await loader({ indexURL: pyodideUrl });

    updateStatus("Loading packages…");
    await pyodide.loadPackage(DM_PACKAGES);

    updateStatus("Preparing notebook tools…");
    const source = await getToolsSource();
    pyodide.FS.writeFile("/home/pyodide/tutorial_tools.py", source, { encoding: "utf8" });
    tools = pyodide.pyimport("tutorial_tools");
    inspectModule = pyodide.pyimport("inspect");
    tools.configure("../data/");
    await pyodide.runPythonAsync(SEED_GLOBALS_CODE);

    updateStatus("Python ready.", "ok");
    return pyodide;
  })().catch((err) => {
    bootPromise = null;
    pyodide = null;
    tools = null;
    console.error("dewmini: Pyodide failed to start", err);
    updateStatus(`Python failed to start: ${err.message}`, "error");
    throw err;
  });

  return bootPromise;
}

/* A real CodeMirror completion source (context => CompletionResult|null),
 * not just a names array — passed straight through to createCodeEditor,
 * which uses it as one of the autocompletion engine's own sources. Reads
 * live from tools._page_globals, the exact dict a cell actually runs
 * against, the same way tutorial-runtime.js's own pageNamesCompletion does. */
function pageNamesCompletion(context) {
  if (!tools) return null;
  const word = context.matchBefore(/\w+/);
  if (!word || (word.from === word.to && !context.explicit)) return null;
  const names = [...tools._page_globals.keys()].filter((name) => !name.startsWith("_"));
  if (!names.length) return null;
  return { from: word.from, options: names.map((label) => ({ label, type: "variable" })) };
}

/* Gets the docstring for a name that's already run, for CodeMirror's
 * hover tooltip — using Python's own `inspect.getdoc`, the same thing
 * behind Python's built-in `help()`. Unlike Mini IDE and the tutorial
 * pages, dewmini runs Python directly on the main thread with no Worker,
 * so there's no Jedi-based static-analysis fallback for code that hasn't
 * run yet — only this live lookup (see this file's own "What's different
 * from a tutorial page" note in docs/DEWMINI.md for why). The `finally`
 * block's `.destroy()` call matters: Pyodide hands JavaScript a *proxy*
 * standing in for the real Python object, and it has to be destroyed
 * explicitly once no longer needed, or Pyodide can't free the memory. */
function getDocForName(name) {
  if (!tools || !inspectModule || !/^[A-Za-z_]\w*$/.test(name)) return null;
  let obj;
  try {
    obj = tools._page_globals.get(name);
  } catch {
    return null;
  }
  if (obj === undefined || obj === null) return null;
  try {
    return inspectModule.getdoc(obj) || null;
  } catch {
    return null;
  } finally {
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

/* Runs one cell's code through tutorial_tools.py's own run_cell() (the
 * same function every dewlab tutorial cell runs through) and records
 * what happened: the rendered output HTML (so it can be saved and shown
 * again without re-running), and whether it errored. Returns whether the
 * run succeeded, the same true/false run_cell() itself returns. */
async function executeCell(cell) {
  await ensurePyodide();
  const outputEl = cell.outputEl;
  if (!outputEl) return true;
  outputEl.classList.remove("dm-empty");
  outputEl.innerHTML = '<span class="dm-running">Running…</span>';
  const startedAt = performance.now();
  const ok = await tools.run_cell(cell.id, outputEl, cell.content);
  setCellRunStats(cell, performance.now() - startedAt);
  cell.output = outputEl.innerHTML;
  cell.error = !ok;
  if (!outputEl.innerHTML.trim()) outputEl.classList.add("dm-empty");
  updateCellChrome(cell.id);
  saveState();
  return ok;
}

/* Formats how long a cell's last run took, human-scale rather than raw
 * milliseconds: "340 ms" under a second, "2.4 s" at or above it. Ported
 * from Mini IDE's own formatRunDuration(). */
function formatRunDuration(ms) {
  return ms < 1000 ? `${Math.round(ms)} ms` : `${(ms / 1000).toFixed(1)} s`;
}

/* Records and (when the "Run time" setting is on) displays how long a
 * cell's most recent run took. Always kept on the cell object — cheap to
 * compute, and worth saving even while the setting is off, in case a
 * reader turns it on later without re-running everything. */
function setCellRunStats(cell, ms) {
  cell.lastRunMs = ms;
  renderCellRunStats(cell);
}

/* Paints (or clears) one cell's stats line from its stored lastRunMs. */
function renderCellRunStats(cell) {
  if (!cell.statsEl) return;
  const showStats = document.documentElement.getAttribute("data-dm-runstats") !== "off";
  cell.statsEl.textContent = (showStats && typeof cell.lastRunMs === "number")
    ? `Ran in ${formatRunDuration(cell.lastRunMs)}`
    : "";
}

/* Clears one cell's output (and its run-time stat) without touching its
 * code — the non-destructive counterpart to deleting the cell outright.
 * A no-op while something is running, since clearing mid-run would fight
 * the output the running cell is actively writing. */
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
  delete cell.lastRunMs;
  renderCellRunStats(cell);
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

/* Runs a single cell by id, in response to its own Run button or
 * Shift+Enter. `running` is a simple flag guarding against overlapping
 * runs — dewmini has one Python interpreter, so only one cell can
 * actually be executing at a time; a click while something else is
 * already running is just ignored rather than queued. */
async function runCell(id) {
  if (running) return;
  const cell = cells.find((c) => c.id === id);
  if (!cell || cell.type !== CELL_TYPES.PYTHON) return;
  running = true;
  try {
    const ok = await executeCell(cell);
    updateStatus(ok ? "Ran." : "Error — see the cell.", ok ? "ok" : "error");
  } catch (err) {
    updateStatus(`Python isn't available: ${err.message}`, "error");
  } finally {
    running = false;
  }
}

/* Runs every Python cell in order, top to bottom — "Run all." Unlike
 * runCell() for a single cell, this first calls
 * `tools.reset_page_state()` and re-seeds the shared namespace: running
 * every cell again from a clean slate is what makes "what's on screen
 * matches what the code actually did" true even if, say, a variable a
 * cell used to define got deleted from the notebook — without the
 * reset, a stale value from a previous run could linger and mask that
 * kind of mistake. */
async function runAllCells() {
  if (running) return;
  const pythonCells = cells.filter((c) => c.type === CELL_TYPES.PYTHON);
  if (!pythonCells.length) { updateStatus("No Python cells to run."); return; }

  running = true;
  const btn = document.getElementById("run-all");
  if (btn) btn.disabled = true;

  try {
    await ensurePyodide();
    tools.reset_page_state();
    await pyodide.runPythonAsync(SEED_GLOBALS_CODE);
    updateStatus(`Running ${pythonCells.length} cell${pythonCells.length === 1 ? "" : "s"}…`);

    let errors = 0;
    for (const cell of pythonCells) {
      const ok = await executeCell(cell);
      if (!ok) errors += 1;
    }
    updateStatus(
      errors ? `Done — ${errors} cell${errors === 1 ? "" : "s"} errored.` : "All cells ran cleanly.",
      errors ? "error" : "ok"
    );
  } catch (err) {
    updateStatus(`Python isn't available: ${err.message}`, "error");
  } finally {
    running = false;
    if (btn) btn.disabled = false;
  }
}

// -------------------------------------------------------------- downloads

/* Reads the reader's chosen filename from Settings, cleaned up for use
 * as an actual filename: any extension they typed is stripped (each
 * download function adds its own), and characters that aren't valid in
 * a filename on at least one common operating system (`\ / : * ? " < >
 * |`) are replaced with a dash, so the same name works whether the
 * download lands on Windows, macOS, or Linux. */
function getFilenameBase() {
  const el = document.getElementById("dm-filename");
  let name = (el?.value || "").trim();
  if (!name) name = "dewmini-notebook";
  name = name.replace(/\.(py|html?|ipynb)$/i, "");
  name = name.replace(/[\\/:*?"<>|]+/g, "-").trim();
  return name || "dewmini-notebook";
}

/* Restores a previously chosen filename (and keeps the browser tab title
 * in sync with it as the reader types) — cosmetic, but it's what makes
 * "print to PDF" and the download buttons suggest something more useful
 * than a generic default name. */
function initFilename() {
  const el = document.getElementById("dm-filename");
  if (!el) return;
  let saved = "dewmini-notebook";
  try { saved = localStorage.getItem("dewmini:filename") || saved; } catch {}
  el.value = saved;
  document.title = `${saved} — dewmini`;
  el.addEventListener("input", () => {
    try { localStorage.setItem("dewmini:filename", el.value); } catch {}
    document.title = `${getFilenameBase()} — dewmini`;
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
 * script — no special notebook format needed to open it. The
 * "# ---- cell N ----"/"# ---- note ----" markers are also exactly what
 * parsePyCells() looks for on the way back in, so a downloaded .py loads
 * straight back into the same cells, notes included. */
function downloadAsPython() {
  if (!cells.length) { updateStatus("No cells to export.", "error"); return; }
  const parts = [`# dewmini export — ${new Date().toISOString().slice(0, 10)}`, ""];
  cells.forEach((cell, i) => {
    if (cell.type === CELL_TYPES.TEXT) {
      parts.push("# ---- note ----");
      cell.content.split("\n").forEach((line) => parts.push(`# ${line}`.trimEnd()));
    } else {
      parts.push(`# ---- cell ${i + 1} ----`, cell.content);
    }
    parts.push("");
  });
  triggerDownload(`${getFilenameBase()}.py`, parts.join("\n"), "text/x-python");
  updateStatus("Downloaded as Python.", "ok");
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

/* Builds a real Jupyter notebook (nbformat 4) file: a Python cell becomes
 * a "code" cell, a text cell becomes a "markdown" cell, in the exact JSON
 * shape Jupyter, JupyterLab, and Colab all expect — so the file this
 * produces opens correctly in any of them, and the same file loads back
 * into dewmini via handleImportFile() below. */
function downloadAsIpynb() {
  if (!cells.length) { updateStatus("No cells to export.", "error"); return; }
  const notebook = {
    nbformat: 4,
    nbformat_minor: 5,
    metadata: {
      kernelspec: { display_name: "Python 3", language: "python", name: "python3" },
      language_info: { name: "python", pygments_lexer: "ipython3" },
    },
    cells: cells.map((cell) => ({
      cell_type: cell.type === CELL_TYPES.PYTHON ? "code" : "markdown",
      metadata: {},
      source: splitLines(cell.content),
      ...(cell.type === CELL_TYPES.PYTHON ? { execution_count: null, outputs: [] } : {}),
    })),
  };
  triggerDownload(`${getFilenameBase()}.ipynb`, JSON.stringify(notebook, null, 2), "application/json");
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
 * for a bug in their own logic that was never there. Ported from Mini
 * IDE's own PYODIDE_INCOMPATIBLE_MODULES. */
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
 * work once they actually run here. Ported from Mini IDE's own
 * scanPyodideCompatibility() — see that function's own comment for the
 * full reasoning; identical logic, just reading dewmini's own cell
 * shape (`content`, not `.content` behind a CELL_TYPES.PYTHON check
 * that differs in name only). */
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
 * #import-compat-notice — the counterpart to Mini IDE's own
 * import-compat-notice, checked before the scanned cells ever land in
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
 * file's own extension, the same way Mini IDE's own import does
 * (mini-ide.js), rather than sniffing content. */
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
 * example fetched by URL) — the counterpart to Mini IDE's own
 * applyImportedCells(). */
function applyImportedCells(imported, sourceLabel) {
  if (!imported.length) { updateStatus("That notebook has no cells.", "error"); return; }
  showImportCompatNotice(scanPyodideCompatibility(imported));
  cells.forEach((c) => c.editor?.destroy());
  cells = imported;
  saveState();
  renderCells();
  updateStatus(`Loaded ${imported.length} cell${imported.length === 1 ? "" : "s"} from ${sourceLabel}.`, "ok");
}

/* Parses a .ipynb notebook's JSON into dewmini's cell shape — the same
 * mapping handleImportFile() applies to a picked file, factored out so
 * loadBuiltInExample() below can reuse it without duplicating it. */
function parseIpynbCells(text) {
  const notebook = JSON.parse(text);
  if (!Array.isArray(notebook.cells)) throw new Error("that file has no cells array");
  return notebook.cells.map((c) => ({
    id: generateId(),
    type: c.cell_type === "code" ? CELL_TYPES.PYTHON : CELL_TYPES.TEXT,
    content: Array.isArray(c.source) ? c.source.join("") : c.source || "",
    output: "",
    error: false,
  }));
}

/* Parses a .py file into dewmini's cell shape — the counterpart to
 * downloadAsPython() below, recognizing that same function's own
 * "# ---- cell N ----" / "# ---- note ----" markers so a file downloaded
 * from dewmini and reopened here round-trips back into the same cells,
 * notes included (Mini IDE's own .py export/import pair only ever
 * carries Python cells, since it has no note-cell concept to preserve —
 * dewmini's own format predates this port and already handles both, so
 * it's kept rather than switched to Mini IDE's plain "# %%" marker,
 * which cannot tell a note from a cell apart on its own).
 *
 * A file with none of dewmini's own markers — a plain script, or one
 * exported from somewhere else entirely — imports as a single Python
 * cell instead, the same fallback Mini IDE's own parsePy() uses for an
 * unmarked file (mini-ide.js).
 *
 * @param {string} text - raw .py file contents
 * @returns {Array<Object>} new cell objects, same shape parseIpynbCells() returns
 */
function parsePyCells(text) {
  const markerRe = /^# ---- (cell \d+|note) ----$/;
  const lines = text.split("\n");
  if (!lines.some((line) => markerRe.test(line))) {
    const trimmed = text.trim();
    return trimmed ? [{ id: generateId(), type: CELL_TYPES.PYTHON, content: trimmed, output: "", error: false }] : [];
  }

  // downloadAsPython() prefixes every note line with "# " (or a bare "#"
  // for a line that was empty) — this reverses exactly that, not a
  // general "#" comment stripper, so a genuine Python comment inside a
  // *code* cell is left alone (this only ever runs on a "note" block's
  // own lines).
  const unescapeNoteLine = (line) => {
    if (line === "#") return "";
    if (line.startsWith("# ")) return line.slice(2);
    if (line.startsWith("#")) return line.slice(1);
    return line;
  };

  const cells = [];
  let currentType = null;
  let buffer = [];
  const flush = () => {
    // Content before the first marker is downloadAsPython()'s own
    // header line ("# dewmini export — <date>") — not a cell.
    if (currentType === null) { buffer = []; return; }
    const raw = currentType === CELL_TYPES.TEXT ? buffer.map(unescapeNoteLine).join("\n") : buffer.join("\n");
    const content = raw.replace(/\n+$/, "");
    if (content.trim()) cells.push({ id: generateId(), type: currentType, content, output: "", error: false });
    buffer = [];
  };
  for (const line of lines) {
    const marker = line.match(markerRe);
    if (marker) {
      flush();
      currentType = marker[1] === "note" ? CELL_TYPES.TEXT : CELL_TYPES.PYTHON;
      continue;
    }
    buffer.push(line);
  }
  flush();
  return cells;
}

/* Loads one of dewlab's own worked examples (assets/examples/*.ipynb) —
 * a real, runnable walkthrough (SQL over a real dataset, a data
 * investigation, a math simulation, text analysis). Ported from Mini
 * IDE's own loadBuiltInExample(); replaces the notebook outright, the
 * same as picking a file already does here. */
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

// ------------------------------------------------------------------ panels

/* The replacement for native CSS `resize: horizontal` on a right-docked
 * panel — ported from tutorial-runtime.js's own copy (DECISIONS_LOG.md
 * 7.84). Native resize draws its handle at a box's own bottom-right
 * corner, which for a panel flush to the browser window's own right
 * edge sits exactly on that edge with no room to drag further right and
 * grow it. Adds a thin strip along `panel`'s left edge instead and
 * tracks a plain pointer drag on it directly. */
function makeRightEdgeResizable(panel, min = 256, max = 640) {
  if (!panel || panel.querySelector(".dl-panel-resize-handle")) return;
  const handle = document.createElement("div");
  handle.className = "dl-panel-resize-handle";
  handle.setAttribute("aria-hidden", "true");
  panel.prepend(handle);

  let startX = 0;
  let startWidth = 0;

  function onMove(ev) {
    const dx = startX - ev.clientX;
    const next = Math.max(min, Math.min(startWidth + dx, Math.min(max, window.innerWidth)));
    panel.style.width = `${next}px`;
  }
  function onUp() {
    handle.classList.remove("dl-panel-resize-active");
    document.removeEventListener("pointermove", onMove);
    document.removeEventListener("pointerup", onUp);
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

/* A small reusable version of the "toggle open/closed, and close the
 * other one" pattern tutorial-runtime.js's Settings/reference/nav
 * panels use — generalized into one function here since dewmini only has
 * the two panels (Settings and Help) to coordinate, rather than three. */
function wireSimplePanel(panel, toggle, closeBtn, otherPanel) {
  if (!panel) return;
  toggle?.addEventListener("click", () => {
    const opening = panel.hidden;
    panel.hidden = !opening;
    toggle.setAttribute("aria-expanded", String(opening));
    if (opening && otherPanel && !otherPanel.hidden) {
      otherPanel.hidden = true;
      otherPanel.dispatchEvent(new Event("dm-closed"));
    }
  });
  closeBtn?.addEventListener("click", () => {
    panel.hidden = true;
    toggle?.setAttribute("aria-expanded", "false");
    toggle?.focus();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !panel.hidden) {
      panel.hidden = true;
      toggle?.setAttribute("aria-expanded", "false");
    }
  });
  document.addEventListener("click", (e) => {
    if (panel.hidden) return;
    if (panel.contains(e.target) || toggle?.contains(e.target)) return;
    panel.hidden = true;
    toggle?.setAttribute("aria-expanded", "false");
  });
}

/* Remembers which of Settings/Help a reader left open, the same
 * localStorage-persisted-sidebar mechanism tutorial pages use (see
 * saveSidebarState()/restoreSidebarState() in tutorial-runtime.js,
 * DECISIONS_LOG.md 7.83) — a returning reader's panel comes back open
 * rather than needing to be reopened, since it's meant to be a permanent
 * pane, not a popover that happens to be open right now. dewmini only
 * ever has one of the two open at a time (both dock to the same right
 * edge), so this stores a single value rather than the tutorial pages'
 * {left, right} pair — ported from Mini IDE's own copy. */
function saveSidebarState() {
  const settingsPanel = document.getElementById("dl-settings");
  const helpPanel = document.getElementById("dm-help");
  const open = settingsPanel && !settingsPanel.hidden ? "settings"
    : helpPanel && !helpPanel.hidden ? "help"
    : null;
  try {
    localStorage.setItem("dewlab:dewmini:sidebar", JSON.stringify({ open }));
  } catch (e) { /* private mode, blocked storage: nothing to remember */ }
}

/* The other half of saveSidebarState() — reopens whatever was left open
 * last time by clicking its toggle, reusing that toggle's own open logic
 * rather than duplicating it. Skipped below the phone breakpoint, where
 * a panel is a bottom sheet covering most of the screen rather than a
 * sidebar worth leaving open by default. */
function restoreSidebarState() {
  if (!window.matchMedia("(min-width: 34rem)").matches) return;
  let state;
  try {
    state = JSON.parse(localStorage.getItem("dewlab:dewmini:sidebar") || "{}");
  } catch (e) {
    return;
  }
  const toggleId = state.open === "settings" ? "dl-settings-toggle"
    : state.open === "help" ? "dm-help-toggle"
    : null;
  if (toggleId) document.getElementById(toggleId)?.click();
}

/* Keeps `<html data-dl-panel-open>` in sync with whether Settings or Help
 * is currently visible, regardless of which of their several open/close
 * paths (toggle click, close button, Escape, click-outside, wireSimplePanel's
 * own "opening one closes the other") fired — a MutationObserver on each
 * panel's `hidden` property, rather than hooking every call site. Ported
 * from Mini IDE's own watchPanelOverlap(). dewmini-style.css reads the
 * attribute to shrink .dl-page's effective width on wide-enough viewports
 * while a panel is open, so its fixed position (tutorial-style.css's own
 * .dl-settings/.dm-panel) never ends up covering a cell's run/reset/delete
 * buttons or its output.
 *
 * A ResizeObserver on the same panels keeps --dl-panel-w in step with
 * whichever one is actually open's *real* rendered width, not a guess —
 * a docked sidebar can be dragged wider or narrower via its own resize
 * handle at any time, same reasoning as tutorial-runtime.js's own copy
 * (DECISIONS_LOG.md 7.83). */
function watchPanelOverlap(...panels) {
  const real = panels.filter(Boolean);
  if (!real.length) return;
  const sync = () => {
    const anyOpen = real.some((p) => !p.hidden);
    document.documentElement.toggleAttribute("data-dl-panel-open", anyOpen);
    saveSidebarState();
  };
  for (const panel of real) {
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ["hidden"] });
  }
  // Only the DOM attribute, not a persisted-state write: every panel is
  // still hidden at this point in startup, before restoreSidebarState()
  // has had a chance to reopen whatever was actually saved last time —
  // persisting here would overwrite a real saved preference with
  // "everything closed" on every single load.
  document.documentElement.toggleAttribute("data-dl-panel-open", real.some((p) => !p.hidden));

  const widthObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      const panel = entry.target;
      if (panel.hidden) continue;
      // offsetWidth, not the observer's own contentRect: the margin
      // needs to clear the panel's full border box (border + padding),
      // plus a small gutter so text doesn't sit flush against its edge.
      document.documentElement.style.setProperty("--dl-panel-w", `${panel.offsetWidth + 16}px`);
    }
  });
  for (const panel of real) widthObserver.observe(panel);
}

function initPanels() {
  const settingsPanel = document.getElementById("dl-settings");
  const helpPanel = document.getElementById("dm-help");
  makeRightEdgeResizable(settingsPanel, 256, 640); // matches .dl-settings' own min/max-width
  makeRightEdgeResizable(helpPanel, 256, 640); // matches .dm-panel's own min/max-width
  wireSimplePanel(settingsPanel, document.getElementById("dl-settings-toggle"), document.getElementById("dl-settings-close"), helpPanel);
  wireSimplePanel(helpPanel, document.getElementById("dm-help-toggle"), document.getElementById("dm-help-close"), settingsPanel);
  watchPanelOverlap(settingsPanel, helpPanel);
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
 * dewmini/Mini-IDE-specific — a plain tutorial page has no code editor
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
 * in this browser, then never again — an invitation, not a nag. Only spent
 * when the button will actually be visible (the notebook is empty), so a
 * reader who arrives with cells already in it (an imported .ipynb, say)
 * doesn't burn the one first impression on a hidden button. */
function maybeHighlightExample() {
  if (cells.length) return;
  const btn = document.getElementById("dm-empty-example");
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
 * data-dm-runstats attribute on <html> (read by renderCellRunStats()),
 * re-painted on every already-rendered cell immediately on toggle, not
 * just future runs. Ported from Mini IDE's own initRunStatsSetting(). */
const RUN_STATS_KEY = "dewmini:show-run-stats";

function initRunStatsSetting() {
  let show = true;
  try { show = localStorage.getItem(RUN_STATS_KEY) !== "off"; } catch {}

  const apply = () => {
    document.documentElement.setAttribute("data-dm-runstats", show ? "on" : "off");
    cells.forEach(renderCellRunStats);
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
  });
  observer.observe(document.documentElement, { attributes: true });
}

/* Wires up every toolbar and Settings button that doesn't already have
 * its own dedicated init*() function above — one line per button, each
 * just calling the one function that actually does the work. */
function wireToolbar() {
  document.getElementById("add-python-cell")?.addEventListener("click", () => addCell(CELL_TYPES.PYTHON));
  document.getElementById("add-text-cell")?.addEventListener("click", () => addCell(CELL_TYPES.TEXT));
  document.getElementById("add-practice")?.addEventListener("click", () => addPracticeProblem());
  document.getElementById("dm-empty-add")?.addEventListener("click", () => addCell(CELL_TYPES.PYTHON, IMPORTS_SNIPPET));
  document.getElementById("dm-empty-example")?.addEventListener("click", () => loadExampleCells());
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
    cells = [];
    saveState();
    renderCells();
    updateStatus("Cleared.");
  });
  document.getElementById("download-python")?.addEventListener("click", downloadAsPython);
  document.getElementById("download-html")?.addEventListener("click", downloadAsHtml);
  document.getElementById("download-ipynb")?.addEventListener("click", downloadAsIpynb);
  document.getElementById("import-ipynb")?.addEventListener("click", () => document.getElementById("import-ipynb-file")?.click());
  document.getElementById("import-ipynb-file")?.addEventListener("change", handleImportFile);
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

  loadSavedState();
  initPanels();
  initTexture((dark) => cells.forEach((c) => { if (c.editor) { try { setEditorTheme(c.editor, dark); } catch {} } }));
  initEditorSettings();
  initNotes();
  initFilename();
  initPracticeOrderSettings();
  initRunStatsSetting();
  wireToolbar();
  setupDragAndDrop();
  renderCells();
  maybeHighlightExample();
  trackChromeHeight();
  observeThemeChanges();
}

document.addEventListener("DOMContentLoaded", init);
if (document.readyState !== "loading") init();
