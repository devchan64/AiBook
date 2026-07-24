# P6-3.2 不是答案，而是生成候选的邻近向量

> Section ID: `P6-3.2`
> Version: `v2026.07.24`

在 P6-3.1 中，我们把 embedding 说明为一种把 token 或句子转换成向量(vector)的表达方式。向量已经生成之后，下一个问题就是怎样阅读这些向量。

如果 embedding 向量已经生成，说两个表达彼此接近，实际意味着什么？意义和距离这些说法，指的是在 embedding 空间中，把用法相近的表达作为彼此接近的候选来比较的计算视角。

这里最先要分开的，是`邻近候选`和`正确依据`。距离(distance)和相似度(similarity)是先缩小候选范围的比较标准，并不保证那个候选立刻就是答案，或就是最新依据。

## 向量候选比较的标准

第一次阅读意义和距离时，先抓住下面的问题。

- 在向量空间中，`接近`是什么意思？
- 距离(distance)和相似度(similarity)可以怎样区别阅读？
- 为什么邻近向量不等于答案或真相？
- 这个视角怎样连接到检索、推荐、RAG？

先把意义和距离抓成`要用什么比较标准，把 embedding 向量读作邻近候选`这个问题。embedding 学习流程、快速候选搜索、检索系统中的实际使用，会在后续小节继续展开；现在需要的是检索与推荐中的基本比较感。

比起背公式，更重要的是把`embedding 空间中的距离`读成实际比较与检索的语言。

如果 P6-3.1 的 embedding 说明处理的是`是否把表达变成向量`，这里处理的是由此得到的向量要按什么标准互相读成近或远。这个比较标准之后会扩展到 Transformer 内部计算、RAG、向量数据库中的检索候选选择。

因此，核心不是停在`向量已经生成`，而是继续读出这个向量应该按什么标准比较。

| 当前阶段的焦点 | 接下来的问题 | 再次扩展阅读的位置 |
| --- | --- | --- |
| Embedding | 文本或句子要转换成什么样的向量表达？ | P6-3.1 |
| 意义和距离 | 这些向量要按什么标准作为邻近候选来比较？ | P6-3.2 |
| 检索和 RAG | 邻近候选怎样用于实际文档检索和生成结合？ | P6-11.1, P6-11.2, P6-12.1, P6-12.2 |
| 推荐和后续选择 | 邻近候选要按什么上下文标准再次筛选，才进入最终选择？ | P6-3.2 的案例和服务上下文整体 |

也就是说，本章现在的核心是从`生成向量`转到`把这些向量读作候选比较标准`。这个标准先固定住，后面阅读 RAG 和向量检索时，才不会把邻近文档候选和最终回答依据混在一起。

## 区分邻近候选和正确依据

这个区分把 P6-3.1 的 embedding 从`生成向量`扩展到`比较向量`，也是理解检索和外部知识连接的核心基础。读完这一节之后，应该能够把距离(distance)和相似度(similarity)说明为候选比较标准，并且同时说出邻近向量`可能是相似候选`，但`并不立刻就是答案`。

## `接近`是什么意思

embedding 向量是由多个数字组成的表达。这些向量之间可以用数学方式定义距离或相似度。

可以这样理解。

- 距离短 -> 向量彼此接近
- 相似度高 -> 向量具有更相似的方向或位置

这时重要的是，这种比较不是`字符串比较`，而是`学得的表达比较`。

也就是说：

- 即使没有相同单词，相似表达也可能变近
- 即使有相同单词，只要上下文不同，也可能变远

## 距离和相似度有什么不同

入门阶段不需要把两者区分得过于严格。不过阅读方向可以不同。

| 表达 | 读者直觉 |
| --- | --- |
| 距离(distance) | 彼此相隔多远 |
| 相似度(similarity) | 彼此有多相似 |

两者共同点是，它们都是`比较标准`。

实际业务中，检索系统或 embedding 模型不同，使用的比较函数也可能不同。但读者首先要带走的不是公式名称，而是观察问题、文档、商品、句子`按什么标准被读作彼此接近`的视角。

## 邻近向量为什么有用

