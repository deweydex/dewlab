---
title: "Mixed problems: loops, counting and chance"
practice_across:
  - doing-it-again
  - counting-every-outfit
  - orders-and-choices
  - how-likely-is-it
  - chances-that-combine
year: "2026-2027"
version: 2026.09.25.1
---

# Mixed problems: loops, counting and chance

These problems draw on every page of Unit 3, and on Units 1 and 2 as
well. None of them says which page it needs. Finding that is part of
the problem. When you are not sure where to start, the four questions
are always allowed: what is named here, what is promised, what happens
when, and what does this space let us do?

Each problem says what kind it is: **Predict** (say what a cell will
print, then run it), **Make** (build something small), **Fix** (find
why code that looks fine does something else, and change it), **Explain** (answer in words) or **Another way** (reach the
same answer by a second route, or find the space where a "wrong" answer
is right). Answers are in the folds. Each is one answer, not the only
one.

Along the way, the problems build this unit's product: a
password-strength checker. I think it is the most useful thing in the
unit, because you can test passwords like your own. Invent ones like
yours. Never type a real password into a web page. Problems 6, 8, 10 and 15 are its parts, and
each one uses the part before it. If you skip one, copy its answer into
a scratch cell before you continue.

## Your toolkit

Your toolkit from this unit is loaded on this page: `total`, `product`,
`all_pairs`, `factorial`, `permutations`, `combinations`, `simulate` and
`at_least_one`. So are the tools from Units 1 and 2, like `between` and
`truth_table`. Run this cell to check the ones from this unit. If one of
them gives a `NameError`, build it on its page.

```python exec
id: mixed-loops-toolkit-check
print(total([1, 2, 3]), product([1, 2, 3]))
print(len(all_pairs([1, 2], [1, 2, 3])))
print(factorial(4), permutations(4, 2), combinations(4, 2))
print(at_least_one(0.5, 2))
```

It should print `6 6`, then `6`, then `24 12 6`, then `0.75`.

## Warm-up

Use this cell for any warm-up problem. Change it, and run it.

```python exec
id: mixed-loops-scratch-1
print(total(range(1, 11)))
```

**1. Predict.** A game draws a triangle in pixels: 1 pixel in the top
row, 2 in the next, 3 in the next, and so on. The cell above adds up
the pixels in the first 10 rows. What will it print?

<details class="dl-answer"><summary>answer</summary>

`55`.

`range(1, 11)` is the whole numbers from 1 to 10. The 11 is left out.
The triangle has $\sum_{i=1}^{10} i = \frac{10 \times 11}{2} = 55$ pixels.
This is the pairing trick from [Doing it again](tutorial:doing-it-again).
1 and 10 make 11, 2 and 9 make 11, and there are five such pairs.

</details>

**2. Predict.** A phone's lock screen takes a code of 4 digits, each
from 0 to 9. How many different codes are there? Predict, then check
with `product`.

<details class="dl-answer"><summary>answer</summary>

10,000.

```python
print(product([10, 10, 10, 10]))
print(10 ** 4)
```

Each of the 4 places can be any of 10 digits, and each choice goes with
every choice before it. That is the counting principle from
[Counting every outfit](tutorial:counting-every-outfit). Multiply the
number of choices at each step.

</details>

**3. Make.** Some phones do not let a code use the same digit twice. How
many 4-digit codes have four different digits? Write one line that
calculates it with a toolkit function.

<details class="dl-answer"><summary>answer</summary>

```python
print(permutations(10, 4))
```

It prints `5040`. The first digit has 10 choices, the second 9, the
third 8, and the fourth 7: $10 \times 9 \times 8 \times 7 = 5040$. Order
matters, because 1234 and 4321 are different codes, so it is a
permutation, from [Orders and choices](tutorial:orders-and-choices).

So the rule "no repeated digits" takes away almost half the codes. A
rule meant to make a code safer can make it easier to guess.

</details>

**4. Explain.** Why does adding one more character to a password
multiply the number of possible passwords, rather than add to it?

<details class="dl-answer"><summary>answer</summary>

Every password that was possible before can now be followed by any of
the characters. With 26 letters, each old password turns into 26 new
ones. So the count is multiplied by 26 for each new character.

It is the same reason a truth table doubles its rows with each new
input, on [True, false and every case](tutorial:true-false-and-every-case).
Every old row appears once for each value of the new input.

</details>

**5. Another way.** Countries have two-letter codes, like IE for
Ireland and FR for France. How many two-letter codes are possible? The
answer is $26^2$. Reach it another way, by listing every code with
`all_pairs`.

<details class="dl-answer"><summary>answer</summary>

```python
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
codes = all_pairs(letters, letters)
print(len(codes), 26 ** 2)
print(codes[0], codes[-1])
```

It prints `676 676`, then `('A', 'A') ('Z', 'Z')`. `all_pairs` works on
a string as well as a list, because a loop over a string visits each
character in turn. Only about 250 of the 676 codes are used by real
countries, so there is plenty of room.

</details>

## Core: building the checker

A password-strength checker asks one question: if a thief tried every
possible password, how many would there be? The answer depends on two
things: how many characters each place could hold, and how many places
there are.

This cell gives three names the problems use. Run it first.

```python exec
id: mixed-loops-characters
lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
print("a" in lowercase_letters, "A" in lowercase_letters)
```

It prints `True False`. `in` works on a string the way it works on a
list. `"a" in lowercase_letters` is True when the character `"a"` is in
the text. And `for character in password:` visits each character of
`password` in turn.

Use this cell for the core problems.

```python exec
id: mixed-loops-scratch-2
# Your pool_size, count_passwords and strength_bits go here
```

**6. Make.** Write `pool_size(password)`. It returns how many
different characters each place in the password could hold: 26 if the
password uses any lowercase letter, 26 more for any capital letter, 10
more for any digit, and 32 more for any other character, which we call
a symbol. Test it with `assert`:
`pool_size("hello")` is 26, `pool_size("Hello1")` is 62,
`pool_size("Hello1!")` is 94, and `pool_size("1234")` is 10.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with four names, `has_lower`, `has_upper`, `has_digit` and
   `has_symbol`, all `False`.
2. Loop over the characters. For each one, use `if`, `elif` and `else`
   to set the right name to `True`.
3. After the loop, start `size` at 0, and add 26, 26, 10 or 32 for each
   name that is `True`.

**Think about:** why the numbers are added after the loop, not inside it.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def pool_size(password):
    """How many different characters each place in password could hold."""
    has_lower = False
    has_upper = False
    has_digit = False
    has_symbol = False
    for character in password:
        if character in lowercase_letters:
            has_lower = True
        elif character in uppercase_letters:
            has_upper = True
        elif character in digits:
            has_digit = True
        else:
            has_symbol = True

    size = 0
    if has_lower:
        size = size + 26
    if has_upper:
        size = size + 26
    if has_digit:
        size = size + 10
    if has_symbol:
        size = size + 32
    return size

assert pool_size("hello") == 26
assert pool_size("Hello1") == 62
assert pool_size("Hello1!") == 94
assert pool_size("1234") == 10
print("pool_size keeps its promise.")
```

Inside the loop, `elif` works, because each character is exactly one
kind.
After the loop, the four checks are separate `if` lines, because a
password can use several kinds at once. With `elif` there, only the
first kind found would count.

</details>

**7. Fix.** Schlomi, who is learning Python too, wrote this version. It
gives 52 for `"Hi"`, as it should, but 130 for `"hello"`. Run it,
find why, and change it.

```python exec
id: mixed-loops-fix-pool
def schlomis_pool_size(password):
    """How many different characters each place in password could hold."""
    size = 0
    for character in password:
        if character in lowercase_letters:
            size = size + 26
        elif character in uppercase_letters:
            size = size + 26
        elif character in digits:
            size = size + 10
        else:
            size = size + 32
    return size

print(schlomis_pool_size("Hi"))       # should be 52
print(schlomis_pool_size("hello"))    # should be 26
```

<details class="dl-answer"><summary>answer</summary>

The code adds inside the loop, so it adds once for every character.
`"hello"` has five lowercase letters, so it adds 26 five times, to make
130. `"Hi"` looked fine only because its two characters are of
two different kinds.

The pool should grow once for each kind of character, however many
characters of that kind there are. So the loop should only note which
kinds appear, and the code should add after it, as in the answer to
problem 6. This is about what happens when. The function has the lines
it needs, but one is in the wrong place.

</details>

**8. Make.** Write `count_passwords(password)`: how many passwords
there are of the same length, using the same pool. Test it:
`count_passwords("hello")` should be 11,881,376, and
`count_passwords("1234")` should be 10,000.

<details class="dl-answer"><summary>answer</summary>

Each of the places can hold any character from the pool, so by the
counting principle the count is the pool size multiplied by itself once
for each place. That is a power.

```python
def count_passwords(password):
    """How many passwords have this length and this pool of characters."""
    return pool_size(password) ** len(password)

