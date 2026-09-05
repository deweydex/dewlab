---
title: "Making Decisions — Practice"
slug: making-decisions-practice
practice_for: making-decisions
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Making Decisions — Practice

Answers are folded. Work out what each condition is true for *before* you write the `if` — most broken conditionals are broken in the condition, not in the branches.

## Comparisons

```python exec
id: comparisons-1
a, b = 7, 3
print(a > b, a < b, a >= b, a == b, a != b)
```

**1.** Predict each, then check.

- (a) `5 > 3`
- (b) `5 >= 5`
- (c) `"apple" < "banana"`
- (d) `"Apple" < "apple"`
- (e) `10 == 10.0`
- (f) `"10" == 10`

<details class="dl-answer"><summary>answer</summary>

(a) True. (b) True. (c) True. (d) True. (e) True. (f) False.

Strings compare alphabetically, and capitals come before lowercase because of where they sit in the character table — which is why sorting names naively puts `Zoe` before `adam`.

The last two together are the important pair. `10 == 10.0` is true because both are the number ten; `"10" == 10` is false because one is text.

</details>

**2.** What is the difference between `=` and `==`?

<details class="dl-answer"><summary>answer</summary>

`=` assigns: it puts a value into a name. `==` asks: it produces `True` or `False`.

`if x = 5:` is a syntax error in Python, which is a kindness — in some languages it is legal, quietly assigns 5, and the condition is then always true.

</details>

**3.** Write a condition that is true when a number is strictly between 10 and 20.

<details class="dl-answer"><summary>answer</summary>

```python
10 < n < 20
```

Python allows chained comparisons and they mean what they look like. Most languages need `n > 10 and n < 20`, which also works here and is worth being able to write.

</details>

## If, Else, Elif

**4.** What does this print when `mark` is 75? When it is 40? When it is 40.5?

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

Only one branch ever runs, and it is the first one whose condition is true. That is why the order matters: put `>= 40` first and everything from 40 up would print `Pass`.

</details>

**5.** This is wrong. Why, and what does it print for a mark of 85?

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

Separate `if` statements are separate questions, each asked in turn. `elif` means "otherwise, ask this", which is what a grade needs — the categories are meant to be exclusive.

</details>

**6.** Write a program that prints whether a number is positive, negative, or zero.

<details class="dl-answer"><summary>answer</summary>

```python
if n > 0:
    print("positive")
elif n < 0:
    print("negative")
else:
    print("zero")
```

Three cases, and zero has to be one of them. Writing `if n >= 0: print("positive")` gets zero wrong, and zero is exactly the value a test will use.

</details>

**7.** Write a program that prints whether a number is even or odd. Then extend it to say "even and positive", "even and negative", and so on.

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

Two independent questions, so two independent decisions. Writing it as one four-branch `if` would work and would need six branches once you include zero.

</details>

## Boolean Operators

```python exec
id: boolean-operators-1
for p in [True, False]:
    for q in [True, False]:
        print(f"{str(p):<6}{str(q):<6} and={p and q!s:<6} or={p or q!s:<6}")
```

**8.** Predict each.

- (a) `True and False`
- (b) `True or False`
- (c) `not True`
- (d) `not (5 > 3)`
- (e) `(5 > 3) and (2 > 4)`
- (f) `(5 > 3) or (2 > 4)`

<details class="dl-answer"><summary>answer</summary>

False, True, False, False, False, True.

</details>

**9.** A cinema gives a discount to anyone under 16 or over 65. Write the condition.

<details class="dl-answer"><summary>answer</summary>

```python
age < 16 or age > 65
```

`and` here would give a discount to nobody, since no age is both. When a condition comes out true for nothing or for everything, the operator is usually the thing that is wrong.

</details>

**10.** A password is acceptable if it is at least 8 characters and contains a digit. Write the condition, given `password` and a variable `has_digit`.

<details class="dl-answer"><summary>answer</summary>

```python
len(password) >= 8 and has_digit
```

Note there is no `== True` on the end. `has_digit` is already true or false; comparing it to `True` adds a step and says nothing.

</details>

**11.** Write the condition for "this year is a leap year", using the full rule: divisible by 4, except centuries, unless divisible by 400.

<details class="dl-answer"><summary>answer</summary>

```python
(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
```

Check it against 2024 (true), 1900 (false), 2000 (true), 2023 (false).

The brackets are not required — `and` binds tighter than `or` — but leaving them out makes the reader work out the precedence to check your logic, and they will not thank you.

</details>

**12.** Simplify `not (a > b)`.

<details class="dl-answer"><summary>answer</summary>

`a <= b`.

The opposite of "greater than" is "less than or equal to", not "less than". Forgetting the equals case is one of the most common off-by-one bugs there is.

</details>

**13.** Simplify `not (a and b)`.

<details class="dl-answer"><summary>answer</summary>

`(not a) or (not b)`.

This is De Morgan's law, and it turns up again in *Logic and Truth* and in *Drawing Sets*. The negation of "both" is "at least one is not". The other half: the negation of "either" is "neither".

</details>

**14.** What does this print, and why does the second condition never get evaluated?

```python
n = 0
if n != 0 and 10 / n > 1:
    print("yes")
else:
    print("no")
```

<details class="dl-answer"><summary>answer</summary>

`no`, with no error.

Python stops evaluating an `and` as soon as one side is false, because nothing on the right can rescue it. This is called short-circuiting, and here it is doing real work: it is the guard that stops the division by zero. Swap the two conditions round and the program crashes.

</details>

## From the Everlearning Problem Bank

These come from the shared problem bank, restated for this page.

**15.** Given two integers, return `True` if one is negative and the other positive, and `False` otherwise.

<details class="dl-answer"><summary>answer</summary>

```python
def opposite_signs(a, b):
    return (a < 0) != (b < 0)
```

Comparing the two truth values for inequality is the neat version — they differ exactly when the signs differ.

The longhand is `(a < 0 and b > 0) or (a > 0 and b < 0)`, and the two disagree about zero. The neat version sorts every number into "negative" or "not negative", so `0` and `-5` come out `True`. The longhand asks for one strictly negative and one strictly positive, so the same pair comes out `False`. Neither is wrong; the question did not say, and that is the actual lesson — a specification with a gap in it gets filled in by whoever writes the code.

</details>

**16.** Return `True` if the sum of two integers is 20, or if one of them is 20.

<details class="dl-answer"><summary>answer</summary>

```python
def twenty(a, b):
    return a == 20 or b == 20 or a + b == 20
```

</details>

**17.** Return `True` if a number is within 20 of either 100 or 200.

<details class="dl-answer"><summary>answer</summary>

```python
def near(n):
    return abs(n - 100) <= 20 or abs(n - 200) <= 20
```

`abs(n - target) <= 20` is the general shape of "within 20 of", and it saves writing two comparisons per target.

</details>

**18.** Return `True` when a positive number is a multiple of 3 or of 7.

<details class="dl-answer"><summary>answer</summary>

```python
def multiple_of_three_or_seven(n):
    return n % 3 == 0 or n % 7 == 0
```

21 satisfies both, and `or` is happy with that. If you wanted "exactly one of the two", that is `!=` on the two conditions again.

</details>

## Classifying Numbers

**19.** Write a classifier that says which of the number families a value belongs to: natural, integer, rational, real.

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

The nesting is the whole structure: each family contains the ones before it, so the first true test is the most specific answer. That is the same reason grade boundaries are checked from the top down.

</details>

**20.** The classifier above says every Python float is rational. Is that true?

<details class="dl-answer"><summary>answer</summary>

Of every float that exists, yes — a float is a whole number times a power of two, which is a fraction.

Of the numbers it is *standing for*, no. `math.pi` is a float, and π is irrational; the float is a rational approximation of it. So the honest statement is that irrational numbers cannot be stored exactly, and every stored number is rational whether or not the thing it represents is.

</details>

**21.** A triangle is valid when each side is shorter than the sum of the other two. Write a checker, and say what it returns for sides 3, 4, 5 and for 1, 2, 10.

<details class="dl-answer"><summary>answer</summary>

```python
def is_triangle(a, b, c):
    return a + b > c and a + c > b and b + c > a
```

3, 4, 5 gives `True`. 1, 2, 10 gives `False` — the two short sides together cannot reach across the long one.

All three comparisons are needed. Checking only `a + b > c` passes 1, 2, 10 if you happen to pass the sides in a different order.

</details>
