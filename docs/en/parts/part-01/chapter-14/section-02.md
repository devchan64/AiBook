# P1-14.2 Where RAG and Tool Use Sit

> Section ID: `P1-14.2`
> Version: `v2026.07.07`

P1-14.1 described an AI service as a combination of the `model`, `application`, `data`, `tool`, and `orchestration`. This section separates two parts that are easy to confuse.

> `RAG`:  
> find outside material and attach it to the model's input context
>
> `tool use`:  
> call a system outside the model to read something or perform an action

Both seem similar because they involve something outside the model. Their roles are still different.

> RAG is a structure for bringing in material needed for an answer, while tool use is a structure for calling external system functions

Part 1 establishes the basic distinction among `RAG`, `tool use`, `retrieval`, `tool call`, and `approval` here. Section 13.3 already introduced RAG as a structure that attaches retrieved results to generation input. Section 14.1 widened the view to the whole service. This section connects those two flows and asks:

> how are RAG and tool use positioned differently inside an AI service?

## Scope of This Section

This section compares the positions of RAG and tool use. The more detailed structure of an `agent` is covered in P1-14.3. MCP is covered in P1-14.4. Harnesses, evaluation, and execution logs are covered in P1-14.5.

`RAG`, `tool use`, `retrieval`, `tool call`, and `approval` belong to different reading, execution, and control steps.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| RAG | a structure that finds outside material and attaches it to input context | the representative structure for connecting evidence |
| tool use | a structure that calls external system functions | the execution path for real lookup and action |
| retrieval | the step of finding relevant material or targets | the starting point of RAG |
| tool call | the step of executing an outside function with a name and arguments | the key action in tool use |
| approval | a process in which a person or policy checks whether execution is allowed | a safety device before risky action |

The baseline distinction here is:

- RAG is for reading
- tool use is for execution
- approval is for review before action

## Goal of This Section

- Understand `RAG` as a structure for reading outside material.
- Understand `tool use` as a structure for calling the functions of an outside system.
- Distinguish that both use resources outside the model, but with different purposes and risks.
- Understand that the two structures can be combined.
- Organize the roles of these basic components before moving on to agents.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| RAG is a structure that finds material and attaches it to context | This clarifies what retrieval plus generation means. | It is enough to understand it as a way to read documents and attach them as evidence. |
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

In RAG, outside material is being `read into` the model's context. It is not directly editing a document, sending email, or making a payment.

## Tool Use Calls an External System

`Tool use` allows the model to use the functions of an outside system.

> model:  
> proposes the needed tool and arguments
>
> application or server:  
> reviews the tool call and executes it
>
> tool:  
> performs work such as retrieval, calculation, file processing, or API calls

If a user asks, "Check tomorrow's weather in Seoul and add it to my schedule note," the request may involve:

| Work | Possible method |
| --- | --- |
| check the weather | weather API tool call |
| add a schedule note | calendar or memo API tool call |
| explain the result | model-generated natural language |

Tool use can read or change the state of an external system. That makes its execution responsibility heavier than RAG.

## RAG and Tool Use Have Different Purposes

The contrast becomes clearer when the two are placed side by side.

| Distinction | RAG | tool use |
| --- | --- | --- |
| main purpose | find material needed for an answer | execute an external function |
| main target | documents, knowledge bases, search indexes | APIs, databases, file systems, business systems |
| relation to model input | retrieved results go into prompt context | tool results are returned to the model or application |
| representative question | what should the model refer to? | what should the system execute? |
| main risk | wrong, stale, or irrelevant material | wrong execution, permission problems, or external state change |

The same source material can still lead to different structures.

> explain the decisions from the meeting notes  
> -> mainly RAG or file retrieval
>
> find the decisions from the meeting notes and register them in the calendar  
> -> RAG plus tool use

## The Two Can Be Combined

Real AI services often use RAG and tool use together.

For example:

> 1. use RAG to retrieve the travel-expense policy  
> 2. let the model compare the policy with a receipt  
> 3. ask the user if some required field is missing  
> 4. if the action is allowed, call the expense-processing API  
> 5. show the result together with the supporting material

In that flow, RAG and tool use have clearly different roles.

| Step | Structure | Role |
| --- | --- | --- |
| policy retrieval | RAG | finds the basis for judgment |
| receipt interpretation | model | reads and organizes the input material |
| expense submission | tool use | executes the external business system |
| result display | application | shows the result and the basis to the user |

## Tool Use Requires Permission and Approval Flow

Because tool use can call external systems, `permission` and `approval` matter.

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

## The Model Proposes the Call, the System Executes It

One boundary is especially important in tool use:

> the model does not directly change the outside world  
> the application and server execute the tool call

The model may generate something like:

> tool name: `calendar.create_event`  
> arguments: date, time, title, participants

But the actual calendar API call is still made by application or server code. That code must check permissions, validate arguments, and request user approval when needed.

| Component | Responsibility |
| --- | --- |
| model | generates candidates for the tool and arguments |
| application/server | checks permissions, validates inputs, decides whether to execute |
| tool | reads from or acts on the external system |
| user | approves or edits when necessary |

## The View to Keep from This Section

RAG and tool use both involve something outside the model, but they are not the same thing.

> RAG reads outside material into the model's context  
> tool use executes outside functions  
> the two can be combined in one service flow  
> reading and acting have different risks and different review responsibility

This distinction makes it easier to move into the next section, where several such steps are tied together into an `agent` workflow.

## Short Check

- You can explain RAG as a structure for retrieving outside material and attaching it to context.
- You can explain tool use as a structure for calling external system functions.
- You can distinguish reading evidence from executing action.
- You can explain that RAG and tool use can be combined in a single service flow.
- You can explain why tool use requires permission, approval, and validation flow.

## When to Recall This View First

- When RAG and tool use are being used as if they meant the same thing
- When you need to explain why reading a document and changing an external system are different
- When an AI service needs both evidence retrieval and outside execution

In those situations, separate `reading` from `execution` first. That prevents the two structures from being collapsed into one vague idea of "using something outside the model."
