---
name: to-prd
description: Turn the current conversation context and Decision Snapshot into a PRD and save it as a Markdown file in the `./.planning` directory. Use when user wants to create a PRD, write a requirements document, or define feature scope and user stories. Particularly useful for large features that will be broken into multiple plans or issues, or when a standalone requirements document is needed for stakeholders. For small features, to-plan can work directly from the Snapshot without a PRD.
---

This skill takes the current conversation and codebase understanding and produces a PRD.

Do NOT run a broad discovery interview. Synthesize from the current conversation and codebase context. Only ask a brief
follow-up if needed to avoid a likely mistake in scope, module selection, or testing recommendations.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Keep exploration under the
   constraint of the current context - there is no need to explore unrelated modules.

2. **Read the Decision Snapshot.** Look for `.planning/decisions-<feature>.md`. If it exists, it is a historical record
   of the brainstorming session. Draw on it as context, but the PRD is the source of truth — write the PRD in its own
   words, not by reproducing the Snapshot.

3. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for
   opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable
interface which rarely changes.

If module boundaries or test targets are ambiguous, ask at most 1-2 focused clarification questions to confirm
expectations. Otherwise proceed without asking.

4. Write the PRD using the template below. Create `./.planning/` if it doesn't exist. Save the PRD as a Markdown file
   named after the feature and prefixed with `PRD` (e.g. `./.planning/PRD-user-onboarding.md`).

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

A list of implementation decisions that were made, written in the PRD's own words. This can include:

- The modules that will be built/modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Write these as natural-language descriptions of what was decided. Code contracts (interfaces, schemas, API shapes)
should only appear in this section when they were **explicitly agreed** during the design session AND are essential to
understanding the scope of the feature. When a code contract is included, write it in its natural form inside a fenced
code block — but do NOT reproduce contracts from the Decision Snapshot byte-for-byte. The PRD is its own document, not a
copy of the Snapshot.

Do NOT include specific file paths or code snippets for implementation details. They may end up being outdated very
quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which directly affected modules will be tested, or which existing modules need tests because their behavior must
  change to support the feature
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>

5. **Completeness Check.** Before saving the PRD, review it against the Decision Snapshot (if one exists) and the
   conversation context. Ask yourself:
    - Does the PRD cover all the decisions that were agreed to — either in user stories or in the Implementation
      Decisions section?
    - Are there any decisions from the Snapshot that are missing from the PRD entirely?
    - If you find a missing decision, add it (in the PRD's own words, not by copying from the Snapshot).
