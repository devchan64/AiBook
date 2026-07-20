# P4-15.3 OOB(Out-Of-Bag) And Checking Random Forest

> Section ID: `P4-15.3`
> Version: `v2026.07.20`

In P4-15.1, we saw why random forest can create more stable predictions by gathering many trees. In P4-15.2, we saw how to read carefully what that forest considered important, namely feature importance.

Then the next remaining question is this:

How can we check whether this forest is actually learning in a reasonable way?

In random forest, one of the first handles that appears for that question is OOB(out-of-bag).

OOB is an internal validation-like method in which random forest uses samples that were not drawn into a bootstrap sample and performs a rough self-check while training.

So OOB is not `a new model`. It is a way to read and inspect a random forest.

This Section also does not repeat the basic structure of random forest at length. The core intuition reconnects through P4-15.1 and the [concept glossary](/AiBook/reference/concept-glossary/), and here we focus only on how bootstrap and OOB connect as an inspection device.

## Scope Of This Section

This Section answers the following questions.

- Why does OOB(out-of-bag) appear?
- What is the relationship between bootstrap and OOB?
- What does `oob_score=True` mean?
- How is an OOB score different from train accuracy, validation score, and test score?
- How far should OOB be trusted, and where should we stop?

The outer boundary of OOB only needs to be fixed to about the following.

| Item | Recovery state in the current main text |
| --- | --- |
| every variant of cross-validation | the basic role of cross-validation reconnects in P4-9.1 and P4-9.3, but this Section does not replace a full explanation of every variant |
| calibration and threshold adjustment | the basic feel for threshold and calibration reconnects in P4-6.4 and P4-11.1, but this Section does not unfold those details together with OOB |
| the OOB character of gradient boosting | the checking feel of boosting reconnects in P4-16.1 and P4-16.2 through validation and early stopping, but this Section does not treat the detailed contrast at length |

In other words, this Section focuses on fixing OOB in place as `the internal inspection board of random forest`, while broader evaluation procedures and score-operating policy are better reread later by question.

## Goals Of This Section

- You can explain OOB as `an internal generalization estimate using samples left out by bootstrap`.
- You can explain why OOB is possible only when `bootstrap=True`.
- You can explain why it is dangerous to declare an OOB score and a test score to be the same thing.
- You can gain a basic attitude of reading `train / OOB / test` together in random-forest experiments.

## Why This Section Is Needed

When readers first use random forest, they often go through this sequence.

1. The training goes well.
2. The train accuracy comes out high.
3. Then the model feels good enough.

But there is a large blank inside that sequence.

`Fitting the training data well` and `working well on unseen data` can be different things.

Because random forest uses bootstrap, `samples that this tree did not see` appear during training. OOB makes use of exactly that gap.

So 15.3 is not a Section about `how to believe one score produced by the forest`. It is a Section about `how to inspect the state of the forest through several scores`.

## Why Does OOB Appear?

The scikit-learn User Guide explains that in random forest, each tree is built from a bootstrap sample drawn with replacement. With sampling like that, some samples can enter one tree multiple times, while some samples can be left out entirely from that tree's training.

Those left-out samples are exactly the out-of-bag samples.

It can be read like this.

- one tree does not see the full training set
- so `training samples that the tree did not see` appear
- those samples can be used to partially inspect that tree

So OOB is a by-product created by bootstrap, and random forest reuses that by-product as an inspection resource.

## The Relationship Between Bootstrap And OOB

Drawn in one scene, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-01-en.mmd"
```

The key point in this figure is that OOB is not `a completely separate additional dataset`. It is still inside the training set. What matters is that, from the viewpoint of a particular tree, it was `an unseen sample`.

## What Does `oob_score=True` Mean?

The scikit-learn API documentation explains `oob_score` as an option that decides whether to estimate a generalization score using out-of-bag samples. It also explains that this feature is available only when `bootstrap=True`.

- `bootstrap=True`: each tree is trained on a bootstrap sample
- `oob_score=True`: gather the left-out samples and calculate an internal inspection score

So OOB does not exist without bootstrap. If every tree always sees the whole dataset, then the idea of `an unseen sample` disappears.

## What Kind Of Score Is OOB?

The API documentation describes `oob_score_` as the score obtained from an out-of-bag estimate on the training dataset.

There are two things readers should be careful about here.

1. OOB is not a score on a completely new dataset outside the training data.
2. But it is not just plain train accuracy either.

So OOB sits between them as `an internal generalization estimate`.

| Score | What it is based on |
| --- | --- |
| train accuracy | how well the model fits data that were directly used in training |
| OOB score | how well each sample is predicted by trees that did not see it |
| test score | how well the model works on a separately held-out dataset |

That is why OOB can feel more realistic than train score, but it is still dangerous to claim that it fully replaces the test score.

Compressed into score patterns:

| Score pattern | First interpretation to recall | Immediate next question |
| --- | --- | --- |
| only train is very high | it may be fitting the training data too much | are OOB and test also high? |
| train is high and OOB/test follow at a similar level | the forest may look relatively stable across internal and separate checking | what kinds of remaining error cases are left? |
| train, OOB, and test are all low | the bottleneck may be feature representation or data quality rather than the forest itself | should the feature representation be revisited? |

So the core of the OOB Section is not `one score`, but `a combination of scores`.

## Why Does OOB Feel Convenient?

The scikit-learn documents and examples explain that OOB error lets readers obtain a validation-like estimate while training a random forest.

That is very practical in early-stage experimentation.

- small experiments can be repeated quickly
- it reduces the mistake of looking only at the train score
- it helps check quickly how the state changes when the number of trees(`n_estimators`) increases

So OOB is closer to `a quick internal inspection board` than to `the final destination of evaluation`.

## Is OOB Alone Enough, Then?

We need to stop once here.

`No. Usually OOB alone is not enough.`

The reason is simple.

- OOB is an internal estimate that depends on the bootstrap structure
- it is not under exactly the same conditions as genuinely new deployment-time data
- when the data are small, the classes are imbalanced, or the metric is sensitive, held-out validation/test scores still matter

The role of OOB can be separated like this.

| Situation | Role of OOB |
| --- | --- |
| early quick experiments | very useful internal inspection |
| rough hyperparameter search | a useful reference indicator |
| final performance report | should be read together with test/validation |
| final judgment before deployment | should not end with OOB alone |

### When Can OOB Be Especially Useful?

OOB does not replace every evaluation, but it becomes a very practical internal inspection board in the early stage of random-forest experiments.

| Current situation | Why OOB is especially useful | What to check together |
| --- | --- | --- |
| you want to compare several forest settings quickly | because an internal inspection score is obtained together inside bootstrap | whether test is being kept for final confirmation |
| the train score is so high that it feels suspicious | because OOB gives a less optimistic estimate than train | the gap between OOB and test |
| you are deciding whether to increase `n_estimators` | because internal stability can be inspected quickly as the number of trees changes | the improvement relative to computation cost |
| it is a small experiment where using a large validation set is hard | because it gives an extra checking signal without another split | whether OOB is being mistaken for the final reporting score |
| you want to see whether a bootstrap-based forest is behaving properly | because internal state can be inspected through predictions on unseen-per-tree samples | whether `bootstrap=True` is actually set |

The point of this table is to position OOB correctly not as `the final truth`, but as `a quick internal state-inspection board`.

## Why Read Train / OOB / Test Together?

In random-forest inspection, it is important to place those three numbers side by side.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-02-en.mmd"
```

For example:

- if train is very high but OOB and test are much lower, overfitting can be suspected
- if train, OOB, and test are all similarly low, weak representation or data limits can be suspected
- if train is high and OOB/test follow at similar levels, the forest can be read as comparatively stable

The core of this Section is not one particular number. It is `the gaps among the numbers`.

## Python Example: Inspect An OOB Score

This example is a small exercise that prints train / OOB / test together on the breast-cancer classification dataset.

- problem situation: inspect whether random forest fits the training data well and whether internal checking and separate test move similarly
- input: 30 continuous features
- label: malignant / benign class
- concepts to check:
- OOB is read through `oob_score_` - OOB plays an internal inspection role between train and test - the gaps among the three scores should be read together

```python
# This example prints train, OOB, and test scores together on breast-cancer classification to read their gaps.
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    bootstrap=True,
    oob_score=True,
    random_state=42
)
model.fit(X_train, y_train)

print("train accuracy:", round(model.score(X_train, y_train), 3))
print("oob score     :", round(model.oob_score_, 3))
print("test accuracy :", round(model.score(X_test, y_test), 3))
print("n_estimators  :", model.n_estimators)
```

An example output can look like this. The exact values can change a little depending on the split, library version, and random setting.

```text
train accuracy: 1.0
oob score     : 0.96
test accuracy : 0.947
n_estimators  : 300
```

The reading order is as follows.

1. Because the train accuracy is 1.0, the forest explained the training set very well.
2. But reading only train can be too optimistic.
3. Because OOB 0.96 and test 0.947 do not diverge greatly, this experiment gives a signal that the forest did not learn only an illusion.

Of course, that alone does not prove the model is good enough. But OOB is very useful because it prevents readers from immediately trusting the number `train 1.0`.

## Python Example: Inspect How OOB Looks As The Number Of Trees Grows

This example changes `n_estimators` and inspects how OOB and test move together.

Problem situation:

- in random forest, readers need practice in seeing how OOB and test move together as the number of trees increases

Input:

- breast-cancer dataset `X`, `y`
- several values of `n_trees`

Expected output:

- OOB score by number of trees
- test score by number of trees

Concepts to check:

- as the number of trees grows, OOB often moves toward a more stable level
- simply increasing the number of trees does not solve every problem

```python
# This example changes n_estimators to compare how OOB and test scores move.
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for n_trees in [10, 50, 100, 300]:
    model = RandomForestClassifier(
        n_estimators=n_trees,
        bootstrap=True,
        oob_score=True,
        random_state=42
    )
    model.fit(X_train, y_train)

    print(
        f"trees={n_trees:3d} | "
        f"oob={model.oob_score_:.3f} | "
        f"test={model.score(X_test, y_test):.3f}"
    )
```

An example output can look like this. The exact values can change a little depending on the split, library version, and random setting.

```text
trees= 10 | oob=0.942 | test=0.947
trees= 50 | oob=0.957 | test=0.947
trees=100 | oob=0.960 | test=0.947
trees=300 | oob=0.960 | test=0.947
```

What the reader should read here is:

- when the number of trees is too small, OOB can fluctuate somewhat
- after a certain point, OOB can begin to look stable
- but because the test score can stay at a similar level, readers should not conclude that `performance keeps rising as trees keep increasing`

So OOB can help inspect `about when the forest becomes roughly stable`, but it is not itself a performance guarantee.

At this point, it also helps to immediately organize not only the score, but what comparison criteria and what remaining cases should be written down together. Even when OOB or test looks similar as a number, the types of repeatedly remaining errors can still differ. So score patterns and case patterns should be read together.

| Item to keep together | What is written in this Section | Why it is needed |
| --- | --- | --- |
| internal comparison criterion | the gap among train / OOB / test | to see how much training fit and generalization estimate are separated |
| remaining review cases | samples repeatedly wrong in OOB and test | to decide whether to enlarge the forest or revisit feature representation |
| next validation question | whether to change the number of trees, depth, or representation first | to pass score interpretation into the next experiment order |

## Frequent Misunderstandings When Interpreting OOB

The following misunderstandings appear especially often.

| Misunderstanding | Safer interpretation |
| --- | --- |
| OOB is high, so it is ready for deployment | OOB is only an internal inspection signal; final verification is still needed |
| OOB looks similar to test here, so they are always the same | they were only similar in this experiment |
| if OOB exists, a validation split is unnecessary | depending on the situation, it is still necessary |
| if OOB is low, random forest is useless | data quality, feature representation, and hyperparameters must be checked together |

What matters is `an attitude that neither underestimates nor overestimates OOB`.

### If OOB And Test Diverge, What Should Be Suspected First?

Beginners often feel that OOB and test should look similar if everything is normal. But a small difference itself is not strange. What matters more is not to rush into a hard conclusion about why they differ.

| Visible scene | What to suspect first | Why |
| --- | --- | --- |
| OOB looks okay but test is lower | hold-out split difference, representativeness difference | because OOB is an internal estimate while test is a separately held-out sample |
| OOB is lower but test is slightly higher | fluctuation in the bootstrap-based internal estimate, small data size | because OOB can look more conservative in some experiments |
| both are unstable | too little data, class imbalance, weak feature representation | because the data state can be the first problem before the forest structure |

What matters here is not to choose immediately `which one is the truth`. It is to inspect whether the pattern remains under repeated experiments, whether the remaining error cases are similar, and whether the split lost too much representativeness.

## Cases And Examples

### Case 1. When Train Looks Perfect But You Want To Check Quickly Whether The Forest Is Really Fine

A fraud-detection team trains a random forest, and the train accuracy comes out almost perfect. The human-first criteria were signals like `repeated payments in a short time`, `a strange region`, and `late-night transactions`.

If readers look only at that high train score, the model can feel good enough already. But the team has already learned from decision trees that `fitting the training data well` and `fitting new data well` can be different. Because bootstrap creates samples that each tree did not see, the team uses an OOB score as an internal check.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-03-en.mmd"
```

In this scene, OOB should be read not as `the final performance score`, but as `an internal generalization estimate`. If train is high but OOB and test are both low, then overfitting or a representation problem should still be suspected. If train, OOB, and test move together without a large gap, the forest can be read as comparatively stable. In other words, what matters is not one number, but the gaps among the numbers.

The verifiable result appears when train / OOB / test are inspected side by side. If OOB is much lower than train, it prevents an overly optimistic reading. If OOB and test move similarly, it becomes a useful handle for checking the state of the forest quickly.

Compressed into memo form, the case can be written like this.

| Observed score pattern | Interpretation to attach immediately | Review cases to keep | Next question |
| --- | --- | --- | --- |
| train is very high while OOB/test are lower | the forest may be fitting the training data too much | repeated error transaction types, rare patterns, class-imbalance cases | should depth be reduced first, or should feature representation be redesigned? |
| train, OOB, and test follow at similar levels | the current forest looks comparatively stable under internal and separate checking | remaining false positives / false negatives | can readers move on to threshold or importance interpretation? |

### Case 2. When OOB Looks Fine But Test Is Lower Than Expected

Suppose a quality-inspection team trains a random forest for defect detection. Train is high, and OOB also looks fairly good. It is easy to feel: `isn't this enough already?` But the separately held-out test can still come out lower than expected.

