
import { createCodeEditor, createReadOnlyCode, setEditorTheme,
         setLineNumbers, setIndentWidth } from "./vendor/codemirror.bundle.js";
import { mountSitePreview } from "./site-relay.js";

const PYODIDE_VERSION = "0.28.3";
const PYODIDE_BASE = new URL(
  globalThis.DEWLAB_PYODIDE_BASE ||
    `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`,
  document.baseURI
).href;

const DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib"];

const TEXTURE_KEY = "dewlab:texture";
const PROGRESS_PREFIX = "dewlab:progress:";
const PROGRESS_BADGES_KEY = "dewlab:progress-badges";
const NOTES_EXPORT_PREFIX = "dewlab:notes-exported-len:";
const NOTES_NUDGE_KEY = "dewlab:notes-nudge";
const NOTES_NUDGE_THRESHOLD = 120;
const RUN_STATS_KEY = "dewlab:run-stats";
const STAGED_HINTS_KEY = "dewlab:staged-hints";
const STAGED_HINTS_RESTART_KEY = "dewlab:staged-hints-restart";
const AUTOSAVE_DELAY = 500;
const SAVED_OUTPUT_STRIP_THRESHOLD = 100_000;
const NON_TUTORIAL_PAGES = new Set(["index", "tree", "about", "topics"]);
const TEXTURE_DEFAULTS = {
  theme: "system", font: "serif", size: 18, width: 34,
  link: "#d4692a", header: "full", contrast: "normal",
  buttons: "both",
  // Cuts CSS transitions/animations site-wide when "reduced" — a plain
  // accessibility toggle, not tied to the system prefers-reduced-motion
  // query, so a reader can ask for it even on a system that hasn't.
  motion: "normal",
  // A multiplier on the code editor's own line height, independent of the
  // overall text size above — a reader who wants more air between lines of
  // code without enlarging the letters themselves.
  codeLineHeight: 1.5,
  // Spaces Tab inserts in a code cell, and what indentOnInput reindents to.
  indent: 4,
  // Line numbers are the CodeMirror default everywhere else this bundle is
  // used, so "on" is the default here too — a reader turns them off, not on.
  linenumbers: "on",
};

const TEXTURE_MIN_SIZE = 16;

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
  // A page with a sql exec cell needs sqlite3 loaded whether it declared its
  // own package list or fell back to DEFAULT_PACKAGES above — added here,
  // once, rather than duplicating DEFAULT_PACKAGES in build.py to append to.
  if (m.needsSqlite && !m.packages.includes("sqlite3")) {
    m.packages = [...m.packages, "sqlite3"];
  }
  m.assetBase = m.assetBase || "";
  m.dataBase = m.dataBase || "";
  m.assetVersions = m.assetVersions || {};
  return m;
}

function assetUrl(manifest, name) {
  const version = manifest.assetVersions[name];
  return manifest.assetBase + name + (version ? `?v=${version}` : "");
}

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

function closeReference() {
  const toggle = document.getElementById("dl-reference-toggle");
  const panel = document.getElementById("dl-reference");
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

function closeSeriesNav() {
  const toggle = document.getElementById("dl-seriesnav-toggle");
  const panel = document.getElementById("dl-seriesnav");
  if (!panel || panel.hasAttribute("hidden")) return;
  panel.setAttribute("hidden", "");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}

function saveSidebarState() {
  const referencePanel = document.getElementById("dl-reference");
  const seriesnavPanel = document.getElementById("dl-seriesnav");
  const settingsPanel = document.getElementById("dl-settings");
  const left = referencePanel && !referencePanel.hasAttribute("hidden") ? "reference"
    : seriesnavPanel && !seriesnavPanel.hasAttribute("hidden") ? "seriesnav"
    : null;
  const right = !!(settingsPanel && !settingsPanel.hasAttribute("hidden"));
  try {
    localStorage.setItem("dewlab:sidebars", JSON.stringify({ left, right }));
  } catch (e) { /* private mode, blocked storage: nothing to remember */ }
}

function restoreSidebarState() {
  if (!window.matchMedia("(min-width: 34rem)").matches) return;
  let state;
  try {
    state = JSON.parse(localStorage.getItem("dewlab:sidebars") || "{}");
  } catch (e) {
    return;
  }

  const leftToggleId = state.left === "reference" ? "dl-reference-toggle"
    : state.left === "seriesnav" ? "dl-seriesnav-toggle"
    : null;
  if (leftToggleId) {
    const toggle = document.getElementById(leftToggleId);
    if (toggle && !toggle.hidden) toggle.click();
  }

  if (state.right) {
    const toggle = document.getElementById("dl-settings-toggle");
    if (toggle) toggle.click();
  }
}

function watchPanelOverlap() {
  const rightPanels = [document.getElementById("dl-settings")].filter(Boolean);
  const leftPanels = [document.getElementById("dl-reference"), document.getElementById("dl-seriesnav")].filter(Boolean);
  const root = document.documentElement;

  const updateAttrs = () => {
    root.toggleAttribute("data-dl-panel-right", rightPanels.some(p => !p.hasAttribute("hidden")));
    root.toggleAttribute("data-dl-panel-left", leftPanels.some(p => !p.hasAttribute("hidden")));
  };
  // Persisting is split from updateAttrs() rather than done unconditionally
  // on every sync: this function runs once synchronously below, before
  // restoreSidebarState() (tutorial-runtime.js's own init sequence) has had
  // a chance to reopen whatever was saved last time — every panel is still
  // hidden at that point, and persisting here would overwrite a real saved
  // preference with "everything closed" before it was ever read back.
  // restoreSidebarState()'s own toggle.click() re-triggers this same
  // MutationObserver-driven path, which does persist, so the saved state
  // ends up correct once the actual open/closed panels are known.
  const sync = () => { updateAttrs(); saveSidebarState(); };
  for (const panel of [...rightPanels, ...leftPanels]) {
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ["hidden"] });
  }
  updateAttrs();

  // The same drag strip on both edges. These two panels relied on native
  // `resize: horizontal` until now, which works but is a corner triangle
  // facing Settings' full-height strip — one page, two affordances, only
  // one of them findable. Wired here rather than
  // in each panel's own init, because this is the one place that already
  // knows which edge each panel is docked to.
  for (const panel of leftPanels) makeEdgeResizable(panel, "left", 256, 640);

  const widthObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      const panel = entry.target;
      if (panel.hasAttribute("hidden")) continue;
      const varName = rightPanels.includes(panel) ? "--dl-panel-right-w" : "--dl-panel-left-w";
      // offsetWidth, not the observer's own contentRect, since the
      // margin needs to clear the panel's full border box (it has both
      // a border and padding), plus a small gutter so text doesn't sit
      // flush against the panel's edge.
      root.style.setProperty(varName, `${panel.offsetWidth + 16}px`);
    }
  });
  for (const panel of [...rightPanels, ...leftPanels]) widthObserver.observe(panel);
}

function clickIsInsidePanels(target, ids) {
  return ids.some((id) => {
    const el = document.getElementById(id);
    return el ? el.contains(target) : false;
  });
}

function makeEdgeResizable(panel, side = "right", min = 256, max = 640, onResize = null) {
  if (!panel || panel.querySelector(".dl-panel-resize-handle")) return;
  const handle = document.createElement("div");
  handle.className = "dl-panel-resize-handle"
    + (side === "left" ? " dl-panel-resize-handle-right" : "");
  handle.setAttribute("aria-hidden", "true");
  panel.prepend(handle);

  let startX = 0;
  let startWidth = 0;

  function onMove(ev) {
    const dx = side === "left" ? ev.clientX - startX : startX - ev.clientX;
    const next = Math.max(min, Math.min(startWidth + dx, Math.min(max, window.innerWidth)));
    panel.style.width = `${next}px`;
  }
  function onUp() {
    handle.classList.remove("dl-panel-resize-active");
    document.removeEventListener("pointermove", onMove);
    document.removeEventListener("pointerup", onUp);
    if (onResize) onResize();
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

function initSettingsPanel() {
  const toggle = document.getElementById("dl-settings-toggle");
  const panel = document.getElementById("dl-settings");
  if (!toggle || !panel) return;

  makeEdgeResizable(panel, "right", 256, 640); // matches .dl-settings' own min/max-width

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    // Settings is right-anchored; the reference and series nav share
    // the left corner instead (see .dl-reference/.dl-seriesnav in
    // tutorial-style.css), so only those two actually conflict with
    // each other — Settings can stay open alongside either.
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
    if (clickIsInsidePanels(ev.target, ["dl-reference-toggle", "dl-reference", "dl-seriesnav-toggle", "dl-seriesnav"])) return;
    setOpen(false);
  });

  for (const section of panel.querySelectorAll(".dl-settings-section")) {
    if (!section.textContent.trim()) section.hidden = true;
  }

  // Search, the same filter-as-you-type shape as the reference panel's own
  // (filterReferenceContent() above) — cleared whenever the panel closes,
  // for the same reason: reopening it later should never start on a stale
  // filter from whichever of this panel's several close paths ran last.
  const searchInput = document.getElementById("dl-settings-search");
  if (searchInput) {
    searchInput.addEventListener("input", () => filterSettingsContent(searchInput.value));
    new MutationObserver(() => {
      if (panel.hasAttribute("hidden") && searchInput.value) {
        searchInput.value = "";
        filterSettingsContent("");
      }
    }).observe(panel, { attributes: true, attributeFilter: ["hidden"] });
  }
}

function filterSettingsContent(query) {
  const panel = document.getElementById("dl-settings");
  const emptyMessage = document.getElementById("dl-settings-empty");
  if (!panel) return;
  const needle = query.trim().toLowerCase();
  let anyRowVisible = false;

  for (const row of panel.querySelectorAll(".dl-texture-row")) {
    const text = `${row.textContent} ${row.dataset.keywords || ""}`.toLowerCase();
    const matches = !needle || text.includes(needle);
    row.hidden = !matches;
    if (matches) anyRowVisible = true;
  }

  if (emptyMessage) emptyMessage.hidden = anyRowVisible || !needle;
}

/* build.py's own kind list — GLOSSARY_KINDS — in the order a reader would
 * find most useful to scan: what a thing *is* before what you *do* with it. */
const GLOSSARY_GROUP_LABELS = {
  concept: "Concepts",
  function: "Functions",
  operator: "Operators",
  formula: "Formulas",
  keyword: "Keywords",
};

function renderReference(manifest) {
  const container = document.getElementById("dl-reference-groups");
  if (!container) return;
  container.replaceChildren();

  const byKind = new Map();
  for (const entry of manifest.glossary || []) {
    if (!byKind.has(entry.kind)) byKind.set(entry.kind, []);
    byKind.get(entry.kind).push(entry);
  }

  for (const [kind, label] of Object.entries(GLOSSARY_GROUP_LABELS)) {
    const group = byKind.get(kind);
    if (!group || !group.length) continue;

    const section = document.createElement("div");
    section.className = "dl-reference-group";
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
      // Where a reader met this, for anything inherited from an earlier
      // tutorial (build.py's origin_of()). The panel already answers "what
      // does this mean"; this answers "where did I meet this", which is the
      // question somebody coming back after a fortnight actually has. A
      // tutorial's own new terms carry no origin — saying "you met this
      // here" on the page teaching it would be noise.
      if (entry.origin && entry.origin.href) {
        const from = document.createElement("p");
        from.className = "dl-term-origin";
        from.append(document.createTextNode("Introduced in "));
        const link = document.createElement("a");
        link.href = entry.origin.href;
        link.textContent = entry.origin.title;
        from.append(link);
        dd.append(from);
      }
      dl.append(dt, dd);
    }
    section.append(dl);
    container.append(section);
  }

  const notes = manifest.notes || [];
  if (notes.length) {
    const section = document.createElement("div");
    section.className = "dl-reference-group";
    const heading = document.createElement("h3");
    heading.textContent = "Notes";
    section.append(heading);
    for (const note of notes) {
      // note.html is build.py's own markdown-to-HTML output for this
      // tutorial's own aside — the same trust level as the rest of the
      // page body, which the shell already writes as raw HTML.
      const div = document.createElement("div");
      div.className = "dl-note";
      div.id = note.id;
      div.innerHTML = note.html;
      section.append(div);
    }
    container.append(section);
  }

  const datasets = manifest.datasets || [];
  if (datasets.length) {
    const section = document.createElement("div");
    section.className = "dl-reference-group";
    const heading = document.createElement("h3");
    heading.textContent = "Datasets used here";
    section.append(heading);

    const dl = document.createElement("dl");
    for (const dataset of datasets) {
      const dt = document.createElement("dt");
      dt.textContent = dataset.name;
      const dd = document.createElement("dd");
      dd.append(document.createTextNode(
        `${dataset.description} — ${dataset.source} (${dataset.license})`));
      dl.append(dt, dd);
    }
    section.append(dl);
    container.append(section);
  }

  // Math Basics (its own tab, renderMathBasics() below) fills the panel
  // whether or not this page has anything of its own — this note is
  // only about the Reference tab's own, page-specific content.
  const nothingYet = document.getElementById("dl-reference-nothing-yet");
  if (nothingYet) nothingYet.hidden = container.children.length > 0;

  // A page with only a handful of terms doesn't need searching; one with
  // a whole series accumulated behind it does. Math Basics' and Python
  // Basics' own fixed sets almost always clear this on their own once
  // they exist, so this mostly still matters for how the Reference tab
  // looks before a series has accumulated much.
  const searchInput = document.getElementById("dl-reference-search");
  const basicsCount = ["mathBasics", "pythonBasics"].reduce((n, key) =>
    n + (manifest[key] || []).reduce((m, group) => m + (group.entries || []).length, 0), 0);
  if (searchInput) {
    searchInput.hidden = container.querySelectorAll("dt, .dl-note").length < 6
      && basicsCount < 6;
  }
}

