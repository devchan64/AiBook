# Part 3-6 실제 모델 Python 예제 후보 리포트

작성일: 2026-07-22

## 목적

이 리포트는 Part 3부터 Part 6까지의 한국어 Section 원고를 순차적으로 확인해, 실제 AI 모델이나 모델에 가까운 라이브러리를 실행해 보면 학습 효과가 커질 Section을 목록화한다.

여기서 `실제 모델`은 반드시 대형 모델이나 외부 API만 뜻하지 않는다. 다음을 모두 포함한다.

- scikit-learn의 classifier, regressor, clustering, baseline, metric, feature selection, dimensionality reduction
- PyTorch 또는 TensorFlow의 작은 neural network, dropout, optimizer, train/eval mode
- tokenizer, vectorizer, embedding, retrieval model, local LLM, Ollama 또는 API 호출 mock
- 실제 모델을 직접 쓰기 어렵지만 모델 입출력에 가까운 작은 실행 구조

검토 기준은 `management/guidelines/python-example-guidelines.md`의 `Part 3 이후 실제 모델 사용 판단`을 따른다. 즉, 실제 모델을 쓰는 것 자체가 목적이 아니라 Section의 중심 질문이 모델 입력, 출력, 평가, 오류, 후보 순위, 생성 결과의 변화로 더 잘 보일 때 후보로 잡았다.

## 검토 범위

- 대상: `docs/parts/part-03`부터 `docs/parts/part-06`까지의 한국어 `section-*.md`
- 제외: 영어 번역본 `*.en.md`, 중국어 번역본 `*.zh.md`
- 검토 단위: Section 제목, Section ID, 도입부 중심 질문, 기존 Python 예제 여부

| Part | 한국어 Section 수 | Python 코드가 있는 Section 수 | Python 코드 블록 수 | 실제 모델 예제 후보 수 |
| --- | ---: | ---: | ---: | ---: |
| Part 3 | 52 | 18 | 18 | 8 |
| Part 4 | 59 | 37 | 79 | 12 |
| Part 5 | 53 | 36 | 37 | 17 |
| Part 6 | 54 | 33 | 33 | 21 |
| 합계 | 218 | 124 | 167 | 58 |

## 선정 기준

다음 조건 중 하나 이상에 해당하면 후보로 잡았다.

- Section 중심축이 데이터셋, 샘플 단위, feature, label, split, metric, 모델 출력 변화와 직접 연결된다.
- 현재 예제가 수작업 계산이나 표 해설 중심이라, 작은 모델 실행이 있으면 `왜 이 판단이 모델에서 문제가 되는가`가 더 잘 보인다.
- 모델의 hyperparameter, threshold, random seed, train/test split, preprocessing, prompt, decoding setting을 바꾸면 출력이나 실패 조건이 실제로 달라진다.
- 기존 Python 예제가 있더라도 `실제 모델 입출력`보다 집계, 표 재구성, 하드코딩된 규칙 확인에 가까워 보강 가치가 있다.
- 실제 외부 API나 큰 모델이 부담이면 scikit-learn, PyTorch 작은 모델, tokenizer/vectorizer, local LLM, mock 결과로 축약할 수 있다.

## Part 3 후보

