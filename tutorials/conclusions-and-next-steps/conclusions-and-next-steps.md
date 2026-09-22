---
title: "Conclusions and Next Steps"
year: "2026-2027"
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

On the last page you documented your site. That site is real. You wrote
it by hand, tag by tag and rule by rule, and anyone with the address can
open it. On this page we look back at how HTML and CSS came to be.
Then we look at other ways people
build a website. Writing HTML and CSS by hand is one choice among
several.

## How HTML and CSS got here

Tim Berners-Lee described the first version of HTML in 1991, with
about eighteen tags. Here is what came after:

| Year | HTML |
|---|---|
| 1995 | HTML 2.0, the first version treated as a real standard |
| 1997 | HTML 3.2 |
| 1999 | HTML 4.01 |
| 2004 | Progress had stalled for years, so a group of browser makers broke away to keep improving HTML on their own |
| 2008 | Their work, HTML5, appears as a public draft |
| 2014 | HTML5 becomes an official standard |

Today HTML is a *living standard*: a document that is updated as the
web changes. There is no HTML6 waiting to happen. HTML5 keeps growing
instead.

CSS has a shorter, steadier history:

| Year | CSS |
|---|---|
| 1996 | CSS1: colours, fonts and basic backgrounds |
| 1998 | CSS2 adds positioning, the same `position` property we met on [A header that stays in view as you scroll](tutorial:position-and-the-sticky-header) |
| 2011 | CSS2.1 tidies up differences between browsers |

After CSS2.1, CSS stopped coming out as one single specification. CSS3
split into many separate *modules*, each developed, tested and released
on its own schedule. Flexbox and grid are two of them.

A *deprecated* tag or property is one that browsers still understand,
but the standard no longer recommends. Usually CSS took over its job.
Two examples:

- `<center>` centred content on the page, before CSS had `text-align`.
- `<font>` set a typeface and a colour, before CSS could style text at
  all.

Both still work in most browsers. Neither belongs in a new page.

## Other ways to build a website

Everything in this course used one method: a text editor, HTML and CSS
written by hand, and GitHub Pages turning a repository's files into a
real website.

A *website management system* is a tool that takes your files or
content and publishes them as a website. GitHub Pages is one, in the
loose sense of the phrase, even if it never felt like one. It serves the
files from a repository at a real address, for free, with no server of
your own.

**WordPress** builds a large share of the web. It is a *content
management system*, or CMS. It keeps a site's content in a database,
and a *theme* decides how that content looks. To add a page or a blog
post, you fill in a form, with no HTML. WordPress and the theme build
the page each time a visitor asks for it.

Two much simpler tools do a smaller job well:

- **Carrd** builds a single page. You pick a template, add your own text
  and images, and publish. It suits a portfolio, an event page or a
  simple online business card. It does not suit a site that needs a
  second page.
- **Solo** goes a step further. From a short description, it drafts a
  whole small site, with images. Then you edit it into your own words.

Both tools trade some control for speed. Neither asks you to write a
line of HTML. Neither lets you change anything outside what its own
screens offer.

## Give it a try

1. Take the site you built in this course.
2. Imagine rebuilding it in one of these tools. Carrd is free to try,
   and quick to test with.
3. What takes less time?
4. What could you do by hand that the tool cannot do? Think of a
   particular spacing, an animation, or a layout the template does not
   offer.

Neither answer is wrong. A site you wrote yourself and a Carrd page
built from a template solve the same problem, with different amounts of
time and control.

What stays the same across all these tools? What a browser receives:
HTML and CSS, however they were made. A WordPress theme, a Carrd
template and your own pages all reach the browser as the same two
languages. You can read and write them directly now, and that makes
every other tool easier to understand. From here, the question is which
tool fits a given job.

## What we have now

We can now place the HTML and CSS we wrote in their history. We can also
compare hand-written pages with a CMS, and with builders like Carrd and
Solo that trade control for speed.

| Word | Meaning | Example |
|---|---|---|
| *living standard* | A standard that is updated as the web changes, with no new numbered version | HTML5 |
| *module* | One separate part of CSS, released on its own schedule | Flexbox, grid |
| *deprecated* | Still understood by browsers, but no longer recommended, usually because CSS replaced it | `<center>`, `<font>` |
| *website management system* | A tool that publishes your files or content as a website | GitHub Pages |
| *content management system (CMS)* | A website management system that builds pages from a database and a theme | WordPress |
