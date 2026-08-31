/* Behaviour for the dewmark exam page: saving, restoring, progress
   counting, and the finish step. The page's questions are already
   rendered as static content by the exam builder; this file only wires
   them up. Everything here runs locally — the page never contacts a
   server. */

"use strict";

const MODEL = JSON.parse(
  document.getElementById("dewmark-exam-model").textContent);
const STORAGE_KEY = "dewmark:" + MODEL.exam_code;

/* One flat map of every answer space: name -> {type, marks, section,
   question}. Built from the model so counting logic never scrapes the
   page. */
const SPACES = {};
for (const section of MODEL.sections) {
  for (const question of section.questions) {
    for (const answer of question.answers) {
      SPACES[answer.name] = {
        type: answer.type, marks: answer.marks,
        section: section.name, question: question.name,
      };
    }
  }
}

let state = {
  format_version: 1,
  exam_code: MODEL.exam_code,
  exam_version: MODEL.exam_version,
  student: {},
  started_at: null,
  saved_at: null,
  finished_at: null,
  answers: {},
};
let fileHandle = null;
let fileSaveTimer = null;

/* ---------------------------------------------- reading answers back */

function collectAnswer(root, type) {
  /* Read one answer space's current value into plain data. Empty
     answers come back as null so "never touched" and "left blank" can
     be told apart by whether the key exists at all. */
  if (type === "multiple-choice") {
    const picked = [...root.querySelectorAll("input:checked")]
      .map((el) => Number(el.value));
    return picked.length ? { chosen: picked } : null;
  }
  if (type === "fill-in-the-blank") {
    const blanks = {};
    let any = false;
    for (const el of root.querySelectorAll(".dm-blank")) {
      blanks[el.dataset.blank] = el.value;
      if (el.value.trim()) any = true;
    }
    return any ? { blanks } : null;
  }
  if (type === "short-written-answer" || type === "long-written-answer") {
    const text = root.querySelector(".dm-writing").value;
    return text.trim() ? { text } : null;
  }
  if (type === "essay") {
    const essay = root.querySelector(".dm-essay").value;
    const planningBox = root.querySelector(".dm-planning");
    const planning = planningBox ? planningBox.value : "";
    return essay.trim() || planning.trim()
      ? { text: essay, planning } : null;
  }
  if (type === "numeric-answer") {
    const boxes = {};
    let any = false;
    for (const el of root.querySelectorAll(".dm-numeric input")) {
      boxes[el.dataset.box] = el.value;
      if (el.value.trim()) any = true;
    }
    const workingBox = root.querySelector(".dm-working");
    const working = workingBox ? workingBox.value : "";
    if (working.trim()) any = true;
    return any ? { boxes, working } : null;
  }
  if (type === "complete-the-table") {
    const cells = {};
    let any = false;
    for (const el of root.querySelectorAll(".dm-cell")) {
      cells[el.dataset.cell] = el.value;
      if (el.value.trim()) any = true;
    }
    return any ? { cells } : null;
  }
  if (type === "describe-a-sketch") {
    const shapeEl = root.querySelector("input[type=radio]:checked");
    const features = {};
    let any = Boolean(shapeEl);
    for (const el of root.querySelectorAll(".dm-feature")) {
      const key = el.dataset.feature + "." + el.dataset.box;
      features[key] = el.value;
      if (el.value.trim()) any = true;
    }
    return any
      ? { shape: shapeEl ? Number(shapeEl.value) : null, features } : null;
  }
  if (type === "label-the-diagram") {
    const labels = {};
    let any = false;
    for (const el of root.querySelectorAll(".dm-diagram-label input")) {
      labels[el.dataset.label] = el.value;
      if (el.value.trim()) any = true;
    }
    return any ? { labels } : null;
  }
  return null;
}

