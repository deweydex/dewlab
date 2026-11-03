---
title: "A panel that opens and closes: details and summary"
year: "2026-2027"
version: 2026.11.03.1
---

# A panel that opens and closes: details and summary

A page of questions often hides each answer until we click its question.
For years that needed a script. Today HTML has an element made for it.
On this page we:

- open and close a panel with `<details>` and `<summary>`
- make a set of panels where only one is open at a time
- see the script way, and when we would still use it

## Let's try it

```html site
id: planets-details-html
site: planets-details
<details>
  <summary>How far is Mars from the Sun?</summary>
  <p>About 228 million kilometres, one and a half times as far as Earth.</p>
</details>
<details>
  <summary>How long is a day on Mars?</summary>
  <p>24 hours and 37 minutes, very close to a day on Earth.</p>
</details>
```

```css site
id: planets-details-css
site: planets-details
details {
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  padding: 0.5rem 1rem;
}
summary {
  cursor: pointer;
  font-weight: bold;
}
details[open] {
  background: #f6f4f0;
}
```

1. Click each question. Click it again.
2. Press Tab until a question is selected, then press Enter. Does the
   keyboard open it too?
3. Add the word `open` inside the first `<details>` tag, so it reads
   `<details open>`. What changes?

## Why does this happen?

`<details>` is a panel that opens and closes on its own. Its
`<summary>` is the part that always shows, and a click on it opens or
closes the rest. The browser does all of this, so there is no script to
write.

- The browser adds the small triangle beside each summary.
- A keyboard reaches each summary with Tab, and Enter opens it. A screen
  reader announces it as something that expands. We got that for free in
  step 2.
- While a panel is open, the browser adds the attribute `open` to its
  tag. The CSS rule `details[open]` styles only open panels. In step 3 we
  added `open` ourselves, so the panel started open.

## Only one open at a time

Sometimes we want a set of panels where opening one closes the others.
That is called an *accordion*. Give every `<details>` in the set the
same `name`.

```question
id: details-name
type: multiple-choice
answer: 2

Three panels all have `name="faq"`. The first is open. What happens when
we click the third?

- The third opens, and the first stays open.
  - Panels open and close one at a time, so the first is not touched.
- The third opens, and the first closes.
  - The shared name makes them one group, and a group allows one open
    panel.
- Nothing happens until the first is closed.
  - The group waits for the open panel to close.
```

Try it. In the HTML above, add `name="mars"` to both `<details>` tags,
then open one and then the other.

## The script way

Before `<details>` reached every browser, around 2020, a page built the
same thing from a button, a hidden box and a script. Here is that
version. HTML and CSS update the preview as we type. JavaScript runs only when we press **Run** in its pane, or Ctrl+Enter inside it, so press Run first.

```html site
id: planets-script-html
site: planets-script
<button id="toggle" aria-expanded="false">How far is Mars from the Sun?</button>
<div id="answer" hidden>
  <p>About 228 million kilometres.</p>
</div>
```

```js site
id: planets-script-js
site: planets-script
const button = document.querySelector("#toggle");
const answer = document.querySelector("#answer");
button.addEventListener("click", function () {
  const isOpen = !answer.hidden;
  answer.hidden = isOpen;
  button.setAttribute("aria-expanded", String(!isOpen));
});
```

It works, but we had to write three things ourselves that `<details>`
gives us: the click, the keyboard, and the `aria-expanded` attribute
that tells a screen reader whether the panel is open.

A script is still the right tool when the panel needs to do more than
open, for example load its answer from a server the first time it
opens.

## Now add your own

1. Add a third question about a planet of your choice.
2. Give all three the same `name`, so only one opens at a time.
3. Can you style the summary of an open panel differently from a closed
   one? `details[open] summary` selects it.

## What we have now

| Word | Meaning | Example |
|---|---|---|
| `<details>` | A panel that opens and closes when its summary is clicked | `<details>…</details>` |
| `<summary>` | The part of a `<details>` that always shows | `<summary>Question</summary>` |
| `open` | The attribute a `<details>` has while it is open | `details[open]` |
| *accordion* | A set of panels where only one is open at a time | `name="faq"` on each `<details>` |
