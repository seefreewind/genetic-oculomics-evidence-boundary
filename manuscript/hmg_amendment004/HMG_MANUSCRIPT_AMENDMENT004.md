# Human genetic evidence constrains causal interpretation of retinal traits in systemic disease

## Title page

**Authors:** Da Lin¹, Ying Chen², Yue Liu², Yu Zhang¹

**Affiliations:** ¹ Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China; ² Wenzhou Medical University, Wenzhou, Zhejiang Province, China

**Corresponding author:** Yu Zhang; email: zhangyu1@wzhealth.com; ORCID: https://orcid.org/0000-0001-8579-3692

**Article type:** Original Article

## Abstract

Retinal imaging traits are increasingly used as systemic biomarkers, yet their position in disease biology remains uncertain. We evaluated 14 retinal traits and eight systemic diseases across complementary human-genetic analyses. None of 112 genome-wide genetic correlations survived false-discovery-rate correction. Primary local analysis of 47 prespecified pairs yielded no corrected signal across 116,472 block tests. In the same 26,639-row sensitivity universe, a historical local-correlation procedure identified 1,877 false-discovery-rate-significant tests, whereas native LAVA inference identified nine; eight of the nine had confidence intervals touching the |rho|=1 boundary. Directional analyses were prospectively restricted to seven optical coherence tomography traits for which source allele-frequency semantics could be verified. Across 112 bidirectional tests, 110 directions were null and two were suggestive; none survived global correction. Seven retinal vascular GWAS releases were retained in correlation analyses but excluded from Mendelian randomization because release-specific allele-frequency coding could not be resolved unambiguously. Thus, genome-wide, primary local and data-integrity-qualified directional analyses yielded no multiplicity-controlled evidence supporting broad shared architecture or robust directional relationships. These findings constrain causal interpretation of the retinal traits studied here without diminishing their potential observational or predictive value as systemic biomarkers.

**Keywords:** retinal imaging; genetic correlation; local genetic correlation; Mendelian randomization; optical coherence tomography; systemic disease

## 1. Introduction

Retinal imaging offers a scalable, non-invasive view of neural tissue and the microvasculature. Unlike many internal tissues, the retina can be measured directly, quantitatively and repeatedly in large populations. Quantitative features derived from optical coherence tomography and fundus photography can capture structural and vascular variation relevant to cardiovascular, metabolic, renal, neurological and inflammatory health. This accessibility has supported the growth of oculomics, which uses retinal phenotypes as systemic biomarkers for screening, risk estimation and physiological monitoring (1). Many retinal layer and vascular measures are heritable, creating an opportunity to examine their systemic relationships through inherited variation as well as observed phenotype. Their genetic determinants may connect retinal morphology to biological processes that operate across organs and across the life course. The resulting genetic evidence can clarify what a retinal association represents, but its interpretation must remain distinct from clinical prediction: prediction or association does not establish causal mediation.

The same retinal feature can occupy several biological positions. It may share inherited determinants with systemic disease, record downstream injury, reflect pleiotropic pathways that influence both tissues, or act as a directional intermediate through which inherited variation affects disease risk. Shared inheritance would support common biological architecture, whereas a downstream retinal change could be informative precisely because it records the cumulative systemic process. Pleiotropy can connect two traits without placing either on the other's causal pathway, and directionality can differ across phenotypes that appear clinically similar. These explanations can produce similar observational associations while implying different mechanisms and translational priorities. Large genome-wide association studies have mapped genetic determinants of retinal layer thickness, photoreceptor morphology and vascular features, and some cross-trait studies have reported retinal–systemic genetic correlations or Mendelian-randomization (MR) signals (2–5). Such findings establish biological connections worth testing, but they do not assign every retinal phenotype to a causal pathway. A retinal biomarker can be clinically informative without being a causal intermediate.

