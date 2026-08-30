# `build.py`, explained

`build.py` is the program that turns the Markdown files in `tutorials/`
into the actual website in `site/`. It's the biggest file in the repo —
almost 3,000 lines — because it does a genuinely large job: parsing
tutorial source, validating it, building navigation and cross-links
across the whole site, rendering the topic tree and knowledge map, and
writing out every page (including each tutorial's downloadable
standalone copy). This document is a map through it; the file's own
docstrings on almost every function already cover the details of what
each one does and why.

---

## The big idea: one tutorial file becomes several finished pages

Run `python3 build.py`, and here's roughly what happens, in order:

1. Every `.md` file under `tutorials/` is **loaded** (`load()`): its
   frontmatter is parsed and validated, code fences and maths are pulled
   out before Markdown can mangle them, the rest is converted to HTML,
   and everything is put back together into a `Tutorial` object.
2. Tutorials are grouped into **series** and **modules**, checked against
   each series' own ordering file, and cross-tutorial links (written as
   `tutorial:slug#anchor` in the source) are resolved to real relative
   URLs — or the build fails, naming exactly which link is broken.
3. Extra pages are built from that same data: the **topic tree**, the
   **knowledge map**, the **contents page**, the **about page**, and
   dewmini's offline download.
4. Every page is **written** to `site/`, including — for a tutorial page
   — a JSON manifest describing its cells for `tutorial-runtime.js` to
   read, and (unless `--no-standalone` is passed) a downloadable,
   self-contained single-file copy.

A `Tutorial` object (defined near the top of the file) is the one shape
that flows through almost this entire pipeline — worth reading its own
class-level comment first, since so much of the rest of the file is
"take a `Tutorial`, or a list of them, and do something with it."

---

## Reading order

The file's own section-header comments (`# --- name ---`) are the real
table of contents; this groups them into a few bigger phases:

1. **Data model** — `Cell`, `CodeBlock`, `Math`, `Note`, `Tutorial`. Read
   this first; everything else operates on these.
2. **Parsing** — `split_frontmatter`, `expand_includes`, `extract_blocks`,
   `extract_math`, `to_html`, `place_blocks`, `extract_notes`. This is the
   "one Markdown file becomes one `Tutorial`" pipeline, tied together by
   `load()` near the bottom of this phase.
3. **Navigation** — `module_order`, `order_files`, `versions_of`,
   `series_of`, `nav_for`, `render_series_nav`. How tutorials relate to
   each other: which series they're in, which version is current, what
   comes before and after.
4. **Reference** — `cumulative_glossary`, `render_toc`,
   `download_section`. The per-tutorial glossary/table-of-contents/
   download panel.
5. **Topic tree and knowledge map** — `topic_tiers`, `topic_layout`,
   `render_knowledge_map`, `tree_data`, and friends. These build the two
   visual "here's how everything connects" pages; `topic_tiers` in
   particular is a good small example of recursion with memoization if
   you haven't seen that pattern before.
6. **Checks** — `check_alt_text`, `check_folds`, `check_datasets`,
   `resolve_links`. Validation that runs as part of building, not a
   separate step — a build fails rather than silently shipping a broken
   page.
7. **Build** — `load()`, `asset_version`/`versioned` (cache-busting),
   `page_notice`, `write()` — the function that actually assembles and
   writes one finished tutorial page.
8. **Standalone** — `standalone_html`, `write_standalone`,
   `write_series_zip`, `zip_directory`, `write_dewmini_bundle`. Every
   downloadable, offline copy this site produces.
9. **Site-level pages** — `write_index` (the homepage), `write_tree_page`,
   `write_about_page`, `write_editor_page`.
10. **`build()` and `main()`** at the very end — the actual orchestration:
    call everything above, in the right order, for every tutorial file
    found.

---

## Two patterns worth understanding on their own

**Extract, convert, and put back.** Cells, illustrative code blocks, and
maths formulas all go through the same three-step dance: pulled out of
the raw Markdown *before* it's converted to HTML (`extract_blocks`,
`extract_math`), replaced with a placeholder the Markdown converter will
leave alone, and put back afterward (`place_blocks`) as their own,
separately-rendered HTML. The reason is that Markdown's own formatting
rules would otherwise reach inside them — `$a_i$` becoming italic instead
of a maths formula is the concrete example the file's own top comment
gives. This same shape (extract → convert prose → put back) is also how
`extract_notes` handles pedagogical asides.

**`re.sub` with a function instead of a string.** A lot of the extraction
functions above use `SOME_RE.sub(one, text)`, where `one` is a small
function defined right there, rather than a plain replacement string.
When `re.sub`'s second argument is callable, it gets called once per
match with the match object, and whatever string it returns replaces
that match. This is what lets each of those functions *do* something
(append to a list, look something up, validate an id) as a side effect of
finding each match, not just substitute fixed text.

---

## Where to look for something specific

- **"Why did my tutorial fail to build?"** — `fail()` is called from many
  places; the message always names the specific file and the specific
  problem. `split_frontmatter` covers the most common first-contact
  errors (missing required fields, a bad version string).
- **"How does a `tutorial:other-slug` link get resolved?"** —
  `resolve_links()`, and `link_between()` for the actual relative-path
  math once a target is found.
- **"How does the knowledge map lay itself out?"** — `topic_tiers()`
  (how deep a topic is, based on its prerequisites) feeds `topic_layout()`
  (turning tiers into actual x/y coordinates), and `arrow_between()` draws
  the connecting lines between them.
- **"How does a downloadable copy differ from the hosted page?"** —
  `standalone_html()` builds it, and its own comments (plus
  `DECISIONS_LOG.md` 7.77, referenced throughout) explain what's
  different and why — most notably, Pyodide running on the main thread
  rather than in a Worker.
