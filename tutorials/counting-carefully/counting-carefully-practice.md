---
title: "Counting: factorials, permutations and combinations — Practice"
practice_for: counting-carefully
year: "2026-2027"
version: 2026.08.23.1
---

# Counting: factorials, permutations and combinations — Practice

Each answer is hidden until you open it. Try the problem first.

Before you start each problem, ask two questions:

1. Does the order matter?
2. Can the same thing be chosen more than once?

Your two answers tell you which formula to use. The hard part of these
problems is to choose the formula. The arithmetic after it is the easy part.

## Tools

This cell holds `permutations` and `combinations` functions, so you can
use them in the problems below. Python's `math` module also has these
built in, as `math.perm` and `math.comb`. The line `import math` loads that module. Run the cell once before you
start.

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

**1.** What are $0!$, $1!$, $5!$ and $10!$?

<details class="dl-answer"><summary>answer</summary>

They are 1, 1, 120 and 3,628,800.

$0! = 1$ is a definition. We do not calculate it. We agree on it. It is the only value that keeps every formula on this page working. It also makes sense, because there is exactly one way to arrange nothing.

</details>

**2.** Can you simplify $\frac{10!}{8!}$ and $\frac{n!}{(n-2)!}$ without calculating the factorials?

<details class="dl-answer"><summary>answer</summary>

They are 90 and $n(n-1)$.

$\frac{10!}{8!} = 10 \times 9 = 90$. Every number from 8 down to 1 is on both the top and the bottom, so they cancel.

Because of this cancelling, we can calculate a permutation count for a large $n$ without ever making a huge number.

</details>

**3.** How big is $20!$? How big is $100!$?

<details class="dl-answer"><summary>answer</summary>

$20!$ is about $2.4 \times 10^{18}$, and $100!$ is about $9.3 \times 10^{157}$.

$20!$ is roughly the number of grains of sand on Earth. $100!$ is far more than the number of atoms in the universe that we can observe, which is about $10^{80}$.

Think about these sizes for a moment. A program that tries every order of 20 things will never finish.

</details>

## Permutations

**4.** How many ways can 5 people stand in a line?

<details class="dl-answer"><summary>answer</summary>

There are 120 ways, which is 5!.

There are five choices for the first position, four for the second, and so on down to one.

</details>

**5.** In how many ways can you pick a first, a second and a third from 8 runners?

<details class="dl-answer"><summary>answer</summary>

There are 336 ways.

$P(8,3) = 8 \times 7 \times 6$. Gold, silver and bronze are different results, so the order matters. That makes it a permutation.

</details>

**6.** How many 4-letter arrangements can be made from the letters of `COMPUTER` with no repeats?

<details class="dl-answer"><summary>answer</summary>

There are 1,680.

$P(8,4) = 8 \times 7 \times 6 \times 5$. The eight letters are all different, and that keeps this one short.

</details>

**7.** How many different arrangements are there of the letters of `LETTER`?

<details class="dl-answer"><summary>answer</summary>

There are 180.

Six different letters would give $6! = 720$. But the two Es look the same, and so do the two Ts. If you swap the two Es, you get the same word, so every word is counted twice. The Ts double it again. So we divide by $2!$ for each repeated letter: $\frac{720}{2 \times 2} = 180$.

Here is the general rule. Start with the factorial of the total number of letters. Then divide by the factorial of each repeat count.

</details>

**8.** How many 4-digit PINs are there, if digits may repeat?

<details class="dl-answer"><summary>answer</summary>

There are 10,000.

There are ten choices in each of four positions, so the count is $10^4$. Repeats are allowed, so we use the multiplication principle. That is why the answer is a power. A permutation would multiply numbers that go down by one each time, like $10 \times 9 \times 8 \times 7$.

Without repeats, the count would be $P(10,4) = 5{,}040$. That is about half as many.

</details>

## Combinations

**9.** In how many ways can you choose 3 people from 8 for a committee?

<details class="dl-answer"><summary>answer</summary>

There are 56 ways.

$C(8,3) = \frac{8 \times 7 \times 6}{3 \times 2 \times 1}$. Question 5 found 336 orders. Each committee can be listed in $3! = 6$ orders, so those 336 orders make only $336 \div 6 = 56$ committees.

The only difference between a permutation and a combination is the division by $r!$.

</details>

**10.** Calculate $C(5,0)$, $C(5,1)$, $C(5,2)$, $C(5,3)$, $C(5,4)$, $C(5,5)$. What do you notice?

<details class="dl-answer"><summary>answer</summary>

They are 1, 5, 10, 10, 5, 1.

The list reads the same forwards and backwards. Why? When you choose 2 things to keep, you also choose 3 things to leave out. That is why $C(n,r) = C(n, n-r)$.

These numbers are also a row of Pascal's triangle. Pascal's triangle is a triangle of numbers with 1 at each end of every row. Each number inside it is the sum of the two numbers above it. Its rows start 1, then 1 1, then 1 2 1, then 1 3 3 1, then 1 4 6 4 1, then 1 5 10 10 5 1.

The row 1 5 10 10 5 1 holds $C(5,0)$ to $C(5,5)$, and every other row works the same way. The same rows appear again in [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive), when we expand $(x+1)^5$.

The numbers also add up to 32, which is $2^5$. A subset of a group of 5 things is any choice of some of them, from none of them up to all 5. Each of the 5 things is either in the subset or out of it, so there are $2^5 = 32$ subsets. The list counts them by size: 1 subset with 0 things, 5 with 1 thing, and so on.

</details>

**11.** The Lotto asks for 6 numbers from 47. How many different tickets are there?

