---
title: "Looking inside a page with the inspector — Practice"
practice_for: the-inspector
year: "2026-2027"
version: 2026.09.22.1
---

# Looking inside a page with the inspector — Practice

On this page we practise with the inspector. There are three kinds of
problem:

- a small page to look inside, where we find things
- a broken page, where the inspector shows us the mistake
- work in your own site, in the browser and in your files

Each example below has a preview. The preview is a small page of its
own, inside this one. Right-click something inside the preview and
choose **Inspect**, and the inspector opens with that part selected.
Near the top of the preview's page you may see a few lines that this
site adds to make the preview work. You can ignore them.

We have not learned HTML or CSS yet, so no problem here asks you to
write any. We read what the inspector shows, and we change a few words.

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, and its
reason, than from reading the answer.

## Look inside a page

**1.** Here is a very small shop page.

```html site
id: inspector-practice-find-html
site: inspector-practice-find
<h1>The Plushie Shop</h1>
<p class="intro">Soft toys, made by hand.</p>
<ul>
  <li>Squishy Squid <span class="price">€12</span></li>
  <li>Cuddly Cuttlefish <span class="price">€15</span></li>
</ul>
```

```css site
id: inspector-practice-find-css
site: inspector-practice-find
body { font-family: sans-serif; }
.price {
  color: #2672ad;
  font-weight: bold;
}
```

1. Right-click the price `€12` in the preview, and choose **Inspect**.
   Which line of the tree is selected? What word comes straight after
   the `<` at its start?
2. That line also has `class="..."` in it. What is written between the
   quotes?
3. Move the mouse up the tree, to the line that starts with `<ul>`.
   Which part of the preview lights up?
4. Click the price's line again. In the panel of rules beside the tree,
   which rule makes the price blue?

<details class="dl-answer"><summary>answer</summary>

1. The selected line is `<span class="price">€12</span>`. The word
   after the `<` is `span`. That word is the *tag name*. It says what
   kind of part this is.
2. The class is `price`.
3. Both lines of the list light up together. The `<ul>` line holds the
   whole list, so pointing at it shows everything inside it.
4. The rule that starts with `.price`. It sets `color: #2672ad`, and
   the inspector shows a small blue square beside that colour.

We meet tags, classes and rules properly in [HTML: tags, elements and
attributes](tutorial:a-page-is-files) and the pages after it.

</details>

## Fix the broken page

**2.** A shop wants only its weekday hours in bold. The author wrapped
`10 to 6` in `<strong>`, which makes text bold. But the Saturday line is
bold too.

```html site
id: inspector-practice-fixed-html
site: inspector-practice-fixed
<h1>Opening hours</h1>
<p>Monday to Friday: <strong>10 to 6</p>
<p>Saturday: 10 to 4</p>
```

```css site
id: inspector-practice-fixed-css
site: inspector-practice-fixed
body { font-family: sans-serif; }
```

Right-click the Saturday line, and choose **Inspect**. Compare the tree
with the HTML in the editor above. What does the tree show that the
editor does not? Then fix the HTML, so that only `10 to 6` is bold.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. In the editor, `<strong>` starts the bold part. What ends it? Look
   for `</strong>`, with a slash.
2. In the tree, look at the line just above the Saturday paragraph.
   Is there a `<strong>` there that the editor does not have?
3. Remember what the inspector shows: the HTML the browser is using,
   after it has fixed the mistakes it found.

**Think about:** when the browser meets a start with no end, where does
it decide the bold part stops?

**Try this next:** what happens if you move `</p>` in the first line
so that it comes before `10 to 6`?

</details>

<details class="dl-answer"><summary>answer</summary>

The `<strong>` in the first line never ends. There is no `</strong>`.
The browser fixes this as it reads the page. It ends the bold part at
the end of the first paragraph, and then starts a new `<strong>` around
the next paragraph too, to keep the rest of the text bold. The tree
shows that second `<strong>`, around the Saturday paragraph. The editor
has no such line. So the inspector can show HTML that differs
from the file you wrote.

The fix is to end the bold part where it should end:

```html
<h1>Opening hours</h1>
<p>Monday to Friday: <strong>10 to 6</strong></p>
<p>Saturday: 10 to 4</p>
```

Now the tree matches the editor, and only `10 to 6` is bold.

</details>

**3.** The shop's heading should be dark blue, `#2c3e50`. The author
wrote that colour in the first rule. But the heading shows up red.

```html site
id: inspector-practice-crossed-html
site: inspector-practice-crossed
<h1>The Plushie Shop</h1>
<p>Soft toys, made by hand.</p>
```

```css site
id: inspector-practice-crossed-css
site: inspector-practice-crossed
h1 {
  color: #2c3e50;
  font-family: sans-serif;
}
p {
  color: #5f6f73;
}
h1 {
  color: #b03a2e;
}
```

