---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

## Workflow

### 1. Understand the plan

If I haven't already, ask me to present my plan. Identify all major decision points and assumptions.

### 2. Probe each branch

Drill down on each decision point.

If a question can be answered by exploring the codebase, explore the codebase instead.

### 3. Resolve dependencies

When two decisions depend on each other, resolve the dependency explicitly. Confirm the resolution with the me before moving on.

### 4. Confirm shared understanding

Summarize the final state of the plan, listing all resolved decisions and remaining open questions. Get explicit confirmation from me.

**Interaction Rules**

- Ask one question at a time - Do not batch several unrelated questions into one message.
- Prefer single-select multiple choice - Use single-select when choosing one direction, one priority, or one next step.
- Use multi-select rarely and intentionally - Use it only for compatible sets such as goals, constraints, non-goals, or success criteria that can all coexist. If prioritization matters, follow up by asking which selected item is primary.
- Use the platform's question tool when available - When asking the user a question, prefer the platform's blocking question tool if one exists.
