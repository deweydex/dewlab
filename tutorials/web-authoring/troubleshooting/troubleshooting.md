---
title: "Troubleshooting"
slug: troubleshooting
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: shelf
version: 2026.09.11.1
covers:
  a-page-or-a-style-doesnt-look-right:
    covers: [WA-LO10]
  my-code-has-a-mistake-i-cant-find:
    covers: [WA-LO10]
---

# Troubleshooting

Something not working is the normal shape of building a website, not a
sign you have done anything wrong. This page groups the problems people
meet most often, each with the checks that usually find it.

Changing one thing at a time can help us see which change makes a
difference.

## A page or a style doesn't look right

### The page is blank

A blank page usually means the browser could not make sense of the file.

- Check the browser's address bar. Is it the file you have been editing?
  A different file may explain why your text is missing.
- Open the file in a text editor and check it starts with
  `<!DOCTYPE html>`, and that `<html>`, `<head>` and `<body>` are all
  there.
- Check that content sits between the opening and closing `<body>` tags,
  not outside them.

[The skeleton](tutorial:the-skeleton) shows the parts of an HTML page
if you want an example to compare.

### The CSS isn't doing anything

The browser may be unable to find your stylesheet. These checks usually
find it:

- Does the `href` in the `<link>` tag match the CSS file's name and
  folder?
- Is that `<link>` tag inside `<head>`, not `<body>`?
- Does the CSS file have a missing semicolon or an unclosed `{` near the
  top? One mistake there can stop everything below it from working.

[A rule and where it lives](tutorial:a-rule-and-where-it-lives) shows
how an HTML page links to CSS.

### Only some of the styles apply

When one rule works and another does not, two rules are usually
disagreeing about the same element.

- Does the selector match the element you meant? A rule for `.card`
  does nothing to an element with no `class="card"`.
- Two rules can both match one element. A more specific selector, such
  as a class name, usually takes priority over a tag name. The
  [inspector](tutorial:the-inspector) can show which rules the browser
  uses.
- Does every value have its unit? `font-size: 16;` does nothing;
  `font-size: 16px;` works.

### An image won't show

- Does the `src` match the image's file name and folder, including
  capital letters? `Photo.jpg` and `photo.jpg` are different files on
  many systems.
- Does the file extension match what is actually saved, such as `.jpg`
  against a file really saved as `.png`?
- The `alt` text still shows if the image itself fails to load. If you
  see the alt text where the picture should be, the path is wrong, not
  the file.

### My file won't open in the browser

This is usually a file extension problem rather than anything wrong with
the page itself.

- Check the file ends in `.html`, not `.txt` or `.doc`. A browser only
  recognises a page by its extension.
- If it opens in a text editor instead of a browser, the **Open with**
  option in your file manager lets you choose a browser.
- You can also open a file from inside the browser itself: `Ctrl+O`
  on Windows or `Cmd+O` on a Mac.

## My code has a mistake I can't find

A page can look almost right and still hide one small error. These are
the three that cause most of the trouble.

### An unclosed tag

Every opening HTML tag needs a closing one, or the browser misreads
everything that follows it.

```html
<!-- Correct -->
<p>This paragraph ends where it should.</p>

<!-- Incorrect: the closing tag is missing -->
<p>This paragraph never ends, so everything after it
```

Work through the file from the top and check that each tag you opened
has a matching close in the right place. `<img>` and `<br>` are the
exception: they never need a closing tag.

### An unclosed brace in CSS

A missing `}` breaks every rule that comes after it, not just the one it
belongs to.

```css
/* Correct */
p {
    color: blue;
}

/* Incorrect: the closing brace is missing */
p {
    color: blue;
```

Most code editors highlight the brace that matches the one your cursor
is on. We can use that to check each `{` has a `}` where we expect it.

### A missing semicolon

In CSS, each property ends with a semicolon. A missing one can stop the
next property from working.

```css
/* Correct */
p {
    color: blue;
    font-size: 16px;
}

/* Incorrect: the missing semicolon stops both properties */
p {
    color: blue
    font-size: 16px;
}
```

## Nothing changed after I edited something

### The page still shows the old version

We can check the steps between editing a file and seeing its result:

1. Is the file saved? Some editors show a dot on the tab for unsaved
   changes.
2. Has the browser loaded it again? Refreshing loads the page again.
3. Is the browser showing the file you edited? Two copies can have
   similar names.

If refreshing does not help, try a *hard refresh*: `Ctrl+F5` on Windows
or `Cmd+Shift+R` on a Mac. Browsers sometimes keep an older copy of a
page, and a hard refresh clears it.

### GitHub Pages still shows the old version

Publishing takes a minute or two after you push, so the delay itself is
normal. Once that time has passed, these questions usually help:

- Are the changes on GitHub? Saving a file on your computer does not
  send it there.
- Are they on the branch used for publishing? The publishing branch is
  usually called `main`.
- Does a hard refresh show the new version?

[The two loops](tutorial:the-two-loops) explains saving and publishing.

## GitHub won't take my changes

- A push needs you to be signed in. If there is a sign-in message,
  signing in through your editor or the GitHub website usually helps.
- `git add`, `git commit` and `git push` are three separate steps.
  Skipping any one of them means the file never reaches GitHub, even if
  the other two ran without an error.
- GitHub can reject a push with a message about the remote having
  changes you do not have. Pull first, then push again.

The error message, the action you tried, and what happened are useful
details if you ask your teacher for help. You do not need to understand
the message before asking.

## My SQL work is missing

Every cell — Python, SQL, or an HTML, CSS or JavaScript site editor —
saves its own code and its last result in this browser as you go, so
nothing here needs a separate save step. **Reset** restores one cell to
the code the tutorial started with; it does not touch a table an earlier
cell built or a variable an earlier cell set.

If the saved code is gone, these are the usual causes:

- A different browser or device. The saved copy does not move between
  them.
- Cleared browser data. That removes it.
- Browser settings or full storage blocking saving.

**Settings** offers ways to keep a copy outside the browser — a
downloadable HTML file, a printed or PDF version, or your cells as a
Jupyter notebook. The [FAQ](tutorial:faq) explains saving and resetting
in more detail.

## This site itself

### The Settings panel doesn't do anything

The **Settings** button opens choices for colours, font, text size, and
line width. Changes apply as soon as you make them, without closing the
panel. Your choices are saved in this browser, so they will not follow
you to a different browser or device.

### The search box finds nothing

**Search** matches a tutorial's title and the terms that tutorial
introduces, not every word in its prose. Try the name of the topic
instead: "flexbox" rather than a sentence about it.

## Still stuck

You can ask your teacher to look at the problem with you. The page
name, the step you tried, and what happened are useful details to share.
You can also return to the tutorial and read the step again.

If the instructions on this site are unclear, the report link at the
bottom of most pages lets you tell us which part needs help.
