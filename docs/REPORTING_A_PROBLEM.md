# Reporting a mistake or a bug

If an explanation is unclear or something does not work, you can tell us.
You do not need to be certain there is a mistake. The page name and what
you noticed are useful places to begin.

You can also ask your teacher to look with you. Reporting through GitHub
needs a free account. Email is another option:
[deweydex@jsaaron.com](mailto:deweydex@jsaaron.com).

## From the page itself

Most pages have a link at the bottom labelled "Something wrong on this
page? Tell us." It offers these options:

- **I have a question** opens a GitHub discussion when that option is
  available. It gives you a place to ask for an explanation.
- **It gives an error** opens a GitHub report form. This can help with a
  cell that will not run or a button that does not work.
- **The page is wrong, or I could not follow it** opens a form for a
  mistake or an explanation that is hard to understand.

The report forms include the page and version. You can add what happened.
If the report link is unavailable, the
[GitHub issue list](https://github.com/deweydex/dewlab/issues) lets you
open a report directly. An *issue* is a message about a question, problem,
or proposed change.

If someone has reported the same problem, you can add what you noticed
to their report. You can also start a new report if you are unsure.

## From a tutorial cell

Some tutorial cells have a small report control in their top bar. It
opens reporting options for that cell. The issue links include the current
code, last visible result, and browser information.

Opening one of those links sends these details to GitHub as part of the
web address. You can check and edit the form before submitting it.
Submitting publishes the report in the project's GitHub issues.

A long piece of code or result may be shortened. You can add the missing
part if it helps explain the problem. Cells you add yourself do not have
this report control; the page's report link is another option.

## Details that can help

For a mistake in an explanation, the page name and the sentence may be
enough. For something that does not work, these details can help:

1. **The page address.** This identifies the tutorial.
2. **What you tried.** For example, "I used Run on the second cell."
3. **What you expected to happen.**
4. **What happened instead.** An error message or screenshot can help.
5. **Your browser and device.** For example, Chrome on a school computer.

You can include what you know. It is fine to ask for help without all
five details. If the problem happens only sometimes, that is useful
information too.

## Before you report a page that will not run

These are options to try if they help. You can report a problem without
completing them first.

**Python may still be loading.** The first run needs an internet
connection to load Python, including in a downloaded tutorial. A slow
connection can take more time. The page's status message may explain
what is loading.

**An earlier cell may be needed.** Cells share values in the order you
run them. Running an earlier example may create a value a later cell
needs. After reopening the page, saved results can be visible even though
Python has not run that code in the new session.

**You can compare with the original code.** A tutorial cell's **reset**
button restores that code and clears its result. This replaces your
edits in the cell. Keeping a copy first lets you return to them. Reset
does not restart Python or clear the values it already holds.

If an example works after reset, comparing the two versions may help us
understand the difference. This does not prove where the problem began.
Questions about your own edits are welcome too.

[Using dewlab](FOR_STUDENTS.md#resetting-code-or-restarting-python)
explains reset, Restart Python, and the saving controls.

## Suggestions and questions

Ideas are welcome alongside problem reports. You might want another
example, more practice, or a tutorial on a new topic. You can describe
what would help you learn.

## If you want to suggest a correction

A *pull request* proposes changes to the project's files for review.
You can send one without opening an issue first. If there is already an
issue, mentioning its number helps connect the discussion and the change.

[Writing a tutorial](WRITING_TUTORIALS.md) explains changes to tutorial
text and code. [Contributing](../CONTRIBUTING.md) and
[Architecture](../ARCHITECTURE.md) explain changes to the site's own code.
