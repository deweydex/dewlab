---
title: "Capstone project: choose a brief"
year: "2026-2027"
version: 2026.09.27.2
datasets: [daylight, dublin-tides, treasure-island]
worlds:
  images-and-pixels: Pictures as grids of numbers. Blur them, find their edges, or draw a fractal.
  sound-and-waves: Notes and chords made from sine waves, an echo, and a tune you can save and play.
  codes-and-secrets: Ciphers, a program that breaks them, and codes that notice their own mistakes.
  simulations-and-games: A small world that follows rules, such as living cells, foxes and rabbits, or a game.
  electronics: A circuit bench in code, with a capacitor that fills and empties and a light that blinks.
  machine-learning: A program that learns from examples, with the pages of the machine learning course.
  sky-and-sea: Daylight and tides from real measurements, and the moment they change fastest.
---

# Capstone project: choose a brief

A *capstone* is the last project of a course: a piece of work that
uses all of it. A *brief* is a description of a piece of work: what to
make, and questions to think about while you make it. This page has 7
briefs, and you choose one.

Each brief is one of the worlds in the choice at the top of this page.
Each one uses programming, data and algebra, and most use trigonometry
or calculus too. Each one starts small, with a few lines of Python that
already run, and it can grow as far as you want to take it. Read one, or
switch between them and read them all before you choose.

## How every brief works

**On your own or in a group.** Every brief has two versions. The
individual version is for one person. The group version is for 2 to 4
people, and gives each person a part of their own. How your class runs
the project is your teacher's decision: whether you work alone or in a
group, the dates, and what you give your teacher at the end.

**Three milestones.** A *milestone* is a point in a project where one
part is finished and works. Every brief has the same three:

1. **A first working piece.** It is small, and it runs.
2. **Something that grows.** The first piece becomes bigger or better,
   often with an idea from another part of the course.
3. **Something shared.** Another person uses it, reads it or listens to
   it, and tells you what they noticed.

**A starter.** Each brief has a starter: a few lines of Python that
already run. The button under it opens a copy in the Notebook, beside
your other work. Change it, break it, and make it yours.

**Questions, not marks.** This page has no marking scheme. Each brief
ends with questions to think about at each milestone, alone or with
the people you work with.

## Your brief

<div class="dl-world" data-world="images-and-pixels">

### Images and pixels

**What you make.** A picture on a screen is a grid of numbers, one for
each small square, or *pixel*. You make programs that change those
numbers: a filter that blurs a picture or finds its edges, a picture
drawn from a rule, or a fractal.

**On your own.** Make 3 filters, and show each one on the same picture,
before and after.

**In a group.** Each person makes one filter, as a function that takes a
grid and returns a new grid. Then the group joins the filters into one
program that can use them in any order. Does the order change the
result?

**Milestones.**

1. The starter draws a pattern from the rule `(x * y) % 256`, and blurs
   it. Change the rule and see what appears. Can you make a pattern you
   did not expect?
2. Make it grow. Here are three ways:
   - A filter that finds edges. An edge is where a pixel is very
     different from the pixel beside it, so an edge is a large slope.
   - A fractal, such as the Mandelbrot set, drawn with complex numbers.
   - A smaller way to store a picture. A row of 20 white pixels could be
     stored as "white, 20". How much smaller is your picture then?
3. Share a gallery of before-and-after pictures. Under each one, write
   one sentence that says what the filter did to the numbers.

**The maths in it.**

- A picture is a list of lists, from [Comprehensions, grids and
  aliasing](tutorial:comprehensions-and-grids).
- A blur is an average, from [Statistics: averages, spread and
  frequency](tutorial:making-sense-of-data).
- An edge is a rate of change, from [Derivatives: the rate of change of
  a curve](tutorial:rates-of-change).
- The Mandelbrot set squares a complex number again and again, from
  [Complex numbers: roots that are not real](tutorial:complex-roots).
- To rotate a picture, each pixel moves round a circle, as on [The
  unit circle: sine, cosine and tangent](tutorial:the-unit-circle).

```python challenge
import matplotlib.pyplot as plt

# A picture is a grid of numbers: 0 is black, and 255 is white.
size = 64
picture = [[(x * y) % 256 for x in range(size)] for y in range(size)]


def blur(grid):
    """Each pixel becomes the average of itself and the pixels around it."""
    height = len(grid)
    width = len(grid[0])
    result = []
    for y in range(height):
        row = []
        for x in range(width):
            total = 0
            count = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if 0 <= y + dy < height and 0 <= x + dx < width:
                        total = total + grid[y + dy][x + dx]
                        count = count + 1
            row.append(total / count)
        result.append(row)
    return result


figure, (left, right) = plt.subplots(1, 2)
left.imshow(picture, cmap="gray", vmin=0, vmax=255)
left.set_title("the pattern")
right.imshow(blur(picture), cmap="gray", vmin=0, vmax=255)
right.set_title("blurred")
```

**Questions to think about.**

- A blur makes a picture softer. Can a program make it sharp again? What
  was lost?
- Which filter surprised you most? What did it do to the numbers?

</div>

<div class="dl-world" data-world="sound-and-waves">

### Sound and waves

**What you make.** A sound is a wave, and a computer stores it as a
long list of numbers, called *samples*. You make sounds from sine waves:
notes, chords, an echo, and perhaps a short tune. You draw each sound,
and play it.

**On your own.** Make a tune of at least 8 notes that ends on a chord,
and draw its wave.

**In a group.** One person makes the notes, one makes the effects, such
as an echo or a fade, and one writes the tune. First, the group agrees
how a sound is stored: a list of samples between -1 and 1, at the same
number of samples each second.

**Milestones.**

1. The starter makes the note A, 440 vibrations a second, and a chord of
   3 notes, and draws both. Change the notes. Look at the chord's
   picture: it repeats itself 110 times a second. Why 110?
2. Make it grow. Here are three ways:
   - An echo: the sound added to itself, a little later and quieter.
   - A tune, from a list of notes and how long each one lasts.
   - A question about the samples. What happens to a note of 660
     vibrations a second when `rate` is only 1000? Draw it, and listen
     to it.
3. Share your tune with someone who listens to it and looks at its
   picture. Can they hear the parts that they can see?

**Hearing it.** `play(samples, rate)` puts a player under the cell.
Press play to hear the sound. A sample beyond -1 or 1 is cut to fit, and
a line under the player says how many were. Cut samples make a sound
crackle.

**The maths in it.**

- Each note is a sine wave, from [Sine and cosine waves: amplitude,
  period and shift](tutorial:sine-and-cosine-waves). A louder note has a
  bigger amplitude, and a higher note has a shorter period.
- A note twice as high has twice the frequency. On a piano, 12 steps
  take a note to the one twice as high, and each step multiplies the
  frequency by $2^{1/12}$, a fractional power, from [Number types,
  powers and logarithms](tutorial:numbers-and-their-families). The
  starter's 550 and 660 are close to 2 of these notes.
- Where a wave changes fastest is its slope, from [The slope of a wave:
  how fast daylight and tides change](tutorial:the-slope-of-a-wave).

```python challenge
import math
import matplotlib.pyplot as plt

rate = 8000    # samples in each second of sound


def note(frequency, seconds):
    """A sine wave: a list of samples, each between -1 and 1."""
    count = int(rate * seconds)
    return [math.sin(2 * math.pi * frequency * n / rate) for n in range(count)]


a = note(440, 2)
# A chord: 3 notes added, then divided by 3 so it stays between -1 and 1.
chord = [(x + y + z) / 3 for x, y, z in zip(note(440, 2), note(550, 2), note(660, 2))]
play(a, rate, label="one note")
play(chord, rate, label="a chord")

plt.plot(a[:80], label="one note, 440 Hz")
plt.plot(chord[:80], label="a chord: 440, 550 and 660 Hz")
plt.xlabel("sample")
plt.legend()
```

**Questions to think about.**

- Which sound was hardest to make? What did its picture look like?
- A real piano note is not a pure sine wave. What would you add to make
  your notes sound more like one?

</div>

<div class="dl-world" data-world="codes-and-secrets">

### Codes and secrets

**What you make.** A cipher hides a message, and a program that breaks
it finds the message without the key. You make both. Then you can make
codes that notice when a message was damaged, or that make a message
shorter.

