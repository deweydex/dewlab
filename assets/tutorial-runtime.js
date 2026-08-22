/* dewlab tutorial runtime.
 *
 * Owns three things on a generated tutorial page:
 *   1. the settings panel — the reader's work, the download, and the reading
 *      texture (theme/font/size/width/link colour -> CSS variables),
 *   2. the CodeMirror editors for `exec` cells, and read-only CodeMirror over
 *      the illustrative blocks build.py marked as `pre.dl-static`,
 *   3. booting Pyodide and running a cell's code.
 *
 * Deliberately thin on rendering: everything a cell produces is turned into
 * markup by tutorial_tools.py, inside Python, so the output rules live in one
 * place and stay unit-testable without a browser. This file starts the work
 * and gets out of the way.
 *
 * Phase 0 scope. Save/load and version-compare (Phase 2) and the series
 * navigation (Phase 3) are not here yet.
 */

import { createCodeEditor, createReadOnlyCode, setEditorTheme } from "./vendor/codemirror.bundle.js";

/* ------------------------------------------------------------------ config */

/* Pyodide is loaded from the public CDN by default. `DEWLAB_PYODIDE_BASE` lets
 * a page point at a self-hosted copy instead — used by the e2e tests, and the
 * escape hatch if a school network ever blocks the CDN (OPEN_QUESTIONS.md 32).
 * Switching the whole site over is a one-line change here, not a redesign. */
const PYODIDE_VERSION = "0.28.3";
/* Resolved against the page, so a relative base ("../assets/pyodide/") works
 * as a module specifier. A bare relative path is not one, and `import()` would
 * reject it. */
const PYODIDE_BASE = new URL(
  globalThis.DEWLAB_PYODIDE_BASE ||
    `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`,
  document.baseURI
).href;

/* The baseline three, per DECISIONS.md. All are official Pyodide packages, so
 * this is one loadPackage call with no micropip step. A tutorial can widen the
 * list via `packages:` in its frontmatter (that is how scipy would arrive). */
const DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib"];

const TEXTURE_KEY = "dewlab:texture";
const PROGRESS_PREFIX = "dewlab:progress:";
const AUTOSAVE_DELAY = 500;
const TEXTURE_DEFAULTS = {
  theme: "system", font: "serif", size: 18, width: 34,
  link: "#d4692a", header: "full",
};

/* -------------------------------------------------------------- manifest */

function readManifest() {
  const el = document.getElementById("dewlab-manifest");
  if (!el) return { cells: [], assetBase: "", dataBase: "", packages: DEFAULT_PACKAGES };
  let m;
  try {
    m = JSON.parse(el.textContent);
  } catch (err) {
    console.error("dewlab: manifest is not valid JSON", err);
    return { cells: [], assetBase: "", dataBase: "", packages: DEFAULT_PACKAGES };
  }
  m.cells = m.cells || [];
  m.packages = m.packages && m.packages.length ? m.packages : DEFAULT_PACKAGES;
  m.assetBase = m.assetBase || "";
  m.dataBase = m.dataBase || "";
  m.assetVersions = m.assetVersions || {};
  return m;
}

/* An asset the runtime fetches for itself, with the version build.py hashed for
 * it. The page's own <link> and <script> tags are versioned in the markup; these
 * two are not in the markup, so they would otherwise be the only files a
 * returning visitor could be served a stale copy of. */
function assetUrl(manifest, name) {
  const version = manifest.assetVersions[name];
  return manifest.assetBase + name + (version ? `?v=${version}` : "");
}

/* ---------------------------------------------------------------- chrome */

/* The sticky masthead and navigation are one group, and everything below has
 * to clear it: the status line, the settings panel, and an anchored jump, which
 * would otherwise land its heading underneath. Its height is not a constant —
 * it depends on how far the neighbouring tutorials' titles wrap, which depends
 * on the window and on the reader's text size — so it is measured rather than
 * guessed, and measured again whenever it changes. */
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
    /* No observer: the window changing size is the case that matters most. */
    window.addEventListener("resize", publish);
  }
}

/* -------------------------------------------------------- settings panel */

/* One panel holds everything a reader can change or take away, so this is the
 * only open/close behaviour on the page. Escape and a click outside both close
 * it: a panel that can only be dismissed by finding the same small button
 * again is the kind of thing that gets left open. */
