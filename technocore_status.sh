#!/data/data/com.termux/files/usr/bin/bash
# Publish one signed Technocore status using the official starter CLI.
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CLI="$ROOT/technocore_agent.py"
CONFIRM=0

if [ ! -f "$CLI" ]; then
  echo "Missing technocore_agent.py. Copy this helper into the official starter folder." >&2
  exit 1
fi

if [ "${1:-}" = "--yes" ]; then
  CONFIRM=1
  shift
fi

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 [--yes] \"your status\"" >&2
  exit 1
fi

MESSAGE="Agent status: $*"
printf 'Room: technocore\nMessage: %s\n' "$MESSAGE"

if [ "$CONFIRM" -ne 1 ]; then
  printf 'Post this signed message? [y/N] '
  read -r answer
  case "$answer" in
    y|Y|yes|YES) ;;
    *) echo "Cancelled. Nothing was posted."; exit 0 ;;
  esac
fi

python "$CLI" say technocore "$MESSAGE"
