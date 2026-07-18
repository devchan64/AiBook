# P4-14.1 Decision Tree

> Section ID: `P4-14.1`
> Version: `v2026.07.12`

P4-11 read classification through drawing a boundary. P4-12 read it through nearby neighbors. P4-13 read it through margin as a criterion for a better boundary. Now the same supervised learning problem is read again in a very different way.

If P4-13.2 held onto the idea that the same data can be reread in a different feature space, this Section reorganizes the same tabular data through a new question: `in what order should we split it with questions?` What changes here is not the problem itself. What changes is the unit used to summarize the same problem.

Instead of drawing one line at once, imagine splitting cases step by step with questions. That makes the starting point of a decision tree easier to see. A decision tree does not try to explain the data all at once. It repeats yes/no questions, groups more similar cases together, and then predicts. So a decision tree is closer to `a question flow` than to `a single boundary line`.

This Section explains the basic meanings of `decision tree`, `split`, `node`, and `leaf`. Later Sections continue the current line of judgment from those handles, and the basic sense of predicting by chaining questions reconnects through this Section and the [concept glossary](/AiBook/reference/concept-glossary/).

## Scope Of This Section

This Section answers the following questions.

- How does a decision tree make a prediction?
- What are `split`, `node`, and `leaf`?
- Why is a tree often treated as a comparatively readable model?
- What kinds of question candidates are compared during training?
- Why can the same structure be used for both classification and regression?

This Section does not go deeply into the following topics.

- overfitting as the tree becomes deeper
- detailed pruning procedures
- random forest and gradient boosting
- formula derivations for entropy and information gain

Those topics continue in P4-14.2, P4-15, and P4-16.

## Goals Of This Section

- You can explain a decision tree as `a model that predicts by splitting with questions`.
- You can explain the meanings of split, node, leaf, and threshold.
- You can understand that decision trees can be used for both classification and regression.
- You can explain that training is `a repetition of choosing promising questions`.
- You can distinguish between `readability` and `the risk of becoming too deep`.

## Learning Background

The representative models seen in the earlier chapters tend to leave these impressions.

- linear regression: read a relationship with a line or plane
- logistic regression: read a decision boundary and a probability-like output
- k-NN: read nearby neighbors
- SVM: read a boundary with more room

A decision tree changes the question itself.

| Earlier viewpoint | Question changed by a decision tree |
| --- | --- |
| Can one boundary be drawn well? | Which question splits the data well? |
| Are distance and margin central? | If we split now, do the labels become cleaner? |
| Do we express the trend with a formula? | Can we separate cases as a flow of conditions? |

In other words, a decision tree shifts the view from `a model that draws a line in space` to `a model that chains questions`. That viewpoint connects directly to understanding random forest and boosting later.

This Section also connects directly to the comparison-record structure that Part 4 has been building. When a tree is raised as a candidate, it is not enough to record only `what the first split is`. It also helps to leave behind `which cases stay near that split`, `what is easier to read than the baseline or another candidate`, and `what split question should be checked next`. Even when two models look similar in score, one tree may still mix more classes inside a particular leaf. So the pattern left after the split should be read separately too.

| Record to keep together | Why it matters |
| --- | --- |
| baseline vs. decision tree | to see what the rule-like question flow actually explains better |
| cases near the first split | to recheck which cases are ambiguous near the question boundary |
| representative cases gathered in each leaf | to see what kind of group the split really created |
| next question | to decide whether to grow deeper or split with another feature |

### When It Is Good To Raise A Decision Tree Early

A decision tree is often a strong first candidate when `the question flow itself` becomes part of the explanation.

| Current problem state | Why raise a decision tree early | What to check first |
| --- | --- | --- |
| A condition-like explanation matters | the branching flow can be read in language closer to human rules | whether the first split is too far from domain common sense |
| Tabular features are central | numeric and categorical features are easy to split with threshold questions | which features dominate the branching |
| A question order feels more natural than a linear boundary or distance rule | stepwise separation may be more explanatory than the whole space at once | whether cases are still mixed too much inside each leaf |
| You want to compare classification and regression with one structure | only the leaf output changes while the structure can stay similar | whether the evaluation metric matches the problem type |
| You may extend later to random forest or boosting | it helps to establish the starting structure of the whole tree family first | whether depth and leaf-size controls are already understood |

The point of this table is not to leave the tree at `a readable model`. It is to position it as `a candidate to try first when the question flow itself becomes a real unit of explanation`.

## Main Learning Content

