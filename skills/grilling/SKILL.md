---
name: grilling
description: Core grilling technique — relentlessly interview the user about the subject under discussion (an idea, design, plan, or question) until shared understanding is reached. Use when the user asks to be grilled or interviewed, wants to stress-test an idea, design, plan or question, or when another skill's workflow calls for a grill.
user-invocable: false
---

Interview the user relentlessly about every aspect of the subject under discussion — an idea, design, plan, or
question — until you and the user reach a shared understanding. If the subject hasn't been presented yet, ask the user
to present it first.

Identify all major decision points and assumptions. Walk down each branch of the decision tree and resolve dependencies
between decisions one-by-one. For each question, provide your recommended answer — if a question can be answered by
exploring the codebase, explore the codebase instead of asking. When two decisions depend on each other, resolve the
dependency explicitly and confirm the resolution with the user before moving on.

## Closing the grill

The grill ends when every branch is resolved or explicitly parked. Close by presenting a decision record in chat:

- One entry per topic: the final resolution and a one-line rationale (naming what it replaced, if anything). A topic
  with multiple positions appears exactly once — superseded positions are collapsed, not listed.
- Include a contract (interface, schema, API shape) only if one was explicitly proposed and confirmed during the
  session — never invent one; prose resolutions stay prose.
- If durable docs were written during the session (glossary terms, ADRs), reference them — don't restate their content.
- Then list cross-topic dependencies, and any remaining open questions or outstanding items.

Get the user's explicit confirmation of this record.

<CRITICAL>
- Ask one question at a time — asking multiple questions at once creates cognitive overload.
- When asking a question, wait for an explicit answer before continuing — the user may have queries or feedback on a
  decision point to resolve first.
- Do not implement anything during the grill — grilling is elicitation, not implementation.
</CRITICAL>
