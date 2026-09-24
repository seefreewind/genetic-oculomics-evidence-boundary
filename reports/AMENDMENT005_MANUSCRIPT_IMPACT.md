# Amendment 005 manuscript impact assessment — recommendations only

No manuscript, Table 1, Abstract, figures or public release was edited in this amendment. The frozen manuscript remains `PRIMARY_PRE_AMENDMENT005`, checksum `c98331f27fe4cc9a383d164e73d5044fc6519173de17c28226013bc6d375b294`.

## Recommended post-amendment changes for an explicitly authorized manuscript revision

**Table 1.** Replace 141,217 as the analysis N for the current exact CAD raw file. Proposed wording: “Publication-level total N=184,305 (60,801 cases; 123,504 controls); the archived summary-statistics file contains no sample-size field.” Ancestry: “Predominantly European multi-ancestry meta-analysis.” Do not describe 184,305 as *file-reported* or treat 141,217 as this file's N.

**Methods.** “The CAD summary statistics originated from a predominantly European multi-ancestry meta-analysis. The archived summary-statistics file did not contain an explicit sample-size field; publication-level totals were therefore used where methods required sample-size metadata. Robustness of the overall conclusions to CAD inclusion was evaluated in a prespecified leave-CAD-out sensitivity analysis.” This wording reflects the actually executed branch and does not imply that a European replacement was run.

**Results / Supplement.** “Excluding all CAD-related tests did not alter the multiplicity-controlled study-level conclusions across genome-wide, primary local or OCT-only directional analyses.” Cite `results/amendment005/LDSC_LEAVE_CAD_OUT_98.tsv`, `HDLL_LEAVE_CAD_OUT.tsv` and `MR_LEAVE_CAD_OUT_98.tsv` in Supplementary Information. Native LAVA should be described as secondary context, with its boundary flags and no newly positive non-CAD native rows. Do not place this sensitivity in the Abstract unless editorially needed.

**Limitations.** “The CAD summary statistics were derived from a predominantly European multi-ancestry meta-analysis, whereas European LD references were used for LD-dependent analyses. The prespecified leave-CAD-out sensitivity did not alter study-level multiplicity-controlled conclusions. A matched European-only CAD replacement could not be evaluated because no source met the prespecified provenance criteria.” Avoid claiming measured ancestry-mismatch bias or CAD-specific robustness to a European replacement.

**Interpretation and submission.** The central null corrected-status pattern is stable, but Table 1's current 141,217 display, exact-file N uncertainty and EUR-reference limitation still need a controlled manuscript correction before submission. Do not alter primary q values or rewrite the title/Abstract on the basis of the denominator-only sensitivity.
