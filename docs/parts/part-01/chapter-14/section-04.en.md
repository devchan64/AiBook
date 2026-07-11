# P1-14.4 MCP and the Standardization of Tool Connections

> Section ID: `P1-14.4`
> Version: `v2026.07.11`

P1-14.3 described an `agent` as a workflow that carries `goal`, `state`, `action`, and `observation` forward. When an agent uses outside data or tools, it needs a connection method.

> agent:  
> decides what should be done and continues the workflow
>
> MCP:  
> standardizes how an agent or AI application connects to outside tools and data

`MCP (Model Context Protocol)` is an open protocol that aims to standardize how AI applications connect to external systems. The most important point is that MCP is neither the `model` itself nor the `agent` itself.

> MCP is a protocol for aligning the way AI applications connect to outside data, tools, and reusable work templates.

This section does not implement MCP in depth. It only explains why this kind of standardization is needed and what components are useful to keep in mind.

In Part 1, the basic distinctions among `MCP`, `host`, `client`, `server`, `tools`, `resources`, and `prompts` are fixed here. Section 14.3 explained how agents continue work across multiple steps toward a goal. Here the focus shifts to a narrower question: `how can that workflow discover and call outside tools and data in a common way?` Execution tracing and evaluation return in 14.5.

## Scope of This Section

This section explains the basic role and structure of MCP. It does not cover MCP server implementation details, SDK usage, JSON-RPC message details, or OAuth authentication flow. Harnesses, evaluation, and execution logs are covered in P1-14.5. Detailed security and privacy issues return in P1-15.1, P1-15.2, and P1-15.3.

`MCP`, `host`, `client`, `server`, `tool`, `resource`, and `prompt` belong to different layers of connection.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| MCP | a connection protocol for AI applications and external systems | the standardization perspective of Chapter 14 |
| host | the application or runtime the user interacts with | the side that owns the connection |
| client | the component that communicates with one MCP server | the unit that manages a connection |
| server | the program that provides tools, resources, or prompts | the provider of outside capability |
| tool | an executable function | the unit of action calling |
| resource | readable context data | the input side of state and evidence |
| prompt | a reusable interaction template | a device for reusing instruction formats |

The baseline distinction here is simple: `MCP is the connection rule`, `the server provides capability`, `tools are for execution`, `resources are for reading`, and `prompts are reusable templates`.

| Topic | Question examined in this section |
| --- | --- |
| standardization | why is a common rule needed for tool connection? |
| components | what do host, client, and server each handle? |
| exposed objects | how are tools, resources, and prompts different? |
| connection flow | what does an agent discover and call through MCP? |
| cautions | what problems does MCP not solve? |

## Goal of This Section

- Understand MCP as a connection `protocol`, not as an agent.
- Distinguish the roles of `host`, `client`, and `server`.
- Avoid mixing up `tools`, `resources`, and `prompts`.
- Understand that MCP can make tool use easier but does not automatically solve permission, approval, or validation.
- Prepare to move into the harness and evaluation environment in P1-14.5.

## Three Standards

This section does not explain MCP like a new model. It frames MCP as a connection rule. The three standards below are the main guide while reading.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| MCP is a connection protocol, not an agent | This prevents MCP from being misunderstood as another AI system. | It is enough to understand it as a rule for linking applications and outside systems. |
| host, client, and server have different roles | This makes the standardization structure readable. | It is enough to distinguish who requests, who mediates, and who provides capability. |
| even with standardization, permission and validation remain separate problems | This prevents overconfidence in the protocol itself. | It is enough to understand that approval and security still need separate handling. |

## Why a Connection Standard Is Needed

As P1-14.1 explained, an AI service combines the model, application, data, tools, and orchestration. The problem is that as the service grows, the number of outside systems that need to be connected also grows.

> file systems  
> databases  
> search engines  
> calendar tools  
> issue trackers  
> design tools  
> automation tools  
> internal document systems

If every AI application builds a separate custom connection for every tool, the combinations become complicated very quickly.

> app A -> tool 1, tool 2, tool 3  
> app B -> tool 1, tool 2, tool 3  
> app C -> tool 1, tool 2, tool 3

In a situation like this, very similar code gets repeated every time the same tool is attached to another application. MCP can be read as an attempt to reduce that problem by offering `a common rule through which AI applications talk to outside systems`.

The idea can be simplified as:

> a different custom connection for each tool  
> -> discovering and calling through a common protocol

Official MCP introduction material describes MCP as an open standard that helps AI applications connect to data sources, tools, and workflows.

## Host, Client, and Server

MCP follows a client-server structure. But if we imagine only the usual web-service client and server, the picture can become blurry. In MCP, it helps to distinguish `host`, `client`, and `server`.

| Component | Description |
| --- | --- |
| MCP host | the AI application or agent runtime the user interacts with |
| MCP client | the component that maintains a connection to one particular MCP server |
| MCP server | the program that exposes outside data, tools, and prompts through MCP |

The flow can be simplified like this:

```mermaid
--8<-- "assets/part-01/chapter-14/mcp-connection-flow-en.mmd"
```

One AI application may connect to several MCP servers. In that case, there is usually a separate MCP client for each server connection. For example, a coding tool may be connected at the same time to a file-system MCP server and an issue-tracker MCP server.

An important point is that an MCP server does not have to be a remote server. It may be a program running on the local machine, or a remote service accessed across the network.

## What an MCP Server Provides

The main elements exposed by an MCP server are `tools`, `resources`, and `prompts`.

| Element | Role | Example |
| --- | --- | --- |
| tools | executable functions or actions | file reading, issue creation, database lookup, calculation |
| resources | readable context data | file contents, database rows, API responses, document fragments |
| prompts | reusable interaction templates | task instructions with examples for a particular workflow |

