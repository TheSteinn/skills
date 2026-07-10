Report each finding as one bullet in exactly this shape, every blocker listed before the first suggestion:

- `blocker (presumptive)` | `suggestion` — `path:line` — <one-sentence finding>
  cite: <axis-specific citation with a short quote>
  <free-form detail; any code in fenced blocks; no length cap>

Return only the findings (or the sentinel) — no preamble, no headers, no closing commentary.

Label rule: `blocker (presumptive)` only on an objective trigger or a documented-rule breach; otherwise
`suggestion`. When unsure, `suggestion`.

Nothing to report → the entire return is exactly this one line:
NO FINDINGS: <one line — what was reviewed>

Only if the instructions above authorise skipping and the skip condition holds → the entire return is exactly:
SKIPPED: <reason>
