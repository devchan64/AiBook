# P4-5.1 Overfitting And Underfitting

> Section ID: `P4-5.1`
> Version: `v2026.07.24`

In Chapter P4-4, we looked at why data are divided into training, validation, and test sets. The next question follows naturally. After splitting the data and checking the results, why do some models work well on training data but weaken on new data? And why do some models fail to explain even the training data well enough?

This Section separates those two states. `Overfitting` means a state that is too tightly matched to the training data, while `underfitting` means a state that still has not learned the important patterns well enough. In machine learning, you need to distinguish these two states before you can make the next choice.

This Section explains the basic distinction between `overfitting` and `underfitting`. The next Section continues the current context through this handle, and the basic distinction of whether a model holds up on new data is connected again through this Section and the [concept glossary](/AiBook/reference/concept-glossary/).

## Scope Of This Section

This Section explains the basic distinction between overfitting and underfitting. It does not yet cover specific mitigation methods such as regularization, dropout, or early stopping. Those responses return in the deep learning parts of Part 4 and later model-specific chapters.

This Section also does not finish the wider question, `why does a model work well on new data?` That question continues in P4-5.2 on `generalization`. The focus here is to visually distinguish `a state that fit too much` from `a state that did not learn enough`.

- What kind of state is overfitting, and what kind of state is underfitting?
- Why is it hard to trust a model by training score alone?
- Why should training score and validation score be read together?
- What happens when a model is too simple or too complex?
- In practice, through what scenes do people feel this problem?

## Goals Of This Section

- You can explain the difference between overfitting and underfitting.
- You can explain why training score and validation score should be read together.
- You can explain why a state that fits only the training data too strongly is risky.
- You can explain why a simple model can miss important patterns.
- You can move naturally into the later discussion of generalization in P4-5.2.

## Learning Background

### Catching The Two States At Once First

The table below is the fastest starting point for looking at both states together.

| State | What it looks like on training data | What it looks like on new data | Interpretation |
| --- | --- | --- | --- |
| underfitting | It does not fit well | It still does not fit well | The model is still too simple or has not learned enough |
| appropriate state | It fits fairly well | It works similarly on new data | It has captured important patterns to some degree |
| overfitting | It fits too well | Performance drops on new data | It followed even accidental fluctuations in the training data too closely |

In this Section, the first thing to read is not yet a number like `is accuracy 0.83 good?` but the `difference across the two data scenes`.

The terms can be fixed very briefly here.

- `fit` means how much a model explains and follows the pattern in the data.
- `underfitting` means a state biased toward too little explanation.
- `overfitting` means a state biased toward explanation that is too detailed.

So both are problems of `fit`, but the direction is different.

- underfitting: it still does not explain enough
- overfitting: it tries to explain too much and follows unnecessary fluctuations too

You can remember this as the difference between `a state that learned too little` and `a state that memorized too much`.

## Main Learning Content

### Underfitting Is A State That Has Not Learned Enough Yet

Underfitting is a state where the model still has not captured the important structure of the problem well enough. It appears often when the model uses rules that are too simple, when training has not progressed enough, or when the model sees only a small part of the features it needs.

Put a bit more carefully, underfitting means `the range of explanation the model can express is too narrow`, or `the model has not yet used that range well enough`. Because of that, it repeatedly misses parts even inside the training data.

In this state, the following traits are often seen together.

| Observed scene | Interpretation toward underfitting |
| --- | --- |
| training score is low | It cannot explain even the data it has already seen well enough |
| validation score is also low | So it is naturally weak on new data as well |
| the gap between training and validation is small | A small gap is not automatically good; both may simply be low and weak together |

Because of this, a reader may misunderstand the result as `the gap is small, so it is fine`. But if both are low, the model may not be stable. It may simply be `still too weak`.

For example, imagine customer-churn prediction where the model looks only at `recent purchase count`. In reality, inquiry count, recent logins, and payment failures also matter. If you judge by only one variable, the model starts from an overly simple point.

| Customer ID | Recent purchase count | Inquiry count | Actual churn | Example of an overly simple rule |
| --- | --- | --- | --- | --- |
| C01 | 8 | 0 | stay | stay |
| C02 | 2 | 3 | churn | churn |
| C03 | 6 | 4 | churn | stay |
| C04 | 5 | 5 | churn | stay |

In this table, if you read only the purchase count, it is easy to miss C03 and C04. This is not mainly a problem caused by too much complexity. It is closer to a problem caused by not explaining the needed pattern well enough yet.

The same problem appears if you change the scene.

