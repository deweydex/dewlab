---
title: "Make it: a chart that tells the truth, and one that lies"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  exoplanets: Planets around other stars, and the ways they were found.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  book-characters: The people in six novels, chapter by chapter.
  games-of-chance: Dice, cards and coins, and the games people play with them.
datasets: [exoplanets, dinosaur-genera, dinosaur-finds, book-characters]
---

# Make it: a chart that tells the truth, and one that lies

This series counted, worked out chances, summed up data and drew it. It
ended with the ways a chart can mislead using only true numbers. Now you
make two charts from the same data in your world: one that tells the
truth about it, and one that lies. Then you write the sentence a
newspaper might print under each, and one reason each sentence could be
wrong, the true one included.

## A first step

In every world, the first step is the same. Take two numbers from your
world's data, and draw them twice, side by side: once with the axis
starting at zero, once with it cut. Here are the planets announced in
2024 and 2025. Change them for two numbers of your own.

```python exec
id: a-first-step-1
import matplotlib.pyplot as plt

labels = ["2024", "2025"]
values = [260, 245]

fig, (true_chart, false_chart) = plt.subplots(1, 2, figsize=(9, 4))
true_chart.bar(labels, values)
true_chart.set_title("Axis from zero")
false_chart.bar(labels, values)
false_chart.set_ylim(240, max(values) + 2)
false_chart.set_title("Axis cut")
```

Once the two charts disagree about the same two numbers, you have made a
chart that lies. Everything after this is yours to decide.

## Make it yours

For your world, make:

1. **A chart that tells the truth.** Choose the chart type for the
   question, and give it a title, labels with units, and a line saying
   where the data came from.
2. **A chart that lies**, from the same data, with every number in it
   true. Use one trick from the Charts page, or one of your own.
3. **Two sentences a newspaper might print**, one under each chart.
4. **One reason each sentence could be wrong.** For the lying chart this
   is easy. For the true one, think about who is missing from the data,
   how it was sampled, whether something else could explain the pattern,
   and whether chance could have made it.

<div class="dl-world" data-world="exoplanets">

Some questions the planets could answer: how the ways of finding planets
have changed; whether new planets are further away than old ones; what
sizes planets come in. Some ways to lie about them: a window that starts
at Kepler's great year, 2016; a size chart that leaves out the planets
whose radius was estimated; a log axis that nobody mentions.

```python exec
id: make-it-yours-1--exoplanets
import matplotlib.pyplot as plt

planets = await load_csv("exoplanets.csv")
print(planets.columns.tolist())
print(len(planets), "planets")
```

</div>

<div class="dl-world" data-world="dinosaurs">

Some questions the fossils could answer: how many new dinosaurs are
named each decade; where on Earth fossils are found; which periods the
finds come from. Some ways to lie about them: a last decade that is not
over yet; a map of finds presented as a map of where dinosaurs lived; one
country's count beside another's with the axis cut.

```python exec
id: make-it-yours-1--dinosaurs
import matplotlib.pyplot as plt

genera = await load_csv("dinosaur-genera.csv")
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)
print(genera.columns.tolist())
print(finds.columns.tolist())
```

</div>

<div class="dl-world" data-world="book-characters">

Some questions the novels could answer: when a character is on stage;
who is named most in each book; how long the chapters are. Some ways to
lie about them: counting names and calling it importance, when a narrator
says "I"; one chapter chosen to stand for a whole book; two books
compared on different scales.

```python exec
id: make-it-yours-1--book-characters
import matplotlib.pyplot as plt

characters = await load_csv("book-characters.csv")
print(list(characters.book.unique()))
print(characters.head())
```

</div>

<div class="dl-world" data-world="games-of-chance">

Design a game with dice or cards, play it thousands of times, and chart
who wins. Some questions: is it fair, and how many games does it take to
tell? Some ways to lie about it: a hundred games presented as proof; a
rule that sounds like a boundary and hides the commonest result, like
"7 or more"; the lucky run cut out of a long record.

```python exec
id: make-it-yours-1--games-of-chance
import random
import matplotlib.pyplot as plt


def play_once():
    """One game: say whether the first player won. Change the rule."""
    total = random.randint(1, 6) + random.randint(1, 6)
    return total >= 7


wins = 0
for game in range(10_000):
    if play_once():
        wins = wins + 1
print("The first player won", wins, "of 10,000 games")
```

</div>

## If you want more

- Swap charts with somebody without saying which one lies. Can they find
  the trick, and say which sentence it supports?
- Can you make a lying chart that is harder to catch: no cut axis, no
  missing labels, only a choice of what to include?
- Add something from a "go further" section: a box plot of two groups, or
  the means of many samples, to show how far a small sample can wander.
- Find a chart in a newspaper or online, and write one reason it could
  be wrong.

## Show somebody

Show your two charts to somebody, or write a few lines for yourself:

- What question does your true chart answer, and why that kind of chart?
- Which trick did your lying chart use, and what would give it away?
- Which of your two "reasons it could be wrong" was harder to find, and
  why?
