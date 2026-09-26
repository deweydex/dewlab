---
title: "What happens when a form is sent"
year: "2026-2027"
version: 2026.09.22.1
context_for: [a-form]
---

# What happens when a form is sent

A visitor fills in your contact form and presses **Send**. What does
the browser send, and where does it go? This page follows a form's
answers out of the page. It is background reading for [A contact
form](tutorial:a-form). You do not need it to finish that page, but it
explains what your form would need to work for real.

On this page we:

- see what a browser sends when a form is sent
- see where the answers go, and what has to be there to receive them
- see why a check in the browser is not enough on its own
- meet one more way to join a label to its field

## Every answer needs a name

Here is a small form. A form in a preview on this site cannot be sent
anywhere, so a short script stands in for the **Send** button. It
shows, below the form, what the browser would send. You do not need to
read the script. This editor has a third pane: JavaScript only runs
when you press **Run** in its pane, or Ctrl+Enter inside it. Press it
once before you start.

```html site
id: form-sent-html
site: form-sent
<form>
  <label for="name">Name</label>
  <input type="text" id="name" name="name">
  <label for="email">Email</label>
  <input type="email" id="email" name="email">
  <button type="button" id="show">Show what would be sent</button>
</form>
<p>Sent: <code id="sent"></code></p>
```

```css site
id: form-sent-css
site: form-sent
label { display: block; margin-top: 8px; font-weight: bold; }
input { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
button { display: block; margin-top: 12px; padding: 6px 12px; }
code { background: #f6f4f0; padding: 2px 4px; }
```

```js site
id: form-sent-js
site: form-sent
const form = document.querySelector("form");
const sent = document.querySelector("#sent");
document.querySelector("#show").addEventListener("click", () => {
  const answers = new URLSearchParams(new FormData(form));
  sent.textContent = answers.toString();
});
```

1. Type a name and an email address, and press the button. What
   appears after "Sent:"?
2. Where does each part of it come from? Compare it with the HTML.
3. Delete `name="email"` from the second `<input>`. Type the address
   again, and press the button. What changes?
4. Put `name="email"` back. What happens to a space in the name, or to
   the `@` in the address?

Now we can explain what we saw. When a form is sent, the browser
collects every field that has a `name`. For each one, it makes a
*name/value pair*: the field's `name`, an `=`, and what the visitor
typed. It joins the pairs with `&`. In step 1 that looked something
like this:

```text
name=Ana+Murphy&email=ana%40example.com
```

The `name` attribute is the label on each answer, for whoever receives
it. A field with no `name` is not sent at all, as we saw in step 3,
however much the visitor typed into it. So a form field needs an `id`
for its label, and a `name` for its answer. The two often have the same
value, as they do in your own contact form, but they do different jobs.

In step 4, some characters changed. A space became `+`, and `@` became
`%40`. Characters such as `&` and `=` have a job in the list itself, so
the browser writes them, and a few others, as a `%` and a code. The
program that receives the answers turns them back.

## Where the answers go

Two attributes on the `<form>` element say where the answers go, and
how:

```html
<form action="https://example.com/contact" method="post">
```

- `action` is the address the answers are sent to. With no `action`,
  the browser sends them to the address of the page the form is on.
- `method` says how they travel. With `method="get"`, the default, the
  answers go on the end of the address, after a `?`. With
  `method="post"`, they travel inside the request, and the address
  stays clean.

`get` suits a search form. The answers are part of the address, so a
visitor can bookmark the results or share them. `post` suits anything
that sends a message or changes something, such as a contact form or a
sign-up form. The answers do not appear in the address bar or the
browser's history.

At the other end of the address there has to be a *server*. A server,
here, is a program on a computer connected to the internet. It
receives requests from browsers and sends back replies. For a form, the
program reads the name/value pairs, does something with them, and
sends back a page, such as "Thank you, we will be in touch".

