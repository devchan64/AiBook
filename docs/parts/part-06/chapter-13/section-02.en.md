# P6-13.2 Function Calling That Splits Natural-Language Requests into Names and Arguments

> Section ID: `P6-13.2`
> Version: `v2026.07.23`

In P6-13.1, we saw that tool use connects the model with external functions. That leads to a more specific question.

In what format does a system exchange the judgment that a tool should be used?

Function calling is a method that makes the model express which tool should be called and with which arguments in a structured format.

## Standards for structuring execution requests

The core questions are these.

- Why is function calling needed?
- How is a natural-language request different from a structured tool call?
- Why does it matter to separate the function name from arguments?

The first issue to close is reading function calling as `a structured execution request for connecting tool use reliably`, and seeing why natural language needs to become a name-and-argument structure.

An execution structure that continues repeated work is a problem of tying several structured calls into multiple steps. Function calling first focuses on making one execution request verifiable.

Here we read function calling not as a product feature name, but as `a structuring method for connecting tool use reliably`. If tool use asked `what should be executed`, function calling asks how that execution judgment should become a name-and-argument structure so the system can validate and continue processing it. The question of how to chain several calls continues in P6-14's agent structure.

The core change is from `what should be executed` to `how do we turn that execution request into a verifiable structure`. This difference lets us read function calling not as a simple product feature, but as an intermediate layer that stabilizes execution connection.

The first records to keep at this stage are the function name, arguments, missing-field check, expected result format, and the reason a call was blocked. These records let us realign natural-language requests with execution structure, and separate execution failure from later operational failure.

## Separating natural-language requests from structured execution requests

A natural-language request is easy for people to read and infer from. A structured execution request separates the name and fields so the system can check them before execution. The two forms can carry the same intent, but they are used differently.

| Distinction | Natural-language request | Structured execution request |
| --- | --- | --- |
| Main reader | Human and model | Application, API, execution environment |
| Main strength | Easy to express intent broadly | Easy to validate fields and trace logs |
| Common weakness | Missing conditions can be hidden inside a sentence | Intent outside the schema needs separate interpretation |
| First thing to check | What did the user want? | Which function will run with which arguments? |

## How a request becomes a function name and arguments

Function calling does not execute natural language directly. It converts it into an intermediate expression that can be checked before execution. The transition can be separated like this.

| Stage | Example | What to check at this stage |
| --- | --- | --- |
| Natural-language request | `Convert 300 dollars to KRW today` | What does the user want? |
| Function candidate | `lookup_exchange_rate` | Which function should be called? |
| Argument candidate | `base_currency=USD`, `quote_currency=KRW`, `amount=300` | Are the values needed for execution filled? |
| Validation result | `ready` or `needs_clarification` | Execute now, ask back, or require approval? |

The important point in this table is that function calling is not an `answer sentence`. It is a verifiable request structure immediately before execution.

## Why structuring is needed

If tool use is handled only with natural-language sentences, ambiguity is large.

Suppose the model says:

`Search today's exchange rate in Seoul and tell me.`

A person can understand the sentence, but the system may still find these unclear.

- Which tool should be used?
- What are the arguments?
- What date format is expected?
- What should be returned on failure?

So a function-calling structure usually separates:

- Tool name
- Argument name
- Argument value

In other words, natural language is not executed as is. It is converted into an `executable structure`.

Natural-language requests and structured function calls carry the same intent in different forms. Natural language is easy for people, but missing conditions can hide inside it. Structured calls look rigid to people, but make it easier for the system to validate fields and keep execution records. Function calling can therefore be read as a method for turning sentences into structure so the system can execute the model's intent more safely.

## Why separate function name and arguments

This distinction lets the system separately verify `which function to call` and `which values to pass into that function`, then divide failure causes.

For example:

- Function name: `lookup_exchange_rate`
- Arguments: `{"base_currency": "USD", "quote_currency": "KRW", "amount": 300}`

With this separation, the system can more easily:

- check whether the tool is allowed
- validate argument formats
- detect missing arguments
- require approval before execution

Function calling is not just neat formatting. It is a structure that increases `verifiability` and `controllability`.

## Should results also be structured?

Yes. When a tool result also returns structurally:

- the model can read it again more easily
- the app can postprocess it more easily
- logging and trace become easier

So function calling is better read not only as input structuring, but as a flow that reconnects execution results.

## Function calling is not always enough

Having function calling does not guarantee:

- the model always chooses the right tool
- arguments are always complete
- wrong execution is fully blocked

Real systems therefore usually add:

- schema validation
- permission checks
- user approval
- retry or error reporting on failure

## A minimal diagram

```mermaid
--8<-- "assets/part-06/chapter-13/p6-c13-s02-function-call-flow-en.mmd"
```

The point of this diagram is that the flow changes to `sentence -> structure -> execution -> result`.

## Cases and examples

### Case 1. Exchange-rate lookup

Consider the request `Tell me today's dollar exchange rate`. It can feel like the system should handle it directly because people roughly understand it. But the system needs to separate arguments such as `which currency pair`, `which date`, and `which regional standard` before an actual lookup is possible. For example, the user's intent may be `USD/KRW`, or it may be the `dollar index`. Without this separation, the lookup can succeed while returning a value different from the user's intended one. `Execution success` and `intent match` are not the same thing.

The standard changes from asking whether `the question is roughly understandable` to asking whether `the arguments required for lookup are fully structured`. Function-calling structure turns natural language into explicit fields, making the execution stage clearer. The misunderstanding to move past is the expectation that `if the sentence is naturally understood, the lookup will also be correct`. The result to check is whether the question is split into arguments such as currency pair and reference date before lookup, and whether those arguments alone let us reconfirm the original intent.

### Case 2. Calendar creation

In natural language, `Schedule a meeting tomorrow at 3 PM` can feel specific enough. People often expect that others will understand it. But the actual calendar API needs more structured arguments such as attendees, timezone, title, and date format. `Tomorrow` can mean a different date when the user's timezone changes, and without attendees the event creation itself can be incomplete. If this difference is missed, the model may understand the sentence well but the execution stage can stop immediately or create an event at the wrong time. A calendar event created with the wrong time or empty attendees is closer to an operational failure than a success.

The standard changes from asking whether `the sentence is specific enough` to asking whether `all fields required by the API are actually filled`. Function-calling structure turns implicit information into an explicit argument bundle. The result to check is whether time, date, title, and attendees are all structured before calendar creation, and whether missing fields become visible before execution.

### Case 3. Code agent

Imagine a code agent alternating among reading files, running tests, and applying patches. If only a natural-language explanation is left, it is hard to trace which work ran with which arguments. A sentence like `I read the file and ran tests` may feel descriptive enough, but in operation we need to know which file was read and which test command ran. The same sentence `ran tests` can mean very different things depending on directory, flags, and target.

If the process is recorded as function calls, steps such as `read_file`, `run_tests`, and `apply_patch` are explicit and the execution flow is easier to replay. The standard changes from recording only `what work was done` to checking whether `which function ran with which arguments` can be traced. Without this record, when the same failure appears again it is hard to tell which stage input changed. Function calling is therefore directly connected not only to execution success, but also to logs and reproducibility. The result to check is whether we can trace which function was called with which arguments, and reconstruct which stage stopped because of missing arguments.

The three cases can be grouped again from the structuring view.

| Situation | What remains ambiguous in natural language | What function-calling structure makes explicit |
| --- | --- | --- |
| Exchange-rate lookup | Which value to look up under which standard | Currency pair, date, region arguments |
| Calendar creation | Execution standard for expressions such as `tomorrow` and `afternoon` | Date, time, timezone, attendee fields |
| Code agent | What ran in what order | Function name, arguments, execution log |

The same content can be reread as a structured execution-request flow.

```mermaid
--8<-- "assets/part-06/chapter-13/p6-c13-s02-function-call-boundary-en.mmd"
```

The key point is that `structured` and `ready to execute` are not the same.

## When structured calls are needed

The most common confusion when first reading function calling is treating `the sentence is understood` and `execution is ready` as the same. In reality, we must separately inspect which function will be called, which fields are required, and whether execution is possible without missing values.

