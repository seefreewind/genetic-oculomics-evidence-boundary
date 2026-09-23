#!/usr/bin/env python3
"""Allele-aware OCT-only harmonisation and locked 112-direction MR."""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import subprocess
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from scipy.stats import norm

import run_phase2a_mr as legacy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "amendment004"
CONFIG = ROOT / "config"
SYSTEMIC = [
    "sys_cad_nikpay2015", "sys_stroke_megastroke2018", "sys_t2d_scott2017",
    "sys_ckd_wuttke2019", "sys_ad_kunkle2019", "sys_pd_nalls2019_clinical",
    "sys_sle_bentham2015", "sys_ibd_delange2017",
]
COMPLEMENT = str.maketrans("ACGT", "TGCA")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_panel() -> list[str]:
    rows = read_tsv(CONFIG / "amendment004_oct_trait_panel.tsv")
    traits = [r["trait_id"] for r in rows if r["included_in_mr"] == "TRUE"]
    if len(traits) != 7:
        raise RuntimeError(f"HOLD_OCT_PANEL_MISMATCH: {len(traits)}")
    return traits


def load_semantics() -> dict[str, dict[str, str]]:
    return {r["trait_id"]: r for r in read_tsv(CONFIG / "frequency_semantics_registry.tsv")}


def load_ref_frequency() -> dict[str, dict[str, object]]:
    path = ROOT / "results" / "phase2" / "1kg_eur_iv_freq.afreq"
    result = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            freq = legacy.parse_num(row.get("ALT_FREQS") or row.get("ALT1_FREQ"))
            if freq is not None:
                result[row["ID"]] = {
                    "ref": (row.get("REF") or "").upper(),
                    "alt": (row.get("ALT") or row.get("ALT1") or "").upper(),
                    "alt_freq": float(freq),
                }
    return result


def complement(a: str) -> str:
    return a.translate(COMPLEMENT) if set(a) <= set("ACGT") else ""


def source_frequency(row: dict[str, object], trait: str, semantics: dict[str, dict[str, str]], ref: dict[str, dict[str, object]]) -> dict[str, object]:
    ea = str(row.get("ea") or "").upper()
    oa = str(row.get("oa") or "").upper()
    raw = legacy.parse_num(row.get("eaf"))
    semantic = semantics[trait]["frequency_represents"]
    if raw is not None:
        if semantic != "EFFECT_ALLELE":
            raise RuntimeError(f"HOLD_AMENDMENT004_HARMONISATION: source frequency semantic {trait}={semantic}")
        return {"source_freq": raw, "freq_allele": ea, "standardized_eaf": raw, "frequency_semantics": semantic, "frequency_origin": "SOURCE"}
    rp = ref.get(str(row.get("rsid")))
    if rp is None:
        return {"source_freq": np.nan, "freq_allele": "NA", "standardized_eaf": np.nan, "frequency_semantics": "NO_SOURCE_FREQUENCY", "frequency_origin": "UNAVAILABLE"}
    if ea == rp["alt"]:
        eaf = float(rp["alt_freq"])
    elif ea == rp["ref"]:
        eaf = 1.0 - float(rp["alt_freq"])
    else:
        return {"source_freq": float(rp["alt_freq"]), "freq_allele": str(rp["alt"]), "standardized_eaf": np.nan, "frequency_semantics": "REFERENCE_PANEL_ALT_ALLELE", "frequency_origin": "ALLELE_MISMATCH"}
    return {"source_freq": float(rp["alt_freq"]), "freq_allele": str(rp["alt"]), "standardized_eaf": eaf, "frequency_semantics": "REFERENCE_PANEL_ALT_ALLELE", "frequency_origin": "1KG_EUR_EXPLICIT_ALT"}


def enrich_leads(leads: dict[str, list[dict[str, object]]], source_rows: dict[str, dict[str, dict[str, object]]], bim: dict[str, tuple[str, int, str, str]]) -> None:
    for trait, rows in leads.items():
        for row in rows:
            src = legacy.lookup_outcome(source_rows[trait], row, bim)
            if src is None:
                continue
            if str(src["ea"]).upper() != str(row["ea"]).upper() or str(src["oa"]).upper() != str(row["oa"]).upper():
                raise RuntimeError(f"HOLD_AMENDMENT004_HARMONISATION: frozen candidate/source allele mismatch {trait} {row['rsid']}")
            row["eaf"] = src.get("eaf")
            row["n"] = row.get("n") or src.get("n")


