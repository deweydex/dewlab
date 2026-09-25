---
title: "True, false and every case: truth tables"
year: "2026-2027"
version: 2026.09.25.1
covers:
  true-and-false-are-values:
    touches: [MIT-2.4]
  and-both-must-be-true:
    covers: [MIT-2.4]
    touches: [PDP-LO6]
  or-at-least-one-is-true:
    covers: [MIT-2.4]
  not-the-opposite:
    covers: [MIT-2.4]
  exclusive-or-exactly-one:
    covers: [MIT-2.4]
  how-many-rows:
    covers: [MIT-2.4]
    touches: [MIT-1.4, MIT-1.1]
  a-tool-for-any-rule:
    touches: [MIT-2.4, PDP-LO6]
  brackets-change-the-rule:
    touches: [MIT-2.4]
---

# True, false and every case: truth tables

A bike-share app unlocks a bike only when your account is paid up and
the dock is working. Before the app goes live, somebody has to be sure
it does the right thing in every situation. "Every situation" sounds
endless, and a little frightening: how could anyone test them all?

Here is the surprise of this page. For a rule like this one, "every
situation" is a short list, and Python can write all of it.

On this page we:

- meet `True` and `False` as values with their own rules
- combine them with `and`, `or`, `not`, and "one or the other, not both"
- list every case of a rule in a truth table, with a loop
- count the rows, and find binary counting hiding inside them
- add `truth_table` to the toolkit, and use it on a digit display

> **The space we're in.** Every value on this page is True or False.
> There is nothing in between: no "maybe", no "half working". Real life
> has plenty of maybes, and we agree to leave them outside for now. The
> moves allowed are `and`, `or`, `not` and `!=`. We also meet a short
> loop, which Python gives us without asking, and use it gently.

## Warm-up

Two questions from earlier pages. The first is from
[Choosing a path: if, elif and else](tutorial:choosing-a-path), and the
second from
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).

```question
id: true-false-warm-up-1
type: fill-in-the-blank

An iPhone is designed to work from 0 °C to 35 °C. The temperature 36 is
outside that range, so `between(36, 0, 35)` gives {False|True}.
```

```question
id: true-false-warm-up-2
type: multiple-choice
correct: 3

One byte is 8 bits, and holds 256 different values. How many different
values can 3 bits hold?

- 3
- 6
- 8
- 9
```

## True and false are values

On the last page, every condition had an answer, `True` or `False`. A
*Boolean value* is a value that is either True or False, and nothing
else. The name comes from George Boole, who worked out the rules of
these values in the 1840s and 1850s, in Cork.

Boole's idea was that True and False can be combined, the way numbers
can be added. Boolean values have three words for it: `and`, `or` and
`not`.

<aside class="dl-note" id="true-false-note-boole">

**George Boole.** Boole taught himself most of his mathematics, and
never studied at a university. In 1849 he became the first professor of
mathematics at Queen's College Cork, now University College Cork. In
1937, Claude Shannon showed that Boole's algebra describes circuits of
switches. Every chip in your phone is built on that idea.

</aside>

## And: both must be true

Here is the bike-share rule in Python. Before you run it, what do you
think it prints?

```python exec
id: true-false-and-1
paid_up = True
dock_working = False

unlock = paid_up and dock_working
print(unlock)
```

The bike stays locked. `A and B` is True only when A is True and B is
True as well. One False is enough to make the whole thing False.

That was one situation. How many are there? `paid_up` can be False or
True. For each of those, `dock_working` can be False or True. So there
are four situations, and we want to see all of them.

A *loop* repeats some lines, once for each value in a list. The line
`for paid_up in [False, True]:` means "do the pushed-in lines once with
`paid_up` as False, then once with it as True". That is all we need from
loops for now. Unit 3 is where we learn them properly.

How many lines will this cell print? Guess before you run it.

```python exec
id: true-false-and-2
for paid_up in [False, True]:
    for dock_working in [False, True]:
        print(paid_up, dock_working, paid_up and dock_working)
```

Four lines, one for each situation. Look at the order. The outer loop
picks a value for `paid_up`. While it holds that value, the inner loop
runs through both values of `dock_working`. Then the outer loop moves
on. The order of the two `for` lines decides the order of the rows.

A *truth table* is a table that lists every combination of inputs, with
the result for each one. Here is the one we printed, tidied up:

| `paid_up` | `dock_working` | `paid_up and dock_working` |
|---|---|---|
| False | False | False |
| False | True | False |
| True | False | False |
| True | True | True |

Maths writes "A and B" as $A \land B$. The symbol looks like the letter A
without its middle line, which is one way to remember it.

## Or: at least one is true

Your phone unlocks with your fingerprint or with your PIN. What if the
fingerprint works, and you also type the right PIN? Nobody would expect
the phone to stay locked. Python agrees. Before you run the cell, which
rows do you think will say True?

