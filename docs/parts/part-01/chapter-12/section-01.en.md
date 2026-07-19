# P1-12.1 What Does a Prompt Specify?

> Section ID: `P1-12.1`
> Version: `v2026.07.19`

Chapter 11 explained where `LLMs` came from. Language models began from the problem of next-token probability, and Transformers and pretraining became key foundations of modern LLMs.

This section now turns to how users interact with LLMs. The starting point is the `prompt`.

The central question is:

> what kind of input does a prompt provide to the model?

The key perspective is:

> a prompt is not training data that retrains the model;  
> it is a way of placing instructions, context, examples, constraints, and output format inside the current input so the model can use them while generating the response

Part 1 introduces the basic distinctions among `prompts`, `instructions`, `context`, `examples`, `constraints`, `output format`, and `prompting versus fine-tuning` here. Section 11.3 already distinguished `in-context learning` from `pretraining`. This section continues from there and organizes the question:

> what can a user specify through input?

Prompts do not reveal the internal mechanics of an LLM directly. But they do make it possible to observe how output changes when the same model receives different input conditions. So a prompt is not proof of the model’s inner structure. It is better treated as an external entry point for observing inference behavior.

This section does not cover a catalog of prompt-engineering techniques. `Chain-of-thought`, `few-shot example design`, and `role prompting` return in P1-12.2. Evaluation prompts and limit analysis return in P1-12.3.

These terms can all sound like similar input ingredients at first. A quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| prompt | the full input that contains the conditions for the current response | the starting point of Chapter 12 |
| instruction | the request that tells the model what to do | the core of task specification |
| context | background information needed for the task | the supporting material that changes output direction |
| example | an input-output demonstration of the desired pattern | a guide to format and judgment style |
| constraint | a limit on length, scope, forbidden content, and so on | the boundary-setting device |
| output format | a way of specifying the shape of the result | a tool that helps downstream review and processing |

The minimum distinction to keep is:

- the prompt is the whole input
- the instruction is the task
- context is background
- an example shows a pattern
- constraints define boundaries

This section focuses only on what prompts specify:

| Topic | Question in this section |
| --- | --- |
| instruction | how do we tell the model what task to perform? |
| context | what background information do we provide for the response? |
| example | how do we show the desired input-output pattern? |
| constraint | how do we limit length, format, scope, or forbidden conditions? |
| output format | what shape of result do we want back? |

A prompt is not a magic spell. Even with the same model, different input arrangements can lead to different outputs, but prompts do not change model weights.

The focus here is to understand prompts as `input structure`. Example placement and evaluation criteria are deferred to 12.2 and 12.3.

## Goal of This Section

- Understand a prompt as natural-language input given to an LLM.
- Explain that prompts can specify instructions, context, examples, constraints, and output format.
- Understand that prompts let us observe how input conditions affect generation.
- Distinguish prompting from fine-tuning.
- Understand that prompts do not guarantee factual verification or truth.
- Treat good prompting not as `clever wording`, but as `clear input specification for a task`.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a prompt is a form of input design for the model | This reduces the mistake of treating prompts like magic spells. | It is enough to understand that a prompt is input that contains a question, conditions, and context. |
| prompts do not change model parameters | This helps separate the learning phase from the usage phase again. | It is enough to know that changing wording or results does not mean the model itself has been retrained. |
| prompts can include instructions, context, and examples | This prepares the next section on prompt components. | It is enough to understand that prompts can specify what to do, what to refer to, and what pattern to follow. |

## A Prompt Is Input for Building the Current Response

An LLM reads input tokens and generates the next tokens. A user’s question, command, document, example, or dialogue history all become part of the input the model can use while producing the next output.

That is why prompts help us understand LLM behavior. If the same topic is asked with different target readers, scope, examples, or forbidden conditions, the output changes. That does not explain the internal circuitry of the model, but it does let us observe that an LLM is sensitive to the current input context.

For example:

> explain the history of AI to a reader who is seeing it for the first time

This prompt already specifies at least three things:

| Element | What it specifies |
| --- | --- |
| topic | the history of AI |
| task | explain it |
| reader | a first-time reader |

If the prompt becomes more explicit:

> explain the history of AI to a first-time reader  
> distinguish the flow of rule-based AI, machine learning, deep learning, and LLMs  
> keep each stage within three sentences  
> avoid exaggerated phrasing

Now the prompt specifies not only the topic, but also scope, structure, length, and tone. The model uses these as part of the input when generating the response.

## Prompting Is Not Learning, but Condition Specification

Giving a prompt does not mean the model has learned something new. As Section 11.3 explained, `in-context learning` is safer to understand as a change in current output behavior caused by instructions and examples inside the input context, without updating model weights.

> fine-tuning:  
> update model weights using training data
>
> prompting:  
> place task conditions inside the current input to guide the output

