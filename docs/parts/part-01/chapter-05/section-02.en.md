# P1-5.2 What Does Model Execution Run?

> Section ID: `P1-5.2`
> Version: `v2026.07.19`

Section 5.1 distinguished `learning` from `training`. Training is the procedure that uses data to adjust internal model values, while learning is the broader idea that performance on a task improves as a result.

This section moves to the next question: once training is over, what exactly is being executed when we use the model?

In AI documents, this process is usually called `inference`. In local-language prose it is often translated with a term that can also suggest `reasoning`, `prediction`, or even `statistical inference`, so this book keeps the English word visible here. That collision of meanings is organized separately in 5.3.

Here, `inference` is treated as `the execution step that produces output for a new input by using learned values`, and it is kept separate from the full service workflow around it.

## How to Read It in This Section

Although `inference` can sound like a thought process when read only through translation, Section 5.2 reads it more narrowly like this:

> inference = the execution that applies a trained model to a new input and produces output

In practical terms, it is closer to `running the model`, `applying the model`, or `executing the step that creates output`. The safer reading is not `the model is thinking`, but `the trained computational structure is being applied to a new input`.

> training: prepares the model  
> inference: runs the prepared model  
> post-processing: connects model output to a result people actually use

These three lines help separate `the step where the model computes a result` from `the larger service step that uses that result`.

This section is not a mathematical explanation of inference. Matrix multiplication and activation functions return later in Part 5. Attention and decoding algorithms return from P1-11 through P1-14 and in Part 6.

It is also not a full AI service architecture section. API servers, caches, RAG, tool calls, permission checks, and monitoring return later in P1-14 and Part 7.

The smaller question here is enough:

> when a trained model receives a new input,  
> what values does it use to produce what kind of output?

## Goal of This Section

- Understand inference as the execution process that uses a trained model.
- Read inference as `running the model`, `applying the model`, or `executing output creation`.
- Distinguish training from inference.
- Understand that inference usually does not change model parameters.
- Connect traditional machine-learning prediction with LLM response generation in one larger structure.
- Distinguish inference output from the whole business-handling process.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| inference is the execution that applies a trained model to new input | This reduces the oversized meaning often suggested by local-language translations. | Understand it as the stage of putting in new input and receiving output. |
| training and inference are different stages | This prevents us from mixing model-building time with model-usage time. | Training changes internal values; inference usually does not. |
| inference output is not the same as the full service process | This helps separate model output from business decision. | See that scores or text may be followed by policy rules and human review. |

At this stage, a short role separation is enough:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| inference | the execution that applies a trained model to new input | the central stage where the model actually produces output |
| prediction | model output such as a class or score | the traditional machine-learning result expression |
| response generation | output that builds a reply token by token | the LLM-side result expression |
| post-processing | the stage that turns model output into the final human-facing result | outer procedures such as routing or policy checks |

## Inference Applies a Trained Model

Google’s Machine Learning Glossary explains inference in traditional machine learning as the process of applying a trained model to unlabeled examples to make predictions. For LLMs, it explains inference as using a trained model to generate a response to an input prompt.

Those descriptions look different on the surface, but they share the same structure:

> trained model + new input -> output

For a support-message classifier:

| Step | Example |
| --- | --- |
| trained model | a classifier trained on past messages and labels |
| new input | `Tracking does not work.` |
| inference result | `delivery` |

For an LLM:

| Step | Example |
| --- | --- |
| trained model | a language model after pretraining and further adjustment |
| new input | `Write a draft reply to this support message.` |
| inference result | a natural-language draft response |

So inference is not the process where the model learns again. It is the process of using the already-trained model to produce output for new input.

## Training and Inference Have Different Purposes

| Distinction | Training | Inference |
| --- | --- | --- |
| purpose | adjust internal model values | use learned values to produce output |
| input | training data, labels, or learning signals | new input, prompt, or observed data |
| main computation | loss calculation and parameter update | output computation, prediction, or generation |
| internal parameters | change | usually do not change |
| result | trained model | prediction, score, class, or response |

Google’s glossary makes the same distinction when explaining weights: training determines good weights, while inference uses learned weights to make predictions.

This matters because beginners often imagine that the AI is still learning every time it answers. In most deployed systems, that is not what happens. When a user asks a question and receives an answer, the process is usually inference, not immediate parameter updating.

There are exceptions such as online learning, continual learning, or systems that later retrain from feedback. But the basic distinction remains useful:

> producing output during use = inference  
> gathering data and adjusting the model again = training or retraining

## The Basic Flow of Inference

The internal computation differs by model type, but the basic flow can still be read like this:

> new input  
> -> transform input into a form the model can read  
> -> compute with learned parameters  
> -> produce candidate outputs, scores, probabilities, or tokens  
> -> convert them into a result people can use

Using the support-message classification example:

| Step | Explanation |
| --- | --- |
| receive input | `Tracking does not work.` |
| convert representation | turn the sentence into tokens, vectors, or feature values |
| compute in the model | use learned parameters to calculate scores for each message type |
| select output | choose the most appropriate label |
| return result | `delivery` |

The key point is that the model is not learning the new input on the spot. The trained internal values are already there, and inference uses those values to pass the input through to an output.

In deep learning, this direction of computation is often called the `forward pass`. By contrast, `backpropagation` is the training-side computation used to adjust parameters, so it is not the center of ordinary inference explanations.

## Output Changes with the Task Definition

Inference results depend on how the model’s task was defined. Google’s glossary explains `prediction` as model output: for binary classification it may be a positive or negative class, for multiclass classification one class, and for linear regression a numeric value.

As Section 4.4 showed, the output definition determines the modeling task. Inference is the execution that produces that defined output.

| Task | Input | Inference result |
| --- | --- | --- |
| message-type classification | message sentence | labels such as `refund`, `delivery`, `exchange` |
| delivery-delay prediction | order information | delay-risk score or expected arrival time |
| anomaly detection | transaction information | anomaly score |
| draft-reply generation | message sentence plus policy | natural-language reply draft |
| image classification | image | image class |

So to understand inference, we first need to check what kind of output the model was defined to produce.

> classification-model inference outputs labels  
> regression-model inference outputs numbers  
> generative-model inference produces outputs such as text, image, or audio

## Scores and Probabilities May Differ from the Final Decision

Model inference does not always end in one label only. Many models internally calculate several candidate scores or probabilities and only later select one or convert the result into the form shown to users.

Suppose a message classifier gives these scores:

| Candidate label | Model score |
| --- | ---: |
| delivery | 0.72 |
| refund | 0.18 |
| exchange | 0.07 |
| other | 0.03 |

The service might show all of them, return only the highest one, or send the case to human review if the score is too uncertain.

> model output: delivery 0.72, refund 0.18, exchange 0.07, other 0.03  
> service decision: route to delivery

So model output and business decision are not the same thing. Inference creates the model output. A separate service design decides how to use that output.

## LLM Inference Is the Execution That Produces a Response

Inference in an LLM looks more complex than in a classifier because the model generates natural-language output. But the larger structure is still the same:

> prompt  
> -> tokenization  
> -> next-token candidate computation with learned parameters  
> -> repeated token selection  
> -> response generation

Suppose the prompt is:

> Please write a polite draft reply for a delivery-delay inquiry.

The LLM turns that input into tokens, uses learned parameters to compute likely next-token candidates, and then selects tokens according to the generation method until it forms a response.

The key point is not the inner algorithmic detail. It is that even here, inference still means `applying a trained model to new input to produce output`.

Values like `temperature`, `top-p`, and `max tokens` should not be confused with learned model parameters. They are generation settings used during inference.

## Inference May Be Only One Part of a Larger Request Flow

Strictly speaking, a real service request often includes stages beyond model computation:

> receive request  
> -> validate input  
> -> preprocess  
> -> model inference  
> -> post-process  
> -> check policy  
> -> return response

But in this section, `inference` points only to the part where the model uses trained internal values to compute output.

For example, in an automatic support-message classification system:

| Stage | Explanation |
| --- | --- |
| model inference | compute the `delivery` label and its score from the message sentence |
| service handling | route to the delivery team, send a notification, store the log |

Model inference may be one part of service handling, but it is not the same thing as the whole service process.

## A Small Example Again

Continuing the example from 5.1:

> training data:  
> - `I want a refund.` -> refund  
> - `When will the delivery arrive?` -> delivery  
> - `The item arrived broken.` -> exchange

Once training is finished, the model holds adjusted internal values that turn input representations into outputs. Now a new message arrives:

> new input:  
> `I ordered yesterday, but tracking still does not work.`

Inference applies the trained model to that input.

| Step | Result |
| --- | --- |
| representation conversion | clues such as delivery, tracking, and failure are turned into computable form |
| model computation | the trained parameters calculate scores for candidate labels |
| output creation | the label `delivery` and its score are returned |
| post-processing | the result may be connected to routing or human review |

The model is not retrained immediately on this new sentence. In ordinary inference, it uses learned values to produce output.

## Checklist

- I can explain inference as the process of applying a trained model to new input and producing output.
- I can explain the difference between training and inference.
- I can explain that model parameters usually do not change during inference.
- I can understand traditional machine-learning prediction and LLM response generation within the same larger structure.
- I can distinguish model output from the final decision of a business system.
- I can explain why inference and reasoning should not be treated as the same term; that difference is organized separately in 5.3.
- I can explain that inference runs a trained model to produce output for a new input, and that `training changes internal values while inference uses those changed values`.
- I can distinguish the moment when a model is trained, the moment when it is run through inference, and the moment when model output is connected to a service decision.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
