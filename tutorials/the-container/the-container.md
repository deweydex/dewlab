---
title: "Setting a page's width and centring it"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Setting a page's width and centring it

On a very wide screen, a line of text that runs from one edge to the
other is hard to read. How do we stop a page's content from growing too
wide, and keep it in the middle? On this page we:

- set the widest a box is allowed to grow
- centre that box, however wide the screen is
- find the rule that does this in your own site

## Let's try it

The HTML has one box, with the class `container`, and a paragraph inside
it. The CSS gives the box a white background and a thin border, so we
can see its edges against the grey page.

```html site
id: container-html
site: container
<div class="container">
  <p>Content inside a container.</p>
</div>
```

```css site
id: container-css
site: container
body { margin: 0; background: #ddd; }
.container {
  max-width: 300px;
  margin: 0 auto;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

The preview has a **Preview width** slider. Beside it, a number shows
the preview's width in pixels.

1. Drag the slider from wide to narrow. What does the white box do while
   the preview is wide? What does it do once the preview gets narrower
   than the box?
2. Put the slider back at its widest. What happens if we change
   `max-width` from `300px` to `100%`?
3. Set it back to `300px`. What happens if we change `margin: 0 auto` to
   `margin: 0`?
4. Put `margin: 0 auto` back. Now change the word `max-width` to `width`,
   and keep `300px`. Drag the slider to narrow again. Does the box still
   fit inside the preview?

## Why does this happen?

Now we can explain what we saw.

`max-width` sets the widest an element is allowed to grow. The element
can still be narrower when there is less room. In step 1, the box grew to
`300px` and stopped there in a wide preview. In a narrow preview, it
shrank to fit. With `max-width: 100%` in step 2, the widest it could grow
was the full width of the preview, so it filled whatever room it had.

`width` works differently. `width: 300px` sets one size, and the box
keeps that size whatever is around it. In step 4, once the preview was
narrower than the box, the box ran past the preview's right-hand edge.

| Declaration | In a wide preview | In a narrow preview |
|---|---|---|
| `max-width: 300px` | The box grows to `300px` and stops | The box shrinks to fit |
| `width: 300px` | The box is `300px` wide | The box stays `300px` wide, and runs past the edge |

Now the margin. On [The box model: padding, border and
margin](tutorial:the-box) we saw that when `margin` has two values, the
first sets the top and bottom, and the second sets the left and right.
So `margin: 0 auto` sets the top and bottom margins to `0`, and the left
and right margins to `auto`.

An *auto margin* is a margin set to `auto`. When an element's width is
capped, as this one's is, there is space left over beside it. Auto
margins on its left and right split that leftover space evenly, which
centres the element. `margin: 0 auto` is the usual way to write that. In
step 3, `margin: 0` took the auto margins away, so the box moved over to
the left.

A *container* is an element that holds most of a page's content, and
sets how wide that content can grow and where it sits. The box in our
example is a small container. Many websites wrap their content in one
like it, often with a class name such as `container` or `wrapper`.

Sometimes we might notice that `margin: 0 auto` seems to do nothing.
What is the first thing to check? Look for a `max-width` or a `width`.
Without one, the box already fills the whole width of the page, so there
is no leftover space for the auto margins to split.

We can also see auto margins in [the browser
inspector](tutorial:the-inspector). When we point at an element there,
most browsers shade its margin in its own colour. On a centred
container, the two auto margins show up as two equal bands, one on each
side.

## Now in your own site

In your fork, `styles.css` has a `.container` rule. It sets
`max-width: 1200px` and `margin: 0 auto`. The change in steps 1 and 2 is
easiest to see with your browser window as wide as it goes.

1. Change `max-width` to `600px`. Save, and refresh. What happens to the
   page's content?
2. Now try `max-width: 100%`. How does the content compare?
3. Put `max-width` back to `1200px`.
4. Remove `margin: 0 auto` for a moment. Save, and refresh. Does the
   container stay in the middle, or line up on the left?
5. Put `margin: 0 auto` back.

Can you see the leftover space on either side of your content, split
evenly between the two auto margins?

## What we have now

We can now keep a box at a sensible width, in the middle of the page,
however wide the screen is.

| Word | Meaning | Example |
|---|---|---|
| `max-width` | The widest an element is allowed to grow. It can still be narrower when there is less room. | `max-width: 1200px;` |
| *auto margin* | A margin set to `auto`. When an element's width is capped, auto margins on its left and right split the leftover space evenly, which centres it. | `margin: 0 auto;` |
| *container* | An element that holds most of a page's content, and sets how wide that content can grow and where it sits | `.container` |
