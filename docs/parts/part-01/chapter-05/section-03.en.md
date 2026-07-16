# P1-5.3 Distinguishing Inference-Related Terms

> Section ID: `P1-5.3`
> Version: `v2026.07.16`

Section 5.2 explained `inference` as the execution that applies a trained model to a new input and produces output. But when we read real AI documents, this one word often overlaps with different translations, everyday expressions, and neighboring concepts across languages.

This confusion is not a special problem of one language. In any language, if one translated term covers several English conceptual roles at once, readers can see the same expression and fail to separate model execution, thought process, output value, statistical procedure, and generation. So this section focuses first on how to separate different conceptual roles, before any one translation habit.

The five expressions we want to separate here are:

> inference  
> reasoning  
> prediction  
> statistical inference  
> generation

The goal of this section is not to define these terms completely in a philosophical sense. The goal is to build a reading standard that lets us ask first, `Is this sentence talking about model execution, a thought process, or an output value?`

## Scope of This Section

This section does not cover all of `inference` in logic, statistics, or cognitive science. It is also not the section that judges whether an LLM really thinks like a human.

It only covers the minimum distinctions needed when an introductory reader reads AI documents:

> `inference` meaning model execution  
> `reasoning` meaning a logical thought process  
> `prediction` meaning a model's output value  
> `statistical inference` meaning the statistical treatment of estimation and testing  
> `generation` meaning the creation of text or images

## Goal of This Section

- Distinguish the central meanings of `inference`, `reasoning`, `prediction`, `statistical inference`, and `generation`.
- Set a reading standard that does not depend only on one language's translation.
- Set the notation policy used in this book.
- Understand that an LLM response can look like reasoning, but that appearance does not automatically guarantee a correct thought process.

## Three Standards

The goal here is not to organize the terms as strict philosophical categories, but to make AI documents less confusing to read. We first separate the three points below.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| `inference` is usually closer to `running the model` | This separates it from the human-thinking image suggested by everyday translation. | Understand it as the process of giving input and producing output. |
| `prediction` is the output value, while `inference` is the process that creates that output | This keeps process and result separate when reading. | Understand the relation `inference -> prediction`. |
| `reasoning`, `statistical inference`, and `generation` belong to different contexts | This prevents LLM discussion, statistics discussion, and general AI discussion from collapsing into one word. | Even when translations look similar, split them again by original term and context. |

At first, all five expressions can sound like vague versions of `making a result`. So we first keep only the positional distinction below.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| inference | execution that applies a trained model to a new input | the process by which the model produces output |
| reasoning | a thought process that reaches a conclusion by following grounds | a term for logical explanation or thought steps |
| prediction | the output value produced by the model | the result-side expression rather than the process |
| statistical inference | a statistical procedure that works with populations, uncertainty, and hypotheses from samples | the statistical context that must be separated from deployment-time model inference |
| generation | creating outputs such as text, image, or audio | the expression for result creation in generative AI |

Here we keep the positional rule that `inference is execution`, `prediction is result`, `reasoning is a thought process`, `statistical inference is statistical context`, and `generation is result creation`.

## Why Does Confusion Happen?

The core reason for confusion is that a single translated word can easily cover several conceptual positions at once. When an everyday expression strongly suggests drawing a conclusion from clues or evidence, using it for `inference` can make readers interpret AI `inference` as something close to a human thought process.

For example, a person may say the following:

> The sky is dark and the wind is strong.  
> So I inferred that it would rain soon.

This sentence contains clues, background knowledge, judgment, and conclusion together. So if readers begin with the translated word first, they can easily read AI `inference` as something close to a human thought process.

But in machine-learning contexts, `inference` usually has a narrower and more execution-centered meaning.

> trained model + new input -> output

Google's Machine Learning Glossary explains inference in traditional machine learning as the process of applying a trained model to unlabeled examples to make predictions. For LLMs, it explains inference as the process of using a trained model to generate a response to an input prompt. The center of that explanation is not `thinking like a human`, but `applying a trained model`.

So the core issue is not any particular language alone. It is a general reading problem that appears when a translated word is read before its conceptual role. In any language, if one local expression covers several standard English terms at once, readers may see the same word and fail to separate `model execution`, `output value`, `thought process`, `statistical procedure`, and `generation act`. A local term that evokes several meanings at once is only an example; the standard itself is the conceptual role.

Therefore, in multilingual writing, we first ask `what role does this sentence describe?` before asking `which local word should translate it?` The local translation may differ by language, but the role distinction should remain stable.

| Expression | First question to ask | How it differs |
| --- | --- | --- |
| `inference` | Is a trained model being applied to a new input? | It is a process, close to model execution or model application. |
| `prediction` | What output value did the model produce? | It is a result, the output produced by inference. |
| `reasoning` | Is the text describing a thought process that follows grounds toward a conclusion? | It belongs to explanation or logical development, not model execution itself. |
| `statistical inference` | Is the text using samples to reason about populations, uncertainty, or hypotheses? | It is a statistical context, different from running a deployed model. |
| `generation` | Is the system producing an artifact such as text, image, or audio? | It focuses on producing a generated result. |

## Separating the Terms

The table below gives the preferred distinctions used in this book.

