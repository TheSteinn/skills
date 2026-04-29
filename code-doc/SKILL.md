---
name: code-doc
description: >
  Guidelines for writing high-quality code documentation (doc comments) across any language.
  Use this skill whenever the user asks about writing, reviewing, or improving documentation
  comments — including docstrings, doc comments, KDoc, Javadoc, JSDoc, or any in-code
  documentation. Trigger even if the user just says "how should I document this?" or "is this
  comment good?" or pastes code and asks for doc improvements.
---

# code-doc
 
Guidelines for writing documentation comments that are clear, useful, and appropriately
scoped — regardless of language.
 
## Language-specific reference index
 
Before applying generic guidance below, check whether a language-specific reference file
exists and load it for additional rules and examples that override or extend the generic ones.
 
| Language | Reference file |
|----------|---------------|
| Kotlin (KDoc) | `references/kdoc.md` |
 
If the user's language is not listed, apply the generic guidance only.
 
---
 
## Generic documentation patterns
 
These apply to all languages unless overridden by a language-specific reference.
 
<should>
 
- **Document the interface, not the implementation.** The comment should give a developer
  everything they need to use a class, function, or module correctly — intent, behaviour,
  parameters, return values, side effects — without requiring them to read the code itself.
- **Include sufficient detail.** A comment so terse it conveys nothing is worse than no
  comment at all. Avoid filler like "Gets the value" for a getter or "Constructor" for a
  constructor.
- **Make the opening sentence count.** The first sentence (or first paragraph, depending on
  the toolchain) is surfaced in IDE tooltips, generated API references, and package/class
  overviews. Write it to be immediately useful in isolation: a single clear statement of
  what the element *does* or *is*.
- **Separate the summary from the detail.** Where the doc format supports it (most do),
  put the summary in the first block and additional detail after a visual break (blank line,
  `<p>`, etc.). Keep the two sections clearly distinct.
- **Link to related symbols.** Where the toolchain supports it, use cross-reference syntax
  to link types, parameters, and related functions so readers can navigate directly.
- **Document edge cases and non-obvious behaviour.** Nullability, empty-collection
  semantics, throwing conditions, thread safety, and ordering constraints are exactly what
  callers need to know and exactly what code alone doesn't communicate.

</should>
 

<should-not>
 
- **Repeat the code verbatim.** A comment that just restates the signature in prose adds
  noise without adding meaning.
- **Be so long that readers skim or skip it.** Prefer concise, high-signal prose. If detail
  is genuinely necessary, structure it so the summary remains short and the detail is
  clearly secondary.
- **State the obvious.** Don't document what the name already unambiguously expresses
  unless there is a non-obvious nuance to add.
</should-not>
