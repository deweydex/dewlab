---
title: "Experiments with a notes app: keeping titles and text together"
year: "2026-2027"
version: 2026.11.26.1
---

# Experiments with a notes app: keeping titles and text together

A note has a title and some text. Our notes app keeps them in two lists, like the usernames and passwords in the login. The first title goes with the first text, the second with the second, and so on. The app can show the list of titles, open a note to read it, and write a new one.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan first

**1.1** Write a sample run where someone looks at the list of notes, reads one, writes a new one, and then goes back to the menu.

<!-- answer -->

**1.2** The app needs commands, such as `list`, `read` and `new`. Choose your own command words, and write a user flow that shows where each command leads.

<!-- answer -->

**1.3** What should happen when someone asks to read a note that does not exist? What should happen when someone writes a new note with a title that is already used?

<!-- answer -->

## 2. Two lists that go together

```python exec
id: two-lists-that-go-together-1
titles = ["shopping", "router setup"]
texts = ["milk, bread, coffee", "admin page is at 192.168.1.1"]
```

**2.1** Run the cell above first. Then predict what each line prints, and run it.

```python exec
id: two-lists-that-go-together-2
print(len(titles))
print(titles.index("router setup"))
print(texts[titles.index("router setup")])
print("homework" in titles)
```

<!-- answer -->

**2.2** Print every title on its own line, with a number in front, starting from 1.

```python exec
id: two-lists-that-go-together-3
# your code here
```

```solution
for position in range(len(titles)):
    print(position + 1, titles[position])
```

**2.3** Add a new note with the title `"ideas"` and the text `"a game about cables"`. Print both lists afterwards to check that they still line up.

```python exec
id: two-lists-that-go-together-4
# your code here
```

```solution
titles.append("ideas")
texts.append("a game about cables")
print(titles)
print(texts)
```

**2.4** Run the cell in 2.3 a second time. What happens to the lists? Why might that be a problem in a real app?

<!-- answer -->

## 3. The app, one command at a time

**3.1** Write a notes app with a `while` loop that asks for a command. Start with only two commands: one that lists the titles, and the agreed word for going back to the menu.

```python exec
id: the-app-one-command-at-a-time-1
# your notes app here
```

**3.2** Add a command that reads a note. It asks for a title and prints the text. Test it with a title that does not exist.

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. Ask for the title with `input`.
2. Use `in` to check whether the title is in `titles`.
3. If it is, find its position with `index`, and print the text at that position.
4. If it is not, print a message.

</details>

**3.3** Add a command that writes a new note. It asks for a title and a text, and adds both to the lists.

<!-- answer -->

```solution
while True:
    command = input("notes> ").strip().lower()
    if command == "back":
        break
    elif command == "list":
        for position in range(len(titles)):
            print(position + 1, titles[position])
    elif command == "read":
        title = input("Title: ").strip()
        if title in titles:
            print(texts[titles.index(title)])
        else:
            print("There is no note called", title)
    elif command == "new":
        title = input("Title: ").strip()
        text = input("Text: ")
        titles.append(title)
        texts.append(text)
        print("Saved.")
    else:
        print("The commands are list, read, new and back.")
```

```typed
list
read
shopping
new
ideas
a game about cables
back
```

**3.4** Compare your app with your user flow from 1.2. Is there a path in the flow that the code does not follow yet? Is there anything the code does that the flow does not show?

<!-- answer -->

## 4. More to try

Choose any of these, or invent your own.

1. Let the person read a note by its number as well as by its title.
2. Add a command that deletes a note. Remember that it must leave both lists lined up. The list method `pop` removes an item at a position.
3. Add a command that searches every text for a word and lists the titles of the notes that contain it.
4. Add a command that adds more text to the end of an existing note.

```python exec
id: more-to-try-1
# your experiments here
```
