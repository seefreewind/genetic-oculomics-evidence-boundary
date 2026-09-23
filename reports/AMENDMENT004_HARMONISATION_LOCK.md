# Amendment 004 harmonisation lock

Status: **LOCKED_FOR_MR**

The prospective harmonisation-only dry run passed before any Amendment 004 MR effect estimate was calculated or inspected.

## Locked universe

- Included retinal traits: 7 primary OCT structural traits
- Included systemic diseases: 8 frozen releases
- Retinal–disease pairs: 56
- Bidirectional tests: 112
- Directions represented in dry run: 112
- Directions with zero retained instruments: 0

## Frequency semantics

- OCT confirmation: 7/7 `PASS`
- OCT source representation: `A1` effect allele, `A2` other allele, `AF1` frequency of `A1`
- Systemic source semantics: inherited from the frozen Amendment 003 registry
- No source frequency was fabricated for T2D, AD, SLE or IBD
- Reference fallback used only with explicit 1KG EUR REF/ALT identity
- Frequency-semantic warnings: 0/112 directions

## Dry-run counts

- Candidate instrument-direction records: 4,868
- Retained instrument-direction records: 3,901
- Missing outcome variants: 688
- Palindromic ambiguous removals: 272
- Incompatible-allele removals: 7
- ΔEAF > 0.20 removals: 0
- Final instruments per direction: range 7–90
- Maximum retained ΔEAF: 0.171647

## Locked checksums

- Amendment configuration: `5a5847de62f5781c70f64ea4d85f7cc24990147cb81faa537de3554b02e61a9c`
- OCT semantics confirmation: `59ba67b3aeb7265f558eb6ad4a6cf27d44b27f57924916ba60a0cb08f1f17466`
- Harmonisation dry-run master: `2c3cae8d5477003cd8eee55a5c92928b9030032337f6d97ce204d141c492b40e`
- Harmonisation summary: `5c19c0383cfe5f10a5cbc3ac865a09a4a5f0ab7944879eab5634f79a7d0366eb`
- Harmonisation/MR script: `fe104e99aa656a139e0096bfcb69bf95dfad369e7acfc2b3c34918bbce3659f3`
- Frequency semantics registry: `2ac893b3994af1034b08380cd3d889385dcbfe6b8a748d5576ed512f40af5a08`

Any subsequent change to frequency mapping, allele alignment, palindromic handling, ΔEAF filtering, instrument thresholds, clumping, estimators or multiplicity requires a new amendment. The MR stage must reproduce this dry-run table exactly before estimating effects.