```python exec
id: true-false-or-1
for fingerprint_ok in [False, True]:
    for pin_ok in [False, True]:
        print(fingerprint_ok, pin_ok, fingerprint_ok or pin_ok)
```

`A or B` is True when at least one of A and B is True. It is False only
when both are False. Maths writes it as $A \lor B$.

This "or" includes the row where both are True, so it is called
*inclusive or*. English uses "or" both ways, so we need to be careful
with it.

### Your turn

An office door opens when your keycard is valid or someone presses the
button on the inside.

1. In the cell below, write a loop over `card_valid` and a loop inside it
   over `button_pressed`, like the ones above.
2. Print both inputs and whether the door opens.
3. Before you run it, say which row is the only False one.

```python exec
id: true-false-your-turn-1
# Your door truth table
```

## Not: the opposite

`not` takes one Boolean value and gives back the other one. `not True`
is False, and `not False` is True. With one input there are only two
rows. Guess them, then run it to check.

```python exec
id: true-false-not-1
for muted in [False, True]:
    print(muted, not muted)
```

Maths writes "not A" as $\lnot A$.

"The phone rings if it is not muted" becomes `rings = not muted`,
which is close to the English.

## Exclusive or: exactly one

A payment form says "pay by card or by cash". Here "or" means one of the
two, but not both. This is *exclusive or*, often written XOR. It is True
when exactly one of its inputs is True.

A real place where XOR lives is the light on a staircase. There is a
switch at the bottom and a switch at the top. Flipping either switch
changes the light. One common way to wire it makes the light come on
when exactly one of the two switches is up.

Python has no word for XOR. It does not need one. When are two Boolean
values different? Exactly when one is True and the other is False.
So for Boolean values, `!=` is XOR. Which rows do you expect to say
True?

```python exec
id: true-false-xor-1
for bottom_up in [False, True]:
    for top_up in [False, True]:
        print(bottom_up, top_up, bottom_up != top_up)
```

Put the four tables side by side and the difference shows in the last
row:

| A | B | A and B | A or B | A XOR B |
|---|---|---|---|---|
| False | False | False | False | False |
| False | True | False | True | True |
| True | False | False | True | True |
| True | True | True | True | False |

Maths writes XOR as $A \oplus B$. On
[Bits that flip](tutorial:bits-that-flip) we will meet it again, working
on the bits of numbers, and see how it catches a mistake in a message.

```question
id: true-false-xor-2
type: multiple-choice
correct: 2

You flip the bottom switch, and then the top switch. The light started
off. What is it now?

- On, because two flips add up
- Off, because the second flip undoes the first
- It depends on which switch was flipped first
```

## How many rows?

A company's computer lets you log in when your password is right, and
you are either at the office or you type a code from your phone. That
rule has three inputs. How many rows will its truth table have? Make a
guess, then run the cell and count.

```python exec
id: true-false-rows-1
for password_ok in [False, True]:
    for at_office in [False, True]:
        for code_ok in [False, True]:
            log_in = password_ok and (at_office or code_ok)
            print(password_ok, at_office, code_ok, log_in)
```

Eight rows. The brackets say which part to work out first, the same way
they do in arithmetic: first `at_office or code_ok`, then `and` with the
password.

Now look at the count. One input gave 2 rows. Two inputs gave 4. Three
gave 8. Each new input doubles the rows, because every old row appears
twice: once with the new input False, and once with it True. For $n$
inputs there are

$$2^n \text{ rows}$$

That is the same doubling as bits and bytes: 8 bits hold $2^8 = 256$
values.

In fact, the rows are more than the same count. `int()` turns `False`
into 0 and `True` into 1. What do you think the rows will look like now?
Run it to check.

```python exec
id: true-false-rows-2
for password_ok in [False, True]:
    for at_office in [False, True]:
        for code_ok in [False, True]:
            print(int(password_ok), int(at_office), int(code_ok))

print("Rows for 3 inputs:", 2 ** 3)
print("Rows for 10 inputs:", 2 ** 10)
```

Read down the rows: 000, 001, 010, 011, 100, 101, 110, 111. That is
counting from 0 to 7 in binary. Nobody told the loops to count in
binary. They did it anyway. I find that one of the nicest surprises in this
unit. A truth table with $n$ inputs is every number from 0 to $2^n - 1$,
written in $n$ bits.

A rule with 10 inputs has 1,024 rows. Nobody wants to write those by
hand, but a computer does not mind.

## A tool for any rule

So far we wrote new loops for every rule. Let's make one tool that
prints the truth table of any rule we give it.

First, a rule becomes a function. Here are the three rules we have met
so far. Each takes Boolean values in and gives one Boolean value back.