### What Kind Of Model Is A Decision Tree?

The scikit-learn User Guide introduces decision trees as non-parametric supervised-learning methods used for classification and regression. The same guide explains their goal as learning simple decision rules inferred from data features to predict a target value. It also notes that the structure can be viewed as a piecewise constant approximation.

That can be restated more simply like this.

`A decision tree looks at input features, asks questions such as whether a value is above or below a threshold, splits the input space into several pieces, and places a representative prediction value on each piece.`

Think about churn prediction for a subscription service.

| Feature | Example question |
| --- | --- |
| number of visits in the last 30 days | are visits 3 or fewer? |
| late payment flag | was there a recent late payment? |
| support-contact count | were there at least 2 support contacts? |

A decision tree chooses one of those questions first and splits the data according to the answer. Then it may continue with another question inside each branch.

### Read It First As A Small Flow

Before treating a decision tree as a learner, read it first as `a decision flow that moves downward through questions`.

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-1-mermaid-01-en.mmd"
```

This diagram helps the reader see a decision tree as `a flow that reaches a leaf by following questions`. Unlike a model that draws one boundary all at once, a tree narrows the cases into more similar groups by going through intermediate questions in sequence.

The key pieces in the diagram are the following.

- the question boxes in the middle are `nodes`
- the places where the flow branches according to the answer are `splits`
- the endpoints that stop asking questions and output a prediction are `leaves`

So a decision tree can be read as `a structure that follows question nodes until it reaches a leaf`.

Compressed into project-note style, it becomes something like this.

| Record item | Example |
| --- | --- |
| first split | `visits <= 3` |
| near-split cases | `customer C`, `customer D` |
| current leaf prediction | `churn` or `stay` |
| needs review? | `recheck customers near the split boundary` |
| next question | `should late_payment be the next split?` |

With this table, the introduction to decision trees reads as `candidate comparison -> near-split cases -> next question`. At this point, it helps to read both the near-split cases and the leaf composition together. Only then can we distinguish between a tree that is easier to read and a tree that is more fragile even when the accuracy looks similar.

### How Should Node, Split, And Leaf Be Understood?

In this Section it matters to keep the terms short and clear.

| Term | Simple explanation | Role in this Section |
| --- | --- | --- |
| node | a place where a question sits | it places a criterion for splitting data |
| split | the act of branching according to a question | it tries to create more similar groups |
| leaf | the endpoint where the final prediction is written | it outputs a class or a number |
| threshold | a cutoff value for a number | it creates a question such as `x <= 3.5` |

These terms connect immediately to the later hyperparameter discussion too.

- `max_depth` is connected to how deep the tree is allowed to grow.
- `min_samples_split` is connected to whether a node has enough examples to split again.

But in this Section the focus is still not `how far should the tree be allowed to grow`. The focus is `what kind of structure is a question-splitting model itself`.

## Detailed Learning Content

### Why Is It Often Called A Comparatively Readable Model?

Among the models first encountered in Part 4, decision trees are comparatively easy to `read like rules`. The scikit-learn User Guide explains this through the viewpoint of a `white box model`. If a situation is visible inside the model, the condition can often be explained with fairly direct boolean logic. Compared with the weights of a linear model or the margin of an SVM, the structure `follow the questions and a prediction appears` feels more familiar to many readers.

Compare the following two explanations.

- linear model: if the weighted sum of several features is above a threshold, predict positive
- decision tree: if recent visits are low and there was a late payment, churn is more likely

Both are models. But the second one looks closer to how people read business rules.

This advantage is also mentioned often in practice.

| Situation | Advantage a decision tree gives |
| --- | --- |
| churn analysis | it is easier to see in what order the questions separated churn |
| loan-review support | it is easier to explain which condition created the first branch |
| equipment anomaly detection | it is easier to read what sensor-value range created a branch |

At the same time, one caution should be attached immediately.

`Being easier to read is not the same thing as always giving better generalization.`

That risk is taken up directly in the next Section, P4-14.2.

### What Does It Mean That Trees Work For Both Classification And Regression?

A decision tree can be used for both classification and regression. What changes is `what the leaf outputs`.

| Problem type | What the leaf outputs |
| --- | --- |
| classification | the most frequent class, or class proportions |
| regression | a representative number such as the average of values in that leaf |

For example:

- churn prediction: `churn` or `stay`
- housing-price prediction: `predicted price 520 million KRW`

So the tree structure remains similar while the character of the final output changes. The scikit-learn explanation of `predict_proba` also reads the class probability in a classification tree as the proportion of samples from the same class inside that leaf. That is why, as emphasized in the Part 4 metrics discussion, the reader should first confirm whether the current problem is classification or regression before focusing on the algorithm name.

### How Does Training Choose Questions?

The core of decision-tree training is `comparing question candidates that look promising`.

1. Look at several features.
2. Create threshold candidates for each feature.
3. Calculate whether the labels become more organized after the split than before it.
4. Place the best question at the current node.
5. Repeat inside each branch if needed.

Drawn simply, the flow becomes the following.

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-1-mermaid-02-en.mmd"
```

