---
title: "A form that checks itself"
year: "2026-2027"
version: 2026.11.03.1
---

# A form that checks itself

Type `mars` into the email box below, then click somewhere else on the
preview. What happens to the box?

```html site
id: signup-html
site: signup
<form>
  <label for="email">Email</label>
  <input id="email" type="email" required>

  <label for="age">Age</label>
  <input id="age" type="number" min="16" max="120" required>

  <label for="code">Mission code, three capital letters</label>
  <input id="code" pattern="[A-Z]{3}" required>

  <button>Sign up</button>
</form>
```

```css site
id: signup-css
site: signup
label {
  display: block;
  margin-top: 0.75rem;
}
input:user-invalid {
  border: 2px solid #b00020;
}
input:user-valid {
  border: 2px solid #2E7D5B;
}
form:has(:invalid) button {
  opacity: 0.5;
}
```

The box turned red, and nobody wrote a script. On this page we:

- let the browser check a form with HTML attributes
- style a field only after the visitor has used it
- see the script way, and the one check that still needs it

## Let's try it

1. Type `mars@example.ie` into the email box. What colour is it now?
2. Type `12` into the age box, then `30`.
3. Type `abc` into the mission code, then `ABC`.
4. Watch the button as you fill in the form. When does it stop looking
   faded?

## Why does this happen?

Each attribute is a rule the browser checks for us.

- `required` means the field cannot be empty.
- `type="email"` means the text must look like an email address, with an
  `@` and something after it.
- `min` and `max` set the smallest and largest number allowed.
- `pattern` gives a pattern the text must match. `[A-Z]{3}` means three
  capital letters, A to Z.

Two CSS selectors show the result. `:user-invalid` matches a field that
breaks a rule, but only after the visitor has typed in it and moved on.
`:user-valid` matches one that keeps every rule. A plain `:invalid` would
turn every empty field red the moment the page loads, before anyone had
typed a thing, which is why `:user-invalid` was added. It has worked in
every major browser since 2023.

The last rule, `form:has(:invalid) button`, fades the button while any
field in the form breaks a rule. `:has()` gets a page of its own later in
this section.

On your own site, the browser also stops the form from being sent and
shows a message beside the first field that breaks a rule. The preview
here cannot send forms, so it does not show that message.

## The script way

A browser can check each field on its own. It cannot compare two fields.
"These two passwords must match" needs a script. HTML and CSS update the preview as we type. JavaScript runs only when we press **Run** in its pane, or Ctrl+Enter inside it, so press Run first.

```html site
id: passwords-html
site: passwords
<label for="pw">Password</label>
<input id="pw" type="password" required minlength="8">
<label for="pw2">Type it again</label>
<input id="pw2" type="password" required>
```

```css site
id: passwords-css
site: passwords
label { display: block; margin-top: 0.75rem; }
input:user-invalid { border: 2px solid #b00020; }
input:user-valid { border: 2px solid #2E7D5B; }
```

```js site
id: passwords-js
site: passwords
const first = document.querySelector("#pw");
const second = document.querySelector("#pw2");
second.addEventListener("input", function () {
  if (second.value === first.value) {
    second.setCustomValidity("");
  } else {
    second.setCustomValidity("The two passwords are different.");
  }
});
```

`setCustomValidity` adds our own rule to the browser's. An empty message
means the field keeps the rule. Any other message means it breaks the
rule, and the same red border appears. So the script adds one rule, and
the browser still does everything else.

```question
id: server-checks
type: multiple-choice
answer: 3

Our form now checks every field in the browser. Does the server that
receives it still need to check the data?

- No, the browser has checked it.
  - The form cannot be sent until every rule is kept.
- Only for the password.
  - The password is the one field a script checked.
- Yes, every field.
  - Anyone can change the page or send data to the server without the
    form, so only the server's own checks protect it.
```

Checks in the browser help the visitor fix a mistake straight away.
They do not protect anything. The server checks again, every time.

## Now add your own

1. Add a field for a phone number that must be exactly 10 digits. The
   pattern `[0-9]{10}` means ten digits.
2. Change the mission code so it allows three or four capital letters.
   `{3,4}` means three or four.
3. Can you make the label of a broken field red too?
   `label:has(+ input:user-invalid)` selects a label just before one.

## What we have now

| Word | Meaning | Example |
|---|---|---|
| `required` | The field cannot be empty | `<input required>` |
| `pattern` | A pattern the text must match | `pattern="[A-Z]{3}"` |
| `min` and `max` | The smallest and largest number allowed | `min="16" max="120"` |
| `:user-invalid` | Matches a field that breaks a rule, once the visitor has used it | `input:user-invalid` |
| `setCustomValidity` | A script's way to add its own rule to a field | `field.setCustomValidity("…")` |
