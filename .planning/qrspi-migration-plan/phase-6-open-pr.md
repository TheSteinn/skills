# Phase 6: `/open-pr` + coherence pass

> Source: [index.md](index.md) · structure slice 6. Self-contained: implement from this file +
> the index only.

## Overview

Land the delivery phase — a PR grounded in `design.md`, so the reviewer confirms decisions they
already approved instead of discovering them — then make the whole repo coherent: full README
narrative rewrite, deviation-record index, sweep for dangling references, install smoke test.
This phase replaces V1's self-grading `validate_plan` with QRSPI's answer: the human reads the
code, and the PR is built to make that fast.

## Changes required

### 1. Create `skills/open-pr/SKILL.md`

Target sketch — a floor, not the finished file (index: "sketches are floors"): flesh out into
a polished skill; structure, gates, and voice are fixed.

```markdown
---
name: open-pr
description: QRSPI step 6 — open a pull request grounded in the design doc, putting the "why" beside the diff. Ends with the one non-negotiable - the human reads the code.
disable-model-invocation: true
---

# Open PR

Deliver the work as a pull request whose description is grounded in `design.md`, so the
reviewer confirms decisions they already approved instead of discovering them in the diff.

## 1. Load

Locate `.planning/<slug>/` (take the slug from the invocation; if none was given and exactly
one directory exists, use it; otherwise ask the user). Read the alignment artifacts that exist
— `design.md` when the design phase ran, otherwise `plan/index.md` and `task.md` — plus the
full diff against the base branch (`git diff <base>...HEAD`) and the phase commits (`git log`).

## 2. Write the description

- **Why** — the problem and desired end state, in the design's own terms when it exists
  (referencing the sections they come from), otherwise from the plan index and task.
- **What changed** — one entry per plan phase/commit, stated as observable behaviour.
- **Decisions exercised** — the resolved decisions this diff embodies; call out any deviation
  implementation surfaced, with its rationale.
- **Verification** — the automated criteria that passed, and the manual steps a reviewer can
  rerun.

## 3. Open it

Use whatever forge CLI is available and already authenticated (`gh`, `bkt`, …). Confirm the
title, description, and target branch with the user before pushing or creating anything —
this is the outward-facing step. If no forge CLI is available, output the title and
description for the user to paste, say which tool was missing, and stop — never install one.

## 4. The gate

Close with the reminder the whole pipeline priced everything toward: the alignment artifacts
that were produced were the cheap reviews; the code is the one that matters — **now read the
code. No exceptions.**
```

### 2. Create `docs/open-pr.md` (deviation record)

Must cover, with reasons: (a) the PR phase replaces V1's `validate_plan` self-grading — a model
cannot certify its own completion, so the human sits at the one gate that matters; (b) the
description is grounded in `design.md` so review is confirmation, not discovery; (c)
forge-agnostic with confirm-before-push — outward-facing actions need explicit consent, and
missing tools are reported, never installed.

### 3. Rewrite `README.md` (full narrative pass)

Target shape (keep the repo's existing voice; Credits and Installation sections survive with
edits noted):

1. **Intro** — replace the current pipeline paragraph: the heart of the repo is now the QRSPI
   pipeline (Question → Research → Design → Structure → Plan → Implement → PR as six
   invocations), humans deep-review the design, the structure, and the code — never the long
   plan. One sentence on artifacts living in `.planning/<feature>/`.
2. **Credits** — add Dex Horthy / HumanLayer as the origin of the QRSPI workflow (link
   `alexlavaee.me/blog/from-rpi-to-qrspi/`), alongside the existing Pocock/Anthropic/v1r3n
   credits; keep the "deliberate divergence lives in docs/" sentence and extend it to name the
   six pipeline deviation records.
3. **Skills sections** — `### QRSPI pipeline` first (`/research`, `/design`, `/structure`,
   `/write-plan`, `/implement`, `/open-pr`, each with its accumulated entry from phases 1–5
   polished into one voice, plus a short "a typical run" walkthrough naming the artifacts and
   the recommended `/clear` between phases and the user-prepared branch before `/implement`);
   then `### Standalone` (grill-me, grill-with-docs, improve-codebase-design, initialise-docs,
   tdd, code-doc, dg) and `### Utilities` (acli, skill-creator) — regrouping is free, removing
   entries for still-existing skills is not.
4. Remove every remaining mention of the retired pipeline (Decision Snapshot → PRD → plan →
   orchestrate flow) except historical notes in Credits.

### 4. Coherence sweep

- `grep -rn 'to-prd\|to-plan\|orchestrate-plan' skills/ docs/ README.md install.sh` — the only
  acceptable hits are historical mentions in Credits and the `docs/` deviation records
  explaining the retirements. Fix anything else.
- `grep -rn 'PRD\|Decision Snapshot' skills/` — acceptable only in `grilling` (standalone
  Snapshot path) and skills that legitimately reference standalone grills; fix anything that
  implies the retired pipeline.
- Run `./install.sh` into a scratch `$HOME` (`HOME=$(mktemp -d) ./install.sh` — the script
  derives its destination from `$HOME`) and confirm the installed set is exactly the intended
  skills: six pipeline skills present; `to-prd`, `to-plan`, `orchestrate-plan` absent.

## Success criteria

### Automated verification

- [ ] `test -f skills/open-pr/SKILL.md && test -f docs/open-pr.md`
- [ ] `grep -q 'disable-model-invocation: true' skills/open-pr/SKILL.md`
- [ ] `grep -q 'QRSPI' README.md && grep -q 'HumanLayer' README.md`
- [ ] Sweep greps above return only the documented acceptable hits.
- [ ] Scratch-home install lists `research design structure write-plan implement open-pr` and
      none of the three retired skills.

### Manual verification

- [ ] Instruction count of SKILL.md body < 40.
- [ ] Dogfood on the micro-task branch from phase 5: `/open-pr` drafts a description whose
      Why/Decisions sections cite `design.md` content, and asks for confirmation before any
      push — stop at the confirmation (do not actually open a PR for the micro-task unless the
      human wants it).
- [ ] Read the README top to bottom as a newcomer: the pipeline story is complete, every named
      skill exists, every link resolves.

## What this phase is NOT doing

No forced forge choice (gh/bkt both acceptable; absence handled by outputting the description);
no CI; no changes to `install.sh`; no cleanup decision on `.planning/install-dry-run/` without
asking the human.

## Dependencies

Phase 5 (consumes the micro-task's implemented branch for dogfooding; textually depends on all
prior phases' README entries).
