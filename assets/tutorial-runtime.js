
import { createCodeEditor, createReadOnlyCode, setEditorTheme,
         setLineNumbers, setIndentWidth } from "./vendor/codemirror.bundle.js";
import { mountSitePreview } from "./site-relay.js";
import { textMatches, tokenize, tokenHits } from "./search-words.js";

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
const HIGHLIGHT_COLOR_KEY = "dewlab:highlight-color";
// Amber first and un-labelled by purpose on purpose: a plain colour name
// leaves what each one means up to whoever is highlighting, the same way
// a paper highlighter set does. Order here is the swatch row's own order.
const HIGHLIGHT_COLORS = ["amber", "green", "blue", "pink"];
const DEFAULT_HIGHLIGHT_COLOR = "amber";
const PANEL_WIDTH_KEY = "dewlab:panel-width";
const AUTOSAVE_DELAY = 500;
const SAVED_OUTPUT_STRIP_THRESHOLD = 100_000;
const NON_TUTORIAL_PAGES = new Set(["index", "tree", "about", "topics"]);
const TEXTURE_DEFAULTS = {
  theme: "system", font: "serif", size: 18, width: 34,
  link: "#d4692a", contrast: "normal",
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
  if (!chrome) {
    // No bar above the page at all (assets/shell.html) — everything that
    // measured from the bar's height measures from the top edge instead.
    // The stylesheet's own default still serves compose/dewmini.html,
    // which keeps a real #dl-chrome of its own.
    document.documentElement.style.setProperty("--dl-chrome-h", "0px");
    return;
  }

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

// Every panel runs from below its own dock to the bottom of the screen,
// and the dock — the identity block and its stack at top-left, the four
// tabs at top-right — sits above the panel in z-index so it stays
// reachable while the panel is open. Left unaccounted for, a panel's own
// header renders right underneath the dock and the two visually collide;
// and the top-left dock's height changes whenever a rung of the tree
// opens or closes. Tracking each dock's real height (the same way
// trackChromeHeight() already tracks --dl-chrome-h) lets the panel's CSS
// start exactly where its dock ends.
function trackCornerDockHeights() {
  const docks = [
    { el: document.querySelector(".dl-corner-dock-tl"), prop: "--dl-corner-tl-h" },
    { el: document.querySelector(".dl-corner-dock-tr"), prop: "--dl-corner-tr-h" },
  ];
  for (const { el, prop } of docks) {
    if (!el) continue;
    const publish = () => {
      document.documentElement.style.setProperty(prop, `${Math.round(el.getBoundingClientRect().height)}px`);
    };
    publish();
    if (typeof ResizeObserver === "function") {
      new ResizeObserver(publish).observe(el);
    } else {
      window.addEventListener("resize", publish);
    }
  }
}

/* On a phone the identity row has no room for the where-you-are tree, so
 * the tree moves — the one real .dl-crumbtrail node, not a copy — into a
 * bottom sheet the launcher opens, and moves back into the dock when the
 * viewport widens again. Moving the node rather than rendering it twice
 * keeps one source of truth for which rungs are open. */
function initWhereYouAre() {
  const sheet = document.getElementById("dl-whereyouare");
  const body = document.getElementById("dl-whereyouare-body");
  const tree = document.querySelector(".dl-crumbtrail");
  const identity = document.querySelector(".dl-corner-identity");
  if (!sheet || !body || !tree || !identity) return;

  const narrow = window.matchMedia("(max-width: 34rem)");
  function place() {
    if (narrow.matches) {
      if (tree.parentElement !== body) body.append(tree);
    } else {
      sheet.setAttribute("hidden", "");
      if (tree.parentElement !== identity) identity.append(tree);
    }
  }
  place();
  narrow.addEventListener("change", place);

  function close() { sheet.setAttribute("hidden", ""); }
  const closeButton = document.getElementById("dl-whereyouare-close");
  if (closeButton) closeButton.addEventListener("click", close);
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && !sheet.hasAttribute("hidden")) close();
  });
  document.addEventListener("click", (ev) => {
    if (sheet.hasAttribute("hidden") || sheet.contains(ev.target)) return;
    close();
  });
  // Following a link in the tree is a jump within this page or away from
  // it; either way the sheet has done its job.
  tree.addEventListener("click", (ev) => { if (ev.target.closest("a")) close(); });
}

function closeReference() {
  const toggle = document.getElementById("dl-reference-toggle");
  const panel = document.getElementById("dl-reference");
  if (!panel || panel.hasAttribute("hidden")) return;
  panel.setAttribute("hidden", "");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
  // Matches closeRightPanels()'s own reset: the left stack only widens to
  // Reference's own width while Reference is open (initReference()'s own
  // setOpen()), so a close reached from outside that path — this one,
  // used when a mobile sheet takes over — has to hand it back itself.
  const leftStack = document.querySelector(".dl-corner-dock-tl .dl-corner-stack");
  if (leftStack) leftStack.style.width = "";
}

// Every right-hand panel is its own; opening one closes the rest, and a
// tab clicked while its own panel is showing closes that panel. Closing
// from outside (the mobile launcher opening a sheet, say) goes through
// here so every tab's aria-pressed is put back too.
// "settings" is Appearance, Behavior and Imports & Exports folded into one
// panel behind one toggle, switched by an internal tablist
// (initSettingsTabs() below) rather than each getting its own corner tab
// — the same pattern Reference already uses for its own three sections.
// "report" is Give Feedback's own door: not in the corner dock at all (a
// fixed circle at the bottom-right, .dl-report-fab), but sharing every
// other bit of open/close machinery this array drives, since a report
// panel and a corner-dock panel close, resize and restore the same way.
const RIGHT_PANELS = ["yourwork", "python", "settings", "report"];

// One shared width for the three that actually live in the corner dock —
// Notes, Python, Settings — not one per panel id: they read as tabs into a
// single dock, so dragging any one wider has to make them all that wide,
// or switching tabs jumps the reading column between whichever width each
// tab happens to remember (initRightPanels() below). Give Feedback's own
// panel sits under its own fixed circle, not that dock, so it never
// touches this key or the dock-stack width sync.
const RIGHT_DOCK_WIDTH_KEY = "dl-right-dock";

function closeRightPanels(except = null) {
  for (const name of RIGHT_PANELS) {
    if (name === except) continue;
    const panel = document.getElementById(`dl-${name}`);
    const toggle = document.getElementById(`dl-${name}-toggle`);
    if (panel && !panel.hasAttribute("hidden")) panel.setAttribute("hidden", "");
    if (toggle) toggle.setAttribute("aria-pressed", "false");
  }
  // Called with no except when nothing on this side is meant to stay open
  // (a mobile sheet taking over, say) — the stack's own width-matching
  // (initRightPanels()'s setOpen()) only runs on the toggle path, so this
  // closing path needs to hand the corner stack back to its own compact
  // default itself.
  if (except === null) {
    const rightStack = document.querySelector(".dl-corner-dock-tr .dl-corner-stack");
    if (rightStack) rightStack.style.width = "";
  }
}

function saveSidebarState() {
  const left = !document.getElementById("dl-reference")?.hasAttribute("hidden") ? "reference"
    : null;
  const right = RIGHT_PANELS.find((name) => !document.getElementById(`dl-${name}`)?.hasAttribute("hidden")) || null;
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

  // A record saved while Series or Documentation still existed as panels
  // names one of those here — no toggle matches, so it restores nothing,
  // the same graceful loss the right side already accepts below.
  const leftToggleId = state.left === "reference" ? "dl-reference-toggle" : null;
  if (leftToggleId) {
    const toggle = document.getElementById(leftToggleId);
    if (toggle && !toggle.hidden) toggle.click();
  }

  // A record saved before the corner-dock rebuild has `right: true`, and
  // one saved before the panels split has `right: "notesreport"` — no
  // toggle id matches either, so this simply restores nothing on the
  // right, the same graceful loss a storage failure gets elsewhere.
  const rightToggle = RIGHT_PANELS.includes(state.right)
    ? document.getElementById(`dl-${state.right}-toggle`) : null;
  if (rightToggle) rightToggle.click();
}

function watchPanelOverlap() {
  const rightPanels = RIGHT_PANELS.map((name) => document.getElementById(`dl-${name}`)).filter(Boolean);
  const leftPanels = [document.getElementById("dl-reference")].filter(Boolean);
  // The corner docks themselves — unlike a panel, always on screen, never
  // hidden as a whole (the top-left one always carries the wordmark, the
  // top-right always its four tabs) — so the reading column needs to
  // clear them permanently, not only while a panel happens to be open
  // over them.
  const leftDocks = [...document.querySelectorAll(".dl-corner-dock-tl")];
  const rightDocks = [...document.querySelectorAll(".dl-corner-dock-tr")];
  const root = document.documentElement;

  // Both sides always have something resting in their corners, so both
  // attributes are permanent now — only the reserved *width* changes,
  // between a corner's own resting size and a panel opened over it.
  root.setAttribute("data-dl-panel-left", "");
  root.setAttribute("data-dl-panel-right", "");

  function widestVisible(elements) {
    let widest = 0;
    for (const el of elements) {
      if (el.hasAttribute("hidden")) continue;
      // offsetWidth, not an observer's own contentRect, since the margin
      // needs to clear the element's full border box (border and padding
      // both), plus a small gutter so text doesn't sit flush against it.
      if (el.offsetWidth > widest) widest = el.offsetWidth;
    }
    return widest;
  }

  const syncWidths = () => {
    root.style.setProperty("--dl-panel-left-w", `${widestVisible([...leftDocks, ...leftPanels]) + 16}px`);
    root.style.setProperty("--dl-panel-right-w", `${widestVisible([...rightDocks, ...rightPanels]) + 16}px`);
  };

  // Persisting is split from syncWidths() rather than done unconditionally
  // on every sync: this function runs once synchronously below, before
  // restoreSidebarState() (tutorial-runtime.js's own init sequence) has had
  // a chance to reopen whatever was saved last time — every panel is still
  // hidden at that point, and persisting here would overwrite a real saved
  // preference with "everything closed" before it was ever read back.
  // restoreSidebarState()'s own toggle.click() re-triggers this same
  // MutationObserver-driven path, which does persist, so the saved state
  // ends up correct once the actual open/closed panels are known.
  const sync = () => { syncWidths(); saveSidebarState(); };
  for (const panel of [...rightPanels, ...leftPanels]) {
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ["hidden"] });
  }
  syncWidths();

  // The same drag strip on both edges. These two panels relied on native
  // `resize: horizontal` until now, which works but is a corner triangle
  // facing Settings' full-height strip — one page, two affordances, only
  // one of them findable. Wired here rather than
  // in each panel's own init, because this is the one place that already
  // knows which edge each panel is docked to.
  const leftStack = document.querySelector(".dl-corner-dock-tl .dl-corner-stack");
  for (const panel of leftPanels) {
    makeEdgeResizable(panel, "left", 256, 640, () => {
      if (leftStack && !panel.hasAttribute("hidden")) leftStack.style.width = panel.style.width;
    });
  }

  const widthObserver = new ResizeObserver(sync);
  for (const el of [...rightPanels, ...leftPanels, ...rightDocks, ...leftDocks]) widthObserver.observe(el);
}

function loadPanelWidth(id) {
  try {
    const all = JSON.parse(localStorage.getItem(PANEL_WIDTH_KEY) || "{}");
    return all[id];
  } catch (err) {
    return undefined;
  }
}

function savePanelWidth(id, width) {
  try {
    const all = JSON.parse(localStorage.getItem(PANEL_WIDTH_KEY) || "{}");
    all[id] = width;
    localStorage.setItem(PANEL_WIDTH_KEY, JSON.stringify(all));
  } catch (err) {
    /* Private mode or blocked storage. A resized panel just falls back to
     * its default width next time, the same graceful loss saveTexture()
     * already accepts for the reader's other preferences. */
  }
}

function makeEdgeResizable(panel, side = "right", min = 256, max = 640, onResize = null, widthKey = null) {
  if (!panel || panel.dataset.resizable) return;
  panel.dataset.resizable = "true";
  const handle = document.createElement("div");
  handle.className = "dl-panel-resize-handle";
  handle.setAttribute("aria-hidden", "true");
  // No longer findable as a child of the panel it resizes (below) -- a
  // page can carry several of these siblings under <body> at once, so
  // this is what a test, or anything else, selects one by.
  if (panel.id) handle.dataset.for = panel.id;
  document.body.append(handle);

  // The handle lives outside the panel (its own comment in
  // tutorial-style.css says why), so nothing keeps it glued to the
  // panel's actual edge for free the way a child element would be.
  // Panel hidden -> handle hidden too, same as the child it used to be;
  // panel visible -> left tracks whichever edge (right-docked: the
  // panel's own left; left-docked: its own right) faces the reading
  // column, on every resize this panel goes through for any reason --
  // this drag, a sibling's drag sharing its width, a font-size change,
  // the window itself resizing.
  function positionHandle() {
    const hidden = panel.hasAttribute("hidden");
    handle.hidden = hidden;
    if (hidden) return;
    const rect = panel.getBoundingClientRect();
    handle.style.left = `${side === "left" ? rect.right : rect.left}px`;
  }
  positionHandle();
  new ResizeObserver(positionHandle).observe(panel);
  new MutationObserver(positionHandle).observe(panel, { attributes: true, attributeFilter: ["hidden"] });

  // widthKey lets several panels share one saved width (RIGHT_DOCK_WIDTH_KEY,
  // below) rather than each remembering its own under its own DOM id.
  const key = widthKey || panel.id;
  const saved = key ? loadPanelWidth(key) : undefined;
  if (saved) panel.style.width = `${Math.max(min, Math.min(saved, max))}px`;

  let startX = 0;
  let startWidth = 0;

  // The reading column keeps at least 26rem — dewlab's own narrowest Width
  // preset — no matter how far a panel gets dragged. .dl-page's own
  // max-width formula reserves each side for what is on it (this panel
  // on this side, the dock or panel on the other) plus a 1rem gutter —
  // .dl-page is border-box, so its padding is inside its width — and this
  // mirrors that arithmetic to
  // find the widest this panel can get before it would push the column
  // below the floor. Nothing did this before, so a drag could ask for
  // more room than the column had left to give, and crush it toward zero.
  function otherSideWidthPx() {
    const varName = side === "left" ? "--dl-panel-right-w" : "--dl-panel-left-w";
    const value = getComputedStyle(document.documentElement).getPropertyValue(varName);
    return parseFloat(value) || 0;
  }
  function floorCapPx() {
    const rootPx = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
    // 16px is the gutter watchPanelOverlap() adds to a side's width.
    return window.innerWidth - otherSideWidthPx() - (26 + 1) * rootPx - 16;
  }

  function onMove(ev) {
    const dx = side === "left" ? ev.clientX - startX : startX - ev.clientX;
    const cap = Math.min(max, floorCapPx());
    const next = Math.max(min, Math.min(startWidth + dx, cap));
    panel.style.width = `${next}px`;
    // Called directly here, on every move, rather than left to the
    // ResizeObserver above alone -- that one is still what catches every
    // *other* reason this panel's width can change (a sibling sharing it,
    // a font-size change, the window itself), but this drag is the one
    // path onResize() and the handle's own position both need to feel
    // perfectly in step with, not just eventually consistent.
    positionHandle();
    // Without this, onResize() only ran once, on release — the panel
    // itself (and, via its own ResizeObserver, the reading column)
    // tracked the drag live, but the corner-dock tab stack this callback
    // widens to match sat frozen at its old width until the drag ended,
    // then jumped to catch up. Calling it here too keeps the tabs moving
    // with the same motion as the panel beneath them.
    if (onResize) onResize();
  }
  function onUp() {
    handle.classList.remove("dl-panel-resize-active");
    document.removeEventListener("pointermove", onMove);
    document.removeEventListener("pointerup", onUp);
    if (key) savePanelWidth(key, panel.getBoundingClientRect().width);
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

// One right-hand panel per corner tab (RIGHT_PANELS above), each opened
// by its own tab and closed by that tab again, its close button, or
// Escape — a docked panel does not close on a click outside it (DECISIONS_LOG
// 7.99 already ruled this for dewmini's own rails: "a docked rail must not
// close on an outside click, unlike a popover"), so the left dock's own
// panel can stay open at the same time without either one stealing focus
// from the other. Appearance (now a tab inside Settings, not a panel of
// its own) alone carries a search box, filtering its own rows. All three
// share one dock width
// (RIGHT_DOCK_WIDTH_KEY): dragging one panel's edge applies the new width
// to the other two immediately, so switching tabs never resizes the dock
// underneath the reading column.
function initRightPanels() {
  const panels = RIGHT_PANELS.map((name) => ({
    name,
    panel: document.getElementById(`dl-${name}`),
    toggle: document.getElementById(`dl-${name}-toggle`),
    close: document.getElementById(`dl-${name}-close`),
  })).filter((p) => p.panel && p.toggle);
  if (!panels.length) return;

  const searchInput = document.getElementById("dl-appearance-search");
  const emptyMessage = document.getElementById("dl-appearance-empty");
  const appearance = document.getElementById("dl-settings-pane-appearance");
  function runFilter() {
    if (!searchInput || !appearance) return;
    const anyRowVisible = filterTextureRows(appearance, searchInput.value);
    if (emptyMessage) emptyMessage.hidden = anyRowVisible || !searchInput.value.trim();
  }
  if (searchInput) searchInput.addEventListener("input", runFilter);

  // The stack widens to match whichever panel is actually open, so the two
  // read as one column instead of a narrow strip sitting askew over a
  // wider box — but only while one is open. Left alone, it stays at its
  // own compact CSS default (12.5rem) rather than permanently reserving a
  // whole panel's width off the reading column for nothing on screen to
  // justify it, so this is set in setOpen() below, not once here.
  const rightStack = document.querySelector(".dl-corner-dock-tr .dl-corner-stack");

  // Give Feedback's own panel shares every open/close path below, but not
  // the corner dock's width story: it opens from its own fixed circle, not
  // a tab in .dl-corner-dock-tr, so it neither drags the other three's
  // shared width around nor pushes the dock stack wider while it's open.
  const dockLinked = panels.filter((p) => p.name !== "report");

  for (const p of panels) {
    for (const section of p.panel.querySelectorAll(".dl-settings-section")) {
      if (!section.textContent.trim()) section.hidden = true;
    }
    if (p.name !== "report") {
      makeEdgeResizable(p.panel, "right", 256, 640, () => {
        const width = p.panel.style.width;
        for (const other of dockLinked) {
          if (other.panel !== p.panel) other.panel.style.width = width;
        }
        if (rightStack && !p.panel.hasAttribute("hidden")) rightStack.style.width = width;
      }, RIGHT_DOCK_WIDTH_KEY);
    }

    function setOpen(open) {
      p.panel.toggleAttribute("hidden", !open);
      p.toggle.setAttribute("aria-pressed", String(open));
      if (rightStack && p.name !== "report") {
        rightStack.style.width = open ? `${p.panel.getBoundingClientRect().width}px` : "";
      }
      if (!open) {
        if (p.name === "settings" && searchInput && searchInput.value) {
          searchInput.value = "";
          runFilter();
        }
        return;
      }
      closeRightPanels(p.name);
      // The notes textarea may have grown (or been given a value) while
      // its panel was hidden, and a hidden element's scrollHeight reads as
      // 0 — re-measure now that it's actually laid out.
      if (p.name === "yourwork") {
        if (notesEl) autoGrowTextarea(notesEl);
        refreshHighlightsList();
      }
      if (p.name === "python") refreshPythonState();
    }

    p.toggle.addEventListener("click", () => setOpen(p.panel.hasAttribute("hidden")));
    if (p.close) p.close.addEventListener("click", () => { setOpen(false); p.toggle.focus(); });

    document.addEventListener("keydown", (ev) => {
      if (ev.key !== "Escape" || p.panel.hasAttribute("hidden")) return;
      setOpen(false);
    });

  }
}

/* Settings' own tablist — Appearance, Behavior, Imports & Exports, one
 * panel behind one corner toggle rather than three. The plain half of
 * initReference()'s own tab-switching (click or arrow keys move the
 * selection): no shared search across tabs the way Reference's is, since
 * only Appearance carries one, so this just hides that search box outside
 * its own tab rather than threading it through every tab like Reference's
 * per-tab filter callbacks. */
function initSettingsTabs() {
  const searchInput = document.getElementById("dl-appearance-search");
  const tabs = [
    {
      name: "appearance",
      tab: document.getElementById("dl-settings-tab-appearance"),
      pane: document.getElementById("dl-settings-pane-appearance"),
    },
    {
      name: "behavior",
      tab: document.getElementById("dl-settings-tab-behavior"),
      pane: document.getElementById("dl-settings-pane-behavior"),
    },
    {
      name: "importsexports",
      tab: document.getElementById("dl-settings-tab-importsexports"),
      pane: document.getElementById("dl-settings-pane-importsexports"),
    },
  ];
  if (!tabs.every((t) => t.tab && t.pane)) return;

  function selectTab(name) {
    for (const t of tabs) {
      const on = t.name === name;
      t.tab.setAttribute("aria-selected", String(on));
      t.tab.tabIndex = on ? 0 : -1;
      t.pane.hidden = !on;
    }
    if (searchInput) searchInput.hidden = name !== "appearance";
  }

  for (const [i, t] of tabs.entries()) {
    t.tab.addEventListener("click", () => selectTab(t.name));
    // Left/right arrow keys move focus and selection together, the usual
    // ARIA tabs keyboard pattern — matches initReference()'s own tabs.
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

/* Filters Appearance's rows by their own text and keywords — the same
 * "search follows what's shown" rule initReference() already uses. */
function filterTextureRows(pane, query) {
  const needle = query.trim().toLowerCase();
  let anyRowVisible = false;
  for (const row of pane.querySelectorAll(".dl-texture-row")) {
    const text = `${row.textContent} ${row.dataset.keywords || ""}`.toLowerCase();
    const matches = !needle || text.includes(needle);
    row.hidden = !matches;
    if (matches) anyRowVisible = true;
  }
  return anyRowVisible;
}

/* The phone-only "one launcher instead of six tabs" menu — see the CSS
 * media query and shell.html's own comment for why. Every row forwards
 * to a real corner toggle (still in the page, just hidden by the same
 * media query) rather than re-implementing open/close/exclusivity here;
 * a hidden element's own .click() still fires its listeners normally,
 * only real user interaction with it is blocked. The one row with no
 * toggle to forward to, "Where you are", opens the sheet
 * initWhereYouAre() keeps the tree in on a phone. */
function initMobileLauncher() {
  const fab = document.getElementById("dl-mobile-fab");
  const menu = document.getElementById("dl-mobile-menu");
  if (!fab || !menu) return;

  // Reference only exists on some pages, decided once at load and never
  // toggled again afterward — mirroring that decision once here, rather
  // than watching for a change that can't happen. Where-you-are exists
  // wherever there is a tree to show, which is every tutorial page.
  for (const name of ["reference"]) {
    const real = document.getElementById(`dl-${name}-toggle`);
    const item = document.getElementById(`dl-mobile-item-${name}`);
    if (real && item) item.hidden = real.hidden;
  }
  const whereItem = document.getElementById("dl-mobile-item-whereyouare");
  if (whereItem) whereItem.hidden = !document.querySelector(".dl-crumbtrail");

  function setOpen(open) {
    menu.toggleAttribute("hidden", !open);
    fab.setAttribute("aria-expanded", String(open));
  }

  fab.addEventListener("click", () => setOpen(menu.hasAttribute("hidden")));

  for (const item of menu.querySelectorAll(".dl-mobile-menu-item")) {
    item.addEventListener("click", (ev) => {
      // Still needed for the sheet path below: showing Where You Are
      // leaves this original event bubbling to document afterward, where
      // its own outside-click listener sees a click that landed on
      // neither the sheet nor its own close button, and closes right
      // back what the line below just opened. The toggle-forwarding path
      // no longer has an equivalent listener to guard against (a docked
      // panel doesn't close on an outside click at all now), but one
      // stopPropagation() covers both forwarding shapes this handler can
      // take, so it stays unconditional rather than sheet-only.
      ev.stopPropagation();
      setOpen(false);
      if (item.dataset.sheet) {
        const sheet = document.getElementById(item.dataset.sheet);
        if (sheet) { closeReference(); closeRightPanels(); sheet.removeAttribute("hidden"); }
        return;
      }
      const real = document.getElementById(item.dataset.forward);
      if (real) real.click();
    });
  }

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || menu.hasAttribute("hidden")) return;
    setOpen(false);
    fab.focus();
  });

  document.addEventListener("click", (ev) => {
    if (menu.hasAttribute("hidden")) return;
    if (menu.contains(ev.target) || fab.contains(ev.target)) return;
    setOpen(false);
  });
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

/* The panel's own search box narrows the list with the same word
 * matching every other search box on the site uses (search-words.js):
 * "loops" finds loop, "chance" finds probability, "poly" finds
 * polynomial, and a bare fragment still narrows as a substring. */
function filterReferenceContent(query) {
  const container = document.getElementById("dl-reference-groups");
  const emptyMessage = document.getElementById("dl-reference-empty");
  if (!container) return;
  const needle = query.trim();
  let anyGroupVisible = false;

  for (const group of container.querySelectorAll(".dl-reference-group")) {
    let groupHasMatch = false;
    for (const dt of group.querySelectorAll(":scope > dl > dt")) {
      const dd = dt.nextElementSibling;
      const text = `${dt.textContent} ${dd ? dd.textContent : ""}`;
      const matches = textMatches(text, needle);
      dt.hidden = !matches;
      if (dd) dd.hidden = !matches;
      if (matches) groupHasMatch = true;
    }
    for (const note of group.querySelectorAll(":scope > .dl-note")) {
      const matches = textMatches(note.textContent, needle);
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
  const needle = query.trim();
  let anyGroupVisible = false;

  for (const group of container.querySelectorAll(".dl-reference-group")) {
    let groupHasMatch = false;
    for (const dt of group.querySelectorAll(":scope > dl > dt")) {
      const dd = dt.nextElementSibling;
      const text = `${dt.textContent} ${dd ? dd.textContent : ""}`;
      const matches = textMatches(text, needle);
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

/* Same open/close mechanics as initDocumentationDock(), staying in sync
 * with initSeriesNav() and initDocumentationDock() — the three share a
 * corner and conflict; the right-anchored docks do not. Starts hidden in
 * shell.html unless this page's manifest carries a glossary, a note, a
 * dataset, Math Basics, or Python Basics.
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

  const leftStack = document.querySelector(".dl-corner-dock-tl .dl-corner-stack");

  function setOpen(open) {
    panel.toggleAttribute("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    if (leftStack) {
      leftStack.style.width = open ? `${panel.getBoundingClientRect().width}px` : "";
    }
  }

  toggle.addEventListener("click", () => setOpen(panel.hasAttribute("hidden")));

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || panel.hasAttribute("hidden")) return;
    setOpen(false);
    toggle.focus();
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

/* Highlights and margin notes: a reader marks a passage of prose,
 * durably, with an optional note tied to it. Anchoring a highlight
 * needs no build-time id — a highlight instead
 * records where it was (an ordinal position among the page's prose
 * blocks) and what it was (the selected text, plus a little context to
 * tell two identical sentences apart), all computed from the live DOM.
 * Restoring one after a later edit searches nearby blocks before giving
 * up, the same "a notice, never a block" posture the version-mismatch
 * banner already uses for a cell whose id disappeared.
 *
 * Only the anchoring lookup lives here so far — nothing yet calls it. */

const PROSE_BLOCK_SELECTOR = "p, li, td, th, blockquote, dt, dd, h1, h2, h3, h4, h5, h6";

// Every anchorable passage in `root`, in reading order. A block nested
// inside another matching block (a loose list's `<li><p>` being the
// common case) is skipped in favour of the inner one, which is the more
// precise anchor; a cell's own code and output are excluded outright,
// the same exclusion the selection toolbar below already applies, since
// neither is prose.
function proseBlocks(root = document.getElementById("dl-body")) {
  if (!root) return [];
  return Array.from(root.querySelectorAll(PROSE_BLOCK_SELECTOR)).filter((el) => (
    !el.closest(".dl-editor, .dl-output") && !el.querySelector(PROSE_BLOCK_SELECTOR)
  ));
}

// How much text either side of a quote to keep, for telling apart two
// identical sentences in the same block. Not "context" in a reading
// sense — just enough characters to disambiguate.
const ANCHOR_CONTEXT = 24;

// The other half of locateHighlightAnchor() below: given a block and the
// [start, end) character offsets of a selection inside its own
// `textContent`, the {quote, prefix, suffix} triple a highlight's anchor
// stores.
function describeQuote(block, start, end) {
  const text = block.textContent;
  return {
    quote: text.slice(start, end),
    prefix: text.slice(Math.max(0, start - ANCHOR_CONTEXT), start),
    suffix: text.slice(end, end + ANCHOR_CONTEXT),
  };
}

// Where a quote sits inside one block's own text. A block with the quote
// appearing exactly once needs no prefix/suffix at all — the common
// case, and the one this returns quickly without looking at either.
// A block with it appearing more than once (the same short phrase used
// twice in one paragraph) is resolved by requiring an exact match on the
// surrounding text instead; failing to disambiguate is treated the same
// as not finding the quote at all, rather than guessing.
function findQuoteInBlockText(text, quote, prefix, suffix) {
  if (!quote) return -1;
  const positions = [];
  for (let i = text.indexOf(quote); i !== -1; i = text.indexOf(quote, i + 1)) {
    positions.push(i);
  }
  if (positions.length <= 1) return positions.length ? positions[0] : -1;
  const match = positions.find((pos) => (
    text.slice(Math.max(0, pos - ANCHOR_CONTEXT), pos) === prefix
      && text.slice(pos + quote.length, pos + quote.length + ANCHOR_CONTEXT) === suffix
  ));
  return match === undefined ? -1 : match;
}

// How many blocks either side of the saved position are worth searching
// before a highlight counts as gone. An edit usually moves a passage a
// little rather than relocating it across the page, so a small window
// catches the ordinary case (a paragraph inserted or removed above it)
// without turning a genuinely deleted passage into a false match found
// by coincidence somewhere far down the page.
const ANCHOR_SEARCH_WINDOW = 5;

// Rebuilds {block, index} for a saved highlight anchor
// ({block_index, quote, prefix, suffix}), tolerating the page having
// drifted a little since the highlight was made. `null` means genuinely
// gone (the caller drops it, and says so, rather than guessing).
function locateHighlightAnchor(anchor, root = document.getElementById("dl-body")) {
  const blocks = proseBlocks(root);
  if (!blocks.length) return null;

  const { block_index: blockIndex, quote, prefix, suffix } = anchor;
  const order = [blockIndex];
  for (let d = 1; d <= ANCHOR_SEARCH_WINDOW; d++) order.push(blockIndex - d, blockIndex + d);

  for (const i of order) {
    const block = blocks[i];
    if (!block) continue;
    const index = findQuoteInBlockText(block.textContent, quote, prefix, suffix);
    if (index !== -1) return { block, index };
  }
  return null;
}

// The other direction: [start, end) character offsets into a block's own
// flattened `textContent` -- exactly what locateHighlightAnchor() and
// describeQuote() already work in -- to the DOM Range spanning that text,
// however many text nodes it crosses. This is what makes a *restored*
// highlight showable at all: locateHighlightAnchor() only ever hands back
// a number, and wrapRange() below only ever accepts a live Range.
function rangeForOffsets(block, start, end) {
  const doc = block.ownerDocument || document;
  const walker = doc.createTreeWalker(block, NodeFilter.SHOW_TEXT);
  const range = doc.createRange();
  let pos = 0;
  let started = false;
  let node = walker.nextNode();
  while (node) {
    const nodeEnd = pos + node.length;
    if (!started && nodeEnd >= start) {
      range.setStart(node, start - pos);
      started = true;
    }
    if (started && nodeEnd >= end) {
      range.setEnd(node, end - pos);
      return range;
    }
    pos = nodeEnd;
    node = walker.nextNode();
  }
  return null; // the offsets don't fit this block's current text
}

// Rollout step 4: showing a highlight, once one exists. A selection
// rarely sits inside a single text node — it can span an <em>, a
// <code>, or just a sentence break — and
// `Range.surroundContents()` throws in exactly that case, on any node it
// can't safely wrap whole. The fix used here is the standard one: walk the
// range's own text nodes and wrap each one's selected portion in its own
// <mark>, rather than asking for one <mark> around the whole range.
// Several <mark>s sharing one `data-highlight-id` is normal, not a bug.
// `color` is one of HIGHLIGHT_COLORS, or omitted for the CSS default
// (amber) -- an un-migrated highlight saved before colour existed.
function wrapRange(range, highlightId, color) {
  const doc = range.startContainer.ownerDocument || document;
  const root = range.commonAncestorContainer;
  const walker = doc.createTreeWalker(
    root.nodeType === Node.TEXT_NODE ? root.parentNode : root,
    NodeFilter.SHOW_TEXT,
  );

  const marks = [];
  let node = walker.nextNode();
  while (node) {
    // Taken before any splitText() below, since splitting inserts a new
    // sibling text node the walker would otherwise visit next — one this
    // range's own end offset has already excluded from it.
    const next = walker.nextNode();
    if (range.intersectsNode(node)) {
      const start = node === range.startContainer ? range.startOffset : 0;
      const end = node === range.endContainer ? range.endOffset : node.length;
      if (start < end) {
        let target = node;
        if (end < target.length) target.splitText(end);
        if (start > 0) target = target.splitText(start);
        const mark = doc.createElement("mark");
        mark.className = "dl-highlight";
        mark.dataset.highlightId = highlightId;
        if (color && color !== DEFAULT_HIGHLIGHT_COLOR) mark.dataset.highlightColor = color;
        // Only the first fragment is a tab stop — several <mark>s can share
        // one highlight id, and a reader tabbing through the page should
        // meet that highlight once, not once per fragment it happens to be
        // split across.
        mark.tabIndex = marks.length === 0 ? 0 : -1;
        target.parentNode.insertBefore(mark, target);
        mark.appendChild(target);
        marks.push(mark);
      }
    }
    node = next;
  }
  return marks;
}

// Recolouring an existing highlight from the popover's swatch row --
// every <mark> sharing this id, since one highlight can be split across
// several when its range crosses a child element (wrapRange()'s own
// comment above explains why more than one is normal).
function recolorHighlight(highlightId, color, root = document.getElementById("dl-body")) {
  const marks = root
    ? root.querySelectorAll(`mark.dl-highlight[data-highlight-id="${CSS.escape(highlightId)}"]`)
    : [];
  for (const mark of marks) {
    if (color && color !== DEFAULT_HIGHLIGHT_COLOR) mark.dataset.highlightColor = color;
    else delete mark.dataset.highlightColor;
  }
}

// The other half: strip a highlight back out, restoring plain text nodes
// (never the surrounding prose itself — only the <mark> wrapper). Adjacent
// text nodes left behind by an earlier wrapRange() split are merged back
// with normalize(), so repeated highlight/unhighlight cycles on the same
// passage don't leave the DOM more fragmented each time.
function unwrapHighlight(highlightId, root = document.getElementById("dl-body")) {
  const marks = root ? Array.from(
    root.querySelectorAll(`mark.dl-highlight[data-highlight-id="${CSS.escape(highlightId)}"]`),
  ) : [];
  const parents = new Set();
  for (const mark of marks) {
    const parent = mark.parentNode;
    while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
    parent.removeChild(mark);
    parents.add(parent);
  }
  for (const parent of parents) parent.normalize();
  return marks.length;
}

// Rollout step 5: actually making one. A highlight anchors to exactly
// one prose block — the same block a reader's selection has to sit
// inside, checked here rather than assumed, since a selection can
// freely cross into a heading or a second paragraph and this is where
// that gets caught, silently, the same way Look Up already stays
// silent for a selection that isn't a term.
function blockFor(node) {
  const el = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
  return el ? el.closest(PROSE_BLOCK_SELECTOR) : null;
}

// The [start, end) offsets rangeForOffsets() would need to rebuild this
// exact range later, read off a *live* selection instead of computed by
// hand — a range from the start of `block` to the selection's own start
// is, stringified, exactly the text before it; the standard trick for
// "where is this selection, as plain character offsets."
function offsetsForRange(block, range) {
  const pre = document.createRange();
  pre.selectNodeContents(block);
  pre.setEnd(range.startContainer, range.startOffset);
  const start = pre.toString().length;
  return { start, end: start + range.toString().length };
}

function generateHighlightId() {
  return `h-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

// The colour a fresh highlight starts in: whichever a reader picked most
// recently, on this device, across every tutorial — not per-page, since a
// reader who settled on "amber means important" wants that to hold
// everywhere, not reset each time they open a new tutorial.
function readLastHighlightColor() {
  try {
    const stored = localStorage.getItem(HIGHLIGHT_COLOR_KEY);
    return HIGHLIGHT_COLORS.includes(stored) ? stored : DEFAULT_HIGHLIGHT_COLOR;
  } catch (err) {
    return DEFAULT_HIGHLIGHT_COLOR;
  }
}

function writeLastHighlightColor(color) {
  try {
    localStorage.setItem(HIGHLIGHT_COLOR_KEY, color);
  } catch (err) {
    /* This reader's own choice only; forgotten after it, same as the rest
     * of this file's storage refusal shape. */
  }
}

// Ties (2), (3) and (4) together: anchor the live selection, save it, show
// it. `range` is still the reader's own selection Range, not yet a
// reconstructed one — wrapRange() needs exactly that, and reconstructing
// it from offsets first would be reading back something already in hand.
function createHighlight(range, block, note = "") {
  const { start, end } = offsetsForRange(block, range);
  const color = readLastHighlightColor();
  const highlight = {
    id: generateHighlightId(),
    block_index: proseBlocks().indexOf(block),
    ...describeQuote(block, start, end),
    note,
    color,
    created_at: new Date().toISOString(),
  };
  highlights.push(highlight);
  wrapRange(range, highlight.id, color);
  scheduleSave();
  refreshHighlightsList();
  return highlight;
}

function initReferenceLookup(manifest) {
  const body = document.getElementById("dl-body");
  const panel = document.getElementById("dl-reference");
  const toggle = document.getElementById("dl-reference-toggle");
  if (!body) return;

  // manifest.glossary is a flat list of entries, the same one
  // renderReference() groups by kind for display. A tutorial with none —
  // termFor() below then never matches anything — still gets the
  // Highlight button; it is not the same feature as REFERENCE_PANEL.md
  // §6b's Look Up, and needs no glossary to work.
  const terms = (manifest.glossary || [])
    .map((entry) => String(entry.term || "").toLowerCase())
    .filter(Boolean);

  // A selection worth offering a lookup for: long enough not to be a stray
  // character, short enough to be a term rather than a dragged paragraph.
  // Highlighting only needs the lower bound — a whole sentence, even a
  // whole paragraph, is an ordinary thing to mark, so there's no upper
  // one; the one-block constraint below is what actually limits it.
  const SHORTEST = 2;
  const LONGEST = 40;

  const lookupButton = document.createElement("button");
  lookupButton.type = "button";
  lookupButton.className = "dl-lookup";
  lookupButton.hidden = true;
  document.body.append(lookupButton);

  // Rollout step 5 — "Add a note" joins this once step 6's edit/remove
  // popover exists to open; for now, Highlight is the only new button,
  // and a note is added afterward by clicking the highlight it made.
  const highlightButton = document.createElement("button");
  highlightButton.type = "button";
  // Its own class, not shared with .dl-lookup: test_reference.py already
  // asserts against `.dl-lookup` specifically, and two buttons answering
  // to the same selector would make those assertions ambiguous. The CSS
  // rule below still styles both the same way, by listing both selectors.
  highlightButton.className = "dl-highlight-btn";
  highlightButton.textContent = "Highlight";
  highlightButton.hidden = true;
  document.body.append(highlightButton);

  function hide() {
    lookupButton.hidden = true;
    highlightButton.hidden = true;
  }

  // Both buttons are independently `position: fixed`, not one toolbar with
  // a shared hidden wrapper — test_reference.py already asserts `.dl-lookup`
  // itself carries `hidden`, and a wrapper would mean that attribute alone
  // no longer says whether the button is actually visible.
  function layout(rect, buttons) {
    const margin = 8;
    const gap = 6;
    const width = buttons.reduce((sum, b) => sum + b.offsetWidth, 0) + gap * (buttons.length - 1);
    const height = Math.max(...buttons.map((b) => b.offsetHeight));
    const left = Math.max(margin, Math.min(rect.left, window.innerWidth - width - margin));
    const below = rect.bottom + 6;
    const top = below + height + margin > window.innerHeight
      ? Math.max(margin, rect.top - height - 6)   // above the selection instead
      : below;
    let x = left;
    for (const b of buttons) {
      b.style.left = `${x}px`;
      b.style.top = `${top}px`;
      x += b.offsetWidth + gap;
    }
  }

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
    const literal = terms.find((term) => bounded.test(term))
      || terms.find((term) => whole(term).test(needle));
    if (literal) return literal;

    // Then the same stemming and synonym rule every search box on the
    // site already uses (search-words.js): a reader who selects
    // "gradients" or "iterating" meets the entry for "gradient" or
    // "iteration" the same way typing either word into a search box
    // would. Token-for-token, in order, so a two-word selection needs a
    // two-word term rather than matching half a phrase.
    const needleTokens = tokenize(needle);
    if (needleTokens.length === 0) return null;
    return terms.find((term) => {
      const termTokens = tokenize(term);
      return termTokens.length === needleTokens.length
        && termTokens.every((token, i) =>
          tokenHits(token, needleTokens[i]) || tokenHits(needleTokens[i], token));
    }) || null;
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

    const range = selection.getRangeAt(0);
    const text = selection.toString();
    const term = termFor(text);

    // A highlight anchors to one prose block (§3) — checked here against
    // the selection's own two ends, not assumed, since a drag can freely
    // leave the block it started in.
    const startBlock = blockFor(range.startContainer);
    const endBlock = blockFor(range.endContainer);
    const highlightable = text.trim().length >= SHORTEST
      && startBlock && startBlock === endBlock ? startBlock : null;

    if (!term && !highlightable) { hide(); return; }

    const rect = range.getBoundingClientRect();
    if (!rect.width && !rect.height) { hide(); return; }

    // A selection can be off-screen — restored by the browser on load, or
    // left behind by a scroll. Placing a button at its coordinates would put
    // the button off-screen too, where it is unreachable but still focusable
    // by keyboard. Nothing to offer for a selection nobody can see.
    const withinViewport = rect.bottom > 0 && rect.top < window.innerHeight;
    if (!withinViewport) { hide(); return; }

    lookupButton.hidden = !term;
    if (term) {
      lookupButton.textContent = `Look up "${term}"`;
      lookupButton.dataset.term = term;
    }
    // The block itself isn't stashed anywhere -- highlightButton's own
    // click handler re-reads the live selection, the same way this
    // handler just did, rather than trusting a reference that could be
    // stale by the time a click actually lands.
    highlightButton.hidden = !highlightable;

    // Positioned against the viewport, so both buttons are fixed rather
    // than absolutely placed — no need to account for the page's own
    // scroll, and a scroll simply dismisses them. Measured after
    // unhiding, since a hidden element has no width to clamp against.
    layout(rect, [lookupButton, highlightButton].filter((b) => !b.hidden));
  });

  lookupButton.addEventListener("mousedown", (ev) => {
    // Before the click, or the selection is gone by the time we read it.
    ev.preventDefault();
  });

  lookupButton.addEventListener("click", () => {
    const term = lookupButton.dataset.term || "";
    // Let the selection go. The reader has what they asked for, and keeping
    // it would leave this button offering the same lookup a second time —
    // the mousedown above deliberately preserved the selection long enough
    // to read the term off it, and this is where that ends.
    const selection = document.getSelection();
    if (selection) selection.removeAllRanges();
    hide();
    panel.removeAttribute("hidden");
    toggle.setAttribute("aria-expanded", "true");
    // The value goes in whether or not the box is visible. renderReference()
    // hides it on a page with only a handful of entries, and the observer in
    // initReference() clears the filter on close by reading this value — so
    // skipping it there left such a page filtered to one term the next time
    // it opened, with no visible box to clear.
    const searchInput = document.getElementById("dl-reference-search");
    if (searchInput) searchInput.value = term;
    filterReferenceContent(term);
  });

  highlightButton.addEventListener("mousedown", (ev) => {
    // Before the click, same reason as lookupButton's own — the selection
    // (and the block/range it sits in) has to survive long enough to act on.
    ev.preventDefault();
  });

  highlightButton.addEventListener("click", () => {
    const selection = document.getSelection();
    if (!selection || selection.isCollapsed) { hide(); return; }
    const range = selection.getRangeAt(0);
    const startBlock = blockFor(range.startContainer);
    const endBlock = blockFor(range.endContainer);
    if (!startBlock || startBlock !== endBlock) { hide(); return; }

    createHighlight(range, startBlock);
    selection.removeAllRanges();
    hide();
  });

  document.addEventListener("scroll", hide, { passive: true });
}

// Rollout step 6: editing or removing a highlight that already exists —
// clicking anywhere on it (or reaching it with Tab, per wrapRange()'s
// first-fragment tab stop) opens a small popover: the note, if any,
// plus Save and Remove. One shared popover element, not one per
// highlight, the same "reused, not per-item" shape
// initReferenceLookup()'s own button already uses.
function initHighlightPopover() {
  const body = document.getElementById("dl-body");
  if (!body) return;

  const popover = document.createElement("div");
  popover.className = "dl-highlight-popover";
  popover.hidden = true;
  popover.setAttribute("role", "dialog");
  popover.setAttribute("aria-label", "Highlight");

  // One radiogroup button per HIGHLIGHT_COLORS entry, filled with the
  // colour it sets via the same [data-highlight-color] CSS the mark
  // itself uses -- so this row never drifts from what a highlight can
  // actually look like.
  const colors = document.createElement("div");
  colors.className = "dl-highlight-popover-colors";
  colors.setAttribute("role", "radiogroup");
  colors.setAttribute("aria-label", "Highlight colour");
  const colorButtons = HIGHLIGHT_COLORS.map((color) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "dl-highlight-popover-color";
    btn.dataset.color = color;
    if (color !== DEFAULT_HIGHLIGHT_COLOR) btn.dataset.highlightColor = color;
    btn.setAttribute("role", "radio");
    btn.setAttribute("aria-checked", "false");
    btn.setAttribute("aria-label", color);
    colors.append(btn);
    return btn;
  });

  const note = document.createElement("textarea");
  note.className = "dl-highlight-popover-note";
  note.placeholder = "Add a note (optional)";
  note.rows = 3;

  const actions = document.createElement("div");
  actions.className = "dl-highlight-popover-actions";

  const saveButton = document.createElement("button");
  saveButton.type = "button";
  saveButton.className = "dl-highlight-popover-save";
  saveButton.textContent = "Save";

  const removeButton = document.createElement("button");
  removeButton.type = "button";
  removeButton.className = "dl-highlight-popover-remove";
  removeButton.textContent = "Remove highlight";

  actions.append(saveButton, removeButton);
  popover.append(colors, note, actions);
  document.body.append(popover);

  let openId = null;

  function close() {
    popover.hidden = true;
    openId = null;
  }

  function open(id, rect) {
    const highlight = highlights.find((h) => h.id === id);
    if (!highlight) return;
    openId = id;
    note.value = highlight.note || "";
    const current = highlight.color || DEFAULT_HIGHLIGHT_COLOR;
    for (const btn of colorButtons) {
      btn.setAttribute("aria-checked", String(btn.dataset.color === current));
    }
    popover.hidden = false;

    // Same fixed-position, viewport-clamped placement initReferenceLookup()'s
    // own buttons already use, against the clicked mark's rect instead of a
    // selection's.
    const margin = 8;
    const width = popover.offsetWidth;
    const height = popover.offsetHeight;
    const left = Math.max(margin, Math.min(rect.left, window.innerWidth - width - margin));
    const below = rect.bottom + 6;
    const top = below + height + margin > window.innerHeight
      ? Math.max(margin, rect.top - height - 6)
      : below;
    popover.style.left = `${left}px`;
    popover.style.top = `${top}px`;
    note.focus();
  }

  function markFor(target) {
    return target.closest && target.closest("mark.dl-highlight");
  }

  body.addEventListener("click", (ev) => {
    const mark = markFor(ev.target);
    if (mark) open(mark.dataset.highlightId, mark.getBoundingClientRect());
  });

  body.addEventListener("keydown", (ev) => {
    if (ev.key !== "Enter" && ev.key !== " ") return;
    const mark = markFor(ev.target);
    if (!mark) return;
    ev.preventDefault();
    open(mark.dataset.highlightId, mark.getBoundingClientRect());
  });

  // Recolouring commits immediately, the same way every other segmented
  // control in Settings does — unlike the note textarea, which still
  // waits for Save, since a colour is a single click and a note is
  // something a reader might still be typing.
  for (const btn of colorButtons) {
    btn.addEventListener("click", () => {
      const highlight = highlights.find((h) => h.id === openId);
      if (!highlight) return;
      highlight.color = btn.dataset.color;
      for (const other of colorButtons) {
        other.setAttribute("aria-checked", String(other === btn));
      }
      recolorHighlight(openId, highlight.color, body);
      writeLastHighlightColor(highlight.color);
      scheduleSave();
      refreshHighlightsList();
    });
  }

  saveButton.addEventListener("click", () => {
    const highlight = highlights.find((h) => h.id === openId);
    if (highlight) {
      highlight.note = note.value;
      scheduleSave();
      refreshHighlightsList();
    }
    close();
  });

  removeButton.addEventListener("click", () => {
    const highlight = highlights.find((h) => h.id === openId);
    // A plain highlight costs nothing to remake — select the text again.
    // One with a note is asking to lose something a reader actually wrote,
    // the same reasoning that put a confirmation on Clear rather than
    // Reset for a cell's own code.
    if (highlight && highlight.note && !confirm("Remove this highlight and its note?")) {
      return;
    }
    unwrapHighlight(openId, body);
    const index = highlights.findIndex((h) => h.id === openId);
    if (index !== -1) highlights.splice(index, 1);
    scheduleSave();
    refreshHighlightsList();
    close();
  });

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || popover.hidden) return;
    close();
  });

  document.addEventListener("click", (ev) => {
    // The click that opened the popover also reaches here, bubbled up from
    // `body`'s own listener above — closing on it would undo the open this
    // same click just caused, so a click landing on a highlight (opening
    // this one, or switching to a different one) is not an "outside" click.
    if (popover.hidden || popover.contains(ev.target) || markFor(ev.target)) return;
    close();
  });

  document.addEventListener("scroll", close, { passive: true });
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

  const panel = document.getElementById("dl-settings-pane-appearance");
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
const appCells = [];

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
    const clearBtn = host.querySelector(".dl-btn-clear");
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
       * every run and reported back as `reached`. */
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
        outputEl.replaceChildren();
        delete cell.lastRunMs;
        delete cell.ranContent;
        delete cell.ranOrder;
        renderCellRunLine(cell);
      });
    }
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        if (!confirm("Put this cell's starter code back? Your own changes to it will be lost.")) return;
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

/* Every ```question fence on the page —
 * one entry per `.dl-question` the build wrote, read straight off the
 * DOM rather than the manifest: unlike a cell, nothing about a question
 * needs restoring beyond what saveNow()/restoreSaved() already carry
 * for it (the reader's own selection or typed words), so there is
 * nothing here a manifest entry would tell the runtime that the markup
 * does not already say.
 */
const questions = [];

/* Fisher-Yates, in place. Shared by a multiple-choice question's own
 * option buttons and a fill-in-the-blank gap's own <option> elements —
 * both are "show these DOM nodes in a different order," and the node
 * doing the moving carries its own correctness with it either way
 * (data-correct, data-expected), so shuffling never has to touch which
 * one is right. */
function shuffle(list) {
  for (let i = list.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [list[i], list[j]] = [list[j], list[i]];
  }
  return list;
}

/* The one feedback message every question shows, right or not —
 * .dl-check/.dl-check-pass/.dl-check-fail are check()'s own classes
 * (tutorial_tools.py's _check_html), reused rather than duplicated so a
 * question reads as the same kind of thing a reader already met inside
 * a cell, not a second feature with its own voice. */
function renderQuestionFeedback(question, passed) {
  const css = passed ? "dl-check-pass" : "dl-check-fail";
  const mark = passed ? "✓" : "✗";
  const heading = passed ? "That’s right." : "Not quite yet.";
  question.feedbackEl.hidden = false;
  question.feedbackEl.innerHTML =
    `<div class="dl-check ${css}"><span class="dl-check-mark">${mark}</span><span>${heading}</span></div>`;
}

/* A fill-in-the-blank gap is correct when a select's chosen <option>
 * carries data-correct, or a typing box's trimmed value matches the
 * word the build wrote onto it (data-expected) — case-sensitive and
 * exact, the same as check()'s own fallback comparison for anything
 * that is not a number, an array or a table. */
function gapIsCorrect(gap) {
  if (gap.tagName === "SELECT") {
    const chosen = gap.options[gap.selectedIndex];
    return !!chosen && chosen.dataset.correct === "true";
  }
  return gap.value.trim() === gap.dataset.expected;
}

/* The pass/fail computation and its redraw, with no side effect beyond
 * the DOM — shared by a live Check click (checkQuestion(), below, which
 * also records that this question has now been checked and saves) and
 * restoreSaved() (which is redrawing a check the reader already made,
 * not making a new one, and has no reason to schedule another save
 * moments after the record it just read back in). */
function evaluateQuestion(question) {
  let passed;
  if (question.type === "multiple-choice") {
    const selected = question.options.find((option) => option.classList.contains("is-selected"));
    if (!selected) return;
    passed = selected.dataset.correct === "true";
  } else {
    passed = true;
    for (const gap of question.gaps) {
      const correct = gapIsCorrect(gap);
      gap.classList.toggle("is-correct", correct);
      gap.classList.toggle("is-incorrect", !correct);
      if (!correct) passed = false;
    }
  }
  renderQuestionFeedback(question, passed);
}

function checkQuestion(question) {
  evaluateQuestion(question);
  question.checked = true;
  scheduleSave();
}

function buildQuestions() {
  for (const host of document.querySelectorAll(".dl-question")) {
    const id = host.dataset.questionId;
    const type = host.dataset.questionType;
    const checkBtn = host.querySelector(".dl-question-check");
    const feedbackEl = host.querySelector(".dl-question-feedback");
    const question = { id, type, element: host, checkBtn, feedbackEl, checked: false };

    if (type === "multiple-choice") {
      const options = shuffle([...host.querySelectorAll(".dl-question-option")]);
      const optionsHost = host.querySelector(".dl-question-options");
      for (const option of options) optionsHost.appendChild(option);
      question.options = options;
      for (const option of options) {
        option.addEventListener("click", () => {
          for (const other of options) other.classList.remove("is-selected");
          option.classList.add("is-selected");
          checkBtn.disabled = false;
          scheduleSave();
        });
      }
    } else {
      question.gaps = [...host.querySelectorAll(".dl-question-gap-select, .dl-question-gap-input")];
      for (const gap of question.gaps) {
        if (gap.tagName === "SELECT") shuffle([...gap.options]).forEach((opt) => gap.appendChild(opt));
        gap.addEventListener(gap.tagName === "SELECT" ? "change" : "input", () => scheduleSave());
      }
      checkBtn.disabled = false;
    }

    checkBtn.addEventListener("click", () => checkQuestion(question));
    questions.push(question);
  }
}

/* A slider that sets a diagram's own width.
 *
 * For a diagram whose subject is what happens *at* a width — a grid that
 * redraws past a breakpoint, a row that wraps. A container query on the
 * sized element does the rest, which is the honest shape of the thing
 * being taught: the width decides, not the control.
 *
 * Generic rather than per-diagram: an `<input type="range">` carrying
 * `data-dl-width-for="<id>"` sizes that element in pixels and writes the
 * figure into the `<output>` beside it. Pixels, not percent, because the
 * breakpoint a diagram like this exists to show is written in pixels.
 *
 * The control ships `hidden` and this reveals it, so a reader whose
 * JavaScript never runs is not left with a slider that does nothing. They
 * see the diagram at its starting width and the prose underneath, which is
 * what a drawn figure would have given them.
 *
 * This lives in the runtime rather than in a script beside the diagram so
 * that it reaches a downloaded page: build.py inlines the standalone
 * bundle into every one, and nothing here waits on a Run button. */
function wireDiagramWidthSliders() {
  for (const input of document.querySelectorAll("input[data-dl-width-for]")) {
    const target = document.getElementById(input.dataset.dlWidthFor);
    if (!target) {
      console.warn(`dewlab: width slider points at "${input.dataset.dlWidthFor}", which is not on the page`);
      continue;
    }
    const out = input.parentElement && input.parentElement.querySelector("output");
    const apply = () => {
      target.style.width = `${input.value}px`;
      if (out) out.textContent = `${input.value}px`;
    };
    input.addEventListener("input", apply);
    apply();
    if (input.parentElement) input.parentElement.hidden = false;
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
    const clearBtn = host.querySelector(".dl-btn-site-clear");
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
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        if (!confirm("Put this editor's starter code back, in every pane? Your own changes will be lost.")) return;
        for (const pane of Object.values(panes)) pane.editor.setValue(pane.starter);
        editorState.ran = false;
        render();
        scheduleSave();
      });
    }

    /* The readout carries the preview's width in pixels beside the
     * percentage, because a layout tutorial's question is nearly always
     * *at what width* — the row wraps, the media query turns on — and a
     * percentage of a column whose own width depends on the reader's font
     * and window answers none of it. Measured from the frame rather than
     * computed from the percentage, so it stays true when the column
     * itself changes: a window resize, the reference panel opening, a
     * different font size. Rounded, since a fractional pixel is noise to
     * anybody reading it.
     *
     * The frame is sandboxed without allow-same-origin, so this is the
     * frame's own width and not the width inside it. The two differ by
     * whatever margin the previewed page's body carries — a tutorial that
     * wants the two to agree sets `body { margin: 0 }` in its own CSS,
     * which flexbox-first-steps does. */
    const widthInput = host.querySelector(".dl-site-width");
    const widthOut = host.querySelector(".dl-site-preview-controls output");

    /* One write and one measurement per animation frame, however fast the
     * drag. Setting the frame's width and then immediately reading it back
     * forces a synchronous layout inside the event handler, and a drag
     * fires `input` far faster than the page can paint — which left the
     * frame's old content smeared across the space it had just vacated,
     * on every site editor on the site. Coalescing into a frame fixes the
     * cause rather than the symptom: the value the reader lands on is
     * still exactly the one under their thumb. */
    let pending = null;
    let frame = 0;
    const showWidth = () => {
      if (!widthOut || !widthInput) return;
      const px = Math.round(iframe.getBoundingClientRect().width);
      const text = px ? `${widthInput.value}% · ${px}px` : `${widthInput.value}%`;
      // Never write the same text twice: a no-op mutation here still costs
      // the style and layout work that a ResizeObserver callback can then
      // notice again.
      if (widthOut.textContent !== text) widthOut.textContent = text;
    };
    const apply = () => {
      frame = 0;
      if (pending !== null) {
        iframe.style.width = `${pending}%`;
        pending = null;
      }
      showWidth();
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(apply);
    };

    if (widthInput) {
      widthInput.addEventListener("input", () => {
        pending = widthInput.value;
        schedule();
      });
      showWidth();
      // Keeps the figure true when the column moves underneath it — a
      // window resize, a panel opening — not only when the slider moves.
      if (typeof ResizeObserver === "function") {
        new ResizeObserver(schedule).observe(iframe);
      }
    }

    siteEditors.push(editorState);
    render();
  }
}

/* The full-stack module's own cell kind. Shares most of
 * buildSiteEditors()'s own shape — panes,
 * a head-level Clear, a per-pane Run button on the JS pane, HTML/CSS
 * live without pressing Run — but the result area is not an iframe:
 * HTML and CSS render straight into a plain `.dl-app-preview` div, CSS
 * scoped to it with the `@scope` at-rule rather than an iframe
 * boundary, and the JS pane's code runs as a real `<script>` element
 * appended to the page, wrapped so `root` (this cell's own preview
 * element) and `dlQuery` (queryRows()/queryRowsMT() below) reach it as
 * plain parameters, nothing added to the page's own global scope. That
 * is the one deliberate difference from a site editor, and it is the
 * whole reason this is a separate cell kind rather than a third `site`
 * pane language: a full-stack cell's JavaScript has to reach the page's
 * own shared SQL connection, and the site editor's sandbox exists
 * specifically to stop a reader's script doing exactly that. */
function buildAppCells(manifest) {
  const dark = isDarkNow();
  const labelFor = { html: "html", css: "css", js: "javascript" };

  for (const spec of manifest.appCells || []) {
    const host = document.querySelector(`.dl-app-cell[data-app-name="${CSS.escape(spec.name)}"]`);
    if (!host) {
      console.warn(`dewlab: manifest lists full-stack cell "${spec.name}" but the page has no such element`);
      continue;
    }
    const preview = host.querySelector(".dl-app-preview");
    const errorBox = host.querySelector(".dl-app-error");
    const clearBtn = host.querySelector(".dl-btn-app-clear");
    const runBtn = host.querySelector(".dl-btn-app-run");

    const panes = {};
    for (const [lang, paneSpec] of Object.entries(spec.panes || {})) {
      const paneHost = host.querySelector(`.dl-app-pane[data-lang="${lang}"] .dl-editor`);
      if (!paneHost) continue;
      const editor = createCodeEditor(paneHost, paneSpec.code || "", {
        dark,
        language: labelFor[lang] || lang,
        onChange: () => { scheduleSave(); if (lang !== "js") renderPreview(); },
        lineNumbersVisible: loadTexture().linenumbers !== "off",
        indentWidth: loadTexture().indent,
      });
      panes[lang] = { id: paneSpec.id, starter: paneSpec.code || "", editor };
    }

    const code = (lang) => (panes[lang] ? panes[lang].editor.getValue() : "");

    let styleEl = null;
    const renderPreview = () => {
      preview.innerHTML = code("html");
      const css = code("css");
      if (!css) {
        if (styleEl) { styleEl.remove(); styleEl = null; }
        return;
      }
      if (!styleEl) {
        styleEl = document.createElement("style");
        styleEl.className = "dl-app-style";
        host.appendChild(styleEl);
      }
      styleEl.textContent = `@scope (#${preview.id}) {\n${css}\n}`;
    };

    const cellState = { name: spec.name, panes, ran: false };
    const run = async () => {
      if (runBtn) runBtn.disabled = true;
      errorBox.textContent = "";
      try {
        await ensureBooted(currentManifest);
        renderPreview();
        const old = host.querySelector(".dl-app-script");
        if (old) old.remove();
        const script = document.createElement("script");
        script.className = "dl-app-script";
        script.textContent =
          `(async function (root, dlQuery) {\n${code("js")}\n})` +
          `(document.getElementById(${JSON.stringify(preview.id)}), window.dewlabQueryRows)` +
          `.catch((err) => { document.getElementById(${JSON.stringify(errorBox.id)}).textContent = String(err); });`;
        host.appendChild(script);
        cellState.ran = true;
        scheduleSave();
      } catch (err) {
        errorBox.textContent = String(err);
      } finally {
        if (runBtn) runBtn.disabled = false;
      }
    };
    cellState.render = renderPreview;
    cellState.run = run;

    if (runBtn) {
      runBtn.addEventListener("mousedown", (e) => e.preventDefault());
      runBtn.addEventListener("click", run);
    }
    if (panes.js) {
      host.querySelector('.dl-app-pane[data-lang="js"]').addEventListener("keydown", (ev) => {
        if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
          ev.preventDefault();
          ev.stopPropagation();
          run();
        }
      }, true);
    }
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        if (!confirm("Put this cell's starter code back, in every pane? Your own changes will be lost.")) return;
        for (const pane of Object.values(panes)) pane.editor.setValue(pane.starter);
        preview.innerHTML = "";
        errorBox.textContent = "";
        if (styleEl) { styleEl.remove(); styleEl = null; }
        const old = host.querySelector(".dl-app-script");
        if (old) old.remove();
        cellState.ran = false;
        scheduleSave();
      });
    }

    appCells.push(cellState);
    renderPreview();
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

/* Every key this page saves under: `dewlab:<kind>:<id>`. The id is the
 * tutorial's folder name, site-wide, so nothing else is needed to tell two
 * pages apart. (Before courses/ existed the keys carried module:slug —
 * migrateStorage() renames those on the first visit after the change.) */
function pageKey(prefix) {
  const manifest = currentManifest || {};
  return `${prefix}${manifest.id || manifest.slug || "unknown"}`;
}

function customCellsKey() {
  return pageKey(CUSTOM_CELLS_PREFIX);
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
  const from = manifest.id || manifest.slug || "";
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
  const from = manifest.id || manifest.slug || "";
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

/* The main-thread twin of pyodide-worker.js's own describeGlobals() —
 * same call, same proxy handling, run directly rather than crossing a
 * worker boundary that doesn't exist in this mode. */
function describeGlobalsMT() {
  if (!toolsMT) return [];
  try {
    const proxy = toolsMT.describe_globals();
    const described = proxy.toJs({ dict_converter: Object.fromEntries });
    proxy.destroy();
    return described;
  } catch {
    return [];
  }
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

/* The main-thread half of queryRows() below — the standalone export's
 * own path, the same fork every other dual-path call in this file
 * makes on `currentManifest.standalone`. */
function queryRowsMT(sql, params) {
  const proxy = toolsMT._query_rows(sql, params || []);
  const rows = proxy.toJs({ dict_converter: Object.fromEntries });
  proxy.destroy();
  return rows;
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

/* A widget rendered by Worker-run Python has no way to report itself back:
 * `_MessageSink.append_html()` returns None, so the Python side holds no
 * element reference and can attach no listener. The page holds the element
 * instead, and posts one message per change into the same dict `.value`
 * reads. The value arrives between runs rather than during one, which is
 * exactly the interaction a cell already has: type, press Run, read it. */
function wireWorkerWidget(cellId, widget) {
  const control = widget.querySelector("input, select");
  if (!control) return;
  /* The DOM id is `dl-w-<cellId>-<widgetId>`, and the cell id is known here,
   * so the widget id is whatever follows that prefix — ids of both kinds are
   * lowercase and hyphenated, and a widget id may hold hyphens of its own. */
  const prefix = `dl-w-${cellId}-`;
  if (!control.id.startsWith(prefix)) return;
  const widgetId = control.id.slice(prefix.length);
  control.addEventListener("input", () => {
    workerRequest("widget-changed", { cellId, widgetId, value: control.value });
  });
}

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
    const added = [...template.content.querySelectorAll(".dl-widget")];
    el.appendChild(template.content);
    added.forEach((widget) => wireWorkerWidget(cellId, widget));
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

/* An app cell's own bridge to the page's shared `db` — `dewlabQueryRows`
 * on `globalThis`, closed over by name as `dlQuery` inside the wrapper
 * buildAppCells() injects, never a name a reader's own code could
 * collide with on the page itself. */
async function queryRows(sql, params) {
  await ensureBooted(currentManifest);
  return currentManifest.standalone
    ? queryRowsMT(sql, params)
    : workerRequest("query-rows", { sql, params: params || [] });
}

/* What's currently in the shared namespace — the Python panel's own
 * Variables/Functions/Packages (refreshPythonState() below), each a
 * {name, type, summary, kind} entry from describe_globals()
 * (tutorial_tools.py). Not gated on ensureBooted(): called before Python
 * has ever run, when there is nothing to describe yet, and booting it
 * just to say so would be the wrong side effect for opening a panel. */
async function describeGlobalsForPanel() {
  if (!pyodideReady) return [];
  return currentManifest.standalone
    ? describeGlobalsMT()
    : worker
      ? await workerRequest("describe-globals", {})
      : [];
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
    emptyResults: 0,  // consecutive runs where a SQL query came back with no rows
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
  a.emptyResults = report.empty === true ? a.emptyResults + 1 : 0;
}

function triggerHolds(terms, a) {
  const value = {
    "errors": a.errors,
    "same-errors": a.sameErrors,
    "unchanged": a.unchanged,
    "runs": a.runs,
    "check-fails": a.checkFails,
    "empty-results": a.emptyResults,
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
    if (completed) {
      announceCellRun(cell);
      refreshPythonState();
    }
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
  refreshPythonState();

  let ok = true;
  try {
    await ensureBooted(currentManifest);
    setStatus("Python restarted.", "ok");
  } catch (err) {
    ok = false;
  }
  updateExecutionStatus();
  refreshPythonState();
  return ok;
}

function updateExecutionStatus() {
  const el = document.getElementById("dl-execution-status");
  if (!el) return;
  el.textContent = pyodideReady
    ? "Python is running."
    : "Not started yet — run a cell to start Python.";
}

/* One row of a describe_globals() entry (tutorial_tools.py) — name, type,
 * and a value summary already length-limited on the Python side, so
 * nothing here needs its own truncation beyond the CSS ellipsis. */
function renderVariableRow(entry) {
  const row = document.createElement("div");
  row.className = "dl-variable-row";

  const name = document.createElement("span");
  name.className = "dl-variable-name";
  name.textContent = entry.name;

  const type = document.createElement("span");
  type.className = "dl-variable-type";
  type.textContent = entry.type;

  const summary = document.createElement("span");
  summary.className = "dl-variable-summary";
  summary.textContent = entry.summary;

  row.append(name, type, summary);
  return row;
}

/* One row of the Notes panel's own "Your highlights" list — the quoted
 * passage, the reader's own note if they left one, and a colour dot
 * standing in for Variables' type column above. The whole row is a
 * button, not a link: clicking it scrolls to and opens the highlight in
 * the page itself, rather than navigating anywhere. */
function renderHighlightRow(highlight) {
  const row = document.createElement("button");
  row.type = "button";
  row.className = "dl-highlight-row";

  const dot = document.createElement("span");
  dot.className = "dl-highlight-dot";
  dot.setAttribute("aria-hidden", "true");
  if (highlight.color && highlight.color !== DEFAULT_HIGHLIGHT_COLOR) {
    dot.dataset.highlightColor = highlight.color;
  }

  const text = document.createElement("span");
  text.className = "dl-highlight-text";

  const quote = document.createElement("span");
  quote.className = "dl-highlight-quote";
  quote.textContent = `"${highlight.quote}"`;
  text.append(quote);

  if (highlight.note) {
    const note = document.createElement("span");
    note.className = "dl-highlight-note";
    note.textContent = highlight.note;
    text.append(note);
  }

  row.append(dot, text);
  row.addEventListener("click", (ev) => {
    // jumpToHighlight() below opens the popover via a synthetic click on
    // the mark, synchronously, before this real click event finishes
    // bubbling to document -- where the popover's own outside-click
    // listener would otherwise see this original click land on neither
    // the popover nor a mark, and close right back what the synthetic
    // one just opened (the same fix initMobileLauncher() needed for its
    // own forwarded clicks, and for the same reason).
    ev.stopPropagation();
    jumpToHighlight(highlight.id);
  });
  return row;
}

// Scrolls a highlight into view and pulses it -- clicking a row in the
// Notes panel's own list also opens the popover (that click is deliberate
// upkeep, the reader chose it from a list of their own highlights), but
// arriving from another page's URL hash (below) is a reader visiting a
// passage to re-read it, not asking to edit it, so that path leaves
// `openPopover` false. Several <mark>s can share one id; only the first
// is a tab stop (wrapRange()'s own comment), so it's the one this scrolls
// to and, when asked, clicks.
function jumpToHighlight(highlightId, { openPopover = true } = {}) {
  const mark = document.querySelector(
    `mark.dl-highlight[data-highlight-id="${CSS.escape(highlightId)}"]`,
  );
  if (!mark) return;
  closeRightPanels();
  mark.scrollIntoView({ behavior: "smooth", block: "center" });
  mark.classList.remove("dl-highlight-flash");
  // Forces a reflow so re-adding the class restarts the animation, in
  // case a reader jumps to the same highlight twice in a row.
  void mark.offsetWidth;
  mark.classList.add("dl-highlight-flash");
  if (openPopover) mark.click();
  else mark.focus();
}

/* Every highlight on this page, live — refreshed on the same schedule
 * the note (highlight.note) and colour above are set on, plus whenever
 * the Notes panel opens (initRightPanels()'s own setOpen()). Empty state
 * doubles as the only place on the page that says highlighting exists at
 * all, since nothing about the selection toolbar itself hints at it. */
function refreshHighlightsList() {
  const list = document.getElementById("dl-highlights-list");
  const status = document.getElementById("dl-highlights-status");
  if (!list || !status) return;
  list.replaceChildren(...highlights.map(renderHighlightRow));
  status.hidden = highlights.length > 0;
}

/* Variables, Functions and Packages in the Python panel — describe_globals()
 * split by its own `kind`: data (Variables), callable (Functions, theirs
 * or a class they defined) and module (Packages, collapsed by default in
 * the markup since it's rarely what a reader opened this panel to check).
 * Called when the panel opens and after every cell run (runCell()), not
 * on a timer — a closed panel skips the round trip entirely. */
async function refreshPythonState() {
  const panel = document.getElementById("dl-python");
  if (!panel || panel.hasAttribute("hidden")) return;

  const lists = {
    data: document.getElementById("dl-variables-list"),
    callable: document.getElementById("dl-functions-list"),
    module: document.getElementById("dl-packages-list"),
  };
  const statuses = {
    data: [
      document.getElementById("dl-variables-status"),
      "Nothing defined yet — run a cell that makes one.",
    ],
    callable: [
      document.getElementById("dl-functions-status"),
      "Nothing declared yet — run a cell that declares one.",
    ],
    module: [
      document.getElementById("dl-packages-status"),
      "Nothing imported yet.",
    ],
  };
  if (!lists.data || !lists.callable || !lists.module) return;

  const notStarted = "Not started yet — run a cell to start Python.";
  const described = await describeGlobalsForPanel();
  for (const kind of ["data", "callable", "module"]) {
    // !entry.builtin drops the toolbox every page starts with (show,
    // check, button, … — tutorial_tools.__all__, reseeded at boot and
    // after every restart) so this reads as what a reader's own code
    // made, not the furniture it was always going to have either way.
    const entries = described.filter((entry) => entry.kind === kind && !entry.builtin);
    lists[kind].replaceChildren(...entries.map(renderVariableRow));
    const [statusEl, emptyMessage] = statuses[kind];
    if (!statusEl) continue;
    statusEl.hidden = entries.length > 0;
    statusEl.textContent = pyodideReady ? emptyMessage : notStarted;
  }
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

/* Highlights and margin notes: one entry per marked passage — {id,
 * block_index, quote, prefix, suffix, note, created_at}. `const`, like
 * `cells` above, and mutated in place
 * rather than reassigned, so a reference to it (globalThis.dewlab's own
 * included) stays valid across a restoreSaved() call. Nothing populates
 * it yet; the selection toolbar that will (rollout step 5) has the same
 * shape to fill in as any other caller, including a test. */
const highlights = [];

function progressKey() {
  return pageKey(PROGRESS_PREFIX);
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
  // A record names its page by id. One written before courses/ existed
  // names it by module and slug instead, and the manifest's `legacy` is
  // that pair for this page, so such a file still fits.
  const ident = record["tutorial-id"] || record["tutorial-slug"];
  const module = record["tutorial-module"];
  const legacy = module ? `${module}:${record["tutorial-slug"]}` : "";
  const here = (!module && ident === currentManifest.id)
    || (!!currentManifest.legacy && legacy === currentManifest.legacy)
    || (!currentManifest.legacy && ident === currentManifest.id);
  if (here) return "";
  const name = [module, ident].filter(Boolean).join(" / ") || "another tutorial";
  return `That file is saved work from ${name}, not this tutorial. `
    + "Nothing has been changed.";
}


function saveNow() {
  clearTimeout(saveTimer);
  saveTimer = null;
  if (NON_TUTORIAL_PAGES.has(currentManifest.slug)) return;
  const record = {
    "tutorial-id": currentManifest.id,
    "tutorial-slug": currentManifest.slug,
    "tutorial-version": currentManifest.version,
    saved_at: new Date().toISOString(),
    notes: notesEl ? notesEl.value : "",
    highlights: highlights.map((h) => ({ ...h })),
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
    questions: questions.map((question) => ({
      id: question.id,
      selected: question.type === "multiple-choice"
        ? (question.options.find((option) => option.classList.contains("is-selected"))?.dataset.option ?? null)
        : question.gaps.map((gap) => gap.value),
      checked: question.checked,
    })),
    // Same reasoning as a site editor's own record just above: cheap to
    // rebuild, so only each pane's current text and whether Run had
    // been pressed travel here, not the preview itself.
    appCells: appCells.map((cell) => ({
      name: cell.name,
      panes: Object.fromEntries(
        Object.entries(cell.panes).map(([lang, pane]) => [lang, pane.editor.getValue()]),
      ),
      ran: cell.ran,
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

  if (notesEl && typeof record.notes === "string") {
    notesEl.value = record.notes;
    autoGrowTextarea(notesEl);
  }

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

  const droppedHighlights = [];
  if (Array.isArray(record.highlights)) {
    highlights.length = 0;
    for (const saved of record.highlights) {
      const anchor = {
        block_index: saved.block_index, quote: saved.quote,
        prefix: saved.prefix, suffix: saved.suffix,
      };
      // Relocated now, at restore time, rather than lazily when something
      // later tries to render it — a highlight that can't be found is
      // dropped and reported here the same way a cell whose id disappeared
      // already is above, not discovered as a mystery gap later.
      const located = locateHighlightAnchor(anchor);
      if (located) {
        highlights.push({ ...saved });
        const range = rangeForOffsets(
          located.block, located.index, located.index + saved.quote.length,
        );
        if (range) wrapRange(range, saved.id, saved.color);
      } else {
        droppedHighlights.push(saved.id);
      }
    }
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

  if (Array.isArray(record.appCells)) {
    const byAppName = new Map(appCells.map((cell) => [cell.name, cell]));
    for (const saved of record.appCells) {
      const cell = byAppName.get(saved.name);
      if (!cell) continue;
      for (const [lang, code] of Object.entries(saved.panes || {})) {
        if (cell.panes[lang] && typeof code === "string") cell.panes[lang].editor.setValue(code);
      }
      // Same reasoning as a site editor's own restore, just above: only
      // re-run the JS pane if Run had actually been pressed before.
      if (saved.ran) cell.run(); else cell.render();
    }
  }

  if (Array.isArray(record.questions)) {
    const byQuestionId = new Map(questions.map((question) => [question.id, question]));
    for (const saved of record.questions) {
      const question = byQuestionId.get(saved.id);
      if (!question) continue;
      if (question.type === "multiple-choice") {
        if (saved.selected != null) {
          const option = question.options.find((o) => o.dataset.option === String(saved.selected));
          if (option) {
            option.classList.add("is-selected");
            question.checkBtn.disabled = false;
          }
        }
      } else if (Array.isArray(saved.selected)) {
        question.gaps.forEach((gap, index) => {
          if (typeof saved.selected[index] === "string") gap.value = saved.selected[index];
        });
      }
      // Recomputed, not merely redisplayed: a gap's own correctness can
      // only be read once its saved value is back in the control, and
      // this is also what redraws the pass/fail classes on each gap the
      // way they looked when the reader last pressed Check. evaluateQuestion(),
      // not checkQuestion() — this is redrawing a check already made, not
      // making a new one, and question.checked is set just below either way.
      if (saved.checked) {
        evaluateQuestion(question);
        question.checked = true;
      }
    }
  }

  return {
    restored,
    dropped,
    droppedHighlights,
    widgets,
    savedAt: record.saved_at,
    savedVersion: String(record["tutorial-version"]),
    versionChanged: String(record["tutorial-version"]) !== String(currentManifest.version),
  };
}

function announceRestore(summary) {
  if (!summary || (
    summary.restored.length === 0 && summary.dropped.length === 0
      && summary.droppedHighlights.length === 0
  )) return;

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
  if (summary.droppedHighlights.length) {
    // Unlike a dropped cell, this can happen with no version change at all —
    // a prose-only edit never bumps `tutorial-version`, so the wording here
    // can't lean on "this version does not have" the way
    // the cell message above does.
    const many = summary.droppedHighlights.length !== 1;
    lines.push(
      many
        ? `${summary.droppedHighlights.length} of your highlights were on text `
          + "that has since changed, so they could not be put back."
        : "One of your highlights was on text that has since changed, so it "
          + "could not be put back."
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
  return pageKey(NOTES_EXPORT_PREFIX);
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

// Grows (or shrinks) a textarea to fit whatever it holds, rather than
// leaving a reader to scroll inside a box sized for four lines. The
// offsetHeight/clientHeight gap is the border alone (clientHeight already
// counts padding on a border-box element), so adding it back keeps this
// exact regardless of how wide that border is.
function autoGrowTextarea(el) {
  el.style.height = "auto";
  const border = el.offsetHeight - el.clientHeight;
  el.style.height = `${el.scrollHeight + border}px`;
}

function initProgressSection() {
  const section = document.getElementById("dl-settings-work");
  if (!section) return;

  if (NON_TUTORIAL_PAGES.has(currentManifest.slug)) {
    section.remove();
    return;
  }

  notesEl = document.getElementById("dl-progress-notes");
  // Not grown here: the Notes panel is normally still hidden at this
  // point, and a hidden element's scrollHeight reads as 0.
  // initRightPanels() re-measures whenever the panel actually opens.
  if (notesEl) {
    notesEl.addEventListener("input", () => {
      autoGrowTextarea(notesEl);
      scheduleSave();
      updateNotesNudge();
    });
  }

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
      refreshHighlightsList();
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
    if (notesEl) {
      notesEl.value = "";
      autoGrowTextarea(notesEl);
    }
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
      const key = `${PROGRESS_PREFIX}${link.dataset.id}`;
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
  return pageKey(VERSION_PIN_PREFIX);
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

  // Which release you are on is a where-you-are question: the section
  // lives under this tutorial's own rung of the tree, not in a panel.
  // Marked up in the Imports & Exports panel only because the tree is
  // built per page and the shell is not.
  const own = document.querySelector(".dl-crumb-level-4");
  if (own) {
    if (own.tagName === "DETAILS") own.append(section); else own.after(section);
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

/* The runtime's saved-work keys were `dewlab:<kind>:<module>:<slug>`; they
 * are `dewlab:<kind>:<id>` now. This runs once per page load, before
 * anything reads a key, and renames the keys that belong to this page's
 * old address. `manifest.legacy` is the old `module:slug` the build writes
 * for every page that had one (and, for the one renamed id, the old slug
 * too); a tutorial written after the change has no `legacy` and this does
 * nothing. */
function migrateStorage(manifest) {
  if (!manifest || !manifest.legacy || !manifest.id) return;
  let store;
  try { store = window.localStorage; } catch (err) { return; }
  const oldSuffix = ":" + manifest.legacy;      // e.g. ":computational-methods:first-steps"
  const newSuffix = ":" + manifest.id;          // e.g. ":first-steps-cm"
  const renames = [];
  for (let i = 0; i < store.length; i += 1) {
    const key = store.key(i);
    if (key && key.startsWith("dewlab:") && key.endsWith(oldSuffix)) {
      renames.push(key);
    }
  }
  for (const key of renames) {
    const next = key.slice(0, -oldSuffix.length) + newSuffix;
    if (store.getItem(next) === null) {
      // Never overwrite work saved under the new key already: a reader who
      // has used the new address since the change keeps that.
      store.setItem(next, store.getItem(key));
    }
    store.removeItem(key);
  }
}

/* Which course the reader is following. A page is built with the chrome
 * — tree, previous and next, "also part of" — of the first course that
 * lists it (build.py, crumb_trail_html()). A reader on another course
 * that lists it arrived from that course's page, which remembered the
 * course here, or chose it on the tree's course rung; then
 * drawCourseChrome() redraws those parts from assets/routes.json. */
const COURSE_KEY = "dewlab:course";

function rememberCourse(course) {
  try { localStorage.setItem(COURSE_KEY, course); } catch (err) { /* private mode */ }
}

function currentCourse(manifest) {
  const listed = Array.isArray(manifest.courses) ? manifest.courses : [];
  if (!listed.length) return "";
  let wanted = "";
  try {
    wanted = new URLSearchParams(location.search).get("course") || localStorage.getItem(COURSE_KEY) || "";
  } catch (err) { wanted = ""; }
  return listed.includes(wanted) ? wanted : listed[0];
}

function initCourse(manifest) {
  // A course page remembers itself: opening a tutorial from it is
  // following that course.
  if (manifest.course) rememberCourse(manifest.course);
  const listed = Array.isArray(manifest.courses) ? manifest.courses : [];
  if (listed.length < 2) return;
  const chosen = currentCourse(manifest);
  const root = (manifest.assetBase || "").replace(/assets\/$/, "");
  fetch(`${manifest.assetBase}routes.json`)
    .then((response) => (response.ok ? response.json() : null))
    .then((routes) => {
      if (!routes || !Array.isArray(routes.courses)) return;
      const mine = routes.courses.filter((course) => listed.includes(course.id));
      addCourseChooser(manifest, mine, chosen, root);
      if (chosen !== listed[0]) drawCourseChrome(manifest, mine, chosen, root);
    })
    .catch(() => {});
}

function courseLink(root, course) {
  const a = document.createElement("a");
  a.href = `${root}${course.url}`;
  a.textContent = course.title;
  return a;
}

function listItem(children) {
  const item = document.createElement("div");
  item.setAttribute("role", "listitem");
  for (const child of children) item.append(child);
  return item;
}

/* The course rung of the tree becomes the switch on a page that sits in
 * more than one course: a select at the top of its list. */
function addCourseChooser(manifest, courses, chosen, root) {
  const rung = document.querySelector(".dl-crumb-level-2");
  const list = rung ? rung.querySelector('[role="list"]') : null;
  if (!list || rung.querySelector(".dl-course-switch")) return;
  const label = document.createElement("label");
  label.className = "dl-course-switch";
  label.append("Course: ");
  const select = document.createElement("select");
  for (const course of courses) {
    const option = document.createElement("option");
    option.value = course.id;
    option.textContent = course.title;
    option.selected = course.id === chosen;
    select.append(option);
  }
  select.addEventListener("change", () => {
    rememberCourse(select.value);
    drawCourseChrome(manifest, courses, select.value, root);
  });
  label.append(select);
  list.prepend(listItem([label]));
}

function drawCourseChrome(manifest, courses, chosen, root) {
  const course = courses.find((c) => c.id === chosen);
  if (!course) return;
  const ident = manifest.id;
  // Where this page sits on the chosen course: the series, its members,
  // and which member is this page or (for a page of problems) its owner.
  let series = null;
  let owner = null;
  let isPractice = false;
  for (const candidate of course.series || []) {
    for (const entry of candidate.tutorials || []) {
      if (entry.id === ident) { series = candidate; owner = entry; }
      else if (entry.practice && entry.practice.id === ident) {
        series = candidate; owner = entry; isPractice = true;
      }
    }
  }

  const courseRung = document.querySelector(".dl-crumb-level-2");
  if (courseRung) {
    courseRung.querySelector("summary").textContent = course.title;
    const list = courseRung.querySelector('[role="list"]');
    const chooser = list.querySelector(".dl-course-switch");
    list.replaceChildren();
    if (chooser) list.append(listItem([chooser]));
    for (const s of course.series || []) {
      const first = (s.tutorials || [])[0];
      if (!first) continue;
      const a = document.createElement("a");
      a.href = `${root}${first.url}`;
      a.textContent = s.title;
      list.append(listItem([a]));
    }
  }

  const seriesRung = document.querySelector(".dl-crumb-level-3");
  const own = document.querySelector(".dl-crumb-level-4");
  if (seriesRung && own && series) {
    seriesRung.querySelector("summary").textContent = series.title;
    const list = seriesRung.querySelector('[role="list"]');
    list.replaceChildren();
    for (const entry of series.tutorials || []) {
      if (entry === owner && !isPractice) {
        list.append(own.parentElement && own.parentElement.getAttribute("role") === "listitem"
          ? own.parentElement : listItem([own]));
        continue;
      }
      const a = document.createElement("a");
      a.href = `${root}${entry.url}`;
      a.textContent = entry.title;
      if (entry === owner && isPractice) {
        const under = document.createElement("div");
        under.setAttribute("role", "list");
        under.append(own.parentElement && own.parentElement.getAttribute("role") === "listitem"
          ? own.parentElement : listItem([own]));
        list.append(listItem([a, under]));
        continue;
      }
      list.append(listItem([a]));
    }
  }

  // Previous and next, for a tutorial on the route (a page of problems
  // has none, as the build gives it none).
  const nav = document.querySelector(".dl-nav-bottom");
  if (nav && series && !isPractice) {
    const members = series.tutorials || [];
    const index = members.indexOf(owner);
    for (const old of nav.querySelectorAll(".dl-nav-prev, .dl-nav-next")) old.remove();
    const up = nav.querySelector(".dl-nav-up");
    if (index > 0) {
      const a = document.createElement("a");
      a.className = "dl-nav-prev";
      a.href = `${root}${members[index - 1].url}`;
      a.textContent = members[index - 1].title;
      nav.prepend(a);
    }
    if (index >= 0 && index < members.length - 1) {
      const a = document.createElement("a");
      a.className = "dl-nav-next";
      a.href = `${root}${members[index + 1].url}`;
      a.textContent = members[index + 1].title;
      if (up) up.after(a); else nav.append(a);
    }
  }

  // "This page is also part of …": every course but the one being followed.
  const line = document.querySelector(".dl-also-part-of");
  if (line) {
    const others = courses.filter((c) => c.id !== chosen);
    line.replaceChildren("This page is also part of ");
    others.forEach((other, i) => {
      if (i > 0) line.append(i === others.length - 1 ? " and " : ", ");
      line.append(courseLink(root, other));
    });
    line.append(".");
  }
}

const currentManifest = readManifest();
migrateStorage(currentManifest);

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
buildQuestions();
buildSiteEditors(currentManifest);
wireDiagramWidthSliders();
buildAppCells(currentManifest);
if (currentManifest.appCells && currentManifest.appCells.length) {
  globalThis.dewlabQueryRows = queryRows;
}
initProgressSection();
initCustomCellsSection();
initExecutionSection();
initRunStatsToggle();
initStagedHintsToggles();
initExportSection();
initVersionsSection();
initVersionMarker();
initRightPanels();
initSettingsTabs();
initReference(currentManifest);
initReferenceLookup(currentManifest);
initHighlightPopover();
// After every toggle it mirrors has settled its own hidden state —
// Reference only unhides itself in initReference() above.
initMobileLauncher();
initWhereYouAre();
initCourse(currentManifest);
watchPanelOverlap();
restoreSidebarState();
initProgressBadgesToggle();
initNotesNudgeToggle();
initContentsProgress();
trackChromeHeight();
trackCornerDockHeights();
announceRestore(restoreSaved());
refreshHighlightsList();
updateProgressSummary();
updateNotesNudge();
annotateNotice();
highlightIllustrativeCode();
const mathsRendered = renderMaths(currentManifest);

// A link from My Notes (or anywhere else) can name one highlight by id in
// the URL's own hash -- #dl-highlight-<id> -- the same way a plain HTML
// anchor names a heading. Waits for maths to finish rendering first: a
// KaTeX block below the highlighted passage can still shift the page's
// layout after this script runs, and jumping before that would land
// short. A hash naming a highlight this page doesn't have (a stale link,
// or one this browser's storage never carried) is silently ignored, the
// same "a notice, never a block" posture a dropped highlight already gets.
if (location.hash.startsWith("#dl-highlight-")) {
  const wanted = location.hash.slice("#dl-highlight-".length);
  mathsRendered.then(() => jumpToHighlight(wanted, { openPopover: false }));
}

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
  // Highlights and margin notes: the anchoring lookup, the
  // in-memory/save-schema state, the DOM wrap/unwrap pair, and the
  // highlight-creation helpers the selection toolbar's Highlight
  // button now calls, exposed here for their own tests too.
  proseBlocks,
  describeQuote,
  locateHighlightAnchor,
  highlights,
  rangeForOffsets,
  wrapRange,
  unwrapHighlight,
  blockFor,
  createHighlight,
  recolorHighlight,
  jumpToHighlight,
  refreshHighlightsList,
};
