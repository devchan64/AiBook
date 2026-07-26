# P6-17.1 Operational Constraints That Filter Again by Cost, Latency, and Usage

> Section ID: `P6-17.1`
> Version: `v2026.07.26`

Even if evaluation selects a good answer candidate, that does not immediately make a service viable. The answer must be provided within a waiting time users can tolerate, at an affordable cost, and repeatedly even when expected request volume arrives. Service operational constraints are a separate pass line that filters candidates that already passed quality evaluation into actual operational candidates.

An AI service is not decided by model quality alone. It must operate inside real constraints such as cost, latency, usage limits, and failure possibility. Even with a good model, a service is hard to call good if it is too slow, too expensive, or stops too often.

## What operational-limit judgment handles

The core questions are:

- Why is a good model alone not enough for a good service?
- How do cost, latency, and usage limits create problems?
- What must be traded off together in service design?

If AI service judgment is trapped only inside `model performance`, important failures are missed. Even a candidate that passed quality evaluation can fail again as an operational candidate if it is too slow, too expensive, or cannot handle concurrent requests. So the question at this stage is not `is there a good model`, but `can this good answer be provided repeatedly within operational limits`.

Service-limit judgment looks at the following together.

| Operational constraint | Question to ask | First thing to adjust when blocked |
| --- | --- | --- |
| Cost | Is the cost of one request and repeated requests inside the budget? | Model size, context length, number of tool calls |
| Latency | Does the answer arrive within the time users can wait? | Search depth, generation length, cache, lightweight path |
| Throughput and capacity | Can the service handle expected request volume concurrently? | Queue, cache, rate limit, infrastructure limits |
| Recoverability | Is there an alternate path when the heavy main path is blocked? | Fallback answer, partial response, human handoff |

So `evaluation pass` and `operational candidate pass` are not the same thing. If evaluation separates quality axes of the answer, operational-limit judgment separates whether that quality can be provided repeatedly.

The first judgment to keep at this stage should show which operational limit blocked the candidate, where to adjust next, and whether an answer that passed evaluation can remain as a real operational candidate.

This judgment becomes input for failure handling and real request records.

| What operational-limit judgment leaves | Operational path that branches | Representative value to leave in request records |
| --- | --- | --- |
| Latency is the main constraint | Adjust timeout criteria, lightweight path, fallback review | Next action, incident note, execution note |
| Cost is the main constraint | Reduce calls, use smaller model, shorten steps | Next action, execution record, cost summary |
| Throughput is the main constraint | Queue, cache, throughput-limit path review | Next action, incident note, operations note |
| Candidate can remain operational | Keep operational candidate | Status summary, operations summary, request run record |

Operational-limit judgment is therefore not a table read once and forgotten. It is an input to failure-handling branches and request-flow records.

## Separating evaluation pass from operational viability

Once this distinction is held, AI service constraints can be read not as a list of operations terms, but as standards for seeing how cost, latency, and usage limits collide with quality. It also becomes clearer why going over an operational limit must immediately move into a failure-handling path.

The first scenes to separate are:

| First visible blockage | First question to ask | Why this question is needed first |
| --- | --- | --- |
| Answer quality is fine, but it feels too slow to users | Does latency exceed the allowed range? | Quality pass and service-experience pass differ, so response time must be judged separately. |
| It works, but operating burden grows sharply as calls increase | Does cost exceed the repeated-operation budget? | A service judgment asks whether it can run continuously, not only whether it succeeded once. |
| One or two requests work, but the system collapses under traffic | Are capacity and throughput limits blocked first? | Demo success and repeated-request operation differ. |
| More steps were added to raise quality, and the whole path became too heavy | Should processing depth be reduced or split into fallback paths? | More steps are not always a better service, so allowed depth must be judged inside operational limits. |

This table helps read service operational constraints not as `operations vocabulary`, but as the criteria that explain why an answer that passed evaluation can fail again as an actual service candidate.

## Why model quality alone is not enough

