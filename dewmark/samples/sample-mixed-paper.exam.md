```exam
title: Sample Mixed Paper - Study Skills and Reasoning
exam_code: sample-mixed-2027
version: 2027.01.15.1
total_marks: 50
time_allowed: 90 minutes
student_details: [full name, student number]
calculator: scientific
instructions: |
  Answer every question in Section A. In Section B, answer one of the
  two essay titles. Show your working where a question asks for it; a
  correct answer without working may not receive full marks.
```

```section
name: A
```

## Section A — Short questions

Answer every question in this section.

### Question A1 — Reading a graph

```question
name: a1
marks: 2
topic: graphs
```

The line on a distance-time graph is horizontal between minute 10 and
minute 15.

```answer
name: a1.choice
type: multiple-choice
marks: 2
options:
  - The object is moving at a steady speed.
  - The object is stationary.
  - The object is accelerating.
  - The object is moving backwards.
correct: 2
```

### Question A2 — The parts of an argument

```question
name: a2
marks: 3
topic: reasoning
```

```answer
name: a2.blanks
type: fill-in-the-blank
marks: 3
text: |
  An argument is made of statements. The statements offered as support
  are called the {premises}, the statement they support is called the
  {conclusion}, and an argument whose final statement follows
  necessarily from its support is called {valid}.
```

```marking
marks: 3
guidance:
  - 1 mark per blank; accept "premisses" for the first blank
```

### Question A3 — A quadratic equation

```question
name: a3
marks: 4
topic: algebra
```

Consider the function $f(x) = x^2 - 2x - 8$.

```answer
name: a3.roots
type: numeric-answer
marks: 4
boxes:
  - label: "x ="
    expected: 4
  - label: "x ="
    expected: -2
working_box: yes
hint: "Try factorising: which pair of numbers multiplies to -8 and adds to -2?"
```

```marking
marks: 4
guidance:
  - 2 marks for a correct method (factorising or the formula), shown in
    the working
  - 1 mark for each correct root
```

### Question A4 — A table of values

```question
name: a4
marks: 5
topic: algebra
```

Complete the table of values for $y = x^2 - 4$.

```answer
name: a4.table
type: complete-the-table
marks: 5
columns: [x, -2, -1, 0, 1, 2]
rows:
  - [y, "?", "?", "?", "?", "?"]
expected:
  - [y, 0, -3, -4, -3, 0]
```

```marking
marks: 5
guidance:
  - 1 mark per cell
```

### Question A5 — The shape of the curve

```question
name: a5
marks: 4
topic: graphs
```

Think about the graph of the same function, $y = x^2 - 4$.

```answer
name: a5.sketch
type: describe-a-sketch
marks: 4
shape:
  prompt: The curve opens
  options: ["upward", "downward"]
  correct: 1
features:
  - label: "Crosses the x-axis at ( _ , 0 ) and ( _ , 0 )"
    boxes: 2
    expected: [-2, 2]
  - label: "Lowest point at ( _ , _ )"
    boxes: 2
    expected: [0, -4]
```

```marking
marks: 4
guidance:
  - 1 mark for the shape
  - 1 mark for each correct crossing point
  - 1 mark for the lowest point
```

### Question A6 — Label the diagram

```question
name: a6
marks: 3
topic: biology
```

The diagram shows a simplified plant cell.

```answer
name: a6.labels
type: label-the-diagram
marks: 3
image: pictures/plant-cell.svg
image_description: |
  A drawing of a plant cell. Pointer 1 indicates the outer boundary of
  the cell. Pointer 2 indicates the region filling the inside of the
  cell. Pointer 3 indicates the large round body near the centre.
labels:
  - number: 1
    expected: cell wall
  - number: 2
    expected: cytoplasm
  - number: 3
    expected: nucleus
```

```marking
marks: 3
guidance:
  - 1 mark per label; accept "cell membrane" for pointer 1
```

### Question A7 — A definition

```question
name: a7
marks: 3
topic: reasoning
```

```answer
name: a7.definition
type: short-written-answer
marks: 3
prompt: State what is meant by a counterexample, and give one for the
  claim "all birds can fly".
model_answer: |
  A counterexample is a single case that shows a general claim to be
  false. A penguin (or an ostrich, or a kiwi) is a bird that cannot
  fly, so it is a counterexample to the claim.
```

### Question A8 — An explanation

```question
name: a8
marks: 6
topic: study skills
```

```answer
name: a8.spacing
type: long-written-answer
marks: 6
prompt: |
  Explain why spreading study sessions across several days works better
  than one long session the night before an exam. Refer to at least one
  idea covered this term.
```

```marking
limit: 6
points:
  - 2 marks - names spaced practice, or describes spreading study over time
  - 2 marks - explains that recall strengthens memory more than rereading
  - 2 marks - explains why cramming fades quickly, in terms of forgetting
  - 2 marks - gives a concrete study plan as an example
```

```section
name: B
choose: 1
```

## Section B — Essay

Answer **one** of the two titles. Aim for roughly 600 words. The
planning box is for your notes; it is handed in but carries no marks.

### Title B1

```question
name: b1
marks: 20
topic: technology and learning
```

"Studying from a screen is worse than studying from paper." Discuss,
drawing on your own experience and on the research summaries covered
this term.

```answer
name: b1.essay
type: essay
marks: 20
guide_words: 600
planning_box: yes
```

```marking
criteria:
  - name: Argument and structure
    marks: 8
    bands:
      - 7 to 8 - a sustained line of argument; each paragraph builds on
        the one before
      - 4 to 6 - a clear position, developed unevenly
      - 0 to 3 - description without an argument
  - name: Use of evidence
    marks: 8
    bands:
      - 7 to 8 - research and experience are woven into the argument
      - 4 to 6 - evidence is present but summarised rather than used
      - 0 to 3 - little or no evidence
  - name: Clarity of writing
    marks: 4
    bands:
      - 3 to 4 - precise, controlled prose
      - 0 to 2 - meaning is sometimes unclear
```

### Title B2

```question
name: b2
marks: 20
topic: technology and learning
```

"An examination is the fairest way to find out what someone has
learned." Discuss, with examples from at least two different subjects.

```answer
name: b2.essay
type: essay
marks: 20
guide_words: 600
planning_box: yes
```

```marking
criteria:
  - name: Argument and structure
    marks: 8
    bands:
      - 7 to 8 - a sustained line of argument; each paragraph builds on
        the one before
      - 4 to 6 - a clear position, developed unevenly
      - 0 to 3 - description without an argument
  - name: Use of examples
    marks: 8
    bands:
      - 7 to 8 - examples from different subjects carry the argument
      - 4 to 6 - examples are present but incidental
      - 0 to 3 - few or no examples
  - name: Clarity of writing
    marks: 4
    bands:
      - 3 to 4 - precise, controlled prose
      - 0 to 2 - meaning is sometimes unclear
```
