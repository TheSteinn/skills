---
name: to-plan
description: Turn a PRD or Decision Snapshot into a multi-phase implementation plan using tracer-bullet vertical slices. Produces a plan index and separate phase documents in ./.planning/. Use when user wants to create an implementation plan, break down a design into phases, or mentions "tracer bullets" or "plan".
---

# Plan from PRD or Snapshot

Break a PRD or Decision Snapshot into a phased implementation plan using vertical slices (tracer bullets). Output is a **plan index** plus one **phase document** per phase, all saved in `./.planning/`.

## Process

### 1. Gather source material

Identify what is available:

- **Decision Snapshot**: Look for `.planning/decisions-<feature>.md`. If it exists, it is the **authoritative source** for durable design contracts and architectural decisions.
- **PRD**: Check if a PRD is in the conversation or in `.planning/`. If it exists, it is the authoritative source for user stories, problem statement, and scope. If the PRD and Snapshot conflict on a durable decision, the Snapshot wins.
- **Conversation context**: If neither a PRD nor a Snapshot is available, source user stories and decisions from the current conversation.

If you have none of these, ask the user to provide a PRD, point you to a Snapshot, or describe the feature.

### 2. Explore the codebase

If you have not already explored the codebase, do so to understand the current architecture, existing patterns, and integration layers.

Delegate exploration to dedicated subagents in order to preserve your own context.

### 3. Identify durable architectural decisions

Before slicing, identify any high-level decisions that are unlikely to change throughout implementation. Extract these **primarily from the Decision Snapshot**, falling back to the PRD or conversation context only if no snapshot exists. Examples, where applicable:

- Route structures / URL patterns
- Database schema shape
- Key data models and interfaces
- Authentication / authorization approach
- Third-party service boundaries

These go in the plan index so every phase can reference them.

### 4. Draft vertical slices

Break the feature into **tracer bullet** phases. Each phase is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE end-to-end path through the relevant layers of the system (for example: data model, API, business logic, UI, background jobs, integrations, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Do NOT include specific file names, function names, or implementation details that are likely to change as later phases are built
- DO include durable decisions that are likely to remain stable across phases, such as route paths, schema shapes, data model names, interface boundaries, or external contracts, where applicable
</vertical-slice-rules>

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each phase show:

- **Title**: short descriptive name
- **User stories covered**: which user stories this addresses
- **Depends on**: which other phases (if any) must be completed first

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Should any phases be merged or split further?

Iterate until the user approves the breakdown.

### 6. Write the output files

Create `./.planning/` if it doesn't exist. Write **two types of file**:

#### 6a. Plan Index

Write a file named `PLAN-<feature>.md` using the template below. This file provides the overall sequencing, shared architectural decisions, and links to individual phase documents.

<plan-index-template>
# Plan: <Feature Name>

> Source PRD: <brief identifier or link, or "N/A — sourced from conversation and Snapshot">
> Source Snapshot: <link to decisions file, or "N/A">

## Architectural decisions

Durable decisions that apply across all phases. Extract these from the Decision Snapshot; do not paraphrase contracts:

<!-- Include only the sections that apply to this feature. -->
- **Routes**: ...
- **Schema**: ...
- **Key models**: ...
- **Interfaces / contracts**: ...

---

## Phase Index

| Phase | Title | Description | User Stories | Depends On | Document |
|-------|-------|------------|-------------|------------|----------|
| 1 | <title> | <brief end-to-end behavior> | <story refs> | — | [Phase 1](PHASE-<feature>-1-<slug>.md) |
| 2 | <title> | <brief end-to-end behavior> | <story refs> | Phase 1 | [Phase 2](PHASE-<feature>-2-<slug>.md) |
| N | <title> | <brief end-to-end behavior> | <story refs> | Phase N-1 | [Phase N](PHASE-<feature>-N-<slug>.md) |

</plan-index-template>

#### 6b. Phase Documents

For each phase in the index, write a **separate file** named `PHASE-<feature>-<N>-<slug>.md`. Each phase document must be **self-contained** — a subagent implementing this phase should need only this document and the plan index, not any other phase document.

<phase-document-template>
# Phase <N>: <Title>

> Source Plan: [PLAN-<feature>.md](PLAN-<feature>.md)
> Source Snapshot: <link to decisions file, if it exists>

## User stories

<list from PRD or conversation>

## Relevant Contracts

Embedded from the Decision Snapshot. Include **only** the contracts this phase touches. Reproduce them verbatim — do NOT paraphrase or summarize. If a contract in the Snapshot conflicts with the conversation context, the Snapshot wins.

```<language>
<Natural-form contract from Snapshot>
```

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies

- **Depends on**: Phase <N-1> (or "None" for Phase 1)
- **Blocks**: Phase <N+1> (or "None" for the last phase)
</phase-document-template>

**Contract embedding rules:**

- Embed only the contracts from the Snapshot that are **relevant to this phase**. If a phase touches the `User` model but not the `Order` model, only include the `User` contract.
- Contracts must be **byte-for-byte identical** to the Snapshot. Do not reformat, rename, or paraphrase.
- If a phase does not touch any contracts from the Snapshot, omit the Relevant Contracts section entirely.

### 7. Anti-Leak Validation

Before saving, review all files against the Decision Snapshot (if one exists):

- Does any phase assume a decision or contract shape that does not appear in the Snapshot?
- Does any phase contradict a contract in the Snapshot?
- Does the Architectural Decisions section contain any invalidated or rejected decision?
- Are any contracts in phase documents paraphrased rather than reproduced verbatim?

If you find a leak or contradiction, align the plan with the Snapshot.
