# P1-3.3 Rule-Based Approaches and Representation Learning

> Section ID: `P1-3.3`
> Version: `v2026.07.20`

Section 3.1 examined the strengths and limits of the way people write rules directly, and Section 3.2 examined the basic structure of learning patterns from data. This section does not explain the whole learning process again. Instead, it narrows the focus to one point: what changes when the system handles input in different forms?

The central question is simple. What is different between the approach in which people write rules directly and the approach in which a model learns representations from data?

The task here is not to explain the internal details of deep learning. It is to first fix the positions of `rule`, `feature`, `representation`, and `parameter` so that they do not get mixed together.

In Part 1, the baseline meanings of `representation`, `vector`, `activation`, and `representation learning` are fixed in this section. The earlier structure of `example`, `label`, `training`, and `generalization` was already fixed in 3.2, and is reconnected here only as much as needed to explain what internal form the input turns into inside the model, and how that differs from rule-based approaches.

This section organizes the following questions.

- What is different between rule-based approaches and representation learning in the way input is handled?
- What is the safest way to read the relation between features and representations?
- What does it mean to say that learned representations are powerful but can be hard to interpret?

This section first closes the positional difference between rules and representations. The more systematic organization of input, output, data, features, and parameters continues immediately in Part 1 Chapter 4.

## Separating the Places of Rules, Features, and Representations

- Distinguish rule-based approaches from representation learning.
- Understand the relation between features and representations.
- See the difference between features designed by people and representations learned by the model.
- Understand that learned representations can be strong but hard to interpret.
- Connect forward to the input, output, data, feature, and parameter concepts used in Part 1 Chapter 4.

## Three Standards

This scene is about the form in which the model handles input. The following three points are the structural baseline.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a rule is a `criterion written outside`, while a representation is an `internal form used inside the model` | This makes the location difference between rule-based and learning-based approaches visible. | Distinguish that rules are readable, while representations are internal values for computation. |
| a feature can be designed by people, while the model may transform it into deeper representations | This leads to the difference between traditional machine learning and deep learning. | Organize that human-made clues and model-learned internal forms are not the same thing. |
| learned representations are powerful, but can make it harder to read `why the model saw it that way` | This connects naturally to why model interpretation and evaluation are needed. | Connect broader handling of similarity with weaker direct explainability. |

`rule`, `feature`, `representation`, `vector`, `activation`, and `parameter` are the core terms repeated throughout this section. The first broad distinction that should remain is: `a rule is an external criterion`, `a feature is a clue extracted from input`, `a representation is an internal form`, `a vector is a bundle of numbers`, `an activation is an intermediate value`, and `a parameter is a learned criterion`. Each term is tied together again in the body below.

## First Look at the Same Problem in Two Ways

Keep using the customer-inquiry classification example. Suppose the following sentence comes in.

> If the delivery does not arrive by tomorrow, I will cancel it.

Under a rule-based approach, a person writes the conditions directly.

> If the sentence contains “delivery” and “tomorrow”, classify it as a delivery inquiry.  
> If the sentence contains “cancel”, mark it as an order-cancellation candidate.  
> If both conditions appear together, send it to human review.

These rules can be read by people. It is also comparatively easy to trace which condition produced which result. But someone has to keep writing the conditions and exceptions.

A learning-based model takes a different route. As seen in 3.2, the model is trained from past inquiries and their classes. The new point in this section is that the model changes the sentence into internal values, and then uses those internal values to compute which class is more plausible.

> sentence -> internal representation -> model computation -> class score

The key point here is `internal representation`. The model does not simply read the sentence exactly as it appears. It changes the sentence into a bundle of computable values and uses that for prediction.

```mermaid
--8<-- "assets/part-01/chapter-03/representation-vs-rules-flow-en.mmd"
```

This diagram only shows that the same input can be processed in two branches. The left branch is a structure in which rules written in advance by people influence the result directly. The right branch is a structure in which the input is first changed into an internal representation the model can compute over, and only then is a prediction produced. The key point of this section is not `which one is better`, but the difference between whether the criterion is `written outside` or `computed inside the model`.

## The Boundary of This Section: It Focuses on Representation, Not All of Learning

Section 3.2 explained the basic structure of training data, labels, models, training, and inference. Section 3.3 does not repeat that structure. The concern here is how input changes into some internal form inside the model, and how that differs from rules written by people.

