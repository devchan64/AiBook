# P5-11.2 卷积（convolution）与池化（pooling）

Section ID: `P5-11.2`
Version: `v2026.07.17`

在 P5-11.1 里，我们已经把 CNN 解释成`会反复读取图像局部模式的神经网络`。接下来还会自然留下一个问题。

真正负责计算这些局部模式的核心运算是什么？为什么池化（pooling）又总是和它一起出现？

卷积（convolution）是用小滤波器计算局部模式分数的运算，而池化（pooling）则是把这些结果整理成更小、更摘要形式的运算。

如果这些运算名称又开始混在一起，更适合重新回到英文概念词汇表里的[convolution](/AiBook/en/reference/concept-glossary/#convolution)和[pooling](/AiBook/en/reference/concept-glossary/#pooling)条目对齐。

## 本节范围

- convolution 到底在计算什么？
- filter 和 feature map 到底是什么意思？
- pooling 为什么会被使用，它又是在减少什么？
- 当这两个运算一起出现时，CNN 的表征流程应该怎样读取？

这一节不会先去严格证明 convolution 的公式，而是先把`CNN 怎样给局部模式打分，又怎样把这些响应做成摘要`这条流程关住。

同时，这一节也会明确哪些问题不会立刻继续展开。CNN 之后更广的 vision 结构比较，会在补充学习 P5-11.3 里回收到`CNN 和 Vision Transformer（ViT）`这个角度。padding、stride、dilation 则只在理解`滤波器怎样读取输入`所必需的范围内处理。

## 本节目标

- 能把 convolution 解释成`小滤波器计算局部模式分数的运算`。
- 能把 feature map 解释成`滤波器响应的空间记录`。
- 能说明 pooling 为什么会被用来缩小空间尺寸，并汇总重要响应。
- 能通过可执行的 Python 例子确认 convolution 与 max pooling 的直觉。

## 阅读这一节的顺序

1. 先看 convolution 怎样计算局部模式分数。
2. 再看这些结果会怎样留下成一张叫作 feature map 的响应图。
3. 然后看 pooling 怎样把这些响应以更小、更摘要的形式继续传下去。
4. 再把 convolution 和 pooling 怎样接成一条流程整理起来。
5. 最后再看 `padding`、`stride`、`dilation` 会怎样改变这条流程的读取方式。

## convolution 做了什么

卷积（convolution）会把一个小滤波器（filter）移动到图像的许多位置上，并给每个位置和某种模式的匹配程度打分。

真正的核心是：滤波器会带着自己想找的小模式，在图像上扫过去，并为每个位置生成响应分数。

- 滤波器可以被看成`想找的小模式模板`
- 它会和图像的每个局部 patch 做乘法与加法
- 然后生成该位置的响应分数

也就是说，convolution 不是一次性判断整张图像，而是把`小模式探测器`反复应用到所有位置上的一种方式。

## filter 到底是什么意思

filter 通常是一个很小的数字数组。例如一个 3x3 filter，就可以读取一个 3x3 的局部 patch。

`filter 是一小组会被学成对 edge、方向、纹理、小形状等模式产生反应的权重。`

当 CNN 被训练时，这些 filter 的数值也会随着数据一起变化。也就是说，不是由人把每一个 filter 都事先写好，而是模型也会一起学出：哪些 filter 更有用。

## 什么是 feature map

如果把同一个 filter 应用于整张图像，就会得到一个新的二维数组，里面记录着这个 filter 在每个位置上反应有多强。这就叫 feature map。

也就是说：

- 在输入图像上
- 把 filter 应用到每一个位置
- 然后把这些响应值记录下来

最后得到的就是 feature map。

关键点是：feature map 是一张结果图，它按位置记录了某一个特定 filter 在图像里的什么地方、以多强的强度作出了反应。

`feature map 是一张地图（map），记录某个特定 filter 在图像的哪里、以多强的强度作出了反应。`

这里最好顺手把下面这个区分也固定下来。

| 名称 | 它的意思 |
| --- | --- |
| filter | 想找的小模式模板 |
| convolution result | 在每个位置上算出的模式分数 |
| feature map | 把这些分数按位置整理起来得到的结果图 |

## 为什么需要 pooling

如果把 convolution 的结果原封不动地一直往后堆，空间尺寸会一直很大，计算量也会继续变大。并且，把每一处细微位置的信息都一模一样地带到最后，也并不总是最好的做法。

pooling 的作用，就是把这些信息整理成更摘要的形式。

例如 max pooling 会在一个小区域里只保留最大的响应值。

`pooling 会减少一部分细节位置的信息，但会把重要的响应以更压缩的方式传给下一层。`

## 为什么 max pooling 很直观

max pooling 会在一个小窗口里选出最大的那个值。这会给读者带来下面的直觉。

- 它保留这个区域里最强的模式响应
- 它可能对小的位置变化没那么敏感
- 它会通过缩小空间尺寸来压缩计算

也就是说，max pooling 最适合被读成：`保留最显眼信号的一种摘要方式。`

如果把这种差异压得更短一点，就是下面这样。

| 阶段 | 主要在做什么 |
| --- | --- |
| convolution | 找模式 |
| pooling | 汇总已经找到的响应 |

把同一个图像场景拆成这两个阶段后，差异会更直接。

| 同一场景 | convolution 先做什么 | pooling 紧接着做什么 |
| --- | --- | --- |
| 白底上的黑线 | 给边界反应强的位置打分 | 在那个区域里只保留最强的边界响应，并以更小的形式传下去 |
| 混合罐上方管道附近 | 先对阀门轮廓、管道边界、警示灯反光这类小结构产生反应 | 把强响应压缩起来，让下一层更容易读取更大的设备部件 |
| 表面缺陷图像 | 在小划痕或裂纹所在的位置提高响应 | 汇总缺陷候选信号，让它们更容易被保留到缺陷判断里 |

## convolution 和 pooling 放在一起时该怎样读取

如果把它们非常简单地连起来，大致会是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-11/convolution-pooling-flow-zh.mmd"
```

这张图展示的是 `找到 -> 记录 -> 汇总` 这三个动作。

1. convolution 会先找出一个局部模式。
2. feature map 会把这个响应按位置记录下来。
3. pooling 则把这份记录以更小、更摘要的形式继续传下去。

把一个实际检测场景和数字数组并排放在一起时，这条流程会更容易读。下面的例子，是把`在封口边缘，左右列分布差异突然变大的小检测 patch`做了简化。

| 场景 | 数值表示 |
| --- | --- |
| 小的检测 patch | 左侧是较高的列分布，右侧是较低的列分布，两者在 4x4 封口 patch 里相遇 |
| 输入矩阵样例 | `[[3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1]]` |

现在可以想象：在这个输入上放一个`会对左右列差异产生反应的 2x2 filter`。

| 项目 | 值 |
| --- | --- |
| filter | `[[1, -1], [1, -1]]` |
| 读取方式 | 比较左列和右列的差异，从而找到封口边界的变化 |

如果让这个 filter 一格一格地移动并计算，就会得到下面这样的 `feature map`。

| 阶段 | 矩阵样例 |
| --- | --- |
| input image | `[[3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1]]` |
| convolution result | `[[0, 4, 0], [0, 4, 0], [0, 4, 0]]` |
| 2x2 max pooling result | `[[4]]` |

如果把这同一组变换拆成一步一步来看，可以按下面这样读取。

![convolution 输入封口 patch](/AiBook/assets/part-05/chapter-11/convolution-pooling-input-zh.png)

输入 patch 仍然更接近人眼看到的那个小列分布场景。左边是高值，右边是低值，它们被放在一起，但在这个阶段，`边界在哪里`还没有被单独分成分数。

![convolution feature map](/AiBook/assets/part-05/chapter-11/convolution-pooling-feature-map-zh.png)

经过 convolution 之后，它会变成一张响应图，表示各个位置和 filter 的匹配程度有多高。这里，只有在左右列差异真正出现的中间位置上，数值 `4` 才会重复出现，这意味着输入场景已经被改写成了`边界响应的位置图`。

![max pooling 汇总结果](/AiBook/assets/part-05/chapter-11/convolution-pooling-max-pool-zh.png)

max pooling 不会把整张响应图原样传下去，而只会在这个小区域里保留最强的响应。这个阶段真正发生的变化是：和细节位置相比，`这个区域里存在很强的封口边界变化`这样一个摘要信号，会被传给下一层。

读取这些数字时，要抓住的重点如下。

- `0` 表示：在这个位置，filter 期待的左右差异几乎不存在
- `4` 表示：filter 想找的列分布边界在这里被强烈捕捉到了
- max pooling 之后的 `[[4]]` 表示：即使具体位置被压缩了，`这里有一个边界变化很强的区域`这个要点仍然被保留下来

也就是说，这个小检测 patch 会帮助读者继续抓住原本的人类场景，而矩阵样例则展示 convolution 和 pooling 实际上会制造出怎样的数值摘要。

这条流程展示了：CNN 会

- 先找到一个模式
- 再把这个响应记录下来
- 然后把它以更压缩的形式交给下一层

也就是说，`convolution 给局部模式打分，而 pooling 则把这些分数变成更容易被下一层读取的更小形式继续传下去。`

在转到下一节的 ViT 比较之前，如果再把 CNN 实际拿什么作为计算单位这件事固定一次，可以看成下面这样。

```mermaid
--8<-- "assets/part-05/chapter-11/cnn-local-window-baseline-zh.mmd"
```

这张基线图里，首先要抓住的是下面几点。

- CNN 的第一个计算单位不是整张图像，而是`会带着重叠去移动的小 local window`
- 每个 window 先制造出来的，是一个局部响应分数，回答`这个位置和 filter 模式有多匹配`
- 所以当后面再去看 ViT 的 patch token 时，就能在同一个输入上比较`扫过许多小窗口的方式`和`读取已经切开的 patch 的方式`

如果只把 CNN 读成 Part 5 之前、或 Transformer 之前出现过的一种旧结构，它就很容易看起来像`一个用于图像的旧模型名称`。但在 Part 5 里，CNN 的责任其实在这里就已经关住了。也就是说，CNN 本身就对`在图像里怎样探测并汇总局部模式`给出了一套答案。后面的 Part 只要继续处理不同的数据结构问题，而不是去“替换”这套答案，就已经足够了。

## padding、stride、dilation 到底是什么意思

虽然这一节的中心是 convolution 和 pooling，但对上面刚出现过的 `padding`、`stride`、`dilation`，这里仍然最好先固定住最小限度的意义。

这三个术语都在调整：`filter 会怎样扫过输入。`

| 术语 | 它改变什么 | 入门直觉 |
| --- | --- | --- |
| padding | 在输入边缘外额外加上一圈数值 | 让边缘更不容易被漏掉，也防止输出尺寸缩得太快 |
| stride | 决定 filter 每次跳多少格 | 决定是一格一格密集地看，还是两格两格地跳着看 |
| dilation | 拉开 filter 单元之间的间隔 | 不增大 filter 本身的尺寸，也能看到更宽的范围 |

三者的差异可以先记成下面这样。

- `padding` 是在边缘外面再加一圈留白的选择
- `stride` 是决定 filter 移动步长的选择
- `dilation` 是拉开 filter 内部单元间距的选择

如果把它们压缩成三种读取同一输入的方式，会是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-11/filter-reading-options-zh.mmd"
```

这张图里首先要确认的结果是：三者改变的不是`filter 想找什么`，而是`它怎样扫过输入`。

这一节不会把三个术语展开成公式，但在后面阅读 convolution 说明时，只要先把它们抓成：用来调整`filter 的内容`、`filter 的移动方式`、`filter 会覆盖多宽范围`的装置就够了。下面的小场景会直接展示这种差异。

先想象我们在读取同一条一维序列。

```text
input = [A B C D E]
filter size = 3
```

这时，这三个术语分别在回答不同的问题。

- padding: `要不要在两端加留白？`
- stride: `每次要移动几格？`
- dilation: `filter 的单元是紧挨着读，还是隔着一些格再读？`

也就是说，这三者改变的不是 convolution 本身，而是`怎样扫过去`的方式。

### 为什么需要 padding

如果没有 padding，filter 就不能越出输入边缘，所以靠近边界的信息会比较容易被读得更少。

例如，若把一个 3x3 filter 直接在 5x5 图像上移动，filter 的中心就只能比较稳定地停留在内部，而不是外边框上。这样一来，边缘附近的小线条或角点就可能较少被反映出来。

padding 的做法，就是在外面再补一圈留白。

- 没有留白时，计算会在边界立刻结束
- 有了留白时，靠近边界的位置也会多一次被读取的机会

也就是说，padding 会给边界附近再增加一次读取机会，避免边缘信息过快消失。

如果用一条很短的序列来写，大致会是这样。

```text
没有 padding: [A B C] [B C D] [C D E]
有 padding:   [0 A B] [A B C] [B C D] [C D E] [D E 0]
```

这里真正的核心就是：`边界也获得了参与计算的机会。`

### stride 改变了什么

stride 会决定 filter 每次移动多少格。

把它看得非常简单一点：

- stride 为 1 时，会`一格一格`地移动，读取得更密
- stride 为 2 时，会`两格两格`地跳，读取得更疏

例如，如果一个宽度为 2 的 filter 正在读取一条长度为 4 的序列：

- stride 1 时，会像 `[1-2]`、`[2-3]`、`[3-4]` 这样带着重叠去读
- stride 2 时，则会像 `[1-2]`、`[3-4]` 这样跳得更大

也就是说，stride 是决定`要扫得多密`的那个选择。stride 越大，输出尺寸会缩得越快，计算也会被更粗地做成摘要。

把这件事重新翻回图像里，可以这样理解。

- stride 1：几乎不跳过位置地去看
- stride 2：不再一格一格地看，而是更稀疏地扫过去

也就是说，当 stride 变大时，`输出会更快缩小，但细微的位置差异也会看得更少。`

### 为什么 dilation 要单独叫一个名字

dilation 会拉开 filter 单元之间的间距，从而在不把 filter 本身做大的情况下，也能看到更宽的范围。

例如，如果把一个 3 单元的 filter 正常放上去，它会读取彼此紧邻的位置。但如果加上 dilation，它就可以把更远的位置一起读进来，例如`第一格`、`跳过一格后的那一格`、`再跳过一格后的那一格`。

也就是说，dilation 是：

- 不大幅增加参数数量的前提下
- 想要看到更宽的 receptive field 时
- 通过拉开 filter 内部间距来实现的选择

所以 dilation 可以被理解成：在不明显增加参数数量的情况下，通过拉开 filter 内部间距，去看到更宽 receptive field 的选择。

如果用一维序列去看，这个差异会更简单。

```text
没有 dilation: [A B C]
有 dilation:    会一起读取像 [A _ C _ E] 这样彼此隔开的几个位置
```

也就是说，filter 的单元数量本身不变，只是`一次看到的范围`变宽了。

再把三个术语压成一行，就是下面这样。

| 术语 | 面向入门者的一句话 |
| --- | --- |
| padding | 在边界外加留白，让边缘信息不要过快消失 |
| stride | 决定 filter 是一格一格看，还是更大步地跳着看 |
| dilation | 拉开 filter 单元间距，让它能一起看到更宽范围 |

在入门阶段，只要再用下面这些问题回头确认一次，就足够了。

- padding: `要不要让边界也被多读一次？`
- stride: `要不要扫得更密，还是跳得更大？`
- dilation: `要不要在不增大 filter 的情况下看到更宽范围？`

### 如果把三种差异放进一个很小的数字例子里一起看

如果只用文字去讲，这三个术语很容易显得彼此相似，所以不如把它们重新放进：同一个 3x3 filter 去读取一个很小的 5x5 输入这个场景里。

```text
input
1 0 0 0 1
0 1 0 1 0
0 0 1 0 0
0 1 0 1 0
1 0 0 0 1

filter
1 0 1
0 1 0
1 0 1
```

在这里，读者首先要看的不是 `filter 的数值` 本身，而是`它一次会把哪些位置绑在一起读取。`

| 设置 | filter 实际读取场景会发生什么变化 | 最先出现的差异 |
| --- | --- | --- |
| padding 0, stride 1, dilation 1 | 只会密集地读取输入内部 | 边缘被读取的机会更少，输出会变成 3x3 |
| padding 1, stride 1, dilation 1 | 会在外面补一圈 0 留白后再读 | 边缘也会多被读一次，输出保持为 5x5 |
| padding 0, stride 2, dilation 1 | 会两格两格地跳着读 | 读取位置数量变少，所以输出更小 |
| padding 0, stride 1, dilation 2 | 会拉开 filter 单元间距，用更宽范围去读 | 即使还是同一个 3x3 filter，也会一次覆盖更大的范围 |

也就是说，这三个设置改变的都不是`filter 在找什么`，而是`filter 会用什么间隔、在多大范围内移动`。

### 先看设置差异的小例子

这个小例子的目标，是用眼睛直接确认 `padding`、`stride`、`dilation` 会怎样改变输出尺寸，以及 filter 实际读取的范围。重点不是背下全部 convolution 数值，而是抓住：`即使 filter 一样，只要扫描方式不同，输出形状和读取 patch 也会一起改变。`

在读代码之前，如果先按顺序看下面三个值，这一节的结构差异会更不容易散掉。

| 先看的值 | 为什么要先看它 |
| --- | --- |
| `shape` | 因为一改设置，输出尺寸先怎样变化会最直观地先出现 |
| `first_patch` | 因为能直接比较 filter 在第一个位置到底读取了多大的范围 |
| `result` | 因为最后可以把前面两种差异怎样改变整张响应图一起收回来 |

输入：

- 一个 5x5 的封口检测 patch
- 一个 3x3 filter
- 不同的 `padding`、`stride`、`dilation` 设置

输出：

- 每种设置对应的输出矩阵 shape
- 第一个位置实际读取到的 patch
- 每种设置对应的 convolution 结果

问题场景：

- `padding`、`stride`、`dilation` 这些名字听起来相似，但它们会让 filter 以不同方式读取图像范围

要确认的概念：

- convolution 的设置会同时改变结果 shape 与实际读取 patch 的范围
- 把第一位置的 patch 和最终结果一起看，各设置之间的差异会更明显

输入（input）：

这里使用上面整理好的输入图像、filter，以及几组 `padding`、`stride`、`dilation` 设置。

```python
import numpy as np

image = np.array([
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1],
], dtype=float)

kernel = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
], dtype=float)

def conv2d(image, kernel, padding=0, stride=1, dilation=1):
    padded = np.pad(image, padding, mode="constant", constant_values=0)
    kernel_h, kernel_w = kernel.shape
    effective_h = kernel_h + (kernel_h - 1) * (dilation - 1)
    effective_w = kernel_w + (kernel_w - 1) * (dilation - 1)
    out_h = ((padded.shape[0] - effective_h) // stride) + 1
    out_w = ((padded.shape[1] - effective_w) // stride) + 1
    output = np.zeros((out_h, out_w))

    first_patch = None
    for out_i in range(out_h):
        for out_j in range(out_w):
            row = out_i * stride
            col = out_j * stride
            sampled = padded[
                row:row + effective_h:dilation,
                col:col + effective_w:dilation,
            ]
            if first_patch is None:
                first_patch = sampled.copy()
            output[out_i, out_j] = np.sum(sampled * kernel)

    return output, first_patch

settings = [
    ("base", 0, 1, 1),
    ("padding=1", 1, 1, 1),
    ("stride=2", 0, 2, 1),
    ("dilation=2", 0, 1, 2),
]

for name, padding, stride, dilation in settings:
    result, first_patch = conv2d(
        image=image,
        kernel=kernel,
        padding=padding,
        stride=stride,
        dilation=dilation,
    )
    print(f"[{name}]")
    print("shape =", result.shape)
    print("first_patch =")
    print(first_patch)
    print("result =")
    print(result)
```

在输出里，只要按顺序看 result 的 shape、第一块 patch，以及最终 result 数值是怎样连起来的，就够了。

```text
[base]
shape = (3, 3)
first_patch =
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
result =
[[3. 0. 3.]
 [0. 5. 0.]
 [3. 0. 3.]]
[padding=1]
shape = (5, 5)
first_patch =
[[0. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
result =
[[2. 0. 2. 0. 2.]
 [0. 3. 0. 3. 0.]
 [2. 0. 5. 0. 2.]
 [0. 3. 0. 3. 0.]
 [2. 0. 2. 0. 2.]]
[stride=2]
shape = (2, 2)
first_patch =
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
result =
[[3. 3.]
 [3. 3.]]
[dilation=2]
shape = (1, 1)
first_patch =
[[1. 0. 1.]
 [0. 1. 0.]
 [1. 0. 1.]]
result =
[[5.]]
```

这组结果里，首先要读出的重点如下。

- `padding=1` 会把输出保持在 5x5，同时让边缘也留在计算范围里
- `stride=2` 会让 filter 两格两格地跳，所以输出很快缩成 2x2
- `dilation=2` 会让一个 3x3 filter 实际上稀疏地读取一个更宽的 5x5 范围

也就是说，这三个术语并不是把 convolution 变成了`另一种运算`，而是一些选择，用来改变`同一个 convolution 会以什么范围、什么步距去读取输入`。

## 案例与示例

### 代表案例. edge detection 的直觉

想象一张白底上穿过一条黑线的图像。人看到这种场景时，首先会想找的是`线到底在哪里`。但如果计算机只拿到原始像素数字，它很难马上判断：哪些数值变化代表一条线，哪些又只是噪声。例如，哪怕这条线只平移了一个像素，原始数字数组看上去也可能完全不同。filter 恰好就可以被设计成：在亮度变化大的位置上产生更强的反应。于是，feature map 里有线或有边界的位置就会变成更大的数值，模型也就开始用数字去读`结构到底在哪里`。

所以，这个案例里要确认的结果是：与其一次性盯着所有原始像素值，不如看边界所在的位置是否真的会先在 convolution 响应里变大，并成为下一阶段判断的出发点。

同样的视角也会自然延伸到设备场景图像、医疗视觉或工业视觉。不过这一节真正要抓住的重点，不是领域名称，而是：`convolution 会先在什么地方制造较大的局部响应，pooling 又怎样把那个响应保留到下一阶段。`

把三个案例放在一起看，就更容易明白：convolution 和 pooling 不该只被读成`两个运算的名字`，而更应该被读成`一条同时区分“在哪里生成响应”与“什么被留下来”的流程`。

把这三个案例重新收成一行，大致如下。

| 情况 | 为什么 convolution 重要 | 为什么 pooling 重要 |
| --- | --- | --- |
| edge detection | 因为要给亮度变化出现的位置打分 | 因为要把强的 edge 响应汇总起来 |
| 设备场景图像 | 因为要找到阀门、管道、警示灯边界这类局部结构 | 因为要把局部响应压缩后继续传给下一层 |
| 医疗/工业视觉 | 因为要找到细小缺陷或边界 | 因为要把重要的异常信号以更小的形式摘要下来 |

| 人最容易先看的标准 | 用 convolution·pooling 视角重读的标准 |
| --- | --- |
| 只要图像整体印象相似，内部计算大概也会相似 | 哪怕只有一个局部边界不一样，convolution 响应和 pooling 结果也可能强烈分开 |
| 容易觉得 pooling 只是把信息扔掉的阶段 | 真正关键的是：它不保留所有值，但会让强响应一路活到下一阶段判断 |
| 容易把 filter、feature map、pooling 这些名字拆开背 | 实际上它们必须连成一条流程：`在哪里生成响应`、`在哪里记录响应`、`最后什么被留下来` |

## 练习与例子

这个例子的目标，是在包装封口（seal）表面的自动检测场景里，确认 convolution 怎样先给`异常边界出现在什么地方`打分，而 pooling 又怎样显示：`这个异常信号是否能活到下一阶段`。

在读代码之前，这个例子里真正要看的三个值如下。

| 先看的值 | 为什么要先看它 |
| --- | --- |
| `normal_conv`, `weak_conv` | 因为可以直接比较正常封口和弱封口在什么位置的响应分开了 |
| `normal_pool`, `weak_pool` | 因为可以检查 pooling 是否会把大响应保留下来，而不是把它抹掉 |
| `weak seal max response` | 因为从操作角度看，更重要的是一个局部异常会多强地活下来，而不是整体平均值 |

输入：

- 一个把正常封口热分布简化后的 5x5 扫描矩阵
- 一个封口局部变弱、边界突然不稳定的 5x5 扫描矩阵
- 一个会对左右变化作出反应的 2x2 filter

输出：

- 正常封口和弱封口的 convolution 结果
- 正常封口和弱封口的 max pooling 结果
- 最大异常响应最后留下的位置与大小

问题场景：

- 在生产线自动检测里，比起整张图像的平均值，一个很小的边界异常更可能成为复检或产线点检的起点

要确认的概念：

- convolution 会制造按位置排列的局部响应，并先揭示`哪里不正常`
- max pooling 即使会压缩局部响应，也仍可能把最大的异常信号保留下来
- 只有把正常场景和异常场景并排比较，`到底变了什么`才会更清楚

在看代码之前，可以先预测正常封口与弱封口会先从哪些值开始分开。

| 比较点 | 正常封口里先预测到的结果 | 弱封口里先预测到的结果 |
| --- | --- | --- |
| `normal_conv` / `weak_conv` | 边界响应会相对较小而且更均匀 | 某一个区域的边界响应会突然变大 |
| `normal_pool` / `weak_pool` | 即使存在较大响应，也会停留在相对较低的范围 | 最大异常响应即使经过 pooling 也会留下来 |
| 最大响应值 | 处在还不至于强烈提示复检的水平 | 单个局部异常可能大到足以改变整体判断 |

输入（input）：

这里使用上面整理好的正常封口（`normal_seal`）和弱封口（`weak_seal`）扫描矩阵。

```python
normal_seal = [
    [2, 2, 2, 2, 2],
    [2, 3, 3, 3, 2],
    [2, 3, 4, 3, 2],
    [2, 3, 3, 3, 2],
    [2, 2, 2, 2, 2],
]

weak_seal = [
    [2, 2, 2, 2, 2],
    [2, 3, 3, 3, 2],
    [2, 3, 6, 2, 1],
    [2, 3, 4, 2, 1],
    [2, 2, 2, 2, 2],
]

kernel = [
    [1, -1],
    [1, -1],
]


def convolve_2x2(image, kernel):
    out = []
    for i in range(len(image) - 1):
        row = []
        for j in range(len(image[0]) - 1):
            score = 0
            for di in range(2):
                for dj in range(2):
                    score += image[i + di][j + dj] * kernel[di][dj]
            row.append(float(score))
        out.append(row)
    return out


def max_pool_2x2(feature_map):
    pooled = []
    for i in range(0, len(feature_map) - 1, 2):
        row = []
        for j in range(0, len(feature_map[0]) - 1, 2):
            block = [
                feature_map[i][j],
                feature_map[i][j + 1],
                feature_map[i + 1][j],
                feature_map[i + 1][j + 1],
            ]
            row.append(float(max(block)))
        pooled.append(row)
    return pooled


normal_conv = convolve_2x2(normal_seal, kernel)
weak_conv = convolve_2x2(weak_seal, kernel)
normal_pool = max_pool_2x2(normal_conv)
weak_pool = max_pool_2x2(weak_conv)

print("normal_conv =", normal_conv)
print("normal_pool =", normal_pool)
print("weak_conv =", weak_conv)
print("weak_pool =", weak_pool)
print("weak seal max response =", max(max(row) for row in weak_conv))
```

在输出里，只要按顺序看：正常封口和弱封口的响应差异，以及最强异常信号在 pooling 之后是否还留着，就够了。

```text
normal_conv = [[-1.0, 0.0, 0.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [-2.0, -1.0, 1.0, 2.0], [-1.0, 0.0, 0.0, 1.0]]
normal_pool = [[0.0, 2.0], [0.0, 2.0]]
weak_conv = [[-1.0, 0.0, 0.0, 1.0], [-2.0, -3.0, 4.0, 2.0], [-2.0, -4.0, 6.0, 2.0], [-1.0, -1.0, 2.0, 1.0]]
weak_pool = [[0.0, 4.0], [-1.0, 6.0]]
weak seal max response = 6.0
```

| 先看的输出 | 这个输出意味着什么 | 如果改动输入，会跟着改变什么 |
| --- | --- | --- |
| `normal_conv` 和 `weak_conv` 的差异 | 即使走的是同一套检测流程，弱封口的某个区域边界响应会明显更大 | 如果改动 `weak_seal` 中异常的位置，强烈反应的格子也会一起移动 |
| `weak_pool` 里的 `6.0` | 即使经过 pooling，最强异常信号仍然会留下来，成为下一阶段的复检候选 | 如果改动 pooling 窗口大小，摘要会变得更粗或更细 |
| 正常场景最大响应 `2.0` 与异常场景最大响应 `6.0` 的差异 | 比起整张图像的整体印象，局部异常分数更可能影响操作判断 | 如果改变 filter 的方向，它可能会对另一类边界异常更敏感 |

在读取这些输出数字时，也要把`响应是在哪里产生的`与`这些响应里什么被留下来了`分开看。

| 比较 | 输出里先看到的事实 | 如果只看数值容易留下的解读 | 带上 convolution·pooling 视角后会改变的解读 |
| --- | --- | --- | --- |
| `normal_conv` vs `weak_conv` | 在弱封口里，某些位置的响应会跳到 `4.0`、`6.0` 这样的值 | 容易只觉得数字变大了 | convolution 会先把局部异常边界按位置打分，让问题 patch 暴露出来 |
| `normal_pool` vs `weak_pool` | 即使经过 pooling，弱封口那边的大响应仍然留着 | 容易觉得 pooling 把信息扔掉后，只是碰巧留下一个大值 | pooling 即使不保留所有位置，也会把对下一阶段判断最重要的异常信号压缩后继续传下去 |
| `weak seal max response` | 最大值 `6.0` 成了最优先的复检候选 | 容易觉得只要有一个大最大值就够了 | 真正关键的不是最大值本身，而是 convolution 制造出来的哪个局部响应会在 pooling 之后继续活着，并改变操作判断 |

- convolution 会读取各位置 patch，并生成`异常边界分数`
- 这些分数组成 feature map，而 `weak_conv` 里有一个位置突然变得很大，这一点最关键
- pooling 会减少信息，但仍然可能把对复检最重要的大响应留下来

也就是说，这个例子展示的是这样一种操作场景：`即使整张图像整体上看起来差不多，只要封口边缘某一部分的边界响应突然变强，就应该重新检查。` 我们之所以要把 convolution 和 pooling 放在一起看，不只是为了记住计算顺序，而是为了理解：`哪个局部异常会活到下一阶段。`

在 CNN 教学里，convolution 和 pooling 几乎总是一起被介绍。因为这两者能以最浓缩的方式展示 CNN 的核心计算流程。

从历史上看，LeNet、AlexNet 这类结构也让人们广泛接受了这样一个直觉：基于 convolution 的局部模式探测，加上基于 pooling 的摘要，构成了图像识别最基础的理解方式。后来的结构当然更丰富了，但在入门阶段，这依然是最重要的一条基础主轴。

这里也可以先停一下，把`什么时候应该先去读“它怎样扫”和“它留下了什么”，而不是先记住运算名字本身`短暂固定下来。这样在进入下一章顺序数据之前，CNN 的计算直觉会更不容易散掉。

| 先想到的问题 | 为什么要先有 convolution·pooling 的视角 | 下一节会继续接到哪里 |
| --- | --- | --- |
| 为什么同一张图像里，有些位置反应很强，有些位置反应很弱？ | 因为 convolution 会把局部模式的匹配程度变成按位置排列的分数 | 下一种结构会怎样读取 feature map |
| 为什么不把所有细节位置都保留下来，而要压缩？ | 因为 pooling 会压缩重要响应，让下一层更容易读取更大的结构 | 这和顺序数据所需要的记忆结构有什么不同 |
| 为什么要先理解 padding、stride、dilation 的区别？ | 因为不只是找什么，连以什么范围、什么步距扫过去，都会改变输出结构 | 到后面结构章节里，当输入结构变化时，读取方式也会怎样变化 |

## 检查清单

- 能解释 convolution 与 pooling 各自到底在计算什么吗？
- 能说明为什么读取局部模式与做成摘要会一起出现吗？
- 能解释 convolution 是一种用小 filter 计算局部模式分数的运算吗？
- 能把 feature map 解释成 filter 响应被按空间记录下来的结果吗？
- 能不只把 pooling 说成`缩小尺寸`，而是解释成`把强响应做成摘要后交给下一层`吗？
- 能说明 CNN 会通过反复执行局部模式探测与摘要来逐步堆出表征吗？
- 当你知道这些运算名字，却不清楚图像是怎样被扫过去、又留下了什么时，能先想到 convolution·pooling 的视角吗？
- 能说明 padding、stride、dilation 都是在改变`filter 会怎样扫过去`的选择吗？

## 来源与参考资料

- Yann LeCun et al., `Gradient-Based Learning Applied to Document Recognition`, Proceedings of the IEEE, 1998，确认日期：2026-06-29。
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016，确认日期：2026-06-29。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, `ImageNet Classification with Deep Convolutional Neural Networks`, NeurIPS 2012，确认日期：2026-06-29。
