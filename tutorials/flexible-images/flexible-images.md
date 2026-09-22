---
title: "Flexible images"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Flexible images

What happens to a picture when the screen is narrower than the picture
itself? On this page we:

- watch two copies of one image on a narrow screen
- find the two declarations that make an image fit its space
- check the images in your own site

## Let's try it

Below are two images. Both come from the same file, and that file is
500 pixels wide. The CSS under them gives the second image two extra
declarations.

```html site
id: responsive-img-html
site: responsive-img
<img class="plain" alt="A test image, 500 by 300"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='300'%3E%3Crect width='500' height='300' fill='%232c3e50'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='28' text-anchor='middle' dominant-baseline='middle'%3E500x300%3C/text%3E%3C/svg%3E">
<img class="responsive" alt="The same test image, made flexible"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='300'%3E%3Crect width='500' height='300' fill='%232c3e50'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='28' text-anchor='middle' dominant-baseline='middle'%3E500x300%3C/text%3E%3C/svg%3E">
```

```css site
id: responsive-img-css
site: responsive-img
img { display: block; margin-bottom: 8px; }
.responsive { max-width: 100%; height: auto; }
```

1. Look at the HTML. Which class does each image have?
2. Drag the preview's width slider toward the narrow end, below 500
   pixels. What happens to the first image?
3. What happens to the second image at the same width?
4. What if we delete `max-width: 100%;` from the `.responsive` rule, and
   narrow the preview again? Put it back afterwards.

## Why does this happen?

Now we can explain what we saw. The first image spills past the edge of
the preview. The second one shrinks to fit.

An `<img>` shows at the size of its file, however wide its container
is. Here the container is the element the image sits in, the preview's
page. So the first image stays 500 pixels wide, even when the preview is
narrower than that.

The second image has two more declarations:

```css
.responsive {
  max-width: 100%;  /* never wider than its container */
  height: auto;     /* keep the shape while it shrinks */
}
```

- `max-width: 100%` sets the widest the image may be: the full width of
  its container, and no more. On a wide screen the image keeps its own
  size. On a narrow screen it shrinks.
- `height: auto` lets the browser work out the height from the width.
  So as the image gets narrower, it also gets shorter, and it keeps its
  shape. A square image stays square, and is never squashed.

The link between an image's width and its height is its *aspect ratio*.
Our test image is 500 by 300, so its height is always three fifths of
its width, at any size.

The rule `img { display: block; margin-bottom: 8px; }` is there for the
demo. It puts each image on its own line, with a small gap below it, so
the two are easy to compare.

Sometimes we might notice that removing `height: auto` changes nothing
in the box above. An image's height is already `auto` unless something
else sets it. Oftentimes that something is a `height` attribute in the
HTML, like `<img src="..." height="300">`. With that attribute and only
`max-width: 100%`, the image gets narrower but stays 300 pixels tall,
and looks squashed. `height: auto` guards against that, which is why the
two declarations usually travel together.

These two lines appear on a great many websites, often in a rule for
every `img` on the page. A phone screen is often narrower than the
photos we put on a page, so without them a site can scroll sideways on a
phone.

## Now in your own site

On [Images, paths and alt text](tutorial:images-and-alt-text) you added
an image to your fork.

1. Open your fork and find that image in the HTML.
2. Open `styles.css`. Can you find `max-width: 100%` and `height: auto`
   for that image? They may be on a rule for the image itself, or on a
   rule that reaches it, such as one for every `img`.
3. If they are missing, you could add them.
4. Save, and refresh.
5. Make your browser window narrow, about the width of a phone.

Does your image stay inside the edge of the page at every width?

## What we have now

We can now make an image fit its container at any width, on any screen.

| Word | Meaning | Example |
|---|---|---|
| `max-width: 100%` | Sets the widest an image may be: the width of its container | `img { max-width: 100%; }` |
| `height: auto` | Works out the height from the width, so the image keeps its shape as it shrinks | `img { height: auto; }` |
| *aspect ratio* | The link between an element's width and its height | 500 by 300 |
