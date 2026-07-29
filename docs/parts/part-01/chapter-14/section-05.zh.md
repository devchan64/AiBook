# P1-14.5 harness 与评估执行环境

> Section ID: `P1-14.5`
> Version: `v2026.07.26`

在 P1-14.4 中，我们把 MCP 看成标准化 AI 应用连接外部工具与数据的协议。接下来问题会更偏向实务：

> 模型可以被调用。  
> 工具也能接进来。  
> agent 能把多个步骤串起来。  
>
> 那么，怎样确认这次执行真的成功了？

这个问题正是 `harness` 的起点。

这个词原本会让人想到一种把力量固定、束住、导向特定用途的装置。在软件里，它自然延伸成 `test harness` 这样的用法，也就是：在受控条件下运行被测系统(system under test)，并检查结果。

在 AI 服务语境里，这种直觉可以进一步扩展为：把模型调用、工具调用、状态变化、日志、评估标准都包进同一套执行环境。

> harness 是一种装置：它把模型与工具放进真实工作流里，使过程可以被记录、结果可以被验证、重复评估成为可能。

这里不会把 harness 当作某个产品名，而是把它限定成更窄的意思：

> 一种包裹 agent 执行的装置，  
> 让它可以被观察、验证、评估。

这一节会围绕 `harness`、`trace`、`log`、`evaluation`、`grader`、`reproducibility` 来整理：执行为什么会变得可观察、可比较。它承接 14.3 的 agent 结构和 14.4 的 MCP 连接，而把成本与运维约束留到 14.6。

这里说明 `harness`、`trace`、`log`、`evaluation`、`grader` 的基本作用。成本(cost)、延迟(latency)、运维(operation)约束会在 P1-14.6 再讨论。这里先集中处理 `怎样让 agent 执行变得可观察、可比较` 这个问题。

`harness`、`trace`、`log`、`evaluation`、`grader`、`reproducibility` 是不同的执行验证要素。它们的角色可以先分成下面这样：

| 术语 | 极简含义 | 本节中的作用 |
| --- | --- | --- |
| harness | 把执行包起来、使之可观察的装置 | 本节的中心概念 |
| trace | 一次请求的逐步执行记录 | 帮助定位“哪里发生了什么” |
| log | 之后还能回看的记录 | 责任与复现的基础 |
| evaluation | 按标准比较结果的过程 | 判断是否真的改进 |
| grader | 把评估标准变成可执行形式 | 自动比较的工具 |
| reproducibility | 在相同条件下可再次检查的性质 | 回归检查与重复验证的前提 |

这里先把 `harness 负责包裹执行`、`trace 与 log 负责留下记录`、`evaluation 负责建立比较标准` 作为基准线。

| 主题 | 本节要问的问题 |
| --- | --- |
| harness | 为什么必须把执行包起来？ |
| trace | 哪些步骤按什么顺序执行了？ |
| log | 事后必须能回看哪些信息？ |
| evaluation | 怎样比较结果是不是真的变好了？ |
| reproducibility | 同样条件下能不能再次确认？ |

## 分离评估执行环境的基准

- 把 harness 理解成包裹执行的环境，而不是模型本身。
- 把这个词的原始直觉和软件里的 test harness 联系起来。
- 理解为什么 agent 与工具工作流需要 trace 与 log。
- 把 evaluation 理解成基于标准、数据集(dataset)、grader、重复运行的比较，而不是模糊感觉。
- 区分调试(debugging)、回归检查(regression checking)、改进循环(improvement loop)。
- 理解“偶尔答对一次”和“反复稳定工作”并不是同一种状态。

## 三个基准

这里希望避免把 harness 误读成产品名或新的 AI 能力。阅读正文时要抓住的三个基准是：

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| harness 包裹执行，而不是增加另一种 AI 能力 | 这能防止把 harness 误当成模型能力。 | 只要理解成它会把执行绑起来、记录下来、校验起来即可。 |
| agent 执行需要 trace 与 log | 这能让事后回看与修改成为可能。 | 只要理解成步骤顺序和各步结果必须被保留下来即可。 |
| 一次成功与反复稳定成功是不同状态 | 这能说明为什么 evaluation 必不可少。 | 只要理解成重要的不是偶然成功，而是可重复验证即可。 |

