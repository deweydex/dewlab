# Topic pairs

A phone-sized page for judging the topic graph two topics at a time. Open
`index.html`, and it asks the same question over and over: of these two, which
one does a student need first?

## The loop

1. Judge pairs. Everything is kept on the device as you go.
2. After a dozen or so, tap **save**. GitHub opens with the file already
   written; sign in and tap **Commit changes**. The file lands in
   `planning/curriculum/review/pairs/`.
3. Run `python3 dev/pair_results.py`. It reads every saved batch and writes
   `planning/curriculum/review/pair-results.md`.
4. Read the report and decide what goes into `topics.yaml`.

The page holds no credential, so the commit is made by whoever is judging,
under their own account. Anyone without a GitHub account can use **Copy
everything** in the save dialog instead and send the text on.

Step 4 stays a person's decision. The report says what the judgements imply;
it never edits `topics.yaml`.

## The queue

All 92 topics make 4,186 pairs, and most of them are two topics with nothing
to do with each other. The page works through them in three tiers:

1. The 95 arrows the graph already has, to check they are real.
2. Every pair inside one section of a descriptor, where a missing prerequisite
   is most likely to be hiding.
3. Everything else, shuffled.

The first two tiers are 542 pairs, which is the part worth finishing.

## The other buttons

**Both ways** is for two topics that each need the other. That cannot be
taught in any order, so the report lists them as something to split or teach
together. **Refine** opens a sheet for a name a student would recognise, the
groups a topic belongs to, and a flag for one that needs thinking about. The
group list starts from `planning/curriculum/topic-groups.yaml`, and the box
underneath adds one that is not there yet.
