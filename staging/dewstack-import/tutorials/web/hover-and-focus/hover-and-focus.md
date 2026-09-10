---
title: "States: hover and focus"
slug: hover-and-focus
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# States: hover and focus

Move your pointer over the button below, then move it away. Now click the
button once and press Tab, then Shift+Tab, to bring keyboard focus back to
it.

```html site=states
<button class="btn">Hover me, or Tab to me</button>
```

```css site=states
.btn {
  padding: 10px 16px;
  border: 2px solid #2c3e50;
  border-radius: 6px;
  background: #f6f4f0;
  font-size: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
}
.btn:focus {
  outline: 3px solid #d9720c;
  outline-offset: 2px;
}
```

The button lifts and its shadow deepens under the pointer. A thick
outline appears when it has keyboard focus. These are two different
states, and a person using a mouse may never see the second one.

## Why this happens

`:hover` matches an element while a pointer sits over it. `transition` on
the button's base rule, not on `:hover` itself, is what makes the change
smooth in both directions, lifting and settling back.

`:focus` matches whichever element currently has keyboard focus, usually
because someone pressed Tab to reach it. Without a visible focus style, a
person moving through a page by keyboard has no way to see where they
are. That is why focus styles matter for accessibility, and why removing
one is a real loss even though it changes nothing for a mouse user.

## Your turn

Let's open your fork and find the `.card` rule in `styles.css`. Try
adding a hover effect:

```css
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
```

Then find `a:focus`. Try pressing Tab repeatedly on your page and watch
the outline move between links. The very first press lands on a hidden
"Skip to main content" link. Look for `.skip-link` in the CSS to see
how it stays hidden until it has focus.

## What you have now

Two states a reader can trigger without typing anything, one with a
pointer and one with a keyboard.

- **`:hover`** — matches an element while a pointer sits over it.
- **`:focus`** — matches whichever element currently has keyboard focus.
- **`transition`** — animates a change smoothly, defined on the base
  state rather than the state that triggers it.
