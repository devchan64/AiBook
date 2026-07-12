# P4-3.2 Heuristics And Model Selection

> Section ID: `P4-3.2`
> Version: `v2026.07.12`

P4-3.1 treated a heuristic as a judgment criterion for reducing candidates under limited time and limited information. This Section applies that perspective to model selection.

When studying machine learning, the question `which model should be used?` often feels very large. But model selection is not simply the act of picking the name of a famous algorithm. It is the work of looking at the problem form, the state of the data, interpretability, computation cost, and evaluation criteria together, then narrowing the candidate set that should be tried first.

Here the heuristic is not the final conclusion but the starting point. You decide something like `for this problem, let's try these models first`, then validate whether that choice is acceptable on real data.

This Section does not define heuristics again at length. The basic meaning of judgment for reducing candidates is connected again through P4-3.1 and the [concept glossary](../../../reference/concept-glossary.md). Here the focus is only on how that judgment operates in the stage of model selection.

## Scope Of This Section

This Section explains how heuristics are used in model selection. It does not go deeply into the formulas, implementation, or detailed performance comparison of individual models here.

Data splitting and validation return in P4-4, overfitting and generalization in P4-5, metrics in P4-6, preprocessing and features in P4-7, model-selection procedures in P4-8, and hyperparameter tuning in P4-9.

Specific models are met separately later. Linear regression appears in P4-10, logistic regression in P4-11, k-nearest neighbors in P4-12, support vector machines in P4-13, decision trees in P4-14, random forests in P4-15, and gradient boosting in P4-16. Clustering and dimensionality reduction are handled in P4-17 and P4-18.

This Section answers the following questions.

- In model selection, what does a heuristic actually reduce?
- How does problem type narrow the model candidates?
- Why is a baseline model needed?
- How do performance, interpretability, and cost conflict?
- What must be written down to keep heuristics as a verifiable record?

## Goals Of This Section

- You can explain model selection not as choosing a model name, but as a flow of reducing candidates and validating them.
- You can explain why the candidates to inspect first change according to problem type.
- You can explain that a baseline model is a comparison standard for judging more complex models.
- You can understand that model selection is influenced not only by performance but also by interpretability, computation cost, and the current state of the data.
- You can learn how to record model-selection heuristics as working hypotheses.

## Understanding It First Through One Scene

Think about a small project for predicting customer churn. The data include recent login count, purchase amount, number of inquiries, and subscription period. The goal is to find customers who are likely to churn next month.

In this situation, many models are possible. But trying every model from the beginning is not always a good starting point.

| Candidate | Why it comes to mind first | What to be careful about | Where it returns later |
| --- | --- | --- | --- |
| Logistic regression | It becomes a simple baseline when predicting two categories such as churn or stay. | A purely linear relation may be insufficient. | P4-11 |
| Decision tree | It is easy to explain `under what conditions churn increases`. | If it grows deep, it can fit the training data too much. | P4-14 |
| Random forest | It can offer more stable performance by combining many trees. | It can become harder to explain than a single tree. | P4-15 |
| Gradient boosting | It often shows strong performance on tabular data. | Tuning and validation must be done more carefully. | P4-16 |

Here the heuristic does not say `logistic regression is the answer`. Instead, it creates an experimental order such as `set a simple baseline first, then compare explainability and performance after that`.

If that judgment is drawn as a case flow, model selection becomes easier to read not as `choosing a name`, but as `reducing candidates through the problem and its constraints, then making a small comparison set`.

```mermaid
--8<-- "assets/part-04/chapter-03/churn-model-selection-flow-en.mmd"
```

## Model Selection Is A Process Of Reducing Candidates

Model selection usually proceeds in the following flow.

```mermaid
--8<-- "assets/part-04/chapter-03/model-selection-basic-flow-en.mmd"
```

The important point in this flow is that it does not try to guess the final model in one step. It first looks at the problem type, then checks the constraints, sets a baseline model, and compares a small candidate set. If the validation result is poor, the candidate set is changed again.

## Problem Type Narrows The First Candidate Set

The first thing to inspect is the problem type. The candidate set changes depending on whether the value to predict is numeric, categorical, or unlabeled structure.

| Question | Problem type | Candidate to recall first | Where it returns later |
| --- | --- | --- | --- |
| Are you predicting a number such as house price, sales, or temperature? | regression | linear regression, tree-based regression | P4-10, P4-14 |
| Are you predicting a category such as pass/fail or churn/stay? | classification | logistic regression, decision tree | P4-11, P4-14 |
| Are you looking for similar groups without labels? | clustering | k-means, DBSCAN | P4-17 |
| Do you want to reduce many features into a smaller set of axes? | dimensionality reduction | PCA, t-SNE | P4-18 |
| Are actions chosen and rewards returned? | reinforcement learning | Q-learning, policy gradient | P4-19 |

This table is not an answer key. It is a map for narrowing the candidates. The actual choice still has to be checked again through data and evaluation results.

## A Baseline Model Is A Comparison Standard

A baseline model is not the model meant to produce the best performance from the beginning. It is the comparison standard used to judge `is it worth using a more complex model?`

For example, in churn prediction, even if you use no model at all and simply predict `most users will not churn`, accuracy can still look high. In that case, it is hard to say a more complex model is truly useful just because accuracy rose a little. Precision, recall, cost, and business purpose must be viewed together.

A baseline model helps answer the following questions.

- Is it better than a simple rule that uses no model at all?
- Is a complex model actually better enough than a simple one?
- Is the performance gain large enough to justify sacrificing interpretability or operational cost?
- With the current data, should data quality be improved before pushing the model further?

Baselines are handled in more detail in P4-8.2. In this Section, they are used only as the first fixed reference point of model-selection heuristics.

## Do Not Choose By Performance Alone

Performance matters in model selection. But if you choose by performance alone, practical problems can appear.

| Criterion | Question | Example |
| --- | --- | --- |
| performance | Is the target metric good on validation data? | In a problem where recall matters, do not inspect accuracy alone. |
| interpretability | Can people explain and inspect the result? | If business stakeholders must understand the rule, a simpler model may be better. |
| computational cost | Is training and prediction time acceptable? | In a real-time service, prediction latency matters. |
| data requirement | Does it fit the current data scale and quality? | If data are small, a complex model can be unstable. |
| operability | Can it be deployed, monitored, and retrained? | Even a good model can fail if it is too hard to operate. |

These criteria can conflict. An easy-to-explain model may underperform, while a high-performing model may cost more or be harder to explain. Model-selection heuristics help surface these conflicts early.

## Frequently Used Model-Selection Heuristics

The following heuristics are used often in early experiments. All of them still require validation.

| Heuristic | Why it can be used | What must always be checked |
| --- | --- | --- |
| Build a simple model first. | A baseline level can be set quickly. | Check whether the simple model is already enough, and whether a more complex model is really better. |
| Divide candidates by problem type. | Regression, classification, and clustering have different goals. | Recheck whether the actual goal has been defined properly. |
| In work where explanation matters, look at interpretable models first. | The result may need to be explained to people. | Do not ignore performance risk just because the model is easier to explain. |
| If the dataset is small, do not rush into very complex models. | The risk of overfitting can rise. | Check data splitting and validation results. |
| For models sensitive to feature scale, inspect preprocessing together. | Models such as k-NN and SVM can be affected by distance and spacing. | Reflect preprocessing conditions fairly in the model comparison. |
| If even the baseline is too weak, suspect the data first. | The problem may be the labels, missing values, or sampling rather than the model. | Recheck data quality and problem definition. |

These heuristics are not rules that say `always do this`. They are starting points that help early exploration proceed in an orderly way.

In practice, the core question is first judging `which model candidates should be narrowed first right now`.

| Current problem state | Direction of the first reduction | Why |
| --- | --- | --- |
| The output is categorical and interpretability also matters | Start with simple classification candidates such as logistic regression and decision tree | Because it is easy to compare a baseline quickly with rule-like intuition |
| Nonlinear relations are suspected in tabular data | Include tree-family candidates together | Because they may capture feature interactions better |
| Structure exploration matters more than labels | Shift direction toward clustering or dimensionality reduction candidates | Because understanding structure matters more right now than comparing prediction models |
| Even the baseline is too weak | Recheck data and labels before the model | Because the problem definition or data quality may already be unstable |

