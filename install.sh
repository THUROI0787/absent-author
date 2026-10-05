#!/usr/bin/env bash
# Install the Absent Author skills.
#   ./install.sh              -> ~/.claude/skills/            (Claude Code, global)
#   ./install.sh --project    -> ./.claude/skills/ of the current directory
#   ./install.sh --codex      -> ${CODEX_HOME:-~/.codex}/skills/
#   ./install.sh --dest DIR   -> DIR
#   add --link to symlink instead of copy (updates follow `git pull`)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude/skills"; MODE=copy
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) DEST="$(pwd)/.claude/skills" ;;
    --codex) DEST="${CODEX_HOME:-$HOME/.codex}/skills" ;;
    --dest) shift; DEST="$1" ;;
    --link) MODE=link ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done
mkdir -p "$DEST"
for s in paper-author-pass paper-slop-screen; do
  if [[ -e "$DEST/$s" || -L "$DEST/$s" ]]; then echo "replacing existing $DEST/$s"; fi
  rm -rf "${DEST:?}/$s"
  if [[ $MODE == link ]]; then ln -s "$HERE/skills/$s" "$DEST/$s"; else cp -R "$HERE/skills/$s" "$DEST/$s"; fi
  echo "installed $s -> $DEST/$s ($MODE)"
done
echo "Done. In your agent: \"Use paper-author-pass on paper/ in audit mode\" or \"Use paper-slop-screen to triage this preprint\"."
