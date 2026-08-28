# P5-15.1 What Changes When We Read Generative AI Through Deep Learning

> Section ID: `P5-15.1`
> Version: `v2026.08.28`

When recording this transition, separate `input_context`, `classification_label`, `candidate_output_form`, `review_criteria`, and `user_visible_artifact`. Then generative AI appears not as a kind of labeler that replaces classification, but as a flow that creates an artifact users can read and review.

In P5-14, we saw that the Transformer directly revisits long context, computes relationships among many tokens at once, and stabilizes deep repeated blocks. The last question in Part 5 is why this structure prepares us to understand generative AI. This question is not only about `what the model computes`; it is also about `what form the computed result takes when it reaches the user`.

Even for deep-learning models, the standard changes when the output is not `one label` or `one score`, but an artifact a user can read and revise, such as a sentence, image, or code snippet. A label is often used as a signal inside a workflow. A generated artifact can become the answer, report draft, description, or code fragment the user actually reads. So to understand generative AI, we first need to catch the moment when output changes from `result signal` to `result artifact to review`.

Part 5 does not fully explain how to use generative AI. Prompting, tokens, GPT, RAG, tool use, and agents are treated in depth in Part 6. Here we prepare one viewpoint needed before that.

A classification model often summarizes an input as a label or a score. Generative AI goes one step further and tries to compose an output artifact suited to the current input. So reading generative AI through deep learning first means changing the question from `which label is correct?` to `what output artifact is being produced in a way that fits this context?`

## Labels Become Output Artifacts

A classification model usually chooses a category for an input.

| Input scene | What a classification model mainly returns |
| --- | --- |
| maintenance report saying `temperature recovered but pressure is still fluctuating` | a state label such as `partial recovery` or `residual anomaly` |
| equipment photo | an object label such as `mixing tank`, `valve`, or `gauge panel` |
| customer inquiry | an inquiry label such as `refund request`, `incident report`, or `restart request` |

These outputs are useful. Labels help route requests, make statistics, and split risk levels quickly. But the user experience of generative AI moves to the artifact that comes after the label.

| Same input scene | What generative AI can produce | Additional standard to check |
| --- | --- | --- |
| maintenance report | a summary sentence that includes both recovery state and remaining risk | does it continue naturally without dropping the current state? |
| equipment photo | a description or alt-text draft | do the main object and relationships in the photo remain in the description? |
| customer inquiry | a response draft with restart steps, clarification questions, and warnings | is it structured so a user can review and revise it? |

So generative AI cannot be judged only by whether it chose the correct label. We also need to ask whether the output fits the current context, continues naturally, and can be reviewed as an actual artifact. From this point, model evaluation includes not only `right or wrong`, but also standards such as `contextual fit`, `enough specificity`, and `reviewable form`.

## What Producing the Output Means

`Producing the output itself` does not mean the model invents anything without constraint. From a deep-learning viewpoint, it means the model uses patterns, representation structures, and continuation possibilities learned from data to compose a new result.

For text generation, we look at the following.

- what expressions naturally follow others
- what answer structures are common for a request
- what warning phrases tend to appear with follow-up actions

For image generation, we look at the following.

- what colors, outlines, and layouts tend to appear together
- what part structures tend to look like one object
- what styles and compositions feel natural under the same condition

The important point is that generative AI should not be read only as a system that pulls one answer from an answer sheet. It appears as a model experience that composes an output artifact suited to the current input from learned patterns.

This difference becomes clearer where the output is actually used.

| Output form | Easy first question | Additional question from the generative-AI viewpoint |
| --- | --- | --- |
| label | which category is it? | what explanation or action becomes necessary after this label? |
| score | how high or low is it? | what is lost if this score is turned into a sentence for a user? |
| generated artifact | did a result appear? | does it satisfy context, naturalness, and reviewability together? |

In other words, a generative-AI output is both the result of model computation and an object a person must read and judge. Inside the model, the computation still produces numbers such as scores or probabilities for candidates. But in generative AI, those numbers do not stop at choosing one final label. In a text model, they can be used to choose the next token or sentence fragment; in an image diffusion model, they can guide how noise is reduced in the current latent representation and how the next restoration state is reached.

For example, after `before restarting the line`, several expressions can follow: `check the interlock`, `confirm the sensor state`, or `start at low speed first`. The model compares such candidates numerically, but the user does not see a table of numbers as the final result. The user sees guidance sentences formed by one or more selected pieces. For images, the user sees one finished image rather than a list of pixel or component candidates. For that reason, when we read the output side of deep learning, we cannot stop at `which number is largest`; we must also prepare to see how that computation becomes an actual sentence or an image that satisfies the conditions.

This distinction prevents an image from being explained as a list of independently selected visual parts.

## Why Output May Not Be Fixed As One Answer

If a model produces output artifacts, one fixed answer may not be enough. After `batch inspection result`, several continuations can be natural: `reverification is needed`, `resume after operator confirmation`, or `measure again in 10 minutes`.

