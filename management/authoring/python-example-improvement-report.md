# Python 예제 학습밀도 개선 통합 리포트

작성일: 2026-07-23

## 목적

이 리포트는 기존 세 문서를 하나로 병합한 관리 문서다.

- `python-actual-model-example-candidates.md`: Part 3-6 실제 모델·라이브러리 예제 후보
- `python-hardcoded-answer-check-report.md`: Part 1-6 하드코딩 정답 확인형 Python 예제 진단
- `part-06-ch01-09-sdk-example-candidates.md`: Part 6 Chapter 1-9 SDK 기반 예제 개편 후보

통합 기준은 `management/guidelines/python-example-guidelines.md`다. 핵심은 Python 예제를 늘리는 것이 아니라, Section 중심 질문을 실제 입력 변화, 모델 출력, 후보 순위, 실패 조건, 평가 로그로 더 잘 확인하게 만드는 것이다. 실제 모델을 쓰는 것 자체가 목적이 아니라, Section의 중심 질문이 모델 입력, 출력, 평가, 오류, 후보 순위, 생성 결과의 변화로 더 잘 보일 때 후보로 잡는다.

원본 문서는 병합 뒤 중복 관리를 위해 삭제했다. 이 통합본은 세 문서의 후보 목록, 판단 기준, 하드코딩 진단, Part 6 Chapter 1-9 SDK 추적 상태를 이어받는 기준 문서다.

## 판단 기준

### 실제 모델·라이브러리 사용

Part 3 이후에는 실제 모델이나 모델에 가까운 라이브러리를 적극 검토한다. 단, 모델 실행 자체가 목적이 되어서는 안 된다.

여기서 `실제 모델`은 반드시 대형 모델이나 외부 API만 뜻하지 않는다. 다음을 모두 포함한다.

- scikit-learn의 classifier, regressor, clustering, baseline, metric, feature selection, dimensionality reduction
- PyTorch 또는 TensorFlow의 작은 neural network, dropout, optimizer, train/eval mode
- tokenizer, vectorizer, embedding, retrieval model, local LLM, Ollama 또는 API 호출 mock
- 실제 모델을 직접 쓰기 어렵지만 모델 입출력에 가까운 작은 실행 구조

후보로 잡는 경우:

- Section 중심축이 feature, label, split, metric, 모델 출력, 후보 순위, 생성 결과 변화와 직접 연결된다.
- threshold, hyperparameter, random seed, preprocessing, prompt, decoding setting을 바꾸면 출력이나 실패 조건이 실제로 달라진다.
- 기존 예제가 수작업 계산, 고정 표, 하드코딩 규칙에 가까워 실제 라이브러리 입출력이 학습 효과를 높인다.
- 기존 Python 예제가 있더라도 `실제 모델 입출력`보다 집계, 표 재구성, 하드코딩된 규칙 확인에 가까워 보강 가치가 있다면 후보로 잡는다.
- 외부 API나 큰 모델이 부담이면 scikit-learn, PyTorch 작은 모델, tokenizer/vectorizer, local LLM, mock 결과, 저장된 CSV 로그로 축약할 수 있다.

예제에 반드시 남길 것:

1. 독자가 바꿀 값: split, feature, threshold, hyperparameter, prompt, decoding setting 등
2. 관찰할 출력: 예측 샘플, 오류 사례, 후보 순위, train/validation gap, retrieved document, generated text 차이 등
3. Section 중심축으로 닫는 해설: 왜 그 출력 차이가 현재 절의 핵심 질문을 확인하는가

### 하드코딩 정답 확인형 판정

다음 패턴은 개선 후보로 본다.

- 사람이 미리 넣은 정답 사전, 기대 범주, 통과 답안을 코드가 들고 있다.
- 코드의 주된 출력이 독자 판단의 확장보다 `맞음/틀림`, `통과/탈락`, `정답 범주 일치` 확인에 머문다.
- 조작 변수를 바꿨을 때 경계, 실패 조건, 후보 순위, 비용, 누락이 달라지는 구조보다 이미 설계된 답안을 다시 확인하는 구조가 앞선다.

다만 지도학습 label, 평가 metric, 검색 기대 상태처럼 모델 학습·평가·오류 비교에 쓰이는 값은 곧바로 하드코딩 정답 확인형으로 보지 않는다. 핵심 질문은 `코드가 답을 확인하는가`, 아니면 `판단 기준이 작동하고 실패하는 조건을 드러내는가`이다.

## 범위 요약

### 실제 모델 후보 검토 범위

- 대상: `docs/parts/part-03`부터 `docs/parts/part-06`까지의 한국어 `section-*.md`
- 제외: 영어 번역본 `*.en.md`, 중국어 번역본 `*.zh.md`
- 검토 단위: Section 제목, Section ID, 도입부 중심 질문, 기존 Python 예제 여부

