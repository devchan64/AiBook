# P4-15.2 Feature Importance

> Section ID: `P4-15.2`
> Version: `v2026.07.20`

In P4-15.1, we saw why random forest can create more stable predictions by gathering many trees. That immediately raises the next question.

What did this forest consider important when it made its judgment?

That question is the starting point of feature importance.

Feature importance is a number that summarizes which features the model used more often or more strongly, but it becomes dangerous if we read that number directly as a ranking of causes or truths.

Feature importance is a useful summary, but it is also a tool that comes with interpretation traps.

This Section does not repeat the basic definition of random forest at length. The core intuition `reduce instability through the agreement of many trees` reconnects through P4-15.1 and the [concept glossary](/AiBook/reference/concept-glossary/). Here we focus only on the problem of interpreting what the forest treated as important.

## Scope Of This Section

This Section answers the following questions.

- How is feature importance created in random forest?
- What does `feature_importances_` mean?
- How are impurity-based importance and permutation importance different?
- Why can an important-looking number still create misunderstanding?
- What different interpretation questions do PDP(partial dependence plot) and SHAP ask compared with importance?
- Why should importance interpretation not be jumped directly into causal inference?
- What conservative interpretation strategy is needed when real data have very strong correlated features?

This Section does not stop after drawing only the outer boundary of importance interpretation. It also recovers the following inside the current Section: `what should be inspected when a number summary is not enough`, `why cause interpretation must be separated`, and `how to read more conservatively when correlation is strong`.

| Item | How this Section handles it |
| --- | --- |
| PDP(partial dependence plot), SHAP | This Section directly recovers what different questions they ask from importance, though it does not unfold every implementation option |
| the causal-inference viewpoint on importance | This Section directly recovers why `model usage` and `causal effect` must be separated, though it does not unfold the full estimation procedure |
| interpretation strategies for real large datasets with strong correlation | This Section directly recovers the minimum order of interpretation strategy, though it does not unfold a full production pipeline |

This Section focuses on establishing `an attitude for reading the number`.

## Goals Of This Section

- You can explain feature importance as `a summary of internal model usage`.
- You can distinguish impurity-based importance(MDI) from permutation importance.
- You can explain that feature importance does not directly mean causality or the true ranking of causes.
- You can explain why correlated features and high-cardinality features can distort interpretation.

## Learning Background

After learning random forest, readers often become ready to expect the following.

- the forest predicts well
- there are many trees inside the forest
- then the model must also be able to say well what is important

That expectation is only half right.

| Expectation | In reality |
| --- | --- |
| if the importance number is large, it is a cause | it is closer to meaning that the model used it a lot |
| if the importance number is low, the feature is useless | it may overlap with or be substituted by another feature |
| importance is always a fair ranking | depending on the calculation method, bias can appear |

That is why 15.2 is not a Section about `how to trust the importance number`, but a Section about `how not to overtrust the importance number`.

The same record structure is fixed here too. This Section is not merely for sorting numbers. It is a Section for leaving `what importance observation appeared`, `what is still inside the interpretation boundary`, and `what the next data-enrichment question is`. Even when two importance rankings look similar, we still need to inspect separately which feature combinations substitute for one another and whether the difference in importance really connects to a difference in performance patterns.

| Record to keep together | Why it matters |
| --- | --- |
| observed importance ranking | to see which features the model used more |
| interpretation-boundary sentence | to avoid turning the importance number into a ranking of causes |
| features marked for review | to revisit correlated or high-cardinality columns |
| next question | to decide what feature to collect more of or what comparison experiment to run next |

### When Should We Read Importance Numbers Especially Carefully?

Feature importance is convenient, but certain data structures make it easy to overtrust the interpretation.

