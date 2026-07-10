# P3-9.11 当 target 候选有多个，或标准在变化时，应该先固定什么

> Section ID: `P3-9.11`
> Version: `v2026.07.10`

在运营数据里，target 候选未必只会出现一个。像 `review_needed`、`final_status`、`failure_type`、`priority_bucket` 这样的多个候选可能会一起出现；即使名字相同的 target，在不同时间里判定标准也可能不同。如果不先固定：哪一个是代表问题，以及当前使用的是哪个定义版本，那么问题本身就会变得摇晃。也就是说，当 target 候选有多个，或者标准在变化时，必须先写清楚：哪一个是代表 target，当前定义版本又是什么。

| 先要固定的东西 | 为什么需要 |
| --- | --- |
| 代表 target | 为了明确当前到底先解决哪个问题 |
| target 定义版本 | 为了避免把同名但不同标准的东西混在一起 |
| 辅助 target 候选 | 为以后比较或扩展留下空间 |

| 常见场景 | 需要留下的备注 |
| --- | --- |
| `review_needed` 和 `final_status` 同时存在 | 先把哪一个当成代表问题 |
| 上个月和这个月的判定标准不同 | 规则变化的时间点和版本 |
| `warning`、`review`、`failure` 同时存在 | 应该把哪一层当作 target |

所以，当 target 候选很多时，真正困难的不是`名字冲突`，而是`如果不把代表结果和定义版本一起固定，问题本身就会摇晃`。这里要固定的是`代表结果定义`、`定义版本管理`和`扩展候选管理`这一组，使得同一份数据里即使冒出多个目标候选，中心问题也仍然能被稳定住。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, 确认日 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, versioning and derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }

