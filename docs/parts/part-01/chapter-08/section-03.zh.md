# P1-8.3 强化学习：动作与奖励

> Section ID: `P1-8.3`
> Version: `v2026.07.20`

8.1 把监督学习说明成：从同时包含 input 与 label 的例子中学习。8.2 则把无监督学习说明成：从无标签数据中寻找 `structure`、`cluster` 和 `representation`。

这一节引入第三个基本区分。`reinforcement learning` 既不是直接去对齐标签，也不是只在无标签数据里找结构。它是一种这样的学习设定：`agent` 在 `state` 中选择 `action`，在行动之后收到 `reward`，并随着时间改进自己选择动作的 `policy`。

这并不是最近才突然冒出来的新区分。强化学习在 1990 年代和 2000 年代的 AI 与机器学习教育里，就已经是重要主轴之一。所以如果更早的入门材料里强化学习比重大，并不表示那段记忆一定错了。真正需要分开的，是“更早期的基本问题设定”和后来公众更熟悉的 Atari、AlphaGo、RLHF 这些案例。这里采用的是前一种更基础的框架：`state`、`action`、`reward` 和 `policy`。

这一节的核心问题是：

> 当系统并不会直接拿到一个正确标签时，  
> 它到底会通过动作结果去改变什么？

> 强化学习不是在匹配一张答案表，  
> 而是在动作之后收到奖励信号，并据此调整行为方式。

这一节会把 `reinforcement learning`、`agent`、`environment`、`state`、`action`、`reward`、`policy`、`exploration` 和 `exploitation` 用“动作结果带来的奖励信号”这一条线串起来。`state` 和 `action` 的基本直觉已经在 7.1 出现，label、监督学习和无监督学习的区分则已经在 8.1 和 8.2 出现。

这一节不会计算强化学习算法。MDP、Bellman equation、Q-learning、policy gradient、actor-critic 和 deep reinforcement learning 都只会以名称与位置的形式出现。

这里也不会深入游戏 AI、机器人控制、推荐系统或 RLHF。强化学习的后续算法和 RLHF 的大图会在 Part 4 Chapter 19 再回来，LLM 对齐语境里的 RLHF 会在 Part 6 再连接。这里的重点更窄：为什么强化学习是一个和监督学习、无监督学习不同的问题设定。

这里先采用一个工作定义：

> 强化学习，就是在状态里选择动作，  
> 并利用动作之后回来的奖励，  
> 去寻找一个长期来看更好的 policy。

## 用动作与奖励确定学习方向的方式

- 用动作与奖励的语言解释 reinforcement learning。
- 在入门层面区分 agent、environment、state、action、reward 和 policy。
- 避免把 reward 和监督学习里的 label 混为一谈。
- 理解 delayed reward 的直觉。
- 理解 exploration 与 exploitation 之间的张力。
- 避免把 reinforcement learning、deep learning、游戏 AI 和 RLHF 当成同一个东西。

## 三个基准

| 基准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 强化学习通过 state、action 与 reward 来调整行为 | 这能一眼看出它和监督学习的问题设定不同。 | 把它读成“动作与后果的流程”，而不是“输入与答案对”。 |
| reward 和 label 不是一回事 | 这能防止把强化学习误解成监督学习的变体。 | 理解系统不是直接拿到答案，而是在动作后收到反馈。 |
| 好动作不一定马上显现价值 | 这是 delayed reward 与 exploration/exploitation 问题的起点。 | 先保留“现在看似吃亏的动作，可能换来以后更好的结果”这一感觉。 |

先做一个角色分拆：

| 术语 | 极短含义 | 本节里的作用 |
| --- | --- | --- |
| reinforcement learning | 通过动作结果的奖励来调整 policy 的学习方式 | Chapter 8 的第三个基准点 |
| agent | 选择动作的行动主体 | 核心决策者 |
| environment | agent 与之交互的外部世界 | 结果返回的地方 |
| state | 当前情境的信息 | 选择动作的依据 |
| action | agent 实际做出的选择 | 直接影响奖励与下一状态的原因 |
| reward | 动作之后回来的数值反馈 | 必须和 label 区分开的学习信号 |
| policy | 从状态映射到动作的方法 | 强化学习试图改进的对象 |
| exploration | 试尚未充分了解的动作 | 为学习收集信息 |
| exploitation | 选当前看起来最好的动作 | 利用已经学到的东西 |

## 强化学习是在动作后果中学习

在强化学习里，最中心的词是 `action`。一个 `agent` 在 `environment` 里观察当前 `state` 或 `observation`，然后选一个 `action`。环境随后发生变化，并把 `reward` 反馈回来。

OpenAI 的 Spinning Up 把强化学习说明成：agent 通过与环境交互，并在 trial and error 中学习。Google 的术语表也说明，agent 会根据 policy 选择 action，并观察环境的 state。

入门阶段的基线流程是：

> 先观察 state。  
> 然后选择 action。  
> environment 发生变化。  
> 收到 reward。  
> 再调整未来怎样行动。

可以想一个仓库机器人：

| 元素 | 仓库机器人例子 |
| --- | --- |
| agent | 负责搬运货物的机器人 |
| environment | 仓库、货架、通道与障碍物 |
| state 或 observation | 机器人位置、目标位置、周围障碍 |
| action | 前进、转向、停止、抓取货物 |
| reward | 安全搬到目标得到正奖励，碰撞得到负奖励 |
| policy | 在不同状态下如何选动作的方法 |

在这个例子里，机器人不会在每一时刻直接拿到一个标准标签。它是先行动，再经历后果，并根据后果得到好坏不一的反馈。

## reward 不是 label

初学强化学习时，最容易产生的误解之一，就是把 `reward` 当成监督学习里的 `label`。两者确实都是学习信号，但它们不是同一种信号。

| 区分 | 监督学习里的 label | 强化学习里的 reward |
| --- | --- | --- |
| 给出的时点 | 一开始就贴在训练例子上 | 在动作之后返回 |
| 中心问题 | 这个输入对应什么输出？ | 这种行动方式长期来看好不好？ |
| 信号形式 | 类别、数值目标、预期输出 | 对动作结果的数值反馈 |
| 解释注意点 | 标签标准不一定是绝对真理 | 奖励也不等于道德真理或全部目标 |

例如在客服分类里：

> 输入：“我想退款。”  
> 标签：退款

而在强化学习式互动里：

> state：客户发来一条退款相关消息  
> action：先发送退款政策说明  
> result：客户问题得到解决  
> reward：正奖励

这里的 reward 并不是 `退款` 这个标签，而是对“这一连串行动是否帮助达成目标”的反馈。

## policy 是选择动作的方法

`policy` 指的是：agent 在看到 state 或 observation 后，怎样决定接下来做什么动作。Google 的 Machine Learning Glossary 把 policy 定义成从 state 到 action 的映射。OpenAI Spinning Up 也把它解释成 agent 决定做什么动作的规则。

所以这里的工作读法是：

> policy = 看见某个状态后，选择哪个动作的方法

用一个简单扫地机器人例子来看：

| 状态 | 动作 |
| --- | --- |
| 前方没有障碍物 | 前进 |
| 前方有障碍物 | 转向 |
| 电量不足 | 返回充电座 |
| 探测到灰尘较多区域 | 提高吸力 |

这当然不是一个真实训练出来的 RL policy，只是为了帮助理解：policy 的本质是“从状态到动作的连接方式”。

强化学习真正想改进的，不是只把下一步动作选对一次，而是逐步形成一个在很多状态下都能带来更高回报的动作方式。

## delayed reward 会让问题更难

强化学习之所以难，一个原因是 `reward` 不一定立刻回来。这就是 `delayed reward` 的直觉。

想一个迷宫里的 agent：

> 它不会在每一步都被告诉“这一步对不对”；  
> 它可能只有走到出口时才收到一个大的奖励；  
> 然后才需要回头判断，前面哪些动作真的帮助它走到了出口。

这和监督学习很不一样。监督学习里，很多例子会直接附着目标输出；而强化学习里，一个动作的真正价值，可能要在很多步之后才显现出来。

类似直觉也出现在业务场景里：

| 情况 | 立刻可见的结果 | 更晚才显现的结果 |
| --- | --- | --- |
| 推荐系统 | 用户点击了 | 用户是否满意并在之后回来 |
| 客服响应 | 用户对第一条回复有反应 | 问题是否真正解决、投诉是否减少 |
| 库存管理 | 今天成本下降了 | 几周后是否减少缺货或积压 |
| 机器人控制 | 机器人无碰撞地走了一步 | 整个任务是否被安全完成 |

