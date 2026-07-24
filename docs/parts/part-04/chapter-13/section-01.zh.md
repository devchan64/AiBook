# P4-13.1 SVM 的直觉

> Section ID: `P4-13.1`
> Version: `v2026.07.20`

P4-11.2 把 classification 读成了 `画出 boundary 并切开空间`。P4-12 又看过了 `通过附近 neighbors 做判断` 的方式。现在，同一个分类问题要再换一个问题来读。

如果能画出 boundary，那么其中哪一条 boundary 才是更好的 boundary？

这正是 SVM(support vector machine) 的出发点。

`SVM 是这样一种模型：它不仅要找到一条能把 class 分开的线，还要尽量让这条线和两边数据之间都留出更大的余地。`

所以，SVM 不会停在 `找出一条分割线` 上，而是会继续去找 `看起来更稳定的分割线`。

这一节会说明 `SVM`、`margin`、`support vector` 的基本含义。后面的章节会沿着这个抓手继续当前判断，而把 boundary 的稳定性读出来的基础感觉，也会通过这一节和 [概念词汇表](/AiBook/reference/concept-glossary/) 再接回来。

## 本节范围

这一节是第一次用 SVM 抓住 `什么是好的 boundary` 这个问题的地方。这里会围绕 margin、support vector、soft margin 的直觉，先读出不只是 `能不能分开`，还包括 `什么样的标准能分得更稳定`。

这一节回答下面这些问题。

- 为什么 SVM 比起单纯的分割线，更看重 `margin`？
- margin 是什么，为什么它会和分类稳定性连在一起？
- support vector 是什么，为什么它会重要到写进模型名字里？
- 当数据不能被完美分开时，会多出什么想法？
- SVM 和前面的 logistic regression、k-NN 有什么不同？

kernel 的大图景和 nonlinear boundary 会在 P4-13.2 立刻继续；`C`、`gamma` 这类 hyperparameter 的读取标准和验证成本，会在 P4-9.1 和 P4-9.2 再接回来。也就是说，这一节是先用 margin 和 support vector 视角抓住 `什么是好的 boundary` 的位置。

## 用SVM 的直觉留下的判断标准

- 能用 `最大化 margin 的分类器` 这个直觉来说明 SVM
- 能说明：即使多条 boundary 都能分开同一批数据，仍然可以说其中一些 boundary 更好
- 能说明 support vector 是 `离 boundary 最近的核心点`
- 能在入门层面理解：当完美分离困难时，margin 和允许错误会一起出现
- 能说明为什么第 11 章的 decision boundary 和第 12 章的 distance / scale 讨论，会自然地接到 SVM

## 学习背景

P4-11 的 logistic regression 已经展示了 `切开 input space 的 boundary`。但光看到那里，仍然会留下下面这些问题。

- 只要能分开就够了吗？
- 如果 boundary 紧贴某一边 class，也算可以吗？
- 如果 boundary 附近只要有一点点扰动，prediction 就很容易翻转，该怎么办？

SVM 正是对这些问题的第一种代表性回答。

这一节与其说是在学 `分割线本身`，不如说更接近在学 `什么才算好的分割线`。

## 主要学习内容

### 为什么要单独把 margin 拿出来看

能把两个 class 分开的直线，不一定只有一条。在同一批数据上，经常可以画出多条不同的线。

问题在于，这些线看起来并不一样好。

- 有些线太贴近某一侧的数据
- 有些线能在两边都留出更多空间
- 有些线看起来只要一点点 noise，就会让很多 case 翻面

SVM 正是用 `margin` 这个词来抓住这种差别。

`margin 是 boundary 和最近数据点之间留下的安全余量宽度。`

如果这段余量更大，就可以把 boundary 读成在两类数据之间放得更稳定。

也就是说，SVM 不只是问 `能不能画出一条线把 class 分开`，而是会继续问：`在这些候选 boundary 里，哪一条更稳定？` 重点不只是能否分离，而是要通过比较最近点和 boundary 的最小距离，优先选择留出更大余量的那条。

