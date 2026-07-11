# P4-19.1 价值型强化学习(value-based reinforcement learning)

> Section ID: `P4-19.1`
> Version: `v2026.07.11`

在 P4-2.3 里，我们把强化学习(reinforcement learning)先抓成了`通过行动(action)与奖励(reward)来调整策略(policy)的学习`。再往里走一步，就会出现下面的问题。

第一次遇到强化学习算法时，问题会立刻冒出来。

- 在什么状态(state)下什么行动是好的，模型到底按什么标准学习？
- `好`这件事，是像规则一样写，还是像数字一样写？
- Q-learning 和 SARSA 都叫强化学习，它们到底差在哪里？

价值型强化学习，是一种通过给每个状态里的行动附上长期好坏的数值来学习的做法。

这一节解释 `value-based reinforcement learning`、`state value`、`action value`、`Q-value` 的基本含义。后面的 Section 会在这个把手上继续当前语境里的判断，而“把行动的长期好坏读成分数”这一基本感觉，会再次通过这一节和[概念词汇表](/AiBook/en/reference/concept-glossary/)连回来。

## 本节范围

这一节回答下面这些问题。

- 学习 value，到底是什么意思？
- state value 和 action value 有什么不同？
- 为什么 Q-value 在强化学习里很重要？
- Q-learning 和 SARSA 哪些地方相似，哪些地方不同？
- 价值型强化学习适合什么问题，又会从哪里开始露出局限？

这一节不会深入展开下面这些内容。

- Bellman equation 的严格推导
- convergence 的证明
- function approximation 与 deep Q-network(DQN)
- policy gradient、actor-critic 的更新过程

这一节集中在抓住价值型强化学习的基本结构，以及 Q-learning 与 SARSA 在解释上的差异。policy-based reinforcement learning 会在 P4-19.2 继续。reward 设计、exploration 成本、现实应用时的注意点，会在 P4-19.3 再整理一次。DQN 与策略系方法的大图，会在补充学习 P4-19.4 重新接上；Bellman equation、convergence、function approximation 的最小连接，则会在 P4-19.5 重新收束。

## 本节目标

- 能把价值型强化学习解释成`把行动的长期好坏学成数字的做法`。
- 能区分 state value 和 action value。
- 能说明 Q-learning 是按`下一个状态里看起来最好的行动`来更新。
- 能说明 SARSA 是按`下一个时刻实际选择的行动`来更新。
- 能理解这两个算法的差异会连接到不同的学习态度。

## 为什么要学习 value

在强化学习问题里，并不会每一步都给出正确标签。相反，agent 会先做行动，再收到奖励，然后经历下一个状态。

这时，不是先把 policy 直接写死，而是先给`这个行动到底有多合适`记一个数字，会带来几个好处。

- 行动更容易比较。
- 即使 policy 还没完成，也可以一点点改进。
- 在同一个状态里，可以相对地读多个行动候选。

也就是说，价值型强化学习更接近`先把什么更好打成分数`，而不是`直接把要做什么背下来`。

如果借一个餐馆推荐的比喻：

- policy：在这个街区里立刻决定去哪里的方法
- value：这个选择从长期看会有多满意的预期分数

这个差别很重要。把价值型强化学习先理解成在做`行动的预期记分板`，会更容易读懂。

## state value 和 action value 不一样

在强化学习书和论文里，value 通常不会只写成一个词，而会分成两类。

| 术语 | 英文 | 简单含义 |
| --- | --- | --- |
| 状态价值 | state value | 处在这个状态整体上有多好 |
| 行动价值 | action value | 在这个状态下做这个行动有多好 |

可以想一个迷宫游戏。

- 出口前一格，可能 state value 很高。
- 但即使在那一格，朝墙那边移动的 action value 也可能很低。

所以，正因为`好的状态里也可能有坏的行动`，action value 才会特别重要。

把这个差别再写具体一点，可以这样读。

