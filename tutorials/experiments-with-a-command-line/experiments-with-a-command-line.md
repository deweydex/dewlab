---
title: "Experiments with a command line: planning a small system of our own"
year: "2026-2027"
version: 2026.11.26.1
---

# Experiments with a command line: planning a small system of our own

A command line is a program that waits for you to type, does what you asked, and then waits again. Routers, switches and servers are often run this way. In the next few pages we build a small one of our own, inside a notebook. It has four parts:

1. a login that checks a username and a password,
2. a menu that lists the apps and starts the one you choose,
3. a few apps: a to-do list, a notes app and a calculator,
4. a way to go back to the menu, and a way to log out.

Different pairs build different parts, and at the end we join the parts into one program. This page comes before any of that. Here we decide what the program should look like and what it should do, so that the parts fit together when we join them.

There are questions on this page to answer in words. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. A sample run

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

## 2. A user flow

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

## 3. Agreements between the parts

When separate pairs build parts that must join, the pairs need to agree on a few things first. If one app returns to the menu when you type `back` and another when you type `exit`, the finished program is confusing to use.

**3.1** As a class, agree on these, and write the answers down where every pair can see them.

1. What does a person type to go back to the menu from any app?
2. What does the prompt look like? (In the sample run it is `> `.)
3. What does the program say when it does not understand what was typed?
4. After the login, which value must the rest of the program know? (Look at the last line of the sample run.)

<!-- answer -->

**3.2** Which pair is building which part? A table like this one is enough.

| Part | Pair | What it needs from the others |
|---|---|---|
| Login | | |
| Calculator | | |
| Notes | | |
| To-do list | | |
| Menu | | |

<!-- answer -->

## 4. A menu that runs

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

## 5. Before you write code

Each pair now has its own page: the login, the calculator, the notes app and the to-do list. Every page starts with the same two questions as this one.

1. What should the screen look like? Write a sample run.
2. What can the person do, and where does each choice lead? Write a user flow.

The code comes after that. Keep your sample run and your user flow, because you will test the finished code against them.
