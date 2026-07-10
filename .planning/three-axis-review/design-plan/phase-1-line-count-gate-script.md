# Design 1: Line-count gate script

> Source: [index.md](index.md). Self-contained: refine from this file + the index only.

## Overview

Deliver `skills/three-axis-review/scripts/file_size_gate.py`: a deterministic script that, given a fixed point,
reports every file the branch pushes from ≤1,000 lines to >1,000 lines. It comes first because it is the skill's only
executable component, it is testable in complete isolation, and it is the prototype for the objective-trigger
labelling the whole output contract rests on (durable decisions 3 and 6).

## Context

- The rule originates in `.planning/review/nuclear-review.md:34-38`: "Do not let a PR push a file from under 1k lines
  to over 1k lines without a very strong reason" — the only objectively checkable criterion in either source skill
  (`findings-nuclear-review.md` §3.1).
- The user pinned the mechanism during the grill (`decisions-three-axis-review.md` §6): computation and filtering are
  done "programmatically and deterministically via a script … the script handles the computation and filtering,
  outputting a list of files that break the rule". The orchestrator runs it at step 1 and pre-seeds crossings as
  Structure findings labelled `blocker (presumptive)`; the Structure sub-agent only adds context.
- House precedent for skill scripts: `skills/skill-creator/scripts/` — Python 3, `#!/usr/bin/env python3`, module
  docstring with Usage section, stdlib only.
- The diff semantics must match the skill's review scope (durable decision 1): comparison is against the merge-base of
  `<fixed-point>` and `HEAD` (three-dot semantics), and the "after" state is `HEAD`, not the working tree.

**Script contract** (this phase's binding interface — phase 3's SKILL.md cites it):

- Invocation: `python3 skills/three-axis-review/scripts/file_size_gate.py <fixed-point>`
- Threshold: fixed at 1,000 lines. A crossing is `before ≤ 1000 and after > 1000`. New files count as `before = 0`;
  deleted files never cross.
- Output: one TSV line per crossing file to stdout — `path<TAB>before<TAB>after` — sorted by path; **empty stdout
  means no crossings**. No headers, no prose.
- Exit codes: `0` on success (with or without crossings); `2` on usage error or any git failure (unresolvable ref,
  not a repo), with the reason on stderr.
- Renames are followed (`before` is counted at the old path); binary files are skipped.
- Stdlib only; no third-party imports.

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The script

**File**: `skills/three-axis-review/scripts/file_size_gate.py`
**Change**: create the script implementing the contract above.

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

def run_git(*args) -> str:
    # subprocess.run(["git", *args], capture_output=True, text=False)
    # non-zero exit -> print stderr, sys.exit(2)
    ...

def changed_files(base: str) -> list[tuple[str, str]]:
    # git diff --name-status -M -z <base> HEAD
    # parse NUL-separated records; yield (before_path, after_path):
    #   A  -> (None, path)      M -> (path, path)
    #   D  -> skip              R<score> -> (old_path, new_path)
    ...

def line_count(rev: str, path: str) -> int | None:
    # git show <rev>:<path>  (missing -> 0 handled by caller for A)
    # blob containing b"\0" -> binary -> None (skip file)
    # else count of b"\n" (+1 if trailing partial line)
    ...

def main() -> int:
    # 1. argv check -> usage on stderr, exit 2
    # 2. base = run_git("merge-base", fixed_point, "HEAD")
    # 3. for each (before_path, after_path): before/after counts,
    #    skip binaries, collect where before <= THRESHOLD < after
    # 4. print sorted "path\tbefore\tafter" lines; return 0
    ...
```

## Success criteria

### Automated verification

- [ ] Fixture repo behaves per contract — build it once, then assert each case:

  ```bash
  FIX="$TMPDIR/fsg-fixture" && rm -rf "$FIX" && mkdir -p "$FIX" && cd "$FIX" && git init -q
  seq 900  > grows.txt          # 900 -> 1100: crossing
  seq 1100 > already-big.txt    # 1100 -> 1300: no crossing (already over)
  seq 500  > shrinks.txt        # deleted: no crossing
  seq 950  > renamed.txt        # renamed 950 -> 1050: crossing, counted across rename
  git add -A && git commit -qm base && git checkout -qb feature
  seq 1100 > grows.txt && seq 1300 > already-big.txt && git rm -q shrinks.txt
  git mv renamed.txt renamed-new.txt && seq 1050 > renamed-new.txt
  seq 1200 > brand-new.txt      # new at 1200: crossing (before = 0)
  printf 'a\0b' > binary.bin    # binary: skipped
  git add -A && git commit -qm feature
  python3 <repo>/skills/three-axis-review/scripts/file_size_gate.py main
  ```

- [ ] Output is exactly three TSV lines, sorted — `brand-new.txt 0 1200`, `grows.txt 900 1100`,
      `renamed-new.txt 950 1050` (tab-separated) — and nothing else: pipe through `diff` against an expected file.
- [ ] Exit code 0 on the fixture run: `echo $?`
- [ ] Empty output + exit 0 when nothing crosses: run against `HEAD` (`... file_size_gate.py HEAD; echo $?`)
- [ ] Exit 2 with a stderr message on a bad ref: `... file_size_gate.py no-such-ref; echo $?`
- [ ] Exit 2 on missing argument: `... file_size_gate.py; echo $?`
- [ ] Stdlib only: `grep -vE '^(import|from) (sys|os|subprocess|argparse|pathlib)' | grep -E '^(import|from)'`
      finds nothing.

### Manual verification

None

## Dependencies

- **Depends on**: None
- **Blocks**: 3
