---
title: "Images, paths and alt text"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# Images, paths and alt text

What happens when a browser cannot find the image we asked for? On this
page we:

- ask for an image that does not exist, and see what the browser shows
- learn how the `<img>` tag finds an image, and how it describes one
- add an image to your own site

## Let's try it

The HTML below asks for an image. The address points at a file that
does not exist.

```html site
id: image-alt-html
site: image-alt
<img src="does-not-exist.jpg"
     alt="A rescued greyhound asleep on a red sofa">
```

1. Look at the preview. What appears where the image should be?
2. Change the words inside `alt="..."`. Does the preview change?
3. Now change `does-not-exist.jpg` to `https://picsum.photos/400/300`.
   If you are online, what happens? Where did the words from `alt` go?

## Why does this happen?

Now we can explain what we saw. Something still appeared, even though
the image failed. Most browsers show the words from `alt` in its place.
Some also show a small broken-image icon. Those words are doing their
job: they tell us what should be there.

`<img>` is different from the tags we have met so far. It has no closing
tag, and no content between tags. The whole element is one tag with
attributes:

```html
<img src="does-not-exist.jpg"
     alt="A rescued greyhound asleep on a red sofa">
<!-- src: where the image file is -->
<!-- alt: what the image shows, in words -->
```

- The `src` attribute holds the address of the image file.
- The `alt` attribute describes the image in words.

### Paths: where the image is

The address in `src` can be one of two kinds. It can be a full web
address, starting with `https://`, like the `picsum.photos` address in
step 3. Or it can be a *path*. A path is the address of a file inside
your own site, starting from the HTML file that uses it.

| `src` | Where the browser looks |
|---|---|
| `photo.jpg` | In the same folder as the HTML file |
| `images/photo.jpg` | In a folder called `images`, inside the HTML file's folder |
| `https://picsum.photos/400/300` | At that full web address, on another site |

Oftentimes, an image works on our own computer and then breaks on the
published site. Check the spelling of the path first, including capital
letters. On Windows and on a Mac, `Photo.jpg` and `photo.jpg` open the
same file. On GitHub Pages they are two different names, so a path
with the wrong capital letter finds nothing.

### Alt text: what the image shows

A screen reader is software that reads a page aloud for someone who
cannot see it. When it reaches an image, it reads the `alt` text in
place of the image. The same text appears on the page whenever the image
fails to load, as it did in step 1. In step 3, the image loaded, so the
`alt` text was no longer shown. It is still there in the code, for a
screen reader.

Sometimes an image is only there for decoration, and it tells a visitor
nothing new. Then we can write an empty `alt=""`. That tells a screen
reader to skip the image. Leaving out `alt` completely is different. A
screen reader then has no description, and some screen readers read out
the file name in its place.

## Now in your own site

Here is an image, with a caption, to add to your fork:

```html
<figure class="profile-image">
    <img src="https://picsum.photos/400/300" alt="A description of what's in the image">
    <figcaption>A caption for the image</figcaption>
</figure>
```

`<figure>` groups an image with its caption. `<figcaption>` holds the
caption, the short text shown under the image. The `picsum.photos`
address gives you a random stand-in image.

1. In your fork, open `index.html`.
2. Find the about-preview section, or the skills section you added in
   [Semantic HTML: tags that describe their
   content](tutorial:sections-that-mean-something).
3. Paste the code above inside that section.
4. Write your own description in `alt`, in place of the example text.
5. Write your own caption inside `<figcaption>`.
6. Save, and refresh.

Now try two more changes, one at a time:

7. Change `alt` to empty: `alt=""`. Save, and refresh.
8. Remove `alt` completely. Save, and refresh.

Can you see any difference on the page between steps 7 and 8? Both look
the same, but a screen reader treats them differently. When you have
finished, put your own description back in `alt`.

## What we have now

We can now place an image on a page, point to it with a path, and
describe it in words that work even when the image does not.

| Word | Meaning | Example |
|---|---|---|
| `<img>` | Places an image. It has no closing tag. | `<img src="photo.jpg" alt="...">` |
| `src` | The address of the image file | `src="images/photo.jpg"` |
| *path* | The address of a file inside your own site, starting from the HTML file | `images/photo.jpg` |
| `alt` | A description of the image, for a screen reader or a failed load | `alt="A greyhound on a sofa"` |
| `alt=""` | An empty description: the image is decoration, and a screen reader skips it | `alt=""` |