In this scene, the easiest judgment is `OOB was wrong` or `test was accidentally bad`. But the safer interpretation is not to discard either one immediately. It is to ask first `why did the internal estimate and the separate validation diverge?` Readers should revisit whether one time period was concentrated more heavily in the test split, whether rare defect types entered the hold-out side more often, or whether the current feature representation misses certain patterns.

So when OOB and test diverge, the core is not `choosing one of them as the answer immediately`. It is using the gap to decide `in what data scene did the difference become larger` and what the next experiment order should be. At that point, it can be safer to revisit the split, the repeated error cases, and the feature representation before simply enlarging the forest.

## How Is It Used In Practice?

Rewritten as a practical flow, OOB is usually read like this.

1. Train a random forest quickly as a baseline model.
2. Look at the train score and the OOB score together.
3. Do not stop after seeing only an optimistic train score.
4. If needed, check again through validation/test.
5. Only then move on to interpretation or adjustment such as feature importance or threshold.

So OOB is a device that corrects `the order of inspection`.

The result of this Section can also be arranged immediately in the same retrospective structure.

| Question to leave in Part 4 | Language in a Part 6 retrospective note |
| --- | --- |
| what were train / OOB / test? | fact |
| what do the gaps suggest among overfitting, stability, and weak representation? | interpretation |
| in the next experiment, what should be revisited first: number of trees, features, or validation setup? | next question |

For example, if only train is high while OOB is low, the current forest may be fitting the training data too optimistically. Then depth, feature representation, and validation separation should be revisited first. Conversely, if OOB and test are both low together, feature representation or data quality may need to be revisited before the forest itself. Only when that level of judgment is attached does OOB become a guide for the next experiment order rather than a score explanation alone.

This Section stops once more to distinguish `what should be changed right now` from `what judgment should still be postponed`.

| Signal that appeared first | Meaning to read right now | Immediate next action | Judgment not to rush at this stage |
| --- | --- | --- | --- |
| only train is high while OOB/test are lower | the forest may fit training data too well | revisit depth, minimum samples, feature representation, and validation split first | do not change threshold or service policy first |
| train, OOB, and test are all low | feature representation or data quality may be a bigger bottleneck than the forest itself | revisit feature design, missing variables, data quality, and gain over the baseline | do not keep trying to solve it only by increasing the number of trees |
| OOB and test follow at similar levels | the current forest looks similar under internal and separate checking | from here, move on to feature importance, threshold, or later ensemble comparison | do not finish the final deployment judgment from OOB alone |

So the core of the OOB Section is not only `what is the score`, but `with this score pattern, what should be changed next and what should still be postponed?`

### The Minimum Experiment Memo To Leave After Reading OOB

If OOB is written down as only one number, its meaning quickly becomes blurry. It is better to leave at least the following four lines together.

| Item | Example note |
| --- | --- |
| observed scores | `train=1.00, OOB=0.96, test=0.947` |
| first interpretation | `there is a gap from train to OOB/test, but the forest is not fully collapsing` |
| review cases | `revisit rare defect types and repeated false-positive cases` |
| next action | `revisit feature representation and validation separation before only increasing the number of trees` |

With that memo, the OOB Section becomes not only a score introduction but an experiment record that leaves the order of the next adjustment.

The next scene after this Section is gradient boosting. If random forest was `a way of reducing instability by gathering many trees in parallel`, then the next boosting chapter in P4-16 moves to `a way in which the next tree corrects the previous error sequentially`.

## Checklist

- Are you reading OOB as if it were the same thing as a test score?
- Can you explain that OOB is possible only when `bootstrap=True`?
- Are you reading the gaps among train / OOB / test together?
- Can you explain OOB as an internal checking method that uses samples left out by bootstrap?
- Can you explain that `oob_score=True` is meaningful only in bootstrap-based random forest, and that OOB can feel more realistic than the train score without fully replacing the test score?
- Do you know that in checking random forest, it matters to read `train / OOB / test` together, and that OOB is useful as a handle for quick experiments but not the sole evidence for final deployment judgment?

## Sources And References

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
