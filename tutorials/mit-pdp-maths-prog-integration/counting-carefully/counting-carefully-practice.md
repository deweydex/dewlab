---
title: "Counting Carefully — Practice"
slug: counting-carefully-practice
practice_for: counting-carefully
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: data-chance-and-logic
version: 2026.08.23.1
---

# Counting Carefully — Practice

Answers are folded. For each problem, decide first whether order matters and whether repeats are allowed — those two questions pick the formula, and getting them wrong is the only real difficulty here.

## Tools

```python exec
id: tools-1
import math

def permutations(n, r):
    """Ways to arrange r things chosen from n, order mattering."""
    return math.factorial(n) // math.factorial(n - r)


def combinations(n, r):
    """Ways to choose r things from n, order not mattering."""
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


print(math.factorial(5), permutations(5, 3), combinations(5, 3))
print(math.comb(5, 3), math.perm(5, 3))     # Python has these built in
```

## Factorials

**1.** Compute 0!, 1!, 5!, 10!.

<details class="dl-answer"><summary>answer</summary>

1, 1, 120, 3,628,800.

0! being 1 is a definition rather than a calculation, and it is the only one that keeps every formula on this page working. There is exactly one way to arrange nothing.

</details>

**2.** Simplify $\frac{10!}{8!}$ and $\frac{n!}{(n-2)!}$ without computing the factorials.

<details class="dl-answer"><summary>answer</summary>

90, and $n(n-1)$.

Everything below the smaller factorial cancels. That cancellation is why permutation counts can be computed for large n without ever forming an astronomical number.

</details>

**3.** How big is 20!? How big is 100!?

<details class="dl-answer"><summary>answer</summary>

About 2.4 × 10¹⁸, and about 9.3 × 10¹⁵⁷.

20! is roughly the number of grains of sand on Earth. 100! is vastly more than the number of atoms in the observable universe, which is about 10⁸⁰.

This is worth feeling rather than knowing: any algorithm that tries all orderings of 20 things has already lost.

</details>

## Permutations

**4.** How many ways can 5 people stand in a line?

<details class="dl-answer"><summary>answer</summary>

120, which is 5!.

Five choices for the first position, four for the second, and so on.

</details>

**5.** How many ways can you pick a first, second and third from 8 runners?

<details class="dl-answer"><summary>answer</summary>

336.

$P(8,3) = 8 \times 7 \times 6$. Order matters — gold, silver and bronze are different outcomes — so it is a permutation.

</details>

**6.** How many 4-letter arrangements can be made from the letters of `COMPUTER` with no repeats?

<details class="dl-answer"><summary>answer</summary>

1,680.

$P(8,4) = 8 \times 7 \times 6 \times 5$. All eight letters are distinct, which is what makes this straightforward.

</details>

**7.** How many arrangements of the letters of `LETTER`?

<details class="dl-answer"><summary>answer</summary>

180.

Six letters would give 720, but the two Es are indistinguishable and so are the two Ts. Divide by 2! for each repeat: $\frac{720}{2 \times 2}$.

The general rule: divide the factorial of the total by the factorial of each repeat count.

</details>

**8.** How many 4-digit PINs are there, if digits may repeat?

<details class="dl-answer"><summary>answer</summary>

10,000.

Ten choices in each of four positions — $10^4$. This is not a permutation, because repeats are allowed; that is what makes it a power rather than a falling product.

Without repeats it would be $P(10,4) = 5{,}040$, which is nearly half as many.

</details>

## Combinations

**9.** How many ways can you choose 3 people from 8 for a committee?

<details class="dl-answer"><summary>answer</summary>

56.

$C(8,3) = \frac{8 \times 7 \times 6}{3 \times 2 \times 1}$. The 336 orderings from question 5 collapse into 56 committees, because each committee can be listed in 3! = 6 orders.

That division by r! is the entire difference between a permutation and a combination.

</details>

**10.** Compute $C(5,0)$, $C(5,1)$, $C(5,2)$, $C(5,3)$, $C(5,4)$, $C(5,5)$. What do you notice?

<details class="dl-answer"><summary>answer</summary>

1, 5, 10, 10, 5, 1.

Symmetric, and they are the row of Pascal's triangle that turned up when expanding $(x+1)^5$. Choosing 2 to keep is the same as choosing 3 to discard, which is why $C(n,r) = C(n, n-r)$.

They also add to 32, which is $2^5$ — the number of subsets of a 5-element set, counted by size.

</details>

**11.** The Lotto asks for 6 numbers from 47. How many tickets are there?