### 실제 모델 후보 검토

| Part | 한국어 Section 수 | Python 코드가 있는 Section 수 | Python 코드 블록 수 | 실제 모델 예제 후보 수 |
| --- | ---: | ---: | ---: | ---: |
| Part 3 | 52 | 18 | 18 | 8 |
| Part 4 | 59 | 37 | 79 | 12 |
| Part 5 | 53 | 36 | 37 | 17 |
| Part 6 | 54 | 33 | 33 | 21 |
| 합계 | 218 | 124 | 167 | 58 |

### 하드코딩 정답 확인형 검토 범위

- 대상: `docs/parts/part-01`부터 `docs/parts/part-06`까지의 한국어 `section-*.md`
- 제외: 같은 Section의 영어 번역본 `*.en.md`, 중국어 번역본 `*.zh.md`
- 검토 단위: Python 코드 블록이 있는 Section과 해당 Section의 도입부, 핵심 질문, 예제 설명

### 하드코딩 정답 확인형 검토

| Part | Python 코드가 있는 한국어 Section 수 | Python 코드 블록 수 | 판정 요약 |
| --- | ---: | ---: | --- |
| Part 1 | 0 | 0 | 해당 없음 |
| Part 2 | 39 | 298 | 문법, 자료구조, pandas, 그래프 사용법 중심. 하드코딩 정답 확인형 사례 없음 |
| Part 3 | 18 | 18 | 샘플 단위, 라벨 품질, 데이터 구조 점검 중심 |
| Part 4 | 37 | 79 | 지도학습 label, metric, 모델 비교 중심 |
| Part 5 | 36 | 37 | 신경망 계산, 손실, gradient, 표현 변화 중심 |
| Part 6 | 33 | 33 | LLM/RAG/평가/에이전트 예제 중 일부가 정답 확인형에 가까움 |
| 합계 | 163 | 465 | 확정 해당 2건, 경계 사례 2건 |

### Part 6 Chapter 1-9 SDK 추적 범위

- 대상: `docs/parts/part-06/chapter-01`부터 `docs/parts/part-06/chapter-09`
- 기존 Python 코드 블록 수: 14개
- 기존 Python 코드가 있는 Section: P6-2.5, P6-3.4, P6-4.2, P6-4.4, P6-5.1, P6-6.1, P6-6.2, P6-7.1, P6-7.2, P6-8.2, P6-9.1, P6-9.2, P6-9.3, P6-9.4
- Chapter 1에는 현재 Python 예제가 없어 기존 예제 개편 범위에서는 추적 대상이 없다.

## Part 3 실제 모델 후보

Part 3은 데이터셋 설계가 중심이다. 모델 예제는 성능 경쟁보다 잘못된 데이터 계약이 모델 평가를 어떻게 왜곡하는지 보여 주는 데 사용한다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P3-4.2 샘플 단위가 흔들리면 무엇이 함께 흔들리는가 | 샘플 단위가 feature, label, split, evaluation을 함께 흔든다 | pandas 집계 예제 있음 | 같은 원시 로그를 row-level과 event-level로 각각 `LogisticRegression` 또는 `DecisionTreeClassifier`에 넣고, row split에서 같은 event가 train/test에 섞여 점수가 부풀 수 있음을 보인다 |
| 높음 | P3-4.5 지금 모은 샘플은 전체 운영 상황을 얼마나 대표하는가 | 대표성과 운영 조건 편향 | Python 예제 있음 | 대표성 편향 train set과 균형 test set에서 `DummyClassifier`와 classifier의 그룹별 오류율을 비교한다 |
| 높음 | P3-6.1 비교할 구조는 어떤 특징으로 남기는가 | 구조를 feature로 바꾸는 기준 | 수작업 feature 계산 예제 있음 | 평균만 쓰는 모델과 변화·변동성 feature 추가 모델의 예측 오류를 비교한다 |
| 중간 | P3-6.2 특징만으로 부족할 때 어떤 중간 표현을 더 둘 수 있는가 | feature와 중간 표현 | Python 예제 있음 | `TfidfVectorizer` 또는 간단한 embedding/vectorizer로 원문 표현과 수작업 feature의 후보 순위 차이를 비교한다 |
| 중간 | P3-6.5 서로 단위와 크기가 다른 특징은 어떻게 함께 읽고 남기는가 | scale 차이 | 코드 없음 | `StandardScaler` 전후로 k-NN 또는 logistic regression 결과가 달라지는 예제를 둔다 |
| 높음 | P3-8.6 확정 라벨이 검토된 사례에만 남아 있다면 무엇을 적어야 하는가 | selective labels | 코드 없음 | 검토된 일부 label만 학습했을 때 전체 후보군 오류가 어떻게 치우치는지 비교한다 |
| 높음 | P3-9.7 입력과 결과는 어떤 조건이 닫혀야 예측 문제로 읽을 수 있는가 | leakage, cutoff, horizon | 코드 없음 | 미래 정보가 섞인 feature와 cutoff 이전 feature만 쓴 모델의 성능 차이를 비교한다 |
| 높음 | P3-9.12 같은 target 이름이라도 어떤 오류가 더 아픈가 | 오류 비용 비대칭 | 코드 없음 | 같은 예측 확률에 threshold와 cost matrix를 적용해 FP/FN 비용 차이를 출력한다 |

