# P6-14.2 分裂为继续、停止和人工审查的 Agent 循环

> Section ID: `P6-14.2`
> Version: `v2026.07.23`

在 P6-14.1 中，我们把 agent 读成一种会根据中间结果改变下一项工作的执行结构。现在需要更具体地看：什么标准会让这个流程继续，在哪里停止，什么时候转向人工审查。

Agent 具有重复结构：根据目标规划下一步，执行实际行动，观察结果，然后选择下一项决策。这里重要的不是循环运行这个事实本身，而是观察结果会分支到哪个方向：`continue`、`stop`、还是 `human review`。

## 重复循环负责什么

这个场景中要收束的问题，是把单个 agent 循环的基本结构读成`计划-行动-观察的重复`，并区分哪里应该继续、哪里应该停止。

工具连接规则和执行环境关注的是循环使用哪些工具和资源，以及什么记录环境保存执行过程。计划-行动-观察循环首先关注的是观察结果如何改变下一项分支和停止判断。

Agent 不应该只停留为抽象概念。它应该被读成 `plan`、`action`、`observation` 反复出现的循环。如果 P6-14.1 看的是多次读取和执行如何作为目标流程继续，那么本节看的是这个流程如何根据中间观察分裂为继续、终止和人工审查。

核心视角会从`多个步骤是否应该继续`变成`这些步骤通过什么观察和决策循环来重复`。

这个阶段要先留下的记录，是显示判断在哪里改变的计划、行动、观察记录，以及显示何时停止、为什么交给人的停止理由和下一步。这些记录让我们之后能缩小循环失败和重试原因。

## 区分计划、行动、观察和停止条件

分开计划、行动、观察和停止条件的理由，不是为了背术语。即使看起来相似的失败，也会因为不稳定点不同而需要不同的下一项决策。

| 观察结果 | 后续决策 | 为什么这样分支 |
| --- | --- | --- |
| 依据仍然不足 | 继续或重新规划 | 系统应该改变搜索词、工具或顺序，而不是重复同一行动。 |
| 依据足够且冲突较小 | 停止 | 更多迭代带来的成本和时间可能大于质量提升。 |
| 文档冲突、权限不足或状态不确定性高 | 转向人工审查或交接 | 高风险场景应作为单独边界留下，而不是自动关闭。 |

先抓住这张表，再阅读下面的 `plan`、`action`、`observation` 和 `stop condition`，会更容易把 agent 循环理解成`下一项行动会根据观察改变的结构`，而不是`持续旋转的结构`。后续定义只是阅读这张分支表所需的最小组件。

## 什么是计划

计划(plan)是决定`现在应该做什么`的阶段。

如果目标是：

`找到并总结最新退款政策`

那么计划阶段可能长这样：

- 先搜索政策文档。
- 先检查最新公告。
- 只提取变更部分。

换句话说，规划意味着把一个目标分成更小的子任务。

## 什么是行动

行动(action)是实际执行某件事的阶段。

示例包括：

- 调用搜索工具
- 读取文件
- 运行计算
- 发起 API 请求

重要的是，行动并不只是`用语言建议下一步`。它是实际影响外部世界或带回真实结果的阶段。

## 什么是观察

观察(observation)是读取行动结果的阶段。

示例包括：

- 搜索结果太稀疏
- 文件不存在
- 计算结果和预期不同
- API 调用失败

没有观察，agent 可能会一直重复同一行动，或者在不知道失败的情况下移动到下一步。

## 为什么要分开计划、行动和观察

读者很容易把这个流程看成一整块。但一旦分开，问题就会清楚很多。

例如：

- 是计划错了吗？
- 是工具行动失败了吗？
- 是结果读错了吗？

只有区分这些，调试和评估才可能进行。

所以计划、行动、观察的分离不只是理论区分。它是实际运行和评估所需的区分。

## 结束重复的停止条件

因为 agent 是重复结构，系统必须预先决定何时已经有足够依据可以停止，何时应该转向人工审查。

如果没有停止标准：

- 同样的搜索可能无限重复
- 即使依据已经足够，也可能继续追加行动
- 成本和时间会不必要地增加

停止条件通常连接到：

- 目标达成
- 依据足够
- 超过重试上限
- 因权限或错误造成的停止

换句话说，停止条件不仅直接关系到 agent 质量，也关系到成本和安全。

## 计划错误、行动失败和误读观察

Agent 循环很强大，但失败点也很多。

- 计划可能不现实。
- 可能选择错误工具。
- 观察可能被误读。
- 应该停止时，循环可能继续。

所以 agent 设计通常会同时带来`更多自由度`和`更多控制需求`。

## 观察后再次分支的循环

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s02-plan-action-loop-zh.mmd"
```

这张图的重点是，agent 不是直线管道。它会在观察之后回到下一次计划，在依据足够时停止，或者把工作交给人工审查。

## 案例和示例

### 案例 1. 文档研究 agent

用户可能要求`总结上个月退款政策的变化`，但第一次搜索结果可能只显示旧公告。这时很容易觉得既然第一次搜索已经完成，系统可以马上进入总结。但人不满意第一条结果时，通常会改变搜索词或重新限制日期。Agent 也应该根据`结果不足`这个观察，改变搜索词或重新应用日期过滤。例如，如果第一次搜索 `refund policy` 过于宽泛，下一步可能加入月份范围，或加入 `notice`、`revision` 等词。

如果系统原样总结旧文档，回答可以读起来很流畅，但仍然用旧标准引导用户，而不是上个月的标准。总结阶段应该只在收集到足够文档后打开，所以下一项计划总是由前一个观察结果改变。这里要越过的误解是`搜索一发生，下一步就自动是总结`。这个案例中要检查的结果，是第一次搜索失败后搜索词和日期条件是否真的被调整，是否只有在那之后才打开总结阶段，以及重新规划的理由是否留在循环记录中。

### 案例 2. 编码 agent

当用户要求修复 bug 时，agent 会先修改相关文件并运行测试。即使第一个补丁失败，也很容易想：`原来的计划是对的，也许再推进一点就行`。但人工调试时，人会读取测试日志，并在测试失败时改变下一次修复方向。例如，如果第一次修复后旧错误消失，但另一个认证测试坏掉，下一项行动应该基于新失败调整补丁，而不是重复原始代码说明。忽略这个日志、只推进第一个计划，可能会修好一个 bug 同时制造另一个回归，使结果更糟。

判断标准从只看`第一个计划是否正确`，变成检查`刚出现的测试日志是否改变下一项行动`。在 agent 中，失败日志会成为新的观察结果，并改变下一次补丁方向。换句话说，`修复 -> 运行 -> 读取失败 -> 再修复`是计划-行动-观察循环的典型实践案例。这个案例中要检查的结果，是第一个补丁失败时，下一次修复是否真的基于新测试日志改变，而不是重复同一说明，并且这个改变理由是否留在循环记录中。

### 案例 3. 日程助理 agent

用户可能要求`明天下午安排一个 30 分钟会议`，但日历查询可能显示没有空档。这时很容易觉得`请求做不了，所以也许只能以失败结束`。但人通常不会只以失败结束。他们会找另一个时间段，或询问是否能减少参会范围。Agent 也应该提出另一个时间段，或询问用户是否缩小参会范围，而不是按原样尝试预订。如果在没有空档的情况下强行推进预订，结果只会留下重复预订或失败响应。

判断标准从`是否直接执行第一个目标`，变成`是否根据观察结果再次询问或提出替代方案`。因为一个观察结果改变了下一项行动，这项任务更适合理解成循环结构，而不是固定管道。这个案例中要检查的结果，是观察到没有空档后，agent 是否打开真正的下一项行动，例如提出备用时间或追问，而不是以失败结束，并且这个转移是否也连接到停止条件或人工确认条件。

三个案例可以按循环转移标准重新分组如下。这张表不是新增分类，而是把前面的叙述压缩成`哪种观察改变下一项决策`。

| 情况 | 让循环继续的观察 | 让循环停止或改变的观察 |
| --- | --- | --- |
| 文档研究 agent | 仍有空间寻找更新文档 | 当前依据足够，或发现文档冲突 |
| 编码 agent | 仍有新的测试失败 | 测试通过，或需要人工审查 |
| 日程助理 agent | 还可以搜索更多备用时间段 | 没有可用空档，必须重新询问用户 |

## 需要循环分支判断的场景

第一次读计划-行动-观察循环时，最容易漏掉的是只记住`循环会运行`，却没有连接到底是什么把`继续`、`停止`、`转向人工审查`分开。实际上，这个分支标准正是防止无限重复和过早停止的关键。

| 如果出现这个场景 | 先检查什么 | 为什么这个标准要先看 |
| --- | --- | --- |
| 第一次尝试失败，但同一行动不断重复 | 新观察结果是否真的改变了下一项计划？ | 如果观察不能改变计划，循环就会变成重复错误，而不是真正的循环。 |
| 依据已经足够，但搜索或执行仍在继续 | 停止条件是否清楚？ | 没有停止标准，成本和时间会上升，质量反而可能变模糊。 |
| 依据冲突或权限问题出现，但系统强行给出答案 | 人工审查或交接标准是否可见？ | 不是每个循环都应该自动关闭，所以需要安全停止条件。 |

首先要学会的标准很简单。Agent 循环不只是`持续运行的结构`。它应该包含这样的分支结构：`根据观察改变下一项计划`、`足够时停止`、`有风险时交给人`。

再看成循环分支结构，同一个想法可以这样读。

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s02-loop-decision-flow-zh.mmd"
```

