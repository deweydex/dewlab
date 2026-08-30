/**
 * Mini IDE - A lightweight cell-based Python environment for dewlab
 *
 * This module provides a browser-based integrated development environment
 * that allows students to create, edit, and run Python and text cells,
 * with full persistence, autocomplete, and download capabilities.
 *
 * Features:
 *   - Python and Text cell creation and management
 *   - Code execution via Pyodide (shared instance with tutorials)
 *   - Drag-and-drop cell reordering
 *   - Download as .py, .html, .ipynb formats
 *   - Full tutorial_tools.py API support
 *   - Persistent storage via localStorage
 *   - Autocomplete via CodeMirror with Jedi integration
 *   - Hover documentation for builtins and user-defined names
 *
 * Architecture:
 *   - Cell array (this file) + Pyodide engine (assets/pyodide-engine.js,
 *     shared with dewmini — DECISIONS_LOG.md 7.89), which boots the same
 *     assets/pyodide-worker.js the tutorial pages use — a
 *     real Worker with real Jedi, a genuine Stop button, and the real
 *     assets/tutorial_tools.py, falling back to the main thread if a
 *     module Worker isn't available (e.g. a file:// download).
 *   - Cells share one persistent Pyodide interpreter (like Jupyter)
 *   - A mounted filesystem (mini-ide-fs.js) — a real local folder if a
 *     student opts in, else OPFS, else IndexedDB — backs uploads,
 *     SQLite .db files, and notebook import/export.
 *   - Cell state persisted to localStorage
 *
 * @module mini-ide
 */

import { createCodeEditor, setEditorTheme } from "./vendor/codemirror.bundle.js";
import * as engine from "./pyodide-engine.js";
import * as fs from "./mini-ide-fs.js";

// ============================================================================
// Configuration Constants
//
// These are the localStorage keys this file itself reads and writes.
// (mini-ide-fs.js and pyodide-engine.js have their own storage keys,
// defined in those files, not here — each module owns the keys it
// actually uses, rather than collecting them all in one shared list.)
// A version suffix like ":v1" on STORAGE_KEY means that if the saved
// shape of a cell ever needs to change in a way old saved data wouldn't
// match, a future ":v2" key can be introduced without old localStorage
// data being silently misread as the new shape.
// ============================================================================

/**
 * LocalStorage key for cells state
 * @constant {string}
 */
const STORAGE_KEY = "mini-ide:cells:v1";

// ============================================================================
// Global State
//
// This file uses plain module-level `let` variables for state, rather
// than a class or a state-management library — the whole page is one
// Mini IDE instance, never more than one at a time, so there's nothing
// to keep separate copies of. `cells` is the one that matters most:
// almost every function in this file either reads it, changes it, or
// both. A cell is a plain JavaScript object (see createNewCell() further
// down); this array holds them in the order they're shown on the page.
// ============================================================================

/**
 * Array of cell objects
 * @type {Array<Object>}
 */
let cells = [];

/**
 * Whether the current cells are sample cells
 * @type {boolean}
 */
let hasSampleCells = false;

// ============================================================================
// DOM Elements
//
// Every element the rest of this file needs to read from or write to
// gets looked up once, in init() (further down), and stored in one of
// these module-level variables — rather than calling
// `document.getElementById(...)` again each time a function needs that
// same element. That's partly for speed (looking an element up by ID is
// not free, even if it's fast), but mainly for clarity: a function like
// `setupEventListeners()` can just write `addPythonBtn.addEventListener(...)`
// and trust the variable already points at the right element, instead
// of re-deriving "which element is this" every time.
// ============================================================================

/**
 * DOM element references (initialized in init())
 */
let cellsContainer;
let addPythonBtn;
let addTextBtn;
let loadExampleBtn;
let runAllBtn;
let clearOutputBtn;
let clearAllBtn;
let statusEl;
let sampleNoticeEl;
let removeSampleBtn;
let filetreeEl;
let filetreeToggleBtn;
let filetreeRefreshBtn;
let filetreeListEl;
let filetreeNoteEl;
let filetreeUploadBtn;
let filetreeUploadInput;
let importNotebookBtn;
let importNotebookInput;
let importCompatNoticeEl;
let importCompatListEl;
let dismissImportCompatBtn;

// ============================================================================
// Drag and Drop State
// ============================================================================

/**
 * The id of the cell currently being dragged, or null when nothing is.
 * Tracked by id rather than a DOM reference — the same reason
 * runCell()/deleteCell() look cells up by id — because the id survives
 * the re-render a drop triggers, where a captured element reference
 * wouldn't.
 * @type {string|null}
 */
let draggedId = null;

// ============================================================================
// Execution State
// ============================================================================

/**
 * ID of the cell currently running, or null. A second click on that same
 * cell's Run button sends a Stop (interrupt) request instead of starting
 * a new run; clicks on any other cell are ignored while one is running.
 * @type {string|null}
 */
let runningCellId = null;

/**
 * Whether "Run All" is in progress.
 * @type {boolean}
 */
let runningAll = false;

/**
 * Whether the filesystem (mini-ide-fs.js) has mounted successfully.
 * The file tree pane stays a placeholder until this flips true.
 * @type {boolean}
 */
let fsReady = false;

// ============================================================================
// Cell Types
// ============================================================================

/**
 * Cell type constants
 * @enum {string}
 */
const CELL_TYPES = {
  PYTHON: 'python',
  TEXT: 'text'
};

// ============================================================================
// Settings Functions (from tutorial-runtime.js)
//
// This block (through initTexture()) is a line-for-line port of the same
// "texture" settings tutorial pages already have — theme, font, text
// size, page width, and link color — copied here rather than imported
// as a shared module, following this codebase's convention that each
// page owns a thin copy of logic it needs rather than sharing one
// runtime file between pages that otherwise have little in common. The
// pattern repeats for every setting: `load*()` reads a saved value from
// localStorage (or a sensible default if there isn't one yet), `apply*()`
// makes the page actually look/behave that way, `save*()` writes the
// current value back to localStorage, and a `commit()` helper calls
// apply-then-save-then-resync in one step so a click handler never has
// to remember the right order itself.
// ============================================================================

/**
 * Check if dark mode is currently active
 * @returns {boolean} True if dark mode is active
 */
function isDarkNow() {
  const t = document.documentElement.getAttribute("data-theme");
  return t === "dark" ? true : t === "light" ? false : window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

/**
 * Load texture preferences from localStorage
 * @returns {Object} Texture state
 */
function loadTexture() {
  try {
    return { theme: "system", font: "serif", size: 18, width: 34, link: "#d4692a", header: "full", ...JSON.parse(localStorage.getItem("dewlab:texture") || "{}") };
  } catch {
    return { theme: "system", font: "serif", size: 18, width: 34, link: "#d4692a", header: "full" };
  }
}

/**
 * Save texture preferences to localStorage
 * @param {Object} state - Texture state to save
 */
function saveTexture(state) {
  try {
    localStorage.setItem("dewlab:texture", JSON.stringify(state));
  } catch {}
}

/**
 * Apply texture preferences to the document
 * @param {Object} state - Texture state
 */
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

/**
 * The replacement for native CSS `resize: horizontal` on a right-docked
 * panel — ported from tutorial-runtime.js's own copy (DECISIONS_LOG.md
 * 7.84). Native resize draws its handle at a box's own bottom-right
 * corner, which for a panel flush to the browser window's own right
 * edge sits exactly on that edge with no room to drag further right and
 * grow it. Adds a thin strip along `panel`'s left edge instead and
 * tracks a plain pointer drag on it directly.
 */
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

/**
 * Initialize the Settings panel
 */
function initSettings() {
  const state = loadTexture();
  applyTexture(state);

  const panel = document.getElementById("dl-settings");
  if (!panel) return state;

  makeRightEdgeResizable(panel, 256, 640); // matches .dl-settings' own min/max-width

  const toggle = document.getElementById("dl-settings-toggle");
  
  // Toggle button
  if (toggle) {
    toggle.addEventListener("click", () => {
      const isHidden = panel.hasAttribute("hidden");
      panel.toggleAttribute("hidden", !isHidden);
      toggle.setAttribute("aria-expanded", String(!isHidden));
      // Opening the panel is exactly when the engine/storage status lines
      // (Phase 6) are worth a fresh read — both are otherwise updated only
      // on state transitions, not continuously.
      if (isHidden) {
        updateExecutionStatus();
        updateStorageStatus();
      }
      // Settings and Help share one corner of the masthead; only one makes
      // sense open at a time, so opening either closes the other.
      closeHelpPanel();
    });
  }

  // Close button
  const closeBtn = document.getElementById("dl-settings-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      panel.setAttribute("hidden", "");
      if (toggle) {
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // Close on escape key
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (!panel.hasAttribute("hidden")) {
      panel.setAttribute("hidden", "");
      if (toggle) {
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    }
  });

  // Close on click outside
  document.addEventListener("click", (e) => {
    if (panel.hasAttribute("hidden")) return;
    if (panel.contains(e.target) || toggle?.contains(e.target)) return;
    panel.setAttribute("hidden", "");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  });

  // Hide empty sections
  for (const section of panel.querySelectorAll(".dl-settings-section")) {
    if (section.textContent.trim() === "") {
      section.hidden = true;
    }
  }

  // Initialize texture controls
  initTexture((isDark) => {
    cells.forEach(cell => {
      if (cell.editor) {
        try {
          setEditorTheme(cell.editor, isDark);
        } catch (e) {}
      }
    });
  });

  return state;
}

// Module-level so initSettings()'s toggle handler can reach it without
// initHelp() having to run first — both wire up during the same init()
// call, in an order that shouldn't matter.
let helpPanel;
let helpToggle;

/** Hides the Help panel, if it exists and is open — the reciprocal half
 * of Settings/Help closing each other on open, called from both. */
function closeHelpPanel() {
  if (!helpPanel || helpPanel.hasAttribute("hidden")) return;
  helpPanel.setAttribute("hidden", "");
  helpToggle?.setAttribute("aria-expanded", "false");
}

/**
 * Initialize the Help panel — the same "?" toggle, reopenable any time,
 * that compose/dewmini.js uses, ported here in place of the old
 * mini-ide-helper banner (shown once, dismissed permanently, and gone
 * for good once a reader had cells). Wired the same way initSettings()
 * wires #dl-settings, since the two panels share a corner and behave
 * the same way otherwise.
 */
function initHelp() {
  helpPanel = document.getElementById("mini-ide-help");
  if (!helpPanel) return;
  helpToggle = document.getElementById("mini-ide-help-toggle");

  makeRightEdgeResizable(helpPanel, 256, 640); // matches .mini-ide-panel's own min/max-width

  helpToggle?.addEventListener("click", () => {
    const isHidden = helpPanel.hasAttribute("hidden");
    helpPanel.toggleAttribute("hidden", !isHidden);
    helpToggle.setAttribute("aria-expanded", String(!isHidden));
    if (isHidden) {
      document.getElementById("dl-settings")?.setAttribute("hidden", "");
      document.getElementById("dl-settings-toggle")?.setAttribute("aria-expanded", "false");
    }
  });

  const closeBtn = document.getElementById("mini-ide-help-close");
  closeBtn?.addEventListener("click", () => {
    closeHelpPanel();
    helpToggle?.focus();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !helpPanel.hasAttribute("hidden")) {
      closeHelpPanel();
    }
  });

  document.addEventListener("click", (e) => {
    if (helpPanel.hasAttribute("hidden")) return;
    if (helpPanel.contains(e.target) || helpToggle?.contains(e.target)) return;
    closeHelpPanel();
  });
}

/**
 * Initialize texture controls
 * @param {Function} onThemeChange - Callback when theme changes
 * @returns {Object} Texture state
 */
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
      for (const btn of group.querySelectorAll("button")) {
        btn.setAttribute("aria-pressed", String(btn.dataset.value === current));
      }
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

  // Segment button groups
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

  // Range inputs
  if (sizeEl) {
    sizeEl.addEventListener("input", () => { 
      state.size = Number(sizeEl.value); 
      commit(); 
    });
  }
  
  if (widthEl) {
    widthEl.addEventListener("input", () => { 
      state.width = Number(widthEl.value); 
      commit(); 
    });
  }
  
  if (linkEl) {
    linkEl.addEventListener("input", () => { 
      state.link = linkEl.value; 
      commit(); 
    });
  }

  // Reset button
  const resetBtn = document.getElementById("dl-texture-reset");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      Object.assign(state, { theme: "system", font: "serif", size: 18, width: 34, link: "#d4692a", header: "full" });
      commit();
    });
  }

  // System theme change
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      if (state.theme === "system") onThemeChange(isDarkNow());
    });
  }

  sync();
  return state;
}

// ============================================================================
// Mini-IDE-specific Settings Sections
// ============================================================================

/**
 * Refresh the "Python" settings section — engine mode (worker vs.
 * main-thread fallback) and whether a genuine Stop is available. Called
 * on settings-panel open and after boot/restart, not continuously.
 */
function updateExecutionStatus() {
  const el = document.getElementById('settings-execution-status');
  if (!el) return;
  const mode = engine.engineMode();
  if (!mode) {
    el.textContent = 'Not started yet — run a cell to start Python.';
    return;
  }
  const where = mode === 'worker'
    ? 'a background worker, so the page stays responsive'
    : "the main thread (no background worker available here) — a runaway cell will freeze the page until it finishes";
  const stop = engine.canStop()
    ? 'Stop can genuinely interrupt a running cell.'
    : "Stop can't interrupt a running cell in this mode.";
  el.textContent = `Running in ${where}. ${stop}`;
}

/**
 * Refresh the "Files" settings section — active storage backend, and the
 * choose/reconnect-folder button's label and visibility.
 *
 * @async
 */
async function updateStorageStatus() {
  const statusEl = document.getElementById('settings-storage-status');
  const chooseBtn = document.getElementById('settings-choose-folder');
  const forgetBtn = document.getElementById('settings-forget-folder');
  if (!statusEl) return;

  const backend = fs.getBackend();
  const labels = {
    native: 'Using a real folder on your computer.',
    opfs: "Using this browser's private storage (fast; not visible in your file browser).",
    idbfs: "Using this browser's private storage (compatibility mode)."
  };
  statusEl.textContent = backend ? labels[backend] : 'Not started yet — run a cell to start Python.';

  if (chooseBtn) {
    const supported = typeof window.showDirectoryPicker === 'function';
    if (!supported || backend === 'native') {
      chooseBtn.hidden = true;
    } else {
      chooseBtn.hidden = false;
      const hasStored = await fs.hasStoredFolder();
      chooseBtn.textContent = hasStored ? 'Reconnect my folder' : 'Use a folder on my computer';
      chooseBtn.dataset.action = hasStored ? 'reconnect' : 'choose';
    }
  }
  if (forgetBtn) forgetBtn.hidden = backend !== 'native';
}

const IMPORT_MODE_KEY = 'mini-ide:import-mode';

/**
 * @returns {"replace"|"append"} what handleImportNotebookFile() should do
 *   with a newly imported notebook's cells relative to the current ones.
 */
function loadImportMode() {
  return localStorage.getItem(IMPORT_MODE_KEY) === 'append' ? 'append' : 'replace';
}

/** Wires the "On import" replace/append segmented control. */
function initImportModeSetting() {
  const group = document.querySelector('[data-import-mode]');
  if (!group) return;
  const buttons = Array.from(group.querySelectorAll('button'));

  function sync() {
    const mode = loadImportMode();
    buttons.forEach((btn) => btn.setAttribute('aria-pressed', String(btn.dataset.value === mode)));
  }

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      localStorage.setItem(IMPORT_MODE_KEY, btn.dataset.value);
      sync();
    });
  });

  sync();
}

/**
 * Wires the Python/Files/Import/Download settings sections added on top
 * of the shared #dl-settings panel (mini-ide.js:202-374's texture code is
 * the shared part; everything here is Mini-IDE-only).
 */
function initMiniIdeSettings() {
  initImportModeSetting();

  document.getElementById('settings-restart-python')?.addEventListener('click', async () => {
    if (!confirm('Restart Python? Anything defined in the current session will be lost.')) return;
    engine.restart();
    fs.reset();
    fsReady = false;
    updateStatus('Restarting Python…');
    updateExecutionStatus();
    updateStorageStatus();
    try {
      await ensureEngineAndFsReady();
      updateStatus('Python restarted.');
    } catch (error) {
      updateStatus(`Python failed to restart: ${error.message}`, 'error');
    }
    updateExecutionStatus();
    updateStorageStatus();
    renderFileTree();
  });

  document.getElementById('settings-choose-folder')?.addEventListener('click', async (e) => {
    const action = e.currentTarget.dataset.action || 'choose';
    try {
      if (action === 'reconnect') await fs.reconnectFolder();
      else await fs.chooseFolder();
      updateStatus('Now using a folder on your computer for files.');
    } catch (error) {
      updateStatus(`Couldn't use that folder: ${error.message}`, 'error');
    }
    updateStorageStatus();
    renderFileTree();
  });

  document.getElementById('settings-forget-folder')?.addEventListener('click', async () => {
    if (!confirm("Stop using that folder? Mini IDE switches back to this browser's private storage — nothing in the folder itself is deleted.")) return;
    await fs.forgetFolder();
    updateStatus('Stopped using that folder. Restart Python to switch storage.');
    updateStorageStatus();
  });

  // Fix: these three buttons existed in the markup with no listener.
  document.getElementById('settings-export-python')?.addEventListener('click', () => downloadAsPython());
  document.getElementById('settings-export-html')?.addEventListener('click', () => downloadAsHtml());
  document.getElementById('settings-export-ipynb')?.addEventListener('click', () => downloadAsIpynb());
  document.getElementById('settings-print-pdf')?.addEventListener('click', () => window.print());

  fs.configure({ onBackendChange: () => updateStorageStatus() });

  // Built-in worked examples — one listener for all four buttons, keyed
  // off the path/label already sitting in each button's own markup
  // rather than one hardcoded handler per example.
  for (const btn of document.querySelectorAll('#dl-settings-import [data-example]')) {
    btn.addEventListener('click', () => loadBuiltInExample(btn.dataset.example, btn.textContent.trim()));
  }
}

// ---------------------------------------------------------- filename

/**
 * Reads the reader's chosen filename from Settings, cleaned up for use
 * as an actual filename: any extension they typed is stripped (each
 * download function adds its own), and characters that aren't valid in
 * a filename on at least one common operating system (\ / : * ? " < >
 * |) are replaced with a dash — ported from compose/dewmini.js's own
 * getFilenameBase(), so the same input produces the same safe name on
 * both pages.
 *
 * @returns {string}
 */