function initSettingsPanel() {
  const toggle = document.getElementById("dl-settings-toggle");
  const panel = document.getElementById("dl-settings");
  if (!toggle || !panel) return;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  const close = document.getElementById("dl-settings-close");
  if (close) close.addEventListener("click", () => { setOpen(false); toggle.focus(); });

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || panel.hasAttribute("hidden")) return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (ev) => {
    if (panel.hasAttribute("hidden")) return;
    if (panel.contains(ev.target) || toggle.contains(ev.target)) return;
    setOpen(false);
  });

  /* A section with nothing in it is a heading over a gap. build.py leaves the
   * download section empty on the contents page, which has nothing to
   * download, and on a downloadable copy, which is already the file. */
  for (const section of panel.querySelectorAll(".dl-settings-section")) {
    if (!section.textContent.trim()) section.hidden = true;
  }
}

/* --------------------------------------------------------- texture panel */

function isDarkNow() {
  const explicit = document.documentElement.getAttribute("data-theme");
  if (explicit === "dark") return true;
  if (explicit === "light") return false;
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function loadTexture() {
  try {
    return { ...TEXTURE_DEFAULTS, ...JSON.parse(localStorage.getItem(TEXTURE_KEY) || "{}") };
  } catch (err) {
    return { ...TEXTURE_DEFAULTS };
  }
}

function saveTexture(state) {
  try {
    localStorage.setItem(TEXTURE_KEY, JSON.stringify(state));
  } catch (err) {
    /* Private mode or blocked storage. Preferences apply for this page view
     * only; nothing else about the page depends on them persisting. */
  }
}

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
      /* Width is a number with three named presets and a slider behind them.
       * Setting it to something between the presets is allowed and leaves none
       * of the three pressed, which is the honest way to show it. */
      const current = group.hasAttribute("data-number") ? String(state[key]) : state[key];
      for (const btn of group.querySelectorAll("button")) {
        btn.setAttribute("aria-pressed", String(btn.dataset.value === current));
      }
    }
    sizeEl.value = state.size;
    widthEl.value = state.width;
    linkEl.value = state.link;
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
      state[group.dataset.texture] = group.hasAttribute("data-number")
        ? Number(btn.dataset.value)
        : btn.dataset.value;
      commit();
    });
  }
  sizeEl.addEventListener("input", () => { state.size = Number(sizeEl.value); commit(); });
  widthEl.addEventListener("input", () => { state.width = Number(widthEl.value); commit(); });
  linkEl.addEventListener("input", () => { state.link = linkEl.value; commit(); });

  document.getElementById("dl-texture-reset").addEventListener("click", () => {
    Object.assign(state, TEXTURE_DEFAULTS);
    commit();
  });

  /* Following the system theme means reacting when the system changes. */
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      if (state.theme === "system") onThemeChange(isDarkNow());
    });
  }

  sync();
  return state;
}

/* ---------------------------------------------------------------- status */

const statusEl = document.getElementById("dl-status");

function setStatus(text, kind) {
  if (!statusEl) return;
  if (!text) {
    statusEl.hidden = true;
    statusEl.textContent = "";
    return;
  }
  statusEl.hidden = false;
  statusEl.textContent = text;
  statusEl.classList.toggle("dl-status-error", kind === "error");
}

/* ----------------------------------------------------------------- cells */

/* One entry per `exec` cell on the page, in document order. */
const cells = [];

function buildCells(manifest) {
  const dark = isDarkNow();

  for (const spec of manifest.cells) {
    const host = document.querySelector(`.dl-cell[data-cell-id="${CSS.escape(spec.id)}"]`);
    if (!host) {
      console.warn(`dewlab: manifest lists cell "${spec.id}" but the page has no such element`);
      continue;
    }

    const editorHost = host.querySelector(".dl-editor");
    const outputEl = host.querySelector(".dl-output");
    const runBtn = host.querySelector(".dl-btn-run");
    const resetBtn = host.querySelector(".dl-btn-reset");

    const editor = createCodeEditor(editorHost, spec.code || "", {
      dark,
      onChange: () => scheduleSave(),
    });

    const cell = {
      id: spec.id,
      starter: spec.code || "",
      editor,
      outputEl,
      runBtn,
      element: host,
      getCode: () => editor.getValue(),
    };
    cells.push(cell);

    runBtn.addEventListener("click", () => runCell(cell));
    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        editor.setValue(cell.starter);
        outputEl.replaceChildren();
      });
    }

    /* Ctrl/Cmd+Enter runs the cell, the shortcut every notebook user reaches
     * for first. Registered on the host rather than inside CodeMirror's keymap
     * so it also fires from the Run button's own focus. */
    host.addEventListener("keydown", (ev) => {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
        ev.preventDefault();
        runCell(cell);
      }
    });
  }
}

