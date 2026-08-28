# Mini IDE

The Mini IDE is a lightweight, browser-based integrated development environment
that allows students to create, edit, and run Python code cells alongside text
documentation cells. It is designed to provide a familiar notebook-like experience
while maintaining the simplicity and zero-installation philosophy of dewlab.

---

## Overview

The Mini IDE provides:

- **Cell-based interface**: Create and manage Python and Text cells
- **Code execution**: Run Python code directly in the browser using Pyodide
- **Persistence**: All work is automatically saved to the browser's localStorage
- **Drag-and-drop**: Reorder cells by dragging their headers
- **Full API support**: All `tutorial_tools.py` functions are available
- **Download options**: Export work as Python, HTML, or Jupyter Notebook

---

## Quick Start

### Opening the Mini IDE

1. From the dewlab contents page, click the **Mini IDE** link in the introduction
2. Or navigate directly to `mini-ide.html`
3. The Mini IDE opens in a new tab

### Creating Your First Cell

1. Click **"+ Python Cell"** to add a code cell
2. Type some Python code, for example:
   ```python
   print("Hello, World!")
   x = 42
   x * 2
   ```
3. Click **Run** or press Shift+Enter to execute the cell
4. The output appears below the cell

### Adding Documentation

1. Click **"+ Text Cell"** to add a text cell
2. Type documentation, comments, or explanations
3. Text cells are rendered as formatted text

### Running All Cells

Click **"Run All"** to execute all Python cells in order. Cells share a common
namespace, so variables and functions defined in one cell are available in
subsequent cells.

### Reordering Cells

Drag a cell by its header and drop it in a new position. The cells will be
executed in the new order when you run all.

### Downloading Your Work

- **Download .py**: Exports as a Python file with text cells as comments
- **Download .html**: Creates a standalone HTML file that works offline
- **Download .ipynb**: Exports as a Jupyter Notebook

All downloads open in a new tab.

---

## User Interface

### Toolbar

| Button | Description |
|--------|-------------|
| + Python Cell | Add a new Python code cell |
| + Text Cell | Add a new text/markdown cell |
| Run All | Execute all cells in order |
| Clear All | Remove all cells (with confirmation) |
| Download .py | Export as Python file |
| Download .html | Export as standalone HTML |
| Download .ipynb | Export as Jupyter Notebook |

### Cell Types

#### Python Cells

- Executable Python code
- Syntax highlighting via CodeMirror
- Autocomplete for:
  - Python keywords
  - Built-in functions and types
  - Local variables (names defined in the same cell)
  - Names from the shared namespace (previous cells)
  - Jedi-based pre-execution completion
- Hover documentation for:
  - User-defined names
  - Built-in functions
  - Imported module members
- Run button executes the cell

#### Text Cells

- Plain text or markdown-style documentation
- Useful for:
  - Comments and explanations
  - Section headers
  - Notes and reminders
- No execution, just display

### Cell Header

Each cell has a header containing:
- **Cell type indicator**: "Python" or "Text"
- **Run button**: (Python cells only) Execute the cell
- **Delete button**: Remove the cell

The header is also the drag handle for reordering.

### Output Area

- Displays the result of cell execution
- Shows printed output
- Displays the value of the last expression
- Renders DataFrames as tables
- Shows matplotlib figures
- Displays errors with formatted tracebacks

---

## Available Functions

The Mini IDE provides the same API as dewlab tutorials through the
`tutorial_tools.py` module:

### Display Functions

| Function | Description |
|----------|-------------|
| `show(*values, label=None)` | Render values mid-cell |
| `show_table(frame, max_rows=20, caption=None)` | Render a DataFrame as a table |

### Verification

| Function | Description |
|----------|-------------|
| `check(actual, expected, tolerance=None, label=None)` | Verify an answer with instant feedback |

### Input Widgets

| Function | Description |
|----------|-------------|
| `text_input(label, value="", id=None)` | Create a text input box |
| `dropdown(label, options, value=None, id=None)` | Create a dropdown selector |
| `button(label, on_click)` | Create a clickable button |

### Data Loading

| Function | Description |
|----------|-------------|
| `await load_csv(name)` | Load a CSV file from the data directory |

### Example Usage

```python
# Display functions
show("The answer is:", 42)
show_table(my_dataframe, caption="My Data")

# Verification
check(my_answer, 100, label="Correct!")

# Widgets
temp = text_input("Enter temperature")
unit = dropdown("Unit", ["Celsius", "Fahrenheit"])

# Data loading
data = await load_csv("my-data.csv")
```

---

## Autocomplete and Documentation

### Static Autocomplete

Available immediately, without running the cell:

- **Keywords**: `if`, `for`, `while`, `def`, `return`, etc.
- **Builtins**: `print`, `len`, `range`, `list`, `dict`, etc.
- **Local names**: Names you've typed in the current cell