| Visible scene | Why caution comes first | What to check together |
| --- | --- | --- |
| a column with many unique values rises to the top | it may be high-cardinality bias | compare with permutation importance |
| there are several features with almost the same meaning | the importance may split across substitute features | inspect groups of correlated features |
| the importance gap is small but the ranking differs | it is easy to exaggerate the ranking difference into a truth ranking | inspect actual performance change together |
| importance is high but the explanation feels awkward | model usage and real-world cause are not the same | inspect domain meaning and cases |
| a low-importance feature looks removable | it may still matter when combined with another feature | run a before/after removal comparison |

The point of this table is not to throw the number away. It is to make the reader first notice `when this number is especially likely to invite misunderstanding`.

## Main Learning Content

### From What Idea Does Feature Importance Come?

The scikit-learn User Guide explains that, in a tree, upper decision nodes affect the predictions of more samples, and relative importance can be estimated by combining how much each split reduces impurity. Averaging that idea over many randomized trees gives mean decrease in impurity, or MDI.

Feature importance is a value that summarizes how often and how strongly a feature contributed to better splits.

`If a feature created split improvements frequently and by a large amount, read that feature as more important.`

That explanation looks very natural at first. And in practice it is fast and convenient. But an important condition must be attached immediately.

`This value is a summary of how the model used branches inside the training data.`

Importance is closer to `a usage record inside the model` than to the true importance in the world or the size of a cause.

### What Is MDI(Mean Decrease In Impurity)?

The scikit-learn documentation explains the feature importance of tree ensembles as impurity-based feature importance, and the average over many trees as MDI.

MDI is calculated in the following order.

1. Inspect how much impurity decreases at each split in a tree.
2. Assign that decrease to the feature that created the split.
3. Sum it across one tree.
4. Average it across the whole forest.
5. Normalize it so that the total becomes 1.

Drawn more briefly:

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-01-en.mmd"
```

Because of that structure, `feature_importances_` is quick to compute and can be read right after training a random forest.

### Why Do Upper Splits Matter More?

The scikit-learn documentation explains that features used in upper splits of a tree influence the final prediction of more input samples. So even with the same impurity decrease, a split that changes the flow of many samples can appear more strongly in the final importance.

Compressed into one line:

`Questions early in the tree divide more people, while later questions divide only a few. That is why features used in early splits can look larger in total importance.`

### How Should We Read `feature_importances_`?

The API documentation describes `feature_importances_` as impurity-based feature importances. The values are positive and their sum is 1.0.

A first reading is as follows.

| Number shape | Meaning |
| --- | --- |
| the value is large | the model used that feature relatively more |
| the value is small | the model used that feature relatively less |
| the total is 1 | it should be read as a relative share rather than an absolute score |

What matters here is the phrase `relative share`.

For example, if the importances are:

- `visits = 0.45`
- `late_payment = 0.35`
- `support_calls = 0.20`

then, inside the branching criteria of this model, `visits` can be read as having played the largest role. But that does not mean `visit count is the strongest real-world cause`.

### Why Is Permutation Importance Needed Separately?

The scikit-learn documentation presents permutation importance as an alternative to impurity-based feature importance. Permutation importance checks how much performance worsens when the values of one feature are randomly shuffled.

If MDI is closer to `an internal usage record`, permutation importance is closer to `how much the real predictive performance shakes when this feature is broken`.

The comparison looks like this.

| Method | Core question |
| --- | --- |
| MDI | How often and how strongly was this feature used in splits? |
| permutation importance | If this feature is shuffled, how much does model performance fall? |

That difference matters a lot. One is closer to `usage traces inside the model`, while the other is closer to `a dependence check through performance`.

### Read Permutation Importance As A Flow

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-02-en.mmd"
```

This flow matters because it makes the reader re-read importance not as `a property of the number`, but as `a performance-change experiment`.

## Detailed Learning Content

### Why Should Impurity-Based Importance Be Treated Carefully?

The scikit-learn User Guide warns of two major problems with impurity-based feature importance.

1. It depends on statistics computed on the training data,
so it does not necessarily reflect importance for generalization on hold-out data.
2. It can favor high-cardinality features with many unique values.

Restated more simply:

`MDI is fast and convenient, but it can overestimate features that make it easy to create fine splits inside the training data.`

For example, if there is a column like a customer ID with very many unique values, it may look important because it makes it easy to split training data finely, even when it contributes little to generalization.

### Why Do Correlated Features Create Confusion?

The scikit-learn examples show that in the presence of multicollinear or correlated features, permutation importance can also look different from what was expected. If several features carry almost the same information, shuffling one of them may not hurt much because another feature can substitute for it.

That creates the following misunderstanding.

- test accuracy is high
- but the permutation importance of one feature is low
- then, is that feature unimportant?

Not always.

It may mean not `unimportant`, but `another correlated feature is already providing similar information`.

So importance interpretation is not only about one feature. It is also about reading the relationships among features.

A tiny table for the same scene:

| feature | actual meaning |
| --- | --- |
| `monthly_spend` | spending over the last month |
| `yearly_spend_div_12` | yearly spending divided by 12 |

These two can carry almost the same directional information. Then the model may use one more often and the other less often. But that does not mean the less-used one is completely useless. We should first imagine `the possibility that importance was split because the two features share similar information`.

The same scene can also look confusing in permutation importance. If `monthly_spend` is shuffled, `yearly_spend_div_12` may still remain, so the performance drop can be smaller than expected. Then even permutation importance may appear low, inviting the misunderstanding `are both of them not very important?` But in reality, the model may simply remain less broken because one substitute feature is still left.

So when correlation is strong, we should not jump from `the number is low` to `it is unimportant`. We should first ask `is another feature standing in for it?`

## What Different Questions Do PDP And SHAP Ask?

Feature importance summarizes `what the model used a lot`. But the reader soon wants to ask the following too.

- If the value of this feature increases, in which direction does the prediction move?
- In this one sample, which feature pushed the prediction up?

That is exactly where PDP(partial dependence plot) and SHAP appear together.

| Tool | First question it tries to answer |
| --- | --- |
| feature importance | What does the model use a lot? |
| PDP | If one feature value changes, how does the prediction move on average? |
| SHAP | In this sample, how did each feature contribute to the prediction? |

So importance is closer to `a usage summary`, PDP to `an average directional effect`, and SHAP to `a decomposition of contribution for an individual prediction`.

Compressed more briefly:

| What you want to inspect now | Tool to think of first |
| --- | --- |
| what the whole model uses a lot | feature importance |
| whether the prediction rises or falls as one feature increases | PDP |
| what pushed the prediction in this one case | SHAP |

Therefore, if we try to say `in which direction does it affect the prediction` using the importance number alone, the information is insufficient. Importance may be high, but that alone does not tell us whether larger values raise the prediction or lower it. That directional question is answered more directly by a tool like PDP.

Likewise, even if importance is high, we cannot assume that the same feature works in the same way for sample A and sample B. The question that tries to read those individual contributions more directly is where SHAP appears.

So PDP and SHAP are not names that replace importance. They are better read as tools that hold onto `different interpretation questions that do not close with the importance number alone`.

## Why Are Importance And Causal Inference Different?

After looking at an importance number, readers easily jump to the sentence:

`This feature is important, so it is the cause of the result.`

But that jump is not safe.

| What importance interpretation tells us | What causal interpretation asks |
| --- | --- |
| which feature the model used a lot for prediction | if we actually change that feature, does the result change? |
| a statistical relationship inside the data | intervention and causal effect |

Suppose the importance of `recent_visits` came out high. That means the model used recent visit count a lot when making predictions. But it does not allow us to say immediately `if we increase visit count, the response rate will definitely rise`. In reality:

- visit count itself may be a cause
- or users who were already highly interested may have both high visit count and high response rate
- or another hidden factor may be moving both together

So importance is an explanatory tool inside a predictive model, while causal inference belongs to a different level: it asks more strictly `what changes the result if we change it?`

The boundary readers should keep from this Section is the following.

