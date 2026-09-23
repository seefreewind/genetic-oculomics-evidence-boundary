# Genetic oculomics evidence-boundary release

This repository contains the public reproducibility materials for a prespecified human-genetic analysis of retinal structural and retinal microvascular traits in relation to systemic disease.

The release is designed to let readers inspect the locked analysis configuration, phenotype and overlap metadata, frozen summary-result tables, instrument-level audit files, publication figures, and the scripts used to build the analyses, figures, and audit outputs. Amendment 004 prospectively restricts directional analysis to seven OCT traits with verified source allele-frequency semantics.

## What is included

- `config/`: analysis locks, phenotype registry, sample-overlap matrix, admission rules, frequency-semantic decisions, and exclusion logs.
- `metadata/`: GWAS provenance metadata and trait-level quality-control summaries.
- `results/`: frozen genome-wide correlation, local genetic-sharing, native local-inference audit, and Amendment 004 OCT-only directional MR tables.
- `tables/` and `supplementary/`: machine-readable result tables and supplementary figures.
- `figures/`: PDF, SVG, PNG, and TIFF main figures plus figure source data.
- `manuscript/hmg_amendment004/`: the editable manuscript and cover letter corresponding to the corrected evidence boundary.
- `scripts/`: analysis, harmonisation, figure, manuscript, audit, and checksum-generation code.
- `environment/`: pinned Python requirements and the recorded Python/R execution environment.
- `archive/legacy_invalid_mr/`: superseded Phase 2 and Phase 2A.1 outputs retained for provenance only and explicitly invalid for interpretation.
- `checksums/`: a checksum manifest from the complete local project artifact set.

## Reproduction notes

The analysis uses publicly released GWAS summary statistics and external EUR reference resources. The original summary-statistics files, LD panels, restricted-access files, local software environments, and large intermediate files are intentionally not redistributed here. They must be obtained from their original providers under the applicable terms. The provenance and access notes needed to identify those resources are retained in `config/phenotype_registry.tsv`, `config/analysis_lock.yaml`, and `metadata/gwas_catalog_meta/`.

The Amendment 004 scripts use paths relative to a project root. Reproduction must preserve the locked thresholds, ancestry definition, multiple-testing families, harmonisation policy, and declared analysis boundaries. Seven retinal vascular GWAS releases remain eligible for retinal redundancy, genome-wide LDSC, HDL-L, and LAVA sensitivity analyses but are excluded from MR because their release-specific allele-frequency semantics could not be resolved authoritatively.

The project intentionally does not include raw GWAS data, participant-level data, credentials, API tokens, or local absolute paths. No colocalisation, SuSiE-coloc, CAUSE, LCV, GSMR, MVMR, mediation, pathway/tissue enrichment, gene-prioritisation, or final causal-position classification is part of this release.

## Citation

Amendment 004 release `v2.0.0` is archived at DOI [10.5281/zenodo.22915396](https://doi.org/10.5281/zenodo.22915396). The concept DOI [10.5281/zenodo.22875271](https://doi.org/10.5281/zenodo.22875271) resolves to the latest version. Use `CITATION.cff` for structured citation metadata.

## Licence

Code in this repository is released under the MIT License. The included derived tables and figures remain subject to the licences and terms of the source datasets; those terms take precedence where applicable.