### Live Autocomplete

Available after the cell has run:

- **User-defined names**: Variables and functions you've created
- **Imported modules**: Names from modules you've imported

### Hover Documentation

Hover over any name to see its documentation:

- **User-defined**: Shows the docstring you wrote
- **Builtins**: Shows Python's built-in documentation
- **Imported**: Shows documentation from the module

### Jedi Integration

For pre-execution completion (before running the cell):

- Jedi runs inside Pyodide
- Provides completion for:
  - Standard library functions
  - Imported module members
  - Class attributes
  - Function parameters
- Works even before the cell has been executed

**Note**: Jedi adds approximately 500KB to the initial load, but only loads when
the Mini IDE is first used.

---

## Persistence

### Automatic Saving

- All cells are automatically saved to localStorage
- Saves on every change (content edit, cell add/remove, reorder)
- No manual save required

### What is Saved

- Cell type (Python or Text)
- Cell content
- Cell order
- Cell ID (for stable references)

### What is NOT Saved

- Cell output (recomputed on load)
- Pyodide state (reloads on each session)
- Widget values (reset on reload)

### LocalStorage Keys

| Key | Purpose |
|-----|---------|
| `mini-ide:cells:v1` | All cell data |
| `mini-ide:helper-visible` | Whether helper text is shown |

---

## Download Formats

### Python File (.py)

```python
# Mini IDE Export
# Generated by dewlab Mini IDE on 2025-01-15

# ===== Cell 1 (Text) =====
# This is a comment
# explaining what the code does

# ===== Cell 2 (Python) =====
print("Hello, World!")
x = 42
x * 2
```

**Features:**
- Text cells become Python comments
- Python cells remain as executable code
- Cells are separated with headers
- Preserves original formatting

### HTML File (.html)

A standalone HTML file that:
- Includes embedded Pyodide
- Works offline after first load (Pyodide cached)
- Has the same styling as the Mini IDE
- Can be opened in any browser
- Executes cells automatically on load

**Use cases:**
- Sharing work with others
- Running without internet (after first load)
- Embedding in other pages

### Jupyter Notebook (.ipynb)

A valid Jupyter Notebook JSON file that:
- Can be opened in Jupyter Notebook
- Can be opened in JupyterLab
- Can be opened in Google Colab
- Preserves cell types and order

**Structure:**
- Text cells → Markdown cells
- Python cells → Code cells
- Includes standard Jupyter metadata

---

## Technical Details

### Architecture

```
+------------------+
|   Mini IDE       |
|  +------------+  |
|  | HTML/CSS   |  |
|  +------------+  |
|  | mini-ide.js|  <--+ Cell management
|  +------------+  |  |
|  | CodeMirror |  <--+-- Editing
|  +------------+  |  |
|  | Pyodide    |  <--+-- Execution
|  +------------+  |  |
|  | Jedi       |  <--+-- Pre-execution completion
|  +------------+  |
+------------------+
        |
        v
+------------------+
| localStorage     |  <-- Persistence
+------------------+
```

### Pyodide Configuration

- **Version**: 0.28.3 (matches tutorials)
- **CDN**: jsDelivr
- **Default packages**: numpy, pandas, matplotlib, jedi
- **Loading**: Lazy (on first cell execution)

### Shared Namespace

All Python cells share a common namespace, similar to Jupyter:

```python
# Cell 1
x = 10

# Cell 2
y = x * 2  # y = 20, x is available from Cell 1
```

The namespace is reset when:
- "Run All" is clicked
- The page is reloaded

### Execution Order

Cells are executed in the order they appear in the UI. When you:
- Click **Run** on a cell: Only that cell executes
- Click **Run All**: All cells execute in order, top to bottom
- Drag to reorder: The new order is used for subsequent "Run All"

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Indent or accept completion |
| Shift+Tab | Outdent |
| Enter | Accept completion or insert newline |
| Escape | Close completion list or leave cell |
| Ctrl+Z | Undo (in editor) |
| Ctrl+Y | Redo (in editor) |
| Ctrl+A | Select all (in editor) |
| Ctrl+C | Copy (in editor) |
| Ctrl+V | Paste (in editor) |
| Ctrl+X | Cut (in editor) |

---

## Troubleshooting

### Pyodide Not Loading

**Symptom**: "Loading Python runtime..." message never disappears

**Causes**:
- No internet connection
- CDN blocked by firewall/proxy
- Browser security restrictions

**Solutions**:
- Check internet connection
- Try a different browser
- Wait a moment (Pyodide is ~10MB)
- Try refreshing the page

### Cells Not Running

**Symptom**: Clicking Run does nothing

**Causes**:
- Pyodide not loaded yet
- Syntax error in code
- Browser console error