```python exec
id: true-false-tool-1
def unlock(paid_up, dock_working):
    """The bike-share rule: both must be True."""
    return paid_up and dock_working


def unlock_phone(fingerprint_ok, pin_ok):
    """The phone rule: at least one must be True."""
    return fingerprint_ok or pin_ok


def log_in(password_ok, at_office, code_ok):
    """The office login rule."""
    return password_ok and (at_office or code_ok)


print(unlock(True, False))
```

Here is something new. A function is a value too, so we can hand the
rule itself to another function, without brackets after its name.
`truth_table(unlock, ["paid_up", "dock_working"])` hands over the rule
`unlock`, and the names of its two inputs. Then `truth_table` can call
`unlock` once for every row.

Here is the promise of `truth_table`:

- It prints a heading of the input names, then every row of the rule.
- It gives back the result column as a list, so we can test it.
- It works for rules with one, two or three inputs.

Three small pieces help it. `len(names)` is how many names the list
holds. `names[0]` is the first name, because Python counts positions
from 0. And `results.append(result)` adds one value to the end of the
list `results`. We use `sep="\t"` inside `print` to put a tab between
values, so the columns line up.

This is a toolkit cell. The branches for one input and two inputs are
written for you. Can you write the branch for three inputs? It follows
the same pattern, with one more loop.

```python exec
id: true-false-toolkit
toolkit: yes
def truth_table(rule, names):
    """Print every row of rule, for one, two or three True/False inputs.

    names holds the name of each input, in order. Give back the
    result column as a list, from the all-False row to the all-True row.
    """
    results = []
    if len(names) == 1:
        print(names[0], "result", sep="\t")
        for a in [False, True]:
            result = rule(a)
            print(a, result, sep="\t")
            results.append(result)
    elif len(names) == 2:
        print(names[0], names[1], "result", sep="\t")
        for a in [False, True]:
            for b in [False, True]:
                result = rule(a, b)
                print(a, b, result, sep="\t")
                results.append(result)
    # Your branch for three names goes here, as another elif.
    else:
        print("truth_table works for one, two or three names.")
    return results
```

```python toolkit-reference
for: true-false-toolkit
def truth_table(rule, names):
    """Print every row of rule, for one, two or three True/False inputs.

    names holds the name of each input, in order. Give back the
    result column as a list, from the all-False row to the all-True row.
    """
    results = []
    if len(names) == 1:
        print(names[0], "result", sep="\t")
        for a in [False, True]:
            result = rule(a)
            print(a, result, sep="\t")
            results.append(result)
    elif len(names) == 2:
        print(names[0], names[1], "result", sep="\t")
        for a in [False, True]:
            for b in [False, True]:
                result = rule(a, b)
                print(a, b, result, sep="\t")
                results.append(result)
    elif len(names) == 3:
        print(names[0], names[1], names[2], "result", sep="\t")
        for a in [False, True]:
            for b in [False, True]:
                for c in [False, True]:
                    result = rule(a, b, c)
                    print(a, b, c, result, sep="\t")
                    results.append(result)
    else:
        print("truth_table works for one, two or three names.")
    return results
```

Run the toolkit cell, then try the tool. What do you expect to see
under the table?

```python exec
id: true-false-tool-2
truth_table(unlock, ["paid_up", "dock_working"])
```

The table comes from the `print` lines. Under it is what `truth_table`
gave back: the column `[False, False, False, True]`. Printing is for us
to read. Giving back is for other code, including tests.

The tests below check the promise. Each one prints its table as it
runs, and the `assert` checks the column. Until your three-input branch
is written, expect the last test to stop with an `AssertionError`.

```python exec
id: true-false-tool-3
assert truth_table(unlock, ["paid_up", "dock_working"]) == [False, False, False, True]
assert truth_table(unlock_phone, ["fingerprint_ok", "pin_ok"]) == [False, True, True, True]
assert len(truth_table(log_in, ["password_ok", "at_office", "code_ok"])) == 8
print("truth_table keeps its promise.")
```

The last test only checks that there are $2^3 = 8$ rows. Can you add an
`assert` for the whole login column? "How many rows?" has the answer.

### Your turn: a digit display

A seven-segment display, like the one Unit 1 builds, shows a digit with seven small bars, called
segments, which each light up or stay dark. You have seen them on
microwaves and alarm clocks. Engineers name the segments with letters,
from a at the top, round the outside, to g in the middle. Segment e is
the one at the bottom left.

Among the digits 0 to 7, segment e lights for 0, 2 and 6 only. (Draw
them in the margin to check.) A three-input truth table lists 0 to 7 in
binary, so "does e light?" is a rule with three inputs: the bits worth
4, 2 and 1.

1. Write `bottom_left(bit_4, bit_2, bit_1)`, which gives True for the
   rows of 0, 2 and 6, and False for the others.
