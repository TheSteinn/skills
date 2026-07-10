# Comprehensive findings: `nuclear-review.md` vs `two-axes-review.md`

Synthesis of two independent adversarial reviews (one subagent per skill, each instructed to judge against the same lens: **skills must not be overly long or instruction-dense — that causes drift and attention loss — and control flow must live in deterministic protocols, not in prose the LLM is trusted to follow**). Individual reports: `findings-nuclear-review.md`, `findings-two-axes-review.md`. Every load-bearing factual claim below was re-verified against the source files and the repo by the orchestrator; corrections to subagent claims are listed in the fact-check appendix.

## Headline

The two skills fail the lens in **opposite directions, and each has exactly what the other lacks**:

- **`nuclear-review.md`** is all *content*, no *process*: ~7 genuinely good review heuristics restated across ~120 discrete instruction items in seven parallel formats, with zero numbered steps, zero commands, zero output template, and a single reviewer expected to self-police the whole thing. It is a values document wearing a skill's frontmatter.
- **`two-axes-review.md`** is all *process*, weak *wiring*: a short, strictly linear 5-step pipeline with a real fail-fast gate and correct subagent-isolation thinking — but its highest-priority spec path depends on a file and a setup skill that do not exist in this repo, and its load-bearing sub-agent prompts are assembled ad hoc from ingredient lists instead of verbatim templates.

Neither is shippable as-is. `two-axes-review.md` is close (four targeted fixes); `nuclear-review.md` needs a structural rewrite, though its heuristic content is the most valuable raw material in either file.

## Quantitative comparison

| Measure | `nuclear-review.md` | `two-axes-review.md` | Repo baseline |
|---|---|---|---|
| Lines / words | 191 / 1,922 | 88 / 1,104 | median SKILL.md ~70 lines (18 skills, range 7–485) |
| Discrete imperative instructions | ~120 | ~55–60 (both roles) | — |
| Numbered process steps | **0** | 5 | house norm: numbered steps |
| Deterministic structures | 1 numeric threshold (1,000 lines), 1 fixed severity ordering | validation gate, 4-item fallback chain, fixed report headings, 400-word caps | — |
| Prose-only decision points | ~15 | ~5–6 | — |
| LLM-managed loops | 13 questions × N hunks, untracked | none | — |
| Subagent orchestration | none (single reviewer, whole-branch "deep audit") | 2 parallel sub-agents, isolation-aware | verbatim prompt templates (`implement:34`) |
| Output contract | priority ordering only; no format, no verdict template | `## Standards` / `## Spec` + one-line summary | structured report-backs |
| External dependencies | none | 2 — **both nonexistent in this repo** | — |
| Frontmatter | `disable-model-invocation: true`, distinctive name | name `code-review` collides with the built-in skill; no flag | process skills carry the flag |
| Internal contradictions | ≥4 competing pairs | ~4 (mostly duplication drift) | — |

## Axis 1 — What each does well

**Shared strength: both know what a good finding looks like.** Nuclear demands high-conviction, structural findings over nit floods (166–167) and orders them by severity (156–164); two-axes demands citations for every claim ("cite the standard (file + the rule)", "Quote the spec line", lines 66/72) and caps sub-agent output at 400 words.

