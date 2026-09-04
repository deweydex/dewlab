# What the pair judgements say about the graph

Written by `dev/pair_results.py` from the saved batches in `pairs/`. Nothing here has been applied to `topics.yaml`.

8 saved batches · 291 pairs judged · 582 judgements in total

## Arrows to add

Pairs judged to need each other in one direction, where no chain of
existing arrows already leads from the first to the second. These are
the ones that change the graph.

| Comes first | Comes after | Judgements | Agreed |
|---|---|---|---|
| Lists, grids and trees (was Data structures and recursion) | What a grid of numbers is good for (was Matrices in practice) | 2 | no |
| How an algorithm's cost grows (was Algorithmic complexity) | Problem-solving strategies | 2 | no |
| Powers and logarithms | How a computer counts: base two and base sixteen (was Binary and hexadecimal) | 2 | no |
| Powers and logarithms | Multiplying two brackets together (was Multiplying out to quadratics) | 2 | yes |
| Rearranging formulae | Solving for a range instead of a single value (was Linear inequalities) | 2 | yes |
| Rearranging formulae | Two equations that have to be true at once (was Simultaneous equations) | 2 | yes |
| The unit circle | Degrees and radians | 2 | yes |
| Counting values into bands (was Frequency tables and histograms) | Choosing a display | 2 | yes |
| Averages and spread | Kinds of data | 2 | yes |

## Arrows the graph already gives you

Judged the same way, but a chain of existing arrows already runs from
the first to the second. Drawing these would change nothing. They are
here because they confirm the chain rather than because they add to it.

| Comes first | Comes after | Judgements | Agreed |
|---|---|---|---|
| Computer simulation | How far you can trust a model's numbers (was What a model's numbers are worth) | 2 | yes |
| Expressions and equations | Solving any quadratic, and the answers that are off the number line (was Solving quadratics, including complex roots) | 2 | yes |
| Expressions and equations | Rearranging formulae | 2 | yes |
| Expressions and equations | Multiplying two brackets together (was Multiplying out to quadratics) | 2 | yes |
| Expressions and equations | Taking a quadratic back apart (was Factorising quadratics) | 2 | yes |
| Expanding and simplifying | Solving any quadratic, and the answers that are off the number line (was Solving quadratics, including complex roots) | 2 | yes |
| Expanding and simplifying | Taking a quadratic back apart (was Factorising quadratics) | 2 | yes |
| Multiplying two brackets together (was Multiplying out to quadratics) | Solving any quadratic, and the answers that are off the number line (was Solving quadratics, including complex roots) | 2 | yes |
| Multiplying the choices (was The counting principle) | Choosing when the order matters (was Permutations) | 2 | no |
| Multiplying the choices (was The counting principle) | Choosing when the order does not matter (was Combinations) | 2 | no |
| How many ways to put things in order (was Factorials) | Choosing when the order does not matter (was Combinations) | 2 | yes |

## Arrows the judges did not keep

| Comes first | Comes after | Judgements | Agreed |
|---|---|---|---|
| Problem definition and design | Finding what actually caused the error (was Symptoms versus root cause) | 2 | yes |
| Modular, reusable code | Deploying a program | 2 | yes |
| Expanding and simplifying | Rearranging formulae | 2 | no |
| Multiplying two brackets together (was Multiplying out to quadratics) | The derivative | 2 | yes |
| Taking a quadratic back apart (was Factorising quadratics) | Solving any quadratic, and the answers that are off the number line (was Solving quadratics, including complex roots) | 2 | yes |
| Taking a quadratic back apart (was Factorising quadratics) | Rewriting a curve to find its lowest point (was Completing the square) | 2 | yes |
| Number families | Set operations | 2 | yes |
| Truth tables | Selection and iteration | 2 | yes |
| Functions and inverses | Functions and scope | 2 | yes |
| Graphing functions | What a grid of numbers is good for (was Matrices in practice) | 2 | yes |
| Equations of lines | The unit circle | 2 | yes |
| Counting values into bands (was Frequency tables and histograms) | Averages and spread | 2 | yes |
| Lists and arrays | Counting values into bands (was Frequency tables and histograms) | 2 | no |
| Iterating by index | Cutting a problem in half (was Divide and conquer) | 2 | no |
| The history of programming | Comparing languages | 2 | yes |
| Testing and debugging | Working as a team | 2 | yes |
| Selection and iteration | Documented programs | 2 | yes |
| Selection and iteration | Functions and scope | 2 | yes |
| Documented programs | Problem definition and design | 2 | yes |
| Documented programs | Testing and debugging | 2 | yes |

## Pairs that turn out to be one level

Two topics that each need the other sit at the same level of the
graph. Either they are taught together, or they are one topic under
two names. Neither is a fault to fix.

- The unit circle and Degrees and radians — the arrow between them runs both ways once these judgements go in
- Writing down a sum over a whole list (was Index and sigma notation) and Iterating by index — judges pointed opposite ways, which between them says this (2 judgements)

## Loops of three or more

A loop this long cannot be taught in any order, and teaching the
topics together does not fix it. Each has to be broken.

- Kinds of data → Counting values into bands (was Frequency tables and histograms) → Averages and spread → Kinds of data

## Pairs where one judge saw an arrow and the other did not

- **Lists, grids and trees (was Data structures and recursion)** and **What a grid of numbers is good for (was Matrices in practice)**
  - ruth: Lists, grids and trees (was Data structures and recursion) first
  - tom: unrelated
