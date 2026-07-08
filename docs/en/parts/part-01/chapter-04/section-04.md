# P1-4.4 How Problem Definition Determines the Model

> Section ID: `P1-4.4`
> Version: `v2026.07.07`

Section 4.1 treated a model as a computational representation reduced for a purpose. Section 4.2 organized input, output, and data. Section 4.3 showed that inputs are turned into features and representations and computed together with internal parameters.

This section ties that flow together with one question: how do we define a real-world goal as an AI task?

Problem definition can look like planning work done before model building. In reality, it determines the kind of model, the data that must be collected, the evaluation criteria, and the way the output connects to work.

## Scope of This Section

This section is not about the detailed formulas of evaluation metrics such as accuracy, precision, recall, or loss functions. Those are handled later in Part 4.

It is also not about full AI service architecture. Routing, permission checks, human review, tool use, and post-deployment monitoring are revisited in P1-14 and Part 7.

The focus here is one earlier step: deciding what real-world goal becomes what input-output task, and deciding what counts as doing well.

## Goal of This Section

- Distinguish a real-world goal from a modeling task.
- Understand that the same real-world goal can be split into several different AI tasks.
- See that once the output definition changes, the data, model, and evaluation criteria also change together.
- Understand that model performance and business performance are not always the same.
- Summarize what it means to turn a problem into a model.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a real-world goal and a modeling task are not the same | This prevents us from exaggerating the range of what AI solves. | Distinguish `improve customer satisfaction` from `classify support messages`. |
| the same goal can become several different output definitions | This shows how classification, score prediction, and generation split apart. | Fix the idea that we must decide what output the model should produce. |
| the output definition changes the data and evaluation criteria together | This shows why problem design matters before model choice. | Understand that changing the output also changes the needed examples and the meaning of success. |

## A Real-World Goal Is Not Yet a Modeling Task

`We want to handle customer-support messages better` is a real-world goal. But this sentence alone does not yet tell us what task to give the model.

To become a modeling task, it needs a more specific form.

| Real-world goal | Expression after turning it into a modeling task |
| --- | --- |
| we want to handle customer-support messages better | classify the message type from the support sentence |
| we want to reduce delivery problems | predict the probability of delivery delay from order information |
| we want to reduce repetitive support work | generate a draft reply from the message and policy |
| we want to reduce risky transactions | output a risk score from transaction information |

Google’s Machine Learning Glossary describes a `task` as a problem that can be solved with machine-learning methods, giving examples such as classification, regression, clustering, and anomaly detection.

So problem definition means turning a real-world goal into a task form like that.

> real-world goal -> modeling task -> input / output / data / evaluation

## The Same Goal Can Become Several Different Tasks

Even the same goal, `help with customer-support messages`, can become different problems depending on what we ask the model to produce.

| Task given to the model | Output | Task character |
| --- | --- | --- |
| choose a message type | `refund`, `delivery`, `exchange`, `other` | classification |
| predict urgency | score from 1 to 5 | regression or score prediction |
| recommend the responsible team | logistics, payments, support | classification or recommendation |
| write a draft reply | natural-language sentence | generation |
| decide whether human review is needed | yes/no | binary classification |

The Google glossary distinguishes classification models, which predict classes, from regression models, which predict numeric values. That distinction is important because the model learns different kinds of relations depending on whether the output is a category, number, or sentence.

Suppose the same input sentence is:

> I ordered yesterday, but tracking still does not work.

| Output definition | Possible output | Required data |
| --- | --- | --- |
| message-type classification | delivery | message sentence plus message-type labels |
| urgency prediction | 2 | message sentence plus urgency scores |
| draft-reply generation | `Tracking updates can take some time...` | message, order state, policy, and examples of good replies |
| human-review decision | no | message plus labels saying whether automation was safe |

So before asking `Which model should we use?`, we first need to ask `What exactly should it output?`

## The Output Definition Changes Evaluation Metrics

Once we decide what the model should output, we also need to decide what counts as doing well.

Google’s glossary describes evaluation as the process of measuring model quality or comparing models, and a metric as a statistic we care about. The scikit-learn model-evaluation guide also explains that evaluation should begin from the final goal and the context in which predictions are used.

In the support-message example, the evaluation standard changes with the output definition.

| Output definition | Evaluation criteria we may look at |
| --- | --- |
| message-type classification | accuracy, precision, recall, confusion matrix |
| urgency score | difference between true urgency and predicted score |
| draft-reply generation | factuality, policy compliance, tone, safety, human-review result |
| human-review decision | how well the model catches cases that must not be missed |

Choosing a metric is also choosing which mistakes are more dangerous.

| Mistake | Business effect |
| --- | --- |
| a risky message is handled automatically | possible customer harm, policy violation, security risk |
| a safe message is sent to human review | higher cost and slower response |

So problem definition includes not only the output, but also the cost of mistakes.

## Problem Definition Also Determines What Data Must Be Collected

Problem definition determines what data should be gathered. Even large amounts of data may be unhelpful if they do not match the task the model is meant to solve.

Let us split the broad goal `reduce delivery problems` into three tasks.

| Task | Required input data | Required output data |
| --- | --- | --- |
| delivery-delay prediction | order time, shipment time, region, product, delivery status | delay flag or expected arrival time |
| delivery-message classification | customer-support sentence | message-type label |
| delivery-reply generation | message sentence, order state, delivery policy | good reply examples or reply rules |

The same delivery problem creates completely different data shapes depending on the task.

## Model Choice Comes After Problem Definition

At this stage, names like linear model, tree model, neural network, or LLM can draw attention first. But if the model name comes first, people often force the problem to fit the model.

The safer order is this.

1. define the real-world goal
2. define the modeling task
3. define the input and output
4. define the data and labeling standard
5. define the evaluation criteria
6. choose model candidates
7. check where the output will be used

For example, a customer-support classification problem does not automatically require an LLM. If message types are clear and the data is well organized, a simpler classifier or a mix of rules and model signals may be enough. On the other hand, if the output must be a natural-language draft reply, a generative model or LLM may be worth considering.

Model choice matters, but it cannot replace problem definition.

## Model Performance and Business Performance Can Be Different

Even if model metrics improve, that does not guarantee that real work improved. A model is only one part of a larger system.

| The model may do well, but... | A problem may still appear in the business flow |
| --- | --- |
| it classifies message types correctly | routing rules may still send the case to the wrong team |
| it predicts whether automation is possible | policy changes may not be reflected, leading to wrong guidance |
| it generates fluent draft replies | the draft may still be rejected in review for unsupported content |
| it predicts delay risk well | alerts may still be sent too late to improve customer experience |

So we must distinguish model evaluation from business evaluation.

| Distinction | Question |
| --- | --- |
| model evaluation | how well does the output match the target or criterion? |
| business evaluation | did real-world work improve after the model was added? |
| safety evaluation | can a bad output create risk for users or the organization? |

## What Should Be Written in a Problem-Definition Note

Even for a small modeling task, confusion decreases if the following are written down.

| Item | Question | Example for support messages |
| --- | --- | --- |
| real-world goal | why is this model needed? | reduce message-handling time |
| modeling task | what problem does the model solve? | message-type classification |
| input | what does the model actually see? | message sentence |
| output | what must the model produce? | `refund`, `delivery`, `exchange`, `other` |
| data | what are the past examples? | message sentences with human labels |
| labeling standard | can people label cases by the same criteria? | definition of refund, delivery, exchange, other |
| evaluation metric | what counts as doing well? | accuracy, recall, human-review result |
| cost of mistakes | which mistakes are more dangerous? | automatically handling a risky message |
| usage point | where will the output be used? | routing, auto-reply support, human review |
| excluded scope | what does the model not do? | final approval of refund or policy responsibility |

This is not a grand planning document. It is the minimum map that defines the world the model is meant to handle.

## What to Remember from This Section

Problem definition is not just preparation before the model. It is the stage that decides what the model will see, what it will output, and how success will be judged.

The flow of Chapter 4 can be summarized like this.

1. A real-world problem becomes a model when we reduce it for a purpose.
2. A model takes input and produces output.
3. Input is turned into features and representations for computation.
4. Problem definition sets the standard for all those choices.

Before choosing a model, we should be able to complete this sentence:

> We want to use [what input] to produce [what output],  
> and we want to check whether that output helps [what business goal]  
> by using [what metrics and review criteria].

If we cannot complete that sentence, the issue is probably not yet a model problem, but a real-world goal that still needs to be clarified.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