| Sentence it is easy to write right away | Safer sentence |
| --- | --- |
| `this feature is the cause` | `this model used this feature a lot in prediction` |
| `if we change this feature, the result changes` | `whether the result changes requires separate causal review` |

Therefore, importance interpretation can help generate `candidate causal hypotheses`, but it is not itself a proof of cause.

## How Should We Read Real Data With Very Strong Correlated Features?

In real large datasets, it is common for not just a few, but dozens of features with similar meaning to enter together. Then, if we conclude by looking only at `the importance of one column`, the interpretation almost always becomes overconfident.

A conservative interpretation strategy is better fixed in the following order.

| Order | First thing to do | Why |
| --- | --- | --- |
| 1 | inspect similar-meaning features as a group | because importance can split across several columns |
| 2 | inspect MDI and permutation importance together | to separate internal usage from performance dependence |
| 3 | run a before/after removal experiment | to confirm whether the feature is really substitutable |
| 4 | leave notes at the level of feature groups rather than one column | because roles are not always fixed to one column in large data |

For example, it is safer to read things like this.

| Risky reading | Safer reading |
| --- | --- |
| `column A has low importance, so remove it` | `first inspect whether other features in the same group are substituting for column A` |
| `column B is ranked first, so it is the most important business cause` | `the feature group containing column B was heavily used by the model` |
| `the permutation drop is small, so it is unnecessary` | `the drop may be small because substitute features remain` |

So when correlation is very strong, it becomes more important to read `similar feature groups`, `before/after removal comparison`, and `comparison across importance methods` than only `a ranking table of individual columns`. That is exactly the goal of this Section. It is not to believe one number more strongly, but to keep a standard for reading the number more conservatively.

### What Should We Do Immediately After Seeing The Importance Numbers?

This is where beginners most often get stuck. `So I saw the numbers. What is the next action?`

In this Section, the minimum order is the following.

| Order | First question | Why it is needed |
| --- | --- | --- |
| 1 | What are the top features? | to confirm what the model mainly looked at |
| 2 | Is this value MDI or permutation? | because even the same word `importance` can mean different things |
| 3 | Are there high-cardinality columns or correlated features? | because possible distortion should be checked first |
| 4 | Does the interpretation fit the domain meaning? | because model usage and real explanation can differ |
| 5 | Is there a comparison experiment before deletion or policy change? | because it is dangerous to conclude from importance alone |

The purpose of this order is not to make the work complicated. It is to make feature importance be read again not as `a score table`, but as `a checklist`.

### Wrong Conclusions That Are Easy To Jump To From High Or Low Importance

Importance numbers look very clear in size, so readers easily jump straight into action conclusions. But safer interpretation takes one extra step.

| Number seen now | Conclusion that is easy to jump to | Safer interpretation |
| --- | --- | --- |
| importance is high | it is the most important cause | the model used this feature a lot |
| importance is low | it can be deleted | it may be hidden behind another feature |
| permutation drop is small | it is unnecessary for performance | substitute features may still remain |
| MDI is very large | this feature alone is enough | possible branching bias on training data must be checked |

Once this table is familiar, the first reaction after seeing an importance number slows down a little. That slowing down is exactly the device that protects interpretation quality.

## Cases And Examples

### Case 1. Why Is It Dangerous To Call A High Importance Number A Cause Right Away?

A marketing team trains a random forest to predict customer response and wants to inspect which features were important. The human-first criteria included signals such as `recent visit count`, `discount-message clicks`, `purchase amount`, and `membership tier`.

