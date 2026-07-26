# P5-9.2 batch 与 tensor 计算

> Section ID: `P5-9.2`
> Version: `v2026.07.26`

在 P5-9.1 里，我们已经看到：为什么深度学习会和 GPU、并行处理（parallel processing）特别合拍。接下来会马上冒出一个问题。

那么，GPU 擅长处理的深度学习计算，真正是以什么样的数据分组形式被交给模型的？

反复会出现的两个词，就是 batch 和 tensor。

batch 是为了把多个样本一起计算而做的分组，而 tensor 则是深度学习处理的多维数字数组的总称，这种分组也包含在里面。

如果之后需要再很短地复习一下 shape 和计算单元，更适合回到概念词汇表里的[批次（batch）](/AiBook/zh/reference/concept-glossary-pinyin/b/#batch)和[张量（tensor）](/AiBook/zh/reference/concept-glossary-pinyin/z/#tensor)。

## batch 与 tensor 怎样组织计算的问题

- 为什么需要 batch？
- tensor 是怎样从 vector 和 matrix 扩展出来的？
- 按 batch 计算和并行处理有什么关系？
- 为什么读 shape 的习惯这么重要？

这一节专注于抓住：`GPU 擅长处理的计算`，在真实深度学习里会以什么样的 batch 分组和 tensor shape 出现。也就是说，这里暂时不先追求 tensor 数学定义的严密性，而是先把`深度学习计算到底沿着什么样的数据形状在流动`关住。

与此同时，这一节也明确哪些问题不会立刻继续展开。`为什么 shape 重要`和`大矩阵计算怎样继续展开`这种感觉，会在后面的 P5-13.2 attention，以及 P5-14.3、P5-14.4 的 Transformer 计算结构里再重新接回。

## 并行单位与 shape 的判断标准

- 能把 batch 解释成`一次处理多个样本的计算单元`。
- 能把 tensor 解释成`包含 vector 和 matrix 在内的多维数组`。
- 能说明为什么读 shape 的习惯对深度学习实作很重要。
- 能通过可执行的 Python 例子确认 batch 和 tensor shape 的直觉。

## 为什么需要 batch

在深度学习里，同一个模型会被反复应用到很多样本上。虽然也可以把样本一个个顺序处理，但那样就很难把并行处理的优势吃满。

batch，就是把多个样本打包后一起计算的方式。

例如：

- 不只处理 1 张图片，而是一次处理 32 张
- 不只送进 1 句话，而是一次送进许多句子
- 表格数据也会把多行一起送进模型

先理解成下面这句话就够了。

`当模型必须把同一类运算重复施加到多个样本上时，batch 会把这些重复打包成一个整体来计算。`

## 使用 batch 之后，会变好在哪里

使用 batch 的原因并不只是方便。

- 可以更好利用 GPU 的并行计算
- 相比逐个样本处理，计算效率可能更高
- gradient 也会一次性反映多个样本的信息

当然，如果 batch 太大，也可能会消耗很多 memory，或者改变学习 dynamics。但在入门阶段，先把它读成`并行计算的基础单元`就够了。

## 什么是 tensor

在 Part 2 里，我们已经看过 scalar、vector、matrix。tensor 就是这条学习脉络很自然的延长。

用下面这张表说明就足够了。

| 名称 | 例子 | 维度数 |
| --- | --- | --- |
| scalar | `3.14` | 0 维 |
| vector | `[1, 2, 3]` | 1 维 |
| matrix | `[[1, 2], [3, 4]]` | 2 维 |
| tensor | 带上 batch 的图片/句子数组 | 包含 3 维及以上 |

也就是说，tensor 并不是什么神秘的特殊概念，而只是`多维数字数组`这个更宽的名字。

`在深度学习里，把输入、中间表示、输出全都看成 tensor 在流动，就已经足够。`

## 图片、句子、表格数据会长成什么样的 tensor

在深度学习里，即使数据种类不同，最后也都会被整理成 tensor shape。

例如：

- 表格数据：`(batch_size, feature_count)`
- 灰度图片：`(batch_size, height, width)`
- 彩色图片：`(batch_size, channel, height, width)`，当然不同 framework 里 channel 的位置也可能变化
- 句子 embedding：`(batch_size, sequence_length, embedding_dim)`

因此，tensor 可以跨越数据领域，扮演一种共同的计算语言。

## 为什么读 shape 的感觉这么重要

在实作里，最常见的错误之一，就是把 shape 读错，于是分不清`哪个轴是 batch`，`哪个轴是长度、channel、feature 维度`。

例如：

- 忘了 batch 维度
- 把行和列翻过来
- 把 channel 的位置看错
- 让 label shape 和输出 shape 对不上

这样一来，模型不是根本跑不起来，就是虽然能跑，却在做错误的计算。

所以需要固定下面这个习惯。

`在深度学习实作里，不要只看数值本身，要永远把 shape 一起看进去。`

## batch 计算和并行处理是怎样接上的

在 P5-9.1 里，我们已经看到：GPU 的强项是同时处理很多相似运算。batch 正是把这种结构，以适合深度学习的形式交给计算的一种方式。

也就是说：

- 模型保持同一组权重
- 面对 batch 里的多个样本
- 重复同样的 forward 和 backward 模式

而这些重复一旦被包进 batch dimension，就会很自然地接到并行计算上。

把它画成极其简化的形式，大致就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-09/batch-tensor-flow-zh.mmd"
```

## 案例与示例

### 案例. 用同一个 batch 轴去读表格、图片、句子

先同时想象三种输入：生产批次特征表、表面检测图片、维修日志 embedding。人一开始很容易觉得它们彼此完全不同，因为表是表、图是图、句子是句子。但在深度学习计算里，这三者首先都会被放进同一套框架里读：`batch 轴 + 它后面剩下的结构。` 也就是说，`(32, 20)` 代表的是`一次处理 32 个样本`的表格输入，`(32, 3, 224, 224)` 代表的是`一次处理 32 张图`的输入，而 `(16, 128, 768)` 则代表`一次处理 16 份文档`的输入。

人原本更习惯的标准，往往会是`表格先数有几行`、`图片先数有几张`、`句子先数有多长`。但只靠这种标准，很容易错过：模型到底是在同时处理什么。只要切到 shape 视角，首先必须固定的永远都是第一轴。第一轴代表的是`同时送进模型的一组样本`，也就是 batch 轴；而它后面剩下的轴，才再分别被读成 feature、channel 与空间、token 与 embedding。

因此，这个案例里首先要确认的是三件事。

- 第一轴是不是总能读成`同时处理的样本数`？
- 从 batch 里拿出一个样本之后，表格是否留下 feature 结构，图片是否留下 channel-空间结构，句子是否留下 token-embedding 结构？
- 只有把 shape 读成`轴的角色`而不是数字堆，实作错误才会真正减少吗？

先把这个案例固定住，下面比较表和 Python 例子里为什么会反复强调`第一轴`以及`取出一个 batch item 后剩下什么结构`，就会更自然地接上。

| 场景 | 人最容易先看到的结果 | shape 视角下真正需要区分的东西 | 接着立刻该确认什么 |
| --- | --- | --- | --- |
| 表格数据分类 | 容易把它看成是按行一条条读的数据 | 第一轴是同时计算的 batch 数，后面剩下的是 feature 轴 | 在 `(32, 20)` 里，试着分开说出 `32` 和 `20` 各自的角色 |
| 图片分类 | 容易只先数大概有几张图片 | 必须把 batch 轴、channel 轴、空间轴分开读，convolution 和 pooling 的含义才会对上 | 在 `(32, 3, 224, 224)` 里，逐个说出各轴是什么 |
| 句子模型 | 容易觉得只看句子长度就够了 | 必须同时读 batch 轴、token 轴、embedding 轴，attention 和 sequence 计算才接得上 | 在 `(batch, sequence_length, embedding_dim)` 里，分开说出每个轴的角色 |

把这三类输入按 shape 标准并排放在一起，大致就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-09/batch-shape-modality-compare-zh.mmd"
```

这张比较图里首先要固定住的点如下。

- 三种情况里，第一轴都代表`同时处理的一组样本`，也就是 batch 轴。
- 变化的是第一轴后面剩下的结构：表格保留 feature 轴，图片保留 channel 和空间轴，句子保留 token 和 embedding 轴。
- 所以在读 shape 时，如果想减少实作错误，必须先区分的不是数字有几个，而是`第一轴后面到底剩下什么。`

## 练习与例子

这个例子的目标，是直接确认：生产批次表格数据、表面检测图片 tensor、维修日志 embedding 三种输入，都把同样的`第一轴`读成 batch 轴。

输入：

- 生产批次特征表
- 类似表面检测图片的 4 维 tensor
- 类似维修日志 embedding 的 3 维 tensor

输出：

- 各 tensor 的 shape
- 第一轴所表示的 batch 数
- 取出一个 batch item 后剩下的结构
- 如果轴被读错，会出现什么误解的比较

问题场景：

- 表格、图片、句子 embedding 虽然都能以 tensor 处理，但它们各轴的意义并不相同
- 如果只把 shape 当成数字堆，就很容易把第一轴和剩余轴的角色混在一起

要确认的概念：

- 解释 tensor 时，不该从值本身开始，而是应该先读 `shape` 和轴的意义
- 只要看取出一个 batch item 后剩下什么结构，各轴角色就会更容易分清
- 一旦轴读错，就可能把`batch 数`、`channel 数`、`token 数`彼此混着理解

从初学者角度，这个例子最适合按下面三个步骤来读。

| 阅读步骤 | 先看什么 | 接着马上要抓住的问题 |
| --- | --- | --- |
| 1 | 每个 tensor 的 `shape[0]` | 第一轴真的会被读成 batch 数吗？ |
| 2 | 取出一个 batch item 后剩下的 `shape` | 表格、图片、句子在第一轴后面留下的结构到底怎样不同？ |
| 3 | `[wrong reading check]` | 哪怕数字一样，如果把 batch 轴、channel 轴、token 轴的角色互换，会出现什么误解？ |

输入（input）：

我们使用上面整理好的生产批次特征表、表面检测图片 tensor，以及维修日志 embedding 形式的 tensor。

在看代码之前，可以先预测：每个 tensor 里的`第一轴`到底代表什么，以及拿掉一个 batch item 之后，剩下的轴又各自意味着什么。

| tensor | 可以先预测的比较 | 预测理由 |
| --- | --- | --- |
| `tabular_batch` | 第一轴很可能是生产 batch 数，而拿掉一个样本后会留下 feature vector | 因为表格数据通常按 `(batch, feature)` 结构来读 |
| `image_batch` | 第一轴很可能是图片数，而拿掉一个样本后会留下 `(channel, height, width)` | 因为图片在 batch 外，还会保留 channel 和空间轴 |
| `text_batch` | 第一轴很可能是维修日志文档数，而拿掉一个样本后会留下 `(sequence_length, embedding_dim)` | 因为句子 tensor 会同时保留 token 轴和 embedding 轴 |

这里真正要确认的差异，也不会停在背 shape 上。如果没办法把`第一轴`正确读成 batch 数，就会把图片数和 channel 数混着数，或者把文档数和 token 长度混在一起。也就是说，这一节真正的核心不是猜数字，而是把`一次喂给模型多少样本`和`单个样本内部还剩下什么结构`连回到实作判断里。

这张表的目的，就是把`第一轴是什么`和`拿掉一个 batch item 后还剩下什么`分开来读。

```python
# 这个例子检查表格、图像、文本张量的第一轴是 batch，并观察取出一个样本后还剩哪些轴。
import numpy as np

tabular_batch = np.array([
    [12, 180, 1],
    [4, 95, 0],
    [9, 140, 1],
])

# (batch, channel, height, width)
image_batch = np.arange(2 * 3 * 2 * 2).reshape(2, 3, 2, 2)

# (batch, sequence_length, embedding_dim)
text_batch = np.arange(2 * 4 * 3).reshape(2, 4, 3)

print("tabular_batch shape =", tabular_batch.shape)
print("number of production batches =", tabular_batch.shape[0])
print("one batch feature row =", tabular_batch[0].tolist())
print()

print("image_batch shape =", image_batch.shape)
print("number of images =", image_batch.shape[0])
print("first image shape =", image_batch[0].shape)
print("first image, first channel =")
print(image_batch[0, 0])
print()

print("text_batch shape =", text_batch.shape)
print("number of maintenance logs =", text_batch.shape[0])
print("first log embedding shape =", text_batch[0].shape)
print("first token embedding =", text_batch[0, 0].tolist())
print()

print("[wrong reading check]")
print("if image_batch.shape[1] is read as number of images ->", image_batch.shape[1])
print("actual number of images ->", image_batch.shape[0])
print("if text_batch.shape[1] is read as number of logs ->", text_batch.shape[1])
print("actual number of logs ->", text_batch.shape[0])
```

读输出时，先看每个 batch 的 shape，以及第一个样本在不同数据类型里留下了什么结构。

```text
tabular_batch shape = (3, 3)
number of production batches = 3
one batch feature row = [12, 180, 1]

image_batch shape = (2, 3, 2, 2)
number of images = 2
first image shape = (3, 2, 2)
first image, first channel =
[[0 1]
 [2 3]]

text_batch shape = (2, 4, 3)
number of maintenance logs = 2
first log embedding shape = (4, 3)
first token embedding = [0, 1, 2]

[wrong reading check]
if image_batch.shape[1] is read as number of images -> 3
actual number of images -> 2
if text_batch.shape[1] is read as number of logs -> 4
actual number of logs -> 2
```

- 三种情况里，第一轴都表示`同时处理的 batch 数`
- 拿出一个 batch item 后，表格留下 feature row，图片留下 channel-空间结构，句子留下 token-embedding 结构
- 读 shape 并不是只数里面有几个数字，而是解释每个轴各自代表什么

| tensor | 现在要读的核心 |
| --- | --- |
| `tabular_batch` | 把第一轴读成生产 batch 数，拿出一个 batch item 后会留下 feature vector。 |
| `image_batch` | 第一轴是图片数，第二轴 `3` 不是图片数，而是 channel 数。 |
| `text_batch` | 第一轴是维修日志数，第二轴 `4` 不是日志数，而是 token 长度。 |

读输出数字时，也要把`数组大小`和`轴的意义`分开来看。

| 比较 | 输出里首先看到的 | 只看数字时容易留下的解读 | 加上 shape 视角后会改变的解读 |
| --- | --- | --- | --- |
| `tabular_batch shape = (3, 3)` | 两个数字相同，所以看起来像扮演同样角色。 | 容易觉得两个都是 `3`，没有太大区别。 | 前面的 `3` 是生产 batch 数，后面的 `3` 是每个 batch item 的 feature 数，角色完全不同。 |
| `image_batch shape = (2, 3, 2, 2)` | `3` 很显眼，容易被误认为图片数。 | 容易把第二轴也当成另一种样本数。 | 实际图片数是第一轴 `2`，第二轴 `3` 是 channel 数；如果交换轴的读法，计算意义就会错。 |
| `text_batch shape = (2, 4, 3)` | `4` 看起来较大，容易被误认为文档数。 | 容易把中间数字当成日志数量读过去。 | 第一轴 `2` 是日志数，`4` 是 token 长度，`3` 是 embedding 维度，这会成为后面 attention 输入解读的基准。 |

| 实作判断标准 | 轴读错时容易出现的误解 | 加上 shape 视角后会改变的判断 |
| --- | --- | --- |
| 表格数据输入设置 | `(3, 3)` 时容易觉得任意交换轴也差不多。 | 第一轴是 batch 数，所以如果 feature 轴放错，首先就会错判一个 step 里进入多少样本。 |
| 图片模型输入检查 | 容易把 `3` 读成图片数，把 batch 误解成 3 张图。 | 真实 batch 是 2 张图，`3` 是 channel 数；如果把 batch 轴和 channel 轴换着放，convolution 的解释本身就会错。 |
| 文本模型输入检查 | 容易把 `4` 读成日志数，以为一次喂入 4 篇文档。 | 实际是喂入 2 篇文档，每篇被切成 4 个 token，所以检查 padding 和 attention 输入时必须分清 token 轴和 batch 轴。 |

也就是说，shape 解读中读者首先要抓住的问题，不是`一共有几个数字`，而是`这个轴是样本数、channel，还是长度`。

如果把这个结果再翻回实作场景，读 shape 更稳的人，不会只问`模型为什么跑不起来`，而会更早先问：`我是不是把 batch 轴、channel 轴、token 轴的角色读混了？` 反过来，如果只把 shape 看成数字堆，就更容易不断重犯同一类错误，却很晚才发现真正的问题是输入定义本身。

batch 和 tensor 这两个表达，也不只是某个库的语法。随着深度学习逐渐稳定成一种大规模并行数值计算体系，把数据读成`单个样本`之外、同时也读成`整批 grouped tensor`的直觉，也一起变成了事实上的标准。

因为下面这些东西，会在这里被合并成一种共同的 shape 语言。

- Part 2 的线性代数和 NumPy 数组
- Part 3 的输入矩阵和 feature table
- P5-9.1 的 GPU 并行处理

也就是说，tensor 更适合被看成：把前面已经学过的数组直觉继续扩展到深度学习规模之后得到的结果，而不是一个突然冒出来的全新困难概念。

在这里先停一下，把`什么时候该比数据种类更早从 shape 和 batch 视角来读`这条判断基准固定住，后面再过渡到 attention 和 Transformer 计算时，基线就会更稳。

| 先冒出的提问 | 为什么此时更需要 batch / tensor 视角 | 后面章节会从这里继续的东西 |
| --- | --- | --- |
| 为什么输入跑不起来，或者为什么会算出完全不对的东西？ | 因为在看数值之前，轴的意义和 shape 是否匹配必须先对上 | attention 里 query、key、value 的 shape 阅读 |
| 为什么表格、图片、句子最后都能看成同一种计算语言？ | 因为即使数据类型不同，只要被放进 tensor 和 batch 维度里，就会露出共同计算结构 | Transformer 的大矩阵计算 |
| 为什么要一次处理多个样本？ | 因为 batch 维度会直接让并行计算和 gradient 汇总变得可能 | 长序列和大 batch 带来的计算负担 |

## 检查清单

- 能说明 batch 和 tensor 在深度学习计算中是什么基本单位吗？
- 能说明一次处理多个样本的结构怎样和 GPU 计算连接吗？
- 能把 batch 解释成一次处理多个样本的计算单元吗？
- 能说出 tensor 是深度学习处理的多维数字数组的总称吗？
- 能不把 batch 说成`为了看起来方便而收集的多个样本`，而是说成`把同一计算同时送到多个样本上的单位`吗？
- 看到 `(batch_size, sequence_length, embedding_dim)` 这样的 shape 时，能实际分开读出轴名称吗？
- 读 shape 时，能先确认当前轴是 batch、length 还是 channel，并检查输入和输出是否符合预期结构吗？
- 能不只按各自不同的直觉看表格、图片、句子数据，而是用 tensor 和 shape 这种共同计算语言重新说明它们吗？

## 出处与参考资料

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29。 [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Aurélien Géron, `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`, 3rd ed., O'Reilly, 2022, 确认日期：2026-06-29。
- NumPy Developers, `ndarray`, NumPy Documentation, 确认日期：2026-06-29。 [https://numpy.org/doc/stable/reference/arrays.ndarray.html](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }
