# P4-9.1 Hyperparameters

> Section ID: `P4-9.1`
> Version: `v2026.07.17`

In P4-8, the discussion chose model candidates and set the starting point of comparison with a baseline. Now it moves to the next question.

Even within the same model family, with what configuration values should training be run?

That question is exactly the starting point of the hyperparameter.

Hyperparameters are often understood as `complex advanced options`. In practice, they are a much more basic concept than that. Hyperparameters are configuration values that people set first before the model begins learning. In other words, they are not values that the model learns for itself from data, but values set from outside that determine how the model will learn.

The scikit-learn documentation explains hyperparameters as `parameters that are not directly learned within the estimator`. The same documentation explains that such values are passed as constructor arguments when creating an estimator.

A hyperparameter is not the rule that the model itself learns, but a value that fixes in advance what shape and strength the model will learn with.

This Section explains `hyperparameters`, `the distinction between learned values and values fixed in advance`, and `the effect of configuration values on comparison experiments`. Later Sections continue the current context through this handle, and the basic meaning of configuration values fixed first from outside the model reconnects through this Section and the [concept glossary](/AiBook/reference/concept-glossary/).

The first criterion that must be distinguished is the following.

| Value being seen now | First question to ask |
| --- | --- |
| weight, intercept | `Was this value learned from data?` |
| `max_depth`, `n_neighbors`, `C` | `Was this value set by a person before training?` |
| `random_state` | `Is this value for experimental reproducibility more than for performance?` |

## Scope Of This Section

This Section answers the following questions.

- What is a hyperparameter?
- How are values that change through learning different from values that a person fixes in advance?
- Why can even the same algorithm look completely different depending on hyperparameters?
- What representative hyperparameters should the reader first distinguish?

This Section first closes `how to distinguish values learned during training from configuration values fixed by a person first`. The basic comparison of GridSearchCV and RandomizedSearchCV, and the cost of validation, are handled immediately in the next Section, P4-9.2, while advanced search-space design and distributed experiment management are reorganized again in the supplementary learning of P4-9.3.

## Goals Of This Section

- You can explain a hyperparameter as `a configuration value fixed before learning`.
- You can distinguish a model parameter from a hyperparameter.
- You can say that even the same algorithm can differ in complexity, generalization, and computational cost depending on hyperparameter values.
- You can understand why a separate task called tuning is needed in the next Section.

## Learning Background

By the time the reader reaches P4-8.2, the following misunderstanding can easily appear.

`Once candidate models have been chosen, does comparison not proceed automatically now?`

In reality, that is not the case. Many settings are hidden even under the same algorithm name.

- For a decision tree, readers must decide how deep it may grow.
- For k-NN, readers must decide how many neighbors to inspect.
- For logistic regression, readers must decide how strongly regularization should be applied.

In other words, if model selection was the stage of deciding `what family should be tested`, hyperparameters are the stage of deciding `with what settings that family should be tested`.

| Curriculum position | Role of this Section |
| --- | --- |
| after P4-8 model selection | lets the reader understand setting differences inside the same model family |
| before P4-9.2 tuning | prepares the reader for why search cost and validation cost appear |
| before the algorithm Sections after P4-10 | gets the reader used to configuration-value names that will be repeated in each algorithm chapter |

In other words, this Section is the entrance that moves from `knowing the model name` to `reading the model settings`.

The connection that must be fixed here is the following.

| Immediately previous stage | What is being newly compared now | What will be checked again later |
| --- | --- | --- |
| set the starting-point score with a baseline | inspect what configuration values change the character inside the same algorithm | inspect what setting change actually changes error cases and validation scores together |

That means the baseline decides `what should be compared against`, and hyperparameters decide `what should be changed and by how much inside the same model name`. Only when this criterion is fixed can tuning in the next Section be read not as simple option manipulation, but as `comparable experiment design`.

## Main Learning Content

### How Are Parameters And Hyperparameters Different?

The very first distinction needed is this.

| Distinction | Who decides it | Example |
| --- | --- | --- |
| model parameter | decided from data during the learning process | weights and intercept of linear regression |
| hyperparameter | decided by a person before training | `max_depth`, `n_neighbors`, `C` |

This distinction appears repeatedly throughout machine learning.

- parameters are values the model `obtains through learning`
- hyperparameters are values a person `puts in first during experiment design`