Part 3은 아직 본격 모델 학습보다 데이터셋 설계가 중심이다. 그래서 실제 모델 예제는 모델 성능을 높이는 목적보다 `잘못된 데이터 계약이 모델 평가를 어떻게 왜곡하는가`를 보여 주는 데 쓰는 편이 좋다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실제 모델 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P3-4.2 샘플 단위가 흔들리면 무엇이 함께 흔들리는가 | 샘플 단위가 feature, label, split, evaluation을 함께 흔든다 | pandas 집계 예제 있음 | 같은 원시 로그를 row-level과 event-level로 각각 `LogisticRegression` 또는 `DecisionTreeClassifier`에 넣고, row split에서는 같은 event가 train/test에 섞여 점수가 부풀 수 있음을 보여 준다 |
| 높음 | P3-4.5 지금 모은 샘플은 전체 운영 상황을 얼마나 대표하는가 | 샘플 대표성과 운영 조건 편향 | Python 예제 있음 | 대표성 편향이 있는 train set과 균형 test set을 만들고 `DummyClassifier`와 간단한 classifier의 그룹별 오류율을 비교한다 |
| 높음 | P3-6.1 비교할 구조는 어떤 특징으로 남기는가 | 구조를 feature로 바꾸는 기준 | 수작업 feature 계산 예제 있음 | 평균만 쓰는 모델과 변화·변동성 feature를 추가한 모델의 예측 오류를 비교해, feature 설계가 모델 출력 차이로 이어짐을 보인다 |
| 중간 | P3-6.2 특징만으로 부족할 때 어떤 중간 표현을 더 둘 수 있는가 | 사람이 만든 feature와 중간 표현 | Python 예제 있음 | `TfidfVectorizer` 또는 간단한 embedding/vectorizer로 원문 표현과 수작업 feature를 비교하고, 후보 순위가 어떻게 달라지는지 확인한다 |
| 중간 | P3-6.5 서로 단위와 크기가 다른 특징은 어떻게 함께 읽고 남기는가 | 스케일 차이와 feature 해석 | 코드 없음 | `StandardScaler` 전후로 k-NN 또는 logistic regression 결과가 달라지는 작은 예제를 넣는다 |
| 높음 | P3-8.6 확정 라벨이 검토된 사례에만 남아 있다면 해석에서 무엇을 함께 적어야 하는가 | selective labels와 해석 편향 | 코드 없음 | 검토된 일부 사례만 label이 있는 데이터로 classifier를 학습했을 때 전체 후보군에서 오류가 어떻게 치우치는지 비교한다 |
| 높음 | P3-9.7 입력과 결과는 어떤 조건이 닫혀야 예측 문제로 읽을 수 있는가 | feature/target, leakage, cutoff/horizon 계약 | 코드 없음 | 미래 정보가 섞인 feature를 넣은 모델과 cutoff 이전 feature만 쓴 모델의 train/test 성능 차이를 비교해 leakage를 직접 보인다 |
| 높음 | P3-9.12 같은 target 이름이라도 어떤 오류가 더 아픈지 왜 먼저 적어야 하는가 | target과 오류 비용의 비대칭성 | 코드 없음 | 같은 예측 확률에 서로 다른 threshold와 cost matrix를 적용해 false positive/false negative 비용이 달라지는 것을 출력한다 |

## Part 4 후보

Part 4는 머신러닝 모델 자체가 중심이므로 실제 모델 실행을 가장 적극적으로 쓸 수 있다. 이미 Python 예제가 있는 Section도 많지만, 일부는 수작업 계산이나 개념 표 중심이므로 scikit-learn 기반 실험으로 바꾸거나 보강할 가치가 있다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실제 모델 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P4-5.1 과적합과 과소적합 | train score와 validation score의 패턴 | 코드 없음 | `DecisionTreeClassifier(max_depth=...)` 또는 polynomial regression으로 underfit/fit/overfit의 train/validation 점수 패턴을 비교한다 |
| 높음 | P4-5.2 일반화 | 새 데이터에서 버티는가 | 코드 없음 | train/test split을 여러 seed로 바꾸며 validation score 분산과 generalization gap을 비교한다 |
| 높음 | P4-6.4 ROC, PR, log loss, calibration, silhouette | 단일 accuracy 밖의 평가 지표 | 코드 없음 | `sklearn.metrics`로 ROC-AUC, PR-AUC, log_loss, calibration curve, silhouette score를 한 번에 비교하는 작은 예제를 둔다 |
| 높음 | P4-7.4 필터, 래퍼, 차원 축소 | feature selection 방식 차이 | 코드 없음 | `SelectKBest`, `RFE`, `PCA`를 같은 데이터에 적용해 남는 feature와 validation score 차이를 비교한다 |
| 높음 | P4-8.1 모델 선택 | 문제에 맞는 모델 비교 | 코드 없음 | 같은 데이터에 logistic regression, k-NN, tree, random forest를 cross-validation으로 비교한다 |
| 높음 | P4-8.2 기준 모델(baseline) | 모델 성능의 최소 비교선 | 코드 없음 | `DummyClassifier`/`DummyRegressor`와 실제 모델을 비교해 baseline보다 못한 모델을 걸러낸다 |
| 중간 | P4-9.2 튜닝과 검증 비용 | 후보 조합과 검증 반복 비용 | GridSearchCV 예제 있음 | 이미 적절하나, `n_candidates`, `cv`, 실행 시간 또는 로그 수를 함께 출력해 비용 감각을 더 강화할 수 있다 |
| 중간 | P4-12.3 k-NN을 사용할 때 무엇을 먼저 점검할까 | k, scale, distance, 데이터 크기 점검 | 코드 없음 | `KNeighborsClassifier`에서 k와 scaling을 바꿔 decision boundary 또는 최근접 이웃 목록이 바뀌는 예제를 둔다 |
| 높음 | P4-17.2 군집 결과를 해석할 때의 주의점 | 군집은 정답 label이 아니다 | 코드 없음 | `KMeans`/`DBSCAN` 결과를 실제 label 또는 업무 그룹과 비교해, 군집 번호가 정답명이 아님을 보여 준다 |
| 중간 | P4-18.2 시각화와 정보 손실 | 차원 축소 시각화의 손실 | Python 예제 있음 | PCA 2D 시각화 뒤 원래 차원에서 가까운 점과 2D에서 가까운 점이 달라지는 사례를 scikit-learn으로 보강한다 |
| 중간 | P4-19.4 DQN, PPO, RLHF를 강화학습 큰 흐름 안에서 읽기 | 강화학습 계열 구분 | 코드 없음 | 큰 RL 라이브러리보다 간단한 bandit 또는 gridworld policy update simulation을 넣어 value/policy 차이를 보인다 |
| 중간 | P4-19.6 policy gradient와 likelihood ratio trick | policy gradient 직관 | Python 예제 있음 | 현재 수식 중심이면 작은 bandit policy gradient simulation으로 reward 분포와 update 방향을 보여 준다 |

