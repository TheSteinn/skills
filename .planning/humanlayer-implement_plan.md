# Analysis: HumanLayer V1 `implement_plan.md`

**Source:** `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/implement_plan.md`
**Size:** 85 lines. YAML frontmatter + 1 H1 title + 5 H2 sections + 2 embedded prose templates.
**Context:** V1 command from the "Research → Plan → Implement" (RPI) methodology, the archaeological ancestor of the later QRSPI workflow (Question → Research → Design → Structure → Plan → Worktree → Implement → PR).

The five H2 sections are: `## Getting Started`, `## Implementation Philosophy`, `## Verification Approach`, `## If You Get Stuck`, `## Resuming Work`.

---

## 1. Purpose

This is the **Implement** stage of RPI — the third and final leg. Its job is to take an *already-approved* technical plan and execute it against the codebase. The frontmatter states it plainly:

> `description: Implement technical plans from thoughts/shared/plans with verification`

And the opening line (line 7):

> "You are tasked with implementing an approved technical plan from `thoughts/shared/plans/`. These plans contain phases with specific changes and success criteria."

**How it's meant to be run:** the user invokes the command and supplies a *plan path*. Per `## Getting Started`, if "no plan path provided, ask for one" (line 19). The agent reads the plan (and the "original ticket and all files mentioned in the plan"), builds a todo list, then implements the plan **phase by phase**, pausing for human verification between phases unless told to run several consecutively. It assumes upstream RPI stages (research, planning) already produced a well-formed plan artifact living under `thoughts/shared/plans/`.

So the command is a **plan consumer**, not a plan author. It owns none of the plan's structure or quality — it inherits both.

---

## 2. What it does well

**a) Persistent, resumable state via checkboxes in the plan file.** Progress is tracked in two places — a working todo list *and* the plan's own `- [x]` checkboxes, edited in place:
- "check for any existing checkmarks (- [x])" (line 12)
- "Update checkboxes in the plan as you complete sections" (line 27)
- "Check off completed items in the plan file itself using Edit" (line 49)

Because state is written back to a durable file (not just the ephemeral context window), work survives a context reset. This is the closest thing V1 has to commit discipline.

**b) An explicit resume protocol.** `## Resuming Work` (lines 77–83) handles interrupted runs cleanly:
> "Trust that completed work is done / Pick up from the first unchecked item / Verify previous work only if something seems off."

**c) Structured plan-reality mismatch handling.** `## Implementation Philosophy` refuses blind execution. On a mismatch the agent must "STOP and think deeply about why the plan can't be followed" (line 32) and emit a fixed template (lines 34–41):
```
Issue in Phase [N]:
Expected: [what the plan says]
Found: [actual situation]
Why this matters: [explanation]

How should I proceed?
```
The framing "The plan is your guide, but your judgment matters too" (line 29) and "You're implementing a solution, not just checking boxes" (line 84) explicitly guard against robotic box-ticking.

**d) A genuine human-in-the-loop checkpoint with automated/manual separation.** `## Verification Approach` distinguishes machine-checkable success criteria from human manual testing, and hard-gates on the human (lines 50–61):
```
Phase [N] Complete - Ready for Manual Verification
Automated verification passed: ...
Please perform the manual verification steps listed in the plan: ...
Let me know when manual testing is complete so I can proceed to Phase [N+1].
```
Reinforced by line 65: "do not check off items in the manual testing steps until confirmed by the user."

**e) Phase sequencing discipline.** "Implement each phase fully before moving to the next" (line 25) and "Fix any issues before proceeding" (line 47) prevent half-finished phases from stacking up.

**f) Front-loaded full context.** "**Read files fully** - never use limit/offset parameters, you need complete context" (line 14) and "Read the original ticket and all files mentioned in the plan" (line 13) push the agent to build understanding before writing code.

---

## 3. What it does poorly

**a) Instruction count is modest per-prompt, but the design leans on it.** Counting discrete directives: `Getting Started` ≈ 7, `Implementation Philosophy` ≈ 7, `Verification Approach` ≈ 7, `If You Get Stuck` ≈ 4, `Resuming Work` ≈ 4 → **roughly 29–30 instructions.** That is actually *within* the QRSPI target of <40 per prompt. The overflow problem is not this file in isolation; it is that this command must simultaneously hold **the entire plan document it reads** (N phases × specific changes × success criteria × manual steps), the ticket, "all files mentioned in the plan," and CLAUDE.md — the *cumulative* instruction load at runtime is what blows the ~150–200 budget, not the command's own prose.

**b) Zero isolation — no git, no branch, no worktree.** The words "git", "branch", "worktree", "commit", "PR", and "pull request" appear **nowhere** in the file. The agent edits files directly in whatever working directory it was launched in. There is no rollback boundary, no protection for the main tree, and no way to discard a botched run cleanly.

**c) No commit discipline at all.** Progress is recorded only as plan checkboxes; nothing is ever committed. Across a multi-phase run, all work accumulates as one uncommitted blob. There is no per-phase atomic, revertible history — the "state" is prose checkmarks in a Markdown file, not real VCS state.

**d) Control flow expressed as prose, not mechanism.** Line 63 is the clearest "prompts for control flow" antipattern:
> "If instructed to execute multiple phases consecutively, skip the pause until the last phase. Otherwise, assume you are just doing one phase."
Whether the agent runs one phase or many hinges on an ambiguous natural-language instruction and the model's interpretation of it — there is no real loop, flag, or structured driver.

**e) It assumes the plan is already high quality — and can't defend against a bad one.** The command trusts that plans "contain phases with specific changes and success criteria" (line 7) and enumerated "manual verification steps" (line 57). If the upstream plan is **horizontal** (layer-by-layer) rather than **vertical** (end-to-end testable slices), this command has no lever to fix it — it just executes what it's handed. Plan quality is entirely an upstream concern.

**f) Weak, hardcoded testing guidance.** The only concrete test instruction is line 46:
> "Run the success criteria checks (usually `make check test` covers everything)"
This bakes a project-specific `make check test` target into a supposedly general command, and "usually … covers everything" is hand-wavy. There is no guidance on writing tests, TDD, or what to do when a phase has no automated criteria — it defers wholesale to the plan.

**g) Heavy dependence on user presence and behavior.** The workflow stalls without an attentive human: the user must supply the plan path, approve every mismatch ("How should I proceed?"), confirm each manual-verification pause before the agent may continue, and explicitly opt into multi-phase execution. An absent user means an indefinitely paused agent.

**h) Ambiguous, subjective conditionals.** Several gates have no measurable threshold:
- "Start implementing if you understand what needs to be done" (line 17)
- "Verify previous work only if something seems off" (line 82)
- "Use sub-tasks sparingly" (line 75)

**i) Trusts pre-existing checkmarks unconditionally.** "Trust that completed work is done" (line 80) will happily propagate stale or wrong state if the plan's checkboxes are inaccurate.

---

## 4. Foreshadowing QRSPI

Reading this artifact against the QRSPI overhaul, the later additions map almost one-to-one onto V1's gaps:

**Worktree phase ← total absence of isolation.** V1's silence on git is exactly the hole QRSPI's dedicated **Worktree** phase fills: implementation moves into an isolated git worktree so it cannot clobber the main tree and can be thrown away wholesale. This is a net-new phase, not a refinement of anything present here.

**Phase-by-phase commits ← checkbox tracking that never committed.** V1 already had the *instinct* for per-phase durable state (edit `- [x]` in the plan after each phase). QRSPI keeps the per-phase rhythm but upgrades the recording medium from Markdown checkmarks to **real git commits** — atomic, revertible, and a genuine mechanism rather than prose. The "state survives context loss" goal is the same; the implementation gets teeth.

**PR grounded in the design doc ← no delivery step and no design artifact.** V1 simply ends when the last phase's manual verification passes — there is no PR, no handoff, and critically **no design document** (V1 only has a "plan" under `thoughts/shared/plans/`). QRSPI's split of **Design** and **Structure** from **Plan**, plus a final **PR** phase grounded in that design doc, adds both the missing rationale artifact and the missing delivery/review artifact.

**Question + Research phases ← inline context-gathering in `Getting Started`.** Lines 12–16 ("Read the plan completely… Read the original ticket and all files… Think deeply about how the pieces fit together") are a research phase crammed into the top of an implementation command. QRSPI extracts that into first-class **Question** and **Research** phases up front.

**Vertical slices ← "codebase has evolved / plan can't be followed" firefighting.** The prominence of `## If You Get Stuck` and lines like "Consider if the codebase has evolved since the plan was written" (line 72) signals that V1 plans were going stale and mismatching reality mid-implementation — a symptom of horizontal, non-testable plans. QRSPI's **Structure** phase (vertical, end-to-end slices with checkpoints) attacks the root cause upstream so the implement stage hits fewer surprises.

**Real control flow ← prose control flow.** The single-vs-multi-phase prose fork (line 63) becomes an explicit structured phase-by-phase loop (implement → verify → commit) in QRSPI, removing the reliance on ambiguous user phrasing.

**Retained but relocated human review.** V1's manual-verification pause (lines 50–65) shows human-in-the-loop was valued from the start; QRSPI preserves checkpointing but makes the **PR** the primary human review surface rather than an ad-hoc "let me know when manual testing is complete" chat gate.

**Instruction budget.** At ~30 instructions this single command is not itself the overflow culprit, but it is one of several monolithic RPI commands each doing research + judgment + verification + control flow at once. QRSPI's decomposition into many small (<40-instruction) phase prompts is the structural answer to keeping the *cumulative* runtime instruction load under the ~150–200 ceiling.