**On your own.** Make a cipher of your own, and a program that breaks
the starter's cipher. Then make a harder cipher, and try to break that
one too.

**In a group.** Half the group makes ciphers, and the other half breaks
them. Then the halves swap. Each cipher comes with a message of a few
sentences.

**Milestones.**

1. The starter hides a message with a shift of 11 letters. Then it tries
   all 26 shifts, and keeps the one whose result has the most common
   English letters. Try messages of your own. How short can a message be
   before the program chooses the wrong shift?
2. Make it grow. Here are three ways:
   - A cipher where each letter is replaced by any other letter, not
     by the letter 11 places along. Letter counts break it too, but
     more slowly.
   - A check digit, like the last digit of a book's ISBN. Which
     mistakes does it notice, and which does it miss?
   - A program that makes a message shorter, by storing repeats once.
3. Swap coded messages with another person or group, and break theirs.
   Afterwards, show each other how you did it.

If you did the secret messages challenge on [How programming languages
came to be](tutorial:how-we-got-here), you can start from your own
program instead of the starter.

**The maths in it.**

- A shift has 26 keys. A cipher where each letter can be replaced by
  any other has 26 factorial, about $4 \times 10^{26}$, from [Counting:
  factorials, permutations and combinations](tutorial:counting-carefully).
  Nobody tries them all.
- Letter counts are chances, from [Probability: simple, compound and
  conditional](tutorial:what-are-the-chances).
- Undoing a cipher is solving for the letter you started with, as on
  [Rearranging formulae: changing the subject](tutorial:rearranging-formulae).