Existing human-genetic studies have largely addressed selected diseases, retinal features or directions, leaving uncertainty about whether positive findings generalize across retinal and systemic domains. The available evidence layers also answer different questions. Genome-wide genetic correlation assesses broad common-variant covariance, whereas local analysis asks whether sharing is concentrated within genomic regions. MR evaluates directionality under instrument assumptions, and instrument-level quality control determines whether a corrected directional signal remains biologically interpretable. Each layer has a distinct inferential target and a distinct source of uncertainty. A signal at one layer neither guarantees nor requires a signal at another. These layers are complementary rather than sequential prerequisites. A prespecified cross-domain evaluation is therefore needed to distinguish retinal phenotypes that show statistically detectable sharing from those supported as directional determinants after multiplicity control and variant-level scrutiny.

We examined 14 retinal imaging traits and eight systemic diseases spanning neuroretinal, outer-retinal and microvascular phenotypes and cardiovascular, metabolic, renal, neurodegenerative and immune or inflammatory disease. The panel was designed to test a general retinal–systemic proposition across anatomical and disease contexts, while retaining phenotype-level results and complete correction families. We asked three questions: whether any pair showed multiplicity-controlled genome-wide sharing; whether regional sharing was stable across primary and sensitivity analyses; and whether either causal direction remained robust after instrument-level quality control. Retinal redundancy assessment and review of cohort overlap were incorporated before cross-systemic interpretation. Genome-wide covariance, likelihood-based primary local analysis, native LAVA sensitivity analysis and bidirectional MR were then applied as parallel sources of evidence. Directional analysis was prospectively restricted to sources with verifiable allele-frequency semantics. The design allowed broad sharing, regional sharing and directionality to contribute independently to interpretation. Our aim was to define the evidential boundary between retinal biomarkers and genetically supported intermediates in systemic disease.

## 2. Results

### 2.1 Prespecified retinal–systemic panel

The primary panel contained 14 retinal traits across neuroretinal, outer-retinal and microvascular domains and eight systemic diseases across cardiovascular, metabolic, renal, neurodegenerative and immune or inflammatory domains (Fig. 1). Pairwise LD Score regression among 16 retinal candidates generated 120 comparisons and identified two redundancy components at |rg|≥0.90. Mean outer nuclear layer thickness clustered with left-eye inner nuclear layer-to-external limiting membrane thickness (rg=0.9818), while retinal bifurcation count clustered with venular density (rg=0.9456). One sentinel from each component was retained, yielding 14 primary and two secondary retinal traits; the secondary traits were excluded from the primary retinal–systemic matrix. Dataset characteristics and provenance are summarized in Table 1 and Supplementary Table S1. Primary systemic releases had no documented UK Biobank contribution, although residual overlap through incompletely reported cohorts could not be excluded.

### 2.2 Genome-wide genetic sharing was not detected after multiplicity correction

All 112 retinal–systemic LD Score regression pairs completed without an incomplete pair in the prespecified analysis matrix. None survived Benjamini–Hochberg correction across the genome-wide testing family. Fifteen pairs had nominal P<0.05, but none was treated as a discovery. Nominal results were distributed across retinal and disease domains and did not define a coherent cross-domain pattern after multiplicity correction (Fig. 2; Supplementary Table S3; Supplementary Fig. S1). Because genome-wide correlation can obscure regionally heterogeneous sharing, we next examined local architecture.

### 2.3 Local genetic evidence was not robust across primary and sensitivity analyses

Forty-seven prespecified retinal–systemic pairs entered the primary HDL-L analysis. Across 116,472 completed block tests, no result survived global-local false-discovery-rate correction (Supplementary Tables S4 and S5).

Sensitivity analysis used LAVA within a separate local testing framework. On the same 26,639-row LAVA universe, the historical normal-approximation procedure yielded 1,877 false-discovery-rate-significant tests, whereas native inference yielded nine (Fig. 3A; Supplementary Table S6). Eight of the nine native rows had confidence intervals touching the |rho|=1 boundary. More broadly, 16,938 of 26,639 native confidence intervals touched or exceeded |rho|=1, 347 raw estimates had |rho|>1 and 68 had |rho|>1.25 (Fig. 3B; Supplementary Table S7). HDL-L and LAVA have different block definitions, eligibility criteria and testing universes, so their discovery proportions were not compared directly (Fig. 3C). Thus, the primary method yielded no corrected local sharing, while the sensitivity framework produced procedure- and boundary-sensitive signals that were not promoted to stable loci. Shared architecture does not establish directionality, so we next tested both causal directions independently.

