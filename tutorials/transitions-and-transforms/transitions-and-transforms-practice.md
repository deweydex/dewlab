---
title: "Moving things smoothly: transforms and transitions — Practice"
practice_for: transitions-and-transforms
year: "2026-2027"
version: 2026.09.22.1
---

# Moving things smoothly: transforms and transitions — Practice

On this page we practise `transform`, which moves, resizes and turns an
element, and `transition`, which makes the change smooth. There are
three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small effect to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

## Fix the broken page

**1.** The designer wanted this tile to lift up by `10px` and grow a
little under the pointer. Move your pointer over it.

```html site
id: transform-practice-two-html
site: transform-practice-two
<div class="tile">Squishy Squid</div>
```

```css site
id: transform-practice-two-css
site: transform-practice-two
.tile {
  display: inline-block;
  margin: 30px;
  padding: 20px;
  background: #f6f4f0;
  border: 2px solid #2c3e50;
  transition: transform 0.3s ease;
}
.tile:hover {
  transform: translateY(-10px);
  transform: scale(1.1);
}
```

Does the tile lift, grow, or both? Fix it, so that it does both.

<details class="dl-answer"><summary>answer</summary>

```css
.tile:hover {
  transform: translateY(-10px) scale(1.1);
}
```

The tile only grew. The two declarations both set the same property,
`transform`, so the second one replaced the first completely. To use two
transform functions together, we list them in one declaration, with a
space between them.

</details>

**2.** The "New!" label should be tilted a little, like a sticker. It
sits flat.

```html site
id: transform-practice-inline-html
site: transform-practice-inline
<p>Cuddly Cuttlefish <span class="badge">New!</span></p>
```

```css site
id: transform-practice-inline-css
site: transform-practice-inline
.badge {
  padding: 2px 6px;
  background: #d9720c;
  color: white;
  transform: rotate(-10deg);
}
```

The `transform` line has no mistake in it. So why does nothing turn?
Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What kind of element is `<span>`? Does it start on a new line, or
   sit inside a line of text?
2. Look back at the tutorial's three boxes. What `display` value did
   they have, and why?
3. What happens if we try the same `rotate(-10deg)` on the `<p>`
   instead?

**Think about:** a transform works on a box. Which kinds of element
make a box that a transform can move?

**Try this next:** would `translateY(-4px)` on a link inside a
sentence move it?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.badge {
  display: inline-block;
  padding: 2px 6px;
  background: #d9720c;
  color: white;
  transform: rotate(-10deg);
}
```

A `<span>` sits inside a line of text, the way a word does, and a
transform does not work on an element like that. `display: inline-block`
keeps the badge in the line of text, next to the name, and gives it a
box that a transform can turn. Links, `<em>` and `<strong>` behave the
same way as a `<span>`.

</details>

**3.** This button should grow smoothly under the pointer. It jumps
instead.

```html site
id: transform-practice-unit-html
site: transform-practice-unit
<button class="grow">Add to basket</button>
```

```css site
id: transform-practice-unit-css
site: transform-practice-unit
.grow {
  margin: 30px;
  padding: 10px 16px;
  font-size: 1rem;
  transition: transform 0.3;
}
.grow:hover {
  transform: scale(1.2);
}
```

The `transition` is on the base rule, where it should be. What is wrong
with it?

<details class="dl-answer"><summary>answer</summary>

```css
.grow {
  margin: 30px;
  padding: 10px 16px;
  font-size: 1rem;
  transition: transform 0.3s;
}
```

A time in CSS needs its unit: `0.3s` for seconds, or `300ms` for
milliseconds. `0.3` on its own does not mean anything to the browser.
When one part of a declaration is wrong, the browser ignores the whole
declaration, so the button had no transition at all. There was no
error message either. That is why a missing unit is easy to miss: the
page looks as if the line is not there.

</details>

## Make this

**4.** Build this effect in the cell below. The photo frame is there
already. Under the pointer, it should:

- turn `3` degrees anticlockwise
- grow to `1.05` times its size
- do both over `0.4s`, and go back as smoothly when the pointer
  leaves

```html site
id: transform-practice-tilt-html
site: transform-practice-tilt
<div class="photo">Sleepy Seal</div>
```

```css site
id: transform-practice-tilt-css
site: transform-practice-tilt
.photo {
  width: 160px;
  height: 120px;
  margin: 40px;
  padding: 10px;
  background: #f6f4f0;
  border: 8px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
```

Which rule does the `transition` go in: `.photo`, or `.photo:hover`?

<details class="dl-answer"><summary>answer</summary>

```css
.photo {
  width: 160px;
  height: 120px;
  margin: 40px;
  padding: 10px;
  background: #f6f4f0;
  border: 8px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.4s ease;
}
.photo:hover {
  transform: rotate(-3deg) scale(1.05);
}
```

Anticlockwise is a minus angle, so `rotate(-3deg)`. Both functions go
in one `transform` declaration. The `transition` goes in the base
`.photo` rule, so the frame settles back as smoothly as it turned.

</details>

## In your own site

**5.** Your site's buttons change colour under the pointer. Let's make
them lift a little too.

1. In your fork, open `styles.css`, and find the `.btn` rule. Look at
   its `transition` line. What does it say?
2. Find the `.btn:hover` rule, below it. Add this line inside it:

   ```css
   transform: translateY(-2px);
   ```

3. Save, and refresh your home page. Move your pointer over **Learn
   More About Me**, then away. Is the lift smooth, in both directions?
4. Try the **Send Me an Email** button in your contact section too.
   Does it lift?
5. Commit the change, with a message such as "Lift buttons on hover".

You added a `transform`, and no new `transition`. So why was the lift
smooth?

<details class="dl-answer"><summary>answer</summary>

The `.btn` rule says `transition: all var(--transition-fast);`. The
word `all` means every property that changes, so a change to
`transform` is smooth too, with no new line. `--transition-fast` is
`0.2s ease`, set near the top of the file.

The **Send Me an Email** button lifts too. It has the class `btn`, so
`.btn:hover` matches it. The `.contact-section .btn:hover` rule changes
its background and border, but it does not set a `transform`, so the
lift from `.btn:hover` still applies. The buttons can take a transform
because `.btn` sets `display: inline-block`.

Did the button's words almost disappear as it lifted? That is a small
bug in the starter. `.btn:hover` makes the text white, and
`.contact-section .btn:hover` makes the background nearly white, but
nothing sets the text back to a dark colour. Adding
`color: var(--primary-color);` to `.contact-section .btn:hover` fixes
it.

</details>