| Work | Example of an overly simple judgment | What is easy to miss |
| --- | --- | --- |
| spam classification | Treat every title with `free` as spam | It cannot separate normal promotional mail from subtle spam well |
| customer recommendation | Recommend using only one recently purchased item | It cannot reflect changes in older preferences or multiple interests |
| price prediction | Predict house price from number of rooms only | It misses major factors such as location, age, transport, and repair condition |

All three cases share the same point. They are states where `the explanation is too small to capture important differences`.

So underfitting can usually be summarized by the following question.

`Does this model still lack even the level of explanatory power needed to solve the problem?`

If you turn this into a defect-detection case, even the same image-classification problem must be read through a different flow when the model is `too simple and misses things` versus when it `memorizes the training examples too strongly`.

```mermaid
--8<-- "assets/part-04/chapter-05/p4-5-1-mermaid-01-en.mmd"
```

### Overfitting Is A State That Memorized Too Much

Overfitting is a state where the model sticks too tightly to the training data. It has not only captured the important patterns, but also followed accidental fluctuations and odd arrangements that happened to be present in that particular data.

The important phrase here is `accidental fluctuations`. Every dataset contains meaningful structure, or signal, but also accidental variation, or noise, mixed into it. Overfitting can be read as a state where the model does not separate those two well enough and ends up treating the noise as if it were a rule worth learning.

Read a little more carefully, overfitting can be restated as the following question.

`Has this model followed not just the general pattern, but also shapes that happened to exist only in this training data?`

In this state, the following traits are often seen together.

| Observed scene | Interpretation toward overfitting |
| --- | --- |
| training score is very high | It matches the data it has already seen too well |
| validation score is lower than expected | It does not hold up that well on new data |
| the gap between training and validation is large | The model may have gained an explanation that is strong only on the training data |

If you rewrite this as work scenes, it looks like this.

- It fits the training data almost perfectly.
- On validation data, the score drops more than expected.
- But the team may still misunderstand the result as `it went well` because it looked only at the training score.

For example, imagine a spam-classification model that gets 99% on training emails but only 81% on new emails. Then the model may not have learned the general pattern of spam well enough. It may simply have become familiar with the training data.

The same scene appears in recommendation systems.

- In the training data, it explains some users' past clicks almost perfectly.
- But for newly arriving users or users whose preferences recently changed, the recommendation weakens.

In that case, the model may be less about learning the `principle of recommendation` and more about `remembering the old records too strongly`.

The following comparison helps read the overfitting state more clearly.

| Question | Answer when it is overfitting |
| --- | --- |
| Is it strong on data it has already seen? | Yes |
| Does it show the same strength on unseen data? | Not necessarily |
| Is the problem a lack of data, or is the degree of memorization too large? | Often the latter may be the problem |

So overfitting is often closer to `the model became too familiar with this particular exam paper` than to `the model became more intelligent`.

### Scores Should Always Be Read Through Two Scenes

Overfitting and underfitting are usually read by looking at `training score` and `validation score` together.

| Candidate | training accuracy | validation accuracy | How to read it |
| --- | --- | --- | --- |
| Model A | 0.62 | 0.60 | Both are low. There may be underfitting |
| Model B | 0.84 | 0.82 | They are similar, and both are fairly good |
| Model C | 0.99 | 0.78 | Only training is too high. There may be overfitting |

The key here is not just `validation score is a little lower than training score`, but `why did that gap appear in that way?`

- both are low -> the model may still be failing to capture important structure
- both are high and the gap is small -> it may be relatively stable
- only training is very high while validation drops a lot -> it may have fit the training data too tightly

Readers often confuse the first and the third patterns.

| Common misunderstanding | What it actually means |
| --- | --- |
| If validation score is low, it must be overfitting | If training score is also low, it may be underfitting |
| If training score is high, it is a good model | Validation score must be read together with it |
| Even a small gap is always a problem | A small gap is natural. The issue is the `pattern` and the `size` |

In one line, it can be summarized like this.

- underfitting is a state where the model is still insufficient
- overfitting is a state where the model matched too aggressively

In practice, the first judgment is often `which side should I suspect first right now, underfitting or overfitting?`

| Current observation | State to suspect first | Why |
| --- | --- | --- |
| both training score and validation score are low | underfitting | Because it is more likely that the model still has not captured important structure well enough |
| training score is very high but validation score drops sharply | overfitting | Because it is more likely that the model followed accidental fluctuations in the training data too |
| both training and validation are high and the gap is small | a relatively appropriate state | Because the model is more likely to hold up to some degree on new data |

## Detailed Learning Content

### It Becomes Faster To Read Through A Diagram

```mermaid
--8<-- "assets/part-04/chapter-05/p4-5-1-mermaid-02-en.mmd"
```