Even if a model can produce good answers, a real service must also satisfy speed, cost, throughput, and stability. So the question moves from `does it work well` to `can it keep operating`.

- It must respond fast enough.
- It must not be too expensive.
- It must handle many requests.
- It must not completely stop when failure occurs.

Service is therefore a problem that includes `operational viability`, not only `answer quality`.

## Why cost is a large problem

AI services usually create cost per call, or infrastructure cost when operated directly. The burden grows especially when the following increase together.

- long input context
- long output
- larger model
- more tool calls
- more retries

`Agent structures and RAG structures can improve quality, but as call stages increase, cost can increase with them.`

The first important point is that `more features = always better choice` is false.

## Why latency matters

Users do not only want `the right answer`; they also want `an answer within a time they can wait`.

For example, latency can accumulate when these steps are chained:

- document retrieval
- model generation
- tool calls
- postprocessing

The service must then ask:

- Must every step run every time?
- Can some steps be cached?
- How much slowness is acceptable?

Latency is therefore also a user-experience problem, not only a technical problem.

The same answer arriving within 2 seconds and after 20 seconds creates a different service experience. Latency can seem less important than accuracy, but in real use it can strongly affect adoption.

## Usage limits and capacity problems

As a service grows, request volume grows too. Then the following problems can appear.

- requests-per-minute limit
- concurrent-processing limit
- model-provider API limit
- internal infrastructure bottleneck

It can be read like this.

`A good demo and an operable service are different. A demo only needs to work once, but a service must withstand repeated requests.`

This sentence is especially important for readers. Many AI demos are impressive, but when moved into real service, concurrent requests and cost often appear first.

## Why quality and constraints must be read together

This point matters.

Using a larger model can improve quality. But it can also:

- increase cost
- increase latency
- increase operational complexity

Using a smaller model can:

- make responses faster
- lower quality or stability

Service design is therefore usually a balance problem:

`What level of quality should be provided, at what cost and speed, and under what usage range?`

In the same service flow:

| What we want to increase | Burden that can increase together |
| --- | --- |
| Larger model | Cost, latency |
| More retrieved documents | Cost, context length, processing time |
| More tool calls | Failure points, operational complexity |

Shortened into deployment-candidate judgment, the following checklist should appear first.

| Check again before keeping as a deployment candidate | Why it must be checked again |
| --- | --- |
| Did it pass quality evaluation? | A good-looking answer must first pass real criteria. |
| Is latency inside the allowed range? | Even the right answer can fail as a service if it arrives too late. |
| Is cost inside the call budget? | One success must be sustainable as repeated operating cost. |
| Can capacity handle the load? | Demo success and repeated-request operation differ. |
| Is there a fallback or lightweight path? | The system should not completely stop when the main path is heavy. |

`Evaluation pass` and `operational candidate pass` are not the same thing. This is why practical materials often treat LLMOps or serving as separate modules.

## Why RAG and AI agent structures become more complex

Compared with simple chat, RAG and AI agents have more steps.

- retrieval
- document organization
- model generation
- tool calls
- retries

As steps increase:

- the number of calls increases
- failure possibility increases
- latency accumulates
- logging and evaluation cost also grow

The stronger the structure becomes, the stronger operational constraints become.

In a simple prompt-only structure, constraints are relatively simple. But when RAG and AI agents are added, the core of this section is that `steps for making a good answer` and `the operational burden of maintaining those steps` grow together.

Simplified once more:

```mermaid
--8<-- "assets/part-06/chapter-17/p6-c17-s01-service-constraint-flow-en.mmd"
```

The core of this figure is that choices that raise quality often bring more steps and operational burden with them.

## Cases and examples

The focus of these cases is not `does it look good`, but `can it continue to be provided inside operational constraints`.

### Case 1. Customer-support chatbot

Suppose a customer-support chatbot retrieves all long policy documents every time and always generates a long answer. At first, it is easy to think `if it reads more and answers longer, it will be a better chatbot`. This can make answers look more detailed and accurate. But even for a simple question such as password reset, users must wait several seconds, and the actual experience can remain `smart but slow`.

