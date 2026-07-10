# Phase 2: Structure baseline stands alone

> Source: [index.md](index.md). Self-contained: implement from this file + the index only.

## Overview

Deliver `skills/three-axis-review/references/structure-baseline.md`: the single deduplicated what→fix baseline the
Structure sub-agent reads by path (decisions 2, 5, 9). The mapping — which Fowler smells collapse into which
nuclear concerns — is this phase's binding decision and the intellectual core of the merge; the user reviews the
file as content, independent of any skill prose.

## Context

**Sources being merged** (restated here in full — `.planning/review/` may not survive later housekeeping):

The 12 Fowler smells, each *what it is* → *how to fix*, verbatim from `.planning/review/two-axes-review.md:45-56`:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it;
  if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the
  shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the
  data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle
  them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. →
  give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with
  polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what
  changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes
  for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete
  it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one
  method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the
  inheritance, use composition.

Nuclear's concerns being merged in, from `.planning/review/nuclear-review.md:23-69` (rules 0–7; rule 3 is posture,
not a smell): the 1k-line file (rule 1, `:34-38`); spaghetti/ad-hoc branching — "new ad-hoc conditionals, scattered
special cases, or one-off branches inserted into unrelated flows", one-off booleans/nullable modes/flags in busy
flows (rule 2, `:40-44`, `:96-97`, `:103`, `:105`); thin wrappers/magic — "thin abstractions, identity wrappers, or
pass-through helpers that add indirection without buying clarity", generic mechanisms hiding simple data-shape
assumptions (rule 4, `:53`, `:99-100`); type/boundary cleanliness — unnecessary optionality, `unknown`/`any`,
cast-heavy code, silent fallback papering over an unclear invariant (rule 5, `:56-59`, `:101`); canonical
layer/helper reuse — feature logic leaking into shared paths, bespoke near-duplicates of canonical helpers (rule 6,
`:61-64`, `:98`, `:106-107`); orchestration/atomicity — independent work serialized for no reason, related updates
leaving state half-applied (rule 7, `:66-69`, `:108-109`); copy-pasted logic instead of extracted helpers (`:102`);
repeated conditionals signalling a missing model (`:82`, `:122`).

**`codebase-designing` vocabulary to write entries in** (decision 5): the deletion test — "Imagine deleting the
module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its
keep" (`skills/codebase-designing/SKILL.md:85-86`); the hypothetical seam — "One adapter means a hypothetical seam.
Two adapters means a real one" (`:89`); the interface includes every fact a caller must know (`:21-23`); complexity
as dependencies + obscurity, judged by the information a developer must hold in their head (`:46-48`, `:91-93`).

**The precedence rule travels with the baseline** (decision 2): a documented repo standard always wins; where it
endorses something the baseline would flag, suppress the entry. Every entry is a labelled judgement call, never a
hard violation.

**Format rules**:

- Uniform schema per entry: **Name** — *tell* (one clause) → *fix* (one clause). Scannable, no sub-bullets.
- Instructions only — no provenance, no history, no "merged from" notes in the file (repo memory: no history in
  skill content). Provenance lives in the mapping table below and nowhere else.
- No first person anywhere. Target ≤ 60 lines total.
- Merged entries must read as one coherent heuristic, not two glued clauses.

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

Not in the baseline, by design: nuclear rule 0 (judo) and rule 3 (clean-design bias) are reviewer posture — they
live in the Structure prompt template (phase 3), gated per decision 4. The "concepts a reader must hold" criterion
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

- [x] All 12 Fowler smell names survive the merge:
      `for s in "Mysterious Name" "Duplicated Code" "Feature Envy" "Data Clumps" "Primitive Obsession" "Repeated Switches" "Shotgun Surgery" "Divergent Change" "Speculative Generality" "Message Chains" "Middle Man" "Refused Bequest"; do grep -q "$s" skills/three-axis-review/references/structure-baseline.md || echo "MISSING: $s"; done`
      prints nothing.
- [x] All five nuclear-only entries present: same loop over "Spaghetti Growth" "Muddy Type Boundary" "Wrong Layer"
      "Needless Sequencing" "File-Size Crossing" prints nothing.
- [x] No first person:
      `grep -inE '\b(i|we|our|let'"'"'s)\b' skills/three-axis-review/references/structure-baseline.md`
      finds nothing.
- [x] No provenance leakage:
      `grep -inE 'fowler|nuclear|merged|refactoring, ch' skills/three-axis-review/references/structure-baseline.md`
      finds nothing.
- [x] Size: `wc -l < skills/three-axis-review/references/structure-baseline.md` ≤ 60.

### Manual verification

- [x] The user reviews the file against the mapping table above: every row implemented, merged entries read as one
      coherent heuristic (not two glued clauses), and the `codebase-designing` terms are used exactly (deletion
      test, hypothetical seam, interface). *(Confirmed by the user 2026-07-10.)*

A phase with manual steps is a pause point: the orchestrator must wait for the user to confirm them before starting
the next phase.

## Dependencies

- **Depends on**: None
- **Blocks**: 3, 6
