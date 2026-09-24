---
title: "Numbers a computer can hold — Practice"
practice_for: numbers-a-computer-can-hold
year: "2026-2027"
version: 2026.09.24.1
---

# Numbers a computer can hold — Practice

Each problem says what kind it is: **Predict**, **Make**, **Fix**,
**Explain** or **Another way**. With numbers, it is tempting to run the
cell first and guess afterwards. Try it the other way round: write your
guess down, then run. The surprises are where the learning is.

## Warm-up

**1. Predict.** Seventeen people turn up for five-a-side football. What
does each line show, and what does each answer mean for the game?

```python exec
id: numbers-practice-predict-1
print(17 // 5)
print(17 % 5)
print(17 / 5)
```

<details class="dl-answer"><summary>answer</summary>

```text
3
2
3.4
```

`17 // 5` is 3: there are enough people for 3 full teams. `17 % 5` is 2:
two people are left over, and could be substitutes. `17 / 5` is 3.4,
which is a true answer in the rational numbers, but nobody can pick 0.4
of a team. For this question, `//` and `%` live in the right space, and
`/` does not.

</details>

**2. Explain.** What is the smallest family of numbers, $\mathbb{N}$,
$\mathbb{Z}$, $\mathbb{Q}$ or $\mathbb{R}$, that each of these belongs to?

- (a) 12 people on a bus
- (b) a temperature of −4 °C in Mullingar in January
- (c) three quarters of a pizza, 0.75
- (d) $\pi$, the number that turns a circle's width into its distance round

<details class="dl-answer"><summary>answer</summary>

(a) $\mathbb{N}$, a counting number.

(b) $\mathbb{Z}$, because it is a whole number below zero.

(c) $\mathbb{Q}$, because it is the fraction $\frac{3}{4}$.

(d) $\mathbb{R}$, because $\pi$ is not a fraction of two whole numbers.

Remember that the families sit inside each other. So 12 is also in
$\mathbb{Z}$, $\mathbb{Q}$ and $\mathbb{R}$. The question asked for the
smallest.

</details>

**3. Predict.** What does each line show?

```python exec
id: numbers-practice-predict-2
print(2 + 3 * 4)
print((2 + 3) * 4)
```

<details class="dl-answer"><summary>answer</summary>

`14`, then `20`.

In the first line, the multiply happens before the add: $3 \times 4 =
12$, then $2 + 12 = 14$. In the second, the brackets go first:
$2 + 3 = 5$, then $5 \times 4 = 20$.

</details>

**4. Make.** Eggs are packed in boxes of 6. A farm has 50 eggs. Write
two lines that show how many full boxes it can pack, and how many eggs
are left over.

```python exec
id: numbers-practice-make-1
# Your two lines here
```

<details class="dl-answer"><summary>answer</summary>

```python
print(50 // 6)
print(50 % 6)
```

8 full boxes, with 2 eggs left over. Check: $8 \times 6 + 2 = 50$. That
check always works: the whole part times the divisor, plus the
remainder, gives back the number you started with.

</details>

## Core

**5. Predict.** What does each line show? Look carefully at the third.

```python exec
id: numbers-practice-predict-3
print(type(10 / 5))
print(10 // 4)
print(10.0 // 4)
```

<details class="dl-answer"><summary>answer</summary>

```text
<class 'float'>
2
2.0
```

`/` always gives a float, even when it comes out exactly, so `10 / 5` is
`2.0`, a float. `10 // 4` keeps the whole part, 2, and since both
numbers were ints, the answer is an int. In the third line, `10.0` is a
float, so the answer is a float too: `2.0`. Floor division keeps the
kind of number it was given.

</details>

**6. Fix.** A basketball player scored 12, 15 and 18 points in three
games. This cell should show her average, which is 15. It shows 33.0
instead. Find the mistake and fix it.

```python exec
id: numbers-practice-fix-1
print(12 + 15 + 18 / 3)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which happens first in this line, the adding or the dividing?
2. So which number is being divided by 3?
3. How can you make the adding happen first?

**Think about:** how would you write this average on paper, with a line
for the division?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print((12 + 15 + 18) / 3)
```

Division comes before addition, so the original line worked out
$18 \div 3 = 6$ first, then $12 + 15 + 6 = 33$. Brackets make the adding
happen first: $45 \div 3 = 15.0$.

On paper, we would write $\frac{12 + 15 + 18}{3}$, and the long line
does the job of the brackets. Python has no long line, so we write the
brackets ourselves.

</details>

**7. Fix.** A bus journey takes 135 minutes. This cell should show it in
hours and minutes: 2 hours and 15 minutes. Run it and see what it shows
instead, then fix it.

