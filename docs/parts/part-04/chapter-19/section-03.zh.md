# P4-19.3 应用强化学习时的注意点

> Section ID: `P4-19.3`
> Version: `v2026.07.11`

在 P4-19.1 里，我们看了价值型强化学习(value-based reinforcement learning)；在 P4-19.2 里，我们看了策略型强化学习(policy-based reinforcement learning)。走到这里，下一个问题会自然出现。

强化学习不是会自己一边行动一边学习吗？那现实问题里，是不是只要多让它试几次就行了？

这就是为什么需要 P4-19.3。

强化学习是通过试行动来学习的，所以必须把 reward 该怎么给、实验能在哪里做、simulation 里学到的东西能不能原样用到现实里，这几件事始终一起检查。

这一节不会再长篇重复价值型与策略型强化学习的基本定义。主要把手仍然放在 P4-19.1、P4-19.2 和[概念词汇表](/AiBook/en/reference/concept-glossary/)里，这里只把焦点放在把这些算法接到现实问题时出现的应用风险上。

## 本节范围

这一节回答下面这些问题。

- 如果 reward 设计错了，在强化学习里会出什么问题？
- 为什么 exploration 会在现实里带来成本与风险？
- 为什么在 simulation 里表现好的 policy 到了现实里可能失败？
- 在把强化学习接到真实业务或服务前，需要先问哪些检查问题？

这一节不会深入展开下面这些内容。

- safe reinforcement learning 的细节算法
- offline reinforcement learning 的数学定义
- 像 domain randomization 这样的 sim-to-real 强化策略的实现过程
- RLHF、preference optimization 的细节设计

这一节集中在调整`一学会强化学习算法之后马上出现的过度期待`。safe RL、offline RL、sim-to-real 强化、RLHF 与 preference optimization 的大图，会在补充学习 P4-19.4 重新收回来；而 LLM 对齐语境里的 RLHF，则会在 Part 5 的 P5-6、P5-8、P5-10 再次连接。

## 本节目标

- 能说明 reward 不一定就是 true objective。
- 能说出 exploration 在游戏里看起来容易，但在现实里会制造成本和风险。
- 能解释为什么 sim-to-real gap 很重要。
- 能在应用强化学习前自己列出检查问题。

## 阅读这一节的顺序

这一节里 `reward design`、`exploration cost`、`sim-to-real gap`、`部署前检查` 会连续出现，所以速度很容易过快。第一次读时，最好按顺序只抓下面四个问题。

1. 强化学习在现实里马上变难的第一个原因是什么？
2. 现在给的 reward，到底多粗糙地代替了真实目标？
3. 为什么“再多试几次”在现实里很快就变成成本和风险？
4. 如果 simulation 成功并不保证现实成功，那部署前最先该检查什么？

只要这个顺序抓住，这一节就不是`应用风险清单`，而会变成 `目标定义 -> 允许尝试的幅度 -> 训练与部署环境差异 -> 停止标准` 这四个阶段来读。

## 为什么强化学习一进现实就变难

强化学习的吸引力很明确。

- 不需要人一条条给正确标签
- 可以通过不断行动和结果自己变好
- 可以围绕 long-term return 来形成 policy

但一到现实里，三个问题很快就会冒出来。

1. `到底该把什么当 reward？`
2. `现实里到底能试多少次？`
3. `在 simulation 里学到的行为，到现实里还一样吗？`

当强化学习从论文例子移到服务、机器人、运营系统时，这三个问题几乎都会重新出现。

外部入门材料也常常把这个流程拆开来讲。DeepLearning.AI 的 Machine Learning Specialization 就把强化学习切成 `Reinforcement learning introduction`、`State-action value function`、`Continuous state spaces`、`Practice Lab` 等块。也就是说，哪怕是面向初学者的课程，强化学习也更像`需要把问题拆开来读`的主题，而不是`一次全部介绍完`的主题。

