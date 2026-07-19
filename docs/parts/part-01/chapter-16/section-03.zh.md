# P1-16.3 如何通过项目(project)来验证

> Section ID: `P1-16.3`
> Version: `v2026.07.19`

在 P1-16.2 中，我们已经从工作流角度看过工作自动化与搜索。现在要整理的是：如何通过一个小型 `项目(project)` 来验证学习与实际应用。

人很容易很快产生一种“我已经理解 AI 了”的感觉。但是否真的理解，往往只有在自己做出一个小型可交付物时才会暴露得更清楚。

本节会围绕 `项目(project)`、`成功标准(success criteria)`、`评估(evaluation)`、`记录(record)`、`失败类型(failure type)`，整理如何把前面关于学习文档化与工作自动化的脉络，转成一个 `小而可验证的项目`。

## 本节范围

这里专注讨论：完成 Part 1 之后，怎样设计并验证一个小项目。具体算法实现与大规模服务开发，则留给后续 Part。

| 主题 | 本节要看的问题 |
| --- | --- |
| 项目范围(scope) | 过大的目标应当怎样缩小？ |
| 成功标准(success criteria) | 什么条件算成功？ |
| 评估(evaluation) | 应怎样检查结果是否正确？ |
| 记录(record) | 失败与修改过程应怎样保留下来？ |

## 本节目标

- 说明为什么一个小项目应从一个具体问题出发。
- 说明为什么应先写下成功标准(success criteria)与评估标准。
- 说明为什么失败记录会在项目回顾(retrospection)中变成学习材料。

## 三个基准

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| 小项目应从一个问题开始，而不是从一个技术名词开始 | 这能减少起步时把范围拉得过大的错误。 | 只要理解成“能否在我的文档集合中找到相关 Section？”比“来做一个 RAG”更稳妥即可。 |
| 成功标准应当先写出来 | 这能避免评估只停留在感觉层面。 | 只要理解成在开始前就应定义成功阈值与失败含义即可。 |
| 失败记录会变成学习材料 | 这能防止把项目只看成简单成败。 | 只要理解成重复出现的失败类型应被命名并保存即可。 |

## 小项目应从一个问题开始

好的入门项目，不应从某个技术名词开始，而应从一个问题开始。

> 弱的起点：  
> 我们来做 RAG。
>
> 更好的起点：  
> 这个系统能否在我写的学习文档集合里，找到相关的 Section？

当问题足够具体时，需要的技术构成也会自然收窄。

| 问题 | 可能需要的构件 |
| --- | --- |
| 能否在我的文档中找到相关 Section？ | 嵌入、向量搜索 |
| 能否依据检索结果来回答？ | RAG、来源标示 |
| 能否减少回答错误？ | 评估问题、核对原文 |
| 能否减少重复写作步骤？ | 模板、自动化脚本 |

## 先写下成功标准

项目常见失败原因之一，是从一开始就没有真正定义 `成功标准(success criteria)`。

> 目标：  
> 做一个基于文档的问答系统
>
> 薄弱的成功标准：  
> 它回答得不错
>
> 更好的成功标准：  
> 在 20 个问题中，至少 16 个能附上相关 Section 链接  
> 不产生无依据的武断断言  
> 面对缺失内容时，会明确说不知道

AI 项目的成功标准不应只包含准确率。它还应当把依据性、保密/安全、成本、延迟，以及人能否审查结果一起纳入。

## 失败记录会变成学习材料

AI 项目里，失败并不少见。重要的不是把失败藏起来，而是把它整理成类别。

| 失败类型 | 应记录什么 |
| --- | --- |
| 检索失败(retrieval failure) | 为什么没有找到相关文档 |
| 幻觉(hallucination) | 在哪里编出了不存在的内容 |
| 缺少依据(missing grounding) | 在哪里出现了无来源主张 |
| 权限问题(permission problem) | 在哪里混入了不应访问的资料 |
| 成本问题(cost problem) | 调用次数、token、延迟情况 |

这些失败记录随后会变成下一轮改进的要求(requirement)。

> 先记录失败  
> 对重复失败做分类  
> 调整验证标准  
> 做小修改后再测试

## 检查清单

- 能说明为什么 AI 项目应从中心问题开始，而不是从技术名词开始。
- 能说明为什么成功标准(success criteria)必须先写出来。
- 能把依据性、成本、延迟与安全条件纳入评估(evaluation)。
- 能说明为什么失败记录会变成下一轮需求(requirement)。
- 能把 `中心问题`、`成功标准`、`评估方式`、`失败记录` 分开来说明 AI 项目为何是可验证的学习单位。

## 来源与参考资料

- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-19.
- OWASP, [2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps](https://genai.owasp.org/llm-top-10/){: target="_blank" rel="noopener noreferrer" }, OWASP GenAI Security Project, 确认日期: 2026-07-19.
- U.S. Department of Education, [Artificial Intelligence and the Future of Teaching and Learning](https://www.ed.gov/sites/ed/files/documents/ai-report/ai-report.pdf){: target="_blank" rel="noopener noreferrer" }, 2023, 确认日期: 2026-07-19.
