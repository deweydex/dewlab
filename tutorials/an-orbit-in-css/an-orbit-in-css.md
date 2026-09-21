---
title: "An orbit in pure CSS"
year: "2026-2027"
version: 2026.09.21.1
covers:
  why-this-happens:
    covers: [WA-LO9]
  why-the-ball-vanishes:
    covers: [WA-LO9]
  your-turn:
    touches: [WA-LO9]
---

# An orbit in pure CSS

A white ball circling a sun, passing behind it and coming back round
the front, with no JavaScript and no arithmetic. The browser does the
dividing by depth for us. Watch it for a full turn before reading on,
and keep an eye on the ball when it is at the far left or far right.

```html site
id: orbit-html
site: orbit
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: orbit-css
site: orbit
.stage {
  width: 320px;
  height: 200px;
  background: #1b1f2a;
  position: relative;
  perspective: 400px;
  transform-style: preserve-3d;
}
.sun, .orbit, .ball {
  position: absolute;
  left: 50%;
  top: 50%;
  border-radius: 50%;
}
.sun {
  width: 48px;
  height: 48px;
  margin: -24px;
  background: #f5c542;
}
.orbit {
  transform-style: preserve-3d;
  animation: turn 6s linear infinite;
}
.ball {
  width: 24px;
  height: 24px;
  margin: -12px;
  background: white;
  transform: translateZ(100px);
}
@keyframes turn {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(360deg); }
}
```

## Why this happens

`perspective: 400px` on the stage is the sheet of glass from [A Point
on the Screen](tutorial:a-point-on-the-screen#why-dividing-works),
standing 400 pixels in front of your eye. Once it is set, anything
inside the stage that has a depth gets its position divided by that
depth: nearer things are drawn bigger and further from the centre,
further things smaller and closer to it. Without this line, every
`rotateY` and `translateZ` below would still run, and the ball would
slide left and right without ever changing size.

The three-dimensional part is two transforms working together.
`rotateY()` turns an element about its vertical axis, and the `turn`
animation turns `.orbit` all the way round once every six seconds.
`translateZ(100px)` pushes the ball 100 pixels towards you, out from
the centre of `.orbit`. Because the ball is inside `.orbit`, it is
carried round as `.orbit` turns, always 100 pixels out from the
centre, which is what a circle is. `.orbit` itself has no size at all.
It is just a point in the middle of the stage for the ball to swing
around.

`transform-style: preserve-3d` is the line that is easiest to leave
out and hardest to diagnose. Normally a browser flattens an element's
children onto it, like a photograph, before applying the parent's own
transform. `preserve-3d` keeps them in their real positions instead,
so the ball's depth survives, and so the browser can see that the ball
is behind the sun for half of every turn and draw it there.

## Why the ball vanishes

At the far left and the far right of its orbit the ball thins to a
line and disappears for a moment. That is not a bug in the browser.
The ball is a flat disc, glued to a turntable, and at those two points
the turntable has turned it edge-on to you. A coin on a record player
does the same thing.

The fix is to turn the ball back the other way, by the same angle, at
the same speed, so that it always faces you. A second animation on the
ball does it. Its keyframes start with the same `translateZ(100px)` as
before, so that the push out from the centre stays, and add a
`rotateY` going from 0 back round to $-360°$:

```html site
id: orbit-facing-html
site: orbit-facing
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: orbit-facing-css
site: orbit-facing
.stage {
  width: 320px;
  height: 200px;
  background: #1b1f2a;
  position: relative;
  perspective: 400px;
  transform-style: preserve-3d;
}
.sun, .orbit, .ball {
  position: absolute;
  left: 50%;
  top: 50%;
  border-radius: 50%;
}
.sun {
  width: 48px;
  height: 48px;
  margin: -24px;
  background: #f5c542;
}
.orbit {
  transform-style: preserve-3d;
  animation: turn 6s linear infinite;
}
.ball {
  width: 24px;
  height: 24px;
  margin: -12px;
  background: white;
  animation: face-front 6s linear infinite;
}
@keyframes turn {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(360deg); }
}
@keyframes face-front {
  from { transform: translateZ(100px) rotateY(0deg); }
  to   { transform: translateZ(100px) rotateY(-360deg); }
}
```

The two animations run for the same six seconds, so at every moment
the ball has been turned one way by `.orbit` and back the other way by
exactly as much. The order inside `face-front` matters: `translateZ`
first, then `rotateY`, so the ball spins on its own spot out at the
edge of the orbit rather than swinging back in to the centre.

## Your turn

Let's try changing the number in `perspective`, in the second editor.
What does `perspective: 150px` do to the size of the ball at the front
compared to the back? What about `perspective: 2000px`? Then try adding
a second ball with `translateZ(-100px)`, on the far side of the sun
from the first. Give it its own class, or the two will share every
rule. Once both are going round, try `transform: rotateX(-30deg)
rotateY(360deg)` as the end of the `turn` keyframes, with the same
`rotateX(-30deg)` at the start, to look down on the orbit from a
little above.

## What you have now

A ball in orbit, in three dimensions, in CSS alone.

`perspective` makes a stage's children shrink with their depth, and the
number is how far the screen sits in front of your eye. `rotateY()`
turns an element about its vertical axis. `translateZ()` pushes an
element towards you or away from you. `transform-style: preserve-3d`
keeps an element's children at their real depth instead of flattening
them onto it. Two animations at the same speed in opposite directions
keep a flat element facing you as it goes round.
