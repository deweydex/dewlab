---
title: "Experiments with a login: checking a username and a password"
year: "2026-2027"
version: 2026.11.26.2
---

# Experiments with a login: checking a username and a password

A login asks two questions. First it asks who you are, and then it asks you to prove it. On this page the users and their passwords live in two lists. The first username goes with the first password, the second with the second, and so on.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan first

**1.1** Write a sample run for a login where the person gets the password wrong once and right the second time.

<!-- answer -->

**1.2** Write the user flow for the login. If you wrote one on the planning page, copy it here and improve it.

<!-- answer -->

**1.3** Should the login tell the person "That username does not exist", or should it only say "Wrong username or password"? Think about who else might be typing. Write down your choice and your reason.

<!-- answer -->

## 2. Two lists that go together

```python exec
id: two-lists-that-go-together-1
usernames = ["ada", "grace", "linus"]
passwords = ["engine", "cobol", "penguin"]
```

**2.1** Run the cell above first. Then predict what each line below prints, and run it.

```python exec
id: two-lists-that-go-together-2
print("grace" in usernames)
print("Grace" in usernames)
print(usernames.index("grace"))
print(passwords[1])
```

<!-- answer -->

**2.2** Try `usernames.index("bob")`. What error comes back? Which line from 2.1 could you run first to avoid it?

```python exec
id: two-lists-that-go-together-3
print(usernames.index("bob"))
```

<!-- answer -->

**2.3** Using `index` and square brackets, print the password that belongs to `"linus"`, without typing the number 2 anywhere.

```python exec
id: two-lists-that-go-together-4
# your code here
```

```solution
position = usernames.index("linus")
print(passwords[position])
```

**2.4** Add a fourth user with a password of your own. What could go wrong if you add the username to one list and forget the other?

<!-- answer -->

## 3. One try

**3.1** Write a login that asks for a username and a password once. It prints `Welcome, ` and the name when both are right. It prints a message of your choice when either one is wrong. Test every path in your user flow.

```python exec
id: one-try-1
# your login here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Ask for the username with `input`, and store it.
2. Use `in` to check whether the username is in `usernames`. Print something different for yes and no.
3. Inside the yes branch, find the position of the username with `index`.
4. Ask for the password, and compare it with the password at that position.

</details>

```solution
name = input("Username: ")
if name in usernames:
    position = usernames.index(name)
    password = input("Password: ")
    if password == passwords[position]:
        print("Welcome, " + name + ".")
    else:
        print("Wrong username or password.")
else:
    print("Wrong username or password.")
```

```typed
grace
cobol
```

**3.2** Run your login and type ` grace` with a space in front, then `GRACE`. Should either of these work? Change the code to match your answer.

<!-- answer -->

**3.3** Try the password `cobol` for the user `ada`. Does your login let `ada` in? It should not. If it does, which line compares the wrong things?

<!-- answer -->

## 4. Three tries

**4.1** Change your login so the person has three tries. After three wrong tries, the program says so and stops asking.

```python exec
id: three-tries-1
# your login with three tries here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Before a `while` loop, make two variables: `tries = 0` and `logged_in = False`.
2. Put your login from 3.1 inside the loop, and add 1 to `tries` after each wrong answer.
3. When the login is right, set `logged_in` to `True`.
4. The loop should continue while there are tries left and nobody has logged in. How do you write that as a condition?

</details>

```solution
tries = 0
logged_in = False
while tries < 3 and not logged_in:
    name = input("Username: ").strip().lower()
    password = input("Password: ")
    if name in usernames and password == passwords[usernames.index(name)]:
        logged_in = True
        print("Welcome, " + name + ".")
    else:
        tries = tries + 1
        print("Wrong username or password.")
if not logged_in:
    print("Too many tries. Goodbye.")
```

```typed
grace
wrong
grace
cobol
```

**4.2** After the loop ends, the rest of the program needs to know two things: did the login work, and who logged in? Which variables in your code hold those two things?

<!-- answer -->

## 5. Questions to think about

These questions have no single right answer. Talk them over with your pair.

**5.1** When you type the password, it shows on the screen. On a real router or server, it does not. Why not? Look up Python's `getpass` module, and try it in a cell. Does it work in this notebook?

<!-- answer -->

**5.2** The passwords sit in a list in plain text. Anyone who can read the code can read every password. How do real systems check a password without storing it?

<!-- answer -->

**5.3** Many systems lock an account after too many wrong tries. What would that need that your login does not have yet?

<!-- answer -->

**5.4** Design the screen a person sees when the login starts, and the one they see when it works. What should a welcome screen say?

<!-- answer -->

```python exec
id: questions-to-think-about-1
# your experiments here
```
