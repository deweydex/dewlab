# Outline — Approaching a Limit

**Closes:** `MIT-3.5` (the limit of a function).
**Goes after:** Angles and Waves.
**Builds on:** Drawing Functions.
**Size:** short — one sitting.

## Why it exists

To make the next tutorial honest. A derivative introduced without a limit is a
rule to memorise; introduced with one, it is a thing the student has watched
happen.

It is also the clearest case in the whole series for a runnable cell over a
page. A limit is a claim about what happens as you get closer, and getting
closer is a loop.

## The shape

### 1. Getting closer

- **Cell:** evaluate `(x**2 - 1) / (x - 1)` at x = 1.1, 1.01, 1.001, 1.0001. The
  answers march towards 2.
- **Cell:** try x = 1. Python raises `ZeroDivisionError`, which is the point,
  not an accident. (And a chance to use the error-reading habit.)
- **Point to make:** the function is not defined at 1, and the limit at 1 is
  still 2. Those two facts are not in conflict, and holding both is the idea.

### 2. From both sides

- **Cell:** approach from below as well as above, printed side by side.
- **Cell:** a function where the two sides disagree — `abs(x) / x` at 0. No
  limit, and the table shows why.

### 3. Seeing it

- **Cell:** plot the function with the hole, using the plotting function from
  Drawing Functions.
- **Point to make:** the graph has a gap you could fill with a single point.
  That is what "the limit exists" looks like.

### 4. Where this is going

- One paragraph, no cell. The slope between two points on a curve, as the two
  points get closer together. Next tutorial.

## Note

Floating point will misbehave if the student pushes close enough — at x =
1 + 1e-16 the answer degrades. Worth meeting deliberately rather than being
surprised by: it ties back to Tutorial 2's data types, and it is honest about
what a computer can and cannot show you about a limit.
