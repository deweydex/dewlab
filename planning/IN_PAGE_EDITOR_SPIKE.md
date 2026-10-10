# Editing a page where it stands: what the spike found

*October 2026. The measuring half of step 2 in
[`IN_PAGE_EDITOR.md`](IN_PAGE_EDITOR.md). The scripts are in
[`editor-spike/`](editor-spike/README.md).*

## The verdict

The approach in the plan works. The build can say which bytes of a markdown
file produced each block of a page, an edited block can be spliced back over
exactly those bytes, and a block can be swapped for an editor that sits in the
page without moving anything. Headings and ordinary paragraphs already do this
with no visible change at all. What the spike did not settle is the awkward
third of the page: maths, tables, a few kinds of list, and the build's own
conventions (`{.term}` marks, raw HTML, includes). Those are known, bounded
pieces of work. None of them made the approach look wrong.

Three decisions follow from what was measured. They are at the end.

## 1. The source map

`source_map.py` and `python3 build.py --source-map` (off by default).

- Every one of the 498 tutorial files renders identically with the map and
  without it. In full real builds, one of each, 1,209 of 1,211 built pages were
  identical once the `data-md` attributes were removed. The other two differed
  only in a download-size label, because the downloadable copies carried the
  attributes too; they carry none now, and all 1,211 match.
- 992 pages carry a map, 51,051 blocks in all, adding 0.08% to the size of the
  HTML.
- 25,647 of 25,827 source blocks were matched to an element. The 180 that were
  not are three kinds that render nowhere in the page body: 120 notes (the
  build moves them out), 50 toolkit references (they render nothing), and 10
  predictions drawn above a cell that is not next to them.
- The kind of block and the element it became agree almost everywhere: headings
  to `h1`–`h3`, lists to `ul`/`ol`, a cell to `div.dl-cell`, a fold to
  `details`, a question to `div.dl-question`, the panes of one site editor to
  one `div.dl-site-editor`. An `{{include: …}}` line is a paragraph in the
  source and a blockquote on the page.
- The edit property: for a paragraph, a heading and a list from each page,
  splicing new text over the block's range and rebuilding changed that block's
  output and nothing else (497, 497 and 370 edits; one page could not be
  reached by my script).
- A real bug turned up on the way. My first attribute name, `data-src`, was read
  by the asset resolver as a file reference and failed the build. A test that
  ran only `load()` had missed it; one that ran the whole build found it.
- It costs a build about 14 seconds of processor time, because each page is
  loaded twice so that the map can be dropped from any page it would change.

## 2. What Crepe does to markdown it did not need to change

The editor rewrites markdown in its own style, so editing one list item would
rewrite the whole list. I pushed 17,994 prose blocks (paragraphs, headings,
lists, quotes and tables, which is every kind I would edit as rich text)
through the editor untouched and compared.

| | Unchanged | Text differs, page the same | Page differs |
|---|---|---|---|
| Crepe as it comes | 16,591 (92.2%) | 490 (2.7%) | 913 (5.1%) |
| With the tidying below | 17,594 (97.8%) | 377 (2.1%) | 23 (0.13%) |

"Page differs" is judged by rendering the original and the round-tripped text
through the build's own markdown steps and comparing the HTML, not by eye.

What Crepe did, and what undid it:

- **Display maths became inline maths**, and multi-line maths came back garbled
  (414 blocks). The fix is to lift maths out before Crepe sees the text and put
  it back after, as the build does for Python-Markdown.
- **Lists came back with `*` bullets and a blank line between every item** (455
  blocks), which makes a tight list render as a loose one. The fix is to restore
  the original bullet and, for a list that was tight, remove the blank lines.
- **Empty table cells came back as `<br />`** (28 blocks). Remove it.
- **Tables are re-padded** to align their columns. The page does not change but
  the diff does, in all 312 tables. Acceptable; a reviewer sees the table
  change only if someone edited it.

The 23 that remain are ten stray backslash escapes (`&` and `#` gain one, which
shows in image alt text), six extra blank lines in unusual lists, two nested
bullet markers, one renumbered list, and four odd ones. None is dangerous. All
could be tidied the same way.

This measured the editor on prose only. It did not measure cells, folds, or the
text inside fences.

