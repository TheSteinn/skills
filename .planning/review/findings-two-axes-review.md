# Adversarial review: `two-axes-review.md`

Target: `.planning/review/two-axes-review.md` (88 lines, 1,104 words; frontmatter name `code-review`).
Baseline for "good": the house skills in `skills/*/SKILL.md` (median ~65–75 lines; deterministic numbered protocols, verbatim fill-in prompt templates, structured report-back formats, explicit STOP gates) and the repo's documented conventions (README, `docs/` deviation records).

## 1. What the skill does well

**Right length.** At 88 lines / ~1,100 words it sits squarely in this repo's normal band (shorter than `implement` at 120 lines, `domain-modelling` at 133; less than half of the sibling `nuclear-review.md` at 191). Under the length/drift lens this is a genuine pass: an executor can hold the whole thing in attention.

**Linear control flow, no loops.** The skill is a straight five-step pipeline (`### 1` … `### 5`, lines 17–80) with exactly one fan-out point (step 4). There is no prose-described looping, no "repeat until", no iteration the LLM must self-manage. Structurally this is the safest shape a skill can have.

**Fail-fast gate before the expensive fan-out.** Line 23: "confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents." A concrete, checkable precondition with an explicit rationale, placed exactly where it prevents the worst waste. Best single instruction in the file.

**Deterministic spec-source fallback chain.** Lines 27–32 are a numbered priority list (commit-message refs → user-passed path → conventional locations → ask the user) with terminal explicit-skip semantics ("the **Spec** sub-agent will skip and report 'no spec available'", line 32). Branching done the right way: an ordered protocol, not scattered "if X consider Y" prose.

**Precise git semantics.** Line 21 specifies `git diff <fixed-point>...HEAD` and explains why ("three-dot, so the comparison is against the merge-base"). No room for the two-dot/three-dot mistake an LLM commonly makes.

**Correct context-isolation model.** Line 11 states the reason for parallel sub-agents ("so they don't pollute each other's context") and line 65 shows real understanding of subagent isolation: the smell baseline must be "pasted in full — the sub-agent has no other access to it." The skill does not assume subagents share the orchestrator's context.

**Bounded sub-agent output.** Both briefs end with "Under 400 words" (lines 66, 72), capping what flows back into the aggregation context.

**Explicit conflict-resolution rule.** Line 40: "**The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell." A stated precedence order between the generic baseline and local standards — most review skills leave this collision undefined.

**Evidence-anchored findings.** Both briefs demand citations: "cite the standard (file + the rule)… name it and quote the hunk" (line 66); "Quote the spec line for each finding" (line 72). Matches the repo's citation culture (`research` requires file:line for every claim).

**A stated invariant with its rationale, enforced twice.** "Do **not** merge or rerank findings" (line 78) and "Don't pick a single winner across axes — that's the reranking the separation exists to prevent" (line 80), backed by "Why two axes" (lines 82–89). The design intent is legible and the aggregator is told exactly what transformation is forbidden.

**Uniform smell schema.** Each of the 12 baseline smells (lines 45–56) follows one shape — name, one-line recognition rule, `→` one-line fix. Compact, parallel, scannable.

**Voice compliance.** No first-person anywhere; addresses "you"/"the user" throughout, per house convention.

## 2. What the skill does poorly

**A dead-end foreign dependency (line 13).** "The issue tracker should have been provided to you — run `/setup-matt-pocock-skills` if `docs/agents/issue-tracker.md` is missing." Neither artifact exists anywhere in this repo (repo-wide grep: the only hit is this file). `/setup-matt-pocock-skills` is not an installed skill; `docs/agents/` does not exist. This is unedited provenance leakage from Matt Pocock's skills repo (credited in the README as a source). An agent obeying it hits a nonexistent skill; an agent skipping it leaves step 2.1's "fetch via the workflow in `docs/agents/issue-tracker.md`" (line 29) unexecutable. It breaks three house conventions at once: explicit invocation of *existing* skills only, "ask, don't discover org specifics", and no auto-setup remedies.

