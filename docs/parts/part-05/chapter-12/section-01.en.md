# P5-12.1 Why Recurrent Neural Networks (RNNs), Long Short-Term Memory (LSTM), And Gated Recurrent Units (GRU) Are Needed

Section ID: `P5-12.1`
Version: `v2026.07.18`

In Chapter P5-11, we saw that CNNs handle local patterns well in data with spatial structure such as images. If we change the data type here, the next question appears.

How do we handle data where order matters, such as sentences, speech, and time series?

The structures that try to answer this question are recurrent neural networks (RNNs), long short-term memory (LSTM), and gated recurrent units (GRU).

The recurrent-network family tries to process sequence data by not looking only at the current input, but also by carrying forward some of the information seen earlier.

When the basic names for sequential-state structures become mixed up again, reread together the glossary entries on [RNN (recurrent neural network)](/AiBook/reference/concept-glossary/#rnn-recurrent-neural-network), [LSTM (long short-term memory)](/AiBook/reference/concept-glossary/#lstm-long-short-term-memory), and [GRU (gated recurrent unit)](/AiBook/reference/concept-glossary/#gru-gated-recurrent-unit).

## Scope Of This Section

- Why is the idea of order important in sequence data?
- What kind of frustration appears if we use only a general feed-forward structure?
- What idea did recurrent neural networks introduce?
- Why did LSTM and GRU become necessary on top of that?

The core point that this section needs to close first is that `in sequence data, the current judgment is changed not by only the last input, but by the accumulated state from earlier steps`. In other words, here we first close `why we need to carry sequential state forward` and `why basic RNNs alone found it hard to remember for a long time`. The long-term dependency problem is treated more directly in the very next section, P5-12.2.

## Goals Of This Section

- You can explain why `order` and `context` matter in sequence-data problems.
- You can explain an RNN as `a structure that carries the previous state forward`.
- You can connect the appearance of LSTM and GRU to the problem of maintaining long-term memory.
- Through an executable Python example, you can confirm how an accumulated sequential state actually changes a judgment.

## Why Is Sequence Data Special

In sequence data, if the order of items changes, the meaning can also change.

For example, in a sentence, even if the words are the same, the meaning changes when the order changes. In speech, even the same sound fragment can be heard as a different pronunciation depending on the rhythm before and after it. In sensor data, the last number alone is often less important than how the values rose and fell before it.

That is, unlike a simple set or one row of a table, sequence data contains `before-and-after relationships`. In sequence data, it matters not only what appears, but also in what order it appears.

## Why Is A General Feed-Forward Structure Frustrating By Itself

A general feed-forward network is natural when it receives an input once and sends it directly to an output. But in sequence data, its limit appears quickly.

For example, when we read a phrase like `confirmed` at the end of a sentence, the meaning of the same word can change depending on whether cues such as `blocked`, `leak`, or `forbidden` already appeared earlier. In sensor data too, the last value being 80 does not automatically imply the same judgment every time. It matters whether that 80 came at the end of a gradual rise, or whether it briefly jumped and then rose again.

That is, in sequence data, we often need to connect `the input we see now` with `the inputs we saw earlier`. The problem is that a general feed-forward structure is not naturally designed to carry that accumulated flow inside the structure itself.

This is where the basic idea of the RNN appears.

If we compare the difference very briefly, it becomes the following.

| Structure | Intuition for how it reads input |
| --- | --- |
| feed-forward | sends the received input directly to the output at once |
| RNN | looks at the current input while also carrying the previous state |

If we split the same scene across the two structures, the difference becomes more direct.

| The same scene | What is easy to keep when reading it first with a feed-forward structure | What is better held when reading it first with an RNN |
| --- | --- | --- |
| a negative expression at the end of a sentence | the immediate signal of the current word itself | the accumulated sentence flow from the earlier words |
| interpreting a short speech fragment | the shape of the sound fragment heard right now | the time context connected to the immediately preceding sound |
| judging the last sensor value | the size of the current number alone | the rise-and-fall flow of the previous several steps |

## What Did RNNs Introduce

The core idea of the RNN can be summarized very simply. It says, `when processing the current input, let us also use the state prepared at the previous step`.

That is, at each time step, an RNN receives:

- the current input \(x_t\)
- the previous state \(h_{t-1}\)

and creates a new state \(h_t\).

The key point is that an RNN is a structure that tries to carry earlier information as a state and pass it together into the next-step computation. So when reading an RNN in this section, it is better to hold first the difference `it sees the current input together with the previous state` rather than only `it sees the current input`.

If we draw this very simply, it becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-12/rnn-state-flow-en.mmd"
```

The result to confirm in this diagram is that the current output is not determined only by the input of the present moment. The state from the previous time step keeps being passed to the next time step and influences the result together with it.

## Why RNNs Alone Were Not Enough

Basic RNNs provided an important idea, but real sequence data is not so short and simple. If the state is passed from step to step continuously, cues seen earlier can weaken as they move farther back, and as the current input comes in strongly, older information can be pushed out more easily.

That is, the idea `we want to remember` and the reality `the information is actually maintained for a long time` are different things. This gap leads directly to the long-term dependency problem in the next section.

## Why LSTM And GRU Appeared

LSTM and GRU are structures that try to handle the memory problem of the basic RNN more effectively.

The key point is that LSTM and GRU try to control more finely what should be kept longer, what should be discarded, and how strongly the current input should be reflected. That is, they are not simply `more complex RNNs`, but can be read as `RNNs that try to manage memory better`.

At the introductory stage, it is enough to read this difference in the following way.

- a basic RNN shows the idea of `carrying the state forward`
- LSTM and GRU reinforce `how to keep that state longer and more stably`

## Why Do We Learn Both LSTM And GRU

At the introductory stage, the number of names can be confusing. But it is enough to distinguish them as follows.

- RNN: the most basic idea of carrying sequential state forward
- LSTM: the representative structure that deals more strongly with the memory-maintenance problem
- GRU: a structure that serves a similar purpose in a somewhat simpler form

That is, it is better to see the three not as unrelated competitors, but as `one developmental flow in the same family that deals with sequential-memory problems`.

At the introductory stage, it is enough to hold first only the difference among `state transfer`, `memory control`, and `structure simplification` as in the table below.

| Name | Intuition to hold first |
| --- | --- |
| RNN | passes the state to the next step |
| LSTM | controls more finely what information to keep for a long time and what to discard |
| GRU | implements a similar purpose in a more concise structure |

Rather than memorizing the model names separately, the flow becomes more stable if we also attach what question should be recalled first in a small sequential scene.

| Small sequential scene | Structure to recall first | Why that structure becomes the starting point |
| --- | --- | --- |
| when only the flow of a few words before and after needs to continue, as in interpreting a short operation memo | RNN | because it lets us directly see the most basic sequential-state idea of `current input + previous state` |
| when we need to hold a somewhat more distant cue for longer, such as a negative expression at the end of a sentence or the subject at the beginning | LSTM | because it deals more directly with the long-memory problem by controlling more finely what to keep and what to discard |
| when we want a purpose similar to LSTM but with a somewhat more concise structure | GRU | because it keeps the feel of reinforced sequential memory while making the state-control structure relatively simple to read |

The purpose of this table is not to decide `which model is always superior`. In this section, it is enough to hold the problem-scene handle that `when we first introduce sequential state, RNN comes first`, and `when memory maintenance becomes more important, LSTM/GRU come in`.

## Cases And Examples

### Representative Case. Interpreting An Operation Memo

We can think of an operation memo such as `a leak was confirmed, but restart was not approved`. When people read a memo, if they encounter words such as `approved` or `restart` in the middle, they can easily lean first toward an interpretation that the work will proceed. But only when the final negative phrase `was not` remains together with the earlier cue `leak` can we avoid missing that this sentence actually means `restart should be held`. If we look only at the last few words or separate the words from one another, it becomes easy to misread the sentence. That is, even when reading the meaning at the current position, the earlier words and the intermediate context matter together. A structure that carries sequential state forward is needed precisely in this kind of situation, where `the risk cue seen earlier and the later denial of approval both need to remain together`.
So the result to confirm in this case is whether the model avoids following only the last `approval`-type word, and instead keeps both the earlier leak cue and the later negative expression so that the final judgment actually closes as `restart hold`.

The same viewpoint extends directly to equipment alarm-sound recognition and time-series prediction. But the core point to hold in this section is not the domain name, but `whether the same final input leads to a different conclusion when the accumulated earlier state is different`.

If we place the three cases together, it becomes clearer why RNN/LSTM/GRU should be read not as `the names of time-axis models`, but as `structures where the same final input can lead to a different conclusion because the accumulated state is different`.

| Case | What is easy to miss if we look only at the current input | Context added by sequential state | Result to confirm in this section |
| --- | --- | --- | --- |
| operation-memo interpretation | the immediate meaning of earlier cues such as `leak` or `blocked` | a flow in which even the same final confirmation phrase is interpreted differently depending on the earlier cues | whether the final judgment reflects the earlier action flow rather than one last word |
| equipment alarm-sound recognition | the ambiguity of one short waveform fragment | the time context in which repeated rhythm and alarm pattern continue across the surrounding fragments | whether the same sound fragment is interpreted more stably depending on what comes before and after |
| time-series prediction | the size of one last number | the rise-and-fall trend across the previous several steps | whether the same final value leads to a different alert depending on the earlier flow |

| Standard that is easy for a person to see first | Standard to reread from the sequential-state viewpoint |
| --- | --- |
| if the last word or the last value is the same, a similar judgment should come out | even with the same final input, different accumulated earlier flows produce different states and different conclusions |
| intermediate cues feel like reference notes rather than something essential | if intermediate cues are not accumulated into the state, the interpretation of the final input itself can easily shake |
| a sequential model is easy to memorize only as `a model name for time-axis data` | the real core is that a judgment structure of `current input + previous state` is added |

## Practice And Example

The goal of this example is to confirm what practical difference is made by the phrase `the previous state is passed to the next step`. This time, we place side by side a very simple baseline with no sequential state and another baseline that carries sequential state forward. That is, we confirm through actual output where `a judgment that looks only at the last input` and `a judgment that keeps the earlier flow` begin to split.

Before reading the example, it helps to fix first the minimum points that need to be confirmed in this section.

| Point to confirm | Value to look at directly in the example | Why it matters |
| --- | --- | --- |
| where the baseline judgment and the state-based judgment split | `baseline_last_word_label`, `baseline_last_value_alert`, and the final `label`, `alert` | shows that a sequential model looks at an accumulated state rather than only one last input |
| how the state accumulates step by step | the `state=` output on each line | shows that the core of an RNN-family structure is not an immediate judgment on the current input, but a state update |
| why even the same final input leads to a different conclusion | comparing the last step of `gradual_rise` and `temporary_spike` | lets us confirm with our eyes that if the preceding flow differs, the current judgment also differs |

Input:

- three short operation memos with the same final confirmation phrase
- two time series with the same final temperature of `80`

Output:

- a baseline judgment that looks only at the last input
- sentence-state values updated at each step
- the final sentence label
- a baseline alert decision that looks only at the last value
- sensor-state values updated at each step
- the alert decision at the last step

Problem situation:

- in sequence data, we need to compare directly the difference between a method that looks only at the final value and a method that keeps updating the intermediate state

Concepts to confirm:

- RNN-family structures do not look at the input all at once, but update the state step by step
- compared with a baseline that looks only at the final value, the meaning of sequential-state updates becomes clearer

Before looking at the code, it helps to predict first where the baseline and the state-based judgment will split.

| Scene | Baseline prediction that looks only at the final input | Prediction from the side that accumulates the state | Why this should be held first |
| --- | --- | --- | --- |
| `shutdown_confirmed` | sees only `confirmed` and predicts `restart_allowed` | the earlier `blocked` action remains, so it predicts `hold_required` | lets us see why the earlier action flow must remain inside the state even when the final word is the same |
| `leak_confirmed` | sees only `confirmed` and predicts `restart_allowed` | the earlier `leak` cue remains, so it predicts `hold_required` | lets us see that even with the same final word, the conclusion can split if the earlier state is different |
| `gradual_rise` vs `temporary_spike` | sees only the last value `80` and predicts an alert for both | predicts an alert only for the sustained rise, and not for the temporary spike | lets us see that even the same final value leaves a different state depending on the preceding trend |

Input:

We use the word signals, sensor signals, and initial state values summarized above.

![gradual rise sequence state](/AiBook/assets/part-05/chapter-12/rnn-gradual-rise-state-en.svg)

![temporary spike sequence state](/AiBook/assets/part-05/chapter-12/rnn-temporary-spike-state-en.svg)

These graphs make us separate first `the final value is the same` from `the accumulated state is the same` before running the code. `gradual_rise` and `temporary_spike` both end at 80, but because sequential state also keeps the immediately preceding flow, the final alert interpretation can differ.

```python
word_signal = {
    "leak": -2.2,
    "blocked": -1.5,
    "restart": 1.2,
    "confirmed": 0.8,
}

def classify_with_last_word(words):
    last_signal = word_signal.get(words[-1], 0.0)
    return "restart_allowed" if last_signal > 0 else "hold_required"

def run_sentence(name, words, alpha=0.7):
    state = 0.0
    print(f"[sentence: {name}]")
    print("baseline_last_word_label =", classify_with_last_word(words))
    for step, word in enumerate(words, start=1):
        signal = word_signal.get(word, 0.0)
        state = alpha * state + signal
        print(f"step {step}: word={word:>9}, signal={signal:>4}, state={state:>5.2f}")
    label = "restart_allowed" if state > 0 else "hold_required"
    print("final_label =", label)
    print()

def alert_with_last_value(sequence, threshold):
    return sequence[-1] >= threshold

def run_sequence(name, sequence, alpha=0.6, threshold=63):
    state = 0.0
    print(f"[sensor: {name}]")
    print("baseline_last_value_alert =", alert_with_last_value(sequence, threshold))
    for step, x in enumerate(sequence, start=1):
        state = alpha * state + (1 - alpha) * x
        alert = state >= threshold
        print(f"step {step}: input={x:>3}, state={state:>6.2f}, alert={alert}")
    print()

gradual_rise = [60, 65, 72, 80]
temporary_spike = [80, 60, 60, 80]

run_sentence("shutdown_confirmed", ["blocked", "confirmed"])
run_sentence("leak_confirmed", ["leak", "confirmed"])
run_sentence("restart_confirmed", ["restart", "confirmed"])
run_sequence("gradual_rise", gradual_rise)
run_sequence("temporary_spike", temporary_spike)
```

In the output, start by looking at when `baseline_last_word_label` and `final_label` split, and then at how the intermediate `state` accumulates.

```text
[sentence: shutdown_confirmed]
baseline_last_word_label = restart_allowed
step 1: word=  blocked, signal=-1.5, state=-1.50
step 2: word=confirmed, signal= 0.8, state=-0.25
final_label = hold_required

[sentence: leak_confirmed]
baseline_last_word_label = restart_allowed
step 1: word=     leak, signal=-2.2, state=-2.20
step 2: word=confirmed, signal= 0.8, state=-0.74
final_label = hold_required

[sentence: restart_confirmed]
baseline_last_word_label = restart_allowed
step 1: word=  restart, signal= 1.2, state= 1.20
step 2: word=confirmed, signal= 0.8, state= 1.64
final_label = restart_allowed

[sensor: gradual_rise]
baseline_last_value_alert = True
step 1: input= 60, state= 24.00, alert=False
step 2: input= 65, state= 40.40, alert=False
step 3: input= 72, state= 53.04, alert=False
step 4: input= 80, state= 63.82, alert=True

[sensor: temporary_spike]
baseline_last_value_alert = True
step 1: input= 80, state= 32.00, alert=False
step 2: input= 60, state= 43.20, alert=False
step 3: input= 60, state= 49.92, alert=False
step 4: input= 80, state= 61.95, alert=False
```

Even when reading the output numbers, we need to separate `the final input` from `the accumulated state`.

| Comparison | What first appears in the output | Interpretation that is easy to keep if we only look at the final input | Interpretation that changes when we include sequential state |
| --- | --- | --- | --- |
| `shutdown_confirmed` / `leak_confirmed` / `restart_confirmed` | all of them have the same final word `confirmed`, but the final labels split | it can look as if the same final word should lead to the same judgment | if hold cues accumulated earlier, such as `blocked` and `leak`, still remain, then even after the final `confirmed`, the final judgment can become `hold_required` |
| `gradual_rise` vs `temporary_spike` | both have the same final value `80`, but the final alert splits | it can look as if both should raise an alert because the final value is the same | a sustained rise pushes the state above the alert line, but a flow that briefly spiked and then returned can still fail to alert even with the same final value because the state accumulated less |
| each step's `state=` output | the state changes gradually rather than being determined by each single input alone | it is easy to think the intermediate output is only supplementary explanation | it reveals that the core of an RNN-family structure lies in `how the accumulated state is updated`, rather than in the current input alone |

| Output to look at first | What this output means | What changes if you vary it |
| --- | --- | --- |
| `baseline_last_word_label = restart_allowed` but `final_label = hold_required` in `shutdown_confirmed` and `leak_confirmed` | even if the same judgment appears when looking only at the final word, the sequential state can still keep earlier block and risk cues and produce a different conclusion | if we change the signal size of `blocked` and `leak`, or change `alpha`, the length of time the earlier hold flow remains will change |
| `baseline_last_value_alert = True` but the final `alert=False` in `temporary_spike` | even if looking only at the final value suggests the same alert, the sequential state can keep the immediately preceding flow and produce a different conclusion | if we change the threshold or `alpha`, the ease with which `sustained rise` and `temporary spike` split will change |
| the final inputs of `gradual_rise` and `temporary_spike` are both `80`, but the states differ | the current judgment is determined not by the present step alone, but by the accumulated traces of previous steps as well | if we change the intermediate values, the degree to which the state differs even under the same final input becomes clearer |
| in the operation-memo example, the final word is the same `confirmed`, but the states of `shutdown_confirmed` and `leak_confirmed` differ | even the same confirmation phrase leads to a different state and final judgment when the earlier action cues differ | if we change the signal values of `blocked` and `leak`, we can see how strongly the earlier action flow remains |

The results above show three things together. First, in the operation-memo example, the baseline reads `shutdown_confirmed`, `leak_confirmed`, and `restart_confirmed` all as `restart_allowed` because it looks only at the final word `confirmed`, but the sequential-state side keeps how strong the earlier block and risk cues were and separates `shutdown_confirmed` and `leak_confirmed` into `hold_required`. Second, in the sensor example, the baseline judges both time series as alerts because it sees only the last value `80`, but the state-based side can leave `sustained rise` and `temporary spike` differently. Third, even when the final input is 80 in both cases or the last word is always `confirmed`, the state values are not the same because the judgment at the current step is determined not by `the input of this one step` alone, but by also referring to the accumulated state from previous steps.

If we reread the operation-memo side by the same standard, the core point becomes clearer. The baseline is easily pulled by the immediate signal of the final word, but the sequential-state side accumulates the traces left in order by `blocked`, `leak`, `restart`, and `confirmed` to form the final conclusion. Real LSTM and GRU can be understood as moving in the direction of managing precisely this state more stably for longer.

This example does not implement a full real RNN. But the core that needs to be read is clearer.

- even the same current input creates a different state depending on the earlier flow
- without state, the judgment easily collapses into a very rough standard such as the final word or the final number
- in sentences, if a later word is to change the meaning of an earlier word, the intermediate state must remain alive
- if the state differs, the final judgment can also differ
- the core of a sequential structure is that it looks not only at `the current value`, but also at `the trace accumulated so far`

Rather than reading the result once and stopping, it is better to continue directly by checking what values can be changed to make the feel of `state accumulation` clearer.

| Output signal seen first | Change to try right now | Conclusion not to rush to from this example alone |
| --- | --- | --- |
| `temporary_spike` is not an alert even though its final value is 80 | raise or lower `alpha` and compare how long past state is carried forward | do not conclude that an RNN-family model is always unconditionally better than a last-value baseline |
| even with the same final `confirmed`, the state and conclusion split | change the signals for `leak`, `blocked`, and `restart` and see how long the earlier action flow remains | do not conclude that a handful of word signals fully explains real operational language understanding |
| the two time series end with different final states | raise or lower the intermediate values and see where `sustained trend` and `temporary spike` begin to split | do not substitute this one simple state-update equation for the entire internal gating of LSTM and GRU |

That is, the basic intuition of the RNN is closer to `it carries the previous state in and makes a new state together with the current input` than to `it immediately classifies the current input`. LSTM and GRU can be read as structures that appeared to better control `what to keep longer` and `what to forget` in precisely that state.

The criterion to gain from this section is clear. Even with the same final word or the same final number, the current judgment can change depending on what flow accumulated earlier. The RNN is the model that first made this idea of accumulated state visible in structure, and LSTM and GRU are structures that try to reinforce that state so it does not weaken too quickly. In the next section, P5-12.2, we look more concretely at where this way of `passing the state forward` begins to shake, that is, why it becomes hard to hold onto a cue from far back all the way to the end.

## Checklist

- Can you explain why state transfer matters in sequence data?
- Can you say why RNN, LSTM, and GRU are grouped into the same family?
- Can you explain that when reading sequence data, even the same item can be interpreted differently depending on the before-and-after order and the accumulated context?
- Can you explain that an RNN is a structure that processes the current input by carrying forward the previous state?
- Can you say that LSTM and GRU are developmental structures that try to deal better with the problem of not being able to remember for a long time?
- Can you explain through a case that even with the same final word or the same final number, a different earlier flow can lead to a different conclusion?
- When the order before and after the input and the accumulated context seem more important than the input type itself, can you recall the sequential-state viewpoint first?
- Can you explain LSTM and GRU not as `different model names`, but as `reinforcing structures that try to manage the state more stably for longer`?

## Sources And References

- David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams, `Learning representations by back-propagating errors`, Nature, 1986, checked on 2026-06-29.
- Sepp Hochreiter, Jürgen Schmidhuber, `Long Short-Term Memory`, Neural Computation, 1997, checked on 2026-06-29.
- Kyunghyun Cho et al., `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`, arXiv, 2014, checked on 2026-06-29.