| If this scene appears | Check first | Why this comes first |
| --- | --- | --- |
| The request meaning is clear, but the system's tool choice is ambiguous. | Is the function name clearly decided? | If the function name is ambiguous, the execution target is unstable before argument validation even begins. |
| The function seems right, but execution often stops immediately. | Are required arguments filled without omissions? | A natural sentence can make sense while fields such as date, timezone, and currency pair are still empty. |
| The structure exists, but results are still unstable. | Are result format and failure reason recorded together? | Retry or correction is possible only when call success and failure can be traced. |

The same standard can be shortened into practical questions.

| If you suspect this | First question to ask |
| --- | --- |
| `I know what it wants to do, but the call is vague.` | Did one function name make the execution target clear? |
| `The request is specific, so why does execution fail?` | Are all required arguments filled? |
| `It failed, but I do not know where it stopped.` | Were result format and failure reason recorded structurally? |

The first standard is simple. Function calling is not `making natural language look neat`. It is a structure that separates `function name`, `arguments`, and `result` so pre-execution validation and post-execution tracing become possible.

## Exercise and example

This example does not call a real API or model. It shows which validation checks function-call candidates must pass before execution. With only one or two sentences, it is easy to think that `making a function name and arguments is enough`. So we validate several function candidates in one batch and see which are ready, which need clarification, and which must stop for approval.

The example below uses the function-call candidate CSV [p6-13-2-function-call-requests-en.csv](/AiBook/assets/part-06/chapter-13/p6-13-2-function-call-requests-en.csv){ .csv-preview }. One row contains a user request, reference English request, function name, argument candidates, and whether approval is required. This CSV is not a log produced by a real model. It is input created to inspect the validation structure of function calling. `model_request_en` is a reference column for imagining multilingual translations and model input format. The validation code in this example uses only the function name and argument candidates. Blank cells in the CSV mean that the function-call candidate still lacks an argument or needs confirmation before execution.

Users ask in natural language to create calendar events, look up exchange rates, patch files, or send email drafts. The system does not execute those sentences directly. It first checks required arguments against each function's schema, and separates requests that change external state into an approval-pending state. Therefore, `structured` and `ready to execute` are not the same.

The inspection items to read together are these.

| Inspection item | Why it is needed |
| --- | --- |
| `function_name` | Check which function is being called. |
| `missing_fields` | Check which arguments are empty before execution. |
| `status` | Separate ready, clarification needed, and approval needed. |
| `schema_required_fields` | Confirm that each function has different required arguments. |

The input CSV has 24 rows. The point is not large-scale data handling or statistical representativeness. It is to place candidates with different validation standards side by side: calendar creation, exchange-rate lookup, file patch, and email draft. The number of rows helps show that each function schema creates different required-argument checks.

The core point in the code is that function-call style tool use separates `function name`, `arguments`, `schema validation`, and `approval` to create the state immediately before execution.

```python
from collections import Counter, defaultdict
import csv
from pathlib import Path

CSV_PATH = Path("docs/assets/part-06/chapter-13/p6-13-2-function-call-requests-en.csv")

function_schemas = {
    "create_calendar_event": ["title", "date", "time", "timezone", "attendees"],
    "lookup_exchange_rate": ["base_currency", "quote_currency", "amount"],
    "apply_file_patch": ["file_path", "change_summary"],
    "send_email_draft": ["recipient", "subject", "body"],
}

def is_blank(value):
    return value is None or value.strip() == ""

def build_function_call(row):
    required_fields = function_schemas[row["function_name"]]
    arguments = {field: row.get(field, "") for field in required_fields}
    return {
        "name": row["function_name"],
        "arguments": arguments,
        "approval_required": row["approval_required"].strip().lower() == "true",
    }

def validate_function_call(function_call):
    required_fields = function_schemas[function_call["name"]]
    missing_fields = [
        field for field in required_fields if is_blank(function_call["arguments"].get(field))
    ]
    if missing_fields:
        status = "needs_clarification"
    elif function_call["approval_required"]:
        status = "needs_approval"
    else:
        status = "ready"
    return {
        "function_name": function_call["name"],
        "schema_required_fields": required_fields,
        "missing_fields": missing_fields,
        "status": status,
    }

with CSV_PATH.open(encoding="utf-8", newline="") as file:
    rows = list(csv.DictReader(file))

reports = []
for row in rows:
    function_call = build_function_call(row)
    validation = validate_function_call(function_call)
    reports.append(
        {
            "request_id": row["request_id"],
            "user_request": row["user_request_en"],
            "function_call": function_call,
            "validation": validation,
        }
    )

status_counts = Counter(report["validation"]["status"] for report in reports)
function_status_counts = defaultdict(Counter)
missing_field_counts = Counter()
for report in reports:
    validation = report["validation"]
    function_status_counts[validation["function_name"]][validation["status"]] += 1
    missing_field_counts.update(validation["missing_fields"])

summary = {
    "request_count": len(reports),
    "status_counts": dict(status_counts),
    "missing_field_counts": dict(missing_field_counts),
    "function_status_counts": {
        function_name: dict(counts)
        for function_name, counts in function_status_counts.items()
    },
}

print("[summary]")
print(summary)
print()

sample_ids = {"F01", "F02", "F07", "F19"}
for report in reports:
    if report["request_id"] not in sample_ids:
        continue
    print("=" * 80)
    print(f"[{report['request_id']}] {report['user_request']}")
    print("[function_call]")
    print(report["function_call"])
    print("[validation]")
    print(report["validation"])
```

Example output can be read like this.

```text
[summary]
{'request_count': 24, 'status_counts': {'ready': 13, 'needs_clarification': 9, 'needs_approval': 2}, 'missing_field_counts': {'time': 1, 'timezone': 1, 'title': 1, 'attendees': 1, 'quote_currency': 1, 'amount': 1, 'file_path': 1, 'change_summary': 1, 'recipient': 1, 'body': 2}, 'function_status_counts': {'create_calendar_event': {'ready': 3, 'needs_clarification': 3}, 'lookup_exchange_rate': {'ready': 4, 'needs_clarification': 2}, 'apply_file_patch': {'ready': 4, 'needs_clarification': 2}, 'send_email_draft': {'needs_approval': 2, 'ready': 2, 'needs_clarification': 2}}}

================================================================================
[F01] Create a design review meeting tomorrow at 3 PM in Seoul time.
[function_call]
{'name': 'create_calendar_event', 'arguments': {'title': 'Design review', 'date': 'tomorrow', 'time': '15:00', 'timezone': 'Asia/Seoul', 'attendees': 'design@example.com'}, 'approval_required': False}
[validation]
{'function_name': 'create_calendar_event', 'schema_required_fields': ['title', 'date', 'time', 'timezone', 'attendees'], 'missing_fields': [], 'status': 'ready'}
================================================================================
[F02] Schedule a team meeting tomorrow afternoon in Seoul time.
[function_call]
{'name': 'create_calendar_event', 'arguments': {'title': 'Team meeting', 'date': 'tomorrow', 'time': '', 'timezone': 'Asia/Seoul', 'attendees': 'team@example.com'}, 'approval_required': False}
[validation]
{'function_name': 'create_calendar_event', 'schema_required_fields': ['title', 'date', 'time', 'timezone', 'attendees'], 'missing_fields': ['time'], 'status': 'needs_clarification'}
================================================================================
[F07] Convert 300 USD to KRW using today's rate.
[function_call]
{'name': 'lookup_exchange_rate', 'arguments': {'base_currency': 'USD', 'quote_currency': 'KRW', 'amount': '300'}, 'approval_required': False}
[validation]
{'function_name': 'lookup_exchange_rate', 'schema_required_fields': ['base_currency', 'quote_currency', 'amount'], 'missing_fields': [], 'status': 'ready'}
================================================================================
[F19] Send Minsu a meeting notes draft.
[function_call]
{'name': 'send_email_draft', 'arguments': {'recipient': 'minsu@example.com', 'subject': 'Meeting notes draft', 'body': "Here is today's meeting notes draft"}, 'approval_required': True}
[validation]
{'function_name': 'send_email_draft', 'schema_required_fields': ['recipient', 'subject', 'body'], 'missing_fields': [], 'status': 'needs_approval'}
```

