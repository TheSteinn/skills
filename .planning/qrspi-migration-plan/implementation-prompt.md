# Handoff prompt for the implementing agent

Copy everything below into a fresh session.

---

Your task: implement the QRSPI migration plan in this repo, phase by phase. Act as the
orchestrator — delegate the authoring of each phase to a fresh subagent, then verify, and
commit each phase yourself. Do not author the skills inline in your own context.

## Study first (in this order)

1. `.planning/qrspi-migration-plan/index.md` — the binding document: durable decisions
   (violating one fails a phase), conventions ("sketches are floors, not finished files";
   skill voice — no first person; < 40 instructions per skill), verification rules, and the
   phase table.
2. `.planning/qrspi-migration-design.md` — the signed-off design. Consult it when a judgment
   call arises; every deviation from QRSPI has its reason recorded there.
3. Voice and register exemplars (what "polished, this repo's register" means):
   `skills/tdd/SKILL.md`, `skills/grilling/SKILL.md`, `skills/codebase-designing/SKILL.md`,
   and `docs/grill-me.md` (the deviation-record exemplar).
4. Deeper background only if a phase file leaves you unsure: `.planning/qrspi-understanding.md`
   (QRSPI synthesis) and `.planning/humanlayer-*.md` (V1 archaeology). Do not re-research
   QRSPI from the web — everything needed is in the repo.

## How to run it

Work on the `workflow-overhaul` branch. If the `.planning/` migration documents are not yet
committed, commit them first as their own commit. Phases run strictly in order (1 → 6); each
leaves the repo coherent and is committed before the next starts.

For each phase N:

1. **Delegate.** Spawn one general-purpose subagent to author the phase. Its prompt must
   instruct it to read fully, before writing anything:
   `.planning/qrspi-migration-plan/phase-N-<name>.md`, `.planning/qrspi-migration-plan/index.md`,
   and the four voice exemplars listed above — and must restate the floor rule: the sketches
   fix structure, gates, and voice; the subagent's job is to flesh them into polished skills,
   fully author the `references/` files, deviation records, and README prose from the phase's
   stated requirements, and keep each SKILL.md under 40 instructions. The subagent authors
   files only — it never commits.
2. **Review.** Diff-review the subagent's work against the phase file yourself: every
   "Changes required" item landed; no keeper skill touched beyond the phase's named exact
   edits; the voice rule holds (do a pronoun sweep: no "I"/"me"/"we"/"my"); the instruction
   budget holds.
3. **Verify.** Run the phase's automated verification commands and check them off in the
   phase file.
4. **On failure:** send the fix back to a subagent with the failure output. A phase that
   fails your review twice → stop the orchestration and report to the user.
5. **Commit.** One atomic commit per phase, message naming the phase.
6. **Checkpoint.** Present the phase's manual verification steps to the user and pause. Those
   steps dogfood the new skill on the plan's standard micro-task and need the user in the loop
   (grills, approvals). Note when handing them over: freshly created skills may require
   `./install.sh` and/or a fresh session before `/name` invocation is picked up. The user may
   defer dogfooding and accept the phase on automated checks + your review — their call, not
   yours.

## Cautions

- The deliverables are prose skills — TDD does not apply; each phase's success criteria are
  its verification.
- If reality contradicts the plan (a file moved, an instruction is impossible, two
  requirements conflict), STOP and report — expected, found, why it matters, how to proceed —
  rather than improvising.
- Phase 4's template adaptation reads V1's original at
  `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/create_plan.md` (lines 182–277);
  that path is read-only reference material — never modify anything outside this repo.
