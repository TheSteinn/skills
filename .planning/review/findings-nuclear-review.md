# Adversarial review: `nuclear-review.md` (thermo-nuclear-code-quality-review)

Target: `.planning/review/nuclear-review.md` (191 lines, ~1,920 words).
Baseline for "good" in this repo: `skills/*/SKILL.md` (median ~67 lines; every process skill uses numbered steps, exact commands, prompt templates, and explicit gates — see `skills/implement/SKILL.md`, `skills/tdd/SKILL.md`) and the sibling `two-axes-review.md` (88 lines, fully deterministic 5-step process).

## 1. What the skill does well

**A coherent, unmistakable reviewer identity.** The intro (lines 9–11) states the posture in three sentences: strict, maintainability-focused, "ambitious" about structure, hunting "code judo" moves — "restructurings that preserve behavior while making the implementation dramatically simpler" (line 11). A model reading this cannot mistake what kind of review is wanted. Persona-setting is the one job the document does thoroughly.

**Several individually sharp, concrete criteria.**
- The 1000-line file threshold (line 34) — the only *objective, checkable* rule in the document.
- "Refactors that move code around but fail to reduce the number of concepts a reader must hold in their head" (line 94) — the best single test in the file for whether a refactor is real or cosmetic.
- "Thin abstractions, identity wrappers, or pass-through helpers that add indirection without buying clarity" (line 54).
- "'Temporary' branching that is likely to become permanent debt" (line 105).
- "One-off booleans, nullable modes, or flags that complicate existing control flow" (line 97).

**Good output discipline — in two places.** The 7-level severity ladder (lines 156–164) is a fixed ordering for findings, the document's only genuinely deterministic output constraint. And lines 166–167 ("Do not flood the review with low-value nits… Prefer a smaller number of high-conviction comments") directly counter the classic failure mode of strict-review prompts: nit avalanches.

**Tone calibration by example.** The "Good phrases" list (lines 142–152) pins the register with nine concrete utterances instead of adjectives. As a *technique*, verbatim example outputs are more reliable than "be direct but not rude" (lines 137–138) alone — though the specific phrases have problems (see §2).

**Burden-shifting approval policy.** "Treat these as presumptive blockers unless the author can justify them clearly" (line 183) is a well-conceived mechanism: the author, not the reviewer, carries the burden of proof. A real review-policy idea, not filler.

**Frontmatter follows house convention.** `disable-model-invocation: true` (line 4) matches the pattern for explicitly-invoked skills (`skills/implement/SKILL.md` line 4), and the description (line 3) carries trigger phrases per skill-creator guidance.

## 2. What the skill does poorly

### No process. None.
Zero numbered steps, zero commands, zero templates, zero output format. It never says how to obtain the changes — the entire scoping is "the current branch's changes" (line 17): no diff command, no base ref, no merge-base decision, no "ask the user", no empty-diff handling. Contrast `two-axes-review.md`, which pins the exact command (`git diff <fixed-point>...HEAD`, line 21), validates the ref *before* work starts (line 23), and prescribes output headings and word limits (lines 66, 72, 78). Nuclear-review is 2.2× longer and specifies none of this.

### Sevenfold restatement of the same seven ideas.
The document is structurally a matrix: ~7 concerns × ~7 restatement formats (rule → question → flag → remedy → phrase → priority → bar item → blocker). Traced occurrences:

| Concern | Restatements (line refs) |
|---|---|
| Code-judo / dramatic simplification | 9–10: intro 11; prompt 18, 20; rule 0 (27–32); Q 75–76; flags 93–94; remedies 116–118, 132–133; phrases 151–152; priority 159; bar 175; blocker 185 |
| 1000-line file | 8: rule 1 (34–38); Q 81; flag 95; remedy 120; phrase 144; priority 162; bar 176; blocker 186 |
| Spaghetti / ad-hoc branching | ~15 mentions in 8 sections: rule 2 (40–44); Q 78, 82, 83; flags 96, 97, 103, 105; remedies 117, 122, 124; phrases 145–146; priority 160; bar 177; blockers 187–188 |
| Thin wrappers / magic | 8: rule 4 (51–54); Q 84; flags 99–100; remedies 119, 125; phrase 148; priority 163; bars 178–179; blocker 189 |
| Types / casts / optionality | 8: rule 5 (56–59); Q 85; flag 101; remedy 127; phrase 149; priority 161; bar 179; blocker 189 |
| Canonical layer / helper reuse | 7: rule 6 (61–64); Q 80, 86; flags 98, 102, 106–107; remedies 126, 128; phrases 147, 150; bar 180; blocker 190 |
| Orchestration / atomicity | 4: rule 7 (66–69); Q 87; flags 108–109; remedies 129–130 |

