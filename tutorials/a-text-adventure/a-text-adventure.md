---
title: "A Text Adventure: Rooms, Things and a Goal"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO5]
  4-week-three-a-goal:
    covers: [PDP-LO10]
---

# A Text Adventure: Rooms, Things and a Goal

In a text adventure, the program describes a place, and the player types where to go and what to do. There are no pictures, so the writing makes the world. On this page we build a small one: a few rooms, some things to pick up, and a goal to reach.

The project has three stages, about one week each. Each stage ends with a game that someone can play. This project suits pairs where one person enjoys writing the world and the other enjoys making the rules work, but either person can do either job.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Draw a map of four to six rooms on paper, with arrows for the ways between them. Give each room a name and one sentence of description.

<!-- answer -->

**1.2** Write a short sample run: the player starts somewhere, moves twice, and picks something up.

<!-- answer -->

**1.3** What is the goal of your game? How does the player win?

<!-- answer -->

## 2. Week One: Moving Between Rooms

Each room has a name, a description and a list of exits. Each exit is a pair: a direction and the room it leads to.

```python exec
id: week-one-moving-between-rooms-1
rooms = ["hall", "server room", "kitchen"]
descriptions = [
    "A long hall. A fan hums somewhere.",
    "Rows of blinking lights. It is very cold.",
    "A kettle and a pile of cups.",
]
exits = [
    [["north", "server room"], ["east", "kitchen"]],
    [["south", "hall"]],
    [["west", "hall"]],
]
```

**2.1** Run the cell above. Then predict what each line prints, and run it.

```python exec
id: week-one-moving-between-rooms-2
print(rooms.index("hall"))
print(exits[0])
print(exits[0][1])
print(exits[0][1][1])
```

<!-- answer -->

**2.2** Write a game loop. The player starts in the hall. Each turn the program prints the room's description and its exits, asks for a direction, and moves the player if that exit exists. Typing `quit` ends the game.

```python exec
id: week-one-moving-between-rooms-3
# your game here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Keep the player's room in a variable, `here = "hall"`.
2. Find the room's position with `rooms.index(here)`, and use it to print the description.
3. Loop over the room's exits. If the first part matches what the player typed, set `here` to the second part.
4. If no exit matched, print "You can't go that way."

</details>

**2.3** Replace our three rooms with the rooms from your map. Walk through every exit to check that each one leads where the map says.

<!-- answer -->

## 3. Week Two: Things to Pick Up

**3.1** Add a list of things for each room, such as `[["key"], [], ["cup"]]`, and a list `carrying = []` for the player. Print the things in each room with its description.

<!-- answer -->

**3.2** Add `take`, which moves a thing from the room to `carrying`, and `drop`, which moves it back. Add `inventory`, which lists what the player is carrying.

<!-- answer -->

**3.3** Your game loop is growing. Put each command in its own function, such as `go(direction)` and `take(thing)`. Which variables does every function need to see?

<!-- answer -->

## 4. Week Three: A Goal

**4.1** Add a locked exit: the player can only go that way while carrying a certain thing. Where in your code does this check belong?

<!-- answer -->

**4.2** Add the goal from 1.3. When the player reaches it, print an ending and stop the game.

<!-- answer -->

**4.3** Write a walkthrough: the exact commands that win the game, in order. Type them in and check that they work. If you change the map later, run the walkthrough again.

<!-- answer -->

## 5. Release and Review

**5.1** Give your game to another pair without telling them the walkthrough. Watch them play, and do not help. Where did they get lost? Which commands did they try that your game does not know?

<!-- answer -->

**5.2** Add the most common command they tried, or a message that points them to the commands your game knows.

<!-- answer -->

## 6. More to Try

1. Add `look` to print the description again, and `help` to list the commands.
2. Count the player's moves and print the count at the end.
3. Add a character who says something different when the player carries a certain thing.
4. Design how each room appears on screen, with its name as a heading.

```python exec
id: more-to-try-1
# your experiments here
```