function setRunnable(enabled, label) {
  for (const cell of cells) {
    cell.runBtn.disabled = !enabled;
    cell.runBtn.textContent = label || (enabled ? "Run" : "…");
  }
}

/* --------------------------------------------------------------- Pyodide */

let pyodide = null;
let tools = null;
let bootPromise = null;

async function boot(manifest) {
  setStatus("Starting Python…");

  /* Two ways in, because a page opened from a file cannot import a module.
   * A standalone export loads Pyodide's classic script first, which leaves
   * loadPyodide on the global; a hosted page has no such script and imports
   * the module instead. */
  if (manifest.standalone && !globalThis.loadPyodide) {
    /* The classic script this file depends on did not load. Falling through to
     * the module import cannot work from a file either, and would report the
     * wrong thing — so say what actually happened. */
    const offline = new Error(
      "Python could not be downloaded. This file needs an internet connection " +
        "the first time you open it — the reading works without one."
    );
    offline.dewlabFinal = true; // already says everything useful; do not dress it up
    throw offline;
  }
  const loadPyodide =
    globalThis.loadPyodide ||
    (await import(/* @vite-ignore */ PYODIDE_BASE + "pyodide.mjs")).loadPyodide;
  pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });

  setStatus(`Loading ${manifest.packages.join(", ")}…`);
  /* One call, no micropip: every package here ships with Pyodide. */
  await pyodide.loadPackage(manifest.packages);

  setStatus("Preparing the notebook tools…");
  /* A standalone export carries this source inside the page, because fetch
   * cannot read a neighbouring file from disk either. */
  const source =
    manifest.toolsSource ||
    (await fetch(assetUrl(manifest, "tutorial_tools.py")).then((r) => {
      if (!r.ok) throw new Error(`tutorial_tools.py: HTTP ${r.status}`);
      return r.text();
    }));
  pyodide.FS.writeFile("/home/pyodide/tutorial_tools.py", source, { encoding: "utf8" });
  tools = pyodide.pyimport("tutorial_tools");

  /* Where a tutorial's `/data/` CSVs live, relative to this page. Setup cells
   * fetch through this rather than hard-coding a path per tutorial. */
  tools.configure(manifest.dataBase);

  /* tutorial_tools owns the page namespace and the whole cell lifecycle, so
   * output ordering and traceback formatting have one implementation rather
   * than being split across two languages. All this side does is start it.
   *
   * Every cell on a page shares that namespace, in document order — the
   * notebook model. Pages do not share state with each other: each is its own
   * Pyodide instance, so a setup cell re-runs on every page load
   * (CONTENT_AND_FILE_ARCHITECTURE.md, "Shared setup code"). */
  await pyodide.runPythonAsync(`
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`);

  setStatus("");
  setRunnable(true, "Run");
}

function ensureBooted(manifest) {
  if (!bootPromise) {
    bootPromise = boot(manifest).catch((err) => {
      console.error("dewlab: Pyodide failed to start", err);
      setStatus(
        err.dewlabFinal
          ? err.message
          : `Python failed to start: ${err.message}. Reloading the page usually fixes it.`,
        "error"
      );
      setRunnable(false, "unavailable");
      throw err;
    });
  }
  return bootPromise;
}

/* ------------------------------------------------------------ running a cell */

let running = false;

async function runCell(cell) {
  if (running) return;
  running = true;
  const previousLabel = cell.runBtn.textContent;
  cell.runBtn.disabled = true;
  cell.runBtn.textContent = "Running…";

  try {
    await ensureBooted(currentManifest);

    /* Python owns the output area for the duration of the cell: stdout,
     * widgets, tables, figures and tracebacks all land through tutorial_tools,
     * so they appear in the order the code produced them. A student's error is
     * normal traffic and is rendered in the cell, not thrown up here. */
    await tools.run_cell(cell.id, cell.outputEl, cell.getCode());
    /* Saved after the run rather than during it, so what is stored is the
     * output the student actually ended up looking at. */
    saveNow();
  } catch (err) {
    /* Boot failure. Already surfaced in the status bar; nothing useful to add
     * inside the cell. */
  } finally {
    running = false;
    cell.runBtn.disabled = false;
    cell.runBtn.textContent = previousLabel === "Running…" ? "Run" : previousLabel;
  }
}

/* ------------------------------------------------- illustrative code, maths */

const readOnlyBlocks = [];

/* An untagged fence. build.py leaves the escaped source inside <pre><code>, so
 * this is an upgrade of something already readable rather than the only way the
 * code ever appears — with JavaScript off, the page still shows it. */
