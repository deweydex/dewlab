# Documents and pages

Two things `PLAN.md` did not cover: the `pages/` folder, and what happens to
every document that describes today's layout. Both are settled here.

## 1. Pages

`pages/` holds three hand-written site pages: `home.md`, `about.md`,
`features.md`. Each has a frontmatter of one field, `title:`, and a body
converted by the same markdown pipeline a tutorial uses, plus three things
prose cannot hold on its own: a ```card fence (a tile linking somewhere), a
`[[name]]` generated block (today only `[[search-box]]`), and a
`<div class="dl-hero">` / `<div class="dl-audience">` wrapper. `read_page()`
in `build.py` reads them; `render_index()`, `write_about_page()` and
`write_features_page()` each write one.

What the refactor touches:

1. `home.md`'s six course cards. They are hand-written ```card fences whose
   `url:` is a module page (`mit-pdp-maths-prog-integration.html`, …) and
   whose text repeats the module's code and blurb. Both move: the module
   page becomes `courses/<id>.html`, and the text now lives in the course
   file's `card:` field. So the six fences are replaced by one line,
   `[[course-cards]]`, a new generated block that `build.py` fills from
   `courses/index.yaml` in order. The two other cards on that page
   (`features.html`, `all-tutorials.html`) stay as they are.
2. Nothing else. `about.md` and `features.md` link to `tree.html`,
   `topics.html`, `all-tutorials.html`, `index.html` and `compose/…`, none
   of which move. `title:` stays the one frontmatter field.

Format change, for the sake of consistency with everything else in the
refactor: **none needed**. A page is already "a file that carries only what
is its own"; it has no placement and never had. The one sensible tidy, which
this refactor does not require and can wait, is one `write_page(name)` for
any `pages/<name>.md` in place of three near-identical functions — a code
change, not a format change.

## 2. Documents: what changes, file by file

The rule from `CONTRIBUTING.md` applies: the change is not finished until
the document describing the behaviour describes the new behaviour. Every
edit below is also in `apply_docs.py`, as an exact old-to-new replacement.
`python3 refactor/apply_docs.py --check` confirms each old passage is still
present, word for word, in the tree; `--apply` makes the edits. Run
`--check` now (it passes on `main` at `3b5b79a`) and `--apply` right after
`migrate_tutorials.py --apply`, in the same commit, so the tree is never
half-described.

Line numbers are for orientation only; the script matches on text.

### docs/WRITING_TUTORIALS.md — the guide a contributor reads

1. **"The file and its frontmatter" (l. 15–66).** The folder becomes
   `tutorials/<id>/`; the example tree loses the module segment; the
   example frontmatter loses `slug`, `module`, `module_title`, `series`;
   the table loses those four rows and gains one sentence saying that the
   folder name is the id and that where a tutorial sits is not in the file.
2. **"Where a tutorial sits in its series" (l. 67–111).** Rewritten whole.
   Today: an order file per series inside the module folder, checked both
   ways, plus yesterday's `module/slug` borrowing form. After: a course
   file under `courses/`, a series is a heading in it, a tutorial is
   placed by adding its id to a list, the same tutorial may be listed in
   any number of courses, and the build refuses an id it cannot find. The
   borrowing paragraph and its example go.
3. **"Practice pages" (l. 354–375).** The example frontmatter loses
   `slug`, `module`, `module_title`, `series`. The sentence about a mixed
   problem set gains: it is listed in the course file under `mixed:`.
4. **"Releasing a new version" (l. 540–566).** Unchanged in substance; the
   one path, `<slug>/v<version>.html`, becomes `<id>/v<version>.html`.
5. **"Adding a new module" (l. 570–574).** Rewritten: a module is a course
   file, `courses/<id>.yaml`, with title, code, status, card text,
   description and contents; plus one line in `courses/index.yaml` for its
   position. Nothing in `build.py` and nothing in any tutorial.
6. **"The authoring editor" (l. 578–597).** "searches every tutorial by
   title, slug or module" becomes "by title, id or course".

### ARCHITECTURE.md — the map

7. **§1, l. 30–31:** "reads `tutorials/**/*.md`" becomes "reads
   `tutorials/*/*.md` and `courses/*.yaml`".
