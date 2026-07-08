# P1-9.3 区分 LLM 的直接谱系与周边证据

> Section ID: `P1-9.3`
> Version: `v2026.07.07`

9.1 看的是图像识别与表征学习，9.2 看的是目标检测与语音生成。

现在需要把这些案例和 `LLM` 的历史谨慎地接起来。

这里的核心问题是：

> AlexNet、YOLO、WaveNet 这些案例，  
> 究竟是 LLM 的直接祖先，  
> 还是更适合被当作“深度学习范式广泛建立说服力的周边证据”？

> LLM 的直接谱系，  
> 更应该通过 language modeling、sequence modeling、Seq2Seq、Attention 和 Transformer 来解释；  
> 图像、目标检测和语音生成案例，更适合被放在周边证据的位置上。

这一节要区分 `direct lineage`、`surrounding evidence`、`language modeling`、`Seq2Seq`、`Attention` 和 `Transformer` 在 LLM 历史中的位置。9.1 和 9.2 的图像、检测与语音案例，不会被整理成“LLM 的直接祖先”，而是被整理成“深度学习范式扩散的背景”。真正直接的主线，会在 Chapter 11 到 Chapter 14 以及 Part 6 里继续展开。

这些历史词汇一开始很容易显得都差不多。先做一个快速分拆：

| 术语 | 极短含义 | 本节里的作用 |
| --- | --- | --- |
| direct lineage | 直接通向 LLM 核心结构的技术链路 | 判断什么对解释 LLM 必不可少 |
| surrounding evidence | 深度学习扩散时形成背景的案例 | 重要背景，但不是直接祖先 |
| language modeling | 建模下一个词或下一个 token 概率的问题 | LLM 直接主线的起点 |
| Seq2Seq | 把输入序列映射到输出序列的结构 | 直接谱系中的重要前阶段 |
| Attention | 在输出过程中更强地参考相关输入位置的结构 | Transformer 之前的重要转折 |
| Transformer | 以 Attention 为中心的序列建模结构 | 现代 LLM 的核心结构家族 |

最少要保留的区分是：

- LLM 的直接谱系属于语言建模这一边
- AlexNet、YOLO、WaveNet 属于周边证据
- Transformer 很核心，但它也不是全部历史

这里还有一个额外意图也很重要。现在很多人一听到“AI”，会立刻想到 LLM 或聊天机器人。这一节会刻意对这种缩写保持警惕。LLM 当然是理解现代 AI 的极重要技术，但如果把整个人工智能都缩成 LLM，那么规则式 AI、搜索、概率模型、计算机视觉、语音、强化学习、推荐系统和机器人等其他大线索就会从视野里消失。

## 本节范围

这一节不会完整书写 LLM 的全部细史。statistical language model、word embedding、RNN、LSTM、Seq2Seq、Attention、Transformer、pretraining、instruction tuning 和 RLHF，在这里只会被放在地图上的位置。更细的说明会从 Part 1 Chapter 11 到 Chapter 14，再到 Part 5 和 Part 6 展开。

因此，这一节在 P1-9 里只承担两个作用：

- 把 LLM 的 `direct lineage` 放在 language modeling 与 sequence modeling 一边
- 防止“AI 整体 = 只有 LLM”这种缩写吞掉其他主线

这里也不会深入解释 `tokenization`、`embedding` 或 `pretraining`。最重要的不是某一个结构细节，而是先建立一张图区分：

> 什么属于 direct lineage  
> 什么属于 surrounding evidence

这件事之所以必要，原因很简单：如果把所有深度学习成功案例都直接拉成一条通往 LLM 的直线，历史会显得很顺，但原因和背景就会混在一起。

## 本节目标

- 区分 direct lineage 与 surrounding evidence。
- 把 LLM 的直接主线放在 language modeling 与 sequence modeling 一边。
- 避免把 AlexNet、YOLO 和 WaveNet 夸大成 LLM 的直接祖先。
- 把 LLM 放回 AI 更大的地形图里，而不是把全部 AI 缩成 LLM。
- 把 Transformer 看成重要转折点，但不假装它单独就能解释完整的 LLM 历史。
- 为从 Chapter 11 到 Chapter 14，再到 Part 5 和 Part 6 的过渡建立一张更安全的地图。

## 三个基准

| 基准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| LLM 的 direct lineage 在 language modeling 与 sequence modeling 一边 | 这能防止图像和语音案例被过度贴进 LLM 的主线里。 | 理解真正直接的线索属于词、token 与语言序列模型即可。 |
| AlexNet、YOLO 和 WaveNet 属于 surrounding evidence | 这能保留深度学习扩散的重要性，又不夸大因果关系。 | 理解它们是在说明深度学习在多个领域建立了力量即可。 |
| 如果把 AI 全部缩成 LLM，其他重要主线就会被遮住 | 这能保持 Part 1 的整体地图不塌缩。 | 理解 LLM 是 AI 里的大流之一，而不是 AI 整体本身。 |

## 先分开：direct lineage 和 surrounding evidence

`direct lineage` 指的是：那些对解释 LLM 核心问题与核心结构“直接必需”的技术流。生成式 LLM 通常会把语言看成一串 `token`，根据前面的 `context` 计算下一个 token 候选的概率分布，并用学到的参数生成输出。

这里的 `token` 不一定等于人平常理解的“一个单词”。在 LLM 里，它指的是把文本切分后、模型可以处理的基本单位。tokenization 和 embedding 的更完整位置，会在 P1-11 到 P1-13 以及 Part 6 再回到。

> 文本  
> -> token  
> -> 下一个 token 的概率分布

这条线并不是和更早的概念完全断开。前面把 `symbol` 理解成可区分标记的视角，有助于理解 token；前面出现过的 `feature` 和 `representation`，也为 tokenization 和 embedding 这样的概念提供准备。但 9.3 的中心并不是 tokenization，而是：

> 先把 direct lineage 和 surrounding evidence 分开

因此，direct lineage 会连向这些问题：

> 词和句子应该怎样数值化？  
> 前面的词序列怎样帮助预测下一个词？  
> 长上下文里应该参考什么信息？  
> 这些结构怎样在大规模数据和大规模计算资源下被训练？

`surrounding evidence` 则指的是：虽然不直接决定 LLM 核心结构，但它们确实帮助深度学习作为一个研究方向在更多领域里变得更有说服力。

| 区分 | 核心问题 | 例子 |
| --- | --- | --- |
| direct lineage | 语言与序列数据应该如何建模？ | neural language model、Seq2Seq、Attention、Transformer |
| surrounding evidence | 深度学习为什么会在多个领域建立说服力？ | AlexNet、YOLO、WaveNet |

这里要强调的不是“周边证据不重要”。恰恰相反，它们很重要，因为它们显示了深度学习作为大方向是怎样逐渐被更多人接受的。

这个边界在反方向上也很重要：

> AI as a whole  
> -> LLM

这种缩写虽然很贴合今天的工具体验，但会让历史过度收缩。9.3 的目的不是把 LLM 看小，而是更清楚地看见：LLM 站在哪条直接技术线上，又是在什么更大的背景中长起来的。

## 那些更靠近 LLM 的材料应该放在哪里

很多材料看起来都像“LLM 的祖先”，但它们并不是以同样方式成为祖先的。

| 材料或路线 | 为什么和 LLM 接近 | 在本节中的位置 |
| --- | --- | --- |
| neural language models | 展示了用神经网络学习词序列概率与词表示的路线 | direct lineage 的起点 |
| word2vec | 强化了“词可以学成向量表示”这条线 | 表征学习与词嵌入的重要前阶段 |
| Seq2Seq | 展示了输入序列到输出序列的语言处理结构 | direct lineage |
| Attention | 展示了生成时按需参考相关输入位置的结构 | direct lineage |
| Transformer | 把 Attention 为中心的结构强力连接到大规模序列建模 | 现代 LLM 的核心结构家族 |
| ELMo | 引入了 contextualized word representation | 上下文化语言表征的重要前阶段 |
| ULMFiT | 展示了 pretrained language model 向下游任务 fine-tuning 的路线 | NLP transfer learning 的重要前阶段 |
| BERT | 强化展示了基于 Transformer 的 pretraining 与 fine-tuning | 现代语言表征模型的直接背景 |
| GPT 系列 | 直接展示了 Transformer decoder、language modeling、pretraining、generation、scaling 与 in-context learning 的路线 | 现代生成式 LLM 最接近的 direct lineage |

这张表不是想一次写完 LLM 全部历史。它只是在这里先固定一个边界：和图像识别、对象检测相比，语言建模、表征学习、pretraining 与 Transformer 家族研究，才更直接属于 LLM 的解释主线。

## direct lineage 1：language modeling

`language modeling` 是把词或 token 序列按概率方式处理的问题。Bengio 等人的工作把 statistical language modeling 的目标写成：学习语言中词序列的联合概率。那篇论文同时也强调了 distributed representation，可以帮助缓解维度灾难。

入门层面的基线可以压成这样：

> 语言模型不是从“它已经理解了整句话”开始的。  
> 它先从“一个词序列有多像合理语言”  
> 以及“接下来最可能出现什么”这种问题开始。

这里的 `probability` 并不是“总能给出唯一正确答案”，而是给不确定候选打分。它和第 6 章里对 probability、uncertainty 和 stochastic 的说明可以连起来。

## direct lineage 2：Seq2Seq

`Seq2Seq` 指的是：接收一个输入序列，再生成一个输出序列。最典型的例子是机器翻译。现代 LLM 并不等于“全部都是 Seq2Seq 结构”，但 Seq2Seq 是理解语言如何被当成“序列输入 + 序列输出”学习问题的重要前阶段。

Sutskever、Vinyals 和 Le 的 Seq2Seq 论文表明，LSTM 可以解决一般 sequence-to-sequence 问题，并展示了用大型 deep LSTM 做英法翻译。

入门层面的核心直觉是：

> 先读完整个输入句子，  
> 再把它变成内部表征，  
> 然后依据这个表征一步步生成输出句子。

这本身还不是现代 LLM 本体，也不是所有 LLM 的最终直接结构。但它展示了一条重要路线：语言不再只是靠固定规则列表处理，而是可以通过神经网络学习输入句子和输出句子的对应关系。

## direct lineage 3：Attention

早期 encoder-decoder 有一个问题：如果把很长的句子都压进一个固定长度向量里，就容易产生信息瓶颈。

Bahdanau、Cho 和 Bengio 的 Attention 论文，正是为了缓解这个问题：在生成输出的每一步，都更强地参考输入句子里当前真正相关的部分。论文里也明确说明，decoder 会学习自己该把注意力放到 source sentence 的哪些位置上。

这里最安全的直觉是：

> 生成每个输出词时，  
> 模型不再只依赖一个把整句揉成一团的固定记忆；  
> 它会更强地参考当前真正相关的输入位置。

这里的 Attention 不应该被读成“像人类一样有意识地集中注意”。更安全的读法是：模型内部会按位置计算权重，并更强地使用那些相关位置信息。

## direct lineage 4：Transformer

`Transformer` 是 Attention 这条线上的重大转折点。Vaswani 等人指出，早期强大的 sequence transduction 模型通常依赖 recurrent 或 convolutional neural network，而他们提出的 Transformer 则把 recurrence 和 convolution 拿掉，转而以 Attention 为核心。

这里最重要的是两点：

| 视角 | 含义 |
| --- | --- |
| self-attention | 同一序列里的各个位置会相互参考来形成表示 |
| parallelization | 减少像 RNN 那样必须严格逐步处理的负担，更利于大规模训练 |

Transformer 论文说明，sequence transduction 可以只靠 Attention 实现，而不依赖 recurrence 和 convolution，并且这种结构更容易并行化。

但这里仍然要避免过度缩短成一句：

> Transformer -> 现代 LLM

这样太短了。现代生成式 LLM 更应该被理解成：Transformer 家族结构，加上大规模数据、pretraining、tokenization、scaling、训练稳定化，以及在不同研究与产品路线里加入 instruction tuning 或 RLHF 等 alignment 方法的结果。

## surrounding evidence 让深度学习更有说服力

9.1 和 9.2 里的案例，更安全的放法是：把它们作为“深度学习在多个领域广泛扩散”的 surrounding evidence，而不是直接写成 LLM 的祖先。

| 案例 | 属于 direct lineage 吗？ | 在本章里的作用 |
| --- | --- | --- |
| AlexNet | 否 | 展示图像识别里大数据、深层 CNN、GPU 与训练技术结合的转折点 |
| YOLO | 否 | 展示目标检测如何被重构成单一神经网络预测问题 |
| WaveNet | 否 | 展示 raw audio 如何被处理成概率式序列生成问题 |

这样就能写出一句更安全的话：

> LLM 不是直接从图像识别或目标检测里长出来的。  
> 但 2010 年代深度学习在多个领域连续成功，  
> 强化了人们对大规模数据、计算资源、表征学习和端到端训练的信心。  
> 在这种背景下，language modeling 与 Transformer 家族研究才更强地成长起来。

## 一些必须避免的缩写

下面这些缩写尤其危险：

| 应避免的缩写 | 问题 | 更安全的说法 |
| --- | --- | --- |
| AI 就等于 LLM | 其他研究路线和应用领域会被抹掉 | LLM 是现代 AI 中的重要大流，但不等于 AI 整体 |
| AlexNet 造就了 LLM | 图像分类和语言建模的直接谱系被混在一起 | AlexNet 是深度学习扩散的代表性转折点 |
| YOLO 推动了 LLM 发展 | 对象检测模型被误写成直接祖先 | YOLO 是目标检测里端到端重构的案例 |
| WaveNet 是 LLM 祖先 | 音频波形生成和语言建模被混淆 | WaveNet 是概率式序列生成的周边案例 |
| 只要知道 Transformer 就能解释 LLM 全史 | pretraining、数据、scaling 和 alignment 全部消失 | Transformer 很核心，但完整历史更宽 |

这一章真正想给出的解释不是：

> 一切都沿直线通向 LLM

而是：

> 深度学习通过学习表征、预测或生成输出，扩散到了很多领域；  
> 而 LLM 则是在语言建模与序列建模的直接主线上成长起来的。

## 本节要记住的观点

解释 LLM 历史时，必须把 `direct lineage` 和 `surrounding evidence` 分开。direct lineage 包括 language modeling、Seq2Seq、Attention 和 Transformer，因为这些结构直接处理语言与序列数据。surrounding evidence 则包括 AlexNet、YOLO 和 WaveNet，因为这些案例帮助研究界和工业界更广泛地接受大规模神经网络方法。

这种区分不是为了否定前面的直觉，而是为了把那种直觉改写成更安全的说明句。

> generative AI 和 LLM 并不是凭空出现的。  
> 但它们的 direct lineage 应该在 language modeling 与 sequence modeling 的发展线上去找，  
> 而不是在图像分类或对象检测上直接去找。  
> 图像、语音和检测案例更适合被当作深度学习范式扩散的背景来读。

读完这一节后，至少应保留这三条区分：

| 应保留的关键区分 | 为什么重要 |
| --- | --- |
| LLM 的 direct lineage 位于 language modeling、Seq2Seq、Attention 和 Transformer 一边 | 这样后面的 LLM 说明就不容易和图像、语音案例混成一团 |
| AlexNet、YOLO、WaveNet 更接近 surrounding evidence，而不是 direct ancestors | 这样能把深度学习的广泛成功与 LLM 的直接历史区分开，又不夸大 |
| 把 AI 全部缩成 LLM 会遮住其他重要主线 | 这样既能保住 Part 1 的整体地图，也能更稳地过渡到 Part 6 的 LLM 主线 |

## 来源与参考资料

- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://jmlr.org/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, 确认日期：2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 确认日期：2026-06-23.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, 确认日期：2026-06-23.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, 确认日期：2026-06-23.
- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, 确认日期：2026-06-23.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 确认日期：2026-06-23.
- Jeremy Howard, Sebastian Ruder, [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 确认日期：2026-06-23.
