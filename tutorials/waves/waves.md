---
title: "Waves: sine, cosine and sound"
year: "2026-2027"
version: 2026.09.26.1
covers:
  a-point-going-round-drawn-against-time:
    covers: [MIT-3.3, MIT-4.6]
  how-high-amplitude:
    covers: [MIT-4.6]
    touches: [MIT-3.3]
  how-often-frequency-and-period:
    covers: [MIT-4.6]
    touches: [MIT-3.3]
  a-tool-for-waves:
    covers: [MIT-3.3]
    touches: [PDP-LO10]
  higher-notes-an-octave-is-a-doubling:
    covers: [MIT-4.6]
    touches: [MIT-1.1]
  starting-late-phase:
    covers: [MIT-4.6]
    touches: [MIT-3.3]
  tangent-repeats-but-is-not-a-wave:
    covers: [MIT-3.3]
---

# Waves: sine, cosine and sound

Pluck the thickest string of a guitar, then the thinnest. The second
note is higher. Both strings are the same length, and both are made to
move by the same finger. So what makes one note higher than another?

Pause and make a guess before you read on. The answer is a number you
can count, and the same number describes the electricity in the wall
beside you.

On this page we:

- draw a point going round a circle against time, and get a wave
- make a wave taller or shorter: its amplitude
- make it repeat faster or slower: its frequency and its period
- add `wave` to the toolkit, and draw the voltage in an Irish socket
- find the notes of a piano, and see that an octave is a doubling
- start a wave late, and use that to cancel a noise
- draw the tangent, which repeats but is not a wave

