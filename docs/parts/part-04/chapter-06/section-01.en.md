# P4-6.1 The Role Of Evaluation Metrics

> Section ID: `P4-6.1`
> Version: `v2026.07.12`

In Chapter P4-5, we looked at overfitting and generalization. The next question follows naturally. What do we actually use to check the claim that `the model also holds up on new data`? What appears at that point is the `evaluation metric`.

An evaluation metric is a tool that shows with numbers how well a model fits. But the more important point is that a metric is not just a scoreboard. It is also `a promise about what we are choosing to treat as important`. Even with the same model, it may look good or risky depending on which metric is examined.

This Section explains the basic roles of `evaluation metrics`, `accuracy`, `precision`, `recall`, and `F1`. The next Section continues the current context through this handle, and the criterion for deciding what kind of error should be treated as important is connected again through this Section and the [concept glossary](../../../reference/concept-glossary.md).

## Scope Of This Section

This Section is an introduction to the role of evaluation metrics. It connects accuracy, precision, recall, and F1 score at a first-meeting level. Metrics such as ROC-AUC, PR-AUC, log loss, calibration, and silhouette are collected separately in the P4-6.4 supplementary Section, while regression metrics and clustering perspectives continue in P4-6.2.

So the main responsibility of this core Section is to fix `what should be treated as important`. More delicate readings such as probability-score interpretation, reliability diagrams, Brier score, or fine threshold adjustment are passed to P4-6.4 and later P4-15.3. Here the first task is to make clear why there is not just one metric.

This Section also fixes a basic attitude for reading metrics. In classification, the first thing to inspect is the confusion matrix and representative error cases, and later in P4-8.2 the question returns again by comparing with a baseline to see whether the change in error structure is actually meaningful. In other words, evaluation in Part 4 continues along a flow that prioritizes `where did the model fail?` and `better compared to what?` over `one number`.

P4-6.2 continues by asking which evaluation criteria should be given more weight for different problem types. For now, the focus is on `why there is not just one metric`, `why even the same number can mean different things`, and `why work goals and error costs must enter the choice of metric`.

- Why are evaluation metrics needed?
- Why can looking only at accuracy create misunderstandings?
- What question does precision answer, and what question does recall answer?
- Do metrics reveal not only model performance but also what we choose to value?
- Why does the next Section need to separate metrics by problem type?

## Goals Of This Section

- You can explain evaluation metrics as `criteria for reading model performance`.
- You can understand that accuracy is not the representative metric in every situation.
- You can explain that precision and recall answer different questions.
- You can explain that work goals and error costs affect metric selection.
- You can prepare to move into problem-type-specific evaluation criteria in P4-6.2.

## Learning Background

### What Does An Evaluation Metric Do?

The scikit-learn documentation treats metrics and scoring as `tools for quantifying the quality of predictions`. At the same time, it explains that the choice of metric is ultimately tied to `what the predictions are being used for`.

`An evaluation metric is a criterion that summarizes a model's result in numbers while also revealing which errors we consider more important.`

So a metric does not merely say, `what is the score?`

- What do we most want to get right?
- Which mistakes do we especially want to reduce?
- What real decision will this model be connected to?

It brings those questions in as well.

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-1-mermaid-01-en.mmd"
```

This diagram shows that evaluation metrics are not only about numbers inside the model. They are criteria connected to an actual decision-making context. Even with the same prediction, the metric that gets inspected first changes depending on which kind of error hurts more.

The key point in this flow is that `the metric is connected to a decision context outside the model`. The model makes predictions, but the metric makes us read what those predictions mean in an actual decision.

## Main Learning Content

### Why Accuracy Alone Is Not Enough

Google's machine-learning glossary explains accuracy as `the proportion of correct predictions among all predictions`. The definition itself is simple and useful. But the same glossary also explains that in class-imbalance data, accuracy can become deeply misleading.

For example, if spam email is extremely rare, a model that predicts every email as `normal` can still show a high accuracy. But such a model does not actually filter spam.

| Question | Misunderstanding that can occur when only accuracy is inspected |
| --- | --- |
| How many did the model get right overall? | It may look like the model got many things right |
| Did it avoid missing important positive cases? | Accuracy may not answer that question well enough |
| Did it avoid raising too many false alarms? | Accuracy may not answer that question well enough either |

So accuracy can be a starting point, but it may not be the metric that carries responsibility all the way to the end.

The starting point of metric reading is to check `what kind of error or success is being asked first right now`.

| Current concern | The question to bring up first | A metric often inspected first |
| --- | --- | --- |
| I want to know how many were correct overall | How many predictions were correct among all predictions? | accuracy |
| It is costly to call something positive for no good reason | Of the things predicted as positive, how many were actually positive? | precision |
| It is costly to miss real positive cases | How many real positive cases did the model avoid missing? | recall |
| I want one summary of precision and recall together | Can the balance between the two be read in one number? | F1 |

### First Read It Through The Confusion Matrix

To understand precision and recall, you should first look lightly at the `confusion matrix`. Google's glossary explains the confusion matrix as `a table that summarizes what the model got right and wrong`.

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-1-mermaid-02-en.mmd"
```

