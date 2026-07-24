# P6-7.2 Scale That Grows Capability and Operational Burden Together

> Section ID: `P6-7.2`
> Version: `v2026.07.23`

In P6-7.1, we explained pretraining as the `stage that first creates a broad language base`. Then the next question follows. `Why do large datasets, large models, and large amounts of computation always come along when making that base?`

In other words, the starting point of this section is not `larger models look better`. Rather, it is `why scale becomes a problem when making a broad base`, and `what that scale-up makes possible and what burden it leaves behind`.

Scale refers to the phenomenon where data volume, model size, and computation all grow together, and although it is strongly connected to LLM performance improvement, it also increases cost and risk together.

## Criteria to Read Together in Scale-Up

Scale-up judgment begins with the following questions.

- What does scale mean?
- Why should data, parameters, and compute be read together?
- Why can performance improve as scale grows, while cost and risk also grow?

Scale is a `structure where data, parameters, and computation grow together, changing performance potential and cost burden at the same time`. This criterion is needed so we do not read large foundation models as a simple performance race.

Next-token prediction is a problem of `what is used as the training objective`, and operational constraints are a problem of `what must be handled when running it as a service`. Scale is the link between them, where capability and burden grow together as the foundation grows larger.

We should avoid the impression that `larger is always better`. If P6-7.1 dealt with `what is learned first`, here we read `why that learning is run at such a large scale`. Before moving on to service connections such as prompts or RAG, we need to be able to judge why later fine-tuning and instruction tuning are usually placed on top of a `large foundation model`.

Therefore, what we must first grasp is not `larger models are better`, but that `as scale grows, capability and burden change together`.

## Why Read Scale Right After Pretraining?

Here, it is easy to receive the explanation `first make a broad base` and the phrase `therefore large models matter` as one bundle. But the two are not the same. P6-7.1 explained `what is learned first`, and this section explains `what actually grows together to make that base`.

We need to separate this difference so later fine-tuning and instruction tuning are also read more accurately. If we do not know what the cost and burden of first making a foundation are, it becomes easy to blur why adjustment stages are usually explained as `adding more on top of an already large base` rather than `learning everything again from scratch`.

The flow should be read as follows. If the previous section grasped what the model learns first, here we look at why data, parameters, and computation grow together when making that base. How to further fit specific tasks and user requests on top of a large base will be separated again later in fine-tuning, instruction tuning, prompts, RAG, and operational policy.

In other words, this section is not `praise for large models`, but a place to read `what capability and cost the phrase making a large base actually means together`. We first distinguish what can improve when data, parameters, and computation grow together, and why performance potential, cost, and risk grow together.

Here we set the baseline that changes the simple impression `a larger model is better` into `data, parameters, and computation grow together, and performance potential and cost burden grow together`.

## Distinguishing Capability and Burden Grown by Scale

- You can explain scale from the perspective of expanding data, model, and computation.
- You can say that performance improvement and cost increase go together.
- You can explain that data quality and verification responsibility become more important with scale.
- You can read later adjustment and operation judgments on top of the capability-burden balance of scale.

Here, we need to remember two things together.

1. Scale is an important factor in performance transitions
2. Scale also grows data quality, verification, cost, and policy problems

We need to include both to connect the pretraining objective from P6-7.1 with `why it is run at such a large scale`, and to naturally continue the perspective in later evaluation and operational-constraint sections, P6-16.1 and P6-17.1, that `as performance grows, cost and control problems also grow`. Reading this way also supports balanced judgment in later chapters of Part 6 and the Part 7 project.

## Judgment Criteria for Capability and Burden

Scale cannot be judged by model size alone. We need to see together what scale-up makes possible and what it makes us handle more.

| Judgment Criterion | Question to Check |
| --- | --- |
| Expanding axes | Do data, parameters, and computation grow together? |
| Capability change | Do longer contexts, more complex requests, and broader pattern handling become possible? |
| Operational burden | Do cost, latency, and incident-response burden grow together? |
| Data responsibility | Does the scope of data quality, duplication, copyright, and bias review also grow? |

## What Does Scale Grow Together?

In an LLM context, scale usually does not mean only one thing getting bigger. The following usually grow together.

- amount of training data
- number of model parameters
- training computation

`Making a model larger usually goes together with seeing more text, using more parameters, and putting in more computational resources.`

## Why Can Performance Improve as Scale Grows?

The intuitive answer to this question is as follows.

- more data lets the model see more diverse language patterns
- a larger model gives the expressive capacity to contain more complex patterns
- more computation makes it possible to actually learn that structure

In other words, scale is not a simple size race, but connects to the `conditions for containing patterns more broadly and more finely`.

