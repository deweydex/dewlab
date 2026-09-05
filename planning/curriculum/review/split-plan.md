# Making the splits official

`decisions.yaml` records sixteen topics that are the wrong shape. This is the
plan for turning those into real topics in `topics.yaml`, written so it can be
carried out without waking anybody.

## The thing that has to change first

Every topic code in `topics.yaml` is a QQI learning outcome code, and
`tests/test_curriculum_map.py::test_no_topic_invents_an_outcome` enforces it: a
code that is not `PRE-` must appear in `outcomes.yaml`. So a split cannot
simply add `MIT-2.1a`. The test would fail, and it is right to.

`outcomes.yaml` is the four module descriptors. Those are the awarding body's
and are not ours to split.

So the two files stop being one list under two names. A topic gets its own code
and says which outcome it serves:

```yaml
  NUM-3:
    name: Rational numbers
    outcome: MIT-2.1          # new field: which descriptor outcome this serves
    plain: >
      ...
```

`PRE-1` already proves a topic can exist without an outcome, so the model
stretches rather than breaks. Several topics may name one outcome. Every
outcome must still be named by at least one topic, which keeps the guarantee
the current test gives: no outcome goes untaught without somebody noticing.

## Order of work

1. **Add the `outcome` field** to every existing topic, set to its own code.
   Nothing changes yet; the file just says out loud what it has been assuming.
2. **Rewrite the two tests** in `TestTheTopicGlossary`:
   - every outcome is claimed by at least one topic (replaces
     `test_every_outcome_has_a_topic`);
   - every `outcome:` value is a real outcome code (replaces
     `test_no_topic_invents_an_outcome`).
   Prove each fails before the fix and passes after.
3. **Check `build.py` and `dev/curriculum_map.py`** for anywhere a topic code is
   assumed to be an outcome code. The topic tree and the reference panel both
   read `topics.yaml`; the map reads `outcomes.yaml`. Fix what breaks.
4. **Apply the thirteen splits**, one commit each, in this order — smallest
   first, so a mistake is cheap:
   `MIT-6.3`, `MIT-1.1`, `MIT-6.8`, `PDP-LO6`, `MIT-1.10`, `MIT-4.10`,
   `MIT-5.12`, `CMPS-LO1`, `MIT-5.8`, `MIT-4.6`, `CMPS-LO4`, `CMPS-LO2`,
   `MIT-2.1`.
   Each child needs `name`, `outcome`, `plain`, `uses`, `needs`. The arrows
   come from `dev/apply_splits.py`'s table, which says for each split which
   child takes the old topic's incoming arrows and which emits its outgoing
   ones. Six of those readings are marked `inferred` there and are guesses:
   carry them over, and list them in the pull request as needing a decision.
5. **Fold `MIT-6.5` into `MIT-6.3`**, and **add the missing topic** for basic
   algebraic operations.
6. **Regenerate** `planning/CURRICULUM_MAP.md` and the two pair reports.
7. **Run** `python3 -m pytest tests -q --ignore=tests/e2e`, `python3 build.py`,
   `python3 dev/check_doc_links.py`.
8. **Push, and open a draft pull request.** Do not merge.

## Every new topic is student-facing

`plain` and `uses` are read by students on the topic tree. They go through the
eight checks in `CLAUDE.md`, and `planning/PLAIN_LANGUAGE_PASS.md` gets updated
to say this surface has been through the pass. A split child inherits its
parent's tone, not its sentences: seven number families do not want one
sentence cut seven ways.

## What this plan does not do

**Tutorial `covers:` frontmatter is left alone.** Tutorials declare outcome
codes, those still validate, and nothing in them breaks. Re-tagging a tutorial
to a finer topic changes what the curriculum map claims is taught, and a wrong
tag makes the map lie about coverage. That needs a person who knows what each
section actually teaches, so the pull request lists the tutorials that look
like candidates instead of editing them.

**Nothing is merged**, and `outcomes.yaml` is not touched.
