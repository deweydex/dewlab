---
title: "Images, paths and alt text"
slug: images-and-alt-text
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Images, paths and alt text

What happens when a browser cannot find the image you asked for? Try it
below: the address points at a file that does not exist.

```html site=image-alt
<img src="does-not-exist.jpg"
     alt="A rescued greyhound asleep on a red sofa">
```

Something still appears: a broken-image marker, and the words from `alt`
somewhere near it. That text is doing its job even though the image
failed.

## Why this happens

`<img>` has no closing tag and no content between tags; the whole element
is one tag with attributes. Its `src` attribute holds the address of the
image file, either a path to a file in your own site or a full web
address.

Its `alt` attribute describes the image in words. Software that reads a
page aloud for someone who cannot see it, called a screen reader, reads
that description instead of the image. The same text also appears in
place of the image whenever it fails to load, as it just did above.

## Your turn

Let's open your fork and find the about-preview section, or the skills
section you added earlier. Try adding an image:

```html
<figure class="profile-image">
    <img src="https://picsum.photos/400/300" alt="A description of what's in the image">
    <figcaption>A caption for the image</figcaption>
</figure>
```

The `picsum.photos` address gives you a random stand-in image; write
your own description in `alt` rather than leaving the example text. Then
try leaving `alt` empty (`alt=""`), and try removing it completely. Both
look the same on the page, but a screen reader treats them differently.

## What you have now

An image with a description that works even when the image does not.

- **`<img>`** — places an image; has no closing tag.
- **`src`** — the address of the image file.
- **`alt`** — describes the image, for a screen reader or a failed load.
