---
title: "Images that shrink to fit the screen — Practice"
practice_for: flexible-images
year: "2026-2027"
version: 2026.09.22.1
---

# Images that shrink to fit the screen — Practice

On this page we practise images that fit their space: `max-width: 100%`
and `height: auto`. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first, and drag the **Preview width** slider
as you go. Most of these mistakes only show on a narrow screen, or only
on a wide one.

## Fix the broken page

**1.** This photo shrinks on a narrow screen, as it should. But look at
its shape when the preview is narrow.

```html site
id: img-practice-squash-html
site: img-practice-squash
<img class="photo" width="500" height="300" alt="A test photo, 500 by 300"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='300'%3E%3Crect width='500' height='300' fill='%232c3e50'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='28' text-anchor='middle' dominant-baseline='middle'%3E500x300%3C/text%3E%3C/svg%3E">
```

```css site
id: img-practice-squash-css
site: img-practice-squash
.photo {
  max-width: 100%;
}
```

Drag the slider to about `300px`. Is the photo still the shape of the
file, 500 by 300? Fix the CSS so it keeps its shape at every width.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the HTML. What does the `height` attribute say?
2. As the photo gets narrower, does its height change at all?
3. Which declaration lets the browser work out the height from the
   width?

**Think about:** the tutorial's example had no `height` attribute. Why
did it not need to worry about this?

**Try this next:** what happens if we delete the `height` attribute
from the HTML instead, and leave the CSS alone?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.photo {
  max-width: 100%;
  height: auto;
}
```

The `height="300"` attribute sets the photo's height. `max-width: 100%`
makes the photo narrower on a narrow screen, but nothing changes its
height, so it stays `300px` tall and looks squashed. `height: auto`
tells the browser to work out the height from the width, so the photo
keeps its aspect ratio. When the photo is `300px` wide, it is `180px`
tall.

</details>

**2.** This orange badge is `120px` square. The author wanted it to
shrink on a very small screen, and to stay at its own size everywhere
else.

```html site
id: img-practice-stretch-html
site: img-practice-stretch
<img class="badge" alt="An orange badge, 120 by 120"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Crect width='120' height='120' fill='%23d9720c'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='18' text-anchor='middle' dominant-baseline='middle'%3E120x120%3C/text%3E%3C/svg%3E">
<p>Our best-selling plushie this week.</p>
```

```css site
id: img-practice-stretch-css
site: img-practice-stretch
.badge {
  width: 100%;
  height: auto;
}
```

How big is the badge in a wide preview? Change one property so the
badge is never bigger than its own file.

<details class="dl-answer"><summary>answer</summary>

```css
.badge {
  max-width: 100%;
  height: auto;
}
```

`width: 100%` makes the image exactly as wide as its container, at
every width. In a wide preview, that stretches a `120px` badge to fill
the whole page, and a stretched image looks blurry. `max-width: 100%`
only sets the widest it may be. The badge keeps its own `120px`, and
shrinks only when the space is narrower than that.

</details>

**3.** The author wanted this photo to fit a phone screen. On a wide
screen it should keep its own size, `500px`.

```html site
id: img-practice-unit-html
site: img-practice-unit
<img class="photo" alt="A test photo, 500 by 300"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='300'%3E%3Crect width='500' height='300' fill='%232c3e50'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='28' text-anchor='middle' dominant-baseline='middle'%3E500x300%3C/text%3E%3C/svg%3E">
```

```css site
id: img-practice-unit-css
site: img-practice-unit
.photo {
  max-width: 100px;
  height: auto;
}
```

How wide is the photo on a wide preview? Fix the CSS.

<details class="dl-answer"><summary>answer</summary>

```css
.photo {
  max-width: 100%;
  height: auto;
}
```

The author typed `px` where they meant `%`. `max-width: 100px` caps the
photo at `100px` wide on every screen. `max-width: 100%` caps it at the
width of its container, which is the whole page here.

</details>

## Make this

**4.** Build a product card with a photo in it. Here is what it should
look like:

- the card has a `max-width` of `300px`, `12px` of padding, and a
  `1px solid #ccc` border
- the photo fills the width of the card, inside the padding, and keeps
  its shape
- on a screen narrower than the card, the card and the photo shrink
  together

```html site
id: img-practice-card-html
site: img-practice-card
<div class="card">
  <img alt="A test photo, 600 by 400"
       src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='400'%3E%3Crect width='600' height='400' fill='%23456'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='28' text-anchor='middle' dominant-baseline='middle'%3E600x400%3C/text%3E%3C/svg%3E">
  <p>Nautical Nautilus, €15</p>
</div>
```

```css site
id: img-practice-card-css
site: img-practice-card
.card {
  /* your rules here */
}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the card. Which property stops a box from growing past a
   width, without fixing its width? We met it on [A readable width,
   centred on the page](tutorial:the-container).
2. The photo's file is `600px` wide. Is that wider or narrower than the
   card?
3. You need a rule for the image inside the card. A descendant
   selector, such as `.card img`, can reach it.

**Think about:** the image's container is the card. So what does
`100%` mean for this image?

**Try this next:** your starter's `.profile-image img` rule uses
`width: 100%`. Would that work here too?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.card {
  max-width: 300px;
  padding: 12px;
  border: 1px solid #ccc;
}
.card img {
  max-width: 100%;
  height: auto;
}
```

The card's `max-width` stops it growing past `300px`, and lets it
shrink on a narrower screen. The image's container is the card, so `max-width:
100%` means "no wider than the inside of the card". The file is wider
than that, so the image always fills the card. `width: 100%` works here
too, for the same reason. It would only behave differently with an image
smaller than the card.

</details>

## In your own site

**5.** Your starter has rules for the picture inside
`<figure class="profile-image">`. But a picture outside that figure
has no rule at all. Let's see what happens to one, and then give every
image a safe default.

1. In `index.html`, find the card under "A Little About Me". Just
   before its "Read More" link, add a large picture:

   ```html
   <img src="https://picsum.photos/1200/800" alt="A large stand-in picture">
   ```

2. Save, and open `index.html`. Open the inspector's device mode, and
   set a phone's width, such as `375px`. What happens to the picture?
   Can you scroll the page sideways?
3. In `styles.css`, find the section called Images. At the top of that
   section, before the `.profile-image` rule, add:

   ```css
   img {
       max-width: 100%;
       height: auto;
   }
   ```

4. Save, and refresh. Does the picture fit inside the card now?
5. You can keep the picture, or take it out again. Either way, keep the
   new `img` rule.
6. Commit the change, with a message such as "Make every image fit its
   container".

Why is the `img` rule a good thing to keep, even once the large picture
is gone?

<details class="dl-answer"><summary>answer</summary>

Without the new rule, the picture shows at the size of its file,
`1200px` wide. On a phone's width, it runs far past the right-hand edge
of the card, and the whole page can scroll sideways. With the rule, the
picture is never wider than the card's content, and `height: auto`
keeps its shape.

The rule is a safe default for every image you add later. You do not
have to remember to write a rule for each one. The `.profile-image img`
rule still applies to your figure, because it is more specific, and it
comes later in the file.

</details>
