# Human genetic evidence constrains causal interpretation of retinal traits in systemic disease

## Title page

**Authors:** Da Lin¹, Ying Chen², Yue Liu², Yu Zhang¹

**Affiliations:** ¹ Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China; ² Wenzhou Medical University, Wenzhou, Zhejiang Province, China

**Corresponding author:** Yu Zhang; email: zhangyu1@wzhealth.com; ORCID: https://orcid.org/0000-0001-8579-3692

**Article type:** Original Article

## Abstract

Retinal imaging traits are increasingly used as systemic biomarkers, yet their position in disease biology remains uncertain. We evaluated 14 retinal traits and eight systemic diseases across complementary human-genetic analyses. None of 112 genome-wide genetic correlations survived false-discovery-rate correction. Primary local analysis of 47 prespecified pairs yielded no corrected signal across 116,472 block tests. In the same 26,639-row sensitivity universe, the normal-approximation P values used in the initial workflow yielded 1,877 tests passing FDR correction, whereas native LAVA bivariate inference yielded nine; eight of the nine had confidence intervals touching the |rho|=1 boundary. Directional analyses were prospectively restricted to seven OCT traits with verifiable source allele-frequency coding. Across 112 bidirectional tests, 110 directions were null and two were suggestive; none survived global correction. Seven retinal vascular GWAS releases were retained in correlation analyses but not analysed by MR because release-specific allele-frequency semantics could not be resolved authoritatively. Thus, genome-wide, primary local and OCT-only directional analyses yielded no multiplicity-controlled evidence supporting broad shared architecture or robust directional relationships. These findings constrain causal interpretation of the retinal traits studied here without diminishing their potential observational or predictive value as systemic biomarkers.

**Keywords:** retinal imaging; genetic correlation; local genetic correlation; Mendelian randomization; optical coherence tomography; systemic disease

## 1. Introduction

Retinal imaging offers a scalable, non-invasive view of neural tissue and the microvasculature. Unlike many internal tissues, the retina can be measured directly, quantitatively and repeatedly in large populations. Quantitative features derived from optical coherence tomography and fundus photography can capture structural and vascular variation relevant to cardiovascular, metabolic, renal, neurological and inflammatory health. This accessibility has supported the growth of oculomics, which uses retinal phenotypes as systemic biomarkers for screening, risk estimation and physiological monitoring (1). Many retinal layer and vascular measures are heritable, creating an opportunity to examine their systemic relationships through inherited variation as well as observed phenotype. Their genetic determinants may connect retinal morphology to biological processes that operate across organs and across the life course. The resulting genetic evidence can clarify what a retinal association represents, but its interpretation must remain distinct from clinical prediction: prediction or association does not establish causal mediation.

The same retinal feature can occupy several biological positions. It may share inherited determinants with systemic disease, record downstream injury, reflect pleiotropic pathways that influence both tissues, or act as a directional intermediate through which inherited variation affects disease risk. Shared inheritance would support common biological architecture, whereas a downstream retinal change could be informative precisely because it records the cumulative systemic process. Pleiotropy can connect two traits without placing either on the other's causal pathway, and directionality can differ across phenotypes that appear clinically similar. These explanations can produce similar observational associations while implying different mechanisms and translational priorities. Large genome-wide association studies have mapped genetic determinants of retinal layer thickness, photoreceptor morphology and vascular features, and some cross-trait studies have reported retinal–systemic genetic correlations or Mendelian-randomization (MR) signals (2–5). Such findings establish biological connections worth testing, but they do not assign every retinal phenotype to a causal pathway. A retinal biomarker can be clinically informative without being a causal intermediate.

Existing human-genetic studies have largely addressed selected diseases, retinal features or directions, leaving uncertainty about whether positive findings generalize across retinal and systemic domains. The available evidence layers also answer different questions. Genome-wide genetic correlation assesses broad common-variant covariance, whereas local analysis asks whether sharing is concentrated within genomic regions. MR evaluates directionality under instrument assumptions, and instrument-level quality control determines whether a corrected directional signal remains biologically interpretable. Each layer has a distinct inferential target and a distinct source of uncertainty. A signal at one layer neither guarantees nor requires a signal at another. These layers are complementary rather than sequential prerequisites. A prespecified cross-domain evaluation is therefore needed to distinguish retinal phenotypes that show statistically detectable sharing from those supported as directional determinants after multiplicity control and variant-level scrutiny.