/* Math Basics: the same fixed set of terms on every page (build.py's
 * load_math_basics()), grouped under the small headings the data file
 * itself carries — Operations, Powers and roots, and so on — rather than
 * GLOSSARY_GROUP_LABELS' kind grouping above, since this data has no
 * "kind" at all, just a term and a plain definition — no example, no
 * origin link, by the house rule math-basics.yaml itself documents. */
function renderMathBasics(manifest) {
  const container = document.getElementById("dl-basics-groups");
  if (!container) return;
  container.replaceChildren();

  for (const group of manifest.mathBasics || []) {
    const section = document.createElement("div");
    section.className = "dl-reference-group";
    const heading = document.createElement("h3");
    heading.textContent = group.label;
    section.append(heading);

    const dl = document.createElement("dl");
    for (const entry of group.entries || []) {
      const dt = document.createElement("dt");
      dt.textContent = entry.term;
      const dd = document.createElement("dd");
      dd.append(document.createTextNode(entry.definition));
      dl.append(dt, dd);
    }
    section.append(dl);
    container.append(section);
  }
}

/* Python Basics: the same shape and site-wide source (build.py's
 * load_python_basics()) as renderMathBasics() above, except an entry
 * here may also carry a short `example` — rendered the same way
 * renderReference() renders a tutorial's own glossary examples — since
 * python-basics.yaml's own house rule allows one where a syntax mark is
 * clearer shown than said. */
function renderPythonBasics(manifest) {
  const container = document.getElementById("dl-python-groups");
  if (!container) return;
  container.replaceChildren();

  for (const group of manifest.pythonBasics || []) {
    const section = document.createElement("div");
    section.className = "dl-reference-group";
    const heading = document.createElement("h3");
    heading.textContent = group.label;
    section.append(heading);

    const dl = document.createElement("dl");
    for (const entry of group.entries || []) {
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

function filterReferenceContent(query) {
  const container = document.getElementById("dl-reference-groups");
  const emptyMessage = document.getElementById("dl-reference-empty");
  if (!container) return;
  const needle = query.trim().toLowerCase();
  let anyGroupVisible = false;

  for (const group of container.querySelectorAll(".dl-reference-group")) {
    let groupHasMatch = false;
    for (const dt of group.querySelectorAll(":scope > dl > dt")) {
      const dd = dt.nextElementSibling;
      const text = `${dt.textContent} ${dd ? dd.textContent : ""}`.toLowerCase();
      const matches = !needle || text.includes(needle);
      dt.hidden = !matches;
      if (dd) dd.hidden = !matches;
      if (matches) groupHasMatch = true;
    }
    for (const note of group.querySelectorAll(":scope > .dl-note")) {
      const matches = !needle || note.textContent.toLowerCase().includes(needle);
      note.hidden = !matches;
      if (matches) groupHasMatch = true;
    }
    group.hidden = !groupHasMatch;
    if (groupHasMatch) anyGroupVisible = true;
  }

  if (emptyMessage) emptyMessage.hidden = anyGroupVisible || !needle;
}

/* Same shape as filterReferenceContent(), shared by both "Basics" tabs'
 * own containers (Math Basics, Python Basics) — one function taking the
 * container/empty ids as arguments, since neither has notes or origin
 * links to skip over: just term/definition pairs to filter. */
function filterBasicsContent(groupsId, emptyId, query) {
  const container = document.getElementById(groupsId);
  const emptyMessage = document.getElementById(emptyId);
  if (!container) return;
  const needle = query.trim().toLowerCase();
  let anyGroupVisible = false;

  for (const group of container.querySelectorAll(".dl-reference-group")) {
    let groupHasMatch = false;
    for (const dt of group.querySelectorAll(":scope > dl > dt")) {
      const dd = dt.nextElementSibling;
      const text = `${dt.textContent} ${dd ? dd.textContent : ""}`.toLowerCase();
      const matches = !needle || text.includes(needle);
      dt.hidden = !matches;
      if (dd) dd.hidden = !matches;
      if (matches) groupHasMatch = true;
    }
    group.hidden = !groupHasMatch;
    if (groupHasMatch) anyGroupVisible = true;
  }

  if (emptyMessage) emptyMessage.hidden = anyGroupVisible || !needle;
}

function filterMathBasicsContent(query) {
  filterBasicsContent("dl-basics-groups", "dl-basics-empty", query);
}

function filterPythonBasicsContent(query) {
  filterBasicsContent("dl-python-groups", "dl-python-empty", query);
}

/* Same open/close mechanics as initSettingsPanel(), staying in sync with
 * initSeriesNav() only — the two share a corner and conflict; Settings
 * does not. Starts hidden in shell.html unless this page's manifest
 * carries a glossary, a note, a dataset, Math Basics, or Python Basics.
 * Math Basics and Python Basics are the same on every page once they
 * exist, so this toggle stops hiding once they do. */
function initReference(manifest) {
  const toggle = document.getElementById("dl-reference-toggle");
  const panel = document.getElementById("dl-reference");
  const hasContent = (manifest.glossary && manifest.glossary.length)
    || (manifest.notes && manifest.notes.length)
    || (manifest.datasets && manifest.datasets.length)
    || (manifest.mathBasics && manifest.mathBasics.length)
    || (manifest.pythonBasics && manifest.pythonBasics.length);
  if (!toggle || !panel || !hasContent) return;

  renderReference(manifest);
  renderMathBasics(manifest);
  renderPythonBasics(manifest);
  toggle.hidden = false;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    // The reference and series nav share the same left-anchored
    // corner (.dl-reference/.dl-seriesnav in tutorial-style.css) and
    // would sit directly on top of each other if both opened — that
    // conflict is real, so only that one still closes the other.
    // Settings is right-anchored and does not conflict with either.
    if (open) closeSeriesNav();
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  const close = document.getElementById("dl-reference-close");
  if (close) close.addEventListener("click", () => { setOpen(false); toggle.focus(); });

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || panel.hasAttribute("hidden")) return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (ev) => {
    if (panel.hasAttribute("hidden")) return;
    if (panel.contains(ev.target) || toggle.contains(ev.target)) return;
    if (clickIsInsidePanels(ev.target, ["dl-settings-toggle", "dl-settings"])) return;
    // The highlight-to-look-up button (initReferenceLookup()) opens this
    // panel, so it is a way in rather than a click outside — without this it
    // would close the panel its own click had just opened.
    if (ev.target.closest && ev.target.closest(".dl-lookup")) return;
    setOpen(false);
  });

  // Three tabs sharing one search box — search filters whichever tab is
  // open, tracked here rather than re-read from the DOM on every
  // keystroke. Switching tabs re-runs the filter against whatever is
  // already typed, so a query survives the switch instead of resetting.
  // An array rather than a hardcoded pair, so a future fourth tab is one
  // more entry here rather than a third copy of this whole block.
  const searchInput = document.getElementById("dl-reference-search");
  const tabs = [
    {
      name: "reference",
      tab: document.getElementById("dl-reference-tab-reference"),
      pane: document.getElementById("dl-reference-pane-reference"),
      placeholder: "Search this page's terms…",
      label: "Search this page's reference",
      filter: filterReferenceContent,
    },
    {
      name: "mathbasics",
      tab: document.getElementById("dl-reference-tab-basics"),
      pane: document.getElementById("dl-reference-pane-basics"),
      placeholder: "Search Math Basics…",
      label: "Search Math Basics",
      filter: filterMathBasicsContent,
    },
    {
      name: "pythonbasics",
      tab: document.getElementById("dl-reference-tab-python"),
      pane: document.getElementById("dl-reference-pane-python"),
      placeholder: "Search Python Basics…",
      label: "Search Python Basics",
      filter: filterPythonBasicsContent,
    },
  ];
  let activeTab = tabs[0];

  function runActiveFilter() {
    if (searchInput) activeTab.filter(searchInput.value);
  }

  function selectTab(name) {
    activeTab = tabs.find((t) => t.name === name) || tabs[0];
    for (const t of tabs) {
      const on = t === activeTab;
      t.tab.setAttribute("aria-selected", String(on));
      t.tab.tabIndex = on ? 0 : -1;
      t.pane.hidden = !on;
    }
    if (searchInput) {
      searchInput.placeholder = activeTab.placeholder;
      searchInput.setAttribute("aria-label", activeTab.label);
    }
    runActiveFilter();
  }

  if (tabs.every((t) => t.tab && t.pane)) {
    for (const [i, t] of tabs.entries()) {
      t.tab.addEventListener("click", () => selectTab(t.name));
      // Left/right arrow keys move focus and selection together, the
      // usual ARIA tabs keyboard pattern — a click already does both at
      // once. Wraps around at either end.
      t.tab.addEventListener("keydown", (ev) => {
        if (ev.key !== "ArrowLeft" && ev.key !== "ArrowRight") return;
        ev.preventDefault();
        const step = ev.key === "ArrowRight" ? 1 : -1;
        const next = tabs[(i + step + tabs.length) % tabs.length];
        next.tab.focus();
        selectTab(next.name);
      });
    }
  }

  // Search, only once the panel actually has enough in it to search
  // (renderReference() decides that and hides the input otherwise).
  // Cleared whenever the panel closes — a MutationObserver on `hidden`
  // rather than hooking every one of this panel's several close paths
  // (toggle click, close button, Escape, click-outside, or being force-
  // closed by the series nav opening), so reopening it later never
  // starts on a stale filter from the last time it was open regardless
  // of which path closed it.
  if (searchInput) {
    searchInput.addEventListener("input", runActiveFilter);
    new MutationObserver(() => {
      if (panel.hasAttribute("hidden") && searchInput.value) {
        searchInput.value = "";
        for (const t of tabs) t.filter("");
      }
    }).observe(panel, { attributes: true, attributeFilter: ["hidden"] });
  }
}

function initReferenceLookup(manifest) {
  const body = document.getElementById("dl-body");
  const panel = document.getElementById("dl-reference");
  const toggle = document.getElementById("dl-reference-toggle");
  if (!body || !panel || !toggle) return;

  // manifest.glossary is a flat list of entries, the same one
  // renderReference() groups by kind for display.
  const terms = (manifest.glossary || [])
    .map((entry) => String(entry.term || "").toLowerCase())
    .filter(Boolean);
  if (!terms.length) return;

  // A selection worth offering a lookup for: long enough not to be a stray
  // character, short enough to be a term rather than a dragged paragraph.
  const SHORTEST = 2;
  const LONGEST = 40;

  const button = document.createElement("button");
  button.type = "button";
  button.className = "dl-lookup";
  button.hidden = true;
  document.body.append(button);

  function hide() { button.hidden = true; }

  function whole(word) {
    // A word-boundary test, built from a selection, so the selection has to
    // be escaped: a reader can select "f()" or "x^2", and those are regex
    // metacharacters before they are anything else.
    return new RegExp(`\\b${word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`);
  }

  function termFor(text) {
    const needle = text.trim().toLowerCase();
    if (needle.length < SHORTEST || needle.length > LONGEST) return null;

    // Exact first, so selecting "running estimate" offers that rather than
    // whichever of it and "estimate" happens to come first in the list.
    if (terms.includes(needle)) return needle;

    // Then a whole-word match either way round: "matrix" selected inside a
    // sentence about a transformation matrix finds the entry, and so does
    // selecting the whole phrase. Whole-word rather than substring is what
    // stops "and" offering pandas and "excellent" offering cell — the same
    // false-positive problem that withdrew prose-linking, reached here by
    // a different route.
    const bounded = whole(needle);
    return terms.find((term) => bounded.test(term))
      || terms.find((term) => whole(term).test(needle))
      || null;
  }

  document.addEventListener("selectionchange", () => {
    const selection = document.getSelection();
    if (!selection || selection.isCollapsed) { hide(); return; }

    // Only the reading. A selection inside a cell's editor belongs to
    // CodeMirror, and one inside the panel itself would be circular.
    const anchor = selection.anchorNode;
    const within = anchor && anchor.nodeType === Node.TEXT_NODE ? anchor.parentElement : anchor;
    if (!within || !body.contains(within) || within.closest(".dl-editor, .dl-output")) {
      hide();
      return;
    }

    const text = selection.toString();
    const term = termFor(text);
    if (!term) { hide(); return; }

    const rect = selection.getRangeAt(0).getBoundingClientRect();
    if (!rect.width && !rect.height) { hide(); return; }

    // A selection can be off-screen — restored by the browser on load, or
    // left behind by a scroll. Placing a button at its coordinates would put
    // the button off-screen too, where it is unreachable but still focusable
    // by keyboard. Nothing to offer for a selection nobody can see.
    const withinViewport = rect.bottom > 0 && rect.top < window.innerHeight;
    if (!withinViewport) { hide(); return; }

    button.textContent = `Look up "${term}"`;
    button.dataset.term = term;
    button.hidden = false;
    // Positioned against the viewport, so the button is fixed rather than
    // absolutely placed — no need to account for the page's own scroll, and
    // a scroll simply dismisses it.
    //
    // Measured after unhiding, because a hidden element has no width to
    // clamp against. Both edges are kept inside the viewport so a selection
    // near the right margin or the last line of the page still gets a
    // button a reader can actually reach.
    const margin = 8;
    const width = button.offsetWidth;
    const height = button.offsetHeight;
    const left = Math.min(Math.max(margin, rect.left),
                          window.innerWidth - width - margin);
    const below = rect.bottom + 6;
    const top = below + height + margin > window.innerHeight
      ? Math.max(margin, rect.top - height - 6)   // above the selection instead
      : below;
    button.style.left = `${Math.max(margin, left)}px`;
    button.style.top = `${top}px`;
  });

  button.addEventListener("mousedown", (ev) => {
    // Before the click, or the selection is gone by the time we read it.
    ev.preventDefault();
  });

  button.addEventListener("click", () => {
    const term = button.dataset.term || "";
    // Let the selection go. The reader has what they asked for, and keeping
    // it would leave this button offering the same lookup a second time —
    // the mousedown above deliberately preserved the selection long enough
    // to read the term off it, and this is where that ends.
    const selection = document.getSelection();
    if (selection) selection.removeAllRanges();
    hide();
    panel.removeAttribute("hidden");
    toggle.setAttribute("aria-expanded", "true");
    closeSeriesNav();
    // The value goes in whether or not the box is visible. renderReference()
    // hides it on a page with only a handful of entries, and the observer in
    // initReference() clears the filter on close by reading this value — so
    // skipping it there left such a page filtered to one term the next time
    // it opened, with no visible box to clear.
    const searchInput = document.getElementById("dl-reference-search");
    if (searchInput) searchInput.value = term;
    filterReferenceContent(term);
  });

  document.addEventListener("scroll", hide, { passive: true });
}

function initSeriesNav() {
  const toggle = document.getElementById("dl-seriesnav-toggle");
  const panel = document.getElementById("dl-seriesnav");
  if (!toggle || !panel) return;
  if (!panel.querySelector(".dl-seriesnav-series")) return;

  toggle.hidden = false;

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    // Shares its corner with the reference (see initReference()'s
    // own comment) — that conflict is real. Settings does not conflict
    // with this one either.
    if (open) closeReference();
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  const close = document.getElementById("dl-seriesnav-close");
  if (close) close.addEventListener("click", () => { setOpen(false); toggle.focus(); });

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || panel.hasAttribute("hidden")) return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (ev) => {
    if (panel.hasAttribute("hidden")) return;
    if (panel.contains(ev.target) || toggle.contains(ev.target)) return;
    if (clickIsInsidePanels(ev.target, ["dl-settings-toggle", "dl-settings"])) return;
    setOpen(false);
  });
}

function setSegChecked(btn, checked) {
  btn.setAttribute("aria-checked", String(checked));
}

function syncSegRoving(group) {
  const buttons = [...group.querySelectorAll("button")];
  const checked = buttons.find((btn) => btn.getAttribute("aria-checked") === "true");
  for (const btn of buttons) btn.tabIndex = btn === (checked || buttons[0]) ? 0 : -1;
}

function initSegKeyboardNav() {
  for (const group of document.querySelectorAll(".dl-seg")) {
    group.addEventListener("keydown", (ev) => {
      const buttons = [...group.querySelectorAll("button:not(:disabled)")];
      const i = buttons.indexOf(document.activeElement);
      if (i === -1) return;
      let next;
      if (ev.key === "ArrowRight" || ev.key === "ArrowDown") next = buttons[(i + 1) % buttons.length];
      else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") next = buttons[(i - 1 + buttons.length) % buttons.length];
      else if (ev.key === "Home") next = buttons[0];
      else if (ev.key === "End") next = buttons[buttons.length - 1];
      else return;
      ev.preventDefault();
      next.click();
      next.focus();
    });
  }
}

function isDarkNow() {
  const explicit = document.documentElement.getAttribute("data-theme");
  if (explicit === "dark") return true;
  if (explicit === "light") return false;
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function loadTexture() {
  let state;
  try {
    state = { ...TEXTURE_DEFAULTS, ...JSON.parse(localStorage.getItem(TEXTURE_KEY) || "{}") };
  } catch (err) {
    return { ...TEXTURE_DEFAULTS };
  }
  if (!(state.size >= TEXTURE_MIN_SIZE)) state.size = TEXTURE_MIN_SIZE;
  return state;
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
  if (state.contrast === "normal") root.removeAttribute("data-contrast");
  else root.setAttribute("data-contrast", state.contrast);
  if (state.buttons === "both") root.removeAttribute("data-button-labels");
  else root.setAttribute("data-button-labels", state.buttons);
  if (state.motion === "normal") root.removeAttribute("data-motion");
  else root.setAttribute("data-motion", state.motion);
  root.style.setProperty("--dl-font-size", state.size + "px");
  root.style.setProperty("--dl-line-width", state.width + "rem");
  root.style.setProperty("--dl-code-line-height", state.codeLineHeight);
  // High contrast overrides a reader's own link colour the same way it
  // already overrides their font choice — but
  // font-family only ever comes from the stylesheet's [data-contrast]
  // rule, while link colour is normally also written here as an inline
  // style, and an inline style always wins over any stylesheet rule
  // regardless of selector specificity. Skipping the inline write while
  // high contrast is on lets that rule apply instead of being shadowed
  // by whatever the reader last picked (including dewlab's own default).
  // The same reasoning applies to the default colour itself. No single
  // inline value can serve both themes: the brand orange is 4.96:1 on the
  // dark background and 3.5:1 on the light one, and a value dark enough
  // for light (4.74:1) drops to 3.66:1 on dark. The stylesheet already
  // carries a value per theme, so a reader who has not picked a colour of
  // their own gets no inline write at all and the right one applies.
  const chosen = state.contrast === "normal" && state.link
                 && state.link.toLowerCase() !== TEXTURE_DEFAULTS.link.toLowerCase();
  if (chosen) root.style.setProperty("--dl-link", state.link);
  else root.style.removeProperty("--dl-link");
}

function initTexture(onThemeChange) {
  const state = loadTexture();
  applyTexture(state);

  const panel = document.getElementById("dl-settings-texture");
  if (!panel) return state;

  const sizeEl = document.getElementById("dl-texture-size");
  const widthEl = document.getElementById("dl-texture-width");
  const linkEl = document.getElementById("dl-texture-link");
  const codeLineHeightEl = document.getElementById("dl-texture-code-line-height");

  function sync() {
    for (const group of panel.querySelectorAll(".dl-seg")) {
      const key = group.dataset.texture;
      const current = group.hasAttribute("data-number") ? String(state[key]) : state[key];
      for (const btn of group.querySelectorAll("button")) {
        setSegChecked(btn, btn.dataset.value === current);
      }
      syncSegRoving(group);
    }
    sizeEl.value = state.size;
    widthEl.value = state.width;
    linkEl.value = state.link;
    codeLineHeightEl.value = state.codeLineHeight;
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
  codeLineHeightEl.addEventListener("input", () => {
    state.codeLineHeight = Number(codeLineHeightEl.value);
    commit();
  });

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

const runAnnouncerEl = document.getElementById("dl-run-announcer");
const statusEl = document.getElementById("dl-status");
const statusTextEl = document.getElementById("dl-status-text");
const bootDotsEl = document.getElementById("dl-boot-dots");

function setStatus(text, kind) {
  if (!statusEl) return;
  if (!text) {
    statusEl.hidden = true;
    if (statusTextEl) statusTextEl.textContent = "";
    return;
  }
  statusEl.hidden = false;
  if (statusTextEl) statusTextEl.textContent = text;
  statusEl.classList.toggle("dl-status-error", kind === "error");
}

function setBooting(active) {
  document.documentElement.toggleAttribute("data-dl-booting", active);
  if (bootDotsEl) bootDotsEl.hidden = !active;
}

/* One entry per `exec` cell on the page, in document order. */
const cells = [];

const customCells = [];

/* One entry per live HTML/CSS/JS site editor on the page — see
 * buildSiteEditors() below. */
const siteEditors = [];

function setCellCollapsed(cell, collapsed) {
  cell.collapsed = collapsed;
  if (cell.contentRegion) cell.contentRegion.hidden = collapsed;
  if (cell.collapsedSummary) {
    cell.collapsedSummary.hidden = !collapsed;
    if (collapsed) {
      const firstLine = (cell.getCode().split("\n")[0] || "").trim();
      cell.collapsedSummary.textContent = firstLine || "(empty)";
    }
  }
  if (cell.collapseBtn) {
    cell.collapseBtn.setAttribute("aria-expanded", String(!collapsed));
    cell.collapseBtn.title = collapsed ? "Expand this cell" : "Collapse this cell";
    cell.collapseBtn.classList.toggle("dl-collapse-toggle-collapsed", collapsed);
  }
}

const REPORT_CODE_LIMIT = 2500;
const REPORT_OUTPUT_LIMIT = 1500;

function truncateForReport(text, limit) {
  if (text.length <= limit) return text;
  return `${text.slice(0, limit)}\n… (cut off here — paste the rest yourself if it matters)`;
}

function updateCellReportLinks(cell, box) {
  const code = truncateForReport(cell.getCode(), REPORT_CODE_LIMIT);
  const output = truncateForReport((cell.outputEl?.innerText || "").trim(), REPORT_OUTPUT_LIMIT);
  const browser = navigator.userAgent;
  for (const link of box.querySelectorAll(".dl-report-issue-link")) {
    const url = new URL(link.href);
    url.searchParams.set("code", code);
    if (output) url.searchParams.set("output", output);
    url.searchParams.set("browser", browser);
    link.href = url.toString();
  }
}

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
    const runLineEl = host.querySelector(".dl-cell-runline");
    const duplicateBtn = host.querySelector(".dl-btn-duplicate");
    const collapseBtn = host.querySelector(".dl-collapse-toggle");
    const contentRegion = host.querySelector(".dl-cell-content");
    const collapsedSummary = host.querySelector(".dl-cell-collapsed-summary");

    const cell = {
      id: spec.id,
      starter: spec.code || "",
      type: spec.type || "python",
      outputEl,
      runBtn,
      runLineEl,
      collapseBtn,
      contentRegion,
      collapsedSummary,
      element: host,
      getCode: () => editor.getValue(),
      /* The author's `expect:` line, if any — evaluated by Python after
       * every run and reported back as `reached` (planning/CELL_HINTS.md). */
      expect: spec.expect || null,
      /* How this cell's runs have gone so far, for its staged hints below;
       * see noteAttempt(). Restored from the saved record, never shown. */
      attempts: freshAttempts(),
      hints: collectStagedHints(spec.id, host),
    };

    const editor = createCodeEditor(editorHost, spec.code || "", {
      dark,
      language: cell.type === "sql" ? "sql" : "python",
      onChange: () => { scheduleSave(); renderCellRunLine(cell); },
      completeNames: pageNamesCompletion,
      getDoc: hoverDoc,
      getSignature: signatureHelp,
      lineNumbersVisible: loadTexture().linenumbers !== "off",
      indentWidth: loadTexture().indent,
    });
    cell.editor = editor;
    cells.push(cell);
    renderCellRunLine(cell);

    runBtn.addEventListener("click", () => runCell(cell));
    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        editor.setValue(cell.starter);
        outputEl.replaceChildren();
        delete cell.lastRunMs;
        delete cell.ranContent;
        delete cell.ranOrder;
        renderCellRunLine(cell);
      });
    }
    initCellRunMenu(cell, host);

    if (collapseBtn) {
      collapseBtn.addEventListener("click", () => {
        setCellCollapsed(cell, !cell.collapsed);
        saveNow();
      });
    }
    if (collapsedSummary) {
      collapsedSummary.addEventListener("click", () => { setCellCollapsed(cell, false); saveNow(); });
      collapsedSummary.addEventListener("keydown", (ev) => {
        if (ev.key !== "Enter" && ev.key !== " ") return;
        ev.preventDefault();
        setCellCollapsed(cell, false);
        saveNow();
      });
    }
    if (duplicateBtn) {
      duplicateBtn.addEventListener("click", () => duplicateAsCustomCell(cell, cell.type));
    }

    const hintIcon = host.querySelector(".dl-hint-icon");
    const hintText = host.querySelector(".dl-hint-text");
    if (hintIcon && hintText) {
      hintIcon.addEventListener("click", () => {
        const open = hintIcon.getAttribute("aria-expanded") === "true";
        hintIcon.setAttribute("aria-expanded", String(!open));
        hintText.hidden = open;
      });
    }

    const reportIcon = host.querySelector(".dl-report-icon");
    const reportBox = host.querySelector(".dl-report-doors");
    if (reportIcon && reportBox) {
      reportIcon.addEventListener("click", () => {
        const open = reportIcon.getAttribute("aria-expanded") === "true";
        reportIcon.setAttribute("aria-expanded", String(!open));
        reportBox.hidden = open;
        if (!open) updateCellReportLinks(cell, reportBox);
      });
    }

    host.addEventListener("keydown", (ev) => {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
        ev.preventDefault();
        runCell(cell);
      }
    });
  }
}

