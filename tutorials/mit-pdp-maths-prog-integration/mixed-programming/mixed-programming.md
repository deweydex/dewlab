---
title: "Mixed Problems — Programming"
slug: mixed-programming
practice_across:
  - first-steps
  - storing-and-computing
  - making-decisions
  - repeating-yourself
  - lists-and-sequences
  - finding-things
  - putting-things-in-order
  - building-reusable-tools
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Mixed Problems — Programming

Every problem here needs more than one tutorial. None of them says which, and that is the point: knowing that a problem wants a loop with a condition inside it, or a sort followed by a search, is a different skill from being able to write either.

Answers are folded, and most have more than one good one. Where a problem has a decision in it, the answer says what was decided and why rather than pretending there was only one route.

## Tools

```python exec
id: tools-1
def show(label, value):
    print(f"{label:<28}{value}")


show("this is a scratchpad", "change anything here")
```

## Warm-Up

**1.** Write a function that takes a list of numbers and returns how many are even, how many odd, and how many zero.

<details class="dl-answer"><summary>answer</summary>

```python
def parity_counts(numbers):
    """(even, odd, zero) counts. Zero is counted in both even and zero."""
    even = sum(1 for n in numbers if n % 2 == 0)
    odd = len(numbers) - even
    zero = numbers.count(0)
    return even, odd, zero
```

The decision hiding in the question: is zero even, or is it its own category? It is even, mathematically — it divides by two exactly. So counting it in both is defensible and needs saying, and counting it in neither would leave the three numbers not adding up.

A question that does not say what to do about zero is a question you have to answer yourself and write down.

</details>

**2.** Given a list of exam marks, return the marks that are above the average.

<details class="dl-answer"><summary>answer</summary>

```python
def above_average(marks):
    if not marks:
        return []
    average = sum(marks) / len(marks)
    return [m for m in marks if m > average]
```

Two passes, unavoidably: you cannot know the average until you have seen everything.

The empty case returns an empty list rather than raising, because "which marks are above average" has a sensible answer for no marks and "what is the average" does not.

</details>

**3.** Write a function that returns the second-largest number in a list.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What should `[5, 5, 3]` give — 5 or 3? The question does not say, so decide before writing anything.
2. Getting the distinct values first makes that decision visible in the code rather than hidden in it.
3. Sorting descending puts the answer at index 1.
4. A list of one distinct value has no second largest. What comes back then?

**Think about:** why this problem is really two problems, and which one the specification forgot to answer.

**Try this next:** write `second_smallest`. Can you write one function that does both, taking a direction?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def second_largest(numbers):
    """The second-largest distinct value, or None if there is not one."""
    distinct = sorted(set(numbers), reverse=True)
    return distinct[1] if len(distinct) > 1 else None
```

`[5, 5, 3]` is the case worth deciding about. With `set`, the answer is 3; without it, 5. Both are reasonable readings of "second largest" and they disagree, so the docstring has to say which.

Sorting is n log n where a single pass tracking the top two is n. For a list you can see the end of, the sort is the better code.

</details>

## Loops and Decisions Together

**4.** FizzBuzz: print the numbers 1 to 100, but `Fizz` for multiples of 3, `Buzz` for multiples of 5, and `FizzBuzz` for both.

<details class="dl-answer"><summary>answer</summary>

```python
for n in range(1, 101):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

The order is the whole problem. Test for 15 first, or a multiple of fifteen matches `n % 3` and prints `Fizz`.

An alternative that avoids the ordering trap entirely:

```python
word = ("Fizz" if n % 3 == 0 else "") + ("Buzz" if n % 5 == 0 else "")
print(word or n)
```

`word or n` uses the fact that an empty string is falsy. Neat, and slightly harder to read — which is a real trade rather than a clear win.

</details>

**5.** Count how many numbers below 1,000 are divisible by 3 or 5, and add them up.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Build the list of numbers below 1000 divisible by 3 or by 5, and count it.
2. Now do it without a loop. The multiples of 3 are 3, 6, 9 … — that is 3 times the whole numbers up to 333, and you know the sum of 1 to n.
3. Do the same for the multiples of 5.
4. Adding those two totals counts some numbers twice. Which ones, and what do you do about them?

**Think about:** the numbers counted twice are exactly the multiples of 15. Where have you seen "add both, subtract the overlap" before?

**Try this next:** the same question with a limit of a billion. The loop takes a while; the formula does not.

</details>

<details class="dl-answer"><summary>answer</summary>

466 numbers, adding to 233,168.

