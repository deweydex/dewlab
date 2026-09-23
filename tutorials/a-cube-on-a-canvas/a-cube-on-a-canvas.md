---
title: "A turning cube drawn on a canvas"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    touches: [WA-LO2]
  now-add-your-own:
    touches: [WA-LO2]
---

# A turning cube drawn on a canvas

On [Drawing frames with
JavaScript](tutorial:drawing-frames-with-javascript), we drew a sun and
a ball on a canvas, and moved them with an animation loop. Can the same
loop draw a solid shape? On this page we:

- store a cube as a list of corners and a list of edges
- turn every corner a little each frame
- draw the twelve edges as lines between the corners

This is the turning cube from [The rotation matrix: turning a cube in 3D](tutorial:turning-a-cube),
on the Computational Methods course, written in JavaScript. You do not
need that page to follow this one. The explanation below has
everything the code uses.

## Let's try it

Here is a second canvas, and the JavaScript that draws a cube on it.

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

1. Press **Run**. How many lines make up the cube? How many corners do
   they meet at?
2. Change `angle + 0.01` to `angle + 0.03`, and press Run again. What
   changes?
3. Put it back. In `project`, change `z + 5` to `z + 3`, and press Run.
   How does the cube look now? Then try `z + 20`.
4. Put it back to `z + 5`. In the `edges` list, delete the first pair,
   `[0, 1],`, and press Run. What is missing?

Put the pair back before you read on.

## Why does this happen?

Now we can explain what we saw.

### Corners and edges

`corners` is a list of eight points, one for each corner of the cube.
Each point is three numbers, `x`, `y` and `z`, and each number is `-1`
or `1`. So the cube is two units wide, with its centre at `0, 0, 0`.
JavaScript counts the items in a list from `0`, so the corners are
numbers `0` to `7`.

`edges` is a list of twelve pairs of corner numbers. Each pair is one
edge: a line from one corner to another.

- The first four edges join the four corners with `z` at `-1`, in a
  square.
- The next four join the four corners with `z` at `1`, in a second
  square.
- The last four join each corner of the first square to the matching
  corner of the second.

In step 4, we took away `[0, 1]`, so the line from corner `0` to corner
`1` was never drawn. A drawing of a shape that shows only its edges is
called a *wireframe*.

### Turning a corner

`rotateY(angle)` builds a *rotation matrix*. A matrix is a grid of
numbers, and this one has three rows of three. It holds everything
needed to turn a point about the vertical axis by `angle`.

`turn` applies the matrix to one point. For each row, it multiplies the
row's three numbers by the point's `x`, `y` and `z`, and adds the
results. That gives one new coordinate. With the numbers of
`rotateY`, the three rows give:

| Row | New coordinate |
|---|---|
| `[cos, 0, sin]` | new `x` = `cos × x + sin × z` |
| `[0, 1, 0]` | new `y` = `y`, the same as before |
| `[-sin, 0, cos]` | new `z` = `-sin × x + cos × z` |

`y` never changes, so every corner goes round the vertical axis at its
own height. Multiplying a row by a point in this way, and adding up, is
called a *dot product*. It is what `multiply` did with a row and a
column on [The rotation matrix: turning a cube in 3D](tutorial:turning-a-cube).

### Drawing the edges

`project` is the same perspective divide as on the orbit canvas, with
one change. It adds `5` to every depth first, which pushes the cube
five units out in front of our eye. Without that push, some corners
would have a depth of `0` or less, and the divide would go wrong.

In step 3, `z + 3` brought the cube closer. The near edges grew much
bigger than the far ones, so the cube looked strongly in perspective.
With `z + 20`, the cube was far away. It was drawn small, and its near
and far edges were almost the same size.

Then the pen draws each edge. `moveTo` puts the pen down at one corner
without drawing, `lineTo` describes a line to the other corner, and
`stroke` draws that line in `strokeStyle`, `lineWidth` pixels wide.

Every frame does the same four things:

1. Build the rotation matrix for the current `angle`.
2. Turn all eight corners with it, and project each one.
3. Draw the twelve edges between the projected corners.
4. Add a little to `angle`, and ask for the next frame.

In step 2, adding `0.03` in place of `0.01` made the cube turn three
times as fast.

## Now add your own

A cube that only spins about the vertical axis never shows us its top.
Let's tilt it as well.

1. Under the `rotateY` function, write a `rotateX` function. It is the
   same shape, but it leaves `x` alone, and turns `y` and `z`:
   `return [[1, 0, 0], [0, cos, -sin], [0, sin, cos]];`
2. In `frame`, under the line that makes `turning`, add
   `const tilt = rotateX(0.4);`.
3. Change `turn(turning, corner)` to `turn(tilt, turn(turning, corner))`,
   and press Run.
4. Now swap the two: `turn(turning, turn(tilt, corner))`, and press Run
   again.

Which order gives a cube that spins on a tilted turntable, and which
gives one that tumbles?

## What we have now

We can now store a shape as corners and edges, turn it with a matrix,
and draw it as lines on a canvas.

| Word | Meaning | Example |
|---|---|---|
| *wireframe* | A drawing of a shape that shows only its edges | the cube on this page |
| *rotation matrix* | A grid of numbers that turns a point about an axis | `rotateY(angle)` |
| *dot product* | Multiply two lists of numbers item by item, and add up the results | `a * x + b * y + c * z` in `turn` |
| `moveTo()` and `lineTo()` | Put the pen down at a point, then describe a line from there to another point | `pen.moveTo(10, 10); pen.lineTo(50, 50);` |
| `stroke()` | Draws the line just described | `pen.stroke();` |
