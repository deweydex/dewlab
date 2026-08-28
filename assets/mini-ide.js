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
 *   - Uses shared Pyodide instance (same as tutorials)
 *   - Cells share a common namespace (like Jupyter)
 *   - State persisted to localStorage
 *   - Jedi runs inside Pyodide for pre-execution completion
 *
 * @module mini-ide
 */

import { createCodeEditor, setEditorTheme } from "./vendor/codemirror.bundle.js";

// ============================================================================
// Configuration Constants
// ============================================================================

/**
 * Pyodide version to use (must match what tutorials use)
 * @constant {string}
 */
const PYODIDE_VERSION = "0.28.3";

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
 * Pyodide instance (loaded on demand, shared across all cells)
 * @type {Object|null}
 */
let pyodide = null;

/**
 * Whether Pyodide has finished loading
 * @type {boolean}
 */
let pyodideLoaded = false;

/**
 * Whether Pyodide is currently loading
 * @type {boolean}
 */
let pyodideLoading = false;

/**
 * Jedi module (loaded on demand for pre-execution completion)
 * @type {Object|null}
 */
let jediModule = null;

/**
 * Shared namespace for all cells (like Jupyter's global namespace)
 * @type {Object}
 */
let sharedNamespace = { __builtins__: {} };

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
  localStorage.setItem(STORAGE_KEY, JSON.stringify(cells));
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
    error: null,
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
  
  // Add error class if cell has error
  if (cell.error) {
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
      completeNames: () => Object.keys(sharedNamespace),
      getDoc: (name) => getDocForName(name),
      getJediCompletions: (text, pos, word) => getJediCompletions(text, pos, word),
      getJediDoc: (name) => getJediDoc(name)
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

  // Cell output area
  const outputEl = document.createElement('div');
  outputEl.className = 'mini-ide-cell-output';
  if (cell.output) {
    outputEl.innerHTML = cell.output;
  } else if (cell.error) {
    outputEl.innerHTML = `<pre class="dl-error">${escapeHtml(cell.error)}</pre>`;
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
 * Run a single cell by ID
 * Executes the Python code and captures output/errors
 *
 * @async
 * @param {string} cellId - ID of cell to run
 */
async function runCell(cellId) {
  const cell = cells.find(c => c.id === cellId);
  if (!cell || cell.type !== CELL_TYPES.PYTHON) return;

  await ensurePyodide();

  const index = cells.findIndex(c => c.id === cellId);
  const outputEl = cell.outputEl;
  
  if (outputEl) {
    outputEl.className = 'mini-ide-cell-output';
    outputEl.innerHTML = '<em>Running...</em>';
  }

  try {
    // Clear previous output
    cell.output = '';
    cell.error = null;

    // Execute the code
    const result = await pyodide.runPythonAsync(cell.content);

    // Capture stdout (Pyodide captures this automatically)
    // For expressions, get the result
    if (result !== undefined) {
      cell.output = formatOutput(result);
    }

    // Update shared namespace with any new definitions
    await updateSharedNamespace();

    // Update status
    updateStatus(`Cell ${index + 1} executed successfully.`);

  } catch (error) {
    cell.error = formatError(error);
    cell.output = '';
    updateStatus(`Cell ${index + 1} error: ${truncateError(cell.error)}`);
  }

  // Re-render to show output
  saveState();
  renderCells();
}

/**
 * Run all cells in order
 * Executes each Python cell sequentially, maintaining shared namespace
 *
 * @async
 * @function runAllCells
 */
async function runAllCells() {
  if (cells.length === 0) {
    updateStatus('No cells to run.');
    return;
  }

  await ensurePyodide();

  // Clear all outputs first
  cells.forEach(cell => {
    cell.output = '';
    cell.error = null;
  });

  // Reset shared namespace
  sharedNamespace = { __builtins__: {} };

  updateStatus(`Running ${cells.length} cells...`);

  // Run each cell in order
  for (let i = 0; i < cells.length; i++) {
    const cell = cells[i];
    if (cell.type === CELL_TYPES.PYTHON && cell.content.trim()) {
      try {
        await pyodide.runPythonAsync(cell.content);
        await updateSharedNamespace();
      } catch (error) {
        cell.error = formatError(error);
        cell.output = '';
        updateStatus(`Error in cell ${i + 1}: ${truncateError(cell.error)}`);
        // Continue to next cell even if this one fails
      }
    }
  }

  // Re-render to show all outputs
  saveState();
  renderCells();
  updateStatus(`All ${cells.length} cells executed.`);
}

// ============================================================================
// Pyodide Management
// ============================================================================

/**
 * Ensure Pyodide is loaded and ready
 * Loads Pyodide and required packages on demand
 *
 * @async
 * @returns {Promise<Object>} Pyodide instance
 */
async function ensurePyodide() {
  if (pyodideLoaded) return pyodide;
  if (pyodideLoading) {
    // Wait for existing load to complete
    while (pyodideLoading) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return pyodide;
  }

  pyodideLoading = true;
  updateStatus('Loading Python...');

  try {
    // Load Pyodide
    const pyodideUrl = new URL(
      globalThis.DEWLAB_PYODIDE_BASE ||
        `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`,
      document.baseURI
    ).href;

    pyodide = await (globalThis.loadPyodide || (await import(pyodideUrl + "pyodide.mjs")).loadPyodide)({
      indexURL: pyodideUrl
    });

    updateStatus('Loading packages...');

    // Load required packages
    await pyodide.loadPackage(['numpy', 'pandas', 'matplotlib']);

    updateStatus('Preparing notebook tools...');

    // Load tutorial_tools.py
    await loadTutorialTools();

    pyodideLoaded = true;
    pyodideLoading = false;
    updateStatus('Python ready.');

    return pyodide;
  } catch (error) {
    pyodideLoading = false;
    console.error('Failed to load Pyodide:', error);
    updateStatus(`Failed to load Python: ${error.message}`, 'error');
    throw error;
  }
}

/**
 * Load tutorial_tools.py into Pyodide
 * Provides the dewlab-specific functions for cells
 *
 * @async
 */
async function loadTutorialTools() {
  const toolsCode = getTutorialToolsCode();
  pyodide.FS.writeFile("/home/pyodide/tutorial_tools.py", toolsCode, { encoding: "utf8" });
  
  // Import and configure tutorial_tools
  const tutorialTools = pyodide.pyimport("tutorial_tools");
  
  // Configure with empty data base (Mini IDE doesn't have a data directory by default)
  tutorialTools.configure("");
  
  // Store reference for later use
  window.tutorialTools = tutorialTools;
}

/**
 * Update shared namespace with current Pyodide globals
 * Excludes builtins and private names
 *
 * @async
 */
async function updateSharedNamespace() {
  try {
    const globals = pyodide.globals.get("dict");
    const newGlobals = await globals.toJs();
    
    // Update shared namespace with non-private, non-dunder names
    Object.keys(newGlobals).forEach(key => {
      if (!key.startsWith('_') && key !== 'In' && key !== 'Out') {
        sharedNamespace[key] = newGlobals[key];
      }
    });
  } catch (error) {
    console.warn('Failed to update shared namespace:', error);
  }
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

  const content = pythonCells.map(cell => cell.content).join('\n\n# ---\n\n');
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

/**
 * Format Python output for display
 * Handles various types of Python objects
 *
 * @param {any} output - Python output to format
 * @returns {string} Formatted output
 */
function formatOutput(output) {
  if (output === undefined || output === null) {
    return '';
  }
  if (typeof output === 'string') {
    return output;
  }
  if (typeof output === 'object') {
    try {
      return JSON.stringify(output, null, 2);
    } catch {
      return String(output);
    }
  }
  return String(output);
}

/**
 * Format Python error for display
 * Extracts meaningful error message from Pyodide errors
 *
 * @param {Error} error - Error to format
 * @returns {string} Formatted error message
 */
function formatError(error) {
  if (typeof error === 'string') return error;
  if (error.message) return error.message;
  return String(error);
}

/**
 * Truncate error message for status display
 * Keeps error messages short for the status bar
 *
 * @param {string} error - Error message
 * @param {number} [maxLength=50] - Maximum length
 * @returns {string} Truncated error
 */
function truncateError(error, maxLength = 50) {
  if (error.length <= maxLength) return error;
  return error.substring(0, maxLength) + '...';
}

// ============================================================================
// Jedi Integration (for autocomplete)
// ============================================================================

/**
 * Get Jedi completions for autocomplete
 * Runs Jedi inside Pyodide for pre-execution completion
 *
 * @async
 * @param {string} text - Code text
 * @param {Object} pos - Cursor position
 * @param {string} word - Current word
 * @returns {Promise<Array>} Array of completion suggestions
 */
async function getJediCompletions(text, pos, word) {
  if (!pyodide) return [];
  
  try {
    if (!jediModule) {
      await pyodide.loadPackage('jedi');
      jediModule = pyodide.pyimport('jedi');
    }

    // This is a simplified version - full Jedi integration would be more complex
    // For now, return basic Python keywords and builtins
    return [
      { label: 'print', type: 'function' },
      { label: 'len', type: 'function' },
      { label: 'range', type: 'function' },
      { label: 'def', type: 'keyword' },
      { label: 'for', type: 'keyword' },
      { label: 'if', type: 'keyword' },
      { label: 'import', type: 'keyword' }
    ];
  } catch (error) {
    console.warn('Jedi completion failed:', error);
    return [];
  }
}

/**
 * Get documentation for a name using Jedi
 *
 * @async
 * @param {string} name - Name to get documentation for
 * @returns {Promise<string|null>} Documentation string or null
 */
async function getJediDoc(name) {
  if (!pyodide) return null;
  
  try {
    if (!jediModule) {
      await pyodide.loadPackage('jedi');
      jediModule = pyodide.pyimport('jedi');
    }
    
    // Simplified - return basic docs
    const docs = {
      'print': 'print(*objects, sep=\' \', end=\'\\n\', file=sys.stdout, flush=False)\n\nPrints the values to a stream, or to sys.stdout by default.',
      'len': 'len(object)\n\nReturn the number of items in a container.',
      'range': 'range(stop)\nrange(start, stop[, step])\n\nGenerate numbers in a range.'
    };
    
    return docs[name] || null;
  } catch (error) {
    console.warn('Jedi doc failed:', error);
    return null;
  }
}

/**
 * Get documentation for a name from shared namespace
 *
 * @param {string} name - Name to get documentation for
 * @returns {string|null} Documentation string or null
 */
function getDocForName(name) {
  // Simplified documentation
  const docs = {
    'print': 'Prints values to stdout',
    'len': 'Returns the length of an object',
    'range': 'Generates a range of numbers',
    'show': 'dewlab function to display values',
    'show_table': 'dewlab function to display a table',
    'check': 'dewlab function to check answers',
    'text_input': 'dewlab function to create a text input widget',
    'dropdown': 'dewlab function to create a dropdown widget',
    'button': 'dewlab function to create a button widget',
    'load_csv': 'dewlab function to load a CSV file'
  };
  
  return docs[name] || null;
}

// ============================================================================
// Tutorial Tools Code
// ============================================================================

/**
 * Get the tutorial_tools.py code as a string
 * This is a simplified version adapted for the Mini IDE
 *
 * @returns {string} Python code for tutorial tools
 */
function getTutorialToolsCode() {
  return `\nimport html\nimport json\nimport sys\nimport traceback\nimport warnings\nimport io\nimport base64\n\n# Suppress matplotlib backend warning\nwarnings.filterwarnings("ignore", message="FigureCanvasAgg is non-interactive")\n\n# Global state for the current cell\n_current_cell_id = None\n_current_output_element = None\n\nclass _OutputCapture:\n    """Capture stdout for display in cell output."""\n    def __init__(self):\n        self.outputs = []\n        \n    def write(self, text):\n        self.outputs.append(text)\n        \n    def flush(self):\n        pass\n\n    def getvalue(self):\n        return ''.join(self.outputs)\n\nclass _Widget:\n    """Base class for all widgets."""\n    _counter = 0\n    \n    def __init__(self, label, widget_id=None):\n        _Widget._counter += 1\n        self.id = widget_id or f"widget-{_Widget._counter}"\n        self.label = label\n        self.type = "widget"\n\nclass _TextInput(_Widget):\n    """Text input widget."""\n    def __init__(self, label, value="", widget_id=None):\n        super().__init__(label, widget_id)\n        self.value = value\n        self.type = "text"\n\nclass _Dropdown(_Widget):\n    """Dropdown widget."""\n    def __init__(self, label, options, value=None, widget_id=None):\n        super().__init__(label, widget_id)\n        self.options = options\n        self.value = value or (options[0] if options else "")\n        self.type = "dropdown"\n\nclass _Button(_Widget):\n    """Button widget."""\n    def __init__(self, label, on_click, widget_id=None):\n        super().__init__(label, widget_id)\n        self.on_click = on_click\n        self.type = "button"\n\ndef text_input(label, value="", widget_id=None):\n    """Create a text input widget."""\n    widget = _TextInput(label, value, widget_id)\n    if _current_output_element:\n        widget_id = widget.id\n        _current_output_element.innerHTML += f'''\n        <div class="dl-widget dl-widget-text" data-widget-id="{widget_id}">\n            <label>{html.escape(label)}: <input type="text" value="{html.escape(widget.value)}" data-widget-id="{widget_id}"></label>\n        </div>\n        '''\n    return widget\n\ndef dropdown(label, options, value=None, widget_id=None):\n    """Create a dropdown widget."""\n    widget = _Dropdown(label, options, value, widget_id)\n    if _current_output_element:\n        widget_id = widget.id\n        options_html = ''.join(f'<option value="{html.escape(o)}"{" selected" if o == widget.value else ""}>{html.escape(o)}</option>' for o in options)\n        _current_output_element.innerHTML += f'''\n        <div class="dl-widget dl-widget-dropdown" data-widget-id="{widget_id}">\n            <label>{html.escape(label)}: <select data-widget-id="{widget_id}">{options_html}</select></label>\n        </div>\n        '''\n    return widget\n\ndef button(label, on_click, widget_id=None):\n    """Create a button widget."""\n    widget = _Button(label, on_click, widget_id)\n    if _current_output_element:\n        widget_id = widget.id\n        _current_output_element.innerHTML += f'''\n        <div class="dl-widget dl-widget-button" data-widget-id="{widget_id}">\n            <button type="button" data-widget-id="{widget_id}">{html.escape(label)}</button>\n        </div>\n        '''\n    return widget\n\nasync def load_csv(name):\n    """Load a CSV file from the data directory."""\n    import pandas as pd\n    import io\n    \n    # In Mini IDE, we need to fetch the CSV\n    try:\n        from js import fetch\n        response = await fetch(f"data/{name}")\n        if response.ok:\n            text = await response.text()\n            return pd.read_csv(io.StringIO(text))\n        else:\n            raise FileNotFoundError(f"Could not find data/{name}")\n    except Exception as e:\n        raise FileNotFoundError(f"Could not load {name}: {e}")\n\ndef show(value):\n    """Display a value in the cell output."""\n    if _current_output_element:\n        _current_output_element.innerHTML += f'<div class="dl-show">{html.escape(repr(value))}</div>'\n    return value\n\ndef show_table(df):\n    """Display a DataFrame as a table."""\n    if _current_output_element:\n        html_table = df.to_html(classes='dl-table', index=False)\n        _current_output_element.innerHTML += f'<div class="dl-show">{html_table}</div>'\n    return df\n\ndef check(value, expected):\n    """Check if a value matches the expected value."""\n    result = value == expected\n    if _current_output_element:\n        color = "#1f6b3f" if result else "#9b2226"\n        _current_output_element.innerHTML += f'<div class="dl-check" style="color: {color}">{"✓ Correct" if result else "✗ Incorrect"}</div>'\n    return result\n\ndef configure(data_base):\n    """Configure the tutorial tools with the data base URL."""\n    global _data_base\n    _data_base = data_base\n  `;
}

// ============================================================================
// Start the Mini IDE
// ============================================================================

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);

// Also handle cases where DOM is already loaded
if (document.readyState !== 'loading') {
  init();
}
