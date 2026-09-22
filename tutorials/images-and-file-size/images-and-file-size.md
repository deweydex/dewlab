---
title: "Images and file size"
year: "2026-2027"
version: 2026.09.11.1
covers:
  an-images-folder:
    touches: [WA-LO8]
  choosing-a-format:
    covers: [WA-LO4]
  keeping-file-size-down:
    covers: [WA-LO4]
  now-in-your-own-site:
    touches: [WA-LO2, WA-LO4]
---

# Images and file size

How large is a photo file? One taken on a phone can be five megabytes (MB). A
megabyte is about a thousand kilobytes (KB). The same photo, resized for
a web page, is often under 200 KB. That is twenty-five times smaller,
and a visitor never notices the difference.

## An images folder

We keep every image in one folder, usually named `images/`. This is
tidier than leaving images loose beside the HTML files. A path like `images/hero.jpg` then tells us
two things: where the file lives, and that it is an image.

```html
<img src="images/hero.jpg" alt="A description of what's in the image">
```

What if a path like this shows a broken image? Check that the folder
name and the file name match exactly, including capital letters.
`Images/Hero.JPG` and `images/hero.jpg` are two different paths on
GitHub Pages. As we saw on [Images, paths and alt
text](tutorial:images-and-alt-text), a wrong capital letter can still
work on Windows or a Mac, and then break once the site is published.

## Choosing a format

A *format* is the way an image file stores its picture. The end of the
file name shows it, like `.jpg`. Three formats cover most web images:

| Format | Suits | Why |
|---|---|---|
| *JPEG* (`.jpg`) | a photograph | It compresses well. It loses some exact detail, but a photo rarely needs that detail. |
| *PNG* (`.png`) | a screenshot, a logo, or anything with a transparent background | It loses no detail. The file is larger than a JPEG of the same photo. |
| *SVG* (`.svg`) | a simple icon, or a logo made of flat shapes | It describes the image as instructions, not pixels. It stays sharp at any size, and it is usually the smallest of the three. |

## Keeping file size down

Before we add a photo to a site, we resize it to about the size it will
show at. Why? CSS scales an image down to fit, however large the file
underneath is, and the visitor still downloads the whole file. To
*compress* an image is to store it in a smaller file.

An image twice as wide as it needs to be is also twice as tall. So it
has four times as many pixels, and a much larger file, for no visible
benefit. Many image editors, including some on phones, can resize and
compress an image before you save it.

## Now in your own site

1. In your fork of `project_wad`, add a folder named `images/`.
2. Resize and compress each of your own images.
3. Put them in `images/`.
4. In `gallery.html`, replace the stand-in images with your own, using
   paths like `images/your-file.jpg`.
5. Write a real `alt` description for each one. [Images, paths and alt
   text](tutorial:images-and-alt-text) shows what makes a good one.
6. Save, and refresh.

Does every image in your gallery load?

## What we have now

We can now keep a folder of images sized for the web, not for a camera.

| Word | Meaning | Example |
|---|---|---|
| `images/` | A folder for every image on the site | `images/hero.jpg` |
| *format* | The way an image file stores its picture | `.jpg`, `.png`, `.svg` |
| *compress* | To store an image in a smaller file | a 5 MB photo saved at 200 KB |
| *JPEG* | A format for photographs | `street.jpg` |
| *PNG* | A format for exact detail or a transparent background | `screenshot.png` |
| *SVG* | A format for simple flat shapes, sharp at any size | `logo.svg` |
