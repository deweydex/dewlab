---
title: "How We Got Here — Practice"
slug: how-we-got-here-practice
practice_for: how-we-got-here
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# How We Got Here — Practice

Answers are folded. The conversion questions are worth doing by hand before you reach for the checking cell — the point is to be able to read the notation, not to have Python read it for you.

## Tools

```python exec
id: tools-1
def to_binary(n):
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(str(n % 2))
        n = n // 2
    return "".join(reversed(digits))


def from_binary(text):
    total = 0
    for character in text:
        total = total * 2 + int(character)
    return total


def to_hex(n):
    return format(n, "X")


print(to_binary(72), from_binary("01001000"), to_hex(72), chr(72))
```

## Reading the Notation

**1.** Convert to base 10: `1010`, `11111111`, `10000000`, `01000001`.

<details class="dl-answer"><summary>answer</summary>

10, 255, 128, 65.

255 is the largest number eight bits can hold, which is why so many limits in computing are 255. And 65 is the ASCII code for capital A.

</details>

**2.** Convert to binary: 5, 16, 100, 200.

<details class="dl-answer"><summary>answer</summary>

101, 10000, 1100100, 11001000.

</details>

**3.** Convert to hex: 15, 16, 255, 4096.

<details class="dl-answer"><summary>answer</summary>

F, 10, FF, 1000.

Notice 16 in hex is `10`, for the same reason 10 in decimal is `10` — you have run out of single digits and carried.

</details>

**4.** Convert `FF`, `A0`, `7E` from hex to binary without going through base 10.

<details class="dl-answer"><summary>answer</summary>

`11111111`, `10100000`, `01111110`.

Each hex digit is exactly four binary digits, so you can convert one at a time: F is 1111, A is 1010, 7 is 0111, E is 1110.

That direct correspondence is the entire reason hexadecimal exists.

</details>

**5.** Decode `01001000 01001001` as ASCII.

<details class="dl-answer"><summary>answer</summary>

72 and 73, which are `H` and `I`. The message is "HI".

</details>

**6.** Decode the hex `43 4F 44 45` as ASCII.

<details class="dl-answer"><summary>answer</summary>

67, 79, 68, 69 — which is "CODE".

</details>

**7.** Why do computers use binary rather than base 10?

<details class="dl-answer"><summary>answer</summary>

Because a transistor is naturally a two-state device: on or off, high voltage or low. Base 2 maps onto that exactly.

Base 10 would need each component to reliably distinguish ten different voltage levels, which is harder to build, harder to keep stable, and gains nothing.

</details>

**8.** Why does hexadecimal exist, given that computers do not use it?

<details class="dl-answer"><summary>answer</summary>

Entirely for people. `11111111` and `11111011` are hard to tell apart at a glance; `FF` and `FB` are not.

One hex digit is exactly four binary digits, so the conversion is mechanical and nothing is lost. It is binary written shorter, for the benefit of whoever has to read it.

</details>

## The History

**9.** What did Ada Lovelace do, and why is it significant that the machine was never built?

<details class="dl-answer"><summary>answer</summary>

She wrote a step-by-step method for the Analytical Engine to compute a sequence of numbers, using loops and conditional branching — in notes appended to a translation, which ended up longer than the paper itself.

The machine's never being built is the point: **a program does not need a working machine to exist.** It is a sequence of precise instructions, and that is true whether or not anything can carry them out yet.

</details>

**10.** Put these in order and say what each made easier: machine code, high-level languages, assembly language.

<details class="dl-answer"><summary>answer</summary>

Machine code (1940s) — binary patterns the hardware consumes directly. Nothing between you and the circuits.

Assembly (1950s) — short names like `ADD` and `MOV` instead of binary, translated back by an assembler. This is the first time a program's job is to write another program.

High-level languages (1957 onwards) — code that reads like English or mathematics, translated by a compiler or interpreter, and no longer tied to one machine's instruction set.

Each step made things easier for people. The hardware never needed any of them.

</details>

**11.** What was the problem with assembly that high-level languages solved?

