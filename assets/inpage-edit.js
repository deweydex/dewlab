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
 *   "rich"   a heading or paragraph the rich editor round-trips safely
 *   "source" anything else a person can reasonably change, as its markdown
 *   "locked" cells, includes and the pieces of a page built from other parts
 * Maths, `{.term}` marks, raw HTML and images are source blocks for now: the
 * rich editor does not yet know them (planning/IN_PAGE_EDITOR_SPIKE.md). */
export function classify(tag, text) {
  const t = text.trim();
  if (!t || t.startsWith("{{include") || t.startsWith("```")) return "locked";
  if (/^h[1-6]$/.test(tag) || tag === "p") {
    if (/[$<{\\]|!\[|^\[[^\]]+\]:/.test(t)) return "source";
    return "rich";
  }
  if (["ul", "ol", "blockquote", "table", "details", "pre"].includes(tag)) return "source";
  return "locked";
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

export async function begin(manifest, { client = null, createEditor = null } = {}) {
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

  return new Session({ manifest, client, source, createEditor, say });
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
  constructor({ manifest, client, source, createEditor, say }) {
    this.manifest = manifest;
    this.client = client;
    this.source = source;
    this.createEditor = createEditor;
    this.say = say;
    this.edits = new Map();    // "start:end" -> { start, end, text }
    this.open = null;          // the block being edited now
    this.pr = null;            // { branch, url } once a pull request exists
    this.saving = false;
    this.changes = 0;          // counts every change to the set of edits,
    this.savedAt = 0;          // so "unsaved" is changes !== savedAt

    this.root = document.getElementById("dl-body");
    this.blocks = [...this.root.children].filter((node) => node.hasAttribute("data-md"));
    document.body.classList.add("dl-editing");
    for (const node of this.blocks) this.arm(node);

    this.onClick = (event) => {
      const node = event.target.closest("[data-md]");
      if (!node || node.parentElement !== this.root || !node.dataset.dlEdit) return;
      if (event.target.closest("a")) event.preventDefault();
      if (!this.open || this.open.node !== node) this.openBlock(node);
    };
    this.root.addEventListener("click", this.onClick, true);

    this.buttons();
    this.report();
  }

  arm(node) {
    const [start, end] = node.getAttribute("data-md").split(":").map(Number);
    const text = this.source.slice(start, end);
    const mode = classify(node.tagName.toLowerCase(), text);
    node.dataset.dlEdit = mode === "locked" ? "" : mode;
    if (mode === "locked") node.classList.add("dl-edit-locked");
    else node.classList.add("dl-editable");
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
    $("dl-edit-toggle").textContent = "Stop editing";
    $("dl-edit-toggle").onclick = () => this.stop();
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
    await this.closeBlock();
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

    if (mode === "rich") {
      const wrap = el("div", { class: "dl-inplace", "data-md": key });
      /* An editable element is its own formatting context, so the block's
       * margins would stay inside it. The wrapper takes the block's own and the
       * editor's first and last child take none (tutorial-style.css), which
       * leaves the page's spacing exactly as it was. */
      wrap.style.margin = getComputedStyle(node).margin;
      node.after(wrap);
      node.hidden = true;
      const editor = this.createEditor(wrap, text);
      await editor.ready;
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
      node.after(box);
      node.hidden = true;
      node.dlBox = box;
      fit();
      box.focus();
      this.open = { node, wrap: box, mode, before: text, key };
    }
  }

  async closeBlock() {
    const open = this.open;
    if (!open) return;
    this.open = null;
    const { node, mode, key } = open;
    const now = mode === "rich"
      ? node.dlEditor.getMarkdown().replace(/\s+$/, "")
      : node.dlBox.value.replace(/\s+$/, "");
    const original = node.dlRange.text;

    const was = this.edits.get(key);
    if (now === original) {
      if (was) this.changes += 1;
      this.edits.delete(key);
      this.restore(node);
    } else {
      if (!was || was.text !== now) this.changes += 1;
      this.edits.set(key, { start: node.dlRange.start, end: node.dlRange.end, text: now });
      if (mode === "rich") node.dlEditor.setEditable(false);
      (node.dlWrap || node.dlBox).dataset.edited = "";
    }
    this.report();
  }

  /* Put the page's own element back where an unchanged block was. */
  restore(node) {
    if (node.dlEditor) { node.dlEditor.destroy(); node.dlEditor = null; }
    if (node.dlWrap) { node.dlWrap.remove(); node.dlWrap = null; }
    if (node.dlBox) { node.dlBox.remove(); node.dlBox = null; }
    node.hidden = false;
  }

  /* -------------------------------------------------------------- session */

  async discard() {
    await this.closeBlock();
    for (const node of this.blocks) this.restore(node);
    if (this.edits.size) this.changes += 1;
    this.edits.clear();
    this.report();
  }

  get unsaved() {
    return this.changes !== this.savedAt;
  }

  async stop() {
    await this.closeBlock();
    if (this.unsaved) {
      const ok = window.confirm(`${summary(this.edits.size)} They are not saved. `
        + "Stop editing and lose them? Press Cancel to keep editing, then press Open pull request.");
      if (!ok) return;
      await this.discard();
    }
    this.root.removeEventListener("click", this.onClick, true);
    document.body.classList.remove("dl-editing");
    $("dl-edit-toggle").textContent = "Edit this page";
    $("dl-edit-toggle").onclick = null;
    $("dl-edit-actions").hidden = true;
    this.say(this.pr ? `Your changes are saved as a draft pull request: ${this.pr.url}` : "");
    window.dlEditSession = null;
    window.dispatchEvent(new CustomEvent("dl-edit-stopped"));
  }

  async save() {
    await this.closeBlock();
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
