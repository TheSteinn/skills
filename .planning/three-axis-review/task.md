# Task: build the three-axis-review skill

Build `skills/three-axis-review/` — a code-review skill with three orthogonal axes (Spec, Standards, Structure) run as
parallel sub-agents, combining the nuclear review's heuristics with the two-axes review's deterministic macro shape.

All design decisions are resolved in [.planning/decisions-three-axis-review.md](decisions-three-axis-review.md)
(grill record, 2026-07-07). Source material and adversarial findings live in `.planning/review/`.

Priority order set by the user:

1. The line-count rule script (`scripts/file_size_gate.py`).
2. The dedup mapping — which Fowler smells collapse into which nuclear concerns — decided in
   `references/structure-baseline.md`.
3. Skill drafting (`SKILL.md` + README wiring).
