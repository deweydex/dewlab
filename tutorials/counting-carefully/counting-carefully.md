---
title: "Counting: factorials, permutations and combinations"
year: "2026-2027"
version: 2026.08.23.1
covers:
  factorials-the-foundation:
    covers: [MIT-5.3]
  permutations-order-matters:
    covers: [MIT-5.4]
  combinations-order-does-not-matter:
    covers: [MIT-5.5]
  a-practical-application-password-strength:
    covers: [MIT-5.2]
---

# Counting: factorials, permutations and combinations

How many different ways can 5 people sit around a dinner table? How many
different 6-digit PINs are there? How many ways can you choose 3
toppings from a menu of 12?

These are *counting problems*. Each one asks how many different ways
something can happen. Counting problems appear in many places:

- in probability
- in security: how hard is a password to guess?
- in games: how many different hands of cards are there?
- in computing: how many different inputs can a function get?

On this page we:

- count the ways to put things in order, with factorials
- count the ways to choose some things and put them in order, with
  permutations
- count the ways to choose some things when order does not matter, with
  combinations
- count choices where the same thing can be picked again
- use these tools to see what makes a password strong

## Factorials: the foundation

The factorial of a positive whole number $n$ is what we get when we
multiply together every whole number from $n$ down to 1. We write it
$n!$, and say "n factorial":

$$n! = n \times (n-1) \times (n-2) \times \cdots \times 2 \times 1$$

For example, $5! = 5 \times 4 \times 3 \times 2 \times 1 = 120$.

What does a factorial count? It counts the different orders, or
*arrangements*, of $n$ different objects.

Suppose you have 5 books to put on a shelf. There are 5 choices for the
first place on the shelf. Once that book is placed, there are 4 books
left for the second place. Then there are 3 for the third place, 2 for
the fourth, and 1 for the last. That gives
$5 \times 4 \times 3 \times 2 \times 1 = 120$ different arrangements.

What about $0!$? Mathematicians agree that $0! = 1$. This can look
strange at first. But it fits. There is exactly one way to arrange zero
objects, and that is to do nothing. It also keeps every formula on this
page working when a number in it is 0.

### Your turn

We met the product version of the accumulator pattern in
[Repeating steps with loops](tutorial:repeating-yourself). Here we turn
it into a function.

1. In the first cell, write a function `factorial(n)` that calculates
   $n!$.
2. Give it a docstring.
3. Make sure it gives 1 when $n$ is 0.
4. In the second cell, test it with the four cases listed there.

Here is one way to plan it, in pseudocode:

```
IF n is 0:
    RETURN 1
SET product = 1
FOR each integer i from 1 to n:
    MULTIPLY product by i
RETURN product
```

```python exec
id: your-turn-1
# Your factorial function
```

```python exec
id: your-turn-2
# Test cases
# factorial(0) should be 1
# factorial(1) should be 1
# factorial(5) should be 120
# factorial(10) should be 3628800
```

## Permutations: order matters

A *permutation* is an arrangement of $r$ objects chosen from $n$
different objects. In a permutation, order matters. A then B is
different from B then A.

We write the number of permutations as $P(n, r)$. The formula takes the
arrangements of all $n$ objects, $n!$, and divides out the arrangements
of the $n - r$ objects we did not choose:

$$P(n, r) = \frac{n!}{(n-r)!}$$

Here is an example. Eight runners are in a race. In how many different
ways can they finish 1st, 2nd and 3rd? We choose 3 runners from 8, and
the order matters, so:

$$P(8, 3) = \frac{8!}{5!} = \frac{40320}{120} = 336$$

We can also count this directly. There are 8 choices for 1st place. Then
there are 7 runners left for 2nd place, and then 6 for 3rd place. That
gives $8 \times 7 \times 6 = 336$, the same answer.

### Your turn

1. Write a function `permutations(n, r)` that calculates $P(n, r)$. Use
   your `factorial` function inside it.
2. What should happen if $r > n$? You cannot choose more items than you
   have. Decide what your function should do in that case.
3. Test it with the cases in the second cell.

```python exec
id: your-turn-3
# Your permutations function
```

```python exec
id: your-turn-4
# Test cases
# permutations(8, 3) should be 336
# permutations(5, 5) should be 120 (same as 5!)
# permutations(5, 0) should be 1
# permutations(5, 1) should be 5
```

## Combinations: order does not matter

A *combination* is a choice of $r$ objects from $n$ different objects,
where the order does not matter. {A, B, C} is the same combination as
{C, A, B}.

How do we count combinations? Take one combination of $r$ items. We can
arrange those $r$ items in $r!$ different orders, so the permutation
count lists each combination $r!$ times. To count each combination only
once, we divide the permutation count by $r!$:

$$C(n, r) = \binom{n}{r} = \frac{n!}{r! \cdot (n-r)!}$$

We read $\binom{n}{r}$ as "n choose r".

Let's try a small example first. How many ways can we choose 2 people
from 4 for a team? The formula gives
$C(4, 2) = \frac{4!}{2! \cdot 2!} = \frac{24}{4} = 6$. If the people are
A, B, C and D, the six teams are AB, AC, AD, BC, BD and CD.

Now we try a bigger one. How many different 5-card hands can be dealt from a
deck of 52 cards?

$$C(52, 5) = \frac{52!}{5! \cdot 47!} = 2{,}598{,}960$$

```question
id: permutation-or-combination
type: multiple-choice
answer: 2

Quick check: a raffle draws 3 winning numbers from a barrel, one at a time. Every winner gets the same prize, whatever order their number came out in. Which counts this situation correctly?

- A permutation, because the numbers come out one at a time.
  - Drawing one at a time is how it happens, but the prize does not depend on the order.
- A combination, because the prize does not depend on the order the numbers came out in.
  - Only which numbers win matters, not the order they came out in.
- A count with repeats allowed, because a number could be drawn more than once.
  - Once drawn, a number is out of the barrel, so it cannot come out again.
```

