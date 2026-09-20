# P3-9.8 Which Rules Turn Prediction Scores into Actions

> Section ID: `P3-9.8`
> Version: `v2026.09.20`

[P3-9.7](section-07.en.md) distinguished inputs available at prediction time from later outcomes. After a model produces a [score](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-score), we still need to decide whom to review. The score is a model output; a [policy rule](/AiBook/en/reference/concept-glossary-alpha/b/#decision) specifies how that output becomes an action.

## State the Score's Source and the Unit of Prediction

The values below are **hypothetical model outputs supplied for this section**. They are not results of training or running a model, nor are they the manually defined queues sorted by comparison differences or safety conditions in earlier chapters. Assume this model predicts whether one completed operation needs additional review. `review_score` is its score for that judgment; higher values receive earlier consideration for review.

A–D are operation IDs local to this section. Assume the same hypothetical model, `demo-model-v1`, scored each operation at completion, and D joins before this review batch is finalized. A–C are not rescored. The action unit is also fixed: assigning one operation for review.

| event_id | Supplied `review_score` | Entry into the candidate batch |
| --- | ---: | --- |
| A | 0.82 | Initial batch |
| B | 0.80 | Initial batch |
| C | 0.79 | Initial batch |
| D | 0.95 | Added before assignments are finalized |

A score between 0 and 1 is not automatically a probability of failure or of needing review. This section uses score order and applies policies. Actual review outcomes have not been supplied, so selected operations must not become actual positives, nor unselected operations confirmed normal cases.

## A Threshold and the Top Two Are Different Rules

Today's capacity is two reviews. First compare threshold eligibility before imposing capacity with selection by rank. Here, **“at least 0.80” means `score >= 0.80`**, including exactly 0.80. Break ties by `event_id` in ascending alphabetical order. These are rules of this teaching policy, not defaults shared by every tool.

| Policy being compared | A, B, and C only | After D joins |
| --- | --- | --- |
| Threshold: all candidates scoring at least 0.80 | A, B — 2 candidates | D, A, B — 3 candidates |
| Top two: descending score, then ascending ID | A, B — 2 candidates | D, A — 2 candidates |

The threshold row lists eligible candidates, not finalized assignments for today's two slots. D's arrival changes neither B's score nor its eligibility. B's position among candidates changes. Conversely, a top-two-only rule has no minimum score and can select up to two candidates even if all their scores are low.

## Separate Eligibility from Today's Assignment Status

Call the combined policy `threshold-capacity-v1`. First keep candidates with scores of at least 0.80. Within that set, assign up to two for review today in descending score order, breaking ties by ascending ID. Do not fill spare slots with candidates below the threshold.

| event_id | Score | `meets_threshold` | `selected_today` | Assignment status determined by policy |
| --- | ---: | ---: | ---: | --- |
| D | 0.95 | 1 | 1 | Assigned for review today |
| A | 0.82 | 1 | 1 | Assigned for review today |
| B | 0.80 | 1 | 0 | Eligible; waiting because of capacity |
| C | 0.79 | 0 | 0 | Below threshold; excluded from this assignment |

Both B and C have `selected_today=0`, for different reasons. B waits because of capacity; C does not meet the current threshold. Neither status is a review outcome or evidence of failure or its absence. Likewise, `selected_today=1` means assigned for review, not that a reviewer has finished the work. Check separate completion records for execution.

## From Scores to Thresholds and Operational Policies {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-8-mermaid-01-en.mmd"
```

The diagram applies `threshold-capacity-v1` to the batch including D. To reproduce assignments for the same batch and policy, retain the model version, prediction subjects and times, scores, candidate roster, threshold, capacity, tie rule, and policy version. Keeping B's 0.80 together with its waiting reason distinguishes model output from the assignment decision.

## Change the Boundary and Capacity

Exercise: Keep the four candidates including D fixed. ① What happens to B and C if only capacity rises to three? ② With capacity two, if the threshold rises to 0.83, should A fill the spare slot? ③ In a separate case, add E with 0.82 and use threshold 0.80 and capacity two: who is assigned?

Answer: ① D, A, and B are assigned; C remains below threshold. ② Only D qualifies, so assign just one candidate. Do not fill the spare slot with A. B's reason for nonselection also changes from capacity waiting to being below threshold. ③ After D, A and E tie, but ascending ID puts A first, so assign D and A. E and B are eligible but waiting. The ID rule makes ordering reproducible; it is not evidence that A is riskier than E.

The existing candidates' model scores remain fixed throughout these policy changes. Changed selections under a new threshold or capacity do not establish improved model accuracy. [P3-9.12](section-12.en.md) continues with the costs of decision errors.

## Checklist

- Can you explain the hypothetical scores' source and the units of prediction and action?
- Can you distinguish why B's 0.80 qualifies from why B waits after D joins?
- Can you apply the tie, spare-slot, and below-threshold rules, and distinguish review assignment from completion?

## Sources and References

- Google, *Thresholds and the confusion matrix*. Used to check that a classification threshold is chosen to convert a model's raw numerical output into a category, and that different thresholds can produce different predictions. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-20
- Google, *Classification: ROC and AUC*. Used to check that AUC is tied to ranking positive examples above negative examples, while the actual classification depends on the chosen threshold. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Machine Learning Glossary*, `classification threshold`, `AUC`. Used to check the term basis for classification threshold and AUC. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
