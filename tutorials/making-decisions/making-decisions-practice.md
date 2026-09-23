---
title: "Making decisions with if, elif and else — Practice"
practice_for: making-decisions
year: "2026-2027"
version: 2026.09.22.1
---

# Making decisions with if, elif and else — Practice

The answers are hidden until you open them. Before you write an `if`,
work out which values its condition is True for. When a conditional is
broken, the fault is most often in the condition, not in the branches.

## Comparisons

```python exec
id: comparisons-1
a = 7
b = 3
print(a > b, a < b, a >= b, a == b, a != b)
```

**1.** What does each of these give? Predict first, then check.

- (a) `5 > 3`
- (b) `5 >= 5`
- (c) `"apple" < "banana"`
- (d) `"Apple" < "apple"`
- (e) `10 == 10.0`
- (f) `"10" == 10`

<details class="dl-answer"><summary>answer</summary>

(a) True. (b) True. (c) True. (d) True. (e) True. (f) False.

Python compares strings in alphabetical order. Capital letters come
before small letters, because of where they sit in the character table.
That is why a simple sort puts `Zoe` before `adam`.

The last two belong together. `10 == 10.0` is True, because both are the
number ten. `"10" == 10` is False, because `"10"` is text and `10` is a
number.

</details>

**2.** What is the difference between `=` and `==`?

<details class="dl-answer"><summary>answer</summary>

`=` assigns: it puts a value into a name. `==` asks a question: it gives
back `True` or `False`.

In Python, `if x = 5:` is a syntax error, and that is a help to you. In
some other languages this line is allowed. It quietly sets `x` to 5, and
the condition is then always true.

</details>

**3.** Can you write a condition that is True when a number is strictly
between 10 and 20?

<details class="dl-answer"><summary>answer</summary>

```python
10 < n < 20
```

Python allows chained comparisons like this one, and they mean what they
look like. Most other languages need `n > 10 and n < 20`. That form also
works in Python, and it is worth being able to write it.

</details>

## If, Else, Elif

**4.** What does this print when `mark` is 75? When it is 40? When it is
40.5?

```python
if mark >= 70:
    print("Distinction")
elif mark >= 50:
    print("Merit")
elif mark >= 40:
    print("Pass")
else:
    print("Fail")
```

<details class="dl-answer"><summary>answer</summary>

`Distinction`, `Pass`, `Pass`.

Only one branch ever runs: the first one whose condition is True. That is
why the order matters. If `>= 40` came first, every mark from 40 up would
print `Pass`.

</details>

**5.** This code is wrong. Why? What does it print for a mark of 85?

```python
if mark >= 40:
    print("Pass")
if mark >= 50:
    print("Merit")
if mark >= 70:
    print("Distinction")
```

<details class="dl-answer"><summary>answer</summary>

It prints all three.

Separate `if` statements are separate questions, and Python asks each
one in turn. `elif` means "otherwise, ask this". A grade needs `elif`,
because a mark belongs to only one grade.

</details>

**6.** Write a program that prints whether a number is positive,
negative or zero.

<details class="dl-answer"><summary>answer</summary>

```python
if n > 0:
    print("positive")
elif n < 0:
    print("negative")
else:
    print("zero")
```

There are three cases, and zero has to be one of them. If you write
`if n >= 0: print("positive")`, zero gets the wrong answer, and zero is
exactly the value a tester will try.

</details>

**7.** Write a program that prints whether a number is even or odd. Then
extend it to say "even and positive", "even and negative", and so on.

<details class="dl-answer"><summary>answer</summary>

```python
if n % 2 == 0:
    print("even")
else:
    print("odd")
```

And with the sign:

```python
parity = "even" if n % 2 == 0 else "odd"
sign = "positive" if n > 0 else "negative" if n < 0 else "zero"
print(parity, "and", sign)
```

This version uses a short form of if-else that fits on one line:
`"even" if n % 2 == 0 else "odd"` gives `"even"` when the condition is
True, and `"odd"` when it is False.

