# P5-8.4 补充学习：较大的初始化尺度会怎样摇晃计算范围

> Section ID: `P5-8.4`
> Version: `v2026.07.26`

在 P5-8.3 里，我们把让深层计算没那么容易摇晃的条件，收成了 initialization、numerical stability、batch normalization 三个概念。现在要用实际数字来确认那条说明。

核心问题非常简单。

当同样的 activation 穿过多层时，较大的 initialization scale 到底会把数值放大到什么程度？

这一节不会重现完整的真实学习过程。它只是假设：从前一层传来的 activation，会连续经过 3 层相同的 linear transform，并比较小尺度和大尺度会怎样改变各层的输出范围与 variance。这里每一层都乘上的那个单一 scalar，只要读成`把该层权重尺度简化后拿来代表的玩具实验值`就够了。然后我们还会一起看：如果在每一层后面插入 batch normalization，输出范围会怎样重新被整理成更容易处理的形式。

## 较大初始化尺度会摇晃哪些范围

- 较大的 initialization scale 会怎样在深层重复计算里放大 raw activation 的范围和 variance？
- 如果在每一层后面都加入 batch normalization，同一条计算流程会怎样变化？
- 这个例子虽然不能代替完整神经网络，但它怎样帮助我们抓住计算稳定化的直觉？

作为第 8 章的最后一步，这一节的角色，是用数字再次确认前一节已经收拢好的`计算稳定化装置`。这也是为什么这里不讨论 optimizer update、loss 下降、真实数据集训练成绩。那些话题会让位给 P5-6.1 的学习循环说明，以及 P5-7.1、P5-7.2 的 optimizer 说明。

## 读这个例子的标准

下面这个例子的输入，并不是随便列出来的一张数字表，而是被假设为从前一层传过来的三个样本的 activation value。

| 样本 | 前一层传来的 activation |
| --- | ---: |
| A | 1.0 |
| B | 2.0 |
| C | 0.5 |

权重尺度会分成四种情况。

| 情况 | 每一层乘上的值 | 最先该预测的变化 |
| --- | ---: | --- |
| `small_init` | 0.8 | 数值会随着层数逐渐缩小 |
| `medium_init` | 1.2 | 数值会一点点变大 |
| `large_init` | 3.0 | 数值范围和 variance 会快速扩大 |
| `very_large_init` | 9.0 | 在深层重复计算里数值会爆炸性增长 |

这里最重要的点，不是`值变大了，所以表示更丰富`。真正重要的是：如果同样的模式在深层里被不断重复，下一层接收到的数值范围和 gradient path 都可能一起变得更容易摇晃。

这个例子更适合边改边看，而不是只运行一次。更好的做法是，直接改下面这些值，然后观察哪类输出最先变得敏感。

| 最先可以改的值 | 最先该看的输出 | 该怎样解读的问题 |
| --- | --- | --- |
| `weight_cases` 里的尺度 | `raw_range`, `raw_variance` | 起始尺度越大，重复计算会多快把范围拉大？ |
| `layer` 的重复次数 | 各层 `raw_range`, `raw_variance` 的变化 | 在同样尺度下，层数变多时不稳定会积累到什么程度？ |
| 输入 activation 表 | `raw_range`, `after_bn_range` | 输入 distribution 一旦变化，batch normalization 之后的范围又会怎样一起变化？ |
| `eps` | `after_bn_range` 的细微变化 | batch normalization 是怎样以 mean 和 variance 为标准整理 distribution 的？ |

这里也要先固定一件事。下面的 batch normalization 结果，并不意味着`初始化再怎么随便变大都没关系`。这个玩具实验只是想分离展示：`在样本相对形状不变、只改尺度时，distribution 会怎样重新被整理。` 所以更安全的读法，是把 batch normalization 看成`重新整理已经产生的 distribution 的装置`，而不是把它看成会替代 initialization 出发点问题的东西。

## Python 例子

