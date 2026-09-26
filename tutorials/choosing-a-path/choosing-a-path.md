---
title: "Choosing a path: if, elif and else"
year: "2026-2027"
version: 2026.09.26.1
covers:
  pictures-on-a-number-line:
    touches: [MIT-1.11]
  asking-python-a-question:
    covers: [PDP-LO4]
  solving-an-inequality:
    covers: [MIT-1.11]
  a-move-that-turns-the-sign-round:
    covers: [MIT-1.11]
  two-paths-if-and-else:
    covers: [PDP-LO6]
    touches: [PDP-LO4]
  more-than-two-paths-elif:
    covers: [PDP-LO6]
  a-tool-of-your-own-between:
    touches: [MIT-1.11, PDP-LO6]
---

# Choosing a path: if, elif and else

You may have felt this. You are on a long video call, and the phone in
your hand gets warm. Then a game on the same phone starts to stutter. Nobody
pressed a button to slow it down. The phone did that by itself, on
purpose. How does a phone decide when to slow its processor down?

A *processor* is the chip that carries out a program's instructions.
When it works hard, it gets hot. Most phones have no fan, so the way to
cool the chip is to run it more slowly for a while. This is called
*thermal throttling*. "Thermal" means "to do with heat". Somewhere in the
phone, a few lines of code read a temperature and choose what to do. By
the end of this page, you will have written lines like them.

On this page we:

- draw "below 0 °C" and "80 °C and over" as pictures on a number line
- ask Python questions that have the answer True or False
- solve an inequality: how many minutes of video fit on a phone?
- let a program choose a path with `if`, `elif` and `else`
- add our first decision tool to the toolkit: `between`

> **The space we're in.** We use the whole numbers and decimals from
> Unit 1, and Python's own ways of comparing them. Every question on this
> page has exactly two answers, True or False. There is no "maybe" here.
> Lines still run from top to bottom, but now some lines can be skipped.
> A temperature rule never says how fine the readings are. Some sensors give whole degrees. Others give tenths.

## Warm-up

Two questions from Unit 1. The first is from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold), and
the second from
[When Python says no: reading error messages](tutorial:when-python-says-no).

```question
id: choosing-warm-up-1
type: multiple-choice
answer: 2

What does Python give for `7 // 2`?

- `3.5`
  - This is `7 / 2`, ordinary division.
- `3`
  - `//` divides and keeps only the whole number part.
- `4`
  - This rounds 3.5 up, and `//` never rounds up.
- `1`
  - This is `7 % 2`, the remainder.
```

```question
id: choosing-warm-up-2
type: multiple-choice
answer: 2

The last line of an error says `NameError: name 'temprature' is not defined`.
What is the most likely cause?

- The number in `temprature` is too big for Python to hold.
  - A number too big would give a different error; a `NameError` is about a name.
- The name was typed differently here from where it was made.
  - The last line names the name Python could not find, spelled as it was typed here.
- Python cannot compare the numbers in this cell.
  - A comparison problem gives a `TypeError`, not a `NameError`.
- The cell has to be run a second time.
  - Running again gives the same error, until the name is made or spelled the same way.
```

## Pictures on a number line

Here are two rules a phone might follow. The numbers are made up, but
real phones have rules with this shape.

| Rule | When it applies |
|---|---|
| Do not charge the battery | the battery is below 0 °C |
| Slow the processor a lot | the chip is at 80 °C and over |

(Charging a lithium battery when it is very cold can damage it.) Let's
draw both rules on a line of temperatures, from $-20$ to 100.

"Below 0" is every temperature to the left of 0. Is 0 itself "below 0"?
No. So on the picture, 0 gets an empty circle, which means "up to here,
but not this point". A thick line runs from the circle to the left.

"80 and over" starts at 80 and runs to the right. This time 80 is
included, so it gets a filled circle.

<img src="two-rules-on-a-line.svg" alt="Two number lines of temperatures, each from −20 to 100 °C. On the first, for 'do not charge the battery: below 0 °C', there is an empty circle at 0 and a thick line running from it to the left. On the second, for 'slow the processor a lot: 80 °C and over', there is a filled circle at 80 and a thick line running from it to the right.">

An *inequality* is a statement that one amount is bigger or smaller than
another. Maths has four symbols for it:

| In words | Symbol | Example |
|---|---|---|
| less than | $<$ | $t < 0$ |
| less than or equal to | $\le$ | $t \le 79$ |
| greater than | $>$ | $t > 79$ |
| greater than or equal to | $\ge$ | $t \ge 80$ |

The small end of the symbol points at the smaller amount. An empty
circle on the number line goes with $<$ and $>$. A filled circle goes
with $\le$ and $\ge$.

```question
id: choosing-number-line-1
type: multiple-choice
answer: 2