function getFilenameBase() {
  const el = document.getElementById('mini-ide-filename');
  let name = (el?.value || '').trim();
  if (!name) name = 'mini-ide-notebook';
  name = name.replace(/\.(py|html?|ipynb)$/i, '');
  name = name.replace(/[\\/:*?"<>|]+/g, '-').trim();
  return name || 'mini-ide-notebook';
}

/**
 * Restores a previously chosen filename and keeps the browser tab
 * title in sync with it as the reader types — ported from
 * compose/dewmini.js's own initFilename().
 */
function initFilename() {
  const el = document.getElementById('mini-ide-filename');
  if (!el) return;
  let saved = 'mini-ide-notebook';
  try { saved = localStorage.getItem('mini-ide:filename') || saved; } catch {}
  el.value = saved;
  document.title = `${saved} — Mini IDE`;
  el.addEventListener('input', () => {
    try { localStorage.setItem('mini-ide:filename', el.value); } catch {}
    document.title = `${getFilenameBase()} — Mini IDE`;
  });
}

// ------------------------------------------------------------- notes

/**
 * Wires the Settings "Your notes" textarea — free-text notes saved
 * alongside cells rather than as one more cell, so clearing all cells
 * or restoring a version never touches them. Ported from
 * compose/dewmini.js's own initNotes(). Saved on every keystroke
 * rather than debounced: a note is short enough that the write is
 * free, and a debounce risks losing the last few characters if the
 * panel closes or the page navigates before it fires.
 */
function initMiniIdeNotes() {
  const notesEl = document.getElementById('mini-ide-notes');
  if (!notesEl) return;
  try { notesEl.value = localStorage.getItem('mini-ide:notes') || ''; } catch {}
  notesEl.addEventListener('input', () => {
    try { localStorage.setItem('mini-ide:notes', notesEl.value); } catch {}
  });
}

// ---------------------------------------------------------- run stats

/**
 * Wires the Settings "Run time" on/off toggle in #dl-settings-execution.
 * Same minimal load→apply→sync pattern as the texture/editor settings,
 * scaled down to one setting: applied as a data-mini-ide-runstats
 * attribute on <html> (read by renderCellRunStats()), and re-painted on
 * every already-rendered cell immediately on toggle, not just future runs.
 */
function initRunStatsSetting() {
  let show = true;
  try { show = localStorage.getItem('mini-ide:show-run-stats') !== 'off'; } catch {}

  function apply() {
    document.documentElement.setAttribute('data-mini-ide-runstats', show ? 'on' : 'off');
    cells.forEach(renderCellRunStats);
  }
  apply();

  const group = document.querySelector('#dl-settings-execution .dl-seg[data-mini-ide="runstats"]');
  if (!group) return;
  const sync = () => {
    for (const btn of group.querySelectorAll('button')) {
      btn.setAttribute('aria-pressed', String(btn.dataset.value === (show ? 'on' : 'off')));
    }
  };
  group.addEventListener('click', (ev) => {
    const btn = ev.target.closest('button');
    if (!btn) return;
    show = btn.dataset.value === 'on';
    try { localStorage.setItem('mini-ide:show-run-stats', show ? 'on' : 'off'); } catch {}
    apply();
    sync();
  });
  sync();
}

// -------------------------------------------------- editor appearance

const MINI_IDE_EDITOR_DEFAULTS = { codeSize: 15, density: 'cozy', cursor: 'medium', gutter: 'on', activeLine: 'on' };
const MINI_IDE_EDITOR_KEY_MAP = { density: 'density', cursor: 'cursor', gutter: 'gutter', activeline: 'activeLine' };

function loadMiniIdeEditorPrefs() {
  try {
    return { ...MINI_IDE_EDITOR_DEFAULTS, ...JSON.parse(localStorage.getItem('mini-ide:editor') || '{}') };
  } catch {
    return { ...MINI_IDE_EDITOR_DEFAULTS };
  }
}

function saveMiniIdeEditorPrefs(state) {
  try { localStorage.setItem('mini-ide:editor', JSON.stringify(state)); } catch {}
}

function applyMiniIdeEditorPrefs(state) {
  const root = document.documentElement;
  root.style.setProperty('--mini-ide-code-size', `${state.codeSize}px`);
  root.setAttribute('data-mini-ide-density', state.density);
  root.setAttribute('data-mini-ide-cursor', state.cursor);
  if (state.gutter === 'off') root.setAttribute('data-mini-ide-gutter', 'off'); else root.removeAttribute('data-mini-ide-gutter');
  if (state.activeLine === 'off') root.setAttribute('data-mini-ide-activeline', 'off'); else root.removeAttribute('data-mini-ide-activeline');
}

/**
 * Wires the Settings "Editor" section — code size, cell spacing, cursor
 * width, line numbers, and active-line highlight. Ported from
 * compose/dewmini.js's own initEditorSettings(): purely a CSS-variable
 * and data-attribute affair (see the :root[data-mini-ide-*] rules in
 * mini-ide-style.css), so nothing here touches createCodeEditor()'s own
 * options — every open cell picks up a change immediately because
 * they're all reading the same handful of :root-scoped values.
 */
function initMiniIdeEditorSettings() {
  const state = loadMiniIdeEditorPrefs();
  applyMiniIdeEditorPrefs(state);

  const panel = document.getElementById('dl-settings-editor');
  if (!panel) return state;

  const sizeEl = document.getElementById('mini-ide-code-size');

  function sync() {
    for (const group of panel.querySelectorAll('.dl-seg')) {
      const stateKey = MINI_IDE_EDITOR_KEY_MAP[group.dataset.miniIde];
      const current = state[stateKey];
      for (const btn of group.querySelectorAll('button')) btn.setAttribute('aria-pressed', String(btn.dataset.value === current));
    }
    if (sizeEl) sizeEl.value = state.codeSize;
  }

  function commit() {
    applyMiniIdeEditorPrefs(state);
    saveMiniIdeEditorPrefs(state);
    sync();
  }

  for (const group of panel.querySelectorAll('.dl-seg')) {
    group.addEventListener('click', (ev) => {
      const btn = ev.target.closest('button');
      if (!btn) return;
      state[MINI_IDE_EDITOR_KEY_MAP[group.dataset.miniIde]] = btn.dataset.value;
      commit();
    });
  }
  sizeEl?.addEventListener('input', () => { state.codeSize = Number(sizeEl.value); commit(); });
  document.getElementById('mini-ide-editor-reset')?.addEventListener('click', () => { Object.assign(state, MINI_IDE_EDITOR_DEFAULTS); commit(); });

  sync();
  return state;
}

/**
 * Remembers which of Settings/Help a reader left open, the same
 * localStorage-persisted-sidebar mechanism tutorial pages use (see
 * saveSidebarState()/restoreSidebarState() in tutorial-runtime.js,
 * DECISIONS_LOG.md 7.83) — a returning reader's panel comes back open
 * rather than needing to be reopened, since it's meant to be a
 * permanent pane, not a popover that happens to be open right now.
 * Mini IDE only ever has one of the two open at a time (both dock to
 * the same right edge), so this stores a single value rather than the
 * tutorial pages' {left, right} pair.
 */
function saveSidebarState() {
  const settingsPanel = document.getElementById('dl-settings');
  const helpPanel = document.getElementById('mini-ide-help');
  const open = settingsPanel && !settingsPanel.hasAttribute('hidden') ? 'settings'
    : helpPanel && !helpPanel.hasAttribute('hidden') ? 'help'
    : null;
  try {
    localStorage.setItem('dewlab:mini-ide:sidebar', JSON.stringify({ open }));
  } catch (e) { /* private mode, blocked storage: nothing to remember */ }
}

/** The other half of saveSidebarState() — reopens whatever was left open
 * last time by clicking its toggle, reusing that toggle's own open logic
 * rather than duplicating it. Skipped below the phone breakpoint, where
 * a panel is a bottom sheet covering most of the screen rather than a
 * sidebar worth leaving open by default. */
function restoreSidebarState() {
  if (!window.matchMedia('(min-width: 34rem)').matches) return;
  let state;
  try {
    state = JSON.parse(localStorage.getItem('dewlab:mini-ide:sidebar') || '{}');
  } catch (e) {
    return;
  }
  const toggleId = state.open === 'settings' ? 'dl-settings-toggle'
    : state.open === 'help' ? 'mini-ide-help-toggle'
    : null;
  if (toggleId) document.getElementById(toggleId)?.click();
}

/**
 * Keeps `<html data-dl-panel-open>` in sync with whether the Settings or
 * Help panel is currently visible, regardless of which of their several
 * open/close paths (toggle click, close button, Escape, click-outside)
 * fired — a MutationObserver on each panel's `hidden` attribute, rather
 * than hooking every call site, so this stays correct even if a future
 * change adds another way to close one. mini-ide-style.css reads the
 * attribute to shrink `.mini-ide-workspace` on wide-enough viewports
 * while a panel is open, so its fixed position (tutorial-style.css's
 * `.dl-settings`/`.mini-ide-panel`) never ends up covering a cell's own
 * run/reset/delete buttons or its output.
 *
 * A ResizeObserver on the same panels keeps --dl-panel-w in step with
 * whichever one is actually open's *real* rendered width, not a guess —
 * a docked sidebar can be dragged wider or narrower via its own resize
 * handle at any time, the same reasoning tutorial-runtime.js's own
 * watchPanelOverlap() ResizeObserver has (DECISIONS_LOG.md 7.83).
 */
function watchPanelOverlap() {
  const panels = [document.getElementById('dl-settings'), document.getElementById('mini-ide-help')]
    .filter(Boolean);
  if (!panels.length) return;
  const sync = () => {
    const anyOpen = panels.some(p => !p.hasAttribute('hidden'));
    document.documentElement.toggleAttribute('data-dl-panel-open', anyOpen);
    saveSidebarState();
  };
  for (const panel of panels) {
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ['hidden'] });
  }
  // Only the DOM attribute, not a persisted-state write: every panel is
  // still hidden at this point in startup, before restoreSidebarState()
  // (called right after this) has had a chance to reopen whatever was
  // actually saved last time — persisting here would overwrite a real
  // saved preference with "everything closed" on every single load.
  document.documentElement.toggleAttribute('data-dl-panel-open', panels.some(p => !p.hasAttribute('hidden')));

  const widthObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      const panel = entry.target;
      if (panel.hasAttribute('hidden')) continue;
      // offsetWidth, not the observer's own contentRect: the margin
      // needs to clear the panel's full border box (border + padding),
      // plus a small gutter so text doesn't sit flush against its edge.
      document.documentElement.style.setProperty('--dl-panel-w', `${panel.offsetWidth + 16}px`);
    }
  });
  for (const panel of panels) widthObserver.observe(panel);
}

/**
 * Track the chrome height for proper positioning
 * Same as tutorial-runtime.js
 */
function trackChromeHeight() {
  const chrome = document.getElementById("dl-chrome");
  if (!chrome) return;

  const publish = () => {
    document.documentElement.style.setProperty(
      "--dl-chrome-h", `${Math.round(chrome.getBoundingClientRect().height)}px`
    );
  };
  publish();

  if (typeof ResizeObserver === "function") {
    new ResizeObserver(publish).observe(chrome);
  } else {
    window.addEventListener("resize", publish);
  }
}

// ============================================================================
// Initialization
// ============================================================================

/**
 * Initialize the Mini IDE
 * Sets up DOM references, loads saved state, and renders the UI
 *
 * @async
 * @function init
 */
async function init() {
  // Get DOM elements
  cellsContainer = document.getElementById('cells-container');
  addPythonBtn = document.getElementById('add-python-cell');
  addTextBtn = document.getElementById('add-text-cell');
  loadExampleBtn = document.getElementById('load-example-cells');
  runAllBtn = document.getElementById('run-all');
  clearOutputBtn = document.getElementById('clear-output');
  clearAllBtn = document.getElementById('clear-all');
  statusEl = document.getElementById('mini-ide-status');
  sampleNoticeEl = document.getElementById('sample-cells-notice');
  removeSampleBtn = document.getElementById('remove-sample-cells');
  filetreeEl = document.getElementById('mini-ide-filetree');
  filetreeToggleBtn = document.getElementById('filetree-toggle');
  filetreeRefreshBtn = document.getElementById('filetree-refresh');
  filetreeListEl = document.getElementById('filetree-list');
  filetreeNoteEl = document.getElementById('filetree-note');
  filetreeUploadBtn = document.getElementById('filetree-upload');
  filetreeUploadInput = document.getElementById('filetree-upload-file');
  importNotebookBtn = document.getElementById('import-notebook');
  importNotebookInput = document.getElementById('import-notebook-file');
  importCompatNoticeEl = document.getElementById('import-compat-notice');
  importCompatListEl = document.getElementById('import-compat-list');
  dismissImportCompatBtn = document.getElementById('dismiss-import-compat');
  dismissImportCompatBtn?.addEventListener('click', () => {
    if (importCompatNoticeEl) importCompatNoticeEl.hidden = true;
  });

  // Wire the engine to this page's cells before anything can run
  engine.configure({
    getOutputEl: (cellId) => {
      const cell = cells.find(c => c.id === cellId);
      return cell ? cell.outputEl : null;
    },
    onStatus: (text, kind) => updateStatus(text, kind)
  });

  // Load saved state
  loadSavedState();

  // Check if we have sample cells
  hasSampleCells = cells.length > 0 && cells.every(cell => cell.isSample);
  if (hasSampleCells && sampleNoticeEl) {
    sampleNoticeEl.hidden = false;
  }

  // Initialize Settings panel
  initSettings();
  initMiniIdeSettings();
  initMiniIdeEditorSettings();
  initRunStatsSetting();
  initMiniIdeNotes();
  initFilename();
  initHelp();
  watchPanelOverlap();
  restoreSidebarState();

  // Setup event listeners
  setupEventListeners();

  // Setup drag and drop
  setupDragAndDrop();

  // Render cells
  renderCells();

  // Update status
  updateStatus('Ready. Add cells to begin.');
  
  // Track chrome height like tutorial pages
  trackChromeHeight();
}

/**
 * Load saved state from localStorage
 * Validates and sanitizes loaded data
 *
 * A notebook with nothing saved starts genuinely empty now, rather than
 * auto-seeding the example cells every time — that used to mean Clear
 * All never actually stayed empty across a reload, and buried the one
 * way back to the example (a toolbar "Remove Sample Cells" button, gone
 * the moment a reader edited anything) with no way to ask for it again.
 * loadExampleCells() (wired to the toolbar's own "Load example" button)
 * is that one way back in now, available any time rather than once.
 *
 * @function loadSavedState
 */
function loadSavedState() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      cells = JSON.parse(saved);
      // Validate cells - ensure each has required fields and valid type
      cells = cells.filter(cell =>
        cell &&
        cell.id &&
        typeof cell.id === 'string' &&
        [CELL_TYPES.PYTHON, CELL_TYPES.TEXT].includes(cell.type)
      );
    } catch (e) {
      console.error('Failed to load saved state:', e);
      cells = [];
    }
  }
}

/**
 * Create sample cells to demonstrate the Mini IDE
 * @returns {Array<Object>} Array of sample cell objects
 */
function createSampleCells() {
  return [
    createNewCell(
      CELL_TYPES.PYTHON, 
      '# Sample Cell 1: Basic Python\n# Click "Run" to execute this cell\nprint("Hello from dewlab Mini IDE!")\nx = 42\nprint(f"The answer is: {x}")',
      true
    ),
    createNewCell(
      CELL_TYPES.PYTHON,
      '# Sample Cell 2: Using numpy\n# The Mini IDE has numpy, pandas, and matplotlib pre-loaded\nimport numpy as np\narr = np.array([1, 2, 3, 4, 5])\nprint(f"Sum: {arr.sum()}")\nprint(f"Mean: {arr.mean()}")',
      true
    ),
    createNewCell(
      CELL_TYPES.TEXT,
      '# Sample Text Cell\n\nThis is a **text cell** for documentation.\n\n- You can write markdown-style text\n- Use it for comments, explanations, or notes\n- Text cells don\'t execute code',
      true
    ),
    createNewCell(
      CELL_TYPES.PYTHON,
      '# Sample Cell 3: Visualization\n# Cells share a common namespace\n# So we can use the x variable from Cell 1\nimport matplotlib.pyplot as plt\nplt.plot([1, 2, 3, 4], [1, 4, 9, 16])\nplt.title("Sample Plot")\nplt.xlabel("X")\nplt.ylabel("Y")\nplt.show()',
      true
    )
  ];
}

/**
 * Replaces the current cells with the worked example — what the
 * toolbar's "Load example" button calls. Asks first if that would
 * throw away real work; doesn't bother when the notebook is already
 * empty, since there's nothing to lose.
 *
 * @function loadExampleCells
 */
function loadExampleCells() {
  if (cells.length && !confirm("Replace the current cells with the example? This can't be undone.")) return;
  cells = createSampleCells();
  hasSampleCells = true;
  saveState();
  renderCells();
  if (sampleNoticeEl) sampleNoticeEl.hidden = false;
  updateStatus('Example loaded.');
}

