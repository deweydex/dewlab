---
title: "Styling a page from its own state: :has()"
year: "2026-2027"
version: 2026.11.03.1
---

# Styling a page from its own state: :has()

Tick the box below. The whole page turns dark. There is no script here,
only HTML and CSS.

```html site
id: dark-html
site: dark
<label><input type="checkbox" id="dark"> Night sky</label>
<h1>Tonight's sky</h1>
<p>Jupiter rises in the east after sunset.</p>
```

```css site
id: dark-css
site: dark
body {
  font-family: Georgia, serif;
  padding: 1rem;
  transition: background 0.4s, color 0.4s;
}
body:has(#dark:checked) {
  background: #0b1430;
  color: #f4f1ea;
}
```

A checkbox changed the colour of the page around it. For most of the
history of CSS, a rule could not do that. On this page we:

- style an element by what is inside it, with `:has()`
- use it to show a form's state, with no script
- see the script way, and the one thing it adds

## Why does this happen?

A CSS selector usually picks an element by its own name, class or
state. `:has()` picks an element by what is inside it.
`body:has(#dark:checked)` means "the body, if it holds a ticked
`#dark` checkbox". The checkbox sits inside the body, so ticking it
changes the body's style.

Before `:has()` reached every browser in 2023, CSS could only look
downwards and forwards, at an element's children or at what came after
it. *Opening and closing content with a checkbox* used `~` because of
that limit. Changing the page around a checkbox needed a script.

```question
id: has-card
type: multiple-choice
answer: 1

What does `.card:has(img)` select?

- Every `.card` that holds an image
  - `:has()` picks the card by what is inside it.
- Every image inside a `.card`
  - The rule styles the image, which comes last in the selector.
- Every `.card` that comes after an image
  - `:has()` looks at the cards that follow the image.
```

## A form that shows its own state

`:has()` works with any state the browser knows about, including the
state of a form.

```html site
id: has-form-html
site: has-form
<form class="card">
  <label for="planet">Your favourite planet</label>
  <input id="planet" required>
  <p class="hint">Type a planet to continue.</p>
</form>
```

```css site
id: has-form-css
site: has-form
.card {
  padding: 1rem;
  border: 2px solid #ccc;
  border-radius: 8px;
}
.card:has(:focus) {
  border-color: #1B2A4A;
}
.card:has(:valid) .hint {
  display: none;
}
```

1. Click into the box. What happens to the border around the form?
2. Type a planet. What happens to the line below the box?

`.card:has(:focus)` styles the card while anything inside it is
selected. `.card:has(:valid) .hint` hides the hint once the box is
filled, because `required` makes an empty box `:invalid`.

## The script way

HTML and CSS update the preview as we type. JavaScript runs only when we press **Run** in its pane, or Ctrl+Enter inside it, so press Run before you try it.

```html site
id: dark-script-html
site: dark-script
<label><input type="checkbox" id="dark"> Night sky</label>
<h1>Tonight's sky</h1>
```

```css site
id: dark-script-css
site: dark-script
body { font-family: Georgia, serif; padding: 1rem; }
body.night { background: #0b1430; color: #f4f1ea; }
```

```js site
id: dark-script-js
site: dark-script
const box = document.querySelector("#dark");
box.addEventListener("change", function () {
  document.body.classList.toggle("night", box.checked);
  try {
    localStorage.setItem("night", box.checked ? "yes" : "no");
  } catch (error) {
    // This preview cannot store anything. On your own site it can.
  }
});
```

The script toggles a class on the body, which `:has()` now does for us.
It adds one thing CSS cannot do: `localStorage` remembers the choice, so
on your own site the page opens dark the next time too. To remember a
visitor's choice, we still need a script.

## Now add your own

1. Change the night colours to ones of your own. Check the contrast with
   a contrast checker.
2. In the form, give the label a colour of its own while the box is
   selected. `.card:has(:focus) label` selects it.
3. Can you make the form's border green once the planet is typed?

## What we have now

| Word | Meaning | Example |
|---|---|---|
| `:has()` | Picks an element by what is inside it | `body:has(#dark:checked)` |
| `:focus` | Matches the element that is selected for typing or pressing | `.card:has(:focus)` |
| `:valid` | Matches a field that keeps all its rules | `.card:has(:valid)` |
| `localStorage` | Keeps a small piece of text in the browser for this site, until the visitor clears it | `localStorage.setItem("night", "yes")` |