### 2.4 Directional analysis was restricted to data-integrity-qualified OCT traits

A pre-submission harmonisation audit identified an unresolved discrepancy between the GWAS-SSF frequency-field definition and external allele-frequency concordance for seven retinal vascular GWAS releases. No authoritative release-specific mapping was available. Their frequency coding was therefore not inferred from reference-panel concordance, and the vascular traits were excluded prospectively from MR while remaining in the genome-wide and local-correlation analyses.

The Amendment 004 MR universe comprised seven primary OCT traits and the same eight systemic diseases, giving 112 bidirectional tests across 56 pairs. All 112 directions retained at least seven instruments after harmonisation. None survived Benjamini-Hochberg correction across the complete 112-test family. Of the 112 directions, 110 were null and two were suggestive (Supplementary Table S8; Supplementary Fig. S2). The suggestive directions were ischemic stroke→total macular thickness (7 instruments; beta=0.0984, SE=0.0408, P=0.0158, q=0.963) and INL thickness→CKD (59 instruments; beta=-0.0725, SE=0.0322, P=0.0243, q=0.963). Neither was treated as a discovery.

Steiger directionality was estimable for 98 directions; 95 supported the specified direction at P<0.05. This orientation evidence did not override the primary false-discovery-rate result. MR-PRESSO completed for all 112 directions without flagging an outlier. The full harmonisation record and sensitivity diagnostics are provided in Supplementary Tables S8 and S9.

### 2.5 Integrated interpretation

Genome-wide analysis showed no multiplicity-controlled shared architecture, and primary local analysis identified no corrected shared loci. LAVA sensitivity findings remained procedure- and boundary-sensitive. Data-integrity-qualified OCT-only MR produced no globally corrected directional signal. Directional evidence for the seven vascular traits was not classified as null because those datasets were not analysed by MR. The retinal traits therefore remain compatible with observational, predictive, downstream or pleiotropic roles, but this study does not establish them as genetically supported intermediates in systemic disease (Table 2).

## 3. Discussion

### 3.1 Principal interpretation

Across complementary human-genetic evidence layers, we found little cross-method support for a broad causal interpretation of retinal phenotypes in systemic disease. None of the 112 genome-wide pairs or 116,472 primary HDL-L block tests survived their respective correction procedures. Native LAVA sensitivity findings were sparse and predominantly boundary-sensitive. Within the prospectively restricted OCT-only MR family, no direction survived correction across 112 tests. The results narrow the mechanistic claim: within the available common-variant resources, structurally defined OCT traits were not established as directional intermediates in the eight systemic diseases studied.

This conclusion does not diminish the observational or predictive value of retinal imaging. Retinal structure and vascular morphology can remain sensitive readouts of vascular, metabolic, neural and inflammatory states even when inherited variation does not support the retina as a mediator of systemic disease risk. Such readouts may reflect downstream injury, accumulated exposure, treatment effects or pleiotropic biology. The relevant distinction is between what the retina records and what it causally transmits. Human genetics informs the second proposition, while prediction and monitoring can remain useful when that proposition is unsupported.

The directional boundary differs by retinal domain. Neuroretinal and outer-retinal OCT traits entered the Amendment 004 MR analysis because their source frequency coding was verifiable. Microvascular traits remained in genome-wide and local analyses, but their directional relationships were not evaluated because seven release-specific allele-frequency mappings could not be resolved authoritatively. These cells represent unavailable directional inference, not null evidence.

### 3.2 Relation to prior retinal–systemic genetics

