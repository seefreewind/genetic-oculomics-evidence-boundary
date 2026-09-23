#!/usr/bin/env python3
"""Targeted, non-expansive QC audit of the locked CRAE -> CKD MR direction."""
from __future__ import annotations

import csv
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_phase2a_mr import (  # noqa: E402
    load_bim, load_manifest, load_outcome_trait, norm_chr, open_text,
    parse_num, resolve, split_line, value,
)

EXPOSURE = "ret_crae"
OUTCOME = "sys_ckd_wuttke2019"
EXPOSURE_PATH = ROOT / "data/raw/retinal/ret_crae__GCST90446763.tsv.gz.complete"
CANDIDATE_PATH = ROOT / "results/phase0/instrument_candidates/ret_crae.tsv"
CLUMP_PATH = ROOT / "results/phase0/clumping/ret_crae.clumps"
OUTDIR = ROOT / "results/phase2a1"


def complement(a: str) -> str:
    return {"A": "T", "T": "A", "C": "G", "G": "C"}.get(a, "N")


def is_pal(a: str, b: str) -> bool:
    return {a, b} in ({"A", "T"}, {"C", "G"})


def eaf_bucket(diff: float | None) -> str:
    if diff is None or not math.isfinite(diff):
        return "NA"
    if diff < 0.05:
        return "<0.05"
    if diff < 0.10:
        return "0.05-0.10"
    if diff < 0.20:
        return "0.10-0.20"
    return ">0.20"


def read_raw_gws() -> dict[str, dict[str, object]]:
    """Load the complete P<5e-8 extraction made from the original raw file.

    The Phase 0 full-file QC already streamed the original 516-MB compressed
    CRAE GWAS and wrote this exact 427-row extraction. Reusing that immutable
    extraction avoids a second multi-minute scan while preserving raw-file
    provenance in the output.
    """
    hits: dict[str, dict[str, object]] = {}
    with CANDIDATE_PATH.open(encoding="utf-8", newline="") as handle:
        for r in csv.DictReader(handle, delimiter="\t"):
            rid = (r.get("rsid") or "").strip()
            if not rid:
                continue
            hits[rid] = {
                "rsid": rid, "chrom": norm_chr(r["chromosome"]), "pos": int(float(r["position"])),
                "ea": r["effect_allele"].upper(), "oa": r["other_allele"].upper(),
                "beta": parse_num(r["beta"]), "se": parse_num(r["standard_error"]),
                "p": parse_num(r["p_value"]), "eaf": parse_num(r["effect_allele_frequency"]),
                "n": parse_num(r["sample_size"]),
            }
    return hits


def load_target_bim(ids: set[str]) -> tuple[dict[str, tuple[str, int, str, str]], dict[tuple[str, int], str]]:
    """Use ripgrep to inspect only the six locked lead SNPs in the 1KG BIM."""
    if not ids:
        return {}, {}
    pattern = "|".join(sorted(ids))
    proc = subprocess.run(["rg", "-e", pattern, str(ROOT / "data/reference/1kg_v3/EUR.bim")],
                          capture_output=True, text=True, check=False)
    by_id: dict[str, tuple[str, int, str, str]] = {}; by_coord: dict[tuple[str, int], str] = {}
    for line in proc.stdout.splitlines():
        f = line.split()
        if len(f) < 6 or f[1] not in ids:
            continue
        c, rid, pos, a1, a2 = norm_chr(f[0]), f[1], int(f[3]), f[4].upper(), f[5].upper()
        by_id[rid] = (c, pos, a1, a2); by_coord[(c, pos)] = rid
    return by_id, by_coord


def read_clump_leads() -> dict[str, dict[str, object]]:
    with CLUMP_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return {
        r["ID"]: {"chrom": norm_chr(r["#CHROM"]), "pos": int(r["POS"]), "p": parse_num(r["P"])}
        for r in rows if r.get("ID")
    }


