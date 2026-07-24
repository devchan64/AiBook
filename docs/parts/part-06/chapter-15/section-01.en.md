# P6-15.1 MCP Connecting Tools and Resources in a Shared Format

> Section ID: `P6-15.1`
> Version: `v2026.07.23`

In P6-14.2, we saw that an agent has a repeated structure of plan, action, and observation. Now we need to see what is needed to connect these tools and states more consistently across several systems.

MCP, or Model Context Protocol, is an interface viewpoint that helps models, agents, and applications connect more consistently to external tools and data. In other words, it is closer to an agreement to connect several tools and data sources in a more regular way instead of attaching each one separately.

## A shared connection format for tools and resources

The first issue to close is `what shared format should connect tools and resources`. Operational devices that wrap execution are about how to record and reproduce executions that use connections, and the point where authentication and permission meet real failure handling remains an operational-control problem.

Here, we read MCP as `a standardization viewpoint that tries to make tool connections less ad hoc`.

If the agent loop asked `through what repeated structure should several reads and executions continue`, the MCP viewpoint asks how the tools and resources used by that loop should be exposed in a shared format so that later execution and records shake less. Here, we hold the standard for reading `Model Context Protocol (MCP)` as a shared connection interface that keeps `model capability` separate from `tool connection format`. Execution records and reproduction environments are covered separately in the P6-15.2 harness section.

The first thing to fix here is exposing which tools and resources in what shared format, and making the connection interface regular.

| Connection information to organize first in MCP | Why it is needed | Check that follows later |
| --- | --- | --- |
| Tool descriptions and resource descriptions | Exposing which tools and resources are available under which names and input formats reduces call failure and connection mismatch. | Leads to P6-15.2 trace/replay and tool-connection notes |
| Permission boundaries and approval conditions | Showing which calls can run immediately and which require approval reduces operational failure. | Leads to P6-15.2 approval records and P6-17.2 failure handling |

The phrase `shared format` may still feel abstract. In that case, instead of memorizing the protocol name first, it is safer to imagine what breaks first when each tool has a different input format while handling the same goal.

Suppose one agent must use the following three items together.

- Search tool: `query`, `top_k`
- File-reading tool: `path`
- Schedule-lookup tool: `date`, `room_id`

If these three are connected only through completely different rules, the agent must first worry about `what shape should this tool be called in this time`, before asking `what information should be passed`. When it passes a search result to a reading step, it needs a path. When it moves to schedule lookup, it needs date and room ID formats again. Intermediate conversion and exception handling quickly increase.

With a shared connection viewpoint, by contrast, the agent can first check in a regular way which `searchable tools`, `readable resources`, and `queryable tools` are exposed under which names and input formats. In other words, MCP does not change the purpose of each tool. It is better read as a layer that makes `what can be passed to the next step` more predictable.

The same scene can be shortened like this.

| What shakes first in the same goal flow | When the shared connection viewpoint is weak | When the shared connection viewpoint exists |
| --- | --- | --- |
| Which tool to choose | Tool description locations and naming systems differ, so even selection can become confusing. | It becomes easier to check exposed tools and resources in one way. |
| What to pass to the next step | Search results, paths, and query arguments must be converted into different formats each time. | It becomes easier to match the input format expected by the next step. |
| Where to find the failure cause | It is easy to mix model judgment problems with connection-format problems. | It becomes easier to separate connection rules from execution judgment. |

## Separating model capability from tool-connection rules

When there are only one or two tools, each connection can be built directly. But as an agent structure grows, the number of tools increases and connection methods easily become inconsistent. A connection viewpoint such as MCP is an attempt to make tool descriptions, request formats, and response formats more regular so that the surrounding connection environment becomes less confusing than the model itself.

From a service-structure viewpoint, tool use is close to `calling a tool`, while MCP handles the stage of `how should those tools be exposed in a shared format`. The model's ability to understand and generate text and the external tool's exposed name, input format, and return format are different levels. We need this distinction first so we can separate whether the cause is a model limitation or a tool-exposure and connection-design problem.