Which of these is true for a chip at exactly 80 °C?

- $t < 80$
  - 80 is not less than 80, so this is False for 80 itself.
- $t \ge 80$
  - Greater than or equal to includes 80 itself: the filled circle.
- $t > 80$
  - 80 is not greater than 80: this is the empty circle.
```

Now a small puzzle. Do $t > 79$ and $t \ge 80$ draw the same picture?
Think about it before you read on.

They do, if the sensor only ever gives whole degrees, because there is
no whole number between 79 and 80. If it can read 79.5, they do not. The rule did
not change. The space we are in decided the answer.

## Asking Python a question

Python writes $\le$ as `<=` and $\ge$ as `>=`, because a keyboard has no
key for either. What do you think each line below will print? Make a
guess for all three, then run it to check.

```python exec
id: choosing-asking-1
temperature = 79
print(temperature < 0)
print(temperature >= 80)
print(temperature <= 79)
```

Python answers each question with `True` or `False`. A *condition* is a
question with exactly two possible answers, True or False. `True` and
`False` are values in Python, the same way `79` is a value. They are
written with a capital letter.

To ask whether two things are equal, we need two equals signs. One
equals sign already has a job. It names a value. So `temperature = 80` means
"let `temperature` stand for 80", and `temperature == 80` asks "is
`temperature` 80?". The sign `!=` asks "is it different?".

```python exec
id: choosing-asking-2
temperature = 80
print(temperature == 80)
print(temperature != 80)

too_hot = temperature >= 80
print(too_hot)
```

A condition's answer is a value, so we can give it a name, like any
other value.

### Your turn

1. In the first cell above, change `temperature = 79` to
   `temperature = -3`. Before you run it, guess the three answers.
2. In the cell below, set `temperature` to any value you like.
3. Write a line that prints True when `temperature` is 35 or more.

```python exec
id: choosing-your-turn-1
# A temperature, and a question about it
```

## Solving an inequality

Your phone has 10,000 MB free, and you want to film in 4K, the sharpest
setting. Say each minute of video takes 350 MB. (The real size depends
on the phone and its settings.) For how many whole minutes is there
room?

Pause here and guess. Ten minutes? An hour? I'll wait.

In words, there is room while the video is at most 10,000 MB. In
symbols, let $m$ stand for the number of minutes. The video takes
$350m$ MB, and we want

$$350m \le 10000$$

We solve an inequality with the same moves as an equation. We can add or
subtract the same amount on both sides. We can multiply or divide both
sides by the same positive number. Dividing both sides by 350 gives

$$m \le 28.57\ldots$$

We asked about whole minutes, so there is room for 28, and not for 29.

Before you run the cell, which line do you expect to say True? Run it to
check.

```python exec
id: choosing-solving-1
free_mb = 10000
mb_per_minute = 350

minutes = 28
print(minutes, "minutes:", mb_per_minute * minutes, "MB. Room?", mb_per_minute * minutes <= free_mb)