assert count_passwords("hello") == 11881376
assert count_passwords("1234") == 10000
print("count_passwords keeps its promise.")
```

`len` works on a string, and gives the number of characters. $26^5 =
11{,}881{,}376$.

</details>

**9. Predict.** Which of these has more possible passwords of its kind:
`"Tr0ub4dor&3"` or `"correcthorsebatterystaple"`? Decide first, then
run `count_passwords` on both.

<details class="dl-answer"><summary>answer</summary>

`"correcthorsebatterystaple"`, by a very long way.

```python
print(count_passwords("Tr0ub4dor&3"))
print(count_passwords("correcthorsebatterystaple"))
```

The first uses all four kinds, so its pool is 94, but it has only 11
characters. That gives $94^{11}$, a number with 22 digits. The second
uses only lowercase letters, a pool of 26, but it has 25 characters.
That gives $26^{25}$, a number with 36 digits.

The length is the power, and the pool is only the base. Each extra
place multiplies the count again, so length usually matters more than
variety.

</details>

**10. Another way.** Numbers like $26^{25}$ are too long to compare by
eye. Security people count *bits of strength* instead. The bits are how
many times you would double 1 to reach the count. That is a logarithm,
base 2,
from [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
Find the bits for `"hello"` two ways: as `math.log2` of the count,
and as the length times `math.log2` of the pool. Do they agree? Then
write `strength_bits(password)`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `import math` first.
2. The first way is `math.log2(count_passwords("hello"))`.
3. The second way is `len("hello") * math.log2(pool_size("hello"))`.

**Think about:** $26^5$ is 26 multiplied 5 times. If one 26 is about
4.7 doublings, how many doublings are five of them?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import math

print(math.log2(count_passwords("hello")))
print(len("hello") * math.log2(pool_size("hello")))

def strength_bits(password):
    """How many doublings it takes to reach the count of passwords like this one."""
    return len(password) * math.log2(pool_size(password))

assert round(strength_bits("hello"), 6) == round(math.log2(count_passwords("hello")), 6)
print(round(strength_bits("hello"), 1))
```

Both ways give about 23.5, and they differ only in the last digit or
two, because floats are very close rather than exact. So the
test rounds both first.

They agree because each character multiplies the count by 26, and one
multiplication by 26 is $\log_2 26 \approx 4.7$ doublings. Five
characters make $5 \times 4.7 = 23.5$ doublings. The second way is the
better one for long passwords. It never has to build the huge count.

</details>

**11. Fix.** This function should say how many years a thief needs to
try every password, at a given number of guesses a second. For
`"Tr0ub4dor&3"` at 10 billion guesses a second it gives a number with
16 digits. It should be about 16,000 years. Find why.

```python exec
id: mixed-loops-fix-years
def years_to_try_all(count, guesses_per_second):
    """How many years it takes to try every one of count passwords."""
    seconds = count / guesses_per_second
    return seconds / 60 * 60 * 24 * 365

print(years_to_try_all(94 ** 11, 10000000000))    # the count for "Tr0ub4dor&3"
```

<details class="dl-answer"><summary>answer</summary>

The trouble is the order of operations. Python does `/` and `*` from
left to right, so the line divides by 60, and then multiplies by 60, 24 and 365.
It should divide by all four. Brackets fix it:

```python
def years_to_try_all(count, guesses_per_second):
    """How many years it takes to try every one of count passwords."""
    seconds = count / guesses_per_second
    seconds_in_a_year = 60 * 60 * 24 * 365
    return seconds / seconds_in_a_year

print(round(years_to_try_all(94 ** 11, 10000000000)))
```

Now it prints `16055`. A name for the number of seconds in a year does
the same job as brackets, and makes the line easier to read.

</details>

**12. Explain.** A bike lock has one dial, from 0 to 9, and a thief has
3 tries before an alarm goes off. A careful thief tries 3 different
numbers. A careless thief picks each try at random, and may try the same
number twice. Run the cell. Why does `at_least_one(0.1, 3)` fit one
thief and not the other?

```python exec
id: mixed-loops-bike-lock
import random

def careful_thief():
    code = random.randint(0, 9)
    return code in [0, 1, 2]

def careless_thief():
    code = random.randint(0, 9)
    for attempt in range(3):
        if random.randint(0, 9) == code:
            return True
    return False

print("careful: ", simulate(careful_thief, 100000), 3 / 10)
print("careless:", simulate(careless_thief, 100000), at_least_one(0.1, 3))
```

<details class="dl-answer"><summary>answer</summary>

The careful thief wins about 0.3 of the time, and the careless one about
0.271.

`at_least_one` keeps its promise for independent tries. The
careless thief's tries are independent: each one has the same chance,
0.1, whatever happened before. So $1 - 0.9^3 = 0.271$ fits him.

The careful thief's tries are not independent. After a wrong guess, that
number is ruled out, so the next try has a better chance: 1 in 9, then
1 in 8. The three tries are three different numbers out of ten, which
are mutually exclusive, so the addition rule gives
$\frac{1}{10} + \frac{1}{10} + \frac{1}{10} = 0.3$.

For a 4-digit PIN, the two answers are 0.0003 and about 0.00029997,
almost the same, because a careless thief seldom repeats a guess out of
10,000.

</details>

**13. Make.** A website accepts a password when it is long enough and
it has a digit or a symbol. Write the rule as a function of three
True/False inputs, and print its truth table with `truth_table`. In how
many of the 8 rows is the password accepted?

<details class="dl-answer"><summary>answer</summary>

```python
def accepted(long_enough, has_digit, has_symbol):
    """The website's rule for a new password."""
    return long_enough and (has_digit or has_symbol)

truth_table(accepted, ["long_enough", "has_digit", "has_symbol"])
```

It is accepted in 3 rows: long enough with a digit, long enough with a
symbol, and long enough with both. The brackets matter, as they did on
[True, false and every case](tutorial:true-false-and-every-case).
Without them, Python does `and` first, and a short password with a
symbol would be accepted.

</details>

## Stretch

A scratch cell for the stretch problems.

```python exec
id: mixed-loops-scratch-3
# Try things here
```

**14. Predict.** A 12-character password that uses all four kinds of
character has $94^{12}$ possible passwords. How many characters would a
password of only lowercase letters need, to have more? Guess, then run
the loop.

```python exec
id: mixed-loops-how-long
length = 1
while 26 ** length <= 94 ** 12:
    length = length + 1
print(length)
```

<details class="dl-answer"><summary>answer</summary>

`17`.

The `while` loop adds one character at a time, for as long as the
lowercase count is not yet bigger. With 16 lowercase letters, $26^{16}$
is still less than $94^{12}$. With 17, it is more.

In bits, one lowercase letter is about 4.7 bits, and one character from
all 94 is about 6.55 bits. So 12 mixed characters are about 78.7 bits,
and $78.7 \div 4.7$ is about 16.7, so it needs 17 letters.

</details>

**15. Make.** Now put the checker together. Write
`password_strength(password)`. It returns a message with the bits of
strength, a rating, and how long a thief would need to try every
password at 10 billion guesses a second. Use these ratings:

| Bits | Rating |
|---|---|
| less than 28 | very weak |
| 28 to less than 36 | weak |
| 36 to less than 60 | fair |
| 60 to less than 128 | strong |
| 128 or more | very strong |

Try it on `"hello"`, `"Hello1!"`, `"9Lq#v2!mZx"` and
`"correcthorsebatterystaple"`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Set `bits = strength_bits(password)` first.
2. Choose the rating with `if`, `elif` and `else`, from the weakest up.
   Each `elif` only runs when every check above it was False.
3. Find the seconds: `count_passwords(password) / 10000000000`.
   Then write a small function that turns seconds into a sensible unit:
   seconds, hours, days or years.
4. Join the pieces into one message with `+` and `str()`.

**Think about:** why the checks for the rating go from the weakest up,
and what would happen if they went from the strongest down with `<`.

**Try this next:** add a warning when the password is shorter than 8
characters, whatever its bits.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def describe_time(seconds):
    """A number of seconds, in the largest unit that makes sense."""
    hour = 60 * 60
    day = 24 * hour
    year = 365 * day
    if seconds < hour:
        return str(round(seconds, 1)) + " seconds"
    elif seconds < day:
        return str(round(seconds / hour, 1)) + " hours"
    elif seconds < year:
        return str(round(seconds / day, 1)) + " days"
    else:
        return str(round(seconds / year)) + " years"