For a short status-check question such as delivery tracking, attaching a long policy explanation every time may look accurate, but users can feel that the answer is late and excessive. Some users may leave without reading to the end. The first operational problem people see is not only quality, but `can customers tolerate this speed`. The result to check in this case is whether response time harms actual use experience separately from answer-quality improvement, and whether short questions can close without excessive processing.

This is a real operational scene because customer-perceived quality is not decided only by accuracy. If a short question takes too long or carries an unnecessary long answer, users feel latency and fatigue before intelligence. Operators should therefore check `is processing depth excessive for the question difficulty`, more than `did it read more and answer longer`.

| Question scene | Easy first judgment | What operations must check again |
| --- | --- | --- |
| Simple question such as password reset | More explanation is better | Does a short question trigger excessive retrieval and long answers? |
| Status-check question such as delivery tracking | Adding policy context is kind | Does the answer close quickly with the needed status value first? |
| Policy question with many exceptions | Reading many documents is safer | Is deeper processing selected only for complex questions? |

This table corrects the misunderstanding that `more processing = always better service`.

### Case 2. Development assistant tool

Suppose a development assistant performs file exploration, search, tests, and retries before editing code. This can raise the success rate of one fix. But as call stages increase, token cost and execution time increase too. If the tool repeats full tests even for one small variable-name change, users can feel that it is `accurate but too heavy`.

For example, running full integration tests every time for a single typo fix can increase safety while greatly reducing daily usability. If the whole team repeats this flow, infrastructure cost can grow quickly. The important question is not `does doing more make it better`, but `is the cost paid for quality improvement acceptable`. The result to check in this case is whether execution time and cost remain within daily-use range, not only whether fix success rate is high.

Development assistants often add more checks and retries `to reduce failure`. But if the same heavy procedure runs regardless of task size, the tool becomes safer but harder to use routinely. Renaming a variable and changing build configuration have different risk levels. If both go through the same full-test and multistep verification path, a team may soon feel `we should use this only for important work`.

| Edit scene | What looks better when more checks run | Cost to recheck in operations |
| --- | --- | --- |
| Variable rename or string typo fix | Mistake possibility decreases | Full tests for small work increase latency and cost. |
| Function signature change | Wider verification can improve safety | In this case, stronger checks may be justified. |
| Multi-file refactor | Retries and search can really improve quality | Call and retry limits need separate caps. |

The important standard is not `it is accurate, so it is good`, but `is the time and cost paid for accuracy proportional to task size`.

### Case 3. Internal document Q&A

Suppose internal document Q&A attaches as many related documents as possible to increase accuracy. In reality, this can increase cost and latency, and too many paragraphs can bury the key sentence, making the answer blurrier. For a refund-policy question, for example, attaching ten documents can make less important general guidance appear more prominently than the key exception clause.

In that case, the answer becomes longer while the one-line criterion the user needed appears later. More evidence does not always lead to a better answer. The criterion changes from first asking `how many documents were attached` to asking `how accurately was the evidence needed by the question selected`. The result to check is whether the key exception clause survives first in the answer, not how many documents were attached.

The three cases can be organized by operational constraints like this.

| Situation | Operational burden that grows while trying to improve performance | Criterion to adjust again |
| --- | --- | --- |
| Customer-support chatbot | Long retrieval and long answers increase latency | Processing depth by question difficulty, response time |
| Development assistant tool | Tests, retries, and tool calls increase cost | Check strength by task size, execution budget |
| Internal document Q&A | Too many documents increase cost and noise | Top-k, document-selection accuracy, answer length |

## Scenes that should be filtered again as operational candidates

A common misunderstanding when first reading operational constraints is thinking `it passed evaluation, so now it can be deployed`. But real service-candidate judgment must separate `good answer` from `continuously affordable answer` once more. Practical questions look like this.