function buildSiteEditors(manifest) {
  const dark = isDarkNow();
  const labelFor = { html: "html", css: "css", js: "javascript" };

  for (const spec of manifest.siteEditors || []) {
    const host = document.querySelector(`.dl-site-editor[data-site-name="${CSS.escape(spec.name)}"]`);
    if (!host) {
      console.warn(`dewlab: manifest lists site editor "${spec.name}" but the page has no such element`);
      continue;
    }
    const iframe = host.querySelector(".dl-site-frame");
    const consoleOut = host.querySelector(".dl-site-console-output");
    const resetBtn = host.querySelector(".dl-btn-site-reset");
    const runBtn = host.querySelector(".dl-btn-site-run");

    const panes = {};
    for (const [lang, paneSpec] of Object.entries(spec.panes || {})) {
      const paneHost = host.querySelector(`.dl-site-pane[data-lang="${lang}"] .dl-editor`);
      if (!paneHost) continue;
      const editor = createCodeEditor(paneHost, paneSpec.code || "", {
        dark,
        language: labelFor[lang] || lang,
        onChange: () => { scheduleSave(); if (lang !== "js") render(); },
        lineNumbersVisible: loadTexture().linenumbers !== "off",
        indentWidth: loadTexture().indent,
      });
      panes[lang] = { id: paneSpec.id, starter: paneSpec.code || "", editor };
    }

    const code = (lang) => (panes[lang] ? panes[lang].editor.getValue() : "");
    const preview = mountSitePreview(iframe, {
      onReset: () => { if (consoleOut) consoleOut.textContent = ""; },
      onConsole: (level, text) => {
        if (!consoleOut) return;
        const line = document.createElement("div");
        line.className = `dl-site-console-line dl-stdout dl-site-console-${level}`;
        line.textContent = text;
        consoleOut.appendChild(line);
      },
      onError: ({ message, where, hint }) => {
        if (!consoleOut) return;
        const line = document.createElement("div");
        line.className = "dl-site-console-line dl-error";
        const text = document.createElement("span");
        text.textContent = where ? `${message} (${where.label}, line ${where.line})` : message;
        line.appendChild(text);
        if (where && panes[where.lang]) {
          const go = document.createElement("button");
          go.type = "button";
          go.className = "dl-site-goto";
          go.textContent = "Go to line";
          go.addEventListener("click", () => selectSiteEditorLine(panes[where.lang].editor, where.line));
          line.appendChild(go);
        }
        consoleOut.appendChild(line);
        if (hint) {
          const hintEl = document.createElement("div");
          hintEl.className = "dl-error-hint";
          hintEl.textContent = hint;
          consoleOut.appendChild(hintEl);
        }
      },
    });

    const editorState = { name: spec.name, panes, ran: false };
    const render = () => preview.render(code("html"), code("css"));
    const run = () => {
      editorState.ran = true;
      preview.run(code("html"), code("css"), code("js"));
      scheduleSave();
    };
    editorState.render = render;
    editorState.run = run;

    if (runBtn) {
      runBtn.addEventListener("mousedown", (e) => e.preventDefault());
      runBtn.addEventListener("click", run);
    }
    if (panes.js) {
      // Capture phase, ahead of CodeMirror's own Enter — the same shape
      // an exec cell's own Ctrl/Cmd+Enter uses above.
      host.querySelector('.dl-site-pane[data-lang="js"]').addEventListener("keydown", (ev) => {
        if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
          ev.preventDefault();
          ev.stopPropagation();
          run();
        }
      }, true);
    }
    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        for (const pane of Object.values(panes)) pane.editor.setValue(pane.starter);
        editorState.ran = false;
        render();
        scheduleSave();
      });
    }

    const widthInput = host.querySelector(".dl-site-width");
    const widthOut = host.querySelector(".dl-site-preview-controls output");
    if (widthInput) {
      widthInput.addEventListener("input", () => {
        iframe.style.width = `${widthInput.value}%`;
        if (widthOut) widthOut.textContent = `${widthInput.value}%`;
      });
    }

    siteEditors.push(editorState);
    render();
  }
}

function selectSiteEditorLine(editor, n) {
  const { view } = editor;
  const line = view.state.doc.line(Math.max(1, Math.min(n, view.state.doc.lines)));
  view.dispatch({ selection: { anchor: line.from, head: line.to }, scrollIntoView: true });
  view.focus();
}

function setRunnable(enabled, label) {
  for (const cell of [...cells, ...customCells]) {
    if (!cell.runBtn) continue; // a text cell has no Run button at all
    cell.runBtn.disabled = !enabled;
    setBtnLabel(cell.runBtn, label || (enabled ? "Run" : "…"));
  }
}

let runSequenceCounter = 0;

/* Formats how long a cell's last run took, human-scale rather than raw
 * milliseconds: "340 ms" under a second, "2.4 s" at or above it. */
function formatRunDuration(ms) {
  return ms < 1000 ? `${Math.round(ms)} ms` : `${(ms / 1000).toFixed(1)} s`;
}

/* "1st", "2nd", "3rd", "4th", … — the ordinal a run-line reports. */
function formatOrdinal(n) {
  const rem100 = n % 100;
  if (rem100 >= 11 && rem100 <= 13) return `${n}th`;
  switch (n % 10) {
    case 1: return `${n}st`;
    case 2: return `${n}nd`;
    case 3: return `${n}rd`;
    default: return `${n}th`;
  }
}

function readRunStats() {
  try {
    return localStorage.getItem(RUN_STATS_KEY) !== "off";
  } catch (err) {
    return true;
  }
}

function writeRunStats(mode) {
  try {
    localStorage.setItem(RUN_STATS_KEY, mode);
  } catch (err) {
    /* This reader's own choice only; forgotten after it, same as the rest
     * of this file's storage refusal shape. */
  }
}

function isStale(cell) {
  return cell.ranContent !== undefined && cell.ranContent !== cell.getCode();
}

function renderCellRunLine(cell) {
  const el = cell.runLineEl;
  if (!el) return;
  clearRunLineTicker(cell);
  el.classList.remove("dl-cell-runline-queued");

  if (cell.ranOrder == null) {
    el.textContent = "Not yet run this session";
    el.classList.add("dl-cell-runline-notrun");
    el.classList.remove("dl-cell-runline-stale");
    return;
  }
  el.classList.remove("dl-cell-runline-notrun");

  const showDuration = readRunStats() && typeof cell.lastRunMs === "number";
  let html = `<span class="dl-run-order">Ran ${formatOrdinal(cell.ranOrder)}</span>`;
  if (showDuration) html += `<span class="dl-run-duration"> in ${formatRunDuration(cell.lastRunMs)}</span>`;
  const stale = isStale(cell);
  if (stale) html += '<span class="dl-run-flag"> — edited since</span>';
  el.classList.toggle("dl-cell-runline-stale", stale);
  el.innerHTML = html;
}

function resetRunSequence() {
  runSequenceCounter = 0;
  for (const cell of cells) {
    delete cell.ranOrder;
    delete cell.ranContent;
    delete cell.lastRunMs;
    renderCellRunLine(cell);
  }
}

function startRunLineTicker(cell) {
  clearRunLineTicker(cell);
  const el = cell.runLineEl;
  if (!el) return;
  el.classList.remove("dl-cell-runline-notrun", "dl-cell-runline-stale", "dl-cell-runline-queued");
  el.classList.add("dl-cell-runline-active");
  const startedAt = performance.now();
  const tick = () => {
    el.textContent = `Running… ${formatRunDuration(performance.now() - startedAt)}`;
    cell._runTicker = setTimeout(tick, 100);
  };
  tick();
}

function clearRunLineTicker(cell) {
  if (cell._runTicker) {
    clearTimeout(cell._runTicker);
    delete cell._runTicker;
  }
  cell.runLineEl?.classList.remove("dl-cell-runline-active");
}

function setRunLineQueued(cell) {
  if (!cell.runLineEl) return;
  clearRunLineTicker(cell);
  cell.runLineEl.classList.remove("dl-cell-runline-notrun", "dl-cell-runline-stale");
  cell.runLineEl.classList.add("dl-cell-runline-queued");
  cell.runLineEl.textContent = "Running next";
}

function initCellRunMenu(cell, host) {
  const wrap = host.querySelector(".dl-cell-more");
  const moreBtn = host.querySelector(".dl-btn-more");
  const menu = host.querySelector(".dl-cell-run-menu");
  if (!wrap || !moreBtn || !menu) return;

  let outsideHandler = null;
  const closeMenu = () => {
    menu.hidden = true;
    moreBtn.setAttribute("aria-expanded", "false");
    if (outsideHandler) {
      document.removeEventListener("click", outsideHandler, { capture: true });
      outsideHandler = null;
    }
  };
  const openMenu = () => {
    menu.hidden = false;
    moreBtn.setAttribute("aria-expanded", "true");
    outsideHandler = (e) => { if (!wrap.contains(e.target)) closeMenu(); };
    // Added after this click has finished bubbling — otherwise the click
    // that opens the menu would immediately reach this listener and
    // close it straight back again.
    setTimeout(() => document.addEventListener("click", outsideHandler, { capture: true }), 0);
  };
  moreBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    if (menu.hidden) openMenu(); else closeMenu();
  });

  // Same Escape-closes-and-returns-focus pattern as Settings/Reference/
  // SeriesNav above — this menu was the one panel on the page missing it.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || menu.hidden) return;
    closeMenu();
    moreBtn.focus();
  });

  const aboveItem = menu.querySelector('[data-run-menu="above"]');
  const belowItem = menu.querySelector('[data-run-menu="below"]');
  aboveItem?.addEventListener("click", (e) => {
    e.stopPropagation();
    closeMenu();
    runAbove(cell.id);
  });
  belowItem?.addEventListener("click", (e) => {
    e.stopPropagation();
    closeMenu();
    runBelow(cell.id);
  });
}

const CUSTOM_CELLS_PREFIX = "dewlab:custom-cells:";

const TRAILING_ANCHOR = "__trailing__";

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function iconButtonHtml(cssClass, icon, label, attrs = "") {
  return (
    `<button type="button" class="dl-btn ${cssClass}"${attrs}>`
    + `<span class="dl-btn-icon" aria-hidden="true">${icon}</span>`
    + `<span class="dl-btn-label">${escapeHtml(label)}</span>`
    + "</button>"
  );
}

function getBtnLabel(btn) {
  return (btn.querySelector(".dl-btn-label") || btn).textContent;
}
function setBtnLabel(btn, text) {
  (btn.querySelector(".dl-btn-label") || btn).textContent = text;
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
  return out.join("\n") || '<p class="dl-doc-empty">Empty note.</p>';
}

function customCellsKey() {
  const manifest = currentManifest || {};
  return `${CUSTOM_CELLS_PREFIX}${manifest.module || "unknown"}:${manifest.slug || "unknown"}`;
}

