#!/usr/bin/env python3
"""Local contribution evidence log. Never stores passphrases or private keys."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_FILE = Path.home() / ".technocore" / "evidence.json"


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Evidence file must contain a JSON list")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Store public Technocore contribution evidence locally")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--url", required=True, help="Public contribution URL")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--room", default="technocore")
    parser.add_argument("--sequence", required=True, type=int)
    parser.add_argument("--did", required=True)
    parser.add_argument("--nonce", required=True)
    args = parser.parse_args()

    if not args.did.startswith("did:key:"):
        parser.error("--did must be a public did:key identity")
    if "identity.pem" in str(args.url).lower() or "identity.pem" in args.description.lower():
        parser.error("Private identity filenames are not allowed in evidence")

    path = args.file.expanduser()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    records = load(path)
    records.append({
        "title": args.title,
        "description": args.description,
        "url": args.url,
        "room": args.room,
        "sequence": args.sequence,
        "did": args.did,
        "nonce": args.nonce,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    })
    path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)
    print(f"Saved public evidence to {path}")


if __name__ == "__main__":
    main()
