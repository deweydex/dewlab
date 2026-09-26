---
title: "A 3D cube in CSS"
year: "2026-2027"
version: 2026.09.21.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
    touches: [WA-LO2]
  now-add-your-own:
    touches: [WA-LO9]
---

# A 3D cube in CSS

On [An orbit in pure CSS](tutorial:an-orbit-in-css), one flat ball
went round in depth. Can flat squares make a solid shape? Six of them
can make a cube, if each one is pushed out and turned to face a
different way. The whole thing is HTML and CSS: six `div`s, six
transforms and one `@keyframes` rule. On this page we:

- build a cube that tumbles on its own
- see why the order of two transforms matters
- make the cube look solid

## Let's try it

Here is a cube made of six squares, each with its name written on it.

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

1. Watch the cube for a while. Can you find all six names? Can you read
   the names on the far side of the cube too?
2. Delete the whole `.top` line from the CSS. Where does the top face
   go now?
3. Put that line back. In the `.right` line, swap the two transforms,
   so that it says `translateZ(50px) rotateY(90deg)`. Where is the
   right face now?

Put the `.right` line back as it was before you read on.

## Why does this happen?

Now we can explain what we saw.

### Where the faces start

All six faces start in the same place. `position: absolute` with no
`top` or `left` leaves each one at the top-left corner of `.cube`. Each
face is 100 pixels square, the same size as `.cube`, so they sit
exactly on top of each other, like six playing cards in a pile. Each
face has one transform, which moves it out of the pile.

In step 2, the top face lost its transform. So it went back to the
pile, in the middle of the cube, facing the same way as the front face
before its push.

### Push, then turn

`.front` has `translateZ(50px)`. It is pushed 50 pixels towards us,
half the cube's width. Every other face has a turn, and then that same
push. The order of the list, the *transform order*, is worth reading
slowly. The browser applies a list of transforms from the right-hand
end. So `rotateY(90deg) translateZ(50px)` means:

1. Push the face 50 pixels towards us.
2. Then turn the pushed-out face a quarter turn about the vertical axis,
   around the middle of the cube.

A face that was in front, facing us, ends up on the right, facing
right. Here is the same thing seen from above:

![Three drawings of the cube seen from above, as a dashed square, with your eye below each one. In the first, labelled "Where it starts", one face lies across the middle of the square. In the second, labelled translateZ(50px), an arrow shows the face pushed down to the front edge of the square, towards you. In the third, labelled rotateY(90deg), a curved arrow shows the face swung a quarter turn about the middle of the square, so it now lies along the right-hand edge.](push-then-turn.svg)

In step 3, the list was the other way round. The browser turned the
face first, in the middle of the cube, so it faced right. Then it
pushed the face 50 pixels towards us, still facing right. So the right
face ended up at the front, side-on to us, as a thin line across the
front face.

Here is where all six faces go:

- `.front`: no turn, pushed towards us
- `.back`: a half turn, `rotateY(180deg)`, so it ends up behind,
  facing away
- `.right` and `.left`: a quarter turn each way about the vertical axis
- `.top` and `.bottom`: a quarter turn each way about the horizontal
  axis, with `rotateX()`

`rotateX()` turns an element about a horizontal axis, so it tips the
element's top towards us or away from us. Six pushes and five turns
make one cube.

### Keeping the shape

`transform-style: preserve-3d` on `.cube` keeps the six faces where
the transforms put them, when `.cube` itself turns. Without it, the
browser would flatten them into one square before it tumbled the cube.

`perspective: 600px` on the stage puts our eye 600 pixels from the
screen, as on the orbit page. The nearer faces are drawn bigger than
the far ones, so the cube looks solid, and not like a flat drawing of
one. `display: grid` and `place-items: center` on the stage put the
cube in the middle of the stage.

### The tumble

`tumble` is a `@keyframes` rule with two frames, a start and an end.
The browser fills in every frame between them. The end is
`rotateX(360deg) rotateY(720deg)`: one full turn about the horizontal
axis and two about the vertical axis, in the same twelve seconds. The
faces are half see-through, so the far faces show through the near
ones. That is why, in step 1, we could read the far names too, back to
front, and watch the whole shape at once.

## Now add your own

The editor above is ours to change. Try each of these on its own.

1. Add `backface-visibility: hidden;` to the `.face` rule. The back of
   a face is the side we see when it has turned away from us. What
   happens to the faces that are turned away?
2. Give each face its own background colour, like a child's building
   block. With `backface-visibility` still on, it is easier to tell
   which face is which.
3. Change the `to` line of `tumble` to
   `to { transform: rotateX(0deg) rotateY(360deg); }`. Now the cube
   spins on a turntable, and does not tumble. Which faces do we never
   see properly now?

Does your cube look solid now? Can you tell which face is on top?

## What we have now

We can now build a solid shape out of flat squares, and we know why the
order of the transforms decides where each square goes.

| Word | Meaning | Example |
|---|---|---|
| `rotateX()` | Turns an element about a horizontal axis, tipping its top towards us or away from us | `transform: rotateX(90deg);` |
| *transform order* | A list of transforms is applied from the right-hand end. In `rotateY(90deg) translateZ(50px)`, the push happens first and the turn second. | `rotateY(90deg) translateZ(50px)` |
| `backface-visibility: hidden` | Stops an element being drawn when its back is towards us | `backface-visibility: hidden;` |

## Where to read more

CrashCourse (2017). *3D Graphics: Crash Course Computer Science #27.*
<https://www.youtube.com/watch?v=TEAtmCYYKZA>. A game does the same work as
the browser, for a whole world. It turns every corner, then flattens it
onto the screen. Twelve minutes.
