/* Editing a page where it stands (planning/IN_PAGE_EDITOR.md).
 *
 * Loaded only when a teacher presses "Edit this page" in Settings (or opens a
 * page with #edit on the end), never by a student's page load. A built page
 * carries `data-md="START:END"` on each top-level block, the byte range of the
 * markdown file that produced it (source_map.py), and its manifest names the
 * file and the git blob sha the site was built from (`manifest.edit`).
 *
 * Opening a block swaps it for an editor that sits in the same place and takes
 * the page's own styles: Crepe for a heading or a plain paragraph, a text box
 * of the block's markdown for anything the rich editor would not round-trip
 * safely. Leaving a block keeps what was typed. Saving splices each changed
 * block's markdown over its own range of the file and opens one draft pull
 * request, then adds commits to it. Every other byte of the file is left alone.
 *
 * This file reads the page and the file and writes nothing but the pull
 * request. It has no server to talk to except GitHub's.
 */

import { githubClient, TOKEN_KEY } from "./github-client.js";
import { richSafe, toEditor, fromEditor } from "./inpage-markdown.js";
import { parseTable, cellText } from "./inpage-table.js";
import { isCellBlock, parseCellBlock, buildCellBlock, problem } from "./inpage-cell.js";

const MIN_WIDTH = 900;

/* ----------------------------------------------------------------- pure */

/* Apply `{start, end, text}` edits to `source`, last first so earlier offsets
 * stay true. Edits must not overlap. */
export function splice(source, edits) {
  const ordered = [...edits].sort((a, b) => a.start - b.start);
  for (let i = 1; i < ordered.length; i += 1) {
    if (ordered[i - 1].end > ordered[i].start) throw new Error("Two edits overlap.");
  }
  let out = source;
  for (const edit of ordered.reverse()) out = out.slice(0, edit.start) + edit.text + out.slice(edit.end);
  return out;
}

/* How a block can be edited, from its element and its markdown:
 *   "rich"   a heading, paragraph, list or quote the rich editor round-trips
 *            safely (inpage-markdown.js says which; maths and `{.term}` marks
 *            are handled there)
 *   "cell"   a `python exec` or `sql exec` cell with its hint and solution
 *            fences: a code editor for the code, its id held fixed
 *            (inpage-cell.js)
 *   "source" anything else a person can reasonably change, as its markdown:
 *            tables, folds, raw HTML, images, display maths, code
 *   "locked" includes, other fences, and the pieces of a page built from
 *            other parts */
export function classify(tag, text) {
  const t = text.trim();
  if (isCellBlock(t) && parseCellBlock(t)) return "cell";
  if (tag === "pre" && t.startsWith("```")) return "source";   // an ordinary code fence
  if (!t || t.startsWith("{{include") || t.startsWith("```")) return "locked";
  if (/^h[1-6]$/.test(tag) || tag === "p" || ["ul", "ol", "blockquote"].includes(tag)) {
    return richSafe(t) ? "rich" : "source";
  }
  if (["table", "details", "pre"].includes(tag)) return "source";
  return "locked";
}

/* Where the title of a fold lies in the fold's markdown, as offsets into the
 * fold's text, or null when it is not a plain one-line title. */
export function foldTitle(text) {
  const open = text.indexOf("<summary>");
  const close = text.indexOf("</summary>");
  if (open < 0 || close < open) return null;
  const start = open + "<summary>".length;
  const title = text.slice(start, close);
  if (/[\n<]/.test(title)) return null;
  return { start, end: close };
}

export function summary(count) {
  if (!count) return "No changes yet.";
  return count === 1 ? "1 block changed." : `${count} blocks changed.`;
}

/* ------------------------------------------------------------------ dom */

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (value !== false && value != null) node.setAttribute(key, value === true ? "" : value);
  }
  node.append(...children);
  return node;
}

const $ = (id) => document.getElementById(id);

/* ------------------------------------------------------------- the session */