So in the history of LLM development, model scale and data scale are often mentioned together with performance transitions.

## Why Do Cost and Latency Also Grow Together?

But as scale grows, only good things do not appear.

- training cost grows
- inference cost can also grow
- response latency can increase
- operational complexity and incident-response burden grow

In other words, scale is a performance problem and also a service-operation problem.

This point connects directly to later explanations of operation, evaluation, and constraints in Part 6.

## Is More Data Always Better?

We need to see this together to judge how scale can raise performance while also growing data quality, cost, and policy burden.

Increasing data volume matters, but quality problems do not disappear.

For example, problems such as:

- outdated information
- duplicated data
- biased expressions
- copyright issues
- incorrect facts

can remain or grow larger even when data increases.

Therefore, a safer explanation is as follows.

`Scale increases performance potential, but it does not remove data quality and verification responsibility.`

## Why Did Scale Change User Experience?

As scale grew, users came to feel changes such as the following more directly.

- responses that seem to handle long contexts more naturally
- reactions to more diverse task instructions
- improved zero-shot and few-shot use experiences
- the feeling that several tasks can be performed with only natural-language queries

But this still does not immediately guarantee `understanding` or `factuality`.

In other words, scale greatly changes user experience, but it does not remove verification responsibility.

## What Grows Together in Scale Judgment

If we summarize this so far in the shortest form, it is as follows.

- Scale increases the `possibility of handling broader patterns`.
- At the same time, it also increases `larger cost and operational burden`.
- Therefore, the phrase `larger` must always be read together with `what gets better and what must be handled more`.

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-06/chapter-07/p6-c07-s02-scale-tradeoff-en.mmd"
```

The core of this diagram is one thing.

`Scale grows performance potential and cost/risk together.`

## Cases and Examples

The diagram below regroups a scale-up decision not as the one-line judgment `is a larger model better?`, but as a question that reads capability, cost, and data-verification burden together.

```mermaid
--8<-- "assets/part-06/chapter-07/p6-c07-s02-scale-decision-en.mmd"
```

What we should confirm from this diagram is that scale-up does not close with one line, `performance improvement`. The same change can look to users like processing longer requests, to the operations team like increased cost and latency, and to data owners like more source data to verify.

### Case. Scale-Up Decision Meeting

Suppose a customer-support team is meeting about whether to move the currently used small model to medium or large. The current model answers short FAQs quickly, but often fails on requests that summarize long contract clauses or read code error logs together. The criterion people first tend to see in the meeting is `if we switch to large, it will do better`. But from the scale perspective, we first need to split the questions.

First, on the capability axis, we look at which requests become newly possible. If the context window widens and model expressiveness grows, there is a possibility of better handling long contracts, long error logs, and complex requests with several mixed conditions. Second, on the cost axis, we look at how much latency and inference cost increase when handling those requests. Third, on the data axis, we see that as more data is used for pretraining or later adjustment, quality problems such as duplication, outdated information, copyright, and bias must be reviewed more broadly.

The result to check in this case is not only `can large handle more requests?` Even if it can handle more requests, that choice may not be best if cost and latency exceed service limits, or if the data-verification burden cannot be handled. Conversely, if medium gives enough improvement within cost and operational burden even while giving up some long requests, it may be the more realistic choice for the current service.

| Scale Stage | What You Gain | What You Must Also Handle |
| --- | --- | --- |
| keep `small` | handle short FAQs with low cost and fast responses | long contracts, long code logs, and complex requests may keep failing |
| switch to `medium` | possibility of handling some long and complex requests | cost and latency increase, and the data scope to verify grows |
| switch to `large` | possibility of handling some long contracts and code logs | inference cost, latency, and data-quality review burden grow significantly |
| switch to `frontier` | possibility of placing the longest multi-document requests inside context | cost, latency, and verification burden become largest, requiring operational criteria to be reset |

This table becomes the criterion for reading the Python example below. The case shows `why the three axes must be compared together`, and the example checks how those three axes change as numbers by stage.

## Scenes Where Scale Judgment Is Needed

After reading this section, even if you do not yet know actual model price lists or benchmarks, you can first practice distinguishing whether what is needed now is `larger capability` or `first reducing cost, latency, and verification burden`. If requests that read long contracts and long logs together often fail, before seeing a larger model as solving everything, you should ask whether what is actually needed is longer context and greater expressiveness. If answer quality improved but responses became slow and cost jumped sharply, the fact that performance improved and whether cost and latency can be handled within service limits must be read separately. If performance improved by using more data but the data bundles to verify grew greatly, you should also see whether what grew is not only capability but also verification responsibility and policy burden.

What matters here is not memorizing either `large models are good` or `small models are cheap`, but first reading `what can be handled more` and `what must be handled more` together.

The things often mixed here are as follows.

- It is easy to see performance improvement and operational feasibility as only one axis.
- It is easy to fail to distinguish problems that need a larger context window from simple cost problems.
- It is easy to feel that data-scale expansion is the same thing as quality guarantee.

Therefore, the sentence `scale grows performance potential and cost/risk together` should become a criterion for real service judgment.

## Exercise and Example

The goal of this example is to separate, by stage, `what can be handled more` and `what must be handled more` as scale grows. Instead of comparing a small model and a large model all at once and choosing a winner, we will track how data amount, parameter count, training computation, context range, inference cost, latency, and verification burden move together when scale grows from `small -> medium -> large -> frontier`.

Input:

The code below uses two input CSV files.

- request list: [p6-7-scale-requests.csv](/AiBook/assets/part-06/chapter-07/p6-7-scale-requests.csv){ .csv-preview }
- scale stages: [p6-7-scale-steps.csv](/AiBook/assets/part-06/chapter-07/p6-7-scale-steps.csv){ .csv-preview }

One row in the request list is one user request. `request_type` indicates the request character, such as FAQ, summarization, contract review, code assistance, and multi-document request, and `input_tokens` is a simplified value for the input length needed to place that request inside context. One row in the scale-stage CSV is one model-scale assumption, and `context_window`, `cost_per_1k_tokens`, `latency_per_1k_tokens`, and `review_batches` are the manipulation variables readers can directly change in this example.

In the result, we check the number of processable requests by scale stage, the number and types of context-over-limit requests, the number of high-priority requests that still exceed context, total expected inference cost and latency, and the number of data-verification waiting batches. The numbers here are not actual price or performance tables for a specific commercial model, but assumed values for operational judgment practice that separates the axes for reading scale.

The key point to confirm is that scale is the phenomenon where data, model, and computation grow together. When the context window grows, longer requests can be handled, but inference cost and latency can also grow, and as data volume grows, the burden of verifying data quality grows together.

```python
# This example reads a CSV request list and scale-stage table to compare processable range and cost burden together.
from csv import DictReader
from pathlib import Path

