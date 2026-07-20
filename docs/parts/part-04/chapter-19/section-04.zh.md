# P4-19.4 补充学习：把 DQN、PPO、RLHF 放回强化学习的大流程里来读

> Section ID: `P4-19.4`
> Version: `v2026.07.20`

读完 P4-19.1 到 P4-19.3 之后，继续学强化学习时，很快就会遇到更多名字。

- DQN
- PPO, TRPO, A2C, A3C
- safe reinforcement learning
- offline reinforcement learning
- domain randomization
- RLHF, preference optimization

这些名字来自不同时代、不同瓶颈，但很容易一起涌进来。这一节不去学每个实现，而是集中整理`为什么这些名字会分叉出来`

这个补充学习 Section 不会再从头解释强化学习的基本定义。价值型强化学习的把手留在 P4-19.1，策略型强化学习的把手留在 P4-19.2，应用风险的把手留在 P4-19.3 与[概念词汇表](/AiBook/en/reference/concept-glossary/)。这里做的，只是把后面出现的名字按谱系收一下。

## 本补充学习的范围

这一节回答下面这些问题。

- 为什么 DQN 常被当作价值型强化学习最代表性的后续例子？
- PPO、TRPO、A2C、A3C 想缓解策略型强化学习里的什么困难？
- 为什么 safe RL、offline RL 会在现实应用语境里变成单独主题？
- domain randomization 和 sim-to-real 问题是怎么连起来的？
- 为什么 RLHF 会把一般强化学习问题和 LLM 对齐问题接起来？

RLHF 的详细训练流水线和对齐实践，会在 Part 5 再回来。

## 用补充学习：把 DQN、PPO、RLHF 放回强化学习的大流程里来读恢复的概念连接

- 能把强化学习后续名字整理成四个分支：价值型扩展、策略型稳定化、现实约束强化、LLM 对齐连接。
- 能说明 DQN 和 PPO 分别站在什么传统上。
- 能说出 safe RL、offline RL、domain randomization 都连着`现实里不能随便试`这个问题。
- 能理解 RLHF 不是`把普通强化学习原样搬进 LLM`，而是为了对齐问题重新变形过的后续分支。

## 先画一张大地图

下面这个表可以先抓住整体地图。

| 名字组 | 它主要在回答什么问题 |
| --- | --- |
| DQN | 怎样把价值型强化学习扩展到更大的状态空间？ |
| PPO, TRPO, A2C, A3C | 能不能直接学 policy，但又不要太不稳定？ |
| safe RL, offline RL | 在现实里，能不能减少危险或昂贵的 exploration？ |
| domain randomization | 能不能让 simulation 里学到的 policy 更稳地搬到现实？ |
| RLHF, preference optimization | 能不能通过人类偏好，让 LLM 输出更 desirable？ |

所以，这些后续算法名，不应读成`更聪明的强化学习`，而更应读成`让强化学习在更宽现实约束下工作起来的分支`

第一次看这张图时，最好不要只记名字，也一起记下`最先坏掉的直觉是什么`

| 最先坏掉的直觉 | 因此分出来的名字组 |
| --- | --- |
| Q-table 装不下整个状态空间 | DQN |
| 直接更新 policy 太容易摇晃 | PPO, TRPO, A2C, A3C |
| 现实里不能自由 exploration | safe RL, offline RL |
| simulation 成绩到了现实就保不住 | domain randomization |
| 人类偏好没法直接给成正确标签 | RLHF, preference optimization |

这一节也不要只列名字。哪怕都属于强化学习家族，它们想减掉的失败成本和现实约束也不一样，所以应该先写问题信号，再写名字。

| 名字组 | 最先出现的问题信号 | 为什么需要这个分支 |
| --- | --- | --- |
| DQN | 单靠值表，状态空间太大了 | 为了把价值型直觉扩展到更大的问题 |
| PPO, TRPO, A2C, A3C | policy update 很容易摇晃 | 为了让策略调整更稳定 |
| safe RL, offline RL | 现实里不能随便试 | 为了减少失败成本和数据约束 |
| domain randomization | simulation 成绩一到现实就崩 | 为了缩小 sim-to-real gap |
| RLHF | 人类偏好很难直接当正确标签 | 为了把人类反馈接到类似 reward 的信号上 |

