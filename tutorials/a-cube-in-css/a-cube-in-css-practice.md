---
title: "A 3D cube in CSS — Practice"
practice_for: a-cube-in-css
year: "2026-2027"
version: 2026.09.22.1
---

# A 3D cube in CSS — Practice

On this page we practise building solid shapes from flat squares: a
push and a turn for each face, the order of the transforms, and
`backface-visibility`. There are two kinds of problem:

- a broken page, where we find the mistake and fix it
- a small shape to build from a description

Each problem has a folded answer. Some also have a hint, folded before
the answer. Watch each shape turn for a few seconds before you change
anything.

## Fix the broken page

**1.** The author built the cube from the tutorial page, but it is not
a cube. It is one flat square that turns and tumbles.

```html site
id: cube-practice-flat-html
site: cube-practice-flat
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
id: cube-practice-flat-css
site: cube-practice-flat
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

All six faces have their transforms. What is missing? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.cube {
  width: 100px;
  height: 100px;
  position: relative;
  transform-style: preserve-3d;
  animation: tumble 12s linear infinite;
}
```

Without `transform-style: preserve-3d` on `.cube`, the browser
flattens the six faces onto `.cube`, like a photograph, before it
applies the `tumble` animation. So the six faces became one flat
picture, and that picture tumbled. With `preserve-3d`, each face keeps
the place its transform gives it, and the whole cube tumbles.

</details>

**2.** Here the six faces are all there, but they float apart, with
gaps between them. The cube looks as if it has burst open.

```html site
id: cube-practice-apart-html
site: cube-practice-apart
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
id: cube-practice-apart-css
site: cube-practice-apart
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
.front  { transform: translateZ(100px); }
.back   { transform: rotateY(180deg) translateZ(100px); }
.right  { transform: rotateY(90deg) translateZ(100px); }
.left   { transform: rotateY(-90deg) translateZ(100px); }
.top    { transform: rotateX(90deg) translateZ(100px); }
.bottom { transform: rotateX(-90deg) translateZ(100px); }
@keyframes tumble {
  from { transform: rotateX(0deg) rotateY(0deg); }
  to   { transform: rotateX(360deg) rotateY(720deg); }
}
```

How far should each face be pushed out from the middle of the cube?
Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Every face starts in the middle of the cube, and is then pushed out.
2. The cube is `100px` wide. How far is it from the middle of the cube
   to its front face?
3. So how big should every push be?

**Think about:** the push is always half the width of the cube.

**Try this next:** change every push to `30px`, and keep the faces
`100px` wide. What shape do you get, and why?

</details>

<details class="dl-answer"><summary>answer</summary>

Change every `translateZ(100px)` to `translateZ(50px)`:

```css
.front  { transform: translateZ(50px); }
.back   { transform: rotateY(180deg) translateZ(50px); }
.right  { transform: rotateY(90deg) translateZ(50px); }
.left   { transform: rotateY(-90deg) translateZ(50px); }
.top    { transform: rotateX(90deg) translateZ(50px); }
.bottom { transform: rotateX(-90deg) translateZ(50px); }
```

Each face starts in the middle of the cube, so the push is the distance
from the middle to a face: half the cube's width, `50px`. With
`100px`, every face went twice as far out as it should, and the faces
no longer met at their edges.

</details>

**3.** This cube has a word on each face. Watch it tumble. One face is
missing, and one name is in the wrong place.

```html site
id: cube-practice-twotops-html
site: cube-practice-twotops
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
id: cube-practice-twotops-css
site: cube-practice-twotops
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
.bottom { transform: rotateX(90deg) translateZ(50px); }
@keyframes tumble {
  from { transform: rotateX(0deg) rotateY(0deg); }
  to   { transform: rotateX(360deg) rotateY(720deg); }
}
```

Which face is missing, and where did the word "bottom" go? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the word "bottom" as the cube turns. Which other word is on the
   same face?
2. Compare the `.top` and `.bottom` lines. How are they different?
3. `.right` and `.left` turn a quarter turn each way. What should
   `.top` and `.bottom` do?

**Think about:** a copied line is the easiest place for a mistake to
hide.

**Try this next:** which transform would put a seventh face exactly on
top of the back face?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.bottom { transform: rotateX(-90deg) translateZ(50px); }
```

The `.bottom` line had the same turn as `.top`, `rotateX(90deg)`. So
both faces were pushed out and then tipped the same way, and they ended
up in the same place, on top. The cube had no bottom face. The bottom
face needs the quarter turn the other way, `rotateX(-90deg)`, the same
way that `.left` turns the other way to `.right`.

</details>

## Make this

**4.** Make the cube bigger: each face `160px` square, still a closed
cube with no gaps, still tumbling. Start from this copy of the tutorial
cube.

```html site
id: cube-practice-big-html
site: cube-practice-big
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
id: cube-practice-big-css
site: cube-practice-big
.stage {
  width: 320px;
  height: 320px;
  background: #1b1f2a;
  perspective: 800px;
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

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which rules set a size of `100px`? Change all of them.
2. How far is it from the middle of a `160px` cube to one of its faces?
3. That distance goes in every `translateZ`.

**Think about:** if one number is left behind, what would you see?
Problem 2 on this page shows one answer.

**Try this next:** can you make a box that is not a cube, `160px` wide
and `160px` tall but only `80px` deep? Which faces change shape?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.cube {
  width: 160px;
  height: 160px;
  position: relative;
  transform-style: preserve-3d;
  animation: tumble 12s linear infinite;
}
.face {
  position: absolute;
  width: 160px;
  height: 160px;
  display: grid;
  place-items: center;
  font: bold 18px sans-serif;
  color: white;
  border: 2px solid white;
  background: rgba(70, 130, 220, 0.55);
}
.front  { transform: translateZ(80px); }
.back   { transform: rotateY(180deg) translateZ(80px); }
.right  { transform: rotateY(90deg) translateZ(80px); }
.left   { transform: rotateY(-90deg) translateZ(80px); }
.top    { transform: rotateX(90deg) translateZ(80px); }
.bottom { transform: rotateX(-90deg) translateZ(80px); }
```

The width and height change in two rules, `.cube` and `.face`, and all
six pushes change too. Each push is half the new width, `80px`. `.cube` must be the same size as a face, so that every face
starts in the middle of the cube.

</details>

**5.** Make a card that flips over when we point at it, to show a
second side. The cell below has a card with two sides, stacked on top
of each other. The finished card should work like this:

- at first, we see the side that says "Squishy Squid"
- when we point at the card, it turns over, smoothly, about its
  vertical axis
- then we see the other side, "€12, in stock", and the words read the
  right way round
- we never see a side's back, reversed, through the other side

```html site
id: cube-practice-flip-html
site: cube-practice-flip
<div class="scene">
  <div class="card">
    <div class="side front">Squishy Squid</div>
    <div class="side back">€12, in stock</div>
  </div>
</div>
```

```css site
id: cube-practice-flip-css
site: cube-practice-flip
.scene {
  width: 160px;
  height: 100px;
  margin: 20px;
  perspective: 600px;
}
.card {
  width: 160px;
  height: 100px;
  position: relative;
}
.side {
  position: absolute;
  width: 160px;
  height: 100px;
  display: grid;
  place-items: center;
  font: bold 16px sans-serif;
  border: 2px solid #2c3e50;
  border-radius: 8px;
}
.front {
  background: #f6f4f0;
}
.back {
  background: #2c3e50;
  color: white;
}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The back side has to start already turned away from us, by half a
   turn about the vertical axis.
2. When the card turns, its two sides must keep their depth. Which
   property on `.card` does that?
3. A side should not be drawn while its back is towards us. Which
   property on `.side` does that?
4. The turn itself is a `transform` on `.card:hover`, and a
   `transition` on `.card` makes it smooth.

**Think about:** why must the back side start turned away, and not
facing us?

**Try this next:** can you make the card flip about its horizontal
axis instead, like a page on a flip chart?

</details>

<details class="dl-answer"><summary>answer</summary>

Add these lines to the rules that are there, and add a rule for
`.card:hover`:

```css
.card {
  width: 160px;
  height: 100px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.6s;
}
.card:hover {
  transform: rotateY(180deg);
}
.side {
  position: absolute;
  width: 160px;
  height: 100px;
  display: grid;
  place-items: center;
  font: bold 16px sans-serif;
  border: 2px solid #2c3e50;
  border-radius: 8px;
  backface-visibility: hidden;
}
.back {
  background: #2c3e50;
  color: white;
  transform: rotateY(180deg);
}
```

The back side starts half a turn round, so its back is towards us, and
`backface-visibility: hidden` hides it. When the card turns half a
turn, the front side turns its back to us and is hidden. The back side
has now turned a whole turn, so it faces us, and its words read the
right way round. `preserve-3d` keeps the two sides at their own angles
while the card turns.

</details>