This diagram shows that decision-tree training is fundamentally `a repetition of choosing a good first question and the next question`. It compares feature and threshold candidates, chooses the split that reduces impurity better, and then repeats the same procedure in each branch.

Here `impurity` refers to how mixed the inside of a node is. In API terms, a classification tree can use criteria such as `gini`, `entropy`, or `log_loss`. Rather than memorizing formulas first, it is enough at this stage to hold onto the intuition that `impurity is high when classes are mixed inside a node, and low when the node becomes more organized around one class`.

### Read Impurity Intuitively

In a classification tree, the reader wants to know whether `asking this question made the labels cleaner`.

Suppose a node contains 10 customers.

- 5 are churn
- 5 are stay

That is a fairly mixed node.

Now suppose a question splits them into:

- left branch: 4 churn, 1 stay
- right branch: 1 churn, 4 stay

Then both branches can be read as cleaner than the original node.

So a good split is often `a question that turns one mixed node into less mixed nodes`.

## Cases And Examples

### Case 1. When You Want To Narrow Churn Step By Step With Questions

A subscription-service team is building a churn-prediction model. The criteria people looked at first were questions such as `are recent visits low?`, `was there a late payment?`, and `are support contacts frequent?`

Instead of computing one score at once as in a linear model, the team wants a question flow that the business side can read. So it starts with a question such as `are visits 3 or fewer?`, then asks `was there a late payment?`, and in this way customers with more similar behavior start gathering into the same branch. At this point the decision tree is read not as one boundary line but as a model that finds `a good order of questions`.

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-1-mermaid-03-en.mmd"
```

What matters in this scene is that the questions themselves are selected from the data. The model is not using arbitrary conditions. It compares features and thresholds to find the split that organizes the current node better, chooses that as the first branch, and then repeats the same procedure. So a decision tree is not a model where humans write rules at will. It is a model that accumulates questions that clean up the data better.

The observable result appears in the scores used to compare first-split candidates and in the final small-tree structure. If `visits <= 3` separates the data better than the other questions, we can explain why that question was placed at the first node. And by looking at which customers gathered in each leaf, we can check how the tree becomes readable like a rule.

### How This Can Be Read In Work Scenes

Decision trees are especially common when `tabular data` is central. The reason is simple: it is comparatively natural to split numeric and categorical features with thresholds or condition questions.

| Work scene | Decision-tree-style question |
| --- | --- |
| customer churn | are recent visits low? was there a late payment? |
| loan-review support | is income above a threshold? is there a delinquency record? |
| equipment anomaly detection | did the temperature exceed a threshold? is vibration outside a range? |
| marketing-response prediction | was there a recent purchase? is the response rate to discount messages high? |

In these scenes, a decision tree may feel more intuitive than a linear model. On the other hand, caution is needed when the data follow a very smooth continuous relationship or when the structure changes sharply under small perturbations. As the API documentation warns, if no size-control values are set, the tree can grow into a fully grown and unpruned structure. That is exactly where the next Section connects to overfitting.

## Practice And Examples

### Python Example: Finding `A Good First Question`

This practice does not start by calling a scikit-learn learner directly. Instead, it is a small exercise that lets the reader see how a decision tree might choose the first split.

- problem situation: choose the first question for churn classification
- input: `visits`, `late_payment`
- label: `stay`, `churn`
- concepts to check:
- the split score changes when the feature or threshold changes - a question that organizes the labels better can become a better first split - tree training is a repetition of this kind of question selection

```python
rows = [
    {"customer": "A", "visits": 1, "late_payment": 1, "label": "churn"},
    {"customer": "B", "visits": 2, "late_payment": 1, "label": "churn"},
    {"customer": "C", "visits": 2, "late_payment": 0, "label": "stay"},
    {"customer": "D", "visits": 4, "late_payment": 0, "label": "stay"},
    {"customer": "E", "visits": 5, "late_payment": 0, "label": "stay"},
    {"customer": "F", "visits": 6, "late_payment": 1, "label": "stay"},
]


