# P3-6.3 How Should We Distinguish Human-Made Features from Representations Learned by the Model

> Section ID: `P3-6.3`
> Version: `v2026.09.19`

A model can receive raw measurements in order without handcrafted summaries. What must be specified is the sample unit, the information available by the prediction time, and the question to answer. **Input boundaries are necessary; computing means, slopes, and tokens is optional.**

## Two Input Paths from the Same Raw Values

Consider a fictional completed action with four sensor observations `[1, 3, 3, 1]`, measured at regular intervals. At action completion, we use these four values to predict whether later inspection will be needed. Both paths use the same data and prediction time.

| Aspect | Path using summary features | Path preserving ordered values |
| --- | --- | --- |
| Human-specified input | Mean 2, last−first 0 | [1, 3, 3, 1], with order and measurement interval |
| Information retained | Overall level and endpoint difference | Position-specific values rising in the middle |
| Example of learning | Learn the relationship between these two features and the outcome | A sequence-processing neural network learns internal values that distinguish patterns across positions |
| Further human decisions | Summary rules, units, missing-data handling | Length, order, intervals, missing-data handling, and input format |

The second path does not require computing means or tokens first. It still requires more than supplying an arbitrary file: specify units, order, and valid observation boundaries, then prepare the array format the model accepts. A combined design can also supply both sequences and summary features.

`[3, 1, 1, 3]` also has mean 2 and last−first 0. A model receiving only those two summaries cannot distinguish the actions from its inputs. Ordered inputs remain different, preserving information for distinguishing them. Whether a model learns to use it effectively depends on data, learning objective, and model. Information availability and useful performance are separate judgments.

## Distinguish Specified Calculations from Learned Calculations

A mean formula or fixed `UP/FLAT/DOWN` boundaries are explicit human rules. Representation learning instead transforms inputs into internal values through parameters adjusted during learning. People specify objectives and model structure, but need not manually name each internal value “late decline,” for example. Learned values are not guaranteed to be as directly interpretable as handcrafted features.

Not every model learns new internal representations. Some learn outcome relationships from supplied features. Conversely, models that learn internal representations can receive handcrafted features. Who summarized the input and what the model learns are separate questions.

In the previous section, “intermediate representation” meant segments or tokens built with human-defined rules. Elsewhere, it can mean learned values inside a neural network. Check whether the term refers to **input created by fixed rules or internal values adjusted through learning**. The later deep-learning Part explains the learning mechanisms.

## Images and Documents Also Need Input Boundaries

| Data | Examples of human boundary decisions | Possible input paths |
| --- | --- | --- |
| Sensor action | Completed action or latest 30 seconds; which sensors | Summary features or ordered measurements |
| Image | Whole photo or crop; capture time and subject | Color summaries or a prepared pixel array |
| Document | Whole document or paragraph; which version is available | Word-count summaries or ordered text tokens |

Text tokens are language-processing units used for model input, not the slope-token rules of the preceding section. Neither path should include outcomes produced after prediction time. Learning internal representations also cannot faithfully restore missing records or details discarded before input.

## Human Decisions in Both Paths {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-3-mermaid-01-en.mmd"
```

Correct this statement: “Deep learning requires making means, converting them to tokens, and then feeding a neural network.” The answer is: “First specify the sample, prediction time, and input scope, then choose suitable summaries, ordered raw values, or tokens.” Omitting handcrafted summaries does not remove the need for an input specification.

If both arrays are reduced to the single mean 2, can a larger neural network recover the original order? That input alone cannot determine which array it was. Preserve necessary order information when designing the input.

## Checklist

- Can you separate required input boundaries from optional handcrafted summaries?
- Can you express the same raw values through both paths and explain what each loses?
- Can you distinguish fixed calculation rules from learned internal calculations?
- Can you define input scope for an image and a document?

Related concepts: [input specification](/AiBook/en/reference/concept-glossary-alpha/m/#model-input), [representation learning](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-representation-learning).

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }. Used for feature, feature engineering, and representation terminology. The arrays and input paths are illustrative examples created here. / 2026-09-19
