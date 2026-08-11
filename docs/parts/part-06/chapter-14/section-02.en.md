# P6-15.2 Agent Loops That Split into Continue, Stop, and Human Review

> Section ID: `P6-15.2`
> Version: `v2026.07.31`

Keep loop records as `plan`, `action`, `observation`, `continue_reason`, `stop_condition`, and `human_review_reason`. Then continuing, stopping, or handing off to human review is connected to observations and stop conditions, not to the model's mood.

In P6-15.1, we read an AI agent as an execution structure that changes the next task based on intermediate results. Now we need to look more concretely at what criteria make that flow continue, where it stops, and when it moves to human review.

An AI agent has a repeated structure: it plans the next step based on a goal, performs an actual action, observes the result, and then chooses the next decision. What matters here is not the mere fact that the loop runs, but which direction the observation result branches into: `continue`, `stop`, or `human review`.

## What the repeated loop is responsible for

The issue to settle in this scene is reading the basic structure of a single AI agent loop as `plan-action-observation repetition`, and distinguishing where it should continue and where it should stop.

Tool connection rules and execution environments are about which tools and resources the loop uses, and what recording environment keeps the execution. The plan-action-observation loop first focuses on how observation results change the next branch and stop decision.

An agent should not be left only as an abstract concept. It should be read as a loop in which `plan`, `action`, and `observation` repeat. If P6-15.1 looked at how several reads and executions continue as a goal flow, this section looks at how that flow splits into continuation, termination, and human review based on intermediate observation.

The core viewpoint changes from `should several steps continue` to `through what observation and decision loop do those steps repeat`.

The first records to keep at this stage are the plan, action, and observation records that show where a judgment changed, plus the stop reason and next step that show when it stopped and why it was handed to a person. These records let us narrow down loop failure and retry reasons later.

## Distinguishing plan, action, observation, and stop conditions

The reason to separate plan, action, observation, and stop condition is not memorizing terms. Even failures that look similar require different next decisions depending on which point was unstable.

| Observation result | Following decision | Why the branch splits this way |
| --- | --- | --- |
| Evidence is still insufficient | Continue or replan | The system should change search terms, tools, or order, not repeat the same action. |
| Evidence is sufficient and conflict is small | Stop | More iterations may add cost and time more than quality. |
| Document conflict, lack of permission, or high state uncertainty | Move to human review or handoff | Risky scenes must be left as a separate boundary instead of being settled automatically. |

If we hold this table first and then read `plan`, `action`, `observation`, and `stop condition` below, it becomes easier to understand an AI agent loop not as `a structure that keeps spinning`, but as `a structure whose next action changes according to observation`. The definitions that follow are the minimum pieces needed to read this branch table.

## What is a plan?

A plan is the stage that decides `what should be done now`.

If the goal is:

`Find and summarize the latest refund policy`

then the plan stage may look like this:

- Search policy documents first.
- Check the latest notice first.
- Extract only the changed parts.

In other words, planning means dividing a goal into smaller subtasks.

## What is an action?

An action is the stage that actually performs something.

Examples include:

- calling a search tool
- reading a file
- running a calculation
- making an API request

The important point is that an action is not merely `suggesting the next step in words`. It is the stage that actually affects the outside world or brings back a real result.

## What is an observation?

An observation is the stage that reads the result of an action.

Examples include:

- search results were too sparse
- the file did not exist
- the calculation result differed from expectation
- the API call failed

Without observation, the agent may keep repeating the same action or move to the next step without realizing that it failed.

## Why split plan, action, and observation

Readers can easily see this flow as one lump. But once separated, the problem becomes much clearer.

For example:

- Was the plan wrong?
- Did the tool action fail?
- Was the result read incorrectly?

Debugging and evaluation become possible only when these are distinguished.

So the plan/action/observation split is not just a theoretical distinction. It is a distinction for real operation and evaluation.

## Stop conditions that end repetition

Because an AI agent is a repeated structure, the system must decide in advance when it has enough evidence to stop and when it should move to human review.

Without a stopping criterion:

- the same search may repeat indefinitely
- extra actions may continue even after enough evidence exists
- cost and time can increase unnecessarily

Stop conditions are usually connected to:

- goal achievement
- enough evidence
- retry limit exceeded
- stop caused by permission or error

In other words, a stop condition is directly connected not only to agent quality, but also to cost and safety.

## Plan errors, action failures, and misread observations

Agent loops are powerful, but they also have many failure points.

- The plan can be unrealistic.
- The wrong tool can be selected.
- The observation can be misread.
- The loop can continue when it should stop.

So agent design usually brings `more freedom` together with `more need for control`.

## A loop that branches again after observation

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s02-plan-action-loop-en.mmd"
```

The key point of this diagram is that an AI agent is not a straight-line pipeline. It is a loop that can return to the next plan after observation, stop when enough evidence exists, or hand work to human review.

## Cases and examples

### Case 1. Document-research agent

A user may ask, `summarize the changes in last month's refund policy`, but the first search result may show only old notices. In this case, it is easy to feel that since the first search is done, the system can immediately move to summarization. But when people dislike the first result, they usually change search terms or restrict the date again. The agent should also change search terms or apply a date filter again based on the observation that `the result is insufficient`. For example, if the first search for `refund policy` is too broad, the next step may add a month range or words such as `notice` and `revision`.

If the system summarizes only old documents as they are, the answer may read smoothly but still guide the user with an old standard rather than last month's. The summarization stage should open only after enough documents are collected, so the next plan is always changed by the previous observation result. The misunderstanding to pass here is the automatic feeling that `once search happened, summary comes next`. The result to check in this case is whether search terms and date conditions are actually adjusted after the first search failure, whether the summary stage opens only after that, and whether the reason for replanning remains in the loop record.

### Case 2. Coding agent

When a user asks for a bug fix, the agent first changes the related file and runs tests. Even if the first patch fails, it is easy to think, `the original plan was right, so maybe it just needs to be pushed a little further`. But in manual debugging, people read the test log and change the next fix direction when a test fails. For example, if the old error disappears after the first fix but another authentication test breaks, the next action should adjust the patch based on the new failure, not repeat the original code explanation. Ignoring this log and pushing only the first plan can make the result worse by fixing one bug and creating another regression.

The criterion changes from focusing only on `was the first plan right` to checking `does the test log that just appeared change the next action`. In an agent, the failure log becomes a new observation result and changes the next patch direction. In other words, `fix -> run -> read failure -> fix again` is a typical practical case of the plan-action-observation loop. The result to check in this case is whether the next fix actually changes based on the new test log when the first patch fails, instead of repeating the same explanation, and whether the reason for that change remains in the loop record.

### Case 3. Scheduling assistant agent

A user may ask, `schedule a 30-minute meeting tomorrow afternoon`, but a calendar lookup may show no open slot. In this case, it is easy to think, `the request cannot be done, so maybe it just ends with failure`. But people usually do not end with simple failure. They look for another time range or ask whether the attendee scope can be reduced. The agent should also propose another time range or ask the user whether to reduce the attendee scope instead of trying to book as is. If it pushes the booking even though there is no open slot, it can leave only a double booking or a failed response.

The criterion changes from `does it directly execute the first goal` to `does it ask again or propose an alternative according to the observation result`. Because one observation result changes the next action, this task is better understood as a loop structure than as a fixed pipeline. The result to check in this case is whether the agent opens a real next action such as proposing an alternate time or asking a follow-up question after observing that no slot exists, instead of ending with failure, and whether this transition is also connected to a stop condition or human confirmation condition.

The three cases can be grouped again by loop-transition criteria as follows. This table does not add a new classification. It compresses the earlier stories into `which observation changes the next decision`.

| Situation | Observation that keeps the loop running | Observation that stops or changes the loop |
| --- | --- | --- |
| Document-research agent | There is room to find a more current document | Enough current evidence exists, or conflicting documents are found |
| Coding agent | A new test failure remains | Tests pass, or human review is needed |
| Scheduling assistant agent | More alternate time ranges can be searched | No open slot remains, so the user must be asked again |

