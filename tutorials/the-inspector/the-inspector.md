---
title: "Looking inside a page with the inspector"
year: "2026-2027"
version: 2026.09.11.1
covers:
  opening-the-inspector:
    touches: [WA-LO10]
  the-elements-tab-how-the-page-is-built:
    covers: [WA-LO10]
  the-console-tab-where-errors-show-up:
    covers: [WA-LO10]
---

# Looking inside a page with the inspector

What can we do when a page looks wrong, and we cannot see why? Every
browser has a tool for this. The *inspector* is a tool built into the
browser that shows the HTML and CSS behind a page. It works on your own
site, and on anyone else's. It is often the quickest way to find out why
something looks wrong.

HTML is the language that says what each part of a page is: a heading,
a paragraph, a link. CSS is the language that says how each part looks.
We learn both in the next series, starting with [HTML: tags, elements
and attributes](tutorial:a-page-is-files). For now, it is enough to know
that the inspector shows both of them.

If you are on the data track, this is one of only two pages in this
series you need. The rest of the series is about publishing a website.

On this page we:

- open the inspector
- look at a page's structure in the **Elements** tab
- find errors in the **Console** tab

## Opening the inspector

There are two ways to open it:

- **With the keyboard.** Press `F12`, or `Ctrl+Shift+I` on Windows and
  Linux, or `Cmd+Option+I` on a Mac.
- **With the mouse.** Right-click anything on a page, and choose
  **Inspect**. In some browsers the menu item is called **Inspect
  Element**.

Both ways open the same panel. It sits along one side or the bottom of
the window. The second way also selects the part of the page you
right-clicked.

In Safari on a Mac, the inspector is hidden at first. To turn it on,
open Safari's **Settings**, go to the **Advanced** tab, and switch on the
option for web developer features.

Let's try it on this page:

1. Right-click the heading at the top of this page.
2. Choose **Inspect**.
3. Can you find the words of the heading in the panel that opens?

The panel has several tabs. Two of them matter for now.

## The Elements tab: how the page is built

The **Elements** tab shows the HTML that the browser is using to draw
the page. In Firefox, this tab is called **Inspector**.

This HTML can differ a little from the file you wrote. The browser fixes
small mistakes as it reads a page, and the inspector shows the fixed
version.

Here is what we can do in this tab:

1. Move the mouse over a line in the tree. Which part of the page lights
   up?
2. Click a line to select that element.
3. Look at the panel beside the tree. It lists every CSS rule that
   affects the selected element. A rule that another rule has overruled
   is still listed, and it is shown crossed out.
4. Double-click any piece of text, tag or attribute in the tree, and
   change it. What happens on the page?

The panel of rules is often the quickest way to find out why a style
you wrote is not the one showing on the page. Look for your rule. Is it
in the list? Is it crossed out?

A change we make in this tab exists only in our own browser. It
disappears when we refresh the page, and it never touches the real file.
That makes the Elements tab a safe place to try an idea before we write
it into our code.

## The Console tab: where errors show up

The **Console** tab lists errors and warnings. The browser finds these
while it loads the page. A misspelt file name, a missing CSS file, or a
script that failed will often show up here first, before you notice
anything is wrong. A script is a small program, written in JavaScript,
that runs inside the page.

Sometimes we might open the Console on a site we did not build and see
a long list of warnings. That is normal. Many working sites have some.
On our own site, an error in red is worth reading, because it often
names the file that the browser could not find.

## What we have now

We can now look inside any page, including one that is not yet working
the way we meant it to.

| Part | What it shows | How we use it |
|---|---|---|
| *inspector* | The HTML and CSS behind a page | Open it with `F12`, or right-click and choose **Inspect** |
| **Elements** tab | The HTML the browser is using, and the CSS rules for each element | Find which rule wins, and try changes safely |
| **Console** tab | Errors and warnings from loading the page | Find missing files and failed scripts |

[Troubleshooting](tutorial:troubleshooting) uses this tool all the way
through. Next time something does not look right, open the inspector
beside it.
