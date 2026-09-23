# Amendment 004 protocol

## Decision

Amendment 004 is a prospective **data-integrity-restricted OCT-only directional analysis**. It was frozen at 2026-09-23T06:13:33Z before any OCT-only MR estimate was calculated or inspected.

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

Amendment configuration SHA256: `5a5847de62f5781c70f64ea4d85f7cc24990147cb81faa537de3554b02e61a9c`.
