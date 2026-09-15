# P2-8.4 循环：逐项处理可迭代对象

> Section ID: `P2-8.4`
> Version: `v2026.09.15`

对四个分数应用同一标准，需要逐个取出并比较。循环按项重复处理，以输出结果、收集所需值，或计算总和与数量。

## for 与逐项处理

`for score in scores:` 从 `scores` 中逐个取值，并用 `score` 指代。冒号（`:`）下方缩进的代码是每项执行的处理。本例把 `82`、`75`、`91`、`68` 分别输出在一行。

```python
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

`print(score)` 执行四次，因此输出四行。缩进决定哪些代码属于循环。

也可以按位置取出相同的值。`len(scores)` 为项数 `4`，`range(4)` 依次提供 `0` 到 `3`。下面输出与前例相同。

```python
scores = [82, 75, 91, 68]

for i in range(len(scores)):
    print(scores[i])
```

只需要值时，直接使用 `for score in scores`。同时需要位置和值时，可使用 `enumerate()`。

## 位置、键与两个列表的对应

### 位置与值：enumerate

`enumerate(scores)` 同时提供位置和值，输出为 `0 82`、`1 75`、`2 91`、`3 68`。

```python
scores = [82, 75, 91, 68]

for index, score in enumerate(scores):
    print(index, score)
```

`index, score` 分别接收每一对中的两个值，可用于记录出错样本的位置并检查其值。

### 键与值：items

字典的 `.items()` 同时提供键和值。代码输出指标名称及其数值：`accuracy 0.91`、`loss 0.32`。

```python
metrics = {"accuracy": 0.91, "loss": 0.32}

for name, value in metrics.items():
    print(name, value)
```

`for name in metrics` 只逐个接收键，使用 `.items()` 才会一起接收关联值。

### 两个列表：zip

`zip()` 从多个迭代对象中各取一项并组合。本例将句子与标签配对，输出 `good positive`、`bad negative`、`great positive`。

```python
texts = ["good", "bad", "great"]
labels = ["positive", "negative", "positive"]

for text, label in zip(texts, labels):
    print(text, label)
```

配对按相同位置进行，`zip()` 不会根据句子含义寻找标签。

默认情况下，`zip()` 在较短列表结束时停止。将 `labels` 缩短为 `["positive", "negative"]`，只会输出前两对，`great` 不被处理。要求长度一致时，可用 `zip(texts, labels, strict=True)`；它处理前两对后，遇到长度不一致便引发 `ValueError`。

## 可迭代对象与迭代器

可迭代对象是支持迭代的对象。除了列表和字符串，字典、文件对象、按需产生值的生成器也可迭代。文件提供行，字典提供键，因此并非所有迭代对象都需要整数索引。

迭代器提供下一项，并记录当前进度。用 `iter()` 创建迭代器，`next()` 取得下一项。本例从 `[82, 75]` 中依次取出 `82`、`75`，没有剩余值时输出指定默认值 `end`。

```python
scores = [82, 75]
iterator = iter(scores)

print(next(iterator))
print(next(iterator))
print(next(iterator, "end"))
```

不提供默认值而再次调用 `next(iterator)`，会引发 `StopIteration`。`for` 从迭代器取值，收到结束信号后停止循环。

| 术语 | 作用 | 示例 |
| --- | --- | --- |
| 可迭代对象 | 迭代的对象 | `scores` |
| 迭代器 | 提供下一项并保存进度 | `iter(scores)` 的结果 |
| 循环 | 处理取得的值 | `for score in scores` |

2001 年、Python 2.2 时期的 PEP 234 提出由对象提供迭代方式的接口，使同一种 `for` 语句能够处理序列之外的多种对象。

## 已经消费过的迭代器

列表开始新一轮迭代时可以从头读取，但已读完的迭代器不会自动回到起点。`zip()` 也返回迭代器。

```python
texts = ["good", "bad"]
labels = ["positive", "negative"]
pairs = zip(texts, labels)

