---
title: "Your development environment: the tools around your code"
year: "2026-2027"
version: 2026.09.05.1
covers:
  an-environment-you-are-already-in:
    covers: [FOOP-LO5]
  errors-worth-reading:
    covers: [FOOP-LO5]
  what-the-editor-already-knows:
    covers: [FOOP-LO5]
  where-a-bigger-project-lives:
    covers: [FOOP-LO5]
---

# Your development environment: the tools around your code

Writing a class is one skill. Running it, and finding out why it broke,
is another. The second skill depends on the tools around your code, not
on the code itself.

A *development environment* is the set of tools around your code: an
editor to write it in, a way to run it and see what happened, and help
with finding out why it broke. On this page we look at what a
development environment gives you. dewlab's own pages are a small one.
dewmini is a larger one, for a real project.

## An environment you are already in

Every cell you have run so far, in every tutorial, sits inside a
development environment. The page lets you edit your code, run it, and
see what happened, all in one place. It is small on purpose: one script,
one job.

`compose/dewmini.html` has the same editor and the same Python. It adds
several cells, several files, and work that is still there when you come
back. Because the tool underneath is the same, what you learn about this
page is also true of dewmini.

## Errors worth reading

The cell below has a mistake in it. Run it, and read the error message
slowly. Can you find the word that is wrong before you look at the code
again?

```python exec
id: errors-worth-reading-1
class Basket:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        self.items.appendd((name, price))


basket = Basket()
basket.add("bread", 2.50)
print(basket.items)
```

The message names the line and the mistake. It says that a `'list'
object has no attribute 'appendd'`. `self.items` is a list, and lists
have no method called `appendd`. Python then adds a suggestion:
`Did you mean: 'append'?`

Getting you to that sentence as fast as possible is the main job of a
development environment at this moment. On this page, the error is
trimmed down to the lines of your own code. It does not show everything
Python did inside itself to reach that line.

Now change `appendd` back to `append`, and run the cell again. The class
was never the problem, and neither was the empty list. One misspelled
word was the problem, and the error message pointed straight at it.

## What the editor already knows

Let's try two things the editor can do.

1. Click at the end of the comment in the cell below, and press Enter.
2. Start typing `bas`. What appears before you finish the word?
3. Press Tab, or click `basket` in the list, to finish the word.
4. Now rest the mouse pointer over a name that is already on the page,
   such as `Basket` in the cell above. What does the editor show you?

```python exec
id: what-the-editor-already-knows-1
# type here
```

A short list of names appears as you type, with `basket` among them.
This is called *autocomplete*: the editor offers to finish a name for
you. When you rest the pointer over `Basket`, the editor shows its
docstring or its shape, so you do not have to scroll back to find it.
(A docstring is a short description written at the top of a class or
function.)

Neither of those needed you to look anything up. The editor already
knew, because it reads the same code you do. That is what an
*integrated development environment* adds to a plain text file. It pays
attention to what you are writing, and it helps.

## Where a bigger project lives

A page like this one holds one script, and it does not remember your
work between visits. A real project grows past that. It has several
files, with a class in one file used from another, and work you want to
find again next week. dewmini is made for that.

Three parts of dewmini do that work.

- **Files** is a real set of files and folders. Write `shapes.py` there,
  and a cell elsewhere can `import shapes`. Real Python programs are
  spread across several files in the same way.
- **Variables**, in the Workbench, lists every name in your current
  session, with its type and a short summary of its value. It updates
  each time you run a cell. It answers the question "did that work?"
  without you having to print everything a second time.
- **Stop** is a button next to each cell. A runaway cell is one stuck
  in a loop that never ends. Press **Stop**, and the cell stops right
  away. You do not have to wait for it, or close the tab.

None of this is a new set of instructions to learn. It is what an
environment does around the code you already know how to write. It runs
your code, shows you what broke, and keeps track of the names you used.
That leaves your own thinking free for the problem, not the tool.