/**
 * Save state to localStorage
 * Persists all cells and their content
 *
 * @function saveState
 */
function saveState() {
  // An explicit allow-list, not JSON.stringify(cells) directly: a rendered
  // cell also carries .editor (CodeMirror), .textarea, .outputEl, and
  // .runBtn — live DOM/editor references whose own property graphs contain
  // real cycles (a DOM node's parentNode/childNodes, CodeMirror's internal
  // extension bookkeeping), which JSON.stringify throws on rather than
  // silently dropping.
  const serializable = cells.map(cell => ({
    id: cell.id,
    type: cell.type,
    content: cell.content,
    output: cell.output || '',
    hasError: Boolean(cell.hasError),
    isSample: Boolean(cell.isSample),
    lastRunMs: typeof cell.lastRunMs === 'number' ? cell.lastRunMs : undefined
  }));
  localStorage.setItem(STORAGE_KEY, JSON.stringify(serializable));
}

// ============================================================================
// Event Listeners
//
// Most of the click handlers below share the same small pattern: change
// `cells` (add, remove, or clear entries), mark `hasSampleCells` as
// false if the change means the notebook is no longer "just the
// starter samples," call `saveState()` so localStorage matches the new
// `cells` array, then call `renderCells()` so the page's DOM matches
// `cells` too. Keeping those two calls right next to every change (never
// changing `cells` without also calling both) is what keeps "what's on
// screen," "what's in memory," and "what's saved" from ever quietly
// drifting apart from each other.
// ============================================================================

/**
 * Setup all event listeners for buttons and UI interactions
 *
 * @function setupEventListeners
 */
function setupEventListeners() {
  // Add cell buttons — append at the very end, via the same
  // insertCellAt() the in-between dividers use.
  addPythonBtn?.addEventListener('click', () => insertCellAt(cells.length, CELL_TYPES.PYTHON));
  addTextBtn?.addEventListener('click', () => insertCellAt(cells.length, CELL_TYPES.TEXT));
  loadExampleBtn?.addEventListener('click', loadExampleCells);

  // Run all cells
  runAllBtn?.addEventListener('click', () => {
    runAllCells();
  });

  // Clear every cell's output, keeping the cells and their code —
  // non-destructive, so no confirmation dialog (unlike Clear All below).
  clearOutputBtn?.addEventListener('click', clearAllOutputs);

  // Clear all cells with confirmation
  clearAllBtn?.addEventListener('click', () => {
    if (confirm('Are you sure you want to clear all cells? This cannot be undone.')) {
      cells = [];
      hasSampleCells = false;
      saveState();
      renderCells();
      if (sampleNoticeEl) sampleNoticeEl.hidden = true;
      updateStatus('All cells cleared.');
    }
  });

  // File tree pane: mobile show/hide toggle + manual refresh
  filetreeToggleBtn?.addEventListener('click', () => {
    const open = filetreeEl?.classList.toggle('mini-ide-filetree-open');
    filetreeToggleBtn.setAttribute('aria-expanded', String(Boolean(open)));
  });
  filetreeRefreshBtn?.addEventListener('click', () => renderFileTree());

  // File tree pane: upload via button or drag-and-drop
  filetreeUploadBtn?.addEventListener('click', () => filetreeUploadInput?.click());
  filetreeUploadInput?.addEventListener('change', (e) => {
    uploadFiles(e.target.files);
    e.target.value = '';
  });
  if (filetreeEl) {
    filetreeEl.addEventListener('dragover', (e) => {
      e.preventDefault();
      filetreeEl.classList.add('mini-ide-filetree-dragover');
    });
    filetreeEl.addEventListener('dragleave', () => {
      filetreeEl.classList.remove('mini-ide-filetree-dragover');
    });
    filetreeEl.addEventListener('drop', (e) => {
      e.preventDefault();
      filetreeEl.classList.remove('mini-ide-filetree-dragover');
      uploadFiles(e.dataTransfer?.files);
    });
  }

  // Import a .ipynb or .py file as this notebook's cells
  importNotebookBtn?.addEventListener('click', () => importNotebookInput?.click());
  importNotebookInput?.addEventListener('change', handleImportNotebookFile);

  // Remove sample cells button
  removeSampleBtn?.addEventListener('click', () => {
    cells = [];
    hasSampleCells = false;
    saveState();
    renderCells();
    if (sampleNoticeEl) sampleNoticeEl.hidden = true;
    updateStatus('Sample cells removed. Add your own cells to begin.');
  });

  // Observe theme changes from Settings panel
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'data-theme') {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        cells.forEach(cell => {
          if (cell.editor) {
            try {
              setEditorTheme(cell.editor, isDark);
            } catch (e) {}
          }
        });
      }
    });
  });
  observer.observe(document.documentElement, { attributes: true });
}

// ============================================================================
// Cell Management
//
// Functions in this section deal with cells as plain data: creating one,
// giving it an ID, choosing default starter content, and rendering the
// whole `cells` array into DOM elements a person can actually see and
// click. Running a cell's code is a separate concern, handled by the
// next section ("Cell Execution") — a cell can exist, be edited, and be
// reordered without Python ever being involved.
// ============================================================================

/**
 * Create a new cell object with default values
 *
 * @param {string} type - Cell type (CELL_TYPES.PYTHON or CELL_TYPES.TEXT)
 * @param {string} [content=''] - Initial cell content
 * @param {boolean} [isSample=false] - Whether this is a sample cell
 * @param {string} [id] - Unique cell ID (auto-generated if not provided)
 * @returns {Object} Cell object
 */
function createNewCell(type, content = '', isSample = false, id = generateId()) {
  return {
    id,
    type,
    content: content || getDefaultContent(type),
    output: '',
    hasError: false,
    isSample
  };
}

/**
 * Inserts a new, empty cell at a specific position — what both the
 * toolbar's "Python Cell"/"Text Cell" buttons (index = cells.length,
 * an append) and the insert-here dividers between cells (any other
 * index) call. Ported from compose/dewmini.js's own insertCellAt(),
 * which follows the same update-array/save/re-render/focus pattern
 * every function in this file that changes `cells` already uses.
 *
 * @param {number} index - Position in `cells` to insert at
 * @param {string} type - Cell type (CELL_TYPES.PYTHON or CELL_TYPES.TEXT)
 * @param {string} [content=''] - Initial cell content
 */
function insertCellAt(index, type, content = '') {
  const cell = createNewCell(type, content);
  cells.splice(index, 0, cell);
  hasSampleCells = false;
  saveState();
  renderCells();
  focusCell(cell.id);
  updateStatus(`${type === CELL_TYPES.PYTHON ? 'Python' : 'Text'} cell added.`);
  if (sampleNoticeEl) sampleNoticeEl.hidden = true;
}

/**
 * Get default content for a cell type
 *
 * @param {string} type - Cell type
 * @returns {string} Default content
 */
function getDefaultContent(type) {
  if (type === CELL_TYPES.PYTHON) {
    return '# Start coding here\nprint("Hello, World!")';
  }
  // Genuinely blank, not a boilerplate placeholder: a text cell with
  // content immediately renders (showRendered() in createCellElement()),
  // and a freshly added cell whose first line has to be clicked away
  // before typing is worse than an empty textarea with its own
  // placeholder text doing the same explaining.
  return '';
}

/**
 * Generate a unique cell ID.
 *
 * Combines the current time (`Date.now()`, milliseconds since 1970) with
 * a short random string, so two cells created in the same session never
 * collide — even one created in the very same millisecond as another
 * still gets a different random suffix.
 * `Math.random().toString(36)` turns a random 0-1 number into a
 * base-36 string (digits 0-9 plus letters a-z), which packs more
 * randomness into fewer characters than a decimal string would;
 * `.substr(2, 9)` drops the leading "0." that toString() always
 * produces and keeps 9 of the remaining characters.
 *
 * This ID isn't shown to a student anywhere — it only exists so code in
 * this file can find "the cell with this exact ID" again later (in
 * `cells.find(c => c.id === cellId)`, used throughout this file), even
 * after the array has been reordered by dragging.
 *
 * @returns {string} Unique cell ID
 */
