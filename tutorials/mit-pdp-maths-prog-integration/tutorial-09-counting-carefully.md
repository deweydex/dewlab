---
title: "Tutorial 9: Counting Carefully"
slug: tutorial-09-counting-carefully
module: mit-pdp-maths-prog-integration
year: "2026-2027"
series: maths-and-programming
order: 9
version: 1
---

# Tutorial 9: Counting Carefully

**Programming Design Principles / Maths for IT**

How many different ways can 5 people sit around a dinner table? How many different 6-digit PINs are possible? How many ways can you choose 3 toppings from a menu of 12?

These are *counting problems*, and they come up everywhere: in probability, in security (how hard is a password to crack?), in game design (how many possible hands of cards?), and in computing (how many possible inputs does a function have?). Today we build the mathematical tools for answering them.

## Factorials: The Foundation

The factorial of a positive integer n, written $n!$, is the product of all positive integers from 1 to n:

$$n! = n \times (n-1) \times (n-2) \times \cdots \times 2 \times 1$$

So $5! = 5 \times 4 \times 3 \times 2 \times 1 = 120$.

What does this count? It counts the number of different orderings (or *arrangements*) of n distinct objects. If you have 5 books, you can arrange them on a shelf in 120 different ways: 5 choices for the first position, then 4 for the second, then 3, then 2, then 1.

By convention, $0! = 1$. This seems strange but is mathematically consistent -- there is exactly one way to arrange zero objects (do nothing).

### Your turn

Write a function `factorial(n)` that computes $n!$. Use the product accumulator pattern we learned in Tutorial 4. Include a docstring and handle the case $n = 0$.

**Pseudocode:**
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

## Permutations: Order Matters

A *permutation* counts the number of ways to choose and arrange $r$ objects from a collection of $n$ distinct objects, where the order of selection matters.

The formula is:

$$P(n, r) = \frac{n!}{(n-r)!}$$

For example: how many ways can 8 runners finish in 1st, 2nd, and 3rd? We are choosing 3 from 8 where order matters:

$$P(8, 3) = \frac{8!}{5!} = \frac{40320}{120} = 336$$

You can also think of it directly: 8 choices for 1st place, then 7 for 2nd, then 6 for 3rd: $8 \times 7 \times 6 = 336$.

### Your turn

Write a function `permutations(n, r)` that computes $P(n, r)$ using your `factorial` function. Think about what should happen if $r > n$ (it should be impossible to choose more items than you have).

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

## Combinations: Order Does Not Matter

A *combination* counts the number of ways to choose $r$ objects from $n$ where the order does *not* matter. Choosing {A, B, C} is the same as choosing {C, A, B}.

Since each combination of $r$ items can be arranged in $r!$ different ways, we divide the permutation count by $r!$:

$$C(n, r) = \binom{n}{r} = \frac{n!}{r! \cdot (n-r)!}$$

The notation $\binom{n}{r}$ is read "n choose r."

For example: how many different 5-card hands can be dealt from a 52-card deck?

$$C(52, 5) = \frac{52!}{5! \cdot 47!} = 2,598,960$$

### Your turn

Write a function `combinations(n, r)` using your `factorial` function.

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

Now let's use these functions to answer some concrete questions. For each one, think about whether order matters (permutation) or not (combination), then use the appropriate function.

1. A committee of 4 needs to be formed from 12 people. How many different committees are possible?
2. How many different 4-letter sequences can be made from the letters A through Z (allowing repetition)?
3. A PIN is 4 digits long (each digit 0-9). How many possible PINs exist?
4. In a class of 20, how many ways can we choose a president, vice-president, and treasurer?
5. A pizza shop offers 15 toppings. How many different 3-topping pizzas can be made?

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

Questions 2 and 3 are interesting because they involve *repetition* -- the same letter or digit can appear more than once. These are not permutations or combinations in the standard sense; they use the *multiplication principle*: if there are $k$ choices at each of $r$ steps, the total is $k^r$. For 4-letter sequences from 26 letters: $26^4 = 456,976$.

### Your turn

Write a function `count_with_repetition(choices, positions)` that implements the multiplication principle. Then verify your answers to questions 2 and 3.

```python exec
id: your-turn-7
# Your count_with_repetition function
```

```python exec
id: your-turn-8
# Verify questions 2 and 3
```

## A Practical Application: Password Strength

Let's use our counting tools to think about password security. A password's strength depends largely on how many possible passwords an attacker would need to try.

If a password uses only lowercase letters (26 choices per character) and is 8 characters long, the number of possible passwords is $26^8$.

If we add uppercase letters (52 choices per character), digits (62), and special characters (let's say 72 total), how does the number of possibilities change?

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

The numbers grow enormously with both the character set size and the length. This is why password guidelines recommend both: use diverse characters *and* make it long.

### Your turn

If a computer can test one billion ($10^9$) passwords per second, how long would it take to try all possibilities for each of the cases above? Write a function `crack_time(num_possibilities, guesses_per_second)` that returns the time in a sensible unit (seconds, minutes, hours, days, or years).

```python exec
id: your-turn-9
# Your crack_time function
```

```python exec
id: your-turn-10
# Apply it to the password cases above
```

## Reflection

We have built three core counting functions -- factorial, permutations, combinations -- and the multiplication principle. Each one is a well-tested, reusable tool that we will use in the next tutorial when we study probability.

The key insight is knowing which tool to use: if order matters, it is a permutation; if order does not matter, it is a combination; if repetition is allowed, it is the multiplication principle. Getting this choice right is the hard part -- the computation itself is mechanical.

What counting question did you find most surprising?
