# Part 3. Data Modeling

> Section ID: `P3-index`
> Version: `v2026.07.10`

In Part 2, we rebuilt the foundations for reading mathematics, Python, arrays, tables, and graphs. But being able to read calculation tools again does not immediately mean we can build AI problems well. When we first meet real source data, the first question is often closer to `what should count as one item of data?` than to `which model should we use?` In the overall structure of this book, Part 2 and Part 3 together form the basic-skills recovery range, and Part 3 is responsible for `rebuilding data-science problem structure`.

The representative case in Part 3 is described in a more general structure than any one device name. There is one automatically executed action, and that action leaves both a control-parameter time series and a sensor-data time series. Several actions can then be grouped again and compared as a recent segment versus a baseline. In this setting, one measurement at one moment can be treated as a sample, one full action can be treated as a sample, or a recent segment made of several actions can be treated as a sample. Depending on that choice, the dataset that gets built, the comparison method, the questions that remain interpretable, and the operational flow structure around how many branches of real action follow can all change. Even with the same source data, the AI problem changes completely depending on how we group it, what we keep, what we compare it against, and which action-flow structure we pass it into.

The way this representative case evolves through the Part can first be fixed with the table below.

| Stage | What one row means | What this stage mainly keeps |
| --- | --- | --- |
| Source log | one record during an action | sensor values, control values, time order |
| Action summary table | one action run | mean, slope, variability, segment differences |
| Recent-vs-baseline comparison table | a state comparison built from several actions | recent mean, baseline mean, difference values |
| Operational output | the result structure read by a person or handed to the next step | warning, review candidate, target-label candidate |

Here, data modeling does not mean only organizing storage structure. Data modeling is the work of re-expressing source data from reality into samples, features, baselines, and output structures that people can compare and AI systems can use. More precisely, it is closer to designing `what should count as one sample`, `how should raw logs be regrouped into summary tables`, `which features and comparison structures should remain`, `how conservatively should we speak`, and `what should remain a comparison report for now versus what should be raised into a prediction problem`, rather than simply `reading a given table`.

Part 3 re-bundles topics that often appear separately in a data-science curriculum, such as data wrangling, feature engineering, sample design, inference, and problem framing, into one relearning flow. Instead of listing them as separate named procedures, this Part follows one representative case and checks, step by step, `what becomes a sample`, `what gets regrouped into a table`, `what gets compared`, and `how far we can speak`. The focus of Part 3 is therefore on establishing `problem representation structure` before algorithms.

The table below shows more briefly that the spine of Part 3 is not an arbitrary order, but a re-arrangement of standard concept bundles from data science and machine learning through the perspective of `rebuilding problem structure`.

| Bundle in this Part | Corresponding standard concepts | Representative evidence axis |
| --- | --- | --- |
| Regrouping source data | data wrangling, sample design | W3C PROV, Fayyad/KDD |
| Building features and baselines | feature engineering, labeled example, base period | Google ML Glossary, BLS |
| Closing interpretation strength and output boundaries | problem framing, conservative interpretation, output structure | Google ML Glossary, NASEM |

