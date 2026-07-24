# P6-5.2 Instruction Following and Conversational Interfaces Added on Top of Generation Structures

> Section ID: `P6-5.2`
> Version: `v2026.07.23`

In P6-5.1, we explained the GPT family as a decoder-centered flow that generates the next token based on previous tokens. But the chatbots, copilots, and conversational assistants we actually meet do not feel like simple continuation writing.

If we explain conversational LLMs only by increasing model size, the change users actually feel becomes blurry. The key point is that instruction following, dialogue format, safety adjustment, and interfaces are added on top of the generation structure, so a `continuation-writing model` begins to look like an `answering system`.

How did this structure become today's user experiences such as chatbots, copilots, and conversational assistants? A conversational LLM is a user experience made by adding layers such as instruction following, dialogue format, safety adjustment, and tool connections on top of a simple autocomplete model.

## Where It Changes Into a Conversational Experience

The conversational transition begins with the following questions.

- What is different between an autocomplete-style generative model and a conversational LLM?
- Why did users come to feel an LLM as an `answering system`?
- What else was needed outside the structure to create the conversational experience?

If we first grasp the broad flow of the conversational transition, later topics such as instruction tuning, alignment, prompt design, tool use, and agent loops can also be read by separating the `model itself` from the `adjustment layers that create user experience`.

The change in user experience did not arise simply from an increase in model parameters. If P6-5.1's GPT explanation dealt with `what generation structure appends the next token`, here we read what adjustments and interfaces are added on top of that generation structure so users feel it as a `system that answers questions`.

Therefore, the core difference is the distinction between `the generation structure itself` and `the adjustment layers that turn that structure into user experience`.

| Current Focus | Follow-Up Question | Where It Broadens Again |
| --- | --- | --- |
| GPT-based generation structure | How is text generated onward? | P6-5.1, P6-6.1, P6-7.1 |
| Conversational LLM experience | Why do users feel this as an answering system? | P6-5.2 |
| Instruction tuning and alignment | Through what adjustment stages is that experience made? | P6-9.1, P6-9.2 |
| Prompts and tool connections | How do we attach that adjusted model to actual requests and execution structures? | P6-10.1, P6-13.1, P6-13.2 |

In other words, the core of this chapter is moving from `what kind of structure generates something` to `why that structure came to look like a conversational experience`. This transition must be in place before we can read next-token prediction, pretraining, and instruction tuning as learning principles and later adjustment stages rather than as surface changes in user experience.

## Distinguishing Autocomplete, Instruction, and Safety Adjustment

- You can explain the difference between autocomplete-style GPT and conversational LLMs.
- You can say that instruction tuning, safety adjustment, and interface design were all needed for the conversational experience.
- You can explain that the chatbot experience is not completed by one model structure alone.
- You can move naturally into later explanations of pretraining, instruction tuning, prompts, and agents.

The result to check here is whether the conversational LLM experience begins to be read not as simple autocomplete, but as a structure where instruction interpretation, conversation history, and safety correction are bundled together.

- because it creates the need for instruction tuning and alignment that appear later
- because it explains why prompt engineering is not just an input sentence
- because it creates the basis for distinguishing agents, tool use, and MCP from the `model itself`

## Difference Between Autocomplete and Conversational Experience

Autocomplete and conversational LLMs both sit on top of generation structures, but the success criteria users expect are different. We need to read this difference as follows so later topics such as instruction tuning, alignment, prompts, and tool use do not get mixed into the same level.

| Level to Distinguish | Autocomplete-Style Experience | Conversational LLM Experience |
| --- | --- | --- |
| Basic expectation | Does it continue naturally after the previous sentence? | Does it reflect the user's question and intent? |
| Additional constraints | Are tone and sentence connection not awkward? | Does it follow format, role, and safety constraints? |
| Interface role | It looks like part of the input box | It looks like an assistant bundled with conversation history and system roles |
| Follow-up question | Why does it continue naturally? | What adjustment layer created the answering experience? |

## What It Means to Change From Autocomplete to Conversation

Early generative model user experience was generally like this.

- give the beginning of text
- make it keep writing after that

