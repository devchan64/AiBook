# P4-19.6 补充学习：如何第一次阅读 policy gradient 和 likelihood ratio trick

> Section ID: `P4-19.6`
> Version: `v2026.07.10`

一旦开始读 P4-19.2 里的策略型强化学习(policy-based reinforcement learning)，下面这些名字很快就会跟着出现。

- policy gradient theorem
- likelihood ratio trick

这一节不是一路把完整严密证明追到底，而是先去读`为什么策略参数的变化会连到期望奖励的变化`，以及`为什么 log-probability 这种形式会反复出现`。

## 本节范围

这一节回答下面这些问题。

- 为什么 policy gradient 会被读成直接调整策略概率？
- 为什么 likelihood ratio trick 会把 log-probability 和期望值计算连接起来？
- 这种公式感觉，又是怎样继续连到 REINFORCE 和 actor-critic 的解释上的？

这一节集中通过 `策略概率`、`期望奖励`、`log-probability gradient` 这三个把手，建立策略型公式的入门感觉。

## 本节目标

- 能把 policy gradient 解释成`沿着提高期望奖励的方向去调整策略概率的梯度`。
- 能把 likelihood ratio trick 解释成`把概率分布内部的微分改写成 log-probability gradient，从而让计算更容易读`的装置。
- 能说明为什么在 REINFORCE 和 actor-critic 里会出现 `log pi(a|s)` 这样的形式。

## 为什么需要这一节

策略型强化学习用直觉句子来读时并不难，但一旦看见公式，陌生感就会一下子变强。

- 为什么对期望奖励求微分时会冒出对数？
- 为什么动作概率的梯度会和奖励相乘？

likelihood ratio trick，正是在这里出现的。

所以，这一节的核心，是第一次把`直接调整策略`这句话，和公式里的`log-probability 的梯度`连起来。

## policy gradient 到底在对什么求微分

策略型强化学习最终带着的问题是：

`如果策略参数发生一点小变化，长程期望奖励会朝哪个方向变得更大？`

所以，如果用一句很短的话来讲，policy gradient 就是：

`把策略参数朝着提高期望奖励的方向移动所需要的梯度`

入门时，只要先抓住下面这些就够了。

| 阅读问题 | policy gradient 在说什么 |
| --- | --- |
| 被改变的是什么 | 策略参数 |
| 为什么要改 | 为了让期望奖励更大 |
| 用什么信号来改 | 让带来好奖励的动作更常出现，让带来坏奖励的动作更少出现 |

所以，policy gradient 更应该被读成`直接微调策略分布的更新`。

## 为什么会出现 likelihood ratio trick

当概率分布坐落在期望值内部时，微分会变得别扭。likelihood ratio trick 就是在这个位置经常出现的一种变形。

它的核心感觉可以压成一句话：

`与其直接对概率本身求微分，不如把它改写成 log-probability 的梯度，这样在期望值里面更容易读。`

如果只把形式很短地写出来，会像下面这样。

```text
grad p(x) = p(x) * grad log p(x)
```

这个式子的作用，是让`位于期望值内部的概率分布微分`，更容易和基于样本的更新连接起来。

所以，对数之所以出现，不是装饰，而是为了改变计算结构本身。

## 那么，REINFORCE 公式应该怎样来读

REINFORCE 的直觉通常可以读成这样一种形式：

`对那些带来好奖励的动作，加强它们的 log-probability 梯度；对那些带来坏奖励的动作，削弱它们的梯度。`

在入门层面，最重要的是下面这个比较。

| 奖励是好的 | 奖励是差的 |
| --- | --- |
| 朝着让这个动作以后更常出现的方向调整 | 朝着让这个动作以后更少出现的方向调整 |
| `log pi(a|s)` 的梯度会被当成强化信号 | 同样的梯度也可能反向成为削弱信号 |

而在这里，likelihood ratio trick 扮演的正是桥梁：它解释了`为什么这种更新会写成 log-probability 形式`。

## 它和 actor-critic 又是怎样连起来的

在 P4-19.2 里看到的 actor-critic，是一种“直接调整策略，同时由 critic 提供更稳定评价信号”的结构。如果从公式感觉来读，它会变成下面这样。

- actor：仍然沿着策略 log-probability 的梯度去调
- critic：给出一个不那么抖动的评价信号，说明这个动作到底有多好

所以，actor-critic 并不是放弃了 policy gradient，而更像是`让乘在那个梯度上的评价信号变得更稳定`的一种方向。

## 案例与示例

### 案例 1. 当你想让好的广告展示比例更常出现，而差的比例更少出现时

假设一个广告展示策略会概率性地选择某种比例，比如 `折扣横幅 70% / 推荐横幅 30%`。如果在某种状态下，提高推荐横幅比例之后，点击后的长期购买变多了，那么策略就会想把这个方向的概率再微微提高一点。反过来，如果即时点击很多，但退款和流失也上升了，那么那个动作的概率就应该往下降的方向走。policy gradient 正可以被读成这种调整问题：`把好的概率调高，把坏的概率调低。`

## 本节要记住的视角

- policy gradient 是把策略参数沿着提高期望奖励的方向移动的梯度。
- likelihood ratio trick 是把概率微分改写成 log-probability gradient，从而让它更容易阅读的装置。
- REINFORCE 和 actor-critic 都可以建立在这种 log-probability gradient 的直觉之上来读。
