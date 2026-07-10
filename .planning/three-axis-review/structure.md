# Structure: three-axis-review

> Slicing approved by the user 2026-07-09; iterated same day: the sub-agent return contract is markdown-only —
> no JSON, no validator/parser, no custom tool — per the decision record's Amendment (2026-07-09). Sources of truth
> for /write-plan: `decisions-three-axis-review.md` (all §refs below, including the Amendment),
> `design-plan/phase-1-line-count-gate-script.md` (script sketch + fixture test),
> `design-plan/phase-2-structure-baseline.md` (the mapping table), `design-plan/phase-3-skill-drafting.md`
> (orchestrator protocol, frontmatter, style constraints, README change). Superseded by this file: the design-plan
> index's three-phase split, and phase-3's inline-template layout and single-phase packaging.

## File layout

```
skills/three-axis-review/
├── SKILL.md                       # orchestrator protocol only          (slice 6)
├── scripts/
│   └── file_size_gate.py          # deterministic 1k-line gate          (slice 1)
└── references/
    ├── structure-baseline.md      # merged what→fix baseline            (slice 2)
    ├── return-contract.md         # shared return format + sentinels    (slice 3)
    ├── structure-prompt.md        # Structure sub-agent template        (slice 3)
    ├── spec-prompt.md             # Spec sub-agent template             (slice 4)
    └── standards-prompt.md        # Standards sub-agent template        (slice 5)
```

Templates are three separate reference files (user decision, supersedes phase-3's inline sketch): per axis, the
orchestrator reads that axis's prompt file, fills the placeholders, and changes nothing else (§10). The return
contract is single-sourced in `return-contract.md` and delivered inline: the orchestrator pastes it into each
template's `{RETURN_CONTRACT}` placeholder at fill time — sub-agents are never asked to look it up by path
(Amendment).

## Slices

### 1. Gate script reports size crossings

`python3 skills/three-axis-review/scripts/file_size_gate.py <fixed-point>` prints one TSV line per file the branch
pushes past 1,000 lines, per the contract in Contracts §A (phase-1's contract plus edge rules).
**Checkpoint**: the phase-1 fixture-repo shell test — a scratch repo in `$TMPDIR` covering grows / already-big /
deleted / renamed / brand-new / binary; assert exact sorted TSV and exit codes 0/2. Seam: the script's CLI — a process
boundary needing no skill around it. **Depends on**: —

### 2. Structure baseline stands alone

`references/structure-baseline.md` holds the 17-entry merged baseline per phase-2's mapping table, written in
`codebase-designing` vocabulary, precedence rule at the top, ≤60 lines.
**Checkpoint**: phase-2's completeness greps (12 Fowler names + 5 nuclear-only entries present; no first person; no
provenance) plus user content review against the mapping table — merged entries read as one heuristic, not two glued
clauses. Seam: the file is the Structure sub-agent's whole heuristic input. **Depends on**: —

### 3. Structure template reviews a real diff standalone

Delivers `references/return-contract.md` (the ~10-line shared return format, Contracts §B) and
`references/structure-prompt.md` — the verbatim Structure template: baseline read-first (§9), explicit Skill-tool
invocation of `codebase-designing` (§5), pre-seeded crossings contextualised never re-derived (§6), judo gated on
sketch + behaviour-preservation + complexity argument, always `suggestion` (§4), read scope per §13, few
high-conviction findings over nit floods.
**Checkpoint**: standalone harness — hand-fill `{DIFF_CMD}` `{COMMIT_LIST}` `{RETURN_CONTRACT}` `{BASELINE_PATH}`
`{PRESEEDED_FINDINGS}`, spawn one `general-purpose` agent on a real branch, and check the return against the
acceptance checklist (Contracts §C): schema-shaped bullets with cite lines, blockers listed first, preseeds back
contextualised with labels intact; a clean-diff run returns exactly `NO FINDINGS: <one line>`. Seam: the
template⇄return contract, proven with no orchestrator. User deep-reads the template against §4/§5/§13.
**Depends on**: 1 (real TSV to pre-seed), 2 (baseline to read)

### 4. Spec template judges a diff against a spec standalone

`references/spec-prompt.md`: missing/partial requirements, scope creep, implemented-but-wrong; every finding's cite
quotes the spec line.
**Checkpoint**: same harness, run twice to prove both handover modes (§14) — `{SPEC_SOURCE}` as a repo path with
read-first instruction, then as pasted content; this repo's `.planning/` dirs are real spec fixtures. Both returns
pass the acceptance checklist. **Depends on**: 3 (return contract)

### 5. Standards template discovers rules and judges standalone

`references/standards-prompt.md`: delegate discovery over the fixed candidate set (§8) to a nested haiku explorer,
read what it finds, judge the diff against documented rules only; tooling filter grounded by
`{LINT_CONFIG_FILENAMES}`.
**Checkpoint**: same harness on this repo (CLAUDE.md exists → rule-cited findings or exactly `NO FINDINGS: <one
line>`) and on a bare fixture repo (→ exactly `SKIPPED: no documented standards`). This isolates the riskiest novel
mechanism — the nested delegation — before any orchestrator exists. **Depends on**: 3 (return contract)

### 6. `/three-axis-review` runs end-to-end

`SKILL.md` (five numbered steps per phase-3: pin/gate → spec chain (§7) → one-message three-Agent fan-out reading and
filling the three prompt files → verify returns against the acceptance checklist (§11 + Contracts §C) → aggregate by
concatenation (§3 + Contracts §E)) plus the README pipeline entry (§12). Frontmatter and style constraints per
phase-3; target ≤120 lines now that templates and contract are external.
**Checkpoint**: `quick_validate.py`, phase-3's greps (frontmatter flag, referenced paths exist, no first person, no
dead concepts), then a wiring-only dry-run on a real branch: gate fires on a bad ref, spec chain asks/confirms, three
parallel sub-agents, three-section blockers-first report with per-axis summary. Slices 3–5 already proved the
contract and templates, so this dry-run tests orchestration only. **Depends on**: 1–5