function applyAnswer(root, type, value) {
  /* Put a saved value back into one answer space's controls. */
  if (!value) return;
  if (type === "multiple-choice") {
    for (const el of root.querySelectorAll("input")) {
      el.checked = (value.chosen || []).includes(Number(el.value));
    }
  } else if (type === "fill-in-the-blank") {
    for (const el of root.querySelectorAll(".dm-blank")) {
      el.value = (value.blanks || {})[el.dataset.blank] || "";
    }
  } else if (type === "short-written-answer"
             || type === "long-written-answer") {
    root.querySelector(".dm-writing").value = value.text || "";
  } else if (type === "essay") {
    root.querySelector(".dm-essay").value = value.text || "";
    const planningBox = root.querySelector(".dm-planning");
    if (planningBox) planningBox.value = value.planning || "";
  } else if (type === "numeric-answer") {
    for (const el of root.querySelectorAll(".dm-numeric input")) {
      el.value = (value.boxes || {})[el.dataset.box] || "";
    }
    const workingBox = root.querySelector(".dm-working");
    if (workingBox) workingBox.value = value.working || "";
  } else if (type === "complete-the-table") {
    for (const el of root.querySelectorAll(".dm-cell")) {
      el.value = (value.cells || {})[el.dataset.cell] || "";
    }
  } else if (type === "describe-a-sketch") {
    for (const el of root.querySelectorAll("input[type=radio]")) {
      el.checked = Number(el.value) === value.shape;
    }
    for (const el of root.querySelectorAll(".dm-feature")) {
      const key = el.dataset.feature + "." + el.dataset.box;
      el.value = (value.features || {})[key] || "";
    }
  } else if (type === "label-the-diagram") {
    for (const el of root.querySelectorAll(".dm-diagram-label input")) {
      el.value = (value.labels || {})[el.dataset.label] || "";
    }
  }
}

/* ---------------------------------------------- saving */

function gatherState() {
  for (const root of document.querySelectorAll(".dm-answer")) {
    const name = root.dataset.answer;
    const value = collectAnswer(root, root.dataset.type);
    if (value === null) delete state.answers[name];
    else state.answers[name] = value;
  }
  state.saved_at = new Date().toISOString();
  return state;
}

function setPill(id, text, cls) {
  const el = document.getElementById(id);
  el.textContent = text;
  el.className = "dm-save-pill" + (cls ? " " + cls : "");
}

function saveEverywhere() {
  gatherState();
  const clock = new Date().toLocaleTimeString(
    [], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    setPill("dm-save-browser", "Browser ✓ " + clock, "dm-ok");
  } catch (err) {
    setPill("dm-save-browser", "Browser save failed", "dm-off");
  }
  if (fileHandle) {
    clearTimeout(fileSaveTimer);
    fileSaveTimer = setTimeout(async () => {
      try {
        const writable = await fileHandle.createWritable();
        await writable.write(JSON.stringify(state, null, 2));
        await writable.close();
        setPill("dm-save-file", "File ✓ " + clock, "dm-ok");
      } catch (err) {
        fileHandle = null;
        setPill("dm-save-file", "File saving is off", "dm-off");
      }
    }, 800);
  }
  refreshProgress();
}

function safeName(text) {
  return String(text || "").toLowerCase()
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "student";
}

function submissionBaseName() {
  const details = state.student || {};
  const number = safeName(details["student number"] || details.number);
  const name = safeName(details["full name"] || details.name);
  return "dewmark_" + MODEL.exam_code + "_" + number + "_" + name;
}

/* ---------------------------------------------- starting and restoring */

function readStoredState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (parsed.exam_code !== MODEL.exam_code) return null;
    return parsed;
  } catch (err) {
    return null;
  }
}

function describeState(candidate, label) {
  const count = Object.keys(candidate.answers || {}).length;
  const when = candidate.saved_at
    ? new Date(candidate.saved_at).toLocaleString() : "an unknown time";
  return label + ": " + count + " answers, saved " + when;
}

function adoptState(candidate) {
  state = candidate;
  const details = state.student || {};
  for (const el of document.querySelectorAll("[data-detail]")) {
    el.value = details[el.dataset.detail] || "";
  }
}

async function begin() {
  for (const el of document.querySelectorAll("[data-detail]")) {
    state.student[el.dataset.detail] = el.value.trim();
    if (!el.value.trim()) {
      alert("Please fill in your " + el.dataset.detail + ".");
      el.focus();
      return;
    }
  }
  if (!state.started_at) state.started_at = new Date().toISOString();

  if (MODEL.variant !== "answer_key" && "showSaveFilePicker" in window) {
    try {
      fileHandle = await window.showSaveFilePicker({
        suggestedName: submissionBaseName() + ".json",
        types: [{ description: "dewmark answer file",
                  accept: { "application/json": [".json"] } }],
      });
    } catch (err) {
      fileHandle = null;
    }
  }
  if (!fileHandle) {
    setPill("dm-save-file", "File saving is off", "dm-off");
  }
  enterExam();
}