REQUESTS_PATH = Path("docs/assets/part-06/chapter-07/p6-7-scale-requests.csv")
STEPS_PATH = Path("docs/assets/part-06/chapter-07/p6-7-scale-steps.csv")


def load_requests(path):
    with path.open(newline="", encoding="utf-8") as f:
        return [
            {
                "request_id": row["request_id"],
                "request_type": row["request_type"],
                "input_tokens": int(row["input_tokens"]),
                "priority": row["priority"],
            }
            for row in DictReader(f)
        ]


def load_steps(path):
    with path.open(newline="", encoding="utf-8") as f:
        return [
            {
                "scale": row["scale"],
                "rank": int(row["rank"]),
                "context_window": int(row["context_window"]),
                "cost_per_1k_tokens": float(row["cost_per_1k_tokens"]),
                "latency_per_1k_tokens": float(row["latency_per_1k_tokens"]),
                "review_batches": int(row["review_batches"]),
            }
            for row in DictReader(f)
        ]


def summarize_scale_step(step, requests):
    supported = [
        request
        for request in requests
        if request["input_tokens"] <= step["context_window"]
    ]
    over_limit = [
        request
        for request in requests
        if request["input_tokens"] > step["context_window"]
    ]
    total_tokens = sum(request["input_tokens"] for request in requests)
    over_limit_types = sorted({request["request_type"] for request in over_limit})
    high_priority_over_limit = [
        request for request in over_limit if request["priority"] == "high"
    ]

    return {
        "scale": step["scale"],
        "context_window": step["context_window"],
        "supported_requests": len(supported),
        "over_limit_requests": len(over_limit),
        "over_limit_types": over_limit_types,
        "high_priority_over_limit": len(high_priority_over_limit),
        "total_inference_cost": round(
            (total_tokens / 1000) * step["cost_per_1k_tokens"],
            2,
        ),
        "total_latency": round(
            (total_tokens / 1000) * step["latency_per_1k_tokens"],
            2,
        ),
        "review_batches": step["review_batches"],
    }


requests = load_requests(REQUESTS_PATH)
steps = sorted(load_steps(STEPS_PATH), key=lambda step: step["rank"])

print(f"request_rows = {len(requests)}")
print(f"scale_steps = {len(steps)}")
for step in steps:
    print(summarize_scale_step(step, requests))
