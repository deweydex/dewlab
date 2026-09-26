# Page templates

Six real pages, one of each shape a dewlab page can take. Together they make
a small series, *Running totals*: a tutorial, its practice page, a closer
look at the misconception the tutorial runs into, a mixed set, a making task
to end the series, and a project brief. Copy the one you need into
`tutorials/<id>/`, change the id and the content, and delete the `<!-- -->`
notes. Each note points to the reason for a choice in
[`../../planning/PEDAGOGICAL_STYLE_GUIDE.md`](../../planning/PEDAGOGICAL_STYLE_GUIDE.md).
The syntax they use is in
[`../WRITING_TUTORIALS.md`](../WRITING_TUTORIALS.md#page-templates).

| Shape | Template | What it shows |
|---|---|---|
| A tutorial | [running-totals.md](running-totals.md) | An opening that runs something and asks, two predict blocks, a walk-through in a fold after a "try changing" prompt, a task in three worlds with its solution, inputs and hint, and the closer with a challenge. |
| A practice page | [running-totals-practice.md](running-totals-practice.md) | Several kinds of problem, a solution in two tiers, a "one way through it" fold for mathematics by hand, and two problems from earlier pages. |
| A closer look | [where-the-total-starts.md](where-the-total-starts.md) | Two ideas, an experiment where only one matches what happens, and why the other idea is so natural to hold. |
| A mixed set | [mixed-running-totals.md](mixed-running-totals.md) | Problems from across a series, with no label saying which page each comes from. |
| A series-end making task | [a-total-you-can-see.md](a-total-you-can-see.md) | A first step anyone can take, then the reader's own piece of work in their world, with no top. |
| A project brief | [a-scale-model-of-the-solar-system.md](a-scale-model-of-the-solar-system.md) | A group version and an individual version, and reflection questions instead of a rubric. |

The templates are never published. `tests/build/test_templates.py` builds
them in a temporary copy of the site on every test run, so a template that
stops building fails there first.

Some of the syntax they use is agreed but not yet live: the predict block
arrives with #313, the worlds with #315 and the challenge with #316. Until
then a predict or challenge block builds as a plain code block, and a
world's `<div>` shows its contents without converting them. Each of those
pull requests updates these templates, and the test, as it lands. The
solution and inputs blocks are live, and the build runs every solution in
these templates on every test run.