function enterExam() {
  document.getElementById("dm-start").hidden = true;
  document.getElementById("dm-app").hidden = false;
  document.getElementById("dm-top-student").textContent =
    Object.values(state.student).filter(Boolean).join(" · ");
  for (const root of document.querySelectorAll(".dm-answer")) {
    applyAnswer(root, root.dataset.type, state.answers[root.dataset.answer]);
  }
  buildPanel();
  saveEverywhere();
}

function loadAnswerFile() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "application/json,.json";
  input.onchange = async () => {
    const file = input.files[0];
    if (!file) return;
    let loaded;
    try {
      loaded = JSON.parse(await file.text());
    } catch (err) {
      alert("That file could not be read as an answer file.");
      return;
    }
    if (loaded.exam_code !== MODEL.exam_code) {
      alert("That answer file belongs to a different exam ("
        + loaded.exam_code + "), so it cannot be loaded here.");
      return;
    }
    const stored = readStoredState();
    if (stored && stored.saved_at !== loaded.saved_at
        && Object.keys(stored.answers || {}).length) {
      const keepFile = confirm(
        "This browser also holds saved work for this exam.\n\n"
        + describeState(loaded, "The file") + "\n"
        + describeState(stored, "This browser") + "\n\n"
        + "Press OK to continue from the file, or Cancel to continue "
        + "from this browser.");
      if (!keepFile) { adoptState(stored); enterExam(); return; }
    }
    adoptState(loaded);
    enterExam();
  };
  input.click();
}

/* ---------------------------------------------- progress */

function refreshProgress() {
  for (const root of document.querySelectorAll(".dm-answer")) {
    const answered = root.dataset.answer in state.answers;
    root.classList.toggle("dm-answered", answered);
  }
  for (const section of MODEL.sections) {
    for (const question of section.questions) {
      const attempted = question.answers.some((a) => a.name in state.answers);
      const button = document.querySelector(
        '[data-panel-question="' + question.name + '"]');
      if (button) button.classList.toggle("dm-done", attempted);
    }
    const label = document.querySelector(
      '[data-panel-count="' + section.name + '"]');
    if (label && section.choose) {
      const attempted = section.questions.filter(
        (q) => q.answers.some((a) => a.name in state.answers)).length;
      label.textContent = "answered " + attempted
        + " · " + section.choose + " will count";
    }
  }
}

function buildPanel() {
  const panel = document.getElementById("dm-panel");
  panel.innerHTML = "";
  for (const section of MODEL.sections) {
    const heading = document.createElement("h2");
    heading.textContent = "Section " + section.name
      + (section.choose ? " — answer any " + section.choose : "");
    panel.appendChild(heading);
    if (section.choose) {
      const note = document.createElement("p");
      note.className = "dm-panel-note";
      note.dataset.panelCount = section.name;
      panel.appendChild(note);
    }
    for (const question of section.questions) {
      const button = document.createElement("button");
      button.className = "dm-panel-q";
      button.dataset.panelQuestion = question.name;
      button.innerHTML = "<span>" + question.name.toUpperCase()
        + "</span><span>(" + question.marks + ")</span>";
      button.addEventListener("click", () => {
        const target = document.querySelector(
          '[data-question="' + question.name + '"]');
        if (target) target.scrollIntoView({ behavior: "smooth" });
      });
      panel.appendChild(button);
    }
  }
  refreshProgress();
}

/* ---------------------------------------------- the finish step */

