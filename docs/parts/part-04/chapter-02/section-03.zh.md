# P4-2.3 强化学习

> Section ID: `P4-2.3`
> Version: `v2026.07.25`

在 P4-2.1 里，我们看的是通过带 [label](/AiBook/zh/reference/concept-glossary-pinyin/l/#label) 的数据来学习的 [监督学习](/AiBook/zh/reference/concept-glossary-pinyin/j/#supervised-learning)；在 P4-2.2 里，我们看的是在没有 label 的数据里寻找结构的 [无监督学习](/AiBook/zh/reference/concept-glossary-pinyin/w/#unsupervised-learning)。这一次要看的是：[强化学习](/AiBook/zh/reference/concept-glossary-pinyin/q/#reinforcement-learning)，也就是 model 通过 [action](/AiBook/zh/reference/concept-glossary-pinyin/a/#action)、得到 [reward](/AiBook/zh/reference/concept-glossary-pinyin/j/#reward)，并据此调整下一步行动方式的学习。

强化学习不同于 `看着正确 label 来匹配答案` 的学习。它并不会总是立刻告诉你哪个动作最好，而是让系统在执行动作之后，根据返回的 reward 和下一状态，逐渐找到更好的行动方式。所以强化学习处理的不是单次输入输出，而是随着时间连续展开的一串选择。

这一节会说明 reinforcement learning、[state](/AiBook/zh/reference/concept-glossary-pinyin/z/#state)、action、reward、[policy](/AiBook/zh/reference/concept-glossary-pinyin/c/#policy) 的基本区分。后面的章节会带着这个抓手继续判断当前语境，而基于长期奖励的学习到底是什么意思这个基础含义，会通过本节和 [概念词汇表](/AiBook/zh/reference/concept-glossary/) 再次接回。

## 本节范围

这一节解释强化学习的基本结构。像 Q-learning、SARSA、policy gradient、actor-critic 这样的具体算法公式和实现，这里不会展开。Q-learning 和 SARSA 会在 P4-19.1 的 value-based reinforcement learning 中再次出现，policy gradient 和 actor-critic 会在 P4-19.2 的 policy-based reinforcement learning 中再次出现。现在最重要的是先把 [强化学习智能体](/AiBook/zh/reference/concept-glossary-pinyin/q/#reinforcement-learning-agent)、[强化学习环境](/AiBook/zh/reference/concept-glossary-pinyin/e/#reinforcement-learning-environment)、state、action、reward、policy 之间的关系立清楚。

- reinforcement learning 和 supervised learning、unsupervised learning 有什么不同？
- 强化学习智能体和强化学习环境分别是什么？
- state、action、reward、policy 是怎样连起来的？
- 为什么延迟奖励会让问题变难？
- 为什么 [exploration](/AiBook/zh/reference/concept-glossary-pinyin/e/#exploration) 和 [exploitation](/AiBook/zh/reference/concept-glossary-pinyin/e/#exploitation) 必须同时存在？

## 用强化学习留下的判断标准

- 能把强化学习说明成 `通过动作和奖励来学习 policy 的方法`。
- 能区分强化学习智能体、强化学习环境、state、action、reward、policy 的角色。
- 能理解强化学习比起一次性的 prediction，更接近 sequential decision making。
- 能说明 immediate reward 和 long-term reward 可能不一样。
- 能用例子说明为什么 exploration 和 exploitation 之间需要平衡。

## 先用一个场景来理解

想一个小型游戏：角色在格子地图上移动，抵达目标点就会得分。

| 元素 | 简单说明 | 游戏例子 |
| --- | --- | --- |
| 强化学习智能体 | 选择动作的主体 | 角色 |
| 强化学习环境 | 强化学习智能体行动的世界 | 格子地图和规则 |
| state | 表示当前情况的信息 | 角色当前位置 |
| action | 可以选择的动作 | 上、下、左、右 |
| reward | 动作结果返回的数字信号 | 到达目标 `+10`，撞墙 `-1` |
| policy | 在某种 state 下决定做什么 action 的方式 | `朝着更接近目标的方向移动` |

如果是监督学习，可能会已经存在像 `在这个位置往右才是正确答案` 这样的 label。强化学习通常不是这样，而是 强化学习智能体先去尝试动作，再根据得到的 reward 来调整下一次怎么行动。

## 强化学习的基本流程

强化学习最基本的结构，是强化学习智能体和强化学习环境之间不断重复的交互。

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-3-mermaid-01-zh.mmd"
```

这张图里最重要的是循环。强化学习不是看一次输入、给一次输出的单步问题，而是 `强化学习智能体动作`、`强化学习环境改变`、`reward 返回`，再把这次经验用于下一轮 policy 调整的重复过程。

MIT Press 的 Sutton 和 Barto 教材，也把强化学习说明成：强化学习智能体在复杂且不确定的环境中交互，并试图最大化累计 reward 的一种计算方法。这里会把它改写成读者更容易读懂的形式：`先行动、再看结果、然后调整下一次的选择方式。`

## 监督学习、无监督学习、强化学习的比较

这三种学习都可以说是在从数据或经验里学东西，但问题的形状不同。

| 区分 | 起点 | 核心问题 | 简单例子 |
| --- | --- | --- | --- |
| supervised learning | 输入和 label | 这个输入的正确输出是什么？ | 这封邮件是不是垃圾邮件？ |
| unsupervised learning | 没有 label 的输入 | 数据里有什么结构？ | 客户会怎样分组？ |
| reinforcement learning | state、action、reward | 怎样的行动方式能让长期 reward 更高？ | 在这个游戏里该怎么走才能得分更高？ |

强化学习表面上也像 `没有 label 的学习`，但它和无监督学习并不相同。无监督学习关注的是数据结构，而强化学习关注的是 `选择动作`、`接收 reward`、`更新行动方式` 这一条连续流程。

## policy 是选择动作的方式

policy 是强化学习里非常重要的词。它表示：在某个 state 下，系统会怎样决定下一步 action。

如果还是用格子游戏来读，policy 可以像下面这样理解。

| 当前 state | 可选 action | policy 选择的 action |
| --- | --- | --- |
| 目标在右边 | 上、下、左、右 | 右 |
| 正前方有墙 | 上、下、左、右 | 下 |
| 离目标还很远 | 多个方向都可能 | 先试一试尚未充分探索的方向 |

policy 一开始不一定就是好规则。强化学习里，强化学习智能体会在不断尝试动作的过程中去改进 policy。这个 policy 可以是人写的规则，也可以是训练过程中不断调整的函数。

## reward 不是立刻告诉你的答案

reward 是对动作结果进行评价的数字信号。但它不像监督学习里的 label 那样，每次都直接告诉你 `这个动作就是正确答案`。

有些动作现在看起来像亏了，但以后可能会换来更大的 reward；反过来，有些动作虽然现在立刻拿到一点收益，长期看却可能是更差的选择。

例如，在游戏里，为了到达最终目标，可能需要先绕一下路。

| 选择 | 立刻发生的结果 | 长期结果 |
| --- | --- | --- |
| 先拿近处的小分数 | 当下 `+1` | 可能会让到达最终目标更慢 |
| 暂时不拿分而绕路 | 当下 `0` | 可能换来抵达目标的 `+10` |

正因为如此，强化学习里必须区分 `现在看起来好` 和 `以后整体更好`。这正是强化学习既难又有意思的核心之一。

如果把它换成优惠券推荐的例子，就会更清楚：只有把 `即时点击` 和 `后续购买` 一起读进去，它才真正像一个强化学习问题。

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-3-mermaid-02-zh.mmd"
```

## exploration 和 exploitation

在强化学习里，exploration 和 exploitation 必须一起考虑。

exploration 指的是去尝试还不熟悉的动作；exploitation 指的是优先使用已经看起来不错的动作。

| 选择方式 | 含义 | 优点 | 风险 |
| --- | --- | --- | --- |
| exploration | 去尝试新的动作 | 可能会发现更好的路径 | 当下 reward 可能更低 |
| exploitation | 选择已经看起来不错的动作 | 可以更稳定地拿到 reward | 可能永远发现不了更好的选择 |

拿选餐厅来比喻会更直观。你去已经喜欢的餐厅，失败概率很低；但如果你从不尝试新餐厅，也很难发现更好的选项。强化学习也是这样：既要利用已有经验，又必须留出足够空间去试新的动作。

## 在现实问题里要小心的点

强化学习经常出现在游戏、机器人、自动驾驶模拟等 `动作和结果会连续相连` 的问题里。但它并不容易直接搬到现实中。

- reward 设计错了，系统可能学到你并不想要的行为。
- 如果在真实环境里盲目 exploration，成本和风险会很高。
- 如果结果来得很晚，就很难知道到底是哪一个动作带来了好结果。
- 在模拟环境里表现好的 policy，不能自动假设在现实里也同样好用。
- 这里的强化学习智能体 和 LLM 服务语境里的 AI agent，不一定是同一个意思。

最后这一点尤其重要。强化学习里的强化学习智能体，是在环境中观察 state、选择 action、接收 reward 的学习主体；而 LLM 服务里说的 AI agent，常常指的是 `把目标拆成工作流并调用工具的执行结构`。它们可以有关联，但如果把这两个词混着当成同义词，就会很容易混乱。

## 它会在哪里再次和 LLM 相遇

到了 Part 5 看 LLM 与 generative AI 时，强化学习会再次出现。尤其是利用人的偏好来调整模型输出的那条路线，会在 P5-10.1 instruction tuning 和 P5-10.2 alignment 的基础问题里再次被提到。

但这一节不会深讲 LLM alignment 或 RLHF。现在最需要先立住的是：强化学习应该被区分成 `通过 reward 来调整行动方式的学习`。

当你先检查 `当前问题是不是要按 sequential decision making 和 reward flow 来读` 时，是否属于强化学习就会清楚得多。

| 当前状态 | 要不要按强化学习来读 | 原因 |
| --- | --- | --- |
| 做出一个动作之后会收到 reward，而且下一步选择会继续受它影响 | 要 | 因为问题核心是连续决策，而不是一次性匹配答案 |
| 比起当前分数，更需要追求长期 reward | 要 | 因为 immediate reward 和 long-term reward 的张力就在问题中心 |
| 已经有输入和正确 label，而且一次性 prediction 才是核心 | 通常不要 | 因为那更直接是监督学习问题 |

## 案例与示例

### 案例 1. 当优惠券推荐要在提高即时点击和提高长期购买之间做选择时

假设某个服务想自动决定：优先给用户展示哪一张优惠券。人很容易先觉得：只要一直展示点击率最高的优惠券不就行了吗？

但即时点击高，并不代表长期销售额或回访率也会更好。有些优惠券点击不高，却会带来后续购买；有些优惠券点击很多，却可能在长期上反而吃亏。

这种问题和监督学习不一样，因为它不是给定一次输入、匹配一次正确 label，而是必须把动作之后的 reward 流一起读进去。所以强化学习会围绕 state、action、reward、policy 来说明，并且把即时 reward 和长期 reward 一起考虑。

真正可检查的结果，会在 policy 对比里出现。如果 `点击率更高的 policy` 和 `长期购买 reward 更高的 policy` 并不相同，那这个问题就已经更接近 `连续决策与奖励设计`，而不是简单分类。

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-3-mermaid-03-zh.mmd"
```

## 检查清单

- 能不能说明在什么状态下，问题应该按强化学习而不是监督学习来读？
- 能不能说明为什么 reward 不像 label 那样立刻告诉你正确答案？
- 能不能说明为什么不能把强化学习里的强化学习智能体 和 LLM 服务里的 agent 当成同一个意思？
- 能不能说明强化学习是强化学习智能体在强化学习环境中交互，并根据 reward 改进 policy 的学习？
- 能不能说明为什么 state、action、reward、policy 是阅读强化学习时最基本的词？
- 能不能说明如果没有 exploration 和 exploitation 的平衡，就很难同时做到 `找到更好动作` 和 `稳定拿到 reward`？

## 来源与参考资料

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 第 2 版，MIT Press，2018，确认日期：2026-07-26. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Olivier Buffet, Olivier Pietquin, Paul Weng, `Reinforcement Learning`, arXiv, 2020，确认日期：2026-07-26. [https://arxiv.org/abs/2005.14419](https://arxiv.org/abs/2005.14419){: target="_blank" rel="noopener noreferrer" }
