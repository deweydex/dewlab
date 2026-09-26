---
title: "Documenting what you built — Practice"
practice_for: documenting-what-you-built
year: "2026-2027"
version: 2026.09.22.1
---

# Documenting what you built — Practice

On this page we practise writing the two documents that explain a
finished site: a README, which says what you built, and a maintenance
plan, which says how you would keep it current. There are three kinds
of problem:

- a document with something wrong or missing, which we fix
- a small piece of a document to write from a description
- a change in your own repository, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. The answers here are examples. Your own words will differ,
and that is fine.

## Fix the broken page

**1.** Here is the README from a student's finished site. The template
in `project_wad` asks for more than this. Two things a stranger needs
are missing.

```markdown
# Hill Walks Near Galway

## What this site is

Five pages of short hill walks within an hour of Galway, for people who
walk at weekends and do not want a long drive.

## Pages

| File | Page | What it covers |
|---|---|---|
| `index.html` | Home | The five walks, with a line about each |
| `about.html` | About | Why these walks, and how to read the maps |
| `gallery.html` | Gallery | Photos from each walk |
| `contact.html` | Contact | A form for sending in a new walk |
| `resources.html` | Resources | Weather, maps and safety links |

## Design choices

**Colour scheme and why:** Greens and greys, to match the hills.

## Credits

Photos are my own.
```

Compare it with the headings in your own `readme.md`. Which two things
would you add first?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Open `readme.md` in your fork, and list its headings and bold
   labels.
2. Tick off each one that the README above has.
3. Of the ones left, which would a stranger need first to *see* the
   site? Which would a teacher need to know the site works?

**Think about:** a README is for someone who did not watch you build
the site. What would they want to open, or to trust?

**Try this next:** the Design choices part has only one of its four
lines. Which of the other three would tell a reader the most?

</details>

<details class="dl-answer"><summary>answer</summary>

The two most important missing things are the live address and the
testing:

```markdown
**Live site:** https://your-username.github.io/hill-walks/

## Testing

**Validated with the W3C validators?** HTML: yes. CSS: yes.

**Browsers tested:** Chrome and Firefox on a laptop, Safari on a phone.

**Checked at a phone width?** Yes. The menu stacks below 480px.

**All internal links checked?** Yes, every link on all five pages.
```

Without the address, a stranger has to find where the site is
published. Without the testing part, nobody can tell whether it works
on a phone, or whether every link was checked. The README is also
missing the fonts, where Flexbox and Grid are used, and the challenges.
Those matter too, but a reader can see the site without them.

</details>

**2.** Here is a maintenance plan. It is short. But it does not
answer the three questions a maintenance plan should answer.

```markdown
# Maintenance plan

I will keep the site up to date and fix things when they break. I might
add more stuff later.
```

Rewrite it, so that it answers the three questions from the tutorial.
Use the hill-walks site from problem 1.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The three questions are: how would you add a page later? What would
   you check every so often? What would you build next?
2. "Up to date" is vague. What, on a site of hill walks, could go out
   of date?
3. "Every so often" is vague too. How often, in weeks or months?

**Think about:** could someone else follow your plan, without asking
you what you meant?

**Try this next:** which part of `styles.css` would you change first,
if you added a sixth walk page? Would you need to change it at all?

</details>

<details class="dl-answer"><summary>answer</summary>

One possible plan:

```markdown
# Maintenance plan

## Updating content

To add a new walk page, I would copy `about.html`, rename it, and change
its content. Then I would add a link to it in the navigation on all six
pages, with `aria-current="page"` on its own link only.

## Keeping it working

Every three months, I would check every link on the Resources page,
because weather and map sites move their pages. Each spring, I would
walk each route again, or check a recent report, in case a path has
closed.

## What I would add next

A page for winter walks, and a table comparing the walks by distance and
time.
```

Each part answers one question, with something a reader could do. The
original plan named no step that a reader could take.

</details>

## Make this

**3.** Write the **Pages** table for this site's README. The student
describes it like this:

> My site is about my local football club. The home page has the next
> three matches and a welcome. There is a page about the club's history,
> a page with a table of the players and their positions, a gallery of
> match photos, and a contact page with a form for joining. The file
> names are `index.html`, `history.html`, `squad.html`,
> `gallery.html` and `join.html`.

Use the same three columns as the template: **File**, **Page** and
**What it covers**.

<details class="dl-answer"><summary>answer</summary>

```markdown
| File | Page | What it covers |
|---|---|---|
| `index.html` | Home | A welcome, and the next three matches |
| `history.html` | History | The club's history |
| `squad.html` | Squad | A table of the players and their positions |
| `gallery.html` | Gallery | Photos from matches |
| `join.html` | Join | A form for joining the club |
```

Each row names a file, gives the page the name a visitor sees in the
menu, and says in a few words what is on it. The student renamed three
of the starter's files, so the table uses the new names. The navigation
on every page must use them too.

</details>

## In your own site

**4.** Put your live address at the top of your README, and check what
a stranger sees.

1. In your fork of `project_wad`, open `readme.md` (or `README.md`, if
   you have already renamed it).
2. Find the line that starts `**Live site:**`. Replace the text in
   square brackets with your own GitHub Pages address.
3. Open that address in a new tab. Does your home page load?
4. Commit the change, with a message such as "Add the live site
   address to the README".
5. Open your repository's front page on GitHub, and read the README
   there.

Could a stranger open your site from the README in one click?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Your GitHub Pages address is shown in your repository's
   **Settings**, under **Pages**.
2. It usually looks like `https://your-username.github.io/your-repository/`.
3. Your fork starts with two READMEs: the starter's own `README.md`,
   and your `readme.md`. The tutorial's last steps say how to make
   yours the one GitHub shows on the front page.

**Think about:** why does the address go near the top, not at the end?

**Try this next:** ask someone who has not seen your site to read only
the README. What do they think the site is about?

</details>

<details class="dl-answer"><summary>answer</summary>

The line should look something like this, with your own address:

```markdown
**Live site:** https://your-username.github.io/your-repository/
```

GitHub turns an address written like this into a link, so a reader can
click it. If the front page of your repository still shows the
starter's own README, the rename in the tutorial's last steps has not
happened yet. If the link opens a "404" page, check the address against
the one under **Settings**, then **Pages**.

</details>