## 为什么 harness 这个词合适

harness 并不制造力量。它更像是把已有的力量固定、连接、导向可安全使用的方式。词源解释也会把它和装备、准备、以及对力量的可控使用联系起来。如果这个直觉丢掉了，就很容易把 AI 里的 harness 误当成模型本身或某种新算法。

> 物理世界中的 harness：  
> 不制造力量，而是固定并连接力量。
>
> test harness：  
> 不负责编写代码，而是让代码在受控条件下运行并接受检查。
>
> AI 执行 harness：  
> 不创造模型能力，而是把模型与工具的执行捆成可观察的工作流。

这也是为什么在软件测试里，harness 这个词很自然。被测系统往往无法自己重建真实运行环境，所以 test harness 会提供输入、模拟必要条件，并比较输出与失败。

在 AI agent 里也是类似的。就算 LLM 能生成句子、能调用工具，也还不等于一个完整服务。prompt、context、tool、permission、approval、log、evaluation 需要被一起绑定，才会变成真实工作流。

> 只有模型时：  
> 可以给出答案，但执行条件和责任边界仍很模糊。
>
> 有 harness 时：  
> 输入、工具、中间步骤、输出和评估标准会被绑在一起。

这样理解以后，harness 不是夸大 AI 能力的说法，而是指向一种现实工作所需的约束和观察装置。把它理解成“让力量被安全使用的连接装置”，会比把它理解成“压制力量的装置”更容易跟上。

最近也出现了尝试把这个松散术语更学术化地整理起来的工作。2026 年的一篇 arXiv 预印本，把 harness 的系谱重构成从马具、软件 test harness、机器学习 evaluation harness 再到 agent harness 的连续流。这里不会把那篇材料当成本节的标准定义，而只把它当成说明“为什么这个词在 AI agent 语境里变重要了”的补充背景。

## 相近的词仍需区分

harness 可以和 workflow、pipeline、operations、framework 比较，但它们只是部分重叠，不是同义词。

| 视角 | 中心问题 | 本节中的位置 |
| --- | --- | --- |
| workflow | 工作按什么顺序流动？ | 用来理解 agent 执行步骤顺序 |
| pipeline | 输入经过哪些处理阶段才变成输出？ | 用来理解可重复的处理流 |
| operations | 如何让执行长期稳定、可观察、可改进？ | 理解 harness 的背景视角 |
| framework | 给开发者提供了什么结构和 API？ | 可能包含 harness，或被用来实现 harness |
| harness | 怎样把执行包起来、记录下来、评估起来？ | 本节的中心概念 |

harness 不应简单等同于 DevOps、MLOps、LLMOps，也不等同于“一个 trace 工具 + 一个 log 工具 + 一个 eval 工具”的固定打包。运维视角在这里更像是帮助我们理解为什么需要观察、重复和验证的比较背景。harness 也不一定必须以单独产品包的形式存在。

在某些系统里，一个 agent 会调用另一个 agent，review agent 会检查结果，另一个评估流又会重新检查执行。在这种情况下，harness 更像是一种让执行被连接、被固定、能被验证的模式，而不是一个单独工具名称。

但只是把多个 agent 连起来，并不会自动形成 harness。只有当这种连接真正限制执行条件、保留中间步骤、比较结果、让失败能够再次核查时，才更适合用 harness 的视角去看。

## 为什么必须把执行包起来

简单模型调用相对容易观察：

> 输入  
> -> 模型  
> -> 输出

而 P1-14.3 与 P1-14.4 里看到的 agent 与 MCP 流程会更复杂：

> 用户请求  
> -> 模型调用  
> -> 文档检索  
> -> 查看工具列表  
> -> 工具调用  
> -> 观察结果  
> -> 再次模型调用  
> -> 最终回答

当最后结果出错时，仅仅说“模型错了”已经远远不够。