## Part 4 실제 모델 후보

Part 4는 머신러닝 모델 자체가 중심이므로 scikit-learn 기반 실험을 적극적으로 쓸 수 있다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P4-5.1 과적합과 과소적합 | train score와 validation score 패턴 | 코드 없음 | `DecisionTreeClassifier(max_depth=...)` 또는 polynomial regression으로 underfit/fit/overfit 점수 패턴을 비교한다 |
| 높음 | P4-5.2 일반화 | 새 데이터에서 버티는가 | 코드 없음 | train/test split seed를 바꾸며 validation score 분산과 generalization gap을 비교한다 |
| 높음 | P4-6.4 평가 지표 지도 | 단일 accuracy 밖의 평가 | 코드 없음 | `sklearn.metrics`로 ROC-AUC, PR-AUC, log_loss, calibration, silhouette를 비교한다 |
| 높음 | P4-7.4 feature selection 방식 | filter, wrapper, PCA | 코드 없음 | `SelectKBest`, `RFE`, `PCA`의 남는 feature와 validation score를 비교한다 |
| 높음 | P4-8.1 모델 선택 | 문제에 맞는 모델 비교 | 코드 없음 | logistic regression, k-NN, tree, random forest를 cross-validation으로 비교한다 |
| 높음 | P4-8.2 기준 모델 | 최소 비교선 | 코드 없음 | `DummyClassifier`/`DummyRegressor`와 실제 모델을 비교한다 |
| 중간 | P4-9.2 튜닝과 검증 비용 | 후보 조합과 검증 반복 비용 | GridSearchCV 예제 있음 | 후보 수, CV 수, 실행 로그 수를 함께 출력해 비용 감각을 강화한다 |
| 중간 | P4-12.3 k-NN 점검 | k, scale, distance | 코드 없음 | `KNeighborsClassifier`에서 k와 scaling을 바꿔 최근접 이웃 목록이 바뀌는 예제를 둔다 |
| 높음 | P4-17.2 군집 해석 주의 | 군집은 정답 label이 아니다 | 코드 없음 | `KMeans`/`DBSCAN` 결과를 실제 label 또는 업무 그룹과 비교한다 |
| 중간 | P4-18.2 시각화와 정보 손실 | 차원 축소 손실 | Python 예제 있음 | PCA 2D에서 가까운 점과 원래 차원에서 가까운 점이 달라지는 사례를 보강한다 |
| 중간 | P4-19.4 강화학습 분기 | value/policy 큰 흐름 | 코드 없음 | bandit 또는 gridworld simulation으로 value/policy 차이를 보인다 |
| 중간 | P4-19.6 policy gradient | update 방향 직관 | Python 예제 있음 | 작은 bandit policy gradient simulation으로 reward 분포와 update 방향을 보인다 |

## Part 5 실제 모델 후보

Part 5는 작은 PyTorch 예제가 학습 루프, 모드 차이, gradient, 표현 변화 이해를 강화할 수 있다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P5-6.1 학습 루프 | forward, loss, backward, step | 수작업 학습 루프 예제 있음 | PyTorch `nn.Linear`로 `zero_grad -> forward -> loss -> backward -> step` 전후 parameter와 gradient를 출력한다 |
| 높음 | P5-6.4 학습 모드와 평가 모드 | train/eval mode | Python 예제 있음 | PyTorch `Dropout` 또는 `BatchNorm1d`로 같은 입력의 train/eval 출력 차이를 비교한다 |
| 높음 | P5-7.1 옵티마이저 | gradient를 update로 바꾸는 주체 | Python 예제 있음 | `backward()` 뒤에도 parameter가 바뀌지 않고 `optimizer.step()`에서 바뀌는 점을 확인한다 |
| 높음 | P5-7.2 학습률 | update 보폭 | Python 예제 있음 | 같은 gradient에서 learning rate별 loss trajectory와 overshoot를 비교한다 |
| 중간 | P5-7.3 Adam | adaptive update | Python 예제 있음 | SGD와 Adam의 초기 update와 loss 감소 곡선을 비교한다 |
| 높음 | P5-8.1 정규화 | 제약과 일반화 | Python 예제 있음 | weight decay 유무에 따른 train/validation loss와 weight norm 변화를 비교한다 |
| 높음 | P5-8.2 드롭아웃 | 과의존 완화 | dropout 로그 예제 있음 | 실제 `nn.Dropout`으로 train mode 무작위 출력과 eval mode 안정 출력을 비교한다 |
| 중간 | P5-8.3 안정화 | 초기화, batch normalization | 코드 없음 | 초기화 scale과 BatchNorm 유무에 따른 activation 분포를 비교한다 |
| 중간 | P5-10.1 표현 학습 | 학습된 표현 | Python 예제 있음 | hidden layer 출력의 class 분리 정도를 PCA/거리로 확인한다 |
| 중간 | P5-10.2 깊은 층의 표현 | 층별 표현 변화 | Python 예제 있음 | 학습 전후 hidden representation을 층별로 출력하거나 시각화한다 |
| 높음 | P5-11.1 CNN | 지역 패턴 | Python 예제 있음 | `nn.Conv2d` 작은 필터로 이미지 패치 반응을 출력한다 |
| 높음 | P5-11.2 합성곱과 풀링 | feature map 변화 | Python 예제 2개 있음 | `Conv2d`와 `MaxPool2d`로 위치 이동 반응과 feature map 크기를 출력한다 |
| 중간 | P5-12.1 RNN/LSTM/GRU | 순서와 상태 전달 | Python 예제 있음 | `nn.RNN` 또는 `nn.GRU`로 같은 토큰도 앞선 상태에 따라 hidden state가 달라짐을 확인한다 |
| 중간 | P5-12.2 장기 의존성 | 먼 정보 보존 | Python 예제 있음 | 단순 RNN과 LSTM을 작은 synthetic task로 비교한다 |
| 중간 | P5-13.1 attention | 위치별 가중 | Python 예제 있음 | scaled dot-product attention으로 query 변화에 따른 weight와 weighted sum 차이를 출력한다 |
| 중간 | P5-14.2 Transformer 블록 | attention, FFN, residual, normalization | Python 예제 있음 | `nn.TransformerEncoderLayer` 또는 축약 block으로 단계별 shape와 값을 보여 준다 |
| 높음 | P5-15.3 샘플링 | temperature, top-k, sampling | Ollama 또는 sampling 예제 있음 | local LLM 또는 고정 logits에서 생성 후보 다양성과 반복성을 비교한다 |

## Part 6 실제 모델·SDK 후보

Part 6은 LLM과 생성형 AI 시스템이 중심이다. 외부 API 과금과 최신성 의존이 크면 local LLM, tokenizer/vectorizer, mock tool result, 저장된 CSV 로그로 축약한다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P6-2.3 토큰화는 무엇을 바꾸는가 | 문자열이 token으로 쪼개지는 방식 | 코드 없음 | 실제 tokenizer로 한국어, 영어, 숫자, 공백, 이모지 입력의 token 수와 token ID 차이를 출력한다 |
| 중간 | P6-2.5 토크나이저 계열 차이 | tokenizer family 차이 | Python 예제 있음 | 기존 예제를 실제 tokenizer 라이브러리 기반으로 확장한다 |
| 높음 | P6-3.1 임베딩은 토큰 ID를 어떻게 비교 가능한 좌표로 바꾸는가 | token ID와 vector 차이 | 코드 없음 | 작은 embedding layer 또는 sentence embedding 모델로 ID 순서와 vector similarity가 다름을 보여 준다 |
| 높음 | P6-3.2 가까운 벡터는 왜 정답이 아니라 후보인가 | similarity는 후보 신호 | 코드 없음 | 실제 embedding/vectorizer로 query와 문서 후보 순위를 만들고 오답 후보도 함께 보여 준다 |
| 중간 | P6-4.2 attention의 참조 범위 | context window와 attention 범위 | Python 예제 있음 | tokenizer 길이 기반 context budget 예제로 window 밖 정보가 반영되지 않는 구조를 보인다 |
| 중간 | P6-4.4 KV cache | 반복 생성 cache | Python 예제 있음 | 현행 NumPy mock 유지 우선. 실제 transformer는 보충 후보로만 둔다 |
| 높음 | P6-6.1 다음 토큰 예측 | next-token과 긴 생성 | Python 예제 있음 | local LLM 또는 고정 logits에서 한 step 예측이 다음 입력으로 누적되는 과정을 출력한다 |
| 높음 | P6-6.2 출력 선택 규칙 | greedy, sampling, temperature | Python 예제 있음 | local LLM 또는 저장 로그로 temperature/top-k/top-p별 반복 출력 차이를 비교한다 |
| 높음 | P6-9.1 지시 튜닝 | 요청 형식 준수 | CSV 평가 예제 있음 | local LLM 또는 저장된 응답 로그로 일반 prompt와 구조화 prompt의 format compliance를 비교한다 |
| 높음 | P6-9.2 정렬 | helpfulness, safety, factuality 균형 | Python 예제 있음 | 실제 생성 후보를 여러 개 만든 뒤 안전 기준에서 탈락하는 후보를 보여 준다 |
| 중간 | P6-10.1 프롬프트 엔지니어링 | prompt가 출력 형식과 근거 사용을 바꿈 | Ollama 예제 있음 | 이미 방향이 좋다. prompt template, structured prompt, constraint prompt 비교를 더 체계화한다 |
| 높음 | P6-10.3 CoT와 self-consistency | 후보 합의 관찰 | 비코드 연습 | local LLM 또는 저장 로그로 같은 질문을 여러 번 생성해 결론 분포를 비교한다 |
| 중간 | P6-10.4 automatic prompt optimization | prompt 반복 개선 | 코드 없음 | 작은 prompt 후보 집합과 평가 함수로 prompt score 개선 loop를 보여 준다 |
| 높음 | P6-11.1 RAG는 왜 답변 전에 외부 근거를 붙이는가 | 검색 전후 근거 연결 | TF-IDF 예제 있음 | sentence embedding 또는 vectorizer를 선택적으로 추가해 lexical retrieval과 semantic retrieval 차이를 비교한다 |
| 높음 | P6-11.2 검색 결과는 어떻게 생성 입력과 답변으로 이어지는가 | retrieval failure와 generation failure 분리 | Python 예제 있음 | retrieved docs와 generated answer를 local LLM 또는 mock generator로 연결한다 |
| 높음 | P6-12.1 벡터 데이터베이스 | vector, 원문, metadata payload | Python 예제 있음 | actual vector store는 부담이 크면 FAISS 또는 `sklearn NearestNeighbors`로 payload 보존과 top-k 변화를 보여 준다 |
| 높음 | P6-12.2 인덱스와 검색 품질 | speed와 후보 품질 trade-off | Python 예제 있음 | brute force와 approximate 후보 축소를 비교해 recall@k와 누락 사례를 출력한다 |
| 중간 | P6-13.1 도구 사용 | 실제 조회·계산·실행 필요성 | mock tool 예제 있음 | 계산기, 날짜 변환, CSV 조회 tool을 함수로 두고 언제 호출하는지 비교한다 |
| 중간 | P6-13.2 함수 호출 | 자연어를 함수 이름과 인자로 나눔 | Python 예제 있음 | JSON schema validation 또는 pydantic으로 missing argument, wrong type을 확인한다 |
| 높음 | P6-16.1 LLM 평가 | 품질 축 분리 | Python 예제 있음, 정답 확인형 개선 필요 | 실제 local LLM 응답 후보 또는 저장된 model output을 평가한다 |
| 높음 | P6-16.2 자동 평가와 사람 평가 | automatic gate와 human judgment | Python 예제 있음, 정답 확인형 개선 필요 | 자동 평가 false positive/false negative와 사람 검토 필요 사례를 집계한다 |
| 중간 | P6-20.1 BERT 계열 | 읽기 중심 encoder | 코드 없음 | sentence-transformer 또는 vectorizer 기반 intent classification/retrieval 예제로 비교한다 |
| 중간 | P6-20.2 이해 중심 NLP 태스크 | 라벨, 관계 점수, 랭킹 | Python 예제 있음 | keyword rule 예제를 classifier/vectorizer/ranker로 바꾸면 BERT 계열의 역할이 더 선명해진다 |

## Part 6 Chapter 1-9 SDK 개편 추적

이 절은 Part 6 Chapter 1-9의 기존 Python 예제 14개만 대상으로 한다. Chapter 1에는 현재 Python 예제가 없어 기존 예제 개편 범위에서는 추적 대상이 없다.

현재 `requirements.txt`에는 `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `chromadb`가 포함되어 있다. `transformers`, `tiktoken`, `openai`, `ollama` Python 클라이언트는 고정 의존성으로 보이지 않으므로 본문 예제로 넣기 전 의존성 정책을 먼저 정해야 한다.

### 우선 개편 후보

| 우선순위 | Section | 현재 예제 성격 | 권장 SDK/라이브러리 | 개편 방향 | 주의점 |
| --- | --- | --- | --- | --- | --- |
| 높음 | P6-2.5 토크나이저 계열 차이 | `transformers.AutoTokenizer` 예제가 있으나 의존성이 고정되어 있지 않은 선택 실행 코드 | `transformers` 또는 `tiktoken` + `transformers` | 별도 자산 스크립트와 실행 결과 CSV/표를 두어 계열별 토큰 수와 token ID 차이를 재현 가능하게 만든다 | 첫 실행 시 tokenizer 다운로드가 필요할 수 있으므로 저장 결과를 함께 둔다 |
| 높음 | P6-3.4 ANN 검색의 속도와 후보 누락 절충 | 무작위 벡터와 `coarse_window`로 ANN 감각을 흉내 냄 | `scikit-learn NearestNeighbors`, 선택적으로 `chromadb` | 전수 비교와 라이브러리 검색을 나란히 두고 `recall@k`, 후보 수, 누락 문서 ID를 출력한다 | 실제 ANN 튜닝이 중심이 되지 않게 한다 |
| 높음 | P6-4.2 attention의 참조 범위 | 수작업 토큰 수와 우선순위로 context budget 선택 | `tiktoken` 또는 tokenizer SDK | `tokens` 값을 실제 tokenizer로 계산해 공백·코드·로그 조각이 budget을 다르게 쓰는 장면을 보인다 | 최신 상용 context window 숫자를 본문 고정값처럼 쓰지 않는다 |
| 높음 | P6-6.2 출력 선택 규칙 | 고정 확률 슬롯에서 greedy/sampling/temperature 비교 | Ollama, OpenAI SDK 저장 로그, 또는 고정 logits 유지 + 선택 실행 스크립트 | temperature/top_p/top_k별 생성 결과를 CSV로 저장하고 본문은 응답 다양성, 반복률, 형식 안정성을 분석한다 | 실시간 API 호출은 기본 본문 예제로 두지 않는다 |
| 높음 | P6-9.1 지시 튜닝 | CSV의 일반 응답/지시형 응답 형식 신호 집계 | Ollama 또는 OpenAI SDK 저장 로그 | 일반 prompt와 구조화 prompt를 같은 모델에 넣어 만든 응답 로그를 CSV로 저장하고 형식 준수율을 비교한다 | 실제 instruction tuning 구현으로 오해되지 않게 한다 |
| 높음 | P6-9.2 정렬 | 사람이 작성한 후보 응답을 문자열 규칙으로 다축 평가 | OpenAI SDK 저장 로그, Ollama 저장 로그, 선택적으로 moderation/eval mock | 위험 질문별 생성 후보를 저장하고 helpfulness/safety/factuality 축에서 자동 판정과 사람 검토 필요 항목을 나눈다 | 자동 안전 판정을 실제 정책 판정으로 단정하지 않는다 |

### 중간 후보

| Section | 현재 예제 성격 | 개편 방향 | 보류 이유 |
| --- | --- | --- | --- |
| P6-5.1 디코더 기반 누적 생성 | 손으로 만든 다음 토큰 후보표와 경로 비교 | 실제 생성 로그의 step별 누적 텍스트를 저장해 첫 출력 선택 뒤 흐름이 갈라지는 사례를 보인다 | 내부 후보표 전체를 안정적으로 노출하기 어렵고 모델 다운로드 의존이 있다 |
| P6-6.1 다음 토큰 예측 | 작은 n-gram 말뭉치로 다음 토큰 분포 생성 | local causal LM 또는 저장 logits로 next-token 예측 감각을 보강한다 | 초심자에게는 n-gram 축소 예제가 더 투명하다 |
| P6-7.2 스케일 | CSV의 가정 token 수와 비용표 집계 | tokenizer SDK로 요청 CSV의 실제 token count를 계산하는 보조 스크립트를 붙인다 | 가격, context window, latency는 최신성 의존이 크다 |
| P6-9.3 실패 신호 진단 | 관찰 신호 가중치로 보강 경로 선택 | 실제 실패 출력 로그 CSV와 rule evaluator로 진단 지도를 보강한다 | 자동 진단기가 정답처럼 보일 위험이 있다 |

### 현행 유지

| Section | 판단 |
| --- | --- |
| P6-4.4 KV cache와 반복 생성 | NumPy로 K/V projection과 cache 재사용량을 보여 주는 현행 예제가 Section 중심축에 맞다 |
| P6-7.1 사전학습 | 실제 사전학습 SDK는 범위가 크므로 현행 bigram/CSV 예제를 유지한다 |
| P6-8.2 LoRA 저장 부담 | PEFT/LoRA 실제 학습보다 저장 부담 수치 감각이 중심이므로 현행 유지가 적절하다 |
| P6-9.4 LoRA low-rank | 실제 LoRA 구현보다 rank별 파라미터 수 비교가 중심이므로 현행 유지가 적절하다 |

### 새 예제 추가 후보

기존 Python 예제 개편은 아니지만 Chapter 1-9 전체를 대상으로 새 예제 추가까지 열면 다음을 별도 검토한다.

- P6-2.3: 실제 tokenizer로 token 수, token ID, 비용/청크 판단 변화 출력
- P6-3.1: 작은 embedding layer 또는 sentence/vectorizer 출력으로 token ID와 vector의 차이 확인
- P6-3.2: 실제 vectorizer/embedding 후보 순위로 가까운 벡터와 정답 근거의 차이 확인

## 하드코딩 정답 확인형 진단

### 확정 해당

| Section | 문제 판정 | 개선 방향 |
| --- | --- | --- |
| P6-16.1 LLM 평가는 왜 자연스러운 답과 품질 기준을 나눠 보는가 | 하드코딩된 답변 후보와 정답 조건이 코드 안에 함께 있다. 문자열 포함 여부로 correctness, groundedness, format, helpfulness를 판정해 이미 설계된 정답 후보가 통과하는 과정을 확인하게 된다 | 답변 후보와 근거 문장을 CSV로 분리하고, 축별 통과율, false positive 후보, 근거 문장 불일치 사례처럼 평가 기준이 실패하는 조건을 드러내게 재설계한다 |
| P6-16.2 자동 평가와 사람 평가는 어떻게 반복 검사와 맥락 판단을 나누는가 | 네 개의 답변 후보와 통과 조건이 모두 코드에 하드코딩되어 있다. 자동 평가와 사람 검토 질문도 문자열 포함 여부로 정해져 정답 확인형 라우팅에 가깝다 | 입력 묶음을 늘리고 `자동 통과지만 사람 검토 필요`, `자동 탈락이지만 수정 가능`, `자동 기준이 놓친 위험` 같은 경계 사례 수를 집계하도록 바꾼다 |

세부 기록:

- P6-16.1
  - 파일: `docs/parts/part-06/chapter-16/section-01.md`
  - 코드 위치: `answers = [`가 시작되는 Python 예제
  - Section 중심축: LLM 평가를 자연스러운 답 고르기가 아니라 정확성, 근거성, 형식, 유용성 같은 여러 축으로 나눠 판정하는 일로 설명한다.
  - 원본 판정 근거: `source_text`, `required_phrase`, `"14일"`, `"30일"`, `"개봉 제품"`, `"최신 정책 기준"`, `"접수"` 같은 문자열 포함 여부로 correctness, groundedness, format, helpfulness를 판정한다. 결과적으로 이미 설계된 정답 후보 `answer_a`가 통과하는 과정을 확인하게 된다.
  - 왜 학습 효과가 약한가: 평가 축의 개념을 탐색하기보다 사람이 심은 문자열 규칙으로 후보 답안을 채점한다. 독자는 평가 기준이 데이터에서 어떻게 흔들리는지 실험하기보다, 어느 문자열이 들어 있으면 맞는지 확인하는 쪽으로 읽을 위험이 있다.
- P6-16.2
  - 파일: `docs/parts/part-06/chapter-16/section-02.md`
  - 코드 위치: `outputs = [`가 시작되는 Python 예제
  - Section 중심축: 자동 평가는 반복 가능한 검사에 강하고, 사람 평가는 맥락 판단에 필요하므로 둘의 역할을 나눠야 한다는 점을 설명한다.
  - 원본 판정 근거: 자동 평가는 `"공지"` 포함, 마침표, 길이를 보고, 사람 검토 질문도 `"주문번호"`, `"직접 찾아보세요"`, `"가능"`, `"조건"` 같은 문자열 포함 여부로 정한다. 결과적으로 `answer_d`가 승인 후보가 되도록 설계된 정답 확인형 라우팅에 가깝다.
  - 왜 학습 효과가 약한가: 사람 판단이 필요한 맥락을 실제로 남기기보다 사람이 만든 문구 규칙으로 사람 검토 질문까지 자동 생성한다. 자동 평가의 한계가 아니라 자동 규칙표의 통과 여부가 중심으로 보일 수 있다.

### 경계 사례

| Section | 판정 | 개선 방향 |
| --- | --- | --- |
| P6-12.1 벡터 데이터베이스는 왜 원문과 메타데이터까지 함께 저장하는가 | `expected_category`, `top1_category_ok`는 정답 확인형 냄새가 있으나 top-k 후보, 유사도, 원문, metadata, payload 출력이 중심이므로 확정 해당은 아니다 | `expected_category`를 중심 출력에서 낮추고, `top_matches`, `retrieval_payload`, metadata 보존과 query vector 변화에 따른 순위 이동을 앞세운다 |
| P6-11.1 RAG는 왜 답변 전에 외부 근거를 붙이는가 | `current_signal`, `version_status == "current"`가 정답 신호처럼 보이지만 실제 TF-IDF 검색, 문서 순위, 유사도, 근거 문서 제목, RAG 답변 변화가 중심이다 | `current_signal` 포함 여부를 유일한 성공 기준처럼 보이지 않게 하고, 검색된 문서의 버전·출처·유사도와 답변 근거 연결을 함께 해석하도록 조정한다 |

세부 기록:

- P6-12.1
  - 파일: `docs/parts/part-06/chapter-12/section-01.md`
  - 코드 위치: `query_vectors = [` 안의 `expected_category`, `top1_category_ok`
  - 보류 이유: 독자가 query vector와 records를 바꿔 순위와 payload 변화를 볼 수 있으므로 확정 해당으로 보지는 않는다.
- P6-11.1
  - 파일: `docs/parts/part-06/chapter-11/section-01.md`
  - 코드 위치: `inspect_question()`의 `memory_mentions_current_signal`, `rag_mentions_current_signal`, `top_doc_is_current`
  - 보류 이유: 코드는 실제 TF-IDF 검색, 문서 순위, 유사도, 근거 문서 제목, RAG 답변 변화를 함께 보여 주며, 중심은 검색 전후 근거 연결 차이에 있다.
  - 추가 개선 메모: 가능하면 최신 신호가 없는 질문이나 잘못된 근거가 top-1으로 올라오는 실패 사례를 추가한다.

### 제외한 대표 유형

- Part 2의 `label_map`, `label_to_id`, 샘플 딕셔너리 예제: 문법 설명이 중심이다.
- Part 3의 라벨 품질 점검 예제: 샘플 단위, 중복 라벨, 검토 편향, 집계 단위 변화가 중심이다.
- Part 4의 분류·회귀·군집·트리·SVM 예제: label과 metric은 학습·평가 계산에 쓰인다.
- Part 5의 손실·gradient·optimizer·표현 변화 예제: 계산 경로와 파라미터 변화가 중심이다.
- P6-9.1 지시 튜닝 예제: CSV의 형식 신호와 요청 유형별 충족률 차이를 집계하는 구조다.
- P6-11.2 RAG 실패 분해 예제: 검색 실패와 생성 실패를 분리하는 실패 유형 실험으로 설계되어 있다.
- P6-13.1 도구 사용 예제: 도구 호출 필요 여부와 결과 반영 여부를 구분하는 흐름이다.
- P6-20.2 이해 중심 NLP 태스크 예제: CSV 입력, `relation_threshold`, 분류·문장쌍·랭킹 출력 차이가 중심이다.

## 우선 작업 묶음

1. Part 4 모델 기본 개념: P4-5.1, P4-5.2, P4-6.4, P4-8.2
2. Part 5 학습 루프와 모드 차이: P5-6.1, P5-6.4, P5-7.1, P5-8.2
3. Part 6 토큰화, 생성 선택, RAG, 평가: P6-2.3, P6-6.2, P6-11.1, P6-16.1, P6-16.2
4. Part 3 데이터 계약 예제: P3-4.2, P3-9.7, P3-9.12
5. Part 6 Chapter 1-9 SDK 우선 개편: P6-2.5, P6-4.2, P6-3.4, P6-6.2, P6-9.1, P6-9.2

## 보류 또는 주의할 Section 유형

- 개념 정의나 역사적 비교가 중심인 Section은 모델 실행이 본문 중심축을 흐릴 수 있다.
- Part 6의 외부 API·최신 제품 기능 의존 Section은 과금, 계정, 네트워크, 최신성 확인이 중심이 되면 본문 예제가 아니라 프로젝트나 보충 자료로 넘긴다.
- 강화학습 고급 보충 Section은 실제 RL 라이브러리보다 bandit/gridworld simulation이 적절하다.
- BERT·embedding 계열 Section은 외부 모델 다운로드가 필요하면 vectorizer나 저장된 embedding을 우선 검토한다.
- Part 6의 평가·RAG·에이전트 예제는 후보 답변, 검색 결과, 실패 유형을 사람이 설계하기 쉬우므로 정답 확인형 코드 판단 기준을 먼저 적용한다.

## 최종 추적 상태

| 상태 | 항목 |
| --- | --- |
| 즉시 패치 가능 | P6-3.4, P6-4.2, P6-16.1, P6-16.2 |
| 의존성 정책 확인 후 패치 | P6-2.5, P6-2.3, P6-3.1, P6-3.2 |
| 저장 로그 생성 방식 결정 후 패치 | P6-6.2, P6-9.1, P6-9.2, P6-10.3 |
| 보충 자산 후보 | P6-5.1, P6-6.1, P6-7.2, P6-9.3 |
| 현행 유지 우선 | P6-4.4, P6-7.1, P6-8.2, P6-9.4 |
