# P2-8.5 函数与小范围复用

> Section ID: `P2-8.5`
> Version: `v2026.09.15`

## 定义与调用函数

函数通常接收输入、执行处理并返回结果。数学强调输入与输出的关系，编程则把关系表达为可执行代码。

Python 用 `def` 为函数命名，并以形参（parameter）命名所需输入。

分数 `82` 不低于阈值 `60`，因此输出 `pass`。这段代码不使用函数，直接通过条件语句判断。

```python
score = 82

if score >= 60:
    result = "pass"
else:
    result = "fail"

print(result)
```

只判断一次时可以这样写。但若要对多个分数反复做相同判断，就会重复代码。

把通过判断命名为 `pass_or_fail` 后，只需改变分数就能调用。下面依次输出 `pass`、`fail`。

```python
def pass_or_fail(score):
    if score >= 60:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(55))
```

`pass_or_fail` 是函数名，`score` 是内部使用的输入名称。`return` 把结果送回调用处并结束本次执行。输入 `82` 时返回 `"pass"`，不会再执行下方的 `return "fail"`。

### 数学函数与 Python 函数

数学中通常用输入与输出的关系描述函数。

$$
f(x) = x + 1
$$

数学函数 \(f(x)=x+1\) 可以写成下面的 Python 代码。传入实参 `3`，输出 `4`。

```python
def f(x):
    return x + 1

print(f(3))
```

| 方面 | 数学函数 | Python 函数 |
| --- | --- | --- |
| 重点 | 输入与输出的关系 | 执行的代码及结果 |
| 表达 | \(f(x) = x + 1\) | `def f(x): return x + 1` |
| 副作用 | 通常作为纯粹关系处理 | 可以输出、保存文件、修改列表 |
| 错误 | 在数学上处理定义域外输入 | 可能出现类型、键或执行错误 |

AI 练习需要两种视角。

- 把损失函数理解为数学关系。
- 用 Python 函数复用这些计算。
- 通过输入输出约定使用库函数，无需了解全部内部实现。

### 形参与实参

形参是在函数定义中命名输入的名称，实参（argument）是调用时传入的值。

给分数 `80` 加上奖励分 `5`，返回 `85`。定义中的 `score`、`bonus` 是形参，调用中的 `80`、`5` 是实参。

```python
def add_bonus(score, bonus):
    return score + bonus

result = add_bonus(80, 5)

print(result)
```

| 术语 | 位置 | 示例 |
| --- | --- | --- |
| 形参 | 定义时使用的输入名称 | `score`、`bonus` |
| 实参 | 调用时传入的实际值 | `80`、`5` |
| 返回值 | 函数返回的结果 | `85` |

### 返回与输出

`return` 将函数计算的结果返回给调用处。

把百分制分数 `82` 除以 100 并返回。调用方把收到的 `0.82` 保存到 `normalized` 并输出。

```python
def normalize_score(score):
    return score / 100

normalized = normalize_score(82)

print(normalized)
```

`normalize_score(82)` 返回 `0.82`，并将结果关联到名称 `normalized`。

`print()` 与 `return` 是不同操作。

`show_score(82)` 在屏幕上输出 `82`，但没有 `return`，因此返回值为 `None`，`print(result)` 输出 `None`。

```python
def show_score(score):
    print(score)

result = show_score(82)

print(result)
```

函数执行到末尾而没有 `return` 时会返回 `None`。屏幕上的 `82` 不会保存在 `result` 中。计算 `result + 1` 会因 `None` 不能与整数相加而引发 `TypeError`。

## 复用重复计算

为重复计算命名，可以显露代码意图。

对四个分数应用 `normalize_score()`，输出 `[0.82, 0.75, 0.91, 0.68]`。循环逐个取分数，函数将每个分数除以 100。

```python
def normalize_score(score):
    return score / 100

scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(normalize_score(score))

print(normalized_scores)
```

简单计算不一定要拆成函数。但在多处使用相同计算，或命名能让意图更清楚时，函数很有用。

### 处理单个样本

