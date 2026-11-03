---
title: "How pages learned to respond: then and now"
year: "2026-2027"
version: 2026.11.03.1
---

# How pages learned to respond: then and now

The two boxes below do the same thing. Point at each one. One of them is
written the way a web page did it in 1999. The other is written the way
we do it now. Which is which?

```html site
id: rollover-then-html
site: rollover-then
<p>Point at the box.</p>
<div id="box" style="width:12rem;padding:1rem;background:#1B2A4A;color:white"
     onmouseover="this.style.background='#D4692A'"
     onmouseout="this.style.background='#1B2A4A'">
  A rollover, 1999 style
</div>
```

```html site
id: rollover-now-html
site: rollover-now
<p>Point at the box.</p>
<div class="box">A rollover, today</div>
```

```css site
id: rollover-now-css
site: rollover-now
.box {
  width: 12rem;
  padding: 1rem;
  background: #1B2A4A;
  color: white;
  transition: background 0.3s;
}
.box:hover {
  background: #D4692A;
}
```

The first box carries two small scripts in its own tag, `onmouseover`
and `onmouseout`. The second has no script at all. A CSS rule says what
the box looks like while the pointer is over it, and the browser does
the rest. This page tells the story of how so much of what once needed a
script became part of HTML and CSS. On this page we:

- follow the web from plain documents to pages that respond
- see why scripts did so many jobs in the 2000s
- see which of those jobs HTML and CSS do on their own now

## 1991 to 1995: documents and forms

The first web page went online at CERN in 1991. It was text and links,
nothing more. A page could not respond to anything except a click on a
link, which fetched a whole new page.

Forms came soon after. A form let a reader type something and send it to
a **server**, the computer that sent the page in the first place. A
program on the server read the form and built a new page as its answer.
Every response, however small, meant a trip to the server and a whole new
page.

## 1995 to 2004: scripts do everything

In 1995 the Netscape browser added **JavaScript**, a language that runs
inside the page itself. For the first time a page could change without
asking the server. CSS arrived in 1996, but browsers supported it
unevenly for years, so scripts did jobs that we now give to CSS:

- swapping an image when the pointer moved over it, as in the first box
  above
- opening and closing parts of a page
- checking a form before it was sent
- opening small pop-up windows

Video, animation and games needed more than either could give. They came
from **plugins**, programs added to the browser, and Flash was the best
known of them.

## 2005 to 2014: Ajax, and then HTML5

In 2005 a new name, **Ajax**, described a page that asks the server for a
little data in the background and updates one part of itself. Gmail and
Google Maps made it famous. This was the heart of what people called Web
2.0: pages that people wrote into, not only read.

At the same time, work began on a new version of HTML. HTML5 became a
W3C standard in 2014. It added `<video>` and `<audio>`, so a page no
longer needed Flash to play a clip. It added form attributes such as
`required` and `type="email"`, so the browser could check a form itself.
CSS3 added transitions, animations and media queries. The scripts of the
early 2000s began to lose their jobs.

Flash reached its official end in December 2020.

## 2015 to now: the browser does it

HTML stopped having numbered versions in 2019. It is now one *living
standard* that grows a little at a time, and each new feature arrives
when every major browser supports it. In the last few years:

| What a page does | Then: a script | Now: HTML or CSS | In every major browser since |
|---|---|---|---|
| Change on hover | `onmouseover` | `:hover` in CSS | long ago |
| Open and close a panel | a click handler | `<details>` | 2020 |
| Show a box over the page | a pop-up script | `<dialog>` and `popover` | 2022 and 2024 |
| Open a dialog from a button | `showModal()` in a script | `commandfor` on the button | late 2025 |
| Check a form | a submit handler | `required`, `pattern`, `:user-invalid` | 2023 for `:user-invalid` |
| Style a page from its own state | a script that adds classes | `:has()` in CSS | 2023 |
| Play a video | Flash | `<video>` | about 2012 |

Scripts did not go away. They moved to the jobs that HTML and CSS still
cannot do: adding up an order, remembering a visitor, and fetching data
without reloading the page. The pages after this one take each feature in
the table in turn. Each shows the HTML and CSS way first, because that is
how it is normally done now. Then it shows the script way, and says when
a script is still the right tool.

## Why the newer way is usually better

```question
id: keyboard-rollover
type: multiple-choice
answer: 1

A visitor uses only a keyboard, with no mouse. Which of the two boxes at
the top of this page can they make change colour?

- Neither
  - Neither box has anything a keyboard can reach, so neither changes.
- Only the 1999 box
  - The script runs on `onmouseover`, which a keyboard never fires.
- Only today's box
  - `:hover` also needs a pointer, so a keyboard user cannot trigger it.
```

Neither, as they stand. The modern fix
is one more selector, `.box:focus-visible`, and a `tabindex="0"` on the
box, both covered in *Styling what the visitor points at*. The 1999 fix
needed two more scripts. That pattern repeats through this section. The
HTML and CSS way is shorter, works with a keyboard and a screen reader
more often, and keeps working when a script fails to load.

## Now add your own

1. In today's box, change `#D4692A` to another colour and point at the
   box again.
2. In the 1999 box, find the colour in `onmouseover` and change it to
   match. Which change was easier to find?
3. Add `tabindex="0"` to today's box, and a `.box:focus-visible` rule
   with the same background as `:hover`. Press Tab until the box is
   selected.

## What we have now

| Word | Meaning | Example |
|---|---|---|
| *server* | The computer that sends a page to the browser, and answers when a form is sent | A web host such as GitHub Pages |
| *JavaScript* | A language that runs inside the page itself, in the visitor's browser | `onmouseover="..."` |
| *plugin* | A program added to a browser to do what HTML could not, such as play video | Flash |
| *Ajax* | A page asking the server for data in the background and updating one part of itself | Gmail loading a new email |
| *living standard* | HTML since 2019: one standard that grows a feature at a time, with no version numbers | The HTML Living Standard |

## Read more

- [The first website](https://info.cern.ch/hypertext/WWW/TheProject.html),
  still online at CERN.
- [How HTML and CSS got here](tutorial:how-html-and-css-got-here), the
  story of the two languages version by version.
