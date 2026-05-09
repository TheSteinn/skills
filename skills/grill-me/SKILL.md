---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch
of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended
answer.

## Workflow

### 1. Understand the plan

If I haven't already, ask me to present my plan. Identify all major decision points and assumptions.

### 2. Probe each branch

Drill down on each decision point.

If a question can be answered by exploring the codebase, explore the codebase instead.

### 3. Resolve dependencies

When two decisions depend on each other, resolve the dependency explicitly. Confirm the resolution with me before moving
on.

### 4. Confirm shared understanding

Summarize the final state of the plan, listing all resolved decisions and remaining open questions. Get explicit
confirmation from me.

**Interaction Rules**

- Ask one question at a time - Do not batch several unrelated questions into one message.
- Prefer single-select multiple choice - Use single-select when choosing one direction, one priority, or one next step.
- Use multi-select rarely and intentionally - Use it only for compatible sets such as goals, constraints, non-goals, or
  success criteria that can all coexist. If prioritization matters, follow up by asking which selected item is primary.
- When asking the user a question, you MUST use the platform's blocking question tool if one exists, e.g. `askQuestion`,
  `askUserQuestion`, etc.

### 5. Compile Decision Snapshot

After I confirm the shared understanding, you MUST compile a **Decision Snapshot** before ending the session.

The Decision Snapshot is a **historical record of the brainstorming session**. It captures what we discussed and
decided. Downstream documents (PRD, Plan) draw on it as a source of context, but the Snapshot is not an authoritative
contract — the PRD and Plan documents are the source of truth during implementation. If implementation reveals a
contract needs to change, that divergence is accepted and noted rather than treated as a violation of the Snapshot.

**Reconciliation Preamble (do this first, in your reasoning):**

1. List every **topic** we discussed (e.g., "Authentication mechanism", "Database schema", "API pagination").
2. For each topic, list every **position** that was considered, in chronological order. Mark each as `accepted`,
   `rejected`, or `superseded`.
3. State the **final resolution** for each topic.
4. Identify any **cross-topic dependencies** (e.g., "Caching strategy depends on Authentication mechanism being
   stateless").
5. If a topic has no clear final resolution, list it under **Open Questions** instead of Decisions.

**Snapshot Rules:**

- Only include topics with a clear, confirmed final resolution in the Decisions section.
- A topic that had multiple positions must appear exactly once, with only the final resolution.
- Do NOT include rejected alternatives in the Decisions section. You may briefly note what was replaced in the Rationale
  field.
- **Contracts are optional.** Only include a `Contracts` block for a topic when a concrete interface, schema, or API
  shape was explicitly proposed (by you or the user) AND explicitly confirmed by the user during the session. Do NOT
  invent code contracts for decisions that were discussed in natural language — a decision like "use PostgreSQL" does
  not need a SQL schema block. When a contract IS included, write it in its natural form (TypeScript, JSON, SQL,
  OpenAPI, etc.) inside a fenced code block.
    - Decisions like "should return a list", or others that can be described via prose do not need a fenced code block
- If no explicit contract was agreed for a topic, omit the `Contracts` field entirely — the Resolution prose is
  sufficient.

**Snapshot File:**

Create `./.planning/` if it doesn't exist. Save the snapshot as `.planning/decisions-<feature>.md`.

<snapshot-template>
# Decision Snapshot: <Feature Name>

## Decisions

### <Topic Name>

- **Resolution**: <The final, confirmed decision>
- **Rationale**: <Why this was chosen. If it replaced an earlier decision, name the earlier decision and briefly why it
  was rejected.>
- **Contracts** *(only if an explicit contract was agreed during the session)*:
  ```<language>
  <Exact contract as discussed and confirmed>
  ```

<!-- Repeat for each resolved topic -->

## Dependencies

- **<Topic A>** depends on **<Topic B>** being resolved as `<resolution>`.

## Open Questions

- <Any topic that was discussed but not definitively resolved>

</snapshot-template>
