---
name: orchestrate-plan
description: Orchestrates codebase implementation of a multi-phase plan, delegating all coding work to subagents. Use when the user wants to implement a plan via orchestration and delegating to subagents.
---

# Orchestrate Plan

Orchestrate implementation of the plan, ensuring you fully understand the plan, the underlying PRD it references, and
relevant areas of the codebase.

You are an orchestrator – your job is to understand the overall task, scope, implementation phases, and keep track of
completed work. You delegate all phase implementation, and by extension code implementation, to dedicated and
independent subagents.

Ensure, when orchestrating the implementation of the plan, you understand how to do so in a TDD manner.

Ensure each subagent you delegate to has a complete encapsulation of the work they need to complete, the scope, and
necessary context. The subagent MUST use the `/tdd` skill - always start the subagent prompt with "/tdd". If a phase has
a specific implementation/architectural decision or instruction, the subagent should know that instead of defining its
own scope/path. If a phase has specific prior art, the subagent should know that.

Keep track of the implementation phases in your task/todo list. When a subagent responds that they have completed a
phase, check the acceptance criteria listed in the plan, and check each item off within the plan document. If an
acceptance criteria does not pass, delegate back to a subagent to address the issue. If a subagent has contradicted or
violated a durable architectural/design decision, it has failed its task – delegate to a new subagent with the original
phases task, scope, prior art, and the violation the original subagent implementation made. If a subagent fails twice
for any one phase, cancel the orchestration and respond back to the human in the loop to course-correct.

- Your todo list – keep track of phases and other high-level tasks
- The plan acceptance criteria lists – keep track of what acceptance criteria have been met
