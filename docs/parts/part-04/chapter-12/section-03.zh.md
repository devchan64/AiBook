# P4-12.3 使用 k-NN 时，应该先检查什么？

> Section ID: `P4-12.3`
> Version: `v2026.07.24`

P4-12.1 看过了 k-NN 的直觉，P4-12.2 看过了为什么 distance 和 scale 会改变结果。现在剩下的问题是：

当 k-NN 的判断开始摇晃时，应该先重新检查什么？

本节的目的，不是再把 preprocessing 一般论重新讲一遍，而是整理在读取 k-NN 时，`哪里应该先被检查`。

## 本节范围

这一节回答下面这些问题。

- 在什么样的问题里，k-NN 适合作为第一个候选？
- 什么信号出现时，应该先怀疑 distance 或 scale？
- 在 `distance rule`、`k`、`data representation` 之间，应该先重新看哪个？
- 对需要 review 的 query，应该怎么读？

## 用使用 k-NN 时，应该先检查什么？留下的判断标准

- 能说明什么样的问题值得先把 k-NN 放上候选
- 能说明哪些信号意味着应该先怀疑 distance 或 scale
- 当结果摇晃时，能排出重新检查的顺序

## 主要学习内容

### 什么时候适合先把 k-NN 放上候选

k-NN 并不是所有 classification 问题的默认答案。但在 `用附近相似案例来解释` 很自然的问题里，它会是一个很好的第一比较候选。

| 当前问题状态 | 为什么会先想到 k-NN |
| --- | --- |
| 相似案例往往得到相似结果 | 因为可以很自然地用附近 neighbors 来解释 prediction |
| 局部模式比一条全局规则更重要 | 因为可以直接把 query 和 주변案例比较 |
| 团队想先给出基于案例的判断，而不是基于公式的判断 | 因为 neighbors 本身就能成为解释 |
| 数据规模还不算太大，比较成本可承受 | 因为 prediction time 的比较仍然是现实可行的 |

关键点不是 `因为写不出公式，所以才用 k-NN`。而是：`当局部相似性本来就有意义时，k-NN 可以成为很好的起点`。

### 什么信号出现时，应先怀疑 distance 或 scale

在 distance-based model 里，如果表现很奇怪，常常比起先怀疑模型结构，更应该先问：`是不是某个轴几乎单独决定了全部 distance？`

| 出现的信号 | 首先应怀疑什么 | 原因 |
| --- | --- | --- |
| 某一列的数字范围远大于其他列 | scale domination | 因为一个大轴可能独占 distance |
| scale 调整前后，neighbor 变化很大 | representation dependence | 因为 nearness 的定义对表示方式过于敏感 |
| 一个小范围特征明明重要，却几乎不出现在 prediction 里 | 被大轴掩埋 | 因为有用信息可能被 distance 埋掉 |
| 同类 query 反复聚到 boundary 附近 | distance rule 或 `k` 设置 | 因为 neighbor 顺序可能很不稳定 |

这张表的目的，不是把 scale adjustment 当成万能解法，而是让读者先确认：`nearness 的定义是不是已经在摇晃了`

### 应该先重新看什么

当结果开始摇晃时，通常按下面这个顺序检查会比较好。

1. 这个问题真的适合用 `附近案例比较` 来读吗？
2. 当前的 distance rule 适合这个问题吗？
3. `k` 是不是太小或太大？
4. scale 或 data representation 是否让某个轴被过度放大？
5. prediction time 的比较成本在实际里能否承受？

这个顺序之所以重要，是因为每个问题都指向不同层次的原因。

- 第 1 项是 `模型家族` 的问题
- 第 2 和第 3 项是 `判断规则` 的问题
- 第 4 项是 `表示方式` 的问题
- 第 5 项是 `运营成本` 的问题

所以，即使只是同一句 `结果看起来怪怪的`，里面也可能混着几个不同层次的原因。

尤其在第 4 项里，一旦真的怀疑到 scale 或 representation，有关 preprocessing 的一般论就不应在本节再长篇展开，而更适合回到 `P4-7.2 Preprocessing` 去重新对 기준。

### 如果把 P4-12.1 的同一个 query 再拿回来读

如果把前一节的 query `(4.0, 4.2)` 重新拿回来，检查顺序就会变得更具体。

| 要重新问的问题 | 在 `(4.0, 4.2)` 上实际看到什么 | 现在应该下什么判断 |
| --- | --- | --- |
| `k` 是否过于敏感？ | `k=1` 时是 class 1，`k=3` 时变成 class 0 | 要重新检查 `k`，因为一两个例外点就可能摇动结果 |
| neighbor 组成是否混杂？ | 附近 label 混成了 `1, 0, 0, 1, 0` 这样 | 这个 query 很可能靠近 boundary |
| 如果换一个 distance rule，会不会改变？ | 即使坐标不变，neighbor 顺序也可能跟着变 | 要继续接到 `P4-12.2` 的 distance-rule 比较 |
| 是否还需要怀疑 scale？ | 在这个 toy coordinate 例子里，scale 不是主要问题 | 但在真实数据里，只要数值范围差很多，就要回头看 `P4-7.2` 和 `P4-12.2` |

这张表的目的，不是让读者去背 checklist，而是拿着一个具体 query，看到 `应该从哪里开始重新怀疑`。

### 把一个 query 一路检查到底的小流程

如果把前面的表再压缩成真正的判断顺序，那么 `结果很模糊` 这句话，就不再只是感觉，而会变成寻找 `到底是哪一步在摇晃` 的过程。

1. 先看 neighbors 是否明显偏向一侧
2. 如果只差一两个点，就看把 `k` 稍微改一下以后，解释还稳不稳
3. 如果 `k` 稍微一改还是继续摇晃，就看 distance rule 本身是否适合当前问题
4. 如果特征的数值范围差很多，最后再去看 scale 和 data representation

所以，一个 review query 更适合被读成：`能暴露判断规则哪一层正在摇晃的观察点`，而不是 `一个错掉的 prediction`

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-3-mermaid-01-zh.mmd"
```

### 对需要 review 的 query，应该怎么读

需要 review 的 query，通常是 `neighbor 组成没有明显偏向一边` 的情况。

例如：

| query | nearest labels | 现在怎么读 |
| --- | --- | --- |
| `(4.0, 4.2)` | `[1, 0, 1]` | 倾向 class 1，但很可能靠近 boundary |
| `(4.0, 4.2)` with `k=5` | `[1, 0, 1, 0, 0]` | 邻域一扩大，解释就可能改变，需要再检查 |

这里最重要的是：`neighbor 分裂了` 这件事，并不等于原因解释已经结束。它更像是在告诉读者：`下一步应该重看哪里`

也就是说，一个 review query 通常按下面这个顺序来读。

1. neighbor 组成分裂得有多厉害
2. 把 `k` 改一改以后，解释还稳不稳
3. 把 distance rule 改一改以后，neighbors 会不会换
4. scale 调整前后，哪些 neighbors 进来、哪些出去

这四个问题之所以重要，是因为它们各自对应不同的原因。

- 第 1 项在问：`这个 query 现在是不是靠近 boundary？`
- 第 2 项在问：`结果是不是对一两个例外 neighbors 太敏感？`
- 第 3 项在问：`当前 nearness 的定义适不适合这个问题？`
- 第 4 项在问：`表示方式是不是已经扭曲了判断？`

## 案例与示例

### 案例 1. prediction 看起来能用，但解释一直摇晃

某个订阅服务团队用 k-NN 来观察流失风险。prediction 本身似乎还可以，但两个看起来很相似的客户，却一再得到不同预测。

这时，不应该马上跳到 `是不是要换模型？`。首先应该重看下面这些点。

- 这个问题是不是本来就适合按 local similarity 来读？
- 当前 distance rule 是否适合这些 features？
- 是否用了像 `k=1` 这样过于敏感的设置？
- 支付金额这类大轴，是否压住了其他特征？

按这个顺序走，可以更好地把 `模型家族本身失败了` 和 `判断 기준 在摇晃` 区分开来。

所以，这里要留下的标准不是一句模糊的结论 `k-NN 要小心用`。更准确地说，是让读者能自己说出：`prediction 一旦开始摇晃，应该先从哪里重新打开检查`

## 练习与示例

这个例子固定同一个 query，观察 `k` 和 scale 调整会怎样改变邻居列表和 prediction。

- 问题场景：用月消费金额和客服咨询次数，通过 k-NN 判断流失
- 输入(input)：每个客户的 `monthly_spend`、`support_tickets`、`churn`
- 期望输出(output)：不同 `k` 下的 prediction、近邻 ID、scale 调整后的近邻变化
- 要确认的概念：
  - `k=1` 很容易被最近的一个案例牵动
  - 增大 `k` 后，局部多数表决可能改变
  - 数字范围不同的特征，在 scale 调整前后可能改变近邻顺序

```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

