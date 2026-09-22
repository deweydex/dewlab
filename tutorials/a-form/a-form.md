---
title: "A contact form"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    touches: [WA-LO2, WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO8, WA-LO10]
---

# A contact form

A form field needs a name, so a visitor knows what to type. How do we
join a name to its field?

## Let's try it

Here is one form field, with the word "Email" above it.

```html site
id: form-demo-html
site: form-demo
<label for="email">Email</label>
<input type="email" id="email" name="email">
```

```css site
id: form-demo-css
site: form-demo
label { display: block; margin-bottom: 4px; font-weight: bold; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
input:focus { outline: 3px solid #0066cc; }
```

1. Click inside the box. What appears around it?
2. Click elsewhere, then click the word "Email". What happens?
3. What if we change `for="email"` to `for="mail"`, and click the word
   again?

## Why does this happen?

Now we can explain what we saw. A *label* is the name of a form field,
written with `<label>`. Its `for` attribute names the `id` of its field.
This connection does two things:

- Clicking the label gives the field focus. That is the blue outline we
  saw in step 2.
- A screen reader reads the label aloud when the field gets focus.
  Without a label, it may say only "edit text".

In step 3, `for` named a missing `id`, so clicking the label did
nothing. This mistake is common: one letter differs between
`for` and `id`. Capitals count too: `Email` and `email`
differ.

`type="email"` says the field expects an email address. A phone then
shows a keyboard with `@` easy to reach. The browser also checks that
the text has roughly the right shape before the form submits.

## Now in your own site

1. In your fork of `project_wad`, open `contact.html` in your editor.
   The `required` attribute is on all three fields. It stops the form
   submitting while any of them is empty.
2. Open the same page in the browser.
3. Click each label in turn. Does focus land on the right field each
   time? If so, each `for` matches its field's `id`.

## What we have now

We can now give every field a name that a person and a screen reader
can both use.

| Word | Meaning | Example |
|---|---|---|
| *label* | The name of a form field. Its `for` names the field's `id`. | `<label for="email">Email</label>` |
| `type="email"` | Gives a phone a keyboard for addresses, and a basic shape check | `<input type="email">` |
| `required` | Stops a form submitting while the field is empty | `<input required>` |
