# Public release status

Release version: 2.1.0

Release date: 2026-09-24

Repository: `seefreewind/genetic-oculomics-evidence-boundary`

Historical Zenodo archive: [10.5281/zenodo.22875272](https://doi.org/10.5281/zenodo.22875272)

Amendment 004 Zenodo version: [10.5281/zenodo.22915396](https://doi.org/10.5281/zenodo.22915396)

Concept DOI for all versions: [10.5281/zenodo.22875271](https://doi.org/10.5281/zenodo.22875271)

The frozen public package contains 112 genome-wide correlation pairs, 116,472 primary local tests, 26,639 native local-audit rows, and 112 OCT-only bidirectional MR directions. The directional family comprises seven OCT traits and eight systemic diseases in both directions: 110 directions were null, two were suggestive, and none survived false-discovery-rate correction. Steiger directionality was estimable for 98 directions and supported the specified direction at P<0.05 for 95. Seven retinal vascular traits were not analysed by MR because their release-specific allele-frequency semantics remained unresolved.

Amendment 003 is closed without corrected vascular MR. Superseded Phase 2 and Phase 2A.1 files are retained only under `archive/legacy_invalid_mr/` and must not be used for scientific interpretation.

The source GWAS summary-statistics files and LD-reference panels are not redistributed. Provenance, access status, sample-overlap metadata, thresholds, and derived result tables are included so that the analysis boundary can be audited without exposing restricted or unnecessarily large source files.

The package is a reproducibility release, not a clinical validation dataset. Its controlling directional verdict is `NO_ROBUST_OCT_DIRECTIONAL_SIGNAL`. Vascular directional cells are unavailable, not null. The release does not establish clinical utility, therapeutic readiness, or a final DRIVER/TARGET/BYSTANDER classification.

Amendment 005 is an additive sensitivity. Its protocol was frozen before inspecting sensitivity results. Excluding CAD left 98 LDSC pairs, 99,126 HDL-L block rows, 22,979 native LAVA rows and 98 OCT-only MR directions. The non-CAD LDSC, primary HDL-L and OCT-only MR families each retained zero FDR-positive results; `CORE_CONCLUSION_CAD_INDEPENDENT=TRUE` under the prespecified criterion. Eight native LAVA non-CAD rows remained FDR-positive as secondary context, with existing boundary diagnostics. No matched European-only Nikpay 2015 CAD file passed the provenance gate, so European-CAD replacement was not run. Primary results, the historical v2.0.0 version and the unresolved exact-file CAD N are retained.