def reference_status(ea: str, oa: str, ref_a1: str, ref_a2: str) -> str:
    pair = (ea, oa)
    ref = (ref_a1, ref_a2)
    comp = (complement(ea), complement(oa))
    if pair == ref:
        return "REF_PANEL_EXACT"
    if pair == (ref_a2, ref_a1):
        return "REF_PANEL_REVERSED"
    if comp == ref:
        return "REF_PANEL_COMPLEMENT_POSSIBLE"
    if comp == (ref_a2, ref_a1):
        return "REF_PANEL_COMPLEMENT_REVERSED_POSSIBLE"
    return "REF_PANEL_MISMATCH"


def audit_one(x: dict[str, object], y: dict[str, object] | None, bim: dict[str, tuple[str, int, str, str]]) -> dict[str, object]:
    rid = str(x["rsid"])
    ref = bim.get(rid)
    ref_chrom, ref_pos, ref_a1, ref_a2 = ref if ref else ("NA", "NA", "NA", "NA")
    out = {
        "rsid": rid, "chr_grch37": x["chrom"], "pos_grch37_exposure": x["pos"],
        "pos_grch37_outcome": y.get("pos") if y else "NA",
        "pos_grch37_1kg_reference": ref_pos,
        "exposure_effect_allele": x["ea"], "exposure_other_allele": x["oa"],
        "outcome_effect_allele": y.get("ea") if y else "NA", "outcome_other_allele": y.get("oa") if y else "NA",
        "reference_a1": ref_a1, "reference_a2": ref_a2,
        "beta_exposure": x["beta"], "se_exposure": x["se"], "p_exposure": x["p"], "eaf_exposure": x.get("eaf"),
        "beta_outcome_raw": y.get("beta") if y else "NA", "se_outcome": y.get("se") if y else "NA",
        "p_outcome": y.get("p") if y else "NA", "eaf_outcome": y.get("eaf") if y else "NA",
        "outcome_present": "YES" if y else "NO", "palindromic": "NA", "allele_orientation": "NA",
        "strand_status": "NA", "reference_panel_orientation": "NA", "build_mismatch_possibility": "NA",
        "beta_outcome_aligned": "NA", "eaf_outcome_aligned": "NA", "eaf_difference": "NA",
        "eaf_difference_bucket": "NA", "harmonisation_status": "NOT_EVALUATED", "removal_reason": "NA",
        "dbsnp_compatible_orientation": "NOT_DIRECTLY_QUERIED; 1KG_GRCh37_PROXY_ONLY",
    }
    if y is None:
        out["harmonisation_status"] = "REMOVED"
        out["removal_reason"] = "OUTCOME_VARIANT_NOT_FOUND"
        return out
    ea, oa, ya, yo = str(x["ea"]), str(x["oa"]), str(y["ea"]), str(y["oa"])
    pal = is_pal(ea, oa)
    out["palindromic"] = "YES" if pal else "NO"
    out["reference_panel_orientation"] = reference_status(ea, oa, str(ref_a1), str(ref_a2))
    out["build_mismatch_possibility"] = "NO_EVIDENCE" if (x["chrom"], x["pos"]) == (y.get("chrom"), y.get("pos")) == (str(ref_chrom), ref_pos) else "REVIEW_COORDINATES"
    ex_eaf = parse_num(x.get("eaf")); out_eaf = parse_num(y.get("eaf"))
    flip = False
    if pal:
        out["strand_status"] = "PALINDROMIC_STRAND_AMBIGUOUS"
        if ex_eaf is None or out_eaf is None or 0.42 <= float(ex_eaf) <= 0.58 or 0.42 <= float(out_eaf) <= 0.58:
            out["allele_orientation"] = "PALINDROMIC_AMBIGUOUS"
            out["harmonisation_status"] = "REMOVED"
            out["removal_reason"] = "PALINDROMIC_AMBIGUOUS"
            return out
        same = abs(float(ex_eaf) - float(out_eaf))
        rev = abs(float(ex_eaf) - (1.0 - float(out_eaf)))
        if same <= rev and same <= 0.20:
            out["allele_orientation"] = "PALINDROMIC_SAME_EAF_ORIENTATION"
        elif rev < same and rev <= 0.20:
            flip = True
            out["allele_orientation"] = "PALINDROMIC_REVERSE_EAF_ORIENTATION"
        else:
            out["allele_orientation"] = "PALINDROMIC_FREQUENCY_MISMATCH"
            out["harmonisation_status"] = "REMOVED"
            out["removal_reason"] = "PALINDROMIC_FREQUENCY_MISMATCH"
            return out
    elif ea == ya and oa == yo:
        out["allele_orientation"] = "SAME"
        out["strand_status"] = "NONPALINDROMIC_NO_STRAND_AMBIGUITY"
    elif ea == yo and oa == ya:
        flip = True
        out["allele_orientation"] = "REVERSED_REQUIRES_SIGN_FLIP"
        out["strand_status"] = "NONPALINDROMIC_NO_STRAND_AMBIGUITY"
    else:
        out["allele_orientation"] = "INCOMPATIBLE"
        out["strand_status"] = "UNRESOLVED_ALLELE_ORIENTATION"
        out["harmonisation_status"] = "REMOVED"
        out["removal_reason"] = "INCOMPATIBLE_ALLELES;UNRESOLVED_ALLELE_ORIENTATION"
        return out
    aligned_eaf = (1.0 - float(out_eaf)) if (flip and out_eaf is not None) else out_eaf
    diff = abs(float(ex_eaf) - float(aligned_eaf)) if ex_eaf is not None and aligned_eaf is not None else None
    out["beta_outcome_aligned"] = -float(y["beta"]) if flip else float(y["beta"])
    out["eaf_outcome_aligned"] = aligned_eaf if aligned_eaf is not None else "NA"
    out["eaf_difference"] = diff if diff is not None else "NA"
    out["eaf_difference_bucket"] = eaf_bucket(diff)
    if diff is not None and diff > 0.20:
        out["harmonisation_status"] = "REMOVED"
        out["removal_reason"] = "EAF_MISMATCH"
    elif out["reference_panel_orientation"] in {"REF_PANEL_MISMATCH", "REF_PANEL_COMPLEMENT_POSSIBLE", "REF_PANEL_COMPLEMENT_REVERSED_POSSIBLE"}:
        out["harmonisation_status"] = "UNRESOLVED"
        out["removal_reason"] = "UNRESOLVED_ALLELE_ORIENTATION"
    else:
        out["harmonisation_status"] = "RETAINED_PRIMARY"
        out["removal_reason"] = "NONE"
    return out


