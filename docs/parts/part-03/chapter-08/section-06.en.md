# P3-8.6 Confirmed Labels Available for Only Some Cases

> Section ID: `P3-8.6`
> Version: `v2026.09.20`

When people examine only selected events from a review queue, confirmed outcomes may exist only for those events. **Unreviewed does not mean non-failure.** [Selective labels](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-selective-labels) arise when which cases receive outcome confirmation determines the scope of observed labels. Even accurate labels raise a separate question: does the labeled set represent all events?

## Which four of the ten events were reviewed?

The following ten events are fictional. `review_score` is an illustrative selection score, not a failure probability. Assume review was completed only for events with `review_score ≥ 0.75`. `fixed_prediction` is a fictional binary prediction held constant when review coverage changes. It was neither calculated from the score nor produced by training a model on this table. One predicts failure; zero predicts non-failure.

`confirmed_failure` records the review outcome: 1 means confirmed failure, 0 confirmed non-failure, and `?` unknown. Assume completed review yields an accurate label, separating label error from selection. Confirming failure does not establish a particular root cause.

| event_id | review_score | fixed_prediction | confirmed_failure |
| --- | ---: | ---: | --- |
| A | 0.92 | 1 | 1 |
| B | 0.88 | 1 | 1 |
| C | 0.81 | 0 | 0 |
| D | 0.76 | 1 | 1 |
| E | 0.69 | 1 | ? |
| F | 0.62 | 1 | ? |
| G | 0.55 | 1 | ? |
| H | 0.48 | 1 | ? |
| I | 0.37 | 1 | ? |
| J | 0.29 | 1 | ? |

Only A–D have labels; E–J are unknown. Label coverage is **labeled events/all events**, hence `4/10=40%`. The reviewed-set failure proportion is **confirmed failures/reviewed events**, or `3/4=75%`. Their denominators and questions differ. Do not report 75% as the failure proportion of all events.

## Separating Reviewed Cases from the Full Evaluation Population {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-6-mermaid-01-en.mmd"
```

Accuracy divides predictions matching confirmed outcomes by the number evaluated. All four predictions for A–D match, so **reviewed-set accuracy is `4/4=100%`**. There is no training step here, so this is not a training-set reevaluation score. It nevertheless does not demonstrate performance on new events or the unreviewed set. It describes four selected high-score events.

Overall accuracy also requires knowing whether predictions for E–J were correct. Replacing `?` with zero invents non-failure outcomes where results are unknown. Knowing that four predictions matched does not determine a single accuracy value for all ten events.

## Reveal hidden outcomes for teaching only

Solely to calculate the difference between the selected set and the full set, assume the following six **hidden teaching outcomes**. These are not automatically available in real operations; further review or suitable follow-up outcome confirmation would be needed.

| event_id | actual_failure_for_demo | fixed_prediction | Prediction match |
| --- | ---: | ---: | --- |
| E | 1 | 1 | match |
| F | 0 | 1 | mismatch |
| G | 1 | 1 | match |
| H | 0 | 1 | mismatch |
| I | 1 | 1 | match |
| J | 0 | 1 | mismatch |

Revealing these outcomes shows three failures, E, G, and I, and three matching predictions among the six unreviewed events. The full-set failure proportion is `(3+3)/10=60%`; full-demo accuracy is `(4+3)/10=70%`. The former describes outcome composition; the latter describes prediction agreement. They are not interchangeable.

| Metric | Numerator/denominator | Calculable from current review records alone? |
| --- | --- | --- |
| Label coverage | 4/10=40% | Yes |
| Reviewed-set failure proportion | 3/4=75% | Yes |
| Full-demo failure proportion | 6/10=60% | No; requires hidden outcomes |
| Reviewed-set accuracy | 4/4=100% | Yes, restricted to the reviewed set |
| Full-demo accuracy | 7/10=70% | No; requires hidden outcomes |

The 100% and 70% values evaluate the same fixed predictions on different sets. All three errors, F, H, and J, were initially unreviewed, but selective review does not always inflate accuracy. This example shows why reviewed-set accuracy cannot simply be generalized to overall performance.

## Record coverage and the outcome-confirmation pathway

Report: “Of ten events, four scoring at least 0.75 were reviewed, giving 40% label coverage. Reviewed-set accuracy was 100%. Outcomes for the other six are unavailable, so overall accuracy is unknown.” Preserve the review policy, actual completion status, label definition, confirmation time, and source. A review request alone does not establish a confirmed label.

For additional checking, consider randomly sampling cases from lower-score ranges or sampling within score bands. Record selection rules, selection probabilities, and incomplete reviews, and use the same label definition and outcome-confirmation period. A few additional labels do not automatically establish representativeness; overall estimates must account for the sampling design.

## Calculate it yourself

Assuming the hidden teaching outcomes are available, change the review threshold to `review_score ≥ 0.60` and complete review for all qualifying events. Keep predictions fixed. What are label coverage, reviewed-set failure proportion, and reviewed-set accuracy?

Explanation: E and F join the set, so A–F are reviewed. Coverage is `6/10=60%`; the failure proportion is `4/6≈66.7%` for A, B, D, and E; accuracy is `5/6≈83.3%` because only F is wrong. Full-demo accuracy remains `7/10=70%` because predictions and outcomes did not change. The reviewed-set accuracy change is not a retraining effect. Without actually confirming E and F's outcomes, these new exercise values cannot be calculated.

## Checklist

- Can you identify the numerator and denominator of coverage, failure proportion, and accuracy?
- Can you leave unknown outcomes unknown and identify metrics unavailable from current records?
- Can you distinguish changing the evaluation set for fixed predictions from a training effect and suggest a way to confirm additional outcomes?

## Sources and references

- [Lakkaraju et al., The Selective Labels Problem, KDD 2017](https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres){: target="_blank" rel="noopener noreferrer" } — The official conference abstract describes how selective outcome observation can distort evaluation. Events, fixed predictions, and hidden outcomes here are our fictional teaching example, not the paper's experimental results. Accessed: 2026-09-20.
