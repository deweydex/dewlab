---
title: "Semantic HTML: tags that describe their content — Practice"
practice_for: sections-that-mean-something
year: "2026-2027"
version: 2026.09.22.1
---

# Semantic HTML: tags that describe their content — Practice

On this page we practise choosing between a `<div>` and a tag that says
what its content is. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, and its
reason, than from reading the answer.

Two questions help with every problem here. What is this piece of
content: navigation, the main content, one meaningful part of the page?
And does it need a tag that says so, or only a box to style?

## Fix the broken page

**1.** Every part of this shop's page should have a grey border. The
second part has none.

```html site
id: sections-practice-border-html
site: sections-practice-border
<section>
  <h2>New this week</h2>
  <p>A squid, a cuttlefish and a very sleepy seal.</p>
</section>
<div>
  <h2>Opening hours</h2>
  <p>Monday to Saturday, from 10 to 6.</p>
</div>
```

```css site
id: sections-practice-border-css
site: sections-practice-border
section {
  border: 2px solid #ccc;
  padding: 12px;
  margin-bottom: 12px;
}
```

Why does "Opening hours" have no border? The opening hours are one
meaningful part of the page. Fix the HTML, and leave the CSS as it is.

<details class="dl-answer"><summary>answer</summary>

```html
<section>
  <h2>New this week</h2>
  <p>A squid, a cuttlefish and a very sleepy seal.</p>
</section>
<section>
  <h2>Opening hours</h2>
  <p>Monday to Saturday, from 10 to 6.</p>
</section>
```

The CSS draws a border around every `<section>`, and the opening hours
were in a `<div>`. The opening hours are one meaningful part of the
page, so `<section>` is the right tag for them anyway. Now the tag says
what the content is, and the CSS finds it too. Remember to change the
closing tag as well as the opening one.

</details>

**2.** The author changed two `<div>` tags into `<section>` tags. Now
the second section sits inside the first, with one border inside
another.

```html site
id: sections-practice-nested-html
site: sections-practice-nested
<section>
  <h2>New this week</h2>
  <p>A squid, a cuttlefish and a very sleepy seal.</p>
</div>
<section>
  <h2>Opening hours</h2>
  <p>Monday to Saturday, from 10 to 6.</p>
</section>
```

```css site
id: sections-practice-nested-css
site: sections-practice-nested
section {
  border: 2px solid #ccc;
  padding: 12px;
  margin-bottom: 12px;
}
```

Why is "Opening hours" inside "New this week"? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the opening tag of the first section. Now find its closing tag.
   Do they match?
2. There is no `<div>` open here. What can the browser do with a
   `</div>`?
3. If the first section never closes, where is the second section?

**Think about:** when we change a tag, how many places in the code do
we need to change?

**Try this next:** open the inspector on this page. In the Elements
tab, can you see the second `<section>` inside the first?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<section>
  <h2>New this week</h2>
  <p>A squid, a cuttlefish and a very sleepy seal.</p>
</section>
<section>
  <h2>Opening hours</h2>
  <p>Monday to Saturday, from 10 to 6.</p>
</section>
```

The author changed the first opening tag, and forgot its closing tag.
There was no `<div>` for `</div>` to close, so the browser ignored it.
The first section stayed open, and everything after it, the second
section included, went inside it. With `</section>`, the first section
ends where it should, and the two sections sit one after the other.

</details>

## Make this

**3.** Build this page in the cell below, from the outside in:

- a header, holding a main heading: "Plushie Shop"
- inside the header, navigation with two links: "New" to `#new`, and
  "Visit" to `#visit`
- after the header, the main content of the page, holding two
  sections
- the first section has the heading "New this week" and one paragraph
- the second section has the heading "Visit us" and one paragraph

The CSS is ready. It draws a labelled, dashed box around each semantic
element, so we can see how the parts sit inside each other.

```html site
id: sections-practice-build-html
site: sections-practice-build
<!-- your HTML here -->
```

