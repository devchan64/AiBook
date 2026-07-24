# P5-8.3 Supplementary Learning: Stabilizing Deep Computation

> Section ID: `P5-8.3`
> Version: `v2026.07.23`

_Subtitle: How do initialization, numerical stability, and batch normalization stabilize deep networks at different points?_

In P5-8.1 and P5-8.2, we saw how to add objective-function control and structure-level control to the learning loop. But even when such control is added, learning can still shake if the deep computation itself is unstable. In P5-6.4, we saw why dropout and batch normalization are sensitive to the difference between training mode and evaluation mode. On top of that background, we add one more question that often remains for beginners.

Why does stacking more layers not immediately mean the model will learn well?

To answer this question, it is better not to memorize initialization, numerical stability, and batch normalization separately, but to read them together under one axis: `why deep networks became able to shake less in practice`. In the flow of Chapter 8, the previous sections dealt with `what should be made less preferred` and `what path dependence should be reduced`, while this section gathers together `the conditions that let the computation itself hold up`.

Initialization sets the starting point where learning begins, numerical stability is the standard for checking whether values and gradients become too large or too small during computation, and batch normalization is the device that organizes activation distributions into a range that is easier to handle during learning.

When this axis becomes blurry again, it helps to reread together the glossary entries for [training mode](/AiBook/reference/concept-glossary-parts/14-hieut/#training-mode), [batch normalization](/AiBook/reference/concept-glossary-parts/06-bieup/#batch-normalization), [initialization](/AiBook/reference/concept-glossary-parts/11-chieut/#initialization), and [numerical stability](/AiBook/reference/concept-glossary-parts/07-siot/#numerical-stability).

## The Question Of Why Deep Computation Shakes

- Why do deep networks not learn well immediately just because we add more layers?
- What does initialization determine?
- What kind of concern is numerical stability?
- Why is batch normalization often mentioned together as a learning-stabilization tool?
- How do these three concepts answer different questions from the optimizer and regularization?

The larger flow of ReLU-type activations and the spread of deep learning reconnects in P5-3.4, and why batch normalization is sensitive to the train/eval mode difference is reread on top of the standard already introduced in P5-6.4. The broader viewpoint that distinguishes regularization from normalization continues from P5-8.1, and the optimizer update itself reconnects to P5-7.1 and P5-7.2.

The role of this section is to gather in one place `the conditions that let deep computation survive both the forward pass and the backward pass`.

## Standards For Initialization, Numerical Stability, And Batch Normalization

- You can explain initialization as `the placement of values at the start of learning`.
- You can explain numerical stability as `the problem of keeping values and gradients within a manageable range during computation`.
- You can explain batch normalization as `a device that organizes activation distributions so learning shakes less`.
- You can distinguish that the optimizer, regularization, and batch normalization answer different questions.
- You can explain that this section plays the role of `a computation-stabilization device` inside Chapter 8.
- You can explain why the Python example in P5-8.4 is needed next, and what that example is meant to confirm.

## Why Should We Read These Three Together

When people first learn deep networks, the following misunderstandings often appear.

- if we stack more layers, the model will automatically learn better
- if we only switch the optimizer to Adam, most problems will be solved
- batch normalization is just one library option

But in reality, the starting point where learning begins, how values grow or shrink in intermediate computation, and what range of values each layer passes to the next layer all interact together.

Drawn very briefly, the flow looks like this.

```mermaid
--8<-- "assets/part-05/chapter-08/stabilization-bridge-flow-en.mmd"
```

The core point is that the phenomenon `learning is not going well` does not always come from only one cause.

- the starting values may be too similar or too extreme
- values may become too large or almost disappear while passing through layers
- the distribution of activations may keep shaking the next computation

So in this section we group these three as `the conditions that make deep learning actually possible`.

## What Does Initialization Determine

Initialization is the act of deciding what numbers to place in the parameters before learning begins.

On the surface, it can look like it only chooses a starting point, but in reality it is directly connected to the following two questions.

1. Can different neurons begin to learn different roles?
2. In the first few forward and backward passes, do values avoid becoming too large or too small?

For example, if all weights start from exactly the same value, especially 0, then multiple neurons can show the same reaction to the same input and receive the same gradient. In that case, even if we stack layers, it becomes difficult for them to divide up different features.

So the first responsibility of initialization is closer to `not letting every neuron start in exactly the same way` than to `not starting arbitrarily`.

## Why Should The Starting Point Not Be Identical

With a single perceptron, an awkward starting value may not look like a large problem. But in a multilayer structure, multiple neurons in the same layer need to learn different combinations.

If the starting point is completely identical:

- they see the same input
- they produce the same output
- they receive the same gradient
- they update in the same direction

As a result, the advantage of having many neurons decreases.

From a beginner's viewpoint, the point can be compressed into one sentence.

`Initialization is not merely the act of writing down the first numbers. It is the act of leaving open the possibility that many neurons will split into different roles.`

## What Does Numerical Stability Worry About

Numerical stability is the standard for checking whether values or gradients become too large or too small during computation, causing learning to shake.

Here it is enough to picture the following two scenes first.

- values keep growing and explode as they pass through layers
- values or gradients become so small as they pass through layers that they effectively disappear

Deep learning repeats the same kind of computation layer after layer. So a small instability in one step can become larger as it passes through many deep layers.

| Problem scene | Beginner-level intuition | What happens in learning |
| --- | --- | --- |
| values become too large | the next layer keeps receiving numbers that are too big | outputs and gradients become more likely to shake |
| values become too small | the next layer sees only almost identical small values | gradients may weaken and learning can slow down |

This section does not provide a mathematical proof, but the important intuition is clear.

`Deep learning is the problem of stacking many layers, but it is also the problem of making that many computations survive within a usable numeric range.`

## Why Is One Activation Function Alone Not Enough

As we saw in P5-3.4, ReLU-type activations are widely used in deep networks. But changing only the activation function does not automatically solve every problem.

In practice, the following factors interact together.

- how an activation function passes values forward
- initialization that avoids starting with values that are too small or too large
- optimizer and learning-rate settings
- distribution-stabilization devices such as batch normalization

So when we say `deep learning became practical`, it usually does not refer to a single invention, but rather to several stabilization devices working together.

## Why Is Batch Normalization Important

Batch normalization reorganizes the activation distribution by referring to the mean and variance inside one batch.

At the beginner level, the following understanding is enough.

- if the outputs of the previous layer are too uneven
- the next layer has to learn while receiving a distribution that keeps shaking
- then both learning speed and stability can be affected

Batch normalization can therefore be read as `a device that, using the current batch as a reference, organizes values once more into a range that is easier to handle before passing them on`.

The mode difference we saw in P5-6.4 reconnects here as well.

- during training, it refers to the current batch statistics
- during evaluation, it relies more on the reference accumulated during training

So batch normalization is not just `one normalization name`, but a representative case that makes us read learning stabilization and mode switching together.

## What Is Different From Regularization

Beginners can easily look at batch normalization, dropout, and weight decay as one bundle of `options that help learning`. But the questions are different.

| Item | The question it answers first |
| --- | --- |
| initialization | From what starting point should learning begin? |
| numerical stability | During repeated computation, do values and gradients remain in a manageable range? |
| batch normalization | Should the activation distribution be reorganized into a range that is easier to handle? |
| optimizer | By what stride and rule should the gradient be turned into an actual update? |
| regularization | What constraints should be placed so the model does not go toward an overly complex solution? |

If we fix this table first, then even when new techniques appear later, it becomes easier to separate whether they are closer to `starting point`, `computational stability`, `update`, or `generalization`.

## Cases And Examples

To read through the earlier phrase `why deep networks became able to shake less in practice` as a concrete case, it is better not to memorize the three terms separately, but to see together `where one deep computation scene shakes, and what reduces that shaking`. The two cases below split the same deep network into `a scene that starts unstably` and `a scene that has been reorganized to shake less`.

### Case 1. A Scene Where A Deep Network Shakes From The Beginning

Imagine a small deep network with input `x = 2`. Suppose the first layer has two neurons and all their weights start at `0`. Then the two neurons initially make the same output, and in backpropagation they are also likely to receive the same gradient and move together as `0 -> 0.3 -> 0.6`. In this first scene, the problem already appears that `if initialization chooses the wrong starting point, many neurons cannot split into different roles`.

Now add another condition: suppose the starting weight scale in later layers is also large. If similar values from the previous layer keep being passed forward and large weights are repeated, the value range can grow more quickly like `0.6 -> 1.8 -> 5.4`. At that point, what shakes is not only the output number itself. The activation response can become skewed and the gradient path can become unstable as well. Numerical stability appears here as the standard that asks `can deep computation survive this numeric range`.

Finally, suppose in one batch the intermediate activations cluster around `0.5, 0.8, 1.0`, but in another batch they arrive in a much larger range such as `15, 20, 24`. Then the next layer receives inputs of very different scale every time, and learning can shake more easily. At this point batch normalization becomes necessary as `the device that reorganizes the activation distribution already created between layers into a range the next layer can handle more easily`.

So this case does not show three unrelated problems. `neurons tied to the same starting point`, `value ranges growing as they pass through depth`, and `intermediate distributions shaking from batch to batch` continue inside one scene, showing why deep networks need to hold onto `starting point`, `repeated computation range`, and `between-layer distribution` together if they are to shake less.

### Case 2. A Scene That Makes A Deep Network Shake Less

Now look at the same structure again, but change the starting conditions. Suppose we do not give the two first-layer neurons exactly the same starting weights, but make one slightly smaller and the other slightly different. Then the two neurons no longer repeat exactly the same reaction from the start, and they gain the possibility of responding along somewhat different paths to different input combinations. Here the role of initialization is not first `finding a good number`, but `providing a starting point that avoids duplicating the same pathway`.

Next, if the weight scale in each layer is not made excessively large, the value range can move more gently like `0.6 -> 0.9 -> 1.1`. Real models are more complex than this, but for a beginner this scene is enough. For a deep network to shake less, even with many layers the computation has to survive without exploding or disappearing all at once. Here numerical stability becomes the standard for reading `what kind of starting scale and computational flow let repeated deep computation hold up`.

Finally, even if the activation distribution passed between layers varies from batch to batch, inserting batch normalization lets the next layer receive not `completely different scales every time`, but `inputs reorganized again into a comparable range`. So the first role of batch normalization is not memorizing the name, but organizing an intermediate distribution that has already started to shake so that the next layer can keep surviving it.

The result to check in this case is clear. Deep networks began to shake less not because there are more technique names, but because initialization separates the starting point, numerical stability keeps repeated computation within range, and batch normalization reorganizes the between-layer distribution.

For beginners, it is useful to fold Case 1 and Case 2 back again in the following order.

```mermaid
--8<-- "assets/part-05/chapter-08/stabilization-case-reading-flow-en.mmd"
```

The one point to catch first in this flowchart is simple. Stabilizing deep networks is not `a list of technique names`, but a judgment sequence that reads `does the starting point split -> does the repeated computation stay within range -> does the distribution between layers keep shaking the next layer`.

![Comparison of neuron paths between the unstable scene and the stabilized scene](/AiBook/assets/part-05/chapter-08/stabilization-neuron-paths-en.png)

This graph shows that in the unstable scene the two neurons move in almost overlapping paths, while in the stabilized scene the two neurons do not repeat exactly the same path.

![Comparison of layer-wise activation ranges between the unstable scene and the stabilized scene](/AiBook/assets/part-05/chapter-08/stabilization-layer-range-en.png)

This graph shows that as the network goes deeper, the range in the unstable scene grows more quickly, while the range in the stabilized scene moves more gently.

![Comparison of batch-wise intermediate activation spreads between the unstable scene and the stabilized scene](/AiBook/assets/part-05/chapter-08/stabilization-batch-spread-en.png)

This graph shows that in the unstable scene the difference in intermediate distribution from batch to batch is large, whereas in the stabilized scene the next layer can more easily receive values on a comparable scale.

If we fold the two cases back into one flow, the stabilization axis this section wants us to read together becomes the following.

| Stage | What shakes first | Device to hold onto first |
| --- | --- | --- |
| before learning begins | are neurons tied to the same starting point? | initialization |
| while computation repeats through layers | are the ranges of values and gradients growing or shrinking? | the numerical-stability viewpoint |
| when passing from one layer to the next | does the intermediate activation distribution keep shaking the next layer? | batch normalization |

In other words, even if the two cases look like `one problem case` and `one solution case`, in reality they should be read as one stabilization axis that separately holds onto `starting point`, `repeated computation range`, and `between-layer distribution` to make deep learning shake less.

| Standard that is easy for a person to see first | Standard to reread from the viewpoint of initialization, numerical stability, and batch normalization |
| --- | --- |
| It is easy to feel that stacking more layers should automatically improve learning because expressive power increases. | The deeper the stack becomes, the more the starting point, value range, and activation distribution can all shake together, so the stabilization conditions must be checked together. |
| It is easy to think switching the optimizer to Adam will solve most things. | The optimizer is the update rule, while initialization, numerical stability, and batch normalization deal with the conditions that let the computation survive before that. |
| It is easy to think batch normalization is only one library option. | Batch normalization is a stabilization device that organizes activation distributions during learning and also makes us read mode differences together. |
| It is easy to think increasing only the number of neurons or layers will automatically make the model learn different features. | If initialization is identical, many neurons can move along the same path, and large values can amplify instability during repeated computation. |

The final result to confirm in these cases is clear. The core of deep-network stabilization is not `memorizing many technique names`, but understanding that initialization handles the starting point, numerical stability handles the range of repeated computation, and batch normalization handles the intermediate distribution, and that the three together make learning shake less.

## Practice And Example

If you can answer the following questions, the role of this section is sufficiently closed.

| Question | Viewpoint to confirm |
| --- | --- |
| What does initialization determine? | It opens the possibility that multiple neurons begin from different starting points and divide roles. |
| What does numerical stability worry about? | It checks whether values and gradients stay within a manageable range during deep repeated computation. |
| Where does batch normalization intervene? | It reorganizes intermediate activation distributions into a standard that the next layer can handle more easily. |

Because this section closes the concept map first, we do not repeat executable code here right away. Instead, in the next [P5-8.4](section-04.en.md) we separately confirm with a Python example and graphs how a large initialization scale grows values while passing through deep layers, and what changes once batch normalization is inserted.

## Checklist

- Can you explain that deep networks are not only a problem of stacking structure, but also a problem of making the computation survive?
- Can you explain initialization from the viewpoint of `placing starting weights`?
- Can you explain numerical stability from the viewpoint of `how deep repeated computation shakes the numeric range`?
- Can you explain why batch normalization appears together with learning stabilization and mode-difference explanations?
- Can you explain that batch normalization is a learning-stabilization device that organizes activation distributions into a range that is easier to handle?
- Can you distinguish that the optimizer, regularization, and batch normalization answer different questions?

## Sources And References

- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, `Dive into Deep Learning`, `5.4 Numerical Stability and Initialization`, `8.5 Batch Normalization`, `12 Optimization Algorithms`, checked on 2026-07-11. [https://d2l.ai/](https://d2l.ai/){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, Part II `Modern Practical Deep Networks`, checked on 2026-07-11. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Stanford `CS231n: Deep Learning for Computer Vision`, schedule and course notes on `Regularization and Optimization`, `Neural Networks and Backpropagation`, `CNN Architectures`, checked on 2026-07-11. [https://cs231n.stanford.edu/](https://cs231n.stanford.edu/){: target="_blank" rel="noopener noreferrer" }