Slices 1–2 land first in the user's priority order; 4 and 5 are independent of each other (both depend on 3 only for
the return-contract file).

## Contracts (binding signatures — the plan implements these verbatim)

### A. Gate script CLI (extends phase-1's contract; phase-1 stays binding for everything not listed)

- Diff enumeration: `git diff --name-status -M -z <merge-base> HEAD`. Statuses: `A` → (None, path); `M` → (path,
  path); `D` → skip; `R<n>` → (old, new); any other status (`T`, …) → treat as `M` at the after path. No `-C`:
  copies surface as adds.
- Binary = blob contains a NUL byte → skip the file. Line count = count of `b"\n"`, +1 if the file is non-empty and
  lacks a trailing newline.
- Any git failure (unresolvable ref, no merge-base, not a repo) → reason on stderr, exit 2.

### B. Return contract (`references/return-contract.md`; pasted into every template via `{RETURN_CONTRACT}`)

The shared file states, once: the finding schema, the exact sentinels, the label rule, and the ordering duty.

```
- `blocker (presumptive)` | `suggestion` — `path:line` — <one-sentence finding>
  cite: <axis-specific citation with a short quote>
  <free-form detail; any code in fenced blocks; no length cap>
```

- Label rule: `blocker (presumptive)` only on an objective trigger or documented-rule breach; otherwise
  `suggestion`; when unsure, `suggestion` (§3).
- Ordering duty: the sub-agent lists blockers before suggestions, so aggregation never reorders.
- Sentinels, exact strings, each the entire return: `NO FINDINGS: <one line — what was reviewed>` for a clean axis;
  `SKIPPED: <reason>` for Standards with no discovered sources.
- Cite content per axis — Spec: quoted spec line; Standards: rule file + quoted hunk; Structure: baseline entry name
  + quoted hunk — stated in each template, not in the shared contract file.

### C. Acceptance checklist and failure handling (operationalises §11; lives in SKILL.md's verify step)

- Accept a return iff it is exactly one sentinel line, OR it contains ≥1 finding bullet matching the §B shape with a
  cite line.
- Anything else — empty return, prose without schema-shaped bullets, findings without cites → failure → rerun once,
  naming the defect in the rerun prompt → second failure → axis rendered `not reviewed`. `not reviewed` is
  orchestrator-side only; sub-agents never emit it.
- Spec with no discovered source is never spawned — the orchestrator marks the axis `skipped` itself (§7 route ④
  exhausted). Standards skips via its sentinel. Structure never skips.
- Gate fallback: if Structure ends `not reviewed`, the orchestrator itself renders the pre-seeded crossings as §B
  findings under `## Structure` — script findings cannot be lost to a dead axis.

### D. Placeholder sets (exact; nothing else is fillable)

- Common to all three: `{DIFF_CMD}` — the literal `git diff <fixed-point>...HEAD` string; the sub-agent runs it
  itself as its first step. `{COMMIT_LIST}` — pasted output of `git log <fixed-point>..HEAD --oneline`.
  `{RETURN_CONTRACT}` — the pasted contents of `references/return-contract.md`, placed at the end of each template.
- `spec-prompt.md`: + `{SPEC_SOURCE}` — either `Read this spec file first: <path>` or pasted tracker content (§14).
- `standards-prompt.md`: + `{LINT_CONFIG_FILENAMES}` — orchestrator-detected config filenames grounding the tooling
  filter; filled `none detected` when empty. The nested haiku-explorer prompt is static text inside the template —
  fixed candidate set, no placeholders; the explorer returns found paths only, the Standards agent reads them itself.
- `structure-prompt.md`: + `{BASELINE_PATH}` — absolute path, read-first; `{PRESEEDED_FINDINGS}` — the gate TSV
  verbatim, or `none`.

### E. Aggregation (pure combination — no transformation step exists)

The aggregated report is the orchestrator's final message; no file is written. Under each of `## Spec`,
`## Standards`, `## Structure`: the axis's findings verbatim (already blockers-first per §B), or its sentinel/state
(`skipped` / `not reviewed`) — labels never re-derived, findings never merged or reranked across axes (§3). Each
axis closes with a composed one-line summary: finding count (= bullet count) and the top blocker, if any. Future
trigger (Amendment): if a machine consumer ever appears (e.g. posting findings as PR comments), revisit a structured
return channel then — not before.
