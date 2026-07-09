# P1-11.1 统计语言模型(statistical language model)与嵌入(embedding)

> Section ID: `P1-11.1`
> Version: `v2026.07.09`

在第 10 章中，我们看到生成式 AI(generative AI)在产出内容时，必须把自然度、事实性、依据与风险分开审查。

现在把问题再往前推一步：

> LLM 是从哪里来的？

这里不会直接用 Transformer 来解释 LLM(large language model)。我们先看在 LLM 之前处理语言的两条脉络：

> 把语言当作概率来处理的脉络  
> 把语言表示成向量的脉络

这两条脉络结合起来，就会出现这样的视角：

> 语言模型会以概率方式处理单词和 token 的顺序，  
> 嵌入则把单词和 token 变成可计算的向量表示。

在 Part 1 中，本节先建立 `语言模型(language model)`、`统计语言模型(statistical language model)`、`n-gram`、`数据稀疏性(sparsity)`、`分布式表示(distributed representation)`、`嵌入(embedding)`、`word2vec` 之间的基本区分。`直接谱系(direct lineage)` 与 `语言建模(language modeling)` 的整体地图已经在 9.3 中先铺过，`生成下一个输出` 的直觉也已在 10.2 中看过。这里会从 `LLM 之前的语言模型` 与 `向量表示` 的层面重新开始。

## 本节范围

这里不会讲完整的 LLM 历史。RNN(recurrent neural network)、LSTM(long short-term memory)、Seq2Seq(sequence-to-sequence)、Attention、Transformer 会在 11.2 与 11.3 中继续讨论。

`语言模型`、`n-gram`、`稀疏性`、`分布式表示`、`嵌入`、`word2vec` 在开始时都可能听起来像类似的 NLP 基础术语。先简短区分一下各自的作用：

| 术语 | 极简含义 | 本节中的作用 |
| --- | --- | --- |
| 语言模型 | 处理下一个单词或 token 出现可能性的模型 | 第 11 章的起点 |
| n-gram | 观察相邻 n 个单位的短上下文模型 | 早期统计方法的代表 |
| 稀疏性 | 稀有组合太多，导致概率难以估计的问题 | n-gram 的核心限制 |
| 分布式表示 | 用多个数值维度共同表示一个词的方式 | 把符号表示转成向量表示的视角 |
| 嵌入 | 把单词或 token 放进稠密向量中的表示 | 后续 LLM 计算的输入基础 |
| word2vec | 让嵌入广为人知的代表性学习方法 | 分布式表示的实用案例 |

这里至少要保留的区分是：`语言模型处理下一个词的概率`、`n-gram 使用短上下文`、`嵌入是向量表示`。

这里主要聚焦三件事：

| 主题 | 本节要看的问题 |
| --- | --- |
| 语言模型(language model) | 如何根据前面的单词计算下一个单词的可能性？ |
| n-gram 语言模型(n-gram language model) | 如何用短上下文中的频率来估计下一个单词的概率？ |
| 嵌入(embedding) | 如何把单词和 token 放进向量空间(vector space)？ |

本节的目的不是“把公式完全学会”。更重要的是抓住这样一种思维方式：为什么把语言当作 `概率` 与 `向量` 来处理，会一路延伸到 LLM。

另外，这里还不会解释 RNN、Attention、Transformer。那些结构上的发展脉络会在 11.2 与 11.3 单独展开；这里先专注于两个起点：`用概率处理语言` 和 `把单词转成向量`。

## 本节目标

- 把语言模型(language model)理解成处理下一个单词或下一个 token 概率的模型。
- 看到 n-gram 语言模型使用短上下文和频数(count)。
- 理解 n-gram 的限制与数据稀疏性(sparsity)、上下文长度、词语相似性问题有关。
- 把分布式表示(distributed representation)与嵌入(embedding)理解成用向量表示单词的方法。
- 区分嵌入不是词典式定义，而是从数据中的使用上下文学到的表示。
- 不把 LLM 看成“突然出现的聊天机器人”，而是放在语言建模与向量表示不断积累的脉络中理解。

## 三个基准

这里不会马上把 LLM 讲成 Transformer，而是先恢复它之前的语言处理思路。只要抓住下面三个基准，整体脉络就会清楚。

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| 语言模型处理的是下一个单词或 token 的可能性 | 这能显示 LLM 最基础的问题是什么。 | 只要理解成它会根据前文估计下一个词有多合理即可。 |
| n-gram 试图用短上下文的频率来处理语言 | 这能同时展示早期语言模型的优点与限制。 | 只要知道它是看附近几个词来估计下一个词即可。 |
| 嵌入是把单词表示成向量的方式 | 这会连接到后面的 token、表示、向量检索说明。 | 只要理解成它把单词变成可计算的位置，而不是只保留字典解释即可。 |

## 语言模型从预测下一个词的问题开始

语言模型(language model)是为句子或词序列(word sequence)赋予概率，或者根据前面的上下文(context)来计算下一个单词或 token(token) 出现可能性的模型。

例如看下面这个句子：

> 我早上会喝热 ___

人通常会想到 `咖啡`、`茶`、`汤`、`水` 之类的候选项。`汽车` 或 `法院` 在语法上未必完全不可能，但在一般语料(corpus)里，它们与前面的上下文往往不太搭。

语言模型会把这种直觉变成计算问题：

> P(咖啡 | 我早上会喝热 ...)  
> P(茶 | 我早上会喝热 ...)  
> P(汽车 | 我早上会喝热 ...)

这里重要的是，语言模型一开始并不会直接宣称自己“理解了意义”。它先处理的是：在观察到的语言数据中，哪些词序列更合理，接下来哪个词更可能出现。

## n-gram 用短上下文来近似概率

n-gram 是由连续 n 个单位构成的序列。这个单位可以是字符(character)、单词(word)或 token(token)。这里把它理解成单词级 n-gram 就够了。

> unigram: 我  
> bigram: 我 / 喝  
> trigram: 我 / 喝 / 咖啡

n-gram 语言模型(n-gram language model)不会使用全部历史上下文，而是用较短的前文来近似估计下一个词的概率。例如 bigram 模型只看紧挨着的前一个词。

> 完整上下文：  
> 我早上会喝热 ___
>
> bigram 近似：  
> 热 ___

我们做一个很小的例子：

> 我喝咖啡  
> 我喝茶  
> 我喝咖啡在早上

如果统计 `喝` 后面出现了什么，就会得到：

| 前一个词 | 下一个词 | 次数 |
| --- | --- | ---: |
| 喝 | 咖啡 | 2 |
| 喝 | 茶 | 1 |

那么一个简单的 bigram 概率可以理解成：

```text
P(咖啡 | 喝) = 2 / 3
P(茶 | 喝) = 1 / 3
```

这个例子对真实语言模型做了很多简化，但核心很明确：

> 它不再只是把句子当作规则清单来处理，  
> 而是根据语料中观察到的频率，  
> 去计算下一个词的可能性。

## n-gram 的限制是 LLM 之前的重要问题

n-gram 是一个直观而强的起点，但它也有明显限制。

第一，上下文太短。bigram 只看前一个词，trigram 只看前两个词。虽然把 n 变大能看到更长上下文，但所需组合数量会急剧增长。

第二，会出现数据稀疏性(sparsity)。真实句子非常多样。训练语料里从未出现过的词组合，看起来就可能像是概率为 0。因此，早期语言建模需要 smoothing、backoff、interpolation 之类的方法。

第三，它不太擅长在相似词之间做一般化。

> 猫喝牛奶  
> 狗喝牛奶

人会利用 `猫` 和 `狗` 都是动物这一点，推测类似上下文。但简单的 n-gram 并不会自动共享这种相似性，因为它主要围绕观察到的字符串组合做计算。

这些限制正好解释了为什么后来会需要神经语言模型(neural language model)与嵌入(embedding)。

## 分布式表示把单词放进向量里

分布式表示(distributed representation)不会只把一个单词看成单独的符号，而是把它表示成由多个数值构成的向量(vector)。

最简单的符号表示是 one-hot 表示(one-hot representation)：

```text
词表:
[猫, 狗, 咖啡, 茶]

猫:
[1, 0, 0, 0]

狗:
[0, 1, 0, 0]
```

one-hot 表示擅长区分不同单词，但不会直接表达 `猫` 比 `咖啡` 更接近 `狗` 这样的信息。

嵌入(embedding)会把单词表示成更低维的稠密向量(dense vector)：

```text
猫   -> [0.21, -0.08, 0.77, ...]
狗   -> [0.19, -0.05, 0.73, ...]
咖啡 -> [-0.44, 0.62, 0.10, ...]
```

这些数字本身不需要人直接读懂。重要的是：在相似上下文中使用的词，可能会在向量空间里靠得更近。

> 在相似上下文中被使用  
> -> 学成相似的向量表示  
> -> 模型就能在相似词之间进行一般化

## word2vec 是让嵌入广为人知的案例

word2vec 是让词嵌入(word embedding)被广泛认识的重要案例。Mikolov 等人在 2013 年的论文中提出了从大规模数据中高效学习连续向量表示(continuous vector representation)的方法。

最有代表性的两种方式是：

| 方式 | 直觉 |
| --- | --- |
| CBOW(continuous bag-of-words) | 根据周围单词预测中间单词。 |
| Skip-gram | 根据当前单词预测周围单词。 |

例如有这样一句话：

> 我早上喝咖啡

CBOW 可以理解成：根据 `我`、`早上`、`喝` 这类周边信息来猜 `咖啡`。Skip-gram 则反过来：根据 `咖啡` 去预测周围可能出现哪些词。

这里关键在于，它并不是把“词典里的定义”直接输入给模型。模型是通过观察单词在什么上下文里一起出现，来学习向量表示的。

所以更安全的说法不是：

> 由人直接定义每个词的意思

而是：

> 观察单词出现的上下文，  
> 在向量空间里学出对计算有用的位置

## 这不是与符号主义断裂，而是层级(level)不同

这里需要小心看待它与符号主义 AI(symbolic AI)之间的关系。

嵌入并没有消灭符号。文本仍然会被切成单词、子词、token 这样的可区分单位，这些单位依然在词表(vocabulary)中被识别。不同的是，模型内部不再只把这些单位当作 one-hot ID，而是把它们转成可计算的向量表示。

> 符号或 token：  
> 可区分的输入单位
>
> 嵌入：  
> 把这个单位转成可计算向量的表示

因此，更安全的说明是：

> LLM 不是简单地替代了符号主义 AI。  
> 它仍然会把文本中的符号单位区分成 token，  
> 再把这些 token 转成向量表示，  
> 用于概率式语言建模。

这也会和前面讲过的符号(symbol)、标签(label)、特征(feature)、表示(representation)接起来。只是嵌入不是人写好的意义表，而是从数据里学到的数值表示。

## 通往 LLM 的连接

现代 LLM 继承了本节的两条脉络：

| 之前的脉络 | 在 LLM 中延续的视角 |
| --- | --- |
| 语言建模(language modeling) | 计算下一个 token 候选项的概率分布。 |
| n-gram 的限制 | 需要更长上下文和更强的一般化能力。 |
| 分布式表示(distributed representation) | 把 token 表示成向量，供模型内部计算使用。 |
| 嵌入(embedding) | 先把输入 token 送入嵌入空间，再经过多层计算。 |

不过，现代 LLM 的嵌入并不能只用 word2vec 这种静态嵌入(static embedding)来解释。在 Transformer 系列模型中，会随着上下文改变的上下文化表示(contextual representation)更重要。这部分内容会在 11.3 和 Part 5 里再讲。

这里先记住这条连接：

> n-gram：  
> 用短上下文的频率预测下一个词
>
> 神经语言模型：  
> 同时学习词表示和下一个词的概率
>
> 嵌入：  
> 把单词和 token 放进向量空间，提高一般化能力
>
> LLM：  
> 利用大规模数据和神经网络结构  
> 在更长上下文中计算下一个 token 的分布并生成输出

## 本节应记住的视角

LLM 不是突然出现的聊天机器人。它可以被理解为建立在以下脉络之上：语言建模(language modeling)把语言作为概率问题来处理，n-gram 用短上下文做统计，嵌入(embedding)把单词转成向量，而神经语言模型试图把单词表示与概率函数一起学出来。

> 语言模型问的是“下一个词有多可能出现”。  
> n-gram 用短上下文与频率来回答。  
> 嵌入把词放进向量空间。  
> LLM 则在这些积累之上继续发展。

这样理解，就不会把 LLM 看成无缘无故突然出现的系统，而会把它放在一条逐步累积起来的研究链条里。

## 检查清单

- 我可以把语言模型(language model)解释为处理下一个单词或 token 概率的模型。
- 我可以说明 n-gram 语言模型利用短上下文和频率来估计下一个单词的概率。
- 我可以说明 n-gram 的限制与稀疏性、上下文长度和弱一般化有关。
- 我可以把分布式表示(distributed representation)与嵌入(embedding)解释为用向量来表示单词的方式。
- 我可以说明嵌入不是词典定义，而是从使用上下文中学到的表示。
- 我可以把 LLM 放在语言建模与向量表示不断积累的脉络中理解。

## 什么时候要先想起这个视角

当 LLM 的来源被过度简化成“Transformer 突然出现”，需要重新恢复它之前的语言处理思路时，就可以先想起本节。

- 当需要重新说明语言模型为什么会从“预测下一个词”这个问题出发时
- 当需要整理 n-gram 如何用短上下文做估计、又为什么会遇到限制时
- 当需要说明嵌入为何能把单词从离散符号转成可计算表示时

此时可以先把 `下一个词的概率`、`短上下文频率`、`向量表示` 分开来看。这样更容易理解为什么现代 LLM 会建立在这些前提之上。

## 来源与参考资料

- Yoshua Bengio et al., [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, 确认日期: 2026-06-23.
- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 确认日期: 2026-06-23.
- Tomas Mikolov et al., [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 确认日期: 2026-06-23.
- Chris Manning, Hinrich Schutze, [Foundations of Statistical Natural Language Processing](https://web.stanford.edu/~jurafsky/fsnlp/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 1999, 确认日期: 2026-06-23.
