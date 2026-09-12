---
title: "Images and file size"
slug: images-and-file-size
module: web
module_title: "Web authoring"
series: several-pages
version: 2026.09.05.1
---

# Images and file size

A photo straight off a phone can be five megabytes. A version resized
for a web page, doing the same visual job, is usually under two hundred
kilobytes. That is twenty-five times smaller, for a difference a visitor
never notices.

## An images folder

Keep every image in one folder, usually named `images/`, rather than
loose beside your HTML files. A path like `images/hero.jpg` then says
two things at once: where the file lives, and that it is an image rather
than a page.

```html
<img src="images/hero.jpg" alt="A description of what's in the image">
```

If a path like that shows a broken image, check the folder name and the
file name match exactly, including capital letters. `Images/Hero.JPG`
and `images/hero.jpg` are different paths as far as a browser is
concerned.

## Choosing a format

**JPEG** suits a photograph: it compresses well, at some loss of exact
detail a photo rarely needs.

**PNG** suits a screenshot, a logo, or anything needing a transparent
background. It loses no detail, at a larger file size than a JPEG of the
same photo would be.

**SVG** suits a simple icon or a logo made of flat shapes. It describes
the image as instructions rather than pixels, so it stays sharp at any
size and is usually the smallest of the three.

## Keeping file size down

Before adding a photo to your site, resize it to roughly the size it
will actually display at. An image twice as wide as it needs to be costs
twice the download for no visible benefit. CSS scales an image down to
fit, regardless of how large the file underneath still is. Most image
editors, including the ones built into phones, can resize and compress
an image before you save it.

## Your turn

Let's open your fork of `project_wad`. Try adding an `images/` folder,
and replacing the stand-in images in `gallery.html` with your own,
resized and compressed first. Write a real `alt` description for each
one; [Images, paths and alt text](tutorial:images-and-alt-text) covers
what makes a good one.

## What you have now

A folder of images sized for the web, not for a camera.

- **`images/`** — a folder gathering every image, its path saying what
  it is.
- **JPEG, PNG, SVG** — a photo, a graphic needing exact detail or
  transparency, and a simple flat shape, respectively.