<details class="dl-answer"><summary>answer</summary>

It was tied to one particular machine. The instruction names matched that machine's instruction set, so a program written for one computer would not run on another, and everything had to be rewritten for each new machine.

</details>

**12.** What is the difference between a compiler and an interpreter?

<details class="dl-answer"><summary>answer</summary>

A compiler translates the whole program into machine code before it runs, producing something the machine can execute on its own. An interpreter reads and runs the program line by line as it goes.

C is traditionally compiled; Python is traditionally interpreted, though strictly it compiles to bytecode first and then interprets that.

</details>

**13.** Why does a compiled program usually run faster, and an interpreted one usually get debugged faster?

<details class="dl-answer"><summary>answer</summary>

A compiled program has done its translating already, so at run time nothing is spent on it, and the compiler had the whole program in view and could optimise across it.

An interpreted program is translated as it runs, which costs time — but there is no compile step between writing a line and seeing what it does. You change something and run it, which for finding a bug is worth a great deal.

</details>

**14.** Which language on the table would you expect to find running a bank's overnight batch processing? Why?

<details class="dl-answer"><summary>answer</summary>

COBOL, and a surprising amount of it still is. It was built in 1959 for business data processing, banks adopted it early, and code that works and has been audited for forty years is not lightly replaced.

That is worth knowing as a fact about the industry as much as about the language: software outlives the reasons it was written.

</details>

## Paradigms

**15.** Name the paradigm each of these is closest to, and say what gave it away.

- (a) `total = 0` then a loop adding to it
- (b) `reduce(lambda a, b: a + b, prices, 0)`
- (c) `cart.add(4.50)` then `cart.total()`
- (d) `[p * 2 for p in prices]`

<details class="dl-answer"><summary>answer</summary>

(a) Procedural — step-by-step instructions changing something as they go.

(b) Functional — describing the transformation rather than the loop that applies it, and no variable being updated.

(c) Object-oriented — the data and the operations on it bundled together, and the object holding state between calls.

(d) A comprehension, which is declarative in style: you say what the result is rather than how to build it.

</details>

**16.** Which of these paradigms does Python support?

<details class="dl-answer"><summary>answer</summary>

All of them, which is unusual and is part of why it is used for teaching.

Most languages push you firmly towards one. Python lets you choose, which is a freedom and also a responsibility — a codebase that uses all four inconsistently is harder to read than one that picks one.

</details>

**17.** Is any of the four paradigms correct?

<details class="dl-answer"><summary>answer</summary>

No. They are habits of thought, and which suits depends on the problem and on who else has to read the code.

A procedural loop is clearer for a beginner; a functional one is clearer once you are used to it; an object-oriented design pays off when there is state to keep track of and costs you when there is not.

</details>

**18.** Rewrite this procedurally: `doubled = [n * 2 for n in numbers]`.

<details class="dl-answer"><summary>answer</summary>

```python
doubled = []
for n in numbers:
    doubled.append(n * 2)
```

Four lines instead of one, doing exactly the same thing. Which one is better depends entirely on who is reading it.

</details>

## Putting It Together

**19.** Write `crack_the_vault(groups)`, where each entry is a pair of the base (`"bin"` or `"hex"`) and the code, and the output is the decoded message.

<details class="dl-answer"><summary>answer</summary>

```python
def crack_the_vault(groups):
    letters = []
    for base, code in groups:
        number = from_binary(code) if base == "bin" else int(code, 16)
        letters.append(chr(number))
    return "".join(letters)
```

It is the two earlier decoders with a check to decide which applies — which is a common shape, and one worth noticing: when two functions differ only in one step, they usually want to become one function with a parameter.

</details>

**20.** A file's first two bytes are `50 4B` in hex. What are those as characters, and what might that tell you?

<details class="dl-answer"><summary>answer</summary>

80 and 75, which are `P` and `K`.

That is the signature of a ZIP file — the initials of Phil Katz, who wrote the original format in 1989. Many file formats start with a fixed few bytes called a magic number, and a great deal of software identifies a file by reading them rather than by trusting the extension.

</details>