We examined 14 retinal imaging traits and eight systemic diseases spanning neuroretinal, outer-retinal and microvascular phenotypes and cardiovascular, metabolic, renal, neurodegenerative and immune or inflammatory disease. The panel was designed to test a general retinal–systemic proposition across anatomical and disease contexts, while retaining all phenotype-level results and complete correction families. We asked three questions: whether any pair showed multiplicity-controlled genome-wide sharing; whether regional sharing was stable across primary and sensitivity analyses; and whether either causal direction remained robust after instrument-level quality control. Retinal redundancy assessment and review of cohort overlap were incorporated before cross-systemic interpretation. Genome-wide covariance, likelihood-based primary local analysis, native LAVA sensitivity analysis and bidirectional MR were then applied as parallel sources of evidence. Directional analysis was prospectively restricted to sources with verifiable allele-frequency semantics. The design allowed broad sharing, regional sharing and directionality to contribute independently to interpretation. Our aim was to define the evidential boundary between retinal biomarkers and genetically supported intermediates in systemic disease.

## 2. Results

### 2.1 Prespecified retinal–systemic panel

The primary panel contained 14 retinal traits across neuroretinal, outer-retinal and microvascular domains and eight systemic diseases across cardiovascular, metabolic, renal, neurodegenerative and immune or inflammatory domains (Fig. 1). Pairwise LD Score regression among 16 retinal candidates generated 120 comparisons and identified two redundancy components at |rg|≥0.90. Mean outer nuclear layer thickness clustered with left-eye inner nuclear layer-to-external limiting membrane thickness (rg=0.9818), while retinal bifurcation count clustered with venular density (rg=0.9456). One sentinel from each component was retained, yielding 14 primary and two secondary retinal traits; the secondary traits were excluded from the primary retinal–systemic matrix. Dataset characteristics and provenance are summarized in Table 1 and Supplementary Table S1. Primary systemic releases had no documented UK Biobank contribution, although residual overlap through incompletely reported cohorts could not be excluded.

![Figure 1. Complementary retinal and systemic genetic evidence framework](../../figures/hmg_final_polish/Figure1_FINAL_POLISHED.png)

### 2.2 Genome-wide genetic sharing was not detected after multiplicity correction

All 112 prespecified retinal–systemic pairs were estimable by LD Score regression. None survived Benjamini–Hochberg correction across the genome-wide testing family. Fifteen pairs had nominal P<0.05, but none was treated as a discovery. Nominal results were distributed across retinal and disease domains and did not define a coherent cross-domain pattern after multiplicity correction (Fig. 2; Supplementary Table S3; Supplementary Fig. S1). Because genome-wide correlation can obscure regionally heterogeneous sharing, we next examined local architecture.

![Figure 2. Integrated human genetic evidence](../../figures/hmg_final_polish/Figure2_FINAL_POLISHED.png)

### 2.3 Local genetic evidence was not robust across primary and sensitivity analyses

Forty-seven prespecified retinal–systemic pairs entered the primary HDL-L analysis. Across 116,472 completed block tests, no result survived global-local false-discovery-rate correction (Supplementary Tables S4 and S5).

Sensitivity analysis used LAVA within a separate local testing framework. On the same 26,639-row LAVA universe, the normal-approximation P values used in the initial workflow yielded 1,877 tests passing FDR correction, whereas native LAVA bivariate inference yielded nine (Fig. 3A; Supplementary Table S6). Eight of the nine native rows had confidence intervals touching the |rho|=1 boundary. More broadly, 16,938 of 26,639 native confidence intervals touched or exceeded |rho|=1, 347 raw estimates had |rho|>1 and 68 had |rho|>1.25 (Fig. 3B; Supplementary Table S7). HDL-L and LAVA have different block definitions, eligibility criteria and testing universes, so their discovery proportions were not compared directly (Fig. 3C). Thus, the primary method yielded no corrected local sharing, while the sensitivity framework produced procedure- and boundary-sensitive signals that were not promoted to stable loci. Shared architecture does not establish directionality, so we next evaluated both directions within the prospectively defined OCT subset with verifiable source allele-frequency semantics.