> **The space we're in.** Time, in seconds, starting from 0. Python's
> `math.sin` and `math.cos` take radians, as on
> [Going round in circles](tutorial:going-round-in-circles#python-measures-angles-another-way),
> and your `point_on_circle` takes degrees. One thing usually goes
> unsaid: a real sound is never a perfect sine wave. A sine wave is the
> simplest sound there is, and it is the model we build the others from.

## Warm-up

The first question is from
[Going round in circles](tutorial:going-round-in-circles#python-measures-angles-another-way),
and the second from
[Doubling and halving](tutorial:doubling-and-halving#a-rumour-that-doubles).

```question
id: waves-warm-up-1
type: multiple-choice
answer: 3

A whole turn is $360^\circ$. How many radians is it?

- 360
  - 360 is the count in degrees; radians measure a turn by the circle's own radius.
- $\pi$
  - π radians is half a turn, 180°.
- $2\pi$
  - The whole way round a circle of radius 1 is 2π long: 2π radians.
- 1
  - 1 radian is the angle whose arc is as long as the radius, about 57°.
```

```question
id: waves-warm-up-2
type: fill-in-the-blank

Start at 55 and double three times. You reach {440}.
```

## A point going round, drawn against time

A sound is air being pushed and pulled. A guitar string swings back and
forth, and each swing squeezes the air next to it, then lets it go. Your
ear feels the air pressure go up and down, again and again.

Something that goes up and down, again and again, is what a point going
round a circle does, if we watch only its height. Picture the point on
the unit circle from
[Going round in circles](tutorial:going-round-in-circles#a-circle-of-radius-1).
It starts at $(1, 0)$ and goes round twice. Each step, we write down
how far it has turned and how high it is. Then we draw the height
against the turn. What shape do you expect?

```python exec
id: waves-unroll-1
import math
import matplotlib.pyplot as plt

turned = []
heights = []
for angle in range(0, 721, 5):
    x, y = point_on_circle(1, angle)
    turned.append(angle)
    heights.append(y)

plt.plot(turned, heights)
plt.axhline(0, color="grey")
plt.axvline(0, color="grey")
plt.xticks(range(0, 721, 90))
plt.xlabel("degrees turned")
plt.ylabel("height of the point")
```

The height rises to 1 at $90^\circ$, falls back through 0 at
$180^\circ$, reaches −1 at $270^\circ$, and is back at 0 after a whole
turn. Then it does the same again. This curve is the graph of
$y = \sin\theta$, and its shape is called a *sine wave*.

Here is the same idea, moving. On the left the point goes round; on the
right its height is drawn against time, one second at a time. After you
have watched it once, change `turns_per_second` to 2. Before you run
it again, guess: what happens to the wave on the right?

```python exec
id: waves-unroll-animation
from matplotlib.animation import FuncAnimation

turns_per_second = 1     # change it, then run the cell again

figure, (circle_side, wave_side) = plt.subplots(
    1, 2, figsize=(4.4, 1.9), gridspec_kw={"width_ratios": [1, 2]})
rim_x = []
rim_y = []
for angle in range(0, 361, 10):
    x, y = point_on_circle(1, angle)
    rim_x.append(x)
    rim_y.append(y)
circle_side.plot(rim_x, rim_y, color="lightgrey")
circle_side.set_aspect("equal")
circle_side.axis("off")
wave_side.set_xlim(0, 2)
wave_side.set_ylim(-1.2, 1.2)
wave_side.axhline(0, color="grey")
wave_side.set_xlabel("seconds")
point, = circle_side.plot([1], [0], "o", color="C1")
trace, = wave_side.plot([], [], color="C0")
times_so_far = []
heights_so_far = []


def draw_frame(frame):
    if frame == 0:           # start the trace again each time round the loop
        times_so_far.clear()
        heights_so_far.clear()
    time = frame / 20
    x, y = point_on_circle(1, 360 * turns_per_second * time)
    point.set_data([x], [y])
    times_so_far.append(time)
    heights_so_far.append(y)
    trace.set_data(times_so_far, heights_so_far)


figure.tight_layout()
FuncAnimation(figure, draw_frame, frames=41, interval=100)
```

At one turn a second, the right side draws two humps in two seconds.
At two turns a second, it draws four, squeezed into the same space.
The circle looks the same, only faster; the wave changes shape. The
animation loops; run the cell again to watch it from the start.

A function whose graph repeats the same piece for ever is *periodic*.
The sine wave repeats every $360^\circ$, because after a whole turn the
point is back where it started.

### Your turn

1. Change `heights.append(y)` to `heights.append(x)`, to draw how far
   across the point is. That is $y = \cos\theta$. How is it like the
   sine wave, and how is it different?
2. Change `721` to `1441` in both places. How many times does the wave
   repeat?

## How high: amplitude

A louder note from the same string moves the air more. Its wave has the
same shape and goes up and down just as often, but further each time.

To make a wave taller, multiply it. $y = 3\sin\theta$ goes up to 3 and
down to −3. The largest distance a wave goes from its middle line is its
*amplitude*. Which of these three waves will be the tallest?

```python exec
id: waves-amplitude-1
for amplitude in [0.5, 1, 3]:
    stretched = []
    for height in heights:
        stretched.append(amplitude * height)
    plt.plot(turned, stretched, label="amplitude " + str(amplitude))

plt.axhline(0, color="grey")
plt.legend()
```

All three cross 0 at the same places, and reach their tops at the same
places. Only the height changes. For a sound, a bigger amplitude is a
louder sound.

## How often: frequency and period

Now time. A point that goes round the circle 2 times every second makes
a wave that repeats 2 times every second. The number of times a wave
repeats in one second is its *frequency*, measured in *hertz*, Hz. One
hertz is once a second.

The time one repeat takes is the *period*. At 2 Hz, each repeat takes
half a second. The frequency and the period undo each other:

$$\text{period} = \frac{1}{\text{frequency}} \qquad T = \frac{1}{f}$$

How far round has the point turned after $t$ seconds? It makes $f$
whole turns every second, so after $t$ seconds it has made $f \times t$
turns. Each turn is $2\pi$ radians. So the angle is $2\pi f t$, and the
height is

$$y = A \sin(2\pi f t)$$

In words: find how many turns, $f \times t$; turn that into radians by
multiplying by $2\pi$; take the sine; then multiply by the amplitude.
Here is a 2 Hz wave over one second. How many humps above the line will
you see?

```python exec
id: waves-frequency-1
times = []
for step in range(201):
    times.append(step / 200)

heights_2hz = []
for time in times:
    heights_2hz.append(math.sin(2 * math.pi * 2 * time))

plt.plot(times, heights_2hz)
plt.axhline(0, color="grey")
plt.xlabel("time in seconds")
```

Two humps, and two dips: 2 repeats in one second, each 0.5 seconds
long.

The electricity in an Irish wall socket is a wave too. The electric
current there is *alternating current*, AC: it pushes one way along the
wire, then the other, again and again. It swings 50 times a second, at
50 Hz, so each repeat takes $\frac{1}{50}$ of a second, 20
milliseconds.

```question
id: waves-period-1
type: multiple-choice
answer: 2

The tide at Dublin comes in and goes out about twice a day: one repeat
takes about 12 hours 25 minutes. What is its period, and roughly what
is its frequency?

- period 2 per day; frequency 12 hours 25 minutes
  - These are swapped: a period is a length of time, and a frequency counts repeats in a time.
- period 12 hours 25 minutes; frequency about 2 per day
  - The period is how long one repeat takes; the frequency is how many repeats fit in a day.
- period and frequency are both 12 hours 25 minutes
  - A frequency counts repeats, and 12 hours 25 minutes is a length of time.
```

## A tool for waves

We will draw a lot of waves, so here is a tool. Its promise is the
formula above, and its one line is yours to write.

```python exec
id: waves-toolkit
toolkit: yes
import math

def wave(amplitude, frequency, time):
    """Return the height of a sine wave at a time in seconds.

    The wave starts at 0, goes up first, and repeats frequency times a second.
    wave(1, 1, 0.25) is 1: a quarter of the way through its first repeat.
    """
    ...
```

```python toolkit-reference
for: waves-toolkit
import math

def wave(amplitude, frequency, time):
    """Return the height of a sine wave at a time in seconds.

    The wave starts at 0, goes up first, and repeats frequency times a second.
    wave(1, 1, 0.25) is 1: a quarter of the way through its first repeat.
    """
    return amplitude * math.sin(2 * math.pi * frequency * time)
```

Run the toolkit cell, then the tests. Until `wave` has its `return`
line, it gives back `None`, and the first test stops with a
`TypeError`. The last test checks the promise that makes a wave a
wave: one period later, it is back at the same height.

```python exec
id: waves-toolkit-tests
assert close_enough(wave(1, 1, 0.25), 1), "the top, a quarter through"
assert close_enough(wave(1, 1, 0.75), -1), "the bottom, three quarters through"
assert close_enough(wave(3, 2, 0.125), 3), "amplitude 3, 2 Hz"
assert close_enough(wave(5, 440, 0), 0), "every wave starts at 0"
for step in range(100):
    time = step / 1000
    assert close_enough(wave(2, 440, time + 1 / 440), wave(2, 440, time)), time
print("wave keeps its promise.")
```

```hint
Try `print(wave(1, 1, 0.25))` on its own. What came back? The formula is
$A \sin(2\pi f t)$: which name is $A$, which is $f$, and which is $t$?
```

Now the wall socket. A socket in Ireland is rated at 230 volts. (A volt
measures the push behind an electric current.) The 230 is a kind of
average of the swing: the steady voltage that would heat a kettle just
as much. The top of the swing, its amplitude, is $\sqrt{2}$ times more.
How high is that, and how many repeats will 40 milliseconds show? Make
both guesses, then run it. This cell and the rest of the page use your
`wave`, so write it first.

```python exec
id: waves-mains-1
peak_volts = 230 * math.sqrt(2)
print(round(peak_volts))

times = []
volts = []
for step in range(401):
    time = step / 10000          # 0 to 0.04 seconds
    times.append(time)
    volts.append(wave(peak_volts, 50, time))

plt.plot(times, volts)
plt.axhline(0, color="grey")
plt.xlabel("time in seconds")
plt.ylabel("volts")
```

The voltage swings between about +325 and −325 volts, twice in 40
milliseconds. That swing is the "alternating" in alternating current.
On
[When there is no real answer](tutorial:when-there-is-no-real-answer),
engineers wrote it as a complex number turning on a plane. Here is the
same turn, seen from the side: a point going round, drawn as its
height.

<aside class="dl-note" id="waves-note-hertz">

**Why hertz.** The unit is named after Heinrich Hertz, a German
physicist. Around 1887 he was the first to make radio waves on purpose
and detect them across a room. Radio, Wi-Fi and mobile phones all send
their messages on waves like the ones on this page, at millions or
thousands of millions of hertz.

</aside>

## Higher notes: an octave is a doubling

Back to the guitar. The thinnest string swings faster, so its wave has
a higher frequency. A higher frequency is a higher note. The word
musicians use for how high or low a note sounds is *pitch*.

Bands tune to one agreed note: the A above middle C, at 440 Hz. Here is
that A beside the A below it, at 220 Hz, over 10 milliseconds. How
many repeats will each one make?

```python exec
id: waves-notes-1
times = []
for step in range(501):
    times.append(step / 50000)

for frequency in [220, 440]:
    heights_note = []
    for time in times:
        heights_note.append(wave(1, frequency, time))
    plt.plot(times, heights_note, label=str(frequency) + " Hz")

plt.axhline(0, color="grey")
plt.xlabel("time in seconds")
plt.legend()
```

In 0.01 seconds, the 220 Hz wave makes 2.2 repeats and the 440 Hz wave
makes 4.4. Every time the lower one repeats once, the higher one
repeats twice, and they meet again at 0.

Two notes like this, where one frequency is double the other, are an
*octave* apart. They sound so alike that music gives them the same
letter. So going up an octave is doubling, as on
[Doubling and halving](tutorial:doubling-and-halving#a-rumour-that-doubles),
and going down is halving. On a guitar, the thickest string is an E at
82.41 Hz and the thinnest is an E at 329.63 Hz: exactly four times
higher, two octaves.

A piano splits each octave into 12 steps, called *semitones*. Each step
multiplies the frequency by the same number, and 12 steps must make a
doubling. So that number is the one that makes 2 when it is multiplied
by itself 12 times: $2^{1/12}$, about 1.0595. What will the loop print
for 12 semitones up from 440?

```python exec
id: waves-notes-2
semitone = 2 ** (1 / 12)
print(semitone, semitone ** 12)

names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"]
for step in range(13):
    print(names[step], round(440 * semitone ** step, 2))
```

The first line shows that $2^{1/12}$, multiplied by itself 12 times,
makes `2.000000000000001`: 2, give or take a float's rounding. Twelve
steps up from 440 end at 880.0, one octave up. Middle C is 9
semitones below the A, at $440 \times 2^{-9/12} \approx 261.63$ Hz. A
negative power counts halvings, as $2^{-3}$ did on
[Doubling and halving](tutorial:doubling-and-halving#halving-down-to-1).

People can hear from about 20 Hz to about 20,000 Hz. That is 1,000
times higher, so it is about $\log_2 1000 \approx 10$ doublings: about
ten octaves. A piano's keys cover a little over seven of them.

### Your turn

1. Find the frequency of the E above the 440 Hz A. It is 7 semitones
   up.
2. Change 220 to 330 in the cell. After how many milliseconds do the
   two waves start a repeat together again?

## Starting late: phase

Look again at the cosine wave from the first section. It is the sine
wave, a quarter turn ahead: the cosine is at its top at $0^\circ$, and
the sine reaches its top at $90^\circ$. In symbols,
$\cos\theta = \sin(\theta + 90^\circ)$.

How far one wave is ahead of or behind another, measured as part of a
turn, is its *phase*. Moving a wave along like this is a *phase shift*.
Two waves half a turn apart are exactly opposite: when one is at its
top, the other is at its bottom.

Noise-cancelling headphones use this. A small microphone hears the
engine noise of a plane. The headphones play the same wave, half a turn
late, and the two add up to almost nothing. What do you expect the sum
to look like?

```python exec
id: waves-phase-1
times = []
for step in range(201):
    times.append(step / 20000)

noise = []
cancel = []
heard = []
for time in times:
    engine = wave(1, 200, time)
    opposite = math.sin(2 * math.pi * 200 * time + math.pi)   # half a turn late
    noise.append(engine)
    cancel.append(opposite)
    heard.append(engine + opposite)

plt.plot(times, noise, label="engine")
plt.plot(times, cancel, label="headphones")
plt.plot(times, heard, label="what you hear", linewidth=3)
plt.legend()
```

The two waves are mirror images, and their sum is a flat line at 0.
Half a turn is $\pi$ radians, so adding $\pi$ inside the sine moved the
wave half a repeat along. Real headphones cancel low, steady sounds best,
such as an engine's hum, because each repeat is like the one before.

## Tangent repeats but is not a wave

On the last page, the tangent was $\frac{\sin\theta}{\cos\theta}$, the
slope of the line out to the point. Is its graph a wave too? The cell
leaves out the angles within $5^\circ$ of $90^\circ$ and $270^\circ$,
where the cosine is 0 or close to it.

```python exec
id: waves-tangent-1
for start, end in [(-85, 86), (95, 266), (275, 361)]:
    angles = []
    slopes_out = []
    for angle in range(start, end):
        angles.append(angle)
        slopes_out.append(math.tan(math.radians(angle)))
    plt.plot(angles, slopes_out, color="tab:blue")

plt.axhline(0, color="grey")
plt.ylim(-6, 6)
```

The tangent is periodic too, but it repeats every $180^\circ$, not
every $360^\circ$. It has no amplitude, because it has no top: near
$90^\circ$ the line out to the point is almost straight up, and its
slope grows without end. At $90^\circ$ itself, it has no value, as a
wall had no slope on [Straight lines](tutorial:straight-lines).

<details class="dl-why"><summary>Why this way?</summary>

This page measured waves in seconds and hertz, as sound is measured.
Most maths courses write a wave as $y = A\sin(B(x - C)) + D$, with $x$
in radians, and study what each of the four letters does to the graph.

The four-letter form is more general. It covers a wave that is lifted
up or down, which ours never was, and it is the form exam questions
and later maths courses use.

We used seconds because a frequency in hertz is a number you can hear,
and because the doubling of an octave links back to Unit 6. The cost is
that the lift, $D$, never came up, and $B$ appeared as $2\pi f$, which
hides it a little.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a wave's amplitude $A$, frequency $f$ and period $T$; a note's name, for a frequency; the phase, for how far along a wave starts |
| What is promised? | `wave(amplitude, frequency, time)` promises $A\sin(2\pi f t)$; one period later, a wave is back at the same height |
| What happens when? | turns first, $f \times t$, then radians, then the sine, then the amplitude; a wave half a turn late cancels the one before it |
| What does this space let us do? | time goes on for ever, so a wave can repeat for ever; `math.sin` takes radians; a sine wave is a model of a sound, never the whole of one |

## What we have now

| Term or tool | What it means |
|---|---|
| sine wave | the graph of $y = \sin\theta$: the height of a point going round |
| periodic | repeating the same piece for ever |
| amplitude, $A$ | how far a wave goes from its middle line; for a sound, how loud |
| frequency, $f$, hertz (Hz) | how many times a wave repeats each second |
| alternating current (AC) | a current that swings back and forth; 50 Hz in Ireland |
| period, $T = \frac{1}{f}$ | how long one repeat takes |
| $y = A\sin(2\pi f t)$ | a wave of amplitude $A$ and frequency $f$, at time $t$ |
| `wave(amplitude, frequency, time)` | your toolkit tool: $A\sin(2\pi f t)$ |
| pitch | how high a note sounds, set by its frequency |
| octave | a doubling of the frequency |
| semitone, $2^{1/12}$ | one of 12 equal steps that make an octave |
| phase, phase shift | how far a wave is moved along, as part of a turn; $\cos\theta = \sin(\theta + 90^\circ)$ |
| graph of $\tan\theta$ | periodic every $180^\circ$, with no value at $90^\circ$ |

## Where to read more

The dewlab page
[Sine and cosine waves: amplitude, period and shift](tutorial:sine-and-cosine-waves)
uses the four-letter form, and fits a wave to a year of daylight.
