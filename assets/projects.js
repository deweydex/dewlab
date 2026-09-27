/* Choose your project (DECISIONS_LOG 7.288). A page offers two to four
 * projects that use one idea in different ways, and the reader picks one.
 * The build writes the cards and the comparison table before the first
 * project, and gives each project an anchor (build.py, place_projects()).
 * This file closes the projects, so nobody scrolls past the first one to
 * reach the third, and opens the one a card or a table row points at.
 *
 * Without JavaScript nothing here runs: every project is open and each
 * card is a plain link to its project.
 *
 * Each project's own `## ` heading becomes its open-and-close button, so
 * the heading, its anchor, the page's contents list and `covers:` keys
 * all stay as they were. */

const KEY_PREFIX = "dewlab:projects:";

function readOpened(pageId) {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY_PREFIX + pageId) || "[]");
    return new Set(Array.isArray(saved) ? saved : []);
  } catch {
    return new Set();
  }
}

function writeOpened(pageId, opened) {
  try {
    localStorage.setItem(KEY_PREFIX + pageId, JSON.stringify([...opened]));
  } catch {
    /* Storage refused: the choice lasts until the page closes. */
  }
}

/* A project the reader has run a cell in: its cells count towards
 * progress, and it opens when the page loads. */
export function projectStarted(section) {
  return [...section.querySelectorAll(".dl-output")].some((output) => output.innerHTML.trim());
}

/* The project an element sits in, if any. */
export function projectOf(element) {
  return element.closest(".dl-project[data-project]");
}

/* Opened, or started: the project is part of what the reader is doing. */
export function projectInPlay(section) {
  return !section.classList.contains("dl-project-closed") || projectStarted(section);
}

export function initProjects({ pageId, onChange = () => {} }) {
  const sections = [...document.querySelectorAll("#dl-body .dl-project[data-project]")];
  if (!sections.length) return;
  const opened = readOpened(pageId);

  function setOpen(section, open, { remember = true } = {}) {
    section.classList.toggle("dl-project-closed", !open);
    const toggle = section.querySelector(".dl-project-toggle");
    if (toggle) toggle.setAttribute("aria-expanded", String(open));
    if (remember) {
      if (open) opened.add(section.dataset.project);
      else opened.delete(section.dataset.project);
      writeOpened(pageId, opened);
    }
    onChange();
  }

  function openAndGo(section) {
    setOpen(section, true);
    section.scrollIntoView({ block: "start", behavior: "smooth" });
    const toggle = section.querySelector(".dl-project-toggle");
    if (toggle) toggle.focus({ preventScroll: true });
    history.replaceState(null, "", `#${section.id}`);
  }

  for (const section of sections) {
    const head = section.querySelector(":scope > h2");
    if (head) {
      head.classList.add("dl-project-head");
      const toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = "dl-project-toggle";
      toggle.setAttribute("aria-controls", section.id);
      toggle.append(...head.childNodes);
      head.append(toggle);
      toggle.addEventListener("click", () => {
        setOpen(section, section.classList.contains("dl-project-closed"));
      });
    }
    const back = document.createElement("p");
    back.className = "dl-project-back";
    const link = document.createElement("a");
    link.href = "#dl-project-chooser";
    link.textContent = "Try another project";
    back.append(link);
    section.append(back);

    // Open if the reader opened it before or has already worked in it.
    const open = opened.has(section.dataset.project) || projectStarted(section);
    setOpen(section, open, { remember: false });
  }

  for (const link of document.querySelectorAll(".dl-project-chooser a[data-project]")) {
    link.addEventListener("click", (ev) => {
      const section = document.getElementById(`project-${link.dataset.project}`);
      if (!section) return;
      ev.preventDefault();
      openAndGo(section);
    });
  }

  /* A link from elsewhere on the page (its contents list, a search result)
   * to something inside a closed project opens that project first. */
  function openForHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = id && document.getElementById(id);
    const section = target && projectOf(target);
    if (section && section.classList.contains("dl-project-closed")) {
      setOpen(section, true);
      target.scrollIntoView({ block: "start" });
    }
  }
  window.addEventListener("hashchange", openForHash);
  openForHash();
}
