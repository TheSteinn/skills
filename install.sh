#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="$HOME/.agents/skills"

mkdir -p "$DEST_DIR"

for skill_dir in "$SCRIPT_DIR"/*/; do
  skill_name="$(basename "$skill_dir")"
  if [ "$skill_name" = ".git" ] || [ "$skill_name" = ".idea" ]; then
    continue
  fi
  echo "--- Installing: $skill_name ---"
  rsync -av --delete "$skill_dir" "$DEST_DIR/$skill_name"
  echo "Installed skill: $skill_name"
  echo
done

echo "All skills installed to $DEST_DIR"