#!/usr/bin/env python3
# Owner-Skill: .claude/skills/scripts-infra/SKILL.md
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path.cwd().resolve()
    source = root / "base.mk"
    if not source.exists():
        return 1
    source_hash = _sha256(source)
    mismatched: list[Path] = []
    checked = 0
    for pyproject in sorted(root.glob("*/pyproject.toml")):
        local_base = pyproject.parent / "base.mk"
        if not local_base.exists():
            continue
        checked += 1
        if _sha256(local_base) != source_hash:
            mismatched.append(local_base.relative_to(root))
    if mismatched:
        for _path in mismatched:
            pass
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
