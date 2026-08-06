# P6-15.3 补充学习：Agent 工作流与图像生成工作流有什么不同？

> Section ID: `P6-15.3`
> Version: `v2026.08.03`

P6-15.1 考察了用共同格式连接工具与资源的视角，P6-15.2 考察了记录并重新说明执行过程的 harness 视角。本补充节是在另一个生成式 AI 场景中重新阅读这两个视角的比较地图。

> 都叫 workflow 时，哪一种流程会选择下一步行动，哪一种流程会变换数据和条件？

这里介绍 InvokeAI 和 ComfyUI，不是为了学习安装、按钮或节点清单。它们是让图像生成 pipeline 可见的案例，目的是不把它和 agent 的控制流程混为一谈。实际运行与比较记录留给 Part 7。

## workflow 这个词并不指同一种结构

Agent workflow 是查看目标和中间观察后改变下一步行动的**控制流程**。图像生成 workflow 则是 prompt、参考条件、模型、潜在表征和图像之间的**数据变换流程**。

| 区分 | 首先移动的东西 | 核心问题 | 代表记录 |
| --- | --- | --- | --- |
| agent workflow | 下一步行动 | 观察之后，应搜索、调用工具还是交给人？ | goal, observation, next_action, stop_reason |
| 图像生成 workflow | 条件和中间表征 | 哪些条件与变换生成了最终图像？ | model, prompt, seed, control, output |
| harness | 执行的可说明性 | 能否重新阅读同一次运行与失败？ | trace, environment, approval, replay |

因此，节点很多的图并不会自动成为 agent。图像生成图可以执行固定的数据路径，而 agent 可以根据观察改变路径本身。

## 以最小范围阅读图像生成 pipeline

Stable Diffusion 系列的最小流程可以写成下面这样。

```text
prompt 与参考条件
-> 文本条件
-> 潜在表征与重复恢复
-> 图像转换
-> 结果审查与执行记录
```

这用执行环境的语言重述了 P5-15.4 的 `文本条件 -> 潜在噪声 -> 重复恢复 -> 图像`。本节不解释每种实现的精确内部细节，也不解释某个节点的全部参数。

ComfyUI 用节点和连接线呈现这类流程。其官方文档把 workflow 定义为相连节点构成的图，并说明它可以保存到图像 metadata 或 JSON 中。[ComfyUI Workflow](https://docs.comfy.org/development/core-concepts/workflow){: target="_blank" rel="noopener noreferrer" }

InvokeAI 通过 Canvas 和 workflow 环境处理图像生成与编辑。Canvas 项目可把图层、mask、参考图像、生成设置与 LoRA 保存在一个项目文件中，因此可用来说明怎样记录被比较的条件。[InvokeAI Canvas Projects](https://invoke.ai/features/canvas/canvas-projects/){: target="_blank" rel="noopener noreferrer" }

## 使用同一个词时要先分开的东西

| 场景 | 阅读流程的方法 | 与 agent 混合时产生的误解 |
| --- | --- | --- |
| ComfyUI 节点图 | 查看模型、条件、潜在表征和图像怎样连接 | 容易以为节点连接本身会进行目标判断或重新规划 |
| InvokeAI Canvas | 查看图像编辑条件和比较状态 | 容易把 Canvas 操作混同为模型内部推理或 agent 行动 |
| AI agent | 查看观察是否选择下一工具、重试或停止 | 容易把所有多步骤执行压平为同一种数据 pipeline |

这两个图像环境有助于显示生成条件和变换路径。但收到 prompt 并不会自动形成能分解目标，或看完结果后自主选择新工具的结构。

## 留下一张 pipeline 卡片

运行工具之前，先填好下面五格。这样可以避免只留下单张输出图像。

| 记录格 | 图像生成 pipeline 要写什么 | 与 agent pipeline 比较时要看什么 |
| --- | --- | --- |
| 输入 | prompt、参考图像、mask、seed | 目标和当前观察是否分开？ |
| 变换 | model、LoRA、control、sampler、steps | 这是数据变换，而不是下一步行动选择吗？ |
| 输出 | 生成图像和审查标准 | 它与最终答案或执行结果有什么不同？ |
| 变更 | 每次只改变一个条件 | 是哪个观察改变了下一步行动？ |
| 再现 | workflow、项目文件、metadata | trace 与 replay 中必须留下什么？ |

这张卡片不是给模型或工具排性能名次的表。它是用来说明 pipeline 的哪个位置改变了结果，以及下一次比较要留下什么的最小记录。

## 交给 Part 7 的边界

- Part 6 比较 workflow 的种类，以及连接、变换、记录的作用。
- Part 7 在 ComfyUI 或 InvokeAI 等环境中实际改变一个输入，并记录结果差异与失败信号。
- 安装方法、custom node 清单、特定模型排名和图像制作技巧不属于本节范围。

## 检查清单

- 我能区分 agent workflow 更接近控制流程，图像生成 workflow 更接近数据变换流程。
- 我能把 ComfyUI 和 InvokeAI 解释成观察并记录 pipeline 的执行环境，而不是模型本身。
- 我能分别记录图像生成的输入、变换、输出、变更和再现。
- 我能说明实际工具操作与条件比较练习属于 Part 7。

## 出处与参考资料

- ComfyUI, [Workflow](https://docs.comfy.org/development/core-concepts/workflow){: target="_blank" rel="noopener noreferrer" }，官方文档，确认日期：2026-08-03。
- ComfyUI, [Nodes](https://docs.comfy.org/development/core-concepts/nodes){: target="_blank" rel="noopener noreferrer" }，官方文档，确认日期：2026-08-03。
- InvokeAI, [Canvas Projects](https://invoke.ai/features/canvas/canvas-projects/){: target="_blank" rel="noopener noreferrer" }，官方文档，确认日期：2026-08-03。
