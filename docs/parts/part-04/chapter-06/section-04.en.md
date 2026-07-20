# P4-6.4 Supplementary Learning: How To Read ROC, PR, Log Loss, Calibration, And Silhouette For The First Time

> Section ID: `P4-6.4`
> Version: `v2026.07.20`

P4-6.1 and P4-6.2 fixed the role of evaluation metrics and the differences by problem type. But once you start reading actual papers or library documentation, more unfamiliar names appear very quickly.

- ROC curve
- PR curve
- log loss
- calibration
- silhouette score

The purpose of this supplementary learning is not to calculate formulas at length. It is to connect `what question each of these metrics appeared to answer`.

## Scope Of This Supplementary Learning

This Section is a first supplementary reading of ROC, PR, log loss, calibration, and silhouette, which appear often in classification and clustering. The focus is not on proof details but on `when and why they get inspected`.

- Why do ROC and PR curves lead into the problem of score and threshold?
- Why does log loss make people inspect probability output as well as right and wrong?
- Why does calibration make people doubt again `a score that looks like a probability`?
- Why does silhouette make people read structure even without answer labels in clustering?

This Section first closes the question of why names such as ROC, PR, log loss, calibration, and silhouette appear separately while reading evaluation metrics. ROC/PR and calibration return in P4-15.3, and the connection between reading cluster structure and silhouette continues in P4-17.1 and P4-17.2.

## Goals Of This Supplementary Learning

- You can explain that ROC and PR curves are tools for reading classification performance while changing the threshold.
- You can explain that log loss is a metric that also reads the confidence of probability output.
- You can explain calibration as the degree of match between scores and actual frequencies.
- You can explain silhouette score as an internal criterion that reads both compactness within a cluster and separation across clusters.

## First Fix The Big Map

These five names are actually answering different questions.

| Item | The first question to read |
| --- | --- |
| ROC curve | What changes when the criterion for separating positive and negative changes? |
| PR curve | How does the precision-recall balance change when positives are rare? |
| log loss | Not only whether it was right or wrong, but how overconfident was it? |
| calibration | Does a score like `0.8` really mean about an 80% frequency in reality? |
| silhouette | Even without answer labels, are the groups compact and separated? |

In other words, these metrics appear `when accuracy alone is not enough`.

The role of this Section can be stated even more briefly as `a place to stop by for a moment when a finer criterion for reading scores is needed while reading the main evaluation questions`.

| Question where the reader gets stuck | What to inspect first in this supplementary Section | Main text place to return to |
| --- | --- | --- |
| I understand classification scores, but what changes if the threshold moves? | ROC, PR | P4-6.2, P4-15.3 |
| Accuracy looks fine, but can the probability score itself be trusted? | log loss, calibration | P4-6.2, P4-15.3 |
| A clustering result exists, but can structure be read without answer labels? | silhouette | P4-17.1, P4-17.2 |

Supplementary metrics are brought in based on `is the current question fully handled by the main metrics, or is a more detailed reading frame needed?`

| Current question | What to inspect first in this Section | Why |
| --- | --- | --- |
| How does the FP/FN balance change if the threshold changes? | ROC, PR | because classification score and threshold change move together |
| Can the confidence of a probability score itself be trusted? | log loss, calibration | because right and wrong alone do not fully show probability interpretation |
| Does the cluster structure look plausible without labels? | silhouette | because a separate criterion is needed to read internal structure |

So this Section is not a new evaluation chapter that replaces the main text. It is a detour Section for reading more finely the `problem-type questions` already established in the main text. After the names and questions are connected here, the most natural flow is to return to the main text's scenes of classification, clustering, and threshold adjustment.

When reading these for the first time, it helps to catch not only `what this metric can tell` but also `what it cannot tell by itself`.