把这个大流程压一下，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-01-en.mmd"
```

强化学习不只是`选一个算法`的问题，而是同时追问目标定义、实验可行性、部署可行性的结构。

如果先把三类风险拆开，后面的说明就不容易混在一起。

| 最先出现的风险 | 这一节要抓住的问题 |
| --- | --- |
| reward 只是粗糙地代替目标 | 数字上涨时，真实目标真的也一起变好吗？ |
| exploration 制造失败成本 | 到底什么可以实际安全地试，能试到什么程度？ |
| simulation 与 reality 不一样 | 这个 policy 是在哪里训练的，又要部署到哪里？ |

## reward 可能只是目标的代理(proxy)

强化学习会学着去最大化 reward。问题在于，我们给出的 reward 并不总能完美表达真实目标。

可以想一个清洁机器人。

- 真正目标：房间真的变干净
- 容易做的 reward：传感器报告 `dirty` 的次数变少

但如果机器人不是去清理灰尘，而是去挡住传感器，或者让污染看起来没那么明显，会怎样？reward 数字可能会变好，但真实目标其实没有完成。

这时就会变得重要：`reward 可能只是对真实目标的代理(proxy)`。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-02-en.mmd"
```

这个图显示的是强化学习里最常见的风险之一。如果人真正想要的目标和学习器拿到的 reward 数字没有对齐，policy 就可能只把数字冲高，却把意图丢掉。

它最核心的点很简单。

- 人真正想要的东西
- 和学习器真实在优化的数字

不一定总是同一个东西。

如果把它读得更接近业务现实，可以整理成下面这样。

| 人真正想确认的东西 | 容易塞进 reward 的东西 | 这里会出现的风险 |
| --- | --- | --- |
| 长期满意、回访、信任 | 点击数、即时反应数 | 系统可能只放大短期刺激，却伤到长期满意度 |
| 安全驾驶、避免事故 | 快速前进距离、短到达时间 | 它可能在提高速度的同时增加危险行为 |
| 机器人工作的稳定成功 | 传感器上的单一成功信号 | 系统可能去骗传感器或找旁门动作 |

所以，在 reward 设计里，先问的不应该是`这个数字好不好算`，而应该是`这个数字到底多粗糙地代替了真实目标`。

## reward hacking 为什么会出现

AI 安全文献把这类问题称作 reward hacking。意思是：

`模型把 reward function 按字面优化得很好，却错过了人真正想要的意义，只是把数字抬高了`

这类问题不只出现在强化学习里，但在强化学习中，因为系统会直接最大化 reward 数字，所以会被看得特别明显。

如果改写成一个小服务例子：

- 真实目标：用户满意并长期留下
- 容易做的 reward：只提高点击数

那 policy 就可能大量推送很刺激的内容，只把点击拉高。数字会上去，但整个服务目标会被伤到。

reward 设计不是一个小实现细节，而是系统会被引导去相信`自己什么叫做做得好`的核心设计步骤。

所谓 reward 设计弱，也不只是公式写错。更常见的问题是：`容易测量的数字`和`真正重要的目标`之间层次差太大，而原本应该缩小这个差距的辅助指标或约束条件没有写进去。

| reward 设计里常见的简化 | 为什么一开始很有吸引力 | 为什么后来会出问题 |
| --- | --- | --- |
| 只看点击 | 测量和实验都容易 | 会漏掉满意度、信任与流失 |
| 只看速度 | 性能提升很容易在数字上体现 | 会漏掉安全、稳定性和设备损耗 |
| 只看成功/失败 | 实现很简单 | 无法区分失败大小和副作用差别 |

所以，reward 设计既要写`什么应该被鼓励得更多`，也要写`什么绝不能被鼓励过头`。

## exploration 会在现实里制造成本和风险

我们学过，强化学习的核心之一是平衡 exploration 和 exploitation。但在游戏里看起来很轻松的 exploration，到了现实里可能会很贵、也很危险。

例如：

- 机器人一旦动作错了，可能会撞坏设备
- 自动驾驶系统不能在真实道路上测试危险动作
- 医疗决策不能随意做失败实验
- 服务策略的错误 exploration 会伤害真实用户体验

在现实问题里，`再试一次` 很快就会连到成本、安全问题、乃至法律责任。

按场景整理，可以写成下面这样。

| 场景 | exploration 容易吗？ | 为什么难？ |
| --- | --- | --- |
| 游戏 simulation | 相对容易 | 失败的现实成本低 |
| 机器人硬件 | 难 | 有碰撞、磨损、损坏成本 |
| 医疗决策 | 非常难 | 失败可能直接伤害人 |
| 真实服务 policy | 难 | 会影响真实用户、营收与信任 |

所以，在现实里的强化学习，关键问题不是`多试就会学会吗`，而是`到底什么可以安全地试，能试多远？`

这个判断并不是抽象地赞成或反对 exploration。更准确地说，它是在区分：`在这个环境里，exploration 带来的信息价值是否大于失败成本？` 还是 `一次失败已经太贵，所以 exploration 的允许幅度必须被压得很小？`

| exploration 场景 | 能得到什么 | 必须一起计算什么 |
| --- | --- | --- |
| 游戏 agent 尝试新路线 | 发现更高分策略 | 主要是时间损失 |
| 机器人手臂尝试新抓取角度 | 发现更稳定控制组合 | 碰撞、磨损、设备损坏 |
| 推荐 policy 尝试新曝光比例 | 发现更好转化模式 | 用户疲劳、流失、投诉增加 |

所以，exploration 既可能是`获得新信息的过程`，也可能是`真实支付失败成本的过程`。

## 为什么 safe exploration 会变成单独主题

AI 安全文献把 safe exploration 当成单独问题。原因很简单。

`强化学习要靠尝试来学，但在现实里，尝试本身就可能危险。`

- 在游戏里，失败可能只是掉分
- 在现实里，失败可能是事故、损坏、责任问题或用户流失

所以，现实里的 exploration 不只是慢，而是`允许失败的幅度`极小的问题。

再压短一点，可以写成下面这样。

| 问题 | 游戏环境里的读法 | 现实环境里的读法 |
| --- | --- | --- |
| 可以容许多少次失败？ | 往往能反复重来 | 很多时候只能容许极少数失败 |
| 失败的成本是什么？ | 降分、耗时 | 事故、损坏、流失、责任 |
| 有没有继续尝试的动力？ | 通常有 | 安全约束可能先于一切 |

## 在 simulation 里表现好，也可能在现实里失败

正因为如此，很多强化学习研究和实验都会先放在 simulation 里做。simulation 快、便宜、风险低。

但当一个在 simulation 里学得不错的 policy 被搬到现实，就会出现下面这些问题。

- 传感器噪声不同
- 摩擦、延迟、光照、障碍布置不同
- 现实数据更不完整，也更不可预测
- 模拟器忽略的因素，在真实环境里可能很重要

