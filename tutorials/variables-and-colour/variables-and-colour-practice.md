---
title: "Colours, and naming them with variables — Practice"
practice_for: variables-and-colour
year: "2026-2027"
version: 2026.09.22.1
---

# Colours, and naming them with variables — Practice

On this page we practise defining a colour once, in a CSS variable, and
reading it back in several rules. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to style from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

## Fix the broken page

**1.** The header and the button should both be dark blue, with white
text. The preview looks empty.

```html site
id: colour-practice-name-html
site: colour-practice-name
<div class="header">Sleepy Seal Plushies</div>
<div class="button">Shop now</div>
```

```css site
id: colour-practice-name-css
site: colour-practice-name
:root {
  --brand-color: #2c3e50;
}
.header, .button {
  background: var(--brand-colour);
  color: white;
  padding: 12px;
  margin-bottom: 8px;
}
```

Is the text really gone? Try selecting it with the mouse. Then find the
mistake and fix it.

<details class="dl-answer"><summary>answer</summary>

```css
:root {
  --brand-color: #2c3e50;
}
.header, .button {
  background: var(--brand-color);
  color: white;
  padding: 12px;
  margin-bottom: 8px;
}
```

The variable is defined as `--brand-color`, but the rule reads
`--brand-colour`. The names must match exactly, letter for letter and
capital for capital. When `var()` finds no variable with that name, the
browser cannot use the value, so the boxes get no background at all.
The white text is still there, on a white page. That is why selecting
it with the mouse shows it.

So when a colour vanishes after an edit, check the spelling of the
name in both places: where it is defined, and where it is read.

</details>

**2.** The shop changed its brand colour to dark green, in `:root`. The
header and the button changed. The footer is still dark blue.

```html site
id: colour-practice-direct-html
site: colour-practice-direct
<div class="header">Sleepy Seal Plushies</div>
<div class="button">Shop now</div>
<div class="footer">Open every day</div>
```

```css site
id: colour-practice-direct-css
site: colour-practice-direct
:root {
  --brand-color: darkgreen;
}
.header, .button {
  background: var(--brand-color);
  color: white;
  padding: 12px;
  margin-bottom: 8px;
}
.footer {
  background: #2c3e50;
  color: white;
  padding: 12px;
}
```

Why did the footer miss the change? Fix it, so that the next change to
`--brand-color` reaches all three boxes.

<details class="dl-answer"><summary>answer</summary>

```css
.footer {
  background: var(--brand-color);
  color: white;
  padding: 12px;
}
```

The footer named its colour directly, as `#2c3e50`. It never read the
variable, so changing the variable could not reach it. Now it reads
`--brand-color` too, like the other two boxes.

When a colour refuses to change on one part of a page, this is often
the reason. That part names the colour itself, and does not read the
variable.

</details>

**3.** Here the variable is spelt the same in every place. The header
is dark green, as it should be. The button should match it, but it has
no background.

```html site
id: colour-practice-root-html
site: colour-practice-root
<div class="header">Sleepy Seal Plushies</div>
<div class="button">Shop now</div>
```

```css site
id: colour-practice-root-css
site: colour-practice-root
.header {
  --brand-color: darkgreen;
  background: var(--brand-color);
  color: white;
  padding: 12px;
  margin-bottom: 8px;
}
.button {
  background: var(--brand-color);
  color: white;
  padding: 12px;
}
```

Where is `--brand-color` defined? Which elements can read it from
there? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the tutorial's example. Which selector held the variable
   there?
2. Which element does that selector match?
3. Is the button inside the header? Or does it sit beside it?

**Think about:** a variable defined in a rule can be read by the
element that rule matches, and by the elements inside that element.