The GPT-3 paper by Brown and colleagues explains zero-shot, one-shot, and few-shot settings while keeping the model fixed and providing task and demonstration through textual interaction rather than gradient updates or fine-tuning.

So the safer distinction is:

> changing the model itself:  
> pretraining, training, fine-tuning
>
> changing the conditions of the current response:  
> prompts, examples, dialogue history, provided documents

If this distinction is lost, people can misunderstand prompts as if they make the model `learn the fact permanently`, or as if something told once will always remain inside the model afterward.

## A Prompt Can Contain Both Instruction and Context

Prompts usually contain both `instruction` and `context`.

> instruction:  
> what is the model being asked to do?
>
> context:  
> what information should the model refer to while doing it?

For example:

> rewrite the following sentence as an introductory explanation
>
> sentence:  
> Transformers compute sequence representations using self-attention.

Here, `rewrite the following sentence as an introductory explanation` is the instruction. `Transformers compute...` is the target text and also the local context.

As prompts become longer, instruction and context can easily blur together. That is why it is often safer to separate them explicitly:

> task:  
> rewrite the following sentence for an introductory reader
>
> original sentence:  
> Transformers compute sequence representations using self-attention.
>
> conditions:  
> - keep it within three sentences  
> - use only one analogy  
> - avoid phrases like “understands like a person”

That makes it more likely that the model can distinguish the roles played by different parts of the input. But even this is not a guarantee. A prompt is a way to express conditions clearly, not a device that guarantees correctness automatically.

## Examples Show a Desired Output Pattern

An `example` is input that shows the model the pattern you want.

> input: AI  
> output: artificial intelligence
>
> input: ML  
> output: machine learning
>
> input: LLM  
> output:

Given these examples, the model becomes more likely to continue with `large language model`.

This is the basic intuition of `few-shot prompting`: place several input-output demonstrations inside the prompt so the model can infer the current task’s form and intention.

Examples can be powerful, but they also carry risks.

> bad example:  
> can reinforce the wrong pattern
>
> biased example:  
> can narrow the direction of output too much
>
> overly long example:  
> can push important instructions out of the effective context window

Examples are not permanent training data. They are current patterns to be referenced inside the input. That is why the quality of examples can directly affect the quality of outputs.

## Constraints Narrow the Range of Results

Prompts can also give `constraints` that narrow the allowed range of outputs.

> explain it in under 200 characters  
> organize it as a table  
> if there is no verifiable evidence, mark it as `needs verification`  
> do not use difficult equations for first-time readers  
> write Korean terms with the English original in parentheses

Constraints tell the model the boundaries of the task. In writing this book, constraints matter a great deal.

For example, these two prompts are likely to produce different results:

> prompt A:  
> explain LLMs
>
> prompt B:  
> explain LLMs to a reader revisiting an introductory AI course  
> cover only the relation among Transformers, pretraining, and prompts  
> leave RAG and agents to the next chapter  
> do not include unsupported forecasts

Prompt B specifies the task, reader, scope, excluded material, and verification standard together. The reason it is more useful is not that it is longer, but that the necessary conditions are clearer.

## Prompts Do Not Guarantee Factuality

A better prompt can raise the chance of getting a more useful answer. But prompts alone cannot guarantee `factuality`, `evidence`, or `safety`.

For example, this is dangerous:

> write this claim so it sounds convincing and factual

That kind of prompt can encourage unsupported statements to appear persuasive. In this book, the preference is the opposite:

> write only verified content as factual  
> if the evidence is weak, label it as `needs verification`  
> separate personal interpretation from standard explanation

Prompts can guide output, but they do not replace verification responsibility. In a learning-oriented book, evidence review matters more than prompt wording.

## Checklist

- I can explain a prompt as the current input given to an LLM.
- I can distinguish instruction from context.
- I can explain that examples show output patterns.
- I can explain that constraints narrow the range of the result.
- I can explain that output format can also be specified in the prompt.
- I can explain that prompts do not directly reveal the inside of the LLM, but do let us observe changes in output under different input conditions.
- I can explain the difference between prompting and fine-tuning.
- I can explain in-context learning as a behavior change inside the current input context without weight updates.
- I can explain that prompts do not automatically guarantee factuality, evidence, or safety.
- I can explain prompts not as `tips for saying things nicely` but through the structure of `current input`, `task conditions`, `no weight update`, and `separate verification responsibility`.
- I can distinguish where prompting, fine-tuning, and in-context learning diverge.

## Sources and Further Reading

- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-06-23.
- Pranab Sahoo et al., [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/abs/2402.07927){: target="_blank" rel="noopener noreferrer" }, arXiv, 2024, accessed 2026-06-23.
- OpenAI, [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering){: target="_blank" rel="noopener noreferrer" }, OpenAI API documentation, accessed 2026-07-19.