function generateId() {
  return `cell-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Render all cells into the DOM, with an insert-here divider before the
 * first cell, between every pair, and after the last — ported from
 * compose/dewmini.js's own renderCells(). No dividers over an empty
 * notebook: the toolbar's own "Python Cell"/"Text Cell" buttons are the
 * one way in until there's at least one cell to insert around.
 *
 * @function renderCells
 */
function renderCells() {
  if (!cellsContainer) return;

  cellsContainer.innerHTML = '';

  if (cells.length) {
    cellsContainer.appendChild(createInsertDivider(0));
    cells.forEach((cell, index) => {
      cellsContainer.appendChild(createCellElement(cell, index));
      cellsContainer.appendChild(createInsertDivider(index + 1));
    });
  }

  // Show/hide sample notice based on whether we have sample cells
  if (sampleNoticeEl) {
    hasSampleCells = cells.length > 0 && cells.every(cell => cell.isSample);
    sampleNoticeEl.hidden = !hasSampleCells;
  }
}

/**
 * A tappable seam between cells (and before the first, after the last)
 * rather than only a toolbar at the top — the fast way to build a
 * notebook is inserting where you're already looking, not scrolling
 * back up after appending at the end. Ported from compose/dewmini.js's
 * own createInsertDivider(): full-height and always visible without
 * hover on a touch device, since hover isn't a thing to reveal it with
 * there (see the `@media (hover: none)` rule in mini-ide-style.css).
 *
 * @param {number} index - Position `insertCellAt()` should insert at
 * @returns {HTMLElement} The divider element
 */
function createInsertDivider(index) {
  const row = document.createElement('div');
  row.className = 'mini-ide-insert';

  const line = document.createElement('div');
  line.className = 'mini-ide-insert-line';

  const actions = document.createElement('div');
  actions.className = 'mini-ide-insert-actions';

  const addPy = document.createElement('button');
  addPy.type = 'button';
  addPy.className = 'mini-ide-insert-btn';
  addPy.title = 'Insert a Python cell here';
  addPy.innerHTML = '<span class="mini-ide-icon mini-ide-icon-python" aria-hidden="true"></span>Python';
  addPy.addEventListener('click', () => insertCellAt(index, CELL_TYPES.PYTHON));

  const addTxt = document.createElement('button');
  addTxt.type = 'button';
  addTxt.className = 'mini-ide-insert-btn';
  addTxt.title = 'Insert a text cell here';
  addTxt.innerHTML = '<span class="mini-ide-icon mini-ide-icon-text" aria-hidden="true"></span>Text';
  addTxt.addEventListener('click', () => insertCellAt(index, CELL_TYPES.TEXT));

  actions.append(addPy, addTxt);
  row.append(line, actions);
  return row;
}

/**
 * Create a cell DOM element with editor and controls
 *
 * A learning note on a real bug this exact function used to cause: it
 * attaches live references — `cell.runBtn`, `cell.editor`,
 * `cell.textarea`, `cell.outputEl` — directly onto the plain `cell`
 * object that also lives in the `cells` array. That's convenient (any
 * code holding a `cell` can reach its own DOM elements straight away),
 * but it means `cell` is no longer *just* data — it's data mixed with
 * live browser objects. Those DOM/editor objects contain their own
 * circular references internally (a DOM node's `parentNode` points back
 * up the tree it's already part of), which broke `JSON.stringify(cells)`
 * with a "Converting circular structure to JSON" error the moment any
 * cell had actually been rendered — see `saveState()`'s own comment for
 * how that got fixed (an explicit list of only the plain-data fields to
 * save, instead of saving `cells` directly). The general lesson: mixing
 * "data you want to serialize" with "live objects you don't" on the same
 * object works until the moment you try to serialize it, and the bug it
 * causes then can look unrelated to where the mixing happened.
 *
 * @param {Object} cell - Cell object
 * @param {number} index - Cell index
 * @returns {HTMLElement} Cell DOM element
 */
function createCellElement(cell, index) {
  const cellEl = document.createElement('div');
  cellEl.className = `mini-ide-cell mini-ide-cell-${cell.type}`;
  cellEl.dataset.index = index;
  cellEl.dataset.id = cell.id;

  // Add error class if the cell's last run raised
  if (cell.hasError) {
    cellEl.classList.add('error');
  }

  // A quiet coloured rail beside the cell rather than a boxed card —
  // ported from compose/dewmini.js's own dm-cell-rail — plus a "main"
  // column holding the header, editor, and output. The rail is a
  // sibling of main, not a child, so mini-ide-style.css can lay them
  // out side by side with plain flexbox.
  const rail = document.createElement('div');
  rail.className = 'mini-ide-cell-rail';

  const main = document.createElement('div');
  main.className = 'mini-ide-cell-main';

  // Cell head: a small pill naming the type, a spacer, and icon-only
  // actions — dragging the head (not the whole cell) reorders it.
  const head = document.createElement('div');
  head.className = 'mini-ide-cell-head';
  head.draggable = true;
  head.dataset.id = cell.id;

  const pill = document.createElement('span');
  pill.className = 'mini-ide-cell-pill';
  pill.textContent = cell.type === CELL_TYPES.PYTHON ? 'Python' : 'Text';

  const spacer = document.createElement('span');
  spacer.className = 'mini-ide-cell-spacer';

  const actions = document.createElement('div');
  actions.className = 'mini-ide-cell-actions';

  // Run button (only for Python cells) — an icon-only ▶, matching
  // compose/dewmini.js's own dm-icon-run. setRunButtonRunning()/
  // resetRunButton() swap its glyph and title between idle and
  // running/stoppable states.
  const runBtn = document.createElement('button');
  runBtn.type = 'button';
  runBtn.className = 'mini-ide-icon-btn mini-ide-icon-run';
  runBtn.title = 'Run this cell (Shift+Enter)';
  runBtn.textContent = '▶';
  runBtn.style.display = cell.type === CELL_TYPES.PYTHON ? 'inline-flex' : 'none';
  runBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    runCell(cell.id);
  });

  // Edit/View toggle (only for text cells) — filled in by the text-cell
  // branch below, once showEditor()/showRendered() exist to keep its
  // label in sync. Built here, alongside Run, so it sits in the same
  // header row regardless of which branch runs.
  const previewBtn = document.createElement('button');
  previewBtn.type = 'button';
  previewBtn.className = 'mini-ide-icon-btn mini-ide-icon-preview';
  previewBtn.style.display = cell.type === CELL_TYPES.TEXT ? 'inline-flex' : 'none';

  // Reset-output button (only for Python cells) — clears this cell's
  // own output without touching its code, distinct from the toolbar's
  // destructive "Clear All" (which deletes every cell outright).
  const resetOutputBtn = document.createElement('button');
  resetOutputBtn.type = 'button';
  resetOutputBtn.className = 'mini-ide-icon-btn mini-ide-icon-reset-output';
  resetOutputBtn.title = "Clear this cell's output";
  resetOutputBtn.textContent = '↺';
  resetOutputBtn.style.display = cell.type === CELL_TYPES.PYTHON ? 'inline-flex' : 'none';
  resetOutputBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    resetCellOutput(cell.id);
  });

  // Delete button — an icon-only ×, matching dm-icon-delete. Arm-then-
  // confirm rather than a native confirm() dialog: a dialog stops the
  // whole page and needs a mouse trip to its own button, where this
  // just needs a second, deliberate press of the same one.
  const deleteBtn = document.createElement('button');
  deleteBtn.type = 'button';
  deleteBtn.className = 'mini-ide-icon-btn mini-ide-icon-delete';
  deleteBtn.title = 'Delete this cell';
  deleteBtn.textContent = '×';
  deleteBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    armDeleteButton(deleteBtn, () => deleteCell(cell.id));
  });

  actions.appendChild(runBtn);
  actions.appendChild(resetOutputBtn);
  actions.appendChild(previewBtn);
  actions.appendChild(deleteBtn);
  head.append(pill, spacer, actions);

  // Store the Run button reference so runCell() can toggle it to Stop
  cell.runBtn = runBtn;

  // Cell content area
  const contentEl = document.createElement('div');
  contentEl.className = 'mini-ide-cell-content';

  if (cell.type === CELL_TYPES.PYTHON) {
    // Python cell: use CodeMirror editor
    const editorEl = document.createElement('div');
    editorEl.className = 'mini-ide-editor';
    contentEl.appendChild(editorEl);

    // Initialize CodeMirror with Jedi support
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const editor = createCodeEditor(editorEl, cell.content, {
      dark: isDark,
      onChange: (newContent) => {
        const idx = cells.findIndex(c => c.id === cell.id);
        if (idx !== -1) {
          cells[idx].content = newContent;
          cells[idx].isSample = false;
          hasSampleCells = cells.length > 0 && cells.every(c => c.isSample);
          saveState();
          if (sampleNoticeEl) sampleNoticeEl.hidden = !hasSampleCells;
        }
      },
      completeNames: engine.pageNamesCompletion,
      getDoc: engine.hoverDoc,
      getSignature: engine.signatureHelp
    });

    // Capture phase: CodeMirror's own handler sees Enter first on bubble,
    // so intercepting Shift+Enter has to happen before that, not after.
    editorEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && e.shiftKey) { e.preventDefault(); e.stopPropagation(); runCell(cell.id); }
    }, true);

    // Store editor reference on cell for later access
    cell.editor = editor;
  } else {
    // Text cell: a textarea that turns into rendered notes — the same
    // .dl-doc-editor/.dl-doc-render shape and renderDocMarkdown() as
    // compose/dewmini.js and tutorial-runtime.js's own text cells (both
    // stylesheets are already loaded here), so a text cell looks and
    // behaves the same no matter which of dewlab's three cell surfaces a
    // reader happens to be using.
    const textarea = document.createElement('textarea');
    textarea.className = 'dl-doc-editor';
    textarea.placeholder = 'Notes… (# heading, **bold**, - bullets)';
    textarea.value = cell.content;

    const renderEl = document.createElement('div');
    renderEl.className = 'dl-doc-render';
    renderEl.tabIndex = 0;
    renderEl.hidden = true;

    const syncPreviewBtn = () => {
      const editing = !textarea.hidden;
      previewBtn.textContent = editing ? 'View' : 'Edit';
      previewBtn.title = editing ? 'Show this note rendered' : 'Edit this note';
    };
    const showEditor = () => {
      textarea.hidden = false;
      renderEl.hidden = true;
      syncPreviewBtn();
    };
    const showRendered = () => {
      if (!textarea.value.trim()) return; // nothing to render — keep it open for typing
      renderEl.innerHTML = renderDocMarkdown(textarea.value);
      renderEl.hidden = false;
      textarea.hidden = true;
      syncPreviewBtn();
    };

    textarea.addEventListener('input', (e) => {
      const idx = cells.findIndex(c => c.id === cell.id);
      if (idx !== -1) {
        cells[idx].content = e.target.value;
        cells[idx].isSample = false;
        hasSampleCells = cells.length > 0 && cells.every(c => c.isSample);
        saveState();
        if (sampleNoticeEl) sampleNoticeEl.hidden = !hasSampleCells;
      }
    });
    textarea.addEventListener('blur', showRendered);
    renderEl.addEventListener('click', showEditor);
    renderEl.addEventListener('keydown', (e) => { if (e.key === 'Enter') showEditor(); });
    // mousedown, not click: a click while the textarea is focused blurs
    // it first (firing showRendered() above), and only then reaches this
    // handler — by which point textarea.hidden already flipped, so
    // reading it here would toggle straight back to editing. preventing
    // the blur on mousedown keeps the state this handler sees accurate.
    previewBtn.addEventListener('mousedown', (e) => e.preventDefault());
    previewBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (textarea.hidden) showEditor(); else showRendered();
    });

    contentEl.append(textarea, renderEl);
    cell.textarea = textarea;
    cell.showTextEditor = showEditor;

    if (cell.content.trim()) showRendered();
    else syncPreviewBtn();
  }

  // Cell output area — repopulated from the last run's rendered markup,
  // which already includes any traceback tutorial_tools.py produced.
  const outputEl = document.createElement('div');
  outputEl.className = 'mini-ide-cell-output';
  // Left empty (rather than tagged with a static "empty" class) on
  // purpose: the CSS hides it via :empty, which keeps working after a
  // later run appends real output — a class set once here and never
  // cleared would hide every cell's output forever after its first run.
  if (cell.output) {
    outputEl.innerHTML = cell.output;
  }
  cell.outputEl = outputEl;

  // Run stats — how long the last run took. Hidden by both a Settings
  // toggle (data-mini-ide-runstats="off" on the root) and, same as the
  // output area above, actual emptiness: nothing is written here until
  // a cell has actually run once. Text only, never a live timer — a
  // cell already shows it's running via its Run→Stop button.
  const statsEl = document.createElement('div');
  statsEl.className = 'mini-ide-cell-stats';
  cell.statsEl = statsEl;
  renderCellRunStats(cell);

  main.append(head, contentEl, outputEl, statsEl);
  cellEl.append(rail, main);

  return cellEl;
}

/**
 * Turns a delete button's click into "press once to arm, press again to
 * actually delete" — a lighter-weight guard against an errant click than
 * a native confirm() dialog, since it needs a second deliberate press of
 * the same button rather than a mouse trip to a dialog's own button. An
 * armed button auto-disarms after a few seconds (a stale "one more click
 * deletes this" state, sitting there from an earlier click a reader has
 * since forgotten about, is exactly the trap this feature exists to
 * avoid), on blur, or the moment anything else on the page is clicked.
 *
 * @param {HTMLButtonElement} btn
 * @param {() => void} onConfirm - called on the second, confirming click
 */
function armDeleteButton(btn, onConfirm) {
  if (btn.classList.contains('mini-ide-armed')) {
    clearTimeout(btn._disarmTimer);
    disarmDeleteButton(btn);
    onConfirm();
    return;
  }
  btn.classList.add('mini-ide-armed');
  btn.title = 'Click again to delete this cell';
  btn._disarmTimer = setTimeout(() => disarmDeleteButton(btn), 3000);
  const disarmOnOutsideClick = (e) => {
    if (e.target !== btn) disarmDeleteButton(btn);
  };
  // Capture phase, and added after this very click has already finished
  // bubbling — otherwise the same click that arms the button would
  // immediately reach this listener and disarm it again.
  setTimeout(() => document.addEventListener('click', disarmOnOutsideClick, { capture: true, once: true }), 0);
  btn.addEventListener('blur', () => disarmDeleteButton(btn), { once: true });
}

/** Restores a delete button to its normal, unarmed state. */
function disarmDeleteButton(btn) {
  clearTimeout(btn._disarmTimer);
  btn.classList.remove('mini-ide-armed');
  btn.title = 'Delete this cell';
}

/**
 * Delete a cell by ID
 * Cleans up editor resources and re-renders
 *
 * @param {string} cellId - ID of cell to delete
 */
function deleteCell(cellId) {
  const index = cells.findIndex(c => c.id === cellId);
  if (index !== -1) {
    const cell = cells[index];
    if (cell.editor) {
      const editorEl = cell.editor.dom;
      if (editorEl && editorEl.parentNode) {
        editorEl.parentNode.removeChild(editorEl);
      }
    }
    
    cells.splice(index, 1);
    hasSampleCells = cells.length > 0 && cells.every(c => c.isSample);
    saveState();
    renderCells();
    updateStatus('Cell deleted.');
    if (sampleNoticeEl) sampleNoticeEl.hidden = !hasSampleCells;
  }
}

/**
 * Scrolls to a cell, briefly highlights it, and puts the cursor in it —
 * used after inserting a cell so a student's eye (and typing) lands on
 * the thing that just appeared, rather than wherever the page happened
 * to be scrolled. Ported from compose/dewmini.js's own focusCell(),
 * looked up by id rather than index since an in-between insert shifts
 * every later cell's index but not its id.
 *
 * @param {string} id - Cell id to focus
 */
function focusCell(id) {
  const el = cellsContainer?.querySelector(`.mini-ide-cell[data-id="${id}"]`);
  const cell = cells.find(c => c.id === id);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.classList.add('focused');
    setTimeout(() => el.classList.remove('focused'), 1000);
  }
  if (cell?.editor) cell.editor.focus();
  else if (cell?.showTextEditor) cell.showTextEditor();
  else if (cell?.textarea) cell.textarea.focus();
}

// ============================================================================
// Cell Execution
//
// Where "Cell Management" (above) deals with cells as data and DOM
// elements, this section is about actually running Python. This file
// never talks to Pyodide directly — it delegates everything to
// pyodide-engine.js (imported at the top of this file as `engine`),
// which in turn talks to assets/pyodide-worker.js. That layering means
// this file doesn't need to know or care whether Python is running in a
// background Worker or, as a fallback, directly on the page — it just
// calls engine.runCell() and engine.ensureBooted() and lets the engine
// module decide how.
// ============================================================================

/**
 * Boots Pyodide if needed, then mounts the filesystem (a previously
 * chosen real folder, else OPFS, else IndexedDB — see mini-ide-fs.js) if
 * it isn't mounted yet. Deferred until here, alongside the first Python
 * boot, rather than run eagerly on page load — booting Pyodide costs a
 * CDN fetch, and nothing should trigger that before a student actually
 * runs a cell.
 *
 * @async
 */
async function ensureEngineAndFsReady() {
  await engine.ensureBooted();
  if (!fsReady) {
    try {
      await fs.init();
      fsReady = true;
      renderFileTree();
    } catch (error) {
      // Not fatal to running a cell — file upload/SQLite/file-manager
      // features just won't have anywhere to persist to this session.
      console.warn('mini-ide: filesystem mount failed; file features are unavailable this session', error);
    }
  }
}

/**
 * Run a single cell by ID
 * Boots the engine if needed, then executes the cell's Python code.
 * A second click on the cell that is already running sends a Stop
 * (interrupt) request instead of starting a new run.
 *
 * @async
 * @param {string} cellId - ID of cell to run
 */
async function runCell(cellId) {
  const cell = cells.find(c => c.id === cellId);
  if (!cell || cell.type !== CELL_TYPES.PYTHON) return;

  if (runningCellId === cellId) {
    engine.requestInterrupt();
    return;
  }
  if (runningCellId || runningAll) return;

  const index = cells.findIndex(c => c.id === cellId);

  try {
    await ensureEngineAndFsReady();
  } catch (error) {
    updateStatus(`Python failed to start: ${error.message}. Reloading the page usually fixes it.`, 'error');
    return;
  }

  runningCellId = cellId;
  const runBtn = cell.runBtn;
  const previousLabel = runBtn ? runBtn.textContent : '▶';
  setRunButtonRunning(runBtn);

  const startedAt = performance.now();
  try {
    const { ok } = await engine.runCell(cellId, cell.content);
    cell.hasError = !ok;
    cell.output = cell.outputEl ? cell.outputEl.innerHTML : '';
    setCellRunStats(cell, performance.now() - startedAt);
    updateStatus(
      ok ? `Cell ${index + 1} executed successfully.` : `Cell ${index + 1} raised an error.`,
      ok ? '' : 'error'
    );
  } catch (error) {
    setCellRunStats(cell, performance.now() - startedAt);
    updateStatus(`Cell ${index + 1} failed to run: ${error.message}`, 'error');
  } finally {
    runningCellId = null;
    resetRunButton(runBtn, previousLabel);
  }

  saveState();
}

/**
 * Formats how long a cell's last run took, human-scale rather than raw
 * milliseconds: "340 ms" under a second, "2.4 s" at or above it.
 *
 * @param {number} ms
 * @returns {string}
 */
function formatRunDuration(ms) {
  return ms < 1000 ? `${Math.round(ms)} ms` : `${(ms / 1000).toFixed(1)} s`;
}

/**
 * Records and (when the "Show run time" setting is on) displays how long
 * a cell's most recent run took. The duration is always kept on the cell
 * object — cheap to compute, and worth saving even while the setting is
 * off, in case a reader turns it on later without re-running everything.
 *
 * @param {Object} cell
 * @param {number} ms - elapsed wall-clock time for the run, in milliseconds
 */
function setCellRunStats(cell, ms) {
  cell.lastRunMs = ms;
  renderCellRunStats(cell);
}

/** Paints (or clears) one cell's stats line from its stored lastRunMs. */
function renderCellRunStats(cell) {
  if (!cell.statsEl) return;
  const showStats = document.documentElement.getAttribute('data-mini-ide-runstats') !== 'off';
  cell.statsEl.textContent = (showStats && typeof cell.lastRunMs === 'number')
    ? `Ran in ${formatRunDuration(cell.lastRunMs)}`
    : '';
}

/**
 * Clears one cell's output (and its run-time stat) without touching its
 * code — the non-destructive counterpart to deleting the cell outright.
 * A no-op on a cell that has never run or is currently running, since
 * there is nothing to clear (and clearing mid-run would fight the output
 * the running cell is actively writing).
 *
 * @param {string} cellId
 */
function resetCellOutput(cellId) {
  const cell = cells.find(c => c.id === cellId);
  if (!cell || cell.type !== CELL_TYPES.PYTHON || cellId === runningCellId) return;
  engine.clearOutput(cellId);
  cell.output = '';
  cell.hasError = false;
  delete cell.lastRunMs;
  renderCellRunStats(cell);
  saveState();
}

/** Resets every Python cell's output — the toolbar-level, non-destructive
 * "Clear Output" action. Distinct from the existing "Clear All" button,
 * which deletes every cell; this only ever touches output, never code. */
function clearAllOutputs() {
  cells.forEach(cell => {
    if (cell.type === CELL_TYPES.PYTHON) resetCellOutput(cell.id);
  });
  updateStatus('Output cleared.');
}

/**
 * Toggle a cell's Run button into its running/Stop state.
 * When a genuine interrupt buffer is available (worker mode, cross-origin
 * isolated) the button becomes a real Stop; otherwise it just shows the
 * cell is busy, since there is nothing to interrupt.
 *
 * @param {HTMLButtonElement|undefined} runBtn
 */
function setRunButtonRunning(runBtn) {
  if (!runBtn) return;
  if (engine.canStop()) {
    runBtn.disabled = false;
    runBtn.textContent = '■';
    runBtn.title = 'Stop this cell';
    runBtn.classList.add('mini-ide-running');
  } else {
    runBtn.disabled = true;
    runBtn.textContent = '…';
    runBtn.title = 'Running…';
  }
}

/**
 * Restore a cell's Run button after it finishes (or fails to) run.
 *
 * @param {HTMLButtonElement|undefined} runBtn
 * @param {string} previousLabel
 */
function resetRunButton(runBtn, previousLabel) {
  if (!runBtn) return;
  runBtn.disabled = false;
  runBtn.classList.remove('mini-ide-running');
  runBtn.title = 'Run this cell (Shift+Enter)';
  runBtn.textContent = previousLabel === '…' || previousLabel === '■' ? '▶' : previousLabel;
}

/**
 * Run all cells in order
 * Executes each Python cell sequentially. Cells share one persistent
 * Pyodide interpreter, so a name defined in an earlier cell is already
 * visible to a later one without any extra bookkeeping here.
 *
 * @async
 * @function runAllCells
 */
async function runAllCells() {
  if (cells.length === 0) {
    updateStatus('No cells to run.');
    return;
  }
  if (runningCellId || runningAll) return;

  try {
    await ensureEngineAndFsReady();
  } catch (error) {
    updateStatus(`Python failed to start: ${error.message}. Reloading the page usually fixes it.`, 'error');
    return;
  }

  runningAll = true;
  updateStatus(`Running ${cells.length} cells...`);

  for (let i = 0; i < cells.length; i++) {
    const cell = cells[i];
    if (cell.type === CELL_TYPES.PYTHON && cell.content.trim()) {
      runningCellId = cell.id;
      const startedAt = performance.now();
      try {
        const { ok } = await engine.runCell(cell.id, cell.content);
        cell.hasError = !ok;
        cell.output = cell.outputEl ? cell.outputEl.innerHTML : '';
        setCellRunStats(cell, performance.now() - startedAt);
        if (!ok) updateStatus(`Error in cell ${i + 1}.`, 'error');
      } catch (error) {
        setCellRunStats(cell, performance.now() - startedAt);
        updateStatus(`Cell ${i + 1} failed to run: ${error.message}`, 'error');
      }
    }
  }

  runningCellId = null;
  runningAll = false;
  saveState();
  updateStatus(`All ${cells.length} cells executed.`);
}

// ============================================================================
// File Tree
// ============================================================================

/**
 * Format a byte count for display in the file tree (e.g. "1.2 KB").
 *
 * @param {number} bytes
 * @returns {string}
 */
function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

/**
 * Re-list the mounted filesystem's root and redraw the file tree pane.
 * A no-op-looking placeholder ("Files appear here once Python starts")
 * stays up until fsReady flips true — see ensureEngineAndFsReady().
 *
 * @async
 */
async function renderFileTree() {
  if (!filetreeListEl || !filetreeNoteEl) return;

  if (!fsReady) {
    filetreeListEl.hidden = true;
    filetreeNoteEl.hidden = false;
    filetreeNoteEl.textContent = 'Files appear here once Python starts — run any cell.';
    return;
  }

  let entries;
  try {
    entries = await fs.listDir('');
  } catch (error) {
    filetreeListEl.hidden = true;
    filetreeNoteEl.hidden = false;
    filetreeNoteEl.textContent = `Couldn't list files: ${error.message}`;
    return;
  }

  if (entries.length === 0) {
    filetreeListEl.hidden = true;
    filetreeNoteEl.hidden = false;
    filetreeNoteEl.textContent = 'No files yet. Files a cell writes, or that you upload, will show up here.';
    return;
  }

  filetreeNoteEl.hidden = true;
  filetreeListEl.hidden = false;
  filetreeListEl.innerHTML = '';

  for (const entry of entries) {
    const item = document.createElement('li');
    item.className = 'mini-ide-filetree-item';

    const nameEl = document.createElement('span');
    nameEl.className = 'mini-ide-filetree-item-name';
    nameEl.textContent = entry.isDir ? `${entry.name}/` : entry.name;
    nameEl.title = entry.name;

    const sizeEl = document.createElement('span');
    sizeEl.className = 'mini-ide-filetree-item-size';
    sizeEl.textContent = entry.isDir ? '' : formatFileSize(entry.size);

    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.className = 'mini-ide-filetree-item-delete';
    deleteBtn.textContent = '×';
    deleteBtn.title = `Delete ${entry.name}`;
    deleteBtn.setAttribute('aria-label', `Delete ${entry.name}`);
    deleteBtn.addEventListener('click', () => deleteTreeFile(entry.name));

    item.appendChild(nameEl);
    item.appendChild(sizeEl);
    item.appendChild(deleteBtn);
    filetreeListEl.appendChild(item);
  }
}

