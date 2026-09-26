---
title: "Headings, paragraphs and emphasis — Practice"
practice_for: headings-and-emphasis
year: "2026-2027"
version: 2026.09.22.1
---

# Headings, paragraphs and emphasis — Practice

On this page we practise choosing heading levels, and marking words as
important or emphasised. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, once you
see why it happened, than from reading the answer.

One check helps with every problem here. Read only the headings of the
page, from top to bottom. Do they look like a list of contents?

## Fix the broken page

**1.** A plushie shop lists its new plushies. The author chose each
heading level by how big it looked.

```html site
id: headings-practice-levels-html
site: headings-practice-levels
<h1>Plushie Shop</h1>
<h4>New this week</h4>
<h2>Squishy Squid</h2>
<p>Soft, purple, and very good at hugs.</p>
<h2>Cuddly Cuttlefish</h2>
<p>Changes colour when nobody is looking.</p>
```

The two plushies belong under "New this week". Why do their names look
bigger than the heading they sit under? Fix the levels.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read only the headings, from top to bottom, and say each one's
   level out loud.
2. Which heading is the main heading of the page? Which heading is a
   section under it? Which headings are parts inside that section?
3. Give each heading the level that matches its place in that list.

**Think about:** does a heading's level say how big it looks, or where
it sits in the page's structure?

**Try this next:** add a section called "Visit us" after the plushies,
with one paragraph. Which level does its heading need?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<h1>Plushie Shop</h1>
<h2>New this week</h2>
<h3>Squishy Squid</h3>
<p>Soft, purple, and very good at hugs.</p>
<h3>Cuddly Cuttlefish</h3>
<p>Changes colour when nobody is looking.</p>
```

"New this week" is a section under the main heading, so it is an
`<h2>`. The two plushies are parts inside that section, so each one is
an `<h3>`. Now the sizes follow the structure too: each level is smaller
than the one above it. If we want a different size later, we change it
with CSS, and keep the levels as they are.

</details>

**2.** In this page, the paragraph under the second heading is as big
and as bold as a heading.

```html site
id: headings-practice-close-html
site: headings-practice-close
<h1>My Portfolio</h1>
<p>Welcome to my site.</p>
<h2>What I'm Learning<h2>
<p>HTML first, and then CSS.</p>
```

Why does the last paragraph look like a heading? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the tags around "What I'm Learning". Which one is the
   opening tag, and which is the closing tag?
2. How is a closing tag different from an opening tag?

**Think about:** if the second tag is another opening tag, what is the
last paragraph inside?

**Try this next:** open the inspector on this page, and look at the
Elements tab. Can you see the paragraph inside a second `<h2>`?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<h1>My Portfolio</h1>
<p>Welcome to my site.</p>
<h2>What I'm Learning</h2>
<p>HTML first, and then CSS.</p>
```

The closing tag was missing its slash, so it was a second opening
`<h2>`. The browser ended the first heading there and started a new
one. The last paragraph landed inside that second heading, so it took
on the heading's size and weight. With `</h2>`, the heading ends after
"What I'm Learning", and the paragraph is an ordinary paragraph again.

</details>

## Make this

**3.** Build this page in the cell below. Here is its list of contents:

- "Greyhound Rescue", the main heading
  - "Our dogs", a section
    - "Bella", a part of that section
    - "Max", a part of that section
  - "Adopt a dog", a section

Under each heading except the main one, add a short paragraph. In the
paragraph about Bella, mark one word as important. In the paragraph
under "Adopt a dog", mark one word as emphasised.

```html site
id: headings-practice-build-html
site: headings-practice-build
<!-- your HTML here -->
```

Read your headings from top to bottom. Do they match the list of
contents above?

<details class="dl-answer"><summary>answer</summary>

Your paragraphs will say something different. The levels matter most:

```html
<h1>Greyhound Rescue</h1>
<h2>Our dogs</h2>
<p>Every dog here is looking for a home.</p>
<h3>Bella</h3>
<p>Bella is <strong>very</strong> gentle with children.</p>
<h3>Max</h3>
<p>Max likes long walks and short naps.</p>
<h2>Adopt a dog</h2>
<p>Come and <em>meet</em> them first.</p>
```

"Our dogs" and "Adopt a dog" are two sections under the main heading,
so both are `<h2>`. Bella and Max are parts inside "Our dogs", so both
are `<h3>`. "Adopt a dog" goes back up to `<h2>`, because it is a new
section, not a part of "Our dogs".

</details>

## In your own site

**4.** Your About page has five headings. Let's read them as a list of
contents, and then make the first section your own.

1. In your fork, open `about.html`. Find every heading, from `<h1>` down
   to `<h3>`, and write down its level and its words.
2. Which heading is an `<h3>`? Which section is it a part of?
3. Under `<h2>My Background</h2>` there are two paragraphs. Rewrite them
   in your own words.
4. Wrap one important word or phrase in `<strong>` tags, and something
   you want to stress in `<em>` tags.
5. If you like, change the words of the "My Background" heading too.
   Keep it an `<h2>`.
6. Save, refresh, and commit the change, with a message such as "Write
   my background".

Do your headings still look like a list of contents?

<details class="dl-answer"><summary>answer</summary>

In the starter, the About page's headings are:

- `<h1>` About Me
  - `<h2>` My Background
  - `<h2>` Why Web Development?
    - `<h3>` What I'm Currently Learning
  - `<h2>` My Goals

"What I'm Currently Learning" is an `<h3>`, inside a card under "Why
Web Development?". It is a part of that section, so it is one level
below it. Changing the words of a heading does not change its place in
the list. Changing its level does, so we keep "My Background" an
`<h2>`.

</details>