| 场景 | state value 视角 | action value 视角 |
| --- | --- | --- |
| 到了出口前一格 | 整体上是有利位置 | `向前`可能高，`向后`可能低 |
| 站在危险区域边缘 | 离目标可能很近 | `抄近路`看起来高，但因为跌落风险，实际可能低 |
| 站在高奖励道具旁边 | 潜在上是个好状态 | `拿道具`可以高，`无视并绕开`可能更低 |

所以，state value 读的是`我现在在哪`，action value 读的是`我从这里做什么`。在强化学习里，真正比较选择时，action value 往往是更直接的标准。

## Q-value 到底在记什么

action value 通常写成 Q-value。`Q(s, a)` 表示在状态 `s` 下采取行动 `a` 时，预期会得到的长期回报(expected long-term return)。

这里重要的不是公式本身，而是解释。

`Q-value 是一个预期分数，用来表示现在在这个状态下做这个行动，接下来整体会有多划算。`

所以，Q-table 或 Q-function 都是在尝试回答下面这些问题。

- 现在在这里往上走，好不好？
- 往下走是不是更好？
- 虽然眼前看起来吃亏，但后面会不会换来更大回报？

如果画成一个小表，可以写成下面这样。

| 状态(state) | 行动(action) | 当前 Q-value 的解释 |
| --- | --- | --- |
| 起点位置 | 向右 | 朝出口方向，所以相对较高 |
| 起点位置 | 向左 | 是死路，所以较低 |
| 出口前 | 向前 | 离到达奖励很近，所以较高 |
| 出口前 | 向后 | 会离开目标，所以较低 |

这个表最关键的是：Q-value 不是单纯在记`这一刻让人舒服的一次选择`。哪怕眼前前进一步的奖励很小，只要后面能连到出口，Q-value 就可能变高。反过来，即使眼前看起来有一点即时收益，只要后面会接更大的惩罚，Q-value 也可能变低。

| 眼前看到的选择 | 即时印象 | Q-value 会再追问什么 |
| --- | --- | --- |
| 立刻拿到 1 分的行动 | 当下看起来不错 | 后面会不会留下更大的惩罚或死路 |
| 暂时绕路的行动 | 当下像是在吃亏 | 之后会不会接上更大的回报 |
| 有风险的捷径 | 看起来好像能更快结束 | 把失败成本算进去后还真的划算吗 |

## 价值型强化学习的基本循环

价值型强化学习的核心，是`做一次行动，看一次结果，再把价值表轻微改一下`的循环。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-1-mermaid-01-en.mmd"
```

这个图会让价值型强化学习被读成`看完行动结果后，一点点修正记分板的循环`。关键不是一次性把整个 policy 做完，而是在循环里逐步调整状态-行动的值。

这个循环比 P4-2.3 看到的强化学习一般循环再具体一步。这里不是一次改整个 policy，而是把焦点放在持续修正像 `Q(s, a)` 这样的值估计上。

## Q-learning 在学什么

Q-learning 是最广为人知的价值型强化学习算法。它的核心想法很简单。

`到达下一个状态时，用那个状态里看起来最好的行动，来更新当前行动的价值。`

也就是说，Q-learning 更新时看的不是`接下来实际做了什么`，而是`下一个状态里看起来最好的选择是什么`。

正因为这一点，Q-learning 常被介绍为 `off-policy` 算法。

`它不是完全贴着实际行为流在学，而是稍微离开当前行动流，按下一个状态里看起来最好的选择来学。`

放到一个小迷宫例子里：

- 现在虽然因为 exploration 而往下走了
- 但更新时仍然可以按`如果在下个状态里最好的行动其实是向右`来修正当前值

所以，Q-learning 会带一点乐观地反映`未来如果做得最好，会走出的路径`。

## SARSA 在学什么

SARSA 也是价值型强化学习算法。它的名字来自 state、action、reward、next state、next action 的首字母。

SARSA 的核心想法和 Q-learning 相似，但标准不同。

`它用下一个状态里实际选择的行动，来更新当前行动的价值。`

也就是说，SARSA 反映的不是`看起来最好的下一个行动`，而是`我接下来真的做了什么`。

正因为这一点，SARSA 常被解释为 `on-policy` 算法。

`它是在自己当前实际遵循的行动方式之内学习。`

例如，如果 exploration 还在混入一些有风险的行动，SARSA 就会把这种带有探索倾向的真实路径一起学进去。

## Q-learning 和 SARSA 的差异

两者都会更新 Q-value，但它们取下一个值的位置不同。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-1-mermaid-02-en.mmd"
```

这个图把 Q-learning 与 SARSA 的差异直接分开了。两者都会看下一个状态，但一个是按`看起来最好的下一个行动`来改值，另一个是按`实际继续做了的下一个行动`来改值。

如果压成表，就是下面这样。

| 项目 | Q-learning | SARSA |
| --- | --- | --- |
| 下一个值的依据 | 下一个状态里的最大 Q-value | 下一个状态里实际选择行动的 Q-value |
| 学习态度 | 可能更乐观 | 更直接反映真实行动流 |
| 常见附带说明 | off-policy | on-policy |

这里比术语更重要的是感觉。

- Q-learning：反映`理论上看起来最好的下一步`
- SARSA：反映`我实际上接着做了什么`

如果把同一个场景再压短一点，两者会这样读。

| 同一个场景 | Q-learning 的解读 | SARSA 的解读 |
| --- | --- | --- |
| 下一个状态里同时存在一个好行动和一个危险行动 | 它更强地反映`如果能做到最好的行动` | 它也会反映`因为 exploration，危险行动也可能真的发生` |
| exploration rate 还很高 | 更容易乐观地读未来 | 更直接反映当前 policy 的不稳定 |
| 环境里的失败成本很大 | 更可能被高最优值快速拉过去 | 更可能保守地把真实失误路径的损失记进去 |

## 为什么这个差别重要

这个差别在掺有危险行动的环境里，尤其会造成解释差异。

可以想象迷宫旁边有一个大惩罚的悬崖。

- Q-learning 更容易把值往`如果总能最优地走，其实是可以的`那边抬高。
- SARSA 则更能反映`探索时真的可能失误`这一点。

所以，如果当前行动 policy 本身就不够谨慎，SARSA 会把这种不够谨慎的现实一起学进去。也正因如此，很多入门教材会把 SARSA 描述成看起来更保守(conservative)。

如果把这个差别改写成运营判断句，可以这样读。

| 环境性质 | 更先冒出来的解释问题 |
| --- | --- |
| 失败成本小，而且寻找最优路径更重要 | `是不是该更快把最好的路径抬上去？` |
| exploration 失误很多，失败成本又大 | `是不是应该把真实 policy 的不稳定也一起反映进去？` |
| 是玩具迷宫或课堂模拟例子 | `是不是很适合用记分板视角来解释两个算法的差别？` |
| 是真实机器人、自动移动这类失误成本明显的场景 | `乐观的值估计会不会把真实风险遮掉？` |

## 什么时候应该先抓价值型视角

第一次把强化学习接到问题上时，应该先问的不是算法名字，而是`这个问题是不是适合读成状态-行动记分板？`

| 先看到的问题场景 | 为什么可以先从价值型视角抓起 | 先要警惕什么 |
| --- | --- | --- |
| 行动候选少而清楚 | 它很适合比较每个行动的长期分数 | 状态一多，表格式直觉会很快变重 |
| 在同一个状态里会反复比较几个行动 | Q-value 可以直接贴到`哪个行动更有利`这个问题上 | 不要只看即时回报而漏掉长期回报 |
| 想用教学例子展示 exploration 与 exploitation 的差别 | Q-learning 与 SARSA 很容易用状态-行动表解释 | 不能把玩具例子直接当成真实部署问题 |
| 比起直接输出 policy，更直观的是先比得分 | 先放价值表，会让说明路径更简单 | 连续行动或巨大的状态空间会很快露出局限 |

