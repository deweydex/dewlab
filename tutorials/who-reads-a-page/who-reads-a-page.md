---
title: "Who else reads a page"
year: "2026-2027"
version: 2026.09.22.1
context_for:
  - headings-and-emphasis
  - the-skeleton
  - sections-that-mean-something
  - describing-an-image
  - three-kinds-of-link
  - navigation
---

# Who else reads a page

A sighted visitor sees the page a browser draws. But other readers use
the HTML itself, and never look at the drawing. Several pages in this
series choose a tag for what it means, and not for how it looks: [The
head and body of a page](tutorial:the-skeleton), [Headings, paragraphs
and emphasis](tutorial:headings-and-emphasis), [Semantic HTML: tags
that describe their content](tutorial:sections-that-mean-something),
[Describing an image with alt text](tutorial:describing-an-image),
[Links to pages, other sites and email](tutorial:three-kinds-of-link)
and [A menu that jumps to each section](tutorial:navigation). This page
shows who reads that meaning. It is background reading. You do not need
it to finish those pages, but it can help you see why they matter.

On this page we:

- compare two pieces of HTML that look the same, and mean different
  things
- see what a browser, a screen reader and a search engine each take
  from a page
- hear how a screen reader moves around a page
- find the browser's own list of what each element means, in the
  inspector

## Two pages that look the same

Here are two versions of the top of a shop's page, one above the other.
The first is built from `<div>` and `<span>`, two tags with no meaning
of their own. The second uses tags that say what each part is. The CSS
makes the two look the same.

```html site
id: readers-html
site: readers
<div class="top">
  <div class="big">Plushie Shop</div>
  <div><span class="link">New</span> <span class="link">Visit us</span></div>
</div>
<hr>
<header>
  <h1>Plushie Shop</h1>
  <nav aria-label="Main"><a href="#new">New</a> <a href="#visit">Visit us</a></nav>
</header>
```

```css site
id: readers-css
site: readers
.big, h1 { font-size: 24px; font-weight: bold; margin: 0 0 4px; }
.link, a { color: #2672ad; text-decoration: underline; }
```

1. Can you see any difference between the two versions?
2. Click in the preview, and press the **Tab** key a few times. Which
   words get an outline around them?
3. Which version do you think a screen reader could describe?

The two look the same, but only the second version's links take part
when we press **Tab**. The words in the first version only look like
links. To the browser, they are text in a box, and so they are to
everyone who uses the browser's model of the page.

## What the browser takes from a page

The browser is the first reader of every page. It uses the meaning of
the tags in three ways.

- **It draws the page.** Each tag has a default look: headings are
  large and bold, `<strong>` is bold, a link is blue and underlined, and
  a link can be reached with the **Tab** key.
- **It names the page.** The text of `<title>` goes on the tab, in the
  browser's history, and on a bookmark. When a page has no title, the
  tab often shows the file name or the web address instead.
- **It builds a second tree.** Next to the tree of elements, the browser
  builds an *accessibility tree*. It holds what each element is for,
  and not how it looks: its role, such as heading, link or image, and
  its name, such as the words of a link or the alt text of an image.
  Screen readers and other tools read the page through this tree.

In the example above, the accessibility tree for the first version holds
three pieces of plain text, and nothing about what they are. For the
second version it holds a banner, a heading at level 1, a navigation
called "Main", and two links. The `lang="en"`
at the top of your own `index.html` goes into this model too. It tells
software which language the words are in, so that it can pronounce them,
check their spelling, or offer to translate them.

## What a screen reader does with it

A *screen reader* is software that reads a page aloud for someone who
cannot see it. It reads the accessibility tree, not the drawing. Here
is the second version of the example, as a sighted visitor sees it, and
as a screen reader might say it:

![Two panels side by side. On the left, headed "A sighted visitor sees", a small drawing of the page: the bold heading "Plushie Shop", and under it two underlined links, "New" and "Visit us". On the right, headed "A screen reader might say", five lines of speech, one under another: "banner", "heading, level 1, Plushie Shop", "Main navigation", "link, New", "link, Visit us". A note under the panels says that the exact words differ from one screen reader to another.](screen-reader-says.svg)