## 先该找哪条后续分支

当后续名字变得很多时，先抓的不是名字，而是`眼前先露出来的瓶颈是什么`

| 最先露出的瓶颈 | 先想到的分支 | 为什么 |
| --- | --- | --- |
| 状态空间太大，Q-table 直觉已经撑不住 | DQN 系 | 中心问题是用 function approximation 扩展价值型视角 |
| policy update 经常摇晃 | PPO、TRPO、actor-critic 系 | 这会直接连到如何让直接学 policy 更稳定 |
| 现实里不能自由 exploration | safe RL、offline RL | 更急迫的是降低失败成本和数据约束 |
| simulation 成绩在现实里保不住 | domain randomization、sim-to-real 强化 | 需要先缩小部署环境差异 |
| 人类偏好必须作用到语言模型输出 | RLHF、preference optimization | 这里 alignment 与人类反馈解释比普通控制更居中 |

所以，找后续名字，不是在选`哪个算法更有名`，而是在先分：现在的瓶颈更像是状态表达、策略稳定化、现实约束，还是人类偏好接入。

## 为什么 DQN 总被单独拿出来说

P4-19.1 里的 Q-learning 很有直觉，但一旦状态和行动变大，表(table)就写不下所有值。DQN 就是在这个地方出现的。

也就是说，DQN 是一种`不用表而改用函数近似器来表达 Q-value，从而处理更大状态空间`的路径。

所以，DQN 不是全新哲学，而是价值型强化学习往更大问题扩展时最代表性的案例。

把这条流再写得紧一点，就是下面这样。

| 从 Q-learning 直觉里保留下来的东西 | 在 DQN 里改变的东西 |
| --- | --- |
| 仍然在问`哪个行动的 value 更大` | 值不再由表表达，而改由近似器表达 |
| 仍然通过 value 比较来选行动 | 让更大的状态空间变得可处理 |
| 继续保留价值型视角 | 一旦引入神经网络等近似器，解释会变得没那么直观 |

所以，DQN 更适合被读成`把价值型直觉搬到更大状态空间里的名字`，而不是`抛弃了价值型学习的名字`

## 为什么 PPO 和 actor-critic 系这么常用

P4-19.2 里的策略型强化学习有一个优势：可以直接调行动方式。但它也容易摇晃。PPO、TRPO、A2C、A3C 这些名字，大多都在回应这个问题。

- 希望 policy 不要一下子变太大
- 希望学习信号不要忽上忽下
- 希望 actor 与 critic 的分工能更稳定地工作

| 家族 | 入门式读法 |
| --- | --- |
| TRPO, PPO | 一条不想让 policy 一次晃太大的路线 |
| A2C, A3C | 一条想更实际地运营 actor-critic 结构的路线 |

所以，这些名字是对`策略型强化学习在实践里容易摇晃`的后续回答。

如果把它再读直接一点，就是下面这样。

| 最先看到的困难 | 后续家族想减掉什么 |
| --- | --- |
| 一次更新会把 policy 改得太大 | update 幅度 |
| reward signal 起伏太大 | 学习方差 |
| 想直接学 policy，但又舍不得完全丢掉 value 信息 | actor 与 critic 分工的不稳定 |

因此，PPO、TRPO、A2C、A3C 虽然名字不同，但共享的方向都是：`保留直接学 policy 的优点，同时别让它不稳定地崩掉`

## 为什么 safe RL 和 offline RL 会变成单独主题

正如 P4-19.3 所说，现实里 exploration 本身就可能危险或昂贵。所以后来长出了两条单独分支。

- safe RL：即使继续探索和改 policy，也要更严格处理风险约束
- offline RL：少做新的探索，优先在已经收集好的数据里学 policy

这两条都来自同一个现实问题：`我们不能想试什么就试什么`

但把它们并在一起时，差异也要一起留下。

