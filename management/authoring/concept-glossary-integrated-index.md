# 개념사전 다국어 통합 관리 인덱스

작성일: 2026-07-29

## 목적

이 문서는 `docs/reference/concept-glossary-terms/`의 단어별 개념사전 원고를 영어 기준 slug로 묶어 한국어, 영어, 중국어 간 대응 상태를 한 파일에서 관리하기 위한 내부 인덱스다. 공개 본문이 아니라 관리 문서이며, 각 언어 공개 색인의 본문을 대체하지 않는다.

## 관리 기준

- 기준 디렉터리: `docs/reference/concept-glossary-terms/`
- 기준 단위: 영어 기준 slug
- 관리 언어: 한국어(`ko`), 영어(`en`), 중국어 간체(`zh`)
- 한국어 단어 파일이 있는 slug를 개념사전 등재 기준으로 본다.
- 같은 slug의 한국어 단어 파일이 없으면 영어·중국어 파일은 독립 표제로 유지하지 않고 삭제 또는 한국어 기준 표제 생성 여부를 재검토한다.
- 언어별 제목은 각 단어 파일의 첫 Markdown 제목에서 가져온다.
- 이 파일은 통합 현황과 누락 상태를 보기 위한 관리 인덱스다. 항목 정의, 관련 개념, 중심 Section, 등장 Section은 각 단어별 원고에서 관리한다.

## 현황 요약

- 전체 slug 수: 329
- 한국어 파일: 329개
- 영어 파일: 329개
- 중국어 파일: 329개
- 3개 언어 모두 있는 slug: 329개
- 한국어만 있는 slug: 0개
- 한국어 기준으로 영어 누락: 0개
- 한국어 기준으로 중국어 누락: 0개
- 한국어 파일 없이 영어·중국어만 있는 slug: 0개

## 우선 점검 큐

### 한국어 파일 없이 남은 slug

- 없음

### 한국어 기준 영어 번역 누락

- 없음

### 한국어 기준 중국어 번역 누락

- 없음

## 통합 표

