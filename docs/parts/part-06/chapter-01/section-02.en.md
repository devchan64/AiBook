# P6-1.2 LLMs As The Central Case For Reading Generative AI

> Section ID: `P6-1.2`
> Version: `v2026.07.23`

Generative AI includes many flows: image generation, speech generation, video generation, code generation, and more. Part 6 does not cover all of them in depth. In this Part, we use an LLM (large language model) as the central case for reading how generative AI works and how it is used.

The reason for placing the LLM at the center is not that an LLM is all of generative AI. Text-based generative AI shows the following flow most directly within one Part.

```mermaid
--8<-- "assets/part-06/chapter-01/p6-c01-s02-llm-service-flow-en.mmd"
```

This flow does not stop at `the LLM creates an answer`. When a request comes in, the LLM first creates an artifact that can be read and written, but in an actual service that artifact must be controlled with better prompts, reinforced with external documents, or connected to tool execution and evaluation records.

Image and speech generation still share the common problem of `creating and reviewing an artifact`. However, the representative path in Part 6 is the text LLM. Reading text LLMs first lets us connect prompts, RAG, tool use, agents, evaluation, and operation constraints in one flow.

The text LLM is suitable as the representative case not because its output is easy just because it is made of sentences. On the contrary, sentence artifacts reveal many of the problems users face in real services on one screen.

## The LLM Is Not All Of Generative AI, But A Connection Point

Reading through LLMs as the central case does not mean image generation or speech generation is less important. The purpose of Part 6 is not to survey every type of generative AI, but to follow one generated artifact all the way through how it is reinforced and reviewed in a use scene.

The text LLM fits this purpose well. A user's request, the model's intermediate input, retrieved documents, function-call arguments, and evaluation records can all remain as text or structured text. This lets readers practice looking not only at the answer on the screen, but also at the traces before and after that answer was created.

| Generative-AI flow | Common problem | Point especially visible in LLMs |
| --- | --- | --- |
| Image generation | The artifact must be checked against the request intent. | It is easy to trace in sentences which conditions the prompt added or removed. |
| Speech generation | Tone, pronunciation, and contextual fit must be checked. | Script, instruction, and safety standards can first be separated as text. |
| Code generation | Execution results and errors must be checked. | Explanation, code, tests, and execution logs connect into one flow. |
| Text answer generation | Facts, evidence, authority, and format must be checked together. | It connects directly to RAG, tool use, evaluation, and operation records. |

Therefore, in Part 6, the LLM is not the conclusion that it is `the most important generative AI`. It is `the representative path where generation, reinforcement, execution, and review continue on one screen`. Without this perspective, the terms that appear later scatter like a list of product features.

## Reinforcement Structures Differ By Request Type

| User request | What the LLM can do first | Why it is hard to stop there | Needed reinforcement |
| --- | --- | --- | --- |
| `Tell me the refund policy.` | Create a natural explanation. | The policy may have changed. | Find and attach the latest document. |
| `Calculate the tax on this amount.` | Explain the calculation method. | Even a one-digit calculation error is a problem. | Check the value with a calculation tool. |
| `Send a reply to the customer.` | Draft the reply. | Actual sending requires authority and records. | Leave an approval process and execution record. |
| `Evaluate whether this answer is safe.` | Create a self-check sentence. | Without evaluation standards, review becomes close to a feeling. | Attach a rubric and human review. |

The important point in this table is not that the LLM solves every problem alone. Because an LLM can read the user's request and create an artifact, it clearly shows how far sentence generation can go and where the task must move to retrieval, calculation, approval, or evaluation. Part 6 is practice in reading that boundary.

So there are three misunderstandings to correct here. An LLM is not all of generative AI, but a representative case. Generative AI is not a technology that simply creates an artifact and ends there; in a use scene, review, reinforcement, and records must be attached. Text generation is not merely a writing function, but an execution flow that easily connects to retrieval, tools, evaluation, and operation structures.

## Cases And Examples

The following examples look like the same request to `create an answer`, but the needed structure differs.

| Request | Artifact that can be created first | Where it gets stuck | Structure to attach next |
| --- | --- | --- | --- |
| `Summarize the meeting in three lines.` | Summary | If the evidence is already in the input, prompt adjustment is usually enough. | Format instruction, length limit |
| `Summarize our company's security policy.` | Policy explanation | Model memory or general knowledge cannot guarantee the latest internal policy. | Document retrieval, evidence citation |
| `Calculate the shipping cost for this order.` | Calculation explanation | Actual order amount, region, and coupon conditions must be calculated accurately. | Data lookup, calculation function |
| `Process a refund if the conditions are met.` | Processing guide | Actual state changes require authority, approval, and records. | Function call, approval, execution log |

The four rows in this table are a compressed map of the Part 6 table of contents ahead. Prompts adjust the format and context of artifacts. RAG attaches external evidence. Tool use handles lookup, calculation, and execution. Agents and harnesses repeat multiple steps and leave them as records.

## Apply It Directly

Read the following requests and separate `what to try first with prompts alone` from `what needs an attached structure`.

| Request | What to try first with prompts alone | What needs an attached structure |
| --- | --- | --- |
| `Make this notice sound softer.` | Specify tone, length, and reader level. | Usually no additional structure is needed. |
| `Write a quotation using today's exchange rate.` | Specify quotation format and tone. | Latest exchange-rate lookup and a calculation tool are needed. |
| `Issue a coupon to the customer and explain it.` | Specify the form of the guidance sentence. | Coupon-issuing authority, execution API, and records are needed. |

The reason for reading LLMs as the central case is that this boundary is visible. The text answer is the starting point, and the actual service is completed by attaching evidence, execution, evaluation, and records to that answer.

## Exercises And Examples

Look at the following requests and mark one reason why the LLM artifact alone is not enough. The right column gives the checking explanation.

| Request | Generated artifact | Additionally needed structure |
| --- | --- | --- |
| `Compare our company's latest pricing plans.` | Comparison explanation | Latest document retrieval |
| `Calculate expected cost from this month's usage.` | Calculation explanation | Actual calculation tool |
| `Issue a compensation coupon to the customer.` | Guidance sentence | Authority check and execution record |

All three requests look like text answers, but the required reinforcement structures differ. This distinction is what lets us read the LLM not as a simple chat tool, but as the central case for reading generative-AI service structures.

Once this distinction is in place, the LLM no longer looks only like `a function that writes sentences in a chat screen`. The LLM is not all of generative AI, but it is the representative case that lets us read generated artifacts, reinforcement structures, and operation records in one flow.

## Checklist

- You can explain that an LLM is a representative case, not all of generative AI.
- You can explain why Part 6 centers on text LLMs.
- You can distinguish commonalities and scope differences between image, speech, video generation, and LLMs.
