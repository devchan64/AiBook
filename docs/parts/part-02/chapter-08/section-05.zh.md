# P2-8.5 函数(function)与小规模复用

> Section ID: `P2-8.5`
> Version: `v2026.07.20`

在 P2-8.1 里，我们看了值(value)、变量(variable)、类型(type)。从 P2-8.2 到 P2-8.4，我们看了如何通过列表(list)、字典(dictionary)、循环(loop)来处理多个值。

现在还剩下一个问题：

如果同一种处理要反复使用很多次，该怎么办？

在 Python 里，我们使用函数(function)。函数是一种结构：它给重复处理起名字，接收需要的值，完成计算，然后把结果返回出去。

这里解释 `函数(function)`、`参数(parameter)`、`实参(argument)`、`返回值(return value)` 之间的基本区分。`值(value)`、`变量(variable)`、`循环(loop)` 的代表性说明仍然放在 P2-8.1、P2-8.4 和[概念词汇表](/AiBook/en/reference/concept-glossary/)里，而这里集中在把输入-处理-输出契约读成一个可复用的小单元。

这一节不会要求把函数语法全部背下来，而是建立这样一种感觉：数学里的函数和 Python 函数怎样相似、又怎样不同；以及怎样把一小段数据处理代码切分成可以复用的单位。

更一般地说，函数就是把 `输入、处理、输出` 打包成一个单元的方法。Python 语法只是表达这种单元的一种方式，而同样的视角也会继续延伸到数学函数、模型函数、API 函数、库函数。

这里不是去学函数的高级特性，而是把前一节里的循环和数据结构处理重新打包成小的复用单元。如果之前我们是分别阅读列表、字典、循环，那么这里就是进入“给那段处理流程起名，从而可以再次使用”的位置。先抓住这个把手，后面再看库函数或模型 API 时，就会更容易先读懂 `输入-处理-输出契约`，而不是先被 `语法` 卡住。

| 术语 | 本节先固定的含义 |
| --- | --- |
| 函数(function) | 接收输入、进行处理并返回结果的有名字代码单元 |
| 参数(parameter) | 定义函数时写下的输入名称 |
| 实参(argument) | 调用函数时实际传入的值 |
| 返回值(return value) | 函数计算后返回到外部的结果 |
| 方法(method) | 附着在某个值或对象上被调用的函数形式 |

## 核心判断标准：函数(function)与小规模复用

- 能读懂使用 `def` 定义函数的基本形式。
- 能区分参数(parameter)和实参(argument)。
- 能说明 `return` 是把函数结果返回出去的语法。
- 能把重复计算和数据处理拆成小函数。
- 能说明数学函数和 Python 函数的差别。
- 能说明 Python 函数也可以像值一样被放进变量里，并传递给其他函数。
- 能在入门层面区分函数(function)和方法(method)在调用形式上的不同。

## 学习背景

这里先看的是 `怎样给重复处理起名并再次使用`，而不是先背函数语法。下面三个基准会成为后面阅读库函数和方法的基础。

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| 函数把输入、处理、输出打包成一个单元 | 它让我们能在同一个大框架里阅读数学函数和代码函数。 | 理解它是“接收值并返回结果的有名字代码”。 |
| 如果同一种处理不断重复，拆成函数更容易阅读 | 它帮助我们理解为什么小型数据处理代码会变成可复用结构。 | 能把通关判断、归一化这类计算读成函数。 |
| `print` 和 `return` 的角色不同 | 这对区分执行输出和计算结果很重要。 | 能解释“显示在屏幕上”和“返回给下一步计算”不是一回事。 |

## 主要学习内容

### 函数是把处理单元用名字分开的方法

一般来说，函数(function)就是一个单元：接收输入，进行处理，然后把结果返回出去。数学更强调输入与输出的关系，而编程则把这种关系写成真正能运行的代码。

在 Python 里，我们用 `def` 给函数起名字，并把需要的输入名写成参数(parameter)。

下面的代码按分数判断是否通过。

问题场景：在拆成函数之前，先看一段直接判断单个分数的代码。
输入(input)：分数值 `82`。
期望输出(output)：字符串 `pass`。
要确认的概念：重复判断也可以先用普通条件语句表达。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
score = 82

