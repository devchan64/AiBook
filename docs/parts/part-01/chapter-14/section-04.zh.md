# P1-14.4 MCP(Model Context Protocol)与工具连接标准化

> Section ID: `P1-14.4`
> Version: `v2026.07.11`

在 P1-14.3 中，我们把 agent 看成一种把 `目标(goal)`、`状态(state)`、`动作(action)`、`观察(observation)` 持续推进的工作流结构。要让 agent 使用外部资料或工具，就必须有一种连接方式。

> agent：  
> 决定该做什么，并继续推进工作流。
>
> MCP：  
> 标准化 agent 或 AI 应用连接外部工具与数据的方式。

MCP(Model Context Protocol) 是一种开放协议(open protocol)，目标是标准化 AI 应用(application)连接外部系统(external system)的方式。最重要的点是：MCP 既不是模型(model)本身，也不是 agent 本身。

> MCP 是一种协议，用来统一 AI 应用连接外部数据、工具与可复用工作模板的方式。

这里不会深入实现 MCP，而是先看：为什么需要这种标准化，以及可以把它拆成哪些组成部分来理解。

在 Part 1 中，`MCP`、`host`、`client`、`server`、`tools`、`resources`、`prompts` 的基本区分会固定在这里。14.3 看的是 agent 如何朝目标继续多个步骤；这里则把焦点收窄到：`这个工作流怎样用一种共通方式发现并调用外部工具与数据？` 执行追踪与评估会在 14.5 再回来。

## 本节范围

这里说明 MCP 的基本作用与结构。不讨论 MCP 服务器实现细节、SDK 用法、JSON-RPC 消息细节或 OAuth 认证流程。harness、评估与执行日志放到 P1-14.5；更细的安全与隐私议题则会在 P1-15.1、P1-15.2、P1-15.3 再看。

`MCP`、`host`、`client`、`server`、`tool`、`resource`、`prompt` 分别属于不同层次的连接概念。

| 术语 | 极简含义 | 本节中的作用 |
| --- | --- | --- |
| MCP | AI 应用与外部系统之间的连接协议 | 本章的标准化视角 |
| host | 用户实际接触到的应用或运行环境 | 持有连接的一方 |
| client | 与某个 MCP server 通信的组件 | 管理单条连接的单元 |
| server | 提供 tools、resources、prompts 的程序 | 外部能力的提供者 |
| tool | 可执行的函数 | 行动调用的单位 |
| resource | 可读的上下文数据 | 状态与依据的输入面 |
| prompt | 可复用的交互模板 | 复用指示格式的装置 |

这里先把 `MCP 是连接规则`、`server 提供能力`、`tool 用于执行`、`resource 用于读取`、`prompt 是复用模板` 作为基准线。

| 主题 | 本节要看的问题 |
| --- | --- |
| 标准化 | 为什么工具连接需要共通规则？ |
| 组成部分 | host、client、server 分别负责什么？ |
| 提供对象 | tools、resources、prompts 有什么不同？ |
| 连接流程 | agent 会通过 MCP 发现并调用什么？ |
| 注意点 | MCP 没有解决哪些问题？ |

## 本节目标

- 把 MCP 理解成连接协议(protocol)，而不是 agent。
- 区分 host、client、server 的角色。
- 不把 tools、resources、prompts 混成同一回事。
- 理解 MCP 可以让工具使用更方便，但不会自动解决权限(permission)、审批(approval)、校验(validation)。
- 为进入 P1-14.5 的 harness 与评估执行环境做准备。

## 三个基准

这里不会把 MCP 当成一种新模型来解释，而是把它理解成连接规则。阅读正文时，可以先抓住下面三个基准。

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| MCP 是连接协议，而不是 agent | 这能防止把 MCP 误解成“另一个 AI”。 | 只要理解成它是应用连接外部系统的规则即可。 |
| host、client、server 的角色不同 | 这能让标准化结构更容易读懂。 | 只要区分谁发起、谁中介、谁提供能力即可。 |
| 即使有了标准化，权限与校验问题仍然独立存在 | 这能避免对协议本身过度信任。 | 只要理解成审批与安全仍需另外管理即可。 |

## 为什么需要连接标准

正如 P1-14.1 所说，AI 服务会把模型、应用、数据、工具、编排组合在一起。问题在于，随着服务变复杂，需要连接的外部系统也会越来越多。

> 文件系统  
> 数据库  
> 搜索引擎  
> 日历工具  
> issue tracker  
> 设计工具  
> 自动化工具  
> 内部文档系统

如果每个 AI 应用都为每个工具单独写一套连接方式，组合复杂度会非常快地膨胀。

> 应用 A -> 工具 1、工具 2、工具 3  
> 应用 B -> 工具 1、工具 2、工具 3  
> 应用 C -> 工具 1、工具 2、工具 3

在这种情况下，每当同一个工具被接到另一个应用上时，就会重复写出非常相似的代码。MCP 可以被理解成一种尝试：它想通过 `AI 应用与外部系统对话的共通规则` 来减少这个问题。

这个想法可以先压缩成下面这样。

> 每个工具都有一套不同连接方式  
> -> 通过共通协议来发现并调用

官方 MCP 介绍材料会把 MCP 描述成一种开放标准，用来帮助 AI 应用连接数据源、工具和工作流。

## host、client、server

MCP 遵循 client-server 结构。但如果只想到一般 웹 服务里的 client 和 server，画面会不够清楚。在 MCP 语境里，更有帮助的是把 `host`、`client`、`server` 分开。

| 组成部分 | 说明 |
| --- | --- |
| MCP host | 用户实际交互的 AI 应用或 agent 运行环境 |
| MCP client | 维持某一个 MCP server 连接的组件 |
| MCP server | 通过 MCP 暴露外部数据、工具和 prompts 的程序 |

这条关系可以简化成：

```mermaid
--8<-- "assets/part-01/chapter-14/mcp-connection-flow-zh.mmd"
```

一个 AI 应用可能同时连接多个 MCP server。此时通常会由不同的 MCP client 分别管理每个 server 的连接。例如，一个编码工具可能会同时连接文件系统 MCP server 和 issue tracker MCP server。

还要记住一点：MCP server 不一定非要是远程服务。它也可以是本地机器上运行的程序，或者通过网络访问的远程服务。

## MCP server 提供什么

MCP server 最常提供的对象是 `tools`、`resources` 和 `prompts`。

| 元素 | 作用 | 例子 |
| --- | --- | --- |
| tools | 可执行的函数或动作 | 读文件、创建 issue、查数据库、计算 |
| resources | 可读取的上下文数据 | 文件内容、数据库记录、API 响应、文档片段 |
| prompts | 可复用的交互模板 | 带示例的工作指示模板 |

这也会和 P1-14.2 中已经见过的区分连起来。

> resources：  
> 提供模型可读取的上下文。
>
> tools：  
> 执行外部系统功能。
>
> prompts：  
> 帮助把某种交互模式稳定复用。

例如，如果把组织内部文档系统暴露成一个 MCP server，可以这样拆分：

| 提供项 | 从 MCP 角度看 |
| --- | --- |
| 读取文档正文 | resource |
| 执行文档搜索 | tool |
| 规章审查问题模板 | prompt |

这样一来，agent 就能更清楚地知道：`什么可以读`、`什么可以执行`、`已经准备好了哪些交互格式`。

## 发现与调用

MCP 的一个核心直觉是 `discovery`。AI 应用可以向已连接的 MCP server 询问：它有哪些 tools 与 resources。

> 1. AI 应用连接到 MCP server。  
> 2. 检查 server 暴露了哪些能力。  
> 3. 获取可用工具列表。  
> 4. 选择需要的工具并调用。  
> 5. 把结果反映回模型输入或应用状态。

官方架构文档会举出类似 `tools/list` 与 `tools/call` 这样的流程。关键点在于：执行前，应用可以先确认 `有什么工具`；调用时，又可以把 `要发送什么名称和参数` 结构化起来。

假设有一个天气 MCP server。

> 工具发现：  
> 存在 `weather_current` 工具
>
> 工具说明：  
> 查询当前天气
>
> 输入格式：  
> `location`、`units`
>
> 调用：  
> `location = Seoul`  
> `units = metric`
>
> 结果：  
> 当前天气数据

有了这种结构，模型就不会停留在模糊的自然语言层面，只说一句“帮我看看天气”。相反，应用可以构造出 host 能理解的工具调用候选。真正的执行仍然必须落在 host 和 server 的权限策略之内。

## MCP 整理了 agent 的连接表面

如果把 P1-14.3 的 agent 循环再拿回来，MCP 的位置会更清楚。

> 查看目标  
> -> 检查状态  
> -> 选择下一步动作  
> -> 执行工具  
> -> 观察  
> -> 更新状态

MCP 主要整理的是其中 `执行工具` 和 `获取外部上下文` 这两部分的连接面。

| agent 流阶段 | MCP 可以帮助的地方 |
| --- | --- |
| 检查状态 | 通过 resources 读取文件、文档、数据 |
| 选择下一步 | 查看可用 tools 及其说明 |
| 执行工具 | 用标准化方式调用工具 |
| 观察结果 | 接收结构化结果，用于下一步判断 |

但 MCP 并不保证计划质量、判断质量或任务最终成功。MCP 是连接规则。agent 设定什么目标、按什么顺序执行、何时停止，仍然是应用、模型、harness 与政策的问题。

## MCP 没有解决什么

MCP 有助于标准化工具连接，但它不会自动解决所有问题。

| 它不能自动解决的问题 | 原因 |
| --- | --- |
| 判断工具是否安全 | server 暴露出来的能力本身可能有风险 |
| 决定用户权限 | 谁能看什么数据仍是服务策略问题 |
| 执行审批 | 改变外部状态的动作仍可能需要人工确认 |
| 解释结果是否可靠 | 工具结果仍需要单独审查和解释 |
| agent 评估 | 任务是否成功属于 harness 与评估设计问题 |

MCP 的安全文档也会单独讨论 confused deputy problem、token passthrough、SSRF(Server-Side Request Forgery)、session hijacking、local MCP server compromise 之类的风险。这里不会深入讲安全，但因为 MCP server 连接的是外部系统，所以必须始终考虑 trust boundary。

首先要保留的安全原则是下面这句。

> 连接一个 MCP server，就意味着新增一种外部能力。  
> 外部能力必须和权限、审批、日志、隔离一起被管理。

## 从文档工作流看 MCP

用一条较长的文档工作流，会更容易看清 MCP 的位置。

> 用户：  
> 请加强某一节的草稿。
>
> agent：  
> 检查目录和前后章节  
> 查找支撑资料  
> 写正文  
> 验证构建  
> 报告结果

如果存在 MCP，下面这些连接面就可以被标准化。

| 工作 | 可能通过 MCP 连接到什么 |
| --- | --- |
| 读取文档文件 | 文件系统 MCP server |
| 检查 issue 与工作状态 | issue tracker 或项目管理 MCP server |
| 搜索支撑资料 | 搜索或文档仓库 MCP server |
| 执行验证工作 | 本地执行环境或命令执行工具 |

这个例子并不是说 MCP 会替 agent 把文章写出来。MCP 只是连接规则，它让 agent 能更一致地发现并使用外部数据与工具。

## 本节应记住的视角

MCP(Model Context Protocol) 是一种协议，它试图标准化 AI 应用与外部系统之间的连接。

> agent 会把目标继续成工作流。  
> MCP 会整理这条工作流连接外部工具和数据的方式。

> host 持有连接。  
> client 管理某条 server 连接。  
> server 提供 tools、resources、prompts。  
> tools 执行动作。  
> resources 提供上下文数据。  
> prompts 提供交互模板。  
> 权限、审批、安全与评估不会被自动解决。

只要这个视角固定下来，下一节里的 `harness` 就更容易读懂。harness 会把问题推进到：模型、工具和 MCP 连接，如何在真实执行环境中被包裹、记录并评估。

## 检查清单

- 能把 MCP 解释成一种连接协议，而不是 agent 或模型。
- 能区分 host、client、server 的角色。
- 能区分 tools、resources、prompts。
- 能说明 MCP 可以帮助 agent 的工具连接与上下文获取。
- 能说明 MCP 不会自动解决权限、审批、安全与评估。

## 什么时候要先想起这个视角

- 当 MCP 被混成与模型、agent、工具本身同一层概念时
- 当外部系统连接里需要区分“标准化”与“实际执行责任”时
- 当必须再次分清工具连接便利性与权限、审批、校验责任是两回事时

这时，就先拆开 `连接规则`、`能力提供者`、`执行责任`。这样就不容易把 MCP 误读成工具本身或 agent 本身。

## 来源与参考资料

- Model Context Protocol, [What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
- Model Context Protocol, [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
- Model Context Protocol, [Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
