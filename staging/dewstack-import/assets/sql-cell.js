/* The data track's cell engine: a fenced ```sql cell=name``` block
 * build.py turns into a `.dl-sql-cell`, and a fenced ```py cell=name```
 * block into a `.dl-py-cell`, both running real Python (SQLite for one,
 * pandas and matplotlib for the other) through Pyodide in the reader's
 * own browser tab. No server, no database anywhere but here.
 *
 * The full-stack module's own cell kind lives here too: consecutive
 * ```html app=name```/```css app=name```/```js app=name``` blocks
 * become one `.dl-app-cell` (build.py's extract_app_cells()), whose
 * JavaScript pane gets `dlQuery(dbName, sql, params)` — a real call
 * into `assets/sql_tools.py`'s `query_rows()`, no separate document to
 * bridge across the way the site editor's sandboxed preview would need.
 *
 * Ported in shape from dewlab's assets/pyodide-engine.js (its main-thread
 * path, not the Worker one — a query or a chart on a student-sized
 * table finishes fast enough that the page staying responsive during a
 * runaway one is not a problem worth a whole postMessage protocol to
 * solve) and its tutorial_tools.py, trimmed hard: dewstack's cells have
 * no widgets and no notebook-wide state, so none of that file's
 * check()/widget machinery comes with it. assets/sql_tools.py and
 * assets/python_tools.py are the two trimmed Python halves, one per
 * cell kind.
 *
 * One Pyodide, one engine, everywhere — decided 2026-09-05, so a page
 * that needs pandas and matplotlib (Data Arc 2) and a page that only
 * ever needs sqlite3 (Data Arc 1) still share the same code path,
 * rather than two engines to keep in step, and a page mixing both cell
 * kinds (a query charted in the next cell down) shares one Pyodide
 * between them rather than running two. What actually downloads is not
 * one fixed bundle, though: build.py already knows, at build time,
 * exactly which fenced blocks are on a page, so it writes that page's
 * own real package list into `window.DEWSTACK_SQL_PACKAGES` — sqlite3
 * alone for a page with only SQL cells, sqlite3 plus pandas and
 * matplotlib once a page has a Python cell. No page pays for a package
 * its own content never imports; python_tools.py is only fetched and
 * imported at all when the page has at least one `.dl-py-cell`.
 *
 * One Pyodide boots per page, shared by every cell on it; assets/
 * sql_tools.py keeps one sqlite3 connection per `data-db` name and
 * assets/python_tools.py keeps one namespace per `data-name`, so cells
 * sharing a name see the same tables or variables and cells with
 * different names never do — but that state, like the rest of Pyodide,
 * is gone the moment the page is left. A `data-persist` SQL cell is the
 * exception: its script is also kept in the browser's own localStorage,
 * keyed by `data-db`, and restored and rerun automatically the next
 * time a page with a persisted cell of that name loads. Download and
 * Load still work underneath this, unchanged, for taking a table out of
 * the browser or bringing one in.
 *
 * A fenced ```sql-check db=... task=...``` block becomes a `.dl-sql-check`
 * button instead: clicking it calls the named `check_*` function in
 * sql_tools.py against `db`'s connection and shows what it says. A quiz's
 * self-check, not a grade — instant, and nothing here sends the result
 * anywhere.
 */