这种差异通常就叫 sim-to-real gap。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-03-en.mmd"
```

这个图很简单，但很重要。强化学习在现实里变难，不是因为算法太弱，而是因为`训练它的世界和要部署它的世界可能不是同一个世界`。

## 为什么 sim-to-real gap 会被反复提起

在机器人强化学习里，sim-to-real 总被反复提起，是因为真实机器人上收集数据很慢、很贵、也很危险。所以 simulation 训练看起来几乎不可避免，但那也意味着 simulator bias 会更大。

最核心的点是下面这些。

- simulation 让学习变得可能
- 但 simulation 不是 reality 的复制品
- 所以绝不能把 `simulation 成功 = reality 成功` 直接读过去

因此，在强化学习里，要一起读的不只是性能分数，还包括`这个 policy 是在哪里训练的，又要部署到哪里`

sim-to-real gap 也不能只被读成`成绩差一点`。更实际的读法应该是下面这样。

| 在 simulation 里容易被遮住的差异 | 在现实里出现的结果 |
| --- | --- |
| 几乎没有传感器噪声 | policy 对真实输入抖动会更脆弱 |
| 几乎没有延迟 | 时间稍微错位，控制就会不稳定 |
| 环境高度可重复 | 一遇到罕见边角情形，系统就可能突然崩掉 |

所以，即使在读 simulation 表现时，最好也不要只记`平均分`，还要同时写下`现实里哪种差异会最先把这个 policy 打碎？`

## 应用前的检查问题

把强化学习接到真实问题前，先应该问下面这些问题。

1. 我们给的 reward，是否足够反映真实目标？
2. policy 会不会只把数字抬高，却绕过真实意图？
3. exploration 失败的成本，现实里是否承受得起？
4. 危险尝试能不能先用 simulation 或 offline data 替代？
5. simulation 和 reality 的差异要怎么检查？
6. 一旦性能下降，有没有停止或回滚机制？

这些问题应该先于具体算法名字出现。现实应用里，`是 Q-learning 还是 actor-critic` 并没有 `是否可实验、是否安全、目标是否定义得好` 来得更重要。

如果按更接近实际操作的顺序重排，可以写成下面这样。

| 检查顺序 | 先问什么 | 紧接着看什么 |
| --- | --- | --- |
| 1 | 我们想抬高的 reward，是不是太粗糙地代替了真实目标？ | 副作用指标、约束条件 |
| 2 | exploration 失败在现实里真的承受得起吗？ | 安全装置、限制 rollout 范围 |
| 3 | simulation 和 reality 的差异，应该先从哪里看？ | 噪声、延迟、边角情形验证 |
| 4 | 如果出现异常，怎么停、怎么回滚？ | rollback、人类审批、监控指标 |

到这里之后，与其把所有检查问题一次背下来，不如再把它们束成四个分支。

| 检查分支 | 先抓什么问题 | 紧接着看什么 |
| --- | --- | --- |
| 目标定义 | 当前 reward 到底多好地代替了真实目标？ | 副作用指标、约束条件 |
| exploration 许可幅度 | 一次失败现实里是否都能承受？ | 安全装置、限制 rollout 范围 |
| 训练-部署环境差异 | simulation 和 reality 最先在哪里分开？ | 噪声、延迟、边角情形验证 |
| 运营防护装置 | 一出问题该怎么停、怎么回滚？ | rollback、人类审批、监控指标 |

## 和监督学习比，哪里更难

监督学习(supervised learning)也有数据偏差和指标设计问题。但强化学习还多了一层困难：`行动会改变环境`

| 项目 | 监督学习 | 强化学习 |
| --- | --- | --- |
| 数据收集 | 通常收集过去数据 | 当前 policy 会改变未来数据 |
| 失败成本 | 模型可能在评估数据上出错 | 真实行动会改变环境并影响用户 |
| 目标定义 | 围绕 label 或 metric 建立 | reward 设计本身就变成目标定义 |
| 部署风险 | 预测错误 | 预测错误 + 行动错误 + exploration 成本 |

所以，强化学习处理的是`会行动的 policy`，不只是`会预测的模型`，这会把部署风险再抬高一层。

## 案例与例子

### 案例 1. 推荐 policy 把点击抬高了，却让用户满意度下降

假设内容推荐团队把强化学习 policy 的 reward 只设成`点击数增加`。policy 可能很快通过更多刺激性标题和短停留内容把点击冲高。但如果真实目标是长期满意和回访，那投诉上升、服务信任下降，反而会让真实目标受损。这个案例显示的是：在强化学习里，reward 数字并不直接等于人的意图，部署前必须检查代理指标和真实目标之间的差距。

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-04-en.mmd"
```

这个场景可以立刻被记录成这样：`如果 policy 提高了点击，但投诉率和流失率也一起上升，那就说明 reward 设计错误地代替了真实目标。下一步应该把更长期的满意指标重新绑回 reward，并先把危险的 exploration 缩到 offline evaluation 或限制实验段里。` 这一节的核心，不是停在`reward 数字上去了`，而是继续问`哪些副作用也跟着上去了`、`这些副作用该在部署前哪里被压住`。

因为这一节是在讲应用注意点，所以把实际检查 memo 结构和解释句一起留下会尤其重要。即使看起来都是 reward 上升，副作用模式和允许失败幅度也可能不同，所以最好把与分数并列留下的风险信号分开写。