def harmonise_one(x: dict[str, object], y: Optional[dict[str, object]], exposure: str, outcome: str,
                  semantics: dict[str, dict[str, str]], ref: dict[str, dict[str, object]]) -> tuple[dict[str, object], Optional[dict[str, object]]]:
    base = {
        "rsid": x["rsid"], "chr": x["chrom"], "pos": x["pos"],
        "exposure_EA": x["ea"], "exposure_OA": x["oa"],
        "outcome_EA": "NA" if y is None else y["ea"], "outcome_OA": "NA" if y is None else y["oa"],
        "palindromic": legacy.is_pal(str(x["ea"]), str(x["oa"])),
        "strand_flip": False, "allele_flip": False, "retained": False, "removal_reason": "",
    }
    fx = source_frequency(x, exposure, semantics, ref)
    fy = source_frequency(y, outcome, semantics, ref) if y is not None else {
        "source_freq": np.nan, "freq_allele": "NA", "standardized_eaf": np.nan,
        "frequency_semantics": semantics[outcome]["frequency_represents"], "frequency_origin": "MISSING_OUTCOME",
    }
    base.update({
        "exposure_frequency_semantics": fx["frequency_semantics"],
        "outcome_frequency_semantics": fy["frequency_semantics"],
        "exposure_source_frequency": fx["source_freq"], "exposure_frequency_allele": fx["freq_allele"],
        "outcome_source_frequency": fy["source_freq"], "outcome_frequency_allele": fy["freq_allele"],
        "exposure_standardized_EAF": fx["standardized_eaf"],
        "outcome_standardized_EAF": fy["standardized_eaf"],
        "aligned_outcome_EAF": np.nan, "delta_EAF": np.nan,
    })
    if y is None:
        base["removal_reason"] = "MISSING_OUTCOME_VARIANT"
        return base, None
    ea, oa, ya, yo = map(str, (x["ea"], x["oa"], y["ea"], y["oa"]))
    ex_eaf = legacy.parse_num(fx["standardized_eaf"])
    out_eaf = legacy.parse_num(fy["standardized_eaf"])
    pal = bool(base["palindromic"])
    flip = False
    strand = False
    if pal:
        if {ea, oa} != {ya, yo}:
            base["removal_reason"] = "INCOMPATIBLE_ALLELES"
            return base, None
        if ex_eaf is None or out_eaf is None or 0.42 <= ex_eaf <= 0.58 or 0.42 <= out_eaf <= 0.58:
            base["removal_reason"] = "PALINDROMIC_AMBIGUOUS"
            return base, None
        same_delta = abs(ex_eaf - out_eaf) if ea == ya else abs(ex_eaf - (1.0 - out_eaf))
        swap_delta = abs(ex_eaf - (1.0 - out_eaf)) if ea == ya else abs(ex_eaf - out_eaf)
        if same_delta <= swap_delta and same_delta <= 0.20:
            flip = ea != ya
        elif swap_delta < same_delta and swap_delta <= 0.20:
            flip = ea == ya
        else:
            base["removal_reason"] = "PALINDROMIC_FREQUENCY_MISMATCH"
            return base, None
    elif (ea, oa) == (ya, yo):
        pass
    elif (ea, oa) == (yo, ya):
        flip = True
    elif (ea, oa) == (complement(ya), complement(yo)):
        strand = True
    elif (ea, oa) == (complement(yo), complement(ya)):
        strand = True
        flip = True
    else:
        base["removal_reason"] = "INCOMPATIBLE_ALLELES"
        return base, None
    aligned = (1.0 - out_eaf) if (flip and out_eaf is not None) else out_eaf
    delta = abs(ex_eaf - aligned) if ex_eaf is not None and aligned is not None else None
    base.update({"strand_flip": strand, "allele_flip": flip, "aligned_outcome_EAF": aligned if aligned is not None else np.nan, "delta_EAF": delta if delta is not None else np.nan})
    if delta is not None and delta > 0.20:
        base["removal_reason"] = "DELTA_EAF_GT_0.20"
        return base, None
    base["retained"] = True
    base["removal_reason"] = "PASS"
    kept = {
        "rsid": x["rsid"], "beta_exp": float(x["beta"]), "se_exp": float(x["se"]),
        "beta_out": -float(y["beta"]) if flip else float(y["beta"]), "se_out": float(y["se"]),
        "eaf": ex_eaf, "n_exp": x.get("n"), "n_out": y.get("n"), "f": x.get("f"),
        "p_exp": x.get("p"), "p_out": y.get("p"),
    }
    return base, kept