| slug | 한국어 제목 | 영어 제목 | 중국어 제목 | 상태 |
| --- | --- | --- | --- | --- |
| `accountability` | AI 책임성(accountability) | accountability | 问责 | 완비 |
| `accuracy` | 정확도(accuracy) | accuracy | 准确率 | 완비 |
| `action` | 에이전트 행동(action) | action | 行动 | 완비 |
| `activation-function` | 활성화 함수(activation function) | activation function | 激活函数 | 완비 |
| `actual-target` | 실제 목표(actual target) | actual target | 实际目标 | 완비 |
| `ai-agent` | AI 에이전트(AI agent) | AI agent | AI 智能体 | 완비 |
| `ai-alignment` | AI 정렬(AI alignment) | AI alignment | AI 对齐 | 완비 |
| `ai-artificial-intelligence` | AI(인공지능, artificial intelligence) | AI, artificial intelligence | AI，人工智能 | 완비 |
| `ai-ethics` | AI 윤리(AI ethics) | AI ethics | AI 伦理(AI ethics) | 완비 |
| `ai-risk` | AI 위험(AI risk) | AI risk | AI 风险(AI risk) | 완비 |
| `algorithm` | 알고리즘(algorithm) | algorithm | 算法(algorithm) | 완비 |
| `ann-approximate-nearest-neighbor` | 근사 최근접 이웃(ANN, approximate nearest neighbor) | ANN, approximate nearest neighbor | ANN，近似最近邻 | 완비 |
| `attention` | 어텐션(Attention) | Attention | 注意力 | 완비 |
| `attribution` | 출처 표시(attribution) | attribution | 出处标示(attribution) | 완비 |
| `automatic-differentiation` | 자동미분(automatic differentiation) | automatic differentiation | 自动微分(automatic differentiation) | 완비 |
| `autoregressive-model` | 자기회귀 모델(autoregressive model) | autoregressive model | 自回归模型(autoregressive model) | 완비 |
| `backpropagation` | 역전파(backpropagation) | backpropagation | 反向传播 | 완비 |
| `baseline` | 기준선(baseline) | baseline | 基准线 | 완비 |
| `baseline-model` | 기준 모델(baseline model) | baseline model | 基准模型 | 완비 |
| `bayes-rule` | 베이즈 규칙(Bayes' rule) | Bayes' rule | 贝叶斯规则(Bayes rule) | 완비 |
| `bias` | 편향(bias) | bias | 偏见 | 완비 |
| `bootstrap` | 부트스트랩(bootstrap) | bootstrap | bootstrap | 완비 |
| `broadcasting` | 브로드캐스팅(broadcasting) | broadcasting | 广播 | 완비 |
| `causal-inference` | 인과 추론(causal inference) | causal inference | 因果推断 | 완비 |
| `centroid` | 중심점(centroid) | centroid | 中心点 | 완비 |
| `chain-rule` | 연쇄 법칙(chain rule) | chain rule | 链式法则(chain rule) | 완비 |
| `chunk` | 청크(chunk) | chunk | 文本块(chunk) | 완비 |
| `classification` | 분류(classification) | classification | 分类 | 완비 |
| `cluster` | 군집(cluster) | cluster | 聚类簇 | 완비 |
| `clustering` | 군집화(clustering, 클러스터링) | clustering | 聚类 | 완비 |
| `cnn-convolutional-neural-network` | 합성곱 신경망(CNN, convolutional neural network) | CNN, convolutional neural network | CNN，卷积神经网络 | 완비 |
| `comparability` | 비교 가능성(comparability) | comparability | 可比性(comparability) | 완비 |
| `composite-function` | 합성함수(composite function) | composite function | 复合函数(composite function) | 완비 |
| `computation-graph` | 계산 그래프(computation graph) | computation graph | 计算图 | 완비 |
| `computational-limit` | 계산 한계(computational limit) | computational limit | 计算限制 | 완비 |
| `confabulation` | 작화(confabulation) | confabulation | 虚构性生成 | 완비 |
| `confidence-interval` | 신뢰구간(confidence interval) | confidence interval | 置信区间(confidence interval) | 완비 |
| `confidential-information` | 비밀 정보(confidential information) | confidential information | 机密信息 | 완비 |
| `confusion-matrix` | 혼동 행렬(confusion matrix) | confusion matrix | 混淆矩阵 | 완비 |
| `context-dependency` | 문맥 의존성(context dependency) | context dependency | 语境依赖(context dependency) | 완비 |
| `context-window` | 문맥 창(context window) | context window | 上下文窗口 | 완비 |
| `contextual-representation` | 문맥적 표현(contextual representation) | contextual representation | 上下文表示 | 완비 |
| `contrastive-learning` | 대조 학습(contrastive learning) | contrastive learning | 对比学习 | 완비 |
| `convergence` | 수렴(convergence) | convergence | 收敛 | 완비 |
| `conversational-llm` | 대화형 LLM(conversational LLM) | conversational LLM | 对话式 LLM | 완비 |
| `convolution` | 합성곱(convolution) | convolution | 卷积 | 완비 |
| `copyright` | 저작권(copyright) | copyright | 版权 | 완비 |
| `corpus` | 말뭉치(corpus) | corpus | 语料库 | 완비 |
| `correlation-coefficient` | 상관계수(correlation coefficient) | correlation coefficient | 相关系数(correlation coefficient) | 완비 |
| `cosine-similarity` | 코사인 유사도(cosine similarity) | cosine similarity | 余弦相似度 | 완비 |
| `covariance` | 공분산(covariance) | covariance | 协方差(covariance) | 완비 |
| `credential` | 인증 정보(credential) | credential | 凭据 | 완비 |
| `cross-entropy` | 교차 엔트로피(cross-entropy) | cross-entropy | 交叉熵(cross-entropy) | 완비 |
| `cross-validation` | 교차검증(cross-validation) | cross-validation | 交叉验证(cross-validation) | 완비 |
| `data` | 데이터(data) | data | 数据 | 완비 |
| `data-distribution` | 데이터 분포(data distribution) | data distribution | 数据分布(data distribution) | 완비 |
| `data-leakage` | 데이터 누수(data leakage) | data leakage | 数据泄漏 | 완비 |
| `data-modeling` | 데이터 모델링(data modeling) | data modeling | 数据建模 | 완비 |
| `data-science` | 데이터과학(data science) | data science | 数据科学 | 완비 |
| `data-structure` | 자료구조 선택(data structure) | data structure | 数据结构 | 완비 |
| `dataset` | 데이터셋(dataset) | dataset | 数据集 | 완비 |
| `dbscan` | DBSCAN | DBSCAN | DBSCAN | 완비 |
| `decision` | 업무 의사결정(decision) | business decision | 业务决策(decision) | 완비 |
| `decision-boundary` | 결정 경계(decision boundary) | decision boundary | 决策边界(decision boundary) | 완비 |
| `decision-tree` | 결정트리(decision tree) | decision tree | 决策树 | 완비 |
| `decoder` | 디코더(decoder) | decoder | 解码器 | 완비 |
| `deep-learning` | 딥러닝(deep learning) | deep learning | 深度学习 | 완비 |
| `deep-reinforcement-learning` | 딥 강화학습(deep reinforcement learning) | deep reinforcement learning | 深度强化学习(deep reinforcement learning) | 완비 |
| `delayed-reward` | 지연 보상(delayed reward) | delayed reward | 延迟奖励(delayed reward) | 완비 |
| `dense-vector` | 조밀한 벡터(dense vector) | dense vector | 稠密向量(dense vector) | 완비 |
| `density` | 밀도(density) | density | 密度 | 완비 |
| `derivative` | 미분(derivative) | derivative | 导数 | 완비 |
| `determinism` | 결정성(determinism) | determinism | 确定性(determinism) | 완비 |
| `diffusion-model` | 디퓨전 모델(diffusion model) | diffusion model | 扩散模型 | 완비 |
| `dimension` | 차원(dimension) | dimension | 维度 | 완비 |
| `dimensionality-reduction` | 차원 축소(dimensionality reduction) | dimensionality reduction | 降维 | 완비 |
| `distance` | 거리(distance) | distance | 距离 | 완비 |
| `distributed-representation` | 분산 표현(distributed representation) | distributed representation | 分布式表示 | 완비 |
| `distribution` | 분포(distribution) | distribution | 分布 | 완비 |
| `embedding` | 임베딩(embedding) | embedding | 嵌入 | 완비 |
| `encoder` | 인코더(encoder) | encoder | 编码器 | 완비 |
| `encoder-decoder` | 인코더-디코더(Encoder-Decoder) | Encoder-Decoder | 编码器-解码器 | 완비 |
| `end-to-end-learning` | 엔드투엔드 학습(end-to-end learning) | end-to-end learning | 端到端学习(end-to-end learning) | 완비 |
| `ensemble` | 앙상블(ensemble) | ensemble | 集成(ensemble) | 완비 |
| `error` | 오차(error) | error | 误差 | 완비 |
| `error-accumulation` | 오류 누적(error accumulation) | error accumulation | 错误累积(error accumulation) | 완비 |
| `error-cost` | 오류 비용(error cost) | error cost | 错误成本 | 완비 |
| `estimation` | 추정(estimation) | estimation | 估计 | 완비 |
| `evaluation-data` | 평가 데이터(evaluation data) | evaluation data | 评估数据(evaluation data) | 완비 |
| `evaluation-design` | 모델 평가 설계(evaluation design) | model evaluation design | 模型评估设计(evaluation design) | 완비 |
| `event` | 확률 사건(event) | probability event | 概率事件(event) | 완비 |
| `excessive-agency` | 과도한 권한(excessive agency) | excessive agency | 过度代理性 | 완비 |
| `expert-system` | 전문가 시스템(expert system) | expert system | 专家系统 | 완비 |
| `exploitation` | 활용(exploitation) | exploitation | 利用 | 완비 |
| `exploration` | 탐험(exploration) | exploration | 探索 | 완비 |
| `exponential-function` | 지수 함수(exponential function) | exponential function | 指数函数(exponential function) | 완비 |
| `factual-claim` | 사실 주장(factual claim) | factual claim | 事实性主张 | 완비 |
| `factuality` | 사실성(factuality) | factuality | 事实性 | 완비 |
| `fair-use` | 공정 이용(fair use) | fair use | 合理使用(fair use) | 완비 |
| `false-negative` | 거짓 음성(false negative) | false negative | 假阴性 | 완비 |
| `false-positive` | 거짓 양성(false positive) | false positive | 假阳性 | 완비 |
| `feature` | 특징(feature) | feature | 特征 | 완비 |
| `feature-selection` | 특징 선택(feature selection) | feature selection | 特征选择 | 완비 |
| `fine-tuning` | 미세조정(fine-tuning) | fine-tuning | 微调 | 완비 |
| `function` | 함수(function) | function | 函数 | 완비 |
| `function-approximation` | 함수 근사(function approximation) | function approximation | 函数近似(function approximation) | 완비 |
| `generalization` | 일반화(generalization) | generalization | 泛化 | 완비 |
| `generation` | 생성(generation) | generation | 生成 | 완비 |
| `generative-ai` | 생성형 AI(generative AI) | generative AI | 生成式 AI | 완비 |
| `generative-model` | 생성 모델(generative model) | generative model | 生成模型 | 완비 |
| `gpt` | GPT | GPT | GPT | 완비 |
| `gradient` | 그래디언트(gradient) | gradient | 梯度 | 완비 |
| `gradient-descent` | 경사하강법(gradient descent) | gradient descent | 梯度下降 | 완비 |
| `group-split` | 그룹 분할(group split) | group split | 分组切分(group split) | 완비 |
| `guardrail` | AI 가드레일(guardrail) | AI guardrail | AI 护栏(guardrail) | 완비 |
| `hallucination` | 환각(hallucination) | hallucination | 幻觉 | 완비 |
| `heuristic` | 휴리스틱(heuristic) | heuristic | 启发式 | 완비 |
| `hidden-state` | 숨은 상태(hidden state) | hidden state | 隐藏状态 | 완비 |
| `human-oversight` | 인간 감독(human oversight) | human oversight | 人工监督 | 완비 |
| `hyperparameter` | 하이퍼파라미터(hyperparameter) | hyperparameter | 超参数 | 완비 |
| `hypothesis-testing` | 가설검정(hypothesis testing) | hypothesis testing | 假设检验(hypothesis testing) | 완비 |
| `image-recognition` | 이미지 인식(image recognition) | image recognition | 图像识别 | 완비 |
| `in-context-learning` | 문맥 내 학습(in-context learning) | in-context learning | 上下文内学习 | 완비 |
| `incomplete-information` | 불완전한 정보(incomplete information) | incomplete information | 不完整信息 | 완비 |
| `inference` | 추론(inference) | inference | 推断 | 완비 |
| `inference-engine` | 추론 엔진(inference engine) | inference engine | 推理引擎 | 완비 |
| `information-integrity` | 정보 무결성(information integrity) | information integrity | 信息完整性(information integrity) | 완비 |
| `information-retrieval` | 정보 검색(information retrieval) | information retrieval | 信息检索 | 완비 |
| `input-context` | 입력 맥락(input context) | input context | 输入上下文 | 완비 |
| `instruction-tuning` | 지시 튜닝(instruction tuning) | instruction tuning | 指令微调 | 완비 |
| `intermediate-representation` | 중간 표현(intermediate representation) | intermediate representation | 中间表示 | 완비 |
| `interpretation-boundary` | 해석 경계(interpretation boundary) | interpretation boundary | 解释边界 | 완비 |
| `intervention-feedback` | 개입 피드백(intervention feedback) | intervention feedback | 干预反馈(intervention feedback) | 완비 |
| `kernel` | SVM 커널(kernel) | kernel | 核函数(kernel) | 완비 |
| `k-means` | k-means | k-means | k-means | 완비 |
| `keyword-search` | 키워드 검색(keyword search) | keyword search | 关键词搜索(keyword search) | 완비 |
| `knowledge-base` | 지식 기반(knowledge base) | knowledge base | 知识库 | 완비 |
| `knowledge-representation` | 지식 표현(knowledge representation) | knowledge representation | 知识表示 | 완비 |
| `label-consistency` | 라벨 일관성(label consistency) | label consistency | 标签一致性(label consistency) | 완비 |
| `label-prediction` | 라벨 예측(label prediction) | label prediction | 标签预测(label prediction) | 완비 |
| `labeled-example` | 라벨이 있는 예시(labeled example) | labeled example | 带标签样本(labeled example) | 완비 |
| `language-model` | 언어 모델(language model) | language model | 语言模型 | 완비 |
| `language-modeling` | 언어 모델링(language modeling) | language modeling | 语言建模 | 완비 |
| `learned-representation` | 학습된 표현(learned representation) | learned representation | 学习到的表示 | 완비 |
| `learning` | AI 학습(learning) | AI learning | AI 学习(learning) | 완비 |
| `learning-based-approach` | 학습 기반 접근(learning-based approach) | learning-based approach | 学习型方法 | 완비 |
| `least-privilege` | 최소 권한(least privilege) | least privilege | 最小权限 | 완비 |
| `license` | 자료 라이선스(license) | material license | 资料许可(license) | 완비 |
| `limit` | 극한(limit) | limit | 极限 | 완비 |
| `linear-algebra` | 선형대수(linear algebra) | linear algebra | 线性代数(linear algebra) | 완비 |
| `linear-regression` | 선형회귀(linear regression) | linear regression | 线性回归 | 완비 |
| `linear-transformation` | 선형 변환(linear transformation) | linear transformation | 线性变换(linear transformation) | 완비 |
| `llm` | LLM(대규모 언어 모델) | LLM | 大语言模型 | 완비 |
| `log-loss` | 로그 손실(log loss) | log loss | log loss | 완비 |
| `logarithm` | 수학 로그(logarithm) | mathematical logarithm | 数学对数(logarithm) | 완비 |
| `logistic-regression` | 로지스틱 회귀(logistic regression) | logistic regression | 逻辑回归 | 완비 |
| `long-context` | 롱 컨텍스트(long-context) | long-context | 长上下文 | 완비 |
| `long-term-dependency` | 장기 의존성(long-term dependency) | long-term dependency | 长期依赖 | 완비 |
| `loss` | 손실(loss) | loss | 损失(loss) | 완비 |
| `loss-curve` | 손실 곡선(loss curve) | loss curve | 损失曲线 | 완비 |
| `loss-function` | 손실 함수(loss function) | loss function | 损失函数 | 완비 |
| `machine-learning` | 머신러닝(machine learning) | machine learning | 机器学习 | 완비 |
| `manifold` | 매니폴드(manifold) | manifold | 流形(manifold) | 완비 |
| `margin` | 마진(margin) | margin | 间隔(margin) | 완비 |
| `market-substitution` | 시장 대체(market substitution) | market substitution | 市场替代(market substitution) | 완비 |
| `matrix` | 행렬(matrix) | matrix | 矩阵 | 완비 |
| `matrix-multiplication` | 행렬 곱(matrix multiplication) | matrix multiplication | 矩阵乘法 | 완비 |
| `maximum-likelihood-estimation-mle` | 최대우도추정(maximum likelihood estimation, MLE) | maximum likelihood estimation (MLE) | 最大似然估计(maximum likelihood estimation, MLE) | 완비 |
| `mean` | 평균(mean) | mean | 平均值 | 완비 |
| `mean-squared-error-mse` | 평균 제곱 오차(mean squared error, MSE) | mean squared error, MSE | 均方误差，MSE | 완비 |
| `metadata` | 문서 검색 메타데이터(metadata) | document retrieval metadata | 文档检索元数据(metadata) | 완비 |
| `metric` | 평가 지표(metric) | metric | 评估指标 | 완비 |
| `missing-value` | 결측값(missing value) | missing value | 缺失值(missing value) | 완비 |
| `model` | 모델(model, 모형) | model | 模型 | 완비 |
| `model-context-protocol-mcp` | 모델 컨텍스트 프로토콜(Model Context Protocol, MCP) | Model Context Protocol, MCP | 模型上下文协议，MCP | 완비 |
| `model-input` | 모델 입력 정의(model input) | model input definition | 模型输入定义(model input) | 완비 |
| `model-output` | 모델 출력 정의(model output) | model output definition | 模型输出定义(model output) | 완비 |
| `model-score` | 모델 후보 점수(model score) | candidate model score | 模型候选分数(model score) | 완비 |
| `model-selection` | 모델 선택(model selection) | model selection | 模型选择 | 완비 |
| `model-training` | 모델 훈련(model training) | model training | 模型训练 | 완비 |
| `model-validation` | 모델 검증(model validation) | model validation | 模型验证 | 완비 |
| `modeling-task` | 모델링 과제(modeling task) | modeling task | 建模任务(modeling task) | 완비 |
| `motion-planning` | 모션 플래닝(motion planning) | motion planning | 运动规划(motion planning) | 완비 |
| `multilayer-neural-network` | 다층 신경망(multilayer neural network) | multilayer neural network | 多层神经网络 | 완비 |
| `nearest-neighbor` | 최근접 이웃(nearest neighbor) | nearest neighbor | 最近邻 | 완비 |
| `next-token-prediction` | 다음 토큰 예측(next-token prediction) | next-token prediction | 下一 token 预测 | 완비 |
| `noise` | 잡음(noise) | noise | 噪声 | 완비 |
| `nondeterminism` | 비결정성(nondeterminism) | nondeterminism | 非确定性 | 완비 |
| `numerical-stability` | 수치 안정성(numerical stability) | numerical stability | 数值稳定性 | 완비 |
| `object-detection` | 객체 검출(object detection) | object detection | 目标检测(object detection) | 완비 |
| `objective-function` | 목적 함수(objective function) | objective function | 目标函数(objective function) | 완비 |
| `observation` | 관찰 결과(observation) | observation | 观测结果(observation) | 완비 |
| `one-hot-representation` | 원-핫 표현(one-hot representation) | one-hot representation | 独热表示(one-hot representation) | 완비 |
| `oob-score` | OOB 점수(out-of-bag score) | OOB score(out-of-bag score) | OOB 分数(out-of-bag score) | 완비 |
| `open-weight-model` | 오픈웨이트 모델(open-weight model) | open-weight model | 开放权重模型(open-weight model) | 완비 |
| `optimization` | 최적화(optimization) | optimization | 优化(optimization) | 완비 |
| `optimizer` | 옵티마이저(optimizer) | optimizer | 优化器(optimizer) | 완비 |
| `outlier` | 이상값(outlier) | outlier | 异常值 | 완비 |
| `output-structure` | 모델링 출력 구조(output structure) | modeling output structure | 建模输出结构(output structure) | 완비 |
| `overfitting` | 과적합(overfitting) | overfitting | 过拟合 | 완비 |
| `parameter` | 파라미터(parameter) | parameter | 参数(parameter) | 완비 |
| `partial-derivative` | 편미분(partial derivative) | partial derivative | 偏导数(partial derivative) | 완비 |
| `partial-observability` | 부분 관측(partial observability) | partial observability | 部分可观测性(partial observability) | 완비 |
| `permission` | 도구 실행 권한(permission) | tool execution permission | 工具执行权限(permission) | 완비 |
| `point-prediction` | 점 예측(point prediction) | point prediction | 点预测(point prediction) | 완비 |
| `policy-based-reinforcement-learning` | 정책 기반 강화학습(policy-based reinforcement learning) | policy-based reinforcement learning | 策略型强化学习(policy-based reinforcement learning) | 완비 |
| `population` | 모집단(population) | population | 总体(population) | 완비 |
| `precision` | 정밀도(precision) | precision | 精确率 | 완비 |
| `prediction` | 예측(prediction) | prediction | 预测 | 완비 |
| `prediction-contract` | 예측 계약(prediction contract) | prediction contract | 预测契约(prediction contract) | 완비 |
| `preprocessing` | 전처리(preprocessing) | preprocessing | 预处理 | 완비 |
| `pretraining` | 사전학습(pretraining) | pretraining | 预训练(pretraining) | 완비 |
| `principal-component-analysis-pca` | 주성분 분석(principal component analysis, PCA) | principal component analysis (PCA) | 主成分分析(PCA) | 완비 |
| `privacy` | 개인정보(privacy) | privacy | 隐私(privacy) | 완비 |
| `probabilistic-choice` | 확률적 선택(probabilistic choice) | probabilistic choice | 概率性选择(probabilistic choice) | 완비 |
| `probabilistic-model` | 확률 모델(probabilistic model) | probabilistic model | 概率模型(probabilistic model) | 완비 |
| `probabilistic-prediction` | 확률적 예측(probabilistic prediction) | probabilistic prediction | 概率性预测(probabilistic prediction) | 완비 |
| `probabilistic-reasoning` | 확률 추론(probabilistic reasoning) | probabilistic reasoning | 概率推理(probabilistic reasoning) | 완비 |
| `probability` | 확률(probability) | probability | 概率(probability) | 완비 |
| `probability-calibration` | 확률 보정(probability calibration) | probability calibration | 概率校准 | 완비 |
| `probability-distribution` | 확률분포(probability distribution) | probability distribution | 概率分布(probability distribution) | 완비 |
| `probability-estimate` | 확률 추정값(probability estimate) | probability estimate | 概率估计 | 완비 |
| `prompt` | 프롬프트(prompt) | prompt | 提示词(prompt) | 완비 |
| `prompt-engineering` | 프롬프트 엔지니어링(prompt engineering) | prompt engineering | 提示词工程(prompt engineering) | 완비 |
| `prompt-injection` | 프롬프트 인젝션(prompt injection) | prompt injection | 提示词注入(prompt injection) | 완비 |
| `prompt-structuring` | 프롬프트 구조화(prompt structuring) | prompt structuring | 提示词结构化(prompt structuring) | 완비 |
| `protected-expression` | 저작권의 표현(protected expression) | protected expression | 受保护表达(protected expression) | 완비 |
| `provenance` | 출처 추적(provenance) | provenance | 出处追踪(provenance) | 완비 |
| `proxy-label` | 프록시 라벨(proxy label) | proxy label | 代理标签(proxy label) | 완비 |
| `proxy-target` | 대리 타깃(proxy target) | proxy target | 代理目标 | 완비 |
| `quotation` | 인용(quotation) | quotation | 引用(quotation) | 완비 |
| `random-forest` | 랜덤포레스트(random forest) | random forest | 随机森林(random forest) | 완비 |
| `ranking` | 순위화(ranking) | ranking | 排序 | 완비 |
| `rate-of-change` | 변화율(rate of change) | rate of change | 变化率(rate of change) | 완비 |
| `reasoning` | 논리적 추론(reasoning) | reasoning | 逻辑推理(reasoning) | 완비 |
| `recall` | 재현율(recall) | recall | 召回率 | 완비 |
| `recommendation-task` | 추천 과제(recommendation task) | recommendation task | 推荐任务(recommendation task) | 완비 |
| `recurrent-neural-network` | 순환 신경망(RNN, recurrent neural network) | RNN, recurrent neural network | RNN，循环神经网络 | 완비 |
| `regression` | 회귀(regression) | regression | 回归(regression) | 완비 |
| `regularization` | 정규화(regularization) | regularization | 正则化(regularization) | 완비 |
| `reinforcement-learning` | 강화학습(reinforcement learning) | reinforcement learning | 强化学习 | 완비 |
| `reinforcement-learning-agent` | 강화학습 에이전트(reinforcement learning agent) | reinforcement learning agent | 强化学习智能体 | 완비 |
| `reinforcement-learning-environment` | 강화학습 환경(reinforcement learning environment) | reinforcement learning environment | 强化学习环境 | 완비 |
| `reinforcement-learning-policy` | 강화학습 정책(reinforcement learning policy) | reinforcement learning policy | 强化学习策略 | 완비 |
| `representation` | 표현(representation) | representation | 表示(representation) | 완비 |
| `representation-learning` | 표현 학습(representation learning) | representation learning | 表示学习(representation learning) | 완비 |
| `reproducibility` | 재현성(reproducibility) | reproducibility | 可复现性 | 완비 |
| `response-generation` | LLM 응답 생성(response generation) | LLM response generation | LLM 响应生成(response generation) | 완비 |
| `retrieval` | RAG 검색(retrieval) | RAG retrieval | RAG 检索(retrieval) | 완비 |
| `retrieval-augmented-generation-rag` | 검색 증강 생성(retrieval-augmented generation, RAG) | retrieval-augmented generation, RAG | 检索增强生成(retrieval-augmented generation, RAG) | 완비 |
| `reward` | 보상(reward) | reward | 奖励 | 완비 |
| `reward-design` | 보상 설계(reward design) | reward design | 奖励设计(reward design) | 완비 |
| `reward-hacking` | 보상 해킹(reward hacking) | reward hacking | reward hacking | 완비 |
| `rightsholder` | 권리자(rightsholder) | rightsholder | 权利人(rightsholder) | 완비 |
| `rlhf-reinforcement-learning-from-human-feedback` | RLHF(reinforcement learning from human feedback) | RLHF, reinforcement learning from human feedback | RLHF，基于人类反馈的强化学习 | 완비 |
| `rule-based-approach` | 규칙 기반 접근(rule-based approach) | rule-based approach | 规则型方法 | 완비 |
| `rule-based-system` | 규칙 기반 시스템(rule-based system) | rule-based system | 规则式系统(rule-based system) | 완비 |
| `safety` | AI 시스템 안전성(safety) | safety | AI 系统安全性(safety) | 완비 |
| `sample-space` | 표본공간(sample space) | sample space | 样本空间(sample space) | 완비 |
| `sample-unit` | 샘플 단위(sample unit) | sample unit | 样本单位 | 완비 |
| `sampling` | 샘플링(sampling) | sampling | 采样 | 완비 |
| `sampling-bias` | 표본 편향(sampling bias) | sampling bias | 样本偏差(sampling bias) | 완비 |
| `scalar` | 스칼라(scalar) | scalar | 标量 | 완비 |
| `search` | 상태공간 탐색(search) | state-space search | 状态空间搜索(search) | 완비 |
| `search-index` | 검색 인덱스(search index) | search index | 搜索索引(search index) | 완비 |
| `search-space` | 탐색 공간(search space) | search space | 搜索空间(search space) | 완비 |
| `security` | 보안(security) | security | 安全(security) | 완비 |
| `selective-labels` | 선택적 라벨(selective labels) | selective labels | 选择性标签(selective labels) | 완비 |
| `self-attention` | 셀프 어텐션(self-attention) | self-attention | self-attention | 완비 |
| `semi-supervised-learning` | 반지도학습(semi-supervised learning) | semi-supervised learning | 半监督学习 | 완비 |
| `sensitive-information` | 민감 정보(sensitive information) | sensitive information | 敏感信息(sensitive information) | 완비 |
| `sequence-modeling` | 순차 모델링(sequence modeling) | sequence modeling | 序列建模(sequence modeling) | 완비 |
| `sigmoid` | 시그모이드(sigmoid) | sigmoid | sigmoid | 완비 |
| `sim-to-real-gap` | 시뮬레이션-현실 간극(sim-to-real gap) | sim-to-real gap | sim-to-real gap | 완비 |
| `similarity` | 유사도(similarity) | similarity | 相似度 | 완비 |
| `similarity-search` | 유사도 검색(similarity search) | similarity search | 相似度检索 | 완비 |
| `softmax` | 소프트맥스(softmax) | softmax | softmax | 완비 |
| `software-regression` | AI 서비스 소프트웨어 회귀(software regression) | AI service software regression | AI 服务软件回归(software regression) | 완비 |
| `source-data` | 원천데이터(source data) | source data | 原始数据 | 완비 |
| `sparsity` | 데이터 희소성(sparsity) | sparsity | 数据稀疏性(sparsity) | 완비 |
| `speech-generation` | 음성 생성(speech generation) | speech generation | 语音生成(speech generation) | 완비 |
| `standard-deviation` | 표준편차(standard deviation) | standard deviation | 标准差(standard deviation) | 완비 |
| `standardization` | 표준화(standardization) | standardization | 标准化(standardization) | 완비 |
| `state` | 에이전트 상태(state) | agent state | 智能体状态(state) | 완비 |
| `statistical-inference` | 통계적 추론(statistical inference) | statistical inference | 统计推断(statistical inference) | 완비 |
| `statistical-language-model` | 통계적 언어 모델(statistical language model) | statistical language model | 统计语言模型(statistical language model) | 완비 |
| `statistical-sample` | 표본(sample) | statistical sample | 统计样本(sample) | 완비 |
| `stochastic-process` | 확률적 과정(stochastic process) | stochastic process | 随机过程(stochastic process) | 완비 |
| `supervised-learning` | 지도학습(supervised learning) | supervised learning | 监督学习 | 완비 |
| `supervised-learning-label` | 지도학습 라벨(supervised learning label) | supervised learning label | 监督学习标签(supervised learning label) | 완비 |
| `support-vector-machine` | SVM(support vector machine) | SVM, support vector machine | 支持向量机(SVM, support vector machine) | 완비 |
| `supporting-evidence` | 검증 근거(supporting evidence) | supporting evidence | 支持证据 | 완비 |
| `symbolic-ai` | 기호 기반 AI(symbolic AI) | symbolic AI | 符号式 AI(symbolic AI) | 완비 |
| `target` | 타깃(target) | target | 目标 | 완비 |
| `task-definition` | 문제 정의(task definition) | task definition | 任务定义(task definition) | 완비 |
| `tensor` | 텐서(tensor) | tensor | 张量 | 완비 |
| `test-data` | 테스트 데이터(test data) | test data | 测试数据 | 완비 |
| `text-and-data-mining` | 학습 데이터 맥락의 텍스트·데이터 마이닝(text and data mining, TDM) | text and data mining in the training-data context | 学习数据语境下的文本与数据挖掘(text and data mining, TDM) | 완비 |
| `threshold` | 임계값(threshold) | threshold | 阈值 | 완비 |
| `time-split` | 시간 순서 분할(time split) | time split | 时间顺序切分(time split) | 완비 |
| `token` | 토큰(token) | token | token | 완비 |
| `tokenization` | 토큰화(tokenization) | tokenization | token 化(tokenization) | 완비 |
| `tool-use` | 에이전트 도구 사용(tool use) | tool use | 智能体工具使用(tool use) | 완비 |
| `topology` | 위상(topology) | topology | 拓扑(topology) | 완비 |
| `training-data` | 학습 데이터(training data) | training data | 训练数据 | 완비 |
| `trajectory` | 궤적(trajectory) | trajectory | 轨迹(trajectory) | 완비 |
| `transformative-use` | 변형적 이용(transformative use) | transformative use | 转换性使用(transformative use) | 완비 |
| `transformer` | 트랜스포머(Transformer) | Transformer | Transformer | 완비 |
| `transparency` | 투명성(transparency) | transparency | 透明性(transparency) | 완비 |
| `true-objective` | 진짜 목표(true objective) | true objective | 真实目标(true objective) | 완비 |
| `trust-boundary` | 신뢰 경계(trust boundary) | trust boundary | 信任边界(trust boundary) | 완비 |
| `uncertainty` | 불확실성(uncertainty) | uncertainty | 不确定性(uncertainty) | 완비 |
| `underfitting` | 과소적합(underfitting) | underfitting | 欠拟合 | 완비 |
| `unsupervised-learning` | 비지도학습(unsupervised learning) | unsupervised learning | 无监督学习 | 완비 |
| `validation-data` | 검증 데이터(validation data) | validation data | 验证数据(validation data) | 완비 |
| `value-based-reinforcement-learning` | 가치 기반 강화학습(value-based reinforcement learning) | value-based reinforcement learning | 价值型强化学习(value-based reinforcement learning) | 완비 |
| `variable` | 변수(variable) | variable | 变量(variable) | 완비 |
| `variable-transformation` | 변수변환(variable transformation) | variable transformation | 变量变换(variable transformation) | 완비 |
| `variance` | 분산(variance) | variance | 方差 | 완비 |
| `vector` | 벡터(vector) | vector | 向量 | 완비 |
| `vector-calculus` | 벡터해석(vector calculus) | vector calculus | 向量微积分(vector calculus) | 완비 |
| `vector-database` | 벡터 데이터베이스(vector database) | vector database | 向量数据库 | 완비 |
| `vector-search` | 벡터 검색(vector search) | vector search | 向量搜索(vector search) | 완비 |
| `vector-space` | 벡터 공간(vector space) | vector space | 向量空间(vector space) | 완비 |
| `vectorization` | 벡터화(vectorization) | vectorization | 向量化 | 완비 |
| `visualization` | 데이터 시각화(visualization) | data visualization | 数据可视化(visualization) | 완비 |
| `vocabulary` | 어휘 사전(vocabulary) | vocabulary | vocabulary | 완비 |
| `weight` | 가중치(weight) | weight | 权重 | 완비 |
| `weighted-sum` | 가중합(weighted sum) | weighted sum | 加权和(weighted sum) | 완비 |
