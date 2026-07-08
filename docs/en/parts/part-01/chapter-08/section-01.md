# P1-8.1 Supervised Learning: Inputs and Labels

> Section ID: `P1-8.1`
> Version: `v2026.07.07`

Chapter 7 dealt with search spaces, computational limits, and heuristics. Now we move into learning types. The first baseline is `supervised learning`.

The core of this section is not an algorithm, but the `label`. To understand supervised learning, we first need to ask what the label points to. If we treat a label vaguely as `the answer`, we can easily miss the more important issue: what standard people attached to the data in the first place.

In Korean explanation, it is often safer to understand a label as something closer to an identification tag than as an absolute statement of truth. A label is a marker attached so that the data can be distinguished. `Labeling` is the act of attaching such markers. Explanations of data labeling from AWS and IBM also describe it as identifying raw data and assigning labels to it. That marker tells the model what standard it should follow, but it does not automatically mean the label is absolute truth in every sense.

So the central question of this section is:

> what does a label point to,  
> and how does the model try to follow that label standard?

Supervised learning uses examples in which `input` and `label` are given together. The model is trained so that when a new input arrives, it produces an output that follows the label standard. So in 8.1, the main object of attention is not the complex inside of the model, but the meaning and standard of the labels attached to the data.

> supervised learning is not the memorization of a list of labels; it is the matching of relationships between inputs and labels

In Part 1, this section fixes the basic distinction among `supervised learning`, `label`, `labeling`, `target`, `classification`, and `regression`. The basic distinction between `input` and `output` was handled first in 4.2, and the execution flow of `training` and `prediction` was handled in 5.1 and 5.2. Since Chapter 7 already organized search and heuristics, this section can focus directly on the structure created by `labeled data`.

## Scope of This Section

This section does not calculate supervised-learning algorithms. Linear regression, logistic regression, decision trees, support vector machines, and neural networks only pass by as names.

It also does not explain loss functions, gradient descent, validation data, or overfitting in detail. Those return later in Part 4.

Likewise, this section does not redefine `input` and `output` at length. Their basic distinction was already fixed in 4.2, and the difference between training and inference was handled in Chapter 5. Here we add one layer on top: how examples with labels become a training signal.

The working definition here is:

> supervised learning is the method of training a model to predict outputs for new inputs by using examples where input and label are given together

## Goal of This Section

- Understand what a label indicates in supervised learning.
- Read a label as something closer to an identifiable marker than to an absolute answer.
- Explain labeling as the act of attaching distinguishing markers to data.
- Understand supervised learning as using examples that contain both input and label.
- Distinguish the relation among label, target, and expected output.
- Distinguish classification from regression at an introductory level.
- Understand that the presence of labels does not always mean absolute truth.
- Prepare to keep supervised learning, unsupervised learning, and reinforcement learning separate.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| supervised learning uses examples that contain both inputs and labels | This is the most basic standard that separates it from other learning types. | It is enough to understand that people-attached distinguishing markers come together with past examples. |
| a label is more accurate when read as an `identification marker` than as absolute truth | This reduces the mistake of treating labels as unquestionable answers. | Keep the intuition that labels are markers attached to distinguish cases. |
| the model tries to generalize that label standard to new inputs | This summarizes the goal of supervised learning in one sentence. | Understand it as an attempt to apply standards seen in past examples to new ones. |

At the minimum, the distinction to keep is:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| supervised learning | learning from examples that contain labels | the first baseline in Chapter 8 |
| label | target marker attached to data | the standard the model tries to fit |
| labeling | the act of attaching labels to data | the preparation that builds the learning standard |
| target | the value the model is meant to match | often close in meaning to label |
| classification | predicting a categorical label | one representative form of supervised learning |
| regression | predicting a numeric label | another representative form of supervised learning |

## A Label Is a Signal That Tells the Model What Direction to Learn