| English expression | Preferred wording in this book | Central meaning | Simple example |
| --- | --- | --- | --- |
| `inference` | inference, model execution, model application | the process that applies a trained model to new input and produces output | put in a support sentence and get the label `delivery` |
| `reasoning` | reasoning, logical reasoning, thought process | the process of reaching a conclusion through grounds and relations | explain a conclusion by checking rules, conditions, and cases |
| `prediction` | prediction, model output | the output value produced by the model | `delivery`, `0.72`, estimated price `32,000 won` |
| `statistical inference` | statistical inference | working with populations, uncertainty, and hypotheses from sample data | confidence intervals, hypothesis tests |
| `generation` | generation | producing results such as text, images, or audio | generate a draft reply |

The most important relation in this table is the relation between `inference` and `prediction`. Google's glossary describes `prediction` as the output of a model. In traditional machine learning, `inference` can therefore be read as the process that produces a `prediction`.

> inference = the execution process that creates a prediction  
> prediction = the output produced by that execution

The explanation of `predict` in scikit-learn is also helpful here. It says that `predict` creates a prediction for each sample and returns values in the target space used during training. In other words, `predict` can be read as a usage-stage API that produces outputs for new input after the model has already been trained.

## Comparing Them on the Same Example

Let us return to the example of automatic handling for customer-support messages.

> input:  
> `I ordered yesterday, but tracking still does not work.`

In a situation that processes this sentence, the terms separate as follows.

| Distinction | Explanation | Example result |
| --- | --- | --- |
| inference | apply the trained support-message classifier to the input sentence | compute a label and a score |
| prediction | the output produced by the model | `delivery`, `0.72` |
| reasoning | explain why the message should be seen as a delivery inquiry | `The words order, tracking, and not yet connect to the intent of checking delivery status.` |
| generation | generate a user-facing reply sentence | `We are sorry for the delay in tracking updates...` |
| statistical inference | evaluate uncertainty in model performance using validation data | accuracy estimate, confidence-interval review |

In this example, `inference` does not necessarily include `reasoning`. Even a simple classifier can perform inference. By contrast, `reasoning` may be a human explanation added after the model output, or a text explanation generated by an LLM.

Put even more simply, a `prediction` is closer to a single result fragment like `delivery` or `0.72`, while `reasoning` and `generation` are closer to longer text that explains the result or presents it to a user. So when an explanation sentence appears, we should not immediately read that sentence itself as identical to `prediction` or `inference`.

## Why Is It More Confusing with LLMs?

LLMs respond in natural language. So an inference result can look like human `reasoning`.

For example, an LLM may answer like this:

> First, the message includes delivery tracking.  
> Second, it says the tracking has not updated after the order.  
> Therefore, this message can be classified as a delivery inquiry.

This looks like reasoning. But from the model's point of view, the sentence itself is also output generated during inference. A step-by-step appearance does not guarantee that a correct grounding process really took place.

So this book uses the following conservative wording:

> LLM inference can generate text that looks like reasoning.  
> But the generated explanation must be reviewed separately.

This point is especially important in generative-AI writing. A generated reply can look natural, but factuality, evidence, and logical connection are not automatically guaranteed.

## It Is Also Different from Statistical Inference

`Statistical inference` is also translated using the word family of `inference`, but it is not the same thing as `inference` in the machine-learning deployment context.

Google's glossary also distinguishes inference in statistics as having a somewhat different meaning. Here we do not define statistical inference in detail. We only confirm that it should not be read as the same thing as machine-learning deployment-time inference.

By contrast, the machine-learning inference discussed in 5.2 and 5.3 is closer to the following:

> use a trained model to produce output for a new input

Machine learning is deeply connected to statistics. Even so, it is safer here not to use the two expressions as though they were interchangeable.

## Notation Policy in This Book

From this point on, the book follows the policies below.

| Situation | Notation policy |
| --- | --- |
| when the meaning is to run a trained model | at first, write `inference (model execution)` or `inference (model application)` together |
| when short wording is needed in local-language prose | avoid using only the local translation by itself; prefer wording that exposes the role, such as `model inference`, `model execution`, or `inference` |
| when referring to a logical thought process | write `reasoning (logical reasoning)` or equivalent wording together |
| when referring to the model's result value | distinguish it as `prediction (model output)` |
| when referring to the statistical meaning | write `statistical inference` together |
| when referring to result creation in generative AI | distinguish it as `generation` |

The point is not to erase local translation. Even when a translation exists, we should first make clear which conceptual position the word points to.

In any language edition, if we use only the local translation for `inference`, the following meanings can easily blur together:

> Is it model execution?  
> Is it logical reasoning?  
> Is it a prediction value?  
> Is it statistical inference?  
> Is it a generative process?

That is why the early part of this book keeps the English expression alongside the local wording. The English term is not decoration. It is a safety device that keeps different language editions and outside materials on the same conceptual axis.

The important habit here is not memorizing every English word, but refusing to decide the meaning only from the translated term. If we ask once more, `Is this sentence talking about model execution, a thought process, or an output value?`, then terminology collisions become much easier to avoid.

## Checklist

- I can explain `inference` as `model execution` or `model application`.
- I can explain why `inference` and `reasoning` should not be treated as the same thing.
- I can explain that `prediction` is not the process, but the model's output.
- I can explain that `statistical inference` is different from inference in the machine-learning deployment context.
- I can explain that an LLM can generate text that looks like reasoning, but that explanation must still be reviewed separately.
- I can explain why this book keeps the English term visible.
- I can explain that `inference` may be translated locally, but this book reads the conceptual position before the translation.
- I can explain the distinction that `inference` is model execution, `prediction` is result, `reasoning` is thought process, `generation` is generation, and `statistical inference` is statistical context.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
