# Phase 1: Gate script reports size crossings

> Source: [index.md](index.md). Self-contained: implement from this file + the index only.

## Overview

Deliver `skills/three-axis-review/scripts/file_size_gate.py`: a deterministic script that, given a fixed point,
reports every file the branch pushes from ≤1,000 lines to >1,000 lines. It comes first because it is the skill's
only executable component, it is testable in complete isolation, and it is the prototype for the objective-trigger
labelling the whole output contract rests on (decisions 3 and 6).

## Context

- The rule this script owns: "Do not let a PR push a file from under 1k lines to over 1k lines without a very
  strong reason" (`.planning/review/nuclear-review.md:34-38`) — the only objectively checkable criterion in either
  source skill. Per decision 6, the orchestrator runs this script at step 1 and pre-seeds its output as Structure
  findings labelled `blocker (presumptive)`; the Structure sub-agent only adds context. Nothing in this phase
  builds that wiring — the script is a plain CLI, a process boundary needing no skill around it.
- House precedent for skill scripts: `skills/skill-creator/scripts/` — Python 3, `#!/usr/bin/env python3`, module
  docstring with a Usage section, stdlib only.
- Diff semantics must match the skill's review scope (decision 1): comparison is against the merge-base of
  `<fixed-point>` and `HEAD` (three-dot semantics), and the "after" state is `HEAD`, never the working tree.
- The binding interface is **Contract A** in the index, restated in full:
  - Invocation: `python3 skills/three-axis-review/scripts/file_size_gate.py <fixed-point>`
  - Threshold fixed at 1,000. A crossing is `before ≤ 1000 and after > 1000`. New files count `before = 0`;
    deleted files never cross.
  - Diff enumeration: `git diff --name-status -M -z <merge-base> HEAD`, parsed as NUL-separated records. Statuses:
    `A` → (None, path); `M` → (path, path); `D` → skip; `R<n>` → (old_path, new_path) — record shape
    `R<score>\0old\0new\0`; any other status (`T`, …) → treat as `M` at the after path. No `-C`: copies surface as
    adds.
  - `before` is counted at the merge-base (at the old path for renames); `after` is counted at `HEAD`.
  - Binary = blob contains a NUL byte → skip the file entirely.
  - Line count = count of `b"\n"`, +1 if the file is non-empty and lacks a trailing newline.
  - Output: one TSV line per crossing to stdout — `path<TAB>before<TAB>after` — sorted by path; **empty stdout
    means no crossings**. No headers, no prose.
  - Exit codes: `0` on success (with or without crossings); `2` on usage error or any git failure (unresolvable
    ref, no merge-base, not a repo), with the reason on stderr.
  - Stdlib only; no third-party imports.

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The script

**File**: `skills/three-axis-review/scripts/file_size_gate.py`
**Change**: create the script implementing Contract A.

```python
#!/usr/bin/env python3
"""Report files a branch pushes past 1,000 lines.

Compares each changed file's line count at the merge-base of <fixed-point>
and HEAD against its line count at HEAD. Prints one TSV line per file that
crosses the threshold: path<TAB>before<TAB>after. Empty output = no crossings.

Usage:
    python3 file_size_gate.py <fixed-point>

Exit codes: 0 success; 2 usage or git error.
"""

THRESHOLD = 1000

def run_git(*args) -> bytes:
    # subprocess.run(["git", *args], capture_output=True)
    # non-zero exit -> reason to stderr, sys.exit(2)
    ...

def changed_files(base: str) -> list[tuple[str | None, str]]:
    # run_git("diff", "--name-status", "-M", "-z", base, "HEAD")
    # walk NUL-separated tokens; yield (before_path, after_path):
    #   A -> (None, path)   M -> (path, path)   D -> skip
    #   R<score> -> (old, new)   anything else -> (path, path)
    ...

def line_count(rev: str, path: str) -> int | None:
    # blob = run_git("show", f"{rev}:{path}")
    # b"\0" in blob -> None (binary; caller skips the file)
    # count b"\n"; +1 if blob non-empty and not blob.endswith(b"\n")
    ...

def main() -> int:
    # 1. argv check -> usage on stderr, exit 2
    # 2. base = run_git("merge-base", fixed_point, "HEAD") (strip)
    # 3. for each (before_path, after_path):
    #      before = 0 if before_path is None else line_count(base, before_path)
    #      after  = line_count("HEAD", after_path)
    #      either side binary (None) -> skip file
    #      collect where before <= THRESHOLD < after
    # 4. print sorted "path\tbefore\tafter" lines; return 0
    ...
```

