# P1-3.2 What It Means to Learn Patterns from Data

> Section ID: `P1-3.2`
> Version: `v2026.07.12`

Section 3.1 examined the strengths and limits of the way people write rules directly. This section moves to the next question. If people find it difficult to write every useful rule, how can a system obtain judgment criteria from data?

The task here is not to explain machine-learning algorithms in detail. The task is to first understand what structure is meant by the phrase `learning patterns from data`, and why this differs from a rule-based system. Algorithms such as linear regression and decision trees return in Part 4, while neural networks and deep-learning structures return in Part 5.

This section organizes the basic structure of pattern learning around `example`, `feature`, `label`, `model`, `training`, and `generalization`. The internal structure of `representation` and the contrast with rule-based approaches continue in 3.3.

## Scope of This Section

This section organizes the following questions.

- What structure is meant by the phrase “learning patterns from data”?
- What roles do examples, features, labels, and models each play?
- Why should pattern learning be read differently from simple memorization?

This section does not go deeply into the following.

- detailed calculations for algorithms such as linear regression, decision trees, and neural networks
- mathematical comparison of overfitting-prevention techniques
- experimental design for large-scale datasets

The focus here is the basic way of thinking in machine learning. The difference between rule-based approaches and representation learning continues in P1-3.3, while concrete algorithms return in Parts 4 and 5.

## Goal of This Section

- Understand the basic structure behind the phrase “learning patterns from data.”
- Distinguish the roles of example, feature, label, and model.
- See the basic difference between training and later use (inference).
- Understand why pattern learning is different from simple memorization.
- See why data quality and generalization matter.
- Connect forward to the contrast between rule-based approaches and representation learning in 3.3.

## Three Standards

This section organizes the most basic mindset of machine learning. The three points below are the structural baseline.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| learning is `finding relations in examples`, not `writing all rules directly` | This makes the difference from rule-based systems visible first. | Distinguish that the model adjusts its criteria after looking at input examples and answer examples. |
| example, feature, label, and model occupy `different roles` | These are the minimum terms needed to read Part 4 machine-learning sections. | Organize that features are input clues, labels are answers, and the model is the computational structure that writes the relation. |
| learning is not `memorization`, but finding patterns that can also work on new data | This leads naturally to generalization and overfitting. | Connect that a good learned model should also work reasonably on unseen input. |

`example`, `feature`, `label`, `model`, `training`, and `generalization` are the core terms that carry the whole section. The first large distinction that should remain is: `an example is a case`, `a feature is a clue`, `a label is an answer`, `a model is the structure that computes the relation`, `training is the adjustment of the criterion`, and `generalization is the state in which the criterion also works on new input`. The body below ties these terms together once more.

## First Read It Through a Small Example

If the section begins only with abstract definitions, the phrase “learn patterns” can feel vague. So begin with a small example of classifying customer inquiries.

Imagine that a customer center receives messages like the following.

| Inquiry sentence | Human-assigned class |
| --- | --- |
| “I want a refund.” | refund |
| “Can I cancel the payment?” | refund |
| “When will the delivery arrive?” | delivery |
| “If it does not arrive by tomorrow, I will cancel.” | delivery |
| “The item arrived broken.” | exchange or reship |
| “Please send it again.” | exchange or reship |
| “I want to change the address.” | delivery information change |
| “I want to change the recipient phone number.” | delivery information change |

If approached through rules, people would have to write rules like the following directly.

> If the sentence contains “refund” or “cancel”, classify it as refund.  
> If the sentence contains “delivery” or “tomorrow”, classify it as delivery.  
> If the sentence contains “broken” or “send again”, classify it as exchange or reship.  
> If the sentence contains “address” or “phone number”, classify it as delivery information change.

At first this can also look plausible. But ambiguous sentences soon appear.

> If delivery is delayed, can I get it resent instead of refunded?

That sentence contains clues such as `delivery`, `refund`, and `resent` together. If a system classifies the sentence from one word alone, it can easily fail. So a learning-based approach changes the question.

> Rather than asking what fixed class should be assigned whenever a certain word appears,
>
> it asks: after seeing many past inquiries and classes,
> what structure is this new inquiry most similar to?