把这个想法压成一个判断流程，可以画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-01-zh.mmd"
```

这张图的关键在于：单独读取 margin 并不是附带装饰。必须先看到同一批数据上可以有多个候选 boundary，再去比较各自最近的点，读者才能真正区分：为什么有的 boundary 紧贴一侧而显得脆弱，而有的 boundary 能在两边都留下余地。

### 为什么更大的 margin 会被认为更好

更大的 margin 并不等于在所有场景里都是绝对答案。但在教学上，它至少因为下面几个原因而非常重要。

1. boundary 不会过度贴近任一侧 class
2. 它看起来对边界附近的小扰动没那么敏感
3. 它给出一种直觉：在未见过的新数据上，可能更容易保持稳定的 generalization

正因为第三点，SVM 常会和 statistical learning theory 一起出现。前面已经看过，generalization 更接近 `在新数据上也能保持合理判断`，而不是 `把 training data 记得很好`。SVM 则让读者能用 margin 这种几何语言去重新读这个问题。

`SVM 把分类问题重新读成：寻找一条留有余量的 boundary。`

如果把这件事改写成 project note 语言，可以写成这样。

| 记录项 | 例子 |
| --- | --- |
| 当前候选 boundary | `linear SVM` |
| 靠近 margin 的案例 | `transaction A`, `transaction B` |
| 是否需要 review | `因为太靠近 boundary，需要 review` |
| 下一个问题 | `如果允许 soft margin，这些案例还会不会继续最关键？` |

这样的表会让读者先通过 `boundary 候选 -> review 案例 -> 下一个问题` 来读这一节，而不是直接陷在公式里。

### 什么是 support vector

SVM 这个名字里就带着 `support vector`。之所以重要，是因为并不是所有点对 boundary 的影响都一样。

在 SVM 的直觉里，通常最重要的是 `离 boundary 最近的那些点`。这些点像是在实际撑住 boundary 一样，因此才会叫 support vector。

- 离 boundary 很远的点，摇动 boundary 的能力更小
- 离 boundary 最近的点，对 boundary 位置的影响更强
- 所以 SVM 会特别看重整批数据里最紧的那些点

这个想法可以简单画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-02-zh.mmd"
```

这张图说明了为什么 support vector 特别。并不是所有 training points 都以同样的权重塑造 boundary。远离 boundary 的点摇动它较少，而少量最近的点真正撑住了分割线的位置。

从实际工作角度，也可以这样再读一遍。

- 不是每一条客户记录都同样重要
- 不是每一份答卷都同样会摇动 cutoff
- 实际上，最模糊、最靠近 boundary 的案例，往往最能改变标准

### Python 例子：直接看哪一条 boundary 的 margin 更大

这个例子并不是直接实现一个 SVM learner，而是放几个垂直 boundary 候选在两类数据之间，直接计算哪一条留出了更大的 margin。

- 问题场景：两类点分别位于 x 轴左侧和右侧
- 输入(input)：二维点
- label：negative / positive
- 要检查的概念：
  - 能把 class 分开的候选 boundary 可能有不止一条
  - SVM 真正关心的是 `最小余量` 最大的那条
  - 最靠近 boundary 的点会像 support vector 一样起作用

```python
# 这个例子比较 SVM 多个边界候选的 margin，以及像 support vector 一样起作用的近邻点。
negative = [(1.0, 2.0), (2.0, 3.0), (3.0, 2.5)]
positive = [(5.0, 2.2), (6.0, 3.2), (7.0, 2.8)]

candidates = [3.4, 4.0, 4.6]

for boundary_x in candidates:
    neg_min = min(boundary_x - x for x, _ in negative)
    pos_min = min(x - boundary_x for x, _ in positive)
    margin = min(neg_min, pos_min)

    support_neg = [p for p in negative if abs((boundary_x - p[0]) - neg_min) < 1e-9]
    support_pos = [p for p in positive if abs((p[0] - boundary_x) - pos_min) < 1e-9]

    print("boundary x =", boundary_x)
    print("  negative-side nearest distance =", round(neg_min, 3))
    print("  positive-side nearest distance =", round(pos_min, 3))
    print("  margin =", round(margin, 3))
    print("  support-like points =", support_neg + support_pos)
    print()
```

示例输出如下。

```text
boundary x = 3.4
  negative-side nearest distance = 0.4
  positive-side nearest distance = 1.6
  margin = 0.4
  support-like points = [(3.0, 2.5), (5.0, 2.2)]

boundary x = 4.0
  negative-side nearest distance = 1.0
  positive-side nearest distance = 1.0
  margin = 1.0
  support-like points = [(3.0, 2.5), (5.0, 2.2)]

boundary x = 4.6
  negative-side nearest distance = 1.6
  positive-side nearest distance = 0.4
  margin = 0.4
  support-like points = [(3.0, 2.5), (5.0, 2.2)]
```

这个输出里最重要的点很清楚。

- 三条 boundary 都能把两类分开
- 但 `x = 4.0` 时，最小余量最大
- 离 boundary 最近的 `(3.0, 2.5)` 和 `(5.0, 2.2)` 像 support vector 一样起作用

所以 SVM 不会停在 `能不能分开`，而会继续追问 `它分开时到底留了多少余量`

## 细部学习内容

### 如果数据不能被完美分开，会怎样

现实数据不会总像上面的 toy example 那样干净。有些点会混到另一边 class 附近，这时就很难再找到完美分割线。

于是，SVM 的直觉会变成下面这样。

- 不再只坚持把每个点都完美分开
- 如果需要，可以允许一些错误或侵入
- 但整体上仍然要尽量保留有意义的 margin

这个想法会继续连到后面的 `soft margin` 和 hyperparameter `C`。在当前这一节，只要先抓住下面这句话就够了。

`现实里的 SVM，不只是完美分离，还要一起处理余量与允许错误之间的平衡。`

这个想法可以概念化地画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-03-zh.mmd"
```

### SVM 适合处理什么问题

scikit-learn 官方文档把 SVM 介绍成一组用于 classification、regression、outlier detection 的 supervised learning 方法。但这一节先只专注在 binary classification。

例如：

| 业务场景 | 要预测的值 |
| --- | --- |
| 正常交易 / 欺诈交易 | 0 / 1 |
| 不及格 / 及格 | 0 / 1 |
| 不流失 / 流失 | 0 / 1 |

在这些任务里，SVM 感兴趣的不只是 `猜对 class`，还包括 `这个分界标准到底留了多少余量`

### 它和 logistic regression、k-NN 有什么不同

把 SVM 和前面的模型并排看，差别就会更清楚。

| 模型 | 中心问题 |
| --- | --- |
| logistic regression | 用什么线性 score 和 threshold 来切开 class？ |
| k-NN | 这个点周边的相似案例属于什么 class？ |
| SVM | 哪一条能把 class 分开、同时又留出更多余量的 boundary 更好？ |

这个比较很重要。三种模型都在做 classification，但它们定义 `好的判断标准` 的方式并不一样。

- logistic regression 更容易读出 score 与像 probability 一样的输出
- k-NN 更容易展示基于周边案例的判断
- SVM 更容易展示以 boundary 质量和 margin 为中心的判断

所以读取 SVM 时，不能只看最终 class prediction，还要一起看 `boundary 到底有多紧`，以及 `哪些点在真正撑住这条 boundary`

### 什么时候适合先把 SVM 放上候选

SVM 不是所有分类问题的默认答案，但当 `boundary 稳定性本身` 很重要时，它会是很好的候选。

| 当前问题状态 | 为什么先考虑 SVM | 先确认什么 |
| --- | --- | --- |
| 分类边界看起来太紧 | 因为它会优先寻找更大 margin 的 boundary | 边界附近案例是不是很多 |
| 只要有小扰动 class 就常常翻转 | 因为需要一种更稳定的分割线思路 | 哪些点看起来像 support vector |
| 已经存在线性 boundary 候选，但余量值得怀疑 | 因为即使都能分开，也能继续比较更好的 boundary | 和 baseline 或 logistic regression 有什么不同 |
| 想把边界附近案例作为 review 对象管理 | 因为 margin 附近案例适合单独记录 | 哪些案例应该继续留在 review 里 |
| 以后可能扩展到非线性 boundary | 因为 linear SVM 能自然接到 kernel SVM | 当前线性是不是已经足够 |

这张表的关键，是把 SVM 放在 `另一个分类器` 之外，更像 `更强地追问什么是好 boundary 的候选`。

这一节会把它和前面模型的差异再抓得更明确一些。

| 模型 | 先抓住的问题 | 这一节更强调的标准 |
| --- | --- | --- |
| logistic regression | 用什么 score 和 threshold 来切开 class？ | 像 probability 一样读取的输出与线性 boundary |
| k-NN | 应该参考周边哪些案例？ | 局部 neighbors 和距离标准 |
| SVM | 多条 boundary 里，哪一条更稳定？ | margin 与 support vector |

SVM 会把中心问题从 `能不能画出 boundary` 换成 `这条 boundary 到底留了多少余量、看起来有多稳定？` 只有先把这个标准固定住，后面的 soft margin、kernel、`C` 才不会被读成只是另一串选项，而会被读成 `调整好 boundary 标准的装置`。

再补上一点，SVM 这一节也会直接接到前面一直在整理的比较记录结构。把 SVM 放上候选时，不要只留下 `margin 很大` 这一句话，还要一起记下 `哪些案例留在 margin 附近`、`它和 baseline 或别的候选相比哪里更稳定`、`下一步还应该调整什么`。margin 附近案例首先应该被读成提高 review 优先级的信号，而不是直接当成原因已经解释完毕。

| 需要一起留下的记录 | 为什么需要 |
| --- | --- |
| baseline 与 SVM 的比较 | 用来看 margin 视角到底比简单标准多改变了什么 |
| margin 附近案例 | 用来找出应该继续留作 review 对象的模糊案例 |
| 看起来像 support vector 的点 | 用来再次检查到底哪些点最会摇动 boundary |
| 下一步实验问题 | 用来决定是去看 `C`、提高 kernel 候选，还是回头再看特征 |

## 案例与示例

如果这个直觉只停在抽象层面，很容易变模糊，所以还需要把它放回工作场景里再读一次。

### 案例 1. 欺诈交易探测

- 如果 margin 太小：
  - 正常交易和欺诈交易之间的 boundary 会变得太紧
  - 金额、地区、时间这些信号只要微微变化，就容易翻类
- 如果 margin 更大：
  - boundary 在两边都能留出更多空间
  - 模糊案例仍然存在，但标准本身没那么容易晃动

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-04-zh.mmd"
```

