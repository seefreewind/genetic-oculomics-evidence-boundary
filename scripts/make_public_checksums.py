#!/usr/bin/env python3
"""Write SHA256 checksums for every tracked public-release file."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "PUBLIC_RELEASE_SHA256.tsv"
excluded_files = {"PUBLIC_RELEASE_SHA256.tsv"}
files = []
for current, dirs, names in os.walk(ROOT):
    dirs[:] = [name for name in dirs if name != ".git"]
    for name in names:
        if name not in excluded_files and not name.startswith("._"):
            files.append(Path(current) / name)
rows = []
for path in sorted(files):
    rows.append(
        f"{path.relative_to(ROOT)}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\t{path.stat().st_size}"
    )
OUT.write_text("path\tsha256\tbytes\n" + "\n".join(rows) + "\n", encoding="utf-8")
print(OUT)
