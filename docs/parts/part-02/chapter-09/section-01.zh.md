# P2-9.1 为什么需要选择数据结构？

> Section ID: `P2-9.1`
> Version: `v2026.09.15`

## 数据组织与操作

数据结构是组织数据的方式。NIST 从提高算法效率的角度定义信息组织。同一份学生信息，用于计算分数、查找学生或沿朋友关系查询时，表示方式可能不同。

| 视角 | 核心问题 | 示例 |
| --- | --- | --- |
| 顺序 | 第几个值？ | 列表 |
| 名称查找 | 用哪个键查找？ | 字典 |
| 成员关系 | 是否存在？ | 集合 |
| 层级 | 有哪些上级与下级？ | 树 |
| 关联 | 什么与什么相连？ | 图 |

选择数据结构时，经常执行的操作很重要，包括查找、添加、删除以及访问全部元素的遍历。

## 顺序、层级与基于键的结构

| 传统结构 | 入门问题 | 直观理解 |
| --- | --- | --- |
| 数组 | 按连续位置处理同类值？ | 带编号的格子 |
| 链表 | 让每项指向下一项？ | 相互连接的元素 |
| 栈 | 最后放入的先取出？ | 叠放盘子 |
| 队列 | 最先放入的先取出？ | 排队 |
| 树 | 表达父子关系？ | 文件夹结构 |
| 图 | 表达多个对象之间的连接？ | 关系网络 |
| 哈希表 | 通过键快速查找？ | 带标签的储物格 |

这些结构还可以大体分为线性与非线性结构。

线性结构将数据按一条顺序组织，数组、列表、栈和队列都符合这种视角。

非线性结构不把所有数据排列成一条顺序。树表达层级，图表达多个方向的关联。

| 类别 | 特征 | 示例 |
| --- | --- | --- |
| 线性 | 前后顺序重要 | 数组、链表、栈、队列 |
| 非线性 | 层级或关系重要 | 树、图 |
| 基于键 | 按键查值重要 | 字典、哈希表 |

分类标准可能重叠。Python 字典按键映射值，同时保留插入顺序。图也可以由字典和列表组合表示。

## 抽象数据类型与实现

抽象数据类型（ADT）描述支持哪些值与操作。

实现说明如何在实际内存与代码中构建这个概念。

例如，栈先取出最后放入的元素，这是一条行为规则。

- `push`：放入值。
- `pop`：取出最近放入的值。
- 最后放入的值最先取出。

栈内部可以使用 Python 列表，也可以使用链表。同一种抽象数据类型可有多种实现。

阅读 Python 时，这一区分也很重要。

| 视角 | 问题 | 示例 |
| --- | --- | --- |
| 抽象数据类型 | 约定什么行为？ | 栈先取出最后放入的值 |
| 实现 | 实际如何存储？ | 可以用列表或链接结构实现 |
| Python 接口 | 由哪些对象和方法提供？ | `list.append()`、`list.pop()` |

先放入 `A`，再放入 `B`，取一次就应得到 `B`。Python 列表可用 `append("A")`、`append("B")` 和 `pop()` 实现。存储方式即使改变，也必须保持该取出规则才仍是栈行为。

## 遍历、查询与关系表示

Kim、Lee、Park 分别得 82、75、91 分。查询分数与表示朋友关系所需的信息，可以放在不同结构中。

### 遍历全部记录

将学生字典放入列表即可遍历全部记录，代码依次输出 `Kim 82`、`Lee 75`、`Park 91`。

```python
students = [
    {"name": "Kim", "score": 82},
    {"name": "Lee", "score": 75},
    {"name": "Park", "score": 91},
]

for student in students:
    print(student["name"], student["score"])
```

三个分数总和为 248，平均约为 82.67。平均值需要全部分数，与查询某个姓名不同。

### 按姓名查询

以姓名为键可以直接访问学生分数，`student_by_name["Kim"]["score"]` 输出 `82`。

```python
student_by_name = {
    "Kim": {"score": 82},
    "Lee": {"score": 75},
    "Park": {"score": 91},
}

print(student_by_name["Kim"]["score"])
```

这种结构适合按姓名查找某名学生。

### 朋友关系

可以为每个姓名保存朋友列表来表示关系。本例 Kim 的朋友列表是 `['Lee', 'Park']`。

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim"],
    "Park": ["Kim"],
}

print(friends["Kim"])
```

这是以学生为对象、以朋友关系为连接的图。相互朋友关系记录在双方列表中。删除 Kim–Lee 关系时，要同时删除 Kim 列表中的 `"Lee"` 和 Lee 列表中的 `"Kim"`。

同一批人的数据，目的不同，结构也会不同。这正是需要数据结构的原因。

## AI 数据的结构

句子输入、标签映射与文档链接需要不同的查询和处理。

| AI 情况 | 常见结构 | 阅读视角 |
| --- | --- | --- |
| 多个句子输入 | 列表 | 逐句处理 |
| 标签编号与名称 | 字典 | 按键查名称 |
| 检查重复词元 | 集合 | 检查是否存在 |
| 表格数据 | 表、DataFrame | 按行和列访问 |
| 句中词元顺序 | 序列 | 按顺序处理 |
| 文档之间的链接 | 图 | 沿关系移动 |

## 案例：同名学生的分数

假设两名同叫 Kim 的学生分别得 `82` 和 `91`。列表保存两条记录，但把姓名作为字典键时，后一个分数覆盖前一个。代码先输出两条记录，再输出 `{'Kim': 91}`。

```python
students = [
    {"id": "s001", "name": "Kim", "score": 82},
    {"id": "s002", "name": "Kim", "score": 91},
]
score_by_name = {}

for student in students:
    score_by_name[student["name"]] = student["score"]

print(students)
print(score_by_name)
```

键的选择关系到保留哪些信息。使用唯一学生 ID 可以区分两个分数。对同一输入运行下面代码，输出 `{'s001': 82, 's002': 91}`。

```python
students = [
    {"id": "s001", "name": "Kim", "score": 82},
    {"id": "s002", "name": "Kim", "score": 91},
]
score_by_id = {}

for student in students:
    score_by_id[student["id"]] = student["score"]

print(score_by_id)
```

把第二个 ID 改为 `"s001"`，又只剩一个键。除了查询方便，还需确认键确实能区分学生。若目的是按姓名收集多个分数，可以用分数列表作为字典值。

## 改变结构时丢失的信息

集合适合去重，但不保留出现次数。Kim 出现两次、Lee 出现一次的姓名列表长度为 3，唯一姓名数为 2。

```python
names = ["Kim", "Kim", "Lee"]
unique_names = set(names)
print(len(names))
print(len(unique_names))
print("Kim" in unique_names)
```

输出为 `3`、`2`、`True`。只保留集合，就无法恢复 Kim 出现几次以及原顺序。次数可用按姓名计数的字典保留，原记录可用列表保留。不要假定集合输出顺序就是输入顺序。

查询字典也需要先读取原数据构建，并占用额外内存。反复按同一 ID 查询时，这种准备有帮助；只求一次整体平均值时，遍历分数就足够。原分数改变而查询字典中的副本未更新时，两者可能不一致，因此还要确定更新依据。

## 检查清单

- 能把数据结构解释为组织数据的方式。
- 能说明数组、链表、栈、队列、树、图和哈希表分别代表什么问题。
- 能初步区分线性与非线性结构。
- 能将结构与查找、添加、删除、遍历联系起来。
- 能解释同一数据如何按顺序、键和关系形成不同表示。
- 能初步区分抽象数据类型与实现。
- 能解释 AI 工作中列表、字典、集合、表和图回答的不同问题。
- 能根据数据要回答的问题选择结构，而不只是把数据收集起来。
- 能解释转为集合时丢失的顺序、重复信息，以及查询副本的更新问题。

## 来源与参考资料

- Paul E. Black, [data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST，确认日期：2026-07-20。用于确认把 data structure 说明为组织数据方式的定义。
- Paul E. Black, [abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST，确认日期：2026-07-20。作为把 abstract data type 区分为偏向行为而非实现的框架依据。
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于把 Python list 与 dictionary 示例连接到数据结构选择说明。