| Distinction | Center of 3.2 | Center of 3.3 |
| --- | --- | --- |
| question | what does it mean to learn patterns from data? | what does it mean to turn input into a representation? |
| key terms | example, label, model, training, inference, generalization | rule, feature, representation, parameter |
| main risk | memorization, overfitting, data-quality problems | difficulty of interpretation and opacity of representation |
| next connection | the learning structure of machine learning | the process of turning a problem into a model-friendly form |

## Rules Are Outside, Representations Are Inside

Explicit rules are close to the outside of the system. They exist in forms that people can read, document, and revise.

> If a condition is satisfied, produce a certain result.

Learned representations, by contrast, live inside the model. They are intermediate values created as input passes through the model, or values created when learned parameters transform the input. Those values are not usually sentences or rules that people can read directly.

| Distinction | Explicit rule | Learned representation |
| --- | --- | --- |
| location | code, configuration, knowledge base, policy document | vectors, activations, and parameters inside the model |
| how it is created | a person writes the condition and result directly | adjusted through data and training procedure |
| strength | easier to read, review, and control | better at handling complex patterns and context |
| weakness | difficult to manage when exceptions grow | can be hard to explain why the judgment came out that way |
| how it is changed | add, remove, or reprioritize rules | adjust data, labels, features, the model, or the training procedure |

When terms such as `representation`, `vector`, `activation`, and `parameter` appear together, they can all sound like the same kind of internal value. So they should be tied together once here as a baseline, and the rest of the section can assume that distinction.

| Term | Very short meaning | What to remember in this section |
| --- | --- | --- |
| representation | the internal form that makes input usable for the model | the sentence people read and the form the model computes over can differ |
| vector | a bundle of numbers arranged side by side | representations are often handled in this kind of numeric bundle |
| activation | an intermediate value computed at one stage inside the model | think of it as the value while the input is changing as it passes through layers |
| parameter | an internal value adjusted through learning | the criterion that influences how the model transforms the same input |

The first distinction that should remain here is: `a representation is an internal form`, `a vector is the numeric bundle that can hold that representation`, `an activation is a computed intermediate value`, and `a parameter is the value adjusted through learning`.

As a short analogy, a `vector` can be read as the numeric table that carries the representation, while an `activation` can be read as the current value of that table after the model has actually computed one step. For example, if the inquiry sentence goes through one layer and produces something like `[0.2, 0.8, -0.1, ...]`, that bundle is a vector-shaped representation and at the same time the activation value computed at that layer. The key difference to keep is: `vector` is the format, while `activation` is the value at a computation step.

Once this distinction is understood, the expression “the AI created rules by itself” can be read more carefully. The model may have learned internal criteria, but it did not automatically produce a human-readable list of rules.

## Features Can Be Designed by People, and Representations Can Be Learned by the Model

Section 3.2 explained a feature as a value the model uses as input. Features can arise in two ways.

First, people can design them directly.

| Original input | Human-designed feature |
| --- | --- |
| inquiry sentence | whether the word `refund` is present |
| inquiry sentence | whether the word `delivery` is present |
| inquiry sentence | sentence length |
| inquiry sentence | whether a negative expression appears |
| customer information | recent number of orders |

These features sit between rule writing and learning. People decide what value to calculate, but the final judgment can still be learned by the model. In this section, such values are read as `human-designed input features`, and are distinguished from the `learned representations` discussed later.

Second, the model can learn representations. In deep learning in particular, the input can pass through several layers and become a different representation at each stage. So a human-made feature may be the starting point, but inside the model that input can still be turned into a more abstract internal representation.

The Stanford Encyclopedia of Philosophy entry on AI explains this with face images: lower layers may react to clues such as edges, the next layers may combine them into face parts such as eyes or noses, and higher layers may respond to bundles of those features. This kind of explanation helps distinguish deep learning from the approach in which people try to write every feature directly.

```mermaid
--8<-- "assets/part-01/chapter-03/layered-representation-flow-en.mmd"
```

This diagram shows that input does not have to be understood all at once. It can change through several stages into representations at different levels. The key point is that `low-level features` are comparatively small clues, `intermediate representations` are combinations of several clues, and `higher-level representations` are closer to more abstract bundles of meaning. A real model is not necessarily stored with such neat stage names, but the structure that `the input changes gradually into different representations` still remains.

