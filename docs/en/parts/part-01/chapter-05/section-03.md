# P1-5.3 Distinguishing Inference-Related Terms

> Section ID: `P1-5.3`
> Version: `v2026.07.08`

Section 5.2 explained `inference` as the execution that applies a trained model to a new input and produces output. But when people read actual AI texts, this one word often overlaps with different translations, everyday expressions, and neighboring concepts across languages.

In Korean, that overlap becomes especially visible because the usual translation also suggests a human thought process. If this section is framed only as a Korean-language problem, however, the core standard becomes weaker in English and in future translations. So the real focus here is not one language-specific habit, but how to separate different conceptual roles before translation choices blur them.

The expressions that need separation are these:

> inference  
> reasoning  
> prediction  
> statistical inference  
> generation

The execution perspective of `inference` was fixed first in 5.2. Here the focus is narrower: when nearby terms collide, how should we separate them again? The goal is not to give a perfect philosophical definition of each word. It is to set a reading standard for the rest of the manuscript.

## Scope of This Section

This section does not cover all of inference in logic, statistics, or cognitive science. It is also not the place to decide whether an LLM really thinks like a person.

It only fixes the minimum distinctions needed for an introductory reader of AI texts:

> inference as model execution  
> reasoning as a logical thought process  
> prediction as model output  
> statistical inference as the statistical treatment of estimation and testing  
> generation as the creation of text or images

## Goal of This Section

- Distinguish the central meanings of `inference`, `reasoning`, `prediction`, `statistical inference`, and `generation`.
- Set a reading standard that does not depend on one language's translation habit.
- Set the notation policy used in this book.
- Understand that an LLM response may look like reasoning, but that does not guarantee a valid thought process.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| inference is usually closer to `running the model` | This separates it from the human-thinking image that some translations suggest. | Understand it as the process of putting in input and producing output. |
| prediction is the output value, while inference is the process that produces it | This keeps process and result separate. | Understand the relation `inference -> prediction`. |
| reasoning, statistical inference, and generation belong to different contexts | This prevents LLM discussion, statistics discussion, and general AI discussion from collapsing into one word. | Even if translations look similar, separate them again by original term and context. |

The five expressions may all sound vaguely like `making a result`, so a short role split is useful:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| inference | execution that applies a trained model to new input | the process that produces output |
| reasoning | thought process that follows grounds to a conclusion | a term for logical explanation or thinking steps |
| prediction | output produced by the model | a result-side expression rather than a process |
| statistical inference | statistical procedure that draws conclusions about populations or uncertainty from samples | a statistical context that should not be mixed with deployment-time model inference |
| generation | creating outputs such as text, image, or audio | the result-making expression used in generative AI |

## Why Does the Confusion Happen?

The core problem is that one translated word can end up covering several conceptual roles at once. Korean is a clear example because the usual word for `inference` often suggests drawing a conclusion from clues or evidence. Here we do not need a dictionary definition. What matters is the reading confusion this creates in AI texts.

A person might say:

> The sky is dark and the wind is strong.  
> So I inferred that it will rain soon.

That sentence combines clues, background knowledge, judgment, and conclusion. So when readers start from that translation, they may naturally imagine `thinking and reaching a conclusion`.

AI `inference` touches that feeling only in a very broad sense. In machine-learning writing, `inference` is usually narrower and more execution-focused:

> trained model + new input -> output

Google’s glossary explains inference in traditional machine learning as applying a trained model to unlabeled examples to make predictions, and in LLMs as using a trained model to generate a response to a prompt. The center of that explanation is not `thinking like a person`, but `applying a trained model`.

So the issue is broader than Korean alone. Korean simply makes the overlap easy to see. The safer reading rule is to ask which conceptual role the sentence is pointing to before trusting the local translation.

## Separating the Terms

The table below gives the preferred distinction used in this book.

| English expression | Preferred expression here | Central meaning | Simple example |
| --- | --- | --- | --- |
| `inference` | inference, model execution, model application | the process of applying a trained model to new input and producing output | put in a message sentence and get the label `delivery` |
| `reasoning` | reasoning, logical reasoning, thought process | a process that follows grounds and relations toward a conclusion | explain a conclusion by checking rules, conditions, and cases |
| `prediction` | prediction, model output | the output value produced by the model | `delivery`, 0.72, estimated price 32,000 won |
| `statistical inference` | statistical inference | working with populations, uncertainty, and hypotheses from sample data | confidence intervals, hypothesis tests |
| `generation` | generation | producing outputs such as text, images, or audio | generate a reply draft |