关键点是，流程不会在 `action` 后立刻结束。它会经过 `observation and decision`，然后回到下一轮循环或停止。

## 练习和示例

这个示例的目标不是实现完整 agent 框架。这里检查的是，当计划、行动、观察和决策作为多轮记录留下时，哪些观察会产生继续探索、停止或人工审查。

下面的示例使用观察日志 CSV [p6-14-2-agent-loop-observations-zh.csv](/AiBook/assets/part-06/chapter-14/p6-14-2-agent-loop-observations-zh.csv){ .csv-preview }。一行是 agent 在一个目标的一轮中留下的记录。`has_current_context`、`evidence_sufficient`、`conflict_found`、`approval_needed`、`action_failed`、`retry_count`、`retry_limit` 列是会改变下一项决策的信号。如果这些值改变，即使是同一个目标，最终决策也可能在 `continue_refine`、`stop_ready`、`human_review` 之间变化。

代码中，Ollama 模型读取观察日志，并先提出下一项计划候选。运行前先执行 `ollama pull qwen2.5:1.5b`，并确认 Ollama 正在运行。若要使用其他模型，可以把环境变量改成 `AIBOOK_OLLAMA_MODEL=model-name` 这样的值。传给模型的 prompt 保持英文。输出中要检查的重点是，即使存在模型提议，最终决策仍会由检查 CSV 观察信号和停止条件的 guard 再次确认。

```python
import csv
import json
import os
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

CSV_PATH = Path("docs/assets/part-06/chapter-14/p6-14-2-agent-loop-observations-zh.csv")
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
You are proposing the next plan for a small LLM agent loop.
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

示例输出可以这样读。

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

首先要注意，36 条观察日志中都出现了模型建议，但 guard 在 15 条中没有把该建议用作最终决策。换句话说，P6-14.2 的核心不是模型可以说出下一项计划候选，而是多轮观察信号和结束条件会把这个候选再次分成 `continue_refine`、`stop_ready`、`human_review`。例如在 `policy-01` 的第 2 轮，模型提出 `summarize_and_stop`，但 CSV 中的 `evidence_sufficient` 仍然是 `false`，所以 guard 把决策维持为 `continue_refine`。相反，在 `policy-02` 的第 2 轮，即使模型建议继续探索，`conflict_found` 是 `true`，所以 guard 会把案例转到 `human_review`。

接着要看的是，最终决策并不会平均分布。16 个目标中，6 个在收集到足够依据后以 `stop_ready` 关闭，9 个因为冲突、批准或重试上限转向 `human_review`，还有 1 个留在继续探索中。真实 agent loop 也并不总是整齐地分成三个方向。重要的是，记录是否能让我们追踪哪一个观察信号分开了模型建议和 guard 最终决策。

![agent loop 决策分支](/AiBook/assets/part-06/chapter-14/agent-loop-decision-split-zh.png)

这张图显示轮次推进时决策如何移动。第 1 轮中，大多数案例是 `continue_refine`。但在第 2 轮和第 3 轮，一部分案例因为获得足够依据而停止，另一部分因为冲突或批准边界转向人工审查。因此，这张图不是为了展示均衡的决策数量。它显示的是，随着观察日志累积，循环不会只剩下继续推进，而会实际分裂出停止和人工审查。

这个示例中要确认的结果，是我们能否不把 agent loop 当成魔法，而是分别记录`计划了什么`、`执行了什么`、`观察到了什么`、`接下来要做什么`、`在哪里停止或交给人`。

输出由以下条件产生。这些列也是读者可以在 CSV 中直接修改的值。

| CSV 列或条件 | 对最终决策的影响 | 修改时要观察什么 |
| --- | --- | --- |
| `approval_needed == true` | 自动推进之前会先选择 `human_review`。 | 确认带有批准边界的目标是否在最终决策中转向人工审查。 |
| `conflict_found == true` | 即使存在依据，也会选择 `human_review`。 | 确认冲突文档是否阻止系统只靠足够依据关闭。 |
| `action_failed == true` and `retry_count >= retry_limit` | 因为超过重试上限，会选择 `human_review`。 | 确认提高 `retry_limit` 后，同一失败是否会留在继续探索中。 |
| `evidence_sufficient == true` and there is no action failure | 会选择 `stop_ready`。 | 确认足够依据信号打开的轮次中，不必要的追加探索是否减少。 |
| 不符合以上条件 | 决策会保持为 `continue_refine`。 | 确认不足的观察是否移动到下一轮，而不是强行得出同一结论。 |
| `model_plan` | 记录为下一项计划候选，但不会替代最终决策。 | 查看 guard 把模型的停止建议改成继续探索或人工审查的案例。 |

这张条件表让 plan-action-observation loop 直接解决的事，以及应该交给其他层位的事更清楚。

| 情况 | Plan-action-observation loop 直接处理什么 | 应该交给后续章节什么 |
| --- | --- | --- |
| 目标不能在一步内关闭 | 是否继续、停止或交给人 | 如何用共享格式暴露工具和资源 |
| 同一行动重复出现 | 停止条件和重试条件 | trace 存储、replay、批准历史管理 |

这张表的核心是，loop 是处理`下一项判断结构`的层位。MCP 会整理这个 loop 使用的工具和资源如何以共享格式暴露，harness 会整理同一个 loop 如何留下 trace 和 replay。

## 观察日志改变下一项决策的位置

这个示例显示，agent 不是总会自动执行到最后的执行器。它是一种分支结构，必须根据观察结果区分`继续`、`停止`和`人工审查`。好的 agent loop 不是移动很多的循环，而是观察信号变化时下一项决策也会变化的循环。

读者可以在示例中尝试这些调整。

- 在 CSV 中把 `retry_limit` 从 2 改成 3，观察因重试上限进入人工审查的案例是否会留在继续探索中。
- 把 `conflict_found` 改成 `true`，观察即使有足够依据，是否也会优先选择人工审查。
- 把 `evidence_sufficient` 改成 `true`，观察追加探索是否会变成停止。
- 把 `approval_needed` 改成 `true`，观察自动推进前是否会选择人工确认。
- 改变 prompt 的允许标签或 `AIBOOK_OLLAMA_MODEL`，观察模型计划候选和 guard 最终决策之间的差距如何变化。

更重要的是要抓住：`产出一个回答`和`根据观察结果重新选择下一项行动`不是同一个问题。因此，计划、行动、观察不是解释 agent 的额外术语。它们更适合读成决定重复执行在哪里继续、在哪里停止的基本循环。

## 检查清单

- 你应该能够把 plan、action、observation 分别说明成`下一步决策`、`实际执行`、`读取结果`。
- 你应该能够说出 loop 质量不仅包括执行成功，还包括`何时继续、何时停止、何时交给人`。
- 你应该知道，loop 说明会继续进入连接规则和执行环境的问题。

## 参考资料

- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-07-19.
- OpenAI, [Agents SDK](https://developers.openai.com/api/docs/guides/agents){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
