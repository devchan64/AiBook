# P6-1.1 Viewing Generative-AI Output As An Artifact To Review

> Section ID: `P6-1.1`
> Version: `v2026.07.23`

In Part 5, we held onto the sense that a generative model creates a candidate distribution and selects an actual output through sampling. Part 6 moves that sense into the experience of using real generative-AI services.

Unlike a model that returns only one category or one number, generative AI creates artifacts that users must read, review, and revise. Those artifacts can take many forms, such as sentences, code, image descriptions, and audio scripts, but Part 6 uses text-based generative AI as the representative path.

| Use scene | What the model returns | What the user must do |
| --- | --- | --- |
| Is this message spam? | A classification result such as `spam` or `normal` | Check whether it was classified by the right standard. |
| What will demand be next month? | A numeric prediction | Check the error range and the supporting data. |
| Write a reply to send to this customer. | A sentence artifact | Review facts, tone, evidence, omissions, and risky wording together. |

This difference matters. Even if a generated result looks like a plausible sentence, it is not a conclusion that can simply be trusted. Understanding generative AI means looking not only at how the model creates artifacts, but also at what standards should be used to review and reinforce those artifacts.

## Artifacts Do Not Fit One Standard Alone

Classification results and numeric predictions can also be wrong. Their output forms, however, are relatively narrow. It is easier to set the checking standard first: whether something is `spam`, or how far a prediction is from the actual value. Generative-AI artifacts are different. A single sentence can contain factual description, a promise, policy interpretation, and tone, so we must first separate what needs to be checked.

For example, suppose a reply says, `We are sorry for the shipping delay. We will resend it today.` The sentence sounds natural, but it still contains items that must be checked.

| Check item | Check question | Problem if sent as-is |
| --- | --- | --- |
| Fact | Can it actually be resent today? | Customer dissatisfaction grows if the promise cannot be kept. |
| Authority | Does the support agent have authority to confirm reshipment? | It becomes a compensation promise made without internal approval. |
| Omission | Are order number, carrier, or expected arrival date needed? | The customer lacks information for deciding the next action. |
| Tone | Does it match the company's response standard? | It may sound too definitive, or the apology may cover too broad a responsibility. |

So a generative-AI artifact is not sufficient just because it is `a readable sentence`. Apart from the artifact's naturalness, the user must check facts, authority, omissions, and risky expressions. This is also why Part 6 later discusses prompts, RAG, tool use, evaluation, and operation records. To use generated results well, we must read not only generation itself but also review and reinforcement structures.

## Cases And Examples

The difference becomes clearer if the same customer request is turned into three model outputs.

| Request | Output form | Review standard |
| --- | --- | --- |
| `Is this inquiry a refund request?` | `refund request` or `general inquiry` | Check whether the label standard and exception conditions are correct. |
| `How likely is this customer to receive a refund?` | A score such as `0.72` | Check the supporting data and threshold behind the score. |
| `Write a reply to send to this customer.` | A draft reply made of several sentences | Check facts, policy, authority, omissions, and tone together. |

All three outputs are produced by AI, but the reader must read them differently. For the first, we check whether the label matches the standard. For the second, we check what data and criteria produced the score. For the third, we read the whole sentence while separating multiple standards at the same time.

This reveals why generative-AI artifacts can feel difficult. When a sentence sounds natural, people can easily feel as if review has already finished. But a natural sentence is not the result of review. It is the target of review. Inside the sentence, verified facts, unverified guesses, plausible wording attached by the model, and promises that require actual execution authority can be mixed together.

## Apply It Directly

Mark the following draft reply by separating it into three review standards.

> Hello. The item you ordered has already been processed for reshipment and is expected to arrive tomorrow afternoon. We are sorry for the inconvenience.

| Sentence fragment | Review standard to attach first | Check explanation |
| --- | --- | --- |
| `has already been processed for reshipment` | fact, authority | Check whether there is an actual reshipment record and whether the support agent may confirm this status. |
| `is expected to arrive tomorrow afternoon` | fact, evidence | Do not state this definitively without carrier tracking information. |
| `We are sorry for the inconvenience` | tone, policy | The apology itself sounds natural, but it must match the company's response standard and responsibility boundary. |

Even this small classification shows why generated results are hard to use as-is. The more sentence-like the output is, the broader the review standards become.

## Exercises And Examples

When you see the following three outputs, first think of what the user must additionally check. The right column gives the checking explanation.

| Output | Additional item to check |
| --- | --- |
| `This is a normal transaction.` | Classification standard and exceptional transaction conditions |
| `Next week's sales volume will be 1,240 units.` | Prediction error range and supporting data period |
| `Refunds are processed within three business days.` | Actual refund policy, differences by payment method, and customer order status |

The first and second outputs also need review, but generative-AI artifacts broaden the set of review items. Facts, policy, authority, and tone can be mixed together inside one sentence.

The standard to keep from this section is clear. Generative-AI output is not `an answer mark`. It is `an artifact that must be reviewed`. That is why Part 6 does not stop at whether generated results sound natural. It continues into the evidence used to reinforce those results and the records used to check them again.

## Checklist

- You can explain how generative-AI output differs from classification results or numeric predictions.
- You can explain why a generated result still needs review even when it looks natural.
- You can explain why Part 6 should begin from generated artifacts and the problem of review.