- **Iterating a model** and **How far you can trust a model's numbers (was What a model's numbers are worth)**
  - ruth: Iterating a model first
  - tom: unrelated
- **Iterating a model** and **Chance, and the random numbers a computer makes (was Probability and information)**
  - ruth: unrelated
  - tom: Chance, and the random numbers a computer makes (was Probability and information) first
- **Iterating a model** and **Computer simulation**
  - ruth: unrelated
  - tom: Computer simulation first
- **How far you can trust a model's numbers (was What a model's numbers are worth)** and **Chance, and the random numbers a computer makes (was Probability and information)**
  - ruth: unrelated
  - tom: Chance, and the random numbers a computer makes (was Probability and information) first
- **How far you can trust a model's numbers (was What a model's numbers are worth)** and **Models, and running a model forward (was Modelling versus simulation)**
  - ruth: unrelated
  - tom: Models, and running a model forward (was Modelling versus simulation) first
- **Chance, and the random numbers a computer makes (was Probability and information)** and **Models, and running a model forward (was Modelling versus simulation)**
  - ruth: unrelated
  - tom: Chance, and the random numbers a computer makes (was Probability and information) first
- **How an algorithm's cost grows (was Algorithmic complexity)** and **Problem-solving strategies**
  - ruth: How an algorithm's cost grows (was Algorithmic complexity) first
  - tom: unrelated
- **Powers and logarithms** and **Solving any quadratic, and the answers that are off the number line (was Solving quadratics, including complex roots)**
  - ruth: unrelated
  - tom: Powers and logarithms first
- **Powers and logarithms** and **How a computer counts: base two and base sixteen (was Binary and hexadecimal)**
  - ruth: Powers and logarithms first
  - tom: unrelated
- **Powers and logarithms** and **Taking a quadratic back apart (was Factorising quadratics)**
  - ruth: unrelated
  - tom: Powers and logarithms first
- **Expanding and simplifying** and **Rearranging formulae**
  - ruth: unrelated
  - tom: Expanding and simplifying first
- **Functions and inverses** and **Algorithms as functions**
  - ruth: Functions and inverses first
  - tom: unrelated
- **Listing outcomes** and **Multiplying the choices (was The counting principle)**
  - ruth: Listing outcomes first
  - tom: unrelated
- **Counting values into bands (was Frequency tables and histograms)** and **Lists and arrays**
  - ruth: unrelated
  - tom: Lists and arrays first
- **Multiplying the choices (was The counting principle)** and **Choosing when the order matters (was Permutations)**
  - ruth: Multiplying the choices (was The counting principle) first
  - tom: unrelated
- **Multiplying the choices (was The counting principle)** and **Choosing when the order does not matter (was Combinations)**
  - ruth: Multiplying the choices (was The counting principle) first
  - tom: unrelated
- **Probability as a scale** and **Combining probabilities**
  - ruth: unrelated
  - tom: Probability as a scale first
- **Cutting a problem in half (was Divide and conquer)** and **Iterating by index**
  - ruth: unrelated
  - tom: Iterating by index first

## Topics with a suggested new name

| Topic | Suggested name |
|---|---|
| Data structures and recursion | Lists, grids and trees |
| Symptoms versus root cause | Finding what actually caused the error |
| Personal attributes in problem-solving | Habits that help when you are stuck |
| What a model's numbers are worth | How far you can trust a model's numbers |
| Probability and information | Chance, and the random numbers a computer makes |
| Matrices in practice | What a grid of numbers is good for |
| Algorithmic complexity | How an algorithm's cost grows |
| Modelling versus simulation | Models, and running a model forward |
| Solving quadratics, including complex roots | Solving any quadratic, and the answers that are off the number line |
| Linear inequalities | Solving for a range instead of a single value |
| Simultaneous equations | Two equations that have to be true at once |
| Binary and hexadecimal | How a computer counts: base two and base sixteen |
| Multiplying out to quadratics | Multiplying two brackets together |
| Factorising quadratics | Taking a quadratic back apart |
| De Morgan's Laws | Turning a negative inside out |
| Completing the square | Rewriting a curve to find its lowest point |
| Limits | What a function is heading towards |
| Rules for differentiating | Shortcuts for finding a derivative |
| Exact trigonometric values | The angles with exact answers |
| Frequency tables and histograms | Counting values into bands |
| The counting principle | Multiplying the choices |
| Factorials | How many ways to put things in order |
| Permutations | Choosing when the order matters |
| Combinations | Choosing when the order does not matter |
| Index and sigma notation | Writing down a sum over a whole list |
| Divide and conquer | Cutting a problem in half |

## Groups

Groups the judges invented:

- How to approach a problem

No topic has been put in a group yet.

## Topics flagged as needing work

- Lists, grids and trees (was Data structures and recursion)
- Habits that help when you are stuck (was Personal attributes in problem-solving)
- Chance, and the random numbers a computer makes (was Probability and information)
- How an algorithm's cost grows (was Algorithmic complexity)
- The instructions a program is built from
- Powers and logarithms
- Solving any quadratic, and the answers that are off the number line (was Solving quadratics, including complex roots)
- Expressions and equations
- Venn diagrams
- Equations of lines
- The angles with exact answers (was Exact trigonometric values)
- Counting values into bands (was Frequency tables and histograms)
- Averages and spread
- Multiplying the choices (was The counting principle)
- Combining probabilities
- Writing down a sum over a whole list (was Index and sigma notation)
- Lists applied to problems
- Working as a team
- Algorithms in the real world

