---
title: "Waves: sine, cosine and sound — Practice"
practice_for: waves
year: "2026-2027"
version: 2026.09.26.1
---

# Waves: sine, cosine and sound — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another way** means reach the same place by a second
route. The answers are folded away until you open them, and each is one
way through: yours may go another way.

Your toolkit is loaded on this page, including `wave` from the tutorial
and `point_on_circle` from
[Going round in circles](tutorial:going-round-in-circles). `math` is
not: each cell that needs it starts with `import math`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: waves-practice-warm-up
import math
# Try things here
```

**1. Predict.** What do these two calls give?

```python
print(wave(2, 1, 0.25), wave(2, 1, 0.5))
```

<details class="dl-answer"><summary>answer</summary>

`2.0 2.4492935982947064e-16`.

A 1 Hz wave takes one second to repeat. A quarter of a second is a
quarter of the way through, where the wave is at its top: the
amplitude, 2. Half a second is halfway, where the wave crosses its
middle line going down. The exact answer is 0, and
$2.4 \times 10^{-16}$ is a float's rounding error.

</details>

**2. Make.** The alternating current in an Irish socket swings at 50
Hz, and the A that bands tune to is 440 Hz. How long is one period of
each, in milliseconds?

<details class="dl-answer"><summary>answer</summary>

```python
print(1000 / 50)
print(1000 / 440)
```

20 ms and about 2.27 ms. The period is $\frac{1}{f}$ seconds, and
there are 1,000 milliseconds in a second, so the period in
milliseconds is $\frac{1000}{f}$.

</details>

**3. Predict.** What does this print? Which notes are they?

```python
print(440 * 2 ** 2, 440 / 2 ** 3)
```

<details class="dl-answer"><summary>answer</summary>

`1760 55.0`.

Each octave up doubles the frequency, so $440 \times 2^2 = 1760$ Hz is
an A two octaves up. Each octave down halves it, so
$440 \div 2^3 = 55$ Hz is an A three octaves down, one of the lowest
notes on a bass guitar.

</details>

**4. Explain.** A resting heart beats 72 times a minute. What is its
frequency in hertz, and its period in seconds? Is a heartbeat a
periodic signal? Is it a sine wave?

<details class="dl-answer"><summary>answer</summary>

72 beats a minute is $72 \div 60 = 1.2$ beats a second, so 1.2 Hz. The
period is $\frac{1}{1.2} \approx 0.83$ seconds.

A steady heartbeat is roughly periodic: the same pattern comes round
again and again. But it is not a sine wave. A heart monitor shows a
sharp spike and some smaller bumps, not a smooth curve. Periodic means
"repeats". A sine wave is one repeating shape among many.

</details>

## Core

A cell for the core problems.

```python exec
id: waves-practice-core
import math
import matplotlib.pyplot as plt
# Your working for problems 5 to 12
```

**5. Make.** The sea rises and falls about twice a day. Here is a model
with made-up numbers of about the right size for the Irish coast: the
sea goes 1.8 m above and below its average level, and one repeat takes
12.42 hours. Measure time in hours, so the frequency is
$\frac{1}{12.42}$ repeats an hour. How high is the sea, compared with
its average, 3 hours after it passes the average on its way up? When is
it first at its highest? Draw 24 hours.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `wave` works in any unit of time, if the frequency uses the same
   unit. Here both are in hours.
2. The height at 3 hours is `wave(1.8, 1 / 12.42, 3)`.
3. A wave is at its top a quarter of the way through its first repeat.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
per_hour = 1 / 12.42
print(wave(1.8, per_hour, 3))
print(12.42 / 4)

hours = []
sea = []
for step in range(241):
    hours.append(step / 10)
    sea.append(wave(1.8, per_hour, step / 10))
plt.plot(hours, sea)
plt.axhline(0, color="grey")
plt.xlabel("hours")
```

After 3 hours the sea is about 1.80 m above average, almost at the
top. It reaches the top at a quarter of the period,
$12.42 \div 4 \approx 3.1$ hours. The drawing shows two high tides and
two low tides in a day, with each high tide a little later than the
last. A real tide is not a perfect sine wave, and the moon and the
shape of the coast change it, but this is a fair first model.

</details>

**6. Fix.** Schlomi, who is learning Python too, wrote her own wave
function. The test fails. What does her function do with a quarter of a
second, and what needs to change?

