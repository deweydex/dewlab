---
title: "Code other people can read: reviewing your toolkit"
year: "2026-2027"
version: 2026.09.24.1
covers:
  reading-code-as-a-stranger:
    covers: [PDP-LO11]
    touches: [PDP-LO8]
  a-checklist-for-a-review:
    covers: [PDP-LO11]
    touches: [PDP-LO10]
  changing-the-code-keeping-the-promise:
    covers: [PDP-LO7]
    touches: [PDP-LO10]
  a-docstring-is-a-promise:
    covers: [PDP-LO7]
    touches: [PDP-LO10]
  rules-a-team-agrees-on:
    covers: [PDP-LO11]
  your-toolkit-read-by-a-stranger:
    covers: [PDP-LO7, PDP-LO11]
---

# Code other people can read: reviewing your toolkit

Next week your team starts its project, and it will share one toolkit.
Someone who has never seen your code opens it and finds `halvings(n)`.
Can they tell what it does, what it needs, and what it gives back,
without asking you? The stranger who reads your code most often is you,
six months from now, and you will have forgotten too.

On this page we:

- read a badly written function the way a stranger would
- review it with a checklist built from the four questions
- rewrite it without changing what it does, with tests keeping watch
- write docstrings a stranger can rely on, and let one check itself
- meet the rules a team agrees on, and a small tool that checks some
  of them
- read your own toolkit as a stranger would

> **The space we're in.** Python runs any code that is valid, however
> it is written. Names, comments, layout and docstrings are for people,
> and Python ignores them. So nothing on this page changes what a
> program does. One thing usually goes unsaid: code is read many more
> times than it is written. Your whole toolkit is loaded, from
> `split_bill` to `angle_between` and beyond.

## Warm-up

The first question is from
[Sorting a hand of cards](tutorial:sorting-a-hand-of-cards#a-new-list-and-the-old-one-left-alone),
and the second from
[What a function can see](tutorial:what-a-function-can-see#what-does-a-function-need).

```question
id: code-other-warm-up-1
type: multiple-choice
correct: 3

After `hand = [7, 2, 9]` and `answer = hand.sort()`, what is `answer`?

- `[2, 7, 9]`
- `[7, 2, 9]`
- `None`
```

```question
id: code-other-warm-up-2
type: fill-in-the-blank

Everything a function needs should come in through its
{parameters|comments|return line}, and everything it gives should come
out through `return`.
```

## Reading code as a stranger

Here is a function a classmate wrote on
[What is typical?](tutorial:what-is-typical), before they tidied it.
The numbers are monthly rents in euro for five flats on one street, in
the order of the houses. The rents are made up. Before you run it, read
only the function. What is it for? And what will `rents` look like
after the call?

```python exec
id: code-other-stranger-1
def m(l, p=False):
    l.sort()    # sort the list
    if len(l)%2==1:
        r=l[len(l)//2]
    else:
        r=(l[len(l)//2-1]+l[len(l)//2])/2
    if p==True:
        print("median is",r)
    return r

rents = [1450, 2100, 1300, 1875, 1600]
print(m(rents))
print(rents)
```

It finds the median, €1,600, and it is right. But look at the second
line of output. The rents are now in order from smallest to largest,
and the order of the houses is gone. The line `l.sort()` sorted the
caller's own list, as `hand.sort()` did in the warm-up.

A change a function makes outside itself, beyond the value it gives
back, is called a *side effect*. Printing is a side effect too. Some
side effects are the whole point of a function, like `plot_rule`
drawing. This one is a surprise, and a surprise side effect is one of
the most expensive bugs there is, because it shows up somewhere else,
later.

It took us a whole paragraph to find out what five short lines do.
Nothing in the function helped: not its name, not the names inside it,
and not its one comment.

## A checklist for a review

A *code review* is one person reading another person's code, to find
problems before they reach anyone who uses it. The person who reads is
the *reviewer*. Reviewers use a checklist, so that nothing depends on
what they happen to notice that day.

Here is one, built from the four questions. Each question asks about
the code, never about the person who wrote it.

| The question | What a reviewer asks |
|---|---|
| What is named here? | Does each name say what it holds? Is any number left without a name? |
| What is promised? | Does the docstring say what goes in and what comes out? Do tests check that promise, edges included? |
| What happens when? | Can you follow the steps in order? Is any step written twice, or never used? |
| What does this space let us do? | Does the function use a name from outside, a [hidden input](tutorial:what-a-function-can-see#what-a-function-can-see-from-outside)? Does it change anything it was handed, or print when it should give back? |

Here is a review of `m`, written the way a reviewer writes one: what
they saw, why it matters, and what they suggest.

1. **Names.** `m`, `l`, `p` and `r` say nothing. `l` also looks like
   the number 1 in many fonts. Suggest `middle_value`, `values`,
   `show` and `result`.
2. **Promise.** There is no docstring, so a reader cannot tell what
   happens with an even number of values, or with an empty list.
3. **Sequence.** `len(l)//2` is worked out three times. Give it a name
   once.
4. **Space.** `l.sort()` changes the list it was handed. Use `sorted()`,
   which gives back a new list.
5. **Space.** With `p=True` the function also prints. It is doing two
   jobs. The caller can print the result.
6. **Comment.** `# sort the list` says what the line already says.

One more finding is the most useful of all, and the checklist does not
ask for it. This function already exists in your toolkit, as `median`.
A reviewer who knows the rest of the code can say "we have this
already", and save a whole rewrite.

```question
id: code-other-checklist-1
type: multiple-choice
correct: 2

Which review comment is the most useful?

- "This function is badly written."
- "`total` is changed inside the loop and again after it. Could the second change go?"
- "I would have done this differently."
```

## Changing the code, keeping the promise

Changing how code is written, without changing what it does, is called
*refactoring*. The danger is plain: a small change can break something
that worked. So a refactor starts with tests, written before any code
is touched.

The cell below builds a test for any median function. It compares the
function with your toolkit's `median` on four lists. Then it checks that
the list handed in comes back unchanged. Run it on `m`. It is meant to
stop with an `AssertionError`. Which test do you expect to fail?

```python exec
id: code-other-refactor-1
def check_median_tool(tool):
    """Test a median function against the toolkit's median, and check it leaves its list alone."""
    for values in [[3, 1, 2], [4, 1, 3, 2], [7], [1450, 2100, 1300, 1875, 1600]]:
        assert tool(list(values)) == median(values), values
    rents_before = [1450, 2100, 1300, 1875, 1600]
    rents_handed_in = list(rents_before)
    tool(rents_handed_in)
    assert rents_handed_in == rents_before, "the list handed in was changed"
    print(tool.__name__, "passes every test.")

check_median_tool(m)
```

Every answer matches, and the last test fails with its message: the
list handed in was changed. The tests now pin down what the function
does, the good and the bad.

Here is the rewrite, with each finding from the review dealt with.
Before you run it, which test do you expect it to fail, if any?

```python exec
id: code-other-refactor-2
def middle_value(values):
    """Return the median of values, a list of at least one number.

    With an even count, return the mean of the two middle values.
    The list handed in is not changed.
    """
    in_order = sorted(values)
    middle = len(in_order) // 2
    if len(in_order) % 2 == 1:
        return in_order[middle]
    return (in_order[middle - 1] + in_order[middle]) / 2

check_median_tool(middle_value)
rents = [1450, 2100, 1300, 1875, 1600]
print("The median rent is", middle_value(rents))
print(rents)
```

It passes every test, and the rents stay in the order of the houses.
The printing moved out of the function, to the line that wants it.
Compare `middle_value` with the `median` you wrote on
[What is typical?](tutorial:what-is-typical#the-middle-one-in-the-line-the-median).
Line for line, they are very close: the review led back to your own
tool.

In a real refactor, the changes go in one at a time, with the tests run
after each one. If a test fails, you know which change broke it.

### Your turn

1. Change `middle_value` so that it uses `values.sort()` again, and run
   the cell. Which test notices?
2. Put `sorted()` back. Then add one more list to the tests in
   `check_median_tool`: a list of two rents. Run both cells again.

## A docstring is a promise

On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
a docstring was the promise a function makes, written at its top. For a
stranger, a good docstring says four things:

1. **What comes out**, in one short first line.
2. **What must go in**: what kind of value each input is, its unit,
   and which values are allowed.
3. **What happens at the edges**, and anything the function changes or
   does not change.
4. **An example**, where one helps.

Python's own guide to docstrings, PEP 257, asks for that shape: one
summary line, a blank line, then the details. `help()` shows a
function's docstring, and it is the first thing a stranger reads. What
do you expect to see?

```python exec
id: code-other-docstring-1
help(split_bill)
```

`help()` shows the function's name and inputs, then its docstring. If
your own `split_bill` has a docstring, that is what appears.

An example in a docstring can do more than explain. Python's `doctest`
module finds each line that starts with `>>>` in a docstring, runs it,
and compares the result with the line under it. So the documentation
checks itself. Here is a running pace, in minutes for each kilometre.
Someone changed the function, and one example is now out of date. The
cell is meant to report one failed example. Which one?

```python exec
id: code-other-docstring-2
import doctest

def pace(minutes, kilometres):
    """Return a running pace, in minutes for each kilometre.

    minutes and kilometres are numbers above 0.

    >>> pace(25, 5)
    5.0
    >>> pace(52.5, 10)
    5.2
    """
    return minutes / kilometres

doctest.run_docstring_examples(pace, globals(), name="pace")
```

The report says it expected `5.2` and got `5.25`. The function is right,
and the docstring is wrong. On
[Does it work?](tutorial:does-it-work#names-and-comments-a-stranger-can-read)
we said that a comment which no longer matches the code is worse than
none. A docstring example that runs cannot drift for long.

### Your turn

1. Fix the second example in `pace`, and run the cell again. What does
   `doctest` show when every example passes?
2. Add a third example: a 5 km parkrun in 30 minutes.

## Rules a team agrees on

[Does it work?](tutorial:does-it-work#names-and-comments-a-stranger-can-read)
met PEP 8, Python's coding standard, for names, comments and
indentation. A team usually agrees a few more rules. Here are the ones
that matter most in a toolkit.

- **Give a number a name.** A *magic number* is a number in code with
  no name to say what it means. In `price * 1.23`, a stranger has to
  guess that 1.23 adds VAT at 23%. A *named constant* is a name for a
  value that never changes while the program runs. PEP 8 writes it in
  capitals, at the top of the file: `VAT_RATE = 0.23`.
- **Spaces make the parts visible.** One space on each side of `=`,
  `==` and `+`, and after each comma. Compare `r=(l[n-1]+l[n])/2` with
  `result = (values[n - 1] + values[n]) / 2`.
- **Names for True and False read as questions.** `is_sorted`,
  `has_tickets`. Write `if is_sorted:`, never `if is_sorted == True:`.
- **Short lines.** PEP 8 asks for lines under 80 characters, so code
  fits beside a second window, or on a phone.
- **Two blank lines between functions**, so each one stands apart.

Above every rule, PEP 8 puts one more: code in one project should look
the same. A team that follows its own agreed rules has done better than
a team where each person follows their own good ones.

Some of these rules can be checked by a tool. A *linter* is a program
that reads code without running it, and reports lines that break a
coding standard. Real ones for Python are called flake8, pylint and
Ruff. Here is a very small one of our own. It looks at a function's
docstring, its names, and whether it uses `print`.

```python exec
id: code-other-rules-1
def quick_review(function):
    """Return a list of notes on function, the way a small linter would."""
    notes = []
    if not function.__doc__:
        notes.append("no docstring")
    code = function.__code__
    for name in code.co_varnames:    # every input and every name made inside
        if len(name) < 3:
            notes.append("short name " + name)
    if "print" in code.co_names:
        notes.append("uses print")
    return notes

print(quick_review(m))
print(quick_review(middle_value))
```

`__doc__` is the docstring, and `__code__` is what Python made from the
function's lines. Its `co_varnames` are the inputs and the names made
inside. For `m`, the tool makes five notes. For `middle_value`, it
makes none.

## Your toolkit, read by a stranger

Now let's point the tool at your own toolkit, one or two tools from
each unit. Before you run it, which of your tools do you expect to get
a note?

```python exec
id: code-other-toolkit-1
tools = [split_bill, to_binary, between, truth_table, total, simulate,
         compose, close_enough, mean, frequency_table, binary_search,
         halvings, solve_quadratic, vertex, slope, distance, angle_between]

for tool in tools:
    notes = quick_review(tool)
    if notes:
        print(tool.__name__, notes)
print(len(tools), "tools read.")
```

The tool flags `n` in `to_binary` and `halvings`, and `a`, `b` and
`c` in `solve_quadratic` and `vertex`. It flags `p`, `q`, `x1` and
`y1` in `slope` and `distance`, and it flags `truth_table` for using
`print`. Are those real problems?

Mostly not. `a`, `b` and `c` match the quadratic formula written above
the code. `p` and `q` are what
[Straight lines](tutorial:straight-lines) called two points, and `x1`
and `y1` are the first point's coordinates, as in the formula. Each
docstring says so. `truth_table` promises to print a table: printing
is its job. A linter finds places worth a second look. A person decides
what they mean. That is why a team uses both.

A note the tool cannot give is whether a docstring is true. For that,
you need a reader, and tests.

### Your turn

This review is yours. Swap toolkits with a partner if you can. If not,
open two of your earlier pages and read your own toolkit cells as a
stranger would.

1. Pick three toolkit functions. Go through the checklist for each,
   question by question.
2. Write your findings as review comments: what you saw, why it
   matters, and what you suggest. Three comments are enough.
3. Improve one docstring so that it says all four things: what comes
   out, what must go in, the edges, and an example.
4. Run that page's tests again. A docstring change should never make a
   test fail. If one fails, what changed?

<details class="dl-why"><summary>Why this way?</summary>

This page taught reviewing with a function written badly on purpose,
and then a checklist. Many courses teach style as a list of rules
first, and ask students to follow them from the start.

A list of rules first is quicker, and in a job it is how a team's
standard arrives: written down, before you write a line.

We started from a bad function because a rule only makes sense to
someone who has felt the problem it solves. Reading `m` cost you a
paragraph, and the side effect cost the street its order. The cost of
our way is that PEP 8 appeared in pieces, across two pages, and it
has many more rules than you have met.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | names that say what they hold; a named constant in capitals in place of a magic number |
| What is promised? | a docstring says what comes out, what goes in, and the edges; `doctest` runs its examples; tests pin down a promise before a refactor |
| What happens when? | tests first, then one change at a time, with the tests run after each; review before the code reaches anyone else |
| What does this space let us do? | Python ignores names and layout, so they are for people; `.sort()` changes the list it was handed, and `sorted()` does not |

## What we have now

| Term or tool | What it means |
|---|---|
| side effect | a change a function makes outside itself, beyond the value it gives back |
| code review, reviewer | reading someone's code to find problems before anyone uses it; the person who reads |
| a review checklist | the four questions, asked of every function |
| refactoring | changing how code is written without changing what it does |
| a good docstring | what comes out, what must go in, the edges, and an example |
| `help(function)` | shows a function's name, inputs and docstring |
| `doctest` | runs the `>>>` examples in a docstring and reports any that fail |
| magic number, named constant | a number with no name; a name in capitals for a value that never changes |
| linter | a program that reads code without running it and reports breaks of a standard |

The practice page is next. Then
[The team project](tutorial:building-it-together) puts this review to
work, with your team's code.

## Where to read more

The dewlab page
[Reviewing code and reflecting on your work](tutorial:critique-and-reflection)
has questions for reading a partner's code, and your own, in writing.

PEP 8 is at [peps.python.org/pep-0008](https://peps.python.org/pep-0008/),
and PEP 257, on docstrings, at
[peps.python.org/pep-0257](https://peps.python.org/pep-0257/).

Google's guide
[How to do a code review](https://google.github.io/eng-practices/review/reviewer/)
is what reviewers at one large company are asked to look for, and how
to say it kindly.
