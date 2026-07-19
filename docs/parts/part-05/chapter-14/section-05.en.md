# P5-14.5 How Do RNN State Passing and Transformer Relation Computation Split in Parallel Processing?

> Section ID: `P5-14.5`
> Version: `v2026.07.19`

P5-14.1 through P5-14.4 looked at roles inside the Transformer block. Now we need to compare how the same representation computation is executed within one sequence.

Why does an RNN feel like sequential state passing, while a Transformer fits token-relation computation and GPU parallel processing more naturally?

The comparison standard is not a timeline impression such as `the Transformer is newer`. The key is the difference between a computation that passes the previous step’s state forward one step at a time and a computation that is easier to organize as large matrix operations over many token relations in one layer.

## Questions About Computation Flow and Parallel Processing

- Why is an RNN read as a structure that passes state forward step by step?
- Why is a Transformer read as a structure that computes token relations more all at once?
- Why does this difference connect to GPU parallel processing and large-scale training?

## RNNs Pass State Forward Sequentially

RNN-family models make each step receive the previous state and produce the next state. So the computation feel naturally looks like this.

- Read the first token and create a state.
- Use that state while reading the second token.
- Pass the state again to the third token.

`An RNN is a structure that computes sequentially while passing the state created in front to the back.`

This structure is natural for data where order matters, but it becomes a burden from the viewpoint of parallel processing. If a later step must wait for the earlier step’s result, even with many compute devices, it is hard to freely process the steps inside one sequence at the same time.

## Transformers Are Closer to Computing Relations Together

Self-attention in a Transformer lets each token refer to other tokens in the same sequence. So its computation feel is closer to handling token-to-token relations together as large matrix computation than to passing a state along one line.

`An RNN passes state in order, while a Transformer computes token relations more together.`

| Viewpoint | RNN Family | Transformer |
| --- | --- | --- |
| computation flow | the previous step’s result is needed for the next step | token relations are computed more together |
| information movement feel | state is passed along | needed positions are compared again |
| parallel processing | sequential dependency easily becomes a bottleneck | easy to bundle into large matrix operations |
| scale expansion | sequential burden grows as long sequences increase | easier to organize through batch and tensor computation |

GPUs are strong when many similar computations can be processed simultaneously. The batch and tensor computation seen earlier in Part 5 carry the same feeling. Transformer self-attention and feed-forward are easy to bundle into large matrix operations, so they matched this compute resource well.

The important observation in a parallel-processing explanation is not simply `it became faster`. It is which computations must wait and which computations can be bundled together.

| Question to Observe | Burden in an RNN-Style Flow | Advantage in a Transformer-Style Flow |
| --- | --- | --- |
| Does the next token computation have to wait for the previous step? | sequential dependency easily becomes a bottleneck | relations among many tokens in one layer are easier to compute together |
| Are many similar multiplications repeated? | they tend to look split apart by step-level repetition | they are easy to bundle into large matrix operations on a GPU |
| Can many sentences be trained together? | order dependency inside sentences accumulates | easier to organize through large batches and tensor computation |

`The Transformer matched large-scale GPU training well because token relations are easy to turn into parallel matrix operations.`

## Cases and Examples

### Case. An Operations-Permit Sentence and a Large Training Batch

Split an operations-permit sentence into lines.

| Line | Document Content | Relation to the Final Judgment |
| --- | --- | --- |
| 1 | `Do not restart line 3 before pressure is relieved.` | blocking rule |
| 2 | `Sensor calibration was completed in the morning.` | intermediate operations log |
| 3 | `Packaging material replenishment was separately approved.` | intermediate operations log |
| 4 | `Current pressure has not yet returned to the safe range.` | current state |
| 5 | `Shift handoff records were updated.` | intermediate operations log |
| 6 | `Can line 3 restart be approved now?` | final question |

The easy human standard is `the document is written in order, so read it from front to back`. But from the viewpoint of computation flow, the question must become more concrete. When comparing the blocking rule in line 1 and the current state in line 4 with the question in line 6, does the computation wait for previous step results, or can it be bundled as several relation computations in the same layer?

In the RNN-style state-passing feel, earlier clues are compressed into a state and passed onward line by line. To process the line-6 question, the state created at line 1 must arrive after passing through computations for lines 2, 3, 4, and 5. So even within the same sentence, the later step waits for earlier step computation.

In the Transformer-style relation-computation feel, the relation between the line-6 question position and line 1 or line 4 can be organized inside the attention computation of the same layer. The point of P5-14.5 is not `how well the model remembers a distant clue`, but that comparisons among position pairs are easy to organize as large matrix operations. How a distant clue is called again for the final judgment is passed to the long-context question in P5-14.6.

| Comparison Scene | Read as RNN-Style State Passing | Read as Transformer-Style Relation Computation |
| --- | --- | --- |
| compare line-6 question with line-1 blocking rule | the clue must pass through steps 2 to 5 into the line-6 state | relation score between position 6 and position 1 can be computed together |
| compare line-6 question with line-4 current pressure state | the clue must pass through step 5 into the line-6 state | relation score between position 6 and position 4 can be computed together |
| compare position relations across several sentences in a batch | step dependency inside each sentence repeats | sentence-level relation scores are easier to organize as tensors |

The result to confirm in this case is not `the Transformer is better because it is newer`. For the same final question, an RNN-style explanation asks `does the previous step state need to finish before the later step starts?`, while a Transformer-style explanation asks `can many position relations be bundled into same-layer matrix computation?` The core of the parallel-processing explanation is not the model name, but `which computations must wait and which computations can be bundled`.