Therefore, the last chapter of Part 5 splits this flow into six sections. P5-15.1 settles the shift in output viewpoint. P5-15.2 looks at how a model keeps the relative plausibility of possible output candidates. P5-15.3 looks at how an actual text output is selected from those candidates. P5-15.4 explains diffusion's noise-prediction learning and repeated restoration. P5-15.5 follows the roles of conditions, attention, and structures such as U-Net and DiT in that restoration. P5-15.6 explains why a VAE moves between images and latent representations in latent diffusion.

So the first preparation for generative AI is not a list of usage tips. We first need to understand why an output artifact may not behave like one fixed answer, and why that artifact becomes something the user must review. Candidate distributions and text selection appear in the next two sections; diffusion's algorithm, structure, and latent representation appear in the following three sections. Prompting practice and service usage are revisited in Part 6 on top of this structural sense.

## From Classification Labels to Reviewable Guidance

Suppose an operations team asks, `tell me the restart order after line shutdown`. A classification model can label this as a `restart procedure inquiry`. That is useful for routing and statistics.

But the user of generative AI usually does not stop at that label. The user expects actual guidance such as `check interlock -> restart at low speed -> confirm sensor stability -> return to normal speed`. The required output is not a category name, but a response draft the user can review.

| Easy first standard | Additional standard from the generative-AI viewpoint |
| --- | --- |
| was the inquiry type classified correctly? | does the actual guidance continue in a way that fits the equipment context? |
| does the response sound plausible? | are action order and risk warnings missing? |
| did it produce a long sentence? | is it structured so a user can review and revise it? |

The result to confirm is that generative AI does not stop at the label `restart procedure inquiry`; it tries to produce an output artifact suited to the current context. How to trust, revise, and attach that artifact to a service is handled in Part 6.

## Comparing Review Criteria for Labels and Artifacts

For each input below, first separate three things yourself. Write what label a classification model would likely return, what output artifact generative AI would produce, and what additional standard should be checked for that artifact. Then compare your answer with the table below.

| Input | Classification viewpoint | Generative-AI viewpoint | Additional check |
| --- | --- | --- | --- |
| `the line stopped because of pressure anomaly` | labels such as `pressure anomaly` or `line stop` | restart checks and risk-warning sentences | does the sequence continue without dangerous omissions? |
| one equipment photo | equipment or part label | photo description, inspection summary, alt-text draft | does it avoid asserting what is not visible? |
| `summarize the meeting notes` | request type such as `summary request` | summary with decisions, tasks, and owners | are decisions and action items separated? |

The point is not that one side is better. Classification and generation solve different questions. But when we use generative AI, the output artifact itself becomes the user experience, so we must pair `what was produced?` with `by what standard should the result be reviewed?`

The difference becomes clearer when the same generated artifact is paired with a review standard.

| Input | Hard-to-review generated artifact | Easier-to-review generated artifact |
| --- | --- | --- |
| `the line stopped because of pressure anomaly` | `Check the problem and restart.` | `Recheck the pressure value, inspect the interlock and possible pipe leakage, and then decide whether to restart at low speed.` |
| `summarize the meeting notes` | `The meeting covered several topics and follow-up action is needed.` | a summary separated into `decisions`, `owners`, and `next actions` |

The check can be summarized this way.

- A state label splits the problem quickly, but a restart guide must include action order and risk warnings.
- A photo label names the object, but a description must separate what is visible from what is not visible.
- A request-type label is useful for workflow classification, but a meeting summary must structure decisions, owners, and action items so the user can verify them.

The result to confirm is that generative AI does not simply make `longer output`; it composes an artifact a user can read and judge. How that artifact remains among several candidates and is selected is continued in the next two sections.

## Checklist

- Can you explain that generative AI creates a different output experience from classification or prediction models?
- Can you say what deep-learning viewpoint Part 5 must prepare before Part 6 analyzes generative AI in depth?
- Can you distinguish labels, scores, and generated artifacts as different output forms?
- Can you explain that producing output means composing a new result from learned patterns, not inventing without constraint?
- Can you explain why candidate distributions and sampling become necessary in the next two sections because generated artifacts may not be fixed as one answer?

## Sources and References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, Chapter 5 `Machine Learning Basics` and Chapter 20 `Deep Generative Models`, checked on 2026-07-21. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Chloe Autio, Reva Schwartz, Jesse Dunietz, Shomik Jain, Martin Stanley, Elham Tabassi, Patrick Hall, Kamie Roberts, `Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile`, NIST AI 600-1, 2024, checked on 2026-07-21. [https://doi.org/10.6028/NIST.AI.600-1](https://doi.org/10.6028/NIST.AI.600-1){: target="_blank" rel="noopener noreferrer" }
- Tom B. Brown et al., `Language Models are Few-Shot Learners`, NeurIPS 2020, checked on 2026-07-21. [https://papers.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html](https://papers.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html){: target="_blank" rel="noopener noreferrer" }