Right-click the heading, and choose **Inspect**. In the panel of rules,
which `color` is crossed out? Which one is used? Fix the CSS so the
heading is dark blue, and keep its font.

<details class="dl-answer"><summary>answer</summary>

The panel lists two rules for `h1`. In the first one, `color: #2c3e50`
is crossed out. The second one, `color: #b03a2e`, is the colour in use,
and that is red. When two rules give the same part of the page a
different value for the same thing, the rule further down the
stylesheet wins. We look at this properly in [The cascade: which CSS rule wins](tutorial:which-rule-wins).

The fix is to delete the second `h1` rule:

```css
h1 {
  color: #2c3e50;
  font-family: sans-serif;
}
p {
  color: #5f6f73;
}
```

Deleting only the line `color: #b03a2e;` works too. Either way, nothing
is crossed out any more, and the heading is dark blue. Notice that
`font-family` was never crossed out, because the second rule did not set
it. Nothing overruled it.

</details>

## Try it in the inspector first

**4.** Here is a product page. The shop wants it changed to say:

- `Squishy Squid (large)` as the heading
- `€14` as the price
- `Only 3 left` in place of `In stock`

```html site
id: inspector-practice-try-html
site: inspector-practice-try
<h1>Squishy Squid</h1>
<p class="price">€12</p>
<p>In stock</p>
```

```css site
id: inspector-practice-try-css
site: inspector-practice-try
body { font-family: sans-serif; }
.price { color: #2672ad; font-size: 1.5rem; }
```

1. Make all three changes in the inspector's **Elements** tab first.
   Double-click a piece of text in the tree, type the new words, and
   press **Enter**.
2. Now go back to the HTML editor above, and type a space at the end of
   any line. What happens to your three changes?
3. Make the same three changes in the HTML editor.

<details class="dl-answer"><summary>answer</summary>

In step 1, each change shows up in the preview straight away. In
step 2, all three disappear. The preview is built again from the code in
the editor each time that code changes. Your changes in the Elements tab
were never in that code. This is the same thing that happens when you
refresh a real page. The browser builds it again from the file, and a
change made only in the inspector is gone.

In step 3, the changes go into the code itself:

```html
<h1>Squishy Squid (large)</h1>
<p class="price">€14</p>
<p>Only 3 left</p>
```

These stay. So the Elements tab is a safe place to try an idea. We keep
the idea in the file.

</details>

## In your own site

**5.** What does a misspelt file name look like? Let's make one on
purpose, in your browser only.

1. Open your home page in your browser. It can be your published site,
   or the file on your own computer.
2. Open the inspector, and go to the **Elements** tab. Near the top, in
   `<head>`, find the line `<link rel="stylesheet" href="styles.css">`.
3. Double-click `styles.css` on that line. Change it to `style.css`,
   with no `s` after `style`, and press **Enter**.
4. What happens to the page?
5. Open the **Console** tab. What does it say, and which file does it
   name?
6. Refresh the page. What comes back?

<details class="dl-answer"><summary>answer</summary>

The page loses all its styles. The dark header and footer turn white,
the text changes to the browser's plain default font, and the cards
lose their shadows. The page's content is all still there.

The Console shows an error in red that names `style.css`, and says it
could not be loaded. On your published site, the error says the server
answered with `404`, which means "not found". On your own computer, it
says the file was not found. You may also see an error that names
`favicon.ico`. That is the small icon in a browser tab. Browsers ask for
it by themselves, and the starter does not have one yet.

The refresh brings everything back. It reads your real `index.html`,
which still says `styles.css`. If a page of yours ever loses its styles
like this, compare the name in the `<link>` line with the real file
name, letter by letter.

</details>

**6.** The Elements tab is a good place to try words out before you
change a file. Let's use it to choose a new main heading.

1. Open your home page in your browser. Right-click the large heading
   at the top, and choose **Inspect**. In the starter, it says
   "Welcome to My Portfolio". If you did Exercise 4 in the starter's
   README, you see your own heading instead.
2. Double-click the heading's words in the tree. Try two or three
   different headings. Which one reads best? Does it fit on one line?
3. Open `index.html` in your editor. Find the `<h1>` near the top of
   `<main>`. The comment under it mentions Exercise 4.
4. Replace the words between `<h1>` and `</h1>` with the heading you
   chose. Save the file.
5. Commit the change, with a message such as "Change the main heading".
   If you work on your own computer, push it too.

Wait a minute or two, then refresh your published site. Does its
heading match the one you chose in the inspector?

<details class="dl-answer"><summary>answer</summary>

Your tries in step 2 changed the page in your browser only. Steps 3 to 5
make the change real. The new heading is in the file, in a
commit, and on GitHub. Once GitHub Pages has rebuilt the site, anyone
who visits sees it.

If the heading on your published site has not changed, look back at
[Saving and publishing a change](tutorial:the-two-loops#why-is-my-change-not-showing).
Did the change reach GitHub, and has the site had time to rebuild?

</details>
