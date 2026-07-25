# P3-6.3 How Should We Distinguish Human-Made Features from Representations Learned by the Model

> Section ID: `P3-6.3`
> Version: `v2026.07.20`

Once we place features together with [intermediate representation](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-intermediate-representation), it becomes important to read clearly where `the human act of deciding the input structure` separates from `the model's act of learning a representation inside that input`. If this distinction becomes blurred, Part 3's feature design can look like outdated preprocessing, or the opposite misunderstanding can arise that the model will decide the structure of the problem for us. The key point is that the two are not in competition. The features and intermediate representations that people make in Part 3 are the act of first deciding `in what input structure the problem will be read`. The representation learned by the model is the act of learning `what patterns inside that input structure better separate useful cases`.

The distinction the reader should hold first is simple. People build the input, and the model learns a representation inside that input. Split as briefly as possible, it looks like this.

| Distinction | What it does |
| --- | --- |
| Human-made features | Leave the comparison axes that fit the question as numerical columns |
| Human-made intermediate representations | Re-bundle order and structure into an input that is easier to read |
| Model-learned representations | Combine useful patterns on its own inside the given input |

So Part 3's responsibility is not `the model will learn a representation, so we can leave things loosely defined`. It is `let us first design the input unit that the model can read`.

## Why Do Humans Build Features First

The reason people build features first is not simply that it is an old-fashioned method. We still have to decide at the level of problem structure what we want to compare now, what difference should matter operationally, and what should still remain in a comparison report.

For example, questions such as `does it collapse sharply in the late phase?`, `has variability grown?`, and `has the difference from the baseline widened?` can already be decided even before a model appears. Only when such questions exist can we explain why features such as averages, slopes, variability, and segment differences are necessary.

| The question fixed first | The feature a person leaves first |
| --- | --- |
| Has the overall level changed? | Average, median |
| Does the structure collapse in the late phase? | Segment difference, decline rate |
| Does it fluctuate more even when the result looks similar? | Standard deviation, variability |
| Is the change from the baseline large? | Difference-from-baseline values |

Without this stage, even if we later use any learning structure, `what we are trying to predict` and `what difference we regard as important` become weak.

## Why Is an Intermediate Representation Needed

An intermediate representation is the bridge between numerical features and the raw log. A token sequence such as `UP, FLAT, DOWN` or a segment-wise expression is still a human-defined representation, but it already has the property of being `an input with order`. So it can preserve structure more directly when numerical features alone may miss it. Here too, the center is not the expectation that the model will create the representation by itself. It is the fact that the human decides once more what input shape will be passed forward.

| The input structure built in Part 3 | What now remains more clearly |
| --- | --- |
| One-action summary vector | The overall level and representative-value differences |
| Segment-wise feature vector | Segment-by-segment changes and fluctuation differences |
| Tokenized segment sequence | The outline of order and repeated patterns |

The important point here is that `an intermediate representation is not itself deep-learning representation learning`. An intermediate representation is an input reconstruction made by a human. Representation learning is the later step where the model learns a more useful internal representation inside that input. In other words, the boundary to hold first in this section is the difference between `the human builds the input` and `the model interprets that input`.

## Where Do Input Specification and Representation Learning Separate

The boundary splits at `does a human first decide what to provide as the input?` versus `does the model itself combine internal patterns inside the given input?`

| Question | What is decided first in input specification | What happens later in representation learning |
| --- | --- | --- |
| What counts as one sample? | Decide whether it is one full action or a recent range | Build an internal representation from the already fixed sample unit |
| What values will be given as input? | Choose an input form such as averages, slopes, or token sequences | Learn useful combinations inside that input |
| How will the raw log be rewritten? | Reconstruct it as a table, vector, or sequence | Capture deeper patterns inside the reconstructed input |

So features and intermediate representations decide `what the input will be`, while representation learning learns `what matters inside that input`.

## Two Common Misunderstandings

The first is the misunderstanding that `if it is deep learning, feature design is unnecessary`. Deep learning can reduce the need for humans to hand-build every feature, but it does not decide sample boundaries and input range on our behalf. Decisions such as whether one full action is one sample, whether a recent range is one sample, and whether to leave the full time series uncut are still the human's responsibility.

The second is the misunderstanding that `if we built features, deep learning is unnecessary`. Human-made features can be a good starting point, but longer sequence dependencies or more complex patterns may be captured better later by representations learned by the model. So feature design and representation learning are closer to sequential stages than to substitutes.

| Misunderstanding | More accurate statement |
| --- | --- |
| If it is deep learning, feature design is unnecessary | Defining the sample and designing the input structure are still needed first |
| If features were built, representation learning is unnecessary | Human-made features are the starting point, and deeper patterns can still be learned later |

## Tying It Again into One Scene

Suppose we have the raw log for one full action.

1. In Part 3, we first define one full action as one sample.
2. We leave averages, slopes, variability, and segment differences as features.
3. If needed, we also create an intermediate representation as a segment sequence such as `UP, FLAT, DOWN`.
4. The tables and sequences built this way become the inputs that the model will read in the later learning stage.
5. After that, the model can learn longer dependencies or more complex combinations inside that input.

Looking at this order makes it clear that feature design is not an outdated preparation step from before deep learning. It is the input-definition stage that is needed first no matter what learning method is used. So the conclusion of this section is not the opposition of `human-made features vs deep learning`, but the question of where `input specification` and `representation learning` separate. Feature design should be read not as obsolete manual labor but as the act of first specifying the input structure on which the later learning stage depends.

## A Small Diagram

The boundary in this section is simple. Humans first design the `input` through features and intermediate representations, and only after receiving that input does the model learn internal representations. They are not competing choices, but consecutive stages.

--8<-- "assets/part-03/chapter-06/p3-6-3-mermaid-01-en.mmd"

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `feature`. Because it explains a feature as an input variable used for prediction, it provides a basis for distinguishing the stage where people first decide what should remain as input variables from the later learning stage. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains feature engineering as the process of turning raw data into a form more useful for learning, it reinforces the point that Part 3's feature design and intermediate-representation design belong to the input-definition stage. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- TensorFlow, `Subword tokenizers`. Because it shows the preprocessing stage in which tokenized sequences are used as model input in the form of token IDs, it supports the explanation that the segment sequences built in Part 3 are `input reconstructions before entering the model`, not `already learned internal representations`. This connection is an interpretation that generalizes the official preprocessing explanation into a time-series example. [https://www.tensorflow.org/text/guide/subwords_tokenizer](https://www.tensorflow.org/text/guide/subwords_tokenizer){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
