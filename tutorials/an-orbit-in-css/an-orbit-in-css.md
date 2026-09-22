---
title: "An orbit in pure CSS"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-add-your-own:
    touches: [WA-LO9]
---

# An orbit in pure CSS

Can a flat web page show depth, with one thing passing behind another?
It can, with no JavaScript and no arithmetic. The browser does all the
work. On this page we:

- watch a ball circle a sun, in HTML and CSS alone
- see how a few lines of CSS give the stage its depth
- change the depth, and add a second ball

## Let's try it

Here is a white ball circling a yellow sun, on a dark stage.

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
body {
  background: #1b1f2a;
}
.stage {
  width: 320px;
  height: 200px;
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

1. Watch the ball for a full turn. When does it look biggest, and when
   does it look smallest? Does it ever pass behind the sun?
2. Keep watching the ball when it reaches the far left or the far right
   of its path. What happens to it there?
3. In the `.stage` rule, change `perspective: 400px` to
   `perspective: 150px`. How does the ball at the front compare with
   the ball at the back now? Then try `2000px`.
4. Put it back to `400px`. Now delete the whole line
   `perspective: 400px;`. What does the ball do now?

Put the line back before you read on.

## Why does this happen?

Now we can explain what we saw. Four ideas work together here: a
`@keyframes` rule that turns, a stage with depth, two transforms that
make a circle, and one line that keeps the depth.

### The frames

A *frame* is one still picture on the screen. The browser draws a new
frame many times a second, often about sixty, and our eye blends them
into movement. On [Animation with
keyframes](tutorial:keyframes-and-the-checkbox-hack) we wrote a
`@keyframes` rule. Its name fits: we write down a few *key* frames, the important
ones, and the browser works out every frame in between. `turn` names
only two:

- at the start, `.orbit` is turned by `0deg`
- at the end, it is turned by `360deg`, one full circle

`animation: turn 6s linear infinite` plays those frames over six
seconds, at a steady speed, and starts again forever. At sixty frames
a second, the browser draws about 360 frames for every turn. We wrote
two of them.

### Where everything starts

The shared rule for `.sun, .orbit, .ball` puts all three in the middle
of the stage. `left: 50%` and `top: 50%` place an element's top-left
corner at the middle. A negative margin of half its size then pulls
the element back, so that its centre sits at the middle. The sun is
`48px` wide, so its margin is `-24px`.

### Depth

`perspective: 400px` on the stage gives it depth. It tells the browser
to imagine our eye 400 pixels in front of the screen, and to draw each
thing the size it would look from there. Here is the stage seen from
the side:

![The stage seen from the side. On the left is your eye. 400 pixels to its right stands the screen, drawn as a tall line, with a label perspective: 400px along the bottom. Two balls of the same size sit near the screen. One is 100 pixels in front of it, nearer the eye, marked translateZ(100px). The other is 100 pixels behind it, marked translateZ(-100px). Dashed lines run from the eye past the edges of each ball to the screen. Where they meet the screen, the ball in front makes a tall bar, labelled "in front: drawn bigger", and the ball behind makes a short bar, labelled "behind: drawn smaller".](perspective-glass.svg)

A thing nearer to us is drawn bigger, and further from the middle of
the stage. A thing further away is drawn smaller, and closer to the
middle. That is what we saw in step 1. At the front of the orbit, the
`24px` ball is drawn about `32px` wide. At the back, it is drawn about
`19px` wide.

A smaller `perspective` puts our eye closer to the screen, so the
difference between near and far grows. That is why `150px` in step 3
made the ball huge at the front and small at the back, and why `2000px`
made it hardly change size. With no `perspective` at all, in step 4,
the browser draws everything the same size, whatever its depth. The
ball still goes round, but it slides left and right and never grows or
shrinks. ([A Point on the
Screen](tutorial:a-point-on-the-screen#why-dividing-works), on the
Computational Methods course, shows the arithmetic the browser does
here.)

### The circle

The circle comes from two transforms working together:

- `rotateY()` turns an element about its vertical axis, like a record
  on a record player. The `turn` animation turns `.orbit` all the way
  round once every six seconds.
- `translateZ(100px)` pushes the ball 100 pixels towards us, out from
  the centre of `.orbit`. A minus value pushes an element away from
  us.

The ball is inside `.orbit`, so it is carried round as `.orbit` turns,
always 100 pixels from the centre. A path that stays the same distance
from a centre is a circle. `.orbit` itself has no size at all. It is a
point in the middle of the stage for the ball to swing around.

### Keeping the depth

`transform-style: preserve-3d` is the line that is easiest to forget,
and the hardest to find when it is missing. Without it, a browser
flattens an element's children onto the element, like a photograph,
before it applies the element's own transform. `preserve-3d` keeps the
children at their real depth.

The page uses it twice. On `.orbit`, it keeps the ball out at its
100 pixels as `.orbit` turns. On `.stage`, it puts the sun and the
orbit in one shared space. Then the browser can work out that the ball
is behind the sun when it passes the back of its circle, and draw it
there.

Did you notice that the dark background is on `body`, and not on the
stage? With `preserve-3d`, the stage's own background is part of that
shared space too, as a flat sheet at depth `0`. The ball spends the back
half of every turn behind depth `0`, so a background on the stage would
hide it there.

### Why the ball thins at the sides

In step 2, at the far left and the far right, the ball thinned to a
line and disappeared for a moment. That is not a mistake in the
browser. The ball is a flat disc, fixed to a turntable. At those two
points the turntable has turned it side-on to us, so all we can see is
its edge. A coin lying on a record player does the same thing. We fix
this on [A ball that keeps facing you](tutorial:a-ball-that-faces-you).

Sometimes we might add `translateZ` to an element and see no change at
all. Two things are worth checking. Is there a `perspective` on an
element around it? And does every element between the two have
`transform-style: preserve-3d`?

## Now add your own

The editor above is ours to change. Try each of these on its own.

1. Add a second ball on the far side of the sun from the first. In the
   HTML, under the first ball and still inside `.orbit`, add
   `<div class="ball far"></div>`. The class `ball` gives it the same
   size, colour and place as the first ball. It needs a class of its
   own as well, `far`, or the two balls would share every rule,
   including the push.
2. In the CSS, after the `.ball` rule, add a rule for `.far` with
   `transform: translateZ(-100px);`. The later rule wins, so only the
   new ball is pushed away from us.
3. Now look down on the orbit from a little above. `rotateX()` turns an
   element about a horizontal axis, and we meet it properly on [A cube
   in CSS](tutorial:a-cube-in-css). Change the `turn` keyframes so that
   both lines start with `rotateX(-30deg)`:
   `from { transform: rotateX(-30deg) rotateY(0deg); }` and
   `to { transform: rotateX(-30deg) rotateY(360deg); }`.

Do the two balls stay on opposite sides of the sun all the way round?
Can you see the whole circle now?

## What we have now

We can now give a stage depth, and send a ball round a circle inside
it, with CSS alone.

| Word | Meaning | Example |
|---|---|---|
| *frame* | One still picture. The browser draws many a second, and `@keyframes` names the important ones. | the `from` and `to` lines of `turn` |
| `perspective` | Gives an element's children depth. The value is how far our eye is from the screen. A smaller value gives a stronger effect. | `perspective: 400px;` |
| `rotateY()` | Turns an element about its vertical axis, like a turntable | `transform: rotateY(90deg);` |
| `translateZ()` | Pushes an element towards us, or away with a minus value. It shows only when an element around it has a `perspective`. | `transform: translateZ(100px);` |
| `transform-style: preserve-3d` | Keeps an element's children at their real depth when the element itself is transformed | `transform-style: preserve-3d;` |
