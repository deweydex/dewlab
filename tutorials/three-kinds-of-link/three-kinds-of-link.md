---
title: "Links to pages, other sites and email"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# Links to pages, other sites and email

A link is an `<a>` element, and its `href` attribute says where the link
goes. Can one tag really point at three quite different things? On this
page we:

- read three links and compare their `href` values
- learn what each shape of `href` tells the browser to do
- add a contact link to your own site

## Let's try it

The box below has three links. Look at the `href` on each one before you
click anything.

```html site
id: links-html
site: links
<p>Read more on the <a href="about.html">About page</a>.</p>
<p>Look something up on <a href="https://developer.mozilla.org">MDN</a>.</p>
<p>Send a message to <a href="mailto:hello@example.com">hello@example.com</a>.</p>
```

1. How is the first `href` different from the second? What does the
   second one start with?
2. The third `href` starts with `mailto:`. What do you think the browser
   does with that?
3. Which of the three links would stay inside your own site?

## Why does this happen?

Each `href` has a different shape, and each shape tells the browser to
do something different. Now we can explain what we saw:

| The `href` | Its shape | Where it goes |
|---|---|---|
| `about.html` | a filename | another page in your own site |
| `https://developer.mozilla.org` | a full web address | a page on another site |
| `mailto:hello@example.com` | `mailto:` and an email address | an email program, not a page |

- A *same-site link* has a filename in its `href`. It points at another
  page in your own site. The browser looks for a file with that name in
  the same folder as the page you are on.
- An *external link* has a full web address in its `href`, starting
  with `https://`. It points at another site, somewhere else on the web.
- A *mailto: link* has `mailto:` in its `href`, followed by an email
  address. It tells the browser to open an email program, with a new
  message addressed to whoever comes after the colon. Unlike the other
  two, it does not lead to a page at all.

Oftentimes, when a same-site link leads to an error page, the filename
is the problem. The name in `href` has to match the real file exactly.
`About.html` and `about.html` are two different names on most web
servers, including GitHub Pages. On your own computer the wrong case may
still work, because Windows and macOS usually ignore the difference.
That makes this mistake easy to miss until the site is published.

Sometimes we might click a `mailto:` link and see nothing happen, or see
the browser ask which program to use. What a `mailto:` link opens
depends on the computer. It uses whatever email program is set up
there, and some computers have none.

## Now in your own site

In your fork, open `index.html`.

1. Find the about-preview section. Inside it there is a button: an `<a>`
   tag with `class="btn"`.
2. Look at its `href`. It should already link to `about.html`. Which
   kind of link is that?
3. Click the button on your site. Do you land on the About page?
4. Now find the closing `</main>` tag. Just before it, add this contact
   section:

```html
<section id="contact" class="section contact-section">
    <div class="container">
        <h2>Get In Touch</h2>
        <p>I'd love to hear from you.</p>
        <a href="mailto:your.email@example.com" class="btn">Send Me an Email</a>
    </div>
</section>
```

5. Replace the email address with your own. You can also leave the
   example address as it is for now.
6. Save, and refresh.

Now click **Send Me an Email**. Does your browser try to open an email
program?

The `id="contact"` on this section has a job too. On the next page,
[A menu that jumps to each section](tutorial:navigation), a link in the menu jumps straight to
it.

## What we have now

We can now point a reader to three kinds of place, and your site has a
working contact link.

| Word | Meaning | Example |
|---|---|---|
| `<a>` | A link. It goes wherever its `href` attribute says. | `<a href="about.html">About</a>` |
| *same-site link* | A link with a filename in `href`, pointing at another page of your own site | `href="about.html"` |
| *external link* | A link with a full web address in `href`, pointing at another site | `href="https://developer.mozilla.org"` |
| *mailto: link* | A link that opens an email program, not a page | `href="mailto:hello@example.com"` |