Even or odd, and the sign, are two separate questions, so the code makes
two separate decisions. You could write it as one long `if` instead. It
would work, but it would need four branches, and six once you include
zero.

</details>

## Boolean Operators

This cell prints every result of `and` and `or`. It uses a loop, which we
meet in [Repeating steps with loops](tutorial:repeating-yourself). For now, you
only need its output.

```python exec
id: boolean-operators-1
# Every pair of True and False, with the result of "and" and "or" for each
for p in [True, False]:
    for q in [True, False]:
        print(p, q, "   and:", p and q, "   or:", p or q)
```

**8.** Predict each one.

- (a) `True and False`
- (b) `True or False`
- (c) `not True`
- (d) `not (5 > 3)`
- (e) `(5 > 3) and (2 > 4)`
- (f) `(5 > 3) or (2 > 4)`

<details class="dl-answer"><summary>answer</summary>

False, True, False, False, False, True.

</details>

**9.** A cinema gives a discount to anyone under 16 or over 65. Write the
condition.

<details class="dl-answer"><summary>answer</summary>

```python
age < 16 or age > 65
```

With `and`, nobody would get the discount, because no age is both under
16 and over 65. When a condition comes out True for nothing, or for
everything, the operator is often the part that is wrong.

</details>

**10.** A password is acceptable if it has at least 8 characters and
contains a digit. Write the condition. You have `password`, and a
variable `has_digit` that is `True` or `False`. (`len(password)` gives
the number of characters in `password`. We meet `len()` properly in
[Lists: keeping many values in order](tutorial:lists-and-sequences).)

<details class="dl-answer"><summary>answer</summary>

```python
len(password) >= 8 and has_digit
```

There is no `== True` on the end. `has_digit` is already True or False,
so comparing it to `True` adds a step and tells us nothing new.

</details>

**11.** Write the condition for "this year is a leap year", using the
full rule: divisible by 4, except for centuries, unless divisible by 400.

<details class="dl-answer"><summary>answer</summary>

```python
(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
```

Check it against 2024 (True), 1900 (False), 2000 (True) and 2023
(False).

Python does not need the brackets, because it works out `and` before
`or`. Without them, though, a reader has to work out that order to check
your logic. The brackets save them the effort.

</details>

**12.** Write `not (a > b)` in a simpler way.

<details class="dl-answer"><summary>answer</summary>

`a <= b`.

The opposite of "greater than" is "less than or equal to". It is not
"less than". Forgetting the equal case is one of the most common
off-by-one bugs.

</details>

**13.** Write `not (a and b)` in a simpler way.

<details class="dl-answer"><summary>answer</summary>

`(not a) or (not b)`.

This is De Morgan's law. We meet it again in
[Logic and Truth](tutorial:logic-and-truth) and in
[Drawing Sets](tutorial:venn-diagrams). The opposite of "both" is "at
least one is not". The other half of the law: the opposite of "either"
is "neither".

</details>

**14.** What does this print? Why does Python never work out the second
condition?

```python
n = 0
if n != 0 and 10 / n > 1:
    print("yes")
else:
    print("no")
```

<details class="dl-answer"><summary>answer</summary>

It prints `no`, with no error.

Python stops working out an `and` as soon as one side is False, because
nothing on the right can make the whole thing True. This is called
*short-circuiting*. Here it does real work: it is the guard that stops
the division by zero. Swap the two conditions, and the program crashes.

</details>

## From the Everlearning Problem Bank

These problems come from the shared problem bank, written again for this
page. The answers are written as small functions, using `def` and
`return`. We meet these properly in
[Writing your own functions](tutorial:writing-your-own-functions). For now, you can
read `def opposite_signs(a, b):` as "here is a rule called
`opposite_signs` that takes two values", and `return` as "give back this
answer". You can also answer each problem with an ordinary `if`.

**15.** You have two integers. Give back `True` if one is negative and
the other is positive, and `False` if not.

<details class="dl-answer"><summary>answer</summary>

```python
def opposite_signs(a, b):
    return (a < 0) != (b < 0)
```

This short version checks whether the two True/False values are
different. They are different exactly when the signs are different.

The long version is `(a < 0 and b > 0) or (a > 0 and b < 0)`. The two
versions give different answers for zero:

- The short version sorts every number into "negative" or "not
  negative". So `0` and `-5` give `True`.
- The long version asks for one number below zero and one number above
  zero. So the same pair gives `False`.

Neither is wrong, because the question did not say what to do with
zero. When a specification has a gap in it, whoever writes the code
fills the gap. That is the real lesson here.

</details>

**16.** Give back `True` if the sum of two integers is 20, or if one of
them is 20.

<details class="dl-answer"><summary>answer</summary>

```python
def twenty(a, b):
    return a == 20 or b == 20 or a + b == 20
```

</details>

**17.** Give back `True` if a number is within 20 of 100, or within 20
of 200.

<details class="dl-answer"><summary>answer</summary>

```python
def near(n):
    return abs(n - 100) <= 20 or abs(n - 200) <= 20
```

`abs()` gives the size of a number without its sign, so `abs(-7)` is
`7`. `abs(n - target) <= 20` is the general shape of "within 20 of".
It saves writing two comparisons for each target.

</details>

**18.** Give back `True` when a positive number is a multiple of 3 or a
multiple of 7.

<details class="dl-answer"><summary>answer</summary>

```python
def multiple_of_three_or_seven(n):
    return n % 3 == 0 or n % 7 == 0
```

21 is a multiple of both, and `or` accepts that. What if you wanted
"exactly one of the two"? Then you would use `!=` between the two
conditions, as in problem 15.

</details>

## Classifying Numbers

**19.** Write a classifier that says which number families a value
belongs to: natural, integer, rational, real.

<details class="dl-answer"><summary>answer</summary>

```python
def classify(value):
    is_integer = value == int(value)
    is_natural = is_integer and value >= 0
    if is_natural:
        return f"{value} is natural, and therefore integer, rational and real"
    if is_integer:
        return f"{value} is an integer, and therefore rational and real"
    return f"{value} is rational and real, but not an integer"


for v in [7, -3, 0, 0.5, -3.5]:
    print(classify(v))
```

The strings with `f` in front are f-strings, from
[Variables, data types and text](tutorial:storing-and-computing). The last two
lines use a loop to try five values in turn; we meet loops in
[Repeating steps with loops](tutorial:repeating-yourself).

The families sit one inside the next, and that gives the code its shape.
Each family contains the ones before it, so the first test that comes
out True gives the most exact answer. For the same reason, we check
grade boundaries from the top down.

</details>

**20.** The classifier above says every Python float is rational. Is
that true?

<details class="dl-answer"><summary>answer</summary>

For the floats themselves, yes. Apart from a few special values, such as
infinity, every float is a whole number times a power of two, and that
is a fraction.

For the numbers the floats *stand for*, no. `math.pi` is a float, and π
is irrational, so the float is only a rational number close to π. The
exact statement is this: a computer cannot store an irrational number
exactly, and every number it stores is rational, whether or not the
thing it stands for is rational.

</details>

**21.** A triangle is possible when each side is shorter than the other
two sides added together. Write a checker. What does it give for sides
3, 4, 5? And for 1, 2, 10?

<details class="dl-answer"><summary>answer</summary>

```python
def is_triangle(a, b, c):
    return a + b > c and a + c > b and b + c > a
```

For 3, 4, 5 it gives `True`. For 1, 2, 10 it gives `False`: the two
short sides together cannot reach across the long one.

All three comparisons are needed. If you check only `a + b > c`, then
1, 2, 10 passes when the sides are given in a different order, such as
1, 10, 2.

</details>