## Scenes that need loop-branching judgment

The easiest thing to miss when first reading a plan-action-observation loop is remembering only that `the loop runs`, without connecting what actually separates `continue`, `stop`, and `move to human review`. In practice, that branching criterion is exactly what prevents both infinite repetition and premature stopping.

| If this scene appears | What to check first | Why this criterion is needed first |
| --- | --- | --- |
| The first attempt failed, but the same action keeps repeating | Does the new observation result actually change the next plan? | If observation cannot change the plan, the loop becomes repeated error, not a real loop. |
| Evidence is sufficient, but search or execution keeps going | Is the stop condition clearly set? | Without a stopping criterion, cost and time grow while quality can become blurrier. |
| Evidence conflicts or permission trouble appears, but the system forces an answer | Are human-review or handoff criteria visible? | Not every loop should settle automatically, so safe stop conditions are needed. |

The criterion to learn first is simple. An AI agent loop is not merely `a structure that keeps running`. It should include the branching structure that `changes the next plan based on observation`, `stops when enough`, and `hands off to a person when risky`.

Seen again as a loop-branching structure, the same idea can be read like this.

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s02-loop-decision-flow-en.mmd"
```

The key point is that the flow does not end immediately after `action`. It passes through `observation and decision`, then either returns to the next loop or stops.

## Practice and example

The goal of the example is not to implement a whole agent framework. What we check here is which observations create continued exploration, stopping, or human review when plan, action, observation, and decision remain as records across several rounds.

The example below uses the observation-log CSV [p6-14-2-agent-loop-observations.csv](/AiBook/assets/part-06/chapter-14/p6-14-2-agent-loop-observations.csv){ .csv-preview }. One row is a record left by the agent in one round of one goal. The `has_current_context`, `evidence_sufficient`, `conflict_found`, `approval_needed`, `action_failed`, `retry_count`, and `retry_limit` columns are signals that change the next decision. If these values change, the final decision can change among `continue_refine`, `stop_ready`, and `human_review` even for the same goal.

In the code, an Ollama model reads the observation log and first proposes a next-plan candidate. Before running it, run `ollama pull qwen2.5:1.5b`, and make sure Ollama is running. To use another model, change the environment variable with a value such as `AIBOOK_OLLAMA_MODEL=model-name`. The prompt sent to the model remains in English. The key point to check in the output is that even when a model proposal exists, the final decision is confirmed again by the guard that checks CSV observation signals and stop conditions.

```python
import csv
import json
import os
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

CSV_PATH = Path("docs/assets/part-06/chapter-14/p6-14-2-agent-loop-observations.csv")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.environ.get("AIBOOK_OLLAMA_MODEL", "qwen2.5:1.5b")

NEXT_PLANS = [
    "refine_or_retry_search",
    "collect_more_evidence",
    "summarize_and_stop",
    "ask_human_review",
    "retry_with_changed_step",
]

def as_bool(value):
    return value.strip().lower() == "true"

def guard_decision(row):
    retry_count = int(row["retry_count"])
    retry_limit = int(row["retry_limit"])

    # The final decision is confirmed again from observation signals and stop conditions, not from the model proposal alone.
    if as_bool(row["approval_needed"]) or as_bool(row["conflict_found"]):
        return "human_review"
    if as_bool(row["action_failed"]) and retry_count >= retry_limit:
        return "human_review"
    if as_bool(row["evidence_sufficient"]) and not as_bool(row["action_failed"]):
        return "stop_ready"
    return "continue_refine"

def plan_to_decision(plan):
    if plan == "ask_human_review":
        return "human_review"
    if plan == "summarize_and_stop":
        return "stop_ready"
    return "continue_refine"

