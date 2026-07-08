# P1-9.1 Image Recognition and Representation Learning

> Section ID: `P1-9.1`
> Version: `v2026.07.07`

Chapter 8 distinguished supervised learning, unsupervised learning, and reinforcement learning by the kind of learning signal they use. Now we move into `deep learning`.

This section does not try to explain all of deep learning. Instead, it uses `image recognition` as a concrete case to explain why deep learning is often understood as a shift from `having people design all the features` to `having the model learn useful representations as well`.

The central question is:

> when we classify images,  
> what is different between a method where people write the features themselves  
> and a method where the model learns the representation?

> one of the key shifts in deep learning is that the model does not only fit the final output; it also learns internal representations that make the input easier to handle

This section organizes `image recognition`, `hand-crafted features`, `learned representations`, `CNN`, and `AlexNet` to explain why deep learning is often treated as a turning point for image problems. The basic intuition of `representation` was introduced earlier in 3.3 and 4.3, and the basic structure of `supervised learning` was introduced in 8.1.

These terms can all sound like similar historical deep-learning vocabulary at first. A quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| image recognition | predicting what is in an image | the first case study in Chapter 9 |
| hand-crafted features | clues designed in advance by people | the baseline before deep learning |
| learned representation | an internal representation learned from data by the model | the core of the deep-learning shift |
| CNN | a neural-network structure that handles local image patterns hierarchically | the representative structure for image recognition |
| AlexNet | a turning-point case where large data, GPUs, and a deep CNN were combined | a symbolic case in the spread of deep learning |

The minimum distinction to keep is:

- hand-crafted features versus learned representations
- CNN as an image-oriented structure
- AlexNet as a turning point in spread, not the absolute beginning

## Scope of This Section

This section does not explain convolutional neural networks with equations. `Convolution` and `pooling` return in Part 5, especially P5-11.2. `Activation functions` return in P5-3.1 and P5-3.2. `Backpropagation` and `optimizers` return in P5-5.1, P5-5.2, and P5-7.1.

This section also does not present AlexNet as `the beginning of all deep learning`. Neural-network and CNN research had already existed for a long time before that. Here, AlexNet is used more narrowly as a representative turning point that made the 2010s spread of deep learning visible.

It also does not redefine `representation` from the ground up. The focus here is the contrast:

> should people design the representation by hand,  
> or should the model learn it from data?

The direct lineage of LLMs is handled separately in the next section and in 9.3.

One more historical distinction matters. Neural networks did not suddenly appear in the 2010s. Around 2006, work on deep belief networks and representation learning helped revive interest in deep learning. So AlexNet in 2012 is more accurately read not as an event that emerged from nothing, but as a case where older neural-network research and the revival around 2006 met large datasets and GPU computation and then became a visible turning point in adoption.

The baseline definition in this section is:

> in image recognition, deep learning strongly demonstrated a direction where models learn hierarchical representations from data, rather than depending only on features designed by people

## Goal of This Section

- Understand image recognition as the task of predicting a category from an input image.
- Explain the difference between hand-crafted features and learned representations.
- Understand at an introductory level why CNNs handle local image patterns hierarchically.
- Read AlexNet as a turning point where large data, GPUs, deep CNNs, and representation learning were combined.
- Avoid exaggerating image-recognition history into the direct lineage of LLMs.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| image classification looks easy to people but is hard to write as fixed rules | This shows why deep learning became necessary. | It is enough to understand that lighting, viewpoint, and occlusion make rules fragile. |
| hand-crafted features and learned representations are different approaches | This captures the core deep-learning shift in one sentence. | It is enough to understand that people used to choose the clues directly, and models later learned the representation as well. |
| AlexNet is better read as a turning point in spread than as `the first beginning` | This keeps the historical explanation important without overstating it. | It is enough to understand it as a representative turning point in adoption. |

## Image Recognition Looks Easy to People but Is Hard to Write as Rules

People can look at a picture and quickly say `cat`, `car`, or `human face`. But as soon as we try to write this judgment as explicit rules, the problem becomes difficult.

Suppose we try to write rules for finding a cat:

> pointed ears may indicate a cat  
> visible whiskers may indicate a cat  
> two eyes and fur may indicate a cat

