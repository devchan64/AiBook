# P5-13.1 The Intuition Of Attention

> Section ID: `P5-13.1`
> Version: `v2026.07.20`

In P5-12.2, we saw that because of long-term dependency, sequential models can have difficulty maintaining information from far back strongly enough. The next question appears here.

Can we make the current position refer more directly to the past information it needs?

The representative answer to this question is attention.

Attention is a method that places greater weight on the positions or tokens that are truly important for the current computation, so the needed information can be referred to more directly.

When you need to fix again the basic motivation of attention in a short form, reread the glossary entry on [attention](/AiBook/reference/concept-glossary-parts/08-ieung/#attention).

## The Question Of How Attention Revisits Needed Positions

- What problem is attention trying to solve?
- What does it mean to `look more strongly at the needed position`?
- How is attention connected to the RNN family?
- Why did attention feel like such a major turning point?

The core point that this section needs to close first is that `instead of only struggling to remember for longer, a method was needed that could look again at the position needed right now`.

The connection to self-attention and the Transformer is continued in the next section and the next chapter. An introductory explanation of query, key, value, and multi-head attention is revisited in supplementary reading P5-13.3.

## Standards For Reference Weights And Context Choice

- You can explain attention as `a method that refers more directly to important positions`.
- You can talk about the connection between the long-term dependency problem and attention.
- You can explain why attention mattered in early encoder-decoder structures and in operational-document transformation scenes.
- Through an executable Python example, you can confirm the intuition of attention as a weighted average.

## Why Did Attention Appear

In basic RNNs or encoder-decoder structures, there was a tendency to try to compress the full long input into one compact state. This can hold up when the input is short, but as the length grows, the specific cue needed right now can easily become blurred inside that compressed state.

Attention looks at this problem differently.

`When producing the current output, let us directly compute which parts of the full input should be referred to more strongly.`

That is, instead of forcing older information to remain only inside a fading state, attention introduces the idea of looking it up again when needed. The key for reading attention in this section lies more in `making the model find again the position needed now` than in `making the model remember for longer`.

## What Does `Looking More Strongly` Mean

The core of attention is to place larger weights on positions that are more relevant to the current task, and then gather information again. What matters is that all positions are not treated equally in advance.

- at the current position
- the model scans past inputs or other positions
- gives larger scores to the more important positions
- and gathers information based on those scores

That is, rather than looking at every position equally, attention is `a method that refers more strongly to positions that are more relevant to the current task`. So even with the same input, if the current question changes, the position that should be looked at strongly can also change.

If we place this flow in a very short table, it becomes the following.

| Step | What is happening now |
| --- | --- |
| 1 | the current position scans the other positions |
| 2 | it gives larger scores to the more relevant positions |
| 3 | it gathers context information by reflecting those scores |

The short sentence below shows `scan -> score -> gather context` in a scene where the current sentence refers more strongly to the reason cue in the later sentence.

```text
The restart was delayed. The reason was pressure instability.
```

If the model is now trying to answer `What was the reason?`, it does not look at every word with equal weight. Instead, it will put more weight on positions such as `pressure`, `instability`, and `reason`. That is, in attention, `looking more strongly` means that `positions more directly connected to the current question are reflected more strongly in the computation`.

## Why Is It Intuitive When Seen As A Direct-Reference Example

Historically, attention gained major force in the context of sequence-to-sequence translation, but from the reader's point of view it is more direct to read it as a work-instruction transformation scene that asks `which part of the input should be looked at again when forming the current phrase`.

For example, when converting an English operating procedure into a Korean work instruction, at the moment the model is forming one current output phrase:

- it can identify which words in the whole input sentence are most relevant right now
- and refer more strongly to those positions

That is, when forming one output word or phrase, it scans the full input each time but puts more weight on the positions it needs.

`Attention is a device that makes the model find the input position that matches the work-instruction phrase being written now, and refer to it more heavily.`

## How Does Attention Answer The Long-Term Dependency Problem

The long-term dependency problem was that old information could weaken or disappear before reaching the current point. Attention answers this problem in the following way.

- instead of leaving old information only as a faint trace inside the state
- at the current step, scan the full set of past positions again
- and directly select the important places to refer to

That is, attention is closer to the idea of `finding the needed information better` than to simply `preserving memory for longer`.

If P5-12.2 was read as a section about `information inside the state becoming faint as it travels farther`, this section flips that problem into `then let us look again at the position needed now`.

If we compress only this transition very briefly, it can be read through the following flow.

```mermaid
--8<-- "assets/part-05/chapter-13/attention-direct-reference-bridge-en.mmd"
```

The key of this diagram is that the handle shifts from `carry information for a long time` to `find it again when needed`.

## If We Draw This Very Simply

```mermaid
--8<-- "assets/part-05/chapter-13/attention-focus-flow-en.mmd"
```

This diagram compresses attention into `find the needed position -> assign weight -> form focused context`.

If we fix once more, very briefly, how the position that needs to be revisited changes when the current question changes even under the same input sentence, it can be seen like this.

```mermaid
--8<-- "assets/part-05/chapter-13/attention-question-shift-en.mmd"
```

The first points to hold from this comparison diagram are the following.

- even when the input sentence is the same, if `what is being asked` changes, the position receiving the higher weight also changes
- so the core of attention is not `deciding one important sentence in advance`, but choosing again the reference position according to the current question
- this intuition is needed in order to move more naturally into the next section on self-attention, where `the position revisited can differ for each token`

## Where Does It Go Wrong If We Mistake Attention For `Summarization`

When first encountering attention, it is easy to feel that it is just `a summarization device that leaves only the important parts`. But it is better to distinguish it a little more precisely here.

- attention gives larger weight to positions that matter more for the current computation
- so the full context can be reread as `a state in which the important parts are emphasized more`
- but attention itself does not reduce the input length or separately compress and store the contents

That is, the core of attention lies not in `making the context shorter`, but in `what should be referred to more strongly inside the context`.

If we reduce this difference to one sentence, it becomes the following.

`Attention is less a device that summarizes context into something short, and more a device that makes the important positions for the current computation be read more strongly.`

## Why Did It Look Like Such A Big Turning Point

Attention was not merely an auxiliary technique that raised performance a little. It had the effect of changing the viewpoint of sequence modeling itself.

Before attention:

- the central method was to put a long sentence into a compressed state

After attention:

- more emphasis was placed on selectively referring to the needed positions while keeping the whole input visible

This change later continued into self-attention and the Transformer, producing a major transition away from the RNN-centered flow. This is the point the reader should hold in the present section. The question itself changed from `shall we carry the information for a long time?` to `shall we look again at the position we need now?`

## Cases And Examples

### Representative Case. Operating-Procedure Transformation Document

Imagine that we are converting an English operating-procedure document into a Korean work instruction. At first, it is easy to feel that it is enough just to read it from left to right and transfer it directly. But in reality, there are many times when we need to check again which position in the full input sentence is most directly connected to the Korean instruction phrase being written now. For example, if we miss the relationship between the subject near the front of the sentence and the safety condition near the back, the result can look grammatically fine while still making it awkward who must do what first. Even when people translate procedure documents, they usually look back with their eyes for the input position that matches the word they are writing now. Attention matches very well this intuition of `looking more strongly at the input position most relevant to the output phrase being produced now`, and can be understood as moving in a direction that reduces the chance of missing an important word located far away in a long sentence.
So the result to confirm in this case is whether the current translated phrase avoids following only the nearby words, and instead actually refers again to both the front subject and the back safety condition so the output closes as a conditional work instruction.

The same viewpoint extends directly to incident-memo summarization and manual question answering. But the core point to hold in this section is not the domain name, but `whether the position that must be referred to strongly also changes when the current question or output goal changes`.

If we place the three cases together, it becomes clearer why attention should be read not as `a device that roughly summarizes important parts`, but as `a structure that changes which position is revisited according to the current question or output goal`.

| Standard that is easy for a person to see first | Standard to reread from the attention viewpoint |
| --- | --- |
| it feels as if the answer to the current question can be produced from the general impression left after reading the whole sentence once | if the current question or output goal changes, the position that must be revisited also changes |
| it feels as if the important sentence is fixed from the beginning | even in the same document, the position receiving the highest weight changes according to `what is being asked` |
| it is easy to understand attention as a simple summarization device | the core is not reducing the length, but redistributing reference weight according to the current task |

## Practice And Example

The goal of this example is to confirm the intuition of attention as assigning larger weights to important positions among multiple candidates and forming a weighted average. This time, instead of placing three numbers directly inside the code, we keep operating-manual candidate lines in a separate CSV file and reread the same candidate group by question.

Problem situation:

- if all input lines are averaged equally, cues directly related to the current question can become blurred
- even in the same manual, the lines that should be referred to more strongly differ depending on whether the question asks about `pressure`, `coolant flow`, or `restart approval`

Input:

- [`attention-operating-manual-candidates.csv`](/AiBook/assets/part-05/chapter-13/attention-operating-manual-candidates.csv){ .csv-preview }
- 40 operating-manual candidate lines
- the representative signal value `evidence_signal` for each line
- question-specific relevance scores: `score_pressure_hold`, `score_flow_limit`, `score_restart_permission`

Output:

- a baseline context value that averages all candidates equally
- attention weights that differ by question
- a context value that differs by question
- candidate lines reflected most strongly for each question

Concepts to confirm:

- instead of looking at all candidates with the same weight, attention looks more strongly at positions more relevant to the current question
- only by comparing the baseline average with the attention weighted average do we see why choosing the important position is necessary
- even with the same candidate set, if the question changes, the weight is redistributed
- when the input has many lines as in a CSV file, it becomes clearer that attention is the problem of `which line to look at more strongly`

A row in the CSV means `one line inside a document`. `evidence_signal` is a representative number contributed by that line to the context value, and the `score_*` columns are relevance scores by question. This is not an implementation of real learned attention scores, but it is enough to confirm the intuition `question-specific scores -> softmax weights -> weighted-average context value`.

If we first look at part of the CSV, it becomes the following.

| line_id | section | text summary | evidence_signal | pressure score | flow score | restart score |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| L05 | pressure | wait 3 minutes after venting | 3.0 | 2.8 | 0.1 | 0.7 |
| L10 | pressure | hold time is counted from the last unstable reading | 2.9 | 3.0 | 0.1 | 1.1 |
| L13 | coolant | coolant flow must stay at least 12 units | 12.0 | 0.2 | 2.9 | 0.5 |
| L18 | coolant | start standby pump if main flow is below limit | 12.6 | 0.1 | 2.8 | 0.9 |
| L25 | restart | pressure, flow, and signature must all pass for restart | 7.2 | 1.3 | 1.7 | 3.0 |
| L40 | handover | routine cleaning note is low priority for all three questions | 4.6 | 0.1 | 0.1 | 0.1 |

Before looking at the code, it helps to predict first which section's lines will receive weight if only the question changes while the same CSV stays in place.

| Question | Misunderstanding that can easily arise in the baseline | Change to predict first in attention |
| --- | --- | --- |
| `What is the pressure-release holding time?` | if we only use the whole-manual average, the pressure-hold cue can be blurred | pressure-section lines and missing-pressure-timestamp lines should rise to the top |
| `What is the coolant-flow criterion?` | it can feel as if the context should be similar to the previous question because the manual is the same | coolant-section lines and flow-meter lines should rise to the top |
| `What are the restart approval conditions?` | it can be mistaken that restart needs only pressure or only flow | restart-section lines and approval-blocking condition lines should rise to the top |

Input:

We read the CSV above and normalize question-specific relevance scores with softmax.

```python
from pathlib import Path
import csv
import math

DATA_PATH = Path("docs/assets/part-05/chapter-13/attention-operating-manual-candidates.csv")

QUESTIONS = {
    "What is the pressure-release holding time?": "score_pressure_hold",
    "What is the coolant-flow criterion?": "score_flow_limit",
    "What are the restart approval conditions?": "score_restart_permission",
}

with DATA_PATH.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

values = [float(row["evidence_signal"]) for row in rows]
baseline_context = sum(values) / len(values)

def softmax(scores):
    # Subtract the maximum so we can focus on how relative score differences create attention weights.
    max_score = max(scores)
    exp_scores = [math.exp(score - max_score) for score in scores]
    total = sum(exp_scores)
    return [score / total for score in exp_scores]

def run_attention(question, score_column):
    scores = [float(row[score_column]) for row in rows]
    weights = softmax(scores)
    context = sum(w * v for w, v in zip(weights, values))
    top_rows = sorted(zip(rows, weights), key=lambda item: item[1], reverse=True)[:3]

    print("question =", question)
    print("csv_rows =", len(rows))
    print("baseline_uniform_context =", round(baseline_context, 3))
    print("context =", round(context, 3))
    print("shift_from_baseline =", round(context - baseline_context, 3))
    for row, weight in top_rows:
        print(row["line_id"], row["section"], "weight =", round(weight, 3), "signal =", row["evidence_signal"])
    print()

for question, score_column in QUESTIONS.items():
    run_attention(question, score_column)
```

In the output, start by looking at how question-related candidate lines rise into the top 3.

```text
question = What is the pressure-release holding time?
csv_rows = 40
baseline_uniform_context = 6.88
context = 4.685
shift_from_baseline = -2.195
L10 pressure weight = 0.092 signal = 2.9
L05 pressure weight = 0.076 signal = 3.0
L07 pressure weight = 0.068 signal = 3.2

question = What is the coolant-flow criterion?
csv_rows = 40
baseline_uniform_context = 6.88
context = 9.922
shift_from_baseline = 3.042
L13 coolant weight = 0.093 signal = 12.0
L18 coolant weight = 0.084 signal = 12.6
L14 coolant weight = 0.076 signal = 11.6

question = What are the restart approval conditions?
csv_rows = 40
baseline_uniform_context = 6.88
context = 6.449
shift_from_baseline = -0.431
L25 restart weight = 0.097 signal = 7.2
L26 restart weight = 0.08 signal = 6.8
L30 restart weight = 0.072 signal = 6.6
```

- if all candidates are averaged equally as in the baseline, the context value becomes `6.88`, so pressure, coolant, restart, log, and handover lines are all mixed with the same weight
- in the pressure question, lines such as `L10`, `L05`, and `L07`, which describe hold time and stabilization waiting conditions, rise to the top
- in the coolant-flow question, lines such as `L13`, `L18`, and `L14`, which describe flow limits and pump conditions, rise to the top
- in the restart-approval question, lines such as `L25`, `L26`, and `L30`, which describe approval and blocking conditions, rise to the top
- that is, attention does not average all positions equally, but reflects more strongly the positions more relevant to the current question

The first result to look at in this example is the attention weight by question. In the pressure-release holding-time question, pressure candidate lines gather near the top, while in the coolant-flow criterion question, coolant candidate lines gather near the top.

![Attention weights for the pressure-release holding-time question](/AiBook/assets/part-05/chapter-13/attention-pressure-question-weights-en.png)

![Attention weights for the coolant-flow criterion question](/AiBook/assets/part-05/chapter-13/attention-flow-question-weights-en.png)

The second result to look at is the context value. The baseline average stays at `6.88` because it cannot distinguish the question, but the attention context changes to `4.685`, `9.922`, and `6.449` depending on the question.

![Comparison of question-specific attention context and the baseline average](/AiBook/assets/part-05/chapter-13/attention-context-comparison-en.png)

Even when reading the output numbers, we need to separate `the same candidate set` from `the weight that changes according to the question`.

| Comparison | What first appears in the output | Interpretation that is easy to keep if we only look at the average | Interpretation that changes when attention is included |
| --- | --- | --- | --- |
| `baseline_uniform_context` | for all three questions, the baseline is the same `6.88` | it can look as if the context should stay almost the same when the CSV is the same | the baseline cannot reflect the question, so even when the position needed right now changes, it remains at the same average value |
| `What is the pressure-release holding time?` | pressure lines gather in the top 3 | it can look as if low-valued lines were chosen by chance and the context simply moved downward | because the question is about holding time, attention redistributes the weight so pressure-hold candidates are referred to more strongly |
| `What is the coolant-flow criterion?` | coolant lines gather in the top 3 | with the same CSV, it can look as if larger-valued lines were simply chosen by chance this time | when the question changes, the reference weights are redistributed, so the context on the flow-criterion side is formed more strongly |
| `What are the restart approval conditions?` | restart lines gather in the top 3 | it can look as if pressure and flow lines are enough for restart | the restart question partly refers to pressure and flow cues, but refers more strongly to final approval and blocking-condition lines |

## If We Reread This Example As A Question-Candidate Comparison

The numbers above do not calculate the whole real word-embedding space, but the intuition is clear.

- the baseline average reflects only the fact that `the candidate lines were simply all in the same CSV`
- the attention weighted average redistributes the weight among the candidates according to `what the current question is`
- so when the question changes among `pressure-release holding time`, `coolant-flow criterion`, and `restart approval conditions`, the position referred to most strongly also changes even with the same candidate group

That is, attention is not simply a method of gathering more information, but `a method of deciding again what information should be mixed more strongly according to the current question`.

Attention gained major influence in sequence-to-sequence translation research, and later, as it continued into self-attention and the Transformer, it became one of the core methods of context reference in modern deep learning. The conclusion the reader should keep from this section is simple. Attention is closer to `a structure that looks again strongly at the position needed now` than to `a structure that carries information for a long time`. In the next section, P5-13.2, we explain how this direct-reference idea continues into a structure where tokens inside the same sequence reread one another.

## Checklist

- Can you explain that attention is `a method that looks again at the positions that are needed`?
- Can you explain the connection between the long-term dependency problem and attention?
- Can you explain that attention is a method that refers more strongly to the positions important for the current computation?
- Can you say that this is a more direct response to the long-term dependency problem?
- Can you explain attention not as `a method that leaves memory for longer`, but as `a method that looks again more strongly at the position needed now`?
- Can you explain the difference between the baseline average and the weighted average using the current question as the standard?
- When the explanation of preserving state for a long time is not enough to explain why performance becomes blocked, can you recall the direct-reference viewpoint of attention first?
- When reading the next section on self-attention, are you ready first to ask `where inside the same sequence does the current token need to look again`?

## Sources And References

- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, ICLR 2015, checked on 2026-07-19. [https://arxiv.org/abs/1409.0473](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Kyunghyun Cho et al., `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`, arXiv, 2014, checked on 2026-07-19. [https://arxiv.org/abs/1406.1078](https://arxiv.org/abs/1406.1078){: target="_blank" rel="noopener noreferrer" }
