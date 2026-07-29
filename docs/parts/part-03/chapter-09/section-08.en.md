# P3-9.8 What Does One Prediction Actually Decide, and Why Are Scores and Policy Different

> Section ID: `P3-9.8`
> Version: `v2026.07.25`

Even after inputs and results are defined, a prediction problem is still only half closed. Even the same `review_needed` prediction can mean different things depending on whether it raises one operating event into a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) or adjusts the warning strength of an entire recent window. In addition, the [score](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-score) output by a model and the [policy rule](/AiBook/en/reference/concept-glossary-alpha/b/#decision) that turns that score into real action are not the same thing.

One predicted value needs to be written together with the unit of action it connects to, and model scores need to be read separately from operating policy.

| Category | Question |
| --- | --- |
| Unit targeted by one prediction | Does this one value refer to one run, one recent window, or the next single case? |
| Model output | Does the model emit a score, a 0/1 value, or a ranking? |
| [Policy rule](/AiBook/en/reference/concept-glossary-alpha/b/#decision) | By what rule is that output turned into action? |
| [Real action](/AiBook/en/reference/concept-glossary-alpha/a/#action) | Does it register a review queue entry, hold back, or trigger automatic action? |

| Level | Example |
| --- | --- |
| Model output | `0.82`, `warning_score` |
| [Policy rule](/AiBook/en/reference/concept-glossary-alpha/b/#decision) | `review if above 0.8`, `look only at the top 10%` |
| Real action | Register in review queue, adjust priority |

Even with the same score, the action can change when the policy changes. Also, some problems use the score only for [ranking](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-ranking), while others want to read the number itself almost like a [probability estimate](/AiBook/en/reference/concept-glossary-alpha/p/#probability-estimate). That difference also needs to be written down first. The meaning of one prediction is therefore not just `producing one number`. It includes the decision structure by which that number goes through a rule and leads to an action. More broadly, this section separates `model output`, `decision rule`, and `real action` as different levels, so that one predicted value is read inside an operational decision structure.

## A Small Diagram

One prediction does not end with a score. It must be read all the way through the policy rule into the resulting action.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-8-mermaid-01-en.mmd"
```

## Sources and References

- Google, *Thresholds and the confusion matrix*. Used to check that a classification threshold is chosen to convert a model's raw numerical output into a category, and that different thresholds can produce different predictions. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Classification: ROC and AUC*. Used to check that AUC is tied to ranking positive examples above negative examples, while the actual classification depends on the chosen threshold. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Machine Learning Glossary*, `classification threshold`, `AUC`. Used to check the term basis for classification threshold and AUC. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
