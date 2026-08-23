/* The editor: reorder a series, insert a tutorial, create one, and edit what
 * is inside it — against the repository, through the GitHub API, committed to
 * a branch and opened as a pull request.
 *
 * It edits *source*, not the built site. Everything here reads and writes the
 * markdown in tutorials/ and the order file beside it, because that is what a
 * person actually changes; site/ is a derived artefact and editing it would be
 * editing the output of a build.
 *
 * Never linked from a student page. It is for authors and course maintainers.
 */

const API = "https://api.github.com";
const TOKEN_KEY = "dewlab:editor:token";
const REPO = "deweydex/dewlab";

/* ------------------------------------------------------------------ parsing
 *
 * The build decides what a cell is by finding ```python exec fences and
 * reading the `id:` line inside. The editor has to agree with it exactly,
 * because a disagreement here is an editor that shows you something the build
 * will not produce. Kept as pure functions so the tests can drive them without
 * a network or a token.
 */

const FENCE = /^ *```([^\n]*)\n([\s\S]*?)^ *```[ \t]*$/gm;

export function splitFrontmatter(text) {
  if (!text.startsWith("---")) return { meta: "", body: text };
  const end = text.indexOf("\n---", 3);
  if (end === -1) return { meta: "", body: text };
  return { meta: text.slice(3, end).trim(), body: text.slice(end + 4).replace(/^\n+/, "") };
}

export function frontmatterField(meta, field) {
  const line = meta.split("\n").find((l) => l.startsWith(field + ":"));
  if (!line) return "";
  return line.slice(field.length + 1).trim().replace(/^"(.*)"$/, "$1");
}

export const STATUSES = ["draft", "beta", "live", "archived"];

export function setFrontmatterField(meta, field, value) {
  /* Set a field, or add it if it is not there. Added after `version:` rather
   * than at the end, because the end of the frontmatter is where `covers:`
   * lives and its indented children would swallow anything put below them. */
  const lines = meta.split("\n");
  const at = lines.findIndex((l) => l.startsWith(field + ":"));
  if (at !== -1) {
    lines[at] = `${field}: ${value}`;
    return lines.join("\n");
  }
  const after = lines.findIndex((l) => l.startsWith("version:"));
  const where = after === -1 ? lines.length - 1 : after;
  lines.splice(where + 1, 0, `${field}: ${value}`);
  return lines.join("\n");
}

export function statusOf(text) {
  return frontmatterField(splitFrontmatter(text).meta, "status") || "live";
}

export function versionOf(text) {
  return frontmatterField(splitFrontmatter(text).meta, "version");
}

/* ------------------------------------------------------------------ releases
 *
 * A version is a release, not a save. It exists when we decide a student
 * should be able to go back to the old one; everything else is an edit
 * (planning/VERSIONS.md). So the editor never bumps a version on its own — it
 * offers, and releasing is a separate gesture from committing an edit.
 */

export const VERSION_RE = /^(\d{4})\.(\d{2})\.(\d{2})\.(\d+)$/;

export function releaseOrder(version) {
  /* The four numbers, so 2026.09.02.1 sorts before 2026.09.15.1 rather than
   * after it — which it would as a string, the first time it ever mattered. */
  const found = VERSION_RE.exec(String(version || ""));
  return found ? found.slice(1, 5).map(Number) : [0, 0, 0, 0];
}

export function isNewer(a, b) {
  const left = releaseOrder(a);
  const right = releaseOrder(b);
  for (let i = 0; i < 4; i += 1) {
    if (left[i] !== right[i]) return left[i] > right[i];
  }
  return false;
}

export function nextVersion(existing, today = new Date()) {
  /* Today where you are, from the browser's own clock: a release at half past
   * midnight in Dublin should carry the date the author's local clock reports,
   * not the date UTC thinks it is.
   *
   * The trailing number is computed rather than typed. It earns its place
   * rarely — you publish, spot something, and publish again — but that is
   * exactly the case that would otherwise collide. */
  const stem = [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, "0"),
    String(today.getDate()).padStart(2, "0"),
  ].join(".");
  const taken = existing
    .map((version) => VERSION_RE.exec(String(version || "")))
    .filter((found) => found && found.slice(1, 4).join(".") === stem)
    .map((found) => Number(found[4]));
  return `${stem}.${taken.length ? Math.max(...taken) + 1 : 1}`;
}

export function cellsChanged(before, after) {
  /* What tells an edit from a release. Prose moving is an edit; a cell
   * appearing, disappearing or changing its id is the kind of change a student
   * might want to go back from.
   *
   * A rename shows up here as one gone and one arrived, which is the truth:
   * to a student's saved work they are two different exercises. */
  const was = parseCells(before).map((cell) => cell.id).filter(Boolean);
  const now = parseCells(after).map((cell) => cell.id).filter(Boolean);
  return {
    added: now.filter((id) => !was.includes(id)),
    removed: was.filter((id) => !now.includes(id)),
  };
}

export function parseCells(body) {
  /* Every exec-tagged fence, with the id the build will key saved work on.
   * An untagged fence is illustrative code and is not a cell, which is the
   * same rule build.py applies. */
  const cells = [];
  FENCE.lastIndex = 0;
  let match;
  while ((match = FENCE.exec(body)) !== null) {
    const info = match[1].trim();
    if (!/^python\s+exec\b/.test(info)) continue;
    const lines = match[2].split("\n");
    let id = "";
    let hint = "";
    let start = 0;
    for (; start < lines.length; start += 1) {
      const header = /^\s*(id|hint)\s*:\s*(.*)$/.exec(lines[start]);
      if (!header) break;
      if (header[1] === "id") id = header[2].trim();
      else hint = header[2].trim();
    }
    cells.push({
      id,
      hint,
      code: lines.slice(start).join("\n").replace(/\n+$/, ""),
      at: match.index,
      length: match[0].length,
    });
  }
  return cells;
}

export function headings(body) {
  return [...body.matchAll(/^(#{1,3})\s+(.+?)\s*$/gm)].map((m) => ({
    level: m[1].length,
    text: m[2],
  }));
}

export function problems(body) {
  /* What the build would refuse, found before the commit rather than after.
   * This is the whole justification for not shipping a visual preview: the
   * mistakes that actually happen are structural, and structure is the part a
   * browser can check honestly. */
  const found = [];
  const cells = parseCells(body);
  const seen = new Map();
  for (const cell of cells) {
    if (!cell.id) {
      found.push({ level: "error", text: "A runnable cell has no id: line. The build stops on this." });
      continue;
    }
    if (!/^[a-z0-9-]+$/.test(cell.id)) {
      found.push({ level: "error", text: `Cell id "${cell.id}" is not lowercase letters, digits and hyphens.` });
    }
    seen.set(cell.id, (seen.get(cell.id) || 0) + 1);
  }
  for (const [id, count] of seen) {
    if (count > 1) {
      found.push({ level: "error", text: `Cell id "${id}" is used ${count} times. Ids must be unique in a page.` });
    }
  }
  const fences = (body.match(/^ *```/gm) || []).length;
  if (fences % 2 !== 0) {
    found.push({ level: "error", text: "A code fence is opened and never closed." });
  }
  if (!headings(body).some((h) => h.level === 1)) {
    found.push({ level: "warn", text: "No level-one heading. The page will have no title on it." });
  }
  return found;
}

export function renamedCells(before, after) {
  /* A cell's id is the key a student's saved work is stored under. Renaming
   * one does not move their work: it orphans it, and the cell comes back
   * empty. Nothing in the build can warn about this, because by then the
   * rename has happened — so the editor has to, while both versions exist. */
  const was = parseCells(before);
  const now = parseCells(after);
  const gone = [];
  const nowIds = new Set(now.map((c) => c.id));
  for (const cell of was) {
    if (cell.id && !nowIds.has(cell.id)) gone.push(cell.id);
  }
  return gone;
}

/* --------------------------------------------------------------- the client
 *
 * Swappable so the browser tests can drive the whole editor without a token
 * or a network. `start()` takes one, and the page passes the real one.
 */

export function githubClient(token) {
  async function call(path, options = {}) {
    const response = await fetch(API + path, {
      ...options,
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${token}`,
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...(options.headers || {}),
      },
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(`GitHub said ${response.status}: ${detail.slice(0, 300)}`);
    }
    return response.status === 204 ? null : response.json();
  }

  return {
    async listTutorials() {
      const head = await call(`/repos/${REPO}/git/ref/heads/main`);
      const tree = await call(`/repos/${REPO}/git/trees/${head.object.sha}?recursive=1`);
      return {
        base: head.object.sha,
        paths: tree.tree
          .filter((e) => e.type === "blob" && e.path.startsWith("tutorials/"))
          .map((e) => e.path),
      };
    },
    async read(path) {
      const file = await call(`/repos/${REPO}/contents/${encodeURI(path)}?ref=main`);
      return decodeURIComponent(escape(atob(file.content.replace(/\n/g, ""))));
    },
    async commit({ base, branch, message, files }) {
      /* One commit for the whole change, through the git data API, rather than
       * one commit per file through the contents API. An insertion touches a
       * markdown file and an order file, and those two arriving separately
       * would leave main briefly describing a series that does not exist. */
      const blobs = [];
      for (const file of files) {
        if (file.text === null) {
          /* A null sha in a tree entry removes the path. This is how a release
           * moves a single-file tutorial into a folder of releases without the
           * old path surviving beside the new ones. */
          blobs.push({ path: file.path, mode: "100644", type: "blob", sha: null });
          continue;
        }
        const blob = await call(`/repos/${REPO}/git/blobs`, {
          method: "POST",
          body: JSON.stringify({ content: file.text, encoding: "utf-8" }),
        });
        blobs.push({ path: file.path, mode: "100644", type: "blob", sha: blob.sha });
      }
      const tree = await call(`/repos/${REPO}/git/trees`, {
        method: "POST",
        body: JSON.stringify({ base_tree: base, tree: blobs }),
      });
      const created = await call(`/repos/${REPO}/git/commits`, {
        method: "POST",
        body: JSON.stringify({ message, tree: tree.sha, parents: [base] }),
      });
      await call(`/repos/${REPO}/git/refs`, {
        method: "POST",
        body: JSON.stringify({ ref: `refs/heads/${branch}`, sha: created.sha }),
      });
      const pull = await call(`/repos/${REPO}/pulls`, {
        method: "POST",
        body: JSON.stringify({
          title: message.split("\n")[0],
          head: branch,
          base: "main",
          draft: true,
          body: `Written from the dewlab editor.\n\n${message}`,
        }),
      });
      return pull.html_url;
    },
  };
}

/* ------------------------------------------------------------------ the page */

/* What each one does, in the tooltip, because four words on four buttons is
 * not enough to tell draft from beta and the difference matters. */
const STATUS_MEANS = {
  draft: "Not published at all. No page is built, so nobody can reach it.",
  beta: "Published but not on the course. Anyone with the link can read it; "
      + "students are not sent to it.",
  live: "On the course, in the reading order.",
  archived: "Was on the course, is not now. Stays readable, keeps saved work.",
};

const TEMPLATE = `---
title: "{title}"
slug: {slug}
module: {module}
module_title: "{module_title}"
year: "{year}"
series: {series}
version: 1
---

# {title}

Write the opening here — what this tutorial is for, and why it comes after the
one before it.

## A first section

\`\`\`python exec
id: a-first-section-1
# The first thing a student runs.
\`\`\`

## Reflection

What surprised you here, and what would you like to understand better?
`;

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (value !== null && value !== undefined) node.setAttribute(key, value);
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child.nodeType ? child : document.createTextNode(String(child)));
  }
  return node;
}

function slugify(title) {
  return title.toLowerCase().replace(/[^\w\s-]/g, "").trim().replace(/[\s_]+/g, "-");
}

export function start(root, client, { onStatus = () => {} } = {}) {
  const state = {
    series: new Map(),
    files: new Map(),
    /* The same files as fetched, never edited. Releasing needs both: the
     * frozen copy has to be what students have now, and the buffer is what
     * they are about to get. Without this the release would freeze the edits
     * it exists to let them go back from. */
    original: new Map(),
    base: null,
    editing: null,
    dirty: new Set(),
    /* Paths to delete in the next commit. A release moves a single-file
     * tutorial into a folder, which is the only thing here that removes a
     * file rather than writing one. */
    removing: new Set(),
  };

  function status(text, kind = "note") {
    onStatus(text, kind);
    const bar = document.getElementById("dl-editor-status");
    if (bar) {
      bar.textContent = text;
      bar.dataset.kind = kind;
      bar.hidden = !text;
    }
  }

  async function load() {
    status("Reading the repository…");
    const { base, paths } = await client.listTutorials();
    state.base = base;
    state.files.clear();
    state.original.clear();
    state.series.clear();
    state.dirty.clear();
    state.removing.clear();
    for (const path of paths) {
      const text = await client.read(path);
      state.files.set(path, text);
      state.original.set(path, text);
    }
    for (const [path, text] of state.files) {
      if (!path.endsWith(".order.yaml")) continue;
      const module = path.split("/")[1];
      const name = path.split("/").pop().replace(".order.yaml", "");
      const order = [...text.matchAll(/^ *- +(\S+)\s*$/gm)].map((m) => m[1]);
      const titled = /^series:\s*(.+)$/m.exec(text);
      state.series.set(path, {
        path, module, name, order,
        title: titled ? titled[1].trim() : name,
        /* Everything belonging to this series, whether or not it is on the
         * route. Without this, setting a tutorial to draft would drop it out
         * of the order file and out of the list at once — a one-way trip, with
         * no way back to it in the editor. */
        off: [],
      });
    }

    /* One entry per tutorial, not per file. A tutorial with more than one
     * release is a folder of them, and reading each file as its own tutorial
     * would list the same thing three times and let an edit to one of them
     * look like an edit to the tutorial. */
    for (const series of state.series.values()) series.off = [];
    const seen = new Set();
    for (const [path, text] of state.files) {
      if (path.endsWith(".order.yaml") || !path.endsWith(".md")) continue;
      const meta = splitFrontmatter(text).meta;
      const module = frontmatterField(meta, "module");
      const slug = frontmatterField(meta, "slug");
      if (seen.has(`${module}/${slug}`)) continue;
      seen.add(`${module}/${slug}`);
      const series = [...state.series.values()].find(
        (s) => s.module === module && !s.order.includes(slug)
          && frontmatterField(meta, "series") === s.name
      );
      if (series) series.off.push(slug);
    }
    status("");
    render();
  }

  function newPathOf(module, slug) {
    /* Where a tutorial is created. Always a single file: a folder is what a
     * tutorial becomes when it has a second release, and most never do. */
    return `tutorials/${module}/${slug}.md`;
  }

  function releasesOf(module, slug) {
    /* Every file that is a release of this tutorial, newest first. One while
     * it is a single file, several once it is a folder. */
    const single = `tutorials/${module}/${slug}.md`;
    const folder = `tutorials/${module}/${slug}/`;
    const paths = [];
    for (const path of state.files.keys()) {
      if (!path.endsWith(".md")) continue;
      if (path === single || (path.startsWith(folder) && !path.slice(folder.length).includes("/"))) {
        paths.push(path);
      }
    }
    return paths.sort((a, b) =>
      isNewer(versionOf(state.files.get(b)), versionOf(state.files.get(a))) ? 1 : -1);
  }

  function pathOf(module, slug) {
    /* The release the plain URL serves, which is the one to open and the one a
     * status change applies to: the newest live one, matching what
     * `versions_of` decides in build.py. Nothing live falls back to the newest
     * of whatever there is, for the same reason the build does — a tutorial
     * that is entirely beta or entirely archived still has to open.
     *
     * This used to be `tutorials/<module>/<slug>.md` and nothing else, so a
     * tutorial with a second release opened as an empty buffer. */
    const paths = releasesOf(module, slug);
    if (paths.length <= 1) return paths[0] || newPathOf(module, slug);
    const live = paths.filter((path) => statusOf(state.files.get(path)) === "live");
    return (live.length ? live : paths)[0];
  }

  function titleOf(module, slug) {
    const text = state.files.get(pathOf(module, slug));
    if (!text) return slug;
    return frontmatterField(splitFrontmatter(text).meta, "title") || slug;
  }

  /* ------------------------------------------------------------ the list view */

  function move(series, from, to) {
    if (to < 0 || to >= series.order.length || from === to) return;
    const moved = series.order.splice(from, 1)[0];
    series.order.splice(to, 0, moved);
    state.dirty.add(series.path);
    render();
  }

  function insert(series, at) {
    const title = prompt("What is the new tutorial called?");
    if (!title) return;
    const slug = slugify(title);
    if (series.order.includes(slug)) {
      status(`This series already has a ${slug}.`, "error");
      return;
    }
    const sibling = state.files.get(pathOf(series.module, series.order[0])) || "";
    const meta = splitFrontmatter(sibling).meta;
    const body = TEMPLATE
      .replaceAll("{title}", title)
      .replaceAll("{slug}", slug)
      .replaceAll("{module}", series.module)
      .replaceAll("{module_title}", frontmatterField(meta, "module_title") || series.module)
      .replaceAll("{year}", frontmatterField(meta, "year") || "2026-2027")
      .replaceAll("{series}", frontmatterField(meta, "series") || series.name);
    state.files.set(newPathOf(series.module, slug), body);
    series.order.splice(at, 0, slug);
    state.dirty.add(series.path);
    state.dirty.add(newPathOf(series.module, slug));
    render();
  }

  function setStatus(series, slug, status) {
    /* One gesture, two files. A status change is not just a frontmatter edit:
     * only a live tutorial is on the reading order, and the build refuses an
     * order file that lists anything else — so the line has to move with the
     * field or the next build stops. Doing that by hand is the part worth
     * automating; the field on its own is trivial. */
    const path = pathOf(series.module, slug);
    const text = state.files.get(path);
    if (!text) return;
    const { meta, body } = splitFrontmatter(text);
    state.files.set(path, `---\n${setFrontmatterField(meta, "status", status)}\n---\n\n${body}`);
    state.dirty.add(path);

    const at = series.order.indexOf(slug);
    const off = series.off.indexOf(slug);
    if (status === "live" && at === -1) {
      series.order.push(slug);
      if (off !== -1) series.off.splice(off, 1);
      state.dirty.add(series.path);
    } else if (status !== "live" && at !== -1) {
      series.order.splice(at, 1);
      if (off === -1) series.off.push(slug);
      state.dirty.add(series.path);
    }
    render();
  }

  /* ---------------------------------------------------------------- release
   *
   * The one gesture that says "a student should be able to go back to what
   * they had". Everything else the editor does is an edit.
   *
   * It freezes the release students currently have and publishes the buffer as
   * a new one dated today. Both stay live: the build serves the newest live
   * release at the plain URL, so the new one becomes what a reader gets and
   * the old one keeps answering its own link and holding the work saved
   * against it.
   */
  function release({ series, slug }) {
    const current = pathOf(series.module, slug);
    const edited = state.files.get(current) || "";
    const frozen = state.original.get(current);

    if (frozen === undefined) {
      status("This tutorial has never been committed, so there is nothing for a "
             + "student to go back to. Commit it first.", "error");
      return;
    }
    /* Both copies, and for different reasons. The frozen one must be live or
     * there is nothing students have to go back to; the buffer must be live or
     * this commit is carrying two intentions at once — taking a tutorial off
     * the course and publishing a new release of it. */
    if (statusOf(frozen) !== "live" || statusOf(edited) !== "live") {
      status("Only a live tutorial is released. A draft has no page to go back "
             + "to, a beta becomes live with the status control rather than by "
             + "being released, and taking one off the course is a separate "
             + "gesture from publishing a new release of it.", "error");
      return;
    }
    if (edited === frozen) {
      status("Nothing has changed, so the new release would be identical to the "
             + "one students already have.", "error");
      return;
    }

    const family = releasesOf(series.module, slug);
    const next = nextVersion(family.map((path) => versionOf(state.files.get(path))));
    const was = versionOf(frozen);
    const folder = `tutorials/${series.module}/${slug}`;

    const { meta, body } = splitFrontmatter(edited);
    let bumped = setFrontmatterField(meta, "version", next);
    /* Lineage, for the "what changed" note. Optional to the build and worth
     * writing, because after two releases nothing else says which one this
     * replaced. */
    bumped = setFrontmatterField(bumped, "supersedes", was);

    if (current === `${folder}.md`) {
      /* A tutorial becomes a folder the moment it has a second release, and
       * not before. Most never do. */
      state.files.delete(current);
      state.dirty.delete(current);
      state.removing.add(current);
      state.files.set(`${folder}/v${was}.md`, frozen);
      state.dirty.add(`${folder}/v${was}.md`);
    } else {
      /* Already a folder. The file being edited is the release students have,
       * so it goes back to exactly that — the edits are the new release, not a
       * revision of the old one. Without this the frozen copy would carry the
       * changes it exists to let them go back from. */
      state.files.set(current, frozen);
      state.dirty.delete(current);
    }

    state.files.set(`${folder}/v${next}.md`, `---\n${bumped}\n---\n\n${body}`);
    state.dirty.add(`${folder}/v${next}.md`);
    render();
    status(`Released as ${next}. The ${was} release is frozen where it is, and a `
           + "reader who worked in it stays there until they choose otherwise. "
           + "Commit to publish.", "done");
  }

  function statusControl(series, slug) {
    const now = statusOf(state.files.get(pathOf(series.module, slug)) || "");
    return el("span", { class: "dl-editor-status", "data-status": now },
      ...STATUSES.map((status) => el("button", {
        type: "button",
        class: "dl-editor-status-option",
        "data-status": status,
        "aria-pressed": String(status === now),
        title: STATUS_MEANS[status],
        onclick: () => setStatus(series, slug, status),
      }, status)));
  }

  function seriesView(series) {
    const list = el("ol", { class: "dl-editor-list", "data-series": series.name });
    series.order.forEach((slug, index) => {
      const card = el("li", {
        class: "dl-editor-card", draggable: "true", "data-slug": slug, "data-index": index,
        ondragstart: (ev) => { ev.dataTransfer.setData("text/plain", String(index)); },
        ondragover: (ev) => ev.preventDefault(),
        ondrop: (ev) => {
          ev.preventDefault();
          move(series, Number(ev.dataTransfer.getData("text/plain")), index);
        },
      },
        el("span", { class: "dl-editor-pos" }, index + 1),
        el("button", {
          class: "dl-editor-open", type: "button",
          onclick: () => { state.editing = { series, slug }; render(); },
        }, titleOf(series.module, slug)),
        statusControl(series, slug),
        el("span", { class: "dl-editor-moves" },
          el("button", { type: "button", class: "dl-editor-up", "aria-label": `Move ${slug} earlier`,
                         onclick: () => move(series, index, index - 1) }, "↑"),
          el("button", { type: "button", class: "dl-editor-down", "aria-label": `Move ${slug} later`,
                         onclick: () => move(series, index, index + 1) }, "↓"),
        ),
      );
      list.append(
        el("li", { class: "dl-editor-gap" },
          el("button", { type: "button", onclick: () => insert(series, index) }, "insert here")),
        card,
      );
    });
    list.append(
      el("li", { class: "dl-editor-gap" },
        el("button", { type: "button", class: "dl-editor-new",
                       onclick: () => insert(series, series.order.length) }, "new tutorial at the end")),
    );
    /* Off the route but still here: drafts, betas, and anything archived. They
     * have no position, so they carry no number and no move arrows — only what
     * they are, and the way back to live. */
    for (const slug of series.off) {
      list.append(el("li", { class: "dl-editor-card dl-editor-off", "data-slug": slug },
        el("span", { class: "dl-editor-pos" }, "—"),
        el("button", {
          class: "dl-editor-open", type: "button",
          onclick: () => { state.editing = { series, slug }; render(); },
        }, titleOf(series.module, slug)),
        statusControl(series, slug),
      ));
    }
    return el("section", { class: "dl-editor-series" },
      el("h2", {}, series.title),
      el("p", { class: "dl-editor-where" }, series.path),
      list);
  }

  /* ------------------------------------------------------- the tutorial view */

  function editorView({ series, slug }) {
    const path = pathOf(series.module, slug);
    const original = state.files.get(path) || "";
    const { meta, body } = splitFrontmatter(original);

    const area = el("textarea", { class: "dl-editor-body", spellcheck: "true", rows: "28" });
    area.value = body;

    const report = el("div", { class: "dl-editor-report", id: "dl-editor-report" });

    function check() {
      const next = area.value;
      report.replaceChildren();
      const gone = renamedCells(body, next);
      if (gone.length) {
        /* This used to say the work was thrown away, which stopped being true
         * when releases arrived and made it contradict the proposal below it.
         * Committed as an edit it is still true; released, the old cells are
         * still there in the release students are working in. Saying both,
         * once, is what stops the two messages arguing. */
        report.append(el("p", { class: "dl-editor-danger" },
          `A cell id is the key a student's answers are saved under. These ids ` +
          `are no longer here: ${gone.join(", ")}. Committed as an edit, the ` +
          `answers in them are orphaned and those cells come back empty.`));
        report.append(el("p", { class: "dl-editor-danger" },
          `Released instead, nothing is orphaned: the ids stay in the release ` +
          `students are working in, and they stay there until they choose to move.`));
      }
      for (const problem of problems(next)) {
        report.append(el("p", { class: `dl-editor-${problem.level}` }, problem.text));
      }
      /* The proposal. The editor knows what changed since the last release and
       * says so; it does not bump anything on its own, because a version per
       * save is the thing the whole design rejects. When only prose moved it
       * stays quiet — that is an edit and it needs no ceremony.
       *
       * A file with nothing committed behind it has no last release to compare
       * with. That is a tutorial just created, or the release just made — and
       * without this guard the release you have this second announces that
       * every cell in it is new. */
      const committed = state.original.get(path);
      const moved = committed === undefined
        ? { added: [], removed: [] }
        : cellsChanged(splitFrontmatter(committed).body, next);
      if (moved.added.length || moved.removed.length) {
        const said = [];
        if (moved.added.length) said.push(`${moved.added.length} new`);
        if (moved.removed.length) said.push(`${moved.removed.length} gone`);
        report.append(el("p", { class: "dl-editor-warn" },
          `The cells have changed since the last release — ${said.join(", ")}. ` +
          "That is usually a release rather than an edit: releasing keeps the " +
          "version students are working in and puts this one beside it."));
      }

      const cells = parseCells(next);
      report.append(el("p", { class: "dl-editor-structure" },
        `${cells.length} runnable cell${cells.length === 1 ? "" : "s"}, ` +
        `${headings(next).length} headings. ` +
        `This is what the build will see — it is not a picture of the page.`));
    }

    area.addEventListener("input", () => {
      state.files.set(path, `---\n${meta}\n---\n\n${area.value}`);
      state.dirty.add(path);
      check();
    });
    check();

    const releases = releasesOf(series.module, slug);
    const version = versionOf(original);

    return el("section", { class: "dl-editor-one" },
      el("p", {},
        el("button", { type: "button", class: "dl-editor-back",
                       onclick: () => { state.editing = null; render(); } }, "← all tutorials")),
      el("h2", {}, frontmatterField(meta, "title") || slug),
      el("p", { class: "dl-editor-where" }, path),
      el("p", { class: "dl-editor-release" },
        el("span", { class: "dl-editor-version" },
           releases.length > 1
             ? `Release ${version}, the newest of ${releases.length}`
             : `Release ${version}, the only one`),
        el("button", {
          type: "button", class: "dl-editor-release-btn", id: "dl-editor-release",
          title: "Freeze the release students have and publish this as a new "
               + "one, dated today. Their saved answers move with them.",
          onclick: () => release({ series, slug }),
        }, "Release as a new version")),
      el("details", { class: "dl-editor-meta" },
        el("summary", {}, "Frontmatter"),
        el("pre", {}, meta)),
      area,
      report);
  }

  /* ------------------------------------------------------------- committing */

  function orderText(series) {
    const original = state.files.get(series.path) || "";
    const head = original.split(/^order:/m)[0];
    return `${head}order:\n${series.order.map((s) => `  - ${s}\n`).join("")}`;
  }

  function pending() {
    return state.dirty.size + state.removing.size;
  }

  async function save() {
    if (!pending()) {
      status("Nothing has changed.", "note");
      return;
    }
    const message = prompt("What did you change? (this becomes the commit message)");
    if (!message) return;
    const files = [];
    for (const path of state.dirty) {
      const series = state.series.get(path);
      files.push({ path, text: series ? orderText(series) : state.files.get(path) });
    }
    /* A release moves a single-file tutorial into a folder, which is the only
     * thing here that removes a file. It has to travel in the same commit as
     * the two files replacing it, or main briefly has a tutorial with no
     * releases in it. */
    for (const path of state.removing) files.push({ path, text: null });
    status(`Committing ${files.length} file${files.length === 1 ? "" : "s"}…`);
    try {
      const branch = `editor/${slugify(message).slice(0, 40)}-${Date.now().toString(36)}`;
      const url = await client.commit({ base: state.base, branch, message, files });
      state.dirty.clear();
      state.removing.clear();
      /* Render first: it rebuilds the status bar, so setting the message
       * before it would write into an element about to be thrown away. */
      render();
      status(`Opened ${url}`, "done");
    } catch (error) {
      status(String(error.message || error), "error");
    }
  }

  /* ------------------------------------------------------------------ render */

  function render() {
    root.replaceChildren();
    root.append(
      el("div", { class: "dl-editor-bar" },
        el("button", { type: "button", id: "dl-editor-save", onclick: save,
                       disabled: pending() ? null : "disabled" },
           pending() ? `Commit ${pending()} change${pending() === 1 ? "" : "s"}` : "Nothing to commit"),
        el("button", { type: "button", id: "dl-editor-forget", onclick: () => {
          try { localStorage.removeItem(TOKEN_KEY); } catch (e) { /* blocked storage */ }
          location.reload();
        } }, "Forget my token"),
      ),
      el("div", { class: "dl-editor-status", id: "dl-editor-status", role: "status", hidden: "hidden" }),
    );
    if (state.editing) root.append(editorView(state.editing));
    /* By the name shown, not the filename behind it. Sorting a visible list on
     * an invisible key puts things in an order nobody can predict. */
    else for (const series of [...state.series.values()].sort((a, b) => a.title.localeCompare(b.title))) {
      root.append(seriesView(series));
    }
  }

  globalThis.dewlabEditor = {
    state, load, save, render, move, insert, setStatus, setFrontmatterField,
    release, pathOf, releasesOf,
  };
  return load();
}

