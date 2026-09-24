# Amendment 005 final report

**Verdict:** `CAD_SENSITIVITY_STABLE_NO_MATERIAL_CHANGE` for the completed mandatory branch; `EUROPEAN_CAD_SENSITIVITY=NOT_RUN` owing to `NO_PROVENANCE_VERIFIED_MATCHED_EUROPEAN_RELEASE`. `CORE_CONCLUSION_CAD_INDEPENDENT=TRUE`; `MATERIAL_CHANGE=FALSE`. The unresolved file-level CAD N and EUR LD compatibility remain transparent limitations rather than being silently solved by this sensitivity.

The protocol was frozen before viewing sensitivity results (`config/amendment_005_cad_sensitivity.yaml`, SHA-256 `ef364bada8a2d50839dcdb3a69dd63845d2f1d1278fa564ad1723d0481ad3b10`). Frozen inputs and their recoverable snapshots are listed in `reports/AMENDMENT005_PRESTATE.md` and `archive/pre_amendment005/`. The execution script verified the lock and primary digests and matched regenerated original BH q values before writing leave-CAD-out tables.

| Primary family | Original → remaining rows | Removed CAD rows | Original corrected positives → leave-CAD-out corrected positives |
|---|---:|---:|---:|
| LDSC | 112 → 98 | 14 | 0 → 0 |
| HDL-L global-local | 116,472 → 99,126 | 17,346 | 0 → 0 |
| OCT-only MR | 112 → 98 | 14 | 0 → 0 |

Forty of the original 47 local admitted pairs remain after removing seven CAD pairs. Native LAVA provides secondary context: 26,639→22,979 rows, nine full-family positives (one CAD) versus eight non-CAD positives after exclusion, with no newly positive non-CAD native rows. The historical initial normal approximation gained two non-CAD q<0.05 rows solely because of the reduced denominator; they did not alter native or primary local conclusions.

The [consortium download page](https://cardiogramplusc4d.org/data-downloads/), [original publication](https://www.nature.com/articles/ng.3396), [GCST003116 archive](https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST003001-GCST004000/GCST003116/) and derived harmonized metadata did not provide an exact, accessible, European-only same-framework file satisfying all prospective criteria. The European replacement branch was not run, and no current-file N stress test was performed.

The next controlled step is a manuscript/release correction that clearly labels 184,305 as a publication-level fallback, states the predominantly European multi-ancestry input and EUR LD limitation, and cites the leave-CAD-out supplement. Primary estimates and q values remain primary. See `reports/AMENDMENT005_MANUSCRIPT_IMPACT.md` for wording. Any future qualifying European source requires a new source lock and CAD-only sensitivity run; it must not replace the primary dataset silently.