If simplified through the customer-inquiry example, it can be read as follows.

| Stage | Human-readable explanation |
| --- | --- |
| raw text | “If the delivery does not arrive by tomorrow, I will cancel it.” |
| low-level clues | `delivery`, `by tomorrow`, `if it does not arrive`, `cancel` |
| intermediate representation | delivery delay, time condition, cancellation possibility |
| higher-level representation | the customer is requesting a solution under a deadline condition |
| output | delivery inquiry or cancellation-related review |

It should not be claimed that the real internal representation of a model is stored as human-readable stages like this. This table is only a simplification for understanding the concept. What matters is that input changes into computable representations inside the model, and that those representations are used for prediction.

## When the Representation Changes, the Difficulty of the Problem Changes

The review by Bengio, Courville, and Vincent on representation learning explains that the success of machine-learning algorithms depends strongly on how data is represented. Even with the same data, one form of representation can make important factors stand out, while another can hide them.

For example, in inquiry classification, the following two sentences look different if seen only as raw strings.

> The item arrived broken.  
> The product I received yesterday was damaged, and I want it sent again.

But if read at the level of meaning, both can connect to `received item`, `damage`, and `exchange or reship possibility`. A good representation makes such common structure easier for the model to use.

| Representation style | What the model sees more easily | What it can miss |
| --- | --- | --- |
| raw string | exact repetition of the same words | different expressions with the same meaning |
| human-designed keywords | presence of important words | context, negation, and conditions |
| learned representation | combinations of several clues and broader similarity | internal criteria that are harder for people to read directly |

That is why, in machine learning, the question `what algorithm should be used?` is not the only important question. It is also important to ask `what form should the input be turned into?`

## Learning Analogy: Grouping by Meaning Units

When describing fast human judgment, one might think of an expression like “context compression.” In this book, however, this is used only as a learning analogy, not as a standard neuroscience term. The “compression” here means something closer to how people use concepts and remembered definitions to handle a complicated situation as a smaller number of meaning units.

In cognitive psychology, one can connect this loosely to ideas such as chunking and recoding. Miller’s classic paper explains that people can increase the amount of information they handle by organizing input into familiar units or chunks and then regrouping those chunks into larger bundles. This reference is used only to support the analogy about human information handling, not as evidence that machine-learning models understand in a human way.

For example, the sentence `If the delivery does not arrive by tomorrow, I will cancel it.` can be grouped by meaning units rather than read one token at a time.

| Expression visible in the input | Grouped meaning unit |
| --- | --- |
| if the delivery does not arrive by tomorrow | delivery delay and deadline condition |
| I will cancel it | cancellation intent or cancellation possibility |
| the whole sentence | the customer is requesting problem resolution under a time condition |

This analogy matters not because it proves representation learning is “human-like understanding.” It matters because it shows that a judgment problem can become easier or harder depending on what units the details of the input are reorganized into.

## Learned Representations Are Less Crisp than Rules but Can Respond More Broadly

An explicit rule is crisp.

> If the phrase indicates an address change, send it to delivery-information change.

But real sentences are not crisp.

> I wrote the wrong recipient number.  
> If it has not shipped yet, can it be sent somewhere else?  
> Please send it to the office instead of the previous address.

Even without using the exact phrase `address change`, these sentences can all relate to delivery-information change. Learned representations can be advantageous in handling such similarity because the model can reflect not just one word, but the way several clues appear together in its internal values.

But the same advantage is also a risk. It can be difficult for people to read directly which clue mattered how much, and the model may also follow bias or accidental repetition in the training data. That is why evaluation, failure-case analysis, and data review become important in systems using learned representations.

| Situation | When rules are advantageous | When learned representations are advantageous |
| --- | --- | --- |
| legal prohibition condition | when something must be blocked clearly | only as an auxiliary detection signal |
| approval procedure | when it must be fixed who approves under what condition | when recommending exception candidates |
| sentence classification | when keywords are explicit | when expressions vary and context matters |
| image recognition | when simple color or size conditions are enough | when lighting, pose, and background vary a lot |
| operations automation | when the procedure must repeat exactly | when trying to find candidates for anomaly signs |

## Rules and Representations Do Not Only Compete

If rule-based approaches and learning-based approaches are divided only into `old method` and `new method`, real systems become harder to understand. Many systems use both together.

