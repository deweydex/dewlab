---
title: "How a browser reads an HTML file"
year: "2026-2027"
version: 2026.09.22.1
context_for: [a-page-is-files, the-skeleton]
---

# How a browser reads an HTML file

What happens between the text in your file and the page on the screen?
Two pages each show a piece of the answer: [HTML: tags, elements and
attributes](tutorial:a-page-is-files) and [The head and body of a
page](tutorial:the-skeleton). This page follows the browser as it reads
a file. It is background reading. You do not need it to finish those
pages, but it can help you see why they work.

On this page we:

- see how a browser turns a file into a tree of elements
- see what it does with spaces, new lines and missing tags
- meet a few kinds of tag that we have not written yet
- read the head of your own `index.html`, line by line

## From text to a tree

A browser reads an HTML file from top to bottom, one tag at a time. As
it reads, it builds a model of the page. Every element goes into the
model, in the place where it sits in the file: inside the element
around it, and after the element before it.

Here is the page from [The head and body of a page](tutorial:the-skeleton),
with the model the browser builds from it:

![On the left, the HTML of a whole page: DOCTYPE, then html, head, title, body, h1 and p, each one indented inside the one around it. On the right, the same page drawn as a tree. At the top is html. Two lines lead down from it, to head and to body. One line leads down from head, to title. Two lines lead down from body, to h1 and to p. Under title, h1 and p, the words each one holds are shown in a lighter colour.](page-tree.svg)

The *document tree* is the browser's model of a page: every element,
arranged by which one sits inside which. Developers often call it the
DOM, short for Document Object Model. An element inside another is its
*child*, and the element around it is its *parent*. So `<head>` and
`<body>` are the two children of `<html>`, and `<h1>` and `<p>` are
children of `<body>`.

Because the tree is built from elements inside elements, an element
that opens inside another must also close inside it:

```html
<p>A <strong>good</strong> example.</p>   <!-- strong closes inside p -->
<p>A <strong>bad example.</p></strong>    <!-- strong closes after p -->
```

The inspector's **Elements** tab shows this tree, and not the file. We
can open and close each element in it, the way we open and close a
folder. To see the file itself, right-click a page and choose **View
page source**. The two can differ, as the next two sections show.

## Spaces and new lines

What does a browser do with the spaces and new lines in a file? Here
are three paragraphs to try:

```html site
id: reads-space-html
site: reads-space
<p>One    space,    or    many?</p>
<p>A new line
in the file.</p>
<p>A line<br>break.</p>
```

1. How many spaces does the first paragraph show between its words?
2. Where does the new line in the second paragraph go?
3. What does `<br>` do in the third?

Spaces, tabs and new lines are called *whitespace*. In ordinary text,
a browser turns every run of whitespace into one space. So many spaces
show as one, and a new line in the file shows as a space too. That is
why we can indent our HTML and break long lines wherever we like: the
page does not change. When we want a new line inside a paragraph, we
ask for one with `<br>`, a line break.

## When a tag is missing

A browser never stops with an error when an HTML file has a mistake in
it. It makes a guess, and carries on. Here is a list and three
paragraphs, all with closing tags missing:

```html site
id: reads-missing-html
site: reads-missing
<ul>
  <li>Squishy Squid
  <li>Cuddly Cuttlefish
</ul>
<p>A paragraph with no closing tag.
<p>Another one.
<p>Some <strong>strong text, never closed.
<p>Is this paragraph strong too?
```

1. Does the list look right? Do the first two paragraphs?
2. Where does the strong text stop?
3. Open the inspector and look at the **Elements** tab. Can you find
   closing tags there that are not in the file?

Some guesses are easy. A paragraph cannot hold another paragraph, so a
new `<p>` ends the one before it. The same goes for a new `<li>` in a
list. Here the browser's guess is always right, and the list and the
first two paragraphs look fine.

Other guesses are harder. A `<strong>` could end anywhere, so the
browser carries it on, even into the next paragraph. That is the kind
of mistake the practice pages ask you to fix. The inspector shows the
tree with the browser's guesses filled in, which is often the quickest
way to see where a missing tag went.

