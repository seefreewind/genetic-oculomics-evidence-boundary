# Amendment 005 exclusion counts and frozen-row integrity

The locked protocol (`config/AMENDMENT005.sha256`) and all prespecified input digests passed before any sensitivity output was written. Original q values were independently regenerated from frozen P values using the original finite-P BH rule and matched the frozen columns to the script's numerical tolerance. Non-CAD estimates, SEs and P values were copied rather than re-estimated.

| Family | Original rows | CAD rows removed | Remaining rows | Finite P values in remaining rows | Original full-family FDR positives | CAD positives removed | Remaining positives under old q | Positives under new q |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LDSC global | 112 | 14 | 98 | 98 | 0 | 0 | 0 | 0 |
| HDL-L global-local | 116,472 | 17,346 | 99,126 | 12,294 | 0 | 0 | 0 | 0 |
| LAVA native, context | 26,639 | 3,660 | 22,979 | 22,921 | 9 | 1 | 8 | 8 |
| LAVA initial normal approximation, historical context | 26,639 | 3,660 | 22,979 | 22,921 | 1,877 | 253 | 1,624 | 1,626 |
| OCT-only MR | 112 | 14 | 98 | 98 | 0 | 0 | 0 | 0 |

The locked Phase 1B set contains 47 admitted pairs, including **7 CAD pairs**, leaving 40 non-CAD pairs. The HDL-L finite-P denominator is 12,294, not the 99,126 physical rows; BH follows the original pipeline's finite-P rule and preserves missing-q rows. The corresponding native and initial LAVA finite-P denominator is 22,921. The 14 MR CAD directions comprise the two directions for each of the seven OCT traits.

Two CKD–venous tortuosity loci, `1170` and `2445`, cross q<0.05 in the **historical initial normal approximation only** after the denominator changes (old q 0.050111→new 0.049953; old q 0.050043→new 0.049889). They do not create new native LAVA positives and do not enter the prespecified core-conclusion Boolean. These q changes do not represent newly estimated biological effects.