### Your turn

How might you write `combinations(n, r)`? Can you build it from your
`factorial` function, the same way `permutations` was built?

```python exec
id: your-turn-5
# Your combinations function
```

```python exec
id: your-turn-6
# Test cases
# combinations(52, 5) should be 2598960
# combinations(10, 3) should be 120
# combinations(5, 0) should be 1
# combinations(5, 5) should be 1
# combinations(n, r) should equal combinations(n, n-r) for any valid n, r
```

### Applying the counting tools

Here are five questions to answer with your functions. For each one,
ask yourself first: does the order matter? If it does, use a
permutation. If it does not, use a combination.

1. A committee of 4 people is chosen from 12 people. How many different
   committees are possible?
2. How many different 4-letter sequences can we make from the letters A
   to Z, if a letter may be used more than once?
3. A PIN is 4 digits long, and each digit is from 0 to 9. How many
   different PINs are there?
4. A class has 20 students. In how many ways can we choose a president,
   a vice-president and a treasurer?
5. A pizza shop offers 15 toppings. How many different 3-topping pizzas
   can it make?

```python exec
id: applying-the-counting-tools-1
# Work through each question
# For each: state whether it's a permutation or combination, and why

# 1. Committee from 12 people

# 2. Four-letter sequences (careful: this is different from the others)

# 3. Four-digit PINs

# 4. President, VP, treasurer from 20

# 5. Three toppings from 15
```

Did questions 2 and 3 feel different from the others? In those two, the
same letter or digit can appear more than once. We call this
*repetition*. Permutations and combinations, as we have defined them,
never choose the same object twice, so they do not fit here.

For repetition we use the *multiplication principle*. The multiplication
principle says: if there are $k$ choices at each of $r$ steps, the total
number of outcomes is $k^r$. For 4-letter sequences from 26 letters,
that is $26^4 = 456{,}976$.

### Your turn

1. Write the multiplication principle as a function,
   `count_with_repetition(choices, positions)`.
2. Use it to check your answers to questions 2 and 3 above.

```python exec
id: your-turn-7
# Your count_with_repetition function
```

```python exec
id: your-turn-8
# Verify questions 2 and 3
```

## A practical application: password strength

Our counting tools can tell us something about password security. An
attacker who tries every possible password has to try a very large
number of them. The more possible passwords there are, the stronger a
password is.

Suppose a password is 8 characters long and uses only lowercase letters.
There are 26 choices for each character, so there are $26^8$ possible
passwords.

Now suppose we allow more kinds of character:

- with uppercase letters too, there are 52 choices for each character
- with digits too, there are 62
- with 10 special characters too, such as `!` and `#`, there are 72

How do you think the number of possible passwords changes? Run the cell
to see.

```python exec
id: a-practical-application-password-strength-1
# Password strength analysis
print("Lowercase only, 8 chars:", 26 ** 8)
print("Lower + upper, 8 chars: ", 52 ** 8)
print("All characters, 8 chars:", 72 ** 8)
print()
print("All characters, 10 chars:", 72 ** 10)
print("All characters, 12 chars:", 72 ** 12)
```

The numbers grow very fast when the set of characters gets bigger. They
grow even faster when the password gets longer, because the length is
the power. This is why password advice asks for both: use many kinds of
character, *and* make the password long.

### Your turn

Suppose a computer can test one billion ($10^9$) passwords every second.
How long would it take to try every possible password in each case
above?

1. Write a function `crack_time(num_possibilities, guesses_per_second)`.
2. Make it return the time in a sensible unit: seconds, minutes, hours,
   days or years.
3. Use it on each password case above.

Would you like to go further? Try a 16-character password. Or try an
attacker who can test only a thousand guesses a second, not a billion.
How much does each change make?

```python exec
id: your-turn-9
# Your crack_time function
```

```python exec
id: your-turn-10
# Apply it to the password cases above
```

## Reflection

We have built three counting functions: factorial, permutations and
combinations. We have also built one for the multiplication principle.
Each one is a tested tool that we can use again. In
[Probability: simple, compound and conditional](tutorial:what-are-the-chances),
we use them to calculate probabilities.

The most important skill is to choose the right tool. Here is a summary:

| The question | The tool | The count |
|---|---|---|
| Does the order matter, with no repeats? | Permutation | $P(n, r) = \frac{n!}{(n-r)!}$ |
| Does the order not matter, with no repeats? | Combination | $C(n, r) = \frac{n!}{r! \cdot (n-r)!}$ |
| Can the same thing be chosen again? | Multiplication principle | $k^r$ |

The choice of tool is the hard part. Once you have the right tool, the
calculation follows a fixed set of steps.

Which counting question surprised you most?

## Where to read more

Khan Academy. *The Fundamental Principle of Counting.*
<https://www.youtube.com/watch?v=HDLBCv4yyIs>. It explains the
multiplication principle this page uses for PINs and letter sequences,
starting from first principles.

Mike Pound (Computerphile) (2016). *Password Cracking.*
<https://www.youtube.com/watch?v=7U-RbOKanYs>. It shows what the numbers
this page computes mean in practice, and how fast a real machine can try
that many passwords.

Stand-up Maths (2015). *Matt Explains: Binomial Coefficients.*
<https://www.youtube.com/watch?v=Pcgvv6T_bD8>. Matt Parker explains "n
choose r" on a whiteboard, and shows where the same numbers appear in
Pascal's triangle. The video is twelve minutes long.