This diagram is not an exact mathematical explanation. It is a directional explanation. The left side means a state that is still insufficient, the middle means a relatively balanced state, and the right side means a state that has fit too aggressively.

If you rewrite that diagram into sentences, it becomes the following.

- left: it still misses important structure
- middle: it mainly captures important structure
- right: it tries to capture not only the important structure but also accidental fluctuations

### Looking Again With A Small Table

The table below shows the three states more intuitively.

| Model state | training score | validation score | How it feels when read |
| --- | --- | --- | --- |
| too simple | low | low | it has still learned too little |
| appropriate | high | similarly high | it may hold up on new data |
| too complex | very high | relatively low | it fit the training data too aggressively |

This table is not a precise mathematical formula. It is a starting point for reading the state in practice.

That is why overfitting and underfitting are not just exam terms. They are the first diagnostic language for reading a model.

### Why A More Complex Model Is Not Always Better

When a model becomes more complex, it can express more patterns. That part is an advantage. But in situations with limited data, unstable features, or many accidental fluctuations, that complexity can instead make the model follow even the noise in the training data.

The official scikit-learn example shows this point as well. It explains that a simple function can become underfitting because it cannot explain the training samples well enough, while a polynomial of excessively high degree can learn even the noise in the training data and become overfitting. In this Section, the whole mathematical shape matters less than the perspective that `model complexity and new-data performance do not always improve together`.

So it is important to build the following reading habit.

1. Is the score I am looking at a training score, or a validation score?
2. Is the gap between them small or large?
3. Are both low, or is only training unusually high?
4. Is the current problem `the model must learn more`, or `the model must memorize less`?

The fourth question is especially important.

- must learn more -> suspect underfitting
- must memorize less -> suspect overfitting

These two questions keep working in later chapters as well.

- when looking at linear regression
- when looking at decision trees
- when looking at neural networks

The first question to ask is similar. `Is this model still under-learned, or has it memorized too much?`

## Cases And Examples

### Case 1. When A Defect-Detection Model Looks Perfect In An Internal Demo

A manufacturing team wants to classify defective parts from photos. The criteria people first used were visible signals such as `is there a crack on the surface`, `is the color uneven`, and `is the edge chipped`.

In the first experiment, the team uses a very complex model and gets an almost perfect score on the training data. So in an internal demo, the team may feel that the model is already good enough. But when the data are switched to the validation set, the score drops sharply, and the model misjudges more often when the lighting condition changes even a little.

This scene shows why overfitting and underfitting must be distinguished together. If both training score and validation score are low, it may still be the underfitting side where the model has not yet learned the important pattern well enough. By contrast, if only the training score is excessively high while the validation score drops sharply, the model should be read as overfitting, where it followed the accidental background and noise in the training photos more than the essential features of defects.

The checkable result appears when training score and validation score are placed side by side. Looking at both the level of the two scores and the gap between them lets you judge whether the next action should be `give the model more explanatory power` or `make it memorize less`.

```mermaid
--8<-- "assets/part-04/chapter-05/p4-5-1-mermaid-03-en.mmd"
```

### Example 1. Reading It Again Through A Practical Scene

If you use a customer-churn prediction project as an example, the team usually sees one of the following two scenes.

| Scene | What appears on the surface | What should actually be suspected |
| --- | --- | --- |
| the model is very good only on training data | it looks excellent in internal review | possibility of overfitting |
| the model is not very good even on training data | scores are poor everywhere | possibility of underfitting |

The key is not to read the result as `if the score is low, it is simply a bad model`. The first question is why it is low, and on which data it is low.

If you rewrite this like an actual meeting scene, it becomes the following.

| What the team says | A more accurate interpretation |
| --- | --- |
| `If the training score is 99%, isn't it almost finished?` | The gap from the validation score should be examined first |
| `If the validation score is 60%, does that mean the model is useless?` | If training score is also low, it may still be underfitting |
| `Wouldn't everything be solved if we made the model more complex?` | Complexity increases expressive power, but it can also increase the risk of overfitting |

So what matters in practice is not simply `complex model versus simple model`. More precisely, the job is to judge `is the explanation insufficient for the current data and problem, or is it excessive?`

## Practice And Examples

### Reading Underfitting And Overfitting Through A Table

The following record is not an example that actually trains a model. It is a scene for reading combinations of training score and validation score that have already been produced. So rather than printing the scores again with Python, it is more direct to compare the score levels and gaps in one table.

