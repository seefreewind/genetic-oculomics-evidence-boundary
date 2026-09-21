# Genetic oculomics evidence-boundary release

This repository contains the public reproducibility materials for a prespecified human-genetic analysis of retinal structural and retinal microvascular traits in relation to systemic disease.

The release is designed to let readers inspect the locked analysis configuration, phenotype and overlap metadata, frozen summary-result tables, instrument-level audit files, publication figures, and the scripts used to build the evidence report and figures.

## What is included

- `config/`: analysis lock, phenotype registry, sample-overlap matrix, admission rules, and exclusion log.
- `metadata/`: GWAS provenance metadata and trait-level quality-control summaries.
- `results/`: frozen genome-wide correlation, local genetic-sharing, native local-inference audit, directional MR, and CRAE–CKD instrument-audit tables.
- `tables/hmg/` and `supplementary/tables/`: machine-readable result tables.
- `figures/`: vector PDF/SVG display and supplementary figures.
- `scripts/`: report, figure, audit, and checksum-generation code.
- `checksums/`: a checksum manifest from the complete local project artifact set.

## Reproduction notes

The analysis uses publicly released GWAS summary statistics and external EUR reference resources. The original summary-statistics files, LD panels, restricted-access files, local software environments, and large intermediate files are intentionally not redistributed here. They must be obtained from their original providers under the applicable terms. The provenance and access notes needed to identify those resources are retained in `config/phenotype_registry.tsv`, `config/analysis_lock.yaml`, and `metadata/gwas_catalog_meta/`.

The scripts use paths relative to a project root and are intended for inspection and adaptation to a local checkout. The report and figure builders consume frozen result tables; they do not silently rerun statistical analyses. Reproduction should preserve the locked thresholds, ancestry definition, multiple-testing families, and declared analysis boundaries.

The project intentionally does not include raw GWAS data, participant-level data, credentials, API tokens, local absolute paths, or submission-only manuscript files. No colocalisation, SuSiE-coloc, CAUSE, LCV, GSMR, MVMR, mediation, pathway/tissue enrichment, gene-prioritisation, or final causal-position classification is part of this release.

## Citation

Please cite this repository using `CITATION.cff`. A DOI can be added after archival in a repository service such as Zenodo.

## Licence

Code in this repository is released under the MIT License. The included derived tables and figures remain subject to the licences and terms of the source datasets; those terms take precedence where applicable.
