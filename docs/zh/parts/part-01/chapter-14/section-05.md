# P1-14.5 harness 与评估执行环境

> Section ID: `P1-14.5`
> Version: `v2026.07.09`

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

## 本节范围

这里说明 `harness`、`trace`、`log`、`evaluation`、`grader` 的基本作用。会涉及这个词从原始直觉到软件 test harness，再到 AI 执行 harness 的延伸，但不会深入讨论 `agent harness` 的严格学术定义争论。具体 SDK 代码、仪表盘用法、评估 API 实现与大规模运维成本不在当前范围内；成本、延迟、运维会在 P1-14.6 再接着讨论。

| 术语 | 极简含义 | 本节中的作用 |
| --- | --- | --- |
| harness | 把执行包起来、使之可观察的装置 | 本节的中心概念 |
| trace | 一次请求的逐步执行记录 | 帮助定位“哪里发生了什么” |
| log | 之后还能回看的记录 | 责任与复现的基础 |
| evaluation | 按标准比较结果的过程 | 判断是否真的改进 |
| grader | 把评估标准变成可执行形式 | 自动比较的工具 |
| reproducibility | 在相同条件下可再次检查的性质 | 回归检查与重复验证的前提 |

这里先把 `harness 负责包裹执行`、`trace 与 log 负责留下记录`、`evaluation 负责建立可重复比较标准` 作为基准线。

## 本节目标

- 把 harness 理解成包裹执行的环境，而不是模型本身。
- 把这个词的原始直觉和软件里的 test harness 联系起来。
- 理解为什么 agent 与工具工作流需要 trace 与 log。
- 把 evaluation 理解成基于标准、数据集(dataset)、grader、重复运行的比较，而不是模糊感觉。
- 区分调试(debugging)、回归检查(regression checking)、改进循环(improvement loop)。
- 理解“偶尔答对一次”和“反复稳定工作”并不是同一种状态。

## 三个基准

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| harness 包裹执行，而不是增加另一种 AI 能力 | 这能防止把 harness 误当成模型能力。 | 只要理解成它会把执行绑起来、记录下来、校验起来即可。 |
| agent 执行需要 trace 与 log | 这能让事后回看与修改成为可能。 | 只要理解成步骤顺序和各步结果必须被保留下来即可。 |
| 一次成功与反复稳定成功是不同状态 | 这能说明为什么 evaluation 必不可少。 | 只要理解成重要的不是偶然成功，而是可重复验证即可。 |

## 为什么 harness 这个词合适

harness 并不制造力量。它更像是把已有的力量固定、连接、导向可安全使用的方式。这个直觉很自然地延伸到了软件，再延伸到 AI 执行。

> 物理世界中的 harness：  
> 不制造力量，而是固定并连接力量。
>
> test harness：  
> 不负责编写代码，而是让代码在受控条件下运行并接受检查。
>
> AI 执行 harness：  
> 不创造模型能力，而是把模型与工具的执行捆成可观察的工作流。

所以，harness 不应被理解成模型本身，也不应被理解成某种新算法。它更接近一种使模型工作变得可检查的执行环境。

## 相近的词仍需区分

harness 可以和 workflow、pipeline、operations、framework 比较，但它们只是部分重叠，不是同义词。

| 视角 | 中心问题 | 本节中的位置 |
| --- | --- | --- |
| workflow | 工作按什么顺序流动？ | 用来理解 agent 执行步骤顺序 |
| pipeline | 输入经过哪些处理阶段才变成输出？ | 用来理解可重复的处理流 |
| operations | 如何让执行长期稳定、可观察、可改进？ | 理解 harness 的背景视角 |
| framework | 给开发者提供了什么结构和 API？ | 可能包含 harness，或被用来实现 harness |
| harness | 怎样把执行包起来、记录下来、评估起来？ | 本节的中心概念 |

harness 不应简单等同于 DevOps、MLOps、LLMOps，也不等同于“一个 trace 工具 + 一个 log 工具 + 一个 eval 工具”的固定打包。

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

## trace 会留下执行流程

`trace` 是一次请求如何一步步走过来的记录。如果说 `log` 是更广义的记录，那么 trace 更接近“这一条请求内部各步骤之间的流与关系”。

| trace 目标 | 它帮助回答的问题 |
| --- | --- |
| 模型调用(model call) | 输入了什么？输出了什么？ |
| 检索(retrieval) | 选中了哪份文档？ |
| 工具调用(tool call) | 用什么参数调用了什么工具？ |
| guardrail | 哪条校验或拦截条件被触发？ |
| 错误(error) | 失败发生在哪一步？ |
| 持续时间(duration) | 哪一步耗时很长？ |

trace 不会自动给出正确答案，但它能提供找原因的线索。

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

当然，日志并不是越多越好。如果它把个人信息、密钥、内部文件或敏感输入原样保留下来，就会造成新的安全问题。

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

这会把问题从：

> 为什么这一次失败了？

转成：

> 这个改动是否在多组请求上整体改善了表现？

## grader 把评估标准变成可执行形式

`grader` 是把评估标准变成可以执行的形式。

在传统软件测试里，答案往往很明确：

> 输入：`2 + 2`  
> 期待输出：`4`

但在生成式 AI(generative AI)里，往往不存在唯一标准答案，所以 grader 往往要使用更丰富的标准：

| 评估标准 | 例子 |
| --- | --- |
| 准确性(accuracy) | 回答是否与来源材料一致？ |
| 格式(format) | 是否遵守 JSON 或表格格式？ |
| 有依据性(groundedness) | 是否避免了无依据主张？ |
| 安全性(safety) | 是否避免了禁用动作或敏感信息泄露？ |
| 任务成功(task success) | 是否真的完成了用户请求？ |

grader 也并不完美。很多时候仍然需要人工评审，而自动评估也可能漏掉质量问题。

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

## 本节应记住的视角

harness 是一种把模型与工具执行包起来的环境。

> 它不会创造力量，但会帮助力量被安全使用。  
> test harness 会把被测系统包在受控条件里。  
> agent harness 会把多步执行包起来，使之可 trace、可 log、可评估。  
> trace 让执行流程可见。  
> log 留下之后可以说明的记录。  
> evaluation 建立可重复比较。  
> grader 把评估标准变成可执行形式。

## 检查清单

- 能把 harness 解释成包裹执行的环境，而不是模型本身。
- 能解释从物理 harness 到 test harness，再到 AI 执行 harness 的直觉延伸。
- 能说明 agent 执行为什么需要 trace 与 log。
- 能用 dataset、标准、grader、重复运行来解释 evaluation。
- 能说明为什么 prompt、模型、RAG、工具变更都需要回归检查。
- 能说明 harness 让执行变得可观察、可改进，而不是保证正确。

## 什么时候要先想起这个视角

- 当某次模型回答被当作“服务验证已经完成”时
- 当需要解释为什么 trace、log、evaluation 属于单独的执行环境时
- 当系统改动后还缺少检测 regression 的办法时

这时，先拆开 `包裹执行`、`保存步骤记录`、`运行可重复比较`，会更容易看清 harness 的位置。

## 来源与参考资料

- Merriam-Webster, [Harness](https://www.merriam-webster.com/dictionary/harness){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-23.
- Online Etymology Dictionary, [Harness](https://www.etymonline.com/word/harness){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-23.
- Sanderson Oliveira de Macedo, [What makes a harness a harness: necessary and sufficient conditions for an agent harness](https://arxiv.org/abs/2606.10106){: target="_blank" rel="noopener noreferrer" }, arXiv preprint, 2026, 确认日期: 2026-06-23.
- OpenAI, [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 确认日期: 2026-06-23.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 确认日期: 2026-06-23.
- OpenAI, [Working with evals](https://developers.openai.com/api/docs/guides/evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 确认日期: 2026-06-23.