print(list(pairs))
print(list(pairs))
```

第一次输出为 `[('good', 'positive'), ('bad', 'negative')]`，第二次为 `[]`。数据没有消失，而是 `pairs` 已被消费完。改为 `pairs = list(zip(texts, labels))` 后，配对结果保存在列表中，两次输出相同，但所有配对也都会保留在内存中。

对空列表执行 `for`，循环体一次也不会运行。在循环外初始化 `total = 0`，空输入时总和仍为 0。若名称只在循环内部首次赋值，空输入时该赋值根本不会执行。

## 筛选与转换

### 选择符合条件的值

假设本数据用 `0` 表示未录入分数。`score != 0` 检查分数是否非零。仅将符合条件的值加入空列表，输出 `[82, 75, 91]`。

```python
scores = [82, 0, 75, 0, 91]
valid_scores = []

for score in scores:
    if score != 0:
        valid_scores.append(score)

print(valid_scores)
```

`if` 下方缩进的 `append()` 只在条件为真时执行。如果实际成绩允许 0 分，这一条件也会删除有效分数，因此需要其他缺失标记。

### 对所有值应用同一转换

将百分制分数除以 100，可表示为 0 到 1 之间的值。转换 `[82, 75, 91, 68]` 后输出 `[0.82, 0.75, 0.91, 0.68]`。

```python
scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

保留原分数不变，把转换结果收集到 `normalized_scores`。类似循环也用于将字符串转为小写或去掉首尾空白。

## 推导式

推导式是通过迭代构建新数据结构的简写。`[结果表达式 for 变量 in 可迭代对象]` 会创建新列表。

把 `range(5)` 提供的 `0` 到 `4` 分别平方，输出 `[0, 1, 4, 9, 16]`。

```python
squares = [number * number for number in range(5)]

print(squares)
```

在末尾加条件，只把符合条件的项放入新列表。本例输出 `[82, 75, 91]`，与前面的缺失分数筛选相同。

```python
scores = [82, 0, 75, 0, 91]

valid_scores = [score for score in scores if score != 0]

print(valid_scores)
```

把分数除以 100 的循环也可以简写。转换 `[82, 75, 91]`，输出 `[0.82, 0.75, 0.91]`。

```python
scores = [82, 75, 91]

normalized_scores = [score / 100 for score in scores]

print(normalized_scores)
```

| 部分 | 含义 |
| --- | --- |
| `scores` | 输入列表 |
| `score` | 逐个取出的分数 |
| `score / 100` | 放入新列表的值 |

在花括号中使用 `键: 值` 可以创建字典，结果为 `{'negative': 0, 'positive': 1, 'neutral': 2}`。

```python
labels = ["negative", "positive", "neutral"]

label_to_id = {label: index for index, label in enumerate(labels)}

print(label_to_id)
```

需要分别说明条件和中间计算时，可以使用普通 `for`。本例只有 `82` 和 `91` 通过阈值 `60`，因此输出 `[0.82, 0.91]`。

```python
items = [{"score": 82}, {"score": 55}, {"score": 91}]
results = []

for item in items:
    if item["score"] >= 60:
        normalized_score = item["score"] / 100
        results.append(normalized_score)

print(results)
```

## 求和与按键计数

### 累加总和

累加是把新值计入当前结果。从 `total = 0` 开始加上 `[82, 75, 91, 68]`，最终输出总和 `316`。

```python
scores = [82, 75, 91, 68]
total = 0

for score in scores:
    total = total + score

print(total)
```

`total = total + score` 把当前分数加到先前总和上，再将结果赋给 `total`。

| 当前分数 | 相加前的 total | 相加后的 total |
| --- | --- | --- |
| 82 | 0 | 82 |
| 75 | 82 | 157 |
| 91 | 157 | 248 |
| 68 | 248 | 316 |

### 按条件分组

把 `[82, 55, 91, 42, 68]` 分为不低于 `60` 和低于 `60` 两组，输出通过列表 `[82, 91, 68]` 与未通过列表 `[55, 42]`。

