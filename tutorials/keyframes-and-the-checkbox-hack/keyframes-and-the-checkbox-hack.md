---
title: "Animation with keyframes"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-add-your-own:
    touches: [WA-LO9]
---

# Animation with keyframes

On [Moving things smoothly: transforms and transitions](tutorial:transitions-and-transforms),
`transition` animated a change between two states. It needed something
to trigger it, such as `:hover`. Can CSS move something with no trigger
at all? On this page we:

- watch a button that animates on its own, and change how it moves
- see how a `@keyframes` rule and the `animation` property work together
- add a second animation of our own

## Let's try it

Here is one button, and a `@keyframes` rule that describes how it
moves.

```html site
id: pulse-html
site: pulse
<button class="pulse">Loading…</button>
```

```css site
id: pulse-css
site: pulse
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.08);
    opacity: 0.8;
  }
}
.pulse {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background: #2c3e50;
  color: white;
  animation: pulse 1.5s ease-in-out infinite;
}
```

1. Watch the button for a few seconds. What does it do? Did you do
   anything to start it?
2. What happens if we change `1.5s` to `4s`?
3. What if we change `scale(1.08)` to `scale(1.5)`?
4. What if we change `infinite` to `3`? Watch until the button stops.
   How does it look when it stops?

## Why does this happen?

Now we can explain what we saw. The button grows a little, fades a
little, and goes back, again and again. Nothing triggers it. A
`@keyframes` animation moves through several stages on its own, so it
does not need a trigger.

`@keyframes pulse` names three stages. Each stage is a percentage of
the way through the animation:

| Stage | `transform` | `opacity` |
|---|---|---|
| `0%`, the start | `scale(1)`: normal size | `1`: fully solid |
| `50%`, halfway | `scale(1.08)`: a little bigger | `0.8`: a little see-through |
| `100%`, the end | `scale(1)`: normal size | `1`: fully solid |

`opacity` sets how solid an element looks. `1` is fully solid and `0`
is invisible. The rule writes `0%, 100%` together because the start and
the end are the same. The browser fills in every frame between one
stage and the next on its own, the same way it fills in a `transition`.
Here is one pass of the pulse, drawn along a line of time:

![A line of time for one pass of the pulse animation, 1.5 seconds long. Three keyframes are marked on it: 0% at 0 seconds, where the button is its normal size and fully solid; 50% at 0.75 seconds, where it is a little bigger and a little see-through; and 100% at 1.5 seconds, where it is back to normal. Between the keyframes, many small ticks along the line mark the frames the browser fills in on its own, sixty every second on most screens.](pulse-on-a-timeline.svg)

The `animation` line then uses the keyframes. It combines four
settings in one line:

```css
animation: pulse 1.5s ease-in-out infinite;
```

1. `pulse`: the name of the `@keyframes` rule to follow.
2. `1.5s`: how long one pass takes.
3. `ease-in-out`: the speed curve, which is how the animation speeds up
   and slows down.
4. `infinite`: how many times to repeat it. `infinite` means it never
   stops on its own.

A number in place of `infinite`, such as `3`, runs the animation that
many times and then stops. After the last pass, the button goes back to
its own normal style. In step 4, that looks the same as the `100%`
stage, because the `100%` stage matches the button's normal style.

Oftentimes, an animation like this one shows that something is
happening, such as a page loading or a new message arriving. Movement
catches the eye, so it works best on one small thing at a time. Some
people set their device to reduce movement on screen, and a page can
turn an animation off for them. The background page beside this one
shows how.

## Now add your own

The box above is ours to change.

1. In the HTML, add a second button below the loading one, with a class
   of its own.
2. In the CSS, add a new `@keyframes` rule with a new name.
3. Give the new button's class an `animation` that uses the new name,
   with a different duration from `1.5s`. The duration is the
   `animation-duration`, the second setting in the `animation` line.
4. Once both work, try changing the timings or the `transform` values.

Do your two buttons move at different speeds?

## What we have now

We can now make an element move on its own, with no trigger, and
decide how long it takes and how often it repeats.

| Word | Meaning | Example |
|---|---|---|
| `@keyframes` | Names the stages of an animation as percentages. The browser fills in the frames between them. | `@keyframes pulse { 50% { opacity: 0.8; } }` |
| `animation` | Combines a `@keyframes` name with its duration, speed curve and repeat count in one line | `animation: pulse 1.5s ease-in-out infinite;` |
