# P5-3.5 代表性激活函数公式比较

> Section ID: `P5-3.5`
> Version: `v2026.07.26`

从 P5-3.2 到 P5-3.4，我们已经分别看过 sigmoid、tanh、ReLU。现在把这三个函数放在一起比较。这里的目的不是背名字，而是确认：同样的分数 \(z\)，在不同公式与不同输出范围下，究竟会变成怎样的值。

如果代表性激活函数之间的比较再次变模糊，可以先把概念词汇表里的[激活函数（activation function）](/AiBook/zh/reference/concept-glossary-pinyin/j/#activation-function)和[sigmoid](/AiBook/zh/reference/concept-glossary-pinyin/s/#sigmoid)条目作为基准线，再在同一组激活函数比较里重读 tanh 与 ReLU。

## 比较代表性激活函数的问题

- 在一张表里比较 sigmoid、tanh、ReLU 的公式。
- 比较它们的输出范围以及是否会饱和。
- 检查同样的输入值在不同函数下会怎样变化。
- 把这种比较继续接到下一节的输出层问题上。

这一节不会长篇重复每个函数的历史和具体使用场景。各自的直觉已经在 P5-3.2、P5-3.3、P5-3.4 处理过，而输出层到底该用什么，会在 P5-3.6 继续。

## 图形形状与输出范围的判断标准

- 能把三个代表性激活函数的公式并排比较。
- 能用输出范围与饱和这两个标准解释它们的差异。
- 能通过数值确认：即使是同一个 \(z\)，传给下一层的值也会不同。
- 能把函数比较接到输出层解读与损失函数上。

## 公式比较

| 函数 | 公式 | 输出范围 | 核心反应 |
| --- | --- | --- | --- |
| sigmoid | \(\sigma(z)=\frac{1}{1+e^{-z}}\) | \(0 < \sigma(z) < 1\) | 压缩到 0 与 1 之间 |
| tanh | \(\tanh(z)=\frac{e^z-e^{-z}}{e^z+e^{-z}}\) | \(-1 < \tanh(z) < 1\) | 围绕 0 压缩正负值 |
| ReLU | \(f(z)=\max(0,z)\) | \(0 \le f(z)\) | 截断负值，放行正值 |

这张表里首先要看的有三条轴。

1. 输出被限制在什么范围里？
2. 负输入会不会继续留给下一层？
3. 较大的正输入还能不能继续增大？

## 用图来比较

先看曲线形状，而不是先记名字，差异会更快出现。

![sigmoid 函数曲线](/AiBook/assets/part-05/chapter-03/sigmoid-curve-zh.svg)

![tanh 函数曲线](/AiBook/assets/part-05/chapter-03/tanh-curve-zh.svg)

![ReLU 函数曲线](/AiBook/assets/part-05/chapter-03/relu-curve-zh.svg)

把这三张图放在一起看时，会发现 sigmoid 与 tanh 都会在两端饱和。也就是说，输入继续变大或变小，输出却会在 1 或 -1 附近越来越不明显地变化。相反，ReLU 会把负值切成 0，但在正值区间仍然沿直线继续增大。

## 把同样的分数送进去比较

假设某个设备警告模型里的隐藏节点，形成了下面这五个分数。

| 场景 | \(z\) | sigmoid | tanh | ReLU |
| --- | --- | --- | --- | --- |
| 安静场景 | \(-2\) | 0.119 | -0.964 | 0 |
| 稳定恢复场景 | \(-0.5\) | 0.378 | -0.462 | 0 |
| 边界警报场景 | \(0.1\) | 0.525 | 0.100 | 0.1 |
| 已确认警告场景 | \(0.5\) | 0.622 | 0.462 | 0.5 |
| 需要立即评估停机场景 | \(3\) | 0.953 | 0.995 | 3 |

这些数字不用死记。真正要读出来的结果是下面这几点。

- sigmoid 会把值永远压到 0 与 1 之间，因此容易被读成某种风险度或倾向分数。
- tanh 会把值压到 -1 与 1 之间，同时保留负号与正号。
- ReLU 会把所有负值都变成 0，而把正值之间的差异原样保留下来。

## 这种比较到底怎么用

| 先需要哪种计算感觉 | 更先想到哪个函数 | 理由 |
| --- | --- | --- |
| 想把值读成 0 到 1 之间 | sigmoid | 输出范围在 0~1，容易接到二元分类的感觉上。 |
| 想同时保留负方向与正方向 | tanh | 它会围绕 0 保留两侧的符号。 |
| 想切掉负值，只保留正向信号 | ReLU | 正值区间里的差异会继续活下来。 |

做完这个比较之后，下一步自然会变成另一个问题：`在最后的输出层，应该选择什么样的激活？` 隐藏层激活是在处理内部表征，而输出层激活则是在处理最后那个数字到底要被读成什么。这个区分会在 P5-3.6 继续。

## 练习与例题

这次练习的目标，不是去选某个函数名字，而是直接确认：同样的线性分数 \(z\)，经过三种激活函数之后，会变成怎样的输出范围与怎样的信号形态。

在看代码前，先猜下面三个值。

| 先看的值 | 为什么要先看它 |
| --- | --- |
| `z = -3.0` | 因为它最能看出负输入在三种函数里会怎样保留或消失。 |
| `z = 0.0` | 因为它正好是 sigmoid 去到 0.5，而 tanh 与 ReLU 去到 0 的基准点。 |
| `z = 2.5` | 因为它最能看出 sigmoid 与 tanh 被压向 1，而 ReLU 仍把 2.5 原样保留下来。 |

输入：

- 来自几个场景的线性分数 \(z\)
- sigmoid、tanh、ReLU 三个函数

输出：

- 同一个 \(z\) 在三种函数下对应的输出值
- 对负输入处理、0 附近反应、大正值处理的差异

问题场景：

- 即使隐藏层里形成了同样的分数 \(z\)，只要经过的激活函数不同，传给下一层的信号含义就会变掉

要确认的概念：

- sigmoid 会压缩到 0 与 1 之间
- tanh 会保留负方向与正方向
- ReLU 会把负信号切成 0，而把正向差异保留下来

输入（input）：

```python
# 这个例子把同一个线性分数 z 送入 sigmoid、tanh、ReLU，比较负信号和正信号如何变化。
import math

z_values = [-3.0, -1.0, 0.0, 0.5, 2.5]

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def relu(z):
    return max(0, z)

print("z | sigmoid | tanh | relu")
for z in z_values:
    print(
        f"{z:>4.1f} | "
        f"{sigmoid(z):>7.3f} | "
        f"{math.tanh(z):>5.3f} | "
        f"{relu(z):>4.1f}"
    )
```

看输出时，必须按“同一行横着读”。`z=-3.0` 那一行展示的是负信号会怎样被处理，`z=2.5` 那一行展示的是较大的正信号会怎样留下来。

```text
z | sigmoid | tanh | relu
-3.0 |   0.047 | -0.995 |  0.0
-1.0 |   0.269 | -0.762 |  0.0
 0.0 |   0.500 | 0.000 |  0.0
 0.5 |   0.622 | 0.462 |  0.5
 2.5 |   0.924 | 0.987 |  2.5
```

| 要比较的行 | 先看到的差异 | 现在该读出的含义 |
| --- | --- | --- |
| `z=-3.0` | sigmoid 会靠近 0，tanh 会靠近 -1，而 ReLU 直接变成 0。 | 对负信号来说，函数之间会决定它是被弱弱保留、连同符号一起保留，还是被完全切掉。 |
| `z=0.0` | 只有 sigmoid 是 0.5，而 tanh 与 ReLU 都是 0。 | 即使是同一个基准点，不同函数里的“中立值”含义也不一样。 |
| `z=2.5` | sigmoid 与 tanh 会被压近 1，而 ReLU 仍然保留 2.5。 | 它们区别在于：大正值差异是继续保留，还是被压进有限区间。 |

这个例子里，最直接可以改的是 `z_values`。如果再加入一个更大的正值，比如 `5.0`，就会发现 sigmoid 与 tanh 在 1 附近变化得更慢，而 ReLU 会继续把数值差异原样拉开。如果加入更小的负值，比如 `-5.0`，tanh 会进一步逼近 -1，而 ReLU 依然会把它切成 0。

| 现在就可以做的变化 | 更清楚出现的差异 | 不要只凭这个练习就仓促下结论的地方 |
| --- | --- | --- |
| 在 `z_values` 里加上 `5.0` | sigmoid/tanh 的饱和与 ReLU 正值直通之间的差异 | 不要据此就断定 ReLU 在大正值区间一定永远更好。 |
| 在 `z_values` 里加上 `-5.0` | tanh 保留负号与 ReLU 切掉负值之间的差异 | 不要据此就断定切掉负信号一定更安全。 |
| 把 `z_values` 缩成 `[-0.2, 0.0, 0.2]` | 三个函数在基准点附近到底动得多不多 | 不要只凭 0 附近的几个数就判断整个函数的全部性格。 |

整理答案时，必须把`输出范围`、`负输入处理`、`大正值处理`这三条轴先说清楚，而不是只报函数名字。只有能用这三条轴来解释，下一节才真正有条件去区分隐藏层激活与输出层激活。

## 检查清单

- 能否把 sigmoid、tanh、ReLU 的公式并排比较？
- 能否区分三个函数的输出范围？
- 能否说明：在大正值区间，sigmoid 与 tanh 会饱和，而 ReLU 会继续增长？
- 能否说明：面对负输入时，sigmoid、tanh、ReLU 的反应方式彼此不同？
- 能否把隐藏层激活的比较，与输出层选择问题区分开来？

## 出处与参考资料

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, `Deep learning`, Nature, 2015, 确认日期：2026-06-29. [https://www.nature.com/articles/nature14539](https://www.nature.com/articles/nature14539){: target="_blank" rel="noopener noreferrer" }
- Xavier Glorot, Antoine Bordes, Yoshua Bengio, `Deep Sparse Rectifier Neural Networks`, AISTATS, 2011, 确认日期: 2026-07-19. [https://proceedings.mlr.press/v15/glorot11a.html](https://proceedings.mlr.press/v15/glorot11a.html){: target="_blank" rel="noopener noreferrer" }
