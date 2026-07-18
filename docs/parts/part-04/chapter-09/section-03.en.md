# P4-9.3 Supplementary Learning: Reading The Big Picture Of Advanced Model Selection, Tuning Automation, And Experiment Tracking

> Section ID: `P4-9.3`
> Version: `v2026.07.12`

P4-8 and P4-9 established the basic flow of setting model candidates, placing a baseline, and comparing hyperparameters inside a validation procedure. After that, the following names usually appear.

- information criteria (AIC, BIC)
- AutoML
- benchmarks and leaderboards
- Bayesian optimization, Hyperband
- nested cross-validation
- experiment tracking

The goal of this Section is not to learn the implementation details of each of them, but to organize `why these names appeared and what level of problem each of them handles`.

This supplementary learning also does not re-explain from the beginning the basic definitions of hyperparameters and tuning. The basic handles remain in P4-9.1, P4-9.2, and the [concept glossary](/AiBook/reference/concept-glossary/), while this Section only organizes the advanced names that come after them in a broad flow.

## Scope Of This Supplementary Learning

This Section answers the following questions.

- In what kind of model-selection problem do information criteria (AIC, BIC) appear?
- What are AutoML and large-scale search systems trying to automate?
- What do benchmarks and leaderboards make it possible to compare, and what can they hide?
- Why did Bayesian optimization and Hyperband appear after grid search?
- Why did nested cross-validation and experiment tracking become important for reducing reproducibility problems and overestimation risk?

This Section does not cover the following topics deeply.

- mathematical proofs of each algorithm
- setup screens and operating procedures of specific platforms
- details of building distributed cluster infrastructure

GPU computation structure is revisited in Part 5, and large-scale operational constraints reconnect in Part 6.

## Goals Of This Supplementary Learning

- You can distinguish that advanced model-selection topics are not all concepts at the same level.
- You can explain AIC/BIC, AutoML, benchmarks, and experiment tracking as solutions to different problems.
- You can develop the perspective that distinguishes `running more things` from `comparing more fairly`.

## Dividing The Levels

These items can look similar when listed in one line, but in reality they answer different questions.

| Name | The question it mainly answers |
| --- | --- |
| AIC, BIC | How should statistical model complexity and fit be viewed together? |
| Bayesian optimization, Hyperband | How can many setting-value candidates be searched more efficiently? |
| nested cross-validation | How can overestimation be reduced more, including the model-selection process itself? |
| AutoML | How far should candidate generation, preprocessing, and some tuning be automated? |
| benchmark, leaderboard | By what common standard should multiple models or systems be compared? |
| experiment tracking | How can many experiment results be preserved and explained again without losing them? |

In other words, all of these connect to `choosing a good model`, but the detailed problems they try to solve differ.

## Where Do AIC And BIC Fit?

AIC and BIC mainly appear in the context of statistical model selection.

- If only goodness of fit is considered, complex models can become advantageous.
- It may be desirable to reflect the model becoming too complex as a kind of penalty.
- AIC and BIC are attempts to compare that balance numerically.

In the current main text of this book, the machine-learning practice flow comes first, so the formula development of AIC/BIC is not extended further here. Instead, it is enough to hold on to why the idea of `viewing fit and complexity together` appeared.

## What Do AutoML And Large-Scale Search Systems Automate?

AutoML usually develops in the direction of automating the following bundle.

1. Create preprocessing candidates.
2. Create model candidates.
3. Search hyperparameter candidates.
4. Organize them by validation score.

In other words, AutoML is closer to not `a button for one model`, but `a system that automatically repeats part of the model-selection and tuning flow`.

But the same risks remain here as well.

- If the validation procedure is loose, overestimation remains even if it is automated.
- The wider the search range is, the larger the computational cost can become.
- The explainability of the result can become lower.

## Why Should Benchmarks And Leaderboards Be Viewed Separately?

A benchmark is a device for comparing multiple models under the same data and the same evaluation rules. A leaderboard is a form that shows that result like a ranking.

They are useful, but they also create the following illusions.

- Even a very small ranking gap can look like an essential difference.
- The strength on one dataset can look like general superiority.
- Differences in preprocessing, time budget, and tuning budget can be hidden.

Therefore, benchmarks and leaderboards are `tables that let comparison begin`, not final truth by themselves.

## Why Did Bayesian Optimization And Hyperband Appear?

As seen in P4-9.2, grid search is easy to explain, but the number of combinations grows quickly. So the following demands appear.

- A desire to find important axes faster
- A desire to spend less time on unlikely candidates
- A desire to see more candidates inside a limited computation budget

In this context, they can be read as follows.

- Bayesian optimization: an approach that tries to choose `where to test next` more intelligently
- Hyperband: an approach that tries to save budget by `stopping unpromising candidates early`

## Why Is Nested Cross-Validation Mentioned Separately?

If nested cross-validation is read only as a technique that runs cross-validation once more in a more complicated way, it becomes blurry. The core is this.

`A stricter separation is desired between the validation used for model selection and the final performance estimation.`

In other words, it is an attempt to reduce the optimistic estimation that can arise when the same validation procedure is used for both selection and evaluation at the same time. It is often mentioned when readers want to make comparison stricter on small data.

This Section treats it as `an advanced validation structure that tries to separate selection and evaluation more strongly`.

## Why Did Experiment Tracking Become A Modeling Topic?

When experiments are few, notebook filenames or simple notes can be enough. But when candidate models, preprocessing, and parameter combinations increase, the following problems soon appear.

- People forget which experiment used which settings.
- Scores remain, but the data version does not.
- It becomes hard to explain why performance improved.

That is why experiment tracking is not a simple record-keeping habit, but a foundation that makes model selection and tuning explainable again.

| What must be left behind | Why |
| --- | --- |
| data version | to confirm whether it was the same data |
| preprocessing rules | to confirm whether the inputs were the same |
| hyperparameters | to explain what was changed |
| metric | to compare what improved |

## When Should Which Advanced Tool Be Brought To Mind?

Advanced model-selection tools all look like `techniques for running more things`, but in reality they target different bottlenecks.

| The point where you are stuck now | The category to bring to mind first | Reason |
| --- | --- | --- |
| You want to view the fit and complexity of a statistical model together. | AIC, BIC | because they compare fit together with a complexity penalty |
| The search space is wide and grid search is too expensive. | Bayesian optimization, Hyperband | because they reduce search cost through next-candidate choice or early stopping |
| You want to separate selection and final evaluation more strictly. | nested cross-validation | because it reduces the optimistic bias of the selection process further |
| You want to automatically repeat candidate generation and some tuning. | AutoML | because it automates preprocessing, candidate generation, and part of the search |
| There are too many experiments and you are starting to lose the grounds for comparison. | experiment tracking | because it lets you trace again the data version, rules, scores, and reasons for setting changes |

The core of this table is not memorizing names, but distinguishing that different tools appear depending on `what the bottleneck is right now`.

## Cases And Examples

### Case 1. When There Were Many Experiments But It Is Hard To Explain Why One Combination Was Good

A recommendation-system team is running several model candidates and tuning combinations at the same time. The criteria people first looked at were signals such as `recent clicks`, `genre preference`, and `similar user behavior`.

Several days later, the score table remains, but memory starts to blur about which experiment used which preprocessing rules, which hyperparameter combination it had, and whether it used the same data version. In this situation, even if one high score on the leaderboard is visible, it is hard to explain whether it is actually the result of a fair comparison. The reason names such as AutoML, benchmarks, and nested cross-validation are needed is also ultimately to handle comparison at this scale more systematically.

In this scene, advanced model-selection tools should all be read as devices that solve different problems. Benchmarks and leaderboards create the comparison board, AutoML automates candidate generation and part of the search, nested cross-validation separates selection and evaluation more strictly, and experiment tracking makes all of those processes explainable again.

The confirmable result appears immediately in whether the record items remain. If the data version, preprocessing rules, hyperparameters, metric, and execution time are all left together, readers can review again why a certain combination was good. But if only the score remains, that comparison is not easily reproducible.

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-3-mermaid-01-en.mmd"
```

## Checklist

- Are AIC/BIC, search techniques, AutoML, and tracking kept from being mixed as if they were solutions at the same level?
- Are you distinguishing whether what is needed now is wider search, stricter validation separation, or better record-keeping?
- Are you looking not only at a high leaderboard score, but also at the comparison conditions and the possibility of keeping records?
- Can you avoid mixing AIC/BIC and hyperparameter tuning as problems at the same level?
- Can you avoid treating benchmark rankings and real generalization performance as immediately identical?
- Can you explain why experiment tracking is not `a convenience feature`, but part of reproducibility?
- Can you explain that AIC/BIC is the language of statistical model selection, while Bayesian optimization and Hyperband are the language of reducing search cost?
- Can you explain that nested cross-validation is the language of making selection and evaluation separation stricter, while AutoML, benchmarks, leaderboards, and experiment tracking are the language of operating experiments at a larger scale?

## Sources And References

- scikit-learn developers, [Tuning the hyper-parameters of an estimator](https://scikit-learn.org/stable/modules/grid_search.html){: target="_blank" rel="noopener noreferrer" }, accessed on 2026-07-01.
- Takuya Akiba et al., [Optuna: A Next-generation Hyperparameter Optimization Framework](https://arxiv.org/abs/1907.10902){: target="_blank" rel="noopener noreferrer" }, accessed on 2026-07-01.
- MLflow, [Tracking](https://mlflow.org/docs/latest/ml/tracking/){: target="_blank" rel="noopener noreferrer" }, accessed on 2026-07-01.
