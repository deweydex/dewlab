# Marking copies of student work

`dev/strip_submission.py` turns a student's submitted notebook (`.ipynb`) or
`# %%` Python file into what the student wrote, and a PDF to mark on. It is
for external examiners and moderation, and it is not part of the site build.

## The idea

The blank student notebook is the specification. A cell of a submission that
is identical to a template cell (ignoring whitespace) is the teacher's and is
dropped. Everything else is the student's and is kept whole, with its saved
outputs. The rule can only delete on an exact match, so a surprise leaves too
much in, never too little.

Cells that are close to a template cell but not the same are kept and listed
under `check:`. An edit to a cell the template marked "do not change" is
flagged the same way, because it is something a marker wants to know.

## Use

```bash
pip install nbconvert nbformat pyyaml ipython
apt-get install pandoc texlive-xetex texlive-fonts-recommended \
    texlive-plain-generic texlive-latex-extra

python3 dev/strip_submission.py init-rubric template.ipynb > rubric.yaml
# fill in the marks, and the criteria if you want them on the points table
python3 dev/strip_submission.py strip template.ipynb submissions/* \
    --rubric rubric.yaml --out marking/
```

Per submission, `--out` gets `<name>.stripped.ipynb` (or `.py`) and
`<name>.marking.pdf`, plus one CSV report for the batch. `--no-pdf`
skips the PDF.

## The rubric

`init-rubric` lists the template's `##` headings with `marks: null`. It does
not guess marks. Each part names a heading, its marks, and optionally the
criteria it is awarded for (they must add up to the part's marks). Only the
headings named in the rubric are kept in the stripped copy, each shown with
its marks, and the cover page carries the points table with a blank "Mark
given" column. With no rubric, headings up to level two are kept and there is
no table.

## The PDF

It goes through LaTeX (XeLaTeX), so a student's `$x^2$` typesets as maths and
accented text survives. Characters Latin Modern has no glyph for (CJK, emoji)
print as blanks; the script says so under `check:`. The layout is
`dev/strip_submission_templates/marking/`: A4, a wide right margin for
writing, the file name on every page.

Student name and number stay, because they are cells the student edited.
