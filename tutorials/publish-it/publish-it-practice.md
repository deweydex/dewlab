---
title: "Publishing your site with GitHub Pages — Practice"
practice_for: publish-it
year: "2026-2027"
version: 2026.09.22.1
---

# Publishing your site with GitHub Pages — Practice

On this page we practise reading GitHub Pages addresses, and finding out
why a published page is missing. Every problem uses the same pattern:

```text
username.github.io/repository-name/file-name
```

When no file name comes at the end, GitHub Pages sends `index.html`.

There are three kinds of problem:

- addresses to work out, and to read
- sites that give a "404: page not found" error, where we find the
  mistake
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

## Work out the address

**1.** What is the address of each page? Write each one without
`https://` at the start.

| Username | Repository | Page |
|---|---|---|
| `janedoe` | `web` | the home page |
| `janedoe` | `web` | `about.html` |
| `sean-k` | `portfolio_wad` | the home page |
| `MaryOB` | `my-site` | `contact.html` |

<details class="dl-answer"><summary>answer</summary>

| Username | Repository | Page | Address |
|---|---|---|---|
| `janedoe` | `web` | the home page | `janedoe.github.io/web/` |
| `janedoe` | `web` | `about.html` | `janedoe.github.io/web/about.html` |
| `sean-k` | `portfolio_wad` | the home page | `sean-k.github.io/portfolio_wad/` |
| `MaryOB` | `my-site` | `contact.html` | `maryob.github.io/my-site/contact.html` |

The home page needs no file name, because GitHub Pages sends
`index.html` when none is given. `janedoe.github.io/web/index.html`
shows the same page.

For Mary, capital letters make no difference in the first part of an
address, before the first `/`. So `MaryOB.github.io` and
`maryob.github.io` lead to the same site. After the first `/`, they do
make a difference, as problem 3 shows.

</details>

**2.** A classmate sends you this link:

```text
https://aoife-m.github.io/plushies/shop.html
```

What is your classmate's GitHub username? What is the repository
called? Which file in it are you looking at?

<details class="dl-answer"><summary>answer</summary>

- The username is `aoife-m`, the part before `.github.io`.
- The repository is `plushies`, the part after the first `/`.
- The file is `shop.html`, in the top level of that repository.

So the same repository is on GitHub at
`github.com/aoife-m/plushies`, and `shop.html` is one of its files.

</details>

## Why is this page not found?

**3.** Each of these people gets a GitHub page that says `404` when
they visit their site. `404` means "not found": the address reached
GitHub, but GitHub had nothing to send for it. For each person, what is
wrong? How would they fix it?

1. Kim copied the starter, then went straight to
   `kim-l.github.io/portfolio_wad/`. She has not opened **Settings**
   yet.
2. Liam's repository has two files, `home.html` and `styles.css`, and
   nothing else. GitHub Pages is switched on. His address is
   `liam-o.github.io/cv/`.
3. Sara's home page works. When she clicks **About** in her menu, she
   gets a 404. Her file is called `about.html`. In her menu, the link
   says `About.html`. The link worked when she opened the page on her
   own computer.
4. Tom's repository is called `portfolio_wad`. He typed
   `tom-b.github.io/portfolio-wad/` in his browser.
5. Nora made a new file, `contact.html`, and committed it thirty
   seconds ago. `nora-d.github.io/web/contact.html` gives a 404.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

Check these four things, in order, for each person:

1. Is GitHub Pages switched on for the repository?
2. Does each part of the address match exactly: the username, the
   repository's name, and the file's name?
3. Is there a file with that exact name in the repository? For the home
   page, that file is `index.html`.
4. Has the site had a minute or two to rebuild since the last commit?

**Think about:** which of the four checks can you answer from the story
alone?

**Try this next:** Liam renames `home.html` to `Index.html`, with a
capital `I`. Does his home page work now?

</details>

<details class="dl-answer"><summary>answer</summary>

1. **Kim** has not switched GitHub Pages on, so GitHub has no site at
   her address yet. She should open **Settings**, then **Pages**, choose
   the `main` branch and `/ (root)`, and press **Save**. Then wait a
   minute or two.
2. **Liam** has no `index.html`. GitHub Pages looks for that exact name
   for the home page, and finds nothing. He should rename `home.html`
   to `index.html`. If any link points to `home.html`, he changes it
   too. For the question in the hint: `Index.html` does not work. The
   name has to be exactly `index.html`, with a small `i`.
3. **Sara's** link says `About.html`, and her file is `about.html`.
   After the first `/`, GitHub Pages treats a capital letter and a
   small letter as different, so there is no file called `About.html`.
   On her own computer the link worked, because Windows and macOS
   usually ignore the difference. She should change the link to
   `about.html`, exactly as the file is named.
4. **Tom** typed a hyphen, `-`, where his repository's name has an
   underscore, `_`. He should type `tom-b.github.io/portfolio_wad/`.
5. **Nora** has done nothing wrong. Her site is still rebuilding. She
   should wait a minute or two, then refresh.

</details>

## In your own site

**4.** Let's find your own address, try it with and without a capital
letter, and put it where people can find it.

1. In your repository on GitHub, open **Settings**, then **Pages**.
   Copy the address of your site.
2. Open the address in your browser. Which page do you see?
3. Add `about.html` to the end of the address, and open it. Then try
   `About.html`, with a capital `A`. What happens each time?
4. Open `README.md` in your editor. This is the file GitHub shows under
   the list of files on your repository's front page.
5. Add a new line at the very top of it:
   `My site: ` followed by your full address, starting with `https://`.
   Save the file.
6. Commit the change, with a message such as "Add my site's address to
   the README". If you work on your own computer, push it too.

Open your repository's front page on GitHub, and look under the list of
files. Can you click your address there?

<details class="dl-answer"><summary>answer</summary>

In step 2 you see your home page: GitHub Pages sends your `index.html`,
because the address names no file.

In step 3, `about.html` opens your About page. `About.html` gives a
GitHub 404 page. There is no file with that name: only one with a small
`a`.

After step 6, the address appears at the top of the README on your
repository's front page. GitHub turns a full address that starts with
`https://` into a link by itself. Now anyone who finds your repository
can find your site too.

</details>
