---
title: "Placing an image, and the path that finds it"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# Placing an image, and the path that finds it

What happens when a browser cannot find the image we asked for? On this
page we:

- ask for an image that does not exist, and see what the browser shows
- learn how the `<img>` tag finds an image, with a web address or a
  path
- put an image of your own on your site

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
2. Now change `does-not-exist.jpg` to `https://picsum.photos/400/300`.
   If you are online, what happens?
3. Take the `https://` away from the start, so that the address is
   `picsum.photos/400/300`. Does the image still load?

## Why does this happen?

Now we can explain what we saw. In step 1, the browser looked for a
file called `does-not-exist.jpg`, and found nothing. Something still
appeared: most browsers show the words from `alt` in place of the
image, and some also show a small broken-image icon. Those words are
the subject of the next page, [Describing an image with alt
text](tutorial:describing-an-image).

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

### Two kinds of address

The address in `src` can be one of two kinds. It can be a full web
address, starting with `https://`, like the `picsum.photos` address in
step 2. Or it can be a *path*. A path is the address of a file inside
your own site, starting from the HTML file that uses it.

| `src` | Where the browser looks |
|---|---|
| `photo.jpg` | In the same folder as the HTML file |
| `images/photo.jpg` | In a folder called `images`, inside the HTML file's folder |
| `../photo.jpg` | In the folder one level up from the HTML file's folder |
| `https://picsum.photos/400/300` | At that full web address, on another site |

Here are the first three paths, drawn as the folders of a small site.
Each one starts from the same HTML file, `index.html`:

![A small site drawn as folders. The outer folder, "projects", holds a file called photo.jpg and a folder called "my-site". Inside "my-site" are the HTML file index.html, a file called photo.jpg, and a folder called "images" that holds a third photo.jpg. Three arrows start from index.html. The arrow labelled "photo.jpg" goes to the photo beside index.html. The arrow labelled "images/photo.jpg" goes into the images folder, to the photo there. The arrow labelled "../photo.jpg" goes up and out of "my-site", to the photo in "projects".](paths.svg)

So a path is a set of directions. Each `/` means "go into this folder".
`..` means "go up one folder". A full web address is different: it
names the site as well, so it finds the same file from any page.

Now we can explain step 3. Without `https://`, the address no longer
starts like a web address. So the browser reads `picsum.photos/400/300`
as a path: a folder called `picsum.photos`, next to the page. There is
no such folder, so the image fails again.

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
4. Write your own caption inside `<figcaption>`.
5. Save, and refresh. Can you see a stand-in image, with your caption
   under it?

Now let's swap the stand-in for a photo of your own, and point at it
with a path. Choose a photo you are happy to put on a public website.

6. Give the photo file a short name, in small letters, with no spaces,
   such as `my-photo.jpg`.
7. Put the file in your fork, in the same folder as `index.html`:
   - **On your own computer:** copy the file into that folder.
   - **On GitHub:** open your fork, click **Add file**, then **Upload
     files**, and drag the photo in. Then commit.
8. In `index.html`, change the `src` of your image from the
   `picsum.photos` address to the photo's file name, such as
   `src="my-photo.jpg"`.
9. Save, and refresh.

Is your own photo on the page now? If not, compare the file name and
the path letter by letter.

## What we have now

We can now place an image on a page, and point to it with a full web
address or with a path.

| Word | Meaning | Example |
|---|---|---|
| `<img>` | Places an image. It has no closing tag. | `<img src="photo.jpg" alt="...">` |
| `src` | The address of the image file | `src="images/photo.jpg"` |
| *path* | The address of a file inside your own site, starting from the HTML file | `images/photo.jpg` |
| `..` | In a path, the folder one level up | `../photo.jpg` |
| `<figure>` | Groups an image with its caption, in `<figcaption>` | `<figure class="profile-image">` |
