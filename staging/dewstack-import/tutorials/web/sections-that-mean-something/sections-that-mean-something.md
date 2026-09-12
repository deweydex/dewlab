---
title: "Sections, and the tags that mean something"
slug: sections-that-mean-something
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Sections, and the tags that mean something

Your fork's `index.html` is full of tags like `<nav>`, `<header>` and
`<section>`, when a plain `<div>` could hold the same content. Try the box
below, then swap `<div>` for `<section>` in the first one and see whether
anything changes on the page.

```html site=semantic
<div>
  <h2>A div</h2>
  <p>A div groups things but says nothing about what they are.</p>
</div>
<section>
  <h2>A section</h2>
  <p>A section says: this is one meaningful part of the page.</p>
</section>
```

```css site=semantic
div, section {
  border: 1px solid #ccc;
  padding: 12px;
  margin-bottom: 12px;
}
```

Both boxes look identical. Swapping the tag changes nothing you can see.

## Why this happens

`<div>` creates a generic container. It groups content together without
saying what that content is. `<nav>`, `<header>`, `<main>` and `<section>`
are containers too, but each one names its content. A `<nav>` says this is
navigation. A `<main>` says this is the main content. A `<section>` says
this is one part of it.

A screen reader, software that reads a page aloud for someone who cannot
see it, can announce "navigation" on reaching a `<nav>`. Search engines and
other developers reading your code use these tags the same way. Choosing a
semantic tag over `<div>` changes what a page means. It usually does not
change how the page looks.

## Your turn

Let's open your fork and find the closing `</section>` tag of the
about-preview section. Try adding a new section straight after it:

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

Save and refresh. The new section appears already styled, without you
writing any new CSS, because `class="section"` and `class="card"` reuse
rules already in `styles.css`.

## What you have now

Content grouped in containers that say what they are, not only how they
look.

- **Semantic element** — a tag, such as `<nav>` or `<section>`, that names
  the kind of content it holds.
- **`<section>`** — marks one meaningful part of a page.
- **`<div>`** — a generic container with no meaning of its own.
