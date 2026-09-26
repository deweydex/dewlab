---
title: "Moving things smoothly: transforms and transitions"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Moving things smoothly: transforms and transitions

On [Styling what the visitor points at: hover and focus](tutorial:hover-and-focus), a button lifted
up under the pointer. That lift was a transform. On this page we:

- move, resize and turn a box with `transform`
- find out what happens to the boxes around it
- slow a transition down, so we can watch it closely

## Let's try it

Here are three boxes side by side. Each one has a different `transform`,
and the text in each box names its own transform.

```html site
id: transforms-html
site: transforms
<div class="box move">translateY(-15px)</div>
<div class="box grow">scale(1.2)</div>
<div class="box turn">rotate(8deg)</div>
```

```css site
id: transforms-css
site: transforms
.box {
  display: inline-block;
  padding: 12px 16px;
  margin: 10px;
  background: #f6f4f0;
  border: 1px solid #2c3e50;
}
.move { transform: translateY(-15px); }
.grow { transform: scale(1.2); }
.turn { transform: rotate(8deg); }
```

1. The first box has `translateY(-15px)`. What happens if we change
   `-15px` to `-40px`? And to `15px`?
2. When the first box moves, do the other two boxes move with it?
3. What happens if we change `scale(1.2)` to `scale(2)`? Look at the
   gaps on either side of the middle box.
4. Change `rotate(8deg)` to `rotate(45deg)`, then to `rotate(-45deg)`.
   Which way does each one turn?

## Why does this happen?

Now we can explain what we saw. `transform` changes an element's
position, size or shape without moving anything else around it. The
page keeps the element's original space exactly as it was, and the
browser draws the element somewhere new. So the other boxes stayed still
in step 2. And in step 3, the bigger box spread
across the gaps and into its neighbours' space, without pushing them
away.

![Three boxes in a row, drawn twice. In the top row, none of them has a transform, and they sit side by side with gaps between them. In the bottom row, the middle box has scale(2). It is drawn twice as big, and spreads over the gaps and over the edges of the boxes on either side. A dashed outline shows the middle box's original space, which the page keeps. The first and third boxes have not moved.](transform-keeps-its-space.svg)

The boxes sit side by side because they have `display: inline-block`.
That lets them share one line, like words, and still take a transform.

Each of the three boxes uses a different transform function:

| Function | What it does | Example |
|---|---|---|
| `translateY()` | Shifts an element up or down. A minus value moves it up, and a plus value moves it down. | `translateY(-15px)` |
| `scale()` | Grows or shrinks an element. `1` is its normal size, so `1.2` is 20% bigger. It grows out from its centre. | `scale(1.2)` |
| `rotate()` | Turns an element. `deg` means degrees, and a full turn is `360deg`. A plus angle turns it clockwise, and a minus angle turns it the other way. | `rotate(8deg)` |

### Transitions

On its own, a transform jumps straight to its new state. We met
`transition` on the last page. It makes a change happen smoothly
instead. One `transition` has three parts:

```css
transition: transform 0.2s ease;
/*          property  time  pacing */
```

- the property to animate, here `transform`
- how long the change takes, here `0.2s`, a fifth of a second
- the curve that controls its pacing, here `ease`

With `ease`, the change speeds up towards the middle and slows down at
the end. With `linear`, it keeps one steady speed from start to finish.

When a transition sits on an element's base rule, not on `:hover`, it
animates a change in both directions. The element settles back as
smoothly as it arrived.

To use two transform functions at once, we list them in one
declaration, with a space between them:
`transform: translateY(-5px) scale(1.05);`.

## Now in your own site

In your fork, find the `.card:hover` rule you turned on in [Styling what the visitor points at: hover and focus](tutorial:hover-and-focus).

1. Change `translateY(-5px)` to `scale(1.05)`.
2. Save, and refresh. Move your pointer over a card. Does it lift, or
   grow?
3. Now find the base `.card` rule, with the `transition` line. It uses
   `var(--transition-fast)` twice, and that variable is `0.2s ease`.
   Change the line to this:

   ```css
   transition: transform 1s ease, box-shadow 1s ease;
   ```

4. Save, refresh, and hover again. Can you follow the same animation in
   slow motion?
5. You could try both at once: `transform: translateY(-5px) scale(1.05);`

Which do you like best for your cards: a lift, a grow, or both? When you
have chosen, you could put `var(--transition-fast)` back in place of
`1s ease`.

## What we have now

We can now move, resize and turn an element, and we know how
`transition` makes any of those changes smooth.

| Word | Meaning | Example |
|---|---|---|
| `transform` | Changes an element's position, size or shape without affecting its neighbours | `transform: scale(1.2);` |
| `translateY()` | Shifts an element up or down | `translateY(-15px)` |
| `scale()` | Grows or shrinks an element | `scale(1.2)` |
| `rotate()` | Turns an element | `rotate(8deg)` |

## Where to read more

SimonDev (2022). *An In-Depth look at Lerp, Smoothstep, and Shaping
Functions.* <https://www.youtube.com/watch?v=YJB1QnEmlTs>. The easing in a
CSS transition is a small function from time to position. SimonDev draws
the common ones as graphs, from a straight line to a curve that starts and
ends slowly. About eight minutes.
