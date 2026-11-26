---
title: "Experiments with a to-do list: showing, adding, changing and removing"
year: "2026-2027"
version: 2026.11.26.2
---

# Experiments with a to-do list: showing, adding, changing and removing

A to-do list app does four things. It shows the list, adds an item, changes an item, and removes an item. People count from 1, and Python counts list positions from 0, so this page is mostly about the difference between the two.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan first

**1.1** Write a sample run where someone shows the list, adds an item, changes the second item, removes the first item, and shows the list again.

<!-- answer -->

**1.2** When someone wants to change or remove an item, how do they say which one? They could type its number or its words. Choose one, and give a reason.

<!-- answer -->

**1.3** Write the user flow for your to-do list. Include what happens when someone types a number that is not on the list.

<!-- answer -->

## 2. Counting from 1 and from 0

```python exec
id: counting-from-1-and-from-0-1
todos = ["check the cables", "update the router", "back up the server"]
```

**2.1** Run the cell above first. Then run this one. Do the numbers on the screen match the positions Python uses?

```python exec
id: counting-from-1-and-from-0-2
for position in range(len(todos)):
    print(position + 1, todos[position])
```

<!-- answer -->

**2.2** A person types `2` because they want to change "update the router". Predict what each line prints, then run it.

```python exec
id: counting-from-1-and-from-0-3
choice = "2"
print(todos[int(choice)])
print(todos[int(choice) - 1])
```

<!-- answer -->

**2.3** Try `todos[3]`, then `todos[-1]`, then `todos[int("0") - 1]`. Which one gives an error? Which one gives an item the person did not ask for, with no error at all?

```python exec
id: counting-from-1-and-from-0-4
print(todos[3])
```

<!-- answer -->

**2.4** Write a condition that is `True` only when the number the person typed is on the screen, from 1 up to the length of the list.

```python exec
id: counting-from-1-and-from-0-5
number = 4
# your condition here
```

```solution
number = 4
print(1 <= number <= len(todos))
```

## 3. The four actions

Try each action on its own first, then join them in section 4.

**3.1** Add `"replace the old switch"` to the end of the list.

**3.2** Change the item the person calls number 2 to `"update the router firmware"`.

**3.3** Remove the item the person calls number 1. The method `pop` removes the item at a position, and `remove` removes an item by its value. Which one fits better here?

**3.4** Show the list again, with numbers from 1.

```python exec
id: the-four-actions-1
# your code for 3.1 to 3.4 here
```

```solution
todos = ["check the cables", "update the router", "back up the server"]
todos.append("replace the old switch")
todos[2 - 1] = "update the router firmware"
todos.pop(1 - 1)
for position in range(len(todos)):
    print(position + 1, todos[position])
```

**3.5** After you remove item 1, what number does "update the router firmware" have on the screen? Why does this matter if the person removes two items in a row?

<!-- answer -->

## 4. The app

**4.1** Write the to-do app with a `while` loop that asks for a command. Use your user flow from 1.3. Start with showing and adding, test them, and then add changing and removing.

```python exec
id: the-app-1
# your to-do app here
```

```solution
todos = ["check the cables", "update the router", "back up the server"]
while True:
    command = input("todo> ").strip().lower()
    if command == "back":
        break
    elif command == "show":
        for position in range(len(todos)):
            print(position + 1, todos[position])
    elif command == "add":
        todos.append(input("New item: "))
    elif command == "edit" or command == "delete":
        number = int(input("Item number: "))
        if 1 <= number <= len(todos):
            if command == "edit":
                todos[number - 1] = input("New text: ")
            else:
                todos.pop(number - 1)
        else:
            print("There is no item", number)
    else:
        print("The commands are show, add, edit, delete and back.")
```

```typed
add
replace the old switch
edit
2
update the router firmware
delete
1
delete
9
show
back
```

**4.2** What happens when the list is empty and someone shows it? Make the app print a message such as "Nothing to do." instead.

<!-- answer -->

## 5. More to try

Choose any of these, or invent your own.

1. Mark an item as done without removing it. One way is to add `[x] ` to the front of its text.
2. Add a command that removes every item that is done.
3. Let the person move an item up or down the list.
4. Ask "Are you sure?" before removing an item.
5. Design how the list looks, with a heading, a line under it, and done items that stand out.

```python exec
id: more-to-try-1
# your experiments here
```
