#!/usr/bin/env python3
"""Write SHA256 checksums for project code/config/report/result artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/phase0/ARTIFACT_SHA256.tsv"
INCLUDED = [
    "README.md", "PROJECT_STATUS.md", "environment.yml", "config", "scripts",
    "reports", "results/phase0", "metadata", "data/raw/PARTIAL_DOWNLOADS.tsv",
    "data/reference/1kg_v3_manifest.tsv", "results/ldsc/GENETIC_CORRELATION_MASTER.tsv",
    "results/ldsc/phase1A_rg_heatmap_plotting.tsv", "results/ldsc/phase1A",
    "results/phase1b", "results/phase1b2", "results/phase2a1",
    "data/reference/lava_ukb100k", "figures/phase1b", "logs/phase1b_hdll",
    "figures/phase1A_rg_heatmap.pdf", "figures/phase1A_rg_heatmap.png",
    "manuscript", "manuscript/human_genetics", "figures/manuscript", "figures/human_genetics",
    "tables/manuscript", "tables/human_genetics", "supplement", "supplement/human_genetics",
    "manuscript/hmg", "figures/hmg", "tables/hmg", "supplement/hmg",
    "logs/PHASE1A_COMMANDS.md", "logs/PHASE1B_COMMANDS.md", "data/reference/hdll_manifest.tsv",
]

files: list[Path] = []
for item in INCLUDED:
    path = ROOT / item
    if path.is_file():
        files.append(path)
    elif path.is_dir():
        files.extend(
            p for p in path.rglob("*")
            if p.is_file() and p != OUT and not p.name.startswith("._") and "__pycache__" not in p.parts
        )

rows = []
for path in sorted(set(files)):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(f"{path.relative_to(ROOT)}\t{digest}\t{path.stat().st_size}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("path\tsha256\tbytes\n" + "\n".join(rows) + "\n", encoding="utf-8")
print(OUT)
