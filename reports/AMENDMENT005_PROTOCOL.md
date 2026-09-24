# Amendment 005: prospectively frozen CAD sensitivity protocol

**No Amendment 005 sensitivity result was calculated or inspected before this protocol was frozen.** The machine-readable lock is `config/amendment_005_cad_sensitivity.yaml`; `config/AMENDMENT005.sha256` records its SHA-256. The frozen primary manuscript and five source tables remain `PRIMARY_PRE_AMENDMENT005`.

## Estimand and rationale

The mandatory comparison asks whether multiplicity-controlled study-level conclusions in the frozen retinal–systemic analyses depend on CAD inclusion. CAD is the only removed systemic trait. Its archived file has a 48-study, predominantly European multi-ancestry fingerprint, while LDSC, HDL-L, LAVA and instrument clumping used EUR LD references. The exact file has no sample-size field; the existing 184,305/60,801/123,504 values are publication-linked fallback metadata, not a file-reported N. The European-subset value 141,217 must never be assigned to this exact file.

## Mandatory leave-CAD-out analysis

Read, without modifying, `results/ldsc/GENETIC_CORRELATION_MASTER.tsv`, `results/phase1b/HDLL_LOCAL_RG_MASTER.tsv`, `results/phase1b/LAVA_LOCAL_RG_MASTER.tsv`, `results/phase1b_audit/LAVA_NATIVE_PVALUE_COMPARISON.tsv` and `results/amendment004/MR_DIRECTIONAL_MASTER_OCT_ONLY.tsv`. Preserve all non-CAD row effect estimates, SEs and P values. Remove rows with `systemic_disease=sys_cad_nikpay2015` (or `disease` for MR), keeping original row order. Confirm exact original/removed/remaining counts before computing q values; halt on mismatch.

Apply the same Benjamini–Hochberg procedure used by the frozen analysis to finite P values in each *new*, prespecified family, retaining nonfinite rows as `NA`. Families are: 98 non-CAD LDSC pairs (from 112); all non-CAD HDL-L block rows (from 116,472 across the locked 47 admitted pairs); all non-CAD native LAVA rows (from 26,639); the corresponding initial normal-approximation LAVA rows as historical context; and 98 non-CAD OCT-only MR directions (from 112). Do not recalculate effect estimates, clump instruments, rerun Steiger/MR-PRESSO/IVW, or change the original q values. Report old and new q values side by side, plus corrected-positive counts at q<0.05. For native LAVA, count frozen-row boundary flags: CI touches/exceeds |rho|=1, raw |rho|>1, and raw |rho|>1.25. LAVA is context, not a condition of the core-conclusion Boolean.

Set `CORE_CONCLUSION_CAD_INDEPENDENT=TRUE` only if **all three** have zero corrected positives: 98-pair LDSC, non-CAD HDL-L global-local, and 98-direction MR. Any new corrected signal makes it `FALSE`, triggers `MATERIAL_CHANGE=TRUE`, and stops automatic manuscript rebuilding. A q-value shift without a corrected-status change does not itself represent a biological change.

## Conditional European CAD replacement gate

Search sources in this fixed order: original Nikpay 2015 European-only release; official consortium European subset of the same analysis; GWAS Catalog archived European subset with explicit file-level provenance. Require phenotype compatibility, exact identifiable file, explicit European-only ancestry, documented exact N/cases/controls, known build, allele/effect and frequency semantics, accessible summary statistics, and a source manifest locked *before* examining effects or results. OpenGWAS 141,217 metadata alone, later CAD GWAS, UK Biobank, FinnGen and unrelated releases fail the gate. If no source passes, set `EUROPEAN_CAD_SENSITIVITY=NOT_RUN` with reason `NO_PROVENANCE_VERIFIED_MATCHED_EUROPEAN_RELEASE`; do not perform a numeric N stress test on the current raw file.

Only after a qualifying source is locked may the separately specified CAD-only LDSC (14 pairs), original seven CAD-admitted HDL-L/LAVA pairs (without readmission), and 14 OCT-only CAD MR directions be recomputed. Such results would form separate 112-pair/direction and local-block sensitivity families; they would not overwrite primary outputs. No mixed-ancestry LD method development is authorized.

## Preservation and interpretation

Before computation, record SHA-256 for the primary manuscript, LDSC, HDL-L, initial/native LAVA, MR, CAD raw input and registry in `reports/AMENDMENT005_PRESTATE.md`; place recoverable copies of the five result tables plus manuscript and registry under `archive/pre_amendment005/`. Neither primary results nor public GitHub/Zenodo release is modified during the sensitivity. If stable, prepare manuscript wording recommendations but do not silently rewrite the core frozen manuscript or public records. The amendment is a sensitivity, not a primary-dataset substitution.
