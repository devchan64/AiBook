# P4-7.4 补充学习：区分特征选择方式

> Section ID: `P4-7.4`
> Version: `v2026.07.26`

从 P4-7.1 到 P4-7.3，我们已经依次处理了[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#feature)挑选、输入表达问题拆分，以及预处理的基本判断。但在实际阅读中，读者很快就会遇到下面这些名字。

- 基于统计检验的特征选择
- 递归特征消除(recursive feature elimination, RFE)
- [降维(dimensionality reduction)](/AiBook/zh/reference/concept-glossary-pinyin/d/#dimensionality-reduction)

这些名字看起来都像是在 `减少输入，或者重新表达输入`，但它们到底按什么标准减少、又留下什么，其实并不一样。

## 各种缩减方式的分界标准

这一节回答下面这些问题。

- filter、wrapper、embedded 特征选择有什么不同？
- 基于统计检验的特征选择，是按什么思路运作的？
- 递归特征消除(RFE)是在重复什么？
- 降维和特征选择有什么不同？

这一节先收束 `该怎样区分减少输入或重新表达输入的那些名称`。各种降维算法的直觉和局限，会在 P4-18.1、P4-18.2 继续展开。

## 区分方法名称时要留下的判断

- 能把[特征选择(feature selection)](/AiBook/zh/reference/concept-glossary-pinyin/f/#feature-selection)和降维区分开来，而不是把它们当成同一件事混在一起。
- 能说明 filter、wrapper、embedded 方法分别是按什么标准去减少特征的。
- 能说明 RFE 是 `反复运行 model，并逐步减少不太重要特征的方法`。

## 先抓大图景

先看下面这张表。

| 方式 | 它保留或改变什么 | 判断标准 |
| --- | --- | --- |
| filter | 从原始特征里选出一部分 | 统计量、相关性、单变量分数 |
| wrapper | 反复比较原始特征的不同子集 | model 性能 |
| embedded | 在学习过程中一起得到重要度 | model 内部规则 |
| dimensionality reduction | 把原始特征重新表达成新的轴 | 方差、距离、结构保持等 |

核心是下面这句话。

`特征选择主要是在决定原始特征里哪些要留下，而降维是在把多个特征重新表达成更少的新轴。`

## 基于统计检验的特征选择属于哪一类

基于统计检验的特征选择，通常属于 filter 方法。也就是说，它会先给每个特征和正确答案之间的关系打分或做检验，再根据这个结果缩减特征候选。

这种方式在下面这些场景里比较直观。

- 特征很多，需要快速做一次初步整理时
- 在反复训练复杂 model 之前，想先把候选范围缩小时
- 想先逐个检查各个特征时

但作为代价，它往往不能充分反映 `特征组合一起产生的效果`。所以这一节把它看成更接近 `快速的一轮初步整理`。

## 递归特征消除(RFE)是在重复什么

可以把 RFE 看成 wrapper 方法的代表例子。非常简单地说，它是在重复下面这个顺序。

1. 用当前特征集合训练 model。
2. 去掉一部分重要度较低的特征。
3. 用剩下的特征重新训练。
4. 一直重复到减少到目标数量。

也就是说，RFE 是一种反复确认 `哪些特征在当前 model 里面帮助较小` 的方法。

它可能比 filter 方法更耗计算，但也更容易反映 `放在当前 model 里一起看时的有用性`。

## 为什么要把降维看成单独类别

降维看起来像是在扔掉特征，但实际上它更常见的是 `重新制造新轴`。

例如:

- 特征选择可以在 `age`、`income`、`visits` 里只留下两个
- 降维则可以把这三个特征混合起来，改成 `component_1`、`component_2` 这样的新轴

所以，降维应该和 `在保留原始列名的前提下减少列` 这类工作分开来读。

| 问题 | 特征选择 | 降维 |
| --- | --- | --- |
| 原始特征名还在吗 | 经常还在 | 通常会变成新轴 |
| 好解释吗 | 相对更容易 | 可能会更难 |
| 目的 | 减少不必要特征 | 压缩表达、总结结构、可视化 |

降维本身的目的和局限，会在 P4-18.1、P4-18.2 再更详细地看。

## 案例及示例

### 现在应该先想到哪种缩减方式

当各种方法名混在一起时，先把问题分成 `要不要保留原始列`、`是不是按 model 性能来减少`、`是不是要重新表达成新轴`，整理起来会快很多。

| 当前需要的判断 | 最先想到的方法 | 原因 |
| --- | --- | --- |
| 我想先快速把很多列做一次初步整理 | filter | 因为它可以用统计量或单变量分数快速缩减候选 |
| 我想按当前 model 标准减少帮助较小的特征 | wrapper，例如 RFE | 因为它会把特征子集和 model 性能一起反复比较 |
| 我想在学习过程中一起得到重要度 | embedded | 因为选择会随着 model 内部规则一起发生 |
| 比起解释，更重视压缩和结构总结 | dimensionality reduction | 因为它会把表达改造成新轴，而不是保留原始列 |

这个区分必须先立住，才不会把本质不同的工作都塞进 `降维` 这一句话里。

### 案例 1. 在客户分群前想减少特征，但方法名看起来混在一起时

一个营销团队在准备客户分群时，想先减少输入列。人最先看的标准，是 `最近访问`、`购买金额`、`折扣反应`、`咨询模式` 这些行为信号。

但在会议上，不同的方法名一下子全都冒出来。有人说先去掉相关性低的列，有人说反复跑 model 把重要度低的列减掉，还有人说直接用 PCA 把轴压缩。它们都被放在 `降维` 这个说法下面，但实际上留下什么、改变什么都不同。

```mermaid
--8<-- "assets/part-04/chapter-07/p4-7-4-mermaid-01-zh.mmd"
```

这里需要分清的是下面这些点。filter 方法更接近于快速检查原始特征，先缩小第一轮候选；wrapper 方法里的 RFE，则是按当前 model 性能反复减少特征。降维则更接近于不是挑出原始列中的一部分，而是把多个特征混合起来，重新表达成新轴。

可确认的结果也要分开读。filter 和 RFE 可以列出哪些原始列被保留下来了，而降维则会把表达改成 `component_1`、`component_2` 这样的新轴，所以解释方式本身也会变化。因此，即使都在说 `减少输入`，也必须先决定：你到底更想保留可解释性，还是想压缩成新的表达。

## 练习与示例

这个例子会在同一份数据上比较 filter 方法、RFE 和 PCA 各自留下了什么。

- 问题场景：想把六个客户行为特征减少到三个保留特征，或三个新轴
- 输入(input)：scikit-learn 生成的小型分类数据
- 期望输出(output)：保留下来的原始特征名、新 component 名、交叉验证分数和输入形状
- 要确认的概念：
  - filter 和 RFE 会从原始特征里挑出一部分
  - PCA 不保留原始特征名，而是重新表达成新轴
  - 分数看起来接近，也不代表解释性相同

可以改动的值:

- 把 `SelectKBest(..., k=3)`、`RFE(..., n_features_to_select=3)`、`PCA(n_components=3)` 里的 `3` 改成 `2` 或 `4`，保留特征数、新轴数量和分数都会一起变化。
- 改动 `class_sep=1.1` 或 `random_state=7`，被选中的特征列表和分数差距也可能变化。

```python
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE, SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

feature_names = [
    "visit_count",
    "avg_order",
    "discount_click",
    "support_calls",
    "days_since_login",
    "newsletter_open",
]

X, y = make_classification(
    n_samples=180,
    n_features=6,
    n_informative=3,
    n_redundant=1,
    class_sep=1.1,
    random_state=7,
    shuffle=False,
)

filter_selector = SelectKBest(score_func=f_classif, k=3).fit(X, y)
filter_features = [
    name for name, keep in zip(feature_names, filter_selector.get_support()) if keep
]

base_model = LogisticRegression(max_iter=1000)
rfe_selector = RFE(base_model, n_features_to_select=3).fit(
    StandardScaler().fit_transform(X),
    y,
)
rfe_features = [
    name for name, keep in zip(feature_names, rfe_selector.support_) if keep
]

models = {
    "filter_selected": X[:, filter_selector.get_support()],
    "rfe_selected": X[:, rfe_selector.support_],
}

print("filter keeps:", filter_features)
print("rfe keeps   :", rfe_features)
print("pca output  :", ["component_1", "component_2", "component_3"])

for name, selected_X in models.items():
    score = cross_val_score(base_model, selected_X, y, cv=5).mean()
    print(name, "cv=", round(score, 3), "shape=", selected_X.shape)

pca_score = cross_val_score(
    make_pipeline(StandardScaler(), PCA(n_components=3), base_model),
    X,
    y,
    cv=5,
).mean()
print("pca_reduced cv=", round(pca_score, 3), "shape=", (X.shape[0], 3))
```

运行结果如下。

```text
filter keeps: ['visit_count', 'discount_click', 'support_calls']
rfe keeps   : ['visit_count', 'avg_order', 'support_calls']
pca output  : ['component_1', 'component_2', 'component_3']
filter_selected cv= 0.817 shape= (180, 3)
rfe_selected cv= 0.828 shape= (180, 3)
pca_reduced cv= 0.617 shape= (180, 3)
```

这里首先要看的不是分数排名。filter 方法和 RFE 保留下来的原始特征列表不同，而 PCA 虽然也把输入减少成三个维度，却让原始列名消失了。因此，`减少到三个`这一句话并不够。还要一起判断：这是保留原始特征的特征选择，还是压缩成新表达的降维。

## Checklist

- 你有没有先区分当前要做的是挑原始列，还是把它们重建成新轴？
- 你有没有把快速初步整理和基于 model 的反复比较说成同一种方法？
- 当可解释性重要时，你能不能说明为什么特征选择可能比降维更合适？
- 你能不能把基于统计检验的特征选择通常理解成 filter 方法，而把 RFE 理解成一种反复训练 model 并逐步减少特征的 wrapper 方法？
- 你能不能说明，降维看起来和特征选择相似，但它是把原始特征重新表达成新轴的另一类问题？
- 你能不能把 filter、wrapper、embedded、降维区分开来，而不把它们混成同一种解法？

## 出处与参考资料

- scikit-learn developers, [Feature selection](https://scikit-learn.org/stable/modules/feature_selection.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-26.
- scikit-learn developers, [Unsupervised dimensionality reduction](https://scikit-learn.org/stable/modules/unsupervised_reduction.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-26.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-26.