## Success criteria

### Automated verification

- [x] Fixture repo behaves per Contract A — build it once, then assert each case (`<repo>` is this repo's
      absolute path):

  ```bash
  FIX="$TMPDIR/fsg-fixture" && rm -rf "$FIX" && mkdir -p "$FIX" && cd "$FIX" && git init -qb main
  seq 900  > grows.txt          # 900 -> 1100: crossing
  seq 1100 > already-big.txt    # 1100 -> 1300: no crossing (already over)
  seq 500  > shrinks.txt        # deleted on the branch: no crossing
  seq 950  > renamed.txt        # renamed and grown 950 -> 1050: crossing, counted across the rename
  seq 900  > boundary.txt       # 900 -> exactly 1000: no crossing (after must exceed 1000)
  git add -A && git commit -qm base && git checkout -qb feature
  seq 1100 > grows.txt && seq 1300 > already-big.txt && seq 1000 > boundary.txt && git rm -q shrinks.txt
  git mv renamed.txt renamed-new.txt && seq 1050 > renamed-new.txt
  seq 1200 > brand-new.txt                       # new at 1200: crossing (before = 0)
  { seq 1000; printf 'tail'; } > no-trail.txt    # 1001 lines, last lacks newline: crossing (before = 0)
  { seq 1200; printf '\0'; } > binary.bin        # >1000 newlines but contains NUL: binary, skipped
  git add -A && git commit -qm feature
  python3 <repo>/skills/three-axis-review/scripts/file_size_gate.py main > "$TMPDIR/fsg-actual.txt"; echo "exit=$?"
  ```

- [x] Output is exactly four sorted TSV lines and nothing else:

  ```bash
  printf 'brand-new.txt\t0\t1200\ngrows.txt\t900\t1100\nno-trail.txt\t0\t1001\nrenamed-new.txt\t950\t1050\n' > "$TMPDIR/fsg-expected.txt"
  diff "$TMPDIR/fsg-expected.txt" "$TMPDIR/fsg-actual.txt" && echo TSV-OK
  ```

- [x] Exit code 0 on the fixture run (the `exit=` echo above prints `exit=0`).
- [x] Empty output + exit 0 when nothing crosses: in the fixture,
      `python3 <repo>/skills/three-axis-review/scripts/file_size_gate.py HEAD; echo $?` prints only `0`.
- [x] Exit 2 with a stderr message on a bad ref: in the fixture,
      `python3 <repo>/skills/three-axis-review/scripts/file_size_gate.py no-such-ref; echo $?`.
- [x] Exit 2 on missing argument: `python3 <repo>/skills/three-axis-review/scripts/file_size_gate.py; echo $?`.
- [x] Exit 2 outside a git repo: from a non-repo directory (e.g. `cd "$TMPDIR"`),
      `python3 <repo>/skills/three-axis-review/scripts/file_size_gate.py main; echo $?`.
- [x] Stdlib only:
      `grep -E '^(import|from)' <repo>/skills/three-axis-review/scripts/file_size_gate.py | grep -vE '^(import|from) (sys|os|subprocess|argparse|pathlib)\b'`
      finds nothing.

### Manual verification

None

## Dependencies

- **Depends on**: None
- **Blocks**: 3, 6
