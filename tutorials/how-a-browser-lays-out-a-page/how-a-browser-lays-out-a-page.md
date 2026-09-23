---
title: "How a browser lays out a page"
year: "2026-2027"
version: 2026.09.22.1
context_for: [the-box, the-container, position-and-the-sticky-header, footer-at-the-bottom]
---

# How a browser lays out a page

How does a browser decide where each box on a page goes? Four pages
each show one piece of the answer: [The box model: padding, border and
margin](tutorial:the-box), [A readable width, centred on the
page](tutorial:the-container), [A header that stays in view as you
scroll](tutorial:position-and-the-sticky-header) and [A footer that
sits at the bottom of a short page](tutorial:footer-at-the-bottom). This
page puts the pieces together. It is background reading. You do not
need it to finish those pages, but it can help you see why they work.

On this page we:

- see how boxes stack and wrap when no layout rule moves them
- see what `width` measures, and why your stylesheet changes that
- look more closely at margin collapse
- see how the values of `position` fit together
- find all of this in the browser inspector

## Boxes that stack, and boxes that wrap

Before we write any layout rules, the browser already puts every box
somewhere. Where? Here is a heading and two paragraphs. The CSS draws a
border around the heading and each paragraph, and shades two phrases
inside the first paragraph.

```html site
id: flow-html
site: flow
<h2>Our plushies</h2>
<p>Every plushie is <em>made by hand</em>, and you can read <a href="#">how we make them</a> on the next page.</p>
<p>A second paragraph.</p>
```

```css site
id: flow-css
site: flow
h2, p {
  border: 2px solid #2c3e50;
  padding: 8px;
}
em, a {
  background: #fbe8a6;
}
```

1. Drag the **Preview width** slider from wide to narrow. What do the
   boxes with a border do? What do the shaded phrases do?
2. Add `display: inline;` to the `h2, p` rule. What happens to the three
   boxes?
3. Take that line out again. Now add `display: block;` to the `em, a`
   rule. What happens to the shaded phrases?

Now we can explain what we saw. When no layout rule moves a box, the
browser places it by a set of default rules called *normal flow*. Normal
flow has two main kinds of box.

- A *block box* starts on a new line, and fills the whole width of the
  element it sits in. Headings, paragraphs, `<div>`, `<section>`,
  `<header>` and `<footer>` make block boxes. Block boxes stack from top
  to bottom, in the order they come in the HTML. In step 1, the bordered
  boxes stayed as wide as the preview, and grew taller as it narrowed.
- An *inline box* sits inside a line of text, and is only as wide as its
  content. `<em>`, `<strong>` and `<a>` make inline boxes. When a line
  is full, an inline box wraps onto the next line, the way a word does.
  In step 1, the shaded phrases moved along the lines of text, and at
  some widths one of them broke across two lines.

<div class="dl-drawn dl-flow" role="img" aria-label="Three block boxes stacked from top to bottom, each as wide as the space it sits in: a heading, a paragraph, and a second paragraph. Inside the first paragraph, two shaded inline boxes sit in the line of text. The second one is too long for the space left on its line, so it wraps: part of it ends one line, and the rest starts the next.">
<div class="dl-fl-block"><span class="dl-fl-tag">h2 · block</span>A heading</div>
<div class="dl-fl-block"><span class="dl-fl-tag">p · block</span>A paragraph with <span class="dl-fl-inline">a short phrase</span> in it, and then <span class="dl-fl-inline">a longer phrase that runs on past the end of the line</span> and wraps.</div>
<div class="dl-fl-block"><span class="dl-fl-tag">p · block</span>A second paragraph starts on a new line.</div>
</div>

Which kind of box an element makes is set by the `display` property.
Each element starts with a value of its own: `block` for a paragraph,
`inline` for a link. In step 2, `display: inline` turned the heading and
paragraphs into inline boxes, so they ran on in one line of text. In
step 3, `display: block` put each shaded phrase on a line of its own.
[Lining boxes up in a row with Flexbox](tutorial:flexbox-first-steps) uses a third value,
`flex`, which lays out the boxes inside an element in a row or a column.

