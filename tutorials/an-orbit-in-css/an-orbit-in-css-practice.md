---
title: "An orbit in pure CSS — Practice"
practice_for: an-orbit-in-css
year: "2026-2027"
version: 2026.09.22.1
---

# An orbit in pure CSS — Practice

On this page we practise giving a stage depth with CSS: `perspective`,
`translateZ`, `rotateY` and `transform-style: preserve-3d`. There are
three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small scene to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Watch each preview for a full turn before you change
anything. Most of these mistakes only show at one part of the circle.

## Fix the broken page

**1.** The author wanted the ball to circle the sun, as on the tutorial
page. Instead, it never leaves the middle of the sun.

```html site
id: orbit-practice-flat-html
site: orbit-practice-flat
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: orbit-practice-flat-css
site: orbit-practice-flat
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

The ball has `translateZ(100px)`, so it should be 100 pixels from the
centre. Where did that push go? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Watch the ball. It turns in place, and thins to a line now and then.
   So `.orbit` is still turning it.
2. The ball is inside `.orbit`. What does a browser do to an element's
   children before it applies the element's own transform?
3. Compare the `.orbit` rule with the one on the tutorial page.

**Think about:** which line keeps an element's children at their real
depth?

**Try this next:** the `.stage` rule has the same line. What do you
think it does there? The next problem shows it.

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.orbit {
  transform-style: preserve-3d;
  animation: turn 6s linear infinite;
}
```

Without `transform-style: preserve-3d`, the browser flattens the ball
onto `.orbit`, like a photograph, before it turns `.orbit`. Flat on
`.orbit`, the ball has no depth left, so the push of `100px` is lost
and the ball sits in the middle. With `preserve-3d`, the ball keeps its
depth, and `.orbit` carries it round the circle.

</details>

**2.** This time the ball goes round, but it disappears for the whole
back half of every turn. It should only be hidden while it passes
behind the sun.

```html site
id: orbit-practice-background-html
site: orbit-practice-background
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: orbit-practice-background-css
site: orbit-practice-background
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

Where does the ball go? Fix it, and keep the dark background.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Watch where the ball disappears. Is it when it reaches the sun, or
   earlier?
2. It disappears at the far right, and comes back at the far left. At
   those two points, its depth is `0`.
3. With `preserve-3d` on the stage, what else sits in the 3D space at
   depth `0`? Look at the `.stage` rule.

**Think about:** the tutorial page puts its dark background somewhere
else. Where?

**Try this next:** what would happen if the stage had no background at
all?

</details>

<details class="dl-answer"><summary>answer</summary>

Move the background from the stage to the body:

```css
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
```

With `preserve-3d`, the stage's own background is part of the 3D space,
as a flat sheet at depth `0`. For the back half of every turn, the ball
is behind depth `0`, so the background covered it. The body is outside
the 3D space, so its background stays behind everything.

</details>

**3.** Here the ball goes all the way round, and we can see it the
whole time. But it never goes behind the sun. At the back of its
circle, it is drawn on top of the sun.

```html site
id: orbit-practice-front-html
site: orbit-practice-front
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: orbit-practice-front-css
site: orbit-practice-front
body {
  background: #1b1f2a;
}
.stage {
  width: 320px;
  height: 200px;
  position: relative;
  perspective: 400px;
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

What is missing? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.stage {
  width: 320px;
  height: 200px;
  position: relative;
  perspective: 400px;
  transform-style: preserve-3d;
}
```

The sun and the orbit are both children of the stage. Without
`preserve-3d` on the stage, they do not share one 3D space. The browser
draws them one after the other, in the order they come in the HTML, and
the orbit comes after the sun. So the ball was always drawn on top.
With `preserve-3d` on the stage, the browser compares their depths, and
draws the ball behind the sun when it is further away.

</details>

## Make this

**4.** Add a second, smaller planet to this scene, on an orbit of its
own:

- it is `12px` wide, and white
- it goes round `60px` from the centre of the sun
- it goes round twice as fast as the big ball, once every three seconds
- it passes behind the sun, the same as the big ball

```html site
id: orbit-practice-inner-html
site: orbit-practice-inner
<div class="stage">
  <div class="sun"></div>
  <div class="orbit">
    <div class="ball"></div>
  </div>
</div>
```

```css site
id: orbit-practice-inner-css
site: orbit-practice-inner
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

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The small planet needs its own turning point, because it turns at a
   different speed. So it needs a second `.orbit`, with the planet
   inside it.
2. Give the new orbit and the new planet a second class each, as well
   as `orbit` and `ball`. Then they get every rule the first ones have,
   and a rule for the second class can change only what is different.
3. What is different? For the orbit, only the duration. For the planet,
   its size, its margin and its push.

**Think about:** the margin is minus half the size. What is half of
`12px`?

**Try this next:** can you make the small planet go round the other
way? Look at the `from` and `to` lines of `turn`.

</details>

<details class="dl-answer"><summary>answer</summary>

In the HTML, add a second orbit after the first, still inside the
stage:

```html
<div class="orbit inner">
  <div class="ball small"></div>
</div>
```

In the CSS, add these two rules after the `.ball` rule:

```css
.inner {
  animation-duration: 3s;
}
.small {
  width: 12px;
  height: 12px;
  margin: -6px;
  transform: translateZ(60px);
}
```

`.inner` gets every rule of `.orbit`, including `preserve-3d` and the
`turn` animation, and changes only the duration. `.small` gets the
colour and the round shape from `.ball`, and changes the size, the
margin and the push. The two rules come after `.orbit` and `.ball`, so
they win where the two disagree.

</details>

## In your own site

**5.** Let's give the cards in your site a small tilt in depth when we
point at them.

In your fork, `styles.css` has the `.card:hover` rule you added on
[Styling what the visitor points at: hover and
focus](tutorial:hover-and-focus). Its `transform` is
`translateY(-5px)`, unless you changed it on [Moving things smoothly:
transforms and transitions](tutorial:transitions-and-transforms).

1. Change the `transform` in `.card:hover` to
   `transform: perspective(800px) rotateX(6deg);`.
   `perspective()` at the start of the list gives this one card a depth
   of its own, with our eye 800 pixels away.
2. Save, and refresh `index.html`. Point at the card under "A Little
   About Me". Which edge of the card moves away from you, and which
   comes closer?
3. Try `rotateX(15deg)`, and then `rotateX(-6deg)`. Keep the one you
   like best.
4. Commit the change, with a message such as "Tilt cards in depth on
   hover".

Why does the tilt happen smoothly, and not in one jump?

<details class="dl-answer"><summary>answer</summary>

With `rotateX(6deg)`, the top edge of the card tips away from us, and
the bottom edge comes closer. With `perspective`, nearer things are
drawn bigger, so the card looks a little wider at the bottom than at
the top. A minus angle tips it the other way.

The tilt is smooth because the `.card` rule already has
`transition: transform var(--transition-fast), box-shadow var(--transition-fast);`.
The transition animates any change to `transform`, and a 3D turn is a
change to `transform` too.

</details>
