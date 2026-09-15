# P3-5.3 Why Can We Not Immediately Call Raw Time Series a Learning Input

> Section ID: `P3-5.3`
> Version: `v2026.09.15`

Do not hide this choice in the table either. If you build a summary vector, each row can keep `event_id` and a structure memo such as `input_type=event_summary`. If you keep a segment sequence, you need `event_id`, `segment_index`, and `segment_order`. For a recent aggregate input, keep `window_id`, `window_start`, `window_end`, and `source_event_count`. Exposing the input structure as columns lets you explain again which rule turned the raw time series into a candidate learning input.

When readers see a raw time series, many of them think like this: `There are many values and they are ordered, so can't we just pass this straight in as the learning input?` But we should pause here once. The mere fact that a raw time series exists does not yet mean we can say a ready-to-use learning [model input](/AiBook/en/reference/concept-glossary-alpha/m/#model-input) has been prepared.

The raw time series may contain a lot of information, but what should count as one [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample), `how much length should be grouped into one input`, and `what we want to predict` may still be undecided. A learning input is not another name for raw data. It is an input structure whose boundaries are fixed to fit a problem. So the first distinction to hold onto in this section is that `a raw time series exists` and `a learning input is ready` are not the same sentence.

The shortest first split looks like this.

| What we currently have in hand | What is still missing |
| --- | --- |
| A raw time series with time-point measurements extending in sequence | Sample boundaries |
| The time order of sensor values and control values | Input length and segment criteria |
| Rich original information | Target labels and comparison questions |

So `a raw time series exists` and `a learning input is ready` do not mean the same thing.

## Why `Just Put It In As-Is` Sounds Fast

The idea of feeding the raw time series in as-is sounds fast for three reasons.

1. When there are many rows and columns, it already feels like a rich dataset.
2. When we hear that deep learning learns representations, it can feel as if input design can be skipped.
3. The more complex the time-series structure is, the more it seems that the model will learn it by itself better than a human summary would.

But all three are illusions that appear when `defining the input structure` and `learning a representation` are read as if they were the same thing.

| The thought that comes quickly | The question Part 3 should ask first |
| --- | --- |
| The longer the time series, the better it is to feed it in directly | Is one sample one full action or one recent range? |
| Deep learning will learn the [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature) by itself | Where will we cut the input? |
| There are many raw logs, so learning can start right away | What will count as the result column? |

## What Else Is Needed to Turn Raw Time Series into a Learning Input

| Decision to make first | Why it is needed |
| --- | --- |
| Sample boundary | Define where one input starts and ends |
| Whether and how to segment | Decide whether to retain the full sequence or compare segment summaries |
| Length handling | Match the input format by retaining variable lengths, truncating, or padding |
| Learning objective | Define labels for supervised learning, or the boundary between input and future values for next-value prediction |

| What must be decided first | Why it is necessary |
| --- | --- |
| Sample boundaries | We have to decide where one input starts and ends |
| Segment-cutting rule | We need a comparison criterion such as early/mid/late |
| Length-alignment rule | Inputs with different lengths are hard to compare immediately |
| Target-label candidates | We have to decide what we want to predict |

For example, the same raw time series can become completely different input structures like these.

| Possible input structures from the same raw log | The question that structure directly answers |
| --- | --- |
| A vector summarizing one full action | Will one action be compared as one row-table input? |
| A segment sequence for one full action | Will one action be read while keeping segment order? |
| An aggregate input built by regrouping the most recent 20 cases | Will recent state be compared as one grouped unit? |

So a raw time series does not naturally point to one model. Depending on the problem we set up, it can be rebuilt into very different input structures. Even with the same record, whether `one-action vector`, `segment sequence`, or `recent aggregate input` comes first is determined by the question.

## Why Summary Tables and Intermediate Representations Are Still Needed

A common misunderstanding here is the thought that `if we are going to look at time-series models later anyway, summary tables or segment representations matter less`. But summary tables and intermediate representations are not just temporary objects. They remain important for at least the following three reasons.

| Structure built first in Part 3 | Why this structure is needed first |
| --- | --- |
| [Summary table](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling) | It lets us establish the basic comparison unit and [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) comparison first |
| [Segment representation](/AiBook/en/reference/concept-glossary-alpha/i/#glossary-intermediate-representation) | It lets people read order and structure first |
| Aggregate table | It lets us interpret recent state and usual state operationally |

So the existence of a raw time series does not make the summary table unnecessary. Some questions are read more directly from the summary table first, and some may later move on again to a longer input structure.

## Looking Again Through One Scene

Suppose an action contains 300 time-point records.

1. Part 3 first decides whether these 300 points constitute `one action`.
2. Choose whether to retain the action's full sequence or reduce it to early, middle, and late summaries.
3. If needed, retain more structure through an intermediate representation such as `UP, FLAT, DOWN`.
4. Document time order, length handling, and missing-value rules for the chosen representation. A summary table is not a prerequisite for using a raw time series as input.

So the correct order is not `a raw time series exists -> it is immediately a learning input`, but `a raw time series exists -> decide what input structure to convert it into`.

## From Sample Boundaries and Learning Objectives to Input Structure {#a-small-diagram}

The sequence of decisions in this section does not stop at `we have a raw time series`. Choosing an `input structure` also requires sample boundaries, segment/length rules, and a learning objective.

--8<-- "assets/part-03/chapter-05/p3-5-3-mermaid-01-en.mmd"

What this section should hold onto is not the model type, but the order that says before calling a raw time series an input, we should first decide sample boundaries, segment criteria, and target structure. So saying that the raw time series is not yet a learning input means less `the data is insufficient` and more `the boundaries and purpose of the input structure have not yet been specified`.

## Checklist

- Did you specify sample boundaries, length handling, and missing-value rules even when retaining raw time series?
- Did you distinguish why handcrafted summaries are optional from why a learning objective is needed?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`, `example`, `labeled example`. An example may lack a label; a labeled example includes features and a label. Used for sample and learning-objective terminology; it does not require every input to have an answer label. [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-15
- Google for Developers, `Machine Learning Glossary`, `label leakage`. Its explanation of features becoming proxies for labels supports the risk of passing inappropriate time-series information into a model when input and target structures are undefined. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){ target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-20
- W3C, `PROV-Overview`. The provenance framework covers identifying objects, derivation, and reproducibility, providing a framework for reproducibly documenting how input lengths and segment rules form a structure. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){ target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-20

- [Google Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){ target="_blank" rel="noopener noreferrer" }. Checked the distinction between supervised-learning labels and general input structures. Checked: 2026-09-15.
