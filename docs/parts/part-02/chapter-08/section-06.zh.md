# P2-8.6 补充学习：第一次遇到类(class)与对象(object)

> Section ID: `P2-8.6`
> Version: `v2026.07.09`

在 P2-8.5 里，我们把函数(function)看成小型复用单元。函数接收输入、进行处理、返回结果。但在阅读 Python 代码时，我们经常会遇到一种看起来和函数调用相似、却又稍微不同的表达。

这里提供一个基础补充说明，用来阅读 `class`、`object`、`method`。这个补充学习整理的是：怎样去读 `value.method()`、`model.fit()` 这样的调用形状。`值(value)`、`类型(type)`、`字典(dictionary)` 的代表性说明仍然放在 P2-8.1、P2-8.3 和[概念词汇表](/AiBook/en/reference/concept-glossary/)里，而这里是在这些内容之上，再加上类和对象的视角。

问题场景：想先用一个最小例子，看看带点(`.`)的调用和普通函数调用到底有什么不同。
输入(input)：字符串 `text = " AI is Useful "`。
期望输出(output)：去掉空格的字符串，以及转换成小写后的字符串。
要确认的概念：像 `value.method()` 这样的形式，是在调用某个值或对象提供的动作。

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

`strip()` 和 `lower()` 看起来也像函数那样用括号调用，但前面多了 `text.`。想读懂这种表达，就必须非常轻量地先了解 object、method、class。

这里不会去讲完整的类语法。它的目标只是：以后读到库代码里的 `value.method()`、`model.fit()`、`dataset.map()` 时，不会在这种形状上停住。

这里会把像 `为什么字符串用 .lower()，而列表用 .append()?` 这样的问题，整理到一个标准里：`对象会根据自己的类型，以方法(method)形式提供相应动作。`

因为这是补充学习，说明会稍微细一点。但目标不是让你现在就能自由设计类，而是让你读懂后面会遇到的 Python 库代码长什么样。

| 术语 | 本节先固定的含义 |
| --- | --- |
| 对象(object) | 一个被我们处理的目标，它同时拥有值以及与这些值相关联的动作 |
| 类(class) | 用来制造这类对象的定义或模板 |
| 方法(method) | 附着在对象上被调用的函数形式动作 |
| 属性(attribute) | 对象拥有的值或名称标签 |
| `value.method()` | 调用某个特定值或对象所提供动作的形状 |

## 本补充学习的范围

这里仅处理 Python 对象和类的入门直觉。值、类型、函数的基础说明会通过 P2-8.1 和 P2-8.5 重新接回，而引用与复制这类由对象共享引起的效果，则会在 P2-8.7 中单独回收。

这里首先要解决的问题是：`对于一个看起来像函数调用、但前面多了一个点的表达，应该用什么标准去读它？`

所以这个补充学习回答下面这些问题。

- 什么是对象(object)？
- 什么是类(class)？
- 方法(method)和函数(function)有什么不同？
- 在 Python 里，值(value)、类型(type)、类(class)是怎样连起来的？
- 为什么在库代码里经常会看到 `model.fit()` 这样的表达？

这里不讨论 inheritance、encapsulation、polymorphism、magic method、class variable、instance variable 的详细规则。

这一节之后的流程也很简单。

- 在 `P2-8.7` 里，我们会再次看由对象共享与引用造成的效果。
- 以后在 AI 库里读到 `model.fit()`、`dataset.map()`、`tokenizer.encode()` 这样的表达时，会重复用到同一套标准。

## 本补充学习的目标

- 能把对象(object)解释成“同时拥有值和动作的目标”。
- 能把类(class)解释成“用来创建对象的定义”。
- 能把方法(method)读成“附着在对象上被调用的函数形式”。
- 能在入门层面说明 `function(value)` 和 `value.method()` 的差别。
- 能从类和方法的角度去读 AI 库里像 `model.fit()`、`model.predict()` 这样的表达。

## 先抓住的标准

在这个补充学习里，最先要抓住的标准是：`带点的调用，是对象所提供的动作。`

| 表达 | 第一种读法 |
| --- | --- |
| `text.lower()` | 字符串对象提供的动作 |
| `scores.append(91)` | 列表对象提供的动作 |
| `model.fit(X, y)` | 模型对象提供训练动作的形式 |
| `sample.text` | 对象拥有的值或属性(attribute) |

所以，这一节的核心不是学会自由设计类，而是建立一种标准：看到 `value.method()` 和 `object.attribute` 时，不会停住。

## 三个基准

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| 对象是一个同时拥有值和动作的处理目标 | 它会成为阅读 `value.method()` 这类调用形状的出发点。 | 把它理解成同时拥有值和方法的对象。 |
| 类是制造这类对象的定义 | 它能解释为什么属性和方法会以一个整体出现。 | 能把它解释成类似“蓝图”的定义。 |
| 这种表达在 AI 库里很常见，因为把模型或数据集当成一个整体来处理很方便 | 它帮助我们从结构上读 `model.fit()`，而不是只盯着语法。 | 理解模型、数据集、设置会像对象一样被处理。 |

## 在 Python 里，很多东西都是对象

Python 官方文档把对象(object)解释成拥有 identity、type、value 的目标。这里先按下面这种方式理解就够了：

对象就是 Python 正在当作值来处理的那个实际目标。

数字、字符串、列表、字典，都可以被读成对象。

问题场景：想通过打印类型来确认，不同种类的值都会被 Python 当作对象处理。
输入(input)：整数、字符串、列表、字典值。
期望输出(output)：依次打印每个值的类型。
要确认的概念：在 Python 里，很多类型的值都是对象，而类型会揭示它们的性质。

```python
score = 82
text = "AI"
scores = [82, 75, 91]
student = {"name": "Kim", "score": 82}

print(type(score))
print(type(text))
print(type(scores))
print(type(student))
```

这里最重要的是 `type()`。每个值都有类型，而在 Python 里，类型会影响它能提供哪些动作。

例如，字符串会提供适合字符串的方法。

问题场景：想看字符串对象提供的方法是怎样被调用的。
输入(input)：带空格和大写字母的字符串 `text`。
期望输出(output)：`strip()` 和 `lower()` 的结果。
要确认的概念：对象会根据自己的类型，以方法的形式提供动作。

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

列表则会提供适合列表的方法。

问题场景：想确认列表对象也拥有适合自己类型的方法。
输入(input)：列表 `scores = [82, 75]` 和要追加的值 `91`。
期望输出(output)：追加值后的列表。
要确认的概念：类型不同，可用的方法也不同。

```python
scores = [82, 75]

scores.append(91)

print(scores)
```

字符串有 `strip()`，列表有 `append()`。因为类型不同，所以能用的动作也不同。

## 类是制造对象的定义

类(class)是用来制造对象的定义。换句话说，它像一个模板，决定某一类对象应该拥有什么数据和什么动作。

Python 的内置类型也可以这样理解。

| 值 | 类型或类 | 常见动作 |
| --- | --- | --- |
| `"AI"` | `str` | `.lower()`, `.strip()` |
| `[1, 2, 3]` | `list` | `.append()`, `.extend()` |
| `{"a": 1}` | `dict` | `.get()`, `.items()` |

读者也可以自己定义类。

问题场景：想看一个最小例子：定义一个类，并用它创建对象。
输入(input)：文本和标签值 `"AI is useful"`、`"positive"`。
期望输出(output)：打印对象的 `text` 和 `label` 属性。
要确认的概念：类是创建对象的定义，而对象可以拥有自己的数据。

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

这段代码定义了一个叫 `Sample` 的类，并创建了一个叫 `sample` 的对象。`sample.text` 和 `sample.label` 就是这个对象所拥有的值。

这里不需要把 `__init__` 的详细规则背下来。关键只是在于：类是用来创建对象的定义，而对象可以持有自己的数据。

## 为什么字典和类读起来会不一样

在 P2-8.3 里，我们说过字典(dictionary)是一种通过 key 查找值的结构。实际上，一条小数据也完全可以用字典来表示。

问题场景：想看一个用字典表示含有文本和标签的小数据示例。
输入(input)：含有 `text` 和 `label` 键的字典 `sample`。
期望输出(output)：打印 `sample["text"]` 和 `sample["label"]` 的值。
要确认的概念：字典是通过 key 查找值的最直接数据表达。

```python
sample = {
    "text": "AI is useful",
    "label": "positive",
}

print(sample["text"])
print(sample["label"])
```

如果把同样的数据改用类来表示，就会是下面这样。

问题场景：想比较同一份数据改成类对象之后，形状会发生什么变化。
输入(input)：类 `Sample` 和构造实参 `"AI is useful"`、`"positive"`。
期望输出(output)：打印 `sample.text` 和 `sample.label` 的值。
要确认的概念：类对象通过属性访问来读取数据，而不是通过 key 查找。

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

两段代码都保存了文本和标签，但阅读感觉不同。

| 视角 | 字典(dictionary) | 由类创建的对象 |
| --- | --- | --- |
| 中心思路 | 用 key 找值 | 造出某一类目标 |
| 访问形式 | `sample["text"]` | `sample.text` |
| 结构显式性 | key 名字在运行时被确认 | 类名直接揭示目标含义 |
| 添加动作 | 常与独立函数配合 | 方法(method)可以放进对象里 |
| 适合场景 | 简单数据、JSON、配置值 | 同时处理状态和动作的目标 |

在最开始，字典更容易。实际数据文件和 API 响应也常常像字典一样来读。所以这本书先讲了字典。

类变得必要的时刻，是“我们不只想有数据，还想把和这份数据一起运行的动作也捆在一起”。

## 把状态(state)和动作(behavior)捆在一起

在解释对象时，经常会出现 `state` 和 `behavior` 这两个词。

状态(state)是对象当前持有的值。

动作(behavior)是这个对象能做的事。

下面这个例子展示的是：一个文本样本既有自己的状态，也有一个可以检查自身状态的动作。

问题场景：想通过一个类的例子确认对象会同时拥有值和动作。
输入(input)：带有文本和标签的 `TextSample` 对象。
期望输出(output)：对象的 `text` 值和 `is_labeled()` 结果。
要确认的概念：状态是对象拥有的值，动作则是对象提供的方法。

```python
class TextSample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def is_labeled(self):
        return self.label is not None

sample = TextSample("AI is useful", "positive")

print(sample.text)
print(sample.is_labeled())
```

这里，`sample.text` 和 `sample.label` 是对象的状态。`sample.is_labeled()` 是它的动作。

同样的事情也可以用函数来完成。

问题场景：想看同样的标签检查也能用函数和字典组合来表达。
输入(input)：带有 `label` 键的样本字典。
期望输出(output)：`is_labeled(sample)` 结果 `True`。
要确认的概念：即使不用类，也可以用函数和字典做出类似的处理结构。

```python
def is_labeled(sample):
    return sample["label"] is not None

sample = {"text": "AI is useful", "label": "positive"}

print(is_labeled(sample))
```

不能说哪一种永远更好。关键是结构的目的。

| 目的 | 更简单的做法 |
| --- | --- |
| 直接读取 JSON 一类的数据 | 字典 |
| 通过 key 快速找多个值 | 字典 |
| 把数据和动作作为同一个目标来处理 | 类 |
| 使用库提供的有状态目标 | 基于类的对象 |

在 AI 实践前期，字典和函数往往已经够用了。但一旦开始使用库，模型、数据集、分词器、优化器这样的目标往往会以对象形式提供。它们持有内部状态，方法会基于这些状态运行。

## 方法看起来像“附着在对象上的函数”

函数(function)通常这样调用：

问题场景：想先看独立函数调用是什么样，再和方法调用比较。
输入(input)：字符串 `" AI "`。
期望输出(output)：清理后的字符串。
要确认的概念：`function(value)` 是把值送进函数里处理的调用形式。

```python
def clean_text(text):
    return text.strip().lower()

print(clean_text(" AI "))
```

方法(method)则是附着在对象上被调用。

问题场景：想看同样的字符串清理，换成方法调用时是什么样子。
输入(input)：字符串 `text = " AI "`。
期望输出(output)：`text.strip()` 的结果。
要确认的概念：方法是以点前对象为中心被调用的。

```python
text = " AI "

print(text.strip())
```

两种写法都会执行动作，但调用中心不同。

| 表达 | 调用中心 | 读法 |
| --- | --- | --- |
| `clean_text(text)` | 函数名 | 把 `text` 放进函数里处理 |
| `text.strip()` | 对象 `text` | 调用 `text` 对象提供的 `strip()` 动作 |

我们也可以把方法放进自己定义的类里。

问题场景：想确认自己定义的对象也能拥有自己的方法。
输入(input)：`Sample` 对象和方法 `has_label()`。
期望输出(output)：`sample.has_label()` 的结果 `True`。
要确认的概念：方法也可以放在用户定义类里面。

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def has_label(self):
        return self.label is not None

sample = Sample("AI is useful", "positive")

print(sample.has_label())
```

`sample.has_label()` 是附着在 `sample` 对象上的方法。它看起来像函数，但前面多了一个目标对象。

阅读方法时，下面这些问题会很有帮助。

1. 点(`.`)前面的目标是什么？
2. 那个目标持有什么状态？
3. 点后面的这个方法是在读状态，还是在改状态？
4. 括号里额外传进去的值是什么？

例如看到 `model.predict(test_data)` 时，可以这样读：

| 问题 | 回答 |
| --- | --- |
| 点前的目标 | `model` |
| 目标的意义 | 很可能是一个训练好的模型对象 |
| 点后的方法 | `predict()` |
| 传进去的值 | `test_data` |
| 整体解释 | 模型对象对测试数据执行预测动作 |

## `self` 是指向对象自身的名字

在 Python 类例子里，我们会经常看到 `self` 这个名字。

问题场景：想用一个最小例子看清 `self` 在类内部究竟占据什么位置。
输入(input)：`Sample` 类的 `__init__` 方法和输入 `text`。
期望输出(output)：一个把 `self.text` 存进对象内部的类定义。
要确认的概念：`self` 是在方法里指向对象自己的惯例名称。

```python
class Sample:
    def __init__(self, text):
        self.text = text
```

这里可以把 `self` 理解成“当前正在被创建或使用的那个对象自己”。`self.text = text` 的意思，就是“把 `text` 这个值存到这个对象内部”。

如果先学过别的语言，可以把它理解成有点像 `this`。不过 Python 的显眼之处在于：方法定义里会显式写出 `self`。

现在只需要先记住下面这些就够了。

- `self` 是惯例名称。
- 它用于在方法内部读取或修改对象自己的值。
- 像 `sample.has_label()` 这样调用时，不需要手动传入 `self`。

如果觉得 `self` 还陌生，可以对比下面两行。

问题场景：想把类外看到的属性访问和类内使用的 `self` 联系起来。
输入(input)：由 `Sample("AI is useful", "positive")` 创建出来的对象 `sample`。
期望输出(output)：打印 `sample.label` 的值。
要确认的概念：在类外写 `sample.label`，在类内则把同一个位置写成 `self.label`。

```python
sample = Sample("AI is useful", "positive")

print(sample.label)
```

`sample.label` 是读取 `sample` 对象内部 `label` 值的表达。类内部则把这个对象叫作 `self`。

问题场景：想再次确认在类内部是怎样通过 `self.label` 这样的形式保存属性的。
输入(input)：`Sample` 类的 `__init__` 方法。
期望输出(output)：一个保存 `self.text` 与 `self.label` 的类定义。
要确认的概念：类内部通过 `self` 来处理对象自身属性。

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label
```

也就是说，从类外看是 `sample.label`，从类内看则是 `self.label`。先把这个对应关系牢牢抓住就够了。

## 类总是必要的吗？

不是。学习 Python 并不意味着所有代码都必须写成类。

在这里，更实用的标准是下面这样。

| 情况 | 先考虑的方式 |
| --- | --- |
| 计算一个值 | 函数 |
| 按顺序处理多个值 | 列表 |
| 通过名字查找值 | 字典 |
| 重复同样的处理 | 循环与函数 |
| 需要构造同时拥有状态与动作的目标 | 类 |

类很强大，但如果太早使用，结构会变重。相反，在阅读库代码时，我们往往避不开类和对象。这里更关注的不是“把所有东西都做成类”，而是“能够读懂由类构成的代码”。

## 为什么 AI 库里经常会出现类和方法

在 AI 实践里，我们经常会看到下面这样的代码。

问题场景：想先用最简单的方式看看 AI 库里常见的方法调用长什么样。
输入(input)：`model`、`train_data`、`test_data`。
期望输出(output)：类似 `model.fit(...)`、`model.predict(...)` 的调用示例。
要确认的概念：因为库对象同时拥有状态和动作，所以方法调用形状会很常见。

```python
model.fit(train_data)
predictions = model.predict(test_data)
```

这段代码会随着具体库不同而不同，但读法很相似。

| 表达 | 入门解释 |
| --- | --- |
| `model` | 模型对象 |
| `.fit()` | 执行训练的方法 |
| `.predict()` | 执行预测的方法 |
| `train_data`, `test_data` | 传给方法的数据 |

为什么会用这种方式？因为模型并不只是一个简单函数。它可能持有很多状态：学到的参数、配置项、内部结构、预处理信息都可能一起存在于对象内部。所以库会把模型做成对象，再把 `fit()`、`predict()`、`save()` 等方法附着到这个对象上。

这个视角在后面阅读机器学习库和深度学习框架时很重要。

- 函数会把一种处理用名字分开。
- 对象可以把状态和动作绑在一起。
- 类是用来创建这种对象的定义。
- 方法是附着在对象上被调用的动作。

这里可以先这样读。

问题场景：想再用一行例子固定 `fit()` 方法调用的读法。
输入(input)：`model`、`train_data`。
期望输出(output)：`model.fit(train_data)` 这一行。
要确认的概念：方法调用可能是在改变对象状态，或者使用对象状态。

```python
model.fit(train_data)
```

这里有一个叫 `model` 的对象，这个对象在运行一个叫 `fit()` 的方法。此时 `fit()` 可能不仅是简单计算，它还可能改变模型对象内部的状态。例如，学到的参数可能会被存进对象里。

问题场景：想用一行例子看看预测方法是怎样使用“已学到的对象状态”的。
输入(input)：`model`、`test_data`。
期望输出(output)：`predictions = model.predict(test_data)` 这一行。
要确认的概念：方法可以利用对象状态来做出结果。

```python
predictions = model.predict(test_data)
```

`predict()` 会利用已经训练好的模型对象状态来产生预测结果。所以，我们不能只盯着一个函数本身，还要一起想：对象现在持有什么状态。

这个视角在后面的机器学习里非常重要。

- 训练前的模型和训练后的模型，看起来可能是同一个对象，但内部状态可以完全不同。
- `fit()` 可能是会改变状态的方法。
- `predict()` 可能是利用状态来生成结果的方法。
- `save()` 可能是把状态保存到文件的方法。

## 本节要记住的视角

- 在 Python 里，很多值都会被当作对象(object)处理。
- 类(class)是用来创建这些对象的定义。
- 方法(method)是附着在对象上被调用的动作。
- `function(value)` 和 `value.method()` 看起来相似，但阅读方向不同。
- 以后再看到 `model.fit()`、`model.predict()`、`dataset.map()` 时，先问：`这个对象把哪些状态和动作绑在一起了？`

