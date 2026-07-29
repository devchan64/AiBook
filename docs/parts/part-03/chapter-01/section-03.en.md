# P3-1.3 How Should a Data Question Be Written So the Problem Structure Appears Before the Model

> Section ID: `P3-1.3`
> Version: `v2026.07.25`

A good [data question](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-data-question) should first reveal `what will count as one case`, `what will be compared with what`, and `what we ultimately want to know`. Only when this question structure is in place before model names or technology names do the later sample unit, table structure, features, baselines, and output structure also settle into place together. In particular, the question that selects what a person should inspect first should visibly lead to a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure), while the question that defines what should later be predicted should lead to a target candidate. A bad question, by contrast, has a model name but leaves the sample unit and comparison reference empty.

| Still too early a phrasing | A better data question |
| --- | --- |
| Let us build an anomaly-detection model | Has one recent execution become more unstable than the usual executions? |
| Let us make it a classification problem | Which one execution should a person review first? |
| Let us use time-series deep learning | Can we decide whether the raw time series should be read as one action input or as a bundle of recent segments? |
| Let us improve accuracy | Have we distinguished whether the current result is a review candidate or a prediction label? |

This table matters not because the goal is to write `good-sounding questions`. It matters because once the question sentence changes, the sample, table, features, baselines, and output structure that come next change with it.

## Three things that must appear in the question sentence

At the front of Part 3, the data question does not have to be written in a highly complex form. It is enough to check first whether the following three things are visible.

1. What will count as one case
2. What do we want to know
3. What is the comparison reference or the result format

Condensed into a table, those three become the following.

| Question element | Why it is needed |
| --- | --- |
| Sample unit | Because we have to decide what one row will mean |
| Desired knowledge | Because it determines the direction in which features and comparison structure will be designed |
| Comparison reference or result format | Because it determines whether we need a baseline, a review candidate, or a target-label candidate |

For example, the sentence `Is recent behavior abnormal?` is still too broad. Once it is rewritten as `If one action is treated as one case, have the most recent 20 actions become shakier than the usual 200?`, the comparison unit and baseline structure finally start to become visible together.

## How to rewrite the question into a better form

At first, it is usually easier not to write the finished question in one attempt, but to revise an overly broad sentence step by step.

| The phrase that first comes to mind | First revision | Second revision |
| --- | --- | --- |
| I want to catch anomalies | I want to know which actions should be examined first | I want to choose the cases in the recent segment that a person should review first, using one action as one case |
| I want to predict the result | I want to decide what result I want to predict later | I want to see whether an outcome candidate such as `review_needed` can be created from an action-level feature table |
| I want to try deep learning | I want to decide whether to use the raw time series as it is | I first want to decide whether an action-level summary vector or a bundle of recent time-series segments is the more natural input structure |

So rewriting the question is not a matter of polishing the sentence. It is the work of revealing the problem structure step by step.

## Good questions and questions that are still too early

The comparison below shows a confusion that appears especially often in Part 3.

| Question type | Why it is still too early, or why it is better |
| --- | --- |
| `Which model would improve accuracy?` | It is too early if there is not yet a label or sample unit |
| `In this one execution, is the late-stage drop larger than in usual executions?` | It is better because the sample unit and comparison reference are visible |
| `Would deep learning solve it?` | It is too broad because the input structure and target structure are empty |
| `Can the raw time series be cut into action-level units and turned into comparable inputs?` | It immediately forces the sample unit and input structure to be decided |

The important point here is not that a `good question` must always be short. It is that it must contain the clues required for the design that follows.

## A small diagram

The same scene can lead into a completely different Part 3 flow depending on how the question is written.

| Question sentence | The next stage that follows immediately |
| --- | --- |
| Has one recent execution become shakier than usual? | Set the sample unit to one action and build a summary table |
| Have the most recent 20 cases changed relative to the prior 200? | Build an aggregate table and a baseline-comparison structure |
| Which actions should a person inspect first? | Build a review queue and output structure |
| Can a candidate future result be defined? | Separate target candidates from the input feature table |

In other words, one question immediately determines the direction of the next Chapter.
What matters in this example is not code execution but the correspondence itself. When the question changes, the table structure that comes next changes with it, so even with the same source data the next table the reader should imagine first also changes.

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-3-mermaid-01-en.mmd"
```

If the question itself is vague, then `what table has to be rebuilt` also remains abstract. That is why rewriting the data question is not an extra sentence-polishing step. It is the starting point for deciding through what sample and table structure the stored data will be read again. The moment the question is written better, it also becomes much more direct why the sample and baseline are needed first. More broadly, a good data question is not just a sentence formulation. It is a problem-definition device that fixes the `target unit`, `desired outcome`, and `comparison or output structure` together at once. In other words, a good data question is not `a nicely worded sentence`, but the minimum design sentence that determines the table structure and comparison structure that follow.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`, `label`, `label leakage`. Because it explains that the unit combining example and label must be fixed first, it supports the judgment in this section that the sample unit and result structure should appear together inside the data question. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general concept of a reference period for comparison, it strengthens the explanation that a good data question should also reveal `what is being compared with what`. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `From Data Mining to Knowledge Discovery in Databases`. Because it explains a broader knowledge-discovery flow that does not separate problem definition from data preparation, it becomes the general background for the claim that a data question is the starting point that opens the later table structure and comparison structure. [https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