## 会用在哪里

价值型强化学习在状态和行动数量相对清楚、且可以反复试行动结果的问题里，很适合提供直觉。

- 网格迷宫与游戏移动
- 简单机器人路径搜索
- 资源分配的玩具模拟
- 顺序选择问题的入门例子

在实务里，一旦问题规模变大，单纯的 Q-table 就无法承受状态数。接下来通常就会走向 function approximation、神经网络，以及更复杂的策略型方法。这个连接会在 Part 4 和 Part 5 再次变得重要。

把它的局限再写明确一点，可以是下面这样。

| 价值型做法适合的场景 | 局限会很快显露的场景 |
| --- | --- |
| 状态和行动数量小到可以用表枚举 | 状态多到 Q-table 实际上根本填不完 |
| 可以大量重复模拟 | 真实环境尝试很贵或有风险 |
| 行动候选是离散的(discrete) | 行动是连续的(continuous)，很难直接做记分板比较 |
| 容易用记分板解释长期回报 | 观测太复杂，仅靠值估计很难表达 policy |

所以，价值型强化学习非常适合建立入门直觉，但现实问题一变大，就会很快撞到`值表到底该怎么维持`这道限制。

## 案例与例子

### 案例 1. 仓库机器人在路口通过记分板学习该往哪边走

仓库机器人去取货时，人最容易先写出的标准，通常是`现在最近的路`、`眼前能更快前进一格的方向`这类简单规则。但有些路现在看起来短，后面却可能更容易堵，或者转向成本更大，从长期看反而吃亏。价值型强化学习会给每个位置和行动组合附上`从现在往后有多划算`的分数，让机器人逐步学到更好的路径。所以，即使在同一个路口，反映后续通行流而不只是眼前距离的选择，也会渐渐拥有更高的 Q-value。

例如，可以想象机器人在路口前积累了下面这些经验。

| 状态 | 行动 | 即时结果 | 后续影响 | 为什么值会变 |
| --- | --- | --- | --- | --- |
| 货架 A 前路口 | 直行 | 立刻快一格 | 前方通道经常堵塞 | 眼前有收益，但长期延迟可能很大 |
| 货架 A 前路口 | 右转 | 开始先绕一格 | 后面通道更宽、更稳定 | 现在看似吃亏，但长期行进更稳定 |
| 货架 A 前路口 | 左转 | 付出转向成本 | 进入碰撞风险区 | 把失败成本算上后，值可能下降 |

