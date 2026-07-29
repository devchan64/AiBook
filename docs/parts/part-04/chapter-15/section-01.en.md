# P4-15.1 Random Forest

> Section ID: `P4-15.1`
> Version: `v2026.07.26`

In P4-14, we saw why a [decision tree](/AiBook/en/reference/concept-glossary-alpha/d/#decision-tree) can feel intuitive while also falling into [overfitting](/AiBook/en/reference/concept-glossary-alpha/o/#overfitting) rather easily. In particular, we confirmed that even after changing `max_depth`, `min_samples_leaf`, and `ccp_alpha`, the structural instability of a single tree may not disappear completely. That leads to the next question.

How can we keep the strengths of trees while reducing the excessive instability of a single tree?

That question is the starting point of the [random forest](/AiBook/en/reference/concept-glossary-alpha/r/#random-forest).

Random forest is a model that gathers predictions from many decision trees trained a little differently and tries to produce a more stable judgment than a single tree.

In other words, random forest is not `a model that throws trees away`, but `a model that gathers many trees and reduces their weaknesses`.

This Section explains the basic meanings of [random forest](/AiBook/en/reference/concept-glossary-alpha/r/#random-forest), [ensemble](/AiBook/en/reference/concept-glossary-alpha/e/#ensemble), [bootstrap](/AiBook/en/reference/concept-glossary-alpha/b/#bootstrap), and random feature selection. The later Sections continue the judgment handles built here, and the basic sense of reducing instability through agreement among many trees reconnects through this Section and the matching glossary entries.

## Questions Closed By Random Forest

This Section answers the following questions.

- Why does random forest use many trees?
- What roles do [bootstrap](/AiBook/en/reference/concept-glossary-alpha/b/#bootstrap), [max_features](/AiBook/en/reference/concept-glossary-alpha/m/#max-features), and `averaging` play?
- Why can it look more stable than a single tree?
- How does random forest combine predictions in classification and regression?
- What do [n_estimators](/AiBook/en/reference/concept-glossary-alpha/n/#n-estimators), [max_features](/AiBook/en/reference/concept-glossary-alpha/m/#max-features), [bootstrap](/AiBook/en/reference/concept-glossary-alpha/b/#bootstrap), and [oob_score](/AiBook/en/reference/concept-glossary-alpha/o/#oob-score) mean?

This Section first closes the question `why gathering many trees tries to make a more stable judgment than one tree`. Feature importance continues in P4-15.2, the evaluation reading of the OOB(out-of-bag) score continues in P4-15.3, the Extra Trees comparison continues in the supplementary Section P4-15.4, and the contrast with gradient boosting continues in P4-16.1 and P4-16.2.

## Judgments To Keep From Random Forest

- You can explain random forest as `an average / aggregation model of many randomized trees`.
- You can explain why bootstrap sampling and random feature selection are needed.
- You can understand that random forest is an attempt to reduce the variance of decision trees.
- You can distinguish the roles of representative hyperparameters at an introductory level.

## Learning Background

By the time readers reach the decision-tree chapter, they usually hold two feelings at once.

- what felt good: it is easy to read and seems to fit tabular data well
- what feels uneasy: once the tree gets deeper, it seems to memorize too much

Random forest appears exactly on top of that tension.

| Question left from Chapter 14 | Direction that 15.1 answers |
| --- | --- |
| What should we do if one tree is unstable? | Gather many trees and average the instability |
| Can we reduce branches that are pulled by exceptions? | Make each tree different so their errors are less tied together |
| Do we lose interpretability completely? | We lose some, but often gain stability and performance |

So random forest does not `deny the weaknesses of the decision tree`. It works by `softening those weaknesses through an ensemble structure of many trees`.

If we add one more point here, this Section connects directly to the comparison-record structure that Part 4 has been building. When random forest is raised as a candidate, it is not enough to leave only the sentence `it uses many trees`. It also helps to record `which error cases become less unstable than under a single tree`, `which ambiguous cases still remain`, and `which forest setting should be checked next`. Even when average scores look similar, we still have to read separately which model repeats a particular error type more often, and which model stays more stable when the seed changes.

| Record to keep together | Why it matters |
| --- | --- |
| single tree vs. random forest | to see what the ensemble actually stabilizes |
| remaining error cases | to revisit cases that remain wrong or ambiguous even after gathering many trees |
| whether instability decreased | to see whether average stability improved, not only one high score |
| next experiment question | to decide whether to adjust `n_estimators`, `max_features`, or `bootstrap` next |

The shift in questions inside the tree family can be summarized like this.

| Model | First question to hold onto | Criterion to emphasize more strongly |
| --- | --- | --- |
| decision tree | In what question order should we split the data? | readable branching structure and leaf rules |
| random forest | How can we reduce the instability of one tree? | diversity among many trees and average stability |
| gradient boosting | How does the next stage correct the previous stage's errors? | sequential correction and residual reduction |

So for random forest, the core is not `it uses more trees`, but `it gathers and reduces the instability of different trees`. Once that criterion is fixed, the later gradient boosting chapter can also be read not as just another ensemble name, but as a contrast between `a stability-centered ensemble` and `an error-correction-centered ensemble`.

### When It Is Good To Raise Random Forest Early

Random forest is especially strong when you want a more stable default candidate on tabular data even if you give up some of the interpretability of a single tree.

| Current problem state | Why raise random forest early | What to check first |
| --- | --- | --- |
| A single tree changes too often | because averaging many trees can reduce variance | how much the score changes across seeds or splits |
| You need a strong default candidate on tabular data | because it can keep the strengths of tree models while gaining stability | whether depth and leaf size are already under control |
| You suspect nonlinear patterns that a linear model misses | because a tree ensemble can hold more complex branching structure flexibly | whether overfitting and computational cost are being checked together |
| You need a stronger baseline before interpretability | because it often gives a less sensitive default performance than a single tree | what error cases still remain |
| You want to inspect importance or OOB later too | because the tree family comes with internal inspection handles | whether importance and OOB are not being overtrusted |

The point of this table is to read random forest not as `using many trees`, but as `a stability candidate that reduces the instability of a single tree`.

## Main Learning Content

### The Large Frame Called Ensemble

The scikit-learn User Guide explains ensemble methods as methods that combine predictions from multiple base estimators in order to achieve better generalizability and robustness than a single estimator.

Random forest is one representative example inside that ensemble family, using many trees.

Random forest is an ensemble method that gathers judgments from many slightly different trees and tries to produce a more stable answer.

`Instead of trusting the judgment of one model as it is, gather the judgments of several slightly different models and make the answer more stable.`

Once you see that large frame, it becomes clearer why random forest appeared.

### What Kind Of Model Is Random Forest?

The scikit-learn documentation explains random forests as `an averaging algorithm based on decision trees`. Each tree is trained on a bootstrap sample drawn with replacement from the training set, and at each split only a random subset of features is considered.

There are two key random elements.

1. The samples are drawn differently.
2. Each split looks at features differently.

Then the predictions of many trees are gathered at the end.

Compressed into one sentence:

`Random forest does not feed exactly the same data to every tree. It lets each tree see slightly different data and slightly different feature candidates, and then combines the results at the end.`

### Read It In One Scene

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-01-en.mmd"
```

The key point in this diagram is that `not every tree sees exactly the same thing`. That creates room for different mistakes, and those mistakes can later be averaged or tied together through voting.

### Why Is Repeating The Same Tree Not Enough?

Beginners often ask the following question here.

`If we train a decision tree 100 times, doesn't that just become random forest?`

The core issue is whether `those 100 trees are really different from one another`. If we build many trees with almost the same data, the same feature candidates, and the same rules, their mistakes may also repeat in almost the same direction. In that case, it is closer to `repeating the same judgment loudly` than to `gathering many genuinely different judgments`.

Random forest matters not because it only increases `the number of trees`, but because it creates `the reasons why the trees are different`.

| Comparison scene | What actually happens | Conclusion to read |
| --- | --- | --- |
| copy almost the same tree many times | it repeats almost the same branches and almost the same mistakes | averaging does not reduce instability very much |
| change only the bootstrap sample | each tree sees a slightly different bundle of cases | the degree to which exceptions pull the tree changes a bit |
| also restrict feature candidates randomly | the first split and later paths can diverge more strongly | the trees resemble one another less, so agreement becomes more meaningful |
| aggregate at the end | the excessive confidence of one tree is softened | the whole forest becomes easier to read as a more stable judgment |

So the core of random forest is not `many trees`, but `aggregation across trees that resemble one another less`.

### Why Can Gathering Many Trees Become More Stable?

Decision trees are often described as high-variance models. The scikit-learn User Guide also explains that individual decision trees have high variance and can overfit easily. Random forest combines many diverse trees to reduce that variance.

The reader-facing intuition is simple.

- one tree may be pulled too strongly by a particular exception case
- another tree may see that exception less strongly because its bootstrap sample is different
- yet another tree may create a completely different path because its split feature candidates are different
- once the answers of many trees are gathered, the excessive instability of one tree may appear less strongly

In other words, random forest usually chooses `the agreement of many trees` over `the confidence of one tree`.

Compressed into project-note style:

| Record item | Example |
| --- | --- |
| baseline or single candidate | `single tree` |
| ensemble candidate | `random forest` |
| remaining review cases | `customer X is still ambiguous` |
| change in instability | `test-score difference shrank even when the seed changed` |
| next question | `does stability improve further if we increase the number of trees?` |

With this table, the random-forest Section reads as `comparison candidate -> remaining error cases -> next question`. Its strength becomes clearer not through one average number, but through whether `the remaining failure patterns become less unstable`.

That is why random forest is often considered in practice for `tabular problems where a single tree is too unstable, but the scale or structure is not yet one that naturally jumps straight to a neural network`. The practical expectation there is not `the best one-off score`, but `a stable default candidate`.

### What Does Bootstrap Do?

The first source of randomness in random forest is bootstrap sampling.

The scikit-learn documentation explains that each tree is built from a bootstrap sample drawn with replacement from the training set. Because the sampling is with replacement, some samples can appear twice inside one tree, while other samples can be left out entirely.

The intuition is:

`Each tree does not learn from an exact copy of the full dataset. Each tree goes through a slightly different training experience.`

Think of a very small example.

If the original data are `A, B, C, D, E`, one bootstrap sample may look like this.

- tree 1: `A, B, B, D, E`
- tree 2: `A, C, D, D, E`
- tree 3: `B, C, C, D, E`

Even though every tree starts from the same original data, their views become slightly different.

Compressed into one sentence:

`Bootstrap creates a different training experience for each tree so that all trees do not memorize exactly the same exception case.`

### What Does Random Feature Selection Do?

The second source of randomness is feature sub-sampling.

The scikit-learn documentation explains that each split examines only a random subset of candidate features. The representative hyperparameter for this role is `max_features`.

Why is that needed?

If one strong feature always dominates the first split of every tree, the trees can become too similar. Then even after gathering many trees, the forest still lacks diversity.

So when only part of the feature candidates are shown at a split:

- one tree may split mainly on feature A
- another tree may look at feature B first
- another tree may create a different detour path

So `max_features` should be read not merely as a speed option, but more importantly as `a device that makes trees resemble one another less`.

Seen together, bootstrap and `max_features` reveal their role difference more clearly.

| Device | What it changes directly | Problem it tries to block |
| --- | --- | --- |
| `bootstrap` | the sample bundle each tree sees | all trees being pulled by exactly the same cases |
| `max_features` | the feature candidates shown at each split | the same feature dominating every tree |
| `averaging` or vote | the final way predictions are combined | the excessive confidence of one tree dominating the final answer |

With this table, random forest no longer looks like a vague idea of `mixing things randomly`. It looks like a structure that separately designs `sample diversity`, `branching diversity`, and `final aggregation`.

### How Does It Combine Outputs In Classification And Regression?

Random forest can be used for both classification and regression. What changes is the way the outputs of many trees are combined.

| Problem type | Output of many trees | Final aggregation |
| --- | --- | --- |
| classification | each tree's class or class probability | vote or probability average |
| regression | each tree's predicted number | average |

The scikit-learn documentation explains that in classification forests, the probability predictions of trees are averaged. The phrase `majority vote` is still fine as a large intuition, but in terms of scikit-learn implementation, the probability-average view is more precise.

### Read Random Forest As A Flow

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-02-en.mmd"
```

The core is not `more trees` itself, but `trees that can produce different errors from one another`.

## Detailed Learning Content

### How Should We Read The Representative Hyperparameters?

According to the API documentation, the main handles readers should first know in random forest are roughly these.

| Hyperparameter | First question to read |
| --- | --- |
| `n_estimators` | How many trees should we create? |
| `max_features` | How many features should be examined as candidates at each split? |
| `bootstrap` | Should each tree be trained on a bootstrap sample? |
| `max_depth` | How deep can each tree grow? |
| `min_samples_leaf` | Should each tree be prevented from creating very tiny leaves? |
| `oob_score` | Should we inspect internal evaluation on samples left out by bootstrap? |

At the 15.1 level, the three most important ones are these.

- `n_estimators`: the size of the forest
- `max_features`: how much diversity the trees can have
- `bootstrap`: whether each tree gets a different training experience

Rather than memorizing only the names, we should also read what changes when the values change.

| Hyperparameter | First change that appears when the value changes | First caution to keep in mind |
| --- | --- | --- |
| `n_estimators` | more trees can make the average judgment more stable | computation cost rises, and improvement may flatten after a point |
| `max_features` | trees can become less similar or more similar | if too large, trees become similar; if too small, each tree may weaken too much |
| `bootstrap` | differences in training experience appear across trees | if turned off, the diversity of trees can shrink and weaken the forest's advantage |
| `max_depth` | the complexity of each individual tree changes | if too deep, each tree inside the forest can still memorize exceptions too much |
| `min_samples_leaf` | it blocks leaves from fragmenting too finely | if too large, even necessary branches can become blunt |

In practice, it helps to read them like this.

- If the score is acceptable but changes across seeds, check `n_estimators` and `max_features` first.
- If the trees all look too similar, suspect that `max_features` may be too large.
- If each tree seems to memorize exceptions too much, inspect `max_depth` and `min_samples_leaf` as well.

### What Is OOB(Out-Of-Bag)?

Once bootstrap sampling is used, some samples are left out of the training for a particular tree. The scikit-learn documentation explains that those left-out samples can be used for an OOB(out-of-bag) estimate of generalization error.

OOB can be understood as a way of getting a partial validation-like sense from samples that each tree did not see.

But OOB should not be understood as `a universal device that replaces every evaluation procedure`. In this Section, we only fix its name and role.

Still, it matters to know why OOB is mentioned here at all. Because random forest uses bootstrap, `samples that a tree did not learn from` appear naturally. OOB is simply a way of reusing those leftover samples. So OOB is not an evaluation trick awkwardly attached from outside. It is more natural to read it as `an internal checking handle that comes together with bootstrap`.

## Cases And Examples

### Case 1. When The Agreement Of Many Trees Is Better Than One Rule In Churn Prediction

A subscription-service team first tried a decision tree for churn prediction. The human-first criteria were signals such as `recent visit count`, `late payment`, `inquiry count`, and `membership tier`.

The single tree was easy to read, but the boundary was easily pulled by a few exceptional customers. Under one data split it matched well, but under another split even a small change could shake the first split and the prediction result. The team wants to keep the question flow of trees while reducing the excessive sensitivity of one tree.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-03-en.mmd"
```

In this scene, random forest should be read not as `a way to throw the tree away`, but as `a way to gather many slightly different trees and let them agree`. If bootstrap lets each tree see a slightly different customer bundle, and `max_features` also changes the split candidates, then a single tree's attraction to a particular exception can become weaker on average across the whole forest.

Compressed into a work note, the order looks like this.

| Stage | What the team actually sees |
| --- | --- |
| human-first criteria | `recent visit count`, `late payment`, `inquiry count`, `membership tier` |
| limit of a single tree | a few exceptional customers easily shake the first split and the boundary |
| what random forest changes | many trees see different customer bundles and different split candidates |
| final judgment method | read the agreement of many trees rather than the excessive rule of one tree |
| verifiable result | inspect seed-to-seed instability and remaining error cases together, not only the best score |

The verifiable result appears not only in the test scores of a single tree and a random forest, but also when we inspect how much they fluctuate across several random seeds. If average stability improves more than the best one-off score, we can explain that the strength of random forest is not `a more complicated rule`, but `a less unstable agreement`.

### Case 2. How Can It Be Read In Practical Scenes?

Random forest can be read especially well in the following scenes.

| Work scene | Why random forest may feel favorable |
| --- | --- |
| churn prediction | it is less pulled by one tree's exceptional branch and is easy to start from on tabular data |
| loan-review support | it can catch nonlinear relationships while keeping the feeling of the tree family |
| equipment anomaly detection | it can divide complex sensor combinations through many trees |
| marketing-response prediction | it can gain stability more easily than a single tree that relies too much on one or two features |

On the other hand, if interpretability is the highest priority and every prediction must be explained immediately as an individual rule, random forest can feel less favorable than a single decision tree. The whole forest is much harder to read than one tree.

## Practice And Example

### Python Example: Compare One Tree And Many Trees

This example is a small exercise that compares one decision tree and a random forest on the same iris-classification problem.

- problem situation: inspect the difference between one tree and a forest of many trees
- input: the 4 iris features
- label: species class
- concepts to check:
  - random forest gathers many trees
  - test performance and stability can change even on the same data
  - `n_estimators` is connected to the size of the forest

Values to change:

- `n_estimators`: compare forest sizes such as 10, 50, and 100 while watching score and runtime together.
- `random_state`: see how differently a single tree and a forest react to the same seed changes.
- `max_features`: compare the default value with `None` to see what changes when tree diversity shrinks.

```python
# This example compares a single decision tree and a random forest side by side on iris classification.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

single_tree = DecisionTreeClassifier(random_state=42)
single_tree.fit(X_train, y_train)

forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
forest.fit(X_train, y_train)

print("single tree")
print("  train accuracy:", round(single_tree.score(X_train, y_train), 3))
print("  test accuracy :", round(single_tree.score(X_test, y_test), 3))
print("  depth         :", single_tree.get_depth())
print("  leaves        :", single_tree.get_n_leaves())
print()

print("random forest")
print("  train accuracy:", round(forest.score(X_train, y_train), 3))
print("  test accuracy :", round(forest.score(X_test, y_test), 3))
print("  trees         :", len(forest.estimators_))
print("  first depth   :", forest.estimators_[0].get_depth())
```

An example output is as follows.

```text
single tree
  train accuracy: 1.0
  test accuracy : 0.911
  depth         : 5
  leaves        : 8

random forest
  train accuracy: 1.0
  test accuracy : 0.911
  trees         : 100
  first depth   : 4
```

From this tiny result alone, the two models can look similar. That is why the next thing to inspect is `how they fluctuate when the random_state changes`.

### Python Example: Inspect The Difference In Instability

This example repeats the same data split across several random seeds and checks how much the test performance of a single tree and a random forest fluctuates.

Problem situation:

- when comparing models, it matters to inspect not only the best score, but also how much the performance shakes across several splits

Input:

- iris dataset
- one decision-tree model
- one random-forest model
- several random seeds

Expected output:

- test scores of the tree and the random forest across seeds
- the average or instability difference between the two models

Concepts to check:

- the strength of random forest can appear more clearly in `reduced instability` than in the single best score
- comparing several seeds is the simplest way to read stability

Values to change:

- `range(10)`: change the number of repeated seeds to 5 or 20 and see how stable the average becomes.
- `n_estimators`: compare 10 and 100 to see how the number of trees affects instability.
- `max_depth`: limit both the single tree and the individual trees inside the forest to see how the average score changes.

```python
# This example compares test-score variation across random_state values for a single tree and a random forest.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

tree_scores = []
forest_scores = []

for seed in range(10):
    tree = DecisionTreeClassifier(random_state=seed)
    tree.fit(X_train, y_train)
    tree_scores.append(tree.score(X_test, y_test))

    forest = RandomForestClassifier(n_estimators=100, random_state=seed)
    forest.fit(X_train, y_train)
    forest_scores.append(forest.score(X_test, y_test))

print("single tree test scores :", [round(s, 3) for s in tree_scores])
print("forest test scores      :", [round(s, 3) for s in forest_scores])
print("tree avg                :", round(sum(tree_scores) / len(tree_scores), 3))
print("forest avg              :", round(sum(forest_scores) / len(forest_scores), 3))
```

An example output is as follows.

```text
single tree test scores : [0.978, 0.933, 0.911, 0.933, 0.911, 0.911, 0.933, 0.911, 0.911, 0.933]
forest test scores      : [0.978, 0.956, 0.933, 0.933, 0.933, 0.933, 0.956, 0.933, 0.933, 0.956]
tree avg                : 0.927
forest avg              : 0.944
```

What this example shows is the following.

1. A single tree can still do well under some seeds.
2. But random forest is often less unstable and more stable on average.
3. The value of random forest comes not from `a completely new structure`,
but from `averaging unstable trees`.

## Checklist

- Can you explain random forest as `an aggregation model of many randomized decision trees`?
- Are you checking whether instability truly decreased compared with a single tree, using the same error cases as a reference?
- Do you understand that bootstrap and random feature selection are devices for making trees resemble one another less?
- Can you explain that random forest tries to reduce the variance of a single tree by gathering predictions from many trees?
- Are you reading the strength of random forest through average stability rather than the highest score?
- Do you know that interpretability can become lower than that of a single tree?
- Can you distinguish which of `n_estimators`, `max_features`, and `bootstrap` is the more important handle in the current situation?

## Sources And References

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, `Random Forests`, Machine Learning, 45(1), 5-32, 2001, accessed 2026-07-26. [https://doi.org/10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324){: target="_blank" rel="noopener noreferrer" }
