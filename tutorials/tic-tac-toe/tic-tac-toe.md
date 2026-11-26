---
title: "Tic-Tac-Toe: A Board, a Winner and a Computer Player"
year: "2026-2027"
version: 2026.11.26.1
covers:
  3-week-two-finding-a-winner:
    covers: [PDP-LO2, PDP-LO8]
  4-week-three-a-computer-player:
    covers: [PDP-LO2]
---

# Tic-Tac-Toe: A Board, a Winner and a Computer Player

Tic-tac-toe is played on a grid of nine squares. Two players take turns to put an X or an O in an empty square, and the first to fill a row, a column or a diagonal wins. On this page we build the game for two people, then teach the program to find a winner, and then teach it to play.

The project has three stages, about one week each. Each stage ends with a game that works.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Play a game on paper with your partner. Then number the squares from 0 to 8, left to right and top to bottom. Write down the squares that make each of the eight winning lines.

<!-- answer -->

**1.2** Write pseudocode for one whole game, from an empty board to "X wins" or "a draw".

<!-- answer -->

## 2. Week One: A Board and Two Players

```python exec
id: week-one-a-board-and-two-players-1
board = ["X", " ", "O",
         " ", "X", " ",
         " ", " ", "O"]
print(board[0], "|", board[1], "|", board[2])
```

**2.1** Run the cell above. It prints the top row. Add lines that print the other two rows, with a line of dashes between rows.

<!-- answer -->

**2.2** Put your drawing code in a function `show(board)`. Call it with an empty board, `[" "] * 9`, and with the board above.

```python exec
id: week-one-a-board-and-two-players-2
def show(board):
    # your drawing here
    print(board)

show([" "] * 9)
show(board)
```

```solution
def show(board):
    for start in [0, 3, 6]:
        print(" " + board[start] + " | " + board[start + 1] + " | " + board[start + 2])
        if start != 6:
            print("---+---+---")

show([" "] * 9)
show(board)
```

**2.3** Write the game loop. It shows the board, asks the current player for a square number, puts their mark there, and swaps players. Nine turns fill the board.

```python exec
id: week-one-a-board-and-two-players-3
# your game here
```

**2.4** What happens if a player picks a square that is already taken? What about `9`, or `hello`? Make the game ask again instead.

<!-- answer -->

## 3. Week Two: Finding a Winner

```python exec
id: week-two-finding-a-winner-1
lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
         [0, 3, 6], [1, 4, 7], [2, 5, 8],
         [0, 4, 8], [2, 4, 6]]
```

**3.1** Run the cell above, and compare `lines` with your list from 1.1. Then predict what this prints.

```python exec
id: week-two-finding-a-winner-2
test_board = ["X", "X", "X",
              "O", "O", " ",
              " ", " ", " "]
line = lines[0]
print(test_board[line[0]], test_board[line[1]], test_board[line[2]])
```

<!-- answer -->

**3.2** Write `winner(board)`, which hands back `"X"` or `"O"` if that player has a full line, and `" "` if nobody has.

```python exec
id: week-two-finding-a-winner-3
def winner(board):
    # your code here
    return " "

print(winner(test_board) == "X")
print(winner([" "] * 9) == " ")
print(winner(["O", "X", " ", "X", "O", " ", " ", "X", "O"]) == "O")
```

```solution
def winner(board):
    for line in lines:
        first = board[line[0]]
        if first != " " and first == board[line[1]] and first == board[line[2]]:
            return first
    return " "

print(winner(test_board) == "X")
print(winner([" "] * 9) == " ")
```

**3.3** Why does the solution check that `first != " "`? What goes wrong without it? Try it.

<!-- answer -->

**3.4** Use `winner` in your game, so it stops as soon as someone wins and prints who. If the board fills with no winner, print that it is a draw.

<!-- answer -->

## 4. Week Three: A Computer Player

**4.1** Make O a computer player that picks a random empty square. Put `import random` at the top of your program. Then you can make a list of the empty squares and use `random.choice` to pick one. Play five games against it. How often do you win?

<!-- answer -->

**4.2** Make the computer smarter with two rules. First, if it can win this turn, it does. Second, if X could win on its next turn, the computer blocks that square. How can you use `winner` on a copy of the board to test a move before making it? (`board.copy()` makes a copy.)

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. Loop over the empty squares.
2. For each one, copy the board, put an O there, and ask `winner` about the copy.
3. If O wins on the copy, that is the move.
4. Do the same with an X to find a square to block.

</details>

**4.3** Can you still beat the computer? Which kind of move does it miss?

<!-- answer -->

## 5. Release and Review

**5.1** Ask another pair to play your game. Did they understand which number to type for each square? Change one thing that would make the game easier to use.

<!-- answer -->

**5.2** Your game is made of a few functions: `show`, `winner`, and the computer's move. Which one would you change to make the board bigger, four by four? Which ones would not need to change at all?

<!-- answer -->

## 6. More to Try

1. Keep a score across several games.
2. Let the players choose their own symbols.
3. Number the squares 1 to 9 on the screen, like a phone keypad, and show the numbers in the empty squares.
4. Add a rule that makes the computer take the centre square when it is free. Does it help?

```python exec
id: more-to-try-1
import random
# your experiments here
```