/* The token gate. Kept separate from start() so the tests can drive the editor
 * without one, and so the trade is stated where somebody has to read it. */
export function gate(root) {
  let token = null;
  try { token = localStorage.getItem(TOKEN_KEY); } catch (e) { /* blocked storage */ }
  if (token) return start(root, githubClient(token));

  const field = el("input", { type: "password", id: "dl-editor-token",
                              placeholder: "github_pat_…", autocomplete: "off" });
  root.replaceChildren(el("form", {
    class: "dl-editor-gate",
    onsubmit: (ev) => {
      ev.preventDefault();
      if (!field.value.trim()) return;
      try { localStorage.setItem(TOKEN_KEY, field.value.trim()); } catch (e) { /* blocked storage */ }
      start(root, githubClient(field.value.trim()));
    },
  },
    el("p", {}, "This page edits the repository directly. It needs a GitHub " +
                "fine-grained token with contents and pull-request write on " +
                REPO + ", and nothing else."),
    el("p", { class: "dl-editor-warn" },
      "The token is kept in this browser's local storage. On your own machine " +
      "that is a fair trade; on a shared one it is not. There is a button to " +
      "forget it, and this page is never linked from anywhere students go."),
    field,
    el("button", { type: "submit" }, "Start editing"),
  ));
}

if (typeof document !== "undefined" && document.getElementById("dl-editor")) {
  gate(document.getElementById("dl-editor"));
}
