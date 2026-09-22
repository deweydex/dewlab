---
title: "Movement, focus and the people who use your page"
year: "2026-2027"
version: 2026.09.22.1
context_for: [hover-and-focus, transitions-and-transforms, keyframes-and-the-checkbox-hack, the-checkbox-hack]
---

# Movement, focus and the people who use your page

Four pages make a page answer the people who use it: [Styling what the
visitor points at: hover and focus](tutorial:hover-and-focus), [Moving
things smoothly: transforms and transitions](tutorial:transitions-and-transforms),
[Animation with keyframes](tutorial:keyframes-and-the-checkbox-hack) and
[Opening and closing content with a
checkbox](tutorial:the-checkbox-hack). This page is about those people.
It is background reading. You do not need it to finish those pages, but
it can help you build things that work for everyone.

On this page we:

- move through a page with the keyboard alone, and see what Tab skips
- see why a focus style must never disappear
- see why hover can only ever be an extra
- turn movement off for people who ask for less of it
- see why some movement is smoother than other movement
- meet the question that opens which HTML has built in

## Moving through a page with the keyboard

Many people use a page without a mouse. Some cannot hold a mouse
steady, because of an injury or an illness that affects their hands.
Some are blind, and use a screen reader, the program that reads a page
aloud. A screen reader is driven from the keyboard. And some
people find the keyboard faster, once they know it.

A few keys do most of the work:

| Key | What it does |
|---|---|
| Tab | Moves focus to the next thing we can use |
| Shift+Tab | Moves focus back |
| Enter | Follows a link, or presses a button |
| Space | Presses a button, or ticks and unticks a checkbox |

Safari on a Mac is different. By default, Tab skips links there. To
change that, open Safari's settings, choose **Advanced**, and turn on
**Press Tab to highlight each item on a webpage**.

Which things does Tab stop at? Here are five, one on each line.

```html site
id: people-keys-html
site: people-keys
<p><a href="#">A link</a></p>
<p><button>A button</button></p>
<p><span class="fake-button">A span that looks like a button</span></p>
<p><input type="checkbox" id="hidden-box" class="hidden">
<label for="hidden-box">The label of a hidden checkbox</label></p>
<p><input type="checkbox" id="shown-box">
<label for="shown-box">A checkbox we can see</label></p>
```

```css site
id: people-keys-css
site: people-keys
.fake-button {
  padding: 2px 8px;
  background: #efefef;
  border: 1px solid #767676;
  border-radius: 3px;
  cursor: pointer;
}
.hidden {
  display: none;
}
:focus {
  outline: 3px solid #d9720c;
  outline-offset: 2px;
}
```

1. Click in the empty space at the top of the preview, above the link.
   Then press Tab, again and again. Which lines get the orange outline?
2. Which lines does Tab skip?
3. When the checkbox we can see has focus, press Space. What happens?

Tab stopped at the link, the button and the checkbox we can see. Links,
buttons and form fields can take focus on their own. A `<span>` or a
`<div>` cannot, even when CSS makes it look like a button. So a person
with a keyboard can never reach a "button" made that way, and a screen
reader does not call it a button.

Tab skipped the hidden checkbox too. `display: none` removes an element
from the page completely: from the screen, from the Tab key, and from
screen readers. That is the weakness of the checkbox hack. Its question
cannot be opened from the keyboard, because the checkbox behind it can
never take focus.

Tab visits things in the order they come in the HTML. That order is the
page's *tab order*. Your own home page has nine stops, once it has the
contact section from [Links to pages, other sites and
email](tutorial:three-kinds-of-link):

![Your home page drawn as five bands, top to bottom: page top, header, hero, card and contact. Each band holds its links and buttons, numbered in the order Tab visits them. 1, Skip to main content, at the page top. 2 to 6 in the header: My Portfolio, Home, About, Skills and Contact. 7, Learn More About Me, in the hero. 8, Read More, in the card. 9, Send Me an Email, in the contact section.](tab-order.svg)

The first stop, "Skip to main content", is there for keyboard users. It
stays hidden until it has focus. Pressing Enter on it jumps past the
five header links, straight to the page's main content. Without it,
someone would press Tab through all five header links, on every page,
before they reached anything new.

## Seeing where focus is

