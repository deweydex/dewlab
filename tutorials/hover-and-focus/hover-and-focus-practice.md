---
title: "Styling what the visitor points at: hover and focus — Practice"
practice_for: hover-and-focus
year: "2026-2027"
version: 2026.09.22.1
---

# Styling what the visitor points at: hover and focus — Practice

On this page we practise the two states a visitor can trigger without
typing: `:hover` under a pointer, and `:focus` from the keyboard. There
are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small design to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try each problem with the mouse and with the Tab key. Some
of these mistakes only show with one of them.

## Fix the broken page

**1.** The author of this menu did not like the ring that appeared
around a link after they clicked it. So they added the last rule.

```html site
id: hover-practice-nofocus-html
site: hover-practice-nofocus
<nav>
  <a href="#">Home</a>
  <a href="#">Shop</a>
  <a href="#">About</a>
</nav>
```

```css site
id: hover-practice-nofocus-css
site: hover-practice-nofocus
nav a {
  margin-right: 12px;
  color: #2c3e50;
}
nav a:hover {
  color: #d9720c;
}
nav a:focus {
  outline: none;
}
```

Click in the empty space below the menu, then press Tab a few times.
Can you tell which link has focus? Fix the CSS, so that a keyboard user
can always see where they are.

<details class="dl-answer"><summary>answer</summary>

```css
nav a:focus {
  outline: 3px solid #d9720c;
  outline-offset: 2px;
}
```

`outline: none` removed the browser's own focus ring, and put nothing in
its place. A mouse user sees no difference. A keyboard user presses Tab,
and nothing on the screen changes, so they cannot tell where they are.
Any outline that stands out from the page fixes it.

If the ring after a click really is a problem, `nav a:focus-visible` in
place of `nav a:focus` shows the outline after Tab, and usually not
after a click. The background page beside the tutorial has more about
`:focus-visible`.

</details>

**2.** This button should turn dark under the pointer, with white text.

```html site
id: hover-practice-space-html
site: hover-practice-space
<button class="btn">Add to basket</button>
```

```css site
id: hover-practice-space-css
site: hover-practice-space
.btn {
  padding: 10px 16px;
  border: 2px solid #2c3e50;
  border-radius: 6px;
  background: white;
  color: #2c3e50;
  font-size: 1rem;
  transition: background 0.2s ease, color 0.2s ease;
}
.btn :hover {
  background: #2c3e50;
  color: white;
}
```

Move your pointer over the button. Nothing happens. The mistake is one
character. Can you find it?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The properties in the second rule are right. So look at its
   selector.
2. Read `.btn :hover` one character at a time, and compare it with
   `.btn:hover` in the tutorial.
3. What does a space between two parts of a selector mean? We met it in
   [Choosing what to style: selectors and classes](tutorial:selectors-and-classes).

**Think about:** which element does `.btn :hover` ask about: the button,
or something inside it?

**Try this next:** what would `nav :hover` match, in the menu from
problem 1?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.btn:hover {
  background: #2c3e50;
  color: white;
}
```

A space in a selector means "inside". So `.btn :hover` matches any
element *inside* a `.btn` while the pointer is over it. This button has
no elements inside it, only text, so the rule never matched anything.
With no space, `.btn:hover` matches the button itself while the pointer
is over it.

</details>

**3.** This card should lift and grow a shadow, smoothly, under the
pointer. Move your pointer over it, slowly, then away.

```html site
id: hover-practice-snap-html
site: hover-practice-snap
<div class="card">Sleepy Seal, €18</div>
```

```css site
id: hover-practice-snap-css
site: hover-practice-snap
.card {
  width: 200px;
  margin: 30px;
  padding: 20px;
  background: #f6f4f0;
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
}
.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}
```

The shadow fades in smoothly. What does the card itself do? Why is one
change smooth, and the other not? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.card {
  width: 200px;
  margin: 30px;
  padding: 20px;
  background: #f6f4f0;
  border-radius: 8px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
```

