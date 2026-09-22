---
title: "Keyframe animation and the checkbox hack"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
    touches: [WA-LO2]
  now-add-your-own:
    touches: [WA-LO2, WA-LO9]
---

# Keyframe animation and the checkbox hack

On [Transitions and transforms](tutorial:transitions-and-transforms),
`transition` animated a change between two states. It needed something
to trigger it, such as `:hover`. Can CSS move something with no trigger
at all? Can it answer a click, with no JavaScript? On this page we:

- watch a button that animates on its own, and change how it moves
- open and close a question with a hidden checkbox
- add a second animation and a second question of our own

## Let's try it

### A button that moves on its own

Here is one button, and a `@keyframes` rule that describes how it
moves.

```html site
id: pulse-html
site: pulse
<button class="pulse">Loading…</button>
```

```css site
id: pulse-css
site: pulse
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.08);
    opacity: 0.8;
  }
}
.pulse {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background: #2c3e50;
  color: white;
  animation: pulse 1.5s ease-in-out infinite;
}
```

1. Watch the button for a few seconds. What does it do? Did you do
   anything to start it?
2. What happens if we change `1.5s` to `4s`?
3. What if we change `scale(1.08)` to `scale(1.5)`?
4. What if we change `infinite` to `3`? Watch until the button stops.
   How does it look when it stops?

### A question that opens

The second box shows a question. Its answer is hidden. There is no
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

Now we can explain what we saw in both boxes.

### How the pulse works

The button grows a little, fades a little, and goes back, again and
again. Nothing triggers it. A `@keyframes` animation moves through
several stages on its own, so it does not need a trigger.

`@keyframes pulse` names three stages. Each stage is a percentage of
the way through the animation:

| Stage | `transform` | `opacity` |
|---|---|---|
| `0%`, the start | `scale(1)`: normal size | `1`: fully solid |
| `50%`, halfway | `scale(1.08)`: a little bigger | `0.8`: a little see-through |
| `100%`, the end | `scale(1)`: normal size | `1`: fully solid |

`opacity` sets how solid an element looks. `1` is fully solid and `0`
is invisible. The rule writes `0%, 100%` together because the start and
the end are the same. The browser fills in every frame between one
stage and the next on its own, the same way it fills in a `transition`.

The `animation` line then puts the keyframes to work. It combines four
settings in one line:

```css
animation: pulse 1.5s ease-in-out infinite;
```

1. `pulse`: the name of the `@keyframes` rule to follow.
2. `1.5s`: how long one pass takes.
3. `ease-in-out`: the speed curve, which is how the animation speeds up
   and slows down.
4. `infinite`: how many times to repeat it. `infinite` means it never
   stops on its own.

A number in place of `infinite`, such as `3`, runs the animation that
many times and then stops. After the last pass, the button goes back to
its own normal style. In step 4 of the first box, that looks the same as the `100%` stage,
because the `100%` stage matches the button's normal style.

### How the checkbox hack works

The answer slides open when we click the question, and closes when we
click again. The pattern behind it is called the *checkbox hack*. The
checkbox hack is a hidden checkbox, a label linked to it with `for`, and
a `:checked ~` rule. Together, they reveal content only while the
checkbox is ticked. Here is each part:

- `display: none` on `.toggle` hides the checkbox completely. That is
  why we could not see it in step 2.
- The label's `for="q1"` links it to the checkbox whose `id` is `q1`.
  Clicking the label's text ticks or unticks the box, even while the box
  itself is hidden.
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
  it would otherwise snap. That is what step 4 of the second box
  showed, at a slower speed.

Sometimes we might notice that a longer answer gets cut off. The open
answer can grow only to its `max-height`, and `overflow: hidden` hides
the rest. Why not use `height` instead? A transition cannot animate
`height` to `auto`, the height of the content. `max-height` with a fixed
number can be animated, so we choose a number larger than the content
will ever need.

Two more things are worth knowing. A checkbox with `display: none`
cannot be reached with the Tab key, so this pattern is hard to use for
someone who moves through a page with a keyboard. HTML has its own
element for a question that opens, `<details>`, with a `<summary>`
inside it, which works with a keyboard by default. And some people set
their device to reduce motion on screen, because movement can make them
feel unwell. A media query, `@media (prefers-reduced-motion: reduce)`,
lets us turn an animation off for them.

## Now add your own

Both boxes above are ours to change. Let's start with the questions.

1. In the question box's HTML, add a second question below the first:
   a new checkbox, a label, and a content block.
2. Give the new checkbox its own `id`, different from `q1`. If both
   boxes had the same `id`, they would answer to the same click.
3. Give the new label a `for` that matches the new `id`.
4. Click the first question. Does the second answer open too? The `~`
   selects every `.toggle-content` that comes after the ticked box, so
   it may.
5. If it does, put each question (its checkbox, label and content)
   inside a `<div>` of its own. Then the parts of one question share a
   parent, and the other question does not.

Now the animation.

6. In the first box's HTML, add a second button below the loading one,
   with a class of its own.
7. In the CSS, add a new `@keyframes` rule with a new name.
8. Give the new button's class an `animation` that uses the new name,
   with a different duration from `1.5s`. The duration is the
   `animation-duration`, the second setting in the `animation` line.
9. Once both work, try changing the timings or the `transform` values.

Do your two buttons move at different speeds? Does each question open
on its own?

## What we have now

We can now add movement or interaction with plain CSS in two ways: one
that repeats on its own, and one that answers a click.

| Word | Meaning | Example |
|---|---|---|
| `@keyframes` | Names the stages of an animation as percentages. The browser fills in the frames between them. | `@keyframes pulse { 50% { opacity: 0.8; } }` |
| `animation` | Combines a `@keyframes` name with its duration, speed curve and repeat count in one line | `animation: pulse 1.5s ease-in-out infinite;` |
| *checkbox hack* | A hidden checkbox, a label linked to it with `for`, and a `:checked ~` rule. Together, they reveal content only while the checkbox is ticked. | `.toggle:checked ~ .toggle-content` |