![Figure 3. Local genetic correlation sensitivity and boundary diagnostics](../../figures/hmg_final_polish/Figure3_FINAL_POLISHED.png)

### 2.4 OCT-based directional analysis yielded no multiplicity-controlled association

Directional analysis was restricted prospectively to seven OCT traits with verifiable source allele-frequency coding. For seven vascular GWAS releases, the frequency-field definition could not be reconciled with external allele-frequency concordance using authoritative release metadata. These traits remained in genome-wide and local-correlation analyses but were not evaluated by MR.

The directional-analysis universe comprised seven primary OCT traits and the same eight systemic diseases, giving 112 bidirectional tests across 56 pairs. All 112 directions retained at least seven instruments after harmonisation. None survived Benjamini-Hochberg correction across the complete 112-test family. Of the 112 directions, 110 were null and two were nominally suggestive; neither survived correction across the complete 112-direction family (Supplementary Table S8; Supplementary Fig. S2). The suggestive directions were ischemic stroke→total macular thickness (7 instruments; beta=0.0984, SE=0.0408, q=0.963; nominal P=0.0158) and INL thickness→CKD (59 instruments; beta=-0.0725, SE=0.0322, q=0.963; nominal P=0.0243).

Steiger orientation diagnostics did not alter the primary multiplicity-controlled inference. MR-PRESSO completed for all 112 directions without flagging an outlier. Instrument-level and orientation results are provided in Supplementary Tables S8 and S9.

### 2.5 Integrated interpretation

Genome-wide analysis showed no multiplicity-controlled shared architecture, and primary local analysis identified no corrected shared loci. LAVA sensitivity findings remained procedure- and boundary-sensitive. OCT-only directional MR produced no multiplicity-controlled signal. Directional evidence for the seven vascular traits was not classified as null because those datasets were not analysed by MR. The retinal traits therefore remain compatible with observational, predictive, downstream or pleiotropic roles, but this study does not establish them as genetically supported intermediates in systemic disease (Table 2).

## 3. Discussion

### 3.1 Principal interpretation

Across complementary human-genetic evidence layers, we found little cross-method support for a broad causal interpretation of retinal phenotypes in systemic disease. None of the 112 genome-wide pairs or 116,472 primary HDL-L block tests survived their respective correction procedures. Native LAVA sensitivity findings were sparse and predominantly boundary-sensitive. Within the prospectively restricted OCT-only MR family, no direction survived correction across 112 tests. The results narrow the mechanistic claim: within the available common-variant resources, structurally defined OCT traits were not established as directional intermediates in the eight systemic diseases studied.

This conclusion does not diminish the observational or predictive value of retinal imaging. Retinal structure and vascular morphology can remain sensitive readouts of vascular, metabolic, neural and inflammatory states even when inherited variation does not support the retina as a mediator of systemic disease risk. Such readouts may reflect downstream injury, accumulated exposure, treatment effects or pleiotropic biology. The distinction is between what the retina records and what it causally transmits. A retinal measurement can track accumulated disease burden even if inherited differences in that measurement do not transmit systemic risk. Predictive use and causal mediation therefore require different validation strategies.

The directional boundary differs by retinal domain. Neuroretinal and outer-retinal OCT traits entered MR, whereas microvascular directional relationships could not be evaluated because release-specific allele-frequency coding remained unresolved. Microvascular MR cells therefore represent unavailable inference, not null evidence.

### 3.2 Relation to prior retinal–systemic genetics

Previous studies have reported positive retinal–systemic genetic associations, but they have generally asked narrower, phenotype-specific questions. Ortín Vela *et al.* identified genetic and MR relationships between retinal vascular traits and systemic phenotypes, including findings consistent with systemic exposures influencing retinal morphology (4). Cui *et al.* combined genetic correlation, MR and cross-sectional analysis for selected retinal characteristics and cardiovascular outcomes (5). Lu *et al.* examined deep-learning-derived retinal image traits in relation to major vascular diseases, including stroke, myocardial infarction and CKD (10), while Man *et al.* reported bidirectional MR associations between diabetic kidney disease phenotypes and retinal structural or vascular measures (11). These studies establish plausible relationships in defined settings and include directions consistent with the retina as a systemic readout.

The present study tested a broader prespecified panel under complete multiplicity control and retained every eligible OCT direction in the reported testing family. Differences in retinal phenotype definition, disease subset, ancestry and sample structure, instrument selection, outcome definition and correction universe can therefore lead to different conclusions without implying direct contradiction. Our findings do not negate phenotype-specific retinal–systemic relationships reported elsewhere; they limit their generalization into a broad model of retinal mediation. Differences from prior studies motivate attention to phenotype definition and evidence robustness rather than simple significance concordance. OCT layers and fundus-derived vascular measurements represent different anatomical substrates and measurement processes. A result for one retinal phenotype should not automatically be transferred to another, even when both are described as retinal biomarkers. Likewise, an association limited to one disease or instrument set does not imply a stable cross-domain pattern.

### 3.3 Why apparent signals did not support stronger biological claims

Across local and directional analyses, statistical evidence depended on the validity of its inferential layer. In local analysis, correlation estimates can become unstable when local heritability is low, linkage disequilibrium is imperfectly represented or a parameter approaches its boundary. Within the same 26,639-row universe, normal-approximation P values yielded 1,877 tests passing FDR correction, whereas native LAVA inference yielded nine; eight of the nine touched the correlation boundary. The primary HDL-L framework independently yielded no corrected result. Prior methodological work has shown that local-correlation procedures can differ in calibration, efficiency and shared-locus identification because their assumptions and reference structures differ (8,12). Procedure- or boundary-sensitive signals therefore require matched linkage-disequilibrium support and independent stability before locus-level interpretation. The contrast between the two LAVA P-value procedures is especially informative because the eligible row universe was held fixed. It identifies inferential instability within the same regional comparisons, not a change in which pairs or loci entered the sensitivity analysis.

Because reference-panel concordance could not resolve the submitted allele-frequency semantics with sufficient certainty, no vascular MR estimates were carried forward. This restriction was defined before OCT-only MR results were examined.

Within the OCT-only family, two directions were nominally suggestive, but neither survived correction across 112 tests. Sensitivity diagnostics did not change that inference.

### 3.4 Strengths, limitations and next evidence

A prespecified full matrix limited selective emphasis on positive pairs, while complete reporting and correction retained null and unresolved findings. Retinal redundancy control reduced duplication among correlated traits. Complementary genome-wide, local and directional evidence addressed distinct parts of the same biological question. Source-data integrity was assessed before submission, and the OCT-only MR restriction preceded inspection of its results.

Five limitations define the scope of the conclusions. First, the retinal GWASs were concentrated in participants of European ancestry and UK Biobank imaging resources, limiting population portability. Second, public metadata documented no UK Biobank contribution to the selected systemic releases but could not exclude residual overlap through incompletely reported cohorts. Third, correction across complete testing families increased specificity at a cost to power for modest or sparse effects. Fourth, a UK Biobank-matched local linkage-disequilibrium sensitivity analysis could not be performed with the available legal local resources. Fifth, directional inference was restricted to structural OCT traits because release-specific allele-frequency coding for seven vascular datasets could not be resolved to a standard sufficient for MR harmonisation. Common-variant summary statistics also leave rare-variant, acquired, developmental, epigenetic and cell-specific mechanisms unresolved.

The next decisive evidence is phenotype-matched independent replication, more diverse retinal GWASs, reference-matched local analyses and authoritative release metadata for vascular summary statistics. Retinal imaging may remain valuable for screening, prediction and physiological monitoring even when genetic directionality is unsupported. Current human-genetic evidence therefore constrains mechanistic interpretation while preserving the biomarker rationale for retinal imaging.


## 4. Materials and Methods

### 4.1 Study design and trait selection

