# Execution counters, and two Jupyter features not wanted

## Execution counters

An execution counter is the small number Jupyter shows beside a cell as
`In [3]`. It says when that cell last ran, counting up across the session, so
the first cell you run is 1 and the next is 2 wherever they sit on the page. A
cell that has never run shows nothing.

dewmini does not have them, and should. A notebook runs in the order you press
Run rather than from the top, so a student whose cell 2 depends on a name
defined in cell 5 has a notebook that works for them and fails for everybody
else. Nothing on the page says so. dewmini makes this sharper than Jupyter
does, because every tab shares one namespace, so a name can arrive from a cell
that is not even on screen.

The change is small: one integer on the cell, one counter on the notebook, one
badge in the cell header. Run all resets the counter, so the numbers afterwards
read 1 to n from the top, which is the point being taught. Restart clears them,
because nothing in the namespace survives a restart. Counts do not survive a
reload either, since the Python session does not, and a count that did survive
would be claiming something false.

nbformat calls this `execution_count`, and dewmini's `.ipynb` writer already
writes `null` for every code cell, so filling it in costs nothing further. One
browser test holds the whole feature: run cell 3, then cell 1, and the badges
read 2 and 1.

## Two Jupyter features argued against

Recorded so neither is proposed again without meeting the argument.

**Magics**, meaning `%%time`, `%matplotlib inline` and `!pip install`. These
are invisible non-Python syntax that works inside a notebook and fails
everywhere else. Our students are asked to write real `.py` files on both PDP
and CMPS, so a dialect that breaks the moment they leave the tool costs them
something. `%%time` in particular has a plain Python answer,
`time.perf_counter`, which teaches something they can take with them.

**Modal keyboard commands**, meaning Jupyter's Escape and Enter modes, `dd` to
delete a cell and `a` or `b` to insert one. These are fast for an expert and a
trapdoor for a beginner. Press Escape by accident and typing stops working,
with nothing on screen to explain why. Jupyter itself needs a help overlay for
it. If some of the speed is wanted, plain shortcuts that always mean the same
thing are the safer half of the idea.