Each restatement is a paraphrase, not a refinement — "New conditionals bolted onto unrelated code paths" (96) vs. "weird if statements in random places" (42) vs. "ad-hoc branching that makes an existing flow more tangled" (187). This is exactly the length/instruction-count pattern that causes drift: ~120 discrete items to convey ~7 heuristics.

### An instruction to presuppose the conclusion.
"**Assume** there is often a 'code judo' move available" (line 31), reinforced by making "no obvious missed opportunity" an approval condition (line 175) and a "plausible code-judo move" a presumptive blocker (line 185). An LLM told to assume a dramatic simplification exists, and empowered to block when it "sees" one, is incentivized to hallucinate restructurings. Nothing requires a proposed restructuring to be validated (sketched, behavior-preservation argued). The lone counterweight is the slogan "Measure twice, cut once" (line 21).

### Reviewer, rewriter, or gatekeeper? Never resolved.
Three output modes blended with no selection rule: **rewriter** — "Rethink how to structure / implement the changes… go for it" (lines 18, 20); **commenter** — the Good phrases (142–152) are PR comments to a human author ("can we decompose this first?"); **gatekeeper** — the Approval Bar (169–192) implies a verdict. A model can legitimately end this skill by editing files, writing comments, or issuing a verdict.

### The final instruction is ambiguous and, under the nearest reading, inverted.
Line 192: "If those conditions are not met, leave explicit, actionable feedback." The nearest antecedent of "those conditions" is the blocker list (185–190); blockers "not met" = no blockers = the good case — demanding feedback precisely when the PR is fine. The intended referent is presumably the approval bar (174–181), two lists earlier. A closing gate whose referent must be guessed is not a gate.

### "Non-Negotiable" standards that negotiate.
The section titled "Non-Negotiable Additional Standards" (line 23) contains "Only waive this if there is a compelling structural reason" (line 38), and the blockers apply "unless the author can justify them clearly" (line 183). The escape hatches are sensible; the heading is false advertising that teaches the model to discount the document's emphasis words.

### Everything is escalated, so nothing is.
"What to Flag **Aggressively** / **Escalate** findings when you see:" (89–91) is followed by 17 unranked triggers broad enough to hit nearly any diff. This competes directly with "Do not flood the review with low-value nits" (166) and "smaller number of high-conviction comments" (167), with no tie-breaking rule beyond the severity ladder.

### Subjective gate conditions throughout.
The approval bar hangs on judgment adjectives: "no **clear** structural regression" (174), "**obvious**" ×4 (175, 177, 178, 181), "**unjustified**" (176), "**unnecessary**" (179), "**avoidable**" (180). Except the line count, none is checkable; the "bar" is a mood.

### House-voice violations.
Repo rule (memory: no first person in skills, "sweep templates and sketches too"): line 151 opens "**i think** there's a code-judo move here", and lines 144–152 use "can **we**… / **let's** keep the behavior / something **we** already have" — first person in exactly the strings the model is told to emit.

## 3. Best attributes worth extracting

1. **The 1000-line gate** (34–38) — portable as a genuinely deterministic check: per-file line counts before/after the diff; crossing 1k = automatic finding. Two shell commands replace four bullets of prose.
2. **The "concepts a reader must hold" criterion** (94) — sharpest articulation of real vs. cosmetic refactoring; worth quoting verbatim anywhere.
3. **The Primary Review Questions** (73–87), deduplicated to ~7 (one per concern) — a fixed per-hunk checklist, i.e., the deterministic loop scaffold this skill lacks.
4. **The severity ladder** (156–164) — drop-in deterministic output ordering for any review skill.
5. **Presumptive-blocker burden shift** (183) — paired with objective triggers it becomes a real gate.
6. **The signal-to-noise rule** (166–167).
7. **Tone-by-example** (142–152) — the mechanism is reusable even though these phrases need a voice sweep.
8. **The concern→remedy pairing** (rules 0–7 ↔ remedies 115–130), Fowler-style. Compressed into one table (concern | tell | remedy) it would replace roughly 140 of the 191 lines with no information loss — the document is machine-generatable from that table, which is both the extraction and the indictment.
9. Individual heuristics worth keeping verbatim: identity wrappers (54/100), one-off booleans/nullable modes (97), temporary-branching-becomes-debt (105), bespoke-helper-vs-canonical (106).

## 4. Worst aspects (ranked, most severe first)

