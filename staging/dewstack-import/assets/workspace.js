/* The dewstack workspace: the site editor component (assets/site-editor.js)
 * on a page of its own, with several named sites saved in the browser
 * (planning/CONSOLE_AND_WORKSPACE.md, section 5, decided 2026-09-06).
 *
 * What this file owns, and site-editor.js does not: the list of sites and
 * which one is open; saving every edit to localStorage; the name field;
 * New, Delete, and Load files; and the CodeMirror panes it hands the
 * component in place of its textareas. What it does not own: the preview,
 * the Run model, the console — those are the component's, written once
 * for the tutorial pages and reused here unchanged.
 *
 * Saved under one key, `dewstack:workspace:v1`, as {active, sites:[{id,
 * name, html, css, js}]}, the same "this browser, this device" pattern as
 * the SQL cell's persisted table and dewmini's notebooks. localStorage
 * can throw (private mode, a browser told to block site data), so every
 * read and write is guarded, and a failure means this visit does not
 * save, not that the page breaks. The student's fork is where real work
 * lives; the page's own first paragraph says so.
 *
 * CodeMirror comes from assets/vendor/codemirror.bundle.js, built by
 * vendor-src/ and loaded on this page alone (section 7 of the design):
 * tutorial pages keep their textareas, because they are read on phones.
 */

import { createCodeEditor } from "./vendor/codemirror.bundle.js";

const KEY = "dewstack:workspace:v1";
/* A site handed over by a tutorial page's "Open in the workspace"
   (site-editor.js writes it, this page consumes it once). */
const INCOMING_KEY = "dewstack:workspace:incoming";

/* A new site's starting text, so the first thing a student sees is a page
 * and a console line, not three empty boxes. */
const STARTER = {
  html: "<h1>Hello</h1>\n<p>Change this text, and watch the preview.</p>\n",
  css: "body {\n  font-family: sans-serif;\n  padding: 1rem;\n}\n",
  js: 'console.log("The script ran.");\n',
};

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
 * pagehide, so a tab closed inside the debounce loses nothing. */
function saveState(state) {
  clearTimeout(saveTimer);
  pendingSave = state;
  saveTimer = setTimeout(() => writeState(state), 150);
}
window.addEventListener("pagehide", () => { if (pendingSave) writeState(pendingSave); });

function newSite(name) {
  return { id: `s${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`, name, ...STARTER };
}

function nextName(state) {
  const taken = new Set(state.sites.map((s) => s.name));
  let n = state.sites.length + 1;
  while (taken.has(`Site ${n}`)) n += 1;
  return `Site ${n}`;
}

/* "My first site" becomes "my-first-site.html": a file name a student can
 * drop into a fork without renaming. */
function fileBase(name) {
  const base = name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return base || "site";
}

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
const editorEl = document.getElementById("site-editor-workspace");
const listEl = document.querySelector(".dl-ws-list");
const nameEl = document.querySelector(".dl-ws-name");
const newButton = document.querySelector(".dl-ws-new");
const deleteButton = document.querySelector(".dl-ws-delete");
const loadButton = document.querySelector(".dl-ws-load");
const fileInput = document.querySelector(".dl-ws-file");

const codeEditors = {};

function activeSite() {
  return state.sites.find((s) => s.id === state.active) || state.sites[0];
}

/* A CodeMirror pane in place of the textarea the markup carries, with the
 * same five-method surface site-editor.js's own textareaPane() has. The
 * textarea stays in the document, hidden, so the component's markup is
 * one thing whichever page it is on. */
function createPane(field, lang) {
  field.hidden = true;
  const host = document.createElement("div");
  host.className = "dl-site-cm";
  field.insertAdjacentElement("afterend", host);
  const inputHandlers = [];
  const runHandlers = [];
  const cm = createCodeEditor(host, field.value, {
    dark: isDark(),
    language: lang,
    onChange: (text) => inputHandlers.forEach((cb) => cb(text)),
    onRun: lang === "js" ? () => runHandlers.forEach((cb) => cb()) : null,
  });
  codeEditors[lang] = cm;
  return {
    get: () => cm.getValue(),
    set: (text) => cm.setValue(text),
    focus: () => cm.focus(),
    selectLine: (n) => cm.selectLine(n),
    onInput: (cb) => inputHandlers.push(cb),
    onRun: (cb) => runHandlers.push(cb),
  };
}

const site = window.dewstackSiteEditor.mount(editorEl, {
  createPane,
  onChange: (lang, text) => {
    activeSite()[lang] = text;
    saveState(state);
  },
});

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
  site.load({ html: s.html, css: s.css, js: s.js });
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
 * button and says so, the second within a few seconds does it. One click
 * on the wrong button should never cost a site. */
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
 * a page from a fork can be brought in, changed, and downloaded back. */
loadButton.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", async () => {
  const s = activeSite();
  const files = { html: s.html, css: s.css, js: s.js };
  for (const file of fileInput.files) {
    const ext = file.name.split(".").pop().toLowerCase();
    if (ext in files) files[ext] = await file.text();
  }
  fileInput.value = "";
  Object.assign(s, files);
  site.load(files);
  saveState(state);
});

/* Settings' theme change reaches CodeMirror too, without a reload. */
function applyTheme() {
  Object.values(codeEditors).forEach((cm) => cm.setTheme(isDark()));
}
new MutationObserver(applyTheme).observe(root, { attributes: true, attributeFilter: ["data-theme"] });
darkQuery.addEventListener("change", applyTheme);

/* A site arriving from a tutorial page becomes a new site here, opened,
 * and the hand-off is cleared so a reload does not make it twice. */
function takeIncoming() {
  let incoming = null;
  try {
    const raw = localStorage.getItem(INCOMING_KEY);
    if (raw) incoming = JSON.parse(raw);
    localStorage.removeItem(INCOMING_KEY);
  } catch (e) { return; }
  if (!incoming || typeof incoming !== "object") return;
  const s = newSite(String(incoming.name || nextName(state)));
  s.html = String(incoming.html || "");
  s.css = String(incoming.css || "");
  s.js = String(incoming.js || "");
  state.sites.push(s);
  state.active = s.id;
}

takeIncoming();
openSite(state.active);