**Nuclear's distinct strengths** are all *content-level*:
- A vivid, internally consistent reviewer persona (strict, ambitious, structure-first) that a model cannot misread.
- Individually sharp heuristics: the 1,000-line file gate (34, the file's only objective rule); "concepts a reader must hold in their head" as the test of a real refactor (94); identity-wrapper detection (54); temporary-branching-becomes-debt (105).
- Two real policy mechanisms: the presumptive-blocker burden shift ("unless the author can justify them clearly", 183) and tone-calibration by example phrases (142–152).

**Two-axes' distinct strengths** are all *process-level*:
- Right size (88 lines) and the safest possible shape: strictly linear, zero loops, one fan-out.
- The best single instruction in either file: validate `git rev-parse <fixed-point>` and non-empty diff *before* spawning — "fail here — not inside two parallel sub-agents" (23).
- Deterministic branching done properly: a numbered 4-item spec-source fallback chain ending in explicit-skip semantics (27–32).
- Correct subagent mental model: isolation stated with rationale (11), baseline "pasted in full — the sub-agent has no other access to it" (65).
- A stated architectural invariant with its why: never merge or rerank across axes, because "reporting them separately stops one axis from masking the other" (78–80, 89).
- The 12-smell Fowler baseline in a uniform *what → fix* schema (45–56), with an explicit precedence rule: "A documented repo standard always wins" (40).
- Exact git semantics: three-dot diff against the merge-base, with the reason spelled out (21).

## Axis 2 — What each does poorly

**Nuclear** — failure is *architectural*:
1. No executable process at all: scope is just "the current branch's changes" (17) — no diff command, no base ref, no output format, no error handling. Every invocation improvises.
2. Massive redundancy: ~7 concerns × ~7 restatement formats (rules → questions → flags → remedies → phrases → priorities → bar → blockers), each a paraphrase rather than a refinement. This is precisely the instruction-density pattern the lens warns about: the model samples a different subset of ~120 items each run.
3. Presupposed conclusions: "Assume there is often a 'code judo' move available" (31) plus blocker status for "missed opportunity" (175, 185) incentivizes hallucinated restructurings, with no validation requirement (no sketch, no behavior-preservation argument).
4. Unresolved role: rewriter ("go for it", 20) vs. PR commenter (the phrases, 142–152) vs. gatekeeper (the approval bar, 169–192) — a model can legitimately end the skill by editing files, commenting, or issuing a verdict.
5. An ambiguous closing gate: "If those conditions are not met" (192) most naturally refers to the blocker list, under which reading it is inverted (fires when the PR is fine).
6. Self-negating emphasis: "Non-Negotiable" standards with waiver clauses (23 vs. 38/183); "Flag Aggressively" (89) vs. "do not flood with nits" (166); a bar built on "clear/obvious/unjustified" adjectives — only one condition in 191 lines is objectively checkable.
7. House-voice violations: first person ("i think", "can we", "let's") inside the very strings the model is told to emit (144–152).

**Two-axes** — failure is *in the wiring*:
1. A dead-end foreign dependency: `/setup-matt-pocock-skills` and `docs/agents/issue-tracker.md` (13, 29) exist nowhere in this repo (verified by grep and `ls`) — unedited provenance leakage that dead-ends the *highest-priority* spec-discovery route.
2. Sub-agent prompts as "include:" ingredient lists (62–72), not verbatim fill-in templates — directly against the house convention (`implement:34`: "filling the placeholders and changing nothing else"; `research` keeps prompts in `references/subagent-prompts.md`). The load-bearing artifacts of the whole design are improvised per run.
3. Unbounded standards discovery: "Anything in the repo that documents how code should be written" (36) — no ordered candidate list, no stopping rule; plus a filter ("skip anything tooling already enforces", 41) the sub-agent cannot check because it never receives the tooling config.
4. No post-spawn failure handling: a crashed or empty axis renders as a clean pass, indistinguishable from "no findings".
5. Smaller defects: severity scheme defined only inside a sub-agent brief (66) while the aggregator must rank "the worst issue" (80); rule duplication that can drift (40–41 vs. 66); undefined "verbatim or lightly cleaned" (78); "path or fetched contents" with no criterion (71) — a tracker-fetched spec passed as a path is unresolvable; several baseline smells (Feature Envy, Refused Bequest, Divergent Change) are not judgeable from the diff alone while the brief says "match it against the diff" (44); frontmatter name collides with the built-in `/code-review` and lacks `disable-model-invocation: true`, which every process-type skill in this repo carries.

## Axis 3 — Best attributes worth extracting (merged, ranked)

From **two-axes** (process mechanisms):
1. **Validate-before-fan-out gate** (23) — cheap deterministic precondition checks before any parallel spend.
2. **Orthogonal-axes report contract** (78–80, 82–89) — separate review dimensions reported side by side, with an explicit anti-merge/anti-rerank invariant *and its rationale*. Generalizes to any multi-dimension review.
3. **Numbered fallback chain with explicit-skip terminal** (27–32) — the correct deterministic encoding of "try A, then B, then C, else degrade visibly".
4. **What→fix checklist schema** (45–56) + **repo-overrides precedence rule** (40) — a pasteable heuristic baseline with its conflict-resolution clause built in.
5. **Word-capped, citation-mandatory sub-agent briefs** (66, 72).

From **nuclear** (review content and policy):
6. **The deduplicated 7-concern heuristic set** (rules 0–7 with their remedies, 23–69 / 115–130) — compressed to one *concern | tell | remedy* table it carries ~140 lines of the file losslessly. This is exactly the shape of two-axes' smell baseline, and would slot into the same pasted-baseline mechanism.
7. **The 1,000-line gate** (34–38) — the only objective rule in either file's review content; two shell commands make it fully deterministic.
8. **"Concepts a reader must hold" criterion** (94) — the sharpest real-vs-cosmetic-refactor test; worth quoting verbatim anywhere.
9. **Severity ladder** (156–164) and **signal-to-noise rule** (166–167) — drop-in output ordering plus nit suppression for any review skill.
10. **Presumptive-blocker burden shift** (183) — becomes a real gate when paired with objective triggers like #7.
11. **Tone-by-example** (142–152) — the mechanism (verbatim sample utterances instead of adjectives), after a voice sweep.

**The compatibility observation:** these extractions compose. Nuclear's deduplicated concern table is a third review axis ("Structure/Maintainability") that fits two-axes' architecture as-is: a third parallel sub-agent, its baseline pasted in full like the smell list, its findings reported under a third heading, ranked by nuclear's severity ladder, filtered by nuclear's signal-to-noise rule, gated by objective triggers with the burden-shift policy. Neither subagent was asked to design a merger; this follows directly from their independent findings.

## Axis 4 — Worst aspects that desperately need improvement

**Nuclear (ranked by its reviewer):**
1. No executable process — every run improvises scope, output shape, and even whether it edits or comments.
2. ~7 ideas × ~7 restatements — attention dilution; run-to-run variance; ~70% of the text is losslessly compressible.
3. "Assume a judo move exists" + missed-opportunity-as-blocker — hallucination incentive with mandated confidence and no validation requirement.
4. Reviewer/rewriter/gatekeeper ambiguity — risk of mutating the working tree when the user wanted comments.
5. Ambiguous (nearest-reading inverted) closing gate at 192.
6. Subjective approval bar — two runs on the same diff can verdict differently while both "following" the skill.
7. Undefined diff scope (17).

**Two-axes (ranked by its reviewer):**
1. The nonexistent `/setup-matt-pocock-skills` / `docs/agents/issue-tracker.md` dependency (13, 29) — unexecutable as written; also violates this repo's "ask, don't discover org specifics" and no-auto-setup conventions.
2. Non-deterministic prompt assembly (62–72) — replace with two verbatim fenced templates, `implement`-style.
3. Unbounded standards discovery + uncheckable tooling filter (36, 41).
4. No sub-agent failure/verification protocol after the fan-out.
5. Severity scheme in the wrong place (66 vs. 80); 6. duplicated rules that can drift (40–41 vs. 66); 7. hand-transcribed baseline instead of a `references/` file (65); 8. frontmatter collision + missing flag (2–3).

**Severity asymmetry:** two-axes' worst defects are *local and patchable* — each has a one-section fix, and items 1–4 together are an afternoon's edit. Nuclear's worst defects are *global* — the fix is a rewrite to a different shape (a short deterministic protocol carrying a compressed heuristic table), not edits to the existing text.

## The evaluation lens, applied across both

**Length / instruction density.** Two-axes passes: 88 lines, within house range, ~55–60 instructions split across two roles, largest block (the smell baseline, ~22% of the file) is payload for a sub-agent rather than orchestrator instructions. Nuclear fails: 191 lines (2.7× house median), ~120 instruction items for ~7 underlying ideas, all aimed at a single reviewer who must hold 8 rules + 13 questions + 17 flags simultaneously while reading code.

**Deterministic control flow.** Two-axes largely passes at the *macro* level — 5 numbered steps, zero loops, a validation gate, a numbered fallback chain — but fails at the *micro* level where it matters most: prompt construction, standards discovery, and post-spawn verification are all left to per-run judgment. (The nuclear reviewer's description of the sibling as "fully deterministic" is accurate for the pipeline shape but overstated for step 4's internals.) Nuclear fails outright: zero numbered steps, ~15 prose conditionals, one untracked 13-question × N-hunk prose loop, an end-of-review approval bar requiring long-span recall of all findings against 14 mostly subjective conditions, and at least four competing self-policing pairs ("escalate" vs. "don't flood"; "be ambitious" vs. "measure twice"; "demanding" vs. "not rude"; "non-negotiable" vs. waivers).

## Fact-check appendix (orchestrator verification)

Confirmed against sources:
- Foreign dependency: `setup-matt-pocock-skills` and `issue-tracker` appear **only** in `two-axes-review.md` itself (repo-wide grep); `docs/agents/` does not exist.
- `skills/implement/SKILL.md:34` contains the exact quote "Build every prompt from this template, filling the placeholders and changing nothing else"; `skills/research/references/subagent-prompts.md` exists.
- Sizes: nuclear 191 lines / 1,922 words; two-axes 88 lines / 1,104 words; repo median SKILL.md ~70 lines across 18 skills.
- Spot-checked structural counts in both reports (8 rules, 13 questions, 17 flags, 16 remedies, 9 phrases, 7 priority levels, 8+6 bar/blockers in nuclear; 12 smells, 4-item fallback, 400-word caps ×2 in two-axes) — all accurate.
- Nuclear's first-person phrases (151: "i think…"; 144–152: "can we", "let's") and line 192's ambiguous referent — confirmed by direct read.

Corrections to subagent claims:
- Two-axes report: "Every comparable house skill … carries `disable-model-invocation: true`" is **overstated** — 10 of 18 skills carry it, 8 do not. The 8 without it are knowledge/reference skills meant to auto-trigger (acli, tdd, code-doc, …); all *process/orchestration* skills (implement, write-plan, research, open-pr, design, …) do carry it. The criticism survives in narrowed form: a review-process skill would carry the flag under house convention, and the `code-review` name collision with the built-in skill stands regardless.
- Nuclear report: the sibling is "fully deterministic" — true of the 5-step pipeline shape, not of step 4's prompt assembly (see lens section above).

## Verdicts

- **`nuclear-review.md`** — high-value review *content* in a shape that guarantees drift: no process, sevenfold redundancy, presupposed conclusions, unresolved output role. Do not run it as-is; mine it. Its deduplicated concern table, 1k-line gate, severity ladder, burden-shift policy, and signal-to-noise rule are the best extractable review content in either file.
- **`two-axes-review.md`** — the right architecture at the right size with a real gate and correct isolation thinking, undermined by a nonexistent dependency, improvised prompts, unbounded standards discovery, and silent-failure fan-out. Four targeted fixes make it consistent with `implement`-grade orchestration discipline.
- **Together** — nuclear supplies the *what to look for*; two-axes supplies the *how to run it*. The natural end state is two-axes' deterministic pipeline carrying nuclear's compressed heuristic table as a pasted baseline for a third review axis.