### 案例 2. 简历筛选

- 如果 margin 太小：
  - 少数非常特殊的简历会过度拉动标准
  - 一旦评分规则变化，或有不同背景的候选人出现，结果就容易晃动
- 如果 margin 更大：
  - boundary 不会那么容易被一两个例外点拉走
  - 标准更可能保持在一个更一般、更容易解释的方向上

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-05-zh.mmd"
```

`SVM 的 margin 直觉，会直接连到：模型生成的 boundary 在现实工作里到底会多敏感地摇晃`

## 练习与示例

### Python 例子：一旦完美分离被打破，会发生什么

这次在前一个例子里，再加入一个靠近 boundary 的模糊 negative 点。

- 问题场景：原本还能分开的两类之间，插进来一个例外点
- 输入(input)：
  - negative 点
  - positive 点
  - 多个候选 boundary `boundary_x`
- 期待输出(output)：
  - negative 一侧最近距离
  - positive 一侧最近距离
  - margin 值
- 要检查的概念：
  - 有些 boundary 可能不再能完美分离
  - 一旦完美分离变困难，就不只是看 `margin 大不大`，还要一起想 `允许多少侵入`

```python
# 这个例子比较 SVM 多个边界候选的 margin，以及像 support vector 一样起作用的近邻点。
negative = [(1.0, 2.0), (2.0, 3.0), (3.0, 2.5), (4.7, 2.4)]
positive = [(5.0, 2.2), (6.0, 3.2), (7.0, 2.8)]

for boundary_x in [4.0, 4.8, 5.2]:
    neg_min = min(boundary_x - x for x, _ in negative)
    pos_min = min(x - boundary_x for x, _ in positive)
    margin = min(neg_min, pos_min)

    print("boundary x =", boundary_x)
    print("  negative-side nearest distance =", round(neg_min, 3))
    print("  positive-side nearest distance =", round(pos_min, 3))
    print("  margin =", round(margin, 3))
    print("  perfectly separates? =", neg_min > 0 and pos_min > 0)
    print()
```

示例输出如下。

```text
boundary x = 4.0
  negative-side nearest distance = -0.7
  positive-side nearest distance = 1.0
  margin = -0.7
  perfectly separates? = False

boundary x = 4.8
  negative-side nearest distance = 0.1
  positive-side nearest distance = 0.2
  margin = 0.1
  perfectly separates? = True

boundary x = 5.2
  negative-side nearest distance = 0.5
  positive-side nearest distance = -0.2
  margin = -0.2
  perfectly separates? = False
```

这个输出里最重要的点很明确。

- 边界附近只多一个例外点，就可能让某些候选 boundary 失去完美分离
- 即使还能分开，margin 也可能变得非常小
- 所以现实里的 SVM 会从 `只追求完美分离` 转向 `margin 和允许错误一起调整`

### 学术背景与历史

SVM 在 statistical learning theory 和 generalization 讨论里占据很重要的位置。前面已经看过，generalization 更接近 `在新数据上也能保持合理判断`，而不是只看 training data 是否拟合得很好。

在这一节里，历史只作为辅助背景，帮助读者抓住：为什么 `好的 boundary` 要通过 margin 单独提出来问。代表性的里程碑是 Cortes 和 Vapnik 的 *Support-Vector Networks*。这里重要的不是证明细节，而是下面这种变化。

1. classification 可以读成寻找 boundary 的问题
2. boundary 候选不止一条
3. 所以必须有 `哪条 boundary 更好` 的标准
4. SVM 用最大化 margin 的语言给出了这个标准

### 再改一个值：如果例外点更靠近 boundary，什么保持不变，什么会改变

现在把那个模糊的 negative 点从 `(4.7, 2.4)` 再往右移到 `(4.9, 2.4)`。

```python
# 这个例子比较 SVM 多个边界候选的 margin，以及像 support vector 一样起作用的近邻点。
negative = [(1.0, 2.0), (2.0, 3.0), (3.0, 2.5), (4.9, 2.4)]
positive = [(5.0, 2.2), (6.0, 3.2), (7.0, 2.8)]

for boundary_x in [4.8, 4.95]:
    neg_min = min(boundary_x - x for x, _ in negative)
    pos_min = min(x - boundary_x for x, _ in positive)
    margin = min(neg_min, pos_min)

    print("boundary x =", boundary_x)
    print("  negative-side nearest distance =", round(neg_min, 3))
    print("  positive-side nearest distance =", round(pos_min, 3))
    print("  margin =", round(margin, 3))
    print("  perfectly separates? =", neg_min > 0 and pos_min > 0)
    print()
```

示例输出如下。

```text
boundary x = 4.8
  negative-side nearest distance = -0.1
  positive-side nearest distance = 0.2
  margin = -0.1
  perfectly separates? = False

boundary x = 4.95
  negative-side nearest distance = 0.05
  positive-side nearest distance = 0.05
  margin = 0.05
  perfectly separates? = True
```

### 什么保持了不变，什么发生了改变

- 保持不变的点：问题仍然不是只问 `能不能分开`，而是 `分开时到底留了多少余量`
- 发生变化的点：例外点再靠近一点以后，原本看起来还可行的 boundary 可能直接失去完美分离，或只剩极小的 margin
- 首先要留下的判断：即使都能分开，margin `0.2` 和 margin `0.05` 的稳定性也完全不同

这个练习让 SVM 不再只是 `能把答案分对的分类器`，而重新读成 `比较 boundary 质量的模型`。重要的不是只看一个分类结果，而是读出：哪些案例会把 boundary 挤得更紧，哪些案例会增加 generalization 风险。反复挪动一个例外点，才能让 margin 不只是停留在数值定义上，而会连到真正的 `摇晃感`。

| 通用记录语言 | 这次练习里应立刻留下的内容 |
| --- | --- |
| 看见的结构 | 只把一个边界附近例外点稍微挪动，separability 和 margin size 就一起剧烈变化 |
| 解释边界 | 在一个 toy example 里 margin 变小，并不能直接证明同一条 boundary 在所有真实数据里都一定不好 |
| 下一个问题 | 如果引入 soft margin 和 `C`，应该允许多少侵入？和别的分类器比较时，又会先看见什么差别？ |

这一节的核心，不是背住 SVM 这个名字，而是固定住：好的 boundary 应该按什么标准来读。

把整条流程再重新绑一次，会变成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-06-zh.mmd"
```

| 需要一起看的东西 | 这一节先问的问题 | 立刻会接到哪里 |
| --- | --- | --- |
| margin 与 support vector | 多条 boundary 里，哪条留了更多余量、看起来更稳定？ | P4-13.2 kernel 与 nonlinear boundary |
| soft margin 与允许错误 | 比起只追求完美分离，应该选择怎样的平衡？ | P4-9 hyperparameter 和 `C` 的读取 |
| 和前面模型的比较 | 除了 logistic regression 和 k-NN，现在又多了什么新的标准？ | 后面分类器比较与 generalization 读取 |

## 检查清单

- 能不能把 SVM 说明成：在能分开 class 的 boundary 里，继续寻找 `margin 更大` 的那条？
- 能不能把 margin 读成 boundary 和最近数据点之间的安全余量宽度？
- 能不能指出哪些案例像 support vector 一样，真的在撑住 boundary？
- 是否理解：在真实数据里，比起完美分离本身，`余量` 和 `允许错误` 之间的平衡更重要？
- 在当前问题里，余量和 boundary 稳定性是不是比单纯分开 class 更重要？
- 是否把 near-margin 案例的性质和最终 score 一起看？
- 能不能说明：和 logistic regression、k-NN 相比，SVM 的问题是 `哪条 boundary 更好？`

## 出处与参考资料

- scikit-learn, *Support Vector Machines*, scikit-learn User Guide, 确认日期: 2026-06-27. <https://scikit-learn.org/stable/modules/svm.html>{: target="_blank" rel="noopener noreferrer" }
- C. Cortes and V. Vapnik, *Support-Vector Networks*, Machine Learning, 1995, 确认日期: 2026-07-19. [https://doi.org/10.1007/BF00994018](https://doi.org/10.1007/BF00994018){: target="_blank" rel="noopener noreferrer" }