minutes = 29
print(minutes, "minutes:", mb_per_minute * minutes, "MB. Room?", mb_per_minute * minutes <= free_mb)
```

At 28 minutes the video takes 9,800 MB, and it fits. At 29 it takes
10,150 MB, and it does not. The algebra and the code agree. (In Unit 3, a
loop will check every value for us.)

### Your turn

A camera's memory card has 16,000 MB free, and each photo takes about
6 MB. How many photos fit?

1. Write the inequality in words, then with a letter.
2. Solve it on paper.
3. Check your answer in the cell below, with one photo fewer and one
   photo more than your answer.

```python exec
id: choosing-your-turn-2
# Check your memory card answer here
```

## A move that turns the sign round

A small drone takes off with its battery at 100%. It uses 3.5% of the
battery each minute, and the pilot wants to land with at least 20% left.
For how many minutes $t$ can it fly?

In symbols: $100 - 3.5t \ge 20$.

Subtract 100 from both sides: $-3.5t \ge -80$.

Now divide both sides by $-3.5$. It looks like the answer is
$t \ge 22.86$. But at 30 minutes the battery would be at
$100 - 3.5 \times 30 = -5$ percent. Something went wrong. Before you run the next cell, can you
guess which of these three lines print True?

```python exec
id: choosing-sign-1
print(3 < 5)
print(-3 < -5)
print(-3 > -5)
```

Three is less than five. But $-3$ is greater than $-5$. It is closer to
zero, so it sits further to the right on the number line. Multiplying or
dividing by a negative number turns the whole number line round, so the
order of any two numbers turns round too. I think this is the strangest
move on the page. The same division gives the right number but the
wrong sign.

<img src="turning-the-line-round.svg" alt="Two number lines from −6 to 6. On the top line, 3 and 5 are marked, and 3 is further left: 3 is less than 5. Multiplying by −1 moves each one to its mirror place on the bottom line, so 3 goes to −3 and 5 goes to −5. Now −5 is further left, so −3 is greater than −5.">

So in the space of inequalities, dividing by a negative number is
allowed, but the sign turns round. So $-3.5t \ge -80$
becomes

$$t \le 22.86\ldots$$

Let's check that on both sides of 22.86.

```python exec
id: choosing-sign-2
battery_start = 100
use_per_minute = 3.5

minutes = 22
print(minutes, "minutes:", battery_start - use_per_minute * minutes, "% left. Safe?", battery_start - use_per_minute * minutes >= 20)
minutes = 23
print(minutes, "minutes:", battery_start - use_per_minute * minutes, "% left. Safe?", battery_start - use_per_minute * minutes >= 20)
```

After 22 minutes the battery is at 23%, which is safe. After 23 minutes
it is at 19.5%, which is not. So the pilot has 22 whole minutes.

There is another way that never divides by a negative. Add $3.5t$ to
both sides of $100 - 3.5t \ge 20$ to get $100 \ge 20 + 3.5t$. Subtract
20: $80 \ge 3.5t$. Divide by 3.5: $22.86 \ge t$. This gives the same
answer.

## Two paths: if and else

Back to the hot phone. Here is a program that knows two speeds. Guess
what it prints for `temperature = 85`. Then run it to check.

```python exec
id: choosing-if-else-1
temperature = 85

if temperature >= 80:
    print("Too hot: slowing the processor down.")
else:
    print("Full speed.")

print("Temperature checked.")
```

Now change `temperature` to 40 and run it again.

The word `if` starts a question. After it comes a condition, then a
colon. The lines pushed in under it run only when the condition is True.
Under `else` are the lines that run when it is False. Each of these
groups of pushed-in lines is a *branch*, and the program takes exactly
one of them. The last line is not pushed in, so it runs every time.

Python uses the spaces at the start of a line to know which lines
belong to a branch. On
[When Python says no](tutorial:when-python-says-no) we met the
`IndentationError`. Now we can see why Python cares so much about those
spaces.

On [Recipes are algorithms](tutorial:recipes-are-algorithms), a robot
making tea chose a path with "if they take milk, add milk". That shape
was called selection. Here is the same shape, with Python doing the
choosing.

Any True or False value can be a condition, including a name:

```python exec
id: choosing-if-else-2
plugged_in = True