The important relation here is between `inference` and `prediction`.

> inference = the execution process that creates a prediction  
> prediction = the output produced by that execution

The scikit-learn explanation of `predict` also helps here. It describes `predict` as creating predictions for each sample and returning values in the target space used during training. In other words, `predict` belongs to the usage stage after the model has already been learned.

## Comparing Them on the Same Example

Take the support-message example again:

> input:  
> `I ordered yesterday, but tracking still does not work.`

In that situation, the words separate like this:

| Distinction | Explanation | Example result |
| --- | --- | --- |
| inference | the trained classifier is applied to the sentence | label and score are computed |
| prediction | the output produced by the model | `delivery`, 0.72 |
| reasoning | an explanation of why it should be treated as a delivery message | `the sentence mentions an order, tracking, and not yet working, which connects to delivery-status checking` |
| generation | a user-facing sentence is produced | `We are sorry for the delay in tracking updates...` |
| statistical inference | uncertainty in model performance is evaluated on validation data | accuracy estimate, confidence-interval review |

Inference does not necessarily include reasoning. A simple classifier can perform inference without generating an explicit explanation. Conversely, reasoning may be something a human adds after the model output, or a text explanation generated by an LLM.

## Why Is It More Confusing with LLMs?

LLMs answer in natural language, so their inference output can look like human reasoning.

For example, an LLM may answer like this:

> First, the message mentions delivery tracking.  
> Second, it says the tracking has not updated after the order.  
> Therefore, this message can be classified as a delivery inquiry.

This looks like reasoning. But from the model’s point of view, that sentence is itself output generated during inference. A step-by-step appearance does not guarantee that a sound reasoning process actually happened.

So this book keeps the wording conservative:

> LLM inference can generate text that looks like reasoning.  
> But the generated explanation must still be reviewed separately.

That point becomes especially important in generative-AI writing, because fluent output does not automatically guarantee factuality, valid grounds, or coherent logic.

## It Is Also Different from Statistical Inference

`Statistical inference` is also translated with the same Korean word family, but it is not the same thing as deployment-time machine-learning inference.

Google’s glossary also notes that inference has a somewhat different meaning in statistics. Here we do not need the full statistical definition. We only need the boundary:

> statistical inference is not the same thing as running a trained model on a new input

By contrast, the machine-learning inference discussed in 5.2 and 5.3 is closer to this:

> use a trained model to produce output for a new input

Machine learning is deeply connected to statistics, but mixing the two expressions without context makes reading harder.

## Notation Policy in This Book

From this point on, the book follows these rules:

| Situation | Notation policy |
| --- | --- |
| meaning `run the trained model` | at first, write `inference (model execution)` or `inference (model application)` together |
| when Korean prose needs a short expression | avoid using the Korean word alone; prefer `model inference`, `model execution`, or `inference` together |
| when speaking about logical thought process | write `reasoning` together with a Korean gloss such as `logical reasoning` |
| when speaking about model result values | distinguish it as `prediction` or `model output` |
| when speaking about the statistical meaning | write `statistical inference` together |
| when speaking about generative-AI result creation | distinguish it as `generation` |

The point is not to erase translations. It is to keep the conceptual role visible even after translation.

In Korean, using that one word by itself can blur several meanings:

> is this model execution?  
> logical reasoning?  
> a prediction value?  
> statistical inference?  
> a generative process?

That is why the early part of this book keeps the English expression alongside the local wording. The English term is not decorative. It is a safety rail that lets different language editions and outside materials meet on the same conceptual axis.

## What to Remember from This Section

It is possible to translate `inference` with the Korean word often used for it, but in this book we read the conceptual role first and the translation second:

> inference = the execution that applies a trained model to a new input and produces output

Human thought process is separated as `reasoning`. Model output is separated as `prediction` or a generated result. The statistical meaning is separated as `statistical inference`.

If we keep those distinctions, later explanations of deep learning, LLMs, prompts, agents, and AI service architecture become much easier to read without unnecessary confusion.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