```css site
id: sections-practice-build-css
site: sections-practice-build
header, nav, main, section {
  border: 2px dashed #999;
  padding: 8px;
  margin: 8px 0;
}
header::before, nav::before, main::before, section::before {
  font: 12px monospace;
  color: #666;
}
header::before { content: "header"; }
nav::before { content: "nav"; }
main::before { content: "main"; }
section::before { content: "section"; }
```

Is every box labelled? Is the `nav` box inside the `header` box, and are
both `section` boxes inside the `main` box?

<details class="dl-answer"><summary>answer</summary>

Your paragraphs will say something different:

```html
<header>
  <h1>Plushie Shop</h1>
  <nav>
    <a href="#new">New</a>
    <a href="#visit">Visit</a>
  </nav>
</header>
<main>
  <section>
    <h2>New this week</h2>
    <p>A squid, a cuttlefish and a very sleepy seal.</p>
  </section>
  <section>
    <h2>Visit us</h2>
    <p>Monday to Saturday, from 10 to 6.</p>
  </section>
</main>
```

Every part of the page is in a tag that says what it is, so every part
has a labelled box. Nothing here needs a `<div>`. If a part has no box
around it, look for a `<div>` or a missing tag. If a box sits in the wrong place, look
for a missing or misplaced closing tag. [A menu that jumps to each
section](tutorial:navigation) shows how links like `#new` work, and
how most menus put their links in a list.

</details>

## In your own site

**4.** On [Semantic HTML: tags that describe their
content](tutorial:sections-that-mean-something) you added a skills
section, with one card inside it. Let's add a second card.

1. In your fork, open `index.html`, and find your skills section.
2. Find the card: the `<div class="card">` that holds "Technical
   Skills".
3. Straight after that card's closing `</div>`, add a second card:

```html
<div class="card">
    <h3>Tools I Use</h3>
    <p>A text editor, a browser, and GitHub.</p>
</div>
```

4. Change the words to your own.
5. Save, and refresh.
6. Commit the change, with a message such as "Add a second skills
   card".

Each card is a `<div>`, and the skills section around the two cards is
a `<section>`. Why do you think the cards are not sections too?

<details class="dl-answer"><summary>answer</summary>

The section is one meaningful part of the page, "What I'm Learning",
with its own `<h2>` heading, so it gets a tag that says so. Each card is
a box that the CSS styles. The class `card` gives it its background,
padding and shadow. The card does not add a new meaning of its own, so
a `<div>` is the right choice.

The two cards sit right against each other, with no space between them.
[The box model: padding, border and margin](tutorial:the-box) shows how
to add space around a box.

Does your second card stretch wider than the first, or sit below the
section? Then it went after the wrong `</div>`, or after `</section>`.
Move it up, so it sits straight after the first card's `</div>`, inside
`<div class="container">`.

</details>

**5.** A tag says what a part of the page is. A class names it, so the
CSS can style it. Your skills section has both. Let's use the class.

1. In your fork, open `styles.css`, and find the comment that starts
   `→ Exercise 18: Uncomment to style the skills section differently`.
2. The two rules under it, `.skills-section` and
   `.skills-section .card`, are inside that comment, so the browser
   ignores them. The comment starts with `/*` at the beginning of that
   line, and ends with `*/` on its own line after the second rule.
3. Delete the whole line that starts `/* → Exercise 18`, and delete the
   `*/` line. The two rules stay.
4. Save, and refresh `index.html`.
5. Commit the change, with a message such as "Style the skills
   section".

What changed on your page? Which part of your HTML told the CSS where
to make that change?

<details class="dl-answer"><summary>answer</summary>

The skills section now has a light grey background, and each card in it
has a blue line down its left side. The rest of the page did not
change.

The class did it. Your section has `class="section skills-section"`,
and the two rules look for the class name `skills-section`. The
`<section>` tag tells a screen reader or a search engine what the
content is. The class tells the CSS which part to style. We meet
classes properly in [Choosing what to style: selectors and
classes](tutorial:selectors-and-classes).

</details>
