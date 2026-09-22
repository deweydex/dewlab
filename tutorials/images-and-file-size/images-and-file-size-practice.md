---
title: "Images and file size — Practice"
practice_for: images-and-file-size
year: "2026-2027"
version: 2026.09.22.1
---

# Images and file size — Practice

On this page we practise getting images ready for a site: a path that
works once the site is published, a format that suits each picture, and
a file size that suits the web. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small image to make, in a cell
- changes in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first.

## Fix the broken page

**1.** An author's site shows a photo on their own computer. Once the
site is published on GitHub Pages, the photo is a broken image. Here is
the folder, as their computer shows it:

```text
my-site/
    index.html
    images/
        Harbour.JPG
```

And here is the line in `index.html`:

```html
<img src="images/harbour.jpg" alt="Fishing boats in the harbour at dawn">
```

Why does it work on their computer, and not once it is published? Fix
it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Compare the file name in the folder with the file name in `src`,
   letter by letter.
2. On [Placing an image, and the path that finds
   it](tutorial:images-and-alt-text) we saw what Windows and a Mac do
   with capital letters in a file name. What do they do?
3. What does GitHub Pages do with them?

**Think about:** which is safer to change: the `src`, or the file's
name?

**Try this next:** the author also has a file called `Boat Trip.jpg`.
What name would you give it, so the same mistake cannot happen?

</details>

<details class="dl-answer"><summary>answer</summary>

The file is called `Harbour.JPG`, with a capital H and a capital JPG.
The `src` says `harbour.jpg`, all in small letters. On Windows and on a
Mac, the two names open the same file, so the photo loads. On GitHub
Pages, they are two different names, and there is no file called
`harbour.jpg`.

The safest fix is to rename the file to `harbour.jpg`, all in small
letters, and keep the `src` as it is. If every file name on the site
uses small letters, with a `-` in place of a space, then there is
nothing to match up.

</details>

**2.** Another author dragged a photo into their editor, and the editor
wrote this line for them. The photo shows on their computer. On the
published site, it is a broken image, for every visitor.

```html
<img src="file:///C:/Users/ana/Desktop/my-site/images/harbour.jpg" alt="Fishing boats in the harbour at dawn">
```

What does this path point at? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Where is `C:/Users/ana/Desktop`? Is it on the web, or on one
   computer?
2. When a visitor opens the published site, which computer does their
   browser look on?
3. On [Placing an image, and the path that finds
   it](tutorial:images-and-alt-text) we met paths that start from the
   HTML file. What would that path be, from `index.html` to the photo?

**Think about:** does a path to a file on your own computer mean
anything on someone else's?

**Try this next:** open one of your own HTML files in your editor, and
search it for `file:` and for `C:`. Are there any?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<img src="images/harbour.jpg" alt="Fishing boats in the harbour at dawn">
```

The path points at one folder on the author's own computer. On their
computer, that file exists, so the photo shows. A visitor's browser
looks for the same path on the visitor's own computer, where there is
no such file. Browsers also refuse to load a `file:` address into a
page that came from the web. A path that starts from the HTML file
works in both places, as long as the `images/` folder is
published with the page.

</details>

## Make this

**3.** An SVG image is a set of instructions for drawing shapes. The
browser follows them at whatever size the image is shown, so the edges
stay sharp. We can write those instructions straight into a page. Here
is a small icon: a circle, with a tick inside it.

```html site
id: images-practice-icon-html
site: images-practice-icon
<svg width="40" height="40" viewBox="0 0 40 40">
  <circle cx="20" cy="20" r="18" fill="#2c7a4b" />
  <path d="M11 21 L17 27 L29 14" stroke="white" stroke-width="4" fill="none" />
</svg>
```

```css site
id: images-practice-icon-css
site: images-practice-icon
body { font-family: sans-serif; }
```

Change the icon:

- make it four times as big: `160` wide and `160` tall
- make the circle a dark blue, `#1f4e79`