Previous studies have reported positive retinal–systemic genetic associations, but they have generally asked narrower, phenotype-specific questions. Ortín Vela *et al.* identified genetic and MR relationships between retinal vascular traits and systemic phenotypes, including findings consistent with systemic exposures influencing retinal morphology (4). Cui *et al.* combined genetic correlation, MR and cross-sectional analysis for selected retinal characteristics and cardiovascular outcomes (5). Lu *et al.* examined deep-learning-derived retinal image traits in relation to major vascular diseases, including stroke, myocardial infarction and CKD (10), while Man *et al.* reported bidirectional MR associations between diabetic kidney disease phenotypes and retinal structural or vascular measures (11). These studies establish plausible relationships in defined settings and include directions consistent with the retina as a systemic readout.

The present study tested a broader prespecified panel under complete multiplicity control and retained every eligible OCT direction in the reported testing family. Differences in retinal phenotype definition, disease subset, ancestry and sample structure, instrument selection, outcome definition and correction universe can therefore lead to different conclusions without implying direct contradiction. Our findings do not negate phenotype-specific retinal–systemic relationships reported elsewhere; they limit their generalization into a broad model of retinal mediation. Differences from prior studies motivate attention to phenotype definition and evidence robustness rather than simple significance concordance.

### 3.3 Why apparent signals did not support stronger biological claims

Across local and directional analyses, statistical evidence depended on the validity of its inferential layer. In local analysis, correlation estimates can become unstable when local heritability is low, linkage disequilibrium is imperfectly represented or a parameter approaches its boundary. Replacing the historical approximation with native LAVA inference reduced 1,877 false-discovery-rate-significant rows to nine in an identical row universe, and eight of the nine touched the correlation boundary. The primary HDL-L framework independently yielded no corrected result. Prior methodological work has shown that local-correlation procedures can differ in calibration, efficiency and shared-locus identification because their assumptions and reference structures differ (8,12). Procedure- or boundary-sensitive signals therefore require matched linkage-disequilibrium support and independent stability before locus-level interpretation.

At the directional layer, the decisive issue was source-data integrity. Seven vascular releases carried a field named `effect_allele_frequency`, but its documented meaning conflicted systematically with external allele-frequency concordance. Reference concordance alone could not establish which labelled allele the released value counted. Inferring the mapping through `1-f`, suppressing frequency checks or replacing the GWAS would have changed the analysis in a result-dependent manner. The vascular MR family was therefore closed without corrected estimates, and Amendment 004 was frozen before any OCT-only result was calculated.

Within the qualified OCT universe, two directions reached nominal significance, but neither survived correction across the complete 112-test family. Steiger orientation and sensitivity analyses were interpreted as supporting diagnostics rather than substitutes for the primary multiplicity-controlled result. This distinction avoids promoting nominal or orientation-supported associations to causal findings.

### 3.4 Strengths, limitations and next evidence

The study has several strengths. A prespecified full matrix limited selective emphasis on positive pairs, and complete multiplicity correction retained null and unresolved findings. Retinal redundancy control reduced duplication among correlated traits. Genome-wide, primary local, sensitivity local and directional analyses addressed distinct aspects of the same question. The pre-submission frequency-semantic audit exposed a source-level ambiguity before manuscript submission, and Amendment 004 restricted MR prospectively rather than inferring allele coding from the desired result.

Five limitations define the scope of the conclusions. First, the retinal GWASs were concentrated in participants of European ancestry and UK Biobank imaging resources, limiting population portability. Second, public metadata documented no UK Biobank contribution to the selected systemic releases but could not exclude residual overlap through incompletely reported cohorts. Third, correction across complete testing families increased specificity at a cost to power for modest or sparse effects. Fourth, a UK Biobank-matched local linkage-disequilibrium sensitivity analysis could not be performed with the available legal local resources. Fifth, directional inference was restricted to structural OCT traits because release-specific allele-frequency coding for seven vascular datasets could not be resolved to a standard sufficient for MR harmonisation. This reduced vascular directional coverage but avoided an allele mapping based on inference alone. Common-variant summary statistics also cannot resolve rare-variant, acquired, developmental, epigenetic or cell-specific mechanisms.