所以，强化学习问的不只是“这一步现在看起来好不好”，而是“这一步会怎样影响未来的结果”。

## exploration 与 exploitation

强化学习里有一个经典张力：`exploration` 和 `exploitation`。

`exploration` 指的是去尝试那些还没有充分了解的动作。`exploitation` 指的是根据目前已经学到的经验，直接选择看起来最好的动作。

| 选择 | 含义 | 风险 |
| --- | --- | --- |
| exploration | 尝试新动作以收集信息 | 短期内可能拿到较低奖励 |
| exploitation | 选择当前看来最好的动作 | 可能永远发现不了更好的动作 |

Google 的术语表也用 `epsilon-greedy policy` 来解释这种平衡。入门阶段最关键的直觉是：

> 如果永远不去试新动作，就学不到更好的做法；  
> 但如果一直只试不确定的动作，又可能得不到稳定表现。

强化学习很大一部分工作，就是在处理这种平衡。

## 强化学习不只属于游戏

游戏 AI 是强化学习最常见的介绍方式，因为游戏里的 state、action、reward 以及输赢结果都比较容易描述。但如果只把强化学习理解成游戏技术，它的范围就会被缩窄。

只要下面这些条件同时成立，强化学习的结构就会比较明显：

> 存在可选择的动作；  
> 动作会影响之后的状态；  
> 系统会收到某种 reward 信号；  
> 现在的动作会影响未来的结果。

因此，下面这些场景都可以用强化学习的结构去理解：

| 例子 | state | action | reward |
| --- | --- | --- | --- |
| 迷宫或游戏 | 当前位置、剩余时间、分数 | 移动、攻击、防御 | 得分增加、胜利、失败 |
| 机器人控制 | 机器人位置、关节状态、障碍物 | 移动、旋转、抓取 | 任务完成、节能、避碰 |
| 推荐系统 | 用户上下文、历史反应 | 选择展示哪个项目 | 点击、满意度、长期回访 |
| 库存管理 | 当前库存、需求估计、成本 | 调整订货量 | 减少缺货、降低仓储成本 |
| 对话系统 | 用户请求、对话历史状态 | 选择下一步回复方式 | 问题解决、用户评分、安全达标 |

这些都只是概念说明例子。真实部署还会涉及 reward 设计、安全约束、exploration 成本、数据收集与评估方式等困难问题。

## 它和其他学习类型的边界

第 8 章在区分三种基本学习类型。重新压缩一下：

| 学习类型 | 数据与信号 | 核心问题 | 本章位置 |
| --- | --- | --- | --- |
| supervised learning | 输入与标签 | 这个输入该预测什么标签？ | 8.1 |
| unsupervised learning | 无标签数据 | 数据内部有什么结构？ | 8.2 |
| reinforcement learning | 状态、动作、奖励 | 哪些动作会提高长期奖励？ | 8.3 |

`deep learning` 不在这张表同一条分类轴上。它可以和强化学习结合，这时人们会说 `deep reinforcement learning`，但强化学习本身并不等于深度学习。

`RLHF` 也不能代表强化学习的全部。它是 LLM 对齐中的重要现代设定，但拿它来当强化学习整体的起点会太窄。

## 检查清单

- 能把 reinforcement learning 说明成由 state、action 和 reward 串起来的学习流程。
- 能在入门层面区分 agent、environment 和 policy。
- 能说明 reward 并不等于监督学习里的 label。
- 能说明 delayed reward 为什么会让强化学习更难。
- 能说明 exploration 和 exploitation 的差别。
- 能避免把 reinforcement learning、deep learning、deep reinforcement learning 和 RLHF 混成同一个词。
- 能把问题读成行动与结果的时间流，而不只是“输入和标准答案”。
- 能把 reward、exploration、exploitation 和 delayed reward 放在同一条强化学习说明线上。

## 来源与参考资料

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
- OpenAI Spinning Up, [Part 1: Key Concepts in RL](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., Chapter 12 Planning with Uncertainty](https://artint.info/3e/html/ArtInt3e.Ch12.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
- Richard S. Sutton and Andrew G. Barto, [Reinforcement Learning: An Introduction, second edition](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2018, 确认日期：2026-07-19.
