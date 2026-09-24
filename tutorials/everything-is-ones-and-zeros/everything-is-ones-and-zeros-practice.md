---
title: "Everything is ones and zeros — Practice"
practice_for: everything-is-ones-and-zeros
year: "2026-2027"
version: 2026.09.24.1
---

# Everything is ones and zeros — Practice

Each problem says what kind it is: **Predict** (say what a cell will
print, then run it), **Make** (build something small), **Fix** (repair
one mistake), **Explain** (answer in words) or **Another way** (reach the
same answer by a second route). Answers are in the folds. Working by hand
first, then checking in Python, teaches more than either one alone.

## Tools

This cell gives you `to_binary` and `to_hex`, the same two tools as on
the tutorial page, so every problem below works even if your own toolkit
is not loaded. Run it once before you start.

```python exec
id: everything-is-practice-tools
def to_binary(n):
    """Give the whole number n (0 or more) in binary, as a string of 0s and 1s."""
    return format(n, "b")


def to_hex(n):
    """Give the whole number n (0 or more) in hexadecimal, as a string, with capital letters."""
    return format(n, "X")


print(to_binary(13), to_hex(255))
```

## Warm-up

**1. Predict.** What does each line print? Say your answers, then run
them in the tools cell.

```python
print(0b101)
print(0b1000)
print(0xA)
```

<details class="dl-answer"><summary>answer</summary>

`5`, `8` and `10`.

- `101` in binary is one 4, no 2 and one 1: $4 + 0 + 1 = 5$.
- `1000` in binary is one 8 and nothing else: $8$.
- `A` is the hex digit for ten, so `0xA` is $10$.

</details>

**2. Make.** A die has six faces. Write 6 in binary by hand, using the
halving recipe. Then check with `to_binary(6)`.

<details class="dl-answer"><summary>answer</summary>

`110`.

| Number | Half | Remainder |
|---|---|---|
| 6 | 3 | 0 |
| 3 | 1 | 1 |
| 1 | 0 | 1 |

The remainders are 0, 1, 1. Read from the last back to the first, they
give `110`. Checking the other way: $4 + 2 + 0 = 6$.

</details>

**3. Explain.** Why is there never a digit 2 in a binary number?

<details class="dl-answer"><summary>answer</summary>

Binary has only two digits, 0 and 1. A column is full as soon as it
reaches 2, so the 2 is carried into the next column, the same way ten is
carried in our own counting. We write 2 as `10`: one 2 and no 1s. In
base 10 there is no single digit for ten, for the same reason.

</details>

**4. Another way.** A friend writes $10 + 10 = 100$ and says it is
right. In ordinary counting it is wrong. In which space is it right?
Check it in Python.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. On the tutorial page, which kind of number is written only with 0s
   and 1s?
2. In that space, what is `10` worth?
3. Add two of those, and write the answer in the same space.

**Think about:** is `10` a number, or a way of writing one?

**Try this next:** in which space is $7 + 1 = 10$?

</details>

<details class="dl-answer"><summary>answer</summary>

It is right in binary. $10_2$ is 2, and $2 + 2 = 4$, which is $100_2$.

```python
print(0b10 + 0b10)
print(to_binary(0b10 + 0b10))
```

This prints `4`, then `100`. The friend's sum was never foolish. It was a
sum from a different space. (The "try this next" one is base 8, where
the columns are worth 1, 8, 64, and so on.)

</details>

## Core

**5. Make.** An electronic keyboard sends each note as a number from 0
to 127. What is 127 in binary? How many bits does that take, and does
it fit in one byte?

<details class="dl-answer"><summary>answer</summary>

```python
print(to_binary(127))
```

This prints `1111111`, which is seven 1s. So 127 needs 7 bits, and it
fits in one byte with a bit to spare. That is not an accident: $2^7 =
128$, so seven bits give exactly the 128 values from 0 to 127. The
system that sends these notes between music machines, MIDI, was
designed that way in the early 1980s.

</details>

**6. Predict.** What does each of these give? Watch the last two.

```python
print(to_hex(10), to_hex(15), to_hex(16), to_hex(255), to_hex(256))
```

<details class="dl-answer"><summary>answer</summary>

`A F 10 FF 100`.

- 10 and 15 are single hex digits, A and F.
- 16 is one sixteen and no ones, so `10`. It is the hex version of how
  ten is `10` for us.
- 255 is the biggest number two hex digits can hold, `FF`.
- 256 is one step past it, so the columns roll over, like 99 to 100:
  `100`.

</details>

**7. Make.** A green often used for the Irish flag is written
`#169B62`. What are its red, green and blue brightnesses, from 0 to 255?
Work out one of them by hand, then use Python for all three.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Split the colour into three pairs of hex digits: `16`, `9B`, `62`.
2. For a pair like `9B`, the left digit counts sixteens and the right
   digit counts ones. B is 11.
3. In Python, `0x` in front of a pair turns it into a number.

**Think about:** which of the three numbers is the biggest, and does
that match the colour being green?

**Try this next:** what are the three brightnesses of `#FF883E`, an
orange often used on the same flag?

</details>

<details class="dl-answer"><summary>answer</summary>

By hand, `9B` is $9 \times 16 + 11 = 144 + 11 = 155$.

```python
print(0x16, 0x9B, 0x62)
```

This prints `22 155 98`. Red 22, green 155, blue 98. Green is by far the
brightest, with a little blue, which gives a slightly cool green.

</details>

**8. Fix.** This cell should build the colour code for red 255, green
136 and blue 0, which is `#FF8800`. Run it. What comes out, and what is
wrong?

```python exec
id: everything-is-practice-fix-colour
red = 255
green = 136
blue = 0
colour = "#" + to_hex(red) + to_hex(green) + to_hex(blue)
print(colour)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the hex digits in what it printed. A colour needs six.
2. Print `to_hex(0)` on its own. How many digits does it give?
3. Each light needs exactly two digits, even when the first one is 0.

**Think about:** `to_hex` promised a number in hexadecimal. Did it
promise two digits?

**Try this next:** would the same problem happen with a brightness of
10?

</details>

<details class="dl-answer"><summary>answer</summary>

It prints `#FF880`, with only five digits. `to_hex(0)` is `"0"`, one
digit, because `to_hex` writes a number the short way, with no zeros in
front. A colour code needs two digits for each light.

`format` can pad a number to two digits with zeros in front. `"02X"`
means "hexadecimal, at least 2 digits, fill with 0":

```python
red = 255
green = 136
blue = 0
colour = "#" + format(red, "02X") + format(green, "02X") + format(blue, "02X")
print(colour)
```

This prints `#FF8800`. The same trouble happens with any brightness
under 16: 10 would give `A` instead of `0A`.

</details>

**9. Predict.** Add $1011_2 + 0110_2$ by hand, with carries. Then say what
this prints, and run it.

```python
print(to_binary(0b1011 + 0b0110))
```

<details class="dl-answer"><summary>answer</summary>

`10001`.

| | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|
| carry | 1 | 1 | 1 | | |
| | | 1 | 0 | 1 | 1 |
| + | | 0 | 1 | 1 | 0 |
| = | 1 | 0 | 0 | 0 | 1 |

From the right: 1 + 0 is 1. Then 1 + 1 is 10: write 0, carry 1. Then
0 + 1 + 1 is 10: write 0, carry 1. Then 1 + 0 + 1 is 10: write 0, carry
1. The last carry starts a new column. Checking in base 10: $11 + 6 =
17 = 16 + 1$.

</details>

**10. Explain.** In the arcade game Pac-Man, the level number was kept
in one byte. The trouble began at level 256. Why 256, and not 250 or
300?

<details class="dl-answer"><summary>answer</summary>

One byte is eight bits, so it holds $2^8 = 256$ different values: 0 to
255. Level 255 is the last number a byte can hold, `11111111`. Adding
one more would need a ninth bit, `100000000`, and there is no ninth
bit, so the byte goes back to `00000000`. The game had never planned for
that. 250 and 300 are round numbers for us, in base 10. The computer's
round numbers are powers of 2.

</details>

**11. Another way.** On the tutorial page we turned numbers into binary
by halving. Here is a second recipe: take away the biggest power of 2
that fits, and repeat. Use it to write 200 in binary, then check with
`to_binary(200)`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. List the powers of 2: 1, 2, 4, 8, 16, 32, 64, 128, 256.
2. The biggest one that fits in 200 is 128. Take it away. What is left?
3. Repeat with what is left, until you reach 0.
4. Write a 1 under each power you used and a 0 under each one you did not.

**Think about:** why can each power be used at most once?

**Try this next:** use the same recipe for 100, and compare with the
halving recipe's answer on the tutorial page.

</details>

<details class="dl-answer"><summary>answer</summary>

$200 - 128 = 72$, then $72 - 64 = 8$, then $8 - 8 = 0$. So we used 128,
64 and 8.

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |

That is `11001000`, and `to_binary(200)` agrees. Both recipes always
give the same answer. Halving finds the bits from the right; taking away
powers finds them from the left.

</details>

**12. Fix.** A rain gauge records 0.1 mm in the morning and 0.2 mm in
the afternoon. The cell should print `True`, and it prints `False`.
Change one line so it checks the total in a way that works with floats.

```python exec
id: everything-is-practice-fix-rain
morning = 0.1
afternoon = 0.2
total_rain = morning + afternoon
print("Is it 0.3 mm?", total_rain == 0.3)
```