The next decisive evidence is phenotype-matched independent replication, more diverse retinal GWASs, reference-matched local analyses and authoritative release metadata for vascular summary statistics. The last resource would permit vascular MR without inferred frequency coding. Retinal imaging may remain valuable for screening, prediction and physiological monitoring even when genetic directionality is unsupported. Current human-genetic evidence therefore constrains mechanistic interpretation while preserving the biomarker rationale for retinal imaging.

This evidence hierarchy also clarifies how future positive findings should be evaluated. A reproducible global or local correlation would identify shared architecture but would not by itself order the traits. A corrected MR association would add directional evidence only if allele identity, frequency coding, instrument strength and pleiotropy diagnostics remained coherent at variant level. Concordance across these layers would strengthen a mechanistic interpretation; discordance would instead help separate shared inheritance, downstream retinal response and horizontal pleiotropy. Applying the same sequence in independent datasets would make apparent replication more informative than repeating a nominal association under a different phenotype definition.

## 4. Materials and Methods

### 4.1 Study design and trait selection

This summary-statistics study examined genome-wide sharing, regional sharing and directional involvement between retinal traits and systemic disease under a prespecified analysis plan. The retinal candidate set comprised optical coherence tomography layer measures and fundus-derived vascular measures from published European-ancestry resources. Pairwise LD Score regression among 16 candidates produced 120 retinal–retinal correlations. Strong redundancy was defined a priori as |rg|≥0.90; one sentinel per connected component was retained according to phenotype coverage and prespecified prioritization, yielding 14 primary and two secondary traits. The systemic panel comprised coronary artery disease, ischemic stroke, type 2 diabetes, CKD, Alzheimer disease, Parkinson disease, systemic lupus erythematosus and inflammatory bowel disease. Resource characteristics are summarized in Table 1 and Supplementary Table S1. No additional phenotype or dataset was substituted during manuscript preparation. Reporting followed STROBE-MR principles where applicable.

### 4.2 GWAS resources, quality control and data-integrity restriction

Summary statistics were harmonized to GRCh37 and assessed for variant identifiers, alleles, effect estimates, standard errors, P values, sample-size fields and duplicate variants. Variants incompatible with the reference or unresolved after harmonisation were excluded under prespecified rules. Retinal GWASs used UK Biobank imaging participants. For each systemic resource, publications, consortium descriptions and metadata were reviewed for documented UK Biobank participation. The selected primary disease releases had no documented UK Biobank contribution, although residual overlap through incompletely reported cohorts could not be excluded.

During pre-submission harmonisation audit, seven retinal vascular GWAS releases showed an unresolved discrepancy between the GWAS-SSF field definition and external allele-frequency concordance. No authoritative release-specific mapping or original export code was available. These traits were retained in retinal redundancy, genome-wide and local-correlation analyses but excluded from MR. This restriction was formalized in Amendment 004 before any OCT-only MR result was calculated. For the seven OCT sources, official fastGWA documentation and source headers established that `A1` was the effect allele and `AF1` its frequency. Systemic releases without source frequency fields were not assigned constructed EAF values; reference-panel fallback was used only when explicit allele identity permitted mapping, and unresolved palindromic variants were excluded.

### 4.3 Genome-wide genetic correlation

Genome-wide genetic correlations were estimated for all 14×8=112 retinal–systemic pairs with LD Score regression and European linkage-disequilibrium scores. The method estimates common-variant covariance while accounting for linkage disequilibrium and sampling error. P values were adjusted across the 112-pair testing family with the Benjamini–Hochberg procedure. Nominal P values were retained for descriptive reporting but were not treated as discoveries when the adjusted threshold was not met.

### 4.4 Primary and sensitivity local genetic correlation

Forty-seven pairs entered prespecified primary local analysis on the basis of nominal genome-wide evidence, effect-size criteria or biological priority. HDL-L completed 116,472 block tests, and global-local false-discovery-rate control was applied across the full tested family. The primary result was interpreted within its own block definition and estimability conditions.

