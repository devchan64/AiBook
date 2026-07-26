# P4-8.1 Model Selection

> Section ID: `P4-8.1`
> Version: `v2026.07.26`

In P4-7, the discussion examined what inputs should remain and what representation those inputs should be changed into. Now it moves to the next question.

What kind of model should those inputs be handed to?

That question is exactly the starting point of [model selection](/AiBook/en/reference/concept-glossary-alpha/m/#model-selection).

Model selection is often understood as `choosing the most famous algorithm`. In practice, it is closer to the opposite. Model selection is the work of narrowing candidates while looking together at the form of the problem, the nature of the data, interpretability, computational cost, and operational conditions.

In academic contexts as well, model selection is not a peripheral choice. In statistics and machine learning, the problem of judging which model to adopt from among several model candidates under observed data and an objective is treated as an independent topic. In other words, model selection is not `a matter of taste about picking an algorithm name`, but the stage that decides `what hypothesis structure should be tested first for the given problem and constraints`.

Model selection is the work of setting up a candidate family of models to test for solving a problem and then narrowing that family into a comparable form.

This Section explains `model selection`, `model candidates`, and `the judgment that narrows candidates by problem form and constraints`. Later Sections continue the current context through this handle, and the criterion for deciding which model drawer should be opened first reconnects through this Section and the [concept glossary](/AiBook/en/reference/concept-glossary/).

The quickest starting point is the following table.

| Problem seen now | First question for the reader | Candidate family to bring to mind first |
| --- | --- | --- |
| [classification](/AiBook/en/reference/concept-glossary-alpha/c/#classification) | `Does it separate two or more classes?` | logistic regression, decision tree, k-NN |
| [regression](/AiBook/en/reference/concept-glossary-alpha/r/#regression) | `Does it predict a continuous value?` | linear regression, tree regression |
| [clustering](/AiBook/en/reference/concept-glossary-alpha/c/#clustering) | `Does it find groups without labels?` | k-means, DBSCAN |

The purpose of this table is not to guess the right answer. It is to help the reader know `which drawer should be opened first` after looking at the problem.

## Questions To Close Before Building A Candidate Family

This Section answers the following questions.

- What is model selection the work of choosing?
- Why is it difficult to handle practical problems by memorizing only one model?
- What model families can be brought to mind first depending on the problem type and data conditions?
- What criteria besides performance enter model selection?

This Section first closes `what model candidates should be built from the problem and constraints`.
The basic role of [cross-validation](/AiBook/en/reference/concept-glossary-alpha/c/#cross-validation) reconnects in P4-4.2 and P4-9.2, while information criteria, AutoML, and large-scale search systems continue in the supplementary learning of P4-9.3 from the perspective of `advanced model selection and automation`.

## Judgments To Keep From Model Selection

- You can explain model selection as `the work of narrowing choices that fit the problem from a set of candidate models`.
- You can say that problem type, data size, feature representation, interpretability, and speed requirements affect model selection.
- You can use the thinking of setting up `a reasonable candidate set` rather than trying to find one correct model.
- You can explain how this connects to the [baseline model](/AiBook/en/reference/concept-glossary-alpha/b/#baseline-model), [hyperparameters](/AiBook/en/reference/concept-glossary-alpha/h/#hyperparameter), and algorithm introduction in the later Sections.

## Learning Background

Part 4 has so far followed the flow below.

- P4-4: how should data be split
- P4-5: why is generalization difficult
- P4-6: what criterion should be used for evaluation
- P4-7: what inputs should remain, and what representation should they be changed into

Only after organizing those points does a condition for `choosing a model` finally appear.

That means model selection is a Section that can be properly handled only after the earlier Sections have been read. If a model is chosen without data splitting, evaluation becomes unstable. If a model is chosen without an evaluation criterion, there is no way to judge what is better. If a model is chosen without feature selection and preprocessing, the choice may not match the input at all.

So in the curriculum, this Section plays the following role.

| Curriculum position | Role of the model-selection Section |
| --- | --- |
| after feature selection and preprocessing | make the reader think about what models fit what input representations |
| before the baseline model | organize candidate families for setting a comparison starting point |
| before the algorithm introduction | provide a large map of where the algorithms that appear later should be used |

In other words, this Section is not `an encyclopedia of algorithms`, but `a topographic map of algorithms`.

From the curriculum perspective, this Section is also the boundary where the flow of Part 4 moves from `handling data fairly` to `deciding what experiment to actually begin`.

- P4-4 examined how data should be split.
- P4-5 examined generalization and overfitting.
- P4-6 examined what should be used as an evaluation criterion.
- P4-7 examined what inputs should remain and how they should be represented.

Only after that does the following question become valid.

`What model families should now be raised as candidates?`

That means model selection is the Section that gathers the results of the previous Sections into `the first choices of experiment design`. That is why this Section serves as the entrance to the later P4-8.2 baseline, P4-9 hyperparameter tuning, and the algorithm-introduction Sections after P4-10.

So model selection is not a Section that appears suddenly. It is the Section that gathers data splitting, generalization, evaluation criteria, and feature design in order to design the next experiment. After that, the flow moves into baseline and tuning to build a comparison structure, and then into the later algorithm chapters.

At this point, the evaluation criteria seen in P4-6 must be carried over unchanged. When setting up a candidate family, the reader should not ask only `who will get the highest score`, but also write down together `what kind of error needs to be reduced`, `which cell in the confusion matrix especially needs to be reduced`, and `what improvement is expected later when compared with the baseline`. Only then are later baseline comparison and tuning results read not as simple score competition, but as `how much the error structure changed`.

The reader should leave the same criteria immediately in candidate notes as well.

| Item to write down now | Why it should be written down together here |
| --- | --- |
| first 2 to 4 candidate models | to reduce the mistake of grabbing one model and tuning it immediately |
| the simplest baseline | to make clear in advance what has to be beaten first in the later Section |
| evaluation metric to look at first | to avoid judging only by one surface score such as accuracy or MAE |
| error scene to inspect | to immediately track problematic cells in the confusion matrix or large-error regions |

That means model-selection notes should not end as `a list of candidate names`. They should also record `the starting point of baseline and error interpretation`.

At this point, the reader naturally asks the next question.

`Then what must be known in order to build a baseline?`

To answer that question, it is more natural not to go deeply into the baseline itself yet, but first to know what must be fixed before setting the baseline. A baseline is not a rule that appears suddenly. It can be built only after `what is being treated as one sample`, `what problem is being solved`, and `what score will be used for comparison` are decided first.

That is why P4-8.1 mentions the baseline in advance: to show that `comparison criteria must also be noted together with candidate-family design`. How the baseline itself is actually built is handed over to the next Section, P4-8.2, as the central question, but the preparation knowledge is more naturally fixed here first.

One more thing makes model-selection notes much stronger. Before writing down candidate models, the reader should also note `what is currently being treated as one sample`, `whether raw logs are being used as they are or a one-action summary table is being used`, and `what baseline recent results will be compared against`. Even the same algorithm name can have a very different meaning in a comparison experiment depending on how the input structure was built.

| What to confirm before writing model candidates | Why it must be confirmed first |
| --- | --- |
| what the sample unit is | because if one row and one case are confused, the evaluation unit also becomes unstable |
| whether to use the raw time series or a one-action summary row | because if the input representation changes, even the same model becomes a completely different experiment |
| what baseline recent results will be compared against | because if only absolute values are seen, the direction of improvement of candidate models is easily misread |
| whether warning and cause confirmation should be distinguished | to avoid exaggerating the interpretation of model output |

That means model selection is the work of opening the algorithm drawer, but before that it is tied to the work of fixing `a comparable data structure`.

The preparation knowledge needed immediately for building the baseline also overlaps here in fact.

| What should be known before the baseline | Why the baseline needs this information first |
| --- | --- |
| whether the problem type is classification or regression | because this determines whether the baseline becomes majority-class prediction or mean/median prediction |
| what one sample is | because if the unit of a row is unstable, what the baseline score is even trying to predict also becomes unstable |
| what evaluation metric will be viewed first | because the interpretation of the baseline changes depending on whether accuracy, recall, or MAE is being watched |
| what the current data distribution is | because to judge what `an easy standard` is, the class imbalance or target distribution must be known |
| what failure is important in operations | because to judge whether barely beating the baseline is actually meaningful, the important error type must be known first |

That means building a baseline does not suddenly require some new advanced theory. It first requires the `problem definition`, `sample unit`, `evaluation metric`, `data distribution`, and `error cost` that have already been organized. Those are exactly the preparations the reader should still be holding at the end of this Section.

In particular, in examples dealing with action-unit raw time series, even the same model name becomes a completely different comparison experiment depending on whether multiple time points are fed in directly or changed into a one-action summary row.

This point ties together once more the flow of Part 3 and P4-7. In Part 3, the reader examined `what one row means` and `why a one-action summary row is needed`. In P4-7, the reader examined what input slots to keep as features in that summary row. Only then does model selection reach the stage of asking `for this input representation, what model family should be tested first`.

That means model selection is not a stage that competes with feature selection. It is a stage that sets up a candidate family on top of an already fixed sample unit and input representation.

The judgments that should be fixed here are the following three.

| What should be nailed down in this Section now | What will be examined in the very next Section | What should remain to the end in actual comparison |
| --- | --- | --- |
| set the first 2 to 4 candidate models | look at what has to be beaten first using the baseline | problematic cells in the confusion matrix, large-error regions, representative failure cases |
| decide which candidate-family drawer should be opened first after seeing the problem | compare whether score increases are real improvements | write down what failure should be reduced more in the next experiment |

Candidate-family notes should be left in the following form so that the comparison criterion becomes less unstable.

| Note item | Example |
| --- | --- |
| sample unit | one action |
| input representation | one-action summary row |
| first candidate family | logistic regression, decision tree, random forest |
| baseline | the simplest rule or majority-class prediction |
| failure to view first | error types that must not be missed, large-error regions |

If notes are written this way, not only model names remain, but also `what kind of experiment is intended to reduce what kind of failure with what kind of input representation`.

It is fine if the baseline item in this table still feels vague. The purpose here is not `how to complete the baseline immediately`, but to first grasp `what materials are needed to build the baseline`. In the next Section, P4-8.2, the reader sees why the baseline is needed first and what the principle of score interpretation is. Then in the following `P4-8.3 supplementary learning`, the reader sees concretely what simple standards can be set first in classification, regression, and time series by using exactly these materials.

## Main Learning Content

### What Is Model Selection The Work Of Choosing?

Academically, model selection is the problem of choosing among candidate models in a way that fits the objective. However, the objective may not be only one thing.

- Is the predictive performance good?
- Does it create less overfitting?
- Is the computational cost manageable?
- Is it easy to explain?
- Is it deployable in the operating environment?

That means model selection is a broader problem than simply `finding a model with high accuracy`.

Put a little more theoretically, what is being chosen here is not simply the name of a program, but a part of the hypothesis space. Whether the reader examines linear models, tree families, or distance-based models is ultimately connected to `what structure is being tried to read from the data`. This Section does not dig into those mathematical details, but focuses on making it possible to distinguish them as `differences in the character of candidate families`.

`Model selection is the work of narrowing model candidates so that they fit the problem and its constraints.`

### Why Should One Not Memorize Only One Model?

Even with the same dataset, if the question changes, the suitable model can change too.

For example, even with customer data, completely different problems can appear as follows.

| Same data | Different question | Model-selection perspective |
| --- | --- | --- |
| customer activity records | will the customer churn next month | classification candidates |
| customer activity records | how much revenue will there be next month | regression candidates |
| customer activity records | can similar customers be grouped together | clustering candidates |

That means model selection starts not from the dataset name, but first from `what kind of prediction or judgment is being attempted`.

The incorrect starting points readers often use also need to be organized together.

- choose the famous algorithm first
- choose the library already used before
- choose the model that looks most complex first

All three of these are `starting from the tool before the problem`. Model selection is the opposite procedure: see the problem first, then narrow tools later.

### Four Questions To Ask Before Model Selection

Here, the order of questions matters more than the algorithm names.

#### 1. What Is The Problem Type?

The very first thing to ask is the problem type.

- is it classification
- is it regression
- is it clustering
- is it closer to ranking or recommendation

If the problem type changes, the candidate family itself changes.

#### 2. How Much Data Are There, And In What Form?

Second comes the size and representation of the data.

- are there many samples or few
- are there many features or few
- are the inputs mostly numeric, or are there many strings and categories
- is the data sparse or dense

For example, the sense of model selection can differ between a case with few samples and many features and a case with very many samples and simple features.

#### 3. Is Interpretability Important?

For some problems, simply getting a correct answer is not enough.

- must the reason for this judgment be explained
- are there regulations or audits
- must people review together

In such cases, an interpretable model can be a better starting point than a more complex model.

#### 4. Are Speed And Operational Constraints Strong?

It also matters whether real-time response is needed, whether inference cost is limited, and whether memory or deployment environments are narrow.

Even if performance is good, it may not be a good choice if service response time is too long or operating cost is not manageable.

### Model Selection Is The Work Of Setting Up A Candidate Family

People often ask:

`So which model is the right answer?`

But the actual starting point of model selection is closer to making `a first shortlist` than to deciding on one correct model.

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-1-mermaid-01-en.mmd"
```

The core of this diagram is that the model does not come first. The problem and constraints come first.

If the practical flow is unfolded a little more, it can be read as follows.

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-1-mermaid-02-en.mmd"
```

This diagram shows model selection not as `algorithm search`, but as `the process of translating a business question into an experimental shortlist`.

### What Model Candidates Should Be Raised First?

The first stage of model selection is not `guessing the best model`, but clarifying `why these candidates should be compared first`.

| Current condition | Candidate family to raise first | Reason |
| --- | --- | --- |
| interpretability matters and the starting point should be simple | linear models, shallow trees | because interpretation and baseline comparison are easy |
| numeric features are relatively organized and the idea of distance matters | review k-NN, SVM | because distance and boundaries among inputs can become directly important |
| nonlinear relationships and interactions should be tested quickly | decision tree, random forest | because complex relationships can be tested relatively quickly |
| the structure should be viewed first without labels | k-means, DBSCAN | because grouping structure and abnormal clusters can be inspected first |
| there are many inputs and operational constraints, so quick baseline comparison comes first | 2 to 4 simple models in a shortlist | because a comparison structure can be set before digging deeply into one model |

This table is not for guessing the correct model. It is a starting table for reasonably narrowing a candidate family based on `problem type`, `input representation`, `interpretability`, and `operational constraints`.

### Candidate Families That Can First Be Brought To Mind By Problem Type

Rather than trying to compare all algorithms at once, the reader should make candidate families that can first be brought to mind by problem type.

| Problem type | Candidate family to bring to mind first |
| --- | --- |
| classification | logistic regression, decision tree, k-NN, SVM |
| regression | linear regression, decision-tree regression, random-forest regression |
| clustering | unsupervised candidates such as k-means and DBSCAN |

This table is not an answer key. It is `a starting point for exploration`.

If it is read together with the baseline in the very next Section, it becomes even clearer as follows.

| Problem scene | Example of a first candidate family | Baseline to write together | Error or comparison point to look at first |
| --- | --- | --- | --- |
| customer-churn classification | logistic regression, decision tree, random forest | always predict `no churn` | the cell where churn customers are missed, change in recall |
| house-price regression | linear regression, tree regression, random-forest regression | predict the average house price | large-money error regions, difference between MAE and RMSE |
| customer-segment clustering | k-means, DBSCAN | none, instead compare with simple rule-based splits and interpretation | density inside clusters, separation between clusters |

The purpose of this table is not to stop at `what model should be chosen`, but to make the reader write at once `what should it be compared against, and what failure should be viewed first`.

Here, baseline comparison is not just adding one more score table. It is the starting point for reading what kind of error structure the recent result actually reduced compared with the existing baseline.

These candidates are handled one after another in the later chapters.

- P4-10 linear regression
- P4-11 logistic regression
- P4-12 k-NN
- P4-13 SVM
- P4-14 decision tree
- P4-15 random forest

That means this Section serves as the entrance to the algorithm Sections that continue from P4-10 to P4-19.

## Detailed Learning Content

### How Do Data Conditions Change Candidate Families?

Even if the problem type is the same, the sense of selection changes when the data conditions change.

| Data condition | Change to think about first |
| --- | --- |
| few features and interpretability matters | start with simple models such as linear models and small trees |
| the concept of distance matters | become more conscious of candidates such as k-NN and SVM |
| nonlinear boundaries seem common | include tree families and kernel-based methods in the candidate set |
| there are many categorical values | review preprocessing burden together with model suitability |
| real-time response matters | review models with fast inference first |

That means model selection is not the superiority of algorithms themselves, but the reading of `the combination of problem and data conditions`.

If this sentence is shortened for the reader, it can be said as follows.

`Model selection is not about finding a good algorithm, but about removing candidates that fit the current problem less well first.`

### Interpretability And Operational Conditions Are Also Selection Criteria

Even with the same performance, in practice different choices can be made for reasons such as the following.

| Criterion | Why a simpler model can have an advantage |
| --- | --- |
| interpretability | results are easier to explain and review |
| debugging | when a strange prediction appears, tracing it is easier |
| operational cost | inference cost and memory usage can be smaller |
| deployment simplicity | the pipeline and model structure are simple, so management is easier |

That means model selection does not end in one line of a performance table.

## Cases And Examples

### Case 1. Even For The Same Churn Prediction, The First Candidate Family Can Differ

A subscription-service team is preparing customer-churn prediction. The criteria people first used were behavioral signals such as `recent visit count`, `number of inquiries`, `whether payment failed`, and `plan-change history`.

In the first meeting, some people say `let's use strong modern models first`, while others say `we need a model that is easy to explain`. The data are tabular, prediction once per day in a batch is enough, and the operations team wants some explanation for why a certain customer was judged risky. Under these conditions, rather than choosing one correct model from the start, it is more reasonable to raise an explainable linear model, a rule-based model, and a stronger nonlinear candidate together.

In this scene, model selection becomes not `choosing a famous algorithm`, but `translating the problem and constraints into a candidate family`. Conditions such as whether it is a classification problem, whether the data are tabular, whether explanation is needed, and whether inference is not real-time become the criteria that narrow the candidate family. That is why it is more reasonable to first set up two or three models with different characters, such as logistic regression, decision tree, and random forest.

The confirmable results appear in the candidate-family table and comparison experiments. If the reader compares side by side which model offers interpretability, which handles nonlinear patterns better, and which can bear the operational cost, the reader can explain why `candidate-family design` is the first stage of model selection.

If this scene is drawn as a diagram, it becomes visible at a glance how even the same churn-prediction problem splits into different candidate families because of constraints.

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-1-mermaid-03-en.mmd"
```

### Setting Up Model Candidates Through A Small Example

Consider the following problem.

| Condition | Content |
| --- | --- |
| problem | customer-churn prediction |
| input | recent visit count, inquiry count, payment amount, membership tier |
| target | classify whether churn will occur next month |
| constraint | results should be explainable to some degree |
| operation | daily batch prediction, not real-time |

In this case, at the introductory level the candidate family can be set up as follows.

| Candidate | Why it is a candidate |
| --- | --- |
| logistic regression | good for interpretation and setting a baseline |
| decision tree | can inspect nonlinear rules intuitively |
| random forest | can become a stronger performance candidate |

By contrast, fixing one very complex model from the beginning can make the comparison criterion disappear.

## Practice And Examples

### Practice 1. Rewrite A Problem Scene Into A Candidate-Family Memo

Look at the three scenes below and write at least the following five items for each scene.

- problem type
- sample unit
- first 2 to 4 candidate models
- baseline to note together
- error or comparison point to inspect first

| Scene | Memo the reader should write first |
| --- | --- |
| An online store wants to find `orders likely to be returned next week` in advance. The inputs are order amount, whether shipping was delayed, category, and previous return count. The operations team wants some explanation for why an order looks risky. | problem type / sample unit / first candidate family / baseline / error to inspect first |
| A real-estate team wants to estimate `the expected apartment transaction price`. The inputs are area, number of rooms, year built, and distance to the nearest station. Interpretability matters, but reducing large-money errors matters more. | problem type / sample unit / first candidate family / baseline / error to inspect first |
| A logistics team wants to inspect `groups of regions with similar delivery patterns` first. The inputs are average delivery time, redelivery rate, and order density. There are no labels yet, and the goal is to inspect structure first. | problem type / sample unit / first candidate family / baseline substitute comparison / comparison point to inspect first |

Compare what you wrote with the explanation below and check not only `whether you wrote candidate names`, but also whether you wrote `why those candidates should be compared first` and `what they should be compared against`.

| Scene | Example explanation |
| --- | --- |
| finding risky return orders | classification, sample unit is one order, candidate family is logistic regression, decision tree, random forest, baseline is always predict `no return`, and the first error to inspect is the cell where actual return orders are missed and recall |
| estimating apartment transaction price | regression, sample unit is one apartment transaction, candidate family is linear regression, tree regression, random-forest regression, baseline is predicting the average transaction price, and the first comparison point is large-money error regions and the MAE/RMSE difference |
| grouping regions with similar delivery patterns | clustering, sample unit is one region, candidate family is k-means and DBSCAN, instead of a separate baseline compare with simple rule-based splits and interpretation, and inspect density inside clusters and separation between clusters first |

The core of this practice is to write once by hand the order `problem type -> sample unit -> candidate family -> baseline -> failure to inspect first`. Without writing this order, it is easy to misunderstand model selection again as `choosing a famous algorithm name`.

### Practice 2. Explain In Words Which Candidate Should Be Removed First

Model selection is closer to `removing candidates that fit the current problem less well first` than to `guessing the one best algorithm`. In the scenes below, explain in one or two sentences why some candidates should be raised first and why others should be delayed.

| Scene | Question the reader should answer first |
| --- | --- |
| It is a tabular-data classification problem, people must review the basis for predictions, and batch inference once per day is enough. | Why can logistic regression or a shallow tree be raised first? |
| The distance concept between features matters, and similar cases are expected to lead to similar judgments. | Why can k-NN or SVM be kept more actively in the candidate family? |
| Real-time response is very important and deployment memory is small. | Why should candidates with simpler inference be reviewed before more complex ones? |

The following short explanations are enough to hold on to.

- If explanation and review matter, raise candidates that are easier to interpret first so that the difference from the baseline can be read more easily.
- When the distance concept matters, distance-based candidates deserve more attention because closeness between inputs can itself become a judgment criterion.
- When operational constraints are large, not only the possibility of a high score but also inference cost and deployment simplicity become criteria for reducing candidates.

### Example. Compare A Bad Candidate Memo With A Better Candidate Memo

The two memos below were written for the same problem scene.

Problem scene:

- The task is to classify `whether a card transaction is fraudulent`.
- The inputs are transaction amount, country, time band, past fraud history, and device information.
- Missing fraud causes large losses, and the operations team wants to see some basis for the risk judgment as well.

Memo A:

| Item | Content |
| --- | --- |
| candidate | XGBoost only |
| reason | I heard it performs well |

Memo B:

| Item | Content |
| --- | --- |
| problem type | classification |
| sample unit | one transaction |
| first candidate family | logistic regression, decision tree, random forest |
| baseline | always predict `normal transaction` |
| first error to inspect | the cell where actual fraudulent transactions are missed, change in recall |
| extra memo | because explanation and operational review matter, include interpretable candidates in the first comparison group |

Answer the following for yourself first.

- Which memo is closer to model selection?
- Why does the other memo still remain at `choosing a famous model name` rather than `candidate-family design`?
- If you wanted to add one more note before later comparison even in Memo B, what would it be?

The explanation can be read as follows.

- Memo B is better. It connects model selection to `problem type`, `sample unit`, `comparison candidates`, `baseline`, and `the error to inspect first`.
- Memo A fixes only one candidate and leaves out what it should be compared against and what failure it should reduce, so it does not continue naturally into the baseline comparison of later Sections.
- Items that can still be added to Memo B are input representation, degree of data imbalance, and the failure types that are operationally hardest to accept.

The purpose of this comparison example is not to find `a good candidate name`, but to let the reader distinguish what `a good candidate memo` is.

If the same candidate-family memo is reduced to an actual comparison procedure, it can look like this. The code below raises logistic regression, k-NN, decision tree, and random forest on the same classification data, then compares train score, CV score, and the fluctuation of CV score with 5-fold cross-validation.

Values to change:

- Change `class_sep=0.9` and `flip_y=0.06`; the data become easier to separate or more mixed, so the CV score and fluctuation can change by candidate.
- Change `n_neighbors=7`, `max_depth=4`, and `n_estimators=80`; each candidate model's complexity and train/CV score gap will change.

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=240,
    n_features=10,
    n_informative=4,
    n_redundant=2,
    class_sep=0.9,
    flip_y=0.06,
    random_state=42,
)

models = {
    "logistic_regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "knn_scaled": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7)),
    "decision_tree": DecisionTreeClassifier(max_depth=4, random_state=0),
    "random_forest": RandomForestClassifier(n_estimators=80, max_depth=5, random_state=0),
}

for name, model in models.items():
    scores = cross_validate(model, X, y, cv=5, scoring="accuracy", return_train_score=True)
    print(
        name,
        "train=", round(scores["train_score"].mean(), 3),
        "cv=", round(scores["test_score"].mean(), 3),
        "spread=", round(scores["test_score"].std(), 3),
    )
```

An example output is as follows.

```text
logistic_regression train= 0.706 cv= 0.688 spread= 0.053
knn_scaled train= 0.819 cv= 0.725 spread= 0.04
decision_tree train= 0.902 cv= 0.762 spread= 0.028
random_forest train= 0.984 cv= 0.796 spread= 0.048
```

This output shows the difference between `choosing one famous model` and `comparing a candidate family`. Random forest has the highest CV score on this small data, but its training score is also very high. The decision tree is lower, but its fluctuation is smaller. Logistic regression is simple and easier to explain, but its score is lower on this data. Therefore, a model-selection memo should leave not only the score, but also the candidate family, comparison method, fluctuation, and interpretability axes.

### Practice 3. Check Whether The Memo Changes When The First Error To Inspect Changes

The two scenes below are both classification problems, and the first candidate family can start similarly. But if the first error to inspect is different, the model-selection memo should also change.

| Scene | How should the first error to inspect be written? |
| --- | --- |
| In hospital intake, `not missing high-risk patients` matters more. | Write which cell especially has to be reduced. |
| In an ad-recommendation system, `showing too much to uninterested people` is the bigger problem. | Write which false-positive judgment should be reduced. |

After writing your own answer, compare it with the explanation below.

| Scene | Example explanation |
| --- | --- |
| high-risk-patient classification | Because [false negatives](/AiBook/en/reference/concept-glossary-alpha/f/#false-negative) that miss actual high-risk patients should be reduced first, it is appropriate to note that [recall](/AiBook/en/reference/concept-glossary-alpha/r/#recall) and missed cases should be examined first. |
| ad-recommendation classification | Because [false positives](/AiBook/en/reference/concept-glossary-alpha/f/#false-positive) that wrongly judge uninterested people as positive should be reduced first, it is appropriate to note that [precision](/AiBook/en/reference/concept-glossary-alpha/p/#precision)-side errors and overexposure cases should be examined first. |

This practice is meant to hold on to the point that `writing the candidate family is not the end`. Even with the same candidate family, the comparison memo changes depending on which failure should be reduced first.

## Checklist

- Are you fixing the problem type first and then building the candidate family?
- Are you comparing candidates only after writing the sample unit and the input representation?
- Before tuning only one model immediately, are you leaving a shortlist of about 2 to 4 models to compare?
- Are you noting not only candidate model names but also the baseline and the error scene to inspect first?
- Is the current problem classification, regression, or clustering?
- Have you considered the input representation and the scale of the data?
- Have you included interpretability and operational constraints in the criteria?
- Are you ready to set up and compare at least two or three candidate families?
- Are you still holding on to only one complex model without a baseline?
- Can you explain that model selection is not about naming one correct algorithm, but about setting up a reasonable candidate family while looking together at problem type, data conditions, interpretability, and operational constraints?

## Sources And References

- Jie Ding, Vahid Tarokh, Yuhong Yang, `Model Selection Techniques -- An Overview`, arXiv, 2018, accessed 2026-07-26. [https://arxiv.org/abs/1810.09583](https://arxiv.org/abs/1810.09583){: target="_blank" rel="noopener noreferrer" }
- Sebastian Raschka, `Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning`, arXiv, 2018, accessed 2026-07-26. [https://arxiv.org/abs/1811.12808](https://arxiv.org/abs/1811.12808){: target="_blank" rel="noopener noreferrer" }