8. **§1, l. 36–37:** "A tutorial is a folder, `tutorials/<module>/<slug>/`,
   holding its markdown at `<slug>.md`" becomes `tutorials/<id>/` and
   `<id>.md`.
9. **§1 step 5, l. 77–82:** "read the `.order.yaml` files and each
   tutorial's frontmatter to work out reading order" becomes "read
   `courses/*.yaml` to work out reading order"; "A slug listed in an order
   file with no tutorial behind it, or a series with no order file" becomes
   "An id listed in a course file with no tutorial behind it".
10. **§2, l. 167:** the storage key `dewlab:progress:<module>:<slug>`
    becomes `dewlab:progress:<id>`.
11. **§4, l. 229–231:** "walking each series in `<series>.order.yaml` order
    and, where a module's `series.yaml` says so (`series_chain()`), every
    earlier series in that module too" becomes "walking each series of the
    course in the course file's order, and every earlier series of that
    course".

### CLAUDE.md — the instructions this repository gives an assistant

12. **l. 4:** "`build.py` turns `tutorials/**/*.md` into `site/`" becomes
    "`build.py` turns `tutorials/*/*.md` and `courses/*.yaml` into
    `site/`".
13. **"Three traps":** "Cell ids are a contract" gains a second sentence:
    a tutorial's id (its folder name) is one too — it is the key under
    which every reader's saved work lives, and the address of the page.

### docs/tutorial-runtime-explained.md

14. **l. 86:** `dewlab:custom-cells:<module>:<slug>` becomes
    `dewlab:custom-cells:<id>`.

### planning/REFERENCE_PANEL.md — the reference panel's own spec

15. **§1 (l. 28), §2 (l. 40–57), §5 (l. 143):** every mention of
    `<series>.order.yaml` and `series.yaml` becomes the course file; the
    explanation of series-only versus chained accumulation becomes: a
    reference accumulates through the course the reader is following, in
    that course file's order, series by series — and a series a course
    leaves unlisted is simply not on that course. The `reflections-and-review`
    example stays as the example of a series with no fixed position (it is
    listed last in its course file, and the reader reaches it whenever they
    like).
16. **§3 (l. 68, 75):** `tutorials/<module>/<slug>.glossary.yaml` becomes
    `tutorials/<id>/<id>.glossary.yaml`.

### .claude/skills — the three skills that name a tutorial's path

17. **`cell-code-review/SKILL.md` l. 25–26, `tutorial-glossary/SKILL.md`
    l. 21–22 and 93, `triage-report/SKILL.md` l. 23:** the path becomes
    `tutorials/<id>/<id>.md` (and `.glossary.yaml`). The "or
    `tutorials/<module>/<slug>.md` without a folder" alternative goes —
    there is one layout.

### Documents that do not change

- `DECISIONS_LOG.md` — history; never edited. It gains entry 7.172 (written
  in the migration commit, not by the script), which supersedes 7.171's
  borrowed form.
- `CONTRIBUTING.md`, `README.md`, `docs/build-explained.md`,
  `docs/FOR_STUDENTS.md`, `docs/FAQ.md`, `planning/PEDAGOGICAL_STYLE_GUIDE.md`,
  `planning/EXERCISES.md` — checked; none names the layout.
- `planning/CURRICULUM_MAP.md` — generated; regenerated by
  `dev/curriculum_map.py` after step 2, not edited.
- `planning/PLAIN_LANGUAGE_PASS.md` — gains a line for "Also part of …",
  the one new student-facing string, in the migration commit.
- `refactor/` itself — deleted at step 9.

### In dewnote (other repository)

18. **`planning/DIALECTS.md` §1** — the file layout and the required field
    list, as `EDITOR.md` §2 says. Not in `apply_docs.py`; different
    repository.

## 3. Order, on the day

1. `python3 refactor/apply_docs.py --check` — every old passage found.
2. `python3 refactor/migrate_tutorials.py --rename computational-methods/first-steps=first-steps-cm --apply`
3. `python3 refactor/apply_docs.py --apply`
4. Replace the six course-card fences in `pages/home.md` with `[[course-cards]]`
   (the script does this too; it is listed so it is not a surprise).
5. Write `DECISIONS_LOG.md` 7.172 by hand.
6. Commit: "Placement moves into courses/". The build does not run yet —
   that is `PLAN.md` step 2 — but the tree and its documents agree.
