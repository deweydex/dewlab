---
title: "The skeleton: head and body"
slug: the-skeleton
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# The skeleton: head and body

You already changed the `<title>` element in your fork. Try the same page
below, but look closely this time. The title and the heading say the same
words. Only one of them shows up.

```html site=skeleton
<title>My page</title>
<h1>My page</h1>
<p>Both lines above say "My page". Only one of them renders below.</p>
```

The `<h1>` text appears. The `<title>` text does not; on a real page it
would show up in the browser tab instead, not in the preview here.

## Why this happens

Every HTML page splits into two parts. Let's see why the title
disappeared from the preview. The **head** holds information about the
page: its `<title>`, and other details a visitor does not see directly.
The **body** holds everything a visitor actually sees: headings,
paragraphs, images, and the rest.

`<title>` lives in the head, which is why its text goes to the browser tab
rather than the page itself. `<h1>` lives in the body, alongside all your
other visible content.

## Your turn

Let's open `index.html` in your fork again. Inside the hero section
there is an `<h1>` element — it currently says "Welcome to My
Portfolio". Try changing it to something that represents you, then save
and refresh.

Now compare the two changes we have made. The title, in the head, changed
your browser tab. The heading, in the body, changed the page itself. Try
making them identical for a moment, then different again, and notice
which feels right for your site.

## What you have now

A page split into two parts, and a reason for it.

- **Head** — the part of the page holding information about it, not shown
  directly to a visitor.
- **Body** — the part holding everything a visitor sees.
- **`<title>`** — the head element whose text appears in the browser tab.