找到邻近向量之后，可以做下面这些事。

- 找相似问题
- 找相关文档候选
- 找相似商品或内容
- 找重复或几乎相同的表达

也就是说，embedding 空间中的距离概念，会自然连接到 Part 6 后面的 RAG、向量数据库(vector database)、推荐(recommendation)等主题。

## 为什么邻近向量不等于答案

这一点要先抓住，才不会把`接近`这个判断和`正确`或`最新`这个判断混在一起。

`邻近向量`通常意味着`相关可能性高的候选`，不意味着答案或真相。

可以想象下面这些情况。

- 表达相似但事实错误的文档
- 表面上和问题相似，但实际需要不同上下文的文档
- 已经过时、不再最新的文档
- 在专业领域中，一般 embedding 无法充分区分的文档

因此，在相似度检索或 RAG 中，必须把`找到邻近候选的阶段`和`确认这些候选是否真的是正确依据的阶段`分开看。

## 极简画法

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s02-similarity-flow-zh.mmd"
```

这个图要确认的结果是，`找到接近的东西`和`把它整理成最终答案`是不同阶段；即使检索命中了，回答整理也还要经过单独判断。

读图时，可以先把`第一轮候选`和`最终确认`分开。

| 先分开什么 | 为什么需要 |
| --- | --- |
| 选择邻近候选的阶段 | 先固定距离和相似度负责做什么。 |
| 打开候选并确认的阶段 | 抓住接近并不立刻等于答案这一点。 |
| 再次查看最新性与例外条件的阶段 | 因为它会自然连接到后面的 RAG 和检索质量说明。 |

## 案例与示例

下面的图把本节的三个案例重新放到同一个共同问题下：重点不是`什么相同`，而是`先把什么作为邻近候选提上来`。

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s02-similarity-use-cases-zh.mmd"
```

这个图要确认的是，任务虽然不同，但`先选择邻近候选`这个阶段是共同的。不过这个候选并不立刻就是答案，因此后续检查和整理阶段仍然需要分开。

### 案例 1. 找相似问题

想象用户在帮助窗口里问：`只靠 prompt 能防止错误回答吗？`如果认为只有问题里的词原样出现在文档标题中才容易找到，就会先找`错误回答`或`防止`这样的词。但实际知识库里，可能只有标题更技术化的文档，例如`prompt 的限制与事实性增强方法`。这时如果只匹配关键词，就可能错过相关文档，用户也可能误以为`看来没有这份文档`。

这里改变的标准，是越过单词是否一致，转向比较两个句子是否实际指向同一个问题场景。相似度检索会把`防止错误回答`和`增强事实性`看作相当接近的问题，并把那份文档作为候选提上来。

这里要纠正的误解是`没有相同词，就不是同一个问题`这种感觉。本案例要确认的结果是，即使问题里的词没有原样出现，处理同一个问题的文档是否也会成为实际候选；并且只看候选，也能否说明为什么那份文档被归到同一个场景。

这个案例最后要关闭的判断很简单。距离比较会先找到同一个问题场景，但候选正文和依据确认仍然是另一个阶段。

### 案例 2. 文档检索

想象要在几百份内部政策文档中询问：`差旅费报销截止日是什么时候？`如果先以标题为标准，就容易觉得只有标题里同时出现`差旅费`、`报销`、`截止日`，答案才会马上出来。但在实际文档结构中，标题可能是`差旅运营指南`，只有正文中间的表格写着`每月 5 个工作日内提交`和`海外差旅例外`。即使打开了一个标题匹配的文档，如果漏掉关键段落，答案仍然会很慢或出错。

这里改变的标准，是不再停在选择一个文档标题，而是把搜索单位下沉，先收集几个与问题最接近的段落。相似度检索会把几个与问题接近的段落收集成候选，然后让 LLM 阅读这些段落并整理自然语言回答。

这里要纠正的误解是`标题匹配了，文档就已经是答案`这种期待。本案例要确认的结果不是找到一个标题相似的文档，而是包含实际截止日的关键段落是否进入候选，以及包含例外条款的段落是否也一起出现。

这个案例最后要关闭的判断，是把标题匹配和回答依据确认分开。先收集邻近段落候选，再重新打开它们，确认是否真的包含截止日和例外条款。

### 案例 3. 推荐系统

想象用户已经完整看完一门入门线性代数课程，系统需要推荐下一门课。很容易先因为都有`入门`标签，就把课程归为相似。但实际上，一门课可能主要是黑板公式讲解，另一门课可能主要是 NumPy 实作，学习节奏会相当不同。例如，完整看完公式讲解视频的用户如果立刻转到代码实作中心的课程，可能更容易中途离开。也就是说，相同标签不能保证相似的消费体验。

这里改变的标准，是不只匹配一个标签，而是同时看用户实际以什么流程消费了什么课程。如果在同时反映观看行为和课程特征的向量空间中寻找邻近项目，就能比简单标签更自然地选出实际学习流程相近的候选。

这里要纠正的误解是`标签相同，体验也相同`这种感觉。本案例要确认的结果是，比起相同标签，实际学习节奏相近的候选是否更靠前聚集；并且这样的候选选择是否还能降低下一步学习的离开可能性。

这个案例最后要关闭的判断也一样。邻近推荐候选不是最终选择，而是后续过滤器的输入，因此还要重新查看难度、目标、最新性等条件。

把三个案例重新按候选选择视角整理，就是下面这样。

| 情况 | 人眼先看到的东西 | 相似度检索先想提上来的候选 |
| --- | --- | --- |
| 找相似问题 | 有相同词的问题 | 处理同一个问题的问题 |
| 文档检索 | 标题相似的文档 | 包含核心答案的段落 |
| 推荐系统 | 贴着相同标签的项目 | 实际消费流程相似的项目 |

## 区分候选选择和答案确认

读完这一节之后，即使还不了解具体距离函数，也应该能跟着下面的例子，先把`选择邻近候选`和`确认最终答案`分开。

| 当前看到的结果 | 容易先想到的误解 | 从意义和距离视角先改问的问题 |
| --- | --- | --- |
| 某个文档按 distance 排第 1 | 容易觉得那个文档就是最终答案 | 这个值是第一轮候选顺序，还是最终答案确认？ |
| 两个候选都很接近 | 容易觉得只看第 1 个就好，其他可以丢掉 | 是否按正文和最新性标准重新打开 top-k 候选？ |
| 出现了和问题相似的文档 | 容易觉得相似就代表事实也正确 | 除了相关性之外，是否另行确认最新性、例外、事实一致？ |

这张表的重要点不是背距离分数。首先需要的是把`候选选择`和`答案确认`读成不同阶段。

这里经常混在一起的，也正是这两个阶段。

- 找到邻近候选后，容易觉得答案已经结束。
- top-1 文档出现后，容易觉得其他候选没有意义。
- 相关性高时，容易觉得事实性也会自动跟上。

但要阅读后面的 RAG、检索质量、运营约束小节，就必须能够分开看`什么被先提为候选`和`什么被最终确认为依据`。

## 练习与示例

这个练习的目标，是区分`先选择邻近候选`的感觉和`接近并不等于答案`这一点。先用一个小数值示例固定判断位置，再用两种检索信号确认同一结构。

假设问题是`差旅费报销截止日是什么时候？`，检索系统提上来了下面三个候选。

| 排名 | 候选 | 距离 | 更新 | 备注 |
| ---: | --- | ---: | --- | --- |
| 1 | `doc_A` | `0.02` | `2026-03` | 上一季度政策 |
| 2 | `doc_C` | `0.05` | `2026-06` | 包含最新例外条款 |
| 3 | `doc_B` | `1.0` | `2025-12` | 其他主题 |

这张表中，距离值是`先把与问题接近的候选排出来的信号`，更新日期和备注则是`能否作为最终依据还要重新确认的信号`。

这里 `doc_A` 按距离排第 1，意味着它是`先打开查看的候选`。但是 `doc_A` 是上一季度政策，而 `doc_C` 虽然按距离排第 2，却包含最新例外条款。因此，距离排序是候选选择阶段的输出，最终依据确认必须重新检查正文和 metadata 之后才可能完成。