```python
# 这个例子读取 CSV activation 日志，比较 initialization scale 是否会放大深层 raw range 和 variance，以及 batch normalization 是否会重新整理范围。
from csv import DictReader
from pathlib import Path


def batch_norm(values, eps=1e-5):
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    normalized = [(v - mean) / ((variance + eps) ** 0.5) for v in values]
    return mean, variance, normalized

csv_path = Path("docs/assets/part-05/chapter-08/deep-scale-activation-log.csv")

rows = []
with csv_path.open(encoding="utf-8") as file:
    for row in DictReader(file):
        rows.append(
            {
                "case_name": row["case_name"],
                "weight_scale": float(row["weight_scale"]),
                "layer": int(row["layer"]),
                "sample": row["sample"],
                "raw_activation": float(row["raw_activation"]),
            }
        )

case_order = ["small_init", "medium_init", "large_init", "very_large_init"]
layer_order = [1, 2, 3]

for case_name in case_order:
    case_rows = [row for row in rows if row["case_name"] == case_name]
    weight = case_rows[0]["weight_scale"]
    print(f"[{case_name}] weight = {weight}")

    for layer in layer_order:
        layer_rows = [
            row for row in case_rows
            if row["layer"] == layer
        ]
        raw_values = [row["raw_activation"] for row in layer_rows]
        _, raw_variance, bn_values = batch_norm(raw_values)

        print(
            f"layer {layer}: "
            f"raw_range=({min(raw_values):.3f}, {max(raw_values):.3f}), "
            f"raw_variance={raw_variance:.3f}, "
            f"after_bn_range=({min(bn_values):.3f}, {max(bn_values):.3f})"
        )
    print("---")
```

这段代码会读取 [`deep-scale-activation-log.csv`](/AiBook/assets/part-05/chapter-08/deep-scale-activation-log.csv) 里记录的 36 个值，并按 case 和 layer 重新计算范围与 variance。它并不是在实现`一个完整的真实神经网络层`，而是一个压缩实验，只想看：`权重尺度在穿过层时，会把数值范围和 variance 推向哪里。` 因此，我们首先要看的不是精确训练成绩，而是`重复计算与尺度累积的方向`。

输出示例如下。

```text
[small_init] weight = 0.8
layer 1: raw_range=(0.400, 1.600), raw_variance=0.249, after_bn_range=(-1.069, 1.336)
layer 2: raw_range=(0.320, 1.280), raw_variance=0.159, after_bn_range=(-1.069, 1.336)
layer 3: raw_range=(0.256, 1.024), raw_variance=0.102, after_bn_range=(-1.069, 1.336)
---
[medium_init] weight = 1.2
layer 1: raw_range=(0.600, 2.400), raw_variance=0.560, after_bn_range=(-1.069, 1.336)
layer 2: raw_range=(0.720, 2.880), raw_variance=0.806, after_bn_range=(-1.069, 1.336)
layer 3: raw_range=(0.864, 3.456), raw_variance=1.161, after_bn_range=(-1.069, 1.336)
---
[large_init] weight = 3.0
layer 1: raw_range=(1.500, 6.000), raw_variance=3.500, after_bn_range=(-1.069, 1.336)
layer 2: raw_range=(4.500, 18.000), raw_variance=31.500, after_bn_range=(-1.069, 1.336)
layer 3: raw_range=(13.500, 54.000), raw_variance=283.500, after_bn_range=(-1.069, 1.336)
---
[very_large_init] weight = 9.0
layer 1: raw_range=(4.500, 18.000), raw_variance=31.500, after_bn_range=(-1.069, 1.336)
layer 2: raw_range=(40.500, 162.000), raw_variance=2551.500, after_bn_range=(-1.069, 1.336)
layer 3: raw_range=(364.500, 1458.000), raw_variance=206671.500, after_bn_range=(-1.069, 1.336)
---
```

这份输出里，最先要盯住的是 `very_large_init` 那一组数字。第一层里，raw range 还是 `(4.500, 18.000)`；但到了第三层，就已经扩大到 `(364.500, 1458.000)`。输入模式完全没变，只是让它重复穿过几层而已，可是当尺度很大时，数值范围就会随着深度迅速被拉开。

从入门读者角度，最好不要把这份输出只当成一整块数字，而是按照下面三行再重读一次。

| 输出里先看到的行 | 接着该马上追问的问题 | 这里要抓住的概念 |
| --- | --- | --- |
| `very_large_init` 的 `raw_range` 每一层都急剧变大 | 同样模式重复时，数值范围会多快开始变得不稳定？ | 较大的 initialization scale 会在深层计算里摇动数值稳定性 |
| `raw_variance` 也跟着变大 | 下一层收到的输入扩散会不会一直继续变大？ | 扩散越大，后续计算和 gradient path 就越可能一起摇晃 |
| `after_bn_range` 又重新聚到可比较的范围里 | batch normalization 重新整理的到底是什么？ | batch normalization 并不是消掉 initialization 问题，而是在整理中间 distribution |

## 用图分开来读

第一张图展示的是每一层的 raw activation range。`large_init` 和 `very_large_init` 都会随着层数加深，把同一批样本之间的数值范围迅速拉开。

![按 initialization scale 比较逐层 raw activation range](/AiBook/assets/part-05/chapter-08/deep-scale-raw-range-zh.png)

第二张图把同样现象压成 variance 来看。因为 variance 会把数值扩散压成一个单独数字，所以会更容易读出：在深层里，较大的尺度会多快制造出不稳定范围。

![按 initialization scale 比较逐层 raw variance](/AiBook/assets/part-05/chapter-08/deep-scale-raw-variance-zh.png)

第三张图展示的是：每一层后面都加上 batch normalization 之后，输出范围会变成什么样。raw activation 在不同 case 之间差异很大，但 normalization 之后，范围会被重新整理到`下一层更容易处理的相近规模`。这里最重要的点不是`数值永远都被固定成一模一样`，而是：`即使输入 distribution 差很多，中心和扩散也会被重新拉回可比较的范围。` 在这个玩具实验里，几种 case 的范围看起来几乎一样，是因为三个样本之间的相对形状保持不变，我们只改了整体尺度。所以不能光看这一张图，就下结论说`batch normalization 几乎把 initialization 问题抹掉了。` 这张图也没有使用追踪变化的折线图，而是按 case 做成点比较，让读者先看到`几乎聚到相近范围`这个事实。

![batch normalization 之后的逐层 activation range](/AiBook/assets/part-05/chapter-08/deep-scale-bn-range-zh.png)

## 这里该读出的结论

| 输出里看到的现象 | 如果原样放着，容易留下的解读 | 用稳定化视角重读后的解读 |
| --- | --- | --- |
| `very_large_init` 的 raw range 和 variance 在每一层都迅速放大 | 容易觉得大数值代表更强表示，所以是好信号 | 在深层重复计算里，过大的尺度会变成一个数值稳定性问题，让下一层和 gradient path 都跟着摇晃 |
| batch normalization 之后，各种 case 的 range 又被整理成相近规模 | 容易觉得 batch normalization 只是把大数值直接消掉了 | 它是在重新对齐中间 distribution 的中心和扩散，让下一层拿到更容易处理的输入范围 |
| `small_init` 的 raw variance 反而会变小 | 容易觉得越小就一定越安全 | 过小的尺度也可能把深层里的信号和 gradient 一路变弱，因此只靠“小”本身并不够 |

因此，initialization 和 batch normalization 并不是在同一个位置解决同一个问题的装置。initialization 负责设定出发尺度，而 batch normalization 负责重新整理已经在层间产生出来的 activation distribution。numerical stability 则是共同问题，用来说明为什么这两者会在深层网络里一起被讨论。

这个实验想让读者首先抓住的结论很简单。它的作用，是让人亲眼看到：`权重尺度一旦变大，raw activation range 和 variance 会以多快的速度变得不稳定`，以及`为什么插入 batch normalization 之后，下一层收到的规模又会被拉回可比较的范围。`

## 检查清单

- 能说明较大的 initialization scale 会在层与层之间真的放大 raw activation range 吗？
- 能说明 raw variance 可以作为一个简单观察值，用来读深层重复计算的不稳定吗？
- 能说明 batch normalization 不是在消灭大数值，而是在重新设定 distribution 标准吗？
- 能区分这个例子不是完整训练过程，而是一个用来确认数值稳定性直觉的小实验吗？

## 出处与参考资料

- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, `Dive into Deep Learning`, `5.4 Numerical Stability and Initialization`, `8.5 Batch Normalization`, 确认日期：2026-07-14。 [https://d2l.ai/](https://d2l.ai/){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, Part II `Modern Practical Deep Networks`, 确认日期：2026-07-14。 [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