if plugged_in:
    print("Charging.")
else:
    print("On battery.")
```

## More than two paths: elif

A laptop has a fan with several speeds. The word `elif` is short for "else if". It adds another condition. Python
checks the conditions from the top, one after another. It takes the
first path whose condition is True, and skips every path after it.

Here is a fan rule as a function, which returns a speed. The limits
are made up.

```python exec
id: choosing-elif-1
def fan_speed_for(temperature):
    """Return the fan speed for a chip temperature in °C."""
    if temperature < 50:
        return "off"
    elif temperature < 70:
        return "low"
    elif temperature < 85:
        return "high"
    else:
        return "full"

print(fan_speed_for(35))
print(fan_speed_for(60))
print(fan_speed_for(75))
print(fan_speed_for(90))
```

Look at the second condition, `temperature < 70`. The fan should be
"low" from 50 to 69, but the code never checks that the temperature is
50 or more. It does not need to. We only reach that line when
`temperature < 50` was False. So the order of the checks
matters.

```question
id: choosing-elif-2
type: multiple-choice
answer: 1

What does `fan_speed_for(70)` give?

- `"high"`, because `70 < 70` is False, and `70 < 85` is True
  - Python checks each condition in turn, and 70 < 85 is the first that is True.
- `"low"`, because 70 is the limit for "low"
  - 70 is not less than 70, so the first condition is False.
- `"full"`, because no condition fits
  - The `elif` for below 85 fits 70, so Python never reaches `else`.
```

Now let's put the same checks in a different order. This cell has a
mistake in it on purpose. Before you run it, what do you think a cool
laptop, at 35 °C, will do?

```python exec
id: choosing-elif-3
def fan_in_wrong_order(temperature):
    """The same four speeds, checked in a different order."""
    if temperature < 85:
        return "high"
    elif temperature < 50:
        return "off"
    elif temperature < 70:
        return "low"
    else:
        return "full"

print(fan_in_wrong_order(35))
```

The fan runs "high" on a cool laptop. Python did exactly what it was
told. Every temperature under 50 is also under 85, so the first
condition catches it, and the line `elif temperature < 50` can never be
reached. Nothing crashed, and no error message appeared. This kind of
mistake only appears when we test with the right temperatures.

### Your turn

Real chips protect themselves: if they get far too hot, they switch off.

1. Copy `fan_speed_for` into the cell below.
2. Add a path so that at 100 °C and over it returns `"shut down"`. Think
   about where in the order it has to go.
3. Test it: `print(fan_speed_for(105))` should print `shut down`, and
   `print(fan_speed_for(90))` should still print `full`.

```python exec
id: choosing-your-turn-3
# Your fan_speed_for, with a shut down at 100 °C and over
```

<aside class="dl-note" id="choosing-note-throttling">

**Slowing down on purpose.** Phones and laptops really do this. The
chip reads its own temperature sensors many times a second. When a
review says a game "runs well for ten minutes and then slows", throttling
is usually why.

</aside>

## A tool of your own: between

Here is a real "between". Apple says an iPhone is designed to work where the air is
from 0 °C to 35 °C. Outside that, it may change how it behaves to protect
itself.

Maths writes it as one line with two signs: $0 \le t \le 35$. Python
lets us write it the same way. What do you expect each line to print?
Run it to check.

```python exec
id: choosing-between-1
temperature = 20
print(0 <= temperature <= 35)

temperature = 35
print(0 <= temperature <= 35)

temperature = 36
print(0 <= temperature <= 35)
```

A value exactly at an end counts, because the signs are `<=`, the filled
circles on the number line.

Now let's make a tool from this. The cell below is a toolkit cell, like
the one where you finished `to_hex` on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
Later pages can use what you write here. The first line of the function and its promise are written for you.
Replace the comment with one `return` line that keeps the promise.

```python exec
id: choosing-between-toolkit
toolkit: yes
def between(value, low, high):
    """Return True when low <= value <= high, with both ends included.

    between(20, 0, 35) is True. between(36, 0, 35) is False.
    """
    # Replace this comment with one return line.