## 检索候选判断中分开的东西

本节代码用两种方式建立同一组文档候选。首先用 `TfidfVectorizer` 做一个接近文字重叠的可复现基准线，随后用 Ollama embedding 模型确认实际 embedding 候选排序。两个输出的排序可能不同。但要阅读的中心相同：把`邻近候选`、`要检查的候选集合`、`最终依据`分成不同阶段。

### 基本示例. 分开 top-k 候选和最终依据候选

这个示例用 `TfidfVectorizer` 代替实际 embedding 模型，把它当作一个小检索模型来使用。核心不是检索模型的种类，而是通过输出确认邻近候选顺序和最终依据候选可能不同。可以直接调整的值是 `query`、`top_k`、`min_similarity`。

```python
# 分开查看邻近 top-k 候选和最终依据候选的示例。
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    {
        "doc_id": "doc_A",
        "title": "差旅费报销政策",
        "text": "差旅费报销截止日和提交截止日是每月 5 个工作日内。以上一季度为准。",
        "current_version": False,
        "contains_exception": False,
    },
    {
        "doc_id": "doc_C",
        "title": "差旅费报销最新例外",
        "text": "海外差旅例外条件和紧急审批例外条件，请确认最新公告链接。",
        "current_version": True,
        "contains_exception": True,
    },
    {
        "doc_id": "doc_B",
        "title": "会议室预订",
        "text": "会议室预订要在内部日历中申请，并一起记录设备借用情况。",
        "current_version": True,
        "contains_exception": False,
    },
]

# 操作变量：改变 query、top_k、min_similarity，会改变要检查的候选集合。
query = "差旅费报销截止日和例外条件是什么？"
top_k = 3
min_similarity = 0.10

vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
document_vectors = vectorizer.fit_transform([doc["text"] for doc in documents])
query_vector = vectorizer.transform([query])
similarities = cosine_similarity(query_vector, document_vectors)[0]

ranked = sorted(
    zip(documents, similarities),
    key=lambda item: item[1],
    reverse=True,
)[:top_k]

print("retrieved candidates:")
for rank, (doc, score) in enumerate(ranked, start=1):
    print(
        rank,
        doc["doc_id"],
        "similarity=", round(float(score), 3),
        "current=", doc["current_version"],
        "exception=", doc["contains_exception"],
    )

grounding_candidates = [
    doc["doc_id"]
    for doc, score in ranked
    if score >= min_similarity and doc["current_version"] and doc["contains_exception"]
]

print("grounding_candidates =", grounding_candidates)
```

执行结果示例可以这样阅读。

```text
retrieved candidates:
1 doc_A similarity= 0.486 current= False exception= False
2 doc_C similarity= 0.237 current= True exception= True
3 doc_B similarity= 0.0 current= True exception= False
grounding_candidates = ['doc_C']
```

在这个输出中，`doc_A` 按相似度排第 1，但它基于上一季度，也没有例外条件。相反，`doc_C` 虽然排第 2，却是最新文档并包含例外条件，所以成为最终依据候选。也就是说，先找到邻近候选和把它确认为回答依据，是彼此不同的阶段。

### 选择示例. 用本地 embedding 模型比较同一组候选

如果已经安装 Ollama，并且下载了 `nomic-embed-text` 模型，就可以用实际 embedding 模型确认同一结构。这个选择示例的目的不是比较模型性能，而是确认：即使用 embedding 模型生成的向量来建立候选，而不是用基于字符串重叠的向量化，也仍然要重新分开看`邻近候选`和`最终依据候选`。

先在本地终端准备模型。

```bash
ollama pull nomic-embed-text
```

然后执行下面的代码。这段代码使用 Python package `ollama`。如果代码输出 `Ollama embedding model is not ready.`，表示 Ollama server 关闭，或 `nomic-embed-text` 模型还没有准备好。

```python
# 用 Ollama 的本地 embedding 模型再次比较 top-k 候选和最终依据候选的选择示例。
from math import sqrt

import ollama

documents = [
    {
        "doc_id": "doc_A",
        "title": "差旅费报销政策",
        "text": "差旅费报销截止日和提交截止日是每月 5 个工作日内。以上一季度为准。",
        "current_version": False,
        "contains_exception": False,
    },
    {
        "doc_id": "doc_C",
        "title": "差旅费报销最新例外",
        "text": "海外差旅例外条件和紧急审批例外条件，请确认最新公告链接。",
        "current_version": True,
        "contains_exception": True,
    },
    {
        "doc_id": "doc_B",
        "title": "会议室预订",
        "text": "会议室预订要在内部日历中申请，并一起记录设备借用情况。",
        "current_version": True,
        "contains_exception": False,
    },
]

# 操作变量：改变 query、top_k、min_similarity，检索候选和依据候选可能会改变。
query = "差旅费报销截止日和例外条件是什么？"
top_k = 3
min_similarity = 0.25
model_name = "nomic-embed-text"

def embed(text: str) -> list[float]:
    return ollama.embed(model=model_name, input=text).embeddings[0]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

try:
    query_vector = embed(query)
    document_vectors = [embed(doc["text"]) for doc in documents]
except Exception as error:
    print("Ollama embedding model is not ready.")
    print(type(error).__name__, error)
    raise SystemExit

ranked = sorted(
    zip(documents, document_vectors),
    key=lambda item: cosine_similarity(query_vector, item[1]),
    reverse=True,
)[:top_k]

print("embedding candidates:")
for rank, (doc, vector) in enumerate(ranked, start=1):
    score = cosine_similarity(query_vector, vector)
    print(
        rank,
        doc["doc_id"],
        "similarity=", round(float(score), 3),
        "current=", doc["current_version"],
        "exception=", doc["contains_exception"],
    )

grounding_candidates = [
    doc["doc_id"]
    for doc, vector in ranked
    if (
        cosine_similarity(query_vector, vector) >= min_similarity
        and doc["current_version"]
        and doc["contains_exception"]
    )
]

print("grounding_candidates =", grounding_candidates)
```

执行结果示例如下。

```text
embedding candidates:
1 doc_C similarity= 0.85 current= True exception= True
2 doc_A similarity= 0.833 current= False exception= False
3 doc_B similarity= 0.813 current= True exception= False
grounding_candidates = ['doc_C']
```

在这个选择示例中，实际 embedding 模型把 `doc_C` 排到了第 1。但不能只凭这一点就读成 embedding 模型已经找到了最终答案。因为 `doc_A` 和 `doc_B` 也以很高相似度一起出现了。在候选文档少、文本又短的示例中，广义的业务文档、申请流程、政策句子可能被抓成彼此接近。即使用实际 embedding 模型，接近也只是`候选选择信号`，不是自动保证最新性和例外条件的判定值。

### 练习 1. 阅读两种检索信号的排序差异

把两个执行结果并排看，同一个问题下第 1 候选也会不同。

| 执行方式 | 第 1 候选 | 需要一起阅读的信号 |
| --- | --- | --- |
| `TfidfVectorizer` 基准线 | `doc_A` | 截止日表达重叠很多，但 `current_version=False`，而且没有例外条件 |
| Ollama embedding 模型 | `doc_C` | 例外条件文档先出现，但其他候选也以高相似度一起出现 |

先自己回答。

- 为什么 `TfidfVectorizer` 中 `doc_A` 会先出现？
- 为什么 Ollama embedding 模型中 `doc_C` 可能先出现？
- 即使两个输出不同，最终确认依据前共同必须检查什么？

解说：`TfidfVectorizer` 会强烈看字符片段的重叠。因此，`差旅费`、`报销`、`截止日`这些表达重叠较多的 `doc_A` 会先出现。Ollama embedding 模型会更宽地看整个句子的意义关系，所以可能先提出包含`例外条件`的 `doc_C`。但两种方式在最终确认依据之前，都必须重新确认文档正文、最新性和例外条件。

### 练习 2. 不要立刻相信高相似度

只看 Ollama embedding 输出时，三个候选的相似度都显得很高。

| 候选 | 相似度 | 当前版本 | 例外条件 |
| --- | ---: | --- | --- |
| `doc_C` | `0.850` | 是 | 是 |
| `doc_A` | `0.833` | 否 | 否 |
| `doc_B` | `0.813` | 是 | 否 |

先自己回答。

- `doc_B` 的相似度很高，就可以把它当作最终依据吗？
- `doc_A` 的相似度很高，就可以把上一季度政策放进答案吗？
- 在这个输出中，为什么最终依据候选要缩小到 `doc_C`？

解说：`doc_B` 即使是当前版本，也不包含问题核心的差旅费报销例外条件。`doc_A` 即使和问题接近，也是上一季度政策。因此，三个候选看起来都很近，最终依据候选也必须缩小到 `current_version=True` 且 `contains_exception=True` 的 `doc_C`。这时，相似度不是丢弃或信任候选的最终判定，而是决定先打开什么的顺序。

### 练习 3. 选择下一步动作

在下面每个场景中，从`检查文档正文`、`确认最新性`、`追加搜索`、`确认依据候选`中选择应该先做什么，并用一句话写出理由。

| 场景 | 先选择的动作 |
| --- | --- |
| top-1 文档最接近问题，但只包含去年的政策 | ? |
| top-3 候选都差不多接近，但只有一个包含最新公告链接 | ? |
| 整个 top-k 候选集合都离问题很远，核心词也几乎不重叠 | ? |
| top-1 候选看起来合理，但完全没有提到例外条款 | ? |

解说：第一个场景先确认最新性。邻近候选如果只包含去年的政策，就不能成为最终依据。第二个场景要同时检查文档正文和最新性。top-k 都接近时，不要只看距离顺序，而要打开实际公告链接和依据段落。第三个场景先追加搜索。候选整体都远、核心词也几乎不重叠时，当前检索 query 或 index 可能不合适。第四个场景先检查文档正文。top-1 候选看起来合理，但没有例外条款时，很难确认答案。四个场景的核心都是把`邻近候选选择`和`最终依据确认`分开阅读。

这个示例说明，实际服务中的`寻找邻近向量`不是`立刻确认答案`，而是`按顺序缩小先要检查的候选`。TF-IDF 基准线和 Ollama embedding 模型可以产生不同排序，但两者都不会自己替你确认最终依据。所以后面阅读检索、RAG、推荐小节时，核心也不是距离计算本身，而是`什么被提为候选，接下来又通过什么阶段检查`。

embedding 和距离概念，与统计语言模型之后的表示学习(representation learning) 有很深的联系。与其只把词当作 one-hot 那样彼此分离的符号，不如说，尝试在向量空间中表达关系的做法，后来扩展到了检索和生成服务整体。

在 LLM 时代，这个视角变得更重要。

- 在模型内部，它连接到 attention 计算
- 在服务外部，它连接到 embedding 检索和 RAG

## 检查清单

- 应该能够把距离和相似度说明为`候选比较标准`。
- 应该能够把最近向量和最终答案分开思考。
- 应该能够分别说明`为什么相似问题和文档会一起出现`，以及`为什么最近候选并不总是答案`。

## 来源与参考资料

- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 确认日期: 2026-07-19. 用作 dense word vector 和相似上下文表达的背景依据。
- Tomas Mikolov et al., [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 确认日期: 2026-07-19. 用作把词和短语作为向量空间中可比较表达来处理的背景依据。
- Nils Reimers, Iryna Gurevych, [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084){: target="_blank" rel="noopener noreferrer" }, arXiv, 2019, 确认日期: 2026-07-19. 用作以 cosine similarity 比较句子 embedding 并用于 semantic similarity search 的说明依据。
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, 确认日期: 2026-07-19. 用作 embedding 和相似度比较说明的一般 NLP 背景依据。
- Ollama, [nomic-embed-text](https://registry.ollama.com/library/nomic-embed-text){: target="_blank" rel="noopener noreferrer" }, Ollama model registry, 确认日期: 2026-07-24. 用于确认使用本地 embedding 模型的选择执行示例中的模型说明和调用流程。
