# P3-9.7 How Do We Separate Inputs Available at Prediction Time from Later Outcomes

> Section ID: `P3-9.7`
> Version: `v2026.09.20`

[P3-9.6](section-06.en.md) checked label meanings and judgment conditions. Now we must construct inputs from information actually available before the outcome was known. A [prediction contract](/AiBook/en/reference/concept-glossary-alpha/p/#glossary-prediction-contract) specifies the prediction subject, when and how inputs are constructed, and the outcome to predict. Check when each value became usable, not just its column name.

## Use the 10:00 Inputs to Predict the Next Seven Days

This fictional equipment example illustrates time boundaries. One prediction concerns `equipment_id=M-01` at `2026-09-01 10:00`; all times use Korea Standard Time (KST). Different prediction times for the same equipment identify different samples.

| Item | Definition in this example |
| --- | --- |
| Input cutoff `cutoff_at` | 2026-09-01 10:00. Use only information the system could actually read by this time |
| Prediction horizon `horizon_days` | 7 days |
| Outcome window | At or after 2026-09-01 10:00, before 2026-09-08 10:00. Start included, end excluded |
| Target `failure_within_7d` | 1 if an equipment failure is confirmed in this window; 0 if the full window is checked and no failure occurred |
| Unconfirmed outcome | Keep unknown. Do not fill unreviewed or incompletely observed outcomes with 0 |

Here, failure means that the equipment could not complete a scheduled operation because of an equipment fault whose cause was confirmed in a maintenance record. Exclude planned stops and record this definition as `failure-v1`. Values and IDs below are illustrative, not estimates of actual equipment risk.

## An Earlier Measurement Can Arrive Too Late

A [feature](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature) is an input value supplied to a model. Here, `recent_diff` subtracts baseline mean flow from recent mean flow under the same measurement conditions. A recent mean of 2.20 L/min and baseline of 2.52 L/min give `2.20 − 2.52 = −0.32 L/min`.

| Information or calculation | Occurrence or covered time | Actual availability | Input decision for September 1 at 10:00 |
| --- | --- | --- | --- |
| `base-v1` baseline, 2.52 | Finalized records through August 31, 17:00 | August 31, 18:00 | Usable. Preserve the finalized records and calculation version |
| Recent mean 2.20 and `recent_diff=-0.32` | Operations completed by September 1, 09:55 | September 1, 09:58 | Usable. Assume source records had arrived and been checked by then |
| Additional sensor measurement | Measured September 1, 09:59 | Arrived September 1, 10:02 | Exclude. It occurred earlier but arrived after cutoff |
| Later recalculation of `recent_diff` | Baseline includes records through September 2, 17:00 | September 2, 18:00 | Exclude. Future records enter the calculation |
| `review_result` | Review completed September 1, 10:20 | Recorded September 1, 10:21 | Exclude. Judgment arose after prediction |
| `failure_within_7d=1` | Failure September 3, 14:00, confirmed through maintenance | Entered in the outcome table September 8, 10:10 in this example | Join as a training outcome; exclude from September 1 inputs |

`feature_available_at` is when the feature value became usable by the system. Required calculations must be complete as well as source records received. The value finalized on September 1 and a value recalculated using September 2 records differ even if both are called `recent_diff`. Giving a later table an earlier date does not make its values historical inputs.

## Putting Later Outcomes into Inputs Gives Away the Answer

Using information unavailable at prediction time to construct a model is [data leakage](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-data-leakage). Joining a subsequently confirmed outcome as the training answer is necessary, but also placing that value in the same sample's inputs supplies future information.

| Separate teaching sample | `failure_within_7d` confirmed after the window | `result_code` copied from that outcome | Answer obtained by copying `result_code` |
| --- | ---: | ---: | ---: |
| E | 1 | 1 | 1 |
| F | 0 | 0 | 0 |

Copying the answers gets `2 / 2 = 100%` correct on these two rows. This does not test a model's ability to predict future outcomes. The example illustrates leakage; it does not mean leakage always raises scores by this amount. Check input availability regardless of whether a score is high or low.

Nor does `review_result=skipped` mean no failure or normal operation. It is a processing status indicating that review was skipped. A task requiring later failure outcomes needs separate observation and confirmation records.

## Separating Available Inputs from Later Outcomes at Prediction Time {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-7-mermaid-01-en.mmd"
```

Arrows show chronological order and record links, not elapsed time to scale. Although the 09:59 measurement precedes the 10:00 cutoff, its 10:02 arrival prevents inclusion in those inputs. When constructing a training table later, reconstruct the inputs available at cutoff and join the outcome as a separate column.

## Evidence to Hand Over with One Row to Part 4

| Handoff field | What to retain in this example |
| --- | --- |
| Sample identity | `equipment_id=M-01` + `cutoff_at=2026-09-01 10:00 KST` |
| Input and availability | `recent_diff=-0.32 L/min`, `feature_available_at=2026-09-01 09:58 KST` |
| Calculation evidence | Recent mean 2.20, `base-v1` mean 2.52, source record IDs, covered period, aggregation rule |
| Outcome boundaries | `target_window_start=2026-09-01 10:00 KST`, `target_window_end=2026-09-08 10:00 KST`, `horizon_days=7`, start included and end excluded |
| Outcome and evidence | `failure-v1`, `failure_within_7d=1`, failure and maintenance record IDs, outcome-table entry September 8 at 10:10 |
| `leakage_check_note` | Exclude the 10:02 arrival, recalculation with a future baseline, and post-review results from inputs |

An actual handoff must supply specific source, failure, and maintenance record IDs. This table identifies the kinds of records to link, so it is not itself real data ready for training. If there are multiple features, check availability separately for each one.

Exercise: ① If the 09:59 measurement arrived earlier, at 09:59:30, could it enter the mean? ② Could a value recalculated with the September 2 baseline overwrite the September 1 row? ③ Could an unreviewed status become outcome 0?

Answer: ① Earlier arrival does not automatically qualify it. This example averages operations completed by 09:55, so first check whether the measurement belongs to that aggregation scope. Changing the input definition requires source checks and feature calculations to finish before 10:00, with the same rule reproducible in operation. ② No: future information enters the calculation. Preserve the historical baseline and input versions. ③ No: unreviewed means the outcome remains unconfirmed, not 0.

These time boundaries apply to both feature vectors and inputs that retain a sequence. Send Part 4 the input values, outcomes, and evidence needed to reconstruct those historical inputs. Training and evaluation splits connect to the handoff items in [P3-9.13](section-13.en.md).

## Checklist

- Can you specify the start, end, and endpoint inclusion of the seven days, separating input timing from outcome observation?
- Can you explain why the 09:59 measurement arriving at 10:02, future-baseline recalculations, and post-review results are excluded from inputs?
- Can you reproduce inputs using historical records and versions, and distinguish unreviewed status from outcome 0?

## Sources and References

- Google, *Machine Learning Glossary*, `feature`, `label`, `label leakage`. Used to check the term basis that features are model input variables and that label leakage is a design flaw in which a label proxy is mixed into the features. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Datasets: Dividing the original dataset*. Used to check the view that train/validation/test data should be separated, the same feature transformation should also apply to real-world data, and validation/test data should match the real-world data the model will encounter. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for preserving processing steps, reproducibility, versioning, and derivation. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20

- [scikit-learn, Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }. Used to check leakage of unavailable information and consistent input transformations in training and production. Accessed: 2026-09-20.
