# AMENDMENT 003 STATUS

**HOLD_FREQUENCY_SEMANTICS_UNRESOLVED**

Amendment 003 was prospectively frozen before any corrected MR effect was calculated or inspected. Legacy Phase 2A/2A.1 outputs remain preserved and labelled `LEGACY_INVALID_PENDING_CORRECTION`. The analysis stopped at the prespecified semantic-conflict gate. No corrected harmonisation dry run, MR estimate, Steiger result, q value, classification, figure, manuscript number, public release, or Zenodo version was generated.

# FREQUENCY SEMANTICS REGISTRY

The registry contains exactly 22 unique primary GWAS sources: 14 retinal traits and 8 systemic diseases. It is stored at `config/frequency_semantics_registry.tsv` (SHA256 `2ac893b3994af1034b08380cd3d889385dcbfe6b8a748d5576ed512f40af5a08`).

- 7 OCT fastGWA sources: `EFFECT_ALLELE`, high confidence, based on official GCTA output documentation linking `AF1` to `A1`.
- CAD, stroke, CKD and PD: `EFFECT_ALLELE`, moderate-to-high confidence, based on explicit release headers or official GWAS-SSF documentation. Reference-panel concordance supports CAD, stroke and CKD at 41/41, 10/10 and 22/23 informative leads, respectively.
- T2D, AD, SLE and IBD: no source frequency field. Their registry value is `UNKNOWN`, but this is not itself a semantic blocker because no unlabelled source frequency would be used; any reference-panel fallback must retain explicit REF/ALT allele identity.
- 7 retinal vascular GWAS: `UNKNOWN`, `UNRESOLVED`, because higher-priority documentation conflicts with the diagnostic reference-panel evidence.

# CRAE FREQUENCY SEMANTICS

The GWAS-SSF v1.0 field definition identifies `effect_allele_frequency` as the frequency of the labelled `effect_allele`. In contrast, all six frozen CRAE lead variants have source frequencies close to the labelled `other_allele` frequency in 1KG EUR:

| SNP | Source EA/OA | Source frequency | 1KG-matching allele | 1KG frequency |
|---|---|---:|---|---:|
| rs17421627 | T/G | 0.069742 | G (OA) | 0.0646123 |
| rs1800407 | C/T | 0.079698 | T (OA) | 0.0755467 |
| rs4284049 | G/T | 0.187260 | T (OA) | 0.2147120 |
| rs4745951 | A/G | 0.798410 | G (OA) | 0.7962230 |
| rs475377 | T/C | 0.472300 | C (OA) | 0.4860830 |
| rs9330813 | G/A | 0.311460 | A (OA) | 0.3111330 |

The conclusion is `SEMANTIC_CONFLICT`, not `OTHER_ALLELE`. Reference-panel concordance is diagnostic support only and cannot override the official field definition. The six-SNP audit is stored at `results/amendment003/CRAE_FREQUENCY_SEMANTICS_AUDIT.tsv` (SHA256 `8ecf2336dc505ada3e43228989bf7d1f937e8a4a3a577481b8e19c6aa5e5c4da`). CRAE MR was not run.

# HARMONISATION DRY RUN

Not run. The protocol requires source semantics to be locked before any frequency-based dry harmonisation. Seven primary retinal vascular GWAS failed that gate. Consequently, `HARMONISATION_DRY_RUN_MASTER.tsv`, `HARMONISATION_CHANGE_SUMMARY.tsv`, the CRAE–CKD corrected pre-MR trace and the harmonisation lock were not created.

# 224-DIRECTION COMPLETION

Corrected directions completed: **0/224**. The seven affected retinal vascular traits participate in 56 retinal–disease pairs and 112 bidirectional directions. A complete-family rerun cannot be validly completed while these sources are blocked. The unaffected half was not run separately because Amendment 003 prespecifies one complete 224-direction reanalysis and one BH family.

# OLD VS CORRECTED MR

No corrected MR estimates exist, so no scientific old-versus-corrected comparison was made. The legacy counts—219 `NULL`, 4 `SUGGESTIVE`, 1 `UNRESOLVED`—remain historical comparison values only and are not valid corrected results.

# CORRECTED FDR RESULTS

Not available. BH-FDR was not recomputed because the complete corrected 224-direction primary family was not generated. Old q values must not be reused.

# CORRECTED CRAE→CKD RESULT

Not available. The old `427 → 6 → 1` trace and its single-IV result remain invalid pending correction. It is not yet defensible to complement the six source frequencies, restore variants, or report a corrected CRAE→CKD instrument count or effect.

# STEIGER RESULTS

Not available. Steiger R², direction and P values were not recomputed. The old CRAE/CKD R² values must not be copied into a corrected manuscript.

# MANUSCRIPT IMPACT

The manuscript remains on hold. Abstract, Results 2.4–2.6, the MR Discussion paragraph, Conclusion and cover letter cannot be regenerated from corrected results. Global LDSC, HDL-L and LAVA outputs were not touched and remain valid under the existing audit, but they cannot substitute for the blocked MR evidence layer.

# FIGURE/TABLE IMPACT

- Old Figure 4 remains `INVALID_PENDING_CORRECTION`; no corrected Figure 4 was generated.
- Figure 2 MR track was not updated.
- Table 2 directional-evidence column was not updated.
- Supplementary Tables S8–S10 were not replaced.

# PUBLIC RELEASE STATUS

No new GitHub release or Zenodo version was created. The existing public release still contains disputed MR/CRAE artifacts and must not be represented as the corrected Amendment 003 release. The verified author-code evidence archive is recorded in `metadata/amendment003_sources/SOURCE_ARCHIVE_AUDIT.tsv`; it contains phenotype extraction code but no GWAS export/allele-frequency mapping.

# REMAINING BLOCKERS

The single blocking issue is authoritative allele-frequency semantics for these seven GCST releases:

- GCST90446760 — arteriolar tortuosity
- GCST90446761 — venular tortuosity
- GCST90446763 — CRAE
- GCST90446764 — CRVE
- GCST90446765 — AVR
- GCST90446768 — arterial density
- GCST90446769 — venular density

Required evidence is an authoritative, release-specific statement or mapping from the data generator, GWAS Catalog curation record, consortium README, or original GWAS export script that identifies which labelled allele the numeric `effect_allele_frequency` actually counts. The key question is whether the seven submitted files had their effect/other allele columns swapped, their frequency column mislabeled, or another release transformation applied. A generic GWAS-SSF definition or reference-panel inference alone is insufficient.

All exceptions are recorded in `reports/AMENDMENT003_EXCEPTION_LOG.tsv`. Once authoritative mapping is supplied, the next allowed action is to update the registry under a documented resolution, implement the allele-aware frequency object, run and freeze the 224-direction dry harmonisation, and only then rerun MR.

# SUBMISSION READINESS

**Not ready for submission. Final status: `HOLD_FREQUENCY_SEMANTICS_UNRESOLVED`.**

No prohibited analyses were run. No existing LDSC, HDL-L or LAVA result was modified. No new phenotype, GWAS, threshold, estimator or FDR family was introduced.
