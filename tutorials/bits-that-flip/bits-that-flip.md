---
title: "Bits that flip: XOR and parity"
year: "2026-2027"
version: 2026.09.24.1
covers:
  xor-on-single-bits:
    covers: [MIT-2.4]
  a-switch-that-flips:
    covers: [MIT-2.4]
  xor-on-whole-numbers:
    covers: [MIT-1.4]
    touches: [MIT-2.4]
  counting-the-1s-parity:
    covers: [MIT-1.4, MIT-2.4]
  catching-a-flipped-bit:
    touches: [MIT-1.4]
---

# Bits that flip: XOR and parity

A weather buoy off the west coast of Ireland sends the sea temperature to
land as a row of bits, over the radio. Radio is noisy. Now and then a
single bit arrives flipped: a 0 that was sent arrives as a 1. The computer
on land has never seen the message before, so how could it tell?

This page is about one extra bit that can catch that mistake.

On this page we:

- meet exclusive or, XOR, on single bits, and Python's `^`
- use XOR to flip a bit, and to flip it back again
- XOR whole numbers, one column of bits at a time, and flip a colour
- add `parity_bit` to the toolkit, and use it to catch a flipped bit

> **The space we're in.** Every value on this page is a bit, 0 or 1, or a
> whole number made of bits, from 0 upwards. Python lets us treat `True`
> and `False` as bits too. One thing usually goes unsaid when people talk
> about checking messages: we assume that at most one bit flips. We will
> see what happens when that is not true.

## Warm-up

```question
id: bits-warm-up-1
type: multiple-choice
correct: 1

From [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros):
what does `to_binary(6)` give?

- `"110"`
- `"0110"`
- `"011"`
- `"6"`
```

```question
id: bits-warm-up-2
type: fill-in-the-blank

From [True, false and every case](tutorial:true-false-and-every-case):
exclusive or, XOR, is True when {exactly one|both|at least one} of its two
inputs is True.
```

## XOR on single bits

On [True, false and every case](tutorial:true-false-and-every-case) we met
the light on the stairs, with a switch at the bottom and a switch at the
top. The light is on when exactly one switch is up. That was XOR, and we
wrote it `bottom_up != top_up`.

Inside a computer, the switches are bits. Let's write *up* as 1 and *down*
as 0. Then the stairs light is a rule on two bits: 1 when the bits are
different, and 0 when they are the same.

Python has an operator for XOR on bits: `^`, the small roof above the 6 on
most keyboards. Before you run this cell, write down the four answers you
expect.

```python exec
id: bits-single-1
print(0 ^ 0)
print(0 ^ 1)
print(1 ^ 0)
print(1 ^ 1)
```

The answer is 1 in the two middle rows, where the bits are different, and
0 where they are the same. With the maths symbol for XOR, the last line
says $1 \oplus 1 = 0$.

The `^` works on `True` and `False` as well. So is `bottom_up ^ top_up`
the same rule as `bottom_up != top_up`? We have a tool for that question:
`same_rule`, from [Untangling a condition](tutorial:untangling-a-condition).
What do you think it will say?

```python exec
id: bits-single-2
def stairs_light(bottom_up, top_up):
    return bottom_up ^ top_up

def different(bottom_up, top_up):
    return bottom_up != top_up

truth_table(stairs_light, ["bottom_up", "top_up"])
print(same_rule(stairs_light, different, 2))
```

For single True/False values, `^` and `!=` are the same rule, checked on
every row. So why have both? Because `!=` only asks whether two values are
different. The `^` can do more: it works on every bit of a whole number at
once, as we will see.

### Your turn

1. In the cell below, write `three_switches(a, b, c)` that returns
   `a ^ b ^ c`. Some big staircases really do have three switches.
2. Print its truth table with `truth_table`.
3. Look at the rows where the result is `True`. How many inputs are `True`
   in each of those rows? What do you notice?

```python exec
id: bits-your-three-switches
# Your three_switches, and its truth table
```

## A switch that flips