def password_strength(password):
    """Rate a password, and say how long trying every password like it takes."""
    bits = strength_bits(password)
    if bits < 28:
        rating = "very weak"
    elif bits < 36:
        rating = "weak"
    elif bits < 60:
        rating = "fair"
    elif bits < 128:
        rating = "strong"
    else:
        rating = "very strong"
    seconds = count_passwords(password) / 10000000000
    return (password + ": " + str(round(bits, 1)) + " bits, " + rating
            + ". Trying every one takes " + describe_time(seconds) + ".")


for password in ["hello", "Hello1!", "9Lq#v2!mZx", "correcthorsebatterystaple"]:
    print(password_strength(password))
```

It prints:

```text
hello: 23.5 bits, very weak. Trying every one takes 0.0 seconds.
Hello1!: 45.9 bits, fair. Trying every one takes 1.8 hours.
9Lq#v2!mZx: 65.5 bits, strong. Trying every one takes 171 years.
correcthorsebatterystaple: 117.5 bits, strong. Trying every one takes 750804889675188992 years.
```

`"hello"` takes about a thousandth of a second, which rounds to 0.0.
The last number is so big that "years" stops meaning much. It is about
50 million times the age of the universe. Its last few digits are float
rounding, the same closeness you met with `0.1 + 0.2`.

Every piece of this unit is in here. Loops walk through the characters,
the counting principle gives the count, a power and a logarithm turn it
into bits, and `if`, `elif` and `else` from Unit 2 choose the rating.

</details>

**16. Predict.** A company gives each member of staff a random 4-digit
PIN for the front door, from all 10,000. How many staff must there be
before the chance that two of them share a PIN is more than a half?
Guess first: 5,000? 1,000? 100? Then write a `while` loop to find it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This is the birthday problem, with 10,000 "days".
2. For a given number of staff, the chance that all PINs are different
   is the product of $\frac{10000 - k}{10000}$ for $k$ from 0 to one
   less than the number of staff.
3. Start at 1 and add one member of staff at a time, while the chance of
   a shared PIN is 0.5 or less.

**Think about:** how many pairs of staff there are when you find the
answer.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def chance_of_shared_pin(staff):
    """The chance that two of this many staff have the same PIN."""
    chances = []
    for already in range(staff):
        chances.append((10000 - already) / 10000)
    return 1 - product(chances)

staff = 1
while chance_of_shared_pin(staff) <= 0.5:
    staff = staff + 1

print(staff, chance_of_shared_pin(staff))
print(combinations(staff, 2), "pairs")
```

It prints `119`, a chance of about 0.506, and `7021 pairs`. With only 119
people and 10,000 possible PINs, two of them probably match.
Each pair has a tiny chance of matching, but 119 people make over 7,000
pairs.

So a PIN should never be used as the only thing that tells
people apart, and why computers that give files short codes need those
codes to be very long.

</details>

**17. Explain.** Schlomo, who is learning Python too, runs the checker on
`"Password1!"`. It gives 65.5 bits, the same as `"9Lq#v2!mZx"`, and
rates it strong, so Schlomo is pleased. But it is one of the first
passwords any thief tries. What does the checker assume that is not true
here? Which of the four questions does that belong to?

<details class="dl-answer"><summary>answer</summary>

The checker assumes that every character was picked at random from the
pool, each one independent of the others. Its count, $94^{10}$, is the
count for that space: ten random characters.

People do not pick passwords that way. `"Password1!"` is a common word
with a capital at the front, a digit and a symbol at the end. A thief
does not try every string of 10 characters. They try lists of common
passwords first, and this one is near the top of them. In that space,
it has only a handful of bits.

The same thinking changes `"correcthorsebatterystaple"`. If a thief
knows it is four words from a list of 2,000 common words, the count is
$2000^4$, which is about 43.9 bits, a long way below the checker's
117.5. That is still better than `"Hello1!"`, and far easier to remember
than `"9Lq#v2!mZx"`.

This belongs to the fourth question: what does this space let us do,
and what does it assume? The maths in the checker is right. It answers
the question for a space of random characters. A real password's
strength depends on the space the thief believes it came from.

</details>
