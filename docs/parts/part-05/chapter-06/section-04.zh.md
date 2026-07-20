# P5-6.4 训练模式（training mode）与评估模式（evaluation mode）

> Section ID: `P5-6.4`
> Version: `v2026.07.20`

在 P5-6.3 里，我们已经把学习（learning）和模型执行（inference）区分成：`改变参数的时间`和`不改变参数、只拿来使用的时间`。再往前走一步，就会出现下一个问题。

既然参数没有改变，计算规则也必须永远完全一样吗？

答案并不总是如此。即使使用同一组参数，有些层（layer）在训练用计算状态和评估用计算状态下，也会表现得不同。只有把这个差别真正理解清楚，才不容易把 dropout、batch normalization、validation、test、部署推理混在一起。

训练模式（training mode）是为了准备参数更新而使用的计算环境，评估模式（evaluation mode）则是为了稳定测量或稳定使用当前模型而使用的计算环境。

如果后面在 dropout 或 batch normalization 的说明里又把 mode 区分重新混在一起，更适合回到[英文概念词汇表里的 training mode 条目](/AiBook/en/reference/concept-glossary/#training-mode)和[evaluation mode 条目](/AiBook/en/reference/concept-glossary/#evaluation-mode)，先重新确认这两个状态分别在管什么。

## 需要训练模式与评估模式的问题

- 为什么还要再把 training mode 和 evaluation mode 分开？
- 哪些层会对 mode 差异特别敏感，而不是所有层都一样？
- dropout 和 batch normalization 为什么会随 mode 改变行为？
- 为什么在 validation 和 test 里，evaluation mode 会很重要？

这一节专注于区分：即使是同一个模型，哪些计算规则更适合训练阶段，哪些计算规则更适合评估阶段。也就是说，这里是在先分开 learning 与 inference 之后，再继续闭合：`同样在使用参数的区间里，为什么还需要 training mode 和 evaluation mode。`

同样，这一节也不会马上把所有相关问题都扩开。dropout 和 regularization 的更大意义，会在 P5-8.1、P5-8.2 里再详细接回；optimizer 在整条学习流程里究竟站在什么位置，则会在 P5-7.1、P5-7.2 重新说明。

## 训练专用行为与执行行为的判断标准

- 能把 training mode 和 evaluation mode 解释成`计算规则会不同的两种状态`。
- 能说明 dropout 与 batch normalization 为什么对 mode 差异敏感。
- 能解释为什么 validation 与部署时，evaluation mode 很重要。
- 能用可运行的 Python 例子，直观确认 mode 差别。

## 为什么同一个模型还需要 mode

读者很容易把模型想象成一个固定函数。好像只要输入一样，它就应该始终做完全相同的计算，并给出完全相同的结果。

但在深度学习里，有些层为了让训练本身更顺利，会`故意引入随机波动`，或者`依赖当前 batch 的统计量`。这些做法在训练阶段可能有帮助，但到了评估或服务执行阶段，反而可能引入不必要的不稳定性。

也就是说，mode 的划分并不只是某个库的语法细节，而是为了下面这两个目的。

- 在训练时允许有助于泛化（generalization）的计算
- 在评估时让结果更稳定、更容易比较和复现

## training mode 指的是什么

training mode 通常可以先按下面几条来理解。

- 当前处在为了降低损失而进行的学习流程里
- forward 之后还可能继续接上损失计算与反向传播
- 有些层会为了帮助训练，而以特别的方式运作

也就是说，training mode 并不只是调用 `optimizer.step()` 的那一瞬间，而是指：`模型正在使用训练用的计算规则。`

## evaluation mode 指的是什么

evaluation mode 通常在下面这些场景里特别需要。

- 用验证数据（validation set）测量表现时
- 用测试数据（test set）确认最终性能时
- 在部署好的服务里处理真实用户输入时

这时最重要的，不是继续帮助模型摇摆着学习，而是尽量稳定地展现：`当前这个模型到底做得怎么样。` 因此，训练时那些带有随机波动或批量依赖的规则，往往就需要收起来，改用更固定的计算方式。

先把它压缩成一句话，会更容易记。

`评估模式是在测量现在的模型有多好，训练模式则是在把模型继续变得更好。`

如果只留下计算规则层面的差异，可以先压缩成下面这张图。

```mermaid
--8<-- "assets/part-05/chapter-06/training-eval-mode-flow-zh.mmd"
```

这张图最先要确认的结果是：即使模型与输入都相同，training mode 会更偏向`允许为了更新而出现的波动`，而 evaluation mode 会更偏向`稳定测量与稳定服务输出`。

## 哪些层对 mode 差异更敏感

并不是所有层都对 mode 差异一样敏感。比如常见的线性层（linear layer）或卷积层（convolution layer），在输入和参数相同时，整体计算逻辑通常不会因为 mode 而大幅变化。

但下面这些层或技巧，更适合先按训练中与评估中分别去读。

| 层或技巧 | 训练模式里的特点 | 评估模式里的特点 |
| --- | --- | --- |
| dropout | 会随机关闭一部分激活值 | 不再随机屏蔽，稳定使用全部路径 |
| batch normalization | 使用当前 batch 的统计量 | 使用训练阶段累计下来的统计量 |

也就是说，之所以需要 mode 差异，是因为有一些层会`为了帮助训练而故意采取不同的行为`。

## dropout 为什么在训练中和评估中不同

dropout 是一种在训练中随机切断部分节点输出的技巧，用来避免模型过度依赖少数固定路径。

先把它读成下面这句话就够了。

`训练时，故意让一部分连接休息一下，避免模型只抓住一两条信号不放。`

但如果在评估时也继续每次随机切断节点，那么结果就会变得摇摆不定。这样一来，就很难稳定地测出：当前模型到底本来有多好。

因此，在 evaluation mode 里，通常会停止 dropout 的随机屏蔽，改为使用已经学好的网络结构来稳定计算。

## batch normalization 为什么也需要 mode 差异

batch normalization 会利用当前 batch 的平均值（mean）和方差（variance）来调整激活值分布。训练中使用当前 batch 的统计量，本来是很自然的；但到了评估阶段，情况就不一样了。

评估数据往往：

- batch 很小
- 甚至可能一次只进来一个样本
- 每次评估时 batch 的组成也可能变化

如果这时还每次都只使用当前 batch 的统计量，结果就可能变得不稳定。所以在 evaluation mode 里，通常会改用训练中累计下来的 running statistics。

先把它记成下面这句话，会更安全。

`batch normalization 在训练时会参考当前 batch，而在评估时会更多参考训练过程中积累下来的平均性标准。`

## 为什么 validation 和 test 必须重视 evaluation mode

验证集与测试集的职责，是测量`当前模型的泛化能力到底怎么样。` 如果此时 training mode 还开着，dropout 仍然会继续随机波动，batch normalization 也会继续对当前 batch 的组成很敏感。

结果就会变成：

- 即使是同一个模型，测得的数值也不够稳定
- 分数会被 batch 构成偶然左右
- 和将来真正部署时用户感受到的表现不容易对齐

也就是说，validation 和 test 是`公平地测量当前模型`的时间，所以 evaluation mode 很重要。

## 练习与例子

mode 区分最适合在这些时刻被拿出来看：验证、部署、小 batch 评估，以及任何`计算规则本身会摇动结果解释`的时候。即使输入同一个 batch，在 `training mode` 和 `evaluation mode` 下，也可能因为不同的计算规则而走出两条不同路径。下面这个例子，会一步一步把这种差别作为中间产物展示出来。

这一版例子不会直接把一长串手工写好的数字塞进去，而是先从一小批用户会话数据算出隐藏层（hidden layer）激活值，再在这些激活值之上，分别施加 dropout 与 batch normalization 的 mode 差异。

输入：

- 每个会话的点击数与停留时间
- 一个简单隐藏层所用的权重与 bias
- dropout 比率
- 两个随机种子，用来复现两次训练模式运行
- evaluation mode 会参考的、过去学习阶段的会话 batch

输出：

- 从输入特征计算出来的隐藏层激活值
- dropout 之后的激活值
- normalization 使用的参考均值
- 减去该参考均值之后的简化输出

问题场景：

- 即使输入相同，训练模式允许波动，而评估模式需要更稳定的基准线

需要确认的概念：

- 在 training mode 里，部分激活值会被随机关闭
- training mode 下的 batch normalization 可以使用当前 batch 的基准
- evaluation mode 会停止 dropout，并改用学习中累计下来的 running mean

输入（input）：

我们会使用前面整理好的当前验证会话 batch 与过去学习阶段的会话 batch。这里的隐藏层计算会把最近点击数、停留时间、错误次数分别乘上权重，再加上 bias，然后只应用把负数裁成 0 的 ReLU（rectified linear unit）。而 batch normalization 为了把重点放在`参考均值来自哪里`，只保留 `值 - 参考均值` 这一部分。真实的 batch normalization 还会涉及方差，以及可学习的 scale 和 shift，但这一节里先不用把它们都展开。

在看代码之前，先猜一猜：哪些东西直接从数据里算出来，哪些东西会因为 mode 而摇摆或固定，会更容易抓住差别。

| 比较项 | 先猜测会看到什么输出 | 猜测理由 |
| --- | --- | --- |
| `hidden_activation` | 每个会话会得到不同的隐藏层数值 | 因为点击数和停留时间本来就不一样 |
| `train_run_1` 与 `train_run_2` 的 dropout 后数值 | 即使原始激活一样，结果模式也可能不同 | 因为训练模式下每次运行的 dropout mask 可能不同 |
| `train_run_1 batch_mean` 与 `train_run_2 batch_mean` | 很可能彼此不同 | 因为活下来的激活值一变，当前 batch 的平均值也会跟着变 |
| `eval_run` | 很可能会保留原本的隐藏层激活值 | 因为评估模式下不会再执行 dropout |
| `eval reference_mean` | 会保持成先前学习 batch 累积出来的固定基准 | 因为评估模式更倾向使用 running mean，而不是当前 batch 的偶然组成 |

这张表的目的，不是让人先把具体数字猜对，而是让人先抓住：训练模式下，即使是同一组隐藏层激活，执行两次也可能因为 dropout 和当前 batch 参考而不同；而评估模式会把这种摇摆停下来，改用稳定基准线。

```python
# 这个例子比较 train 模式和 eval 模式中 dropout 与 batch 参考均值如何摇动或固定。
from random import Random

validation_sessions = [
    {"id": "S01", "clicks_5m": 3, "dwell_seconds": 42, "error_count": 0},
    {"id": "S02", "clicks_5m": 6, "dwell_seconds": 55, "error_count": 1},
    {"id": "S03", "clicks_5m": 2, "dwell_seconds": 28, "error_count": 0},
    {"id": "S04", "clicks_5m": 7, "dwell_seconds": 70, "error_count": 2},
    {"id": "S05", "clicks_5m": 4, "dwell_seconds": 36, "error_count": 0},
    {"id": "S06", "clicks_5m": 5, "dwell_seconds": 48, "error_count": 1},
    {"id": "S07", "clicks_5m": 1, "dwell_seconds": 24, "error_count": 0},
    {"id": "S08", "clicks_5m": 8, "dwell_seconds": 73, "error_count": 2},
    {"id": "S09", "clicks_5m": 4, "dwell_seconds": 52, "error_count": 1},
    {"id": "S10", "clicks_5m": 6, "dwell_seconds": 61, "error_count": 0},
    {"id": "S11", "clicks_5m": 2, "dwell_seconds": 39, "error_count": 1},
    {"id": "S12", "clicks_5m": 7, "dwell_seconds": 58, "error_count": 2},
]
weights = {"clicks_5m": 0.18, "dwell_seconds": 0.015, "error_count": 0.32}
bias = -0.35
drop_rate = 0.4

def make_prior_batch(rows, dwell_shift, error_shift):
    batch = []
    for row in rows:
        batch.append({
            "clicks_5m": row["clicks_5m"],
            "dwell_seconds": max(12, row["dwell_seconds"] + dwell_shift),
            "error_count": max(0, row["error_count"] + error_shift),
        })
    return batch

prior_session_batches = [
    make_prior_batch(validation_sessions, dwell_shift=-4, error_shift=0),
    make_prior_batch(validation_sessions, dwell_shift=2, error_shift=1),
    make_prior_batch(validation_sessions, dwell_shift=5, error_shift=-1),
]

def hidden_activation(row):
    raw = (
        row["clicks_5m"] * weights["clicks_5m"]
        + row["dwell_seconds"] * weights["dwell_seconds"]
        + row["error_count"] * weights["error_count"]
        + bias
    )
    return round(max(0.0, raw), 3)

def make_dropout_mask(count, seed):
    rng = Random(seed)
    return [1 if rng.random() >= drop_rate else 0 for _ in range(count)]

def apply_dropout(values, mask, drop_rate):
    scale = 1 / (1 - drop_rate)
    result = []
    for value, keep in zip(values, mask):
        if keep == 0:
            result.append(0.0)
        else:
            result.append(round(value * scale, 3))
    return result

def mean(values):
    return round(sum(values) / len(values), 3)

def flatten(rows):
    return [value for row in rows for value in row]

def hidden_batch(batch):
    return [hidden_activation(row) for row in batch]

def center_by_mean(values, reference_mean):
    return [round(value - reference_mean, 3) for value in values]

def summarize(values):
    return {
        "count": len(values),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
        "mean": mean(values),
        "preview": values[:5],
    }

def run_training_mode(name, seed):
    mask = make_dropout_mask(len(activations), seed)
    after_dropout = apply_dropout(activations, mask, drop_rate)
    batch_mean = mean(after_dropout)
    centered_output = center_by_mean(after_dropout, batch_mean)
    return {
        "mode": name,
        "kept": sum(mask),
        "dropped": len(mask) - sum(mask),
        "after_dropout_summary": summarize(after_dropout),
        "reference_mean": batch_mean,
        "centered_preview": centered_output[:5],
    }

def run_evaluation_mode():
    after_dropout = activations[:]
    centered_output = center_by_mean(after_dropout, running_mean)
    return {
        "mode": "eval_run",
        "kept": len(after_dropout),
        "dropped": 0,
        "after_dropout_summary": summarize(after_dropout),
        "reference_mean": running_mean,
        "centered_preview": centered_output[:5],
    }

activations = [hidden_activation(row) for row in validation_sessions]
prior_hidden_batches = [hidden_batch(batch) for batch in prior_session_batches]
running_mean = mean(flatten(prior_hidden_batches))

train_run_1 = run_training_mode("train_run_1", seed=17)
train_run_2 = run_training_mode("train_run_2", seed=29)
eval_run = run_evaluation_mode()

print("validation_session_count =", len(validation_sessions))
print("hidden_activation_summary =", summarize(activations))
print("running_mean_from_prior_batches =", running_mean)
for result in [train_run_1, train_run_2, eval_run]:
    print(result["mode"])
    print("kept/dropped =", result["kept"], "/", result["dropped"])
    print("after_dropout_summary =", result["after_dropout_summary"])
    print("reference_mean =", result["reference_mean"])
    print("centered_preview =", result["centered_preview"])
```

输出里首先要确认的是：`hidden_activation_summary` 是从输入特征计算出来的隐藏层值摘要；然后再按顺序比较 `kept/dropped`、`after_dropout_summary`、`reference_mean`、`centered_preview`。

```text
validation_session_count = 12
hidden_activation_summary = {'count': 12, 'min': 0.19, 'max': 2.825, 'mean': 1.474, 'preview': [0.82, 1.875, 0.43, 2.6, 0.91]}
running_mean_from_prior_batches = 1.534
train_run_1
kept/dropped = 7 / 5
after_dropout_summary = {'count': 12, 'min': 0.0, 'max': 3.125, 'mean': 0.935, 'preview': [1.367, 3.125, 0.717, 0.0, 1.517]}
reference_mean = 0.935
centered_preview = [0.432, 2.19, -0.218, -0.935, 0.582]
train_run_2
kept/dropped = 6 / 6
after_dropout_summary = {'count': 12, 'min': 0.0, 'max': 4.708, 'mean': 0.947, 'preview': [1.367, 0.0, 0.717, 0.0, 1.517]}
reference_mean = 0.947
centered_preview = [0.42, -0.947, -0.23, -0.947, 0.57]
eval_run
kept/dropped = 12 / 0
after_dropout_summary = {'count': 12, 'min': 0.19, 'max': 2.825, 'mean': 1.474, 'preview': [0.82, 1.875, 0.43, 2.6, 0.91]}
reference_mean = 1.534
centered_preview = [-0.714, 0.341, -1.104, 1.066, -0.624]
```

这个例子并没有完整复现某个深度学习框架，但这里需要读出的核心很明确。

- 隐藏层激活值是由输入特征计算出来的中间产物
- 在训练模式里，即使放进去的是同一组隐藏层激活，dropout 后保留下来的激活值数量和组成也可能不同
- 只要 dropout 后的值不同，当前 batch 计算出来的参考均值也可能跟着变化
- 在评估模式里，dropout 会停下来，并改用过去学习 batch 累积出来的 running mean 作为更稳定的基准
- 这正是 validation、test、部署时为什么需要 evaluation mode 的原因

先把同一套计算规则重新用图来读。第一张图只展示：验证会话输入里的最近点击数、停留时间、错误次数怎样被变成隐藏层激活值。这里看到的还不是 mode 差异，而只是输入数据被映射成模型内部中间表示的那一步。

![会话输入对应的隐藏层激活值图](/AiBook/assets/part-05/chapter-06/hidden-activation-from-sessions-zh.png)

第二张图展示的是：同样的隐藏层激活，到了最后一层输出解释时，会因为 mode 不同而怎样变化。`train 1` 和 `train 2` 表示两次具有不同 dropout mask 的训练模式执行，`eval` 则表示关闭 dropout、并用 running mean 作为参考的评估执行。值大于 0 表示输出高于该参考均值，值小于 0 则表示输出低于该参考均值。

![两次 training mode 与一次 evaluation mode 的中心化输出比较图](/AiBook/assets/part-05/chapter-06/mode-centered-output-comparison-zh.png)

前两张图是例子代码本身的直接说明，下面两张图则是把同一种现象拉长到多次执行以后做的摘要。若只是把 `train_run_1` 和 `train_run_2` 两条样本线画出来，很容易看起来像是在硬比较人为挑的两个 mask；因此，这里把同样的计算规则应用到更长一点的小 batch 上，并把 30 次 forward pass 里 dropout 后保留下来的比例做成摘要。training mode 下，这个保留比例会跟着 pass 摇摆；evaluation mode 则因为关闭了 dropout，保留比例固定在 1.0 这条基准线上。

![training mode 下 dropout 保留比例会摇摆，而 evaluation mode 固定在 1.0 的图](/AiBook/assets/part-05/chapter-06/dropout-mode-output-trace-zh.png)

normalization 的参考均值也要用同样方式来读。training mode 下，每一次 forward pass 都会用 dropout 之后当前 batch 的数值重新算一个平均值，因此参考均值会波动；evaluation mode 下，基准线则来自学习期间累计好的 running mean，而不是来自这一次 pass 的偶然 mask。

![training mode 的 batch mean 会摇摆，而 evaluation mode 的 running mean 保持成基准线的图](/AiBook/assets/part-05/chapter-06/batchnorm-mode-reference-trace-zh.png)

这里再次要强调的是：只看到`输出不同`，和真正读懂`mode 改变了什么计算规则`并不是同一回事。

| 比较场景 | 较轻的误解 | 更危险的误解 | 现在先要确认的东西 |
| --- | --- | --- | --- |
| `train_run_1` 与 `train_run_2` 的 `after_dropout` 不同 | 认为训练时本来就会有一点摇摆 | 直接断言：同样输入却得不同结果，所以模型本身不可信 | 先看是不是处在允许随机性的 training mode |
| `reference_mean` 每次都不同 | 意识到当前 batch 的基准会变化 | 直接认为评估结果全部失真 | 先分清：这是 training mode 的 batch 基准，还是 eval mode 的 running 基准 |
| `eval_run` 看起来更固定 | 意识到评估模式更稳定 | 反而觉得评估也应该像训练那样多摇几次才更真实 | 先确认：验证、测试、部署的目的就是稳定比较 |

因此，这个例子的下一步确认点，不是停在`两种 mode 有差别`，而是继续问：如果把 mode 用错，会摇坏什么。

| 故意制造的失败场景 | 会看见什么东西被摇坏 | 本节先要确认的结果 |
| --- | --- | --- |
| 在验证阶段也直接拿 `run_training_mode(...)` 这样的输出来用 | 同样的输入重跑时，dropout 与当前 batch 基准会不必要地摇摆 | 性能测量会不会比模型本身更受随机性和 batch 构成影响？ |
| 把 `drop_rate` 从 0.4 提高到 0.7 | 训练模式输出会丢掉更多信息，平均激活值也更不稳定 | dropout 太强时，帮助泛化的效果是否开始被信息损失盖过去？ |
| 在评估里也试图像 train run 那样多次摇摆比较 | 原本应该固定的评估基准线被人为摇动 | `评估`和`允许训练中波动`是不是本来就是不同目的？ |

也就是说，这一节的实验不会停在`training/eval mode 不一样`这种定义确认上，而必须继续确认：如果在评估中也保留训练式的波动，究竟会把结果解释哪里弄坏。

随着深度学习模型变深、规模变大，仅靠`模型会学习权重`这种说法，已经很难把真实学习系统讲清楚。regularization、normalization、batch-based training 这些东西越来越常见之后，学习中和评估中的行为差异，就必须在课程里明确点出来。

特别是 dropout 作为减少过拟合（overfitting）的实用技巧，早已被广泛介绍；batch normalization 也常出现在深层网络的训练稳定性和速度讨论里。因此，在现代深度学习教育里，把 `training/eval mode` 单独作为一个概念来介绍，是很自然的。

换句话说，这一节不是某个库 API 的小技巧，而是在解释：`为什么深度学习模型看起来不像一个永远静止的函数，而更像一个带有运行状态的系统。`

## 什么时候需要单独读 training/eval mode 的差别

在先分清 learning 和 inference 之后，下一步就要单独确认：`即使是同一个模型，计算规则也会不会有些不同？` 这条边界就是 training/eval mode。

| 先出现的问题场景 | 为什么必须单独读 mode 差异 | 紧接着会连到哪里 |
| --- | --- | --- |
| 同样的输入，在训练中和验证中的感觉不一样 | 因为 dropout 与 batch normalization 可能会按 mode 不同而改变行为 | 后面会继续看 optimizer 在什么状态下真正更新 |
| 验证分数看起来忽高忽低 | 可以先明确：evaluation mode 是为了公平且稳定地测量 | 之后还会再去看 regularization 与 normalization 的意义 |
| 部署服务里的输出似乎波动很大 | 如果把训练用的随机行为原样带到服务执行里，就可能变得不稳定 | 会继续连到 inference serving 与 optimizer 分离的问题 |
| 对 dropout、batch normalization 为什么要特别处理没有感觉 | 可以把对 mode 敏感的层单独区分出来读 | 会和后面的正则化、优化器章节接上 |

## 检查清单

- 能解释 training mode 与 evaluation mode 为什么会采用不同的计算规则吗？
- 能说明 dropout 或 batch normalization 为什么必须重视 mode 差异吗？
- 能把 training mode 与 evaluation mode 解释成同一模型的两种不同计算状态吗？
- 能指出 dropout 与 batch normalization 是对 mode 差异特别敏感的代表例子吗？
- 能说明 validation、test、部署时为什么需要 evaluation mode 来提供更稳定的输出吗？
- 当同样输入在训练中和验证中表现感觉不同的时候，能先想到 training/evaluation mode 这条边界吗？
- 当需要压低验证和部署时的输出摇摆时，能说出 evaluation mode 提供的是稳定基准线吗？
- 能理解：这一节之后，课程会继续转向 optimizer，去看 gradient 怎样被改写成真正的更新规则吗？

## 出处与参考资料

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Nitish Srivastava et al., `Dropout: A Simple Way to Prevent Neural Networks from Overfitting`, JMLR, 2014, 确认日期: 2026-07-19. [https://jmlr.org/papers/v15/srivastava14a.html](https://jmlr.org/papers/v15/srivastava14a.html){: target="_blank" rel="noopener noreferrer" }
- Sergey Ioffe, Christian Szegedy, `Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift`, ICML, 2015, 确认日期: 2026-07-19. [https://arxiv.org/abs/1502.03167](https://arxiv.org/abs/1502.03167){: target="_blank" rel="noopener noreferrer" }