function generateCustomCellId() {
  return `custom-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

function loadCustomCells() {
  try {
    const raw = JSON.parse(localStorage.getItem(customCellsKey()) || "[]");
    return Array.isArray(raw) ? raw : [];
  } catch (err) {
    return [];
  }
}

function saveCustomCells() {
  const record = [...document.querySelectorAll(".dl-cell-custom")]
    .map((host) => {
      const cell = customCells.find((c) => c.id === host.dataset.cellId);
      if (!cell) return null;
      return {
        id: cell.id,
        type: cell.type,
        anchor: host.dataset.anchor,
        code: cell.getCode(),
        output: cell.outputEl ? cell.outputEl.innerHTML : "",
        collapsed: !!cell.collapsed,
      };
    })
    .filter(Boolean);
  try {
    localStorage.setItem(customCellsKey(), JSON.stringify(record));
  } catch (err) {
    /* Storage full or refused. The reader keeps working; their custom
     * cells just will not be there next time they open this page. */
  }
}

let customSaveTimer = null;

function scheduleCustomSave() {
  clearTimeout(customSaveTimer);
  customSaveTimer = setTimeout(saveCustomCells, AUTOSAVE_DELAY);
}

function createCustomCellElement(id, type) {
  const host = document.createElement("div");
  host.className = type === "text" ? "dl-cell dl-cell-custom dl-cell-text" : "dl-cell dl-cell-custom";
  host.dataset.cellId = id;
  const collapseCol = (
    '<div class="dl-cell-collapse-col">'
    + '<button type="button" class="dl-collapse-toggle" aria-expanded="true" '
    + 'title="Collapse this cell">'
    + '<span class="dl-collapse-caret" aria-hidden="true">&#8250;</span>'
    + "</button>"
    + "</div>"
  );
  // Duplicate and Delete read the same on a reader's own cell as on an
  // authored one (icon, glyph, and title alike — the delete "×" matches
  // compose/dewmini.js's own delBtn) so the same muscle memory carries
  // over; Share and the note's view/edit toggle have no dewmini
  // counterpart to match, since neither exists there.
  const duplicateBtn = iconButtonHtml(
    "dl-btn-duplicate", "&#10697;", "Duplicate",
    ' title="Copy this cell, right below it"',
  );
  const shareBtn = iconButtonHtml(
    "dl-btn-share", "&#8681;", "Save",
    ' title="Save this cell to a file"',
  );
  const deleteBtn = iconButtonHtml("dl-btn-delete", "&#215;", "Delete", ' title="Delete this cell"');
  const head = (label, typeLabel, dataType, headerEnd) => (
    '<div class="dl-cell-head">'
    + '<span class="dl-cell-pill">'
    + `<span class="dl-cell-pill-num">${label}</span>`
    + `<span class="dl-cell-pill-type" data-type="${dataType}">${typeLabel}</span>`
    + "</span>"
    + '<span class="dl-cell-spacer"></span>'
    + `<div class="dl-cell-header-end">${headerEnd}</div>`
    + "</div>"
  );
  if (type === "text") {
    const previewBtn = iconButtonHtml("dl-btn-preview", "&#128065;", "View", ' title="Show this note rendered"');
    host.innerHTML = (
      head("Your note", "Note", "text", previewBtn + duplicateBtn + shareBtn + deleteBtn)
      + '<div class="dl-cell-body-row">'
      + collapseCol
      + '<div class="dl-cell-content">'
      + '<textarea class="dl-doc-editor" placeholder="Notes… (# heading, **bold**, - bullets)"></textarea>'
      + '<div class="dl-doc-render" tabindex="0" hidden></div>'
      + "</div>"
      + '<div class="dl-cell-collapsed-summary" role="button" tabindex="0" hidden></div>'
      + "</div>"
    );
  } else {
    const runAttrs = pyodideReady ? "" : " disabled";
    const runLabel = pyodideReady ? "Run" : "…";
    const runBtn = iconButtonHtml("dl-btn-run", "&#9654;", runLabel, runAttrs);
    host.innerHTML = (
      head("Your cell", "Python", "python", duplicateBtn + shareBtn + deleteBtn)
      + '<div class="dl-cell-body-row">'
      + collapseCol
      + '<div class="dl-cell-content"><div class="dl-editor"></div></div>'
      + '<div class="dl-cell-collapsed-summary" role="button" tabindex="0" hidden></div>'
      + "</div>"
      + '<div class="dl-cell-footbar">'
      + runBtn
      + '<span class="dl-cell-spacer"></span>'
      + '<span class="dl-cell-runline"></span>'
      + "</div>"
      + '<div class="dl-output"></div>'
    );
  }
  return host;
}

function createCustomInsertDivider(anchor, seed = false) {
  const row = document.createElement("div");
  row.className = seed ? "dl-insert dl-insert-seed" : "dl-insert";
  row.dataset.anchor = anchor;

  const line = document.createElement("div");
  line.className = "dl-insert-line";

  const actions = document.createElement("div");
  actions.className = "dl-insert-actions";

  const addCode = document.createElement("button");
  addCode.type = "button";
  addCode.className = "dl-insert-btn";
  addCode.title = "Add a code cell here";
  addCode.textContent = "+ Code";
  addCode.addEventListener("click", () => insertCustomCell(row, "python", "", anchor));

  const addText = document.createElement("button");
  addText.type = "button";
  addText.className = "dl-insert-btn";
  addText.title = "Add a text cell here";
  addText.textContent = "+ Text";
  addText.addEventListener("click", () => insertCustomCell(row, "text", "", anchor));

  actions.append(addCode, addText);
  row.append(line, actions);
  return row;
}

function lastDividerFor(anchor) {
  const all = document.querySelectorAll(`.dl-insert[data-anchor="${CSS.escape(anchor)}"]`);
  return all.length ? all[all.length - 1] : null;
}

function mountCustomCellAfter(afterNode, id, type, code, anchor) {
  const host = createCustomCellElement(id, type);
  host.dataset.anchor = anchor;
  const divider = createCustomInsertDivider(anchor);
  afterNode.insertAdjacentElement("afterend", divider);
  afterNode.insertAdjacentElement("afterend", host);

  const shareBtn = host.querySelector(".dl-btn-share");
  const deleteBtn = host.querySelector(".dl-btn-delete");
  const duplicateBtn = host.querySelector(".dl-btn-duplicate");
  const collapseBtn = host.querySelector(".dl-collapse-toggle");
  const contentRegion = host.querySelector(".dl-cell-content");
  const collapsedSummary = host.querySelector(".dl-cell-collapsed-summary");
  let cell;

  if (type === "text") {
    const textarea = host.querySelector(".dl-doc-editor");
    const renderEl = host.querySelector(".dl-doc-render");
    const previewBtn = host.querySelector(".dl-btn-preview");
    textarea.value = code || "";

    // Clicking a rendered note to get back to editing it (renderEl's own
    // click handler below) works with a mouse, but a touch device has no
    // hover to hint that the note is clickable at all — previewBtn is the
    // same toggle, explicit and always visible, so there is no gesture a
    // reader has to already know about to find their way back in.
    const previewIcon = previewBtn.querySelector(".dl-btn-icon");
    const syncPreviewBtn = () => {
      const editing = !textarea.hidden;
      previewIcon.innerHTML = editing ? "&#128065;" : "&#9998;";
      setBtnLabel(previewBtn, editing ? "View" : "Edit");
      previewBtn.title = editing ? "Show this note rendered" : "Edit this note";
    };
    const showEditor = () => { textarea.hidden = false; renderEl.hidden = true; syncPreviewBtn(); };
    const showRendered = () => {
      if (!textarea.value.trim()) return; // nothing to render — keep it open for typing
      renderEl.innerHTML = renderDocMarkdown(textarea.value);
      renderEl.hidden = false;
      textarea.hidden = true;
      syncPreviewBtn();
    };
    textarea.addEventListener("input", () => scheduleCustomSave());
    textarea.addEventListener("blur", showRendered);
    renderEl.addEventListener("click", showEditor);
    renderEl.addEventListener("keydown", (ev) => { if (ev.key === "Enter") showEditor(); });
    // mousedown, not click: a click while the textarea is focused blurs
    // it first (firing showRendered() above), and only then reaches this
    // handler — by which point textarea.hidden already flipped, so
    // reading it here would toggle straight back to editing. preventing
    // the blur on mousedown keeps the state this handler sees accurate.
    previewBtn.addEventListener("mousedown", (ev) => ev.preventDefault());
    previewBtn.addEventListener("click", () => (textarea.hidden ? showEditor() : showRendered()));
    syncPreviewBtn();

    cell = {
      id,
      type,
      element: host,
      collapseBtn,
      contentRegion,
      collapsedSummary,
      getCode: () => textarea.value,
      focus: () => { showEditor(); textarea.focus(); },
    };
    if (textarea.value.trim()) showRendered();
  } else {
    const editorHost = host.querySelector(".dl-editor");
    const outputEl = host.querySelector(".dl-output");
    const runBtn = host.querySelector(".dl-btn-run");
    const editor = createCodeEditor(editorHost, code || "", {
      dark: isDarkNow(),
      language: type === "sql" ? "sql" : "python",
      onChange: () => scheduleCustomSave(),
      completeNames: pageNamesCompletion,
      getDoc: hoverDoc,
      getSignature: signatureHelp,
      lineNumbersVisible: loadTexture().linenumbers !== "off",
      indentWidth: loadTexture().indent,
    });

    cell = {
      id,
      type,
      editor,
      outputEl,
      runBtn,
      element: host,
      collapseBtn,
      contentRegion,
      collapsedSummary,
      getCode: () => editor.getValue(),
      focus: () => editor.focus(),
      attempts: freshAttempts(),
      hints: [],
    };
    runBtn.addEventListener("click", () => runCell(cell).then(scheduleCustomSave));
    host.addEventListener("keydown", (ev) => {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
        ev.preventDefault();
        runCell(cell).then(scheduleCustomSave);
      }
    });
  }

  customCells.push(cell);
  shareBtn.addEventListener("click", () => exportCustomCell(cell));
  deleteBtn.addEventListener("click", () => deleteCustomCell(cell));
  if (duplicateBtn) {
    duplicateBtn.addEventListener("click", () => duplicateAsCustomCell(cell, cell.type));
  }
  if (collapseBtn) {
    collapseBtn.addEventListener("click", () => {
      setCellCollapsed(cell, !cell.collapsed);
      saveCustomCells();
    });
  }
  if (collapsedSummary) {
    collapsedSummary.addEventListener("click", () => { setCellCollapsed(cell, false); saveCustomCells(); });
    collapsedSummary.addEventListener("keydown", (ev) => {
      if (ev.key !== "Enter" && ev.key !== " ") return;
      ev.preventDefault();
      setCellCollapsed(cell, false);
      saveCustomCells();
    });
  }

  return { cell, divider };
}

function insertCustomCell(afterNode, type, code, anchor) {
  const { cell } = mountCustomCellAfter(afterNode, generateCustomCellId(), type, code, anchor);
  scheduleCustomSave();
  cell.element.scrollIntoView({ behavior: "smooth", block: "center" });
  cell.focus();
  return cell;
}

function addCustomCell(type = "python", code = "") {
  const afterNode = lastDividerFor(TRAILING_ANCHOR);
  return afterNode ? insertCustomCell(afterNode, type, code, TRAILING_ANCHOR) : null;
}

function duplicateAsCustomCell(cell, type) {
  const afterNode = cell.element.nextElementSibling;
  if (!afterNode || !afterNode.classList.contains("dl-insert")) return null; // should not happen
  return insertCustomCell(afterNode, type, cell.getCode(), afterNode.dataset.anchor);
}

function deleteCustomCell(cell) {
  const divider = cell.element.nextElementSibling;
  if (divider && divider.classList.contains("dl-insert")) divider.remove();
  cell.editor?.destroy();
  cell.element.remove();
  const idx = customCells.indexOf(cell);
  if (idx !== -1) customCells.splice(idx, 1);
  saveCustomCells();
}

function exportCustomCell(cell) {
  const payload = { "dewlab-custom-cell": 1, type: cell.type, code: cell.getCode() };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const manifest = currentManifest || {};
  const from = [manifest.module, manifest.slug].filter(Boolean).join("-");
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${from || "dewlab"}-custom-cell.json`;
  link.click();
  URL.revokeObjectURL(link.href);
}

async function importCustomCell(file) {
  let payload;
  try {
    payload = JSON.parse(await file.text());
  } catch (err) {
    setStatus("That file isn't valid JSON.", "error");
    return;
  }
  if (typeof payload.code !== "string") {
    setStatus("That file doesn't look like a shared dewlab cell.", "error");
    return;
  }
  const type = payload.type === "text" ? "text" : payload.type === "sql" ? "sql" : "python";
  if (!addCustomCell(type, payload.code)) return;
  setStatus("Cell loaded — read it before you press Run.");
}

function clearCustomCells() {
  if (!window.confirm("Remove all your own cells? This can't be undone.")) return;
  for (const cell of customCells.splice(0)) {
    cell.editor?.destroy();
  }
  for (const el of document.querySelectorAll(".dl-cell-custom, .dl-insert:not(.dl-insert-seed)")) {
    el.remove();
  }
  saveCustomCells();
}

function initCustomCellsSection() {
  const settingsSection = document.getElementById("dl-settings-custom-cells");
  if (cells.length === 0) {
    if (settingsSection) settingsSection.remove();
    return;
  }

  const realIds = new Set(cells.map((c) => c.id));
  const byAnchor = new Map();
  for (const saved of loadCustomCells()) {
    if (!saved || typeof saved.id !== "string" || typeof saved.code !== "string") continue;
    const type = saved.type === "text" ? "text" : saved.type === "sql" ? "sql" : "python";
    const anchor = typeof saved.anchor === "string" && realIds.has(saved.anchor)
      ? saved.anchor
      : TRAILING_ANCHOR;
    if (!byAnchor.has(anchor)) byAnchor.set(anchor, []);
    byAnchor.get(anchor).push({ ...saved, type });
  }

  const restoreGroup = (seedDivider, anchor) => {
    let point = seedDivider;
    for (const saved of byAnchor.get(anchor) || []) {
      const { cell, divider } = mountCustomCellAfter(point, saved.id, saved.type, saved.code, anchor);
      if (typeof saved.output === "string" && cell.outputEl) cell.outputEl.innerHTML = saved.output;
      if (saved.collapsed) setCellCollapsed(cell, true);
      point = divider;
    }
  };

  for (const real of cells) {
    const seed = createCustomInsertDivider(real.id, true);
    real.element.insertAdjacentElement("afterend", seed);
    restoreGroup(seed, real.id);
  }

  const section = document.createElement("section");
  section.className = "dl-custom-cells";
  section.id = "dl-custom-cells";
  section.innerHTML = (
    "<h2>Try something of your own</h2>"
    + '<p class="dl-panel-note">Add a cell below, or right under any cell '
    + "above — it's separate from the tutorial itself, and it's still here "
    + "next time you visit.</p>"
  );
  document.getElementById("dl-body").appendChild(section);
  const trailingSeed = createCustomInsertDivider(TRAILING_ANCHOR, true);
  section.appendChild(trailingSeed);
  restoreGroup(trailingSeed, TRAILING_ANCHOR);

  const importBtn = document.getElementById("dl-custom-cells-import");
  const file = document.getElementById("dl-custom-cells-file");
  const clearBtn = document.getElementById("dl-custom-cells-clear");
  if (importBtn && file) {
    importBtn.addEventListener("click", () => file.click());
    file.addEventListener("change", async () => {
      const chosen = file.files && file.files[0];
      file.value = "";
      if (chosen) await importCustomCell(chosen);
    });
  }
  if (clearBtn) clearBtn.addEventListener("click", clearCustomCells);
}

function initExportSection() {
  document.getElementById("dl-print-pdf")?.addEventListener("click", () => window.print());
  document.getElementById("dl-export-ipynb")?.addEventListener("click", downloadAsIpynb);
}

function splitLines(text) {
  const lines = text.split("\n");
  return lines.map((line, i) => (i < lines.length - 1 ? `${line}\n` : line));
}

function downloadAsIpynb() {
  const notebookCells = [];
  for (const host of document.querySelectorAll(".dl-cell")) {
    const id = host.dataset.cellId;
    const cell = cells.find((c) => c.id === id) || customCells.find((c) => c.id === id);
    if (!cell) continue;
    const isText = cell.type === "text";
    notebookCells.push({
      cell_type: isText ? "markdown" : "code",
      metadata: {},
      source: splitLines(cell.getCode()),
      ...(isText ? {} : { execution_count: null, outputs: [] }),
    });
  }
  if (notebookCells.length === 0) {
    setStatus("No cells to export yet.", "error");
    return;
  }
  notebookCells.unshift({ cell_type: "markdown", metadata: {}, source: [`# ${document.title}`] });

  const notebook = {
    nbformat: 4,
    nbformat_minor: 5,
    metadata: {
      kernelspec: { display_name: "Python 3", language: "python", name: "python3" },
      language_info: { name: "python", pygments_lexer: "ipython3" },
    },
    cells: notebookCells,
  };
  const manifest = currentManifest || {};
  const from = [manifest.module, manifest.slug].filter(Boolean).join("-");
  const blob = new Blob([JSON.stringify(notebook, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${from || "dewlab"}.ipynb`;
  link.click();
  URL.revokeObjectURL(link.href);
}

let bootPromise = null;
let running = null;

let pyodideReady = false;

let pyodideMT = null;
let toolsMT = null;
let inspectModuleMT = null;
let builtinsModuleMT = null;
let jediHoverFnMT = null;
let jediSignatureFnMT = null;

function lookupLiveNameMT(name) {
  if (!toolsMT || !/^[A-Za-z_]\w*$/.test(name)) return undefined;
  try {
    const local = toolsMT._page_globals.get(name);
    if (local !== undefined) return local;
  } catch {
    /* fall through to builtins */
  }
  if (!builtinsModuleMT) return undefined;
  try {
    return builtinsModuleMT[name];
  } catch {
    return undefined;
  }
}

function docForMT(name) {
  if (!toolsMT || !inspectModuleMT) return null;
  const obj = lookupLiveNameMT(name);
  if (obj === undefined || obj === null) return null;
  try {
    return inspectModuleMT.getdoc(obj) || null;
  } catch {
    return null;
  } finally {
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

function signatureForMT(name) {
  if (!toolsMT || !inspectModuleMT) return null;
  const obj = lookupLiveNameMT(name);
  if (obj === undefined || obj === null) return null;
  let sig;
  try {
    sig = inspectModuleMT.signature(obj);
    return name + sig.toString();
  } catch {
    return null;
  } finally {
    if (sig && typeof sig.destroy === "function") sig.destroy();
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

function jediDocMT(source, line, col) {
  if (!jediHoverFnMT) return null;
  try {
    return jediHoverFnMT(source, line, col) || null;
  } catch {
    return null;
  }
}

function jediSignatureMT(source, line, col) {
  if (!jediSignatureFnMT) return null;
  try {
    return jediSignatureFnMT(source, line, col) || null;
  } catch {
    return null;
  }
}

const NETWORK_PATCH_SOURCE = `
try:
    import pyodide_http
    pyodide_http.patch_all()
except Exception:
    pass
`;

const JEDI_HELPER_SOURCE = `
import jedi

def _dewlab_hover_doc(source, line, col):
    try:
        for d in jedi.Script(source).help(line, col):
            doc = d.docstring()
            if doc:
                return doc
    except Exception:
        pass
    return None

def _dewlab_signature(source, line, col):
    try:
        sigs = jedi.Script(source).get_signatures(line, col)
        if sigs:
            return sigs[0].to_string()
    except Exception:
        pass
    return None
`;

const RESEED_GLOBALS_SOURCE = `
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`;

const SEED_SQL_DB_SOURCE = `
import sqlite3
_dewlab_previous_db = tutorial_tools._page_globals.get("db")
if _dewlab_previous_db is not None:
    _dewlab_previous_db.close()
tutorial_tools._page_globals["db"] = sqlite3.connect(":memory:")
`;

async function loadJediMT() {
  try {
    await pyodideMT.loadPackage(["jedi", "parso"]);
    await pyodideMT.runPythonAsync(JEDI_HELPER_SOURCE);
    jediHoverFnMT = pyodideMT.globals.get("_dewlab_hover_doc");
    jediSignatureFnMT = pyodideMT.globals.get("_dewlab_signature");
  } catch (err) {
    console.warn("dewlab: Jedi failed to load; pre-run tooltips stay live-only", err);
  }
}

async function bootMainThread(manifest) {
  setStatus("Starting Python…");

  if (!globalThis.loadPyodide) {
    const offline = new Error(
      "Python could not be downloaded. This file needs an internet connection " +
        "the first time you open it — the reading works without one."
    );
    offline.dewlabFinal = true; // already says everything useful; do not dress it up
    throw offline;
  }
  pyodideMT = await globalThis.loadPyodide({ indexURL: PYODIDE_BASE });

  setStatus(`Loading ${manifest.packages.join(", ")}…`);
  await pyodideMT.loadPackage(manifest.packages);
  // Separately, and forgivingly: a Pyodide without this package must still
  // boot. See NETWORK_PATCH_SOURCE for what it buys.
  try {
    await pyodideMT.loadPackage(["pyodide-http"]);
    await pyodideMT.runPythonAsync(NETWORK_PATCH_SOURCE);
  } catch {
    /* no browser-backed urllib; tutorial_tools.py's hints cover it */
  }

  setStatus("Preparing the notebook tools…");
  /* The standalone export carries this source inside the page, because
   * fetch cannot read a neighbouring file from disk either. */
  const source = manifest.toolsSource;
  pyodideMT.FS.writeFile("/home/pyodide/tutorial_tools.py", source, { encoding: "utf8" });
  toolsMT = pyodideMT.pyimport("tutorial_tools");
  inspectModuleMT = pyodideMT.pyimport("inspect");
  builtinsModuleMT = pyodideMT.pyimport("builtins");
  toolsMT.configure(manifest.dataBase);

  await pyodideMT.runPythonAsync(RESEED_GLOBALS_SOURCE);
  if (manifest.needsSqlite) await pyodideMT.runPythonAsync(SEED_SQL_DB_SOURCE);

  setStatus("");
  setBooting(false);
  pyodideReady = true;
  setRunnable(true, "Run");
  updateExecutionStatus();
  loadJediMT();
}

async function resetPageStateMT() {
  toolsMT.reset_page_state();
  await pyodideMT.runPythonAsync(RESEED_GLOBALS_SOURCE);
  if (currentManifest.needsSqlite) await pyodideMT.runPythonAsync(SEED_SQL_DB_SOURCE);
}

function pageNamesMT() {
  if (!toolsMT) return [];
  return [...toolsMT._page_globals.keys()].filter((name) => !name.startsWith("_"));
}

function wrapSqlCode(sql) {
  return `import tutorial_tools as _dl_tt\n_ = _dl_tt._run_sql_cell(db, ${JSON.stringify(sql)})`;
}

function codeToRun(cell) {
  return cell.type === "sql" ? wrapSqlCode(cell.getCode()) : cell.getCode();
}

async function runCellMainThread(cell) {
  return JSON.parse(
    await toolsMT.run_cell_report(cell.id, cell.outputEl, codeToRun(cell), cell.expect, cell.name),
  );
}

let worker = null;
let interruptBuffer = null;
let jediReadyWorker = false;
let nextRequestId = 1;
const pendingRequests = new Map(); // id -> resolve

function workerRequest(type, payload) {
  const id = nextRequestId++;
  return new Promise((resolve, reject) => {
    pendingRequests.set(id, { resolve, reject });
    worker.postMessage({ type, id, ...payload });
  });
}

const openStreams = new Map(); // cellId -> {el, cssClass}

function applyOutputEvent(cellId, kind, cssClass, text, markup) {
  // A reader's own cell streams output through this exact same worker
  // path as an authored one — searching only `cells` silently dropped
  // every custom cell's output on the floor, since it never found a
  // match and returned before ever touching `el`.
  const cell = cells.find((c) => c.id === cellId) || customCells.find((c) => c.id === cellId);
  if (!cell) return;
  const el = cell.outputEl;
  if (kind === "stream") {
    let open = openStreams.get(cellId);
    if (!open || open.cssClass !== cssClass) {
      const pre = document.createElement("pre");
      pre.className = cssClass;
      el.appendChild(pre);
      open = { el: pre, cssClass };
      openStreams.set(cellId, open);
    }
    /* textContent, never innerHTML: printed output is data, not markup —
     * the same rule _DomSink itself always followed. */
    open.el.textContent += text;
  } else if (kind === "append") {
    openStreams.delete(cellId);
    const template = document.createElement("template");
    template.innerHTML = markup;
    el.appendChild(template.content);
  } else if (kind === "clear") {
    openStreams.delete(cellId);
    el.replaceChildren();
  }
}

function ensureWorker(manifest) {
  if (worker) return;
  worker = new Worker(new URL(assetUrl(manifest, "pyodide-worker.js"), document.baseURI), {
    type: "module",
  });
  worker.onmessage = (ev) => {
    const msg = ev.data;
    if (msg.type === "status") {
      setStatus(msg.text);
    } else if (msg.type === "jedi-ready") {
      jediReadyWorker = true;
    } else if (msg.type === "output") {
      applyOutputEvent(msg.cellId, msg.kind, msg.cssClass, msg.text, msg.markup);
    } else if (msg.type === "response") {
      const pending = pendingRequests.get(msg.id);
      if (!pending) return;
      pendingRequests.delete(msg.id);
      if ("error" in msg) pending.reject(new Error(msg.error));
      else pending.resolve(msg.result);
    }
  };
}

async function bootWorker(manifest) {
  ensureWorker(manifest);
  await workerRequest("boot", {
    pyodideBase: PYODIDE_BASE,
    packages: manifest.packages,
    /* Absolute: a relative fetch from inside the worker resolves against
     * the worker script's own location, not this page's. */
    toolsSourceUrl: new URL(assetUrl(manifest, "tutorial_tools.py"), document.baseURI).href,
    dataBase: new URL(manifest.dataBase, document.baseURI).href,
    seedDb: !!manifest.needsSqlite,
  });

  if (globalThis.crossOriginIsolated && typeof SharedArrayBuffer !== "undefined") {
    interruptBuffer = new SharedArrayBuffer(4);
    worker.postMessage({ type: "set-interrupt-buffer", buffer: interruptBuffer });
  }

  setBooting(false);
  pyodideReady = true;
  setRunnable(true, "Run");
  updateExecutionStatus();
}

function requestInterrupt() {
  if (!interruptBuffer) return;
  /* 2 is SIGINT in Pyodide's own interrupt-buffer convention. */
  new Int32Array(interruptBuffer)[0] = 2;
}

async function runCellWorker(cell) {
  return workerRequest("run-cell", {
    cellId: cell.id, code: codeToRun(cell), expect: cell.expect, label: cell.name,
  });
}

async function resetPageStateWorker() {
  await workerRequest("reset-page-state", {});
}

async function hoverDoc(name, source, line, col) {
  if (currentManifest.standalone) return docForMT(name) || jediDocMT(source, line, col);
  if (!worker) return null;
  return workerRequest("hover-doc", { name, source, line, col });
}

async function signatureHelp(name, source, line, col, argIndex) {
  void argIndex; // not needed here — the CodeMirror side bolds the argument
  if (currentManifest.standalone) return signatureForMT(name) || jediSignatureMT(source, line, col);
  if (!worker) return null;
  return workerRequest("signature-help", { name, source, line, col });
}

function boot(manifest) {
  return manifest.standalone ? bootMainThread(manifest) : bootWorker(manifest);
}

function resetPageState() {
  return currentManifest.standalone ? resetPageStateMT() : resetPageStateWorker();
}

function ensureBooted(manifest) {
  if (!bootPromise) {
    setBooting(true);
    bootPromise = boot(manifest).catch((err) => {
      console.error("dewlab: Pyodide failed to start", err);
      setBooting(false);
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

async function pageNamesCompletion(context) {
  const word = context.matchBefore(/\w+/);
  if (!word || (word.from === word.to && !context.explicit)) return null;
  const names = currentManifest.standalone
    ? pageNamesMT()
    : worker
      ? await workerRequest("page-names", {})
      : [];
  if (!names.length) return null;
  return { from: word.from, options: names.map((label) => ({ label, type: "variable" })) };
}

async function executeCell(cell) {
  const startedAt = performance.now();
  /* What ran last time, read before it is overwritten — the "ran the same
   * code again" signal a staged hint can wait for (noteAttempt()). */
  const previousCode = cell.ranContent;
  cell.ranContent = cell.getCode();
  const report = currentManifest.standalone
    ? await runCellMainThread(cell)
    : await runCellWorker(cell);
  cell.lastRunMs = performance.now() - startedAt;
  cell.ranOrder = ++runSequenceCounter;
  noteAttempt(cell, report, previousCode);
  maybeRevealHint(cell, report);
  renderCellRunLine(cell);
  saveNow();
  return report.ok;
}

function freshAttempts() {
  return {
    runs: 0,          // runs since the counters were last cleared
    errors: 0,        // of those, how many raised
    sameErrors: 0,    // consecutive runs ending in the same error as the one before
    unchanged: 0,     // consecutive runs of code identical to the run before
    checkFails: 0,    // consecutive runs in which a check() failed
    firstRunAt: null, // when the first counted run happened, for `minutes`
    lastErrorKey: null,
  };
}

function collectStagedHints(cellId, host) {
  const marker = host.querySelector(".dl-hint-marker");
  const folds = document.querySelectorAll(
    `details.dl-hint-staged[data-cell="${CSS.escape(cellId)}"]`,
  );
  return [...folds].map((el, index) => {
    const terms = {};
    for (const term of (el.dataset.after || "").split(/\s+/)) {
      const [key, count] = term.split(":");
      if (key && /^\d+$/.test(count || "")) terms[key] = Number(count);
    }
    /* Opening the fold is what the marker was asking for, so it goes. */
    el.addEventListener("toggle", () => { if (el.open && marker) marker.hidden = true; });
    return { el, index, terms, revealed: false };
  });
}

function noteAttempt(cell, report, previousCode) {
  const a = cell.attempts;
  if (report.error && report.error.type === "KeyboardInterrupt") return;
  a.runs += 1;
  if (a.firstRunAt == null) a.firstRunAt = Date.now();
  a.unchanged = previousCode !== undefined && previousCode === cell.ranContent
    ? a.unchanged + 1 : 0;
  if (report.error) {
    a.errors += 1;
    const key = `${report.error.type}: ${report.error.message}`;
    a.sameErrors = key === a.lastErrorKey ? a.sameErrors + 1 : 1;
    a.lastErrorKey = key;
  } else {
    a.sameErrors = 0;
    a.lastErrorKey = null;
  }
  if (report.check) a.checkFails = report.check.passed ? 0 : a.checkFails + 1;
}

function triggerHolds(terms, a) {
  const value = {
    "errors": a.errors,
    "same-errors": a.sameErrors,
    "unchanged": a.unchanged,
    "runs": a.runs,
    "check-fails": a.checkFails,
    "minutes": a.firstRunAt == null ? 0 : (Date.now() - a.firstRunAt) / 60000,
  };
  return Object.entries(terms).every(([key, count]) => (value[key] ?? 0) >= count);
}

function maybeRevealHint(cell, report) {
  if (report.reached === true) return;
  for (const hint of cell.hints) {
    if (hint.revealed) continue;
    if (!triggerHolds(hint.terms, cell.attempts)) continue;
    hint.revealed = true;
    if (readStagedHints()) {
      showStagedHint(cell, hint, { arriving: true });
      cell.hintArrived = true;
    }
    return;
  }
}

function showStagedHint(cell, hint, { arriving } = {}) {
  hint.el.hidden = false;
  if (!arriving) return;
  hint.el.classList.add("dl-hint-arrived");
  const marker = cell.element.querySelector(".dl-hint-marker");
  if (marker && !hint.el.open) marker.hidden = false;
}

/* Every revealed hint shown or hidden to match the setting — called when
 * the setting changes, and once at load after restoreSaved(). */
function syncStagedHints() {
  const on = readStagedHints();
  for (const cell of cells) {
    for (const hint of cell.hints) {
      if (hint.revealed) hint.el.hidden = !on;
    }
    if (!on) {
      const marker = cell.element.querySelector(".dl-hint-marker");
      if (marker) marker.hidden = true;
    }
  }
}

function resetStagedHints() {
  for (const cell of cells) {
    cell.attempts = freshAttempts();
    for (const hint of cell.hints) {
      hint.revealed = false;
      hint.el.hidden = true;
      hint.el.open = false;
      hint.el.classList.remove("dl-hint-arrived");
    }
    const marker = cell.element.querySelector(".dl-hint-marker");
    if (marker) marker.hidden = true;
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
    /* This reader's own choice only; forgotten after it, same as the rest
     * of this file's storage refusal shape. */
  }
}

function readStagedHintsRestart() {
  try {
    return localStorage.getItem(STAGED_HINTS_RESTART_KEY) === "hide" ? "hide" : "keep";
  } catch (err) {
    return "keep";
  }
}

function writeStagedHintsRestart(mode) {
  try {
    localStorage.setItem(STAGED_HINTS_RESTART_KEY, mode);
  } catch (err) {
    /* As above. */
  }
}

function initStagedHintsToggles() {
  const onOff = document.querySelector("[data-staged-hints]");
  if (onOff) {
    const sync = () => {
      const on = readStagedHints();
      for (const btn of onOff.querySelectorAll("button")) {
        setSegChecked(btn, (btn.dataset.value === "on") === on);
      }
      syncSegRoving(onOff);
    };
    onOff.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      writeStagedHints(btn.dataset.value);
      sync();
      syncStagedHints();
    });
    sync();
  }
  const restart = document.querySelector("[data-staged-hints-restart]");
  if (restart) {
    const sync = () => {
      const mode = readStagedHintsRestart();
      for (const btn of restart.querySelectorAll("button")) {
        setSegChecked(btn, btn.dataset.value === mode);
      }
      syncSegRoving(restart);
    };
    restart.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      writeStagedHintsRestart(btn.dataset.value);
      sync();
    });
    sync();
  }
}

function setCellRunning(cell) {
  const previousLabel = getBtnLabel(cell.runBtn);
  const runIcon = cell.runBtn.querySelector(".dl-btn-icon");
  const canStop = !currentManifest.standalone && interruptBuffer !== null;
  if (canStop) {
    cell.runBtn.disabled = false;
    if (runIcon) runIcon.innerHTML = "&#9632;"; // ■, matches compose/dewmini.js's own Stop affordance
    setBtnLabel(cell.runBtn, "Stop");
    cell.runBtn.classList.add("dl-btn-stop");
  } else {
    cell.runBtn.disabled = true;
    setBtnLabel(cell.runBtn, "Running…");
  }
  return previousLabel;
}

function clearCellRunning(cell, previousLabel) {
  cell.runBtn.disabled = false;
  cell.runBtn.classList.remove("dl-btn-stop");
  const runIcon = cell.runBtn.querySelector(".dl-btn-icon");
  if (runIcon) runIcon.innerHTML = "&#9654;"; // ▶, back from Stop's ■
  setBtnLabel(
    cell.runBtn,
    previousLabel === "Running…" || previousLabel === "Stop" ? "Run" : previousLabel,
  );
}

function announceCellRun(cell) {
  if (!runAnnouncerEl) return;
  const errored = !!cell.outputEl?.querySelector(".dl-error");
  // A live region only announces on a genuine text change — running the
  // same cell twice in a row would say nothing the second time without
  // this. Clearing first, then setting the real text next tick, makes
  // every run its own change even when the result reads identically.
  const hint = cell.hintArrived ? ". A hint has appeared below this cell." : "";
  cell.hintArrived = false;
  runAnnouncerEl.textContent = "";
  setTimeout(() => {
    runAnnouncerEl.textContent = (errored ? "Ran — error" : "Ran — output below") + hint;
  }, 0);
}

async function runCell(cell) {
  if (running === cell) {
    requestInterrupt();
    return;
  }
  if (running) return;
  running = cell;
  const previousLabel = setCellRunning(cell);
  startRunLineTicker(cell);

  let completed = false;
  try {
    await ensureBooted(currentManifest);

    await executeCell(cell);
    completed = true;
  } catch (err) {
    /* Boot failure. Already surfaced in the status bar; nothing useful to add
     * inside the cell. */
  } finally {
    running = null;
    clearCellRunning(cell, previousLabel);
    clearRunLineTicker(cell);
    if (completed) announceCellRun(cell);
  }
}

async function runCellBatch(list, { reset, emptyMessage, describe }) {
  if (running) return;
  if (!list.length) { setStatus(emptyMessage); return; }

  running = true;
  try {
    await ensureBooted(currentManifest);
    if (reset) {
      await resetPageState();
      resetRunSequence();
    }
    setStatus(describe(list.length));
    // Only ever the one cell right after whichever is about to run, kept
    // current as the batch moves along below — not the whole remaining
    // list marked "next" at once.
    if (list[1]) setRunLineQueued(list[1]);

    let errors = 0;
    for (let i = 0; i < list.length; i++) {
      const cell = list[i];
      running = cell;
      const previousLabel = setCellRunning(cell);
      startRunLineTicker(cell);
      try {
        const ok = await executeCell(cell);
        if (!ok) errors += 1;
      } finally {
        clearCellRunning(cell, previousLabel);
        clearRunLineTicker(cell);
      }
      const next = list[i + 1];
      if (next) setRunLineQueued(next);
    }
    setStatus(
      errors ? `Done — ${errors} cell${errors === 1 ? "" : "s"} errored.` : "All cells ran cleanly.",
      errors ? "error" : "ok"
    );
  } catch (err) {
    setStatus(`Python isn't available: ${err.message}`, "error");
  } finally {
    running = null;
  }
}

async function runAllCells() {
  await runCellBatch(cells, {
    reset: true,
    emptyMessage: "No cells to run.",
    describe: (n) => `Running ${n} cell${n === 1 ? "" : "s"}…`,
  });
}

async function runAbove(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const slice = cells.slice(0, idx + 1);
  await runCellBatch(slice, {
    reset: true,
    emptyMessage: "No cells above this one to run.",
    describe: (n) => `Running the ${n} cell${n === 1 ? "" : "s"} above and including this one…`,
  });
}

async function runBelow(id) {
  const idx = cells.findIndex((c) => c.id === id);
  if (idx === -1) return;
  const slice = cells.slice(idx);
  await runCellBatch(slice, {
    reset: false,
    emptyMessage: "No cells here or below to run.",
    describe: (n) => `Running the ${n} cell${n === 1 ? "" : "s"} from here on…`,
  });
}

async function restartPython() {
  if (currentManifest.standalone) {
    pyodideMT = null;
    toolsMT = null;
    inspectModuleMT = null;
    builtinsModuleMT = null;
    jediHoverFnMT = null;
    jediSignatureFnMT = null;
  } else {
    if (worker) {
      try {
        worker.terminate();
      } catch {
        // already gone
      }
    }
    worker = null;
    interruptBuffer = null;
    jediReadyWorker = false;
    for (const { reject } of pendingRequests.values()) {
      reject(new Error("Python was restarted before this finished."));
    }
    pendingRequests.clear();
    openStreams.clear();
  }

  resetRunSequence();
  if (readStagedHintsRestart() === "hide") resetStagedHints();

  bootPromise = null;
  pyodideReady = false;
  setRunnable(false);
  setStatus("Restarting Python…");
  updateExecutionStatus();

  let ok = true;
  try {
    await ensureBooted(currentManifest);
    setStatus("Python restarted.", "ok");
  } catch (err) {
    ok = false;
  }
  updateExecutionStatus();
  return ok;
}

function updateExecutionStatus() {
  const el = document.getElementById("dl-execution-status");
  if (!el) return;
  el.textContent = pyodideReady
    ? "Python is running."
    : "Not started yet — run a cell to start Python.";
}

function initExecutionSection() {
  const section = document.getElementById("dl-settings-execution");
  if (!section) return;
  if (cells.length === 0) {
    section.remove();
    return;
  }

  document.getElementById("dl-restart-python")?.addEventListener("click", async () => {
    if (!confirm("Restart Python? Anything defined in the current session will be lost.")) return;
    await restartPython();
  });
  document.getElementById("dl-restart-run-all")?.addEventListener("click", async () => {
    if (!confirm(
      "Restart Python and run every cell on this page from the top? "
      + "Anything defined in the current session will be lost."
    )) return;
    const ok = await restartPython();
    if (ok) await runAllCells();
  });

  updateExecutionStatus();
}

function initRunStatsToggle() {
  const group = document.querySelector("[data-run-stats]");
  if (!group) return;

  function sync() {
    const on = readRunStats();
    for (const btn of group.querySelectorAll("button")) {
      setSegChecked(btn, (btn.dataset.value === "on") === on);
    }
    syncSegRoving(group);
  }

  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    writeRunStats(btn.dataset.value);
    sync();
    for (const cell of [...cells, ...customCells]) renderCellRunLine(cell);
  });

  sync();
}

const readOnlyBlocks = [];

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

async function renderMaths(manifest) {
  const spans = document.querySelectorAll(".dl-math");
  if (!manifest.math || spans.length === 0) return;
  let renderMath;
  try {
    ({ renderMath } = await import("./vendor/katex.bundle.js"));
  } catch (err) {
    console.error("dewlab: KaTeX failed to load; maths stays as source TeX", err);
    return;
  }
  for (const span of spans) {
    renderMath(span, span.textContent, span.classList.contains("dl-math-display"));
  }
}

let saveTimer = null;
/* Set by initProgressSection() when this page has one; read by saveNow()
 * and restoreSaved() the same way `cells` already is. */
let notesEl = null;

function progressKey() {
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
  if (NON_TUTORIAL_PAGES.has(currentManifest.slug)) return;
  const record = {
    "tutorial-slug": currentManifest.slug,
    "tutorial-module": currentManifest.module,
    "tutorial-version": currentManifest.version,
    saved_at: new Date().toISOString(),
    notes: notesEl ? notesEl.value : "",
    cells: cells.map((cell) => ({
      task_id: cell.id,
      student_code: cell.getCode(),
      output_html: cell.outputEl.innerHTML,
      errored: !!cell.outputEl.querySelector(".dl-error"),
      collapsed: !!cell.collapsed,
      attempts: cell.attempts,
      hints_shown: cell.hints.filter((hint) => hint.revealed).map((hint) => hint.index),
    })),
    // A site editor's own preview and console are cheap to rebuild — no
    // Pyodide, no network — so unlike a cell's output_html, nothing here
    // caches what the preview showed, only what would rebuild it: each
    // pane's current text, and whether Run had been pressed (so a reload
    // shows the script's effect again rather than a blank one, matching
    // the same fix already made to dewmini's own Site tab).
    siteEditors: siteEditors.map((editor) => ({
      name: editor.name,
      panes: Object.fromEntries(
        Object.entries(editor.panes).map(([lang, pane]) => [lang, pane.editor.getValue()]),
      ),
      ran: editor.ran,
    })),
  };
  try {
    localStorage.setItem(progressKey(), JSON.stringify(record));
    rememberVersion();
    showSaveState(record.saved_at);
  } catch (err) {
    const oversized = record.cells.some(
      (cell) => cell.output_html.length > SAVED_OUTPUT_STRIP_THRESHOLD,
    );
    if (oversized) {
      const slimmed = {
        ...record,
        cells: record.cells.map((cell) => (
          cell.output_html.length > SAVED_OUTPUT_STRIP_THRESHOLD
            ? { ...cell, output_html: "" }
            : cell
        )),
      };
      try {
        localStorage.setItem(progressKey(), JSON.stringify(slimmed));
        rememberVersion();
        showSaveState(
          record.saved_at,
          "Saved your code and notes, but this browser ran out of room "
            + "for a large figure. Run that cell again after reloading "
            + "to see it.",
        );
        updateProgressSummary();
        return;
      } catch (err2) {
        /* Still too big even without it — fall through to the plain
         * failure message below. */
      }
    }
    showSaveState(null, "Your browser would not let this page save your work.");
  }
  updateProgressSummary();
}

