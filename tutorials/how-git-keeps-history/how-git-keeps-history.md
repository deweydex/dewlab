---
title: "How Git keeps a project's history"
year: "2026-2027"
version: 2026.09.22.1
context_for: [the-two-loops, how-the-pieces-fit, issues-and-pull-requests, your-copy-of-the-starter]
---

# How Git keeps a project's history

What is a commit, and where does it go? Four pages use commits without
looking inside one: [The tools for building a
website](tutorial:how-the-pieces-fit), [Issues and pull
requests](tutorial:issues-and-pull-requests), [Making your own copy of
the starter](tutorial:your-copy-of-the-starter) and [Saving and
publishing a change](tutorial:the-two-loops). This page looks inside.
It is background reading. You do not need it to finish those pages, but
it can help you see why the steps are the way they are.

On this page we:

- see what a commit holds
- see why Git asks us to `add` before we `commit`
- see how commits make a history, and how to look back through it
- see what `push` copies, and what a branch is
- meet Git outside this course

## What a commit holds

*Git* is the program that records the changes to a project's files. A
commit is the record of one moment in the project. It holds:

- a snapshot of the project's files, as they were when the commit was
  made
- a message that says what changed
- the name of the person who made it, and the date and time
- the commit before it, so Git knows the order
- an id, a long string of letters and numbers, such as
  `5f60c9a2e8b41d07c3f9a6e15b2d8c47f0a9e3b1`

A snapshot is the state of every file, not only the changed ones. Git
saves space by storing each version of a file only once, however many
commits share it.

The id is worked out from everything in the commit: the files, the
message, the author, the time and the commit before it. So two
different commits never end up with the same id, and a commit cannot be
changed later without its id changing too. GitHub shows only the first
seven characters, such as `5f60c9a`, because that is enough to tell
commits apart.

## Why `add` comes before `commit`

Sometimes we change two things at once: we fix a spelling mistake in
`about.html`, and we try a new colour in `styles.css`. Those are two
different changes, and each one deserves its own message.

`git add` is how we choose. It puts a change in the *staging area*: a
list of the changes that will go into the next commit. `git commit`
records what is in the staging area, and nothing else. So we can add
`about.html`, commit it as "Fix a spelling mistake", then add
`styles.css`, and commit that as "Try a darker heading colour".

`git status` shows what is in the staging area, and which changed files
are not in it yet. It is a good command to type whenever you are not
sure where a change is.

GitHub's own editor does the `add` for us, because we edit one file at a
time there. That is why a commit on the GitHub website needs one button.

## A line of commits

Each commit points to the one before it, so the commits of a project
form a line. That line is the project's *history*. Here are four
commits, made on one computer, and the same project on GitHub:

![Two rows of commits, drawn as circles joined by a line, with older commits on the left and newer on the right. The top row, on your computer, has four commits, e41b9d2, 7ac03f5, b2d7e18 and 5f60c9a, with the messages: change the page title, rewrite the introduction, add a skills section, add a contact section. A label, main, points at the newest commit. The bottom row, on GitHub, has only the first three commits, and main points at the third. A dashed circle marks where the fourth will go, and an arrow from the fourth commit on your computer down to it says: git push copies the new commit.](commits-and-push.svg)

Because every commit is kept, we can look back at any of them. On
GitHub, a repository's front page has a link above its list of files
that counts its commits. It opens the history, newest first. Clicking a
commit shows exactly what it changed: removed lines in red, and added
lines in green. This is the same view a pull request shows.

Going back does not mean losing work. `git revert` makes a new commit
that undoes an earlier one. The mistake and its fix both stay in the
history, so we can always see what happened and when.

## Two copies of the history, and branches

When you clone a repository, you get the whole history, not only the
newest files. So there are two copies of the history: one on your
computer and one on GitHub. A commit you make on your computer is in
your copy only. `git push` copies the commits that GitHub does not have
yet, as in the picture above. That is the whole job of `push`.

In the picture, a label called `main` points at the newest commit in
each copy. A *branch* is a name for a line of commits, and that name
always points at the newest commit in the line. Each new commit moves
the name along. `main` is the usual name for a repository's first
branch. That is why GitHub Pages asks which branch to publish from: it
publishes the files as they are in the newest commit on that branch.

A repository can have more than one branch, so that someone can try an
idea without touching `main`. A pull request is a proposal to bring the
commits from one branch into another, often from a fork into the
original repository.

This also explains the two buttons on [Making your own copy of the
starter](tutorial:your-copy-of-the-starter). A fork copies the
original's commits, so its history starts with the original's history.
A copy made with **Use this template** takes the files but not the
commits, so its history starts with one new commit of its own.

## Git and GitHub, outside this course

Git and GitHub are two different things. Git is a program. It runs on
your own computer, and it keeps working with no internet connection.
GitHub is a website that keeps Git repositories online, and adds its own
tools around them: issues, pull requests and GitHub Pages. Other
websites do the same job, such as GitLab and Bitbucket.

Git was written in 2005 by Linus Torvalds, to keep track of the code of
Linux, a system that runs on computers all over the world. Many people
work on Linux at once, and Git was built so that each of them could
have a full copy of the history.

These are not tools made only for students. Many people who build
websites and software for a living use Git and GitHub every day, and the
path a change takes, from an editor to a published site, is much the
same for them as it is for us.

## What we have now

We can now say what a commit holds, where it goes, and how to look back
at it.

| Word | Meaning | Example |
|---|---|---|
| *Git* | The program that records the changes to a project's files | `git commit` |
| *snapshot* | The state of every file in a project at one moment, as a commit records it | the files as they were after "Add a skills section" |
| *commit id* | The long string that names one commit. GitHub shows the first seven characters. | `5f60c9a` |
| *staging area* | The list of changes that will go into the next commit. `git add` puts a change there. | `git add about.html` |
| *history* | The line of commits in a repository, each pointing to the one before | the list behind the commits link on GitHub |
| *branch* | A name for a line of commits, which points at the newest one | `main` |

## Where to read more

DevDuck (2019). *Using Git with Unity Tutorial [2019].*
<https://www.youtube.com/watch?v=BlUldSuOgDc>. A game developer shows how
to put a real project into Git, with tips for using it as the work grows.
About four minutes.