def gini(group):
    total = len(group)
    if total == 0:
        return 0.0

    counts = {}
    for row in group:
        counts[row["label"]] = counts.get(row["label"], 0) + 1

    score = 1.0
    for count in counts.values():
        p = count / total
        score -= p * p
    return score


def weighted_gini(left, right):
    total = len(left) + len(right)
    return (len(left) / total) * gini(left) + (len(right) / total) * gini(right)


candidates = [
    ("visits", 1.5),
    ("visits", 3.0),
    ("visits", 5.5),
    ("late_payment", 0.5),
]

best = None

for feature, threshold in candidates:
    left = [row for row in rows if row[feature] <= threshold]
    right = [row for row in rows if row[feature] > threshold]
    score = weighted_gini(left, right)

    print(f"feature={feature:12} threshold={threshold:>3} weighted_gini={score:.3f}")
    print("  left :", [(row["customer"], row["label"]) for row in left])
    print("  right:", [(row["customer"], row["label"]) for row in right])
    print()

    if best is None or score < best["score"]:
        best = {"feature": feature, "threshold": threshold, "score": score}

print("best first split")
print(best)
```

An example output is as follows.

```text
feature=visits       threshold=1.5 weighted_gini=0.400
  left : [('A', 'churn')]
  right: [('B', 'churn'), ('C', 'stay'), ('D', 'stay'), ('E', 'stay'), ('F', 'stay')]

feature=visits       threshold=3.0 weighted_gini=0.222
  left : [('A', 'churn'), ('B', 'churn'), ('C', 'stay')]
  right: [('D', 'stay'), ('E', 'stay'), ('F', 'stay')]

feature=visits       threshold=5.5 weighted_gini=0.400
  left : [('A', 'churn'), ('B', 'churn'), ('C', 'stay'), ('D', 'stay'), ('E', 'stay')]
  right: [('F', 'stay')]

feature=late_payment threshold=0.5 weighted_gini=0.250
  left : [('C', 'stay'), ('D', 'stay'), ('E', 'stay')]
  right: [('A', 'churn'), ('B', 'churn'), ('F', 'stay')]

best first split
{'feature': 'visits', 'threshold': 3.0, 'score': 0.2222222222222222}
```

Three things matter in this output.

1. Not every question gives the same quality.
2. `visits <= 3.0` looks like the first question that organizes the current data best.
3. A tree builds its structure by repeating this comparison.

So a decision tree is not `a model where someone writes questions by intuition`. It is `a model that keeps finding questions that organize the data better`.

At the same time, it is worth taking one more step: `a good first question` can change even under a small data change. If customer `F` had label `churn` instead of `stay`, the `late_payment` question could begin to look stronger. So the first split is not an absolute rule. It depends on how the current training data are forming groups.

### Change One Value And Check Whether The First Split Shifts

Keep the same example and change only one value. Then it becomes easier to see `how sensitive the first question can be`.

- value to change: the `label` of customer `F`
- reason for the change: intentionally create a setting where `late_payment` looks like a stronger signal
- concepts to check:
- split scores change when the data composition changes - a decision tree changes its question flow according to the direction that organizes the current data better - when reading the first split, it helps to read both the score and the cases that changed the criterion

```python
changed_rows = [row.copy() for row in rows]
for row in changed_rows:
    if row["customer"] == "F":
        row["label"] = "churn"

best_changed = None

for feature, threshold in candidates:
    left = [row for row in changed_rows if row[feature] <= threshold]
    right = [row for row in changed_rows if row[feature] > threshold]
    score = weighted_gini(left, right)

    print(f"feature={feature:12} threshold={threshold:>3} weighted_gini={score:.3f}")

    if best_changed is None or score < best_changed["score"]:
        best_changed = {"feature": feature, "threshold": threshold, "score": score}

print("best first split after one label change")
print(best_changed)
```

An example output is as follows.

```text
feature=visits       threshold=1.5 weighted_gini=0.500
feature=visits       threshold=3.0 weighted_gini=0.444
feature=visits       threshold=5.5 weighted_gini=0.267
feature=late_payment threshold=0.5 weighted_gini=0.250
best first split after one label change
{'feature': 'late_payment', 'threshold': 0.5, 'score': 0.25}
```

The key point in this comparison is this: `at first visits looked better, but after changing one label, late_payment moved up as the first question`. That does not mean the tree should simply be declared unstable. It means that when reading the branching structure, the reader should also inspect `which cases the current data place where`.

A short record can summarize the same comparison like this.

| Comparison point | Original data | After label change |
| --- | --- | --- |
| first split | `visits <= 3.0` | `late_payment <= 0.5` |
| case that moved the structure | `F` does not change the first split | changing the label of `F` changes the first split |
| what to review first | why is `C` grouped with `visits`? | why does `F` push the structure under `late_payment`? |

The point of this table is not only to summarize `what changed`. For a beginner, it is useful to write down once `which case really changed the question choice`. That makes it easier to connect naturally to the next Section, where depth and leaf size can shake the structure even more.

It is also worth answering the following questions directly.

1. Which single case changed the first-split choice?
2. When the score difference is small, should human readability also be considered?
3. How does this sensitivity seem likely to connect to depth, leaf size, and overfitting in the next Section?

If possible, write one more sentence: `In the current data, visits was the first question, but after changing only the label of F, late_payment became the better first question.` Writing that sentence directly helps make it clear that a decision tree is not `memorizing a fixed rule`, but `choosing questions that organize the current data better`.

### Apply A Very Small Tree By Hand

Using the first split found above, a very small tree that a person can read looks like this.

```text
if visits <= 3:
    if late_payment == 1:
        predict churn
    else:
        predict stay
else:
    predict stay
```

This code is not `the whole learner`. It is a simplified reading of the result of training. When people say a decision tree looks comparatively explainable, they usually have a shape like this in mind.

It becomes clearer if the same structure is run in a very short Python example.

Problem situation:

- instead of looking at a decision-tree rule only as a picture, it helps to put in real inputs and check how the result comes out

Input:

- a simple tree rule `predict`
- a list of example customers `examples`

Expected output:

- the prediction result for each example customer

Concepts to check:

- a decision tree can be read as an if-else branching rule
- what people mean by higher explainability is close to saying that a person can follow this branching process

```python
def predict(tree_input):
    if tree_input["visits"] <= 3:
        if tree_input["late_payment"] == 1:
            return "churn"
        return "stay"
    return "stay"


examples = [
    {"customer": "G", "visits": 2, "late_payment": 1},
    {"customer": "H", "visits": 2, "late_payment": 0},
    {"customer": "I", "visits": 5, "late_payment": 1},
]

for row in examples:
    print(row["customer"], "->", predict(row))
```

An example output is as follows.

```text
G -> churn
H -> stay
I -> stay
```

This example shows three important characteristics of decision trees.

- the prediction path can be read step by step
- it is easy to explain at which question the flow branched
- if more and more questions are added, the structure can become large very quickly

That last point is exactly the topic of the next Section.

### Practice: Leave A Small Tree Record Yourself

If you ran the two exercises above, do not stop at only looking at the results. Leave a short record.

1. Write what the first split was in the original data.
2. Write what the first split changed to after modifying one label.
3. In both cases, choose one `most ambiguous case`.
4. Finally, write one sentence answering whether you want to grow the tree deeper right away, or first inspect depth limits in the next Section.

If possible, fill the following format yourself.

| Record item | Original data | After label change |
| --- | --- | --- |
| first split | `visits <= 3.0` | `late_payment <= 0.5` |
| most ambiguous case | `C` | `F` |
| place where the leaf is most mixed | left group of `visits <= 3.0` | right group of `late_payment > 0.5` |
| next question | should `late_payment` be the next split? | should the leaf be checked before growing deeper? |

The point of this exercise is not to memorize the answer. It is to build the habit of reading a decision tree not only as `one score`, but as `a question structure and a set of grouped cases`.

At first, even a shorter note like the following is enough.

| Example note | Original data | After label change |
| --- | --- | --- |
| first split | `visits <= 3.0` | `late_payment <= 0.5` |
| most ambiguous case | `C` | `F` |
| next question | should `late_payment` be the next split? | should the leaf be checked before growing deeper? |

## Checklist

- In the current problem, is a question flow more natural than a straight-line boundary?
- Can you recheck what groups of cases were created by the first split and the leaf structure?
- Are you keeping readability and generalization performance separate instead of mixing them into the same claim?

## Sources And References

- scikit-learn developers, `1.10. Decision Trees`, scikit-learn User Guide, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/tree.html](https://scikit-learn.org/stable/modules/tree.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `DecisionTreeClassifier`, scikit-learn API Reference, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984.
