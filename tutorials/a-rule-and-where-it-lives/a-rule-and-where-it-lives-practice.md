---
title: "CSS rules and stylesheets — Practice"
practice_for: a-rule-and-where-it-lives
year: "2026-2027"
version: 2026.09.22.1
---

# CSS rules and stylesheets — Practice

On this page we practise writing CSS rules, and finding them in a
stylesheet. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small page to style from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

## Fix the broken page

When a browser meets CSS it cannot understand, it does not show an
error. It skips that part and carries on. So each broken page below
looks calm. Only the result is wrong.

**1.** The heading on this page should be dark blue. It stays black.

```html site
id: rule-practice-spelling-html
site: rule-practice-spelling
<h2>Opening hours</h2>
<p>Monday to Friday, 9 to 5.</p>
```

```css site
id: rule-practice-spelling-css
site: rule-practice-spelling
h2 {
  colour: darkslateblue;
}
```

The selector is right, and `darkslateblue` is a real colour. So what is
wrong? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
h2 {
  color: darkslateblue;
}
```

CSS property names use American spelling, so the property is `color`,
with no `u`. The browser does not know a property called `colour`, so
it skips the whole declaration. Many people in Ireland and Britain make
this mistake, because `colour` is how we spell the word everywhere
else.

</details>

**2.** Both paragraphs should be firebrick red, and in italics.
`font-style: italic` is the declaration that makes text slanted. Neither
change shows up.

```html site
id: rule-practice-semicolon-html
site: rule-practice-semicolon
<p>Free delivery this week.</p>
<p>New plushies every Friday.</p>
```

```css site
id: rule-practice-semicolon-css
site: rule-practice-semicolon
p {
  color: firebrick
  font-style: italic;
}
```

Look closely at the end of each declaration. Can you find the mistake?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A declaration is a property, a colon, a value, and then one more
   character. Which character?
2. Compare the two declarations. Do they both end the same way?
3. Where does the browser think the first value stops?

**Think about:** without that character, how does the browser know
where one declaration ends and the next one starts?

**Try this next:** what happens if the semicolon is missing from the
*last* declaration in a rule, just before the `}`?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
p {
  color: firebrick;
  font-style: italic;
}
```

The first declaration had no semicolon at the end. The semicolon is what
tells the browser that a declaration has ended. Without it, the browser
reads everything up to the next semicolon as one value:
`firebrick font-style: italic`. That is not a colour, so the browser
skips it, and both changes are lost.

And the *Try this next*? The semicolon after the last declaration is
optional, because the `}` ends the rule anyway. Most people write it
every time. Then adding another declaration later cannot break the one
above it.

</details>

**3.** The heading should be dark blue, and the paragraph firebrick. The
heading works. The paragraph stays black.

```html site
id: rule-practice-brace-html
site: rule-practice-brace
<h2>Opening hours</h2>
<p>Monday to Friday, 9 to 5.</p>
```

```css site
id: rule-practice-brace-css
site: rule-practice-brace
h2 {
  color: darkslateblue;

p {
  color: firebrick;
}
```

The `p` rule looks right on its own. So why does it do nothing? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the `{` characters, and then count the `}` characters. Is
   there the same number of each?
2. Where does the `h2` rule end?
3. If the `h2` rule never ends, where does the browser think the `p`
   rule is?

**Think about:** why does the `h2` rule still work?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
h2 {
  color: darkslateblue;
}

p {
  color: firebrick;
}
```

The `h2` rule had no closing `}`. So the browser read the `p` rule as
part of the `h2` rule, inside its braces. Read that way, the `p` rule
no longer matches the paragraph. The `h2` rule still worked, because
its declaration came before the mistake.

A good habit: type the `{` and the `}` together, and then write the
declarations between them. Many editors do this for us.

</details>

## Make this

**4.** Style this page with three rules, one for each kind of element:

- the heading is `darkslateblue`
- both paragraphs are `dimgray`
- the emphasised word is `firebrick`

We have only met the selector `p` so far. Can you work out the selectors
for the heading and the emphasised word from their tags?

```html site
id: rule-practice-three-html
site: rule-practice-three
<h1>Squishy Squid</h1>
<p>A soft squid with eight long arms.</p>
<p>Only <em>twelve</em> left in the shop.</p>
```

```css site
id: rule-practice-three-css
site: rule-practice-three
/* your rules here */
```

<details class="dl-answer"><summary>answer</summary>

```css
h1 {
  color: darkslateblue;
}

p {
  color: dimgray;
}

em {
  color: firebrick;
}
```

A tag name works as a selector for every kind of element, not only for
`p`. The selector `h1` matches every `<h1>`, and `em` matches every
`<em>`.

Notice that `twelve` is firebrick, even though it sits inside a `dimgray`
paragraph. The `em` rule is written for the `<em>` element itself, so it
sets that element's colour.

</details>

**5.** Here is a notice. Style it with one rule that holds two
declarations:

- the text is `darkgreen`
- the background is `honeydew`

The property for a background colour is `background-color`.

```html site
id: rule-practice-notice-html
site: rule-practice-notice
<p>Your order is on its way.</p>
```

```css site
id: rule-practice-notice-css
site: rule-practice-notice
/* your rule here */
```

<details class="dl-answer"><summary>answer</summary>

```css
p {
  color: darkgreen;
  background-color: honeydew;
}
```

One rule can hold as many declarations as we need. Each one goes on its
own line and ends with a semicolon. Notice that the background fills
the whole width of the preview, and not only the words. A paragraph is
a box as wide as the page, and the background colours the whole box.

</details>

## In your own site

**6.** In your fork, we break the link to the stylesheet on purpose,
mend it, and then add a rule of our own.

1. Open `about.html`, and find the `<link>` tag in its `<head>`.
2. Change `href="styles.css"` to `href="style.css"`, with no `s` at the
   end of `style`. Save, and open `about.html` in your browser. What
   happens to the page?
3. Put the `s` back. Save, and refresh. Is everything back?
4. Now open `styles.css`, and find section 3, Typography. It has a rule
   `h2 { font-size: 2rem; }`.
5. Add a second declaration to that rule, so it reads
   `h2 { font-size: 2rem; color: darkslateblue; }`. Save, and refresh
   both pages.
6. Commit the change, with a message such as "Make h2 headings dark
   blue".

Which `h2` headings change colour? If you added the contact section to
your home page, does its heading change too?

<details class="dl-answer"><summary>answer</summary>

With the wrong `href`, the page loses every style at once. The text is
black on white, the headings use the browser's own sizes, and the
links are blue and underlined. The browser looked for a file called
`style.css`, found nothing, and so had no rules to apply. No error
appears on the page. So when every style on a page disappears together,
the `<link>` tag is a good first place to look. A file saved in a
different folder breaks the link in the same way.

After step 5, the headings on white backgrounds turn dark blue, on both
pages, because both pages link to the same `styles.css`. The heading
"Get In Touch" in the contact section stays white. Further down,
`styles.css` has a rule `.contact-section h2` that sets the colour of
that one heading to white, and it wins.
[Choosing what to style: selectors and
classes](tutorial:selectors-and-classes) explains that kind of selector.

</details>
