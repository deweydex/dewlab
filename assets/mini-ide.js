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
 *   - Cell array (this file) + Pyodide engine (mini-ide-engine.js), which
 *     boots the same assets/pyodide-worker.js the tutorial pages use — a
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
import * as engine from "./mini-ide-engine.js";
import * as fs from "./mini-ide-fs.js";

// ============================================================================
// Configuration Constants
// ============================================================================

/**
 * LocalStorage key for cells state
 * @constant {string}
 */
const STORAGE_KEY = "mini-ide:cells:v1";

/**
 * LocalStorage key for helper visibility state
 * @constant {string}
 */
const HELPER_VISIBLE_KEY = "mini-ide:helper-visible";

// ============================================================================
// Global State
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
// ============================================================================

/**
 * DOM element references (initialized in init())
 */
let cellsContainer;
let addPythonBtn;
let addTextBtn;
let runAllBtn;
let clearAllBtn;
let downloadPythonBtn;
let downloadHtmlBtn;
let downloadIpynbBtn;
let helperEl;
let helperCloseBtn;
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

// ============================================================================
// Drag and Drop State
// ============================================================================

/**
 * Currently dragged cell element
 * @type {HTMLElement|null}
 */
let draggedCell = null;

/**
 * Drop placeholder element
 * @type {HTMLElement|null}
 */
let dropPlaceholder = null;

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
 * Initialize the Settings panel
 */
function initSettings() {
  const state = loadTexture();
  applyTexture(state);

  const panel = document.getElementById("dl-settings");
  if (!panel) return state;

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

  fs.configure({ onBackendChange: () => updateStorageStatus() });
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
  runAllBtn = document.getElementById('run-all');
  clearAllBtn = document.getElementById('clear-all');
  downloadPythonBtn = document.getElementById('download-python');
  downloadHtmlBtn = document.getElementById('download-html');
  downloadIpynbBtn = document.getElementById('download-ipynb');
  helperEl = document.getElementById('mini-ide-helper');
  helperCloseBtn = document.getElementById('helper-close');
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

  // Check if helper should be shown
  const showHelper = localStorage.getItem(HELPER_VISIBLE_KEY) !== 'false' && cells.length === 0;
  if (helperEl && showHelper) {
    helperEl.style.display = 'block';
  }

  // Check if we have sample cells
  hasSampleCells = cells.length > 0 && cells.every(cell => cell.isSample);
  if (hasSampleCells && sampleNoticeEl) {
    sampleNoticeEl.hidden = false;
  }

  // Initialize Settings panel
  initSettings();
  initMiniIdeSettings();

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
  
  // If no cells, create sample cells
  if (cells.length === 0) {
    cells = createSampleCells();
    hasSampleCells = true;
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
    isSample: Boolean(cell.isSample)
  }));
  localStorage.setItem(STORAGE_KEY, JSON.stringify(serializable));
}

// ============================================================================
// Event Listeners
// ============================================================================

/**
 * Setup all event listeners for buttons and UI interactions
 *
 * @function setupEventListeners
 */