This also connects to the distinction already seen in P1-14.2.

> resources:  
> provide context the model can read
>
> tools:  
> execute external system functions
>
> prompts:  
> help reuse an interaction pattern in a stable form

For example, if an internal document system is exposed through an MCP server, the items can be separated like this.

| Exposed item | From the MCP point of view |
| --- | --- |
| reading document body | resource |
| executing document search | tool |
| a regulation-review question template | prompt |

With this split, the agent can understand more clearly `what can be read`, `what can be executed`, and `what interaction formats are already prepared`.

## Discovery and Calling

One of the main intuitions of MCP is `discovery`. An AI application can ask a connected MCP server what tools and resources it offers.

> 1. the AI application connects to an MCP server  
> 2. it checks what capabilities the server exposes  
> 3. it retrieves the available tool list  
> 4. it selects the needed tool and calls it  
> 5. it reflects the result into model input or application state

Official architecture documents show flows such as `tools/list`, which retrieves the available tools, and `tools/call`, which executes a chosen tool. The important point is that before execution, the application can check `what tools exist`, and at call time it can structure `what name and arguments should be sent`.

Suppose there is a weather MCP server.

> tool discovery:  
> there is a `weather_current` tool
>
> tool description:  
> retrieves current weather
>
> input format:  
> `location`, `units`
>
> call:  
> `location = Seoul`  
> `units = metric`
>
> result:  
> current weather data

With this structure, the model does not remain at the vague level of answering in natural language, `check the weather`. Instead, the application can construct a tool-call candidate the host can understand. Actual execution still has to happen within the host and server permission policy.

## MCP Organizes the Connection Surface of an Agent

If we return to the agent loop from P1-14.3, MCP’s position becomes clearer.

> check the goal  
> -> inspect state  
> -> choose the next action  
> -> execute a tool  
> -> observe  
> -> update state

MCP mainly organizes the connection surface for `tool execution` and `outside context acquisition`.

| Agent-flow stage | What MCP can help with |
| --- | --- |
| checking state | reading files, documents, or data through resources |
| choosing the next action | inspecting what tools are available and what they do |
| executing the tool | calling the tool in a standardized way |
| observing | receiving structured tool results for the next decision |

But MCP does not guarantee plan quality, judgment quality, or final task success. MCP is a connection rule. Which goal the agent chooses, in what order it acts, and when it stops are still questions of the application, model, harness, and policy.

## What MCP Does Not Solve

MCP helps standardize tool connections, but it does not automatically solve every problem.

| Problem it does not solve | Why |
| --- | --- |
| deciding whether a tool is safe | the tool exposed by the server itself may be risky |
| deciding user permissions | who may see which data remains a service-policy issue |
| execution approval | actions that change outside state may still require human confirmation |
| truthfulness of interpretation | tool results still need separate review for interpretation |
| agent evaluation | measuring whether the task succeeded belongs to harness and evaluation design |

MCP security documents also discuss risks such as the confused deputy problem, token passthrough, SSRF (Server-Side Request Forgery), session hijacking, and local MCP server compromise. Security is not covered deeply here, but because MCP servers connect to outside systems, trust boundaries must always be considered.

The first safety principle to keep is the following.

> Connecting an MCP server means adding outside capability.  
> Outside capability has to be handled together with permission, approval, logging, and isolation.

## MCP in a Document Workflow

A long-form document workflow makes MCP’s position easier to see.

> user:  
> strengthen the draft of a specific section
>
> agent:  
> checks the table of contents and surrounding sections  
> finds supporting material  
> writes the body  
> verifies the build  
> reports the result

If MCP exists, the following connection surfaces can be standardized.

| Task | What it could connect to through MCP |
| --- | --- |
| reading document files | a file-system MCP server |
| checking issues and work status | an issue-tracker or project-management MCP server |
| searching supporting material | a search or document-repository MCP server |
| running verification work | a local execution environment or command-execution tool |

This example does not mean MCP writes the document for the agent. MCP is only the connection rule that lets the agent discover and use outside data and tools more consistently.

## The View to Keep from This Section

MCP (Model Context Protocol) is a protocol that tries to standardize the connection between AI applications and outside systems.

> the agent continues a goal as a workflow  
> MCP organizes how that workflow connects to outside tools and data

> the host owns the connection  
> the client manages a server link  
> the server provides tools, resources, and prompts  
> tools execute actions  
> resources provide context data  
> prompts provide interaction templates  
> permission, approval, security, and evaluation are not solved automatically

If this view is fixed, the next section’s `harness` becomes easier to read. A harness leads to the question of how the model, tools, and MCP connections are wrapped, recorded, and evaluated in an actual execution environment.

## Checklist

- You can explain MCP as a connection protocol rather than as an agent or model.
- You can distinguish the roles of host, client, and server.
- You can distinguish tools, resources, and prompts.
- You can explain that MCP can help with tool connection and context acquisition in an agent workflow.
- You can explain that MCP does not automatically solve permission, approval, security, or evaluation.

## When to Recall This View First

- when MCP is being mixed at the same level as the model, the agent, or the tool itself
- when standardization and actual execution responsibility must be distinguished in an outside-system connection
- when the convenience of tool connection must be separated again from the responsibilities of permission, approval, and validation

At that point, first separate `connection rule`, `capability provider`, and `execution responsibility`. That makes it less likely to misread MCP as the tool itself or the agent itself.

## Sources and Further Reading

- Model Context Protocol, [What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Model Context Protocol, [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Model Context Protocol, [Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
