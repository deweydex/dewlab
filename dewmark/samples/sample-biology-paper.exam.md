```exam
title: Sample Biology Paper - Cells and Living Systems
exam_code: sample-biology-2027
version: 2027.01.20.1
total_marks: 60
time_allowed: 90 minutes
student_details: [full name, student number]
instructions: |
  Answer every question in Section A. In Section B, answer two of the
  three questions. Write in full sentences where a question asks you
  to explain, and use the biological names for the parts you describe.
```

```section
name: A
```

## Section A — Short questions

Answer every question in this section. Section A carries 30 marks.

### Question A1 — The parts of a cell

```question
name: a1
marks: 3
topic: cell structure
```

```answer
name: a1.blanks
type: fill-in-the-blank
marks: 3
text: |
  Every living thing is made of cells. The control centre of the cell
  is the {nucleus}, the jelly-like material that fills the cell is the
  {cytoplasm}, and the thin layer that controls what enters and
  leaves is the cell {membrane}.
```

```marking
marks: 3
guidance:
  - 1 mark per blank; accept close spellings when the word is clear
```

### Question A2 — What photosynthesis takes in

```question
name: a2
marks: 2
topic: photosynthesis
```

Which pair does a plant take in for photosynthesis, and in what way?

```answer
name: a2.choice
type: multiple-choice
marks: 2
options:
  - Carbon dioxide and water, using energy from light.
  - Oxygen and glucose, using energy from light.
  - Carbon dioxide and glucose, releasing energy.
  - Oxygen and water, releasing energy.
correct: 1
```

### Question A3 — Labelling a plant cell

```question
name: a3
marks: 5
topic: cell structure
```

The diagram shows a plant cell with five parts marked.

```answer
name: a3.labels
type: label-the-diagram
marks: 5
image: pictures/plant-cell-detailed.svg
image_description: |
  A drawing of a plant cell. Pointer 1 indicates the thick outer
  boundary. Pointer 2 indicates the thin layer just inside that
  boundary. Pointer 3 indicates the round body in the upper left of
  the cell. Pointer 4 indicates one of three small green oval bodies.
  Pointer 5 indicates the large pale space filling the middle of the
  cell.
labels:
  - number: 1
    expected: cell wall
  - number: 2
    expected: cell membrane
  - number: 3
    expected: nucleus
  - number: 4
    expected: chloroplast
  - number: 5
    expected: vacuole
```

```marking
marks: 5
guidance:
  - 1 mark per label; the wall and the membrane must not be swapped
```

### Question A4 — The parts of blood

```question
name: a4
marks: 6
topic: circulation
```

Complete the table. For each part of the blood, give its main job and
say roughly how it looks under a microscope.

```answer
name: a4.table
type: complete-the-table
marks: 6
columns: [part, main job, appearance]
rows:
  - [red blood cells, "?", "?"]
  - [white blood cells, "?", "?"]
  - [platelets, "?", "?"]
expected:
  - [red blood cells, carry oxygen, round discs with a dip in the
     middle]
  - [white blood cells, fight infection, larger cells with a visible
     nucleus]
  - [platelets, help the blood to clot, small fragments of cells]
```

```marking
marks: 6
guidance:
  - 1 mark per cell; accept any wording that carries the same fact
```

### Question A5 — Working out magnification

```question
name: a5
marks: 4
topic: microscopy
```

A drawing of a cheek cell measures 30 millimetres across. The real
cell is 0.06 millimetres across.

```answer
name: a5.magnification
type: numeric-answer
marks: 4
boxes:
  - label: "magnification = ×"
    expected: 500
working_box: yes
hint: "Magnification = drawing size ÷ real size, in the same units."
```

```marking
marks: 4
guidance:
  - 2 marks for the method (drawing size divided by real size), shown
    in the working
  - 2 marks for the answer 500; an answer with no working earns at
    most 2
```

### Question A6 — A population of yeast

```question
name: a6
marks: 4
topic: population growth
```

A student grew yeast in a flask of sugar solution and counted the
cells every two hours.

| Hours | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cells (thousands) | 10 | 40 | 150 | 400 | 700 | 900 | 980 | 1000 |

Describe the graph you would draw from this table.

```answer
name: a6.sketch
type: describe-a-sketch
marks: 4
shape:
  prompt: The curve
  options:
    - rises slowly, then quickly, then levels off
    - rises at a steady rate throughout
    - rises, then falls back down
    - falls throughout
  correct: 1
features:
  - label: "The population levels off at about _ thousand cells"
    boxes: 1
    expected: [1000]
  - label: "Growth is fastest between hour _ and hour _"
    boxes: 2
    expected: [4, 8]
```