The model centers on reading the given input and choosing the next needed word or action candidate. A connection viewpoint such as MCP, on the other hand, centers on how to access external tools and data outside the model, such as files, search, databases, and APIs. So MCP is closer to the problem of how to connect the execution environment around the model, rather than an `internal model capability`.

For example, when an agent structure grows, several kinds of tools become necessary inside one task.

- One tool reads files.
- One tool searches.
- One tool queries a database.
- One tool calls an API.

If all these connections are ad hoc, the system becomes harder to handle. As tools increase, failure causes scatter differently across tools unless what the model can use and what format it should use are made regular.

MCP makes three things easier first. It becomes easier to expose the tool list in a regular way, easier to keep request and response structures more consistent, and easier to reuse the connection viewpoint even when several systems change. In other words, MCP is closer to a `connection-organizing tool` than to a `new capability generator`.

Placed again inside the same request flow, prompts write the request, RAG attaches documents to read, and tool use calls functions to execute. Agents continue several steps, and MCP helps those connections be handled in a more regular format. This order keeps MCP separate from model performance and harness recording environments.

The learning needed in this section is not memorizing every implementation detail of MCP. It is enough at the introductory level to explain MCP, distinguish model capability from connection interface, and say why connection standards become important as agents and tool use grow. Then we can continue to how connected execution is passed into the P6-15.2 harness recording environment.

The first scenes to separate can be organized like this.

| First visible blockage | First question to ask | Why this question is needed first |
| --- | --- | --- |
| Tools that handle the same goal have names and input formats so different that the flow shakes before the call | Which tools and resources are exposed under which names and input formats? | If connection formats are ad hoc, format conversion and exception handling grow before model judgment matters. |
| A call succeeds, but return shapes differ and the next step keeps breaking | Can the response format also be read as a shared rule? | Even if inputs match, ad hoc output structures make the next-step connection unstable again. |
| Tools increased, but explanations of which one to use first are inconsistent | Can tool descriptions and resource descriptions be checked in one way? | If selection criteria are scattered, the same goal flow shakes from tool choice. |
| Calls that need permission are mixed with calls that can run immediately | Are permission boundaries and approval conditions visible inside the connection description? | If approval problems appear late, connection success and operational failure can be blurred into the same error. |

Using this table while reading the rest makes it easier to read MCP not as `the protocol name`, but more directly as `a shared format that makes tools and resources less ad hoc to connect`.

```mermaid
--8<-- "assets/part-06/chapter-15/p6-c15-s01-mcp-task-tool-flow-en.mmd"
```

The key point in this figure is that the agent sees tools and resources through shared connection rules instead of memorizing a different private rule for every tool.

If we understand MCP first by role rather than by technical details, connection problems become easier to separate. What MCP first tries to standardize is `what tools exist`, `what data or resources can be read`, and `in what format requests and responses happen`. So MCP is more accurately read not as `a way to make the model smarter`, but as `a way for models and external systems to connect with less confusion`.

## Differences visible in multi-tool flows

```mermaid
--8<-- "assets/part-06/chapter-15/p6-c15-s01-mcp-connection-layer-en.mmd"
```

The core of this diagram is reading MCP as `a connection layer between model and tools`.

The same content can be compared again from the viewpoint of connection congestion.

| State | What the model or agent must know | Common operational problem |
| --- | --- | --- |
| When a shared connection viewpoint such as MCP is weak | Different names, argument formats, and return formats for each tool | Format mismatch, more exception handling, higher cost to add new tools |
| When a shared connection viewpoint such as MCP exists | Tool list and resource information exposed in a shared way | It becomes easier to separate permission, quality, and evaluation problems from the connection itself. |

MCP does not automatically solve tool quality, permission problems, wrong calls, or evaluation. Organizing the connection format and improving real operational quality are different problems. So MCP is better read not as a `new capability generator`, but as a connection-organizing viewpoint that helps prompts, RAG, tool use, and agent flows handle their growing connections in a more regular format.