def build_prompt(row):
    labels = "\n".join(f"- {label}" for label in NEXT_PLANS)
    return f"""
You are proposing the next plan for a small LLM AI agent loop.
Return exactly one label and no explanation.

Allowed labels:
{labels}

Goal: {row["goal"]}
Current planned step: {row["planned_step"]}
Observation: {row["observation_signal"]}
Signals:
- has_current_context: {row["has_current_context"]}
- evidence_sufficient: {row["evidence_sufficient"]}
- conflict_found: {row["conflict_found"]}
- approval_needed: {row["approval_needed"]}
- action_failed: {row["action_failed"]}
- retry_count: {row["retry_count"]}
- retry_limit: {row["retry_limit"]}
""".strip()

def ask_model_for_plan(row):
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [{"role": "user", "content": build_prompt(row)}],
        "options": {"temperature": 0},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        return {"model_plan": None, "model_raw": error.__class__.__name__}

    raw = result["message"]["content"].strip()
    plan = next((label for label in NEXT_PLANS if label in raw), None)
    return {"model_plan": plan, "model_raw": raw[:80]}

rows = []
with CSV_PATH.open(encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file):
        row["round"] = int(row["round"])
        row["guard_decision"] = guard_decision(row)
        model_hint = ask_model_for_plan(row)
        row["model_plan"] = model_hint["model_plan"]
        row["model_raw"] = model_hint["model_raw"]
        row["model_plan_decision"] = (
            plan_to_decision(row["model_plan"])
            if row["model_plan"]
            else "model_unavailable"
        )
        row["guard_changed_model_plan"] = row["model_plan_decision"] != row["guard_decision"]
        rows.append(row)

by_case = defaultdict(list)
for row in rows:
    by_case[row["case_id"]].append(row)

final_rows = []
decision_changes = []
for case_id, case_rows in by_case.items():
    ordered = sorted(case_rows, key=lambda item: item["round"])
    final_rows.append(ordered[-1])
    for before, after in zip(ordered, ordered[1:]):
        if before["guard_decision"] != after["guard_decision"]:
            decision_changes.append(
                {
                    "case_id": case_id,
                    "from_round": before["round"],
                    "to_round": after["round"],
                    "from": before["guard_decision"],
                    "to": after["guard_decision"],
                    "signal": after["observation_signal"],
                    "model_plan": after["model_plan"],
                }
            )

round_summary = {
    round_number: dict(Counter(row["guard_decision"] for row in rows if row["round"] == round_number))
    for round_number in sorted({row["round"] for row in rows})
}
final_summary = Counter(row["guard_decision"] for row in final_rows)
model_plan_summary = Counter(row["model_plan"] or "model_unavailable" for row in rows)

print("[model]")
print(
    {
        "model": OLLAMA_MODEL,
        "model_hint_count": sum(row["model_plan"] is not None for row in rows),
        "guard_changed_model_plan_count": sum(row["guard_changed_model_plan"] for row in rows),
    }
)
print("[round summary]")
print(round_summary)
print("[final decisions]")
print(dict(final_summary))
print("[model plan counts]")
print(dict(model_plan_summary))
print("[decision changes]")
for item in decision_changes[:8]:
    print(item)
print("[sample guard checks]")
for row in rows[:8]:
    print(
        {
            "case_id": row["case_id"],
            "round": row["round"],
            "signal": row["observation_signal"],
            "model_plan": row["model_plan"],
            "guard_decision": row["guard_decision"],
            "changed": row["guard_changed_model_plan"],
        }
    )
