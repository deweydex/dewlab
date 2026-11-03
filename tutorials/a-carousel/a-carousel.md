---
title: "Pictures in a row: a carousel"
year: "2026-2027"
version: 2026.11.03.1
---

# Pictures in a row: a carousel

A *carousel* shows one picture at a time from a row of them. Scroll the
row below sideways, with a trackpad, a finger, or Shift and the mouse
wheel. Where does each picture stop?

```html site
id: snap-html
site: snap
<div class="row">
  <div class="slide mercury">Mercury</div>
  <div class="slide venus">Venus</div>
  <div class="slide earth">Earth</div>
  <div class="slide mars">Mars</div>
</div>
```

```css site
id: snap-css
site: snap
.row {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 1rem;
}
.slide {
  flex: 0 0 100%;
  scroll-snap-align: center;
  height: 10rem;
  display: grid;
  place-items: center;
  font-size: 2rem;
  color: white;
  border-radius: 8px;
}
.mercury { background: #8c8c8c; }
.venus { background: #c9a227; }
.earth { background: #2b6cb0; }
.mars { background: #c0392b; }
```

Each picture stops in the middle, never halfway. On this page we:

- make a row that stops on each picture, with scroll snap
- make pictures change on their own, with a CSS animation
- see the script way, and when we would still use it

## Why does this happen?

1. Delete the line `scroll-snap-type: x mandatory;` and scroll again.
   What changes? Put it back.
2. Change `flex: 0 0 100%;` to `flex: 0 0 60%;`. How many pictures can
   we see now?

`overflow-x: auto` lets the row scroll sideways. *Scroll snap* makes the
scroll stop at set places. `scroll-snap-type: x mandatory` on the row
turns it on, sideways. `scroll-snap-align: center` on each slide says to
stop when that slide is in the middle. Without it, as step 1 showed, the
row stops wherever the scroll happens to end.

## Pictures that change on their own

A row that cycles by itself needs a timer. CSS has one: an animation
with keyframes, which we met in *Animation with keyframes*.

```html site
id: cycle-html
site: cycle
<div class="window">
  <div class="strip">
    <div class="slide mercury">Mercury</div>
    <div class="slide venus">Venus</div>
    <div class="slide earth">Earth</div>
    <div class="slide mars">Mars</div>
  </div>
</div>
```

```css site
id: cycle-css
site: cycle
.window {
  overflow: hidden;
  border-radius: 8px;
}
.strip {
  display: flex;
  width: 400%;
  animation: cycle 12s infinite;
}
.slide {
  width: 25%;
  height: 10rem;
  display: grid;
  place-items: center;
  font-size: 2rem;
  color: white;
}
.mercury { background: #8c8c8c; }
.venus { background: #c9a227; }
.earth { background: #2b6cb0; }
.mars { background: #c0392b; }
@keyframes cycle {
  0%, 20% { transform: translateX(0); }
  25%, 45% { transform: translateX(-25%); }
  50%, 70% { transform: translateX(-50%); }
  75%, 95% { transform: translateX(-75%); }
  100% { transform: translateX(0); }
}
.window:hover .strip {
  animation-play-state: paused;
}
@media (prefers-reduced-motion: reduce) {
  .strip { animation: none; }
}
```

The four slides sit side by side in one long strip, and the window shows
one at a time. The animation moves the strip a quarter of its width every
three seconds. Between those moves, each pair of percentages, such as
`0%, 20%`, holds the strip still.

```question
id: cycle-hover
type: multiple-choice
answer: 2

What does the rule `.window:hover .strip` do?

- It moves to the next slide.
  - Pointing at the window starts the next move.
- It pauses the animation while the pointer is over it.
  - `animation-play-state: paused` stops the animation where it is.
- It hides the window.
  - The rule changes how the strip looks.
```

The last rule turns the animation off for visitors who have asked their
computer for less movement. Moving pictures can make some people feel
unwell.

## The script way

HTML and CSS update the preview as we type. JavaScript runs only when we press **Run** in its pane, or Ctrl+Enter inside it, so press Run before you try it.

```html site
id: cycle-script-html
site: cycle-script
<div id="slide" class="slide">Mercury</div>
```

```css site
id: cycle-script-css
site: cycle-script
.slide {
  height: 10rem;
  display: grid;
  place-items: center;
  font-size: 2rem;
  color: white;
  background: #8c8c8c;
  border-radius: 8px;
}
```

```js site
id: cycle-script-js
site: cycle-script
const planets = [
  { name: "Mercury", colour: "#8c8c8c" },
  { name: "Venus", colour: "#c9a227" },
  { name: "Earth", colour: "#2b6cb0" },
  { name: "Mars", colour: "#c0392b" },
];
let current = 0;
const slide = document.querySelector("#slide");
setInterval(function () {
  current = (current + 1) % planets.length;
  slide.textContent = planets[current].name;
  slide.style.background = planets[current].colour;
}, 3000);
```

`setInterval` runs the function every 3000 milliseconds. The `%` gives
the remainder after dividing, so `current` goes 0, 1, 2, 3 and back to 0.

A script is still the right tool when the visitor needs Next and
Previous buttons, or when the list of pictures comes from somewhere else,
such as a server.

## Now add your own

1. Add Jupiter to the scroll-snap row, with a colour of your choice.
2. In the animation, make each slide stay for longer. Which number would
   you change?
3. Add Jupiter to the script version. Do you need to change anything
   besides the list?

## What we have now

| Word | Meaning | Example |
|---|---|---|
| *carousel* | A row of pictures that shows one at a time | |
| `scroll-snap-type` | Turns on scroll snap for a scrolling box | `scroll-snap-type: x mandatory` |
| `scroll-snap-align` | Where each item stops when the box snaps | `scroll-snap-align: center` |
| `prefers-reduced-motion` | Matches a visitor who has asked for less movement | `@media (prefers-reduced-motion: reduce)` |
| `setInterval` | Runs a function again and again, every so many milliseconds | `setInterval(next, 3000)` |
