# P1-10.3 生成结果(output)的质量(quality)与风险(risk)

> Section ID: `P1-10.3`
> Version: `v2026.07.26`

在 10.1 中，我们看了分类(classification)、预测(prediction)、生成(generation)之间的区别。在 10.2 中，我们又看了生成式 AI(generative AI)会基于条件(condition)逐步构造产出物的直觉。

这里要讨论的是：我们应该如何理解和审阅这些生成结果。

这里的核心问题是：如果生成式 AI 的结果看起来自然、流畅、很像真的，那么这个结果就可以直接相信吗？

入门阶段的基准线很明确：

> 自然度只是质量的一部分，  
> 事实性、依据、安全性、版权、隐私、使用场景都需要分开审查。

在 Part 1 中，本节先建立 `质量(quality)`、`依据(evidence)`、`幻觉(hallucination)`、`confabulation`、`安全(safety)`、`权利与责任(rights and responsibility)` 的入门区分。10.1 讨论的是 `输出什么`，10.2 讨论的是 `如何生成`，这里则把第三个问题单独拆开：`应该如何阅读并验证生成结果`。版权、安全、隐私的更详细讨论会在 P1-15 中继续展开。

这里不会覆盖生成式 AI 的所有风险。法律判断、安全架构、隐私保护、版权争议、AI 治理(governance)等内容，会在 P1-15 中更详细讨论。

`质量`、`依据`、`幻觉`、`安全`、`权利与责任` 在开始时都可能听起来像类似的检查项。先用一句很短的话把它们区分开：

| 术语 | 极简含义 | 本节中的作用 |
| --- | --- | --- |
| 质量 | 输出是否符合请求、是否可读 | 最先能看见的评价轴 |
| 依据 | 事实主张是否有可核查来源支持 | 区分自然度与正确性的轴 |
| 幻觉 | 看起来合理但没有依据的错误 | 生成式 AI 的代表性风险 |
| 安全 | 对人和系统造成伤害的可能性 | 结合使用场景来评估的风险 |
| 权利与责任 | 版权、隐私、机密信息、使用责任 | 发布或部署前的审查轴 |

这里至少要保留的区分是：`自然度 != 事实性`、`幻觉是似是而非的错误`、`安全与权利需要另外审查`。

本节作为第 10 章的收束，先建立四个审查视角：

| 视角 | 核心问题 |
| --- | --- |
| 质量(quality) | 结果是否符合请求、易读且有用？ |
| 依据(evidence) | 事实主张是否有可核查来源支持？ |
| 安全(safety) | 输出是否可能对人、组织、社会造成伤害？ |
| 权利与责任(rights and responsibility) | 是否审查了版权、隐私、机密信息与责任问题？ |

## 检查自然生成结果的基准

- 区分生成结果的自然度和事实性。
- 把幻觉(hallucination)或 confabulation 理解为：以看似可信的方式呈现出来、但缺乏依据的事实内容。
- 理解 AI 输出不会自动附带有效来源和依据。
- 从质量、依据、安全、权利四个视角来审视生成结果的风险。
- 说明为什么本书中的 AI 草稿仍然必须经过人工审阅。

## 三个基准

这里并不是要主张禁止或恐惧生成式 AI，而是要整理“应该如何阅读结果”。只要抓住下面三个基准，整体脉络就会清楚。

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| 自然的句子与正确的句子可能不同 | 这能纠正生成式 AI 最常见的误解之一。 | 只要明确知道“写得顺”也可能是错的即可。 |
| 来源与依据不会自动随着输出一起到来 | 这直接连接到整本书的验证原则。 | 只要知道事实主张需要单独核查即可。 |
| 风险不只包括质量，还包括安全、权利与责任 | 这能自然衔接到 P1-15 的伦理、版权与安全章节。 | 只要知道“写得好”并不等于“足够可靠”即可。 |

## 自然的句子与正确的句子不同

生成式 AI 的输出可能看起来非常自然。句子很流畅，表述很像真的，表格和列表也能整理得很整齐。

但自然度(naturalness)并不等于准确性(accuracy)。

> 自然的句子：  
> 容易阅读、看起来合理的句子
>
> 正确的句子：  
> 在事实、范围、条件、依据上都成立的句子

例如下面这句话在形式上可能看起来很自然：

> Transformer 发表于 2012 年，并且是 AlexNet 的直接后续研究。

但这句话在事实关系上是错误的。Transformer 论文发表于 2017 年，而 AlexNet 与其说是 LLM 的直接后续研究，不如更安全地放在深度学习扩散的周边证据中来理解。

使用生成式 AI 时最危险的点就在这里：

> 句子看起来自然  
> -> 因此让人觉得是真的  
> -> 没有核查依据就进入正文

这里必须阻止这个过程。

## 幻觉是似是而非的错误

NIST 的 Generative AI Profile 把 `confabulation` 说明为：以自信方式呈现、但实际上错误或虚假的内容生成，并指出这种现象常被称为 hallucination 或 fabrication。NIST 还把这种现象与生成模型通过近似训练数据的统计分布来生成输出的方式联系起来。

在本书中，韩文正文使用 `환각(hallucination)` 这一表达；理解时也建议同时想起以下相关说法：

- 无依据的生成
- 似是而非的错误
- confabulation

幻觉可能表现为：

| 类型 | 例子 |
| --- | --- |
| 编造不存在的来源 | 生成并不存在的论文、书籍、URL |
| 给出错误年份 | 说错论文发表年份或事件时间 |
| 混合概念 | 把 AlexNet、YOLO、LLM 说成像同一条直接谱系 |
| 过度泛化 | 把部分模型的特点套用到所有生成式 AI |
| 虚假引文 | 把原文里不存在的话当作引文给出 |

幻觉的问题不只是“可能会错”。更大的问题在于：错误内容往往会以流畅、笃定的方式出现，如果没有人工审查，就很容易被放进正文里。

## 缺少依据本身也是质量问题

在这里，我们把 AI 生成的句子视为草稿。草稿可以有用，但事实主张仍然需要依据。

下面两句话表面上看都像在陈述，但质量不同：

> 没有依据的句子：  
> 大多数 AI 研究者认为生成式 AI 复现了人类思考。
>
> 更安全的句子：  
> 生成式 AI 会基于数据中学到的模式生成新内容，  
> 但是否应把这种工作方式理解为对人类思考的复现，还需要另外审查。

尤其是下面这些类型的句子，必须核查来源：

| 句子类型 | 要确认什么 |
| --- | --- |
| 历史说明 | 年份、论文、研究者、上下文 |
| 技术定义 | 官方文档、教材、论文 |
| 产品功能 | 官方文档、发布说明 |
| 法律与政策 | 法规、机构材料、专家审查 |
| 最新动向 | 带日期的新闻、报告、官方公告 |
| 预测 | 是谁、在何时、基于什么依据提出的 |

即使生成式 AI 同时给出了链接，也仍然要重新确认这些链接是否真的支持正文中的主张。`有 URL` 和 `有依据` 不是同一回事。

## 安全风险往往在输出之后才显现

生成式 AI 的风险并不只存在于模型内部。输出会被用在什么地方，会显著改变风险的性质。

NIST 列出的生成式 AI 风险包括 confabulation、data privacy、information integrity、information security、intellectual property。OWASP Top 10 for LLM Applications 2025 也把 prompt injection、sensitive information disclosure、improper output handling、excessive agency 等 LLM 应用层安全风险单独列出。

在入门阶段，可以先这样分开看：

| 风险 | 说明 | 例子 |
| --- | --- | --- |
| 事实性风险 | 把错误内容说得像是真的 | 总结不存在的判例或论文 |
| 信息完整性风险 | 扩散虚假或被操纵的内容 | 假图片、假新闻草稿 |
| 隐私风险 | 敏感信息被输入或输出 | 客户资料、医疗信息、内部文档 |
| 安全风险 | 模型输出与系统动作连接 | prompt injection、不安全的代码执行 |
| 版权风险 | 使用他人表达或数据时产生问题 | 长段复制受保护文本、未经授权的风格模仿 |
| 过度信任风险 | 人在未审查的情况下直接使用结果 | 直接用于医疗、法律、金融判断 |

这里重要的并不是简单得出“AI 很危险”的结论。更准确的视角是：

> 输出的风险是由  
> 模型、  
> 输入数据、  
> 使用目的、  
> 审查流程、  
> 部署环境  
> 共同形成的。

## 新闻报道可以帮助看到真实使用场景

新闻报道不是概念定义的主要标准，但它可以作为辅助案例，帮助展示生成式 AI 的风险如何在真实使用场景中暴露出来。

| 报道中的场景 | 对应风险 | 在 10.3 中应怎样阅读 |
| --- | --- | --- |
| 竞选网站发布 AI 生成的假新闻式文章 | 信息完整性(information integrity)、幻觉(hallucination)、审查缺失 | 看起来像新闻的句子也仍然需要核查来源与事实。 |
| 法院文件引用了不存在的 AI 生成案例 | 事实性风险、高风险领域、责任(accountability) | 在法律、医疗、金融等高影响领域，人工审查是必需的。 |
| 针对欺骗性 AI 生成媒体与深度伪造(deepfake)的法律应对 | 安全(safety)、权利(rights)、公共信任 | 生成结果会影响个人权利、声誉、选举与公共信任。 |

因此，在本节中，新闻报道只作为 `真实案例` 使用。真正的标准仍然放在 NIST、OWASP、版权机构这类更稳定的官方或专业资料上。

## 即使在草稿阶段，也要审查版权与权利问题

即使生成式 AI 产出了新的句子或图像，也不代表权利问题就自动消失。

美国版权局(US Copyright Office) 关于 AI 与版权的报告继续维持这样一种立场：`human authorship` 仍然是版权保护的核心要求。同时，该报告也区分了“完全由 AI 生成的内容”和“包含有人类创造性贡献的 AI 辅助产出物”。

本书是公开发布的韩语文档，也可能涉及韩国出版物与教育资料，因此还需要从韩国版权法的角度另行审查。但这里不会试图给出法律结论，更详细的讨论会放在 P1-15。

10.3 里要记住的标准是：

> 即使句子是 AI 写的，  
> 也不要把事实主张在无来源的情况下当成事实发布。
>
> 即使原文是 AI 总结的，  
> 也不要长段搬运受版权保护的表达。
>
> 即使图像或代码是 AI 生成的，  
> 也要审查许可证、原创性、相似性与使用范围。

## 处理生成结果时的基本审查流程

在学习文档、业务文档、公开文章等需要把生成结果再次用于外部场景的情况下，更安全的做法不是原样相信草稿，而是按照下面的流程处理：

> AI 生成草稿  
> -> 拆分主张  
> -> 核查依据  
> -> 一般化表达  
> -> 检查领域边界  
> -> 人工审阅  
> -> 反映到公开文稿

各步骤的意义如下：

| 步骤 | 要确认什么 |
| --- | --- |
| 拆分主张 | 区分事实主张、解释、工作假设 |
| 核查依据 | 确认真实来源是否支持正文中的主张 |
| 一般化表达 | 把个人直觉连接到标准概念 |
| 检查领域边界 | 不侵入其他 Section 的范围 |
| 人工审阅 | 修正错误内容、危险表达、缺失的依据 |

核心点是一样的。AI 可以很快地产出草稿，但文档的可信度不是来自起草速度，而是来自审查流程。

## 检查清单

- 我可以区分自然的句子与准确的句子。
- 我可以把幻觉(hallucination)或 confabulation 解释成似是而非的错误。
- 我可以说明“有来源链接”并不等于依据审查已经完成。
- 我可以把生成结果的风险分成事实性、信息完整性、隐私、安全、版权、过度信任来理解。
- 我可以说明 AI 草稿在进入公开文档前为什么必须经过人工审查。
- 我可以记住 P1-15 会更详细地讨论版权、安全与隐私。
- 我可以把 `自然度`、`准确性`、`依据`、`使用场景`、`权利与责任` 分开来审查。
- 我可以说明即使把生成式 AI 当作学习工具，草稿也仍然需要更严格的人工审查。

## 来源与参考资料

- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf){: target="_blank" rel="noopener noreferrer" }, NIST AI 600-1, 2024-07, 确认日期: 2026-06-23.
- OWASP GenAI Security Project, [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/){: target="_blank" rel="noopener noreferrer" }, 2024-11-17, 确认日期: 2026-06-23.
- U.S. Copyright Office, [Copyright and Artificial Intelligence, Part 2: Copyrightability](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf){: target="_blank" rel="noopener noreferrer" }, 2025-01, 确认日期: 2026-06-23.
- IBM, [What are AI hallucinations?](https://www.ibm.com/think/topics/ai-hallucinations){: target="_blank" rel="noopener noreferrer" }, IBM Think, 确认日期: 2026-06-23.
- Associated Press, [Philly sheriff's campaign takes down bogus 'news' stories posted to site that were generated by AI](https://apnews.com/article/fake-news-philadelphia-sheriff-website-ai-headlines-7bace99ffe0f11d8e8b17862c7b55e4e){: target="_blank" rel="noopener noreferrer" }, 2024-02-05, 确认日期: 2026-06-23.
- Associated Press, [UK judge warns of risk to justice after lawyers cited fake AI-generated cases in court](https://apnews.com/article/uk-courts-fake-ai-cases-46013a78d78dc869bdfd6b42579411cb){: target="_blank" rel="noopener noreferrer" }, 2025-06-07, 确认日期: 2026-06-23.
- Associated Press, [Creating and sharing deceptive AI-generated media is now a crime in New Jersey](https://apnews.com/article/new-jersey-deepfake-videos-criminal-civil-penalties-276ca23b00b10a7ee7e7303ead8b4260){: target="_blank" rel="noopener noreferrer" }, 2025-04-03, 确认日期: 2026-06-23.
