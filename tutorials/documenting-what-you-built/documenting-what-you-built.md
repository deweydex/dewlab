---
title: "Documenting what you built"
year: "2026-2027"
version: 2026.09.11.1
covers:
  what-readmemd-is-for:
    covers: [WA-LO6]
  what-maintenancemd-is-for:
    covers: [WA-LO11]
  now-in-your-own-site:
    touches: [WA-LO6, WA-LO11, WA-LO14]
---

# Documenting what you built

Imagine you open a stranger's repository. It has no `README`. How do
you find out what the project is? You have to read every file. That
includes you, six months from now, opening your own project again. A
short document at the top saves all that reading, for a stranger and
for your future self.

Your fork has three documents about your site. You wrote the first,
`planning.md`, before building. On this page we look at the other two,
`readme.md` and `maintenance.md`, and fill them in once your site is
built.

## What readme.md is for

A *README* is a document that explains a project to someone opening it
for the first time. How is it different from `planning.md`? The two
are written at different times, and they say different things:

| Document | When we write it | What it says |
|---|---|---|
| `planning.md` | before any code | what you meant to build |
| `readme.md` | after the site is built | what you actually built |

`readme.md` says what the site covers and how its pages connect. It
describes the design choices you made, and why. It also records how you
tested the site.

The plan and the README rarely match exactly. That is normal. A plan
changes once building starts. `readme.md` records what you built, and
the plan shows what you expected to build.

## What maintenance.md is for

A site does not stay finished. Links move. Information goes out of date.
New pages get added. A *maintenance plan* says how you would keep a site
current. In your fork, it lives in `maintenance.md`. It answers three
questions:

1. How would you add a page later?
2. What would you check every so often?
3. What would you build next, if you kept going?

Nobody expects you to do that work after you submit the project. The
brief marks whether you have thought it through.

## Now in your own site

1. Finish building all five pages of your site first.
2. In your fork of `project_wad`, open `readme.md`.
3. Fill it in: what the site is, how the pages connect, your colour and
   layout choices, and what you tested.
4. Open `maintenance.md`, and write a short, realistic plan.
5. Rename `readme.md` to `README.md`. If your fork already has a
   `README.md`, copy the contents of `readme.md` into it instead,
   replacing what is there. GitHub shows `README.md` on your
   repository's front page.

Now open your repository on GitHub. Could a stranger tell what your site
is about, without opening a single HTML file?

## What we have now

We can now leave a repository that explains itself, from the plan that
started it to the record of what it became.

| Word | Meaning | Example |
|---|---|---|
| *README* | A document that explains a project to someone opening it for the first time | `README.md` |
| `readme.md` | Your site's README, written after building it | what the site covers, and how you tested it |
| *maintenance plan* | A short plan for keeping a site current after it is submitted | `maintenance.md` |