function finishReport() {
  const empty = [];
  for (const name of Object.keys(SPACES)) {
    if (!(name in state.answers)) {
      empty.push({ name, marks: SPACES[name].marks });
    }
  }
  const lines = [];
  if (empty.length === 0) {
    lines.push('<li class="dm-finish-good">Every answer space has '
      + "something in it.</li>");
  } else {
    const total = empty.reduce((sum, e) => sum + e.marks, 0);
    lines.push('<li class="dm-finish-warn">' + empty.length
      + " answer spaces are empty, worth " + total + " marks: "
      + empty.map((e) => e.name).join(", ") + "</li>");
  }
  for (const section of MODEL.sections) {
    if (!section.choose) continue;
    const attempted = section.questions.filter(
      (q) => q.answers.some((a) => a.name in state.answers)).length;
    const cls = attempted >= section.choose
      ? "dm-finish-good" : "dm-finish-warn";
    lines.push('<li class="' + cls + '">Section ' + section.name
      + ": " + attempted + " answered, " + section.choose
      + " will count.</li>");
  }
  lines.push("<li>Handing in as: "
    + Object.values(state.student).filter(Boolean).join(" · ")
    + "</li>");
  return "<ul>" + lines.join("") + "</ul>"
    + "<p>Pressing the button downloads one file. Upload it to the "
    + "assignment your teacher named, and show the confirmation to your "
    + "invigilator. If you are given more time, keep working and "
    + "download again — the newest file is the one that counts.</p>";
}

function readableCopy() {
  /* A plain copy of the paper with the answers written in as text: the
     student's own record, openable anywhere, containing no scripts. */
  const clone = document.documentElement.cloneNode(true);
  for (const el of clone.querySelectorAll(
      "script, button, #dm-panel, #dm-start, #dm-finish-screen,"
      + " .dm-save-pill")) {
    el.remove();
  }
  for (const el of clone.querySelectorAll("#dm-app, #dm-topbar")) {
    el.hidden = false;
  }
  for (const root of clone.querySelectorAll(".dm-answer")) {
    for (const field of root.querySelectorAll("textarea, input")) {
      const shown = document.createElement(
        field.tagName === "TEXTAREA" ? "pre" : "span");
      let text = field.value;
      if (field.type === "radio" || field.type === "checkbox") {
        /* Cloned controls lose checked state; read the live one. */
        const live = document.querySelector(
          '[name="' + field.name + '"][value="' + field.value + '"]');
        if (!(live && live.checked)) { field.closest("label").remove(); continue; }
        text = "✓ chosen";
      }
      shown.textContent = text.trim() ? text : "(not attempted)";
      shown.style.whiteSpace = "pre-wrap";
      field.replaceWith(shown);
    }
  }
  const student = Object.entries(state.student)
    .map(([key, value]) => key + ": " + value).join(" · ");
  const note = "<p style=\"font-family: system-ui, sans-serif;"
    + " font-size: 13px; border: 1px solid #ddd7cd; padding: 8px 12px;\">"
    + "Readable copy of a dewmark submission · " + student
    + " · saved " + state.saved_at + "</p>";
  return "<!doctype html>\n<html>" + clone.innerHTML
    .replace("<main id=\"dm-paper\"", note + "<main id=\"dm-paper\"")
    + "</html>";
}

/* A minimal zip writer. Entries are stored without compression, which
   every unzip tool accepts; writing the format directly keeps the page
   free of outside code. */
function makeZip(entries) {
  const encoder = new TextEncoder();
  const table = [];
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[n] = c >>> 0;
  }
  const crc32 = (bytes) => {
    let c = 0xffffffff;
    for (const byte of bytes) c = table[(c ^ byte) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  };
  const chunks = [];
  const central = [];
  let offset = 0;
  const u16 = (v) => new Uint8Array([v & 255, (v >> 8) & 255]);
  const u32 = (v) => new Uint8Array(
    [v & 255, (v >> 8) & 255, (v >> 16) & 255, (v >> 24) & 255]);
  for (const entry of entries) {
    const nameBytes = encoder.encode(entry.name);
    const data = typeof entry.data === "string"
      ? encoder.encode(entry.data) : entry.data;
    const crc = crc32(data);
    const header = [u32(0x04034b50), u16(20), u16(0), u16(0), u16(0),
      u16(0), u32(crc), u32(data.length), u32(data.length),
      u16(nameBytes.length), u16(0)];
    for (const part of header) chunks.push(part);
    chunks.push(nameBytes, data);
    central.push({ nameBytes, crc, size: data.length, offset });
    offset += header.reduce((s, p) => s + p.length, 0)
      + nameBytes.length + data.length;
  }
  const centralStart = offset;
  for (const entry of central) {
    const record = [u32(0x02014b50), u16(20), u16(20), u16(0), u16(0),
      u16(0), u16(0), u32(entry.crc), u32(entry.size), u32(entry.size),
      u16(entry.nameBytes.length), u16(0), u16(0), u16(0), u16(0),
      u32(0), u32(entry.offset)];
    for (const part of record) chunks.push(part);
    chunks.push(entry.nameBytes);
    offset += record.reduce((s, p) => s + p.length, 0)
      + entry.nameBytes.length;
  }
  chunks.push(u32(0x06054b50), u16(0), u16(0), u16(central.length),
    u16(central.length), u32(offset - centralStart), u32(centralStart),
    u16(0));
  return new Blob(chunks, { type: "application/zip" });
}