```marking
marks: 4
guidance:
  - 2 marks for the shape, 1 for the levelling value, 1 for the
    fastest stretch; accept hour ranges from 2 to 8 that follow the
    student's reading of the table
```

### Question A7 — Plant and animal cells

```question
name: a7
marks: 6
topic: cell structure
```

```answer
name: a7.differences
type: short-written-answer
marks: 6
prompt: >
  Give three differences between a plant cell and an animal cell. For
  each difference, name the part and say which kind of cell has it.
model_answer: |
  A plant cell has a cell wall; an animal cell does not. A plant cell
  has chloroplasts; an animal cell does not. A plant cell has one
  large permanent vacuole; an animal cell has none, or only small
  temporary ones.
```

```marking
limit: 6
points:
  - 2 marks - the cell wall, named and placed in the plant cell
  - 2 marks - chloroplasts, named and placed in the plant cell
  - 2 marks - the large permanent vacuole, named and placed in the
    plant cell
  - 2 marks - any other correct difference, such as the regular shape
    of plant cells
```

```section
name: B
choose: 2
```

## Section B — Explaining

Answer two of the three questions in this section. Each is worth 15
marks. Write in full sentences, and use the biological names as you
explain.

### Question B1 — Osmosis

```question
name: b1
marks: 15
topic: osmosis
```

```answer
name: b1.osmosis
type: long-written-answer
marks: 15
prompt: >
  A plant wilts when it is short of water and becomes firm again when
  it is watered. Explain what osmosis is, then use it to explain both
  the wilting and the recovery. A labelled description of what happens
  inside one cell will strengthen your answer.
model_answer: |
  Osmosis is the movement of water from a place where water is
  plentiful to a place where it is scarcer, through a membrane that
  lets water through but holds back dissolved substances. When the
  soil is dry, the cells lose water by osmosis. The vacuole shrinks,
  the cytoplasm pulls away from the wall, and the cell becomes soft,
  so the plant droops. When the soil is watered, water enters the
  cells by osmosis. The vacuole swells and presses the cytoplasm
  against the wall, each cell becomes firm, and the plant stands up
  again.
```

```marking
marks: 15
guidance:
  - 5 marks for a correct account of osmosis, including the membrane
  - 5 marks for the wilting, traced through the cell
  - 5 marks for the recovery, traced through the cell
  - full marks need the account at the level of the cell, not only
    the whole plant
```

### Question B2 — Digestion

```question
name: b2
marks: 15
topic: digestion
```

```answer
name: b2.digestion
type: long-written-answer
marks: 15
prompt: >
  Describe the journey of a piece of bread through the digestive
  system, from the mouth to the small intestine. At each stage, name
  the organ, say what happens to the bread there, and name any juice
  or enzyme that acts on it.
model_answer: |
  First, in the mouth, the teeth grind the bread and saliva moistens
  it; the enzyme amylase in saliva begins breaking the starch into
  sugars. Then the tongue shapes the bread into a ball and it passes
  down the oesophagus, squeezed along by muscle contractions. In the
  stomach, churning mixes it with acidic gastric juice, which works
  mainly on protein, so the bread mostly waits there as a paste. In
  the small intestine, juices from the pancreas finish breaking the
  starch into glucose. Finally, the glucose passes through the wall
  of the small intestine into the blood.
```

```marking
marks: 15
guidance:
  - 3 marks per stage (mouth, oesophagus, stomach, small intestine)
    for the organ, the change, and the juice or enzyme
  - 3 marks for the final absorption into the blood
```

### Question B3 — Photosynthesis and respiration

```question
name: b3
marks: 15
topic: photosynthesis
```

```answer
name: b3.energy
type: long-written-answer
marks: 15
prompt: >
  Photosynthesis and respiration are often described as opposites.
  Explain what each process does, giving the word equation for each.
  Then explain why a plant needs both, and what happens to a plant
  kept in the dark for a week.
model_answer: |
  Photosynthesis builds food. In the chloroplasts, light energy turns
  carbon dioxide and water into glucose and oxygen: carbon dioxide +
  water → glucose + oxygen, using light. Respiration releases energy
  from that food, in every living cell, day and night: glucose +
  oxygen → carbon dioxide + water, releasing energy. A plant needs
  both because photosynthesis only captures energy in glucose;
  respiration is what makes that energy usable for growth and repair.
  In the dark, photosynthesis stops but respiration continues, so the
  plant uses up its stored glucose. After a week it has grown pale
  and weak, and it will die when the stores run out.
```

```marking
marks: 15
guidance:
  - 4 marks for photosynthesis with its word equation
  - 4 marks for respiration with its word equation
  - 4 marks for why both are needed
  - 3 marks for the plant in the dark, traced to the used-up stores
```
