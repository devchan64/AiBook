# P1-14.2 The Place of RAG and Tool Use

> Section ID: `P1-14.2`
> Version: `v2026.07.23`

P1-14.1 described an AI service as a combination of the `model`, `application`, `data`, `tool`, and `orchestration`. This section separates two parts that are easy to confuse.

> `RAG`:  
> find outside material and attach it to the model's input context
>
> `tool use`:  
> call a system outside the model to read something or perform an action

Both seem similar because they involve something outside the model. Their roles are still different.

> RAG is a structure for bringing in material needed for an answer, while tool use is a structure for calling external system functions.

This section compares the two structures and explains where each sits inside an AI service.

Part 1 establishes the basic distinction among `RAG`, `tool use`, `retrieval`, `tool call`, and `approval` here. Section 13.3 first introduced RAG as a structure that attaches retrieved results to generation input, and 14.1 widened the frame to the whole service. This section connects the two and asks:

> how are RAG and tool use positioned differently inside a service?

The three words most often mixed between Chapters 13 and 14 can be fixed first like this:

| Distinction | One-sentence baseline | Closest role |
| --- | --- | --- |
| RAG | finds outside documents and attaches them to the model context | reading and evidence reinforcement |
| tool use | calls external system functions to query or act | execution and outside connection |
| agent | ties RAG and tool use into multiple steps toward a goal | workflow and state management |

The key point of this summary box is: `RAG`, `tool use`, and `agent` can work together, but they are not the same thing. This section first separates `reading` from `execution`, and the structure that carries multiple steps as an `agent` continues in P1-14.3.

This section compares the positions of RAG and tool use. The more detailed structure of an `agent` is covered in P1-14.3. MCP is covered in P1-14.4. Harnesses, evaluation, and execution logs are covered in P1-14.5.

`RAG`, `tool use`, `retrieval`, `tool call`, and `approval` belong to different reading, execution, and control steps.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| RAG | a structure that finds outside material and attaches it to input context | the representative structure for connecting evidence |
| tool use | a structure that calls external system functions | the execution path for real lookup and action |
| retrieval | the step of finding relevant material or targets | the starting point of RAG |
| tool call | the step of executing an outside function with a name and arguments | the key action in tool use |
| approval | a process in which a person or policy checks whether execution is allowed | a safety device before risky action |

The baseline distinction here is simple: `RAG is for reading`, `tool use is for execution`, and `approval is for review before action`.

| Topic | Question examined in this section |
| --- | --- |
| RAG | why search outside material and place it into input context? |
| tool use | why call an outside system? |
| difference | how is reading material different from executing an action? |
| combination | can RAG and tool use be used together? |
| responsibility | who reviews retrieval results and tool execution results? |

## Where RAG and Tool Use Sit in the System

- Understand `RAG` as a structure for reading outside material.
- Understand `tool use` as a structure for calling the functions of an outside system.
- Distinguish that both use resources outside the model, but with different purposes and risks.
- Understand that the two structures can be combined.
- Organize the roles of these basic components before moving on to agents.

## Three Standards

These two structures are often mixed together simply because both `use something outside the model`. The following three perspectives are the reading baseline.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| RAG is a structure that finds material and attaches it to context | This clarifies what retrieval plus generation means. | It is enough to understand it as reading documents and attaching them as evidence. |
| tool use is a structure that actually calls an external function | This separates referencing material from executing action. | It is enough to understand it as calling things like search APIs, calculators, databases, or file tools. |
| the two can be used together, but their roles and risks differ | This sets the boundary needed before discussing agents. | It is enough to understand that reading and acting are different and require different review responsibility. |

## RAG Finds Material and Attaches It to Context

As Section 13.3 explained, RAG connects `retrieval` and `generation`.

> user question  
> -> retrieve relevant documents  
> -> add the retrieved passages to the input context  
> -> let the model generate an answer

The central question of RAG is:

> where should the model get the material it needs to refer to?

Suppose a user asks:

> In this document set, was embedding explained as if it were meaning itself?

RAG can search the document collection and retrieve the relevant passages.

| Step | Role |
| --- | --- |
| question embedding | turn the question into a vector |
| similarity search | find candidate document passages |
| context augmentation | place the retrieved passages into the prompt |
| answer generation | let the model answer using the retrieved material |

In RAG, outside material is being `read into` the model's context. It is not directly editing a document, sending email, or making a payment.

## Tool Use Calls an External System

`Tool use` allows the model to use the functions of an outside system. OpenAI’s function-calling documentation also explains that models can be connected to outside data and systems in this way.

At a first pass, it can be understood like this:

> model:  
> proposes the needed tool and arguments
>
> application or server:  
> reviews the tool call and executes it
>
> tool:  
> performs work such as retrieval, calculation, file processing, or API calls

Suppose a user asks:

> Check tomorrow's weather in Seoul and add it to my schedule note.

Two different kinds of outside work may appear in one request:

| Work | Possible method |
| --- | --- |
| check the weather | weather API tool call |
| add a schedule note | calendar or memo API tool call |
| explain the result | model-generated natural language |

Tool use can read from or change the state of an external system. That makes its execution responsibility heavier than RAG.

> RAG:  
> brings material into the input
>
> tool use:  
> calls an outside system to query or act

## RAG and Tool Use Have Different Purposes

The contrast becomes clearer when the two are placed side by side.

| Distinction | RAG | tool use |
| --- | --- | --- |
| main purpose | find material needed for an answer | execute an external function |
| main target | documents, knowledge bases, search indexes | APIs, databases, file systems, business systems |
| relation to model input | retrieved results go into prompt context | tool results are returned to the model or application |
| representative question | what should the model refer to? | what should the system execute? |
| main risk | wrong, stale, or irrelevant material | wrong execution, permission problems, or external state change |

Even the same source, such as `meeting notes`, can lead to different structures.

> explain the decisions from the meeting notes  
> -> mainly RAG or file retrieval
>
> find the decisions from the meeting notes and register them in the calendar  
> -> RAG plus tool use

The first request mainly needs retrieval and summarization. The second request must also execute an action in an outside system after the material is found.

## The Two Can Be Combined

Real AI services often use RAG and tool use together.

For example, imagine a work assistant that uses internal company documents:

> user:  
> process this receipt according to the travel-expense policy

A possible flow is:

> 1. use RAG to retrieve the travel-expense policy  
> 2. let the model compare the policy with the receipt  
> 3. if some required field is missing, ask the user a follow-up question  
> 4. if the action is allowed, call the expense-processing API  
> 5. show the result together with the supporting policy text

In this flow, RAG and tool use have different roles.

| Step | Structure | Role |
| --- | --- | --- |
| retrieve the policy | RAG | finds the basis for judgment |
| interpret the receipt | model | reads and organizes the input material |
| submit the expense | tool use | executes the outside business system |
| show the result | application | displays the result and the basis |

This kind of combination can later develop into an `agent` structure. But this section does not yet go into the agent explanation that ties multiple steps together automatically.

## Tool Use Requires Permission and Approval Flow

Because tool use can call outside systems, `permission` and `approval` matter.

If RAG retrieves the wrong document, answer quality may drop. If tool use goes wrong, the state of an outside system may change.

| Situation | Risk |
| --- | --- |
| wrong email sent | false information reaches real recipients |
| mistaken payment | money may be lost |
| unauthorized document access | personal or confidential information may leak |
| wrong file modification | work output may be damaged |
| duplicate API call | the same action may run multiple times |

That is why tool use should always raise questions such as:

> is this user allowed to call this tool?  
> what external state will this tool change?  
> is user approval required before execution?  
> if execution fails, how will it be rolled back or recorded?  
> how will the result be reviewed?

This is also connected to security, privacy, and operation. But the longer discussions of ethics, copyright, and security are left for P1-15.

## The Model Proposes the Call, the System Executes It

One boundary is especially important in tool use:

> the model does not directly change the outside world  
> the application and server execute the tool call

The model may generate information such as:

> tool name:  
> `calendar.create_event`
>
> arguments:  
> date, time, title, participants

But the actual calendar API call is still made by application or server code. That code must check permissions, validate arguments, and ask for user approval when required.

This distinction makes responsibility clearer.

| Component | Responsibility |
| --- | --- |
| model | generates candidates for the tool and arguments |
| application/server | checks permissions, validates inputs, decides whether to execute |
| tool | reads from or acts on the external system |
| user | approves or edits when necessary |

This perspective is also important when reading agent-style tools such as Codex. Even if the model proposes work, actual file editing, command execution, commits, and deployment still happen inside an execution environment and permission policy.

## A Small Example of the Positional Difference

Take the example of checking and updating a long learning document.

> request:  
> verify the evidence for the vector-search explanation and strengthen the related paragraph

A possible flow is:

| Step | Structure | Description |
| --- | --- | --- |
| read the current document | tool use | read the current section from the file system |
| find supporting material | search or RAG | find candidate papers and documents |
| review the evidence | model plus person | judge whether the material really supports the claim |
| modify the document | tool use | patch the file |
| verify the build | tool use | run the MkDocs build |
| report the result | application or chat UI | show the change and the verification result |

In this flow, RAG is closest to `finding supporting material and strengthening the answer context`, while tool use is the part that actually touches the outside environment through file reading, patching, building, and committing.

## Checklist

- You can explain RAG as a structure that retrieves outside material and attaches it to input context.
- You can explain tool use as a structure that calls the functions of an outside system.
- You can distinguish the difference as `reading material` versus `executing action`.
- You can explain with an example that RAG and tool use may be used together.
- You can explain that tool use requires permission, approval, validation, and execution logs.
- You can explain that the model may propose a tool call, but the actual execution is handled by the application or server.
- You can keep `reading material`, `executing an outside function`, and `approval before action` separate when comparing RAG and tool use.

## Sources and Further Reading

- Patrick Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Text generation](https://developers.openai.com/api/docs/guides/text){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
