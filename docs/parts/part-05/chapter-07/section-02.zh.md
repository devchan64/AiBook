# P5-7.2 学习率（learning rate）与 update 步幅

> Section ID: `P5-7.2`
> Version: `v2026.07.20`

在 P5-7.1 里，我们已经看到：优化器（optimizer）是`把 gradient 变成真实参数更新的规则`。走到这里，马上就会出现下一个问题。

既然 gradient 相同，那么为什么一次 update 仍然可能太小，或者太大？

回答这个问题时，最先出现的设置就是学习率（learning rate）。

学习率是 optimizer 把 gradient 变成真实 update 时，用来决定一次到底走多大的步幅。换句话说，如果 gradient 告诉你`该朝哪个方向改`，那么 learning rate 就是在决定`这一 step 到底沿着这个方向走多远。`

如果后面又开始把 learning rate、gradient、update 的关系混在一起，更适合回到[英文概念词汇表里的 learning rate 条目](/AiBook/en/reference/concept-glossary/#learning-rate)和[optimizer 条目](/AiBook/en/reference/concept-glossary/#optimizer)，重新把它们放回各自的位置。

## learning rate 怎样决定步幅的问题

- 学习率会接在 optimizer update 的哪一步？
- 为什么同样的 gradient，在不同 learning rate 下会得到不同 update？
- learning rate 太小或太大时，会分别发生什么？
- 为什么`gradient 方向正确`与`update 结果合适`并不是同一句话？

这一节专注于闭合一个问题：`同样的 gradient，真实到底走多远？` 也就是说，在已经理解 optimizer 角色的前提下，这里继续说明 learning rate 如何改变 update 的步幅。只有这条区分够清楚，后面看 Adam 这类自适应 optimizer 时，才不容易搞不清：它们究竟又额外调了什么。

同时，这一节不会马上扩大的问题也要明确。会同时参考最近 gradient 流向与按坐标差异来做调整的自适应 update，会在下一节 P5-7.3 继续说明；learning rate 不是一直固定，而是会随训练过程做 warmup 或 decay 的问题，会放到 P5-7.6 补充学习；adaptive optimization 的收敛分析则会单独放在 P5-7.4。

## update 大小与稳定性的判断标准

- 能把学习率解释成`optimizer update 的步幅`。
- 能说明：同样的 gradient，在不同 learning rate 下会得到不同 update 结果。
- 能解释为什么太小的步幅和太大的步幅会制造两种完全不同的问题。
- 能用一个可运行的 Python 例子确认 gradient 与 update 步幅的差别。

## optimizer 在做 update 时，learning rate 接在什么位置

之所以在讲 optimizer 时总会同时提到 learning rate，是因为 optimizer 把 gradient 变成真实 update 的那一刻，learning rate 正是以步幅的形式接进去。learning rate 本身不会直接改权重，但 optimizer 在决定`要改多大`时，它通常会作为最核心的缩放因子出现。也就是说，learning rate 并不是告诉模型`该往哪边走`，而是在已经知道方向之后，继续决定`这次沿着这个方向走多大。`

最简单的写法里，update 通常可以先按下面两行来读。

$$
\text{update} = - \text{learning rate} \times \text{gradient}
$$

$$
\text{new parameter} = \text{old parameter} + \text{update}
$$

这一节真正需要抓住的，并不是把公式硬背下来，而是读懂每个量在干什么。

- `gradient` 说明：往哪边改，损失更可能下降
- `learning rate` 决定：这个方向信号要被放大还是缩小到什么程度
- `update` 则是两者组合之后，真正应用到参数上的移动量

把这两行连起来读，learning rate 的位置就很清楚了。第一行里，它在决定 gradient 到底会被变成多大的 update；第二行里，这个 update 再被真实地反映到参数上。也就是说，learning rate 不是直接改损失的数字，而是通过控制参数移动幅度，间接影响下一次预测和下一次损失。

如果跳过这层解释，读者就很容易在`gradient 已经算出来了`和`参数已经变了`之间，漏掉：到底是谁在决定移动量大小。P5-7.2 正是在解释这条中间链。

如果 learning rate 太小：

- 学习会变得非常慢
- 损失下降会拖很久

如果 learning rate 太大：

- 即使方向是对的，也可能一步越过去
- 损失会变得不稳定，甚至重新变大

因此，learning rate 更准确的读法是：optimizer 在做 update 时使用的`步幅（step size）`。即使 gradient 完全一样，只要 learning rate 不同，真实移动量就会不同，下一 step 开始时参数所在的位置也会不同。

正如 Part 4 讲过超参数（hyperparameter）时提到的，learning rate 不是学习自己产生出来的参数，而是人先设定或搜索的设置值。

这里最好把下面这张区分表也一起固定住。

| 值 | 角色 |
| --- | --- |
| gradient | 告诉你在当前位置哪边更像下降方向的信号 |
| learning rate | 决定你沿着这个方向一次要走多远的步幅 |
| optimizer | 把这个步幅和规则真正应用成移动的过程 |

如果把这张表再压成一句话，就是：`gradient 是方向，learning rate 是距离，optimizer 负责真实移动。`

## 为什么同样的 gradient，结果仍然会不同

即使知道同一个位置上的下降方向，如果步幅太小，你几乎前进不了；如果比较合适，就可能靠近更低损失的位置；如果太大，就可能直接越过更好的点，让损失重新变大。这里最重要的是：`知道方向`和`成功走到更好的下一位置`并不是同一件事。

![不同 learning rate 在损失曲线上的步幅](/AiBook/assets/part-05/chapter-07/learning-rate-step-size-zh.svg)

这张图最重要的信息，是：`gradient 方向正确`与`optimizer 做出的 update 合适`不是同一句话。读 optimizer 时，不要只看方向信号，还要继续看：这个信号最后把参数推到了哪里。即使沿着同一支箭头走，步子太短时几乎没进展，步子太长时则可能越过更好的位置。learning rate 决定的，正是这`一步的长度。`

因此更安全的读法是下面三句。

- gradient 告诉你`该朝哪边去`
- learning rate 决定`要走多远`
- 所以即使 gradient 一样，只要 learning rate 不同，结果就会不同

## 案例与示例

这一节的案例，不是在比谁是更有名的 optimizer，而是在看：`同一个 gradient，如何因为不同步幅而变成不同结果。` 因此，案例最好按下面三个问题来读。

1. gradient 的方向是不是一致的？
2. learning rate 把 optimizer update 放大或缩小了多少？
3. update 之后，参数与损失到底怎样变了？

### 案例. gradient 相同，但 learning rate 不同

假设当前状态完全一样，算出来的 gradient 也完全一样。比如当前风险权重是 `1.0`，算出来的 `gradient_risk_weight` 都是 `-20.648`。现在唯一变化的，就是 learning rate。

这里读者真正要看的，不是`哪个 optimizer 更有名`，而是：`同样的方向信号，会怎样被变成完全不同的真实移动量。`

第一次读这个场景的人，常常会想：`既然 gradient 一样，最后不是应该学得差不多吗？` 这种想法并不奇怪，因为如果只盯着方向看，三种情况确实都在朝着同一边走。但从 learning rate 的角度看，问题早就变了。现在关键不是`朝哪边走`，而是`沿着这个方向到底走多远。`

假设 learning rate 分别是 `0.003`、`0.03`、`0.12`。

- 如果是 `0.003`，update 会很小。方向虽然对，但一 step 几乎走不了多远，看上去损失也许会下降，可实际训练仍然可能慢得让人着急。
- 如果是 `0.03`，同样的 gradient 会被变成一个比较合理的移动量。它既不至于几乎不动，也不至于一下越过去，更可能把 batch 平均预测拉近目标。
- 如果是 `0.12`，update 就会过大。方向虽然仍然没错，但步子太猛，可能直接越过目标，导致损失重新变大，或者学习开始剧烈晃动。

所以三种情况真正不同的，不是方向，而是步幅。learning rate 不会重新生成 gradient，它只是在决定：已经算出来的这个 gradient，要被多大程度地反映成真实 update。

如果把这个场景重新做成表，大概就是下面这样。

| 面对同一个 gradient 时 | learning rate 太小 | learning rate 比较合适 | learning rate 太大 |
| --- | --- | --- | --- |
| 真实 update 的大小 | 小到几乎不动 | 足以靠近目标 | 大到可能越过目标 |
| 表面上看到的结果 | 损失下降很慢 | 损失下降明显 | 损失重新变大或明显摇摆 |
| 更准确的解释 | 方向是对的，但前进幅度不足 | 方向与步幅都比较匹配 | 方向虽然对，但步幅过于激烈 |

这个案例真正支撑本节的地方，就在于：learning rate 不是一个附带数字，而是决定`同样的 gradient 到底被反映成多大真实移动量`的值。因此，P5-7.2 里要固定住的中心句，就是：`同样的 gradient，只要 learning rate 不同，真实 update 结果就会不同。`

## 练习与例子

这一节例子的目标，是让人直接看到：同一个 gradient 计算结果，会在不同 learning rate 下变成完全不同的 update。这里真正要读的，不是 learning rate 数字本身，而是 `optimizer_delta` 怎样变化。这个例子里，固定不动的是`同一个 CSV batch`、`当前风险权重`和`gradient`，会变化的则是 learning rate 与因此产生的真实移动量。

在看代码之前，先把`固定不变的`和`真正变化的`分开，会更容易。

| 固定不变的 | 会变化的 |
| --- | --- |
| CSV batch 与当前风险权重 `risk_weight` | 学习率 `learning_rate` |
| batch 当前平均预测值与平均损失 | `optimizer_delta` |
| 从 batch 计算出来的平均 `gradient_risk_weight` | 更新后的权重、平均分数、平均损失 |

输入：

- 当前风险权重 `risk_weight`
- CSV 文件里的多条观测行
- 每一行的压力未恢复程度 `pressure_unrecovered`
- 每一行的目标阻断分数 `target_block_score`
- 学习率 `learning_rate`

输出：

- 平均目标阻断分数
- 当前平均损失
- 平均 gradient
- optimizer 做出的 update 值
- 不同 learning rate 下更新后的权重
- 更新后的平均预测与平均损失比较

问题场景：

- learning rate 不会改动 gradient 本身，但会大幅改变 optimizer 做出的 batch update 幅度
- 太大的 learning rate 即使方向正确，也可能越过更好的位置，因此必须连结果一起看

需要确认的概念：

- 同一个 gradient，也可能得到不同大小的 update
- update 大小一旦改变，新的权重、新的预测、新的损失都会跟着变化
- 所以`算出了 gradient`并不等于`学习就一定进行得合适`

```python
# 这个例子在同一个 CSV batch 和同一个 gradient 下，只改变 learning rate，
# 比较 update 幅度、平均预测和平均损失的变化。
from csv import DictReader
from pathlib import Path

DATA_PATH = Path("docs/assets/part-05/chapter-07/optimizer-step-role-log.csv")


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return [
            {
                "case_id": row["case_id"],
                "equipment_group": row["equipment_group"],
                "pressure_unrecovered": float(row["pressure_unrecovered"]),
                "target_block_score": float(row["target_block_score"]),
            }
            for row in DictReader(f)
        ]


def predict(row, risk_weight):
    return row["pressure_unrecovered"] * risk_weight


def mean_loss(rows, risk_weight):
    losses = [
        (predict(row, risk_weight) - row["target_block_score"]) ** 2
        for row in rows
    ]
    return sum(losses) / len(losses)


def mean_gradient(rows, risk_weight):
    gradients = [
        2
        * (predict(row, risk_weight) - row["target_block_score"])
        * row["pressure_unrecovered"]
        for row in rows
    ]
    return sum(gradients) / len(gradients)


def mean_prediction(rows, risk_weight):
    predictions = [predict(row, risk_weight) for row in rows]
    return sum(predictions) / len(predictions)


rows = load_rows(DATA_PATH)
risk_weight = 1.0
loss = mean_loss(rows, risk_weight)
gradient_risk_weight = mean_gradient(rows, risk_weight)
mean_target = sum(row["target_block_score"] for row in rows) / len(rows)

print("[shared state]")
print("sample_count =", len(rows))
print("mean_target_block_score =", round(mean_target, 3))
print("mean_loss_before =", round(loss, 3))
print("gradient_risk_weight =", round(gradient_risk_weight, 3))
for lr in [0.003, 0.03, 0.12]:
    print(f"[lr={lr}]")
    optimizer_delta = -lr * gradient_risk_weight
    updated_risk_weight = risk_weight + optimizer_delta
    updated_prediction = mean_prediction(rows, updated_risk_weight)
    updated_loss = mean_loss(rows, updated_risk_weight)
    print(
        "optimizer_delta =", round(optimizer_delta, 3),
        "-> updated_risk_weight =", round(updated_risk_weight, 3),
        ", mean_block_score =", round(updated_prediction, 3),
        ", mean_loss =", round(updated_loss, 3),
    )
```

```text
[shared state]
sample_count = 36
mean_target_block_score = 6.139
mean_loss_before = 7.308
gradient_risk_weight = -20.648
[lr=0.003]
optimizer_delta = 0.062 -> updated_risk_weight = 1.062 , mean_block_score = 3.77 , mean_loss = 6.087
[lr=0.03]
optimizer_delta = 0.619 -> updated_risk_weight = 1.619 , mean_block_score = 5.749 , mean_loss = 0.287
[lr=0.12]
optimizer_delta = 2.478 -> updated_risk_weight = 3.478 , mean_block_score = 12.346 , mean_loss = 48.454
```

这段输出里展示的，正是同一个 gradient 经过 optimizer update 规则之后，被变成不同 `optimizer_delta` 的场景。所以不要停在`gradient 是多少`，而要继续按步骤去看：optimizer 做出的 update 值、更新后的权重、更新后的分数、更新后的损失。

而且这里特别重要的一点是：这三组结果不是来自三个不同 gradient，而是来自`同一个 shared state`。上面的 `[shared state]` 区域明确写出了：CSV batch、当前平均损失、gradient 都是共享的；下面 `[lr=0.003]`、`[lr=0.03]`、`[lr=0.12]` 才是在比较：如果只改 learning rate，会发生什么。

![不同 learning rate 下 batch update 后的风险权重](/AiBook/assets/part-05/chapter-07/learning-rate-batch-updated-weight-ko.png)

![不同 learning rate 下 batch update 后的平均阻断分数](/AiBook/assets/part-05/chapter-07/learning-rate-batch-updated-score-ko.png)

![不同 learning rate 下 batch update 后的平均损失](/AiBook/assets/part-05/chapter-07/learning-rate-batch-updated-loss-ko.png)

一起读这三张图时，更安全的顺序是下面这样。先看 `learning-rate-batch-updated-weight`，确认 learning rate 如何让真实移动量把权重数字改得很不一样；再看 `learning-rate-batch-updated-score`，确认这种差别如何把 batch 平均预测值带到不同位置；最后看 `learning-rate-batch-updated-loss`，确认它最终让平均损失只是稍微下降、明显下降，还是因为越过目标而变大。

这个例子里，读者至少要确认下面这些点。

- gradient 相同，但结果仍然可能完全不同
- 真正造成差别的，是 learning rate 变出来的 `optimizer_delta`
- `0.03` 让结果更接近平均目标，而 `0.12` 虽然方向也对，却因为走得太大反而把平均损失推高了
- 所以`算出了 gradient`与`学习进行得合适`并不是同一句话

## 什么时候要先用 learning rate 视角来读

当你已经看懂了 gradient，却还看不明白`为什么模型移动得这么慢或这么粗暴`时，就要先把这一节拿出来。

| 先出现的问题场景 | 为什么 learning rate 视角先有用 | 紧接着要看的问题 |
| --- | --- | --- |
| gradient 看起来没错，但参数几乎不动 | 它会迫使你先确认 update 步幅是不是太小 | 后面还要继续看 Adam 这类自适应 update 还想补什么 |
| 损失持续跳动、发抖 | 它会先让你检查：问题是不是在于步幅太大，而不是方向有错 | 接下来要看最近流向与按坐标调节的 optimizer |
| 同一个 gradient 为什么会得到不同结果直觉上不清楚 | 它能固定住：learning rate 会直接改变 update 步幅 | 后面还要继续看 P5-7.3 的自适应 update 差异 |

## 检查清单

- 能把学习率（learning rate）解释成`optimizer update 的步幅`吗？
- 能说明：同样的 gradient，在不同 learning rate 下会得到不同 update 结果吗？
- 能解释太小的 learning rate 与太大的 learning rate 会制造什么不同问题吗？
- 能区分`gradient 方向正确`与`update 结果合适`吗？
- 能知道下一节 P5-7.3 会继续说明 Adam 类方法如何把最近流向与按坐标差异也一起考虑进去吗？

## 来源与参考资料

- PyTorch, `Optimizing Model Parameters`, PyTorch Tutorials. 用于确认 optimizer 使用 gradient 调整参数，并把 learning rate 作为 hyperparameter 接收的结构。确认日期：2026-07-19. [https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html){: target="_blank" rel="noopener noreferrer" }
- PyTorch, `torch.optim.SGD`, PyTorch API Reference. 用于确认 SGD update 中 `lr` 与 momentum 如何进入参数更新。确认日期：2026-07-19. [https://docs.pytorch.org/docs/stable/generated/torch.optim.SGD.html](https://docs.pytorch.org/docs/stable/generated/torch.optim.SGD.html){: target="_blank" rel="noopener noreferrer" }
