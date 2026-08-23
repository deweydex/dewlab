# Practice problems

Josh, 2026-08-23:

> I think it's really important that we now start thinking about and planning our
> exercises — so practice problems associated with each tutorial. For that, we
> may want to convert some things from the mathematics repo also under the same
> username.

This is a plan, not a build. Nothing here has been made.

## What already exists, and it is a great deal

`deweydex/Mathematics` holds **twenty-seven worksheets** under `markdown/`,
written for AIML Foundations Mathematics at Dublin and Dún Laoghaire ETB. They
are Josh's, they are finished, and they are not small: 250 to 600 lines each,
sixty-odd problems apiece, **with an answer key at the bottom of every one**.

They are also, without anybody having planned it that way, almost exactly the
shape of the proposals in `planning/curriculum/proposed.yaml`:

| Worksheet | The tutorial it belongs to |
|---|---|
| `02a_lines_coordinates_vectors` | Lines and Distances |
| `02b_linear_thinking_data_curves` | Drawing Functions |
| `03a_foil_expanding`, `03b_factoring_solving`, `03c_applications` | Expressions Come Alive, Cracking Equations |
| `03d_graphing` | Drawing Functions, Parabolas |
| `04a_derivatives_integrals_inverse`, `04b_what_they_tell_us` | Rates of Change |
| `04c_advanced_rules`, `04d_transcendental_series`, `04e_optimisation` | beyond the descriptor — bonus or out |
| `05a_angles_radians_unit_circle` | The Unit Circle |
| `05b_right_triangle_trig`, `05e_laws_sines_cosines` | Solving Triangles |
| `05c_graphs_sine_cosine` | Sine and Cosine Waves |
| `05d_identities_equations` | out of scope — identities are ruled out |
| `06a_statistics_probability`, `08a_bayes`, `08b_distributions` | What Are the Chances, Making Sense of Data |
| `07a`–`07d` matrices | the matrices strand |
| `01_fractions`, `01a`, `01b`, exponents and logarithms | Numbers and Their Families |

`05a` is the case worth looking at first. It is degrees and radians, arc length,
the unit circle and the exact values in surd form — the three outcomes of *The
Unit Circle*, in the order that outline proposes, with sixty-four problems and
their answers. Its applications are already computing-flavoured: refractive
index, semiconductor lithography, wavelength limits.

**The work here is conversion and a teaching pass, not authorship.** That is the
same sentence as the everlearning notebooks, and it was true there.

## The four decisions this needs

### 1. Where a practice set lives

Not at the end of its tutorial. A worksheet is 250 to 600 lines and a tutorial is
about that long already; appending one doubles the page and buries the teaching
under the drill.

**Proposal: a page of its own, paired with the tutorial.** `Lines and Distances`
and `Lines and Distances — Practice`, linked from each other, with the practice
page out of the reading order the way an archived tutorial is out of it. It
inherits everything — the shell, the settings panel, saved work, mathematics
rendering — and needs one new idea in the build: that a page can belong to a
tutorial rather than to a series.

### 2. Whether the answers are on the page

The worksheets have answer keys. The site is static and public, so an answer key
that exists is an answer key a student can read, and there is no login that could
make it otherwise.

**Proposal: each answer behind a fold, next to its problem.** Not a key at the
bottom, and not a separate page — both of those are one scroll or one click from
the question, which is the same thing as being on it, minus the honesty.

Hiding answers from a self-directed adult learner is theatre. What is worth
protecting is not secrecy but the *moment before looking*, and a fold is exactly
that moment made physical. Checking your own answer immediately is most of what
makes practice work at all.

This also settles the `SOLUTION_` notebooks question left open in
`planning/OPEN_QUESTIONS.md`, which is the same question wearing different
clothes.

### 3. Runnable, or paper

Both, and not in the way that first suggests itself.

A cell per problem would mean sixty cells on a page, sixty keys in a student's
saved work, and a page that takes a long time to become usable. What the
worksheets actually want is **a few checking tools per section** — one cell that
lets a student test any answer in that part, rather than sixty that each test
one.

For `05a`, that is roughly: a `to_radians` to check the conversions against, a
`unit_point(angle)` to check coordinates against, and one cell that squares an
exact value and a decimal to show which is which. Three cells, sixty problems,
and every problem checkable.

The problems stay as prose and mathematics. dewlab's advantage over the paper
version is not that it turns questions into code — it is that the student can
find out whether they are right without turning the page.

### 4. What the conversion looks like

The worksheets share a rigid structure: a title block, `## Part A` … `## Part D`,
numbered problems, and a `## Answer Key` with numbered answers matching. That is
machine-splittable, which means a `dev/from_worksheet.py` beside
`dev/from_notebook.py` rather than a manual pass over twenty-seven files.

What it would do: read the parts and the key, pair each answer with its problem,
wrap each pair in a fold, drop the GeoGebra links (dewlab plots its own), and
leave the LaTeX alone because the build already renders it.

What it would not do: invent the checking cells or the connective prose. Those
are the teaching pass, and they are per-tutorial work.

## What has to change in the build

Less than it sounds, and it is worth listing so the size is honest.

- **A page that belongs to a tutorial rather than a series.** New, and the
  smallest version of it is a `practice_for: <slug>` field plus the same
  treatment archived tutorials already get: built, reachable, linked, not in the
  reading order.
- **A link between the pair**, both ways.
- **The contents page** needs to show practice sets without doubling the length
  of every series listing.
- **Nothing in the curriculum map.** A practice set teaches no outcome its
  tutorial does not already teach, and counting it would make coverage look
  wider than it is. The map should ignore these pages entirely.

## The order to do it in

1. **One worksheet, by hand, end to end** — `05a` against *The Unit Circle*,
   once that tutorial exists. Doing one by hand is what tells us whether the
   fold-per-answer design survives contact, and it is cheaper to find out on one
   than on twenty-seven.
2. **The build change**, once the shape is settled by (1).
3. **`dev/from_worksheet.py`**, once there is a worked example for it to
   reproduce.
4. **The rest of the worksheets**, in the order their tutorials get written.

Doing (3) first would be the obvious mistake: a converter built before anybody
has seen a converted page tends to produce twenty-seven pages that all need the
same fix.

## Open questions

- **Which worksheets are out.** `05d_identities_equations` covers material
  ruled out of scope, and `04c`–`04e` go past the descriptor. They are good
  worksheets; that does not make them this course's.
- **Whether practice belongs to a tutorial or to a topic.** The mapping above is
  mostly one-to-one, but `03d_graphing` serves two proposals and `05b`/`05e`
  both serve *Solving Triangles*. One page per tutorial means splitting and
  merging worksheets rather than converting them whole.
- **Attribution.** The worksheets carry a header naming the course and the
  instructor. Whether that survives into dewlab, changes, or goes is Josh's
  call — it is his name on them.
