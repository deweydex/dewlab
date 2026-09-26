---
title: "Opening and closing content with a checkbox — Practice"
practice_for: the-checkbox-hack
year: "2026-2027"
version: 2026.09.22.1
---

# Opening and closing content with a checkbox — Practice

On this page we practise the checkbox hack: a hidden checkbox, a label
linked to it with `for`, and a `:checked ~` rule that shows content
while the box is ticked. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small design to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Each part of the checkbox hack has to be exactly right, or
nothing opens. So when a question will not open, check the parts one at
a time.

## Fix the broken page

**1.** Click the question. The answer should open.

```html site
id: checkbox-practice-for-html
site: checkbox-practice-for
<input type="checkbox" id="delivery" class="toggle">
<label for="delivery-info" class="toggle-label">How long does delivery take?</label>
<div class="toggle-content">
  <p>Two to four working days, anywhere in Ireland.</p>
</div>
```

```css site
id: checkbox-practice-for-css
site: checkbox-practice-for
.toggle {
  display: none;
}
.toggle-label {
  display: block;
  padding: 10px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  cursor: pointer;
}
.toggle-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.toggle:checked ~ .toggle-content {
  max-height: 200px;
}
```

The CSS is the same as the tutorial's. So the mistake is in the HTML.
What is it?

<details class="dl-answer"><summary>answer</summary>

```html
<input type="checkbox" id="delivery" class="toggle">
<label for="delivery" class="toggle-label">How long does delivery take?</label>
<div class="toggle-content">
  <p>Two to four working days, anywhere in Ireland.</p>
</div>
```

The label's `for` must match the checkbox's `id` exactly. Here the
label said `delivery-info`, and no element has that `id`. So a click on
the label ticked nothing, and the answer stayed closed. With
`for="delivery"`, the click reaches the hidden checkbox.

</details>

**2.** The author thought the checkbox would be tidier at the end, out
of the way. Now the answer never opens.

```html site
id: checkbox-practice-order-html
site: checkbox-practice-order
<label for="wash" class="toggle-label">Can I wash my plushie?</label>
<div class="toggle-content">
  <p>Yes. Every plushie can go in the washing machine, on a cool wash.</p>
</div>
<input type="checkbox" id="wash" class="toggle">
```

```css site
id: checkbox-practice-order-css
site: checkbox-practice-order
.toggle {
  display: none;
}
.toggle-label {
  display: block;
  padding: 10px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  cursor: pointer;
}
.toggle-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.toggle:checked ~ .toggle-content {
  max-height: 200px;
}
```

The `for` and the `id` match this time. So what stops it opening?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Does the click still tick the checkbox? Delete `display: none;` for a
   moment, and click the question to see.
2. Read the rule `.toggle:checked ~ .toggle-content` again. What does
   `~` select?
3. Where is the checkbox now, compared with the answer?

**Think about:** `~` only looks one way along the elements that share a
parent. Which way?

**Try this next:** would the answer open if the checkbox sat between
the label and the answer?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<input type="checkbox" id="wash" class="toggle">
<label for="wash" class="toggle-label">Can I wash my plushie?</label>
<div class="toggle-content">
  <p>Yes. Every plushie can go in the washing machine, on a cool wash.</p>
</div>
```

The click did tick the checkbox. But `~` selects only elements that
come *after* this one, and the answer came before the checkbox. So the
`:checked ~` rule found nothing to open. With the checkbox back at the
start, the answer comes after it again. The checkbox is hidden, so its
place in the HTML makes no difference to how the page looks.

</details>

**3.** This question opens, but look at the end of its answer.

```html site
id: checkbox-practice-cut-html
site: checkbox-practice-cut
<input type="checkbox" id="returns" class="toggle">
<label for="returns" class="toggle-label">Can I send a plushie back?</label>
<div class="toggle-content">
  <p>Yes, within thirty days. Keep the label on, and put the plushie
  back in its box. Then fill in the form that came with your order, and
  post the box to us. We send your money back as soon as the plushie
  arrives, and we pay for the post.</p>
