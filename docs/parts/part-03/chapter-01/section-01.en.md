# P3-1.1 What Is Data Modeling Trying to Achieve

> Section ID: `P3-1.1`
> Version: `v2026.07.20`

As soon as the reader enters Part 3, they meet words such as [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample), [feature](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature), [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), [output structure](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure), and [target](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target). These terms do not stand alone. The outer judgment that decides what counts as one case, which values remain, what gets compared, and in what result format the process closes is [data modeling](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-data-modeling).

If data modeling is understood only as organizing storage structure, it is easy to think of it as little more than making an already existing table look cleaner. But in AI and data analysis, data modeling is an earlier judgment than that. Data modeling is the work of deciding `what question can this source data be turned into an answerable structure for?`

The most common early confusion is to treat `how should we store the database?` and `how should we build a problem structure that AI can read?` as if they were the same task. They are connected, but their goals differ.

| Point of comparison | A view centered on storage structure | The data-modeling view of Part 3 |
| --- | --- | --- |
| First question | How should records be stored and retrieved without loss? | How should samples and comparison structure be built so a question can be answered? |
| Representative unit | one log row, one event, one sensor reading | one action, one recent segment, one entity as an analysis sample |
| Main concern | Is it stored without omission, linked correctly, and traceable? | What can be compared, and which features should remain? |
| Immediate result | raw log tables, event tables, joinable storage structure | summary tables, feature tables, baseline comparison tables, output structures for review |
| Question in this Part | It may still be a starting point, but it is not the end point | The central question handled throughout Part 3 |

If storage structure is `the frame for not losing records`, data modeling is closer to `the frame for building comparison structure that can answer a question`. Even with the same source data, storage structure alone is not enough. We also have to decide which sample unit and comparison reference it should be reread through before a table for learning and analysis exists.

Suppose there is a record of automatically executed actions. The source data may contain time-step sensor values, control parameters, and start and end times for each action. That structure may be sufficient for storage and traceability. But in that state, it is still difficult to answer questions such as `was this action different from the usual ones?`, `is repeatability unstable in the recent segment?`, or `what should a person review first?`

What data modeling is trying to achieve here is simple. It takes source data as it is and rebuilds it into a structure that people can compare and models can use. The result that has to be built can usually be divided into four layers.

1. Decide what should count as one sample.
2. Build features that describe that sample.
3. Set a baseline for what the recent state will be compared against.
4. Decide the output structure, such as whether the final result is for human review or a candidate prediction target.

So data modeling is closer to `designing a comparison structure that makes a problem solvable` than simply `organizing a table`.

At this point, the relation between data modeling and data science also needs to be fixed. Data science is the broader flow that includes data collection, cleaning, exploration, summarization, comparison, interpretation, prediction, and connection to decision making. Inside that larger flow, the data modeling that Part 3 focuses on is closer to `the front-end judgment that turns source data into a problem structure for AI learning and analysis`. In other words, Part 3 is not the Part that teaches all of data science. It teaches the core design range inside data science that AI learning must pass through.

To see this more clearly, place the outputs data modeling is actually trying to create side by side.

| What it tries to achieve | Why it is needed | Question that it connects to later |
| --- | --- | --- |
| Sample unit | Because we must decide what counts as one case | What does one row mean? |
| Feature table | Because descriptive values for comparison and learning must be built | Which values should remain? |
| Baseline comparison structure | Because the recent state must be read against the usual state | What should it be compared to? |
| Output structure | Because human review and prediction targets must not be mixed | What should the result be emitted as? |

The important point in this table is that data modeling is not yet the `model selection` stage. At this stage, before classifier names or deep-learning structures, we first have to decide what table gets built and what comparison becomes possible. Only then do `X`, `y`, evaluation, and baseline models stop floating in midair in the later machine-learning Parts.

