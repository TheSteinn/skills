---
name: codebase-designing
description: Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, diagnose why code is hard to understand or change, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that
interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage
for callers, locality for maintainers, and testability for everyone — all in service of reducing **complexity**:
keeping the system easy to understand and modify.

## Glossary

Use these terms exactly — don't substitute "component," "service," "API," or "boundary." Consistent language is the
whole point.

**Module** — anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package,
or tier-spanning slice. _Avoid_: unit, component, service.

**Interface** — everything a caller must know to use the module correctly: the type signature, but also invariants,
ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API, signature (too
narrow — they refer only to the type-level surface).

**Implementation** — what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter
with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach
for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth** — leverage at the interface: the amount of behaviour a caller (or test) can exercise per unit of interface
they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow**
when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_ — a place where you can alter behaviour without editing in that place; the *location* at
which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it.
_Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter** — a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not
substance (what's inside).

**Leverage** — what callers get from depth: more capability per unit of interface they learn. One implementation pays
back across N call sites and M tests.

**Locality** — what maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place
rather than spreading across callers. Fix once, fixed everywhere.

**Complexity** — anything about the structure of a system that makes it hard to understand and modify.
Symptoms: change amplification, cognitive load, unknown unknowns. Causes: dependencies and obscurity.
See [complexity.md](references/complexity.md).

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small,
  mockable, swappable parts — they just aren't part of the interface. A module can have **internal seams** (private to
  its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity
  reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the
  interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something
  actually varies across it.
- **Judge every design idea by whether it reduces complexity** — does it reduce the amount of information a developer
  must hold in their head, or make the required information more obvious? For the symptoms and causes of complexity,
  see [complexity.md](references/complexity.md).

## Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.
- **Complexity** is what all of the above reduce: **Depth** lowers cognitive load, **Locality** counters change
  amplification, and obvious **Interfaces** fight obscurity and unknown unknowns.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use
  depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow — interface here
  includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

## Going deeper

- **Recognising and diagnosing complexity** — see [complexity.md](references/complexity.md): Ousterhout's definition,
  the three symptoms (change amplification, cognitive load, unknown unknowns), the two causes (dependencies,
  obscurity), and the zero-tolerance stance — complexity accumulates incrementally.
- **Deepening a cluster given its dependencies** — see [deepening.md](references/deepening.md): dependency categories,
  seam discipline, and replace-don't-layer testing.
- **Exploring alternative interfaces** — see [design-it-twice.md](references/design-it-twice.md): spin up parallel
  sub-agents to design the interface several radically different ways, then compare on depth, locality, and seam
  placement.