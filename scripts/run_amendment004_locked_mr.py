#!/usr/bin/env python3
"""Execute Amendment 004 MR after canonical comparison to the frozen dry run."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_amendment004_oct_mr as locked  # noqa: E402
import run_phase2a_mr as legacy  # noqa: E402


def verify_lock(frozen: pd.DataFrame, current: pd.DataFrame) -> None:
    if list(frozen.columns) != list(current.columns) or len(frozen) != len(current):
        raise RuntimeError("HOLD_HARMONISATION_QC: dry-run shape/columns changed")
    numeric = [
        "pos", "exposure_source_frequency", "outcome_source_frequency",
        "exposure_standardized_EAF", "outcome_standardized_EAF", "aligned_outcome_EAF", "delta_EAF",
    ]
    boolean = ["palindromic", "strand_flip", "allele_flip", "retained"]
    categorical = [c for c in frozen.columns if c not in numeric + boolean]
    for col in categorical:
        left = frozen[col].fillna("NA").astype(str).to_numpy()
        right = current[col].fillna("NA").astype(str).to_numpy()
        if not np.array_equal(left, right):
            idx = int(np.where(left != right)[0][0])
            raise RuntimeError(f"HOLD_HARMONISATION_QC: categorical mismatch {col} row {idx}: {left[idx]} != {right[idx]}")
    for col in boolean:
        def norm(series):
            return series.map(lambda x: str(x).strip().lower() in {"true", "1", "yes"}).to_numpy()
        if not np.array_equal(norm(frozen[col]), norm(current[col])):
            raise RuntimeError(f"HOLD_HARMONISATION_QC: boolean mismatch {col}")
    for col in numeric:
        left = pd.to_numeric(frozen[col], errors="coerce").to_numpy(float)
        right = pd.to_numeric(current[col], errors="coerce").to_numpy(float)
        if not np.allclose(left, right, rtol=1e-12, atol=1e-12, equal_nan=True):
            raise RuntimeError(f"HOLD_HARMONISATION_QC: numeric mismatch {col}")


def main() -> None:
    if not (locked.CONFIG / "AMENDMENT004_HARMONISATION_LOCK.sha256").exists():
        raise RuntimeError("HOLD_HARMONISATION_QC: lock missing")
    retinal, registry, semantics, bim, leads, source_rows = locked.prepare()
    audit, harmonised = locked.all_harmonisations(retinal, registry, semantics, bim, leads, source_rows)
    frozen = pd.read_csv(locked.OUT / "HARMONISATION_DRY_RUN_112.tsv", sep="\t")
    current = audit[list(frozen.columns)].copy()
    verify_lock(frozen, current)
    print("canonical_lock_comparison=PASS", flush=True)

    records, instrument_rows = [], []
    for ret in retinal:
        for disease in locked.SYSTEMIC:
            pair = f"{ret}__{disease}"
            for exposure, outcome in ((ret, disease), (disease, ret)):
                direction = f"{exposure}_to_{outcome}"
                rows = harmonised[(pair, direction)]
                result = locked.estimate_direction(exposure, outcome, rows, registry)
                result.update({"pair_id": pair, "direction": direction, "retinal_trait": ret, "disease": disease,
                               "n_iv_initial": len(leads[exposure]), "frequency_semantics": semantics[exposure]["frequency_represents"]})
                records.append(result)
                instrument_rows.extend(rows)
    df = pd.DataFrame(records)
    df["q_amendment004_global"] = legacy.bh(df["p"])
    harm_path = locked.OUT / "MR_HARMONIZED_INSTRUMENTS_OCT_ONLY.tsv"
    pd.DataFrame(instrument_rows).to_csv(harm_path, sep="\t", index=False, na_rep="NA")
    import subprocess
    subprocess.run(["Rscript", str(ROOT / "scripts/run_phase2a_mrpresso.R"), str(harm_path), str(locked.OUT / "MR_PRESSO_OCT_ONLY.tsv")], cwd=ROOT, check=True)
    presso = pd.read_csv(locked.OUT / "MR_PRESSO_OCT_ONLY.tsv", sep="\t")
    lookup = {(r.pair_key, r.direction): r.status for r in presso.itertuples(index=False)}
    df["presso_status"] = [lookup.get((r.pair_id, r.direction), r.presso_status) for r in df.itertuples(index=False)]
    for i, row in df.iterrows():
        if row.n_iv_final == 0:
            df.at[i, "evidence_status"] = "UNRESOLVED"
        elif pd.notna(row.q_amendment004_global) and row.q_amendment004_global < 0.05:
            steiger_ok = row.steiger_direction is True or str(row.steiger_direction).lower() == "true"
            pleio = pd.notna(row.egger_p) and row.egger_p < 0.05
            sensitivity_ok = True if row.n_iv_final < 3 else pd.isna(row.weighted_median) or np.sign(row.weighted_median) == np.sign(row.beta)
            df.at[i, "evidence_status"] = "DIRECTIONAL_MR_SUPPORTED" if steiger_ok and not pleio and sensitivity_ok else "UNRESOLVED"
        elif pd.notna(row.p) and row.p < 0.05:
            df.at[i, "evidence_status"] = "SUGGESTIVE"
        else:
            df.at[i, "evidence_status"] = "NULL"
    if len(df) != 112:
        raise RuntimeError(f"HOLD_MR_INCOMPLETE: {len(df)}")
    df.to_csv(locked.OUT / "MR_DIRECTIONAL_MASTER_OCT_ONLY.tsv", sep="\t", index=False, na_rep="NA")

    pairs = []
    for (ret, disease), group in df.groupby(["retinal_trait", "disease"], sort=False):
        rd = group[group.exposure == ret].iloc[0]
        dr = group[group.exposure == disease].iloc[0]
        pairs.append({
            "retinal_trait": ret, "disease": disease,
            "retina_to_disease_status": rd.evidence_status, "disease_to_retina_status": dr.evidence_status,
            "retina_to_disease_n_iv": rd.n_iv_final, "disease_to_retina_n_iv": dr.n_iv_final,
            "retina_to_disease_beta": rd.beta, "retina_to_disease_se": rd.se, "retina_to_disease_ci_low": rd.ci_low, "retina_to_disease_ci_high": rd.ci_high,
            "retina_to_disease_p": rd.p, "retina_to_disease_q": rd.q_amendment004_global,
            "disease_to_retina_beta": dr.beta, "disease_to_retina_se": dr.se, "disease_to_retina_ci_low": dr.ci_low, "disease_to_retina_ci_high": dr.ci_high,
            "disease_to_retina_p": dr.p, "disease_to_retina_q": dr.q_amendment004_global,
            "retina_to_disease_steiger": rd.steiger_direction, "disease_to_retina_steiger": dr.steiger_direction,
            "retina_to_disease_heterogeneity_p": rd.heterogeneity_p, "disease_to_retina_heterogeneity_p": dr.heterogeneity_p,
            "retina_to_disease_pleiotropy_p": rd.egger_p, "disease_to_retina_pleiotropy_p": dr.egger_p,
        })
    pd.DataFrame(pairs).to_csv(locked.OUT / "MR_PAIR_SUMMARY_OCT_ONLY.tsv", sep="\t", index=False, na_rep="NA")

    exclusions = locked.read_tsv(locked.CONFIG / "amendment004_vascular_mr_exclusions.tsv")
    vascular = []
    for item in exclusions:
        for disease in locked.SYSTEMIC:
            for direction in (f"{item['trait_id']}_to_{disease}", f"{disease}_to_{item['trait_id']}"):
                vascular.append({"retinal_trait": item["trait_id"], "disease": disease, "direction": direction,
                                 "status": "NOT_ANALYSED_FREQUENCY_SEMANTICS_UNRESOLVED", "reason": item["reason_for_exclusion"]})
    pd.DataFrame(vascular).to_csv(locked.OUT / "VASCULAR_MR_STATUS.tsv", sep="\t", index=False)
    print(f"mr_directions={len(df)} pairs={len(pairs)} vascular_status={len(vascular)}")


if __name__ == "__main__":
    main()
