# P1-14.1 Model, Application, Data, and Tool

> Section ID: `P1-14.1`
> Version: `v2026.07.26`

Chapter 13 covered embeddings, similarity search, RAG, and the intuition behind vector search implementation. That flow creates an important shift:

> from seeing only a single `LLM`  
> to seeing the `service structure` around the LLM

An AI service is not made from a model alone. It also needs an `application` the user interacts with, `data` the model can refer to, `tools` that connect to outside systems, and code or execution structure that coordinates the whole flow.

> an AI service is a system in which the model handles generation and judgment, the application shapes user experience and flow, data provides evidence and state, tools connect the service to outside action, and orchestration ties these parts together

What matters here is not implementation detail but a broad map.

Part 1 establishes the basic distinctions among `model`, `application`, `data`, `tool`, and `orchestration` here. Chapter 13 focused on how the model can refer to outside material through embeddings, retrieval, and RAG. This section widens the frame and asks:

> what combination of parts makes up an AI service as a whole?

This section separates the main components of an AI service. The specific positions of `RAG` and `tool use` are covered in P1-14.2. `Agents`, `MCP`, `harnesses`, and cost or operational constraints are covered in P1-14.3 and later.

`Model`, `application`, `data`, `tool`, and `orchestration` are different service components. Their roles can first be separated like this:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| model | a computational component that performs generation and judgment from input | the core computation element of the service |
| application | the surface and flow through which the user requests and receives results | the entry point of user experience |
| data | information that provides evidence and state | the material answers and actions depend on |
| tool | a connection method that calls external system functions | the execution side of lookup and action |
| orchestration | how these elements are connected in order and under conditions | the frame that shapes the service structure |

The baseline distinction here is simple: `the model computes`, `the application shapes experience`, `data provides evidence`, `tools execute`, and `orchestration connects the flow`.

| Topic | Question examined in this section |
| --- | --- |
| model | who is actually generating and judging? |
| application | where does the user make the request and see the result? |
| data | where do evidence and state come from? |
| tool | how are systems outside the model called? |
| orchestration | who connects these elements and in what order? |

## Separating Model, Application, Data, and Tool

- Understand an AI service as a combination of components rather than as a single model.
- Distinguish the roles of the `model`, `application`, `data`, and `tool`.
- Get the broad picture of where prompts, RAG, and tool calls sit in the service flow.
- Understand that the model does not do everything directly, and that service code wraps the model's inputs and outputs.
- Prepare to move into the distinction between RAG and tool use in P1-14.2.

## Three Standards

This section loosens the intuition that `AI service = model`. The following three perspectives are the main baseline.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| an AI service is not made from a model alone | This reduces the mistake of treating the chatbot experience as the whole system. | It is enough to understand that the application, data, and tools are also necessary. |
| the model, application, data, and tool each have different roles | This becomes the basic map for later discussions of RAG, agents, and MCP. | It is enough to distinguish generation, flow management, evidence, and external action. |
| service quality depends not only on model capability, but on the way the whole system is connected | This introduces the first architecture view. | It is enough to understand that permissions, retrieval, and post-processing matter too. |

## Model as Core Answer-Producing Component

A `model` is the core computation component in an AI service. It can read user input and output text, code, image descriptions, structured data, and other forms.

At first, the model can be simplified like this:

> input  
> -> model  
> -> output

But a real service wraps much more structure around that chain:

> user request  
> -> the application prepares input  
> -> retrieves needed data  
> -> calls the model  
> -> reviews or post-processes the result  
> -> shows it to the user

The model performs important generation and judgment, but it does not by itself handle account management, permission checks, data storage, external API calls, or screen rendering. Those jobs belong to the application and service code.

So if we read `AI service` as if it were just `the model itself`, we overlook the real flow.

| Misunderstanding | Safer explanation |
| --- | --- |
| the model handles everything in the service | the model is only the core computation component in the service |
| the model knows all the data | the model answers using the input context and learned representations it is given |
| the model directly executes actions | real actions are carried out by the application, server, and tool-calling code |

## Application Handles User Request and Result Flow

The `application` is the layer the user actually touches. A web page, mobile app, chat interface, IDE extension, or dashboard can all be applications.

The application does not only pass a question to the model. It usually also handles the following work:

| Role of the application | Description |
| --- | --- |
| input collection | receives the user's question, file, selected values, and settings |
| context construction | organizes user state, screen information, previous conversation, and selected documents |
| output display | shows the model's result in a readable way |
| error handling | reports failures, delays, or permission problems |
| review flow | lets the user edit, approve, or retry the result |

For example, imagine a writing-assistant application:

> user:  
> rewrite this paragraph so it is easier to understand
>
> application:  
> collects the current paragraph, document title, selected range, and desired tone, then sends them together
>
> model:  
> generates a revision candidate
>
> application:  
> shows the original and revised version side by side, and lets the user decide whether to accept it

The user may feel they are `talking directly to the model`, but the actual experience is usually being shaped by the application.

## Data Provides Evidence and State

In an AI service, `data` usually plays two major roles.

First, it provides the evidence needed for answers. Documents retrieved through RAG, internal knowledge bases, product manuals, and the book text itself all belong here.

Second, it provides the current state the service needs. User settings, permissions, task history, order status, and project metadata all belong to the information needed to process the current request.

| Type of data | Example |
| --- | --- |
| evidence data | documents, manuals, papers, FAQs, book sections |
| state data | user settings, permissions, session data, task progress |
| input data | uploaded files, questions, selected paragraphs |
| log data | request history, errors, evaluation results, feedback |

For an AI service, the key question is not simply `is there a lot of data?`, but rather: what data should be shown to the model, what data should be hidden, and what data must stay current?

> good data connection:  
> only necessary information is passed, permissions are respected, freshness is maintained, and sources can be traced
>
> bad data connection:  
> irrelevant information, stale information, unauthorized information, or source-less information is mixed in

This perspective connects directly to the RAG discussion from Chapter 13. RAG does not dump all data into the model. It first finds candidate passages relevant to the question, then places only those into the model's input context.

## Tools Execute Actions Outside the Model

A `tool` is the execution path that connects the service to systems outside the model. It lets functions outside the model participate in the same service flow.

At a first pass, it can be understood like this:

> model:  
> proposes what should be done, or generates the tool name and arguments
>
> tool-execution code:  
> actually performs the API call, retrieval, file processing, or database lookup

Suppose a user asks:

> From last week's meeting notes, extract only the decisions and add them to the schedule note.

This kind of request may not be solvable by the model alone.

| Work that must be done | Main responsible element |
| --- | --- |
| find the meeting notes | a search tool or file retrieval |
| extract the decisions | model |
| convert them into schedule format | model or application code |
| write them into the calendar or notes system | calendar or note API tool |
| confirm the result | application |

Tool use is powerful, but it also introduces risk. A tool may be called incorrectly, access unauthorized data, or execute an action the user never approved. That is why tool use is examined more directly in P1-14.2.

## Orchestration Connects the Flow

Even if the model, application, data, and tools all exist, they do not automatically become a good service. Someone still has to decide in what order these elements are connected.

That role can be described as `orchestration`.

> receive the user request  
> -> check permissions  
> -> retrieve needed data  
> -> compose the prompt  
> -> call the model  
> -> decide whether tools are needed  
> -> post-process the result  
> -> show it to the user  
> -> save logs and feedback

Different services emphasize different parts of that flow.

| Service | More important flow parts |
| --- | --- |
| document-retrieval chatbot | retrieval, source display, answer review |
| coding assistant | file reading, patch generation, test execution |
| customer-support bot | reading customer state, checking policy, handing off to a human when needed |
| work-automation application | approval, external API calls, execution logs |

The key point is that the model does not automatically own the whole flow. The model performs generation and judgment inside the flow, while the application and server code decide when to call the model, what data to provide, what tools to allow, and how to review the result.

## Seeing the Four Components Together

If we simplify an AI service further, we get a structure like this:

```mermaid
--8<-- "assets/part-01/chapter-14/ai-service-components-flow-en.mmd"
```

This diagram does not show every detail of a real system, but it is enough to connect the roles of the components at a glance.

## Checklist

- You can explain an AI service not as one `model`, but as a combination of application, data, tools, and flow.
- You can explain that the application can handle user input, context construction, output display, and error handling.
- You can distinguish data into evidence data, state data, input data, and log data.
- You can explain a tool as the connection path that executes systems outside the model.
- You can explain that the model does not directly execute every action, and that the application and server code wrap the execution flow.
- You can distinguish that RAG is one way of connecting data to the model, while tool use is the way of connecting outside actions.
- You can separate `model`, `application`, `data`, `tool`, and `flow control` so the chatbot experience is not mistaken for the whole service structure.

## Sources and Further Reading

- OpenAI, [Text generation](https://developers.openai.com/api/docs/guides/text){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- NIST, [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf){: target="_blank" rel="noopener noreferrer" }, 2023, accessed 2026-06-23.
