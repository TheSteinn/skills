# `/research` — what changed from the source

Inspired by the **QRSPI** workflow by [Dex Horthy](https://github.com/dexhorthy) / HumanLayer. QRSPI splits agentic
development into eight phases; `/research` handles the first two — Question and Research — in one skill. This documents
what survived intact and where this skill deviates, and why.

## What carried over

The core insight is kept whole: **facts by architecture, not by exhortation**. This skill keeps that, along with the
question-decomposition move ("query planning for codebases": the planner sees the task, the executors only see
questions), the WHERE/HOW/EXAMPLES fan-out (locator, analyzer, pattern-finder), file:line citations on every claim,
and a self-contained `research.md` with provenance frontmatter that downstream phases rebuild from.

## Question and Research are one invocation

QRSPI runs Question and Research as separate phases. But the human's role at the seam between them is only an
optional sanity-check of the questions — QRSPI itself doesn't gate on it. A gate that is optional in the source
doesn't justify a second invocation here, so `/research` merges the two: it decomposes the task, pauses once
to offer the questions for review, and proceeds on a single confirmation. The pause is offered, not gated — the
human review that *is* load-bearing (the design doc, the structure doc, the code) comes later in the pipeline.

## The firewall is blind subagents, not a fresh window

In QRSPI, the firewall between the task and the research is a fresh top-level context window: the questions are
carried into a new session that has never seen the ticket. Claude Code skills run in the main conversation — and by
the time `/research` fires, that conversation has already seen the task; there is no un-seeing it. So the firewall
moves down one level: the main window takes QRSPI's query-planner role (it may read the task, but only questions
travel downstream), and blind subagents are its executors. Their prompts are built from templates with **no slot for
task content** — the absence of the slot, not an instruction to stay neutral, is what keeps the research factual.

## Synthesis is blind too

The tempting shortcut is to let the main window merge the researchers' notes into `research.md` itself — it has all
of them in hand. That can cause a failure mode: decomposition *and synthesis* lived in the contaminated window, so the
task's framing leaked back into the "factual" record at the merge step. This skill spawns one more blind subagent to
organise the notes into the final document. The main window's only touch on the output is verification — spot-checking
citations and re-running researchers when one doesn't resolve, never editing findings from its own (task-aware) knowledge.
