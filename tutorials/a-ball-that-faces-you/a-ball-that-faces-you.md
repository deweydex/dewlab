---
title: "A ball that keeps facing you"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-add-your-own:
    touches: [WA-LO9]
---

# A ball that keeps facing you

On [An orbit in pure CSS](tutorial:an-orbit-in-css), the ball thinned
to a line at the far left and the far right of its path. Can we keep it
round all the way? On this page we:

- turn the ball back as the orbit carries it round
- see why two animations must keep in step
- see why the order of two transforms matters

## Let's try it

Here is the same orbit, with one change: the ball now has an animation
of its own, called `face-front`.

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

1. Watch the ball at the far left and the far right of its path. Does it
   still thin to a line?
2. In the `.ball` rule, change `face-front 6s` to `face-front 3s`, and
   leave `turn` at `6s`. What happens at the sides now?
3. Now set both animations to `2s`: `turn 2s` in the `.orbit` rule, and
   `face-front 2s` in the `.ball` rule. Does the ball stay round?
4. Set both back to `6s`. Now type a letter, such as `A`, between
   `<div class="ball">` and `</div>` in the HTML. Can you read it all
   the way round?

## Why does this happen?

Now we can explain what we saw. The ball is a flat disc. On the orbit
page, `.orbit` carried it round like a coin lying on a turntable. The
coin turns with the turntable, so at the far left and the far right it
is side-on to us, and we see only its edge. Here is the orbit seen from
above, with the ball drawn as the flat disc it is:

![Two drawings of the orbit seen from above, each with the sun in the middle, a dashed circle for the ball's path, and your eye below the circle. The ball is drawn as a short thick line, at eight places round the circle. On the left, labelled "carried round, never turned back", each line lies along the circle, so at the far left and the far right the lines point straight at your eye: only the ball's edge faces you. On the right, labelled "turned back each time", every line lies flat across, square to your eye, all the way round.](ball-from-above.svg)

### Turning the ball back

The fix is to turn the ball back the other way, by the same angle, at
the same speed. Then it always faces us. `face-front` does this:

```css
@keyframes face-front {
  from { transform: translateZ(100px) rotateY(0deg); }
  to   { transform: translateZ(100px) rotateY(-360deg); }
}
```

- `translateZ(100px)` is the same push out from the centre that the
  ball had on the orbit page. The `.ball` rule has no `transform` of
  its own now, so the push is written inside the animation.
- `rotateY` goes from `0deg` back round to `-360deg`, the opposite way
  to `turn`.

At every moment, `.orbit` has turned the ball one way, and `face-front`
has turned it back the other way by exactly as much. The two turns
cancel each other, so the ball faces us all the way round. That is why the
letter in step 4 stayed readable.

### Keeping in step

The two turns only cancel if the two animations keep in step. In step
2, `face-front` went twice as fast as `turn`. So the ball was turned
back twice as far as it was carried round, and at the sides it was
side-on to us again. In step 3, both went faster, but they kept in
step, so the ball stayed round. Two animations keep in step when they
have the same duration, the same timing, such as `linear`, and the same
start.

### Why the order matters

The order of the two transforms inside `face-front` matters. On [A 3D cube in CSS](tutorial:a-cube-in-css) we saw that the browser applies a list
of transforms from the right-hand end. So `translateZ(100px)
rotateY(-360deg)` means:

1. Turn the ball in place, about its own centre.
2. Then push it 100 pixels out from the centre of the orbit.

The ball spins in place, out at the edge of the orbit. If we swapped
the two, the ball would be pushed out first and then turned back about
the centre of the orbit. That second turn would undo all of `.orbit`'s
turn, so the ball would stop going round at all.

Sometimes we might see a ball that faces us most of the way round, but
looks squashed at the sides. That is a sign that the two animations
have drifted out of step. Check the duration, the timing and the start
of both.

## Now add your own

The editor above is ours to change.

1. Add a second ball, on the far side of the sun, that also keeps
   facing us. In the HTML, add `<div class="ball far"></div>` under the
   first ball, inside `.orbit`.
2. It needs its own animation, because its push is `translateZ(-100px)`.
   Add a `@keyframes` rule called `face-front-far`, the same as
   `face-front` but with `-100px`.
3. Add a rule for `.far`, after the `.ball` rule, that gives it
   `animation: face-front-far 6s linear infinite;`.

Do both balls stay round all the way round the sun?

## What we have now

We can now keep a flat element facing us as it goes round, and we know
why the order of two transforms matters.

| Idea | Meaning | Example |
|---|---|---|
| an opposite turn | A second turn by the same angle, the other way, at the same speed. It keeps a flat element facing us while its parent carries it round. | `rotateY(-360deg)` in `face-front` |
| animations *in step* | Two animations with the same duration, timing and start, so that their changes match at every moment | `turn 6s linear` and `face-front 6s linear` |
| the order of transforms | The browser applies a list of transforms from the right-hand end, so the last one in the list happens first | `translateZ(100px) rotateY(-360deg)` turns, then pushes |

## Where to read more

Josh's Channel (2022). *In Video Games, The Player Never Moves.*
<https://www.youtube.com/watch?v=wiYTxjJjfxs>. A game keeps its camera
still, and moves the whole world the other way. It uses the same kind of
turns and moves this page makes. About nineteen minutes.