```python exec
id: numbers-practice-fix-2
minutes = 135
print(minutes / 60, "hours and", minutes % 60, "minutes")
```

<details class="dl-answer"><summary>answer</summary>

It shows `2.25 hours and 15 minutes`. The 2.25 hours already includes
the 15 minutes (a quarter of an hour), so the time is counted twice.

```python
minutes = 135
print(minutes // 60, "hours and", minutes % 60, "minutes")
```

This shows `2 hours and 15 minutes`. `//` gives the whole hours, and `%`
gives the minutes left over. Both answers come from the same division,
seen two ways.

</details>

**8. Another way.** A child says: "You can't take 5 away from 3." Find
a space where they are right, and a space where they are wrong. Give a
real situation for each.

<details class="dl-answer"><summary>answer</summary>

They are right in $\mathbb{N}$. If you have 3 apples, you cannot give
away 5. There is no such thing as −2 apples in a bowl.

They are wrong in $\mathbb{Z}$. If it is 3 °C and the temperature drops
by 5 degrees, it is −2 °C. And if you have €3 in your account and spend
€5, your balance is −€2 (if the bank allows it).

The child has not made a mistake. They have described the natural
numbers correctly. Some situations need a bigger space.

</details>

**9. Make.** A message is passed on in rounds. In the first round, one
person tells 2 people. In each round after that, everyone who has heard
tells 2 new people, so the number who heard it in that round doubles.
In the 2022 census, Ireland's population was 5,149,139. Use `math.log2`
to find about how many rounds of doubling it takes for one round to
reach that many people.

```python exec
id: numbers-practice-make-2
import math

# Your line here
```

<details class="dl-answer"><summary>answer</summary>

```python
import math

print(math.log2(5149139))
```

It shows about 22.3. So 22 doublings is not quite enough, and 23 is more
than enough. We can check with powers: $2^{22} = 4{,}194{,}304$, which
is less than the population, and $2^{23} = 8{,}388{,}608$, which is more.

A logarithm answers "how many times do I multiply by 2?". A very big
number needs surprisingly few doublings, and that is why news can
spread so fast.

</details>

**10. Explain.** Predict what this cell shows, then run it. Why is the
answer what it is, and why might it matter in a program that handles
money?

```python exec
id: numbers-practice-explain-1
print(0.1 + 0.2 == 0.3)
```

<details class="dl-answer"><summary>answer</summary>

It shows `False`.

`0.1 + 0.2` is `0.30000000000000004` as a float. Python cannot store 0.1
or 0.2 exactly, only very close to them, and the tiny differences show
up in the sum. `==` asks whether two values are exactly equal, and these
two are not, quite.

For money, this means a program should not test an answer with `==` on
floats that have not been rounded. That is one reason `split_bill` rounds
to the cent before it returns. Try `print(round(0.1 + 0.2, 2) == 0.3)`:
it shows `True`. A later page in this unit explains why 0.1 cannot be
stored exactly.

</details>

The next two problems use `split_bill`. If you wrote your own on the
tutorial page, it should do the same as this one. Run this cell first,
so that the page has a `split_bill` to use.

```python exec
id: numbers-practice-tools
def split_bill(total, people, tip_percent=0):
    """Return each person's share of a bill, in euro, rounded to the cent."""
    with_tip = total * (1 + tip_percent / 100)
    share = with_tip / people
    return round(share, 2)
```

**11. Make.** Five friends share a taxi that costs €37.50, and they want
to add a 10% tip. Use `split_bill` to find each person's share. Then
find it with no tip.

```python exec
id: numbers-practice-make-3
# Your lines here
```

<details class="dl-answer"><summary>answer</summary>

```python
print(split_bill(37.50, 5, 10))
print(split_bill(37.50, 5))
```

With the tip, each pays €8.25. With no tip, each pays €7.50, which
Python shows as `7.5`. In the second call, we did not give a tip, so
`tip_percent` took its default value, 0.

Check the first one by hand: 10% of €37.50 is €3.75, so the total is
€41.25, and $41.25 \div 5 = 8.25$.

</details>

**12. Make.** On a piano, one A is 110 Hz and a higher A is 1760 Hz.
Each octave up doubles the frequency. Use `math.log2` to find how many
octaves apart they are.

```python exec
id: numbers-practice-make-4
import math

# Your line here
```

<details class="dl-answer"><summary>answer</summary>

```python
import math

print(math.log2(1760 / 110))
```

It shows `4.0`: they are 4 octaves apart. First, $1760 \div 110 = 16$,
so the higher note is 16 times the frequency. Then $\log_2 16 = 4$,
because $2^4 = 16$. Check by doubling: 110, 220, 440, 880, 1760. That is
four doublings.

</details>

## Stretch