customers = pd.DataFrame(
    [
        {"id": "A", "monthly_spend": 30, "support_tickets": 0, "churn": 0},
        {"id": "B", "monthly_spend": 58, "support_tickets": 0, "churn": 0},
        {"id": "C", "monthly_spend": 61, "support_tickets": 0, "churn": 0},
        {"id": "D", "monthly_spend": 65, "support_tickets": 0, "churn": 0},
        {"id": "E", "monthly_spend": 40, "support_tickets": 8, "churn": 1},
        {"id": "F", "monthly_spend": 62, "support_tickets": 8, "churn": 1},
        {"id": "G", "monthly_spend": 90, "support_tickets": 9, "churn": 1},
    ]
)

X = customers[["monthly_spend", "support_tickets"]]
y = customers["churn"]
query = pd.DataFrame([{"monthly_spend": 63, "support_tickets": 7}])

for k in [1, 3, 5]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X, y)
    distances, indices = model.kneighbors(query, n_neighbors=k)
    neighbor_ids = customers.iloc[indices[0]]["id"].tolist()
    print("raw k=", k, "prediction=", int(model.predict(query)[0]), "neighbors=", neighbor_ids)

scaled_model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
scaled_model.fit(X, y)
knn = scaled_model.named_steps["kneighborsclassifier"]
scaled_query = scaled_model.named_steps["standardscaler"].transform(query)
distances, indices = knn.kneighbors(scaled_query, n_neighbors=3)
neighbor_ids = customers.iloc[indices[0]]["id"].tolist()
print("scaled k= 3 prediction=", int(scaled_model.predict(query)[0]), "neighbors=", neighbor_ids)
```

运行结果如下。

```text
raw k= 1 prediction= 1 neighbors= ['F']
raw k= 3 prediction= 0 neighbors= ['F', 'C', 'D']
raw k= 5 prediction= 0 neighbors= ['F', 'C', 'D', 'B', 'E']
scaled k= 3 prediction= 1 neighbors= ['F', 'E', 'G']
```

这个输出不是让读者马上说 `k-NN 错了`。同一个 query 在 `k=1` 时被最近的 F 强烈牵动，而在 `k=3` 时，C 和 D 进入邻域后 prediction 发生改变。再做 scale 调整后，客服咨询次数在距离计算中被更清楚地反映出来，于是 E 和 G 进入近邻集合。因此，遇到摇晃的 query 时，应该按顺序重新打开 `k`、邻居构成和 scale。

## 检查清单

- 能不能说明在局部相似性很重要的问题里，k-NN 可以是很好的第一比较候选？
- 能不能区分：哪些问题适合先把 k-NN 放上候选，哪些不适合？
- 是否理解结果开始摇晃时，通常应该先重看 `distance rule`、`k`、`data representation`，再去谈模型名字本身？
- 能不能说明结果摇晃时，`distance rule`、`k`、`scale` 应该按什么顺序来看？
- 是否把 review query 读成 `需要重新检查的信号`，而不是 `原因已经确认`？

## 出处与参考资料

- scikit-learn, *Nearest Neighbors*, scikit-learn User Guide, 确认日期: 2026-06-27. <https://scikit-learn.org/stable/modules/neighbors.html>{: target="_blank" rel="noopener noreferrer" }
- scikit-learn, *Importance of Feature Scaling*, scikit-learn Examples, 确认日期: 2026-06-27. <https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html>{: target="_blank" rel="noopener noreferrer" }