## Part 5 후보

Part 5는 딥러닝 계산 흐름이 중심이므로 작은 PyTorch 또는 TensorFlow 예제가 학습 효과를 크게 높일 수 있다. 다만 초심자에게 프레임워크 문법이 중심이 되지 않게, 출력은 loss, gradient, parameter 변화, train/eval 차이, hidden representation 변화처럼 Section 중심축에 묶어야 한다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실제 모델 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P5-6.1 학습 루프 | forward, loss, backward, optimizer step | 수작업 학습 루프 예제 있음 | PyTorch의 작은 `nn.Linear` 모델로 `zero_grad -> forward -> loss -> backward -> step` 전후 parameter와 gradient를 출력한다 |
| 높음 | P5-6.4 학습 모드와 평가 모드 | train/eval mode 차이 | Python 예제 있음 | PyTorch `Dropout` 또는 `BatchNorm1d`를 같은 입력에 적용해 `model.train()`과 `model.eval()` 출력 차이를 비교한다 |
| 높음 | P5-7.1 옵티마이저의 역할 | gradient를 실제 update로 바꾸는 주체 | Python 예제 있음 | SGD optimizer가 `backward()` 뒤에도 parameter를 바꾸지 않고 `step()`에서만 바꾸는 것을 PyTorch로 확인한다 |
| 높음 | P5-7.2 학습률과 update 보폭 | learning rate가 이동량을 바꿈 | Python 예제 있음 | 같은 모델과 gradient에서 learning rate만 바꿔 loss trajectory와 overshoot를 비교한다 |
| 중간 | P5-7.3 Adam 직관 | 적응형 update | Python 예제 있음 | SGD와 Adam을 같은 작은 회귀 문제에 적용해 초기 update와 loss 감소 곡선 차이를 비교한다 |
| 높음 | P5-8.1 정규화 | 목적 함수 제약과 일반화 | Python 예제 있음 | L2 weight decay 유무에 따른 train/validation loss와 weight norm 변화를 작은 MLP로 비교한다 |
| 높음 | P5-8.2 드롭아웃 | 일부 경로를 흔들어 과의존을 줄임 | dropout 로그 예제 있음 | 실제 `nn.Dropout`으로 train mode의 무작위 출력과 eval mode의 안정 출력을 비교한다 |
| 중간 | P5-8.3 초기화, 수치 안정성, batch normalization | 깊은 계산 안정화 조건 | 코드 없음 | 작은 deep MLP에서 초기화 scale과 BatchNorm 유무에 따른 activation 분포를 비교한다 |
| 중간 | P5-10.1 표현 학습 | 사람이 만든 feature와 학습된 표현 비교 | Python 예제 있음 | 작은 MLP의 hidden layer 출력으로 class가 더 잘 분리되는지 PCA/산점도 또는 거리로 확인한다 |
| 중간 | P5-10.2 깊은 층의 표현 | 층을 거치며 표현 공간이 바뀜 | Python 예제 있음 | 학습 전후 hidden representation을 층별로 출력하거나 시각화해, 깊은 층이 구분을 어떻게 바꾸는지 본다 |
| 높음 | P5-11.1 CNN 직관 | 지역 패턴을 읽는 구조 | Python 예제 있음 | `nn.Conv2d` 작은 필터로 이미지 패치 반응을 출력해 지역 패턴 감지를 확인한다 |
| 높음 | P5-11.2 합성곱과 풀링 | convolution과 pooling의 역할 | Python 예제 2개 있음 | 실제 `Conv2d`와 `MaxPool2d`를 함께 써서 위치 이동에 대한 반응과 feature map 크기 변화를 출력한다 |
| 중간 | P5-12.1 RNN/LSTM/GRU 필요성 | 순서와 상태 전달 | Python 예제 있음 | PyTorch `nn.RNN` 또는 `nn.GRU`로 같은 토큰이라도 앞선 상태에 따라 hidden state가 달라지는지 확인한다 |
| 중간 | P5-12.2 장기 의존성 | 먼 정보 보존의 어려움 | Python 예제 있음 | 단순 RNN과 LSTM의 긴 sequence 기억 성능을 아주 작은 synthetic task로 비교한다 |
| 중간 | P5-13.1 attention 직관 | 필요한 위치를 더 크게 본다 | Python 예제 있음 | 실제 scaled dot-product attention으로 query가 바뀔 때 attention weight와 weighted sum이 달라지는지 출력한다 |
| 중간 | P5-14.2 Transformer 블록의 네 부품 | attention, FFN, residual, normalization | Python 예제 있음 | `nn.TransformerEncoderLayer` 또는 축약 block으로 입력 shape, attention output, residual 후 값을 단계별로 보여 준다 |
| 높음 | P5-15.3 샘플링은 후보 분포에서 실제 출력을 어떻게 꺼내는가 | temperature, top-k, sampling 변화 | Ollama 또는 sampling 예제 있음 | local LLM 또는 고정 logits에서 temperature/top-k/top-p를 바꿔 생성 후보 다양성과 반복성을 비교한다 |