After training the model, `feature_importances_` shows high values for `recent_visits` and `discount_clicks`. At that point, the team may want to say immediately `visit count is the biggest cause`. But the number is first a summary of `how much the model used that feature in branching`, not a direct ranking of causes in the real world.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-03-en.mmd"
```

In this scene, feature importance should be read as `a starting point for explanation`. MDI summarizes the internal usage traces of the model, while permutation importance inspects how much real performance shakes when that feature is shuffled. Also, if there are several features with similar meaning, one may appear high and another low, even though in reality they may be standing in for one another.

The verifiable result appears when MDI and permutation importance are read side by side, and when we inspect together whether there are high-cardinality columns or correlated features. Instead of changing policy from one importance number alone, we should separate which column was used a lot inside the model from which column really shakes predictive performance.

### Case 2. Why Should We Not Delete A Feature Immediately Even When Its Importance Looks Low?

Suppose a team built a subscription-cancellation prediction model. Its features include `monthly_spend`, `yearly_spend_div_12`, `recent_visits`, and `late_payment_count`. When they inspect importance, `monthly_spend` appears around the middle or higher, while `yearly_spend_div_12` appears almost at the bottom.

The easiest human-first judgment here is `yearly_spend_div_12 is unnecessary. Let's remove it.` But if the two features carry almost the same information, then a low importance is closer to `another feature is already providing similar explanation` than to `this feature is useless`.

What matters here is not the importance number itself, but `the before/after removal comparison`. After removing the low-importance feature, we need to inspect together how performance and interpretation change. If the performance changes very little, the redundancy may indeed be strong. But if the explanation of certain cases collapses or the permutation results change, then that feature may still have been playing a supporting role.

So rather than reading a low importance immediately as `a feature to discard`, it is safer to ask first: `is the information overlapping?`, `did it matter only for certain cases?`, and `what changes before and after removal?`

### How Is It Better To Read It In Practice?

Feature importance is used more conservatively in the following way.

| Good use | Risky use |
| --- | --- |
| inspect what signals the model mainly looks at | turn the ranking into a ranking of causes |
| inspect whether strange columns rose to the top | delete low-number features immediately |
| cross-check with permutation results | conclude from one training-data-based MDI value alone |
| inspect correlation and data meaning together | change policy from the number alone |

In the end, importance is `the starting point of an explanation tool`, not `the final verdict`.

Compressed into project-note style:

| Record item | Example |
| --- | --- |
| observed importance | `petal length = 0.444` |
| safe interpretation | `this model used this feature often` |
| review_needed | `there are correlated features, so do not overtrust it` |
| next_question | `should we also inspect permutation importance?` |

With this table, the feature-importance Section reads as `observed importance -> interpretation boundary -> next question`. What matters in the end is not the rank order itself, but whether we also write down `what this importance observation helps explain` and `from where overtrust is still dangerous`.

### The Minimum Interpretation Memo To Leave After Seeing Importance

In practice, teams often save only the importance table and stop there. But later, that leaves no record of `why did we trust this number` and `where did we stop interpreting it`.

It is better to leave at least the following four lines together.

| Item | Example note |
| --- | --- |
| observed importance | `recent_visits came out highest` |
| interpretation boundary | `this value is a usage trace inside the model, not a ranking of causes` |
| review target | `need to check the correlation between discount_clicks and recent_visits` |
| next action | `add permutation importance and before/after removal comparison` |

With that memo, the importance Section stops being only an explanation and turns into a learning record that leads to the next experiment.

## Practice And Example

### Python Example: Inspect MDI

This example is the smallest exercise that reads `feature_importances_` directly after training a random forest.

- problem situation: inspect which features are used more importantly in the iris data
- input: the 4 iris features
- label: species class
- concepts to check:
  - importance is a relative share
  - the sum of the values is close to 1

```python
# This example reads MDI-based feature importance through feature_importances_ in a random forest.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

print("test accuracy:", round(model.score(X_test, y_test), 3))
print("feature importances:")

for name, score in zip(feature_names, model.feature_importances_):
    print(f"  {name:20} {score:.3f}")

print("sum:", round(model.feature_importances_.sum(), 3))
```

An example output is as follows.

```text
test accuracy: 0.911
feature importances:
  sepal length (cm)    0.098
  sepal width (cm)     0.028
  petal length (cm)    0.444
  petal width (cm)     0.430
sum: 1.0
```

What should be read here is:

1. importance appears as a relative share
2. petal length and petal width were used more in this model
3. this is `a branching-usage trace of this model`,
not an immediate causal explanation

### Python Example: Read It Next To Permutation Importance

This time we inspect permutation importance together for the same model.

Problem situation:

- one importance number can look like a fixed fact,
but the result can change once the calculation method changes

Input:

- iris dataset
- a trained random-forest model

Expected output:

- MDI-based importance
- permutation-importance results

Concepts to check:

- MDI and permutation importance do not necessarily return the same values
- when the two numbers differ, first recall that they answer different questions

```python
# This example compares MDI and permutation importance side by side on the same model.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

baseline_accuracy = model.score(X_test, y_test)

perm = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=20,
    random_state=42
)

print("baseline accuracy:", round(baseline_accuracy, 3))
print("feature".ljust(20), "MDI".rjust(8), "perm_mean".rjust(12))
for i, name in enumerate(feature_names):
    mdi = model.feature_importances_[i]
    pmean = perm.importances_mean[i]
    print(f"{name:20} {mdi:8.3f} {pmean:12.3f}")
```

An example output is as follows.

```text
baseline accuracy: 0.911
feature                   MDI    perm_mean
sepal length (cm)       0.098        0.011
sepal width (cm)        0.028        0.000
petal length (cm)       0.444        0.222
petal width (cm)        0.430        0.189
```

This result means the following.

- the two methods may have similar rankings, or they may differ
- even for the same feature, `was it used a lot in branching?`
and `how much does performance fall when it is shuffled?` are different questions
- therefore it is dangerous to finish the interpretation from only one importance number

### Try Interpreting It Yourself

Before moving on, look at the following observations and decide which interpretation is safer.

| Observation | Hasty conclusion | Safer interpretation |
| --- | --- | --- |
| `petal length` has the largest MDI | it is the strongest cause | it is the feature this model used most often in branching |
| `sepal width` has a permutation value close to 0 | it is completely useless | another feature may still be standing in for similar information |
| MDI and permutation values differ | one of them is wrong | the two numbers answer different questions |

The purpose of this table is not to test whether you found one correct answer. It is to build the habit of asking `what question does this number answer?` before jumping straight to a conclusion.

### Why Should We Be Careful With High-Cardinality Features?

Tree-family models can react easily to features with many unique values. That is because such features create many opportunities to split the training data finely.

For example:

- customer ID
- order number
- raw timestamp

Columns like these may look important not because of business meaning, but because `they offer too many split candidates`.

So whenever we inspect importance, we also ask:

`Is this really a meaningful variable, or is it only a column that is easy to split finely?`

### Why Should We Be Careful With Correlated Features?

For example, if both `monthly_spend` and `yearly_spend / 12` enter the model together, then the model may use one more often and the other less often.

As a result:

- one importance becomes high
- the other becomes low

But that does not mean the lower one is useless. It may simply have been substituted because the information overlaps.

That is why importance interpretation should always travel with the following questions.

- Are there several features with similar meaning?
- Is a feature with a large number truly important on its own?
- Is a feature with a small number being hidden by another feature?

## Checklist

- Are you reading importance as if it were a ranking of causes?
- Can you distinguish that MDI and permutation importance answer different questions?
- Are you first checking whether there are correlated features or high-cardinality columns?
- Can you explain that feature importance is a tool that summarizes what the model looked at, that MDI is an internal summary, and that permutation importance is an external check?
- Can you explain that the importance number does not directly mean causality or a true ranking of causes?
- Can you explain that high-cardinality and correlated features can distort interpretation?

## Sources And References

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Permutation feature importance`, scikit-learn User Guide, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/permutation_importance.html](https://scikit-learn.org/stable/modules/permutation_importance.html){: target="_blank" rel="noopener noreferrer" }
- Gilles Louppe, *Understanding Random Forests: From Theory to Practice*, PhD Thesis, University of Liege, 2014. [https://arxiv.org/abs/1407.7502](https://arxiv.org/abs/1407.7502){: target="_blank" rel="noopener noreferrer" }