| 分支 | 最先想减少的风险 | 基本想法 |
| --- | --- | --- |
| safe RL | 尝试过程中可能直接发生的风险 | 继续探索和学习，但加更严格约束 |
| offline RL | 新尝试本身带来的成本和风险 | 先在已有数据里学习 |

所以，两者都来自现实约束，但 safe RL 更接近`还要试，但要更安全`，offline RL 更接近`少试，先用现成数据学`

## 为什么 domain randomization 会和 sim-to-real 连起来

simulation 里学得好的 policy 到现实里失败，其中一个原因就是环境差异。domain randomization 可以被理解成：故意把 simulator 条件摇得更丰富一些，让 policy 对现实差异没那么脆弱。

它的核心想法就是：

`如果没法完美复制现实，那就别让系统只在一种过于干净的模拟条件里学。`

再具体一点，可以写成下面这样。

| 只贴着一种模拟条件去训练时 | 故意摇动条件时期待得到什么 |
| --- | --- |
| policy 过度适应某一种光照、摩擦或延迟 | 希望得到对现实差异不那么敏感的 policy |
| 在 simulator 里分数很高 | 希望降低现实里突然崩掉的机会 |

所以，domain randomization 更适合被读成`不让学习器只看到过于干净世界的强化手段`，而不是`最大化 simulator 分数的技巧`

## 为什么 RLHF 在这里重要，而且还要在 Part 5 再看

RLHF，reinforcement learning from human feedback，从名字上看像是强化学习的一条分支。但在 LLM 语境里，它并不是把普通的游戏或机器人控制问题直接搬过去。

- 在 LLM 里，人类偏好和评价标准往往很难直接变成正确标签
- 所以才出现了把人类反馈转换成类似 reward 的信号，再由此调整 policy 的流
- 在这里，强化学习语言和 alignment 语言会碰到一起

所以，RLHF 虽然属于强化学习一般论的一部分，但因为它又属于 LLM 对齐这个单独语境，所以还必须在 Part 5 里再详细看一遍。

如果把它和一般强化学习问题并排，会更清楚。

| 比较点 | 一般控制问题里的强化学习 | RLHF 主要处理的一边 |
| --- | --- | --- |
| 行动对象 | 移动、控制、选择动作 | 文本输出 policy |
| 和人类目标的连接 | 通过 reward 设计间接连接 | 更直接地把人类偏好反馈反映进去 |
| 为什么会单独变难 | exploration 与环境反馈本身很难 | 偏好解释与 alignment 目标很难 |

所以，RLHF 不该只被读成`LLM 也用了 RL`，而应该被读成`如何把人类反馈解释成类似 reward`这个问题被推到台前的一条分支。

| 现在在 Part 4 先固定的东西 | 在 Part 5 再看的东西 |
| --- | --- |
| RLHF 为什么会和强化学习谱系连起来 | RLHF 在 LLM 训练流水线里处在什么位置 |
| 人类反馈可以被当成类似 reward 的东西 | reward model、preference data、alignment procedure |

## 案例与例子

### 案例 1. 当 DQN、PPO、RLHF 同时出现时，最先要分开什么

强化学习初学者找资料时，很容易在同一个位置连续碰到 DQN 的游戏表现、PPO 的策略稳定化、RLHF 的 LLM 对齐说明。人最先容易使用的标准，通常是`最近常见的强化学习名字`、`更强的新算法`这种归法。

