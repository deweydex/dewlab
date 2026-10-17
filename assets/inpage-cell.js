/* Editing a cell where it stands (planning/IN_PAGE_EDITOR.md, step 4).
 *
 * A cell's block in the markdown file is its `python exec` or `sql exec` fence
 * plus any hint, solution, predict, inputs and typed fences written straight
 * after it (source_map.py). This module cuts that text into the parts a person
 * may change and the parts they may not, and puts them back together. It reads
 * no page and writes nothing; assets/inpage-edit.js does the editing.
 *
 * What stays fixed, whatever is typed:
 *   - the fence's opening line (its language and `exec`),
 *   - the cell's `id:` line. A cell id is the key saved work lives under, so
 *     the editor does not offer it, and refuses a typed one,
 *   - the blank lines between the fences.
 * Everything else in each fence (the other header lines such as `hint:`, then
 * the code or the text) is the person's to change.
 */

const OPEN = /^(`{3,})[ \t]*([^\n`]*)$/;
const EXEC = /^(python|sql)[ \t]+exec\b/;
const ID_LINE = /^\s*id\s*:/;

const LABELS = {
  hint: "Hint, shown after a failed run",
  solution: "Solution",
  predict: "Prediction question",
  inputs: "Inputs",
  typed: "Typed answer",
};

/* A block that is a cell: `python exec` or `sql exec` first. */
export function isCellBlock(text) {
  const open = OPEN.exec(text.split("\n", 1)[0] || "");
  return !!open && EXEC.test(open[2].trim());
}

/* Cut a cell block into segments: `{gap}` for text between fences, `{fence}`
 * for a fence. A fence that never closes makes the block unparseable (null). */
export function parseCellBlock(text) {
  const lines = text.split("\n");
  const segments = [];
  let gap = [];
  let i = 0;
  while (i < lines.length) {
    const open = OPEN.exec(lines[i]);
    if (!open) { gap.push(lines[i]); i += 1; continue; }
    if (gap.length) { segments.push({ type: "gap", text: gap.join("\n") }); gap = []; }
    const ticks = open[1];
    const info = open[2].trim();
    let j = i + 1;
    while (j < lines.length && !(lines[j].startsWith(ticks) && /^`+[ \t]*$/.test(lines[j]))) j += 1;
    if (j >= lines.length) return null;
    segments.push({ type: "fence", ticks, info, body: lines.slice(i + 1, j) });
    i = j + 1;
  }
  if (gap.length) segments.push({ type: "gap", text: gap.join("\n") });

  const fences = segments.filter((s) => s.type === "fence");
  /* Blank lines at the end of a fence are the file's, not the person's. */
  for (const fence of fences) {
    fence.blankTail = 0;
    while (fence.body.length && fence.body[fence.body.length - 1].trim() === "") {
      fence.body.pop();
      fence.blankTail += 1;
    }
  }
  if (!fences.length || !EXEC.test(fences[0].info)) return null;

  /* The first fence is the cell. Its id line is held apart. */
  const cell = fences[0];
  const at = cell.body.findIndex((line) => ID_LINE.test(line));
  const header = [];
  for (const line of cell.body) {
    if (!/^\s*(id|hint|expect|name|toolkit|tests)\s*:/.test(line)) break;
    header.push(line);
  }
  if (at < 0 || at >= header.length) return null;   // no id in the header: leave it to the file
  cell.idLine = cell.body[at];
  cell.id = cell.idLine.replace(ID_LINE, "").trim();
  cell.rest = cell.body.filter((_line, index) => index !== at);

  const parts = [{ segment: cell, label: `Cell ${cell.id}`, language: cell.info.split(/\s+/)[0],
                   text: cell.rest.join("\n"), locked: cell.idLine }];
  for (const fence of fences.slice(1)) {
    const word = fence.info.split(/\s+/)[0];
    parts.push({ segment: fence, label: LABELS[word] || `${word} fence`, language: null,
                 text: fence.body.join("\n"), locked: null });
  }
  return { segments, parts };
}

/* What is wrong with the values, or null. `values[i]` is the new text of
 * `parts[i]`. The cell's own text may not bring an `id:` line back into its
 * header: the cell has one already, held apart. */
export function problem(parsed, values) {
  for (const line of values[0].split("\n")) {
    if (!/^\s*(id|hint|expect|name|toolkit|tests)\s*:/.test(line)) break;
    if (ID_LINE.test(line)) {
      return "A cell's id cannot be changed here: saved answers are filed under it. "
        + "Edit the file on GitHub if it must change.";
    }
  }
  return null;
}

/* The block's text with the values in. Each fence keeps its own backtick run
 * unless the new text needs a longer one. */
export function buildCellBlock(parsed, values) {
  const byFence = new Map(parsed.parts.map((part, index) => [part.segment, values[index]]));
  const out = [];
  for (const segment of parsed.segments) {
    if (segment.type === "gap") { out.push(segment.text); continue; }
    const text = byFence.get(segment);
    const body = [...(segment.idLine !== undefined ? [segment.idLine] : []), ...splitLines(text),
                  ...Array(segment.blankTail).fill("")];
    const runs = body.map((line) => /^`+/.exec(line)).filter(Boolean).map((m) => m[0].length);
    const ticks = "`".repeat(Math.max(segment.ticks.length, runs.length ? Math.max(...runs) + 1 : 0));
    out.push([ticks + (segment.info ? segment.info : ""), ...body, ticks].join("\n"));
  }
  return out.join("\n").replace(/\n+$/, "");
}

function splitLines(text) {
  return text === "" ? [] : text.replace(/\n+$/, "").split("\n");
}
