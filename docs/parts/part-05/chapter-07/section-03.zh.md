# P5-7.3 自适应 update 的直觉：以 Adam 为例

Section ID: `P5-7.3`
Version: `v2026.07.17`

在 P5-7.2 里，我们已经看到：即使 gradient 相同，真实的 update 步幅也会因为 learning rate 而不同。走到这里，接下来会自然出现一个新问题：`是不是所有参数都应该永远用完全相同的方式去应用这个步幅？`

自适应 update（adaptive update）正是从这个问题里出现的。如果最基本的直接 update 只是`根据当前 gradient 与 learning rate 移动一次`，那么自适应 update 则会进一步把最近的 gradient 流向，以及不同参数坐标之间的差异也一起考虑进来。

这一节会以 Adam（Adaptive Moment Estimation）为代表例子来读这种直觉。这里真正要抓住的，不是 Adam 这个名字本身，而是：`为什么 update 规则里会开始加入最近流向和按坐标调节。`

如果之后又把基本 update 与自适应 update 的区别混在一起，更适合回到[英文概念词汇表里的 gradient descent 条目](/AiBook/en/reference/concept-glossary/#gradient-descent)和[optimizer 条目](/AiBook/en/reference/concept-glossary/#optimizer)，重新对齐比较基准。

## 本节范围

- 自适应 update 试图在基本 gradient update 上补什么？
- `最近 gradient 流向`和`按坐标调节`这两个核心直觉到底分别是什么意思？
- 为什么 Adam 经常被拿来当作自适应 update 的代表例子？
- 虽然 Adam 在实务里经常出现，但为什么不能把它背成绝对优劣结论？

这一节不会先堆更多 optimizer 名称，而是先解释：自适应 update 是从什么问题意识里长出来的。这里真正要读的是：`已经算出来的 gradient，到底要按什么规则变成真实 update`，以及为什么那个规则开始引入最近流向和按坐标差异。Adam 只是帮助我们抓住这种直觉的代表例子。至于 optimizer 家族名字的更细比较，会放到 P5-7.5；optimizer state 与 parameter-wise update 的进一步区分，则会在 P5-7.7 补充学习里接着说明；regularization 与 generalization 的视角会在 P5-8.1、P5-8.2 重新接回；而 adaptive optimization 的收敛分析则会放到 P5-7.4。

| 现在这一节要区分的 | 为什么重要 |
| --- | --- |
| 模型结构 | 因为这是在讨论 CNN、RNN、Transformer 之类如何表达输入的结构问题 |
| optimizer 过程 | 因为这是在讨论：同样的结构里，参数到底如何被移动 |
| 与 regularization 的区别 | optimizer 在处理`怎么移动`，regularization 更偏向`不希望哪种解` |

## 本节目标

- 能把自适应 update 解释成`会把最近 gradient 流向与坐标差异一起反映进去的 update 方式`。
- 能理解基本直接 update 与自适应 update 的差别。
- 能说明为什么 Adam 常被作为 adaptive update 的代表例子。
- 能通过可运行的 Python 例子确认不同 update 直觉造成的差异。

## 理解自适应 update 之前，先要有一个基准线

如果一上来就从复杂公式讲起，初学者往往会看不出：到底新增了什么。所以这里先放一个最简单的基准线。当前最先要抓住的，不是某个 optimizer 名字，而是下面这个最基础的直觉：

`沿着当前 gradient 指向的方向，用预先设定好的 learning rate 走一步。`

这条直觉，正好延续了 P5-7.2 里`learning rate 决定步幅`的说明。P5-7.2 解释的是步幅本身；这一节则把`所有参数都按一个共同标准步幅直接移动`看成基准线，然后再比较：自适应 update 又另外加入了什么。

之所以不先把某个名字摆上来，也很明确。当前最需要的不是记名字，而是先建立一个最薄的比较基准。只有先有这个基准线，读者之后才知道：自适应 update 到底在补什么。

- 这个基准线的直觉最简单
- 它能清楚露出 gradient descent 的核心思想
- 它让 update 规则的变化最容易被看见

也就是说，这一节的基准线不是某个特定品牌 optimizer，而是：`最简单的直接 update 感觉。`

## 自适应 update 试图补什么

自适应 update 会使用比单纯`当前 gradient + learning rate`更多的信息。以 Adam 为代表例子，大致可以先按下面这些点来理解。

- 它会参考最近 gradient 的方向流向
- 它会尝试按参数坐标分别调节移动量
- 它通常带着让初期学习更快、更稳的实用目的

也就是说，自适应 update 并不满足于`所有参数都按同一把尺子走`，而是想把那些单纯共用步幅很容易漏掉的信息也一起反映进去。

如果把它压成一句话，就是：

`Adam 会同时参考最近 gradient 的流向以及按坐标的大小差异，尝试让每个参数更自适应地移动。`

换成更直觉的说法，就是：

- 直接 update 的基准：`看当前 gradient，按共同步幅走一步`
- Adam 的直觉：`把最近几步的流向也留下来，并按坐标分别调节步幅`

例如，假设某个参数的 gradient 一直很大又摇摆，另一个参数的 gradient 则一直很小但比较稳定。最简单的直接 update 会把它们都按同一 learning rate 往前推；而 Adam 这种自适应方式则会开始问：`这个坐标最近是不是摇摆太大？`、`另一个坐标是不是一直动得太慢？` 正因为这样，自适应 update 给人的感觉就不再是`所有坐标一视同仁地走同一步`，而更接近于`每个坐标按自己的状况走不同的一步。`

## 如果以 Adam 为例，会看见什么

入门阶段，比起一开始就看复杂公式，下面这张表更重要。

| 项目 | 直接 update 基准 | Adam |
| --- | --- | --- |
| 基本感觉 | 直接走一步 | 反映更多累积信息的自适应 update |
| 优点 | 直觉简单，基准清楚 | 初期学习常显得更快，实务中也比较方便 |
| 注意点 | 可能对 learning rate 很敏感 | 即使看起来方便，也不能直接断言最终 generalization 一定更好 |

这张表最重要的，并不是`哪一个绝对更强`。更安全的读法是下面这句话。

`Adam 是在最基本的 gradient update 之上，再加入最近流向与按坐标调节，因而形成更自适应 update 的代表例子。`

## 为什么 Adam 常被拿来当代表例子

在实务里，Adam 被频繁提到。这里读者需要长期留下来的，不是`很多人都在用`，而是：`为什么它常被选来代表自适应 update。`

- 它常常在默认设置下也能工作得不错
- 它很容易给人一种`学习初期下降得比较快`的体验
- 在大模型或复杂数据上，它会让入门门槛显得低一些

但这里也必须一起保留一个警告。

`Adam 虽然常用，但这并不等于它在所有问题里都自动保证更好的最终结果。`

也就是说，Adam 的流行，很大一部分来自实用性与方便性；但是否更适合某个任务，仍然是另外一个判断。

如果把前面的意思再压缩一次，自适应 update 就是：`在直接 update 之上，再加入最近流向与按坐标调节。` 而 Adam 是帮助我们读懂这种直觉的一个代表例子。

如果只把这层 update 规则再画得更紧一点，就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-07/sgd-vs-adam-flow-zh.mmd"
```

这张图最先要确认的结果，是：如果最基本的直接 update 更接近`对当前 gradient 与共同步幅立刻反应`，那么 Adam 的直觉则更接近`把最近流向与按坐标差异都考虑进去，再调节步幅。`

## 练习与例子

下面两个例子都不是在完整实现真实 Adam，而是在把自适应 update 的核心直觉拆开来看。第一个例子主要看`时间轴上的最近流向累积`，第二个例子主要看`坐标轴上的分别调节`。只要按这两个轴来读，Adam 就更像一个代表例子，而不是要硬背整套公式的名字。

输入：

- 当前风险权重 `risk_weight`
- 多个 step 中依次出现的风险权重 gradient 列表

输出：

- 直接 update 方式下连续发生的风险权重变化
- 用简化 moving average 直觉表达的 Adam-like 更新结果
- 每个 step 的 `direct_delta` 与 `adam_like_delta`
- 在第二个小实验里，当两个参数坐标的 gradient 尺度不同，按坐标调节会怎样出现

问题场景：

- 观察自适应 update 时，比起背名字，更适合看：同样的 gradient 流，最后是怎样被变成不同 step update 的

需要确认的概念：

- 最直接的 update 会对当前 gradient 立即反应
- Adam 类直觉会把最近 gradient 信息累积起来，再调节移动量
- Adam 类直觉还会把不同坐标上的 gradient 尺度差异也一起考虑进去

输入（input）：

假设存在一个读取压力未恢复信号的 `risk_weight`，它在学习中依次收到 `gradient_risk_weight = -4.0`, `-2.0`, `-1.0`。即使看到的是同一串 gradient 流，直接 update 与 Adam-like 也会在`反应得多直接`和`会不会把最近平均留下来`这两点上出现差别。

在看代码之前，最好先猜一猜：哪一边的移动量会更直接，哪一边的移动会更平滑。这样更容易抓住`当前 gradient 反应`与`累积平均反应`的差别。

| 比较项 | 先猜一下会看到什么 update | 猜测理由 |
| --- | --- | --- |
| 第一个 `direct_delta` | 很可能是最大的一次移动 | 因为第一步的 `-4.0` 会直接乘上 learning rate 反映出去 |
| 第一个 `adam_like_delta` | 很可能明显小于 `direct_delta` | 因为 moving average 在开头只会部分吸收这个 gradient |
| 随着 step 推进，`direct_delta` | 会跟着 gradient 绝对值一起立刻变小 | 因为它对当前 `gradient_risk_weight` 直接反应 |
| 随着 step 推进，`adam_like_delta` | 变化得会更慢、看起来更平滑 | 因为前几步的 gradient 还会留在 moving average 里 |

这张表的目的，并不是提前背数字，而是先抓住：即使看到的是同一条 `gradient_risk_weight` 流，最直接的 update 更像`立刻反应`，而 Adam-like 更像`把最近流向留下来再移动。`

```python
gradient_risk_weight_history = [-4.0, -2.0, -1.0]
risk_weight_direct = 1.0
risk_weight_adam_like = 1.0
learning_rate = 0.1
moving_avg = 0.0
beta = 0.9

print("Direct updates")
for gradient_risk_weight in gradient_risk_weight_history:
    direct_delta = -learning_rate * gradient_risk_weight
    risk_weight_direct = risk_weight_direct + direct_delta
    print(
        " gradient_risk_weight =", gradient_risk_weight,
        "direct_delta =", round(direct_delta, 3),
        "-> risk_weight =", round(risk_weight_direct, 3)
    )

print()
print("Adam-like updates (simplified intuition)")
for gradient_risk_weight in gradient_risk_weight_history:
    moving_avg = beta * moving_avg + (1 - beta) * gradient_risk_weight
    adam_like_delta = -learning_rate * moving_avg
    risk_weight_adam_like = risk_weight_adam_like + adam_like_delta
    print(
        " gradient_risk_weight =", gradient_risk_weight,
        "moving_avg =", round(moving_avg, 3),
        "adam_like_delta =", round(adam_like_delta, 3),
        "-> risk_weight =", round(risk_weight_adam_like, 3)
    )
```

输出里先要比较的是：面对完全相同的 `gradient_risk_weight` 流，直接 update 与 Adam-like 的每一步 update 是怎样分开的。

```text
Direct updates
 gradient_risk_weight = -4.0 direct_delta = 0.4 -> risk_weight = 1.4
 gradient_risk_weight = -2.0 direct_delta = 0.2 -> risk_weight = 1.6
 gradient_risk_weight = -1.0 direct_delta = 0.1 -> risk_weight = 1.7

Adam-like updates (simplified intuition)
 gradient_risk_weight = -4.0 moving_avg = -0.4 adam_like_delta = 0.04 -> risk_weight = 1.04
 gradient_risk_weight = -2.0 moving_avg = -0.56 adam_like_delta = 0.056 -> risk_weight = 1.096
 gradient_risk_weight = -1.0 moving_avg = -0.604 adam_like_delta = 0.06 -> risk_weight = 1.156
```

如果再把这些输出拆成`输入 gradient -> 每步 update -> 累积后的 risk_weight`三层来读，自适应 update 试图补什么会更清楚。

![逐 step 的 gradient 输入流](/AiBook/assets/part-05/chapter-07/sgd-adam-gradient-history-zh.png)

第一张图只是输入，还不是 optimizer 改过之后的东西。这里能看到：随着 step 变化，`gradient_risk_weight` 的绝对值越来越小。也就是说，直接 update 与 Adam-like 的差别，并不是因为输入不同，而是因为它们对同样输入采用了不同更新规则。

![直接 update 与 Adam-like 的逐 step delta 对比](/AiBook/assets/part-05/chapter-07/sgd-adam-delta-comparison-zh.png)

第二张图开始出现差异。直接 update 会立刻把当前 gradient 与 learning rate 相乘，因此第一步就走得比较大；Adam-like 则会先通过 moving average，因此即使面对同样输入，也会做出更小、更平滑的移动量。

![直接 update 与 Adam-like 的 risk_weight 移动轨迹](/AiBook/assets/part-05/chapter-07/sgd-adam-risk-weight-trajectory-zh.png)

第三张图显示，这种差异最终会积累成不同参数路径。直接 update 会比较快地走到 `1.7`，而 Adam-like 则会更缓慢地到达 `1.156`。这里最重要的，并不是判断哪一边绝对更好，而是确认：optimizer 规则会把同一条 gradient history 变成不同的 parameter path。

这个例子并不是完整重现 Adam 公式，也不是在下结论说哪种方法更强。这里真正要留下来的，是下面三点。

- 直接 update 对当前 `gradient_risk_weight` 的反应更直接
- Adam 类直觉会保留最近方向，因此 step 之间的移动更平滑
- optimizer 不是简单地让损失减少，而是在决定：同样的 gradient 会被改写成怎样的 update 路径

### 按坐标调节的小实验

下面这个小实验把注意力从`同一个参数在多个 step 上怎么动`，切到`不同参数坐标为什么会收到不同 update。`

```python
learning_rate = 0.1
beta2 = 0.9
second_moment = {
    "risk_weight": 0.0,
    "recovery_weight": 0.0,
}
gradient_by_parameter = {
    "risk_weight": [-8.0, -4.0],
    "recovery_weight": [-0.5, -0.25],
}

for step in range(2):
    print("step", step + 1)
    for parameter_name, gradient_history in gradient_by_parameter.items():
        gradient = gradient_history[step]
        direct_delta = -learning_rate * gradient

        second_moment[parameter_name] = (
            beta2 * second_moment[parameter_name]
            + (1 - beta2) * gradient * gradient
        )
        adam_like_delta = -learning_rate * gradient / (second_moment[parameter_name] ** 0.5)

        print(
            parameter_name,
            "gradient =", gradient,
            "direct_delta =", round(direct_delta, 3),
            "second_moment =", round(second_moment[parameter_name], 3),
            "adam_like_delta =", round(adam_like_delta, 3),
        )
```

这段输出不需要重新背成完整 Adam 公式。更适合先看的是：`同样沿坐标分开来看时，update 是怎样被重新缩放的。`

```text
step 1
risk_weight gradient = -8.0 direct_delta = 0.8 second_moment = 6.4 adam_like_delta = 0.316
recovery_weight gradient = -0.5 direct_delta = 0.05 second_moment = 0.025 adam_like_delta = 0.316
step 2
risk_weight gradient = -4.0 direct_delta = 0.4 second_moment = 7.36 adam_like_delta = 0.147
recovery_weight gradient = -0.25 direct_delta = 0.025 second_moment = 0.029 adam_like_delta = 0.147
```

在最直接的 update 里，`risk_weight` 的第一步 update 是 `0.8`，`recovery_weight` 则只有 `0.05`。也就是说，gradient 尺度差异几乎会被原样带进 update。而在 Adam-like 的按坐标调节里，每个坐标会先把自己的 gradient 历史写进 `second_moment`，再按这个尺度去重新缩放 update。结果就是：很大的 gradient 坐标会被压一压，而很小的 gradient 坐标也不会永远被彻底淹没。

这里不需要把这些数字全背下来。真正要抓住的学习点只有一个：Adam 里的`adaptive`不仅表示会记住最近流向，也表示：不同参数坐标会按各自的 gradient 尺度历史，被分别调节步幅。

当然，也不能把这个小实验误读成`Adam 总会把不同参数的 update 调成一样大。` 这里两条 `adam_like_delta` 恰好相同，是因为我们故意用了比例相似的简单示例。真实 Adam 还会同时涉及第一动量、第二动量、bias correction 以及稳定项等因素。这个实验的目的不是完整还原公式，而只是先把`较大的 gradient 会除以较大的历史尺度，较小的 gradient 也会除以较小的历史尺度`这种按坐标调节的感觉拆出来。

把这两个例子合在一起读，自适应 update 的补强就会分成两个轴。

| 例子 | 看的轴 | 直接确认到的变化 | 本节要留下来的句子 |
| --- | --- | --- | --- |
| 单个 `risk_weight` 在多个 step 上变化 | 时间轴 | 最近 gradient 会留在 moving average 里，使 step 间移动更平滑 | 自适应 update 不只看当前 gradient，也会看最近流向 |
| `risk_weight` 与 `recovery_weight` 并排比较 | 坐标轴 | 每个参数会按自己的 gradient 历史分别调节步幅 | 自适应 update 不会把所有参数永远按同一标准步幅去推 |

把这张表读完以后，至少应该能够把自适应 update 说成：`把时间轴累积与坐标轴调节都写进 update 规则里的方式。` Adam 则是帮助我们看懂这件事的代表例子，仅此而已。

## 什么时候要先用自适应 update 视角

在已经理解 optimizer 一般角色之后，还要继续判断：`现在最简单的直接 update 感觉够不够？还是需要把自适应 update 这层直觉也调出来？`

| 先出现的问题场景 | 先想到的 optimizer 视角 | 理由 |
| --- | --- | --- |
| 需要说明 gradient 与步幅最基本的关系 | 先用直接 update 作为基准 | 因为它最清楚地展示了对当前 gradient 立即反应的感觉 |
| 初期学习很粗糙，或不同坐标尺度差异很大 | 先想到自适应 update | 因为此时最近流向与按坐标调节的直觉更重要 |
| 需要说明为什么实务里常提 Adam | 先想到自适应 update，把 Adam 作为代表例子来看 | 因为它的方便与实用性强，但不能把代表例子直接等同于一般原理 |
| 开始有人想把 optimizer 背成绝对优劣表 | 把直接基准与自适应 update 并排放回来看 | 因为速度、稳定性、generalization 不应该被揉成一句话 |

## 检查清单

- 能说明自适应 update 是在基本 update 上又补了什么吗？
- 能把自适应 update 解释成`会更多反映累积信息与按坐标差异的方式`吗？
- 能把直接 update 与自适应 update 区分成`立刻对当前 gradient 反应`和`同时参考累积信息与坐标差异`两种感觉吗？
- 能区分：第一个例子主要在看时间轴累积，第二个例子主要在看坐标轴调节吗？
- 能说明 Adam 只是自适应 update 的代表例子，而不是自动等于绝对更好的 optimizer 吗？

## 出处与参考资料

- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 确认日期: 2026-06-29.
- Diederik P. Kingma, Jimmy Ba, `Adam: A Method for Stochastic Optimization`, arXiv, 2014, 确认日期: 2026-06-29.
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 确认日期: 2026-06-29.
