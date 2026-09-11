/* dewmini web: several named HTML/CSS/JS sites, kept in this browser
 * (DECISIONS_LOG.md 7.143, DEWSTACK_MERGE.md §4). A separate product
 * from dewmini — a multi-file site, not a Python notebook — shaped like
 * dewstack's own assets/workspace.js: what this file owns is the list
 * of sites, which one is open, saving every edit, the name field, and
 * New/Delete/Load files/Download. What it does not own is the preview,
 * the Run model, and the console — those are assets/site-relay.js's
 * mountSitePreview(), the same engine assets/tutorial-runtime.js's
 * buildSiteEditors() and compose/dewmini.js's own Site tab already
 * mount, ported in shape from dewstack's own workspace.js rather than
 * sharing its code, the same "port in shape, not code" rule that
 * governs everything crossing the dewlab/dewstack boundary.
 *
 * The console's own DOM (one div per line, an error's "Go to line"
 * button, a friendly hint) is written fresh here rather than imported
 * from tutorial-runtime.js's buildSiteEditors(), which draws the
 * identical-looking thing for a tutorial page's site editor: the two are
 * independently maintained look-alikes, the same relationship
 * render_cell() (build.py) already has with dewmini's own cell markup
 * — worth sharing if it starts drifting, not worth the coupling before
 * it has.
 */

import { createCodeEditor, setEditorTheme } from "../assets/vendor/codemirror.bundle.js";
import { mountSitePreview } from "../assets/site-relay.js";

const KEY = "dewminiweb:sites:v1";

/* A new site's starting text, so the first thing a reader sees is a page
 * and a console line, not three empty boxes — the same reasoning
 * dewstack's own STARTER constant gives. */
const STARTER = {
  html: "<h1>Hello</h1>\n<p>Change this text, and watch the preview.</p>\n",
  css: "body {\n  font-family: sans-serif;\n  padding: 1rem;\n}\n",
  js: 'console.log("The script ran.");\n',
};

function newSite(name) {
  return {
    id: `s${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`,
    name,
    ...STARTER,
  };
}

function nextName(state) {
  const taken = new Set(state.sites.map((s) => s.name));
  let n = state.sites.length + 1;
  while (taken.has(`Site ${n}`)) n += 1;
  return `Site ${n}`;
}

/* "My first site" becomes "my-first-site" — a filename a reader can drop
 * into a project without renaming. */
function fileBase(name) {
  const base = name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return base || "site";
}

/* ------------------------------------------------------------- storage */

function readState() {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.sites) && parsed.sites.length) return parsed;
    }
  } catch (e) { /* unreadable or blocked: start fresh */ }
  const first = newSite("Site 1");
  return { active: first.id, sites: [first] };
}

let saveTimer = null;
let pendingSave = null;
function writeState(state) {
  clearTimeout(saveTimer);
  pendingSave = null;
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* this visit does not save */ }
}
/* Debounced, so a keystroke does not serialise every site; flushed on
 * pagehide, so a tab closed inside the debounce loses nothing — the
 * same pattern dewstack's own workspace.js uses. */
function saveState(state) {
  clearTimeout(saveTimer);
  pendingSave = state;
  saveTimer = setTimeout(() => writeState(state), 150);
}
window.addEventListener("pagehide", () => { if (pendingSave) writeState(pendingSave); });

/* --------------------------------------------------------------- theme */

const root = document.documentElement;
const darkQuery = window.matchMedia("(prefers-color-scheme: dark)");
function isDark() {
  const chosen = root.getAttribute("data-theme");
  if (chosen) return chosen === "dark";
  return darkQuery.matches;
}

/* ---------------------------------------------------------------- page */

const state = readState();

const listEl = document.querySelector(".dl-ws-list");
const nameEl = document.getElementById("dl-ws-name");
const newButton = document.querySelector(".dl-ws-new");
const deleteButton = document.querySelector(".dl-ws-delete");
const loadButton = document.querySelector(".dl-ws-load");
const fileInput = document.querySelector(".dl-ws-file");
const downloadButton = document.querySelector(".dl-ws-download");
const editorEl = document.getElementById("dl-ws-editor");
const iframe = document.getElementById("dl-ws-frame");
const consoleOut = document.getElementById("dl-ws-console");
const runButton = document.querySelector(".dl-btn-site-run");
const widthInput = document.getElementById("dl-ws-width");
const widthOut = document.getElementById("dl-ws-width-out");

function activeSite() {
  return state.sites.find((s) => s.id === state.active) || state.sites[0];
}

/* One CodeMirror pane per language, mounted once and reused across every
 * site — switching sites calls .setValue() on all three rather than
 * tearing editors down and rebuilding them, the same "the component
 * stays, the content changes" choice dewstack's own workspace.js makes
 * (its site.load()). */
const panes = {};
for (const lang of ["html", "css", "js"]) {
  const host = editorEl.querySelector(`.dl-site-pane[data-lang="${lang}"] .dl-editor`);
  panes[lang] = createCodeEditor(host, "", {
    dark: isDark(),
    language: lang === "js" ? "javascript" : lang,
    onChange: (text) => {
      activeSite()[lang] = text;
      saveState(state);
      if (lang !== "js") render();
    },
  });
}

function selectPaneLine(lang, n) {
  const { view } = panes[lang];
  const line = view.state.doc.line(Math.max(1, Math.min(n, view.state.doc.lines)));
  view.dispatch({ selection: { anchor: line.from, head: line.to }, scrollIntoView: true });
  view.focus();
}

const preview = mountSitePreview(iframe, {
  onReset: () => { consoleOut.textContent = ""; },
  onConsole: (level, text) => {
    const line = document.createElement("div");
    line.className = `dl-site-console-line dl-stdout dl-site-console-${level}`;
    line.textContent = text;
    consoleOut.appendChild(line);
  },
  onError: ({ message, where, hint }) => {
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
      go.addEventListener("click", () => selectPaneLine(where.lang, where.line));
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

function currentCode(lang) {
  return panes[lang].getValue();
}
function render() {
  preview.render(currentCode("html"), currentCode("css"));
}
function run() {
  preview.run(currentCode("html"), currentCode("css"), currentCode("js"));
}

runButton.addEventListener("mousedown", (e) => e.preventDefault());
runButton.addEventListener("click", run);
editorEl.querySelector('.dl-site-pane[data-lang="js"]').addEventListener("keydown", (ev) => {
  if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
    ev.preventDefault();
    ev.stopPropagation();
    run();
  }
}, true);

widthInput.addEventListener("input", () => {
  iframe.style.width = `${widthInput.value}%`;
  widthOut.textContent = `${widthInput.value}%`;
});

/* -------------------------------------------------------- site list UI */

function renderList() {
  listEl.innerHTML = "";
  state.sites.forEach((s) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = s.name;
    button.className = s.id === state.active ? "dl-ws-current" : "";
    button.setAttribute("aria-current", s.id === state.active ? "true" : "false");
    button.addEventListener("click", () => openSite(s.id));
    li.appendChild(button);
    listEl.appendChild(li);
  });
}

function openSite(id) {
  state.active = id;
  const s = activeSite();
  nameEl.value = s.name;
  editorEl.dataset.siteName = fileBase(s.name);
  for (const lang of ["html", "css", "js"]) panes[lang].setValue(s[lang]);
  run();
  renderList();
  disarmDelete();
  saveState(state);
}

nameEl.addEventListener("input", () => {
  const s = activeSite();
  s.name = nameEl.value.trim() || s.name;
  editorEl.dataset.siteName = fileBase(s.name);
  renderList();
  saveState(state);
});

newButton.addEventListener("click", () => {
  const s = newSite(nextName(state));
  state.sites.push(s);
  openSite(s.id);
  nameEl.focus();
  nameEl.select();
});

/* Two clicks to delete, the way dewmini settled on: the first arms the
 * button and says so, the second within a few seconds does it. */
let armedUntil = 0;
const DELETE_LABEL = "Delete this site";
function disarmDelete() {
  armedUntil = 0;
  deleteButton.textContent = DELETE_LABEL;
  deleteButton.classList.remove("dl-ws-armed");
}
deleteButton.addEventListener("click", () => {
  const now = Date.now();
  if (now > armedUntil) {
    armedUntil = now + 4000;
    deleteButton.textContent = "Click again to delete";
    deleteButton.classList.add("dl-ws-armed");
    setTimeout(() => { if (Date.now() >= armedUntil) disarmDelete(); }, 4100);
    return;
  }
  const index = state.sites.findIndex((s) => s.id === state.active);
  state.sites.splice(index, 1);
  if (!state.sites.length) state.sites.push(newSite("Site 1"));
  disarmDelete();
  openSite(state.sites[Math.max(0, index - 1)].id);
});

/* Load files: each picked file lands in the pane its extension names, so
 * a page from elsewhere can be brought in, changed, and downloaded back. */
loadButton.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", async () => {
  const s = activeSite();
  for (const file of fileInput.files) {
    const ext = file.name.split(".").pop().toLowerCase();
    const lang = ext === "js" ? "js" : ext === "css" ? "css" : ext === "html" ? "html" : null;
    if (lang) s[lang] = await file.text();
  }
  fileInput.value = "";
  for (const lang of ["html", "css", "js"]) panes[lang].setValue(s[lang]);
  run();
  saveState(state);
});

/* One file per pane, named after the site — the same naming
 * triggerDownload() (compose/dewmini.js) uses for its own exports. */
function triggerDownload(filename, content) {
  const blob = new Blob([content], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
downloadButton.addEventListener("click", () => {
  const s = activeSite();
  const base = fileBase(s.name);
  triggerDownload(`${base}.html`, s.html);
  triggerDownload(`${base}.css`, s.css);
  triggerDownload(`${base}.js`, s.js);
});

/* Settings' theme change reaches CodeMirror too, without a reload —
 * dewstack's own workspace.js watches the same attribute the same way. */
function applyTheme() {
  Object.values(panes).forEach((cm) => setEditorTheme(cm, isDark()));
}
new MutationObserver(applyTheme).observe(root, { attributes: true, attributeFilter: ["data-theme"] });
darkQuery.addEventListener("change", applyTheme);

renderList();
openSite(state.active);
