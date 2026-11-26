---
title: "An Equipment Inventory: Who Has the Cables?"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO5]
  4-week-three-code-other-people-can-read:
    covers: [PDP-LO7, PDP-LO11]
  5-release-and-review:
    touches: [PDP-LO12]
---

# An Equipment Inventory: Who Has the Cables?

A network lab has a store of equipment: cables, switches, routers and adapters. People borrow things and bring them back, and somebody needs to know how many are left and who has what. On this page we build the program that keeps track.

The project has three stages, about one week each. Each stage ends with a program that works. This project is also about writing code that other people can read, so each stage asks you to look at your names and comments as well as at what the program does.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Who uses this program, and what do they need to know? Write two or three short sentences from their point of view, such as "As a lab assistant, I want to see what is running low."

<!-- answer -->

**1.2** Write a sample run and a list of commands. For each command, write one line of pseudocode that says what it does.

<!-- answer -->

## 2. Week One: Counting Stock

```python exec
id: week-one-counting-stock-1
items = ["patch cable", "switch", "router", "usb adapter"]
counts = [24, 3, 2, 7]
```

**2.1** Run the cell above. Then print the stock as a neat table, with the names in one column and the counts in another. The text method `ljust(15)` pads a string to 15 characters.

```python exec
id: week-one-counting-stock-2
# your table here
```

```solution
for position in range(len(items)):
    print(items[position].ljust(15), counts[position])
```

**2.2** Write a command line with `stock`, `in` and `out`. For `in`, ask for an item and a number, and add the number to its count. For `out`, take the number away.

```python exec
id: week-one-counting-stock-3
# your inventory here
```

**2.3** What should happen when someone takes out 5 routers and there are only 2? What about an item that is not in the list? Make your program handle both.

<!-- answer -->

**2.4** When an item drops to 2 or fewer, print a warning such as `Running low: router`. Where in the code should this check go, so it happens after every `out`?

<!-- answer -->

## 3. Week Two: Who Borrowed What

**3.1** Change `out` so it also asks who is borrowing the item. Keep two more lists: one for borrowers and one for what each borrowed. Change `in` so a person returns what they borrowed.

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. Make `borrowers = []` and `borrowed = []` next to the other lists.
2. In `out`, append the person's name to `borrowers` and the item to `borrowed`.
3. In `in`, find a position where both the name and the item match, and `pop` it from both lists.

</details>

**3.2** Add a command `who` that asks for an item and lists everyone who has one.

<!-- answer -->

**3.3** Your program now has four lists that must stay in step. Write down one way they could fall out of step. How would you notice?

<!-- answer -->

## 4. Week Three: Code Other People Can Read

**4.1** Swap code with another pair, without explaining it. Read their code for five minutes. Write down every name or line you did not understand.

<!-- answer -->

**4.2** Look at the notes the other pair wrote about your code. Rename any variable whose name did not explain itself. Add a comment where a reader was confused. A good comment says why a line is there. A comment that only repeats the line adds nothing.

<!-- answer -->

**4.3** Put each command in its own function, such as `show_stock()` and `take_out()`. Does the main loop become easier to read? Is anything harder?

<!-- answer -->

**4.4** Add a short note at the top of your program for a new user: what the program is for and the list of commands.

<!-- answer -->

## 5. Release and Review

**5.1** Ask somebody outside your pair to use the program for a few minutes without your help. Where did they get stuck? Write down one change you would make.

<!-- answer -->

## 6. More to Try

1. Add a command `report` that prints everything that is out, grouped by person.
2. Add a date to each loan, typed in by hand, and list loans older than a date the person gives.
3. Four lists in step are hard to manage. Python has a type called a dictionary that stores a value under a name, like `{"router": 2}`. Try it for the counts and see whether the code gets shorter.
4. Design a stock screen with a heading, a line under it, and the low items marked.

```python exec
id: more-to-try-1
# your experiments here
```
