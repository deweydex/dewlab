---
title: "A turning cube drawn on a canvas — Practice"
practice_for: a-cube-on-a-canvas
year: "2026-2027"
version: 2026.09.22.1
---

# A turning cube drawn on a canvas — Practice

On this page we practise drawing a shape as corners and edges, turning
it with a rotation matrix, and projecting it onto a canvas. There are
two kinds of problem:

- a broken page, where we find the mistake and fix it
- a small change to build from a description

Each problem has a folded answer. Some also have a hint, folded before
the answer. Remember to press **Run** after every change.

## Fix the broken page

**1.** Press Run. The cube turns, but one of its edges is missing.

```html site
id: canvas-cube-practice-edge-html
site: canvas-cube-practice-edge
<canvas id="screen" width="320" height="240"></canvas>
```

```css site
id: canvas-cube-practice-edge-css
site: canvas-cube-practice-edge
canvas {
  background: #1b1f2a;
}
```

```js site
id: canvas-cube-practice-edge-js
site: canvas-cube-practice-edge
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
  [0, 1], [1, 2], [2, 3], [3, 3],
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


Which edge is missing? Find the mistake, and fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the lines on the canvas. How many are there? How many should
   there be?
2. Each edge is a pair of corner numbers. Read the first four pairs in
   `edges`. They should go round a square: from one corner to the next,
   and back to the start.
3. Is there a pair that goes from a corner to itself?

**Think about:** what does a line from a point to the same point look
like?

</details>

<details class="dl-answer"><summary>answer</summary>

```js
const edges = [
  [0, 1], [1, 2], [2, 3], [3, 0],
  [4, 5], [5, 6], [6, 7], [7, 4],
  [0, 4], [1, 5], [2, 6], [3, 7],
];
```

The fourth pair was `[3, 3]`, a line from corner `3` to corner `3`. A
line from a point to itself has no length, so nothing was drawn. The
edge from corner `3` back to corner `0`, which closes the first square,
was missing. With `[3, 0]`, all twelve edges are drawn.

</details>

**2.** Press Run. There is no cube, only long lines that cross the
canvas and jump about.

```html site
id: canvas-cube-practice-depth-html
site: canvas-cube-practice-depth
<canvas id="screen" width="320" height="240"></canvas>
```

```css site
id: canvas-cube-practice-depth-css
site: canvas-cube-practice-depth
canvas {
  background: #1b1f2a;
}
```

```js site
id: canvas-cube-practice-depth-js
site: canvas-cube-practice-depth
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
  return [middleX + glass * x / z, middleY + glass * y / z];
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


Compare `project` with the tutorial page. What is missing? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The corners have `z` values of `-1` and `1`. As the cube turns, `z`
   goes between about `-1.4` and `1.4`.
2. `project` divides by `z`. What happens when `z` is `0`, or very close
   to `0`? What happens when it is below `0`?
3. On the tutorial page, the cube is pushed somewhere before the divide.
   Where?

**Think about:** where is the cube, compared with our eye, if nothing
pushes it away?

</details>

<details class="dl-answer"><summary>answer</summary>

```js
function project([x, y, z]) {
  const depth = z + 5;   // push the cube five units out in front
  return [middleX + glass * x / depth, middleY + glass * y / depth];
}
```

Without the push, the middle of the cube is at our eye. Some corners
have a depth close to `0`, and dividing by a tiny number gives a huge
answer, far off the canvas. Other corners have a depth below `0`, which
means behind our eye, and the divide flips them to the other side. So
the lines shot off in all directions. `z + 5` puts every corner between
about `3.6` and `6.4` units in front of us, so every divide is safe.

</details>

## Make this

**3.** Draw a white dot, with a radius of `4` pixels, on every corner of
the cube, on top of the edges.

```html site
id: canvas-cube-practice-dots-html
site: canvas-cube-practice-dots
<canvas id="screen" width="320" height="240"></canvas>
```

```css site
id: canvas-cube-practice-dots-css
site: canvas-cube-practice-dots
canvas {
  background: #1b1f2a;
}
```