<details class="dl-answer"><summary>answer</summary>

```python
morning = 0.1
afternoon = 0.2
total_rain = morning + afternoon
print("Is it 0.3 mm?", round(total_rain, 2) == 0.3)
```

This prints `Is it 0.3 mm? True`. The total is kept as
`0.30000000000000004`, because 0.1 and 0.2 have no exact binary form.
Rounding to 2 places, which is more precise than a rain gauge reads,
asks "is it close enough?" instead of "is it exactly equal?".

</details>

## Stretch

**13. Another way.** A bus fare is €1.10 and a coffee is €2.20. Run
`print(1.10 + 2.20)`. Then find a way to add them that gives an exact
answer, and print the result as euro and cents, using `//` and `%` from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which kind of number does binary keep exactly: whole numbers, or
   decimals?
2. Write each price in cents instead of euro.
3. How many whole euro are in 330 cents? What is left over?

**Think about:** why would a bank keep your balance in cents?

**Try this next:** add 5 prices of €0.10 in cents, and in euro. Which
one gives exactly 50 cents?

</details>

<details class="dl-answer"><summary>answer</summary>

`print(1.10 + 2.20)` shows `3.3000000000000003`. Counting in whole cents
avoids that:

```python
fare_cents = 110
coffee_cents = 220
total_cents = fare_cents + coffee_cents
print(total_cents // 100, "euro and", total_cents % 100, "cent")
```

This prints `3 euro and 30 cent`. Whole numbers are kept exactly in
binary, so adding cents never drifts. `// 100` gives the whole euro and
`% 100` gives what is left over.

</details>

**14. Make.** A phone's step counter may need to count up to 100,000
steps in a day. How many bits does it need? Use `math.log2`, then check
your answer with powers of 2.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `import math` first, then print `math.log2(100000)`.
2. The answer is not a whole number. Should you round it up or down?
3. Print $2$ to the power of your answer, and $2$ to one less. Which
   one reaches 100,000?

**Think about:** what would happen on the day somebody walks further
than the counter can hold?

**Try this next:** how many bits would a counter for every person in
Ireland need, about 5.5 million?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import math

print(math.log2(100000))
print(2 ** 16, 2 ** 17)
```

This prints `16.609640474436812`, then `65536 131072`. So 16 bits reach
only 65,536, which is too few, and 17 bits reach 131,072, which is
enough. Always round up: a part of a bit is not something a machine can
have.

</details>

**15. Explain.** In 2014 a music video passed 2,147,483,647 views.
YouTube had already moved its view counter to 64 bits, because 32 bits
stop at 2,147,483,647. That number is $2^{31} - 1$. A 32-bit counter
keeps each number in 32 bits, and one of those bits says whether the
number is positive or negative. Why does a 32-bit counter stop there?
Would Python's own whole numbers have had the same problem?

<details class="dl-answer"><summary>answer</summary>

With one bit used for the sign, 31 bits were left for the count. The
biggest number 31 bits can hold is 31 ones, which is $2^{31} - 1 =
2{,}147{,}483{,}647$, in the same way the biggest 8-bit number is
$2^8 - 1 = 255$. One more view needs a bit the 32-bit counter does not
have.

Python's whole numbers would have been fine. Python grows a whole
number to as many bits as it needs, so `print(2 ** 31)` and even
`print(2 ** 100)` work. That is part of the space Python gives us, and
it is not true of every language. A counter with a fixed size needs
room planned ahead, which is why YouTube gave its counter 64 bits before
the video got there.

</details>

**16. Make.** A painter wants a darker version of `#FF8800`, with every
light at half its brightness. Use `//` to halve each one, and build the
new colour code with two digits for each light. Draw both colours to
compare them, the way the tutorial page did.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from the three brightnesses: 255, 136 and 0.
2. Halve each one with `// 2`, so the answers stay whole numbers.
3. Build the code with `format(..., "02X")`, as in problem 8.
4. Put both codes in a list and draw them with `plt.bar`.

**Think about:** why `//` and not `/` here?

**Try this next:** can you make a lighter version, halfway between
`#FF8800` and white, `#FFFFFF`?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

red = 255 // 2
green = 136 // 2
blue = 0 // 2
darker = "#" + format(red, "02X") + format(green, "02X") + format(blue, "02X")
print(darker)

colours = ["#FF8800", darker]
plt.figure(figsize=(4, 2))
plt.bar(colours, [1, 1], color=colours)
plt.yticks([])
```

This prints `#7F4400` and draws the orange beside a brown. The halves
are 127, 68 and 0. We need `//` because a brightness must be a whole
number from 0 to 255: `255 / 2` is `127.5`, and `format` cannot write
that in hexadecimal.

</details>