A listener cannot glance down a page, so a screen reader gives them
other ways to move around it. The exact keys differ, but most screen
readers can:

- **Jump from heading to heading**, or list every heading on the page.
  Many screen reader users move around a page this way. That is why the
  heading levels need to make sense on their own, as a list of
  contents. A heading chosen for its size breaks that list.
- **Jump from landmark to landmark.** A *landmark* is a main region of
  a page that a screen reader can jump to. `<header>`, `<nav>`, `<main>`
  and `<footer>` each make one. When a page has two `<nav>` elements, an
  `aria-label` gives each one its own name, such as "Main navigation".
- **List every link on the page.** In that list, each link is heard on
  its own, away from the words around it. So a link's words need to
  make sense alone. Five links that each say "Read more" all sound the
  same. "Read more about me" does not.
- **Read an image's alt text**, in place of the image. With `alt=""`,
  the screen reader skips the image. With no `alt` at all, some screen
  readers read out the file name.

What about bold and italic text? The tags `<b>` and `<i>` also make
text bold and italic, and they often look the same as `<strong>` and
`<em>`. The difference is in the meaning. `<strong>` and `<em>` tell any
software that reads the code that the words are important or stressed.
`<b>` and `<i>` do not say that. Not every screen reader announces the
difference, but the meaning is there in the code for the ones that do,
and for search engines.

Windows and macOS each come with a screen reader. You could listen to
your own site:

1. Turn a screen reader on. On Windows, Narrator starts with the
   **Windows logo key**, **Ctrl** and **Enter** together. On a Mac,
   VoiceOver starts with **Cmd** and **F5**. The same keys turn it off
   again.
2. Open your published site, and let it read the top of your page.
3. Press **Tab** to move from link to link. Does each link's name make
   sense on its own?
4. Turn the screen reader off.

It is a strange experience the first time, and it is fast. Many people
who use a screen reader every day set it to speak much faster than
this.

## What a search engine takes from a page

A search engine uses a program, often called a *crawler*, that visits
pages, reads their HTML, and follows their links to find more pages. It
never sees the page drawn. It uses the same meaning a screen reader
does:

| From the HTML | What a search engine can do with it |
|---|---|
| `<title>` | Show it as the heading of a search result, as most search engines do |
| `<meta name="description">` | Show it under the title, in place of a piece of the page |
| headings | Learn what the page, and each part of it, is about |
| link words | Learn what the page at the other end of a link is about |
| alt text | Find the image in a search for images |

So the choices that help a listener help a search engine too. A page
with a clear title, headings that form a list of contents, links whose
words make sense, and images with alt text is easier for both to
understand.

## Seeing the accessibility tree

The inspector can show the accessibility tree, next to the tree of
elements. You could look at your own site:

1. Open your site in the browser, and open the inspector.
2. In the **Elements** tab, select the `<nav>` element in your header.
3. Find the accessibility panel. In Chrome and Edge, it is a tab called
   **Accessibility**, next to **Styles**. You may need to click `»` to
   see it. In Firefox, it is a separate tab called **Accessibility**.
4. What role does it give your `<nav>`? What name?
5. Now select your `<img>`. What name does it have? Where did that
   name come from?

## What we have now

We can now name the readers of a page besides a sighted visitor, and
say what each one takes from the HTML.

| Word | Meaning | Example |
|---|---|---|
| *accessibility tree* | The browser's model of what each element on a page is for: its role and its name | a link, named "Visit us" |
| *screen reader* | Software that reads a page aloud for someone who cannot see it, from the accessibility tree | Narrator, VoiceOver |
| *landmark* | A main region of a page that a screen reader can jump to | `<nav>`, `<main>` |
| *crawler* | A search engine's program that reads pages and follows their links | it reads your `<title>` and headings |
| `<b>` and `<i>` | Bold and italic text with no meaning of its own | `<b>New</b>` |
