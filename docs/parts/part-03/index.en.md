# Part 3. Data Modeling

> Section ID: `P3-index`
> Version: `v2026.07.20`

In Part 2, we rebuilt the foundations for reading math, Python, arrays, tables, and graphs. But being able to read computational tools again does not immediately mean you can build an AI problem well. When you first face real source data, the first question is usually closer to `what should count as one item of data?` than to `which model should we use?` In the overall structure of this book, Part 2 and Part 3 together form the basic-skills recovery range, and Part 3 is responsible for `rebuilding data-science problem structure`.

The representative case in Part 3 is described in a structure more general than any one device name. There is one automatically executed action, and that action leaves both the time series of control parameters used in the action and the time series of sensor observations captured during the action. Several actions can then be grouped again and compared as a recent segment versus a baseline. In that setting, one measurement at one moment can be treated as a sample, one full action can be treated as a sample, or a recent segment made of several actions can be treated as a sample. Depending on that choice, the dataset that gets built, the comparison method, the interpretable questions, and the operational flow structure around how many branches of real action follow can all change. Even with the same source data, the AI problem changes completely depending on how you group it, what you keep, what you compare it against, and what action-flow structure you pass it into.

The way this representative case evolves through the Part can first be held with the reference table below.

| Stage | What one row means | What this stage mainly keeps |
| --- | --- | --- |
| Source log | one record during an action | sensor values, control values, time order |
| Action summary table | one action run | mean, slope, variability, segment difference |
| Recent-vs-baseline comparison table | a state comparison built from several actions | recent mean, baseline mean, difference value |
| Operational output | a result read by a person or handed to the next step | warning, review candidate, target-label candidate |

Here, data modeling does not mean only organizing storage structure. Data modeling is the work of re-expressing source data from reality into samples, features, baselines, and output structures that people can compare and AI can use. More precisely, it is closer to designing `what should count as one sample`, `how raw logs should be regrouped into summary tables`, `which features and comparison structures should remain`, `how conservatively we should speak`, and `what should still remain a comparison report versus what should be raised into a prediction problem`, rather than simply `reading a given table`.

Part 3 re-bundles topics that often appear separately in a data-science curriculum, such as data wrangling, feature engineering, sample design, inference, and problem framing, into one relearning flow. It does not list those items as a sequence of named procedures. Instead, it follows one case and checks in order `what becomes a sample`, `what gets regrouped into a table`, `what gets compared`, and `how far we can speak`. So the focus of Part 3 is on establishing `problem representation structure` before algorithms.

The table below shows more briefly that the spine of Part 3 is not an arbitrary order, but a rearrangement of standard concept bundles from data science and machine learning through the perspective of `rebuilding problem structure`.

| Bundle in this Part | Corresponding standard concepts | Representative evidence axis |
| --- | --- | --- |
| Regrouping source data | data wrangling, sample design | W3C PROV, Fayyad/KDD |
| Building features and baselines | feature engineering, labeled example, base period | Google ML Glossary, BLS |
| Closing interpretation strength and output boundaries | problem framing, conservative interpretation, output structure | Google ML Glossary, NASEM |

Within Part 3, the larger definition of `data modeling` itself is first fixed in 3.1, and the working sequence is fixed in 3.2. Later sections keep only the minimum connection needed for the current question rather than repeating long definitions of the same term. [Sample](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-sample), [feature](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-feature), [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), [comparison report](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparison-report), and [target](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target) can be checked again in the glossary when needed.

Part 3 first fixes what data modeling is trying to achieve and in what order it proceeds. It then checks why stored records should not be read immediately as a dataset, decides the meaning of one row and one sample, and regroups raw logs into comparable tables. After that, it designs features and intermediate representations, and separates which columns are for identification, comparison, and target candidates. It then builds the structure that compares recent segments with a baseline, places boundaries on how far interpretation can go in front of small samples and unstable repeatability, and finally separates problems that should remain comparison reports from problems that should be raised into prediction problems while closing input/output boundaries and time boundaries.

## The Role Data Modeling Takes On

- Prevent data modeling from being misunderstood as database design alone.
- Build familiarity with the flow that re-expresses source data as samples, summary tables, features, and baselines.
- Show that data preparation, feature engineering, conservative interpretation, and problem framing form one connected flow.
- Help the reader learn which problem structures should be closed first, without mixing comparison reports and prediction problems.

## Why It Is Needed

- Because you first have to learn that raw logs are not immediately a dataset.
- Because without a fixed sample unit and comparison reference, explanations of feature and label become unstable.
- Because warning candidates and confirmed diagnosis, and baseline comparison and absolute-value judgment, are often confused.
- Because even when the average is the same, segment pattern and variability can differ, and it is easy to conclude too quickly from one representative value.
- Because if sample structure and input boundaries remain vague, later learning explanations also tend to leave only names without a problem structure.

## Main Questions

- What role does data modeling play in the overall data-science flow?
- Why are stored records not immediately a dataset?
- How are one row and one sample different, and what table structure is needed?
- Why are features and intermediate representations designed the way they are?
- Why must baselines and comparison structure be fixed before models?
- How far can interpretation go in front of sample size and repeatability?
- What should remain a comparison report, and what should be passed into a learning problem?

## Flow for Building Problem Structure

Part 3 proceeds through 9 chapters, but the flow can be summarized in three bundles.

1. Fix the role of data modeling and its working order.
2. Rebuild storage structure into a comparison structure with samples, tables, features, and baselines.
3. Set interpretation boundaries, then separate comparison reports from prediction problems and close the input/output boundaries.

This order matters because if you talk about feature and label before turning storage structure into problem structure, the terms float in the air, and if you bring up prediction problems before interpretation boundaries are fixed, model names become visible before data structure. The table below shows again, in shorter form, what each bundle fixes.

| Flow bundle | Question fixed here | Structure left behind |
| --- | --- | --- |
| Fixing role and order | What does data modeling take responsibility for, and in what sequence does it decide? | the position of problem-structure design, the map of working order |
| Rebuilding comparison structure | Into what sample, table, feature, and baseline structure should stored records be read again? | dataset candidates, summary tables, feature columns, baseline comparison tables |
| Closing interpretation and problems | How far can we speak, and what should still remain a report? | conservative statements, operational outputs, input/output boundaries, time boundaries |

The questions repeated through Part 3 can also be grouped as follows: what should count as one sample, into what table raw logs should be regrouped, which features and baselines should remain, what should stay as a comparison report and what should rise into a target candidate, and whether the input structure and observation boundaries are closed. Each chapter is responsible for making one of those question bundles clearer.

## Boundaries Data Modeling Closes and Questions Left Open

Part 3 covers sample units, raw logs and summary tables, features and intermediate representations, baseline comparison, sample size and repeatability, and the boundary between warning candidates and label prediction.

By contrast, the learning procedure of specific machine-learning algorithms, the detailed procedure of train/validation/test splits, and complex time-series deep-learning structures themselves are not the center here.

The reason for this scope limit is simple. The responsibility of Part 3 is to clarify first `what data should be built into what structure`.

## Understanding That Should Remain After Part 3

What should remain is the sense that a dataset is not a given table but a designed comparison structure, and that machine learning is only read properly on top of that structure. Sample structure, features, target candidates, and time boundaries must be organized first, so that later learning explanations can also be read with `what is being predicted` and `what input is being used` kept clear.

## Sources and Further Reading

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. Because it explains data collection, cleaning, representation, modeling, and interpretation as one connected data-science flow, it supports the curriculum perspective on this page that places Part 3 as a `problem-structure recovery` section. [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`. Because it provides role distinctions for core terms such as sample, feature, label, and label leakage, it supports the explanation that Part 3 must fix sample structure and input/output boundaries before model names. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it treats provenance and derivation together, it supports the common premise of Part 3 that when source data is rebuilt into problem-representation structures, the rules that produced derived tables must remain traceable. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `Knowledge Discovery and Data Mining: Towards a Unifying Framework`, Microsoft Research publication page, 1996. This classic KDD reference supports treating source-data regrouping as a separate axis in the data preparation and discovery flow. [https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/](https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Consumer Price Index: Concepts`, Handbook of Methods. Its explanation of CPI index values and base periods is used as a reference for the idea of fixing a base period before comparing current values. [https://www.bls.gov/opub/hom/cpi/concepts.htm](https://www.bls.gov/opub/hom/cpi/concepts.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