**Sub-agent prompts are ingredient lists, not templates.** Lines 62–72 specify each prompt as "include:" plus bullets. The house convention is the opposite: `implement` says "Build every prompt from this template, filling the placeholders and changing nothing else" (a full fenced template); `research` sources prompts from `references/subagent-prompts.md`. Here the orchestrator assembles wording, ordering, and framing fresh on every run — precisely the non-deterministic construction the repo's orchestration doctrine exists to eliminate. Only the quoted "brief" sentences are fixed; everything around them is improvised.

**Data-vs-pointer ambiguity in the prompts.** Line 64 says include "The full diff command and commit list" — the *command*, so presumably the sub-agent re-runs it; but line 71 says "The path or fetched contents of the spec" — an unguided `or` with no criterion. If the spec came from an issue tracker (step 2.1), passing "the path" hands the sub-agent a reference it cannot resolve (no tracker access, no tracker doc). The correct rule — fetched content must be pasted, repo files may be paths — is derivable but never stated.

**The severity classification lives only inside a sub-agent brief.** Line 66 introduces the hard-violation/judgement-call distinction ("documented-standard breaches can be hard, but baseline smells are always judgement calls") — inside the quoted brief, addressed to the sub-agent. Step 5 then requires the orchestrator to name "the worst issue _within each axis_" (line 80) with no severity criteria of its own. The aggregator must rank using a scheme the skill only ever gave to someone else.

**Duplicated rule statements that can drift.** The baseline's two binding rules appear at lines 40–41 and are restated in different words inside the brief at line 66 ("a documented repo standard overrides the baseline. Skip anything tooling enforces."). Two phrasings of one rule in one file is a maintenance hazard: edit one, and the skill argues with itself. Line 66's "documented-standard breaches *can be* hard" adds a hedge that appears nowhere in step 3.

**Unbounded standards discovery.** Line 36 in its entirety: "Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`." Contrast with step 2's ordered four-item chain: step 3 gives no search protocol, no candidate list beyond two examples (no `CLAUDE.md`, lint configs, or `docs/`), and no stopping rule. Two runs on the same repo can assemble different standards corpora. "Skip anything tooling already enforces" (line 41) compounds it: the sub-agent must filter against a tooling configuration it was never given and has no instruction to discover.

**No post-spawn failure handling of any kind.** After step 4 there is no protocol for a sub-agent that errors, returns nothing, blows the 400-word cap, or produces uncited claims. Compare `implement`: rerun-with-failure-output, fresh-agent retry, "Two failures on one phase → stop." Here a failed Standards agent silently becomes an empty `## Standards` section indistinguishable from "no findings".

**"Verbatim or lightly cleaned" (line 78) is undefined** and sits in the same sentence as the merge/rerank prohibition. "Lightly cleaned" is a judgement licence adjacent to the exact transformation being forbidden; nothing says what cleaning is permitted.