```

This example was run with the local `.venv` Python environment and checked against the output in the body.

The execution result example can be read as follows.

```text
request_rows = 36
scale_steps = 4
{'scale': 'small', 'context_window': 2048, 'supported_requests': 8, 'over_limit_requests': 28, 'over_limit_types': ['code_assistant', 'contract_review', 'multi_document', 'summary'], 'high_priority_over_limit': 16, 'total_inference_cost': 52.38, 'total_latency': 183.33, 'review_batches': 2}
{'scale': 'medium', 'context_window': 4096, 'supported_requests': 13, 'over_limit_requests': 23, 'over_limit_types': ['code_assistant', 'contract_review', 'multi_document', 'summary'], 'high_priority_over_limit': 16, 'total_inference_cost': 144.04, 'total_latency': 288.09, 'review_batches': 7}
{'scale': 'large', 'context_window': 8192, 'supported_requests': 24, 'over_limit_requests': 12, 'over_limit_types': ['code_assistant', 'contract_review', 'multi_document'], 'high_priority_over_limit': 12, 'total_inference_cost': 314.28, 'total_latency': 471.42, 'review_batches': 22}
{'scale': 'frontier', 'context_window': 32768, 'supported_requests': 36, 'over_limit_requests': 0, 'over_limit_types': [], 'high_priority_over_limit': 0, 'total_inference_cost': 838.08, 'total_latency': 811.89, 'review_batches': 75}
```

The core to read in this example is as follows.

- `small` places only 8 short FAQs inside context, leaving the other 28 requests over the context limit.
- `medium` handles up to some summarization requests, but 16 high-priority requests still exceed context.
- `large` handles 24 requests, but 12 long contract, code, and multi-document requests still remain.
- `frontier` places all 36 requests inside context, but total inference cost, latency, and data-verification batches are the largest.
- `review_batches` simply shows that as data volume grows, the batches to verify also grow together.

When separated as graphs, it becomes clearer that the three axes grow with different meanings. First, as context range grows, the number of processable requests increases.

![Number of processable requests by scale stage](/AiBook/assets/part-06/chapter-07/scale-context-coverage-en.png)

But the total inference cost for handling the same request bundle also grows. What this graph confirms is not that `large` handles more requests, but that the choice comes with cost increase.

![Total inference cost by scale stage](/AiBook/assets/part-06/chapter-07/scale-inference-cost-en.png)

When data volume grows, the data-quality burden to verify also grows. The graph below is not an actual risk measurement value, but a simplification to show the structure that as data increases, the batches to review also increase.

![Data verification burden by scale stage](/AiBook/assets/part-06/chapter-07/scale-data-review-burden-en.png)

In this example, readers can directly change `input_tokens` and `priority` in the request CSV, and `context_window`, `cost_per_1k_tokens`, `latency_per_1k_tokens`, and `review_batches` in the scale-stage CSV. For example, if you increase long contract requests, the context over-limit issue for `small` and `medium` becomes more visible; conversely, if only short FAQs remain, you can reconsider whether the additional cost of `frontier` is really needed.

## Choices Split by Scale-Cost Balance

This comparison helps avoid a one-line understanding such as `larger models are better`. Since actual selection is always a problem of reading capability expansion and increased training/inference cost together, later model selection and operation sections should treat scale as simultaneous judgment axes of `performance`, `context range`, `cost`, and `latency`.

Scale is an unavoidable topic when understanding the LLM era. Especially after GPT-3, many discussions connected scale to `why models began to show these capabilities`.

If we reduce this example back into judgment criteria, the following three questions should come first.

| Scene | Question to Answer First |
| --- | --- |
| Why does a larger model seem necessary for some requests? | Is the current failure a problem that needs longer context and greater expressiveness? |
| Why does better performance not immediately become the operational optimum? | Are cost and latency exceeding service limits? |
| Why does verification burden also grow as data increases? | Are the scope of quality, copyright, and bias review growing together with capability expansion? |

## Checklist
- Can you explain scale as a pair of `what gets better` and `what must be handled more`?
- Can you see long context, performance improvement, and operational cost together on one axis?
- Are you ready to read the next chapters by separating the performance of large foundation models from later adjustment cost?

## Sources and References

- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, accessed 2026-07-19. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }
- Jared Kaplan et al., `Scaling Laws for Neural Language Models`, arXiv, 2020, accessed 2026-07-19. [https://arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361){: target="_blank" rel="noopener noreferrer" }
- Jordan Hoffmann et al., `Training Compute-Optimal Large Language Models`, arXiv, 2022, accessed 2026-07-19. [https://arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556){: target="_blank" rel="noopener noreferrer" }
- OpenAI Docs, `Models`, model-specific price and context window examples, accessed 2026-07-19. [https://developers.openai.com/api/docs/models](https://developers.openai.com/api/docs/models){: target="_blank" rel="noopener noreferrer" }
