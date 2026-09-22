---
title: "The head and body of a page"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# The head and body of a page

On the last page we changed the `<title>` element in your fork. Let's
look more closely at it this time. Why does some text on a page never
appear on the page itself?

## Let's try it

The code below has a `<title>` and an `<h1>`. Both say the same words.

```html site
id: skeleton-html
site: skeleton
<title>My page</title>
<h1>My page</h1>
<p>Both lines above say "My page". Only one of them renders below.</p>
```

1. Before changing anything, look at the preview. How many times does
   "My page" appear?
2. What if we change the text inside `<title>`? Does the preview change?
3. What about the text inside `<h1>`?

The `<h1>` text appears. The `<title>` text does not. Where do you think
it went? On a real page, it shows up in the browser tab instead, not in
the page itself.

## Why does this happen?

Every HTML page splits into two parts. Here is a whole page, so we can
see both:

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

- The *head* holds information about the page: its `<title>`, and other
  details a visitor does not see directly.
- The *body* holds everything a visitor sees: headings, paragraphs,
  images, and the rest.

Now we can explain what we saw. `<title>` lives in the head, which is
why its text goes to the browser tab and not to the page. `<h1>` lives
in the body, with all the other visible content.

## Now in your own site

We are back in `index.html` in your fork.

1. Inside the hero section there is an `<h1>` element. It says "Welcome
   to My Portfolio".
2. What would represent you better? Change the text to that.
3. Save, and refresh.

We have now made two changes. How do they compare?

| What we changed | It lives in the | It changed |
|---|---|---|
| `<title>`, on the last page | head | the browser tab |
| `<h1>`, on this page | body | the page itself |

What happens if we make them identical for a moment, then different
again? Which feels right for your site?

## What we have now

A page split into two parts, and a reason for it.

- The *head* holds information about the page. It is not shown directly
  to a visitor.
- The *body* holds everything a visitor sees.
- `<title>` is the head element whose text appears in the browser tab.
