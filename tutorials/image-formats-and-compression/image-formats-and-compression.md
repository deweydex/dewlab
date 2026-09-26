---
title: "Image formats and compression"
year: "2026-2027"
version: 2026.09.22.1
context_for: [images-and-file-size]
---

# Image formats and compression

Why is a JPEG right for a photo, and wrong for a logo? How can the same
photo be 5 MB on your phone and 200 KB on a web page, and look the same?
This page looks inside image files to answer those questions. It is
background reading for [Images and file size](tutorial:images-and-file-size).
You do not need it to finish that page, but it explains why its advice
works.

On this page we:

- see what a picture is made of, and why a plain copy of a photo is huge
- see the two ways a format makes a file smaller
- see how SVG stores a picture in a different way altogether
- meet two newer formats, and the hidden details a photo can carry

## A picture is a grid of pixels

A photo on a screen is a grid of tiny squares. A *pixel* is one of
those squares, filled with a single colour. A photo from a phone might
be `4000` pixels wide and `3000` tall. That is twelve million pixels.

A computer stores each pixel's colour as three numbers: how much red,
how much green and how much blue. Each number takes one byte. So a
plain copy of that photo, with every number written out, takes
`12,000,000 × 3` bytes: 36 MB. Yet the file on the phone is about 5 MB.
Where did the rest go? The phone saved it in a format that
compresses it. There are two ways to do that.

## Two ways to make a file smaller

A *lossless* format makes a file smaller without changing a single
pixel. Open the file again, and every pixel comes back exactly as it
was. It works by finding patterns. Suppose a screenshot has a row of
two hundred white pixels. A lossless format does not need to write
"white" two hundred times. It can write, in effect, "white, two hundred
times". PNG is lossless.

This works very well on a screenshot or a logo, which have large areas
of one flat colour. It works badly on a photo. In a photo of a sky,
neighbouring pixels are rarely exactly the same colour, so there are
few patterns to find. A PNG of a photo is often several times the size
of a JPEG of the same photo.

A *lossy* format makes a file smaller by throwing some detail away, on
purpose. JPEG is lossy. It is designed around how we see. We notice
the outline of a shape, and a change from light to dark. We notice much
less a tiny change of colour between neighbouring pixels. So JPEG keeps
the first, and stores the second roughly. When we save a JPEG, most
image editors ask for a *quality*, often from 0 to 100. A lower quality
throws more away, for a smaller file.

At a sensible quality, on a photo, we cannot see what was lost. On a
logo or a screenshot, we often can. Sharp edges, such as the edges of
lettering, come out with a faint blur or speckle around them. At a very
low quality, a photo breaks up into small, visible squares.

Oftentimes, one photo gets saved as a JPEG, edited, and saved as a JPEG
again, several times. Each save throws a little more detail away. It is
worth keeping the original photo somewhere safe, and making each web
copy from it, not from the last copy.

GIF is an older lossless format, from the 1980s. It can hold only 256
colours in one image, which is too few for a photo. It can hold a short
animation, and that is the main reason it is still around.

## Shapes, not pixels: SVG

JPEG, PNG and GIF all store a grid of pixels. SVG stores something else:
a list of instructions for drawing shapes. A circle in an SVG file is
one line:

```html
<circle cx="20" cy="20" r="18" fill="#2c7a4b" />
```

It says: a circle, with its centre at 20 across and 20 down, a radius of
18, filled with green. An SVG file is plain text, and you can open it in
the same editor you use for HTML.

When a browser shows an SVG, it follows the instructions at whatever
size the image is shown. So the edges are always as sharp as the screen
allows. A grid of pixels can only be stretched. Here is the same circle
stored both ways, and shown much bigger than it was made:

![Two large circles side by side, both shown much bigger than they were made. The left one was stored as a small grid of pixels: its edge is a staircase of square blocks. The right one was stored as SVG instructions: its edge is a smooth curve.](pixels-and-shapes.svg)

That is why SVG suits an icon or a logo made of flat shapes. It does
not suit a photo, because a photo is not made of a few simple shapes.

## Screens with more pixels

Many phones and laptops have screens with two or three real pixels for
every pixel in CSS. On such a screen, an image shown `500px` wide in CSS
covers `1000` real pixels or more. If the image file is only `500`
pixels wide, the screen has to stretch it, and it can look a little
soft.

So some people save photos at about twice the width they will be shown
at. It is a trade. The photo looks sharper on those screens, and every
visitor downloads a larger file. For a gallery of your own photos, the
size the image is shown at, as the tutorial says, is a fine place to
start.

## Newer formats: WebP and AVIF

Two newer formats do the jobs of both JPEG and PNG, in smaller files.
*WebP* can be lossy or lossless, and can have a transparent background.
A lossy WebP of a photo is often noticeably smaller than a JPEG that
looks the same. *AVIF* is newer still, and its files are often smaller
again.

All the current major browsers can show both. Some image editors, and
some older programs, cannot yet save them, or open them. JPEG, PNG and
SVG remain the safe choice for this course's project.

## What else is in a photo file

A photo file holds more than the picture. It also holds *metadata*:
information about the photo itself. That can include the date and time
it was taken, the make of the camera or phone, and, if the phone's
location setting was on, the exact place where it was taken.

Sometimes we might put a photo taken at home on a public website, and
publish our home's location with it, without knowing. Many image
editors and websites remove this information when a photo is exported
or uploaded, but not all of them do. You can check, and remove it, on
your own computer:

- On Windows, right-click the file, and choose **Properties**. The
  **Details** tab shows the metadata. **Remove Properties and Personal
  Information**, at the bottom, removes it.
- On a Mac, open the photo in **Preview**, and choose **Tools**, then
  **Show Inspector**. If the photo has a location, a tab shows it, with
  a button to remove it.

## What we have now

We can now explain why each format suits the pictures it does, and what
happens to a photo when we make its file smaller.

| Word | Meaning | Example |
|---|---|---|
| *pixel* | One tiny square of a single colour. A picture on a screen is a grid of them. | a photo `4000` pixels wide |
| *lossless* | A way of compressing that keeps every pixel exactly as it was | PNG |
| *lossy* | A way of compressing that throws away detail we are unlikely to notice | JPEG |
| *quality* | A setting, often from 0 to 100, for how much detail a lossy format keeps | a JPEG saved at 75 |
| *WebP* | A newer format that can be lossy or lossless, often smaller than JPEG or PNG | `photo.webp` |
| *AVIF* | A newer format again, often smaller than WebP | `photo.avif` |
| *metadata* | Information about a photo, stored inside its file: the date, the camera, sometimes the place | the location a phone recorded |

## Where to read more

CrashCourse (2017). *Compression: Crash Course Computer Science #21.*
<https://www.youtube.com/watch?v=OtDxDvCpPL4>. The two ways to make a file
smaller, keeping everything or losing a little on purpose, explained with
text, sound and pictures. Thirteen minutes.

Branch Education (2021). *How are Images Compressed? JPEG In Depth.*
<https://www.youtube.com/watch?v=Kv1Hiv3ox8I>. Step by step, how JPEG
makes a photo about ten times smaller, and what it leaves out. Nineteen
minutes.
