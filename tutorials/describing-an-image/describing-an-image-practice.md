---
title: "Describing an image with alt text — Practice"
practice_for: describing-an-image
year: "2026-2027"
version: 2026.09.22.1
---

# Describing an image with alt text — Practice

On this page we practise writing alt text: what to say, what to leave
out, and when to leave it empty. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

The images on this page point at files that do not exist. So every
preview shows the alt text, just as a screen reader would read it. For
each image, ask: if I could not see the picture, would these words tell
me what it is there to say?

## Fix the broken page

**1.** The photo of a new plushie has not been uploaded yet, so its alt
text shows in its place.

```html site
id: alt-practice-filename-html
site: alt-practice-filename
<h2>New this week</h2>
<img src="IMG_2041.jpg" alt="IMG_2041.jpg">
<p>Sleepy Seal, €18.</p>
```

What does this alt text tell a visitor who cannot see the photo? The
photo shows a grey seal plushie, curled up asleep on a pillow. Fix the
alt text.

<details class="dl-answer"><summary>answer</summary>

```html
<h2>New this week</h2>
<img src="IMG_2041.jpg" alt="A grey seal plushie, curled up asleep on a pillow">
<p>Sleepy Seal, €18.</p>
```

A file name tells a visitor nothing about the photo. A camera or a
phone gives every photo a name like `IMG_2041.jpg`, and it is easy to
copy that into `alt` without thinking. The alt text should say what
the photo shows. Your words can be different: "A grey seal plushie,
asleep" says enough.

</details>

**2.** This photo has a caption. Look at what shows when the photo fails
to load.

```html site
id: alt-practice-caption-html
site: alt-practice-caption
<figure>
  <img src="squid.jpg" alt="Squishy Squid, €12">
  <figcaption>Squishy Squid, €12</figcaption>
</figure>
```

A screen reader reads the alt text, and then the caption. What would a
listener hear? The photo shows a purple squid plushie, with eight long,
curly arms. Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the alt text and the caption one after the other, out loud.
2. What does the caption already tell the listener?
3. What does the photo show that the caption does not say?

**Think about:** which words tell a listener something that nothing
else on the page tells them?

**Try this next:** if the caption said "A purple squid with eight curly
arms", what would a good alt text be then?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<figure>
  <img src="squid.jpg" alt="A purple squid plushie with eight long, curly arms">
  <figcaption>Squishy Squid, €12</figcaption>
</figure>
```

A listener heard "Squishy Squid, €12" twice, and nothing about the
photo. The caption already gives the name and the price. So the alt
text says what the photo shows: the colour and the shape of the
plushie.

</details>

**3.** A wavy line sits between two sections of this page. It is only
there for decoration.

```html site
id: alt-practice-divider-html
site: alt-practice-divider
<p>Every plushie is made by hand.</p>
<img src="wavy-line.png" alt="A decorative wavy line image">
<p>Delivery is free on every order.</p>
```

What would a screen reader read out between the two paragraphs? Does
the listener need to hear it? Fix it.

<details class="dl-answer"><summary>answer</summary>

```html
<p>Every plushie is made by hand.</p>
<img src="wavy-line.png" alt="">
<p>Delivery is free on every order.</p>
```

The wavy line tells a visitor nothing new, so it gets an empty
`alt=""`. A screen reader then skips it, and the listener goes straight
from one paragraph to the next. Notice that we keep `alt`, and leave it
empty. Without `alt` at all, a screen reader has no description, and
may read out the file name, `wavy-line.png`.

</details>

## Make this

**4.** Here is the top of a shop's page, with three images. None of them
has any alt text yet. Here is what each image shows:

- `logo.png` is the shop's logo: the words "Plushie Shop", in a round
  blue badge.
- `seal.jpg` is a photo of a grey seal plushie, asleep on a pillow.
- `dots.png` is a row of small coloured dots, between two parts of the
  page.

```html site
id: alt-practice-build-html
site: alt-practice-build
<img src="logo.png">
<h1>New this week</h1>
<img src="seal.jpg">
<p>Sleepy Seal, €18. Soft, grey, and always tired.</p>
<img src="dots.png">
<p>Delivery is free on every order.</p>
```

Add an `alt` to each image. Then read the preview from top to bottom.
Does it make sense without the pictures?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each image, ask what it is there to say.
2. The logo has words in it. What should the alt text be?
3. The photo is the plushie itself. What does it show that the
   paragraph under it does not say?
4. The dots say nothing new. What kind of `alt` does decoration get?

**Think about:** which of the three images would a visitor miss, if it
disappeared?

**Try this next:** if the logo were also a link to the home page, what
would a listener need to hear?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<img src="logo.png" alt="Plushie Shop">
<h1>New this week</h1>
<img src="seal.jpg" alt="A grey seal plushie, curled up asleep on a pillow">
<p>Sleepy Seal, €18. Soft, grey, and always tired.</p>
<img src="dots.png" alt="">
<p>Delivery is free on every order.</p>
```

- The logo shows words, so its alt text is those words. The round blue
  badge is only how the words look.
- The photo gets a short description of what it shows. The price and
  the name are already in the paragraph, so the alt text does not
  repeat them.
- The dots are decoration, so they get `alt=""`, and nothing shows in
  their place.

</details>

## In your own site

**5.** Your About page has no image yet. Let's add one, with a caption
and alt text that each say something different.

1. Choose a second photo for your About page. It could show where you
   work, something you made, or something you like.
2. Put the photo in your fork, in the same place as the photo on your
   home page.
3. In `about.html`, straight after the two paragraphs under "My
   Background", add a figure:

```html
<figure class="profile-image">
    <img src="images/my-desk.jpg" alt="">
    <figcaption></figcaption>
</figure>
```

4. Change the `src` to the path of your photo. If your first photo is
   beside `index.html`, and not in an `images` folder, leave out
   `images/`.
5. Write a caption that says why the photo is there.
6. Write alt text that says what the photo shows.
7. Save, and refresh `about.html`.
8. Commit the change, with a message such as "Add a photo to my About
   page".

Read the alt text and then the caption, out loud. Do they say the same
thing twice?

<details class="dl-answer"><summary>answer</summary>

Your words will be your own. Here is one example:

```html
<figure class="profile-image">
    <img src="images/my-desk.jpg" alt="A laptop on a kitchen table, next to a mug of tea and a notebook">
    <figcaption>Where I practise my HTML, most evenings</figcaption>
</figure>
```

The caption says why the photo is there. The alt text says what a
sighted visitor would see. A listener hears both, and learns something
new from each.

If the photo does not show, check the path letter by letter. `about.html`
is in the same folder as `index.html`, so the path is the same as on
your home page. The class `profile-image` gives the figure the same
style as the one on your home page, because both pages use the same
`styles.css`.

</details>
