---
title: "The browser inspector"
slug: the-inspector
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: welcome
version: 2026.09.11.1
covers:
  opening-it:
    touches: [WA-LO10]
  elements-the-pages-actual-structure:
    covers: [WA-LO10]
  console-where-errors-show-up:
    covers: [WA-LO10]
---

# The browser inspector

Every browser has a tool that shows you the HTML and CSS actually
running a page, on your own site or anyone else's. It is called the
*inspector*, and it is the fastest way to find out why something looks
wrong. If you are on the data track, this is one of only two pages in
this series you need. The rest is about publishing a website.

## Opening it

Press `F12`, or `Ctrl+Shift+I` on Windows and Linux, or `Cmd+Option+I` on
a Mac. Alternatively, right-click anything on a page and choose
**Inspect**. Both open the same panel, usually docked to one side or the
bottom of the window. The second method also selects whatever you
clicked on.

The panel has several tabs. Two matter for now.

## Elements: the page's actual structure

The **Elements** tab, called **Inspector** in Firefox, shows the HTML the
browser is currently using to draw the page. This can differ slightly
from the file you wrote, since the browser fixes small mistakes as it
reads a page.

Click an element in this tree, and the matching part of the page
highlights so you can see exactly what you selected. Alongside the tree,
a panel lists every CSS rule affecting that element, including ones
overridden by something more specific. This is usually the fastest way
to find out why a style you wrote is not the one actually showing.

You can also double-click any piece of text, tag or attribute in this
tab to change it. The change only exists in your browser; it disappears
on refresh and never touches the real file. This makes the Elements tab
a safe place to try an idea before writing it into your code.

## Console: where errors show up

The **Console** tab lists errors and warnings the browser found while
loading the page. A misspelled file name, a failed script, or a missing
CSS file typically shows up here first, before you notice anything is
wrong.

## What you have now

A way to look inside any page, including one that is not yet working the
way you meant it to. [Troubleshooting](tutorial:troubleshooting) leans on
this tool throughout; open the inspector alongside it the next time
something does not look right.
