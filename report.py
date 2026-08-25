#!/usr/bin/env python3
"""Render the local public evidence log as Markdown."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Technocore evidence as Markdown")
    parser.add_argument("--input", type=Path, default=Path.home() / ".technocore" / "evidence.json")
    parser.add_argument("--output", type=Path, default=Path("technocore-contribution-report.md"))
    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"Evidence file not found: {args.input}")
    records = json.loads(args.input.read_text(encoding="utf-8"))
    lines = ["# Technocore Contribution Report", "", "Public evidence only. No private identity material is included.", ""]
    for index, item in enumerate(records, 1):
        lines += [
            f"## {index}. {item['title']}",
            "",
            f"- URL: {item['url']}",
            f"- Description: {item['description']}",
            f"- Room: `{item['room']}`",
            f"- Sequence: `{item['sequence']}`",
            f"- DID: `{item['did']}`",
            f"- Nonce: `{item['nonce']}`",
            f"- Recorded: `{item['recorded_at']}`",
            "",
        ]
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