This was powerful, but it might not yet feel like an `assistant that answers questions`.

The conversational LLM experience arises when the following layers are added to this.

- the form of questions and answers
- instruction understanding that follows the user's intent
- response adjustment that reduces unnecessary repetition
- safety and policy constraints
- maintaining dialogue state

In other words, the model still generates the next token, but users no longer see it as an `autocomplete machine`; they come to feel it as a `conversational assistant`.

## What Changed the Experience?

It is insufficient to explain the conversational transition with only one cause. A safer explanation is as follows.

1. larger pretrained models
2. additional learning that adjusts the model to follow instructions
3. conversational interface design
4. safety and policy adjustment
5. sometimes tool use and search connections

In other words, the experience users meet is the combination of `model structure + later adjustment + product interface`.

## Why Did Natural-Language Instructions Become Important?

After the GPT-3 period, users more strongly experienced changing model behavior by putting explanations and examples inside prompts.

This matters because tasks can be specified:

- without replacing the model separately
- using only natural language
- as the work to perform

For example, instructions such as:

- `Summarize it in three sentences`
- `Organize it as a table`
- `Explain it so an elementary school student can understand`

become possible.

At this point, the model starts to feel not like a simple language generator, but like an `interface that follows natural-language instructions`.

## Why Did Safety Adjustment Become Important Together?

Conversational experience exposes risks more directly than simple generation.

- plausible errors
- aggressive expressions
- sensitive information handling problems
- wrong advice

These problems are exposed more directly to users.

So conversational LLMs usually need safety adjustment outside the structure as well.

We can understand it as follows.

`A good conversational LLM is not only a model that knows a lot, but a system also adjusted for how not to answer.`

## Why Does the Interface Also Feel Like Part of the Model?

Users usually experience the following as one bundle.

- input box
- conversation history
- system instructions
- model response
- sometimes search/tool execution results

But structurally, these are not all the same thing.

For example:

- the model generates the next token
- the app maintains conversation history
- the system prompt constrains the response direction
- tool connections perform external computation or search

We need to distinguish these differences to explain agents, MCP, and harnesses later without confusion.

## Three Layers That Create Conversational Experience

If we bundle the flow so far in one view, the conversational LLM experience is not closed by one `next-token generation model`.

- The model still generates the next token.
- The adjustment stage changes which instructions and formats that generation follows.
- The interface bundles conversation history, roles, and tool results together and shows them as user experience.