function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, AUTOSAVE_DELAY);
}

/* Put the work back, and report honestly on what could not be put back. */
function restoreSaved() {
  const record = readSaved();
  if (!record || !Array.isArray(record.cells)) return null;

  if (notesEl && typeof record.notes === "string") notesEl.value = record.notes;

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
    if (saved.collapsed) setCellCollapsed(cell, true);
    if (saved.attempts && typeof saved.attempts === "object") {
      cell.attempts = { ...freshAttempts(), ...saved.attempts };
    }
    if (Array.isArray(saved.hints_shown)) {
      for (const hint of cell.hints) {
        if (saved.hints_shown.includes(hint.index)) {
          hint.revealed = true;
          if (readStagedHints()) showStagedHint(cell, hint);
        }
      }
    }
    restored.push(cell.id);
  }

  if (Array.isArray(record.siteEditors)) {
    const byName = new Map(siteEditors.map((editor) => [editor.name, editor]));
    for (const saved of record.siteEditors) {
      const editor = byName.get(saved.name);
      if (!editor) continue;
      for (const [lang, code] of Object.entries(saved.panes || {})) {
        if (editor.panes[lang] && typeof code === "string") editor.panes[lang].editor.setValue(code);
      }
      // run(), not render(): a reload should show the script's effect
      // again if Run had already been pressed, the same distinction
      // buildSiteEditors()'s own comment explains for a fresh page.
      if (saved.ran) editor.run(); else editor.render();
    }
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

function notesExportKey() {
  const manifest = currentManifest || {};
  return `${NOTES_EXPORT_PREFIX}${manifest.module || "unknown"}:${manifest.slug || "unknown"}`;
}

function readNotesNudge() {
  try {
    return localStorage.getItem(NOTES_NUDGE_KEY) !== "off";
  } catch (err) {
    return true;
  }
}

function writeNotesNudge(mode) {
  try {
    localStorage.setItem(NOTES_NUDGE_KEY, mode);
  } catch (err) {
    /* This reader's own choice only; forgotten after it, same as the rest of
     * this project's toggles when storage is refused. */
  }
}

function updateNotesNudge() {
  const btn = document.getElementById("dl-progress-export");
  if (!btn) return;
  if (!notesEl || !readNotesNudge()) {
    btn.classList.remove("dl-nudge");
    return;
  }
  let exportedLen = 0;
  try {
    exportedLen = parseInt(localStorage.getItem(notesExportKey()) || "0", 10);
  } catch (err) {
    exportedLen = 0;
  }
  const grown = notesEl.value.length - exportedLen;
  btn.classList.toggle("dl-nudge", grown >= NOTES_NUDGE_THRESHOLD);
}

function markNotesExported() {
  if (!notesEl) return;
  try {
    localStorage.setItem(notesExportKey(), String(notesEl.value.length));
  } catch (err) {
  }
}

function initProgressSection() {
  const section = document.getElementById("dl-settings-work");
  if (!section) return;

  if (NON_TUTORIAL_PAGES.has(currentManifest.slug)) {
    section.remove();
    return;
  }

  notesEl = document.getElementById("dl-progress-notes");
  if (notesEl) notesEl.addEventListener("input", () => { scheduleSave(); updateNotesNudge(); });

  document.getElementById("dl-progress-export").addEventListener("click", () => {
    saveNow();
    const record = readSaved() || {};
    const blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    const from = [currentManifest.module, currentManifest.slug].filter(Boolean).join("-");
    link.download = `${from || "dewlab"}-progress.json`;
    link.click();
    URL.revokeObjectURL(link.href);
    markNotesExported();
    updateNotesNudge();
  });

  const file = document.getElementById("dl-progress-file");
  document.getElementById("dl-progress-import").addEventListener("click", () => file.click());
  file.addEventListener("change", async () => {
    const chosen = file.files && file.files[0];
    if (!chosen) return;
    try {
      const record = JSON.parse(await chosen.text());
      const wrong = describeMismatch(record);
      if (wrong) {
        showSaveState(null, wrong);
        file.value = "";
        return;
      }
      localStorage.setItem(progressKey(), JSON.stringify(record));
      announceRestore(restoreSaved());
      showSaveState(record.saved_at);
      updateProgressSummary();
      markNotesExported();
      updateNotesNudge();
    } catch (err) {
      showSaveState(null, "That file could not be read as saved dewlab work.");
    }
    file.value = "";
  });

  document.getElementById("dl-progress-clear").addEventListener("click", () => {
    if (!window.confirm("Clear your work on this tutorial and start again?")) return;
    try {
      localStorage.removeItem(progressKey());
      localStorage.removeItem(notesExportKey());
    } catch (err) {
      /* Nothing to remove, or storage refused. Reset the page either way. */
    }
    for (const cell of cells) {
      cell.editor.setValue(cell.starter);
      cell.outputEl.replaceChildren();
    }
    if (notesEl) notesEl.value = "";
    for (const box of document.querySelectorAll(".dl-restored")) box.remove();
    showSaveState(null);
    updateProgressSummary();
    updateNotesNudge();
  });
}

function progressCounts(entries) {
  /* entries: [{started, errored}]. started means an output exists — run,
   * or restored from a save — not merely that the cell was edited. */
  let done = 0;
  let errored = 0;
  for (const entry of entries) {
    if (!entry.started) continue;
    if (entry.errored) errored++;
    else done++;
  }
  return { total: entries.length, done, errored };
}

function liveProgressCounts() {
  return progressCounts(
    cells.map((cell) => ({
      started: !!cell.outputEl.innerHTML,
      errored: !!cell.outputEl.querySelector(".dl-error"),
    }))
  );
}

function updateProgressSummary() {
  const el = document.getElementById("dl-progress-summary");
  if (!el) return;
  const { total, done, errored } = liveProgressCounts();
  const ran = done + errored;
  if (ran === 0) {
    el.hidden = true;
    return;
  }
  let text = `${ran} of ${total} cell${total === 1 ? "" : "s"} run`;
  if (errored) text += ` · ${errored} with an error`;
  el.textContent = text;
  el.hidden = false;
}

function readProgressBadges() {
  try {
    return localStorage.getItem(PROGRESS_BADGES_KEY) !== "off";
  } catch (err) {
    return true;
  }
}

function writeProgressBadges(mode) {
  try {
    localStorage.setItem(PROGRESS_BADGES_KEY, mode);
  } catch (err) {
    /* This page's own choice only; forgotten after it, same as the rest of
     * this project's texture/follow settings when storage is refused. */
  }
}

function renderContentsProgress() {
  for (const badge of document.querySelectorAll(".dl-progress-badge")) badge.remove();
  if (!readProgressBadges()) return;
  for (const link of document.querySelectorAll(".dl-contents a[data-cells]")) {
    const total = parseInt(link.dataset.cells, 10);
    if (!total) continue;
    let record;
    try {
      const key = `${PROGRESS_PREFIX}${link.dataset.module}:${link.dataset.slug}`;
      record = JSON.parse(localStorage.getItem(key) || "null");
    } catch (err) {
      record = null;
    }
    if (!record || !Array.isArray(record.cells)) continue;
    const { done, errored } = progressCounts(
      record.cells.map((cell) => ({ started: !!cell.output_html, errored: !!cell.errored }))
    );
    const ran = done + errored;
    if (ran === 0) continue;
    const badge = document.createElement("span");
    badge.className = "dl-progress-badge" + (errored ? " dl-progress-badge-errored" : "");
    badge.textContent = `${ran}/${total}`;
    link.insertAdjacentElement("afterend", badge);
  }
}

function initContentsProgress() {
  /* Not the contents page, or a build with no live tutorials listed. */
  if (!document.querySelector(".dl-contents a[data-cells]")) return;
  renderContentsProgress();
}

function initProgressBadgesToggle() {
  const group = document.querySelector("[data-progress-badges]");
  if (!group) return;

  function sync() {
    const on = readProgressBadges();
    for (const btn of group.querySelectorAll("button")) {
      setSegChecked(btn, (btn.dataset.value === "on") === on);
    }
    syncSegRoving(group);
  }

  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    writeProgressBadges(btn.dataset.value);
    sync();
    renderContentsProgress();
  });

  sync();
}

function initNotesNudgeToggle() {
  const group = document.querySelector("[data-notes-nudge]");
  if (!group) return;

  function sync() {
    const on = readNotesNudge();
    for (const btn of group.querySelectorAll("button")) {
      setSegChecked(btn, (btn.dataset.value === "on") === on);
    }
    syncSegRoving(group);
  }

  group.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    writeNotesNudge(btn.dataset.value);
    sync();
    updateNotesNudge();
  });

  sync();
}

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
      setSegChecked(btn, btn.dataset.value === mode);
    }
    syncSegRoving(group);
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

const currentManifest = readManifest();

const leaving = followTheVersionYouLeftOff();

const textureState = initTexture((dark) => {
  for (const cell of [...cells, ...customCells]) {
    if (!cell.editor) continue;
    setEditorTheme(cell.editor, dark);
    setLineNumbers(cell.editor, textureState.linenumbers !== "off");
    setIndentWidth(cell.editor, textureState.indent);
  }
  for (const editor of siteEditors) {
    for (const pane of Object.values(editor.panes)) {
      setEditorTheme(pane.editor, dark);
      setLineNumbers(pane.editor, textureState.linenumbers !== "off");
      setIndentWidth(pane.editor, textureState.indent);
    }
  }
  for (const block of readOnlyBlocks) setEditorTheme(block, dark);
});
initSegKeyboardNav();

buildCells(currentManifest);
buildSiteEditors(currentManifest);
initProgressSection();
initCustomCellsSection();
initExecutionSection();
initRunStatsToggle();
initStagedHintsToggles();
initExportSection();
initVersionsSection();
initVersionMarker();
initSettingsPanel();
initReference(currentManifest);
initReferenceLookup(currentManifest);
initSeriesNav();
watchPanelOverlap();
restoreSidebarState();
initProgressBadgesToggle();
initNotesNudgeToggle();
initContentsProgress();
trackChromeHeight();
announceRestore(restoreSaved());
updateProgressSummary();
updateNotesNudge();
annotateNotice();
highlightIllustrativeCode();
const mathsRendered = renderMaths(currentManifest);

if (cells.length === 0 || leaving) {
  /* Nor is there a reason to pay for it on a page that is being replaced this
   * instant by the release the reader left off in. */
  setStatus("");
} else {
  setRunnable(false, "…");
  ensureBooted(currentManifest).catch(() => {});
}

globalThis.dewlab = {
  version: PYODIDE_VERSION,
  cells,
  restartPython,
  customCells,
  addCustomCell,
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
  customCellsKey,
  downloadAsIpynb,
  jediReady: () => (currentManifest.standalone ? jediHoverFnMT !== null : jediReadyWorker),
  hoverDoc,
  signatureHelp,
  canStop: () => !currentManifest.standalone && interruptBuffer !== null,
};