function downloadSubmission() {
  state.finished_at = new Date().toISOString();
  saveEverywhere();
  const zip = makeZip([
    { name: "answers.json", data: JSON.stringify(state, null, 2) },
    { name: "your-exam.html", data: readableCopy() },
  ]);
  const link = document.createElement("a");
  link.href = URL.createObjectURL(zip);
  link.download = submissionBaseName() + ".zip";
  link.click();
  URL.revokeObjectURL(link.href);
}

function downloadAnswerFile() {
  gatherState();
  const blob = new Blob([JSON.stringify(state, null, 2)],
    { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = submissionBaseName() + ".json";
  link.click();
  URL.revokeObjectURL(link.href);
}

/* ---------------------------------------------- wiring */

document.getElementById("dm-begin").addEventListener("click", begin);
document.getElementById("dm-load-file").addEventListener("click",
  loadAnswerFile);
document.getElementById("dm-download").addEventListener("click",
  downloadAnswerFile);
document.getElementById("dm-finish").addEventListener("click", () => {
  gatherState();
  document.getElementById("dm-finish-report").innerHTML = finishReport();
  document.getElementById("dm-app").hidden = true;
  document.getElementById("dm-finish-screen").hidden = false;
});
document.getElementById("dm-keep-working").addEventListener("click", () => {
  document.getElementById("dm-finish-screen").hidden = true;
  document.getElementById("dm-app").hidden = false;
});
document.getElementById("dm-submit").addEventListener("click",
  downloadSubmission);

document.addEventListener("input", (event) => {
  if (event.target.closest(".dm-answer")) {
    const essay = event.target.closest(".dm-answer")
      .querySelector(".dm-essay");
    if (essay) {
      const counter = event.target.closest(".dm-answer")
        .querySelector(".dm-word-count");
      const words = essay.value.trim().split(/\s+/).filter(Boolean).length;
      counter.textContent = words + " words";
    }
    saveEverywhere();
  }
});
document.addEventListener("change", (event) => {
  if (event.target.closest(".dm-answer")) saveEverywhere();
});
window.addEventListener("beforeunload", () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(gatherState()));
  } catch (err) { /* the periodic save already reported storage trouble */ }
});

/* If this browser already holds saved work for this exam, offer to
   continue from it rather than starting blank. */
const stored = readStoredState();
if (stored && Object.keys(stored.answers || {}).length) {
  const note = document.createElement("p");
  note.className = "dm-restore-note";
  note.textContent = "Saved work was found ("
    + describeState(stored, "this browser") + "). ";
  const resume = document.createElement("button");
  resume.className = "dm-secondary";
  resume.textContent = "Continue from saved work";
  resume.addEventListener("click", () => { adoptState(stored); enterExam(); });
  note.appendChild(resume);
  document.getElementById("dm-start").prepend(note);
}

/* A second copy of the exam open in this browser must not save over the
   first; the second copy detects the first and steps back. */
const channel = "BroadcastChannel" in window
  ? new BroadcastChannel(STORAGE_KEY) : null;
if (channel) {
  let iAmFirst = true;
  channel.onmessage = (event) => {
    if (event.data === "anyone-there?" && iAmFirst) channel.postMessage("yes");
    if (event.data === "yes") {
      iAmFirst = false;
      /* Every way into the exam is closed, not only the Begin button. */
      for (const button of document.querySelectorAll(
          "#dm-begin, #dm-load-file, .dm-restore-note button")) {
        button.disabled = true;
      }
      alert("This exam is already open in another window on this "
        + "computer. Please continue there; this window will not save.");
    }
  };
  channel.postMessage("anyone-there?");
}