This summary-statistics study examined genome-wide sharing, regional sharing and directional involvement between retinal traits and systemic disease under a prespecified analysis plan. The retinal candidate set comprised optical coherence tomography layer measures and fundus-derived vascular measures from published European-ancestry resources. Pairwise LD Score regression among 16 candidates produced 120 retinal–retinal correlations. Strong redundancy was defined a priori as |rg|≥0.90; one sentinel per connected component was retained according to phenotype coverage and prespecified prioritization, yielding 14 primary and two secondary traits. The systemic panel comprised coronary artery disease, ischemic stroke, type 2 diabetes, CKD, Alzheimer disease, Parkinson disease, systemic lupus erythematosus and inflammatory bowel disease. The selected GWAS resources covered cardiovascular and metabolic (14–16), renal and neurodegenerative (17–19), and immune or inflammatory (20,21) outcomes. Resource characteristics are summarized in Table 1 and Supplementary Table S1. No additional phenotype or dataset was substituted during manuscript preparation. Reporting followed STROBE-MR principles where applicable (13).

### 4.2 GWAS resources, quality control and data-integrity restriction

Summary statistics were harmonized to GRCh37 and assessed for variant identifiers, alleles, effect estimates, standard errors, P values, sample-size fields and duplicate variants. Variants incompatible with the reference or unresolved after harmonisation were excluded under prespecified rules. Retinal GWASs used UK Biobank imaging participants. For each systemic resource, publications, consortium descriptions and metadata were reviewed for documented UK Biobank participation. The selected primary disease releases had no documented UK Biobank contribution, although residual overlap through incompletely reported cohorts could not be excluded.

A pre-submission harmonisation audit identified unresolved allele-frequency semantics in seven retinal vascular GWAS releases. Because no authoritative release-specific mapping was available, these traits were retained in retinal redundancy, genome-wide and local-correlation analyses but excluded prospectively from MR. The directional analysis therefore comprised seven OCT traits with verifiable source frequency coding. Systemic releases without source frequency fields were not assigned constructed EAF values; reference-panel fallback was used only when explicit allele identity permitted mapping, and unresolved palindromic variants were excluded.

### 4.3 Genome-wide genetic correlation

Genome-wide genetic correlations were estimated for all 14×8=112 retinal–systemic pairs with LD Score regression and European linkage-disequilibrium scores (6). The method estimates common-variant covariance while accounting for linkage disequilibrium and sampling error. P values were adjusted across the 112-pair testing family with the Benjamini–Hochberg procedure (22). Nominal P values were retained for descriptive reporting but were not treated as discoveries when the adjusted threshold was not met.

### 4.4 Primary and sensitivity local genetic correlation

Forty-seven retinal–systemic pairs entered the prespecified local-analysis subset if they satisfied at least one of three criteria: global BH q<0.05; nominal P<0.05 together with |rg|≥0.10; or inclusion in a prospectively defined biology-priority list. The biology-priority list and admission framework were prespecified before local-correlation results were computed or inspected. HDL-L (8) completed 116,472 block tests, and global-local false-discovery-rate control was applied across the full tested family. The primary result was interpreted within its own block definition and estimability conditions.

LAVA (7) was used as a sensitivity framework. Bilateral nominal local-heritability gating yielded 26,639 bivariate rows. The normal-approximation P values used in the initial workflow and native LAVA bivariate inference were compared on this identical row universe, with false-discovery-rate adjustment recomputed separately for each procedure. Boundary diagnostics counted confidence intervals touching or exceeding |rho|=1 and raw estimates exceeding |rho|>1 and |rho|>1.25. HDL-L and LAVA were not treated as denominator-matched methods because their block definitions, eligibility criteria and testing universes differ. A UK Biobank-matched local linkage-disequilibrium reference was not available within the legal local resources and was therefore not tested.

### 4.5 OCT-based bidirectional Mendelian randomization

Directional analysis included the seven primary OCT traits with verified source frequency semantics and the same eight systemic diseases, producing 7×8×2=112 directions. The seven vascular traits were not analysed by MR because release-specific allele-frequency semantics could not be resolved authoritatively. Exposure variants reaching genome-wide significance (P<5×10⁻⁸) were LD-clumped at r²<0.001 within 10 Mb using the 1000 Genomes Phase 3 EUR reference panel (GRCh37). Variants were matched to outcomes and aligned to the exposure effect allele without automatic proxies. Ambiguous palindromic A/T and C/G variants were excluded when either effect-allele frequency was missing or lay within 0.42–0.58; resolvable palindromes required allele-frequency concordance within 0.20. Variants with absolute aligned effect-allele-frequency differences >0.20 were excluded. Frequency values were paired explicitly with their source allele identity before standardisation to the effect allele.

