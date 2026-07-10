# Design 2: Merged structure baseline

> Source: [index.md](index.md). Self-contained: refine from this file + the index only.

## Overview

Deliver `skills/three-axis-review/references/structure-baseline.md`: the single deduplicated what→fix baseline the
Structure sub-agent reads by path (durable decisions 2, 5, 9). This phase decides the mapping — which Fowler smells
collapse into which nuclear concerns — which is why it is its own phase: the mapping is the intellectual core of the
merge, and the user reviews it as content, independent of any skill prose.

## Context

**Sources being merged** (restated here for self-containment):

- The 12 Fowler smells, each "what it is → how to fix", from `.planning/review/two-axes-review.md:45-56`:
  Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun
  Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest.
- Nuclear's seven concerns, from `.planning/review/nuclear-review.md:23-69` (rules 0–7; rule 3 is posture, not a
  smell): dramatic simplification (0), the 1k-line file (1), spaghetti/ad-hoc branching (2), thin wrappers/magic (4),
  type/boundary cleanliness (5), canonical layer/helper reuse (6), orchestration/atomicity (7).
- `codebase-designing` vocabulary to write entries in (durable decision 5): the deletion test
  (`skills/codebase-designing/SKILL.md:85-86`), hypothetical seam (`:89`), interface-includes-every-fact-a-caller-
  must-know (`:21-23`), complexity as dependencies + obscurity (`:46-48`).
- The precedence rule travels with the baseline (durable decision 2): a documented repo standard always wins; where it
  endorses something the baseline would flag, suppress the entry. Every entry is a labelled judgement call, never a
  hard violation.

**Format rules**:

- Uniform schema per entry: **Name** — *tell* (one clause) → *fix* (one clause). Same shape as the source baseline —
  scannable, no sub-bullets.
- Instructions only — no provenance, no history, no "merged from" notes in the file (repo memory: no history in skill
  content). Provenance lives in the mapping table below and nowhere else.
- No first person anywhere. Target ≤ 60 lines total.

**The mapping** (this phase's binding decision — the file implements it, this table records why):

| # | Merged entry | Fowler source | Nuclear source |
|---|---|---|---|
| 1 | Mysterious Name | as-is | — |
| 2 | Feature Envy | as-is | — |
| 3 | Data Clumps | as-is | — |
| 4 | Primitive Obsession | as-is | — |
| 5 | Shotgun Surgery | as-is | — |
| 6 | Divergent Change | as-is | — |
| 7 | Message Chains | as-is | — |
| 8 | Refused Bequest | as-is | — |
| 9 | Duplicated Code | Duplicated Code | copy-pasted logic instead of extracted helper (`:102`) |
| 10 | Repeated Switches | Repeated Switches | repeated conditionals signal a missing model (`:82`, `:122`) |
| 11 | Shallow Module (Middle Man) | Middle Man | thin/identity wrappers, pass-through helpers (rule 4, `:99-100`); tell = the deletion test |
| 12 | Speculative Generality | Speculative Generality | "magic" generic mechanisms hiding simple shapes (`:53`, `:99`); tell = hypothetical seam |
| 13 | Spaghetti Growth | — | rule 2: ad-hoc conditionals, one-off booleans/nullable modes/flags bolted into unrelated or busy flows (`:40-44`, `:96-97`, `:103`, `:105`) |
| 14 | Muddy Type Boundary | — | rule 5: casts, `any`/`unknown`, unnecessary optionality, silent fallback over an unclear invariant (`:56-59`, `:101`) |
| 15 | Wrong Layer / Bespoke Duplicate | — | rule 6: feature logic in shared paths; near-duplicates of canonical helpers (`:61-64`, `:98`, `:106-107`) |
| 16 | Needless Sequencing / Non-Atomic Update | — | rule 7: independent work serialized; related updates leaving half-applied state (`:66-69`, `:108-109`) |
| 17 | File-Size Crossing *(script-owned)* | — | rule 1: the 1k gate (`:34-38`) — detected by `scripts/file_size_gate.py`, pre-seeded, sub-agent adds context only |

Not in the baseline, by design: nuclear rule 0 (judo) and rule 3 (clean-design bias) are reviewer posture — they live
in the Structure prompt template (phase 3), gated per durable decision 4. The "concepts a reader must hold" criterion
(`nuclear-review.md:94`) also goes to the template as the judo complexity test, not here.

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The baseline file

**File**: `skills/three-axis-review/references/structure-baseline.md`
**Change**: create the merged baseline implementing the mapping table.

```markdown
# Structure baseline

Two rules bind everything below. A documented repo standard always wins — where
it endorses something an entry would flag, suppress the entry. And every entry
is a labelled judgement call ("possible Feature Envy"), never a hard violation.

Each entry reads *tell* → *fix*; match it against the change:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal
  what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Feature Envy** — a method reaching into another object's data more than its
  own. → move the method onto the data it envies.
- …entries 3–10 in the same shape, per the mapping table…
- **Shallow Module (Middle Man)** — a wrapper or pass-through that fails the
  deletion test: delete it and no complexity reappears at its callers. → cut it,
  call the real target direct.
- **Speculative Generality** — abstraction, parameters, or hooks for needs the
  change doesn't have; one adapter means a hypothetical seam. → delete it;
  inline back until a real need shows.
- **Spaghetti Growth** — a new ad-hoc conditional, one-off boolean, nullable
  mode, or flag bolted into an unrelated or already busy flow. → reframe the
  state model or move the logic behind its own abstraction so the branch
  disappears.
- **Muddy Type Boundary** — casts, `any`/`unknown`, needless optionality, or a
  silent fallback papering over an unclear invariant; the interface is
  everything a caller must know. → make the boundary an explicit typed contract.
- **Wrong Layer / Bespoke Duplicate** — feature logic leaking into a shared
  path, or a near-duplicate of an existing canonical helper. → move the logic to
  the module that owns the concept; reuse the canonical helper.
- **Needless Sequencing / Non-Atomic Update** — independent work serialized for
  no reason, or related updates that can leave state half-applied. → parallelize
  what's independent; restructure related updates to land atomically.
- **File-Size Crossing** — a file pushed from ≤1,000 to >1,000 lines. Detected
  by the gate script and pre-seeded as `blocker (presumptive)`; do not
  re-derive it — add context only: is decomposition sensible, does the author
  justify the size. → split into focused modules before growing further.
```

## Success criteria

### Automated verification

- [ ] All 12 Fowler smell names survive the merge:
      `for s in "Mysterious Name" "Duplicated Code" "Feature Envy" "Data Clumps" "Primitive Obsession" "Repeated Switches" "Shotgun Surgery" "Divergent Change" "Speculative Generality" "Message Chains" "Middle Man" "Refused Bequest"; do grep -q "$s" skills/three-axis-review/references/structure-baseline.md || echo "MISSING: $s"; done`
      prints nothing.
- [ ] All five nuclear-only entries present: same loop over "Spaghetti Growth" "Muddy Type Boundary" "Wrong Layer"
      "Needless Sequencing" "File-Size Crossing".
- [ ] No first person: `grep -inE '\b(i|we|our|let'"'"'s)\b' skills/three-axis-review/references/structure-baseline.md`
      finds nothing.
- [ ] No provenance leakage: `grep -inE 'fowler|nuclear|merged|refactoring, ch' skills/three-axis-review/references/structure-baseline.md`
      finds nothing.
- [ ] Size: `wc -l` ≤ 60.

### Manual verification

- [ ] The user reviews the file against the mapping table above: every row implemented, merged entries read as one
      coherent heuristic (not two glued clauses), and the `codebase-designing` terms are used exactly (deletion test,
      hypothetical seam, interface).

A phase with manual steps is a pause point: the orchestrator must wait for the user to confirm them before starting
the next phase.

## Dependencies

- **Depends on**: None
- **Blocks**: 3