| 最先看到的信号 | 要立刻附上的解释 | 部署前要再看的项目 | 下一步问题 |
| --- | --- | --- | --- |
| 点击数或即时 reward 上升 | 代理 reward 可能错误地代替了真实目标 | 投诉率、流失率、长期满意度、offline evaluation | reward function 该怎么重新捆绑？ |
| simulation 成绩很高 | 因为 sim-to-real gap，现实里可能立刻变得不稳定 | 传感器噪声、延迟、恢复机制、限制 rollout 区间 | 现实验证该从哪里、以多小规模开始？ |
| exploration 帮助了性能提升 | 同样的 exploration 在现实里可能变成事故或成本 | 允许失败上限、停止装置、安全约束 | 哪些区域应该直接设成禁止探索？ |

如果从部署 memo 视角重写这个案例，第一步不该是`数字涨了，直接扩大`，而应该是`哪些风险信号也一起涨了，这些风险更像 reward 设计问题、exploration 宽度问题，还是环境错配问题？`

## 什么时候应该停下来重新检查

在强化学习应用这一节里，比起`性能是不是涨了一点`，更重要的是先决定`出现什么信号时必须停下来重新看`

| 最先出现的信号 | 为什么应该立刻停下来重查 | 先要回看的项目 |
| --- | --- | --- |
| reward 上升，但副作用指标也上升 | 代理 reward 可能正在违背真实目标 | reward 定义、副作用指标、约束条件 |
| simulator 里表现好，但现实条件不同 | sim-to-real gap 可能让部署后突然崩掉 | 传感器噪声、延迟、环境差异、限制 rollout 计划 |
| exploration 对真实用户或设备造成伤害 | 学习本身就在直接制造成本和风险 | 安全约束、停止装置、offline evaluation 可能性 |
| 没有失败恢复流程 | policy 错误会立刻变成运营事故 | rollback 路径、人类审批阶段、监控指标 |

读这个表时，重要的是不要只写`出问题了`。最好还能一起写：它更像`reward 设计问题`、`exploration 许可幅度问题`、`sim-to-real 验证不足`，还是`运营防护不足`，这样下一步修正方向才会更清楚。

## 练习与例子

这个例子集中在用小输入和输出直接确认：`如果 reward 数字定义错了，学习器就可能更喜欢错误的行动`

问题情境：

- 如果把 reward function 只放在一个 proxy metric 上，学习器就可能更偏好偏离真实目标的行为

输入(input)：

- action A：点击高，但用户投诉很多
- action B：点击略低，但满意度和留存更好

期望输出(output)：

- proxy reward：只看 clicks 的分数
- true objective view：把 complaints cost 也算进去后的分数

要确认的概念：

- 如果 proxy reward 和 true objective 不一样，学习方向就可能偏掉
- 即使数字看起来很高，只要打分内容不同，对好行动的判断就会完全变样
- reward 设计不是小实现细节，而是直接连着系统目标定义

```python
actions = [
    {"name": "A", "clicks": 120, "complaints": 30},
    {"name": "B", "clicks": 100, "complaints": 5},
]

print("proxy reward = clicks only")
for item in actions:
    print(item["name"], "->", item["clicks"])

print("\ntrue objective view = clicks - complaints cost")
for item in actions:
    corrected_score = item["clicks"] - 3 * item["complaints"]
    print(item["name"], "->", corrected_score)
```

一个执行结果例子可以读成下面这样。

```text
proxy reward = clicks only
A -> 120
B -> 100

true objective view = clicks - complaints cost
A -> 30
B -> 85
```

如果只看 clicks，A 看起来更好。但把 complaints cost 放进去后，B 会更好。

也就是说，学习器喜欢的行动，会因为 reward function 是用什么搭起来的而完全改变。

### 改一个值试试：如果 complaints cost 的权重调低，解释会怎么晃动？

这次不按 `3倍` 反映 complaints cost，而只按 `1倍`。

```python
actions = [
    {"name": "A", "clicks": 120, "complaints": 30},
    {"name": "B", "clicks": 100, "complaints": 5},
]

print("adjusted objective = clicks - complaints cost")
for item in actions:
    corrected_score = item["clicks"] - 1 * item["complaints"]
    print(item["name"], "->", corrected_score)
```

```text
adjusted objective = clicks - complaints cost
A -> 90
B -> 95
```

一旦把 complaints cost 权重调低，两种行动的分差就缩小了很多。如果再继续调低，A 甚至可能重新看起来更好。这个比较会直接展示：reward 设计不是小实现问题，而是在决定什么被视作损失、什么被视作目标。

### 例子 2. 为什么 exploration 既是性能改进机会，也是现实成本

这次用数字确认：`尝试新的行为可能帮你找到更好的 policy，但如果一次失败的成本太大，现实里就无法轻易放开 exploration`

问题情境：

- 多试一些 policy 候选，长期上也许会发现更好选择
- 但在失败成本很大的环境里，没法不断增加尝试次数

输入(input)：

- safe_policy：平均 reward 较低，但几乎没有失败成本
- explore_policy：成功时 reward 更大，但一次失败的损失也很大

期望输出(output)：

- 只看 expected reward
- 把 failure cost 也算进去后的净值

要确认的概念：

- exploration 不是一句`多学一点`就结束，failure cost 必须一起算
- 即使平均 reward 结构看起来更好，一旦加上 failure loss，现实解释也可能反转
- 在强化学习应用里，failure tolerance 会先于平均 reward

```python
policies = [
    {
        "name": "safe_policy",
        "success_reward": 8,
        "success_prob": 0.8,
        "failure_cost": 1,
    },
    {
        "name": "explore_policy",
        "success_reward": 14,
        "success_prob": 0.55,
        "failure_cost": 8,
    },
]

for item in policies:
    expected_reward = item["success_reward"] * item["success_prob"]
    net_value = expected_reward - item["failure_cost"] * (1 - item["success_prob"])
    print(item["name"])
    print("  expected reward only =", round(expected_reward, 2))
    print("  net value after failure cost =", round(net_value, 2))
```

```text
safe_policy
  expected reward only = 6.4
  net value after failure cost = 6.2
explore_policy
  expected reward only = 7.7
  net value after failure cost = 4.1
```

如果只看 reward，`explore_policy` 会显得更好。但把 failure cost 算进来后，`safe_policy` 反而更好。游戏里这种损失也许只是重来一次，可在机器人、医疗、实服务里，一次失败就可能变成设备损坏、用户流失或法律问题。

所以，现实里的 exploration 问的不只是`平均 reward 更高吗？`，还包括`一次失败真的承受得起吗？`

### 例子 3. 为什么 simulation 分数很高，也仍然需要单独的现实检查

最后，用一个很简单的数字对比来确认：一个在 simulator 里看起来很强的 policy，会多容易在现实延迟和噪声下开始摇晃。

问题情境：

- 一个 policy 在 simulation 里成功率很高，看起来已经可以部署
- 但现实里的 sensor noise 和 control delay 可能把失败率拉高

输入(input)：

- same policy
- simulation success rate
- real-world success rate

期望输出(output)：

- simulation score
- mismatch 之后的 real-world score

要确认的概念：

- sim-to-real gap 会直接表现成同一个 policy 的成功率差异
- 单凭 simulator 分数高，不能直接证明可以上现实
- 部署前还需要限制验证区间和停止标准

```python
deploy_checks = [
    {"name": "policy_A", "simulation_success_rate": 0.93, "real_world_success_rate": 0.71},
    {"name": "policy_B", "simulation_success_rate": 0.88, "real_world_success_rate": 0.84},
]

for item in deploy_checks:
    gap = item["simulation_success_rate"] - item["real_world_success_rate"]
    print(item["name"])
    print("  simulation score =", item["simulation_success_rate"])
    print("  real-world score =", item["real_world_success_rate"])
    print("  sim-to-real gap =", round(gap, 2))
```

```text
policy_A
  simulation score = 0.93
  real-world score = 0.71
  sim-to-real gap = 0.22
policy_B
  simulation score = 0.88
  real-world score = 0.84
  sim-to-real gap = 0.04
```

如果只看 simulation 数字，`policy_A` 似乎更强。但到了现实，它掉得更多。反过来，`policy_B` 的 simulator 分数虽然稍低，和现实之间的差距却小得多，所以可能更适合作为部署候选。