2. Print its table with `truth_table`, and check that the column is
   `[True, False, True, False, False, False, True, False]`.

```python exec
id: true-false-your-segment
# Your bottom_left rule, and its truth table
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 0, 2 and 6 are all even. What is `bit_1` for an even number?
2. Among the even digits 0, 2, 4 and 6, only 4 stays dark. 4 is `100`.
3. So e lights when `bit_1` is off, and the digit is not `100`: `bit_2`
   is on, or `bit_4` is off.

**Think about:** how many different rules could give this same column?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one good answer. There are many others, and yours may read
better.

```python
def bottom_left(bit_4, bit_2, bit_1):
    """True when segment e lights, for the digits 0 to 7."""
    return not bit_1 and (bit_2 or not bit_4)

column = truth_table(bottom_left, ["bit_4", "bit_2", "bit_1"])
print(column == [True, False, True, False, False, False, True, False])
```

The last line prints `True`. A chip inside a real display works out a
rule like this for each of the seven segments.

</details>

<aside class="dl-note" id="true-false-note-decoder">

**A chip for every segment.** Many clocks use a small decoder chip,
such as the CD4511, that takes a digit as four bits and lights the right
segments. Inside, it is seven truth tables. Displays do not all agree:
some draw 6 without its top bar.

</aside>

## Brackets change the rule

Here is a question that many programmers get wrong. The login rule had
brackets: `password_ok and (at_office or code_ok)`. What if someone
writes the brackets in a different place?
`(password_ok and at_office) or code_ok` uses the same words, in the
same order. Is it the same rule?

Guess first. Then run the cell and compare the two result columns row
by row. This cell needs the three-input branch of your `truth_table`, so
finish that first.

```python exec
id: true-false-brackets-1
def log_in_other_brackets(password_ok, at_office, code_ok):
    """The login words, with the brackets moved."""
    return (password_ok and at_office) or code_ok


first = truth_table(log_in, ["password_ok", "at_office", "code_ok"])
second = truth_table(log_in_other_brackets, ["password_ok", "at_office", "code_ok"])
print(first == second)
```

They are different. Look at the rows where `password_ok` is False and
`code_ok` is True. The second rule lets those people in. Anyone who has
the phone code gets in with no password at all. That is a real security
hole, made by moving two brackets.

The brackets decide what happens first, and what happens first changes
the answer. That is the same lesson as the order of the `elif` checks on
the last page. The next page,
[Untangling a condition](tutorial:untangling-a-condition), looks at what
Python does when there are no brackets at all.

### Your turn

A phone plays a notification sound when a message arrives, and the phone
is not on silent, or the message is from a favourite contact.

1. Write it as a function with three inputs: `message`, `silent` and
   `favourite`. You will need `not`, and brackets.
2. Print its truth table with `truth_table`.
3. Find the row where a favourite contact's message makes a sound even on
   silent. Is that what you wanted the rule to say? If not, move the
   brackets.

```python exec
id: true-false-your-turn-2
# Your notification rule
```

<details class="dl-why"><summary>Why this way?</summary>

On this page, Python wrote every truth table for us, with a short loop.
The more usual way is to fill the table in on paper, one row at a time.

Filling a table by hand is slower, and that is its strength: you look
at every row yourself.

We let the computer write the rows because the page asked "can we list
every case, and be sure we missed none?". A loop never forgets a row,
and it writes 1,024 rows as readily as 4. The cost was meeting a loop a
unit before loops are taught.

</details>

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | Each input got a name (`paid_up`, `code_ok`), and so did each rule (`unlock`, `log_in`). A rule's name can be handed to another function. |
| What is promised? | `and`, `or`, `not` and XOR each promise one result for every row. `truth_table` promises every row, and gives back the result column. |
| What happens when? | Nested loops run the inner loop fully for each value of the outer one, which counts in binary. Brackets decide which part is worked out first. |
| What does this space let us do? | Only True and False live here. That is what makes "every case" a list we can finish: $2^n$ rows for $n$ inputs. |

## What we have now

| Term or move | What it means |
|---|---|
| Boolean value | `True` or `False`, and nothing else |
| `and` ($\land$) | True only when both inputs are True |
| `or` ($\lor$) | True when at least one input is True: inclusive or |
| `not` ($\lnot$) | Gives the other value |
| XOR ($\oplus$) | True when exactly one input is True. For Boolean values, `!=` does it. |
| truth table | Every combination of inputs, with the result for each |
| $2^n$ rows | The number of rows for $n$ inputs. The rows count in binary. |
| `for x in [False, True]:` | A loop: do the pushed-in lines once for each value |
| `truth_table(rule, names)` | Your toolkit tool that prints any rule's table, for up to three inputs |

For another route through the same ideas, the integrated course has
[Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth).