A `label` is the value attached to data that tells the model what output it is expected to match. In supervised learning, the word `supervised` does not mean a person gives direct instructions at every step. It is closer to meaning that labels inside the training data serve as signals that guide learning.

For example, if customer-support sentences are labeled as `delivery`, `refund`, or `exchange`, the model is trained to match the relationship between the sentence and that label. If price data includes actual sale prices, the model is trained to match the relationship between input conditions and that numeric label.

So a label is not just a name tag. More precisely, it is a distinguishing marker attached within a problem definition. In that sense it resembles a symbol in the broad sense that people assign a sign such as `delivery`, `refund`, or `exchange` to distinguish one type of case from another. But labeling is not the same thing as symbolic AI. Labeling is a preparation step for machine learning.

> a label is a distinguishing marker attached to data  
> labeling is the act of attaching that marker  
> the marker is then used as the target output the model is trained to match  
> the label standard determines the direction of learning

## Supervised Learning Starts from Labeled Examples

Google’s Machine Learning Glossary explains supervised learning as training a model from input features and the labels associated with them. It also explains that a labeled example contains one or more features and a label, and that such examples are used for training.

At this stage, we do not need to go deeply into features. The first important structure is simpler:

> input + label = labeled example

For customer-support classification:

| Input | Label |
| --- | --- |
| `I want a refund.` | refund |
| `When will the delivery arrive?` | delivery |
| `The item arrived broken.` | exchange |
| `Can I cancel the payment?` | refund |

The model sees these examples and then predicts which label fits a new sentence:

> new input: `The product I ordered still has not arrived.`  
> model output: delivery

The crucial point is that supervised learning uses a standard already attached by people. Without labels, the same problem would have to be approached differently.

## Label, Target, and Expected Output

In supervised learning, the label is the target output the model is meant to match. Google’s glossary explains `target` as a synonym for `label`.

The practical reading used in this book is:

| Expression | Meaning in this section |
| --- | --- |
| label | the distinguishing marker attached to data and used as target output |
| labeling | the act of attaching labels to data |
| target | the value the model is meant to match; often nearly the same as label |
| expected output | the output that people expect the model to produce |

In introductory explanation, labels are often called `answers`. But this wording should be read carefully. A label is usually a distinguishing marker attached within a specific problem definition and data-collection standard.

Consider the sentence:

> I want to cancel the payment.

Its label may differ depending on the labeling scheme:

| Labeling scheme | Possible label |
| --- | --- |
| workflow handling | cancellation |
| customer intent | refund |
| payment-system classification | payment |

So a label is not an absolute truth floating outside context. It is a marker attached inside a specific problem definition and used as a target value for supervised learning.

> a label is a distinguishing marker attached inside a problem definition  
> in supervised learning, that marker is used as the target output  
> if the problem definition changes, the label for the same input may also change

## The Basic Flow of Supervised Learning

The basic flow can be summarized like this:

> collect labeled examples  
> let the model predict outputs from inputs  
> compare predictions with labels  
> train the model so the gap becomes smaller  
> use the trained model to predict for new inputs

Using customer-support examples:

| Stage | Explanation |
| --- | --- |
| data preparation | collect past support sentences and human-assigned labels |
| training | adjust the model so it matches the relation between sentences and labels |
| prediction | when a new sentence arrives, output a label |
| evaluation | check whether the prediction fits the actual business standard |

As Chapter 5 explained, training is the procedure that adjusts internal model values. In 8.1, the point is to see why this labeled-data setting is called supervised learning.

## Classification Predicts Categorical Labels

`Classification` is a supervised-learning problem where the input is assigned to one or more predefined categories or labels. The key is that the label is categorical. Google’s glossary distinguishes classification models, which predict classes, from regression models, which predict numeric values.

Customer-support type selection is a classification problem:

| Input | Possible label |
| --- | --- |
| `The delivery is late.` | delivery |
| `I want a refund.` | refund |
| `The product is damaged.` | exchange |

