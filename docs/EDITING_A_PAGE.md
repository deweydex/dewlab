# Editing a page

This page is for a teacher or course author who sees something to fix on a
dewlab page: a typo, a sentence that is hard to follow, a heading that is
wrong. You can change it on the page itself. You do not need to know Git, and
you do not need to install anything.

Your change does not go live straight away. It goes to the course owner as a
proposal, which GitHub calls a **pull request**. Someone reads it and approves
it, and then the page changes for everyone.

## What you need

- A GitHub account, and an invitation to work on this repository. If you were
  not invited, ask the course owner.
- A computer or a wide tablet. The editor says so if the screen is too narrow.
- A **token**: a long password that lets this page propose changes to this one
  repository, and nothing else. It cannot publish a change. You make it once.

## Make a token

1. Sign in to GitHub. Open **Settings**, then **Developer settings**, then
   **Personal access tokens**, then **Fine-grained tokens**, then **Generate new
   token**.
2. Give it a name you will recognise, such as "dewlab editing". Choose how long
   it lasts. A few months is sensible.
3. Under **Repository access**, choose **Only select repositories** and pick
   `deweydex/dewlab`.
4. Under **Repository permissions**, set **Contents** to **Read and write** and
   **Pull requests** to **Read and write**. Leave everything else alone.
5. Press **Generate token** and copy it. GitHub shows it once.

If `deweydex/dewlab` is not in GitHub's list, you have not been given access
yet. Tell the course owner.

## Edit a page

1. Open the page you want to change. Open **Settings** (the tab at the edge of
   the page) and scroll to the bottom. Press **Edit this page**. Or add `#edit` to
   the end of the page's address and press Enter.
2. The first time, paste your token when the page asks. It is kept in this
   browser only. Press **Forget my token** in the same place to remove it,
   which is a good idea on a computer other people use.
3. Click a heading or a paragraph and type. The page looks the same while you
   edit; a thin line shows which block you are in. Click somewhere else to
   finish that block.
4. When you have finished, open **Settings** and press **Open pull request**.
   The page tells you where your proposal is on GitHub.
5. Keep editing if you like. Pressing **Open pull request** again adds your new
   changes to the same proposal.

**Discard my changes** puts the page back as it was. **Stop editing** leaves
edit mode. If you have changes you have not saved, it asks first, and stopping
then discards them.

## What you can change

| On the page | What happens when you click it |
|---|---|
| A heading, or a paragraph of plain text | You edit it in place |
| A paragraph with maths, a link written as HTML, an image, a list, a quote, a table, or a fold (a hint or an answer) | A box opens with that block's markdown, the plain-text form the file is written in. Change the words and leave the symbols around them alone |
| Code cells, questions, live site editors, and text shared between pages | Locked for now. The pointer shows it. They are edited in the file on GitHub |

More of these will become editable. If you want to change something that is
locked, open the page's file on GitHub. The page's address names it: the page whose
address ends in tutorials/an-editor.html comes from the file
`tutorials/an-editor/an-editor.md`.

## What happens next

- The change is a **draft** pull request. Nothing on the live site moves.
- The course owner reads it. They may ask a question, change something, or
  approve it. When it is approved and merged, the site rebuilds and the page
  changes.
- If the page was changed on GitHub while you were editing, saving stops and
  says so. Reload the page and make your change again.

## If something goes wrong

- **"Could not read this page's source from GitHub."** The token is wrong, has
  run out, or was not given access to this repository. Press **Forget my
  token**, make a new one, and try again.
- **"Editing needs a larger screen."** Open the page on a computer.
- **A block you want to edit does not respond.** It is locked (see the table).
- **You are not sure about a change.** Press **Discard my changes**. Nothing
  has been sent until you press **Open pull request**.
