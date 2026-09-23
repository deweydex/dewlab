# Problems in the `portfolio_wad` starter

The Web Authoring students fork
[deweydex/portfolio_wad](https://github.com/deweydex/portfolio_wad) as
their own site, and many dewlab pages send them into it. This file lists
the problems found in it at commit `4a79d36` ("Say where the course
lives"), on 23 September 2026, so they can be fixed in the starter itself.
dewlab cannot change that repository.

Every item was checked, not just read. The files were loaded in Chromium,
both as shipped and with every commented-out exercise switched on, and the
computed styles, sizes and contrast ratios were measured. Each suggested
fix was tested the same way.

When an item is fixed in the starter, check the dewlab pages named under
it, then delete the item here.

## Breaks something

### 1. Two buttons have an invisible focus outline

styles.css 432–435: `.btn:focus` draws its outline in
`--primary-color` (`#2c3e50`). Two buttons sit on a background of that
same colour, so a keyboard user cannot see which one has focus. The
contrast ratio is 1.00.

- **Send Me an Email**: index.html 228, in `.contact-section`
  (appears after Exercise 11).
- **Learn More About Me**: index.html 154, in `.hero`. This one is
  visible from the first day.

A third outline is weak. The logo's `a:focus` outline (styles.css
167–169) is `--accent-color` on the header's `--primary-color`: 2.14:1,
under the 3:1 WCAG 1.4.11 asks for.

**Fix**, after `.btn:focus`:

```css
.hero .btn:focus,
.contact-section .btn:focus,
.logo:focus {
    outline-color: var(--white);
}
```

**In dewlab:** the practice for *Styling what the visitor points at:
hover and focus* (`tutorials/hover-and-focus/hover-and-focus-practice.md`)
teaches the contact-button half of this fix as a problem. It stays a good
problem once the starter is fixed, but its first step ("Can you see an
outline?") would then need a new broken case.

### 2. Hovering Send Me an Email hides its label

styles.css 401–404: `.contact-section .btn:hover` changes the
background to near-white (`--light-gray`) but not the text colour. The
text colour comes from two rules of equal weight, `.contact-section .btn`
(line 397, dark) and `.btn:hover` (line 428, white), and the later one
wins. So the label turns white on `#f8f9fa`.

**Fix:**

```css
.contact-section .btn:hover {
    background-color: var(--light-gray);
    border-color: var(--light-gray);
    color: var(--primary-color);
}
```

**In dewlab:** the practice for *Moving things smoothly: transforms and
transitions* asks students to hover this button, and its answer now
mentions what they will see.

### 3. Uncommenting an exercise by deleting only `/*` and `*/` breaks the rule

styles.css 367 (Exercise 22), 374 (Exercise 18) and 586 (Exercise 24):
each block starts with its instruction on the same line as the `/*`, for
example `/* → Exercise 22: Uncomment to add hover effects`. A student who
deletes only the comment markers leaves that text in front of the first
selector, and the browser drops the whole rule without a message:

- Exercise 22: `.card:hover` does nothing.
- Exercise 18: the skills section loses its background, while
  `.skills-section .card` still works, so it looks half done.
- Exercise 24: the whole `@media (max-width: 480px)` block is dropped.

**Fix:** give the instruction a comment of its own.

```css
/* → Exercise 22: delete the two comment markers around the rule below */
/*
.card:hover { ... }
*/
```

The same trap exists in HTML at index.html 189–191, 206–207 and 221–222.
There the leftover "→ Exercise 9 / 8 / 11" text shows up on the page,
which is at least visible. The same fix applies:
`<!-- → Exercise 8: remove the comment markers around the section below -->`
followed by `<!--` section `-->`.

**In dewlab:** *Choosing what to style: selectors and classes*, *Changing
the layout for phones: media queries*, *Styling what the visitor points
at: hover and focus* and the *Semantic HTML* practice already tell
students to delete the whole instruction line, so they avoid this.

### 4. The Skills and Contact links go nowhere until Exercises 8 and 11

index.html 114–115 and about.html 67, 72 and 161 link to `#skills`,
`#contact`, `index.html#skills` and `index.html#contact`. No element has
those ids until the student adds the sections. That includes the About
page's **Contact Me** button.

Exercise 12 (README.md 213) says "Update the links to point to your
sections", but its snippet is the same as what index.html 111–116
already has, so the exercise changes nothing.

**Fix, one of:**

- Ship the nav with only Home and About, so Exercise 12 adds the two
  links, on both pages (`index.html#skills` and `index.html#contact` on
  the About page). The About page's Contact Me button waits until then.
- Keep the links, and reword Exercise 12: "The Skills and Contact links
  are already in the nav, but they did nothing until you added those
  sections in Exercises 8 and 11. Click them now."

## Wrong teaching

### 5. `position: relative` is not the default

README.md 334 (Exercise 20) says "`position: relative`, which is the
default". The default is `static`. Line 477 then lists "static" among
things practised, though no exercise uses it.

**Fix:** "Change it to `position: static`, which is the default, and the
header scrolls away with the content."

### 6. Switching the header to `position: fixed` also shrinks it

Exercise 20's "Explore" step switches `sticky` to `fixed`. A fixed
element with no width shrinks to fit its content, so the header collapses
to about 476px on a 1280px window, with the logo and nav jammed together.
That hides the lesson the step is after, which is that content slides
under a fixed header.

**Fix:** add `width: 100%;` to the `header` rule (styles.css 235–241).
It changes nothing while the header is sticky.

### 7. Removing the `:focus` rule does not hide focus

README.md 377 (Exercise 23) asks students to remove "the `:focus` rule"
and notice they cannot tell where they are. There are four `:focus`
rules, and removing `a:focus` makes Chromium fall back to its own focus
ring, which is clearly visible. The moment the exercise wants does not
happen.

**Fix:** "Add `a:focus, .btn:focus, .main-nav a:focus { outline: none; }`
at the bottom of the file for a moment. Press Tab through the page. Can
you tell where you are? Then delete it."

### 8. Exercise 18 blames specificity for something else

README.md 314 says changing `.skills-section .card` to `.card` shows
specificity at work. It shows a wider selector: the base `.card` rule sets
no border, so there is no conflict to settle.

**Fix:** "This shows how a selector decides which elements a rule reaches.
`.skills-section .card` reaches only the cards in the skills section;
`.card` reaches all of them."

### 9. The 1 / 10 / 100 points model of specificity gives wrong answers

CONCEPTS.md 76–81. By that scoring, eleven classes (110) beat one id
(100). In CSS an id beats any number of classes.

**Fix:** "Compare three counts, left to right: ids, then classes, then
elements. Any id beats any number of classes, and any class beats any
number of elements. `.hero h1` is (0,1,1), `h1` is (0,0,1),
`#contact .btn` is (1,1,0) and `.section .btn` is (0,2,0)."

dewlab teaches specificity this way already, in *The cascade: which CSS rule wins*.

### 10. Two media-query descriptions in CONCEPTS.md are wrong

- Line 135 says the query stacks the navigation vertically. The 768px
  query puts the logo above the nav; the links stay in one centred row,
  which can wrap. At 375px all four links sit on the same line.
  **Fix:** "…to put the logo above the navigation on small screens, and
  centre the links so they can wrap onto a second line."
- Line 141 says `min-width: 1200px` applies "above 1200px". It applies at
  1200px and wider, which line 131 gets right for `max-width`.
  **Fix:** "These rules only apply when the viewport is 1200px or wider."

### 11. "Inherits" is used for two different things

README.md 164 says a new section "inherits" its styling. It is styled
because the `.section` and `.card` rules match it. CONCEPTS.md 38 uses
*inheritance* for values passing down from parent to child, which is the
CSS meaning.

**Fix:** "…already styled, because the `.section` and `.card` rules in
the CSS file match it."

## Minor

### 12. README and the commented-out code disagree

- README.md 300 (Exercise 18) says "Add this near the bottom, before any
  @media rules", but the same rules are already in styles.css 374–382,
  commented out. A student who follows the README gets two copies.
- README.md 350 (Exercise 22) says "Add to your CSS"; styles.css 367
  says "Uncomment".
- README.md 387–396 (Exercise 24) leaves out the `.card { padding:
  1rem; }` that styles.css 596–598 includes.

**Fix:** "Find the commented-out rules in styles.css (search for
'Exercise 18') and switch them on", with snippets that match the file.

### 13. No two cards are ever side by side

README.md 274 (Exercise 15) asks students to "notice how the cards push
away from each other". Every section has one card (index.html 175 and
213, about.html 128), so there is nothing to see.

**Fix:** "…notice how the card now keeps a gap from the heading above it
and from the edges of its section."

### 14. An example uses a class the site does not have

CONCEPTS.md 158 styles `.header`. The site styles the `header` element,
so the example matches nothing if copied. **Fix:** `header {`.

## Checked and fine

- Every text colour pair passes WCAG AA (4.5:1), before and after the
  exercises. The lowest is `.page-subtitle` at 4.97.
- No sideways scrolling at 375px on either page.
- The skip link works, and anchor targets are not hidden under the sticky
  header.
- Headings are in order, the one image has alt text, and the HTML has no
  unclosed tags, repeated ids or bad nesting.
- Exercises 1–25 run in order, and every "→ Exercise N" comment is in the
  right place.