if score >= 60:
    result = "pass"
else:
    result = "fail"

print(result)
```

如果这种判断只写一次，完全可以保持原样。但如果要对很多分数反复做同样的判断，代码就会开始重复。

如果用函数，我们就能给这段处理起名字。

问题场景：想看一个把同样的通过/不通过判断打包成函数，以便多次复用的例子。
输入(input)：函数 `pass_or_fail` 和分数 `82`、`55`。
期望输出(output)：分别得到 `pass`、`fail`。
要确认的概念：函数能给重复处理起名字，并让它再次使用。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def pass_or_fail(score):
    if score >= 60:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(55))
```

`pass_or_fail` 是函数名。`score` 是函数内部使用的输入名。`return` 会把结果送回函数外部。

在这一节里，我们用下面这个标准来理解函数：

函数是“接收输入、进行处理、返回结果的有名字代码”。

| 视角 | 一般说明 | 在 Python 里 |
| --- | --- | --- |
| 函数(function) | 把输入、处理、输出打包成一个单元 | 用 `def` 定义 |
| 输入 | 函数要处理的值 | 要区分参数(parameter)和实参(argument) |
| 输出 | 交给下一步计算的结果 | 用 `return` 返回 |

### 数学函数与 Python 函数

在数学里，函数通常通过输入与输出的关系来说明。

$$
f(x) = x + 1
$$

换成 Python，可以写成这样。

问题场景：想看最小的例子，把数学函数 \(f(x)=x+1\) 搬成 Python 函数。
输入(input)：输入值 `3`。
期望输出(output)：`4`。
要确认的概念：数学函数的输入-输出关系，也可以用 Python 的函数形式表达。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def f(x):
    return x + 1

print(f(3))
```

两者确实相似。都有输入 `x`，也都有结果。

但它们并不完全相同。

| 视角 | 数学函数 | Python 函数 |
| --- | --- | --- |
| 核心关注 | 输入与输出的关系 | 真正运行的代码与结果 |
| 表达形式 | \(f(x) = x + 1\) | `def f(x): return x + 1` |
| 副作用(side effect) | 通常看成纯关系 | 可以打印、存文件、修改列表 |
| 错误 | 超出定义域时按数学处理 | 可能出现类型错误、键错误、运行错误 |

在 AI 实践里，这两种视角都需要。

- 损失函数(loss function)需要按数学关系理解。
- Python 函数让我们能在代码里复用那个计算。
- 库函数则让我们即使不知道内部实现，也能根据输入-输出契约来使用它。

### 区分参数与实参

既然已经看到数学函数和 Python 函数都会接收输入，现在就可以区分 Python 文档里常见的术语了。学习函数时，经常会遇到 parameter 和 argument。

问题场景：想通过一个真实调用例子区分参数和实参。
输入(input)：函数 `add_bonus(score, bonus)` 与调用时传入的 `80`、`5`。
期望输出(output)：相加后的结果 `85`。
要确认的概念：定义函数时写的名字是参数，调用时实际传入的值是实参。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def add_bonus(score, bonus):
    return score + bonus

result = add_bonus(80, 5)

print(result)
```

在这段代码里，`score` 和 `bonus` 是参数(parameter)。它们是函数定义内部用来称呼输入值的名字。

`80` 和 `5` 是实参(argument)。它们是调用函数时真正传进去的值。

| 区分 | 所在位置 | 示例 |
| --- | --- | --- |
| 参数(parameter) | 定义函数时写下的名字 | `score`, `bonus` |
| 实参(argument) | 调用函数时实际放进去的值 | `80`, `5` |
| 返回值(return value) | 函数送回来的结果 | `85` |

这种区分会在之后阅读模型函数、损失函数、API 函数、库函数文档时反复出现。

### `return` 会把结果返回出去

`return` 是一种语法：把函数计算出来的结果送回到调用它的位置。