这个表最关键地显示的是：`现在最短的行动` 和 `长期最有利的行动` 可能并不一样。价值型强化学习，正是在尝试把这个差异累积成数字去读。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-1-mermaid-03-en.mmd"
```

如果把这个案例压成 review memo，可以这样写。

| 当前状态 | 行动候选 | 需要一起看的失败成本 | 下一步问题 |
| --- | --- | --- | --- |
| 进入路口前 | 左、右、直行 | 堵塞通道、转向延迟、碰撞风险 | 最高的 Q-value 在现实里也真的是最安全的路径吗？ |
| exploration 混入的拥挤区段 | 看起来最短的行动、绕行动作 | exploration 可能造成更大瓶颈或碰撞 | 是否应该比乐观更新更重视真实 policy 流？ |

这个案例可确认的结果，体现在比较下面这些点：`一开始直行看起来更快`，但经过多次经验后，`绕行路线的 Q-value 会不会更高`，以及选择直行时留下的延迟和碰撞模式会不会反复出现。也就是说，价值型解释看的不是`哪边看起来快`，而是`哪边的长期分数随着真实经验上升得更多`。

### 案例 2. 悬崖旁通道上，快路和安全路分开时

假设 agent 到目标点有两条路。人最容易先抓的标准通常是`到达最快的路`，或`当前奖励涨得快的路`。所以，旁边有大惩罚的悬崖捷径，起初可能显得更好。但在强化学习里，必须把`连同失误可能性一起的长期回报`一起读进去。此时，Q-learning 会更强地反映`如果下一个状态里总能最优行动`这一点，所以可能让快路保持相对较高的值。相反，SARSA 更直接反映 exploration 中真的会混入悬崖失误的路径，因此可能把安全绕路读得更高。

| 同样的路径选择问题 | Q-learning 更先出现的解释 | SARSA 更先出现的解释 |
| --- | --- | --- |
| 快但危险的捷径 | 如果始终最优行动，它可能是划算的 | 一旦把 exploration 中的失误算进去，风险成本就很大 |
| 慢但安全的绕路 | 即时效率看起来较低 | 按真实 policy 来看，可能更稳定 |

这个案例可确认的结果，体现在比较下面这些点：走快捷径时悬崖惩罚到底多频繁地真实累积，安全绕路在重复学习后会不会得到更高的 Q-value，以及当 exploration rate 较高时两种算法的路径偏好是否会拉得更开。也就是说，这个案例让我们不是从公式，而是从`失误可能性被多直接地写进值估计`去读算法差别。

### 案例 3. 客服机器人在快速结束与安全解决之间学到不同的值

当客服机器人收到咨询时，人最容易先看的标准，通常是`平均处理时间`、`能不能一次很快关掉`这类即时效率指标。所以，在`直接结束回答`、`追加提问`、`转人工`之间，眼前最省时间的行动可能看起来最好。但现实里，问题没有真正解决时，用户可能会再次发起咨询，或者不满继续积累。相反，转人工虽然眼前看起来更贵，却可能在长期上减少重复咨询并保住满意度。

这个场景会更清楚地说明：为什么需要价值型视角。因为系统不是先把 policy 用句子写死，而是要把每个状态与行动组合`长期到底有多合适`学成值。

| 咨询状态 | 行动候选 | 即时印象 | 长期需要再看的东西 |
| --- | --- | --- | --- |
| 看起来像简单问题的初始状态 | 立刻结束 | 处理时间短，看起来高效 | 是否真的解决、是否发生重复咨询 |
| 信息不足的状态 | 追加提问 | 眼前对话变长 | 是否减少误答并提升解决率 |
| 不满正在升高的状态 | 转人工 | 即时成本大 | 是否防止流失并维持满意度 |

这个案例说明：Q-value 不是单纯的速度分，而是读取`当前行动会怎样改变后续状态与奖励流`的装置。

这个案例可确认的结果，体现在比较以下现象：在`经常被立即结束`的状态里，重复咨询、不满、再次转人工等后续成本是否持续增大；而在`追加提问`或`转人工`的状态里，长期回报是否真的更高。也就是说，价值型视角记下的不是`现在关得快不快`，而是`这个行动会怎样改变下一个状态与后续成本`。

## 练习与例子

这个例子集中在用数字直接确认 `Q-learning` 与 `SARSA` 会把同样的经验读得稍有不同。

问题情境：

- 即使是同样的奖励经验，Q-learning 与 SARSA 也可能因为取下一个值的标准不同而得到不同更新结果

输入(input)：

- 当前状态 `S0`
- 当前行动 `right`
- 即时奖励 `+1`
- 下一个状态 `S1`
- 当前 Q-table 的值

期望输出(output)：

- Q-learning 计算出的更新结果
- SARSA 计算出的更新结果
- 能看出两种方式差别的更新前后值

要确认的概念：

- Q-learning 会按下一个状态里看起来最好的行动值来修正当前值
- SARSA 会按下一个状态里实际继续选择的行动值来修正当前值
- 即使是同样经验，只要更新标准不同，也会通向不同学习态度

```python
alpha = 0.5
gamma = 0.9

q_table = {
    ("S0", "right"): 0.40,
    ("S1", "up"): 0.80,
    ("S1", "down"): 0.30,
}

state = "S0"
action = "right"
reward = 1.0
next_state = "S1"
actual_next_action = "down"

old_value = q_table[(state, action)]

# Q-learning: 在 next state 里使用最大的值
best_next_value = max(
    q_table[(next_state, "up")],
    q_table[(next_state, "down")],
)
q_learning_target = reward + gamma * best_next_value
q_learning_updated = old_value + alpha * (q_learning_target - old_value)

# SARSA: 使用实际下一个行动的值
actual_next_value = q_table[(next_state, actual_next_action)]
sarsa_target = reward + gamma * actual_next_value
sarsa_updated = old_value + alpha * (sarsa_target - old_value)

print("old Q(S0, right) =", round(old_value, 3))
print("Q-learning target =", round(q_learning_target, 3))
print("Q-learning updated =", round(q_learning_updated, 3))
print("SARSA target =", round(sarsa_target, 3))
print("SARSA updated =", round(sarsa_updated, 3))
```

执行结果可以读成下面这样。

```text
old Q(S0, right) = 0.4
Q-learning target = 1.72
Q-learning updated = 1.06
SARSA target = 1.27
SARSA updated = 0.835
```

这里重要的是：两个算法都从同一个当前经验出发，但由于读取下一个值的标准不同，结果就变了。

- Q-learning 用的是 `S1` 里看起来最好的行动 `up` 的值 `0.8`
- SARSA 用的是 `S1` 里实际选择的行动 `down` 的值 `0.3`

所以，Q-learning 那边的更新抬得更高。

### 改一个值试试：如果实际下一个行动变了，更新态度会变多少？

这次保持当前经验不变，只把下一个状态里实际选择的行动改成 `up`。

```python
alpha = 0.5
gamma = 0.9

q_table = {
    ("S0", "right"): 0.40,
    ("S1", "up"): 0.80,
    ("S1", "down"): 0.30,
}

state = "S0"
action = "right"
reward = 1.0
next_state = "S1"
actual_next_action = "up"

old_value = q_table[(state, action)]
best_next_value = max(
    q_table[(next_state, "up")],
    q_table[(next_state, "down")],
)
q_learning_target = reward + gamma * best_next_value
q_learning_updated = old_value + alpha * (q_learning_target - old_value)

actual_next_value = q_table[(next_state, actual_next_action)]
sarsa_target = reward + gamma * actual_next_value
sarsa_updated = old_value + alpha * (sarsa_target - old_value)

