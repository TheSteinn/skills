# Decision Snapshot

Compiled at the confirmation gate (workflow step 5), after I confirm shared understanding. Consult this spec when you
compile it.

The Decision Snapshot is a **historical record of the brainstorming session**. It captures what we discussed and
decided. Downstream documents (PRD, Plan) draw on it as a source of context, but the Snapshot is not an authoritative
contract — the PRD and Plan documents are the source of truth during implementation. If implementation reveals a
contract needs to change, that divergence is accepted and noted rather than treated as a violation of the Snapshot.

## Reconciliation preamble (do this first, in your reasoning)

1. List every **topic** we discussed (e.g., "Authentication mechanism", "Database schema", "API pagination").
2. For each topic, list every **position** that was considered, in chronological order. Mark each as `accepted`,
   `rejected`, or `superseded`.
3. State the **final resolution** for each topic.
4. Identify any **cross-topic dependencies** (e.g., "Caching strategy depends on Authentication mechanism being
   stateless").
5. If a topic has no clear final resolution, list it under **Open Questions** instead of Decisions.

## Snapshot rules

- Only include topics with a clear, confirmed final resolution in the Decisions section.
- A topic that had multiple positions must appear exactly once, with only the final resolution.
- Do NOT include rejected alternatives in the Decisions section. You may briefly note what was replaced in the Rationale
  field.
- **Reference durable docs; never restate them (content boundary).** A choice captured as a glossary term or an ADR
  lives canonically in its durable file. In the Snapshot, *reference* it — `→ LANGUAGE.md` for a term, `→ ADR-NNNN` for
  an ADR — and do not restate its definition or rationale. Each piece of content has exactly one canonical copy.
  A decision whose ADR offer I declined is demoted to middle-tier: it has no durable home, so record it as an ordinary
  Decision here — never silently lost.
  **In a monorepo, qualify every reference with its owning context** (the name from `CONTEXT-MAP.md`):
  `→ Ordering LANGUAGE.md`, `→ Ordering ADR-0007`, or `→ root ADR-0003` for a cross-cutting ADR; single-context
  references stay bare. The Decisions section is therefore for the **middle-tier decisions** — real choices that are neither glossary terms nor
  ADRs (e.g. "cart uses optimistic locking", "paginate with cursors") — plus the reasoning and rejected alternatives
  that have no home in the durable docs.
- **Record code/language divergences as findings.** If the cross-reference-with-code lens found the code disagreeing
  with the canonical language and the human made the *language* canonical, log it under **Code/language divergences** as
  an outstanding code rename. No code is edited — the finding is the record.
- **Contracts are optional.** Only include a `Contracts` block for a topic when a concrete interface, schema, or API
  shape was explicitly proposed (by you or the user) AND explicitly confirmed by the user during the session. Do NOT
  invent code contracts for decisions that were discussed in natural language — a decision like "use PostgreSQL" does
  not need a SQL schema block. When a contract IS included, write it in its natural form (TypeScript, JSON, SQL,
  OpenAPI, etc.) inside a fenced code block.
    - Decisions like "should return a list", or others that can be described via prose do not need a fenced code block
- If no explicit contract was agreed for a topic, omit the `Contracts` field entirely — the Resolution prose is
  sufficient.

## Snapshot file

Create `./.planning/` if it doesn't exist. Save the snapshot as `.planning/decisions-<feature>.md`.

The Snapshot is **non-authoritative** and **safe to delete once a PRD or plan exists** — its middle-tier decisions live
in it until they are promoted into a PRD/plan downstream. **No skill ever auto-deletes it**; deletion is the human's
call.

## Template

<snapshot-template>
# Decision Snapshot: <Feature Name>

> **Canonical docs** — language: `LANGUAGE.md` · ADRs: `docs/adr/`
> Non-authoritative brainstorm record. Safe to delete once a PRD or plan exists; no skill auto-deletes it.

## Decisions

### <Topic Name>

- **Resolution**: <The final, confirmed decision. Reference any term/ADR with `→ LANGUAGE.md` / `→ ADR-NNNN` instead of
  restating it (context-qualified in a monorepo — see the content-boundary rule).>
- **Rationale**: <Why this was chosen. If it replaced an earlier decision, name the earlier decision and briefly why it
  was rejected.>
- **Contracts** *(only if an explicit contract was agreed during the session)*:
  ```<language>
  <Exact contract as discussed and confirmed>
  ```

<!-- Repeat for each resolved middle-tier topic -->

## Captured in durable docs

<!-- Omit this section if the session produced no terms or ADRs. -->
Terms and decisions promoted to canonical docs this session — referenced here, defined there (never restated). Single
context:

- `<Term>`, `<Term>` → LANGUAGE.md
- → ADR-NNNN (<short title>)

In a monorepo, group by owning context (which qualifies every reference under it):

- **Ordering** — `<Term>`, `<Term>` → LANGUAGE.md · → ADR-0007 (<short title>)
- **root** — → ADR-0003 (<short title>)
- **CONTEXT-MAP.md** — Ordering → Billing (<what flows>)

## Dependencies

- **<Topic A>** depends on **<Topic B>** being resolved as `<resolution>`.

## Open Questions

- <Any topic that was discussed but not definitively resolved>

## Code/language divergences

<!-- Omit this section unless the cross-reference lens found the code disagreeing with the canonical language. -->
- **<concept>**: canonical language is `<documented term>` (→ LANGUAGE.md; context-qualified in a monorepo), but the
  code uses `<code name>` — outstanding code rename, not yet applied. No code was changed.
</snapshot-template>

In a monorepo, the pointer header points at `CONTEXT-MAP.md` (and the relevant module docs) instead of a single root
`LANGUAGE.md`, for example:

> **Canonical docs** — contexts: `CONTEXT-MAP.md` · ADRs: `docs/adr/` (+ `<module>/docs/adr/`)