LAVA was used as a sensitivity framework. Bilateral nominal local-heritability gating yielded 26,639 bivariate rows. The historical normal-approximation P values used in the earlier workflow and native LAVA bivariate inference were compared on this identical row universe, with false-discovery-rate adjustment recomputed separately for each procedure. Boundary diagnostics counted confidence intervals touching or exceeding |rho|=1 and raw estimates exceeding |rho|>1 and |rho|>1.25. HDL-L and LAVA were not treated as denominator-matched methods because their block definitions, eligibility criteria and testing universes differ. A UK Biobank-matched local linkage-disequilibrium reference was not available within the legal local resources and was therefore not tested.

### 4.5 Data-integrity-qualified bidirectional MR

Directional analysis included the seven primary OCT traits with verified source frequency semantics and the same eight systemic diseases, producing 7×8×2=112 directions. The seven vascular traits were not analysed by MR. Genome-wide-significant exposure variants were clumped at the original Phase 2A threshold against the same European reference, matched to outcomes, aligned to the exposure effect allele and screened under the frozen palindromic and absolute ΔEAF >0.20 rules. Frequency was represented as a value paired with its allele identity and standardized to the effect allele only after mapping.

Inverse-variance weighting with random effects was prespecified when at least two instruments remained, and the Wald ratio was reserved for one instrument. Weighted-median, weighted-mode, MR-Egger, Cochran Q, Egger-intercept, leave-one-out and MR-PRESSO analyses were run only at the original instrument-count requirements. Steiger exposure and outcome variance explained, direction and P values were recomputed from the Amendment 004 instrument set. Primary P values were adjusted by Benjamini-Hochberg correction across the complete 112-direction family. Results were classified as null, suggestive, unresolved or directional-MR-supported under the original thresholds. The 112-test q values are specific to Amendment 004 and were not compared numerically with the superseded 224-test family as evidence of increased significance.

### 4.6 Reproducibility and data availability

Analysis scripts, frozen configurations, frequency-semantic registries, harmonisation records, complete testing-family outputs and shareable derived data were archived. Tables and figures were generated from the Amendment 004 result freeze, and no post hoc phenotype, outcome, instrument, threshold or estimator substitution was made. The public repository is https://github.com/seefreewind/genetic-oculomics-evidence-boundary. The historical Zenodo record is doi:10.5281/zenodo.22875272; the Amendment 004 package requires a new versioned release before submission. Source GWAS summary statistics remain governed by their originating repositories and licences.

## Funding

The authors received no specific funding for this work.

## Acknowledgements

The authors thank the investigators and participants of the contributing genome-wide association studies and consortia. OpenAI Codex (model: GPT-5.6) and DeepSeek (model: V4 Flash) were used under author direction to assist with code writing, debugging, workflow orchestration, manuscript formatting and language editing. The analysis plan and thresholds were author-defined. The authors reviewed and verified all AI-assisted outputs and take responsibility for the final manuscript.

## Authors' contributions

Da Lin: conceptualization, data curation, formal analysis, methodology, software, visualization, and writing—original draft. Ying Chen: data curation, investigation, validation, visualization, and writing—review and editing. Yue Liu: data curation, investigation, validation, and writing—review and editing. Yu Zhang: conceptualization, supervision, project administration, resources, and writing—review and editing. All authors approved the final manuscript.

## Data availability

Derived result tables, analysis configurations, audit scripts, figure-generation scripts and checksums are available at https://github.com/seefreewind/genetic-oculomics-evidence-boundary. The historical Zenodo record is doi:10.5281/zenodo.22875272; a manuscript-compatible Amendment 004 version will be deposited before submission. Source GWAS summary statistics remain available under the terms of their originating studies and repositories.

## Ethics approval and consent to participate

This study used publicly available summary statistics and involved no new recruitment or access to individual-level data. Ethical approvals and participant consent were obtained by the original studies.

## Consent for publication

Not applicable.

## Conflict of interest statement

The authors declare no competing interests.

## Abbreviations

