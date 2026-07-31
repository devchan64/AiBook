# P2-8.4 循环（loop）：逐个处理 iterable

> Section ID: `P2-8.4`
> Version: `v2026.07.31`

这个例子的基准源代码保持不变。阅读时，不要只看 `scores` 是否一次性输出，而要看循环中的 `score` 每次变成哪个值。输出分成四行，并不是因为列表被拆成四段代码，而是同一个处理 `print(score)` 对每个项目各执行了一次。

在 P2-8.2 中，我们看过列表（list）；在 P2-8.3 中，我们看过字典（dictionary）。现在把“把这些集合一个个处理掉”的循环（loop）单独拿出来看。

与其把 Python 的循环读成“重复多少次”，不如读成“从什么里面一个一个拿出什么”。这样结构会更清楚。本节会把 iterable、iterator、循环模式整理到基础概念的层面。

这里会说明 `循环（loop）`、`iterable`、`iterator` 的基本区分。`列表（list）` 和 `字典（dictionary）` 的代表性说明放在 P2-8.2、P2-8.3 和 P2-8.4，而这里集中处理的是：如何从这些集合里把值一个个拿出来，转成处理流程。

循环并不是只有 Python 才有的语法。在数据处理、统计计算、模型评估中，几乎总是要把多个项目按同一个标准逐个处理。Python 的 `for` 只是把这种一般流程表现成一种容易读懂的形式。

这里不以“背循环语法种类”为目标，而是把集合型数据结构变成真正的处理流程来读。前面的列表和字典章节处理的是 `值被放在什么结构里`，而这里处理的是：从这些结构里一个个取出值之后，到底在生成什么。只要先抓住这个转换，后面的函数章节里，也会自然地转到 `把循环包起来重复利用` 这个视角。

## 先带走的东西

这一节同时包含循环模式入门和循环抽象的补充说明。第一次阅读时，只要先抓住下面这些 `必需` 内容就够了。

| 区分 | 先带走的内容 |
| --- | --- |
| 必需 | `for item in items` 是从集合里一个个取出值的结构 |
| 必需 | `enumerate()` 用在位置和值都要一起看时，`.items()` 用在字典的键和值都要一起看时 |
| 必需 | `zip()` 用在把两个或更多集合并排一起读的时候 |
| 必需 | 循环结果经常表现成输出、创建新集合、或者累积 |
| 扩展 | 对 iterable 和 iterator 更严格的区分说明 |
| 扩展 | PEP 234 与迭代接口的历史 |
| 扩展 | 通往 generator 等后续学习主题的循环抽象感觉 |

| 本节要先抓住什么 | 紧接着会出现什么问题 | 之后会在什么地方再次使用 |
| --- | --- | --- |
| `for item in items` 是从集合里一个个取出项的结构 | 这会接到 P2-8.5 中“如何把这种循环处理包进函数里重复利用”。 | 之后会持续出现在预处理、评估、文件处理、模型输出整理中。 |
| 列表和字典在循环中会以不同方式被遍历 | 这会让 `enumerate()`、`.items()`、`zip()` 什么时候用变得更清楚。 | 之后会在 DataFrame 行处理、配置值遍历、结果汇总中反复出现。 |
| 循环结果经常表现成输出、新集合、累积值 | 这会接到“如何在同一个框架里读 comprehension 和累积模式”的标准。 | 之后会成为 NumPy 之前的预处理、Python 基础实践、项目代码阅读的基础。 |

| 术语 | 本节先要抓住的意思 |
| --- | --- |
| 循环（loop） | 按同一个处理标准把多个值依次处理的流程。 |
| iterable | 能一个个吐出值，因此可以成为循环目标的结构。 |
| iterator | 负责真正把下一个值一个个取出来的循环装置。 |
| 累积（accumulation） | 在循环过程中不断加值或收集值，形成一个结果的模式。 |
| comprehension | 用循环来生成新列表或新字典的简洁表达。 |

## 核心判断标准：循环（loop）：逐个处理 iterable

