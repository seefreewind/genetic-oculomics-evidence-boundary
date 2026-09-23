#!/usr/bin/env python3
"""Rebuild manuscript-facing Markdown after the Amendment 004 numeric freeze."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript" / "hmg_narrative_final" / "HMG_MANUSCRIPT_NARRATIVE_v3.md"
OUTDIR = ROOT / "manuscript" / "hmg_amendment004"


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(rf"(?ms)^{re.escape(start)}\n.*?(?=^{re.escape(end)}\n)")
    updated, n = pattern.subn(replacement.rstrip() + "\n\n", text)
    if n != 1:
        raise RuntimeError(f"Expected one section {start!r}, replaced {n}")
    return updated


def words(section: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", re.sub(r"\([^)]*\)", "", section)))


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    intro = re.search(r"(?ms)^## 1\. Introduction\n(.*?)(?=^## 2\.)", text).group(1)
    discussion = re.search(r"(?ms)^## 3\. Discussion\n(.*?)(?=^## 4\.)", text).group(1)
    refs = re.search(r"(?ms)^## References\n(.*?)(?=^## Figure legends)", text).group(1)
    ref_count = len(re.findall(r"^\d+\.", refs, re.M))
    intro_citations = len(re.findall(r"\([0-9][0-9,– -]*\)", intro))
    discussion_citations = len(re.findall(r"\([0-9][0-9,– -]*\)", discussion))
    diagnosis = f"""# Structure diagnosis before Amendment 004 revision

- Introduction word count: {words(intro)}
- Discussion word count: {words(discussion)}
- Discussion-to-Introduction ratio: {words(discussion)/words(intro):.2f}
- Total reference count: {ref_count}
- Introduction citation-marker count: {intro_citations}
- Discussion citation-marker count: {discussion_citations}

The Amendment 004 revision preserves the established Introduction and reference list. It revises the directional Results, Methods and Discussion so that the MR scope, evidence family and data-integrity boundary are accurate.
"""
    (ROOT / "reports" / "AMENDMENT004_STRUCTURE_DIAGNOSIS.md").write_text(diagnosis, encoding="utf-8")

    abstract = """## Abstract

Retinal imaging traits are increasingly used as systemic biomarkers, yet their position in disease biology remains uncertain. We evaluated 14 retinal traits and eight systemic diseases across complementary human-genetic analyses. None of 112 genome-wide genetic correlations survived false-discovery-rate correction. Primary local analysis of 47 prespecified pairs yielded no corrected signal across 116,472 block tests. In the same 26,639-row sensitivity universe, a historical local-correlation procedure identified 1,877 false-discovery-rate-significant tests, whereas native LAVA inference identified nine; eight of the nine had confidence intervals touching the |rho|=1 boundary. Directional analyses were prospectively restricted to seven optical coherence tomography traits for which source allele-frequency semantics could be verified. Across 112 bidirectional tests, 110 directions were null and two were suggestive; none survived global correction. Seven retinal vascular GWAS releases were retained in correlation analyses but excluded from Mendelian randomization because release-specific allele-frequency coding could not be resolved unambiguously. Thus, genome-wide, primary local and data-integrity-qualified directional analyses yielded no multiplicity-controlled evidence supporting broad shared architecture or robust directional relationships. These findings constrain causal interpretation of the retinal traits studied here without diminishing their potential observational or predictive value as systemic biomarkers.

**Keywords:** retinal imaging; genetic correlation; local genetic correlation; Mendelian randomization; optical coherence tomography; systemic disease"""
    text = replace_section(text, "## Abstract", "## 1. Introduction", abstract)

    results = """### 2.4 Directional analysis was restricted to data-integrity-qualified OCT traits

A pre-submission harmonisation audit identified an unresolved discrepancy between the GWAS-SSF frequency-field definition and external allele-frequency concordance for seven retinal vascular GWAS releases. No authoritative release-specific mapping was available. Their frequency coding was therefore not inferred from reference-panel concordance, and the vascular traits were excluded prospectively from MR while remaining in the genome-wide and local-correlation analyses.

The Amendment 004 MR universe comprised seven primary OCT traits and the same eight systemic diseases, giving 112 bidirectional tests across 56 pairs. All 112 directions retained at least seven instruments after harmonisation. None survived Benjamini-Hochberg correction across the complete 112-test family. Of the 112 directions, 110 were null and two were suggestive (Supplementary Table S8; Supplementary Fig. S2). The suggestive directions were ischemic stroke→total macular thickness (7 instruments; beta=0.0984, SE=0.0408, P=0.0158, q=0.963) and INL thickness→CKD (59 instruments; beta=-0.0725, SE=0.0322, P=0.0243, q=0.963). Neither was treated as a discovery.

