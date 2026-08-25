#!/usr/bin/env python3
"""Run safe local checks before using the Technocore helpers."""
from __future__ import annotations

import argparse
import os
import stat
from pathlib import Path


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'OK' if ok else 'WARN'}] {label}: {detail}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a local Technocore Termux setup")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Folder containing technocore_agent.py")
    args = parser.parse_args()
    root = args.path.expanduser().resolve()
    good = True

    good &= check("Python", True, "running")
    cli = root / "technocore_agent.py"
    good &= check("Starter CLI", cli.is_file(), str(cli) if cli.is_file() else "technocore_agent.py is missing")
    identity = root / "identity.pem"
    if identity.exists():
        mode = stat.S_IMODE(identity.stat().st_mode)
        good &= check("Identity file", mode & 0o077 == 0, f"permissions {oct(mode)} (private)" if mode & 0o077 == 0 else f"permissions {oct(mode)} are too broad; run chmod 600 identity.pem")
    else:
        check("Identity file", True, "not found here (safe for this toolkit folder)")

    risky = []
    for p in root.rglob('*'):
        # identity.pem is expected in the official starter folder; its
        # permissions are checked above. Ignore the virtual environment,
        # whose dependency certificates are not project secrets.
        rel = p.relative_to(root)
        if ".venv" in rel.parts:
            continue
        # Other private-looking files are unexpected and should not be
        # published with the toolkit.
        if p.is_file() and p.name != "identity.pem" and (p.suffix.lower() in {'.pem', '.key'} or p.name in {'.env', '.env.local'}):
            risky.append(str(rel))
    good &= check("Private-file scan", not risky, "none found" if not risky else ", ".join(risky))
    gitignore = root / ".gitignore"
    good &= check("Git ignore", gitignore.is_file(), "present" if gitignore.is_file() else "missing .gitignore")
    print("Ready for manual, reviewed use." if good else "Fix the WARN items before publishing or posting.")
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
