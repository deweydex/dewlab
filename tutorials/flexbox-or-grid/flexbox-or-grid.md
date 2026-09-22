---
title: "Flexbox or Grid?"
year: "2026-2027"
version: 2026.09.22.1
context_for: [flexbox-first-steps, named-grid-areas, order-on-screen]
---

# Flexbox or Grid?

CSS has two tools for laying boxes out side by side: flexbox and grid.
Three pages each use one of them: [Lining boxes up in a row with
Flexbox](tutorial:flexbox-first-steps), [Laying out a page with grid
areas](tutorial:named-grid-areas) and [Changing the order of boxes on
screen](tutorial:order-on-screen). This page compares the two tools. It
is background reading. You do not need it to finish those pages, but it
can help you choose between the tools in your own work.

On this page we:

- watch flexbox and grid lay out the same five boxes
- see which jobs suit each tool, and how they work together
- look back at how pages were laid out before these tools
- find flex and grid layouts in the inspector
- think again about moving boxes away from the order of the HTML

## One direction, or two

Here are five boxes, twice. The first five sit in a flex container that
wraps, as on the flexbox page. The second five sit in a grid with three
equal columns. We meet grids properly on [Laying out a page with grid
areas](tutorial:named-grid-areas), where `1fr` means one share of the
space.

```html site
id: flex-or-grid-html
site: flex-or-grid
<div class="flex">
  <div>1</div>
  <div>2</div>
  <div>3</div>
  <div>4</div>
  <div>5</div>
</div>
<div class="grid">
  <div>1</div>
  <div>2</div>
  <div>3</div>
  <div>4</div>
  <div>5</div>
</div>
```

```css site
id: flex-or-grid-css
site: flex-or-grid
.flex {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}
.flex div {
  flex: 1 1 100px;
}
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
}
.flex div, .grid div {
  padding: 12px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  text-align: center;
  font-family: sans-serif;
}
```

1. Set the **Preview width** slider to about 420 pixels. Compare boxes
   4 and 5 in the two layouts. Which ones are wider?
2. Drag the slider slowly toward the narrow end. What does each layout
   do?

Now we can explain what we saw. Flexbox works in one direction at a
time. It fills one line, then wraps and starts the next, and each line
shares out its own space. So at 420 pixels, boxes 4 and 5 had a line
of their own, and they grew to fill it. They no longer lined up with
the boxes above them. As the preview narrowed, the flex row wrapped
again, to two boxes on a line, then one.

Grid works in two directions at once. It sets up rows and columns, and
every box goes into a cell. Boxes 4 and 5 sat in the first two
columns, under boxes 1 and 2, and the third cell stayed empty. The grid
kept three columns at every width, and the columns got narrower,
because our grid asks for three columns and nothing else.

![Five numbered boxes laid out two ways, side by side. On the left, flexbox with wrapping: boxes 1, 2 and 3 share the first row, and boxes 4 and 5 share the second row, each half its width. On the right, a grid with three columns: boxes 1, 2 and 3 fill the first row, and boxes 4 and 5 sit under boxes 1 and 2, with an empty dashed cell after them. The caption under flexbox says each row shares out its own space. The caption under grid says the columns line up in every row.](flex-or-grid.svg)

A short way to say it: with flexbox, the content decides how much room
each box gets. With grid, the grid decides, and the content fills it.

## Which one to reach for

Both tools can do many of the same jobs, so there is often no wrong
answer. Still, each is at its best in some places:

| Job | Often done with | Why |
|---|---|---|
| A row of buttons or links | flexbox | one line, and each item as wide as its text |
| A logo on one side and a menu on the other | flexbox | one line, with the space between them |
| A row of cards that wrap and fill each row | flexbox | each line shares out its own space |
| A whole page: header, menu, main, footer | grid | rows and columns together, with named areas |
| A gallery of equal tiles | grid | the tiles line up in columns |

The two work well together. A page might use grid for its main areas,
and then flexbox inside the header to line up the logo and the menu.

Your own site uses flexbox four times, and grid not at all. In
`styles.css`, `display: flex` appears on `body`, which keeps the footer
at the bottom; on `.header-content`, the logo and the menu; on
`.main-nav ul`, the links in the menu; and on `.cta-buttons`, the two
buttons near the bottom of `about.html`. The project starter, in the
series A site with several pages, uses grid for its gallery. [A grid
gallery](tutorial:a-grid-gallery) looks at it.

## Before flexbox and grid

Flexbox and grid are fairly new. Grid arrived in all the main browsers
in 2017, and flexbox a few years before that. Before them, there was no
tool made for page layout. Designers borrowed other tools for the job.
Many early websites were built inside large HTML tables, with one cell
for the menu and another for the content. Later, many used the `float`
property, which was made to let text flow around a picture. Both ways
worked, but they were fragile, and a small change could break the whole
layout. You may still meet them in older code.

## Seeing flex and grid in the inspector

The inspector we met on [Looking inside a page with the
inspector](tutorial:the-inspector) knows about both tools. In the
**Elements** tab, Chrome and Firefox show a small **flex** or **grid**
label beside an element that uses one of them. Select the element with
`display: grid`, and look for the grid options in the **Layout** panel.
They draw the grid lines over the page, and can show the area names
too. For a flex container, the same panel can outline each flex item.

You could try it on your own site:

1. Open your home page, and open the inspector.
2. In the **Elements** tab, find the line that says
   `<div class="container header-content">`. Is there a **flex** label
   beside it?
3. Click the label. What does the browser draw over your header?

## When the screen order and the HTML order differ

[Changing the order of boxes on screen](tutorial:order-on-screen)
showed that `order` moves a box on screen, while the Tab key and screen
readers keep to the order of the HTML. Grid can do the same, by placing
an area anywhere on the map. So both tools can make the screen order
and the HTML order disagree.

The rules for accessible websites, called WCAG, ask for two things
here. When the order of content matters to its meaning, a screen reader
must be able to read it in an order that makes sense. And the keyboard
focus must move through the page in an order that makes sense. The
flexbox rules themselves say the same thing: `order` is for how things
look, and it is no replacement for putting the HTML in the right order.

A simple test catches most problems. Load the page, put the mouse away,
and press Tab from the top to the bottom. Does the outline move in the
same order as your eyes would read the page?

## What we have now

We can now choose between flexbox and grid for a job, and we know that
many pages use both.

- Flexbox lays boxes out in one direction at a time. Each line shares
  out its own space, and the content decides how much room each box
  gets.
- Grid lays boxes out in rows and columns at once. The columns line
  up in every row, and the grid decides how much room each box gets.
- Both can move boxes away from the order of the HTML. The Tab key and
  screen readers still follow the HTML, so we check a page with Tab.