In other words, it is safer to read the chatbot users see as the result of `generative model + adjustment + interface`.

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-06/chapter-05/p6-c05-s02-conversation-shift-en.mmd"
```

The result to check in this diagram is that today's conversational experience is not a feature completed all at once, but an accumulated structure that passed through autocomplete, instruction following, and dialogue alignment stages.

## Cases and Examples

The diagram below groups the three cases in this section around the common question `are user intent and format constraints reflected in the actual response structure?`, rather than `does the sentence continue?`.

```mermaid
--8<-- "assets/part-06/chapter-05/p6-c05-s02-experience-types-en.mmd"
```

What we should confirm from this diagram is that even though all three experiences sit on top of generation, their evaluation criteria change. Autocomplete centers on `does it continue naturally?`, but conversational LLMs must also check `are intent, format, and safety constraints reflected in the actual response structure?`

### Case 1. General Autocomplete

Imagine writing only `Hello, what we discussed in the last meeting was` in an email compose box and receiving a recommendation for the next sentence. The first criterion people usually look at in this feature is `does the sentence continue naturally?` Here, rather than understanding the question intent or distinguishing roles, it is more important that a reasonable follow-up expression attaches after the previous sentence.

For example, if a natural follow-up sentence such as `I have attached the meeting materials` or `I organized it as follows` continues, users feel that the feature is working well. But at this stage, the system does not deeply interpret what the user is curious about or what format it should answer in.

This experience is closer to `writing the next sentence` than to `answering a question`. What changes here is that the criterion does not move to `does it solve the question?`; it remains at the criterion of `does a natural next sentence attach after the previous sentence?`

So the result to check in this case is not whether the user's question is deeply interpreted, but whether a natural follow-up sentence actually continues after the previous sentence.

The core of this case is not to bundle autocomplete and chatbots under the same success criterion. What we first look at in autocomplete is not `did it solve the intent?` but `is the continuation experience smooth?` If a reasonable follow-up sentence attaches after the previous sentence, users feel the feature worked well; conversely, even if the system understands the question well, awkward sentence connection can feel uncomfortable as autocomplete. So even though general autocomplete sits on top of generation, we need to separate the fact that its evaluation criterion differs from conversational instruction response.

Even with the same generation structure, the first criterion in autocomplete is narrower as follows.

| Scene | What Is Easy to Expect | What Autocomplete First Checks in Practice |
| --- | --- | --- |
| Continuing an email draft | It may seem like it will understand the question and solve the intent too | Does a natural follow-up expression attach after the previous sentence? |
| Recommending a meeting follow-up notice sentence | It may seem like it will do everything like an answering system | Are tone and continuation smoothness maintained? |
| Recommending a short sentence | It is easy to expect meaning resolution too | Are next-sentence candidates reasonable and quickly continued? |

The misunderstanding this table corrects is the expectation that `if it is a generative model, it should immediately work like a chatbot`. Even though general autocomplete sits on the same generation, its evaluation criterion remains much closer to the `continuation-writing experience`.

### Case 2. Chatbot

Imagine asking `Explain this policy in three sentences` while an internal policy document is open. What people usually expect from a simple autocomplete tool is about `next sentence candidates`, but from a chatbot they expect understanding the question, matching the length, maintaining the tone, and avoiding risky answers together.

If the model only continues part of the policy sentence at length, users will feel it as a `tool that continues sentences`, not as a `system that heard the question`. Conversely, when the system role, conversation history, summary length constraint, and safety rules work together, users feel that the request `three-sentence explanation` has actually been reflected.

This difference is the core dividing line between autocomplete and conversational LLM experience. What changes here is moving from a criterion of `does it continue naturally?` to a criterion of `are the question intent and format constraints reflected in the actual answer structure?`

So the result to check in this case is not simple continuation writing, but whether the length constraint and question intent are reflected in the actual answer structure.

This scene is also very important in actual product experience. From the moment users feel that they have `spoken to` a chatbot, they expect much more from it than from autocomplete. A three-sentence request should actually be three sentences, a policy explanation should summarize the key points without unnecessary additions, and risky guidance should be avoided. In other words, a chatbot does not pass just because its sentences are natural; `what it was told to do` and `what it must not do` must be reflected in the actual structure. So even with the same generation structure, autocomplete and conversational responses have different evaluation layers.

When the same generative model is read as a chatbot, the following criteria are added.

| Scene | What Is Easy to Miss If We Only Use Autocomplete Criteria | What Must Be Checked Additionally by Chatbot Criteria |
| --- | --- | --- |
| Request: `Explain it in three sentences` | If the sentences are natural, it may look okay | Was the three-sentence format actually followed? |
| Policy summary response | Smooth continuation may seem sufficient | Were the question intent and key information reflected? |
| Response with safety constraints | If it is long and friendly, it may look good | Did avoidance of prohibited content and role constraints actually work? |

The important criterion in this case is separating `natural sentences` from `an answer structure that matches the question`. A chatbot is not a continuation-writing tool; it appears here as a generation experience that must reflect intent, format, and safety constraints together.

### Case 3. Copilot

Imagine a developer writing a comment inside a function: `validate the user input here and return an error if it fails`. What people usually expect from simple autocomplete is `the next few characters`, but from a code assistant they expect it to read the function name, arguments, return format, and surrounding file context together.

If the model only gets the next line right and misses exception handling or return structure, it is hard for the developer to feel that it `understood the code context`. Conversely, when it reads the editor context and signature together and proposes conditionals, error messages, and return statements as one block, the same generation structure looks like a much more purpose-fit tool.

What changes here is moving from a criterion of `does the next line continue?` to a criterion of `does it reflect the surrounding code context and propose a more complete block?`

So the result to check in this case is whether a suggestion reflecting the whole function context actually continues into a more complete code block, rather than only completing one line.

If we group the three cases again from the user-experience perspective, we get the following.

| Situation | What Autocomplete Alone Lacks | What Conversational or Context-Reflecting Structures Must Check Further |
| --- | --- | --- |
| General autocomplete | natural continuation writing | in some cases, this alone is enough |
| Chatbot | simple follow-up sentence generation | question intent, format constraints, safety conditions |
| Copilot | next-line suggestion | function context, return format, exception handling block |

## Scenes Where Adjustment Layers Are Needed

After reading this section, even if you do not yet know the details of instruction tuning or alignment, you can first practice distinguishing `whether the scene you are seeing is a simple continuation-writing experience or an experience that needs conversational adjustment layers` as follows.

| Scene You See Now | Misunderstanding That Comes First | Question to Ask Instead |
| --- | --- | --- |
| It is enough if one natural sentence attaches well after the previous sentence | It is easy to feel that if it is a generative model, it should immediately solve questions like a chatbot | Is the current criterion continuation smoothness rather than intent resolution? |
| It often violates `summarize in three sentences` or tone is inconsistent | It is easy to feel that if the model gets smarter, format and role will automatically fit too | Is what is blocked now more a problem of instruction and format adjustment layers than generation ability? |
| One-line code recommendations are okay, but whole-function context and exception handling are often missed | It is easy to feel that if next-token generation works well, surrounding context reflection will also be solved automatically | Is what is needed now longer context reflection and product-interface combination? |

What matters in this table is not memorizing the name `chatbot`, but applying the fact that user evaluation criteria differ even on top of the same generation structure to concrete scenes.

The things often mixed here are as follows.

- It is easy to bundle natural continuation writing and question-intent resolution under the same success criterion.
- It is easy to see format following, role maintenance, and safety constraints only as a problem of one model structure.
- It is easy to fail to distinguish interface layers attached in product experiences such as copilots and chatbots from the model itself.

So the closing point of this section is to turn the phrase `a conversational LLM is the combination of a generative model + adjustment + interface` into an actual judgment criterion.

The purpose of this distinction is not to decide the cause all at once. Instead of flattening the situation into one sentence, `the conversational LLM is strange`, it is to briefly distinguish where the phenomenon you are seeing appears first among `continuation-writing experience`, `adjustment layer`, and `product-interface combination`.

## Exercise and Example

The goal of this exercise is to confirm how the `autocomplete experience` and the `conversational instruction-response experience` differ even on top of the same generation structure. We will compare two response candidates and directly mark whether format constraints, role, safety constraints, and structure are actually reflected.

Suppose the user request is as follows.

> Summarize this document in three sentences.

The system role is `an assistant that calmly explains learning content`, and what should be avoided is asserting uncertain facts and using aggressive expressions. These conditions are the input for this exercise. In other words, response candidates A and B in the table are two possible output examples after receiving the same user request, same system role, and same safety conditions.

The first table shows two output candidates for the input conditions. The `Response Candidate` column is the name of the comparison target, and the `Output Example` column is the sentence the user will actually see. The `First Visible Character` column helps with the first judgment of whether the output is closer to autocomplete or closer to conversational instruction response.

| Response Candidate | Output Example | First Visible Character |
| --- | --- | --- |
| A | `This document covers important content and also asserts uncertain facts...` | closer to autocomplete that continues after the previous sentence |
| B | `First, it organizes the core concepts.`<br>`Second, it explains the main examples and limitations together.`<br>`Third, it provides a perspective that connects to the next learning stage.` | closer to a conversational response that matches the requested format and role |

The second table is a criteria table that evaluates the output candidates from the first table. The `Judgment Criterion` on the left is an additional condition that must be checked in the conversational LLM experience, and the A and B columns mark whether each candidate satisfies that condition. The last column explains why that judgment is made.

Let's mark it directly with the following criteria.

| Judgment Criterion | A | B | Why They Split |
| --- | --- | --- | --- |
| Does it follow the three-sentence format? | No | Yes | A is closer to one line of continuation writing, while B matches the requested sentence count. |
| Is the explanatory assistant role visible? | No | Yes | A continues the context, while B reveals the role of organizing learning content. |
| Does it avoid expressions that should be avoided? | No | Yes | A contains an assertion of uncertain facts, while B reduces assertion risk. |
| Is it a structured response? | No | Yes | B creates a response structure with `First`, `Second`, and `Third`. |

The important point in this exercise is not that B is always the better sentence. In an autocomplete scene, simply continuing naturally after the previous sentence like A may be enough. But in a conversational scene where the user requested `summarize it in three sentences`, natural continuation writing is not enough; the requested format, role, and safety constraints must be reflected in the actual response structure.

## Output Criteria That Change in Conversational Experience

The previous exercise is the shortest scene showing that even with the same generation structure, `the experience of continuing the next sentence` and `the experience of following the user's instruction while matching response format, role, and safety conditions` are different. The key point to read here is not whether the model speaks longer, but that it is an adjusted experience where the format condition `summarize it in three sentences`, the role `an assistant that calmly explains learning content`, and expressions to avoid are reflected in the actual response structure.