| Model | Training score | Validation score | Gap `gap` | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `simple_rule` | 0.62 | 0.60 | 0.02 | The gap is small, but both are low, so this is closer to underfitting |
| `balanced_model` | 0.84 | 0.82 | 0.02 | Both are high and the gap is small, so it is relatively stable |
| `very_complex_model` | 0.99 | 0.78 | 0.21 | Only the training score is high and validation drops, so overfitting should be suspected |

What you should read from this table is not only the `gap`.

- `simple_rule` has a small gap, but both scores are low. This is closer to an underfitting interpretation.
- `balanced_model` has both scores high and the gap small. It can be read as a relatively stable state.
- `very_complex_model` has a very high training score, but a large gap from validation. This is a scene where overfitting should be suspected.

So a small gap is not always good, and a high training score is not always good either. In this table, you should read the levels of the two scores first, and then look at the gap between them.

The same judgment can also be checked by running a small actual model. The example below creates two moon-shaped classes and changes only `max_depth` in the same `DecisionTreeClassifier`, then compares training score and validation score. The value to manipulate is `max_depth`.

```python
from sklearn.datasets import make_moons
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_moons(n_samples=160, noise=0.28, random_state=7)
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.35, random_state=3, stratify=y
)

for depth in [1, 3, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=0)
    model.fit(X_train, y_train)
    train_score = accuracy_score(y_train, model.predict(X_train))
    valid_score = accuracy_score(y_valid, model.predict(X_valid))
    label = "no_limit" if depth is None else f"depth_{depth}"
    print(
        label,
        "train=", round(train_score, 3),
        "valid=", round(valid_score, 3),
        "gap=", round(train_score - valid_score, 3),
    )
```

An example output is as follows.

```text
depth_1 train= 0.846 valid= 0.839 gap= 0.007
depth_3 train= 0.933 valid= 0.911 gap= 0.022
no_limit train= 1.0 valid= 0.893 gap= 0.107
```

`depth_1` is too simple, so the scores are lower, and `depth_3` improves training and validation together. By contrast, `no_limit` fits the training data perfectly, but the validation score drops and the gap grows. So even in code, underfitting and overfitting must be read through `training score, validation score, and the gap between the two`, not through one training score.

The same point can be restated more precisely like this.

- `low + low` may mean a state that misses because it is still insufficient
- `high + similarly high` may mean a relatively stable state
- `very high + noticeably lower` may mean a state that fit the training data too aggressively

If you rewrite the same example as one-line judgments, it becomes the following.

```text
simple_rule -> still too simple
balanced_model -> the most stable among the current candidates
very_complex_model -> may have fit the training data too strongly
```

### Adding A Work Question Through A Table

This time, attach a work question to the same numbers.

| Candidate | Training score | Validation score | Gap `gap` | Selection judgment |
| --- | ---: | ---: | ---: | --- |
| `candidate_A` | 0.65 | 0.61 | 0.04 | Both are low, so it is weak as a baseline candidate |
| `candidate_B` | 0.88 | 0.85 | 0.03 | Most stable by the validation criterion |
| `candidate_C` | 0.98 | 0.76 | 0.22 | Training score is highest, but overfitting should be suspected |

If you choose by the validation criterion, the choice is `candidate_B`.

In this example, `candidate_C` looks best if you look only at training score. But the actual choice becomes `candidate_B` when you use validation score as the criterion. This is the most basic reading habit for guarding against overfitting.

There is one core sentence readers should remember here.

`Model selection is not about choosing the candidate with the highest training score. It is about choosing the candidate that is more stable under the validation criterion.`

And at the center of that stability judgment is ultimately this question.

`Did this model capture the pattern worth learning, or did it follow the shape of this particular dataset too much?`

## Checklist

- Can you explain why `both low` and `only training very high` should be read differently when training score and validation score are examined together?
- Can you explain in what scenes the problem should be divided into `must learn more` and `must memorize less`?
- Can you explain that a more complex model is not always better, because it can also increase the risk of overfitting?
- Can you explain that underfitting is a state where the model still has not learned the important pattern enough, while overfitting is a state where it sticks too tightly to the training data?
- Can you explain that training score alone is not enough to judge a model, and that reading it with validation score helps you find weaknesses on new data more quickly?
- Can you explain that even if training score is very high, a low validation score should make you suspect overfitting first, while both low should make you suspect underfitting first?

## Sources And References

- scikit-learn developers, `Underfitting vs. Overfitting`, scikit-learn Examples, accessed 2026-07-19. [https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html){: target="_blank" rel="noopener noreferrer" }
- Google for Developers, `Machine Learning Glossary`, accessed 2026-07-19. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, Jonathan Taylor, `An Introduction to Statistical Learning`, Springer, official website accessed 2026-07-19. [https://www.statlearning.com/](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }
