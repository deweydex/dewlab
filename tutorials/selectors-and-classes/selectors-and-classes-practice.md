---
title: "Choosing what to style: selectors and classes — Practice"
practice_for: selectors-and-classes
year: "2026-2027"
version: 2026.09.22.1
---

# Choosing what to style: selectors and classes — Practice

On this page we practise picking out exactly the elements we mean, with
class selectors and descendant selectors. There are three kinds of
problem:

- a broken page, where we find the mistake and fix it
- a small page to style from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, and its
reason, than from reading the answer.

## Fix the broken page

**1.** The paragraph inside the highlighted box should be red and bold.
Nothing on the page is styled.

```html site
id: selectors-practice-dot-html
site: selectors-practice-dot
<div class="highlight">
  <p>Inside the highlighted box.</p>
</div>
<p>Outside it.</p>
```

```css site
id: selectors-practice-dot-css
site: selectors-practice-dot
highlight p {
  color: firebrick;
  font-weight: bold;
}
```

Compare the selector with the one in the tutorial. What is missing?

<details class="dl-answer"><summary>answer</summary>

```css
.highlight p {
  color: firebrick;
  font-weight: bold;
}
```

The dot was missing. Without it, `highlight` is a tag name, so
`highlight p` looks for a paragraph inside an element called
`<highlight>`. There is no such element in HTML, so the rule matched
nothing. The dot is what makes `.highlight` mean "an element with
`class="highlight"`".

</details>

**2.** The sale item should be red and bold. Nothing changes.

```html site
id: selectors-practice-space-html
site: selectors-practice-space
<p class="sale">Squishy Squid, now €9</p>
<p>Sleepy Seal, €18</p>
```

```css site
id: selectors-practice-space-css
site: selectors-practice-space
.sale p {
  color: firebrick;
  font-weight: bold;
}
```

Which element carries the class `sale`? And what does the selector
`.sale p` look for? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the selector out loud: "a `p` that is somewhere inside an
   element with the class `sale`".
2. Now look at the HTML. Is there a `p` inside the element with the
   class `sale`?
3. Where is the class instead?

**Think about:** what does the space in the middle of a selector mean?

**Try this next:** what does `p.sale`, with no space, match?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.sale {
  color: firebrick;
  font-weight: bold;
}
```

The class is on the paragraph itself. `.sale p` is a descendant
selector, so it looks for a paragraph *inside* an element with the
class `sale`. That paragraph has nothing inside it but text, so the
rule matched nothing. `.sale` on its own matches the paragraph that
carries the class.

And the *Try this next*? `p.sale`, with no space, means a `<p>` that
carries the class `sale` itself. It works here too. The space changes
the meaning completely: `p.sale` and `.sale p` are two different
selectors.

</details>

**3.** The featured plushie should have a thick border. It has none.

```html site
id: selectors-practice-case-html
site: selectors-practice-case
<div class="Featured">Cuddly Cuttlefish</div>
<div>Sleepy Seal</div>
```

```css site
id: selectors-practice-case-css
site: selectors-practice-case
.featured {
  border: 4px solid #2c3e50;
  padding: 1rem;
}
```

The dot is there, and there is no space. What else can make a class
selector miss? Fix it, and change only one character.

<details class="dl-answer"><summary>answer</summary>

```html
<div class="featured">Cuddly Cuttlefish</div>
<div>Sleepy Seal</div>
```

The HTML says `Featured`, with a capital `F`, and the CSS says
`featured`. Class names must match exactly, capital letters included.
Changing the selector to `.Featured` works too. Most people write class
names all in small letters, with a dash between words, like
`skills-section`. Then there is nothing to remember.

</details>

## Make this

**4.** Here is a menu, and a note under it. Make the prices in the menu
bold and firebrick red. Leave the price in the note as it is.

```html site
id: selectors-practice-menu-html
site: selectors-practice-menu
<div class="menu">
  <p>Squishy Squid <span class="price">€12</span></p>
  <p>Sleepy Seal <span class="price">€18</span></p>
</div>
<p class="note">Delivery costs <span class="price">€4</span>.</p>
```

```css site
id: selectors-practice-menu-css
site: selectors-practice-menu
/* your rule here */
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. All three prices carry the class `price`. What would `.price` on its
   own match?
2. What do the two prices in the menu have that the third one does not?
3. Which kind of selector matches an element only when it sits inside
   another one?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.menu .price {
  color: firebrick;
  font-weight: bold;
}
```

`.price` on its own would match all three prices. `.menu .price`
matches a price only when it sits somewhere inside the element with the
class `menu`. The price in the note is outside the menu, so it stays as
it is. Notice that the prices sit two levels down, inside a `<p>` inside
the menu. A descendant selector matches at any depth.

</details>

**5.** These three cards share one rule. Make the middle card stand
out, with a `4px` solid `firebrick` border on its left side.

Do not remove the class `card`, and do not change the `.card` rule. Can
you give the middle card a second class, and write a rule for that
class?

```html site
id: selectors-practice-two-html
site: selectors-practice-two
<div class="card">Squishy Squid</div>
<div class="card">Cuddly Cuttlefish</div>
<div class="card">Sleepy Seal</div>
```

```css site
id: selectors-practice-two-css
site: selectors-practice-two
.card {
  background: #f6f4f0;
  padding: 1rem;
  margin-bottom: 8px;
}
```

<details class="dl-answer"><summary>answer</summary>

```html
<div class="card">Squishy Squid</div>
<div class="card featured">Cuddly Cuttlefish</div>
<div class="card">Sleepy Seal</div>
```

```css
.card {
  background: #f6f4f0;
  padding: 1rem;
  margin-bottom: 8px;
}
.featured {
  border-left: 4px solid firebrick;
}
```

Any class name works, as long as the HTML and the CSS match. The middle
card now carries two classes, with a space between them. It matches
both `.card` and `.featured`, so it gets the background and padding
from one rule, and the border from the other.

</details>

## In your own site

**6.** The headings on your About page should use your accent colour.
The headings on your home page should stay as they are.

1. Open `about.html`. The headings "My Background", "Why Web
   Development?" and "My Goals" are `<h2>` elements. Which element are
   they inside? Look for a `class` on it.
2. Open `styles.css`, and find section 9, About Page. Is there already
   a rule whose selector matches those headings?
3. Add `color: var(--accent-color);` to that rule. Save, and refresh
   `about.html`, then `index.html`.
4. Commit the change, with a message such as "Accent colour for About
   page headings".

Why did the headings on the home page stay the same? And which `<h2>`
on the About page did not change?

<details class="dl-answer"><summary>answer</summary>

The headings sit inside `<article class="about-content">`. Section 9
already has a rule for them, `.about-content h2`, which sets their
`margin-top`. After step 3 it reads:

```css
.about-content h2 {
    margin-top: var(--spacing-lg);
    color: var(--accent-color);
}
```

`.about-content h2` is a descendant selector. It matches an `<h2>` only
when it sits inside an element with the class `about-content`. Your
home page has no element with that class, so its headings stay as they
were. On the About page, the heading "Want to See My Work?" sits in a
different section, outside the article, so it does not change either.

</details>
