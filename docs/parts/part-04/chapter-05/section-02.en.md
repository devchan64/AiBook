# P4-5.2 Generalization

> Section ID: `P4-5.2`
> Version: `v2026.07.11`

P4-5.1 separated `overfitting` from `underfitting`. Now we need to move one step higher. Why do we care so much about that distinction? In the end, the goal of machine learning is not `raising the score on training data`, but `working usefully even on data the model has not seen yet`. The word that organizes that question is `generalization`.

Generalization may sound difficult, but the starting point is simple. It asks whether a model stops at matching examples it has already seen, or whether it also responds properly to new examples with similar structure.

## Scope Of This Section

This Section explains the meaning of generalization. It does not yet cover the formula of generalization error or theoretical bounds. The focus here is to connect `why new data matter`, `why validation and test are needed`, and `why training score alone is not enough`.

The detailed calculation of metrics is handled in P4-6, and the practical use of cross-validation returns in P4-8.1 and P4-9.2. This Section fixes generalization first not as a mathematical theory, but as a goal sentence that runs through machine learning as a whole.

- What is generalization?
- Why is the goal of machine learning described as generalization rather than training score?
- What is the relationship between overfitting and generalization?
- What exactly does unseen data mean?
- How is generalization felt in practice?

## Goals Of This Section

- You can explain generalization in one sentence.
- You can explain that training score and generalization are not the same thing.
- You can explain why overfitting can weaken generalization.
- You can understand that validation data and test data are ultimately tools for checking generalization.
- You can connect this Section to why later chapters on metrics and model choice are needed.

## Learning Background

### What Does Generalization Ask?

Google's machine-learning glossary effectively explains generalization as the question `can the model make good predictions on examples that are not in the training set?` The meaning to hold onto is the following.

`Generalization is the property that lets a model make usable judgments even on data it has not seen yet.`

The important part here is `even though the data are not the same as before`.

We also need to ask why such a word is used separately. Because machine learning learns rules from data, it is easy to leave only the sentence `the score is high` on the surface. But `high only on the data it has seen` and `maintained even on the data it has not seen` are entirely different questions. We use the word `generalization` to separate those two.

| Question | Meaning from the perspective of generalization |
| --- | --- |
| Does it fit the training data well? | That is only a starting point |
| Does it also fit new data similarly? | That is the core question of generalization |
| Is it just memorizing specific samples? | That can be a warning signal that harms generalization |

So generalization asks less whether the model `adapted to this dataset` and more whether it `learned the structure of the problem to some degree`.

This can be restated more simply like this.

- Did it memorize the shape of the dataset?
- Did it learn the structure of the problem?

Generalization is closer to the second side.

### The Historical Background That Made Generalization Important

Generalization did not appear suddenly only in recent generative AI discussions. It is a question that has long been treated in the history of statistical learning theory. A survey paper by Ulrike von Luxburg and Bernhard Schoelkopf explains that statistical learning theory began in Russia in the 1960s and became widely known with the rise of support vector machines in the 1990s. The same paper describes the central question of the field as `how can valid conclusions be drawn from empirical data?`

This history can be read through the following flow.

1. Statistics and learning research long tried to separate rules that fit only the observed data from rules that also work on new data.
2. That question was handled more systematically inside statistical learning theory.
3. Later, in machine-learning practice, procedures such as validation, test, and cross-validation became standard habits for checking generalization.

So generalization is not a trend word. It is a long-standing criterion that separates `was this really learning?`

## Main Learning Content

### Why Generalization Becomes The Goal

Machine learning is almost always used for `data that will arrive next`.

- A spam classifier must classify the emails that arrive tomorrow.
- A customer-churn model must predict next month's customers.
- A price-prediction model must estimate houses that have not been traded yet.

So the real usage scene is always on the side of `data not seen yet`.

| Where the model is used | What the training data are | What arrives at actual use time |
| --- | --- | --- |
| spam filter | past email records | newly arriving email |
| recommendation system | past click and purchase records | the next action of a user who logs in now |
| demand forecasting | past sales data | demand for next week that has not arrived yet |

This table shows immediately why training score alone is not enough. A real service is not about `reviewing the past`, but about `responding to the future`.

That is why generalization is not just a bonus property. It is tied to the reason machine learning is used at all. If there were no need to deal with new data, then a rule table or lookup table would often be enough without a machine-learning model.

### What Counts As New Data

The phrase `unseen data` may sound like data from a completely unfamiliar world. But usually it means `examples from the same problem that were not used in training`.

This point is often misunderstood. Generalization usually does not mean `it works unconditionally in any environment`. It is first closer to `within the same problem setting, it still holds up to some degree on examples it has not seen yet`.

For example, in customer-churn prediction, it can be organized like this.

| Category | Example |
| --- | --- |
| training data | some customer records from the past three months |
| validation data | some held-out records from the same period that were not used for training |
| test data | some records kept aside for the final check |
| real service input | new customer records accumulated next month |

All four belong to the same domain, but from the model's perspective, there is a boundary between `what it has seen` and `what it has not seen yet`. Generalization is a story that happens exactly at that boundary.

To make that boundary clearer, it can be divided like this.

| Case | Usually included in the explanation of generalization? | Why |
| --- | --- | --- |
| next week's customer data from the same service | yes | it is a future example of the same problem |
| different samples from the same classification task | yes | they are unseen examples of the same structure |
| data from a completely different industry | usually not directly | the problem definition itself may be different |
| data whose input format and meaning differ greatly | usually needs separate review | it is hard to treat it as the same generalization problem |

So generalization is not a declaration that `it works on any data`. It is closer to `how much does it hold up on unseen examples of the same problem?`

The range of generalization becomes easier to organize when you first ask `how far can this still be treated as a new example of the same problem?`

| Current comparison scene | Included directly in a generalization discussion? | Why |
| --- | --- | --- |
| next week's data from the same service | usually yes | because it is a new sample of the same problem |
| other unseen cases of the same problem | usually yes | because they are unused examples of the same structure |
| data from the same problem but under slightly changed conditions | conditionally yes | because it may still be the same problem, though a harder case of generalization |
| data from a completely different industry or with different meaning | usually not directly | because the problem definition itself may be different |

The range can be visualized like this.

```mermaid
--8<-- "assets/part-04/chapter-05/p4-5-2-mermaid-01-en.mmd"
```

This diagram divides the range that generalization points to. The most direct test of generalization happens on new samples of the same problem, and as you move toward condition shifts or entirely different tasks, it becomes harder to group everything under the same generalization claim.

- `same task, same meaning` is the region closest to the training data
- `same task, new samples` is the region where generalization is tested first
- `same task, condition shift` may still be the same problem, but it is a harder region
- once you reach `different task or meaning`, it is usually hard to group it immediately as the same generalization issue

### The Relationship Between Overfitting And Generalization

Now it also becomes natural to connect why we need to bring back `overfitting` and `underfitting` from P4-5.1. Generalization ultimately asks `does the model hold up on new data?`

The overfitting discussed in P4-5.1 is a representative scene where generalization weakens.

| State | Read through the perspective of generalization |
| --- | --- |
| underfitting | it may be weak on new data too because it did not learn the important structure well enough |
| appropriate state | it may show relatively stable performance between training data and new data |
| overfitting | it may be strong on training data but drop on new data |

So overfitting can be read as `a direction that harms generalization`. But generalization is not a concept that ends simply as the opposite of overfitting. More broadly, generalization points to the whole question of `how much does the model hold up on new data?`

- overfitting can weaken generalization
- underfitting can also weaken generalization
- generalization ultimately asks about `the power to hold up on new data`

### Validation And Test Are Ultimately Tools For Seeing Generalization

The reason validation and test were separated in P4-4.2 was also generalization in the end.

- validation data: a tool for comparing which candidate is more likely to hold up on new data
- test data: a tool for checking one last time whether the final choice really holds up on new data

```mermaid
--8<-- "assets/part-04/chapter-05/p4-5-2-mermaid-02-en.mmd"
```

This diagram shows that train, validation, and test all exist in the end to estimate future unseen data in advance. Generalization should be read not as if validation or test score itself were the final goal, but as part of the full flow that asks how much the model will hold up on actual unseen data in real use.

In this diagram, validation and test are not the destination. Both are intermediate tools used to estimate `future unseen data`.

Therefore, validation and test are not simply procedures for assigning scores. Before that, they are procedures for observing generalization indirectly.

If the same procedure is rewritten into a table, it becomes the following.

| Stage | What is being done now | What is ultimately being checked |
| --- | --- | --- |
| training | learn patterns from seen data | is there at least a minimum starting point? |
| validation | compare candidate models or settings | which candidate is more likely to hold up on new data? |
| test | check once more separately at the end | is the chosen result overly optimistic? |
| real use | receive future inputs | does generalization actually hold up? |

## Detailed Learning Content

### Generalization Means Robustness, Not Perfection

Readers may misunderstand generalization as `it must be perfect on new data too`. But generalization is not perfect replication. Usually, it asks `does the model hold up above some usable level even on new data?`

| Misunderstanding | More accurate expression |
| --- | --- |
| Generalization means matching new data in exactly the same way | Generalization means maintaining usable performance even on new data |
| Training score and validation score must be exactly identical | A small difference is natural |
| If a model generalizes, it gets every case right | Even with generalization, it can still be wrong. What matters is overall robustness |

So generalization is closer to `stability` than to `perfection`.

Generalization is not the power to repeat memorized answers. It is the power to hold up even on similar problems seen for the first time.

## Cases And Examples

### Case 1. When A Recommendation Model Is Strong Only For Familiar Users

A content-service team is operating a recommendation model. The criteria people first used were signals such as `recently watched genre`, `frequently clicked category`, and `items watched a lot by similar users`.

On the training data, a model that follows those criteria well can achieve a high score. But when you move to a bundle of new users that is closer to actual service conditions, or to users whose recent preferences have changed, recommendation satisfaction drops noticeably. If the team had been looking only at training score, it could easily mistake the model for a sufficiently good one.

From the perspective of generalization, the question changes. What matters is not `did it explain the old records well?` but `does it hold up even for similar users it has not seen yet?` Validation data and test data should be read as tools for checking that point in advance.

The checkable result appears when you compare scores from a familiar user group and scores from a new user group. That lets you read how stably the model remains inside the same problem. If the gap is small, generalization is relatively preserved. If the gap is large, you need to check again whether the model adapted too strongly only to old patterns.

```mermaid
--8<-- "assets/part-04/chapter-05/p4-5-2-mermaid-03-en.mmd"
```

### Example 1. Reading Generalization Again Through Recommendation Systems And Price Prediction

Now that the relationships among definition, new data, overfitting, validation, and test have been organized, they can be read again through actual scenes. All of the examples below connect to the same question.

`Can this model hold up beyond the table currently in our hands?`

If you rewrite it as a recommendation-system example, it can be read like this.

| Scene | Interpretation from the perspective of generalization |
| --- | --- |
| recommendations fit existing user records very well | adaptation to the training data may have gone well |
| recommendations are weak for new users or recent preference shifts | generalization may be insufficient |
| validation experiments behave similarly across several user groups | the possibility of generalization is relatively higher |

Price prediction is similar.

| Scene | Interpretation from the perspective of generalization |
| --- | --- |
| error is very small on past transaction records | it may fit the training data well |
| error grows on new regions or new time periods | generalization may be weak |
| similar error ranges across various periods and regions | generalization may be relatively stable |

