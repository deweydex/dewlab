---
title: "Animation with keyframes — Practice"
practice_for: keyframes-and-the-checkbox-hack
year: "2026-2027"
version: 2026.09.22.1
---

# Animation with keyframes — Practice

On this page we practise `@keyframes`, which names the stages of an
animation, and `animation`, which puts those stages to work. There are
three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small animation to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Watch each preview for a few seconds before you change
anything. To play an animation from the start again, press **Run**.

## Fix the broken page

**1.** This loading circle should turn round and round. It stays still.

```html site
id: keyframes-practice-name-html
site: keyframes-practice-name
<div class="spinner"></div>
```

```css site
id: keyframes-practice-name-css
site: keyframes-practice-name
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.spinner {
  width: 40px;
  height: 40px;
  margin: 20px;
  border: 5px solid #ccc;
  border-top-color: #2c3e50;
  border-radius: 50%;
  animation: spinning 1s linear infinite;
}
```

The keyframes are right, and so is the rest of the `animation` line.
What is wrong?

<details class="dl-answer"><summary>answer</summary>

```css
.spinner {
  width: 40px;
  height: 40px;
  margin: 20px;
  border: 5px solid #ccc;
  border-top-color: #2c3e50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

The first setting in the `animation` line is the name of the
`@keyframes` rule to follow. The rule is called `spin`, but the line
asked for `spinning`. No rule has that name, so there was nothing to
play, and the browser gave no error. The two names must match exactly.

</details>

**2.** This bar should fill up once, over three seconds, and then stay
full. Watch it until the end. Press **Run** to see it again.

```html site
id: keyframes-practice-fill-html
site: keyframes-practice-fill
<div class="track">
  <div class="bar"></div>
</div>
```

```css site
id: keyframes-practice-fill-css
site: keyframes-practice-fill
@keyframes fill {
  0% { width: 0; }
  100% { width: 100%; }
}
.track {
  height: 20px;
  background: #eee;
}
.bar {
  width: 0;
  height: 20px;
  background: #2672ad;
  animation: fill 3s ease-out 1;
}
```

What happens when the animation ends? Fix it, so the bar stays full.
Change only the `.bar` rule.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The animation runs once, because of the `1` at the end of the
   `animation` line.
2. When an animation stops, which style does the element show: the
   last keyframe, or something else?
3. What `width` does the `.bar` rule give the bar, when no animation is
   playing?

**Think about:** in the tutorial, why did the pulsing button look fine
when it stopped after three passes?

**Try this next:** what would happen if the `.bar` rule said
`width: 50%`?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.bar {
  width: 100%;
  height: 20px;
  background: #2672ad;
  animation: fill 3s ease-out 1;
}
```

The bar filled up, and then it was empty again. When an animation
stops, the element goes back to its own normal style. Here the normal
style was `width: 0`, so the bar snapped back to nothing. With
`width: 100%` in the `.bar` rule, the normal style matches the last
keyframe, so the bar stays full. The keyframes still start it at `0`,
so it still fills up.

</details>

**3.** This "Live" sign should fade out and back in, smoothly, over and
over. Watch it for a few passes.

```html site
id: keyframes-practice-blink-html
site: keyframes-practice-blink
<span class="live">Live</span>
```

```css site
id: keyframes-practice-blink-css
site: keyframes-practice-blink
@keyframes fade {
  0% { opacity: 1; }
  100% { opacity: 0; }
}
.live {
  padding: 4px 10px;
  border-radius: 4px;
  background: #c0392b;
  color: white;
  animation: fade 2s ease-in-out infinite;
}
```

The fade out is smooth. What happens at the end of each pass? Fix the
keyframes, so that it fades back in as smoothly as it fades out.

<details class="dl-answer"><summary>answer</summary>

```css
@keyframes fade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
```

At the end of each pass, the sign jumped straight from invisible back
to solid. An `infinite` animation starts again at `0%` as soon as it
reaches `100%`, and the browser fills in nothing between the end of one
pass and the start of the next. So the `100%` stage should match the
`0%` stage, as it does in the tutorial's pulse. Then the fading back
happens inside the pass, between `50%` and `100%`.

</details>

## Make this

**4.** Make this sign swing, like a sign hanging in a shop door:

- at the start and the end of each pass, it is straight
- a quarter of the way through, it is turned `10` degrees
  anticlockwise
- three quarters of the way through, it is turned `10` degrees
  clockwise
- one pass takes `2s`, with `ease-in-out`, and it repeats forever

```html site
id: keyframes-practice-swing-html
site: keyframes-practice-swing
<div class="sign">Open</div>
```

```css site
id: keyframes-practice-swing-css
site: keyframes-practice-swing
.sign {
  display: inline-block;
  margin: 40px;
  padding: 10px 20px;
  border: 3px solid #2c3e50;
  border-radius: 6px;
  font-size: 1.5rem;
}
```

How many stages does your `@keyframes` rule need? Can two of them share
one line?

<details class="dl-answer"><summary>answer</summary>

```css
@keyframes swing {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}
.sign {
  display: inline-block;
  margin: 40px;
  padding: 10px 20px;
  border: 3px solid #2c3e50;
  border-radius: 6px;
  font-size: 1.5rem;
  animation: swing 2s ease-in-out infinite;
}
```

There are four stages, and the start and the end share one line,
`0%, 100%`, because they are the same. A minus angle turns
anticlockwise. The sign already has `display: inline-block`, so a
transform can turn it. The name `swing` is our choice. Any name works,
as long as the `animation` line uses the same one.

</details>

## In your own site

**5.** Let's make the big heading on your home page rise gently into
place when the page loads, and only once.

1. In your fork, open `styles.css`, and find the `.hero h1` rule, in
   the section called Hero Section.
2. Above that rule, add this `@keyframes` rule:

   ```css
   @keyframes rise {
       0% {
           opacity: 0;
           transform: translateY(20px);
       }
       100% {
           opacity: 1;
           transform: translateY(0);
       }
   }
   ```

3. Inside the `.hero h1` rule, add this line:

   ```css
   animation: rise 0.8s ease-out;
   ```

4. Save, and refresh your home page. What does the heading do?
5. Some people set their device to ask for less movement on screen.
   A media query called `prefers-reduced-motion` tells us when they
   have. At the very end of `styles.css`, add this block:

   ```css
   @media (prefers-reduced-motion: reduce) {
       .hero h1 {
           animation: none;
       }
   }
   ```

6. Commit the change, with a message such as "Heading rises in on the
   home page".

The `animation` line has no repeat count. How many times does the
heading rise? And why does it stay where it is when the animation
ends? Open your About page too. Does its heading rise?

<details class="dl-answer"><summary>answer</summary>

The heading fades in and rises `20px` into place, once. With no repeat
count, an animation runs one time. When it ends, the heading goes back
to its own normal style. That style has full opacity and no transform,
which is exactly the `100%` stage, so nothing jumps.

The About page's heading does not rise. The rule is for `.hero h1`, and
the About page has no `.hero` section. Its heading sits in a section
with the class `page-header`.

For someone whose device asks for less movement, the media query sets
`animation: none`, and the heading is in place from the start.
The background page beside the tutorial shows how to test that setting
in the browser, without changing your device.

</details>
