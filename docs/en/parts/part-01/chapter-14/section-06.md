# P1-14.6 The Constraints AI Services Meet in the Real World

> Section ID: `P1-14.6`
> Version: `v2026.07.09`

P1-14.5 described a `harness` as an execution environment that wraps model and tool runs and makes tracing, logging, and evaluation possible. The next question moves in a more practical direction:

> the model can produce an answer  
> tools can be connected  
> the execution can be recorded
>
> then can this structure keep running as a real service?

An AI service is not completed by good answers alone. If it is too expensive, it cannot be sustained. If it is too slow, users will not wait. If failure cannot be explained or recovered from, it is hard to put the service into real work.

This section looks at that problem through the lens of `service constraints`: `cost`, `latency`, `throughput`, `usage limit`, `rate limit`, `retry`, `batch`, `caching`, and `monitoring`.

## Scope of This Section

This section explains, at an introductory level, the constraints that matter when an AI service is actually used. It does not go deeply into a particular provider's pricing table, specific model recommendations, deployment infrastructure design, or cloud cost calculation. Security and privacy return in Part 1 Chapter 15.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| cost | resource consumption per request and across operation | the standard for judging sustainability |
| latency | the time from request to response | the core of user waiting experience |
| throughput | how many requests can be handled in a period of time | the standard for judging service scale |
| rate limit | call limits within a short time window | both a design condition and a source of failure |
| retry | the policy of trying again after a failure | a means of restoring stability |
| batch | a way to process work later in groups | an efficiency path for non-real-time work |
| caching | reusing part of a result for repeated inputs | a way to reduce cost and latency |
| operations | the repeated work of maintaining and tuning the service | the viewpoint of observation and adjustment |

The baseline distinction here is:

- quality alone is not enough
- cost and latency have to be considered together
- failure and limits are part of design, not just accidents

## Goal of This Section

- Understand service constraints by dividing them into cost, latency, throughput, and failure response.
- Understand cost as more than token count alone, including model choice, request count, tool use, retries, and evaluation runs.
- Understand latency as more than model execution time alone, including retrieval, tool calls, networking, and post-processing.
- Treat rate limits, usage limits, and retries as basic service-design constraints.
- Understand batch, caching, and streaming as contextual choices rather than universal fixes.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| good answers alone do not complete a service | This separates model quality from operational viability. | It is enough to understand that cost and latency matter alongside quality. |
| cost is created across the whole flow, not only by one model call | This makes RAG, tool use, and retries visible as service cost. | It is enough to understand that retrieval, evaluation, and failed retries also consume resources. |
| latency and failure response are part of design | This keeps user experience and operational stability in the same frame. | It is enough to understand that a good model is still hard to use if it is slow or fails often. |

## Good Answers Alone Are Not Enough

At first, people often focus on whether the model gives a good answer. But once the system becomes a service, the questions change.

| Question in the learning stage | Question in the service stage |
| --- | --- |
| is the answer correct? | can the same quality be produced repeatedly? |
| is the explanation natural? | does it respond within the time a user can wait? |
| should we just use a smarter model? | are cost and latency within the acceptable range? |
| does adding more tools help? | can tool failures and permission problems be handled? |
| is it enough to keep logs and evaluations? | can the cost and risk created by logging and evaluation themselves be handled? |

An AI service has to consider three things together:

> quality  
> cost  
> latency and reliability

## Cost Is Not Only a Token Problem

In LLM services, `tokens` are an important unit for understanding cost. Longer input and longer output usually require more computation, so they often increase both cost and latency.

But cost cannot be reduced to tokens alone.

| Cost driver | Description |
| --- | --- |
| model choice | a larger model may produce better results but can increase both cost and latency |
| input tokens | long prompts, long documents, and many retrieval results raise cost |
| output tokens | long answers, long code, and long reports raise cost |
| request count | multiple model calls inside one request accumulate cost |
| tool call | retrieval, database access, and external API calls can create separate cost and time |
| retry | repeating a failed request may increase cost regardless of whether it succeeds |
| eval run | repeated quality checks also consume resources |

## Latency Is Not Only the Model's Time

`Latency` is the time the user waits between sending a request and receiving a response. In an AI service, that time is not determined by model inference alone.

> user request  
> -> input validation  
> -> retrieval or data lookup  
> -> model call  
> -> tool call  
> -> another model call  
> -> post-processing  
> -> user response

Each stage may add delay.

| Latency source | Example |
| --- | --- |
| network | request and response travel time |
| retrieval | vector search, database lookup, document loading |
| model inference | time spent processing input and generating output |
| output length | long answers may take longer to generate |
| tool call | external APIs or file operations may be slow |
| post-processing | format validation, safety checks, or storage |

`Streaming` can reduce perceived wait time because the user can start seeing output before the entire answer is complete. But streaming does not eliminate all computation. The full completion time is still shaped by the model, tools, network, and post-processing.

`Prompt caching` can also help reduce both latency and cost when long repeated prefixes appear, such as a stable system instruction or shared context.

## Limits Are Not Just Failures, They Are Design Conditions

Service providers often impose both `usage limits` and `rate limits`.

`Rate limits` are restrictions on how many requests or tokens can be handled in a certain time window. `Usage limits` may be broader limits, such as monthly or project-level caps.

These are not just inconveniences. They are design conditions.

| Limit | Design question it raises |
| --- | --- |
| request limit | what happens when many users arrive at once? |
| token limit | how should long documents and long outputs be reduced? |
| usage limit | how should the service stop before the budget is exceeded? |
| model-specific limit | is there a fallback path if one model becomes unavailable? |
| batch limit | how should non-real-time work be separated out? |

That is why `retry` needs a policy. A common approach is `exponential backoff` with `jitter`:

> bad retry:  
> fail -> retry immediately -> retry immediately -> retry immediately
>
> better retry:  
> fail -> wait briefly -> retry -> wait longer -> retry -> stop or inform the user

## Real-Time Work and Batch Work Are Different

Not every AI task needs an immediate answer. A task where the user is waiting in a conversation window is close to `interactive` work. A task such as large-scale document classification, embedding creation, evaluation runs, or data enrichment is often better treated as `batch` work.

| Work type | Characteristic | Example |
| --- | --- | --- |
| interactive work | the user waits now | chatbot replies, coding assistance, search queries |
| batch work | the result can arrive later | bulk document classification, embedding generation, evaluation runs |

One simple question can change the service structure:

> does the user need this answer now?  
> or can this be processed later?

## Operations Are the Conditions for Repeated Use

Here, `operations` does not mean the entire methodology of DevOps or MLOps. It means the narrower question:

> under what conditions can this AI service be used repeatedly and maintained?

At a minimum, operations should watch:

| What to observe | Why |
| --- | --- |
| error rate | to see which requests fail often |
| latency | to see whether user wait time is growing |
| cost | to see whether the budget is being exceeded or a feature is too expensive |
| token usage | to see whether inputs or outputs are becoming unnecessarily long |
| tool failure | to see whether outside APIs, files, or databases are causing trouble |
| quality metric | to see whether quality has dropped after a model or prompt change |

The key lesson is simple:

> after execution begins, the service still has to be observed and adjusted

## Standards to Decide Early Even in a Small Service

It is not necessary to build a huge operating system from the start. Even a small AI feature is more stable if some standards are defined early.

| Standard | Example question |
| --- | --- |
| response-time target | how many seconds can the user wait? |
| maximum output length | how long should the answer be allowed to become? |
| maximum tool-call count | how many tool calls can one request make? |
| retry policy | how many times should it try again, and when should it stop? |
| budget standard | how will daily or monthly usage be watched? |
| failure notice | what should the user be told when execution fails? |
| evaluation standard | what cases will be used to check quality after changes? |

For a document-based Q&A feature, a first draft of standards might look like:

> start the response within five seconds if possible  
> include at most five retrieved documents  
> limit the first answer to about 800 characters  
> allow at most three tool calls in one request  
> retry a rate-limit error at most twice  
> if no source exists, do not answer as if the claim were verified

These are not universal correct values. They depend on the service's purpose, users, budget, and risk.

## The Full Flow One Request Actually Goes Through

The elements introduced in Chapter 14 become intertwined inside one real request. In a document-based work assistant, the user may ask one question, but many steps can happen underneath.

> user question  
> -> permission check  
> -> retrieve related documents  
> -> compose the prompt  
> -> model call  
> -> call a tool if needed  
> -> review and record the result  
> -> respond to the user

If the user asks:

> find only the decisions from last week's meeting notes,  
> draft a schedule,  
> and add the needed items to the calendar

the internal steps can be read like this:

| Stage | Internal work | Important constraint there |
| --- | --- | --- |
| permission check | confirm that the user may access the meeting notes and calendar | security, privacy, and approval conditions |
| retrieval | find the meeting-note file and related passages | retrieval latency and risk of selecting the wrong document |
| first model call | extract decisions and candidate schedule items | model cost, output length, interpretation error |
| tool call | register a draft event through the calendar API | permission, retry policy, outside state change |
| review and record | preserve what documents were used and what was registered | logging cost, reproducibility, auditability |
| user response | show the result together with its basis | response time and explainability |

The key point of this integrated example is that:

> one good model does not automatically become an operable service

Real service structure moves `reading`, `judging`, `executing`, `reviewing`, `recording`, and `constraint management` together inside one request.

## The View to Keep from This Section

An AI service is not sustained by model quality alone.

> good answers are necessary  
> but good answers alone are not enough
>
> cost determines sustainability  
> latency shapes user experience  
> limits and failure response shape stability  
> observation and evaluation shape the ability to improve

Especially once agents and tool use are involved, the number of calls and failure points increases. That is why quality and constraints must be read together.

## Checklist

- You can explain service constraints through cost, latency, throughput, and failure response.
- You can explain that cost is connected not only to tokens but also to model choice, request count, tool calls, retries, and evaluation runs.
- You can explain that latency includes retrieval, tool calls, networking, and post-processing in addition to model execution.
- You can explain streaming, caching, and batch as situational choices.
- You can explain rate limits and usage limits as design conditions rather than mere failures.
- You can explain why retries need a policy such as exponential backoff with jitter.
- You can explain operations as the conditions for observation and adjustment in repeated use.
- You can explain why even a small AI feature needs standards for response time, tool calls, retries, budget, and failure handling.

## When to Recall This View First

- When better answer quality is being treated as if it automatically made a service usable
- When cost, latency, retries, and limits need to be read as design conditions rather than as afterthoughts
- When even a small feature needs explicit standards for response time, tool-call count, and budget

In those cases, separate `quality`, `cost`, and `latency and reliability` first.

## Sources and Further Reading

- OpenAI, [Latency optimization](https://developers.openai.com/api/docs/guides/latency-optimization){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-06-23.
- OpenAI, [Cost optimization](https://developers.openai.com/api/docs/guides/cost-optimization){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-06-23.
- OpenAI, [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-06-23.
- OpenAI, [Batch API](https://developers.openai.com/api/docs/guides/batch){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-06-23.
- OpenAI, [Rate limits](https://developers.openai.com/api/docs/guides/rate-limits){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-06-23.
- OpenAI, [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-06-23.
- OpenAI, [Deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-06-23.
