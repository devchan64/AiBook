# P4-15.4 补充学习：如何第一次比较 Extra Trees 与随机森林

> Section ID: `P4-15.4`
> Version: `v2026.07.20`

在 P4-15.1 学完随机森林(random forest)之后， 读者很快也会遇到一个名字相近的模型：Extra Trees(Extremely Randomized Trees)。 因为这两者都像是 `把很多树聚起来再取平均的森林`， 所以一开始很容易把它们当成几乎一样的模型。

但它们在 `随机性到底注入到哪里`、 `分支标准是怎样选的`、 以及 `bootstrap 与 OOB 是否属于默认流程` 这几件事上， 有明确差别。

这一节不会再重复随机森林的正文解释， 而是把读者第一次比较 Extra Trees 时最容易混淆的地方， 整理成一节补充学习。

## 本节范围

本节回答以下问题。

- Extra Trees 和随机森林属于同一家族吗？
- 两者都把很多树拿来平均，但真正不同的是什么？
- `best split` 与 `random threshold` 的差别是什么？
- 为什么说 Extra Trees 更随机？
- 在随机森林与 Extra Trees 里，OOB(out-of-bag) 应该怎样不同地理解？

这一节会先收束 `随机森林与 Extra Trees 应该在哪里看成相同、又应该在哪里读出差异` 这个问题。 Extra Trees 与梯度提升(gradient boosting)的哲学差异，会在 P4-16.1、P4-16.2 重新连接。

## 用补充学习：如何第一次比较 Extra Trees 与随机森林留下的判断标准

- 你可以把 Extra Trees 解释成 `加入了更强随机性的树集成`。
- 你可以从 `样本抽取`、`分支阈值选择`、`OOB 成立条件` 这几个标准来比较随机森林与 Extra Trees。
- 你可以在入门层面说明：Extra Trees 往往会再多降一点 variance，但也可能多加一点 bias。
- 你可以说明什么时候值得把随机森林与 Extra Trees 一起列为比较候选。

## 为什么需要这一节

刚理解完随机森林时， 很容易出现下面这种误解。

- 两者都是森林
- 两者都随机选 feature
- 那它们不就是名字不同，其实是同一个模型吗？

这里还需要再往下分一层。

| 问题 | 随机森林 | Extra Trees |
| --- | --- | --- |
| 训练数据 | 通常是 bootstrap sample | 默认是完整训练集 |
| 分支阈值 | 在候选里搜索最好的 split | 随机抽阈值，再在其中选择 |
| 随机性强度 | 大 | 更大 |
| 默认 OOB 流程 | 自然连得上 | 默认设置下连不上 |

所以， Extra Trees 虽然仍然属于 `和随机森林相同的森林家族`， 但更准确的读法是： `连分支标准的选择方式也进一步随机化的森林。`

## 主要学习内容

### Extra Trees 也属于同一个树集成家族吗

scikit-learn 用户指南把 random forest 和 Extra-Trees 都解释成 `randomized decision tree ensemble` 家族里的 averaging algorithm。 也就是说， 两者都会建立很多棵树， 再把这些树的预测做平均或聚合， 以提升泛化与稳定性。

如果先把共同点固定下来， 大致是下面这些。

- 两者都使用很多决策树(decision tree)
- 两者都会在只看部分特征的情况下制造分支候选
- 两者都会把多棵树的预测做平均或聚合
- 两者都很强调：比起单棵树，要尽量减少摇摆

所以没必要把 Extra Trees 读成 `完全新的另一家人`。 一开始把它定位成 `非常接近随机森林的比较候选` 就够了。

### 核心差异 1：分支阈值是怎么选的

scikit-learn 用户指南说明， random forest 会在每个 node 里搜索 `best split`。 而 extremely randomized trees 也会看特征子集， 但它会先为每个特征随机抽出若干阈值， 再从这些随机阈值里选相对更好的那个。

换成更适合初学者的说法：

- 随机森林更接近：`这一层到底在哪切最好？`
- Extra Trees 更接近：`先随机试几刀，再用里面相对不差的那一刀。`

所以在 Extra Trees 里， 随机的不只是特征选择， 还包括 `到底从哪里切`。

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-01-zh.mmd"
```

这张图的重点是： 两者都共享 `特征子集` 这件事， 但在 `阈值怎么定` 上态度不同。

### 核心差异 2：bootstrap 的默认值不同

scikit-learn 用户指南说明， random forest 的默认值是 `bootstrap=True`， 而 Extra Trees 的默认值是 `bootstrap=False`。 Extra Trees 的 API 文档也说明， 在 `bootstrap=False` 时， 每棵树会直接用完整数据集训练。

这个差异比第一眼看起来更重要。

| 项目 | 随机森林默认值 | Extra Trees 默认值 |
| --- | --- | --- |
| `bootstrap` | `True` | `False` |
| 每棵树的输入 | 有放回抽样得到的样本 | 完整训练集 |
| 能不能直接用 OOB | 默认流程里自然成立 | 默认设置下不成立 |

所以， Extra Trees 虽然是 `更随机的森林`， 但这份额外随机性并不一定来自 `抽不同的样本`。 在默认设置里， 它更核心的随机性来自 `阈值随机化`， 而样本本身仍然是完整训练集。

### 核心差异 3：OOB 不是两者共享的默认抓手

如同 P4-15.3 所示， OOB 必须建立在 `bootstrap 漏掉了样本` 这件事上。 scikit-learn API 文档也说明， 无论是 random forest 还是 Extra Trees， `oob_score` 都只有在 `bootstrap=True` 时才能使用。

因此：

- 随机森林默认就是 `bootstrap=True`，所以 OOB 会自然接上
- Extra Trees 默认是 `bootstrap=False`，所以默认情况下不能把 OOB 当成检查抓手

很多读者在这里会疑惑： `为什么 Extra Trees 看不到 OOB？` 这不是模型换了另一个完全不同的道理， 而是默认抽样策略不同。

### 为什么 Extra Trees 更随机，却仍然值得当候选

scikit-learn 用户指南说明， extremely randomized trees 会在 split 计算阶段注入更多随机性， 这样可能进一步减少一点 variance， 但也会多增加一点 bias。

压成一句话就是：

`单棵树可能没那么精细，但整个森林可以由彼此更不像的树组成。`

所以 Extra Trees 可以被读成： 稍微放弃一些 `单棵树里精细地搜 split`， 换取 `整个森林里更大的多样性`。

| 视角 | 随机森林 | Extra Trees |
| --- | --- | --- |
| 单棵树的 split 搜索 | 更仔细 | 更粗一些 |
| 整个森林的多样性 | 大 | 可能更大 |
| 期待效果 | 稳定性提升 | 稳定性提升 + 进一步降低 variance 的可能 |
| 可能一起出现的代价 | 计算成本 | 稍微更大的 bias |

这张表最重要的不是 `Extra Trees 一定更好`， 而是 `随机性注入的位置不同`。

### 什么时候值得把 Extra Trees 一起比较

在和随机森林同一组候选里， 当读者想要一个 `稍微更快、也稍微更随机的森林` 时， Extra Trees 就很值得一起试。

| 当前情况 | 为什么一起列上 Extra Trees | 一起检查什么 |
| --- | --- | --- |
| 已经懂随机森林，但还想多一个比较候选 | 因为它是树集成里非常近的一条比较轴 | test 上是否真的有差异 |
| 深层 split 搜索的成本让人有负担 | 因为 split 搜索可能更简单 | 速度收益是否真的有体感 |
| 想更强地压低单棵树的摇摆 | 因为 split 阶段的随机性更大 | 多出来的 bias 会不会拉低 test |
| 当前更关心 train/test 比较，而不是 OOB | 因为默认 `bootstrap=False`，所以对 OOB 的依赖更弱 | 额外的 validation 或 test 管理 |
| 想同时比较 importance、预测稳定性、计算时间 | 因为它是和随机森林天然并排的兄弟模型 | importance 解释是否被过度相信 |

这个表的重点不是说 `一定要加 Extra Trees`， 而是把它放对位置： `一个应该紧挨随机森林一起试的比较候选。`

## 案例与示例

### 案例 1：在客户流失问题里，两片森林该怎样不同地读

假设某个团队先用随机森林做客户流失(churn)预测。 test 性能还算可以， 但团队会留下这样的疑问： `这片森林会不会把分支切得太细？` `如果随机化更粗一点，反而会不会更稳定？`

此时把 Extra Trees 列进来， 并不是因为需要 `一套完全不同哲学的模型`。 而是想在同一个树集成家族里检查： `如果分支搜索更随机，结果会怎样变化？`

例如：

- 随机森林会更认真地搜索像 `最近登录数 < 3.5`、`支付失败数 < 1.5` 这种阈值
- Extra Trees 会更随机地抽阈值，再从里面选相对不差的那个

如果把团队正在看的客户表压缩得很小， 可能像这样。

| 客户 | 最近登录数 | 支付失败数 | 咨询次数 | 实际流失 |
| --- | ---: | ---: | ---: | --- |
| A | 1 | 2 | 4 | 是 |
| B | 2 | 1 | 3 | 是 |
| C | 5 | 0 | 1 | 否 |
| D | 6 | 0 | 0 | 否 |

看这张表时， 随机森林更接近认真搜索： `登录数在 2 和 5 之间到底从哪里切最好？` 以及 `支付失败数在 0 和 1 之间哪个阈值更合理？` Extra Trees 则更接近： 先随机试几个切点，再用里面相对不差的那一个。

因此， 连比较问题本身也会稍微不同。

| 比较问题 | 在随机森林里更先看的点 | 在 Extra Trees 里更先看的点 |
| --- | --- | --- |
| 为什么它预测对了？ | 更精细的 split 搜索是不是帮了忙？ | 更粗的随机化是不是反而更利于泛化？ |
| 为什么它预测错了？ | 细阈值是不是被例外客户拉走了？ | 粗阈值是不是把关键边界弄模糊了？ |
| 下一步该调什么？ | `max_features`、depth、leaf 大小 | `max_features`、depth，以及必要时 `bootstrap` |

所以实验备忘里不能只写 `两者都是森林`。 还应该一起留下：

- test 分数差
- train 与 test 的间隔
- importance 排名是否大改
- 计算时间差

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-02-zh.mmd"
```

这个流程里真正重要的不是 `谁赢了`， 而是： `当随机性注入的位置改变时，性能、摇摆、计算成本一起怎么变。`

### 案例 2：为什么在不良品检测里也值得一起试 Extra Trees

在工厂不良品检测问题里， 传感器值往往很多， 某些边界还可能非常细。 假设团队先用随机森林， 发现 train 性能很高， 但 test 会随着某些生产日的例外模式而摇摆。

这时把 Extra Trees 一起跑， 并不是因为它 `更高级`， 而是想检查： `如果不那么执着地去搜最细阈值，会不会反而少被某一天的偶然边界绑住？`

如果把传感器记录缩成一个很小的场景：

| 批次 | 温度偏差 | 振动偏差 | 压力偏差 | 实际不良 |
| --- | ---: | ---: | ---: | --- |
| A | 0.8 | 0.9 | 0.3 | 是 |
| B | 0.7 | 0.8 | 0.4 | 是 |
| C | 0.2 | 0.3 | 0.2 | 否 |
| D | 0.3 | 0.2 | 0.1 | 否 |

随机森林可能会去搜索像 `振动偏差 = 0.82` 这种更细的切点。 有时这会有帮助， 但如果数据小， 或者某一天混进了噪声， 这份噪声也可能被读成边界。 Extra Trees 使用更随机的阈值， 所以单棵树也许看上去不那么精细， 但整片森林也可能因此更不容易像那些例外日期的模式。

在这个场景里， 下面这些记录会让比较更容易。

- 随机森林在 train 上提升的分数，是否还能在 test 上维持
- Extra Trees 是否在保持 test 相近或略高的同时，减少了摇摆
- 两者的高 importance 传感器是否相似
- 计算时间差在实务里是否明显

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-03-zh.mmd"
```

这个案例的核心不是 `Extra Trees 总是更准`， 而是： `当细阈值搜索对例外模式太敏感时，Extra Trees 会成为紧挨着的比较候选。`

## 练习与示例

这个例子把 `RandomForestClassifier` 和 `ExtraTreesClassifier` 并排训练在同一份数据上， 一起检查默认设置差异， 以及分数的阅读重点。

- 问题场景：即使随机森林和 Extra Trees 看起来相似，也要检查 `bootstrap`、`OOB` 与 train/test 的阅读点到底怎么不同
- 输入(input)：乳腺癌分类数据里的 30 个连续特征
- 标签(label)：恶性 / 良性 class
- 要确认的概念：
  - 随机森林的默认流程天然贴合 `bootstrap=True`
  - Extra Trees 的默认流程是 `bootstrap=False`，所以 OOB 不会自动跟上来
  - 比较两者时，不该只看 test 分数，也要一起看 train/test 间隔与计算时间

```python
# 这个例子在同一个乳腺癌数据上比较 Random Forest 和 Extra Trees 的默认差异与分数。
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

rf = RandomForestClassifier(
    n_estimators=300,
    bootstrap=True,
    oob_score=True,
    random_state=42
)

et = ExtraTreesClassifier(
    n_estimators=300,
    random_state=42
)

rf.fit(X_train, y_train)
et.fit(X_train, y_train)

print("[Random Forest]")
print("  bootstrap     :", rf.bootstrap)
print("  oob score     :", round(rf.oob_score_, 3))
print("  train accuracy:", round(rf.score(X_train, y_train), 3))
print("  test accuracy :", round(rf.score(X_test, y_test), 3))

print("[Extra Trees]")
print("  bootstrap     :", et.bootstrap)
print("  train accuracy:", round(et.score(X_train, y_train), 3))
print("  test accuracy :", round(et.score(X_test, y_test), 3))
```

示例输出可能大致如下。 实际值会因切分方式、库版本、随机设置而略有变化。

```text
[Random Forest]
  bootstrap     : True
  oob score     : 0.96
  train accuracy: 1.0
  test accuracy : 0.947

[Extra Trees]
  bootstrap     : False
  train accuracy: 1.0
  test accuracy : 0.953
```

这个结果的阅读顺序是：

1. 两者的 train accuracy 都可能很高，所以不能只看 train 就下结论。
2. 随机森林可以和 OOB 一起读，但 Extra Trees 在默认设置下没有 OOB。
3. 即使 test accuracy 看起来相近，或某次 Extra Trees 稍高，也不能只凭这一次数字就推广，要重新检查它在不同数据集上的表现差异。

所以这个例子的重点不是 `谁永远更好`， 而是通过输出本身直接确认： `即使都属于森林家族，随机性注入的方式也不一样。`

## 检查清单

- 你能不能把 Extra Trees 解释成和随机森林同属 `randomized tree ensemble` 家族？
- 你能不能把 Extra Trees 解释成 `和随机森林非常接近的兄弟模型`？
- 差异比起 `feature 随机选择` 本身，更明显地出现在 `threshold 到底随机到什么程度`，这一点你理解了吗？
- 你能不能说明 `best split` 与 `random threshold` 的差别？
- 你知不知道随机森林默认自然连到 bootstrap 与 OOB 流程，而 Extra Trees 默认设置下不会？
- 你能不能说明为什么 Extra Trees 默认设置下不会立刻出现 OOB？
- 你是不是把 Extra Trees 读成一个可能多降一点 variance、但也多加一点 bias 的比较候选？
- 你是否知道比较随机森林与 Extra Trees 时，要一起看 train/test 间隔、OOB 可用性、以及计算成本？

## 出处与参考资料

- scikit-learn, "1.11.2. Random forests and other randomized tree ensembles", User Guide, [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" } (确认日: 2026-07-09)
- scikit-learn, "ExtraTreesClassifier", API Reference, [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html){: target="_blank" rel="noopener noreferrer" } (确认日: 2026-07-09)
- scikit-learn, "RandomForestClassifier", API Reference, [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" } (确认日: 2026-07-09)
- Pierre Geurts, Damien Ernst, Louis Wehenkel, "Extremely randomized trees", *Machine Learning*, 63(1), 3-42, 2006, 确认日期: 2026-07-19. [https://doi.org/10.1007/s10994-006-6226-1](https://doi.org/10.1007/s10994-006-6226-1){: target="_blank" rel="noopener noreferrer" }
