---
title: "Probability: simple, compound and conditional"
year: "2026-2027"
version: 2026.08.23.2
covers:
  basic-probability:
    covers: [MIT-5.1, MIT-5.6, MIT-5.7]
  compound-events:
    covers: [MIT-5.8]
  simulation-testing-probability-with-code:
    touches: [MIT-5.7]
  conditional-probability:
    covers: [MIT-5.8]
---

# Probability: simple, compound and conditional

*Probability* is the part of mathematics that measures how likely something is to happen. It gives us exact words and numbers for talking about chance. Weather forecasts use it. So do medical tests, and so does machine learning.

A program gives us a second way to find a probability. To *simulate* a random event is to write code that makes the event happen many times, at random, and count the results. We can then compare the count with our calculation.

On this page we:

- calculate the probability of a single event
- combine events with "or", "and" and "not"
- check our answers by simulating coins and cards in Python
- see how knowing one thing changes the probability of another

## Basic probability

An *outcome* is one possible result, such as rolling a 4 on a die. An *event* is a group of outcomes we are interested in, such as rolling an even number.

The probability of an event is a number from 0 to 1. A probability of 0 means the event is impossible. A probability of 1 means it is certain.

A *favourable outcome* is an outcome that makes the event happen. When every outcome is equally likely, we find the probability of an event A in two steps. First, count the favourable outcomes. Then divide by the number of all possible outcomes:

$$P(A) = \frac{\text{number of favourable outcomes}}{\text{total number of outcomes}}$$

Let's try it with a fair coin. There are 2 equally likely outcomes, heads and tails. If the event is "heads", there is 1 favourable outcome. So $P(\text{heads}) = \frac{1}{2} = 0.5$.

Now we try a fair die. There are 6 equally likely outcomes. Only one of them is a 4, so $P(\text{rolling a 4}) = \frac{1}{6}$. Three of them are even (2, 4 and 6), so $P(\text{rolling an even number}) = \frac{3}{6} = \frac{1}{2}$.

### Your turn

1. Before you write any code, decide what your function should do in two special cases. What should happen when the total is 0? What should happen when the favourable count is larger than the total?
2. Write a function `probability(favourable, total)` that calculates a basic probability. Give it a docstring.
3. Try it on the three test cases in the second cell.

```python exec
id: your-turn-1
# Your probability function
```

```python exec
id: your-turn-2
# Test cases
# probability(1, 6)     -> a specific die face
# probability(13, 52)   -> drawing a heart from a deck
# probability(4, 52)    -> drawing an ace
```

## Compound events

A *compound event* is an event made by joining two or more events with words such as "or", "and" and "not". Four rules help us calculate compound events. The table below gives all four. We look at each one in turn.

| Rule | When we use it | The formula |
|---|---|---|
| Complement rule | "not A" | $1 - P(A)$ |
| Addition rule | "A or B", when A and B cannot both happen | $P(A) + P(B)$ |
| General addition rule | "A or B", when A and B can both happen | $P(A) + P(B) - P(A \text{ and } B)$ |
| Multiplication rule | "A and B", when A and B are independent | $P(A) \times P(B)$ |

**The complement rule.** The complement of an event is the event that it does not happen. Its probability is $1 - P(A)$. For example, if there is a 30% chance of rain, there is a $100\% - 30\% = 70\%$ chance of no rain.

**The addition rule.** Two events are *mutually exclusive* when they cannot both happen at the same time. A 2 and a 5 on one roll of a die are mutually exclusive. For mutually exclusive events, we add the probabilities:

$$P(A \text{ or } B) = P(A) + P(B)$$

For example, the probability of rolling a 2 or a 5 on a die is $\frac{1}{6} + \frac{1}{6} = \frac{2}{6} = \frac{1}{3}$.

**The general addition rule.** Some events *can* happen together. A card can be an ace and a heart at the same time: the ace of hearts. We say these events overlap. For events that can overlap, the rule is:

$$P(A \text{ or } B) = P(A) + P(B) - P(A \text{ and } B)$$

Why do we subtract? The ace of hearts is counted once among the aces and once among the hearts. When we subtract $P(A \text{ and } B)$ once, it is counted only once.

What do you think the probability of drawing an ace or a heart is? Make a guess, then run the cell to check.

```python exec
id: compound-events-1
# Card example: probability of drawing an Ace OR a Heart
p_ace = 4 / 52
p_heart = 13 / 52
p_ace_of_hearts = 1 / 52    # the overlap: it's both an ace AND a heart

p_ace_or_heart = p_ace + p_heart - p_ace_of_hearts
print("P(Ace or Heart):", p_ace_or_heart)
print("That's", round(p_ace_or_heart, 4), "or about", round(p_ace_or_heart * 100, 1), "%")
```