```js site
id: canvas-cube-practice-dots-js
site: canvas-cube-practice-dots
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


<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `onScreen` already holds the eight corners, projected onto the
   canvas. Each one is `[x, y]`.
2. The dots go on top of the edges, so draw them after the loop that
   draws the edges.
3. On [Drawing frames with
   JavaScript](tutorial:drawing-frames-with-javascript), `drawBall`
   drew a circle with `beginPath`, `arc` and `fill`.

**Think about:** why must the dots be drawn after the edges, and not
before?

**Try this next:** make the dots on near corners bigger than the dots
on far corners. `project` would need to return the depth as well.

</details>

<details class="dl-answer"><summary>answer</summary>

Add this loop in `frame`, after the loop that draws the edges, and
before `angle` changes:

```js
  pen.fillStyle = "white";
  for (const [x, y] of onScreen) {
    pen.beginPath();
    pen.arc(x, y, 4, 0, 2 * Math.PI);
    pen.fill();
  }
```

`onScreen` has the eight projected corners, so the loop runs eight
times. `arc` describes a circle of radius `4` round each corner, and
`fill` colours it in. The dots are drawn after the edges, so they cover
the ends of the lines.

</details>

**4.** Change the cube into a pyramid with a square base. The base is
the bottom face of the cube, and the tip is straight above the middle
of the base, at the height of the cube's top. It should turn the same
way the cube does.

```html site
id: canvas-cube-practice-pyramid-html
site: canvas-cube-practice-pyramid
<canvas id="screen" width="320" height="240"></canvas>
```

```css site
id: canvas-cube-practice-pyramid-css
site: canvas-cube-practice-pyramid
canvas {
  background: #1b1f2a;
}
```

```js site
id: canvas-cube-practice-pyramid-js
site: canvas-cube-practice-pyramid
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


<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A canvas counts `y` downwards, so the bottom of the cube is at
   `y = 1`, and the top is at `y = -1`.
2. The base has four corners, all with `y = 1`. The tip is one more
   corner. What are its `x`, `y` and `z`?
3. The base needs four edges, round a square. The sides need four more,
   one from each corner of the base to the tip.

**Think about:** the rest of the code never says "cube". Why does it
still work for a pyramid?

**Try this next:** make a pyramid with a triangle for its base.

</details>

<details class="dl-answer"><summary>answer</summary>

```js
const corners = [
  [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1],
  [0, -1, 0],
];
const edges = [
  [0, 1], [1, 2], [2, 3], [3, 0],
  [0, 4], [1, 4], [2, 4], [3, 4],
];
```

Corners `0` to `3` are the base, and corner `4` is the tip, above the
middle of the base. The first four edges go round the base, and the
last four go from each corner of the base up to the tip. Nothing else
changes. `frame` turns, projects and joins whatever corners and edges
it is given.

</details>

**5.** Make the cube spin on a tilted turntable. It should spin about
its own vertical axis, the way it does now, but be tipped towards us
by a fixed amount, so that we look down on its top all the time.

```html site
id: canvas-cube-practice-tilt-html
site: canvas-cube-practice-tilt
<canvas id="screen" width="320" height="240"></canvas>
```

```css site
id: canvas-cube-practice-tilt-css
site: canvas-cube-practice-tilt
canvas {
  background: #1b1f2a;
}
```

```js site
id: canvas-cube-practice-tilt-js
site: canvas-cube-practice-tilt
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


<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write a `rotateX` function beside `rotateY`. It leaves `x` alone:
   its rows are `[1, 0, 0]`, `[0, cos, -sin]` and `[0, sin, cos]`.
2. The tilt is a fixed angle, such as `0.4` radians, so it does not use
   `angle`.
3. Each corner needs two turns. The one written nearest the corner
   happens first. Which should happen first: the spin, or the tilt?

**Think about:** if the tilt happened first, what would the spin turn
round: the cube's own axis, or the axis of the page?

</details>

<details class="dl-answer"><summary>answer</summary>

Add a `rotateX` function after `rotateY`:

```js
function rotateX(angle) {
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  return [[1, 0, 0], [0, cos, -sin], [0, sin, cos]];
}
```

Then, in `frame`, make the tilt and use both turns:

```js
  const turning = rotateY(angle);
  const tilt = rotateX(0.4);
  const onScreen = corners.map((corner) => project(turn(tilt, turn(turning, corner))));
```

`turn(turning, corner)` is nearest the corner, so it happens first. The
cube spins about its own vertical axis. Then `turn(tilt, ...)` tips the
spinning cube towards us, so we look down on its top. With the two the
other way round, the cube is tipped first, and then spun about the
vertical axis of the page. Then it tumbles, and shows its top and its
bottom in turn.

</details>
