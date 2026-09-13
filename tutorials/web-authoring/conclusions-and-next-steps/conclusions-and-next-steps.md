---
title: "Conclusions and Next Steps"
slug: conclusions-and-next-steps
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: several-pages
version: 2026.09.12.1
covers:
  how-html-and-css-got-here:
    covers: [WA-LO1]
  other-ways-to-build-a-website:
    covers: [WA-LO5]
  give-it-a-try:
    touches: [WA-LO5]
---

# Conclusions and Next Steps

The site you documented on the last page is real: written by hand, tag
by tag and rule by rule, and published where anyone with the address can
open it. That is worth pausing on before moving anywhere else. This
page looks back at how HTML and CSS got to be the way they are, then
looks at other ways people build a website, so the choice this course
made — writing both by hand — reads as one choice among several rather
than the only one there is.

## How HTML and CSS got here

Tim Berners-Lee wrote the first version of HTML in 1993, with about
eighteen tags. HTML 2.0 followed in 1995, the first version treated as
a real standard. HTML 3.2 came in 1997, then HTML 4.01 in 1999. After
that, HTML's development stalled for years, until a group of browser
makers broke away in 2004 to keep improving it on their own. Their
work became HTML5: a public draft in 2008, an official standard in
2014, and now a *living standard*, a document updated as the web
changes rather than replaced by a numbered version every few years.
There is no HTML6 waiting to happen; HTML5 keeps growing instead.

CSS has a shorter, steadier history. CSS1 arrived in 1996, with colours,
fonts and basic backgrounds. CSS2 followed in 1998, adding
positioning — the same `position` property [this
course](tutorial:position-and-the-sticky-header) already covers. CSS2.1
tidied up inconsistencies between browsers in 2011. After that, CSS
stopped shipping as one single specification at all. Flexbox and grid,
both taught earlier in this course, are two of the many separate
modules CSS3 split into — each one developed, tested and released on
its own schedule, rather than the whole language waiting on all of them
together.

A *deprecated* tag or property is one a browser still understands but
no longer recommends, usually because CSS took over its job. `<center>`
positioned text before `text-align` existed; `<font>` set a typeface
and colour before CSS could style text at all. Both still work in most
browsers today. Neither belongs in a page written now.

## Other ways to build a website

Everything in this course used one specific method: a text editor,
hand-written HTML and CSS, and GitHub Pages turning a repository's own
files into a real website. That is a genuine choice, not the only way
a website gets built.

GitHub Pages itself is a *website management system* in the loose sense
that phrase is usually meant, even though it never felt like one while
you were using it: it takes files from a repository and manages the
job of serving them at a real address, for free, with no server of your
own to set up.

**WordPress** is the way a large share of the web actually gets built.
It stores a site's content in a database rather than in files, and a
theme decides how that content looks. Adding a page or a blog post
means filling in a form, not writing HTML — the theme and WordPress
itself generate the page each time a visitor asks for it.

Two much simpler tools solve a narrower problem well. **Carrd** builds
a single page — pick a template, add your own text and images, publish.
It suits a portfolio, an event page or a simple business card of a
website, and nothing that needs more than one page. **Solo** goes a
step further and drafts a whole small site from a short description you
give it, images included, which you then edit into your own words. Both
trade some control for speed: neither one asks you to write a line of
HTML, and neither lets you change something outside what its own
interface offers.

## Give it a try

Take the site you built in this course and imagine rebuilding it in one
of these tools — Carrd is free to try and quick to test with. Notice
what takes less time, and notice what you cannot do that you could do
by hand: a specific spacing, an animation, a layout the template does
not offer. Neither answer is wrong. A GitHub Pages site you wrote
yourself and a Carrd page you assembled from a template solve the same
problem in different amounts of time, with different amounts of
control traded away.

What does not change between any of these tools is what a browser
actually receives: HTML and CSS, however they were produced. A
WordPress theme, a Carrd template and the pages you wrote by hand this
course all become the same two languages once they reach a browser.
Knowing how to read and write them directly, the way this course
taught, is what makes any of the other tools easier to understand
rather than harder — the choice going forward is which tool fits a
given job, not which one to learn first.

## What you have now

- **HTML and CSS both moved from a single numbered release to an
  ongoing one.** HTML5 is a living standard with no successor number
  waiting; CSS3 split into modules released on their own schedules.
- **Deprecated** means a browser still supports something it no longer
  recommends, usually because CSS replaced what it did.
- **A website management system, a CMS, and a single-page builder are
  three different trade-offs.** GitHub Pages manages files you wrote;
  WordPress generates pages from a database and a theme; Carrd and
  Solo build a page for you from a template or a description.