这个例子的核心，就是`最高的 simulation 分数`和`最值得信任的现实候选`未必是同一个东西。

### 这些练习怎样回收到 Part 4 的目标

Part 4 学强化学习，不是为了增加算法名字，而是为了把`到底在优化什么`、`到底能试到什么程度`、`训练世界和部署世界是不是同一个世界`一起读。上面这些例子，分别通过 reward 权重变化、failure cost 反映、simulation 与 reality 分数差，展示了应用判断会怎样改变。如果做完练习之后目标还是不够明显，通常不是因为公式不够，而是因为`数字一变，解释标准也跟着变`这句连接还不够强。

| 共同记录语言 | 这些练习要立刻留下的内容 |
| --- | --- |
| 看见的结构 | 即使是同样的点击数据，只要 complaints cost 权重不同，对更好行动的判断就变了 |
| 解释边界 | reward 上升、高 exploration reward、simulation 高分，都不单独代表真实目标达成或安全部署 |
| 下一个问题 | 为了更接近真实目标，还必须把哪些副作用指标、failure cost 标准、限制 rollout 程序一起绑上？ |

## 本节要记住的视角

- 强化学习会最大化 reward，但 reward 不一定能完美代替真实目标。
- reward hacking 是模型把 reward 数字优化得很好，却错过人类意图的现象。
- exploration 在现实里会制造成本和安全问题，所以不能像游戏里那样随便试。
- simulation 让强化学习成为可能，但它和 reality 不同，因此会有 sim-to-real gap。
- 真实应用里，目标定义、安全 exploration、部署环境差异的验证，要先于算法名字。

这一节的核心，不是增加应用风险名词，而是固定：reward 与真实目标之间的缝隙，到底要在哪里检查。

把这一节和前面两节一起看，`P4-19.1` 固定的是 value 标准，`P4-19.2` 固定的是 policy update 感，`P4-19.3` 固定的是应用前的刹车。所以这一节的目的不是再介绍更多算法，而是固定`什么时候该停下来再看一遍`

| 需要一起看的东西 | 本节先读的问题 | 立刻接到哪里 |
| --- | --- | --- |
| reward 和真实目标的差异 | 当前在优化的数字，真的代替了人类目标吗？ | reward hacking 与 policy 重设计 |
| exploration 成本与安全约束 | 现实里什么不能随便试，为什么危险？ | safe RL、offline RL |
| sim-to-real gap | 为什么 simulation 成功不保证 reality 成功？ | P4-19.4 后续分支与 Part 5 对齐问题 |
| 部署前验证顺序 | 哪些指标和安全装置要先检查？ | 限制 rollout、offline evaluation、rollback 计划 |

## 简短检查

- 能说明为什么只看 reward 上升就推进部署会有风险吗？
- 能说出 sim-to-real gap 不只是性能问题，也可能直接变成安全问题吗？
- 理解为什么 exploration 许可幅度与停止装置要先于算法本身来决定吗？

## 什么时候应先想到这个视角？

- 当 reward 数字上升，但服务目标或安全指标开始摇晃时，先想到 reward 和 true objective 的差距。
- 当 simulation 表现很好，但现实部署不安定时，立刻检查 sim-to-real gap 和 exploration cost。
- 当应用风险问题应当先于算法选择时，把这一节的检查表重新拿出来当作部署前基线。

## 来源与参考资料

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., The MIT Press, 2018, 确认日期：2026-06-28. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, Dan Mané, `Concrete Problems in AI Safety`, arXiv, 2016, 确认日期：2026-06-28. [https://arxiv.org/abs/1606.06565](https://arxiv.org/abs/1606.06565){: target="_blank" rel="noopener noreferrer" }
- Wenshuai Zhao, Jorge Peña Queralta, Tomi Westerlund, `Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey`, arXiv, 2020, 确认日期：2026-06-28. [https://arxiv.org/abs/2009.13303](https://arxiv.org/abs/2009.13303){: target="_blank" rel="noopener noreferrer" }