AI 练习中经常使用处理单个样本的函数。

检查样本是否同时具有 `"text"` 和 `"label"` 键。本例两者都有，因此输出 `True`。

```python
def has_required_keys(sample):
    return "text" in sample and "label" in sample

sample = {"text": "AI is useful", "label": "positive"}

print(has_required_keys(sample))
```

该函数只检查键是否存在。`{"text": "", "label": None}` 也会得到 `True`，不会检查文本是否为空或标签值是否允许。

同一函数可以处理多个样本。

对三个样本应用相同键检查。第二个缺少 `"label"`，因此结果列表只保留第一个和第三个字典。

```python
def has_required_keys(sample):
    return "text" in sample and "label" in sample

samples = [
    {"text": "AI is useful", "label": "positive"},
    {"text": "missing label"},
    {"text": "Models can fail", "label": "negative"},
]

samples_with_keys = []

for sample in samples:
    if has_required_keys(sample):
        samples_with_keys.append(sample)

print(samples_with_keys)
```

### 形参默认值

函数形参可以设置默认值。

默认阈值 `60` 下，分数 `82` 返回 `pass`；指定 `threshold=90` 则返回 `fail`。两次调用仅阈值不同。

```python
def pass_or_fail(score, threshold=60):
    if score >= threshold:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(82, threshold=90))
```

第一次调用未传阈值，因此使用 `60`；第二次明确指定 `threshold=90`。

AI 工具和库中经常出现这种形式。

- `batch_size=32`
- `learning_rate=0.001`
- `shuffle=True`
- `max_tokens=100`

默认值很方便，但不了解默认设置就可能误判代码行为，因此应查看库文档中的默认值。

### 传递函数对象

Python 函数也是对象，函数名指向该对象。

`normalize = normalize_score` 为函数对象增加一个名称，`normalize(82)` 也会输出 `0.82`。

```python
def normalize_score(score):
    return score / 100

normalize = normalize_score

print(normalize(82))
```

`normalize` 没有创建新计算，而是用另一名称指向 `normalize_score`。应区分函数对象 `normalize_score` 与调用结果 `normalize_score(82)`。

把分数 `[82, 75, 91]` 和处理函数 `normalize_score` 一起传入。`apply_to_scores()` 对各分数应用该函数，返回 `[0.82, 0.75, 0.91]`，由外层 `print()` 输出。

```python
def normalize_score(score):
    return score / 100

def apply_to_scores(scores, function):
    results = []
    for score in scores:
        results.append(function(score))
    return results

scores = [82, 75, 91]

print(apply_to_scores(scores, normalize_score))
```

`apply_to_scores()` 同时接收分数列表与函数，在执行 `function(score)` 时调用传入函数来处理当前分数。

这种方式经常用于数据处理和 AI 库。

- 用函数指定排序依据。
- 把预处理函数传给重复处理流程。
- 把评估函数传给训练代码。
- 用回调函数指定特定时刻的操作。

### 函数与方法

`function(value)` 按函数名调用，`value.method()` 则在对象上找到并调用方法。

函数是独立定义的处理单元。方法看起来像附着于某个对象并通过它调用的函数。

对 `" AI is Useful "` 去除空白并转小写。`clean_text(text)` 输出 `ai is useful`，`text.strip()` 输出 `AI is Useful`，`text.lower()` 输出保留首尾空格的 ` ai is useful `。

```python
def clean_text(text):
    return text.strip().lower()

text = " AI is Useful "

print(clean_text(text))
print(text.strip())
print(text.lower())
```

`clean_text(text)` 是独立函数调用，`strip()` 和 `lower()` 是字符串提供的方法。方法同样用括号调用，但方法名前带有目标对象。

| 形式 | 入门说明 | 示例 |
| --- | --- | --- |
| 函数 | 具有名称的独立处理单元 | `clean_text(text)` |
| 方法 | 通过值或对象调用的函数式操作 | `text.strip()` |

### 拆分处理步骤

小函数的输入、处理和输出比较清晰。一个函数承担过多任务，会让代码职责变得模糊。

