# P5-6.3 Learning And Model Execution (Inference)

Section ID: `P5-6.3`
Version: `v2026.07.17`

In P5-6.2, we first grouped how the training loop repeats in units of step, batch, and epoch. Once we reach this point, the next question appears.

If the gradient has been computed, is this model currently learning, or is it simply being used?

This question is very important. Readers often think the model always works in the same way, but the boundary we have to separate first here is not a detailed difference in computational rules. It is `is this a procedure that changes parameters` or `is this a procedure that uses parameters the model already learned`.

Learning is the stage that changes model parameters, and model execution (inference) is the stage that computes results with the current parameters without changing them.

If the distinction between learning and model execution starts to blur again in later sections, it helps to return together to the [training](/AiBook/reference/concept-glossary/#training) and [inference](/AiBook/reference/concept-glossary/#inference) entries in the concept glossary.

## Scope Of This Section

- Why do we need to distinguish learning from model execution?
- In the deep-learning context, what does the learning stage include?
- What changes in the model-execution stage?
- Why do we need a different reading viewpoint for the same model when it is learning and when it is being used?

This section focuses on distinguishing `the time when parameters are actually changed` from `the time when the current model is used without changing them`. In other words, here we first close learning and inference using the standard `does an update path attach or not?`

At the same time, it is also clear which question we will not widen immediately in this section. `Inside the interval that uses the current parameters, what computational rule should be used?` is still the next question. Why the computational rule may differ between training and evaluation even for the same model continues in the next section, P5-6.4. The larger meaning of dropout and regularization reconnects again in P5-8.1 and P5-8.2.

## Goals Of This Section

- You can distinguish learning and model execution using the criterion `whether parameters change`.
- You can explain that learning includes not only forward pass, but also loss computation, backpropagation, and update.
- You can say that model execution is the stage that computes results but does not change parameters.
- You can confirm the difference between the two stages with an executable Python example.

## Why Is This Distinction Important

A common misunderstanding in introductory deep learning is the following.

- If you put in data and a result comes out, that itself is learning.
- If the model produced one result, it has already learned.
- If you make predictions many times, the model gradually becomes better.

But in reality, that is not the case.

For the model to improve, the following stages are needed.

1. Make a prediction with the current parameters.
2. Compute the loss by comparing it with the correct answer.
3. Compute the gradient.
4. Let the optimizer update the parameters.

In other words, the simple fact that `a result was produced` does not mean learning happened.

`Computing a result can happen in inference too, but learning includes the process that uses that result to actually change the numbers inside the model.`

There is one question to fix first here.

`Does the procedure we are looking at continue all the way to parameter update, or does it only compute the output using the current parameters?`

Once this question is answered, the primary boundary between learning and inference is fixed. We are not yet asking how dropout or batch normalization differ inside a region that uses the same parameters. That is because the question there is not `do the parameters change`, but the next-stage question `by what computational rule should the same parameters be used?`

## What Does Learning Include In Deep Learning

Here, it is enough to understand learning in the deep-learning context as the following bundle of four stages.

| Stage | Role |
| --- | --- |
| forward pass | compute predictions with the current parameters |
| loss computation | compute the difference between prediction and answer as a number |
| backpropagation | compute the gradient for each parameter |
| update | the optimizer actually changes the parameters |

Only when all four stages are present can we say `learning happened once`.

In other words, in deep learning, learning is not simply `seeing lots of data`. It is `repeatedly adjusting parameters based on loss`.

## What Does Model Execution (Inference) Do

Model execution (inference) is the stage that computes results for an input while keeping the current parameters fixed.

For example:

- if a user uploads a photo, it returns a classification result
- if someone enters equipment inspection notes, it returns a risk summary
- if a partial document is given, it generates the next token

At that time, the model is computing. But that computation does not immediately mean parameter update.

In other words, inference is `the stage that uses what the model currently knows to make an answer`.

`Learning is the time when the model changes, and inference is the time when it is used without changing.`

## Even The Same Forward Pass Has A Different Meaning

There is one more important point here. Both learning and inference use the forward pass. So to the reader they can look similar.

But the purpose is different.

- forward pass during learning: an intermediate stage for loss computation and update
- forward pass during inference: a computation that produces the final result

In other words, even if it looks like the same computation, `why are we computing it` is different. The question in this section is not the detailed setting of forward, but whether that forward continues into `loss -> gradient -> update`.

If we draw it very simply, it looks like the following.

```mermaid
--8<-- "assets/part-05/chapter-06/training-vs-inference-flow-en.mmd"
```

The result to confirm in this diagram is that even if the predicted value looks similar, during learning it continues into loss computation and update, while during execution it continues directly into the user-facing result.

- During learning, after the prediction there are additional stages that compute `how wrong it was` and then change the parameters.
- During execution, the prediction becomes the result shown to the user or the input to the next system stage.

## Why Does Confusion Arise If We Translate Inference Using Only One Localized Word

As we already saw in Part 1, the core problem is that one localized word can cover several different conceptual positions at once. In Korean, for example, the single word often translated as `inference` can also sound mixed with reasoning and prediction, and the same problem appears in other languages if one local term covers several standard technical meanings at once. So in this section, it is safer not to flatten into a single translated word the questions `what kind of thinking is happening`, `is the learned model being executed`, and `what output was produced`.

In the deep-learning context, inference usually points to `the stage of executing a learned model and computing output values with the current parameters`. In other words, in this section inference is not immediately the same thing as `deep thinking`, `logical reasoning`, or `future prediction`. It is closer to the model-execution procedure.

| Expression | Question to ask first | What is different from P5-6.1 | Safe expression in this section |
| --- | --- | --- | --- |
| `reasoning` | Does it mean a thought process that follows grounds toward a conclusion? | It points more toward explanation and logical development, not to the stage of executing model parameters itself. | `reasoning`, `logical reasoning`, `thought process` |
| `inference` | Is the learned model being applied to a new input? | It performs forward with the current parameters and computes output, but no update follows. | `model execution (inference)`, `model application` |
| `prediction` | What output value did the model produce? | It is the result created by inference. It is an output-side expression, not a process expression. | `prediction`, `model output` |
| `generation` | Is it producing an artifact such as text or tokens? | In LLM execution, the result of inference may look like generated text, but the act of generation and the stage of model execution are not treated as the same thing. | `generation`, `generating` |

The basic meaning of inference in this section is the following three stages.

- put in the input
- compute using the current parameters
- produce the output

In other words, the core here is not `how deeply did it think`, but `was the output computed by running the current model?`

So in this section it is safer to keep the paired expression `model execution (inference)` rather than using only one localized translation. The same point should carry into other language editions later too: do not mix together `reasoning`, `inference`, `prediction`, and `generation` again in this position, and instead translate around the role `the stage that executes the learned model`.

## Fixing The Boundary Between 6.3 And 6.4 First

P5-6.3 and the next section, P5-6.4, can look attached on first reading because both discuss the expressions `during learning` and `during use`. So here too it is safer to separate the questions into two levels.

| Question to answer first | Answer in this section | Answer in the next section |
| --- | --- | --- |
| Does this procedure change the model parameters? | If it is learning, it changes them. If it is inference, it does not. | This question is already a finished premise there. |
| Even in a region where parameters are not changed, do the computational rules always have to be the same? | We do not handle that yet here. | It explains why training mode and evaluation mode split. |

In other words, P5-6.3 is the section that separates `whether an update path exists`, and P5-6.4 is the section that then separates `even when the same model is being executed, what computational state should be used`.

## Cases And Examples

### Case. Splitting The Same Alarm Input Into Two Execution Logs

We can imagine a scene where an operator enters one new equipment alarm log and sees a classification result such as `stop immediately`, `check on site`, or `record only`. When people see the decision result appear immediately on the screen, they often feel that the model also learned more from that log right away. But to separate this scene into learning and inference, we first have to look not at `did it see a new input`, but at `did an update path attach?`

If we split the same alarm input into two execution logs, the difference becomes clear.

| Execution log | Stages that actually continue | Parameter change |
| --- | --- | --- |
| service execution log | `alarm_count -> forward -> predicted_block_score -> operation-screen output` | none |
| training log | `alarm_count -> forward -> compare with target_block_score -> loss -> gradient -> update` | yes |

In the service execution log, the current parameters are used to compute a risk score and show it on the operations screen. If the input changes, `predicted_block_score` may also change, but that by itself does not mean the parameters changed. In contrast, in the training log, even with the same kind of input, it has to be compared with `target_block_score`, compute loss and gradient, and then attach an update before the parameters actually change. So the result to confirm in this case is not whether the result screen changed, but whether `loss -> gradient -> update` actually attached and changed the parameters.

| Standard a person is likely to look at first | Standard reread from the viewpoint of learning/inference |
| --- | --- |
| Since a new input was processed, the model probably learned more right away | It may only have computed an output, with no parameter update |
| Since the result changed, the numbers inside the model must also have changed | A changed output from changed input and a changed parameter are separate matters |
| If it is used a lot, it will probably learn automatically | It becomes learning only when the loss, gradient, and update procedure actually exists |

This same scene carries over directly to an inspection-image demo or LLM chat. Uploading an image to an inspection screen, retyping a question into a chat window, or entering a new alarm log can all be inference. Even if the output changes every time, the parameters stay the same unless an update path is attached.

If we bundle this case again into learning and inference, the difference is not `did a result come out`, but `did that result continue into a computation that actually changes the parameters`.

| Scene | Result a person is likely to look at first | What must actually be separated from the viewpoint of learning/inference | Do the parameters change? |
| --- | --- | --- | --- |
| service execution log | a new alarm result came out immediately | check whether only forward happened with the current parameters | no |
| training log | the alarm sample was compared with the target value | check whether loss, gradient, and update actually followed | yes |
| service inputs such as inspection images or LLM chat | when the input changed, the output changed too | separate output change due to input change from real-time relearning | usually no in ordinary service use |

The result the reader should hold first in this table is that the key point that separates learning and inference is not `whether the output changed`, but `whether loss and update actually attached so that the parameters changed`.

If we compress this case one more time, the first flow for reading learning and inference is the following.

```mermaid
--8<-- "assets/part-05/chapter-06/learning-inference-parameter-bridge-en.mmd"
```

This diagram is not there to explain the service execution log and training log all over again, but to separate once more, at a glance, `the output changed because a new input was processed` from `the parameters changed because loss and update were attached`.

## Practice And Example

The goal of this example is to confirm over several steps that the same small risk-score model changes several parameters when it sees a `training batch`, and does not change those parameters when it sees `service inputs`. Here, the code does not merely print one number. It serves the role of testing whether the parameters actually become different depending on `whether an update path was attached`, even for the same kind of input.

Input:

- 4 alarm samples for training
- initial parameters `alarm_weight`, `delay_weight`, `bias`
- learning rate `learning_rate`

Output:

- prediction values, loss, and parameter changes for each step
- inference results after learning is complete
- parameter comparison before and after inference
- a check of whether only the outputs change when several service inputs are processed with the same risk weights

Problem scene:

- even when learning and inference use the same formula, their purposes differ, so we need to separate the interval where weights are updated and the interval where they stay fixed
- even if service inputs arrive many times, we have to check directly whether the parameters stay the same when there is no update

Concepts to confirm:

- during learning, the weights keep changing in order to reduce loss
- during inference, the learned weights are kept fixed and only the result is computed
- even if inputs change and outputs change, that does not mean the parameters changed

Input:

Assume that in the training batch, `alarm_count` and `restart_delay_hours` are used to create `predicted_block_score`, which is then compared with the target value `target_block_score` to update `alarm_weight`, `delay_weight`, and `bias`. After that, in the service interval, we only check whether those same parameters keep being used even when new inputs arrive.

Before looking at the code, it helps to predict in which interval the `weights` will change.

| Interval | Comparison to predict first | Why that is the expected result |
| --- | --- | --- |
| `train step 1~4` | `alarm_weight`, `delay_weight`, and `bias` will probably become different | Because actual updates are performed using loss and gradients. |
| `service input 1` | the output will be computed, but the parameters will probably stay the same | Because inference only uses the current parameters. |
| `service input 2` | even if the output changes, the parameters will probably still remain the same | Because input change and parameter change are different matters. |

The purpose of this table is to read `output change` and `parameter change` separately.

This example becomes more clearly experimental if you change the three values below directly while reading it.

| Value to change | Output to observe first | Question to interpret |
| --- | --- | --- |
| change `learning_rate` from 0.03 to 0.01 or 0.08 | how much the three parameters move at each step | Even when learning sees the same batch, does the amount of parameter change differ with the update step size? |
| add a new input to `service_inputs` | does `parameters_used` keep staying the same even though predictions differ? | Is the point preserved that changing service input and changing parameters are separate matters? |
| change `target_block_score` of `service_shadow_sample` to 10.0 or 13.0 | how does `shadow_parameters_after` change when update is attached to the same service input? | Do parameters change only when `the loss-update path` is attached, rather than because of the input itself? |

```python
train_alarm_data = [
    {"alarm_count": 1.0, "restart_delay_hours": 2.0, "target_block_score": 4.0},
    {"alarm_count": 2.0, "restart_delay_hours": 1.0, "target_block_score": 5.0},
    {"alarm_count": 3.0, "restart_delay_hours": 2.0, "target_block_score": 8.0},
    {"alarm_count": 4.0, "restart_delay_hours": 3.0, "target_block_score": 11.0},
]

parameters = {
    "alarm_weight": 0.4,
    "delay_weight": 0.2,
    "bias": 0.0,
}
learning_rate = 0.03
service_inputs = [
    {"alarm_count": 4.0, "restart_delay_hours": 1.0},
    {"alarm_count": 5.0, "restart_delay_hours": 3.0},
]
service_shadow_sample = {
    "alarm_count": 4.0,
    "restart_delay_hours": 1.0,
    "target_block_score": 10.0,
}

def predict_block_score(alarm_count, restart_delay_hours, parameters):
    return (
        alarm_count * parameters["alarm_weight"]
        + restart_delay_hours * parameters["delay_weight"]
        + parameters["bias"]
    )

def run_train_step(sample, parameters, learning_rate):
    prediction = predict_block_score(
        sample["alarm_count"],
        sample["restart_delay_hours"],
        parameters,
    )
    target_block_score = sample["target_block_score"]
    loss = (prediction - target_block_score) ** 2
    error = prediction - target_block_score
    gradients = {
        "alarm_weight": 2 * error * sample["alarm_count"],
        "delay_weight": 2 * error * sample["restart_delay_hours"],
        "bias": 2 * error,
    }
    new_parameters = {
        name: value - learning_rate * gradients[name]
        for name, value in parameters.items()
    }
    return {
        "prediction": prediction,
        "loss": loss,
        "gradients": gradients,
        "parameters_after": new_parameters,
    }

print("initial_parameters =", {name: round(value, 3) for name, value in parameters.items()})

for step, sample in enumerate(train_alarm_data, start=1):
    step_result = run_train_step(sample, parameters, learning_rate)
    print(
        f"train step {step}: "
        f"alarm_count={sample['alarm_count']}, "
        f"restart_delay_hours={sample['restart_delay_hours']}, "
        f"target_block_score={sample['target_block_score']}, "
        f"prediction={step_result['prediction']:.3f}, loss={step_result['loss']:.3f}, "
        f"parameters_before={ {name: round(value, 3) for name, value in parameters.items()} }, "
        f"parameters_after={ {name: round(value, 3) for name, value in step_result['parameters_after'].items()} }"
    )
    parameters = step_result["parameters_after"]

parameters_before_inference = parameters.copy()
for service_input in service_inputs:
    print(
        f"inference: alarm_count={service_input['alarm_count']}, "
        f"restart_delay_hours={service_input['restart_delay_hours']}, "
        f"prediction={predict_block_score(service_input['alarm_count'], service_input['restart_delay_hours'], parameters):.3f}, "
        f"parameters_used={ {name: round(value, 3) for name, value in parameters.items()} }"
    )
print("parameters_before_inference =", {name: round(value, 3) for name, value in parameters_before_inference.items()})
print("parameters_after_inference =", {name: round(value, 3) for name, value in parameters.items()})

shadow_result = run_train_step(
    sample=service_shadow_sample,
    parameters=parameters,
    learning_rate=learning_rate,
)
print(
    "same_input_with_update: "
    f"alarm_count={service_shadow_sample['alarm_count']}, "
    f"restart_delay_hours={service_shadow_sample['restart_delay_hours']}, "
    f"target_block_score={service_shadow_sample['target_block_score']}, "
    f"prediction={shadow_result['prediction']:.3f}, loss={shadow_result['loss']:.3f}, "
    f"shadow_parameters_after={ {name: round(value, 3) for name, value in shadow_result['parameters_after'].items()} }"
)
```

In the output, first compare the change in `parameters_before`/`parameters_after` during the learning stage with the unchanged `parameters_used` during the inference stage.

```text
initial_parameters = {'alarm_weight': 0.4, 'delay_weight': 0.2, 'bias': 0.0}
train step 1: alarm_count=1.0, restart_delay_hours=2.0, target_block_score=4.0, prediction=0.800, loss=10.240, parameters_before={'alarm_weight': 0.4, 'delay_weight': 0.2, 'bias': 0.0}, parameters_after={'alarm_weight': 0.592, 'delay_weight': 0.584, 'bias': 0.192}
train step 2: alarm_count=2.0, restart_delay_hours=1.0, target_block_score=5.0, prediction=1.960, loss=9.242, parameters_before={'alarm_weight': 0.592, 'delay_weight': 0.584, 'bias': 0.192}, parameters_after={'alarm_weight': 0.957, 'delay_weight': 0.766, 'bias': 0.374}
train step 3: alarm_count=3.0, restart_delay_hours=2.0, target_block_score=8.0, prediction=4.778, loss=10.384, parameters_before={'alarm_weight': 0.957, 'delay_weight': 0.766, 'bias': 0.374}, parameters_after={'alarm_weight': 1.537, 'delay_weight': 1.153, 'bias': 0.568}
train step 4: alarm_count=4.0, restart_delay_hours=3.0, target_block_score=11.0, prediction=10.174, loss=0.682, parameters_before={'alarm_weight': 1.537, 'delay_weight': 1.153, 'bias': 0.568}, parameters_after={'alarm_weight': 1.735, 'delay_weight': 1.302, 'bias': 0.617}
inference: alarm_count=4.0, restart_delay_hours=1.0, prediction=8.859, parameters_used={'alarm_weight': 1.735, 'delay_weight': 1.302, 'bias': 0.617}
inference: alarm_count=5.0, restart_delay_hours=3.0, prediction=13.197, parameters_used={'alarm_weight': 1.735, 'delay_weight': 1.302, 'bias': 0.617}
parameters_before_inference = {'alarm_weight': 1.735, 'delay_weight': 1.302, 'bias': 0.617}
parameters_after_inference = {'alarm_weight': 1.735, 'delay_weight': 1.302, 'bias': 0.617}
same_input_with_update: alarm_count=4.0, restart_delay_hours=1.0, target_block_score=10.0, prediction=8.859, loss=1.302, shadow_parameters_after={'alarm_weight': 2.009, 'delay_weight': 1.37, 'bias': 0.686}
```

Here, first confirm that `alarm_weight`, `delay_weight`, and `bias` actually change in the learning step, while during inference the same parameters are preserved even though new inputs arrive. The final line, `same_input_with_update`, is intentionally there as a contrast scene showing that parameters change only when update is attached even to the same kind of input.

- In the learning step, `parameters_before` and `parameters_after` differ, so the parameters actually change.
- In inference, even when different inputs are entered, `parameters_used` stays the same, and `parameters_before_inference` and `parameters_after_inference` are also the same.
- In `same_input_with_update`, even if the kind of input is the same, once loss and gradient are attached, `shadow_parameters_after` actually becomes different.
- In other words, putting in many service inputs does not automatically trigger relearning. Parameters change only when an update path is attached.

If we reread it as graphs, the procedural difference becomes clearer. In the learning procedure, `alarm_weight`, `delay_weight`, and `bias` change after the update at each step, and the value after update becomes the reference for the next step.

![Graph showing several parameters changing by step in the learning procedure](/AiBook/assets/part-05/chapter-06/learning-weight-update-trace-en.png)

In the model-execution procedure, `predicted_block_score` changes as the service inputs change, but the parameters in that same interval stay fixed like horizontal lines. What to confirm in this graph is not first the fact that the output line changes, but the fact that the parameter lines do not move.

![Graph showing that predictions change in the model-execution procedure but parameters stay fixed](/AiBook/assets/part-05/chapter-06/inference-fixed-weight-trace-en.png)

| Interval | Core point to read now |
| --- | --- |
| `train step 1~4` | After looking at output and loss, an actual update follows, so the parameters keep changing. |
| `inference input 1` | Even when a new input is processed, the current parameters are used as they are. |
| `inference input 2` | The output changes, but what changed was the input, not the parameters. |

If we bundle this result again around `output change` and `parameter change`, the difference becomes even clearer.

| Difference shown in the execution result | Interpretation easy to leave behind if you look only at the result | Interpretation reread from the viewpoint of learning/inference |
| --- | --- | --- |
| prediction keeps changing in `train step 1~4` | It is easy to feel it was only the result of seeing many alarm samples | Read that the parameters themselves changed because loss and update were attached |
| prediction changes for the two inference inputs | It is easy to feel the model changed too because the output changed | Read that only the input changed while `parameters_used` stayed the same |
| `parameters_before_inference` and `parameters_after_inference` are the same | It is easy to feel there may still have been learning because a result came out | Read that inference only performed computation and the parameters stayed fixed |
| `shadow_parameters_after` changes in `same_input_with_update` | It is easy to feel the same input should only produce the same result | Read that parameter change is decided not by the input kind, but by whether `the loss-update path was attached` |

Once this table is read, it becomes clearer that the core of learning and inference is not `both use forward`, but distinguishing `when update actually attaches`.

Even in traditional statistics and machine-learning education, the viewpoint of separating `training data` and the `prediction stage` has long been important. In deep learning, this distinction becomes even more important because backpropagation, the optimizer, and mode switching are added on top of it.

The reason this section is needed from the curriculum viewpoint is also clear. If we just saw in P5-5.1 and P5-5.2 how the gradient is computed, we now have to distinguish `when that computation leads to an actual update` and `when it is only simple execution`.

- right after learning backpropagation, every computation can start to feel like learning
- model execution can be underestimated as if it were only `a simple stage that just does forward`
- and to understand dropout, batch normalization, and evaluation mode later, we first have to know clearly when updates happen and when they do not

In other words, this section is the first section that starts reading the deep-learning procedure from an operational viewpoint.

## When Do We First Separate Learning And Inference

The time to bring out this section is when the explanation `the model produces a result` is not enough to see clearly when parameters actually change and when they stay fixed.

| Problem scene that appears first | Why the learning/inference distinction is useful first | The next question to hand off immediately |
| --- | --- | --- |
| It feels like as soon as a result comes out, learning also happened | We can clearly separate learning and execution using the criterion of whether the parameters changed | We next have to see why the mode can still differ in the same model |
| Only forward is visible, and loss, backpropagation, and update are mixed together | We can close the point that learning is the procedure that includes update too | We then have to see how the computational rules differ in training/eval mode |
| Chat, classification demos, and service responses look like real-time relearning | We can make clear that inference is the stage that uses the current parameters | We next need to see when the optimizer actually takes charge of updates |
| Processing training data and processing user requests look like the same thing | We can separate the difference in purpose between training computation and service-execution computation | We then need to look at layers sensitive to mode difference in the next section |

## Checklist

- Can you explain the criterion by which learning and model execution (inference) are separated?
- Can you distinguish the stage that changes parameters from the stage that uses fixed parameters?
- Can you explain that learning is the stage that changes parameters, while inference is the stage that uses them without changing them?
- Can you say that deep-learning learning includes forward pass, loss computation, backpropagation, and update?
- Can you explain that forward is also performed in inference, but the purpose and later stages differ?
- Can you say that the mere fact that a result came out does not mean learning happened?
- When the same model execution and service processing are being described as the same thing, can you first recall the distinction between learning and inference?
- Do you know that after this section, the flow goes on to separately examine the computational difference between training mode and evaluation mode?

## Sources And Further Reading

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, accessed 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Christopher M. Bishop, `Pattern Recognition and Machine Learning`, Springer, 2006, accessed 2026-06-29.
- Aurélien Géron, `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`, 3rd ed., O'Reilly, 2022, accessed 2026-06-29.
