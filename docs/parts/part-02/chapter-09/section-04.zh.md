# P2-9.4 补充学习：初读传统数据结构

> Section ID: `P2-9.4`
> Version: `v2026.09.15`

数组按位置查值，链表沿指向下一项的连接移动。栈和队列规定放入与取出顺序，树与图表示对象关系。数据结构名称区分存储方式或操作规则。

| 结构 | 主要特性 | 用途示例 |
| --- | --- | --- |
| 数组 | 按索引访问 | 向量、图像像素 |
| 链表 | 通过节点连接表达顺序 | 修改元素间的连接 |
| 栈 | 最后输入先取出 | 撤销、函数调用 |
| 队列 | 最先输入先取出 | 任务队列 |
| 树 | 父子层级 | 目录、分类体系 |
| 图 | 节点间连接 | 朋友关系、文档链接 |
| 哈希表 | 利用哈希按键查询 | ID 查询、单词计数 |

栈与队列的取出规则描述抽象数据类型的行为，实际存储和执行的实现可以不同。在 Python 列表末尾放入并从末尾取出，就可实现栈。

## 数组与位置访问

数组按索引读取值，`[10, 20, 30, 40]` 的索引 2 对应 `30`。图像和向量中，位置变化可能改变计算对象的含义。

Python 列表也使用索引。代码输出第一项 `10`、第三项 `30`，再输出将第二项改为 `25` 后的 `[10, 25, 30, 40]`。

```python
values = [10, 20, 30, 40]

print(values[0])
print(values[2])

values[1] = 25
print(values)
```

Python 列表保存对象引用，长度可变。NumPy 数组通过一个 dtype 解释元素，用于数值计算。两者都支持位置访问，但并非同一类型。

## 链表与下一节点

单向链表的每个节点保存值以及指向下一节点的引用，最后一个连接表示结束。

```text
Kim → Lee → Park → None
```

代码用三个字典作为节点，`next` 保存下一节点的引用。从第一个节点出发，依次输出 `Kim`、`Lee`、`Park`。

```python
third = {"value": "Park", "next": None}
second = {"value": "Lee", "next": third}
first = {"value": "Kim", "next": second}

node = first
while node is not None:
    print(node["value"])
    node = node["next"]
```

`while node is not None` 在当前节点存在时重复执行，`node = node["next"]` 移到下一节点，遇到 `None` 时停止。

在创建节点后加入 `first["next"] = third`，输出变为 `Kim`、`Park`。Lee 节点仍存在，但不再能从首节点沿连接到达。逻辑顺序由节点链接决定。

在链表中查值需要从起点沿链接移动。已知某节点或前驱时可修改连接，但找到该位置的过程未必快。若把最后节点的 `next` 连回首节点，就形成环，原 `while` 循环无法遇到 `None`，因此不会结束。

## 栈：后进先出

栈遵循 LIFO（后进先出），就像从叠放的盘子顶部取盘子。

依次加入 A、B、C，再取两次，得到 C、B，留下 A。`append()` 在末尾添加，无参数的 `pop()` 从末尾取出。

```python
stack = []

stack.append("A")
stack.append("B")
stack.append("C")

print(stack.pop())
print(stack.pop())
print(stack)
```

输出为 `C`、`B`、`['A']`。依次完成编辑 A、B、C 后，可以按 C、B 顺序撤销。嵌套函数调用也先结束较晚进入的调用，这种结构称为调用栈。

## 队列：先进先出

队列遵循 FIFO（先进先出）。`collections.deque` 支持两端添加和取出；在后端加入、前端取出，就可实现队列。

代码依次加入 A、B、C，再从前端取两次，输出 `A`、`B`、`deque(['C'])`。

```python
from collections import deque

queue = deque()

queue.append("A")
queue.append("B")
queue.append("C")

print(queue.popleft())
print(queue.popleft())
print(queue)
```

`append()` 在后端添加，`popleft()` 从前端取出。A、B、C 依次到达时，从 A 开始取出处理。并发执行任务的服务中，取出顺序与完成顺序可能不同。

## 从空结构取出元素

对空列表调用 `pop()`，或对空双端队列调用 `popleft()`，都会引发 `IndexError`。下面代码逐个取请求，没有剩余项便结束循环。

```python
from collections import deque

queue = deque(["A", "B"])
while queue:
    request = queue.popleft()
    print(request)
print("remaining:", len(queue))
```

输出为 `A`、`B`、`remaining: 0`。若一开始就是 `deque()`，循环体不会执行，只输出最后一行。列表 `pop(0)` 也能取首项，但需要将后续位置前移，因此频繁从前端取项适合用 deque。本例处理单一执行流程，并未实现并发访问队列的同步。

## 树：父节点与子节点

有根树中，根以外每个节点有一个父节点。目录可在书籍下放 Part，在 Part 下放 Chapter。

代码输出书名、两个 Part 及各自的 Chapter。外层循环读取 Part，内层循环读取对应 Chapter。

```python
book = {
    "title": "study-book",
    "children": [
        {
            "title": "Part 1",
            "children": ["Chapter 1", "Chapter 2"],
        },
        {
            "title": "Part 2",
            "children": ["Chapter 8", "Chapter 9"],
        },
    ],
}

print(book["title"])
for part in book["children"]:
    print("-", part["title"])
    for chapter in part["children"]:
        print("  -", chapter)
```

```text
study-book
- Part 1
  - Chapter 1
  - Chapter 2
- Part 2
  - Chapter 8
  - Chapter 9
```

`Chapter 9` 的路径是 `study-book → Part 2 → Chapter 9`，沿父子连接可确认归属。

## 图：对象间的连接

图通过节点和边表示关系。树是连通且无环的一类图，一般图则可具有环或多条路径。

本例 Kim 的直接邻居为 Lee、Park。代码先输出 `['Lee', 'Park']`，再输出 `Kim is connected to Lee`、`Kim is connected to Park`。

```python
graph = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim", "Choi"],
    "Park": ["Kim"],
    "Choi": ["Lee"],
}

print(graph["Kim"])

for friend in graph["Kim"]:
    print("Kim is connected to", friend)
```

Choi 不是 Kim 的直接邻居，但可经 `Kim → Lee → Choi` 连接。这里沿朋友关系移动，而非按归属层级分组。

## 哈希表与按键查询

哈希表利用键的哈希值确定存储位置并查值。不同键可能对应同一位置，形成冲突，因此需要冲突处理规则。

Python 字典关联键和值，并使用基于哈希的查询。代码先输出 Kim 的分数 `82`，再添加 `"Choi": 88`。

```python
score_by_name = {
    "Kim": 82,
    "Lee": 75,
    "Park": 91,
}

print(score_by_name["Kim"])

score_by_name["Choi"] = 88
print(score_by_name)
```

第二次输出为 `{'Kim': 82, 'Lee': 75, 'Park': 91, 'Choi': 88}`。`score_by_name["Kim"]` 这样的字典用法，与内部哈希表定位过程，是不同层次的解释。

哈希冲突指不同键对应相同哈希值或候选存储位置，并不自动覆盖原值；实现会区分实际键来保存值。同一键赋新值的替换，与不同键之间的哈希冲突处理，是不同操作。

## 案例：等待队列与撤销

按到达顺序执行请求 A、B、C 时，队列先取 A；撤销已经完成的 A、B、C 时，栈先取 C。同样的项因目的不同，需要不同取出规则。

| 输入顺序 | 从栈取两次 | 从队列取两次 |
| --- | --- | --- |
| A, B, C | C, B | A, B |
| A, B, C, D | D, C | A, B |

在前例 `append("C")` 后加入 `append("D")`，可验证第二行。栈剩 `['A', 'B']`，队列剩 `deque(['C', 'D'])`。输入顺序相同，并不意味着处理顺序相同。

## AI 任务与数据结构

| 任务 | 所需特性 | 结构示例 |
| --- | --- | --- |
| 保留词元顺序 | 位置与顺序 | 数组、序列 |
| 按标签编号查名称 | 键值对应 | 字典 |
| 单词去重 | 成员关系 | 集合 |
| 探索文档链接 | 连接与路径 | 图 |
| 按到达顺序取请求 | FIFO | 队列 |
| 查找文档上级标题 | 父子层级 | 树 |

## 检查清单

- 能解释数组按索引处理值。
- 能解释链表中的项指向下一项。
- 能解释栈的 LIFO 与队列的 FIFO。
- 能区分树的层级与一般图的关系。
- 能将字典、哈希表与按键查询联系起来。
- 能理解便利的 Python 语法背后的传统结构。
- 能执行数组、链表、栈、队列、树、图和字典示例并说明输出。
- 能解释空队列的终止条件、链表中的环和哈希冲突。

## 来源与参考资料

- NIST, [Data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures，确认日期：2026-07-20。用于确认把传统数据结构名称读成组织数据方式的基本定义。
- NIST, [Abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures，确认日期：2026-07-20。作为按提供的行为而非实现来说明 stack、queue 等结构的依据。
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认 Python list 与 dictionary 语法怎样连接到传统数据结构直觉。
- Python Software Foundation, [deque objects](https://docs.python.org/3/library/collections.html#collections.deque){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。确认空 deque 的取出错误及两端插入、删除特性。
- Paul E. Black, NIST, [collision](https://xlinux.nist.gov/dads/HTML/collision.html){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。用于区分不同键的哈希冲突和同一键的值更新。