def prepare() -> tuple[list[str], dict, dict, dict, dict, dict]:
    OUT.mkdir(parents=True, exist_ok=True)
    retinal = load_panel()
    traits = retinal + SYSTEMIC
    semantics = load_semantics()
    for trait in retinal:
        if semantics[trait]["frequency_represents"] != "EFFECT_ALLELE" or semantics[trait]["confidence"] != "HIGH":
            raise RuntimeError(f"HOLD_OCT_FREQUENCY_SEMANTICS: {trait}")
    for trait in SYSTEMIC:
        if semantics[trait]["frequency_column"] != "NA" and semantics[trait]["frequency_represents"] != "EFFECT_ALLELE":
            raise RuntimeError(f"HOLD_AMENDMENT004_HARMONISATION: {trait}")
    legacy.ALIASES["eaf"] = list(dict.fromkeys(legacy.ALIASES["eaf"] + ["af1"]))
    registry = legacy.load_registry()
    manifest = legacy.load_manifest()
    missing = [t for t in traits if t not in manifest]
    if missing:
        raise RuntimeError("Missing frozen raw files: " + ",".join(missing))
    confirmations = []
    for trait in retinal:
        raw = manifest[trait]
        with zipfile.ZipFile(raw) as archive:
            members = [m for m in archive.infolist() if not m.is_dir() and not m.filename.startswith("__MACOSX/")]
            member = max(members, key=lambda m: m.file_size)
            with archive.open(member) as handle:
                header = handle.readline().decode("utf-8", errors="replace").strip().split("\t")
        required = {"A1", "A2", "AF1", "BETA"}
        status = "PASS" if required.issubset(header) and semantics[trait]["frequency_represents"] == "EFFECT_ALLELE" else "HOLD"
        confirmations.append({
            "trait_id": trait, "source_file": str(raw.relative_to(ROOT)), "effect_allele_column": "A1",
            "other_allele_column": "A2", "frequency_column": "AF1", "AF1_corresponds_to_A1": "YES",
            "A1_is_effect_allele": "YES", "evidence": "Official GCTA/fastGWA documentation plus source release header",
            "status": status,
        })
    pd.DataFrame(confirmations).to_csv(OUT / "OCT_FREQUENCY_SEMANTICS_CONFIRMATION.tsv", sep="\t", index=False)
    if any(r["status"] != "PASS" for r in confirmations):
        raise RuntimeError("HOLD_OCT_FREQUENCY_SEMANTICS")
    bim, _ = legacy.load_bim()
    leads = legacy.load_leads(traits)
    requests = {}
    for trait in traits:
        requests[trait] = (
            {str(x["rsid"]) for rows in leads.values() for x in rows},
            {(str(x["chrom"]), int(x["pos"])) for rows in leads.values() for x in rows},
        )
    source_rows = {}
    for idx, trait in enumerate(traits, 1):
        print(f"loading source {idx}/{len(traits)} {trait}", flush=True)
        source_rows[trait] = legacy.load_outcome_trait(trait, manifest[trait], *requests[trait], legacy.registry_n(registry[trait]))
    enrich_leads(leads, source_rows, bim)
    return retinal, registry, semantics, bim, leads, source_rows


def all_harmonisations(retinal, registry, semantics, bim, leads, source_rows):
    ref = load_ref_frequency()
    audit = []
    harmonised = defaultdict(list)
    for ret in retinal:
        for sys in SYSTEMIC:
            pair = f"{ret}__{sys}"
            for exposure, outcome in ((ret, sys), (sys, ret)):
                direction = f"{exposure}_to_{outcome}"
                for x in leads[exposure]:
                    y = legacy.lookup_outcome(source_rows[outcome], x, bim)
                    row, kept = harmonise_one(x, y, exposure, outcome, semantics, ref)
                    row.update({"pair_id": pair, "direction": direction, "exposure": exposure, "outcome": outcome})
                    audit.append(row)
                    if kept is not None:
                        kept.update({"pair_key": pair, "direction": direction, "exposure": exposure, "outcome": outcome})
                        harmonised[(pair, direction)].append(kept)
    return pd.DataFrame(audit), harmonised