If this difference is drawn very briefly, it becomes the following.

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-1-mermaid-01-en.mmd"
```

The core of this diagram is that `hyperparameters are inputs to learning`, while `parameters are results of learning`.

If the actual sentence that often confuses the reader is rewritten, it becomes the following.

- It is not correct to say `the model learns depth`.
- It is more accurate to say `a person fixes depth, and the tree learns within that condition`.

Once this difference is grasped, the tuning Section that follows becomes clearer too.

### Why Does Even The Same Algorithm Change Depending On Settings?

Hyperparameters are not just option names. They can change the very way a model sees data.

Consider a decision tree.

- If `max_depth=1`, it creates only very shallow rules.
- If `max_depth=10`, it can create much more complex rules.

Both are the same decision tree, but in practice they can behave almost like models with different characters.

This difference can be organized as follows.

| Hyperparameter change | What often changes |
| --- | --- |
| model complexity | how finely it fits |
| generalization | whether it holds up on new data |
| computational cost | how much time learning and prediction take |
| interpretability | how easy it is for a person to read |

That means hyperparameters are handles that change the `character` of a model.

If this is reduced to one sentence for the reader, it can be remembered as follows.

`A hyperparameter is a dial that changes the character of the model within the same model name.`

### Examples Of Hyperparameters Readers Often Meet

Rather than memorizing every setting of every algorithm, it is better first to look at what kinds of settings repeat.

| Model family | Representative hyperparameter | Question for the reader |
| --- | --- | --- |
| decision tree | `max_depth` | How deep should the tree be allowed to grow? |
| k-NN | `n_neighbors` | Over how many neighbors should the model judge? |
| logistic regression | `C` | How weak or strong should regularization be? |
| random forest | `n_estimators` | How many trees should be combined? |
| SVM | `kernel`, `C`, `gamma` | What kind of boundary should be created, and how sensitively should it respond? |

The purpose of this table is not to teach detailed formulas. Rather, it is to build the sense that `even if the hyperparameter names differ, many of them ultimately control model complexity, sensitivity, regularization strength, and computation volume`.

That means the `handles that change character` seen in the previous Section actually appear under these names, and from here onward the core question becomes what configuration values should be suspected first.

### What Hyperparameters Should Be Suspected First?

When the reader first sees hyperparameters, it is better not to memorize all names, but to first inspect `what character of the model this value changes`.

| Setting visible now | Axis to read first | Why read it first |
| --- | --- | --- |
| `max_depth`, `min_samples_leaf` | model complexity | because they immediately shake overfitting and rule depth |
| `n_neighbors` | locality / smoothness | because they change whether neighbors are viewed narrowly or widely |
| `C`, `alpha` | regularization strength | because they directly adjust the tendency to fit too much and the degree of generalization |
| `n_estimators` | computation volume and stability | because even if performance increases, time and resource cost also increase |
| `random_state` | reproducibility | because it first fixes repeatability of the experiment rather than performance |

The purpose of this table is not to replace detailed formulas by algorithm, but to make the reader quickly read `what handle in the model this value is changing now`.

`Why have such configuration values been treated as a separate topic for so long?`

This question matters because if the reader sees hyperparameters only as a table of options, they can easily be misunderstood as `values that can be touched one by one whenever needed`. In reality, these values shake fairness of comparison, generalization, and computational cost together.

## Detailed Learning Content

### Why Did Hyperparameters Become A Separate Topic?

If the historical background of hyperparameters is summarized very roughly, the flow is as follows.

1. In the early stage, researchers and practitioners adjusted values manually through experience.
2. Later, grid search, which tests every value in a predefined candidate table, became widely used.
3. As models and data became more complex, hyperparameter search itself became an independent research topic.

The survey paper by Marc Claesen and Bart De Moor explains that many learning algorithms have hyperparameters that must be set before training, and that the choice of those values has a large effect on performance. The same paper also summarizes that in actual practice, hyperparameter search for a long time was centered on manual search, rules of thumb, and grid search.

If this explanation is converted into the flow of the main text, it becomes the following.

`In machine learning, not only the algorithm itself, but also how well its configuration values are set, has long had a major effect on the result.`

In a 2012 paper, James Bergstra, Daniel Yamins, and David Cox point out that computer-vision algorithms depend on many configuration values, and although such tuning is often treated as a secondary matter, it can actually be decisive in performance evaluation. The paper goes further and explains that it can be difficult to distinguish whether one method is truly better or merely better tuned.

The important messages here are the following.

- Hyperparameters are not options that were added suddenly in recent years.
- For a long time, they have been `a factor that makes fair algorithm comparison difficult`.
- That is why hyperparameter search increasingly needed to be treated not as `personal intuition`, but as `a reproducible procedure`.

In other words, the history of hyperparameters should be read not as `there are now more options`, but as `the need to make model comparison fairer grew larger`.

`Hyperparameters are difficult not because there are many names, but because even the same model can produce completely different results depending on its settings.`

## Cases And Examples

### Case 1. Why Do Results Keep Changing Even With The Same Decision Tree?

An operations team raises a decision tree as a candidate in a customer-churn prediction experiment. The criteria people first looked at were behavioral signals such as `recent visit count`, `number of inquiries`, and `whether payment failed`.

However, even though the team says it experimented with the same decision tree, each member gets slightly different results. One side uses a shallow tree, so the rules are simple but the score is low. The other side uses a large depth, so the training score is very high but the validation score becomes unstable. At this point, the issue is not `the algorithm is different`, but `the settings of the same algorithm are different`.

In this scene, the hyperparameter should be read as a handle fixed in advance from outside the model. If `max_depth` is kept small, only simple rules are allowed. If it is made large, more complex rules are allowed. In other words, the data determine what the decision tree learns, but people decide first how complex it may become.

The confirmable result appears when train score and validation score are viewed together. If the reader compares how training score and validation score change when depth is changed, the reader can explain why a hyperparameter is not a simple option, but a setting that changes model character.

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-1-mermaid-02-en.mmd"
```

