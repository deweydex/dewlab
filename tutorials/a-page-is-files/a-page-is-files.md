---
title: "A page is files"
year: "2026-2027"
version: 2026.09.11.1
covers:
  how-it-works:
    covers: [WA-LO2]
  in-your-own-site:
    covers: [WA-LO8]
---

# A page is files

A web page starts as a plain text file. The browser reads the text and
builds the page you see. On this page you:

- change some HTML and watch the page change with it
- learn three words for the parts of HTML: *tag*, *element* and
  *attribute*
- make your first change to your own site

## Try it

The box below is HTML, the language web pages are written in. The
preview under it shows the page the browser builds from that text.

```html site
id: first-page-html
site: first-page
<h1>A heading</h1>
<p>A paragraph with some <strong>strong</strong> and <em>emphasised</em>
text in it.</p>
```

1. Change the words between `<h1>` and `</h1>`. The heading in the
   preview changes as you type.
2. Change the word between `<strong>` and `</strong>`. It stays bold.
3. Add a second paragraph on a new line: `<p>Another paragraph.</p>`.

You cannot break anything here. If the preview looks wrong, undo your
change.

## How it works

The text inside angle brackets, like `<h1>` or `</p>`, is a *tag*. Most
tags come in pairs:

- an opening tag, like `<p>`
- a closing tag, with a slash, like `</p>`

An opening tag, the content after it and the matching closing tag make
one *element*. So `<p>Hello</p>` is one paragraph element.

The browser reads the file from top to bottom. It does not show the
tags. It uses them to decide what each piece of text is: a heading, a
paragraph, bold text. Then it draws the page.

Some tags also hold extra information, called an *attribute*. An
attribute is written as `name="value"` inside the opening tag:

```html
<a href="about.html">About me</a>
```

Here `href="about.html"` is an attribute. It tells the link where to go.
You will use attributes on later pages. For now, it is enough to
recognise the shape.

## In your own site

Your site's home page is a file called `index.html` in your fork of the
starter. Near the top of the file, inside the `<head>` section, there is
a `<title>` element. It says "My Portfolio".

1. Open `index.html`.
2. Change the text between `<title>` and `</title>` to your name.
3. Save the file.
4. See the change:
   - **On your own computer:** refresh the page in your browser.
   - **In GitHub's web editor:** commit the change, then wait about a
     minute for your site to rebuild.

**Check:** look at the tab at the top of your browser. It should show
the text you typed.

## Summary

| Word | Meaning | Example |
|---|---|---|
| *tag* | A marker in angle brackets | `<p>` or `</p>` |
| *element* | An opening tag, its content and its closing tag | `<p>Hello</p>` |
| *attribute* | Extra information inside an opening tag | `href="about.html"` |