问题场景：想看一个函数计算结果被下一步计算继续使用的例子。
输入(input)：分数 `82`。
期望输出(output)：归一化结果 `0.82`。
要确认的概念：`return` 会把函数结果返回给调用者。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def normalize_score(score):
    return score / 100

normalized = normalize_score(82)

print(normalized)
```

当 `normalize_score(82)` 运行时，结果 `0.82` 会被返回。然后这个结果被放进名为 `normalized` 的变量里。

`print()` 和 `return` 是不同的。

问题场景：想比较“屏幕上显示的东西”和“真正返回的值”之间的区别。
输入(input)：分数 `82`。
期望输出(output)：函数内部会打印 `82`，但外部变量 `result` 会得到 `None`。
要确认的概念：`print()` 是显示输出，而 `return` 是传递计算结果。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def show_score(score):
    print(score)

result = show_score(82)

print(result)
```

这个函数会在屏幕上打印 `82`，但它没有返回值。在 Python 里，如果没有显式返回某个值，结果通常会被读成 `None`。

在这一节里，我们要区分下面两件事。

- `print()` 是给人看的输出。
- `return` 是把结果送给下一步计算。

## 细部学习内容

### 把重复计算拆成函数

只要给重复计算起名字，代码意图就会更清楚。

问题场景：想看一个把分数归一化拆成函数，并在循环里复用的例子。
Input: 分数列表 `scores`。
期望输出(output)：归一化后的分数列表 `normalized_scores`。
要确认的概念：如果同一个计算出现在循环里，拆成函数会让意图更清晰。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def normalize_score(score):
    return score / 100

scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(normalize_score(score))

print(normalized_scores)
```

现在，比起 `score / 100` 这个表达式本身，`normalize` 的意图会更先被看见。

当计算非常简单时，不一定非得拆成函数。但如果同样的计算会在多个地方反复使用，或者给它一个名字会让意图更明确，那么函数就会变得有用。

### 处理单条数据的函数

在 AI 实践里，我们经常会创建“处理一条样本(sample)”的函数。

问题场景：想看一个检查单个样本是否具备所有必要键的函数。
输入(input)：一个带有 `text`、`label` 键的样本字典。
期望输出(output)：有效性结果 `True`。
要确认的概念：函数可以把“检查一条数据”的规则封装起来。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def is_valid_sample(sample):
    return "text" in sample and "label" in sample

sample = {"text": "AI is useful", "label": "positive"}

print(is_valid_sample(sample))
```

这个函数检查样本里是否有 `text` 和 `label` 两个键。

它也可以被应用到很多样本上。

问题场景：想看一个把刚才创建的样本检查函数重复应用到多个样本上的例子。
输入(input)：样本字典列表 `samples`。
期望输出(output)：只保留有效样本的 `valid_samples`。
要确认的概念：当“处理一条数据的函数”和循环结合时，它的复用价值会明显变大。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def is_valid_sample(sample):
    return "text" in sample and "label" in sample

samples = [
    {"text": "AI is useful", "label": "positive"},
    {"text": "missing label"},
    {"text": "Models can fail", "label": "negative"},
]

valid_samples = []

for sample in samples:
    if is_valid_sample(sample):
        valid_samples.append(sample)

print(valid_samples)
```

这个结构虽然小，但很重要。

- 循环会把多个样本一个一个取出来。
- 函数负责检查一条样本。
- 条件语句根据检查结果改变处理方式。

这种小组合，会成为后面预处理(preprocessing)、评估(evaluation)、筛选(filtering)代码的基本形状。

### 可以设置默认值

函数参数还可以带默认值(default value)。

问题场景：想看一个阈值不常变化的函数里，默认值是如何工作的。
输入(input)：`score`、默认值 `threshold=60`、以及显式传入的 `threshold=90`。
期望输出(output)：同一个分数会因为阈值不同而得到不同判定。
要确认的概念：默认参数让函数即使省略某个实参，也能保持默认行为。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def pass_or_fail(score, threshold=60):
    if score >= threshold:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(82, threshold=90))
```

第一次调用没有单独给阈值，所以会用 `60`。第二次调用则显式写了 `threshold=90`。

在 AI 工具和库里，我们也经常会看到这种形状。

