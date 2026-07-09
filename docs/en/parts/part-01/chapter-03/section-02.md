# P1-3.2 What It Means to Learn Patterns from Data

> Section ID: `P1-3.2`
> Version: `v2026.07.09`

Section 3.1 reviewed the strengths and limits of writing rules directly. This section moves to the next question: if people cannot write every useful rule explicitly, how can a system obtain judgment criteria from data?

The goal here is not to explain machine-learning algorithms in detail. The goal is to understand the basic structure behind the phrase `learning patterns from data`, and why that structure is different from a rule-based system.

This section organizes the baseline meaning of `example`, `feature`, `label`, `model`, `training`, and `generalization`. The internal structure of `representation` and the contrast with rule-based approaches continues in 3.3.

## Scope of This Section

This section organizes the following questions.

- What structure is meant by “learning patterns from data”?
- What roles do examples, features, labels, and models play?
- Why should pattern learning not be read as simple memorization?

This section does not go deeply into the following.

- detailed calculations for linear regression, decision trees, or neural networks
- mathematical comparison of overfitting countermeasures
- full experimental design for large datasets

The focus here is the basic mindset of machine learning.

## Goal of This Section

- Understand the basic structure behind the phrase “learning patterns from data.”
- Distinguish the roles of example, feature, label, and model.
- See the basic difference between training and later use.
- Understand why pattern learning is not the same thing as memorization.
- See why data quality and generalization matter.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| learning is `finding relations in examples`, not `writing all rules directly` | This makes the difference from rule-based systems visible at once. | Distinguish that the model adjusts its criteria from examples. |
| example, feature, label, and model are `different roles` | These are the minimum terms needed for later machine-learning chapters. | Organize feature as input clue, label as answer, and model as computational relation. |
| learning is not `memorization`, but finding patterns that work on new data | This leads naturally to generalization and overfitting. | Connect good learning to performance on unseen input. |

## A Small Example First

Suppose a customer-support team wants to classify incoming messages.

| Message | Human-assigned class |
| --- | --- |
| “I want a refund.” | refund |
| “Can I cancel the payment?” | refund |
| “When will my delivery arrive?” | delivery |
| “If it does not arrive by tomorrow, I will cancel.” | delivery |
| “The item arrived broken.” | exchange or reship |
| “Please send it again.” | exchange or reship |
| “I want to change the address.” | delivery information change |

If this were handled only through explicit rules, someone would have to keep writing rules such as:

- if the message contains `refund` or `cancel`, classify it as refund
- if it contains `delivery` or `tomorrow`, classify it as delivery
- if it contains `broken` or `send again`, classify it as exchange or reship

This can look workable at first, but ambiguous cases appear quickly.

> If the delivery is late, can I get it resent instead of refunded?

A learning-based approach asks a different question:

> after seeing many past messages and their classes, what structure does this new message most resemble?

The rest of the section can be read through that example.

## Instead of Writing Rules, It Finds Relations

Rule-based systems begin from explicit conditions.

> if condition A and condition B hold, produce result C

Machine learning changes the center of work.

> example data -> training -> model -> prediction for a new input

The same workflow looks different when compared directly.

| Approach | Main question | Main work |
| --- | --- | --- |
| rule-based | what written condition should map to what class? | people write rules and exceptions |
| learning-based | what relation keeps repeating between past input and output? | the system uses data to adjust a model |

Both approaches still receive input and produce output. The difference lies in where the judgment standard comes from.

## A Pattern Is a Reusable Relation

In this context, a `pattern` is not just anything repeated in old data. It must be a relation that still helps on new data.

| Observation | Why caution is needed |
| --- | --- |
| the word `cancel` often appears in refund messages | “If delivery is late, I will cancel” may still be mainly a delivery issue |
| the word `again` often appears in reship requests | “I logged in again and it still failed” is not a reship request |
| the word `address` often appears in delivery-info changes | “I entered the wrong address and now want a refund” may still be a refund case |

So a useful pattern is not just one visible word. It is a relation that continues to help when context changes.

This is why terms such as `overfitting`, `underfitting`, and `generalization` appear.

| Term | Meaning at this stage |
| --- | --- |
| overfitting | the model fits old data too specifically and weakens on new data |
| underfitting | the model fails to learn enough structure even from old data |
| generalization | the model still works reasonably on unseen data |

This section only introduces these as names for the quality of learned patterns. Later Parts recover their evaluation in more detail.

## Example, Feature, Label, and Model

In supervised learning, data can be read as a collection of examples. Each example contains input information and an answer to be predicted.

| Term | Meaning |
| --- | --- |
| example | one case or observation |
| feature | a value used by the model as input |
| label | the answer or target to be predicted |
| model | the computational structure that maps features toward a prediction |
| training | the process of adjusting internal model values from examples |
| inference | using the trained model on new input |

At this stage, the important baseline is this: one example contains features and a label, and the model learns a relation between them.

| Example | Feature view | Label |
| --- | --- | --- |
| “I want a refund.” | words and clues such as `refund` | refund |
| “When will my delivery arrive?” | words and clues such as `delivery` | delivery |
| “The item arrived broken.” | clues such as `arrived` and `broken` | exchange or reship |

This table is simplified for learning. Real systems usually need an earlier preparation step that turns rough records into examples, chooses labels, and decides what counts as a usable feature.

## Training Adjusts Internal Criteria

In a rule-based system, people change the criteria by editing rules. In machine learning, training adjusts internal model parameters using data and evaluation criteria.

The process can be simplified like this.

1. The model predicts from the input.
2. The difference between prediction and answer is measured.
3. Internal values are adjusted so that the difference becomes smaller.
4. This is repeated across many examples.

The comparison with rule-based systems becomes clearer in one table.

| Distinction | Rule-based system | Learning-based model |
| --- | --- | --- |
| who sets the criteria | people write rules directly | data and training adjust parameters |
| how correction happens | add, remove, or reorder rules | change data, features, objective, or internal values |
| error review | inspect which rule was wrong | inspect data quality, labels, model behavior, and evaluation |

This is why machine-learning systems require data review and failure analysis, not only reading explicit logic.

## Learning Is Not Memorization

“Learning from data” should not be read as “storing old examples and repeating them exactly.” The aim is to find relations that still help on new examples.

If the model only remembers the old messages, it has not really learned the classification structure. Good learning means that a new message with similar meaning but different wording can still be handled reasonably.

This is why data quality matters so much. If examples are noisy, labels are inconsistent, or the collected cases represent only a narrow situation, the learned pattern becomes weak.

## Cases and Examples

### Case 1. Customer-Support Message Classification

A team may begin by writing keyword rules, but soon messages appear that mix delivery, refund, and exchange language. At that point, the problem becomes less about listing every possible phrase and more about learning reusable relations from many labeled examples. This shows the shift from explicit rule writing to pattern learning.

### Case 2. Churn Prediction from Behavioral Logs

A company may want to predict customer churn from visit frequency, payment history, and recent activity. No one can realistically write every useful behavior rule by hand. This is a case where machine learning becomes attractive because the relation must be discovered from many examples rather than authored directly.

## What to Remember from This Section

- learning from data means learning relations from examples rather than writing every rule directly
- examples, features, labels, and models occupy different roles
- good learning is not memorization; it should also work on new data
- data quality and generalization matter because the goal is reuse beyond the training set

The shortest sentence to keep is this: `machine learning learns reusable relations from examples instead of requiring people to write every judgment rule explicitly.`
