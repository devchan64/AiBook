# P4-18.1 降维(dimensionality reduction)

> Section ID: `P4-18.1`
> Version: `v2026.07.26`

在 P4-17 里，我们用[聚类(clustering)](/AiBook/zh/reference/concept-glossary-pinyin/c/#clustering)追问`隐藏着什么分组`。这里抓住另一个问题。

如果[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#feature)太多，结构很难读，能不能把表达本身重新做成更少的轴？

这个问题，就是[降维(dimensionality reduction)](/AiBook/zh/reference/concept-glossary-pinyin/d/#dimensionality-reduction)的起点。降维不是简单丢掉很多特征的技术，而更接近`当原始表达太复杂时，用更容易阅读的轴重新表达`。

这一节会用同一个玩具数据场景，把[维度(dimension)](/AiBook/zh/reference/concept-glossary-pinyin/d/#dimension)、[PCA(principal component analysis)](/AiBook/zh/reference/concept-glossary-pinyin/p/#principal-component-analysis-pca)，以及`为什么这里会出现特征值(eigenvalue)和特征向量(eigenvector)`连在一起说明。下一节 P4-18.2 会继续讨论这样得到的图能信到什么程度，以及信息损失该怎么读。

## 降维先收束的问题

这一节回答下面这些问题。

- 在机器学习里，dimension 到底指什么？
- 为什么特征数一多，学习和解释都会变难？
- 降维想缓解什么问题？
- PCA 展示了什么代表性直觉？
- 为什么[方差(variance)](/AiBook/zh/reference/concept-glossary-pinyin/v/#variance)、正交(orthogonal)、特征值、特征向量会一起出现在 PCA 说明里？
- kernel PCA 和 Truncated SVD 与 PCA 应该用什么直觉区分？

这一节集中在入门层面抓住`为什么要降维`以及`PCA 做的是一种什么计算`。可视化结果解释、t-SNE、UMAP、重构误差(reconstruction error)、trustworthiness 会在下一节 P4-18.2 里继续处理。

## 降维要留下的判断标准

- 能把降维解释为`用更少的轴重新表达特征空间`。
- 能把 PCA 解释成`把数据变化很大的方向重新设成新轴的方法`。
- 能说明为什么第一成分和第二成分要彼此正交。
- 能把特征向量读成新轴方向，把特征值读成该轴解释的变动大小。

## 为什么需要这一节

随着机器学习继续往下学，特征(feature)会越来越多。

- 客户数据里可能有几十个数值指标
- 文档数据里可能有几千个词特征
- 图像数据里会因为像素数而产生大量特征

这时读者很容易产生下面这种感觉。

- 特征越多，不是应该越细吗？
- 那为什么反而会更难理解？

这正是降维变得必要的地方。特征数越多，信息可能更多，但人更难一次抓住结构。所以降维会先检查`现在这个表达是不是太复杂`，再创建能重新阅读大流向的轴。

## 先看一个场景

这一节会反复使用下面这个两个特征几乎一起移动的小数据。

| 样本 | 每月访问次数 `x1` | 平均购买金额 `x2` |
| --- | ---: | ---: |
| A | 2.0 | 2.1 |
| B | 3.0 | 3.2 |
| C | 4.0 | 3.9 |
| D | 5.0 | 5.1 |

这张表有一个流向：`访问次数较高的客户，平均购买金额也大体一起升高`。现在只有两条轴，所以还能直接看出来，但 PCA 为什么有用的核心已经出现了。

1. 两个特征几乎朝同一个方向移动。
2. 于是不用一直分别拿着两条轴，一个新轴也可能概括大的流向。
3. 但两条轴之间细小错位的差异可能会变弱。

也就是说，降维不是`把复杂表格硬塞进几个轴里`，而是`决定什么作为大流向、什么作为细节差异留下`。

## dimension 在这里指什么

在机器学习语境里，dimension 通常和描述一个样本所需的轴数量相连，也就是特征数。

在上面的表里，一个客户由`每月访问次数`和`平均购买金额`两个值表示，所以这是二维数据。如果再加上`距离最近一次登录已经过去多少天`，它就变成三维；如果再加上`退货比例`，它就变成四维。

如果把这个感觉画得很简单，会是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-01-zh.mmd"
```

这里先把维度理解成`看数据时使用的坐标轴个数`就够了。每增加一个特征，描述数据的轴也会增加一条。

## 为什么特征一多就会更难

特征多，一方面意味着表达能力可以变强，但同时也带来三类困难。

1. 人更难直接想象结构
2. 计算成本可能上升
3. 无用或重叠的信息可能很多

例如，下面这些值彼此可能并不完全独立。

- 每月购买金额
- 每年购买金额
- 购买次数
- 平均订单金额

这时问题不只是`特征数很多`，而是`真正新增的信息到底有多少`。如果很多特征几乎朝同一个方向变化，原始表格可能很长，但真正要读的大流向也许并不多。

所以，降维也会变成一个重新追问`当前表达是不是不必要地变得太庞大`的步骤。

## 降维想缓解什么

scikit-learn 用户指南把 PCA 描述成：把多变量(multivariate)数据集分解成连续的正交成分(component)，并找出能解释最多方差的方向。

在入门层面，可以把降维读成一种试图缓解下面问题的做法。

| 困难 | 降维试图提供的帮助 |
| --- | --- |
| 特征太多，看不清结构 | 试着用更少的轴重新概括 |
| 特征彼此重叠 | 试着把重叠变动归并成少数几个成分 |
| 可视化困难 | 降到 2D 或 3D 先看一个大致结构 |
| 计算太重 | 改成更小的表达，让后续模型更容易处理 |

所以，与其把降维理解成`完全替代原始数据`，不如理解成`构建一种更容易阅读的表达工具`。

## PCA 怎样重新表达这个场景

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-02-zh.mmd"
```

PCA 试图把`数据实际扩散很多的方向`重新设成新轴。在上面的玩具数据里，`x1` 和 `x2` 几乎一起变大，所以比起分别看两个轴，一条对角线方向更像重要的大流向。

## PCA 展示了什么代表性直觉

scikit-learn 文档把 PCA 描述成一种寻找`能够解释最多方差的连续正交成分`的方法。

`先把数据扩散最多的方向拿来做第一条轴，再在与它垂直的方向里，找出另一个仍然扩散很多的方向做第二条轴。`

PCA 更接近一种这样的感觉：不是继续直接使用原来的 x、y、z 轴，而是把轴重新旋转到数据真正变化很大的方向上。

## 换一种更容易懂的 PCA 比喻

想象很多点斜着铺成一个椭圆。

- 如果按原来的 x 轴、y 轴去看，扩散会被分得比较别扭
- 但如果把椭圆长轴当成新的轴 1，大的变化流向会更容易被看见
- 如果把短轴当成新的轴 2，就能把较小的波动单独分出来

PCA 就是在尝试寻找`比原始坐标系更贴近数据流向的坐标系`。

把这个感觉压缩成图，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-03-zh.mmd"
```

这张图帮助读者把 PCA 读成`根据数据真正扩散较多的方向，再次旋转轴的过程`。一旦找到更贴近数据流向的轴，第一成分就能比原来的坐标轴更高效地解释主要变动。

## 为什么要看 variance

正如在 Part 2 和 Part 3 前面看到的，variance 是一种用来感受数值分散程度的基本方式。PCA 想抓住的，正是这种“分散得最多的方向”。

- 方差大的方向：数据变化很大的方向
- 方差小的方向：可能只是相对没那么重要的波动

当然，方差小并不代表一定没有意义。但在降维时，常常在问的是：`能不能先保留大的变动，再把较小的变动往后放甚至舍弃？`

总结起来，PCA 按照`什么变化得更多`来决定概括的优先级。

如果把这个优先级说得再直接一点：PCA 并不会一口气保留所有变动，而是先留下最能解释整体大变动的成分；之后的成分，则在不和前一个重叠的方向上解释剩下的变动。

## 为什么会出现 orthogonal 这个词

scikit-learn 文档把 PCA 的成分描述成 orthogonal components。这里的 orthogonal 可以理解成：新轴彼此不重叠，也就是尽量减少重复解释。

把它说短一点，就是：

`第一成分已经解释过的变动，第二成分不应该原样再解释一遍。`

所以，PCA 会在创建新轴的同时，把信息尽量分散到不同方向里去承载。

## 为什么 PCA 里会出现 eigenvalue 和 eigenvector

只要稍微往深一点看 PCA，马上就会碰到协方差矩阵(covariance matrix)的 eigenvalue 和 eigenvector。原因其实很简单。

`如果要用公式找出数据扩散最大的方向，就得找到最能解释这种扩散的方向向量。`

在入门层面，只要先抓住下面这个流程就够了。

1. 先把数据做中心化(centering)
2. 构造一个描述各轴共同变化程度的协方差矩阵
3. 在这个矩阵里找出`最能解释方差的方向`
4. 把那些方向读成 eigenvector，把沿着那些方向的方差大小读成 eigenvalue

公式通常写成下面这样。

\[ \Sigma v = \lambda v \]

这里：

- \(\Sigma\)：协方差矩阵
- \(v\)：方向向量，也就是候选新轴
- \(\lambda\)：这个方向上的方差大小

如果把这个式子翻成话，它就是：

- 当你沿着某个方向 \(v\) 去看数据时
- 协方差结构又把这个方向按同一个方向拉伸
- 那么这个方向就会成为解释数据扩散的轴候选

所以，在 PCA 里，eigenvector 可以读成`新轴的方向`，而 eigenvalue 可以读成`这条新轴解释了多少变动`。

| 在 PCA 里想看到的东西 | 数学上对应什么 |
| --- | --- |
| 第一条最重要的新轴 | 对应最大 eigenvalue 的 eigenvector |
| 下一条重要的新轴 | 对应下一个较大 eigenvalue 的 eigenvector |
| 每条轴解释了多少信息 | 各个 eigenvalue 的大小 |

即使不把完整推导一路跟到底，也很有必要先在这里抓住`为什么 eigenvector 会变成轴、eigenvalue 会变成解释方差`这个连接。否则 PCA 就只会停留在“旋转轴”的比喻上，而不会成为`寻找最能解释方差方向的计算`。

## kernel PCA 和 Truncated SVD 有什么不同

PCA 并不是降维里唯一的标准。即便都属于`重建表达`这条大流里，也会因为“想更好处理什么”而出现不同名字。

| 方法 | 入门时先抓住的核心 | 更自然会在哪些场景里出现 |
| --- | --- | --- |
| PCA | 重新建立线性(linear)轴，并保留大方差方向 | 想概括数值特征里的大范围整体变动时 |
| kernel PCA | 试图在 kernel 空间里看清原空间中不容易线性表达的结构 | 想更好展开弯曲或非线性结构时 |
| Truncated SVD | 通过矩阵分解，只保留少数几个主要成分 | 处理稀疏(sparse)矩阵或文本-词矩阵时 |

如果把差别写得更短一点：

- PCA：`用直线型新轴重新看`
- kernel PCA：`连非线性结构也想展开来看`
- Truncated SVD：`在大矩阵里只保留几个最重要成分`

从数学上看，它们注视的对象也稍有不同。

| 比较项 | PCA | kernel PCA | Truncated SVD |
| --- | --- | --- | --- |
| 基本起点 | 协方差结构 | 通过 kernel 构造的相似度结构 | 对原始数据矩阵本身做分解 |
| 更贴合的感觉 | 线性再表达 | 非线性再表达 | 大矩阵的低秩近似 |
| 初学者最先要记住的差异 | `旋转轴并抓住大方差` | `把直线轴看不清的结构放到别的空间里看` | `把矩阵压成少数几个成分` |

换句话说，kernel PCA 和 Truncated SVD 不是 PCA 的小变体，而是它们在`把什么当成数据的中心结构`这件事上稍有不同的分支。在这一节里，比起记名字，更值得先把它们区分成 `线性轴再表达`、`非线性结构展开`、`矩阵压缩` 这三种感觉。

## 降维之后，什么变好，什么又会消失

降维总会带来一种交换(trade-off)。

| 得到的东西 | 可能失去的东西 |
| --- | --- |
| 更简单的表达 | 原始数据里按特征展开的细节 |
| 更容易做可视化 | 某些细小差异 |
| 更快的计算 | 解释时的直接性 |
| 被压缩的重叠信息 | 绑在某一条轴上的业务意义 |

所以，看完降维后的表达之后，总要再问一句：

`现在这个更简单的表达，已经足够支撑我眼前想看的问题了吗？`

这句话重要，是因为降维总是先改变表达，再问这种改变后的表达对当前任务是不是还够用。

有时，简化后的轴已经足够看清大的流向。

有时，某个按特征区分的重要差异，会在压缩过程中变弱。

所以，降维很方便，但它从来都不是免费的。

真正要追问的，不只是`图是不是更容易读了`。

还包括`图变得更容易读的同时，当前问题真正重要的差异有没有一起被压掉`。

## 案例与示例

### 案例 1. 当客户指标有几十项，想先压成几个轴来读时

假设一个业务团队手里同时有很多客户指标：访问次数、购买金额、最近活跃度、会话时长、品类多样性、折扣响应等等。直接盯着完整表格看，很难抓住整体流向。这时，降维可以把信息压缩成少数几个成分，比如 `类似活跃度的轴`、`消费规模轴`、`类似最近性的轴`，让结构更容易重新被看见。这里重要的不是原始特征从此没用了，而是`先建立一种新的表达，让大的结构变得可读。`

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-05-zh.mmd"
```

如果把这个案例压缩成审查备忘，可以写成这样。

| 先想概括什么 | 不要立刻下什么结论 | 下一步要确认什么 |
| --- | --- | --- |
| 客户行为能不能通过几个大轴重新来读 | 不要把一条压缩轴直接等同成一个业务意义 | 检查哪些原始特征对这条轴贡献较大 |
| 在后续聚类或建模前，能否先看见整体流向 | 不要把降维后的表达当成原始表格的完整替代品 | 和原始特征对照，并检查信息损失 |

## 练习与示例

这个练习继续直接使用前面那四个样本，把它变成一个小型动手检查：`如果真的用 PCA 把 2 维数据压成 1 维，什么会留下，什么会消失？`

- 问题场景：当两个特征几乎一起移动时，只保留 1 个主成分，看看大的流向是否仍能保住
- 输入(input)：访问次数与平均购买金额两个特征
- 期望输出(output)：1 维主成分分数、解释方差比、复原值
- 要确认的概念：PCA 可以把原始特征投影到 1 条新轴上；即使只保留 1 个成分，也可能保住大部分大变动，但复原值不一定和原始值完全相同

```python
# 这个例子用 PCA 把二维特征降到一个主成分，再复原来看还保留了什么。
import numpy as np
from sklearn.decomposition import PCA

sample_ids = np.array(["A", "B", "C", "D"])
X = np.array([
    [2.0, 2.1],
    [3.0, 3.2],
    [4.0, 3.9],
    [5.0, 5.1],
])

pca = PCA(n_components=1)
X_reduced = pca.fit_transform(X)
X_restored = pca.inverse_transform(X_reduced)

print("principal axis:", np.round(pca.components_, 3))
print("explained variance ratio:", np.round(pca.explained_variance_ratio_, 3))

for idx, reduced, restored in zip(sample_ids, X_reduced, X_restored):
    print(
        idx,
        "reduced =", np.round(reduced, 3),
        "restored =", np.round(restored, 3),
    )
```

执行结果如下。

```text
principal axis: [[0.707 0.707]]
explained variance ratio: [0.996]
A reduced = [-2.112] restored = [2.007 2.086]
B reduced = [-0.662] restored = [3.032 3.111]
C reduced = [0.52] restored = [3.868 3.947]
D reduced = [2.254] restored = [5.093 5.172]
```

这个结果里要读出的重点如下。

1. `principal axis` 几乎是 `[0.707, 0.707]`，说明两个特征以相近权重一起变化的方向，被抓成了第一主成分。
2. `explained variance ratio` 是 `0.996`，说明只保留 1 个成分，也能保住几乎全部的整体变动。
3. `restored` 值和原值非常接近，但并不完全相同，这说明降维可以保住大的流向，同时仍会丢掉一些细节。

### 改一个值看看：如果不再一起移动，复原误差会变大

这一次，故意把最后一个样本的第二个特征大幅压低，让两个特征不再沿着同一条流向移动。

```python
# 这个例子加入两个特征不一起变化的样本，观察 PCA reconstruction error 如何变大。
import numpy as np
from sklearn.decomposition import PCA

sample_ids = np.array(["A", "B", "C", "D"])
X = np.array([
    [2.0, 2.1],
    [3.0, 3.2],
    [4.0, 3.9],
    [5.0, 2.5],
])

pca = PCA(n_components=1)
X_reduced = pca.fit_transform(X)
X_restored = pca.inverse_transform(X_reduced)

row_errors = np.sum((X - X_restored) ** 2, axis=1)

print("principal axis:", np.round(pca.components_, 3))
print("explained variance ratio:", np.round(pca.explained_variance_ratio_, 3))

for idx, reduced, restored, err in zip(sample_ids, X_reduced, X_restored, row_errors):
    print(
        idx,
        "reduced =", np.round(reduced, 3),
        "restored =", np.round(restored, 3),
        "row_error =", round(float(err), 3),
    )
```

```text
principal axis: [[0.894 0.449]]
explained variance ratio: [0.904]
A reduced = [-1.937] restored = [2.075 1.959] row_error = 0.027
B reduced = [-0.555] restored = [3.311 2.578] row_error = 0.413
C reduced = [0.54] restored = [4.29  3.067] row_error = 0.736
D reduced = [1.952] restored = [5.554 3.698] row_error = 1.727
```

这一次，D 的 `row_error` 最大。也就是说，只保留 1 个主成分时，D 那种错位的模式就无法被很好复原。这个 Python 例子直接说明了：`降维可以保住大的流向，但并不会把每个样本的细节都同样完好地保留下来。`

## 检查清单

- 你能不能说明，dimension 和描述数据的轴数量，也就是特征数量，是连在一起的？
- 你现在需要的，更接近重新建立表达，而不是先找分组吗？
- 你能不能把降维解释成更接近`重新建立表达的技术`，而不只是`删除特征的技术`？
- 你能不能说明第一成分抓的是大流向，第二成分抓的是剩下的差异？
- 你能不能把 eigenvector 连到`新轴方向`，把 eigenvalue 连到`这条轴解释了多少变动`？
- 你是否理解，降维会让表达更容易读，但一些细节差异可能会变弱？
- 就算降维后的表达看起来很方便，你是否准备回头检查原始特征里有没有重要差异被压掉？

## 出处与参考资料

- scikit-learn developers, `2.5. Decomposing signals in components (matrix factorization problems)`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/decomposition.html](https://scikit-learn.org/stable/modules/decomposition.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `PCA`, scikit-learn API Reference, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html){: target="_blank" rel="noopener noreferrer" }