**Solutions**:
- Wait for Pyodide to load
- Check browser console (F12) for errors
- Fix syntax errors

### Autocomplete Not Working

**Symptom**: No completion suggestions appear

**Causes**:
- Jedi not loaded
- Pyodide not loaded
- Browser console error

**Solutions**:
- Run a cell first (triggers Jedi load)
- Check browser console for errors
- Try refreshing the page

### Download Not Working

**Symptom**: Clicking download does nothing

**Causes**:
- Browser popup blocker
- No cells to download

**Solutions**:
- Allow popups for this site
- Add at least one cell
- Try a different browser

---

## Browser Support

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Recommended |
| Firefox | ✅ Full | Works well |
| Safari | ✅ Full | Works well |
| Edge | ✅ Full | Works well |
| Mobile Chrome | ✅ Most | Some UI limitations |
| Mobile Safari | ⚠️ Partial | Limited testing |

**Requirements:**
- ES6 module support
- WebAssembly support
- localStorage support
- Fetch API support

---

## Performance

### Initial Load

- **Base page**: ~50KB (HTML + CSS + JS)
- **Pyodide**: ~10MB (loaded on demand)
- **Jedi**: ~500KB (loaded with Pyodide)
- **Total**: ~10.5MB (only when first cell runs)

### Memory Usage

- **Per cell**: Minimal (just text)
- **Pyodide**: ~50-100MB (kept in memory)
- **Total**: Scales with number of cells

### Execution Speed

- **Simple operations**: Instant
- **Complex operations**: Depends on code
- **Matplotlib**: ~1-2 seconds for simple plots
- **Pandas**: Fast for small datasets

---

## Limitations

1. **No Internet = No Pyodide**: Pyodide must be loaded from CDN on first use
2. **No Persistence Between Devices**: Work is saved per browser/device
3. **No Collaboration**: Cannot share live sessions
4. **Limited Widgets**: Widgets are static in downloaded files
5. **No Debugger**: Cannot step through code
6. **Memory Limits**: Browser memory limits apply

---

## Comparison with Other Tools

| Feature | Mini IDE | Jupyter | Colab | VS Code |
|---------|----------|---------|-------|---------|
| Browser-based | ✅ | ❌ | ✅ | ❌ |
| Zero install | ✅ | ❌ | ❌ | ❌ |
| Offline support | ⚠️ (after first load) | ❌ | ❌ | ✅ |
| Cell-based | ✅ | ✅ | ✅ | ❌ |
| Autocomplete | ✅ | ✅ | ✅ | ✅ |
| Persistence | ✅ (localStorage) | ⚠️ (server) | ✅ (Google Drive) | ✅ (local) |
| Download as .py | ✅ | ❌ | ✅ | ✅ |
| Download as .ipynb | ✅ | ✅ | ✅ | ❌ |
| Download as .html | ✅ | ❌ | ❌ | ❌ |
| Shared namespace | ✅ | ✅ | ✅ | ❌ |
| tutorial_tools.py API | ✅ | ❌ | ❌ | ❌ |

---

## Future Enhancements

The following features are planned or considered for future versions:

- **Signature help**: Parameter hints on typing `(`
- **Code folding**: Collapse/expand code blocks
- **Cell output folding**: Hide/show output
- **Multiple tabs**: Organize cells into tabs
- **Import/export**: Load previously saved sessions
- **Keyboard shortcuts**: More IDE-like shortcuts
- **Themes**: More color themes
- **Font size**: Adjustable font size

---

## Contributing

To contribute to the Mini IDE:

1. **Report bugs**: Open an issue on GitHub
2. **Suggest features**: Open an issue or discussion
3. **Submit code**: Open a pull request
4. **Test**: Try the Mini IDE and report issues

### Development Setup

```bash
# Clone the repository
git clone https://github.com/deweydex/dewlab
cd dewlab

# Install build dependencies
pip install -r requirements-build.txt

# Build the site
python3 build.py

# Start local server
python3 -m http.server -d site 8000

# Open Mini IDE
# http://localhost:8000/mini-ide.html
```

### File Structure

```
assets/
├── mini-ide.html          # Main HTML page
├── mini-ide.js            # Core JavaScript logic
├── mini-ide-style.css     # Styling
└── vendor/
    ├── codemirror.bundle.js  # CodeMirror (includes Jedi support)
    └── ...
```

### Code Style

The Mini IDE follows the same style guidelines as the rest of dewlab:

- **JavaScript**: ES6+ modules
- **Comments**: JSDoc style
- **Naming**: camelCase for variables and functions
- **Constants**: UPPER_CASE with underscores
- **Error handling**: Try/catch with meaningful messages
- **Async**: Use async/await for clarity

---

## License

The Mini IDE is part of dewlab and is licensed under the same terms.
See [LICENSE.md](../LICENSE.md) for details.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-XX | Initial release |
