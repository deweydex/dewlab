---
title: "Semantic HTML: tags that describe their content"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# Semantic HTML: tags that describe their content

Your fork's `index.html` is full of tags like `<nav>`, `<header>` and
`<section>`. A plain `<div>` could hold the same content. So why use
different tags? On this page we:

- swap one container tag for another, and see what changes
- find out what these tags tell the browser and other software
- add a new section to your own site

## Let's try it

The HTML below has two blocks of content. The first uses `<div>`, and
the second uses `<section>`. The code under it is CSS, the language for
how a page looks. It draws a border around each of the two blocks.

```html site
id: semantic-html
site: semantic
<div>
  <h2>A div</h2>
  <p>A div groups things but says nothing about what they are.</p>
</div>
<section>
  <h2>A section</h2>
  <p>A section says: this is one meaningful part of the page.</p>
</section>
```

```css site
id: semantic-css
site: semantic
div, section {
  border: 1px solid #ccc;
  padding: 12px;
  margin-bottom: 12px;
}
```

1. Look at the preview. Can you see any difference between the two
   blocks?
2. In the HTML, change the first `<div>` to `<section>`, and `</div>` to
   `</section>`. Does anything change on the page?
3. Now change them back to `<div>` and `</div>`. In the CSS box, what
   happens if we delete `, section` from the first line?

## Why does this happen?

Now we can explain what we saw. The two blocks look the same, and
swapping the tag changes nothing we can see. How a box looks comes from
the CSS, and the CSS gives `div` and `section` the same border. When we
deleted `, section`, only the `<div>` kept its border.

So what does the tag change? It changes what the content *means*.

- `<div>` makes a generic container. It groups content together, but it
  does not say what that content is.
- `<nav>`, `<header>`, `<main>` and `<section>` are containers too. Each
  one names the kind of content it holds.

A *semantic element* is a tag that names the kind of content it holds.
Here are four of them:

| Tag | What it says about its content |
|---|---|
| `<nav>` | This is navigation: links to other pages or parts of the page. |
| `<header>` | This is introductory content, such as a title or a logo. |
| `<main>` | This is the main content of the page. |
| `<section>` | This is one meaningful part of the page. |

Who reads this meaning? Software that reads the code does. A *screen
reader* is software that reads a page aloud for someone who cannot see
it. It can say "navigation" when it reaches a `<nav>`. Search engines
use these tags too, and so do other developers who read your code.

So choosing a semantic tag in place of a `<div>` changes what a page
means. It does not change how the page looks. Even with no CSS at all, a
browser shows a `<div>` and a `<section>` the same way. `<div>` is still
useful. It is the right choice when a group of content has no special
meaning, and we only need a box to style.

## Now in your own site

Here is a new section for your fork's `index.html`:

```html
<section id="skills" class="section skills-section">
    <div class="container">
        <h2>What I'm Learning</h2>
        <p>Write something here about skills you're developing.</p>
        <div class="card">
            <h3>Technical Skills</h3>
            <p>List some things you're learning or want to learn.</p>
        </div>
    </div>
</section>
```

1. In your fork, open `index.html`.
2. Find the closing `</section>` tag of the about-preview section.
3. Straight after it, paste the new section above.
4. Change the text inside `<h2>`, `<h3>` and the two `<p>` tags to your
   own words.
5. Save, and refresh.

Does the new section appear with a style of its own? You did not write
any new CSS. The section is styled because `class="section"` and
`class="card"` reuse rules that are already in `styles.css`. A `class`
attribute can hold more than one name, with a space between each one,
as in `class="section skills-section"`. We meet classes properly in
[Choosing what to style: selectors and classes](tutorial:selectors-and-classes). The
`id="skills"` gives this section a name of its own, and we come back to
`id` in [Links to pages, other sites and email](tutorial:three-kinds-of-link).

## What we have now

We can now group content in containers that say what the content is, as
well as how it looks.

| Word | Meaning | Example |
|---|---|---|
| *semantic element* | A tag that names the kind of content it holds | `<nav>`, `<section>` |
| `<section>` | One meaningful part of a page | `<section id="skills">` |
| `<div>` | A generic container with no meaning of its own | `<div class="container">` |
| *screen reader* | Software that reads a page aloud for someone who cannot see it | it says "navigation" at a `<nav>` |
