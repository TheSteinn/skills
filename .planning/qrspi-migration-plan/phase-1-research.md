# Phase 1: `/research` (Question + Research)

> Source: [index.md](index.md) · structure slice 1. Self-contained: implement from this file +
> the index only.

## Overview

Create the pipeline's first skill: one invocation that captures the task, decomposes it into
neutral research questions (QRSPI's Question phase), then answers them via **task-blind
subagents** (QRSPI's Research phase). Establishes the `.planning/<slug>/` artifact convention
every later phase consumes. Deviations embodied here (recorded in `docs/research.md`): Q+R
merged into one invocation; firewall implemented as blind subagents rather than a fresh
top-level window; synthesis also kept blind.

## Changes required

### 1. Create `skills/research/SKILL.md`

Target sketch — a floor, not the finished file (index: "sketches are floors"): flesh out into
a polished skill; structure, gates, and voice are fixed.

```markdown
---
name: research
description: QRSPI step 1 — decompose a task into neutral research questions, then answer them with task-blind subagents. Produces task.md, questions.md, and research.md (facts with file:line citations, no recommendations) in .planning/<feature>/.
disable-model-invocation: true
---

# Research (Question + Research)

Turn a task into neutral research questions, then answer them with subagents that never see the
task. You are the query planner: you may read the task, but only questions travel downstream.

## 1. Capture the task

The task comes from the user's invocation — a description, ticket text, or file path. If
nothing was given, ask the user for it. Read any referenced files fully.

Derive a short kebab-case feature slug, create `.planning/<slug>/`, and write `task.md`: the
task as given (verbatim where possible) plus its source (link, ticket, or "conversation").

## 2. Decompose into neutral questions

Write `questions.md`: the research questions whose answers would let a stranger design this
feature. Good questions send a researcher into every part of the codebase that matters — "how
do X endpoints work end to end?", "trace everything that touches Y", "what patterns exist for
Z?".

Neutrality is the contract: a question must not reveal or imply the intended change. Test each
one — could a reader reconstruct the task from it? If yes, rewrite it. ("How should we add
multi-tenant support?" fails; "how is tenancy currently modelled, and where is it enforced?"
passes.)

Present the questions to the user and ask whether to adjust or proceed — one confirmation,
then move on.

## 3. Research with blind subagents

Spawn parallel general-purpose subagents to answer the questions, building every prompt from
[references/subagent-prompts.md](references/subagent-prompts.md). Prompts contain question
text, repo location, and output instructions — nothing else. Never put task content, the
intended change, or conversation context into a subagent prompt: the subagents' blindness is
the firewall that keeps research factual.

Fan out along the reference's three axes: locators (WHERE things live), analyzers (HOW they
work), pattern-finders (EXAMPLES to follow). Findings must carry file:line citations and
describe what IS — researchers are documentarians, not critics.

Each subagent writes its findings to `.planning/<slug>/research-notes/<topic>.md`.

## 4. Blind synthesis

Spawn one more subagent — prompt again from the reference, again without the task — that reads
`questions.md` and the notes and writes `research.md` per the reference's template: provenance
frontmatter (date, git commit, branch), summary, findings organised by question with citations,
and unanswered questions. Target ~300 lines. Delete `research-notes/` after synthesis.

## 5. Hand off

Spot-check a few citations against the live code; fix any that don't resolve by re-running the
relevant subagent (never by editing findings from your own knowledge — your window knows the
task). Then ask the user to skim `research.md` for factual misses, and point at `/design` as
the next step — best run in a fresh session (`/clear`).
```

### 2. Create `skills/research/references/subagent-prompts.md`

Contains four prompt templates and the research.md template. Required content (write prose
around these skeletons; every template ends with "Return findings with file:line citations.
Document what IS, not what should be. No recommendations, no critique."):

- **Locator** — "In the repository at <path>, find WHERE the following lives: <question>. Report
  file paths grouped by role (entry points, config, tests, docs). Write your findings to
  <notes-path>."
- **Analyzer** — "In the repository at <path>, explain HOW the following works: <question>.
  Trace the flow end to end; cite every claim as file:line. Read files fully before concluding.
  Write your findings to <notes-path>."
- **Pattern-finder** — "In the repository at <path>, find existing EXAMPLES relevant to:
  <question>. For each, show the pattern with file:line and what it is an example of. Write
  your findings to <notes-path>."
- **Synthesizer** — "Read <slug>/questions.md and every file in <slug>/research-notes/. Write
  <slug>/research.md using the template below. You are organising verified findings — do not
  add conclusions of your own, do not speculate about purpose. Preserve citations exactly."
- **research.md template** — YAML frontmatter (`date`, `git_commit`, `branch`, `questions:
  questions.md`), then `## Summary`, `## Q1: <question>` (findings + citations) per question,
  `## Unanswered questions`.

The templates have **no slot for task content** — that absence is the firewall (index decision
3); a comment at the top of the reference must say exactly that, so future editors don't add
one.

### 3. Create `docs/research.md` (deviation record)

Follow the tone/format of `docs/grill-me.md`. Must cover, with reasons: (a) Question and
Research are one invocation because QRSPI's question-review gate is optional — the pause is
offered, not gated; (b) the firewall maps to blind subagents because Claude Code skills run in
the main conversation, which has seen the task — the main window is QRSPI's query planner,
subagents its blind executors; (c) synthesis is also a blind subagent because V1's failure was
decomposition *and synthesis* living in the contaminated window; (d) source: QRSPI (Dex
Horthy/HumanLayer), link the blog `alexlavaee.me/blog/from-rpi-to-qrspi/`.

### 4. Edit `README.md`

Insert a new `### QRSPI pipeline` subsection at the top of the `## Skills` section (before
`### Planning`), with an intro sentence ("A port of Dex Horthy's QRSPI workflow — each phase a
separate small invocation, reviewed by the human at the cheap artifacts") and a `#### /research`
entry describing the skill in the README's existing voice. Do not touch other entries yet.

## Success criteria

### Automated verification

- [x] `test -f skills/research/SKILL.md && test -f skills/research/references/subagent-prompts.md`
- [x] `grep -q 'disable-model-invocation: true' skills/research/SKILL.md`
- [x] `grep -qi 'no slot for task content' skills/research/references/subagent-prompts.md` (or
      equivalent firewall comment)
- [x] `grep -q '/research' README.md`
- [x] `test -f docs/research.md`
- [x] `! grep -rn 'EnterWorktree\|to-prd\|orchestrate' skills/research/` (no scope leakage)

### Manual verification

- [ ] Instruction count of SKILL.md body < 40 (count imperatives; templates excluded).
- [ ] Run `/research` on the standard micro-task (index: `--dry-run` flag for install.sh).
      Inspect: `questions.md` questions pass the reconstruct-the-task test; every spawned
      subagent prompt contains no task text (check the transcripts); `research.md` has zero
      recommendations and its citations resolve.

## What this phase is NOT doing

No `/design` handoff logic beyond the closing pointer; no changes to any existing skill; no
ticket-system integration (task arrives via invocation text/file only).

## Dependencies

None — first slice. Establishes the artifact contract for phases 2–6.