**Smell baseline must be re-transcribed by hand.** Line 65 requires the 12-entry baseline "pasted in full" into a prompt — the orchestrator re-emits ~19 lines of skill text from context. The house pattern ("paths as persisted memory"; `research`'s `references/` file) would put the baseline in a `references/smell-baseline.md`, making inclusion a file operation instead of a fidelity-dependent transcription.

**Frontmatter deviations.** `name: code-review` (line 2) collides with the harness's built-in `/code-review` skill and is maximally generic. Every comparable house skill — including the sibling `nuclear-review.md` — carries `disable-model-invocation: true`; this one omits it while shipping a trigger-rich description, so it competes for auto-invocation against the built-in of the same name.

**The dependency check is buried in the preamble.** Line 13 sits between the overview and `## Process`, outside any numbered step. The one consumer of the tracker doc (step 2.1, line 29) doesn't mention the missing-doc case; the remedy and the need are 16 lines apart and unlinked.

**Some smells are not diff-detectable, and the sub-agent's read scope is unstated.** Feature Envy (line 47) and Refused Bequest (line 56) require seeing class definitions beyond the hunks; Divergent Change (line 52) implies knowing "several unrelated reasons" for edits. The Standards sub-agent is never told whether it may read whole files or only the diff — the framing says "match it against the diff" (line 44), which makes several baseline entries unjudgeable as specified.

## 3. Best attributes worth extracting

1. **Validate-before-fan-out gate** (line 23). "Fail here — not inside two parallel sub-agents": cheap deterministic precondition checks before any parallel spend. Port into any skill spawning subagents off user-supplied refs.
2. **The orthogonal-axes report contract** (lines 78–80, 82–89). Separate review dimensions, reported side by side, with an explicit anti-merge/anti-rerank invariant *and its rationale* ("stops one axis from masking the other", line 89). Generalizes to any multi-dimension review (security vs. correctness, performance vs. readability).
3. **The what→fix smell checklist schema** (lines 45–56). Twelve heuristics, each "recognition rule → remedy" in two clauses. As a standalone `references/` checklist this is immediately reusable — more disciplined than `nuclear-review.md`'s 18-item unstructured flag list.
4. **The precedence rule** (line 40): "A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell." A one-line conflict-resolution clause every generic-baseline-vs-local-convention skill needs and most lack.
5. **Word-capped, citation-mandatory sub-agent briefs** (lines 66, 72). "Under 400 words" + "quote the hunk"/"Quote the spec line" bounds return size while forcing evidence anchoring.
6. **Explicit graceful degradation for a missing spec** (lines 32, 74): the axis skips *and says so* in the final report, rather than silently narrowing scope.
7. **The stated isolation rationale** (line 11) and isolation-aware prompt construction (line 65) — the correct mental model to copy even where this file's mechanism (hand transcription) shouldn't be.

## 4. Worst aspects, ranked

1. **The broken `/setup-matt-pocock-skills` / `docs/agents/issue-tracker.md` dependency (lines 13, 29).** Failure mode: unexecutable in this repo — the agent invokes a nonexistent skill or silently loses step 2.1, the *first and highest-priority* spec-discovery route. Fix: replace with this repo's convention (user-maintained org-setup reference, or ask the user), moved into step 2 as a numbered gate.
2. **Non-deterministic prompt assembly (lines 62–72).** Failure mode: differently worded, differently ordered sub-agent prompts every run; the "path or fetched contents" branch (line 71) can hand a sub-agent an unresolvable reference. Fix: two verbatim fenced templates with placeholders, `implement`-style, with the content-vs-path rule explicit.
3. **Unbounded standards discovery + un-checkable tooling filter (lines 36, 41).** Failure mode: standards corpus differs per run; the sub-agent must "skip anything tooling enforces" against tooling it cannot see. Fix: an ordered candidate list like step 2's, plus pass lint/format configs or drop the clause.
4. **No sub-agent failure/verification protocol after step 4.** Failure mode: a crashed or empty Standards report renders as a clean pass; no distinction between "no findings" and "no review happened". Fix: empty/failed report → rerun once → then report the axis as *not reviewed*.
5. **Severity scheme defined only inside the sub-agent brief (line 66) while the aggregator must rank "the worst issue" (line 80).** Failure mode: within-axis ranking improvised per run; a judgement-call smell can outrank a hard documented-standard breach. Fix: state the ordering once, in step 5.
6. **Rule duplication between lines 40–41 and line 66.** Failure mode: future edits desynchronize the phrasings; orchestrator and sub-agent operate under different precedence rules. Fix: state the rules once in a block the prompt template includes by reference.
7. **Hand-transcribed baseline (line 65).** Failure mode: 12 smells copied from context into a prompt invites truncation or paraphrase drift; bloats the skill body with content only a sub-agent consumes. Fix: `references/smell-baseline.md`, pasted via file read.
8. **Frontmatter: colliding generic `name: code-review`, missing `disable-model-invocation: true` (lines 2–3).** Failure mode: auto-trigger competition with the built-in `/code-review`; ambiguous invocation. Fix: rename (e.g., `two-axes-review`) and add the flag per house pattern.

## Quantitative profile

- **Size:** 88 lines, 1,104 words. Repo context: house median ~65–75 lines; `implement` 120; sibling `nuclear-review.md` 191. The 12-smell baseline is the largest block: 19 lines (45–56 plus framing), ~22% of the file.
- **Discrete imperative instructions:** ~36 addressed to the orchestrator (8 in step 1, 6 in step 2, 5 framing + 12 smell-matching in step 3, ~10 in step 4, 6 in step 5, 1 preamble), plus ~7 embedded in the two sub-agent briefs and 12 `→ fix` directives inside smell entries. Roughly 55–60 total across both roles.
- **Decision points:** ~10. In deterministic structure: 5 (the four-item ordered spec fallback, lines 27–32; the rev-parse/non-empty gate, line 23; the spec-skip, lines 32/74). In prose: ~5–6 (ask-if-unspecified, line 19; repo-overrides suppression, line 40, per finding; skip-tooling-enforced, line 41, per finding; "path or fetched contents", line 71; "verbatim or lightly cleaned", line 78; the line-13 missing-doc remedy). Loops: **zero** — strictly linear with one parallel fan-out.
- **Distinct concerns:** 7 — ref pinning/validation, spec discovery (incl. tracker integration), standards discovery, smell taxonomy, sub-agent orchestration, aggregation/reporting, design rationale. Coherent for one skill; none off-mission.
- **State the orchestrator carries across spans:** fixed point + diff command + commit list (step 1 → 4), spec source/flag (step 2 → 4 → 5), standards file list (step 3 → 4), the full 12-smell baseline text (step 3 → 4, by transcription), spec-missing note (step 2 → 5). Modest in an 88-line file; the baseline transcription is the heaviest and most fidelity-sensitive.
- **Self-policing reliance:** aggregator restraint ("Do not merge or rerank", line 78; "Don't pick a single winner", line 80 — stated with rationale, which helps); sub-agent word caps (lines 66, 72); the sub-agent tooling-filter (lines 41/66) — the only one *unverifiable* as written.
- **Internal contradictions / competing instructions:** line 13's remedy (run a setup skill) vs. step 2.4's remedy (ask the user), with no ordering; line 66's "documented-standard breaches *can be* hard" hedging a scheme step 3 never states; "lightly cleaned" (line 78) granted in the same breath as the merge/rerank prohibition; smell definitions requiring beyond-diff context (lines 47, 52, 56) vs. "match it against the diff" (line 44).

## Verdict

Skeleton: good. Wiring: sloppy. Judged by the lens that matters — length, instruction count, deterministic control flow — the skill is fundamentally sound: short by house standards, strictly linear with zero loops, gates its one expensive operation behind a concrete precondition check, uses a genuinely deterministic fallback chain for spec discovery, and states its one architectural invariant (no cross-axis reranking) clearly and with rationale. Its two-axis contract, smell checklist schema, and fail-before-fan-out gate are worth extracting regardless of the file's fate.

But it is not shippable in this repo as-is. Its highest-priority spec-discovery path depends on a file and setup skill that exist only in the source author's repo (lines 13/29); its sub-agent prompts — the load-bearing artifacts of the whole design — are assembled ad hoc from ingredient bullets in direct violation of the house's strongest convention (verbatim fill-in templates); its standards discovery is a one-sentence shrug; and nothing after the fan-out checks whether the sub-agents actually delivered. Fixing ranked items 1–4 converts a well-shaped draft into a skill consistent with `implement`-grade orchestration discipline; leaving them makes its two headline sections only as reliable as whatever prompt the orchestrator happened to improvise that day.