There are 4 aces and 13 hearts, but the ace of hearts is in both groups, so there are $4 + 13 - 1 = 16$ cards that are an ace or a heart. $\frac{16}{52}$ is about 30.8%.

**The multiplication rule.** Two events are *independent* when one happening does not change the probability of the other. Two flips of a coin are independent, because the coin does not remember the first flip. For independent events, we multiply the probabilities:

$$P(A \text{ and } B) = P(A) \times P(B)$$

For example, the probability of flipping heads twice in a row is $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$.

Some events are not independent. Suppose we draw a card and keep it out of the deck, then draw a second card. *Without replacement* means we do not put a card back before the next draw. Now the first draw changes what is left for the second one. We still multiply, but the second probability must take the first draw into account:

$$P(\text{two aces in a row}) = \frac{4}{52} \times \frac{3}{51}$$

After we draw one ace, there are 3 aces left among the 51 cards that remain. So the probability is $\frac{4}{52} \times \frac{3}{51} = \frac{12}{2652} = \frac{1}{221}$, which is about 0.0045.

![A tree from 52 cards. The first draw branches into ace, 4 over 52, and
other, 48 over 52. Under ace the next draw is 3 over 51. Under other it is
4 over 51. The ace then ace path is marked.](two-aces-tree.svg)

The formula says $\frac{4}{52} \times \frac{3}{51}$. The tree shows
where each of those numbers comes from.

Look at the two branches of the second draw. Both have 51 on the bottom,
because one card has gone, whichever card it was. The top number is
different. 3 aces are left if the first card was an ace, and 4 if it was
not. This difference is the meaning of "not independent". The first draw
changed the probabilities for the second one.

### Your turn

Here are five questions about one ordinary deck of 52 cards. It has 4 suits of 13 cards: hearts and diamonds are red, and clubs and spades are black. You can use your `probability` function, and the combination functions from
[Counting: factorials, permutations and combinations](tutorial:counting-carefully).

For each question, write your reasoning as a comment first, then the calculation. Mistakes are much easier to see in the reasoning than in the numbers.

1. What is the probability of drawing a face card (Jack, Queen, or King)?
2. What is the probability of drawing a card that is red *and* a face card?
3. What is the probability of drawing a card that is red *or* a face card?
4. If you draw two cards without replacement, what is the probability both are hearts?
5. What is the probability of being dealt a royal flush (A, K, Q, J, 10 all of the same suit) in a 5-card hand?

```python exec
id: your-turn-3
# Your reasoning and calculations for each question

# 1. Face cards

# 2. Red AND face card

# 3. Red OR face card (careful: these overlap!)

# 4. Two hearts without replacement

# 5. Royal flush (hint: how many royal flushes are possible? 
#    how many total 5-card hands are possible?)
```

## Simulation: testing probability with code

Now we can check our calculations with a simulation. If we flip a simulated coin 10,000 times, how often do you expect to see heads?

Python's `random` module has the tools we need. A *module* is a collection of ready-made functions. The line `import random` loads the `random` module, so that we can use its functions. `random.choice()` picks one item at random from a list.

Run the cell to see how close the result is.

```python exec
id: simulation-testing-probability-with-code-1
import random

# Simulate flipping a coin 10,000 times
num_flips = 10000
heads_count = 0

for i in range(num_flips):
    flip = random.choice(["heads", "tails"])
    if flip == "heads":
        heads_count = heads_count + 1

proportion = heads_count / num_flips
print("Heads:", heads_count, "out of", num_flips)
print("Proportion:", round(proportion, 4))
print("Expected:   0.5")
```

Did you get exactly 0.5? Probably not, but it should be close. Run the cell again. The result changes each time.

A *trial* is one run of a random event. Here, one trial is one flip of the coin.

The more trials we run, the closer the proportion usually gets to the true probability. This is called the *law of large numbers*.

### Your turn

1. Write a function `simulate_coin_flips(num_trials)` that returns the proportion of heads.
2. Call it with 100 trials, then 1,000, then 10,000, then 100,000.

What happens to the proportion as the number of trials grows? How fast does it change?

```python exec
id: your-turn-4
# Your simulate_coin_flips function
```

```python exec
id: your-turn-5
# Run with increasing numbers of trials
```

### Simulating card draws

Next we simulate the card probabilities we calculated earlier. First we need a deck of cards in Python.

In the cell below, each card is a pair of values in round brackets, such as `("A", "Hearts")`. Python calls a pair like this a tuple. A tuple works like a list, but we cannot change it after we make it. What do you think the first five cards will be?