**13. Another way.** The tutorial found $\log_2 1024$ with
`math.log2`. Find it another way, without any logarithm and without a
computer. Start from 1024 and keep halving.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Halve 1024. Write the answer down.
2. Halve that. Keep going.
3. Stop when you reach 1.
4. Count how many halvings you did.

**Think about:** why does counting halvings down to 1 give the same
answer as counting doublings up from 1?

**Try this next:** how many halvings from 1,000,000 to get below 1? What
does `math.log2(1000000)` say?

</details>

<details class="dl-answer"><summary>answer</summary>

1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1. That is 10 halvings, so
$\log_2 1024 = 10$.

Halving down to 1 undoes doubling up from 1, one step at a time. So the
number of halvings is the number of doublings, which is the logarithm.
The same idea, seen from the other end, is why searching a sorted list
by halving it is so fast. A later unit is built on it.

For the "try this next", `math.log2(1000000)` is about 19.9, so 20
halvings take a million below 1.

</details>

**14. Fix.** Here is a friend's first try at a bill calculator, with its
tests. The tests fail. Run the cell, find the one mistake, and fix it so
that all the tests pass.

```python exec
id: numbers-practice-fix-3
def bill_share(total, people, tip_percent=0):
    """Return each person's share of a bill, in euro, rounded to the cent."""
    with_tip = total * tip_percent / 100
    share = with_tip / people
    return round(share, 2)

assert bill_share(84, 4) == 21.0
assert bill_share(84, 4, 10) == 23.1
print("bill_share keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which test fails first? The error message names its line.
2. Work out `bill_share(84, 4)` by hand, line by line. With no tip,
   `tip_percent` is 0. What is `with_tip`?
3. Is `with_tip` the bill with the tip added, or the tip on its own?

**Think about:** what should `with_tip` be when there is no tip at all?

</details>

<details class="dl-answer"><summary>answer</summary>

The first test fails. With no tip, `with_tip` is $84 \times 0 \div 100 =
0$, so each person pays €0. The line works out the tip on its own, and
forgets to add the bill.

```python
    with_tip = total * (1 + tip_percent / 100)
```

`total + total * tip_percent / 100` works too. It is the same amount,
written another way. This is a realistic mistake, and it is why a
function should be tested with more than one case: a test with a tip of
0 catches it at once.

</details>

**15. Predict.** You know `7 // 2` is 3. What do you think `-7 // 2` is?
Make a guess, then run the cell.

```python exec
id: numbers-practice-predict-4
print(-7 // 2)
print(-7 % 2)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work out $-7 \div 2$ exactly. You get −3.5.
2. Draw a number line, and mark −3.5 on it.
3. `//` is floor division. Floor means "the next whole number down".
   Which whole number comes next below −3.5 on your line?

**Think about:** is "down" the same as "towards zero" for a negative
number?

</details>

<details class="dl-answer"><summary>answer</summary>

`-4`, then `1`.

$-7 \div 2 = -3.5$. Floor division rounds down, to the whole number
below, and on the number line the whole number below −3.5 is −4, not
−3. For positive numbers, rounding down and cutting off the decimal
part give the same answer. For negative numbers they do not.

The remainder follows from that. Python keeps the rule from problem 4:
$-4 \times 2 + 1 = -7$. So the remainder is 1.

Most people guess −3. It is a very reasonable guess, and it is right in
some other programming languages, which round towards zero. Python
chose "down" instead. Same move, a different space.

</details>

**16. Make.** A recipe for 4 people uses 300 g of flour. Write a
function `scale(amount, from_people, to_people)` that returns how much
you need for a different number of people. Give it a docstring, and
test it with at least two `assert` lines.

```python exec
id: numbers-practice-make-5
def scale(amount, from_people, to_people):
    """Your promise here."""
    ...
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. How much flour is that for one person?
2. Then how much for `to_people` people?
3. Write that as one expression after `return`.
4. Test it with numbers you can check in your head: 300 g for 4 should
   be 150 g for 2.

**Think about:** does your function work for any ingredient, or only
flour?

**Try this next:** what does your function give for 250 g, from 4
people to 3? Is that a sensible amount to weigh?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def scale(amount, from_people, to_people):
    """Return the amount of an ingredient for to_people, from a recipe
    that serves from_people."""
    return amount / from_people * to_people

assert scale(300, 4, 2) == 150
assert scale(300, 4, 6) == 450
print("scale keeps its promise.")
```

First we divide by 4 to get the amount for one person, 75 g. Then we
multiply by the new number of people. For 6 people that is 450 g.

It works for any ingredient, because the promise is about amounts, not
flour. For the "try this next", `scale(250, 4, 3)` gives 187.5 g. That
is fine on a kitchen scale, and it is a float, because `/` always gives
one.

</details>