def steiger_single(row: dict[str, object]) -> dict[str, object]:
    p = float(row["eaf_exposure"])
    bx = float(row["beta_exposure"]); by = float(row["beta_outcome_aligned"])
    r2x = 2 * p * (1 - p) * bx * bx
    r2y = 2 * p * (1 - p) * by * by
    n_exp = 65015.0
    cases = 41395.0; controls = 439303.0
    n_out_eff = 4.0 / (1.0 / cases + 1.0 / controls)
    rx = min(math.sqrt(r2x), 0.999999); ry = min(math.sqrt(r2y), 0.999999)
    z = (math.atanh(rx) - math.atanh(ry)) / math.sqrt(1 / (n_exp - 3) + 1 / (n_out_eff - 3))
    return {
        "variance_explained_exposure": r2x, "variance_explained_outcome": r2y,
        "n_exposure_assumed": n_exp, "n_outcome_cases": cases, "n_outcome_controls": controls,
        "n_outcome_effective": n_out_eff, "binary_outcome_scale": "effective N=4/(1/cases+1/controls); r2=2*p*(1-p)*beta^2",
        "prevalence_assumption": "not separately used; case/control effective-N approximation",
        "steiger_direction": "TRUE" if rx > ry else "FALSE",
        "steiger_p": 2 * norm.sf(abs(z)),
    }


