# P6-1.3 Generation Is Repeated Candidate Distributions And Selection

> Section ID: `P6-1.3`
> Version: `v2026.07.22`

The core sense of generative models covered in Part 5 was the flow of `creating candidates and choosing one of them`. An LLM also does not pull out a finished sentence all at once. It creates the next candidates from the current context, appends the selected piece back to the context, and then creates the next candidates again.

## Look At The Next Candidate Before The Finished Sentence

Users usually see the completed answer. That makes it easy to feel as if the LLM retrieved a sentence stored somewhere. But to understand generation, we must put the finished answer aside for a moment and first ask, `What can come next in the current context?`

For example, after the context `The refund policy`, many candidates can follow. Candidates such as `purchase`, `item`, `customer`, and `receipt` can all make sense, but they are not equally plausible. The model assigns relative scores to these candidates and chooses the actual next piece according to a selection rule. Once that piece is attached, the context changes, and the next candidate scores change again in the changed context.

Here, `candidate distribution` means that candidates are not placed with the same likelihood. Some candidates are strong, and some are weak. Generation is not looking at this distribution once and stopping. It is a repetition of attaching the selected piece to the context and creating a new distribution again.

## A Small Candidate-Selection Table

One small scene of creating candidates and choosing one of them can look like this.

| Current context | Candidates and relative scores | Selection method | Selection result |
| --- | --- | --- | --- |
| `The refund policy` | `purchase 0.46`, `item 0.21`, `receipt 0.18`, `customer 0.15` | Choose the highest score | `purchase` |
| `The refund policy purchase` | `after 0.38`, `date 0.24`, `history 0.20`, `cancel 0.18` | Do not always choose only rank 1; choose one candidate | `after` |
| `The refund policy purchase after` | `14 days 0.44`, `7 days 0.33`, `30 days 0.23` | Stability-first selection | `14 days` |

This table is not the actual internal implementation of an LLM. The numbers are examples for showing stronger and weaker candidates. Read `0.46` only as meaning that `purchase` was more plausible than the other candidates. The learning needed here is the sense that generation is not `pulling out a finished answer`, but `a repeated flow of candidate distributions and selection`. With this sense, tokens, next-token prediction, temperature, and sampling later become tools for reading the generation process, not just settings.

The selection result becomes the input to the next calculation. So what was selected earlier changes the later candidates.

| Piece selected earlier | New context | Candidates that become stronger | Candidates that become weaker |
| --- | --- | --- | --- |
| `purchase` | `The refund policy purchase` | `after`, `date`, `cancel` | `customer`, `inquiry` |
| `customer` | `The refund policy customer` | `inquiry`, `center`, `support` | `7 days`, `14 days` |

Even with the same starting sentence, once one selection differs, the direction of the next candidates changes. That is why generation should be read not as retrieval of a fixed sentence, but as a process that keeps updating the current context and recalculating the next candidates.

```mermaid
--8<-- "assets/part-06/chapter-01/p6-c01-s03-generation-loop-en.mmd"
```

## Cases And Examples

Even a small change in the user request changes the candidate distribution.

| User request | Current context | Candidates likely to strengthen | Candidates likely to weaken |
| --- | --- | --- | --- |
| `Write a short apology.` | `We apologize for` | `the inconvenience`, `this issue` | `therefore`, `when calculated` |
| `Explain the refund conditions.` | `Refunds are available after` | `7 days`, `14 days`, `business days` | `thank you`, `attachment` |
| `Calculate it in Python code.` | `total =` | `price`, `sum`, `amount` | `hello`, `the policy is` |

This table is not data showing actual model scores. What readers should hold onto is the relation that `context changes candidates`. Even with the same LLM, if the request, the token selected earlier, the provided document, or the system instruction changes, the strength of the next candidates changes.

## Apply It Directly

Compare the following two starting sentences.

| Starting context | Predict the next candidates | Check explanation |
| --- | --- | --- |
| `The cause of the shipping delay is` | Explanation candidates such as `snowstorm`, `logistics`, `inventory`, `customs` | Nouns that explain the cause are likely to become stronger. |
| `About the shipping delay, tell the customer` | Action candidates such as `apologize`, `explain`, `inform`, `send` | Candidates leading into a customer-response sentence are likely to become stronger. |

Both contexts talk about a shipping delay, but the role of what is needed next differs. The first context leads into an explanation of the cause, and the second leads into a customer-response action. When context changes like this, the candidate distribution changes, and when the candidate distribution changes, the actual generated result also changes.

## Exercises And Examples

Compare how the next candidates may differ in the following two contexts.

| Current context | Candidates likely to become stronger | Reason |
| --- | --- | --- |
| `If we summarize the meeting notes,` | `decisions`, `action items`, `issues` | A summary is likely to continue with key items. |
| `If we translate the meeting notes,` | `The`, `Meeting`, `Summary` | A translation request is likely to continue with the first expression in another language. |

The two sentences begin similarly, but `summarize` and `translate` create different next-candidate distributions. In Part 6, context is not simply a bundle of preceding characters. It is a condition that changes the next-candidate scores.

When we ask what unit candidates are created in for text generation, the answer is the token. So the token is not the starting point of Part 6. It is the computational unit that appears after we have first held onto generative-AI artifacts and the LLM's candidate-selection flow.

## Checklist

- You can explain generation as repeated candidate distributions and selection.
- You can explain why the idea of pulling out a finished sentence all at once is insufficient.
- You can explain why tokens appear as the basic unit of candidate calculation.