The card jumped up and down, while its shadow faded. A `transition`
animates only the properties it names. This one named `box-shadow`
alone, so the change to `transform` happened all at once. Naming both,
with a comma between them, makes both changes smooth, in both
directions.

</details>

## Make this

**4.** Build this link, styled as a button, in the cell below:

- white text on a `#2672ad` background, with no underline
- `10px` of padding above and below the text, and `20px` at the sides
- corners rounded by `6px`
- under the pointer, the background turns `#2c3e50`, over `0.2s`, and
  turns back as smoothly
- with keyboard focus, a `3px` solid `#d9720c` outline, `3px` outside
  the link

```html site
id: hover-practice-link-html
site: hover-practice-link
<p><a href="#" class="shop">Shop now</a></p>
```

```css site
id: hover-practice-link-css
site: hover-practice-link
.shop {
  /* your rules here */
}
```

Check it with the pointer, and with Tab. Is the focus style different
from the hover style?

<details class="dl-answer"><summary>answer</summary>

```css
.shop {
  padding: 10px 20px;
  border-radius: 6px;
  background: #2672ad;
  color: white;
  text-decoration: none;
  transition: background 0.2s ease;
}
.shop:hover {
  background: #2c3e50;
}
.shop:focus {
  outline: 3px solid #d9720c;
  outline-offset: 3px;
}
```

The `transition` goes on the base `.shop` rule, not on `:hover`, so the
colour changes smoothly both ways. `outline-offset` sets the gap
between the link and its outline. The two states look different on
purpose: a keyboard user needs to see focus clearly, even while the
pointer is resting on the link.

</details>

## In your own site

**5.** In [Links to pages, other sites and
email](tutorial:three-kinds-of-link), you added a contact section to
your home page, with a **Send Me an Email** button. Let's check its
focus style.

1. Open your home page in the browser. Press Tab again and again, until
   **Send Me an Email** has focus. Can you see an outline around it?
2. In `styles.css`, find the `.btn:focus` rule. What colour is its
   outline?
3. Now find the `.contact-section` rule. What colour is the section's
   background?

Why can you not see the outline? Once you know, add a rule that gives
this one button a white outline, the same way `.main-nav a:focus` does
for the header's links. Save, refresh, and Tab to the button again.
Then commit the change, with a message such as "Show focus on the
contact button".

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `.btn:focus` sets `outline: 2px solid var(--primary-color)`.
2. `.contact-section` sets `background-color: var(--primary-color)`.
3. `outline-offset: 2px` puts the outline `2px` outside the button. What
   is behind the outline there?
4. A rule that starts with `.contact-section .btn` matches only the
   buttons in that section. Can you find two rules that start that way
   already?

**Think about:** an outline needs to stand out from what is behind it,
and not only from the button.

**Try this next:** press Tab through the rest of your site. Is there
any other place where a focus outline is hard to see?

</details>

<details class="dl-answer"><summary>answer</summary>

The outline is there, but you cannot see it. `.btn:focus` draws it in
`--primary-color`, `2px` outside the button. The contact section's
background is `--primary-color` too, so the outline is the same colour
as the background behind it.

Add this rule next to `.contact-section .btn:hover`:

```css
.contact-section .btn:focus {
    outline-color: var(--white);
}
```

`outline-color` changes only the colour, and keeps the width and style
from `.btn:focus`. When two rules set the same property, the one with
the more exact selector wins. `.contact-section .btn:focus` names the
section as well as the button, so it wins over `.btn:focus`, the same
way `.contact-section .btn:hover` already wins over `.btn:hover`.

Is this the only button with the problem? The **Learn More About Me**
button sits in the hero, and `.hero` has the same dark background. Press
Tab until it has focus: its outline is hidden too. The same fix works
there, with `.hero .btn:focus` as the selector. Buttons on a light
background keep their dark outline, which shows well.

</details>
