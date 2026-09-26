---
title: "Logic: truth tables, XOR and De Morgan's laws"
year: "2026-2027"
version: 2026.08.23.1
covers:
  every-possible-case:
    covers: [MIT-2.4]
  exclusive-or:
    covers: [MIT-2.4]
  de-morgans-laws:
    covers: [MIT-2.5]
  where-you-have-already-used-this:
    covers: [MIT-2.5]
  the-same-shapes-on-sets:
    covers: [MIT-2.5]
---

# Logic: truth tables, XOR and De Morgan's laws

You have been writing `and`, `or` and `not` since
[Making decisions with if, elif and else](tutorial:making-decisions).
There we met a short rule for each operator. On this page we lay out
every case in full.

The operators are everywhere in code, so it can feel as if there is
nothing left to learn about them. But here is a question that most
people find hard, even after a month of using them: what is
`not (A and B)` the same as? And why can a condition work correctly, but
still be very hard to read?

On this page we:

- list every case for `and`, `or` and `not`, in tables made by a loop
- meet a fourth operator, *exclusive or*, and build it three ways
- learn two rules, De Morgan's laws, that turn a tangled condition into
  one a person can read
- see the same two rules at work on sets

This page comes after
[Sets: building them from sorted lists](tutorial:sets-as-sorted-lists)
on purpose. Union and intersection showed us a pattern. The logic here
turns out to be the same pattern with different names.

## Every possible case

An `and` takes two values, each either `True` or `False`, and gives back
one value. Each input has only two possibilities, so there are only four
situations in total. Four is few enough to list them all.

A *truth table* is a list of every possible combination of inputs, with
the result for each one. Here is the truth table for `and`:

```python exec
id: every-possible-case-1
print("   A        B      A and B")
for a in [True, False]:
    for b in [True, False]:
        print(f"{str(a):>6} {str(b):>7} {str(a and b):>10}")
```

There are four rows, and a loop made them. Nobody typed them out. This is
the main idea of this section. A truth table is what you get when you try
every input, so there is no need to memorise it. And trying every input
is a nested loop, which you can already write.

Here are the truth tables for the other two operators:

```python exec
id: every-possible-case-2
print("   A        B      A or B")
for a in [True, False]:
    for b in [True, False]:
        print(f"{str(a):>6} {str(b):>7} {str(a or b):>10}")

print()
print("   A      not A")
for a in [True, False]:
    print(f"{str(a):>6} {str(not a):>10}")
```

`or` is true when either input is true, and that includes when both are
true. This is the one that trips people up. In everyday English, "or"
usually means one or the other, but not both. If someone asks "tea or
coffee?", they do not expect you to say "both". The logical `or` does
include both.

### Your turn

What would the truth table for `A and (not B)` look like?

1. Predict the four rows, and write them down.
2. Write a loop, like the ones above, that prints the table.
3. Run it, and compare with your prediction.

```python exec
id: your-turn-1
# Your loop here.
```

## Exclusive or

The everyday "or", the one that leaves out "both", also has a name.
*Exclusive or*, or *XOR* for short, is true when exactly one of its two
inputs is true.

Python has no `xor` keyword. That gives us a chance to build it
ourselves, in three different ways, from things we already have. Look
at the three column headings in the next cell. What do you expect to see
in the three columns? Run it to check.

```python exec
id: exclusive-or-1
def xor_written_out(a, b):
    return (a or b) and not (a and b)


print("   A        B     XOR    !=     ^")
for a in [True, False]:
    for b in [True, False]:
        print(f"{str(a):>6} {str(b):>7} {str(xor_written_out(a, b)):>7}"
              f" {str(a != b):>5} {str(a ^ b):>5}")
```

The three columns are the same all the way down.

The middle column deserves a second look. For `True` and `False`
values, "exclusive or" and "not equal to" are the *same operation*.
Exactly one of the two being true means the same as the two being
different. This is not a coincidence or a trick. It is one idea with two
names, because people reached it from different directions.

The third column uses `^`. This is Python's *bitwise XOR*. It works on
whole numbers, one binary digit (bit) at a time. It also gives the right
answer for `True` and `False`.

### Your turn

Can you write XOR a fourth way, using only `not` and `==`?

1. Fill in the body of `xor_again(a, b)`.
2. Check it against all four rows, with a loop like the one above.

```python exec
id: your-turn-2
def xor_again(a, b):
    pass


# Check it here.
```

## De Morgan's laws

*De Morgan's laws* are two rules for moving a `not` inside a bracket.
Here they are:

> `not (A and B)` is the same as `(not A) or (not B)`
>
> `not (A or B)` is the same as `(not A) and (not B)`

In words: when you move a `not` inside a bracket, each `and` becomes an
`or`, and each `or` becomes an `and`.

The rules are easy to state and hard to believe. So we will not ask you
to believe them. We will check them, with a loop over every case. Before
you run the two cells, what do you expect the last two columns to show?

```python exec
id: de-morgans-laws-1
print("   A        B    not(A and B)   (not A) or (not B)")
for a in [True, False]:
    for b in [True, False]:
        left = not (a and b)
        right = (not a) or (not b)
        print(f"{str(a):>6} {str(b):>7} {str(left):>12} {str(right):>18}")
```

```python exec
id: de-morgans-laws-2
print("   A        B    not(A or B)   (not A) and (not B)")
for a in [True, False]:
    for b in [True, False]:
        left = not (a or b)
        right = (not a) and (not b)
        print(f"{str(a):>6} {str(b):>7} {str(left):>12} {str(right):>19}")
```

In both laws, the two columns match in every row.

That loop is the proof. It is not an example of the proof, and it is not
evidence for it. It is the whole proof. There are exactly four cases,
and the loop tried all four.

This is unusual, and it is worth stopping to think about. Usually, "I
tested it and it worked" is a weak argument. Testing a few inputs cannot
show that a program works for every input, and you will soon see this
go wrong in real code. Here the argument is complete, because there are
only four possible inputs, and we tried every one. Checking every case
is a proof when there are few enough cases to check them all, and almost
never otherwise.

## Where you have already used this

Why learn De Morgan's laws? They turn conditions that are hard to read
into conditions that are easy to read.

Here is a condition of the kind that turns up in real code. The last
lines use `all()`, a built-in function that gives `True` when every
value it is given is `True`. The `for` parts inside it work like a list
comprehension: they try all four combinations of `a` and `s`.

What do you think the cell prints? Run it to check.

```python exec
id: where-you-have-already-used-this-1
def can_sit_exam(attended, submitted):
    return not (not attended or not submitted)


def can_sit_exam_readable(attended, submitted):
    return attended and submitted


print("agree everywhere:",
      all(can_sit_exam(a, s) == can_sit_exam_readable(a, s)
          for a in [True, False] for s in [True, False]))
```

The first version has three `not`s, and it takes a moment to work out.
The second version says what it means. They are the same function, and
De Morgan's laws take you from one to the other.

People rarely write the first version on purpose. It grows a little at a
time: someone adds a condition, later wraps the whole thing in a `not`,
then adds another condition. Knowing the laws lets you untangle it
afterwards.

### Your turn

Here are three conditions to simplify. How would you rewrite each one?

1. Write a simpler version of `one`, `two` and `three`.
2. Check that each simpler version agrees with the original in every
   case, with the same `all(...)` check as above. For `three`, which
   has three inputs, the check needs a third `for` part.

```python exec
id: your-turn-3
def one(a, b):
    return not (a and not b)


def two(a, b):
    return not (not a and not b)


def three(a, b, c):
    return not (a or (b and not c))


# Your simplified versions, and a check that each agrees with the original.
```

## The same shapes, on sets

Here is the reason this page comes after
[Sets: building them from sorted lists](tutorial:sets-as-sorted-lists).

Everything above was about `True` and `False`. The same two laws hold for
sets. Union takes the place of `or`, intersection takes the place of
`and`, and complement takes the place of `not`.

To talk about a complement, we need a *universal set*. The universal set
is the set of everything we are talking about. In the next cell it is
called `everyone`. The *complement* of a set is everything in the
universal set that is not in that set.

The cell uses Python's own `set` type. Python writes a set in curly
brackets, and gives us `|` for union, `&` for intersection and `-` for
difference. These are the same operations we built ourselves from
sorted lists on the sets page.

Before you run it, look at each pair of lines. Should the two lines in
each pair print the same set?

```python exec
id: the-same-shapes-on-sets-1
everyone = {1, 2, 3, 4, 5, 6, 7, 8}
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

def complement(s):
    return everyone - s


print("not (A or B):        ", complement(a | b))
print("(not A) and (not B): ", complement(a) & complement(b))
print()
print("not (A and B):       ", complement(a & b))
print("(not A) or (not B):  ", complement(a) | complement(b))
```

Each pair gives the same set. These are the same two laws, with sets
instead of `True` and `False`.

So De Morgan's laws are one idea that appears in two places. A statement
is either true or false. An item is either in a set or out of it. These
are the same kind of question, asked about different things. Once you
see that, a rule you learned in one place works in the other, and you do
not have to learn it again.

This connection is why this page sits where it does, and it is the most
useful idea on the page.
[Venn diagrams: drawing sets and their overlaps](tutorial:venn-diagrams)
turns it into a picture. There, we shade the same two laws on a diagram,
and check them by looking instead of by counting rows.

## Reflection

We met three operators with four rows each (`not` needs only two), a
fourth operator built three ways, and two rules for moving a `not`
through a bracket. These are the ideas worth keeping:

- **A truth table is a loop over every case.** There is no need to
  memorise it. If you forget what `or` does, generate the table.
- **Checking every case is a proof only when there are few cases.** Four
  rows is few. Almost nothing else you meet will be that small.
- **De Morgan's laws are for readability.** They turn tangled conditions
  into ones a person can read. They do not make code do anything new.
  You will mostly use them on code you wrote yourself two weeks earlier.

Now look back at something you have written before, and find a
condition in it. In a few sentences, say whether De Morgan's laws would
make it easier to read.

## Where to Read More

Khan Academy. *Equivalent Compound Booleans.*
<https://www.khanacademy.org/computing/ap-computer-science-principles/programming-101/x2d2f703b37b450a3:logical-equivalence/a/equivalent-compound-booleans>.
De Morgan's Laws from the programming side, with the same two rules this
page proves by looping over four rows.

Steve Mould (2013). *Can you solve this 4 card puzzle?*
<https://www.youtube.com/watch?v=Hpwd_ns2Wjs>. A famous puzzle that most
people get wrong the first time, because an "if" does not mean what we
expect. Three minutes. Write your answer down before the end.

CrashCourse (2017). *Boolean Logic & Logic Gates: Crash Course Computer
Science #3.* <https://www.youtube.com/watch?v=gI-qXk7XojA>. AND, OR, NOT
and XOR as switches inside a computer, each with its truth table. About
ten minutes.
