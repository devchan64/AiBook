# P1-7.4 补充学习：从路径寻找走向自动驾驶路径规划

> Section ID: `P1-7.4`
> Version: `v2026.07.12`

7.1 把 `search` 抽象成寻找通向目标的路径问题。7.2 解释了当候选看不完时，`heuristic` 减少的是什么；7.3 又把启发式和概率模型分开。

现在，这一节通过一个具体领域案例，来看这些一般概念在真实系统里是怎样被分成多个层级的。

这里的核心问题是：

> 像“找路”这样一个问题，  
> 在自动驾驶这类真实系统中，是怎样被拆成多个 planning 层级的？

这一节并不是要完整讲解自动驾驶技术。它的目的更窄：借自动驾驶来理解，系统是如何表示路径、如何减少候选、又如何决定“此刻就要执行的动作”。

这一节也不是首次定义这些核心术语的位置。`search`、`search space` 和 `computational limit` 已在 7.1 介绍，`heuristic` 在 7.2 介绍，启发式和概率模型的边界在 7.3 介绍。这里做的是：把这些概念接到一个“真实系统是分层工作的”案例上。

## 本节范围

这里不会深入讨论 sensor、perception、map making、control 或 vehicle dynamics。也不会在这里系统比较以 reinforcement learning 为中心的自动驾驶路线。那些内容会在后面的部分另行出现。

这里先固定一个更窄的基线：

> “找到整体路线”这个问题，  
> 和“决定此刻接下来几秒该怎么动”这个问题，  
> 通常不适合放在同一层里处理。

也正因为如此，真实系统里经常会出现 `global` 和 `local`，或者 `path` 和 `trajectory` 的区分。

## 本节目标

- 把找路问题理解成连接图搜索与真实行驶规划的桥梁。
- 把 `waypoint` 理解成“应该经过的参考点表示”。
- 在入门层面说明 `global planner` 和 `local planner` 的角色差异。
- 避免把 `path` 和 `trajectory` 当成同义词。
- 把自动驾驶案例读成一般搜索与启发式问题的延伸。

## 三个基准

| 基准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 找到整体路线和决定当前运动是不同问题 | 这能把抽象找路和真实车辆控制分开。 | 理解“去终点的大路线”和“接下来几秒的运动”属于不同层。 |
| global 和 local planning 会分开 | 这能说明复杂现实问题为什么不会一次性全解。 | 理解一个层决定大方向，另一个层决定即时动作。 |
| path 和 trajectory 不能混用 | 这能减少后面读机器人或自动驾驶材料时的混乱。 | 理解“经过哪里”和“如何随时间运动”是不同问题。 |

先做一个角色分拆：

| 术语 | 极短含义 | 本节里的作用 |
| --- | --- | --- |
| waypoint | 需要经过的一串参考点 | 表达整体路径流向的单位 |
| global planner | 决定去往终点的大路线的层 | 决定跟随哪条道路与车道流向 |
| local planner | 决定当前要执行的短时运动的层 | 比较即时 trajectory 候选 |
| path | “经过哪里”的空间流向 | 表达整体移动方向 |
| trajectory | 包含时间与速度的运动计划 | 表达即将执行的具体短时运动 |
| layering | 按不同分辨率拆分问题 | 让大型规划问题更可处理的框架 |

## 经典找路会被抽象成图上的路径搜索

Poole 和 Mackworth 说明，达到目标的问题可以抽象成：从起点节点走到目标节点的路径搜索。在这种视角下，关键不在于“世界的所有细节”，而在于当前节点可以去哪里、什么路径能通向目标。

最简单的找路问题可以写成这样：

| 元素 | 找路例子 |
| --- | --- |
| node | 路口、位置、路段入口 |
| edge | 可以通行的道路段 |
| cost | 距离、时间、能耗、交通条件 |
| goal | 到达目的地 |
| result | 一条通往目的地的路径 |

这个抽象也很适合导航系统：给定出发地和目的地，系统可以在路网里决定走哪些道路。

但对真实车辆来说，这还不够。

> 知道“要经过哪些路”本身，  
> 并不能直接决定  
> 此刻该打多少方向、如何调节速度、以及怎样绕开附近障碍物。

自动驾驶路径规划正是在这里，把经典找路问题进一步细分成更多层。

## 历史上，“整体路线”和“即时动作”逐渐被分开

早期 AI 和机器人 planning 常把“如何到达目标”当成一个相对抽象的路径问题。但真实车辆并不只在抽象图上移动，它还要面对车道、曲率、转向极限、其他车辆、行人、信号灯和停止线。

因此，实际行驶系统自然会长出这样的分层：

| 层级 | 中心问题 |
| --- | --- |
| 整体路线规划 | 应该沿着哪些道路与车道流向去到终点？ |
| 当前运动规划 | 接下来这几秒，车辆应该以什么线形和速度运动？ |
| 控制 | 如何把这份计划变成转向与加减速指令？ |

这并不是自动驾驶独有的神奇发明。它更像是一种普遍的 `layering`：当现实问题太复杂，无法一次性用同一分辨率解决时，就把它拆成多个层。

> 看远处的规划问题，  
> 和决定“现在立刻怎么动”的问题，  
> 通常很难用同一种分辨率来求解。

## waypoint 帮助表达整体路线

在这条线里，`waypoint` 可以先理解成车辆应该经过的一组参考点。不同系统对 waypoint 的具体定义略有不同，但这里先抓住一个核心：

> waypoint 让“到终点的大致流向”  
> 可以被表示成一串参考点。

waypoint 可以承担几种作用：

| waypoint 的作用 | 说明 |
| --- | --- |
| 表示整体路线 | 给出车辆应经过的参考点 |
| 支持路线跟随 | 告诉车辆大致应该沿哪个方向流前进 |
| 近似车道中心线 | 把地图几何转换成一串更好处理的点 |
| 给 local planning 提供参考 | 在生成短时 trajectory 候选时提供参考线 |

重要的注意点是：waypoint 不自动等于完整真实运动。

| 表达 | 中心含义 |
| --- | --- |
| waypoint | 需要经过的参考点 |
| route / path | 连接这些点的整体流向 |
| trajectory | 还包含时间、速度和加速度的真实运动计划 |

所以，人们常说“follow the waypoints”，但更严格的读法通常是：

> 以 waypoint 或参考线为依据，  
> 构造出适合当前情境的真实 trajectory。

## DARPA 时代的案例常被看成一个转折点

在自动驾驶历史里，DARPA Grand Challenge 和 Urban Challenge 经常被提到。更安全的读法不是“那时自动驾驶已经彻底完成”，而是：它们让人更清楚地看到，真实车辆必须把路线表示、障碍规避与控制结合起来。

特别是在 Urban Challenge 时期的文档以及后续研究流中，道路网络、车道、路段、检查点等表示变得更结构化。也正是在这一阶段，自动驾驶讨论更清楚地转向了这样的问题：

- 应该怎样表示道路网络和车道流向？
- 应该怎样在这种表示上找到整体路线？
- 又该怎样在当前局部条件下生成短时动作候选？

这里提到 DARPA，只是为了提供历史定位，并不表示今天所有系统都用同一种格式或完全相同的流水线。

## global planner 决定整体路线

`global planner` 一般会计算从起点到终点的大路线。它使用的通常是相对长期的信息：地图、道路连接关系、车道关系、路口和通行条件等。

这里最安全的入门理解是：

> global planner 决定  
> “到终点时，应该沿哪条整体道路与车道流向前进”。

它的输出可以有多种形式：

- 道路段的顺序
- 沿车道中心线形成的参考路径
- waypoint 的序列

因此，global planner 的核心工作不是决定“每一时刻具体打多少方向”，而是决定“总体应该沿着哪条流向走”。

## local planner 决定此刻要执行的短时 trajectory

`local planner` 并不是把 global route 原样照搬的模块。它会结合当前车辆状态、附近障碍物、车道边界、速度条件和安全约束，来决定当前可以执行的一小段 trajectory。

很多现代 motion planning 的说明会把它写成下面这些步骤：

| local planning 常见阶段 | 说明 |
| --- | --- |
| 检查参考线 | 读取道路中心线或 global route |
| 生成候选 | 构造多个短时 trajectory 候选 |
| 评估候选 | 比较碰撞风险、平滑性、舒适性和约束满足情况 |
| 选择其一 | 决定当前要执行哪条 trajectory |
| 交给跟踪或控制 | 转成转向与加减速命令 |

