---
title: "A cube in CSS"
year: "2026-2027"
version: 2026.09.21.1
covers:
  why-this-happens:
    covers: [WA-LO9]
    touches: [WA-LO2]
  your-turn:
    touches: [WA-LO9]
---

# A cube in CSS

Six squares, each pushed out and turned to face a different way, make
a cube. The cube tumbles on its own, and the whole thing is HTML and
CSS. Six `div`s, six transforms, one `@keyframes` rule. The same
trick, with more faces, is how a product spins round on a shop's
website.

```html site
id: cube-html
site: cube
<div class="stage">
  <div class="cube">
    <div class="face front">front</div>
    <div class="face back">back</div>
    <div class="face right">right</div>
    <div class="face left">left</div>
    <div class="face top">top</div>
    <div class="face bottom">bottom</div>
  </div>
</div>
```

```css site
id: cube-css
site: cube
.stage {
  width: 320px;
  height: 240px;
  background: #1b1f2a;
  perspective: 600px;
  display: grid;
  place-items: center;
}
.cube {
  width: 100px;
  height: 100px;
  position: relative;
  transform-style: preserve-3d;
  animation: tumble 12s linear infinite;
}
.face {
  position: absolute;
  width: 100px;
  height: 100px;
  display: grid;
  place-items: center;
  font: bold 18px sans-serif;
  color: white;
  border: 2px solid white;
  background: rgba(70, 130, 220, 0.55);
}
.front  { transform: translateZ(50px); }
.back   { transform: rotateY(180deg) translateZ(50px); }
.right  { transform: rotateY(90deg) translateZ(50px); }
.left   { transform: rotateY(-90deg) translateZ(50px); }
.top    { transform: rotateX(90deg) translateZ(50px); }
.bottom { transform: rotateX(-90deg) translateZ(50px); }
@keyframes tumble {
  from { transform: rotateX(0deg) rotateY(0deg); }
  to   { transform: rotateX(360deg) rotateY(720deg); }
}
```

## Why this happens

**Where the faces start.** All six faces start in the same place.
`position: absolute` with no `top` or `left` leaves each one at the
top-left corner of `.cube`. They are stacked on top of each other, each
100 pixels square, like six playing cards in a pile. One transform each
is what separates them.

**Push, then turn.** `.front` is `translateZ(50px)`: pushed 50 pixels
towards you, half the cube's width. Every other face is a `rotate`
followed by that same push. The order is worth reading slowly, because
the browser applies a list of transforms from the right-hand end.
`rotateY(90deg) translateZ(50px)` means:

1. Push the face 50 pixels towards you.
2. Then turn the pushed-out face a quarter turn about the vertical
   axis.

A face that was in front and facing you ends up on the right and
facing right. Here is where all six go:

- `.front`: no turn, pushed towards you.
- `.back`: a half turn, `rotateY(180deg)`, so it ends up behind, facing
  away.
- `.right` and `.left`: a quarter turn each way about the vertical
  axis.
- `.top` and `.bottom`: a quarter turn each way about the horizontal
  axis, with `rotateX`.

Six pushes, five turns, one cube. [Two Turns at
Once](tutorial:turning-a-cube#two-turns-at-once) has the same rule
written as matrices: the transform nearest the element acts first.

**Keeping the shape.** `transform-style: preserve-3d` on `.cube` is
what keeps the six faces where the transforms put them when `.cube`
itself turns. Without it the browser would flatten them into one
square before tumbling it. And `perspective: 600px` on the stage is
the sheet of glass from [A Point on the
Screen](tutorial:a-point-on-the-screen#why-dividing-works), 600 pixels
away: the nearer faces are drawn bigger than the far ones, which is
why the cube looks solid rather than like a drawing of one.

**The tumble.** `tumble` is a `@keyframes` rule with two frames, a
start and an end, and the browser fills in every frame between them,
about sixty a second. The end is `rotateX(360deg) rotateY(720deg)`:
once about $x$ and twice about $y$ in the same twelve seconds. The
faces are half transparent, so the back ones show through the front
ones and you can watch the whole shape at once.

## Your turn

Let's try these in the editor, one at a time:

- `backface-visibility: hidden` on `.face`. A face's back is the side
  you see when it has turned away from you, so hiding it makes the
  cube look solid, and the three faces facing away stop being drawn.
- A different background colour on each face, like a child's building
  block. Which face is which is easiest to tell with `backface-visibility`
  still on.
- Change the `to` line of `tumble` to `rotateX(0deg) rotateY(360deg)`,
  so that the cube spins on a turntable instead of tumbling. Which
  faces do you never see now?
- Change `50px` to `30px` in every face, but leave the faces 100 pixels
  wide. What shape do you get, and why?

## What you have now

A solid, turning cube, built from six flat squares.

`rotateX()` turns an element about a horizontal axis, tipping its top
towards you or away from you. A list of transforms is applied from the
right-hand end, so `rotateY(90deg) translateZ(50px)` pushes first and
turns second. `backface-visibility: hidden` stops an element being
drawn when its back is towards you.
