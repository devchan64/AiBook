# P4-14.2 Overfitting In Trees

> Section ID: `P4-14.2`
> Version: `v2026.07.26`

P4-14.1 read a [decision tree](/AiBook/en/reference/concept-glossary-alpha/d/#decision-tree) as `a model that predicts by splitting with questions`. That Section had clear strengths.

- it is easy to read as a question flow
- it is easy to explain like a chain of conditions
- it often feels intuitive on tabular data

But the same property also leads directly to risk. If the model can keep adding questions, the tree may end up almost memorizing the training data. That is exactly where tree [overfitting](/AiBook/en/reference/concept-glossary-alpha/o/#overfitting) appears.

If P4-14.1 asked `how should a good first question and the next question be read?`, this Section asks `where does that question flow stop describing a pattern and start memorizing exceptions?` So here the reader must see not only when making the tree deeper helps, but also when that deeper structure begins to shake the model.

This Section does not repeat the base definition of a decision tree at length. The core intuition `it predicts by splitting with questions` reconnects through P4-14.1 and the [decision tree](/AiBook/en/reference/concept-glossary-alpha/d/#decision-tree) entry, while the general handle for overfitting itself should be recalled again through [overfitting](/AiBook/en/reference/concept-glossary-alpha/o/#overfitting) and P4-5.1.

## Questions Closed By Tree Overfitting

This Section answers the following questions.

- Why does overfitting stand out so easily in decision trees?
- What happens as the tree grows deeper?
- What roles do [max_depth](/AiBook/en/reference/concept-glossary-alpha/m/#max-depth), [min_samples_leaf](/AiBook/en/reference/concept-glossary-alpha/m/#min-samples-leaf), and [ccp_alpha](/AiBook/en/reference/concept-glossary-alpha/c/#ccp-alpha) play?
- Why can train performance and test performance move differently?

This content reconnects with P4-15, P4-16, and the tuning context of P4-9. In other words, this Section first holds onto the point where a tree's question flow stops explaining patterns and starts memorizing exceptions.

## Judgments To Keep From Tree Overfitting

- You can explain tree overfitting as `the phenomenon where overly detailed questions memorize the training data`.
- You can explain that depth, leaf size, and [pruning](/AiBook/en/reference/concept-glossary-alpha/p/#pruning) are tools for controlling tree complexity.
- You can recheck that higher train performance does not guarantee higher test performance.
- You can gain a criterion for reading both the strengths of trees and the risk of overfitting together.

## Learning Background

### Why Is Overfitting So Visible In Trees?

A decision tree is fundamentally `a structure that keeps splitting nodes into smaller pieces`. That structure is powerful. But if no limits are given, it can create smaller and smaller leaves.

The scikit-learn User Guide explains that decision-tree learners can create `over-complex trees`, and that such trees generalize poorly. The same guide calls this overfitting and explains why controls such as pruning, `min_samples_leaf`, and `max_depth` are needed.

`As a tree keeps adding questions, it can begin to follow exceptions in the training data too closely. But there is no guarantee that those exceptions will repeat in new data.`

Here too it helps to keep a fixed record structure. This Section is not only saying `depth can become dangerous`. It is a Section for recording `what new failure appears as complexity grows`, `which review cases keep remaining`, and `at what point branches should be stopped or reduced`. Even when two models show similar average scores, a deeper tree may memorize a new set of cases while still leaving the same failures unresolved. That difference must be read separately.

| Record to keep together | Why it matters |
| --- | --- |
| change in depth or leaf size | to see how the complexity control actually moved |
| train/test difference | to distinguish memorization from generalization |
| failure cases that keep remaining | to recheck cases that are still unresolved even after more branching |
| next pruning question | to decide whether `max_depth`, `min_samples_leaf`, or `ccp_alpha` should be adjusted next |

### When Should Tree Overfitting Be Suspected Early?

To catch overfitting quickly, the reader should not watch only the score. It also helps to ask `have the questions become too fine-grained?`

| Visible sign | What to suspect first | Why |
| --- | --- | --- |
| train is almost perfect but test falls | too much depth | the tree may have started memorizing the training data |
| one leaf contains only a tiny number of samples | undersized leaves | the model may be treating exceptions like stable patterns |
| more branches still leave the same failure cases | the wrong kind of complexity increase | only the number of questions increased while the core problem stayed unsolved |
| too many branches appear after the first split | overly fine later-stage splitting | the later branches may be following accidental fluctuations |
| the explanation became long, but harder to interpret | pruning is needed | the advantage of readability is disappearing |

This table helps the reader go beyond the vague statement `deeper trees are risky`. Instead it frames the real question as: `At what point do the questions stop talking about a pattern and start talking about exceptions?`

## Main Learning Content

### Intuition By Comparing Small And Large Trees

Think again about churn data.

| Tree state | Intuition |
| --- | --- |
| shallow tree | it sees only the large tendency |
| moderately deep tree | it balances major patterns and useful exceptions |
| overly deep tree | it follows accidental fluctuations in the training data |

The same point can be compressed into the following diagram.

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-01-en.mmd"
```

This diagram shows that tree overfitting is not `the more questions, the better`. More splits may fit the training data better. But at the last stage, memorization may begin instead of generalization.

The key is the final arrow.

`Fits better` and `generalizes better` are not the same statement.

In project-note style, the same point becomes something like this.

| Record item | Example |
| --- | --- |
| complexity change | `max_depth 3 -> 5` |
| train change | `0.971 -> 1.000` |
| test change | `0.933 -> 0.911` |
| needs review? | `depth increased, but failure cases remain` |
| next question | `should leaves be enlarged or should pruning be used?` |

This table lets the overfitting Section read as `complexity change -> remaining failures -> next pruning question`. What matters is not just one cell of numbers. It is whether the remaining failure pattern became simpler, or the model only matched the training data more closely.

### What Happens As The Tree Gets Deeper?

As the tree gets deeper, fewer samples remain inside each leaf. Then several things happen.

1. One or two exceptional cases can create an extra branch.
2. A leaf may begin to predict after seeing only a tiny number of samples.
3. On the training set, the model may become almost error-free.
4. On the test set, the prediction may become much easier to shake under a small change.

The scikit-learn documentation notes that each extra level in the tree needs roughly twice as many samples to fill it, and recommends controlling size with `max_depth`. It also recommends `min_samples_split` and `min_samples_leaf` so that decisions are based on more than only a handful of samples.

Compressed into one sentence:

`As a tree becomes deeper, it can become more detailed. But if there are not enough data to support that detail, the tree may become sensitive rather than truly smarter.`

### Read Overfitting As A Data Flow

Overfitting lasts longer in memory when it is understood as a flow rather than only as a formula.

The early branches often catch meaningful large patterns. The problem tends to start later. The last few stages may explain not `the real structure`, but `accidental fluctuations that appeared only in the training data`.

That flow can be read in stages like this.

| Flow stage | What the tree is mainly doing | Question to raise first |
| --- | --- | --- |
| early branches | splitting large patterns | is it catching a truly important difference? |
| middle branches | adding exceptions and subpatterns | is it still looking at a structure that repeats? |
| later branches | separating tiny groups of cases | is it now memorizing accidental fluctuations? |
| final leaves | becoming almost training-data-only rules | would this leaf survive on new data too? |

For example, an early branch may use a broad criterion such as `is the temperature high and vibration large?` or `do we see both reduced visits and a complaint signal?` Later branches may move toward narrow questions such as `did the value fluctuate only at the third time point?` or `did visits drop twice only during a specific week?`

So the real issue is not simply that `there are many questions`. It is whether `the nature of the questions changed from describing a major pattern to describing training-data exceptions`.

### Why Train And Test Performance Must Be Read Together

Tree overfitting becomes especially visible when train and test performance are read together.

| Observation | Interpretation |
| --- | --- |
| both train and test are low | the model may still be too simple to learn enough |
| both train and test are high | the current balance may look acceptable |
| only train is very high while test falls | overfitting should be suspected |

This viewpoint appears often in trees, but it is really a shared Part 4 principle. Linear regression, logistic regression, SVM, and tree models all eventually face the same question: `how well does the model hold up on data it has not seen?`

## Detailed Learning Content

### Why Is `min_samples_leaf` Needed?

If `max_depth` limits the overall height of the tree, `min_samples_leaf` limits how small one leaf is allowed to become.

The API explains `min_samples_leaf` as the minimum number of samples required to be in a leaf node. It also notes that in regression it can have a smoothing effect.

`If a leaf is allowed to contain only one or two cases, that leaf becomes more likely to talk about exceptions than about patterns.`

For example:

- `min_samples_leaf=1`: even a leaf with only one case is allowed
- `min_samples_leaf=5`: at least five cases are needed before a leaf is accepted

This difference can be reread as: `how small an exception group are we willing to trust?`

### Python Example: Controlling Leaf Size

This time, keep the depth unfixed and change only the leaf size.

Problem situation:

- on the same data, changing how small a leaf is allowed to be can change how train and test should be read

Input:

- `X_train`, `X_test`, `y_train`, `y_test` from the iris dataset
- several `leaf_size` values

Expected output:

- train score by leaf size
- test score by leaf size

Concepts to check:

- when leaves are too small, the train score rises easily
- enlarging the leaf may make the structure less sensitive

```python
# This example changes min_samples_leaf to see how small-leaf limits affect train/test scores and tree structure.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for leaf_size in [1, 2, 5, 10]:
    model = DecisionTreeClassifier(
        min_samples_leaf=leaf_size,
        random_state=42
    )
    model.fit(X_train, y_train)

    print(f"min_samples_leaf={leaf_size}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(model.score(X_train, y_train), 3))
    print("  test accuracy  :", round(model.score(X_test, y_test), 3))
    print()
```

An example output is as follows.

```text
min_samples_leaf=1
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911

min_samples_leaf=2
  depth          : 4
  leaves         : 7
  train accuracy : 0.981
  test accuracy  : 0.933

min_samples_leaf=5
  depth          : 3
  leaves         : 4
  train accuracy : 0.971
  test accuracy  : 0.933

min_samples_leaf=10
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
```

This example gives one important intuition.

`Blocking very small leaves does not automatically make performance worse. In some cases, the test side becomes more stable instead.`

### What Does Pruning Do?

If limiting depth in advance can be read as pre-pruning, then simplifying a tree after it has grown can be read as pruning.

scikit-learn supports `Minimal Cost-Complexity Pruning`. The API explains `ccp_alpha` as the complexity parameter for that pruning. As the value becomes larger, more nodes can be cut away.

- `max_depth`, `min_samples_leaf`: keep the tree from becoming too complex from the start
- `ccp_alpha`: give a complexity cost after growth and simplify the tree

The goal is the same in both cases.

`Leave a structure that survives on new data, rather than only memorizing the training data.`

The first distinction a beginner should hold is `when the intervention happens`.

| Method | When it intervenes | First meaning to read |
| --- | --- | --- |
| `max_depth`, `min_samples_leaf` | while the tree is growing | stop overly detailed branching from the start |
| pruning, `ccp_alpha` | after the tree has already grown | trim away small branches with weak effect |

So pre-pruning is `a handle that prevents the tree from growing too deeply in the first place`, while pruning is `a handle that reselects which branches should remain after the tree has grown once`.

A small scene makes this clearer.

| Branch state | Before pruning | After pruning |
| --- | --- | --- |
| large early branches | remain | usually remain |
| leaves explaining only a few rare cases | may still be present | may be cut away |
| train score | may look higher | may drop a little |
| test stability | may fluctuate | may become more stable |

The key in this table is that pruning should not be read as `damaging the tree`. It should be read as `keeping the large structure while removing leftover tiny questions`.

Suppose a late branch creates one more leaf using a very narrow condition such as: `temperature is high`, `vibration is large`, and `only the third time-point pressure was in a narrow range`. If that leaf only explains two products in the training data, pruning asks whether that branch is worth keeping.

That is why `ccp_alpha` is not just one more number. It is a handle that asks: `Is the gain in train score from this small branch really larger than the cost of added complexity?`

As a direction-only memory aid:

- when `ccp_alpha` is very small, more branches tend to remain
- as `ccp_alpha` grows, small branches are more easily removed
- if it is too small, the model may tilt toward memorization
- if it is too large, meaningful patterns may be removed too

### Read Pruning As A Flow

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-02-en.mmd"
```

This Section does not calculate pruning formulas. Instead, it centers on `which leftover branches should not be kept` and `why someone may give up a little train score to gain more stable test behavior`.

## Cases And Examples

### Case 1. When A Defect-Detection Tree Starts Memorizing Factory Exceptions

A manufacturing team is building a decision tree that separates defective products from normal ones using sensor values. The criteria people looked at first were questions such as `is the temperature above a threshold?`, `is vibration beyond a range?`, and `is the pressure change abrupt?`

When more and more questions are added, the model can begin to look smarter. In fact, a deeper tree may become almost error-free on the training data. But when the later branches are inspected, leaves that explain only one or two exceptional products start to appear. Those leaves can easily shake when the production process changes even a little.

Reduced to a small scene, the situation looks like this.

| Product | Temperature | Vibration | Pressure change | Human first judgment |
| --- | --- | --- | --- | --- |
| A | high | large | abrupt | high defect-review priority |
| B | normal | small | stable | likely normal |
| C | high | medium | slightly large | review candidate |
| D | slightly high | briefly large | stable | hard to call defective immediately |

The human-first pattern here is a relatively large one such as `temperature rise + vibration/pressure anomaly`. An overly deep tree may keep adding tiny questions such as `did the vibration rise only briefly at the third measurement?` or `did the pressure curve bend twice inside a narrow range?` Then it starts explaining only a few products that happened to resemble D in the training data.

| Human-first criterion | What an overly deep tree easily grabs |
| --- | --- |
| do we see both temperature and vibration abnormality? | a brief fluctuation at one time point |
| does the pressure change look like a process anomaly? | a rare sensor combination in the training data |
| should this be a review-first case? | a very fine branch that fits only one or two products |

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-03-en.mmd"
```

If the same scene is divided into `a comparatively simple reading` and `an overly deep reading`, the difference becomes clearer.

| Reading style | How it reads product D |
| --- | --- |
| comparatively simple tree | temperature is a little high, but pressure is stable, so it stays as a review candidate |
| overly deep tree | it gets separated into its own leaf using a brief vibration fluctuation and a rare sensor combination |

In this scene, overfitting should be read as `the model increases question detail so much that it memorizes the training data`. `max_depth` limits how far the tree may grow. `min_samples_leaf` prevents one leaf from becoming a tiny exception set. `ccp_alpha` reduces already grown branches again. In short, more questions do not always mean a better explanation.

The observable result appears when train accuracy and test accuracy are read together. If the train score keeps rising while the test score stops improving or begins to fall, later branches should be read as memorization rather than generalization. The important question is not only `did the model describe sensor anomalies more finely?` It is `did it produce a criterion that still repeats on new factory data?`

### Case 2. When A Churn Tree Starts Memorizing Exceptional Customers More Than Review Rules

Now imagine a subscription-service team building a decision tree for churn prediction. The human-first criteria were broad patterns such as `did visits drop sharply?`, `was there a payment failure?`, and `was there a complaint signal after support contact?`

But if the tree keeps growing deeper, later branches may start stacking combinations such as: `were there 2 visits during the last 17 days?`, `was last month's payment inside a narrow range?`, `was the promotion mail opened once?` These combinations may fit a small set of customers in the training data very well, but may not repeat in real operation or may have weak meaning.

Reduced to a small scene, it looks like this.

| Customer | Recent visit change | Payment failure | Complaint signal | Human first judgment |
| --- | --- | --- | --- | --- |
| A | strongly decreased | yes | yes | high review priority |
| B | slightly decreased | no | no | hard to call churn immediately |
| C | strongly decreased | no | yes | review candidate |
| D | almost unchanged | no | no | likely stay |

The human-first pattern is still a large one such as `visit decline + payment/complaint signal`. An overly deep tree may instead add tiny questions such as `were there zero visits only in the second week?` or `was the event mail opened on Wednesday morning?` Then the model starts building branches that explain only a few customers similar to C in the training data.

| Human-first criterion | What an overly deep tree easily grabs |
| --- | --- |
| is the visit decline clear? | a small fluctuation in one specific week |
| were payment trouble and complaint signal present together? | a rare customer combination in the training data |
| should this be raised as a review case first? | a very fine branch that fits only one leaf well |

If the same scene is divided into `a shallow reading` and `an overly deep reading`, the difference becomes clearer.

| Reading style | How it reads customer C |
| --- | --- |
| comparatively simple tree | visit decline plus complaint signal makes C a review candidate |
| overly deep tree | it gets separated into its own leaf using a specific week pattern, amount range, and mail-response detail |

In this scene, overfitting should be read as a state where `questions that look highly descriptive actually make the review criterion less clear and instead memorize accidental combinations from the training data`. So when reading a tree, the reader should ask not only `did the explanation become more detailed?` The reader should also ask `is that detail likely to repeat on new customers?` and `does it improve review priority in practice?`

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-04-en.mmd"
```

The same scene becomes easier to diagnose when reread through leaves rather than only through a score table.

| What to inspect in a leaf | Scene that reads like an overfitting signal |
| --- | --- |
| sample count inside the leaf | many leaves are left with only one or two cases |
| nature of the questions that created the leaf | instead of large patterns, tiny week-level or point-level questions increase |
| practical meaning of the leaf | it looks more like a note about training cases than a stable review rule |

Holding onto this table makes it harder to praise the tree just because `train accuracy went up`. For beginners especially, it helps to ask once in a sentence: `Does this leaf describe new customers, or is it only memorizing a tiny set of training customers?`

### Which Handles Should Be Checked In Practice?

At the beginning, it is better to separate the controls by role instead of touching everything at once.

| Handle | Question to read first |
| --- | --- |
| `max_depth` | how deep should the tree be allowed to grow? |
| `min_samples_split` | are there enough samples in this node to split it again? |
| `min_samples_leaf` | should one leaf be prevented from becoming too small? |
| `ccp_alpha` | how much should already grown branches be reduced? |

In practical language, that becomes the following.

- the explanation feels too long and complex -> check `max_depth`
- there seem to be too many leaves explaining only a few cases -> check `min_samples_leaf`
- there are too many branches and too many leftover twigs -> consider `ccp_alpha`

## Practice And Examples

### Python Example: See Overfitting By Changing Depth

This exercise uses the same decision-tree classifier while changing only depth, and watches how train/test results separate.

- problem situation: classify iris species
- input: sepal and petal lengths and widths
- label: three species
- concepts to check:
  - as depth grows, train performance can rise easily
  - test performance may plateau or fall after a point
  - tree depth is one of the main complexity handles

It helps to define what to compare first.

| Value to compare | Why read it together |
| --- | --- |
| `max_depth` | to see how far the tree is allowed to grow |
| `leaves` | to see how many end nodes that depth actually created |
| train accuracy | to see fit on the training data |
| test accuracy | to see generalization on new data |
| `train - test` gap | to see how far memorization and generalization separate |

Values to change:

- `max_depth`: try 1, 2, 3, 5, `None`, or add 4 between 3 and 5.
- `random_state`: see how much the gap moves when the split and tree choices change.
- `test_size`: see how sensitive the interpretation becomes when the test share changes.

```python
# This example changes max_depth to read tree depth and the train-test gap as overfitting signals.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for depth in [1, 2, 3, 5, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"max_depth={depth}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

An example output is as follows.

```text
max_depth=1
  depth          : 1
  leaves         : 2
  train accuracy : 0.667
  test accuracy  : 0.667
  train-test gap : 0.0

max_depth=2
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
  train-test gap : 0.063

max_depth=3
  depth          : 3
  leaves         : 5
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

max_depth=5
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

max_depth=None
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089
```

What should be read from this result is the following.

1. As depth grows, train accuracy easily keeps improving.
2. Test accuracy may stop improving after a point.
3. As the `train-test gap` grows, the memorization signal may be getting stronger.
4. In this example, around `max_depth=3` looks more balanced.

So when tree performance is read, the real question is not only `did the tree get deeper?` It is `how did train and test separate once it became deeper?`

Also, it matters not to watch only the accuracy number. The difference between `max_depth=5` and `max_depth=3` is not only a score difference. It is also a structural difference: the deeper tree created more leaves and started to describe the training data in finer detail.

### Change One More Value And Read `depth` Together With `leaf`

This time, check how the judgment changes when leaf size is read together with depth.

- value to change: `min_samples_leaf`
- reason: to see whether blocking tiny leaves reduces exception memorization even under the same depth limit
- concepts to check:
  - `max_depth` and `min_samples_leaf` control the same complexity problem at different points
  - even when depth looks similar, larger leaves can change the train/test interpretation
  - overfitting diagnosis is safer when read as `depth + leaf size + gap`, not only one depth value

Values to change:

- `min_samples_leaf`: compare small and large leaves with values such as 1, 2, 5, and 10.
- `max_depth`: alternate between 3 and 5 to see how depth limits and leaf limits work together.
- output fields: record which of `get_depth()`, `get_n_leaves()`, and `train-test gap` changes first.

```python
# This example changes min_samples_leaf under the same depth limit to read leaf size and the gap together.
for leaf_size in [1, 2, 5]:
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=leaf_size,
        random_state=42,
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"min_samples_leaf={leaf_size}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

An example output is as follows.

```text
min_samples_leaf=1
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

min_samples_leaf=2
  depth          : 4
  leaves         : 7
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

min_samples_leaf=5
  depth          : 3
  leaves         : 4
  train accuracy : 0.971
  test accuracy  : 0.933
  train-test gap : 0.038
```

The first thing to notice in this comparison is: `even when train accuracy drops a little, test accuracy can become more stable.` So overfitting relief should not be read as a defeat where score is sacrificed. It should be read as an adjustment that `memorizes less and holds up better`.

It is useful to write the following three sentences directly.

1. In what sense is `max_depth=5, min_samples_leaf=1` the most sensitive structure?
2. What became less sensitive under `min_samples_leaf=2` or `5`?
3. If pruning is added next, which leftover branches look likely to be removed first?

### Change `ccp_alpha` And Read The Direction Of Pruning

Now shake the tree once more by changing how much of an already grown tree should be cut back.

- value to change: `ccp_alpha`
- reason: depth and leaf-size tuning prevented growth from the start, but pruning simplifies after the tree has already grown
- concepts to check:
  - as `ccp_alpha` grows, small branches are more easily removed
  - train score may fall a little while the test side becomes more stable
  - pruning is closer to `reselecting the main structure that should remain` than to `damaging the tree`

Values to change:

- `ccp_alpha`: add 0.01 between 0.005 and 0.02 to see where the change becomes large.
- `max_depth`: compare pruning with and without an explicit depth limit.
- `min_samples_leaf`: see which combinations become too simple when pruning and leaf-size limits are used together.

```python
# This example changes ccp_alpha to see how pruning changes depth, leaf count, and the train/test gap.
for alpha in [0.0, 0.005, 0.02]:
    model = DecisionTreeClassifier(
        random_state=42,
        ccp_alpha=alpha,
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"ccp_alpha={alpha}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

An example output is as follows.

```text
ccp_alpha=0.0
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

ccp_alpha=0.005
  depth          : 4
  leaves         : 6
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

ccp_alpha=0.02
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
  train-test gap : 0.063
```

The first thing to read from this result is: `cutting a little helped, but cutting too much made the model simple again in the wrong way.` So pruning is not `the more, the better`. It is a search for balance: remove leftover twigs, but keep the larger pattern.

If possible, write the following sentences too.

1. What kind of small branch does `ccp_alpha=0.005` seem to have removed?
2. Why does `ccp_alpha=0.02` look like a candidate that became too simple?
3. Among `max_depth`, `min_samples_leaf`, and `ccp_alpha`, which handle would you adjust first on your current data?

### Practice: Leave Complexity Controls In Record Language

If the experiments above were run, stop not at seeing the result, but at leaving a short comparison record.

| Comparison item | Depth-only experiment | Experiment with leaf size too |
| --- | --- | --- |
| setting that looks most balanced |  |  |
| setting that looks most sensitive |  |  |
| setting with the largest train-test gap |  |  |
| next handle to adjust |  |  |

When filling the table, do not write only `the setting with the highest score`. It is better to write one sentence explaining why that setting looked balanced.

If possible, add one more line for the pruning experiment too.

| Pruning comparison item | Record |
| --- | --- |
| `ccp_alpha` that looks most balanced |  |
| `ccp_alpha` that feels over-pruned |  |
| handle to compare next |  |

For example, a note might read like this.

- `max_depth=3` is a good baseline because train and test improve together.
- `max_depth=5, min_samples_leaf=1` has perfect train fit but a larger gap, so it looks like a candidate that memorizes more exceptions.
- Next, I want to see whether the same failures remain after pruning leftover branches with `ccp_alpha`.

## Checklist

- Are you reading a rise in train performance as if it automatically meant a rise in test performance?
- Have the leaves become so small that they are speaking like rules about exceptional cases?
- Are you distinguishing clearly between the next adjustment being a depth limit, a leaf-size change, or pruning?
- Can you explain that a tree is easy to read, but without limits it can follow the training data too much, and that overfitting risk grows as depth increases and leaves become smaller?
- Can you explain that higher train performance does not guarantee that test performance improves together?
- Can you explain how `max_depth`, `min_samples_leaf`, and `ccp_alpha` each control tree complexity?

## Sources And References

- scikit-learn developers, `1.10. Decision Trees`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/tree.html](https://scikit-learn.org/stable/modules/tree.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `DecisionTreeClassifier`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984, accessed 2026-07-26. [https://doi.org/10.1201/9781315139470](https://doi.org/10.1201/9781315139470){: target="_blank" rel="noopener noreferrer" }
