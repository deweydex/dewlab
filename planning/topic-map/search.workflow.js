export const meta = {
  name: 'dewlab-topic-map-search',
  description: 'Rebuild dewlab topics as a multi-level map: one search per area, integrate, critique, revise',
  phases: [
    { title: 'Search', detail: 'one proposer per area, working from the pages and from the learner' },
    { title: 'Integrate', detail: 'regions, cross-area needs, one validated graph' },
    { title: 'Critique', detail: 'size, needs, learner-eye and completeness critics' },
    { title: 'Revise', detail: 'apply what holds up, questions for Josh' },
  ],
}

const T = '/home/user/dewlab/planning/topic-map'
const AREAS = [
  { id: 'number', about: 'number, fractions, powers, roots, surds, logarithms, sets and logic, the number line; much of The Zen of Slashes and Surds' },
  { id: 'algebra-geometry', about: 'equations, functions and graphs, calculus, geometry, trigonometry, vectors and matrices in their maths sense' },
  { id: 'chance-data', about: 'probability, statistics, simulation, modelling, data and charts, machine learning' },
  { id: 'programming', about: 'Python from first steps, control flow, functions, data structures, algorithms, object-oriented programming, complexity, and the practice of making software (testing, debugging, documenting, Git, deploying, working together)' },
  { id: 'databases', about: 'tables, SQL, querying and joining, designing and building databases, importing and exporting data' },
  { id: 'web', about: 'HTML, CSS, how a browser works, layout, accessibility, design, forms, publishing, and the full-stack page' },
]
const METHOD = 'Work from **both directions**. First go bottom-up: go through every page in your inventory, in course order, and write down what each page (or each section, where sections teach different things) teaches, then group those into topics by the size rule and topics into districts. Then check top-down: list the ideas a learner in this area would name, from what the courses set out to teach (their descriptions in courses/*.yaml, the series titles), and fix every gap between the two lists by splitting, merging or adding topics.'
const VAL = (file, area) => `python3 ${T}/validate.py proposal ${file} ${area}`

const PROPOSAL_SUMMARY = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    topics: { type: 'integer' },
    districts: { type: 'integer' },
    landmarks: { type: 'integer' },
    elsewhere: { type: 'integer' },
    errors: { type: 'integer', description: 'errors in the last validator run (must be 0)' },
    hidden_topics: { type: 'array', items: { type: 'string' }, description: 'names of topics with no old equivalent' },
    notes: { type: 'string' },
  },
  required: ['file', 'topics', 'districts', 'errors', 'hidden_topics', 'notes'],
}
const GRAPH_SUMMARY = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    regions: { type: 'array', items: { type: 'string' } },
    districts: { type: 'integer' },
    topics: { type: 'integer' },
    landmarks: { type: 'integer' },
    max_depth: { type: 'integer' },
    questions: { type: 'integer' },
    errors: { type: 'integer' },
    notes: { type: 'string' },
  },
  required: ['file', 'regions', 'districts', 'topics', 'max_depth', 'questions', 'errors', 'notes'],
}
const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          ids: { type: 'array', items: { type: 'string' }, description: 'topic, district or region ids concerned' },
          kind: { type: 'string', enum: ['split', 'merge', 'demote-to-step', 'promote-to-topic', 'add-need', 'remove-need', 'move', 'rename', 'rewrite-plain', 'missing-topic', 'cull', 'restore', 'regroup', 'other'] },
          severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          detail: { type: 'string', description: 'what is wrong, with the evidence (page slugs, headings, glossary terms)' },
          proposal: { type: 'string', description: 'the exact change: new ids, names, needs, steps' },
        },
        required: ['ids', 'kind', 'severity', 'detail', 'proposal'],
      },
    },
  },
  required: ['findings'],
}
const REVISE_SUMMARY = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    applied: { type: 'integer' },
    rejected: { type: 'array', items: { type: 'object', properties: { finding: { type: 'string' }, why: { type: 'string' } }, required: ['finding', 'why'] } },
    topics: { type: 'integer' },
    districts: { type: 'integer' },
    regions: { type: 'array', items: { type: 'string' } },
    questions: { type: 'integer' },
    errors: { type: 'integer' },
    summary: { type: 'string' },
  },
  required: ['file', 'applied', 'rejected', 'topics', 'districts', 'regions', 'questions', 'errors', 'summary'],
}

const COMMON = `Read ${T}/BRIEF.md first and follow it exactly: it defines the levels, the size rule, the tests, needs, naming, ids and the file format. Do not edit anything in the repository at /home/user/dewlab; write only the file named below.`

function proposerPrompt(area) {
  const file = `${T}/proposals/${area.id}.json`
  return `You are rebuilding dewlab's topics for the search area **${area.id}** (${area.about}).

${COMMON}

Your pages: ${T}/generated/inventory-${area.id}.json. The old topics to account for: the "${area.id}" list in ${T}/generated/old-topics-by-area.json.

${METHOD}

Other agents are doing the other areas at the same time; do not open their files in ${T}/proposals/.

Be thorough about hidden topics — ideas pages teach that the old list never named — and strict about the size rule and the not-a-topic tests. Open page markdown whenever the inventory leaves you unsure what a page or section teaches.

Write your proposal to ${file} (create the folder if needed). Then run:
    ${VAL(file, area.id)}
and fix every error until it reports 0 errors; act on warnings that are right. Return the summary.`
}

// the design spec is being researched by a separate agent outside this workflow
phase('Search')
const perArea = await parallel(AREAS.map((area) => () =>
  agent(proposerPrompt(area), { label: `propose:${area.id}`, phase: 'Search', schema: PROPOSAL_SUMMARY })
    .then((r) => ({ area: area.id, proposal: r }))))
const areasDone = perArea.filter(Boolean).filter((x) => x.proposal)
log(`proposals for ${areasDone.length} of ${AREAS.length} areas`)
if (areasDone.length < AREAS.length) log(`missing: ${AREAS.map((a) => a.id).filter((id) => !areasDone.some((x) => x.area === id)).join(', ')}`)

phase('Integrate')
const graphFile = `${T}/graph.json`
const integrated = await agent(`You integrate dewlab's topic proposals, one per search area, into one map.

${COMMON}

Inputs: ${AREAS.map((a) => `${T}/proposals/${a.id}.json`).join(', ')}. All pages: ${T}/generated/inventory.json.

Write ${graphFile} in the brief's format, with these differences for the whole map:
- Add "regions": [{"id", "name", "blurb"}] — the map's countries, about eight to eleven, named for learners. Search areas are not regions: split or join as the topics demand (a region for machine learning, or for making software, only if the topics warrant it). Every district gets a "region" field; regions hold about two to six districts each. Add "neighbours": [[regionA, regionB], ...] for regions that should border each other on the map, from the needs that cross between them.
- Place every "elsewhere" page into a topic in its target region (or make the topic it calls for); the final file has no "elsewhere".
- Merge topics that two areas both produced (for example the same idea taught once in maths and once in Python) only when they are the same idea for a learner; keep distinct ideas distinct, and attach the Python "closer look" pages where they belong.
- Resolve every "ext:" and "old:" need to a topic id; if nothing matches, link the nearest real topic or drop it, and say which in "notes". Needs must form a DAG with no redundant direct needs.
- Keep and de-duplicate "questions" into one list for Josh (at most about fifteen, each with evidence, options and a lean).
- Every descriptor outcome in outcomes.yaml (outside out-of-scope.yaml) must be served by a topic or be in "outcomes_culled"; every old topic code must appear in some "replaces" or be culled.

Validate with
    python3 ${T}/validate.py graph ${graphFile}
until it reports 0 errors, and read the effort-by-depth table: if effort climbs or collapses with depth, look at those topics again. Return the summary.`, { label: 'integrate', phase: 'Integrate', schema: GRAPH_SUMMARY })

