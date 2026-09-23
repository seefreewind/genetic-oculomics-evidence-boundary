# Amendment 003 protocol

## Status

**LOCKED BEFORE CORRECTED HARMONISATION AND MR RESULTS**

Amendment 003 was created at 2026-09-23T02:25:26Z after a pre-submission audit identified an allele-frequency semantic inconsistency and before any corrected MR effect estimate was calculated or inspected.

## Reason

The Phase 2A harmonisation implementation accepted source frequency values under the assumption that a column named `effect_allele_frequency`, `EAF`, `A1FREQ`, `FRQ`, `MAF` or a related label necessarily described the labelled effect allele. The CRAE audit showed that the six clumped lead frequencies were instead concordant with the labelled other allele in the 1KG EUR reference. This invalidated the frequency-based exclusion trace as a submission-ready result and required an allele-aware correction.

## Authorized scope

- Construct a source-level frequency-semantics registry for the same 14 retinal GWAS and eight systemic-disease GWAS.
- Correct the harmonisation code so each frequency value is carried with an explicit frequency allele.
- Standardize to effect-allele frequency only after the source frequency allele is established.
- Perform a results-blind harmonisation-only dry run across the complete 224-direction instrument universe.
- Freeze the harmonisation dry run before calculating MR effects.
- Rerun all 224 prespecified MR directions with the same instruments, clumping, estimators, sensitivity eligibility rules, Steiger method and complete-family BH-FDR framework as Phase 2A.
- Compare legacy and corrected results without overwriting any legacy file.
- Regenerate manuscript inputs only after independent QC and a corrected numerical freeze.

## Locked analysis constants

| Component | Locked value |
|---|---|
| Retinal traits | Same 14 primary retinal traits |
| Systemic diseases | Same 8 primary systemic diseases |
| Directions | 224 |
| Instrument threshold | P<5×10⁻⁸ |
| Clumping | r²<0.001 within 10 Mb |
| LD reference | 1KG Phase 3 EUR, GRCh37 |
| One-IV estimator | Wald ratio |
| Two-or-more-IV estimator | IVW random effects |
| Sensitivity estimators | Same Phase 2A eligibility and methods |
| ΔEAF threshold | Strict absolute aligned difference >0.20 |
| Multiple testing | BH across the complete 224-direction primary family |
| Classification | Unchanged Phase 2A rules |

No standard may be changed to preserve or restore the previous CRAE→CKD result.

## Frequency-semantics hierarchy

Source semantics will be determined in this order:

1. official GWAS documentation or consortium README;
2. original release documentation or header;
3. original publication or supplement;
4. explicit allele/frequency metadata;
5. reference-panel concordance as diagnostic support only.

Reference-panel concordance alone cannot be described as documented source semantics. A conflict between documentation and reference concordance stops the affected GWAS and is entered in the exception log.

## Allele-aware mapping

Every usable frequency object must contain `frequency_value` and `frequency_allele`. Standardized effect-allele frequency is calculated only when the frequency allele is known. Complementation is permitted only when the verified source frequency allele differs from the target effect allele. Minor-allele frequency without the minor-allele identity and unknown semantics are not mappable and cannot support ΔEAF filtering.

## Stage gates

1. Preserve legacy outputs and checksums as `LEGACY_INVALID_PENDING_CORRECTION`.
2. Lock this protocol and its checksum.
3. Complete and lock the frequency-semantics registry, including the dedicated CRAE audit.
4. Run harmonisation-only dry audit; do not calculate MR estimates.
5. Stop with `HOLD_FREQUENCY_SEMANTICS_UNRESOLVED` if frequency semantics required for palindromic or ΔEAF QC remain unknown.
6. Freeze the accepted dry run and harmonisation code.
7. Rerun all 224 MR directions.
8. Recompute Steiger quantities and complete-family BH-FDR.
9. Perform an independent read-only audit and freeze corrected outputs.
10. Regenerate manuscript, figures, tables and public-release materials from the corrected freeze only.

## Prohibited work

No new trait, disease, GWAS, threshold, FDR family, estimator or phenotype selection is permitted. Colocalisation, CAUSE, LCV, GSMR, MVMR, pathway analysis, enrichment and gene prioritisation remain outside scope. LDSC, retinal redundancy, HDL-L and LAVA are not rerun.

## Prospective declaration

**No corrected effect estimate had been calculated or inspected before this amendment was frozen.**

