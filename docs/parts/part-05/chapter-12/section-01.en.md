# P5-12.1 Why RNN, LSTM, and GRU Are Needed

> Section ID: `P5-12.1`
> Version: `v2026.07.26`

_Subtitle: What sequence-data problem do RNNs, LSTMs, and GRUs address?_

In Chapter P5-11, we saw that CNNs handle local patterns well in data with spatial structure such as images. If we change the data type here, the next question appears.

How do we handle data where order matters, such as sentences, speech, and time series?

The structures that try to answer this question are recurrent neural networks (RNNs), long short-term memory (LSTM), and gated recurrent units (GRU).

The recurrent-network family tries to process sequence data by not looking only at the current input, but also by carrying forward some of the information seen earlier.

When the basic names for sequential-state structures become mixed up again, reread together the glossary entries on [RNN (recurrent neural network)](/AiBook/en/reference/concept-glossary-alpha/r/#rnn-recurrent-neural-network), [LSTM (long short-term memory)](/AiBook/en/reference/concept-glossary-alpha/l/#lstm-long-short-term-memory), and [GRU (gated recurrent unit)](/AiBook/en/reference/concept-glossary-alpha/g/#gru-gated-recurrent-unit).

## The Question of How RNNs Remember Order

- Why is the idea of order important in sequence data?
- What kind of frustration appears if we use only a general feed-forward structure?
- What idea did recurrent neural networks introduce?
- Why did LSTM and GRU become necessary on top of that?

The core point that this section needs to close first is that `in sequence data, the current judgment is changed not by only the last input, but by the accumulated state from earlier steps`. In other words, here we first close `why we need to carry sequential state forward` and `why basic RNNs alone found it hard to remember for a long time`. The long-term dependency problem is treated more directly in the very next section, P5-12.2.

## Standards for State Passing and Time-Axis Representations

- You can explain why `order` and `context` matter in sequence-data problems.
- You can explain an RNN as `a structure that carries the previous state forward`.
- You can connect the appearance of LSTM and GRU to the problem of maintaining long-term memory.
- Through an executable Python example, you can confirm how an accumulated sequential state actually changes a judgment.

## Why Is Sequence Data Special

In sequence data, if the order of items changes, the meaning can also change.

For example, in a sentence, even if the words are the same, the meaning changes when the order changes. In speech, even the same sound fragment can be heard as a different pronunciation depending on the rhythm before and after it. In sensor data, the last number alone is often less important than how the values rose and fell before it.

That is, unlike a simple set or one row of a table, sequence data contains `before-and-after relationships`. In sequence data, it matters not only what appears, but also in what order it appears.

## Why Is a General Feed-Forward Structure Frustrating by Itself

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

State transfer can sound abstract, but in practice it can be read as follows. Using the same `MEMO_ALPHA=0.85` setting as the later Python example, if the previous state is `-1.5` and the current input `confirmed` has a signal of `0.8`, the new state is not the current-input-only value `0.8`. It reflects both `the hold signal left from earlier` and `the current confirmation signal`.

| step | Current input | Value from the last input alone | New state with previous state reflected | Difference to read |
| --- | --- | ---: | ---: | --- |
| 1 | `blocked` | -1.5 | -1.50 | a hold-side cue remains in the state first |
| 2 | `confirmed` | 0.8 | -0.48 | even if the last word is positive, the final state is still negative because the earlier hold trace remains |

The important point in this small calculation is not that an RNN ignores the current input `confirmed`. It sees the current input, but it sees it together with the state passed from the previous step. Because of that, even with the same `confirmed`, the final state and judgment can differ depending on whether `blocked` or `restart` appeared earlier.

If we draw this very simply, it becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-12/rnn-state-flow-en.mmd"
```

The result to confirm in this diagram is that the current output is not determined only by the input of the present moment. The state from the previous time step keeps being passed to the next time step and influences the result together with it.

## Why RNNs Alone Were Not Enough

Basic RNNs provided an important idea, but real sequence data is not so short and simple. If the state is passed from step to step continuously, cues seen earlier can weaken as they move farther back, and as the current input comes in strongly, older information can be pushed out more easily.

For example, even if a strong hold cue such as `leak` appears at the beginning, if unrelated words continue for a long time and `confirmed` appears at the end, the state of a basic RNN can be pulled more and more toward the current input. A structure that passes the state forward is necessary, but if it cannot control what should remain for a long time and what should weaken quickly, it is hard to hold an old key cue until the end.

| Situation | Pressure that appears with state transfer alone | Why it becomes a problem |
| --- | --- | --- |
| an important cue appears near the front, followed by many neutral inputs | the state is diluted little by little at each step | the first cue may not remain enough for the final judgment |
| the current input comes in strongly | the latest input overwrites the previous state | the balance between the old cue and the current cue can shake |
| needed memory and disposable traces are mixed together | everything is passed to the next step in the same way | important information and noise are not distinguished |

That is, the idea `we want to remember` and the reality `the information is actually maintained for a long time` are different things. This gap leads directly to the long-term dependency problem in the next section.

## Why LSTM and GRU Appeared

LSTM and GRU are structures that try to handle the memory problem of the basic RNN more effectively.

The key point is that LSTM and GRU try to control more finely what should be kept longer, what should be discarded, and how strongly the current input should be reflected. That is, they are not simply `more complex RNNs`, but can be read as `RNNs that try to manage memory better`.

At the introductory stage, it is enough to read this difference in the following way.

- a basic RNN shows the idea of `carrying the state forward`
- LSTM and GRU reinforce `how to keep that state longer and more stably`

So the need for LSTM and GRU is not simply that `there is one more model name than RNN`. It is that, if we want to use sequential state in real problems, we needed additional devices for managing memory. At the introductory stage, it is more useful to hold the questions below first than to memorize the internal gate equations.

| Question | Limitation that appears first in a basic RNN | Direction LSTM/GRU tries to reinforce |
| --- | --- | --- |
| What should remain for a long time? | all states are mixed into the next step in the same way | tries to preserve important cues for longer |
| What should be forgotten? | old traces and noise remain or weaken together | tries to reduce less important information |
| How much should the current input be reflected? | new input can easily shake the previous state | tries to control how much of the new input and existing state to reflect |

## Why Do We Learn Both LSTM and GRU

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

## Cases and Examples

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

## Practice and Example

The goal of this example is to confirm what practical difference is made by the phrase `the previous state is passed to the next step`. This time, we place side by side a very simple baseline with no sequential state and another baseline that carries sequential state forward. That is, we confirm through actual output where `a judgment that looks only at the last input` and `a judgment that keeps the earlier flow` begin to split. We also look at the data-processing point that, when rows from several sequences are mixed in one CSV file, the step order must be restored by `sequence_id` before sequential state can be calculated.

Before reading the example, it helps to fix first the minimum points that need to be confirmed in this section.

| Point to confirm | Value to look at directly in the example | Why it matters |
| --- | --- | --- |
| where the baseline judgment and the state-based judgment split | `baseline_label`/`state_label`, `baseline_alert`/`state_alert` | shows that a sequential model looks at accumulated state rather than only one last input |
| how the state accumulates step by step | `previous_state -> new_state` in the `trace` output | shows that the core of an RNN-family structure is not immediate judgment on the current input, but state update |
| why even the same final input leads to a different conclusion | rows where `changed=True` | lets us confirm visually that if the preceding flow differs, the current judgment also differs |

Input:

- operation-memo sequences with the same final confirmation phrase
- sensor sequences with the same final temperature `80`
- input file: [`rnn-sequence-events.csv`](/AiBook/assets/part-05/chapter-12/rnn-sequence-events.csv)

Output:

- baseline judgment that looks only at the last input
- final sentence label in the memo summary and whether it is `changed`
- baseline alert decision that looks only at the last value
- final accumulated state, alert decision, and `changed` flag in the sensor summary
- `previous_state -> new_state` state-update flow in a representative trace

Problem situation:

- in sequence data, we need to compare directly the difference between a method that looks only at the final value and a method that keeps updating the intermediate state

Concepts to confirm:

- RNN-family structures do not look at the input all at once, but update the state step by step
- compared with a baseline that looks only at the final value, the meaning of sequential-state updates becomes clearer

Before looking at the code, it helps to predict first where the baseline and the state-based judgment will split.

| Scene | Baseline prediction that looks only at the final input | Prediction from the side that accumulates the state | Why this should be held first |
| --- | --- | --- | --- |
| `memo_shutdown_confirmed` | sees only `confirm` and predicts `restart_allowed` | the earlier `block` action remains, so it predicts `hold_required` | lets us see why the earlier action flow must remain inside the state even when the final word is the same |
| `memo_leak_confirmed` | sees only `confirm` and predicts `restart_allowed` | the earlier `leak` cue remains, so it predicts `hold_required` | lets us see that even with the same final word, the conclusion can split if the earlier state is different |
| `gradual_rise` vs `temporary_spike` | sees only the last value `80` and predicts an alert for both | predicts an alert only for the sustained rise, and not for the temporary spike | lets us see that even the same final value leaves a different state depending on the preceding trend |

Input:

One CSV row means one step in one sequence. `sequence_id` marks the same sequential group, and `kind` distinguishes operation memos (`memo`) from sensors (`sensor`). Operation memos use `token`, and sensor sequences use `sensor_value`. The Python example reads this file, restores step order by `sequence_id`, and compares last-input judgment with accumulated-state judgment.

The code below assumes it is run from the repository root.

![CSV-based accumulated state comparison for sensor sequences](/AiBook/assets/part-05/chapter-12/rnn-sequence-csv-state-trace-en.svg)

This graph makes us separate first `the final value is the same` from `the accumulated state is the same` before running the code. The sensor sequences in the CSV all end at 80, but because sequential state also keeps the preceding flow, only some sequences cross the alert threshold.

```python
from collections import defaultdict
from pathlib import Path
import csv

DATA_PATH = Path("docs/assets/part-05/chapter-12/rnn-sequence-events.csv")

MEMO_ALPHA = 0.85     # Lower this value to make earlier cues weaken faster.
SENSOR_ALPHA = 0.6    # Raise this value to carry past sensor state for longer.
SENSOR_THRESHOLD = 68

WORD_SIGNAL = {
    "leak": -2.2,
    "block": -1.5,
    "restart": 1.2,
    "approve": 0.6,
    "confirm": 0.8,
}

def load_sequences(path):
    sequences = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sequences[row["sequence_id"]].append(row)
    for rows in sequences.values():
        rows.sort(key=lambda row: int(row["step"]))
    return sequences

def label_from_state(state):
    return "restart_allowed" if state > 0 else "hold_required"

def label_from_last_token(rows):
    last_signal = WORD_SIGNAL.get(rows[-1]["token"], 0.0)
    return label_from_state(last_signal)

def trace_memo_state(rows, alpha=MEMO_ALPHA):
    state = 0.0
    trace = []
    for row in rows:
        previous_state = state
        step = int(row["step"])
        word = row["token"]
        input_signal = WORD_SIGNAL.get(word, 0.0)
        state = alpha * state + input_signal
        trace.append((step, word, input_signal, previous_state, state))
    return trace

def alert_from_last_value(rows, threshold=SENSOR_THRESHOLD):
    return float(rows[-1]["sensor_value"]) >= threshold

def trace_sensor_state(rows, alpha=SENSOR_ALPHA, threshold=SENSOR_THRESHOLD):
    state = 0.0
    trace = []
    for row in rows:
        previous_state = state
        step = int(row["step"])
        value = float(row["sensor_value"])
        state = alpha * state + (1 - alpha) * value
        trace.append((step, value, previous_state, state, state >= threshold))
    return trace

sequences = load_sequences(DATA_PATH)

print(f"Control variables: MEMO_ALPHA={MEMO_ALPHA}, SENSOR_ALPHA={SENSOR_ALPHA}, SENSOR_THRESHOLD={SENSOR_THRESHOLD}")
print()

print("[memo summary: does the same final word 'confirm' get read differently?]")
print("case                  last_word  baseline_label   final_state  state_label      changed")
for case_name, rows in sequences.items():
    if rows[0]["kind"] != "memo":
        continue
    trace = trace_memo_state(rows)
    final_state = trace[-1][-1]
    baseline_label = label_from_last_token(rows)
    state_label = label_from_state(final_state)
    changed = baseline_label != state_label
    print(f"{case_name:27} {rows[-1]['token']:>5}  {baseline_label:15} {final_state:>10.2f}  {state_label:15} {changed}")

print()
print("[sensor summary: does the same final value 80 get read differently?]")
print("case              last_value  baseline_alert  final_state  state_alert  changed")
for case_name, rows in sequences.items():
    if rows[0]["kind"] != "sensor":
        continue
    trace = trace_sensor_state(rows)
    final_state = trace[-1][3]
    baseline_alert = alert_from_last_value(rows)
    state_alert = trace[-1][4]
    changed = baseline_alert != state_alert
    print(f"{case_name:29} {rows[-1]['sensor_value']:>5}  {str(baseline_alert):>14}  {final_state:>11.2f}  {str(state_alert):>11}  {changed}")

print()
print("[trace: memo_shutdown_confirmed]")
for step, word, signal, previous_state, new_state in trace_memo_state(sequences["memo_shutdown_confirmed"]):
    print(
        f"step {step}: input={word}, input_signal={signal:>4}, "
        f"previous_state={previous_state:>5.2f} -> new_state={new_state:>5.2f}"
    )

print()
print("[trace: sensor_temporary_spike]")
for step, value, previous_state, new_state, alert in trace_sensor_state(sequences["sensor_temporary_spike"]):
    print(
        f"step {step}: input={value:>3}, "
        f"previous_state={previous_state:>5.2f} -> new_state={new_state:>5.2f}, "
        f"state_alert={alert}"
    )
```

In the output, first find the rows where `changed=True`. Those are the points where the last-input baseline and the accumulated sequential-state judgment split. Then use the `trace` to confirm which previous state was passed into the next step.

```text
Control variables: MEMO_ALPHA=0.85, SENSOR_ALPHA=0.6, SENSOR_THRESHOLD=68

[memo summary: does the same final word 'confirm' get read differently?]
case                  last_word  baseline_label   final_state  state_label      changed
memo_shutdown_confirmed       confirm  restart_allowed      -0.12  hold_required   True
memo_leak_confirmed           confirm  restart_allowed      -0.55  hold_required   True
memo_restart_confirmed        confirm  restart_allowed       2.18  restart_allowed False
memo_blocked_then_approved    confirm  restart_allowed       1.26  restart_allowed False
memo_leak_then_recovered      confirm  restart_allowed       0.47  restart_allowed False

[sensor summary: does the same final value 80 get read differently?]
case              last_value  baseline_alert  final_state  state_alert  changed
sensor_gradual_rise             80            True        71.72         True  False
sensor_temporary_spike          80            True        66.60        False  True
sensor_late_rise                80            True        69.16         True  False
sensor_stable_high              80            True        74.83         True  False
sensor_recovered_then_rise      80            True        66.91        False  True

[trace: memo_shutdown_confirmed]
step 1: input=block, input_signal=-1.5, previous_state= 0.00 -> new_state=-1.50
step 2: input=inspect, input_signal= 0.0, previous_state=-1.50 -> new_state=-1.27
step 3: input=wait, input_signal= 0.0, previous_state=-1.27 -> new_state=-1.08
step 4: input=confirm, input_signal= 0.8, previous_state=-1.08 -> new_state=-0.12

[trace: sensor_temporary_spike]
step 1: input=80.0, previous_state= 0.00 -> new_state=32.00, state_alert=False
step 2: input=60.0, previous_state=32.00 -> new_state=43.20, state_alert=False
step 3: input=59.0, previous_state=43.20 -> new_state=49.52, state_alert=False
step 4: input=61.0, previous_state=49.52 -> new_state=54.11, state_alert=False
step 5: input=63.0, previous_state=54.11 -> new_state=57.67, state_alert=False
step 6: input=80.0, previous_state=57.67 -> new_state=66.60, state_alert=False
```

Even when reading the output numbers, we need to separate `the final input` from `the accumulated state`.

| Comparison | What first appears in the output | Interpretation that is easy to keep if we only look at the final input | Interpretation that changes when we include sequential state |
| --- | --- | --- | --- |
| `memo_*` sequences | all have the final word `confirm`, but `changed` differs | it can look as if the same final word should lead to the same judgment | if hold signals accumulated earlier, such as `block` and `leak`, remain, then even after the final `confirm`, the final judgment can become `hold_required` |
| `sensor_*` sequences | all have the final value `80`, but only some have `changed=True` | it can look as if all should alert because the final value is the same | sustained rise pushes state above the alert line, but a flow that returned after a temporary spike can still fail to alert even with the same final value because less state has accumulated |
| `previous_state -> new_state` in the `trace` | the current input is mixed with previous state instead of becoming the final judgment directly | it is easy to think intermediate output is only supplementary explanation | it reveals that the core of an RNN-family structure lies in `how accumulated state is updated`, rather than in the current input alone |

| Output to look at first | What this output means | What changes if you vary it |
| --- | --- | --- |
| rows with `changed=True` in the memo summary | even when last-word-only reading gives the same judgment, sequential state can keep earlier block and risk cues and produce a different conclusion | if we change CSV `token` values, `WORD_SIGNAL` values, or `MEMO_ALPHA`, how long the earlier hold flow remains changes |
| rows with `changed=True` in the sensor summary | even when the last value alone looks like the same alert, sequential state can keep the immediately preceding flow and produce a different conclusion | if we change intermediate CSV `sensor_value`, `SENSOR_THRESHOLD`, or `SENSOR_ALPHA`, the ease with which `sustained rise` and `temporary spike` split changes |
| `previous_state` is used in the next `new_state` calculation in the `trace` | the current judgment sees not one current step alone, but the accumulated traces from previous steps as well | if we change intermediate inputs, the amount by which state differs under the same final input becomes clearer |

The results above show three things together. First, in the operation-memo example, the baseline reads every memo sequence as `restart_allowed` because it looks only at the final word `confirm`, but the sequential-state side keeps how strong the earlier block and risk cues were and separates some sequences into `hold_required`. Second, in the sensor example, the baseline judges every sensor sequence as an alert because it sees only the last value `80`, but the state-based side can leave sustained rise and return-after-spike flows differently. Third, even when the final input is 80 or the last word is always `confirm`, the state values are not the same because the judgment at the current step is determined not by `the input of this one step` alone, but by also referring to the accumulated state from previous steps.

If we reread the operation-memo side by the same standard, the core point becomes clearer. The baseline is easily pulled by the immediate signal of the final word, but the sequential-state side accumulates the traces left in order by tokens such as `block`, `leak`, `restart`, and `confirm` to form the final conclusion. Real LSTM and GRU can be understood as moving in the direction of managing precisely this state more stably for longer.

This example does not implement a full real RNN. But the core that needs to be read is clearer.

- even the same current input creates a different state depending on the earlier flow
- without state, the judgment easily collapses into a very rough standard such as the final word or the final number
- in sentences, if a later word is to change the meaning of an earlier word, the intermediate state must remain alive
- if the state differs, the final judgment can also differ
- the core of a sequential structure is that it looks not only at `the current value`, but also at `the trace accumulated so far`

Rather than reading the result once and stopping, it is better to continue directly by checking what values can be changed to make the feel of `state accumulation` clearer.

| Output signal seen first | Change to try right now | Conclusion not to rush to from this example alone |
| --- | --- | --- |
| some `sensor_*` sequences do not alert even though their final value is 80 | change intermediate CSV `sensor_value`, `SENSOR_ALPHA`, and `SENSOR_THRESHOLD` to compare how long past state is carried forward | do not conclude that an RNN-family model is always unconditionally better than a final-value baseline |
| even with the same final `confirm`, the state and conclusion split | change CSV `token`, `WORD_SIGNAL`, and `MEMO_ALPHA` to see how long the earlier action flow remains | do not conclude that a handful of word signals fully explains real operational language understanding |
| several sensor sequences leave different final states | raise or lower intermediate values and see where `sustained trend` and `temporary spike` begin to split | do not substitute this one simple state-update equation for the entire internal gating of LSTM and GRU |

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

## Sources and References

- David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams, `Learning representations by back-propagating errors`, Nature, 1986, checked on 2026-07-19. [https://doi.org/10.1038/323533a0](https://doi.org/10.1038/323533a0){: target="_blank" rel="noopener noreferrer" }
- Sepp Hochreiter, Jürgen Schmidhuber, `Long Short-Term Memory`, Neural Computation, 1997, checked on 2026-07-19. [https://doi.org/10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735){: target="_blank" rel="noopener noreferrer" }
- Kyunghyun Cho et al., `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`, arXiv, 2014, checked on 2026-07-19. [https://arxiv.org/abs/1406.1078](https://arxiv.org/abs/1406.1078){: target="_blank" rel="noopener noreferrer" }