**Try this next:** move `<div class="button">` so it sits inside the
header's `<div>`, with the CSS still broken. Does the button get the
colour now?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
:root {
  --brand-color: darkgreen;
}
.header {
  background: var(--brand-color);
  color: white;
  padding: 12px;
  margin-bottom: 8px;
}
.button {
  background: var(--brand-color);
  color: white;
  padding: 12px;
}
```

The variable was defined inside the `.header` rule. A variable defined
there can be read by the header, and by the elements inside the header.
The button sits beside the header, not inside it, so it found no
variable. `:root` matches the `<html>` element, which holds every
element on the page. That is why a variable defined there reaches them
all.

And the *Try this next*? Inside the header, the button can read the
variable, so it turns dark green.

</details>

**4.** A classmate chose this bright blue for their brand colour. The
page works, but is the white text readable enough?

```html site
id: colour-practice-contrast-html
site: colour-practice-contrast
<div class="header">Sleepy Seal Plushies</div>
<div class="button">Shop now</div>
```

```css site
id: colour-practice-contrast-css
site: colour-practice-contrast
:root {
  --brand-color: #3498db;
}
.header, .button {
  background: var(--brand-color);
  color: white;
  padding: 12px;
  margin-bottom: 8px;
}
```

Put the two colours, `#ffffff` for the text and `#3498db` for the
background, into the [WebAIM contrast
checker](https://webaim.org/resources/contrastchecker/). Does the pair
pass for ordinary text? If not, choose a blue that passes, and change
one line of the CSS.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The checker shows a ratio. For ordinary text, what is the smallest
   ratio that passes?
2. White is as light as a colour can be. To make the ratio bigger,
   should the blue get lighter or darker?
3. Try `#2980b9`. It looks darker. Does it pass?

**Think about:** how many lines of CSS do we need to change, to fix
both boxes?

</details>

<details class="dl-answer"><summary>answer</summary>

White on `#3498db` gives a ratio of 3.15 to 1. Ordinary text needs
at least 4.5 to 1, so it fails. `#2980b9` looks darker, but it gives
4.3 to 1, and it still fails. Our eyes are not a good guide here,
so the checker is worth using every time.

A darker blue passes. Here is one:

```css
:root {
  --brand-color: #2672ad;
}
```

White on `#2672ad` gives 5.13 to 1. This is the blue your own site
uses for `--accent-color`. Because both boxes read the variable, one
line fixed both.

</details>

## Make this

**5.** Here is a price card. Style it with two variables:

- in `:root`, define `--ink` as `#2c3e50` and `--paper` as `#f6f4f0`
- the card has a `--paper` background and `--ink` text
- the price has an `--ink` background and `--paper` text

Every colour in the rules should come from `var()`. When it works, swap
the two values in `:root`. What happens?

```html site
id: colour-practice-card-html
site: colour-practice-card
<div class="card">
  Cuddly Cuttlefish
  <div class="price">€15</div>
</div>
```

```css site
id: colour-practice-card-css
site: colour-practice-card
.card {
  padding: 16px;
}
.price {
  padding: 8px;
  margin-top: 8px;
}
```

<details class="dl-answer"><summary>answer</summary>

```css
:root {
  --ink: #2c3e50;
  --paper: #f6f4f0;
}
.card {
  background: var(--paper);
  color: var(--ink);
  padding: 16px;
}
.price {
  background: var(--ink);
  color: var(--paper);
  padding: 8px;
  margin-top: 8px;
}
```

When we swap the two values in `:root`, the whole card turns dark, and
the price turns light. We changed two lines, and four declarations
followed them. That is the point of a variable: its name says what job
the colour does, and the value can change without touching the rules.

</details>

## In your own site

**6.** Your `styles.css` defines seven colour variables in `:root`. Is
every one of them used?

1. Open `styles.css` in your editor.
2. Use your editor's search (**Ctrl** and **F**, or **Cmd** and **F** on
   a Mac) to look for `var(--secondary-color)`. How many times is it
   read?
3. Find the `footer` rule, in section 10, Footer. It sets
   `background-color: var(--primary-color);`.
4. Change it to `background-color: var(--secondary-color);`. Save, and
   refresh. Look closely at the footer. Can you see the change?
5. Put `#ffffff` and `#34495e`, the value of `--secondary-color`, into
   the contrast checker. Does the footer's white text still pass?
6. Commit the change, with a message such as "Use the secondary colour
   for the footer".

`--text-dark` and `--primary-color` hold the same value, `#2c3e50`. Why
might a stylesheet keep two variables with the same value?

<details class="dl-answer"><summary>answer</summary>

In the starter, nothing reads `--secondary-color`. It is defined, and
waiting to be used. After step 4, the footer is a slightly lighter
blue-grey than the header. White on `#34495e` gives 9.29 to 1, so
it passes easily.

`--text-dark` is the colour of the body text. `--primary-color` is the
colour of the header, the hero and the footer. They hold the same value
now, but they do different jobs. With two variables, you can change
the colour of the header without changing the colour of every
paragraph.

</details>
