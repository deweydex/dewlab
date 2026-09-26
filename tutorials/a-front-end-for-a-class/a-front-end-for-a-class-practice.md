---
title: "A front end: letting someone use your classes — Practice"
practice_for: a-front-end-for-a-class
year: "2026-2027"
version: 2026.09.26.1
---

# A front end: letting someone use your classes — Practice

This page has problems on front ends, commands and checking what people
type, and three from earlier pages. Try each problem before you open anything under it,
and run the cells to test your guesses.

## 1. Four commands

```python exec
id: four-commands-1
def run_choice(choice):
    if choice == "attack":
        print("You swing at the troll.")
    elif choice == "look":
        print("A cave, and a troll.")
    elif choice == "quit":
        return False
    else:
        print("Not a command:", choice)
    return True

results = []
for choice in ["look", "Look", "quit", "attack"]:
    results.append(run_choice(choice))
print(results)
```

```predict
What will the last line print?

- [True, True, False, True]
  - Every command returns True except quit, and an unknown one is answered, not stopped.
- [True, False, False, True]
  - `Look` is not a command, so it stops the game.
- [True, True, False]
  - Nothing runs after quit.
```

<details class="dl-answer"><summary>why</summary>

`[True, True, False, True]`. `Look`, with a capital, is not a command, so
it prints `Not a command: Look` and returns `True`. `quit` returns
`False`, but the list loop does not stop for it. Only a `while` loop that
checks the answer would stop.

</details>

## 2. Reading a number

A player types how far to dive, as text. Can you write `read_metres(text)`,
which returns the number if the text is a whole number of metres, and
`None` if it is not? Spaces at the ends are fine.

```python exec
id: reading-a-number-1
def read_metres(text):
    return int(text)

print(read_metres("120"))
```

```inputs
read_metres("120")
read_metres(" 40 ")
read_metres("-5")
read_metres("ten")
read_metres("")
```

```hint
`.strip()` removes spaces at the ends. `.isdigit()` answers whether every
character is a digit. What should happen before `int()` is ever called?
```

```solution
def read_metres(text):
    text = text.strip()
    if not text.isdigit():
        return None
    return int(text)

print(read_metres("120"))
---
120, 40, then `None` for "-5", "ten" and the empty text. `int("ten")`
would stop with a `ValueError`, so the check comes first. "-5" is refused
too, since `-` is not a digit: a dive is never negative.
```

## 3. Why keep them apart?

`run_choice` decides what a command means, and a separate loop asks for
it. What would be lost if `run_choice` called `input()` itself?

<details class="dl-answer"><summary>answer</summary>

It could no longer be tested with a list of commands. Every test would
wait for somebody to type. And it could not be given a menu as a second
front end without being written again. With one job each, you can test
it and reuse it.

</details>

## 4. What the menu does

```python
command = dropdown("What now?", ["look", "attack", "rest", "quit"])
still_playing = run_choice(ada, grog, command.value)
```

```question
id: what-the-menu-does-1
type: fill-in-the-blank

- Each run of the cell plays {one turn|every command in the menu|until quit}.
- `command.value` is {whichever command is chosen when the cell runs|always the first command in the list}.
- A player {cannot|can} choose a command that is not in the menu.
```

<details class="dl-answer"><summary>why</summary>

Each run reads the menu once, and calls `run_choice` once. `command.value`
is whatever is chosen at that moment, and the page remembers the choice
between runs. The menu offers only four commands, so a mistyped one cannot
happen. The `else` in `run_choice` is still there for front ends that let
people type.

</details>

## 5. A command that goes too far

A player's command `dive` calls `submarine.dive(50)`. They press it ten
times at 400 m of hull. Where should the refusal come from: the front
end, or the submarine?

<details class="dl-answer"><summary>one answer</summary>

The submarine. `dive` already keeps the hull limit, for every caller: this
front end, the menu, and any front end written next year.
A front end that checks the limit itself would be a second copy of the
rule, and the two copies could become different.

</details>

## 6. From earlier: a promise for run_choice

From *Documenting a class*. What should the docstring of `run_choice` say
about a command it does not know?

<details class="dl-answer"><summary>one answer</summary>

It should say that it prints that the text is not a command, and returns
`True`, so the game continues. That is the refusal a caller most needs to know about,
since players type something unexpected all the time.

</details>

## 7. From earlier: a test for a front end

From *Testing a class*. Can you write a test that checks `run_choice`
from problem 1 returns `False` for `quit`, and `True` for a word that is
not a command?

<details class="dl-answer"><summary>answer</summary>

```python
def test_quit_stops_and_nonsense_does_not():
    assert run_choice("quit") == False
    assert run_choice("xyzzy") == True
```

Because `run_choice` is kept apart from `input()`, the test is only two
lines. The printing still happens, and the test ignores it.

</details>

## 8. From earlier: one front end, every kind

From *Inheritance*. A front end calls `probe.burn(10)`. The probe might be
a `Probe` or a `Lander`. Does the front end need to check which?

<details class="dl-answer"><summary>answer</summary>

No. Each object runs its own class's version: a landed lander refuses
through its own `can_burn`, and the front end prints whatever happened.
That is polymorphism, working in a front end.

</details>