```python
hits = [n for n in range(1, 1000) if n % 3 == 0 or n % 5 == 0]
print(len(hits), sum(hits))
```

Worth doing a second way, without a loop: the multiples of 3 sum to $3 \times \frac{333 \times 334}{2}$, the multiples of 5 to $5 \times \frac{199 \times 200}{2}$, and the multiples of 15 have been counted twice and come off once. That gives 233,168 as well, in no time at all for any limit you like.

Inclusion–exclusion turning up in a programming exercise is not a coincidence — it is the same idea as the union of two sets.

</details>

**6.** A shop gives 10% off orders over €50, and a further €5 off if the customer has a loyalty card. Write a function returning the price to pay.

<details class="dl-answer"><summary>answer</summary>

```python
def to_pay(total, loyalty=False):
    """The price after the over-fifty discount and the loyalty deduction."""
    if total > 50:
        total = total * 0.9
    if loyalty:
        total = max(0, total - 5)
    return round(total, 2)
```

Three decisions the question did not make. Is €50 exactly "over 50"? Taken as no. Does the loyalty fiver come off before or after the percentage? Taken as after, which is worse for the customer. Can the total go below zero? Guarded, because a shop that pays you is not what anybody meant.

Real specifications are like this. Writing the assumptions in the docstring is what turns a guess into a decision somebody can correct.

</details>

**7.** Write a function that takes a sentence and returns the longest word, ignoring punctuation and case.

<details class="dl-answer"><summary>answer</summary>

```python
def longest_word(sentence):
    """The longest word, ties going to the first. None for no words."""
    cleaned = [w.strip(".,!?;:'\"()").lower() for w in sentence.split()]
    words = [w for w in cleaned if w]
    if not words:
        return None
    longest = words[0]
    for word in words:
        if len(word) > len(longest):
            longest = word
    return longest
```

Three tutorials in one function: a loop, a decision inside it, and a list built by filtering. The `if w` at the end of the comprehension drops anything that was entirely punctuation, which `split` will hand you from a sentence containing " — ".

</details>

## Search and Sort

**8.** Given a sorted list of a million numbers and 10,000 numbers to look up, how would you do it, and how much faster is that than the obvious way?

<details class="dl-answer"><summary>answer</summary>

Binary search each one: 10,000 × 20 = 200,000 comparisons.

Linear search each one: 10,000 × 500,000 on average = five billion. Twenty-five thousand times slower.

If the list were *not* already sorted, sorting it first costs about 20 million comparisons — still repaid many times over by 10,000 lookups. The break-even is around 40 lookups.

</details>

**9.** Write a function that finds the two numbers in a list adding to a given target.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the obvious version first: check every pair. Count how many pairs that is for a list of n.
2. Now think about what you are asking for each number. For 7 and a target of 10, you want to know whether 3 is present.
3. You have already seen every number before it. What if you kept them?
4. Testing membership of a `set` takes the same time whether it holds ten numbers or ten million.

**Think about:** the second version does not compute anything faster. It changes the question from a search into a lookup.

**Try this next:** find three numbers that add to a target. Can the same trick apply, and what does it cost now?

</details>

<details class="dl-answer"><summary>answer</summary>

The obvious way checks every pair, which is n²:

```python
def pair_summing_to(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return numbers[i], numbers[j]
    return None
```

The good way remembers what it has seen, and is n:

```python
def pair_summing_to(numbers, target):
    seen = set()
    for n in numbers:
        if target - n in seen:
            return target - n, n
        seen.add(n)
    return None
```

The second is not cleverer arithmetic — it is the same question asked differently. Instead of "do any two of these add up", it asks "have I already seen the number that would complete this one", which is a lookup rather than a search.

</details>

**10.** Sort a list of names by surname, given full names as `"Ada Lovelace"`.

<details class="dl-answer"><summary>answer</summary>

```python
names = ["Ada Lovelace", "Alan Turing", "Grace Hopper", "Karen Sparck Jones"]
print(sorted(names, key=lambda name: name.split()[-1]))
```

`['Grace Hopper', 'Karen Sparck Jones', 'Ada Lovelace', 'Alan Turing']`.

Taking the last word is a guess about names, and it is wrong for double-barrelled surnames, for names written family-name-first, and for anybody with one name. It works for this list. Whether that is good enough depends on whose list it is, and "surname" is not a property every name in the world has.

</details>

**11.** Merge two sorted lists into one sorted list, without sorting the result.

<details class="dl-answer"><summary>answer</summary>

```python
def merge(a, b):
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result + a[i:] + b[j:]
```

The same merge walk as the set operations, and it is the heart of merge sort: split the list until every piece has one item, then merge back up. That is how you get n log n instead of n².

`<=` rather than `<` keeps it stable — equal items keep the order they came in.

</details>

## Putting Several Together

**12.** Write a program that reads a list of daily temperatures and reports: the warmest and coldest days, the average, how many days were above average, and the longest run of consecutive days above average.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take the four easy parts first — warmest, coldest, average, and how many are above it.
2. For the longest run, imagine walking the list with two numbers in your head: how long the current streak is, and the best you have seen.
3. What happens to the current streak when a day is above average? When it is not?
4. When do you compare the current streak against the best?

**Think about:** why the "best so far" has to be updated inside the loop rather than after it.

**Try this next:** report *when* the longest run started, not just how long it was. What extra do you have to remember?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def report(temperatures):
    """A summary of a list of daily readings."""
    if not temperatures:
        return "no readings"
    average = sum(temperatures) / len(temperatures)

    longest = run = 0
    for t in temperatures:
        run = run + 1 if t > average else 0
        longest = max(longest, run)

    return {
        "warmest day": temperatures.index(max(temperatures)) + 1,
        "coldest day": temperatures.index(min(temperatures)) + 1,
        "average": round(average, 2),
        "days above": sum(1 for t in temperatures if t > average),
        "longest run above": longest,
    }
```

The run counter is the only part that is not a one-liner, and it is the pattern worth taking away: keep a current run and a best-so-far, reset the current one whenever the streak breaks. The same three lines find the longest run of anything.

</details>

**13.** Write a number-guessing game where the *computer* guesses your number between 1 and 100, and report how many guesses it needs.

<details class="dl-answer"><summary>answer</summary>

```python
def guess(secret):
    """How many halvings it takes to find a number from 1 to 100."""
    low, high, tries = 1, 100, 0
    while low <= high:
        tries += 1
        middle = (low + high) // 2
        if middle == secret:
            return tries
        if middle < secret:
            low = middle + 1
        else:
            high = middle - 1
    return None


print(max(guess(n) for n in range(1, 101)))
```

Seven, at worst — and binary search is the strategy, applied to a number nobody wrote down. Run it over all hundred numbers and the average comes out at about 5.8.

</details>

**14.** Write a function that checks whether a list is sorted, and one that checks whether it is a permutation of another list.

<details class="dl-answer"><summary>answer</summary>

```python
def is_sorted(items):
    return all(items[i] <= items[i + 1] for i in range(len(items) - 1))


def same_items(a, b):
    return sorted(a) == sorted(b)
```

These two together are how you test a sorting function properly. The output must be sorted *and* contain exactly what went in — checking only the first accepts a function that returns `[]` every time, and checking only the second accepts one that does nothing at all.

Two obvious properties, and neither alone is worth anything.

</details>

**15.** A list contains every number from 1 to n except one. Find the missing number, using as little work as possible.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Three approaches are all correct here: sort and look for the gap, build a set and test each candidate, or use arithmetic. Try to think of all three before reading on.
2. You know something about the list that you have not used yet — what its contents *should* have been.
3. The sum of 1 to n has a formula. You met it in *Repeating Yourself*.
4. What is the difference between the sum it should be and the sum it is?

**Think about:** the arithmetic version uses knowledge about the data, and the other two only use what they can see in it. That is usually where the good answer lives.

**Try this next:** now two numbers are missing. The sum tells you what they add to. What second fact would pin them down?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def missing(numbers, n):
    return n * (n + 1) // 2 - sum(numbers)
```

One pass, no sorting, no extra memory. The sum of 1 to n is known, so the gap between that and the actual total is the missing number.

Sorting and looking for the break also works, at n log n. Building a set of what is present and testing each candidate also works, at n and a copy of the list. The arithmetic version is the one that uses something you *know* about the data rather than only what you can see in it — which is usually where the good answer is.

</details>

**16.** You are handed somebody else's function. It works. What would you check before using it in your own code?

<details class="dl-answer"><summary>answer</summary>

What it does with nothing — an empty list, a zero, an empty string.

Whether it changes its arguments, or only reads them.

Whether it is the same every time, or depends on something outside itself.

What it does with input it was not designed for: a negative where a count was expected, text where a number was.

None of these is about whether the code is *right* on the cases it was written for. They are about what happens at the edges, which is where the code you did not write meets the data you did not expect.

</details>