Random-effects inverse-variance weighting was used when at least two instruments remained, and the Wald ratio was used for single-instrument analyses. Cochran Q was evaluated with at least two instruments; weighted median, weighted mode, MR-Egger, Egger intercept and leave-one-out analyses required at least three, and MR-PRESSO required at least four (23–25). Steiger orientation was calculated where allele frequencies and phenotype-scale inputs permitted (9). Primary P values were adjusted by Benjamini–Hochberg correction across the complete 112-direction family. Nominal P<0.05 with q≥0.05 was classified as suggestive, while q<0.05 was required for multiplicity-controlled directional evidence. 

### 4.6 Reproducibility and data availability

Analysis scripts, prespecified configurations, frequency-semantic registries, harmonisation records, complete testing-family outputs and shareable derived data were archived. Tables and figures were generated from the prespecified final result set, and no post hoc phenotype, outcome, instrument, threshold or estimator substitution was made. The public repository is https://github.com/seefreewind/genetic-oculomics-evidence-boundary. The versioned release is archived at doi:10.5281/zenodo.22915396; the concept DOI for all versions is doi:10.5281/zenodo.22875271. Source GWAS summary statistics remain governed by their originating repositories and licences.

## Funding

The authors received no specific funding for this work.

## Acknowledgements

The authors thank the investigators and participants of the contributing genome-wide association studies and consortia. OpenAI Codex (model: GPT-5.6) and DeepSeek (model: V4 Flash) were used under author direction to assist with code writing, debugging, workflow orchestration, manuscript formatting and language editing. The analysis plan and thresholds were author-defined. The authors reviewed and verified all AI-assisted outputs and take responsibility for the final manuscript.

## Authors' contributions

Da Lin: conceptualization, data curation, formal analysis, methodology, software, visualization, and writing—original draft. Ying Chen: data curation, investigation, validation, visualization, and writing—review and editing. Yue Liu: data curation, investigation, validation, and writing—review and editing. Yu Zhang: conceptualization, supervision, project administration, resources, and writing—review and editing. All authors approved the final manuscript.

## Data availability

Derived result tables, analysis configurations, audit scripts, figure-generation scripts and checksums are available at https://github.com/seefreewind/genetic-oculomics-evidence-boundary and in the versioned Zenodo release at doi:10.5281/zenodo.22915396. The concept DOI for all versions is doi:10.5281/zenodo.22875271. Source GWAS summary statistics remain available under the terms of their originating studies and repositories.

## Ethics approval and consent to participate

This study used publicly available summary statistics and involved no new recruitment or access to individual-level data. Ethical approvals and participant consent were obtained by the original studies.

## Consent for publication

Not applicable.

## Conflict of interest statement

The authors declare no competing interests.

## References

1. Zhu, Z. et al. Oculomics: current concepts and evidence. Prog Retin Eye Res 106, 101350 (2025). doi:10.1016/j.preteyeres.2025.101350.
2. Zhao, Y. et al. Eye-brain connections revealed by multimodal retinal and brain imaging genetics. Nat Commun 15, 6064 (2024). doi:10.1038/s41467-024-50309-w.
3. Currant, H. et al. Genetic variation affects morphological retinal phenotypes extracted from UK Biobank optical coherence tomography images. PLoS Genet 19, e1010587 (2023). doi:10.1371/journal.pgen.1010587.
4. Ortín Vela, M. et al. Phenotypic and genetic characteristics of retinal vascular parameters and their association with diseases. Nat Commun 15, 9593 (2024). doi:10.1038/s41467-024-52334-1.
5. Cui, X. et al. Causal effects between retinal characteristics and cardiovascular diseases: insights from genetic correlation, Mendelian randomization, and cross-sectional study. Glob Heart 20, 104 (2025). doi:10.5334/gh.1493.
6. Bulik-Sullivan, B. et al. LD Score regression distinguishes confounding from polygenicity in genome-wide association studies. Nat Genet 47, 291–295 (2015). doi:10.1038/ng.3211.
7. Werme, J. et al. An integrated framework for local genetic correlation analysis. Nat Genet 54, 274–282 (2022). doi:10.1038/s41588-022-01017-y.
8. Li, Y., Pawitan, Y. and Shen, X. An enhanced framework for local genetic correlation analysis. Nat Genet 57, 1053–1058 (2025). doi:10.1038/s41588-025-02123-3.
9. Hemani, G., Tilling, K. and Davey Smith, G. Orienting the causal relationship between imprecisely measured traits using GWAS summary data. PLoS Genet 13, e1007081 (2017). doi:10.1371/journal.pgen.1007081.
10. Lu, M. et al. Phenotypic screening and genetic insights for predicting major vascular-related diseases using retinal imaging. NPJ Digit Med 8, 437 (2025). doi:10.1038/s41746-025-01850-5.
11. Man, S. et al. Retinal structural and vascular alterations in diabetic kidney disease: a bidirectional Mendelian randomization study. Microvasc Res 166, 104928 (2026). doi:10.1016/j.mvr.2026.104928.
12. Darlay, R. et al. Exploring similarities and differences between methods that exploit patterns of local genetic correlation to identify shared causal loci through application to genome-wide association studies of multiple long term conditions. Genet Epidemiol 49, e70012 (2025). doi:10.1002/gepi.70012.
13. Skrivankova, V.W. et al. Strengthening the reporting of observational studies in epidemiology using Mendelian randomization (STROBE-MR): explanation and elaboration. BMJ 375, n2233 (2021). doi:10.1136/bmj.n2233.
14. Nikpay, M. et al. A comprehensive 1,000 Genomes-based genome-wide association meta-analysis of coronary artery disease. Nat Genet 47, 1121–1130 (2015). doi:10.1038/ng.3396.
15. Malik, R. et al. Multiancestry genome-wide association study of 520,000 subjects identifies 32 loci associated with stroke and stroke subtypes. Nat Genet 50, 524–537 (2018). doi:10.1038/s41588-018-0058-3.
16. Scott, R.A. et al. An expanded genome-wide association study of type 2 diabetes in Europeans. Diabetes 66, 2888–2902 (2017). doi:10.2337/db16-1253.
17. Wuttke, M. et al. A catalog of genetic loci associated with kidney function from analyses of a million individuals. Nat Genet 51, 957–972 (2019). doi:10.1038/s41588-019-0407-x.
18. Kunkle, B.W. et al. Genetic meta-analysis of diagnosed Alzheimer's disease identifies new risk loci and implicates Aβ, tau, immunity and lipid processing. Nat Genet 51, 414–430 (2019). doi:10.1038/s41588-019-0358-2.
19. Nalls, M.A. et al. Identification of novel risk loci, causal insights, and heritable risk for Parkinson's disease: a meta-analysis of genome-wide association studies. Lancet Neurol 18, 1091–1102 (2019). doi:10.1016/S1474-4422(19)30320-5.
20. Bentham, J. et al. Genetic association analyses implicate aberrant regulation of innate and adaptive immunity genes in the pathogenesis of systemic lupus erythematosus. Nat Genet 47, 1457–1464 (2015). doi:10.1038/ng.3434.
21. de Lange, K.M. et al. Genome-wide association study implicates immune activation of multiple integrin genes in inflammatory bowel disease. Nat Genet 49, 256–261 (2017). doi:10.1038/ng.3760.
22. Benjamini, Y. and Hochberg, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc B 57, 289–300 (1995). doi:10.1111/j.2517-6161.1995.tb02031.x.
23. Verbanck, M., Chen, C.-Y., Neale, B. and Do, R. Detection of widespread horizontal pleiotropy in causal relationships inferred from Mendelian randomization between complex traits and diseases. Nat Genet 50, 693–698 (2018). doi:10.1038/s41588-018-0099-7.
24. Bowden, J., Davey Smith, G. and Burgess, S. Mendelian randomization with invalid instruments: effect estimation and bias detection through Egger regression. Int J Epidemiol 44, 512–525 (2015). doi:10.1093/ije/dyv080.
25. Bowden, J., Davey Smith, G., Haycock, P.C. and Burgess, S. Consistent estimation in Mendelian randomization with some invalid instruments using a weighted median estimator. Genet Epidemiol 40, 304–314 (2016). doi:10.1002/gepi.21965.

## Figure legends