Look again at the table for `^`, one row at a time. What does XOR with 1
do to a bit? And XOR with 0?

- `0 ^ 1` is 1, and `1 ^ 1` is 0. XOR with 1 *flips* the bit.
- `0 ^ 0` is 0, and `1 ^ 0` is 1. XOR with 0 leaves the bit as it was.

That makes `^ 1` a *toggle*: an action that switches between two states
each time you do it, like the shuffle button on a music player. Press it
once, and shuffle is on. Press it again, and it is off.

This cell starts with shuffle off and presses the button three times. Is
shuffle on or off at the end? Guess first, then run it to check.

```python exec
id: bits-toggle-1
shuffle = 0
shuffle = shuffle ^ 1
print(shuffle)
shuffle = shuffle ^ 1
print(shuffle)
shuffle = shuffle ^ 1
print(shuffle)
```

After an odd number of presses, shuffle is on. After an even number, it
is back where it started. Each line gives the name `shuffle` a new value,
worked out from the old one, and the order of those lines is the whole
story.

There is a second fact hiding here. XOR with the same bit twice leaves a
bit as it was, whatever that bit is:

$$b \oplus k \oplus k = b$$

In words: XOR with $k$ is a promise that undoes itself. Flip, then flip
again, and you are home.

## XOR on whole numbers

A whole number is a row of bits, so what would `12 ^ 10` mean? Python
lines the two numbers up in binary and does XOR on each column, on its
own. An operation that works on each column of bits separately is called
*bitwise*.

