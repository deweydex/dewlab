# Using dewlab

dewlab is a set of tutorials you read in a browser. Each one mixes an
explanation with small boxes of Python you can change and run yourself, so you
can try an idea out in the same place you are reading about it.

You do not need to install anything, and you do not need an account. The Python
runs on your own computer, inside the browser tab. Nothing you write is sent
anywhere, nothing is marked, and nobody is watching how you get on.

---

## The reading page

A tutorial looks like a page of writing, because most of it is. Set into the
writing are **cells**: small editable boxes of Python with a **Run** button.
Press Run, or Ctrl-Enter, and the result appears directly underneath.

What comes back is whatever the code printed, the value of the last line if it
is an expression, a table drawn as a table, and a chart drawn as a picture. If
something goes wrong, you get an error message trimmed down to your own line
rather than a wall of machinery you did not write.

The cells on one page share their variables from top to bottom, so a cell near
the end can use something a cell near the start set up. Each page starts fresh,
though, so nothing carries over from one tutorial to the next.

If a code box has no Run button, it is there to be read rather than run. That
is the only difference, and it is meant to be visible at a glance.

Some cells have a small **?** beside them. That is a hint, tucked out of the
way until you want it.

Every cell also has a **reset** button, which puts back the code that came with
the tutorial. If you have changed a cell past the point of rescuing it, reset
that one cell and carry on — the rest of the page is untouched.

Some tutorials have no code at all. Those are ordinary dewlab tutorials too,
and they open instantly, because a page with nothing to run never starts Python.

---

## Your work is saved

Everything you type is saved in your own browser as you go, along with the last
output each cell produced. Close the tab, come back a week later, and your work
is waiting.

Because it is saved in the browser, it lives on the machine you were using. It
will not follow you to a different computer, and clearing your browser data
will clear it. If you want a copy you can keep or move, use the export button
described below.

If a tutorial is updated after you have worked on it, your answers carry over
cell by cell wherever the cell has not been replaced. Where a tutorial has more
than one published version, a small picker on the page lets you move between
them, and you stay in the version you were working in rather than being moved
without being asked.

---

## Settings

Every page has a **Settings** button in the bar at the top, and that bar
follows you down the page, so it is always one tap away. What is behind it is
grouped in three parts.

**Your work** — whether the page is saving, and buttons to export a copy of
your work, load one back in, or start the tutorial over.

**This tutorial** — the ways to take the page with you, described below.

**Texture** — how the page looks and reads: light or dark, serif or sans or
mono, text size, how wide the lines run, and the colour of links. There is also
**Header: full or minimal**, which tightens the bar at the top and is worth
knowing about if you are reading on a phone.

These choices follow you from page to page and from visit to visit. If the
default is uncomfortable to read, change it — that is what it is for.

---

## Finding your way around

The **previous / All tutorials / next** row sits with the bar at the top, so
moving on never means scrolling to find the link.

Any tutorial with more than one section has a **Contents** list, closed until
you open it, showing the page's headings with sub-headings nested underneath.

A **Reference** button sits in the page's top-left corner. It opens a panel of
the definitions, functions and formulas this tutorial — and everything before it
in its series — has covered. Nothing appears in it that you have not been taught
yet. On a phone it opens as a sheet across the bottom of the screen.

The contents page lists everything in teaching order and has a search box. Two
other pages cut across that order. The **topic tree** shows every topic in the
course and what each one needs before it; you can drag to move around it, scroll
to zoom, and choose any topic to read what it is and where it turns up. Topics
that are not taught here yet are drawn with a dashed outline, so the tree is
straight with you about its gaps. **Browse by topic** gathers everything on one
subject in one place, which is the better page when you already know what you
want to practise.

On the contents page, a small badge next to a tutorial you have opened shows how
many of its cells you have run, turning red only if a cell's last run failed. It
is read from your own browser, and you can turn it off in Settings.

---

## Practice

Nearly every tutorial has a practice page beside it, linked from the contents
page and from the end of the tutorial. Some pages are mixed sets that draw on
several tutorials at once, for when you want to practise across a few topics
rather than one.

Problems come with two folds. The first is a hint: a few steps, something to
think about, and a related problem to try next. The second is the answer, with
the working. They are in that order on purpose. Opening the hint first and
having a go tends to teach you more than opening the answer, though the answer
is there when you want to check yourself.

---

## Adding your own cells

On any page that already has cells, you can add your own — a Python cell or a
short text note — directly below any cell on the page, not only at the bottom.
Use them for working something out, leaving yourself a note, or trying a
variation on what the tutorial just showed you.

Your own cells are kept separately from the tutorial's, so updating the
tutorial leaves them alone. You can also save one as a small file and send it to
someone else, who can load it into their copy of the same page.

---

## Taking a tutorial with you

Settings offers a few ways to keep a copy.

**Download to keep** gives you one HTML file — on a memory stick, in your
downloads folder, wherever you like — that you open by double-clicking. The
reading, the cells, the editor and the mathematics are all inside it, and it
behaves like the page you downloaded it from. One thing worth knowing: the
first time you open it, it needs an internet connection, because Python itself
is fetched then. Without one, the reading still works and the cells say so
rather than failing quietly.

**Print — or save as PDF** gives you the reading as a document.

**Save as a Jupyter notebook** gives you the page's cells, including any you
added yourself, as a `.ipynb` file you can open elsewhere.

The contents page also offers **Download all N as single files** for a whole
series at once, as a zip. That is the one to use if you are filling a memory
stick or taking a set of tutorials home.

---

## When you want Python without a tutorial

Two workspaces come with dewlab for when you just want somewhere to write code.

**[dewmini](DEWMINI.md)** is the small, quiet one: a blank page, add a cell,
run it. Good for testing an idea or working a problem away from the tutorial it
came from.

**[Mini IDE](MINI_IDE.md)** is the larger one: a file manager, uploading your
own files, a real SQL database, importing a notebook or a `.py` file, and a Stop
button that can interrupt code that has got stuck. Reach for it when something
grows past a few cells.

---

## Something wrong?

If a tutorial has a mistake in it, or something on the site does not work,
please tell us. You do not need to be certain it is a bug to say something.
[`REPORTING_A_PROBLEM.md`](REPORTING_A_PROBLEM.md) explains where to report it
and what is helpful to include.