These rules soon run into exceptions.

| Change | Why rules become difficult |
| --- | --- |
| lighting change | the same object can look different in brightness and color |
| pose change | the positions of ears, eyes, and legs shift |
| background change | the background may dominate more than the object |
| occlusion | only part of the object may be visible |
| variation inside one category | cat breeds, sizes, and fur colors all vary |

The earlier face-recognition example in 3.1 connects directly to this problem. Surveys of face recognition describe older approaches such as geometry-based features, holistic methods, hand-crafted features, and hybrid methods. Those were important research streams, but uncontrolled conditions such as lighting, pose, expression, age, and occlusion created pressure for stronger methods.

So the core difficulty of image recognition is not only `which classifier should we choose?` The deeper issue comes first:

> what should we look at in the image at all?

In other words, the question of `features` and `representations` matters before classification.

## Hand-Crafted Features Decide in Advance What Clues to Look At

`Hand-crafted features` are clues that people decide in advance for the model to use. For example:

| Problem | Features people may design |
| --- | --- |
| face detection | distance between the eyes, nose position, face contour |
| lane detection | line direction, brightness change, boundary edges |
| object classification | edges, textures, color histograms |
| character recognition | stroke direction, curves, intersections |

This approach has strengths. It is relatively interpretable, and it can still work with limited data. In certain stable environments it can remain useful.

But as variation grows, it becomes difficult for people to design all the clues by hand.

> which edges matter?  
> which texture still indicates the same object?  
> can the object still be treated as the same one when the lighting changes?  
> can the same category be preserved across different backgrounds?

These questions connect back to the problem of `representation` introduced in 3.3 and 4.3. A good representation reveals the differences that matter for classification while suppressing differences that do not.

## Learned Representations Are Built Inside the Model

`Representation learning` is the attempt to learn from data how to turn raw input into a form that is more useful for the model. Bengio, Courville, and Vincent explain that the success of machine-learning algorithms depends heavily on the representation of the data.

For images, the raw input is the `pixel`. But pixel values alone do not directly expose categories such as cat, car, or human face. Across multiple layers, a model may transform lower-level clues into higher-level representations.

> pixel  
> -> line and edge  
> -> texture and local part  
> -> object part  
> -> category prediction

This does not mean every model literally divides its inside into human-readable stages. At the introductory level, the safe understanding is:

> the model does not classify the raw image exactly as it is;  
> through several stages of computation, it forms internal representations that are useful for classification

The Nature review by LeCun, Bengio, and Hinton explains deep learning as a family of computational models with multiple processing layers that learn data representations at multiple levels of abstraction. It also notes that deep learning greatly improved performance in speech recognition, visual object recognition, object detection, and related areas.

## CNNs Handle Local Image Patterns Hierarchically

`CNNs` are one of the most important neural-network structures in image recognition. Here we only need the intuition, not the equations.

In images, location matters. Clues such as eyes, noses, mouths, wheels, doors, and handles first appear in small local regions. CNNs are structured so that local patterns can be detected repeatedly across positions and then combined in later layers into larger patterns.

```mermaid
flowchart LR
  Pixels[Pixels]
  Edges[Edges and Corners]
  Parts[Parts and Shapes]
  Object[Object Representation]
  Class[Class Prediction]

  Pixels --> Edges --> Parts --> Object --> Class
```

For a simplified car image:

| Stage | Example of clues the model may handle |
| --- | --- |
| lower layers | lines, corners, brightness changes |
| middle layers | repeated circular shapes like wheels, window-like patterns |
| higher layers | combinations of parts associated with the whole car |
| output | category scores such as car, bus, or truck |

The important point is that people do not have to write every rule such as `if there is a wheel, then it may be a car`. Instead, the model adjusts internal representations and parameters together by seeing many labeled images.

## Why AlexNet Is Mentioned So Often

`AlexNet` is often mentioned together with the 2012 ImageNet competition as a representative case in the spread of deep learning. Krizhevsky, Sutskever, and Hinton describe a large deep CNN trained to classify roughly 1.2 million high-resolution images into 1,000 categories. The paper reports about 60 million parameters, 650,000 neurons, five convolutional layers, and three fully connected layers.

