---
title: "A page is files"
slug: a-page-is-files
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# A page is files

Where does a web page actually live? It lives in a plain text file,
sitting in your fork, that you can open and read like any other document.
Let's try changing the text below and see what the browser builds from it.

```html site=first-page
<h1>A heading</h1>
<p>A paragraph with some <strong>strong</strong> and <em>emphasised</em>
text in it.</p>
```

Try adding a second paragraph, or changing a word inside the `<strong>`
tags. Nothing you do here can break anything; this is a small copy of the
same idea your fork uses.

## Why this happens

Every piece in angle brackets, like `<h1>` or `</p>`, is a **tag**. An
opening tag, the content after it, and a matching closing tag together
make one **element**. `<p>Hello</p>` is one paragraph element: an opening
tag, the word "Hello", and a closing tag.

Your browser reads a file like this from top to bottom. It does not show
you the tags. It uses them to work out what each piece of text is, then
builds the page you see from that.

Some tags carry extra information inside them, called an **attribute**,
written as `name="value"`. You will meet these often; for now it is enough
to recognise the shape.

## Your turn

Let's open your fork of the starter and find `index.html`. Near the top,
inside the `<head>` section, is a `<title>` element. It currently says "My
Portfolio". Try changing it to your name, or to anything else, then save.

If you are working on your own computer, refresh the browser to see the
change. If you are using GitHub's web editor, commit the change first, then
wait a minute for the page to rebuild. Look at your browser tab: the text
there should match what you typed.

## What you have now

A page you can trace back to plain text, and the words for the pieces that
text is made of.

- **Tag** — a marker in angle brackets, like `<p>` or `</p>`.
- **Element** — an opening tag, its content, and a matching closing tag.
- **Attribute** — extra information inside a tag, written `name="value"`.