```

```python toolkit-reference
for: choosing-between-toolkit
def between(value, low, high):
    """Return True when low <= value <= high, with both ends included.

    between(20, 0, 35) is True. between(36, 0, 35) is False.
    """
    return low <= value <= high
```

Run your cell. Then how does your `between` compare with one way to
write it? The table below runs the same calls on your function and on a
solution, side by side. Until you write your `return` line, your column
shows `None`. A function with no `return` line returns `None`, Python's
value for nothing.

```inputs
for: choosing-between-toolkit
between(20, 0, 35)
between(0, 0, 35)     # the low end counts
between(35, 0, 35)    # so does the high end
between(-1, 0, 35)
between(36, 0, 35)
```

```solution
for: choosing-between-toolkit
def between(value, low, high):
    """Return True when low <= value <= high, with both ends included.

    between(20, 0, 35) is True. between(36, 0, 35) is False.
    """
    return low <= value <= high
```

Two rows sit on the ends, and two one step outside. A mistake like `<`
in place of `<=` would hide at the ends.

### Your turn

A road sensor sends out an ice warning when the road is from $-2$ to 2
degrees. (The limits here are made up.)

1. Set `temperature = 1` in the cell below.
2. Write an `if` and `else` that uses `between` to print either "Risk of
   ice" or "No ice warning".
3. Try `temperature` at $-3$, $-2$ and 2, and check each answer against
   the number line in your head.

```python exec
id: choosing-your-turn-4
# Your ice warning
```

<details class="dl-why"><summary>Why this way?</summary>

This page put two topics side by side: solving an inequality, from
algebra, and choosing a path with `if`, from programming. In most
courses they belong to different subjects, often in different terms,
with different teachers.

There are good reasons to keep them apart. Each subject can go at its
own speed.

We joined them because they are one question asked two ways. "How many
minutes of video fit?" is an inequality, and a phone answers it with
`if`. The number line works for both, and the code checks the algebra.
When each subject needs the other, neither one is a topic you learn once
and never use again.

</details>

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | Temperatures, minutes and battery levels. A condition's answer too: `too_hot = temperature >= 80`. `=` names, `==` asks. |
| What is promised? | `fan_speed_for` promises a speed for any temperature. `between` promises True exactly when the value is from `low` to `high`. The asserts check the promise. |
| What happens when? | Conditions are checked from the top. The first True one wins, and the rest are skipped, so the order of the `elif` checks changes the answer. |
| What does this space let us do? | Inequalities allow the same moves as equations, but dividing by a negative turns the sign round. Whole-degree readings make $t > 79$ and $t \ge 80$ the same. |

## What we have now

| Term or move | What it means |
|---|---|
| inequality | A statement that one amount is bigger or smaller than another: $<$, $\le$, $>$, $\ge$ |
| `<`, `<=`, `>`, `>=`, `==`, `!=` | Python's comparisons. Each gives `True` or `False`. |
| condition | A question whose answer is True or False |
| solving an inequality | The same moves as an equation. Dividing or multiplying by a negative number turns the sign round. |
| `if`, `elif`, `else` | Choose one branch. Checked from the top; the first True condition wins. |
| branch | The lines pushed in under `if`, `elif` or `else` |
| `low <= value <= high` | Two comparisons in one line, the way maths writes "between" |
| `between(value, low, high)` | Your first decision tool, now in your toolkit |

For more examples of `if`, `elif` and `else`, the integrated course has
[Making decisions with if, elif and else](tutorial:making-decisions).

## Where to read more

Stand-up Maths (2016). *Leap Years: we can do better.*
<https://www.youtube.com/watch?v=qkt_wmRKYNQ>. A year is a leap year if it
divides by 4, unless it divides by 100, unless it divides by 400. Matt
Parker explains where that rule comes from, and suggests a better one.
Twelve minutes.
