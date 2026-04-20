---
name: to-prd
description: Turn the current conversation context into a PRD and save it as a Markdown file in the `./.planning` directory. Use when user wants to create a PRD from the current context.
---

This skill takes the current conversation context and codebase understanding and produces a PRD.

Do NOT run a broad discovery interview. Synthesize from the current conversation and codebase context. Only ask a brief follow-up if needed to avoid a likely mistake in scope, module selection, or testing recommendations.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Keep exploration under the constraint of the current context - there is no need to explore unrelated modules.

2. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

If module boundaries or test targets are ambiguous, ask at most 1-2 focused clarification questions to confirm expectations. Otherwise proceed without asking.

3. Write the PRD using the template below. Create `./.planning/` if it doesn't exist. Save the PRD as a Markdown file named after the feature and prefixed with `PRD` (e.g. `./.planning/PRD-user-onboarding.md`).

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which directly affected modules will be tested, or which existing modules need tests because their behavior must change to support the feature
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