| If you suspect this | First question to ask |
| --- | --- |
| `The answer is right, so why does it feel uncomfortable?` | Is response time inside actual user expectations? |
| `It is accurate, but too expensive.` | Can the same quality be achieved with fewer calls and a shorter path? |
| `It worked one by one, but collapses under simultaneous use.` | Can the current structure actually handle expected request volume? |
| `Many documents were attached, but the answer became blurrier.` | Can only the evidence needed by the question remain while the rest is reduced? |

If we immediately label `which operational constraint failed first`, the judgment becomes shorter.

| First judgment to leave on a design | Criterion for leaving that judgment |
| --- | --- |
| `latency needs adjustment` | Answer quality is fine, but it falls outside the time users can wait. |
| `cost needs adjustment` | Keeping the same quality requires too many calls, too large a model, or too much context. |
| `capacity needs adjustment` | One request works, but throughput and concurrency cannot handle traffic. |
| `processing depth needs adjustment` | Retrieval, tool calls, or long-answer stages are excessive for question difficulty. |
| `can remain as operational candidate` | Quality, latency, cost, and capacity are all inside current service limits. |

The key point is separating `this is a good answer` from `this is an operable design`. This connects naturally to the example's `primary_tradeoff` and `next_adjustment` values.

The standard to learn first is simple. Service operational constraints are not secondary conditions added after `quality is good`. They are a separate pass line that asks whether that quality can be provided repeatedly within cost, latency, and capacity.

## Practice and example

The goal of the example is to see quality and constraints together as actual selection results, and read `what should be reduced or changed first` for each design. Instead of comparing only two designs, we place several service designs under the same operational constraints and compare which pass and which fail. Along with quality, latency, and cost, we include `requests per minute the design can handle`, so we can see how a design can work as a demo but fail in operation.

The example uses service design candidates, the team's maximum allowed latency and cost, minimum quality line, and expected requests per minute. Some designs are fast and cheap but low quality. Some are high quality but slow or expensive. Some look good for a single request but cannot handle requests per minute.

The output shows whether each design is acceptable, why it was selected or rejected, the highest-quality candidate among designs that pass operational constraints, and what adjustment should be made next. The key point in the code is that service design must satisfy latency, cost, and throughput together with individual answer quality.

The operational-constraint criteria to read together are:

| Check item | Why it is needed |
| --- | --- |
| `quality_ok` | A design below the minimum quality line is hard to adopt even if fast and cheap. |
| `latency_ok` | The answer must arrive within the time users can wait. |
| `cost_ok` | Even if one request is good, operating beyond budget is hard to sustain. |
| `throughput_ok` | If it cannot survive repeated requests, it is a demo rather than a service. |
| Next adjustment | We need to know what to reduce or change first for a failed design. |

The example uses the service candidate CSV [p6_17_1_service_candidates.csv](/AiBook/assets/part-06/chapter-17/p6_17_1_service_candidates.csv){ .csv-preview }. One row is one service design. `quality_score` is answer quality, `avg_latency_ms` is average response time, `estimated_cost_per_1k_requests` is estimated cost per 1,000 requests, and `max_requests_per_minute` is the requests per minute the current structure can handle. These values are learning candidates, not real operational logs, but 36 candidates are compared together so we do not decide from only one or two numbers.

```python
--8<-- "assets/part-06/chapter-17/p6_17_1_evaluate_service_candidates_en.py"
```

The example output can be read like this.

