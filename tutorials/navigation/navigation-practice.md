---
title: "A menu that jumps to each section — Practice"
practice_for: navigation
year: "2026-2027"
version: 2026.09.22.1
---

# A menu that jumps to each section — Practice

On this page we practise anchor links: a link with `#` and a name in its
`href`, and an element with the same name in its `id`. There are three
kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more if you make a
mistake and then find the reason than if you read the answer.

In each preview, the sections have a large space above them, so the
page is too long for the preview. Then we can see whether a link jumps.
When an anchor link does not work, check its two halves: the name after
`#` in the `href`, and the name in the `id`.

## Fix the broken page

**1.** Clicking **Opening hours** should jump down to the opening hours.
Nothing happens.

```html site
id: nav-practice-case-html
site: nav-practice-case
<nav aria-label="Page">
  <ul>
    <li><a href="#new">New this week</a></li>
    <li><a href="#Hours">Opening hours</a></li>
  </ul>
</nav>
<section id="new">
  <h2>New this week</h2>
  <p>A squid, a cuttlefish and a very sleepy seal.</p>
</section>
<section id="hours">
  <h2>Opening hours</h2>
  <p>Monday to Saturday, from 10 to 6.</p>
</section>
```

```css site
id: nav-practice-case-css
site: nav-practice-case
section { margin-top: 400px; }
```

The **New this week** link works. Why does **Opening hours** not? Fix
it.

<details class="dl-answer"><summary>answer</summary>

```html
<li><a href="#hours">Opening hours</a></li>
```

The link said `#Hours`, with a capital H, and the section says
`id="hours"`. The two names must match exactly, capital letters
included. There was no element with `id="Hours"`, so the browser had
nowhere to jump to. Changing either one works, as long as both match.

</details>

**2.** Now clicking **Opening hours** makes the whole preview go blank.

```html site
id: nav-practice-hash-html
site: nav-practice-hash
<nav aria-label="Page">
  <ul>
    <li><a href="#new">New this week</a></li>
    <li><a href="hours">Opening hours</a></li>
  </ul>
</nav>
<section id="new">
  <h2>New this week</h2>
  <p>A squid, a cuttlefish and a very sleepy seal.</p>
</section>
<section id="hours">
  <h2>Opening hours</h2>
  <p>Monday to Saturday, from 10 to 6.</p>
</section>
```

```css site
id: nav-practice-hash-css
site: nav-practice-hash
section { margin-top: 400px; }
```

Why does the page disappear? Run the cell again to bring it back, and
then fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Compare the two `href` values. What does the working one have that
   the other does not?
2. Without that, which kind of link is `href="hours"`? Think back to
   [Links to pages, other sites and email](tutorial:three-kinds-of-link).
3. Where does that kind of link send the browser?

**Think about:** what does `#` tell the browser about where to go?

**Try this next:** on a real site, what do you think a visitor would
see after clicking `href="hours"`?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<li><a href="#hours">Opening hours</a></li>
```

Without `#`, `hours` is a filename, so the link is a same-site link. The
browser tried to leave this page and open a file called `hours`. The
preview has no other files, so it went blank. On a real site, the
visitor would see an error page, because there is no file called
`hours`. With `#`, the browser stays on the same page, and jumps to the
element with `id="hours"`.

</details>

**3.** The author copied the first section to make the second one. Now
clicking **Visit us** jumps to the wrong place.

```html site
id: nav-practice-twice-html
site: nav-practice-twice
<nav aria-label="Page">
  <ul>
    <li><a href="#new">New this week</a></li>
    <li><a href="#visit">Visit us</a></li>
  </ul>
</nav>
<section id="new">
  <h2>New this week</h2>
  <p>A squid, a cuttlefish and a very sleepy seal.</p>
</section>
<section id="new">
  <h2>Visit us</h2>
  <p>12 Harbour Street, Monday to Saturday.</p>
</section>
```

```css site
id: nav-practice-twice-css
site: nav-practice-twice
section { margin-top: 400px; }
```

Where does **Visit us** take us? Scroll down: is **New this week** any
better? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The link says `#visit`. Is there an element with `id="visit"`?
2. Look at the `id` of each section. What did the author forget to
   change when they copied the first section?
3. If two elements share one `id`, which one does the browser jump to?

**Think about:** an `id` must appear only once on a page. Why?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<section id="visit">
  <h2>Visit us</h2>
  <p>12 Harbour Street, Monday to Saturday.</p>
</section>
```

The author copied the first section, and forgot to change its `id`. So
there was no element with `id="visit"`, and **Visit us** did nothing.
Two sections also shared `id="new"`, and **New this week** jumped to the
first of them. An `id` must appear only once on a page, so that every
link has one place to go. When you copy a block of HTML, check its
`id`.

</details>

## Make this

**4.** Build a page with a menu that jumps to three sections:

- navigation named "Page" for a screen reader
- inside it, a list with three links: "Plushies", "Delivery" and
  "Contact"
- three sections, in the same order, each with a heading and a short
  paragraph
- each link jumps to its own section

The CSS puts a large space above each section, as in the other
problems.

```html site
id: nav-practice-build-html
site: nav-practice-build
<!-- your HTML here -->
```

```css site
id: nav-practice-build-css
site: nav-practice-build
section { margin-top: 400px; }
```

Click each link in turn. Does each one jump to its own section?

<details class="dl-answer"><summary>answer</summary>

Your names and paragraphs may be different. Each `href` must match one
`id`:

```html
<nav aria-label="Page">
  <ul>
    <li><a href="#plushies">Plushies</a></li>
    <li><a href="#delivery">Delivery</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
</nav>
<section id="plushies">
  <h2>Plushies</h2>
  <p>Every plushie is made by hand.</p>
</section>
<section id="delivery">
  <h2>Delivery</h2>
  <p>Delivery is free on every order.</p>
</section>
<section id="contact">
  <h2>Contact</h2>
  <p>Write to us at hello@example.com.</p>
</section>
```

`aria-label="Page"` gives the navigation its name. Short names in small
letters, like `delivery`, are easy to match, and easy to type in the
`href`.

</details>

## In your own site

**5.** An anchor link can also jump to a place on another page. Your
About page already uses one: its menu links to `index.html#skills`.
Let's make one of our own, from your home page to the "My Goals" part
of your About page.

1. In your fork, open `about.html`, and find `<h2>My Goals</h2>`.
2. Give it an `id`: `<h2 id="goals">My Goals</h2>`.
3. Open `index.html`, and find the **Read More** button in the
   about-preview section.
4. Straight after that button, add a second link:
   `<a href="about.html#goals" class="btn">My Goals</a>`
5. Save both files, and refresh your home page.
6. Click **My Goals**. Where do you land?
7. Look at the address bar. How does the address end?
8. Commit the change, with a message such as "Link to my goals".

How is `about.html#goals` different from `#goals`?

<details class="dl-answer"><summary>answer</summary>

You land on the About page, already scrolled down to "My Goals". The
address in the address bar ends with `about.html#goals`.

`#goals` alone jumps to `id="goals"` on the same page, and there is no
such element on your home page. `about.html#goals` has two halves: the
file to open, and then the element to jump to inside it. The About
page's menu uses `index.html#skills`, because the skills section is on
the home page, and not on the About page.

On a small screen, the heading may land just under your header, which
stays at the top of the window as you scroll. [A header that stays in
view as you scroll](tutorial:position-and-the-sticky-header) explains
that header.

The address with `#goals` on the end works anywhere. If you copy it and
send it to someone, it opens your About page at "My Goals".

</details>