export async function begin(manifest, { client = null, createEditor = null, createCode = null } = {}) {
  const status = $("dl-edit-status");
  const say = (text) => { if (status) status.textContent = text; };

  if (window.innerWidth < MIN_WIDTH) {
    say("Editing needs a larger screen. Open this page on a computer or a tablet held wide.");
    return null;
  }

  if (!client) {
    let token = null;
    try { token = localStorage.getItem(TOKEN_KEY); } catch (e) { /* blocked storage */ }
    if (!token) token = await askForToken();
    if (!token) return null;
    client = githubClient(token);
  }

  say("Getting this page's source…");
  let source;
  try {
    source = await client.blob(manifest.edit.sha);
  } catch (error) {
    say(`Could not read this page's source from GitHub. ${error.message}`);
    return null;
  }

  if (!createEditor) {
    const bundle = await import(manifest.edit.editor);
    createEditor = bundle.createInPlaceEditor;
  }

  return new Session({ manifest, client, source, createEditor, createCode, say });
}

function askForToken() {
  const gate = $("dl-edit-gate");
  gate.hidden = false;
  return new Promise((resolve) => {
    const field = el("input", { type: "password", id: "dl-edit-token", autocomplete: "off",
                                placeholder: "github_pat_…", "aria-label": "GitHub token" });
    const form = el("form", { class: "dl-edit-gate-form", onsubmit: (event) => {
      event.preventDefault();
      const value = field.value.trim();
      if (!value) return;
      try { localStorage.setItem(TOKEN_KEY, value); } catch (e) { /* blocked storage */ }
      const forget = $("dl-edit-forget");
      if (forget) forget.hidden = false;
      gate.hidden = true;
      gate.replaceChildren();
      resolve(value);
    } },
      el("p", { class: "dl-panel-note" },
        "Paste a GitHub token that can propose changes to this repository. "
        + "It stays in this browser. The guide says how to make one."),
      field,
      el("button", { type: "submit", class: "dl-btn" }, "Start editing"));
    gate.replaceChildren(form);
    field.focus();
  });
}

class Session {
  constructor({ manifest, client, source, createEditor, createCode, say }) {
    this.manifest = manifest;
    this.client = client;
    this.source = source;
    this.createEditor = createEditor;
    this.createCode = createCode;
    this.say = say;
    this.edits = new Map();    // "start:end" -> { start, end, text }
    this.open = null;          // the block being edited now
    this.pr = null;            // { branch, url } once a pull request exists
    this.saving = false;
    this.changes = 0;          // counts every change to the set of edits,
    this.savedAt = 0;          // so "unsaved" is changes !== savedAt

    this.root = document.getElementById("dl-body");
    /* The page's blocks, and the blocks inside its folds. A fold's title is a
     * block of its own, given a range here (the fold's markdown has one). */
    const found = [];
    const walk = (parent) => {
      for (const node of parent.children) {
        if (!node.hasAttribute("data-md")) continue;
        found.push(node);
        if (node.tagName === "TABLE") found.push(...this.tableCells(node));
        if (node.tagName === "DETAILS" && node.querySelector("[data-md]")) {
          const [start] = node.getAttribute("data-md").split(":").map(Number);
          const title = foldTitle(this.source.slice(start, Number(node.getAttribute("data-md").split(":")[1])));
          const head = node.querySelector(":scope > summary");
          if (title && head) {
            head.setAttribute("data-md", `${start + title.start}:${start + title.end}`);
            found.push(head);
          }
          walk(node);
          /* Edit mode shows what a fold holds; stopping puts it back. */
          if (!node.open) { node.open = true; this.folded.push(node); }
        }
      }
    };
    this.folded = [];
    walk(this.root);
    this.blocks = found;
    document.body.classList.add("dl-editing");
    for (const node of this.blocks) this.arm(node);

    this.onClick = (event) => {
      const hit = event.target.closest("[data-md]");
      if (!hit) return;
      const node = hit.dlOwner || hit;           // an editor stands for the block it replaced
      if (!this.blocks.includes(node)) return;
      if (node.tagName === "SUMMARY" || event.target.closest("summary")) event.preventDefault();   // do not fold or unfold
      if (!node.dataset.dlEdit) return;
      if (event.target.closest("a")) event.preventDefault();
      /* A cell's own buttons (run, reset, the code box) do nothing while editing. */
      if (node.dataset.dlEdit === "cell" && !hit.dlOwner) { event.preventDefault(); event.stopPropagation(); }
      if (!this.open || this.open.node !== node) this.openBlock(node);
    };
    this.root.addEventListener("click", this.onClick, true);

    this.buttons();
    this.report();
  }

