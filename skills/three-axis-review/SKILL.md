---
name: three-axis-review
description: Review the diff since a fixed point along three orthogonal axes — Spec (does it do the right thing), Standards (does it follow documented repo rules), Structure (is it well built) — as parallel sub-agents reporting labelled findings, never a verdict. Use when the user wants to review a branch, review since a given ref, or asks for a three-axis review.
disable-model-invocation: true
---

# Three-Axis Review

Review the diff between a user-pinned fixed point and `HEAD` along three orthogonal axes, one parallel sub-agent each:

- **Spec** — does the change do what the spec asks?
- **Standards** — does the change follow the repo's documented rules?
- **Structure** — is the change well built?

Findings are labelled `blocker (presumptive)` or `suggestion`, blockers first within an axis, and there is no overall
verdict.

The harness supplies this skill's base directory at invocation. Every skill file named below lives under it, and
absolute paths — including the one that fills `{BASELINE_PATH}` — derive from it.

## 1. Pin and gate

The fixed point comes from the user; if the invocation names none, ask. Then, before any fan-out:

- Verify `git rev-parse <fixed-point>` resolves and `git diff <fixed-point>...HEAD` is non-empty — a bad ref or an
  empty diff fails here, not inside three sub-agents.
- Capture the literal string `git diff <fixed-point>...HEAD` (fills `{DIFF_CMD}`) and the output of
  `git log <fixed-point>..HEAD --oneline` (fills `{COMMIT_LIST}`).
- Run `python3 <base-dir>/scripts/file_size_gate.py <fixed-point>`. Exit 2 → stop and report the reason from
  stderr. Its TSV output — one `path<TAB>before<TAB>after` line per file the branch pushes past 1,000 lines —
  pre-seeds Structure findings labelled `blocker (presumptive)` and fills `{PRESEEDED_FINDINGS}` verbatim, `none`
  when empty.
- Detect lint/format config filenames at the repo root (e.g. `.editorconfig`, `.eslintrc*`, `.prettierrc*`,
  `ruff.toml`, ktlint/detekt configs); the detected names fill `{LINT_CONFIG_FILENAMES}`, `none detected` when
  empty.

## 2. Find the spec

Take the first route that yields a spec:

1. A spec path passed by the user — the only route needing no confirmation.
2. A `.planning/<slug>/` directory matching the branch or feature — preferring `plan/index.md` plus its phase
   files, then `structure.md`, then `design.md` — best match confirmed with the user.
3. Ticket keys in the commit messages, fetched through a forge CLI inferred from session context (CLAUDE.md /
   AGENTS.md instructions, loaded skills): definitive proof the CLI is in use → use it, otherwise ask; confirm
   inferred ticket matches with the user. Never install a missing CLI — ask the user instead.
4. Ask the user.

Nothing found → mark the Spec axis `skipped`; its sub-agent is never spawned. The handover fills `{SPEC_SOURCE}`:
a spec that is a repo file passes as `Read this spec file first: <path>`; tracker-fetched content is pasted in
full.

## 3. Fan out

Read each running axis's template under `references/` — `spec-prompt.md`, `standards-prompt.md`,
`structure-prompt.md` — fill exactly the placeholder set its header names, and change nothing else.
`{RETURN_CONTRACT}` is the pasted contents of `references/return-contract.md`; `{BASELINE_PATH}` is the absolute
path of `references/structure-baseline.md`.

Spawn all sub-agents in one message — three parallel Agent calls of type `general-purpose`, or two when Spec is
skipped.

## 4. Verify returns

Hard checks per axis — any failure triggers a repair-rerun:

- **Usability floor** (every axis): the return is non-empty and contains a sentinel or at least one bullet
  starting with a legal label.
- **Paths in diff** (Structure and Standards only): every finding's `path` appears in
  `git diff --name-only <fixed-point>...HEAD`.
- **Pre-seed preservation** (Structure only): every gate TSV path reappears in a `blocker (presumptive)` finding.
- **Illegal skip**: `SKIPPED:` from Spec or Structure — only Standards may emit it.

The repair-rerun prompt is the original filled prompt + the previous return verbatim + the explicit defect list +
the instruction "Repair the listed defects. Keep every finding whose substance is sound. Do not re-review from
scratch." — except a floor failure, which has nothing to repair: rerun the original prompt as-is. A second
failure renders the axis `not reviewed` — an orchestrator-side state, distinct from `skipped`; sub-agents never
emit it.

Advisory — pasted through with a one-line orchestrator note under the axis, never a rerun: a Spec finding path
absent from both the diff and the repo (legitimate for missing-requirement findings), unknown labels, and format
noise (preamble, headers, closing commentary, first person).

Gate fallback: if Structure ends `not reviewed`, render the pre-seeded TSV crossings as return-contract findings
under `## Structure` directly — script findings cannot be lost to a dead axis.

## 5. Aggregate

The report is the final message; no file is written. Under each of `## Spec`, `## Standards`, `## Structure`: the
axis's findings verbatim (already blockers-first per the return contract), or its sentinel / state (`skipped`,
`not reviewed`) — labels never re-derived, findings never merged or reranked across axes. Close each axis with a
composed one-line summary: the finding count (= bullet count) and the top blocker, if any.

## Why three axes

A change can pass one axis and fail another. Reporting the axes separately stops one axis from masking another.
That separation is why findings are never reranked across axes.
