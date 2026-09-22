---
title: "Changing the layout for phones: media queries"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Changing the layout for phones: media queries

A phone has much less room than a laptop. How can one stylesheet suit
both? On this page we:

- write CSS that applies only at some widths
- find the width where that CSS switches on
- add a rule for very small screens to your own site

## Let's try it

The HTML has one message. The CSS has a rule for the message, and then
a second rule for it, inside an `@media` block.

```html site
id: media-html
site: media
<p class="msg">Watch me as the preview gets narrower.</p>
```

```css site
id: media-css
site: media
.msg { background: #f6f4f0; padding: 12px; font-weight: bold; }
@media (max-width: 350px) {
  .msg { background: #d9720c; color: white; }
}
```

The preview has a **Preview width** slider. Beside it, a number shows
the preview's width in pixels.

1. Drag the slider slowly from wide to narrow. Does anything about the
   message change along the way? Watch the number: at about what width
   does it happen?
2. Does anything else on the page change at the same moment?
3. What happens if we change `350px` to `500px`? Does the change come
   sooner or later as we drag?
4. What happens if we change `max-width` to `min-width`?

## Why does this happen?

Now we can explain what we saw. While the preview was wide, the message
kept its normal look. At about 350 pixels, it changed colour, and
nothing else on the page was touched.

A *media query* wraps a block of CSS in a condition. The rules inside
apply only while the condition is true. Outside that condition, the
rules inside do nothing at all.

```css
@media (max-width: 350px) {                     /* the condition */
  .msg { background: #d9720c; color: white; }   /* used only while it is true */
}
```

The condition here is about width, the most common kind. It tests the
width of the *viewport*. The viewport is the part of the browser window
that shows the page. On a phone, that is most of the screen. In our
example, the viewport is the preview itself, and that is why the slider
turns the rule on and off.

- `max-width: 350px` means "when the viewport is 350 pixels wide or
  narrower".
- `min-width` works the other way. `min-width: 350px` means "when the
  viewport is 350 pixels wide or wider". In step 4, the rule applied
  above that width, not below it.

Here are the two conditions on one line of widths:

![A line of widths from 0 to 600 pixels, with a mark at 350. Above the line, a band runs from 0 up to the mark, labelled max-width: 350px, applies at 350 pixels or narrower. Below the line, a band runs from the mark up to 600 and beyond, labelled min-width: 350px, applies at 350 pixels or wider. The mark at 350 is the breakpoint where each one switches on or off.](media-query-ranges.svg)

The word `max-width` also appeared on [A readable width, centred
on the page](tutorial:the-container). The name is the same, but the job
is different. There, `max-width` sets the widest an element can grow.
Inside `@media ( )`, it tests the width of the viewport.

A *breakpoint* is a width where a media query switches on or off. In
our example, the breakpoint is `350px`. In step 3 we moved it to
`500px`, so the change came sooner as we dragged.

What if a media query and an ordinary rule both set the same property?
While the condition is true, both rules match. When two rules with the
same selector set the same property, the one further down the
stylesheet wins. That is why the `@media` block comes after the
ordinary `.msg` rule. Media queries usually sit at the bottom of a
stylesheet, below the rules they change. [Which rule
wins](tutorial:which-rule-wins) looks at this more closely.

## Now in your own site

1. Open your site in the browser, and open the inspector.
2. Switch it to device mode, also called responsive mode. This mode
   shows the page at the width of a phone or a tablet. In Chrome and
   Edge it is the **Toggle device toolbar** button. In Firefox it is
   **Responsive Design Mode**.
3. Set a narrow width, like a phone's.
4. In your fork, open `styles.css`. Find the `@media (max-width: 768px)`
   block at the bottom.
5. Just below it, a second breakpoint for very small screens is
   already waiting, switched off inside a comment. It starts with
   `/* → Exercise 24` and ends with `*/`. Delete those two comment
   markers to switch it on. The block looks like this:

   ```css
   @media (max-width: 480px) {
       .hero h1 {
           font-size: 1.75rem;
       }

       .container {
           padding: 0 1rem;
       }

       .card {
           padding: 1rem;
       }
   }
   ```

6. Save, and refresh. Is the heading smaller at a phone's width?
7. Change `max-width: 480px` to `max-width: 800px`. At what width does
   the smaller heading start to apply now?
8. Now try `min-width` in place of `max-width`. Does the rule apply
   above that width, or below it?
9. Put the line back to `@media (max-width: 480px)`, and save.

Can you find the width where your heading changes size, and say which
media query caused it?

## What we have now

We can now write CSS that applies only while a condition is true, and
not everywhere at once.

| Word | Meaning | Example |
|---|---|---|
| *media query* | A block of CSS that applies only while a condition, most often about width, is true | `@media (max-width: 768px) { ... }` |
| *viewport* | The part of the browser window that shows the page | |
| *breakpoint* | A width where a media query switches on or off | `768px` |
| `max-width` in a media query | Applies the rules inside at that width or narrower | `@media (max-width: 480px)` |
| `min-width` in a media query | Applies the rules inside at that width or wider | `@media (min-width: 480px)` |
