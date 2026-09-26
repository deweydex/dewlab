---
title: "How a browser draws each frame"
year: "2026-2027"
version: 2026.09.22.1
context_for: [drawing-frames-with-javascript, an-orbit-in-css, a-cube-in-css, a-ball-that-faces-you, a-cube-on-a-canvas]
---

# How a browser draws each frame

Every page in the series "Movement and depth" moves something: [An
orbit in pure CSS](tutorial:an-orbit-in-css), [A 3D cube in CSS](tutorial:a-cube-in-css), [A ball that keeps facing
you](tutorial:a-ball-that-faces-you), [Drawing frames with
JavaScript](tutorial:drawing-frames-with-javascript) and [A turning cube
drawn on a canvas](tutorial:a-cube-on-a-canvas). How does a browser
make anything move at all? This page is background reading. You do not
need it to finish those pages, but it can help you see why they work.

On this page we:

- see why a row of still pictures looks like movement
- follow the steps a browser takes to draw one frame
- see why `transform` and `opacity` move more smoothly than other
  properties
- keep a JavaScript animation at the same speed on every screen
- turn movement down for people who ask for less of it

## Still pictures, fast enough

Nothing on a screen ever really moves. The browser draws one still
picture, a frame, and then another, many times a second. When the
pictures change a little each time, and come fast enough, our eye
blends them into movement. A film works the same way.

How many frames a second? That depends on the screen. The *refresh
rate* is how many times a second a screen shows a new picture. It is
measured in hertz, written Hz, where 1 Hz is once a second. Many
screens run at 60 Hz. Many newer phones and laptops run at 90 Hz or
120 Hz. A browser draws its frames in step with the screen, so on a
60 Hz screen it has about 16.7 milliseconds for each frame. A
millisecond is a thousandth of a second.

## What the browser does for each frame

For every frame, the browser works through the same steps, in order:

1. It runs any JavaScript that asked for this frame, with
   `requestAnimationFrame`.
2. **Style.** It works out which CSS rules apply to each element, and
   their values. For a CSS animation, this is where it works out how
   far through the animation each element has got.
3. **Layout.** It works out the size and the place of every box on the
   page. [How a browser lays out a
   page](tutorial:how-a-browser-lays-out-a-page) describes the rules it
   follows.
4. **Paint.** It fills in the pixels of each part of the page: its
   colours, text, borders and shadows. Some parts are painted onto
   layers of their own, like sheets of clear plastic.
5. **Composite.** It puts the painted layers together, each one in its
   place and in the right order, to make the one picture on the screen.

*Layout*, *paint* and *composite* are the names most browsers' tools
use for those steps. If all the steps take longer than one frame, the
screen shows the old picture again, and the movement stutters.

Not every change needs every step:

![A diagram of the four steps of one frame, left to right: Style, Layout, Paint, Composite. Below them, two rows. The first row, for a change to width or left, marks all four steps as needed. The second row, for a change to transform or opacity, marks Style and Composite as needed, and Layout and Paint as steps the browser can skip.](frame-steps.svg)

## Why `transform` and `opacity` move smoothly

On [Moving things smoothly: transforms and
transitions](tutorial:transitions-and-transforms), we saw that a
transform moves an element without moving anything around it. The page
keeps the element's space exactly as it was. So when only a transform
changes, the browser has no layout to do. It can keep the picture of
the element it has already painted, and move that picture in the
composite step. The same goes for `opacity`, which only fades the
picture.

A change to `width`, `left` or `margin` is different. The box's size
or place changes, so the browser has to do the layout again, and paint
again. On a big page, that is a lot of work to fit into one frame.

Here are two boxes that slide the same distance. The first moves with
`left`, and the second with `transform`. `alternate` plays each
animation forwards, then backwards, then forwards again.

```html site
id: smooth-html
site: smooth
<div class="track"><div class="box by-left">left</div></div>
<div class="track"><div class="box by-transform">transform</div></div>
```

```css site
id: smooth-css
site: smooth
.track {
  width: 300px;
  margin: 10px 0;
  background: #f6f4f0;
}
.box {
  width: 90px;
  padding: 10px 0;
  text-align: center;
  background: #2c3e50;
  color: white;
}
.by-left {
  position: relative;
  animation: slide-left 2s ease-in-out infinite alternate;
}
.by-transform {
  animation: slide-transform 2s ease-in-out infinite alternate;
}
@keyframes slide-left {
  from { left: 0; }
  to   { left: 210px; }
}
@keyframes slide-transform {
  from { transform: translateX(0); }
  to   { transform: translateX(210px); }
}
```

On a fast computer, the two look the same. The difference shows up on
a slow phone, or on a busy page. In Chrome and Edge, we can see the
extra work:

1. Open the inspector on this page.
2. Open the menu with three dots, choose **More tools**, then
   **Rendering**.
3. Tick **Paint flashing**. The browser now marks in green every part
   of the page it paints again.
4. Watch the two boxes. Which one keeps flashing green?

Your site has an example of both kinds. In your `styles.css`, the
`.card` rule has a `transition` on `transform` and on `box-shadow`. The
lift from `transform` needs no painting. A change of shadow needs the
card to be painted again. For one card, that is very little work.

## Asking for the next frame

`requestAnimationFrame` asks the browser to call a function once, just
before the next frame. That keeps a JavaScript animation in step with
the screen: one drawing for each picture the screen shows. When the tab
is hidden, browsers stop calling it, or call it much less often, so a
page nobody is looking at does not waste power.

JavaScript has older ways to run a function again and again, such as
`setInterval`. They run on a clock of their own, which is not in step
with the screen. So a drawing can land between two frames, or two
drawings can land in the same frame, and the movement looks uneven.

If you have done the Computational Methods course, this loop will look
familiar. It is `FuncAnimation`, written out by hand. There, matplotlib
called `draw_step` once for each frame. Here, the browser calls
`frame`. Games on the web, and many animated charts, are built round a
loop like this one.

## The same speed on every screen

The orbit on the canvas adds `0.02` to `angle` in every frame. On a
60 Hz screen, one turn takes about five seconds. On a 120 Hz screen,
`frame` runs twice as often, so one turn takes about two and a half.

CSS animations do not have this problem. `6s` means six seconds on
every screen, because the browser works out how far through the
animation it is from the time, in the style step.

A JavaScript animation can do the same. `requestAnimationFrame` gives
the function it calls one number: the time, in milliseconds, since the
page started to load. We can work out the angle from the time, and not
from a count of frames:

```html site
id: timed-orbit-html
site: timed-orbit
<canvas id="screen" width="320" height="200"></canvas>
```

```css site
id: timed-orbit-css
site: timed-orbit
canvas {
  background: #1b1f2a;
}
```

```js site
id: timed-orbit-js
site: timed-orbit
const canvas = document.getElementById("screen");
const pen = canvas.getContext("2d");
const glass = 200;
const middleX = canvas.width / 2;
const middleY = canvas.height / 2;
const radiansPerSecond = 1.2;   // the same on any screen

function project(point) {
  return {
    x: middleX + glass * point.x / point.z,
    y: middleY + glass * point.y / point.z,
    scale: glass / point.z,
  };
}

function drawBall(point, radius, colour) {
  const onScreen = project(point);
  pen.fillStyle = colour;
  pen.beginPath();
  pen.arc(onScreen.x, onScreen.y, radius * onScreen.scale, 0, 2 * Math.PI);
  pen.fill();
}

function frame(time) {
  const angle = (time / 1000) * radiansPerSecond;

  pen.fillStyle = "#1b1f2a";
  pen.fillRect(0, 0, canvas.width, canvas.height);

  const sun = { x: 0, y: 0.2, z: 4 };
  const ball = { x: 1.5 * Math.cos(angle), y: 0.2, z: 4 + 1.5 * Math.sin(angle) };

  const farthestFirst = [sun, ball].sort((a, b) => b.z - a.z);
  for (const body of farthestFirst) {
    if (body === sun) drawBall(body, 0.5, "#f5c542");
    else drawBall(body, 0.2, "white");
  }

  requestAnimationFrame(frame);
}

requestAnimationFrame(frame);
```

Three things changed from the orbit on the canvas:

1. `frame(time)` takes the time that `requestAnimationFrame` hands it.
2. `angle` is worked out from that time, so there is no `let angle`
   and no `angle + 0.02` any more. `time / 1000` is the time in
   seconds, so the ball goes round `1.2` radians a second, whatever the
   screen does.
3. The last line is `requestAnimationFrame(frame)`, and not `frame()`.
   A plain `frame()` would run once with no time at all.

A full turn is `2π` radians, about `6.28`, so one turn takes about five
seconds on a 60 Hz screen and on a 120 Hz screen alike.

## Less movement, for people who ask

Some people feel dizzy or unwell when things on a screen spin or move
in depth. They can ask their device to reduce motion. In Windows, it
is **Animation effects** in the **Visual effects** settings, under
**Accessibility**. On a Mac, it is **Reduce motion**, under
**Accessibility**, then **Display**.

A page can answer with a media query,
`@media (prefers-reduced-motion: reduce)`, which applies its CSS only
when the visitor has asked for less motion. [Accessibility: keyboards, focus and movement](tutorial:movement-focus-and-keyboards) has
more about it. For the orbit, it could stop both animations:

```css
@media (prefers-reduced-motion: reduce) {
  .orbit, .ball {
    animation: none;
  }
}
```

JavaScript can ask the same question.
`window.matchMedia("(prefers-reduced-motion: reduce)").matches` is
`true` when the visitor has asked for less motion. A canvas animation
could then draw one frame, and not ask for the next.

We can test this without changing any settings. In Chrome and Edge,
the same **Rendering** panel has a setting called **Emulate CSS media
feature prefers-reduced-motion**. It makes the page behave as if the
visitor had asked for less motion.

## What we have now

We can now say what a browser does for every frame, and why some
animations cost it more work than others.

| Word | Meaning | Example |
|---|---|---|
| *refresh rate* | How many times a second a screen shows a new picture, in hertz | `60 Hz`, `120 Hz` |
| *layout* | The step where the browser works out the size and place of every box | changing `width` needs it |
| *paint* | The step where the browser fills in the pixels of each part of the page | changing `box-shadow` needs it |
| *composite* | The step where the browser puts the painted layers together into one picture | changing `transform` needs only this, after style |
| `requestAnimationFrame(frame)` | Calls `frame` once, before the next frame, and hands it the time in milliseconds | `function frame(time) { … }` |
| `prefers-reduced-motion` | A media query that is true when the visitor has asked for less motion | `@media (prefers-reduced-motion: reduce)` |

## Where to read more

Captain Disillusion (2019). *CD / Frame Rate.*
<https://www.youtube.com/watch?v=DyqjTZHRdRs>. Captain Disillusion
explains frame rate, and why still pictures shown fast enough look like
movement. Four minutes.