最好不要从困难的语法开始学类。先把 Python 代码里出现的调用形状区分开就够了。

`function(value)` 是“把值送进函数”的形状。

`value.method()` 是“调用这个值或对象提供的动作”的形状。

当我们在 AI 库里看到 `model.fit()` 这样的表达时，可以先读成：`模型对象调用了它的训练方法`。仅凭这一点，读很多代码时就不会一开始停住。

只要把下面这些标准回收回来，这个补充学习就可以安全接回正文。

| 这里要回收的内容 | 要回到正文的哪个问题 | 继续读哪里 |
| --- | --- | --- |
| `function(value)` 与 `value.method()` 的调用中心差异 | 为什么不同值和类型会使用不同动作 | 值、变量、类型在 P2-8.1，列表和字典在 P2-8.2 到 P2-8.3 |
| `model.fit()` 这类表达其实是对象方法调用 | 在库代码里该怎样读点(`.`)前面的目标 | 函数在 P2-8.5，后续库示例在 Part 3 正文 |

也就是说，只要我们能读出点(`.`)前面的目标是什么，并且知道方法是附着在对象上的动作，就不必在这里停留太久，而应该回到正文继续前进。

## 通过案例来看

### 案例 1. 为什么 `model.fit()` 看起来不像普通函数

假设一个学习者第一次在机器学习示例里看到 `model.fit(train_data)` 和 `model.predict(test_data)`。人很自然地可能会期待一种像 `fit(model, train_data)` 那样的函数形式，然后在看到点调用时停住。

这时重要的不是去死记语法，而是读调用中心。`model` 很可能是一个持有状态的对象，`fit()` 可能是在改变这个对象状态的动作，而 `predict()` 则可能是在利用这个状态生成结果。

所以，第一次遇到类和对象时，必须先抓住两个标准：`对象同时拥有值和动作`，以及 `方法是附着在对象上被调用的`。字符串里的 `text.strip()` 和模型里的 `model.fit()` 虽然复杂度差很多，但它们共享同一种调用形状。

可以验证的一点是：只要点前的目标变了，动作含义也会跟着变。`text.lower()` 处理字符串，`scores.append(91)` 修改列表，而 `model.predict(test_data)` 使用模型状态。只要能读懂点前目标是什么，代码解释就会容易很多。

## 简短检查

- 能把对象解释成 `同时拥有值和动作的目标` 吗？
- 能说出类和对象的区别吗？
- 能区分 `function(value)` 和 `value.method()` 吗？
- 能说明为什么像 `model.fit()` 这样的表达需要用类和方法视角来读吗？
- 能把对象解释成 Python 处理值时面对的实际目标吗？
- 能把类解释成“创建对象的定义”吗？
- 能把方法解释成附着在对象上的函数形式吗？
- 能在入门层面说明字典和类对象的差别吗？
- 能通过例子说明“状态和动作被绑在一起”是什么意思吗？
- 能说明 `function(value)` 和 `value.method()` 的调用中心差异吗？
- 能把 `self` 解释成“指向对象自己的名字”吗？
- 能说明类并不总是必要，有些情况函数和字典就够了吗？
- 能从对象和方法的角度读懂 AI 库里的 `model.fit()`、`model.predict()` 吗？

## 什么时候该先想起这个视角

- 当需要重新理解为什么像 `model.fit()`、`text.lower()` 这样的点调用看起来和普通函数不一样时，先想起它。
- 当需要用“对象同时拥有值和动作”的视角，把字符串、列表、模型对象放进同一个框架时，先想起它。
- 当需要重新判断“字典和类对象哪一个更自然”时，先按数据和动作结合得有多紧来思考。

## 来源与参考资料

- Python Software Foundation, [Classes](https://docs.python.org/3/tutorial/classes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-06-25.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-06-25.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-06-25.
