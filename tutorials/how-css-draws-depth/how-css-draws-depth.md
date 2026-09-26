---
title: "How CSS draws 3D: perspective and depth"
year: "2026-2027"
version: 2026.09.22.1
context_for: [an-orbit-in-css, a-cube-in-css, a-ball-that-faces-you, drawing-frames-with-javascript, a-cube-on-a-canvas]
---

# How CSS draws 3D: perspective and depth

On [An orbit in pure CSS](tutorial:an-orbit-in-css), [A 3D cube in CSS](tutorial:a-cube-in-css) and [A ball that keeps facing
you](tutorial:a-ball-that-faces-you), the browser drew depth for us,
with no arithmetic written down. [Drawing frames with
JavaScript](tutorial:drawing-frames-with-javascript) and [A turning cube
drawn on a canvas](tutorial:a-cube-on-a-canvas) wrote the same
arithmetic out by hand. What does the browser work out, and where does
it do it? This page is background reading. You do not need it to finish
those pages, but it can help you see why they work.

On this page we:

- work out how big `perspective` makes a thing look
- move the eye, and give each element an eye of its own
- see the circle, and the list of transforms, as the browser sees them
- find what flattens a 3D scene without warning
- see where depth in CSS turns up on real websites

## The sheet of glass, in numbers

`perspective` is the distance from our eye to the screen. A thing that
`translateZ` pushes towards us is nearer to our eye, so the browser
draws it bigger. A thing pushed away is drawn smaller. How much bigger,
or smaller?

The browser divides the distance to the screen by the distance to the
thing. On the orbit page, `perspective` is `400px`.

| Where the ball is | Distance from our eye | Size on screen |
|---|---|---|
| at the front, `translateZ(100px)` | `400 - 100 = 300px` | `24 × 400 / 300 = 32px` |
| at the sides, depth `0` | `400px` | `24 × 400 / 400 = 24px` |
| at the back, `translateZ(-100px)` | `400 + 100 = 500px` | `24 × 400 / 500 = 19.2px` |

