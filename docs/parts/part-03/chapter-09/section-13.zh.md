# P3-9.13 交给 Part 4 之前的问题边界

> Section ID: `P3-9.13`
> Version: `v2026.07.25`

_副标题: 在把问题交给预测任务之前，为什么必须一起闭合时间、个体、信息和产物形式边界？_

如果结构已经整理到足以梳理当前问题类型，那么最后还需要一起关上的，是一组边界。时间顺序是不是重要？同一个个体能不能混到两边？预测时点之后的信息有没有渗进输入？真实[输出格式(output format)](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-output-format)更像排序或连续值，而不是简单的 0/1 分类？这里重要的不是把术语名称越列越多，而是确认当前问题结构在这些边界面前是否能不自相矛盾地站住。

| 现在要检查的项目 | 当前要抓住的最小句子 |
| --- | --- |
| [time split](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-time-split) | 时间顺序重要的问题，不能和随机切分一样看 |
| [group split](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-group-split) | 如果同一个个体混到两边，性能可能会被夸大 |
| [data leakage](/AiBook/zh/reference/concept-glossary-pinyin/d/#glossary-data-leakage) | 如果预测时点之后的信息混进来，分数看起来再好也不能用 |
| [evaluation design](/AiBook/zh/reference/concept-glossary-pinyin/p/#evaluation-design) | 指标和切分方式是否合适，要和问题结构连起来看 |
| [ranking](/AiBook/zh/reference/concept-glossary-pinyin/p/#glossary-ranking) | 挑出前几条时，核心可能是顺序问题而不是类别问题 |
| multiclass / [regression](/AiBook/zh/reference/concept-glossary-pinyin/h/#glossary-regression) | 结果结构未必只是一个 0/1 标签 |

在梳理当前问题类型的这个阶段，只要下面这些边界已经关上，就已经足够。

- 这个问题是否首先要求按时间顺序切分？
- 是否必须避免同一个个体同时出现在两边？
- 结果之后的信息有没有混进输入？
- 实际目标是否比 0/1 分类更接近排序或连续值？

## 用一个小图来看

这个最后检查更重要的不是背下项目名称，而是按合理顺序把当前问题结构关起来。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-13-mermaid-01-zh.mmd"
```

在这一节里，比起把名字全部背下来，更重要的是确认：当前数据结构是否已经把时间边界、个体边界、信息边界和产物形式都关好了。在现在这个阶段，需要的不是把细节流程铺得很长，而是让当前结构能够不自相矛盾地说明：它在预测什么，又还有什么不应该预测。所以，这一节不该被读成术语清单，而应被读成一张最后的检查表：确认`切分设计`、`信息边界检查`、[产物形式选择](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-output-format)是否已经在梳理当前问题类型的阶段于当前问题结构里无矛盾地关上了。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label leakage`。用于确认信息边界依据：预测时点之后的信息如果混入特征，就可能成为标签代理。确认日: 2026-07-20. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Classification: ROC and AUC*。用于确认 ranking/evaluation design 依据：AUC 和 ROC 关注把正例排在负例之前的能力，并且不同于具体 threshold 的选择。确认日: 2026-07-20. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*。用于确认 provenance 视角下记录处理步骤、可复现性、版本管理和派生关系的依据。确认日: 2026-07-20. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
- Hyndman, Athanasopoulos, *Forecasting: Principles and Practice (3rd ed.)*, Section 5.10 Time series cross-validation. 用于确认 time split 依据：在有时间顺序的问题里，训练集只应包含早于测试观测值的观测值，不能用未来观测值构造 forecast。确认日: 2026-07-20. [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, *Cross-validation: evaluating estimator performance*, cross-validation iterators for grouped data. 用于确认 group split 依据：当组内依赖重要时，同一 group 的样本不应同时出现在配对的训练侧和验证/测试侧。确认日: 2026-07-20. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" }
