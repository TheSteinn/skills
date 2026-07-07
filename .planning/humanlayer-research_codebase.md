# Archaeology: HumanLayer `research_codebase.md` (RPI V1)

Source analyzed: `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/research_codebase.md` (214 lines).
Requested as "search_codebase"; the canonical file is `research_codebase.md`.

This is a V1 command from HumanLayer's "Research → Plan → Implement" (RPI) methodology, later
overhauled into "QRSPI" (Question → Research → Design → Structure → Plan → Worktree → Implement → PR).
The reading below quotes the actual file so the artifact can be used to infer *why* QRSPI was built.

---

## 1. Purpose

The frontmatter (lines 1-4) states the intent in one line:

> `description: Document codebase as-is with thoughts directory for historical context`
> `model: opus`

The opening charge (line 8):

> "You are tasked with conducting comprehensive research across the codebase to answer user
> questions by spawning parallel sub-agents and synthesizing their findings."

**How it is meant to be run.** It is a two-turn interactive command. On invocation it does *not*
act; the "Initial Setup" section (lines 19-26) makes it print a fixed prompt —

> "I'm ready to research the codebase. Please provide your research question or area of interest,
> and I'll analyze it thoroughly..."

— and then "wait for the user's research query" (line 26). Everything after that is driven by the
9-step procedure under "Steps to follow after receiving the research query" (lines 28-176):
read mentioned files → decompose the question → fan out sub-agents → synthesize → gather metadata →
write a structured research doc → add GitHub permalinks → sync & present → handle follow-ups. The
whole thesis is compressed in the phrase "as-is" / "what IS, not what SHOULD BE": the output is a
**technical map of the existing system**, explicitly not a proposal.

---

## 2. What it does well

**Sub-agent fan-out across vertical slices of the codebase.** Step 3 (lines 43-72) delegates to 8
specialized sub-agents grouped into 4 domains, and the split is genuinely well-factored along a
WHERE / HOW / EXAMPLES axis:
- `codebase-locator` — "find WHERE files and components live"
- `codebase-analyzer` — "understand HOW specific code works (without critiquing it)"
- `codebase-pattern-finder` — "find examples of existing patterns (without evaluating them)"
- `thoughts-locator` / `thoughts-analyzer` — historical docs
- `web-search-researcher` — external docs (gated: "only if user explicitly asks")
- `linear-ticket-reader` / `linear-searcher` — ticket context

The fan-out is explicitly a **context-management** device, not just speed: "Always use parallel Task
agents to maximize efficiency and minimize context usage" (line 179) and "Keep the main agent
focused on synthesis, not deep file reading" (line 188). The guidance to "Start with locator agents...
Then use analyzer agents on the most promising findings" (lines 67-68) encodes a sensible
cheap-scan-then-deep-read strategy.

**Facts-only / objectivity discipline (on the output side).** The single strongest instinct in the
file. It opens with a shouted section header — "CRITICAL: YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN
THE CODEBASE AS IT EXISTS TODAY" (line 10) — followed by five `DO NOT` clauses (improvements, root
cause, future enhancements, critique, refactoring). I count **16 distinct anti-opinion directives**
across the file (lines 10-17 ×8, 49, 50, 52, 72, 132, 191, 192, 193), culminating in
"Document what IS, not what SHOULD BE" (192) and "NO RECOMMENDATIONS" (193). This documentarian
ethos is the direct philosophical ancestor of QRSPI's "good research is all facts."

**File:line citation conventions.** Verifiability is baked in: "Include specific file paths and line
numbers for reference" (line 80); a dedicated `## Code References` block using ``path/to/file.py:123``
and ``another/file.ts:45-67`` (lines 137-140); and Step 7 (lines 157-162) upgrades local refs to
durable **GitHub permalinks** (`https://github.com/{owner}/{repo}/blob/{commit}/{file}#L{line}`)
once a commit is pushed. Findings are meant to be navigable and permanent.

**A complete, self-contained research-doc structure.** Step 6 (lines 96-155) ships a full template:
YAML frontmatter + `Research Question`, `Summary`, `Detailed Findings`, `Code References`,
`Architecture Documentation`, `Historical Context (from thoughts/)`, `Related Research`, and
`Open Questions`. "Research documents should be self-contained with all necessary context" (line 183).

**Frontmatter / reproducibility metadata.** The YAML block (lines 100-111) captures `date`,
`researcher`, `git_commit`, `branch`, `repository`, `topic`, `tags`, `status`, `last_updated`,
`last_updated_by` — generated via `hack/spec_metadata.sh` (line 86). This gives every doc temporal
and provenance context ("Include temporal context", line 186).

**Ordering & source-of-truth discipline.** Hard sequencing rules: read mentioned files FULLY before
spawning anything (lines 30-34, 194); "Wait for ALL sub-agent tasks to complete before proceeding"
(line 75); metadata before writing; "NEVER write the research document with placeholder values"
(line 199). And a clear source hierarchy: "Prioritize live codebase findings as primary source of
truth. Use thoughts/ findings as supplementary historical context" (lines 77-78), plus "Always run
fresh codebase research - never rely solely on existing research documents" (line 180).

---

## 3. What it does poorly

**Nothing stops the user pasting the ticket in — the command actively invites it.** This is the core
failure. Step 1 (lines 30-31) reads: "If the user mentions specific files (tickets, docs, JSON), read
them FULLY first." The Initial Setup asks for the user's "research question **or area of interest**"
(line 23) with zero neutrality guardrail. Two of the eight sub-agents (`linear-ticket-reader`,
`linear-searcher`, lines 62-64) exist to pull ticket context in. The filename convention embeds the
ticket: `YYYY-MM-DD-ENG-XXXX-description.md` with the example `2025-01-08-ENG-1478-parent-child-
tracking.md` (lines 87-94). Every affordance in the file assumes a ticket is present and welcomes it
into the research context. So the research window routinely sees "what we're building." Per Dex
Horthy's framing — *"good research is all facts, but if you tell the model what you're building, then
you get opinions"* — this file tells the model what's being built by design.

**The anti-opinion rules are output-side band-aids, not an input-side firewall.** The 16 repeated
"don't opine" directives (see §2) fight the *symptom* (the model emitting recommendations) while
leaving the *cause* (contaminated input) untouched. The repetition itself is a tell: "documentarian /
not evaluator" is restated at least five times (lines 10, 52, 72, 191-193) and "CRITICAL" is shouted
three times (10, 191, plus 195). This is the signature of a prompt patched reactively — each new leak
of opinion answered with another `DO NOT` — rather than fixed structurally. You cannot instruct your
way out of an input that already framed the goal.

**Decomposition happens inside the contaminated context.** Step 2, "Analyze and decompose the research
question" (lines 36-42), runs in the *same* context window that just read the ticket in Step 1. The
sub-agents may themselves be neutral (they never see the ticket), but the **questions handed to them**
are authored by a context that saw the proposed solution — so the framing leaks downstream through the
prompts, not just the final synthesis. Worse, line 38 actively invites intent-inference: "ultrathink
about the underlying patterns, connections, and architectural implications **the user might be
seeking**." "What the user is seeking" is precisely the goal-orientation that turns fact-gathering
into opinion.

**Heavy, unenforced dependence on user skill.** Research neutrality is entirely a function of how the
user phrases the query, and the command enforces nothing. A skilled engineer types a neutral question
("how does authentication work today?") and gets facts; a novice pastes "implement OAuth per ENG-1478,
we should use library X" and gets opinions shaped around library X. The labor of converting a task into
neutral questions is silently offloaded to the human. There is no Question phase to do it for them.

**Instruction overload.** By my count the file packs on the order of **~100 discrete directives**:
7 in the CRITICAL block, roughly 55 across the 9 numbered steps (Step 3 alone ~19; Step 4 ten
sub-bullets), and ~34 in the "Important notes" tail (lines 178-213, ~19 top-level bullets plus nested
sub-bullets for ordering, path-handling, and frontmatter). With this much text and this much
repetition, the salience of any single rule — including the all-important "no opinions" — is diluted.

**Org-specific machinery baked into the flow.** `thoughts/searchable/` hard-link path rewriting
(lines 200-207), `humanlayer thoughts sync` (line 165), `hack/spec_metadata.sh` (line 86), and Linear
coupling make the command hard to lift out of HumanLayer's environment.

---

## 4. Foreshadowing QRSPI

**The disease was already correctly diagnosed; only the treatment layer was wrong.** This file proves
the RPI authors already believed research must be facts-not-opinions (16 directives say so). What they
lacked in a single-command world was any lever *other than instructions*. QRSPI's innovation is to move
the fix from the **prompt layer** to the **architecture layer** — from "please don't opine" to a
structure in which opinions are impossible to form.

**The Question/Research split is exactly the firewall this file is missing.** V1 fuses three things in
one contaminated context: read-the-ticket (Step 1), decompose (Step 2), and answer (Steps 3-4). QRSPI
cleaves them:
- The **Question** phase is the one place the task/ticket is *allowed* to be seen — its only job is to
  decompose the task into neutral research questions, in one context window.
- The **Research** phase runs in a **fresh context that never sees the task** and answers only those
  questions. This is the query-planner / executor separation: the planner sees the query, the executor
  just runs the plan. Contamination becomes *structurally impossible*, not merely discouraged.

**This directly resolves every §3 weakness:**
- "Nothing stops the ticket paste" → the ticket is confined to the Question phase and firewalled out of
  Research.
- "16 output-side band-aids" → largely unnecessary; a context that doesn't know what's being built
  can't recommend how to build it.
- "Decomposition in a contaminated context" → decomposition is deliberately *isolated* as its own phase.
- "Dependence on user skill" → the machine now performs the neutral-question authoring that only skilled
  engineers did by hand in V1. It is novice-proofing by construction.

**What survived into QRSPI (the good parts carried forward):**
- The facts-only / documentarian ethos ("Document what IS, not what SHOULD BE") — now the *definition*
  of the Research phase rather than a plea within it.
- Parallel sub-agent fan-out with the locator / analyzer / pattern-finder (WHERE / HOW / EXAMPLES)
  division, used for context management.
- `file:line` citations and GitHub permalinks as the unit of verifiable fact.
- The persisted, self-contained research document with YAML frontmatter / provenance metadata.
- "Live codebase = source of truth; historical docs = supplementary."
- Read directly-mentioned files fully before fanning out.
- The phased, strictly-ordered discipline itself — V1's 9 in-command steps generalize into QRSPI's
  8 named phases across the whole pipeline.

**What was restructured away:** the single-context "decompose + answer" fusion, the built-in invitation
to paste a ticket into research, and the reliance on ~16 "don't opine" reminders to hold the line.