- 能读懂 `for item in items` 这种循环。
- 能在入门层面区分 iterable 和 iterator。
- 能说明 `iterable` 这个词为什么不仅覆盖 sequence，也覆盖字典、文件、generator 这类可以一个个吐出值的对象。
- 能说明 `enumerate()`、`.items()`、`zip()` 分别属于什么循环模式。
- 能区分过滤、变换、累积、条件分离循环。
- 能把列表推导式（list comprehension）和字典推导式（dictionary comprehension）读成“通过循环生成新数据结构的表达”。
- 能读懂“往空列表里收集结果”的模式和“按键往字典里累积值”的模式。
- 能说明一边循环一边直接修改原始集合可能产生问题。

## 先抓住的标准

本节最先要抓住的标准是：`循环是把同一种处理依次作用到多个值上的流程。`

| 循环场景 | 先问什么 |
| --- | --- |
| `for score in scores` | 一个个取出来的是什么？ |
| `enumerate(scores)` | 是否还需要位置？ |
| `metrics.items()` | 是否需要把名字和值一起看？ |
| `zip(a, b)` | 是不是在并排读两个或更多集合？ |

也就是说，与其背循环语法，不如先读出 `从集合里拿出了什么，又在生成什么。`

## 学习背景

循环（loop）并不是再学一个 Python 语法，而是在恢复 `把多个值按同一个标准处理` 的数据工作基础流程。即使已经看过列表和字典，只要一加上循环，代码就必须读成 `看项目`、`生成新集合`、`累积值` 这些不同结构。

这里就是要把这种转换明确地处理出来。所以比起语法记忆，更强调先去读 `从集合里拿出了什么，又在生成什么。`

## 三个标准

这里先抓的不是循环语法，而是 `从集合里一个个取值并处理` 的感觉。下面三个标准会成为后面阅读函数复用和预处理例子时的基础。

| 标准 | 为什么重要 | 本节所需的理解程度 |
| --- | --- | --- |
| 循环是把同一种处理作用到多个值上的方式 | 它让你先看到目的，而不是先背 `for` 语句 | 理解成从列表里一个个取值出来并打印的结构 |
| Python 的循环比起“重复几次”，更自然的是读成“从什么里一个个拿出来” | 这样能把按项目循环和 iterable 概念连起来 | 能说明 `for score in scores` 是从 `scores` 里一个个拿出值的结构 |
| 循环结果经常表现成输出、新集合、累积值 | 这样以后更容易读懂 comprehension 和数据预处理例子 | 理解循环可以生成新列表或新字典 |

## 主要学习内容

### 循环是把同一种处理作用到多个值上的方式

一般来说，循环（loop）就是一种把数据集合逐个处理的方法。它把同一种规则应用到多个项上，然后把结果输出出来、做成新集合，或者收集成累积值。

Python 的 `for` 循环非常清楚地表现了这种视角：`从集合里一个个取出项目并处理。`

问题场景：我想看一个最基本的循环：从列表里一个个取出值，并对它们应用同一种处理。
输入（input）：分数列表 `scores`。
期望输出（output）：每个分数都单独打印一行。
要确认的概念：`for item in items` 是从集合里一个个取出项目并处理的基本结构。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

这段代码会从 `scores` 列表里一个个取出值，并用 `score` 这个名字来使用它。

先学过其他语言的人，可能会先把循环想成以数字索引为中心。

问题场景：我想比较看看：如果用位置编号来写同一个循环，它会长什么样。
输入（input）：分数列表 `scores`。
期望输出（output）：通过索引访问的分数会依次打印。
要确认的概念：按项目循环和按位置循环可以得到同样结果，但阅读视角不同。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91, 68]

for i in range(len(scores)):
    print(scores[i])
```

这种方式也能工作。但如果目的只是逐个处理项目，那么像 `for score in scores` 这种以项目为中心的写法，会更清楚地显示意图。

Python 官方教程也说明，`for` 语句和 C、Pascal 中熟悉的数字推进方式略有不同，它是按顺序遍历列表或字符串这类序列（sequence）的项。

| 视角 | 一般说明 | 在 Python 中 |
| --- | --- | --- |
| 循环（loop） | 逐个处理集合中的值的过程 | 经常使用 `for item in items` 这种形式 |
| 循环目标 | 能一个个取出值的集合 | 叫做 iterable |
| 循环结果 | 输出、新集合、累积值、被分离的集合 | 会表现成 `print`、`append`、累积变量、字典累积等 |

如果把这三件事再改写成更实战的形式：

| 循环结果 | 常见形状 |
| --- | --- |
| 输出 | `print(score)` |
| 创建新列表 | `results.append(...)` |
| 创建累积值 | `total += score` |
| 条件分离 | 通过 `if ...:` 只选出一部分项 |

### 为什么叫 iterable

从这里开始，内容会稍微更偏向 `扩展`。如果前面的按项目循环、`enumerate()`、`.items()`、`zip()` 的感觉已经抓住了，这一段不一定要一次全部消化。

`iterable` 的意思是“可以被循环的对象”。中文里也可以说 iterable、可迭代对象、可重复取值的目标。之所以需要这个词，是因为 Python 的循环并不只绑定在列表这类序列（sequence）上。

如果回忆起早年学习编程的感觉，人很容易把循环想成下面这样。

- 一个数字变量一点点增加。
- 按顺序访问数组的第 0、1、2 个位置。
- 到达结束位置时停止循环。

这种方式在处理数组（array）或列表（list）时很自然。但并不是所有循环目标都是 `可以靠数字索引访问的数组`。字典是通过键（key）查值，文件是一行一行地读，生成器（generator）则会在需要的时候一个个地产生值。要想用同一个 `for` 去处理这些对象，比起“它有没有索引”，更重要的是“它能不能一个个吐出值”。

这一点也能从 Python 的历史里看到。PEP 234 是一份写于 2001 年的提案，它提出了迭代接口（iteration interface），让对象能够控制 `for` 循环的行为。这份提案与 Python 2.2 时期的循环结构相连，也展现了 `for` 语句如何从旧式的序列中心循环，扩展成一致处理多种可迭代对象的方式。

PEP 234 的核心可以概括成下面这样。

| 更容易先想到的旧式循环 | Python 的 iterable 视角 |
| --- | --- |
| 要取出第几个位置？ | 能不能一个个接收到下一个值？ |
| 是否需要像数组或列表那样有索引？ | 即使不是列表，也能不能形成循环流程？ |
| 循环本身必须了解结构内部吗？ | 对象能不能提供自己的循环方式？ |

在 Python 官方术语里，iterable 是一种能够一次返回一个成员的对象。除了列表、字符串、元组这些序列之外，字典、文件对象、乃至自己写的类也可以是 iterable。而 `for` 语句会先从 iterable 中创建 iterator，再把 iterator 给出的值一个个处理。

这个视角很重要。看到 `for item in items` 时，不能默认 `items` 一定是列表。`items` 可能是列表，也可能是字典 `.items()` 的结果，也可能是文件，或者是后面会遇到的 generator。名称不同，但共同的问题始终一样。

这个对象能不能一个个吐出值？

### iterable 和 iterator 的感觉

在阅读 Python 代码时，会遇到各种不同的循环模式。下面的例子会一次比较：只循环项目、同时循环位置和值、同时循环字典的键和值。

问题场景：我想比较循环对象改变时，`for` 里面到底会一个个拿出什么。
输入（input）：分数列表 `scores` 和指标字典 `metrics`。
期望输出（output）：分别打印项目本身、位置-项目对、键-值对。
要确认的概念：即使循环模式不同，出发点始终是从 iterable 中一个个取值。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91]
metrics = {"accuracy": 0.91, "loss": 0.32}

print("items only")
for score in scores:
    print(score)

print("index and item")
for index, score in enumerate(scores):
    print(index, score)

print("key and value")
for name, value in metrics.items():
    print(name, value)
```

| 代码形状 | 一个个拿出来的东西 | 主要使用场景 |
| --- | --- | --- |
| `for score in scores` | 一个值 | 只处理值本身就足够时 |
| `for index, score in enumerate(scores)` | 位置和值 | 还需要一起看这是第几个样本时 |
| `for name, value in metrics.items()` | 键和值 | 需要同时读取字典的名字和值时 |

这些写法表面不同，但有共同点：Python 的 `for` 是从 `可循环目标` 里一个个取值并处理。

官方术语里，这种可循环目标叫 iterable。iterable 是一种能一次返回一个成员的对象。列表（list）、字符串（str）、元组（tuple）、字典（dict）、文件对象（file object）都可以是 iterable 的例子。

iterator 则是实际把值流（stream）一个个取出来的对象。在这一节里，比起 `iter()` 和 `next()` 的细节用法，我们先保留这样一种感觉：`for` 在内部会建立这种值流。

如果把它极度简化，可以这样看。

| 术语 | 入门说明 | 例子 |
| --- | --- | --- |
| iterable | 可以一个个取值的对象 | 列表、字符串、字典、文件 |
| iterator | 真实地一个个送出下一个值的流 | 通过 `iter(scores)` 得到的对象 |
| 循环（loop） | 接收这些值并逐个处理的代码 | `for score in scores` |

正因为有这层结构，Python 中很多不同的循环模式其实都能用同一原理来理解。真正重要的是：`循环的是什么？`，以及 `循环结果会生成什么？`

## 细部学习内容

### 循环结构的主要类型

Python 的循环与其只背一种语法，不如按模式来区分阅读。

本节按下面这个顺序来看循环模式。先看一个个取出项目的基本型，然后看位置、键值、两个集合的并排读取。再之后，看循环结果如何生成新列表、累积值，以及如何按条件分离。

| 流程 | 中心问题 |
| --- | --- |
| 项目循环 | 一个个取出来的是什么？ |
| 带位置的循环 | 还需要知道第几个吗？ |
| 键值循环 | 名字和值要一起看吗？ |
| 结果生成 | 是不是在生成新的列表或字典？ |
| 累积与分离 | 是在积累值，还是按条件拆分？ |

### 一个个处理项目

这是最基本的循环。

问题场景：我想再固定一次项目循环的基本型。
输入（input）：分数列表 `scores`。
期望输出（output）：各分数会按顺序打印。
要确认的概念：项目循环更看重值本身，而不是位置。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

读法很简单。

从 `scores` 中一个个取出 `score` 并处理。

在 AI 实践里，看样本（sample）、句子（sentence）、文件名、预测结果时，经常这样写。

### 同时看位置和项目

如果还需要知道它是第几个项，就用 `enumerate()`。

问题场景：我想看一个循环：不仅需要值，也需要知道它是第几个项。
输入（input）：`enumerate(scores)`。
期望输出（output）：位置编号和分数一起输出。
要确认的概念：`enumerate()` 会给值附上位置信息，让循环同时看到二者。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91, 68]

for index, score in enumerate(scores):
    print(index, score)
```

可以这样读。

从 `scores` 中同时取出位置和值并处理。

这在确认报错样本编号、或检查前几个结果时很有用。

### 同时看字典的键和值

对于字典，经常会使用 `.items()`。

问题场景：我想看一个循环：同时确认字典的键和值。
输入（input）：指标字典 `metrics`。
期望输出（output）：会打印 `accuracy`、`loss` 以及对应值。
要确认的概念：字典循环经常不是只看键，而是把键值对一起拿出来读。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
metrics = {"accuracy": 0.91, "loss": 0.32}

for name, value in metrics.items():
    print(name, value)
```

可以这样读。

从 `metrics` 中同时取出指标名和值并处理。

在检查配置值（config）、评估指标（metric）和 API 响应（response）时，经常会看到这种写法。

### 并排看两个集合

当想把两个列表按相同位置配对起来看时，就会遇到 `zip()`。

问题场景：我想把输入文本和标签按同一位置配成对一起看。
输入（input）：两个列表 `texts`、`labels`。
期望输出（output）：文本和标签成对输出。
要确认的概念：`zip()` 会让多个 iterable 在同一位置上的项一起被循环。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
texts = ["good", "bad", "great"]
labels = ["positive", "negative", "positive"]