```text
[constraints]
{'max_cost_per_1k_requests': 3.0,
 'max_latency_ms': 2000,
 'min_quality_score': 0.75,
 'required_requests_per_minute': 80}
[summary]
{'acceptable_count': 16,
 'best_operational_candidate': 'balanced_stable_support',
 'candidate_count': 36,
 'cost_fail_count': 9,
 'latency_fail_count': 12,
 'quality_fail_count': 5,
 'throughput_fail_count': 12}
[selected_cases]
{'avg_latency_ms': 900,
 'estimated_cost_per_1k_requests': 1.2,
 'failed_checks': [],
 'max_requests_per_minute': 130,
 'next_adjustment': 'keep_as_operational_candidate',
 'operationally_acceptable': True,
 'primary_tradeoff': 'operational_fit',
 'quality_score': 0.78,
 'service_name': 'fast_cached_faq'}
{'avg_latency_ms': 1700,
 'estimated_cost_per_1k_requests': 2.3,
 'failed_checks': [],
 'max_requests_per_minute': 95,
 'next_adjustment': 'keep_as_operational_candidate',
 'operationally_acceptable': True,
 'primary_tradeoff': 'operational_fit',
 'quality_score': 0.84,
 'service_name': 'balanced_support'}
{'avg_latency_ms': 3200,
 'estimated_cost_per_1k_requests': 4.8,
 'failed_checks': ['latency', 'cost', 'throughput'],
 'max_requests_per_minute': 42,
 'next_adjustment': 'reduce_steps_context_or_tool_calls',
 'operationally_acceptable': False,
 'primary_tradeoff': 'latency_too_high',
 'quality_score': 0.89,
 'service_name': 'rich_deep_rag'}
```

![service operational constraint pass by axis](/AiBook/assets/part-06/chapter-17/service-constraint-matrix-en.png)

The first thing to notice is the difference between `failed_checks` and `primary_tradeoff`. `failed_checks` shows all limits a candidate failed to pass, while `primary_tradeoff` narrows which axis to adjust first. The judgment order is not simply choosing the largest number. If the candidate does not pass the minimum quality line, it is first treated as a quality problem. If it passes quality but is blocked by operational limits, the bottleneck is narrowed in the order of latency, cost, and throughput because these connect directly to user experience and request-path reduction.

So `rich_deep_rag` fails latency, cost, and throughput together, but the first axis to adjust is latency. This candidate is close to a case where retrieval and generation paths became heavy to improve answer quality, so the next judgment is to first reduce search depth, generation length, or cache opportunities rather than discard the whole structure immediately. By contrast, `accurate_but_capped` can look better than `balanced_support` from single-request quality alone, but it fails as an operational candidate because of request-per-minute capacity. `cost_over_budget_support` passes quality, latency, and throughput but fails cost, and `capacity_shortfall_support` fails because it is just short of the required throughput. `next_adjustment` lets us read not only that it failed, but where to fix first.

The chart is not meant to make us memorize individual candidate names. It summarizes how 36 candidates are filtered by each constraint axis. Even when many candidates pass quality, latency, cost, or throughput separately, the final `operational candidate` count decreases once all four conditions are combined. The result to check is that a higher quality number can still lose when latency, cost, and throughput constraints are applied together, and a fast cheap design can also fail if it does not pass the minimum quality line.

Readers can try these adjustments in the example.

- Relax `max_latency_ms` and see whether high-quality designs pass.
- Raise `min_quality_score` and see when `balanced_support` also fails.
- Raise `required_requests_per_minute` and see when `balanced_support` is pushed out of the operational candidates.

In one line, service operational constraints are not `choosing a good model`; they are `choosing a design that can be maintained within constraints and deciding which weak axis to adjust first`.

In a real service stage, producing a `good-looking response` is not enough. We must also ask whether that response can be maintained `fast, affordable, and stable`. This section should therefore be read as a place for operational-constraint judgment, not a simple model-performance comparison.

This operational judgment matters because it:

- moves from P6-16.1 and P6-16.2's question of `is this a good answer` to whether that answer can actually be provided `fast, cheaply, and stably`
- shifts the viewpoint from model-centered thinking to service-operation thinking
- prepares failure handling and incident-management problems
- prepares Part 7 deployment and operations reflection to include constraint design, not only feature implementation

## Checklist

- You should be able to explain service operational constraints not as `is quality good`, but as `can this quality continue within cost, speed, and capacity`.
- You should be able to say that cost, latency, and usage limits are different constraints, and the same quality-improvement choice can shake all three.
- You should be able to continue into thinking about which recovery path should handle failures inside these limits.

## Sources and Further Reading

- OpenAI, [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Latency optimization](https://developers.openai.com/api/docs/guides/latency-optimization){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Cost optimization](https://developers.openai.com/api/docs/guides/cost-optimization){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
