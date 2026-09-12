---
title: "Rendering Tour"
slug: rendering-tour
module: fixtures
year: "2026-2027"
series: e2e
version: 2026.08.23.1
covers:
  matplotlib:
    covers: [MIT-5.10]
  when-it-goes-wrong:
    covers: [PDP-LO9]
---

<!--
A test fixture, not a tutorial. Its cells exist to exercise every branch of the
output renderer in one page — printed text, a last expression, a DataFrame, a
figure, a traceback, the tools, the widgets — so the browser tests can drive
them all against one Pyodide boot. Nothing here is meant to teach anything, and
it deliberately does not live in tutorials/.

Keep the cell ids stable: the tests select on them.
-->

## Running code

Every cell below is live. Edit it, press **Run** (or Ctrl-Enter), and the
output appears directly underneath — the same prose, cell, output rhythm every
dewlab tutorial follows.

```python exec
id: plain-python
# Printed text and the value of the last expression both show up.
for n in range(3):
    print("counting:", n)

2 ** 10
```

## numpy

Whole arrays at once.

```python exec
id: numpy-basics
hint: Arrays behave like a whole column at once, not one number at a time.
import numpy as np

readings = np.array([12.5, 13.0, 11.75, 14.25])
print("mean:", readings.mean())
readings * 2
```

## pandas

A DataFrame renders as a table.

```python exec
id: pandas-table
import pandas as pd

df = pd.DataFrame({
    "country": ["Ireland", "Spain", "Japan", "Kenya"],
    "life_expectancy": [82.4, 83.2, 84.8, 66.7],
})
df[df["life_expectancy"] > 75]
```

## SQL

A `sql exec` cell's code is SQL text, not Python — it runs against the same
shared `db` every SQL cell on this page uses, and a `select` renders as a
table exactly like a DataFrame does.

```sql exec
id: sql-basics
CREATE TABLE creatures (name TEXT, legs INTEGER);
INSERT INTO creatures VALUES ('spider', 8), ('hen', 2), ('dog', 4);
SELECT * FROM creatures WHERE legs > 2;
```

A Python cell reads the same `db` a SQL cell just wrote to.

```python exec
id: sql-read-from-python
import pandas as pd

pd.read_sql("SELECT COUNT(*) AS n FROM creatures", db)
```

## matplotlib

A figure renders as an image.

```python exec
id: matplotlib-figure
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x))
plt.title("One period of sin(x)")
```

Every textbook ends a plot with `plt.show()`, so students write it. It renders
the figure rather than warning about a canvas it cannot open.

```python exec
id: matplotlib-show
import matplotlib.pyplot as plt

plt.plot([1, 4, 9, 16])
plt.title("Squares")
plt.show()
print("after the plot")
```

## When it goes wrong

Errors are part of the lesson.

```python exec
id: error-traceback
# A mistake should point at the student's own line,
# not at dewlab's plumbing.
total = 0
for value in [1, 2, "three"]:
    total += value
```

## A hint that waits for an attempt

Run this cell as it is and it fails. The hint below stays hidden until the
same error has come up twice; a second one after three errors in all; and
none of that once `total` is 6.

```python exec
id: staged-hints
expect: total == 6
total = 0
for value in [1, 2, 3]:
    total = total + valeu
```

```hint
after: 2 identical errors
What does the last line of the message say Python could not find? Is that
word spelled the same way on the line above it?
```

```hint
after: 3 errors
title: some steps
1. Read the name in the error message.
2. Find that name in your cell, letter by letter.

Then $t = \sum v$ once it runs.
```

## Site editor

A live HTML/CSS/JS editor: `hero`'s two panes are grouped by their shared
`site:` name.

```html site
id: site-hero-html
site: hero
<button id="go">Click me</button>
<p id="out">not yet</p>
```

```css site
id: site-hero-css
site: hero
#go { font-weight: bold; }
```

```js site
id: site-hero-js
site: hero
document.getElementById("go").addEventListener("click", () => {
  document.getElementById("out").textContent = "clicked";
});
console.log("script loaded");
```

An HTML+CSS-only editor gets no JavaScript pane, no Run button, and no
console.

```html site
id: site-quiet-html
site: quiet
<p>No script here.</p>
```

```css site
id: site-quiet-css
site: quiet
p { color: teal; }
```

## Checking your own answer

```python exec
id: tools-show-check
hint: check() is feedback, not a mark. Nothing is recorded.
show("show() renders anything, mid-cell.")
show_table(df, max_rows=3, caption="First three rows")

check(sum([1, 2, 3]), 6, label="Does the total come out right?")
check(0.1 + 0.2, 0.3)          # floats compare within a tolerance
check(2 + 2, 5)                # and a wrong answer says so
```

## Widgets

Type something, then press the button.

```python exec
id: tools-widgets
name = text_input("Your name", value="")
units = dropdown("Units", ["metric", "imperial"])

def greet():
    print(f"Hello {name.value or 'there'} — using {units.value} units.")

button("Say hello", on_click=greet)
```