for text, label in zip(texts, labels):
    print(text, label)
```

可以这样读。

按同样顺序把 `texts` 和 `labels` 配在一起，一个个处理。

在处理输入句子与标签、预测值与正确值、文件名与路径时，经常会出现这种模式。

### 只把符合条件的值重新收集起来

在 P2-8.2 中，我们说过可以先创建一个空列表。在循环里，这个空列表经常会作为收集结果的容器出现。

一边循环，一边只把满足条件的值做成一个新列表。

问题场景：我想看一个过滤循环：从含有 `0` 的分数列表中，只收集有效值。
输入（input）：混有 `0` 的分数列表 `scores`。
期望输出（output）：只包含非 `0` 分数的 `valid_scores`。
要确认的概念：循环经常用来筛选满足条件的项，并生成新的集合。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 0, 75, 0, 91]
valid_scores = []

for score in scores:
    if score != 0:
        valid_scores.append(score)

print(valid_scores)
```

可以这样读。

一个个看 `scores`，只把满足条件的值收集进 `valid_scores`。

这经常出现在删除缺失值、剔除低于标准的值、只选特定标签等预处理（preprocessing）里。

### 把值转换后生成新集合

循环也常用来把现有值变成另外一种值。

问题场景：我想看一个变换循环：把分数改成 0 到 1 之间的值，并生成新列表。
输入（input）：分数列表 `scores`。
期望输出（output）：`normalized_scores`，其中每个分数都除以 100。
要确认的概念：循环可以对所有项应用同样变换，并生成新的结果集合。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

可以这样读。

一个个看 `scores`，把每个值改成 0 到 1 之间的值，再放进新的列表。

这种模式会出现在归一化（normalization）、统一转小写、去掉字符串前后空白等 `对所有项应用同一处理` 的场景。

### 用列表推导式生成新列表

如果循环规则很短，而且结果是一个新列表，就会遇到列表推导式（list comprehension）。

问题场景：我想看一个例子：用很短的循环规则，在一行里生成新列表。
输入（input）：`range(5)`。
期望输出（output）：平方值列表 `squares`。
要确认的概念：列表推导式是“通过循环创建新列表”的紧凑表达。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
squares = [number * number for number in range(5)]

print(squares)
```

这段代码会生成从 `0` 到 `4` 的平方值列表。

如果加上条件，也可以把过滤和变换一起写在一行里。

问题场景：我想看一个例子：用推导式只挑出符合条件的值，生成新列表。
输入（input）：含有 `0` 的分数列表 `scores`。
期望输出（output）：只收集非 `0` 值的 `valid_scores`。
要确认的概念：推导式可以把过滤与新列表生成合并成一个表达。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 0, 75, 0, 91]

valid_scores = [score for score in scores if score != 0]

print(valid_scores)
```

可以这样读。

从 `scores` 中一个个取出 `score`，并把不等于 `0` 的值组成新列表。

在这一节里，我们先按“用普通 `for` 看清结构，再去读简洁表达”的顺序来安排。

### Python 也会把循环放进数据结构定义里面

在 Python 代码里，经常会遇到一种模式：看起来像把循环语句塞进了列表或字典定义的语法里。这就叫 comprehension（推导式）。

comprehension 是一种表达：把现有 iterable 的项一个个处理之后，生成一个新的 collection。Python 官方教程把列表推导式说明为一种创建新列表的简洁方法。在这一节里，我们把这个视角稍微扩展开来，把它理解成一种“通过循环生成新数据结构（如列表或字典）”的表达。

从定义上看，可以把下面三个要素一起看。

| 要素 | 问题 | 例子 |
| --- | --- | --- |
| 输入 iterable | 从什么里面一个个取出值？ | `scores` |
| 循环变量 | 取出的值叫什么名字？ | `score` |
| 结果表达式 | 取出的值会被变成什么再放进去？ | `score / 100` |

所以 `[score / 100 for score in scores]` 可以读成：

从 `scores` 中一个个取出 `score`，并把每个 `score` 改成 `score / 100`，生成一个新列表。

如果用普通 `for` 写长一点，就是下面这样。

问题场景：我想先看在推导式之前，普通 `for` 结构到底长什么样。
输入（input）：分数列表 `scores`。
期望输出（output）：归一化后的分数列表 `normalized_scores`。
要确认的概念：推导式通常是把使用 `append()` 的循环缩短后的表达。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

如果用列表推导式表达同样意图，就会缩短成下面这样。

问题场景：我想比较看看：把刚才的循环缩短成推导式之后，形状怎么变了。
输入（input）：分数列表 `scores`。
期望输出（output）：一行表达出同样归一化结果。
要确认的概念：当循环的目的就是生成新数据结构时，推导式特别容易读。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91]

normalized_scores = [score / 100 for score in scores]

print(normalized_scores)
```

这个表达的意思是：`从 scores 中一个个取出 score，并把每个值变成 score / 100，生成一个新列表。` 它不是把循环藏起来，而是通过语法外形直接表明“这个循环的目的就是生成新列表”。

字典也可以用同样方式生成。

问题场景：我想看一个例子：通过循环生成新字典的推导式。
输入（input）：标签列表 `labels` 和 `enumerate(labels)`。
期望输出（output）：键是标签名、值是位置编号的 `label_to_id`。
要确认的概念：字典推导式同样是通过循环生成新映射结构的表达。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
labels = ["negative", "positive", "neutral"]

label_to_id = {label: index for index, label in enumerate(labels)}

print(label_to_id)
```

这段代码会生成一个字典：标签名称是键（key），位置编号是值（value）。

推导式之所以常被偏好，原因如下。

| 原因 | 说明 |
| --- | --- |
| 意图 | 一眼就能看到目的是生成新列表或新字典 |
| 简洁 | 可以省掉创建空列表再 `append()` 的过程 |
| 一致性 | “取出什么、变成什么”会被集中在一行里 |
| 数据处理 | 过滤、变换、映射这些常见模式可以简短表达 |

但推导式并不总是更好。如果条件很长、嵌套循环太多、或者中间计算需要单独命名，普通 `for` 反而更容易读。

问题场景：我想看一个例子：中间计算和条件一起出现时，普通 `for` 会更易读。
输入（input）：检查 `item["score"]` 并归一化的循环。
期望输出（output）：只有通过条件的值才被加入 `results`。
要确认的概念：有时比起推导式，更适合使用能清楚显示步骤的普通循环。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
results = []

for item in items:
    if item["score"] >= 60:
        normalized_score = item["score"] / 100
        results.append(normalized_score)
```

像这种代码，步骤展开会更清楚。因此，这一节采用下面这些标准。

- 如果循环结果是新列表或新字典，而且规则很短，就可以读成推导式。
- 如果处理过程很长或需要解释，就使用普通 `for`。
- 不要把推导式记成“高级语法”，而是理解成“通过循环生成新数据结构的表达”。

### 计算累积值

循环也经常用来一个个累积值。

问题场景：我想看一个例子：通过循环逐步累加出分数总和。
输入（input）：分数列表 `scores` 和初始值 `total = 0`。
期望输出（output）：所有分数加总后的和。
要确认的概念：累积循环会不断把“当前结果”更新到变量里。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 75, 91, 68]
total = 0

for score in scores:
    total = total + score

print(total)
```

可以这样读。

一个个看 `scores`，不断往 `total` 里面加。

这种结构会出现在总和、数量、出现次数、loss 累积等需要不断堆叠的计算中。

### 按条件分离

一个集合也可以被拆成两个集合。

问题场景：我想看一个循环：把分数列表拆成通过和未通过两组。
输入（input）：分数列表 `scores` 和标准 `60`。
期望输出（output）：两个列表 `passed` 和 `failed`。
要确认的概念：如果把循环和条件语句一起使用，就能把一个集合拆成多个结果集合。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 55, 91, 42, 68]
passed = []
failed = []

