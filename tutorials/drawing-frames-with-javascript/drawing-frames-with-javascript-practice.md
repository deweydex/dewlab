---
title: "Drawing frames with JavaScript — Practice"
practice_for: drawing-frames-with-javascript
year: "2026-2027"
version: 2026.09.22.1
---

# Drawing frames with JavaScript — Practice

On this page we practise drawing on a canvas with an animation loop:
clearing, drawing, moving on a little, and asking for the next frame,
with the far things drawn first. There are two kinds of problem:

- a broken page, where we find the mistake and fix it
- a small change to build from a description

Each problem has a folded answer. Some also have a hint, folded before
the answer. Remember that the JavaScript runs only when we press
**Run**, so press it after every change.

## Fix the broken page

**1.** Press Run. The sun and the ball are drawn, but the ball never
moves.

```html site
id: frames-practice-still-html
site: frames-practice-still
<canvas id="screen" width="320" height="200"></canvas>
```

```css site
id: frames-practice-still-css
site: frames-practice-still
canvas {
  background: #1b1f2a;
}
```

```js site
id: frames-practice-still-js
site: frames-practice-still
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
}

frame();
```


`angle` goes up by `0.02` at the end of `frame`. So why does the ball
stay still? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. How many times does `frame` run? Look for every line that calls it.
2. The last line of the code calls `frame()` once. What makes it run a
   second time, and a third?
3. Compare the end of `frame` with the tutorial page.

**Think about:** the four things every frame of an animation loop does.
Which one is missing?

**Try this next:** what would happen if `requestAnimationFrame(frame)`
were the first line inside `frame`, and not the last?

</details>

<details class="dl-answer"><summary>answer</summary>

Add `requestAnimationFrame(frame);` as the last line of `frame`:

```js
  angle = angle + 0.02;
  requestAnimationFrame(frame);
}
```

`frame` ran once, from the last line of the code. It drew one frame,
added `0.02` to `angle`, and stopped. Nothing asked the browser to call
it again, so the canvas kept that first picture. With
`requestAnimationFrame(frame)` at the end, every frame asks for the
next one, and that is the loop.

</details>

**2.** Press Run, and watch the ball for a full turn. When it passes
the back of its circle, it is drawn on top of the sun. When it passes
the front, it disappears behind the sun. Both are the wrong way round.

```html site
id: frames-practice-sort-html
site: frames-practice-sort
<canvas id="screen" width="320" height="200"></canvas>
```

```css site
id: frames-practice-sort-css
site: frames-practice-sort
canvas {
  background: #1b1f2a;
}
```

```js site
id: frames-practice-sort-js
site: frames-practice-sort
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
  const farthestFirst = [sun, ball].sort((a, b) => a.z - b.z);
  for (const body of farthestFirst) {
    if (body === sun) drawBall(body, 0.5, "#f5c542");
    else drawBall(body, 0.2, "white");
  }

  angle = angle + 0.02;
  requestAnimationFrame(frame);
}

frame();
```


Fix it, so that the ball passes behind the sun at the back of its
circle, and in front of the sun at the front.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. When two things overlap on a canvas, which one covers the other: the
   one drawn first, or the one drawn last?
2. The code sorts the sun and the ball before it draws them. Which one
   comes first in the sorted list?
3. `sort` puts `a` before `b` when the function gives a number below
   `0`. With `a.z - b.z`, which comes first: the smaller depth, or the
   larger?

**Think about:** the painter's algorithm draws from the back forwards.
Is the back the smaller depth, or the larger?

</details>

<details class="dl-answer"><summary>answer</summary>

```js
  const farthestFirst = [sun, ball].sort((a, b) => b.z - a.z);
```

`a.z - b.z` sorts the smaller depth first, so the nearer body was drawn
first, and the farther one was drawn over it. When the ball was in
front of the sun, the sun covered it. When the ball was behind the
sun, the ball covered the sun. `b.z - a.z` sorts the larger
depth first. The farther body is drawn first, and the nearer one covers
it, which is the painter's algorithm.

</details>

**3.** Press Run. The ball leaves a thick white smear round its path,
and the smear never goes away.

```html site
id: frames-practice-smear-html
site: frames-practice-smear
<canvas id="screen" width="320" height="200"></canvas>
```

```css site
id: frames-practice-smear-css
site: frames-practice-smear
canvas {
  background: #1b1f2a;
}
```

