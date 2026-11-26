---
title: "A Word Processor at the Command Line: Lines, Words and Wrapping"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO6]
  3-week-two-finding-and-replacing:
    covers: [PDP-LO8]
  4-week-three-wrapping-and-aligning:
    covers: [PDP-LO2, PDP-LO10]
---

# A Word Processor at the Command Line: Lines, Words and Wrapping

Before word processors had windows, people edited text one line at a time at a command line. Network engineers still do this when they change a configuration file on a router or a server. On this page we build a small word processor of that kind. It shows a document with line numbers, lets you add, change and delete lines, finds and replaces words, counts them, and wraps long text to a width you choose.

The project has three stages, about one week each. Each stage ends with a program that works.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Write a sample run where someone writes three lines, fixes a spelling mistake in the second line, and asks how many words the document has.

<!-- answer -->

**1.2** Choose your commands, and write one line of pseudocode for each. Some commands need a line number, some need words, and some need both. Write down which is which.

<!-- answer -->

**1.3** A word processor changes the person's work, so a mistake can destroy something they wrote. Which commands could lose text? What should the program do before it runs them?

<!-- answer -->

## 2. Week One: A Document of Lines

```python exec
id: week-one-a-document-of-lines-1
document = [
    "hostname lab-router",
    "interface eth0",
    "description link to the switch",
]
```

**2.1** Run the cell above. Then print the document with line numbers starting from 1, with the numbers lined up on the right. The text method `rjust(3)` pads a string on the left to 3 characters.

```python exec
id: week-one-a-document-of-lines-2
# your code here
```

```solution
for position in range(len(document)):
    print(str(position + 1).rjust(3), document[position])
```

**2.2** Write the first version of the program. It repeats until the person types `quit`, and it knows these commands:

1. `show` prints the document with line numbers.
2. `add` asks for a line of text and puts it at the end.
3. `insert` asks for a line number and a line of text, and puts the text before that line.
4. `delete` asks for a line number and removes that line.
5. `edit` asks for a line number and new text, and replaces the line.

```python exec
id: week-one-a-document-of-lines-3
# your word processor here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Start with `show`, `add` and `quit`, and test them.
2. The person counts lines from 1, and the list counts from 0. Where do you subtract 1?
3. The list methods `insert` and `pop` do most of the work for `insert` and `delete`.
4. Check that each line number is on the document before you use it.

</details>

**2.3** Type `insert` with line number 1, then with a number one bigger than the last line. Should both work? What does your program do?

<!-- answer -->

## 3. Week Two: Finding and Replacing

**3.1** Predict what each line prints, then run the cell.

```python exec
id: week-two-finding-and-replacing-1
line = "description link to the switch"
print("switch" in line)
print("Switch" in line)
print(line.replace("switch", "router"))
print(line)
print(line.split())
print(len(line.split()))
```

<!-- answer -->

**3.2** Look at the fourth line of the output. Did `replace` change `line`? What do you need to write to keep the change?

<!-- answer -->

**3.3** Write three functions that take the document as an argument:

1. `find(document, word)` prints the number and text of every line that contains the word.
2. `replace_all(document, old, new)` changes every line, and hands back how many lines changed.
3. `count_words(document)` hands back the number of words in the whole document.

Then add a command for each one.

```python exec
id: week-two-finding-and-replacing-2
def count_words(document):
    # your code here
    return 0

print(count_words(document))
```

```solution
def count_words(document):
    total = 0
    for line in document:
        total = total + len(line.split())
    return total

print(count_words(document))
```

**3.4** `replace_all` changes the list it is given, even though it is inside a function. Test it, and then show the document. Why does the change stay? Compare this with a function that sets a number variable to a new value.

<!-- answer -->

**3.5** Make `find` ignore capital letters, so `find switch` also finds `Switch`. The method `lower` helps.

<!-- answer -->

## 4. Week Three: Wrapping and Aligning

A word processor wraps text: when a line would be too long, the next word moves to a new line. Wrapping is a small algorithm, and it is worth planning on paper first.

**4.1** Take the sentence `the quick brown fox jumps over the lazy dog` and wrap it by hand to a width of 12 characters. Write down each line and its length.

<!-- answer -->

**4.2** Write `wrap(text, width)`, which hands back a list of lines, none longer than `width`, without cutting any word.

```python exec
id: week-three-wrapping-and-aligning-1
def wrap(text, width):
    # your code here
    return [text]

for line in wrap("the quick brown fox jumps over the lazy dog", 12):
    print(line.ljust(12) + "|")
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Split the text into words, and start with an empty list of lines and an empty current line.
2. For each word, check whether the current line plus a space plus the word still fits.
3. If it fits, add the word to the current line. If it does not, put the current line in the list and start a new line with the word.
4. After the loop, the last line is still waiting. Do not forget it.

</details>

```solution
def wrap(text, width):
    lines = []
    current = ""
    for word in text.split():
        if current == "":
            current = word
        elif len(current) + 1 + len(word) <= width:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    if current != "":
        lines.append(current)
    return lines

for line in wrap("the quick brown fox jumps over the lazy dog", 12):
    print(line.ljust(12) + "|")
```

**4.3** Write a test plan for `wrap`, and run each test. Include an empty text, a width of 1, and a single word longer than the width. What should happen to a word that is too long for any line? Decide, and make the code match.

<!-- answer -->

**4.4** Add a command `wrap` that asks for a width and wraps the whole document. Add `centre` and `right`, which show the document centred or aligned to the right at a chosen width. They only change how the document is shown, not the lines themselves.

<!-- answer -->

## 5. Release and Review

**5.1** Give your program to another pair with a short document already in it. Ask them to fix three mistakes you planted in the text, using only your commands. Where did they get stuck?

<!-- answer -->

**5.2** Which command is most likely to lose somebody's work? What did you do about it in 1.3, and did it work?

<!-- answer -->

## 6. More to Try

1. Add `undo`. Before each change, keep a copy of the document with `document.copy()` in a list of copies. `undo` puts the last copy back.
2. Add a spelling check that lists every word not found in a short list of words you type in.
3. Add `stats`: the number of lines, words and characters, and the longest word.
4. Justify the text, so both edges are straight, by sharing extra spaces between the words on each line.

```python exec
id: more-to-try-1
# your experiments here
```
