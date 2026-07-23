# P5-15.2 Candidate Distributions in Generative Models

> Section ID: `P5-15.2`
> Version: `v2026.07.23`

_Subtitle: Why do generative models keep candidate distributions instead of one answer?_

In P5-15.1, we saw that the output experience changes first when we read generative AI through deep learning. Classification models often return labels or scores, while generative AI produces artifacts such as sentences, images, or code.

Then how should we understand what a generative model prepares for that output?

The core point is that a generative model does not memorize and return one correct answer. It keeps the relative plausibility of possible output candidates. This sense is needed before P5-15.3 can read sampling not as random picking, but as the procedure that pulls an actual output from a candidate distribution.

## A Candidate Distribution Is The Possibility After The Current Input

A classification model usually asks `what class is this input?` A generative model is closer to `what outputs could naturally continue after this input?`

| Viewpoint | Classification model | Generative model |
| --- | --- | --- |
| core question | what class is it? | what output is natural? |
| representative output | label, score | next sentence, new image, code draft |
| first reading standard | highest label | relative plausibility of candidates |

A candidate distribution is a side-by-side view of how plausible each possible continuation is after the current input. For example, if three sentences can all follow `batch inspection result`, the generative model does not store only one of them as the answer. It prepares a form that can compare how natural each candidate is relative to the others.

## How Data Distribution And Candidate Distribution Connect

The word `distribution` can feel difficult at first. Here, read it as a statistical sense of patterns and combinations that often appear together.

For text, the model sees what words and sentence structures often continue. For images, it sees what colors, outlines, and layouts appear together. For operational responses, it sees what action phrases tend to follow a given alert.

This does not mean the model stored every correct sentence. More precisely, it learned enough recurring patterns to calculate which candidates could plausibly continue after the current input.

Two levels need to be separated here. The data distribution is the broad pattern of what combinations often appear across the training data. A candidate distribution is the current-position view of `what can naturally come next, and by how much`, unfolded for this particular input.

| Data type | Pattern the model often sees | What to check in the result |
| --- | --- | --- |
| operation sentences | repeated action phrases and warning structures | whether the next sentence and tone fit the alert context |
| equipment images | colors, outlines, and layouts that appear together | whether composition and form remain natural |
| field-support responses | answer lengths and structures used by request type | whether order and warning placement fit the situation |

## most_likely And probabilities Are Different

In generation, the explanation does not end by finding one most plausible candidate. Several continuations can be natural after the same prefix.

After `batch inspection result`, candidates such as these can all remain possible.

- `reverification is needed`
- `resume after operator confirmation`
- `measure again in 10 minutes`

The highest candidate can be read as `most_likely`. But that is not all the model has kept. Only by reading the full `probabilities` can we see what output space the model learned.

If we look only at `most_likely`, the generative model can start to look like a classification model: one input, one highest answer. If we also read `probabilities`, the second and third candidates remain visible behind the highest one. They may not be selected first right now, but they can still become plausible continuations in the next sentence or another context.

```mermaid
--8<-- "assets/part-05/chapter-15/generative-model-flow-en.mmd"
```

The important point in this diagram is where the interpretation splits after we see the `candidate distribution`. If we read only `most_likely`, one highest candidate remains. If we read `probabilities` together, the candidate space behind the current input remains visible. Sampling in the next section continues from this candidate space into the actual output.

## Cases And Examples

Suppose operation records contain two alert types and follow-up action phrases. In this section, the important task is not the calculation procedure itself, but the sense of reading the distribution, so we first place record counts and distribution interpretation side by side.

| Alert context | Follow-up-action candidate | Record count | Share of records | What to read from the generative-model viewpoint |
| --- | --- | ---: | ---: | --- |
| temperature alert | First check the coolant flow | 14 | 0.50 | It is the most frequent continuation, but not the only answer |
| temperature alert | Check the heat-exchanger fan state | 9 | 0.32 | It remains as a supporting candidate in the same context |
| temperature alert | Review sensor calibration again | 5 | 0.18 | Even a lower-weight candidate does not disappear from the candidate space |
| seal-edge alert | Readjust the sealing pressure | 13 | 0.52 | When the context changes, the highest candidate itself changes |
| seal-edge alert | Retune the film tension | 8 | 0.32 | A different inspection axis remains in the candidate distribution |
| seal-edge alert | Inspect blade wear state | 4 | 0.16 | A lower candidate can still lead to a follow-up explanation or additional check |

The first thing to read is not only the largest number. In the temperature alert, coolant-flow inspection, fan-state checking, and sensor-calibration review form one candidate space. In the seal-edge alert, sealing pressure, film tension, and blade wear form another.

| Example context | Judgment left when holding only `most_likely` | Judgment that changes after reading `probabilities` together |
| --- | --- | --- |
| `temperature_alert` | it is easy to place `check coolant flow` as the first sentence and stop there | fan-state and sensor-calibration recheck remain as follow-up sentence candidates |
| `seal_edge_alert` | it is easy to fix only `readjust the sealing pressure` as the default action | film tension and blade wear remain in the same candidate space for other equipment causes |

A generative model does not memorize `what comes next` as one sentence. It organizes `what followed how often in this context` as a distribution. This is the difference that lets us read generation as learning a candidate distribution rather than choosing one correct label.

## Practice And Example

Read the candidate weights below and make the distinction yourself. First mark the `most_likely` candidate. Then explain why the other two candidates have not disappeared completely.

| Current input | Candidate | Weight |
| --- | --- | ---: |
| `batch inspection result` | `reverification is needed` | 0.46 |
| `batch inspection result` | `resume after operator confirmation` | 0.34 |
| `batch inspection result` | `measure again in 10 minutes` | 0.20 |

In this table, `most_likely` is `reverification is needed`. But the full candidate distribution shows that `resume after operator confirmation` still has a substantial weight, and `measure again in 10 minutes` has not disappeared.

So if we look only at the highest candidate and say `the answer to this input is reverification`, we read the generative model like a classifier. If we read the candidate distribution, we can say: `reverification is the most natural continuation, but operator confirmation and remeasurement also remain possible follow-up phrases in the same context`.

The goal is not to say more candidates are always better. The goal is to separate the highest candidate from the candidate space that remains behind it.

## Checklist

- Can you explain that a generative model solves a different question from a classification model?
- Can you explain `learning the data distribution` as learning patterns and natural combinations that often appear together?
- Can you explain why `most_likely` and `probabilities` are different?
- Can you describe a generative model as a model that learns a candidate distribution of natural outputs, not just as a model that makes something?
- Are you ready to separate `what has been learned` from `what is actually sampled` in the next section?

## Sources And References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, Chapter 20 `Deep Generative Models`, checked on 2026-07-21. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