def dry_run() -> None:
    retinal, registry, semantics, bim, leads, source_rows = prepare()
    audit, harmonised = all_harmonisations(retinal, registry, semantics, bim, leads, source_rows)
    columns = [
        "pair_id", "direction", "exposure", "outcome", "rsid", "chr", "pos",
        "exposure_EA", "exposure_OA", "outcome_EA", "outcome_OA",
        "exposure_frequency_semantics", "outcome_frequency_semantics",
        "exposure_source_frequency", "exposure_frequency_allele", "outcome_source_frequency", "outcome_frequency_allele",
        "exposure_standardized_EAF", "outcome_standardized_EAF", "aligned_outcome_EAF", "delta_EAF",
        "palindromic", "strand_flip", "allele_flip", "retained", "removal_reason",
    ]
    audit[columns].to_csv(OUT / "HARMONISATION_DRY_RUN_112.tsv", sep="\t", index=False, na_rep="NA")
    summary = []
    for (pair, direction), group in audit.groupby(["pair_id", "direction"], sort=False):
        reasons = Counter(group["removal_reason"])
        matched = int((group.removal_reason != "MISSING_OUTCOME_VARIANT").sum())
        after_allele = matched - reasons["INCOMPATIBLE_ALLELES"] - reasons["PALINDROMIC_AMBIGUOUS"]
        after_frequency = after_allele - reasons["PALINDROMIC_FREQUENCY_MISMATCH"] - reasons["DELTA_EAF_GT_0.20"]
        summary.append({
            "pair_id": pair, "direction": direction, "initial_GWS_IV": len(group), "after_clumping": len(group),
            "matched_outcome": matched, "after_allele_harmonisation": after_allele,
            "after_frequency_QC": after_frequency, "final_IV": int(group.retained.sum()),
            "frequency_semantic_warning": "NONE",
            "palindromic_warning": f"REMOVED_{reasons['PALINDROMIC_AMBIGUOUS'] + reasons['PALINDROMIC_FREQUENCY_MISMATCH']}" if reasons["PALINDROMIC_AMBIGUOUS"] + reasons["PALINDROMIC_FREQUENCY_MISMATCH"] else "NONE",
            "other_warning": ";".join(f"{k}={v}" for k, v in sorted(reasons.items()) if k not in {"PASS", "PALINDROMIC_AMBIGUOUS", "PALINDROMIC_FREQUENCY_MISMATCH"} and v) or "NONE",
        })
    summary_df = pd.DataFrame(summary)
    if len(summary_df) != 112:
        raise RuntimeError(f"HOLD_HARMONISATION_QC: expected 112 directions, observed {len(summary_df)}")
    summary_df.to_csv(OUT / "HARMONISATION_SUMMARY_112.tsv", sep="\t", index=False, na_rep="NA")
    print(f"dry_directions={len(summary_df)} candidates={len(audit)} retained={int(audit.retained.sum())}")


