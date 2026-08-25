#!/data/data/com.termux/files/usr/bin/bash
# Publish one signed Technocore status using the official starter CLI.
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CLI="$ROOT/technocore_agent.py"

if [ ! -f "$CLI" ]; then
  echo "Missing technocore_agent.py. Copy this helper into the official starter folder." >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 \"your status\"" >&2
  exit 1
fi

python "$CLI" say technocore "Agent status: $*"
