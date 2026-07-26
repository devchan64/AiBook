# P6-8.1 Fine-Tuning Needed for Purpose-Specific Adjustment

> Section ID: `P6-8.1`
> Version: `v2026.07.26`

In P6-7.1, we saw pretraining, which first creates a broad language base.
But pretraining alone does not automatically create `responses that match our work criteria`. This section explains how the learning axis placed on top of the generation structure narrows from `making a general-purpose base` to `purpose-specific adjustment`.

In P6-6.2, we saw that generation is a process of repeatedly selecting the next token from a probability distribution. But in an actual service, one more question appears here.

How can we change a large pretrained model so it fits our purpose better?

Fine-tuning is the process of additionally adjusting an already pretrained model so it fits a specific task or domain better.

If we say the same thing more simply, it is as follows.

Fine-tuning is the stage of refining a large model that has already broadly learned language so it fits our work better.

## Moment Purpose-Specific Adjustment Is Needed

Purpose-specific adjustment begins with the following questions.

- What does fine-tuning adjust?
- How is it different from only changing prompts?
- In what situations is fine-tuning needed?

Fine-tuning is an `adjustment layer that narrows a general-purpose base closer to our purpose`. The cost problem of adjusting the whole model is a problem of efficient adjustment, and the choice problem with prompts, RAG, and tool use is a problem of input design and external evidence connection. We need to separate these levels so we do not read fine-tuning as the solution to every problem.

Fine-tuning is not `making a model from scratch`, but an adjustment stage after pretraining. If pretraining was the stage that made a broad base, fine-tuning adjusts response habits so that base comes closer to our classification criteria, style, and output format.

Therefore, the question to hold here is `what should we adjust so it fits our task and format better?` Instruction tuning then narrows it further so it responds better to the way people make requests, and alignment further fits safety and policy boundaries. How to reduce the cost of adjusting the whole model is handled separately in P6-8.2 on LoRA.

The impression of `making a new model` should be reread as `additionally adjusting a pretrained foundation model for our purpose`.

## Distinguishing Prompt Adjustment and Purpose-Specific Adjustment

- You can explain fine-tuning as additional adjustment after pretraining.
- You can say the difference between prompt adjustment and fine-tuning.
- You can distinguish when fine-tuning is advantageous and when prompts or RAG may come first.
- You can read efficient adjustment methods such as LoRA as `options that reduce fine-tuning cost`.

This distinction matters for the following reasons.

- because it shows the practical connection point after pretraining
- because it separates prompts, RAG, and fine-tuning as different options
- because it creates the base for explaining PEFT and LoRA in P6-8.2

## Judgment Criteria for Choosing Fine-Tuning

Fine-tuning cannot be chosen by saying that it is a stronger method than prompts. We first need to split the selection criteria according to what we want to change.

| Judgment Criterion | Question to Check |
| --- | --- |
| Adjustment target | Is it adjusting the response habits of a foundation model for a purpose, rather than making a new model from scratch? |
| Difference from prompts | Is this a problem of changing input instructions, or changing the model's internal response tendency? |
| Difference from RAG | Is this a problem of connecting latest information, or a problem of repeated judgment criteria and output habits? |
| Work criteria | Do internal labels, domain expressions, or output formats repeatedly shake? |

## What Does Fine-Tuning Adjust?

A pretrained model is already in a state where it has learned broad general language patterns. But actual work is more concrete.

It is easier to understand if we first read it through the following three questions.

| Question | Short Answer |
| --- | --- |
| Why adjust an existing model again? | because general ability alone may fit our purpose less well |
| What are we trying to fit better? | format, domain terms, classification criteria, response tendency |
| Do we make it again from scratch? | usually no; we adjust it on top of an existing foundation model |

For example:

- summarizing legal documents
- classifying internal customer inquiries
- drafting medical consultation notes
- generating answers that match an internal company format

In these cases, a general model alone may not match expression style, judgment criteria, or domain terms enough. Fine-tuning additionally adjusts the model's weights to reduce this gap.

In other words, fine-tuning is a process of placing `additional adaptation for a specific purpose` on top of a `base model`.

Therefore, the core question of fine-tuning is closer to `does this model fit the criteria and format of our problem better?` than `is this model smart?`

## Difference from Prompts

This difference is very important.

| Method | What It Changes |
| --- | --- |
| prompt | input instructions and context |
| fine-tuning | part or all of the model's internal weights |

A prompt is a method of designing input outside the model. Fine-tuning, on the other hand, adjusts the model's internal operation itself a little more toward a specific purpose.

`Prompts change how we speak to the model, while fine-tuning adjusts the model's response habit itself so it fits the purpose better.`

The difference between the two can be divided as follows.

- prompt: a method of writing instructions better outside the model
- fine-tuning: a method of adjusting internal response tendencies to fit the purpose better

## When Is Fine-Tuning Needed?

Not every problem needs to be solved with fine-tuning. Instead, we should first ask the following questions.