- A check that a count is even or odd is logic, from [Logic: truth
  tables, XOR and De Morgan's laws](tutorial:logic-and-truth).

```python challenge
def shift(text, key):
    """Move each capital letter `key` places along the alphabet."""
    result = ""
    for character in text:
        if character.isupper():
            place = (ord(character) - ord("A") + key) % 26
            result = result + chr(ord("A") + place)
        else:
            result = result + character
    return result


def score(text):
    """How many times E, T, A, O, I and N, English's commonest letters, appear."""
    return sum(text.count(letter) for letter in "ETAOIN")


secret = shift("MEET ME AT THE OLD BRIDGE AT NOON", 11)
print(secret)

# Try every key, and keep the one whose result looks most like English.
best_key = 0
for key in range(26):
    if score(shift(secret, -key)) > score(shift(secret, -best_key)):
        best_key = key
print(best_key, shift(secret, -best_key))
```

**Questions to think about.**

- What made a cipher hard to break? Was it the key, or the message?
- Where did your program need a person's help, and why?

</div>

<div class="dl-world" data-world="simulations-and-games">

### Simulations and games

**What you make.** A simulation is a small world that follows rules and
runs by itself. You make one: cells that live and die, foxes and
rabbits, a moon going round a planet, a game where players take turns,
or a map made by chance.

**On your own.** Make one simulation, with a picture of what it does
over time, and one question that it answers.

**In a group.** Make one world together, where each person owns one
part: the rules, the pictures, or the questions it answers. Or make a
small game where players take turns, and each person writes one kind of
player.

**Milestones.**

1. The starter runs John Conway's Game of Life. A cell with 3 living
   neighbours comes to life, and a living cell with 2 or 3 stays alive.
   The starter's shape, a *glider*, moves one square down and one
   square to the right every 4 steps. Try shapes of your own. What
   happens to a row of 3? To a square of 4?
2. Make it grow. Here are three ways:
   - Foxes and rabbits. Each year, the rabbits increase, the foxes eat
     some of them, and foxes without food die. How do the two numbers
     change together?
   - A moon that goes round a planet, one small step at a time.
   - A map made by chance, with land, sea and mountains, or a game for
     2 players.
3. Another person runs your world, changes one rule, and tells you what
   happened. Did you expect it?

**The maths in it.**

- The world is a grid, from [Comprehensions, grids and
  aliasing](tutorial:comprehensions-and-grids), and its rules are logic,
  from [Logic: truth tables, XOR and De Morgan's
  laws](tutorial:logic-and-truth).
- Foxes and rabbits change at a rate that depends on how many there are,
  from [Derivatives: the rate of change of a
  curve](tutorial:rates-of-change).
- An orbit is the unit circle made bigger, from [The unit circle: sine,
  cosine and tangent](tutorial:the-unit-circle).
- A map or a game made by chance uses [Probability: simple, compound and
  conditional](tutorial:what-are-the-chances).

```python challenge
size = 10
alive = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}    # a glider


def neighbours(cell):
    """The 8 cells around this one. The grid wraps round at its edges."""
    x, y = cell
    around = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx, dy) != (0, 0):
                around.append(((x + dx) % size, (y + dy) % size))
    return around


def step(alive):
    """The next generation, by John Conway's rules."""
    counts = {}
    for cell in alive:
        for other in neighbours(cell):
            counts[other] = counts.get(other, 0) + 1
    born = {cell for cell, count in counts.items() if count == 3}
    stays = {cell for cell in alive if counts.get(cell, 0) == 2}
    return born | stays


def draw(alive):
    for y in range(size):
        print("".join("#" if (x, y) in alive else "." for x in range(size)))
    print()


for generation in range(5):
    draw(alive)
    alive = step(alive)
```

**Questions to think about.**

- Which rule changed your world the most when you changed it?
- Is your simulation like the real thing? Where is it different?

</div>

<div class="dl-world" data-world="electronics">

### Electronics

**What you make.** A circuit bench in code. A *capacitor* stores
electric charge, and a resistor limits the current that fills it. You
model a capacitor that fills and empties, and then a light that blinks.
You do not need real parts. If you have some, you can compare them with
your model.

**On your own.** Make a model of a capacitor that fills through a
resistor. Then make a light that blinks at a speed you choose.

**In a group.** One person models the filling, one models the emptying,
and one joins them into a blinking light. If someone has a kit with a
chip called a 555 timer, they can build the real circuit and time its
blinks.

**Milestones.**

1. The starter fills a capacitor in two ways: step by step, and with a
   formula. After 1 second, the step-by-step model says 3.17 volts, and
   the formula says 3.161. Why do they differ? What happens to the
   difference when `step` is smaller?
2. Make it grow. Here are two ways:
   - Empty the capacitor through the resistor. The current now flows the
     other way.
   - Make a light blink. The capacitor fills to 2/3 of the supply, and
     then empties to 1/3, again and again. This is the idea behind the
     555 timer. How long does one blink take? Can you choose a resistor
     so that it blinks once a second?
3. Share a picture of your blinking light's voltage, with a table of
   resistors and blink times that another person could use to build it.

**The maths in it.**

- The current is the voltage divided by the resistance, and that
  formula can be rearranged, as on [Rearranging formulae: changing the
  subject](tutorial:rearranging-formulae).
- Each step adds the rate of change times a small time, so the model is
  a slope, from [Derivatives: the rate of change of a
  curve](tutorial:rates-of-change). [Time steps: simulating a falling
  ball, one step at a time](tutorial:stepping-forward-in-time), a page
  from another course, does the same for a falling ball.
- The formula uses the number $e$, which [Limits: getting closer without
  arriving](tutorial:approaching-a-limit) meets in its practice
  problems. The time for one blink has a logarithm in it, from [Number
  types, powers and logarithms](tutorial:numbers-and-their-families).

```python challenge
import math
import matplotlib.pyplot as plt

supply = 5.0            # volts, from the battery
resistance = 10_000     # ohms
capacitance = 0.0001    # farads: 100 microfarads
step = 0.01             # seconds

# Step by step: the current fills the capacitor, and the fuller it is,
# the smaller the current. This is Ohm's law, current = volts / resistance.
volts = [0.0]
for _ in range(500):
    current = (supply - volts[-1]) / resistance
    volts.append(volts[-1] + current / capacitance * step)

# The formula that calculus gives, to compare with.
times = [n * step for n in range(501)]
formula = [supply * (1 - math.exp(-t / (resistance * capacitance))) for t in times]

print(round(volts[100], 3), round(formula[100], 3))
plt.plot(times, volts, label="step by step")
plt.plot(times, formula, "--", label="formula")
plt.xlabel("seconds")
plt.ylabel("volts across the capacitor")
plt.legend()
```

**Questions to think about.**

- Where did your model and the formula disagree, and which did you
  trust?
- If you built the real circuit, how close was it to your model? What
  might explain the difference?

</div>

<div class="dl-world" data-world="machine-learning">

### Machine learning

**What you make.** A program that learns from examples. The machine
learning course has the pages for it. This brief is a small project that
uses them, starting with a chain that writes in the style of a book.

**On your own.** Make a chain that writes in the style of a book you
choose. Then test it: can a friend tell your chain's sentences from the
book's own?

**In a group.** Each person makes a chain from a different book. Then
the group mixes real sentences with made ones, and tests other people.
Which sentences are real, and which book is each one from?

**Milestones.**

1. The starter makes a chain from *Treasure Island* and writes 15 words.
   Change the book, or the first word. [A Markov chain from a whole
   book: a dictionary of dictionaries](tutorial:a-chain-reads-a-book)
   explains how it works.
2. Make it grow. Here are two ways:
   - A chain that remembers 2 words, not 1, from [N-grams: a Markov
     chain that remembers more words](tutorial:how-much-it-remembers).
   - A model that learns to tell two kinds of picture apart, from [The
     perceptron: a model that learns from its
     mistakes](tutorial:a-model-that-corrects-itself) and [Classifying
     pictures: one perceptron for each
     class](tutorial:telling-many-pictures-apart).
3. Run your test with other people. How often could they tell? Before
   you share, read [Limits and judgement: testing what a model can
   do](tutorial:limits-and-judgement).

**The maths in it.**

- The chain chooses each word with a chance that comes from counts, as
  on [Probability: simple, compound and
  conditional](tutorial:what-are-the-chances).
- A perceptron with two inputs divides its examples with a straight
  line, from [Straight lines: slope, and the line that breaks the
  formula](tutorial:slope-and-lines).
- A test of your chain is a small experiment, and its result is data,
  as on [Statistics: averages, spread and
  frequency](tutorial:making-sense-of-data).

```python challenge
import random

raw = await load_text("treasure-island.txt")
words = raw.split()

# For each word, every word that comes straight after it in the book.
chain = {}
for word, following in zip(words, words[1:]):
    chain.setdefault(word, []).append(following)

random.seed(1)
word = "The"
sentence = [word]
for _ in range(15):
    if word not in chain:
        break
    word = random.choice(chain[word])
    sentence.append(word)
print(" ".join(sentence))
```

**Questions to think about.**

- When people could tell, what told them that a sentence came from
  your chain?
- Your chain copies a book. Whose words are they when it writes?

</div>

<div class="dl-world" data-world="sky-and-sea">

### Sky and sea

**What you make.** A study of daylight or tides from real measurements:
how they change, when they change fastest, and how well a wave
describes them. The data has the hours of daylight on every day of 2026
in Reykjavik, Dublin, Accra and Cape Town, and the height of the tide at
Dublin Port every hour of March 2026.

**On your own.** Choose daylight in one place, or the tides. Find when
it changes fastest in two ways: from the data, and from a wave that
fits the data.

**In a group.** Each person takes one place, from Reykjavik in the far
north to Cape Town in the south. Then compare the four. Where does
daylight change fastest, and when?

**Milestones.**

1. The starter finds the biggest change in Dublin's daylight from one
   day to the next. It is 5.4 minutes, and 6 different days share it.
   Why do 6 days share it? Look at the lower picture, and at how the
   hours are written in the data.
2. Make it grow. Here are two ways:
   - Fit a wave to the year, as on [Sine and cosine waves: amplitude,
     period and shift](tutorial:sine-and-cosine-waves). Where is its
     slope greatest? Does that agree with the data?
   - Do the same for the tides, in `dublin-tides.csv`, as on [The
     slope of a wave: how fast daylight and tides
     change](tutorial:the-slope-of-a-wave). Is the water rising fastest
     at high tide, at low tide, or between them?
3. Share one picture with all four places on it, and one sentence about
   each place, for a reader who has never been there.

**The maths in it.**

- Daylight and tides are waves, from [Sine and cosine waves: amplitude,
  period and shift](tutorial:sine-and-cosine-waves).
- The change from one day to the next is a slope, from [Derivatives: the
  rate of change of a curve](tutorial:rates-of-change), and the slope of
  a wave is a wave too, from [The slope of a wave: how fast daylight and
  tides change](tutorial:the-slope-of-a-wave).
- Why the days change at all is on [The seasons: a closer look at the
  Earth and the Sun](tutorial:why-we-have-seasons).

```python challenge
import matplotlib.pyplot as plt

table = await load_csv("daylight.csv")
dublin = table[table["place"] == "Dublin"]
dates = dublin["date"].tolist()
hours = dublin["daylight_hours"].tolist()

# How much longer each day is than the day before: a slope, one day wide.
change = [round(hours[day + 1] - hours[day], 2) for day in range(len(hours) - 1)]
biggest = max(change)
days = [dates[day + 1] for day in range(len(change)) if change[day] == biggest]
print("The biggest change:", round(biggest * 60, 1), "minutes, on", len(days), "days")
print(days)

figure, (top, bottom) = plt.subplots(2, 1, sharex=True)
top.plot(hours)
top.set_ylabel("hours of daylight")
bottom.plot(change)
bottom.set_ylabel("change from the day before")
bottom.set_xlabel("day of 2026")
```

**Questions to think about.**

- The data and the wave gave two answers. Which did you trust more, and
  why?
- What would you need to measure to answer your question better?

</div>

## Looking back

These questions fit every brief. They are for the end of each
milestone, and for the end of the project.

- What did you try that did not work? What did you learn from it?
- Where did you use maths that you did not expect to use?
- What would you add next, with another week?
- Which page of the course did you use most? Which one did you not need?
- If you started again tomorrow, what would you do first?

## Where to read more

<div class="dl-world" data-world="images-and-pixels">

Computerphile. *How Blurs & Filters Work.*
<https://www.youtube.com/watch?v=C_zFhWdM4ic>. Mike Pound shows how a
blur works, one small grid of numbers at a time, as the starter does.

Computerphile. *Finding the Edges (Sobel Operator).*
<https://www.youtube.com/watch?v=uihBwtPIBxM>. The next step after the
blur: a filter that finds edges.

</div>

<div class="dl-world" data-world="sound-and-waves">

3Blue1Brown. *But what is the Fourier Transform? A visual introduction.*
<https://www.youtube.com/watch?v=spUNpyF58BY>. Grant Sanderson shows how
to find the notes inside a sound, which is the opposite of what the
starter does.

</div>

<div class="dl-world" data-world="codes-and-secrets">

3Blue1Brown. *But what are Hamming codes? The origin of error
correction.* <https://www.youtube.com/watch?v=X8jsijhllIA>. A code that
finds and corrects its own mistakes, built from checks of even and odd.

Singh, S. (1999). *The Code Book.* London: Fourth Estate. The history of
ciphers and how people broke them, from ancient Rome to computers.

</div>

<div class="dl-world" data-world="simulations-and-games">

Numberphile. *Inventing Game of Life (John Conway).*
<https://www.youtube.com/watch?v=R9Plq-D1gEk>. John Conway talks about
how he invented the rules the starter uses.

</div>

<div class="dl-world" data-world="electronics">

Ben Eater. *Astable 555 timer - 8-bit computer clock - part 1.*
<https://www.youtube.com/watch?v=kRlSFm519Bo>. A real 555 timer on a
breadboard, making a light blink.

</div>

<div class="dl-world" data-world="machine-learning">

3Blue1Brown. *But what is a neural network? Deep learning chapter 1.*
<https://www.youtube.com/watch?v=aircAruvnKk>. What comes after the
perceptron: many of them, in layers, reading handwritten digits.

</div>

<div class="dl-world" data-world="sky-and-sea">

Marine Institute. *Irish National Tide Gauge Network.*
<https://erddap.marine.ie/erddap/tabledap/IrishNationalTideGaugeNetwork.html>.
The source of the tide data. Its gauges round the coast of Ireland
measure the height of the sea every 5 minutes.

NASA Jet Propulsion Laboratory. *Horizons.*
<https://ssd.jpl.nasa.gov/horizons/>. The source of the daylight data. It
can give the times the Sun rises and sets for any place on Earth.

</div>
