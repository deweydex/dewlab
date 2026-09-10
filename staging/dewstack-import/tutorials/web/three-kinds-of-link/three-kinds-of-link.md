---
title: "Three kinds of link"
slug: three-kinds-of-link
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Three kinds of link

An `<a>` tag can point at three quite different things. Look at the
`href` on each link below before you click anything.

```html site=links
<p>Read more on the <a href="about.html">About page</a>.</p>
<p>Look something up on <a href="https://developer.mozilla.org">MDN</a>.</p>
<p>Send a message to <a href="mailto:hello@example.com">hello@example.com</a>.</p>
```

Each `href` has a different shape, and each shape tells the browser to do
something different.

## Why this happens

A filename, like `about.html`, points at another page in your own site.
The browser looks for a file with that name in the same place as the page
you are on.

A full web address points at another site entirely, somewhere else on
the web.

`mailto:` followed by an address tells the browser to open an email
application, addressed to whoever comes after the colon. It is not a page
at all, unlike the other two.

## Your turn

Let's open your fork and find the button in the about-preview section,
the `<a>` tag with `class="btn"`. It should already link to
`about.html`. Try clicking it to confirm you land on the About page.

Then, before the closing `</main>` tag, let's add a contact section:

```html
<section id="contact" class="section contact-section">
    <div class="container">
        <h2>Get In Touch</h2>
        <p>I'd love to hear from you.</p>
        <a href="mailto:your.email@example.com" class="btn">Send Me an Email</a>
    </div>
</section>
```

Replace the email address with your own, or leave the example as it is
for now. Try clicking the link and see your browser try to open an email
application.

## What you have now

Three ways to point a reader somewhere else, and a page of your own with
a working contact link.

- **`<a>`** — a link, pointing wherever its `href` says.
- **A same-site link** — a filename, pointing at another page of yours.
- **A `mailto:` link** — opens an email application instead of a page.
