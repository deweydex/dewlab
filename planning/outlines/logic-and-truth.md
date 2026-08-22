# Outline — Logic and Truth

**Closes:** `MIT-2.4` (truth tables: AND, NOT, OR, XOR), `MIT-2.5` (De Morgan's
Laws).
**Goes after:** Tutorial 16, Sets as Sorted Lists.
**Builds on:** Tutorial 3 (Boolean operators), Tutorial 16 (sets).
**Size:** short.
**Not included:** Venn diagrams — see `planning/curriculum/out-of-scope.yaml`.

## Why it exists, and why here

Students have been writing `and`, `or` and `not` since Tutorial 3 without ever
seeing them laid out. That is the definition of a quiet gap: it looks covered
because the operators are everywhere, and no student could tell you what `not (A
and B)` is equivalent to.

After sets rather than before, because union and intersection give the shape
first and the logic then names it.

## The shape

### 1. Every possible case

- **Cell:** a nested loop over `[True, False]` printing a truth table for `and`.
  Four rows, generated rather than typed.
- **Cell:** the same loop, `or` and `not`.
- **Point to make:** a truth table is not a thing to memorise. It is what you get
  when you try every input, which is a loop the students can already write.

### 2. Exclusive or

- **Cell:** XOR from the operators they have, then compared against `!=` on
  booleans and against `^`.
- **Your turn:** write XOR three different ways and show all three agree over
  every input.

### 3. De Morgan's Laws

- **Cell:** a table with columns for `not (A and B)` and `(not A) or (not B)`.
  Identical columns, every row.
- **Cell:** the second law, same treatment.
- **Point to make:** the loop over all four cases *is* the proof. There are only
  four cases, so exhaustive checking is not a shortcut here — it is complete.

### 4. Where you have already used this

- **Cell:** take a real `if` condition from an earlier tutorial and rewrite it
  with De Morgan. Show the two versions agree on every input.
- **Your turn:** simplify three tangled conditions.
- **Point to make:** this is the readability argument from the Interlude with a
  rule behind it.

### 5. The same shapes, on sets

- **Cell:** complement of a union versus intersection of complements, using the
  set functions from Tutorial 16.
- **Point to make:** De Morgan is one law wearing two costumes. That connection
  is the reason this tutorial sits after sets.

## Note

Exhaustive checking as proof is worth naming out loud. It works here because the
input space is four rows, and it does not work for most claims — a good moment to
say so, since the students will meet "I tested it and it worked" as a habit soon
enough.