These guesses are the same in every modern browser. The rules for HTML
spell out what to do with each kind of mistake, so browsers do not
have to make up their own. The same rules add a missing `<html>`,
`<head>` or `<body>`, which is why the example on [The head and body
of a page](tutorial:the-skeleton) worked without them. We still write
every closing tag. Then the browser has nothing to guess, and the next
person to read the file does not either.

## Tags with no closing tag

A few elements can never hold any content, so they have no closing tag
at all. They are called *void elements*. Here are four of them:

| Tag | What it does |
|---|---|
| `<img>` | Places an image |
| `<br>` | Starts a new line |
| `<meta>` | Gives information about the page, in the head |
| `<link>` | Connects the page to another file, such as a stylesheet |

Sometimes we see these written with a slash at the end, as `<br />` or
`<img ... />`. In HTML, that slash is allowed, and the browser ignores
it. Both ways of writing them work.

## Writing the characters HTML uses

What if a paragraph needs a `<` sign, or the © sign? A browser reads
`<` as the start of a tag. So HTML has a way to write such characters
by name, starting with `&` and ending with `;`:

```html site
id: reads-entity-html
site: reads-entity
<p>&lt;p&gt; is the tag for a paragraph.</p>
<p>Fish &amp; chips, &copy; 2026.</p>
```

A *character reference* is a name for a character, written between `&`
and `;`, such as `&copy;` for ©. Your own footer uses `&copy;`. The
three that matter most are `&lt;` for `<`, `&gt;` for `>` and `&amp;`
for `&` itself.

## Comments

Your starter files are full of notes like this one:

```html
<!--
This connects your HTML to the CSS file.
-->
```

A *comment* is text between `<!--` and `-->`. The browser skips it, so
it never shows on the page. It stays in the file, so **View page
source** shows it to anyone who looks. Comments are for people reading
the code: notes, reminders, and exercises, as in your starter. Never
put anything private in one.

## The head of your own site

Now we can read the top of your own `index.html`, one line at a time.
In the starter, without its comments, it looks like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="A personal portfolio website">
    <title>My Portfolio</title>
    <link rel="stylesheet" href="styles.css">
</head>
```

| Line | What it tells the browser |
|---|---|
| `<!DOCTYPE html>` | Read this page with today's rules. Without it, browsers fall back to an old set of rules, called quirks mode, kept so that very old pages still work. |
| `<html lang="en">` | The page is written in English. [Who else reads a page](tutorial:who-reads-a-page) shows who uses that. |
| `<meta charset="UTF-8">` | How the text is stored in the file. UTF-8 can hold the letters of almost every language, and it comes first so that the browser knows it before it reads any words. |
| `<meta name="viewport" ...>` | How wide to draw the page on a phone. [Changing the layout for phones: media queries](tutorial:media-queries) comes back to it. |
| `<meta name="description" ...>` | A short description of the page, which search engines may show. |
| `<title>` | The text for the browser tab. |
| `<link rel="stylesheet" href="styles.css">` | Load the CSS in `styles.css`. [CSS rules and stylesheets](tutorial:a-rule-and-where-it-lives) starts there. |

You could compare the file with the tree on your own site:

1. Open your published site in the browser.
2. Right-click the page, and choose **View page source**. Can you find
   the lines in the table above, and the comments between them?
3. Now open the inspector. In the **Elements** tab, open the `<head>`
   line. Are the same elements there?
4. Look for `&copy;` in your footer. What does **View page source** show
   there? What does the Elements tab show?

## What we have now

We can now describe how a browser reads an HTML file, and what it does
when the file is not quite right.

| Word | Meaning | Example |
|---|---|---|
| *document tree* | The browser's model of a page: every element, arranged by which one sits inside which. Often called the DOM. | `<html>`, with `<head>` and `<body>` under it |
| *child* and *parent* | An element inside another is its child. The element around it is its parent. | `<title>` is a child of `<head>` |
| *whitespace* | Spaces, tabs and new lines. A browser shows each run of them as one space. | an indent in your HTML |
| `<br>` | A line break inside a paragraph | `A line<br>break.` |
| *void element* | An element that can never hold content, so it has no closing tag | `<img>`, `<br>`, `<meta>` |
| *character reference* | A name for a character, written between `&` and `;` | `&copy;` for © |
| *comment* | Text between `<!--` and `-->`, for people reading the code. The browser skips it. | `<!-- a note -->` |