```js site
id: frames-practice-smear-js
site: frames-practice-smear
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


What is missing from the start of `frame`? Fix it.

<details class="dl-answer"><summary>answer</summary>

Add these two lines as the first lines of `frame`:

```js
function frame() {
  pen.fillStyle = "#1b1f2a";
  pen.fillRect(0, 0, canvas.width, canvas.height);
```

A canvas keeps everything drawn on it until something is drawn over it.
Without the dark rectangle at the start of each frame, every ball ever
drawn stayed on the canvas, and together they made the smear. The first
step of every frame of an animation loop is to clear the canvas.

</details>

## Make this

**4.** Change this orbit so that the ball goes round exactly once every
ten seconds, on a 60 Hz screen, where `frame` runs sixty times a second.

```html site
id: frames-practice-slow-html
site: frames-practice-slow
<canvas id="screen" width="320" height="200"></canvas>
```

```css site
id: frames-practice-slow-css
site: frames-practice-slow
canvas {
  background: #1b1f2a;
}
```

```js site
id: frames-practice-slow-js
site: frames-practice-slow
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


How much should `frame` add to `angle` each time? Work it out before
you change the code.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A full turn is `2π` radians. In JavaScript, that is `2 * Math.PI`.
2. How many frames are there in ten seconds, at sixty a second?
3. Share one full turn out between that many frames.

**Think about:** on a 120 Hz screen, `frame` runs twice as often. How
long would one turn take there?

</details>

<details class="dl-answer"><summary>answer</summary>

```js
  angle = angle + 2 * Math.PI / 600;
```

Ten seconds at sixty frames a second is `600` frames. One full turn is
`2π` radians, about `6.28`. So each frame adds `2π / 600`, about
`0.0105`. After `600` frames, the ball has gone round once. On a 120 Hz
screen the same code would take five seconds for a turn.

</details>

**5.** Give the ball a moon. The moon is a small grey ball that circles
the ball, the way the ball circles the sun:

- it goes round the ball at a distance of `0.4`
- it goes round three times as fast as the ball goes round the sun
- its radius is `0.08`, and its colour is `"#9aa4b2"`
- it passes behind the ball and in front of it, and behind the sun and
  in front of it, at the right times

```html site
id: frames-practice-moon-html
site: frames-practice-moon
<canvas id="screen" width="320" height="200"></canvas>
```

```css site
id: frames-practice-moon-css
site: frames-practice-moon
canvas {
  background: #1b1f2a;
}
```

```js site
id: frames-practice-moon-js
site: frames-practice-moon
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


<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The ball's position is the sun's centre, plus a circle. The moon's
   position is the ball's position, plus a smaller circle.
2. So after the line that makes `ball`, make `moon` with
   `ball.x + 0.4 * Math.cos(...)` across and `ball.z + 0.4 * Math.sin(...)`
   in depth. What angle goes inside, for three times as fast?
3. To go behind and in front at the right times, the moon must be in the
   list that gets sorted.
4. The drawing loop draws everything that is not the sun as a white
   ball. How can it tell the moon apart?

**Think about:** why does one sort by depth handle all three bodies,
with no extra rules for which is in front of which?

**Try this next:** give the sun a second planet, with a moon of its
own.

</details>

<details class="dl-answer"><summary>answer</summary>

Make the moon after the ball, add it to the sorted list, and give it
its own branch in the drawing loop:

```js
  const sun = { x: 0, y: 0.2, z: 4 };
  const ball = { x: 1.5 * Math.cos(angle), y: 0.2, z: 4 + 1.5 * Math.sin(angle) };
  const moon = {
    x: ball.x + 0.4 * Math.cos(3 * angle),
    y: 0.2,
    z: ball.z + 0.4 * Math.sin(3 * angle),
  };

  // Draw the farther one first, so the nearer one covers it.
  const farthestFirst = [sun, ball, moon].sort((a, b) => b.z - a.z);
  for (const body of farthestFirst) {
    if (body === sun) drawBall(body, 0.5, "#f5c542");
    else if (body === moon) drawBall(body, 0.08, "#9aa4b2");
    else drawBall(body, 0.2, "white");
  }
```

`3 * angle` goes round three times for every one turn of `angle`. The
moon's position starts from the ball's, so it goes wherever the ball
goes. The sort puts all three bodies in order of depth in every frame,
so whichever is farthest is drawn first. That one rule decides every
case: moon and ball, moon and sun, ball and sun.

</details>
