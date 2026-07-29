# P1-5.1 What Does Learning Change?

> Section ID: `P1-5.1`
> Version: `v2026.07.26`

Chapter 4 organized real-world problems in terms of `input`, `output`, `feature`, `representation`, and `parameter` so that a model could handle them. Now we move one step further and ask: when we say a model learns, what inside the model actually changes?

In AI, `learning` is a broad concept that means performance on a task improves after experience data. Within that broader idea, `training` is the more concrete procedure in which the model sees examples and adjusts internal values to reduce output error. Those internal values mainly refer to parameters, especially `weights` and `biases`.

In Part 1, this section fixes the baseline distinction among `learning`, `training`, and `fitting`. The baseline meaning of `parameter`, `weight`, and `bias` was introduced in 4.3, and the execution perspective of `inference` is developed in 5.2. Here the focus is narrower: separating `what changes` from `what procedure causes that change`.

At the same time, this topic can easily be read too broadly. Saying that a model learns does not mean it understands the world the way a person understands experience. In this section, we keep the terms narrower:

> learning = the broad idea that task performance improves after experience data  
> training = the procedure that adjusts internal model values to fit data and goals

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| learning is broad, while training is one concrete procedure inside it | This reduces the confusion created when both are translated simply as `learning`. | Read learning as the result of change, and training as the procedure that adjusts values. |
| training mainly adjusts parameters | This connects directly to later discussion of weights, loss, and optimization. | Understand that internal model values are changed to fit data. |
| learning is not understanding or consciousness, but task-performance improvement | This prevents us from exaggerating the similarity between human learning and model learning. | Read it as measurable improvement after experience data. |

The useful first distinction is:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| learning | a broad improvement after experience | the outer concept for what got better |
| training | the concrete procedure that adjusts internal values | the stage that changes criteria to fit data and goals |
| fitting | the act of matching model state to data in a specific tool | a practical term often connected to APIs like `fit` |
| inference | the stage that uses learned values to create new output | the next stage after training |

Here we keep the distinction: `learning is the broad result`, `training is value adjustment`, `fitting is an execution form`, and `inference is the usage stage`.

## Why Is It Called Learning?

The term `learning` in machine learning does not mean a model gains understanding or consciousness like a person. It is used in a narrower technical sense.

The *Deep Learning* book introduces Tom Mitchell’s definition: a program learns if its performance on a task improves through experience. Three words matter in that definition.

| Element | Meaning in machine learning | Customer-support example |
| --- | --- | --- |
| experience | the data or examples the model sees | past support sentences and labels |
| task | the job the model must perform | support-message classification |
| performance measure | the criterion used to judge improvement | classification accuracy or human-review result |

So we use the word `learning` because the model sees experience-like data, changes internal values, and improves on a defined task by a measurable standard.

> experience data enters  
> internal model values are adjusted  
> task performance improves  
> so we call it learning

This resembles human learning only in one limited way: past experience affects later behavior or judgment. But human learning also involves understanding, memory, context, purpose, bodily experience, and social interaction. Machine-learning `learning` is usually defined much more narrowly, in terms of data, goals, performance criteria, and internal value adjustment.

In this book, when we say `the model learns`, we mean:

> the model sees data,  
> adjusts the internal values used in output computation,  
> and does so with respect to a defined goal

## It Is Safer to Distinguish Learning and Training

In research and technical writing, `learning` and `training` are not always treated as a perfectly strict pair of opposites. A `learning algorithm` may include the training procedure, and everyday technical writing often moves naturally between `train a model` and `learn from data`.

Still, the two words have different centers of gravity. `Learning` often points to the broader phenomenon or problem setting in which performance improves after experience. `Training` more often points to the concrete procedure of adjusting model parameters using data.

Since Korean often translates both as one word, these two levels can easily mix. In this book, we keep them apart like this.

| English expression | Preferred Korean expression in this book | Central question | Example |
| --- | --- | --- | --- |
| learning | learning | did performance improve after experience? | classification performance improved after seeing support data |
| training | training or learning procedure | how were internal values adjusted? | weights and biases were updated to reduce loss |
| fitting | fitting | was model state matched to the given data? | `model.fit(X, y)` was run |
| inference | inference or execution | was a new output created using learned values? | a new support sentence was classified as delivery |

