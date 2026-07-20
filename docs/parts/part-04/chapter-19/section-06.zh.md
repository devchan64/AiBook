# P4-19.6 补充学习：如何第一次阅读 policy gradient 和 likelihood ratio trick

> Section ID: `P4-19.6`
> Version: `v2026.07.19`

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

假设一个广告展示策略会概率性地选择某种比例，比如 `折扣横幅 70% / 推荐横幅 30%`。人最容易先采用的规则，通常是`这次效果好的横幅比例，下次就更常用一点`。

这个直觉方向是对的，但一旦公式出现，很快就会变得发虚。`为什么是在直接改概率？`、`为什么会冒出 log-probability？`、`为什么同一个动作会因为奖励正负而往相反方向调整？`这些问题都会马上出现。policy gradient 和 likelihood ratio trick 正是在这里把`把好的概率调高，把坏的概率调低`这一直觉，接到可读的公式解释上。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-6-mermaid-01-zh.mmd"
```

| 问题场景 | 人最容易先采用的规则 | 很快出现的限制 | 这一节补上的解释 |
| --- | --- | --- | --- |
| 推荐横幅占比提高后，长期购买增加了 | 下次更常用这个比例 | 还说不清概率更新该怎样写进计算 | 读成沿着提高期望奖励方向移动的 policy gradient |
| 点击升高了，但退款和流失也升高了 | 把这个比例降下来 | 很难用公式解释为什么同一个动作现在收到反向信号 | 通过奖励符号和 log-probability 梯度来读 |
| 公式里出现 `log pi(a|s)` | 看起来像困难的数学装饰 | 概率微分和基于样本的更新之间还没连上 | 通过 likelihood ratio trick 来读 |

这个案例真正要确认的结果是：`好的比例更常出现，差的比例更少出现`这句话，现在能不能通过 `期望奖励`、`log-probability gradient`、`奖励符号` 这三个把手重新读回来。也就是说，公式不该抹掉策略型直觉，而应该把那种直觉写得更精确。

## 练习与示例

这个练习的重点，是用很小的数字直接看到：`好奖励 -> 强化所选动作概率`、`坏奖励 -> 削弱它`，以及`为什么 log-probability 会一起出现`。

问题场景：

- policy gradient 和 likelihood ratio trick 只看名字会很抽象，但实际是在计算“所选动作的概率该往哪个方向推”

输入(input)：

- 所选动作的概率 `0.7`
- 对数概率 `log(0.7)`
- 同一个动作对应的一次正奖励和一次负奖励

期望输出(output)：

- 对数概率值
- 随奖励符号变化而改变的解释方向

要确认的概念：

- log-probability 是把所选动作概率连到更新计算上的阅读把手
- 奖励符号一变，同一个动作的调整方向也会跟着变

```python
# 这个例子展示所选动作的 log-probability 和奖励符号如何改变 policy update 的解释方向。
import math

chosen_prob = 0.7
log_prob = math.log(chosen_prob)

positive_reward = 2.0
negative_reward = -2.0

print("log pi(a|s) =", round(log_prob, 3))
print("positive signal =", round(positive_reward * log_prob, 3))
print("negative signal =", round(negative_reward * log_prob, 3))
```

这个例子的结果可以像下面这样来读。

```text
log pi(a|s) = -0.357
positive signal = -0.713
negative signal = 0.713
```

这个例子里最重要的，并不是把符号本身背下来。

1. `log pi(a|s)` 是把所选动作概率连到更新计算上的阅读把手。
2. 即使是同一个动作，奖励是好的时，要读成“让它更常出现”的方向；奖励是坏的时，要读成“让它更少出现”的方向。
3. likelihood ratio trick 的作用，就是把`概率微分`改写成`log-probability gradient`，让这种连接更容易读出来。

### 直接判断一下

看看下面这些观察，先选哪个解释更安全。

| 观察 | 过快下的结论 | 更安全的解释 |
| --- | --- | --- |
| `log pi(a|s)` 是负数 | 策略错了 | 只要概率小于 1，对数就可能是负的，真正重要的是它和奖励相乘后的调整方向 |
| 给同一个动作分别乘上正奖励和负奖励后，信号符号变了 | 公式不稳定 | 奖励符号改变了“这个动作该更常出现还是更少出现”的方向 |
| 公式里出现 log-probability | 只是数学装饰 | 它是把期望值内部的概率微分，更容易连接到基于样本更新上的装置 |

这张表的目的，不是证明公式，而是抓住解释：`策略概率到底是怎样被推高或压低的`，以及`为什么这种连接需要 log-probability`。

## 检查清单

- 你能否说明，policy gradient 是把策略参数往提高期望奖励方向移动的梯度？
- 你能否说明，likelihood ratio trick 是把概率微分改写成 log-probability gradient，从而让它更容易读？
- 你能否说明，REINFORCE 和 actor-critic 都建立在这种 log-probability gradient 的直觉之上？
- 你能否说明，正奖励和负奖励会让所选动作的概率往不同方向调整？

## 来源与参考资料

- Ronald J. Williams, `Simple statistical gradient-following algorithms for connectionist reinforcement learning`, Machine Learning, 1992. 用于确认 REINFORCE 系列算法和 expected reinforcement 的 gradient-following 视角。确认日期: 2026-07-19. [https://doi.org/10.1007/BF00992696](https://doi.org/10.1007/BF00992696){: target="_blank" rel="noopener noreferrer" }
- Richard S. Sutton, David McAllester, Satinder Singh, Yishay Mansour, `Policy Gradient Methods for Reinforcement Learning with Function Approximation`, NeurIPS 1999. 用于确认 policy gradient theorem、近似 value/advantage function 与经验估计之间的连接。确认日期: 2026-07-19. [https://papers.nips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html](https://papers.nips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Vijay R. Konda, John N. Tsitsiklis, `On Actor-Critic Algorithms`, SIAM Journal on Control and Optimization, 2003. 用于确认把 actor-critic 连接到 policy-gradient 方法中评价信号稳定化的视角。确认日期: 2026-07-19. [https://doi.org/10.1137/S0363012901385691](https://doi.org/10.1137/S0363012901385691){: target="_blank" rel="noopener noreferrer" }
