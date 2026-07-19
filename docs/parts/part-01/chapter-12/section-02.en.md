# P1-12.2 Instructions, Context, and Examples

> Section ID: `P1-12.2`
> Version: `v2026.07.19`

Section 12.1 described a `prompt` as a way of arranging task conditions inside the current input. A prompt does not retrain the model. Instead, it places instructions, context, examples, constraints, and output format inside the input that the model can use during `inference`.

This section separates the three most basic parts of that structure:

> instruction:  
> what is the model being asked to do?
>
> context:  
> what should it refer to while doing that?
>
> example:  
> what desired input-output pattern is being shown?

Once these three are distinguished, a prompt becomes easier to read not as `a polished sentence`, but as `an input structure that arranges task conditions by role`.

Part 1 introduces the basic intuition of `instructions`, `context`, `examples`, `few-shot prompting`, and `structured prompting` here. Section 12.1 first explained what prompts specify. This section separates the three most central elements. Evaluation criteria and limits are handled separately in 12.3.

## Scope of This Section

This section does not cover advanced prompt-engineering techniques in detail. Techniques such as `Chain-of-thought`, `self-consistency`, and `automatic prompt optimization` are not explained deeply here. They return later in the practical context of Part 5 P5-9.3.

These terms can all sound like decorative ways of making a prompt longer. A quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| instruction | the request that says what to do | the element that sets the task goal |
| context | the information that should be referred to | the element that sets background and scope |
| example | a demonstration of how the answer should look | the element that guides format and judgment style |
| few-shot prompting | the method of including a few examples in the prompt | the representative form showing how examples work |
| prompt structuring | the method of separating roles inside the input | the way to improve repeatability and reviewability in long tasks |

The minimum distinction to keep is:

- the instruction is the task
- context is the reference information
- an example is the demonstration
- few-shot prompting means a prompt that includes examples

This section also does not cover `RAG`, `tool use`, or `agents`. RAG returns in P1-13.3 and P1-13.4. Tool use and agents return in P1-14.2 and P1-14.3. The only goal here is to learn the basic components that should be separated first when giving requests to an LLM.

This section also does not ask whether a prompt `guarantees a good result`. That question is deferred to 12.3 through the lenses of limits, evaluation, and reproducibility.

| Element | Question in this section |
| --- | --- |
| instruction | how do we state the task clearly? |
| context | how do we provide the background information and materials needed for the task? |
| example | how do we show the desired shape of the result? |

## Goal of This Section

- Distinguish instruction, context, and example.
- Explain how the three can be arranged separately inside one prompt.
- Understand that examples do not retrain the model, but show patterns inside the current input.
- Understand that even with context, factual verification is not automatically complete.
- Prepare naturally for the limits and evaluation criteria handled in 12.3.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| an instruction means `do this task` | This clarifies the most visible part of a prompt. | It is enough to know that it is a request such as summarize, compare, translate, or review. |
| context is the background the model should refer to | This shows why the same question can lead to different answers under different background information. | It is enough to understand that context includes support material such as documents, role, or scope. |
| an example shows the desired output pattern | This makes few-shot prompting easier to understand. | It is enough to treat it as a demonstration of how to answer. |

## The Instruction Specifies the Task

An `instruction` is the part that tells the model what to do.

> summarize this  
> compare these two things  
> rewrite this for beginners  
> organize it as a table  
> mark weakly supported statements as `needs verification`

If the instruction is vague, the model interprets the task broadly.

> vague instruction:  
> tell me about AI
>
> clearer instruction:  
> explain the relationship among AI, machine learning, deep learning, and generative AI to a reader reviewing an introductory AI course

Both prompts are natural-language requests. But the second one specifies the task target, the reader, and the concepts to compare much more clearly.

An instruction is not better just because it is longer. A good instruction narrows the task.

| Focus of the instruction | Example |
| --- | --- |
| task | summarize, compare, classify, transform, review |
| target | sentence, table, code, claim, table of contents |
| reader | first-time reader, practitioner, researcher, child |
| criteria | evidence-centered, short, bilingual, avoid exaggeration |

In writing this book, it is especially important to include the `target reader` and the `review standard` inside the instruction.

> explain this to readers who studied introductory AI a long time ago but forgot much of it  
> separate personal interpretation from standard explanation  
> do not write unsupported forecasts

That kind of instruction tells the model not only `what to write`, but also `by what standard to write it`.

## Context Provides the Information to Refer To

`Context` is the information the model should use while carrying out the instruction. This can include background, source text, purpose, earlier decisions, reader conditions, or excluded scope.

For example, this prompt has only an instruction:

> rewrite this sentence more simply

The model still does not know what sentence it should work on. Once context is added, the task becomes possible:

> task:  
> explain the following sentence more simply for a reader reviewing introductory AI
>
> original sentence:  
> Transformers compute relationships among input tokens using self-attention.
>
> context:  
> this document prioritizes conceptual recovery over mathematical detail

Here, `task` is the instruction. The original sentence and the contextual note are reference material.

Context does not mean only general background description. The following can all count as context:

| Type of context | Example |
| --- | --- |
| source text | the sentence to rewrite, the passage to summarize, the claim to review |
| reader | first-time learner, reviewer, developer, non-major |
| purpose | book manuscript, review memo, presentation material, code comment |
| earlier decision | this chapter does not cover RAG yet |
| excluded scope | unsupported forecasts, exaggerated phrasing, core explanation reserved for a later chapter |

When giving context, an important distinction is:

> what is left for the model to guess  
> versus  
> what is explicitly provided as input

Compare:

> prompt that leaves guessing:  
> write the next section
>
> prompt with context:  
> the previous section explained what prompts specify  
> this section distinguishes instruction, context, and example  
> the next section will cover limits and evaluation  
> so do not go deeply into those limits here

The second prompt tells the model the chapter position and section boundary. This matters especially in long documents.

## Examples Show the Desired Pattern

An `example` is the part that demonstrates the input-output pattern you want. Brown and colleagues described the `few-shot` setting in GPT-3 as including a few task demonstrations inside the input without additional fine-tuning.

At an introductory level:

> instruction:  
> write terms in Korean with the English original
>
> example:  
> input: AI  
> output: 인공지능(artificial intelligence)
>
> input: ML  
> output: 머신러닝(machine learning)
>
> input: inference  
> output:

The example shows the model the pattern of the desired answer. That increases the chance that it continues with something like `모델 실행(inference)` or, depending on context, another context-appropriate bilingual form.

Examples can also show not only answer format, but judgment criteria.

> instruction:  
> review the following sentence and separate standard explanation from personal interpretation
>
> example:  
> sentence: Deep learning is a direct copy of the human brain.  
> review:  
> - standard explanation: artificial neural networks were inspired by biological neural networks, but are not literal copies of the human brain  
> - personal interpretation: it is acceptable as a loose analogy for intuition  
> - judgment: risk of exaggeration
>
> sentence: A prompt does not change model weights.  
> review:

This example does more than show a formatting pattern. It also shows the review frame itself: `standard explanation`, `personal interpretation`, and `judgment`.

Examples still need caution.

| Problem with the example | Why it is risky |
| --- | --- |
| wrong example | the model may copy the wrong pattern |
| biased example | the output direction may become too narrow |
| too many examples | important instructions and context may be buried |
| conflicting examples | it becomes unclear what pattern the model should follow |

Examples are not permanent knowledge updates. They are patterns supplied for the current input.

## Once the Three Parts Are Separated, the Prompt Becomes Readable

The first step to writing better prompts is not to craft stylish sentences. It is to separate roles inside the input.

> task:  
> rewrite the following paragraph for readers reviewing introductory AI
>
> context:  
> - this document is study material for recovering concepts learned long ago  
> - personal interpretation must be separated from standard explanation  
> - this section does not cover RAG or agents
>
> original text:  
> prompts are a means to understand how LLMs behave
>
> example:  
> good wording:  
> prompts do not reveal the inside of an LLM directly,  
> but they let us observe how outputs change under different input conditions
>
> wording to avoid:  
> by looking at prompts, we can know the internal principle of an LLM
>
> output format:  
> - revised sentence  
> - reason for revision  
> - points that need verification

This prompt separates instruction, context, source text, example, and output format. That makes it easier for a reviewer to see what is being requested, and more likely that the model can distinguish the roles played by each part.

Of course, structuring a prompt this way does not guarantee a correct answer. A prompt organizes input conditions. It does not replace fact checking or quality evaluation. Those limits return in 12.3.

## A Basic Template That Works Well for Long Learning Documents

For long learning documents, the following template is often useful:

> task:  
> what is being requested?
>
> target:  
> what original text or material is being reviewed or written?
>
> context:  
> what are the document position, reader, earlier decisions, and excluded scope?
>
> criteria:  
> what are the standards for evidence, terminology, bilingual notation, section boundaries, and avoiding exaggeration?
>
> example:  
> what short example shows the desired format or judgment style?
>
> output:  
> in what shape should the result be returned?

This template does not fit every situation exactly. But when a long book is written with AI tools, it helps structure the request and leaves clearer points for later human review.

## Checklist

- I can explain that an instruction specifies the task the model should perform.
- I can explain that context provides background information and materials needed for the task.
- I can explain that examples show the desired input-output pattern.
- I can explain that examples do not change model weights the way fine-tuning does.
- I can read a long prompt by separating task, context, source text, example, and output format.
- I can explain that prompt structuring does not replace fact verification.
- I can read a long prompt by separating it into `what to do`, `what to refer to`, and `what pattern to follow`.
- I can explain that few-shot prompting does not retrain the model, but only presents a pattern inside the current input.

That shifts the problem away from `making the prompt longer` and toward `making its roles readable and checkable`.

## Sources and Further Reading

- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-06-23.
- Pranab Sahoo et al., [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/abs/2402.07927){: target="_blank" rel="noopener noreferrer" }, arXiv, 2024, accessed 2026-06-23.
- OpenAI, [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering){: target="_blank" rel="noopener noreferrer" }, OpenAI API documentation, accessed 2026-07-19.