This diagram shows why the confusion matrix becomes the starting point of evaluation metrics. Only when actual values and predicted values are gathered in one table can you read not only accuracy, but also different kinds of mistakes such as FP and FN separately.

The first four cells a reader should fix in the confusion matrix are the following.

| Item | Meaning |
| --- | --- |
| TP (true positive) | a real positive case correctly predicted as positive |
| TN (true negative) | a real negative case correctly predicted as negative |
| FP (false positive) | a real negative case incorrectly predicted as positive |
| FN (false negative) | a real positive case incorrectly predicted as negative |

The important point here is that even `wrong` has two forms.

- FP means `a false alarm that did not need to be raised`
- FN means `a needed alarm that was missed`

Because the cost of those two is not the same, evaluation cannot end with one metric.

It becomes quicker with a small example.

| Actual / Predicted | Predicted positive | Predicted negative |
| --- | --- | --- |
| actual positive: 10 cases | 8 cases -> TP | 2 cases -> FN |
| actual negative: 90 cases | 6 cases -> FP | 84 cases -> TN |

If this table is turned back into reader questions, it becomes the following.

- It caught 8 of the 10 actual positive cases -> a recall-side question
- Of the 14 cases called positive, only 8 were actually positive -> a precision-side question

So even with the same table, you can ask `how many positives were missed?` or `how many cases were called positive for no good reason?`

Even with the same result table, the first reader question is not always the same. If missing cases hurts more, recall is read first. If false alarms hurt more, precision is read first.

### Precision And Recall Answer Different Questions

Google's glossary explains recall through the following question.

> When the case was actually positive, what percent of those cases did the model correctly catch as positive?

From the same perspective, precision at an introductory level can be organized through the following question.

> Of the things the model said were positive, what proportion was actually positive?

If the two are separated into a table, it becomes clearer.

| Metric | Reader question | Mistake it especially worries about |
| --- | --- | --- |
| accuracy | How many were correct overall? | total errors |
| precision | Of the things called positive, how many were correct? | the side of reducing FP |
| recall | Of the actual positive cases, how many were not missed? | the side of reducing FN |

Understanding this table alone is enough to prepare for the next Section.

## Detailed Learning Content

### The Historical Background Of Evaluation Metrics

Evaluation metrics are not tools that suddenly appeared only in recent machine learning. In information-retrieval research, the question `what should be called a good result?` had long been central. In his classic textbook on information retrieval, C. J. van Rijsbergen treats evaluation as a separate chapter and explains why evaluation is needed through social and economic questions. The same chapter introduces recall and precision as a key pair that took root in explaining the effectiveness of retrieval systems after Cyril Cleverdon's measurement work.

1. Computer systems early on had to separate `relevant things` from `irrelevant things`.
2. So the question became not only `did the system find many things?` but also `did it avoid missing relevant things?` and `did it avoid returning too many useless things?`
3. That idea later spread beyond information retrieval into classification, detection, and machine-learning evaluation.

So evaluation metrics are not decoration added to numbers. They are a language developed to ask `what actual help and what actual harm does this system produce for a user?`

## Cases And Examples

### Case 1. How Should We Read An Inspection Model That Raises Too Many Defect Alarms?

A factory inspection system is separating product images into `defective` and `normal`. The criteria people first used were signals such as `is there a crack`, `is there a surface stain`, and `is the corner chipped`.