## Cases and examples

The focus of these cases is not `what the tool is`, but `where connection rules shake first`.

### Case 1. An agent that uses document reading and search together

Imagine an agent that finds internal policy documents and answers from them. It is easy to think that file reading and document search can be connected similarly because both are `looking at documents`. But this agent sometimes needs to open a file directly and sometimes needs to search for related documents first. For example, the approach differs when the exact file path is already known and when only keywords are known and candidate documents must be found first.

If the file-reading tool and the search tool use different call rules and result formats, the agent must separately learn `how should I access this` before making an answer. If this connection is mixed up, the preparation step before the answer may choose the wrong tool, trying to directly read a document that should be searched first, or pointlessly searching for a file whose path is already known.

The criterion changes from asking `are both about looking at documents` to asking `can readable resources and searchable resources be distinguished and handled in the same format`. A connection layer such as MCP exposes these resources in a more regular format so that `what can be read` and `what can be searched` become easier to handle in the same way. The result to check in this case is whether tool choice actually separates more consistently: files with paths are read directly, while questions without paths search first.

| Starting state | What should be used first | Problem when connection rules shake |
| --- | --- | --- |
| Exact file path is known | Read-resource call | It needlessly searches first, lengthening the response or exploring irrelevant candidates. |
| Only the topic is known, not the path | Search-resource call | It passes a wrong path to the read tool and fails immediately. |
| A candidate must be chosen from search results | Connection between search result and readable resource | The flow breaks because the format for passing search results to the next reading step is inconsistent. |

### Case 2. Coding agent

Suppose a coding agent searches a codebase, reads files, runs tests, and applies patches. It is easy to think that attaching one search tool and one execution tool separately is enough. But if each tool is attached directly, input formats and return formats differ, so separate exception handling tends to increase at every step. For example, search results may be a file list, while the test runner expects a directory path, and the patch tool may require yet another format.

In that case, `connecting tools to each other` can become a larger burden than actually fixing code. If this connection is unstable, the patch itself may be right, but verification can stop at the test-running stage because of a format mismatch. The criterion changes from `did we attach each tool` to `do tool inputs and return formats connect predictably`. With a connection-standard viewpoint, the agent can handle `searchable tools`, `readable resources`, and `executable tools` in a more predictable way. The result to check in this case is whether stages that used to stop because of input-format mismatch decrease before the patch content itself, and whether the connection from search result to test execution becomes more stable.

| Stage connection | Problem that can occur even when each tool succeeds alone | Benefit of a shared connection viewpoint |
| --- | --- | --- |
| Search result -> file read | The read resource cannot directly accept the file candidate list, so extra conversion is needed. | It becomes more predictable which item is a readable resource. |
| File read -> patch application | Location information and patch target format differ, increasing intermediate processing. | It becomes easier to regularize the minimum information structure passed as the patch target. |
| Patch application -> test execution | A file-based result cannot be directly used by a directory/command-based runner. | The executable tool can be called through a shared method, reducing next-step instability. |

### Case 3. Connecting internal organization systems

Imagine an assistant that uses a document repository, work database, and calendar API inside an organization. It is easy to think that connection itself is not a big problem as long as the needed data exists. But when these systems are attached by hand, access methods differ: documents use search queries, the database uses SQL-like queries, and the calendar uses separate API arguments. For example, even the same request to `check today's schedule` may require finding person information in the database, looking up the schedule through the calendar API, and then reading related guidance again from the document repository.

The problem here is not `there is no data`, but `each data source has a very different access rule`. If access rules are ad hoc, format errors or omissions easily occur while passing values from one system call to the next. The criterion changes from asking `does the needed data exist` to asking `can access rules for different systems be handled in a regular format`. A connection layer such as MCP exposes these systems in a model-friendly way, making what resources the agent can access and in what format more regular. The result to check in this case is whether person lookup, schedule lookup, and guidance-document reading continue more stably as one workflow instead of frequently breaking because of different rules.

The three cases can be grouped again from the connection-stability viewpoint.

