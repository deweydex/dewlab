---
title: "A form"
slug: a-form
module: web
module_title: "Web authoring"
series: several-pages
version: 2026.09.05.1
---

# A form

Click directly on the word "Email" below, not the box beside it. The
input gains focus anyway, with the same blue outline a click on the box
itself would give it.

```html site=form-demo
<label for="email">Email</label>
<input type="email" id="email" name="email">
```

```css site=form-demo
label { display: block; margin-bottom: 4px; font-weight: bold; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
input:focus { outline: 3px solid #0066cc; }
```

## Why this happens

`for="email"` on the `<label>` names the `id` of the field it belongs to.
That connection does two things at once. Clicking the label text focuses
the input, the way you just saw. A screen reader also reads the label's
words aloud the moment that input gets focus, rather than saying nothing
more than "edit text."

`type="email"` changes more than what the field is called. A phone shows
a keyboard suited to typing an address, with `@` easy to reach. The
browser also checks the text has roughly the right shape before letting
the form submit.

## Your turn

Let's open your fork of `project_wad` and its `contact.html`. Try
clicking each label and watching focus land on the right field — that
confirms every field has a `<label>` whose `for` matches its input's
`id`. The `required` attribute is already on all three fields, which
stops the form submitting with any of them empty.

## What you have now

A form where every field has a name a person and a screen reader can
both use.

- **`<label for="…">`** — names which field a label belongs to, matching
  the field's `id`.
- **`type="email"`** — a phone-friendly keyboard, and a basic shape
  check.
- **`required`** — stops a form submitting while the field is empty.