def write_tsv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    raw = read_raw_gws()
    leads = read_clump_leads()
    bim, by_coord = load_target_bim(set(leads))
    reconstruction = []
    for rid, x in sorted(raw.items(), key=lambda kv: (str(kv[1]["chrom"]), int(kv[1]["pos"]), kv[0])):
        selected = rid in leads
        reconstruction.append({
            "rsid": rid, "chr": x["chrom"], "pos": x["pos"],
            "effect_allele_exposure": x["ea"], "other_allele_exposure": x["oa"],
            "beta_exposure": x["beta"], "se_exposure": x["se"], "p_exposure": x["p"],
            "eaf_exposure": x["eaf"], "F_stat": (float(x["beta"]) / float(x["se"])) ** 2,
            "clumped": "YES" if selected else "NO",
            "reason_removed": "NONE" if selected else "LD_CLUMPED_OUT",
        })
    write_tsv(reconstruction, OUTDIR / "CRAE_INSTRUMENT_RECONSTRUCTION.tsv")
    if len(raw) != 427 or len(leads) != 6:
        raise RuntimeError(f"Unexpected reconstruction counts: raw_gws={len(raw)} clumped_leads={len(leads)}")

    manifest = load_manifest()
    ckd_path = manifest.get(OUTCOME)
    if ckd_path is None:
        raise RuntimeError("Locked CKD file is missing from the local manifest")
    requests = set(leads); coords = {(str(raw[r]["chrom"]), int(raw[r]["pos"])) for r in leads if r in raw}
    outcome = load_outcome_trait(OUTCOME, ckd_path, requests, coords, 480698.0)
    trace = []
    for rid in sorted(leads):
        x = raw[rid]
        y = outcome.get(rid) or outcome.get(f"coord:{x['chrom']}:{x['pos']}")
        trace.append(audit_one(x, y, bim))
    write_tsv(trace, OUTDIR / "CRAE_CKD_IV_TRACE.tsv")

    retained = [r for r in trace if r["harmonisation_status"] == "RETAINED_PRIMARY"]
    for r in trace:
        if r in retained:
            r.update(steiger_single(r))
    if len(retained) == 1:
        r = retained[0]
        bx, sx = float(r["beta_exposure"]), float(r["se_exposure"])
        by, sy = float(r["beta_outcome_aligned"]), float(r["se_outcome"])
        ratio = by / bx
        se = math.sqrt(sy ** 2 / bx ** 2 + by ** 2 * sx ** 2 / bx ** 4)
        summary = {
            "direction": "ret_crae_to_sys_ckd_wuttke2019", "snp": r["rsid"],
            "beta_crae": bx, "se_crae": sx, "beta_ckd_aligned": by, "se_ckd": sy,
            "F_stat": (bx / sx) ** 2, "wald_ratio": ratio, "wald_se": se,
            "ci_low": ratio - 1.95996398454 * se, "ci_high": ratio + 1.95996398454 * se,
            "wald_p": 2 * norm.sf(abs(ratio / se)), "allele_orientation": r["allele_orientation"],
            "eaf_exposure": r["eaf_exposure"], "eaf_outcome_aligned": r["eaf_outcome_aligned"],
            "eaf_difference": r["eaf_difference"], "steiger_direction": r["steiger_direction"],
            "steiger_p": r["steiger_p"], "variance_explained_exposure": r["variance_explained_exposure"],
            "variance_explained_outcome": r["variance_explained_outcome"],
            "pleiotropy_annotation": "NOT_RUN_NO_LOCAL_LEGAL_ANNOTATION_RESOURCE",
            "status": "SINGLE_IV_UNRESOLVED",
        }
    else:
        summary = {"direction": "ret_crae_to_sys_ckd_wuttke2019", "status": "NULL_AFTER_QC", "retained_iv_count": len(retained)}
    write_tsv([summary], OUTDIR / "CRAE_CKD_SINGLE_IV_SUMMARY.tsv")
    write_tsv([{"status": "NO_VALID_INDEPENDENT_CKD_REPLICATION_DATASET", "dataset": "NA", "reason": "Only the locked CKDGen European discovery file is locally available; no independent pre-existing compatible CKD dataset was admitted under this amendment."}], OUTDIR / "CRAE_CKD_REPLICATION.tsv")
    print(f"raw_gws={len(raw)} clumped_leads={len(leads)} outcome_rows={sum(r['outcome_present']=='YES' for r in trace)} retained={len(retained)}")


if __name__ == "__main__":
    main()
