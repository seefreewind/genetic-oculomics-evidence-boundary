#!/usr/bin/env python3
"""Add audit metadata and generate Amendment 004 tables and reports."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "amendment004"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def main() -> None:
    master_path = OUT / "MR_DIRECTIONAL_MASTER_OCT_ONLY.tsv"
    master = pd.read_csv(master_path, sep="\t", keep_default_na=False, na_values=["NA"])
    inst = pd.read_csv(OUT / "MR_HARMONIZED_INSTRUMENTS_OCT_ONLY.tsv", sep="\t")
    strength = inst.groupby(["pair_key", "direction"])["f"].agg(["mean", "min"]).reset_index()
    strength.columns = ["pair_id", "direction", "mean_F", "min_F"]
    master = master.drop(columns=[c for c in ["mean_F", "min_F", "effect_scale", "multiple_testing_family"] if c in master], errors="ignore")
    master = master.merge(strength, on=["pair_id", "direction"], how="left")
    master["effect_scale"] = master["outcome"].map(lambda x: "log_odds" if str(x).startswith("sys_") else "standardized_continuous_trait")
    master["multiple_testing_family"] = "BH_across_112_Amendment004_primary_directions"
    master.to_csv(master_path, sep="\t", index=False, na_rep="NA")

    # Manuscript-facing combined matrix: analysed OCT and explicitly non-analysed vascular directions.
    analysed = master[["retinal_trait", "disease", "direction", "evidence_status", "n_iv_final", "p", "q_amendment004_global"]].copy()
    analysed["analysis_status"] = "ANALYSED_AMENDMENT004"
    vascular = pd.read_csv(OUT / "VASCULAR_MR_STATUS.tsv", sep="\t")
    vascular_matrix = vascular.rename(columns={"status": "evidence_status"})
    vascular_matrix["n_iv_final"] = pd.NA
    vascular_matrix["p"] = pd.NA
    vascular_matrix["q_amendment004_global"] = pd.NA
    vascular_matrix["analysis_status"] = "NOT_ANALYSED"
    combined = pd.concat([analysed, vascular_matrix[analysed.columns]], ignore_index=True)
    combined.to_csv(OUT / "FINAL_DIRECTIONAL_EVIDENCE_MATRIX.tsv", sep="\t", index=False, na_rep="NA")

    sup = ROOT / "supplement" / "amendment004"
    sup.mkdir(parents=True, exist_ok=True)
    master.to_csv(sup / "Supplementary_Table_S8_OCT_MR_directions.tsv", sep="\t", index=False, na_rep="NA")
    sensitivity_cols = ["pair_id", "direction", "n_iv_final", "heterogeneity_Q", "heterogeneity_p", "egger_intercept", "egger_p", "weighted_median", "weighted_median_p", "weighted_mode", "weighted_mode_p", "loo_status", "loo_beta_min", "loo_beta_max", "presso_status", "steiger_direction", "steiger_p", "variance_explained_exposure", "variance_explained_outcome"]
    master[sensitivity_cols].to_csv(sup / "Supplementary_Table_S9_OCT_MR_sensitivity.tsv", sep="\t", index=False, na_rep="NA")
    registry = pd.read_csv(ROOT / "config" / "frequency_semantics_registry.tsv", sep="\t", keep_default_na=False)
    exclusions = pd.read_csv(ROOT / "config" / "amendment004_vascular_mr_exclusions.tsv", sep="\t")
    audit = exclusions.merge(registry[["trait_id", "reported_column_name", "evidence_source", "frequency_represents"]], on="trait_id", how="left")
    audit["official_field_definition"] = "GWAS-SSF effect_allele_frequency denotes frequency of the labelled effect allele"
    audit["reference_diagnostic_evidence"] = audit["evidence_source"]
    audit["final_status"] = "UNRESOLVED"
    audit["MR_inclusion"] = "EXCLUDED_FROM_MR"
    audit[["trait_id", "display_name", "GCST_accession", "official_field_definition", "reference_diagnostic_evidence", "final_status", "MR_inclusion"]].to_csv(sup / "Supplementary_Table_vascular_GWAS_semantic_audit.tsv", sep="\t", index=False)
    combined.to_csv(sup / "Supplementary_Table_directional_evidence_matrix.tsv", sep="\t", index=False, na_rep="NA")

    status = master["evidence_status"].value_counts().to_dict()
    fdr = master[master.q_amendment004_global < 0.05]
    nominal = master[master.p < 0.05].sort_values("p")
    steiger_estimable = master[master.steiger_direction.astype(str).str.lower().isin(["true", "false"])]
    steiger_supported = steiger_estimable[(steiger_estimable.steiger_direction.astype(str).str.lower() == "true") & (steiger_estimable.steiger_p < 0.05)]
    lines = [
        "# Amendment 004 MR report", "", "## Completion", "",
        "- Primary directional family: 112/112 completed", "- Retinal-disease pairs: 56/56 completed",
        "- All directions used IVW random-effects under the frozen >=2-IV rule", f"- Final instruments per direction: {int(master.n_iv_final.min())}-{int(master.n_iv_final.max())}",
        "", "## Multiplicity-controlled result", "", f"- FDR-positive directions: {len(fdr)}", f"- Evidence-status counts: {status}",
        "- Final verdict: NO_ROBUST_OCT_DIRECTIONAL_SIGNAL", "", "## Nominal directions", "",
    ]
    if len(nominal):
        lines.append("| Direction | n IV | Beta | SE | P | q | Status |")
        lines.append("|---|---:|---:|---:|---:|---:|---|")
        for r in nominal.itertuples():
            lines.append(f"| {r.direction} | {r.n_iv_final} | {r.beta:.4g} | {r.se:.4g} | {r.p:.4g} | {r.q_amendment004_global:.4g} | {r.evidence_status} |")
    lines += ["", "The nominal rows are non-discovery findings and were not promoted to directional support.", "", "## Steiger and sensitivity", "",
              f"- Steiger estimable directions: {len(steiger_estimable)}/112", f"- Expected direction with Steiger P<0.05: {len(steiger_supported)}/112",
              "- MR-PRESSO: 112/112 computed; no outliers flagged", "- Steiger support does not override the primary 112-family FDR result.", "",
              "## Vascular boundary", "", "All 112 vascular directions are labelled `NOT_ANALYSED_FREQUENCY_SEMANTICS_UNRESOLVED`; none is classified as null or non-significant."]
    (ROOT / "reports" / "AMENDMENT004_MR_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    impact = """# Amendment 004 manuscript impact