The raw numbers matter less than the combination:

| Element | Meaning |
| --- | --- |
| large-scale data | many labeled images became the material for learning |
| deep CNN | multiple layers transformed image representations step by step |
| GPU implementation | large matrix computation and repeated training became feasible in realistic time |
| regularization and data augmentation | the risk of fitting only the training data was reduced |

These were not independent strengths. They worked together. Without large data, a deep model does not see enough varied examples. Without a deep CNN structure, it is harder to combine low-level clues and higher-level representations across multiple layers. Without GPUs, repeated training and comparison of large models become impractical. Without regularization and data augmentation, a large model is more likely to overfit.

So the safer reading is not `one good CNN appeared`, but:

> large labeled data  
> + deep CNN structure  
> + GPU-based computation  
> + training techniques that reduce overfitting  
> = a visible turning point where deep learning showed strong performance in image recognition

The AlexNet paper notes that training took five to six days on two NVIDIA GTX 580 GPUs, and it suggested that faster GPUs and larger datasets could improve results further. That helps show that the rise of deep learning was not only a change in ideas. It was also a change in the combined role of data scale, model structure, compute, and training methods.

The Nature review describes the AlexNet paper as a breakthrough that triggered rapid adoption of deep learning in the computer-vision community. But that should not be read as `AlexNet invented deep learning for the first time`. The safer statement is:

> AlexNet is a representative turning point that clearly showed deep learning could be a strong option for large-scale image recognition

## Image Recognition Is Not the Direct Lineage of LLMs

The goal of this section is not to write the direct history of LLMs. `Image recognition`, `object detection`, and `speech synthesis` are not direct ancestors of LLMs.

But they do show one important background:

> for complex inputs, it is hard for people to describe everything through rules and features alone  
> with large data and compute, neural networks can learn useful representations  
> this approach spread across images, speech, and language

Against that background, the next sections examine object detection and speech generation. The same rule stays in place there as well: cases such as YOLO and WaveNet are not the direct cause of LLMs, but surrounding evidence that the deep-learning paradigm had spread across many kinds of input and output problems.

## What to Remember from This Section

Image recognition looks intuitive to people, but it is difficult to handle reliably with rules and hand-crafted features alone because of lighting changes, pose changes, backgrounds, occlusion, and large variation inside a category.

Deep learning changed the framing:

> people design every feature themselves  
> -> the model learns useful representations from data as well

AlexNet is the representative case that made this shift widely visible. The point to remember is not `image recognition created LLMs`, but:

> representation learning and large-scale neural networks spread the deep-learning paradigm by showing strong results across many domains

## Short Check

- I can explain image recognition as the problem of predicting a category from an image.
- I can distinguish hand-crafted features from learned representations.
- I can explain that CNNs handle local image patterns hierarchically.
- I can describe AlexNet as a turning point where large data, deep CNNs, GPUs, and training techniques were combined.
- I do not treat image-recognition history as the direct lineage of LLMs.

## When to Recall This View First

This section is useful when a discussion describes the deep-learning turning point only as `performance improved` and loses the meaning of representation learning.

- when contrasting a feature-engineering approach with a representation-learning approach
- when explaining at an intuitive level why CNNs mattered for images
- when placing AlexNet safely as a turning point in spread rather than as `the absolute first beginning`

In those cases, it helps to separate three questions:

> why was the problem hard to write as rules?  
> what did people design, and what did the model learn?  
> why did data, GPUs, and model structure matter together?

That makes it possible to explain the shift in the deep-learning paradigm clearly without overstating the historical case.

## Sources and Further Reading

- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, [ImageNet Classification with Deep Convolutional Neural Networks](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2012, accessed 2026-06-23.
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, [Deep learning](https://www.nature.com/articles/nature14539){: target="_blank" rel="noopener noreferrer" }, Nature 521, 436-444, 2015-05-27, accessed 2026-06-23.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, arXiv, 2012-06-24, accessed 2026-06-23.
- Daniel Saez Trigueros, Li Meng, Margaret Hartnett, [Face Recognition: From Traditional to Deep Learning Methods](https://arxiv.org/abs/1811.00116){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-06-23.