## Part 6 후보

Part 6은 LLM과 생성형 AI 시스템이 중심이므로 실제 모델 또는 시스템에 가까운 실행을 다양하게 활용하는 편이 좋다. 단, 외부 API 과금과 최신성 의존이 크면 local LLM, tokenizer/vectorizer, mock tool result, 저장된 CSV 로그로 축약한다.

| 우선순위 | Section | 중심축 | 현재 상태 | 추천 실제 모델 실험 |
| --- | --- | --- | --- | --- |
| 높음 | P6-2.3 토큰화는 무엇을 바꾸는가 | 문자열이 token으로 쪼개지는 방식 | 코드 없음 | 실제 tokenizer로 한국어, 영어, 숫자, 공백, 이모지 입력의 token 수와 token ID 차이를 출력한다 |
| 중간 | P6-2.5 토크나이저 계열 차이 | tokenizer family 차이 | Python 예제 있음 | 기존 예제를 실제 tokenizer 라이브러리 기반으로 확장해 BPE/SentencePiece 계열 차이를 비교한다 |
| 높음 | P6-3.1 임베딩은 토큰 ID를 어떻게 비교 가능한 좌표로 바꾸는가 | token ID와 embedding vector의 차이 | 코드 없음 | 작은 embedding layer 또는 sentence embedding 모델로 ID 순서와 vector similarity가 다름을 보여 준다 |
| 높음 | P6-3.2 가까운 벡터는 왜 정답이 아니라 후보인가 | similarity는 후보 신호 | 코드 없음 | 실제 embedding/vectorizer로 query와 문서 후보 순위를 만들고, 가까운 후보 중 오답 후보를 함께 보여 준다 |
| 중간 | P6-4.2 attention은 context window 안에서만 무엇을 볼 수 있는가 | context window와 attention 범위 | Python 예제 있음 | 작은 attention mask 예제 또는 tokenizer 길이 초과 예제로 window 밖 정보가 반영되지 않는 구조를 보여 준다 |
| 중간 | P6-4.4 KV cache는 반복 생성에서 무엇을 다시 계산하지 않는가 | 반복 생성의 cache | Python 예제 있음 | local transformer를 직접 쓰기보다 mock cache 또는 작은 decoder block으로 token별 재계산량 차이를 출력한다 |
| 높음 | P6-6.1 다음 토큰 예측은 어떻게 긴 생성의 출발점이 되는가 | next-token prediction과 긴 생성 | Python 예제 있음 | local LLM 또는 고정 logits에서 한 step 예측이 다음 입력으로 누적되는 과정을 출력한다 |
| 높음 | P6-6.2 출력 선택 규칙은 왜 답변의 안정성과 다양성을 바꾸는가 | greedy, sampling, temperature | Python 예제 있음 | local LLM 또는 고정 logits로 temperature/top-k를 바꿔 동일 prompt의 반복 출력 차이를 비교한다 |
| 높음 | P6-9.1 지시 튜닝은 어떻게 요청 형식에 맞는 응답 습관을 만드는가 | 요청 형식 준수 | CSV 평가 예제 있음 | local LLM 또는 저장된 응답 로그로 일반 prompt와 구조화 prompt의 format compliance를 비교한다 |
| 높음 | P6-9.2 정렬은 왜 잘 따르는 답과 허용 가능한 답을 나누는가 | helpfulness, safety, factuality 균형 | Python 예제 있음 | 실제 생성 후보를 여러 개 만든 뒤 간단한 평가 축으로 자동 점검하고, 안전 기준에서 탈락하는 후보를 보여 준다 |
| 중간 | P6-10.1 프롬프트 엔지니어링은 무엇을 입력에서 조정하는가 | prompt가 출력 형식과 근거 사용을 바꿈 | Ollama 예제 있음 | 이미 방향이 좋다. prompt template, structured prompt, constraint prompt를 같은 local LLM에 넣어 결과 차이를 더 체계화한다 |
| 높음 | P6-10.3 CoT와 self-consistency | 답변 경로와 후보 합의 관찰 | 비코드 연습 | local LLM 또는 저장된 생성 로그로 같은 질문을 여러 번 생성해 결론 분포와 소수 경로를 비교한다 |
| 중간 | P6-10.4 automatic prompt optimization | prompt 실험 반복 개선 | 코드 없음 | 외부 최적화 대신 작은 prompt 후보 집합과 평가 함수로 prompt score가 반복 개선되는 loop를 보여 준다 |
| 높음 | P6-11.1 RAG는 왜 답변 전에 외부 근거를 붙이는가 | 검색 전후 근거 연결 | TF-IDF 예제 있음 | 현재 예제는 좋다. 가능하면 sentence embedding 또는 vectorizer를 선택적으로 추가해 lexical retrieval과 semantic retrieval 차이를 비교한다 |
| 높음 | P6-11.2 검색 결과는 어떻게 생성 입력과 답변으로 이어지는가 | retrieval failure와 generation failure 분리 | Python 예제 있음 | retrieved docs와 generated answer를 실제 local LLM 또는 mock generator로 연결해 잘못 검색된 문서가 답에 새는 과정을 보여 준다 |
| 높음 | P6-12.1 벡터 데이터베이스 | vector, 원문, metadata payload | Python 예제 있음 | actual vector store는 부담이 크면 FAISS 또는 sklearn NearestNeighbors로 payload 보존과 top-k 변화를 보여 준다 |
| 높음 | P6-12.2 인덱스와 검색 품질 | speed와 후보 품질 trade-off | Python 예제 있음 | `NearestNeighbors` brute force와 approximate 후보 축소를 비교해 검색 시간, recall@k, 누락 사례를 출력한다 |
| 중간 | P6-13.1 도구 사용 | 실제 조회·계산·실행 필요성 | mock tool 예제 있음 | 실제 외부 API 대신 계산기, 날짜 변환, CSV 조회 tool을 함수로 두고 LLM 판단 또는 rule planner가 언제 호출하는지 비교한다 |
| 중간 | P6-13.2 함수 호출 | 자연어 요청을 함수 이름과 인자로 나눔 | Python 예제 있음 | JSON schema validation 또는 pydantic으로 missing argument, wrong type, executable payload를 확인한다 |
| 높음 | P6-16.1 LLM 평가 | 자연스러운 답과 품질 축 분리 | Python 예제 있음, 정답 확인형 개선 필요 | 실제 local LLM 응답 후보 또는 저장된 model output을 평가해 correctness, groundedness, format, helpfulness가 서로 다르게 실패하는 사례를 만든다 |
| 높음 | P6-16.2 자동 평가와 사람 평가 | automatic gate와 human judgment 분업 | Python 예제 있음, 정답 확인형 개선 필요 | 자동 평가가 통과시키지만 사람 검토가 필요한 실제 출력 후보를 만들고, 자동 기준의 false positive/false negative를 집계한다 |
| 중간 | P6-20.1 BERT 계열 | 읽기 중심 encoder와 생성 중심 decoder 비교 | 코드 없음 | 작은 sentence-transformer 또는 vectorizer 기반 intent classification/retrieval 예제로 키워드 규칙과 읽기 중심 표현을 비교한다 |
| 중간 | P6-20.2 이해 중심 태스크 | 라벨, 관계 점수, 랭킹 출력 | Python 예제 있음 | 현재 keyword rule 예제를 실제 classifier/vectorizer/ranker로 바꾸면 BERT 계열의 역할이 더 선명해진다 |