/**
 * Delete a file from the mounted filesystem and refresh the tree.
 *
 * @async
 * @param {string} name - entry name, relative to the mount's root
 */
async function deleteTreeFile(name) {
  if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
  try {
    await fs.deleteFile(name);
  } catch (error) {
    updateStatus(`Couldn't delete ${name}: ${error.message}`, 'error');
    return;
  }
  renderFileTree();
}

/**
 * Write one or more dropped/selected files into the mounted filesystem's
 * root, then refresh the tree. Requires Python to have already started
 * (fsReady) — the button/dropzone work either way, but nothing is
 * written until then.
 *
 * @async
 * @param {FileList|File[]|null|undefined} fileList
 */
async function uploadFiles(fileList) {
  const files = fileList ? Array.from(fileList) : [];
  if (files.length === 0) return;

  if (!fsReady) {
    updateStatus('Run a cell first to start Python, then upload files.', 'error');
    return;
  }

  let uploaded = 0;
  for (const file of files) {
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      await fs.writeFile(file.name, bytes);
      uploaded++;
    } catch (error) {
      updateStatus(`Couldn't upload ${file.name}: ${error.message}`, 'error');
    }
  }

  renderFileTree();
  if (uploaded > 0) {
    updateStatus(`Uploaded ${uploaded} file${uploaded === 1 ? '' : 's'}.`);
  }
}

// ============================================================================
// Notebook Import (.ipynb / .py)
//
// Two file formats, two parsers (parseIpynb and parsePy further down),
// one shared entry point (handleImportNotebookFile). Both parsers do the
// same basic job — turn raw file text into an array of plain cell
// objects, the same shape createNewCell() produces — without touching
// the page's actual `cells` array themselves; handleImportNotebookFile
// is the only place that assigns the result into `cells`, `saveState()`s
// it, and re-renders. That split (parse text -> plain data, versus
// apply that data to the page) is what makes each parser independently
// testable and easy to reason about: neither one needs to know about
// the DOM, localStorage, or the replace/append setting at all.
// ============================================================================

/**
 * Shared tail end of every import path (a picked file, or a built-in
 * example fetched by URL): run the compatibility scan, replace/append
 * per the Settings choice, save, and re-render. Split out so
 * loadBuiltInExample() below doesn't have to duplicate any of it — the
 * only thing that differs between a picked file and a built-in example
 * is where `imported` came from.
 *
 * @param {Array<Object>} imported - freshly parsed cells, not yet in `cells`
 * @param {string} sourceLabel - shown in the status line, e.g. a filename
 */
function applyImportedCells(imported, sourceLabel) {
  if (imported.length === 0) {
    updateStatus('That file has no cells to import.', 'error');
    return;
  }

  // Checked before the cells ever land in the notebook — the warning,
  // if any, should be the first thing a reader sees about this import,
  // not something they stumble into three cells later as a confusing
  // error with no obvious cause.
  const compatWarnings = scanPyodideCompatibility(imported);
  if (importCompatNoticeEl && importCompatListEl) {
    if (compatWarnings.length) {
      // Every warning is built entirely from this file's own hardcoded
      // strings and plain integers (scanPyodideCompatibility() never
      // inserts anything from the imported file's actual text) — safe
      // to turn `backticks` into <code> and drop straight into innerHTML.
      const toHtml = (w) => `<li>${w.replace(/`([^`]+)`/g, '<code>$1</code>')}</li>`;
      importCompatListEl.innerHTML = compatWarnings.map(toHtml).join('');
      importCompatNoticeEl.hidden = false;
    } else {
      importCompatNoticeEl.hidden = true;
    }
  }

  cells = loadImportMode() === 'append' ? cells.concat(imported) : imported;
  hasSampleCells = false;
  saveState();
  renderCells();
  if (sampleNoticeEl) sampleNoticeEl.hidden = true;
  updateStatus(`Loaded ${imported.length} cell${imported.length === 1 ? '' : 's'} from ${sourceLabel}.`);
}

/**
 * Import a .ipynb or .py file, replacing the current notebook's cells.
 * Routed from the toolbar's "Import" button.
 *
 * @async
 * @param {Event} e - the file input's change event
 */
async function handleImportNotebookFile(e) {
  const input = e.target;
  const file = input.files && input.files[0];
  input.value = '';
  if (!file) return;

  let imported;
  try {
    const text = await file.text();
    imported = file.name.toLowerCase().endsWith('.ipynb') ? parseIpynb(text) : parsePy(text);
  } catch (error) {
    updateStatus(`Couldn't read ${file.name}: ${error.message}`, 'error');
    return;
  }

  applyImportedCells(imported, file.name);
}

/**
 * Loads one of dewlab's own worked examples (assets/examples/*.ipynb) —
 * a real, runnable walkthrough (SQL over a real dataset, a data
 * investigation, a math simulation, text analysis), not the short
 * "Load example" starter. Goes through the exact same
 * parseIpynb()/applyImportedCells() path a reader's own uploaded file
 * would, so a compatibility warning would show up here too if one of
 * these examples ever needed something Pyodide can't do — the same
 * honesty the examples ask of anyone else's notebook.
 *
 * @async
 * @param {string} path - relative to this page, e.g. "assets/examples/sql-owid.ipynb"
 * @param {string} label - shown in the status line
 */
async function loadBuiltInExample(path, label) {
  let imported;
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    imported = parseIpynb(await response.text());
  } catch (error) {
    updateStatus(`Couldn't load "${label}": ${error.message}`, 'error');
    return;
  }
  applyImportedCells(imported, label);
}

/**
 * Parse a Jupyter notebook's JSON into Mini IDE cells. Best-effort on rich
 * outputs — image/png, text/html, and text/plain or a stream — everything
 * else (widgets, other MIME types) is silently skipped rather than
 * attempting a full nbformat renderer.
 *
 * @param {string} text - raw .ipynb file contents
 * @returns {Array<Object>} new cell objects (not yet added to `cells`)
 */
function parseIpynb(text) {
  const notebook = JSON.parse(text);
  if (!Array.isArray(notebook.cells)) {
    throw new Error('that file has no cells array');
  }
  return notebook.cells.map((nbCell) => {
    const isCode = nbCell.cell_type === 'code';
    const source = Array.isArray(nbCell.source) ? nbCell.source.join('') : (nbCell.source || '');
    const cell = createNewCell(isCode ? CELL_TYPES.PYTHON : CELL_TYPES.TEXT, source, false);
    if (isCode && Array.isArray(nbCell.outputs) && nbCell.outputs.length > 0) {
      cell.output = renderIpynbOutputs(nbCell.outputs);
    }
    return cell;
  });
}

/**
 * Render a code cell's `outputs` array (nbformat 4) as the same HTML
 * string shape cell.output already holds for a freshly-run cell.
 *
 * @param {Array<Object>} outputs
 * @returns {string}
 */
function renderIpynbOutputs(outputs) {
  const joinText = (value) => (Array.isArray(value) ? value.join('') : (value || ''));
  const parts = [];

  for (const out of outputs) {
    const data = out.data || {};
    if (data['image/png']) {
      const encoded = joinText(data['image/png']);
      parts.push(`<div class="dl-figure"><img alt="Figure from imported notebook" src="data:image/png;base64,${encoded}"></div>`);
    } else if (data['text/html']) {
      // Trusted: this is markup the notebook's own renderer produced
      // (e.g. a DataFrame's own to_html()), not user-entered text.
      parts.push(joinText(data['text/html']));
    } else if (data['text/plain']) {
      parts.push(`<pre>${escapeHtml(joinText(data['text/plain']))}</pre>`);
    } else if (out.output_type === 'stream' && out.text !== undefined) {
      const cssClass = out.name === 'stderr' ? 'dl-error' : 'dl-stdout';
      parts.push(`<pre class="${cssClass}">${escapeHtml(joinText(out.text))}</pre>`);
    }
    // Anything else (widgets, other MIME types) is dropped — best-effort,
    // not a full nbformat renderer.
  }

  return parts.join('');
}

/**
 * Modules with no Pyodide build at all, or that need something a
 * browser tab fundamentally cannot offer (a display to draw a GUI
 * window in, a separate OS process, a raw network socket, a real
 * terminal) — not every package Pyodide happens to lack (that list
 * changes with every Pyodide release, and Mini IDE has no reliable way
 * to check it from here), just the common, *structurally* impossible
 * ones worth telling a student about before they spend time debugging a
 * cryptic ImportError. Checked against a cell's own top-level import
 * name, so `import tkinter as tk` and `from tkinter import ttk` both
 * match on `tkinter`.
 */
const PYODIDE_INCOMPATIBLE_MODULES = {
  tkinter: 'opens a GUI window — there is no display here to draw one on',
  turtle: 'opens a GUI window — there is no display here to draw one on',
  pygame: 'needs a real display and audio device Pyodide cannot offer',
  PyQt5: 'opens a GUI window — there is no display here to draw one on',
  PyQt6: 'opens a GUI window — there is no display here to draw one on',
  PySide2: 'opens a GUI window — there is no display here to draw one on',
  PySide6: 'opens a GUI window — there is no display here to draw one on',
  wx: 'opens a GUI window — there is no display here to draw one on',
  kivy: 'opens a GUI window — there is no display here to draw one on',
  cv2: 'OpenCV has no Pyodide build',
  torch: 'not available in Pyodide — too large, and needs native GPU code',
  tensorflow: 'not available in Pyodide — too large, and needs native GPU code',
  keras: 'not available in Pyodide — too large, and needs native GPU code',
  multiprocessing: 'Pyodide runs on a single thread — there is no separate process to start',
  subprocess: 'there is no operating system underneath to run a command in',
  socket: 'the browser has no raw network socket access',
  ctypes: 'there are no native shared libraries here to load',
  serial: 'the browser has no serial port access',
  pyaudio: 'the browser has no direct audio device access',
  sounddevice: 'the browser has no direct audio device access',
  selenium: 'there is no separate browser process for it to drive',
  pty: 'this needs a real terminal, which the browser has none of',
  curses: 'this needs a real terminal, which the browser has none of',
  termios: 'this needs a real terminal, which the browser has none of',
};

/**
 * Best-effort scan of imported Python cells for things that will not
 * work once they actually run here — not a full Python parser, just the
 * regexes worth the trouble for the mistakes a notebook written outside
 * Mini IDE actually tends to make: a magic command or shell escape (only
 * valid inside a real Jupyter/IPython kernel, a plain SyntaxError
 * anywhere else), and an import Pyodide cannot satisfy no matter what
 * packages get loaded. Returns one short message per distinct problem,
 * each naming which imported cell(s) it showed up in — good enough to
 * flag before a student goes looking for a bug in their own logic that
 * was never there.
 *
 * @param {Array<Object>} importedCells - freshly parsed, not yet in `cells`
 * @returns {Array<string>} human-readable warnings, empty if none found
 */
function scanPyodideCompatibility(importedCells) {
  const magicCells = [];
  const shellCells = [];
  const moduleCells = new Map(); // module name -> Set of 1-based cell numbers

  importedCells.forEach((cell, index) => {
    if (cell.type !== CELL_TYPES.PYTHON) return;
    const cellNumber = index + 1;
    const lines = cell.content.split('\n');

    for (const rawLine of lines) {
      const line = rawLine.trim();
      // A line-or-cell magic ("%time", "%%bash") or a shell escape ("!pip
      // install x") is only meaningful inside a real IPython kernel —
      // Pyodide's Python sees plain "%" or "!" as a syntax error, not a
      // special command, so these never work as-is once run here.
      if (/^%{1,2}\S/.test(line)) magicCells.push(cellNumber);
      else if (/^!\S/.test(line)) shellCells.push(cellNumber);

      const importMatch = line.match(/^(?:import|from)\s+([A-Za-z_][\w.]*)/);
      if (importMatch) {
        const topLevelModule = importMatch[1].split('.')[0];
        if (Object.prototype.hasOwnProperty.call(PYODIDE_INCOMPATIBLE_MODULES, topLevelModule)) {
          if (!moduleCells.has(topLevelModule)) moduleCells.set(topLevelModule, new Set());
          moduleCells.get(topLevelModule).add(cellNumber);
        }
      }
    }
  });

  const describeCells = (numbers) => `cell${numbers.length === 1 ? '' : 's'} ${numbers.join(', ')}`;
  const warnings = [];
  for (const [moduleName, cellNumbers] of moduleCells) {
    warnings.push(
      `\`${moduleName}\` (${describeCells([...cellNumbers].sort((a, b) => a - b))}) ${PYODIDE_INCOMPATIBLE_MODULES[moduleName]}.`
    );
  }
  if (magicCells.length) {
    warnings.push(`Jupyter "magic" commands like \`%matplotlib\` or \`%%time\` (${describeCells(magicCells)}) aren't valid Python here and will raise an error if run as-is.`);
  }
  if (shellCells.length) {
    warnings.push(`Lines starting with \`!\` (${describeCells(shellCells)}) run a shell command in Jupyter — there's no shell here, and Mini IDE's packages are already loaded, so these aren't needed anyway.`);
  }
  return warnings;
}

