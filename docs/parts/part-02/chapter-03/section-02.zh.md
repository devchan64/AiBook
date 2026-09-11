# P2-3.2 向量空间(vector space)与位置的直觉

> Section ID: `P2-3.2`
> Version: `v2026.09.08`

把向量的各个值用作坐标，就能把向量放成空间中的一个点。使用相同坐标标准表示的向量，可以比较位置和距离。

## 三个向量的位置

把下面三个向量放到二维平面上。

\[
\mathbf{a} = [2,\ 3]
\]

\[
\mathbf{b} = [2.2,\ 3.1]
\]

\[
\mathbf{c} = [8,\ 1]
\]

从 `a` 移动到 `b`，第一个坐标变化 `0.2`，第二个坐标变化 `0.1`。从 `a` 移动到 `c`，两个坐标分别变化 `6` 和 `−2`。坐标图也显示，`a` 和 `b` 较近，`c` 则更远。

![向量空间中 a 和 b 更接近而 c 更远的坐标图](/AiBook/assets/part-02/chapter-03/vector-space-near-far-zh.svg)

## 比较位置的条件

| 基准 | 为什么重要 |
| --- | --- |
| 把向量读成位置 | 因为 embedding 和表示学习的说明经常使用坐标、位置、空间这套语言。 |
| 接近是相似的候选 | 因为它解释了为什么 similarity search 和 recommendation 会去找附近的向量。 |
| 只能在同一空间里比较 | 因为一旦维度和 shape 不同，就无法直接计算距离或相似度。 |

## 向量与坐标

一个包含两个值的向量可以读成两个坐标。

\[
\mathbf{x} = [2,\ 3]
\]

这个向量是一个含有两个值的列表。同时，它也可以被读成二维平面上某个点的坐标。此时，第一个值可以读成横向位置，第二个值可以读成纵向位置。

所以，\([2,\ 3]\) 可以读成向右移动 2、向上移动 3 后到达的位置。

当然，这并不意味着 `数字接近，意义就一定接近`。这还取决于这些值是怎样被做成有意义的表示、它们是如何被学习出来的、以及使用了什么距离或相似度标准。

## 相同空间与维度

在向量空间中，向量加法和标量乘法按确定的规则进行。比较坐标向量时，值的个数以及每个坐标的标准也必须一致。

例如，下面这些向量都包含两个值。

\[
[1,\ 2],\quad [3,\ 4],\quad [0,\ -1]
\]

它们可以被放进同一个二维空间。相反，如果是一个包含三个值的向量，就可以看成三维空间里的表达。

\[
[1,\ 2,\ 3]
\]

关键点在于：比较必须发生在同一个空间里。一个有两个值的向量和一个有三个值的向量，很难立刻用同样方式直接比较。

[1, 2] 与 [1, 2, 3] 长度不同，因此不能直接套用同一种位置比较或距离计算。

这也会连到代码里的 shape 问题。向量空间的直觉，最后会落到这样一种感觉上：`比较只能发生在同样规则和同样形状之内`。

## 加法、标量乘法与线性组合

向量空间的基本运算是加法和标量乘法。

- 向量之间可以相加。
- 一个数字可以乘到向量上。

第一个叫向量加法(vector addition)。

\[
[1,\ 2] + [3,\ 4] = [4,\ 6]
\]

第二个叫标量乘法(scalar multiplication)。这里的 scalar 就是一个数字。

\[
2[1,\ 2] = [2,\ 4]
\]

这两个运算重要，是因为它们能制造新向量。比如，可以把两个向量加在一起，或者把一个向量放大、缩小。

\[
0.5[2,\ 4] = [1,\ 2]
\]

这种“先把向量乘上数字，再加起来”的方式，叫作线性组合(linear combination)。

\[
2\mathbf{a} + 3\mathbf{b}
\]

这个式子表示：把向量 \(\mathbf{a}\) 乘 2，把向量 \(\mathbf{b}\) 乘 3，再把结果加起来。

例如，输入向量乘上权重、多个值相加变成新表示、向量表示被一点点调整，这些计算都建立在这样的视角之上。

回到共同场景，不只是 `a` 和 `b` 能拿来比较，我们也可以形成 `a + b` 这样的新表示，或者像 `2a` 那样改变大小。也就是说，向量空间既是比较的地方，也是构造新向量的计算场所。

## 坐标个数与高维

在下面的坐标向量中，分量的个数对应空间的维度。

\[
[2,\ 3]
\]

这个向量有两个值，所以可以读成二维向量。

\[
[0.1,\ 0.7,\ -0.2,\ 1.5]
\]

这个向量有四个值，所以可以读成四维向量。

在现实里，二维和三维比较容易画出来想象。但在 AI 里，几百维、几千维的向量也经常出现。例如，文本 embedding 可以把一句话或一个词表示成由大量数字组成的向量。

人很难直接把这么多维度画出来。但基础直觉仍然成立：每个维度都能像一个坐标那样使用，整个向量可以像一个位置那样被比较，而远近关系可以成为读取数据关系的线索。

不过，也不能断言每个维度都一定有一个人能立刻解释的意义。在训练得到的 embedding 里，每个数字不一定都有人工贴上的明确标签。

## 接近与相似性

在向量空间里，位置接近的向量可能对应相似的数据。这就是 embedding 与向量检索的核心直觉。

举个简单例子，想象一下只有两个特征的商品向量。

这里把第一个值看成价格档位，第二个值看成重量。

\[
\mathbf{p}_1 = [3,\ 2]
\]

\[
\mathbf{p}_2 = [3.1,\ 2.2]
\]

\[
\mathbf{p}_3 = [9,\ 8]
\]

\(\mathbf{p}_1\) 和 \(\mathbf{p}_2\) 的价格档位与重量都比较接近，因此这两个向量很可能彼此靠近。相对地，\(\mathbf{p}_3\) 可能会离它们更远。

这种直觉经常被用在 recommendation、search、classification 里。最后都会连到这样的问题：怎样找到相似用户、相似文档、相似图像、相似商品。

但接近只是候选，不是最终答案。我们仍然需要验证：究竟用什么标准定义“接近”、这些向量是怎样从数据里学出来的、以及在真实问题里这种接近是否真的有用。

## 位置与拓扑

这里说的位置(position)，是把向量像坐标一样放进空间、并用来思考远近的入门表达。相对地，拓扑(topology)是数学里更宽、更抽象的概念。它不只是谈一个点的坐标，而是涉及哪些点彼此接近、哪些结构彼此连通、以及如何看待 continuity 这样的性质。

在 AI 文档里，也可能会出现 `空间的拓扑`、`数据流形(manifold)`、`表示空间的结构` 这类说法。这些表达并不是只盯着某个向量坐标本身，而是更接近于讨论所有数据表示一起形成的整体连接关系和结构。

## 嵌入与文档检索

嵌入是一种把文本、图像、商品、用户等对象转成向量的表示。

一个对象经过 embedding 模型，会变成向量，而这个结果会被当成向量空间中的一个位置来处理。

例如，假设一句话被表示成下面这个向量。

\[
\mathbf{e} = [0.12,\ -0.03,\ 0.88,\ 0.41]
\]

很难说这个向量中的每个数字都对应一个人能直接读懂的词义。但整个向量仍然可以被当成那句话的一种表示(representation)。

一旦这个表示被放进向量空间，就可以和其他句子的向量进行比较。

如果把句子 A、句子 B、句子 C 的向量放在同一个空间里，我们就可以比较哪一句和哪一句更近。

文档检索使用同一个嵌入模型把问题和文档转成向量，再寻找与问题向量接近的文档向量。检索结果用作回答问题的候选资料。

## 表示学习与词向量研究

在表示学习与词向量研究中，数据表示与向量空间之间的关系也是重要主题。

Bengio、Courville、Vincent 关于表示学习的综述指出，机器学习算法的成功很大程度上依赖于数据表示。它还把表示学习、密度估计(density estimation)、流形学习(manifold learning)之间的几何联系当作重要问题提出。这为 `向量表示不仅仅是数字列表，还可能是揭示数据结构的一种表示` 提供了支持。

Mikolov、Chen、Corrado、Dean 的 word2vec 论文在大规模文本数据中学习了词的连续向量表示，并通过词相似性任务评估了表示质量。这展示了现代 NLP 的一个重要方向：即使是词这样的符号对象，也可以被转成向量空间里的表示，并比较这些向量之间的接近程度。

## 检查清单

- 能把向量解释成“值的列表”与“像坐标一样可读的表达”吗？
- 能把向量空间解释成摆放和比较向量的可计算空间吗？
- 能把维度(dimension)解释成向量里值的个数或坐标轴数量吗？
- 能说明靠近的向量会成为相似候选，但不自动等于答案吗？
- 能区分位置(position)、距离(distance)、拓扑(topology)，而不把它们混成同一个词吗？
- 能说明 embedding 是把对象转成向量空间内部表示的一种方式吗？
- 能说明为什么向量空间直觉会在 similarity search、RAG、recommendation、clustering 中再次出现吗？
- 能轻量解释 vector addition、scalar multiplication、linear combination 是向量空间的基本计算吗？
- 能把向量作为值列表的解释连接到位置与接近的视角吗？
- 能说明 embedding 和 similarity search 为什么要求在同一空间、同一维度里比较吗？

## 来源与参考资料

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, 确认日期: 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, 确认日期: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 确认日期: 2026-07-19.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, arXiv, 2012, 确认日期: 2026-07-19.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 确认日期: 2026-07-19.
- Google for Developers, [Embeddings: Embedding space and static embeddings](https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space){: target="_blank" rel="noopener noreferrer" }, Machine Learning Crash Course, 确认日期：2026-07-19. 这个官方教育资料把 embedding 解释为向量表示和 embedding 空间中的邻近位置。
- Google for Developers, [Measuring similarity from embeddings](https://developers.google.com/machine-learning/clustering/dnn-clustering/supervised-similarity){: target="_blank" rel="noopener noreferrer" }, Machine Learning Crash Course, 确认日期：2026-07-19. 这个参考资料支持用距离、余弦或点积来度量 embedding 向量相似度的连接。
