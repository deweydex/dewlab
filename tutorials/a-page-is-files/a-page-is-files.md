---
title: "HTML: tags, elements and attributes"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    covers: [WA-LO8]
---

# HTML: tags, elements and attributes

Where does a web page live? It lives in a plain text file, sitting in
your fork, that you can open and read like any other document. On this
page we:

- change some HTML and watch the page change with it
- find words for the parts of HTML: *tag*, *element* and *attribute*
- make a first change to your own site

## Let's try it

The box below is HTML, the language web pages are written in. The
preview under it is the page the browser builds from that text.

```html site
id: first-page-html
site: first-page
<h1>A heading</h1>
<p>A paragraph with some <strong>strong</strong> and <em>emphasised</em>
text in it.</p>
```

1. What happens to the preview if we change the words between `<h1>`
   and `</h1>`? Watch it as you type.
2. The word between `<strong>` and `</strong>` is bold. If we change
   it, does the new word stay bold?
3. What if we add a second paragraph on a new line, like
   `<p>Another paragraph.</p>`?

Nothing you do here can break anything. This is a small copy of the same
idea your fork uses.

## Why does this happen?

Every piece in angle brackets, like `<h1>` or `</p>`, is a *tag*. Most
tags come in pairs:

- an opening tag, like `<p>`
- a closing tag, with a slash, like `</p>`

An opening tag, the content after it, and a matching closing tag
together make one *element*. So `<p>Hello</p>` is one paragraph element:
an opening tag, the word "Hello", and a closing tag.

Did you notice that the preview never shows the tags? The browser reads
the file from top to bottom, and uses the tags to decide what each piece
of text is: a heading, a paragraph, some bold text. Then it builds
the page we see from that.

Some tags carry extra information inside them, called an *attribute*,
written as `name="value"`:

```html
<a href="about.html">About me</a>
```

Can you spot the attribute here? It is `href="about.html"`, and it tells
the link where to go. We will meet attributes often. For now, it is
enough to recognise the shape.

So a web page is a text file, and the tags in it tell the browser what
each part of the text is. Every website works this way, not only ours.

## Now in your own site

Let's open your fork of the starter and find `index.html`. Near the top,
inside the `<head>` section, there is a `<title>` element. It says "My
Portfolio".

1. Change the text between `<title>` and `</title>` to your name, or
   to anything else you like.
2. Save the file.
3. How we see the change depends on where you are working:
   - **On your own computer:** refresh the browser.
   - **In GitHub's web editor:** commit the change first, then wait a
     minute for the page to rebuild.

Now look at your browser tab. Does the text there match what you typed?

## What we have now

We can now trace a page back to plain text, and we have words for the
pieces that text is made of:

| Word | Meaning | Example |
|---|---|---|
| *tag* | A marker in angle brackets | `<p>` or `</p>` |
| *element* | An opening tag, its content and a matching closing tag | `<p>Hello</p>` |
| *attribute* | Extra information inside a tag, written `name="value"` | `href="about.html"` |