## 3. Swapping a block for an editor with no visible change

On a page built with the map, I replaced one block at a time with an editor and
measured the edited block, how far every other block on the page moved, and how
many pixels changed in the region around it. A random ten pages in light theme
and eight in dark, up to two blocks of each kind from each.

What made it work:

- **Crepe's stylesheet is not used.** It resets every margin and pads the editor
  by 60 and 120 pixels. Without it, the editor's own paragraphs and headings
  pick up the page's ordinary styles, which is where the fidelity comes from.
  The extra furniture Crepe mounts (link popups, block handle, slash menu) is
  hidden until it is shown, and the empty paragraph ProseMirror leaves after a
  list is hidden. The whole of the styling is eight lines
  (`editor-spike/inplace.css`).
- **Crepe's features that draw their own markup are off**: its list-item view,
  its table view, its block menu, its maths and code blocks.

| Block | Nothing else moved, and under 0.5% of nearby pixels changed |
|---|---|
| Heading (`h2`, `h3`), light | 23 of 23, nothing moved, 0.00% of pixels |
| Heading, dark | 19 of 19 |
| Paragraph, light | 17 of 20 |
| Paragraph, dark | 14 of 16 |
| Bullet list, light / dark | 9 of 12 / 7 of 9 |
| Quote, light | 2 of 5 |
| Ordered list, light | 4 of 9 |
| Table, light | 0 of 6 |

Every miss has a cause I can name, and most come from the build's own
conventions that Crepe does not know:

- **Maths** shows as the text standing in for it, not as rendered maths, so a
  block with maths changes height. This is the biggest open piece: 2,714 of the
  17,994 prose blocks, on 264 pages, contain maths.
- **`*word*{.term}`** (an attribute list on an italic term) shows its braces.
  620 blocks on 139 pages.
- **A paragraph that starts with raw HTML, or an `{{include}}` line**, is
  treated as text. 426 blocks on 202 pages. These should be source-only blocks,
  as the plan already says of includes.
- **Tables** still differ (worst shift 122 pixels after Crepe's table view was
  turned off, from 325 before). The page wraps its tables in markup Crepe does
  not produce.
- **A code fence inside a list item** loses the page's cell styling. Nine blocks.

A phone: I did not test one. I emulated a 390-pixel touch screen. The pixel
change for headings and paragraphs matched the control, but my layout-shift
number was unusable there: the page moved other blocks by up to 490 pixels with
no editor on it at all. That may be a real problem with how the pages settle on
a phone, and is worth a look of its own. Typing, the on-screen keyboard and
selection handles are all untested. You will need to try it on a real device.

## 4. What this means for the plan

- **Step 3 can start**, with a narrower first scope than the plan's table gave:
  rich editing for headings, paragraphs and bullet lists; the rest as source
  text in a box, as the plan already allowed for folds, hints and the other
  fences. Quotes and ordered lists are close and can join once their last
  mismatches are fixed.
- **The editor needs its own entry point.** `milkdown-entry.js` builds Crepe for
  the old editor page. The in-page editor wants different features and none of
  Crepe's stylesheet, so it should be a second bundle, loaded when Edit is
  pressed (about 2.9 MB, as now). Committing it means a vendor rebuild in the
  same pull request, per `CLAUDE.md`.
- **The tidying belongs in the editor.** Lifting maths out, restoring bullets
  and tightness, and removing `<br />` from empty cells are about forty lines of
  JavaScript, and the measurement above is the test for them: round-trip the
  corpus, count what differs.

## Decisions for you

1. **Maths while a block is being edited.** Rendering it in place needs
   Crepe's LaTeX feature, which in turn needs CodeMirror and brings its own
   styling to fix. The cheaper first version shows a block's maths as its TeX
   (`$x^2$`) while the cursor is in that block, and renders it again when the
   cursor leaves. That block changes height while edited and nothing else does.
   Which do you want first?
2. **`{.term}` marks.** Either teach the editor the mark (it renders as an
   italic with the page's term styling and round-trips as `*word*{.term}`), or
   leave braces visible in edited text for now. 139 pages use them.
3. **Phones.** Does the first version need to work on one, or can it say "this
   needs a larger screen" below some width? The answer changes the size of
   step 3.