</div>
```

```css site
id: checkbox-practice-cut-css
site: checkbox-practice-cut
.toggle {
  display: none;
}
.toggle-label {
  display: block;
  padding: 10px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  cursor: pointer;
}
.toggle-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.toggle:checked ~ .toggle-content {
  max-height: 60px;
}
```

Where does the answer stop? Drag the **Preview width** slider to
narrow the preview. Does more of it go missing? Fix it, and keep the
answer's slide.

<details class="dl-answer"><summary>answer</summary>

```css
.toggle:checked ~ .toggle-content {
  max-height: 300px;
}
```

The open answer can grow only as tall as its `max-height`, and
`overflow: hidden` hides everything below that. Here `60px` was shorter
than the answer, and in a narrow preview the answer is taller still,
because its lines wrap. A larger number fixes it. The answer is still
only as tall as its own content, because `max-height` is a limit, and
not a height.

Why not `height: auto`? A transition cannot animate a change to `auto`,
so the answer would snap open with no slide. So the checkbox hack uses
`max-height`, with a number larger than the answer will ever
need.

</details>

## Make this

**4.** Build a "show more" link in the cell below, with the checkbox
hack. The checkbox and the label are there already.

- the list of ingredients is hidden at first
- clicking **Show the ingredients** shows it, and clicking again hides
  it
- the checkbox itself is never seen
- there is no slide: the list appears at once

```html site
id: checkbox-practice-more-html
site: checkbox-practice-more
<input type="checkbox" id="more" class="more-toggle">
<label for="more" class="more-label">Show the ingredients</label>
<ul class="more-list">
  <li>Soft cotton cover</li>
  <li>Recycled stuffing</li>
  <li>Two stitched eyes</li>
</ul>
```

```css site
id: checkbox-practice-more-css
site: checkbox-practice-more
.more-label {
  color: #2672ad;
  text-decoration: underline;
  cursor: pointer;
}
```

With no slide, do you still need `max-height`? What could you use
instead?

<details class="dl-answer"><summary>answer</summary>

```css
.more-toggle {
  display: none;
}
.more-label {
  color: #2672ad;
  text-decoration: underline;
  cursor: pointer;
}
.more-list {
  display: none;
}
.more-toggle:checked ~ .more-list {
  display: block;
}
```

With no slide, we do not need `max-height` or `overflow`. `display:
none` hides the list completely, and `display: block` shows it again at
its own full height. The list comes after the checkbox, and shares its
parent, so `~` can reach it.

</details>

## In your own site

**5.** Let's add a question that opens to your About page, and then
make sure a keyboard can open it too.

1. In your fork, open `about.html`. Find the paragraph under the
   heading "My Goals". After that paragraph, and before `</article>`,
   add this:

   ```html
   <div class="question">
       <input type="checkbox" id="goal-question" class="toggle">
       <label for="goal-question" class="toggle-label">What am I building next?</label>
       <div class="toggle-content">
           <p>Write your own answer here.</p>
       </div>
   </div>
   ```

2. Write your own question and answer in place of the examples.
3. In `styles.css`, find the section called About Page. At the end of
   that section, add these rules:

   ```css
   .toggle {
       display: none;
   }

   .toggle-label {
       display: block;
       padding: var(--spacing-sm);
       background-color: var(--light-gray);
       border-radius: var(--radius-sm);
       cursor: pointer;
   }

   .toggle-content {
       max-height: 0;
       overflow: hidden;
       transition: max-height var(--transition-normal);
   }

   .toggle:checked ~ .toggle-content {
       max-height: 200px;
   }
   ```

4. Save, and refresh your About page. Click your question. Does it
   open?
5. Now refresh again, and press Tab, again and again, until you reach
   **View Portfolio**. Did focus stop at your question on the way?

It did not. Can you change the `.toggle` rule, so that the checkbox is
still invisible, but Tab can reach it? Your site already hides one
thing that way. When the checkbox has focus, the label should get an
outline, so a keyboard user can see where they are. When it works,
commit the change, with a message such as "Add a question to the About
page".

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `display: none` removes the checkbox from the Tab key completely. We
   need a way to hide it that keeps it on the page.
2. Look at the `.skip-link` rule in `styles.css`. The skip link is
   invisible, and yet Tab reaches it. Which properties does that rule
   use to hide it?
3. The checkbox comes before its label, and they share a parent. Which
   symbol in a selector reaches from the checkbox to the label?

**Think about:** while the checkbox has focus, which element does the
person need to see an outline on: the invisible checkbox, or the label?

**Try this next:** once the question has focus, which key ticks the
checkbox?

</details>

<details class="dl-answer"><summary>answer</summary>

Replace the `.toggle` rule with these two rules:

```css
.toggle {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    white-space: nowrap;
}

.toggle:focus ~ .toggle-label {
    outline: 2px solid var(--accent-color);
    outline-offset: 2px;
}
```

The first rule hides the checkbox the same way `.skip-link` hides the
skip link. The checkbox is one pixel in size, and `clip` hides even
that one pixel, but it is still on the page. So Tab stops at it now,
between **Contact** in the header and **View Portfolio**.

The second rule gives the label an outline while the checkbox has
focus. The label comes after the checkbox and shares its parent, so
`~` reaches it, the same way it reaches the answer.

With focus on the question, press Space. Space ticks and unticks a
checkbox, so the answer opens and closes from the keyboard. HTML also
has an element built for a question that opens, `<details>`, which
does all of this with no CSS. The background page beside the tutorial
shows it.

</details>