1. **No executable process** (whole document). No steps, no diff command, no scope resolution, no output template, no verdict format, no error handling. Failure mode: every invocation improvises — different diff bases, different output shapes, sometimes edits instead of comments, sometimes no explicit verdict. The sibling proves the house fix in half the length.
2. **~7 concerns restated ~7 times each.** Failure mode: attention dilution — the model samples a subset of ~120 items per run, so behavior varies run-to-run; late sections compete with early ones instead of building on them. Fix: one 7-row table + one checklist + one gate; target ≤60 lines.
3. **The "assume a judo move exists" bias + missed-opportunity blocker** (31, 175, 185). Failure mode: hallucinated restructurings delivered with the mandated "demanding" confidence (137), blocking correct PRs on speculative redesigns nothing requires be validated. Fix: any judo claim must include a concrete sketch and behavior-preservation argument; unvalidated ones demote to suggestion.
4. **Unresolved reviewer/rewriter/gatekeeper role** ("go for it" 20 vs. phrases 142–152 vs. bar 169–192). Failure mode: an agent that mutates the working tree when the user wanted comments. Fix: one sentence declaring the output contract.
5. **Ambiguous, possibly inverted closing instruction** (192). Failure mode: the final gate — the thing the document builds to — fires on the wrong branch or is skipped as noise.
6. **Subjective approval bar** (174–181). Failure mode: the gate outputs whatever the model already felt; two runs on the same diff can verdict differently while both "following" the skill.
7. **Undefined review scope** ("the current branch's changes", 17). Failure mode: confidently reviewing the wrong diff (uncommitted vs. branch vs. merge-base).
8. **Minor**: "Non-Negotiable" heading contradicted by its own waivers (23 vs. 38/183); first-person voice in emit-phrases (144–152) against repo convention.

## Quantitative profile

- **Size**: 191 lines, ~1,920 words. Repo median SKILL.md ~67 lines; sibling two-axes-review 88 lines. Within skill-creator's <500-line letter, but 2–3× house norm while specifying no process.
- **Discrete instruction items**: ~120. Breakdown: 8 numbered rules + 28 sub-bullets (23–69); 13 review questions (75–87); 17 flag triggers (93–109); 16 remedies (115–130); 9 tone phrases (142–152); 7 priority levels (156–164); 8 bar conditions + 6 blockers (174–190); ~13 standalone imperative sentences (11, 17–21, 132–133, 137–140, 166–167, 171, 192).
- **Prohibitions**: 12 "Do not" instructions (11, 28, 34, 40, 48, 69, 132, 133, 137×2, 166, 171) — self-restraint with no enforcing mechanism.
- **Decision points**: ~15 prose conditionals (37, 38, 42, 47, 59, 67, 183, 192, …). **Deterministic branches/steps/templates: 0.** Deterministic structures present: the severity ladder (fixed ordering) and one numeric threshold (1,000 lines). No numbered process, no command, no output schema, no checklist artifact.
- **Distinct concerns attempted**: ~10 (seven quality axes + tone + output ordering + approval policy). Absent: diff acquisition, scope confirmation, context management (no subagents despite a whole-branch "deep audit"), output format, edge handling (empty diff, missing base, huge diff), interaction mode.
- **Memory/self-policing spans flagged**: line 73 "For every meaningful change, ask:" → prose loop of 13 questions × N hunks, no tracking — partial execution guaranteed; the Approval Bar (169–192) requires recalling all findings and evaluating 8+6 subjective conditions at the end — long-span state retention with no artifact; the reviewer must simultaneously hold 8 rules + 13 questions + 17 flags while reading code; competing self-policing pairs: "escalate" (91) vs. "do not flood" (166), "be ambitious" (11) vs. "measure twice" (21), "demanding" (137) vs. "do not be rude" (138).

## Verdict

A values document wearing a skill's frontmatter. The reviewer persona is vivid and internally consistent, and five or six heuristics/mechanisms are genuinely worth extracting (the 1k-line gate, the concepts-held criterion, the severity ladder, the burden-shift blocker policy, the signal-to-noise rule). But as an executable skill it fails the evaluation lens on both counts: long and repetitive where it should be compressed (~7 ideas × ~7 restatements across ~120 items), and prose-judgment everywhere it should be deterministic (no steps, no commands, no templates, one checkable condition in 191 lines, a final gate with an ambiguous referent). Roughly 70% of the text could collapse into a 7-row concern table with zero information loss; the remaining effort belongs in the process scaffolding the document never provides. `two-axes-review.md` demonstrates the target shape in the same directory at half the length.