## Heuristics Must Be Recorded

If heuristics remain only as intuition in someone's head, they are hard to validate. In model selection, you need to record why a model was looked at first, what the concern was, and by what criterion the choice would later be changed.

| Record item | Example |
| --- | --- |
| Selected candidates | Compare logistic regression and decision tree first. |
| Reason for selection | It is a churn classification problem and interpretability is needed. |
| Expected risk | A linear relation may be insufficient, or the tree may overfit. |
| Validation method | Compare them using the validation data discussed in P4-4. |
| Evaluation criterion | Look at both recall and precision, which are discussed in P4-6. |
| Next action | If neither is sufficiently better than the baseline, revisit the data and features. |

When written like this, the heuristic no longer means `we picked it by gut feeling`. It becomes `we started with a verifiable working hypothesis`.

## Misunderstandings To Be Careful About In This Section

The most common misunderstanding in model selection is thinking that a more famous model is always better. In reality, if data are small, labels are unstable, or interpretability matters greatly, a simpler model can be more appropriate.

The second misunderstanding is choosing a model by looking at only one validation score. That can also lead to fitting the validation data too strongly. This problem returns in P4-5 on overfitting and generalization.

The third misunderstanding is seeing model selection as a problem of the model alone. If performance is poor, before making the model more complex, you must first check whether the data, labels, features, and evaluation criteria actually fit the problem.

## Cases And Examples

### Case 1. Which Model Should Be Compared First In Customer-Inquiry Classification?

Suppose a customer center wants to classify inquiries automatically into `refund`, `delivery delay`, `account problem`, and `product inquiry`. Until now, business staff have first separated them manually using keyword rules based on whether the title contains words such as `refund`, `cancel`, or `delivery`.

That method is fast in the beginning, but as soon as wording changes a little, more inquiries start slipping through. `I want a refund` can be caught, but a sentence like `would it be possible to cancel this payment` expresses a similar meaning in different words and can be missed by rules alone. So the team must choose a starting point somewhere between `use the most complex model right away` and `just keep the existing rules`.

Here a model-selection heuristic can become `first check how far simple sentence classification works with a baseline such as logistic regression, then compare whether more explainability or better performance is still needed`. After that, decision trees or stronger models can be added for comparison, so the actual gain from increased complexity becomes visible.

The checkable result is clear as well. By comparing the error types of the baseline model and the rule-based classifier, then looking at precision and recall by class, you can confirm which inquiry types improved. If the baseline already handles most repeated inquiries stably, more complex models can be postponed. If it keeps failing on inquiries with high wording variation, then a stronger representation model should be reviewed.

```mermaid
--8<-- "assets/part-04/chapter-03/inquiry-classification-model-selection-flow-en.mmd"
```

## Checklist

- Can you explain why model selection is not `choosing a famous model` but `reducing the candidate set`?
- Can you explain in what state the data and labels should be rechecked before making the model more complex?
- Can you explain why a baseline model becomes the comparison standard for interpreting the performance of more complex candidates?
- Can you explain that model selection is not guessing a model name, but the process of reducing candidates and validating them?
- Can you explain that problem type is the first criterion for narrowing model candidates, and that a baseline model is the minimum standard for comparing more complex candidates?
- Can you explain why performance, interpretability, computation cost, data state, and operability all need to be viewed together?

## Sources And References

- scikit-learn developers, `Choosing the right estimator`, scikit-learn User Guide, accessed 2026-06-25. [https://scikit-learn.org/stable/machine_learning_map.html](https://scikit-learn.org/stable/machine_learning_map.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Cross-validation: evaluating estimator performance`, scikit-learn User Guide, accessed 2026-06-25. [https://scikit-learn.org/stable/modules/cross_validation.html](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, Jonathan Taylor, `An Introduction to Statistical Learning`, Springer, official website accessed 2026-06-25. [https://www.statlearning.com/](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }
