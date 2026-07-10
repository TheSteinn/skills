# Decision record — three-axis-review

Design decisions for a new review skill combining the nuclear review's heuristics with the two-axes review's
deterministic macro shape. Sources: `.planning/review/nuclear-review.md`, `.planning/review/two-axes-review.md`, and
the adversarial findings in `.planning/review/findings-*.md`.

## Resolutions

**1. Architecture** — Three orthogonal axes run as parallel sub-agents: **Spec** (does it do the right thing),
**Standards** (does it follow documented repo rules), **Structure** (is it well built). Adopts the two-axes
deterministic macro shape: pin fixed point → `git rev-parse` + non-empty-diff gate *before* fan-out → three-dot diff
(`git diff <fixed-point>...HEAD`) → one message, three Agent calls → aggregate. *(Replaces the nuclear review's
process-free single reviewer.)*

**2. Baseline placement** — The Fowler smells move off Standards and merge with the nuclear review's seven concerns
into **one deduplicated what→fix baseline on Structure**; the repo-overrides precedence rule ("a documented repo
standard always wins") moves with it. Standards becomes documented-rules-only. *(Kills cross-axis duplicate findings;
makes the axes genuinely orthogonal.)*

**3. Output contract** — Findings only, no overall verdict. Each finding labelled `blocker (presumptive)` or
`suggestion`, driven by objective triggers where possible. The aggregator sorts blockers-first within each axis and
**never re-derives labels or reranks across axes**; one-line per-axis summary closes the report. *(Replaces the
nuclear review's subjective approval bar, keeping its burden-shift idea in concrete form.)*

**4. Judo** — Simplification-reframing findings are kept, validation-gated: reportable only with a concrete sketch
(what disappears, what replaces it) + a behavior-preservation argument + a complexity argument in `codebase-designing`
terms. The "assume a judo move exists" instruction is dropped; judo findings are always `suggestion`. *(Keeps the
nuclear review's signature ambition, removes the hallucination incentive.)*

**5. codebase-designing coupling** — The Structure sub-agent's prompt template contains an explicit Skill-tool
invocation of `codebase-designing`; the merged baseline is written in its vocabulary (deletion test for thin
wrappers/Middle Man, hypothetical-seam for Speculative Generality). Definitions stay canonical in one place.

**6. 1k-line gate** — A script in the skill's `scripts/` dir; the orchestrator runs it at step 1; the script computes
per-file before/after line counts, filters, and outputs the rule-breaking files. Crossings become pre-seeded Structure
findings auto-labelled `blocker (presumptive)`; the Structure sub-agent only adds context (is decomposition sensible,
is there justification). *(The template for objective-trigger labelling; precedent: `skill-creator/scripts/`.)*

**7. Spec discovery** — Ordered chain:

1. A path the user passed — the only route needing no confirmation.
2. `.planning/<slug>/` artifacts matching the branch or feature, in this preference order:
   `plan/index.md` + `plan/phase-N-<slug>.md` (the tactical spec — self-contained phases with success criteria)
   → `structure.md` (high-level plan: ordered slices, test checkpoints, signature sketches)
   → `design.md` (design decisions). A best match is **confirmed with the user**, never raced forward.
3. Ticket keys in commit messages → forge CLI inferred from session context (project/global CLAUDE.md or AGENTS.md
   instructions, loaded-skill hints). Definitive proof in context → use it; otherwise ask how to look the ticket up or
   for the spec directly. Inferred matches are confirmed before proceeding.
4. Nothing → ask the user. No spec → the Spec axis skips and says so in the report.

No PRD references anywhere — PRDs are superseded by the workflow pipeline. *(Replaces the dead
`docs/agents/issue-tracker.md` route.)*

**8. Standards discovery** — Fixed, closed candidate set: project CLAUDE.md / AGENTS.md; root-level CONTRIBUTING /
CODING_STANDARDS / STYLE docs; root `docs/` scanned for similarly named files (CONTRIBUTING, CODING_STANDARDS, STYLE,
code-style, etc.) — explicit stopping rule, no repo-wide crawl. The scoped scan is delegated by the Standards
sub-agent to a **haiku (small-model) exploration sub-agent** so the reviewer's own context stays clean. Nothing found
→ explicit skip, same contract as Spec. Tooling filter kept but grounded: the orchestrator lists detected lint/format
config filenames in the prompt; the sub-agent skips only findings those named tools would catch.

**9. Baseline delivery** — The merged baseline lives at `references/structure-baseline.md` in the skill dir and is
passed by absolute path in the prompt template with a read-first instruction. *(Replaces the two-axes
hand-transcription; sub-agents share the filesystem.)*

**10. Prompt discipline** — Three verbatim fenced templates, placeholders filled and nothing else (the `implement`
convention). Label definitions live inside the template text, stated once; sub-agents label their own findings.

**11. Sub-agent report contract** — No word caps: original detail is wanted, and a cap invites lossy summarising.
Citations remain mandatory (standards: cite the rule's file + quote the hunk; spec: quote the spec line; structure:
quote the hunk and name the baseline entry). Failure handling: an empty or failed axis → rerun once → then reported as
**"not reviewed"**, distinct from "no findings". *(Supersedes an earlier proposal of 400/600-word caps.)*

**12. Identity & pipeline placement** — `skills/three-axis-review/` (SKILL.md + `references/` + `scripts/`),
frontmatter `disable-model-invocation: true`, invoked as `/three-axis-review`. Standalone: no other skill invokes it;
the README documents it as an optional quality gate between `/implement` and `/open-pr`, where its Spec axis consumes
the `.planning/<slug>/` plan artifacts naturally.

## Cross-topic dependencies

- The merged baseline (2), the vocabulary coupling (5), and the delivery mechanism (9) are one artifact:
  `references/structure-baseline.md`.
- The 1k script (6) is the prototype for objective-trigger labelling in the output contract (3).
- The judo gate (4) depends on the vocabulary coupling (5) for its complexity-argument criterion.
- Spec chain step 2 (7) and pipeline placement (12) both hinge on the `.planning/<slug>/` artifact set.

## Open / outstanding

- Script contract details (filename, args, exact output format) — implementation.
- The actual dedup mapping (which Fowler smells collapse into which nuclear concerns) — implementation, decided in the
  baseline file.
- Huge-diff handling — parked; v1 gates only bad-ref/empty-diff.
- Fate of the `.planning/review/` source and findings files once the skill ships — housekeeping, user's call.

## Amendment (2026-07-09) — sub-agent return contract

**Decision:** Markdown only. No JSON contract, no validator/parser script, no MCP/custom tool, no Workflow-based
fan-out. Supersedes the JSON-contract direction explored during structuring; the markdown finding schema stands,
hardened as below.

**Rationale:**

1. The aggregator combines three reports into one output — no re-ranking, no merging, no label re-derivation (§3).
   Fields are never manipulated, so JSON would be parsed only to be re-rendered as markdown: round-trip overhead plus
   a rendering step where verbatim-ness could drift. Markdown-in → markdown-out is the most §3-faithful pipeline.
2. The report's only consumer is a human reader; the format needs to be stable enough to read and spot-check, not
   machine-parseable.
3. An MCP tool (even a local stdlib one) requires whitelisting under company policy — rejected on that ground
   independent of technical merit. Workflow-based fan-out is rejected as unwanted harness coupling.
4. With no transformation step to guard, a validator/parser doesn't hold its weight (simplest-solution-first).

**Hardenings that travel with the decision:**

- The return format is single-sourced: one short contract file (`references/return-contract.md` — finding schema,
  exact sentinels, label rule, ordering duty) pasted into every sub-agent template via a common `{RETURN_CONTRACT}`
  placeholder. Sub-agents are never asked to look it up by path.
- Sentinels are exact strings: a clean axis returns exactly `NO FINDINGS: <one line>`; Standards with no sources
  returns exactly `SKIPPED: <reason>`. They are what make a dead or empty return detectable without a parser.
- Each sub-agent orders its own findings blockers-first, so aggregation is pure concatenation plus a composed
  per-axis summary line (finding count = bullet count).
- The §11 rerun-once trigger is a deterministic acceptance checklist in the verify step, not a judgement: accept iff
  the return is exactly a sentinel line OR contains ≥1 finding bullet matching the schema shape with a cite line;
  otherwise rerun once naming the defect; second failure → `not reviewed`.
- Future trigger: if a machine consumer ever appears (e.g. posting findings as PR comments), revisit a structured
  return channel then — not before.

## 2026-07-10 Amendment (validation and reruns)

Supersedes the §11 rerun-once acceptance checklist in the 2026-07-09 Amendment's hardenings. Driven by phase 3–4
harness evidence: sub-agents repeatedly added preamble/closing commentary even when a rerun named that exact
defect, so strict format gating doesn't converge — and each enforcement rerun cost a full re-review.

1. **Return contract restructured for salience, not gating** (user edit): the finding schema sits in a
   `<template>` tag, the label rule in a `<rule>` tag, and the return-only + no-first-person rules in a
   `<CRITICAL>` block at the end of the file — which, because the contract is pasted last into every template, is
   the final content of every filled prompt.
2. **Tiered, axis-aware validation** replaces the format gate. Hard checks (repair-rerun on failure): usability
   floor — non-empty return containing a sentinel or ≥1 legally-labelled bullet (all axes); every finding path
   appears in `git diff --name-only <fixed-point>...HEAD` (Structure, Standards); every gate TSV path reappears
   as a `blocker (presumptive)` finding (Structure); `SKIPPED:` only ever from Standards. Advisory — pasted
   through with a one-line orchestrator note, never a rerun: Spec paths absent from both diff and repo
   (legitimate for missing-requirement findings — a phase 4 harness run anchored a correct finding to a file
   whose absence it was reporting), unknown labels, format noise (preamble, headers, commentary, first person).
3. **Repair-rerun, not re-review**: the rerun prompt is the original filled prompt + the previous return verbatim
   + the explicit defect list + "Repair the listed defects. Keep every finding whose substance is sound. Do not
   re-review from scratch." Usability-floor failures have nothing to repair and rerun the original prompt.
   Second failure → `not reviewed`, unchanged.

Contract C in `plan/index.md` carries the binding restatement; phases 4–6 reference it.
