# P3-9.13 Problem Boundaries to Hand Off to Part 4

> Section ID: `P3-9.13`
> Version: `v2026.09.20`

Part 4 needs more than an input table. Hand over what is predicted and when, where performance should be tested, and which conditions remain unverified. [Evaluation design](/AiBook/en/reference/concept-glossary-alpha/e/#evaluation-design) divides learning and evaluation data and compares outcomes in line with that question.

## A Handoff Memo for Future Failures of Existing Equipment

The following **teaching draft** continues the equipment example in [P3-9.7](section-07.en.md). It does not imply that real source records or training and evaluation results are ready. Fix the question as “Can we predict failures over the next seven days for equipment already observed?”

| Handoff item | Decision for this example |
| --- | --- |
| Purpose and evaluation subjects | Predict future failures of existing equipment; claims about unseen equipment require separate evaluation |
| One sample | Pair of `equipment_id` and `cutoff_at`; different prediction times for one unit produce different rows |
| Example prediction time | M-01 at `2026-09-01 10:00 KST` |
| Example inputs | Recent mean 2.20 L/min from operations completed by 09:55, finalized historical `base-v1` mean 2.52 L/min, `recent_diff=-0.32 L/min`; this feature is available at 09:58 |
| Input evidence | Retain source IDs, arrival times, measurement conditions, aggregation scope, baseline version, and calculation completion; exclude the 10:02 arrival and later baseline recalculation |
| Outcome definition and window | `failure_within_7d`, `failure-v1`; from September 1 at 10:00 inclusive to September 8 at 10:00 exclusive |
| Label confirmation | 1 when a failure within the window is confirmed; 0 after complete follow-up and record checks establish no failure; retain unconfirmed status separately |
| Training-data cutoff | Freeze hypothetical training data at August 31, 18:00 KST; only rows whose inputs, answers, and version evidence were usable then are candidates |
| Evaluation data | Prediction rows starting September 1 at 10:00, after training-data freeze; join outcomes later, without using final evaluation answers beforehand for model or policy selection |
| Output and action | Failure score plus a separate review-assignment policy; a score alone establishes neither probability nor intervention effects |
| Baseline comparison | Compare with always predicting 0 on the same evaluation rows; high accuracy alone is insufficient when failures are rare |
| Still unverified | Actual availability times and baseline source records, equipment and failure counts, follow-up gaps, interventions, actual error costs and review capacity |

`failure-v1` means an equipment fault prevented completion of a scheduled operation, with its cause confirmed in maintenance records; planned stops are excluded. One illustrated row with numerical inputs is not sufficient training data. Resolve open items from real records rather than handing unsupported rows over as verified data.

## An Earlier Row May Still Have an Answer That Arrives Too Late

Consider two training candidates relative to the August 31, 18:00 freeze. All dates below are in 2026 KST; assume each input was available at its prediction time.

| Candidate prediction time | Seven-day window end, excluded | Outcome confirmation | Candidate for this training run? |
| --- | --- | --- | --- |
| August 20, 10:00 | August 27, 10:00 | 0 confirmed August 28, 12:00 after complete follow-up | Yes, subject to other quality checks |
| August 28, 10:00 | September 4, 10:00 | Still under observation with no confirmed failure at August 31, 18:00 | No; no confirmed answer was available then |

Adding the second row's September answer retrospectively would evaluate a model that could not have run on September 1. Collecting final evaluation outcomes after prediction, however, is normal. The distinction is when those outcomes are used for learning or policy selection. This is why confirmation status and times in [P3-9.10](section-10.en.md) matter.

Also inspect overlapping input windows. Check whether random row splitting puts near-duplicates sharing source records on both sides, and whether baseline or transformation calculations use future data. Reusing past observations for future predictions of existing equipment is not automatically leakage. Assess duplication and dependence against actual availability and the evaluation question.

## Evaluating Unseen Equipment Requires Different Boundaries

| Performance question | Time and entity separation |
| --- | --- |
| Future of existing equipment | The same equipment may appear in training and evaluation, but use past data to evaluate later predictions; this memo's choice |
| Equipment absent from training | Separate equipment IDs across training and evaluation; repeated rows from known equipment do not demonstrate unseen-equipment performance |
| New equipment arriving in the future | Apply both equipment-ID separation and chronological ordering |

Entity separation treats all related rows for a piece of equipment as a group. Removing its ID from inputs does not make those rows independent. When deployment predicts the future, time and input availability matter in unseen-equipment evaluation too. Start splitting from the intended use, not merely a fraction of stored rows.

## State What Metrics Count, Not Just Their Names

| Evaluation note | What to count and its limits |
| --- | --- |
| Fraction of failures flagged | Confirmed-failure samples assigned 1 / all confirmed-failure samples; measures how many misses are avoided and is undefined with zero failure samples |
| Unnecessary candidates and workload | Count actual-0 samples assigned 1 and total candidates separately; distinguish false-alarm burden from capacity |
| Policy cost comparison | Misses × miss cost + false alarms × false-alarm cost on the same evaluation rows; actual cost assumptions and capacity remain unresolved |
| Outcome-confirmation coverage | Report confirmed and unconfirmed counts out of all evaluation rows; results on the confirmed subset alone do not establish overall performance |

The counting unit is an equipment–prediction-time sample. Multiple prediction rows can refer to one real failure, so do not equate flagged samples with distinct failure events. Periods, equipment rosters, and policies must match when comparing a baseline and model.

If the purpose is to review only the top few cases today, redesign evaluation around ranks and selected candidates' outcomes. State categories can call for multiclass prediction; numerical outcomes can call for continuous-value prediction. Building a table does not automatically imply binary classification. This memo specifically chooses failure within seven days.

## Checking Time, Entity, and Information Boundaries Before Handoff {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-13-mermaid-01-en.mmd"
```

Exercise: M-01's August and September rows were separated chronologically for evaluation. ① Does this show that the model works well on equipment it has never seen? ② Can the unconfirmed answer for the August 28 row be filled with 0 and used for training?

Answer: ① No; evaluating the future of the same equipment provides insufficient evidence about unseen equipment. That goal requires evaluation subjects whose IDs do not overlap with training. ② No answer was available then, so exclude the row and preserve its pending status and exclusion reason. Part 4 will implement splitting, model selection, and tuning from this memo's question, constraints, and open items.

## Checklist

- Can you choose existing equipment's future or unseen equipment and explain the corresponding boundaries?
- Can you distinguish input cutoff, training-data freeze, outcome window, and confirmation time?
- Can you write a memo that states counting units, unconfirmed coverage, and records still to be checked?

## Sources and References

- Google, *Machine Learning Glossary*, `label leakage`. Used to check the information-boundary basis that information from after prediction time can become a label proxy inside the features. Accessed: 2026-07-20. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Classification: ROC and AUC*. Used to check the ranking/evaluation-design view that AUC and ROC relate to ranking positive examples above negative examples and are distinct from the chosen threshold. Accessed: 2026-07-20. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for recording processing steps, reproducibility, versioning, and derivation relationships. Accessed: 2026-07-20. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
- Hyndman, Athanasopoulos, *Forecasting: Principles and Practice (3rd ed.)*, Section 5.10 Time series cross-validation. Used as time-split evidence that, in time-ordered problems, each training set should contain only observations before the test observation and no future observations should be used to construct the forecast. Accessed: 2026-09-20. [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, *Cross-validation: evaluating estimator performance*, cross-validation iterators for grouped data. Used as group-split evidence that samples from the same group should not appear in both the paired training and validation/test sides when group dependence matters. Accessed: 2026-09-20. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" }
