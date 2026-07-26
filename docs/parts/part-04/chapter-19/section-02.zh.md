# P4-19.2 策略型强化学习

> Section ID: `P4-19.2`
> Version: `v2026.07.26`

在 P4-19.1 里，我们已经看过[价值型强化学习(value-based reinforcement learning)](/AiBook/zh/reference/concept-glossary-pinyin/j/#value-based-reinforcement-learning)把`什么状态里什么行动有多好`学成 value 的视角。如果把问题再换一步，下面的问题就会出现。

不经过 value 再去选行动，能不能直接调整行动方式(policy)本身？

从这个问题出发的，就是[策略型强化学习(policy-based reinforcement learning)](/AiBook/zh/reference/concept-glossary-pinyin/c/#policy-based-reinforcement-learning)。

策略型强化学习，不是先造一个行动记分板，而是直接调整行动选择的概率与方式，让系统学会拿到更大的 reward。

这一节解释 [policy-based reinforcement learning](/AiBook/zh/reference/concept-glossary-pinyin/c/#policy-based-reinforcement-learning)、[policy gradient](/AiBook/zh/reference/concept-glossary-pinyin/c/#policy-gradient)、[actor-critic](/AiBook/zh/reference/concept-glossary-pinyin/a/#actor-critic) 的基本含义。后面的 Section 会在这个把手上继续当前语境里的判断，而“直接调整行动方式”的强化学习基本感觉，会再次通过这一节和相关概念词汇表条目连回来。

## 策略型强化学习先收束的问题

这一节回答下面这些问题。

- 直接学习 policy，到底是什么意思？
- 价值型强化学习和策略型强化学习哪里不同？
- policy gradient 是按什么想法调整 policy 的？
- actor-critic 为什么会出现？
- 策略型强化学习在哪些问题里会更自然？

这一节先收住`为什么会出现直接调整 policy 本身的强化学习`这个问题。reward 设计与现实应用约束会在 P4-19.3 继续，PPO、TRPO、A2C、A3C 与 continuous control 的扩展流程会在 P4-19.4 继续，policy-gradient theorem 与 likelihood ratio trick 的最小数学感觉会在补充学习 P4-19.6 继续。

## 策略型强化学习要留下的判断标准

- 能把策略型强化学习解释成`直接调整行动概率与行动方式的做法`。
- 能区分价值型与策略型方法在提问上的差异。
- 能把 policy gradient 解释成`让高 reward 的行动更常出现，让低 reward 的行动更少出现`的想法。
- 能说明 actor-critic 为什么把 policy 调整和值估计一起使用。
- 能理解为什么策略型强化学习常常出现在连续行动或复杂 policy 表达的问题里。

## 为什么要直接学习 policy

价值型强化学习很强，但不是所有问题都容易读成 Q-table。

- 行动数可能太多
- 行动可能是连续值
- `选一个最高分行动`这种表达方式可能并不自然

想象一下，直接调整机器人手臂的角度。

- 行动不是只有 `left / right`
- 它可能是 `0.1 度`、`0.2 度`、`0.3 度` 这样极多、甚至几乎连续的值

在这种场景里，比起`给每个行动都写一个分数`，`直接决定当前状态下要形成什么样的行动分布`会更自然。

如果把这个差别读得更接近实际操作，就是下面这样。

| 问题场景 | 为什么记分板方法会变得别扭 | 为什么策略型方法更自然 |
| --- | --- | --- |
| 机器人手臂角度调整 | 可选行动太多 | 直接输出角度和力量的倾向更合适 |
| 自动移动体转向 | 很难只分成几个像 `left/right` 的动作 | 直接处理连续转向量更自然 |
| 概率性战术选择 | 只选一个最高行动太粗糙 | 可以直接调整行动比例本身 |
| 推荐里的曝光比例实验 | 很难为每个比例单独写值 | 更容易直接处理每个选择该出现多频繁 |

所以，策略型强化学习更接近下面这个问题。

`在当前这个状态里，要让什么行动以多大频率出现？`

如果把它画得非常简单，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-01-zh.mmd"
```

这个图显示的是：policy 不一定只是吐出`唯一正确行动`，它也可以在看到状态后，直接生成多个行动候选的倾向或强度。也正因为如此，策略型强化学习会被读成一种不经过记分板、直接调整行动分布本身的视角。

这个图最关键的是：policy 不是`只选一个行动的开关`，它也可以是生成多个行动候选倾向或分布的表达。

## 直接学习 policy 是什么意思

在 P4-2.3 里，policy 被定义成`在什么状态下做什么行动的方法`。而在策略型强化学习里，这个 policy 本身就被视为直接调整对象。

说得更直白一点：

- 价值型强化学习：先做一个行动记分板，再根据记分板选行动
- 策略型强化学习：直接一点点改行动方式本身

并排比较可以写成下面这样。

| 视角 | 中心问题 | 代表直觉 |
| --- | --- | --- |
| 价值型 | 这个行动的长期得分是多少？ | 先看记分板再选 |
| 策略型 | 在这个状态下要形成什么行动分布？ | 直接调整行动方式 |

在策略型方法里，policy 经常会被表示成概率分布(probability distribution)。

例如，在同一个状态下：

- 向右走的概率 0.7
- 向上走的概率 0.2
- 向左走的概率 0.1

这样，policy 本身就会变成包含`行动选择倾向`的模型。

如果把这个例子再具体一点，可以写成下面这样。

| 状态 | 行动候选 | 当前 policy 的解释 |
| --- | --- | --- |
| 刚绕过障碍物后的行驶状态 | `直行 0.6`、`轻微左转 0.3`、`轻微右转 0.1` | 主要直行，但经常需要一点左侧修正 |
| 与箱子稍微错位的抓取状态 | `轻抓 0.2`、`中等力度 0.5`、`强抓 0.3` | 中等力度最常划算，但偶尔也需要更强力度 |

这个表最关键的是：policy 说的不是`唯一正确行动`，而是当前状态下什么行动倾向应该更常出现。

这时重要的是，policy 不是`行动名称列表`，而是`行动会怎样被产出的方法`。

| 读同一个状态时的问题 | 价值型先看的东西 | 策略型先看的东西 |
| --- | --- | --- |
| 现在什么更好？ | 每个行动的长期得分 | 什么行动应当出现得更频繁 |
| 更新后什么会变？ | 某个特定行动的值 | 行动概率或控制输出倾向 |
| 失败发生时重新看什么？ | 为什么分数估计错了 | 哪个行动倾向该减少、减少多少 |

把同一个场景拆成价值型与策略型两边来读，差别会更清楚。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-02-zh.mmd"
```

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-03-zh.mmd"
```

第一张图是`比较行动值后再选`，第二张图则是`直接表达行动出现概率的结构`。

## policy gradient 想做什么

policy gradient 是一类代表性方法，它直接调整 policy parameter，让 expected return 上升。

`把 policy 一点点改到这样一个方向：高 reward 的行动更常出现，低 reward 的行动更少出现。`

所以，policy gradient 不是想先把 value table 完成，而是直接去调整`推动 policy 的把手`。

把这种感觉再压短一点，可以写成下面这样。

| 先看到的 reward 经验 | 策略型解释 |
| --- | --- |
| 某个行动反复带来好结果 | 把 policy 往那个行动更常出现的方向推 |
| 某个行动反复带来失败 | 把 policy 往那个行动更少出现的方向拉 |
| 某次结果好但整体很摇晃 | 不要立刻过度相信，要积累多次经验再调倾向 |

压成图，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-04-zh.mmd"
```

这个图的关键点，是把 policy 读成`可调整的行动倾向`，而不是`固定输出规则`。

[REINFORCE](/AiBook/zh/reference/concept-glossary-pinyin/r/#reinforce) 可以看成最直接展示上面 policy-gradient 流程的入门例子。它把一个 episode 里的行动与 reward 收集起来，然后在下一轮 policy 里，提高那些最终有帮助的选择的概率。

放成一个小直觉例子：

- 在同一个状态里，多次尝试 `go straight`，长期上更快到达目标
- 相反，`sharp turn` 虽然也有成功，但平均上制造了更多碰撞与惩罚

这时，REINFORCE 式直觉就是：提高 `go straight` 的概率，降低 `sharp turn` 的概率。

## 为什么 REINFORCE 总是一起出现

在入门文献里，解释 policy gradient 时，REINFORCE 常常一起出现。REINFORCE 是策略型强化学习里最具代表性的早期算法之一。

`沿着一个 episode 走完后，把最终带来更好 reward 的那些选择，在下一轮 policy 里提高其出现概率的方法`

这说明，REINFORCE 用最直接的方式展示了策略型方法的基本哲学。

- 做得好的行动，更常出现
- 做得不好的行动，更少出现

但如果只靠这样做，学习信号会很容易摇晃。正是在这里，actor-critic 出现了。

## actor-critic 为什么会出现

直接调整 policy 很自然，但如果只靠 reward signal 立刻修 policy，波动会很大。因为很容易摇摆：这个行动是真的好，还是只是偶然看起来好？

所以，就会出现把`调整 policy 的一边(actor)`和`评价当前选择到底多合适的一边(critic)`放在一起的想法。

actor-critic 应该这样读。

- actor：调整真实行动方式的一边
- critic：提供这个行动有多合适的评价信号的一边

所以，actor-critic 是把策略型方法和值估计方法混合在一起的结构。

如果把角色再拆细一点，更好读成下面这样。

| 组成部分 | 做什么 | 读者常见误解 | 重新阅读标准 |
| --- | --- | --- | --- |
| actor | 产出真实行动分布或控制输出 | 以为 critic 会代替它选行动 | actor 才真正握着 policy |
| critic | 给出当前选择有多合适的评价信号 | 以为 critic 会告诉正确行动 | critic 是评价者，不是直接选择者 |
| actor-critic 组合 | 同时使用 policy 调整与评价信号 | 以为只是把两个独立算法硬拼在一起 | 应读成降低波动的分工结构 |

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-05-zh.mmd"
```

在这个图里，critic 不是替 actor 决定行动的存在，而是给 actor update 提供更稳定评价信号的角色。

## 价值型与策略型只是互相竞争吗

读者很容易把这两条路线看成`只能二选一的正确做法`。但实际情况是，它们反映的是不同的问题直觉。

| 问题 | 价值型更自然的时候 | 策略型更自然的时候 |
| --- | --- | --- |
| 行动候选少而清楚吗？ | 是 | 没那么明显 |
| 行动是连续的或极多吗？ | 处理起来更麻烦 | 相对更自然 |
| 用记分板选行动容易吗？ | 容易 | 不一定需要 |
| 你想直接控制行动概率本身吗？ | 间接 | 直接 |

所以，策略型强化学习不是替代价值型强化学习，而是在不同条件下提供更自然的表达。

## 它特别常在哪里出现

策略型强化学习常在下面这些场景里被提起。

- 像机器人控制这样行动是连续值的问题
- 比起`选一个最高行动`，更关心整个行动分布的问题
- 想直接处理 stochastic policy 的问题
- 需要大状态空间与复杂 function approximation 的问题

如果换成更现实的例子来读：

| 问题场景 | 为什么策略型视角更合适 |
| --- | --- |
| 机器人手臂控制 | 角度、力度、速度这些行动都可能是连续值 |
| 自动移动体的转向与加速 | 相比少数离散行动，连续控制更自然 |
| 游戏里的概率性战术选择 | 有时需要按情境混合策略，而不是只固定一个行动 |
| 广告或推荐实验中的探索 policy | 可能需要直接处理每个选择该暴露多少比例 |

如果借一个服务运营的比喻：

- 价值型更像在做`每个应对选项的记分板`
- 策略型更像直接调整`按情境让各种应对强度以什么概率出现`

当然，这只是帮助直觉的比喻，不能把真实服务 policy 设计和强化学习 policy 完全混读。

机器人手臂这个例子特别重要。像 `left`、`right` 这种行动很少的问题里，价值型方法可以很直观；但一旦需要同时决定`多少`、`多快`、`多大角度`，直接输出 policy 的那一边就会读起来更自然。

反过来，也不能因此把策略型强化学习读成对所有问题都更好。如果行动候选少，并且能通过记分板清楚比较，价值型方法可能更简单，也更有解释力。

把这个比较再直接写一点：

| 场景 | 为什么容易先想到价值型 | 为什么容易先想到策略型 |
| --- | --- | --- |
| 迷宫里上下左右移动 | 行动候选少，比较容易 | 如果刻意想处理概率性移动 policy，也可以 |
| 机器人手臂的细微角度调整 | 很难用值表装下所有行动 | 直接输出控制量更自然 |
| 游戏战术选择 | 如果是简单选择，值比较就够了 | 如果要按情境混用策略，就更自然 |
| 广告曝光比例实验 | 曝光方案少时，可以先比值 | 曝光比例本身就很适合像 policy 一样调整 |

## 什么时候应该先抓策略型视角

当`先给行动打分，再选最高行动`这条路开始变得别扭时，策略型强化学习会更自然。

| 先看到的问题场景 | 为什么可以先抓策略型视角 | 先要警惕什么 |
| --- | --- | --- |
| 行动是连续的 | 与其把每个行动都列值，不如让 policy 直接输出控制量 | 即使 policy 当下看起来不错，也要单独检查学习摇晃和安全性 |
| 行动分布本身需要被设计 | 关键问题就是每种行动该出现多频繁 | 提高了概率的行动也可能带来副作用 |
| 状态复杂，policy 表达更重要 | 中心问题变成`怎样形成行动倾向`而不是`具体做什么` | 如果不看值估计就直接改 policy，波动会更大 |
| actor-critic 这种角色分工很自然 | 把 policy 调整和评价信号拆开看更容易理解 | 有 critic 并不代表现实部署风险自动消失 |

## 用运营感再读 actor-critic

actor-critic 常被使用，是因为人们希望同时拿到`直接调整 policy 的自由`和`值估计带来的稳定信号`。

- 只有 actor：直接改 policy 很方便，但可能很摇晃
- 再加一个 critic：就能更好地给出当前修改方向是否合适的评价信号

所以，actor-critic 不该被读成让策略型和值类型对立，而应被读成`把两边分工后协作起来的结构`。

如果非常谨慎地贴一个业务比喻：

- actor 是实际提出执行方案的一边
- critic 是对这个执行方案是否比预期更好或更差给反馈的一边

不过，这仍然只是帮助结构直觉的比喻。如果把现实组织里的人和强化学习组件一一对应，就会产生误读。

## 案例与例子

### 案例 1. 当机器人手臂需要一点点调抓取角度时，为什么直接学习 policy 更自然

机器人手臂抓箱子时，不是在 `left` 或 `right` 这几个动作里选一个，而是要连续决定角度与力度该给多少。在这种场景里，比起把所有可能行动都写成表分数，更自然的是直接调整 policy，让某些角度和力度在当前状态下更常出现。策略型强化学习会提高成功抓取动作的概率、降低失败动作的概率，从而直接修整行动分布。所以，在复杂连续控制问题里，`直接修改行动方式`往往比`先做记分板再挑最高值`更贴切。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-06-zh.mmd"
```

把这个案例压成 project memo，可以写成下面这样。

| 当前状态 | policy 更常给出的行动 | 需要一起看的失败成本 | 下一个问题 |
| --- | --- | --- | --- |
| 箱子位置稍微歪斜 | 更大的旋转角度与更强的抓力 | 打滑、过大用力、设备磨损 | 这个概率分布在其他位置误差下也稳定吗？ |
| 需要连续控制的重复作业 | 成功率更高的控制值组合 | 罕见失败可能累积成大损伤 | 要不要再加 critic 信号或额外安全约束？ |

### 案例 2. 当广告曝光比例必须被当成分布，而不是一个正确答案时

假设实验平台要给用户展示三个 banner 候选。有些场景里，与其总是给每个用户固定展示一个 banner，不如按状态让 A 以 60%、B 以 30%、C 以 10% 的比例出现更自然。这时，策略型视角问的就不只是`哪个 banner 最好`，而是直接处理`在什么状态下什么 banner 应该多常出现`。

| 用户状态 | 策略型先读的问题 | 一起要警惕什么 |
| --- | --- | --- |
| 新用户 | 什么 banner 比例能平衡 exploration 与 conversion？ | 会不会因为一次高点击率就过度集中 |
| 回访用户 | 哪个 banner 更常出现更利于长期转化？ | 会不会把短期点击和长期满意度混在一起 |

这个案例说明的是：策略型强化学习更适合处理的，不是`选一个最高行动`，而是`设计行动分布本身`。

例如，可以想象新用户状态下当前 policy 会像下面这样变化。

| Banner | 当前曝光概率 | 观察后要再看的问题 |
| --- | --- | --- |
| A | 0.5 | 点击高，但流失也一起上升了吗？ |
| B | 0.3 | 点击较低，但购买转化是否更稳定？ |
| C | 0.2 | exploration 比例该继续降低还是保留？ |

这个小例子会更清楚地展示：策略型方法并不只是问`A 是不是最强`，而是在直接处理`A、B、C 应该按什么比例一起被展示`。

## 练习与例子

这个例子集中在用数字直接确认策略型强化学习的核心感觉：`提高收到好 reward 的行动概率`。它不会停在只提升一次概率，而是会一起看 reward 符号变掉时，policy 会如何朝相反方向移动。

问题情境：

- 策略型强化学习，不只是改行动记分板，而是改行动被选中的概率本身

输入(input)：

- 当前 policy 的行动分数
- 这次 episode 中选中的行动
- 由此得到的 reward

期望输出(output)：

- 更新前的行动分数
- 反映 reward signal 后的行动分数
- 归一化之后的新行动概率

要确认的概念：

- 收到好 reward 的行动，在下一轮 policy 里可能更常出现
- 在策略型强化学习里，重要的是把行动分数读成概率分布
- 焦点在于改变行动倾向本身，而不是只估值

```python
# 这个例子提高获得好奖励的动作分数，观察新的 policy 概率如何变化。
import math

action_scores = {
    "left": 0.20,
    "right": 0.40,
}

chosen_action = "right"
reward_signal = 1.5
step_size = 0.3

print("before update:", action_scores)

# 把选中的行动分数稍微提高一点。
updated_scores = action_scores.copy()
updated_scores[chosen_action] += step_size * reward_signal

print("score after reward:", updated_scores)

# 用 softmax 归一化，让分数可以像概率一样来读。
exp_left = math.exp(updated_scores["left"])
exp_right = math.exp(updated_scores["right"])
total = exp_left + exp_right

new_policy = {
    "left": round(exp_left / total, 3),
    "right": round(exp_right / total, 3),
}

print("new policy:", new_policy)
```

一个执行结果例子可以读成下面这样。

```text
before update: {'left': 0.2, 'right': 0.4}
score after reward: {'left': 0.2, 'right': 0.85}
new policy: {'left': 0.343, 'right': 0.657}
```

这虽然不是严格的 policy gradient 实现，但它展示了策略型强化学习的核心想法。

- 收到好 reward 的 `right` 分数被提高了
- 结果就是，在新 policy 里 `right` 的概率更大了

也就是说，策略型强化学习会朝着这种方向，直接调整`行动更容易出现的倾向`。

### 改一个值试试：同样的行动如果收到坏 reward，概率会怎样变？

这次仍然选择同样的行动 `right`，但把 reward signal 改成 `-1.0`。

```python
# 这个例子让同一个动作得到坏奖励，观察 softmax policy 概率如何反向变化。
import math

action_scores = {
    "left": 0.20,
    "right": 0.40,
}

chosen_action = "right"
reward_signal = -1.0
step_size = 0.3

updated_scores = action_scores.copy()
updated_scores[chosen_action] += step_size * reward_signal

exp_left = math.exp(updated_scores["left"])
exp_right = math.exp(updated_scores["right"])
total = exp_left + exp_right

new_policy = {
    "left": round(exp_left / total, 3),
    "right": round(exp_right / total, 3),
}

print("score after reward:", updated_scores)
print("new policy:", new_policy)
```

```text
score after reward: {'left': 0.2, 'right': 0.1}
new policy: {'left': 0.525, 'right': 0.475}
```

在好 reward 下，`right` 的概率上升；但在坏 reward 下，同样这个行动的概率就下降。这个比较很清楚地展示了：策略型强化学习不是在`读行动记分板`，而是在`推拉行动倾向`。所以，学习策略型方法时，比起只看某个值大小，更应该先看什么反馈导致了什么行动分布变化。

这个比较的关键在于，策略型强化学习不只是在决定`做什么`，而是在直接调整`什么行动应该更常出现`。评估也要通过`reward 的变化，实际上怎样改变了行动分布`来读取。所以，要真正理解 policy 这个词，就要把`概率分布变化的前后场景`拿来比较。

### 先自己判断一下

先看下面这些观察，再选哪种解释更稳妥。

| 观察 | 草率结论 | 更稳妥的解释 |
| --- | --- | --- |
| `right` 收到好 reward 后，概率变大了 | 以后只要一直选 `right` 就行了 | 当前 policy 倾向于让 `right` 更常被尝试 |
| 同一个行动收到坏 reward 后，概率下降了 | 策略型方法不会用记分板 | 它是按照 reward signal 去推拉行动倾向本身 |
| 出现了一个概率上升的行动 | 这个行动在现实里也一定安全而且最好 | 还要把其他状态和失败成本一起读进去 |

这张表的目的，是不要把策略型方法只背成`改概率数字`。它要让人一起读出：什么 reward signal 导致了什么行动分布变化，以及为什么这种变化并不立刻等于现实安全。

| 共同记录语言 | 这次练习要立刻留下的内容 |
| --- | --- |
| 看见的结构 | 同一个行动，也会因为 reward 符号改变而让 policy 概率朝相反方向移动 |
| 解释边界 | 某个行动概率升高，并不立刻等于它在现实里安全或 desirable |
| 下一个问题 | 这种 policy 分布调整，在别的状态或约束下还能保持吗？ |

这一节也不要只留下 policy 说明。还要一起留下：提出了什么行动分布、需要警惕什么失败成本。因为看起来相近的 reward，也可能让某些 policy 更常制造某类失败，而另一些则更保守，所以行动分布与失败模式必须一起读。

| 一起要留下的项目 | 这一节写的内容 | 为什么需要 |
| --- | --- | --- |
| policy 提案 | 当前状态里让什么行动以什么概率出现 | 为了明确 policy 是行动倾向，而不是记分板 |
| expected reward 标准 | 因为什么 reward，提高了某个行动概率 | 为了把行动分布调整和目标定义连起来 |
| 失败成本边界 | 被提高概率的行动在真实环境里会带来什么副作用 | 因为 policy update 不立刻等于安全 |
| 下一步验证问题 | 这个分布在别的状态和现实约束下能不能站住 | 为了把策略型选择交给后续审查 |

这一节的核心，不是背策略型名字，而是固定住：直接改 policy 到底是什么意思。

| 需要一起看的东西 | 本节先读的问题 | 立刻接到哪里 |
| --- | --- | --- |
| 和价值型的差异 | 是先学记分板，还是直接改行动方式？ | P4-19.1 价值型强化学习 |
| policy gradient 与 actor-critic | policy 是怎么被改的，谁给评价信号？ | P4-19.4 后续算法地图 |
| 连续行动与大状态空间 | 为什么直接处理 policy 更自然？ | P4-19.3 现实应用与控制问题 |
| 失败成本边界 | 被提高概率的行动，在真实场景会带来什么副作用？ | safe RL、sim-to-real、offline review |

## 检查清单

- 能不能把策略型强化学习解释成：一边提高 expected reward，一边直接调整 policy 本身的做法？
- 和价值型强化学习相比，你是否理解策略型方法是在直接处理行动概率与行动方式？
- 能不能解释 policy gradient 调整的是行动倾向，而不是记分板？
- 能不能把 REINFORCE 解释成展示策略型强化学习基本哲学的入门算法？
- 能不能区分 actor-critic 里的 critic 不是代替 policy 选行动，而是提供评价信号？
- 能不能说明为什么在连续行动问题里，直接处理 policy 本身会更自然？

## 来源与参考资料

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., The MIT Press, 2018, 确认日期：2026-06-27. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Ronald J. Williams, `Simple statistical gradient-following algorithms for connectionist reinforcement learning`, Machine Learning, 1992, 确认日期：2026-06-27. [https://link.springer.com/article/10.1007/BF00992696](https://link.springer.com/article/10.1007/BF00992696){: target="_blank" rel="noopener noreferrer" }
- Richard S. Sutton, David McAllester, Satinder Singh, Yishay Mansour, `Policy Gradient Methods for Reinforcement Learning with Function Approximation`, NeurIPS 1999, 确认日期：2026-06-27. [https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Vijay R. Konda, John N. Tsitsiklis, `On Actor-Critic Algorithms`, SIAM Journal on Control and Optimization, 2003, 确认日期：2026-06-27. [https://doi.org/10.1137/S0363012901385691](https://doi.org/10.1137/S0363012901385691){: target="_blank" rel="noopener noreferrer" }
