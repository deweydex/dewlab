---
title: "Drawing frames with JavaScript"
year: "2026-2027"
version: 2026.09.21.1
covers:
  why-this-happens:
    touches: [WA-LO2, WA-LO9]
  the-cube-again:
    touches: [WA-LO2]
  your-turn:
    touches: [WA-LO2]
---

# Drawing frames with JavaScript

The last two pages let the browser do the dividing by depth. This one
does the arithmetic by hand, in JavaScript, and draws the result onto
a `<canvas>` sixty times a second. It is the ball in orbit from [A
Point on the Screen](tutorial:a-point-on-the-screen#a-ball-in-orbit),
written in a different language.

This editor has a third pane. HTML and CSS update the preview as you
type, the way they have all along, but JavaScript only runs when you
press **Run** in its pane, or Ctrl+Enter inside it. Press it now.

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

## Why this happens

A `<canvas>` is a blank rectangle of pixels that JavaScript can draw
on. `getContext("2d")` hands back the pen that does the drawing:
`fillRect` for a rectangle, `arc` for a circle, `fill` to colour in
whatever path was just described.

`project` is the perspective divide, with two changes to fit a canvas.
A point's $x$ and $y$ are divided by its $z$ and then multiplied by
`glass`, the distance to the screen in pixels, since a canvas counts in
pixels rather than units. And the result is added to the middle of the
canvas, because a canvas puts $(0, 0)$ in its top-left corner rather
than at the centre. A canvas also counts $y$ downwards, so the $0.2$
in the sun and the ball puts them a little below eye level, which is
why you look slightly down on the orbit. The ball's radius is scaled by
`glass / z`, the same divide again, so it shrinks as it goes away.

`requestAnimationFrame(frame)` is the line that makes it move. It asks
the browser to call `frame` once, just before it next paints the
screen, which is usually sixty times a second. `frame` clears the
canvas, works out where the ball is now, draws everything, moves the
angle on a little, and then asks to be called again. That loop, draw
and ask again, is the *animation loop*, and every game and every
animated chart on the web is built round one.

One line does something CSS did for us last time. The ball has to go
behind the sun for half of every turn, and a canvas has no idea what is
in front of what. It draws whatever it is told, in the order it is
told. So `frame` sorts the two bodies by depth, farthest first, and the
nearer one is painted over the farther one. Sorting a scene by depth
and painting from the back is called the *painter's algorithm*, after
the way a painter lays down a background before the figures in front
of it.

## The cube again

The turning cube from [Turning a Cube](tutorial:turning-a-cube), with
the rotation matrix applied to each corner by `turn`, which is the
matrix multiplication from that tutorial written for one point at a
time.

```html site
id: cube-canvas-html
site: cube-canvas
<canvas id="screen" width="320" height="240"></canvas>
```

```css site
id: cube-canvas-css
site: cube-canvas
canvas {
  background: #1b1f2a;
}
```

```js site
id: cube-canvas-js
site: cube-canvas
const canvas = document.getElementById("screen");
const pen = canvas.getContext("2d");
const glass = 200;
const middleX = canvas.width / 2;
const middleY = canvas.height / 2;

const corners = [
  [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
  [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
];
const edges = [
  [0, 1], [1, 2], [2, 3], [3, 0],
  [4, 5], [5, 6], [6, 7], [7, 4],
  [0, 4], [1, 5], [2, 6], [3, 7],
];

function rotateY(angle) {
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  return [[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]];
}

function turn(matrix, [x, y, z]) {
  return matrix.map(([a, b, c]) => a * x + b * y + c * z);
}

function project([x, y, z]) {
  const depth = z + 5;   // push the cube five units out in front
  return [middleX + glass * x / depth, middleY + glass * y / depth];
}

let angle = 0;

function frame() {
  pen.fillStyle = "#1b1f2a";
  pen.fillRect(0, 0, canvas.width, canvas.height);

  const turning = rotateY(angle);
  const onScreen = corners.map((corner) => project(turn(turning, corner)));

  pen.strokeStyle = "white";
  pen.lineWidth = 2;
  for (const [start, end] of edges) {
    pen.beginPath();
    pen.moveTo(onScreen[start][0], onScreen[start][1]);
    pen.lineTo(onScreen[end][0], onScreen[end][1]);
    pen.stroke();
  }

  angle = angle + 0.01;
  requestAnimationFrame(frame);
}

frame();
```

`turn` takes a row of the matrix at a time and dots it with the point,
which is exactly what `multiply` did with a row and a column. Then the
same `project`, with the cube pushed five units out first, and twelve
`moveTo` and `lineTo` pairs for the twelve edges.

## Your turn

Let's try changing `angle + 0.02` in the first editor to `angle + 0.05`
and pressing Run again, to see the ball go faster. Then try a second
ball, on a smaller orbit, going the other way: a negative angle does
that. Remember to add it to the list that gets sorted, or it will not
know to go behind anything. In the second editor, try a `rotateX`
function alongside `rotateY`, with `x` left alone this time, and apply
both turns to each corner. Which order gives a cube that spins on a
tilted turntable, and which gives one that tumbles?

## What you have now

The perspective divide written out by hand, running sixty times a
second.

A `<canvas>` is a rectangle JavaScript draws on, and
`getContext("2d")` gives the pen that draws on it. The animation
loop draws one frame, then calls `requestAnimationFrame` to ask for
the next. The painter's algorithm sorts what is to be drawn by depth
and paints from the back forwards, so nearer things cover farther
ones.