- Is prompting alone enough?
- Is RAG more appropriate because latest external knowledge is needed?
- Must result format, tone, and classification criteria be maintained very consistently?

Fine-tuning is especially considered in situations such as the following.

- when output in a specific format is repeated often
- when domain terms and expression style matter strongly
- when classification or extraction criteria are strongly connected to internal policy
- when prompts alone lack stable reproducibility

If we reduce this list further, the following two cases are central.

1. when `format consistency` of the result matters
2. when the `judgment criteria` of the result are strongly connected to internal rules

## Fine-Tuning Is Not万能

We need to remember this together as well.

Fine-tuning does not automatically give:

- latest fact reflection
- hallucination removal
- security resolution

For example, for latest company notices or real-time policy changes, RAG or separate data connections may be more appropriate than fine-tuning.

Therefore, a safer explanation is as follows.

`Fine-tuning is a method for increasing specific response tendencies and task fit, not a method that solves recency, factuality, and safety all at once.`

We need to hold this sentence first in practice so we do not mix `response tendency adjustment`, `latest information connection`, `evidence presentation`, and `permission control` as the same problem. In reality, the last three are separate design problems.

## Conditions Where Fine-Tuning Is Needed

If we summarize this so far in the shortest form, it is as follows.

- Prompts change `input instructions and context`.
- Fine-tuning adjusts `the model's response habits and output tendencies` more toward a purpose.
- RAG deals with `connecting latest information and external evidence`.

We need to distinguish these three so we can first choose the right option according to `what we want to change`.

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-06/chapter-08/p6-c08-s01-finetuning-flow-en.mmd"
```

The result to check in this diagram is that fine-tuning is not `making a new model from scratch`, but the process of adjusting an already broadly trained foundation model to current task criteria.

The way to read this figure is simple.

- the foundation model on the left is `already broadly learned`
- task data is `the criteria of our problem`
- the result is `a response that fits the purpose better`

## Cases and Examples

The diagram below groups the three cases in this section around the common question `does it fit the format and judgment criteria of our work more stably?`, rather than `does it make the model smarter?`

```mermaid
--8<-- "assets/part-06/chapter-08/p6-c08-s01-finetuning-cases-en.mmd"
```

What we should confirm from this diagram is that the core of fine-tuning is not `unconditionally putting in more knowledge`. In all three scenes, what matters first is whether work-side rules such as `internal labels`, `domain terms`, and `output structure` are reflected more stably.

### Case 1. Internal Customer-Center Classification

Even if a general model can roughly classify inquiries, it is easy to think, `Wouldn't it be okay in practice if they are only roughly separated and a person checks them again?` But in actual operations, people first check whether inquiries are stably divided by `our company's label criteria`. For example, by external general criteria, `cancellation` and `refund` may be treated similarly, but internally they may need to be sent to different teams. If this boundary shakes, the routing itself goes wrong and handling time increases even if the answer sentence is natural.

What changes here is a shift from the criterion `is it classified roughly similarly?` to the criterion `does it stably preserve internal label boundaries?` In this case, it becomes more important to adjust model responses so they reflect internal label criteria more strongly than to write longer explanations. So the result to check in this case is whether similar inquiries enter the same team more stably according to internal label criteria, and whether variation that people must keep filling in afterward actually decreases.

### Case 2. Medical Document Summarization

Even if general summarization is possible, in medical documents it is easy to feel, `Isn't a good summary just one that shortens well?` But in medical documents, people first check `which terms must remain and which expressions must be maintained in the same way`, rather than `was it shortened well?` For example, drug names, dosages, and contraindication expressions must always remain in the same way, but if a general model shortens them differently each time, practical quality can shake greatly even if the length is right. In severe cases, the same prescription content may be changed into different expressions in each summary, forcing reviewers to compare the original again.

What changes here is moving from the criterion `did it shorten length well?` to the criterion `does it consistently preserve domain key terms and expression rules?` In this scene, adjustment that reflects domain style and abbreviation rules more stably becomes more important than adding latest knowledge. So the result to check in this case is whether drug names, dosages, and contraindication expressions are maintained the same way across summaries, and whether reviewers actually compare the original less because of expression variation.

### Case 3. Legal Draft Format

When document format and expression rules matter, not simple information generation, it is easy to first check `is the content correct?` Prompts can guide the format to some degree, but if article-numbering methods, proviso phrases, and liability-limitation expressions differ by draft, review cost grows quickly. For example, if the same contract draft starts with `Article 1` in one answer and `1.` in another, and the position of disclaimer language also shakes, format correction must be done again before content review.

What changes here is moving from the criterion `is only the factual content correct?` to the criterion `does it repeatedly maintain the same style and output structure?` In this case, creating `the same drafting habit every time` matters more than finding new facts. So the result to check in this case is whether article numbers, disclaimer language, and proviso expression positions do not shake greatly across drafts, and whether the reviewer's format-correction burden actually decreases.

If we group the three cases again from the purpose-adaptation perspective, we get the following.

| Situation | What Can Easily Shake With a General Model | What Fine-Tuning Tries to Stabilize |
| --- | --- | --- |
| Internal customer-center classification | internal label boundaries and routing criteria | maintaining classification boundaries by team |
| Medical document summarization | consistency of drug names, dosages, and contraindication expressions | maintaining domain terms and summary format |
| Legal draft format | repetition of article numbers, provisos, and disclaimer positions | reproducibility of style and output structure |

## Scenes Where Fine-Tuning Judgment Is Needed

After reading this section, even if you do not yet know the details of LoRA or PEFT, you can first practice separating whether what is needed now is `prompt adjustment`, `fine-tuning`, or `latest information connection`. If the same inquiry frequently crosses internal label boundaries and goes to different teams, you should see whether fine-tuning that reflects internal judgment criteria more stably is needed, rather than making explanations longer. If tone and style shake slightly each time in the same domain answer, ask whether persistent response-habit adaptation is needed rather than putting long style rules into every prompt. If only the latest notices and policy numbers are often wrong, RAG or external data connection may come before fine-tuning. If the output format is mostly right and only the tone of the first sentence needs a small adjustment, prompt design is a lower-cost option than adjusting inside the model.

What matters here is not memorizing that `fine-tuning is the stronger method`, but first reading `what do we want to change?` by splitting it into `input instruction`, `model response habit`, and `external information connection`.

The things often mixed here are as follows.

- It is easy to see internal response-habit adjustment and latest information connection as the same problem.
- It is easy to fail to distinguish scenes where prompts are enough from scenes where fine-tuning is needed.
- It is easy to feel fine-tuning as `making a model from scratch`.

Therefore, the sentence `fine-tuning is a purpose-specific adjustment layer` should become a practical selection criterion.

## Exercise

The goal of this exercise is not to run code, but to look at the same work scenes and distinguish what should be suspected first among `prompt adjustment`, `fine-tuning`, and `RAG`. Fine-tuning is not a choice that makes the model memorize more facts, but a choice that tries to fit repeated response habits and internal criteria more stably.

Look at the following inquiry-handling scenes.

| Scene | What Shakes | Choice to Pick First |
| --- | --- | --- |
| the same payment inquiry is classified as `refund_request` on one day and `cancel_status` on another | internal label boundary | review fine-tuning |
| answer format is right, but this month's refund policy amount is often wrong | latest policy information | review RAG or external data connection |
| output format is mostly right, but the first sentence tone is a little stiff | input instruction and style | review prompt adjustment |
| in medical summaries, the way drug names, dosages, and contraindication expressions are kept differs every time | domain expression rules | review fine-tuning |

The scenes where fine-tuning should be reviewed first here are the first and fourth. Both are not expression problems in a single question, but problems where the same internal criteria or expression rules must be repeatedly kept across many inputs.

The second scene is a problem of latest policy information. In this case, even if fine-tuning is done, it may not automatically follow changes after the training point, so it is natural to review RAG or external data connection first.

The third scene is likely solvable by adjusting only input instructions rather than changing the model's internal habits. In that case, improving the prompt more briefly and clearly has lower cost and risk than thinking of fine-tuning first.

The criteria to hold in this exercise are as follows.

- If internal label boundaries repeatedly shake, it is a fine-tuning candidate.
- If latest facts or policy values are wrong, it is a RAG or external information connection candidate.
- If only one or two sentences of tone or format shake, it is a prompt adjustment candidate.
- If domain expression rules repeatedly shake, it is a fine-tuning candidate.

In other words, it is safer to understand fine-tuning often as `the power to make the response method fit the work form better` rather than `the power to create new correct answers`.

Fine-tuning connects to the transfer learning flow that was widely used even before LLMs. The method of first making a large foundation model and then increasing purpose fit with smaller task data has been repeated in modern NLP and vision.

Therefore, it is helpful to understand fine-tuning not as an unfamiliar invention that suddenly appeared in the LLM era, but as the result of a broader appearance of the flow `make a large base and later adapt it by purpose`.

## Checklist
- Can you explain fine-tuning as `a stage that places purpose-specific adjustment on top of a general-purpose base`?
- Can you distinguish what prompts, fine-tuning, and RAG each change?
- Are you ready to read efficient adjustment as a problem of `how to reduce the cost when fine-tuning is needed`?

## Sources and References

- Jeremy Howard, Sebastian Ruder, `Universal Language Model Fine-tuning for Text Classification`, arXiv, 2018, accessed 2026-07-19. [https://arxiv.org/abs/1801.06146](https://arxiv.org/abs/1801.06146){: target="_blank" rel="noopener noreferrer" }
- Neil Houlsby et al., `Parameter-Efficient Transfer Learning for NLP`, ICML, 2019, accessed 2026-07-19. [https://proceedings.mlr.press/v97/houlsby19a.html](https://proceedings.mlr.press/v97/houlsby19a.html){: target="_blank" rel="noopener noreferrer" }
- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, accessed 2026-07-19. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }
