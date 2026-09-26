## When a cell does not do what you expect

A cell can fail when nothing is wrong with the site. Here are three things
to try, in this order.

**Clear the cell.** The **Clear** button (↻) next to Run puts back the
code the page started with. If the cell works again after that, the
problem was in an edit, not in the page.

**Run the cells above it.** A later cell often uses something an earlier
cell made. The cells on a page share their work, so the order you run them
in matters. The small **⋯** button beside Run opens "Run this cell and all
above". It runs every cell before this one, from the top of the page.

**Reload the page.** This starts Python again, fresh. It does not delete
anything you have saved. Your work is kept in this browser, on this device.

When a cell stops with an error, Python says what went wrong, and where.
[Reading an error message](tutorial:reading-an-error-message#reading-a-traceback)
shows how to read what it says, from the bottom up.

If none of these explains it, the small circle on a cell's bar opens a
report with your code and the cell's last output already in it, so there is
nothing to copy. The line at the bottom of every page does the same for the
whole page.