CKD, chronic kidney disease; CRAE, central retinal arteriolar equivalent; EAF, effect-allele frequency; FDR, false discovery rate; GWAS, genome-wide association study; HDL-L, high-definition likelihood local analysis; LD, linkage disequilibrium; LDSC, LD Score regression; LAVA, local analysis of co-variant association; MR, Mendelian randomization; OCT, optical coherence tomography; UKB, UK Biobank.

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

**Figure 1. Complementary evidence framework with data-integrity-qualified directionality.** Retinal phenotypes span neuroretinal, outer-retinal and microvascular domains, while systemic contexts span cardiovascular, metabolic, renal, neurodegenerative and immune or inflammatory disease. Genome-wide sharing was evaluated across all 14 retinal traits and eight diseases (112 pairs), and local analysis retained the locked 47-pair subset. Directional MR was restricted prospectively to seven OCT traits with verifiable source allele-frequency semantics (112 directions). The seven vascular traits remained in correlation analyses but were not evaluated by MR. *Alt text:* Three parallel evidence layers distinguish the full retinal panel used for global and local analyses from the seven-trait OCT subset used for directional MR.

**Figure 2. Integrated evidence after Amendment 004.** Genome-wide sharing included 112 pairs with no FDR-significant result. Primary HDL-L included 116,472 block tests with no global-local FDR-significant result. Native LAVA sensitivity analysis included 26,639 rows, with nine FDR-significant rows of which eight were boundary-sensitive. OCT-only directional MR included 112 directions, with 110 null and two suggestive classifications and no FDR-positive direction. Seven vascular traits were excluded from directional analysis because release-specific allele-frequency semantics remained unresolved. Track positions are categorical and do not represent comparable discovery proportions across different testing universes. *Alt text:* Four non-proportional evidence tracks show the testing universe, corrected result and bounded interpretation for genome-wide, primary local, LAVA sensitivity and OCT-only MR analyses.

**Figure 3. Local retinal–systemic evidence was sensitive to inference procedure and testing framework.** (A) Historical approximation and native LAVA are compared only within the same 26,639-row universe, yielding 1,877 and nine FDR-significant rows, respectively. (B) Native LAVA boundary diagnostics show 16,938 confidence intervals touching or exceeding |rho|=1, 347 raw estimates with |rho|>1 and 68 with |rho|>1.25; 63.6% of native rows had a confidence interval touching or exceeding the boundary. (C) The primary HDL-L analysis completed 116,472 block tests and yielded no global-local FDR-significant result. HDL-L and LAVA use different local testing universes and are not interpreted as denominator-matched discovery-rate comparisons. Vascular traits remained eligible for the originally admitted local pairs. *Alt text:* A dot comparison preserves visibility of nine native LAVA rows, a bar chart reports boundary behavior, and a separate information panel reports the primary HDL-L result.

## Supplementary figure legends

**Supplementary Figure S1. Genome-wide genetic-correlation matrix.** The heatmap displays the 112 retinal–systemic LD Score regression estimates. Outlines identify nominal P<0.05 cells; none survived FDR correction across the complete 112-pair family. Color encodes the estimated genetic correlation and does not indicate corrected significance.

**Supplementary Figure S2. Final directional-evidence matrix.** OCT cells summarize classifications from the 112-direction Amendment 004 family. Vascular cells are labelled not analysed because source allele-frequency semantics remained unresolved; they must not be interpreted as null. No OCT direction survived global FDR correction.

## Tables

**Table 1. Dataset-level inventory of retinal and systemic GWAS resources.** Trait-specific analysis N was not available in the prespecified registry for the Zhao et al. OCT traits; the release-level mean of 60,748 is shown. Sample size varied by vascular phenotype. UK Biobank status describes participation in the source GWAS, not pairwise overlap.

**Table 2. Retinal-domain interpretation boundary.** Neuroretinal and outer-retinal OCT traits were analysed in Amendment 004 MR. Microvascular traits remained in global and originally admitted local analyses but were not evaluated by MR because release-specific allele-frequency semantics could not be resolved authoritatively. Global evidence covers all 112 retinal-disease pairs, local evidence covers the locked 47-pair subset, and directional evidence covers the complete 112-direction OCT-only family.
