#!/usr/bin/env python3
"""Amendment 005: frozen-row CAD exclusion and prespecified BH recalculation.

No GWAS, LDSC, local correlation, MR, clumping or Steiger estimator is run.
The protocol lock must exist and all primary inputs must match their pre-state
SHA-256 digests before any sensitivity output is written.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/amendment005"
CAD = "sys_cad_nikpay2015"
EXPECTED = {
    "archive/pre_amendment005/HMG_MANUSCRIPT_FINAL_POLISHED.md": "c98331f27fe4cc9a383d164e73d5044fc6519173de17c28226013bc6d375b294",
    "results/ldsc/GENETIC_CORRELATION_MASTER.tsv": "72d0956d7bb9a437833aff1d433791ecc47611119b9b66dcfe862569e4f97b21",
    "results/phase1b/HDLL_LOCAL_RG_MASTER.tsv": "6a9b7846d212ff4b8beddd7be503d2bd542c539fec90f22dfff89d72adb01bff",
    "results/phase1b/LAVA_LOCAL_RG_MASTER.tsv": "772ecfc4cc1abfbb4ce2fd86c9791bf5a82d4238ef554ffb21f164511495a19f",
    "results/phase1b_audit/LAVA_NATIVE_PVALUE_COMPARISON.tsv": "229374847b53b326d4cfe4a61d38c4782aa06953fdaadb006618aa4634263606",
    "results/amendment004/MR_DIRECTIONAL_MASTER_OCT_ONLY.tsv": "626d8267beccfc0ebed8ce0a9e8731e348f81d0a9441913b871001df182a0ab9",
    "config/phenotype_registry.tsv": "55958c7d572476729570b9b7db7273605ac9204ee20a264cd1fe03957b767577",
}
PROTOCOL_SHA256 = "ef364bada8a2d50839dcdb3a69dd63845d2f1d1278fa564ad1723d0481ad3b10"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check_lock() -> None:
    lock = ROOT / "config/amendment_005_cad_sensitivity.yaml"
    sha_file = ROOT / "config/AMENDMENT005.sha256"
    if digest(lock) != PROTOCOL_SHA256:
        raise RuntimeError("HOLD_PROTOCOL_LOCK_CHANGED")
    if sha_file.read_text(encoding="utf-8").split()[0] != PROTOCOL_SHA256:
        raise RuntimeError("HOLD_PROTOCOL_DIGEST_CHANGED")
    for rel, wanted in EXPECTED.items():
        if digest(ROOT / rel) != wanted:
            raise RuntimeError(f"HOLD_FROZEN_INPUT_CHANGED: {rel}")


def bh(values: pd.Series) -> pd.Series:
    p = pd.to_numeric(values, errors="coerce").to_numpy(dtype=float)
    out = np.full(len(p), np.nan)
    valid = np.isfinite(p)
    if not valid.any():
        return pd.Series(out, index=values.index)
    if ((p[valid] < 0) | (p[valid] > 1)).any():
        raise RuntimeError("HOLD_INVALID_P_VALUE")
    pos = np.flatnonzero(valid)
    order = pos[np.argsort(p[valid], kind="stable")]
    ranked = p[order] * len(order) / np.arange(1, len(order) + 1)
    out[order] = np.minimum(np.minimum.accumulate(ranked[::-1])[::-1], 1.0)
    return pd.Series(out, index=values.index)


def check_old_q(frame: pd.DataFrame, p_col: str, q_col: str, label: str) -> None:
    expected = bh(frame[p_col]).to_numpy(dtype=float)
    actual = pd.to_numeric(frame[q_col], errors="coerce").to_numpy(dtype=float)
    if not np.allclose(expected, actual, rtol=1e-8, atol=1e-10, equal_nan=True):
        bad = np.flatnonzero(~np.isclose(expected, actual, rtol=1e-8, atol=1e-10, equal_nan=True))
        raise RuntimeError(f"HOLD_OLD_Q_MISMATCH:{label}:{len(bad)}")


def read_split(path: str, group_col: str, expected_total: int, expected_cad: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(ROOT / path, sep="\t", low_memory=False)
    if len(frame) != expected_total:
        raise RuntimeError(f"HOLD_SOURCE_COUNT:{path}:{len(frame)}")
    if group_col not in frame:
        raise RuntimeError(f"HOLD_GROUP_COLUMN:{path}:{group_col}")
    is_cad = frame[group_col].eq(CAD)
    if int(is_cad.sum()) != expected_cad:
        raise RuntimeError(f"HOLD_CAD_COUNT:{path}:{int(is_cad.sum())}")
    if frame[group_col].isna().any():
        raise RuntimeError(f"HOLD_MISSING_DISEASE:{path}")
    return frame, frame.loc[~is_cad].copy().reset_index(drop=True)


def numeric_equal(left: pd.Series, right: pd.Series) -> bool:
    x = pd.to_numeric(left, errors="coerce").to_numpy(dtype=float)
    y = pd.to_numeric(right, errors="coerce").to_numpy(dtype=float)
    return np.allclose(x, y, rtol=0, atol=0, equal_nan=True)


def prepare(
    frame: pd.DataFrame,
    non_cad: pd.DataFrame,
    p_col: str,
    old_q_col: str,
    new_q_col: str,
    label: str,
) -> pd.DataFrame:
    check_old_q(frame, p_col, old_q_col, label)
    out = non_cad.copy()
    out[f"old_{old_q_col}"] = pd.to_numeric(out[old_q_col], errors="coerce")
    out[new_q_col] = bh(out[p_col])
    out["old_status"] = np.where(pd.to_numeric(out[old_q_col], errors="coerce") < 0.05, "FDR_POSITIVE", "NOT_FDR_POSITIVE")
    out["leave_CAD_out_status"] = np.where(out[new_q_col] < 0.05, "FDR_POSITIVE", "NOT_FDR_POSITIVE")
    if not numeric_equal(out[p_col], non_cad[p_col]):
        raise RuntimeError(f"HOLD_P_CHANGED:{label}")
    return out


def write(frame: pd.DataFrame, name: str) -> None:
    frame.to_csv(OUT / name, sep="\t", index=False, na_rep="NA")


def main() -> None:
    check_lock()
    ldsc, ldsc_nc = read_split("results/ldsc/GENETIC_CORRELATION_MASTER.tsv", "systemic_disease", 112, 14)
    hdll, hdll_nc = read_split("results/phase1b/HDLL_LOCAL_RG_MASTER.tsv", "systemic_disease", 116472, 17346)
    lava, lava_nc = read_split("results/phase1b/LAVA_LOCAL_RG_MASTER.tsv", "systemic_disease", 26639, 3660)
    native, native_nc = read_split("results/phase1b_audit/LAVA_NATIVE_PVALUE_COMPARISON.tsv", "systemic_disease", 26639, 3660)
    mr, mr_nc = read_split("results/amendment004/MR_DIRECTIONAL_MASTER_OCT_ONLY.tsv", "disease", 112, 14)
    if len(ldsc_nc) != 98 or len(hdll_nc) != 99126 or len(lava_nc) != 22979 or len(native_nc) != 22979 or len(mr_nc) != 98:
        raise RuntimeError("HOLD_REMAINING_FAMILY_COUNT")
    admitted = pd.read_csv(ROOT / "config/phase1b_pair_admission.tsv", sep="\t")
    if int(admitted["admit_phase1b"].astype(str).str.upper().eq("TRUE").sum()) != 47:
        raise RuntimeError("HOLD_ADMITTED_PAIR_COUNT")
    if int((admitted["systemic_disease"].eq(CAD) & admitted["admit_phase1b"].astype(str).str.upper().eq("TRUE")).sum()) != 7:
        raise RuntimeError("HOLD_CAD_ADMITTED_PAIR_COUNT")

    ldsc_out = prepare(ldsc, ldsc_nc, "p", "q_global", "new_q_98", "LDSC")
    ldsc_out["old_q_112"] = ldsc_out["q_global"]
    hdll_out = prepare(hdll, hdll_nc, "p_local_rg", "q_global_local", "new_q_global_local", "HDLL")
    lava_out = prepare(lava, lava_nc, "p", "q_lava_global", "new_q_initial_global", "LAVA_INITIAL")
    native_out = prepare(native, native_nc, "native_lava_p", "native_q", "new_q_native_global", "LAVA_NATIVE")
    mr_out = prepare(mr, mr_nc, "p", "q_amendment004_global", "new_q_98", "MR")
    mr_out["pair"] = mr_out["pair_id"]
    mr_out["old_q_112"] = mr_out["q_amendment004_global"]

    # Summaries only count frozen-row diagnostics; no rho or CI is estimated.
    lower = pd.to_numeric(native_out["rho_lower"], errors="coerce")
    upper = pd.to_numeric(native_out["rho_upper"], errors="coerce")
    raw = pd.to_numeric(native_out["raw_rho"], errors="coerce")
    masks = {
        "CI_TOUCHES_OR_EXCEEDS_ABS_RHO_ONE": (lower <= -1) | (upper >= 1),
        "RAW_ABS_RHO_GT_ONE": raw.abs() > 1,
        "RAW_ABS_RHO_GT_ONE_POINT_TWO_FIVE": raw.abs() > 1.25,
    }
    boundary = pd.DataFrame(
        {
            "metric": list(masks),
            "count_all_remaining_rows": [int(m.sum()) for m in masks.values()],
            "denominator_all_remaining_rows": len(native_out),
            "count_native_FDR_positive_rows": [int((m & (native_out["new_q_native_global"] < 0.05)).sum()) for m in masks.values()],
            "native_FDR_positive_denominator": int((native_out["new_q_native_global"] < 0.05).sum()),
        }
    )

    OUT.mkdir(parents=True, exist_ok=True)
    write(ldsc_out, "LDSC_LEAVE_CAD_OUT_98.tsv")
    write(hdll_out, "HDLL_LEAVE_CAD_OUT.tsv")
    write(lava_out, "LAVA_INITIAL_APPROX_LEAVE_CAD_OUT.tsv")
    write(native_out, "LAVA_NATIVE_LEAVE_CAD_OUT.tsv")
    write(boundary, "LAVA_LEAVE_CAD_OUT_BOUNDARY_SUMMARY.tsv")
    write(mr_out, "MR_LEAVE_CAD_OUT_98.tsv")
    for name, old, new in [
        ("LDSC", ldsc_out["q_global"], ldsc_out["new_q_98"]),
        ("HDLL", hdll_out["q_global_local"], hdll_out["new_q_global_local"]),
        ("LAVA_INITIAL", lava_out["q_lava_global"], lava_out["new_q_initial_global"]),
        ("LAVA_NATIVE", native_out["native_q"], native_out["new_q_native_global"]),
        ("MR", mr_out["q_amendment004_global"], mr_out["new_q_98"]),
    ]:
        print(f"{name}\tremaining={len(new)}\told_positive_remaining={int((old < 0.05).sum())}\tnew_positive={int((new < 0.05).sum())}", flush=True)


if __name__ == "__main__":
    main()
