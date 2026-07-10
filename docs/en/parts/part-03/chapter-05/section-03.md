# P3-5.3 Why Can We Not Immediately Call Raw Time Series a Learning Input

> Section ID: `P3-5.3`
> Version: `v2026.07.10`

When readers see a raw time series, many of them think like this: `There are many values and they are ordered, so can't we just pass this straight in as the learning input?` But we should pause here once. The mere fact that a raw time series exists does not yet mean we can say `a ready-to-use learning input has been prepared`.

The raw time series may contain a lot of information, but `what should count as one sample`, `how much length should be grouped into one input`, and `what we want to predict` may still be undecided. A learning input is not another name for raw data. It is an input structure whose boundaries are fixed to fit a problem. So the first distinction to hold onto in this section is that `a raw time series exists` and `a learning input is ready` are not the same sentence.

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
| Deep learning will learn the features by itself | Where will we cut the input? |
| There are many raw logs, so learning can start right away | What will count as the result column? |

## What Else Is Needed to Turn Raw Time Series into a Learning Input

To turn a raw time series into an actual input structure, at least the following decisions must already exist.

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
| Summary table | It lets us establish the basic comparison unit and baseline comparison first |
| Segment representation | It lets people read order and structure first |
| Aggregate table | It lets us interpret recent state and usual state operationally |

So the existence of a raw time series does not make the summary table unnecessary. Some questions are read more directly from the summary table first, and some may later move on again to a longer input structure.

## Looking Again Through One Scene

Suppose an action contains 300 time-point records.

1. In Part 3, we first decide whether these 300 points form `one full action`.
2. We divide them into early, middle, and late segments and build a summary table.
3. If needed, we preserve more structure through an intermediate representation such as `UP, FLAT, DOWN`.
4. Only after that can we choose whether to view that one full action as one input, as several segment sequences, or as a recent-range aggregate.

So the correct order is not `a raw time series exists -> it is immediately a learning input`, but `a raw time series exists -> decide what input structure to convert it into`.

What this section should hold onto is not the model type, but the order that says before calling a raw time series an input, we should first decide sample boundaries, segment criteria, and target structure. So saying that the raw time series is not yet a learning input means less `the data is insufficient` and more `the boundaries and purpose of the input structure have not yet been specified`.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example is a structure where features and labels are defined together, it supports the claim that before calling a raw time series an input, the boundary of one sample and the result column should first be fixed. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it explains a design flaw where a feature becomes a proxy for the label, it reinforces the point that unless the input structure and target structure are fixed first, part of the raw time series can be passed through incorrectly as the input. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because the provenance framework says identifying an object, derivation, and reproducibility should be supported, it reinforces the higher-level frame that input length and segment rules should also remain reproducible as a designed structure. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
