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

  // Load saved state
  loadSavedState();

  // Check if helper should be shown
  const showHelper = localStorage.getItem(HELPER_VISIBLE_KEY) !== 'false' && cells.length === 0;
  if (helperEl && showHelper) {
    helperEl.style.display = 'block';
  }

  // Setup event listeners
  setupEventListeners();

  // Setup drag and drop
  setupDragAndDrop();

  // Render cells
  renderCells();

  // Update status
  updateStatus('Ready. Add cells to begin.');
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
  
  // If no cells, create a default Python cell with helpful starter code
  if (cells.length === 0) {
    cells.push(createNewCell(
      CELL_TYPES.PYTHON, 
      '# Start coding here\nprint("Hello, World!")'
    ));
  }
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
    saveState();
    renderCells();
    scrollToCell(cells.length - 1);
    updateStatus('Python cell added.');
  });

  addTextBtn?.addEventListener('click', () => {
    cells.push(createNewCell(CELL_TYPES.TEXT, ''));
    saveState();
    renderCells();
    scrollToCell(cells.length - 1);
    updateStatus('Text cell added.');
  });

  // Run all cells
  runAllBtn?.addEventListener('click', () => {
    runAllCells();
  });

  // Clear all cells with confirmation
  clearAllBtn?.addEventListener('click', () => {
    if (confirm('Are you sure you want to clear all cells? This cannot be undone.')) {
      cells = [];
      saveState();
      renderCells();
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

  // Observe theme changes from Settings panel (if it exists)
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'data-theme') {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        updateAllEditorThemes(isDark);
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
 * @param {string} [id] - Unique cell ID (auto-generated if not provided)
 * @returns {Object} Cell object
 */
function createNewCell(type, content = '', id = generateId()) {
  return {
    id,
    type,
    content: content || getDefaultContent(type),
    output: '',
    error: null
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
  runBtn.className = 'dl-btn dl-btn-small';
  runBtn.innerHTML = '<span class="mini-ide-icon mini-ide-icon-run"></span>Run';
  runBtn.style.display = cell.type === CELL_TYPES.PYTHON ? 'inline-flex' : 'none';
  runBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    runCell(cell.id);
  });

  // Delete button
  const deleteBtn = document.createElement('button');
  deleteBtn.className = 'dl-btn dl-btn-small dl-btn-secondary';
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
          saveState();
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
        saveState();
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
    // Clean up editor if it exists
    const cell = cells[index];
    if (cell.editor) {
      // CodeMirror doesn't have a simple destroy method, but we can remove the DOM
      const editorEl = cell.editor.dom;
      if (editorEl && editorEl.parentNode) {
        editorEl.parentNode.removeChild(editorEl);
      }
    }
    
    cells.splice(index, 1);
    saveState();
    renderCells();
    updateStatus('Cell deleted.');
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
    
    // Visual feedback
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

  // Save state and re-render
  saveState();
  renderCells();
  updateStatus(`All cells executed. ${cells.filter(c => c.error).length} errors.`);
}

// ============================================================================
// Pyodide Management
// ============================================================================

/**
 * Ensure Pyodide is loaded and initialized
 * Loads Pyodide script and packages on first use
 *
 * @async
 * @function ensurePyodide
 */
async function ensurePyodide() {
  if (pyodideLoaded) return;
  if (pyodideLoading) {
    // Wait for existing load to complete
    while (pyodideLoading) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return;
  }

  pyodideLoading = true;
  updateStatus('Loading Python runtime...');

  try {
    // Load Pyodide script from CDN
    const pyodideScript = document.createElement('script');
    pyodideScript.src = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js`;
    document.head.appendChild(pyodideScript);

    // Wait for script to load
    await new Promise((resolve, reject) => {
      pyodideScript.onload = resolve;
      pyodideScript.onerror = reject;
    });

    // Initialize Pyodide
    pyodide = await loadPyodide({
      indexURL: `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`
    });

    // Load default packages
    await pyodide.loadPackage(['numpy', 'pandas', 'matplotlib']);

    // Set up the tutorial_tools API
    await setupTutorialTools();

    // Load Jedi for pre-execution completion
    await loadJedi();

    pyodideLoaded = true;
    pyodideLoading = false;
    updateStatus('Python runtime ready.');
  } catch (error) {
    pyodideLoading = false;
    updateStatus(`Failed to load Python runtime: ${error.message}`);
    console.error('Failed to load Pyodide:', error);
    throw error;
  }
}

/**
 * Load Jedi module in Pyodide for static analysis
 *
 * @async
 * @function loadJedi
 */
async function loadJedi() {
  try {
    // Jedi is already in Pyodide's package index
    await pyodide.loadPackage('jedi');
    jediModule = pyodide.globals.get('jedi');
    console.log('Jedi loaded successfully');
  } catch (error) {
    console.warn('Failed to load Jedi:', error);
    jediModule = null;
  }
}

/**
 * Setup tutorial_tools.py API in Pyodide
 * Makes all tutorial functions available globally
 *
 * @async
 * @function setupTutorialTools
 */
async function setupTutorialTools() {
  // Load tutorial_tools.py into Pyodide
  const toolsCode = getTutorialToolsCode();
  await pyodide.runPythonAsync(toolsCode);

  // Make tutorial_tools functions available globally
  await pyodide.runPythonAsync(`
    from tutorial_tools import show, show_table, check, text_input, dropdown, button, load_csv
    __builtins__.show = show
    __builtins__.show_table = show_table
    __builtins__.check = check
    __builtins__.text_input = text_input
    __builtins__.dropdown = dropdown
    __builtins__.button = button
    __builtins__.load_csv = load_csv
  `);

  // Patch matplotlib show() to work in Pyodide
  await pyodide.runPythonAsync(`
    import matplotlib.pyplot as plt
    
    def dewlab_show():
        from tutorial_tools import _capture_figures
        _capture_figures()
    
    plt.show = dewlab_show
  `);
}

// ============================================================================
// Jedi Integration
// ============================================================================

/**
 * Get completions from Jedi for pre-execution autocomplete
 * Uses Jedi's static analysis to provide completions before code runs
 *
 * @async
 * @param {string} text - Full text up to cursor
 * @param {number} pos - Cursor position
 * @param {string} [word] - Word at cursor (optional)
 * @returns {Promise<Array<Object>>} Array of completion objects with name and type
 */
async function getJediCompletions(text, pos, word = '') {
  if (!jediModule || !pyodideLoaded) {
    return [];
  }

  try {
    // Use Jedi to analyze the code and get completions
    const result = await pyodide.runPythonAsync(`
      import jedi
      import json
      
      try:
          # Create a Script object from the code
          script = jedi.Script(${JSON.stringify(text)}, line=${Math.floor(pos / (text.split('\\n')[0].length + 1)) + 1}, column=${pos % (text.split('\\n')[0].length + 1)})
          # Get completions
          completions = script.complete()
          # Format as JSON-serializable list
          result = []
          for comp in completions:
              result.append({
                  'name': comp.name,
                  'type': comp.type,
                  'description': comp.docstring() if comp.docstring() else ''
              })
          json.dumps(result)
      except Exception as e:
          json.dumps([])
    `);
    
    if (result) {
      return JSON.parse(result);
    }
    return [];
  } catch (error) {
    console.warn('Jedi completion error:', error);
    return [];
  }
}

/**
 * Get documentation from Jedi for hover tooltips
 * Provides documentation for names before they've been executed
 *
 * @async
 * @param {string} name - Name to get documentation for
 * @returns {Promise<string|null>} Documentation string or null
 */
async function getJediDoc(name) {
  if (!jediModule || !pyodideLoaded) {
    return null;
  }

  try {
    const doc = await pyodide.runPythonAsync(`
      import jedi
      
      try:
          # Try to get documentation from Jedi
          script = jedi.Script('${name}')
          names = script.goto()
          if names:
              doc = names[0].docstring()
              doc if doc else None
          else:
              None
      except Exception:
          None
    `);
    
    return doc || null;
  } catch (error) {
    console.warn('Jedi doc error:', error);
    return null;
  }
}

// ============================================================================
// Shared Namespace Management
// ============================================================================

/**
 * Update shared namespace from Pyodide's global scope
 * Captures all user-defined names that can be used in subsequent cells
 *
 * @async
 * @function updateSharedNamespace
 */
async function updateSharedNamespace() {
  try {
    // Get all user-defined names (excluding special names)
    const userNames = await pyodide.runPythonAsync(`
      [name for name in dir() 
       if not name.startswith('_') and name not in 
       ['In', 'Out', 'get_ipython', 'exit', 'quit', 'show', 'show_table', 
        'check', 'text_input', 'dropdown', 'button', 'load_csv', 'jedi']]
    `);

    // Update shared namespace
    const newNamespace = { __builtins__: {} };
    for (const name of userNames) {
      try {
        const value = pyodide.globals.get(name);
        newNamespace[name] = value;
      } catch (e) {
        // Can't access this one (might be a module or special object)
      }
    }
    sharedNamespace = newNamespace;
  } catch (error) {
    console.warn('Failed to update shared namespace:', error);
  }
}

/**
 * Get documentation for a name from the running interpreter
 * Checks shared namespace first, then builtins
 *
 * @async
 * @param {string} name - Name to get documentation for
 * @returns {Promise<string|null>} Documentation string or null
 */
async function getDocForName(name) {
  try {
    // Check shared namespace first (user-defined)
    if (sharedNamespace[name]) {
      const doc = await pyodide.runPythonAsync(`
        import inspect
        obj = ${JSON.stringify(name)}
        if isinstance(obj, str):
            try:
                obj = eval(obj)
            except:
                pass
        doc = inspect.getdoc(obj)
        doc if doc else ""
      `);
      return doc || `User-defined: ${name}`;
    }

    // Check builtins
    const builtinDoc = await pyodide.runPythonAsync(`
      import inspect
      import builtins
      if hasattr(builtins, '${name}'):
          obj = getattr(builtins, '${name}')
          doc = inspect.getdoc(obj)
          doc if doc else ""
      else:
          ""
    `);

    if (builtinDoc) return builtinDoc;

    // Check imported modules
    const moduleDoc = await pyodide.runPythonAsync(`
      import inspect
      import sys
      for module_name, module in sys.modules.items():
          if module_name.startswith('_'):
              continue
          if hasattr(module, '${name}'):
              obj = getattr(module, '${name}')
              doc = inspect.getdoc(obj)
              if doc:
                  return f"[{module_name}] " + doc
      ""
    `);

    return moduleDoc || null;
  } catch (e) {
    console.warn('Failed to get doc for', name, e);
    return null;
  }
}

// ============================================================================
// Drag and Drop
// ============================================================================

/**
 * Setup drag and drop for cell reordering
 *
 * @function setupDragAndDrop
 */
function setupDragAndDrop() {
  if (!cellsContainer) return;

  // Drag start - when user starts dragging a cell header
  cellsContainer.addEventListener('dragstart', (e) => {
    if (e.target.classList.contains('mini-ide-cell-header')) {
      draggedCell = e.target.parentElement;
      e.target.parentElement.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', draggedCell.dataset.id);
    }
  });

  // Drag end - when drag operation ends
  cellsContainer.addEventListener('dragend', (e) => {
    if (draggedCell) {
      draggedCell.classList.remove('dragging');
      draggedCell = null;
    }
    removeDropPlaceholder();
  });

  // Drag over - show drop placeholder
  cellsContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    
    const targetCell = findCellElement(e.target);
    if (targetCell && targetCell !== draggedCell) {
      const rect = targetCell.getBoundingClientRect();
      const midY = rect.top + rect.height / 2;
      
      if (e.clientY < midY) {
        // Insert before target
        createDropPlaceholder(targetCell);
      } else {
        // Insert after target
        createDropPlaceholder(targetCell.nextElementSibling);
      }
    }
  });

  // Drag leave - remove placeholder when leaving container
  cellsContainer.addEventListener('dragleave', (e) => {
    const relatedTarget = e.relatedTarget;
    if (!relatedTarget || !cellsContainer.contains(relatedTarget)) {
      removeDropPlaceholder();
    }
  });

  // Drop - reorder cells
  cellsContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    
    if (!draggedCell) return;
    
    const dropId = e.dataTransfer.getData('text/plain');
    const draggedIndex = cells.findIndex(c => c.id === dropId);
    
    if (draggedIndex === -1) return;
    
    let insertIndex;
    const targetCell = findCellElement(e.target);
    
    if (targetCell && targetCell !== draggedCell) {
      const targetId = targetCell.dataset.id;
      const targetIndex = cells.findIndex(c => c.id === targetId);
      
      const rect = targetCell.getBoundingClientRect();
      const midY = rect.top + rect.height / 2;
      
      if (e.clientY < midY) {
        insertIndex = targetIndex;
      } else {
        insertIndex = targetIndex + 1;
      }
    } else {
      // Drop at end
      insertIndex = cells.length;
    }
    
    // Reorder cells array
    const [movedCell] = cells.splice(draggedIndex, 1);
    cells.splice(insertIndex, 0, movedCell);
    
    saveState();
    renderCells();
    
    draggedCell = null;
    removeDropPlaceholder();
    updateStatus('Cells reordered.');
  });
}

/**
 * Find the cell element from a target element
 * Walks up the DOM tree to find the cell container
 *
 * @param {HTMLElement} target - Target element
 * @returns {HTMLElement|null} Cell element or null
 */
function findCellElement(target) {
  let current = target;
  while (current && !current.classList.contains('mini-ide-cell')) {
    current = current.parentElement;
  }
  return current;
}

/**
 * Create a visual drop placeholder
 *
 * @param {HTMLElement} beforeEl - Element to insert placeholder before
 */
function createDropPlaceholder(beforeEl) {
  removeDropPlaceholder();
  
  dropPlaceholder = document.createElement('div');
  dropPlaceholder.className = 'mini-ide-drop-placeholder';
  
  if (beforeEl) {
    cellsContainer.insertBefore(dropPlaceholder, beforeEl);
  } else {
    cellsContainer.appendChild(dropPlaceholder);
  }
}

/**
 * Remove the drop placeholder
 */
function removeDropPlaceholder() {
  if (dropPlaceholder) {
    dropPlaceholder.remove();
    dropPlaceholder = null;
  }
}

// ============================================================================
// Download Functionality
// ============================================================================

/**
 * Download all cells as a Python file
 * Text cells become comments, Python cells remain as code
 *
 * @function downloadAsPython
 */
function downloadAsPython() {
  let pythonContent = '# Mini IDE Export\n';
  pythonContent += `# Generated by dewlab Mini IDE on ${new Date().toISOString().split('T')[0]}\n\n`;

  cells.forEach((cell, index) => {
    if (cell.type === CELL_TYPES.TEXT) {
      // Text cells become multi-line comments
      const lines = cell.content.split('\n');
      pythonContent += `# ===== Cell ${index + 1} (Text) =====\n`;
      lines.forEach(line => {
        pythonContent += `# ${line}\n`;
      });
      pythonContent += '\n';
    } else if (cell.type === CELL_TYPES.PYTHON) {
      pythonContent += `# ===== Cell ${index + 1} (Python) =====\n`;
      pythonContent += cell.content + '\n\n';
    }
  });

  downloadFile('mini-ide-export.py', pythonContent, 'text/x-python');
  updateStatus('Downloaded as Python file.');
}

/**
 * Download all cells as a standalone HTML file
 * Includes embedded Pyodide for offline execution
 *
 * @async
 * @function downloadAsHtml
 */
async function downloadAsHtml() {
  await ensurePyodide();
  
  const htmlContent = buildStandaloneHtml();
  downloadFile('mini-ide-export.html', htmlContent, 'text/html');
  updateStatus('Downloaded as HTML file.');
}

/**
 * Build standalone HTML content with embedded Pyodide
 *
 * @returns {string} Complete HTML document as string
 */
function buildStandaloneHtml() {
  const cellsData = cells.map(cell => ({
    type: cell.type,
    content: cell.content
  }));

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const themeStyles = isDark ? 
    '--dl-bg: #1e1e1e; --dl-bg-secondary: #252525; --dl-text: #e0e0e0; --dl-text-secondary: #999; --dl-border: #444; --dl-accent: #d4692a;' :
    '--dl-bg: #fff; --dl-bg-secondary: #f8f8f8; --dl-text: #333; --dl-text-secondary: #666; --dl-border: #ddd; --dl-accent: #d4692a;';

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mini IDE Export</title>
  <script src="https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js"></script>
  <style>
    :root {
      ${themeStyles}
      --dl-mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      --dl-error: #d32f2f;
      --dl-check-pass: #388e3c;
      --dl-check-fail: #d32f2f;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 1rem;
      background: var(--dl-bg);
      color: var(--dl-text);
    }
    
    h1 {
      color: var(--dl-heading, var(--dl-text));
      margin-bottom: 1rem;
    }
    
    .cell {
      margin-bottom: 1rem;
      border: 1px solid var(--dl-border);
      border-radius: 4px;
      background: var(--dl-bg);
      overflow: hidden;
    }
    
    .cell-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 0.75rem;
      background: var(--dl-bg-secondary);
      border-bottom: 1px solid var(--dl-border);
      font-size: 0.875rem;
    }
    
    .cell-type {
      font-weight: 600;
      color: var(--dl-text-secondary);
    }
    
    .cell-content {
      padding: 0.75rem;
      font-family: var(--dl-mono);
      font-size: 0.875rem;
      white-space: pre-wrap;
      word-break: break-all;
      background: var(--dl-bg);
    }
    
    .cell-output {
      padding: 0.75rem;
      background: var(--dl-bg-secondary);
      border-top: 1px solid var(--dl-border);
      font-family: var(--dl-mono);
      font-size: 0.875rem;
      white-space: pre-wrap;
      word-break: break-all;
    }
    
    .dl-error {
      color: var(--dl-error);
    }
    
    .dl-check {
      padding: 0.25rem 0.5rem;
      border-radius: 3px;
      margin: 0.25rem 0;
      font-size: 0.875rem;
    }
    
    .dl-check-pass {
      background: rgba(56, 142, 60, 0.1);
      color: var(--dl-check-pass);
    }
    
    .dl-check-fail {
      background: rgba(211, 47, 47, 0.1);
      color: var(--dl-check-fail);
    }
    
    pre {
      margin: 0;
      font-family: var(--dl-mono);
    }
    
    .status {
      padding: 0.5rem;
      margin-top: 1rem;
      background: var(--dl-bg-secondary);
      border-radius: 3px;
      font-size: 0.875rem;
      color: var(--dl-text-secondary);
    }
    
    .dl-table {
      border-collapse: collapse;
      margin: 0.5rem 0;
    }
    
    .dl-table th,
    .dl-table td {
      border: 1px solid var(--dl-border);
      padding: 0.25rem 0.5rem;
    }
    
    .dl-table th {
      background: var(--dl-bg-secondary);
      font-weight: 600;
    }
  </style>
</head>
<body>
  <h1>Mini IDE Export</h1>
  <div id="cells"></div>
  <div class="status" id="status">Loading Python runtime...</div>

  <script>
    const cellsData = ${JSON.stringify(cellsData)};
    let pyodide;
    let pyodideLoaded = false;

    async function init() {
      const statusEl = document.getElementById('status');
      
      try {
        pyodide = await loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/"
        });
        
        await pyodide.loadPackage(['numpy', 'pandas', 'matplotlib']);
        
        // Load tutorial tools
        await pyodide.runPythonAsync(
          "` + escapeHtmlForJs(getTutorialToolsCode()) + `"
        );
        
        pyodideLoaded = true;
        statusEl.textContent = 'Ready.';
        
        renderCells();
      } catch (error) {
        statusEl.textContent = 'Failed to load Python: ' + error.message;
        console.error('Failed to load Pyodide:', error);
      }
    }

    async function renderCells() {
      const cellsContainer = document.getElementById('cells');
      cellsContainer.innerHTML = '';
      
      for (let i = 0; i < cellsData.length; i++) {
        const cell = cellsData[i];
        const cellEl = document.createElement('div');
        cellEl.className = 'cell cell-' + cell.type;
        
        const header = document.createElement('div');
        header.className = 'cell-header';
        header.innerHTML = '<span class="cell-type">' + (cell.type === 'python' ? 'Python' : 'Text') + ' Cell ' + (i + 1) + '</span>';
        
        const content = document.createElement('div');
        content.className = 'cell-content';
        content.innerHTML = '<pre>' + escapeHtml(cell.content) + '</pre>';
        
        const output = document.createElement('div');
        output.className = 'cell-output';
        
        cellEl.appendChild(header);
        cellEl.appendChild(content);
        cellEl.appendChild(output);
        cellsContainer.appendChild(cellEl);
        
        // Run Python cells
        if (cell.type === 'python' && pyodideLoaded) {
          try {
            const result = await pyodide.runPythonAsync(cell.content);
            if (result !== undefined) {
              output.innerHTML += '<pre>' + escapeHtml(String(result)) + '</pre>';
            }
          } catch (error) {
            output.innerHTML = '<pre class="dl-error">' + escapeHtml(error.message) + '</pre>';
          }
        }
      }
    }

    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    // Start
    init();
  </script>
</body>
</html>`;
}

/**
 * Download all cells as a Jupyter Notebook
 *
 * @function downloadAsIpynb
 */
function downloadAsIpynb() {
  const notebook = buildNotebook();
  const jsonContent = JSON.stringify(notebook, null, 2);
  downloadFile('mini-ide-export.ipynb', jsonContent, 'application/json');
  updateStatus('Downloaded as Jupyter Notebook.');
}

/**
 * Build Jupyter Notebook structure
 *
 * @returns {Object} Jupyter Notebook JSON structure
 */
function buildNotebook() {
  const notebookCells = [];

  cells.forEach((cell, index) => {
    if (cell.type === CELL_TYPES.TEXT) {
      notebookCells.push({
        cell_type: 'markdown',
        metadata: {},
        source: cell.content.split('\n')
      });
    } else if (cell.type === CELL_TYPES.PYTHON) {
      notebookCells.push({
        cell_type: 'code',
        metadata: {},
        source: cell.content.split('\n'),
        execution_count: null,
        outputs: []
      });
    }
  });

  return {
    nbformat: 4,
    nbformat_minor: 5,
    metadata: {
      kernelspec: {
        display_name: 'Python 3',
        language: 'python',
        name: 'python3'
      },
      language_info: {
        name: 'python',
        version: '3.12.0',
        pygments_lexer: 'ipython3'
      }
    },
    cells: notebookCells
  };
}

/**
 * Download a file with the given content
 * Opens in new tab as requested
 *
 * @param {string} filename - Name of file to download
 * @param {string} content - File content
 * @param {string} mimeType - MIME type of file
 */
function downloadFile(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  
  // Open in new tab as requested
  a.target = '_blank';
  
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Format output for display
 * Handles various Python types appropriately
 *
 * @param {*} result - Python result to format
 * @returns {string} Formatted string
 */
function formatOutput(result) {
  if (result === undefined) return '';
  if (result === null) return 'None';
  if (typeof result === 'string') return result;
  if (typeof result === 'number') return String(result);
  if (typeof result === 'boolean') return String(result);
  return JSON.stringify(result, null, 2);
}

/**
 * Format error for display
 * Extracts meaningful error message from Pyodide errors
 *
 * @param {Error|Object} error - Error to format
 * @returns {string} Formatted error string
 */
function formatError(error) {
  if (typeof error === 'string') return error;
  if (error.python_error) return error.python_error;
  if (error.message) return error.message;
  return String(error);
}

/**
 * Truncate error message for status display
 *
 * @param {string} error - Error message
 * @param {number} [maxLength=60] - Maximum length
 * @returns {string} Truncated error
 */
function truncateError(error, maxLength = 60) {
  if (!error) return '';
  const str = String(error);
  return str.length > maxLength ? str.substring(0, maxLength) + '...' : str;
}

/**
 * Escape HTML special characters
 *
 * @param {string} text - Text to escape
 * @returns {string} Escaped HTML
 */
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Escape HTML for JavaScript string literal
 *
 * @param {string} text - Text to escape
 * @returns {string} Escaped string safe for JS
 */
function escapeHtmlForJs(text) {
  return text
    .replace(/\\/g, '\\\\')
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r')
    .replace(/\t/g, '\\t')
    .replace(/"/g, '\\"')
    .replace(/'/g, '\\\'')
    .replace(/`/g, '\\`')
    .replace(/\$/g, '\\$');
}

