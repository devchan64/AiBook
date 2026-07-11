# P3-9.11 当 target 候选有多个，或标准在变化时，应该先固定什么

> Section ID: `P3-9.11`
> Version: `v2026.07.11`

在现实数据里，target 候选未必只会出现一个。像 `review_needed`、`final_status`、`status_type`、`priority_bucket` 这样的多个候选可能会一起出现；即使名字相同的 target，在不同时间里判定标准也可能不同。如果不先固定：哪一个是代表问题，以及当前使用的是哪个定义版本，那么问题本身就会变得摇晃。也就是说，当 target 候选有多个，或者标准在变化时，必须先写清楚：哪一个是代表 target，当前定义版本又是什么。

| 先要固定的东西 | 为什么需要 |
| --- | --- |
| 代表 target | 为了明确当前到底先解决哪个问题 |
| target 定义版本 | 为了避免把同名但不同标准的东西混在一起 |
| 需要一起管理的其他 target 候选 | 为了留下同一份数据里有哪些结果候选并存 |

| 常见场景 | 需要留下的备注 |
| --- | --- |
| `review_needed` 和 `final_status` 同时存在 | 先把哪一个当成代表问题 |
| 上个月和这个月的判定标准不同 | 规则变化的时间点和版本 |
| `warning`、`review`、`failure` 同时存在 | 应该把哪一层当作 target |

## 为什么必须先固定代表 target

当多个 target 候选同时存在时，最常见的混淆是：`反正它们都来自同一批事件，之后再挑一个也可以`。但如果不先固定代表 target，那么连“当前到底在解决什么问题”这件事本身都会开始摇晃。

例如，如果把 `review_needed` 当作代表 target，问题就变成`应该优先重新看什么`。相反，如果把 `final_status` 当作代表 target，问题就变成`最终会收敛成什么状态`。即使用的是同一张事件表，这两个问题的目标、评估方式、错误解释也都会变化。所以，没有固定代表 target 的状态，并不只是`数据很多`，而更接近于`问题本身还没有被关成一个问题`。

## 再看一个冲突场景

| event_id | review_needed | final_status | status_type | priority_bucket |
| --- | --- | --- | --- | --- |
| A | 1 | pending | unstable | high |
| B | 1 | normal | recovered | medium |
| C | 0 | normal | stable | low |

看这张表，`A` 和 `B` 虽然都有 `review_needed = 1`，但它们的 `final_status` 和 `status_type` 并不一样。如果当前把 `review_needed` 固定为代表 target，那么 `A` 和 `B` 会被并成同一个结果。反过来，如果把 `final_status` 固定为代表 target，那么 `pending` 与 `normal` 就会变成不同结果。也就是说，同一个事件会因为你把哪一列固定成代表 target，而变成相同答案，也可能变成不同答案。

这个场景说明，`选择代表 target` 并不是事后附加的管理备注。它本身就是在定义当前问题的中心提问，而定义版本则是在固定：你究竟按照什么标准来读取这个提问。

所以，当 target 候选很多时，真正困难的不是`名字冲突`，而是`如果不把代表结果和定义版本一起固定，问题本身就会摇晃`。这里要固定的是`代表结果定义`、`定义版本管理`和`扩展候选管理`这一组，使得同一份数据里即使冒出多个目标候选，中心问题也仍然能被稳定住。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, 确认日 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, versioning and derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