(function () {
  "use strict";

  const PYODIDE_VERSION = "0.28.3";

  /* Captured now, synchronously: document.currentScript is only set while
   * this script is first executing, not once boot() below is running as a
   * later microtask after an await. */
  const OWN_SCRIPT_URL = document.currentScript ? document.currentScript.src : null;

  /* A CDN by default, the same one dewlab defaults to. A page can override
   * this before this script runs, the same way dewlab's DEWLAB_PYODIDE_BASE
   * does, to point at a self-hosted copy instead — a path relative to this
   * script's own folder, e.g. "./vendor/pyodide/" (populated by tools/
   * fetch_pyodide.py). Resolved to an absolute URL here, against this
   * script's own location the same way sql_tools.py's URL is below: Pyodide
   * re-resolves indexURL itself once it's running, against the page rather
   * than the script, so a relative value has to be made absolute before it
   * gets there, or the two resolutions disagree. */
  function pyodideBase() {
    const configured =
      window.DEWSTACK_PYODIDE_BASE ||
      `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
    return OWN_SCRIPT_URL ? new URL(configured, OWN_SCRIPT_URL).href : configured;
  }

  let booting = null; // the one boot() Promise every cell shares
  let tools = null; // the imported sql_tools Python module, once ready
  let pyTools = null; // the imported python_tools Python module, once ready (only if the page has a py cell)

  function statusElements(cells, pyCells, appCells) {
    const sqlStatus = cells.map((cell) => cell.querySelector(".dl-sql-status"));
    const pyStatus = pyCells.map((cell) => cell.querySelector(".dl-py-status"));
    const appStatus = (appCells || []).map((cell) => cell.querySelector(".dl-app-status"));
    return sqlStatus.concat(pyStatus, appStatus).filter(Boolean);
  }

  function setStatus(statuses, text) {
    statuses.forEach((status) => {
      status.textContent = text;
    });
  }

  /* Fetches one Python module's source and writes it into Pyodide's own
   * filesystem so `pyimport()` can find it — the same two steps for
   * sql_tools.py and, when the page has a py cell, python_tools.py. */
  async function loadModule(pyodide, filename) {
    const url = OWN_SCRIPT_URL ? new URL(filename, OWN_SCRIPT_URL).href : filename;
    const source = await fetch(url).then((r) => {
      if (!r.ok) throw new Error(`${filename}: HTTP ${r.status}`);
      return r.text();
    });
    pyodide.FS.writeFile(`/home/pyodide/${filename}`, source, { encoding: "utf8" });
    return pyodide.pyimport(filename.replace(/\.py$/, ""));
  }

  async function boot(cells, pyCells, appCells) {
    const statuses = statusElements(cells, pyCells, appCells);
    setStatus(statuses, "Starting Python…");
    const base = pyodideBase();
    const { loadPyodide } = await import(/* webpackIgnore: true */ base + "pyodide.mjs");
    const pyodide = await loadPyodide({ indexURL: base });

    /* build.py writes this page's own real package list — just what its
     * fenced blocks actually need, no more. Falls back to sqlite3 alone
     * if the variable is somehow missing, since every page using this
     * script has at least one SQL cell, check, or Python cell. */
    const packages = window.DEWSTACK_SQL_PACKAGES || ["sqlite3"];
    setStatus(statuses, `Loading ${packages.join(", ")}…`);
    await pyodide.loadPackage(packages);

    setStatus(statuses, "Preparing the cell…");
    tools = await loadModule(pyodide, "sql_tools.py");
    if (pyCells.length) pyTools = await loadModule(pyodide, "python_tools.py");

    /* A full-stack cell's own bridge: its JavaScript pane gets this
     * function directly (see extract_app_cells()'s docstring in build.py
     * for why there is no iframe to cross instead), a thin wrapper round
     * sql_tools.py's query_rows() that hands back a plain JS array of
     * plain objects rather than a PyProxy the reader would have to know
     * how to unwrap. */
    if (appCells && appCells.length) {
      window.dlQuery = async (dbName, sql, params) => {
        const rows = tools.query_rows(dbName, sql, params || []);
        return rows.toJs({ dict_converter: Object.fromEntries });
      };
    }

    setStatus(statuses, "");
  }

  function ensureBooted(cells, pyCells, appCells) {
    if (!booting) booting = boot(cells, pyCells, appCells).catch((err) => {
      setStatus(statusElements(cells, pyCells, appCells), "Python didn't start. Reloading the page usually fixes this.");
      booting = null; // a later click can try again rather than staying stuck
      throw err;
    });
    return booting;
  }

  /* A `data-persist` cell's script lives in the reader's own browser
   * storage, keyed by its `data-db` name, so it survives a reload of this
   * page or a visit to a later page sharing that name — the mechanism a
   * plain cell has no use for, since its table is meant to live only as
   * long as this one page's Pyodide does. localStorage can throw (private
   * browsing, a blocked origin, a full quota); every use below is wrapped
   * so that failure just means this one visit doesn't persist, not that
   * the cell stops working. */
  function storageKey(cell) {
    return `dewstack-sql:${cell.dataset.db}`;
  }

  function isPersisted(cell) {
    return cell.dataset.persist === "true";
  }

  function savePersisted(cell) {
    if (!isPersisted(cell)) return;
    try {
      localStorage.setItem(storageKey(cell), cell.querySelector(".dl-sql-input").value);
    } catch (err) {
      /* this visit's table just won't be there on the next */
    }
  }

  function clearPersisted(cell) {
    if (!isPersisted(cell)) return;
    try {
      localStorage.removeItem(storageKey(cell));
    } catch (err) {
      /* nothing to clear if storage was never reachable */
    }
  }

  /* Restores a persisted cell's saved text into its textarea, if there is
   * any yet. Returns whether it found something, so the caller knows this
   * cell needs an automatic first run once Python is ready — the restored
   * table should already be there, not waiting on a click nobody knows to
   * make. */
  function restorePersisted(cell) {
    if (!isPersisted(cell)) return false;
    try {
      const saved = localStorage.getItem(storageKey(cell));
      if (saved === null) return false;
      cell.querySelector(".dl-sql-input").value = saved;
      return true;
    } catch (err) {
      return false;
    }
  }

  async function runCell(cell, cells, pyCells, appCells) {
    const input = cell.querySelector(".dl-sql-input");
    const output = cell.querySelector(".dl-sql-output");
    const runButton = cell.querySelector(".dl-sql-run");
    const dbName = cell.dataset.db;

    savePersisted(cell);
    runButton.disabled = true;
    try {
      await ensureBooted(cells, pyCells, appCells);
      output.innerHTML = tools.run_sql(dbName, input.value);
    } catch (err) {
      output.innerHTML = `<p class="dl-sql-error">${String(err)}</p>`;
    } finally {
      runButton.disabled = false;
    }
  }

  function resetCell(cell, original) {
    const input = cell.querySelector(".dl-sql-input");
    const output = cell.querySelector(".dl-sql-output");
    input.value = original;
    output.innerHTML = "";
    clearPersisted(cell);
    if (tools) tools.reset(cell.dataset.db);
  }

  /* Saves the cell's current text as a .sql file — the same idea as the
   * site editor's "Download these files" button, for taking a copy of a
   * persisted table out of the browser (a different computer, a
   * submission), or keeping one from a cell with no persistence at all. */
  function downloadCell(cell) {
    const input = cell.querySelector(".dl-sql-input");
    const blob = new Blob([input.value], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${cell.dataset.db}.sql`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  /* Reads a file straight into the textarea. Loading only fills the box —
   * a reader still clicks Run, the same as if they had typed it, so a
   * loaded file never runs SQL nobody chose to run. A persisted cell's
   * loaded file becomes its new saved copy, so the next page still sees
   * whatever was just brought in rather than what was there before. */
  function loadCell(cell, file) {
    const input = cell.querySelector(".dl-sql-input");
    file.text().then((text) => {
      input.value = text;
      savePersisted(cell);
    });
  }

  /* Kept well under any server's practical URL-length limit (commonly
   * ~8000 characters) — code and output are the only two fields on a
   * cell's report link that can run long, so they are the only two this
   * ever has to shorten. */
  const REPORT_CODE_LIMIT = 2500;
  const REPORT_OUTPUT_LIMIT = 1500;

  function truncateForReport(text, limit) {
    if (text.length <= limit) return text;
    return `${text.slice(0, limit)}\n… (cut off here — paste the rest yourself if it matters)`;
  }

  /* Fills in the two fields build.py's cell_report_markup() could not:
   * this cell's code exactly as the reader has it right now, and
   * whatever its output area is currently showing (an error included —
   * runCell()/runPyCell() both write an error straight into that same
   * area, same as any other result). Called once, right as the panel
   * opens, not kept in sync on every keystroke. */
  function updateCellReportLinks(box, code, outputText) {
    const truncatedCode = truncateForReport(code, REPORT_CODE_LIMIT);
    const truncatedOutput = truncateForReport(outputText.trim(), REPORT_OUTPUT_LIMIT);
    const browser = navigator.userAgent;
    box.querySelectorAll(".dl-report-issue-link").forEach((link) => {
      const url = new URL(link.href);
      url.searchParams.set("code", truncatedCode);
      if (truncatedOutput) url.searchParams.set("output", truncatedOutput);
      url.searchParams.set("browser", browser);
      link.href = url.toString();
    });
  }

  /* Wires a cell's own report icon — the same open/close-a-panel-below
   * shape build.py's cell_report_markup() comment describes, shared by
   * both a SQL cell and a Python cell since only which input/output
   * elements to read differs between them. */
  function setUpReport(cell, input, output) {
    const icon = cell.querySelector(".dl-report-icon");
    const box = cell.querySelector(".dl-report-doors");
    if (!icon || !box) return;
    icon.addEventListener("click", () => {
      const open = icon.getAttribute("aria-expanded") === "true";
      icon.setAttribute("aria-expanded", String(!open));
      box.hidden = open;
      if (!open) updateCellReportLinks(box, input.value, output.innerText);
    });
  }

  /* Wires up one cell's buttons and restores its saved text if it is a
   * persisted cell with something already saved. Returns whether it was
   * restored, so the caller can give it its automatic first run. */
  function setUp(cell, cells, pyCells, appCells) {
    const input = cell.querySelector(".dl-sql-input");
    const original = input.value;
    const loadInput = cell.querySelector(".dl-sql-load-input");

    cell.querySelector(".dl-sql-run").addEventListener("click", () => runCell(cell, cells, pyCells, appCells));
    cell.querySelector(".dl-sql-reset").addEventListener("click", () => resetCell(cell, original));
    cell.querySelector(".dl-sql-download").addEventListener("click", () => downloadCell(cell));
    cell.querySelector(".dl-sql-load").addEventListener("click", () => loadInput.click());
    loadInput.addEventListener("change", () => {
      const file = loadInput.files[0];
      if (file) loadCell(cell, file);
      loadInput.value = "";
    });
    setUpReport(cell, input, cell.querySelector(".dl-sql-output"));

    return restorePersisted(cell);
  }

  /* ---- staged hints: folds that wait for a check attempt ----
   * planning/CELL_HINTS.md — ported in shape from dewlab's own
   * tutorial-runtime.js (its "staged hints" section), for `sql-check`
   * blocks only for now: the counter is nearly free there, since a check
   * already reports pass or fail on every click, and nothing on the SQL
   * or Python cell tracks needs it yet.
   */

  const STAGED_HINTS_KEY = "dewstack:staged-hints";

  function freshCheckAttempts() {
    return { runs: 0, checkFails: 0, firstRunAt: null };
  }

  /* The folds build.py wrote for this check — every `details.dl-hint-staged`
   * whose data-for is this check's own task, in source order, each with
   * its `data-after` parsed once into {signal: count}. build.py has
   * already validated the grammar, so an unreadable term here is a bug,
   * not an author's slip, and is skipped rather than breaking the page. */
  function collectStagedHints(task) {
    const marker = document.querySelector(
      `.dl-sql-check[data-task="${CSS.escape(task)}"] .dl-hint-marker`,
    );
    const folds = document.querySelectorAll(
      `details.dl-hint-staged[data-for="${CSS.escape(task)}"]`,
    );
    return Array.from(folds).map((el) => {
      const terms = {};
      for (const term of (el.dataset.after || "").split(/\s+/)) {
        const [key, count] = term.split(":");
        if (key && /^\d+$/.test(count || "")) terms[key] = Number(count);
      }
      /* Opening the fold is what the marker was asking for, so it goes. */
      el.addEventListener("toggle", () => { if (el.open && marker) marker.hidden = true; });
      return { el, terms, revealed: false };
    });
  }

  /* Whether every term of a hint's `data-after` holds against the counters.
   * `check-fails:2` means two clicks in a row came back wrong; `runs:3` is
   * three clicks total, right or wrong; `minutes` is measured from the
   * first click. */
  function triggerHolds(terms, attempts) {
    const value = {
      "check-fails": attempts.checkFails,
      "runs": attempts.runs,
      "minutes": attempts.firstRunAt == null ? 0 : (Date.now() - attempts.firstRunAt) / 60000,
    };
    return Object.entries(terms).every(([key, count]) => (value[key] ?? 0) >= count);
  }

  /* Updates a check's counters from one click's result. */
  function noteCheckAttempt(attempts, passed) {
    attempts.runs += 1;
    if (attempts.firstRunAt == null) attempts.firstRunAt = Date.now();
    attempts.checkFails = passed ? 0 : attempts.checkFails + 1;
  }

  /* Removes `hidden` from a revealed fold, closed, in normal flow — the
   * check grows by one summary line below it, nothing is covered and
   * nothing is opened for the reader. */
  function showStagedHint(check, hint) {
    hint.el.hidden = false;
    hint.el.classList.add("dl-hint-arrived");
    const marker = check.querySelector(".dl-hint-marker");
    if (marker && !hint.el.open) marker.hidden = false;
  }

  /* At most one hint arrives per click, in the order the author wrote them. */
  function maybeRevealHint(check, hints, attempts) {
    for (const hint of hints) {
      if (hint.revealed) continue;
      if (!triggerHolds(hint.terms, attempts)) continue;
      hint.revealed = true;
      if (readStagedHints()) showStagedHint(check, hint);
      return;
    }
  }

  /* Every revealed hint shown or hidden to match the setting — called when
   * the setting changes. Nothing here is persisted (planning/CELL_HINTS.md
   * §3), so there is nothing to restore at load; a hint only ever arrives
   * from a click made this same page view. */
  function syncStagedHints(allHints) {
    const on = readStagedHints();
    for (const hint of allHints) {
      if (hint.revealed) hint.el.hidden = !on;
    }
  }

  function readStagedHints() {
    try {
      return localStorage.getItem(STAGED_HINTS_KEY) !== "off";
    } catch (err) {
      return true;
    }
  }

  function writeStagedHints(mode) {
    try {
      localStorage.setItem(STAGED_HINTS_KEY, mode);
    } catch (err) {
      /* This reader's own choice only; forgotten after it. */
    }
  }

  /* The Settings row for staged hints — shown only on a page that has at
   * least one sql-check block, whether or not this particular page has a
   * staged hint written for it yet: the setting is a standing preference,
   * not a per-page one. */
  function initStagedHintsToggle(hasChecks, allHints) {
    const section = document.getElementById("dl-settings-hints");
    const onOff = document.querySelector("[data-staged-hints]");
    if (!section || !onOff || !hasChecks) return;
    section.hidden = false;
    const sync = () => {
      const on = readStagedHints();
      for (const btn of onOff.querySelectorAll("button")) {
        btn.setAttribute("aria-pressed", String(btn.dataset.value === (on ? "on" : "off")));
      }
    };
    onOff.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      writeStagedHints(btn.dataset.value);
      syncStagedHints(allHints);
      sync();
    });
    sync();
  }

  /* One self-check button: calls the named check_* function in
   * sql_tools.py against the named connection and shows what it says.
   * Instant, and never sent anywhere — a check, not a grade. Returns the
   * staged hints collected for this check, so the caller can fold them
   * into the one page-wide list initStagedHintsToggle() needs. */
  function setUpCheck(check, cells, pyCells, appCells) {
    const button = check.querySelector(".dl-sql-check-run");
    const output = check.querySelector(".dl-sql-check-output");
    const dbName = check.dataset.db;
    const task = check.dataset.task;
    const attempts = freshCheckAttempts();
    const hints = collectStagedHints(task);

    button.addEventListener("click", async () => {
      button.disabled = true;
      try {
        await ensureBooted(cells, pyCells, appCells);
        const fn = tools[task];
        output.innerHTML = fn
          ? fn(dbName)
          : `<p class="dl-sql-error">No such check: ${task}</p>`;
        if (fn) {
          noteCheckAttempt(attempts, !!output.querySelector(".dl-check-pass"));
          maybeRevealHint(check, hints, attempts);
        }
      } catch (err) {
        output.innerHTML = `<p class="dl-sql-error">${String(err)}</p>`;
      } finally {
        button.disabled = false;
      }
    });

    return hints;
  }

  /* A Python cell's own Run: calls python_tools.py's run_python() with
   * this cell's namespace name and current text, and drops whatever
   * HTML comes back straight into the output area — python_tools.py has
   * already turned any DataFrame, figure, print, or error into HTML. */
  async function runPyCell(cell, cells, pyCells, appCells) {
    const input = cell.querySelector(".dl-py-input");
    const output = cell.querySelector(".dl-py-output");
    const runButton = cell.querySelector(".dl-py-run");
    const name = cell.dataset.name;

    runButton.disabled = true;
    try {
      await ensureBooted(cells, pyCells, appCells);
      output.innerHTML = await pyTools.run_python(name, input.value);
    } catch (err) {
      output.innerHTML = `<p class="dl-sql-error">${String(err)}</p>`;
    } finally {
      runButton.disabled = false;
    }
  }

  function resetPyCell(cell, original) {
    const input = cell.querySelector(".dl-py-input");
    const output = cell.querySelector(".dl-py-output");
    input.value = original;
    output.innerHTML = "";
    if (pyTools) pyTools.reset(cell.dataset.name);
  }

  function setUpPy(cell, cells, pyCells, appCells) {
    const input = cell.querySelector(".dl-py-input");
    const original = input.value;
    cell.querySelector(".dl-py-run").addEventListener("click", () => runPyCell(cell, cells, pyCells, appCells));
    cell.querySelector(".dl-py-reset").addEventListener("click", () => resetPyCell(cell, original));
    setUpReport(cell, input, cell.querySelector(".dl-py-output"));
  }

  function appPane(cell, lang) {
    return cell.querySelector(`.dl-app-input[data-lang="${lang}"]`);
  }

  /* HTML and CSS redraw the moment a cell runs, the same as a site
   * editor's live panes — but here there is no separate document to
   * write them into. The HTML pane's text becomes the preview's own
   * innerHTML directly; the CSS pane's text is wrapped in `@scope` so
   * a reader's selectors reach only this cell's own preview, the same
   * separation an iframe would have given for free, kept without one. */
  function renderAppPreview(cell, preview) {
    const htmlPane = appPane(cell, "html");
    const cssPane = appPane(cell, "css");
    preview.innerHTML = htmlPane ? htmlPane.value : "";

    let style = cell.querySelector(".dl-app-style");
    const css = cssPane ? cssPane.value : "";
    if (!css) {
      if (style) style.remove();
      return;
    }
    if (!style) {
      style = document.createElement("style");
      style.className = "dl-app-style";
      cell.appendChild(style);
    }
    style.textContent = `@scope (#${preview.id}) {\n${css}\n}`;
  }

  /* The JS pane's own Run: rebuilds the preview from the current HTML
   * and CSS, then runs the current JavaScript as a real <script> element
   * (an assignment to innerHTML never executes one — this is why a new
   * element is created and appended each time rather than reused).
   * Wrapped in an async IIFE so `root` and `dlQuery` reach the reader's
   * code as plain parameters, nothing added to the page's own global
   * scope, and so a thrown error or a rejected await both land in the
   * same .catch(). */
  async function runAppCell(cell, cells, pyCells, appCells) {
    const jsPane = appPane(cell, "js");
    const errorBox = cell.querySelector(".dl-app-error");
    const preview = cell.querySelector(".dl-app-preview");
    const runButton = cell.querySelector(".dl-app-run");

    runButton.disabled = true;
    errorBox.textContent = "";
    try {
      await ensureBooted(cells, pyCells, appCells);
      renderAppPreview(cell, preview);

      const old = cell.querySelector(".dl-app-script");
      if (old) old.remove();
      const script = document.createElement("script");
      script.className = "dl-app-script";
      script.textContent =
        `(async function (root, dlQuery) {\n${jsPane.value}\n})` +
        `(document.getElementById(${JSON.stringify(preview.id)}), window.dlQuery)` +
        `.catch((err) => { document.getElementById(${JSON.stringify(errorBox.id)}).textContent = String(err); });`;
      cell.appendChild(script);
    } catch (err) {
      errorBox.textContent = String(err);
    } finally {
      runButton.disabled = false;
    }
  }

  /* Unlike a SQL or Python cell's own Reset, this never calls
   * tools.reset(): an app cell doesn't own a connection the way those
   * do, only ever reading one through whatever name its own dlQuery()
   * calls happen to pass — often a SQL cell's, elsewhere on the same
   * page, that other cells still depend on. Resetting the panes and the
   * preview is what "start this cell over" can safely mean here. */
  function resetAppCell(cell, originals) {
    ["html", "css", "js"].forEach((lang) => {
      const pane = appPane(cell, lang);
      if (pane) pane.value = originals[lang];
    });
    cell.querySelector(".dl-app-preview").innerHTML = "";
    cell.querySelector(".dl-app-error").textContent = "";
    const style = cell.querySelector(".dl-app-style");
    if (style) style.remove();
    const script = cell.querySelector(".dl-app-script");
    if (script) script.remove();
  }

  function setUpApp(cell, cells, pyCells, appCells) {
    const originals = {};
    ["html", "css", "js"].forEach((lang) => {
      const pane = appPane(cell, lang);
      if (pane) originals[lang] = pane.value;
    });
    cell.querySelector(".dl-app-run").addEventListener("click", () => runAppCell(cell, cells, pyCells, appCells));
    cell.querySelector(".dl-app-reset").addEventListener("click", () => resetAppCell(cell, originals));

    /* Not setUpReport(): that helper reads one `.dl-*-input`, and this
     * cell has three panes to read instead — the same open/close-a-panel
     * shape, just its own fill-in of what "this cell's code" means. */
    const icon = cell.querySelector(".dl-report-icon");
    const box = cell.querySelector(".dl-report-doors");
    if (!icon || !box) return;
    icon.addEventListener("click", () => {
      const open = icon.getAttribute("aria-expanded") === "true";
      icon.setAttribute("aria-expanded", String(!open));
      box.hidden = open;
      if (open) return;
      const code = ["html", "css", "js"]
        .filter((lang) => appPane(cell, lang))
        .map((lang) => `=== ${lang.toUpperCase()} ===\n${appPane(cell, lang).value}`)
        .join("\n\n");
      updateCellReportLinks(box, code, cell.querySelector(".dl-app-error").innerText);
    });
  }

  const cells = Array.from(document.querySelectorAll(".dl-sql-cell"));
  const checks = Array.from(document.querySelectorAll(".dl-sql-check"));
  const pyCells = Array.from(document.querySelectorAll(".dl-py-cell"));
  const appCells = Array.from(document.querySelectorAll(".dl-app-cell"));
  if (cells.length || checks.length || pyCells.length || appCells.length) {
    const restored = cells.filter((cell) => setUp(cell, cells, pyCells, appCells));
    const allStagedHints = [];
    checks.forEach((check) => allStagedHints.push(...setUpCheck(check, cells, pyCells, appCells)));
    initStagedHintsToggle(checks.length > 0, allStagedHints);
    pyCells.forEach((cell) => setUpPy(cell, cells, pyCells, appCells));
    appCells.forEach((cell) => setUpApp(cell, cells, pyCells, appCells));
    const booted = ensureBooted(cells, pyCells, appCells);
    if (restored.length) {
      booted.then(() => restored.forEach((cell) => runCell(cell, cells, pyCells, appCells))).catch(() => {});
    }
  }
})();
