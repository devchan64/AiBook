# P5-2.2 Hidden Layers And Representation

> Section ID: `P5-2.2`
> Version: `v2026.07.20`

In P5-2.1, we saw that a multilayer neural network stacks several computation units like perceptrons across multiple layers, so that the input does not go directly to the final judgment but passes through intermediate stages. Now let us make the question a little more concrete.

What exactly is being created in that intermediate stage?

The viewpoint that answers this question is representation. A hidden layer is not the place that simply copies the input values as they are. It is a layer that internally creates intermediate representations that are more favorable for later judgment.

When the idea of representation needs to be reviewed briefly again in later chapters, return to the [representation](/AiBook/en/reference/concept-glossary-alpha/r/#representation) entry in the concept glossary as the baseline.

## The Question Of How Hidden Layers Change Representations

This section organizes the following questions.

- Why is the hidden layer treated as important beyond being a simple intermediate calculation?
- What does it mean to say that representation is learned?
- What does it mean to say that deeper layers create more abstract representations?
- Is it safe to interpret the hidden layer immediately with easy human-readable names?
- Why is deep learning explained together with representation learning?

The larger flow called representation learning is expanded again in P5-10.1 and P5-10.2. Filters and spatial representations in CNNs return in P5-11.1 and P5-11.2, and attention-based representations reconnect in P5-13.1, P5-13.2, and the Transformer main sections from P5-14.1 through P5-14.5. In other words, this section focuses on first holding onto the hidden layer as `an internal representation layer that rewrites the input`.

## Standards For Internal Representations And Intermediate Features

- You can explain the hidden layer as `a representation-transformation layer between input and output`.
- You can understand representation as something like `an internal coordinate system that rewrites the original input`.
- You can say that deeper layers can create more complex and abstract representations.
- You can understand that forcing simple human names onto each hidden node too quickly can create misunderstanding.

## Why Is The Hidden Layer Important

In the traditional machine learning of Part 4, people often selected features directly.

- recent alarm count
- average vibration size
- temperature rise width
- recovery delay time

These features were organized by people and then fed into the model. The model then performed regression or classification on top of them.

But in deep learning, the question changes.

`Instead of having people write every useful feature directly, can the model create intermediate representations internally?`

This is where the hidden layer becomes important. The hidden layer is not a channel that passes the input through unchanged. It can be read as the place where internal representations that are more useful for later judgment are formed.

In other words, deep learning begins to look not only like learning `a decision function`, but also like learning `the representation that is favorable for the decision`.

## What Does Representation Mean

The word representation can sound abstract to readers. Here it is enough to understand it first like this.

`A representation is a way of rewriting the same object inside the model.`

For example, suppose equipment-state data originally enters as four numbers.

- recent alarm count
- average vibration size
- temperature rise width
- recovery delay time

After passing through the hidden layer, the model may no longer keep these in exactly the same form. Instead, it may change them into something more useful internally, such as combinations like the following.

- an internal axis similar to how well normal operation is being maintained
- an internal axis similar to fault-sign risk
- an internal axis similar to how urgently inspection is needed

Of course, actual nodes are not literally given these names. But for reader intuition, it is enough to understand that `the original input is rewritten into a more useful internal coordinate system`.

## Why Is The Phrase Internal Coordinate System Useful

If representation is compared to an internal coordinate system, the role of the hidden layer becomes clearer.

- Objects that are hard to separate in the original input coordinate system
- may become easier to separate in the new coordinate system formed after the hidden layer

In other words, the hidden layer can be seen not as a simple calculation, but as `the process of moving the problem into a coordinate system where it is easier to solve`.

If that is reduced very simply, it becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-02/internal-coordinates-flow-en.mmd"
```

The key point of this diagram is not that `the data itself changes`, but that `the model's internal way of viewing the same data changes`. Examples that looked mixed together in the original coordinate system can be rewritten into a coordinate system where they are easier to separate after passing through the hidden layer. That is why the phrase `internal coordinate system` is useful.

## What Changes As The Layers Become Deeper

One explanation that appears often in deep learning is that `earlier layers catch simpler features, while later layers catch more abstract features`.

This sentence has to be read carefully.

It is usually closer to the following meaning.

- Earlier layers can first capture small combinations or local patterns.
- Later layers can regroup those combinations into larger patterns or more problem-centered representations.

For images, for example, it is often explained like this.

| Layer level | Intuitive explanation |
| --- | --- |
| Earlier layers | Small patterns such as lines, corners, and brightness changes |
| Middle layers | Simple shape combinations |
| Later layers | Larger part structures or representations closer to classification |

Text and tabular data can also be read with the same intuition. Of course, what any particular layer captures depends on the model structure and the data. What matters is that `as the data passes through the layers, an internal representation that is increasingly favorable for the problem can be formed`.

## Why Is It Risky To Interpret The Hidden Layer Too Easily

Readers can easily want to give each hidden-layer node a name right away, such as `this is stability`, `this is risk level`, or `this is warning-light status`. But such interpretation has to be handled carefully.

Hidden-layer representations often have the following characteristics.

- One node may not be responsible for only one meaning.
- Several nodes together may express one property.
- It may be a distributed representation that is hard for people to read intuitively.

In other words, the hidden layer may be not an explicit rule table designed by people, but an internal space where several values share information together.

Because of this, representation learning is powerful, but at the same time interpretation can become difficult.

## Why Is Distributed Representation Important

One reason representation learning is treated as important in the deep-learning literature is distributed representation.

It can be understood like this.

`Important information does not have to sit in only one node. It can be divided across a combination of several nodes.`

For example, instead of one node representing the entire property of an input:

- node A may hold one tendency
- node B may hold another tendency
- node C may become meaningful only when combined with the first two

Because of this structure, neural networks gain expressive power, but it also becomes difficult for a person to conclude that `this one cell is exactly this one thing`.

## Where Does The Responsibility For Feature Design Move

Traditional machine learning models also had feature combinations. But in many cases, people controlled more directly:

- which features to include
- which preprocessing to use
- which distance or splitting rule to apply

By contrast, in a multilayer neural network the model itself takes over more of the work of creating useful intermediate representations.

This difference does not simply mean that the tool changed. It means that some of the responsibility moves from a mode where people adjust boundaries or scores on top of features they chose directly, to a mode where the model creates internal axes inside the hidden layer that are favorable for the judgment. So the key thing to hold in this section is not `which is better, the traditional model or the multilayer neural network`, but the fact that an intermediate representation emerges before the final judgment and makes the problem easier to separate.

## Cases And Examples

### Case 1. Judging Warning States On An Equipment Panel

Imagine a scene where an equipment camera reads a frame containing a control panel and warning light together, and distinguishes states such as `normal monitoring`, `warning check`, or `review immediate stop`. At first, people also do not look at the raw pixels directly. Instead, they first use intermediate criteria in their head such as `is the needle close to the red zone?`, `is the warning light on?`, or `is the valve-handle direction different from usual?` This kind of operational video judgment is also a good scene for showing why the hidden layer is needed.

The original input may be a long list of pixel values. But the model may not identify the state correctly by looking at each pixel one by one and jumping directly to the label. For example, `a pressure gauge with a slightly raised needle`, `a weakly flashing warning light`, and `a slightly rotated valve handle` may each be ambiguous when seen alone. As the data passes through the hidden layer, internal representations like the following may gradually be formed.

- is the pressure-gauge needle close to the warning zone?
- is a bright flashing pattern visible in the warning light?
- is the valve-handle direction different from its normal position?
- are several visual cues overlapping toward the warning side at the same time?

Of course, this too is only an intuitive explanation supplied by people. The actual internal representation may be more complex and more distributed. But this analogy shows clearly that the hidden layer does not leave the raw input alone. It changes it into a more useful representation.

In other words, a multilayer structure is closer to `first creating intermediate judgment material, then sending that material to the final judgment` than to `sending the camera frame straight to the final state`. This point is the most important difference between one perceptron and a multilayer structure. So the result to confirm in this case is whether it is possible to explain in practice why the viewpoint `pass through an intermediate representation, then go to the final judgment` is needed more than the viewpoint `classify the state directly from a list of pixels`.

If the judgment order in this case is compressed again into a small flow, it becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-02/panel-warning-representation-flow-en.mmd"
```

It is easy to feel that if we look at enough pixels, we should be able to identify the state immediately. But from the viewpoint of representation, the pixels are only raw material. First, clues such as the needle, warning light, and valve survive as part of an intermediate representation, and the final state judgment closes as the result of reading their combination. The reason similar scenes feel confusing is not simply that the pixels look alike, but also that different internal axes can come alive more strongly depending on the scene.

### Case 2. Representing Equipment Warning States

Something similar happens in tabular data as well. Suppose that the recent alarm count, average vibration size, temperature rise width, and recovery delay time of one piece of equipment all come in together. At first, a person may try to read the four numbers one by one and judge things like `it is still manageable now` or `it should be stopped immediately`. But in reality, a high alarm count alone is not always dangerous, and an important state may appear only when several signals overlap, such as when vibration and temperature rise grow together and recovery delay also becomes long. The hidden layer does not copy these inputs as they are. It works in the direction of rewriting them into a more useful internal representation, such as `a state where visible output is still maintained but signs of failure are accumulating`.

The difference becomes clearer when the same equipment state is read side by side through the original input and through the viewpoint of internal representation.

| Observation style | Values that appear | Easier judgment to read |
| --- | --- | --- |
| Original input columns | Alarm count `high`, average vibration `above normal`, temperature rise `large`, recovery delay `long` | Signals are mixed across items, so it is hard to conclude immediately |
| Internal hidden-layer representation | Normal-operation-maintenance axis `still present`, fault-sign-risk axis `high` | A more direct distinction becomes possible, such as `output is maintained but inspection priority is high` |

If the four numbers are read one by one, it is easy to feel that the system is still manageable just because one alarm looked tolerable, or to remain vague about which combination is actually the problem. If the situation is reread through the hidden-layer representation, the first thing examined is the intermediate state created by several inputs together, and then how close the danger representation formed by vibration, temperature, and recovery delay is to the final judgment. So the result to confirm in this case is whether the internal representation created by grouped signals separates the equipment state better than looking at the original numeric columns one by one.

If these two cases are tied into one line, it becomes the following.

`The hidden layer does not judge the original input directly. It rewrites it into an internal representation that is easier to separate.`

In the equipment-panel case, it is easy to stop at saying that similar pixels simply cause confusion, but once the hidden representation is examined, it becomes easier to see why combinations such as needle position, warning light, and valve direction separate normal monitoring from immediate inspection. In the tabular-data case, instead of looking separately at alarm count, vibration, temperature rise, and recovery delay, the first thing examined is an internal state closer to the problem, such as a stability axis and a risk axis. The result the reader should hold first is that the core of the hidden layer is not `doing more arithmetic`, but `recreating the internal axes that will be examined before the final judgment`.

If the two cases are compressed again at once, the first flow for reading the hidden layer and representation becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-02/hidden-representation-bridge-en.mmd"
```

This diagram is not trying to explain separately again the visual clues of case 1 and the tabular signals of case 2. It is here to gather once more the common flow shown by both cases: `original input -> rewrite into internal axes -> the final judgment becomes easier to read`.

## Practice And Exercise

The goal of this exercise is to compare how even equipment-panel scenes that look somewhat similar are rewritten into different internal representations after passing through the hidden layer, and how that difference connects to the final score and the next judgment.

Input:

- four frames with gauge-needle deviation, warning-light blink intensity, and valve-handle offset

Output:

- the hidden representation of each frame
- the final score of each sample
- a comparison of whether samples with similar final scores can still have different internal representations

Problem situation:

- equipment-camera frames may all look `slightly abnormal` on the surface, but in reality one scene may be centered on needle deviation while another may be centered on the combination of warning light and valve. It is necessary to check how a hidden layer passing through ReLU rewrites that difference into internal representation.

Concepts to confirm:

- hidden-layer representation is not a simple sum; it is formed after passing through an activation function
- the final score changes depending on what values remain in the intermediate representation
- even with similar final scores, the hidden axis that led the result can be different

Input:

Use the four frames organized above and the hidden-layer and output-layer weights that pass through ReLU.

Before looking at the code, it is useful first to predict which hidden axis will respond more strongly for each frame, and why the final score can look similar while the internal state is still different.

| Frame | Reaction to predict first | Reason to expect it |
| --- | --- | --- |
| `needle_dominant_frame` | `pressure_axis` is larger | The needle deviation is large while the warning-light blink is weak, so the pressure-gauge axis is likely to become active first. |
| `beacon_valve_frame` | `warning_axis` and `coordination_axis` are larger | The warning-light and valve combination is strong, so the warning/action axes may react more strongly. |
| `combined_stop_frame` | All three axes are large | The needle, warning light, and valve are all strong, so internal representations close to reviewing an immediate stop are likely to come alive together. |
| `borderline_watch_frame` | All three axes are moderate | Each signal remains somewhat ambiguous, so it may be hard to tell immediately which axis leads. |

The purpose of this table is not to guess the exact numbers in advance. It is to hold first that `scenes that look similarly abnormal on the surface can still be rewritten into different axes in the hidden layer`, and that `even if the final score looks similar, the internal representation and the next judgment can still differ`.

```python
# This example shows how equipment-panel signals become ReLU hidden-axis representations and affect the final score.
def relu(z):
    return max(0.0, z)

frames = [
    ("needle_dominant_frame", {"needle_deviation": 1.0, "beacon_blink": 0.2, "valve_offset": 0.1}),
    ("beacon_valve_frame", {"needle_deviation": 0.5, "beacon_blink": 0.9, "valve_offset": 0.8}),
    ("combined_stop_frame", {"needle_deviation": 1.1, "beacon_blink": 1.0, "valve_offset": 0.9}),
    ("borderline_watch_frame", {"needle_deviation": 0.7, "beacon_blink": 0.6, "valve_offset": 0.5}),
]

for name, values in frames:
    pressure_axis = relu(
        values["needle_deviation"] * 1.0
        + values["beacon_blink"] * 0.1
        + values["valve_offset"] * 0.2
        - 0.4
    )
    warning_axis = relu(
        values["needle_deviation"] * 0.1
        + values["beacon_blink"] * 1.0
        + values["valve_offset"] * 0.6
        - 0.5
    )
    coordination_axis = relu(
        values["needle_deviation"] * 0.4
        + values["beacon_blink"] * 0.5
        + values["valve_offset"] * 0.9
        - 0.7
    )
    score = (
        pressure_axis * 0.6
        + warning_axis * 0.5
        + coordination_axis * 0.7
        - 0.2
    )

    print(
        f"{name}: "
        f"input=({values['needle_deviation']}, {values['beacon_blink']}, {values['valve_offset']}), "
        f"hidden=({round(pressure_axis, 3)}, {round(warning_axis, 3)}, {round(coordination_axis, 3)}), "
        f"score={round(score, 3)}"
    )
```

In the output, first examine how the same frame is rewritten across the three hidden axes, and how the score is then computed on top of that representation.

```text
needle_dominant_frame: input=(1.0, 0.2, 0.1), hidden=(0.64, 0.0, 0.0), score=0.184
beacon_valve_frame: input=(0.5, 0.9, 0.8), hidden=(0.35, 0.93, 0.67), score=0.944
combined_stop_frame: input=(1.1, 1.0, 0.9), hidden=(0.98, 1.15, 1.05), score=1.698
borderline_watch_frame: input=(0.7, 0.6, 0.5), hidden=(0.46, 0.47, 0.33), score=0.542
```

The numerical output gives the calculation results, but it becomes clearer when the original input is split into stage-by-stage graphs showing what intermediate values it turns into inside the hidden layer and what survives after ReLU before reaching the final score.

![Raw input values by frame](/AiBook/assets/part-05/chapter-02/hidden-axis-input-en.png)

The first graph is the raw input that enters the model. At this stage, the three input values - needle deviation, warning-light blink, and valve offset - are still listed as they are. At this stage alone, it is hard to close immediately which judgment each frame should lead to.

![Pre-activation linear-combination values by frame](/AiBook/assets/part-05/chapter-02/hidden-axis-preactivation-en.png)

The second graph shows the value of each hidden axis after multiplying the input values by weights and adding the bias. Values below 0 still appear here, which means they are traces of the calculation before that hidden axis is activated. In `needle_dominant_frame`, the pressure axis remains positive, but the warning axis and coordination axis are below 0, so they are in a state that is ready to disappear in the next step.

![Hidden representation after ReLU by frame](/AiBook/assets/part-05/chapter-02/hidden-axis-activation-en.png)

The third graph shows the actual hidden representation that remains after passing through ReLU. Values below 0 are cut to 0, and only the axes that remain positive are passed to the next layer. At this stage, `beacon_valve_frame` keeps both the warning axis and the coordination axis alive, while `combined_stop_frame` keeps all three axes strongly alive.

![Final output score by frame](/AiBook/assets/part-05/chapter-02/hidden-axis-score-en.png)

The last graph is the final score after applying the output-layer weights to the hidden representation left after ReLU. The key point is that the original input does not become the score directly. It becomes the output only after passing through the pre-activation values and then the post-ReLU representation.

What matters in this example is the following.

- The same frame input is not used as-is. It is rewritten into a new representation in the hidden layer.
- When the input combination changes, the three axes of `hidden` also react in different ways.
- The final score is calculated on top of that intermediate representation rather than directly from the original input.

The difference becomes clearer when the execution results are reread through the question `which axis led more strongly?`

| Frame | hidden pattern | score | Core point to read now |
| --- | --- | --- | --- |
| `needle_dominant_frame` | `(0.64, 0.0, 0.0)` | `0.184` | Only the needle-deviation axis is alive, so it still does not close as a scene for reviewing an immediate stop |
| `beacon_valve_frame` | `(0.35, 0.93, 0.67)` | `0.944` | The warning-light and valve-combination axes lead, so it is read as a stronger intervention signal than a simple warning check |
| `combined_stop_frame` | `(0.98, 1.15, 1.05)` | `1.698` | All three axes are strongly alive, so internal representations close to reviewing an immediate stop overlap together |
| `borderline_watch_frame` | `(0.46, 0.47, 0.33)` | `0.542` | All three axes overlap weakly, so it remains closer to boundary monitoring |

In particular, `needle_dominant_frame` and `borderline_watch_frame` are both not strong stop scenes, but their internal representations differ quite a bit. One has only the pressure-gauge axis alive, while the other has all three axes overlapping weakly. Even when two scenes both look like `weak abnormality`, the next judgment can differ depending on which hidden axis becomes active first. That is the real computational feel of the phrase `the hidden layer rewrites the original input`.

In other words, the hidden layer is the stage that turns the input into a more useful internal representation.

After reading all the outputs, it is useful to connect once more whether `this input should be read as original columns` or `rewritten through hidden axes`.

`needle_dominant_frame` and `borderline_watch_frame` are both not strong stop scenes, but one is centered on the pressure-gauge axis while the other is a state where several axes overlap shallowly. `beacon_valve_frame` and `combined_stop_frame` both lean toward needing intervention, but one is led by the warning-light and valve combination while the other has all three axes strongly alive. Once it becomes visible that the three hidden axes move differently from the original three inputs, it becomes reasonable to read that the model has rewritten the input into a more useful internal coordinate system before making the final judgment. The core of representation learning is not `throwing away the input`, but `rewriting the input into an internal coordinate system that separates it better`.

After running the code once, it is better to continue changing the values directly so you can see which frame grows which internal axis more quickly.

| Value to change next by hand | Output to inspect first | Interpretation question |
| --- | --- | --- |
| Raise `beacon_blink` in `borderline_watch_frame` from `0.6` to `0.9` | How quickly do `warning_axis` and `coordination_axis` grow? | When the warning-light cue grows, which internal axis takes the lead first? |
| Raise `valve_offset` in `needle_dominant_frame` from `0.1` to `0.6` | Does a pressure-axis-centered scene turn into a scene where several axes overlap? | At what point does a frame that was strong on only one input axis move into a combined representation? |
| Change the bias in the final `score` calculation from `-0.2` to `0.0` | How many more frames become intervention-needed even with the same hidden pattern? | Even when the internal representation stays the same, how does the operational interpretation change if the final judgment rule changes? |

## Why Does The Phrase Representation Learning Appear

In Yoshua Bengio's work and in the 2015 paper by LeCun, Bengio, and Hinton, deep learning is explained not as merely a large neural network, but as a structure that learns representations across several levels.

It can be summarized as follows.

`The strength of deep learning does not lie only in having many parameters, but in being able to learn intermediate representations across several layers that are favorable to the problem.`

So to understand deep learning, it is more important to look not at depth itself, but at `what kinds of representation transformation the depth makes possible`.

## When To Close The Representation Explanation Here And Pass To The Next Chapter

The responsibility of this section, which explains hidden layers and representation, is to close `why the intermediate calculation should be read not as simple arithmetic, but as a representation transformation`. After that, the flow should move to `what nonlinearity makes that representation possible`.

| Signal that appears first | Interpretation that should be closed here | Where it connects immediately next |
| --- | --- | --- |
| The hidden representation looks like a better-separated axis than the input | It means the internal coordinate system is changing into a representation that makes the problem easier to solve. | Move to Chapter 3 on activation functions and nonlinearity. |
| You want to attach a human-readable name to each node immediately | Because it may be a distributed representation, the interpretation should not be fixed too strongly. | Pass to later Parts on interpretability, attention, and embedding examples. |
| The phrase `the model made the features itself` still feels abstract | It is enough here to fix the fact that the model learns intermediate representations instead of relying only on human-designed features. | Connect to the broader treatment in P5-10. |
| You begin asking again why activation functions are needed | That is a signal that the role of nonlinearity is not yet closed by representation explanation alone. | Connect directly to P5-3.1 through P5-3.5. |

## Checklist

- Can you explain that the hidden layer is not just an intermediate calculation, but a layer that creates an internal representation?
- Can you explain the connection between representation and representation learning?
- Can you explain the hidden layer as `a representation-transformation layer between input and output`?
- Can you understand representation as a way of rewriting the same object inside the model?
- Can you say that as layers become deeper, internal representations that are more favorable for the problem can be formed?
- Can you explain why misunderstanding can arise if the internal representation is fixed too quickly with one simple human term?
- When you find yourself describing the hidden layer only as an intermediate calculation box, can you first recall the view that it is a layer that rewrites representation?
- Do you understand the flow that after explaining representation learning, activation functions and nonlinearity must come next?

## Sources And References

- Yoshua Bengio, Aaron Courville, Pascal Vincent, `Representation Learning: A Review and New Perspectives`, IEEE Transactions on Pattern Analysis and Machine Intelligence, 2013, date checked: 2026-07-19. [https://arxiv.org/abs/1206.5538](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, date checked: 2026-06-28. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, `Deep learning`, Nature, 2015, date checked: 2026-06-28. [https://www.nature.com/articles/nature14539](https://www.nature.com/articles/nature14539){: target="_blank" rel="noopener noreferrer" }