<details class="dl-answer"><summary>answer</summary>

There are 10,737,573 tickets.

This is $C(47,6)$. If you bought one ticket a week, you would expect to win about once every 206,000 years.

On a lottery ticket, the order does not matter. That is the only reason the count is about ten million. If the order did matter, the count would be $P(47,6)$, which is about 7.7 billion.

</details>

**12.** A pizza place has 10 toppings. How many pizzas with exactly 3 toppings? With any number, including none?

<details class="dl-answer"><summary>answer</summary>

There are 120 with exactly 3 toppings, and 1,024 with any number.

For exactly 3 toppings, the count is $C(10,3) = 120$. For any number of toppings, each of the 10 toppings is either on the pizza or off it. That gives 2 choices, ten times, so $2^{10} = 1{,}024$.

This is the "how many subsets" question from question 10 again. It is also why every row of Pascal's triangle adds up to a power of two.

</details>

**13.** A hand of 5 cards is dealt from a deck of 52. How many different hands are there? How many of them are all hearts?

<details class="dl-answer"><summary>answer</summary>

There are 2,598,960 hands, and 1,287 of them are all hearts.

These are $C(52,5)$ and $C(13,5)$, because there are 13 hearts in the deck. A hand of 5 cards all from one suit is called a flush. So the chance of a flush in hearts is about 1 in 2,020. There are 4 suits, so the chance of a flush in any suit is about 1 in 505.

</details>

## Choosing the right tool

**14.** Is each of these a permutation, a combination or a power? Can you also calculate each count?

- (a) Choosing 3 books from 10 to take on holiday
- (b) Choosing a president, secretary and treasurer from 10 members
- (c) A 5-character password from 26 letters
- (d) Ranking your top 3 films from a list of 20

<details class="dl-answer"><summary>answer</summary>

- (a) Combination: $C(10,3) = 120$.
- (b) Permutation: $P(10,3) = 720$. The three roles are different, so the order matters.
- (c) Power: $26^5 = 11{,}881{,}376$. Letters can repeat.
- (d) Permutation: $P(20,3) = 6{,}840$.

Two questions decide it every time. Does the order matter? Can things repeat?

</details>

**15.** In how many ways can 5 people sit around a *circular* table?

<details class="dl-answer"><summary>answer</summary>

There are 24 ways. The answer is not 120.

Suppose everybody moves one seat to the left. Each person still has the same neighbours, so it is the same arrangement. Each arrangement can be turned in 5 ways like this, so $5!$ counts each one 5 times. That gives $\frac{5!}{5} = 4! = 24$.

Most people answer 120 at first. The formula is easy. The hard part is to notice that this situation is different.

</details>

## Password strength

**16.** How many 8-character passwords are there using lowercase letters only? How many if we add uppercase letters? How many if we also add digits and 10 symbols?

<details class="dl-answer"><summary>answer</summary>

The counts are $26^8 \approx 2.1 \times 10^{11}$, then $52^8 \approx 5.3 \times 10^{13}$, then $72^8 \approx 7.2 \times 10^{14}$.

When we go from 26 to 52 letters, the choices for each character double. That multiplied the count by 256, which is $2^8$: one doubling for each of the 8 characters.

</details>

**17.** An attacker makes a billion guesses a second. How long does it take to try every password in each of those cases?

<details class="dl-answer"><summary>answer</summary>

It takes about 3.5 minutes, about 15 hours, and about 8 days.

None of those is safe. What does this tell us? Eight characters is too short. Symbols still help. The same 72 characters with a length of 12 take about 600,000 years.

**Length matters more than the kinds of character**, because the length is the power in the formula.

</details>

**18.** Which is stronger: a 10-character password from 72 characters, or four random common words?

<details class="dl-answer"><summary>answer</summary>

The four words are stronger, if the list is large enough.

The 10-character password gives $72^{10} \approx 3.7 \times 10^{18}$ possibilities. Four words from a list of 10,000 give $10{,}000^4 = 10^{16}$. That is far fewer: about 370 times fewer. Four words from a list of 50,000 give $6.25 \times 10^{18}$, which is slightly more.

The stronger reason is about people. People can remember four words. They do not use ten random characters. A strong password that nobody can remember gets written on a note, and then anyone who finds the note has the password.

</details>

**19.** A company requires "at least one uppercase, one digit and one symbol". Does that make passwords stronger?

<details class="dl-answer"><summary>answer</summary>

It makes the number of possible passwords smaller. The rule removes every password that is all lowercase, and adds none.

The rule does stop the weakest choices. That helps against an attacker who tries lowercase passwords first. But it also produces `Password1!` again and again, because people meet the rule in the easiest way they can.

It is easy to count the possible passwords. It is hard to guess which ones people really choose, and counting cannot answer that.

</details>

**20.** In how many ways can we choose 6 numbers from 47, *if repeats are allowed and the order does not matter*?

<details class="dl-answer"><summary>answer</summary>

There are $C(52,6) = 20{,}358{,}520$ ways.

To choose $r$ things from $n$ with repeats allowed, the formula is $C(n + r - 1, r)$. Here that is $C(47 + 6 - 1, 6) = C(52, 6)$.

Where does the formula come from? Picture $r$ items and $n - 1$ dividers in one row, $n + r - 1$ places in all. The dividers split the row into $n$ groups, one for each number, and the items in a group say how many times that number was chosen. So each choice matches one way to pick which $r$ places hold the items. It is worth seeing this idea once, even if you never need the formula.

The count is roughly twice the real lottery's, because repeats are allowed.

</details>
