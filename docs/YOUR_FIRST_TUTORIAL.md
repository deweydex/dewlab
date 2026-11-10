# Your first tutorial

This page takes you from nothing to a tutorial you can send for review. It is
for a teacher or a course author. You do not need to know Git, and you do not
need to be a programmer to write the words; the code cells are copied from a
template and you change them.

Plan for about an hour for the first time, most of it setting up. After that,
a new page starts in one minute.

If you only want to fix a typo or a sentence on a page that already exists,
you do not need any of this. [`EDITING_A_PAGE.md`](EDITING_A_PAGE.md) shows how
to change it in your browser.

## Words used on this page

- **Terminal**: a window where you type a command and press Enter. On Windows
  it is called PowerShell. On a Mac it is called Terminal.
- **Repository**: the project's folder of files, kept on GitHub.
- **Pull request**: your proposal to add your files to the project. Somebody
  reads it before anything changes for students.
- **Tutorial id**: the folder name, like `first-steps`. It is the page's web
  address, and each student's saved work is stored under it. Choose it once.

## Once: get the project

You need [Python](https://www.python.org/downloads/) (version 3.12 or later),
[Git](https://git-scm.com/downloads) and a free [GitHub](https://github.com)
account.

**If you were invited to work on the project**, copy it to your computer:

```bash
git clone https://github.com/deweydex/dewlab
cd dewlab
```

**If you were not invited**, which is most people and is how it should be, make
your own copy first. Open the project on GitHub and press **Fork**. GitHub makes
a copy under your name. Then copy that one to your computer, using your own user
name in the address, and tell Git where the original is:

```bash
git clone https://github.com/YOUR-USER-NAME/dewlab
cd dewlab
git remote add upstream https://github.com/deweydex/dewlab
```

Either way, then install what the project needs:

```bash
pip install -r requirements-dev.txt
```

## 1. Make the page

First make a branch, which is a separate line of work for this one change:

```bash
git switch -c add-my-tutorial
```

Then make the page:

```bash
python3 new.py my-tutorial "A title for it"
```

Choose the id with small letters, digits and hyphens: `fractions-on-a-number-line`,
not `Fractions Lesson 1`. The command makes a folder in `tutorials/` named for your id,
with the tutorial and its practice page inside. Both are copies of a working
example, with your title, today's date as the version, and this school year.

## 2. Look at it

```bash
python3 build.py --serve
```

This builds the site, which takes about half a minute, and then prints an
address: `http://localhost:8000/`. Open it in your browser. Your page is at the
address with `/tutorials/<id>.html` added, where `<id>` is the id you chose.

The address works only on your own computer. Nobody else can open it.

To see a change you make, press Ctrl-C in the terminal to stop it, and run the
same command again.

## 3. Write

Open `tutorials/<id>/<id>.md` in any text editor. The grey notes
in `<!-- -->` comments say why each part of the example is there. Read each one,
change the content, and delete the note.

Three things to keep:

- **Start by running something and asking about it.** Do not start by defining
  a word. The page then names the idea once the reader has seen it.
- **One idea, about an hour of somebody's evening.**
- **Every cell has an `id:` as its first line.** Once students have saved work
  under a cell id, do not change it. [`CHECK_YOUR_WORK.md`](CHECK_YOUR_WORK.md)
  has the checklist.

The [style guide](../planning/PEDAGOGICAL_STYLE_GUIDE.md#who-reads-this) says
who reads these pages: adults coming back to education, some reading in a
second language, some with a screen reader. Write for the person at home at ten
at night, when nobody can answer a question. Its
[checklist](../planning/PEDAGOGICAL_STYLE_GUIDE.md#checklist) is short and is
worth reading before you send anything.

### So that every reader can use the page

- **A description on every picture.** Put the words in the square brackets:
  `![A table sorted by date](a-sorted-table.png)`. If a picture is only
  decoration, leave the brackets empty. The build stops on a picture tag with
  no description at all.
- **Real headings, in order.** Use `##` for a section and `###` inside it. Bold
  text is not a heading, and a screen reader cannot jump to it.
- **Colour is never the only signal.** If a line is red, say in words what the
  red means.
- **Short paragraphs, plain words.** A sentence a reader has to read twice is
  too long for the person reading in their second language.

## 4. Put it on a course

Until you do, the page builds, but no course page links to it. Open the file
for your course in `courses/`, for example `courses/computational-methods.yaml`,
and add your id to the right list:

```yaml
contents:
  - title: Python fundamentals
    tutorials: [first-steps-cm, my-tutorial, storing-and-computing]
```

The order of the list is the reading order.
[`WRITING_TUTORIALS.md`](WRITING_TUTORIALS.md) explains courses and series.

## 5. Check it

```bash
python3 check.py tutorials/my-tutorial
```

It reads your page the way the build does. Then it runs your page: each cell
in order, and each answer you wrote in a `solution` block. It tells you in
plain words what to fix. A line that starts with **Problem** must be fixed. A
line that starts with **Note** is only something good to know.

Run it again after each fix. It takes about a quarter of a minute.

## 6. Send it

```bash
python3 check.py tutorials/my-tutorial --pr
```

When there are no problems, this commits your files, pushes them to your copy,
and opens GitHub's page for a new pull request to the project, with the title
and description already written. Read them, change what you like, and press the
green button.

The pull request asks you two questions: what changes, and why. If you chose
between two ways of doing something, say which you chose and why. That is where
the project keeps its reasons.

Somebody reads your pull request and may ask you to change something. Nothing
reaches students until it is approved and merged. [`CHECK_YOUR_WORK.md`](CHECK_YOUR_WORK.md)
says more about this step.

## When you are stuck

- A **Problem** line you do not understand: copy it into an
  [issue](https://github.com/deweydex/dewlab/issues/new) and say which command
  you ran.
- A block you have not used before (a prediction, a solution, a choice of
  world): [`WRITING_TUTORIALS.md`](WRITING_TUTORIALS.md#blocks) has each one,
  and `docs/templates/` has a working example of every page shape.
- How the whole project fits together: [`../README.md`](../README.md).