**Figure 1. Complementary evidence framework for retinal and systemic traits.** Retinal phenotypes span neuroretinal, outer-retinal and microvascular domains, while systemic contexts span cardiovascular, metabolic, renal, neurodegenerative and immune or inflammatory disease. Genome-wide sharing was evaluated across all 14 retinal traits and eight diseases (112 pairs), and local analysis retained the prespecified 47-pair subset. Directional MR was restricted prospectively to seven OCT traits with verifiable source allele-frequency coding (112 directions). The seven vascular traits remained in correlation analyses but were not evaluated by MR. *Alt text:* Three parallel evidence layers distinguish the full retinal panel used for global and local analyses from the seven-trait OCT subset used for directional MR.

**Figure 2. Integrated human-genetic evidence.** Genome-wide sharing included 112 pairs with no test passing FDR correction. Primary HDL-L included 116,472 block tests with no global-local test passing FDR correction. Native LAVA sensitivity analysis included 26,639 rows, with nine tests passing FDR correction of which eight were boundary-sensitive. OCT-only directional MR included 112 directions, with 110 null and two suggestive classifications and no FDR-positive direction. Seven vascular traits were not analysed by MR because release-specific allele-frequency semantics remained unresolved. Track positions are categorical and do not represent comparable discovery proportions across different testing universes. *Alt text:* Four non-proportional evidence tracks show the testing universe, corrected result and bounded interpretation for genome-wide, primary local, LAVA sensitivity and OCT-only MR analyses.

**Figure 3. Local retinal–systemic evidence was sensitive to inference procedure and testing framework.** (A) Within the same 26,639-row universe, normal-approximation P values yielded 1,877 tests passing FDR correction, whereas native LAVA inference yielded nine. (B) Native LAVA boundary diagnostics show 16,938 confidence intervals touching or exceeding |rho|=1, 347 raw estimates with |rho|>1 and 68 with |rho|>1.25; 63.6% of native rows had a confidence interval touching or exceeding the boundary. (C) The primary HDL-L analysis completed 116,472 block tests and yielded no global-local test passing FDR correction. HDL-L and LAVA use different local testing universes and are not interpreted as denominator-matched discovery-rate comparisons. Vascular traits remained eligible for the originally admitted local pairs. *Alt text:* A dot comparison preserves visibility of nine native LAVA rows, a bar chart reports boundary behavior, and a separate information panel reports the primary HDL-L result.

## Supplementary figure legends

**Supplementary Figure S1. Genome-wide genetic-correlation matrix.** The heatmap displays the 112 retinal–systemic LD Score regression estimates. Outlines identify nominal P<0.05 cells; none survived FDR correction across the complete 112-pair family. Color encodes the estimated genetic correlation and does not indicate corrected significance.

**Supplementary Figure S2. Final directional-evidence matrix.** OCT cells summarize classifications from the complete 112-direction OCT-only family. Vascular cells are labelled not analysed because source allele-frequency semantics remained unresolved; they must not be interpreted as null. No OCT direction passed FDR correction across the complete 112-direction family.

## Tables

**Table 1. Dataset-level inventory of retinal and systemic GWAS resources.** Trait-specific analysis N was not available in the prespecified registry for the Zhao et al. OCT traits; the release-level mean of 60,748 is shown. Sample size varied by vascular phenotype. UK Biobank status describes participation in the source GWAS, not pairwise overlap.

**Table 2. Retinal-domain interpretation boundary.** Neuroretinal and outer-retinal OCT traits were analysed in the OCT-only MR family. Microvascular traits remained in global and originally admitted local analyses but were not evaluated by MR because release-specific allele-frequency semantics could not be resolved authoritatively. Global evidence uses domain-specific retinal–disease denominators; local evidence covers only admitted pairs within the prespecified 47-pair subset; and directional evidence covers the OCT-only family by domain.

## Abbreviations

CKD, chronic kidney disease; CRAE, central retinal arteriolar equivalent; EAF, effect-allele frequency; FDR, false discovery rate; GWAS, genome-wide association study; HDL-L, high-definition likelihood local analysis; LD, linkage disequilibrium; LDSC, LD Score regression; LAVA, local analysis of co-variant association; MR, Mendelian randomization; OCT, optical coherence tomography; UKB, UK Biobank.
