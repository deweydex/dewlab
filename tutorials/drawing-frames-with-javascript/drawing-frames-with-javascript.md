---
title: "Drawing frames with JavaScript"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    touches: [WA-LO2, WA-LO9]
  now-add-your-own:
    touches: [WA-LO2]
---

# Drawing frames with JavaScript

On the last three pages, the browser drew every frame for us, from the
few key frames we wrote down. This page does the opposite. We draw
every frame ourselves, in JavaScript, and the browser only tells us
when it is time for the next one. On this page we:

- draw a sun and a ball on a canvas
- make them move with an animation loop
- draw the far one first, so that the near one covers it

This is the first JavaScript on this course. JavaScript is the language
that makes a web page do things after it has loaded, and this page is
a first taste of it. Nothing here needs to be memorised. Read the code
alongside the explanation below it, then change something and press
Run. The ball in orbit is the same one as on [A Point on the
Screen](tutorial:a-point-on-the-screen#a-ball-in-orbit), on the
Computational Methods course, written in a different language.

## Let's try it

This editor has a third pane, for JavaScript. HTML and CSS update the
preview as we type, as they have all along. JavaScript runs only when
we press **Run** in its pane, or Ctrl+Enter inside it.

Here is a canvas, and the JavaScript that draws on it.

```html site
id: orbit-canvas-html
site: orbit-canvas
<canvas id="screen" width="320" height="200"></canvas>
```

```css site
id: orbit-canvas-css
site: orbit-canvas
canvas {
  background: #1b1f2a;
}
```

```js site
id: orbit-canvas-js
site: orbit-canvas
const canvas = document.getElementById("screen");
const pen = canvas.getContext("2d");
const glass = 200;   // how far the screen stands from your eye, in pixels
const middleX = canvas.width / 2;
const middleY = canvas.height / 2;

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

let angle = 0;

function frame() {
  pen.fillStyle = "#1b1f2a";
  pen.fillRect(0, 0, canvas.width, canvas.height);

  const sun = { x: 0, y: 0.2, z: 4 };
  const ball = { x: 1.5 * Math.cos(angle), y: 0.2, z: 4 + 1.5 * Math.sin(angle) };

  // Draw the farther one first, so the nearer one covers it.
  const farthestFirst = [sun, ball].sort((a, b) => b.z - a.z);
  for (const body of farthestFirst) {
    if (body === sun) drawBall(body, 0.5, "#f5c542");
    else drawBall(body, 0.2, "white");
  }

  angle = angle + 0.02;
  requestAnimationFrame(frame);
}

frame();
```

1. Press **Run**. What does the ball do? Does it pass behind the sun?
2. Change `angle + 0.02` to `angle + 0.05`, and press Run again. How
   long does one turn take now?
3. Put it back to `0.02`. Now delete the line
   `pen.fillRect(0, 0, canvas.width, canvas.height);` near the top of
   `frame`, and press Run. What do you see?
4. Put that line back, and press Run once more.

## Why does this happen?

Now we can explain what we saw.

### The canvas

A *canvas* is a blank rectangle of pixels that JavaScript can draw on.
The `<canvas>` element makes one, and its `width` and `height` set how
many pixels it has. Nothing else on this course has needed one, because
HTML and CSS describe a page and the browser draws it. A canvas is for
when we want to do the drawing ourselves.

`getContext("2d")` gives us the pen that draws on it. The code calls it
`pen`:

- `fillStyle` sets the colour for the next shape
- `fillRect` draws a rectangle
- `beginPath` starts a new shape
- `arc` describes a circle, or part of one
- `fill` colours in the shape that was just described

### Where a point lands

`project` does by hand what `perspective` did for us on the CSS pages.
It divides a point's `x` and `y` by its depth, `z`, so that far things
come closer to the middle. This is called the *perspective divide*. It
makes two changes to fit a canvas.

First, it multiplies the result by `glass`, the distance from our eye
to the screen in pixels. The points are measured in units, and a
canvas counts in pixels. Second, it adds the middle of the canvas,
because a canvas puts `(0, 0)` in its top-left corner, and not at the
centre:

![A rectangle for the canvas, 320 wide and 200 tall. Its top-left corner is marked (0, 0), with an arrow along the top saying "x grows to the right" and an arrow down the left side saying "y grows downwards". A cross in the middle is marked (160, 100), middleX, middleY. The bottom-right corner is marked (320, 200).](canvas-coordinates.svg)

A canvas also counts `y` downwards. So the `0.2` in the sun and the
ball puts them a little below eye level, and we look slightly down on
the orbit.

The ball's radius is multiplied by `glass / z`, the same divide again,
so it shrinks as the ball goes away. We can check one number. The sun is
at depth 4, so its radius of `0.5` becomes `0.5 × 200 / 4 = 25` pixels.

### The loop

`requestAnimationFrame(frame)` is the line that makes it move. It asks
the browser to call `frame` once, just before it next draws the screen.
Many screens do that sixty times a second, and some do it more often.
Each time `frame` runs, it does the same four things:

1. Clear the canvas, by painting a dark rectangle over everything.
2. Work out where the ball is now, from `angle`.
3. Draw the sun and the ball.
4. Add a little to `angle`, and ask to be called again.

That loop, draw and ask again, is an *animation loop*. In step 3 we
took away its first step. Nothing cleared the old pictures, so every
ball ever drawn stayed on the canvas, and the ball left a white smear
behind it.

`angle` is measured in radians, where a full turn is `2π`, about
`6.28`. Adding `0.02` each time, sixty times a second, adds `1.2` a
second, so one full turn takes about five seconds. In step 2, `0.05`
adds `3` a second, so one turn takes about two seconds. On a screen
that draws more frames a second, the ball goes faster.
[How a browser draws each frame](tutorial:how-a-browser-draws-a-frame)
shows how to keep the speed the same on every screen.

### Front and back

On the CSS pages, the browser worked out what was in front of what. A
canvas has no idea. It draws whatever it is told, in the order it is
told, and each new shape covers what is already there. But the ball has
to go behind the sun for half of every turn.

So `frame` sorts the two bodies by depth, farthest first, and draws
them in that order. The nearer one is drawn last, over the farther one.
Sorting a scene by depth and drawing it from the back forwards is
called the *painter's algorithm*. It is named after the way a painter
paints the background first, and then the people in front of it.

## Now add your own

Let's add a second ball, on a smaller orbit, going the other way.

1. Under the line that makes `ball`, add a line that makes `ball2`.
   Copy the `ball` line, change both `1.5`s to `0.8`, and change both
   `angle`s to `-angle`. A minus angle goes round the other way.
2. Add `ball2` to the list in the sort line: `[sun, ball, ball2]`.
3. Press Run.

Does the new ball go behind the sun, and in front of it? What happens
if you leave `ball2` out of the list that gets sorted?

## What we have now

We can now draw on a canvas, and move what we draw with an animation
loop.

| Word | Meaning | Example |
|---|---|---|
| *canvas* | A blank rectangle of pixels that JavaScript draws on | `<canvas id="screen" width="320" height="200"></canvas>` |
| `getContext("2d")` | Gives the pen that draws on a canvas | `const pen = canvas.getContext("2d");` |
| `requestAnimationFrame()` | Asks the browser to call a function once, just before it next draws the screen | `requestAnimationFrame(frame);` |
| *animation loop* | A function that draws one frame, moves things on a little, and asks to be called again | `frame` |
| *painter's algorithm* | Sort what is to be drawn by depth, and draw from the back forwards, so nearer things cover farther ones | the sort line in `frame` |