In that sense, `learning` is the broader result and `training` is a representative procedure inside it.

> learning: what got better?  
> training: by what procedure were the values changed?

It is safer to read this distinction as a flow rather than as a rigid classification table. Read `learning` broadly, read `training` as a representative procedure inside it, and place `inference` as the next stage that uses the result.

The same scene can be worded differently depending on which level is being discussed. Saying `the model learned support-message classification` usually points to the result side: performance on new messages improved. Saying `the model was trained on support data` points more to the procedure: labeled examples were used to adjust internal values.

For example, `the model learned customer-inquiry classification` is a broad statement. More precisely, it can be separated like this.

> training: past inquiries and labels were used to adjust model parameters
> learning: as a result, classification performance on new inquiries improved
> inference: the adjusted model predicted the type of a new inquiry

So the `learning` in the title of this section is a broad introductory expression. When the body discusses internal value adjustment, it uses `training` or `learning procedure` more precisely.

## Experience and Signals Differ by Learning Type

The support-message example so far is closest to `supervised learning`: the input sentence and desired output label are given together, and the model is trained to reduce the difference between prediction and label. But not all AI learning has that shape.

| Type | Experience data | Adjustment signal | Introductory intuition |
| --- | --- | --- | --- |
| supervised learning | input plus correct label | difference between prediction and label | like practicing with an answer key |
| unsupervised learning | unlabeled data | internal structure, clusters, or representations in the data | finding structure without an answer sheet |
| reinforcement learning | states, actions, rewards | reward received after action | trying actions and moving toward higher reward |

So the explanation `training reduces the difference between prediction and label` is a simplified entry point for supervised learning only.

In reinforcement learning, the center shifts from correct labels to actions and rewards. In unsupervised learning, the center shifts to the structure or representation in the data rather than a human-provided answer.

`Deep learning` is a different axis. It is not a learning type in the same sense. It is an approach that uses multilayer neural networks to learn representations, and it can be combined with supervised learning, unsupervised learning, self-supervised learning, or reinforcement learning.

> learning type: by what experience and signal does performance improve?  
> deep learning: by what structure are representations and parameters learned?

Here, the supervised-learning example is used first to build the intuition that internal values are adjusted. The finer differences among reinforcement learning and deep learning return in P1-8, P1-9, Part 4, and Part 5.

Section 5.1 explains the intuition behind learning and training. It does not go into the formulas or implementations of `loss function`, `gradient descent`, `backpropagation`, or `optimizer`. Those return later in Part 4 and Part 5.

It also does not explain inference in detail. Inference is handled separately in 5.2. Here we mention only enough to distinguish it from training: values changed during training are used later when the model is run.

## Adjusting Internal Values Through Training

- Understand training as the process of adjusting internal model values.
- Distinguish learning from training.
- Avoid mixing supervised learning, unsupervised learning, reinforcement learning, and deep learning as if they were the same category.
- See how parameters, weights, and biases connect to learning.
- Understand loss as the signal that guides learning.
- Distinguish learning from simply storing all data as-is.
- Prepare the boundary among training, fitting, and inference.

## Training Is the Process of Adjusting Criteria from Examples

Google’s Machine Learning Glossary explains training as the process of determining the ideal parameters that make up a model. During training, the system reads examples and adjusts parameters gradually.

Continuing the customer-support classification example:

| Input sentence | Desired output |
| --- | --- |
| `I want a refund.` | refund |
| `When will the delivery arrive?` | delivery |
| `The item arrived broken.` | exchange |
| `Can I cancel the payment?` | refund |

At first, the model may not know which clues should connect strongly to which outputs. Training adjusts those internal criteria little by little.

> example input  
> -> model prediction  
> -> comparison with desired output  
> -> internal value adjustment in the direction that reduces the difference

The numeric form of that difference is `loss`.

> large loss = the model output differs a lot from the desired output  
> small loss = the model output is closer to the desired output

## What Changes Is Mainly the Parameters

Section 4.3 defined a parameter as `an adjustable internal value the model uses to turn input into output`. We can now add one more sentence:

> training is the process of changing parameters

Google’s glossary explains parameters as the weights and biases that a model learns during training. In simple terms, weights determine how strongly some value influences another, and training searches for weights that better fit the task.

In a simplified support-message classifier, it may look like this:

| Clue | Before learning | Expected state after learning |
| --- | --- | --- |
| `refund` | unclear connection to an output | strongly connected to the refund output |
| `delivery` | unclear connection to an output | strongly connected to the delivery output |
| `damage` | unclear connection to an output | strongly connected to exchange or reshipment |
| `cancel` | may be confused between refund and delivery condition | adjusted to work together with surrounding clues |

This does not show the literal inside of a real model. It is a simplified way to see what learning changes.

One beginner confusion appears here: people hear `the model changed` and imagine the whole structure was rebuilt from scratch. At the introductory level, it is safer to understand that the overall model framework stays in place while internal values change inside it.

## Bias Changes the Default Position

If weights adjust the influence of input clues, `bias` can be read as the value that shifts the default position of the output when input clues are weak or absent.

Suppose most support messages in a service are delivery-related. Even when the model sees little evidence, it may tilt slightly toward delivery. That default tilt can also become something learned.

> weight: how strongly should a clue matter?  
> bias: where should the default output position begin when evidence is weak?

This is an intuition mainly useful for linear models and neural networks. Not every model exposes internal structure in exactly this way.

## Learning Is Not the Same as Memorizing an Answer Sheet

If we reduce learning to `memorizing data`, we misunderstand machine learning. Of course, large models can remember or reproduce parts of training data, and that matters later in discussions of copyright, privacy, and security.

But the main goal of learning is not to store the training data exactly. It is to find relationships that can also be used for new inputs. The *Deep Learning* book distinguishes fitting training data from finding patterns that generalize to new data.

Using the support-message example:

| Method | How it behaves | Limit |
| --- | --- | --- |
| simple memorization | gives the same answer only when the sentence is exactly the same as before | weak when wording changes even slightly |
| direct rule writing | answers according to words and conditions written by people | hard to maintain when exceptions and context variation grow |
| supervised-learning model | adjusts internal values to fit relationships between input and output across many examples | highly dependent on data quality and task definition |

For example, these two sentences differ in wording but may carry similar business intent:

> I want a refund.  
> Can I cancel the payment?

A learning-based model tries to adjust itself so that different expressions can still lead to the same output when the training objective supports that pattern.

The safer interpretation is:

> a learned model is adjusted to compute relationships between input representations and outputs  
> according to training data and the learning objective

## Learning Moves in the Direction That Reduces Loss

Any learning process needs a criterion for what counts as better. The loss function quantifies that criterion.

For example, suppose a classifier predicts like this:

| Input | Desired output | Model prediction | Intuitive loss |
| --- | --- | --- | --- |
| `I want a refund.` | refund | refund | small |
| `When will the delivery arrive?` | delivery | refund | large |
| `The item arrived broken.` | exchange | delivery | large |

In real training, the model usually uses more detailed scores or probabilities rather than simple right-or-wrong judgments. Once loss is computed, the training procedure adjusts internal values in the direction that reduces it.

Google’s glossary describes `gradient descent` as a mathematical technique for minimizing loss by repeatedly adjusting weights and biases.

The important point here is not the formula, but the role.

> loss: a signal of how bad the current prediction is  
> training procedure: a way to change internal values so that loss becomes smaller

## Training Is Repeated, Not Finished in One Step

Training usually does not end with one example. The model looks at many examples repeatedly and adjusts itself little by little.

> initial model  
> -> check a batch of examples  
> -> compare predictions and labels  
> -> compute loss  
> -> adjust parameters  
> -> check examples again

If loss decreases, we can say the model is fitting the training data better. But fitting training data too well is not always good, because overfitting may make the model weak on new data. That broader issue returns later in Part 4. Here the point is only that internal values are adjusted repeatedly during learning.

## Representations May Change Too in Deep Learning

Section 4.3 described `representation` as the transformed form that makes original data easier to compute over. In more classical machine learning, people often design features and the model learns parameters on top of them.

In deep learning, that boundary becomes less sharp. As input passes through several layers, the network builds internal representations, and learning adjusts the weights used to create those representations as well.

In a simplified support-message example:

> sentence  
> -> word or token representation  
> -> internal vector representation  
> -> message-type output

So in deep learning, learning may change not only the final output criteria, but also the internal values that create intermediate representations.

