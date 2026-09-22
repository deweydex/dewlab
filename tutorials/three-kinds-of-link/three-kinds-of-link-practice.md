---
title: "Links to pages, other sites and email — Practice"
practice_for: three-kinds-of-link
year: "2026-2027"
version: 2026.09.22.1
---

# Links to pages, other sites and email — Practice

On this page we practise writing links, and choosing the right shape of
`href` for each one. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

The previews on this page have no other pages to open. So if you click
a link to a file such as `about.html`, the preview goes blank. Run the
cell again to bring it back. To see where a link goes, read its `href`.

## Fix the broken page

**1.** Only the words "About page" should be a link. Look at the second
paragraph.

```html site
id: links-practice-close-html
site: links-practice-close
<p>Read more on our <a href="about.html">About page.</p>
<p>We are open from 10 to 6, Monday to Saturday.</p>
```

Why is the second paragraph blue and underlined too? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the opening `<a>` tag. Where is its closing tag?
2. Without a closing tag, where does the browser think the link ends?

**Think about:** which words should a visitor be able to click?

**Try this next:** once it works, move the full stop so that it sits
outside the link. Does the link change?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<p>Read more on our <a href="about.html">About page</a>.</p>
<p>We are open from 10 to 6, Monday to Saturday.</p>
```

The closing tag `</a>` was missing, so the browser had to guess where
the link ends. It carried the link on past the end of the first
paragraph, and wrapped the second paragraph in it too. With `</a>`
after "About page", only those two words are a link. The full stop now
sits outside the link, where it belongs.

</details>

**2.** This page should have an email link. There is nothing to click.

```html site
id: links-practice-empty-html
site: links-practice-empty
<p>Email us at <a href="mailto:hello@example.com"></a>hello@example.com.</p>
```

The `href` looks right. So why is nothing blue? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the opening `<a>` tag and the closing `</a>` tag.
2. What is between them?

**Think about:** a link is the content between its two tags. What if
there is no content?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<p>Email us at <a href="mailto:hello@example.com">hello@example.com</a>.</p>
```

The link had no content: `</a>` came straight after the opening tag. So
the link was there, but it had no words in it, and nothing on the page
to click. The words a visitor clicks go between `<a ...>` and `</a>`.

</details>

## Make this

**3.** Write this paragraph in the cell below, with three links in it:

> You can read about us, look up HTML on MDN, or write to us.

- "read about us" is a link to the page `about.html` in the same site
- "MDN" is a link to `https://developer.mozilla.org`
- "write to us" is a link that starts a new email to
  `hello@example.com`

```html site
id: links-practice-build-html
site: links-practice-build
<!-- your HTML here -->
```

Which of your three links is a same-site link, which is an external
link, and which is a mailto: link?

<details class="dl-answer"><summary>answer</summary>

```html
<p>You can <a href="about.html">read about us</a>, look up HTML on
<a href="https://developer.mozilla.org">MDN</a>, or
<a href="mailto:hello@example.com">write to us</a>.</p>
```

- `about.html` is a filename, so the first is a same-site link.
- `https://developer.mozilla.org` is a full web address, so the second
  is an external link.
- `mailto:hello@example.com` starts with `mailto:`, so the third is a
  mailto: link.

The paragraph can run over several lines of HTML. The browser joins
them into one line of text on the page.

</details>

## In your own site

**4.** Your contact section has an email link. Let's add an external
link beside it, to your profile on GitHub.

1. In your fork, open `index.html`, and find your contact section.
2. Straight after the paragraph "I'd love to hear from you.", add:

```html
<p>You can also find my work on <a href="https://github.com/your-username">GitHub</a>.</p>
```

3. Change `your-username` to your own GitHub username.
4. Save, refresh, and click the new link. Does your GitHub profile
   open?
5. Commit the change, with a message such as "Link to my GitHub
   profile".

Which kind of link did you add?

<details class="dl-answer"><summary>answer</summary>

It is an external link: its `href` is a full web address, starting with
`https://`, and it goes to another site. If it opens a GitHub page that
says it cannot find the address, check the username letter by letter.

The link sits on the dark background of the contact section. If it is
hard to read there, that is a job for CSS. We start on CSS in [CSS
rules and stylesheets](tutorial:a-rule-and-where-it-lives).

</details>

**5.** What does a visitor see when a same-site link is broken? Let's
find out on your published site, and then fix it.

1. In `index.html`, find the **Read More** button in the about-preview
   section. Its `href` is `about.html`.
2. Change it to `About.html`, with a capital A.
3. Commit the change. Wait a minute for GitHub Pages, then open your
   published site.
4. Click **Read More**. What do you see?
5. Change the `href` back to `about.html`, and commit again.
6. Wait a minute, refresh, and click **Read More** once more.

Why did one capital letter break the link?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What is the real name of your About page's file, letter by letter?
2. On GitHub Pages, are `About.html` and `about.html` the same name?

**Think about:** the browser does not guess which file we meant. It
asks for exactly the name in `href`.

**Try this next:** the navigation at the top of your page also links to
`about.html`. Does that link still work while **Read More** is broken?

</details>

<details class="dl-answer"><summary>answer</summary>

With `About.html`, the published site shows an error page from GitHub
with the number 404 on it. 404 means the server could not find the file
the browser asked for. Your file is called `about.html`, and on GitHub
Pages a capital letter makes a different name.

On your own computer, the link may still work, because Windows and
macOS usually treat `About.html` and `about.html` as the same name.
That is what makes this mistake easy to miss until the site is
published.

The navigation link has its own `href`, which still says `about.html`,
so it kept working the whole time.

</details>