Are the edges still sharp at the larger size? Zoom the browser in, too.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The size the icon is shown at is set by `width` and `height` on the
   `<svg>` element.
2. `viewBox="0 0 40 40"` says the drawing inside is measured on a grid
   40 units wide and 40 units tall. Leave it as it is.
3. The circle's colour is its `fill`.

**Think about:** we changed the size the icon is shown at. Did we
change any of the drawing's instructions?

**Try this next:** change `stroke-width` from `4` to `2`. What changes?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<svg width="160" height="160" viewBox="0 0 40 40">
  <circle cx="20" cy="20" r="18" fill="#1f4e79" />
  <path d="M11 21 L17 27 L29 14" stroke="white" stroke-width="4" fill="none" />
</svg>
```

`width` and `height` set the size the icon is shown at. The `viewBox`
keeps the drawing on its own 40 by 40 grid, so the browser draws the
same shapes, four times as big. The edges stay sharp, because the
browser draws them again at the new size. A JPEG or a PNG of this icon,
made at 40 pixels, would look blurred or blocky at 160, because its
pixels would be stretched.

</details>

## In your own site

**4.** List every image your site will use, and choose a format for
each one. Most sites have at least these three kinds of picture:

- a photograph, such as a place, a person or some food
- a logo, made of flat colours and some lettering
- a small icon, such as a phone or an envelope beside your contact
  details

1. Open `planning.md` in your fork of `project_wad`. Find section 3,
   **Design**.
2. At the end of that section, add a line **Images:**, and under it a
   short list: each image, and the format you choose for it.
3. Beside each one, write why, in a few words.
4. Commit the change, with a message such as "Choose image formats".

<details class="dl-answer"><summary>answer</summary>

Your own list depends on your site. For the three kinds above:

| Image | Format | Why |
|---|---|---|
| a photograph | JPEG | It compresses well. The small loss of detail does not show in a photo. |
| a logo of flat colours | SVG, or PNG | SVG stays sharp at any size and is often the smallest. If you only have the logo as a picture file, PNG keeps its flat colours and sharp edges exactly. |
| a small icon | SVG | An icon is a few simple shapes, which is what SVG describes best. |

A PNG also suits a screenshot, and anything with a transparent
background. If you choose JPEG for a logo, look at its edges closely.
JPEG often leaves a faint blur or speckle around sharp lettering.

</details>

**5.** Resize and compress one of your own photos, and measure what you
saved.

1. Choose one photo for your gallery. Before you change it, note its
   width and height in pixels, and its file size. Most computers show
   both in the file's details or properties.
2. Your `.container` is at most `1000px` wide. So no image on your site
   is ever shown wider than that. Resize the photo so it is at most
   `1000` pixels wide.
3. Save it as a JPEG, in your `images/` folder, with a name in small
   letters.
4. Note its new width, height and file size.
5. Use it in `gallery.html`, with a real `alt` description.
6. Commit the change, with a message such as "Add a resized gallery
   photo".

How many times smaller is the new file?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. On Windows, the **Photos** app and **Paint** can both resize an
   image. On a Mac, **Preview** can, under **Tools**, then **Adjust
   Size**.
2. When you save a JPEG, many editors ask for a quality. A value around
   70 to 80 out of 100 usually looks the same as the original.
3. To compare sizes, divide the old file size by the new one. Use the
   same unit for both: KB, or MB.

**Think about:** your photo is now fewer pixels wide. How many times
fewer pixels does it have in all?

**Try this next:** try saving the same photo at quality 40. Can you see
a difference at the size your gallery shows it?

</details>

<details class="dl-answer"><summary>answer</summary>

Your numbers depend on your photo. As an example, a phone photo might
be `4000` by `3000` pixels, and about 4 MB. Resized to `1000` by `750`,
it is a quarter of the width and a quarter of the height. So it has
one sixteenth of the pixels: `750,000` in place of `12,000,000`. Saved
as a JPEG, it might be about 200 KB, which is about twenty times
smaller. In your gallery, the two look the same, because the gallery
never shows the photo wider than `1000px`.

</details>
