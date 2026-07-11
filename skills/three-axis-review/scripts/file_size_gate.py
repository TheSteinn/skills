#!/usr/bin/env python3
"""Report files a branch pushes past 1,000 lines.

Compares each changed file's line count at the merge-base of <fixed-point>
and HEAD against its line count at HEAD. Prints one TSV line per file that
crosses the threshold: path<TAB>before<TAB>after. Empty output = no crossings.

Usage:
    python3 file_size_gate.py <fixed-point>

Exit codes: 0 success; 2 usage or git error.
"""

import subprocess
import sys

THRESHOLD = 1000
CHUNK_SIZE = 64 * 1024


def run_git(*args: str) -> bytes:
    """Run a git command and return its stdout as bytes.

    On any git failure, prints the reason to stderr and exits the
    process with code 2 — callers never see a failed command.
    """
    result = subprocess.run(["git", *args], capture_output=True)
    if result.returncode != 0:
        reason = result.stderr.decode(errors="replace").strip()
        print(f"git {args[0]} failed: {reason}", file=sys.stderr)
        sys.exit(2)
    return result.stdout


def parse_name_status(raw: bytes) -> list[tuple[bytes | None, bytes]]:
    """Parse raw `git diff --name-status -z` output into (before, after) pairs.

    Paths stay bytes; a None before marks a file counted from zero. Records:
    additions and copies emit (None, path) — copies surface as adds at the
    destination; deletions are omitted; renames pair the old path with the
    new; any other status is treated as a modification at the after path.
    """
    tokens = raw.split(b"\0")
    if tokens and tokens[-1] == b"":
        tokens.pop()
    pairs: list[tuple[bytes | None, bytes]] = []
    i = 0
    while i < len(tokens):
        status = tokens[i]
        if status.startswith(b"R"):
            pairs.append((tokens[i + 1], tokens[i + 2]))
            i += 3
            continue
        if status.startswith(b"C"):  # C<score>\0src\0dst\0: an add at dst
            pairs.append((None, tokens[i + 2]))
            i += 3
            continue
        path = tokens[i + 1]
        i += 2
        if status == b"A":
            pairs.append((None, path))
        elif status == b"D":
            continue
        else:  # M, T, and anything else: treat as modify at the after path
            pairs.append((path, path))
    return pairs


def changed_files(base: str) -> list[tuple[bytes | None, bytes]]:
    """List files changed between `base` and HEAD as (before_path, after_path).

    Paths are bytes exactly as git reports them — no encoding is assumed.
    A None before_path marks a file counted from zero; see
    `parse_name_status` for the per-status record semantics.
    """
    return parse_name_status(run_git("diff", "--name-status", "-M", "-z", base, "HEAD"))


def line_count(rev: str, path: bytes) -> int | None:
    """Count lines of `path` (bytes) at `rev`, or None if the blob is binary.

    Streams the blob in fixed-size chunks rather than holding it in memory.
    A file is binary when its blob contains a NUL byte anywhere — the whole
    blob is scanned, not just a leading window; on the first NUL the git
    process is stopped and None is returned. A non-empty file without a
    trailing newline still counts its final line. On git failure, prints
    the reason to stderr and exits the process with code 2.
    """
    with subprocess.Popen(
        ["git", "show", rev.encode() + b":" + path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as proc:
        count = 0
        last = b""
        while chunk := proc.stdout.read(CHUNK_SIZE):
            if b"\0" in chunk:
                proc.kill()
                proc.wait()
                return None
            count += chunk.count(b"\n")
            last = chunk[-1:]
        stderr = proc.stderr.read()
        if proc.wait() != 0:
            reason = stderr.decode(errors="replace").strip()
            print(f"git show failed: {reason}", file=sys.stderr)
            sys.exit(2)
    if last and last != b"\n":
        count += 1
    return count


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: file_size_gate.py <fixed-point>", file=sys.stderr)
        return 2
    fixed_point = sys.argv[1]
    base = run_git("merge-base", fixed_point, "HEAD").decode().strip()
    crossings: list[tuple[bytes, int, int]] = []
    for before_path, after_path in changed_files(base):
        before = 0 if before_path is None else line_count(base, before_path)
        after = line_count("HEAD", after_path)
        if before is None or after is None:
            continue
        if before <= THRESHOLD < after:
            crossings.append((after_path, before, after))
    for path, before, after in sorted(crossings):
        sys.stdout.buffer.write(b"%s\t%d\t%d\n" % (path, before, after))
    return 0


if __name__ == "__main__":
    sys.exit(main())
