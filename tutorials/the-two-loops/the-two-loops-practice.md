---
title: "Saving and publishing a change — Practice"
practice_for: the-two-loops
year: "2026-2027"
version: 2026.09.22.1
---

# Saving and publishing a change — Practice

On this page we practise one question: which loop is this change in?
Here are the two loops again:

- **On your computer:** change the file, save it, refresh the browser.
- **On GitHub:** commit, push, wait for the site to rebuild, refresh
  the published site. In GitHub's editor, a commit goes straight to
  GitHub, so there is no separate push.

There are three kinds of problem:

- stories about a change that is not showing, where we find which loop
  it is stuck in
- a set of Git commands that went wrong, which we fix
- changes in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. You learn more from a mistake, and
its reason, than from reading the answer.

## Which loop is it in?

**1.** Each of these people changed a heading, and cannot see the new
heading yet. For each one, where is the change now? What should they do
next?

1. Aoife changes the heading in VS Code. On the file's tab in VS Code,
   there is a round dot where the **×** usually is. She refreshes her
   browser, and sees the old heading.
2. Ben changes the heading in VS Code and saves the file. He looks at
   the browser tab where the page is already open. He sees the old
   heading.
3. Chloe changes the heading, saves, and refreshes the file in her
   browser. She sees her new heading. Then she opens her
   `github.io` address, and sees the old heading there.
4. Dan works in GitHub's editor. He changes the heading, presses
   **Commit changes**, and confirms. Straight away, he opens his
   published site. He sees the old heading.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each person, list the steps they did: change, save, refresh,
   commit, push.
2. Which step comes next, after the last one they did?
3. Which browser tab are they looking at: the file on their own
   computer, or the published site?

**Think about:** which loop does each browser tab belong to?

**Try this next:** Chloe commits her change in VS Code, but her
published site still shows the old heading ten minutes later. What
might she have missed?

</details>

<details class="dl-answer"><summary>answer</summary>

| Who | Where the change is | What to do next |
|---|---|---|
| Aoife | In the editor, not saved. VS Code shows a dot on the tab of a file with unsaved changes. | Save the file, then refresh. |
| Ben | Saved on his computer. The browser still shows the file as it read it before. | Refresh the tab. A refresh makes the browser read the saved file again. |
| Chloe | Saved on her computer, and seen there. It has not been committed or pushed. | Commit and push, wait a minute or two, then refresh her published site. |
| Dan | Committed on GitHub. The site has not finished rebuilding. | Wait a minute or two, then refresh. |

Chloe's story is the most common one. Her change is real, and it has
finished the first loop. She is looking for it at the end of the second
loop, which it has not started yet.

For the question in the hint: ten minutes is long enough for a rebuild.
So Chloe most likely made a commit on her computer and did not push it.
The commit is on her computer, and GitHub has never seen it.

</details>

**2.** Here are the steps for one change, made on your own computer and
published through GitHub. They are in the wrong order. Put them in the
right order.

- `git push`
- refresh the published site
- save the file
- `git commit -m "Change the main heading"`
- wait a minute or two
- `git add index.html`
- change the heading in `index.html`

<details class="dl-answer"><summary>answer</summary>

1. change the heading in `index.html`
2. save the file
3. `git add index.html`
4. `git commit -m "Change the main heading"`
5. `git push`
6. wait a minute or two
7. refresh the published site

Steps 1 and 2 are the first loop. You could refresh the file in your
browser between step 2 and step 3, to check the change before you
commit it. Steps 3 to 7 are the second loop.

</details>

## Fix the commands

**3.** Sam typed these three commands in a terminal, in this order,
after changing and saving `index.html`:

```text
git commit -m "Change the main heading"
git add index.html
git push
```

None of them gave a red error. The first one printed a message ending in
`no changes added to commit`. The last one printed
`Everything up-to-date`. Sam's published site never changed. Why not?
What should Sam type now?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What does `git add` do? What does `git commit` record?
2. When Sam ran `git commit`, had any file been chosen for the commit
   yet?
