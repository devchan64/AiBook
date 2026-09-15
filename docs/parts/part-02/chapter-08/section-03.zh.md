# P2-8.3 字典（dictionary）：通过键查找值

> Section ID: `P2-8.3`
> Version: `v2026.09.15`

## 键与值

映射（mapping）将某个查找依据与值连接起来。这个依据称为键（key），键所关联的对象称为值（value）。

Python 通常使用字典表示这种映射结构。

把姓名 `"Kim"`、分数 `82.5` 和通过状态 `True` 分别关联到 `"name"`、`"score"`、`"passed"` 键。查找姓名和分数会输出 `Kim`、`82.5`。

```python
student = {
    "name": "Kim",
    "score": 82.5,
    "passed": True,
}

print(student["name"])
print(student["score"])
```

列表通过位置取值，Python 字典通过键取值。

| 结构 | 查找依据 | 示例 |
| --- | --- | --- |
| 列表 | 索引 | `scores[0]` |
| 字典 | 键 | `student["score"]` |

AI 练习中经常使用字典。

- 配置项：`{"learning_rate": 0.01, "epochs": 10}`
- 一行数据：`{"text": "hello", "label": "positive"}`
- API 响应的一部分：`{"model": "example", "tokens": 120}`
- 模型评估结果：`{"accuracy": 0.91, "loss": 0.32}`

当值的名称比它是第几项更重要时，适合使用字典。

| 概念 | 一般含义 | 在 Python 中 |
| --- | --- | --- |
| 映射 | 将查找依据与值关联 | 使用字典表示 |
| 键 | 查找值的依据 | 字符串、数字等可哈希值 |
| 值 | 键关联的对象 | 可以是数字、字符串、列表、字典等 |

## 标签映射与键检查

标签编号 `0` 对应 `"negative"`，`1` 对应 `"positive"`。以预测值 `1` 为键查找，会输出 `positive`。

```python
label_name = {
    0: "negative",
    1: "positive",
}

prediction = 1
print(label_name[prediction])
```

当 `prediction` 为 `1` 时，字典返回键 `1` 关联的 `"positive"`。数字键 `1` 是查找标识，不表示第二个位置。

除了标签，配置名称、ID 和列名也能作为键。

| 情况 | 字典表示 |
| --- | --- |
| 将标签编号转为可读名称 | `{0: "negative", 1: "positive"}` |
| 按名称查找配置 | `{"batch_size": 32, "learning_rate": 0.001}` |
| 按用户 ID 查找信息 | `{"u001": {"name": "Kim"}}` |
| 按列名说明数据含义 | `{"score": "考试分数", "label": "真实标签"}` |

`键 in 字典` 检查指定键是否存在。

用 `in` 检查 `"learning_rate"` 键，存在时输出其值。本例输出 `0.001`；把 `name` 改为不存在的 `"dropout"`，则不会输出任何内容。

```python
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

name = "learning_rate"

if name in config:
    print(config[name])
```

## 可哈希的键

Python 文档把字典称为映射类型。映射关联键和值，哈希用于实现查找。字典的键必须可哈希。

字符串和数字可以作为键。元组只有在所有元素都可哈希时才能作为键。列表不可哈希，因此不能作为键。

以 `"Kim"` 为键查找，会输出关联分数 `82`。

```python
scores_by_name = {
    "Kim": 82,
    "Lee": 91,
}

print(scores_by_name["Kim"])
```

字典保留键的插入顺序，不会自动按大小或字母顺序排序。本例先插入 `"Lee"`，因此键列表是 `['Lee', 'Kim']`。

```python
scores_by_name = {"Lee": 91, "Kim": 82}
print(list(scores_by_name))
```

`list(字典)` 将键组成列表，与使用 `scores_by_name["Kim"]` 查询值不同。

## 替换同一键的值

在已有键下保存新值，会替换旧值。

在空字典的 `"Kim"` 键下先保存 `82`，再保存 `91`，输出为 `{'Kim': 91}`，原分数被覆盖。

```python
scores = {}

scores["Kim"] = 82
scores["Kim"] = 91

print(scores)
```

这段代码不会在 `"Kim"` 下保留两个分数，只留下最后的 `91`。要在同一键下收集多个值，可把列表等集合用作值。

可以用列表保存一个人的两个分数，此时查询 `"Kim"` 得到 `[82, 91]`。

```python
scores = {
    "Kim": [82, 91],
}

print(scores["Kim"])
```

## 查询配置、标签与 ID

当查找依据明确时，字典很合适。

### 配置项

查找表示学习率的 `"learning_rate"` 键，会输出 `0.001`。

```python
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

print(config["learning_rate"])
```

`config[1]` 并非查找第二项配置，而是查找整数键 `1`。本例没有该键，因此引发 `KeyError`。

### 将标签编号转换为名称

把数字标签 `2` 映射到情感名称，会输出 `neutral`。

```python
label_map = {
    0: "negative",
    1: "positive",
    2: "neutral",
}

predicted_label = 2

print(label_map[predicted_label])
```

模型输出数字标签时，可以用字典转成人能读懂的名称。

### 按样本 ID 查找数据

`"s001"` 对应的值是包含样本信息的字典，再查找其中的 `"text"`，会输出 `good product`。

```python
samples_by_id = {
    "s001": {"text": "good product", "label": "positive"},
    "s002": {"text": "bad service", "label": "negative"},
}

sample_id = "s001"

print(samples_by_id[sample_id]["text"])
```

数据增多时，样本的 ID 可能比它是第几项更重要。这时字典相当于从 ID 到样本的映射。

### 通过列名说明含义

把列名与描述关联后，查找 `"score"` 就能得到 `模型分数` 这一说明。

```python
column_description = {
    "text": "输入句子",
    "label": "真实标签",
    "score": "模型分数",
}

print(column_description["score"])
```

读取数据集时记录列名含义，有助于后续预处理和文档编写。

## 字典与对象

字典是 Python 对象的一种。数字、字符串、列表和函数也都是对象；字典专门负责关联键与值。它的花括号形式类似 JSON 对象，但不能把所有 Python 对象都称为字典。

键访问与属性访问不同。应通过 `student["name"]` 读取姓名；对同一个字典使用 `student.name` 不会返回姓名，而会引发 `AttributeError`。

## 缺失键与默认值

直接读取不存在的字典键可能引发错误。

`student` 只有 `"name"` 和 `"score"`。用方括号查询不存在的 `"label"` 会引发 `KeyError`。

```python
student = {"name": "Kim", "score": 82.5}

print(student["label"])
```

`KeyError` 表示请求的键不存在。

键可能缺失时，可以使用 `get()`。

键不存在时，`get()` 返回指定默认值。代码在省略默认值时输出 `None`，指定默认值时输出 `unknown`。

```python
student = {"name": "Kim", "score": 82.5}

print(student.get("label"))
print(student.get("label", "unknown"))
```

使用默认值不会把该键添加到字典。必填项缺失时，应检查错误并修正输入；可选项则可以用 `get()` 指定默认值。

## 缺失键与空值项

键不存在与键存在但值为 `None` 是两种情况。`get()` 仅在键不存在时使用默认值。

```python
sample = {"text": "hello", "label": None}
print(sample.get("label", "unknown"))
print(sample.get("source", "unknown"))
print("label" in sample)
print("hello" in sample)
```

输出依次为 `None`、`unknown`、`True`、`False`。`"label"` 键存在，因此不会使用默认值。`in` 检查键而非值，所以即使值中有 `"hello"`，最后结果仍是 `False`。

即使改为 `sample["label"] = ""`，`get("label", "unknown")` 也会原样返回空字符串。检查必填标签时，需要分别确认键存在，以及值属于允许的标签。

## 案例：不连续的标签编号

假设情感标签编号为 `10`、`20`、`90`。把它们作为列表位置需要许多空位，而字典只需关联实际编号与名称。代码为预测编号 `90` 输出 `neutral`，为不存在的 `30` 输出默认值 `unknown`。

```python
label_map = {10: "negative", 20: "positive", 90: "neutral"}
prediction = 90

print(label_map[prediction])
print(label_map.get(30, "unknown"))
```

把 `prediction` 改为 `20`，首次输出变成 `positive`。改为 `30` 时，第一次查询便引发 `KeyError`，不会执行后面的输出。编号与名称的对应关系，以及缺失编号的处理方式，需要分别确定。

## 检查清单

- 能将字典解释为键和值的集合。
- 能将字典解释为映射结构。
- 能从使用角度解释映射，从实现角度解释基于哈希的结构。
- 能说明列表按位置、字典按键查找的区别。
- 能解释键可能缺失时 `get()` 的用途。
- 能读懂标签映射、配置、样本 ID 和列说明示例。
- 能根据键是否可能缺失选择查询方式。

- 能区分缺失键与值为 `None`，并解释 `get()` 默认值的使用条件。

## 来源与参考资料


- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认字典创建、通过 key 访问 value，以及使用 `items()` 遍历的示例。
- Python Software Foundation, [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。用于确认 `dict` 是 mutable mapping type，并且是通过 key 查找 value 的结构。
- Python Software Foundation, [Glossary: dictionary, hashable](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认 dictionary 与 hashable 的术语定义。
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认对象的 identity/type/value 和 hashability，作为字典 key 限制的背景依据。
