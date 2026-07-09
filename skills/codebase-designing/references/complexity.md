# Complexity

What complexity is, how it shows up, and what causes it. From Ousterhout, *A Philosophy of Software Design*. Use this
as the lens for evaluating any design decision: does it reduce complexity? Assumes the vocabulary
in [SKILL.md](../SKILL.md) — **module**, **interface**, **depth**, **seam**, **locality**.

## Definition

**Complexity is anything related to the structure of a software system that makes it hard to understand and modify the
system.** It might be hard to understand how a piece of code works; a small improvement might take a lot of effort; it
might not be clear which parts of the system must be modified; it might be difficult to fix one bug without introducing
another. If a system is hard to understand and modify, it is complicated; if it is easy to understand and modify, it is
simple.

The most important contributors to complexity relate to information:

- How much information must a developer have in their head in order to carry out a task?
- How accessible and obvious is the information the developer needs?

The more information a developer needs, the harder the work. It gets worse when the required information isn't obvious.
The worst case is a crucial piece of information hidden in some far-away piece of code the developer has never heard
of.

**Apparent complexity is what matters** — what a developer experiences at a particular moment, in the common case. It
is judged by readers of the code, not the writer, and doesn't necessarily correlate with system size or number of
features.

## Symptoms

### Change amplification

A seemingly simple change requires code modifications in many different places — e.g. an old web site where a colour is
defined explicitly on each page. A goal of good design is to reduce the amount of code affected by each design
decision, so design changes don't require many code modifications.

### Cognitive load

How much a developer needs to know in order to complete a task. Higher load means more time spent learning, and a
greater risk of bugs from missing something important — e.g. a C function that allocates memory and returns a pointer,
assuming the caller will free it; a caller who doesn't know that leaks memory. Cognitive load arises from APIs with
many methods, global variables, inconsistencies, and dependencies between modules. **Lines of code do not measure
complexity**: an approach with more lines can be simpler, if it reduces cognitive load.

### Unknown unknowns

It is not obvious which code must be modified, or what information is needed to carry out the task — **the worst of the
three symptoms**. There is something you need to know, but no way to find out what it is, or even whether there is an
issue; you find out when bugs appear after the change. Change amplification is annoying, but once it's clear which code
to modify, the system works when the change is complete. High cognitive load raises the cost of a change, but if it's
clear what to read, the change is still likely correct. With unknown unknowns, it is unclear what to do or whether a
proposed solution will even work; the only way to be certain is to read every line of the system — impossible for
systems of any size, and still insufficient when the change depends on a design decision that was never documented.

**The antidote is obviousness — one of the most important goals of good design, and the opposite of high cognitive load
and unknown unknowns.** In an obvious system, a developer can quickly understand how the existing code works and what
is required to make a change. A developer can make a quick guess about what to do, without thinking very hard, and yet
be confident the guess is correct.

## Causes

### Dependencies

A dependency exists when a piece of code cannot be understood and modified in isolation: the code relates to other
code, and that other code must be considered — and possibly modified — alongside it. Dependencies are fundamental to
software and can't be completely eliminated: every new class creates dependencies around its API, and every method
signature creates a dependency between the implementation and its callers. The design goal is to **reduce the number of
dependencies and make the ones that remain as simple and obvious as possible**.

### Obscurity

Important information is not obvious — a variable name so generic it carries no useful information, or documentation
that omits a variable's units so the only way to find out is scanning the code for uses. Obscurity is often associated
with dependencies: a dependency exists, but it isn't obvious that it does. Inconsistency is a major contributor — the
same name used for two different purposes. Inadequate documentation plays a part, but obscurity is a design issue: **a
clean, obvious design needs less documentation, and the need for extensive documentation is a red flag that the design
isn't right**. The best way to reduce obscurity is to simplify the design.

## Complexity is incremental

No single thing makes a system complicated. Complexity accumulates in thousands of small dependencies and obscurities,
and once it arises it is hard to eliminate. **Adopt zero tolerance: everything matters.**

## The evaluative question

When weighing any design idea, ask: **will it reduce complexity?** That usually means one of two things:

- reducing the amount of information a developer has to know, or
- making the required information more obvious.

## How this skill fights it

Each term in [SKILL.md](../SKILL.md) attacks a symptom or a cause:

- An **interface**, as defined there, is everything a caller must know — a caller's cognitive load, made explicit. A
  **deep** module lowers that load: more behaviour per unit of interface to learn.
- **Locality** counters change amplification: change, bugs, and knowledge concentrate in one place instead of spreading
  across callers.
- **Seams** don't remove dependencies — nothing can — but they make the ones that remain simple and obvious, which is
  exactly the design goal for dependencies.
- Obscurity at an interface becomes unknown unknowns: invariants, ordering constraints, or error modes that callers
  must honour but can't see are discovered through bugs. **Keep the real interface no bigger than the visible one.**
