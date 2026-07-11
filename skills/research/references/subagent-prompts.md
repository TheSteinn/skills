# Subagent prompts

> **These templates have no slot for task content. That absence is deliberate — it is the firewall.** Research stays
> factual because the researchers cannot know the intended change; a researcher that knows the destination starts
> finding evidence for it. Never add a task, background, or context slot to any template, and never smuggle task
> content through an existing placeholder.

Every prompt `/research` sends to a subagent is built from a template on this page: fill the placeholders, add
nothing else.

## Placeholders

- `<path>` — absolute path to the repository being researched
- `<question>` — one research question, copied verbatim from `questions.md`
- `<notes-path>` — `.planning/<slug>/research-notes/<topic>.md`, where `<topic>` is a short kebab-case name derived
  from the question
- `<slug>` — the feature slug naming the `.planning/<slug>/` directory

Choose the template by what the question asks for: **locator** for WHERE, **analyzer** for HOW, **pattern-finder**
for EXAMPLES. A broad question may fan out to more than one researcher — a locator to map the ground, then an
analyzer to trace it.

## Locator — WHERE things live

For questions about location: which files, directories, and layers are involved.

```
In the repository at <path>, find WHERE the following lives: <question>. Report file paths grouped by role (entry
points, config, tests, docs). Write your findings to <notes-path>.

Return findings with file:line citations. Document what IS, not what should be. No recommendations, no critique.
```

## Analyzer — HOW it works

For questions about behaviour: control flow, data flow, life cycles.

```
In the repository at <path>, explain HOW the following works: <question>. Trace the flow end to end; cite every
claim as file:line. Read files fully before concluding. Write your findings to <notes-path>.

Return findings with file:line citations. Document what IS, not what should be. No recommendations, no critique.
```

## Pattern-finder — EXAMPLES to follow

For questions about precedent: existing code that already solves a similar shape.

```
In the repository at <path>, find existing EXAMPLES relevant to: <question>. For each, show the pattern with
file:line and what it is an example of. Write your findings to <notes-path>.

Return findings with file:line citations. Document what IS, not what should be. No recommendations, no critique.
```

## Synthesizer

One synthesis subagent runs after every researcher has written its notes. Append the research.md template (next
section) to this prompt, so "the template below" resolves.

```
Read .planning/<slug>/questions.md and every file in .planning/<slug>/research-notes/. Write
.planning/<slug>/research.md using the template below. You are organising verified findings — do not add conclusions
of your own, do not speculate about purpose. Preserve citations exactly.

Return findings with file:line citations. Document what IS, not what should be. No recommendations, no critique.
```

## research.md template

```
---
date: <YYYY-MM-DD>
git_commit: <commit the research was run against>
branch: <branch name>
questions: questions.md
---

## Summary

<What the findings add up to, in a few paragraphs a stranger could follow.>

## Q1: <question>

<Findings that answer this question, every claim cited as file:line. One section per question, in questions.md
order.>

## Unanswered questions

<Anything the notes could not settle — the question, or the part of it, and where the researchers looked without
finding an answer.>
```
