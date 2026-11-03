---
title: "A gallery that opens each picture"
year: "2026-2027"
version: 2026.11.03.1
---

# A gallery that opens each picture

A gallery shows small versions of its pictures, and opens a large one
when we click. Click a planet below. Then press Escape.

```html site
id: gallery-html
site: gallery
<div class="thumbs">
  <button class="thumb mercury" commandfor="big-mercury" command="show-modal">Mercury</button>
  <button class="thumb earth" commandfor="big-earth" command="show-modal">Earth</button>
  <button class="thumb mars" commandfor="big-mars" command="show-modal">Mars</button>
</div>

<dialog id="big-mercury" class="big mercury">
  <p>Mercury, the smallest planet</p>
  <button commandfor="big-mercury" command="close">Close</button>
</dialog>
<dialog id="big-earth" class="big earth">
  <p>Earth, the only planet we know has life</p>
  <button commandfor="big-earth" command="close">Close</button>
</dialog>
<dialog id="big-mars" class="big mars">
  <p>Mars, the red planet</p>
  <button commandfor="big-mars" command="close">Close</button>
</dialog>
```

```css site
id: gallery-css
site: gallery
.thumbs {
  display: flex;
  gap: 0.5rem;
}
.thumb {
  width: 6rem;
  height: 6rem;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
}
.big {
  width: min(30rem, 90vw);
  height: 16rem;
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1.5rem;
}
.big::backdrop {
  background: rgb(0 0 0 / 60%);
}
.mercury { background: #8c8c8c; }
.earth { background: #2b6cb0; }
.mars { background: #c0392b; }
```

Each small picture is a button, and each large one is a dialog. On this
page we:

- build a gallery from buttons and dialogs, with no script
- see why each small picture is a button
- see the script way, with one dialog for every picture

## Why does this happen?

The page *Boxes over the page* showed how `commandfor` and `command`
open and close a dialog. A gallery is the same idea, once per picture.

- Each small picture is a `<button>` whose `commandfor` names its own
  dialog.
- `command="show-modal"` opens that dialog and darkens the page.
- The Close button inside, and the Escape key, close it again.

On a real site, each button would hold an `<img>`, and so would each
dialog, a larger copy. We use coloured boxes here so the page needs no
picture files.

```question
id: gallery-button
type: multiple-choice
answer: 2

Why is each small picture a `<button>`, and not an `<img>` with a click
on it?

- A button is the only element that can show colour.
  - Colour needs a button.
- A button can be reached with Tab and pressed with Enter.
  - A keyboard and a screen reader both treat a button as something to
    press.
- An image cannot sit next to another image.
  - Images need buttons to line up.
```

Press Tab until a planet is selected, then press Enter. The gallery
works with a keyboard because every picture is a button.

## The script way

Three planets need three dialogs. With a script, one dialog can show any
of them: the script copies the planet's name and colour into it before it
opens. HTML and CSS update the preview as we type. JavaScript runs only when we press **Run** in its pane, or Ctrl+Enter inside it, so press Run first.

```html site
id: gallery-script-html
site: gallery-script
<div class="thumbs">
  <button class="thumb" data-name="Mercury" data-colour="#8c8c8c">Mercury</button>
  <button class="thumb" data-name="Earth" data-colour="#2b6cb0">Earth</button>
  <button class="thumb" data-name="Mars" data-colour="#c0392b">Mars</button>
</div>
<dialog id="big">
  <p id="big-name"></p>
  <button commandfor="big" command="close">Close</button>
</dialog>
```

```css site
id: gallery-script-css
site: gallery-script
.thumbs { display: flex; gap: 0.5rem; }
.thumb { width: 6rem; height: 6rem; border: none; border-radius: 8px; }
#big { width: min(30rem, 90vw); height: 16rem; border: none; border-radius: 12px; color: white; font-size: 1.5rem; }
```

```js site
id: gallery-script-js
site: gallery-script
const big = document.querySelector("#big");
const bigName = document.querySelector("#big-name");
for (const thumb of document.querySelectorAll(".thumb")) {
  thumb.style.background = thumb.dataset.colour;
  thumb.style.color = "white";
  thumb.addEventListener("click", function () {
    bigName.textContent = thumb.dataset.name;
    big.style.background = thumb.dataset.colour;
    big.showModal();
  });
}
```

Each button keeps its planet's name and colour in `data-` attributes, and
`dataset` reads them. The script version is shorter when a gallery has
many pictures, because it needs only one dialog. The HTML version needs
no script and keeps working if a script fails to load. A gallery of a
handful of pictures suits HTML. A gallery of fifty, or one whose
pictures come from a server, suits a script.

## Now add your own

1. Add Venus to the HTML gallery. You need a button and a dialog, with
   matching names.
2. Add Venus to the script gallery. How many places did you change this
   time?
3. In the HTML gallery, add a sentence about each planet inside its
   dialog.

## What we have now

| Word | Meaning | Example |
|---|---|---|
| `command="show-modal"` | Opens a dialog and darkens the page behind it | `<button commandfor="big" command="show-modal">` |
| `command="close"` | Closes a dialog | `<button commandfor="big" command="close">` |
| `data-` attribute | Keeps a value of our own on an element, for a script to read | `data-name="Mars"` |
| `dataset` | A script's way to read an element's `data-` attributes | `thumb.dataset.name` |