但这个标准很快就会露出限制。只按新旧或知名度把名字放在一起，`为什么 DQN 会出现`、`为什么 PPO 会被广泛使用`、`为什么 RLHF 必须和普通控制问题分开读`都会变模糊。实际上，这三个名字并不是因为都属于`更好的强化学习`才并排出现，而是因为它们分别回应了不同的瓶颈。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-4-mermaid-01-zh.mmd"
```

| 遇到的名字 | 人最先容易按什么标准归组 | 很快露出的限制 | 当前这一节要切换到的读法 |
| --- | --- | --- | --- |
| DQN | 著名的游戏强化学习算法 | 会遮住它为什么出现在价值型路线里 | 把它读成 Q-table 在更大状态空间里撑不住之后的分支 |
| PPO | 表现很强的新 RL 算法 | 会遮住策略稳定化才是中心问题 | 把它读成减少 policy update 摇晃的分支 |
| RLHF | 把强化学习接到 LLM 上的名字 | 会把人类偏好与 alignment 问题抹掉 | 把它读成人类反馈像 reward 一样接进来的对齐分支 |

如果把这个案例压成 handoff memo，可以写成下面这样。

| 遇到的名字 | 先要读的问题意识 | 下一步要确认的连接 |
| --- | --- | --- |
| DQN | 价值型方法是怎样被扩到更大状态空间的？ | function approximation 与神经网络连接 |
| PPO | policy update 是怎样被做得更不摇晃的？ | actor-critic 与策略稳定化 |
| RLHF | 人类反馈是怎样接到类似 reward 的信号上的？ | Part 5 的 alignment 与 preference optimization |

同一个地方名字越多，越要先记`最先出问题的是什么`，而不是只记`它在算什么`。这个案例里真正要确认的结果，也不是`我知道 DQN、PPO、RLHF 这几个名字了`，而是`我看到这些名字时，最先想到的瓶颈问题有没有变得不同`。这个补充学习的目的，也正是把这种分叉感固定下来。

## 练习与示例

这次练习把重点放在：不是把后续强化学习名字当成`算法名背诵`，而是把它们重新读成`瓶颈与分支`。

问题场景：

- 当 DQN、PPO、offline RL、RLHF 这些名字一起出现时，它们很容易都被看成`更好的强化学习`

输入(input)：

- 四种最先露出的瓶颈
- 对应这些瓶颈的后续分支候选

期待输出(output)：

- 一张先该查哪条分支的对应表

要检查的概念：

- 后续算法名首先该按`它是从什么瓶颈里长出来的`来读，而不是按知名度来读
- 价值型扩展、策略稳定化、现实约束强化、LLM 对齐连接是彼此不同的分支

| 最先露出的瓶颈 | 容易仓促贴上的名字 | 更该先对应的分支 |
| --- | --- | --- |
| 状态空间太大，Q-table 已经撑不住 | PPO | DQN 系 |
| policy update 太摇晃 | DQN | PPO、TRPO、A2C、A3C |
| 现实里没法做很多新 exploration | RLHF | safe RL、offline RL |
| 人类偏好必须作用到语言模型输出 | DQN | RLHF、preference optimization |

### 直接判断一下

看下面这些观察，先选哪种解释更安全。

| 观察 | 仓促结论 | 更安全的解释 |
| --- | --- | --- |
| DQN 和 PPO 都很常被提起 | 它们都是同一种性能升级 | 一个是价值型扩展，一个是策略稳定化路线 |
| offline RL 会单独分出来 | 只是因为数据不够才有这个名字 | 它直接连着现实里不能做很多新探索的约束 |
| RLHF 出现在强化学习列表里 | 是把普通控制问题里的 RL 原样搬进 LLM | 应该把它重新读成把人类偏好像 reward 一样接进去的对齐问题 |

这张表的目的不是背名字，而是养成一种习惯：立刻先分`最先露出的瓶颈是什么`，以及`因此先该看哪条分支`。

## 检查清单

- 能不能说明 DQN 是把价值型强化学习扩展到更大状态空间的一条路线，而 PPO、TRPO、A2C、A3C 是试图减少策略型强化学习不稳定性的路线？
- 能不能说明 safe RL、offline RL、domain randomization 都是因为现实约束与部署风险才长出来的分支？
- 能不能说明 RLHF 是强化学习和 LLM 对齐相遇的地方？
- 当很多名字一起出现时，是否已经养成先问`这个名字是从什么瓶颈里长出来的`的习惯？

## 来源与参考资料

- Richard S. Sutton, Andrew G. Barto, [Reinforcement Learning: An Introduction, 2nd ed.](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-07-01.
- Volodymyr Mnih et al., [Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-07-01.
- John Schulman et al., [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-07-01.
- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-07-01.