- `batch_size=32`
- `learning_rate=0.001`
- `shuffle=True`
- `max_tokens=100`

默认值很方便，但如果不知道默认值是什么，就可能误解代码行为。所以，需要养成查看库文档里默认值的习惯。

### Python 函数也能像值一样被对待

如果先学过 C 或 Java，Python 函数可能会显得有点不同。在 Python 里，函数也是对象(object)。所以函数名不只是代码位置的标签，它也可以被看成“指向函数对象的名字”。

例如，我们可以把函数放到另一个名字里。

问题场景：想确认函数也能像值一样放到另一个变量名里再调用。
输入(input)：函数 `normalize_score` 和新名字 `normalize`。
期望输出(output)：`normalize(82)` 得到 `0.82`。
要确认的概念：Python 函数是对象，因此可以被放进变量里，用另一个名字来引用。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def normalize_score(score):
    return score / 100

normalize = normalize_score

print(normalize(82))
```

`normalize` 并没有创建新的计算，它只是用另一个名字指向了同一个函数对象。这种感觉可能一开始比较陌生，但在 Python 库代码里经常出现。

函数也可以作为实参传给另一个函数。

问题场景：想看一个把函数本身作为实参传给另一个函数，再在公共循环逻辑里应用的例子。
输入(input)：分数列表 `scores` 和函数 `normalize_score`。
期望输出(output)：`apply_to_scores` 产生的归一化分数列表。
要确认的概念：在 Python 里，函数也可以像其他值一样被传递。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
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

在这个例子里，`apply_to_scores()` 同时接收一组分数和一个函数。然后它把那个函数应用到每一个分数上。这里的函数不再只是“会执行的代码片段”，也像一种“可以被传递的值”。

这种方式会在后面的数据处理和 AI 库里经常出现。

- 排序标准会以函数形式传入。
- 预处理函数会传给重复处理逻辑。
- 评估函数(metric function)会传给训练代码。
- callback 函数会指定某个时刻该发生什么行为。

这一节不讨论高级函数式编程(functional programming)。当前正文里也不会把函数式编程单独扩展开来，这里所需的范围只到 `函数也可以像值一样传递` 这一点为止。不过，只要先知道 Python 里的函数可以像值一样传递，读库 API 时就会没那么陌生。

### 函数和方法的调用中心不同

在阅读 Python 代码时，我们会同时看到 `function(value)` 这种调用，以及 `value.method()` 这种调用。这里不进入类(class)的详细概念，只区分函数(function)和方法(method)的调用形状。

函数(function)是独立定义出来的处理单元。

问题场景：为了区分独立函数与方法调用，先看函数一侧的例子。
输入(input)：字符串 `text`。
期望输出(output)：去除空格并转换成小写后的字符串。
要确认的概念：函数是通过独立名称被调用的处理单元。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
def clean_text(text):
    return text.strip().lower()
```

方法(method)则看起来像“附着在某个对象上的函数”。

问题场景：想比较即使是类似的字符串处理，方法调用会是什么样子。
输入(input)：字符串 `text = " AI is Useful "`。
期望输出(output)：分别打印 `strip()` 和 `lower()` 的结果。
要确认的概念：方法是附着在值或对象上被调用的函数形式。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

这里的 `strip()` 和 `lower()` 是字符串对象提供的方法。它们和函数一样带括号调用，但前面多了一个目标对象。

在这一节里，先记住下面这个层次就够了。

| 表达 | 入门说明 | 例子 |
| --- | --- | --- |
| 函数(function) | 独立的、有名字的处理单元 | `clean_text(text)` |
| 方法(method) | 附着在值或对象上被调用的函数形式 | `text.strip()` |

类(class)和对象(object)会在 P2-8.6 的补充学习里再回来。这里先只区分：`function(value)` 和 `value.method()` 虽然都表示“调用某个行为”，但调用的中心并不一样。

### 如果一个函数做的事情太多，就把它拆开

小函数能让输入、处理、输出更清楚。相反，如果一个函数做的事情太多，它负责的范围就会开始模糊。

例如，想象下面这些工作全部塞进一个函数里：

1. 读文件。
2. 删除空行。
3. 把分数转成数字。
4. 计算平均值。
5. 保存结果。

这种函数一开始看起来也许还算简单，但以后要改其中某一部分时就会变得很困难。

在这一节里，当我们考虑要不要拆分函数时，会问下面这些问题。

- 这个函数只做一件事吗？
- 函数名能不能准确说明它的实际行为？
- 输入和输出是否清楚？
- 屏幕输出和返回结果有没有混在一起？
- 同样的处理是不是已经在很多地方重复出现？

这些标准在 AI 实践里也很有用。只要把数据加载、预处理、模型执行、评估稍微分开，找错误就会容易得多。

## 案例与示例

### 一个小复用示例

下面这个例子会对文本样本做很轻量的整理，并只保留非空样本。

问题场景：想看一个把两个小函数组合起来，对多条文本进行清理与筛选的例子。
输入(input)：包含空格和空字符串的文本列表 `texts`。
期望输出(output)：只保留整理后且非空文本的 `cleaned_texts`。
要确认的概念：函数会制造小的处理单元，而循环则把这些单元应用到多条数据上。

```python
# 这个例子用来确认函数如何作为小型复用单位连接输入和输出。
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

这段代码从 Python 语法上看很简单，但它展示了一个重要的数据处理流程。

- `clean_text()` 清理一条文本。
- `is_not_empty()` 检查一条文本。
- 循环把同样的处理应用到多条文本上。
- 结果被放进一个新的列表里。

当许多这样的“小函数”积累起来之后，它们就会帮助我们理解后面出现的 Pandas、NumPy 和机器学习库代码。

### 案例 1. 为什么同样的归一化计算不该一直复制粘贴

假设一个学习者把“分数归一化”代码复制到了好几个笔记本单元里。刚开始看起来也许很快，但以后只要归一化标准需要改变，就必须重新找回所有单元并逐个修改。

人的第一反应可能会是：`这段很短，那就再写一遍吧。` 但一旦同样的处理开始重复，与其盯着那个计算式本身，不如先把“这段处理到底在做什么工作”分离成一个有名字的单元，这样会更容易阅读，也更容易修改。

函数正是在这个位置变得必要。只要把输入、处理、输出打包成一个单元，并给它一个名字，那么重复使用同一计算时，就能减少代码重复，也能更清楚地表达意图。区分 `print` 和 `return` 的原因，也是在于要把“给人看”的输出和“交给下一步计算”的结果分开。

这种结构的可验证结果，会直接体现在“需要修改的地方数量”上。如果改变归一化标准时，只需要修改一个函数，而所有调用结果都会一起改变，那就说明复用结构比简单复制代码更合理。

## 练习与例子

下面这些小练习足以重新确认本节的核心。

- 写一个接收单个分数并返回等级的函数，然后把它反复应用到多个分数上。
- 分别写一个只使用 `print()` 的函数和一个使用 `return` 的函数，然后比较结果差异。
- 把“清理单个字符串的函数”和“检查是否为空的函数”拆开，再去筛选多条文本。

## 检查清单

- 能读懂以 `def` 开头的函数定义。
- 能区分参数(parameter)和实参(argument)。
- 能解释 `print()` 和 `return` 的区别。
- 能把重复计算拆成函数。
- 能写一个处理单条数据的函数，并在循环里复用它。
- 能说明 Python 函数可以被放进变量，也可以作为实参传给别的函数。
- 能解释函数(function)和方法(method)在调用形状上的不同。
- 能说明函数名应该揭示代码意图。
- 能说明函数为什么会把重复处理变成有名字的可复用单元。

## 来源与参考资料

- Python Software Foundation, [More Control Flow Tools: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。作为 `def`、parameter、`return` 和函数调用示例的官方依据。
- Python Software Foundation, [More Control Flow Tools: Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认默认参数示例和关于 mutable default 的注意说明。
- Python Software Foundation, [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认函数定义语法、参数列表和函数对象创建的说明。
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。作为说明 Python 中函数可以被当作对象处理的背景依据。
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。作为入门层面区分函数调用和方法调用形状的依据。
