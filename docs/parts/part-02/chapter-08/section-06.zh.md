# P2-8.6 补充学习：初识类与对象

> Section ID: `P2-8.6`
> Version: `v2026.09.15`

`text.lower()` 将字符串转为小写，`scores.append(91)` 则向列表添加值。点号（`.`）前是目标对象，后是方法名称。可用操作取决于对象类型。

## 对象与类型

Python 对象具有标识、类型和值。数字、字符串、列表、字典也都是对象。代码依次输出 `<class 'int'>`、`<class 'str'>`、`<class 'list'>`、`<class 'dict'>`。

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

字符串提供 `strip()` 和 `lower()`。分别用于 `" AI is Useful "` 时，输出 `AI is Useful` 和保留首尾空格的 ` ai is useful `。

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

这两个方法返回处理后的字符串，不修改原 `text`。列表的 `append()` 则改变原列表：向 `[82, 75]` 添加 `91` 后输出 `[82, 75, 91]`。

```python
scores = [82, 75]

scores.append(91)

print(scores)
```

`text.append(91)` 请求字符串不提供的方法，因此引发 `AttributeError`。

## 类与实例

类（class）定义一类对象可以拥有的数据与行为，由该类创建的个体对象称为实例（instance）。

| 对象示例 | 类 | 方法示例 |
| --- | --- | --- |
| `"AI"` | `str` | `.lower()`、`.strip()` |
| `[1, 2, 3]` | `list` | `.append()`、`.extend()` |
| `{"a": 1}` | `dict` | `.get()`、`.items()` |

可以通过自定义的 `Sample` 类创建带文本和标签的对象。代码输出 `AI is useful`、`positive`。

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

`Sample` 是类，`sample` 是指向所创建实例的名称。`sample.text` 和 `sample.label` 读取该对象的属性。

初始化新实例时调用 `__init__()`。它把传入的 `text`、`label` 保存到 `self.text`、`self.label`，成为对象自身的数据。

## self 与各对象的状态

`self` 是指代方法执行目标实例的惯用形参名称。调用 `sample.method()` 时，目标对象自动传入，调用者无需另写 `self`。

同一类创建的两个对象也能拥有不同值。代码只把第一个对象的标签改为 `positive`，依次输出 `positive`、`None`。

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

first = Sample("good product", None)
second = Sample("new review", None)
first.label = "positive"

print(first.label)
print(second.label)
```

初始化第一个对象时，`self` 指向第一个对象；初始化第二个时，则指向第二个。外部的 `first.label` 在该对象的方法内部就是 `self.label`。

## 字典的键与对象的属性

文本与标签也可以用字典表示。通过键读取两值，输出 `AI is useful`、`positive`。

```python
sample = {
    "text": "AI is useful",
    "label": "positive",
}

print(sample["text"])
print(sample["label"])
```

前面的 `Sample` 对象用 `sample.text` 读取，字典用 `sample["text"]`。字典也是对象，但键与属性的访问方式不同。

| 方面 | 字典 | 自定义 Sample 实例 |
| --- | --- | --- |
| 访问 | `sample["text"]` | `sample.text` |
| 存储 | 将值与键关联 | 把值保存在属性中 |
| 处理 | 可与独立函数配合 | 可在类中定义方法 |
| 用途示例 | 配置、从 JSON 读取的数据 | 具有数据和专用行为的样本 |

类名能表达对象含义，但不会仅凭名称就自动验证属性类型或值。

## 状态与方法

状态是对象当前持有的数据，行为是读取或修改它的处理。`TextSample` 保存文本与标签，用 `is_labeled()` 检查标签是否为 `None`。输出为 `AI is useful`、`True`。

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

把 `sample.label` 改为 `None` 后再次调用 `sample.is_labeled()`，得到 `False`。该方法只检查标签是否不为 `None`，空字符串 `""` 也得到 `True`，并不验证标签内容是否合适。

函数与字典也能表达相同检查。下面检查字典标签 `"positive"`，输出 `True`。

```python
def is_labeled(sample):
    return sample["label"] is not None

sample = {"text": "AI is useful", "label": "positive"}

print(is_labeled(sample))
```

`is_labeled(sample)` 把样本传给函数，`sample.is_labeled()` 则调用样本对象的方法。按键查数据可用字典，需要一起定义状态与专用行为时可用类。

## 获取方法与调用方法

`sample.is_labeled` 获取方法，`sample.is_labeled()` 才执行并取得返回值。在前面的 `TextSample` 定义后运行以下代码，输出 `False`、`True`。

```python
sample = TextSample("new review", None)
check = sample.is_labeled
print(check())
sample.label = "positive"
print(check())
```

`check` 是绑定到 `sample` 的方法。第一次调用后标签改变，因此第二次读取当前状态并返回 `True`。写成 `if sample.is_labeled:` 而漏掉括号，不会执行检查。本例方法对象本身为真，因此标签为 `None` 时也会通过该条件。

## 函数调用与方法调用

清理 `" AI "` 的函数可以在内部调用字符串方法。代码输出 `function: ai`、`method: AI`。

```python
def clean_text(text):
    return text.strip().lower()

text = " AI "

print("function:", clean_text(text))
print("method:", text.strip())
```

`clean_text(text)` 同时去空白并转小写，`text.strip()` 只去空白，因此保留大写字母。

| 表达式 | 目标与操作 |
| --- | --- |
| `clean_text(text)` | 将字符串传给函数 |
| `text.strip()` | 调用字符串对象的空白清理方法 |
| `sample.is_labeled()` | 调用样本对象的标签检查方法 |
| `model.predict(test_data)` | 将数据传给模型对象的预测方法 |

## 案例：训练前后的模型状态

模型对象保存设置和从训练中得到的值，方法改变或使用这些状态。`SimplePassModel` 是教学用类，把通过分数中的最小值保存为阈值，并非实际机器学习库训练算法的实现。

`[(62, False), (75, True), (83, True)]` 中每对表示分数与通过状态。`fit()` 保存通过分数 `75`、`83` 的最小值 `75`，`predict()` 将 `[70, 78]` 与此阈值比较。

```python
class SimplePassModel:
    def __init__(self):
        self.threshold = None

    def fit(self, train_data):
        # fit() 读取训练数据并在对象中保存状态。
        passed_scores = [score for score, passed in train_data if passed]
        if not passed_scores:
            raise ValueError("at least one passing score is required")
        self.threshold = min(passed_scores)

    def predict(self, test_data):
        # predict() 使用 fit() 保存的状态。
        if self.threshold is None:
            raise ValueError("请先调用 fit()。")
        return [score >= self.threshold for score in test_data]


train_data = [(62, False), (75, True), (83, True)]
test_data = [70, 78]

model = SimplePassModel()

print("before fit:", model.threshold)
model.fit(train_data)
print("after fit:", model.threshold)
predictions = model.predict(test_data)
print("predictions:", predictions)
```

输出如下：

```text
before fit: None
after fit: 75
predictions: [False, True]
```

训练前 `model.threshold` 为 `None`，`fit()` 后变为 `75`。`predict()` 读取已保存阈值，因此应继续使用同一对象。新建对象后直接调用 `predict()`，会因没有阈值而引发代码定义的 `ValueError`。

把训练项 `(75, True)` 改成 `(68, True)` 后，阈值变为 `68`，预测变为 `[True, True]`。测试分数未变，但模型状态变化使判断改变。

本例要求至少有一个通过分数，否则 `fit()` 明确引发 `ValueError`。异常发生后应检查输入，不应继续预测。此外，未通过分数不参与阈值计算，因此不能直接把此规则用于复杂的实际分类问题。

## 检查清单

- 能将对象解释为 Python 值的实际载体。
- 能将类解释为创建对象的定义。
- 能将方法解释为通过对象调用的函数式操作。
- 能初步区分字典与基于类的对象。
- 能通过示例解释状态与行为的组合。
- 能区分 `function(value)` 与 `value.method()` 的调用目标。
- 能解释 `self` 指代实例自身。
- 能说明何时函数和字典已足够，无需使用类。
- 能从对象与方法角度读懂 `model.fit()`、`model.predict()`。

- 能区分获取方法与调用方法，并解释条件中省略括号为何不执行实际检查。

## 来源与参考资料


- Python Software Foundation, [Classes](https://docs.python.org/3/tutorial/classes.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。作为 class objects、instance objects、attribute references 和 method objects 入门说明的官方依据。
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。作为说明对象具有 identity、type、value，以及不同行为会随类型而变化的背景依据。
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。用于确认把 `value.method()` 调用读成附着在对象上的函数形式这一说明。
