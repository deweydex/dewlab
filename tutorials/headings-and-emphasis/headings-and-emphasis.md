---
title: "Headings, paragraphs and emphasis"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# Headings, paragraphs and emphasis

A page has one main heading, and smaller headings over each part of it.
How does the browser know which heading is which? On this page we:

- change the level of a heading, and watch what shifts
- mark words as important or emphasised
- rewrite the opening paragraph of your own site

## Let's try it

The box below is a short page. It has two headings, two paragraphs, and
two marked words.

```html site
id: headings-html
site: headings
<h1>My Portfolio</h1>
<p>Welcome. I am a <strong>developer</strong> and I love
<em>learning</em> new things.</p>
<h2>What I'm Learning</h2>
<p>A smaller heading for a smaller section.</p>
```

1. What happens if we change the `<h2>` to an `<h1>`? Change both the
   opening tag and the closing tag.
2. What about `<h3>`, or `<h6>`?
3. Look at "developer" and "learning" in the preview. How does each one
   look?
4. What happens if we swap the two tags, so that "developer" is inside
   `<em>` and "learning" is inside `<strong>`?

## Why does this happen?

Now we can explain what we saw. The tags `<h1>` to `<h6>` are six
heading levels. A *heading level* tells the browser how important a
heading is in the page's structure:

- `<h1>` marks the page's one main heading.
- `<h2>` marks a heading for a section under it.
- `<h3>` marks a heading for a smaller part inside that section, and so
  on down to `<h6>`.

When we changed `<h2>` to `<h1>`, the heading grew to the size of the
main heading. Browsers make each level smaller than the one before it.
We can change how headings look later with CSS, the language for how a
page looks. We start on CSS in [CSS rules and
stylesheets](tutorial:a-rule-and-where-it-lives).

So we choose a level for its place in the page's structure, and not for
its size. A good check is to read only the headings of a page, from top
to bottom. Do they look like a list of contents? Here is a slightly
longer page, with its headings read out on their own:

![On the left, a short shop page as a browser draws it: a large heading "Plushie Shop", a smaller heading "New this week", two smaller headings again, "Squishy Squid" and "Cuddly Cuttlefish", each with a line of text under it, and then another heading the size of "New this week", "Visit us". On the right, the same headings as a list of contents: "Plushie Shop" at the top, marked h1; under it, indented once, "New this week" and "Visit us", marked h2; and under "New this week", indented twice, "Squishy Squid" and "Cuddly Cuttlefish", marked h3.](heading-outline.svg)

`<p>` marks a paragraph of ordinary text.

Inside a paragraph, two tags mark words that matter more than the rest:

| Tag | What it means | How browsers show it |
|---|---|---|
| `<strong>` | This text is important. | In bold |
| `<em>` | This text is emphasised: we would stress it if we said it aloud. | In italics |

When we swapped the two tags, the bold and the italics swapped too. The
bold and the italics are only how a browser shows these two meanings.
The meaning itself stays in the code, where other software can read it.

## Now in your own site

In your fork, open `index.html`. Below your `<h1>` there is a paragraph
with `class="hero-text"` in its opening tag. `class` is an attribute.
It gives an element a name that CSS can use to style it. We meet
classes properly in [Choosing what to style: selectors and classes](tutorial:selectors-and-classes).

1. Find the paragraph with `class="hero-text"`.
2. Rewrite it in your own words: who you are, what you are working on,
   and what interests you. A few sentences is enough.
3. Wrap one important word or phrase in `<strong>` tags.
4. Wrap something you want to emphasise in `<em>` tags.
5. Save, and refresh.

Can you see the bold and the italic text on your page?

## What we have now

We can now break text into headings at the right level and into
paragraphs, and we can mark words as important or emphasised.

| Word | Meaning | Example |
|---|---|---|
| *heading level* | One of `<h1>` to `<h6>`. It shows how important a heading is in the page's structure. | `<h2>What I'm Learning</h2>` |
| `<p>` | A paragraph of ordinary text | `<p>Welcome.</p>` |
| `<strong>` | Marks text as important. Browsers show it in bold. | `<strong>developer</strong>` |
| `<em>` | Marks text as emphasised. Browsers show it in italics. | `<em>learning</em>` |
