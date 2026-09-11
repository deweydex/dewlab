
(function () {
  "use strict";

  const PYODIDE_VERSION = "0.28.3";

  const OWN_SCRIPT_URL = document.currentScript ? document.currentScript.src : null;

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

    const packages = window.DEWSTACK_SQL_PACKAGES || ["sqlite3"];
    setStatus(statuses, `Loading ${packages.join(", ")}…`);
    await pyodide.loadPackage(packages);

    setStatus(statuses, "Preparing the cell…");
    tools = await loadModule(pyodide, "sql_tools.py");
    if (pyCells.length) pyTools = await loadModule(pyodide, "python_tools.py");

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

  function loadCell(cell, file) {
    const input = cell.querySelector(".dl-sql-input");
    file.text().then((text) => {
      input.value = text;
      savePersisted(cell);
    });
  }

  const REPORT_CODE_LIMIT = 2500;
  const REPORT_OUTPUT_LIMIT = 1500;

  function truncateForReport(text, limit) {
    if (text.length <= limit) return text;
    return `${text.slice(0, limit)}\n… (cut off here — paste the rest yourself if it matters)`;
  }

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

  const STAGED_HINTS_KEY = "dewstack:staged-hints";

  function freshCheckAttempts() {
    return { runs: 0, checkFails: 0, firstRunAt: null };
  }

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