3. So was a commit made? And if there is no new commit, what can
   `git push` send?

**Think about:** the order of the three actions. Why does `add` have to
come first?

**Try this next:** what would happen if Sam typed `git add index.html`
and `git commit -m "..."`, and then closed the terminal?

</details>

<details class="dl-answer"><summary>answer</summary>

`git commit` records only the changes that `git add` has chosen. When
Sam ran it, nothing had been chosen yet, so Git made no commit. `no
changes added to commit` means this. Then `git add` chose the file,
but nothing recorded it. So `git push` had no new commit to send, and it
said `Everything up-to-date`. GitHub already had every commit Sam had
made.

The change is saved, and chosen for the next commit, but it is still
only on Sam's computer. Sam should now type:

```text
git commit -m "Change the main heading"
git push
```

Then wait a minute or two, and refresh the published site.

For the question in the hint: the commit would be made, but only on
Sam's computer. Without `git push`, it never reaches GitHub, and the
published site stays the same.

</details>

## In your own site

**4.** Let's follow one change through both loops, and time the second
one. The starter's own Exercise 3 asks you to change the page's title,
so we use that.

1. Open `index.html` in your editor. Find the `<title>` line near the
   top, inside `<head>`. In the starter it says `My Portfolio`. If you
   have changed it already, choose a new title anyway.
2. Change the words between `<title>` and `</title>` to your name, or
   the name of your site.
3. If you work on your own computer: save, and refresh the file in your
   browser. Look at the text on the browser tab. Has it changed?
4. Commit the change, with a message such as "Put my name in the page
   title". If you work on your own computer, push it too.
5. Look at a clock. Open your published site, and refresh it every
   thirty seconds or so.

How long did it take before the tab on your published site showed the
new title?

<details class="dl-answer"><summary>answer</summary>

The title is the text on the browser tab, not a heading on the page.
So we look at the tab to check it.

On your own computer, the change shows as soon as you save and refresh.
On your published site, it usually takes a minute or two. If you work
in GitHub's editor, step 3 has nothing to do. Your commit in step 4
saves the file.

You can watch the rebuild happen. In your repository on GitHub, open
the **Actions** tab. Each rebuild of your site is listed there, with a
name like "pages build and deployment". A green tick means the new
version of your site is ready.

</details>

**5.** Now let's make a change that is not showing on purpose, and then
find it in your repository's history.

1. Open `index.html` in your editor, and find the `<footer>` near the
   bottom. It has the line `<p>&copy; 2025 My Portfolio. All rights reserved.</p>`.
2. Change `2025` to this year, and `My Portfolio` to your name. Save
   the file, but do not commit it yet.
3. Open your published site. Before you look at its footer, decide:
   will it show your change? Which loop is the change in?
4. Now commit the change, with a message such as "Update the footer".
   Push it if you work on your own computer. Wait, and refresh your
   published site.
5. On GitHub, open your repository's front page. Above the list of
   files, find the link that counts your commits, and click it. Can you
   find your commit, with your message? Click it. What do the red and
   green lines show?

<details class="dl-answer"><summary>answer</summary>

In step 3, the published site still shows the old footer. The change
is saved on your computer, so it has finished the first loop only. If
you use GitHub's editor, there is no save without a commit, so for you
step 2 and step 4 happen together.

In step 5, the list of commits shows the newest first, each with its
message. Your "Update the footer" commit is at the top. Further down
are older commits: the starter's own, if you pressed **Fork**, or one
first commit, if you pressed **Use this template**. Click it to see
exactly what changed: the old line in red, marked `-`, and the new line
in green,
marked `+`. This is the same view of changed lines that a pull request
shows, from [Issues and pull requests](tutorial:issues-and-pull-requests).

</details>