```python
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

`if` 条件为假时执行 `else`。阈值提高到 `70` 后，`68` 移入未通过列表，结果变为 `[82, 91]` 和 `[55, 42, 68]`。

### 按标签计数

字典可以累计各标签的出现次数。本列表有三个 `positive`，以及各一个 `negative`、`neutral`，输出 `{'positive': 3, 'negative': 1, 'neutral': 1}`。

```python
labels = ["positive", "negative", "positive", "neutral", "positive"]
label_counts = {}

for label in labels:
    label_counts[label] = label_counts.get(label, 0) + 1

print(label_counts)
```

第一次遇到标签时，`get(label, 0)` 返回 `0`，于是记录数量 `1`。再次遇到同一标签，就在已有数量上加 `1`。

## 案例：收集通过学生的姓名

Kim 得 82.5 分，Lee 得 55 分，Park 得 91 分。每名学生用字典表示，三名学生组成列表。收集不低于 `60` 分的姓名，输出 `['Kim', 'Park']`。

```python
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

循环逐个接收学生字典，检查 `student["score"]`，将符合条件的 `"name"` 加入结果。阈值改为 `90` 后，只剩 `['Park']`。

## 迭代过程中删除元素

遍历时删除元素，会使后面的元素前移，可能跳过部分项。本例试图删除所有 0，但两个连续的 0 留下一个，输出 `[82, 0, 91]`。

```python
scores = [82, 0, 0, 91]

for score in scores:
    if score == 0:
        scores.remove(score)

print(scores)
```

删除第一个 0 后，第二个 0 移到原位置，而循环继续前进，不再检查它。保留原列表并收集新结果可以避免此问题。下面代码对同一输入输出 `[82, 91]`。

```python
scores = [82, 0, 0, 91]
filtered_scores = []

for score in scores:
    if score != 0:
        filtered_scores.append(score)

print(filtered_scores)
print(scores)
```

第二次输出的原列表保持 `[82, 0, 0, 91]`。这里与筛选例相同，假定 0 表示未录入。

## 计算句子长度

对每个句子应用 `len()` 可得到字符数列表。本例计入空格，输出 `[12, 15, 12]`。

```python
texts = ["AI is useful", "Models can fail", "Data matters"]
lengths = []

for text in texts:
    lengths.append(len(text))

print(lengths)
```

输出长度与输入句子顺序一致。`lengths[1]` 中的 `15` 是第二句 `"Models can fail"` 的长度。

## 检查清单

- 能读懂 `for item in items` 并解释执行流程。
- 能初步区分可迭代对象与迭代器。
- 能解释可迭代对象不仅包含序列，也包括字典、文件和生成器。
- 需要位置时能使用 `enumerate()`。
- 同时查看字典键和值时能使用 `.items()`。
- 能识别用于并行配对的 `zip()`。
- 能区分逐项处理、转换、累加和按条件分组。
- 能把列表、字典推导式读作通过迭代创建新结构的表达式。
- 能说明复杂推导式何时适合改用普通 `for`。
- 能解释迭代中直接修改原数据可能造成问题。

- 能解释为何再次读取耗尽的迭代器得不到元素。

## 来源与参考资料


- Python Software Foundation, [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。作为 `for`、`range()`、函数定义示例和控制流程说明的官方依据。
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认列表推导式、字典遍历、`items()` 示例，以及遍历时修改 collection 的注意说明。
- Python Software Foundation, [Glossary: iterable, iterator](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。作为在入门层面区分 iterable 与 iterator 的依据。
- Python Software Foundation, [The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认 `for` 语句会从 iterable expression 的 iterator 中逐个取得项目并赋值。
- Ka-Ping Yee, Guido van Rossum, [PEP 234 -- Iterators](https://peps.python.org/pep-0234/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, 2001，确认日期：2026-07-20。用于确认 Python iteration interface 从 sequence-centered iteration 扩展到对象提供自身 iteration behavior 的历史背景。

- Python Software Foundation, [Built-in Functions: iter, next, zip](https://docs.python.org/3/library/functions.html){: target="_blank" rel="noopener noreferrer" }, 2026-09-15. 迭代器耗尽、默认值，以及 zip 长度检查与 strict 选项。
