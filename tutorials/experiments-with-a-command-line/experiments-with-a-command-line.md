---
title: "Planning a Command Line: A Small System of Our Own"
year: "2026-2027"
version: 2026.11.26.2
covers:
  2-a-user-flow:
    covers: [PDP-LO5, PDP-LO6]
  3-agreements-between-the-parts:
    covers: [PDP-LO12]
  4-a-menu-that-runs:
    touches: [PDP-LO6]
---

# Planning a Command Line: A Small System of Our Own

A command line is a program that waits for you to type, does what you asked, and then waits again. Routers, switches and servers are often run this way. In the next few pages we build a small one of our own, inside a notebook. It has four parts:

1. a login that checks a username and a password,
2. a menu that lists the apps and starts the one you choose,
3. a few apps: a to-do list, a notes app and a calculator,
4. a way to go back to the menu, and a way to log out.

Each pair chooses the part they want to build, and at the end we join the parts into one program. If nobody chooses a part this time, the menu keeps a "coming soon" line for it, and the part can wait for another day. Some pairs care most about how the program looks, and others care most about what it does. A program needs both, so either is a good place to start. This page comes before any of that. Here we decide what the program should look like and what it should do, so that the parts fit together when we join them.

There are questions on this page to answer in words. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. A Sample Run

Here is one possible session with the finished program. The lines after `>` and `:` are what the person typed.

```text
Username: grace
Password: cobol
Welcome, grace.

1  To-do list
2  Notes
3  Calculator
q  Log out
> 3

Calculator. Type back to return to the menu.
First number: 12
Operation (+ - * /): /
Second number: 4
12 / 4 = 3.0
First number: back

1  To-do list
2  Notes
3  Calculator
q  Log out
> q
Goodbye, grace.
```

**1.1** Read the session from top to bottom. Every line is either something the program printed or something the person typed. Which lines did the person type?

<!-- answer -->

**1.2** The program never asks "Do you want to log in?". It starts by asking for a username. Name two other things the program does without being asked.

<!-- answer -->

**1.3** Find one place where this session could go wrong if the person typed something unexpected. What might they type, and what should the program do then?

<!-- answer -->

## 2. A User Flow

A user flow is a plan of every path a person can take through a program. One way to write it is as numbered steps, with a note at each step that says where the person goes next. Here is a user flow for the menu.

```text
MENU
1. Show the list of apps.
2. Ask for a choice.
3. If the choice is 1, go to TO-DO. When it finishes, come back to step 1.
4. If the choice is 2, go to NOTES. When it finishes, come back to step 1.
5. If the choice is 3, go to CALCULATOR. When it finishes, come back to step 1.
6. If the choice is q, say goodbye and stop.
7. For anything else, say the choice is not on the menu, and go back to step 1.
```

Words in capitals are the names of other parts. A drawing with boxes and arrows shows the same thing, and some people find it easier to read. Use whichever suits you.

**2.1** Step 7 deals with choices that are not on the menu. Why does a menu need a step like this?

<!-- answer -->

**2.2** Write a user flow for the login, in the same style. Start with "Ask for a username." Include what happens when the username does not exist, and what happens when the password is wrong.

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. List the two questions the login asks.
2. After each question, there are two possible answers: right or wrong. Write what happens for each one.
3. When everything is right, where does the person go next?
4. Can the person try again after a mistake? How many times?

</details>

**2.3** Write a user flow for the app your pair is building. Then write a short sample run for it, like the one in section 1.

<!-- answer -->

## 3. Agreements Between the Parts

When separate pairs build parts that must join, the pairs need to agree on a few things first. If one app returns to the menu when you type `back` and another when you type `exit`, the finished program is confusing to use.

**3.1** As a class, agree on these, and write the answers down where every pair can see them.

1. What does a person type to go back to the menu from any app?
2. What does the prompt look like? (In the sample run it is `> `.)
3. What does the program say when it does not understand what was typed?
4. After the login, which value must the rest of the program know? (Look at the last line of the sample run.)

<!-- answer -->

**3.2** Which part does each pair want to build? A table like this one is enough. A part with no pair is fine.

| Part | Pair |
|---|---|
| Login | |
| Menu | |
| Calculator | |
| Notes | |
| To-do list | |
| How the screens look | |

<!-- answer -->

## 4. A Menu That Runs

This cell is a first version of the menu. The apps do not exist yet, so each choice only prints a message. Run it and try each choice.

```python exec
id: a-menu-that-runs-1
while True:
    print()
    print("1  To-do list")
    print("2  Notes")
    print("3  Calculator")
    print("q  Log out")
    choice = input("> ")
    if choice == "1":
        print("The to-do list is coming soon.")
    elif choice == "2":
        print("The notes app is coming soon.")
    elif choice == "3":
        print("The calculator is coming soon.")
    elif choice == "q":
        print("Goodbye.")
        break
    else:
        print("That is not on the menu:", choice)
```

**4.1** Type `q`. Which line stops the loop?

<!-- answer -->

**4.2** Run the menu again and type `Q`, then `3 ` with a space after it, then press Enter without typing anything. What does the menu do each time? Which of these should it accept?

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. The text methods `strip` and `lower` were on the page about text. What does each one do?
2. Where in the cell could you use them, so that every later line sees the cleaned-up choice?

</details>

**4.3** Compare the cell with the user flow in section 2. Which line of code matches each step of the flow?

<!-- answer -->

**4.4** Change the menu so it matches the agreements from 3.1. Add an app of your own to the menu if you like, even if it only prints "coming soon".

```python exec
id: a-menu-that-runs-2
# your menu here
```

```solution
while True:
    print()
    print("1  To-do list")
    print("2  Notes")
    print("3  Calculator")
    print("q  Log out")
    choice = input("> ").strip().lower()
    if choice == "1":
        print("The to-do list is coming soon.")
    elif choice == "2":
        print("The notes app is coming soon.")
    elif choice == "3":
        print("The calculator is coming soon.")
    elif choice == "q":
        print("Goodbye.")
        break
    else:
        print("That is not on the menu:", choice)
```

```typed
3
 Q
```

## 5. How the Screens Look

A command line has no buttons or colours, but it can still look tidy or messy. Lines of symbols, spaces and capital letters can do most of the design. Run this cell.

```python exec
id: how-the-screens-look-1
width = 30
print("+" + "-" * width + "+")
print("|" + "MAIN MENU".center(width) + "|")
print("+" + "-" * width + "+")
print("|" + "  1  To-do list".ljust(width) + "|")
print("|" + "  2  Notes".ljust(width) + "|")
print("|" + "  3  Calculator".ljust(width) + "|")
print("|" + "  q  Log out".ljust(width) + "|")
print("+" + "-" * width + "+")
```

**5.1** Change `width` to 20, and then to 50. What happens to the box? Which part of each line keeps the right-hand edge straight?

<!-- answer -->

**5.2** Try `"MAIN MENU".center(width, "*")`, then `.ljust` and `.rjust` in place of `.center`. What does each one do?

<!-- answer -->

**5.3** Design a screen of your own: a welcome screen after the login, a heading for an app, or a new look for the whole menu. Write it as a sample first, then make Python print it.

```python exec
id: how-the-screens-look-2
# your screen here
```

**5.4** If every app draws its own boxes in its own way, the joined program looks patchy. What would the class need to agree on so the screens match?

<!-- answer -->

## 6. Before You Write Code

Each part has its own page: the login, the calculator, the notes app and the to-do list. A pair working on the menu or on how the screens look can use this page and borrow from the others. Every page starts with the same two questions as this one.

1. What should the screen look like? Write a sample run.
2. What can the person do, and where does each choice lead? Write a user flow.

The code comes after that. Keep your sample run and your user flow, because you will test the finished code against them.