Typical classification outputs are category labels:

| Problem | Input | Label |
| --- | --- | --- |
| spam classification | email title and body | spam, normal |
| support-message classification | support sentence | delivery, refund, exchange, other |
| image classification | image | cat, dog, car |
| risk detection | transaction information | normal, suspicious |

This section does not go deeply into probability estimates or thresholds. Their place was already introduced in P1-6.3 and P1-7.3.

## Regression Predicts Numeric Labels

`Regression` is a supervised-learning problem where the model predicts a continuous numeric value. Here the label is not a category name but a number. Google’s glossary also explains that regression models predict numeric values.

Examples:

| Problem | Input | Label or target |
| --- | --- | ---: |
| delivery-time prediction | region, distance, order time, carrier state | expected duration |
| product-price prediction | product attributes, season, inventory, demand | price |
| server-cost prediction | request count, data transfer, instance count | monthly cost |
| temperature prediction | time, region, pressure, humidity | temperature |

Classification and regression are both supervised learning. The difference is the form of the label:

| Distinction | Label form | Example |
| --- | --- | --- |
| classification | category | delivery, refund, exchange |
| regression | number | 3.5 hours, 12,000 won, 27.2 degrees |

The introductory summary is:

> classification chooses a name tag  
> regression predicts a number

## In Supervised Learning, Label Standards Matter

In supervised learning, labels are the learning signal. So if the label standard is unstable, the model also becomes unstable.

Labeling is the act of attaching distinguishing markers to data. That can look like simple data entry, but in reality it is the act of deciding `what counts as the same thing` and `what should be distinguished`.

If different people attach different labels to the same support sentence, the result becomes unstable:

| Input | Label A | Label B | Problem |
| --- | --- | --- | --- |
| `I want to cancel the payment.` | refund | cancellation | intent standard and workflow standard are mixed |
| `I want to change the address.` | delivery | address change | the label system overlaps |
| `The item arrived broken.` | exchange | defective item | handling method and cause classification are mixed |

Such data still satisfies `having labels`, but it is not necessarily good supervised-learning data, because the standard the model is meant to fit is inconsistent.

Questions to ask when designing labels:

> does the label match the work objective?  
> can different people apply the same standard?  
> do labels overlap with one another?  
> can the model really predict the label from the actual available input?

Whenever possible, the label standard should be documented together with the dataset. The *Datasheets for Datasets* proposal is helpful here because it argues that motivation, composition, collection process, and recommended use should all be documented so that the dataset is understandable to later users. At the level of 8.1, the key point is simply that label standards are part of dataset context.

## Having a Label Does Not Automatically Mean Having Truth

Supervised learning is often explained as `learning from data with the correct answer`. As an introductory metaphor, that can be useful, but it should not be read too literally. The more careful phrase is `learning from data that has labels`.

Some labels are relatively clear:

| Input | Label |
| --- | --- |
| image of a handwritten digit | one of 0 through 9 |
| product sales record | actual sale price |

But many real-world labels are not that simple. They can depend on business conventions, human judgment, timing, or partial information. So a label is better understood as a target marker attached under a specific definition than as an absolute universal answer.

## What to Remember from This Section

Supervised learning uses examples in which input and label are given together. The model learns not by memorizing label names one by one, but by trying to generalize the relationship between inputs and the attached label standard.

> supervised learning = training from examples that contain both inputs and labels  
> label = the target marker attached to data  
> labeling = the act of attaching those markers

The safest reading is that labels are standards inside a problem definition, not automatically absolute truth.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- AWS, [What is data labeling?](https://aws.amazon.com/what-is/data-labeling/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- IBM, [What is data labeling?](https://www.ibm.com/think/topics/data-labeling){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daumé III, Kate Crawford, [Datasheets for Datasets](https://arxiv.org/abs/1803.09010){: target="_blank" rel="noopener noreferrer" }, 2021-03-01, accessed 2026-06-23.