The core to read in this example is as follows.

- both are generation
- autocomplete is closer to natural continuation writing
- a conversational LLM is an experience adjusted to follow the user's instruction format, role, and safety constraints more explicitly
- therefore, even on top of the same generative model, differences in user experience actually appear in items such as `format_followed`, `role_followed`, and `safety_ok`

If we separate this difference item by item, it can be read as follows. The autocomplete-style response is closer to writing a natural next sentence and does not satisfy the four criteria, while the instruction-response style includes format, role, safety conditions, and structure as response evaluation criteria.

![Comparison of user-experience criteria between autocomplete-style and instruction-response-style outputs](/AiBook/assets/part-06/chapter-05/conversation-experience-criteria-en.png)

The conversational LLM transition is hard to explain only as a simple increase in model scale. The reason actual user experience changed greatly is that:

- large generative models
- instruction-following adjustment
- conversational product interfaces
- safety correction

were bundled together.

If we reduce this example back into judgment criteria, the following three questions should come first.

| Scene | Question to Answer First |
| --- | --- |
| Why is natural autocomplete still unsatisfactory as a chatbot? | Is what you expect now reflection of format, intent, and role rather than continuation writing? |
| Why do `three sentences`, `calm tone`, and `avoid prohibited expressions` split even with the same generative model? | What adjustment layers and interface were added on top of the generation structure? |
| Why should a copilot read more than the next line and include surrounding function context? | Is product-provided context combination needed beyond simple token generation? |