| Situation | What shakes first without a shared connection viewpoint | What stabilizes first with a shared connection viewpoint |
| --- | --- | --- |
| Document reading + search | Rules for choosing readable resources and searchable resources | Distinguishing which resources are read and which resources are searched |
| Coding agent | Tool-specific input and return-format connections | Format predictability from search to execution |
| Internal system connection | Different access rules for each system | Connection flow for person information, schedules, and document lookup |

## Scenes where connection rules should be checked first

A common misunderstanding when first reading MCP is treating `tools do not connect well` immediately as a lack of model capability. But what should be checked first is not how smart the model is, but `in what shared format tools and resources are exposed`. The earlier criteria can be converted into practical check questions like this.

| If you suspect this | First question to ask |
| --- | --- |
| `The tool exists, so why does the connection keep shaking?` | Are tool descriptions and request formats exposed through shared rules? |
| `The reading step keeps breaking after search.` | Can readable resources and search results be passed through the same connection viewpoint? |
| `The call works, but the next step again requires separate processing.` | Is the return value also a shared format that the next step can read directly? |
| `Why is adding a tool so expensive?` | Is it easy to put a new tool into the same interface? |

The criterion to learn first is simple. MCP is not `a feature that makes the model smarter`. It is a shared-interface viewpoint that reduces connection instability by making `tool descriptions`, `resource access`, and `request/response formats` less ad hoc.

## Practice and example

The goal of the example is not to implement the whole protocol. It is to see how an MCP server exposes tools and resources through the official Python SDK. This example needs Python 3.10 or later and the `mcp` Python SDK. If it is not installed, install the stable release line with `pip install "mcp[cli]>=1.27,<2"` and then run the code.

There are two things to look at first in the code. The function registered with `@mcp.tool()` is exposed as an executable tool, and the function registered with `@mcp.resource("policy://refund/latest")` is exposed as a readable resource. In other words, the agent does not directly know external systems however it wants. It sees the tool names, input formats, and resource URIs exposed by the server as connection targets.

```python
from pprint import pprint

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AiBook MCP demo", json_response=True)

POLICY_INDEX = {
    "refund": "policy://refund/latest",
    "security": "policy://security/baseline",
}
POLICY_TEXT = {
    "policy://refund/latest": "Latest refund policy: request review before final reply.",
    "policy://security/baseline": "Security baseline: approval is required for account changes.",
}

@mcp.tool()
def search_policy(query: str) -> list[dict[str, str]]:
    """Search policy resources by keyword."""
    hits = [
        {"keyword": keyword, "resource_uri": uri}
        for keyword, uri in POLICY_INDEX.items()
        if keyword in query.lower()
    ]
    return hits

@mcp.resource("policy://refund/latest")
def refund_policy() -> str:
    """Read the latest refund policy resource."""
    return POLICY_TEXT["policy://refund/latest"]

request = {"query": "refund rule for a customer support answer"}
tool_result = search_policy(**request)
resource_uri = tool_result[0]["resource_uri"]
resource_text = POLICY_TEXT[resource_uri]

print("[mcp server exposes]")
pprint(
    {
        "tools": ["search_policy(query: str)"],
        "resources": ["policy://refund/latest"],
    }
)
print("[tool call]")
pprint({"name": "search_policy", "arguments": request, "result": tool_result})
print("[resource read]")
pprint({"uri": resource_uri, "text": resource_text})
```

The example output can be read like this.

```text
[mcp server exposes]
{'resources': ['policy://refund/latest'],
 'tools': ['search_policy(query: str)']}
[tool call]
{'arguments': {'query': 'refund rule for a customer support answer'},
 'name': 'search_policy',
 'result': [{'keyword': 'refund', 'resource_uri': 'policy://refund/latest'}]}
[resource read]
{'text': 'Latest refund policy: request review before final reply.',
 'uri': 'policy://refund/latest'}
```