## 우선 작업 묶음

후속 수정은 모든 후보를 한 번에 바꾸기보다 다음 순서가 적절하다.

1. Part 4의 모델 기본 개념: P4-5.1, P4-5.2, P4-6.4, P4-8.2  
   실제 모델 실행이 가장 자연스럽고, scikit-learn으로 작게 닫을 수 있다.
2. Part 5의 학습 루프와 모드 차이: P5-6.1, P5-6.4, P5-7.1, P5-8.2  
   PyTorch 작은 모델을 쓰면 수작업 계산보다 딥러닝 프레임워크 감각이 살아난다.
3. Part 6의 토큰화, 생성 선택, RAG, 평가: P6-2.3, P6-6.2, P6-11.1, P6-16.1, P6-16.2  
   생성형 AI 구간에서 실제 모델·시스템 출력이 가장 직접적으로 학습 효과를 만든다.
4. Part 3의 데이터 계약 예제: P3-4.2, P3-9.7, P3-9.12  
   모델 성능 경쟁이 아니라 데이터 계약 오류가 모델 평가를 왜곡한다는 점을 보여 주는 축약 실험으로 설계한다.

## 보류 또는 주의할 Section 유형

다음 Section은 실제 모델을 무조건 붙이기보다 신중히 본다.

- 개념 정의나 역사적 비교가 중심인 Section: 모델 실행이 본문 중심축을 흐릴 수 있다.
- Part 6의 외부 API·최신 제품 기능 의존 Section: 과금, 계정, 네트워크, 최신성 확인이 중심이 되면 본문 예제가 아니라 프로젝트나 보충 자료로 넘긴다.
- 강화학습 고급 보충 Section: 실제 RL 라이브러리는 설치와 실행 로그가 커지므로 bandit/gridworld simulation 정도가 적절하다.
- BERT·embedding 계열 Section: 외부 모델 다운로드가 필요하면 네트워크 의존을 피하기 위해 vectorizer나 저장된 embedding을 우선 검토한다.

## 검토 결론

Part 3 이후에는 실제 모델 예제를 더 적극적으로 쓸 여지가 크다. 특히 Part 4는 scikit-learn 기반 모델 실험, Part 5는 작은 PyTorch 학습 루프, Part 6은 tokenizer/vectorizer/local LLM/RAG/evaluation 출력이 Section 중심축을 더 잘 보여 준다.

다만 실제 모델 예제는 `모델을 돌렸다`에서 끝나면 학습 효과가 약하다. 각 후보 Section에서 반드시 같이 남겨야 할 것은 다음 세 가지다.

1. 독자가 바꿀 값: split, feature, threshold, hyperparameter, prompt, decoding setting 등
2. 관찰할 출력: 예측 샘플, 오류 사례, 후보 순위, train/validation gap, retrieved document, generated text 차이 등
3. Section 중심축으로 닫는 해설: 왜 그 출력 차이가 현재 절의 핵심 질문을 확인해 주는가
