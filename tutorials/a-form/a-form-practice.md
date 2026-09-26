---
title: "A contact form — Practice"
practice_for: a-form
year: "2026-2027"
version: 2026.09.22.1
---

# A contact form — Practice

On this page we practise joining a label to its field. A `<label>`'s
`for` attribute names the `id` of its field, and the two must match
exactly. There are three kinds of problem:

- a broken form, where we find the mistake and fix it
- a small form to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. The quickest test for every problem here is the same one:
click the label. Does the right field get focus?

## Fix the broken page

**1.** Click the word "Email". Nothing happens.

```html site
id: form-practice-case-html
site: form-practice-case
<label for="Email">Email</label>
<input type="email" id="email" name="email">
```

```css site
id: form-practice-case-css
site: form-practice-case
label { display: block; margin-bottom: 4px; font-weight: bold; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
input:focus { outline: 3px solid #0066cc; }
```

Compare the `for` and the `id`, letter by letter. Fix it.

<details class="dl-answer"><summary>answer</summary>

```html
<label for="email">Email</label>
<input type="email" id="email" name="email">
```

`for="Email"` has a capital E, and `id="email"` does not. An `id` must
match exactly, capitals included, so the label named a field that does
not exist. Many people write every `id` in small letters, so there is
one less thing to check.

</details>

**2.** This form has two fields. Click the word "Town". Which field gets
focus?

```html site
id: form-practice-copy-html
site: form-practice-copy
<p>
  <label for="name">Name</label>
  <input type="text" id="name" name="name">
</p>
<p>
  <label for="name">Town</label>
  <input type="text" id="name" name="town">
</p>
```

```css site
id: form-practice-copy-css
site: form-practice-copy
label { display: block; margin-bottom: 4px; font-weight: bold; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
input:focus { outline: 3px solid #0066cc; }
```

The author made the second field by copying the first. What did they
forget to change? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the second field's `<label>` and `<input>`. Which of their
   attributes still say `name`?
2. Which of those were changed to suit the new field, and which were
   not?
3. How many elements on the page have `id="name"`?

**Think about:** an `id` must be unique on the page. When two elements
share one, which one does the label find?

**Try this next:** once it works, add a third field, "Phone", with
`type="tel"`. Click its label to check it.

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<p>
  <label for="name">Name</label>
  <input type="text" id="name" name="name">
</p>
<p>
  <label for="town">Town</label>
  <input type="text" id="town" name="town">
</p>
```

The author changed the `name` attribute to `town`, but left the `for`
and the `id` as `name`. Two elements then had `id="name"`. An `id` must
be unique on a page. When two elements share one, the browser uses the
first, so the "Town" label focused the Name field.

</details>

**3.** Click the word "Message". Nothing happens.

```html site
id: form-practice-name-html
site: form-practice-name
<label for="message">Message</label>
<textarea id="msg" name="message" rows="4"></textarea>
```

```css site
id: form-practice-name-css
site: form-practice-name
label { display: block; margin-bottom: 4px; font-weight: bold; }
textarea { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
textarea:focus { outline: 3px solid #0066cc; }
```

The word `message` is in the label and in the field. Why is the label
still not joined to the field? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The field has two attributes that look alike: `id` and `name`. What
   is each one set to?
2. Which of the two does a label's `for` look for?

**Think about:** the `name` attribute has a different job. It names the
answer when the form is sent. Does a label ever read it?

**Try this next:** what else could we change, instead of the `for`, to
fix it?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<label for="msg">Message</label>
<textarea id="msg" name="message" rows="4"></textarea>
```

A label's `for` names a field's `id`, and never its `name`. Here the
`id` was `msg`, so `for="message"` found nothing. We could also change
the `id` to `message`. The `name` can stay as it is. It names the answer
when the form is sent, and the label never reads it.

</details>

## Make this

**4.** Add a checkbox to this form, with the label "Send me the
newsletter". A *checkbox* is a small box a visitor ticks or unticks,
written `<input type="checkbox">`. Clicking the words of its label
should tick the box, and clicking again should untick it.

```html site
id: form-practice-tick-html
site: form-practice-tick
<form>
  <label for="email">Email</label>
  <input type="email" id="email" name="email">
  <!-- your checkbox here -->
</form>
```

```css site
id: form-practice-tick-css
site: form-practice-tick
label { display: block; margin-bottom: 4px; font-weight: bold; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The checkbox is an `<input>` with `type="checkbox"`, an `id` and a
   `name`.
2. The label is a `<label>` whose `for` matches that `id`.
3. A checkbox usually comes before its label, on the same line.

**Think about:** why does a bigger thing to click help a visitor on a
phone?

**Try this next:** the label sits on a line of its own, because the CSS
says `display: block` for every label. How could we keep the checkbox's
label on the same line as the box?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<form>
  <label for="email">Email</label>
  <input type="email" id="email" name="email">
  <p>
    <input type="checkbox" id="news" name="news">
    <label for="news">Send me the newsletter</label>
  </p>
</form>
```

The `for` and the `id` match, so the label is joined to the checkbox.
Clicking the words ticks the box, the same way clicking a text field's
label gives it focus. That makes a much bigger target than the box
alone. In this cell, the words sit on the line under the box, because
every label has `display: block`. A rule for this one label, such as
`label[for="news"] { display: inline; }`, keeps it on the same line.

</details>

## In your own site

**5.** In your fork of `project_wad`, `contact.html` has a form with
three fields: Name, Email and Message. Add a fourth field for a subject
line.

1. Open `contact.html`. Find the `<div class="form-row">` around the
   Email field.
2. Copy that whole `<div>`, and paste the copy after it.
3. In the copy, change the label's text to "Subject". Change the
   `for`, the `id` and the `name` to `subject`. Change `type` to
   `text`.
4. Decide whether a subject is `required`. Keep or remove it.
5. Save, and open the page in your browser. Click each label in turn.
6. Commit the change, with a message such as "Add a subject field to
   the contact form".

Does each label give focus to its own field? Now leave the Name field
empty and press **Send**. What does the browser do?

<details class="dl-answer"><summary>answer</summary>

The new row looks like this:

```html
<div class="form-row">
    <label for="subject">Subject</label>
    <input type="text" id="subject" name="subject">
</div>
```

The `for`, the `id` and the `name` all changed, so this is not the
mistake from problem 2. When a `required` field is empty and we press
**Send**, the browser stops the form, and shows a short message beside
that field. Your form has no server behind it to receive the answers.
So when every field is filled in, the page loads again, with the
answers added to the end of its address, and nothing keeps them.

</details>