A person who uses Tab needs to see where focus is, on every press. The
focus style is the only thing that tells them. When a stylesheet sets no
focus style, the browser draws its own, often a blue or black ring.

Sometimes we might find `outline: none` in a stylesheet, on `:focus` or
on every element. It was often added to hide the outline after a mouse
click. It removes the browser's ring and puts nothing in its place. A
person using a mouse sees no change at all. A person using a keyboard
is suddenly lost on the page.

There is a better way to hide the outline after a click. The
*`:focus-visible`* pseudo-class matches an element that has focus, but
only when the browser decides the person needs to see it. After Tab, it
matches. After a mouse click on a button, it does not. Here are two
buttons with the same outline. The first uses `:focus`, and the second
uses `:focus-visible`.

```html site
id: people-visible-html
site: people-visible
<button class="with-focus">Styled with :focus</button>
<button class="with-focus-visible">Styled with :focus-visible</button>
```

```css site
id: people-visible-css
site: people-visible
button {
  margin: 8px;
  padding: 8px 12px;
  font-size: 1rem;
}
.with-focus:focus {
  outline: 3px solid #d9720c;
  outline-offset: 2px;
}
.with-focus-visible:focus-visible {
  outline: 3px solid #d9720c;
  outline-offset: 2px;
}
```

1. Click the first button. Does it get the outline?
2. Click the second button. Does it get the outline?
3. Now press Shift+Tab, then Tab. Does the second button get the outline
   this time?

Many sites use `:focus-visible` for this reason. The outline appears for
the people who need it, and stays out of the way for everyone else.

An outline also has to stand out from whatever is behind it. Your own
site shows this. The `a:focus` rule in `styles.css` gives links an
outline in the accent colour. The `.main-nav a:focus` rule gives the
header's links a white outline, because the header behind them is dark.
When you add a focus style, Tab to it and check that you can see it on
its own background.

## Hover is an extra

A phone or a tablet has no pointer that can rest over an element. We
touch the screen, and the finger is gone again. On many phones, a tap
turns the `:hover` style on, and it stays on until we tap somewhere
else. A keyboard has no pointer either.

So a hover effect is a nice extra, and it should never be the only way
to find something. A price that appears only under the pointer is a
price that phone users and keyboard users never see. If an effect makes
sense only with a pointer, a media query can keep it to devices that
have one:

```css
@media (hover: hover) {
  .card:hover {
    transform: translateY(-5px);
  }
}
```

A media query is a block of CSS that applies only when a condition is
true. We meet media queries properly on [Changing the layout for phones:
media queries](tutorial:media-queries). Here the condition is that the
device has a pointer that can hover.

## When movement makes people unwell

For some people, movement on a screen does more than catch the eye. It
can make them dizzy or sick, or give them a headache. This happens most
often with large movements: things that slide across the screen, zoom
in, or move at a different speed from the page as it scrolls. People
who feel this can turn on a setting on their device that asks for less
movement. The setting has a different name on each system. It is called
Reduce motion on Apple devices, Remove animations on Android, and
Animation effects on Windows 11.

A page can read that setting with a media query:
*`prefers-reduced-motion`*. The query
`@media (prefers-reduced-motion: reduce)` applies its CSS only when the
person has asked for less movement. Here is a dot that bounces, unless
that setting is on:

```html site
id: people-calm-html
site: people-calm
<div class="dot"></div>
<p>This dot bounces, unless your device asks for less movement.</p>
```

```css site
id: people-calm-css
site: people-calm
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
.dot {
  width: 30px;
  height: 30px;
  margin-top: 30px;
  border-radius: 50%;
  background: #d9720c;
  animation: bounce 1s ease-in-out infinite;
}
@media (prefers-reduced-motion: reduce) {
  .dot {
    animation: none;
  }
}
```

1. Does the dot bounce? If it does not, your device may already ask for
   less movement.
2. You can test the other case without changing your device. In Chrome
   or Edge, open the inspector and press Ctrl+Shift+P (Cmd+Shift+P on a
   Mac). Type "rendering" and choose **Show Rendering**. In the panel
   that opens, find **Emulate CSS media feature
   prefers-reduced-motion**, and choose `reduce`. What does the dot do
   now?

"Reduce" does not have to mean "remove". A small fade or a short change
of colour is fine for most people. The things to turn off are the large
ones: movement across the screen, zooming, and anything that repeats
forever. The web's accessibility guidelines, WCAG, ask one more thing:
anything that moves on its own for more than five seconds should have a
way to pause it, stop it or hide it.

