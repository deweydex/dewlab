---
title: "HTML: tags, elements and attributes — Practice"
practice_for: a-page-is-files
year: "2026-2027"
version: 2026.09.22.1
---

# HTML: tags, elements and attributes — Practice

On this page we practise reading and writing tags, elements and
attributes. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

A browser does not stop when it meets a mistake in HTML. It guesses
what we meant, and carries on. So a small mistake in the text can make
a strange change on the page, some distance away from the mistake
itself.

## Fix the broken page

**1.** The author wanted only the words "made by hand" in bold. Look at
the preview.

```html site
id: files-practice-strong-html
site: files-practice-strong
<p>Our plushies are <strong>made by hand in Galway.</p>
<p>Delivery is free on every order.</p>
```

How much of the text is bold? Why does the bold go on so far? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the opening `<strong>` tag. Where is its closing tag?
2. Without a closing tag, where does the browser think the element
   ends?

**Think about:** an element is an opening tag, its content, and a
matching closing tag. Which of those three is missing?

**Try this next:** once it works, make "Delivery is free" bold as well,
and not the rest of that sentence.

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<p>Our plushies are <strong>made by hand</strong> in Galway.</p>
<p>Delivery is free on every order.</p>
```

The closing tag `</strong>` was missing. The browser had to guess where
the bold text should end, and it guessed wrong: the bold ran on to the
end of the first paragraph, and then into the second one too. With the
closing tag straight after "made by hand", the element ends where we
meant it to.

</details>

**2.** Half of this page has gone. The HTML has two paragraphs, but the
preview shows only two words.

```html site
id: files-practice-quote-html
site: files-practice-quote
<p>Read the <a href="about.html>About page</a> to find out more.</p>
<p>We are open from 10 to 6, Monday to Saturday.</p>
```

Where did the rest of the text go? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last words we can see are "Read the". What comes straight after
   them in the HTML?
2. Look at the attribute. An attribute is written `name="value"`. Count
   the quote marks.
3. Where does the browser think the value ends?

**Think about:** the browser reads a value until it finds the closing
quote mark. What if there is not one?

**Try this next:** what happens if we add a quote mark in the wrong
place, as `href="about".html"`?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<p>Read the <a href="about.html">About page</a> to find out more.</p>
<p>We are open from 10 to 6, Monday to Saturday.</p>
```

The value of `href` had an opening quote mark, and no closing one. So
the browser kept reading the value, looking for the closing quote, all
the way to the end of the file. Everything after `href="` became part
of one long, broken tag, and a tag is never shown on the page. With
the closing quote back, the value is `about.html` again, and the rest
of the page comes back.

</details>

**3.** This link should be blue, and we should be able to click it. It
looks like ordinary text.

```html site
id: files-practice-equals-html
site: files-practice-equals
<p>Our shop has an <a href"about.html">About page</a>.</p>
```

What is wrong with the attribute? Fix it.

<details class="dl-answer"><summary>answer</summary>

```html
<p>Our shop has an <a href="about.html">About page</a>.</p>
```

An attribute is written `name="value"`, and here the `=` was missing.
The browser could not tell the name from the value, so the link had no
`href` at all. An `<a>` element with no `href` is not a link: it shows
as plain text, and nothing happens when we click it. With `=` back, the
link is blue again. (Clicking it in the preview still goes nowhere,
because there is no `about.html` here. In your own site, there is.)

</details>

## Make this

**4.** Build this small page in the cell below:

- a main heading that says "Plushie Shop"
- a paragraph: "Every plushie is made by hand." The words "made by
  hand" are important, so they are bold.
- a second paragraph: "Read more on our About page." The words "About
  page" are a link to `about.html`.

```html site
id: files-practice-build-html
site: files-practice-build
<!-- your HTML here -->
```

How many elements did you write? How many attributes?

<details class="dl-answer"><summary>answer</summary>

```html
<h1>Plushie Shop</h1>
<p>Every plushie is <strong>made by hand</strong>.</p>
<p>Read more on our <a href="about.html">About page</a>.</p>
```

There are five elements: one `<h1>`, two `<p>`, one `<strong>` and one
`<a>`. There is one attribute, `href="about.html"`. The `<strong>` and
the `<a>` each sit inside a paragraph, so each one is an element inside
another element.

</details>

## In your own site

**5.** Near the top of `index.html`, inside the `<head>` section, there
is this line:

```html
<meta name="description" content="A personal portfolio website">
```

It has two attributes, `name` and `content`. The value of `content` is
a short description of your site. Search engines may show it under your
page's title in a list of search results. It never shows on the page
itself.

1. In your fork, open `index.html` and find that line.
2. Change the value of `content` to one sentence about your own site.
   Keep both quote marks.
3. `about.html` has its own `<meta name="description">` line. Change its
   `content` to one sentence about your About page.
4. Save both files.
5. Commit the change, with a message such as "Describe my pages".

How can you check the change, when the description never shows on the
page?

<details class="dl-answer"><summary>answer</summary>

Open the page in your browser, and open the inspector. In the
**Elements** tab, open the `<head>` line. The `<meta name="description">`
line is there, with your new sentence as the value of `content`.

Most browsers can also show the file itself: right-click the page, and
choose **View page source**. That shows your HTML exactly as you wrote
it, comments and all.

If a quote mark went missing, look at the page itself. Does part of it
look wrong? Problem 2 on this page showed what one missing quote mark
can do.

</details>
