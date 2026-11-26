---
title: "Experiments with joining the parts: one program from many pieces"
year: "2026-2027"
version: 2026.11.26.2
---

# Experiments with joining the parts: one program from many pieces

Each pair now has a part that works on its own. The class may not have built every part. That is fine, because the menu keeps a "coming soon" line for any part that is missing. This page joins the parts we have into one program. To do that, we give each part a name, so the menu can start it by name. A block of code with a name is called a function. The next pages say much more about functions. Here we only need the simplest kind.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. A block of code with a name

```python exec
id: a-block-of-code-with-a-name-1
def say_hello():
    print("Hello from inside a function.")
    print("This is the second line.")
```

**1.1** Run the cell above. Nothing appears below it. Then run the cell below. What changed?

```python exec
id: a-block-of-code-with-a-name-2
say_hello()
say_hello()
```

<!-- answer -->

The line that starts with `def` defines the function: it gives the block a name. The indented lines under it are the block. Writing the name with brackets, `say_hello()`, runs the block. That is called calling the function.

**1.2** Remove the brackets, so the line is only `say_hello`. Run it. What appears, and does the block run?

<!-- answer -->

**1.3** Call `say_goodbye()` before you define it. What error comes back? What does that tell you about the order of the cells?

```python exec
id: a-block-of-code-with-a-name-3
say_goodbye()
```

<!-- answer -->

## 2. Each part becomes a function

**2.1** Put your pair's part inside a function. Use the name the class agreed on, such as `run_calculator`, `run_notes` or `run_todo`. Indent every line of your code once, under the `def` line. Then call the function to check it still works.

```python exec
id: each-part-becomes-a-function-1
def run_calculator():
    print("Calculator. Type back to return to the menu.")
    # your calculator here, indented

run_calculator()
```

**2.2** Now put the menu in a cell of its own. For each part that exists, replace its "coming soon" line with a call to the matching function. Leave the other lines as they are.

```python exec
id: each-part-becomes-a-function-2
# the menu, calling the other parts
```

## 3. Where the notes live

**3.1** Here is a very small notes app as a function. It creates its list inside the function. Run both cells. Add a note, type `back`, and then run the second cell again. Is your note still there?

```python exec
id: where-the-notes-live-1
def run_notes():
    titles = []
    while True:
        command = input("notes> ")
        if command == "back":
            break
        elif command == "new":
            titles.append(input("Title: "))
        print(titles)
```

```python exec
id: where-the-notes-live-2
run_notes()
```

<!-- answer -->

**3.2** Move the line `titles = []` above the `def` line, with no indent. Run both cells again, add a note, go back, and open the notes again. What changed, and why?

<!-- answer -->

**3.3** Which lists in your own part need to stay alive between visits from the menu? Where should they be created?

<!-- answer -->

## 4. The login hands back a name

The menu needs to know who logged in. A function can hand a value back to the line that called it, with the word `return`. This function hands back the username after a good login, and `None` after three wrong tries. `None` is Python's value for "nothing".

```python exec
id: the-login-hands-back-a-name-1
usernames = ["ada", "grace", "linus"]
passwords = ["engine", "cobol", "penguin"]

def log_in():
    for tries in range(3):
        name = input("Username: ").strip().lower()
        password = input("Password: ")
        if name in usernames and password == passwords[usernames.index(name)]:
            return name
        print("Wrong username or password.")
    return None
```

**4.1** Run the cell above, then run this one twice: once with a good login and once with three wrong tries. What does `user` hold each time?

```python exec
id: the-login-hands-back-a-name-2
user = log_in()
print(user)
```

<!-- answer -->

**4.2** The function has no `break`, but the loop stops early after a good login. Which word stops it?

<!-- answer -->

## 5. The whole program

**5.1** Join everything in one cell. The program logs in first. If the login works, it greets the person by name and shows the menu. When the person logs out, it says goodbye by name. If the login fails, the menu never appears.

```python exec
id: the-whole-program-1
# the whole program here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Make sure every cell that defines a function has been run.
2. Call `log_in()` and store what it hands back.
3. Use `if` to check whether the value is `None`.
4. Put the menu loop inside the branch where the login worked.

</details>

**5.2** Test the whole program against the sample run from the planning page. Where does it still differ? Decide as a class which differences to fix.

<!-- answer -->

**5.3** Do all the screens look as if they belong to one program? If your class designed a shared look, use it in every part.

<!-- answer -->
