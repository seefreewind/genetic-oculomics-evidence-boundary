# Amendment 005 leave-CAD-out sensitivity

The mandatory, prospectively locked sensitivity excluded CAD from every specified family and recomputed BH-FDR only. All 98 non-CAD LDSC r_g, SE and P values; 99,126 HDL-L block rows; 22,979 LAVA rows; and 98 non-CAD OCT-only MR estimates were carried forward from frozen tables. The run code and exact inputs are `scripts/run_amendment005_leave_cad_out.py` and `reports/AMENDMENT005_PRESTATE.md`.

## Primary corrected conclusions

- **LDSC:** 112→98 pairs; 0 FDR-positive before and 0 after exclusion. No new corrected pair.
- **HDL-L:** 116,472→99,126 block rows; 17,346 CAD rows removed; 0 global-local FDR-positive before and 0 after exclusion. No new primary local signal.
- **OCT-only MR:** 112→98 directions; 0 FDR-positive before and 0 after exclusion. No new direction. No IVW/Wald, MR-PRESSO, Steiger or clumping was rerun.

Therefore `CORE_CONCLUSION_CAD_INDEPENDENT=TRUE` under the protocol's three explicit criteria. This means the study-level *corrected-status conclusions* in these frozen non-CAD families do not depend on including CAD in the BH denominator. It does not validate the CAD-specific estimates or establish that European LD is suitable for the mixed-ancestry CAD input.

## LAVA context and boundary diagnostics

Native LAVA: 26,639→22,979 rows; 9 full-family positives (one CAD) become 8 positives among non-CAD rows, exactly the same eight non-CAD loci that were positive under old q. Initial normal approximation: 1,877 full-family positives (253 CAD) become 1,626 non-CAD positives; two are newly across the 0.05 threshold owing solely to the smaller BH family. Native results remain the sensitivity interpretation; the initial approximation is historical comparison only.

Among 22,979 non-CAD native rows, 14,515 frozen CIs touch or exceed |rho|=1, 296 raw |rho| values exceed 1 and 58 exceed 1.25. Of the eight native FDR-positive rows, seven have a CI boundary flag and four have raw |rho|>1; none has raw |rho|>1.25. These are frozen-row counts, not refitted intervals or correlations. See `results/amendment005/LAVA_LEAVE_CAD_OUT_BOUNDARY_SUMMARY.tsv`.

## Interpretation boundary

The data support **no material change in the prespecified core corrected conclusions**. The local native LAVA positives remain bounded by the existing local-parameter/CI diagnostics and do not become primary HDL-L findings. No manuscript or public repository was altered as part of the computation.