Reduced to a short summary, the order of judgment in data modeling can be read like this.

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-1-mermaid-01-en.mmd"
```

If this still feels too abstract, it becomes clearer when source data and post-modeling tables are placed side by side in the same scene.

Suppose source data is accumulated as time-step logs like this.

| action_id | t_sec | flow_rate | pressure | valve_open |
| --- | ---: | ---: | ---: | ---: |
| A-101 | 0.0 | 24.8 | 101.2 | 1 |
| A-101 | 1.0 | 25.1 | 101.0 | 1 |
| A-101 | 2.0 | 23.9 | 102.4 | 1 |
| A-102 | 0.0 | 24.7 | 100.9 | 1 |
| A-102 | 1.0 | 24.8 | 101.1 | 1 |
| A-102 | 2.0 | 24.8 | 101.0 | 1 |

This table is sufficient for storage and traceability, but it is difficult to compare `which action was more unstable than usual` directly from it. Data modeling rebuilds logs like this into an action-level summary table.

| action_id | flow_mean | flow_std | pressure_mean | late_drop_rate | baseline_gap | review_flag |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A-101 | 24.60 | 0.63 | 101.53 | -1.2 | 0.9 | review |
| A-102 | 24.77 | 0.06 | 101.00 | 0.0 | 0.1 | normal |

The difference between these two tables shows exactly what data modeling is for.

- The source-data table preserves time-step records.
- The modeled table reveals the sample unit and features needed for comparison and judgment.
- An output structure such as `review_flag` is used to choose what a person should inspect first.
- A comparison column such as `baseline_gap` directly connects the recent state to the usual state.

The difference between the old human-centered reading and what data modeling changes can be compressed into one scene.

| Judgment stage | When a person reads the logs directly | After data modeling |
| --- | --- | --- |
| How one case is counted | reads one time row at a time | groups one full action as one sample |
| How comparison works | scans many rows by eye | compares immediately through mean, variability, and baseline gaps |
| How priority is decided | the person chooses again while rereading | a column such as `review_flag` filters first |
| Next action | records remain, but judgment is slower | the structure can be passed directly to a review-candidate table or prediction-input table |

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-1-mermaid-02-en.mmd"
```

Whether data modeling has succeeded is not judged by whether a flashy model was used. It is judged by whether the following questions can be answered.

- What does one row in the current table mean?
- Why was this value kept?
- What should it be compared against?
- Is this result an automatic conclusion, or only a candidate for human review?

If those four questions can be answered, data modeling has already succeeded to a large degree. If they cannot be answered, then no matter how much source data exists, later model explanations are likely to remain unstable. Increasing learning density is not mainly about piling on more definitions. It is closer to showing enough cases and comparison structure that the reader can answer these four questions alone.

That is why Part 3 does not unfold every topic of data science. Data cleaning and exploration are brought in only as needed, while statistical testing and algorithm details are kept outside the center. Instead, it first fixes `what should count as a sample`, `which values should remain`, `what it should be compared to`, and `what output structure it should pass into`. Once that boundary is secured, the data problem can be read as `a problem solved on top of an already designed structure`.

Seen more broadly, this section is the starting point of data-problem design, where `what should count as one case`, `in what representation should it remain`, `what should it be compared against`, and `in what result format should it close` are all decided together.

So it is more accurate to read data modeling as `designing representation and comparison structure that can answer a question` than as simply `organizing a table`.

## Sources and Further Reading

- W3C, `PROV-Overview`. Because the provenance framework explains that it should support identifying an object and representing derivation, it becomes a general basis for the claim that `what counts as one case` and `through what process summary tables and comparison structures were made` should remain explainable. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `labeled example`, `feature`, `label leakage`. Because an example should be a natural unit where features and labels connect, and feature engineering is the process of building useful input structure, it supports the explanation that sample units, feature tables, and output structures must be fixed first in Part 3. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general concept of using a point or period in time as a reference, it supports the explanation that data modeling must first establish a baseline for what the recent state will be compared against. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `From Data Mining to Knowledge Discovery in Databases`. Because it explains a broader discovery flow that includes data collection, selection, preprocessing, transformation, and interpretation, it provides the general background for the boundary that Part 3 does not cover all of data science, but focuses on problem-structure design and representation transformation inside it. [https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
