---
title: "The cascade: which CSS rule wins"
year: "2026-2027"
version: 2026.09.22.1
context_for: [a-rule-and-where-it-lives, variables-and-colour, text-and-units, selectors-and-classes]
---

# The cascade: which CSS rule wins

What happens when two CSS rules set the same property on the same
element? Four pages each meet a piece of the answer: [CSS rules and
stylesheets](tutorial:a-rule-and-where-it-lives), [Colours, and naming
them with variables](tutorial:variables-and-colour), [Text size, units
and alignment](tutorial:text-and-units) and [Choosing what to style:
selectors and classes](tutorial:selectors-and-classes). This page puts
the pieces together. It is background reading. You do not need it to
finish those pages, but it can help you see why they work.

On this page we:

- see where the styles on a page come from
- find out which rule wins when two rules disagree
- see how some properties pass down to the elements inside
- find the rules that lost, crossed out, in the browser inspector

## Where styles come from

Sometimes we might notice that a page with no CSS at all still has
some style. Headings are large and bold, and links are blue and
underlined. Where do those styles come from?

Every browser has its own built-in stylesheet. It gives each element a
starting look: a margin above and below each paragraph, a large bold
font for headings, blue underlined links. Our own stylesheet is applied
on top of it, and our rules win wherever the two disagree.

So the styles on a page come in layers. The browser's built-in rules
come first, and our rules come after them. But our stylesheet can also
disagree with itself. Two of our own rules can both match one element,
and both set its colour. Which one wins then?

## Two rules, one element

Here are two paragraphs, one of them inside a highlighted box. The CSS
has two rules, and both of them set `color`.

```html site
id: cascade-html
site: cascade
<p>A plain paragraph.</p>
<div class="highlight">
  <p>A paragraph in the highlighted box.</p>
</div>
```

```css site
id: cascade-css
site: cascade
.highlight p {
  color: firebrick;
}
p {
  color: darkslateblue;
}
```

1. Both rules match the paragraph in the box. The `p` rule comes later
   in the file. Which colour does that paragraph get?
2. Change the selector `.highlight p` to plain `p`. Now the two rules
   have the same selector. Which colour wins now?
3. Move the whole `firebrick` rule to the bottom, under the other one.
   Which colour wins this time?

Now we can explain what we saw. The browser has a fixed set of steps
for deciding which declaration wins, when several set the same
property on one element. This set of steps is called the *cascade*.
Two of its steps explain almost everything we meet in our own
stylesheets:

1. **The more precise selector wins.** How precise a selector is, is
   called its *specificity*. `.highlight p` names a class and a tag, so
   it is more precise than `p`, which names only a tag. That is why the
   paragraph in the box stayed firebrick in step 1, even though the `p`
   rule came later.
2. **If the selectors are equally precise, the later rule wins.** In
   step 2, both selectors were `p`, so the later rule set the colour.
   In step 3, we moved the firebrick rule to the end, and it won.

### Counting specificity

The browser works out specificity by counting the parts of a selector,
in three columns:

| Selector | ids | classes | tags |
|---|---|---|---|
| `p` | 0 | 0 | 1 |
| `.card` | 0 | 1 | 0 |
| `.highlight p` | 0 | 1 | 1 |
| `.skills-section .card` | 0 | 2 | 0 |
| `#skills` | 1 | 0 | 0 |

To compare two selectors, the browser looks at the ids column first.
The selector with more ids wins. If that is a tie, it compares the
classes, and then the tags. A higher column always beats a lower one,
however many parts the lower one has. So `.card` beats `div div div p`,
because one class beats any number of tags.

The last row is an *id selector*: a `#` and an id, such as `#skills`.
It matches the element with `id="skills"`. You gave your skills section
that id on an earlier page. An id selector is more precise than any
number of classes. Most stylesheets use classes for styling, and keep
ids for links, like the ones in your navigation. Your starter's
`styles.css` has no id selectors at all.

A `style` attribute written on the element itself, like
`<p style="color: red">`, beats every selector in the stylesheet.
You may meet it in other people's code. It is hard to change from the
stylesheet later, because no selector can beat it.

### The same steps in your own stylesheet

Your starter's `styles.css` leans on both steps.

- **Specificity.** Section 8 has a `.btn` rule, which gives every
  button a transparent background. Section 7, earlier in the file, has
  a rule `.contact-section .btn`, which gives the button in the contact
  section a white background. It comes first, and it still wins: two
  classes beat one. If you did the practice for [CSS rules and
  stylesheets](tutorial:a-rule-and-where-it-lives), you saw the same
  thing with `h2`. The heading "Get In Touch" stayed white, because
  `.contact-section h2` beats `h2`. Moving your `h2` rule to the end of
  the file would not change that. Specificity is checked before order.
- **Order.** Section 6 gives `.hero` a padding of `var(--spacing-xl) 0`.
  Near the end of the file, inside the `@media (max-width: 768px)`
  block, another `.hero` rule sets `var(--spacing-lg) 0`. An `@media`
  rule holds other rules that apply only on some screen sizes. We meet
  them in [Changing the layout for phones: media
  queries](tutorial:media-queries). The two selectors are the same, so
  on a narrow screen the later rule wins, and the hero gets less
  padding.

That second point is why the order of a stylesheet matters. Say we add
a new `.hero` rule at the very end of the file, after the `@media`
block. It now comes later than the `@media` rule, so it wins on every
screen size, phones included, and the phone layout stops working for
the hero. That is why new rules usually go above the `@media` rules.
Your starter's sections already follow that order: every `@media` rule
is in the last section, section 13.

