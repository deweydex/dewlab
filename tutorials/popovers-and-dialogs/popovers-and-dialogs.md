---
title: "Boxes over the page: popovers and dialogs"
year: "2026-2027"
version: 2026.11.03.1
---

# Boxes over the page: popovers and dialogs

Click the button below. A box opens over the page. There is no
JavaScript in this example.

```html site
id: popover-html
site: popover
<button popovertarget="tip">What is a light year?</button>
<div id="tip" popover>
  <p>The distance light travels in one year: about 9.5 trillion kilometres.</p>
</div>
```

```css site
id: popover-css
site: popover
[popover] {
  max-width: 16rem;
  padding: 1rem;
  border: 2px solid #1B2A4A;
  border-radius: 8px;
}
```

How did the button know which box to open? On this page we:

- open a box with the `popover` attribute
- open a dialog with `commandfor`, and close it again
- see the script way, and when we would still use it

## Why does this happen?

1. Click the button, then click anywhere else on the preview. What
   happens to the box?
2. Open it again and press Escape.

The `popover` attribute turns any element into a box that opens over the
page. It starts hidden. A button with `popovertarget="tip"` opens the
element whose `id` is `tip`. The browser closes a popover when we click
somewhere else or press Escape, as steps 1 and 2 showed. A popover suits
a tip, a small menu, or a note.

## A dialog

A *dialog* is a box that asks for the visitor's attention. While a modal
dialog is open, the rest of the page cannot be clicked. HTML has
`<dialog>` for this. A button opens it with two attributes:
`commandfor` names the dialog, and `command` says what to do.

```html site
id: dialog-html
site: dialog
<button commandfor="launch" command="show-modal">Launch the rocket</button>
<dialog id="launch">
  <p>Are you sure? There is no way to call it back.</p>
  <button commandfor="launch" command="close">Cancel</button>
</dialog>
```

```css site
id: dialog-css
site: dialog
dialog {
  border: 2px solid #D4692A;
  border-radius: 8px;
  padding: 1.5rem;
}
dialog::backdrop {
  background: rgb(0 0 0 / 40%);
}
```

```question
id: dialog-backdrop
type: multiple-choice
answer: 3

With the dialog open, what does `::backdrop` style?

- The dialog's own background
  - The dialog is the box, so the rule styles its inside.
- The button that opened it
  - The rule follows the button that was clicked.
- Everything behind the dialog
  - A modal dialog covers the page with a layer, and that layer is the
    backdrop.
```

`command="show-modal"` opens the dialog and darkens the page behind it.
`command="close"` closes it. These two attributes reached every major
browser in late 2025, so a very old browser ignores them.

## The script way

Here is the same dialog opened by a script. Before `commandfor`, every
dialog needed these few lines. HTML and CSS update the preview as we type. JavaScript runs only when we press **Run** in its pane, or Ctrl+Enter inside it, so press Run first.

```html site
id: dialog-script-html
site: dialog-script
<button id="open">Launch the rocket</button>
<dialog id="launch">
  <p>Are you sure?</p>
  <button id="cancel">Cancel</button>
</dialog>
```

```js site
id: dialog-script-js
site: dialog-script
const dialog = document.querySelector("#launch");
document.querySelector("#open").addEventListener("click", function () {
  dialog.showModal();
});
document.querySelector("#cancel").addEventListener("click", function () {
  dialog.close();
});
```

A script is still the right tool when the dialog must open by itself,
for example after a visitor has been on the page for a minute, or when
the page needs to know which button closed it.

## Now add your own

1. Add a second button to the dialog, "Launch", that also closes it.
2. Change the popover so it holds a fact about a planet of your choice.
3. Can you make the dialog open without the darkened page behind it?
   Try `command="show"` in place of `show-modal`.

## What we have now

| Word | Meaning | Example |
|---|---|---|
| `popover` | Turns an element into a box that opens over the page and closes on a click elsewhere | `<div id="tip" popover>` |
| `popovertarget` | Makes a button open the popover with that `id` | `<button popovertarget="tip">` |
| `<dialog>` | A box that asks for the visitor's attention | `<dialog id="launch">` |
| `commandfor` and `command` | Make a button open or close a dialog, with no script | `commandfor="launch" command="show-modal"` |
| `::backdrop` | The layer behind a modal dialog | `dialog::backdrop { … }` |
