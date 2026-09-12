
import { createProseEditor } from "./vendor/milkdown.bundle.js";

const API = "https://api.github.com";
const TOKEN_KEY = "dewlab:editor:token";
const REPO = "deweydex/dewlab";

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
  const was = parseCells(before).map((cell) => cell.id).filter(Boolean);
  const now = parseCells(after).map((cell) => cell.id).filter(Boolean);
  return {
    added: now.filter((id) => !was.includes(id)),
    removed: was.filter((id) => !now.includes(id)),
  };
}

export function parseCells(body) {
  const cells = [];
  FENCE.lastIndex = 0;
  let match;
  while ((match = FENCE.exec(body)) !== null) {
    const info = match[1].trim();
    if (!/^(python|sql)\s+exec\b/.test(info)) continue;
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

export function restoreExecTag(markdown) {
  // Every exec-family fence keeps its tag on a round trip through the
  // Crepe-based authoring editor, which otherwise keeps only the first word
  // of a fence's info string (ARCHITECTURE.md §3, "The authoring editor").
  // `python exec`/`sql exec` recover from a lone `id:` header line; a site
  // editor or full-stack cell's `html`/`css`/`js` pane needs two header
  // lines — `id:` plus `site:` or `app:` — since the grouping key is what
  // a bare `html`/`css`/`js` fence would otherwise lose. Order between the
  // two header lines isn't fixed (build.py's parse_site_pane/parse_app_pane
  // read them as an unordered pair), so both orders are matched.
  const two = (key) => `(?=(?:id|${key}):\\s*\\S[^\\n]*\\n(?:id|${key}):\\s*\\S[^\\n]*\\n)`;
  return markdown
    .replace(/^```(python|sql)\n(?=id:\s*\S)/gm, "```$1 exec\n")
    .replace(new RegExp("^```(html|css|js)\\n" + two("site"), "gm"), "```$1 site\n")
    .replace(new RegExp("^```(html|css|js)\\n" + two("app"), "gm"), "```$1 app\n");
}

function withoutFences(body) {
  return body.replace(FENCE, (match) => match.replace(/[^\n]/g, " "));
}

export function headings(body) {
  return [...withoutFences(body).matchAll(/^(#{1,3})\s+(.+?)\s*$/gm)].map((m) => ({
    level: m[1].length,
    text: m[2],
  }));
}

export function slugifyHeading(text) {
  return text
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9\s_-]/g, "")
    .trim()
    .replace(/\s+/g, "-");
}

export function tutorialAnchors(body) {
  const cellIds = parseCells(body).map((cell) => cell.id).filter(Boolean);
  const headingIds = [...withoutFences(body).matchAll(/^#{1,6}\s+(.+?)\s*$/gm)]
    .map((m) => slugifyHeading(m[1]));
  return new Set([...cellIds, ...headingIds]);
}

export function findTutorialLinks(body) {
  const RE = /\]\(tutorial:([^)#\s]+)(?:#([^)\s]+))?\)/g;
  return [...body.matchAll(RE)].map((m) => ({ slug: m[1], anchor: m[2] || null }));
}

export function resolveTutorialLink(slug, ownModule, all) {
  const own = all.find((t) => t.module === ownModule && t.slug === slug);
  if (own) return { target: own };
  const elsewhere = all.filter((t) => t.slug === slug);
  if (elsewhere.length === 1) return { target: elsewhere[0] };
  if (elsewhere.length > 1) {
    return { ambiguous: [...new Set(elsewhere.map((t) => t.module))].sort() };
  }
  return {};
}

export function tutorialLinkProblems(body, ownModule, all) {
  const found = [];
  for (const { slug, anchor } of findTutorialLinks(body)) {
    const resolved = resolveTutorialLink(slug, ownModule, all);
    if (resolved.ambiguous) {
      found.push({ level: "error",
        text: `Link to "${slug}" is ambiguous — it exists in ${resolved.ambiguous.join(", ")}, `
            + "and not in this module. The build will fail on this." });
      continue;
    }
    if (!resolved.target) {
      found.push({ level: "error",
        text: `Link to "${slug}" does not match any tutorial. The build will fail on this.` });
      continue;
    }
    if (anchor && !resolved.target.anchors.has(anchor)) {
      found.push({ level: "error",
        text: `Link to "${slug}#${anchor}" — that tutorial has no heading or cell "${anchor}". `
            + "The build will fail on this." });
    }
  }
  return found;
}

export function matchTutorials(query, all) {
  const q = query.trim().toLowerCase();
  const ranked = all
    .map((t) => {
      if (!q) return { t, score: 0 };
      const title = t.title.toLowerCase();
      if (title.includes(q)) return { t, score: title.startsWith(q) ? 0 : 1 };
      if (t.slug.toLowerCase().includes(q) || t.module.toLowerCase().includes(q)) {
        return { t, score: 2 };
      }
      return null;
    })
    .filter(Boolean);
  ranked.sort((a, b) => a.score - b.score || a.t.title.localeCompare(b.t.title));
  return ranked.map((r) => r.t);
}

export function problems(body) {
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
  const was = parseCells(before);
  const now = parseCells(after);
  const gone = [];
  const nowIds = new Set(now.map((c) => c.id));
  for (const cell of was) {
    if (cell.id && !nowIds.has(cell.id)) gone.push(cell.id);
  }
  return gone;
}

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
      const blobs = [];
      for (const file of files) {
        if (file.text === null) {
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
    original: new Map(),
    base: null,
    editing: null,
    dirty: new Set(),
    removing: new Set(),
    editor: null,
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

  const READ_CONCURRENCY = 16;

  async function load() {
    status("Reading the repository…");
    const { base, paths } = await client.listTutorials();
    state.base = base;
    state.files.clear();
    state.original.clear();
    state.series.clear();
    state.dirty.clear();
    state.removing.clear();
    for (let i = 0; i < paths.length; i += READ_CONCURRENCY) {
      const batch = paths.slice(i, i + READ_CONCURRENCY);
      const texts = await Promise.all(batch.map((path) => client.read(path)));
      batch.forEach((path, j) => {
        state.files.set(path, texts[j]);
        state.original.set(path, texts[j]);
      });
      status(`Reading the repository… (${Math.min(i + READ_CONCURRENCY, paths.length)}/${paths.length})`);
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
        off: [],
      });
    }

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
    return `tutorials/${module}/${slug}/${slug}.md`;
  }

  function releasesOf(module, slug) {
    const folder = `tutorials/${module}/${slug}/`;
    const paths = [];
    for (const path of state.files.keys()) {
      if (!path.endsWith(".md") || !path.startsWith(folder)) continue;
      const name = path.slice(folder.length);
      if (name === `${slug}.md` || /^v\d[^/]*\.md$/.test(name)) paths.push(path);
    }
    return paths.sort((a, b) =>
      isNewer(versionOf(state.files.get(b)), versionOf(state.files.get(a))) ? 1 : -1);
  }

  function pathOf(module, slug) {
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

  function allTutorials() {
    const seen = new Set();
    const out = [];
    for (const path of state.files.keys()) {
      if (path.endsWith(".order.yaml") || !path.endsWith(".md")) continue;
      const meta = splitFrontmatter(state.files.get(path)).meta;
      const module = frontmatterField(meta, "module");
      const slug = frontmatterField(meta, "slug");
      const key = `${module}/${slug}`;
      if (!module || !slug || seen.has(key)) continue;
      seen.add(key);
      const current = state.files.get(pathOf(module, slug)) || "";
      const { meta: currentMeta, body } = splitFrontmatter(current);
      out.push({
        module, slug,
        title: frontmatterField(currentMeta, "title") || slug,
        anchors: tutorialAnchors(body),
      });
    }
    return out;
  }

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

  function release({ series, slug }) {
    const current = pathOf(series.module, slug);
    const edited = state.files.get(current) || "";
    const frozen = state.original.get(current);

    if (frozen === undefined) {
      status("This tutorial has never been committed, so there is nothing for a "
             + "student to go back to. Commit it first.", "error");
      return;
    }
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
    bumped = setFrontmatterField(bumped, "supersedes", was);

    state.files.set(current, frozen);
    state.dirty.delete(current);

    const frozenPath = `${folder}/v${was}.md`;
    if (frozenPath !== current) {
      state.files.set(frozenPath, frozen);
      state.dirty.add(frozenPath);
    }

    const currentPath = `${folder}/${slug}.md`;
    state.files.set(currentPath, `---\n${bumped}\n---\n\n${body}`);
    state.dirty.add(currentPath);
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

  function editorView({ series, slug }) {
    const path = pathOf(series.module, slug);
    const original = state.files.get(path) || "";
    const { meta, body } = splitFrontmatter(original);

    const mount = el("div", { class: "dl-editor-body" });
    const report = el("div", { class: "dl-editor-report", id: "dl-editor-report" });

    const linkQuery = el("input", {
      type: "text", class: "dl-editor-linkpicker-search",
      placeholder: "Search tutorials to link to…",
      "aria-label": "Search tutorials to link to",
      oninput: () => renderLinkResults(linkQuery.value),
    });
    const linkResults = el("div", { class: "dl-editor-linkpicker-results" });
    const linkPicker = el("div", { class: "dl-editor-linkpicker", hidden: "hidden" },
      linkQuery, linkResults);

    function insertTutorialLink(t, anchor) {
      const href = anchor ? `tutorial:${t.slug}#${anchor}` : `tutorial:${t.slug}`;
      state.editor.insertLink(t.title, href);
      applyEdit(state.editor.getMarkdown());
      linkPicker.hidden = true;
      linkQuery.value = "";
    }

    function renderLinkResults(query) {
      linkResults.replaceChildren();
      const matches = matchTutorials(query, allTutorials());
      if (!matches.length) {
        linkResults.append(el("p", { class: "dl-editor-linkpicker-empty" }, "No tutorials match."));
        return;
      }
      /* A handful, not the whole course — this is a search box, and a list
       * of everything defeats the point of one. */
      for (const t of matches.slice(0, 8)) {
        const anchors = [...t.anchors].sort();
        linkResults.append(el("div", { class: "dl-editor-linkpicker-row" },
          el("button", {
            type: "button", class: "dl-editor-linkpicker-pick",
            title: `Insert a link to ${t.title}`,
            onclick: () => insertTutorialLink(t),
          }, t.title, " ", el("span", { class: "dl-editor-linkpicker-where" }, `${t.module}/${t.slug}`)),
          anchors.length ? el("span", { class: "dl-editor-linkpicker-anchors" },
            ...anchors.map((a) => el("button", {
              type: "button", class: "dl-editor-linkpicker-anchor",
              title: `Link to "${a}" in ${t.title}`,
              onclick: () => insertTutorialLink(t, a),
            }, a))) : null,
        ));
      }
    }

    const linkToggle = el("button", {
      type: "button", class: "dl-editor-linkpicker-toggle",
      onclick: () => {
        linkPicker.hidden = !linkPicker.hidden;
        if (!linkPicker.hidden) { renderLinkResults(""); linkQuery.focus(); }
      },
    }, "Link to another tutorial");

    function check(next) {
      report.replaceChildren();
      const gone = renamedCells(body, next);
      if (gone.length) {
        report.append(el("p", { class: "dl-editor-danger" },
          `A cell id is the key a student's answers are saved under. These ids ` +
          `are no longer here: ${gone.join(", ")}. Committed as an edit, the ` +
          `answers in them are orphaned and those cells come back empty.`));
        report.append(el("p", { class: "dl-editor-danger" },
          `Released instead, nothing is orphaned: the ids stay in the release ` +
          `students are working in, and they stay there until they choose to move.`));
      }
      const allProblems = [...problems(next), ...tutorialLinkProblems(next, series.module, allTutorials())];
      for (const problem of allProblems) {
        report.append(el("p", { class: `dl-editor-${problem.level}` }, problem.text));
      }
      const committed = state.original.get(path);
      const released = committed !== undefined
        && versionOf(state.files.get(path)) !== versionOf(committed);
      const moved = committed === undefined || released
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

    function applyEdit(raw) {
      const next = restoreExecTag(raw);
      state.files.set(path, `---\n${meta}\n---\n\n${next}`);
      state.dirty.add(path);
      check(next);
    }

    state.editor = createProseEditor(mount, body, { onChange: applyEdit });
    state.editBody = applyEdit;
    check(body);

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
          onclick: async () => {
            const editor = state.editor;
            await editor.ready;
            if (editor !== state.editor) return; // a different tutorial opened meanwhile
            applyEdit(editor.getMarkdown());
            release({ series, slug });
          },
        }, "Release as a new version")),
      el("details", { class: "dl-editor-meta" },
        el("summary", {}, "Frontmatter"),
        el("pre", {}, meta)),
      linkToggle,
      linkPicker,
      mount,
      report);
  }

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

  function render() {
    if (state.editor) {
      state.editor.destroy();
      state.editor = null;
      state.editBody = null;
    }
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

  function getBody() {
    if (!state.editing) return "";
    const path = pathOf(state.editing.series.module, state.editing.slug);
    return splitFrontmatter(state.files.get(path) || "").body;
  }

  function setBody(markdown) {
    if (!state.editing) return;
    const path = pathOf(state.editing.series.module, state.editing.slug);
    const { meta } = splitFrontmatter(state.files.get(path) || "");
    state.files.set(path, `---\n${meta}\n---\n\n${markdown}`);
    state.dirty.add(path);
    render();
  }

  function editBody(markdown) {
    if (state.editBody) state.editBody(markdown);
  }

  globalThis.dewlabEditor = {
    state, load, save, render, move, insert, setStatus, setFrontmatterField,
    release, pathOf, releasesOf, getBody, setBody, editBody,
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
