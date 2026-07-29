# P4-15.4 Supplementary Learning: Comparing Extra Trees and Random Forest

> Section ID: `P4-15.4`
> Version: `v2026.07.26`

Once readers learn [random forest](/AiBook/en/reference/concept-glossary-alpha/r/#random-forest) in P4-15.1, they soon encounter a similarly named model, [Extra Trees(Extremely Randomized Trees)](/AiBook/en/reference/concept-glossary-alpha/e/#extra-trees). Because both look like `forests that gather many trees and average them`, it is easy at first to pass over them as if they were essentially the same model.

But the two differ clearly in `how far the randomness is injected`, `how the split criterion is chosen`, and whether [bootstrap](/AiBook/en/reference/concept-glossary-alpha/b/#bootstrap) and [OOB](/AiBook/en/reference/concept-glossary-alpha/o/#oob-score) are used as the default flow.

This Section does not repeat the main explanation of random forest. Instead, it organizes the confusing points that appear when readers compare Extra Trees for the first time.

## Questions Closed By Comparing Extra Trees And Random Forest

This Section answers the following questions.

- Is [Extra Trees](/AiBook/en/reference/concept-glossary-alpha/e/#extra-trees) in the same family as random forest?
- If both average many trees, what is actually different?
- What is the difference between [`best split`](/AiBook/en/reference/concept-glossary-alpha/b/#best-split) and [random threshold](/AiBook/en/reference/concept-glossary-alpha/r/#random-threshold)?
- Why is Extra Trees described as more random?
- How should [OOB(out-of-bag)](/AiBook/en/reference/concept-glossary-alpha/o/#oob-score) be read differently in random forest and Extra Trees?

This Section first closes the question `where should random forest and Extra Trees be read as the same, and where should they be read differently?` The philosophical contrast between Extra Trees and gradient boosting reconnects in P4-16.1 and P4-16.2.

## Judgments To Keep From Comparing Extra Trees And Random Forest

- You can explain Extra Trees as `a tree ensemble with stronger randomness`.
- You can compare random forest and Extra Trees by `sample drawing`, `split-threshold selection`, and `the condition under which OOB is possible`.
- You can explain at an introductory level that Extra Trees often reduces [variance](/AiBook/en/reference/concept-glossary-alpha/v/#variance) a little more while increasing [bias](/AiBook/en/reference/concept-glossary-alpha/b/#bias) a little.
- You can explain when it is worth raising random forest and Extra Trees together as comparison candidates.

## Why This Section Is Needed

Right after readers understand random forest, the following misunderstanding appears easily.

- both are forests
- both choose features randomly
- then are they not really the same model with different names?

One further distinction is needed here.

| Question | Random Forest | Extra Trees |
| --- | --- | --- |
| training data | usually a bootstrap sample | by default, the full training set |
| split threshold | search for the best split among candidates | draw thresholds randomly and choose among them |
| strength of randomness | large | larger |
| default OOB flow | connected naturally | not connected under the default setting |

So Extra Trees is still `in the same forest family as random forest`, but it should be read as `a forest that randomizes even the way split criteria are chosen`.

## Main Learning Content

### Is Extra Trees Also In The Same Tree-Ensemble Family?

The scikit-learn User Guide explains both random forest and Extra-Trees as averaging algorithms in the family of `randomized decision tree ensemble`. In other words, both models create many trees and average or aggregate their predictions to improve generalization and stability.

If we fix the common points first, they look like this.

- both use many decision trees
- both create split candidates while looking at only part of the features
- both average or aggregate the predictions of many trees
- both have a large goal of reducing instability compared with a single tree

So there is no need to read Extra Trees as `a completely new family`. At first, it is enough to position it as `a comparison candidate very close to random forest`.

### Key Difference 1. How Is The Split Threshold Chosen?

The scikit-learn User Guide explains that random forest searches for the `best split` at each node. By contrast, extremely randomized trees also look at feature subsets, but for each feature they draw split thresholds randomly and choose the best one among those random candidates.

Restated for beginners:

- random forest explores more of the question `where is the best place to cut at this node?`
- Extra Trees is closer to `draw several random cuts and use the one that is less bad`

So in Extra Trees, not only feature selection, but also `where to cut` is more random.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-01-en.mmd"
```

The core of this diagram is that the two models share the idea of feature subsets, but their attitude toward choosing thresholds is different.

### Key Difference 2. The Default Bootstrap Setting Is Different

The scikit-learn User Guide explains that the default of random forest is `bootstrap=True`, while the default of Extra Trees is `bootstrap=False`. The Extra Trees API documentation also explains that when `bootstrap=False`, each tree is trained on the whole dataset.

That difference is more important than it first looks.

| Item | Default in Random Forest | Default in Extra Trees |
| --- | --- | --- |
| `bootstrap` | `True` | `False` |
| input to each tree | sample drawn with replacement | the full training set |
| can OOB be used? | naturally under the default flow | impossible under the default setting |

So Extra Trees is `a more random forest`, but that extra randomness does not necessarily come from `drawing different samples`. Under the default setting, the central source of randomness is `randomized split thresholds`, while the sample itself remains the full training set.

### Key Difference 3. OOB Is Not The Same Default Handle In The Two Models

As P4-15.3 showed, OOB requires `samples that were left out by bootstrap`. The scikit-learn API documentation explains that in both random forest and Extra Trees, `oob_score` can be used only when `bootstrap=True`.

Therefore:

- in random forest, the default is `bootstrap=True`, so OOB follows naturally
- in Extra Trees, the default is `bootstrap=False`, so OOB cannot be used as a default inspection handle

Many readers feel confused and ask, `why can't I see OOB in Extra Trees?` The model is not different in that sense. The difference comes from the default sampling strategy.

### Why Is Extra Trees Still A Candidate Even Though It Is More Random?

The scikit-learn User Guide explains that extremely randomized trees increase randomness further in the split-computation stage, which can reduce variance a little more while increasing bias a little.

Compressed into one sentence:

`Each individual tree may become a little less precise, but the whole forest can be made of trees that resemble one another even less.`

So Extra Trees can be read as giving up a little of `careful split search in each individual tree` in exchange for enlarging `diversity in the whole forest`.

| Viewpoint | Random Forest | Extra Trees |
| --- | --- | --- |
| split search in one tree | more careful | rougher |
| diversity of the whole forest | large | can become larger |
| expected effect | improved stability | improved stability plus possible extra variance reduction |
| possible cost | computation cost | slightly larger bias |

The important point in this table is not `Extra Trees is always better`. It is `the position where randomness is injected is different`.

### When Is It Worth Comparing Extra Trees Together?

Inside the same candidate family as random forest, Extra Trees is worth trying together when readers want `a slightly faster and slightly more random forest`.

| Current situation | Why raise Extra Trees together | What to check together |
| --- | --- | --- |
| random forest is understood, but one more comparison candidate is needed | because it becomes a very close comparison axis inside tree ensembles | whether a real difference appears on test |
| the cost of deep split search feels burdensome | because split search can become simpler | whether the speed gain is actually noticeable |
| readers want to reduce the instability of a single tree even more strongly | because randomness inside the split stage is larger | whether the extra bias lowers the test score |
| train/test comparison matters more than OOB right now | because the default is `bootstrap=False`, so OOB dependence is weaker | separate validation or test management |
| readers want to compare importance, prediction stability, and computation time together | because it is a sibling model that compares naturally next to random forest | whether the importance interpretation is being overtrusted |

The point of this table is not to say `always add Extra Trees`. It is to position it correctly as `a comparison candidate to test right next to random forest`.

## Cases And Examples

### Case 1. How Should Two Forests Be Read Differently In A Churn Problem?

Suppose a team first tries random forest for churn prediction. The test performance is acceptable, but the team is left with questions such as `is this forest fitting branches too finely?` and `could a slightly rougher randomness actually improve stability?`

The reason to raise Extra Trees here is not that `a totally different philosophy is needed`. It is to inspect, inside the same tree-ensemble family, `what changes if split search becomes more random`.

For example:

- random forest searches for better thresholds such as `recent logins < 3.5` and `failed payments < 1.5`
- Extra Trees draws threshold candidates more randomly and uses the less-bad split among them

If the team shrinks the current customer table into a tiny scene, it may look like this.

| Customer | Recent login count | Failed-payment count | Inquiry count | Actual churn |
| --- | ---: | ---: | ---: | --- |
| A | 1 | 2 | 4 | yes |
| B | 2 | 1 | 3 | yes |
| C | 5 | 0 | 1 | no |
| D | 6 | 0 | 0 | no |

When looking at this table, random forest is closer to searching more seriously for `where between 2 and 5 should logins be cut` and `what threshold between 0 and 1 is best for failed payments`. Extra Trees is closer to choosing several random cuts and then using the less-bad one.

So even the comparison questions shift a little.

| Comparison question | What to look at first in random forest | What to look at first in Extra Trees |
| --- | --- | --- |
| why did it get this right? | did the more precise split search help? | did the rougher randomness actually help generalization? |
| why did it get this wrong? | was a fine threshold pulled by exceptional customers? | did a rough threshold blur an important boundary? |
| what should be adjusted next? | `max_features`, depth, leaf size | `max_features`, depth, and if needed `bootstrap` |

So the experiment note should not say only `both are forests`. It should also keep the following.

- the gap in test score
- the gap between train and test
- whether the importance ranking changes a lot
- the gap in computation time

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-02-en.mmd"
```

What matters in this flow is not only `who won`, but also `how performance, instability, and computation cost move when the position of randomness is changed`.

### Case 2. Why Try Extra Trees Together In Defect Detection?

In factory defect detection, there can be many sensor values, and some boundaries can be very fine. Suppose a team first uses random forest. The train performance is very high, but the test behavior looks unstable depending on exceptional patterns from particular production days.

The reason to run Extra Trees together here is not that `it is a more advanced model`. It is to check whether `a less stubborn threshold search may become less attached to accidental boundaries from a particular date`.

If we shrink the sensor records into a tiny scene:

| Batch | Temperature deviation | Vibration deviation | Pressure deviation | Actual defect |
| --- | ---: | ---: | ---: | --- |
| A | 0.8 | 0.9 | 0.3 | yes |
| B | 0.7 | 0.8 | 0.4 | yes |
| C | 0.2 | 0.3 | 0.2 | no |
| D | 0.3 | 0.2 | 0.1 | no |

Random forest may search for a more detailed cut such as `vibration deviation = 0.82`. That can help in some cases, but if the dataset is small or one production day contains noise, that noise can itself begin to look like a boundary. Extra Trees uses more random thresholds, so each individual tree can look less precise, but the whole forest can also end up resembling those exceptional date patterns less.

In this scene, the following notes make the comparison easier.

- whether the train score improved by random forest is still maintained on test
- whether Extra Trees keeps test similar or slightly higher while reducing instability
- whether the top sensor rankings are similar across the two models
- whether the computation time difference is noticeable in practice

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-03-en.mmd"
```

The core of this case is not `Extra Trees always fits better`. It is that `when fine threshold search becomes too sensitive to exceptional patterns, Extra Trees becomes an immediate nearby comparison candidate`.

## Practice And Example

This example trains `RandomForestClassifier` and `ExtraTreesClassifier` side by side on the same data, so that readers can inspect together the difference in default settings and the points for reading their scores.

- problem situation: even when random forest and Extra Trees look similar, inspect how the reading points for `bootstrap`, `OOB`, and train/test actually differ
- input: 30 continuous features from the breast-cancer classification dataset
- label: malignant / benign class
- concepts to check:
  - the default random-forest flow matches `bootstrap=True`
  - the default Extra Trees flow has `bootstrap=False`, so OOB does not follow automatically
  - the two models should be compared not only by test score but also by the train/test gap and computation time
- values to change:
  - add `bootstrap=True, oob_score=True` to `et` and confirm the condition under which OOB appears
  - change `n_estimators` in both models to 100, 300, and 600, then inspect test score and computation time together
  - change `max_features` and inspect how the randomness difference appears in scores and importance

```python
# This example compares Random Forest and Extra Trees defaults and scores on the same breast-cancer data.
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

rf = RandomForestClassifier(
    n_estimators=300,
    bootstrap=True,
    oob_score=True,
    random_state=42
)

et = ExtraTreesClassifier(
    n_estimators=300,
    random_state=42
)

rf.fit(X_train, y_train)
et.fit(X_train, y_train)

print("[Random Forest]")
print("  bootstrap     :", rf.bootstrap)
print("  oob score     :", round(rf.oob_score_, 3))
print("  train accuracy:", round(rf.score(X_train, y_train), 3))
print("  test accuracy :", round(rf.score(X_test, y_test), 3))

print("[Extra Trees]")
print("  bootstrap     :", et.bootstrap)
print("  train accuracy:", round(et.score(X_train, y_train), 3))
print("  test accuracy :", round(et.score(X_test, y_test), 3))
```

An example output can look like this. The exact values can change a little depending on the split, library version, and random setting.

```text
[Random Forest]
  bootstrap     : True
  oob score     : 0.96
  train accuracy: 1.0
  test accuracy : 0.947

[Extra Trees]
  bootstrap     : False
  train accuracy: 1.0
  test accuracy : 0.953
```

The reading order is as follows.

1. Both models can have very high train accuracy, so readers should not decide from train alone.
2. Random forest can be read together with OOB, but Extra Trees has no OOB under the default setting.
3. Even if the test accuracy looks similar or Extra Trees looks slightly higher once, readers should not generalize from only that one number and should recheck the dataset-specific difference.

So the core of this example is not `who is always better`. It is confirming through output itself that `even inside the same forest family, the way randomness is injected is different`.

## Checklist

- Can you explain Extra Trees as belonging to the same `randomized tree ensemble` family as random forest?
- Can you explain Extra Trees as `a very close sibling model of random forest`?
- Do you understand that the difference appears more strongly not in `random feature selection` itself, but in `how randomly the threshold is chosen`?
- Can you explain the difference between `best split` and `random threshold`?
- Do you know that random forest connects naturally to the bootstrap and OOB flow by default, while Extra Trees does not under its default setting?
- Can you explain why OOB does not appear immediately under the default Extra Trees setting?
- Are you reading Extra Trees as a comparison candidate that may reduce variance a bit more while increasing bias a bit?
- Do you know that when comparing random forest and Extra Trees, the train/test gap, OOB availability, and computation cost should be inspected together?

## Sources And References

- scikit-learn, "1.11.2. Random forests and other randomized tree ensembles", User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, "ExtraTreesClassifier", API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, "RandomForestClassifier", API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Pierre Geurts, Damien Ernst, Louis Wehenkel, "Extremely randomized trees", *Machine Learning*, 63(1), 3-42, 2006, accessed 2026-07-26. [https://doi.org/10.1007/s10994-006-6226-1](https://doi.org/10.1007/s10994-006-6226-1){: target="_blank" rel="noopener noreferrer" }