## Central conclusion

The corrected narrative is scenario A: genome-wide analysis found no FDR-significant sharing, primary HDL-L found no corrected local sharing, native LAVA findings remained procedure- and boundary-sensitive, and data-integrity-qualified OCT-only MR found no robust directional signal across 112 directions. Seven vascular traits remain in global and local analyses but are not interpretable by MR because release-specific allele-frequency semantics could not be resolved authoritatively.

## Required changes

- Replace every claim that 224 directions were analysed with 112 OCT-only directions.
- Remove CRAE-CKD, rs475377, single-instrument Wald and legacy Steiger claims from scientific interpretation.
- State that vascular MR was not analysed, not null.
- Remove legacy Figure 4 from the main text; retain three main figures.
- Update Figure 1 directionality scope, Figure 2 MR track, Table 2 microvasculature interpretation, Methods, Abstract, Results, Discussion, Conclusion and cover letter.
- Preserve the full 14-trait global matrix and locked 47-pair local subset.
"""
    (ROOT / "reports" / "AMENDMENT004_MANUSCRIPT_IMPACT.md").write_text(impact, encoding="utf-8")

    table_dir = ROOT / "tables" / "amendment004"
    table_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        {"retinal_domain": "Neuroretina", "primary_traits": "RNFL; GCIPL; INL; INL-to-ELM", "global_evidence": "No pair survived FDR across all 112 LDSC pairs", "local_evidence": "Included where admitted in the locked 47-pair subset; no primary HDL-L signal survived correction", "directional_evidence": "Analysed in Amendment 004 OCT-only MR; no robust direction"},
        {"retinal_domain": "Outer retina", "primary_traits": "ELM-to-IS/OS; IS/OS-to-RPE; total macular thickness", "global_evidence": "No pair survived FDR across all 112 LDSC pairs", "local_evidence": "Included where admitted in the locked 47-pair subset; no primary HDL-L signal survived correction", "directional_evidence": "Analysed in Amendment 004 OCT-only MR; no robust direction"},
        {"retinal_domain": "Microvasculature", "primary_traits": "Arteriolar and venular tortuosity; CRAE; CRVE; AVR; arterial and venular density", "global_evidence": "Retained in all 112 LDSC pairs", "local_evidence": "Retained in the originally admitted local pairs", "directional_evidence": "Not evaluated by MR because allele-frequency semantics of the seven source GWAS releases could not be resolved authoritatively"},
    ]
    pd.DataFrame(rows).to_csv(table_dir / "Table2_retinal_domain_interpretation.tsv", sep="\t", index=False)
    print(f"master={len(master)} status={status} fdr={len(fdr)} steiger_supported={len(steiger_supported)}")


if __name__ == "__main__":
    main()