## Checklist
- Can you explain a conversational LLM as a combination of `generative model + adjustment + interface`?
- Can you distinguish autocomplete and conversational response by format following, role, and safety constraints?
- Are you ready to read the next chapters by separating the model itself, adjustment layers, and tool layers?

## Sources and References

- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI 2019, accessed 2026-07-19. Used as background evidence for the language-model-based generation flow of GPT-2 before the conversational transition.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv 2020, accessed 2026-07-19. Used as the basis for explaining that GPT-3 receives task specifications and few-shot demonstrations through text interaction.
- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155){: target="_blank" rel="noopener noreferrer" }, arXiv 2022, accessed 2026-07-19. Used as the basis for explaining that compliance with user intent is not automatically guaranteed by model scale alone and that InstructGPT is made through human-feedback fine-tuning.
- OpenAI, [Aligning language models to follow instructions](https://openai.com/index/instruction-following/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used as supporting evidence that InstructGPT and RLHF are later adjustment layers that handle instruction following, safety, and alignment problems.
- OpenAI, [Introducing ChatGPT](https://openai.com/index/chatgpt/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used as the basis for explaining that dialogue format enables user experiences such as follow-up questions, admitting mistakes, and refusing inappropriate requests.
- OpenAI Help Center, [How can I use the Chat Completion API?](https://help.openai.com/en/articles/7232945-how-can-i-use-the-chatgpt-api){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used as operational evidence from current API usage guidance that developer instructions, message roles, and instruction following adjust the roles and constraints of a conversation session.
