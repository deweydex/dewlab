# Outline — The Simulation Strand

**Module:** `computational-methods`, **series:** `simulation` — the third
series in that module, after `python-fundamentals` and `matrices`.
**Closes:** `CMPS-LO3` in full, and the randomness half of `CMPS-LO2`.
**Partly closes:** `CMPS-LO6` — the reliability and network-loss half. Its
average-case-analysis half needs `CMPS-LO5`, which the complexity strand has
not been written yet, so this strand deliberately does not claim it.
**Touches:** `CMPS-LO7` (modelling as distinct from simulation) and
`CMPS-LO13` (accuracy, precision, and trusting a number a model produced) —
both named where they arise, neither claimed as taught. They belong to the
modelling strand.
**Attaches to:** probability (`MIT-5.x`, taught in the other module) and
lists and loops, from `python-fundamentals`.

## Why this, and why here

`CMPS-LO3` is the outcome with the widest gap between how hard it sounds and
how little it needs. "Basic computational and numerical methods for computer
simulation" reads like a term of numerical analysis; what it actually asks
for is the idea that you can answer a question by running something many
times and counting, rather than by solving it.

That idea is the one thing in this module that paper genuinely cannot teach.
A student can be *told* that throwing ten thousand random points at a square
estimates π. Watching the estimate wobble, settle, and stay stubbornly wrong
in the fourth decimal place no matter how long it runs is a different kind of
knowing, and it is available here for the price of a Run button.

It also gives the module something it currently lacks: a reason to care about
being wrong. Every tutorial so far produces an answer that is right. A Monte
Carlo estimate is *never* exactly right, and the interesting question stops
being "what is the answer" and becomes "how far off am I likely to be, and
what would it cost to do better." That is `CMPS-LO13`'s whole subject,
arriving through the front door rather than as an essay prompt.

## Where it attaches, and why only there

- **Probability**, from the other module. A reader needs to be comfortable
  that a probability is a proportion, and nothing more than that. The
  strand re-establishes what it needs rather than assuming it, since a
  reader may reach `computational-methods` without having done the maths
  module.
- **Lists and loops**, from `python-fundamentals`. Everything here is a loop
  that accumulates a count. No new language machinery is needed at all,
  which is deliberate: the difficulty should be in the idea, not the syntax.

Nothing downstream depends on it yet. The modelling strand will.

## The shape — four small tutorials

Each is one sitting, following the split-into-single-topics principle the
matrices strand established.

### 1. Leaving It to Chance

Randomness in computing, and the uncomfortable fact underneath it: the
numbers are not random. A reader generates some, then sets a seed and
generates them again, and gets the same ones — which is the moment the word
*pseudo-random* becomes worth having rather than a piece of vocabulary.

Discover-first ordering matters here. The repetition is noticed before it is
named, and the reason it is a feature rather than a bug — an experiment
nobody can re-run is not an experiment — is drawn out of the reader rather
than asserted.

Closes the randomness half of `CMPS-LO2`.

### 2. Counting Darts

The canonical Monte Carlo estimate: points thrown at a square, the fraction
landing inside a quarter-circle, multiplied by four. The reader builds it
from a loop and a counter, watches the estimate move as the count grows, and
plots it settling.

The pedagogical work is in the last third. The estimate does not converge
smoothly, it does not converge to the right answer, and running it ten times
longer buys only about three times less error. None of that is a
disappointment to be apologised for — it is the actual behaviour of the
method, and a reader who has seen it will never mistake a long-running
simulation for an accurate one.

Covers `CMPS-LO3`.

### 3. How Wrong Are We?

The square-root law, met head-on, and then turned on real data.

First half: run the dart estimate many times over and look at the *spread* of
the answers rather than any one of them. The spread halves when the sample
size quadruples, and a reader can see that in a plot before meeting
$1/\sqrt{n}$ as a formula.

Second half, and the first use of a real dataset anywhere in dewlab:
*bootstrap resampling* on `life-expectancy.csv`. Take one country's real
figures, resample them with replacement a few thousand times, and look at how
much the mean moves. This is the same Monte Carlo idea pointed at a question
with no formula behind it — how confident can I be in an average I computed
from limited data — and it is what the method is actually for outside
textbooks.

Needs `data/life-expectancy.yaml` written first (attribution: OWID's
Gapminder/UN/IHME compilation, CC BY 4.0).

Covers `CMPS-LO3`; touches `CMPS-LO13`.

### 4. The Queue

Discrete-event simulation, at the smallest scale that still shows the
phenomenon: customers arriving at random intervals, one server, a queue that
forms and clears. The reader simulates a morning and measures the average
wait.

Then the finding that makes queueing theory worth teaching to computing
students: as the arrival rate approaches the service rate, the average wait
does not rise steadily — it explodes. A server at 90% utilisation is not
"10% worse" than one at 80%. Every reader who has watched a system fall over
under load has met this without knowing it had a name.

Covers `CMPS-LO3` and the reliability half of `CMPS-LO6`; touches
`CMPS-LO7`.

## What this strand deliberately does not do

- **No `numpy` in tutorials 1 and 2.** A vectorised million-point estimate is
  one line and teaches nothing about what the method is doing. The loop comes
  first; `numpy` is introduced in tutorial 3, where the point is running many
  experiments and the loop has become the obstacle rather than the lesson.
- **No random-number-generator internals.** How a Mersenne twister works is a
  genuinely interesting question and is not `CMPS-LO2`'s. Tutorial 1 names
  the idea that an algorithm produces the sequence and moves on.
- **No claim on `CMPS-LO6`'s average-case half**, which needs complexity
  first. The curriculum map should show LO6 as touched here, not covered,
  until the complexity strand lands.
