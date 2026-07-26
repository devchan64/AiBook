# 중국어 개념사전 인덱스

이 파일은 중국어 번역어 후보와 중국어판 본문에서 쓰는 용어를 `docs/reference/concept-glossary-terms/`의 단어별 원고으로 연결하는 보조 인덱스다.

정의는 이 파일에 중복 작성하지 않는다. 대표 정의는 단어별 원고 파일과 해당 `중심 Section`을 기준으로 확인한다.

| 索引词 | 代表词条 | 英语基准术语 | 中心 Section | 文件 slug | 锚点 | 验证参考资料 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 行动 | 行动 | action | P1-8.3 | action | action | P1-14.3 source context | 智能体或系统在某个状态下实际选择并执行的操作 |
| 实际目标 | 实际目标 | actual target | P3-9.9 | actual-target | actual-target | P3-9.9 source context | 真正想知道、想减少或想预测的结果 |
| 基准模型 | 基准模型 | baseline model | P4-8.2 | baseline-model | baseline-model | P4-8.2 source context | 候选模型需要超过的最简单比较模型或分数标准 |
| 基准线 | 基准线 | baseline | P3-7.3 | baseline | baseline | BLS base period, NCI baseline context | 让当前数值或模型分数不被孤立解读的参照标准 |
| 基准线区间 | 基准线区间 | baseline window | P7-1.3 | baseline-window | baseline-window | P3-7.1 source context | 作为平常参照来解读最近变化的时间区间或观测区间 |
| 标签一致性 | 标签一致性 | label consistency | P3-9.6 | label-consistency | label-consistency | P3-9.6 source context | 同一事件或相似条件下是否会反复获得相同含义标签的程度 |
| 标签预测 | 标签预测 | label prediction | P3-9.1 | label-prediction | label-prediction | P3-9.1 source context | 用输入案例去预测稳定目标标签的更强问题设定 |
| 可比较的参考群体 | 可比较的参考群体 | comparable reference group | P3-7.4 | comparable-reference-group | comparable-reference-group | P3-7.4 source context | 与当前样本共享样本单位和运行条件、可用于基准线比较的过去案例集合 |
| 可比性 | 可比性 | comparability | P3-2.3 | comparability | comparability | P3-2.3 source context | 能否把值、样本、模型或条件放在同一标准上解释 |
| 比较报告 | 比较报告 | comparison report | P3-9.2 | comparison-report | comparison-report | P3-9.2 source context | 整理近期状态与基准线差异，让人决定先检查什么的输出结构 |
| 比较表 | 比较表 | comparison table | P7-2.1 | comparison-table | comparison-table | P3-7.2 source context | 把两个以上对象放在共同列上以便读取差异的表 |
| 混淆矩阵 | 混淆矩阵 | confusion matrix | P4-6.1 | confusion-matrix | confusion-matrix | P4-6.1 source context | 按真实标签和预测标签组合读取分类错误方向的表 |
| 数据建模 | 数据建模 | data modeling | P3-1.1 | data-modeling | data-modeling | P3-1.1 source context | 把原始记录重新设计成样本、特征、比较和输出结构 |
| 数据质量检查 | 数据质量检查 | data quality check | P3-2.3 | data-quality-check | data-quality-check | P3-2.3 source context | 在比较前检查缺失、重复、顺序错误、单位混用等问题 |
| 数据问题 | 数据问题 | data question | P3-1.3 | data-question | data-question | P3-1.3 source context | 固定案例单位、比较对象和想知道结果的问题设计句 |
| 数据科学 | 数据科学 | data science | P3-1.1 | data-science | data-science | P3-1.1 source context | 收集、清理、表示、建模和解释数据的宽泛流程 |
| 数据泄漏 | 数据泄漏 | data leakage | P2-12.3 | data-leakage | data-leakage | P2-12.3 source context | 预测时本不该知道的信息进入训练或评估的问题 |
| 过拟合 | 过拟合 | overfitting | P4-5.1 | overfitting | overfitting | P4-5.1 source context | 训练数据表现很好但新数据表现变差的状态 |
| 错误成本 | 错误成本 | error cost | P3-9.12 | error-cost | error-cost | Google ML Glossary thresholding, P3-9.12 source context | 按错误类型分别记录真实负担，用来解释阈值和判断方向的标准 |
| 交叉验证 | 交叉验证 | cross-validation | P4-4.2 | cross-validation | cross-validation | scikit-learn Cross-validation, P4-4.2 source context | 在已有数据中多次拆分，并在不同验证部分上反复评估模型或设置的方法 |
| 假阴性 | 假阴性 | false negative | P3-9.12 | false-negative | false-negative | Google ML Glossary false negative, P3-9.12 source context | 实际为正例，却被模型或规则判成负例而漏掉的案例 |
| 假阳性 | 假阳性 | false positive | P3-9.12 | false-positive | false-positive | Google ML Glossary false positive, P3-9.12 source context | 实际为负例，却被模型或规则判成正例而误报的案例 |
| 精确率 | 精确率 | precision | P1-13.4 | precision | precision | P4-6.1 source context | 被模型预测为正类的案例中实际为正类的比例 |
| 列角色分离 | 列角色分离 | column-role separation | P3-6.4 | column-role-separation | column-role-separation | P3-6.4 source context | 在决定模型输入前，先按角色区分工作表里的列 |
| 数据集候选 | 数据集候选 | dataset candidate | P3-2.1 | dataset-candidate | dataset-candidate | P3-2.1 source context | 针对一个问题重新组合样本和列的临时表结构 |
| 随机森林 | 随机森林 | random forest | P4-15.1 | random-forest | random-forest | P4-15.1 source context | 把多棵决策树组合起来进行预测的集成模型 |
| 代表目标 | 代表目标 | representative target | P3-9.11 | representative-target | representative-target | P3-9.11 source context | 多个目标标签候选中被固定为当前中心结果的目标 |
| 代理目标 | 代理目标 | proxy target | P3-9.9 | proxy-target | proxy-target | Google ML Glossary proxy labels, P3-9.9 source context | 实际目标不可用或出现太晚时临时当作目标的替代列 |
| 标签确认延迟 | 标签确认延迟 | delayed label confirmation | P3-9.10 | delayed-label-confirmation | delayed-label-confirmation | Google ML Glossary label, P3-9.10 source context | 真实结果还没有闭合成答案标签的时间延迟状态 |
| 观察未完成的负例 | 观察未完成的负例 | incomplete negative | P3-9.10 | incomplete-negative | incomplete-negative | Label selection follow-up context, P3-9.10 source context | 因必要追踪期尚未结束而不能当成已闭合 0 的案例 |
| 证据强度 | 证据强度 | evidence strength | P3-8.1 | evidence-strength | evidence-strength | P3-8.1 source context | 判断差异或信号可以用多大表达强度来说时所依据的稳固程度 |
| 折叠规则 | 折叠规则 | folding rule | P3-5.7 | folding-rule | folding-rule | P3-5.7 source context | 把多个后续事件缩减成一个代表结果列的明确规则 |
| 特征定义身份 | 特征定义身份 | feature-definition identity | P3-6.6 | feature-definition-identity | feature-definition-identity | P3-6.6 source context | 判断同名特征是否共享同一单位、规则、版本和运行定义 |
| 格式一致性 | 格式一致性 | format consistency | P3-2.3 | format-consistency | format-consistency | P3-2.3 source context | 同一含义的值是否使用稳定格式、单位和记法规则 |
| 规则型方法 | 规则型方法 | rule-based approach | P1-2.1 | rule-based-approach | rule-based-approach | P1-2.1 source context | 由人明确写出判断规则后再应用的解决问题方式 |
| 分组切分 | 分组切分 | group split | P3-9.13 | group-split | group-split | scikit-learn grouped cross-validation, P3-9.13 source context | 避免同一实体或同一组记录同时出现在训练侧和验证/测试侧的切分方式 |
| 监督学习 | 监督学习 | supervised learning | P1-8.1 | supervised-learning | supervised-learning | P1-8.1 source context | 用带有输入和正确标签的样本学习目标输出的机器学习问题 |
| 奖励 | 奖励 | reward | P1-8.3 | reward | reward | P1-8.3 source context | 强化学习中行动之后由环境返回的反馈信号 |
| 输入窗口 | 输入窗口 | input window | P3-5.4 | input-window | input-window | P3-5.4 source context | 从源时间序列中切出并作为一条学习输入处理的时间区间 |
| 输入说明 | 输入说明 | input specification | P3-6.3 | input-specification | input-specification | P3-6.3 source context | 说明交给模型或后续学习阶段的输入单位、列、顺序和结构 |
| 学习型方法 | 学习型方法 | learning-based approach | P4-1.2 | learning-based-approach | learning-based-approach | P4-1.2 source context | 从案例数据中拟合输入和输出关系来形成模型判断标准的方法 |
| 干预反馈 | 干预反馈 | intervention feedback | P3-8.7 | intervention-feedback | intervention-feedback | P3-8.7 source context | 复核规则或运营处置改变后续数据和标签的反馈结构 |
| 解释边界 | 解释边界 | interpretation boundary | P3-8.2 | interpretation-boundary | interpretation-boundary | P3-1.2 source context | 数据结果或比较结论能够说到哪里的边界 |
| 告警 | 告警 | alert | P3-9.1 | alert | alert | P3-9.1 source context | 相对于基准线或平常状态看到了变化，提醒先检查的轻量信号 |
| 候选分布 | 候选分布 | candidate distribution | P6-1.3 | candidate-distribution | candidate-distribution | P6-1.3 source context | 当前上下文中下一候选的相对自然程度分布 |
| 缺失值 | 缺失值 | missing value | P3-5.5 | missing-value | missing-value | P3-5.5 source context | 本应有观测值的位置为空，可能需要填补、标记或撤回样本 |
| 输出产出物 | 输出产出物 | output artifact | P1-10.1 | output-artifact | output-artifact | P1-10.1 source context | 生成式 AI 制造、需要人检查和再利用的结果对象 |
| 输出结构 | 输出结构 | output structure | P3-2.2 | output-structure | output-structure | P3-1.1 source context | 比较报告、复核队列或目标候选等结果框架 |
| 策略 | 策略 | policy | P1-8.3 | policy | policy | P1-14.3 source context | 在当前状态或观测下决定选择哪个行动的标准或函数 |
| 策略规则 | 策略规则 | policy rule | P3-9.8 | policy-rule | policy-rule | P3-9.8 source context | 把模型分数或类别输出转换成实际运营行动的规则 |
| 预测契约 | 预测契约 | prediction contract | P3-9.7 | prediction-contract | prediction-contract | P3-9.7 source context | 同时关闭输入定义、结果定义、时点可用性和可复现性的预测问题约定 |
| 概率估计 | 概率估计 | probability estimate | P1-7.3 | probability-estimate | probability-estimate | P1-7.3 source context | 需要单独判断是否校准、是否能按概率解释的模型数值输出 |
| 问题表示结构 | 问题表示结构 | problem-representation structure | P3-2.1 | problem-representation-structure | problem-representation-structure | P3-2.1 source context | 把存储记录重新表示为样本、派生列、比较标准和输出形式 |
| 无监督学习 | 无监督学习 | unsupervised learning | P1-8.2 | unsupervised-learning | unsupervised-learning | P1-8.2 source context | 在没有人工标签的数据中寻找结构、相似性或表示的机器学习问题 |
| 表示学习 | 表示学习 | representation learning | P1-3.3 | representation-learning | representation-learning | representation learning review | 模型从数据中学习对任务有用的内部表示 |
| 强化学习 | 强化学习 | reinforcement learning | P1-8.3 | reinforcement-learning | reinforcement-learning | P1-8.3 source context | 通过状态、行动和奖励调整策略的机器学习问题 |
| 欠拟合 | 欠拟合 | underfitting | P4-5.1 | underfitting | underfitting | P4-5.1 source context | 模型连训练数据中的基本规律也没有充分学到的状态 |
| 复核候选 | 复核候选 | review candidate | P3-9.1 | review-candidate | review-candidate | P3-9.1 source context | 基于变化信号和判断语境，值得人工重新确认的案例 |
| 复核候选队列 | 复核候选队列 | review queue | P3-9.3 | review-queue | review-queue | P3-1.3 source context | 按优先级排列人工复核候选案例的运营输出 |
| 分数 | 分数 | score | P1-5.2 | score | score | P1-5.2 source context | 用于比较、排序或阈值判断的模型数值输出 |
| 算法 | 算法 | algorithm | P4-3.1 | algorithm | algorithm | AIMA, P4-3.1 source context | 为解决问题而按顺序执行的一套明确步骤 |
| 排序 | 排序 | ranking | P1-13.2 | ranking | ranking | P1-13.2 source context | 按分数或优先级排列多个候选的任务类型 |
| 召回率 | 召回率 | recall | P1-13.4 | recall | recall | P4-6.1 source context | 实际正类中被模型成功找出的比例 |
| 评估设计 | 评估设计 | evaluation design | P3-9.13 | evaluation-design | evaluation-design | P3-9.13 source context | 为问题结构选择数据切分、指标和比较条件的设计 |
| 评估数据 | 评估数据 | evaluation data | P4-4.1 | evaluation-data | evaluation-data | P4-4.1 source context | 没有直接用于模型训练，而是专门留下来检查已训练模型表现的数据 |
| 回归 | 回归 | regression | P1-8.1 | regression | regression | P1-8.1 source context | 根据输入预测连续数值或分数的建模任务 |
| 输出格式 | 输出格式 | output format | P1-12.1 | output-format | output-format | OpenAI prompt engineering | 规定结果以表格、列表、JSON 或段落等形状返回的条件 |
| 提示词 | 提示词 | prompt | P1-12.1 | prompt | prompt | OpenAI prompt engineering, GPT-3 paper | 设置当前回答条件的完整输入 |
| 时间顺序切分 | 时间顺序切分 | time split | P3-9.13 | time-split | time-split | FPP3 time series cross-validation, P3-9.13 source context | 在时间顺序数据中只用较早信息评价较晚案例的切分方式 |
| 样本偏差 | 样本偏差 | sampling bias | P2-5.3 | sampling-bias | sampling-bias | P2-5.3 source context | 观测样本不能很好代表总体并向某个方向倾斜的状态 |
| 选择性标签 | 选择性标签 | selective labels | P3-8.6 | selective-labels | selective-labels | KDD 2017 selective labels problem | 只在经过既有复核或决策路径的部分案例上留下的结果标签 |
| 验证数据 | 验证数据 | validation data | P2-6.2 | validation-data | validation-data | P2-6.2 source context | 在模型开发过程中用来检查和调整模型设置的数据 |
| 跨异质尺度的角色感知阅读 | 跨异质尺度的角色感知阅读 | role-aware reading across heterogeneous scales | P3-6.5 | role-aware-reading-across-heterogeneous-scales | role-aware-reading-across-heterogeneous-scales | P3-6.5 source context | 按角色和相对基准线变化读取不同尺度的数值列 |
| 原始数据 | 原始数据 | source data | P3-1.1 | source-data | source-data | P3-1.1 source context | 重新设计为分析或学习问题之前的起始记录 |
| 源事件 | 源事件 | source event | P3-5.6 | source-event | source-event | P3-5.6 source context | 被切成输入窗口或汇总行之前实际发生的原始事件单位 |
| 参考维护策略 | 参考维护策略 | reference maintenance strategy | P3-7.5 | reference-maintenance-strategy | reference-maintenance-strategy | P3-7.5 source context | 决定基准线或参考区间要固定还是随最近平时区间更新的运行选择 |
| 存储结构 | 存储结构 | storage structure | P3-2.1 | storage-structure | storage-structure | P3-2.1 source context | 为保存记录并保持可追踪而设计的数据结构 |
| 状态 | 状态 | state | P1-7.1 | state | state | P1-14.3 source context | 选择下一步行动时使用的当前信息和条件 |
| 目标 | 目标 | target | P1-8.1 | target | target | P2-12.3 source context | 模型需要预测的答案列或目标值 |
| 目标标签候选 | 目标标签候选 | target candidate | P3-9.3 | target-candidate | target-candidate | P3-1.2 source context | 以后可能成为模型目标的临时结果列 |
| 目标定义版本 | 目标定义版本 | target definition version | P3-9.11 | target-definition-version | target-definition-version | W3C PROV versioning context, P3-9.11 source context | 记录目标定义所采用标准和时间段的版本信息 |
| token | token | token | P6-2.1 | token | token | P6-2.1 source context | 模型处理文本时切分出来的基本计算单位 |
| token ID | token ID | token ID | P6-2.2 | token-id | token-id | P6-2.2 source context | token 片段在模型 vocabulary 中对应的编号 |
| token 化 | token 化 | tokenization | P6-2.2 | tokenization | tokenization | P3-6.2 source context | 把原始文本或区段结构转换成 token 序列 |
| 词汇表 | 词汇表 | vocabulary | P6-2.2 | vocabulary | vocabulary | P6-2.2 source context | tokenizer 可生成的 token 片段和 ID 的内部列表 |
| BPE | BPE | Byte Pair Encoding | P6-2.2 | bpe-byte-pair-encoding | bpe-byte-pair-encoding | P6-2.2 source context | 通过合并高频片段构建 subword vocabulary 的 tokenizer 系列 |
| WordPiece | WordPiece | WordPiece | P6-2.2 | wordpiece | wordpiece | P6-2.2 source context | 按 vocabulary 效率选择 subword 片段的 tokenizer 系列 |
| SentencePiece | SentencePiece | SentencePiece | P6-2.5 | sentencepiece | sentencepiece | P6-2.5 source context | 从包含空白的字符串中处理 subword 片段的 tokenizer 系列 |
| 词表外 | 词表外 | out-of-vocabulary, OOV | P7-4.2 | out-of-vocabulary-oov | out-of-vocabulary-oov | P7-4.2 source context | 落在当前 vocabulary 或 tokenization 规则之外的词或 token |
| token 覆盖率 | token 覆盖率 | token coverage | P7-4.2 | token-coverage | token-coverage | P7-4.2 source context | 输入 token 中能按当前 vocabulary 或 tokenizer 规则实际读取的比例 |
| 文本块 | 文本块 | chunk | P1-13.1 | chunk | chunk | P1-13.1 source context | 为搜索或检索从长文档中切出的较小文本单位 |
| 距离 | 距离 | distance | P2-3.4 | distance | distance | P2-3.4 source context | 衡量两个向量在表示空间中相隔多远的数值标准 |
| 相似度检索 | 相似度检索 | similarity search | P1-13.2 | similarity-search | similarity-search | information retrieval context | 寻找与问题或文档向量接近的候选 |
| top-k | top-k | top-k | P1-13.2 | top-k | top-k | vector retrieval context | 按接近程度取回前 k 个候选 |
| 变量变换 | 变量变换 | variable transformation | P3-6.1 | variable-transformation | variable-transformation | P3-6.1 source context | 把同一结构或数值转换成更容易比较的表达 |
| 向量 | 向量 | vector | P2-3.1 | vector | vector | P2-3.1 source context | 把有顺序的多个数值作为一个整体来表示的结构 |
| 向量数据库 | 向量数据库 | vector database | P6-12.1 | vector-database | vector-database | vector database context | 管理向量存储、索引、metadata、过滤和更新的系统 |
| 向量化 | 向量化 | vectorization | P2-11.3 | vectorization | vectorization | P2-11.3 source context | 把重复计算表达成数组级运算 |
| word2vec | word2vec | word2vec | P1-11.1 | word2vec | word2vec | Mikolov et al. 2013, P1-11.1 source context | 根据邻近词上下文学习词嵌入的方法系列 |
| 优化 | 优化 | optimization | P2-6.1 | optimization | optimization | P2-6.1 source context | 在目标和约束下从多个候选中寻找更好值或设置 |
| 工作假设 | 工作假设 | working hypothesis | P1-16.1 | working-hypothesis | working-hypothesis | P1-16.1 source context | 为开始解释或实验而暂时采用、后续必须验证的假设性说法 |
| 对比学习 | 对比学习 | contrastive learning | P6-3.3 | contrastive-learning | contrastive-learning | SimCLR, SBERT context | 通过应该靠近和应该远离的成对项目学习表达空间排列 |
| 正样本对 | 正样本对 | positive pair | P6-3.3 | positive-pair | positive-pair | contrastive learning context | 表示学习中应该彼此靠近的输入对 |
| 负样本对 | 负样本对 | negative pair | P6-3.3 | negative-pair | negative-pair | contrastive learning context | 表示学习中应该彼此远离的输入对 |
| GloVe | GloVe | GloVe | P6-3.3 | glove | glove | Pennington et al. 2014 | 根据全局词-词共现统计学习词向量的方法 |
| 句子、段落和文档嵌入 | 句子、段落和文档嵌入 | sentence, paragraph, and document embedding | P1-13.1 | sentence-paragraph-and-document-embedding | sentence-paragraph-and-document-embedding | P1-13.1 source context | 把较长文本单位转换成可比较向量表达 |
| 最近邻 | 最近邻 | nearest neighbor | P1-13.2 | nearest-neighbor | nearest-neighbor | P1-13.2 source context | 在距离或相似度规则下最接近查询向量的候选 |
| 全量比较 | 全量比较 | full scan | P6-3.4 | full-scan | full-scan | P6-3.4 source context | 不跳过候选、逐一比较所有候选向量的搜索方式 |
| HNSW | HNSW | hierarchical navigable small world | P1-13.4 | hnsw-hierarchical-navigable-small-world | hnsw-hierarchical-navigable-small-world | HNSW paper | 基于图的 ANN 向量搜索索引方法 |
| 检索增强生成 | 检索增强生成 | retrieval-augmented generation, RAG | P1-13.3 | retrieval-augmented-generation-rag | retrieval-augmented-generation-rag | RAG paper | 先检索外部依据并接到模型输入中再生成回答的结构 |
| 长上下文 | 长上下文 | long-context | P6-4.5 | long-context | long-context | long-context design context | 在长输入中保留并使用重要信息的设计问题 |
| 上下文窗口 | 上下文窗口 | context window | P6-4.2 | context-window | context-window | P6-4.2 source context | 模型在一次输入输出计算中能够同时参考的最大 token 范围 |
| KV 缓存 | KV 缓存 | KV cache | P6-4.4 | kv-cache | kv-cache | long-context generation context | 复用先前 token 已经计算出的 key/value 表示 |
| 采样 | 采样 | sampling | P5-15.3 | sampling | sampling | P5-15.3 source context | 根据候选分布选择一个实际输出片段的步骤 |
| Transformer | Transformer | Transformer | P1-11.3 | transformer | transformer | Attention Is All You Need | 以 attention 为中心比较序列位置关系的神经网络结构系列 |
| 前馈网络 | 前馈网络 | feed-forward network | P5-14.6 | feed-forward-network | feed-forward-network | Transformer block context | attention 之后按位置重新加工表示的小网络 |
| 多头注意力 | 多头注意力 | multi-head attention | P5-13.3 | multi-head-attention | multi-head-attention | Transformer context | 用多个 attention head 读取 token 关系后再合并结果的结构 |
| query-key-value, QKV | query-key-value, QKV | query-key-value, QKV | P5-13.3 | query-key-value-qkv | query-key-value-qkv | attention context | attention 中区分查询、匹配条件和传递内容的三个角色 |
| 位置编码 | 位置编码 | positional encoding | P1-11.3 | positional-encoding | positional-encoding | Transformer context | 在 token 含义向量之外单独供应的序列位置信息 |
| self-attention | self-attention | self-attention | P5-13.2 | self-attention | self-attention | Transformer context | 同一序列中每个 token 根据其他 token 更新自己表示的 attention 机制 |
| 下一 token 预测 | 下一 token 预测 | next-token prediction | P1-10.2 | next-token-prediction | next-token-prediction | LLM generation context | 根据当前上下文计算下一个 token 候选并逐 token 继续生成 |
| softmax | softmax | softmax | P2-2.4 | softmax | softmax | P2-2.4 source context | 把多个 score 归一化为总和为 1 的可比较值的函数 |
| 稀疏注意力 | 稀疏注意力 | sparse attention | P6-4.5 | sparse-attention | sparse-attention | long-context attention context | 只保留部分连接而不是密集比较所有 token 对的 attention 设计 |