That is the same divide as `project` on the canvas pages. There, `z` is
the distance from our eye, and `glass` is the distance to the screen:
`glass * x / z`. The same division also moves a thing towards the
middle of the stage as it goes away, so far things look closer
together. [Perspective projection: dividing by depth](tutorial:a-point-on-the-screen#why-dividing-works),
on the Computational Methods course, shows why one division does all of
that.

## Where the eye stands

`perspective` sets how far away our eye is. `perspective-origin` sets
where it is, across the element. By default, the eye is in front of the
middle of the element that has the `perspective`. Here are three cards
in a row, each turned by the same `40deg`, with one `perspective` on the
row:

```html site
id: eye-html
site: eye
<div class="row">
  <div class="card">one</div>
  <div class="card">two</div>
  <div class="card">three</div>
</div>
```

```css site
id: eye-css
site: eye
.row {
  display: flex;
  gap: 20px;
  padding: 20px;
  perspective: 400px;
}
.card {
  width: 80px;
  height: 100px;
  display: grid;
  place-items: center;
  background: #2c3e50;
  color: white;
  transform: rotateY(40deg);
}
```

1. Do the three cards look the same? Which one looks widest?
2. Add `perspective-origin: left;` to the `.row` rule. What changes?
3. Take out the `perspective` and `perspective-origin` lines from
   `.row`. Then change the card's transform to
   `transform: perspective(400px) rotateY(40deg);`. Do the cards look
   the same now?

The three cards share one eye, in front of the middle of the row. So we
see each card from a different angle, and they look different. Moving
the eye to the left in step 2 changed every card again. In step 3, the
`perspective()` function gave each card an eye of its own, in front of
its own middle, so all three look the same.

Both ways are useful. One `perspective` on a parent puts all its
children in one shared scene, like the sun and the orbit. `perspective()`
inside a `transform` suits one element on its own, such as a single
card that turns when we point at it.

## The circle, as the browser sees it

On the orbit page, `rotateY()` and `translateZ()` together made a
circle. What does the browser work out? Say the ball is pushed out by
`r`, and `.orbit` has turned by the angle `θ`. Then the ball is at:

- across: `x = r × sin θ`
- depth: `z = r × cos θ`

At `θ = 0`, `sin θ` is `0` and `cos θ` is `1`, so the ball is straight in
front of the sun, at depth `r`. At `θ = 90deg`, it is out at the side,
at depth `0`. The browser does the `sin` and the `cos` for every frame.

[3D animation: a camera and a ball in orbit](tutorial:a-ball-in-orbit#a-ball-in-orbit)
has the same ball, written as `x = r cos θ` and `z = 5 + r sin θ`. It
measures the angle from a different starting place, and pushes the whole
circle five units away from the eye. It is still the same circle.

## A list of transforms is one matrix

The browser turns the whole list in a `transform` into one grid of
sixteen numbers, a four-by-four matrix. We can see it in the inspector.
Select `.orbit` on the orbit page, open the **Computed** tab, and find
`transform`. It says `matrix3d(` followed by sixteen numbers, and the
numbers change as the orbit turns.

The order of a list matters for the same reason that the order of
matrix multiplication matters. The section "Two Turns at Once" in [The rotation matrix: turning a cube in 3D](tutorial:turning-a-cube#two-turns-at-once), on the Computational
Methods course, has the same rule written as matrices: the matrix
nearest the points acts first. In CSS, the transform at the
right-hand end of the list acts first. [Homogeneous coordinates and the projection matrix](tutorial:the-fourth-number) explains why the grid needs four
rows, and not three: a push like `translateZ` cannot be written with
three.

## What flattens a 3D scene

`transform-style: preserve-3d` keeps an element's children at their
real depth. Some other properties quietly turn it off. When an element
has one of these, the browser flattens its children onto it, even with
`preserve-3d`:

- `overflow: hidden`
- an `opacity` below `1`
- a `filter`

So if a 3D scene goes flat after a change, look for one of these on the
element that holds it. For example, `opacity: 0.9` on `.orbit` puts the
ball back in the middle of the sun.

There is one more thing that surprises most people. With `preserve-3d`,
the element's own background is part of the scene, as a flat sheet at
depth `0`. Anything pushed behind it is hidden. That is why the orbit's
dark background is on `body`, and not on the stage.

## Where depth turns up on real websites

Oftentimes, depth in CSS is a small touch. A card flips over when we
point at it, to show a second face on its back, with
`backface-visibility: hidden` on both faces. A button can tip a little
towards us as we press it. With more faces, the cube trick is how a
product spins round on a shop's website.

3D games use a trick from [A ball that keeps facing
you](tutorial:a-ball-that-faces-you) all the time. A tree far away, or
a spark, is a flat picture that is turned every frame to face the
player.

Movement in depth can make some people feel unwell. [How a browser draws
each frame](tutorial:how-a-browser-draws-a-frame#less-movement-for-people-who-ask)
shows how to turn it off for people who have asked for less motion.

## What we have now

We can now work out what `perspective` does to a size, and say what the
browser works out for a 3D transform.

| Word | Meaning | Example |
|---|---|---|
| `perspective-origin` | Sets where our eye is, across the element that has the `perspective`. By default, it is in the middle. | `perspective-origin: left;` |
| `perspective()` | Gives one element its own eye, inside its `transform` | `transform: perspective(400px) rotateY(40deg);` |
| `matrix3d()` | The one grid of sixteen numbers that a browser makes from a list of transforms | shown in the **Computed** tab |

## Where to read more

This Place (2017). *The Dolly Zoom.*
<https://www.youtube.com/watch?v=tod2qZnKZEQ>. A camera trick from films
that changes how far away the eye is while keeping the subject the same
size, the same trade that CSS's `perspective` makes. About nine minutes.