for score in scores:
    if score >= 60:
        passed.append(score)
    else:
        failed.append(score)

print(passed)
print(failed)
```

可以这样读。

一个个看 `scores`，然后按条件放进不同的列表里。

这会成为后面“训练数据与测试数据分离”“正常数据与异常数据分离”“按标签分离数据”的基本感觉。

### 累积到字典里

在 P2-8.3 中，我们把字典看成通过键查值的结构。当它和循环放在一起时，就会变成 `按键累积值的结构`。

把循环和字典一起用，就能做按键聚合。

问题场景：我想看一个循环：统计每个标签出现了多少次。
输入（input）：标签列表 `labels`。
期望输出（output）：字典 `label_counts`，里面放着每个标签的数量。
要确认的概念：字典和循环一起使用时，可以生成按键累积的统计结果。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
labels = ["positive", "negative", "positive", "neutral", "positive"]
label_counts = {}

for label in labels:
    label_counts[label] = label_counts.get(label, 0) + 1

print(label_counts)
```

可以这样读。

一个个看 `labels`，并把同一标签出现的次数累积到字典中。

在分类数据里检查标签分布（label distribution）时，这种模式经常会出现。

## 循环连接到数据处理的场景

### 一个小型数据处理例子

下面这个例子会看多个学生的分数，并把超过标准的学生放进通过名单里。

问题场景：我想看一个小型数据处理例子：列表、字典和条件循环一起出现。
输入（input）：`students`，一个装着学生字典的列表。
期望输出（output）：只包含通过学生名字的 `passed_students`。
要确认的概念：在真实数据处理中，样本集合、字段查找、条件过滤会同时出现在一个循环里。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
students = [
    {"name": "Kim", "score": 82.5},
    {"name": "Lee", "score": 55.0},
    {"name": "Park", "score": 91.0},
]

passed_students = []

for student in students:
    if student["score"] >= 60:
        passed_students.append(student["name"])

print(passed_students)
```

这里同时出现了三种结构。

| 代码 | 含义 |
| --- | --- |
| `students` | 存放学生信息的列表 |
| `{"name": "Kim", "score": 82.5}` | 表示一个学生的字典 |
| `for student in students` | 一个个取出学生信息的循环 |

这个例子虽然小，但它很像 AI 实践中的基本结构。

- 数据集（dataset）是多个样本（sample）的集合。
- 一个样本可以拥有多个字段（field）。
- 循环会一个个检查样本。
- 条件语句会筛选需要的样本，或者改变处理方式。

### 循环时要小心不要直接修改原对象

如果在循环过程中直接修改同一个列表或字典，就可能出现和预期不同的结果。

例如，一边遍历列表一边删除项的代码，就必须很小心。

问题场景：我想看一种更安全的过滤方式：不是直接删除原对象，而是生成新结果列表。
输入（input）：含有 `0` 的分数列表 `scores`。
期望输出（output）：排除 `0` 的新列表 `filtered_scores`。
要确认的概念：与其在循环中直接修改原集合，不如生成一个新集合，这样更清楚。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
scores = [82, 0, 75, 0, 91]
filtered_scores = []

for score in scores:
    if score != 0:
        filtered_scores.append(score)

print(filtered_scores)
```

这个例子并没有直接从原始 `scores` 中删除，而是生成了一个新列表 `filtered_scores`。Python 官方教程也说明，在遍历同一个 collection 的同时修改它会比较棘手，而遍历副本或者创建新集合会更清楚。

这个原则在数据预处理中也很有用。

- 保留原始数据。
- 把过滤后的结果放进新的名字里。
- 在代码中保留“按什么标准筛掉的”。

### 案例 1. 如果要从多个样本里挑出通过的那些，到底在循环什么

假设一位学习者想看多个文本样本，并把有标签的样本单独收集起来。人一开始也许可以看单个样本并判断，但一旦样本数量超过几十个，就必须重复应用同一个标准。