phase('Critique')
const CRITICS = [
  { key: 'size', brief: `**Size and granularity.** Apply the size rule and every test in the brief to every topic. Use the validator's effort table and each topic's teaching pages (word and cell counts, headings, the page text where needed). Find topics to split, merge, demote to a step or promote from a step; landmarks or context steps that teach an idea something else needs; districts that are too big or too small. Check that the early regions are fine-grained where beginners get stuck and that deep topics are chunked, not shattered.` },
  { key: 'needs', brief: `**Needs and structure.** Test every need against "you cannot sensibly start this without that": remove the ones that are only "taught earlier" or "related"; add the ones a learner would be lost without; catch wrong directions and discover-first violations. Check the cross-region needs make sense as bridges, that region and district boundaries hold, that nothing is unreachable or orphaned without reason, and that depth is sane (a learner starting from nothing reaches everything by a plausible route). Use the course reading orders in courses/*.yaml and the pair judgements in planning/curriculum/review/ as evidence.` },
  { key: 'learner', brief: `**The learner's eye and completeness.** Read every region, district and topic name and every plain description as a learner who may be working in a second language (PEDAGOGICAL_STYLE_GUIDE.md#voice and #plain-language): jargon before it is met, vague or institutional names, names that don't say what you will be able to do. Then hunt for what is still missing: ideas the pages teach (glossary terms of kind concept or formula in the inventory, section headings) that no topic names; pages placed only as landmarks or context that teach something; outcome culls that lose something a learner needs.` },
]
const critiques = await parallel(CRITICS.map((c) => () =>
  agent(`You critique a proposed topic map for dewlab. ${c.brief}

${COMMON} You write no file: return findings only.

The map: ${graphFile} (validate it yourself with python3 ${T}/validate.py graph ${graphFile} to see the effort table and warnings). All pages: ${T}/generated/inventory.json; page markdown under /home/user/dewlab/tutorials/<slug>/<slug>.md.

Be specific and evidenced: each finding names the ids, the pages and headings that show the problem, and the exact change. High severity only for problems a learner or teacher would hit. Prefer twenty real findings to sixty weak ones.`, { label: `critic:${c.key}`, phase: 'Critique', schema: FINDINGS })
    .then((r) => ({ key: c.key, findings: (r && r.findings) || [] }))))
const allFindings = critiques.filter(Boolean).flatMap((c) => c.findings.map((f) => ({ critic: c.key, ...f })))
log(`${allFindings.length} findings from ${critiques.filter(Boolean).length} critics`)

phase('Revise')
const finalFile = `${T}/graph-final.json`
const revised = await agent(`You revise dewlab's proposed topic map in the light of three critics.

${COMMON}

The map: ${graphFile}. Write the revised map to ${finalFile} (leave ${graphFile} as it is). All pages: ${T}/generated/inventory.json; page markdown under /home/user/dewlab/tutorials/<slug>/<slug>.md.

The findings (JSON):
${JSON.stringify(allFindings)}

For each finding: check it against the pages and the brief. Apply it if it holds up; reject it with a one-line reason if it doesn't, or if critics contradict each other and the brief decides. Where a finding is a real judgement call for a teacher, turn it into a question rather than applying it. Set "agreement": "critic" on topics a finding created or reshaped. Finish the "questions" list for Josh: at most twelve, each a decision only he should make, with the evidence, the options and your lean.

Validate with
    python3 ${T}/validate.py graph ${finalFile}
until it reports 0 errors. Return the summary, listing every rejected finding.`, { label: 'revise', phase: 'Revise', schema: REVISE_SUMMARY })

return { areas: areasDone, integrated, critiques: critiques.filter(Boolean).map((c) => ({ key: c.key, count: c.findings.length })), revised }
