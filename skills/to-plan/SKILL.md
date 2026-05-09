---
name: to-plan
description: Turn a PRD or Decision Snapshot into a multi-phase implementation plan using tracer-bullet vertical slices. Produces a plan index and separate phase documents in ./.planning/. Use when user wants to create an implementation plan, break down a design into phases, or mentions "tracer bullets" or "plan".
---

# Plan from PRD or Snapshot

Break a PRD or Decision Snapshot into a phased implementation plan using vertical slices (tracer bullets). Output is a *
*plan index** (like a Jira Epic — describing the overall objective and very durable architecture decisions) plus one *
*phase document** per phase, all saved in `./.planning/`.

## Process

### 1. Gather source material

Identify what is available:

- **Decision Snapshot**: Look for `.planning/decisions-<feature>.md`. If it exists, it is a **historical record of the
  brainstorming session** — useful context, but not an authoritative contract. The PRD and Plan documents are the source
  of truth during implementation.
- **PRD**: Check if a PRD is in the conversation or in `.planning/`. If it exists, it is the authoritative source for
  user stories, problem statement, scope, and implementation decisions.
- **Conversation context**: If neither a PRD nor a Snapshot is available, source user stories and decisions from the
  current conversation.

If you have none of these, ask the user to provide a PRD, point you to a Snapshot, or describe the feature.

### 2. Explore the codebase

If you have not already explored the codebase, do so to understand the current architecture, existing patterns, and
integration layers.

Delegate exploration to dedicated subagents in order to preserve your own context.

### 3. Identify durable architectural decisions

Before slicing, identify any high-level decisions that are genuinely unlikely to change throughout implementation. These
are the rare, bedrock decisions — like "we're using PostgreSQL" or "the API follows REST conventions" — not
implementation details like class shapes or method signatures. Extract these primarily from the PRD, falling back to the
Decision Snapshot only as supplementary context.

These go in the plan index so every phase can reference them.

**What counts as durable:** Technology choices, architectural patterns, authentication approach, major integration
boundaries. **What does NOT count as durable:** Interface shapes, class contracts, method signatures, specific file
paths, schema field names — these are implementation details that may change as phases are built out.

### 4. Draft vertical slices

Break the feature into **tracer bullet** phases. Each phase is a thin vertical slice that cuts through ALL integration
layers end-to-end, NOT a horizontal slice of one layer.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE end-to-end path through the relevant layers of the system (for example: data model, API, business logic, UI, background jobs, integrations, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Do NOT include specific file names, function names, or implementation details that are likely to change as later phases are built
- DO include genuinely durable architectural decisions that apply across phases (technology choices, patterns, integration boundaries), but describe them in natural language — not as code contracts
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

Write a file named `PLAN-<feature>.md` using the template below. This file provides the overall sequencing, shared
architectural decisions, and links to individual phase documents.

<plan-index-template>
# Plan: <Feature Name>

> Source PRD: <brief identifier or link, or "N/A — sourced from conversation and Snapshot">

## Architectural decisions

Genuinely durable decisions that apply across all phases. These are bedrock choices like technology stack or
authentication approach — not implementation details like class shapes or method signatures. Describe in natural
language.

---

## Phase Index

| Phase | Title   | Description                 | User Stories | Depends On | Document                               |
|-------|---------|-----------------------------|--------------|------------|----------------------------------------|
| 1     | <title> | <brief end-to-end behavior> | <story refs> | —          | [Phase 1](PHASE-<feature>-1-<slug>.md) |
| 2     | <title> | <brief end-to-end behavior> | <story refs> | Phase 1    | [Phase 2](PHASE-<feature>-2-<slug>.md) |
| N     | <title> | <brief end-to-end behavior> | <story refs> | Phase N-1  | [Phase N](PHASE-<feature>-N-<slug>.md) |

</plan-index-template>

#### 6b. Phase Documents

For each phase in the index, write a **separate file** named `PHASE-<feature>-<N>-<slug>.md`. Each phase document must
be **self-contained** — a subagent implementing this phase should need only this document and the plan index, not any
other phase document.

<phase-document-template>
# Phase <N>: <Title>

> Source Plan: [PLAN-<feature>.md](PLAN-<feature>.md)

## User stories

<list from PRD or conversation>

## Relevant decisions

Paraphrase the implementation decisions from the PRD and Decision Snapshot that are relevant to this phase. Write them
in this document's own words — do not reproduce contracts byte-for-byte from any source.

If an explicitly-agreed code contract (interface, schema, API shape) from the PRD or Snapshot is directly relevant to
this phase, include it here in its natural form. But most decisions can be described in natural language.

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.
If a specific files needs to be modified, mention the file path.

As part of exploring the codebase to implement this phase, you may form high-level code contracts (class shapes,
interfaces, etc.) that make sense given existing code patterns. That's expected — phases are where implementation
details get worked out.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies

- **Depends on**: Phase <N-1> (or "None" for Phase 1)
- **Blocks**: Phase <N+1> (or "None" for the last phase)
  </phase-document-template>

### 7. Consistency Check

Before saving, review all phase documents against the PRD (if one exists):

- Does each phase paraphrase the relevant decisions accurately?
- Are there any contradictions between what a phase describes and what the PRD states?
- If you find a contradiction, align the phase with the PRD.

If implementation later reveals that a decision in the PRD needs to change, that divergence should be raised to the user
and accepted explicitly — later phases will then follow the updated approach rather than reverting to the old contract.