On [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
`format(n, "b")` gave a number in binary. Putting `04` in front of the `b`
asks for at least four digits, with zeros filled in on the left. That
keeps the columns lined up.

| | 8 | 4 | 2 | 1 |
|---|---|---|---|---|
| 12 | 1 | 1 | 0 | 0 |
| 10 | 1 | 0 | 1 | 0 |
| `^` | ? | ? | ? | ? |

Fill in the last row by hand, one column at a time, and turn it into a
number. Then run it to check.

```python exec
id: bits-whole-1
print(format(12, "04b"))
print(format(10, "04b"))
print(format(12 ^ 10, "04b"))
print(12 ^ 10)
```

The answer is `0110`, which is 6. The column worth 8 has two 1s, so it
gives 0. The columns worth 4 and 2 have one 1 each, so they give 1.

Here is the useful way to read it. Think of 10 as a list of instructions,
one per column: 1 means "flip this bit" and 0 means "leave it". A number
used like this is called a *mask*. So `12 ^ 10` means "flip the bits of 12
in the columns worth 8 and 2".

### Flipping a colour

On [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
`#FF8800` was orange: three bytes, for red, green and blue. What happens if
we flip every bit of it? The mask for that is all 1s: `0xFFFFFF`. Each
light that was bright goes dark, and each dark one goes bright.

What colour do you expect? Run it to check.

```python exec
id: bits-colour-1
import matplotlib.pyplot as plt

orange = 0xFF8800
flipped = orange ^ 0xFFFFFF
print(to_hex(flipped))

colours = ["#FF8800", "#0077FF"]
plt.figure(figsize=(4, 2))
plt.bar(colours, [1, 1], color=colours)
plt.yticks([])
```

`to_hex` prints `77FF`, because it leaves out zeros at the front, the same
way `to_binary(6)` gave `"110"`. A colour needs all six digits, so we put
the zeros back: `#0077FF`, a bright blue. Painters call these two colours
*complementary*: they sit opposite each other on the colour wheel. Here,
each light's brightness has become 255 minus what it was.

### Your turn

1. In the cell below, flip `flipped` with the same mask again, and print
   the result with `to_hex`. Which colour is it?
2. Choose a colour of your own, and flip it. Predict the result first.
3. Try the mask `0xFF0000`. Which light does it flip, and which does it
   leave alone?

```python exec
id: bits-your-colour
# Flip flipped back, then flip a colour of your own
```

## Counting the 1s: parity

Back to the weather buoy. It sends a reading of 14 degrees as one byte,
eight bits. Before it sends it, it counts the 1s.

The *parity* of a row of bits says whether it has an even or an odd number
of 1s. A *parity bit* is one extra bit, sent with the message. It is chosen
so that the total number of 1s, message and parity bit together, is even.

Let's find the parity bit for 14 by hand. `format(14, "08b")` is
`00001110`. It has three 1s, which is odd. So the parity bit is 1, to make
four.

Now remember your three switches. `a ^ b ^ c` was 1 exactly when an odd
number of the inputs were 1. That works for any number of bits: XOR them
all together, and you get 1 when the count of 1s is odd, and 0 when it is
even. That is the parity bit.

What do you think `0 ^ 0 ^ 0 ^ 0 ^ 1 ^ 1 ^ 1 ^ 0` gives? Run it to check.

```python exec
id: bits-parity-1
print(0 ^ 0 ^ 0 ^ 0 ^ 1 ^ 1 ^ 1 ^ 0)
```

Typing every bit is slow, so let's write a toolkit function. It takes the
bits as a string of 0s and 1s, like the text `to_binary` gives, and XORs
them together one at a time. `int("1")` turns the text `"1"` into the
number 1, the same way it turned `False` into 0 on
[True, false and every case](tutorial:true-false-and-every-case). The line
`for bit in bits` does something for each character of the string, from
left to right.

This is a toolkit cell with one gap. The line with the XOR in it uses `0`
where each bit should go. Change that `0`, so that the line uses the bit
the loop is looking at.

```python exec
id: bits-toolkit
toolkit: yes
def parity_bit(bits):
    """Return the bit, 0 or 1, that makes the number of 1s even.

    bits is a string of 0s and 1s, like "1011", or a list like [1, 0, 1, 1].
    parity_bit("1011") is 1, because "1011" has three 1s.
    """
    parity = 0
    for bit in bits:
        parity = parity ^ 0    # change this 0 so the line uses each bit
    return parity
```

```python toolkit-reference
for: bits-toolkit
def parity_bit(bits):
    """Return the bit, 0 or 1, that makes the number of 1s even.

    bits is a string of 0s and 1s, like "1011", or a list like [1, 0, 1, 1].
    parity_bit("1011") is 1, because "1011" has three 1s.
    """
    parity = 0
    for bit in bits:
        parity = parity ^ int(bit)
    return parity
```

Then run the tests. Until the gap is filled, the function always gives 0,
so expect the first test to stop with an `AssertionError`. That is the
test telling you the promise is not kept yet.

```python exec
id: bits-toolkit-tests
assert parity_bit("1011") == 1        # three 1s: odd, so add a 1
assert parity_bit("1001") == 0        # two 1s: already even
assert parity_bit("00001110") == 1    # the buoy's 14
assert parity_bit("") == 0            # no 1s at all is an even number
assert parity_bit([1, 1, 1]) == 1     # a list works too
assert parity_bit(to_binary(14)) == 1
print("parity_bit keeps its promise.")
```

```hint
Which test does the error point at? What did you expect `parity_bit` to
give there, and what does it give now?
```

```hint
after: 12 errors
title: some steps
1. The loop gives the name `bit` to each character in turn: `"1"`, then
   `"0"`, and so on.
2. `int(bit)` turns that character into the number 0 or 1.
3. The line should XOR `parity` with that number, in place of the `0`.

**Think about:** why does `parity` start at 0 before the loop?
```

## Catching a flipped bit

Now let's send the reading. The cells in this section use your own
`parity_bit`, so finish it and pass the tests before you go on.

The buoy sends the byte for 14 and its parity bit. On the way, the radio noise flips one bit. We can play the noise
ourselves with a mask: XOR with `0b00000100` flips the bit worth 4.

The computer on land does not know what was sent. It only has what
arrived. So it works out the parity of the byte that arrived, and compares
it with the parity bit that arrived. If they differ, something flipped.

What temperature will land receive? Will the check catch it? Run it to
check.

```python exec
id: bits-catch-1
sent_byte = 14
sent_parity = parity_bit(format(sent_byte, "08b"))

noise = 0b00000100                   # one bit flips on the way
received_byte = sent_byte ^ noise
received_parity = sent_parity        # the parity bit arrives safely

looks_right = parity_bit(format(received_byte, "08b")) == received_parity
print("Received:", received_byte, "degrees")
print("Looks right?", looks_right)
```

The buoy sent 14 degrees, and land received 10. Without the parity bit,
nobody would know. With it, land sees that the count of 1s has changed
from odd to even, and says the message does not look right. It can then
ask the buoy to send it again.

Here is why it works. Flipping any one bit changes the number of 1s by
exactly one, up or down. So an even count becomes odd, and an odd count
becomes even. The parity always changes, and the check always sees it.

Now the limit. The assumption in "the space we're in" was that at most one
bit flips. What if two do? This cell has noise that flips the bits worth 4
and 2. Before you run it, think about the count of 1s. Will the check catch
this one?

```python exec
id: bits-catch-2
noise = 0b00000110                   # two bits flip on the way
received_byte = sent_byte ^ noise

looks_right = parity_bit(format(received_byte, "08b")) == sent_parity
print("Received:", received_byte, "degrees")
print("Looks right?", looks_right)
```

Land receives 8 degrees, and the check says it looks right. Two flips
change the count of 1s twice, and odd, then even, then odd again, puts it
back where it started. So a parity bit promises to catch any one flipped
bit, and it promises nothing about two.

That is still a useful promise. When flips are rare, two in one short
message are much rarer than one. For this reason, parity bits have been
used in computer memory, and on the cables that joined early computers to
modems. The check letter at the end of an Irish PPS number is a
cousin of the same idea: one extra character, worked out from the others,
that catches a mistyped digit.

### Your turn

1. In the cell below, set `noise` to a mask that flips one bit of your
   choice, and check that the message is caught.
2. Now flip three bits. Is it caught? What about four?
3. What if the parity bit is the bit that flips? Set
   `received_parity = sent_parity ^ 1`, keep `received_byte` the same as
   `sent_byte`, and run the check. What happens?
4. Write one sentence: which numbers of flipped bits does a parity bit
   catch?

```python exec
id: bits-your-noise
# Your own noise, and the check from the cell above
```

```hint
To flip three bits, the mask needs three 1s in it, for example
`0b00000111`. How many 1s did the byte have before, and after?
```

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | Up and down became 1 and 0. A mask is a number whose bits are named as instructions: flip, or leave. The parity bit names a fact about a whole message in one bit. |
| What is promised? | `parity_bit` promises the bit that makes the count of 1s even. A parity check promises to catch any one flipped bit, and promises nothing about two. |
| What happens when? | Each toggle depends on the value before it. XOR with the same mask twice brings a value back. The parity loop works through the bits one at a time, from left to right. |
| What does this space let us do? | In the space of bits, XOR is its own undo. The whole check rests on an assumption that often goes unsaid: at most one bit flips. |

## What we have now

| Term or tool | What it means |
|---|---|
| `^` | XOR in Python. `1 ^ 1` is 0, `1 ^ 0` is 1. Also works on `True` and `False`. |
| $\oplus$ | XOR, as maths writes it |
| flip, toggle | XOR with 1 flips a bit. Doing it again flips it back. |
| bitwise | Working on each column of bits separately, as `12 ^ 10` does |
| mask | A number whose 1s say which bits to flip |
| `format(n, "08b")` | `n` in binary, with zeros on the left to make eight digits |
| parity | Whether a row of bits has an even or an odd number of 1s |
| parity bit | One extra bit that makes the number of 1s even |
| `parity_bit(bits)` | Your toolkit function: the XOR of all the bits |

The practice page is next. After it, the unit ends with
[Mixed problems: decisions and logic](tutorial:mixed-decisions-and-logic),
which draws on all four pages of Unit 2.