At first, the model looked good because the accuracy was high. But in the actual field, it keeps sending normal products to reinspection as defects. Another setting reduces reinspections but increases the number of real defects that get missed. At that point, it is hard to say which model is better through accuracy alone.

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-1-mermaid-03-en.mmd"
```

Here the evaluation metric becomes the criterion that reveals `which kind of pain matters more`. If reinspection cost is high in the field, precision deserves more careful inspection. If missing a defect is more dangerous, recall should be treated as more important. Even with the same confusion matrix, the judgment changes depending on which error cost is read first.

The checkable result appears when the confusion matrix, precision, and recall are inspected together. Once `how many normal products were called defective for no good reason` and `how many real defects were missed` are counted separately, you can explain why a model with high accuracy still becomes problematic in actual operation.

## Cases And Examples

### Work Goals Change The Metric

Even in the same classification problem, the first metric people look at changes when the work goal changes.

| Scene | Metric that tends to be inspected first | Why |
| --- | --- | --- |
| disease screening | recall | because missing a case can create a major problem |
| spam blocking | precision and recall together | because both blocking normal email and missing spam must be handled carefully |
| ad-click prediction | precision, recall, and post-threshold performance may matter more than accuracy | because the positive ratio and cost structure are not simple |
| fraud detection | recall is often emphasized strongly, but FP cost is also inspected | because both misses and false alarms become operational cost |

So a metric is not only about mathematical formulas. It is also about `which kind of error hurts more`.

If you rewrite it into an operating scene that feels familiar to software engineers, it may become more intuitive.

| Operational question | In what way it resembles a machine-learning metric question |
| --- | --- |
| Are we raising too many alerts? | Are we creating too many FP cases? |
| Are we missing real incidents? | Are we creating too many FN cases? |
| Is the overall ratio of handled requests high? | Are we looking at the overall ratio like accuracy? |

This analogy does not mean exactly the same thing. But it is very similar in the sense that `the number to inspect changes depending on which failure should be reduced more`.

### Reading It Again Through Social-Phenomenon Examples

This issue does not arise only inside company services. The same question appears in classification and detection tasks that deal with social phenomena.

| Scene | Question to inspect first | Why the metric must be read differently |
| --- | --- | --- |
| disaster alerts | How many real dangers were not missed? | if recall is low, major events may be missed |
| welfare-recipient selection | How many people in need were not left out? | when FN increases, people who need support can be excluded |
| automatic resume sorting in hiring | How high is the rate of incorrect rejection? | high accuracy alone may hide unfair disadvantages to some groups |
| online hate-expression detection | Are dangerous expressions not being missed while normal expressions are not being blocked too aggressively? | if recall and precision are not read together, the social cost can grow |

The important point in this table is that `the good metric` is not always fixed as one thing. In social phenomena, the cost of error changes depending on who bears it and in what form.

For example, in disaster alerts, misses or false negatives can be especially severe. In automatic resume sorting, `incorrect exclusion` can become a major social issue. In cases such as online-expression detection, where both sides of the cost are large, precision and recall must be inspected together.

If welfare-recipient selection is reduced to a very simple example, it can be read like this.

| Scene | What the number means |
| --- | --- |
| recall is low | many people who actually need support may be getting missed |
| precision is low | many cases with lower urgency may be getting included |
| only accuracy is high | the overall proportion may look good, but an important minority group may still be getting missed |

This example matters because in social phenomena, `who was left out` and `who was incorrectly included` are often more important than `how many were correct overall`.

### Even With The Same Accuracy, The Models Can Be Different

The table below shows that even the same accuracy can lead to different interpretations.

| Model | accuracy | precision | recall | How to read it |
| --- | --- | --- | --- | --- |
| A | 0.95 | 0.91 | 0.42 | It is fairly correct when it says positive, but it misses many actual positive cases |
| B | 0.95 | 0.63 | 0.88 | It catches more positives, but it may also raise more false alarms |

If you look only at accuracy, the two models seem the same. But the choice can change depending on which type of error you want to reduce more.

- high accuracy can be a good starting point
- but missing positive cases and calling things positive for no good reason are different problems
- that is why precision and recall should be read together

### F1 Score Is An Attempt To Read Both Together

Google's glossary explains F1 score as a representative summary metric that uses precision and recall together. The definition to hold first is the following.

`F1 score is a compromise metric used when you want to inspect precision and recall together through one number.`

But F1 is not magic either.

| Strength | Limit |
| --- | --- |
| It lets you inspect precision and recall together | It can hide which of the two matters more |
| It is often more useful than accuracy on imbalanced data | It still does not replace the whole work-cost structure |

So F1 is only a summary that says `let us inspect the two together`. It is not always the final conclusion.

This Section sees it as more accurate to read classification evaluation through the following order than to memorize many metric names.

| Reading order | What to inspect first | Why this order is needed |
| --- | --- | --- |
| 1 | confusion matrix | because you should first see which kind of mistake is frequent if you want to reduce illusions caused by accuracy |
| 2 | representative error cases | because even with the same FN or FP, looking at what kind of input was missed reveals data problems and boundary cases |
| 3 | precision, recall, F1 | because only after seeing the error structure can you judge which number summarizes the problem better |
| 4 | comparison with a baseline | because later in P4-8.2 you still need to check whether the score change is actually a meaningful improvement |

## Practice And Examples

### Reading The Role Of Metrics Through A Python Example

The following code is not actual training. It is an example that reads metrics from confusion-matrix counts.

Problem situation:

- A model that looks good when only accuracy is checked can look very different when the confusion matrix is used to recalculate the metrics

Input:

- `tp`, `tn`, `fp`, `fn`

Output:

- accuracy
- precision
- recall
- f1

Concept to check:

- even with the same confusion matrix, model evaluation can change depending on which metric is read
- in imbalanced data, accuracy can look too optimistic

```python
tp = 30
tn = 4999000
fp = 950
fn = 20

accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)

print("accuracy:", round(accuracy, 4))
print("precision:", round(precision, 4))
print("recall:", round(recall, 4))
print("f1:", round(f1, 4))
```

The output can be read like this.

```text
accuracy: 0.9998
precision: 0.0306
recall: 0.6
f1: 0.0582
```

These numbers give an important sense.

- accuracy looks almost perfect
- but precision is very low
- recall stays around 60%

In other words, `a model that looks good through accuracy alone but still has serious problems in practice` can really exist.

### Looking At Same Accuracy, Different Interpretation Through A Python Example

This time, read the point that accuracy can be the same while precision and recall differ.

Problem situation:

- there can be two models whose operational meaning is completely different even though they have the same accuracy

Input:

- each model's accuracy
- each model's precision
- each model's recall

Output:

- comparison of the three metrics for each model

Concept to check:

- the same accuracy does not mean the two models have the same quality
- precision and recall are interpreted differently depending on which kind of pain matters more

```python
models = [
    {"name": "model_A", "accuracy": 0.95, "precision": 0.91, "recall": 0.42},
    {"name": "model_B", "accuracy": 0.95, "precision": 0.63, "recall": 0.88},
]

for item in models:
    print(item["name"])
    print("  accuracy :", item["accuracy"])
    print("  precision:", item["precision"])
    print("  recall   :", item["recall"])
```

The output can be read like this.

```text
model_A
  accuracy : 0.95
  precision: 0.91
  recall   : 0.42
model_B
  accuracy : 0.95
  precision: 0.63
  recall   : 0.88
```

The important point in this example is not to mechanically choose `which one is better`. The important point is that `the interpretation changes depending on what is treated as more important`.

If you rewrite it very briefly as an operations sentence, it can be said like this: `Model A has many misses, so dangerous cases should be reviewed first. Model B may create more false alarms, so reinspection cost and the threshold should be checked together again.` In other words, once a metric table is read, the next sentence should immediately become `which error increased more` and `what should be checked next because of that error`.

## Checklist

- Can you explain why accuracy alone can miss important error costs?
- Can you explain by what criterion you would choose to inspect precision first or recall first in the current scene?
- Can you explain why the confusion matrix and representative error cases should be read before the metrics?
- Can you explain that evaluation metrics summarize model results in numbers while also revealing which errors are treated as more important?
- Can you explain that accuracy is a useful starting point but not the representative metric in every situation, and that even with the same accuracy, interpretation and choice can change if precision and recall differ?
- Can you explain what question precision, recall, and F1 each answer?

## Sources And References

- scikit-learn developers, `Metrics and scoring: quantifying the quality of predictions`, scikit-learn User Guide, accessed 2026-06-26. [https://scikit-learn.org/stable/modules/model_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }
- Google for Developers, `Machine Learning Glossary`, accessed 2026-06-26. [https://developers.google.com/machine-learning/glossary/](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" }
