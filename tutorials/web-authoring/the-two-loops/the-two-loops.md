---
title: "The two loops"
slug: the-two-loops
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: welcome
version: 2026.09.11.1
covers:
  the-local-loop-save-and-refresh:
    touches: [WA-LO13]
  the-github-loop-commit-push-and-wait:
    touches: [WA-LO13]
  telling-the-two-apart:
    touches: [WA-LO13]
---

# The two loops

[How the pieces fit](tutorial:how-the-pieces-fit) named two loops without
explaining either. You now have an account, a copy of the starter, and a
published site to try them on. Here is how each one runs.

## The local loop: save and refresh

Working on a file follows the same short cycle every time, whichever
editor you use.

First, open the file and change something in it. Then save the file: in
most editors, `Ctrl+S` on Windows or `Cmd+S` on a Mac. Then look at it in
a browser, either by opening the file directly or, if it is already
published, by refreshing the page.

Nothing you do in this loop leaves your own computer, or GitHub's editor
if that is where you are working. A browser will not show an unsaved
change. It will also not show a saved change until you tell it to look
again. Both halves of that surprise people at first, in opposite
directions.

## The GitHub loop: commit, push, and wait

Publishing a change needs three separate actions, in this order: `git
add`, `git commit`, and `git push`, or their equivalents in whichever
interface you are using. Changing a file on its own is not enough.
Skipping any one of the three means the file never reaches GitHub, even
if the other two ran without an error.

GitHub's own website simplifies this. Editing a file there already does
the equivalent of `add`. Scroll down after your edit to the "Commit
changes" section, write a short message describing what changed, and
press the button. That single action is usually enough, since GitHub
adds and pushes for you.

Once a commit reaches GitHub, and if GitHub Pages is switched on for that
repository, the published site rebuilds on its own. This typically takes
a minute or two, so a change you just pushed will not always be visible
the instant you refresh. Waiting briefly and refreshing again usually
resolves it.

## Telling the two apart

A useful habit: if a change is not showing up, ask which loop you are
in. Still editing locally means you need to save and refresh. Already
committed means you need to wait for GitHub, then refresh. Confusing the
two is the single most common reason a change "isn't working" when
nothing is actually wrong.

## What you have now

A way to make a change, and to know why it has or has not appeared yet.
[The inspector](tutorial:the-inspector) covers what to do once a page
looks different from how you expected, whichever loop you are in.