<details class="dl-answer"><summary>answer</summary>

10,737,573.

$C(47,6)$. Buying one ticket a week, you would expect to win about once every 206,000 years.

Order does not matter on a lottery ticket, which is the only reason the number is merely ten million rather than the seven billion it would be if it did.

</details>

**12.** A pizza place has 10 toppings. How many pizzas with exactly 3 toppings? With any number, including none?

<details class="dl-answer"><summary>answer</summary>

120, and 1,024.

$C(10,3) = 120$. For any number, each topping is independently on or off: $2^{10}$.

The second is the "how many subsets" question again, and it is why the sum of a row of Pascal's triangle is a power of two.

</details>

**13.** A hand of 5 cards is dealt from 52. How many hands? How many are all hearts?

<details class="dl-answer"><summary>answer</summary>

2,598,960 hands, and 1,287 of them all hearts.

$C(52,5)$ and $C(13,5)$. So the chance of a flush in hearts is about 1 in 2,020, and about 1 in 505 for a flush of any suit.

</details>

## Choosing the Right Tool

**14.** For each, say whether it is a permutation, a combination, or a power.

- (a) Choosing 3 books from 10 to take on holiday
- (b) Choosing a president, secretary and treasurer from 10 members
- (c) A 5-character password from 26 letters
- (d) Ranking your top 3 films from a list of 20

<details class="dl-answer"><summary>answer</summary>

(a) Combination, $C(10,3) = 120$. (b) Permutation, $P(10,3) = 720$ — the roles are different. (c) Power, $26^5 = 11{,}881{,}376$ — repeats allowed. (d) Permutation, $P(20,3) = 6{,}840$.

The two questions that decide it: does order matter, and can things repeat.

</details>

**15.** How many ways can 5 people sit around a *circular* table?

<details class="dl-answer"><summary>answer</summary>

24, not 120.

Rotating everybody one seat round gives the same arrangement, and there are 5 rotations, so $\frac{5!}{5} = 4!$.

This is the sort of question where the formula is easy and noticing that the situation is different is the whole difficulty.

</details>

## Password Strength

**16.** How many 8-character passwords are there using lowercase letters only? Adding uppercase? Adding digits and 10 symbols?

<details class="dl-answer"><summary>answer</summary>

$26^8 \approx 2.1 \times 10^{11}$, then $52^8 \approx 5.3 \times 10^{13}$, then $72^8 \approx 7.2 \times 10^{14}$.

Doubling the alphabet multiplied the count by 256 — that is $2^8$, one doubling per character.

</details>

**17.** At a billion guesses a second, how long does each of those take to exhaust?

<details class="dl-answer"><summary>answer</summary>

About 3.5 minutes, about 15 hours, and about 8 days.

None of those is safe. The lesson is not that symbols are useless but that eight characters is short — the same alphabet at 12 characters takes about 600,000 years.

**Length beats complexity**, because length is the exponent.

</details>

**18.** Which is stronger: a 10-character password from 72 symbols, or four random common words?

<details class="dl-answer"><summary>answer</summary>

The words, if the list is large enough.

$72^{10} \approx 3.7 \times 10^{18}$. Four words drawn from a list of 10,000 gives $10^{16}$ — slightly fewer. Drawn from 50,000 it is $6.25 \times 10^{18}$, slightly more.

The real argument is that people actually remember the words and do not actually use ten random symbols. A strong password nobody can remember gets written on a note, and its strength then depends on the note.

</details>

**19.** A company requires "at least one uppercase, one digit and one symbol". Does that make passwords stronger?

<details class="dl-answer"><summary>answer</summary>

It makes the *space* smaller, not larger — it rules out every all-lowercase password.

What it does is prevent the weakest choices, which is a real benefit against an attacker who tries lowercase first. What it also does, reliably, is produce `Password1!`, because people satisfy the rule in the cheapest way available.

Counting the space is easy; predicting which parts of it people use is the actual problem, and it is not a combinatorics question.

</details>

**20.** How many ways are there to choose 6 numbers from 47 *if repeats were allowed and order did not matter*?

<details class="dl-answer"><summary>answer</summary>

$C(52,6) = 20{,}358{,}520$.

The formula for choosing r from n with repeats is $C(n + r - 1, r)$, which here is $C(52, 6)$. The trick behind it — think of r items and n−1 dividers in a row, and choose which positions are dividers — is worth seeing once even if you never need the formula.

Roughly twice as many as the real lottery, which is what allowing repeats buys.

</details>
