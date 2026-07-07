---
name: research
description: QRSPI step 1 — decompose a task into neutral research questions, then answer them with task-blind subagents. Produces task.md, questions.md, and research.md (facts with file:line citations, no recommendations) in .planning/<feature>/.
disable-model-invocation: true
---

# Research (Question + Research)

Turn a task into neutral research questions, then answer them with subagents that never see the task. You are the
query planner: you may read the task, but only questions travel downstream. The result is a factual map of the
codebase — what IS, with file:line citations — that the design step can trust precisely because none of it was
written with the intended change in mind.

## 1. Capture the task

The task comes from the user's invocation — a description, ticket text, or a file path. If nothing was given, ask the
user for it. Read any referenced files fully before moving on.

Derive a short kebab-case feature slug and create `.planning/<slug>/`. Write `task.md` there: the task as given
(verbatim where possible) plus its source — a link, a ticket reference, or "conversation". Later phases read this
file instead of re-deriving the task, so capture it faithfully.

## 2. Decompose into neutral questions

Write `questions.md`: the research questions whose answers would let a stranger design this feature. Good questions
send a researcher into every part of the codebase that matters — "how do X endpoints work end to end?", "trace
everything that touches Y", "what patterns exist for Z?".

Neutrality is the contract: a question must not reveal or imply the intended change. Test each one — could a reader
reconstruct the task from it? If yes, rewrite it. ("How should multi-tenant support be added?" fails; "how is tenancy
currently modelled, and where is it enforced?" passes.)

Present the questions to the user and ask whether to adjust or proceed — one confirmation, then move on.

## 3. Research with blind subagents

Spawn parallel general-purpose subagents to answer the questions, building every prompt from
[subagent-prompts.md](references/subagent-prompts.md). A prompt contains question text, the repo location, and output
instructions — nothing else. Never put task content, the intended change, or conversation context into a subagent
prompt: the subagents' blindness is the firewall that keeps the research factual. A researcher that knows the
destination starts finding evidence for it.

Fan out along the reference's three axes:

- **Locators** — WHERE things live: file paths grouped by role.
- **Analyzers** — HOW things work: flows traced end to end, every claim cited.
- **Pattern-finders** — EXAMPLES to follow: existing code that already solves a similar shape.

Findings must carry file:line citations and describe what IS — researchers are documentarians, not critics. Each
subagent writes its findings to `.planning/<slug>/research-notes/<topic>.md`.

## 4. Blind synthesis

Spawn one more subagent — its prompt again built from [subagent-prompts.md](references/subagent-prompts.md), again
without the task — that reads `questions.md` and the notes and writes `research.md` per the reference's template:
provenance frontmatter (date, git commit, branch), a summary, findings organised by question with citations
preserved, and unanswered questions. Target ~300 lines. Delete `research-notes/` after synthesis — `research.md` is
the artifact; the notes are scaffolding.

## 5. Hand off

Spot-check a few citations against the live code. Fix any that don't resolve by re-running the relevant subagent —
never by editing findings from your own knowledge, because your window knows the task and the document must stay
blind. Then ask the user to skim `research.md` for factual misses, and point at `/design` as the next step — best run
in a fresh session (`/clear`), rebuilt from the artifacts rather than this conversation.