## Practice and Examples

### Example. Compare a Sequential Trace and a Relation-Score Matrix

This example is not an implementation of an actual Transformer. It is a small experiment for checking the central question of P5-14.5. We do not compare runtime. We observe that `the sequential trace accumulates by step order`, while `relation scores are organized at once as a matrix shape`.

| Value to Manipulate | Output to Observe | Question to Confirm |
| --- | --- | --- |
| the line order in `line_features` | `recurrent trace` | Is the previous step state passed to the later step in order? |
| `relation_kernel` | `request row`, `top related lines` | Which earlier lines have a large relation score with the current question? |
| number of sentences placed in `batch` | `score tensor shape` | Are relation scores for several sentences bundled into one tensor computation? |

```python
import numpy as np

line_features = np.array([
    [0.0, 1.0, 1.0, 0.0, 0.0],  # rule: pressure + block
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [0.0, 1.0, 0.0, 0.0, 0.0],  # state: pressure
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [1.0, 0.0, 0.0, 0.0, 1.0],  # request: restart + question
])

line_names = [
    "rule",
    "sensor_log",
    "packing_log",
    "pressure_state",
    "shift_log",
    "request",
]

relation_kernel = np.array([
    [1.0, 1.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 0.3, 0.0, 0.0],
    [0.0, 0.5, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.2, 0.0],
    [1.0, 0.5, 0.5, 0.0, 1.0],
])

state = np.zeros(5)
recurrent_trace = []
for step, (name, features) in enumerate(zip(line_names, line_features), start=1):
    state = 0.55 * state + features
    recurrent_trace.append((step, name, np.round(state, 3)))

relation_scores = line_features @ relation_kernel @ line_features.T
request_scores = relation_scores[-1]
ranked = sorted(zip(request_scores, line_names), reverse=True)

batch = np.stack([
    line_features,
    line_features[[0, 2, 4, 3, 1, 5]],
    line_features[[1, 2, 0, 3, 4, 5]],
])
batch_scores = batch @ relation_kernel @ np.transpose(batch, (0, 2, 1))

print("[recurrent trace]")
for step, name, snapshot in recurrent_trace:
    print(f"step {step}: {name:14s} state={snapshot}")

print("\n[relation score matrix]")
print("shape =", relation_scores.shape)
print("request row =", np.round(request_scores, 1).tolist())
print("top related lines =", [(name, float(score)) for score, name in ranked[:3]])

print("\n[batched relation scores]")
print("batch shape =", batch.shape)
print("score tensor shape =", batch_scores.shape)
```

Read the output like this.

```text
[recurrent trace]
step 1: rule           state=[0. 1. 1. 0. 0.]
step 2: sensor_log     state=[0.   0.55 0.55 1.   0.  ]
...
step 6: request        state=[1.    0.353 0.05  0.808 1.   ]

[relation score matrix]
shape = (6, 6)
request row = [3.0, 0.0, 0.0, 1.5, 0.0, 4.0]
top related lines = [('request', 4.0), ('rule', 3.0), ('pressure_state', 1.5)]

[batched relation scores]
batch shape = (3, 6, 5)
score tensor shape = (3, 6, 6)
```

The first output shows the RNN-style state feel. The line-6 request state is produced only after updates from lines 1 through 5 have passed in order. The second output shows the relation-computation feel. Relations among 6 positions are placed as a `(6, 6)` matrix, and the request row gives large scores to `rule` and `pressure_state`. The third output, `(3, 6, 6)`, shows that if three sentences are bundled as a batch, each sentence’s position-relation matrix can also be organized together in tensor form.

Explanation: The result to read here is not `which side is how many times faster in reality`. The core of P5-14.5 is that sequential state passing is read as a step trace, while Transformer-style relation computation is read as a position-relation matrix and batch tensor. So the parallel-processing explanation should close as a difference in computation structure, not as hardware boasting.

### Practice. Mark Waiting Computations and Bundled Computations

For each scene below, first mark it as `waiting` or `bundled`.

| Scene | Mark | Explanation |
| --- | --- | --- |
| The 3rd token computation in a sentence must receive the hidden state of the 2nd token. | waiting | The earlier step result is needed by the later step, so sequential dependency appears. |
| Attention scores for every token pair in one sentence are computed in the same layer. | bundled | Many token relation scores are easy to organize as matrix computation. |
| Feed-forward computation for many sentences in a batch applies the same weights to each position. | bundled | The same kind of position-wise computation is easy to process together as tensor computation. |
| During generation, the next token that has not yet appeared must be known in advance. | waiting | There is still an order constraint during generation execution. It should be distinguished from the parallelization feel during training. |
| A rule at the front of a document is compressed into one state and carried to the end. | closer to waiting | Since the earlier clue must pass through many steps, the burden of sequential transfer grows. |

Explanation: This practice is not about implementing an actual GPU kernel. The learning needed in P5-14.5 is to distinguish `computation that passes state`, `a flow that recalculates relations`, and `computation that can be bundled together`. This distinction is what lets us explain the Transformer’s parallel-processing advantage as a change in computation structure, not merely as an impression of speed.

## Checklist

- Can you explain an RNN as a sequential state-passing structure?
- Can you explain a Transformer as a token-relation computation structure?
- Can you explain why the Transformer fits parallel processing from the viewpoint of large matrix operations?
- Can you compare RNN sequential dependency and Transformer relation computation from the viewpoint of parallel processing?

## Sources and References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