这时，如果只把循环看成 `重复几次的语法`，就很容易错过真正的结构。真正重要的是：`从什么里一个个拿出什么？` 以及 `结果到底生成了什么？` 核心流程是：从样本列表里一个个取出样本，检查条件，再把结果收进新列表或字典。

这也是为什么本节要把循环拆成 iterable、项目循环、累积、过滤、按键统计这些模式。在实践中，循环并不是单纯把代码写长的装置，而是按同一标准处理多份数据的基本结构。

可确认的结果，是看有没有生成新的结果集合。例如，一次遍历样本列表之后，如果出现了 `passed_samples` 或 `label_counts` 这样的结果，那么这个循环就不是单纯打印，而是在进行过滤或累积。

## 阅读循环代码时的共同问题

当列表、字典、循环例子越来越多时，只跟着语法走很容易迷路。这时候就用下面这些问题去读代码。

1. 什么是集合？
2. 这个集合里，是顺序重要，还是键重要？
3. 循环一个个取出的是什么？
4. 对取出的值做了什么？
5. 结果是新列表、新字典、输出，还是累积值？

例如，看下面这段代码。

问题场景：我想用共同问题来阅读一个例子：从句子列表生成长度列表。
输入（input）：句子列表 `texts`。
期望输出（output）：`lengths`，其中存放每个句子的长度。
要确认的概念：循环代码可以按照“集合、逐个取出的值、处理、结果”这个框架来读。

```python
# 这个例子用来确认循环如何从一组值中逐个取出项目并处理。
texts = ["AI is useful", "Models can fail", "Data matters"]
lengths = []

for text in texts:
    lengths.append(len(text))

print(lengths)
```

这段代码可以这样读。

| 问题 | 回答 |
| --- | --- |
| 什么是集合？ | `texts` |
| 顺序重要，还是键重要？ | 句子列表，因此是顺序重要的列表 |
| 一个个取出的是什么？ | 一句句子 |
| 对取出的值做了什么？ | 计算长度 |
| 结果是什么？ | 长度列表 `lengths` |

这些问题以后在阅读 NumPy、Pandas、机器学习数据处理代码时，也可以原样使用。即使工具变了，`集合、逐个取出的值、处理、结果` 这个结构仍然成立。

## 检查清单

- 能读懂 `for item in items` 吗？
- 能说出什么时候使用 `enumerate()`、`.items()`、`zip()` 吗？
- 能区分循环结果是输出、新集合还是累积吗？
- 能读懂 `for item in items` 循环并说明执行流程。
- 能在入门层面区分 iterable 和 iterator。
- 能说明 iterable 这个词为什么不仅覆盖 sequence，也覆盖字典、文件、generator 这类可以一个个吐出值的对象。
- 能说明当需要位置时可以使用 `enumerate()`。
- 能说明当需要同时看到字典的键和值时，可以使用 `.items()`。
- 能说明当需要并排看两个集合时，会遇到 `zip()`。
- 能区分项目循环、变换循环、累积循环、条件分离循环。
- 能把列表推导式和字典推导式读成“通过循环生成新数据结构的表达”。
- 能说明当推导式过于复杂时，普通 `for` 反而更合适。
- 能说明一边循环一边直接修改原始数据会产生问题。
- 能说明比起语法，应该先确认输入集合和结果形状吗？

## 来源与参考资料

- Python Software Foundation, [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。作为 `for`、`range()`、函数定义示例和控制流程说明的官方依据。
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认列表推导式、字典遍历、`items()` 示例，以及遍历时修改 collection 的注意说明。
- Python Software Foundation, [Glossary: iterable, iterator](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。作为在入门层面区分 iterable 与 iterator 的依据。
- Python Software Foundation, [The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 `for` 语句会从 iterable expression 的 iterator 中逐个取得项目并赋值。
- Ka-Ping Yee, Guido van Rossum, [PEP 234 -- Iterators](https://peps.python.org/pep-0234/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, 2001，确认日期：2026-07-20。用于确认 Python iteration interface 从 sequence-centered iteration 扩展到对象提供自身 iteration behavior 的历史背景。
