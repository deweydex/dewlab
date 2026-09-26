---
title: "A ball that keeps facing you — Practice"
practice_for: a-ball-that-faces-you
year: "2026-2027"
version: 2026.09.22.1
---

# A ball that keeps facing you — Practice

On this page we practise keeping a flat element facing us while its
parent carries it round: an opposite turn, two animations in step, and
the order of two transforms. There are two kinds of problem:

- a broken page, where we find the mistake and fix it
- a small scene to build from a description

Each problem has a folded answer. Some also have a hint, folded before
the answer. Watch each preview for a full turn before you change
anything. Most of these mistakes only show at one part of the circle.

## Fix the broken page

**1.** The author wanted the ball to go round the sun and keep facing
us. Instead, the ball does not go round at all.

```html site
id: facing-practice-still-html
site: facing-practice-still
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: facing-practice-still-css
site: facing-practice-still
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
  from { transform: rotateY(0deg) translateZ(100px); }
  to   { transform: rotateY(-360deg) translateZ(100px); }
}
```

Both animations are there, and both take six seconds. Why does the
ball sit still in front of the sun? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Compare the `face-front` keyframes with the ones on the tutorial
   page. The same two transforms are there. What is different?
2. The browser applies a list of transforms from the right-hand end.
   In this list, which happens first: the push or the turn?
3. If the ball is pushed out first, what does the turn go round: the
   ball's own centre, or the centre of the orbit?

**Think about:** `.orbit` turns the ball one way round the centre of the
orbit. What does a second turn the other way, round the same centre, do
to that?

**Try this next:** what would you see if `face-front` turned by
`+360deg` in this broken order?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
@keyframes face-front {
  from { transform: translateZ(100px) rotateY(0deg); }
  to   { transform: translateZ(100px) rotateY(-360deg); }
}
```

The two transforms were in the wrong order. With `rotateY` on the left,
the push happened first, and then the turn went round the centre of the
orbit. So `face-front` carried the ball back round the circle, exactly
as far as `.orbit` carried it forwards. The two cancelled each other, and the
ball stayed at the front. With `translateZ` on the left, the turn
happens first, while the ball is still at the centre, so the ball only
spins in place.

</details>

**2.** In this scene, the ball stays round at the front and at the
back. But at the sides it looks squashed, like an egg standing on its
end.

```html site
id: facing-practice-timing-html
site: facing-practice-timing
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: facing-practice-timing-css
site: facing-practice-timing
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
  animation: face-front 6s ease-in-out infinite;
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

Both animations take six seconds. So what is out of step? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.ball {
  width: 24px;
  height: 24px;
  margin: -12px;
  background: white;
  animation: face-front 6s linear infinite;
}
```

`face-front` had `ease-in-out` timing, and `turn` had `linear`. Both
start and end together, so the ball faces us at the start and halfway.
In between, `ease-in-out` starts slowly, so the ball is turned back
less than `.orbit` has turned it. Then it turns faster to match. At the sides the
two turns do not cancel, and the ball is partly side-on. Two
animations are in step only with the same duration, the same timing
and the same start.

</details>

**3.** The author put a letter on this ball, to check that it faces us.
Watch the letter for a full turn.

```html site
id: facing-practice-sign-html
site: facing-practice-sign
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball">R</div>
  </div>
</div>
```

```css site
id: facing-practice-sign-css
site: facing-practice-sign
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
  text-align: center;
  font: bold 16px/24px sans-serif;
  animation: face-front 6s linear infinite;
}
@keyframes turn {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(360deg); }
}
@keyframes face-front {
  from { transform: translateZ(100px) rotateY(0deg); }
  to   { transform: translateZ(100px) rotateY(360deg); }
}
```

Where does the ball thin to a line now? What happens to the letter at
the far left and the far right? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
@keyframes face-front {
  from { transform: translateZ(100px) rotateY(0deg); }
  to   { transform: translateZ(100px) rotateY(-360deg); }
}
```

`face-front` turned the ball the same way as `.orbit`, so the two turns
added together, and the ball turned twice as fast as the orbit. It thinned
to a line halfway between the front and each side. At the far left
and the far right it had turned half a turn, so the letter was back to
front.
The turn that keeps it facing us has to go the other way, to
`-360deg`.

</details>

## Make this

**4.** This name tag goes round the sun, but at the sides we only see
its edge, and on the far side its word is back to front. Make it face
us all the way round, so that we can read "Moon" wherever it is.

```html site
id: facing-practice-tag-html
site: facing-practice-tag
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="tag">Moon</div>
  </div>
</div>
```

```css site
id: facing-practice-tag-css
site: facing-practice-tag
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
.sun, .orbit, .tag {
  position: absolute;
  left: 50%;
  top: 50%;
}
.sun {
  width: 48px;
  height: 48px;
  margin: -24px;
  border-radius: 50%;
  background: #f5c542;
}
.orbit {
  transform-style: preserve-3d;
  animation: turn 8s linear infinite;
}
.tag {
  width: 60px;
  height: 24px;
  margin: -12px -30px;
  background: white;
  text-align: center;
  font: bold 14px/24px sans-serif;
  transform: translateZ(110px);
}
@keyframes turn {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(360deg); }
}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The tag needs an animation of its own, the way the ball has
   `face-front` on the tutorial page.
2. What push does the tag have now? The animation replaces the tag's
   `transform`, so the push must be inside the animation too.
3. How long does `turn` take here? Is it the same as on the tutorial
   page?

**Think about:** the three things that keep two animations in step.

**Try this next:** add a second tag, on the far side of the sun, that
also stays readable.

</details>

<details class="dl-answer"><summary>answer</summary>

Add a `@keyframes` rule, and give the tag an animation in step with
`turn`:

```css
.tag {
  width: 60px;
  height: 24px;
  margin: -12px -30px;
  background: white;
  text-align: center;
  font: bold 14px/24px sans-serif;
  animation: face-front 8s linear infinite;
}
@keyframes face-front {
  from { transform: translateZ(110px) rotateY(0deg); }
  to   { transform: translateZ(110px) rotateY(-360deg); }
}
```

The push is now `110px`, inside the animation, with the turn back on
the right so that it happens first. `turn` takes `8s` here, so
`face-front` takes `8s` too. We can delete the `transform` line in
`.tag`, because the animation sets `transform` all the time.

</details>

**5.** Here is the ball from the tutorial page. Make it go round the
sun the other way, and still face us all the way round.

```html site
id: facing-practice-reverse-html
site: facing-practice-reverse
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: facing-practice-reverse-css
site: facing-practice-reverse
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

<details class="dl-answer"><summary>answer</summary>

Change the end of both `@keyframes` rules:

```css
@keyframes turn {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(-360deg); }
}
@keyframes face-front {
  from { transform: translateZ(100px) rotateY(0deg); }
  to   { transform: translateZ(100px) rotateY(360deg); }
}
```

`turn` now goes to `-360deg`, so the orbit turns the other way. The
turn back always goes the opposite way to the orbit, so `face-front`
now goes to `+360deg`. If we changed only `turn`, the two turns would
go the same way, and add together, the way they did in problem 3.

</details>
