---
title: "Changing the order of boxes on screen"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    touches: [WA-LO9]
---

# Changing the order of boxes on screen

Can a box appear first on screen when it comes last in the HTML? CSS can
do that. But the keyboard, and a screen reader, may not agree with what
we see. On this page we:

- move one box in a row with the `order` property
- press Tab, and follow where the keyboard goes
- decide when to use `order`, and when to change the HTML

## Let's try it

The HTML has three links in a row. The CSS makes the row a flex
container, and gives the third link, the nautilus, an `order` of its
own. The last rule draws an orange outline on whichever link has
keyboard focus.

```html site
id: order-html
site: order
<div class="row">
  <a href="#" class="item squid">Squid</a>
  <a href="#" class="item cuttlefish">Cuttlefish</a>
  <a href="#" class="item nautilus">Nautilus</a>
</div>
```

```css site
id: order-css
site: order
.row {
  display: flex;
  gap: 12px;
}
.item {
  padding: 12px 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
  color: #2c3e50;
  font-family: sans-serif;
}
.nautilus {
  order: -1;
}
.item:focus {
  outline: 3px solid #d9720c;
  outline-offset: 2px;
}
```

1. Read the HTML. In what order do the three links come? Now look at
   the preview. Which link is first on screen?
2. Click an empty part of the preview, below the links. Then press Tab
   three times, slowly. Which link gets the orange outline first? Which
   gets it next?
3. What happens if we change `order: -1` to `order: 1`?
4. What happens with `order: 0`?
5. With the nautilus back at `order: -1`, what if we add `order: -2`
   to a new `.cuttlefish` rule?

## Why does this happen?

Now we can explain what we saw. On screen, the nautilus came first. But
Tab went to the squid first, then the cuttlefish, and the nautilus
last, as if the CSS were not there.

`order` sets where a flex item sits in its row, on screen. It takes a
whole number, which may be negative. The browser lines the items up
from the smallest number to the largest.

- Every item starts at `order: 0`. So in step 3, `1` put the nautilus
  after the other two.
- Items with the same number keep the order they have in the HTML. So
  in step 4, `0` put the nautilus back at the end, where the HTML has
  it.
- In step 5, `-2` is smaller than `-1`, so the cuttlefish went in front
  of the nautilus.

The order of the elements in the HTML file is the *source order*.
`order` changes what we see, and nothing else. The source order stays
the same. The Tab key follows the source order, and so does a screen
reader, which reads the page aloud from the HTML. So in step 2, Tab
jumped from the squid to the cuttlefish, and then back to the left, to
the nautilus.

![Two views of the same three links. On the left, the source order, as the HTML lists them: 1 Squid, 2 Cuttlefish, 3 Nautilus. On the right, the row on screen, with order: -1 on the nautilus: Nautilus, Squid, Cuttlefish. Numbered arrows show where Tab goes on screen: first to Squid, second to Cuttlefish, and third back to Nautilus at the far left.](order-and-tab.svg)

For someone who sees the screen and moves with the keyboard, focus that
jumps back like this is confusing. For someone who hears the page, the
spoken order and the screen order no longer match. So we use `order`
for small changes of look, where the order does not change the meaning.
When the order matters, such as steps in a list, or the links in a
menu, we change the source order instead, in the HTML. Then the screen,
the keyboard and the screen reader all agree.

`order` works on grid items too. A grid map can do the same thing. On
[Laying out a page with grid areas](tutorial:named-grid-areas), we
swapped `"nav main"` for `"main nav"`, and the menu moved to the other
side of the page. The source order did not change, so the same care
applies.

Oftentimes a design wants a different order on a phone. For example, a
shop might show a product's price above its photo on a narrow screen,
and beside it on a wide one. An `order` inside a media query can do
that, and it is a fair use, because both orders make sense to a reader.

## Now in your own site

Your header is a flex container too. The `.header-content` rule sets
`display: flex`, with the logo on the left and the menu on the right.

1. Open your fork, and open `styles.css`.
2. Find the `.main-nav ul` rule. Just above it, add a new rule:
   `.main-nav { order: -1; }`
3. Save, and open `index.html` in your browser, in a wide window.
   Where is the menu now? Where is the logo?
4. Refresh the page, and press Tab a few times. The first press shows
   the "Skip to main content" link. Where does the outline go after
   that: to the menu on the left, or to the logo on the right?
5. Delete the rule you added, and save. Your menu goes back to the
   right.

Could you explain to someone why Tab went where it did in step 4?

## What we have now

We can now move a box on screen with `order`, and we know that the
keyboard and screen readers still follow the HTML.

| Word | Meaning | Example |
|---|---|---|
| `order` | Sets where a flex or grid item sits on screen. Smaller numbers come first. Every item starts at `0`. | `order: -1;` |
| *source order* | The order of the elements in the HTML. Tab and screen readers follow it, whatever the CSS shows. | squid, cuttlefish, nautilus |
