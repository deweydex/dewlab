---
title: "Opening and closing content with a checkbox"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
    touches: [WA-LO2]
  now-add-your-own:
    touches: [WA-LO2, WA-LO9]
---

# Opening and closing content with a checkbox

Many websites have a list of questions where each answer stays hidden
until we click its question. Can a page do that with no JavaScript, only
HTML and CSS? On this page we:

- open and close a question with a hidden checkbox
- see the three parts that make it work
- add a second question of our own

## Let's try it

This box shows a question. Its answer is hidden. There is no
JavaScript here, only HTML and CSS.

```html site
id: accordion-html
site: accordion
<input type="checkbox" id="q1" class="toggle">
<label for="q1" class="toggle-label">What is the checkbox hack?</label>
<div class="toggle-content">
  <p>A pattern that shows or hides content using a hidden checkbox and
  the <code>:checked</code> selector, with no JavaScript at all.</p>
</div>
```

```css site
id: accordion-css
site: accordion
.toggle {
  display: none;
}
.toggle-label {
  display: block;
  padding: 10px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  cursor: pointer;
}
.toggle-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.toggle:checked ~ .toggle-content {
  max-height: 200px;
}
```

1. Click the question. What happens? Click it again.
2. The HTML has a checkbox in it. Can you see the checkbox in the
   preview?
3. What happens if we delete `display: none;` from the `.toggle` rule?
   Click the checkbox, then click the question text. Put the line back
   afterwards.
4. What if we change `0.3s` in the `transition` to `2s`?

## Why does this happen?

Now we can explain what we saw. The answer slides open when we click
the question, and closes when we click again. The pattern behind it is
called the *checkbox hack*. The checkbox hack is a hidden checkbox, a
label linked to it with `for`, and a `:checked ~` rule. Together, they
reveal content only while the checkbox is ticked. Here is each part:

- `display: none` on `.toggle` hides the checkbox completely. That is
  why we could not see it in step 2.
- The label's `for="q1"` links it to the checkbox whose `id` is `q1`.
  Clicking the label's text ticks or unticks the box, even while the box
  itself is hidden. In step 3, with the checkbox showing, clicking
  either one ticked the box.
- `:checked` matches a checkbox only while it is ticked.
- `~` selects an element that comes after this one and shares the same
  parent. So `.toggle:checked ~ .toggle-content` means "a
  `.toggle-content` that comes after a ticked `.toggle`".
- `.toggle-content` starts with `max-height: 0` and
  `overflow: hidden`. `overflow: hidden` hides any content that does
  not fit, so the answer cannot be seen. While the box is ticked, the
  rule above gives it a taller `max-height`, `200px`, and the answer
  shows.
- The `transition` on `.toggle-content` makes that change slide, where
  it would otherwise snap. That is what step 4 showed, at a slower
  speed.

Why `max-height`, and not `height`? A transition cannot animate `height`
to `auto`, the height of the content. `max-height` with a fixed number
can be animated. So we choose a number larger than the content will
ever need, and the answer grows until it is its own full height.

This pattern has one real weakness. A checkbox with `display: none`
cannot be reached with the Tab key, so someone who uses only a keyboard
cannot open the question. HTML has its own element for a question that
opens, `<details>`, which works with a keyboard. The background page
beside this one shows it.

## Now add your own

The box above is ours to change.

1. In the HTML, add a second question below the first: a new checkbox,
   a label, and a content block.
2. Give the new checkbox its own `id`, different from `q1`. If both
   boxes had the same `id`, they would answer to the same click.
3. Give the new label a `for` that matches the new `id`.
4. Click the first question. Does the second answer open too? The `~`
   selects every `.toggle-content` that comes after the ticked box, so
   it may.
5. If it does, put each question (its checkbox, label and content)
   inside a `<div>` of its own. Then the parts of one question share a
   parent, and the other question does not.

Here is why the `<div>` helps:

![Two drawings of the same two questions. On the left, all six parts share one parent: checkbox q1, its label, answer 1, checkbox q2, its label, answer 2. Arrows from the ticked checkbox q1 reach both answers, because both come after it and share its parent, so both open. On the right, each question sits in a div of its own. The arrow from the ticked checkbox q1 reaches only answer 1, because answer 2 now has a different parent.](one-parent-or-two.svg)

Does each question open on its own now?

## What we have now

We can now show and hide content with a click, using only HTML and CSS.

| Word | Meaning | Example |
|---|---|---|
| `:checked` | Matches a checkbox only while it is ticked | `.toggle:checked` |
| `~` | Selects an element that comes after this one and shares the same parent | `.toggle:checked ~ .toggle-content` |
| *checkbox hack* | A hidden checkbox, a label linked to it with `for`, and a `:checked ~` rule. Together, they reveal content only while the checkbox is ticked. | `.toggle:checked ~ .toggle-content` |