Within Part 3, the larger definition of `data modeling` itself is first fixed in 3.1, and the working sequence is fixed in 3.2. Later sections keep only the minimum connection needed for the current question rather than repeating long definitions of the same term. [Sample](../../reference/concept-glossary.md#glossary-sample), [feature](../../reference/concept-glossary.md#glossary-feature), [baseline](../../reference/concept-glossary.md#glossary-baseline), [comparison report](../../reference/concept-glossary.md#glossary-comparison-report), and [target](../../reference/concept-glossary.md#glossary-target) can be checked again in the glossary when needed.

Part 3 first fixes what data modeling is trying to achieve and in what order it moves. It then checks why stored records should not be read immediately as a dataset, decides the meaning of one row and one sample, and regroups raw logs into comparable tables. After that, it designs features and intermediate representations, separates which columns are for identification, comparison, and target candidates, and then builds a structure for comparing recent segments with a baseline. It also places boundaries on how far interpretation can go in front of small samples and unstable repeatability. Finally, it separates problems that should remain comparison reports from problems that should be raised into prediction tasks, and it closes both input/output boundaries and time boundaries.

## Purpose of Part 3

- Prevent data modeling from being mistaken for database design alone.
- Build familiarity with the flow that re-expresses source data as samples, summary tables, features, and baselines.
- Show that data preparation, feature engineering, conservative interpretation, and problem framing are one connected flow.
- Help the reader learn which problem structures should be closed first, without mixing comparison reports and prediction problems.

## Why It Is Needed

- Because we first have to learn that raw logs are not immediately a dataset.
- Because without a fixed sample unit and comparison reference, explanations of features and labels become unstable.
- Because review candidates and confirmed diagnoses, and baseline comparison and absolute-value judgment, are often confused.
- Because even when the average is the same, segment patterns and variability can differ, and it is easy to conclude too quickly from one representative value.
- Because if sample structure and input boundaries remain unclear, later learning explanations can also turn into names without problem structure.

## Main Questions

- What role does data modeling play in the broader data-science flow?
- Why are stored records not immediately a dataset?
- How are one row and one sample different, and what table structure is needed?
- Why are features and intermediate representations designed the way they are?
- Why must baselines and comparison structure be fixed before models?
- How far can interpretation go in front of sample size and repeatability?
- What should remain a comparison report, and what should be passed into a learning problem?

## Reading Order

Part 3 proceeds through 9 chapters, but the flow can be summarized in three bundles.

1. Fix the role of data modeling and its working order.
2. Rebuild storage structure into a comparable structure with samples, tables, features, and baselines.
3. Set interpretation boundaries, then separate comparison reports from prediction problems and close the input/output boundaries.

This order matters because if we talk about features and labels before turning storage structure into problem structure, the terms float in midair, and if we bring up prediction problems before interpretation boundaries are set, model names appear before data structure. The table below briefly shows what each of these three bundles secures.

| Flow bundle | Question fixed here | Structure left behind |
| --- | --- | --- |
| Fixing role and order | What does data modeling take responsibility for, and in what sequence does it decide? | the position of problem-structure design, the map of the working sequence |
| Rebuilding comparison structure | Into what sample, table, feature, and baseline structure should stored records be read again? | dataset candidates, summary tables, feature columns, baseline comparison tables |
| Closing interpretation and problems | How far can we speak, and what should still remain a report? | conservative statements, operational outputs, input/output boundaries, time boundaries |

The questions repeated through Part 3 can also be grouped. What should count as one sample, into what table should raw logs be regrouped, which features and baselines should remain, what should stay as a comparison report and what should rise into a target candidate, and whether the input structure and observation boundaries are closed. Each chapter is responsible for making one of those question bundles clearer.

## Scope and Non-Scope

Part 3 covers sample units, raw logs and summary tables, features and intermediate representations, baseline comparison, sample size and repeatability, and the boundary between warning candidates and label prediction.

By contrast, detailed learning procedures for specific machine-learning algorithms, the detailed procedure of train/validation/test splits, and complex time-series deep-learning structures are not the center here.

The reason for this scope limit is simple. The responsibility of Part 3 is to make clear first `what data should be built into what structure`.

## Connection to the Previous Part

If Part 2 rebuilt calculation and representation tools, Part 3 decides `what should be represented in what structure` with those tools. Tables, arrays, summary statistics, and visualizations begin here to act as `problem-representation tools`.

## Understanding That Should Remain After Part 3

The reader should come away with the sense that a dataset is not a given table but a designed comparison structure, and that machine learning is only read properly on top of that structure. Sample structure, features, target candidates, and time boundaries must be organized first, so that later learning explanations can also be read with `what is being predicted` and `what inputs are being used` kept clear.

## Sources and Further Reading

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. Because it presents data collection, cleaning, representation, modeling, and interpretation as one data-science flow, it supports the curriculum view on this page that places Part 3 as a `problem-structure recovery` section. [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`. Because it provides role distinctions for core terms such as sample, feature, label, and label leakage, it supports the explanation that Part 3 must fix sample structure and input/output boundaries before model names. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because it treats provenance and derivation together, it supports the shared premise of Part 3 that when source data is remade into problem-representation structures, the rules that produced derived tables must remain traceable. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
