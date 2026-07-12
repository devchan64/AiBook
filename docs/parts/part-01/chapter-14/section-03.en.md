# P1-14.3 Agent: A Structure That Carries a Goal Through a Workflow

> Section ID: `P1-14.3`
> Version: `v2026.07.12`

P1-14.2 distinguished `RAG` from `tool use`.

> RAG:  
> finds needed material and attaches it to the model's input context
>
> tool use:  
> calls external system functions to retrieve information or execute an action

An `agent` may include both of those, but it is not the same term. Once the word `agent` appears, the focus shifts from `one answer` to a longer flow.

> an agent is an execution structure that takes a `goal`, checks the current `state`, chooses the next `action`, reflects the `observation` from tool execution, and decides whether to continue or stop

This section treats an agent not as exaggerated autonomy but as a structure that carries multi-step work inside an AI service.

## Scope of This Section

This section explains an `agent` as a structure that carries a goal through a workflow. The standardization of tool connections through `MCP` is covered in P1-14.4. Harnesses, execution logs, evaluation, and reproducibility are covered in P1-14.5. Cost, latency, and operations are covered in P1-14.6.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| agent | an execution structure that carries a goal through multiple steps | the central idea of this section |
| goal | the task to be solved | the starting point of the loop |
| state | what has been read and executed so far | the material for deciding the next step |
| action | the next task to perform | a real step such as retrieval, editing, or calling a tool |
| observation | the result obtained after an action | the basis for updating state |
| stop condition | the rule that decides when to stop and report | protection against endless loops or over-execution |

The baseline distinction here is:

- the agent follows a goal
- it chooses actions by looking at state
- it updates state from observations
- it stops under a defined condition

| Topic | Question in this section |
| --- | --- |
| goal | what part of the request should be interpreted as the working goal? |
| state | what is already known, and what has already been done? |
| action | what tool should be used next, or what response should be produced next? |
| observation | how should tool results be reflected back into the flow? |
| stop condition | when should the task stop and the result be reported? |

## Goal of This Section

- Understand an `agent` as an execution structure rather than as just a smarter chatbot or another model name.
- Distinguish prompts, RAG, tool use, and agents.
- Understand that agents can carry multi-step work, but that does not mean unlimited autonomy.
- Understand that the application, server, and runtime still manage permissions, approvals, and state.
- Prepare to interpret coding-agent tools such as Codex in service-architecture terms.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| an agent is a structure that carries a goal through multiple steps | This separates agents from one-shot chat responses. | It is enough to understand the flow as goal, state, action, observation, and stop condition. |
| prompts, RAG, and tool use can become parts inside an agent | This places the related concepts on one map. | It is enough to understand that an agent can combine them. |
| an agent still has to operate inside permissions and approval flow | This creates a safer service-level understanding. | It is enough to understand that the app and server manage scope and approval. |

## An Agent Handles a Longer Flow Than a Single Answer

A simple model call can be described like this:

> input  
> -> model  
> -> output

A prompt adds instructions, context, and examples to that input. RAG attaches retrieved outside material. Tool use calls an outside system when needed.

An agent does not use these only once. It continues connecting them until the task reaches a stopping point.

> requested goal  
> -> check current state  
> -> choose the next step  
> -> execute a tool or generate a response  
> -> observe the result  
> -> update state  
> -> decide whether to continue or stop

Suppose a user asks for something like this:

> write one section of a technical document, leave a review record, and confirm that the result is reflected correctly in the final artifact

That request does not end with one generated paragraph.

| Stage | Possible action |
| --- | --- |
| understand the goal | confirm the section's central question and document boundary |
| inspect the state | read the table of contents, the related earlier sections, and existing review records |
| gather evidence | check official documents and papers related to agents |
| write | draft the section text and supporting notes |
| verify | run a build or review procedure to confirm the result is reflected correctly |
| report | tell the user what files changed and what was verified |

## The Agent Loop: Goal, State, Action, Observation

The `loop` view is useful for understanding agents.

```mermaid
--8<-- "assets/part-01/chapter-14/agent-loop-flow-en.mmd"
```

| Element | Description |
| --- | --- |
| goal | what the user wants solved |
| state | the conversation so far, files read, execution results, and intermediate judgment |
| choose next step | decide what to do next and what tool is needed |
| action | retrieval, file reading, code editing, API call, answer writing |
| observation | tool results, errors, retrieved material, test results |
| stop condition | decide whether the task is solved or more approval or information is needed |

The ReAct paper is a useful reference point here because it studies a flow in which a language model alternates between reasoning and acting while gathering information from an outside environment. The main point for this book is not the exact method but the structure:

> think  
> -> act  
> -> observe  
> -> continue or stop

## RAG and Tool Use Can Become Building Blocks of an Agent

An agent is not a replacement word for RAG or tool use. Instead, those can be placed inside an agent workflow.

| Component | Role inside the agent flow |
| --- | --- |
| prompt | conveys goals, instructions, constraints, and output format |
| RAG | finds supporting material and inserts it into context |
| tool use | performs outside retrieval, calculation, file handling, or API execution |
| state | preserves intermediate results and execution history |
| orchestration | decides the order of execution |

For example, a request such as processing a receipt under a travel-expense policy can unfold like this:

> 1. retrieve the policy document  
> 2. read the receipt  
> 3. compare the policy with the receipt  
> 4. ask about missing fields  
> 5. after approval, register the item in the expense system  
> 6. report the basis and the result

That whole flow is closer to an agent structure than to a single model call.

## Agent Does Not Mean Unlimited Autonomy

The word `agent` can easily be misunderstood, as if the model sets its own goals, uses every tool freely, and changes the outside world at will. That is a dangerous reading.

A safer explanation is:

> an agent is a structure that carries a goal through multiple steps  
> but permissions, approvals, execution scope, and stop conditions still have to be managed by the application and server

That is why service design still needs:

| Needed control | Why |
| --- | --- |
| permission | to limit what data and tools the user may access |
| approval | to require human review before risky actions such as email, payment, or deployment |
| validation | to check tool arguments and execution results |
| stop condition | to prevent endless or incorrect loops |
| log | to preserve a record of what was executed |

## A Coding Agent Like Codex Is a Useful Example

A coding agent such as Codex is a good example for understanding the structure. If someone asks it to write a section and check the build, it is not enough to generate prose once.

| Work | Agent view |
| --- | --- |
| read files | checks the current state |
| inspect supporting material | observes the surrounding context and evidence |
| write a patch | performs the next action |
| run a build | verifies whether the result actually works |
| commit or deploy | acts according to scope and permission policy |
| report back | explains what changed and what was verified |

What makes the agent useful is not magical autonomy. It is the ability to continue a chain of steps without dropping the goal, while still remaining inside policy and approval boundaries.

## Failures Have to Be Considered Early

Agents are powerful, but their failures are more complex too.

| Failure point | Example |
| --- | --- |
| goal-interpretation error | working beyond the requested scope |
| bad planning | skipping documents that should have been checked first |
| wrong tool choice | using an external API when retrieval would have been enough |
| state-management failure | forgetting or misusing previous results |
| repeated loop | continuing to edit or retry after the task is already complete |
| missing approval | deleting files, sending messages, or deploying without human confirmation |
| missing evidence | writing unsupported claims as if they were facts |

That is why agent-style services also have to ask:

> how should this goal be broken into steps?  
> what data and tools are needed at each step?  
> which actions require human approval?  
> where should the flow stop when it fails or becomes ambiguous?  
> does the final result preserve evidence and execution history?

These questions then lead naturally to the next section on harnesses, logs, and evaluation.

## Checklist

- You can explain an agent as an execution structure by separating `goal`, `state`, `action`, `observation`, and `stop condition`.
- You can distinguish prompts, RAG, tool use, and agents instead of mixing them together.
- You can explain that an agent can continue a multi-step task without implying unlimited autonomy.
- You can explain that the application and server still manage permissions, approvals, state, and scope.
- You can describe a coding-agent workflow as a chain of reading, editing, verifying, and reporting.
- You can explain how the `goal`, `state`, `action`, `observation`, and `stop condition` frame keeps the agent distinct from a single model ability.

## Sources and Further Reading

- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629){: target="_blank" rel="noopener noreferrer" }, arXiv preprint, 2022, accessed 2026-06-23.
- OpenAI, [Building agents](https://developers.openai.com/tracks/building-agents/){: target="_blank" rel="noopener noreferrer" }, OpenAI Docs, accessed 2026-06-23.
- OpenAI, [Orchestrating multiple agents](https://openai.github.io/openai-agents-python/multi_agent/){: target="_blank" rel="noopener noreferrer" }, OpenAI Agents SDK Docs, accessed 2026-06-23.