![A browser window on the left, showing a contact form with a Send button. An arrow labelled "name=Ana&email=ana%40example.com" runs from it to a box on the right labelled "server: a program that receives the answers". The server's box lists what it does: check every answer again, then store it or email it. A second arrow runs back to the browser, labelled "a reply page: Thank you".](form-sent.svg)

## Your form, and GitHub Pages

Your `contact.html` has no `action` and no `method`. So when every
field is filled in and a visitor presses **Send**, the browser sends
the answers to the page's own address, after a `?`, and loads the page
again. You can see them in the address bar:

```text
contact.html?name=Ana&email=ana%40example.com&message=Hello
```

Nothing keeps them. GitHub Pages sends back files, and it runs no
program of yours, so there is nobody at that address to read the
answers. The comment at the top of `contact.html` says the same. The
project asks for a form's markup, and a working form needs something
behind it.

To make a form on a site like yours send email for real, people often
use a *form service*. A form service is a company that runs the server
side for you. It gives you an address to put in `action`, and it emails
you each set of answers. Others write their own server program, in a
language such as PHP, Python or JavaScript. Either way, the HTML you
have written stays the same, apart from `action` and `method`.

## `required` is not security

In your own site, `required` stops the form while a field is empty,
and `type="email"` checks that an address has roughly the right shape.
Checks like these are called *validation*: making sure each answer is
the kind of thing it should be.

Validation in the browser is there for the visitor. It catches a
mistake before the form is sent, and says what to fix. It does not
protect anything, because the visitor controls their own browser. You
can see this for yourself:

1. Open your own `contact.html` in the browser, and leave the Name field
   empty.
2. Open the inspector, and find the `<input>` for the name.
3. Double-click `required` in the **Elements** tab, and delete it.
4. Fill in the other two fields, and press **Send**. Is the form sent
   now, with an empty name?

Anyone can do the same, and a program can send answers to a server with
no page and no browser at all. So the server has to check every answer
again, and never trust that the browser checked it. The browser's check
also only looks at the shape of an address. `a@b` passes, because it
has the right shape. Only an email sent to it shows whether it is
real.

## Labels, more closely

On [A contact form](tutorial:a-form) we joined a label to its field with
`for` and `id`. There is a second way. A `<label>` can wrap around its
field:

```html
<label>
  Email
  <input type="email" name="email">
</label>
```

The label and the field are joined because one is inside the other.
Clicking the word gives the field focus, and a screen reader reads the
label, the same as with `for` and `id`. Both ways are correct. The
`for` and `id` way lets the label and the field sit anywhere in the
HTML, which makes the layout easier to change.

Sometimes we might see a form with no labels at all, only grey text
inside each field, such as "Your email". That grey text is a
*placeholder*, set with the `placeholder` attribute. A placeholder is
not a label. It disappears as soon as the visitor starts typing, so
they can no longer see what the field was for. It is often pale grey,
which many people find hard to read. A placeholder can add an example,
such as `placeholder="ana@example.com"`, but the label still needs to
be there.

## What we have now

We can now follow a form's answers out of the page: what the browser
sends, where it goes, and what has to be waiting at the other end.

| Word | Meaning | Example |
|---|---|---|
| `name` | On a form field, the label on its answer when the form is sent. A field with no `name` is not sent. | `name="email"` |
| *name/value pair* | One answer as it is sent: the field's `name`, `=`, and what the visitor typed | `email=ana%40example.com` |
| `action` | On a `<form>`, the address its answers are sent to | `action="https://example.com/contact"` |
| `method` | On a `<form>`, how the answers travel: on the end of the address (`get`), or inside the request (`post`) | `method="post"` |
| *server* | A program on a computer connected to the internet, that receives requests and sends back replies | the program that reads a contact form |
| *validation* | Checking that each answer is the kind of thing it should be. The browser's check helps the visitor. The server must check again. | `required`, `type="email"` |
| *placeholder* | Grey example text inside a field, which disappears when the visitor types. It is not a label. | `placeholder="ana@example.com"` |

## Where to read more

CrashCourse (2017). *The Internet: Crash Course Computer Science #29.*
<https://www.youtube.com/watch?v=AEaKrq3SpW8>. It shows where a form's
answers travel after you press the button: to the right computer, in small
packets, across many networks. Twelve minutes.
