/* What the in-page editor gives the rich editor, and what it takes back
 * (planning/IN_PAGE_EDITOR.md). Pure text in, text out; no page, no editor.
 *
 * The rich editor (Crepe) does not know dewlab's markdown: it would read the
 * `_` in `$x_1$` as emphasis, and drop the `{.term}` after `*word*`. So a block
 * goes in with those pieces made safe, and comes out with them put back:
 *
 *   maths     `$x_1$` goes in as an inline code span holding the same TeX, so
 *             a person edits the TeX itself, and comes out as it went in.
 *   terms     `*word*{.term}` goes in as plain emphasis; any emphasis that
 *             comes out with the same words as a term gets its mark back.
 *   lists     bullets come out in the marker the list was written with, and a
 *             list written tight comes out tight.
 *
 * Everything else the editor writes is kept as it writes it.
 */

/* The same spans the build lifts out (build.py INLINE_MATH_RE, DISPLAY_MATH_RE). */
const INLINE_MATH = /\$(?!\s)([^$\n]+?)(?<!\s)\$/g;
const TERM = /(?<![*_])(\*|_)(?![*_\s])([^*_\n]+?)(?<![*_\s])\1(?![*_])\{\.term\}/g;

/* Can the rich editor take this block? Display maths, raw HTML, images, links
 * written as reference definitions, and a block that mixes code spans with
 * maths (the maths handling relies on code spans being its own) stay as
 * markdown in a text box. */
export function richSafe(text) {
  if (/\$\$|<|!\[|^\[[^\]]+\]:/m.test(text)) return false;
  if (text.includes("`") && text.includes("$")) return false;
  if (/^\s*\|/.test(text)) return false;                 // a table

  /* A list inside a list: the editor renumbers it, loosens it or changes its
   * bullets in ways the file's markdown does not (measured on the corpus). */
  if (/^\s*(?:[-*+]|\d+[.)])\s/.test(text) && /\n[ \t]+(?:[-*+]|\d+[.)])\s/.test(text)) return false;

  /* A list with a blank line in it, or code fenced inside it, could be loose
   * or two lists: the editor's choice of spacing is then a guess. */
  if (/^\s*(?:[-*+]|\d+[.)])\s/.test(text) && (/\n[ \t]*\n/.test(text) || text.includes("```"))) return false;

  /* Emphasis written inside a link text comes out wrapped round the link. */
  if (/\[[*_][^\]]*[*_]\]\(/.test(text)) return false;

  /* A backslash is only safe as the escape of a dollar sign. */
  if (/\\(?!\$)/.test(text)) return false;
  /* A brace is only safe as the `{.term}` mark. */
  const stripped = text.replace(TERM, "$1$2$1");
  if (/[{}]/.test(stripped)) return false;
  return true;
}

export function toEditor(text) {
  const terms = [];
  let doc = text.replace(/\\\$/g, "\u0000");
  doc = doc.replace(INLINE_MATH, (whole) => `\`${whole}\``);
  doc = doc.replace(TERM, (_whole, mark, words) => {
    terms.push(words);
    return `*${words}*`;
  });
  return { doc: doc.replace(/\u0000/g, "\\$"), terms };
}

export function fromEditor(markdown, state, original) {
  let out = markdown.replace(/\s+$/, "");

  /* Maths comes back out of its code span. TeX the person typed fresh was
   * escaped like prose (`x\_1`); put the escapes back inside the dollars. */
  out = out.replace(/`(\$(?!\s)[^$\n`]+?(?<!\s)\$)`/g, "$1");
  out = out.replace(INLINE_MATH, (whole) => whole.replace(/\\([_*])/g, "$1"));

  /* A line that begins with `=` is escaped by the editor (it could underline a
   * heading), but this build's markdown would show the backslash. */
  out = out.replace(/^(\s*)\\=(?=\s)/gm, "$1=");

  /* Terms. The editor writes emphasis as `*words*` or `_words_`. */
  if (state.terms.length) {
    out = out.replace(/(?<![*_])(\*|_)(?![*_\s])([^*_\n]+?)(?<![*_\s])\1(?![*_{])/g, (whole, _mark, words) =>
      state.terms.includes(words) ? `*${words}*{.term}` : whole);
  }

  if (/^\s*(?:[-*+]|\d+[.)])\s/.test(original)) out = tidyList(original, out);
  return out;
}

function tidyList(original, md) {
  const marker = original.match(/^\s*([-*+])\s/);
  const tight = !/\n[ \t]*\n/.test(original);
  if (marker) {
    md = md.replace(/^(\s*)[*+-](\s)/gm, (_whole, space, gap) => `${space}${marker[1]}${gap}`);
  }
  if (tight) md = md.replace(/\n[ \t]*\n(?=[ \t]*(?:[-*+]|\d+[.)])\s)/g, "\n");
  return md;
}
