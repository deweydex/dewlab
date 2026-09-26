---
title: "Placing an image, and the path that finds it — Practice"
practice_for: images-and-alt-text
year: "2026-2027"
version: 2026.09.22.1
---

# Placing an image, and the path that finds it — Practice

On this page we practise the `<img>` tag, and the address in its `src`.
There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, and its
reason, than from reading the answer.

The previews on this page load images from `picsum.photos`, a site that
gives out stand-in images. You need to be online to see them. A preview
has no folders of its own, so a path like `photo.jpg` never finds a file
in a preview. We practise paths in your own site instead.

## Fix the broken page

**1.** This shop wants a photo of its window at the top of its page.
The image does not load.

```html site
id: images-practice-scheme-html
site: images-practice-scheme
<h1>Plushie Shop</h1>
<img src="picsum.photos/400/300" alt="The shop window, full of plushies">
```

The address looks right. What is missing from it? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Is this address a path, or a full web address? How can the browser
   tell?
2. If the browser reads it as a path, where does it look for the file?

**Think about:** what does every full web address start with?

**Try this next:** once it works, change `400/300` to `200/100`. What
do the two numbers set?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<h1>Plushie Shop</h1>
<img src="https://picsum.photos/400/300" alt="The shop window, full of plushies">
```

Without `https://`, the browser does not know that `picsum.photos` is
the name of another site. It reads the address as a path: a folder
called `picsum.photos`, next to the page. There is no such folder, so
the browser shows the alt text in place of the image. With `https://`
in front, it is a full web address again.

</details>

**2.** This image does not load either. Only its alt text shows.

```html site
id: images-practice-attribute-html
site: images-practice-attribute
<h1>Plushie Shop</h1>
<img href="https://picsum.photos/400/300" alt="The shop window, full of plushies">
```

The address is a full web address this time. So what is wrong? Fix it.

<details class="dl-answer"><summary>answer</summary>

```html
<h1>Plushie Shop</h1>
<img src="https://picsum.photos/400/300" alt="The shop window, full of plushies">
```

An `<img>` finds its file with the `src` attribute. `href` is the
attribute a link uses, so the image had no address at all. It is an
easy mix-up, because both attributes hold an address. One way to
remember: `src` is short for "source", where the image comes from.

</details>

## Make this

**3.** Build this in the cell below:

- a figure, holding an image and its caption
- the image comes from `https://picsum.photos/300/200`
- its alt text says "A stand-in photo"
- the caption under it says "Our shop window, some day soon"

```html site
id: images-practice-figure-html
site: images-practice-figure
<!-- your HTML here -->
```

Does the caption sit under the image? What does the preview show if you
break the address on purpose?

<details class="dl-answer"><summary>answer</summary>

```html
<figure>
  <img src="https://picsum.photos/300/200" alt="A stand-in photo">
  <figcaption>Our shop window, some day soon</figcaption>
</figure>
```

The `<figcaption>` goes inside the `<figure>`, after the `<img>`, so the
caption sits under the image. With a broken address, the alt text
shows in place of the image, and the caption stays under it. The two
numbers in the address set the size of the stand-in image: `300` pixels
wide and `200` pixels high.

</details>

## In your own site

**4.** On [Placing an image, and the path that finds
it](tutorial:images-and-alt-text) you put a photo in the same folder as
`index.html`. Most sites keep their images together in one folder,
often called `images`. Let's do the same.

1. Make a folder called `images`, in small letters, and put your photo
   inside it:
   - **On your own computer:** make the `images` folder in the same
     folder as `index.html`, and move your photo into it.
   - **On GitHub:** on your computer, make a folder called `images`, and
     put a copy of your photo inside it. On your fork's page on GitHub,
     click **Add file**, then **Upload files**, and drag the whole
     `images` folder onto the page. Commit.
2. In `index.html`, change the `src` of your image so that the path
   goes into the new folder.
3. Save, and refresh. Does your photo still show?
4. Commit the change, with a message such as "Keep images in their own
   folder".

What path did you write? If `about.html` showed the same photo, what
path would it use?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Where is `index.html`? Where is the photo now?
2. From `index.html`, which folder do we go into to find the photo?
3. A path writes each folder, then a `/`, then the file name.

**Think about:** a path starts from the HTML file that uses it. Where
is `about.html`, compared with `index.html`?

**Try this next:** if a page sat inside a folder called `blog`, next to
the `images` folder, what path would it need to reach your photo?

</details>

<details class="dl-answer"><summary>answer</summary>

With a photo called `my-photo.jpg`, the path is:

```html
<img src="images/my-photo.jpg" alt="A description of what's in the image">
```

`images/` means "go into the folder called `images`", and then
`my-photo.jpg` is the file inside it. `about.html` sits in the same
folder as `index.html`, so it would use the same path. A page inside a
`blog` folder would need `../images/my-photo.jpg`: first up one folder,
out of `blog`, and then into `images`.

On GitHub, the old copy of the photo is still beside `index.html`. You
could delete it: open it on GitHub, and choose **Delete file** from the
**...** menu.

</details>

**5.** A path can work on your own computer, and then fail once the
site is published. Let's see why, on purpose.

1. In `index.html`, change the start of your path from `images/` to
   `Images/`, with a capital I. Save.
2. If you work on your own computer, refresh the page there. Does the
   photo still show?
3. Commit the change. Wait a minute for GitHub Pages, then open your
   published site. Does the photo show there?
4. Change the path back to `images/`, and commit again.
5. Check your published site once more. Is the photo back?

Why can the same path give two different results?

<details class="dl-answer"><summary>answer</summary>

On GitHub Pages, `Images` and `images` are two different names, so the
path with the capital letter finds nothing, and the alt text shows in
place of the photo.

On Windows and on a Mac, the files on your own computer usually treat
`Images` and `images` as the same name. So the photo may still show
there, and the mistake is easy to miss until the site is published.
(On Linux, the capital letter breaks it on your computer too.)

This is one reason to name every file and folder in small letters, with
no spaces. Then there is only one way to write each path.

</details>
