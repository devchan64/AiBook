# P1-4.4 How Problem Definition Determines the Model

> Section ID: `P1-4.4`
> Version: `v2026.07.12`

Section 4.1 treated a model as a computational representation reduced for a purpose. Section 4.2 organized input, output, and data. Section 4.3 showed that input is transformed into features and representations and then computed together with internal parameters.

This section ties that flow into one question: how should a real-world goal be defined as an AI problem?

Problem definition can look like documentation work that happens before model building. In reality, it determines the model type, the data that must be collected, the evaluation criteria, and the way the result connects to business workflow. If problem definition is unstable, the result can miss the target even when a strong algorithm is used.

In Part 1, this section fixes the baseline for `task definition` and the way a real-world goal is turned into a modeling task. The basic meanings of `model`, `input/output/data`, and `features/representations/parameters` were prepared first in 4.1 through 4.3. Here the focus shifts to deciding what task those elements should be grouped into and what should count as doing well.

## Scope of This Section

Section 4.4 is not a section for calculating detailed model metrics. The detailed formulas of accuracy, precision, recall, and loss functions are handled in Part 4.

Section 4.4 is also not a section for designing a full AI service architecture. Routing, permission checks, human review, tool use, and post-deployment monitoring are handled in P1-14 and Part 7.

This section only covers the step before that: defining which real-world goal becomes which input-output problem, and deciding what should count as doing well.

## Goal of This Section

- Distinguish a real-world goal from a modeling task.
- Understand that the same real-world goal can split into several different AI problems.
- See that the output definition changes the data, the model, and the evaluation criteria together.
- Understand that model performance and business performance are not always the same.
- Summarize what it means to turn a problem into a model at the end of Chapter 4.

## Three Standards

Before choosing a good algorithm, we should first separate the three ideas below.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a real-world goal and a modeling task are not the same | This prevents us from exaggerating the scope of what AI solves. | Distinguish `improve customer satisfaction` from `classify support messages` as different levels. |
| the same goal can become several output definitions | This shows how classification, score prediction, and generation split apart. | Fix the point that we must decide what the model should output. |
| the output definition changes the data and evaluation criteria together | This shows that problem design matters before model choice. | Understand that when output changes, the needed examples and the standard of success change together. |

`real-world goal`, `modeling task`, `output definition`, `evaluation`, and `business performance` are connected, but they are not the same thing.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| real-world goal | the outside problem we actually want to improve | the starting point that explains why the model is needed |
| modeling task | the narrowed computational problem given to the model | a form such as classification, score prediction, or generation |
| output definition | the format of the result the model must produce | the baseline that determines what data to collect and what metrics to watch |
| evaluation | the standard used to check how correct the model output is | a judging frame such as accuracy, recall, or score error |
| business performance | whether real work improved after the model was inserted | outside effects such as speed, cost, safety, and customer experience |

The important positional distinction here is this: `the real-world goal is the outside problem`, `the modeling task is the narrowed computational problem`, `the output definition is what we ask the model to produce`, `evaluation checks the model`, and `business performance is the real result`.

## A Real-World Goal Is Not Yet a Modeling Task

`We want to handle customer-support messages better` is a real-world goal. But that sentence alone does not yet tell us what we should ask a model to do.

To become a modeling task, it needs a more specific form.

| Real-world goal | Expression after turning it into a modeling task |
| --- | --- |
| we want to handle customer-support messages better | classify the message type from the support sentence |
| we want to reduce delivery problems | predict delivery-delay risk from order information |
| we want to reduce repetitive support work | generate a draft reply from the message and policy |
| we want to reduce risky transactions | output a risk score from transaction information |

Google's Machine Learning Glossary explains `task` as a problem that can be solved with machine-learning methods, and gives examples such as classification, regression, clustering, and anomaly detection.

So problem definition is the work of changing a real-world goal into a task form like that.

> real-world goal -> modeling task -> input / output / data / evaluation

This order is not just a planning sentence. It is a baseline that keeps later model candidates and data-collection scope from drifting. The core point here is to understand clearly that `a real-world problem is not put directly into a model`; there is an intermediate task-definition step in between.