Steiger directionality was estimable for 98 directions; 95 supported the specified direction at P<0.05. This orientation evidence did not override the primary false-discovery-rate result. MR-PRESSO completed for all 112 directions without flagging an outlier. The full harmonisation record and sensitivity diagnostics are provided in Supplementary Tables S8 and S9.

### 2.5 Integrated interpretation

Genome-wide analysis showed no multiplicity-controlled shared architecture, and primary local analysis identified no corrected shared loci. LAVA sensitivity findings remained procedure- and boundary-sensitive. Data-integrity-qualified OCT-only MR produced no globally corrected directional signal. Directional evidence for the seven vascular traits was not classified as null because those datasets were not analysed by MR. The retinal traits therefore remain compatible with observational, predictive, downstream or pleiotropic roles, but this study does not establish them as genetically supported intermediates in systemic disease (Table 2)."""
    text = replace_section(text, "### 2.4 Bidirectional MR yielded no robust directional relationship", "## 3. Discussion", results)

    principal = """### 3.1 Principal interpretation

Across complementary human-genetic evidence layers, we found little cross-method support for a broad causal interpretation of retinal phenotypes in systemic disease. None of the 112 genome-wide pairs or 116,472 primary HDL-L block tests survived their respective correction procedures. Native LAVA sensitivity findings were sparse and predominantly boundary-sensitive. Within the prospectively restricted OCT-only MR family, no direction survived correction across 112 tests. The results narrow the mechanistic claim: within the available common-variant resources, structurally defined OCT traits were not established as directional intermediates in the eight systemic diseases studied.

This conclusion does not diminish the observational or predictive value of retinal imaging. Retinal structure and vascular morphology can remain sensitive readouts of vascular, metabolic, neural and inflammatory states even when inherited variation does not support the retina as a mediator of systemic disease risk. Such readouts may reflect downstream injury, accumulated exposure, treatment effects or pleiotropic biology. The relevant distinction is between what the retina records and what it causally transmits. Human genetics informs the second proposition, while prediction and monitoring can remain useful when that proposition is unsupported.

The directional boundary differs by retinal domain. Neuroretinal and outer-retinal OCT traits entered the Amendment 004 MR analysis because their source frequency coding was verifiable. Microvascular traits remained in genome-wide and local analyses, but their directional relationships were not evaluated because seven release-specific allele-frequency mappings could not be resolved authoritatively. These cells represent unavailable directional inference, not null evidence."""
    text = replace_section(text, "### 3.1 Principal interpretation", "### 3.2 Relation to prior retinal–systemic genetics", principal)

    why = """### 3.3 Why apparent signals did not support stronger biological claims

Across local and directional analyses, statistical evidence depended on the validity of its inferential layer. In local analysis, correlation estimates can become unstable when local heritability is low, linkage disequilibrium is imperfectly represented or a parameter approaches its boundary. Replacing the historical approximation with native LAVA inference reduced 1,877 false-discovery-rate-significant rows to nine in an identical row universe, and eight of the nine touched the correlation boundary. The primary HDL-L framework independently yielded no corrected result. Prior methodological work has shown that local-correlation procedures can differ in calibration, efficiency and shared-locus identification because their assumptions and reference structures differ (8,12). Procedure- or boundary-sensitive signals therefore require matched linkage-disequilibrium support and independent stability before locus-level interpretation.

At the directional layer, the decisive issue was source-data integrity. Seven vascular releases carried a field named `effect_allele_frequency`, but its documented meaning conflicted systematically with external allele-frequency concordance. Reference concordance alone could not establish which labelled allele the released value counted. Inferring the mapping through `1-f`, suppressing frequency checks or replacing the GWAS would have changed the analysis in a result-dependent manner. The vascular MR family was therefore closed without corrected estimates, and Amendment 004 was frozen before any OCT-only result was calculated.

Within the qualified OCT universe, two directions reached nominal significance, but neither survived correction across the complete 112-test family. Steiger orientation and sensitivity analyses were interpreted as supporting diagnostics rather than substitutes for the primary multiplicity-controlled result. This distinction avoids promoting nominal or orientation-supported associations to causal findings."""
    text = replace_section(text, "### 3.3 Why apparent signals did not support stronger biological claims", "### 3.4 Strengths, limitations and next evidence", why)

    limits = """### 3.4 Strengths, limitations and next evidence