/**
 * Split a .py file into cells on "# %%" markers (the Jupytext/VS Code/
 * Spyder convention) — the same marker downloadAsPython() now exports
 * with, so a round trip lands back where it started. A file with no
 * markers imports as a single cell.
 *
 * @param {string} text - raw .py file contents
 * @returns {Array<Object>} new cell objects (not yet added to `cells`)
 */
function parsePy(text) {
  const marker = /^#\s*%%.*$/m;
  if (!marker.test(text)) {
    return text.trim() ? [createNewCell(CELL_TYPES.PYTHON, text, false)] : [];
  }
  return text
    .split(/^#\s*%%.*$/m)
    .map((chunk) => chunk.replace(/^\s+|\s+$/g, ''))
    .filter((chunk) => chunk.length > 0)
    .map((chunk) => createNewCell(CELL_TYPES.PYTHON, chunk, false));
}

// ============================================================================
// Download Functions
//
// All three functions here follow the same four steps: build the file's
// text content as a JavaScript string, wrap it in a Blob (the browser's
// representation of raw file-like data), turn that Blob into a
// temporary object URL with `URL.createObjectURL()`, then create an
// invisible `<a download>` link pointing at that URL and click it in
// code — the same as if a person had clicked a real download link
// themselves. `URL.revokeObjectURL()` afterwards frees the browser's
// memory for that temporary URL, since nothing else needs it once the
// download has started. downloadAsPython() and the "Import" feature
// (see the Notebook Import section above) are a matched pair: the "# %%"
// separator this file writes is exactly what parsePy() looks for, so a
// downloaded .py file can be loaded straight back in as the same cells.
// ============================================================================

/**
 * Download all cells as a Python file
 * Combines all Python cells into a single .py file
 *
 * @function downloadAsPython
 */
function downloadAsPython() {
  const pythonCells = cells.filter(c => c.type === CELL_TYPES.PYTHON);
  if (pythonCells.length === 0) {
    updateStatus('No Python cells to download.', 'error');
    return;
  }

  // "# %%" (the Jupytext/VS Code/Spyder convention) rather than an
  // arbitrary separator, so a downloaded .py round-trips back through
  // "Import" (parsePy()) into the same cells it came from.
  const content = pythonCells.map(cell => cell.content).join('\n\n# %%\n\n');
  const blob = new Blob([content], { type: 'text/x-python' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${getFilenameBase()}.py`;
  a.click();
  URL.revokeObjectURL(url);
  updateStatus('Downloaded as Python file.');
}

/**
 * Download all cells as a static HTML snapshot.
 *
 * This is deliberately NOT a runnable page — it has no embedded Pyodide
 * and nothing in the downloaded file executes. It's just each cell's
 * source code and its last output, saved as plain markup, for showing
 * someone what a notebook looked like. If you're looking for a copy of
 * Mini IDE a reader could actually run, that's a different feature —
 * see docs/MINI_IDE.md's "The Downloadable Mini IDE" section, which
 * `build.py`'s `write_mini_ide_bundle()` produces, not this function.
 *
 * @function downloadAsHtml
 */
function downloadAsHtml() {
  const content = cells.map(cell => {
    if (cell.type === CELL_TYPES.PYTHON) {
      return `<div class="cell python">\n<pre>${escapeHtml(cell.content)}</pre>\n${cell.output ? `<div class="output">${cell.output}</div>` : ''}\n</div>`;
    } else {
      return `<div class="cell text">\n${cell.content}\n</div>`;
    }
  }).join('\n');

  const html = `<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>Mini IDE Export</title>\n</head>\n<body>\n${content}\n</body>\n</html>`;
  
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${getFilenameBase()}.html`;
  a.click();
  URL.revokeObjectURL(url);
  updateStatus('Downloaded as HTML file.');
}

/**
 * Download all cells as a Jupyter Notebook (.ipynb)
 * Creates a valid Jupyter notebook JSON file
 *
 * @function downloadAsIpynb
 */
function downloadAsIpynb() {
  const notebook = {
    cells: cells.map(cell => ({
      cell_type: cell.type === CELL_TYPES.PYTHON ? 'code' : 'markdown',
      source: cell.content.split('\n'),
      outputs: cell.output ? [{ output_type: 'stream', name: 'stdout', text: cell.output }] : [],
      metadata: {}
    })),
    metadata: {
      kernelspec: {
        display_name: 'Python 3',
        language: 'python',
        name: 'python3'
      },
      language_info: {
        codemirror_mode: { name: 'ipython', version: 3 },
        file_extension: '.py',
        mimetype: 'text/x-python',
        name: 'python',
        nbconvert_exporter: 'python',
        pygments_lexer: 'ipython3',
        version: '3.8.0'
      }
    },
    nbformat: 4,
    nbformat_minor: 4
  };

  const content = JSON.stringify(notebook, null, 2);
  const blob = new Blob([content], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${getFilenameBase()}.ipynb`;
  a.click();
  URL.revokeObjectURL(url);
  updateStatus('Downloaded as Jupyter Notebook.');
}

// ============================================================================
// Drag and Drop
//
// Ported from compose/dewmini.js's own setupDragAndDrop() — its id-based
// approach (rather than the DOM-child-index approach this file used
// before) is what makes reordering work correctly now that renderCells()
// interleaves an insert divider between every cell: cellsContainer's
// direct children are no longer one-cell-per-index the way a plain list
// of cells would be, so an index read off `cellsContainer.children`
// would count dividers as if they were cells. Working entirely in terms
// of `cells.findIndex(...)` by id sidesteps that — a divider never has
// an id to find.
//
// Four HTML5 Drag and Drop API events, fired automatically by the
// browser while a draggable element is being dragged:
//   - "dragstart" (on the thing being dragged): remembers which cell's
//     id is being dragged, in the module-level `draggedId`.
//   - "dragover" (fired repeatedly, on whatever the mouse is currently
//     over): must call `e.preventDefault()` — a drop target's default
//     behavior is to refuse the drop entirely unless something
//     explicitly opts in every time, not just once. Also decides, from
//     the mouse's vertical position within the hovered cell, whether to
//     mark the drop as landing above or below it.
//   - "dragend" (on the thing that was dragged, once the drag is over
//     however it ended): cleanup, whether or not a drop happened.
//   - "drop" (on whatever the mouse was over when released): the actual
//     reordering — removes the dragged cell from its old array position
//     and re-inserts it at the new one, using the same before/after
//     calculation dragover already made.
// ============================================================================

/** Removes the drop-position highlight from wherever it currently is. */
function clearDropMarkers() {
  cellsContainer?.querySelectorAll('.mini-ide-drop-before,.mini-ide-drop-after')
    .forEach(el => el.classList.remove('mini-ide-drop-before', 'mini-ide-drop-after'));
}

/**
 * Setup drag and drop functionality for cells
 * Allows reordering cells by dragging their head
 *
 * @function setupDragAndDrop
 */
function setupDragAndDrop() {
  if (!cellsContainer) return;

  cellsContainer.addEventListener('dragstart', (e) => {
    const head = e.target.closest('.mini-ide-cell-head');
    if (!head) return;
    draggedId = head.dataset.id;
    head.closest('.mini-ide-cell')?.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', draggedId);
  });

  cellsContainer.addEventListener('dragend', () => {
    cellsContainer.querySelectorAll('.dragging').forEach(el => el.classList.remove('dragging'));
    clearDropMarkers();
    draggedId = null;
  });

  cellsContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    if (!draggedId) return;
    clearDropMarkers();
    const target = e.target.closest('.mini-ide-cell');
    if (!target || target.dataset.id === draggedId) return;
    const rect = target.getBoundingClientRect();
    const before = e.clientY < rect.top + rect.height / 2;
    target.classList.add(before ? 'mini-ide-drop-before' : 'mini-ide-drop-after');
  });

  cellsContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    if (!draggedId) return;
    const target = e.target.closest('.mini-ide-cell');
    clearDropMarkers();

    const fromIdx = cells.findIndex(c => c.id === draggedId);
    if (fromIdx === -1) { draggedId = null; return; }

    let toIdx = cells.length;
    if (target && target.dataset.id !== draggedId) {
      const rect = target.getBoundingClientRect();
      const before = e.clientY < rect.top + rect.height / 2;
      toIdx = cells.findIndex(c => c.id === target.dataset.id);
      if (!before) toIdx += 1;
    }

    const [moved] = cells.splice(fromIdx, 1);
    if (toIdx > fromIdx) toIdx -= 1;
    cells.splice(toIdx, 0, moved);

    saveState();
    renderCells();
    draggedId = null;
    updateStatus('Reordered.');
  });

  cellsContainer.addEventListener('dragenter', (e) => {
    e.preventDefault();
  });

  cellsContainer.addEventListener('dragleave', (e) => {
    e.preventDefault();
  });
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Update the status message
 * Shows temporary messages to the user
 *
 * @param {string} message - Status message
 * @param {string} [type=''] - Message type ('error' for errors)
 */
function updateStatus(message, type = '') {
  if (statusEl) {
    statusEl.hidden = !message;
    statusEl.textContent = message;
    statusEl.className = `mini-ide-status ${type}`;
  }
}

/**
 * Escape HTML special characters
 * Prevents XSS when displaying user content
 *
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Formatting inside one line of a text cell's rendered view: `code`,
 * **bold**, and italic written with either asterisks or underscores.
 * Ported from compose/dewmini.js's own renderDocInline() — each
 * `.replace()` scans the whole string for one pattern, chained so code
 * is handled before bold/italic (so something inside backticks is never
 * misread as a bold marker).
 *
 * @param {string} text - Already-escaped text for one line
 * @returns {string} That line with inline formatting applied
 */
function renderDocInline(text) {
  return text
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>')
    .replace(/(^|[^\w])_([^_\n]+)_(?!\w)/g, '$1<em>$2</em>');
}

/**
 * Turns a whole text cell's raw content into rendered HTML, line by
 * line — a small, hand-written parser (ported from compose/dewmini.js's
 * own renderDocMarkdown()) that walks the text once, tracking whether a
 * bullet list or a paragraph is currently open, and decides what to do
 * from what kind of line it just read: a heading, a bullet, a blank
 * line, or plain text to add to the paragraph in progress.
 *
 * @param {string} text - A text cell's raw, unescaped content
 * @returns {string} Rendered HTML for the .dl-doc-render element
 */
function renderDocMarkdown(text) {
  const out = [];
  let listOpen = false;
  let para = [];
  const closeList = () => { if (listOpen) { out.push('</ul>'); listOpen = false; } };
  const flushPara = () => { if (para.length) { out.push(`<p>${renderDocInline(para.join(' '))}</p>`); para = []; } };

  for (const raw of escapeHtml(text).split('\n')) {
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
      if (!listOpen) { out.push('<ul>'); listOpen = true; }
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
  return out.join('\n') || '<p class="dl-doc-empty">Empty note.</p>';
}

// ============================================================================
// Start the Mini IDE
// ============================================================================

// Initialize when DOM is ready. A module script runs after the document
// has already been parsed, so document.readyState is frequently no longer
// "loading" by the time this line executes — without the guard below, both
// branches can fire (the immediate check here, then DOMContentLoaded a tick
// later), double-registering every toolbar listener setupEventListeners()
// attaches.
let initialized = false;
function initOnce() {
  if (initialized) return;
  initialized = true;
  init();
}

document.addEventListener('DOMContentLoaded', initOnce);
if (document.readyState !== 'loading') {
  initOnce();
}