| Name | What it mainly tells | What it still cannot fully say by itself |
| --- | --- | --- |
| ROC | the full picture of separation ability | which threshold should actually be chosen in operation |
| PR | how positive-decision quality changes | whether the score itself can be trusted like a probability |
| log loss | whether probability output is overconfident | whether a high score matches the actual frequency |
| calibration | the trustworthiness of score interpretation | whether the model separates positives and negatives well |
| silhouette | the internal quality of cluster structure | whether that cluster is useful in actual work interpretation |

If this table is fixed first, it becomes less confusing later why similar-looking names remain separate.

## ROC And PR Curves Reveal The Threshold Problem

P4-6.2 explained that classification is not only about matching a category, but also about how a score is turned into a decision. ROC and PR curves are exactly what make that point readable.

ROC and PR curves show that when the threshold for treating a model's score as positive changes, the balance between false alarms and misses changes with it.

An ROC curve shows this balance through false positive rate and true positive rate. A PR curve shows it through precision and recall.

The reason they are read separately is the following.

| Tool | Scene where it is especially useful |
| --- | --- |
| ROC curve | when you want to see overall separation ability |
| PR curve | when positives are rare and the precision-recall balance is important |

For example, in problems such as fraud detection, disease screening, and anomaly-transaction detection, where the positive ratio is low, a PR curve often feels more intuitive.

What beginners often miss here is that the phrase `the curve looks good` still does not finish the decision rule. ROC and PR show `how well the model separates scores`, but in an actual service, a threshold still has to be chosen for block, review, or pass. In other words, the curve is not an answer that replaces decision making. It is closer to a map that makes people debate where to cut.

When reading the two curves, it becomes less confusing if the questions are ordered like this.

| Question to inspect first | Reading intuition on the ROC side | Reading intuition on the PR side |
| --- | --- | --- |
| Does the model have the overall strength to separate positives from negatives? | inspect the overall balance of TPR and FPR | it does not answer that directly, but recall change can still be seen |
| Is the quality of positive decisions maintained in a reality where positives are rare? | intuition can weaken in class-imbalance scenes | it becomes more direct because precision is shown together |
| If the threshold is lowered a little, what shakes first? | inspect how quickly FPR grows | inspect how much precision falls when recall rises |

So ROC often shows `the full picture of separation ability`, while PR often shows `the cost structure of positive decisions` more directly.

#### Connecting ROC And PR To Actual Decisions

Even with the same model, the operational result changes greatly depending on where the threshold is set.

1. If the threshold is raised, positive decisions usually become more cautious, so FP can shrink.
2. But that can increase FN by missing more actual positives.
3. If the threshold is lowered, recall may improve, but precision can deteriorate sharply.

Because of this flow, ROC and PR must be read not only with `is the model score decent?` but also with `what kind of mistake is the work less able to tolerate?` For spam blocking, a threshold that does not make normal-mail errors too large may matter. For disease screening, a threshold that misses fewer risky cases may matter more.

It becomes more intuitive with a small numerical scene.

| Threshold change | precision | recall | Reading intuition |
| --- | --- | --- | --- |
| 0.80 | 0.94 | 0.41 | alarms are very cautious, but there are many misses |
| 0.50 | 0.82 | 0.73 | this may be a relatively balanced point |
| 0.20 | 0.48 | 0.93 | it catches almost everything, but the false-alarm burden grows |

This table shows that ROC and PR are not tools that simply say `good or bad`. They are tools that help read `which threshold fits better under which cost structure`.

#### Questions ROC And PR Do Not Answer

Even though ROC and PR are useful, they cannot solve the following questions by themselves.

- Can a score of `0.82` really be read as an 82% risk?
- Does a group of high-score cases actually contain risk at the same frequency?
- After the threshold is changed, how much do human-review staff load, customer complaints, and operating cost increase?

So ROC and PR help begin a decision-boundary discussion, but they do not finish the trustworthiness of score interpretation.

## Log Loss Reads Even The Confidence Of Probability Output

Accuracy first inspects whether the result was right or wrong. But one model may `barely be right with weak confidence`, while another may `be wrong but far too confident`.

Log loss appears in order to read that difference.

Log loss treats a wrong answer as a problem, but it penalizes the case even more strongly when the model gave the wrong answer with very high probability.

In other words, log loss makes people read classification as `evaluation that includes probability output`.

That is why log loss connects well to the following questions.

- Is this model acceptable if we inspect only right and wrong?
- Or should the confidence of the score be inspected too?

The reason this metric is needed is that even `answers that were both correct` can have different quality. For example, even if two models both got the answer right, one may have given the correct class 0.51 and the other 0.95. Their usefulness can differ later for threshold adjustment, ranking, and follow-up decisions.

There is also a more dangerous scene.

| Situation | If you look only at accuracy | What log loss reads more sensitively |
| --- | --- | --- |
| It barely gets the right answer with 0.51 | it is counted as a correct prediction | it does not give a high score because the confidence is weak |
| It gives the wrong answer with 0.55 | it is counted as a wrong prediction | it sees that the model was wrong, but not severely overconfident |
| It gives the wrong answer with 0.99 | it is also counted as a wrong prediction | it heavily penalizes this as dangerous overconfidence |

So log loss is a metric that asks not only `was it wrong?` but also `how dangerously was it wrong?`

#### When Should Log Loss Come To Mind Earlier?

- When prediction probabilities will be used directly for ranking, prioritization, or automatic approval rules
- When threshold adjustment is likely later, so the quality of the score itself matters
- When models have the same accuracy, but you need to separate which one gives more trustworthy scores

In these scenes, accuracy and F1 are often not enough, and the shape of the probability output has to be read more delicately.

If one more simple contrast is added, the intention becomes clearer.

| Model | accuracy | Example probabilities for the correct class | Reading intuition |
| --- | --- | --- | --- |
| Model A | 0.90 | it barely gets cases right with values such as 0.51, 0.54, 0.58 | it gets them right, but confidence is weak |
| Model B | 0.90 | it gets them clearly right with values such as 0.88, 0.91, 0.95 | even with the same accuracy, the score is easier to use in later decisions |

So log loss helps separate `which model gives more trustworthy scores even under the same accuracy`.

But log loss is still not enough alone. Even when log loss is low, it cannot immediately justify the claim `if the score is 0.8, it is really about 80% in reality`. That question has to be checked again through calibration.

## Calibration Checks Whether Score And Actual Frequency Match

Just because a model says `0.82` does not mean that this score exactly matches an 82% frequency in the real world. Calibration is the perspective that reads this gap.

Calibration asks whether, when cases with similar scores are grouped together, that score roughly matches the actual frequency of occurrence.

For example, if among 100 cases with scores near `0.8`, about 80 are actually positive, calibration can be read as fairly well matched. But if only 40 are positive, score interpretation should be treated more carefully.

This perspective matters especially in the following scenes.

- services that use risk scores as priorities
- scenes where probability interpretation directly connects to decision making
- scenes where the size of the score itself must be trusted when a threshold is chosen

Because threshold adjustment and calibration return again in P4-15.3, this Section first connects the perspective that `even scores that look like probabilities must be examined again`.

What beginners especially confuse is that `classifying well` and `speaking probabilities well` are not the same ability. A model may rank positives and negatives reasonably well, while the score value itself still deviates from actual frequency. In other words, ranking can be acceptable while probability interpretation is poor.

The distinction becomes clearer like this.

| Question | The closer tool |
| --- | --- |
| Can the model rank who is more risky? | separation perspectives such as ROC and PR |
| Can a number like `0.8` really be read like 80%? | the calibration perspective |

For example, if only cases with risk scores above 0.8 will be reviewed by humans, operators want to know not only `is the rough ranking of risk correct?` but also `is the group above 0.8 really a high-risk group in actual frequency?` At that point, calibration connects directly to threshold policy, staffing, and customer explainability.

#### Do Not Misunderstand Calibration Too Lightly

