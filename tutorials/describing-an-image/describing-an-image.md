---
title: "Describing an image with alt text"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# Describing an image with alt text

A screen reader cannot see a picture. So what does it read out when it
reaches one? On this page we:

- compare three images that fail to load, each described in a different
  way
- learn what `alt` is for, and when to leave it empty
- write a real description for the image on your own site

## Let's try it

The HTML below asks for the same missing file three times. Each `<img>`
has a different `alt`: a description, an empty one, and none at all.

```html site
id: alt-text-html
site: alt-text
<p>1. A description:</p>
<img src="does-not-exist.jpg" alt="A rescued greyhound asleep on a red sofa">
<p>2. An empty alt:</p>
<img src="does-not-exist.jpg" alt="">
<p>3. No alt at all:</p>
<img src="does-not-exist.jpg">
```

1. Look at the preview. What appears under each of the three labels?
2. Change the words in the first `alt`. Does the preview change?
3. Change the first `src` to `https://picsum.photos/400/300`. If you are
   online, what happens to the words from `alt`?
4. The second and third images look the same in the preview. Do you
   think a screen reader treats them the same way?

## Why does this happen?

Now we can explain what we saw. *Alt text* is the description of an
image that we write in its `alt` attribute. It stands in for the image
whenever the image cannot be seen.

- **When the image fails to load**, the browser shows the alt text in
  its place. That is what we saw under the first label, and why the
  preview changed in step 2.
- **When a screen reader reaches the image**, it reads the alt text
  aloud, in place of the image. It does this whether the image loaded
  or not. In step 3, the image loaded, so the alt text was no longer
  shown on the page. It is still there in the code, for a screen
  reader.

So each of the three images gives a screen reader something different:

| The `alt` | On the page, when the image fails | A screen reader |
|---|---|---|
| `alt="A rescued greyhound..."` | the words | reads the words |
| `alt=""` | nothing | skips the image |
| no `alt` at all | nothing, or a small broken-image icon | has no description, and some screen readers read out the file name |

An empty `alt=""` is a choice we make on purpose. Sometimes an image is
only there for decoration, and it tells a visitor nothing new. Then an
empty `alt` tells a screen reader to skip it. Leaving out `alt`
completely is different. Nothing tells the screen reader what the image
is, and it may read out a file name like `does-not-exist.jpg`.

### What makes a good description

What should we write in `alt`? Ask what the image is there to say, and
say that, in one short sentence at most.

- **Say what matters here.** "A rescued greyhound asleep on a red sofa"
  tells us much more than "dog".
- **Leave out "image of" or "picture of".** A screen reader usually
  says for itself that it has reached an image.
- **Do not repeat the words next to it.** If a caption already says
  something, the alt text can say something else, or less.
- **Write out any words in the image.** For a logo that shows a shop's
  name, the alt text is the name.
- **Leave it empty for decoration.** A line or a pattern between two
  sections gets `alt=""`.

## Now in your own site

On [Placing an image, and the path that finds
it](tutorial:images-and-alt-text) you put a photo of your own on your
home page, inside a `<figure>`. Its `alt` still has the example text,
"A description of what's in the image".

1. In your fork, open `index.html`, and find your `<img>`.
2. Look at your photo. What is it there to say about you, or about your
   site?
3. Write that in `alt`, in one short sentence. Try not to repeat your
   caption.
4. Save, and refresh.

Now try two more changes, one at a time:

5. Change `alt` to empty: `alt=""`. Save, and refresh.
6. Remove `alt` completely. Save, and refresh.

Can you see any difference on the page between steps 5 and 6? Both look
the same, but a screen reader treats them differently.

7. Put your own description back in `alt`. Save, and commit the change.

Read your alt text and your caption one after the other, out loud. Does
the alt text tell a listener what the photo shows?

## What we have now

We can now describe an image in words that work when the image does
not, or when the visitor cannot see it.

| Word | Meaning | Example |
|---|---|---|
| `alt` | The attribute that holds an image's description | `alt="A greyhound on a sofa"` |
| *alt text* | The description of an image, for a screen reader or a failed load | "A rescued greyhound asleep on a red sofa" |
| `alt=""` | An empty description: the image is decoration, and a screen reader skips it | `<img src="line.png" alt="">` |

## Where to read more

Technology Connections (2018). *Closed Captioning: More Ingenious than You
Know.* <https://www.youtube.com/watch?v=6SL6zs2bDks>. Alt text gives a
picture words; captions give sound words. How captions were added to
television, and who uses them. About twenty minutes.
