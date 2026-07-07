# QRSPI: My Understanding

A synthesis of the QRSPI workflow (Dex Horthy / HumanLayer), built from three source classes:

1. **The blog post** — [alexlavaee.me/blog/from-rpi-to-qrspi](https://alexlavaee.me/blog/from-rpi-to-qrspi/)
2. **Two transcripts of Dex's talk** — extracted in `no-more-slop-extract.md` and `qrspi-transcript-extract.md`
3. **The V1 archaeological record** — HumanLayer's original RPI commands, analyzed in `humanlayer-create_plan.md`, `humanlayer-research_codebase.md`, `humanlayer-iterate_plan.md`, `humanlayer-implement_plan.md`, `humanlayer-validate_plan.md`

Sections marked **[inference]** are my detective work from the artifacts, not something a source states directly.

---

## 1. What QRSPI is, in one paragraph

QRSPI is the successor to HumanLayer's Research → Plan → Implement (RPI) methodology for coding agents. It splits the pipeline into eight phases — **Question → Research → Design → Structure → Plan → Worktree → Implement → PR** — five of which are alignment (Q, R, D, S, P) and three execution (W, I, PR). Its central bet: the human's scarce attention should be spent on the *cheapest artifact that can catch a mistake* — a ~200-line design doc and a ~2-page structure outline before any code exists, and then the actual code at PR time — while the 1000-line plan is demoted from a human review artifact to a tactical document for the agent. Dex's team couldn't make an acronym out of the phase names, "so we just picked the ones we liked" and call it **"crispy"**; the blog renders it QRSPI. Both names refer to the same workflow.

## 2. Why RPI died: five documented diseases

The talk gives the narrative; the V1 command files supply the physical evidence. Each disease below is real in the artifacts, not just rhetoric.

### Disease 1 — Instruction budget overflow
Frontier LLMs follow only **~150–200 instructions with consistency** (per co-founder Kyle's blog post citing an arXiv paper); beyond that the model "half-attends" to everything. Dex's talk claims the old `create_plan` had "85 or more instructions." The archaeology shows it was **worse than the confession**: counting discrete directives, `create_plan.md` carries **~120–135 instructions**, `research_codebase.md` ~100, `iterate_plan.md` ~60–75 — each competing with CLAUDE.md, system prompt, and tool docs for the same budget. The instructions most likely to be dropped were exactly the mid-pipeline collaboration gates that made the process valuable.

### Disease 2 — Magic words
`create_plan` contained the right alignment steps (Step 2.4 "present design options", Step 3 "get feedback on structure before writing details") — but as *narrative flow buried mid-monolith*, not blocking gates. For ~50% of users the model skipped straight to writing the plan unless they typed the incantation: *"work back and forth with me starting with your open questions and outline before writing the plan."* Dex's verdict: "This isn't the user's fault. If you built a tool that requires hours of training to get good results from, go fix the tool." **[inference]** The tell that this was an enforcement failure rather than a knowledge failure: the same prompt *does* contain one hard gate ("No Open Questions in Final Plan... STOP") — the author knew how to write blocking gates and simply didn't apply that force to the alignment steps.

### Disease 3 — Contaminated research
"Good research is all facts. But if you tell the model what you're building, then you get opinions." V1's `research_codebase.md` fought this with **16 distinct anti-opinion directives** ("Document what IS, not what SHOULD BE", "NO RECOMMENDATIONS") — while its own Step 1 said to read the user's tickets FULLY, two of its eight sub-agents existed to pull Linear tickets in, and its filename convention embedded the ticket number. The prompt shouted "don't opine" at a context window it had already told what was being built. Skilled engineers routed around this by hand-writing neutral questions from the ticket; novices pasted the ticket and got opinions.

### Disease 4 — The plan-reading illusion
"A thousand-line plan tends to be about a thousand lines of code within 10% or so. And plans can have surprises." Reviewing the plan costs as much as reviewing the code — and then the code comes out different anyway, so the reviewer reads both. That isn't leverage. The archaeology corroborates on two fronts: `create_plan`'s template demanded ~13 sections *including actual code blocks* ("// Specific code to add/modify") — a 1000-line-plan generator by construction — and the very existence of a dedicated 250-line `iterate_plan.md` command proves plans routinely needed heavy post-hoc revision, i.e. **all substantive feedback was landing on the most expensive artifact in the pipeline**.

### Disease 5 — Horizontal plans
"Despite every single model and trying to prompt this out and eval the hell out of this, we cannot get models to stop writing horizontal plans" — all database, then all services, then all API, then all frontend; 1,200 lines later nothing works and there was nothing to test along the way. The smoking gun in the artifacts: `create_plan`'s own "Common Patterns" section *prescribed* the disease — "Start with data model → Build backend logic → Add API endpoints → **Implement UI last**." V1 wasn't failing to prevent horizontal plans; it was recommending them.

Two more gaps the archaeology surfaces that the talk mostly skips:

- **No isolation, no delivery** — `implement_plan.md` (85 lines) never mentions git, branch, worktree, commit, or PR. State was Markdown checkboxes in the plan file; a botched run had no rollback boundary and a finished run had no delivery step.
- **Self-grading** — `validate_plan.md` had the implementing agent verify its own work ("If you were part of the implementation: Review the conversation history..."), with "Be honest" as the only safeguard and no definition of what pass/fail even meant.

## 3. The design principles underneath the fix

These are the invariants that generated QRSPI; the phases are just their consequences.

1. **Do not outsource the thinking** (credited to Jake from Netflix). The engineer is part of the process; the workflow's job is to give the agent "every single opportunity to show you what it's wrong about" before code exists.
2. **Control flow for control flow, not prompts for control flow.** Don't encode an 8-step pipeline as narrative inside one prompt and hope the model follows it — make each step a separate invocation. "The if statement is really really powerful."
3. **Mind the instruction budget.** Every QRSPI prompt is **under 40 instructions** (vs. the ~130 monolith), leaving headroom under the ~150–200 ceiling for system prompt, CLAUDE.md, and tools.
4. **Facts by architecture, not by exhortation.** Where V1 used 16 "don't opine" reminders, QRSPI makes opinion *structurally impossible*: the research context never learns what's being built.
5. **Leverage = review the cheapest artifact that catches the mistake.** 200 lines of design beats 1000 lines of plan beats 2000 lines of wrong code. And at the end: **read the code** — "we tried not reading the code for like six months... we had to rip out and replace large parts of that system."
6. **State lives in static artifacts, not the context window.** Every phase writes a Markdown file; every next phase starts a **fresh context window** rebuilt from those files. That's why they don't use compaction — "everything that matters is going into static assets" — and why the "dumb zone" (~40% context utilization for beginners) is avoidable by design.
7. **Vertical slices with test checkpoints.** Each phase of work should be an end-to-end, testable 200–400-line block, so failures localize.
8. **Aim for 2–3x with near-human quality, not 10x slop.** "Going 10 times faster doesn't matter if you're going to throw it all away in 6 months."

## 4. The workflow, phase by phase

| # | Phase | Sees | Produces | Human's role |
|---|-------|------|----------|--------------|
| 1 | **Question** | The task/ticket (the *only* alignment phase that must) | `task.md` + `questions.md` — the task decomposed into neutral research questions | Optionally sanity-check the questions |
| 2 | **Research** | Only the questions — **never the task** | `research.md` (~300 lines) — facts with file:line citations | Skim; correct factual misses |
| 3 | **Design** | Task + research | `design.md` (~200 lines) | **Deep review — the main alignment gate** |
| 4 | **Structure** | Design + task + research (fresh window) | `structure.md` (~2 pages) | **Review the slicing and checkpoints** |
| 5 | **Plan** | All prior artifacts (fresh window) | `plan.md` (~8 pages) | Spot-check only |
| 6 | **Worktree** | — | An isolated git worktree | — |
| 7 | **Implement** | The plan, phase by phase | Code; a commit after each phase | Verify at checkpoints if slice is risky |
| 8 | **PR** | The design doc + the diff | A pull request grounded in `design.md` | **Read the code. No exceptions.** |

### Question — query planning for codebases
One context window reads the ticket and decomposes it into questions that will "cause the model to go touch all the parts of the codebase that matter" (ticket: "add an endpoint to reticulate splines across tenants" → "how do endpoints work; trace everything that touches splines; find the workers that do reticulation"). This mechanizes, deterministically, what only skilled engineers did by hand in V1. Dex's analogy: **query planning** — the planner sees the query; the executor only runs the plan.

### Research — the firewalled fact-gatherer
A **fresh context window with no knowledge of what's being built** answers the questions. Everything good from V1's `research_codebase` survives here: parallel sub-agent fan-out along the WHERE/HOW/EXAMPLES axis (locator/analyzer/pattern-finder), file:line citations upgraded to permalinks, a self-contained doc with provenance frontmatter, "live codebase is the source of truth." What's gone is the contamination — and with it, the need for 16 anti-opinion band-aids.

### Design — "where are we going?"
The agent brain-dumps everything it found, everything it intends, everything it *thinks* you want, and — mandatorily, questions first — everything it doesn't know, into ~200 lines: **current state, desired end state, patterns to follow, resolved design decisions, open questions**. This is Matt Pocock's "design concept" (the shared understanding otherwise locked inside a context window) forced out into an inspectable artifact so the human can do **"brain surgery on the agent"** before 2,000 lines of code exist. "Patterns to follow" is the specific antidote to agents copying the wrong idiom: "Nope, that's not how we do atomic SQL updates. That's some engineer that doesn't work here anymore." It is also the team artifact — Dex sends his design discussions to his co-founder (the code owner) so that code review later is just "yep, that's what I wanted." Meeting analogy: the **architecture review**.

### Structure — "how do we get there?"
Built in a new context window from design + task + research: a high-level overview of the *phases* of work — what order, and how each will be tested — in ~2 pages. The **C header file analogy**: if the plan is the implementation, the structure is the `.h` file — signatures and new types, just enough to see what the agent is thinking and correct it. Its reason for existing is blunt: prompting cannot cure the models' horizontal-plan compulsion, so a dedicated human-reviewed artifact enforces **vertical slices** — mock the endpoint, wire the frontend, then services, then the migration — each a 200–400-line block with a test checkpoint. Meeting analogy: **sprint planning**.

### Plan — demoted, not improved
Deliberately the "exact same template, exact same setup, exact same prompt" as V1's `create_plan` output — the change is its *audience*. It's now a tactical document **for the agent**; the human spot-checks it and saves deep review for the code. **[inference]** This is the most elegant move in the redesign: rather than fight the 1000-line plan, QRSPI re-priced it. Nothing about the artifact changed; everything about who must read it did. It's also why there is **no `iterate_plan` in QRSPI** — feedback lands on design/structure while it's cheap, so by plan time there's little left to argue about.

### Worktree — isolation as a phase
Implementation happens in an isolated git worktree. **[inference]** This is a direct patch on `implement_plan`'s most glaring hole (zero mentions of git): a rollback boundary, protection for the main tree, and disposability for botched runs.

### Implement — commit per phase
Executes the plan phase-by-phase, committing after each. V1's good instincts survive — the per-phase rhythm, resume-from-checkboxes, the "STOP and report" template on plan/reality mismatch, automated-vs-manual verification splits — but the recording medium upgrades from Markdown checkmarks to real, atomic, revertible git commits, and checkpoints align with the structure doc's test boundaries.

### PR — where the human reads the code
A pull request **grounded in the design document** — the reviewer gets the "why" alongside the diff. This replaces `validate_plan`'s self-grading: QRSPI implicitly concedes a model can't be trusted to certify its own completion, so the human sits at the one gate that matters. Review is fast *because* alignment already happened — the reviewer saw the design weeks of decisions ago and is confirming, not discovering.

## 5. The information-isolation model **[inference]**

Reading across all sources, QRSPI is best understood as **context-window access control**. Each phase is a fresh window with a deliberately curated view of the artifacts:

- **Question** is the only alignment window that reads the raw task — it exists to *launder* the task into neutral questions.
- **Research** sees questions only. Opinion contamination is impossible, not discouraged.
- **Design** is the first window allowed to hold both the task and the facts — because forming an opinion is now *its job*, and its opinion is immediately subjected to human review.
- **Structure, Plan** each rebuild from artifacts in fresh windows — nothing depends on a long-running session, so there is no compaction, no dumb zone, and any phase can be re-run or resumed from disk.

V1's failure, seen through this lens, was giving one window every permission at once: ticket + research + design + structure + writing, ~130 instructions, one session.

## 6. The review-economics model

The human's attention across the pipeline, in QRSPI's pricing:

- `design.md` (~200 lines): **deep read** — cheapest point to kill a bad approach, before the agent (or you) is attached to working code.
- `structure.md` (~2 pages): **deep read** — cheapest point to fix slicing and test order.
- `plan.md` (~8 pages): **spot-check**.
- The code at PR: **deep read, always** — "if you have people who depend on your code, please, I'm begging you, please read it."

The time-savings claim follows: a two-day feature with 2–4 hours of coding doesn't get faster by making coding 20 minutes — the two days were alignment, review, rework, and verification. QRSPI attacks *those* with AI, which is where the actual 2–3x lives.

## 7. What survived from V1 unchanged

QRSPI is a **re-architecture, not a new idea**. Almost every QRSPI phase already existed inside `create_plan.md` as a buried, skippable sub-step:

| QRSPI phase | V1 ancestor | What changed |
|---|---|---|
| Question | create_plan Step 1.5 ("present focused questions"); the skilled engineer's manual ticket→questions habit | Promoted to a dedicated phase; made deterministic |
| Research | research_codebase.md + create_plan Steps 1–2 | Firewalled from the task; dedup of double research |
| Design | create_plan Step 2.4 ("present design options") — the ~50%-skipped gate | Promoted from a paragraph to an un-skippable phase with its own artifact |
| Structure | create_plan Step 3 ("get feedback on structure") | Promoted; now carries the vertical-slice enforcement |
| Plan | create_plan Step 4 + template | Same template — audience demoted from human to agent |
| Worktree | (nothing — the gap itself) | Net-new |
| Implement | implement_plan.md | + worktree isolation, + commit per phase |
| PR | (nothing; validate_plan/describe_pr gestured at it) | Net-new as a phase; human replaces model as the verifier |

Carried forward intact: the facts-only research ethos, parallel sub-agent fan-out for context management, file:line citations and permalinks, self-contained artifacts with provenance frontmatter, automated-vs-manual success-criteria splits, read-files-FULLY discipline, and per-phase human checkpoints.

## 8. The one-sentence theory of the overhaul **[inference]**

Every V1 failure was an attempt to get *behavior* out of *instructions*; every QRSPI fix moves that behavior into *structure* — a separate invocation instead of a buried step, a blind context instead of an exhortation not to opine, a git worktree instead of nothing, a commit instead of a checkbox, a human at the PR instead of a model grading itself. **When the model won't reliably follow an instruction, stop instructing and change the architecture so the instruction is unnecessary.**

## 9. Open problems (Dex's own list)

- **Adoption**: three steps was already hard for teams to learn; now there are seven-plus. (HumanLayer is building an IDE to orchestrate it.)
- **Measurement**: "we've been trying to measure developer productivity for 50 years and we still don't know how to do it."
- **Platform rollout**: how a central team improves shared prompts without regressing some team's workflow.
- **Testing/verifying**: explicitly punted — "a whole other talk" (Drew Brunick's).
- **How much code to read**: "we're binary searching through the space" — don't-read-the-code advocates will recant within six months, but full-read may not be the end state either. He does not endorse spec-as-source-of-truth (Sean Grove) or the no-human-reads "software factory."

## 10. Source notes and discrepancies

- **Naming**: Dex says "crispy" on stage; the blog (and this repo's framing) says QRSPI. The letters don't map cleanly to the eight phases — "that didn't make a very good acronym, so we just picked the ones we liked."
- The two transcripts are near-identical transcriptions of the same talk; the `qrspi` one is slightly more precise on names (Drew Brunick, founders@humanlayer.dev) and includes "worktree" in the first phase enumeration; the `no-more-slop` one uniquely has the MC intro and the 158-slide count.
- **"Eigor"** is almost certainly a mis-transcription of the researcher behind the "ship 50% more, half is rework / good at greenfield, bad at brownfield" findings (plausibly Yegor Denisov-Blanch of Stanford, but the transcripts don't confirm this).
- Artifact names and sizes (`task.md`, `questions.md`, `research.md` ~300 lines) come from the workflow summary provided with this research task; the talk confirms design ≈ 200 lines, structure ≈ 2 pages, plan ≈ 8 pages, and the blog confirms the phase semantics but not file names.
- The blog adds two operational rules the talk only gestures at: keep context utilization under 40% / start fresh at 60%, and use cheap models for scoped sub-agent tasks with expensive models for orchestration ("sub-agents as firewalls").
