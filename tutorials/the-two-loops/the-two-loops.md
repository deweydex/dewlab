---
title: "Saving and publishing a change"
year: "2026-2027"
version: 2026.09.11.1
covers:
  on-your-computer-save-and-refresh:
    touches: [WA-LO13]
  on-github-commit-push-and-wait:
    touches: [WA-LO13]
  why-is-my-change-not-showing:
    touches: [WA-LO13]
---

# Saving and publishing a change

[The tools for building a website](tutorial:how-the-pieces-fit) followed
one change from your editor to your published site. That path has two
loops in it. A loop is a short set of steps that we repeat many
times. One loop happens on your own computer, and one happens on
GitHub.

You now have an account, a copy of the starter, and a published site.
On this page we:

- walk through the loop on your computer
- walk through the loop on GitHub
- use the two loops to work out why a change is not showing yet

## On your computer: save and refresh

Working on a file follows the same short cycle every time, whichever
editor you use:

1. Open the file, and change something in it.
2. Save the file. In most editors, the keys are `Ctrl+S` on Windows and
   `Cmd+S` on a Mac.
3. Look at the file in a browser. The first time, open the file in the
   browser directly. After that, refresh the browser tab to see each new
   change.

Nothing in this loop leaves your own computer. Your published site stays
the same until the change goes through the second loop, on GitHub.

Two things in this loop surprise most people at first. A browser does
not show a change you have not saved. And it does not show a saved
change either, until you refresh the page and the browser reads the file
again.

What if you work in GitHub's editor, on the GitHub website? Then there
is no separate save on your computer. Saving a file there makes a
commit on GitHub, so you go straight to the second loop.

## On GitHub: commit, push and wait

A change reaches GitHub in three separate actions, in this order:

1. `git add` chooses which changed files go into the next commit.
2. `git commit` records those changes as a commit, with a short message
   that says what changed.
3. `git push` sends your commits to GitHub.

These are Git commands. We type them in a terminal, a window for
typing commands to the computer. VS Code's **Source Control** panel
has the same three actions as buttons, and other editors have their own
versions. Changing a file is not enough on its own. If
you skip any one of the three actions, the change never reaches GitHub,
even when the other two run without an error.

GitHub's own editor needs fewer steps:

1. Edit the file on the GitHub website.
2. Press **Commit changes**.
3. Write a short message that says what changed.
4. Confirm the commit.

That one commit is enough. GitHub does the work of `add` and `push` for
you, because the file is already on GitHub.

### Waiting for the site to rebuild

Once a commit reaches GitHub, and GitHub Pages is switched on for that
repository, the published site rebuilds on its own. This takes a minute
or two. So a new change may not appear the moment you push it and
refresh. Wait a little, then refresh again.

## Why is my change not showing?

When a change does not show up, a good first question is: which loop am
I in?

| Where the change is | What to do next |
|---|---|
| Changed in the editor, not saved | Save the file, then refresh the browser. |
| Saved on your computer, not committed | Commit and push it, if you want it on your published site. |
| Committed and pushed to GitHub | Wait a minute or two for the site to rebuild, then refresh. |

Oftentimes, a change that "isn't working" is fine. It has only
finished one loop, and we are looking for it at the end of the other
one. For example, we save a file on our computer, then refresh the
published site and wonder why nothing changed. The change is real, but
it has not been pushed yet.

## What we have now

We can now make a change, and work out why it has or has not appeared
yet.

| Loop | Where it happens | Steps |
|---|---|---|
| Save and refresh | On your own computer | Change the file, save it, refresh the browser. |
| Commit, push and wait | On GitHub | `git add` chooses the files, `git commit` records the change, `git push` sends it, and GitHub Pages rebuilds the site. |

In GitHub's editor, each commit goes straight to GitHub, so we only need
the second loop.

Sometimes a page appears, but it looks different from what we
expected. [Looking inside a page with the inspector](tutorial:the-inspector) shows us what
to do then, whichever loop we are in.
