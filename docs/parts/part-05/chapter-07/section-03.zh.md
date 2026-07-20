# P5-7.3 自适应 update 的直觉：以 Adam 为例

> Section ID: `P5-7.3`
> Version: `v2026.07.20`

在 P5-7.2 里，我们已经看到：即使 gradient 相同，真实的 update 步幅也会因为 learning rate 而不同。走到这里，接下来会自然出现一个新问题：`是不是所有参数都应该永远用完全相同的方式去应用这个步幅？`

自适应 update（adaptive update）正是从这个问题里出现的。如果最基本的直接 update 只是`根据当前 gradient 与 learning rate 移动一次`，那么自适应 update 则会进一步把最近的 gradient 流向，以及不同参数坐标之间的差异也一起考虑进来。

这一节会以 Adam（Adaptive Moment Estimation）为代表例子来读这种直觉。这里真正要抓住的，不是 Adam 这个名字本身，而是：`为什么 update 规则里会开始加入最近流向和按坐标调节。`

如果之后又把基本 update 与自适应 update 的区别混在一起，更适合回到[英文概念词汇表里的 gradient descent 条目](/AiBook/en/reference/concept-glossary/#gradient-descent)和[optimizer 条目](/AiBook/en/reference/concept-glossary/#optimizer)，重新对齐比较基准。

## Adam 自适应修正的问题

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

## gradient 历史与步幅调节的判断标准

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

下面直接进入例子。这一节的例子不是在完整实现真实 Adam，而是在把自适应 update 的核心直觉拆开来看。示例数据在 [optimizer-gradient-history.csv](/AiBook/assets/part-05/chapter-07/optimizer-gradient-history.csv)。这个文件记录了 12 个 step 里三个参数收到的 gradient 流：一个坐标收到较大的负 gradient 且逐渐变小，一个坐标收到较小的负 gradient 且逐渐变小，还有一个坐标的方向持续摇摆。

输入：

- 多个 step 里记录的按参数区分的 gradient 流
- 参数名 `parameter_name`
- 学习 step `step`
- 每个 step 的 `gradient`

输出：

- 简单直接 update 方式下的参数移动结果
- 简化 Adam-like 累积平均和 second moment 的 update 结果
- 各参数的平均 `direct_delta` 与 `adam_like_delta`
- 大 gradient、小 gradient、摇摆 gradient 下移动路径如何不同

问题场景：

- 自适应 update 的差异，比起看公式名称，更适合看按参数区分的 gradient 流如何被变成逐 step update

需要确认的概念：

- 最直接的 update 会对当前 gradient 立即反应
- Adam 类直觉会把最近 gradient 信息累积起来，再调节移动量
- Adam 类直觉还会把不同坐标上的 gradient 尺度差异也一起考虑进去

输入（input）：

CSV 里有下面三个坐标的 gradient 流。

| 参数 | gradient 流 | 先预想的事情 |
| --- | --- | --- |
| `risk_weight` | 较大的负 gradient 持续变小 | direct update 会移动得很远，Adam-like 会参考大小历史来调节步幅 |
| `recovery_weight` | 较小的负 gradient 持续变小 | direct update 几乎动不了，Adam-like 会按这个小坐标自己的历史来调节 |
| `noise_weight` | 负 gradient 与正 gradient 交替摇摆 | direct update 会持续改方向，Adam-like 会累积最近流向并减小摇摆 |

这张表的目的不是提前背准确数字。它只是让读者在看代码前先抓住：即使用同一个 learning rate，简单 direct update 会立刻反映`当前 gradient`，而 Adam-like 会留下`最近流向`和`按坐标的大小历史`，于是可能形成不同的移动路径。

```python
# 这个例子读取 CSV gradient history，比较 direct update 与 Adam-like update
# 如何制造不同的参数移动路径。
from csv import DictReader
from pathlib import Path

DATA_PATH = Path("docs/assets/part-05/chapter-07/optimizer-gradient-history.csv")
PARAMETER_ORDER = ["risk_weight", "recovery_weight", "noise_weight"]


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return [
            {
                "step": int(row["step"]),
                "parameter_name": row["parameter_name"],
                "signal_group": row["signal_group"],
                "gradient": float(row["gradient"]),
            }
            for row in DictReader(f)
        ]


def simulate_updates(rows):
    learning_rate = 0.05
    beta1 = 0.8
    beta2 = 0.9
    epsilon = 1e-8
    state = {
        parameter_name: {
            "direct_weight": 1.0,
            "adam_like_weight": 1.0,
            "m": 0.0,
            "v": 0.0,
        }
        for parameter_name in PARAMETER_ORDER
    }
    simulated = []

    parameter_index = {
        parameter_name: index
        for index, parameter_name in enumerate(PARAMETER_ORDER)
    }
    for row in sorted(
        rows,
        key=lambda item: (item["step"], parameter_index[item["parameter_name"]]),
    ):
        parameter_name = row["parameter_name"]
        gradient = row["gradient"]
        parameter_state = state[parameter_name]

        direct_delta = -learning_rate * gradient
        parameter_state["direct_weight"] += direct_delta

        parameter_state["m"] = beta1 * parameter_state["m"] + (1 - beta1) * gradient
        parameter_state["v"] = (
            beta2 * parameter_state["v"]
            + (1 - beta2) * gradient * gradient
        )
        adam_like_delta = (
            -learning_rate
            * parameter_state["m"]
            / (parameter_state["v"] ** 0.5 + epsilon)
        )
        parameter_state["adam_like_weight"] += adam_like_delta

        simulated.append(
            {
                "step": row["step"],
                "parameter_name": parameter_name,
                "gradient": gradient,
                "direct_delta": direct_delta,
                "adam_like_delta": adam_like_delta,
                "direct_weight": parameter_state["direct_weight"],
                "adam_like_weight": parameter_state["adam_like_weight"],
            }
        )

    return simulated


rows = load_rows(DATA_PATH)
simulated = simulate_updates(rows)

print("[input]")
print("rows =", len(rows))
print("parameters =", ", ".join(PARAMETER_ORDER))

print("\n[checkpoints]")
for item in simulated:
    if item["step"] in [1, 6, 12]:
        print(
            item["parameter_name"],
            "step =", item["step"],
            "gradient =", item["gradient"],
            "direct_delta =", round(item["direct_delta"], 3),
            "adam_like_delta =", round(item["adam_like_delta"], 3),
        )

print("\n[final weights]")
for parameter_name in PARAMETER_ORDER:
    last = [
        item for item in simulated
        if item["parameter_name"] == parameter_name
    ][-1]
    print(
        parameter_name,
        "direct_weight =", round(last["direct_weight"], 3),
        "adam_like_weight =", round(last["adam_like_weight"], 3),
    )
```

输出里先要比较的是：在同一个 CSV 输入下，简单 direct update 与 Adam-like 的每一步 update 是怎样分开的。

```text
[input]
rows = 36
parameters = risk_weight, recovery_weight, noise_weight

[checkpoints]
risk_weight step = 1 gradient = -7.0 direct_delta = 0.35 adam_like_delta = 0.032
recovery_weight step = 1 gradient = -0.6 direct_delta = 0.03 adam_like_delta = 0.032
noise_weight step = 1 gradient = -3.0 direct_delta = 0.15 adam_like_delta = 0.032
risk_weight step = 6 gradient = -3.0 direct_delta = 0.15 adam_like_delta = 0.049
recovery_weight step = 6 gradient = -0.29 direct_delta = 0.014 adam_like_delta = 0.05
noise_weight step = 6 gradient = 1.2 direct_delta = -0.06 adam_like_delta = -0.001
risk_weight step = 12 gradient = -0.4 direct_delta = 0.02 adam_like_delta = 0.03
recovery_weight step = 12 gradient = -0.05 direct_delta = 0.003 adam_like_delta = 0.034
noise_weight step = 12 gradient = 0.3 direct_delta = -0.015 adam_like_delta = -0.0

[final weights]
risk_weight direct_weight = 2.87 adam_like_weight = 1.502
recovery_weight direct_weight = 1.171 adam_like_weight = 1.52
noise_weight direct_weight = 1.07 adam_like_weight = 1.063
```

如果再把这些输出拆成`输入 gradient -> 每步 update -> 累积后的 weight`三层来读，Adam-like 试图补什么会更清楚。

![按参数区分的 gradient 流](/AiBook/assets/part-05/chapter-07/adaptive-gradient-history-ko.png)

第一阶段的输入，是 optimizer 尚未改动的 gradient 流。`risk_weight` 是较大的负 gradient 持续变小，`recovery_weight` 是较小的负 gradient 持续变小，`noise_weight` 则方向持续改变。简单 direct update 与 Adam-like 都会收到同一个输入。

![按坐标区分的平均 update 大小](/AiBook/assets/part-05/chapter-07/adaptive-delta-scale-ko.png)

delta 阶段开始出现差异。简单 direct update 会几乎原样把 gradient 大小差异转成 update 大小差异。Adam-like 因为同时使用最近流向和按坐标的大小历史，所以大的 gradient 坐标会被相对压住，小的 gradient 坐标也会按自己的历史被调节。

![按 update 规则区分的参数移动路径](/AiBook/assets/part-05/chapter-07/adaptive-weight-trajectory-ko.png)

看最终参数路径时，这种差异会累积起来。对于大 gradient 持续出现的 `risk_weight`，direct update 移动得远得多；对于小 gradient 稳定出现的 `recovery_weight`，Adam-like 反应更大；对于方向摇摆的 `noise_weight`，两条路径都没有走得太远。这一步真正改变的不是`重新计算了 gradient`，而是 optimizer 规则把同一条 gradient 流变成实际 parameter path 的方式。

这个例子并不是完整重现真实 Adam 公式，也不是在判定 direct update 与 Adam 的性能优劣。这里真正要读的是下面几点。

- 简单 direct update 会比较直接地反映当前 `gradient`
- Adam 类想法会累积最近方向和按坐标的大小历史，从而让逐 step update 不同
- optimizer 不是简单地`让它下降`，而是在决定同样的 gradient 要变成`怎样的 update 路径`

读完这个例子后，自适应 update 的补强会分成两个轴。

| 看的轴 | 直接确认到的变化 | 本节要留下来的句子 |
| --- | --- | --- |
| 时间轴 | 最近 gradient 会留在 moving average 里，使逐 step update 更平滑 | 自适应 update 不只看当前 gradient，也会看最近流向 |
| 坐标轴 | 每个参数会分别累积自己的 gradient 大小历史并调节步幅 | 自适应 update 不会把所有参数永远按同一标准步幅去推 |

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

- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 确认日期: 2026-07-19. [https://doi.org/10.1007/978-3-7908-2604-3_16](https://doi.org/10.1007/978-3-7908-2604-3_16){: target="_blank" rel="noopener noreferrer" }
- Diederik P. Kingma, Jimmy Ba, `Adam: A Method for Stochastic Optimization`, arXiv, 2014, 确认日期: 2026-07-19. [https://arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980){: target="_blank" rel="noopener noreferrer" }
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 确认日期: 2026-07-19. [https://arxiv.org/abs/1609.04747](https://arxiv.org/abs/1609.04747){: target="_blank" rel="noopener noreferrer" }
