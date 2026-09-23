# Amendment 004 final quality-control report

## Controlling decision

- Amendment 003: `CLOSED_WITHOUT_CORRECTED_MR`
- Amendment 003 reason: `AUTHORITATIVE_FREQUENCY_MAPPING_UNAVAILABLE`
- Amendment 004 verdict: `NO_ROBUST_OCT_DIRECTIONAL_SIGNAL`
- Vascular directional status: `NOT_ANALYSED_FREQUENCY_SEMANTICS_UNRESOLVED`

## Protocol and harmonisation lock

- Amendment 004 was frozen before any OCT-only MR estimate was calculated or inspected.
- Protocol SHA256: `5a5847de62f5781c70f64ea4d85f7cc24990147cb81faa537de3554b02e61a9c`.
- Seven of seven OCT sources passed the source frequency-semantic confirmation.
- The allele-aware dry run covered all 112 directions and left no zero-instrument direction.
- Candidate instrument-direction rows: 4,868; retained: 3,901; missing outcome: 688; ambiguous palindromic: 272; incompatible allele: 7; removed by absolute delta-EAF greater than 0.20: 0.
- Final instrument count per direction ranged from 7 to 90.

## Corrected MR family

- Directions completed: 112 of 112.
- Retinal–disease pairs completed: 56 of 56.
- Primary estimator: random-effects inverse-variance weighting for all 112 directions.
- Evidence classes: 110 null, 2 suggestive, 0 directional-MR-supported.
- FDR-positive directions: 0.
- Suggestive directions: ischemic stroke to total macular thickness, P=0.0158 and q=0.963; INL thickness to CKD, P=0.0243 and q=0.963.
- Steiger estimable: 98 directions; direction supported: 98; direction supported at P<0.05: 95.
- MR-PRESSO completed for all 112 directions and flagged no outlier.
- Invalid numeric outputs: 0.

## Excluded vascular MR family

- Seven vascular traits across eight diseases in two directions produced 112 explicit `not analysed` rows.
- Exclusion reason is uniform: `UNRESOLVED_RELEASE_SPECIFIC_ALLELE_FREQUENCY_SEMANTICS`.
- These rows are unavailable directional evidence and are not classified as null.

## Manuscript and figure consistency

- The manuscript reports 112 OCT-only directions, 110 null and 2 suggestive results, and no FDR-positive direction.
- Superseded CRAE-to-CKD, rs475377, single-instrument Wald and corrected 224-direction claims are absent from the scientific interpretation.
- Introduction word count: 599; Discussion word count: 1,100; ratio: 1.84.
- The editable manuscript and cover letter were rendered and visually inspected page by page: 14 manuscript pages and 1 cover-letter page, with no clipping, overlap or missing glyphs.
- Three main figures and one Amendment 004 supplementary directional matrix passed visual and automated quality checks.

## Release integrity

- Superseded Phase 2 and Phase 2A.1 MR files are retained only under `archive/legacy_invalid_mr/` for provenance.
- Active release paths contain the Amendment 004 protocol, harmonisation records, complete corrected result family, manuscript, tables, figures, source data and scripts.
- Raw GWAS summary statistics, participant-level data, credentials and local absolute paths are excluded from the public package.

## Public release

- GitHub release: `v2.0.0`, published 23 September 2026.
- GitHub release URL: https://github.com/seefreewind/genetic-oculomics-evidence-boundary/releases/tag/v2.0.0
- Amendment 004 Zenodo version DOI: `10.5281/zenodo.22915396`.
- Concept DOI for all versions: `10.5281/zenodo.22875271`.
- Zenodo file: `seefreewind/genetic-oculomics-evidence-boundary-v2.0.0.zip`, 16.1 MB, public open access.

Final QC status: `PASS`