| 失败原因 | 例子 |
| --- | --- |
| 输入问题 | 错读了用户请求 |
| 检索问题 | 选进来了无关文档 |
| 工具问题 | 给 API 传了错误参数 |
| 状态问题 | 错记了上一步结果 |
| 判断问题 | 错误解读了工具返回 |
| 输出问题 | 无依据断言，或违反格式要求 |

harness 的作用，就是把这些执行一步一步包起来，让系统能看见问题究竟出在哪里。

> 没有被包起来的执行：  
> 只能看见结果。
>
> 被包起来的执行：  
> 输入、检索、工具调用、中间结果、最终输出和错误会一起可见。

## trace 会留下执行流程

`trace` 是一次请求如何一步步走过来的记录。如果说 `log` 是更广义的记录，那么 trace 更接近“这一条请求内部各步骤之间的流与关系”。

OpenAI Agents SDK 文档说明，执行 trace 可以把模型调用、工具调用、handoff、guardrail、custom span 保存成结构化记录。这里不需要把这些产品细节背下来，它们只提供一个通用根据：agent 执行需要步骤级观察。

| trace 目标 | 它帮助回答的问题 |
| --- | --- |
| 模型调用(model call) | 输入了什么？输出了什么？ |
| 检索(retrieval) | 选中了哪份文档？ |
| 工具调用(tool call) | 用什么参数调用了什么工具？ |
| guardrail | 哪条校验或拦截条件被触发？ |
| 错误(error) | 失败发生在哪一步？ |
| 持续时间(duration) | 哪一步耗时很长？ |

假设一个请求是“找到文档、做摘要、然后创建 issue”，结果失败了。

> 失败结果：  
> issue 内容是错的
>
> trace 帮助追问：  
> 取回来的文档对吗？  
> 摘要本身错了吗？  
> issue 创建工具的参数传错了吗？  
> 用户审批被跳过了吗？

trace 不会自动给出正确答案，但它会提供追查原因所需的线索。

## log 让事后说明成为可能

`log` 是执行之后还能再查看的记录。在 AI 服务里，log 不只是给开发者调试看，它也是责任追踪与可复现性的基础。

| 可记录内容 | 为什么要记 |
| --- | --- |
| request id | 便于再次定位某次执行 |
| 输入摘要 | 便于回看当时是什么请求 |
| 使用的模型 | 便于比较模型变更前后差异 |
| 检索到的上下文 | 便于确认用了哪些依据 |
| 工具调用 | 便于确认对外部系统做了什么 |
| 审批记录 | 便于确认是否有人批准过动作 |
| 最终输出 | 便于确认给用户发出了什么 |
| 错误 | 便于分析失败原因 |

当然，日志并不是越多越好。如果它把个人信息、密钥、内部文件或敏感输入原样保留下来，就会造成新的安全问题。所以日志应该做到：`足以事后说明，但又尽量减少危险信息暴露`。

这个问题会继续连到第 15 章关于安全与个人信息的讨论。在这里，只要先记住一点：harness 必须留下记录，但记录本身也同样是设计对象。

## evaluation 不是感觉，而是可重复比较

看到某次输出以后觉得“看起来不错”，可以作为起点；但要把它变成服务，就必须有可重复的 `evaluation`。

评估通常至少包括：

| 元素 | 说明 |
| --- | --- |
| 数据集(dataset) | 一组可以反复测试的输入案例 |
| 期待结果(expected output) | 参考答案、标准答案、或期望属性 |
| grader | 把结果打分或判定通过/失败的标准 |
| eval run | 用同一标准跑多条案例的过程 |
| report | 汇总哪里变好了、哪里变差了 |

OpenAI 的 agent evaluation 资料也建议：先看个别 trace，等到需要重复性时，再转向数据集和反复评估。这个过程不只是产品使用建议，而是 AI 服务改进时普遍需要的思维方式。

> 单个案例检查：  
> 为什么这一次失败了？
>
> 重复评估：  
> 这个改动在多条请求上是否整体提升了表现？

## grader 把评估标准变成可执行形式

`grader` 是把评估标准转成可执行形式的东西。

在传统软件测试里，期待答案往往很明确：

> 输入：`2 + 2`  
> 期待输出：`4`

但在生成式 AI 里，往往不存在唯一标准答案，所以 grader 通常会采用更丰富的标准：

| 评估标准 | 例子 |
| --- | --- |
| 准确性(accuracy) | 回答是否与来源材料一致？ |
| 格式(format) | 是否遵守 JSON 或表格格式？ |
| 有依据性(groundedness) | 是否避免了无依据主张？ |
| 安全性(safety) | 是否避免了禁用动作或敏感信息泄露？ |
| 任务成功(task success) | 是否真的完成了用户请求？ |

grader 也并不完美。很多时候仍然需要人工评审，而自动评估也可能漏掉质量问题。所以更安全的理解是：grader 不是完全替代人的判断，而是帮助反复检查的可重复标准。

## 回归(regression)检查很重要

在软件里，`regression` 指的是新的改动破坏了原本正常工作的功能。AI 服务也会发生类似问题。

> 改了提示词后，回答更友善了，  
> 但来源引用反而更常丢失。

> 换了模型后，总结质量提升了，  
> 但成本和延迟都变高了。

harness 与 evaluation 有助于把这些变化看清楚。

| 改动 | 应该检查什么 |
| --- | --- |
| prompt 修改 | 旧案例上的质量是否还保持住？ |
| 模型替换 | 准确度、成本、延迟怎样变化？ |
| RAG 检索方式改变 | 文档选择是否更好了？ |
| 增加工具 | 错误工具调用是否增加了？ |
| 审批策略调整 | 高风险动作是否仍被拦住？ |

没有这个视角时，AI 服务很容易停留在“今天看起来能用”的状态。对于学习者来说，一旦建立评估标准，也会更容易冷静地检查 AI 输出。

## harness 不能自动解决什么

即使有了 harness，也不代表服务会自动变得安全或正确。

| 它不能自动解决的问题 | 原因 |
| --- | --- |
| 定义好的评估标准 | 什么算“好结果”仍由人决定 |
| 数据集代表性 | 测试案例仍需代表真实请求 |
| 自动评估误判 | grader 本身也可能判断错误 |
| 安全策略 | 日志与工具执行仍需要额外安全设计 |
| 成本与延迟 | trace 与 eval 自身也会消耗资源 |

所以，harness 不是“保证正确答案的装置”，而是“让执行可观察、可改进的装置”。

## Checklist

- 我可以把 harness 解释成包裹执行的环境，而不是模型本身。
- 我可以通过装备、固定、连接、使用这条线索解释 harness 的原始直觉。
- 我可以说明它怎样从 test harness 扩展到 agent harness。
- 我可以说明为什么不应把 harness 和 DevOps、framework 或固定的 trace/log/eval 工具包看成同一个东西。
- 我可以说明为什么 trace 和 log 对理解 agent 执行是必要的。
- 我可以把 evaluation 解释成 dataset、criteria、grader 和 eval run 的组合。
- 我可以说明为什么 prompt、模型、RAG 和工具的变更都要做 regression 检查。
- 我可以说明 harness 不是保证正确答案的装置，而是让观察和改进成为可能的装置。
- 我可以用 `把执行包起来`、`把步骤记下来`、`做重复比较` 这三个角色来说明 harness。

## 出处与参考资料

- Merriam-Webster, [Harness](https://www.merriam-webster.com/dictionary/harness){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-23.
- Online Etymology Dictionary, [Harness](https://www.etymonline.com/word/harness){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-23.
- Sanderson Oliveira de Macedo, [What makes a harness a harness: necessary and sufficient conditions for an agent harness](https://arxiv.org/abs/2606.10106){: target="_blank" rel="noopener noreferrer" }, arXiv preprint, 2026, 确认日期: 2026-06-23.
- OpenAI, [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 确认日期: 2026-07-19.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 确认日期: 2026-07-19.
- OpenAI, [Working with evals](https://developers.openai.com/api/docs/guides/evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 确认日期: 2026-07-19.
