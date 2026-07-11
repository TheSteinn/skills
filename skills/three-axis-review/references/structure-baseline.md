# Structure baseline

Two rules bind everything below. A documented repo standard always wins — where
it endorses something an entry would flag, suppress the entry. And every entry
is a labelled judgement call ("possible Feature Envy"), never a hard violation.

Each entry reads *tell* → *fix*; match it against the change:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal
  what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Feature Envy** — a method that reaches into another object's data more than
  its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a
  type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain
  concept that deserves its own type. → give the concept its own small type.
- **Shotgun Surgery** — one logical change forces scattered edits across many
  files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated
  reasons. → split so each module changes for one reason.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't
  depend on. → hide the walk behind one method on the first object.
- **Refused Bequest** — a subclass or implementer that ignores or overrides
  most of what it inherits. → drop the inheritance, use composition.
- **Duplicated Code** — the same logic shape copy-pasted across hunks or files
  instead of extracted. → extract the shared shape into one helper, call it
  from every site.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type
  recurs across the change, signalling a concept the model is missing. →
  replace with polymorphism, or one map every site shares.
- **Shallow Module (Middle Man)** — a wrapper, delegate, or pass-through helper
  that fails the deletion test: delete it and no complexity reappears at its
  callers. → cut it, call the real target direct.
- **Speculative Generality** — a generic mechanism, abstraction, parameter, or
  hook for needs the change doesn't have; one adapter means a hypothetical
  seam. → delete it; inline back until a real need shows.
- **Spaghetti Growth** — a new ad-hoc conditional, one-off boolean, nullable
  mode, or flag bolted into an unrelated or already busy flow. → reframe the
  state model or move the logic behind its own abstraction so the branch
  disappears.
- **Muddy Type Boundary** — casts, `any`/`unknown`, needless optionality, or a
  silent fallback papering over an unclear invariant; the interface is
  everything a caller must know. → make the boundary an explicit typed contract.
- **Wrong Layer / Bespoke Duplicate** — feature logic leaking into a shared
  path, or a near-duplicate of an existing canonical helper. → move the logic
  to the module that owns the concept; reuse the canonical helper.
- **Needless Sequencing / Non-Atomic Update** — independent work serialized for
  no reason, or related updates that can leave state half-applied. →
  parallelize what's independent; restructure related updates to land
  atomically.
- **File-Size Crossing** — a file pushed from ≤1,000 to >1,000 lines. Detected
  by the gate script and pre-seeded as `blocker (presumptive)`; do not
  re-derive it — add context only: is decomposition sensible, does the author
  justify the size. → split into focused modules before growing further.
