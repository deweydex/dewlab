---
title: "The tools for building a website"
year: "2026-2027"
version: 2026.09.11.1
covers:
  from-a-change-to-a-published-page:
    touches: [WA-LO13]
---

# The tools for building a website

Welcome. In this course we build a website and publish it online. Let's
start by meeting the tools we will use, and seeing how they connect. You
do not need to do anything on this page yet: you can read it first, then
try the steps on the pages that follow.

Would you rather begin with data? [A table is a list of
rows](tutorial:a-table-is-a-list-of-rows) has an example you can run.
The data exercises work in your browser, without a GitHub account.

## The tools for a website

We use four tools. Here they are side by side:

| Tool | What it does | Where we find it |
|---|---|---|
| An *editor* | A program for changing text files. We write our code in it. | VS Code, on your own computer, is one option. GitHub also has an editor on its website, so you can work without installing anything. |
| *GitHub* | Keeps a project's files online, and records every change we save, so we can look back at earlier versions. | github.com |
| *GitHub Pages* | Publishes a website from the files on GitHub. Once it is set up, updates to your files appear at your site's web address. | Part of GitHub |
| A *browser* | Shows a web page. It can open a file on your computer, or a website that has been published online. | Chrome, Firefox, Safari, Edge |

GitHub keeps a project's files in a folder called a *repository*, often
shortened to "repo". Who do you think can see the files in a public
repository? Anyone can, which is worth remembering before you put
something there.

This site has explanations and examples. We can try an idea here first,
then use it in a website or a database of our own.

## From a change to a published page

How does a change in a file end up on a website that anyone can visit?
If we use an editor on our own computer, it happens in two stages.

**Stage one: on your computer.**

1. We change a file and save it.
2. We refresh the browser. It loads the saved file again, so we can see
   the result.

**Stage two: on GitHub.**

3. We record the change. Git calls a recorded set of changes a *commit*.
4. We send our commits to GitHub. This is called a *push*.
5. GitHub publishes the update. Now other people can see it on your
   website.

Here is the same path as a picture. The numbers on the arrows match the
steps above.

![A diagram in two bands. The top band, stage one, is on your computer. Your editor has an arrow labelled 1 save to the file, saved on your computer, and the file has an arrow labelled 2 refresh to your browser, where only you see it. From the file, an arrow labelled 3 commit goes down to a commit, recorded by Git. The bottom band, stage two, is on GitHub. From the commit, an arrow labelled 4 push goes down into your repository, and from there an arrow labelled 5 publish goes to your published site. Below that, an arrow goes to anyone's browser, at your site's address. A dashed line runs from your editor straight down into your repository, labelled: GitHub's editor, a commit goes straight here.](path-of-a-change.svg)

What if we use GitHub's editor in the browser instead? Then we save a
commit straight onto GitHub, so stage one and stage two happen together.
[Saving and publishing a change](tutorial:the-two-loops) looks at both ways of working,
with steps to try once your site is ready.

## Reading and trying examples

Let's look at how this site itself works:

- The bar at the top stays in view as you scroll. **dewlab** takes you
  back to the front page. **Settings** lets you change the colours,
  font, text size and line width. Your choices are saved in this
  browser.
- Links near the top and bottom of a page take you to the previous or
  next page in a *series*: a group of tutorials in teaching order. You
  can go back to an earlier page whenever it helps.

Some code boxes are examples to read, like this one:

```sql
SELECT name, price
FROM products
WHERE price < 20;
```

This is SQL, and we explore it in the data tutorials. You do not need
to understand it yet. On those pages, code boxes with a **Run** button
let us change the code and see its result. Some website tutorials have
an editor with a preview instead, and the preview changes as we type.

## Where to go next

- For a website, [Creating a GitHub account](tutorial:a-github-account) is the
  next step.
- For data, we can begin with [a table is a list of
  rows](tutorial:a-table-is-a-list-of-rows).

If something is unclear, come back to this page, or ask your teacher.
It is fine to learn these tools one at a time.
