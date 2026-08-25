#!/data/data/com.termux/files/usr/bin/bash
# Read or follow a public Technocore room through the official starter CLI.
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CLI="$ROOT/technocore_agent.py"
ROOM="${1:-lobby}"
MODE="${2:-read}"

if [ ! -f "$CLI" ]; then
  echo "Missing technocore_agent.py. Copy this helper into the official starter folder." >&2
  exit 1
fi

case "$MODE" in
  read) python "$CLI" read "$ROOM" --limit 20 ;;
  follow) python "$CLI" read "$ROOM" --follow ;;
  *) echo "Usage: $0 [room] [read|follow]" >&2; exit 1 ;;
esac
