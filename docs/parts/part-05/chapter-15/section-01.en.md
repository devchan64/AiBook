# P5-15.1 What Does A Generative Model Learn

> Section ID: `P5-15.1`
> Version: `v2026.07.20`

In P5-14.4 and P5-14.5, we saw that the Transformer became a major turning point in parallel processing and direct reference to long context, and that this structure eventually became the foundation for the spread of LLMs and generative AI. The next question now appears.

Then how is a generative model different from a classification model, and what does it actually learn?

A generative model is a model that tries to learn not only which class an input belongs to, but also what patterns the data appears in and what is likely to continue next.

When you need to briefly review again the difference between classification and generation, return to the glossary entry on [generative model](/AiBook/reference/concept-glossary/#generative-model).

## The Question That Separates Generation From Classification

- How is a generative model different from a classification model?
- How can the phrase `it learns the data distribution` be explained to the reader?
- Why is generation often connected to probabilistic output?
- How does this viewpoint continue into LLMs and image-generation models?

The core point that this section needs to close first is that `a generative model does not stop at choosing the correct label, but learns what kind of output is itself natural`.

It is less shaky if this section is fixed first on `the axis of learning a candidate distribution`.

That is, the core of the present chapter is that the handle changes from `which label should be chosen for the input` to `how should the distribution of possible next outputs be learned`.

What is first read here is not output-control procedures such as temperature or sampling settings, but the generative structure in which the model learns what candidate distribution itself.

| What is read in this section now | What is passed to the next section or later Parts |
| --- | --- |
| what patterns and candidate distributions the generative model learns | how, among the learned candidates, the actual output is pulled out through what rule |
| the difference between the question asked by a classification problem and the question asked by a generative problem | how token-level generation settings and service-quality adjustment change |

Sampling and output-quality variation are treated more concretely in the very next section, P5-15.2, and next-token prediction in text generation reconnects in P6-5.1. That is, here we first close `what candidate distribution the generative model itself learns`.

## Standards For Reading Distribution Learning And New Outputs

- You can explain a generative model as `a model that learns data patterns and creates a new sample or the next output`.
- You can compare the difference between classification models and generative models at an introductory level.
- You can explain `next-token prediction` and `image generation` together through one generative viewpoint.
- Through an executable Python example, you can confirm the intuition of generation from a learned distribution.

## From Classification Comparison To Generative Distributions

1. First compare how the question asked by a classification model and the question asked by a generative model are different.
2. Then unpack at an introductory level what the phrase `learning the data distribution` means.
3. Next group text generation and image generation under the same generative viewpoint.
4. Finally organize why the generation problem naturally continues from `what has been learned` to `what is actually sampled or produced`.

## How Are Classification Models And Generative Models Different

A classification model usually answers questions like the following.

- what class is this input?
- should it be immediately shut down, or is it enough just to leave a record?
- is it residual anomaly, or stable recovery?

That is, it centers on mapping the input into some category.

A generative model, by contrast, is closer to questions like the following.

- what kinds of patterns does this data appear in?
- what token is likely to come next after this sentence?
- in this drawing style, what pixel pattern is natural?

That is, a generative model is more directly connected to `the problem of creating a new output itself`.

If we first place this difference in a table, it becomes the following.

| Viewpoint | Classification model | Generative model |
| --- | --- | --- |
| core question | what class is it? | what output is natural? |
| representative output | label, score | next token, new sentence, new image |
| representative examples | alert-grade classification, residual-anomaly judgment | generating an operation-guidance sentence, incident summary, equipment image generation |

If we split the same scene into the two approaches, the difference becomes more direct.

| The same input scene | What the classification model outputs first | What the generative model outputs first |
| --- | --- | --- |
| an operation inquiry saying `tell me the restart order after line shutdown` | an inquiry-type label such as `restart procedure request` | an actual response sentence such as `After checking the interlock, begin low-speed restart.` |
| a maintenance-report sentence saying `temperature has recovered, but pressure fluctuation remains` | a status label such as `partial recovery` or `residual anomaly` | a summary sentence that contains both the recovery state and the remaining risk |
| an equipment-scene photograph | an equipment-type label such as `mixing tank` | an equipment-description phrase or an alternative-text draft |

That is, classification chooses first `how to categorize it`, while generation directly handles `what should actually be said or created`.

## What Does It Mean To `Learn The Data Distribution`

Readers can feel immediate difficulty at the word `distribution`. Here it is best to first hold it as `a statistical feel for what patterns appear often together and what combinations are natural`.

`To learn the data distribution means that the model learns a statistical feel for what patterns appear often and what combinations are natural.`

For example, in text, the model learns:

- what words often come after what words
- what sentence structures are natural

In images, it can learn:

- what colors and shapes often appear together
- what partial structures make up a natural object

If the reader is to hold this again through a practical scene, it helps to divide at minimum `what has been seen a lot`, `what appears naturally together`, and `what should be checked in the result`.

| Data type | Pattern the model sees a lot | What should be checked first in the result |
| --- | --- | --- |
| operation sentences | what action phrases often continue, and what warning-sentence structures repeat | whether the next sentence and guidance tone continue in a way that fits the current alert context |
| equipment images | what colors, outlines, and layouts often appear together | whether the composition and form remain natural and do not break awkwardly |
| field-support responses | what answer length and structure are often used for each question type | whether the order of the response and the placement of warning phrases change appropriately for the situation |

That is, a generative model is closer to learning the data pattern itself more broadly than to being `a model that only gets the correct label`.

## Why Is Generation Often Connected To Probabilistic Output

Generation often does not have only one correct answer.

For example:

- the next word after a sentence may not be only one possibility
- there can be several natural ways to draw a picture
- a summary sentence can also be phrased in several natural ways

So a generative model often deals with `among several possible outputs, which one is more plausible`. Because of this, ideas such as probability, sampling, and temperature naturally follow along.

`Generation is often not a matter of selecting one correct answer, but a matter of deciding which one among several plausible candidates to produce.`

## How Are LLMs And Image Generation Grouped Under The Same View

On the surface, text generation and image generation look very different. But from the viewpoint of generative models, they share common ground.

- both learn data patterns
- both create new outputs
- both can be connected to probabilistic choice or sampling

That is, generative AI refers to models that create plausible new outputs in many data domains.

### Text Generation

It continues a sentence by predicting the next token.

### Image Generation

It builds an image by gradually constructing pixels or latent representations.

Though the domains differ, they share the common view that `a model learns patterns and then creates a new result`.

## If We Draw This Very Simply

```mermaid
--8<-- "assets/part-05/chapter-15/generative-model-flow-en.mmd"
```

This diagram compresses the generative model at the broadest level.

## Cases And Examples

| Situation | Question directly handled by the generative model | What output can actually vary |
| --- | --- | --- |
| operation-guidance sentence generation | what action phrase is more natural to come next now | the sentence choice and the tone of the following guidance |
| field-support response | what answer structure fits the current equipment context | the order of explanation, the length, and the placement of warning phrases |
| equipment-image generation | what visual combination looks plausible | composition, color, layout, and emphasized target |

The diagram below regroups the three cases of this section not as `the problem of choosing one correct label`, but as `the problem of creating a natural output among several candidates`.

```mermaid
--8<-- "assets/part-05/chapter-15/generative-task-flow-en.mmd"
```

### Representative Case. Predicting The Next Word

Let us think about the scene of continuing an operation-notice sentence after the prefix `Batch inspection result`. A person can also think of several follow-up action phrases such as `reverification is required`, `resume after supervisor confirmation`, or `remeasure in 10 minutes`, but it is easy at first to feel as if there must be only one correct answer. Yet in real operation text, the natural next phrase differs according to the alert context, the field state, and the guidance tone. For example, if sensor anomalies are repeated, `reverification is required` fits better, while if action has already begun, `resume after supervisor confirmation` can sound more natural. It is hard to capture this difference if we use only a method that chooses one correct label as in classification. A generative model is exactly a model that learns the relative plausibility of several such candidates together, and raises the more natural ones as output candidates in the current context.

So the result to confirm in this case is that the phrase that can come after `Batch inspection result` remains not as one correct answer, but as several follow-up action candidates, and that the generative model learns their relative plausibility together.

The same viewpoint extends directly to field-support responses and image generation. But the core point to hold in this section is not the domain name, but `whether the model learns not one correct answer but the whole candidate distribution that is natural in the current context`.

| Standard that is easy for a person to see first | Standard to reread from the generative-model viewpoint |
| --- | --- |
| it is easy to feel that the explanation ends once one correct answer is found | the real core is that the whole distribution of what candidates are how plausible is learned together |
| it feels enough to look only at one most likely candidate | behind the highest candidate, other natural candidates must also remain for the generative intuition to close |
| text generation and image generation feel like completely different problems | although the domains differ, they share the structure of `learning patterns and making a new output` through candidate-distribution learning |

If we place the three cases together, the core of a generative model is not `it chooses one correct answer`, but `it learns the full candidate space of outputs that can be natural in the current context`.

If we divide the same three cases again from the viewpoint of operational judgment, it becomes more direct why it is insufficient to read a generative model as `picking one correct sentence`.

| Case | What is easy to leave when looking for only one fixed answer | What actually remains when we look up to the candidate distribution |
| --- | --- | --- |
| operation-guidance sentence generation | it becomes easy to repeat only one template phrase for every alert | even under the same alert, several follow-up phrase candidates such as reverification, remeasurement, or supervisor confirmation remain together |
| field-support response | it becomes easy to output one SOP sentence as if it were the only answer | different answer-structure candidates such as pressure-release first, interlock-check first, or warning-first remain together |
| equipment-image generation | it becomes easy to imagine only one correct picture in mind | even with the same prompt, the visual candidate space remains together, such as valve emphasis, warning-beacon emphasis, or piping-layout difference |

If we pause once here and briefly fix `when should we first recall the generative viewpoint rather than only label prediction`, the learning stage and the output stage mix less when moving into the next sampling section.

| Question to recall first | Why the generative-model viewpoint is needed first | What continues in the very next section |
| --- | --- | --- |
| why are several natural answers possible instead of only one correct answer? | because a generative problem deals with the candidate distribution itself rather than only label selection | which one among those candidates will actually be sampled |
| why are LLMs and image generation explained on the same axis? | because, though the domains differ, they share the structure of learning patterns and producing new outputs | sampling and diversity control |
| why is classification-style explanation alone insufficient for operation-guidance generation or field-support responses? | because the output is not a category name but an actual sentence, image, or composition | output-selection procedures and user-experience differences |

## Practice And Example

The goal of this example is to confirm how a generative model learns, as a distribution, `which follow-up action phrase often continued after each alert type`. We are not yet doing actual sampling, but rather first fixing from the viewpoint of operation records what it means to say the model learned something.

Before reading the code, if we look together first at the following three values, the question of this section spreads less.

| Value to look at first | Why it should be looked at first |
| --- | --- |
| `probabilities` | because it shows that the generative model holds `what often continued next` not as one label, but as a distribution |
| `most_likely` | because it lets us see together what the most plausible candidate is and how that differs from the full distribution |
| the difference between `temperature_alert` and `seal_edge_alert` | because it confirms that even the same generative model learns completely different candidate distributions when the context changes |

Input:

- two different kinds of operation-alert context
- counts of the follow-up action phrases that often continued in the past under each context

Output:

- the probability distribution of follow-up actions by alert type
- the most likely follow-up action in each alert

Problem situation:

- when we say a generative model learned something, in actual operation records we need first to understand how `the distribution of phrases that could follow next` should be read

Concepts to confirm:

- a generative model learns the candidate distribution itself rather than deciding only one candidate
- even in the same context, there is not just one follow-up action, but several phrases that remain together with relative weights
- when the context changes, both the most likely candidate and the whole distribution change together

Before looking at the code, it helps to predict the two alert contexts by splitting them into `a reading that chooses only one label` and `a reading that keeps the candidate distribution`.

| Context | Misunderstanding that can easily arise if we read by choosing only one label | Change to predict first from the generative-model viewpoint |
| --- | --- | --- |
| `temperature_alert` | it is easy to feel that it is enough to know only `the one most common follow-up action` | even if the first candidate is highest, the other inspection phrases should also remain inside the distribution |
| `seal_edge_alert` | it is easy to feel that it will produce an operation response similar to the previous alert | when the context changes, both the highest candidate and the whole candidate set should change together |
| both alerts | it is easy to feel that once `most_likely` is seen, the explanation of generation is finished | only when we also look at `probabilities` can we explain what the model learned |

The difference we actually want to confirm here is also clear. A reading that carries only `most_likely` easily leaves only one template like `this phrase for this alert`, while a reading that also sees `probabilities` keeps as a candidate set `what inspection order and warning phrases are all possible even under the same alert`. That is, a generative model should be read as learning the `space of operation responses` together instead of fixing one answer.

The table below keeps the same situation as an interpretive case instead of aggregating it again in code. When candidate phrases and record counts are already given, Python easily ends up repeating only the counting step, so a table and explanation are enough for this section.

| Alert context | Follow-up-action candidate | Record count | Share of records | What to read from the generative-model viewpoint |
| --- | --- | ---: | ---: | --- |
| temperature alert | First check the coolant flow | 14 | 0.50 | It is the most frequent continuation, but not the only answer |
| temperature alert | Check the heat-exchanger fan state | 9 | 0.32 | It remains as a supporting candidate in the same context |
| temperature alert | Review sensor calibration again | 5 | 0.18 | Even a lower-weight candidate does not disappear from the candidate space |
| seal-edge alert | Readjust the sealing pressure | 13 | 0.52 | When the context changes, the highest candidate itself changes |
| seal-edge alert | Retune the film tension | 8 | 0.32 | A different inspection axis remains in the candidate distribution |
| seal-edge alert | Inspect blade wear state | 4 | 0.16 | A lower candidate can still lead to a follow-up explanation or additional check |

The first thing to read in this table is not just the largest number, such as `0.50` or `0.52`. In the temperature alert, coolant-flow inspection, fan-state checking, and sensor-calibration review form one candidate space. In the seal-edge alert, sealing pressure, film tension, and blade wear form a different candidate space. The generative-model viewpoint is about reading this difference between candidate spaces.

| Output to look at first | What this output means | What changes if you vary it |
| --- | --- | --- |
| `probabilities` of `temperature_alert` | in the temperature-alert context, `check coolant flow` continues most often, but other actions also remain together in the distribution | if the record weights change, the most likely action and the width of the distribution both change together |
| `probabilities` of `seal_edge_alert` | in the seal-edge alert, a completely different follow-up action set becomes central | if more context types are added, it becomes clearer that the generative model learns different phrase distributions for each context |
| `most_likely` of each context | it means that, separately from the full distribution, one highest-probability candidate can also be read by itself | if we fix our reading on only one candidate, we miss the possibility of the other candidates still remaining behind it |

| Standard for designing operation responses | Easy judgment if we look only at `most_likely` | Judgment that changes after reading `probabilities` together |
| --- | --- | --- |
| temperature-alert guidance | it becomes easy to output only `check coolant flow` as one fixed response | we are led to leave `check fan state` and `review sensor calibration again` together as further candidates, and to attach them later according to the situation |
| seal-edge-alert guidance | it becomes easy to feel that a similar inspection phrase can be reused from the previous alert | we are led to maintain a completely different candidate set such as sealing pressure, film tension, and blade wear |

If we translate this difference more directly into an operation-guidance design decision, it can be read as the difference between `locking immediately one most likely candidate into a fixed template` and `leaving the candidate space open and later adjusting the follow-up sentence and warning placement`.

| Example context | Less harmful reading if we hold only `most_likely` | More dangerous reading if we hold only `most_likely` | Safer next judgment after reading `probabilities` together |
| --- | --- | --- | --- |
| `temperature_alert` | we can place `check coolant flow` as the first sentence and stop there | we may throw away fan-state and sensor-calibration-recheck candidates, freezing the follow-up inspection order into one template | we start with coolant-flow check, but keep fan-state and sensor-calibration-recheck as follow-up sentence candidates and adjust the guidance by situation |
| `seal_edge_alert` | we can present `readjust the sealing pressure` as the default action | by reusing a response tone similar to a temperature alert, we may attach film-tension and blade-wear checks too late or miss them | we place sealing-pressure readjustment as the first candidate, but keep film tension and blade wear in the same candidate space so other equipment causes can follow immediately |

- a generative model does not memorize `what comes next` as one sentence, but organizes as a distribution `what followed how often in this context`
- even if there is one most likely candidate, other candidates still remain behind it together
- therefore, if we look only at `most_likely`, it becomes easy to read generation as if it were classification, but only when we also look at `probabilities` does the candidate space learned by the generative model appear
- only by seeing this difference do we read a generative problem not as `choosing one correct label`, but as `learning a candidate distribution`

If we translate this into an operation-support system, a system that looks only at `most_likely` is easy to read like a template that repeats one fixed phrase for each alert, while a system that also sees `probabilities` is closer to a structure that can prepare several candidate combinations of inspection order, warning phrase, and follow-up guidance even under the same alert. What the generative model learns is exactly this `space of candidate responses`, and at the actual output stage, how narrowly to reduce that space and how much to leave open is decided again by sampling in the next section.

This example is better not to read once and end, but to continue directly by checking what values can be changed to make the feel of the candidate distribution clearer.

| Output signal seen first | Change to try right now | Conclusion not to rush to from this example alone |
| --- | --- | --- |
| in the temperature alert, one candidate is highest at 0.5 | increase or decrease the first candidate count and see how quickly the most likely action changes | do not conclude that because there is a highest candidate, generation is already deterministic |
| in the seal alert, three candidates remain together | add or remove more candidates and see how the width of the distribution changes | do not conclude that the mere fact that several candidates remain automatically means good operational quality |
| when the context changes, the whole distribution changes | add another alert type and see how the phrase distribution splits further | do not immediately generalize the whole learning of a large-scale generative model from just these two simple operation examples |

## Checklist

- Can you explain that a generative model solves a different kind of question from a classification model?
- Can you say what it means that a generative model learns `what output is natural`?
- Can you explain that a generative model is a model that learns data patterns and makes new samples or the next outputs?
- Can you say that a classification model chooses a category, while a generative model creates the output itself?
- Can you explain that generative problems are often connected to probabilistic output because several plausible answers can exist?
- Can you explain a generative model not only as `a model that makes something`, but as `a model that learns the candidate distribution of what output is natural`?
- Can you distinguish through a case what classification gives first and what generation gives first in the same input scene?
- When reading the next section on sampling, are you ready first to separate `what has been learned` from `what will actually be sampled or produced`?

## Sources And References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Diederik P. Kingma, Max Welling, `Auto-Encoding Variational Bayes`, ICLR 2014, checked on 2026-07-19. [https://arxiv.org/abs/1312.6114](https://arxiv.org/abs/1312.6114){: target="_blank" rel="noopener noreferrer" }
- Ian J. Goodfellow et al., `Generative Adversarial Nets`, NeurIPS 2014, checked on 2026-07-19. [https://papers.nips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html](https://papers.nips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html){: target="_blank" rel="noopener noreferrer" }