例如，假设一个函数同时执行以下任务：

1. 读取文件。
2. 删除空行。
3. 把分数转换成数字。
4. 计算平均值。
5. 保存结果。

这种函数看似简单，之后只修改其中一部分却可能很困难。

## 案例：清理空白后排除空文本

清理 `[" AI is Useful ", "", " Models can FAIL "]` 后排除空字符串，输出 `['ai is useful', 'models can fail']`。

```python
def clean_text(text):
    return text.strip().lower()

def is_not_empty(text):
    return len(text) > 0

texts = [" AI is Useful ", "", " Models can FAIL "]
cleaned_texts = []

for text in texts:
    cleaned = clean_text(text)
    if is_not_empty(cleaned):
        cleaned_texts.append(cleaned)

print(cleaned_texts)
```

`clean_text()` 清理一个字符串，`is_not_empty()` 检查是否还剩字符。即使添加三个空格的 `"   "`，清理后也变成空字符串，因此结果不变。若先检查再清理，它的长度为 3，会通过检查。调用顺序会影响结果。

## 案例：改变满分标准

假设把分数除以 100 的代码复制到两处，之后考试满分改为 50。只把一处改为 `/ 50`，同样的 40 分就会在一处得到 `0.8`，另一处得到 `0.4`。

把满分设为形参，就能向同一个函数传入分数与满分。下面 100 分制的 80 分和 50 分制的 40 分都会返回 `0.8`。

```python
def score_ratio(score, maximum):
    return score / maximum

print(score_ratio(80, 100))
print(score_ratio(40, 50))
```

把第二次调用的满分改为 `100`，结果变成 `0.4`。函数可以集中管理公式，但调用方也必须传入正确满分。本函数假定满分为正，分数介于 0 与满分之间。

## 修改输入对象与重新赋值

把列表传入函数后，形参引用该列表。函数内部调用 `append()`，调用方也会看到变化；但仅给形参名称赋一个新列表，不会改变外部名称。

```python
def add_score(scores):
    scores.append(91)

def replace_scores(scores):
    scores = [100]

original = [82, 75]
add_score(original)
print(original)
replace_scores(original)
print(original)
```

两次输出都是 `[82, 75, 91]`。第一个函数修改共享列表，第二个只将内部名称重新绑定到新列表。使用函数时，需要知道它会修改原对象还是返回新结果。

## 列表默认值的共享

`def collect(score, results=[]):` 这样的可变默认值并不会在每次调用时创建空列表。默认值在函数定义时只求值一次，因此上次添加的值可能保留到下次调用。每次需要新结果时，可将默认值设为 `None`，在函数内部创建列表。

```python
def collect(score, results=None):
    if results is None:
        results = []
    results.append(score)
    return results

print(collect(82))
print(collect(75))
```

输出为 `[82]`、`[75]`。两次调用均省略 `results`，因此创建不同列表。反之，若明确传入同一个列表，就会继续向该列表添加。

## 检查清单

- 能读懂以 `def` 开头的函数定义。
- 能区分形参与实参。
- 能解释 `print()` 与 `return` 的差别。
- 能将重复计算提取为函数。
- 能编写处理单个样本的函数并在循环中复用。
- 能解释为函数绑定名称、将函数作为实参传递。
- 能区分函数与方法的调用形式。
- 能说明函数名应表达代码意图。
- 能解释函数如何把重复处理变成有名称的可复用单元。

- 能区分修改输入列表与重新绑定形参，并在每次调用需要新列表时使用 `None` 默认值。

## 来源与参考资料


- Python Software Foundation, [More Control Flow Tools: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。作为 `def`、parameter、`return` 和函数调用示例的官方依据。
- Python Software Foundation, [More Control Flow Tools: Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。用于确认默认参数示例和关于 mutable default 的注意说明。
- Python Software Foundation, [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认函数定义语法、参数列表和函数对象创建的说明。
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。作为说明 Python 中函数可以被当作对象处理的背景依据。
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。作为入门层面区分函数调用和方法调用形状的依据。
