---
title: "Bits that flip: XOR and parity — Practice"
practice_for: bits-that-flip
year: "2026-2027"
version: 2026.09.25.1
---

# Bits that flip: XOR and parity — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything.

Your toolkit is loaded on this page, so `parity_bit`, `to_binary`,
`to_hex`, `truth_table` and `same_rule` are all ready to use.

## Warm-up

Use this cell for any of the warm-up problems. Type a line, and run it.

```python exec
id: bits-practice-scratch-1
print(1 ^ 1 ^ 1)
```

**1. Predict.** In a game, the pause button toggles: `paused = paused ^ 1`.
The game starts with `paused = 0`, and you press the button three times. Is
the game paused at the end?

<details class="dl-answer"><summary>answer</summary>

Yes. `paused` ends at 1.

The value goes 0, then 1, then 0, then 1. That is the same as
`0 ^ 1 ^ 1 ^ 1`, which is 1. An odd number of presses leaves it paused.

</details>

**2. Predict.** What is `5 ^ 5`? What is `5 ^ 0`?

<details class="dl-answer"><summary>answer</summary>

`5 ^ 5` is 0, and `5 ^ 0` is 5.

In binary, 5 is `101`. XOR with itself compares each bit with the same
bit, so every column is "the same" and gives 0. XOR with 0 is a mask with
no 1s in it, so nothing flips.

</details>

**3. Make.** A seven-segment display can keep which segments are lit as
seven bits, a to g from the left. The digit 1 lights
b and c, so it is `0b0110000`. The digit 2 lights a, b, d, e and g, so it
is `0b1101101`. When the display counts from 1 to 2, which segments
switch? Guess first, then find out with one XOR.

<details class="dl-answer"><summary>answer</summary>

XOR gives a 1 wherever the two patterns differ, and those are the
segments that switch.

```python
change = 0b0110000 ^ 0b1101101
print(format(change, "07b"))    # 1011101
```

The 1s are in the places of a, c, d, e and g. Five segments switch, and
only b stays as it was. So `change` is also a mask: XOR the pattern for 1
with it, and you get the pattern for 2.

</details>

**4. Explain.** Say in your own words why `bit ^ 1` always flips a bit,
whatever the bit is.

<details class="dl-answer"><summary>answer</summary>

XOR gives 1 when its two inputs are different. If `bit` is 0, then 0 and 1
are different, so the answer is 1. If `bit` is 1, then 1 and 1 are the
same, so the answer is 0. Either way, the result is the other value.

</details>

## Core

```python exec
id: bits-practice-scratch-2
settings = 0b1010
print(format(settings, "04b"))
```

**5. Make.** A music app keeps four settings as four bits of one number.
From the left they are shuffle (worth 8), repeat (4), lyrics (2) and dark
mode (1). Right now `settings = 0b1010`: shuffle and lyrics are on. Find
one mask that turns shuffle off and dark mode on, with one XOR, and leaves
the other two alone.

<details class="dl-answer"><summary>answer</summary>

The mask needs a 1 in the columns that should flip, shuffle and dark mode,
and a 0 in the others. That is `0b1001`.

```python
settings = 0b1010
settings = settings ^ 0b1001
print(format(settings, "04b"))    # 0011
```

Now lyrics and dark mode are on. Shuffle is off, and repeat did not
change.

</details>

**6. Predict.** What does `format(0b1010 ^ 0b1111, "04b")` print?

<details class="dl-answer"><summary>answer</summary>

`0101`.

A mask of all 1s flips every bit. So `1010` becomes `0101`.

</details>

**7. Fix.** Schlomi, who is learning Python too, wrote her own parity
function, to be sure she understood it. It passes the first test, but not
the second. Find the one mistake, and fix it.

```python exec
id: bits-practice-fix-parity
def parity_draft(bits):
    """Return the bit that makes the number of 1s even."""
    parity = 0
    for bit in bits:
        parity = int(bit)
    return parity

print(parity_draft("1011"))    # should be 1
print(parity_draft("1110"))    # should be 1
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow `parity` through the loop for `"1110"`, one character at a time.
2. What is `parity` after the last character?
3. Does the old value of `parity` ever get used?

**Think about:** which bit does `parity_draft` really give back?

**Try this next:** find a string where `parity_draft` gives the right
answer by luck, and one where it does not.

</details>

<details class="dl-answer"><summary>answer</summary>

The line `parity = int(bit)` throws the old value away each time, so the
function gives back the last bit and nothing else.

- `"1011"` has three 1s, so the answer is 1. Its last bit is 1, so the
  first test passes by luck.
- `"1110"` also has three 1s, so the answer is 1. But its last bit is 0.

The line must XOR the old value with the new bit:

```python
def parity_draft(bits):
    parity = 0
    for bit in bits:
        parity = parity ^ int(bit)
    return parity

print(parity_draft("1110"))    # 1
```

</details>

**8. Fix.** This function is meant to flip every bit of a colour, the way
`#FF8800` became `#0077FF` on the tutorial page. It gives the wrong colour.
Find the mistake.

```python exec
id: bits-practice-fix-colour
def flip_colour(colour):
    """Flip every bit of a #RRGGBB colour, given as a number."""
    return colour ^ 0xFFFF

print(format(flip_colour(0xFF8800), "06X"))    # should be 0077FF
```

<details class="dl-answer"><summary>answer</summary>

The mask `0xFFFF` has only four hex digits, which is 16 bits. A colour has
24 bits, six hex digits. So the mask flips green and blue, and leaves red
alone. The result is `FF77FF`, a pink.

The mask needs six Fs:

```python
def flip_colour(colour):
    return colour ^ 0xFFFFFF

print(format(flip_colour(0xFF8800), "06X"))    # 0077FF
```

`format(n, "06X")` writes the number in hex with at least six digits,
which keeps the zeros at the front that `to_hex` would leave out.

</details>

**9. Another way.** Find the parity bit of 14 without using XOR. Strings
have a method `.count()`: `"00001110".count("1")` counts the 1s. And `% 2`,
from [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
gives the remainder after dividing by 2.

<details class="dl-answer"><summary>answer</summary>

```python
ones = to_binary(14).count("1")
print(ones)        # 3
print(ones % 2)    # 1
print(parity_bit(to_binary(14)))    # 1, the same
```

An odd count leaves a remainder of 1, and an even count leaves 0. That is
the parity bit. Two routes, one answer.

</details>

**10. Explain.** A fitness watch sends your step count to your phone, one
byte at a time, each with a parity bit. The phone finds that one byte does
not pass the check. Can the phone tell which bit flipped? What can it do
instead?

<details class="dl-answer"><summary>answer</summary>

No. The parity bit only says that the count of 1s is now odd. Any one of
the nine bits flipping would make the same change, so the check cannot
say which one it was.

The phone can ask the watch to send that byte again. Cleverer codes, with
several check bits, can say which bit flipped and put it right. One bit
is enough to notice a mistake, but not enough to find it.

</details>

**11. Another way.** In ordinary counting, $1 + 1 = 2$. Show that
`(a + b) % 2` gives the same answer as `a ^ b` for every pair of bits. In
which space is $1 + 1 = 0$ a right answer?

```python exec
id: bits-practice-add-mod-2
# Compare (a + b) % 2 with a ^ b for every pair of bits
```

<details class="dl-answer"><summary>answer</summary>

```python
for a in [0, 1]:
    for b in [0, 1]:
        print(a, b, (a + b) % 2, a ^ b)
```

The last two columns match on all four rows. So XOR is addition, in a space
where we keep only the remainder after dividing by 2. In that space there
are only two numbers, 0 and 1, and $1 + 1 = 0$ is correct. It is like a
clock with only two hours: go forward two, and you are back where you
started. The answer $1 + 1 = 0$ is wrong in ℕ, and right in the space of
bits.

</details>

## Stretch

```python exec
id: bits-practice-scratch-3
# Use this cell for the stretch problems
```

**12. Make.** A scoreboard at a GAA match sends each score as a row of
bits, with the parity bit already added at the end. Write
`looks_right(received)`, which gives `True` when the whole row, parity bit
included, has an even number of 1s. Test it on `"000011101"` (14 with its
parity bit), and on `"000010101"` (one bit flipped).

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The sender chose the parity bit to make the count of 1s even.
2. So if nothing flipped, the whole row has an even count.
3. `parity_bit` of a row with an even count is 0.

**Think about:** what should `parity_bit` of the whole received row be?

**Try this next:** what does `looks_right` say about `"000011100"`, where
only the parity bit flipped?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def looks_right(received):
    """True when the row, parity bit included, has an even number of 1s."""
    return parity_bit(received) == 0

print(looks_right("000011101"))    # True
print(looks_right("000010101"))    # False
```

A row that arrived safely has an even count of 1s, so its own parity bit
is 0. We do not need to split off the parity bit at all. This is a
function that uses another function's promise to keep its own.

</details>

**13. Predict.** Two players' scores are kept in `score_a` and `score_b`.
This cell swaps them without a third name, using XOR three times. Follow
it by hand in binary. What does it print?

```python
score_a = 12     # 1100
score_b = 10     # 1010
score_a = score_a ^ score_b
score_b = score_a ^ score_b
score_a = score_a ^ score_b
print(score_a, score_b)
```

<details class="dl-answer"><summary>answer</summary>

It prints `10 12`. The scores have swapped.

- Line 3: `score_a` becomes `1100 ^ 1010`, which is `0110`.
- Line 4: `score_b` becomes `0110 ^ 1010`, which is `1100`, the old
  `score_a`. XOR with 10 twice gave back 12.
- Line 5: `score_a` becomes `0110 ^ 1100`, which is `1010`, the old
  `score_b`. XOR with 12 twice gave back 10.

It works because XOR undoes itself. The order of the three lines is the
whole trick: swap any two, and it breaks. In Python you would normally
write `score_a, score_b = score_b, score_a`, which says what it does.

</details>

**14. Make.** A phone has a four-digit PIN, 2468. You want to write
down a hint that is not the PIN. Write `lock(code, key)`, which gives
`code ^ key`, and use it with the key 1357. Then show that locking the
result again with the same key gives back 2468.

<details class="dl-answer"><summary>answer</summary>

```python
def lock(code, key):
    """XOR a code with a key. Doing it twice with the same key undoes it."""
    return code ^ key

hint = lock(2468, 1357)
print(hint)                # 3305
print(lock(hint, 1357))    # 2468
```

The same function locks and unlocks, because $c \oplus k \oplus k = c$.
Someone who finds 3305 does not know the code, unless they also know the
key. This is a toy: it is not safe for anything that matters. The idea
behind it is used in real encryption, with much longer keys.

</details>

**15. Explain.** Schlomo, who is learning Python too, wants the hint to
be safer. His idea: lock the PIN twice, first with the key 1357 and then
with a second key, 4000. Does two keys make it safer? Try it, and
explain what you see.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work out `lock(lock(2468, 1357), 4000)`.
2. Now work out `1357 ^ 4000`, and lock 2468 once with that.
3. Compare the two answers.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(lock(lock(2468, 1357), 4000))    # 841
print(1357 ^ 4000)                     # 2797
print(lock(2468, 2797))                # 841
```

Locking twice gives 841, and so does locking once with the key 2797.
XOR lets us move the brackets:
$(c \oplus k_1) \oplus k_2 = c \oplus (k_1 \oplus k_2)$. So Schlomo's
two keys behave exactly like one key, and a thief who finds that one key
has undone both.

It was a reasonable idea: doing something twice often does make a lock
stronger. With XOR, the second lock joins the first. This is one good
answer; yours might also say what *would* help, such as a longer key.

</details>

**16. Make.** On [Untangling a condition](tutorial:untangling-a-condition)
we had only `not`, `and` and `or`. Write `xor_from_and_or(a, b)` using
only those three words, and check with `same_rule` that it is the same rule
as `a ^ b`.

<details class="dl-answer"><summary>answer</summary>

XOR means "at least one, but not both":

```python
def xor_from_and_or(a, b):
    return (a or b) and not (a and b)

def xor(a, b):
    return a ^ b

print(same_rule(xor_from_and_or, xor, 2))    # True
```

With De Morgan's first law, `not (a and b)` is `not a or not b`, so you
could also write `(a or b) and (not a or not b)`. That is the same rule a
third way.

</details>

**17. Explain.** The weather buoy sends 16 bytes of readings. It could add
one parity bit to each byte (16 extra bits), or one parity bit for all 128
bits together (1 extra bit). What does each choice catch? When would you
choose each?

<details class="dl-answer"><summary>answer</summary>

One bit for all 128 catches any one flip in the whole message, and misses
any two. It costs very little.

One bit per byte catches one flip in each byte, so up to 16 flips can be
caught, as long as no byte has two. It also says which byte went wrong,
so only that byte needs to be sent again. It costs 16 bits.

When the radio is quiet and flips are rare, one bit for the whole message
is enough. When the radio is noisy, and two flips in 128 bits are likely,
a bit per byte is worth the extra cost.

</details>

## Where to read more

Stand-up Maths (2020). *The almost impossible chessboard puzzle.*
<https://www.youtube.com/watch?v=as7Gkm7Y7h4>. A coin on every square of a
chessboard, a key hidden under one square, and one coin flip to pass a
message. The answer is built from parity. Think about it for a while
before you watch. About thirty-two minutes.
