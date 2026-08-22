# The editor

A page where Josh reorders tutorials, inserts one between two others, and
creates a new one — without a terminal, without Python, and without asking
anybody.

Not built yet. This is the plan.

---

## The problem underneath the request

Reordering is currently expensive for a reason that has nothing to do with
editors: **the order is stored in eighteen places.** Every tutorial carries
`order: 12` in its own frontmatter, so inserting one in the middle means editing
every file after it. Add the numbers in titles and filenames and a single
insertion becomes a fifty-place edit that nothing verifies
(`curriculum/DECISIONS_NEEDED.md`, question 5).

An editor built on top of that would be a nice front end for a bad
representation. So the first piece of work is not the editor.

## Step 1 — Order becomes one file per series

```yaml
# tutorials/mit-pdp-maths-prog-integration/maths-and-programming.order.yaml
series: Maths and programming
order:
  - first-steps
  - storing-and-computing
  - making-decisions
```

`order:` leaves the frontmatter. The build reads this list; a tutorial not
listed is not in the series and the build says so.

What that buys, before any editor exists:

- **Reordering is one file and one commit.** Moving a line moves a tutorial.
- **Inserting is one line**, and nothing else changes.
- **A human can do it in the GitHub web editor today**, which is worth having
  even after the editor is built, because it still works when the editor does
  not.
- The editor becomes a small thing: it edits one list.

This step also carries the rename. Filenames lose their numbers
(`tutorial-14-expressions-come-alive.md` → `expressions-come-alive.md`), titles
lose theirs, and the fifty prose references become names rather than numbers.
Published URLs change, which is a real cost and the reason to do it exactly once.

## Step 2 — The editor page

A page in the built site — `editor.html` — that reads the repository through the
GitHub API and writes back a commit.

**Reordering.** The series as a list of cards, drag to reorder, or move up and
down for anyone not using a mouse. Save writes the new `order.yaml` as one
commit on a branch.

**Inserting.** A gap between any two cards, and at the end. Choosing one asks for
a title, makes a slug from it, writes a new markdown file from a template, and
adds it to the list. One commit, two files.

**Creating.** The same as inserting, at the end.

The template matters more than it sounds: it is where the house conventions live
— frontmatter with the fields the build requires, an opening section, a first
exec cell, a `## Reflection` at the end. A new tutorial should start out looking
like the others.

## How it writes

The page holds a **GitHub personal access token**, fine-scoped to contents:write
on `deweydex/dewlab`, in `localStorage`. Then a commit is three API calls.

Being honest about what that means:

- **The token is in the browser.** On Josh's own machine that is a reasonable
  trade; on a shared one it is not. The page should say so plainly, offer a
  "forget this token" button, and never be linked from anywhere students go.
- **Fine-scoped, not classic.** Contents write on one repository. Not a token
  that can do anything else.
- **It commits to a branch and opens a pull request**, never straight to main.
  That keeps the two-author review the access model was designed around, and it
  means a mistake in the editor is a pull request rather than a live site.

The alternative — a GitHub App with proper OAuth — removes the token from the
browser and costs an app registration, a redirect URL, and somewhere to keep a
secret. Worth revisiting if a third person ever edits; overkill for two.

## What it deliberately does not do

**It is not a markdown editor.** Writing a tutorial happens where writing
happens — an editor, an IDE, the GitHub web editor. This page exists for the
things that are painful precisely because they are spread across many files:
order, insertion, creation. Trying to make it a content editor as well would
double its size and halve its chance of being finished.

## Order of work

1. `order.yaml` and the rename. Nothing here needs the editor, and everything
   after it is easier. **This is the piece that unblocks the re-planned series.**
2. The editor page, reordering only. Useful the day it works.
3. Insert and create, with the template.
4. Revisit the token if anyone else needs to edit.
