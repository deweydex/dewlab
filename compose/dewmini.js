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

function generateId() {
  return `cell-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

function loadSavedState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    cells = saved
      .filter((c) => c && c.id && [CELL_TYPES.PYTHON, CELL_TYPES.TEXT].includes(c.type))
      .map((c) => ({ id: c.id, type: c.type, content: c.content || "", output: c.output || "", error: !!c.error }));
  } catch {
    cells = [];
  }
}

function saveState() {
  const plain = cells.map(({ id, type, content, output, error }) => ({ id, type, content, output: output || "", error: !!error }));
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(plain));
  } catch {}
}

// ------------------------------------------------------------------- cells

function insertCellAt(index, type, content = "") {
  const cell = { id: generateId(), type, content, output: "", error: false };
  cells.splice(index, 0, cell);
  saveState();
  renderCells();
  focusCell(cell.id);
}

function addCell(type, content = "") {
  insertCellAt(cells.length, type, content);
}

function deleteCell(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  cells[idx].editor?.destroy();
  cells.splice(idx, 1);
  saveState();
  renderCells();
  updateStatus("Cell deleted.");
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

/* A small, deliberately shallow markdown for documentation cells — headings,
 * bold/italic, inline code, bullets, paragraphs. Not CommonMark: a text
 * cell is a note beside the code, not a document, and the whole point is
 * that a student can read the syntax in the raw textarea at a glance. */
function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderDocInline(text) {
  return text
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>")
    .replace(/(^|[^\w])_([^_\n]+)_(?!\w)/g, "$1<em>$2</em>");
}

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

  const addImports = document.createElement("button");
  addImports.type = "button";
  addImports.className = "dm-insert-btn";
  addImports.title = "Insert a Python cell with the common imports";
  addImports.innerHTML = '<span class="dm-tool-icon dm-tool-icon-python" aria-hidden="true"></span>Imports';
  addImports.addEventListener("click", () => insertCellAt(index, CELL_TYPES.PYTHON, IMPORTS_SNIPPET));

  actions.append(addPy, addTxt, addImports);
  row.append(line, actions);
  return row;
}

function updateCellChrome(id) {
  const el = cellsContainer?.querySelector(`.dm-cell[data-id="${id}"]`);
  const cell = cells.find((c) => c.id === id);
  if (el && cell) el.classList.toggle("dm-error", !!cell.error);
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

  if (cell.type === CELL_TYPES.PYTHON) {
    const runBtn = document.createElement("button");
    runBtn.type = "button";
    runBtn.className = "dm-icon-btn dm-icon-run";
    runBtn.title = "Run this cell (Shift+Enter)";
    runBtn.textContent = "▶";
    runBtn.addEventListener("click", (e) => { e.stopPropagation(); runCell(cell.id); });
    actions.appendChild(runBtn);
  }

  const delBtn = document.createElement("button");
  delBtn.type = "button";
  delBtn.className = "dm-icon-btn dm-icon-delete";
  delBtn.title = "Delete this cell";
  delBtn.textContent = "×";
  delBtn.addEventListener("click", (e) => { e.stopPropagation(); deleteCell(cell.id); });
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

    const showEditor = () => {
      textarea.hidden = false;
      renderEl.hidden = true;
      textarea.focus();
    };
    const showRendered = () => {
      if (!cell.content.trim()) return; // nothing to render — keep it open for typing
      renderEl.innerHTML = renderDocMarkdown(cell.content);
      renderEl.hidden = false;
      textarea.hidden = true;
    };

    textarea.addEventListener("input", (e) => { cell.content = e.target.value; saveState(); });
    textarea.addEventListener("blur", showRendered);
    renderEl.addEventListener("click", showEditor);
    renderEl.addEventListener("keydown", (e) => { if (e.key === "Enter") showEditor(); });

    content.append(textarea, renderEl);
    cell.textarea = textarea;
    cell.showTextEditor = showEditor;

    if (cell.content.trim()) showRendered();
  }

  const outputEl = document.createElement("div");
  outputEl.className = "dm-cell-output";
  if (cell.output) outputEl.innerHTML = cell.output;
  else outputEl.classList.add("dm-empty");
  cell.outputEl = outputEl;

  main.append(head, content, outputEl);
  wrap.append(rail, main);
  return wrap;
}

// -------------------------------------------------------------- execution

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

async function ensurePyodide() {
  if (pyodide && tools) return pyodide;
  if (bootPromise) return bootPromise;

  bootPromise = (async () => {
    updateStatus("Loading Python…");
    const pyodideUrl = new URL(`https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`, document.baseURI).href;
    const loader = globalThis.loadPyodide || (await import(/* @vite-ignore */ pyodideUrl + "pyodide.mjs")).loadPyodide;
    pyodide = await loader({ indexURL: pyodideUrl });

    updateStatus("Loading packages…");
    await pyodide.loadPackage(["numpy", "pandas", "matplotlib"]);

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

async function executeCell(cell) {
  await ensurePyodide();
  const outputEl = cell.outputEl;
  if (!outputEl) return true;
  outputEl.classList.remove("dm-empty");
  outputEl.innerHTML = '<span class="dm-running">Running…</span>';
  const ok = await tools.run_cell(cell.id, outputEl, cell.content);
  cell.output = outputEl.innerHTML;
  cell.error = !ok;
  if (!outputEl.innerHTML.trim()) outputEl.classList.add("dm-empty");
  updateCellChrome(cell.id);
  saveState();
  return ok;
}

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

function getFilenameBase() {
  const el = document.getElementById("dm-filename");
  let name = (el?.value || "").trim();
  if (!name) name = "dewmini-notebook";
  name = name.replace(/\.(py|html?|ipynb)$/i, "");
  name = name.replace(/[\\/:*?"<>|]+/g, "-").trim();
  return name || "dewmini-notebook";
}

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

function splitLines(text) {
  const lines = text.split("\n");
  return lines.map((line, i) => (i < lines.length - 1 ? `${line}\n` : line));
}

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
    await pyodide.loadPackage(["numpy", "pandas", "matplotlib"]);
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
let practiceBank = null;

async function loadPracticeBank() {
  if (practiceBank) return practiceBank;
  const res = await fetch("practice-bank.json");
  if (!res.ok) throw new Error(`practice-bank.json: HTTP ${res.status}`);
  practiceBank = await res.json();
  return practiceBank;
}

/* Adds one problem from dewlab's own practice bank — the doc cell states
 * which one, and the code cell is exactly the function stub from the
 * source bank (docstring, Args/Returns/Example and all), so there is
 * nothing to duplicate or drift out of sync with. Cycles through the bank
 * in the order it's numbered and remembers where a reader left off. */
async function addPracticeProblem() {
  try {
    const bank = await loadPracticeBank();
    if (!bank.length) { updateStatus("The practice bank is empty.", "error"); return; }

    let idx = 0;
    try { idx = parseInt(localStorage.getItem(PRACTICE_INDEX_KEY) || "0", 10) || 0; } catch {}
    idx = ((idx % bank.length) + bank.length) % bank.length;
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

    try { localStorage.setItem(PRACTICE_INDEX_KEY, String((idx + 1) % bank.length)); } catch {}
    updateStatus(`Problem ${problem.number} of ${bank.length} added.`, "ok");
  } catch (err) {
    updateStatus(`Couldn't load the practice bank: ${err.message}`, "error");
  }
}