The rest of the section can be read through that small example. Here, `example`, `feature`, `label`, `model`, `training`, and `inference` are treated only as the minimum vocabulary for explaining the training data and later model use. How features and representations differ inside the model is organized separately in 3.3.

## It Finds Relations Instead of Writing Rules

Rule-based systems work by having people write judgment criteria in sentences or code.

> if condition A and condition B are satisfied, produce result C

Machine learning uses a different approach. Instead of people writing every condition directly, the system looks for relations between input and output in past data or examples.

> example data -> training -> model -> prediction for a new input

If read again through the customer-inquiry example above, it looks like this.

| Approach | Question | Work |
| --- | --- | --- |
| rule-based | If certain words appear, which class should the system send the inquiry to? | a person writes words, conditions, and exceptions as rules |
| learning-based | What relation repeats between past inquiry sentences and their classes? | collect inquiry sentences and classes, then let the model learn the boundary |

Both approaches still receive input and produce output. The difference lies in where the judgment criterion comes from. Rule-based systems have people write the criterion explicitly, while machine-learning models adjust the criterion from data.

```mermaid
--8<-- "assets/part-01/chapter-03/rule-vs-learning-flow-en.mmd"
```

This diagram helps you compare side by side `the flow in which people write the criterion directly` and `the flow in which the criterion is adjusted from example data`. The key contrast is that `in the rule-based flow, the criterion is written outside the model`, while `in the learning-based flow, the criterion is adjusted through data`.

## A Pattern Is a Repeating Relation

In this section, a `pattern` is not just any visible repetition. A pattern usable for learning must be a relation that still helps when applied to new data.

In the customer-inquiry example, simple repetition can look like the following.

| Observation | Why caution is needed |
| --- | --- |
| when the word `cancel` appears, the inquiry is often refund-related | “If delivery is late, I will cancel” can still be mainly a delivery issue |
| when the word `again` appears, it is often a reship case | “I tried logging in again and it still failed” may instead be an account issue |
| when the word `address` appears, it is often delivery-information change | “I entered the wrong address and now want a refund” may still be mainly a refund issue |

So a pattern is closer not to one single word, but to a repeated relation created by words, context, sentence structure, and past class results together.

The KDD overview paper by Fayyad, Piatetsky-Shapiro, and Smyth describes a pattern found in data as an expression or model that describes part of the data, and expects that such a pattern should also remain useful to some degree on new data. That perspective matters for understanding machine learning. If a relation only fits the old data and fails on new data, it is difficult to call it a good learned pattern.

For example, the following relation can look like a pattern on the surface.

> Customers who clicked the blue icon last month had a lower churn rate.

But it still has to be checked whether that relation is accidental, whether it was caused by a temporary event, and whether it will repeat later. In machine learning, it is not enough to explain old data well. It is also important to find relations that are usable on new input.

| Distinction | Explanation |
| --- | --- |
| simple repetition | something that may have appeared together by accident in old data |
| useful pattern | a relation that still helps prediction or classification on new data |
| overfitting | a state that matches old data too closely and becomes weak on new data |
| underfitting | a state that fails to learn enough relation and is weak even on the training data |
| generalization | a state that works reasonably well on unseen new data |

This section introduces overfitting, underfitting, and generalization only as basic states for judging whether pattern learning worked well. Evaluation methods and validation procedures return in Part 4.

## Example, Feature, Label, and Model

From the point of view of supervised learning, data can usually be thought of as a collection of examples. Each example can contain both input values the model should use and the answer it is supposed to predict.

Google’s introductory machine-learning materials explain that, in supervised learning, examples contain features and a label. Features are the values the model uses to predict the label, and the label is the correct answer or target value the model is trying to guess.

| Term | English expression | Meaning |
| --- | --- | --- |
| example | example | one observed case or one row of data |
| feature | feature | a value used by the model as input |
| label | label | the correct answer or target value the model is trying to predict |
| model | model | the computational structure that receives features and produces a prediction |
| training | training | the process of adjusting internal model values by using examples |
| inference | inference | the process of running the trained model on new input to get an output |