## The Same Goal Can Become Several Tasks

Even the same goal, `help with customer-support messages`, becomes a different problem depending on what we ask the model to produce.

| What we ask the model to do | Output | Character of the task |
| --- | --- | --- |
| choose a message type | `refund`, `delivery`, `exchange`, `other` | classification |
| predict urgency | score from 1 to 5 | regression or score prediction |
| recommend the responsible team | logistics, payments, support | classification or recommendation |
| write a draft reply | natural-language sentence | generation |
| decide whether human review is needed | yes/no | binary classification |

Google's Machine Learning Glossary explains a classification model as a model that predicts classes, and a regression model as a model that predicts numeric values. That distinction is very important at the introductory level. When the output is a category, a number, or a sentence, the model must learn a different kind of relation.

For example, even with the same support sentence, the problem changes completely when the output definition changes.

> `I ordered yesterday, but tracking still does not work.`

| Output definition | Possible output | Required data |
| --- | --- | --- |
| message-type classification | delivery | message sentence and message-type labels |
| urgency prediction | 2 | message sentence and urgency scores |
| draft-reply generation | `Tracking updates may take some time...` | message, order state, policy, and examples of good replies |
| human-review decision | no | the message and labels indicating whether automatic handling is safe |

Even when the input sentence is the same, changing the output changes both the needed data and the evaluation style. So before asking `Which model should we use?`, we have to ask `What should the model output?`

In practice, different teams often imagine different outputs first, even with the same goal. An operations team may think, `let's attach message types automatically`. A manager may think, `let's surface urgent cases first`. A writing-support team may think, `let's generate draft replies`. All three begin from the same goal of `handling messages better`, but the real modeling tasks split into classification, score prediction, and generation. That split is not a problem. The role of problem definition is to fix that difference clearly in writing.

## The Output Definition Changes the Evaluation Metrics

Once we decide what the model should output, we then need to decide what should count as doing well.

Google's Machine Learning Glossary explains evaluation as the process of measuring model quality or comparing different models. It also explains a metric as a statistic we care about.

The scikit-learn model-evaluation guide explains that evaluation functions should be chosen by starting from the final goal and the context in which predictions are used. It also distinguishes `prediction` from the `decision making` that uses that prediction. Section 4.4 adopts this perspective and connects metrics not only to model output, but also to where that output is used.

In the support-message example, the evaluation criteria change with the output definition.

| Output definition | Possible evaluation criteria |
| --- | --- |
| message-type classification | accuracy, precision, recall, confusion matrix |
| urgency score | the gap between the true urgency and the predicted score |
| draft-reply generation | factuality, policy compliance, tone, safety, human-review result |
| human-review decision | how well the model catches the cases that must not be missed |

The important point here is that an evaluation metric means more than a number. Choosing a metric is also deciding `which mistakes should be treated as more dangerous`.

For example, sending a message that needs human review into automatic handling can be dangerous. By contrast, sending a message that could have been automated to a human may mainly increase cost. Both are wrong predictions, but their business effects are different.

| Mistake | Business effect |
| --- | --- |
| a risky message is handled automatically | possible customer harm, policy violation, or security problems |
| a safe message is sent to a human | higher processing cost and slower response |

So problem definition must include not only the output itself, but also the cost of mistakes.

## Problem Definition Also Determines the Scope of Data Collection

Problem definition also determines what data needs to be collected. Even if there is a lot of data, it may not be useful when it does not match the task the model is supposed to solve.

For example, let us rewrite the goal `we want to reduce delivery problems` into three different tasks.

| Task | Required input data | Required output data |
| --- | --- | --- |
| delivery-delay prediction | order time, shipment time, region, product, delivery status | delay flag or expected arrival time |
| delivery-message classification | customer-support sentence | message-type label |
| delivery-reply generation | message sentence, order state, delivery policy | examples of good replies or reply criteria |

Even with the same delivery problem, the shape of the data changes completely. Collecting only message-classification data makes it hard to build a delivery-delay prediction model. By contrast, having many order logs does not directly teach reply quality for customer messages.

So before collecting data, we need these questions:

> What output are we trying to predict or generate?  
> What input can the model actually see to produce that output?  
> Do we have past cases where that input and output appear together?  
> Is the labeling standard consistent across people?

## Model Choice Comes After Problem Definition

At this point, model names can easily grab attention first. Linear model, tree model, neural network, and LLM all sound familiar. But when the model name comes first, the problem is often forced to fit the model.

The safer order is the following:

1. define the real-world goal
2. define the modeling task
3. define the input and output
4. define the data and labeling standard
5. define the evaluation criteria
6. choose model candidates
7. confirm where the output will be used

For example, in a support-message classification problem, we do not need to decide from the start that we must use an LLM. If message types are clear and the data is well organized, a simpler classifier or a mix of rules and model signals may be enough. By contrast, if the task is to generate a natural-language draft reply, then a generative model or an LLM becomes worth considering.

Model choice matters, but it cannot replace problem definition. If problem definition is unclear, even a large model makes it hard to judge what it should do well.

## Model Performance and Business Performance Can Be Different

Even when model metrics improve, we cannot automatically conclude that real business performance improved. A model is only one part inside a larger system.

For example, suppose message-type classification accuracy became higher. Even then, the following problems may remain:

| The model did well, but... | A problem may still appear in real work |
| --- | --- |
| it classifies message types correctly | routing rules still send the case to the wrong team |
| it predicts whether automatic handling is possible well | a policy change was not reflected, so guidance is wrong |
| it generates a fluent draft reply | the draft is rejected in review because it contains unsupported content |
| it predicts delay risk well | alerts are sent too late, so customer experience does not improve |

Google's Machine Learning Glossary notes that LLM evaluation helps not only with performance comparison, but also with checking safe and ethical use. That topic is developed later in the generative-AI part. In Section 4.4, it is enough to remember that `when the output changes, the evaluation criteria also change`.

So we must separate model evaluation from business evaluation.

| Distinction | Question |
| --- | --- |
| model evaluation | how well does the output match the answer or criterion? |
| business evaluation | did real work improve after the model was inserted? |
| safety evaluation | can bad output create risk for users or the organization? |

The two evaluations can move differently even for the same model. For example, message-type classification accuracy may be high, but business performance may still improve only a little if the routing rules are outdated or the responsible team receives the result too late. On the other hand, even if model accuracy is not extremely high, actual business safety may improve if the system is good at catching risky messages and sending them to human review.

## What Should Be Written in a Problem-Definition Document

Even for a small modeling task, confusion decreases if the following items are written down.

| Item | Question | Example for support messages |
| --- | --- | --- |
| real-world goal | why is this model needed? | reduce message-handling time |
| modeling task | what problem does the model solve? | message-type classification |
| input | what does the model actually see? | message sentence |
| output | what must the model produce? | `refund`, `delivery`, `exchange`, `other` |
| data | what are the past cases? | message sentences and labels attached by people |
| labeling standard | can people apply the same standard? | the definitions of refund, delivery, exchange, and other |
| evaluation metric | what should count as doing well? | accuracy, recall, human-review result |
| cost of mistakes | which mistakes are more dangerous? | automatically handling a risky message |
| usage point | where will the output be used? | routing, auto-reply support, input to human review |
| excluded scope | what does the model not do? | final refund approval and final policy responsibility |

This kind of document is not a large planning document. It is the minimum map that defines the world the model is supposed to handle. Without this map, it becomes hard to judge whether the model improved or whether the data is sufficient. Whether deployment is actually possible still requires later chapters, because security, permissions, review flow, and operational responsibility must also be checked together.

## Checklist

- I can distinguish a real-world goal from a modeling task.
- I can explain that the same goal can become different tasks such as classification, regression, recommendation, or generation.
- I can explain that the output definition changes the data, the model candidates, and the evaluation criteria together.
- I can explain that model performance and real business performance can differ.
- I can write the input, output, data, labeling standard, evaluation criteria, cost of mistakes, and excluded scope into a problem-definition note.
- I can explain that problem definition is the central stage that determines what the model sees, what it produces, and how success is judged.
- I can restate a problem in the order `real-world goal -> modeling task -> input/output/data -> evaluation -> business performance`.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