这里的关键不是“它只是在做预测”，而是：

> local planner 的中心工作是  
> 生成多个短时 trajectory 候选、比较它们，  
> 然后决定此刻执行哪一个。

对周围车辆或行人的未来运动做预测，当然可能是其中的重要输入。但很多系统仍然会把 prediction 和 planning 分开：prediction 处理“别人会怎么动”，planning 则处理“参考这些预测后，我们该怎么动”。

## path 和 trajectory 必须分开

这一主题里最常见的混乱，就是把 `path` 和 `trajectory` 当成同义词。

一旦把它们分开，global planner 和 local planner 的角色也会更清楚：

| 区分 | 问题 | 例子 |
| --- | --- | --- |
| path / route | 应该经过哪里？ | 跟随哪条道路或哪条车道？ |
| trajectory | 应该在什么时候以什么速度怎么动？ | 接下来的 3 秒里是否要平滑左避并减速？ |

`path` 更接近空间上的流向，`trajectory` 则把时间上的计划也包括进来。

因此，下列总结相对安全：

- global planner 生成整体 `path`
- local planner 参考这个 path，生成短时 `trajectory`
- controller 再把 trajectory 转成真实转向与加减速命令

## 再用搜索与启发式的语言重读这个案例

如果把自动驾驶案例重新写成第 7 章的语言，大致会得到：

| P1-7 的一般概念 | 在自动驾驶规划中的对应 |
| --- | --- |
| search space | 可能的路线、车道选择与短时驾驶候选 |
| cost | 距离、时间、安全性、舒适性、碰撞风险、约束违反 |
| heuristic | 先检查哪些候选、如何生成参考路径附近的候选、如何尽早丢掉高风险候选 |
| good-enough solution | 在有限时间里找到的安全且可执行的 trajectory |
| layering | 拆成 global path、local trajectory 与 control |

重要的不是把自动驾驶说成一种和搜索完全无关的新问题，而是：

> 自动驾驶路径规划，  
> 仍然可以被理解成：  
> 一个现实世界的大型搜索问题，  
> 只是它必须通过更合适的表示与层次拆分，才能变得可处理。

## 检查清单

- 能把经典找路与自动驾驶路径规划的关系说明成图搜索的延伸。
- 能把 `waypoint` 说明成需要经过的参考点表示。
- 能说明 `global planner` 和 `local planner` 的角色差异。
- 能说明为什么 `path` 和 `trajectory` 不能混用。
- 能用 `search space`、`cost`、`heuristic` 和 `layering` 的语言重读自动驾驶规划。
- 能把“决定整体路线”“选择当前短时 trajectory”“变成真实控制命令”这三个层次分开说明。
- 能把自动驾驶案例读成 planning 层次与概念对应的示例，而不是一个巨大模型。

## 来源与参考资料

- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., 3.1 Problem Solving as Search](https://artint.info/3e/html/ArtInt3e.Ch3.S1.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-29.
- DARPA, [DARPA Urban Challenge, Route Network Definition File (RNDF) and Mission Data File (MDF) Formats](https://web.archive.org/web/20130224095708/https://archive.darpa.mil/grandchallenge/docs/RNDF_MDF_Formats_031407.pdf){: target="_blank" rel="noopener noreferrer" }, 2007-03-14, 确认日期：2026-06-29.
- Siyu Teng, Xuemin Hu, Peng Deng, Bai Li, Yuchen Li, Dongsheng Yang, Yunfeng Ai, Lingxi Li, Zhe Xuanyuan, Fenghua Zhu, Long Chen, [Motion Planning for Autonomous Driving: The State of the Art and Future Perspectives](https://arxiv.org/abs/2303.09824){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023-03-17, 确认日期：2026-06-29.
- Yuncheng Jiang, Xiaofeng Jin, Yanfei Xiong, Zhaoyong Liu, [A Dynamic Motion Planning Framework for Autonomous Driving in Urban Environments](https://arxiv.org/abs/1912.04458){: target="_blank" rel="noopener noreferrer" }, arXiv, 2019-12-10, 确认日期：2026-06-29.