Historical explanation alone may still feel weak. In practice, the point that hyperparameters are not `extra options`, but factors that shake results strongly, was repeatedly observed in many cases.

#### Case 1. In Computer Vision, Even The Same Family Became Hard To Compare Depending On Tuning

The 2012 paper by Bergstra, Yamins, and Cox explains that many computer-vision algorithms depend on many configuration values, and how those settings are chosen can be decisive for evaluating the potential of the algorithm. The paper reports strong results on three different tasks such as face verification (LFW), face identification (PubFig83), and object recognition (CIFAR-10) by using automated model-search procedures.

The reason this case matters is simple.

- It is not enough to say only `which algorithm is better`.
- Even the same algorithm family can look entirely different if the settings differ.
- That is why it is hard to separate algorithm comparison from hyperparameter comparison.

#### Case 2. Grid Search Was Not Always Efficient

The 2012 JMLR paper by Bergstra and Bengio explains that in hyperparameter space, often only a few values strongly affect actual performance. The paper showed that in such situations, random search can be more efficient than grid search.

- A method that inspects every axis densely at equal intervals is not always good.
- In reality, a few important hyperparameters may shake the result greatly, while other values matter less.
- That is why what mattered became not simply `it was run a lot`, but `what space was inspected and how`.

In other words, the hyperparameter problem developed not as simply trying many values, but as `the problem of designing the search method itself`.

#### Case 3. The Small Decision-Tree Example In This Section Shows The Same Phenomenon

The small Python example above is only a toy experiment, but it shows the empirical meaning of hyperparameters directly.

- With `max_depth=1`, both train and test scores are low.
- With `max_depth=3`, train and test scores rise together.
- With `max_depth=None`, train score becomes highest, but test score can instead weaken.

Even this small example shows that hyperparameters can shake the following three things at once.

| Observation | Meaning |
| --- | --- |
| rise in train score | the model follows the training data better |
| test score stagnates or falls | generalization does not always improve together |
| same algorithm, different result | the configuration value itself becomes a comparison target |

That means the history of hyperparameters is not only the history of some grand separate field. It was a problem visible immediately even in small exercises, and as that problem grew larger it became a common topic of research and practice.

### Why Must Hyperparameters Be Fixed Directly By People?

The scikit-learn documentation on hyperparameter tuning explains that because such values are not directly learned inside the estimator, it is possible and recommended to search them based on cross-validation scores. This explanation can be summarized directly in the following sentence.

`Because data do not tell hyperparameters by themselves, several values must be tested and compared through validation scores.`

That means that even when data let the model learn parameters directly, hyperparameters usually must be chosen `through experiments`.

At this point, what matters is the issue of the search range: `what values should be tested, and how far`.

`What values should be tested, and how far?`

That question is exactly tuning.

### Why Should Practitioners Not Increase Hyperparameters Carelessly?

People often feel that the more they touch hyperparameters, the more performance will continue to improve. In reality, the opposite risks are also large.

- The number of experiments can increase rapidly.
- The reader can overfit by looking at validation data too often.
- A setting that looks good by chance can be mistaken for `real improvement`.

The scikit-learn common pitfalls documentation explains that if test data enter model selection, performance estimation can look overly optimistic. This risk appears in the same direction not only in preprocessing but also in hyperparameter selection. In other words, if settings are chosen while looking at test data, that may not be `building the model well`, but `fitting to the test`.

In practice, the following rules matter.

1. Split train and test first.
2. Compare hyperparameters through validation procedures inside train.
3. Keep test only for the final check.

This Section fixes that principle as the baseline rule, and the actual search methods are handled in the next Section.

### A Small Example To Build Intuition

How does the result change if the same decision tree is given different depths?

Below is a very small toy example.

| Setting | Reader intuition |
| --- | --- |
| `max_depth=1` | allows only very simple rules |
| `max_depth=3` | allows somewhat more complex rules |
| `max_depth=None` | can continue getting deeper until the stopping condition |

Even from this table alone, the reader can see that hyperparameters change not the `model type`, but the `range of model behavior`.

That means the sense the reader should hold in this Section is the following.

- Even if the model name is the same, comparison results can change if settings differ.
- That is why it is not enough to write only `what model was used`.
- The experiment becomes readable again only when `with what settings it was used` is also written down.

## Practice And Examples

### Looking At Hyperparameter Differences Through A Python Example

The example below is an exercise that changes only `max_depth` in the same decision-tree algorithm and observes how the training result changes.

- Problem situation: treat flower data (iris) as a classification problem of species.
- Input: four features, sepal length, sepal width, petal length, and petal width.
- Label: three species classes.
- Concept to check: even with the same algorithm, train score and test score can differ when the hyperparameter changes.

```python
# This example compares how hyperparameter settings change model performance and behavior on the Iris dataset.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for depth in [1, 3, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"max_depth={depth}")
    print("  train accuracy:", round(train_score, 3))
    print("  test accuracy :", round(test_score, 3))
    print("  tree depth    :", model.get_depth())
    print()
```

An example of the execution result is as follows.

```text
max_depth=1
  train accuracy: 0.667
  test accuracy : 0.667
  tree depth    : 1

max_depth=3
  train accuracy: 0.981
  test accuracy : 0.933
  tree depth    : 3

max_depth=None
  train accuracy: 1.0
  test accuracy : 0.911
  tree depth    : 5
```

What this example shows is simple.

- Even for the same decision tree, the result changes if the value of `max_depth` changes.
- If unlimited depth is allowed, train accuracy can become very high.
- But test accuracy does not necessarily improve together.

That means a hyperparameter is `a configuration value that changes the generalization behavior without changing the model type`.

## Supplement To The Detailed Learning Content

### What Kind Of Hyperparameter Is `random_state`?

A value that often confuses readers is `random_state`.

This value usually does not directly change model complexity, but it is a setting that helps reproduce the same result in learning or data splitting where randomness is involved.

The scikit-learn documentation explains that some estimators and cross-validation splitters inherently contain randomness, and that `random_state` controls that randomness.

`random_state` is a handle that makes it easier to confirm the same result when the experiment is run again, rather than a handle that raises performance.

So `random_state` has a somewhat different role from other hyperparameters.

| Type of hyperparameter | Representative role |
| --- | --- |
| values that change model character | `max_depth`, `n_neighbors`, `C` |
| values that help experimental reproducibility | `random_state` |

This distinction becomes especially important later when organizing experiment comparison.

## Checklist

- Is the value being inspected now a learned parameter or a hyperparameter fixed in advance?
- Do you understand that even for the same algorithm, changing settings can change the result?
- Can you explain why train score and test score must be viewed together?
- Have you distinguished that `random_state` is more related to reproducibility than to performance improvement?
- Can you anticipate why the next Section must look at `search range` and `validation cost` together?
- Can you explain that a hyperparameter is a configuration value fixed by a person before learning, while a parameter is learned from data?
- Can you explain that even the same algorithm can differ in complexity, generalization, and computational cost depending on hyperparameters?
- Can you explain that touching many hyperparameters also increases experiment cost and validation cost?

## Sources And References

- scikit-learn, `Glossary of Common Terms and API Elements`, scikit-learn User Guide, accessed 2026-06-26. [https://scikit-learn.org/stable/glossary.html](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`, scikit-learn User Guide, accessed 2026-06-26. [https://scikit-learn.org/stable/modules/grid_search.html](https://scikit-learn.org/stable/modules/grid_search.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `12. Common pitfalls and recommended practices`, scikit-learn User Guide, accessed 2026-06-26. [https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }
- Marc Claesen, Bart De Moor, `Hyperparameter Search in Machine Learning`, arXiv, 2015, accessed 2026-06-26. [https://arxiv.org/abs/1502.02127](https://arxiv.org/abs/1502.02127){: target="_blank" rel="noopener noreferrer" }
- James Bergstra, Daniel Yamins, David D. Cox, `Making a Science of Model Search`, arXiv, 2012, accessed 2026-06-26. [https://arxiv.org/abs/1209.5111](https://arxiv.org/abs/1209.5111){: target="_blank" rel="noopener noreferrer" }
- James Bergstra, Yoshua Bengio, `Random Search for Hyper-Parameter Optimization`, Journal of Machine Learning Research, 2012, accessed 2026-06-26. [https://jmlr.org/beta/papers/v13/bergstra12a.html](https://jmlr.org/beta/papers/v13/bergstra12a.html){: target="_blank" rel="noopener noreferrer" }
