---
title: "The skeleton: head and body"
year: "2026-2027"
version: 2026.09.11.1
covers:
  how-it-works:
    covers: [WA-LO2]
  in-your-own-site:
    touches: [WA-LO8]
---

# The skeleton: head and body

Every HTML page has two parts: a *head* and a *body*. On this page you
find out what goes in each part, and why some text never appears on the
page itself.

## Try it

The code below has a `<title>` and an `<h1>`. Both say "My page".

```html site
id: skeleton-html
site: skeleton
<title>My page</title>
<h1>My page</h1>
<p>Both lines above say "My page". Only one of them renders below.</p>
```

1. Look at the preview. How many times does "My page" appear?
2. Change the text inside `<title>`. Does the preview change?
3. Now change the text inside `<h1>`. What happens this time?

Only the `<h1>` shows in the preview. The `<title>` text is not lost: on
a real page, it appears in the browser tab.

## How it works

A complete HTML page has this shape:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My page</title>
  </head>
  <body>
    <h1>My page</h1>
    <p>Everything a visitor sees goes here.</p>
  </body>
</html>
```

The page has two parts:

- The *head* holds information *about* the page. A visitor does not see
  it on the page itself. The `<title>` goes here, and the browser shows
  it in the tab.
- The *body* holds everything a visitor sees: headings, paragraphs,
  images, links.

That is why the two "My page" lines behaved differently. `<title>` belongs
in the head, so its text goes to the tab. `<h1>` belongs in the body, so
its text goes on the page.

## In your own site

1. Open `index.html` in your fork.
2. Find the hero section. It has an `<h1>` element that says "Welcome to
   My Portfolio".
3. Change the text to something that describes you. Save, and refresh
   your browser.

**Check:** you have now changed two things in this file.

| You changed | It is in the | It shows up in |
|---|---|---|
| `<title>` (last page) | head | the browser tab |
| `<h1>` (this page) | body | the page itself |

Should the title and the heading say the same thing? Try making them the
same, then different, and decide which works better for your site.

## Summary

- The *head* holds information about the page. Visitors do not see it on
  the page.
- The *body* holds everything visitors see.
- `<title>` goes in the head. Its text appears in the browser tab.