That is why deep learning often makes the question `does a person design the features directly?` less central than `can the model learn useful representations?`

Here, first keep the view that `intermediate representations can also change`. The way this connects to hidden representations, embeddings, and the role of deeper layers returns in `P1-3.3` and Part 5.

## Fitting Also Appears as a Practical Term

When you use machine-learning tools, you often see `fitting` together with `training`. scikit-learn describes `fit` as the operation that matches an estimator’s state to data, and a fitted estimator as one that holds the information needed for prediction in internal attributes.

In this section, we separate the terms like this.

| Expression | Meaning |
| --- | --- |
| training | the process of adjusting internal model values to match data and goals |
| fitting | the execution of matching model state to data in a specific tool or statistical workflow |
| fitted or trained model | a model whose internal values have been adjusted and is ready to handle new inputs |

In practical code, training is often triggered through APIs like `model.fit(X, y)`. In this book's conceptual explanations, `learning` is used as the broader term, while `training` is used for the procedure that adjusts internal values.

## Parameter Still Has Multiple Levels

As noted in 4.3, the word `parameter` changes meaning with context. Google’s glossary uses it for weights and biases learned by the model. By contrast, the scikit-learn glossary also uses `parameter` for configuration values passed to an estimator constructor.

To reduce confusion, this book separates them like this.

| Distinction | Example | Preferred expression here |
| --- | --- | --- |
| internal values adjusted by learning | weights, biases | model parameters |
| settings for learning procedure or model structure | learning rate, max depth | hyperparameters or model settings |
| values that control output choice during generation | temperature, top-p, max tokens | generation settings |
| library constructor arguments | `max_depth=3`, `random_state=42` | API parameters or configuration arguments |

So when this section says `learning changes parameters`, it means the first sense: model parameters. Generation settings such as an LLM's `temperature` are not internal parameters obtained by learning.

## Learning and Inference Are Different

Training and inference are often mentioned together, but they are not the same process. Google’s glossary distinguishes training, which finds good weights, from inference, which uses learned weights to produce predictions.

The boundary to keep first is:

| Distinction | What it does | Do internal values usually change? |
| --- | --- | --- |
| training | adjusts internal values so that loss becomes smaller on examples | yes |
| inference | uses learned internal values to create output for new input | usually no |

Real systems can include online learning, continual learning, caches, retrieval, and tool calls, so the full picture can be more complex. But this baseline distinction is still necessary:

> training changes values  
> inference uses the changed values

Section 5.2 looks separately at what inference actually executes.

## A Small Example Again

Suppose we build a support-message classifier.

> goal: classify the message type from the support sentence  
> input: support sentence  
> output: refund, delivery, exchange, other  
> training data: support sentences with human-assigned labels

Before learning, the model may be wrong like this:

| Input | Desired output | Prediction before training |
| --- | --- | --- |
| `I want a refund.` | refund | other |
| `Tracking does not work.` | delivery | other |
| `The product is damaged.` | exchange | delivery |

Learning adjusts internal values so that these differences shrink. After learning, the model may behave more like this:

| Input | Desired output | Prediction after training |
| --- | --- | --- |
| `I want a refund.` | refund | refund |
| `Tracking does not work.` | delivery | delivery |
| `The product is damaged.` | exchange | exchange |

But that alone is not enough. We still need to check whether it works on new sentences that were not in the training data.

> The item I received yesterday was broken, and I want it resent.

If the model can handle that as exchange or reshipment, then it has captured at least some more general relation rather than only exact memorization. This judgment must be checked with validation data and evaluation criteria.

## Checklist

- I can explain training as the process of adjusting internal model values.
- I can explain how parameters, weights, and biases connect to learning.
- I can explain that loss is the signal that guides the direction of learning.
- I can explain that learning is not the same as memorizing the training data as-is.
- I can state the basic difference between training and inference.
- I can distinguish that the word `parameter` can refer to model-internal values, hyperparameters, or API settings.
- I can explain that learning is not a process of injecting knowledge into a model like a human mind, but a process of adjusting internal values that turn input representations into outputs according to data and goals.
- I can explain that before asking what a model learned, we should ask from what data, toward what output goal, through what loss criterion, and with which internal values adjusted.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 5: Machine Learning Basics](https://www.deeplearningbook.org/contents/ml.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, accessed 2026-06-22.
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
