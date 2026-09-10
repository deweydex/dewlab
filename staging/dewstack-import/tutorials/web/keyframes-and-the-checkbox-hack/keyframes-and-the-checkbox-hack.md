---
title: "Keyframe animation and the checkbox hack"
slug: keyframes-and-the-checkbox-hack
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.05.1
---

# Keyframe animation and the checkbox hack

`transition`, on the page about [transitions and
transforms](tutorial:transitions-and-transforms), animates a change
between two states, and needs something to trigger it, such as `:hover`.
A `@keyframes` animation goes further: it moves through several stages on
its own, with nothing to trigger it at all.

```html site=pulse
<button class="pulse">Loading…</button>
```

```css site=pulse
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

## Why this happens

`@keyframes pulse` names three stages, each a percentage of the way
through: `0%`, `50%`, `100%`. The browser fills in every frame between
one stage and the next on its own, the same way it fills in a
`transition`.

`animation: pulse 1.5s ease-in-out infinite;` combines four settings in
one line: the keyframes rule to follow, how long one pass takes, and its
speed curve (how the animation speeds up and slows down). The last
setting is how many times to repeat it. `infinite`
means it never stops on its own. A number there instead, such as `3`,
would run the animation that many times and then stop on its final stage.

## A second pattern: the checkbox hack

A checkbox can show or hide content with no JavaScript at all. Click the
question below.

```html site=accordion
<input type="checkbox" id="q1" class="toggle">
<label for="q1" class="toggle-label">What is the checkbox hack?</label>
<div class="toggle-content">
  <p>A pattern that shows or hides content using a hidden checkbox and
  the <code>:checked</code> selector, with no JavaScript at all.</p>
</div>
```

```css site=accordion
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

## Why this happens

`label`'s `for="q1"` links it to the checkbox whose `id` is `q1`. Clicking
the label's text checks the box, even though `display: none` hides the
box itself. `:checked` matches only while a checkbox is
ticked, and `~` selects an element that comes after this one and shares
the same parent. Together, they give
`.toggle-content` its taller `max-height` only while the checkbox right
before it is checked. The `transition` on `.toggle-content` is what makes
that change slide rather than snap.

## Your turn

Let's try adding a second question to the accordion above. Give it a
new checkbox with its own `id`, a label with a matching `for`, and its
own content block below it. Give the checkbox a different `id` from the
first one, or the two boxes will answer to the same click. Then, in the
first editor, try adding a second button below the loading one. Give it
its own `@keyframes` rule and a different `animation-duration`, so the
two animate at different speeds. Once both work, try changing the
timings or the transform values and see what happens.

## What you have now

Two ways to add movement or interaction with plain CSS: one that repeats
on its own, one that answers a click.

- **`@keyframes`** — names the stages of an animation as percentages, and
  the browser fills in the frames between them.
- **`animation`** — combines a `@keyframes` name with its duration,
  speed curve and repeat count in one line.
- **The checkbox hack** — a hidden checkbox, a label linked to it with
  `for`, and a `:checked ~` rule. Together, they reveal content only
  while the checkbox is ticked.