```python exec
id: waves-practice-fix-degrees
import math

def sound_wave(amplitude, frequency, time):
    """Return the height of a sine wave at a time in seconds."""
    return amplitude * math.sin(360 * frequency * time)

assert close_enough(sound_wave(1, 1, 0.25), 1), "the top, a quarter through"
print("sound_wave keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

A whole turn is $360^\circ$, and in degrees Schlomi's idea holds. But
`math.sin` takes radians, and a whole turn in radians is $2\pi$:

```python
    return amplitude * math.sin(2 * math.pi * frequency * time)
```

`math.sin(math.radians(360 * frequency * time))` works too. The first
version made $360 \div 2\pi \approx 57$ turns where it meant one.

</details>

**7. Predict.** What does this give? Think about how far through its
repeat the wave is.

```python
print(wave(1, 440, 1 / 880))
```

<details class="dl-answer"><summary>answer</summary>

`1.2246467991473532e-16`, which is 0 give or take a rounding error.

The period of a 440 Hz wave is $\frac{1}{440}$ of a second, and
$\frac{1}{880}$ is half of that. Halfway through a repeat, a sine wave
is back on its middle line, going down.

</details>

**8. Make.** The major scale that starts on middle C (C, D, E, F, G,
A, B, C) goes up by these numbers of semitones from middle C: 0, 2, 4,
5, 7, 9, 11 and 12. Middle C is 9 semitones below the 440 Hz A. Print
each note's frequency, rounded to two decimal places.

<details class="dl-answer"><summary>answer</summary>

```python
semitone = 2 ** (1 / 12)
middle_c = 440 * semitone ** -9
names = ["C", "D", "E", "F", "G", "A", "B", "C"]
steps = [0, 2, 4, 5, 7, 9, 11, 12]
for position in range(8):
    print(names[position], round(middle_c * semitone ** steps[position], 2))
```

C 261.63, D 293.66, E 329.63, F 349.23, G 392.0, A 440.0, B 493.88 and
C 523.25. The last C is exactly twice the first: 12 semitones make an
octave. These are the white keys of a piano from middle C up.

</details>

**9. Another way.** Make a cosine wave with your `wave` tool, without
`math.cos`. It should have amplitude 3 and frequency 2. Check it against
`3 * math.cos(2 * math.pi * 2 * t)` at a few times.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A cosine wave is a sine wave a quarter turn ahead.
2. A quarter turn of a 2 Hz wave takes a quarter of its period:
   $\frac{1}{4} \times \frac{1}{2} = \frac{1}{8}$ of a second.
3. So the cosine at time `t` is the sine at time `t + 1/8`.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
for t in [0, 0.1, 0.37]:
    print(wave(3, 2, t + 1 / 8), 3 * math.cos(2 * math.pi * 2 * t))
```

The two columns agree, give or take a rounding error: 3.0, then
0.927..., then −0.188.... Asking the sine wave for a time an eighth of
a second later gives the cosine wave now: a phase shift of a quarter
turn.

</details>

**10. Predict.** The tangent has no value at $90^\circ$. So what will
Python do with this line?

```python
print(math.tan(math.radians(90)))
```

<details class="dl-answer"><summary>answer</summary>

It prints `1.633123935319537e+16`, about 16 thousand million million,
with no error.

`math.radians(90)` is a tiny bit less than $\frac{\pi}{2}$, because a
float cannot keep all of its digits. Just before $90^\circ$, the line
out to the point is almost straight up, and its slope is enormous. So
Python gives an enormous number instead of an error. A value like this
in a program is a sign that the maths has no answer there.

</details>

**11. Make.** Write `wave_late(amplitude, frequency, time, delay)`: the
same wave as `wave`, but starting `delay` seconds late. Then show that a
200 Hz wave and the same wave half a period late add up to 0 at every
time you try.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A wave that starts `delay` seconds late is, at time `time`, where
   the first wave was at `time - delay`.
2. So `wave_late` can give back `wave(amplitude, frequency, time - delay)`.
3. Half a period of a 200 Hz wave is $\frac{1}{2} \times \frac{1}{200}$
   seconds.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def wave_late(amplitude, frequency, time, delay):
    """Return the height of a sine wave that starts delay seconds late."""
    return wave(amplitude, frequency, time - delay)

half_period = 1 / 400
for step in range(100):
    time = step / 10000
    together = wave(1, 200, time) + wave_late(1, 200, time, half_period)
    assert close_enough(together, 0), time
print("They cancel at every time tried.")
```

It prints `They cancel at every time tried.` This is the tutorial's
noise-cancelling idea, written with a delay in seconds instead of
$\pi$ radians.

</details>

**12. Explain.** Two sounds are played one after the other. The first
is `wave(0.5, 300, t)` and the second is `wave(2, 300, t)`. What would
you hear that is different, and what would be the same? And for
`wave(1, 300, t)` then `wave(1, 600, t)`?

<details class="dl-answer"><summary>answer</summary>

The first pair has the same frequency, so the same pitch: the same
note. The second sound has four times the amplitude, so it is louder.

The second pair has the same amplitude but double the frequency. The
second note is higher, by exactly one octave. It is about as loud,
although our ears do not hear all pitches equally loudly.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: waves-practice-stretch
import math
import matplotlib.pyplot as plt
# Your working for problems 13 to 16
```

**13. Make.** When two guitar strings are almost in tune, you can hear
the sound swell and fade, slowly. Add a 440 Hz wave and a 441 Hz wave
together, each with amplitude 1, and draw the sum over 2 seconds. Use
8,000 points a second. How often does the sound swell?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The times are `step / 8000` for `step` in `range(16001)`.
2. At each time, add `wave(1, 440, time)` and `wave(1, 441, time)`.
3. The picture will be a solid block of colour where the sound is
   loud. Look at its outline.

**Think about:** at the start both waves are in step. After half a
second, the 441 Hz wave has made half a repeat more. What happens when
they are half a turn apart?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
times = []
together = []
for step in range(16001):
    time = step / 8000
    times.append(time)
    together.append(wave(1, 440, time) + wave(1, 441, time))

plt.plot(times, together, linewidth=0.3)
plt.xlabel("time in seconds")
```

The outline swells to 2 at 0, 1 and 2 seconds, and shrinks to almost
nothing at 0.5 and 1.5 seconds: once a second. Each second, the 441 Hz
wave makes one more repeat than the 440 Hz wave. When the two are in
step they add up, and when they are half a turn apart they cancel.
These swells are called *beats*, and there is one for each hertz of
difference. Guitarists tune by turning a peg until the beats slow down
and stop.

</details>

**14. Another way.** Here are 8,000 heights of a note, measured over one
second. Pretend you do not know its frequency. Find it by counting how
many times the wave crosses its middle line going up. Does it match?

```python exec
id: waves-practice-count
heights_heard = []
for step in range(8001):
    heights_heard.append(wave(1, 262, step / 8000))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The wave crosses going up between two heights when the first is
   below 0 and the next is 0 or more.
2. Go through the positions from 1 to the end, and compare each height
   with the one before it.
3. Count the crossings.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
crossings = 0
for position in range(1, len(heights_heard)):
    if heights_heard[position - 1] < 0 <= heights_heard[position]:
        crossings = crossings + 1
print(crossings)
```

It prints `262`, the frequency the heights were made with: one upward
crossing per repeat, and 262 repeats in a second. That is middle C,
rounded. A tuner app does something like this with the sound from its
microphone, with more care about noise.

</details>

**15. Explain.** Noise-cancelling headphones do well with the hum of a
plane's engine, and much less well with a baby crying two rows back.
Why?

<details class="dl-answer"><summary>answer</summary>

To cancel a sound, the headphones must play its opposite, half a turn
out of phase, at the same moment the sound arrives. An engine's hum
repeats steadily at low frequencies, so the headphones can predict its
next repeat, and there is time to make its opposite. A cry changes
all the time, in pitch and in loudness, and has many high frequencies.
Each repeat is short, so a small delay is a large part of a turn, and
the opposite wave arrives out of step. Closed ear cups still block
some high sounds in the ordinary way.

</details>

**16. Fix.** A piano has 88 keys. Key 49 is the 440 Hz A, and each key
is one semitone from the next, so key number `key` has frequency
$440 \times 2^{(\text{key} - 49)/12}$. Schlomo, who is learning Python
too, wrote this function, and for middle C, key 40, it gives 220. What
is it doing, and what needs to change?

```python exec
id: waves-practice-fix-piano
def key_frequency(key):
    """Return the frequency in Hz of a piano key, where key 49 is the 440 Hz A."""
    return 440 * 2 ** ((key - 49) // 12)

print(key_frequency(49), key_frequency(40))
assert close_enough(key_frequency(40), 261.63, tolerance=0.01), "middle C"
print("key_frequency keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

It prints `440 220.0`, and the test fails. `//` rounds down to a whole
number, so $(40 - 49) \div 12 = -0.75$ becomes −1: a whole octave down,
to the A at 220 Hz. Every key is pushed down to the nearest A at or
below it. The power needs the fraction, which is `/`:

```python
    return 440 * 2 ** ((key - 49) / 12)
```

Now middle C gives 261.6255653005986, and the test passes. The test at
key 49 alone would never have found this, because $0 // 12$ and
$0 / 12$ are both 0. Schlomo's `//` is the division he has used most,
for pixels and digits, and here it quietly rounds the power down.

</details>
