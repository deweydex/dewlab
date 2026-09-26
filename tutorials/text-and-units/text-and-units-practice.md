---
title: "Text size, units and alignment — Practice"
practice_for: text-and-units
year: "2026-2027"
version: 2026.09.22.1
---

# Text size, units and alignment — Practice

On this page we practise choosing between `px` and `rem`, and lining up
text with `text-align`. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to style from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, and its
reason, than from reading the answer.

In several problems, the first line of the CSS sets the root font size.
When we change it, we can test a page the way a reader with bigger text
would see it.

## Fix the broken page

**1.** The designer wants all the spacing on this page to grow when a
reader chooses bigger text.

```html site
id: units-practice-padding-html
site: units-practice-padding
<div class="card">Squishy Squid, €12</div>
<div class="note">Free delivery this week</div>
```

```css site
id: units-practice-padding-css
site: units-practice-padding
html { font-size: 16px; }
.card {
  padding: 1rem;
  border: 1px solid #2c3e50;
  margin-bottom: 8px;
}
.note {
  padding: 16px;
  border: 1px solid #2c3e50;
}
```

Change the first line to `32px`. Which box's space grows, and which
stays the same? Fix the one that stays the same.

<details class="dl-answer"><summary>answer</summary>

```css
.note {
  padding: 1rem;
  border: 1px solid #2c3e50;
}
```

At `16px`, the two boxes look the same, because `1rem` and `16px` are
equal there. This hides the mistake. At `32px`, `1rem` becomes
`32px`, so the card's space doubles, and the note's stays at `16px`.
With `1rem`, the note grows too.

</details>

**2.** The small print on this page should grow along with the heading,
when a reader chooses bigger text.

```html site
id: units-practice-small-html
site: units-practice-small
<h2 class="title">Sleepy Seal</h2>
<p class="small-print">Hand wash only. Keep away from fire.</p>
```

```css site
id: units-practice-small-css
site: units-practice-small
html { font-size: 16px; }
.title {
  font-size: 1.5rem;
}
.small-print {
  font-size: 12px;
}
```

Change the first line to `32px`. Does the small print grow? Fix it, so
that it is still `12px` at the default size.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. By default, how many pixels is `1rem`?
2. `12px` is what part of that? Is it more or less than `1rem`?
3. Write that part as a decimal number, followed by `rem`.

**Think about:** how can you check your answer? What should the small
print look like when the first line says `16px`?

**Try this next:** how many `rem` is `24px`? And `8px`?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.small-print {
  font-size: 0.75rem;
}
```

`12px` in `px` stays `12px` whatever the root font size is. By default,
`1rem` is `16px`, and `12` is three quarters of `16`, so we need
`0.75rem`. It is `12px` at the default size, and `24px` when the root
is `32px`.

To turn pixels into `rem`, divide by 16. So `24px` is `1.5rem`, and
`8px` is `0.5rem`.

</details>

**3.** The banner text should sit in the middle of the banner. It stays
on the left.

```html site
id: units-practice-centre-html
site: units-practice-centre
<div class="banner">Summer sale: everything half price</div>
```

```css site
id: units-practice-centre-css
site: units-practice-centre
.banner {
  background: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: centre;
}
```

Find the mistake, and fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.banner {
  background: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}
```

Values use American spelling too, so the value is `center`, not
`centre`. The browser does not know `centre`, so it skips the
declaration, and the text stays where it starts, on the left.

</details>

## Make this

**4.** Build this price tag. With the default root font size of
`16px`, it should have:

- text that is `20px` tall
- `8px` of space above and below the text, and `24px` to its left and
  right
- the text in the middle of the tag
- a `2px` solid border in `#2c3e50`

Use `rem` for the text size and for the padding. When it works, change
the first line to `32px`. Does everything grow except the border?

```html site
id: units-practice-tag-html
site: units-practice-tag
<div class="tag">Sleepy Seal, €18</div>
```

```css site
id: units-practice-tag-css
site: units-practice-tag
html { font-size: 16px; }
.tag {
  /* your rules here */
}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Divide each size by 16 to turn it into `rem`: `20`, `8` and `24`.
2. Padding with two values sets the top and bottom first, then the left
   and right.
3. Which property puts lines of text in the middle?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
html { font-size: 16px; }
.tag {
  font-size: 1.25rem;
  padding: 0.5rem 1.5rem;
  text-align: center;
  border: 2px solid #2c3e50;
}
```

At `32px`, the text and the padding double, and the border stays at
`2px`. That is often what we want. A thin line does not need to grow
for the text to stay readable.

</details>

**5.** Here is a receipt. Line up its text like this:

- the shop's name sits in the middle
- the two items stay on the left
- the total sits on the right

```html site
id: units-practice-receipt-html
site: units-practice-receipt
<div class="receipt">
  <h3>Plushie Shop</h3>
  <p>Squishy Squid, €12</p>
  <p>Sleepy Seal, €18</p>
  <p class="total">Total: €30</p>
</div>
```

```css site
id: units-practice-receipt-css
site: units-practice-receipt
.receipt {
  border: 1px solid #2c3e50;
  padding: 1rem;
}
```

<details class="dl-answer"><summary>answer</summary>

```css
.receipt {
  border: 1px solid #2c3e50;
  padding: 1rem;
}
h3 {
  text-align: center;
}
.total {
  text-align: right;
}
```

The items need no rule, because `left` is where text starts. Notice
that the heading and the total stay inside the receipt's border.
`text-align` moves the lines of text inside each element. It does not
move the elements themselves.

What happens if we put `text-align: right` on `.receipt` instead? Every
line inside it moves to the right, the heading too. Text inside an
element follows that element's `text-align`, unless a rule of its own
says something else.

</details>

## In your own site

**6.** Let's test your site the way a reader with bigger text sees it.

1. Make your browser window as wide as it goes, and open your home
   page.
2. Open your browser's settings, and set the font size to
   **Very large**. In Chrome, it is under **Settings**, then
   **Appearance**, then **Font size**. In Firefox, look under
   **Settings**, then **General**, then **Fonts**.
3. Look at your home page again. Which parts grew? Look at the
   paragraph under the main heading in the hero. How many words fit on
   each line now?
4. In `styles.css`, find the `.hero-text` rule. It sets
   `max-width: 600px`, which stops the paragraph from growing wider
   than `600px`.
5. Change it to `max-width: 37.5rem;`. Save, and refresh. How many
   words fit on each line now?
6. Set the browser's font size back to its first setting. Does the hero
   look the same as it did before step 2?
7. Commit the change, with a message such as "Let the hero text width
   grow with the font size".

<details class="dl-answer"><summary>answer</summary>

At **Very large**, the text and most of the spacing grow, because your
site uses `rem` for them. But with `max-width: 600px`, the paragraph
could not get any wider, so fewer words fit on each line. Lines of only
a few words are tiring to read.

`37.5rem` is `600` divided by `16`. At the default font size, it is
exactly `600px`, so nothing changes for most readers. At a bigger font
size it grows with the text, so each line holds about as many words as
before.

</details>