  /* Give each cell of a table the range of its own text, if the table's
   * markdown and the page's table agree on its shape. Otherwise none, and the
   * table stays one markdown box. */
  tableCells(table) {
    const [start, end] = table.getAttribute("data-md").split(":").map(Number);
    const parsed = parseTable(this.source.slice(start, end));
    const rows = [...table.querySelectorAll("tr")];
    if (!parsed || parsed.length !== rows.length
        || parsed.some((cells, i) => cells.length !== rows[i].children.length)) return [];
    const out = [];
    parsed.forEach((cells, i) => cells.forEach((range, j) => {
      const cell = rows[i].children[j];
      cell.setAttribute("data-md", `${start + range.start}:${start + range.end}`);
      out.push(cell);
    }));
    table.dlGrid = true;
    return out;
  }

  arm(node) {
    const [start, end] = node.getAttribute("data-md").split(":").map(Number);
    const text = this.source.slice(start, end);
    const tag = node.tagName.toLowerCase();
    /* A fold with blocks inside is edited through them and its title. */
    const mode = tag === "summary" ? "summary"
      : tag === "td" || tag === "th" ? "tablecell"
      : tag === "details" && node.querySelector("[data-md]") ? "fold"
      : tag === "table" && node.dlGrid ? "fold"
      : classify(tag, text);
    node.dataset.dlEdit = mode === "locked" || mode === "fold" ? "" : mode;
    if (mode === "locked") node.classList.add("dl-edit-locked");
    else if (mode !== "fold") node.classList.add("dl-editable");
    node.dlRange = { start, end, text };
  }

  report() {
    this.say(summary(this.edits.size) + (this.pr ? ` In ${this.pr.url}` : ""));
    const save = $("dl-edit-save");
    if (save) save.disabled = this.saving || this.edits.size === 0;
    const discard = $("dl-edit-discard");
    if (discard) discard.disabled = this.saving || this.edits.size === 0;
  }

  buttons() {
    /* The button's own listener (assets/shell.html) calls toggle(), which stops
       a session that exists; a second handler here made one click stop the
       session and, a moment later, start another. */
    $("dl-edit-toggle").textContent = "Stop editing";
    const actions = $("dl-edit-actions");
    actions.hidden = false;
    $("dl-edit-save").onclick = () => this.save();
    $("dl-edit-discard").onclick = () => this.discard();
  }

  /* ------------------------------------------------------------ one block */

  textOf(node) {
    const edit = this.edits.get(node.getAttribute("data-md"));
    return edit ? edit.text : node.dlRange.text;
  }

