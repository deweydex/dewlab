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

/* Settings and the cheat sheet (initCheatSheet(), below) are two open/close
 * behaviours on the page rather than one now, and both panels anchor to the
 * same corner (tutorial-style.css) — opening either one closes the other,
 * or they would sit on top of each other. Escape and a click outside both
 * close whichever is open: a panel that can only be dismissed by finding the
 * same small button again is the kind of thing that gets left open. */
function closeCheatSheet() {
  const toggle = document.getElementById("dl-cheatsheet-toggle");
  const panel = document.getElementById("dl-cheatsheet");
  if (!panel || panel.hasAttribute("hidden")) return;
  panel.setAttribute("hidden", "");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}

function closeSettings() {
  const toggle = document.getElementById("dl-settings-toggle");
  const panel = document.getElementById("dl-settings");
  if (!panel || panel.hasAttribute("hidden")) return;
  panel.setAttribute("hidden", "");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}

function initSettingsPanel() {
  const toggle = document.getElementById("dl-settings-toggle");
  const panel = document.getElementById("dl-settings");
  if (!toggle || !panel) return;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    if (open) closeCheatSheet();
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

/* -------------------------------------------------------- cheat sheet */

/* build.py's own kind list — GLOSSARY_KINDS — in the order a reader would
 * find most useful to scan: what a thing *is* before what you *do* with it. */
const GLOSSARY_GROUP_LABELS = {
  concept: "Concepts",
  function: "Functions",
  operator: "Operators",
  formula: "Formulas",
  keyword: "Keywords",
};

function renderCheatSheet(entries) {
  const container = document.getElementById("dl-cheatsheet-groups");
  if (!container) return;
  container.replaceChildren();

  const byKind = new Map();
  for (const entry of entries) {
    if (!byKind.has(entry.kind)) byKind.set(entry.kind, []);
    byKind.get(entry.kind).push(entry);
  }

  for (const [kind, label] of Object.entries(GLOSSARY_GROUP_LABELS)) {
    const group = byKind.get(kind);
    if (!group || !group.length) continue;

    const section = document.createElement("div");
    section.className = "dl-cheatsheet-group";
    const heading = document.createElement("h3");
    heading.textContent = label;
    section.append(heading);

    const dl = document.createElement("dl");
    for (const entry of group) {
      const dt = document.createElement("dt");
      dt.textContent = entry.term;
      const dd = document.createElement("dd");
      dd.append(document.createTextNode(entry.definition));
      if (entry.example) {
        const code = document.createElement("code");
        code.textContent = entry.example;
        dd.append(code);
      }
      dl.append(dt, dd);
    }
    section.append(dl);
    container.append(section);
  }
}

/* Same open/close mechanics as initSettingsPanel(), and the two stay in sync
 * (closeCheatSheet()/closeSettings(), above) because both panels anchor to
 * the same corner. The one real difference: this toggle starts `hidden` in
 * shell.html, and stays that way — offering nothing at all — unless this
 * page's own manifest actually carries a glossary. A tutorial with nothing
 * accumulated yet (planning/CHEAT_SHEETS.md §6) is not a rare case early on:
 * it is every tutorial before the skill has been run on anything ahead of
 * it in its series. */
function initCheatSheet(manifest) {
  const entries = manifest.glossary;
  const toggle = document.getElementById("dl-cheatsheet-toggle");
  const panel = document.getElementById("dl-cheatsheet");
  if (!toggle || !panel || !entries || !entries.length) return;

  renderCheatSheet(entries);
  toggle.hidden = false;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    if (open) closeSettings();
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  const close = document.getElementById("dl-cheatsheet-close");
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
      completeNames: pageNamesCompletion,
      getDoc: docFor,
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
let inspectModule = null;
let bootPromise = null;

/* --------------------------------------------------- code intelligence
 *
 * Both wired into every cell's editor at buildCells() time, before Pyodide
 * exists — each checks for a live interpreter itself, at call time, rather
 * than needing anything reconfigured once boot() finishes. A page left open
 * through a boot just starts offering real completions and real docs; there
 * is no "not ready yet" state for a caller to manage.
 */

/* Every name currently defined in the shared page namespace — the same
 * dict every cell actually runs against, tutorial_tools._page_globals
 * (run_cell's `globals=`) — so what is offered is exactly what a cell could
 * reference right now: a name from an earlier cell, or from this tutorial's
 * own setup cell, not a generic Python index. `__name__` and anything else
 * tutorial_tools itself seeds with a leading underscore are filtered out. */
function pageNamesCompletion(context) {
  if (!tools) return null;
  const word = context.matchBefore(/\w+/);
  if (!word || (word.from === word.to && !context.explicit)) return null;
  const names = [...tools._page_globals.keys()].filter((name) => !name.startsWith("_"));
  if (!names.length) return null;
  return { from: word.from, options: names.map((label) => ({ label, type: "variable" })) };
}

/* A real docstring for a name the student defined or imported, read from the
 * interpreter actually running their code — accurate by construction, and
 * there is nothing bundled to fall out of date with it. Only ever looks an
 * existing name up in the page's own namespace; never evaluates anything a
 * student typed, and Python builtins (print, len, …) are deliberately out of
 * scope here — they are not in _page_globals, and reaching into __builtins__
 * as well was a bigger surface than this needed for a first pass. */
function docFor(name) {
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
  inspectModule = pyodide.pyimport("inspect");

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
  /* Module and slug, because a slug is only unique within its module — both
   * modules have a `first-steps`. Keyed on the slug alone, the two shared one
   * record and each overwrote the other's answers.
   *
   * This is the third time scoping slugs per module has left something keyed
   * on the slug alone: the built pages, the downloadable copies, and now the
   * saved work. */
  const manifest = currentManifest || {};
  return `${PROGRESS_PREFIX}${manifest.module || "unknown"}:${manifest.slug || "unknown"}`;
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

function describeMismatch(record) {
  /* Whether a loaded file belongs to this tutorial, and if not, which one it
   * is. Slug always; module only when the record carries one, so a file saved
   * before the module was recorded still loads where it belongs.
   *
   * An empty string means it fits. */
  if (!record || typeof record !== "object" || !Array.isArray(record.cells)) {
    return "That file could not be read as saved dewlab work.";
  }
  const slug = record["tutorial-slug"];
  const module = record["tutorial-module"];
  const here = slug === currentManifest.slug
    && (!module || module === currentManifest.module);
  if (here) return "";
  const name = [module, slug].filter(Boolean).join(" / ") || "another tutorial";
  return `That file is saved work from ${name}, not this tutorial. `
    + "Nothing has been changed.";
}


function saveNow() {
  clearTimeout(saveTimer);
  saveTimer = null;
  if (cells.length === 0) return;
  const record = {
    "tutorial-slug": currentManifest.slug,
    /* The module too, because the slug alone does not say which tutorial this
     * came from — both modules have a `first-steps`. Written so an exported
     * file can be checked before it replaces anything. */
    "tutorial-module": currentManifest.module,
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
    rememberVersion();
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
    savedVersion: String(record["tutorial-version"]),
    versionChanged: String(record["tutorial-version"]) !== String(currentManifest.version),
  };
}

function announceRestore(summary) {
  if (!summary || (summary.restored.length === 0 && summary.dropped.length === 0)) return;

  const box = document.createElement("div");
  box.className = "dl-restored";
  box.setAttribute("role", "status");

  /* Where the tutorial has releases, both lines below can say what happened
   * rather than guess at it: which release the work came from, which one this
   * is, and that an answer with no cell to go in is still saved. Where it has
   * only one, the work was written against a file that has since been edited
   * in place, and "may not line up" is the honest thing to say (7.30). */
  const from = versionList().find((v) => v.version === summary.savedVersion);
  const here = thisVersion();

  const lines = [];
  if (summary.versionChanged && from && here) {
    lines.push(
      `Your work is back below. You wrote it in the ${from.date} version and ` +
        `you are reading the ${here.date} one.`
    );
  } else if (summary.versionChanged) {
    lines.push(
      "This tutorial has been updated since you last worked on it. Your work is " +
        "back below, but some of it may not line up with the new version."
    );
  } else {
    lines.push("Your work from last time is back below.");
  }
  if (summary.dropped.length) {
    const many = summary.dropped.length !== 1;
    lines.push(
      here
        ? (many
            ? `${summary.dropped.length} of your saved answers are in cells this `
              + "version does not have. They are still saved, and they come back "
              + "in a version that has those cells."
            : "One of your saved answers is in a cell this version does not "
              + "have. It is still saved, and it comes back in a version that "
              + "has the cell.")
        : `${summary.dropped.length} saved ${many ? "cells are" : "cell is"} `
          + "not in this tutorial any more, so there was nowhere to put it back."
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

  /* Below the page's own notice where there is one. Which release you are
   * reading is the thing to know first; what happened to your work only makes
   * sense once you know it. */
  const body = document.getElementById("dl-body");
  const notice = body.querySelector(".dl-archived");
  if (notice) notice.insertAdjacentElement("afterend", box);
  else body.insertBefore(box, body.firstChild);
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
    /* Module in the filename: two files called first-steps-progress.json in a
     * downloads folder are indistinguishable, and they are from different
     * tutorials. */
    const from = [currentManifest.module, currentManifest.slug].filter(Boolean).join("-");
    link.download = `${from || "dewlab"}-progress.json`;
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
      /* Check before writing. This used to overwrite whatever was already
       * saved and only then discover the cells did not match, which destroyed
       * the student's real work to make room for somebody else's. */
      const wrong = describeMismatch(record);
      if (wrong) {
        showSaveState(null, wrong);
        file.value = "";
        return;
      }
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

/* -------------------------------------------------------------- versions */
/*
 * A tutorial can have more than one release, and two different questions
 * decide which one a reader gets:
 *
 *   the build  — what the plain URL serves, for somebody arriving for the
 *                first time. The newest live release.
 *   this file  — what somebody who has already worked here gets. The release
 *                they last worked in, unless they have said otherwise.
 *
 * Saved work is keyed by tutorial rather than by release, and restore matches
 * on cell id, so answers move between releases on their own. That is what lets
 * this list say what will happen rather than warn that something might: the
 * manifest carries every release's cell ids, so the page can count the answers
 * that survive a move before the reader makes it.
 */

const VERSION_PIN_PREFIX = "dewlab:version:";
const FOLLOW_KEY = "dewlab:versions-follow";

function versionList() {
  /* Absent on a tutorial with one release, which is most of them. */
  const list = currentManifest && currentManifest.versions;
  return Array.isArray(list) ? list : [];
}

function versionPinKey() {
  const manifest = currentManifest || {};
  return `${VERSION_PIN_PREFIX}${manifest.module || "unknown"}:${manifest.slug || "unknown"}`;
}

/* Which release this reader is on: the one they picked, or failing that the
 * one their saved work was written against.
 *
 * The fallback is what makes this work for somebody who was here before a
 * second release existed — there was nothing to pick then, but the record
 * says where they were. */
function readPin() {
  try {
    const picked = localStorage.getItem(versionPinKey());
    if (picked) return picked;
  } catch (err) {
    /* Private browsing or blocked storage. Fall through to the record, which
     * has its own guard and will return null under the same conditions. */
  }
  const record = readSaved();
  const worked = record && record["tutorial-version"];
  return worked ? String(worked) : null;
}

function writePin(version) {
  try {
    localStorage.setItem(versionPinKey(), version);
  } catch (err) {
    /* The reader still gets where they clicked; they just will not land there
     * again by themselves. */
  }
}

function rememberVersion() {
  /* Working in a release is a reader saying that is the one they are on, and
   * it has to outrank an older pick or a stale pick would keep pulling them
   * back off the page they are working on.
   *
   * Nothing to remember where there is no choice. */
  if (versionList().length < 2) return;
  writePin(currentManifest.version);
}

function readFollow() {
  /* "started" is the default because it is the one that does not move the
   * ground under somebody halfway through. */
  try {
    return localStorage.getItem(FOLLOW_KEY) === "newest" ? "newest" : "started";
  } catch (err) {
    return "started";
  }
}

function writeFollow(mode) {
  try {
    localStorage.setItem(FOLLOW_KEY, mode);
  } catch (err) {
    /* As above: the choice holds for this page and is forgotten after it. */
  }
}

function thisVersion() {
  return versionList().find((v) => v.version === currentManifest.version) || null;
}

function defaultVersion() {
  return versionList().find((v) => v.isDefault) || null;
}

/* Where a reader who has been here before is sent.
 *
 * Only ever away from the page the plain URL serves, and only to a release
 * that still exists — the first so this cannot bounce between two pages, the
 * second so a reader following a link to one particular release lands on the
 * release they asked for rather than on their own.
 */
function continuityTarget() {
  if (readFollow() !== "started") return null;
  const here = thisVersion();
  if (!here || !here.isDefault) return null;
  const pin = readPin();
  if (!pin || pin === currentManifest.version) return null;
  return versionList().find((v) => v.version === pin) || null;
}

function followTheVersionYouLeftOff() {
  const target = continuityTarget();
  if (!target) return false;
  /* replace rather than assign: Back should go where the reader came from, not
   * to a page that immediately sends them here again. */
  location.replace(target.url);
  return true;
}

/* The answers a reader has written, as opposed to the cells they happened to
 * have open. A starter left untouched is not an answer, and counting it would
 * inflate every number below — the point of these counts is that they are
 * true. */
function answeredCells() {
  const record = readSaved();
  if (!record || !Array.isArray(record.cells)) return [];
  const starters = new Map(cells.map((cell) => [cell.id, cell.starter]));
  return record.cells.filter((saved) => {
    const code = typeof saved.student_code === "string" ? saved.student_code.trim() : "";
    if (!code) return false;
    const starter = starters.get(saved.task_id);
    return starter === undefined || code !== String(starter).trim();
  });
}

function carryOver(entry) {
  const answers = answeredCells();
  if (answers.length === 0) return null;
  const there = new Set(Array.isArray(entry.cells) ? entry.cells : []);
  return {
    carried: answers.filter((saved) => there.has(saved.task_id)).length,
    total: answers.length,
  };
}

function describeCarry(entry) {
  const count = carryOver(entry);
  if (!count) return "";
  if (count.carried === count.total) {
    return count.total === 1
      ? "Your answer carries over."
      : `All ${count.total} of your answers carry over.`;
  }
  const missing = count.total - count.carried;
  const rest = missing === 1
    ? "1 cell is not in that version, so that answer stays saved but is not shown there."
    : `${missing} cells are not in that version, so those answers stay saved `
      + "but are not shown there.";
  return `${count.carried} of your ${count.total} answers carry over. ${rest}`;
}

function versionOption(entry) {
  const item = document.createElement("li");
  item.className = "dl-version";
  item.dataset.version = entry.version;

  const here = entry.version === currentManifest.version;
  if (here) item.dataset.current = "";

  const name = document.createElement(here ? "span" : "a");
  name.className = "dl-version-name";
  name.textContent = entry.date;
  if (!here) {
    name.href = entry.url;
    name.addEventListener("click", () => writePin(entry.version));
  }
  item.appendChild(name);

  const tags = [];
  if (here) tags.push("you are reading this");
  if (entry.isDefault && !here) tags.push("current");
  if (entry.status === "beta") tags.push("draft");
  if (entry.status === "archived") tags.push("retired");
  for (const text of tags) {
    const tag = document.createElement("span");
    tag.className = "dl-version-tag";
    tag.textContent = text;
    item.appendChild(tag);
  }

  const carry = here ? "" : describeCarry(entry);
  if (carry) {
    const line = document.createElement("p");
    line.className = "dl-version-carry";
    line.textContent = carry;
    item.appendChild(line);
  }
  return item;
}

function fillVersionList(list) {
  list.replaceChildren();
  for (const entry of versionList()) list.appendChild(versionOption(entry));
}

/* The control beside the title: nothing at all on a tutorial with one release,
 * something always visible on a tutorial with several.
 *
 * Not a control that appears on hover. Hover does not exist on a phone, and a
 * good share of these readers are on one — an affordance that only appears on
 * hover is not subtle to them, it is missing.
 */
function initVersionMarker() {
  if (versionList().length < 2) return;
  const here = thisVersion();
  const wrap = document.createElement("div");
  wrap.className = "dl-versions";
  wrap.id = "dl-versions";

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "dl-versions-toggle";
  toggle.id = "dl-versions-toggle";
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-controls", "dl-versions-list");
  toggle.append(here ? here.date : currentManifest.version);
  const caret = document.createElement("span");
  caret.className = "dl-versions-caret";
  caret.setAttribute("aria-hidden", "true");
  toggle.appendChild(caret);
  wrap.appendChild(toggle);

  const list = document.createElement("ul");
  list.className = "dl-versions-list";
  list.id = "dl-versions-list";
  list.hidden = true;
  wrap.appendChild(list);

  function setOpen(open) {
    /* Built on opening rather than at load, because the counts read saved work
     * and the reader may have written some since the page loaded. */
    if (open) fillVersionList(list);
    list.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  }

  toggle.addEventListener("click", () => setOpen(list.hidden));
  document.addEventListener("click", (ev) => {
    if (!list.hidden && !wrap.contains(ev.target)) setOpen(false);
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && !list.hidden) {
      setOpen(false);
      toggle.focus();
    }
  });

  /* Under the title where there is one, which is every tutorial that opens
   * with a `# Heading`. A tutorial that opens straight into a section is legal
   * and would otherwise get no marker at all, so it goes to the top of the
   * body instead — after the notice, which is the one thing that outranks it. */
  const heading = document.querySelector("#dl-body h1");
  if (heading) {
    heading.insertAdjacentElement("afterend", wrap);
    return;
  }
  const body = document.getElementById("dl-body");
  const notice = body.querySelector(".dl-archived");
  if (notice) notice.insertAdjacentElement("afterend", wrap);
  else body.insertBefore(wrap, body.firstChild);
}

/* build.py already writes the notice that says which release this is and links
 * to the current one. What it cannot know is how much of this reader's work
 * moves with them, so that is added here rather than duplicated as a second
 * box saying nearly the same thing. */
function annotateNotice() {
  const notice = document.querySelector("#dl-body .dl-archived");
  const home = defaultVersion();
  if (!notice || !home || home.version === currentManifest.version) return;

  for (const link of notice.querySelectorAll(`a[href="${CSS.escape(home.url)}"]`)) {
    link.addEventListener("click", () => writePin(home.version));
  }

  const lines = [];
  if (readPin() === currentManifest.version) {
    lines.push("You are on this one because it is where you left off.");
  }
  const carry = describeCarry(home);
  if (carry) lines.push(`Moving to the current version: ${carry[0].toLowerCase()}${carry.slice(1)}`);
  for (const text of lines) {
    const line = document.createElement("p");
    line.className = "dl-version-carry";
    line.textContent = text;
    notice.appendChild(line);
  }
}

function initVersionsSection() {
  const section = document.getElementById("dl-settings-versions");
  if (!section) return;
  if (versionList().length < 2) {
    section.remove();
    return;
  }

  const note = document.getElementById("dl-versions-note");
  if (note) {
    note.textContent =
      `This tutorial has ${versionList().length} releases. Your work is saved `
      + "against the tutorial rather than against one of them, so it moves with "
      + "you: an answer is there in every version whose cells it belongs to.";
  }

  const group = section.querySelector("[data-versions-follow]");
  const list = document.getElementById("dl-versions-settings");

  function sync() {
    const mode = readFollow();
    for (const btn of group.querySelectorAll("button")) {
      btn.setAttribute("aria-pressed", String(btn.dataset.value === mode));
    }
    fillVersionList(list);
  }

  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    writeFollow(btn.dataset.value);
    sync();
    /* Asking for the newest from an older release is a request to be on the
     * newest, not a preference to take effect the next time they visit. */
    const home = defaultVersion();
    if (btn.dataset.value === "newest" && home
        && home.version !== currentManifest.version) {
      location.href = home.url;
    }
  });

  sync();
}

/* ------------------------------------------------------------------ start */

const currentManifest = readManifest();

/* Before anything is built or booted: a reader who has worked in an older
 * release goes back to it rather than being handed the newest one halfway
 * through. Everything below is skipped, because this page is about to be
 * replaced by another one. */
const leaving = followTheVersionYouLeftOff();

initTexture((dark) => {
  for (const cell of cells) setEditorTheme(cell.editor, dark);
  for (const block of readOnlyBlocks) setEditorTheme(block, dark);
});

buildCells(currentManifest);
initProgressSection();
initVersionsSection();
initVersionMarker();
initSettingsPanel();
initCheatSheet(currentManifest);
trackChromeHeight();
announceRestore(restoreSaved());
annotateNotice();
highlightIllustrativeCode();
const mathsRendered = renderMaths(currentManifest);

if (cells.length === 0 || leaving) {
  /* A prose-only tutorial is a normal tutorial, not a special case
   * (CONTENT_AND_FILE_ARCHITECTURE.md). No cells means no reason to pay for
   * Pyodide at all. */
  /* Nor is there a reason to pay for it on a page that is being replaced this
   * instant by the release the reader left off in. */
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
  describeMismatch,
  versionList,
  readPin,
  writePin,
  readFollow,
  carryOver,
  describeCarry,
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