```

The example output can be read like this.

```text
[model]
{'model': 'qwen2.5:1.5b', 'model_hint_count': 36, 'guard_changed_model_plan_count': 15}
[round summary]
{1: {'continue_refine': 13, 'human_review': 2, 'stop_ready': 1}, 2: {'continue_refine': 8, 'human_review': 2, 'stop_ready': 2}, 3: {'stop_ready': 3, 'human_review': 5}}
[final decisions]
{'stop_ready': 6, 'human_review': 9, 'continue_refine': 1}
[model plan counts]
{'refine_or_retry_search': 24, 'summarize_and_stop': 12}
[decision changes]
{'case_id': 'policy-01', 'from_round': 2, 'to_round': 3, 'from': 'continue_refine', 'to': 'stop_ready', 'signal': 'sufficient current evidence', 'model_plan': 'summarize_and_stop'}
{'case_id': 'policy-02', 'from_round': 1, 'to_round': 2, 'from': 'continue_refine', 'to': 'human_review', 'signal': 'conflicting effective dates', 'model_plan': 'refine_or_retry_search'}
{'case_id': 'policy-03', 'from_round': 2, 'to_round': 3, 'from': 'continue_refine', 'to': 'human_review', 'signal': 'no current source after retry', 'model_plan': 'refine_or_retry_search'}
{'case_id': 'policy-04', 'from_round': 2, 'to_round': 3, 'from': 'continue_refine', 'to': 'stop_ready', 'signal': 'sufficient current evidence', 'model_plan': 'summarize_and_stop'}
{'case_id': 'code-01', 'from_round': 1, 'to_round': 2, 'from': 'continue_refine', 'to': 'stop_ready', 'signal': 'tests pass with notes', 'model_plan': 'summarize_and_stop'}
{'case_id': 'code-02', 'from_round': 2, 'to_round': 3, 'from': 'continue_refine', 'to': 'human_review', 'signal': 'permission-sensitive change', 'model_plan': 'refine_or_retry_search'}
{'case_id': 'code-04', 'from_round': 2, 'to_round': 3, 'from': 'continue_refine', 'to': 'human_review', 'signal': 'retry limit reached', 'model_plan': 'refine_or_retry_search'}
{'case_id': 'schedule-01', 'from_round': 2, 'to_round': 3, 'from': 'continue_refine', 'to': 'human_review', 'signal': 'user confirmation needed', 'model_plan': 'refine_or_retry_search'}
[sample guard checks]
{'case_id': 'policy-01', 'round': 1, 'signal': 'old notice only', 'model_plan': 'refine_or_retry_search', 'guard_decision': 'continue_refine', 'changed': False}
{'case_id': 'policy-01', 'round': 2, 'signal': 'current notice found', 'model_plan': 'summarize_and_stop', 'guard_decision': 'continue_refine', 'changed': True}
{'case_id': 'policy-01', 'round': 3, 'signal': 'sufficient current evidence', 'model_plan': 'summarize_and_stop', 'guard_decision': 'stop_ready', 'changed': False}
{'case_id': 'policy-02', 'round': 1, 'signal': 'current notice found', 'model_plan': 'summarize_and_stop', 'guard_decision': 'continue_refine', 'changed': True}
{'case_id': 'policy-02', 'round': 2, 'signal': 'conflicting effective dates', 'model_plan': 'refine_or_retry_search', 'guard_decision': 'human_review', 'changed': True}
{'case_id': 'policy-03', 'round': 1, 'signal': 'old notice only', 'model_plan': 'refine_or_retry_search', 'guard_decision': 'continue_refine', 'changed': False}
{'case_id': 'policy-03', 'round': 2, 'signal': 'still no current notice', 'model_plan': 'refine_or_retry_search', 'guard_decision': 'continue_refine', 'changed': False}
{'case_id': 'policy-03', 'round': 3, 'signal': 'no current source after retry', 'model_plan': 'refine_or_retry_search', 'guard_decision': 'human_review', 'changed': True}
```

The first thing to notice is that although model proposals appeared for all 36 observation logs, the guard did not use those proposals as the final decision in 15 cases. In other words, the core of P6-15.2 is not the fact that a model can speak a next-plan candidate. It is that multiround observation signals and stop conditions branch that candidate again into `continue_refine`, `stop_ready`, and `human_review`. For example, in round 2 of `policy-01`, the model proposed `summarize_and_stop`, but because `evidence_sufficient` is still `false` in the CSV, the guard keeps the decision at `continue_refine`. Conversely, in round 2 of `policy-02`, even if the model suggests continued exploration, `conflict_found` is `true`, so the guard moves the case to `human_review`.

The next thing to see is that final decisions are not evenly balanced. Among 16 goals, 6 settle as `stop_ready` after enough evidence is collected, 9 move to `human_review` because of conflict, approval, or retry limits, and 1 remains in continued exploration. Real AI agent loops also do not always divide neatly into three directions. What matters is whether the record lets us follow which observation signal separated the model proposal from the guard's final decision.

![AI agent loop decision branching](/AiBook/assets/part-06/chapter-14/agent-loop-decision-split-en.png)

This chart shows how decisions move as rounds progress. In round 1, most cases are `continue_refine`. But in rounds 2 and 3, some stop after gaining enough evidence, while others move to human review because of conflicts or approval boundaries. So the chart is not about balanced decision counts. It shows that as observation logs accumulate, the loop does not leave only continued progress; stopping and human review actually split out.

The result to check in this example is whether we can avoid treating an AI agent loop as magic and instead separately record `what it planned`, `what it did`, `what it observed`, `what it will do next`, and `where it stops or hands work to a person`.

The output is created from the following conditions. These columns are also the values readers can edit directly in the CSV.

| CSV column or condition | Effect on final decision | What to observe when changing it |
| --- | --- | --- |
| `approval_needed == true` | `human_review` is chosen before automatic progress. | Check whether a goal with an approval boundary moves to human review in the final decision. |
| `conflict_found == true` | `human_review` is chosen even if evidence exists. | Check whether conflicting documents prevent settlement by enough evidence alone. |
| `action_failed == true` and `retry_count >= retry_limit` | `human_review` is chosen because the retry limit is exceeded. | Check whether increasing `retry_limit` leaves the same failure in continued exploration. |
| `evidence_sufficient == true` and there is no action failure | `stop_ready` is chosen. | Check whether unnecessary extra exploration decreases in rounds where the enough-evidence signal is on. |
| None of the above conditions match | The decision remains `continue_refine`. | Check whether insufficient observation moves to the next round instead of forcing the same conclusion. |
| `model_plan` | It is recorded as a next-plan candidate, but does not replace the final decision. | Check cases where the guard changes a model stop proposal into continued exploration or human review. |

This condition table makes clearer what the plan-action-observation loop directly solves and what should be passed to a separate level.

| Situation | What the plan-action-observation loop directly handles | What should be passed to later sections |
| --- | --- | --- |
| The goal does not settle in one step | Whether to continue, stop, or hand off to a person | How tools and resources should be exposed in a shared format |
| The same action repeats | Stop conditions and retry conditions | Trace storage, replay, approval-history management |

The key point of this table is that the loop is the level that handles `the structure of the next judgment`. MCP organizes how the tools and resources used by this loop are exposed in a shared format, and a harness organizes how the same loop is left as trace and replay.

## Where observation logs change the next decision

This example shows that an AI agent is not an automatic executor that always goes all the way to the end. It is a branching structure that must separate `continue`, `stop`, and `human review` based on observation results. A good AI agent loop is therefore not a loop that moves a lot, but a loop whose next decision changes when the observation signal changes.

Readers can try these adjustments in the example.

- Change `retry_limit` from 2 to 3 in the CSV and see whether a case that moved to human review because of retry limit stays in continued exploration.
- Change `conflict_found` to `true` and see whether human review is chosen first even when there is enough evidence.
- Change `evidence_sufficient` to `true` and see whether additional exploration changes into stopping.
- Change `approval_needed` to `true` and see whether human confirmation is chosen before automatic progress.
- Change the prompt's allowed labels or `AIBOOK_OLLAMA_MODEL` and see how the gap between model plan candidates and guard final decisions changes.

The more important point to hold is that `producing one answer` and `choosing the next action again based on observation results` are not the same problem. So plan, action, and observation are not extra terms for explaining agents. They are better read as the basic loop that makes us decide where repeated execution continues and where it stops.

## Checklist

- You should be able to explain plan, action, and observation respectively as `next-step decision`, `actual execution`, and `reading the result`.
- You should be able to say that loop quality includes not only execution success, but also `when to continue, when to stop, and when to hand over to a person`.
- You should know that loop explanations continue into the problems of connection rules and execution environments.

## Sources and Further Reading

- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-07-19.
- OpenAI, [Agents SDK](https://developers.openai.com/api/docs/guides/agents){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
