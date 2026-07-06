---
name: tdd
description: Test-driven development with the red-green-refactor loop. Use when the user wants to build features or fix bugs using TDD or test-first development, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red → green → refactor loop. This skill is the reference that makes the loop produce tests worth
keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. It is an
**implementation skill** — design happens before the loop, not inside it.

Before the loop, read `LANGUAGE.md` (if it exists) so test names and vocabulary match the project's domain
language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behaviour through public interfaces, not implementation details. Code can change entirely; tests
shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what
capability exists — and survives refactors because it doesn't care about internal structure. If persisted state
or an external side effect is itself the contract, assert that outcome directly.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Where tests go

Tests live at **seams** — used exactly as the `codebase-designing` glossary defines the term. Seams are a design
decision, so they should already exist when the loop starts: take them from the plan, design docs, or the
conversation. When they aren't established, ask the user — "What's the public interface, and which seams should
we test?" — rather than inventing them. When no user is reachable (delegated runs), derive the seams from the
phase scope and durable decisions, state them explicitly before the first test, and include them in your report.

You can't test everything. Before the first test, list the behaviours to cover and their priority — critical
paths and complex logic first, not every edge case. Take priorities from the plan when it has them; otherwise
confirm with the user.

If a test is hard to write at the agreed seam — awkward setup, no way to observe the behaviour — the design is
wrong, not the test. Step out of the loop and revisit the design (see `codebase-designing`); don't design
mid-loop.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side
  channel when a stable public interface is available. The tell: the test breaks when you refactor but behaviour
  hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does
  (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to
  itself), so it passes by construction and can never disagree with the code. Expected values must come from an
  independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify *imagined*
  behaviour: you test the shape of things rather than behaviour, and commit to test structure before
  understanding the implementation. Work in **vertical slices** — one test → one implementation → repeat, each
  test a **tracer bullet** responding to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write one failing test, watch it fail, then write only enough code to pass it. Don't
  anticipate future tests or add speculative features.
- **Minimal is not sloppy.** "Enough code to pass" means direct and well-structured, not tactical or hacky. A
  deliberately cheap spike to prove something is possible is the exception — flag it as such, and redo it
  properly once confirmed.
- **One slice at a time.** One seam, one behaviour, one test, one minimal implementation per cycle.
- **Green includes documentation.** Apply the `/code-doc` skill to any new or changed interfaces before moving on.
- **Never refactor while red.** Get to green first.

## Refactor

Refactor is the third step of the loop, and its scope is **tidying, not design**: remove duplication, improve
names, extract private helpers — restructure the implementation behind the seam. Run the tests after each
refactor step. The tests are the line: if a change would require touching a test, it isn't refactoring — it's a
new slice or a design revision.

If a refactor wants to change an interface, add an abstraction, or introduce a new seam, that's design leaking
into implementation — stop and take it back through the design stage instead.