The study has several strengths. A prespecified full matrix limited selective emphasis on positive pairs, and complete multiplicity correction retained null and unresolved findings. Retinal redundancy control reduced duplication among correlated traits. Genome-wide, primary local, sensitivity local and directional analyses addressed distinct aspects of the same question. The pre-submission frequency-semantic audit exposed a source-level ambiguity before manuscript submission, and Amendment 004 restricted MR prospectively rather than inferring allele coding from the desired result.

Five limitations define the scope of the conclusions. First, the retinal GWASs were concentrated in participants of European ancestry and UK Biobank imaging resources, limiting population portability. Second, public metadata documented no UK Biobank contribution to the selected systemic releases but could not exclude residual overlap through incompletely reported cohorts. Third, correction across complete testing families increased specificity at a cost to power for modest or sparse effects. Fourth, a UK Biobank-matched local linkage-disequilibrium sensitivity analysis could not be performed with the available legal local resources. Fifth, directional inference was restricted to structural OCT traits because release-specific allele-frequency coding for seven vascular datasets could not be resolved to a standard sufficient for MR harmonisation. This reduced vascular directional coverage but avoided an allele mapping based on inference alone. Common-variant summary statistics also cannot resolve rare-variant, acquired, developmental, epigenetic or cell-specific mechanisms.

The next decisive evidence is phenotype-matched independent replication, more diverse retinal GWASs, reference-matched local analyses and authoritative release metadata for vascular summary statistics. The last resource would permit vascular MR without inferred frequency coding. Retinal imaging may remain valuable for screening, prediction and physiological monitoring even when genetic directionality is unsupported. Current human-genetic evidence therefore constrains mechanistic interpretation while preserving the biomarker rationale for retinal imaging."""
    text = replace_section(text, "### 3.4 Strengths, limitations and next evidence", "## 4. Materials and Methods", limits)

    qc = """### 4.2 GWAS resources, quality control and data-integrity restriction

Summary statistics were harmonized to GRCh37 and assessed for variant identifiers, alleles, effect estimates, standard errors, P values, sample-size fields and duplicate variants. Variants incompatible with the reference or unresolved after harmonisation were excluded under prespecified rules. Retinal GWASs used UK Biobank imaging participants. For each systemic resource, publications, consortium descriptions and metadata were reviewed for documented UK Biobank participation. The selected primary disease releases had no documented UK Biobank contribution, although residual overlap through incompletely reported cohorts could not be excluded.

During pre-submission harmonisation audit, seven retinal vascular GWAS releases showed an unresolved discrepancy between the GWAS-SSF field definition and external allele-frequency concordance. No authoritative release-specific mapping or original export code was available. These traits were retained in retinal redundancy, genome-wide and local-correlation analyses but excluded from MR. This restriction was formalized in Amendment 004 before any OCT-only MR result was calculated. For the seven OCT sources, official fastGWA documentation and source headers established that `A1` was the effect allele and `AF1` its frequency. Systemic releases without source frequency fields were not assigned constructed EAF values; reference-panel fallback was used only when explicit allele identity permitted mapping, and unresolved palindromic variants were excluded."""
    text = replace_section(text, "### 4.2 GWAS resources, quality control and overlap", "### 4.3 Genome-wide genetic correlation", qc)

    mrmethod = """### 4.5 Data-integrity-qualified bidirectional MR

Directional analysis included the seven primary OCT traits with verified source frequency semantics and the same eight systemic diseases, producing 7×8×2=112 directions. The seven vascular traits were not analysed by MR. Genome-wide-significant exposure variants were clumped at the original Phase 2A threshold against the same European reference, matched to outcomes, aligned to the exposure effect allele and screened under the frozen palindromic and absolute ΔEAF >0.20 rules. Frequency was represented as a value paired with its allele identity and standardized to the effect allele only after mapping.