### Example 2. Social-Phenomenon Data Can Be Read Through The Same Generalization Question

Generalization is not needed only in business services. The same question appears in models that read social phenomena.

For example, imagine a model that classifies online opinion or post flows.

| Scene | Interpretation from the perspective of generalization |
| --- | --- |
| it reacts well to last month's style of expression | it may have adapted to the tone and pattern of past data |
| it becomes unstable when new slang, sarcasm, or indirect expressions appear | generalization to new data may be weak |
| it still reads the broad direction similarly even when the period changes | generalization may be relatively preserved |

Cases dealing with recurring social patterns such as traffic congestion or a rise in complaints are similar.

| Scene | Interpretation from the perspective of generalization |
| --- | --- |
| it matches weekday commuting-hour patterns well | it may be strong on rules it has often seen |
| it fails badly under unusual conditions such as holidays, events, or heavy rain | the range of generalization may be narrow |
| predictions do not completely collapse even under seasonal shifts or small condition changes | generalization may be relatively stable |

The common point of these examples is the same. The fact that a model saw many past cases is not sufficient by itself. Social phenomena change in expression, in conditions, and in the way people respond. So generalization can also be read as the question `does it hold up to some degree even in new social scenes?`

It also helps to note that the changes on the side of social phenomena are not just one type.

| Type of change | Example | Burden it adds to generalization |
| --- | --- | --- |
| expression change | new slang, abbreviations, sarcasm | the same meaning may appear through different surface sentences |
| condition change | holidays, events, heavy rain, policy changes | everyday patterns may weaken and exceptions may grow |
| group change | new user groups, different regions, different generations | reactions unlike the old distribution may appear |
| time change | seasonal shifts, long-term trend changes | older rules may gradually fit less well |

## Practice And Examples

### Reading The Generalization Question Through A Python Example

The following code shows how to read scores from the perspective of generalization.

Problem situation:

- Generalization can sound abstract, but in practice it can start from reading the difference between training score and validation score

Input:

- each model's `train_score`
- each model's `validation_score`

Output:

- each model's training score, validation score, and `generalization gap`

Concept to check:

- generalization is a perspective that asks about robustness on new data
- even if the gap is small, if both scores are low, it is not immediately good generalization

```python
results = [
    {"name": "model_A", "train_score": 0.81, "validation_score": 0.79},
    {"name": "model_B", "train_score": 0.99, "validation_score": 0.74},
    {"name": "model_C", "train_score": 0.63, "validation_score": 0.61},
]

for item in results:
    gap = round(item["train_score"] - item["validation_score"], 2)
    print(item["name"])
    print("  train:", item["train_score"])
    print("  validation:", item["validation_score"])
    print("  generalization gap:", gap)
```

The example output can be read like this.

```text
model_A
  train: 0.81
  validation: 0.79
  generalization gap: 0.02
model_B
  train: 0.99
  validation: 0.74
  generalization gap: 0.25
model_C
  train: 0.63
  validation: 0.61
  generalization gap: 0.02
```

In this example, `generalization gap` is not a formal theoretical explanation. It is only a supporting expression that helps readers interpret the difference between training score and validation score.

- `model_A` is relatively similar between training and validation.
- `model_B` is very high on training but much lower on validation.
- `model_C` has a small gap, but both scores are low.

So when reading generalization, looking only at `the gap` is not enough, and looking only at `the level` is not enough either. Both need to be read together.

The important interpretation here is the following.

- training score asks `how well does it match the data it has already seen?`
- validation score asks `how much does it hold up on similar data it has not seen yet?`

Generalization is closer mainly to the second question.

### Reading Generalization On Social Phenomena Through A Python Example

The next example simplifies the idea that a post-classification model can be strong on `familiar expressions` but become unstable when `new expressions` enter.

Problem situation:

- Even on the same task, it is useful to check numerically how much the model's generalization shakes when the expression style changes

Input:

- score on familiar expressions: `train_like_score`
- score on new expressions: `new_expression_score`

Output:

- the two scores for each case and the `generalization gap`

Concept to check:

- generalization is tied not only to adapting to past data but also to holding up under condition changes
- expression change is a good example of how generalization is tested even inside the same problem

```python
scenarios = [
    {"case": "posts from last month", "train_like_score": 0.93, "new_expression_score": 0.90},
    {"case": "new slang appears", "train_like_score": 0.93, "new_expression_score": 0.68},
    {"case": "sarcasm and indirect wording increase", "train_like_score": 0.93, "new_expression_score": 0.61},
]

for item in scenarios:
    gap = round(item["train_like_score"] - item["new_expression_score"], 2)
    print(item["case"])
    print("  familiar expression score:", item["train_like_score"])
    print("  new expression score:", item["new_expression_score"])
    print("  generalization gap:", gap)
```

The output can be read like this.

```text
posts from last month
  familiar expression score: 0.93
  new expression score: 0.9
  generalization gap: 0.03
new slang appears
  familiar expression score: 0.93
  new expression score: 0.68
  generalization gap: 0.25
sarcasm and indirect wording increase
  familiar expression score: 0.93
  new expression score: 0.61
  generalization gap: 0.32
```

This is not actual training code. It is a reading exercise for interpreting generalization.

- `posts from last month` has only a small difference between familiar and new expressions.
- `new slang appears` shows that the score can drop sharply when the expression changes even a little.
- `sarcasm and indirect wording increase` shows that when the surface sentence changes, the model may become even more unstable.

So in social phenomena too, generalization should be read more accurately as `how much does it hold up under new expressions and changed conditions?` rather than just `it worked well on the past`.

And the phrase `hold up` is important here. When new data enter, some difference and fluctuation always appear. Generalization asks whether the model does not completely collapse amid those fluctuations and still keeps a usable level.

## Perspective To Remember In This Section

- generalization is the property that lets a model work usefully even on data it has not seen yet
- the real goal of machine learning is not training score itself, but generalization
- both overfitting and underfitting can weaken generalization
- validation and test are ultimately tools for estimating generalization in advance
- generalization means stable robustness on new data more than perfect agreement

## Checklist

- Can you explain why generalization should be described not as `raising training score` but as `holding up on new examples of the same problem`?
- Can you distinguish which cases can be put directly into the range of generalization and which cases should be treated as a different problem?
- Can you explain that validation and test are ultimately devices for checking generalization?

After reading this Section, the following flow should continue.

| Question fixed in this Section | What will be made more concrete immediately next | What will be revisited later as a comparison criterion |
| --- | --- | --- |
| Why must a model hold up even on new data? | Through what metrics and error structures should that robustness be read? | How much better it holds up than a baseline, and whether it still holds after tuning |

## When Should This Perspective Come To Mind First

- Bring up the perspective of generalization when you need to explain again that the goal of machine learning is not training score itself, but robustness on new data.
- Return to this Section when you need to reconnect that both overfitting and underfitting ultimately weaken generalization.
- This Section becomes the criterion when you need to organize why validation and test are tools for estimating generalization in advance.

## Sources And References

- Google for Developers, `Machine Learning Glossary`, accessed 2026-06-26. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Cross-validation: evaluating estimator performance`, scikit-learn User Guide, accessed 2026-06-26. [https://scikit-learn.org/stable/modules/cross_validation.html](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, Jonathan Taylor, `An Introduction to Statistical Learning`, Springer, official website accessed 2026-06-26. [https://www.statlearning.com/](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }
- Ulrike von Luxburg, Bernhard Schoelkopf, `Statistical Learning Theory: Models, Concepts, and Results`, Max Planck Institute publication page, accessed 2026-06-26. [https://is.mpg.de/publications/4179](https://is.mpg.de/publications/4179){: target="_blank" rel="noopener noreferrer" }
