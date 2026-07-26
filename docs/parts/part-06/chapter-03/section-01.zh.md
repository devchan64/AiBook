# P6-3.1 把 token ID 变成可比较坐标的 embedding

> Section ID: `P6-3.1`
> Version: `v2026.07.26`

在 P6-2 章中，我们看到 LLM 会以 token 为单位读取文本，而且 token 长度会直接连接到成本和上下文长度。可是仅靠 token 编号，模型无法计算意义，所以 token 很快必须变成另一种数值表达。

被分成 token 的输入，在模型内部会变成什么样的数字表达？embedding 是把 token 或句子转换成模型可以计算的向量(vector)的表达方式。

这里首先要分开的，是`赋予编号`和`转换成可比较坐标`。token ID 是指向 vocabulary 中某个项目的编号，而 embedding 向量是让这个项目可以和其他表达比较、计算的坐标表达。

## 从 token 编号到向量表达

第一次阅读 embedding 时，先抓住下面几个问题。

- embedding 是为了什么而存在的表达？
- token ID 和 embedding 向量有什么不同？
- `相似意义会变近`这句话可以用什么直觉来说明？
- 为什么 embedding 看起来像 LLM 和检索服务的共同基础？

这里先把 embedding 抓成`把 token 或句子转换成可计算向量表达的基础`。不同家族的学习背景、快速检索结构、RAG 连接会在后续小节更广地处理，但现在需要的起点，是 token ID 和向量表达为什么不同。

embedding 不是`像魔法一样保存意义的仓库`。它是把文本放进模型可以计算的空间中的表达方式。核心是从 token 编号本身包含意义的想法中离开，理解它会变成后续计算可以使用的向量表达。

| 当前阶段的焦点 | 已经抓住的内容 | 后续会连接的内容 |
| --- | --- | --- |
| 模型内部表达层位 | token 与 tokenization | 语义距离、向量检索、RAG 的基础 |

## 区分 token ID 与 embedding 向量

如果前面的 P6-2 章已经抓住了`token 是什么`和`长度与成本为什么重要`，现在就需要知道这些 token 怎样变成向量，并连接到模型计算和检索。这里需要的理解，不是先背复杂公式，而是把`token ID`、`embedding 向量`、`向量之间的比较结果`读成不同层位。

## token ID 和 embedding 有什么不同

tokenization 结束后，文本首先可以变成 token ID 这样的离散编号(discrete index)。

例如：

- `"AI"` -> `1042`
- `"model"` -> `3881`

这些数字本身几乎没有意义。它们只是 vocabulary 中指向项目的编号。

embedding 会从这里再往前走一步。它把每个 token 转换成由多个数字组成的向量。

直觉上可以像下面这样理解。

```text
token id 1042 -> [0.12, -0.08, 0.44, ...]
token id 3881 -> [0.09, -0.02, 0.39, ...]
```

也就是说：

- token ID 是`指向它是什么的编号`
- embedding 向量是`用于计算的数值表达`

## 为什么要变成向量

Part 5 中看到的 Transformer 会计算 token 之间的关系。但关系计算不是在文本字符串本身上进行，而是在数字向量上进行。

embedding 必要的理由如下。

- 必须能够做数值运算
- 必须能把 token 之间相似的用法在某种程度上放到相近位置
- 必须能连接到 attention、similarity search、classification head 等后续计算

可以这样理解。

`embedding 是把 token 转换成模型计算可以使用的坐标的阶段。`

## `相似意义会变近`是什么意思

这个表达很常见，但也很容易被误解。

更安全的说明如下。

`在相似上下文中经常使用，或者承担相似角色的表达，在学得的 embedding 空间中可能变成更近的向量。`

例如：

- `car` 和 `automobile`
- `文档摘要` 和 `生成摘要`

这类表达即使并不完全相同，只要在相似上下文中使用过，就可能变近。

但这不是绝对规则。embedding 会随着训练数据、模型结构、目标函数而变化。因此把`接近 = 完美理解意义`来读是危险的。

## 为什么在 LLM 和检索中都显得重要

embedding 在 LLM 内部计算和检索服务两边都扮演重要角色。

### LLM 内部

- 把 token 转换成向量
- 把这些向量用于 attention 和 feed-forward 计算

### 检索和 RAG

- 把问题和文档转换成向量
- 找到接近的文档，再提供给 LLM

也就是说，embedding 既是`生成模型的内部表达`，也是`检索系统的比较表达`。

## 极简图示

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s01-embedding-flow-zh.mmd"
```

这个图中要确认的结果是，embedding 不是直接给出最终答案的功能，而是把输入移到向量空间中，让后续相似度检索和表达比较等计算成为可能的起点。

## 案例与示例

下面的图把本节三个案例重新捆到同一个共同问题下：不是`是否原样读取字符串`，而是`表达会变成怎样的比较坐标`。

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s01-embedding-use-cases-zh.mmd"
```

这个图中要确认的是，即使任务不同，首先需要的阶段也相同。它们都不是直接计算字符串本身，而是先把 token 或句子移到`可比较的向量坐标`，然后下一步计算才开始。

### 案例 1. 语言模型内部表达

想象用户正在读一份包含 `foundation model` 和 `model card` 的文档。人很容易一看到同样拼写的 `model`，就觉得意义已经确定。但在实际上下文中，一个指向整个模型家族，另一个指向模型说明文档，所以角色会因旁边的词而改变。

反过来，也可能有 `system` 或 `architecture` 这样拼写不同，却经常在相似说明上下文中一起出现的表达。只抓住字符串，很难用数值计算处理这些关系。模型把 token 转换成 embedding 向量，建立同一上下文中一起出现的程度、与其他 token 的距离、attention 计算需要的比较标准之后，才进入下一阶段。

这里改变的标准，是从`读取单词`移动到`把单词放到可计算坐标中`。模型与其像词典释义那样固定地读单词，不如说会根据它在什么上下文中和什么一起使用，把它放到可计算坐标中。所以像 `model` 这样同样拼写的词，如果周围线索不同，可能被放进不同关系；反过来，拼写不同但经常在同一说明流中出现的词，也可能聚到更近的坐标。

即使是同一个词或不同词，比较标准也会随上下文不同而变化。

| 表达场景 | 人眼首先看到的东西 | embedding 视角重新看的东西 |
| --- | --- | --- |
| `foundation model` 中的 `model` | 同样拼写 `model` | 指向整个模型家族的上下文关系 |
| `model card` 中的 `model` | 仍然是同样拼写 `model` | 模型说明文档这个不同角色关系 |
| `system`、`architecture` 这样的不同拼写 | 表面上不同的单词 | 在相似说明上下文中一起出现的关系 |

这张表纠正的误解是`拼写相同，计算上的意义也几乎相同`这种期待。embedding 会把上下文中的关系做成比表面拼写更直接的比较标准。

这个案例中要收住的判断很明确。token ID 可以指向同一个字符串，但后续计算会在和周边上下文一起形成的向量关系上继续进行。

### 案例 2. 句子检索

用户可能问`prompt 的限制是什么`，而文档中写的是`仅靠 prompt 能否保证事实性`。人通常会觉得同一主题需要重复同样的词。所以如果只用字符串匹配，问题中没有出现很多同样词的文档很容易被推到后面。

但这两个句子都处理同一个问题场景：`仅靠 prompt 是否足够`。这里改变的标准，不是看单词是否完全一样，而是比较它们是否指向同一说明流和问题场景。基于 embedding 的检索会把问题和文档放到同一向量空间中，即使表面词不同，也能把方向相似的句子找近。需要 embedding 检索，不是为了背更多词，而是为了更直接比较问题和文档是否指向同一个问题场景。

同一个检索场景，也会因为标准不同而得到不同候选。

| 问题与文档关系 | 字符串标准容易先漏掉的东西 | embedding 标准更想先抓住的东西 |
| --- | --- | --- |
| 问题：`prompt 的限制是什么` | 没有 `限制` 这个词的相关文档 | `仅靠 prompt 是否足够`这个同一问题场景 |
| 文档：`仅靠 prompt 能否保证事实性` | 表面单词不完全相同，可能被推后 | 同一说明流和限制讨论 |
| 问题和文档只是表达不同 | keyword 重叠看起来少 | 同方向的向量关系 |

这个案例中的重要标准，是分开看`有没有同样的词`和`是不是在谈同一个问题`。embedding 在句子检索中重要，是因为这两者在实际中经常错开。

这个案例中要收住的判断，是检索结果的意义。接近的向量候选不是答案确认，而是可能处理同一问题场景的一次候选。怎样验证这个候选并把它作为依据接上，会在后面的向量检索和 RAG 小节再看。

### 案例 3. 推荐与相似度比较

假设一个视频服务想推荐相似课程。人很容易认为标题中相同单词多的课程就是相似课程。但即使标题都包含`入门`，一个可能以数学为中心，另一个可能以实践为中心；反过来，标题不同，观众实际也可能连续观看同一类型课程。

如果只比较标题字符串，很容易错过这种差异，让推荐偏离。这里改变的标准，不是数标题文字，而是把实际消费流和课程性质一起放到同一个比较坐标系中。此时如果把课程说明、观看模式、缩略图特征等信息一起放进 embedding 空间，就能在一个比较坐标系中处理不同信号。

结果是，推荐器可以把`实际一起被消费的课程`放到`字面相似的课程`之前。这个案例中要确认的结果，是实际学习流相似的课程是否比标题单词相同的课程更集中地出现在推荐上方。

把三个案例重新用表达坐标视角捆起来，可以写成下面这样。

| 情况 | 只看表面字符串容易漏掉的东西 | embedding 坐标中更想看到的东西 |
| --- | --- | --- |
| 语言模型内部表达 | 同样拼写也可能因上下文承担不同角色 | 在同一上下文中一起使用的关系 |
| 句子检索 | 问题词没有原样出现就漏掉相关文档 | 处理同一问题场景的句子接近性 |
| 推荐与相似度比较 | 标题词相同，实际消费流也可能不同 | 实际使用模式和性质的相似性 |

这个案例中要收住的判断也相同。embedding 不是推荐的最终答案，而是缩小候选的表达基础，候选之后还会通过过滤器和政策判断再次筛选。

## 区分编号、坐标、比较结果

读完本节后，即使还不知道复杂向量公式，也可以按下面例子先区分`现在看到的是编号、坐标，还是比较结果`。

| 现在看到的值 | 首先容易想到的误解 | embedding 视角中先要换成的问题 |
| --- | --- | --- |
| 一个 token ID | 容易觉得这个数字本身含有意义 | 这个值只是 vocabulary 中的编号，还是可比较坐标 |
| 一行 embedding 向量 | 数字很多，容易当作复杂内部值跳过 | 这个向量怎样用于和其他表达比较距离或方向 |
| 两个句子接近的结果 | 容易以为只是同样词很多 | 是否是比表面词更接近的上下文和角色被读近了 |

这张表中重要的不是预先猜对数值答案。首先需要的是区分`我看到的是编号`、`我看到的是表达坐标`、`我看到的是候选比较结果`。

经常混在一起的层位也正是这三个。

- 看到 token ID 时，容易觉得意义比较已经开始。
- 看到 embedding 向量时，容易觉得它太像内部值而跳过。
- 看到`接近`结果时，容易马上把它当作答案。

要阅读意义和距离、RAG、向量检索说明，必须先能分开这三个层位。

## 练习与示例

这个练习的目标，是区分`token ID 只是编号，实际比较发生在 embedding 向量上`。先用 Python 确认 ID 顺序和向量距离顺序不同的场景，然后再用手读同一组值。

### 示例. 比较 ID 顺序和向量距离顺序

这个示例不是训练真实 LLM embedding 的代码。它用 `numpy` 数组制作一个小表达表，查看项目 ID 的数字顺序和接近 query vector 的顺序怎样不同。直接操作的值是 `query_vector` 和 `embeddings`。改变这些值，距离顺序和最近表达项目也会改变。

```python
# 确认 token ID 数字顺序和 embedding 向量距离顺序不同的示例。
import numpy as np

token_ids = {
    "prompt_limit_phrase": 1042,
    "factuality_risk_phrase": 3881,
    "vector_search_phrase": 2210,
}

# 操作变量：改变表达向量或 query_vector，邻近项目顺序会改变。
embeddings = {
    "prompt_limit_phrase": np.array([0.12, -0.08, 0.44]),
    "factuality_risk_phrase": np.array([0.09, -0.02, 0.39]),
    "vector_search_phrase": np.array([-0.30, 0.11, 0.15]),
}
query_vector = np.array([0.10, -0.01, 0.41])

def squared_distance(a, b):
    return float(np.sum((a - b) ** 2))

id_order = sorted(token_ids.items(), key=lambda item: item[1])
distance_order = sorted(
    (
        (name, token_ids[name], squared_distance(query_vector, vector))
        for name, vector in embeddings.items()
    ),
    key=lambda item: item[2],
)

print("ID order:")
for name, token_id in id_order:
    print(name, token_id)

print("\nVector distance order:")
for name, token_id, distance in distance_order:
    print(name, "token_id=", token_id, "distance=", round(distance, 3))
```

执行结果示例如下。

```text
ID order:
prompt_limit_phrase 1042
vector_search_phrase 2210
factuality_risk_phrase 3881

Vector distance order:
factuality_risk_phrase token_id= 3881 distance= 0.001
prompt_limit_phrase token_id= 1042 distance= 0.006
vector_search_phrase token_id= 2210 distance= 0.242
```

这个输出中要看的值，是 `ID order` 和 `Vector distance order` 不同。ID 最小的项目是 `prompt_limit_phrase`，但和 query vector 最近的项目是 `factuality_risk_phrase`。因此 token ID 是识别用编号，而 embedding 向量是后续距离比较中使用的坐标表达。

要观察的值可以分成下面三组。

| 项目 | token ID | 说明用 embedding 向量 | 与 query vector 的距离 |
| --- | ---: | --- | ---: |
| `prompt_limit_phrase` | `1042` | `[0.12, -0.08, 0.44]` | `0.006` |
| `factuality_risk_phrase` | `3881` | `[0.09, -0.02, 0.39]` | `0.001` |
| `vector_search_phrase` | `2210` | `[-0.30, 0.11, 0.15]` | `0.242` |

假设 query vector 是 `[0.10, -0.01, 0.41]`。距离值是为了显示 query vector 和各表达向量有多近而预先计算的说明用值。现在重要的不是背距离公式，而是`ID 数字大小`和`向量空间中的接近`是不同判断。

按距离标准排序表达项目，就会得到下面结果。

| 排名 | 项目 | 距离 | 应该读出的意义 |
| ---: | --- | ---: | --- |
| 1 | `factuality_risk_phrase` | `0.001` | 与 query vector 最近的表达项目 |
| 2 | `prompt_limit_phrase` | `0.006` | 也是接近项目，但不是第 1 位 |
| 3 | `vector_search_phrase` | `0.242` | 在这个示例中相对较远的项目 |

这张表中马上要确认的概念只有一个。使用 embedding 的比较不是 token ID 是否一致，也不是比较 ID 大小，而是按向量空间中的距离和方向选择接近项目。

## 表达空间中看到的距离差异

前面的示例不是学习 embedding 的程序，而是用最短场景展示`赋予编号`和`转换成可比较数值表达`不同。最后回答下面三个问题来固定层位。每个问题先自己回答，再和下面解说比较。

| 场景 | 首先要回答的问题 |
| --- | --- |
| 看到 token ID | 这个值是指向项目的编号，还是意义比较坐标 |
| 看到 embedding 向量 | 这个表达能以怎样的距离和方向与其他项目比较 |
| 看到接近项目顺序 | 这个顺序是答案确认，还是一阶段候选选择 |

解说：token ID 是指向项目的编号。数字 `1042` 比 `3881` 小或大这一事实本身，不能说明两个表达项目的意义更接近。embedding 向量是可比较的坐标表达，所以可以计算和 query vector 的距离。接近项目顺序不是答案确认，而是交给下一步检索、依据确认、生成阶段的一阶段候选选择结果。

也就是说，本节的收束不是背下`embedding 是向量`，而是能够把`编号`、`坐标`、`候选比较`读成不同层位。这里要读的核心是，`1042` 和 `3881` 的数字差异本身没有意义，但在向量空间中，可以比较 query 与 `factuality_risk_phrase` 比 `vector_search_phrase` 更接近。如果 ID 是识别用的，那么 embedding 就是让后续相似度比较和上下文计算成为可能的表达空间起点。

### 练习 1. 分离 ID 大小和语义距离

观察值：

| 项目 | 值 |
| --- | --- |
| `prompt_limit_phrase` 的 ID | `1042` |
| `factuality_risk_phrase` 的 ID | `3881` |
| `prompt_limit_phrase` 的距离 | `0.006` |
| `factuality_risk_phrase` 的距离 | `0.001` |

先自己回答。

- `3881` 比 `1042` 大这一事实，是否表示 `factuality_risk_phrase` 更重要或更远？
- 只看 ID 数字，能否说出哪一个表达项目更接近 query？

解说：不是。`1042` 和 `3881` 只是 vocabulary 或存储系统中的项目编号，所以不能用两个数的大小差异判断意义关系。`3881 - 1042 = 2839` 这个计算可以做，但这个值不会说明两个表达项目和 query 有多相似。这个练习中首先要分开的，是`看起来像可以计算的数字`和`可以用于意义比较的坐标`并不相同。

### 练习 2. 直接比较向量距离

观察值：

| 项目 | 与 query vector 的距离 |
| --- | --- |
| `prompt_limit_phrase` | `0.006` |
| `factuality_risk_phrase` | `0.001` |
| `vector_search_phrase` | `0.242` |

先自己回答。

- 最近的项目是什么？
- 最远的项目是什么？
- 这个判断不是以 ID，而是以什么值为标准？

解说：最近的项目是距离值最小的 `factuality_risk_phrase`。最远的项目是距离值最大的 `vector_search_phrase`。这里的比较标准不是 ID，而是 query vector 与表达向量之间的距离。因此即使 `prompt_limit_phrase` 的 ID `1042` 最小，在这个示例的向量空间中，`factuality_risk_phrase` 更接近 query。这就是 embedding 应该读成`可比较坐标表达`的理由。

### 练习 3. 不要把接近项目误认为答案

观察值：

| 排名 | 项目 | 距离 |
| --- | --- | --- |
| 1 | `factuality_risk_phrase` | `0.001` |
| 2 | `prompt_limit_phrase` | `0.006` |
| 3 | `vector_search_phrase` | `0.242` |

先自己回答。

- 第 1 位项目是否就是答案？
- 接近的项目能否直接写进回答？
- 这个结果在下一步应该用作什么？

解说：第 1 位项目不是答案确认。即使 `factuality_risk_phrase` 最接近 query vector，也必须另外确认它是否有足够依据回答实际问题、是否符合用户询问范围。因此这个结果应该用作`先检视的候选列表`，而不是`直接答案`。embedding 视角不是答案判定器，而是让编号无法做到的候选比较成为可能的表达基础。

## 作为背景简单点到

embedding 不是只在 LLM 时代才出现的概念。自然语言处理很早就持续研究怎样把单词转换成 distributed representation，word2vec 等研究也广泛传播了`相似上下文中的单词可能变成相似向量`这种感觉。

到了 LLM 时代，这个概念变得更宽。

- 不只单词，token、句子、文档也成为 embedding 对象
- 生成模型内部表达和检索服务表达更直接地连接起来

## 检查清单
- 能否把 embedding 重新说明成`计算可以使用的坐标表达`？
- 能否区分 token ID 和 embedding 向量承担的角色差异？
- 能否说明向量生成之后，会继续出现`以什么标准判断接近`这个问题？

## 出处与参考资料

- Yoshua Bengio et al., [A Neural Probabilistic Language Model](https://jmlr.csail.mit.edu/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, 确认日期：2026-07-19。作为学习单词的 distributed representation 并用于语言模型泛化的背景依据。
- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 确认日期：2026-07-19。作为 word2vec 系列 dense word vector 和基于上下文的表达学习背景依据。
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, 确认日期：2026-07-19。作为 embedding、向量表达、语言模型输入说明的一般 NLP 背景依据。