  async openBlock(node) {
    if (!(await this.closeBlock())) return;
    const mode = node.dataset.dlEdit;
    const text = this.textOf(node);
    const key = node.getAttribute("data-md");

    if (node.dlEditor) {                       // edited before: wake it
      node.dlEditor.setEditable(true);
      node.dlEditor.focus();
      this.open = { node, wrap: node.dlWrap, mode: "rich", before: text, key };
      return;
    }
    if (node.dlBox) {
      node.dlBox.focus();
      this.open = { node, wrap: node.dlBox, mode: "source", before: text, key };
      return;
    }
    if (node.dlLine) {
      node.focus();
      this.open = { node, wrap: node, mode: "tablecell", before: text, key };
      return;
    }
    if (node.dlInput) {
      node.dlInput.focus();
      this.open = { node, wrap: node.dlInput, mode: "summary", before: text, key };
      return;
    }
    if (node.dlCell) {
      node.dlCell.focus();
      this.open = { node, wrap: node.dlCell.panel, mode: "cell", before: text, key };
      return;
    }

    if (mode === "tablecell") {
      node.dlHtml = node.innerHTML;
      node.textContent = text;                   // the cell's markdown, as in the file
      node.contentEditable = "plaintext-only";
      if (node.contentEditable !== "plaintext-only") node.contentEditable = "true";
      node.dlLine = true;
      node.addEventListener("keydown", node.dlKeys = (event) => { if (event.key === "Enter") { event.preventDefault(); node.blur(); } });
      node.addEventListener("blur", node.dlBlur = () => this.closeBlock());
      node.focus();
      const range = document.createRange();
      range.selectNodeContents(node);
      range.collapse(false);
      getSelection().removeAllRanges();
      getSelection().addRange(range);
      this.open = { node, wrap: node, mode, before: text, key };
    } else if (mode === "summary") {
      node.dlHtml = node.innerHTML;
      const input = el("input", { class: "dl-inplace-summary", type: "text", value: text,
                                  "aria-label": "Title of this fold" });
      input.addEventListener("blur", () => this.closeBlock());
      input.addEventListener("keydown", (event) => { if (event.key === "Enter") input.blur(); if (event.key === " ") event.stopPropagation(); });
      node.replaceChildren(input);
      node.dlInput = input;
      input.focus();
      this.open = { node, wrap: input, mode, before: text, key };
    } else if (mode === "cell") {
      await this.openCell(node, text, key);
    } else if (mode === "rich") {
      const wrap = el("div", { class: "dl-inplace", "data-md": key });
      /* An editable element is its own formatting context, so the block's
       * margins would stay inside it. The wrapper takes the block's own and the
       * editor's first and last child take none (tutorial-style.css), which
       * leaves the page's spacing exactly as it was. */
      wrap.style.margin = getComputedStyle(node).margin;
      wrap.dlOwner = node;
      node.after(wrap);
      node.hidden = true;
      const state = toEditor(text);
      const editor = this.createEditor(wrap, state.doc);
      await editor.ready;
      state.baseline = editor.getMarkdown();     // what it writes before any typing
      node.dlState = state;
      node.dlWrap = wrap;
      node.dlEditor = editor;
      editor.focus();
      wrap.addEventListener("focusout", (event) => {
        if (!wrap.contains(event.relatedTarget)) this.closeBlock();
      });
      this.open = { node, wrap, mode, before: text, key };
    } else {
      const box = el("textarea", { class: "dl-inplace-source", spellcheck: "true",
                                   "aria-label": "This block's markdown", "data-md": key });
      box.value = text;
      box.style.margin = getComputedStyle(node).margin;
      const fit = () => { box.style.height = "auto"; box.style.height = `${box.scrollHeight}px`; };
      box.addEventListener("input", fit);
      box.addEventListener("blur", () => this.closeBlock());
      box.dlOwner = node;
      node.after(box);
      node.hidden = true;
      node.dlBox = box;
      fit();
      box.focus();
      this.open = { node, wrap: box, mode, before: text, key };
    }
  }

  /* A cell: its code in a code editor, the id shown and held, and each fence
   * written after it (hint, solution…) as a text box. */
  async openCell(node, text, key) {
    const parsed = parseCellBlock(text);
    const code = this.createCode || (await import(this.manifest.edit.code)).createCodeEditor;
    const dark = document.documentElement.getAttribute("data-theme") === "dark"
      || (document.documentElement.getAttribute("data-theme") !== "light"
          && window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
    const panel = el("div", { class: "dl-inplace-cell", "data-md": key });
    panel.dlOwner = node;
    panel.style.margin = getComputedStyle(node).margin;
    const fields = parsed.parts.map((part, index) => {
      const label = el("p", { class: "dl-cell-part-label" }, part.label);
      const children = [label];
      let read;
      let focus;
      if (index === 0) {
        children.push(el("p", { class: "dl-cell-id" },
          el("code", {}, part.locked.trim()), " — the id is fixed: saved answers are filed under it"));
        const host = el("div", { class: "dl-cell-code" });
        children.push(host);
        panel.append(...children);
        const editor = code(host, part.text, { dark, language: part.language || "python" });
        read = () => editor.getValue();
        focus = () => editor.focus();
        return { read, focus, destroy: () => editor.destroy() };
      }
      const box = el("textarea", { class: "dl-inplace-source", spellcheck: "true", "aria-label": part.label });
      box.value = part.text;
      const fit = () => { box.style.height = "auto"; box.style.height = `${box.scrollHeight}px`; };
      box.addEventListener("input", fit);
      children.push(box);
      panel.append(...children);
      fit();
      return { read: () => box.value, focus: () => box.focus(), destroy: () => {}, fit };
    });
    panel.addEventListener("focusout", (event) => {
      if (!panel.contains(event.relatedTarget)) this.closeBlock();
    });
    panel.addEventListener("focusin", () => {
      if (!this.open || this.open.node !== node) this.openBlock(node);
    });
    node.after(panel);
    node.hidden = true;
    for (const field of fields) if (field.fit) field.fit();
    node.dlCell = {
      panel, parsed, fields,
      values: () => fields.map((field) => field.read()),
      focus: () => fields[0].focus(),
      destroy: () => { for (const field of fields) field.destroy(); },
    };
    node.dlCell.initial = node.dlCell.values();
    node.dlCell.focus();
    this.open = { node, wrap: panel, mode: "cell", before: text, key };
  }

  async closeBlock() {
    const open = this.open;
    if (!open) return true;
    this.open = null;
    const { node, mode, key } = open;
    const original = node.dlRange.text;
    let now;
    if (mode === "tablecell") {
      now = cellText(node.textContent);
    } else if (mode === "summary") {
      now = node.dlInput.value.replace(/\s+/g, " ").trim();
      if (/[<\n]/.test(now)) {
        this.say("A fold's title is a single line of plain text. Edit the file on GitHub for more.");
        this.open = open;
        return false;
      }
    } else if (mode === "cell") {
      const { parsed, values, initial } = node.dlCell;
      const now_values = values();
      const unchanged = now_values.every((value, index) => value === initial[index]);
      const wrong = unchanged ? null : problem(parsed, now_values);
      if (wrong) {
        this.say(wrong);
        this.open = open;                       // stays open until it is put right
        return false;
      }
      now = unchanged ? original : buildCellBlock(parsed, now_values);
    } else if (mode === "rich") {
      const written = node.dlEditor.getMarkdown();
      /* Nothing typed: the editor writes the block a little differently from
       * the file (an indent, a marker), which is not a change. */
      now = written === node.dlState.baseline ? original : fromEditor(written, node.dlState, original);
    } else {
      now = node.dlBox.value.replace(/\s+$/, "");
    }

    const was = this.edits.get(key);
    if (now === original) {
      if (was) this.changes += 1;
      this.edits.delete(key);
      this.restore(node);
    } else {
      if (!was || was.text !== now) this.changes += 1;
      this.edits.set(key, { start: node.dlRange.start, end: node.dlRange.end, text: now });
      if (mode === "rich") node.dlEditor.setEditable(false);
      (node.dlWrap || node.dlBox || node.dlInput || (node.dlLine && node) || node.dlCell.panel).dataset.edited = "";
    }
    this.report();
    return true;
  }

  /* Put the page's own element back where an unchanged block was. */
  restore(node) {
    if (node.dlEditor) { node.dlEditor.destroy(); node.dlEditor = null; }
    if (node.dlWrap) { node.dlWrap.remove(); node.dlWrap = null; }
    if (node.dlBox) { node.dlBox.remove(); node.dlBox = null; }
    if (node.dlInput) { node.innerHTML = node.dlHtml; node.dlInput = null; }
    if (node.dlLine) {
      node.removeEventListener("keydown", node.dlKeys);
      node.removeEventListener("blur", node.dlBlur);
      node.removeAttribute("contenteditable");
      node.innerHTML = node.dlHtml;
      node.dlLine = false;
      delete node.dataset.edited;
    }
    if (node.dlCell) { node.dlCell.destroy(); node.dlCell.panel.remove(); node.dlCell = null; }
    node.hidden = false;
  }

  /* -------------------------------------------------------------- session */

  async discard() {
    await this.closeBlock();
    this.open = null;                          // a cell left unfinished is discarded with the rest
    for (const node of this.blocks) this.restore(node);
    if (this.edits.size) this.changes += 1;
    this.edits.clear();
    this.report();
  }

  get unsaved() {
    return this.changes !== this.savedAt;
  }

  async stop() {
    if (!(await this.closeBlock())) return;
    if (this.unsaved) {
      const ok = window.confirm(`${summary(this.edits.size)} They are not saved. `
        + "Stop editing and lose them? Press Cancel to keep editing, then press Open pull request.");
      if (!ok) return;
      await this.discard();
    }
    this.root.removeEventListener("click", this.onClick, true);
    for (const fold of this.folded) fold.open = false;
    for (const node of this.blocks) {
      node.classList.remove("dl-editable", "dl-edit-locked");
      delete node.dataset.dlEdit;
      if (node.dlLine) {                                 // a saved cell keeps what was typed
        node.removeEventListener("keydown", node.dlKeys);
        node.removeEventListener("blur", node.dlBlur);
        node.removeAttribute("contenteditable");
        node.removeAttribute("data-md");
      } else if (node.tagName === "TD" || node.tagName === "TH") {
        node.removeAttribute("data-md");
      }
      if (node.tagName === "SUMMARY") {
        if (node.dlInput) node.textContent = node.dlInput.value;   // keep a saved title, drop the box
        node.removeAttribute("data-md");
      }
    }
    document.body.classList.remove("dl-editing");
    $("dl-edit-toggle").textContent = "Edit this page";
    $("dl-edit-actions").hidden = true;
    this.say(this.pr ? `Your changes are saved as a draft pull request: ${this.pr.url}` : "");
    window.dlEditSession = null;
    window.dispatchEvent(new CustomEvent("dl-edit-stopped"));
  }

  async save() {
    if (!(await this.closeBlock())) return;
    if (!this.edits.size || this.saving) return;
    this.saving = true;
    this.report();
    try {
      const { path, sha } = this.manifest.edit;
      const onMain = await this.client.fileShaAtMain(path);
      if (onMain !== sha) {
        throw new Error("This page has changed on GitHub since the site was built. "
          + "Reload the page, then make your changes again.");
      }
      const text = splice(this.source, [...this.edits.values()]);
      const files = [{ path, text }];
      const title = this.manifest.title || path;
      const message = `Edit ${title}\n\nChanged ${summary(this.edits.size).toLowerCase()}`;
      if (!this.pr) {
        const base = await this.client.mainSha();
        const stamp = new Date().toISOString().replace(/[-:T]/g, "").slice(0, 12);
        const branch = `edit/${this.manifest.slug}-${stamp}`;
        const url = await this.client.commit({ base, branch, message, files });
        this.pr = { branch, url };
      } else {
        await this.client.commitMore({ branch: this.pr.branch, message, files });
      }
      this.saving = false;
      this.savedAt = this.changes;
      this.say(`Saved. Your changes are a draft pull request: ${this.pr.url}`);
      const save = $("dl-edit-save");
      if (save) save.disabled = false;
    } catch (error) {
      this.saving = false;
      this.report();
      this.say(`${summary(this.edits.size)} Not saved. ${error.message}`);
    }
  }
}

/* The button in Settings calls this; so does a #edit address. */
export async function toggle(manifest) {
  if (window.dlEditSession) { await window.dlEditSession.stop(); return; }
  window.dlEditSession = await begin(manifest);
}
