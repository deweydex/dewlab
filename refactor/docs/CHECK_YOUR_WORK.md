# Check your work

This page is for you if you are adding one thing to dewlab: a tutorial, a
practice page, a series, or a course. It shows you how to check that thing
before you open a pull request.

You need Python 3 and one command. Nothing else.

## The one command

```bash
python3 check.py tutorials/my-tutorial
```

Change `my-tutorial` to the name of your folder. The program reads your
files and prints short lines. Each line starts with one word:

- **OK** — this part is fine.
- **Problem** — this will break the build or a page. Fix it, then run the
  command again.
- **Note** — nothing is broken. It is something useful to know.

At the end it says either *No problems. You can open a pull request.* or
how many problems there are.

To check a course instead:

```bash
python3 check.py courses/my-course.yaml
```

To check everything:

```bash
python3 check.py
```

## If you are adding a tutorial

A tutorial is one folder inside `tutorials/`. The folder name is the
tutorial's **id**. The id is used in the web address, in links from other
tutorials, and to save each reader's work. Choose it once. Do not change it
later.

Checklist:

- [ ] The folder name uses only small letters, digits and hyphens.
      Good: `first-steps`. Not good: `First Steps`, `first_steps`.
- [ ] No other folder in `tutorials/` has the same name. (Your computer will
      not let you make a second one. `check.py` tells you if it happens some
      other way.)
- [ ] Inside the folder there is a file with the same name and `.md` at the
      end. For the folder `first-steps`, the file is `first-steps.md`.
- [ ] The file starts with a frontmatter block: three dashes, a few lines,
      three dashes. It needs `title:`, `year:` and `version:`.

  ```markdown
  ---
  title: "First Steps"
  year: "2026-2027"
  version: 2026.09.14.1
  ---
  ```

- [ ] The frontmatter does **not** say which course or series the tutorial
      is in. That is written somewhere else (see "If you are adding to a
      course" below). If you copied an old file, delete any `module:`,
      `module_title:`, `series:` and `slug:` lines.
- [ ] Every cell a reader can run has an `id:` line as its first line, and
      no two cells on the page share an id.

  ````markdown
  ```python exec
  id: first-print
  print("hello")
  ```
  ````

- [ ] Every image the page shows is a file in the same folder.
- [ ] Run `python3 check.py tutorials/first-steps`. Fix each **Problem**.

Then, to put the tutorial on a course, see the course section below. Until
you do, the page builds but no course page links to it. `check.py` reminds
you with a **Note**.

## If you are adding a practice page

A practice page is a page of problems for one tutorial. It lives in that
tutorial's folder, with `-practice` added to the name: for `first-steps`,
the file is `first-steps-practice.md`.

Checklist:

- [ ] The file is in the tutorial's folder, named `<id>-practice.md`.
- [ ] Its frontmatter has `title:`, `year:`, `version:` and one more line,
      `practice_for:`, with the tutorial's id:

  ```markdown
  ---
  title: "First Steps — Practice"
  year: "2026-2027"
  version: 2026.09.14.1
  practice_for: first-steps
  ---
  ```

- [ ] It has no `covers:` line. The tutorial says what is taught; the
      practice page only practises it.
- [ ] Run `python3 check.py tutorials/first-steps`. The practice page is
      checked with its tutorial.

You do not add a practice page to any course. It follows its tutorial onto
every course the tutorial is on.

## If you are adding to a course, or adding a series

A course is one file in `courses/`. A series is a heading inside that file
with a list of tutorial ids in reading order. Here is a whole course file:

```yaml
title: Computational Methods and Problem Solving
code: 5N0554 · QQI Level 5
status: beta
card: |
  We work through matrices, simulation, algorithms and debugging, in Python.
description: |
  This module is Computational Methods and Problem Solving (5N0554).
contents:
  - title: Python fundamentals
    tutorials: [first-steps-cm, working-with-tables]
  - title: Matrices
    tutorials: [grid-of-numbers, multiplying-grids]
```

To add a tutorial to a series: add its id to the `tutorials:` list, in the
place where it should be read. To move it: move it in the list. To make a
new series: add a new `- title:` block with its own `tutorials:` list.

Checklist:

- [ ] Every id in every `tutorials:` list is the name of a folder in
      `tutorials/`. One wrong letter and the build stops.
- [ ] No id appears twice in the same course.
- [ ] Every series has a `title:`.
- [ ] Run `python3 check.py courses/computational-methods.yaml`.

The same tutorial may be in more than one course. Just list its id in both
files.

## If you are adding a course

Checklist:

- [ ] Make a new file in `courses/`. The file name is the course's id, like
      `programming-design-principles.yaml`.
- [ ] Give it `title:`, `code:`, `status:`, `card:` (two short sentences for
      the front page), `description:` (a paragraph for the course's own
      page) and `contents:` (its series, as above).
- [ ] Open `courses/index.yaml` and add the course's id to the `order:`
      list, in the place where the course should appear.
- [ ] Run `python3 check.py courses/programming-design-principles.yaml`.

You do not change any tutorial and you do not change `build.py`.

## Words on this page

- **id** — the name of a tutorial's folder, or of a course's file. Small
  letters, digits and hyphens.
- **frontmatter** — the lines between two `---` lines at the top of a file.
- **cell** — a box of code a reader can run.
- **series** — a list of tutorials read in order.
- **course** — a file in `courses/` that gathers series. The site calls a
  course a *module*.

## If something is still wrong

Run `python3 build.py`. It checks more than `check.py` does and stops at the
first thing it cannot build, with the file name and a reason. If the reason
is not clear, open a pull request anyway and say what you see. Somebody
will help.