Inverse-variance weighting with random effects was prespecified when at least two instruments remained, and the Wald ratio was reserved for one instrument. Weighted-median, weighted-mode, MR-Egger, Cochran Q, Egger-intercept, leave-one-out and MR-PRESSO analyses were run only at the original instrument-count requirements. Steiger exposure and outcome variance explained, direction and P values were recomputed from the Amendment 004 instrument set. Primary P values were adjusted by Benjamini-Hochberg correction across the complete 112-direction family. Results were classified as null, suggestive, unresolved or directional-MR-supported under the original thresholds. The 112-test q values are specific to Amendment 004 and were not compared numerically with the superseded 224-test family as evidence of increased significance."""
    text = replace_section(text, "### 4.5 Bidirectional MR and CRAE–CKD audit", "### 4.6 Reproducibility and data availability", mrmethod)

    repro = """### 4.6 Reproducibility and data availability

Analysis scripts, frozen configurations, frequency-semantic registries, harmonisation records, complete testing-family outputs and shareable derived data were archived. Tables and figures were generated from the Amendment 004 result freeze, and no post hoc phenotype, outcome, instrument, threshold or estimator substitution was made. The public repository is https://github.com/seefreewind/genetic-oculomics-evidence-boundary. The historical Zenodo record is doi:10.5281/zenodo.22875272; the Amendment 004 package requires a new versioned release before submission. Source GWAS summary statistics remain governed by their originating repositories and licences."""
    text = replace_section(text, "### 4.6 Reproducibility and data availability", "## Funding", repro)

    text = text.replace(
        "OpenAI GPT-5.6 and DeepSeek V4 Flash were used under author direction to assist with code writing, manuscript formatting and language editing.",
        "OpenAI Codex (model: GPT-5.6) and DeepSeek (model: V4 Flash) were used under author direction to assist with code writing, debugging, workflow orchestration, manuscript formatting and language editing. The analysis plan and thresholds were author-defined."
    )
    text = text.replace(
        "Reproducible code and shareable derived data are available at https://github.com/seefreewind/genetic-oculomics-evidence-boundary and archived at Zenodo (doi:10.5281/zenodo.22875272). Source GWAS summary statistics remain available under the terms of their originating studies and repositories.",
        "Derived result tables, analysis configurations, audit scripts, figure-generation scripts and checksums are available at https://github.com/seefreewind/genetic-oculomics-evidence-boundary. The historical Zenodo record is doi:10.5281/zenodo.22875272; a manuscript-compatible Amendment 004 version will be deposited before submission. Source GWAS summary statistics remain available under the terms of their originating studies and repositories."
    )

    legends = """## Figure legends

**Figure 1. Complementary evidence framework with data-integrity-qualified directionality.** Retinal phenotypes span neuroretinal, outer-retinal and microvascular domains, while systemic contexts span cardiovascular, metabolic, renal, neurodegenerative and immune or inflammatory disease. Genome-wide sharing was evaluated across all 14 retinal traits and eight diseases (112 pairs), and local analysis retained the locked 47-pair subset. Directional MR was restricted prospectively to seven OCT traits with verifiable source allele-frequency semantics (112 directions). The seven vascular traits remained in correlation analyses but were not evaluated by MR. *Alt text:* Three parallel evidence layers distinguish the full retinal panel used for global and local analyses from the seven-trait OCT subset used for directional MR.

**Figure 2. Integrated evidence after Amendment 004.** Genome-wide sharing included 112 pairs with no FDR-significant result. Primary HDL-L included 116,472 block tests with no global-local FDR-significant result. Native LAVA sensitivity analysis included 26,639 rows, with nine FDR-significant rows of which eight were boundary-sensitive. OCT-only directional MR included 112 directions, with 110 null and two suggestive classifications and no FDR-positive direction. Seven vascular traits were excluded from directional analysis because release-specific allele-frequency semantics remained unresolved. Track positions are categorical and do not represent comparable discovery proportions across different testing universes. *Alt text:* Four non-proportional evidence tracks show the testing universe, corrected result and bounded interpretation for genome-wide, primary local, LAVA sensitivity and OCT-only MR analyses.

**Figure 3. Local retinal–systemic evidence was sensitive to inference procedure and testing framework.** (A) Historical approximation and native LAVA are compared only within the same 26,639-row universe, yielding 1,877 and nine FDR-significant rows, respectively. (B) Native LAVA boundary diagnostics show 16,938 confidence intervals touching or exceeding |rho|=1, 347 raw estimates with |rho|>1 and 68 with |rho|>1.25; 63.6% of native rows had a confidence interval touching or exceeding the boundary. (C) The primary HDL-L analysis completed 116,472 block tests and yielded no global-local FDR-significant result. HDL-L and LAVA use different local testing universes and are not interpreted as denominator-matched discovery-rate comparisons. Vascular traits remained eligible for the originally admitted local pairs. *Alt text:* A dot comparison preserves visibility of nine native LAVA rows, a bar chart reports boundary behavior, and a separate information panel reports the primary HDL-L result.

## Supplementary figure legends

**Supplementary Figure S1. Genome-wide genetic-correlation matrix.** The heatmap displays the 112 retinal–systemic LD Score regression estimates. Outlines identify nominal P<0.05 cells; none survived FDR correction across the complete 112-pair family. Color encodes the estimated genetic correlation and does not indicate corrected significance.

**Supplementary Figure S2. Final directional-evidence matrix.** OCT cells summarize classifications from the 112-direction Amendment 004 family. Vascular cells are labelled not analysed because source allele-frequency semantics remained unresolved; they must not be interpreted as null. No OCT direction survived global FDR correction."""
    text = replace_section(text, "## Figure legends", "## Tables", legends)

    tables = """## Tables

**Table 1. Dataset-level inventory of retinal and systemic GWAS resources.** Trait-specific analysis N was not available in the prespecified registry for the Zhao et al. OCT traits; the release-level mean of 60,748 is shown. Sample size varied by vascular phenotype. UK Biobank status describes participation in the source GWAS, not pairwise overlap.

**Table 2. Retinal-domain interpretation boundary.** Neuroretinal and outer-retinal OCT traits were analysed in Amendment 004 MR. Microvascular traits remained in global and originally admitted local analyses but were not evaluated by MR because release-specific allele-frequency semantics could not be resolved authoritatively. Global evidence covers all 112 retinal-disease pairs, local evidence covers the locked 47-pair subset, and directional evidence covers the complete 112-direction OCT-only family."""
    text = re.sub(r"(?ms)^## Tables\n.*\Z", tables.rstrip() + "\n", text)

    # Remove citations from Methods in accordance with the project manuscript rules.
    methods_match = re.search(r"(?ms)(^## 4\. Materials and Methods\n.*?)(?=^## Funding)", text)
    methods = re.sub(r"\s*\([0-9][0-9,– -]*\)", "", methods_match.group(1))
    text = text[:methods_match.start(1)] + methods + text[methods_match.end(1):]

    OUTDIR.mkdir(parents=True, exist_ok=True)
    manuscript = OUTDIR / "HMG_MANUSCRIPT_AMENDMENT004.md"
    manuscript.write_text(text, encoding="utf-8")

    cover = """# Cover letter

Dear Editors,

We submit “Human genetic evidence constrains causal interpretation of retinal traits in systemic disease” for consideration as an Original Article in *Human Molecular Genetics*.

This study evaluates 14 retinal imaging traits and eight systemic diseases across genome-wide genetic correlation, primary and sensitivity local genetic correlation, and bidirectional Mendelian randomization. None of 112 genome-wide pairs or 116,472 primary HDL-L block tests survived the relevant correction procedures. Native LAVA findings were sparse and predominantly boundary-sensitive. Directional analysis was prospectively restricted to seven structural OCT traits with verifiable source allele-frequency coding. Across 112 OCT-only directions, no association survived global false-discovery-rate correction.

As part of pre-submission quality control, seven retinal vascular GWAS releases were excluded from MR because source allele-frequency semantics could not be resolved authoritatively. These traits remained in the genome-wide and local-correlation analyses. This data-integrity restriction was formalized before OCT-only MR results were calculated, and the complete harmonisation and Amendment 004 records are included in the reproducibility package.

The manuscript has not been published and is not under consideration elsewhere. All authors have approved the manuscript and agree with its submission. There is no related preprint, thesis, conference abstract or overlapping manuscript. The authors declare no competing interests and received no specific funding for this work.

OpenAI Codex (model: GPT-5.6) and DeepSeek (model: V4 Flash) assisted with code writing, debugging, workflow orchestration, manuscript formatting and language editing under author direction. The analysis plan and thresholds were author-defined, all outputs were independently reviewed by the authors, and the authors take full responsibility for the work.

Thank you for considering our manuscript.

Sincerely,

Yu Zhang  
Corresponding author  
Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University  
zhangyu1@wzhealth.com  
ORCID: https://orcid.org/0000-0001-8579-3692
"""
    (OUTDIR / "HMG_COVER_LETTER_AMENDMENT004.md").write_text(cover, encoding="utf-8")
    print(manuscript)


if __name__ == "__main__":
    main()