In this output, `search_policy(query: str)` is an executable tool and `policy://refund/latest` is a readable resource. The important point is not the internal calculation of the function, but that the tool name, input format, and resource URI are registered on the server. A real MCP client discovers and calls tools and resources based on this exposed server information. What MCP organizes is not `the ability to summarize refund policies well`, but how the tool for finding refund policies and the resource for reading them are exposed in a shared format.

Extending the same principle to several requests makes the connection-format difference clearer. The graph below is not meant to explain SDK usage. It is a supporting experiment that compares what happens when tool/resource exposure is consistent and when it shakes. Using the tool catalog CSV [p6-15-1-mcp-tool-catalog.csv](/AiBook/assets/part-06/chapter-15/p6-15-1-mcp-tool-catalog.csv){ .csv-preview }, resource catalog CSV [p6-15-1-mcp-resource-catalog.csv](/AiBook/assets/part-06/chapter-15/p6-15-1-mcp-resource-catalog.csv){ .csv-preview }, and request CSV [p6-15-1-mcp-connection-requests.csv](/AiBook/assets/part-06/chapter-15/p6-15-1-mcp-connection-requests.csv){ .csv-preview }, 36 requests are passed through a shared connection layer (`common_layer`) and an ad hoc connection layer (`mixed_layer`). The comparison shows where request completion, connection readiness, tool interpretation, and resource interpretation split.

![MCP connection-layer check](/AiBook/assets/part-06/chapter-15/mcp-connection-layer-check-en.png)

This chart separates the difference between the shared connection layer and the ad hoc connection layer into request completion, connection readiness, tool interpretation, and resource interpretation. Even in the shared connection layer, completion remains at 19 cases because of approval and missing inputs, but connection readiness passes all 36 cases. In contrast, even if the ad hoc connection layer can find tools and resources to some extent, input formats and resource types shake, so connection readiness and request completion drop sharply.

The result to check in this graph is that models or agents do not handle external systems directly one by one. They access tools and resources through a connection layer that exposes them through a shared interface.

Readers can try these adjustments in this section.

- Call `search_policy()` with a question containing `security` in the SDK example and see whether a different resource URI is returned.
- Add one more `@mcp.tool()` tool to the SDK example and see how the tool name and input format appear in the output description.
- In the CSV supporting experiment, add `input_schema` to only one tool in `mixed_layer` and check why overall consistency is still broken.

One more step separates what MCP directly organizes from what still needs to be passed to a harness or operations.

| Situation | What MCP directly organizes | What still remains beyond MCP alone |
| --- | --- | --- |
| Tool names and input formats are ad hoc | Exposes shared names, input formats, and resource types | Execution trace storage, replay, evaluation records |
| Resource access differs by system | Exposes readable resources and executable tools in the same connection layer | Judging which execution was actually safe |
| Connections often break when adding a new tool | Lowers addition cost by keeping connection formats regular | Approval gates, failure recovery, cost control |
| It is unclear whether the problem is model performance or connection design | Separates connection-interpretation failure from internal model-performance problems | How to manage quality and operation after connection succeeds |

The key point of this table is that MCP is `a layer that makes connections regular`, not a layer that records execution or judges quality. A harness leaves the same connection as execution trace and replay, while evaluation and operations read that record as quality judgment and control action.

## Connection format matters more than tool count

This compressed connection structure shows that in an era of many tools, what matters is `how to connect them in the same way`, more than `the number of tools`. The MCP viewpoint is not `a technology for attaching more tools`, but `a connection rule that lets attached tools be read and called in the same way`. The more important point is that `what the model says` and `what systems that model connects to, and in what format`, are not the same problem.

## Checklist

- You should be able to explain MCP not as `a new model capability`, but as `a connection-interface viewpoint that exposes tools and resources in a shared format`.
- You should be able to say that model problems and connection problems should be separated into different levels.
- You should know that connected execution continues into the problem of what record and reproduction environment should manage it.

## Sources and Further Reading

- Model Context Protocol, [What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19.
- OpenAI, [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Using tools](https://developers.openai.com/api/docs/guides/tools){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
