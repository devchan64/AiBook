# P4-8.2 Baseline

> Section ID: `P4-8.2`
> Version: `v2026.07.31`

When recording a baseline, keep `baseline_rule`, `baseline_score`, `comparison_metric`, `important_error_case`, `candidate_gain`, and `next_action` together. This connects the decision to use a more complex model not only to score gain, but to which failure it actually reduces.

In P4-8.1, the discussion examined what model families should be raised as candidates. Now, instead of immediately grabbing those candidates in order of complexity, it moves to the question of setting the starting point of comparison first.

In this problem, what is the simplest standard that must be beaten first?

That question is exactly the starting point of the [baseline model](/AiBook/en/reference/concept-glossary-alpha/b/#baseline-model).

The baseline is often understood as `a temporary model with low performance`. In practice, however, it is much more important than that. A baseline is the floor line of comparison that checks whether a complex model is really creating meaningful improvement.

In both academic and practical contexts, a baseline is closer not to `a good model`, but to `the minimum standard that makes comparison possible`. In other words, without a baseline, even if a performance number looks high, it becomes hard to tell whether that is because the problem is easy, because the data are biased, or because the modeling actually helped.

This Section explains the meaning and role of the `baseline`. Later Sections continue the current context through this handle, and the criterion for what the improvement of a complex model should be compared against reconnects through this Section and the [concept glossary](/AiBook/en/reference/concept-glossary/).

The perspective that must be fixed here is the following one sentence.

A baseline is not simply a weak opponent that must be beaten, but a reference line for reading the meaning of a score.

The order of baseline comparison is fixed briefly as follows.

| What to look at first | Question that comes immediately next | What to judge after that |
| --- | --- | --- |
| baseline score | is this score an easy illusion, or a real starting point | how much did the candidate model improve on the same metric |
| [confusion matrix](/AiBook/en/reference/concept-glossary-alpha/c/#confusion-matrix) and representative [error cases](/AiBook/en/reference/concept-glossary-alpha/m/#model-validation) | what failures were reduced and what failures remain | is this change operationally meaningful |
| candidate-model score | besides accuracy, what changed in recall, F1, or error size | can readers decide whether to tune further or change candidates |

To actually set up a baseline, two things are needed together.

1. a methodology for deciding `what should be used as the simplest comparison standard`
2. minimal theory that explains `why comparison with such a simple standard must come first`

This Section handles `why it is needed first` and `what must be fixed first`, while the following `P4-8.3 supplementary learning` handles with examples and exercises `what representative baselines should be set and how`.

## Questions To Settle Before Setting The Reference Line

This Section answers the following questions.

- Why is a baseline needed first?
- What kind of illusion can occur if there is no baseline?
- Why must the baseline and candidate model be compared under the same conditions?
- As preparation for reading the practical procedure of setting a baseline, what should be grasped first?

This Section first settles `what the improvement of a complex model should be compared against`. The operational perspective of benchmarks and leaderboards, and the big picture of statistical-test-based model comparison, are reorganized again in the supplementary learning of P4-9.3, while the actual hyperparameter comparison procedure continues directly in P4-9.2.

## Judgments To Keep From The Baseline Model

- You can explain a baseline as `the comparison standard that is set before a complex model`.
- You can explain why accuracy illusions and mean-prediction illusions occur when there is no baseline.
- You can explain why tools such as DummyClassifier and DummyRegressor are educationally useful.
- You can adopt the perspective that a good model is not simply one with a high score, but one that creates meaningful improvement over the baseline.
- You can explain why the next Section, P4-8.3, separately reinforces how to actually set a baseline.

## Learning Background

In P4-8.1, the discussion set up a candidate family of models. But setting up candidates does not mean comparison starts immediately. Comparison needs a starting point.

- Even if there is a candidate family, without a comparison standard it is hard to distinguish improvement from illusion.
- Even if there is an evaluation metric, it is hard to know whether the score comes from an easy problem or from the model.
- Even if preprocessing and feature selection were done, the experiment floats in the air if readers do not confirm whether it is better than a simple rule.

So in the curriculum, this Section plays the following role.

| Curriculum position | Role of the baseline Section |
| --- | --- |
| after model selection | turns the candidate family into something actually comparable |
| before tuning | provides the floor line for judging whether tuning created meaningful improvement |
| before the algorithm introduction | prepares readers to explain why a complex algorithm is better than a simple standard |

So if P4-8.1 dealt with `what should be raised as a candidate`, P4-8.2 deals with `by what standard should this candidate be compared`.

The first three questions that must be held onto in this Section are the following.

- Is this a problem that can be matched to some degree without looking deeply at any features at all?
- Is the model I built really better than that easy standard?
- If it improved, on what metric did it improve?

One more thing must be attached here. In classification problems, the mere fact that the score went a little higher than the baseline is not enough. Only when readers place the confusion matrix and representative error cases beside it and inspect `did misses decrease`, `did false alarms increase`, and `does it catch important minority cases better` does baseline comparison come alive. In other words, a baseline is both a numeric comparison table and a reference line for error interpretation.

If this is translated into a customer-churn case, the baseline appears not as `one score`, but as the branching point for reading `did the current model really go beyond the easy standard`.

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-2-mermaid-01-en.mmd"
```

One more thing needs to be remembered separately. `Baseline model` and `baseline reference` meet in the same context, but they are not exactly the same object. The former often means the simplest predictor, while the latter can include the comparison frame that places recent results next to the usual range. This Section separates these two meanings so that even when the reader writes project-retrospective documents in Part 6, the wording does not become confused.

This Section reads them in the following way.

| Distinction | Question to ask first | Role in this Section |
| --- | --- | --- |
| baseline model | `How much can be predicted even without using features deeply?` | the minimum score standard a candidate model must beat |
| baseline reference | `Next to what should recent results be placed so that change becomes visible?` | the comparison frame for interpreting numeric change and error scenes |

The two are different objects, but they share something too. Both are `comparison criteria that keep readers from viewing a number alone without interpretation`.

So the first confirmation items that must be left in baseline comparison are the following four.

| What to leave first | Why it is needed |
| --- | --- |
| baseline score | because the reader needs to know what the starting point was |
| candidate-model score | to see how much it actually improved over the baseline |
| problematic cell in the confusion matrix or large-error region | because the reader must know what direction of failure the score change reduced |
| representative error case | because the reader must confirm whether the model still misses the same kind of input or changed into a different failure |

If the same criteria are moved into a recording structure, they become even clearer.

| Question to leave in Part 4 | Language for a Part 6 retrospective document |
| --- | --- |
| What was the baseline? | fact |
| What actually improved over the baseline? | interpretation |
| What should be checked more in the next comparison or tuning? | next question |

The core of this flow is that the baseline should be placed after selection and before tuning. First, candidate models are set up. Then those candidates must be comparable with the baseline. Only after that is it natural to attach tuning and algorithm-specific expansion.

## Main Learning Content

### What Must Be Fixed First Before Setting A Baseline?

The actual procedure for setting a baseline is examined separately in the next Section, P4-8.3. Still, even in this Section, the preparation items that must be fixed first should be held clearly. A baseline is not a rule that suddenly appears. It can be set only after `what problem is being solved`, `what counts as one sample`, and `what score will be used for comparison` are fixed first.

| What must be fixed before the baseline | Why it must be fixed first here |
| --- | --- |
| problem type | because the simple standard itself changes depending on whether it is classification or regression |
| sample unit | because if what one row means becomes unstable, the baseline score becomes unstable too |
| evaluation metric | because baseline interpretation changes depending on whether accuracy, recall, or MAE is being viewed |
| data distribution | because readers need to know class imbalance or target distribution to see what `an easy standard` is |
| important failure scene | because to judge whether improvement over the baseline is actually meaningful, the operationally important error must be known first |

That means the first stage of a baseline is not `what rule should be chosen immediately`, but `what comparison is being attempted`. In the next Section, these preparation items are used to examine how representative baselines are actually set by problem type.

### Why Is Some Theoretical Knowledge Needed For A Baseline?

Advanced mathematics is not needed first to set a baseline. But a minimal theoretical background is necessary. Only then can the reader explain why a baseline is not merely `a roughly made weak model`, but the comparison standard that must come first.

The common point that becomes clear in the directly checked documents is obvious. scikit-learn explains `DummyClassifier` as a `simple baseline to compare against other more complex classifiers`, and `DummyRegressor` as a `simple baseline to compare against other regressors`. The scikit-learn cross-validation documentation handles procedures for checking evaluation performance over data splitting, and Raschka's review literature summarizes that model-evaluation and model-selection procedures are important. The minimum generalization that this Section takes from here is roughly this: `score differences become readable only when a simple standard and a candidate model are placed on top of comparable conditions`.

The theory needed here can be grouped into three broad points.

| Interpretation perspective used in this Section | Connection to the baseline |
| --- | --- |
| contrast perspective | to see whether the improvement of a complex model really comes from modeling, a minimum comparison target is needed |
| minimum-standard perspective | to read the actual contribution of input features, readers must know what default performance comes out even when the input is hardly used |
| comparability perspective | score differences become less unstable to interpret when both are placed on the same evaluation procedure and metric |

Stated very briefly, these three points mean the following.

- a baseline can be read as `a simple comparison target that uses the input very little`
- only with a baseline does the experiment become one that asks `did the input actually help`
- only when the baseline and candidate model are placed under comparable evaluation conditions does the score gap become easier to interpret

That means this Section reads the baseline not through specific library syntax, but through the interpretation principle that `to talk about improvement, readers must first fix a simple comparison target and then read the score gap under comparable conditions`.

### What Does A Baseline Model Do?

The scikit-learn `DummyClassifier` documentation explains a classifier that ignores input features and makes predictions as `a simple baseline to compare against other more complex classifiers`. The `DummyRegressor` documentation likewise explains a regressor that predicts by simple rules such as the mean or median as a `simple baseline`.

If this explanation is summarized as briefly as possible, it becomes the following.

`A baseline model is the simplest comparison standard that can be built even without deeply understanding the input.`

In other words, a baseline is not a finished model meant to solve a real problem well. It is the minimum standard that says `if the model is not better than this, there was no point in using a complex model`.

Read a little more theoretically, the baseline functions as a minimum comparison target. Even if complex structure is added and much tuning is done, if it is not meaningfully better than the baseline, that experiment may have increased only complexity rather than improvement.

### What Kind Of Illusion Appears Without A Baseline?

Without a baseline, a high number can look like a good model right away. But in reality it may not be.

For example, in data where only 10% of customers churn, if the model predicts `no one churns` for everyone, accuracy can still come out to 90%. In this case, the accuracy alone looks good, but the model actually catches none of the important minority class.

In other words, without a baseline, illusions such as the following can appear.

| Visible number | Actual problem |
| --- | --- |
| high accuracy | it may be high even when the model predicts only the majority class |
| small regression error | it may be similar even when only the average is predicted |
| the new model is complex | complexity does not necessarily mean improvement |

So a baseline is not a device for lowering scores, but a device that makes scores `readable`.

This book distinguishes `baseline model` and `baseline reference`. The former means the simplest prediction standard, and the latter means the comparison frame that interprets recent results by placing them alongside the usual standard. If such a comparison frame is built separately, the scores of rule-based warnings or learned models seen later can be read more clearly as to how meaningful a change they actually represent.

However, the difference between a recent interval and a baseline is not a device that automatically confirms the cause of that difference. It is only a comparison signal that narrows explanation candidates.

That means this book reads the word baseline together at two levels.

| Level where baseline is placed | Example | How this Section reads it |
| --- | --- | --- |
| baseline model | predict only the majority class, predict only the mean | check whether the candidate model is better than the minimum standard |
| baseline reference | compare the recent interval with the usual interval, compare the previous-version rule with the current result | interpret what kind of actual difference a numeric change represents |

| Item | Recent interval | Usual baseline | Difference | Reading |
| --- | ---: | ---: | ---: | --- |
| middle-section average | 2.10 | 2.34 | -0.24 | the recent value is lower than usual |
| late decline rate | -0.42 | -0.28 | -0.14 | the late decline is steeper |
| number of actions | 18 | 20 | -2 | comparison is possible, but the sample count must be viewed together |

Even when reading this table, what matters is the comparison frame more than one absolute value. And for this kind of comparison to be possible, multiple time-point raw series first have to be changed into one-action summary rows so that the same units can be placed side by side.

That is why the baseline reference in this Section should be read not as a separate technique competing with the baseline model, but as an expression that extends the reading principle of `setting the comparison standard first` into the scene of interpreting operational data.

If this difference is drawn in the simplest way, it becomes the following.

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-2-mermaid-02-en.mmd"
```

The core of this diagram is that even the same number is read in a completely different way depending on whether a baseline exists.

The following table is especially important.

| Visible scene | Misunderstanding the reader can easily make | What the baseline does |
| --- | --- | --- |
| accuracy 0.90 | `It predicts pretty well` | checks whether this is just a majority-class prediction |
| regression error is small | `It learned the input well` | checks whether the result is similar even with average-only prediction |
| a complex model raised the score a little | `As expected, the complex model is better` | checks whether the improvement width is actually meaningful |

In other words, baseline comparison is not adding one more score table. It is an interpretation device that asks `is this improvement really the result of reading the structure better`.

That is why when reading a baseline, readers should not write only the number, but also leave the following two things immediately together.

- what representative error scene the baseline is still missing
- whether the failure reduced by the candidate model is a failure that is actually important in operations

These questions are the final stage of baseline methodology. The role of the baseline does not end at writing one line of numbers. It goes as far as showing `what kind of failure that number still leaves behind`.

### Where Are Representative Baseline Methods Continued?

If this Section first established the need for the baseline and the principle of interpretation, then the natural next question is `so what baseline should be built, and how`. That question is continued in `P4-8.3 supplementary learning: how to first set a baseline by problem type`.

That next Section in particular groups the following into actual cases and exercises.

| What the next Section continues with | Why it must be seen right away |
| --- | --- |
| classification baselines | because the reader must know by what simple standard the high-accuracy illusion should first be exposed |
| regression baselines | because the mean/median standard becomes the starting point for judging the actual contribution of input features |
| time-series baselines | because the reader must know why standards such as naive and seasonal naive are often used in time-axis problems |
| baseline-setting procedure | because the reader must know in what order comparison begins, from fixing the problem type to interpreting errors |

### Why Must The Baseline Come Before Tuning?

People often proceed like this.

1. Choose a complex model.
2. Change many parameters.
3. If the score rises a little, treat it as success.

But without a baseline, there is no way to know whether that improvement is actually meaningful.

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-2-mermaid-03-en.mmd"
```

This diagram shows together the correct order of setting the baseline first, comparing the candidate model, and only then entering tuning, and the problem that if a complex model is tuned immediately without a baseline, the meaning of the score change becomes difficult to interpret.

In practice, this difference in order quickly becomes a difference in cost. If a candidate that cannot even beat the baseline is tuned for a long time, experiment time and computational cost may be spent without leaving any improvement that can be explained.

## Detailed Learning Content

### How Should DummyClassifier And DummyRegressor Be Understood?

The dummy-family models of scikit-learn are especially useful educationally.

| Tool | Introductory understanding |
| --- | --- |
| `DummyClassifier` | a baseline that classifies by a simple rule while ignoring features |
| `DummyRegressor` | a baseline that predicts by simple rules such as the mean or median |

The value of these tools is not for actual service use. It lies in quickly showing `what a real model must at least beat`.

In other words, a baseline is part of model selection and at the same time part of reading evaluation.

## Cases And Examples

### Case 1. Fraud Detection That Looks High In Accuracy But Actually Catches Nothing

A payment-service team is building a classification model that catches fraudulent transactions. The criteria people first used were signals such as `repeated payment in a short time`, `a region different from usual`, and `payment at a strange hour`.

Before building the model, the team first sets up a very simple standard that predicts every transaction as `normal`. If fraudulent transactions are extremely rare, even this baseline can produce high accuracy. So without a baseline, it is easy to mistakenly think that a complex model improved performance just by looking at its accuracy.

In this scene, the baseline becomes the floor line for checking `did the complex model really improve in a meaningful way`. Even if the actual model raised accuracy a little, it may not be a big improvement from the operational point of view if fraud recall is still low. By contrast, if recall and F1 clearly improved over the baseline, only then can the reader say that the complex model handles the minority-class problem better.

The confirmable result appears when the baseline and actual model are compared side by side on the same metrics. When not only accuracy but also recall and F1 are placed together, it becomes clear why the baseline is not `a low-performance model`, but `a reference line for interpreting scores`.

The example below reduces this illusion with an actual `DummyClassifier` and `DecisionTreeClassifier`. The data are created as a classification problem with a small positive class, like fraud transactions.

Values to change:

- Lower the positive-class ratio in `weights=[0.82, 0.18]`; baseline accuracy can look even higher, and positive recall becomes more important.
- Change `class_sep=0.9` or `max_depth=3`; how many positive cases the decision tree catches and the confusion matrix will change together.

```python
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=260,
    n_features=6,
    n_informative=2,
    n_redundant=0,
    weights=[0.82, 0.18],
    class_sep=0.9,
    random_state=21,
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.35, random_state=4, stratify=y
)

models = {
    "dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
    "decision_tree": DecisionTreeClassifier(max_depth=3, random_state=0),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, predicted, labels=[0, 1]).ravel()
    print(name)
    print(
        " accuracy=", round(accuracy_score(y_test, predicted), 3),
        "positive_recall=", round(recall_score(y_test, predicted, zero_division=0), 3),
    )
    print(" confusion=", {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)})
