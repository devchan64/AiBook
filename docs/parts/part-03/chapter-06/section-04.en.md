# P3-6.4 Why Not Every Column in a Summary Table Is a Feature

> Section ID: `P3-6.4`
> Version: `v2026.07.20`

The fact that a column appears in a summary table and the judgment that it is a feature are not the same statement. A summary table can contain features that describe sample structure, but it can also contain columns for comparison, candidate result columns, and columns for identification and context. So the distinction to hold first in this section is that `a column in the summary table` and `a feature to be read as model input` do not automatically match.

## Why Is This Distinction Needed

Once we create a one-action summary table, many kinds of columns can sit together inside one table like this.

| Example of a column name | Is it directly a feature? | A more natural role |
| --- | --- | --- |
| `mid_flow_mean` | usually yes | A feature that describes sample structure |
| `late_minus_early` | usually yes | A feature that shows change structure |
| `baseline_mid_flow_mean` | it depends | A comparison-reference column |
| `review_needed` | no | A result or target-label candidate |
| `event_id` | no | An identification column |
| `captured_at` | no | A time-context column |

This table matters because it slows the habit of reading `if it is a numerical column, it must be a feature`. Some columns describe the structure of the sample, some were attached for comparison, and some may record an outcome we later want to predict.

## Why Do Several Roles Mix Inside One Table

A summary table is a table that turns `one-action samples into readable rows`. But the information a person needs when reading the table and the information that should immediately be used as model input are not always exactly the same.

For example, we can imagine a table like this.

| event_id | mid_flow_mean | late_minus_early | baseline_mid_flow_mean | review_needed |
| --- | ---: | ---: | ---: | ---: |
| A | 2.40 | -0.80 | 3.05 | 1 |
| B | 2.55 | -0.10 | 2.60 | 0 |

If we look at this table, all of them may appear numerical, but their roles differ.

- `mid_flow_mean`, `late_minus_early` describe the structure of the sample.
- `baseline_mid_flow_mean` is a reference column attached for comparison with the usual state.
- `review_needed` can be a candidate result we later want to predict.
- `event_id` is the name that points to the sample.

So one table can temporarily contain together `comparison for people to read`, `input to be passed later into learning`, and `candidate results`.

## It Gets Less Confusing If We First Split into Four Kinds

When reading for the first time, it is better not to think too complicatedly, but to split the columns first into four kinds.

| Column kind | The question to ask first | Example |
| --- | --- | --- |
| Feature column | Does this value describe sample structure? | Average, slope, variability |
| Comparison column | Does this value let us read the difference between usual and recent state? | Baseline average, difference value |
| Candidate result column | Is this a result that we later want to predict? | `review_needed`, `final_status` |
| Identification / context column | Does this value distinguish the sample or explain its time point? | `event_id`, `captured_at` |

Once split into these four boxes, it becomes clearer why even columns that sit together in the same working table still play different roles. Comparison columns let us read the difference between usual and recent state, candidate result columns make us set aside values we may later want to predict, and identification/context columns keep us from losing which sample and which time point produced the judgment. So the distinction here is not a simple classification chart. It is a criterion for organizing why the columns inside one table should not all be read in the same way.

## Even the Same Numerical Column Is Not Always a Feature

What is especially easy to confuse is a column such as `baseline_mid_flow_mean` or `delta_from_baseline`. Because it is numerical, it looks like a feature, but we should first inspect why that column was attached.

| Numerical column | The misunderstanding that first comes to mind | What to check first |
| --- | --- | --- |
| `baseline_mid_flow_mean` | It is a number, so it must be a feature | Is it the baseline itself, or a value to be used as an input feature? |
| `delta_from_baseline` | It is a difference value, so it must be a feature | Is it a column that explains the comparison structure, or will it actually be passed as input? |
| `review_score` | It is a number, so it must be a feature | Is it an outcome score, or an input description value? |

So the format `numerical column` comes after the question `why was this column created?`

## Small Check Table

In this section, separating column roles matters more than a calculation experiment. We can reread the columns in a working table by `why the column was created`, not by `the format of the value`.

| Column name | Example value | Role to read first | Use directly as model input? | Reason for the judgment |
| --- | ---: | --- | --- | --- |
| `event_id` | A | context | no | It identifies the sample. |
| `mid_flow_mean` | 2.40 | feature | yes | It describes the sample's own middle-segment average. |
| `late_minus_early` | -0.80 | feature | yes | It describes the early-to-late change structure inside the sample. |
| `baseline_mid_flow_mean` | 3.05 | comparison | depends | It stores the baseline itself. |
| `delta_from_baseline` | -0.65 | comparison | depends | It expresses the gap versus the baseline. |
| `review_score` | 87 | target candidate | no | It may be an outcome score we later want to predict. |
| `review_needed` | 1 | target candidate | no | It is a result candidate: whether review is needed. |
| `captured_at` | 2026-07-08 09:10 | context | no | It records when the sample was captured. |

What this table shows is not a grand classification rule. The core point is that one working table can temporarily contain several kinds of columns side by side, and that those columns need to be read again with role-specific reasons. In particular, `baseline_mid_flow_mean` and `delta_from_baseline` are numerical columns, yet they are first read as comparison columns, while `review_score` and `review_needed` are numerical columns, yet they are first read as candidate results. This also explains why `depends` appears. The baseline itself or a difference-from-baseline value was created for comparison explanation, so whether it should immediately be passed on as an input feature has to be judged again later according to what prediction problem will be built.

If we touch this distinction once right after feature design, the illusion `aren't they all features anyway?` becomes weaker. A summary table is not a table that stores only features. It is a working table where feature candidates, comparison columns, candidate results, and identification/context columns can temporarily sit together. Once we read it this way, the roles of baseline-comparison columns and target-candidate columns also feel less abrupt when they reappear later.

This section can be read not only as the question `which numerical column is a feature?`, but as the problem of `column-role separation in a working table`.


So instead of the misunderstanding `if it is a numerical column, it must be a feature`, we should first ask whether each column describes the sample, holds a comparison reference, records a result, or merely keeps context.

## A Small Diagram

The core point of this section is that not every column in a working table should be read as the same kind. Even inside one table, columns split into feature, comparison, target-candidate, and context columns, and that role separation has to come first.

--8<-- "assets/part-03/chapter-06/p3-6-4-mermaid-01-en.mmd"

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because it explains a labeled example as the combination of features and label, it provides the basic frame for distinguishing input-description columns from candidate result columns. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it explains the design flaw in which a feature becomes a proxy for the label, it provides a basis for not carelessly mixing candidate result columns such as `review_needed` or `review_score` into the feature set. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it provides a standard context for recording and tracing provenance information separately, it can serve as a general basis for leaving identification/context columns such as `event_id` and `captured_at` as information with a role different from features that describe the sample itself. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