The structure that should be fixed first here is this: `one example contains multiple features and one label together`. An example refers to the whole case, features are the input clues the model reads from inside that case, and the label is the answer attached to the whole case. Later paragraphs assume that structure while reading pattern learning and generalization.

| Term | Very short meaning | What it looks like in the customer-inquiry example |
| --- | --- | --- |
| example | one case | one inquiry sentence and its class result |
| feature | an input clue read by the model | clues such as words and expressions related to `refund`, `delivery`, or `address change` |
| label | the answer assigned by people | `refund`, `delivery`, `exchange or reship` |
| model | the computational structure that writes the relation between features and labels | the structure that gives scores for which class a new inquiry should be sent to |
| parameter | an internal value that changes during training | a value that affects how strongly each clue matters |
| training | the process that adjusts internal values | the stage in which the system looks at past inquiries and tunes the class criterion |
| inference | the stage of using the trained model in practice | the stage of predicting a class when a new inquiry arrives |

The first distinction that should remain in this section is: `an example is a case`, `a feature is a clue`, `a label is an answer`, `the model is the structure that writes the relation`, and `parameters are the internal values changed by training`.

Looked at through the customer-inquiry example, it becomes the following. Here, the features are simplified clues for beginner understanding, not necessarily the exact final input representation used by a real model.

| Example | Features | Label |
| --- | --- | --- |
| inquiry 1 | `refund`, `want to` | refund |
| inquiry 2 | `delivery`, `when` | delivery |
| inquiry 3 | `broken`, `arrived` | exchange or reship |
| inquiry 4 | `address`, `want to change` | delivery information change |

The model learns the relation between features and labels by looking at many examples. When training is finished, it can predict which class is more plausible for a new inquiry that does not yet have a label.

For beginners, one more step matters here. In real work, `example`, `feature`, and `label` usually do not arrive already clean and ready. There is often rough data first, such as raw inquiry text, 상담 history, and handling results. Then someone has to decide what counts as one example, what class should be assigned as the label, and what clues inside the sentence should be used as features. So the phrase `learning patterns from data` does not mean pouring raw data directly into a model. It more accurately includes the preparation work that turns real records into a `learnable example structure`.

So a whole line like `inquiry 1` or `inquiry 2` is the example, while clues such as `refund`, `delivery`, and `broken` are the input features read from inside that example. The label is the answer attached by people to the entire example, and the model learns the relation between bundles of those features and labels across many examples together.

```mermaid
--8<-- "assets/part-01/chapter-03/feature-label-training-flow-en.mmd"
```

This picture helps you read supervised learning in the order `example -> features and label -> training -> model -> prediction for new input`. The important point is that the model is not just memorizing the new input directly. It interprets new input through the criterion adjusted from examples.

## Training Means Adjusting the Criterion Inside the Model

In rule-based systems, people correct the criterion directly. In machine learning, training data and evaluation criteria are used to adjust the model’s internal `parameters`.

Parameters are adjustable internal values used by the model when it turns input into output. In linear models, coefficients can be parameters. In neural networks, weights can be parameters. This section does not go deeply into formulas; it is enough to understand a parameter here as `an internal value that changes during training`.

If the training process is simplified, it looks like this.

> 1. The model looks at an input and makes a prediction.  
> 2. It calculates the difference between the prediction and the correct answer.  
> 3. It adjusts internal values so that the difference becomes smaller.  
> 4. It repeats this across many examples.

If read as a table, the contrast with rule-based systems becomes clearer.

| Distinction | Rule-based system | Learning-based model |
| --- | --- | --- |
| who creates the criterion | people write the rules | data and the training procedure adjust the parameters |
| way of correction | add rules, remove rules, or change priority | adjust internal values through training data, objective, and algorithm |
| how errors are handled | check which rule was wrong | check what is wrong in the data, features, evaluation criterion, or model structure |
| result explanation | relatively easy to trace the applied rule | depending on the model, explanation can be difficult |

Because of this difference, machine-learning models can handle complex patterns, but the review method differs from that of rule-based systems. Reading the rules alone is not enough. Data quality, evaluation results, and failure cases must also be examined together.

## Learning Is Not Memorization

If the phrase `learn from data` is understood as `store old cases and take them out exactly as they were`, that becomes misleading. The goal of machine learning is not to memorize old data exactly, but to find relations that can be applied to new data as well.

Use the customer-inquiry example again.

| Input sentence | Label |
| --- | --- |
| “I want a refund.” | refund |
| “When will the delivery arrive?” | delivery |
| “The item arrived broken.” | exchange or reship |
| “I want to change the address.” | delivery information change |

If the model only memorized those four sentences, it would struggle with a sentence like the following.

> The item I received yesterday was damaged, and I would like to receive it again.

A good model should be able to judge that this sentence is close to exchange or reship intent, even if the wording is not exactly the same as any training example. It should use clues such as `damaged`, `receive again`, and their context.

So the aim of learning is not to answer:

> Have I seen this exact sentence before?

but rather:

> What kind of previously seen problem structure is this sentence similar to?

| State | Explanation |
| --- | --- |
| memorization | it works on training input itself but fails as soon as wording changes slightly |
| generalization | it can also respond to new input that has different wording but similar structure |
| overfitting | it follows even accidental details of training data and becomes weak on new data |
| underfitting | it fails to learn enough relation and stays weak even on training data |

Overfitting and underfitting can be read as failures in opposite directions. Overfitting is the failure of matching too much, while underfitting is the failure of not learning enough. Here, it is enough to remember that the phrase `learn patterns from data` means `find relations that can also be applied to new data`.

### A Short Distinction Exercise

Look at the following situations and first judge whether the case is closer to `memorization`, `generalization`, or `a data problem`.

| Situation | First question to ask | First interpretation in this section |
| --- | --- | --- |
| the model works well on exactly the same sentences seen in training, but often fails when wording changes only a little | did it only memorize the seen sentences? | it may be close to memorization |
| after learning “I want a refund,” it also classifies “Can I cancel the payment?” correctly as refund | did it capture the same intent even though the words differ? | it may be close to generalization |
| it works well for inquiries from one region but poorly for expressions used in another region | is the diversity of training data insufficient? | suspect a data-coverage problem first |
| it often fails even on training data and also fails on new data | did it fail to learn enough relation? | suspect underfitting first |
| it is nearly perfect on training data but performance drops sharply in production | did it become too closely fitted to the training data? | suspect overfitting first |

The key to this exercise is not only to ask `was the model correct?` but to read `why did it become correct or wrong?` from the perspective of data and generalization.

The scikit-learn example on overfitting versus underfitting shows the same point. An overly simple model may fail to explain the training data well, while an overly complex model may learn noise in the training data and become weak on new data.

## Data Quality Limits Model Quality

Learning-based models obtain their criteria from data. So if the data is narrow, biased, mislabeled, or different from the actual usage environment, the model will inherit those limits.

Google’s machine-learning introduction explains that the size and diversity of a dataset influence model performance and generalization. Even a large dataset may not represent the actual environment well if diversity is lacking. Conversely, even if diversity exists, too few examples may make it difficult to find a stable pattern.

| Data problem | Problem that can appear in the model |
| --- | --- |
| too few examples | the model can mistake accidental relations for patterns |
| lack of diversity | it works well in some situations but weakly in others |
| inaccurate labels | it learns by treating wrong answers as the standard |
| missing important features | it cannot see information necessary for judgment |
| mismatch with real usage environment | performance can fall after deployment |

For example, a rain-prediction model built only from summer data can be weak on winter precipitation patterns. A model built only from customer inquiries in one region can be weak on the expressions, products, and delivery policy of another region. To say that a model learns from data is also to say that the model follows the world-view contained in that data.

So in a machine-learning project, the important question is not only `what model should be used?`

> What data was collected?  
> What was chosen as the label?  
> What features were given as input?  
> How similar are the training data and the real usage data?  
> Does the performance hold on new data?

## The Point Where It Connects to Representation

Up to this point, the section has looked at the basic structure of training data, labels, models, and generalization. But to recognize whether two sentences are `similar in meaning`, the form in which input is handled also becomes important. The same meaning can be expressed with different words, and the same word can mean different things depending on context.

For example, the word `cancel` does not always mean a cancellation request. In a sentence such as `When will it arrive if I do not cancel it?`, meaning changes through condition, negation, and context. This issue continues in 3.3 as the difference between rule-based approaches and representation learning.

## Pattern Learning Connects to Probabilistic Judgment

Real-world data does not divide cleanly. The same word can appear with different intentions, and similar behavior can lead to different outcomes. That is why learning-based models often output not a fixed rule, but a score, probability, or ranking.

For example, an inquiry-classification model may judge a sentence like this.

| Candidate label | Model score |
| --- | ---: |
| delivery inquiry | 0.62 |
| order cancellation | 0.24 |
| refund | 0.09 |
| other | 0.05 |

These scores are signals that `the model computed it this way`. They do not mean the result is automatically the true answer. So in real learning-based systems, model outputs can be followed by a threshold, human review, or rule-based safety layer.

```mermaid
--8<-- "assets/part-01/chapter-03/score-rule-human-flow-en.mmd"
```

This structure reconnects to the conclusion of 3.1. Rule-based systems and machine learning are not related only by replacement. The model can find patterns that are too hard for people to write as rules, while rules can manage procedures and safety conditions that must be enforced.

## Cases and Examples

### Case 1. Why Inquiry-Classification Rules Keep Increasing

Imagine that a customer center wants to classify inquiries into `refund`, `delivery`, `exchange`, and `information change`. If people write rules directly, the process may begin simply: if the word `refund` appears, then refund; if the word `delivery` appears, then delivery.

But real inquiries quickly become mixed. Sentences such as `delivery is late so I want a refund`, `not a refund, please send it again`, and `I want to change the address, but first tell me whether it has already shipped` combine multiple clues in one line. The more rules people add, the more exceptions and priority problems grow together.

A learning-based approach turns this from `writing more word rules` into `finding repeated relations between past inquiries and their classes`. That creates the possibility that even when the same intent is expressed differently, the model may still group them as a similar pattern.

This case shows why 3.2 comes after 3.1. It is not because rule-based classification was wrong. It is because patterns that are difficult for people to write directly increased, and a way of learning relations from data became necessary.

## What to Remember from This Section

Learning patterns from data does not mean storing past cases exactly as they were. In the supervised-learning example of this section, it is better understood as trying to find relations between input and output in example data, then applying those relations to new data.

This shift begins from the limit of rule-based systems. In problems where people find it hard to write every exception and complex pattern directly, it becomes useful to find relations from data. But models learned from data are not perfect either. Their judgment can change depending on data quality, labels, features, evaluation, and the actual usage environment.

So when understanding learning-based AI, it is not enough to look only at the model. You must also look together at how the data was created, by what criteria it was labeled and trained, and how it is validated on new data. The next section takes over this flow and organizes how rule-based approaches and representation learning occupy different positions.

## Checklist

- I can explain `learning patterns from data` as the process of finding relations that can also be applied to new data.
- I can distinguish the roles of example, feature, label, model, training, and inference.
- I can explain that training is the process that adjusts internal model parameters.
- I can explain that learning differs from memorization and that generalization is important.
- I can explain that data size, diversity, and label quality affect model performance.
- I can explain that the way input is represented connects to the next section on representation learning.
- I can explain that model output can be a score or probability, and that real systems often need rules and review procedures together.

## When This View Should Come to Mind First

Bring back the view of this section when the phrase `learning patterns from data` needs to be explained again not as a buzzword, but as a learning structure.

- when you need to distinguish whether a model memorized rules or learned a relation that still works on new input
- when you need to organize where example, feature, label, model, training, and generalization sit
- when operational performance starts to shake and you need to judge whether data diversity, label quality, or overfitting should be suspected first

At that point, return first to the flow `example -> features and label -> training -> model -> prediction for new input`. On top of that, divide whether the current problem is closer to `memorization`, `generalization`, or `a data problem`. That stabilizes the explanation.

## Sources and Further Reading

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Tom Mitchell, [Machine Learning textbook](https://www.cs.cmu.edu/~tom/mlbook.html){: target="_blank" rel="noopener noreferrer" }, Carnegie Mellon University, McGraw Hill, 1997, accessed 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- scikit-learn, [Underfitting vs. Overfitting](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, [From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" }, AI Magazine, 1996, accessed 2026-06-22.