Your own site has movement you may not have noticed. In `styles.css`,
the `html` rule sets `scroll-behavior: smooth`. That is why a menu link
glides down the page to its section, instead of jumping. A gliding
page is movement too, so it is a good thing to turn off:

```css
@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}
```

## Why some movement is smoother than other movement

A browser shows a moving page as a quick run of still pictures, one
after another, sixty every second on most screens. For each picture,
the browser does two jobs. First, it works out where every box goes and
how big it is. This job is called layout. Then it draws the boxes. [How a
browser lays out a page](tutorial:how-a-browser-lays-out-a-page) looks
at the first job closely.

A `transform` changes only the second job. The browser draws the box
somewhere new, bigger or turned, but the layout stays exactly as it
was. That is why a transformed box never pushes its neighbours away. It
is also why a transform moves smoothly: the browser does not have to
work out the whole layout again for every picture. `opacity` works the
same way.

Other properties change the layout itself. `width`, `height`, `margin`
and `top` all change where boxes go. When a transition or an animation
changes one of these, the browser works out the layout again for every
picture. On a slow phone, that can make the movement stutter. So when
something only needs to look as if it moves, a `transform` is the better
choice. The checkbox hack animates `max-height`, which does change the
layout. For one short answer that is fine, because there is very little
to work out.

## A question that opens, built into HTML

HTML has its own element for a question that opens. *`<details>`* is an
element that hides its content until we open it. The *`<summary>`*
inside it is the part that always shows, and clicking it opens or
closes the rest. There is no checkbox, and no CSS is needed to make it
work. Here are two questions built that way:

```html site
id: people-details-html
site: people-details
<details>
  <summary>What is the checkbox hack?</summary>
  <p>A pattern that shows or hides content using a hidden checkbox and
  the <code>:checked</code> selector, with no JavaScript at all.</p>
</details>
<details>
  <summary>Is there a built-in way?</summary>
  <p>Yes, this one: a details element, with a summary inside it.</p>
</details>
```

```css site
id: people-details-css
site: people-details
summary {
  padding: 10px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  cursor: pointer;
}
details p {
  padding: 0 10px;
}
```

1. Click each question. Can both be open at the same time?
2. Click the first question again to close it. Now press Tab. Where
   does focus go? Press Enter, then Space. What does each one do?
3. What happens if we add the word `open` to the first `<details>` tag,
   as in `<details open>`?

The browser does all the work here. The summary can take focus, so Tab
reaches it, and Enter or Space opens it. A screen reader says whether
it is open or closed. The `open` attribute makes a question start open.
The small triangle beside each summary is the browser's own marker,
which turns when the question opens.

| | The checkbox hack | `<details>` and `<summary>` |
|---|---|---|
| Opens with a mouse | Yes | Yes |
| Opens with the keyboard | No, the checkbox is hidden | Yes |
| A screen reader says if it is open | No | Yes |
| Needs CSS to work | Yes | No |
| Slides open | Yes, with a `transition` | No, it opens at once |

So why learn the checkbox hack at all? Many older sites use it, and
you will meet it in their code. The way it works is useful on its own,
too: a hidden control, a `:checked` state, and a `~` rule that reaches
other elements. For a question that opens on your own pages,
`<details>` is the better choice.

## What we have now

We can now check a page with the keyboard, keep its focus visible, and
turn movement off for the people who ask for less of it.

| Word | Meaning | Example |
|---|---|---|
| *tab order* | The order Tab visits links, buttons and form fields: the order they come in the HTML | your skip link, then your logo |
| *`:focus-visible`* | Matches an element with focus, only when the browser decides the person needs to see it: after Tab, not after a click on a button | `a:focus-visible` |
| `@media (hover: hover)` | Applies CSS only on a device with a pointer that can hover | `@media (hover: hover) { … }` |
| *`prefers-reduced-motion`* | A media query that tells us whether the person has asked their device for less movement | `@media (prefers-reduced-motion: reduce)` |
| *`<details>`* | An element that hides its content until we open it | `<details>…</details>` |
| *`<summary>`* | The part of a `<details>` that always shows. Clicking it opens or closes the rest. | `<summary>A question</summary>` |
