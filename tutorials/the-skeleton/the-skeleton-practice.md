---
title: "The head and body of a page — Practice"
practice_for: the-skeleton
year: "2026-2027"
version: 2026.09.22.1
---

# The head and body of a page — Practice

On this page we practise the two parts of every HTML page: the head,
which holds information about the page, and the body, which holds
everything a visitor sees. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, and its
reason, than from reading the answer.

The previews on this page have no browser tab of their own. So the text
of a `<title>` never shows anywhere in a preview. In your own site, it
shows in the tab.

## Fix the broken page

**1.** The author wanted "Plushie Shop" as a big heading at the top of
the page. It is not there.

```html site
id: skeleton-practice-heading-html
site: skeleton-practice-heading
<title>Plushie Shop</title>
<p>Every plushie is made by hand.</p>
```

Why does "Plushie Shop" not show on the page? Fix it, and keep the
`<title>` as well.

<details class="dl-answer"><summary>answer</summary>

```html
<title>Plushie Shop</title>
<h1>Plushie Shop</h1>
<p>Every plushie is made by hand.</p>
```

`<title>` belongs in the head. Its text goes to the browser tab, and
never onto the page. A heading on the page is an `<h1>`, which belongs
in the body. Most pages have both, and they often say something
similar.

</details>

**2.** This page has a heading and a paragraph in its HTML. The preview
is empty.

```html site
id: skeleton-practice-empty-html
site: skeleton-practice-empty
<title>Plushie Shop
<h1>Plushie Shop</h1>
<p>Every plushie is made by hand.</p>
```

Where did the heading and the paragraph go? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at each opening tag. Does each one have a closing tag?
2. The text of a `<title>` never shows on the page. Where does the
   browser think this title ends?

**Think about:** the browser reads everything up to `</title>` as the
text of the title, tags and all. What if there is no `</title>`?

**Try this next:** in your own site, what would the browser tab show if
the title had no closing tag?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<title>Plushie Shop</title>
<h1>Plushie Shop</h1>
<p>Every plushie is made by hand.</p>
```

The `</title>` closing tag was missing. The browser reads everything
after `<title>` as the title's text, up to `</title>`. There was no
`</title>`, so the heading and the paragraph, tags and all, became part
of the title. The text of a title never shows on the page, so the
preview was empty. On a real page, the browser tab would show all of
that text, angle brackets included.

</details>

## Make this

**3.** Write out a whole HTML page in the cell below, with every part of
the skeleton:

- the line that says this is a modern HTML page
- the element that wraps everything else
- a head, with the title "Home | Plushie Shop"
- a body, with a main heading "Plushie Shop" and one paragraph of your
  own

```html site
id: skeleton-practice-build-html
site: skeleton-practice-build
<!-- your HTML here -->
```

Which parts of your page show in the preview? Which parts do not?

<details class="dl-answer"><summary>answer</summary>

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Home | Plushie Shop</title>
  </head>
  <body>
    <h1>Plushie Shop</h1>
    <p>Every plushie is made by hand.</p>
  </body>
</html>
```

Only the heading and the paragraph show in the preview, because only
they are in the body. The title is in the head. The indents are there
to help us read the file: each element inside another one moves two
spaces to the right. The browser ignores them.

`Home | Plushie Shop` is a common pattern for titles: the name of this
page, then the name of the site. Your own `about.html` uses it, as we
see in the next problem.

</details>

## In your own site

**4.** Your two pages each have their own `<title>`. In `index.html` you
changed it to your name. What does `about.html` say?

1. In your fork, open `about.html`. Find the `<title>` in the head. It
   says `About Me | My Portfolio`.
2. The part after the `|` is the name of the site. Change it to match
   the title you gave `index.html`. For example:
   `About Me | Aoife Byrne`.
3. Save, and open both pages in your browser, each in its own tab.
4. Commit the change, with a message such as "Match the About page
   title".

Can you tell the two tabs apart? What would they look like if both
pages had the same title?

<details class="dl-answer"><summary>answer</summary>

The About page's tab now starts with "About Me", and then shows your
site's name. If both pages had the same title, the two tabs would look
the same, and a visitor could not tell which one was which. Each page
has its own head, so each page can have its own title.

</details>

**5.** Your header shows the words "My Portfolio" at the top left of
every page. Is that text in the head, or in the body?

1. In `index.html`, find `<a href="index.html" class="logo">My
   Portfolio</a>`. Which part of the page is it in: inside `<head>`, or
   inside `<body>`?
2. Change "My Portfolio" to your own name, or your site's name.
3. `about.html` has the same line in its header. Make the same change
   there.
4. Save both files, and refresh both pages.
5. Commit the change, with a message such as "Put my name in the
   header".

On your home page, your name may now be in three places: the title,
the logo, and perhaps the `<h1>`. Which of those are in the head, and
which are in the body?

<details class="dl-answer"><summary>answer</summary>

The logo link is inside `<header>`, which is inside `<body>`. So it is
in the body, and it shows on the page.

On `index.html`, the three places are:

| Where | Part of the page | Where it shows |
|---|---|---|
| `<title>` | head | the browser tab |
| the logo link in `<header>` | body | the top of the page |
| `<h1>`, on `index.html` | body | the hero section |

On `about.html`, the `<h1>` says "About Me", so there your name is in
the title and the logo only. Each page has its own copy of the header,
so a change to the header has to be made in both files.

</details>
