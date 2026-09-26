---
title: "Maths that runs the world"
context_for:
  - how-likely-is-it
  - chances-that-combine
  - counting-every-outfit
  - bits-that-flip
year: "2026-2027"
version: 2026.09.24.1
---

# Maths that runs the world

The chances, counts and parity bits in this course are not only for
exercises. They decide what your phone can read, how a photo gets home
from the edge of the solar system, and why the internet had to change
the way it names computers. Here are four short stories, each true, and
each built on an idea you have already met.

On this page we:

- follow a puzzle about three doors that thousands of people argued about
- see why the birthday problem matters to every program that stores files
- meet codes that fix a flipped bit, not only notice it
- count our way to the moment the internet ran out of addresses

> **The space we're in.** The real world, which is messier than a
> page of problems. Each story names the assumption its maths rests on,
> because in the real world that assumption is where things go right or
> wrong.

## Three doors and thousands of letters

This story goes with [How likely is it?](tutorial:how-likely-is-it).

A game show host shows you three doors. A car is behind one, and a goat
is behind each of the others. You pick a door. The host, who knows
where the car is, opens one of the other two and shows you a goat. Then
he asks: do you want to switch to the last closed door?

Most people say it makes no difference, because two doors are left and
one hides the car. In fact, switching wins two times in three. A
statistician, Steve Selvin, wrote about the puzzle in two letters to the
journal *The American Statistician* in 1975. The second one called it
the Monty Hall problem, after the host of the American game show
*Let's Make a Deal*.

Most people first heard of it in 1990. A reader sent the puzzle to
Marilyn vos Savant, who answered questions in a column in *Parade*
magazine, and she said: switch. Thousands of readers wrote in to say she
was wrong, and some of those letters came from people with doctorates in
mathematics. She was right.

Why did so many careful people get it wrong? The usual argument treats
the two closed doors as the same. They are not, because the host's
choice was not random. He could never open the door with the car. His
choice carries information, and the answer changes because of it.

The story also shows a way to settle an argument that does not depend
on who argues best: play the game many times and count, the way
`simulate` does. If you want to do exactly that, the page
[The Monty Hall problem: three doors and a simulation](tutorial:three-doors)
plays it ten thousand times in Python, and then changes the host to see
what happens.

## The birthday problem, inside every computer

This story goes with [Chances that combine](tutorial:chances-that-combine).

In a room of 23 people, the chance that two share a birthday is a little
more than a half. There are only 365 birthdays, but there are 253 pairs
of people, and any one pair can match.

Computers meet the same problem with a different kind of birthday. A
*hash* is a short code worked out from a piece of data, such as a file
or a password, so that the same data always gives the same code. A
program can compare two short hashes much faster than it can compare two
long files. When two different pieces of data get the same hash, that is
called a *collision*: two files with the same "birthday".