function setupEventListeners() {
  // Add cell buttons
  addPythonBtn?.addEventListener('click', () => {
    cells.push(createNewCell(CELL_TYPES.PYTHON, ''));
    hasSampleCells = false;
    saveState();
    renderCells();
    scrollToCell(cells.length - 1);
    updateStatus('Python cell added.');
    if (sampleNoticeEl) sampleNoticeEl.hidden = true;
  });

  addTextBtn?.addEventListener('click', () => {
    cells.push(createNewCell(CELL_TYPES.TEXT, ''));
    hasSampleCells = false;
    saveState();
    renderCells();
    scrollToCell(cells.length - 1);
    updateStatus('Text cell added.');
    if (sampleNoticeEl) sampleNoticeEl.hidden = true;
  });

  // Run all cells
  runAllBtn?.addEventListener('click', () => {
    runAllCells();
  });

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

  // Download buttons
  downloadPythonBtn?.addEventListener('click', () => downloadAsPython());
  downloadHtmlBtn?.addEventListener('click', () => downloadAsHtml());
  downloadIpynbBtn?.addEventListener('click', () => downloadAsIpynb());

  // Helper close button
  helperCloseBtn?.addEventListener('click', () => {
    if (helperEl) helperEl.style.display = 'none';
    localStorage.setItem(HELPER_VISIBLE_KEY, 'false');
  });

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
 * Get default content for a cell type
 *
 * @param {string} type - Cell type
 * @returns {string} Default content
 */
function getDefaultContent(type) {
  if (type === CELL_TYPES.PYTHON) {
    return '# Start coding here\nprint("Hello, World!")';
  }
  return '# Add your text here\n\nThis is a text cell for documentation or comments.';
}

/**
 * Generate a unique cell ID
 * Uses timestamp and random string for uniqueness
 *
 * @returns {string} Unique cell ID
 */
function generateId() {
  return `cell-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Render all cells into the DOM
 * Creates or updates cell elements based on current state
 *
 * @function renderCells
 */
function renderCells() {
  if (!cellsContainer) return;
  
  cellsContainer.innerHTML = '';
  
  cells.forEach((cell, index) => {
    const cellEl = createCellElement(cell, index);
    cellsContainer.appendChild(cellEl);
  });
  
  // Hide helper if there are cells
  if (cells.length > 0 && helperEl) {
    helperEl.style.display = 'none';
    localStorage.setItem(HELPER_VISIBLE_KEY, 'false');
  }
  
  // Show/hide sample notice based on whether we have sample cells
  if (sampleNoticeEl) {
    hasSampleCells = cells.length > 0 && cells.every(cell => cell.isSample);
    sampleNoticeEl.hidden = !hasSampleCells;
  }
}

/**
 * Create a cell DOM element with editor and controls
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

  // Cell header with type label and action buttons
  const header = document.createElement('div');
  header.className = 'mini-ide-cell-header';
  header.draggable = true;
  header.dataset.id = cell.id;

  const typeLabel = document.createElement('span');
  typeLabel.className = 'mini-ide-cell-type';
  typeLabel.textContent = cell.type === CELL_TYPES.PYTHON ? 'Python' : 'Text';

  const actions = document.createElement('div');
  actions.className = 'mini-ide-cell-actions';

  // Run button (only for Python cells)
  const runBtn = document.createElement('button');
  runBtn.className = 'dl-btn';
  runBtn.innerHTML = '<span class="mini-ide-icon mini-ide-icon-run"></span>Run';
  runBtn.style.display = cell.type === CELL_TYPES.PYTHON ? 'inline-flex' : 'none';
  runBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    runCell(cell.id);
  });

  // Delete button
  const deleteBtn = document.createElement('button');
  deleteBtn.className = 'dl-btn dl-btn-secondary';
  deleteBtn.innerHTML = '<span class="mini-ide-icon mini-ide-icon-clear"></span>Delete';
  deleteBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    deleteCell(cell.id);
  });

  actions.appendChild(runBtn);
  actions.appendChild(deleteBtn);
  header.appendChild(typeLabel);
  header.appendChild(actions);

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

    // Store editor reference on cell for later access
    cell.editor = editor;
  } else {
    // Text cell: use textarea
    const textarea = document.createElement('textarea');
    textarea.className = 'mini-ide-textarea';
    textarea.value = cell.content;
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
    contentEl.appendChild(textarea);
    cell.textarea = textarea;
  }

  // Cell output area — repopulated from the last run's rendered markup,
  // which already includes any traceback tutorial_tools.py produced.
  const outputEl = document.createElement('div');
  outputEl.className = 'mini-ide-cell-output';
  if (cell.output) {
    outputEl.innerHTML = cell.output;
  } else {
    outputEl.className += ' empty';
  }
  cell.outputEl = outputEl;

  cellEl.appendChild(header);
  cellEl.appendChild(contentEl);
  cellEl.appendChild(outputEl);

  return cellEl;
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
 * Scroll to a specific cell
 *
 * @param {number} index - Cell index to scroll to
 */
function scrollToCell(index) {
  const cellEl = cellsContainer?.querySelector(`.mini-ide-cell[data-index="${index}"]`);
  if (cellEl) {
    cellEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    cellEl.classList.add('focused');
    setTimeout(() => cellEl.classList.remove('focused'), 1000);
  }
}

// ============================================================================
// Cell Execution
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
  const previousLabel = runBtn ? runBtn.textContent : 'Run';
  setRunButtonRunning(runBtn);

  try {
    const { ok } = await engine.runCell(cellId, cell.content);
    cell.hasError = !ok;
    cell.output = cell.outputEl ? cell.outputEl.innerHTML : '';
    updateStatus(
      ok ? `Cell ${index + 1} executed successfully.` : `Cell ${index + 1} raised an error.`,
      ok ? '' : 'error'
    );
  } catch (error) {
    updateStatus(`Cell ${index + 1} failed to run: ${error.message}`, 'error');
  } finally {
    runningCellId = null;
    resetRunButton(runBtn, previousLabel);
  }

  saveState();
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
    runBtn.textContent = 'Stop';
    runBtn.classList.add('dl-btn-stop');
  } else {
    runBtn.disabled = true;
    runBtn.textContent = 'Running…';
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
  runBtn.classList.remove('dl-btn-stop');
  runBtn.textContent = previousLabel === 'Running…' || previousLabel === 'Stop' ? 'Run' : previousLabel;
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
      try {
        const { ok } = await engine.runCell(cell.id, cell.content);
        cell.hasError = !ok;
        cell.output = cell.outputEl ? cell.outputEl.innerHTML : '';
        if (!ok) updateStatus(`Error in cell ${i + 1}.`, 'error');
      } catch (error) {
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
// ============================================================================

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

  if (imported.length === 0) {
    updateStatus('That file has no cells to import.', 'error');
    return;
  }

  cells = loadImportMode() === 'append' ? cells.concat(imported) : imported;
  hasSampleCells = false;
  saveState();
  renderCells();
  if (sampleNoticeEl) sampleNoticeEl.hidden = true;
  updateStatus(`Loaded ${imported.length} cell${imported.length === 1 ? '' : 's'} from ${file.name}.`);
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
  a.download = 'mini-ide-export.py';
  a.click();
  URL.revokeObjectURL(url);
  updateStatus('Downloaded as Python file.');
}

/**
 * Download all cells as a standalone HTML file
 * Creates a self-contained HTML with embedded Pyodide
 *
 * @function downloadAsHtml
 */
function downloadAsHtml() {
  // This is a simplified version - a full standalone HTML would be complex
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
  a.download = 'mini-ide-export.html';
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
  a.download = 'mini-ide-export.ipynb';
  a.click();
  URL.revokeObjectURL(url);
  updateStatus('Downloaded as Jupyter Notebook.');
}

// ============================================================================
// Drag and Drop
// ============================================================================

/**
 * Setup drag and drop functionality for cells
 * Allows reordering cells by dragging
 *
 * @function setupDragAndDrop
 */
function setupDragAndDrop() {
  if (!cellsContainer) return;

  cellsContainer.addEventListener('dragstart', (e) => {
    if (e.target.classList.contains('mini-ide-cell-header')) {
      draggedCell = e.target.parentElement;
      e.target.parentElement.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/html', draggedCell.innerHTML);
    }
  });

  cellsContainer.addEventListener('dragend', (e) => {
    if (draggedCell) {
      draggedCell.classList.remove('dragging');
      draggedCell = null;
    }
    if (dropPlaceholder) {
      dropPlaceholder.remove();
      dropPlaceholder = null;
    }
  });

  cellsContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';

    if (!draggedCell) return;

    const afterElement = getDragAfterElement(cellsContainer, e.clientY);
    
    if (dropPlaceholder) dropPlaceholder.remove();
    
    if (afterElement) {
      dropPlaceholder = document.createElement('div');
      dropPlaceholder.className = 'mini-ide-drop-placeholder';
      cellsContainer.insertBefore(dropPlaceholder, afterElement);
    } else {
      dropPlaceholder = document.createElement('div');
      dropPlaceholder.className = 'mini-ide-drop-placeholder';
      cellsContainer.appendChild(dropPlaceholder);
    }
  });

  cellsContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    if (!draggedCell) return;

    const dropIndex = Array.from(cellsContainer.children).indexOf(dropPlaceholder || draggedCell);
    const dragIndex = Array.from(cellsContainer.children).indexOf(draggedCell);

    if (dropIndex !== dragIndex) {
      // Reorder cells array
      const cellId = draggedCell.dataset.id;
      const cell = cells.find(c => c.id === cellId);
      if (cell) {
        cells.splice(dragIndex, 1);
        cells.splice(dropIndex, 0, cell);
        saveState();
      }
    }

    if (dropPlaceholder) {
      dropPlaceholder.remove();
      dropPlaceholder = null;
    }
    draggedCell.classList.remove('dragging');
    draggedCell = null;
    
    renderCells();
  });

  cellsContainer.addEventListener('dragenter', (e) => {
    e.preventDefault();
  });

  cellsContainer.addEventListener('dragleave', (e) => {
    e.preventDefault();
  });
}

/**
 * Get the element after which to insert the dragged cell
 * Based on mouse position
 *
 * @param {HTMLElement} container - Container element
 * @param {number} y - Mouse Y position
 * @returns {HTMLElement|null} Element after which to insert
 */
function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.mini-ide-cell:not(.dragging)')];
  
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    
    if (offset < 0 && offset > closest.offset) {
      return { offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
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
