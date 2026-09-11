---
title: "Publish it"
slug: publish-it
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: welcome
version: 2026.09.11.1
covers:
  turning-it-on:
    covers: [WA-LO13]
  why-the-address-looks-the-way-it-does:
    touches: [WA-LO13]
  keeping-it-up-to-date:
    covers: [WA-LO13]
---

# Publish it

A repository of HTML and CSS files is not yet a website anyone can visit.
GitHub Pages is the switch that turns it into one, and it is free.

## Turning it on

In your repository, open **Settings**, then **Pages** in the sidebar.
Choose the branch GitHub should publish from, usually `main`, and the
folder within it, usually the repository's root rather than a
subfolder. Save that choice, and GitHub starts building your site.

This first build typically takes a minute or two. Once it finishes,
GitHub shows the address your site now lives at and generally emails you
too.

## Why the address looks the way it does

A personal GitHub Pages site follows one pattern:
`username.github.io/repository-name`. If your username is `janedoe` and
your repository is `web`, your address is `janedoe.github.io/web`.

GitHub Pages looks for a file named exactly `index.html` and serves it as
the homepage. If your main file is named anything else, rename it, or
visitors will see a directory listing instead of your page.

The connection runs the other way too. GitHub Pages generally needs a
repository to be public, unless you are on a paid plan. The starter is
meant to be forked as a public repository for exactly this reason.

## Keeping it up to date

Once Pages is switched on, commit a change to the branch you chose.
GitHub rebuilds the site on its own, usually within a minute or two.
There is no separate publishing step to remember. [The two
loops](tutorial:the-two-loops) covers this update cycle from the editing
side.

## What you have now

A live address, and a website behind it, however small. Anyone with the
link can see it, which is worth remembering before you commit anything
you would rather keep private.