Say a hash has 32 bits. Then there are $2^{32}$ possible hashes, more
than four thousand million. That sounds like plenty. How many files do
you think it takes before a collision is as likely as not? Make a guess,
then run the cell. It counts the chance exactly, the way
[Chances that combine](tutorial:chances-that-combine#way-two-count-it-exactly)
did for birthdays, with `values` in place of 365.

```python exec
id: world-hash-collisions
def chance_of_shared(people, values):
    """The chance that at least two of this many people share one of the values."""
    all_different = 1
    for already in range(people):
        all_different = all_different * (values - already) / values
    return 1 - all_different

print(chance_of_shared(23, 365))
print(chance_of_shared(77000, 2 ** 32))
```

With about 77,000 files, a collision is as likely as not, and 77,000 is
a tiny fraction of four thousand million. A useful guide is that the
trouble starts at about the square root of the number of possible
values: $\sqrt{365}$ is about 19, and $\sqrt{2^{32}}$ is $2^{16}$, which
is 65,536.

That is why hashes that must never collide are long. Git, the program
many programmers use to keep the history of their code, names every
saved version by a hash of 160 bits, written as 40 hexadecimal digits.
By the square-root guide, a collision by chance only becomes likely at around
$2^{80}$ versions, and that is far more than all the code ever written.

## Codes that fix a flipped bit

This story goes with [Bits that flip](tutorial:bits-that-flip).

A parity bit notices that one bit has flipped, but it cannot say which
one. The only thing a computer can do is ask for the message again.

In the late 1940s, Richard Hamming worked at Bell Labs, in the United
States, on a computer built from electrical switches called relays. On
weekdays, when the machine found an error, it stopped and waited for an
operator. At weekends there was no operator, so it dropped the job and
moved on to the next one. Hamming ran his work at weekends, and more
than once came back on Monday to find nothing done. So he asked a
better question: if a machine can notice an error, why can it not fix
one? In 1950 he published codes that do exactly that. An
*error-correcting code* adds extra bits to a message in a way that lets
the receiver find a flipped bit and flip it back.

Here is the simplest code of that kind. Send every bit three times.
If one copy flips on the way, the other two still agree, so we take the
*majority vote*: whichever bit appears at least twice in a group. The
cell uses `bit * 3`, which repeats text, as `"na" * 2` did on
[Four questions for any puzzle](tutorial:four-questions). `group.count("1")`
counts the 1s in a group. Before you run it: will the decoded message
match the one that was sent?

```python exec
id: world-three-copies
message = "1011"
sent = ""
for bit in message:
    sent = sent + bit * 3
print("sent:    ", sent)

# The noise flips one bit, in the third group of three.
received = ["111", "000", "011", "111"]

decoded = ""
for group in received:
    if group.count("1") >= 2:
        decoded = decoded + "1"
    else:
        decoded = decoded + "0"
print("decoded: ", decoded)
```

The third group arrived as `011`, and the vote still says 1, so the
message comes back as `1011`. The price is high: every bit is sent
three times. Hamming's codes are much cheaper. His best-known one adds
three check bits to every four bits of message, and still fixes any one
flipped bit. Each check bit is a parity bit, but over a different group
of the message's bits, so the pattern of failed checks points at the
bit that flipped.

Codes like these are inside many things you use.

- **QR codes.** A QR code uses a family called *Reed–Solomon codes*. The
  person making the code chooses one of four levels. At the lowest,
  about 7% of the code can be damaged and it still reads. At the
  highest, about 30% can. That is why a QR code with a logo printed
  over its middle still works: the logo is damage the code was built to
  survive.
- **Music CDs** use Reed–Solomon codes too, so a scratched disc can
  often still play.
- **Deep space.** The two Voyager probes were launched in 1977. For the
  later part of their journey, after they passed Saturn, their data
  were sent home using a Reed–Solomon code together with a second code.
  A signal from that far away is very weak by the time it reaches Earth,
  and without codes that fix errors, a great deal of it would be lost.

Each of these rests on an assumption, as the parity bit did: that only
so many bits are damaged. Scratch more than a third of a QR code, and no
code can bring it back.

## Running out of numbers

This story goes with [Counting every outfit](tutorial:counting-every-outfit).

Every computer on the internet needs an address, so that messages can
find it. The address system most of the internet was built on, called
IPv4, gives each address 32 bits. Each bit is a choice of 2, so by the
counting principle there are $2^{32}$ addresses. How many is that, and
is it enough for the world? Guess, then run it. The last line counts the
newer system, IPv6, which uses 128 bits.

```python exec
id: world-addresses
ipv4_addresses = 2 ** 32
people_in_the_world = 8_000_000_000   # about 8 thousand million

print(ipv4_addresses)
print(ipv4_addresses / people_in_the_world)
print(2 ** 128)
```

(The underscores in `8_000_000_000` are there only to make the number
easier to read. Python ignores them.)

There are about 4.3 thousand million IPv4 addresses, which is about half
an address for every person alive, before counting phones, laptops,
printers and servers. The people who build the internet knew for years
that the addresses would run out. In February 2011, the organisation that hands out the
world's addresses gave away its last free blocks of them. Today much of
the internet uses IPv6, whose $2^{128}$ addresses are a number 39 digits
long. Adding 96 more bits did not add 96 more addresses. It multiplied
the count by 2, ninety-six times.

The counting principle also explains a small change on Irish roads. Up
to 2012, an Irish number plate began with two digits for the year, like
`12`. The motor trade worried that people would not want a car with a
`13` plate, and from 2013 the year was followed by one more digit: 1
for a car registered from January to June, and 2 for July to December.
So 2013 plates begin `131` or `132`. That digit is a choice of 2, so
every year now has twice as many ways to begin a plate. The change was
made for a superstition, and it has stayed ever since.

## Where to read more

Rosenhouse, J. (2009). *The Monty Hall Problem: The Remarkable Story of
Math's Most Contentious Brain Teaser*. Oxford University Press. A whole
book on the three doors, and on the many versions where the answer
changes.

Hamming, R. W. (1950). Error detecting and error correcting codes.
*Bell System Technical Journal*, 29(2). The paper that started the
subject. Its opening pages explain the idea in words, before the maths
begins.

PurpleMind (2025). *This Coding Mistake Cost $370 Million.*
<https://www.youtube.com/watch?v=Qehl4h5MDsg>. In 1996, a new rocket
exploded less than a minute after launch, because a number grew too big
for the space the program kept for it. This video tells the story. Twenty
minutes.