## Styles that pass down

Some properties pass down from an element to the elements inside it.
Here is a card with a heading and a paragraph inside. The CSS has only
one rule, for the card.

```html site
id: inherit-html
site: inherit
<div class="card">
  <h3>Sleepy Seal</h3>
  <p>Soft, grey and <em>very</em> sleepy.</p>
</div>
```

```css site
id: inherit-css
site: inherit
.card {
  color: darkslateblue;
  text-align: center;
  border: 2px solid darkslateblue;
  padding: 1rem;
}
```

1. The rule is written for `.card`. Which elements have dark blue text?
   Which have centred text?
2. Does the heading or the paragraph get a border of its own?
3. Add a second rule, `p { color: dimgray; }`. Which colour does the
   paragraph take now?

Now we can explain what we saw. *Inheritance* is how some properties
pass down from an element to the elements inside it, unless a rule
sets them there. `color` and `text-align` are inherited, so the heading
and the paragraph took both from the card. The emphasised word took the
colour from its paragraph. `border` and `padding` are not inherited, so
only the card itself got them. That is useful: if `border` passed down,
the heading and the paragraph would each draw a border of their own,
inside the card's.

| Inherited | Not inherited |
|---|---|
| `color` | `background` |
| `font-size` | `padding` |
| `font-family` | `border` |
| `font-weight` | `margin` |
| `text-align` | `width` |
| every CSS variable | |

In step 3, the paragraph turned grey. A rule written for the element
itself always beats a value it inherits, however precise the parent's
selector is. Inheritance is only the starting value, for when no rule
matches the element.

This explains a few things on the other pages:

- On [Text size, units and alignment](tutorial:text-and-units), the
  words in both boxes grew when we changed the font size on `<html>`.
  Neither box set a font size, so both inherited it.
- On [Colours, and naming them with
  variables](tutorial:variables-and-colour), the variables live in
  `:root`. A CSS variable is inherited too, and `:root` matches
  `<html>`, which holds every element on the page. So every element
  can read them. A variable defined on one element reaches only the
  elements inside it.
- In your starter, the `body` rule sets `color`, `font-family` and
  `line-height`. Those three reach every element on the page, from one
  rule. The `.hero` rule sets `color: var(--white)` and
  `text-align: center`, and the heading and paragraph inside the hero
  take both.

And why do links stay blue inside a paragraph with a different colour?
The browser's built-in stylesheet has a rule for `<a>` that sets its
colour. A rule for the element itself beats an inherited value, so the
link keeps its own colour. Your starter's `a` rule replaces that
built-in colour with `var(--accent-color)`.

## Rules that lost, in the inspector

[Looking inside a page with the inspector](tutorial:the-inspector)
showed how to select an element. Beside the HTML, Chrome and Edge show
a **Styles** pane. Firefox calls it **Rules**. It lists every rule that
matches the selected element, with the winning rule at the top. When a
declaration has lost to another one, the inspector draws a line through
it.

Here is roughly what the pane shows for the paragraph in the highlighted
box, in the first example on this page:

![A simplified drawing of the inspector's Styles pane, with the paragraph in the highlighted box selected. At the top is the rule .highlight p, with color firebrick. Under it is the rule p, with color darkslateblue drawn with a line through it, because it lost. At the bottom is a rule labelled user agent stylesheet: the browser's built-in rule for p, with display block and a top and bottom margin of 1em.](inspector-crossed-out.svg)

The last block is the browser's built-in stylesheet. Chrome and Edge
label it **user agent stylesheet**. The *user agent* is the program that
fetches and shows the page for the user, which is the browser.

You could try it on your own site:

1. Open your home page, and scroll to the contact section you added on
   [Links to pages, other sites and email](tutorial:three-kinds-of-link).
2. Right-click the button "Send Me an Email", and choose **Inspect**.
3. In the **Styles** pane, find the rule `.contact-section .btn` near
   the top. Under it is the `.btn` rule. Which of its declarations are
   crossed out?
4. Scroll further down. Can you find the `a` rule, and under it a rule
   from the user agent stylesheet? Which of their declarations lost?
5. Further down again, the pane lists styles **Inherited from** the
   elements around the button. Can you find `.contact-section` there,
   with its `text-align: center`?

In the `.btn` rule, `background-color` and `color` are crossed out,
because `.contact-section .btn` sets both and is more precise. In the
`a` rule, `color` and `text-decoration` are crossed out, because `.btn`
beats `a`. In the built-in rule, the blue colour and the underline are
crossed out too. Your own rules always beat the browser's built-in
ones, whatever their selectors.

When a style does not show up on a page, this is often the fastest way
to find out why. If the declaration is not in the pane at all, the
selector does not match the element. If it is there but crossed out,
another rule won, and the pane shows which one.

## What we have now

We can now say which of two rules wins, and we know where to look when
a style does not show up.

| Word | Meaning | Example |
|---|---|---|
| *cascade* | The steps a browser follows to decide which declaration wins, when several set the same property on one element | the more precise selector wins; if they are equal, the later rule wins |
| *specificity* | How precise a selector is. The browser counts ids, then classes, then tags. | `.highlight p` beats `p` |
| *id selector* | A `#` and an id. It matches the element with that `id`, and beats any number of classes. | `#skills` |
| *inheritance* | How some properties, such as `color` and `font-size`, pass down to the elements inside | `.card { color: darkslateblue; }` colours the card's paragraph too |
| *user agent stylesheet* | The browser's built-in stylesheet. Our rules come after it, so they win where the two disagree. | blue, underlined links |
