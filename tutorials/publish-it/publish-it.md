---
title: "Publishing your site with GitHub Pages"
year: "2026-2027"
version: 2026.09.11.1
covers:
  turning-it-on:
    covers: [WA-LO13]
  why-the-address-looks-the-way-it-does:
    touches: [WA-LO13]
  keeping-it-up-to-date:
    covers: [WA-LO13]
---

# Publishing your site with GitHub Pages

Your repository holds HTML and CSS files. Can anyone visit it as a
website yet? Not yet. GitHub Pages is a free part of GitHub that turns a
repository into a website. On this page we:

- switch GitHub Pages on for your copy of the starter
- read the web address your site gets
- see how the site stays up to date

## Turning it on

1. In your repository, open **Settings**.
2. In the list on the left, choose **Pages**.
3. If there is a **Source** choice, pick **Deploy from a branch**.
4. Choose the branch GitHub should publish from. This is usually `main`.
5. Choose the folder in that branch. This is usually the top level of
   the repository, shown as `/ (root)`, and not a folder inside it.
6. Press **Save**. GitHub starts to build your site.

The first build often takes a minute or two. When it finishes, the
**Pages** screen shows the address where your site now lives. GitHub
may also send you an email about it.

## Why the address looks the way it does

A GitHub Pages site for a personal account follows one pattern:

```text
username.github.io/repository-name
```

What would your own address be? Suppose your username is `janedoe`, and
your repository is `web`. Then your address is `janedoe.github.io/web`.

### The home page is `index.html`

GitHub Pages looks for a file named exactly `index.html`, and shows it
as the home page. What if your main file has a different name? Then
visitors will not see your page. They will get a "404: page not found"
error, or the repository's README file. So rename your main file to
`index.html`.

### Public repository, public site

GitHub Pages needs your repository to be public, unless you are on a
paid plan. This is why the starter is meant to be copied as a public
repository. The published site is public too: anyone with the address
can see it, even when a paid plan publishes it from a private
repository.

## Keeping it up to date

Once Pages is on, how do you update your site?

1. Commit a change to the branch you chose.
2. Wait. GitHub rebuilds the site by itself, usually within a minute or
   two.
3. Refresh your site in the browser. Can you see your change?

There is no separate publishing step to remember. [Saving and publishing
a change](tutorial:the-two-loops) looks at this cycle again, from the
side of the editor.

## What we have now

You now have a live web address, and a website behind it, however small
it is. Anyone with the link can see it. Remember this before you commit
anything you would like to keep private.

- GitHub Pages publishes a website from the files in a repository.
- The address follows the pattern `username.github.io/repository-name`.
- The home page must be a file named `index.html`.
- Each commit to the chosen branch updates the site.