def estimate_direction(exposure: str, outcome: str, rows: list[dict[str, object]], registry: dict[str, dict[str, str]]) -> dict[str, object]:
    exp_binary, out_binary = exposure.startswith("sys_"), outcome.startswith("sys_")
    for r in rows:
        r["binary_exp"], r["binary_out"] = exp_binary, out_binary
        r["n_exp"] = r.get("n_exp") or legacy.registry_n(registry[exposure])
        r["n_out"] = r.get("n_out") or legacy.registry_n(registry[outcome])
    k = len(rows)
    base = {
        "exposure": exposure, "outcome": outcome, "n_iv_final": k, "method": "NO_VALID_IV",
        "beta": np.nan, "se": np.nan, "ci_low": np.nan, "ci_high": np.nan, "OR": np.nan, "p": np.nan,
        "q_amendment004_global": np.nan, "heterogeneity_Q": np.nan, "heterogeneity_p": np.nan,
        "egger_intercept": np.nan, "egger_p": np.nan, "weighted_median": np.nan, "weighted_median_p": np.nan,
        "weighted_mode": np.nan, "weighted_mode_p": np.nan, "egger_beta": np.nan,
        "steiger_direction": "NA", "steiger_p": np.nan, "variance_explained_exposure": np.nan,
        "variance_explained_outcome": np.nan, "presso_status": "NOT_RUN", "loo_status": "NOT_RUN",
        "loo_beta_min": np.nan, "loo_beta_max": np.nan, "evidence_status": "UNRESOLVED" if k == 0 else "NULL",
    }
    if not rows:
        return base
    bx = np.array([r["beta_exp"] for r in rows]); sx = np.array([r["se_exp"] for r in rows])
    by = np.array([r["beta_out"] for r in rows]); sy = np.array([r["se_out"] for r in rows])
    if k == 1:
        beta = by[0] / bx[0]
        se = math.sqrt(sy[0] ** 2 / bx[0] ** 2 + by[0] ** 2 * sx[0] ** 2 / bx[0] ** 4)
        mr = {"beta": beta, "se": se, "p": 2 * norm.sf(abs(beta / se)), "Q": np.nan, "Q_p": np.nan, "ratio_var": np.array([se * se])}
        base["method"] = "Wald_ratio"
    else:
        mr = legacy.ivw_random(bx, sx, by, sy)
        beta, se = mr["beta"], mr["se"]
        base["method"] = "IVW_random_effects"
    base.update({"beta": beta, "se": se, "ci_low": beta - 1.95996398454 * se, "ci_high": beta + 1.95996398454 * se,
                 "OR": math.exp(beta) if out_binary and abs(beta) < 700 else np.nan, "p": mr["p"],
                 "heterogeneity_Q": mr.get("Q", np.nan), "heterogeneity_p": mr.get("Q_p", np.nan)})
    if k >= 3:
        ratios = by / bx
        weights = 1 / np.maximum(mr["ratio_var"], 1e-300)
        base["weighted_median"] = legacy.weighted_median(ratios, weights)
        base["weighted_median_p"] = 2 * norm.sf(abs(base["weighted_median"] / math.sqrt(1 / weights.sum())))
        base["weighted_mode"] = legacy.weighted_mode(ratios, weights)
        base["weighted_mode_p"] = 2 * norm.sf(abs(base["weighted_mode"] / math.sqrt(1 / weights.sum())))
        eb, _, ei, eise = legacy.egger(ratios, bx, sy)
        base["egger_beta"], base["egger_intercept"] = eb, ei
        base["egger_p"] = 2 * norm.sf(abs(ei / eise)) if eise > 0 else np.nan
        loo = [legacy.ivw_random(np.delete(bx, i), np.delete(sx, i), np.delete(by, i), np.delete(sy, i))["beta"] for i in range(k) if k - 1 >= 2]
        if loo:
            base.update({"loo_status": "COMPUTED", "loo_beta_min": min(loo), "loo_beta_max": max(loo)})
    elif k == 2:
        base["loo_status"] = "NOT_RUN_TWO_IV"
    ve, vo, correct, sp = legacy.steiger(rows, exp_binary, out_binary, registry[exposure], registry[outcome])
    base.update({"variance_explained_exposure": ve, "variance_explained_outcome": vo,
                 "steiger_direction": bool(correct) if isinstance(correct, (bool, np.bool_)) else "NA",
                 "steiger_p": sp if isinstance(sp, (float, int)) else np.nan,
                 "presso_status": "PENDING_MRPRESSO" if k >= 4 else "NOT_ELIGIBLE_LT4_IV"})
    return base


def run_mr() -> None:
    lock = CONFIG / "AMENDMENT004_HARMONISATION_LOCK.sha256"
    if not lock.exists():
        raise RuntimeError("HOLD_HARMONISATION_QC: harmonisation lock missing")
    retinal, registry, semantics, bim, leads, source_rows = prepare()
    audit, harmonised = all_harmonisations(retinal, registry, semantics, bim, leads, source_rows)
    frozen = pd.read_csv(OUT / "HARMONISATION_DRY_RUN_112.tsv", sep="\t")
    current = audit[[c for c in frozen.columns]].copy()
    for frame in (frozen, current):
        frame.replace({True: "True", False: "False"}, inplace=True)
    if not frozen.fillna("NA").astype(str).equals(current.fillna("NA").astype(str)):
        raise RuntimeError("HOLD_HARMONISATION_QC: rerun differs from locked dry run")
    records, instrument_rows = [], []
    for ret in retinal:
        for sys in SYSTEMIC:
            pair = f"{ret}__{sys}"
            for exposure, outcome in ((ret, sys), (sys, ret)):
                direction = f"{exposure}_to_{outcome}"
                rows = harmonised[(pair, direction)]
                result = estimate_direction(exposure, outcome, rows, registry)
                result.update({"pair_id": pair, "direction": direction, "retinal_trait": ret, "disease": sys,
                               "n_iv_initial": len(leads[exposure]), "frequency_semantics": semantics[exposure]["frequency_represents"]})
                records.append(result)
                instrument_rows.extend(rows)
    df = pd.DataFrame(records)
    df["q_amendment004_global"] = legacy.bh(df["p"])
    harm_path = OUT / "MR_HARMONIZED_INSTRUMENTS_OCT_ONLY.tsv"
    pd.DataFrame(instrument_rows).to_csv(harm_path, sep="\t", index=False, na_rep="NA")
    subprocess.run(["Rscript", str(ROOT / "scripts/run_phase2a_mrpresso.R"), str(harm_path), str(OUT / "MR_PRESSO_OCT_ONLY.tsv")], cwd=ROOT, check=True)
    presso = pd.read_csv(OUT / "MR_PRESSO_OCT_ONLY.tsv", sep="\t")
    p_lookup = {(r.pair_key, r.direction): r.status for r in presso.itertuples(index=False)}
    df["presso_status"] = [p_lookup.get((r.pair_id, r.direction), r.presso_status) for r in df.itertuples(index=False)]
    for i, row in df.iterrows():
        if row.n_iv_final == 0:
            df.at[i, "evidence_status"] = "UNRESOLVED"
        elif pd.notna(row.q_amendment004_global) and row.q_amendment004_global < 0.05:
            steiger_ok = row.steiger_direction is True or str(row.steiger_direction).lower() == "true"
            pleio = pd.notna(row.egger_p) and row.egger_p < 0.05
            sens = True if row.n_iv_final < 3 else pd.isna(row.weighted_median) or np.sign(row.weighted_median) == np.sign(row.beta)
            df.at[i, "evidence_status"] = "DIRECTIONAL_MR_SUPPORTED" if steiger_ok and not pleio and sens else "UNRESOLVED"
        elif pd.notna(row.p) and row.p < 0.05:
            df.at[i, "evidence_status"] = "SUGGESTIVE"
        else:
            df.at[i, "evidence_status"] = "NULL"
    if len(df) != 112:
        raise RuntimeError(f"HOLD_MR_INCOMPLETE: {len(df)}")
    df.to_csv(OUT / "MR_DIRECTIONAL_MASTER_OCT_ONLY.tsv", sep="\t", index=False, na_rep="NA")
    pair_rows = []
    for (ret, disease), group in df.groupby(["retinal_trait", "disease"], sort=False):
        rd = group[group.exposure == ret].iloc[0]
        dr = group[group.exposure == disease].iloc[0]
        pair_rows.append({
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
    pd.DataFrame(pair_rows).to_csv(OUT / "MR_PAIR_SUMMARY_OCT_ONLY.tsv", sep="\t", index=False, na_rep="NA")
    exclusions = read_tsv(CONFIG / "amendment004_vascular_mr_exclusions.tsv")
    vascular = []
    for item in exclusions:
        for disease in SYSTEMIC:
            for direction in (f"{item['trait_id']}_to_{disease}", f"{disease}_to_{item['trait_id']}"):
                vascular.append({"retinal_trait": item["trait_id"], "disease": disease, "direction": direction,
                                 "status": "NOT_ANALYSED_FREQUENCY_SEMANTICS_UNRESOLVED", "reason": item["reason_for_exclusion"]})
    pd.DataFrame(vascular).to_csv(OUT / "VASCULAR_MR_STATUS.tsv", sep="\t", index=False)
    print(f"mr_directions={len(df)} pairs={len(pair_rows)} vascular_status={len(vascular)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-mr", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.run_mr:
        parser.error("choose exactly one of --dry-run or --run-mr")
    dry_run() if args.dry_run else run_mr()


if __name__ == "__main__":
    main()
