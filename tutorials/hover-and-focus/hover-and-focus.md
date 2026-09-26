---
title: "Styling what the visitor points at: hover and focus"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Styling what the visitor points at: hover and focus

A button can change its look when a pointer moves over it, or when
someone reaches it with the keyboard. Each of these is a state the
button can be in. On this page we:

- style a button while a pointer is over it
- style it while it has keyboard focus
- see why the second state matters so much to people who use a keyboard

## Let's try it

Here is one button, with three rules: its normal look, its look under a
pointer, and its look with keyboard focus.

```html site
id: states-html
site: states
<button class="btn">Hover me, or Tab to me</button>
```

```css site
id: states-css
site: states
.btn {
  padding: 10px 16px;
  border: 2px solid #2c3e50;
  border-radius: 6px;
  background: #f6f4f0;
  font-size: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
}
.btn:focus {
  outline: 3px solid #d9720c;
  outline-offset: 2px;
}
```

1. Move your pointer over the button, then move it away. What changes?
   Does the change happen all at once, or bit by bit?
2. Click the button once. Then press Tab, then Shift+Tab. Tab moves
   keyboard focus forward, to the next thing you can use, and Shift+Tab
   moves it back. What do you see when focus comes back to the button?
3. Which of these two changes would a person see if they only used a
   mouse? And if they only used a keyboard?
4. What happens if we cut the `transition` line out of the `.btn` rule,
   and paste it into the `.btn:hover` rule? Is the movement smooth in
   both directions now?

## Why does this happen?

Now we can explain what we saw. Under the pointer, the button lifts and
a shadow appears beneath it. With keyboard focus, a thick orange outline
appears around it. These are two different states, and each one has its
own rule:

```css
.btn:hover { ... }   /* while a pointer is over the button */
.btn:focus { ... }   /* while the button has keyboard focus */
```

- `:hover` matches an element while a pointer sits over it.
- An element with *focus* is the one the keyboard is working with right
  now. Pressing Tab moves focus from one link or button to the next.
- `:focus` matches whichever element currently has keyboard focus,
  usually because someone pressed Tab to reach it.

In the hover rule, `transform: translateY(-4px)` moves the button up by
4 pixels. We look at `transform` properly on the next page,
[Moving things smoothly: transforms and transitions](tutorial:transitions-and-transforms).
`box-shadow` draws a shadow behind the box. Its colour here,
`rgba(0, 0, 0, 0.2)`, is black that is 80% see-through, so the shadow is
soft.

**Why was the change smooth?** The base `.btn` rule has a `transition`.
The `transition` property makes a change to another property happen
smoothly over time, instead of jumping straight to its new value. This
one says: when `transform` or `box-shadow` changes, take 0.2 seconds to
do it. The transition sits on the button's base rule, not on `:hover`
itself. This makes the change smooth in both directions, as it lifts and
as it settles back. In step 4, with the transition inside `:hover`, the
button lifted smoothly, but jumped straight back when the pointer left.

**Why does focus matter?** Some people move through a page with the
keyboard alone, pressing Tab from one link to the next. The focus style
shows them where they are. A person using a mouse may never see it at
all. This answers step 3. The lift is for the mouse, and the
outline is for the keyboard. In most browsers, clicking a button also
gives it focus, so you may have seen the outline as soon as you
clicked.

## Now in your own site

In your fork, `styles.css` has a `.card` rule. We can give your cards a
hover effect like the button's. The starter has already done half of
the work.

1. Find the `.card` rule. It already has a `transition` line:

   ```css
   transition: transform var(--transition-fast), box-shadow var(--transition-fast);
   ```

   `--transition-fast` is a variable, set near the top of the file to
   `0.2s ease`. So this is the same transition as our button's.
2. Below the `.card` rule, there is a `.card:hover` rule inside a
   comment. The comment starts with `/* → Exercise 22`. Delete that
   first line of the comment, and the `*/` line after the rule. The
   rule should now look like this:

   ```css
   .card:hover {
       transform: translateY(-5px);
       box-shadow: var(--shadow-lg);
   }
   ```

   `--shadow-lg` is a larger, deeper shadow than the card's own
   `--shadow-md`.
3. Save, and refresh. Move your pointer over a card. What happens?
4. Now find the `a:focus` rule in `styles.css`.
5. Go back to your page and press Tab several times. Where does the
   outline go each time?
6. The very first press of Tab lands on a hidden "Skip to main content"
   link. Look for `.skip-link` in the CSS to see how it stays hidden
   until it has focus.

Can you reach every link on your page with Tab alone, and see the
outline on each one?

## What we have now

We can now style two states a visitor can trigger without typing any
text: one with a pointer, and one with the keyboard.

| Word | Meaning | Example |
|---|---|---|
| `:hover` | Matches an element while a pointer sits over it | `.card:hover` |
| *focus* | An element with focus is the one the keyboard is working with. Tab moves it to the next link or button. | |
| `:focus` | Matches whichever element currently has keyboard focus | `a:focus` |
| `transition` | Makes a change to another property happen smoothly over time. We put it on the base rule, not the state that triggers the change, so it works in both directions. | `transition: transform 0.2s ease;` |
