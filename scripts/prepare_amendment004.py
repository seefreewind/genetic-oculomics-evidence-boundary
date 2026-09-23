#!/usr/bin/env python3
"""Freeze Amendment 004 and derive its OCT-only panel before MR results exist."""
from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"
RESULTS = ROOT / "results" / "amendment004"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    admission = {r["trait"]: r for r in read_tsv(CONFIG / "retinal_trait_admission.tsv")}
    semantics = {r["trait_id"]: r for r in read_tsv(CONFIG / "frequency_semantics_registry.tsv")}
    phenotype = {r["trait_id"]: r for r in read_tsv(CONFIG / "phenotype_registry.tsv")}

    panel = []
    excluded = []
    for trait, adm in admission.items():
        if adm["primary"].upper() != "TRUE":
            continue
        sem = semantics.get(trait)
        meta = phenotype.get(trait)
        if sem is None or meta is None:
            raise RuntimeError(f"Missing registry entry for primary retinal trait: {trait}")
        qualified = (
            adm["domain"] in {"neuroretina", "outer_retina"}
            and sem["frequency_represents"] == "EFFECT_ALLELE"
            and sem["confidence"] == "HIGH"
        )
        if qualified:
            panel.append({
                "trait_id": trait,
                "display_name": meta["trait_name"],
                "retinal_domain": adm["domain"],
                "source_study": sem["source_study"],
                "frequency_semantics": sem["frequency_represents"],
                "confidence": sem["confidence"],
                "included_in_mr": "TRUE",
                "reason": "PRIMARY_OCT_TRAIT_WITH_VERIFIABLE_EFFECT_ALLELE_FREQUENCY",
            })
        elif adm["domain"] == "microvasculature":
            accession = Path(sem["source_file"]).name.split("__")[-1].split(".")[0]
            excluded.append({
                "trait_id": trait,
                "display_name": meta["trait_name"],
                "GCST_accession": accession,
                "frequency_semantics_status": "SEMANTIC_CONFLICT",
                "reason_for_exclusion": "UNRESOLVED_RELEASE_SPECIFIC_ALLELE_FREQUENCY_SEMANTICS",
            })

    if len(panel) != 7:
        raise RuntimeError(f"HOLD_OCT_PANEL_MISMATCH: expected 7, observed {len(panel)}")
    if len(excluded) != 7:
        raise RuntimeError(f"HOLD_OCT_PANEL_MISMATCH: expected 7 vascular exclusions, observed {len(excluded)}")

    write_tsv(
        CONFIG / "amendment004_oct_trait_panel.tsv", panel,
        ["trait_id", "display_name", "retinal_domain", "source_study", "frequency_semantics", "confidence", "included_in_mr", "reason"],
    )
    write_tsv(
        CONFIG / "amendment004_vascular_mr_exclusions.tsv", excluded,
        ["trait_id", "display_name", "GCST_accession", "frequency_semantics_status", "reason_for_exclusion"],
    )

    trait_lines = "\n".join(f"  - {r['trait_id']}" for r in panel)
    excluded_lines = "\n".join(f"  - {r['trait_id']}" for r in excluded)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    config_text = f"""# Prospective protocol frozen before any Amendment 004 OCT-only MR estimate was calculated or inspected.
amendment_id: AMENDMENT_004_DATA_INTEGRITY_RESTRICTED_OCT_ONLY_DIRECTIONAL_ANALYSIS
amendment_date_utc: {now}
status: LOCKED_BEFORE_OCT_ONLY_HARMONISATION_AND_MR_RESULTS
reason: unresolved allele-frequency semantics in 7 vascular GWAS releases
authoritative_mapping_unavailable: true

included_retinal_traits:
{trait_lines}

excluded_from_mr:
{excluded_lines}

systemic_diseases:
  - sys_cad_nikpay2015
  - sys_stroke_megastroke2018
  - sys_t2d_scott2017
  - sys_ckd_wuttke2019
  - sys_ad_kunkle2019
  - sys_pd_nalls2019_clinical
  - sys_sle_bentham2015
  - sys_ibd_delange2017

directions:
  retinal_traits: 7
  systemic_diseases: 8
  bidirectional_tests: 112

multiple_testing:
  family: all_112_primary_directional_tests
  method: Benjamini-Hochberg
  output_field: q_amendment004_global

instrument_threshold:
  p: 5.0e-8
  source: config/analysis_lock.yaml

clumping:
  r2: 0.001
  window_kb: 10000
  ancestry: EUR
  LD_reference: data/reference/1kg_v3/EUR
  source: config/analysis_lock.yaml

harmonisation_policy:
  base_policy: same_as_original_Phase_2A
  eligibility_change_only: semantically_valid_sources_only
  delta_eaf_threshold: 0.20
  no_automatic_frequency_complement: true
  reference_frequency_requires_explicit_allele_identity: true
  unresolved_palindromic_policy: exclude

primary_estimators:
  one_iv: Wald_ratio
  two_or_more_iv: IVW_random_effects
  source: config/amendment_002_phase1b1_phase2a_mr.yaml

sensitivity_estimators:
  methods: [weighted_median, weighted_mode, MR_Egger, Cochran_Q, Egger_intercept, leave_one_out, MR_PRESSO]
  eligibility: same_instrument_count_requirements_as_Phase_2A

steiger:
  method: same_as_Phase_2A
  instrument_set: Amendment_004_harmonised_instruments

preservation:
  amendment003_status: CLOSED_WITHOUT_CORRECTED_MR
  amendment003_reason: AUTHORITATIVE_FREQUENCY_MAPPING_UNAVAILABLE
  legacy_phase2a_status: LEGACY_INVALID_PENDING_CORRECTION
  vascular_global_local_results_retained: true

result_blinding:
  statement: No OCT-only MR estimate was calculated or inspected before Amendment 004 was frozen.
  dry_run_before_mr: true
  harmonisation_lock_required_before_mr: true

forbidden:
  - vascular_frequency_1_minus_f_inference
  - infer_frequency_semantics_from_1KG_concordance
  - disable_delta_EAF_QC
  - substitute_vascular_GWAS
  - new_traits_or_diseases
  - new_thresholds_or_estimators
  - modify_global_or_local_results
  - coloc
  - CAUSE
  - LCV
  - GSMR
  - MVMR
  - pathway_analysis
  - functional_follow_up
"""
    amendment = CONFIG / "amendment_004_oct_only_mr.yaml"
    amendment.write_text(config_text, encoding="utf-8")
    amendment_sha = sha256(amendment)
    (CONFIG / "AMENDMENT004.sha256").write_text(f"{amendment_sha}  config/amendment_004_oct_only_mr.yaml\n", encoding="utf-8")

    closure = f"""# Amendment 003 closure

Status: **CLOSED_WITHOUT_CORRECTED_MR**  
Reason: **AUTHORITATIVE_FREQUENCY_MAPPING_UNAVAILABLE**

Amendment 003 remains preserved with final status `HOLD_FREQUENCY_SEMANTICS_UNRESOLVED`. Its registry, CRAE six-SNP semantic audit, exception log, legacy Phase 2A files and checksums were not overwritten. No corrected 224-direction MR family was calculated.

The seven retinal vascular releases remain usable for the already-frozen retinal redundancy, global LDSC, HDL-L and LAVA analyses. They are excluded only from primary directional MR because release-specific allele-frequency coding cannot be resolved authoritatively to the standard required for frequency-aware harmonisation.

This closure was recorded before any Amendment 004 OCT-only MR estimate was calculated or inspected. Amendment 004 prospectively restricts directional analysis to the seven existing primary OCT traits with documented `AF1 = frequency(A1)` and `A1 = effect allele` semantics.
"""
    (REPORTS / "AMENDMENT003_CLOSURE.md").write_text(closure, encoding="utf-8")

    protocol = f"""# Amendment 004 protocol

## Decision

Amendment 004 is a prospective **data-integrity-restricted OCT-only directional analysis**. It was frozen at {now} before any OCT-only MR estimate was calculated or inspected.

## Scientific reason

Seven retinal vascular GWAS releases show an unresolved discrepancy between the GWAS-SSF frequency-field definition and frozen external allele-frequency concordance. Authoritative, release-specific mapping is unavailable. The traits remain in correlation-based analyses but are excluded from MR; the exclusion is unrelated to significance, biological priority or prior MR results.

## Locked universe

- Included retinal traits: 7 primary OCT structural traits derived programmatically from `retinal_trait_admission.tsv` and `frequency_semantics_registry.tsv`.
- Systemic diseases: the same 8 frozen releases.
- Directional family: 7 × 8 × 2 = 112 tests.
- Multiplicity: Benjamini–Hochberg across all 112 primary tests.
- Instruments, clumping, EUR LD reference, harmonisation thresholds, estimators, sensitivity eligibility and Steiger method: unchanged from Phase 2A.

## Stopping gates

All seven OCT sources must reconfirm `AF1 = frequency(A1)` and `A1 = effect allele`. Any OCT or systemic semantic conflict stops the pipeline before MR. A harmonisation-only dry run must cover all 112 directions and be locked by checksum before effect estimation.

## Boundary

No vascular frequency complement, inferred semantic mapping, replacement GWAS, new phenotype, new estimator, altered threshold, coloc, CAUSE, LCV, GSMR, MVMR, pathway or functional follow-up is authorised.

Amendment configuration SHA256: `{amendment_sha}`.
"""
    (REPORTS / "AMENDMENT004_PROTOCOL.md").write_text(protocol, encoding="utf-8")
    print(f"panel={len(panel)} excluded={len(excluded)} amendment_sha={amendment_sha}")


if __name__ == "__main__":
    main()
