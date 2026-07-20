# P5-11.3 补充学习：卷积神经网络（CNN）与视觉 Transformer（ViT, Vision Transformer）比较

Section ID: `P5-11.3`
Version: `v2026.07.18`

在 P5-11.1 与 P5-11.2 里，我们已经先看过：为什么卷积神经网络（CNN）特别适合图像，以及 convolution 和 pooling 分别承担什么角色。顺着这里，自然会出现下一个问题。

在 CNN 之后经常一起被提到的视觉 Transformer（ViT, Vision Transformer）到底有什么不同？为什么在理解后面的生成式 AI 与多模态模型之前，先知道这种差异会有帮助？

当需要再次简短确认 Vision Transformer 的不同起始单位时，可以回到英文概念词汇表里的[ViT（Vision Transformer）](/AiBook/en/reference/concept-glossary/#vit-vision-transformer)条目重新对齐。

## 本补充学习的范围

- CNN 和 ViT 会怎样开始读取一张图像？
- 以局部模式为中心的读取，与以 token 关系为中心的读取，有什么不同？
- 为什么这种差异会成为后面理解 attention、Transformer、生成式 AI 的准备？

这一节补充学习会通过`它们是用什么计算单位开始读取图像`这个问题来比较 CNN 和 ViT。目标不是拉出一条很长的模型谱系，而是先抓住：后来连图像也会通过`被切成像 token 一样的输入单位`与`这些单位之间的关系计算`来读取。

ViT 里的 self-attention 本身，会在后面的 P5-13.2 与 P5-14.1 再重新接回。这里先整理的，只是从图像角度看：`它是先读局部模式，还是先读 patch 之间的关系`，以及这个差异为什么会在走向生成式 AI 时变得有用。

## 本补充学习的目标

- 能比较 CNN 与 ViT 读取图像时的起始单位。
- 能区分 CNN 的局部模式中心读取，与 ViT 的 patch 关系中心读取。
- 能说明 patch token 与 self-attention 会为图像解释带来什么直觉。
- 能连接起来：为什么在后面的 attention、Transformer、生成式 AI 小节里，`把输入当成 token 一样处理`这个视角会不断回来。

## 阅读这个补充学习的顺序

1. 先回想在 CNN 里已经熟悉的起点：`先读取局部模式`。
2. 再比较 ViT 会怎样把图像切成 patch token，并通过 attention 读取它们的关系。
3. 最后整理：为什么这个比较会成为后面 Transformer 系列模型与生成式 AI 输入解释的准备。

## 如果先用一句话比较

| 结构 | 读取图像时的第一直觉 |
| --- | --- |
| CNN | 反复读取小的局部模式 |
| ViT | 把图像切成 patch token，并用 attention 读取 token 之间的关系 |

这一句会在后面再次出现`图像也能像 token 一样处理吗？`这个问题时，成为返回的基准。

## CNN 的自然之处在哪里

CNN 会把图像里相邻像素共同形成意义这件事，直接放进结构本身。

- 它会先读 edge、corner、texture 这样的局部线索
- 再把这些线索逐层堆成更大的局部结构
- 并且把同一个 filter 重复应用到很多位置

所以 CNN 很符合这样一种直觉：`图像里，局部模式很重要。`

## ViT 会让人感觉哪里不一样

ViT 会先把图像切成小的 patch，再把每个 patch 当成 token 一样处理。然后，它会通过 attention 去读：某一个 patch 和其他 patch 之间到底形成了什么关系。

这里最先要拆开的说法，就是`把 patch 当成 token 一样看`。就像语言模型里，token 是组成句子的最小单位一样，在 ViT 里，图像也会被切成很多小方块，而每一个方块都会成为计算的基本单位。

也就是说，ViT 不是从`一个 3x3 filter 去扫邻近像素`这种方式出发，而是从`先把图像切成很多块，再把每一块当成一个输入单位`这种方式出发。

所以，ViT 可以被理解成：先把图像改写成 patch 级 token，再通过 attention 去计算这些 patch 之间关系的结构。

- 先把图像切成很多小块
- 把每个小块当作一个 token
- 再用 attention 去计算：哪些块会和哪些块一起变得重要

把这条流程写得非常简单，会是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-11/vit-patch-flow-zh.mmd"
```

这张图压缩了图像如何被切成 patch，再如何进入 patch 关系计算，最后怎样形成表征的顺序。

1. 先把图像切成小块。
2. 再把每一块变成一个数值向量。
3. 用 attention 计算：每一块会参考其他块到什么程度。
4. 最后把这些结果合起来，交给描述整张图像的表征。

也就是说，ViT 从一开始就把`这个 patch 和那个 patch 之间是什么关系`这个问题放进了计算流程里。

如果把它想成一个很简单的四格图，会更直观。

| 阶段 | 面向入门者的直觉 |
| --- | --- |
| 原始图像 | 一张同时看见储罐与阀门的设备照片 |
| patch 切分 | 把照片切成 4 个或 16 个小方块 |
| patch token | 开始把每个小方块读成一个数值向量 |
| attention | 看含有阀门的方块与含有储罐主体的方块会不会一起变得重要 |

也就是说，ViT 不会先强烈假设`只有紧挨着的像素关系最重要`，而是更直接地问：`这一块和那一块到底有多相关。` 这个点也会在后面阅读 Transformer 系列生成模型时，自然地再接回来。

如果说 CNN 更像是`从近处出发，一路长成更大的结构`，那么 ViT 更接近`直接去读这些块之间的关系`。

`CNN 会把局部模式往上堆，而 ViT 会试图直接读取 patch token 之间的关系。`

## 为什么“把图像切成 patch”这件事很重要

第一次读 ViT 时，最容易困惑的地方之一，就是：`为什么非要把图像切成一块一块？`

真正的核心原因在于：attention 是一种会计算`输入单位之间关系`的结构。在句子里，这个输入单位是 token；而在图像里，patch 承担了这个角色。

- 在句子里，词片之间会形成关系。
- 在 ViT 里，图像片段之间也会形成关系。

也就是说，patch 并不只是某种预处理技巧，而是对这样一个需求的回答：`即使是图像，attention 也需要一个基本单位可以去读。`

关键点是：patch 是图像中的一个小区域，而它会被改写成一个 attention 能读取的基本向量单位。

- 一个 patch 是图像里的一个小方形区域
- 一个 patch 之后会变成一个数值向量
- attention 会计算这些 patch 向量彼此之间有多相关

如果 patch 切得太小，计算量会增加；切得太大，又可能把细小的局部信息糊掉。这些设计选择与学习 recipe 属于 ViT 的更细实现主题，所以这里不展开。当前只要稳稳抓住一点就足够了：`ViT 会把 patch 当作输入单位。`

把这件事再和 CNN 放在一起读，差异会更清楚。

- 在 CNN 里，小的 filter 会扫过`彼此相邻的像素`
- 在 ViT 里，已经切好的 patch 会`从一开始就成为读取单位`

也就是说，如果 CNN 的第一个问题更接近`这附近有没有 edge 或 texture？`，那么 ViT 的第一个问题就更接近`这个 patch 会和哪些其他 patch 形成关系？`

这个差异会原封不动地继续延伸到后面的生成式 AI。因为在生成式 AI 里，文本会被切成 token，图像也会被改写成 patch、latent token 等单位，而这些单位之间的关系计算会一再出现。所以，如果先在这里抓住`图像是按什么单位被切开并读取的`，后面即使模型名字换了，解释输入的基本视角也不会太摇晃。

## 把 CNN 和 ViT 的起始单位并排放在一起

| 问题 | CNN | ViT |
| --- | --- | --- |
| 第一轮计算触及的单位 | 小的 receptive field | 已经切好的 patch |
| 一开始先强调什么 | 相邻像素之间的局部模式 | patch 与 patch 之间的关系 |
| 随着层变深，预期会发生什么 | 读取更大的局部结构 | 读取更宽的 patch 关系 |

## 如果继续往生成式 AI 看，会准备好什么

这一节之所以会紧跟在 CNN 之后，并不只是因为`顺便把 ViT 也认识一下`。更重要的理由，是先在脑子里建立起一种感觉：图像后来也会被当成`像 token 一样切开的输入`。

很多初学者会觉得生成式 AI 突然变难，其中一个原因就是：文本里一直在讲 token，可到了图像这里，又突然出现 patch、latent、multimodal token 这些词。但底层问题其实没有那么不同。

- 输入应该切成什么单位？
- 这些单位会被改写成什么向量表征？
- 这些单位之间的关系要靠什么方式去计算？
- 这些结果又会怎样被传给后面的生成、分类或说明阶段？

CNN 更接近这样一种回答：先把`邻近像素与局部模式`立起来。ViT 则更接近另一种回答：先把`切好的 patch token 与它们之间的关系`立起来。等到去读生成式 AI 时，ViT 这一侧的视角会更频繁地重新出现。因为在图像生成模型、vision-language model、多模态聊天模型里，都反复会出现：先把输入改写成规则的单位，再去计算这些单位之间的关系，有时还要和文本 token 一起处理。

当然，并不是所有生成式 AI 都完全照着 ViT 的结构来。有人会把图像读成 patch token，有人会使用经过 CNN 系列 encoder 的表征，也有人会在 latent space 里使用类似 token 的单位。但即便如此，读者首先应该抓住的共同问题依然是同一个：与其问`图像是不是被整体当作一块处理`，不如问`它被切成了什么输入单位，这些单位之间的关系又是怎样计算的`。

把这个视角放到文本与图像输入两侧并排去看，会更清楚。

| 问题 | 文本输入 | 图像输入（CNN 侧直觉） | 图像输入（ViT 侧直觉） |
| --- | --- | --- | --- |
| 最先切开的单位 | token | 小局部窗口附近的像素 | patch token |
| 一开始先强调什么 | token 顺序与上下文关系 | 相邻位置的局部模式 | patch 之间的关系 |
| 后面又会重新变重要的问题 | 哪个 token 与哪个 token 发生连接 | 哪个位置的局部线索先起反应 | 哪个 patch 会和哪个 patch 一起变得重要 |
| 对生成式 AI 的准备 | token 级输入读取直觉 | 局部特征提取直觉 | token 化图像输入与关系计算直觉 |

这张表的目的，并不是勉强把文本和图像说成同一件东西，而是显示这样一个共同框架：即使输入不同，我们仍然会`先把输入切成基本单位，再去计算这些单位之间的关系`。一旦先把这个框架固定住，后面再遇到 `text token`、`image token`、`patch embedding`、`vision encoder`、`multimodal token` 这些说法时，就更容易在同一问题之下重新整理，而不是分别硬背。

## 案例与示例

### 案例 1. 在管道照片里读取阀门与主体的方法

假设我们要从一张管道照片中分类阀门状态。人一开始很容易先想到的是：能不能看见阀门把手、管道主体、金属轮廓这些显眼部分。

- 从 CNN 的视角看，会先抓到阀门边界、金属纹理、管道轮廓这类局部响应，然后这些响应会在多层里逐渐堆成更大的设备表征。
- 从 ViT 的视角看，则更适合直接去想：含有阀门的 patch 和含有管道主体的 patch，会不会因为某种关系而一起变得重要。

| 问题 | CNN 先看到什么 | ViT 先建立什么 |
| --- | --- | --- |
| 在一张管道照片里读取阀门与管道主体时 | 阀门边界、金属纹理、管道轮廓这类局部响应 | 含有阀门的 patch 与含有管道主体的 patch 是否共同组成同一设备 |

所以，这个案例里真正要确认的结果，不只是`它们是不是都能认出管道`，而是：CNN 会先提出`哪一个局部位置先强烈起反应`，而 ViT 会提出另一个起点问题：`哪一个 patch 关系会一起变得重要`。

```mermaid
--8<-- "assets/part-05/chapter-11/cnn-vit-valve-body-case-flow-zh.mmd"
```

这张图把案例 1 压缩成了`同一输入 -> CNN 的局部线索问题 -> ViT 的 patch 关系问题`，从而让我们能一眼看出：两者是从哪里开始拥有不同的判断起点。

这个比较里真正重要的，不是把它们简单切成`CNN 看部分，ViT 看整体`。两者最终都会走向整张图像的判断，但它们在起始直觉上，确实有`局部模式中心`与`patch 关系中心`的差异。

而这个差异，恰好会马上影响到后面的生成式 AI。等到我们之后遇到：图像会像 token 一样被切开，用 attention 读取很多 token 之间的关系，甚至和文本 token 一起处理的结构时，这里就先帮读者准备了：`为什么图像也可以用这种方式表达。`

## 练习与例子

这个例子的目标，是把同一张检测帧同时交给 CNN 风格的读取与 ViT 风格的读取，然后比较：`局部缺陷候选`与`远距离区域关系`会怎样以不同方式先被读出来。它不会去实现一个完整 CNN 或完整 ViT，但会让我们直接看到：同一输入在这两种结构里会被改写成什么样的计算单位。

问题场景：

- 即使面对同一张检测帧，CNN 会先密集地扫描小缺陷候选，而 ViT 会从比较较大区域 token 之间的关系开始

输入：

- 一张 6x6 的检测帧，里面同时包含标签印刷区域、空白背景区域、封口区域、代码区域
- CNN 读取的 2x2 局部 patch
- ViT 读取的 3x3 patch token

输出：

- 按 CNN 方式抽出的局部缺陷高优先候选
- 按 ViT 方式得到的各区域 patch token 平均值
- 代码区域 token 与其他区域 token 之间的差异

要确认的概念：

- CNN 会沿着重叠的局部 patch，先读出局部缺陷候选
- ViT 会先形成不重叠的 patch token，再去比较分离区域之间的关系
- 即使面对同一输入，`现在最先浮出来的异常信号`也会随着输入被改写成什么计算单位而改变

这里 ViT 一侧的 `patch token mean` 并不是真正的 patch embedding 或 self-attention 结果。真正的 ViT 会先把 patch 投影成向量，再加上位置资讯，并通过多层 attention 去计算关系。这个例子把那个过程缩短了，只确认：`一旦图像被改写成不重叠的大 patch 单位，会先出现什么样的区域比较问题。`

输入（input）：

这里使用上面整理好的 6x6 包装检测帧，以及 CNN / ViT 风格的切分规则。

在读代码之前，只要先抓住一个问题就够了：如果把同一帧送进这两种结构，CNN 会先把`哪个小位置先跳出来`摆在前面，而 ViT 这一侧的辅助计算会先把`哪个区域关系先拉开`摆在前面。

```python
# 这个例子比较同一检查帧中，CNN 重叠局部分数和 ViT 式非重叠 patch token 均值会先显出哪些异常信号。
inspection_frame = [
    [4, 4, 4, 1, 1, 1],
    [4, 5, 4, 1, 2, 1],
    [4, 4, 4, 1, 1, 1],
    [2, 2, 2, 3, 3, 3],
    [2, 2, 2, 3, 8, 3],
    [2, 2, 2, 3, 3, 3],
]


def cnn_local_scores(image, window=2, stride=1):
    patches = []
    for i in range(0, len(image) - window + 1, stride):
        for j in range(0, len(image[0]) - window + 1, stride):
            values = []
            for di in range(window):
                for dj in range(window):
                    values.append(image[i + di][j + dj])
            local_score = max(values) - min(values)
            patches.append(((i, j), local_score, values))
    return sorted(patches, key=lambda item: (-item[1], item[0]))


def vit_patch_tokens(image, patch_size=3):
    tokens = []
    for i in range(0, len(image), patch_size):
        for j in range(0, len(image[0]), patch_size):
            values = []
            for di in range(patch_size):
                for dj in range(patch_size):
                    values.append(image[i + di][j + dj])
            mean_value = round(sum(values) / len(values), 2)
            tokens.append(((i, j), mean_value, values))
    return tokens


cnn_candidates = cnn_local_scores(inspection_frame, window=2, stride=1)[:5]
vit_tokens = vit_patch_tokens(inspection_frame, patch_size=3)
token_means = {position: mean for position, mean, _ in vit_tokens}

print("[cnn top local candidates]")
for position, score, values in cnn_candidates:
    print("position =", position, "score =", score, "values =", values)

print("[vit patch tokens]")
for position, mean, values in vit_tokens:
    print("position =", position, "mean =", mean, "values =", values)

print("seal_code_gap =", round(abs(token_means[(3, 0)] - token_means[(3, 3)]), 2))
print("blank_code_gap =", round(abs(token_means[(0, 3)] - token_means[(3, 3)]), 2))
```

在输出里，先看 CNN 的局部缺陷高优先候选，与 ViT 的区域 token 摘要会怎样提出不同的起始问题，就够了。

```text
[cnn top local candidates]
position = (3, 3) score = 5 values = [3, 3, 3, 8]
position = (3, 4) score = 5 values = [3, 3, 8, 3]
position = (4, 3) score = 5 values = [3, 8, 3, 3]
position = (4, 4) score = 5 values = [8, 3, 3, 3]
position = (0, 2) score = 3 values = [4, 1, 4, 1]
[vit patch tokens]
position = (0, 0) mean = 4.11 values = [4, 4, 4, 4, 5, 4, 4, 4, 4]
position = (0, 3) mean = 1.11 values = [1, 1, 1, 1, 2, 1, 1, 1, 1]
position = (3, 0) mean = 2.0 values = [2, 2, 2, 2, 2, 2, 2, 2, 2]
position = (3, 3) mean = 3.56 values = [3, 3, 3, 3, 8, 3, 3, 3, 3]
seal_code_gap = 1.56
blank_code_gap = 2.45
```

因为同一张帧会从不同的起点开始制造表征，所以等到后面再读 attention 与 patch embedding 时，也必须一起去看：`到底是什么被当成 token 处理。`

如果把 CNN 风格的 2x2 局部分数画成地图，代码区域周围那些彼此重叠的窗口，会连续地成为最高优先候选。这里最先浮出的提问是：`到底哪一个小位置需要被重新检查？`

![CNN 风格的 2x2 局部候选分数地图](/AiBook/assets/part-05/chapter-11/cnn-vit-cnn-local-score-map-zh.png)

如果模仿 ViT 风格的起始单位，单独去看 3x3 patch 的平均值，那么同一张帧就会被压缩成四个较大的区域。这些平均值不是实际 ViT 的 attention 数值，而只是辅助值，用来展示：一旦从 patch token 出发，会先出现什么样的区域比较问题。

![ViT 风格的 3x3 patch token 平均值地图](/AiBook/assets/part-05/chapter-11/cnn-vit-patch-token-mean-map-zh.png)

| 先看的输出 | 这个输出意味着什么 | 如果改动设定，会跟着改变什么 |
| --- | --- | --- |
| CNN 的高优先候选聚集在 `(3, 3)` 周围 | 说明 CNN 会先很强地暴露`代码区域中央的局部异常` | 如果改变 `window` 尺寸或 `stride`，局部缺陷候选的密度也会改变 |
| ViT 风格辅助 patch 平均里，`(3, 3)` 区域高到 `3.56` | 说明如果把整个代码区域先总结成一个 patch 单位，就会自然出现拿它和其他区域比较的起点 | 如果把 `patch_size` 切小，分块会更细；切大，区域摘要会更粗 |
| `seal_code_gap` 与 `blank_code_gap` 都被算出来 | 说明从 patch 单位出发时，比较相隔较远区域之间差异的问题会自然跑到前面 | 如果换别的区域对来比较，就会用另一种方式读取`哪种关系更异常` |

即使读这些输出数字时，也要把`哪个位置先跳出来`与`哪一种区域关系拉得更开`分开看。

| 比较 | 输出里先看到的东西 | 这组比较里真正要抓住的意思 |
| --- | --- | --- |
| CNN 高优先候选 | 围绕 `(3, 3)` 的 2x2 窗口连续出现在最前面 | 这说明 CNN 是一种会扫过重叠局部窗口，并先建立`哪个小位置是复检候选`的问题结构 |
| patch 单位辅助值 | `(3, 3)` patch 的平均值是 `3.56`，而 `(0, 3)` patch 的平均值是 `1.11` | 这说明一旦把图像改写成 patch 单位，`这个区域与另一个区域差在哪里`就会跑到更前面 |
| `seal_code_gap` vs `blank_code_gap` | 代码区域和空白区域之间的 gap，比代码与封口区域之间更大 | 这说明在 ViT 这一侧，`哪个区域和哪个区域更不对齐`这样的关系问题会自然跑到前面 |

也就是说，这个比较真正的核心在于：CNN 是从会重叠移动的局部窗口出发，先制造`哪里应该重看`；ViT 则是从已经切好的 patch token 出发，进一步比较`哪些区域在关系上更不对齐`。

在这个例子里，可以继续把 `inspection_frame` 做大，或者改动 `patch_size` 与 `stride`。这样读者就不只是死记`CNN 看局部，ViT 看 patch`这句话，而是能够直接比较：同一输入会被改写成多少个`局部缺陷候选`，又会被改写成多少个`区域 token 关系`。这种直觉以后在阅读图像 token 数、patch 尺寸、多模态输入单位时也会继续派上用场。

## 它和 self-attention 又是怎样连起来的

如果想把 ViT 理解成一种图像版 Transformer，就必须在`它把 patch 当成 token 来看`之后，马上看到下一步连接：`所以 self-attention 就可以被用上。`

- 在句子里，token 会彼此参考
- 在 ViT 里，patch token 也会彼此参考
- 所以 self-attention 同样可以作用在图像上

也就是说，ViT 可以被看成一个例子，展示了：`原本在语言里使用的 attention 计算方式，也可以迁移到图像读取问题上。`

这条连接在阅读生成式 AI 时尤其重要。后面不管是文本生成模型、图像描述模型，还是多模态问答模型，哪怕输入类型不同，attention 一再出现时，本质上都还是在计算：`这些单位之间，谁在参考谁。` 如果先通过 ViT 看见：图像也可以进入这套计算框架，那么后面再遇到 attention 往语言之外扩展，就会自然得多。

不过，这里并不会先展开 self-attention 的公式，也不会先讲 Q、K、V。那部分核心结构会在 P5-13.2 再重新整理，Transformer 的整体流程会在 P5-14.1 再回收。

## 为了生成式 AI，最少要记住什么

记住下面这张表，其实就足够了。

| 问题 | CNN | ViT |
| --- | --- | --- |
| 一开始先强调什么 | 局部模式 | patch token 之间的关系 |
| 核心计算直觉 | convolution + pooling | self-attention |
| 图像解释给人的感觉 | 从小部分一路长成更大结构 | 直接去读取很多 patch 之间的相关性 |
| 通往生成式 AI 的准备 | 基于局部线索的输入直觉 | token 化图像输入与关系计算直觉 |

整理到这个程度后，从这一节直接带去阅读生成式 AI 的准备句，大致可以压成下面四句。

1. 图像也可以像文本一样，被切成某种基本单位来读取。
2. 这个单位是什么，会决定模型一开始提出什么问题。
3. ViT 的视角会让我们用 token 与关系计算的框架去理解图像输入。
4. 所以后面再遇到 image token、multimodal token、vision encoder 这些词时，就不会觉得它们像一套完全陌生的新语言。

## 为什么它在 Part 5 的流程里重要

这一节补充学习之所以有必要，是因为在 Part 5 后面会继续学 attention 与 Transformer，而之后进入生成式 AI 时，`token`、`关系`、`多模态输入`这些词又会不断回来。

- 在 P5-11 里，我们先固定住为什么 CNN 对图像是自然的
- 在 P5-13、P5-14 里，再去学为什么 attention 与 Transformer 会成为转折点
- 然后才会更自然地看到：`原来 attention 系列结构也能用在图像上`，`原来图像也能像 token 一样处理`

也就是说，这个补充学习不是为了抹掉 CNN 然后直接跳到 ViT，而是为了提前整理：`局部模式型图像结构`和`token 关系型结构`其实是从不同的问题设置起步的。

这里也可以先停一下，把`什么时候单靠 CNN 说明已经不够，必须单独把 ViT 比较视角拿出来`短暂固定一下。这样后面接到 attention 与 Transformer 小节时，连接会更稳。

| 先想到的问题 | 为什么要先有 CNN-vs-ViT 的比较视角 | 后面会继续接到哪里 |
| --- | --- | --- |
| 为什么图像 attention 结构突然出现时，也不会显得完全陌生？ | 因为如果先固定住 patch token 与关系读取的起点差异，就能在图像语境里把 attention 继续接着读下去 | self-attention 与 Transformer 的一般计算结构 |
| 为什么不能把 CNN 与 ViT 简单读成旧结构/新结构比较？ | 因为它们在读取图像时的第一个计算单位，以及默认的关系假设，本来就不同 | attention 型 vision 结构该用什么问题去读 |
| 为什么 patch 这个词会突然变重要？ | 因为图像也需要一个能被当成 token 处理的基本单位，attention 结构才能接上去 | patch token、self-attention、image Transformer 扩展与多模态输入读取 |

## 检查清单

- 能解释 CNN 与 ViT 在开始读取图像时，所用单位是怎么不同的吗？
- 能以入门层次说明：从局部模式出发，与从 token / patch 出发，有什么区别吗？
- 能解释 CNN 会反复读取局部模式，而 ViT 则会先把图像 patch 当成 token，再用 attention 读取 patch 间关系吗？
- 能把 CNN 与 ViT 的差异解释成`局部模式中心`与`patch 关系中心`的起点差异吗？
- 能把 patch 解释成不只是预处理技巧，而是`attention 在图像中要读取的基本单位`吗？
- 当只靠 CNN 的解释还不足以让图像 attention 结构显得自然时，能先想到 CNN-vs-ViT 的比较视角吗？
- 当自己想把 CNN 与 ViT 只读成旧结构/新结构比较时，能重新拿出局部模式中心与 patch 关系中心的起点差异吗？
- 等到后面进入 attention 小节时，是否已经准备好先去问：`图像片段也能像 token 一样彼此形成关系吗？`

## 来源与参考资料

- Alexey Dosovitskiy et al., `An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale`, ICLR 2021, URL: [https://openreview.net/forum?id=YicbFdNTTy](https://openreview.net/forum?id=YicbFdNTTy){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-30。
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, URL: [https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-30。
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-30。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