/**
 * Update status message
 *
 * @param {string} message - Status message
 * @param {boolean} [isError=false] - Whether this is an error message
 */
function updateStatus(message, isError = false) {
  if (!statusEl) return;
  
  statusEl.textContent = message;
  statusEl.className = 'mini-ide-status' + (isError ? ' error' : '');
  
  // Clear after 3 seconds if not an error
  if (!isError) {
    setTimeout(() => {
      if (statusEl.textContent === message) {
        statusEl.textContent = '';
        statusEl.className = 'mini-ide-status';
      }
    }, 3000);
  }
}

/**
 * Update all editor themes when global theme changes
 *
 * @param {boolean} isDark - Whether dark mode is enabled
 */
function updateAllEditorThemes(isDark) {
  cells.forEach(cell => {
    if (cell.editor) {
      try {
        setEditorTheme(cell.editor, isDark);
      } catch (e) {
        // Editor might not support theme changes
      }
    }
  });
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
  return `
import html
import json
import sys
import traceback
import warnings
import io
import base64

# Suppress matplotlib backend warning
warnings.filterwarnings("ignore", message="FigureCanvasAgg is non-interactive")

# Global state for the current cell
_current_cell_id = None
_current_output_element = None

class _OutputCapture:
    """Capture stdout for display in cell output."""
    def __init__(self):
        self.outputs = []
        
    def write(self, text):
        self.outputs.append(text)
        
    def flush(self):
        pass

def _format_value(value):
    """Format a Python value for display."""
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    try:
        import pandas as pd
        if isinstance(value, (pd.DataFrame, pd.Series)):
            return _format_dataframe(value)
    except ImportError:
        pass
    try:
        import numpy as np
        if isinstance(value, np.ndarray):
            return _format_array(value)
    except ImportError:
        pass
    return repr(value)

def _format_dataframe(df):
    """Format a DataFrame as HTML table."""
    html_parts = ['<table class="dl-table">']
    html_parts.append('<thead><tr>')
    for col in df.columns:
        html_parts.append(f'<th>{html.escape(str(col))}</th>')
    html_parts.append('</tr></thead>')
    html_parts.append('<tbody>')
    for i, row in enumerate(df.head(20).itertuples()):
        html_parts.append('<tr>')
        for val in row[1:]:
            html_parts.append(f'<td>{html.escape(str(val))}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody></table>')
    if len(df) > 20:
        html_parts.append(f'<p><em>Showing 20 of {len(df)} rows</em></p>')
    return '\\n'.join(html_parts)

def _format_array(arr):
    """Format a numpy array."""
    return repr(arr)

def show(*values, label=None):
    """Render something mid-cell."""
    if _current_output_element is None:
        return
    html_parts = []
    for value in values:
        html_parts.append(_format_value(value))
    result = ' '.join(html_parts)
    if label:
        result = f'<strong>{html.escape(label)}:</strong> {result}'
    _current_output_element.innerHTML += result

def show_table(frame, max_rows=20, caption=None):
    """Render a DataFrame as a table."""
    if _current_output_element is None:
        return
    html_str = _format_dataframe(frame)
    if caption:
        html_str = f'<figcaption>{html.escape(caption)}</figcaption>' + html_str
    _current_output_element.innerHTML += html_str

def check(actual, expected, tolerance=None, label=None):
    """Check if actual equals expected, with tolerance for floats."""
    import math
    
    if _current_output_element is None:
        return False
    
    # Handle different types
    is_equal = False
    
    if isinstance(actual, float) and isinstance(expected, float):
        if tolerance is None:
            tolerance = 1e-9
        is_equal = math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)
    elif isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        if len(actual) != len(expected):
            is_equal = False
        else:
            is_equal = all(check(a, e, tolerance) for a, e in zip(actual, expected))
    elif hasattr(actual, '__eq__'):
        # Special case: True != 1, False != 0
        if isinstance(actual, bool) or isinstance(expected, bool):
            is_equal = actual is expected
        else:
            try:
                is_equal = actual == expected
            except (TypeError, ValueError):
                is_equal = False
    else:
        is_equal = actual == expected
    
    # Format message
    if is_equal:
        msg = label or "That\\'s right."
        _current_output_element.innerHTML += f'<div class="dl-check dl-check-pass">{html.escape(msg)}</div>'
    else:
        msg = label or "Not quite yet."
        _current_output_element.innerHTML += f'<div class="dl-check dl-check-fail">{html.escape(msg)}</div>'
    
    return is_equal

class _Widget:
    """Base class for interactive widgets."""
    def __init__(self, label, widget_id=None):
        self.label = label
        self.id = widget_id or f"{label.lower().replace(' ', '-')}-{id(self)}"
        self.value = None

class _TextInput(_Widget):
    """Text input widget."""
    def __init__(self, label, value="", widget_id=None):
        super().__init__(label, widget_id)
        self.value = value
        self.type = "text"

class _Dropdown(_Widget):
    """Dropdown widget."""
    def __init__(self, label, options, value=None, widget_id=None):
        super().__init__(label, widget_id)
        self.options = options
        self.value = value if value is not None else (options[0] if options else None)
        self.type = "dropdown"

class _Button(_Widget):
    """Button widget."""
    def __init__(self, label, on_click, widget_id=None):
        super().__init__(label, widget_id)
        self.on_click = on_click
        self.type = "button"

def text_input(label, value="", widget_id=None):
    """Create a text input widget."""
    widget = _TextInput(label, value, widget_id)
    if _current_output_element:
        widget_id = widget.id
        _current_output_element.innerHTML += f'''
        <div class="dl-widget dl-widget-text" data-widget-id="{widget_id}">
            <label>{html.escape(label)}: <input type="text" value="{html.escape(widget.value)}" data-widget-id="{widget_id}"></label>
        </div>
        '''
    return widget

def dropdown(label, options, value=None, widget_id=None):
    """Create a dropdown widget."""
    widget = _Dropdown(label, options, value, widget_id)
    if _current_output_element:
        widget_id = widget.id
        options_html = ''.join(f'<option value="{html.escape(o)}"{" selected" if o == widget.value else ""}>{html.escape(o)}</option>' for o in options)
        _current_output_element.innerHTML += f'''
        <div class="dl-widget dl-widget-dropdown" data-widget-id="{widget_id}">
            <label>{html.escape(label)}: <select data-widget-id="{widget_id}">{options_html}</select></label>
        </div>
        '''
    return widget

def button(label, on_click, widget_id=None):
    """Create a button widget."""
    widget = _Button(label, on_click, widget_id)
    if _current_output_element:
        widget_id = widget.id
        _current_output_element.innerHTML += f'''
        <div class="dl-widget dl-widget-button" data-widget-id="{widget_id}">
            <button type="button" data-widget-id="{widget_id}">{html.escape(label)}</button>
        </div>
        '''
    return widget

async def load_csv(name):
    """Load a CSV file from the data directory."""
    import pandas as pd
    import io
    
    # In Mini IDE, we need to fetch the CSV
    try:
        from js import fetch
        response = await fetch(f"data/{name}")
        if response.ok:
            text = await response.text()
            return pd.read_csv(io.StringIO(text))
        else:
            raise FileNotFoundError(f"Could not find data/{name}")
    except Exception as e:
        raise FileNotFoundError(f"Could not load {name}: {e}")
  `;
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
