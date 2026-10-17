/* Editing a table where it stands (planning/IN_PAGE_EDITOR.md, step 4).
 *
 * A table in the markdown file is rows of cells between pipes. This module
 * finds where each cell's text lies, so that changing one cell changes those
 * characters and nothing else: the other cells, the column padding and the
 * delimiter row stay as written. Pure text; assets/inpage-edit.js does the
 * editing.
 */

const DELIMITER = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;

/* The rows of a table's markdown as lists of cells, each `{start, end}`: the
 * cell's text without its surrounding spaces, as offsets into `text`. The
 * delimiter row is left out. Null if the text is not a table this can read. */
export function parseTable(text) {
  const lines = text.split("\n");
  if (lines.length < 2 || !DELIMITER.test(lines[1])) return null;
  const rows = [];
  let offset = 0;
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (index !== 1) {
      const cells = splitRow(line, offset);
      if (!cells.length) return null;
      rows.push(cells);
    }
    offset += line.length + 1;
  }
  return rows;
}

/* Split one line on pipes that are not escaped and not inside a code span. */
function splitRow(line, offset) {
  const pieces = [];
  let from = 0;
  let inCode = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === "\\") { i += 1; continue; }
    if (ch === "`") inCode = !inCode;
    else if (ch === "|" && !inCode) { pieces.push([from, i]); from = i + 1; }
  }
  pieces.push([from, line.length]);
  /* A line usually starts and ends with a pipe; those make empty end pieces. */
  if (pieces.length && line.slice(pieces[0][0], pieces[0][1]).trim() === "" && /^\s*\|/.test(line)) pieces.shift();
  if (pieces.length && line.slice(pieces[pieces.length - 1][0]).trim() === "" && /\|\s*$/.test(line)) pieces.pop();
  return pieces.map(([a, b]) => {
    const raw = line.slice(a, b);
    const lead = raw.length - raw.trimStart().length;
    if (raw.trim() === "") {                          // empty: a place to type, after one space
      const at = a + Math.min(1, raw.length);
      return { start: offset + at, end: offset + at };
    }
    return { start: offset + a + lead, end: offset + a + lead + raw.trim().length };
  });
}

/* A cell's new text as it is written in a table: one line, pipes escaped. */
export function cellText(typed) {
  return typed.replace(/\s+/g, " ").trim().replace(/(?<!\\)\|/g, "\\|");
}