```python exec
id: simulating-card-draws-1
def make_deck():
    """Create a standard 52-card deck as a list of (rank, suit) tuples."""
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    return deck

deck = make_deck()
print("Deck size:", len(deck))
print("First 5 cards:", deck[:5])
print("Last 5 cards:", deck[-5:])
```

### Your turn

1. Write a function `simulate_draw(num_trials)`. Each trial shuffles the deck and looks at the top card.
2. Count how often the top card is an ace or a heart, and return the proportion.
3. Compare it with the probability you calculated earlier.

How close does the simulation get?

**Hint:** `random.shuffle(deck)` shuffles the list. It changes the list itself, and returns nothing. `deck[0]` is the top card. The card's rank is `deck[0][0]` and its suit is `deck[0][1]`.

```python exec
id: your-turn-6
# Your simulate_draw function
```

```python exec
id: your-turn-7
# Compare simulation to calculation
```

### A more complex simulation

How could you simulate drawing two cards *without replacement*, and count how often both are hearts? The hard part is "without replacement". The second card must come from the cards that are left. How close does your simulation come to your calculation?

If you have time, try dealing 5-card hands and counting the royal flushes. A royal flush is so rare that it takes millions of trials to see even one. When a simulation finds nothing, that tells you something too. It shows how rare the event is.

```python exec
id: a-more-complex-simulation-1
# Your two-hearts simulation
```

```python exec
id: a-more-complex-simulation-2
# Optional: royal flush simulation (this may take a while to run!)
```

## Conditional probability

Sometimes the probability of an event depends on something we already know. Suppose we have drawn one heart and kept it out of the deck. What is the probability that the next card is a heart? There are 12 hearts left among 51 cards, so it is $\frac{12}{51}$. It is no longer $\frac{13}{52}$.

A *conditional probability* is the probability of an event B when we know that another event A has happened. We write it $P(B|A)$, and read it as "the probability of B given A". In words, the formula says: out of the times when A happens, what share of them does B happen too?

$$P(B|A) = \frac{P(A \text{ and } B)}{P(A)}$$

Here is one worked number. Two cards are drawn without replacement. Let A be "the first card is a heart" and B be "the second card is a heart". Then $P(A \text{ and } B) = \frac{13}{52} \times \frac{12}{51}$ and $P(A) = \frac{13}{52}$. If we divide, we get $P(B|A) = \frac{12}{51}$, the same answer as before.

We only meet the idea here, without going deeper. It is still worth knowing. A rule called Bayes' theorem is built on conditional probability, and machine learning uses it all the time.

### Your turn

You draw one card and see that it is red. What is the probability that it is a heart?

1. First, make a guess without the formula. How many red cards are there, and how many of them are hearts?
2. Then check your guess with the formula.

```python exec
id: your-turn-8
# Your reasoning and calculation
```

## Reflection

We have met the main rules of probability: the complement rule, the addition rules and the multiplication rule. We have also used simulation to check our calculations.

Simulation is more than a way to learn. Sometimes a problem is too complicated to calculate exactly. Then people run it a million times and count. This method has a name: *Monte Carlo simulation*.

Calculation and simulation work well together. First we calculate a probability, then we simulate to check it. If they disagree, there is a mistake to find, and we learn something when we find it. If they agree, that is good evidence, but it is not proof. A simulation can be built on the same misreading of the problem as the calculation, and then the two agree on the wrong answer.

In the next tutorial, [The Monty Hall problem: three doors and a simulation](tutorial:three-doors), we use both on a famous puzzle.

What was most surprising about the relationship between calculation and simulation?

## Where to read more

3Blue1Brown (2020). *Bayes theorem, the geometry of changing beliefs.*
<https://www.youtube.com/watch?v=HZGCoVF3YvM>. It draws conditional probability
as areas. It is the picture that makes the medical-test result in problem 16 of the
[practice page](tutorial:what-are-the-chances-practice) stop being surprising.

StatQuest with Josh Starmer (2017). *Probability is not Likelihood.*
<https://www.youtube.com/watch?v=pYxNSUDSFH4>. It explains a difference this
tutorial does not cover. That difference matters as soon as you study statistics
properly.

Numberphile (2016). *Monty Hall Problem.*
<https://www.youtube.com/watch?v=4Lb-6rxZxx0>. It shows the classic worked
argument. Watch it after you simulate the problem, not before.

Mlodinow, L. (2008). *The Drunkard's Walk: How Randomness Rules Our Lives.*
Pantheon. It is easy to read, and unusually good on why human intuition about
probability is so unreliable.

Python Software Foundation. *`random` — Generate pseudo-random numbers.*
<https://docs.python.org/3/library/random.html>. Look in particular at the
difference between `random.choice` and `random.sample`. It is the difference
between drawing with and without replacement.