For example, an automatic customer-inquiry classification system can be structured like this.

```mermaid
--8<-- "assets/part-01/chapter-03/policy-model-review-flow-en.mmd"
```

This diagram means that `policy rules can first filter forbidden and required conditions at the front`, then `the model can calculate classification candidates while reflecting diversity of expression`, and finally `depending on the score or sensitivity, the case can split into automatic handling or human review`. In other words, the purpose of the diagram is to show that rules and models can divide responsibility inside one system.

### A Short Exercise in Role Distinction

Look at the following cases and first distinguish whether the central difficulty is closer to `rule design`, `representation learning`, or `a combination of both`.

| Case | First question to bring to mind | First-pass judgment by the standard of this section |
| --- | --- | --- |
| a prohibition such as `if a resident-registration number appears, do not store it` must be enforced | can the condition be written clearly as a sentence by people? | closer to rule design |
| expressions such as `please send it to the office`, `I want to change the receiving place`, and `please modify the delivery address` should be grouped as one intent | must the system treat different surface forms as close in meaning? | closer to representation learning |
| customer inquiries should be classified automatically, but messages containing sensitive information should go to human review | must policy blocking and semantic classification be handled together? | closer to a combination of both |
| fine cracks must be found in product images | can people write all the useful visual features directly? | stronger weight on representation learning |
| approval stages must be divided by amount ranges according to policy | is the center of the task an explicit standard rather than varied expression? | closer to rule design |

The key to this exercise is not to ask `which is more modern, rules or representation`. It is to first separate `which part can be written explicitly by people` and `which part requires learning similarity from data`.

In that structure, rules take responsibility for policies that must always be followed, while the model handles the diversity and similarity of expressions that are difficult for people to write directly.

For example, the roles can be divided like this.

| Role | Main handling method |
| --- | --- |
| do not respond automatically when the inquiry contains personal information | explicit rule |
| classify candidates such as refund, delivery, and exchange | model using learned representations |
| send low-score or sensitive cases to a person | combination of rules and model score |
| collect repeated failure cases and strengthen the dataset | operational review and retraining |

So the important question is not `rules or model?` A better question is the following.

> Which part must be explicitly controlled by people?  
> Which part can be left to the model to learn representation from data?  
> Which judgments should remain with human review?

## Cases and Examples

### Case 1. An Inquiry Box Where the Intention Is Similar but the Sentences Keep Changing

Imagine that customers contact support because they want to change the delivery destination. One person writes `I want to change the address`, another writes `it should be delivered to the office`, and another says `I entered the recipient number incorrectly`.

A rule-based approach keeps increasing the list of words and combinations such as `address`, `modify`, `change`, `recipient`, `phone number`, and `to the office` in order to catch all these expressions. That approach is easy for people to read and revise, but gaps appear as soon as the expression changes slightly, and once negation or condition clauses are attached, rule priority becomes complicated.

Representation learning treats the problem more broadly than a word list. If different sentences can be grouped into internal representations that are close to `delivery-information change`, then even without the exact same keyword the model can place similar intentions near one another. The tradeoff is that the internal criterion is not directly readable like a rule table.

This case reveals the key distinction of 3.3. Rules are criteria written outside by people, while representations are internal forms computed inside the model. Real systems often do not choose only one. Instead, they divide the roles so that policies stay fixed as rules while bundles of varied expression are handled by the model.

## Checklist

- I can explain the difference between rule-based approaches and representation learning.
- I can explain that both features and representations are concepts for turning input into a form that is easier for the model to use.
- I can distinguish between human-designed features and model-learned representations.
- I can explain that learned representations are powerful but can be difficult to interpret.
- I can read rules and models not only as competitors, but as a division of responsibility.
- I can explain that explicit rules are human-readable criteria and strong for explanation and control, but become harder to maintain as exceptions and expression diversity grow.
- I can explain that learned representations are computable internal forms created by the model, strong for handling complex patterns and similarity, but not a rule list people can read directly.

## Sources and Further Reading

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, arXiv, 2012-06-24, accessed 2026-06-22.
- George A. Miller, [The Magical Number Seven, Plus or Minus Two: Some Limits on our Capacity for Processing Information](http://psychclassics.yorku.ca/Miller/){: target="_blank" rel="noopener noreferrer" }, Psychological Review, 1956, accessed 2026-06-22.
