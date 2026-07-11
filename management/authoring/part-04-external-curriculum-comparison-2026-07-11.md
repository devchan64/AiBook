# Part 4 외부 커리큘럼 비교 메모

작성일: 2026-07-11

이 문서는 Part 4 `머신러닝` 파트가 외부 머신러닝 입문 커리큘럼과 비교해 어떤 축에서 표준 범위와 맞고, 어떤 축에서 의도적으로 넓어지거나 좁아졌는지 점검하기 위한 내부 메모다.

이번 비교의 목적은 `외부 목차를 그대로 따라가기`가 아니라, 현재 Part 4가 초심자 기준에서 필요한 핵심 설명을 빠뜨리지 않았는지 확인하고 후속 보강 우선순위를 정하는 데 있다.

## 비교에 사용한 외부 기준

이번 비교는 가능한 한 1차 자료나 공식 교육 자료만 사용했다.

### 1. Stanford CS229

- 자료: Stanford `CS229: Machine Learning`
- URL: https://cs229.stanford.edu/
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - course description의 `supervised learning`
  - `unsupervised learning`
  - `learning theory`
  - `bias/variance tradeoffs`
  - `practical advice`
  - `reinforcement learning and adaptive control`

### 2. scikit-learn User Guide

- 자료: scikit-learn `User Guide`
- URL: https://scikit-learn.org/stable/user_guide.html
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - `Supervised learning`
  - `Unsupervised learning`
  - `Model selection and evaluation`
  - `Dataset transformations`
  - `Common pitfalls and recommended practices`
  - `Choosing the right estimator`

### 3. An Introduction to Statistical Learning

- 자료: Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, `An Introduction to Statistical Learning`
- URL: https://www.statlearning.com/
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - `What is statistical learning?`
  - `Regression`
  - `Classification`
  - `Resampling methods`
  - `Linear model selection and regularization`
  - `Tree-based methods`
  - `Support vector machines`
  - `Unsupervised learning`

### 4. DeepLearning.AI Machine Learning Specialization

- 자료: DeepLearning.AI `Machine Learning Specialization`
- URL: https://www.deeplearning.ai/specializations/machine-learning
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - `Supervised Machine Learning: Regression and Classification`
  - `Advanced Learning Algorithms`
  - `Advice for applying machine learning`
  - `Decision trees`
  - `Tree ensembles`
  - `Unsupervised learning`
  - `Anomaly detection`
  - `Principal Component Analysis`
  - `Reinforcement learning`

## 외부 기준에서 반복해서 보이는 공통 뼈대

외부 기준을 묶어 보면, 머신러닝 입문 커리큘럼의 공통 뼈대는 대체로 다음 순서로 반복된다.

1. 지도학습, 비지도학습, 강화학습 같은 큰 문제 유형 구분
2. train/validation/test, bias-variance, generalization 같은 검증 구조
3. metrics, resampling, model selection, hyperparameter tuning
4. preprocessing, feature selection, leakage 방지 같은 입력 준비
5. 대표 알고리즘군 비교
6. clustering, dimensionality reduction, anomaly detection 같은 비지도 계열
7. practical advice, pitfalls, computational trade-off

Part 4는 이 큰 줄기를 거의 모두 포함한다.

## 현재 Part 4와의 대응 표

외부 기준과 현재 Part 4를 빠르게 대조하려면 아래 표처럼 보는 편이 가장 명확하다.

| 외부 커리큘럼 공통 축 | 현재 Part 4 대응 위치 | 현재 판단 |
| --- | --- | --- |
| 지도/비지도/강화학습의 큰 구분 | P4-2.1 ~ P4-2.3 | 표준 입문 범위와 잘 맞는다. |
| 휴리스틱, practical advice, 모델 선택 전 판단 | P4-3.1, P4-3.2 | 외부 기준보다 앞단 설명이 더 두텁다. |
| train/validation/test | P4-4.1, P4-4.2 | 표준 구조와 잘 맞는다. |
| bias/variance, overfitting/generalization | P4-5.1, P4-5.2 | CS229, ISLR 기준과 직접 대응된다. |
| metrics, evaluation, threshold, calibration 입문 | P4-6.1 ~ P4-6.4 | 외부 기준보다 운영 판단 연결이 더 강하다. |
| preprocessing, feature selection, leakage, pipeline 감각 | P4-7.1 ~ P4-7.4 | scikit-learn 실무 지침과 특히 잘 맞는다. |
| model selection, baseline, hyperparameter tuning | P4-8.1 ~ P4-9.3 | 표준 범위와 잘 맞고, baseline 축이 특히 선명하다. |
| 대표 회귀/분류 알고리즘군 | P4-10.1 ~ P4-16.3 | 선형회귀, 로지스틱, k-NN, SVM, 트리, 앙상블을 모두 포함한다. |
| clustering | P4-17.1 ~ P4-17.4 | 표준 범위와 잘 맞는다. |
| dimensionality reduction / PCA | P4-18.1, P4-18.2 | 표준 범위와 맞고, 현재 책에서는 비지도 해석 축이 더 강하다. |
| anomaly detection | P4-2.2 도입부와 사례들에 분산 | 완전 부재는 아니지만 독립 회수 절은 없다. |
| reinforcement learning | P4-19.1 ~ P4-19.6 | 현대 ML 입문 강의 축과는 잘 맞고, 통계 입문서보다 넓다. |

이 표를 기준으로 보면 현재 Part 4의 핵심 문제는 `큰 범위 누락`보다 `어떤 항목을 별도 절로 다시 회수할 필요가 있는가`에 더 가깝다.

## Part 4와 잘 맞는 축

### 1. 알고리즘보다 문제 구조와 검증 구조를 먼저 세운 점

Part 4는 `학습 유형 -> 휴리스틱 -> 데이터 분리 -> 과적합/일반화 -> 평가 지표 -> 입력 준비 -> 모델 선택 -> baseline -> 튜닝 -> 대표 알고리즘군` 순서로 간다.

이 순서는 ISLR이나 DeepLearning.AI처럼 알고리즘을 더 빨리 소개하는 입문 커리큘럼보다 앞단 설명이 두텁다. 하지만 초심자 기준에서는 오히려 장점이다. 현재 책의 독자는 `모델 이름`보다 먼저 `무엇을 비교하고 무엇을 검증하는가`를 잡아야 하기 때문이다.

특히 P4-4부터 P4-9까지의 구조는 scikit-learn User Guide의 `Model selection and evaluation`, `Dataset transformations`, `Common pitfalls` 축과도 잘 맞는다.

### 2. 일반화, 검증, baseline을 Part의 중심축으로 둔 점

CS229는 course description에서 `learning theory`, `bias/variance tradeoffs`, `practical advice`를 명시한다. ISLR도 `Resampling methods`를 별도 장으로 둔다. DeepLearning.AI도 `Advice for applying machine learning`, `Bias and variance`, `Machine learning development process`를 따로 둔다.

Part 4 역시 `검증/테스트`, `과적합/과소적합`, `일반화`, `평가 지표`, `baseline`, `튜닝 비용`을 알고리즘 장 앞에서 충분히 다룬다. 이 점은 외부 기준과 비교해도 강한 축이다.

### 3. 대표 고전 모델군의 선택은 표준 범위 안에 있다

scikit-learn User Guide와 ISLR, DeepLearning.AI를 함께 보면 입문자가 반복해서 만나는 대표 모델군은 대체로 다음과 같다.

1. 선형회귀
2. 로지스틱 회귀
3. k-NN
4. SVM
5. 결정트리
6. 랜덤포레스트와 부스팅 같은 트리 앙상블
7. clustering
8. dimensionality reduction

Part 4는 이 범위를 모두 포함한다. 따라서 `대표적인 전통 머신러닝 계열을 빠뜨렸다`고 보기는 어렵다.

### 4. 비지도학습과 강화학습을 끝에 배치한 구조도 외부 기준과 호환된다

CS229와 DeepLearning.AI는 모두 지도학습 이후에 비지도학습과 강화학습을 배치한다. Part 4도 같은 큰 흐름을 따른다.

특히 강화학습을 Part 4 끝에 두는 결정은 `학습 유형 3분류`를 초반에 소개한 뒤, 실제 대표 알고리즘군을 모두 본 후 다시 큰 유형 하나를 회수한다는 점에서 교육적으로 일관성이 있다.

### 5. 전처리, 특징 선택, 누수 방지를 별도 장으로 다룬 점

scikit-learn User Guide는 `Preprocessing data`, `Imputation of missing values`, `Feature selection`, `Pipelines`, `Data leakage during pre-processing`를 별도 지침으로 강하게 다룬다.

Part 4도 P4-7.1과 P4-7.2에서 이 축을 별도 Chapter로 떼어 다룬다. 외부 입문 교재 중 일부는 이 내용을 실습 도중에 흩어 다루는데, 현재 책처럼 전처리와 leakage를 독립 주제로 먼저 세우는 방식은 초심자에게 오히려 안전하다.

## 외부 기준보다 상대적으로 약하거나 의도적으로 다른 축

### 1. anomaly detection이 독립 장으로는 서지 않는다

DeepLearning.AI는 `Unsupervised learning` 주차 안에 `Anomaly detection`을 독립 항목으로 둔다. scikit-learn도 `Novelty and Outlier Detection`을 비지도학습의 독립 범주로 둔다.

현재 Part 4는 anomaly detection을 완전히 빠뜨린 것은 아니다.

- P4-2.2에서 비지도학습 대표 문제로 소개한다.
- 여러 예시와 표에서 점검 후보 구조로 계속 언급한다.
- 일부 모델 절에서도 이상 탐지 예시를 쓴다.

하지만 외부 커리큘럼과 비교하면 `군집화나 차원 축소처럼 다시 돌아와 한 번 더 다루는 장`은 없다. 따라서 현재 상태는 `부재`보다 `압축`에 가깝지만, 입문 커리큘럼의 대표 축으로 보겠다면 별도 보충학습 후보로 남길 가치가 있다.

### 2. Naive Bayes, LDA/QDA 같은 생성 분류기 계열은 의도적으로 얇다

CS229 course description에는 `generative learning`이 직접 들어간다. scikit-learn User Guide는 `Naive Bayes`, `Linear and Quadratic Discriminant Analysis`를 대표 감독학습 범주로 별도 둔다.

현재 Part 4는 이 계열을 직접 장으로 세우지 않는다. 본문 안에서 Fisher 판별이나 Bayes 분류기 전통을 짧게 언급하는 정도다.

이것은 지금 Part 4의 중심 질문과는 충돌하지 않는다. 현재 Part 4는 `초심자가 먼저 비교해야 하는 대표 모델군`을 좁게 잡아 설명 밀도를 확보하는 편집을 택하고 있기 때문이다. 다만 외부 기준과 비교하면 이 omission은 명시적으로 기록해 두는 편이 낫다. 그래야 나중에 `빠진 내용`인지 `범위 제한`인지 혼동하지 않는다.

### 3. PCA와 차원 축소의 위치는 외부 기준보다 뒤에 있다

DeepLearning.AI는 `Unsupervised learning` 코스 안에서 clustering 뒤에 `Principal Component Analysis`를 둔다. scikit-learn는 `Dataset transformations`와 `Unsupervised dimensionality reduction`에서도 PCA를 반복해서 호출한다.

현재 Part 4는 차원 축소를 Chapter 18에서, clustering 뒤쪽에 둔다. 이 배치는 크게 어색하지 않다. 다만 외부 기준보다 `전처리 도구`보다는 `비지도 구조 해석 도구`로 더 강하게 읽히게 만든다.

따라서 이 차이는 `순서 오류`라기보다 `강조점 차이`에 가깝다. 대신 P4-7.4에서 차원 축소를 처음 구분할 때 `여기서는 입력 준비 관점으로 살짝만 보고, 본격 해석은 P4-18에서 다시 본다`는 연결을 더 또렷하게 둘 여지는 있다.

### 4. reinforcement learning은 ISLR류 통계 입문서보다 넓은 범위다

ISLR의 공개 소개 페이지에 나열된 장 목록에는 reinforcement learning이 없다. 반면 CS229와 DeepLearning.AI에는 reinforcement learning이 들어간다.

즉, 현재 Part 4의 강화학습 포함은 `통계학 중심 입문서`보다는 `현대 ML 입문 강의` 쪽에 더 가깝다. 이것은 현재 책 전체 구조에서는 장점에 가깝다. Part 1에서 이미 학습 유형의 큰 구분을 소개했기 때문에, Part 4 말미에서 가치 기반, 정책 기반, 적용 주의점을 다시 다루는 편이 학습 유형 구조를 닫아 주기 때문이다.

## 커리큘럼 적합성 판단

### 전체 판단

현재 Part 4는 외부 머신러닝 입문 커리큘럼과 비교했을 때 `큰 구조는 적합하고, 초심자용 문제 구조 설명은 오히려 더 강한 편`이다.

즉, 지금 상태를 `대표 범위가 잘못 잡혔다`고 볼 근거는 약하다.

### 가장 중요한 강점

- 검증, 일반화, baseline, tuning을 알고리즘 장보다 앞에 두어 초심자 관점에서 더 안전하다.
- 대표 고전 모델군의 선택이 표준 입문 범위를 벗어나지 않는다.
- preprocessing, leakage, threshold, calibration을 `문제 적용 판단`과 연결해 읽게 만드는 편집 방향이 외부 실무형 자료와 잘 맞는다.
- clustering, dimensionality reduction, reinforcement learning까지 이어지므로 `머신러닝 전체 지도`를 닫는 힘이 있다.

### 가장 중요한 리스크

외부 기준과 비교했을 때 가장 먼저 눈에 띄는 리스크는 다음 셋이다.

1. anomaly detection이 별도 장 없이 비지도학습 도입부와 예시들 속에 흩어져 있다.
2. Naive Bayes, LDA/QDA 같은 생성 분류기 omission이 의도적 범위 제한인지 독자에게는 아직 선명하지 않을 수 있다.
3. PCA와 차원 축소가 `입력 준비 도구`인지 `비지도 구조 해석 도구`인지 초반 연결 문장이 더 분명할수록 좋다.

## 권장 후속 조치

이번 비교 뒤 현재 기준에서 가장 현실적인 정리는 다음과 같다.

1. `anomaly detection`은 새 Chapter를 만들기보다, 필요 시 Chapter 17 아래 짧은 보충학습 1개로 보강하는 쪽이 적절하다.
2. `Naive Bayes / LDA / QDA`는 현 단계 Part 4 대표 장으로 올리지 않고, `의도적 범위 제한`으로 명시하는 쪽이 적절하다.
3. 차원 축소는 계속 `비지도 구조 해석` 축을 중심으로 두고, P4-7.4에서는 `입력 준비에서 잠깐 만나는 다른 갈래`로만 연결하는 편이 적절하다.

이 판단의 이유는 다음과 같다.

- anomaly detection은 이미 P4-2.2에서 비지도학습의 대표 문제로 소개되고, 여러 예시와 절에서 점검 후보 관점이 반복된다. 따라서 `완전한 공백`은 아니다. 다만 clustering과 dimensionality reduction처럼 `한 번 더 돌아와 해석 기준을 세우는 자리`가 없으므로, 보강이 필요하다면 별도 Chapter보다 짧은 보충학습이 균형에 맞다.
- Naive Bayes와 LDA/QDA는 외부 기준에서는 대표 범주이지만, 현재 Part 4의 핵심 편집 원리는 `초심자가 먼저 비교해야 하는 모델군을 좁혀 설명 밀도를 확보하는 것`이다. 현재 목차에 이 계열을 넣으면 `경계`, `이웃`, `트리`, `앙상블`로 이어지는 주 비교축이 흐려질 가능성이 더 크다.
- 차원 축소는 외부 기준에서 전처리와 비지도학습 양쪽에 모두 나타나지만, 현재 본문을 다시 읽어 보면 P4-7.4가 이미 `특징 선택과 차원 축소의 차이`를 먼저 잡고 있고, P4-18.1이 `표현 다시 만들기`라는 본격 해석 책임을 진다. 따라서 현재 구조 문제는 `위치`보다 `연결 문장 선명도`에 가깝다.

## 현재 결정

이번 비교를 마친 현재 시점의 관리 기준은 다음과 같다.

- anomaly detection은 지금 당장 새 Chapter를 만들지 않는다.
- 다만 Part 4를 다시 읽다가 `이상치 후보가 왜 clustering, density, novelty 관점과 다르게 읽히는가`가 반복해서 막히면, Chapter 17 보충학습 1개를 우선 후보로 둔다.
- Naive Bayes, LDA, QDA는 현재 Part 4 본편 범위 밖에 둔다.
- 이 계열은 `대표 입문 모델을 다 빠짐없이 열거하지 않기로 한 편집 원칙` 아래에서 의도적으로 생략한 것으로 기록한다.
- 차원 축소는 현재처럼 Chapter 18의 `비지도 구조 해석과 재표현` 축을 중심 설명 위치로 유지한다.
- P4-7.4와 P4-18.1의 연결 문장은 이후 본문 수정 차수가 오면 다듬되, 지금 단계에서는 구조 변경보다 연결 명료화만 검토한다.

## 명시적 범위 밖 항목

현재 비교 기준으로 `지금 Part 4에 없지만 바로 결손으로 보지 않는 항목`은 다음처럼 정리할 수 있다.

| 항목 | 현재 처리 | 판단 이유 |
| --- | --- | --- |
| Naive Bayes | 본편 범위 밖 | 대표 모델군을 좁혀 설명 밀도를 유지하는 편집 원칙을 우선하기 때문 |
| LDA / QDA | 본편 범위 밖 | 로지스틱 회귀, SVM, k-NN, 트리 계열의 주 비교축을 먼저 세우는 편이 초심자에게 더 직접적이기 때문 |
| anomaly detection 독립 Chapter | 아직 만들지 않음 | 이미 P4-2.2와 여러 사례에 분산돼 있어 `완전 공백`은 아니기 때문 |
| PCA를 전처리 Chapter로 이동 | 하지 않음 | 현재 책에서는 `표현 다시 만들기`와 `비지도 구조 해석` 축이 더 자연스럽기 때문 |

즉, 이 항목들은 `빠뜨린 상태`보다 `현재 구조상 의도적으로 뒤로 미루거나 압축한 상태`로 기록하는 편이 맞다.

## 이번 검토의 결론

이번 외부 비교의 결론은 `Part 4가 외부 입문 커리큘럼보다 부족하다`가 아니라, `현재 구조는 충분히 경쟁력 있고, 다만 무엇을 의도적으로 생략했고 무엇을 압축했는지 더 명시하면 더 강해진다`에 가깝다.

특히 현재 Part 4의 가장 좋은 점은 알고리즘 나열보다 `문제 정의 -> 검증 -> 기준선 -> 비교 -> 적용 위험`을 반복하는 구조다. 이 축은 외부 자료를 그대로 따라가면 오히려 약해질 수 있으므로 유지하는 편이 맞다.