print("Q-learning updated =", round(q_learning_updated, 3))
print("SARSA updated =", round(sarsa_updated, 3))
```

```text
Q-learning updated = 1.06
SARSA updated = 1.06
```

第一次运行里，实际下一个行动是 `down`，所以 SARSA 更保守地更新了。但一旦把实际下一个行动改成 `up`，SARSA 也会得到和 Q-learning 相同的值。也就是说，两种方法的差别，与其说是名字记忆，不如说是它们在更新里有多直接地反映`policy 实际上会继续做什么行动`。

### 这个练习怎样回收到 Part 4 的目标

Part 4 里读强化学习，不是为了把公式背下来，而是为了在问题定义层面理解`系统是在什么标准下，一边与环境互动一边更新的`。这个对比练习显示的是：即使 reward 一样，只要实际下一个行动不同，学习结果也会不同。因此，评估标准也不能只剩平均 reward，而必须把 exploration 成本、失败风险、policy 的真实行动流一起放进来。如果读者没有感到这一节的目标，通常不是因为 Q-learning 的式子太难，而是因为`为什么值会变`没有被回收到运营判断句里。

| 共同记录语言 | 这次练习要立刻留下的内容 |
| --- | --- |
| 看见的结构 | 同样的奖励经验，也会因为实际下一个行动不同，让 Q-learning 与 SARSA 的更新分开 |
| 解释边界 | 高 Q-value 或大更新幅度，并不立刻意味着安全的 policy |
| 下一个问题 | 如果改 reward、exploration rate、失败成本，哪种更新态度更合适？ |

这一节也不要只留下值的说明。还要一起记下哪些状态-行动候选与哪些失败成本被并排放在一起。即使同样看起来是高 Q-value，有些状态可能能稳定重复，有些状态却会留下更大的 exploration 成本和失败损失，所以 review memo 要一起保留下来。

| 一起要留下的项目 | 这一节写的内容 | 为什么需要 |
| --- | --- | --- |
| 状态-行动候选 | 当前状态里在比较什么行动候选 | 为了明确价值表到底在比较什么 |
| 累积回报标准 | 相比眼前收益，长期上把什么视为更好 | 为了显示 Q-value 不是短期记分板 |
| 失败成本 | 错误 exploration 或绕路带来的损失 | 为了追问高值在真实运营里是不是也安全 |
| 下一步调整问题 | 乐观更新和保守更新哪种更适合 | 为了把 Q-learning 与 SARSA 的差异带到下一次实验标准里 |

## 本节要记住的视角

- 价值型强化学习，不是先背 policy，而是先把状态和行动的长期好坏学成值。
- state value 与 action value 不一样，而真正要做行动选择时，action value 往往更直接。
- Q-value 是`在这个状态下做这个行动，接下来整体会有多划算`的预期分数。
- Q-learning 按`看起来最好的下一个行动`来学，SARSA 按`实际做出的下一个行动`来学。
- 这个差别连接着：对掺有 exploration 的行动流，到底有多直接地反映进去。

这一节的核心，不是背两个算法名字，而是读懂价值表是以什么态度被更新的。

| 需要一起看的东西 | 本节先读的问题 | 立刻接到哪里 |
| --- | --- | --- |
| state value 与 action value | 正在把什么样的好坏写成分数？ | 价值表解释与 Q-value 比较 |
| Q-learning 与 SARSA 的差异 | 用看起来最好的下一个行动，还是用实际下一个行动作标准？ | P4-19.2 策略型强化学习 |
| 掺着 exploration 的现实行动流 | 这种更新方式有多乐观或多保守？ | P4-19.3 应用风险与 exploration 成本 |
| 失败成本 | 值高的行动，在真实环境里是不是也承受得起？ | 强化学习应用前的风险复核 |

## 简短检查

- 能说明为什么在行动候选少且容易比较的问题里，价值型视角会先冒出来吗？
- 能解释为什么同样经验下，Q-learning 与 SARSA 会得到不同的值吗？
- 知道高 Q-value 并不立刻等于现实部署上的安全吗？

## 什么时候应先想到这个视角？

- 当行动候选少，而且每个选择的长期好坏可以像记分板一样比较时，就先想到价值型视角。
- 当 Q-learning 与 SARSA 的差别开始模糊时，就重新按`看起来最好的下一个行动`和`实际做出的下一个行动`来分开。
- 当高 Q-value 快要被误读成现实里安全的行动时，就把值估计和部署风险重新拆开来看。

## 来源与参考资料

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., The MIT Press, 2018, 确认日期：2026-06-27. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Christopher J. C. H. Watkins, Peter Dayan, `Q-learning`, Machine Learning, 1992, 确认日期：2026-06-27. [https://link.springer.com/article/10.1007/BF00992698](https://link.springer.com/article/10.1007/BF00992698){: target="_blank" rel="noopener noreferrer" }
- Satinder Singh, Tommi Jaakkola, Michael L. Littman, Csaba Szepesvari, `Convergence Results for Single-Step On-Policy Reinforcement-Learning Algorithms`, Machine Learning, 2000, 确认日期：2026-06-27. [https://link.springer.com/article/10.1023/A:1022689125041](https://link.springer.com/article/10.1023/A:1022689125041){: target="_blank" rel="noopener noreferrer" }