```

An example output is as follows.

```text
dummy_most_frequent
 accuracy= 0.824 positive_recall= 0.0
 confusion= {'tn': 75, 'fp': 0, 'fn': 16, 'tp': 0}
decision_tree
 accuracy= 0.956 positive_recall= 0.75
 confusion= {'tn': 75, 'fp': 0, 'fn': 4, 'tp': 12}
```

`dummy_most_frequent` also looks high in accuracy at 0.824. But positive-class [recall](/AiBook/en/reference/concept-glossary-alpha/r/#recall) is 0.0, and it missed all 16 actual positives. A baseline model is therefore not decoration for showing a failed model. It is a comparison line that first reveals the illusion created when only accuracy is read.

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-2-mermaid-04-en.mmd"
```

## Checklist

- What is the simplest baseline for the current problem?
- Are the baseline score and the actual model score being compared on the same metric?
- Are you distinguishing whether the model is better than the baseline, or only more complex?
- Have you checked easy traps such as class imbalance or mean-only prediction through the baseline?
- Before tuning, did you first read the difference between the baseline and candidate model?
- Can you explain that a baseline is the comparison standard set before a complex model, and that even a high score is hard to interpret without comparing it to the baseline?
- Can you explain that a baseline is not `one more score to inspect`, but a standard that leaves together the starting-point score, representative error cases, and key-metric differences?

## Sources And References

- scikit-learn developers, [`DummyClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, accessed 2026-07-26.
- scikit-learn developers, [`DummyRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, accessed 2026-07-26.
- scikit-learn developers, [`Cross-validation: evaluating estimator performance`](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, accessed 2026-07-26.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [*The Elements of Statistical Learning*](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-26.
- Sebastian Raschka, [`Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning`](https://arxiv.org/abs/1811.12808){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-07-26.
