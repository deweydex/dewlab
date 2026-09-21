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

On the last two pages the browser drew every frame for you, from the
few key frames you wrote down. This page does the opposite. You draw
every frame yourself, in JavaScript, and the browser only tells you
when it is time for the next one. It is the ball in orbit from [A
Point on the Screen](tutorial:a-point-on-the-screen#a-ball-in-orbit),
written in a different language, and it is the first JavaScript on
this course.

This editor has a third pane. HTML and CSS update the preview as you
type, the way they have all along, but JavaScript only runs when you
press **Run** in its pane, or Ctrl+Enter inside it. Let's press it
now.

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

**The canvas.** A `<canvas>` is a blank rectangle of pixels that
JavaScript can draw on. Nothing else on this course has needed one,
because HTML and CSS describe a page and the browser draws it. A
canvas is for when you want to do the drawing yourself.
`getContext("2d")` gives you the pen that does it:

- `fillRect` draws a rectangle;
- `arc` draws a circle, or part of one;
- `fill` colours in whatever shape was just described.

**The divide, in pixels.** `project` is the perspective divide, with
two changes to fit a canvas. The first change: after dividing by $z$,
the result is multiplied by `glass`, the distance to the screen in
pixels, because a canvas counts in pixels rather than units. The
second: the result is added to the middle of the canvas, because a
canvas puts $(0, 0)$ in its top-left corner, not at the centre. A
canvas also counts $y$ downwards, so the $0.2$ in the sun and the ball
puts them a little below eye level, which is why you look slightly
down on the orbit. The ball's radius is scaled by `glass / z`, the
same divide again, so it shrinks as it goes away. Let's check one
number: the sun is at depth 4, so its radius of $0.5$ becomes
$0.5 \times 200 / 4 = 25$ pixels.

**The loop.** `requestAnimationFrame(frame)` is the line that makes it
move. It asks the browser to call `frame` once, just before it next
paints the screen, which is usually sixty times a second. Each time
`frame` runs it does the same four things:

1. Clear the canvas, by painting a dark rectangle over everything.
2. Work out where the ball is now, from `angle`.
3. Draw the sun and the ball.
4. Add a little to `angle`, and ask to be called again.

That loop, draw and ask again, is the ***animation loop***, and every
game and every animated chart on the web is built round one. It is
`FuncAnimation` from the Computational Methods course, written out by
hand: there, matplotlib called `draw_step` once per frame; here, the
browser calls `frame`. Adding `0.02` to the angle each time, at sixty
frames a second, is $1.2$ radians a second, so one full turn takes
about five seconds.

**Front and back.** One line does a job that CSS did for us on the
last two pages. The ball has to go behind the sun for half of every
turn, and a canvas has no idea what is in front of what. It draws
whatever it is told, in the order it is told. So `frame` sorts the two
bodies by depth, farthest first, and the nearer one is painted over
the farther one. Sorting a scene by depth and painting from the back
is called the ***painter's algorithm***, after the way a painter lays
down a background before the figures in front of it.

## The cube again

Here is the turning cube from [Turning a Cube](tutorial:turning-a-cube).
`turn` applies the rotation matrix to one corner at a time. It is the
matrix multiplication from that tutorial, written for a single point.

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

`turn` takes one row of the matrix at a time and works out its dot
product with the point. That is exactly what `multiply` did with a row
and a column. Then the same `project`, with the cube pushed five units
out first, and twelve `moveTo` and `lineTo` pairs for the twelve
edges. Every frame:

1. Build the rotation matrix for the current `angle`.
2. Turn all eight corners with it, and project each one.
3. Draw the twelve edges between the projected corners.
4. Add a little to `angle`, and ask for the next frame.

## Your turn

Some things to try, each one in its own run:

- In the first editor, change `angle + 0.02` to `angle + 0.05` and
  press Run again. The ball goes faster. How long does one turn take
  now?
- Add a second ball on a smaller orbit, going the other way: a
  negative angle does that. Remember to add it to the list that gets
  sorted, or it will not know to go behind anything.
- In the second editor, write a `rotateX` function alongside
  `rotateY`, with `x` left alone this time, and apply both turns to
  each corner. Which order gives a cube that spins on a tilted
  turntable, and which gives one that tumbles?

## What you have now

The perspective divide written out by hand, running sixty times a
second.

A `<canvas>` is a rectangle JavaScript draws on, and
`getContext("2d")` gives the pen that draws on it. The animation loop
draws one frame, then calls `requestAnimationFrame` to ask for the
next. The painter's algorithm sorts what is to be drawn by depth and
paints from the back forwards, so nearer things cover farther ones.