async function handleImportFile(e) {
  const input = e.target;
  const file = input.files && input.files[0];
  input.value = "";
  if (!file) return;
  try {
    const text = await file.text();
    const notebook = JSON.parse(text);
    if (!Array.isArray(notebook.cells)) throw new Error("that file has no cells array");
    const imported = notebook.cells.map((c) => ({
      id: generateId(),
      type: c.cell_type === "code" ? CELL_TYPES.PYTHON : CELL_TYPES.TEXT,
      content: Array.isArray(c.source) ? c.source.join("") : c.source || "",
      output: "",
      error: false,
    }));
    if (!imported.length) { updateStatus("That notebook has no cells.", "error"); return; }
    cells.forEach((c) => c.editor?.destroy());
    cells = imported;
    saveState();
    renderCells();
    updateStatus(`Loaded ${imported.length} cell${imported.length === 1 ? "" : "s"} from ${file.name}.`, "ok");
  } catch (err) {
    updateStatus(`Couldn't read that file: ${err.message}`, "error");
  }
}

// ------------------------------------------------------------- drag reorder

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

// ------------------------------------------------------------------ status

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

function initPanels() {
  const settingsPanel = document.getElementById("dl-settings");
  const helpPanel = document.getElementById("dm-help");
  wireSimplePanel(settingsPanel, document.getElementById("dl-settings-toggle"), document.getElementById("dl-settings-close"), helpPanel);
  wireSimplePanel(helpPanel, document.getElementById("dm-help-toggle"), document.getElementById("dm-help-close"), settingsPanel);

  // Hide any Settings section that ended up with nothing in it (mirrors the
  // rest of the site: an empty section is furniture, not a feature).
  settingsPanel?.querySelectorAll(".dl-settings-section").forEach((section) => {
    if (section.textContent.trim() === "") section.hidden = true;
  });
}

// ----------------------------------------------------------- shared texture

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

// -------------------------------------------------------------- chrome/misc

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
  });
  observer.observe(document.documentElement, { attributes: true });
}

function wireToolbar() {
  document.getElementById("add-python-cell")?.addEventListener("click", () => addCell(CELL_TYPES.PYTHON));
  document.getElementById("add-text-cell")?.addEventListener("click", () => addCell(CELL_TYPES.TEXT));
  document.getElementById("add-practice")?.addEventListener("click", () => addPracticeProblem());
  document.getElementById("dm-empty-add")?.addEventListener("click", () => addCell(CELL_TYPES.PYTHON, IMPORTS_SNIPPET));
  document.getElementById("run-all")?.addEventListener("click", () => runAllCells());
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
  wireToolbar();
  setupDragAndDrop();
  renderCells();
  trackChromeHeight();
  observeThemeChanges();
}

document.addEventListener("DOMContentLoaded", init);
if (document.readyState !== "loading") init();
