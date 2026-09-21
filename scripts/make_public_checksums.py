#!/usr/bin/env python3
"""Write SHA256 checksums for every tracked public-release file."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "PUBLIC_RELEASE_SHA256.tsv"
excluded = {".git", "PUBLIC_RELEASE_SHA256.tsv"}
files = [
    p for p in ROOT.rglob("*")
    if p.is_file() and not any(part in excluded for part in p.parts)
]
rows = []
for path in sorted(files):
    rows.append(
        f"{path.relative_to(ROOT)}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\t{path.stat().st_size}"
    )
OUT.write_text("path\tsha256\tbytes\n" + "\n".join(rows) + "\n", encoding="utf-8")
print(OUT)