Good calibration does not automatically mean that classification performance is good. By contrast, good classification performance does not guarantee that calibration is also good.

1. A model may separate well, yet still exaggerate probability interpretation.
2. A model may give plausible-looking probabilities, yet have weak separation ability.
3. So in practice, `does it separate well?` and `is its score interpretation correct?` must be inspected separately.

With a short contrasting scene, it can be read like this.

| Score range | Probability claimed by the model | Actual positive ratio | Calibration reading |
| --- | --- | --- | --- |
| group of cases near 0.8 | about 80% | about 78% | a relatively good match |
| group of cases near 0.8 | about 80% | about 43% | the score is overconfident |

This difference is not a small numerical error. It can shake decisions such as how many items should be sent to human review, how a risk score should be explained to customers, and where the threshold should be set.

By contrast, even if calibration looks good, that is not the end. Score interpretation can fit well while the actual ability to separate positives from negatives remains weak. So calibration is a tool for reading `the trustworthiness of probabilistic wording`, not an all-purpose score that represents the whole classification problem.

## Silhouette Is An Internal Criterion For Reading Cluster Structure Without Answers

P4-6.2 explained that in clustering there may be no answer labels. Silhouette score is an internal evaluation criterion that appears often in that kind of scene.

Silhouette score is a criterion that reads the grouping as better when points are closer within the same cluster and farther from other clusters.

Silhouette can be read through the feeling of comparing `closeness to my own cluster` and `distance to the nearest other cluster`.

So silhouette helps the following questions.

- Is the current grouping too mixed together?
- When the number of clusters changes, does the structure improve?

Because cluster-result interpretation and cluster-quality metrics return in P4-17.1 and P4-17.2, this Section first fixes the point that silhouette is `an internal criterion for reading structure even without answers`.

When reading silhouette, it is often better to set aside for a moment the habit of reading classification metrics. Here the first question is not `how many correct answers were matched?` but `does the grouping itself look natural?`

The following question order helps.

| Question | Why silhouette helps |
| --- | --- |
| Are samples inside the same cluster not too far from each other? | it reflects compactness within a cluster |
| Is the nearest other cluster sufficiently far away? | it reflects separation between clusters |
| If the number of clusters grows or shrinks, does the structure improve? | it can be used as an internal structure-comparison criterion |

But silhouette is not magic either. Even when the value is high, that does not guarantee the cluster is useful in actual work interpretation. For example, three purchase-pattern groups may be separated very cleanly, but it is still hard to call them `good clusters` if the grouping does not connect to marketing strategy or operational policy.

So silhouette helps first with `is this a mathematically neat grouping?` but it does not answer by itself `is this a grouping that is useful in work?`

It also helps to remember a short comparison scene.

| Cluster result | Silhouette reading | The next question that follows immediately |
| --- | --- | --- |
| inside clusters are compact and well separated | the structure looks plausible | can a name be attached to this grouping? |
| clusters overlap heavily | the structure looks unstable | is the number of clusters or the feature composition wrong? |
| the value is high but interpretation is vague | the mathematical separation is acceptable | is this a grouping criterion that is useful in work? |

Because of this, silhouette is usually a good `first internal inspection tool`, but it does not become the final owner of interpretation. In the end, clustering only reaches actual use when people can read `what name can be attached to this grouping?`

## Even Inside The Same Problem, The Questions Split Apart

Even when looking only at one classification problem such as fraud detection, the questions split into several branches like this.

| Detailed question inside the same problem | Name to bring up first | Why |
| --- | --- | --- |
| What changes if the blocking threshold is lowered from 0.7 to 0.5? | ROC, PR | because the FP/FN balance and the precision-recall balance move together |
| If accuracy is the same, which model makes more dangerously confident mistakes? | log loss | because we want to inspect overconfident wrong answers more heavily |
| Can a risk score of 0.8 be used directly in policy? | calibration | because the match between score and actual frequency must be checked |
| Do groups of customer types really form a structure? | silhouette | because unlabeled internal structure must be read first |

So the statement `one problem has many metrics` does not mean the problem became unnecessarily complicated. It means that several layers of judgment exist even inside one problem.

## Grouping The Five Metrics Again By Different Levels

If the discussion so far is compressed one more time, the five names are not the same kind of metric.

| Metric | The closer level | Core question |
| --- | --- | --- |
| ROC, PR | classification score and threshold adjustment | where should the score be cut into a decision? |
| log loss | quality of probability output | when the model was wrong, how dangerously confident was it? |
| calibration | trustworthiness of score interpretation | how much can a number such as `0.8` be trusted? |
| silhouette | internal quality of cluster structure | does the grouping look plausible even without answers? |

So ROC and PR appear `when the decision boundary moves`, log loss appears `when the confidence of probabilities is being judged`, calibration appears `when probability interpretation itself must be trusted`, and silhouette appears `when unlabeled structure is being read`.

Once these levels are not mixed up, even within the same classification problem the questions can be separated and read one by one.

| Question inside the same fraud-detection problem | Tool to bring up first |
| --- | --- |
| Where should the score be cut as a blocking criterion? | ROC, PR |
| Is the model too confident when it is wrong? | log loss |
| Can a `risk score of 0.8` really be read like 80%? | calibration |
| Do risky-customer groups really form a structure? | silhouette |

## You Do Not Need To Memorize These Five Names All At Once

What matters is not memorizing the metric names but connecting them to questions.

| Question | Connected name |
| --- | --- |
| What changes when the threshold changes? | ROC, PR |
| Is the probability output too overconfident? | log loss |
| Does the score match the actual frequency? | calibration |
| Without answer labels, does the grouping structure still look plausible? | silhouette |

In other words, all of these are tools brought out `when accuracy alone is not enough`.

## Cases And Examples

### Case 1. Fraud-Detection Scores Look High, But Actual Operational Judgment Still Shakes

A payment system is assigning a fraud-risk score to each transaction. The criteria people first used were signals such as `is it an overseas payment`, `is it at an unusual hour`, and `were there many attempts in a short period of time`.

When the discussion moves from comparing models by accuracy and recall into actual operations, a more complicated problem appears. One model may look as if it separates positives and negatives well, but a small threshold change can sharply increase false alarms. Another model may output many probability scores such as `0.8`, but those cases may not actually be that risky. If customers are grouped by cluster, people may also want to inspect separately whether risky transactions gather into one kind of group.

At that point, ROC and PR make it possible to read what changes when the threshold changes, log loss makes it possible to read how excessively the model was confident when it was wrong, calibration makes it possible to check how much the score itself can be trusted, and silhouette appears when unlabeled customer-group structure is being read.

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-4-mermaid-01-en.mmd"
```

The checkable result also differs by question. Precision and recall must be inspected separately when the threshold changes, the match between high-risk score groups and actual fraud ratio must be checked, and the internal similarity of transactions inside a cluster must be examined separately. So these names should be read not as `new terms`, but as tools that answer `more specific questions`.

## Checklist

- Can you explain when ROC and PR should be brought in after the main text's accuracy, precision, and recall?
- Can you explain why log loss and calibration make people doubt again `a score that looks like a probability`?
- Can you explain what internal question silhouette answers in clustering?
- Can you explain that evaluation metrics increase not because the model became more complicated, but because the questions we ask became more specific?
- Can you explain that ROC and PR read classification balance when the threshold changes, log loss reads the confidence of probability output, and calibration reads the match between score and actual frequency?
- Can you explain that `there are many metrics` connects to the point that `the meaning of a good result is not just one thing`?

## Sources And References

- scikit-learn developers, [Metrics and scoring: quantifying the quality of predictions](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-29.
- scikit-learn developers, [Probability calibration](https://scikit-learn.org/stable/modules/calibration.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-29.
- scikit-learn developers, [Clustering performance evaluation](https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-29.
