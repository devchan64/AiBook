# P3-5.5 How Do We Handle Samples with Missing Values or Empty Segments

> Section ID: `P3-5.5`
> Version: `v2026.09.19`

When encountering a [missing value](/AiBook/en/reference/concept-glossary-alpha/m/#glossary-missing-value), first identify what is absent. A missing observation, an unavailable segment mean, and an unconfirmed action end are different problems. **Retaining a sample and being able to calculate a particular feature are separate decisions.**

## A Measured Zero and Missingness Change the Denominator

If observations are 2 and 4 with a third missing, the observed-value mean is `(2+4)/2 = 3`. Filling the blank with zero gives `(2+4+0)/3 = 2`, introducing an assumption about an unobserved value. If the third value was actually measured as zero, however, 2 is the mean of three observations.

The observed mean of 3 does not recover the mean of the original three values including the missing one. Preserve observation counts, missing counts, and whether values were filled. Even a recorded zero needs separate sensor-validity checks; a blank does not itself mean “flow stopped.”

## Read the Blanks in E01–E03 Differently {#small-code-example}

The [fictional segment-summary CSV](/AiBook/assets/part-03/chapter-05/p3_5_5_missing_segments.csv) contains 36 candidate event summaries. Mean flow is in L/min, and a blank means that mean was not obtained. `end_detected=1` means completion was confirmed; 0 means it was not. Zero alone cannot distinguish an unfinished action from a missed completion record.

| event_id | early_flow_mean | mid_flow_mean | late_flow_mean | end_detected |
| --- | ---: | ---: | ---: | ---: |
| E01 | 1.10 | 2.40 | 1.80 | 1 |
| E02 | 1.00 | 2.50 | Unavailable | 1 |
| E03 | 1.20 | Unavailable | Unavailable | 0 |

Assume starts and event linkage are correct and populated segment means for confirmed-complete events have been checked. Under those assumptions, use the following decisions for comparing middle−early differences. Comparisons requiring late values remain separate.

| Event and state | Allowing partial summaries | Usable values | Values not calculated or confirmed |
| --- | --- | --- | --- |
| E01: three means, confirmed end | Retain | Middle−early 1.30; late−middle −0.60 | Rates per second remain unknown without times |
| E02: confirmed end, no late mean | Retain for early/middle comparison | Middle−early 1.50 | Late mean and late−middle difference |
| E03: unconfirmed end | Hold from completed-action comparison | Preserve 1.20 as a clue for tracing source records | Total duration and segment features depending on the end boundary |

Retaining E02 does not make it usable for late-segment comparisons. E03’s 1.20 need not be erased, but if “early” depends on the end boundary, its validity as an action feature needs checking. Holding means withholding from this comparison and inspecting source records, not deleting them.

A blank segment mean also does not prove that every sensor record in that segment is missing. Distinguishing insufficient observations, quality rejection, and failed aggregation requires source records and aggregation rules.

## Which Twelve Events Disappear When Retention Policy Changes?

Use `keep_partial_samples` as the policy name for keeping incomplete events as candidates for the current comparison. `True` retains confirmed-complete events with early and middle means for comparisons using those values; `False` retains only events with all three means. Both hold events with unconfirmed ends. This is a case-specific policy, not a universal missing-data rule.

| CSV state | Events | Retained with True | Retained with False |
| --- | ---: | ---: | ---: |
| Three means and confirmed end | 12 | 12 | 12 |
| Confirmed end, no late mean | 12 | 12 | 0 |
| Unconfirmed end, no middle/late means | 12 | 0 | 0 |
| Total | 36 | 24 | 12 |

Without changing the source, find events newly excluded by switching True to False. They are **E02, E05, E08, E11, E14, E17, E20, E23, E26, E29, E32, E35**. The twelve unconfirmed-end events such as E03 were already held, so they are not new exclusions caused by the policy change.

Retained events fall from 24 to 12. Yet **comparisons using late means still have twelve events under either policy**. The twelve additional events retained by True lack those values. A retained-sample count is not automatically the denominator for every feature.

## Check Operating Conditions Separately from Missingness States

This CSV establishes counts by missingness state. Without machine, shift, load, or collection-period columns, it cannot show which operating conditions are excluded more often. Link condition data through `event_id`, then compare counts and shares before and after exclusion. Do not infer conditions from IDs such as E01.

As a separate hypothetical assumption, suppose all twelve events lacking late means were night events. The stricter policy removes those twelve night events. Whether other night events remain requires additional condition data. This illustrates how exclusions can change coverage; it is not a claim about night distribution in the actual CSV.

## Missingness Indicators Are Records, Not Automatically Valid Features {#looking-through-a-small-diagram}

Keeping `late_mean_missing`, `end_detected`, `keep_sample`, and `exclusion_reason` makes missing information and exclusion decisions traceable. Whether missingness relates to communication, sensors, or operating conditions requires investigation. Blanks alone cannot identify a fault cause.

Before using a missingness indicator as model input, check whether it was available at prediction time, whether it arose after the target outcome, and whether its meaning persists between training and application. Creating an indicator does not establish predictive usefulness or improved performance.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-5-mermaid-01-en.mmd"
```

Correct “We retained E02, so we can fill its late value with zero and compare it.” One answer is: “Retain E02 for early/middle comparison, leaving its late mean and difference unavailable. Exclude it from comparisons requiring late values, recording the reason and the denominator for that comparison.”

## Checklist

- Can you explain why the observed mean of 3 and zero-filled mean of 2 answer different questions?
- Can you distinguish E02’s unavailable late mean from E03’s unconfirmed end?
- Have you identified the shared state of the twelve newly excluded events?
- Can you distinguish 24 retained events from twelve eligible for late comparison?
- Have you identified the extra data needed to inspect exclusions by operating condition?
- Can you separate an indicator’s recordkeeping value from its suitability as model input?

## Sources and Further Reading

- scikit-learn developers, [Imputation of missing values](https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values){: target="_blank" rel="noopener noreferrer" }. Explains that removing incomplete rows can lose information and indicators can preserve original missingness. The retention/holding policies and numerical examples here are our fictional design. / Accessed: 2026-09-19