One rule of normal flow explains a lot on the other pages: a block box
fills the width of its parent, unless something stops it. That is why a
container needs a `max-width` before `margin: 0 auto` can centre it.
Without one, the box already fills the width, and there is no space left
over for the auto margins to share. Many websites wrap their content in
a container like this, often with a class name such as `container` or
`wrapper`. Your site's `.container` is one.

Normal flow also explains the footer. In normal flow, a block box is
only as tall as its content, and each box comes straight after the one
above it. So on a short page, the footer sits right under the text.
`display: flex` on the body changes the rules for the body's children,
and that is what lets `margin-top: auto` push the footer down.

## What `width` measures

Sometimes we might set a box's `width` to `200px`, and then notice that
it takes up more room than that on the page. Why? By default, `width`
sets the width of the content only. The padding and the border are
added on outside it.

The property that decides this is `box-sizing`. *box-sizing* sets what
`width` and `height` measure. It has two values:

- `content-box` is the default. `width` measures the content alone, and
  the padding and border are added outside it.
- `border-box` makes `width` measure the whole box: content, padding and
  border together. The content shrinks to make room.

Here are two boxes with the same CSS, `width: 120px`, `16px` of padding
and a `4px` border. Only `box-sizing` is different:

<div class="dl-drawn dl-sizing" role="img" aria-label="Two boxes side by side, each with width 120px, 16 pixels of padding and a 4 pixel border. The left box uses content-box: a ruler marked width 120px spans only its content, and the whole box is 160 pixels across. The right box uses border-box: the same ruler spans the whole box, which is 120 pixels across, and its content has shrunk to 80 pixels.">
<div class="dl-bs-col">
<p class="dl-bs-name">content-box</p>
<div class="dl-bs-rule dl-bs-rule-inner"><span class="dl-bs-width">width: 120px</span></div>
<div class="dl-bs-box dl-bs-content-box"><div class="dl-bs-content">content</div></div>
<p class="dl-bs-sum">160px across<br><span class="dl-bs-said">4 + 16 + 120 + 16 + 4</span></p>
</div>
<div class="dl-bs-col">
<p class="dl-bs-name">border-box</p>
<div class="dl-bs-rule"><span class="dl-bs-width">width: 120px</span></div>
<div class="dl-bs-box dl-bs-border-box"><div class="dl-bs-content">content</div></div>
<p class="dl-bs-sum">120px across<br><span class="dl-bs-said">the content shrinks to 80px</span></p>
</div>
</div>

Many stylesheets set `border-box` on every element, because it makes
sizes easier to plan. A box set to `200px` wide is then `200px` wide on
the page, whatever its padding. Your site's stylesheet does this too.
Near the top of `styles.css`, in the section called Reset & Base
Styles, there is a rule that starts with `*`. The `*` selector matches
every element on the page, and that rule sets `box-sizing: border-box`.
The comment beside it gives the same kind of example: without it, a
`200px` box with `20px` of padding would be `240px` wide.

The live examples on this site's pages do not set it, so a box in a
preview uses `content-box`. We meet `box-sizing` again in [Cards in a row: grow, shrink and basis in Flexbox](tutorial:cards-in-a-row), where cards share one row and every pixel
of their width counts.

## Margin collapse, more closely

On [The box model: padding, border and
margin](tutorial:the-box#why-does-this-happen) we saw that when a bottom
margin meets a top margin, the larger one sets the gap. This is *margin
collapse*. Three more things about it are worth knowing.

1. **It happens in normal flow.** The children of an element with
   `display: flex` keep their margins apart, and the margins add up.
2. **It can happen between a parent and its first child.** Suppose a
   box has no border and no padding at the top. Then the top margin of
   its first child does not stay inside it. The margin passes through,
   and shows up above the parent instead. A little padding or a border
   on the parent keeps the child's margin inside. This surprises most
   people the first time they see it.
3. **You can find it in your own site.** On your About page, look at
   the gap above the second heading (in the starter, it says "Why Web
   Development?"). The paragraph above it has a bottom margin of `1rem`,
   from the `p` rule. The heading has a top margin of `3rem`, from the
   `.about-content h2` rule. How big is the gap? It is `3rem`, not
   `4rem`.

## How the values of `position` fit together

[A header that stays in view as you
scroll](tutorial:position-and-the-sticky-header) compared four values of
`position`. There is a fifth, `absolute`. One question sorts all five:
does the element keep its space in normal flow?

| Value | Keeps its space in the flow? | Placed against |
|---|---|---|
| `static` | Yes | Nothing: normal flow places it. This is the default. |
| `relative` | Yes | Its own place in the flow. `top` and `left` move it from there, and the space it left stays empty. |
| `sticky` | Yes | Its own place in the flow, until scrolling reaches the point set by `top`. Then the edge of the window, for as long as its parent is on screen. |
| `fixed` | No | The window. |
| `absolute` | No | The nearest element around it that has a `position` other than `static`. If there is none, the page itself. |

An element that keeps its space leaves room for itself in the flow,
even when it is drawn somewhere else. An element that leaves the flow
takes no room at all, and the boxes after it move up to fill the gap.
That is the clue you may have found on the sticky header page, when
`fixed` let the content slide up behind the header. Here is the same
difference between `relative` and `absolute`:

![Two panels, each holding three boxes, One, Two and Three, that start one above the other. On the left, Two has position: relative. It is drawn a little lower and to the right, and a dashed outline marks its old place, which stays empty. Three has not moved. On the right, Two has position: absolute. It has left the flow and is drawn lower down on its own, and Three has moved up into the space where Two used to be.](relative-and-absolute.svg)

Your site uses `absolute` once. The "Skip to main content" link at the
top of every page has `position: absolute`, with `top: 0` and `left: 0`.
It takes no room in the flow, so it never pushes your header down. It
stays hidden until someone presses Tab, as we see on [Styling what the visitor points at: hover and focus](tutorial:hover-and-focus).

When two boxes overlap, which one is drawn on top? For an element with
a `position` other than `static`, the `z-index` property decides. A box
with a higher `z-index` is drawn above one with a lower `z-index`. Your
header has `z-index: 100`, which keeps it drawn above the content that
scrolls under it.

Sticky headers are common on shops and news sites. The same idea works
on long tables too: `position: sticky` on a table's heading cells keeps
the heading row in view as we scroll down the rows.

## Seeing all this in the inspector

All of this is easier to believe once we see it on a real page, and
[Looking inside a page with the inspector](tutorial:the-inspector) can show it. When we
point at an element in the **Elements** tab, most browsers shade its
margin in its own colour. On a centred container, the two auto margins
show up as two equal bands, one on each side. When we select an
element, most browsers also have a panel that draws its box model as a
diagram, like the one on [The box model: padding, border and
margin](tutorial:the-box), with the real numbers for each layer.

You could try it on your own site:

1. Make your browser window as wide as it goes, and open your home page.
2. Open the inspector. In the **Elements** tab, point at a line that
   says `<div class="container">`. Can you see a shaded band on each
   side of your content?
3. Click a line that says `<div class="card">`. Find the box model
   diagram. In Chrome and Edge, it is at the top of the **Computed**
   tab. In Firefox, it is in the **Layout** tab. Does the padding it
   shows match your `.card` rule?
4. Look at the `<body>` line. Chrome and Firefox show a small **flex**
   label beside it. What does that label tell you about your `body`
   rule?

## What we have now

We can now describe how a browser places the boxes on a page, and we
know where to look when a box lands somewhere we did not expect.

| Word | Meaning | Example |
|---|---|---|
| *normal flow* | The default way a browser places boxes: block boxes stack, and inline boxes wrap in lines of text | a heading, with a paragraph under it |
| *block box* | A box that starts on a new line and fills the width of its parent | `<p>`, `<div>`, `<section>` |
| *inline box* | A box inside a line of text. It is as wide as its content, and wraps like a word. | `<em>`, `<a>` |
| `display` | Sets which kind of box an element makes | `display: block;` |
| *box-sizing* | Sets what `width` measures: the content alone (`content-box`), or the whole box (`border-box`) | `box-sizing: border-box;` |
| `position: absolute` | Takes an element out of the flow, and places it against the nearest element around it that has a `position` set | your `.skip-link` rule |
| `z-index` | Decides which of two overlapping positioned boxes is drawn on top. The higher number is on top. | `z-index: 100;` |