The first thing to inspect is `status_counts`. Of 24 call drafts, 13 are ready to execute, 9 need clarification because required arguments such as `time`, `timezone`, `file_path`, or `body` are missing, and 2 stop in approval-pending state even though required arguments are filled. This is why function-call structure matters: it exposes these differences before execution instead of hiding them behind a natural-language answer.

Next, look at `function_status_counts`. The same `ready` state is produced by different required-argument bundles across calendar creation, exchange-rate lookup, file patching, and email draft. Function calling is therefore not applying one universal field check to every tool. Once the function name is determined, validation changes to that function's schema.

Finally, `missing_field_counts` shows that missing information is not one kind of failure. Calendar creation may miss `time`, `timezone`, or `attendees`. Exchange-rate lookup may miss `amount` or `quote_currency`. File patching may miss `file_path` or `change_summary`. Email drafts may miss `recipient` or `body`. Function calling can therefore record not just `failure`, but which argument stopped execution.

The reader can directly adjust the example in these ways.

- Add a new function candidate to the CSV and add required arguments to `function_schemas`.
- Change `approval_required` and check whether the same argument structure becomes `ready` or `needs_approval`.
- Fill or remove blank cells and see how `status_counts` and `missing_field_counts` change.
- Add required fields to `function_schemas` and see how stricter operation policy increases clarification needs.

One step further, we should separate what function calling solves from what remains unsolved.

| Situation | What function calling directly solves | What remains beyond function calling |
| --- | --- | --- |
| The request is understandable, but execution input is ambiguous. | Separates function name and arguments to make execution input explicit. | Quality of deciding which tool to choose |
| Missing fields need to be caught before execution. | Validates missing arguments such as `missing_fields`. | Semantic interpretation of whether the values match user intent |
| Results need to be passed to a later step. | Makes it easier to return results in a consistent structure. | Planning the order of several calls |
| Failure needs to be reproduced and logged. | Traces which function was called with which arguments. | Retry, alternative path, and stopping criteria in the operational loop |

This table matters because it prevents us from collapsing `function calling = agent`. Function calling structures one request immediately before execution, while planning and retrying several calls belongs to the agent layer.

## Validation standards that split inside structured execution requests

The example above is not code that implements all of function calling. It shows that `what a person says` and `what a system executes` are not the same sentence. The important point is not removing natural language, but reading which name and argument structure must exist immediately before execution.

In the chart, each function splits into a different execution-readiness state within the same batch. The left side shows calendar creation, exchange-rate lookup, file patch, and email draft divided into `ready`, `needs clarification`, and `needs approval`. The right side shows every missing field that blocked execution. So the important point is not merely that a structure exists, but that the structure can reveal which fields are missing and which requests must not proceed without approval.

![Function-call validation example showing readiness state by function and missing-field distribution](/AiBook/assets/part-06/chapter-13/function-call-validation-en.png)

## How function calling stabilizes execution requests

The core of function calling is not removing natural language. It is changing a request immediately before execution into `a verifiable structure where name and arguments are separated`.

The more important distinction is that `explaining well` and `passing an actually executable request structure` are not the same problem. Function calling is therefore not decoration that adds more tools. It is a representative way to make tool use less unstable by turning requests into verifiable structures just before execution.

This structuring matters because it:

- keeps tool use from staying at the level of vague natural language
- gives us the structural sense needed to understand agents, MCP, and harnesses
- explains why executable AI services need an application layer

## Checklist

- You should be able to explain function calling as `a verifiable call structure where name and arguments are separated`, not as a natural-language instruction.
- You should be able to say why separating `which function` from `which arguments` makes validation and failure tracing easier.
- You should understand that the next question moves to how structured calls are connected in order inside a goal flow.

## Sources and references

- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed: 2026-07-19.
- OpenAI, [Using tools](https://developers.openai.com/api/docs/guides/tools){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed: 2026-07-19.
- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed: 2026-07-19.