function highlightIllustrativeCode() {
  const dark = isDarkNow();
  for (const pre of document.querySelectorAll("pre.dl-static")) {
    const code = pre.querySelector("code");
    if (!code) continue;
    const source = code.textContent.replace(/\n$/, "");
    const language = pre.dataset.lang || "";
    pre.textContent = "";
    readOnlyBlocks.push(createReadOnlyCode(pre, source, { dark, language }));
  }
}

/* KaTeX is fetched only when the manifest says the page has maths — 266 KB that
 * a prose-and-code tutorial never pays for (DECISIONS_LOG 1.8). Each span holds
 * its own source TeX, which is both the fallback and the input. */
async function renderMaths(manifest) {
  const spans = document.querySelectorAll(".dl-math");
  if (!manifest.math || spans.length === 0) return;
  let renderMath;
  try {
    /* Deliberately a plain string: the standalone export bundles this import
     * into one file, and it can only do that if the specifier is static. That
     * costs the maths bundle its cache-busting, which is the right trade — it
     * is vendored and pinned, so it changes only when we re-vendor on purpose,
     * whereas the stylesheet and the runtime change most weeks. */
    ({ renderMath } = await import("./vendor/katex.bundle.js"));
  } catch (err) {
    console.error("dewlab: KaTeX failed to load; maths stays as source TeX", err);
    return;
  }
  for (const span of spans) {
    renderMath(span, span.textContent, span.classList.contains("dl-math-display"));
  }
}


/* ------------------------------------------------------------- saved work */

/* Everything a student types is kept in their own browser, on their own
 * device, and goes nowhere else. VERSIONING_AND_PROGRESS.md sets the rules:
 * autosave is the real safety net, restore matches on cell id rather than
 * position, and a tutorial edited since they last saved restores anyway — with
 * a notice, never a block. Losing an afternoon's practice is an annoyance, not
 * a lost grade, and the design is sized to that.
 */

let saveTimer = null;

function progressKey() {
  return PROGRESS_PREFIX + (currentManifest.slug || "unknown");
}

function readSaved() {
  try {
    const raw = localStorage.getItem(progressKey());
    return raw ? JSON.parse(raw) : null;
  } catch (err) {
    /* Private browsing, blocked storage, or something that is not ours. */
    return null;
  }
}

function saveNow() {
  clearTimeout(saveTimer);
  saveTimer = null;
  if (cells.length === 0) return;
  const record = {
    "tutorial-slug": currentManifest.slug,
    "tutorial-version": currentManifest.version,
    saved_at: new Date().toISOString(),
    cells: cells.map((cell) => ({
      task_id: cell.id,
      student_code: cell.getCode(),
      output_html: cell.outputEl.innerHTML,
    })),
  };
  try {
    localStorage.setItem(progressKey(), JSON.stringify(record));
    showSaveState(record.saved_at);
  } catch (err) {
    /* Storage full or refused. Say so rather than pretending it saved. */
    showSaveState(null, "Your browser would not let this page save your work.");
  }
}

function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, AUTOSAVE_DELAY);
}

/* Put the work back, and report honestly on what could not be put back. */
function restoreSaved() {
  const record = readSaved();
  if (!record || !Array.isArray(record.cells)) return null;

  const byId = new Map(cells.map((cell) => [cell.id, cell]));
  const restored = [];
  const dropped = [];
  let widgets = false;

  for (const saved of record.cells) {
    const cell = byId.get(saved.task_id);
    if (!cell) {
      /* The tutorial no longer has this cell. Say so rather than discarding it
       * silently — a student who wrote something there deserves to know. */
      dropped.push(saved.task_id);
      continue;
    }
    if (typeof saved.student_code === "string") cell.editor.setValue(saved.student_code);
    if (typeof saved.output_html === "string" && saved.output_html) {
      cell.outputEl.innerHTML = saved.output_html;
      if (saved.output_html.includes("dl-widget")) widgets = true;
    }
    restored.push(cell.id);
  }

  return {
    restored,
    dropped,
    widgets,
    savedAt: record.saved_at,
    versionChanged: String(record["tutorial-version"]) !== String(currentManifest.version),
  };
}

function announceRestore(summary) {
  if (!summary || (summary.restored.length === 0 && summary.dropped.length === 0)) return;

  const box = document.createElement("div");
  box.className = "dl-restored";
  box.setAttribute("role", "status");

  const lines = [];
  if (summary.versionChanged) {
    lines.push(
      "This tutorial has been updated since you last worked on it. Your work is " +
        "back below, but some of it may not line up with the new version."
    );
  } else {
    lines.push("Your work from last time is back below.");
  }
  if (summary.dropped.length) {
    lines.push(
      `${summary.dropped.length} saved ${summary.dropped.length === 1 ? "cell is" : "cells are"} ` +
        "not in this tutorial any more, so there was nowhere to put it back."
    );
  }
  if (summary.widgets) {
    lines.push(
      "Cells with a box or a button in them need running again before they work."
    );
  }

  for (const text of lines) {
    const p = document.createElement("p");
    p.textContent = text;
    box.appendChild(p);
  }

  const dismiss = document.createElement("button");
  dismiss.type = "button";
  dismiss.className = "dl-restored-dismiss";
  dismiss.textContent = "Hide this";
  dismiss.addEventListener("click", () => box.remove());
  box.appendChild(dismiss);

  const body = document.getElementById("dl-body");
  body.insertBefore(box, body.firstChild);
}

function showSaveState(savedAt, problem) {
  const el = document.getElementById("dl-progress-state");
  if (!el) return;
  if (problem) {
    el.textContent = problem;
    return;
  }
  el.textContent = savedAt
    ? `Saved at ${new Date(savedAt).toLocaleTimeString()}. Saving as you go.`
    : "Saving as you go.";
}

function initProgressSection() {
  const section = document.getElementById("dl-settings-work");
  if (!section) return;

  /* A page with no cells has nothing to save — the contents page, or a
   * tutorial that is all prose and mathematics. Offering to export a student's
   * work from a page where they cannot do any is a button that can only
   * disappoint, so the whole section goes rather than sitting there empty. */
  if (cells.length === 0) {
    section.remove();
    return;
  }

  document.getElementById("dl-progress-export").addEventListener("click", () => {
    saveNow();
    const record = readSaved() || {};
    const blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${currentManifest.slug || "dewlab"}-progress.json`;
    link.click();
    URL.revokeObjectURL(link.href);
  });

  const file = document.getElementById("dl-progress-file");
  document.getElementById("dl-progress-import").addEventListener("click", () => file.click());
  file.addEventListener("change", async () => {
    const chosen = file.files && file.files[0];
    if (!chosen) return;
    try {
      const record = JSON.parse(await chosen.text());
      localStorage.setItem(progressKey(), JSON.stringify(record));
      announceRestore(restoreSaved());
      showSaveState(record.saved_at);
    } catch (err) {
      showSaveState(null, "That file could not be read as saved dewlab work.");
    }
    file.value = "";
  });

  document.getElementById("dl-progress-clear").addEventListener("click", () => {
    if (!window.confirm("Clear your work on this tutorial and start again?")) return;
    try {
      localStorage.removeItem(progressKey());
    } catch (err) {
      /* Nothing to remove, or storage refused. Reset the page either way. */
    }
    for (const cell of cells) {
      cell.editor.setValue(cell.starter);
      cell.outputEl.replaceChildren();
    }
    for (const box of document.querySelectorAll(".dl-restored")) box.remove();
    showSaveState(null);
  });
}

/* ------------------------------------------------------------------ start */

const currentManifest = readManifest();

initTexture((dark) => {
  for (const cell of cells) setEditorTheme(cell.editor, dark);
  for (const block of readOnlyBlocks) setEditorTheme(block, dark);
});

buildCells(currentManifest);
initProgressSection();
initSettingsPanel();
trackChromeHeight();
announceRestore(restoreSaved());
highlightIllustrativeCode();
const mathsRendered = renderMaths(currentManifest);

if (cells.length === 0) {
  /* A prose-only tutorial is a normal tutorial, not a special case
   * (CONTENT_AND_FILE_ARCHITECTURE.md). No cells means no reason to pay for
   * Pyodide at all. */
  setStatus("");
} else {
  setRunnable(false, "…");
  ensureBooted(currentManifest).catch(() => {});
}

/* Exposed for the e2e tests to await, and for debugging from the console. */
globalThis.dewlab = {
  version: PYODIDE_VERSION,
  cells,
  saveNow,
  readSaved,
  progressKey,
  ready: () =>
    Promise.all([
      mathsRendered,
      cells.length === 0 ? Promise.resolve() : ensureBooted(currentManifest),
    ]),
  runCell: (id) => {
    const cell = cells.find((c) => c.id === id);
    if (!cell) throw new Error(`no cell "${id}"`);
    return runCell(cell);
  },
};
