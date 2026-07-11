# Part 4 보강 검토 메모

작성일: 2026-07-11

이 문서는 Part 4 `머신러닝` 파트의 외부 커리큘럼 비교 결과를 바탕으로, 실제 본문 보강 후보를 `우선순위`, `기대 효과`, `삽입 위치`, `권장 조치` 수준까지 좁혀 정리한 내부 메모다.

이번 문서의 목적은 `새 절을 많이 만들기`가 아니라, 현재 Part 4 구조를 유지하면서도 학습 공백을 가장 적은 비용으로 메울 수 있는 보강 순서를 정하는 데 있다.

## 검토 기준

이번 보강 검토는 다음 자료를 기준으로 했다.

- Stanford CS229: https://cs229.stanford.edu/
- scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- scikit-learn `Novelty and Outlier Detection`: https://scikit-learn.org/stable/modules/outlier_detection.html
- ISLR: https://www.statlearning.com/
- DeepLearning.AI Machine Learning Specialization: https://www.deeplearning.ai/specializations/machine-learning

특히 DeepLearning.AI는 `Unsupervised learning` 주차 안에 `Clustering`, `Anomaly detection`, `Principal Component Analysis`, `Reinforcement learning`을 함께 두고 있고, scikit-learn User Guide는 `Novelty and Outlier Detection`을 비지도학습의 독립 범주로 둔다. 따라서 Part 4 보강 검토에서는 `비지도 계열의 회수 밀도`가 핵심 확인 지점이었다.

## 현재 상태 요약

현재 Part 4는 큰 범위 기준으로는 충분히 강하다.

- 문제 유형 구분, 검증, 일반화, 평가, 입력 준비, baseline, tuning, 대표 알고리즘군, clustering, dimensionality reduction, reinforcement learning까지 모두 포함한다.
- 특히 `검증 -> 기준선 -> 비교 -> 적용 위험`을 알고리즘 장보다 앞에 두는 구조는 외부 입문 커리큘럼보다 초심자 친화적이다.

반면 `보강 후보`로 남는 것은 대체로 `큰 범위 누락`보다 `회수 밀도 부족`에 가깝다.

## 우선순위 결론

현재 기준에서 보강 후보 우선순위는 다음처럼 정리하는 편이 적절하다.

1. `anomaly detection` 보충학습 1개 검토
2. `차원 축소의 위치`는 구조 변경 없이 연결 문장 명료화만 검토
3. `Naive Bayes / LDA / QDA`는 보강 후보가 아니라 명시적 범위 제외로 유지

즉, 실제 본문 보강 대상으로 가장 진지하게 볼 항목은 현재로서는 `anomaly detection` 하나에 가깝다.

## 1순위 보강 후보: anomaly detection 보충학습

### 왜 이 후보가 가장 우선인가

현재 Part 4에는 anomaly detection이 완전히 없는 것은 아니다.

- P4-2.2에서 군집화, 차원 축소와 함께 대표 비지도 문제로 소개한다.
- 여러 예시 문맥에서 `이상치 후보`, `점검 후보` 관점이 계속 등장한다.
- SVM, 트리, 전처리 사례에서도 이상 탐지 장면을 간접적으로 호출한다.

하지만 clustering은 P4-17 전체에서 다시 회수되고, dimensionality reduction은 P4-18 전체에서 다시 회수되는 반면, anomaly detection은 `도입 후 다시 독립적으로 정리되는 자리`가 없다.

외부 기준도 이 차이를 뒷받침한다.

- DeepLearning.AI는 unsupervised learning 안에 `Anomaly detection`을 독립 항목으로 둔다.
- scikit-learn는 anomaly detection을 `outlier detection`과 `novelty detection`으로 나누어 설명한다.
- scikit-learn 문서는 `outlier detection`은 오염된 학습 데이터에서 중심 영역을 찾는 문제, `novelty detection`은 깨끗한 정상 데이터 밖의 새 관측을 찾는 문제로 구분한다.

현재 Part 4에서 가장 보강 가치가 큰 지점은 바로 이 구분이 본문 구조상 독립된 자리를 아직 못 가진다는 점이다.

### 무엇을 보강하면 좋은가

새 Chapter를 만드는 것보다, Chapter 17 아래 짧은 보충학습 1개로 다음 질문을 정리하는 편이 가장 균형이 좋다.

- `이상치(outlier)`와 `새로운 이상(novelty)`는 왜 같은 말이 아닌가?
- 군집화와 anomaly detection은 무엇이 다른가?
- 밀도 기반 이상, 거리 기반 이상, 규칙 위반 이상을 어떻게 다르게 읽는가?
- `점검 후보`와 `확정 이상`을 왜 구분해야 하는가?

이 보강은 P4-17.2 뒤 또는 P4-17.4 뒤에 붙는 것이 가장 자연스럽다.

### 권장 위치

- 1안: `P4-17.2` 뒤 보충학습 위치를 겨냥해 실제 번호는 `P4-17.5`로 추가
- 2안: `P4-17.4` 뒤에 새 보충학습 추가

현재 구조 기준으로는 `군집 해석의 주의점`을 먼저 본 뒤 anomaly detection으로 넘어가는 쪽이 가장 자연스럽다. 다만 기존 Section 번호 안정성을 생각하면, 실제 번호는 당장 밀지 않고 `P4-17.5`로 추가하는 편이 더 안전하다.

### 기대 효과

- 비지도학습 3대 대표 문제로 이미 소개한 anomaly detection이 Part 후반에서 다시 한 번 닫힌다.
- `cluster label`과 `anomaly flag`를 같은 종류의 출력으로 오해하는 위험을 줄일 수 있다.
- Part 4 후반의 `구조 찾기` Module이 clustering과 dimensionality reduction만으로 보이지 않게 된다.

### 비용 판단

중간 수준이다.

- 새 Chapter는 필요 없다.
- 새 Section 1개 정도면 충분하다.
- 기존 Module 6 구조를 깨지 않고 보강할 수 있다.
- 실제 절 설계 초안은 `2026-07-11-p4-17-anomaly-detection-section-design.md`에 별도 정리한다.

## 2순위 보강 후보: 차원 축소 연결 문장 명료화

### 현재 상태

차원 축소 자체는 이미 충분히 있다.

- P4-7.4에서 특징 선택과 차원 축소의 차이를 먼저 구분한다.
- P4-18.1, P4-18.2에서 PCA, 시각화, 정보 손실까지 다시 회수한다.

즉, 범위 부족 문제가 아니라 `독자가 전처리 도구와 비지도 해석 도구 사이의 위치를 혼동할 수 있는가`가 핵심이다.

### 무엇을 보강하면 좋은가

현재로서는 구조 변경보다 연결 문장 한두 개를 더 분명히 하는 정도면 충분하다.

예를 들면 다음 수준이다.

- P4-7.4에서 `여기서는 특징 선택과의 차이만 먼저 잡고, 본격 목적은 P4-18에서 다시 본다`
- P4-18.1에서 `Part 4에서는 차원 축소를 입력 압축 도구이기도 하지만, 더 강하게는 비지도 구조 해석 도구로 다시 읽는다`

### 권장 위치

- [docs/parts/part-04/chapter-07/section-04.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-07/section-04.md)
- [docs/parts/part-04/chapter-18/section-01.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-18/section-01.md)

### 기대 효과

- `PCA를 왜 전처리 장이 아니라 Module 6에서 다시 보는가`에 대한 독자의 혼란을 줄인다.
- 구조 변경 없이 현재 편집 의도를 더 선명하게 만든다.

### 비용 판단

낮다.

- 새 절 추가가 아니라 연결 문장 수정 수준이다.

## 보강 제외 유지: Naive Bayes / LDA / QDA

### 왜 보강 우선순위에서 내리는가

외부 기준에서는 분명 대표 항목이다.

- scikit-learn User Guide는 `Naive Bayes`, `Linear and Quadratic Discriminant Analysis`를 감독학습 장 아래 둔다.
- CS229 계열은 generative learning 전통을 직접 언급한다.

하지만 현재 Part 4의 중심 편집 원리는 `대표 모델군을 좁혀 밀도를 확보하는 것`이다. 이 구조에서 새 모델 계열을 더 넣으면 생기는 손해가 더 크다.

- 로지스틱 회귀, k-NN, SVM, 트리, 앙상블로 이어지는 주 비교축이 흐려진다.
- 새 모델을 넣는 순간 알고리즘 카탈로그처럼 보일 위험이 커진다.
- 현재 책의 초심자 기준에서는 `무엇을 먼저 비교하는가`보다 `빠진 모델 목록 채우기` 쪽으로 시선이 흔들릴 수 있다.

### 결론

이 계열은 `지금 당장 보강할 후보`가 아니라, `현재 범위 밖으로 명시해 두고 유지할 항목`으로 보는 편이 맞다.

## 권장 실행 순서

실제로 보강 작업까지 이어 간다면 순서는 다음이 가장 효율적이다.

1. Chapter 17에 anomaly detection 보충학습 1개 추가 여부를 먼저 검토한다.
2. 그다음 P4-7.4와 P4-18.1 연결 문장을 다듬을지 결정한다.
3. Naive Bayes / LDA / QDA는 별도 본문 추가 없이 관리 문서의 범위 결정만 유지한다.

## 최종 판단

현재 Part 4에서 `보강 검토`의 실질적 의미는 여러 알고리즘 이름을 더 넣는 일이 아니다. 가장 타당한 보강은 `비지도학습의 세 번째 축으로 이미 소개한 anomaly detection을 후반부에서 한 번 더 회수할지`를 결정하는 일이다.

따라서 지금 시점의 우선순위는 다음 한 문장으로 요약할 수 있다.

`Part 4 보강의 1순위는 anomaly detection 보충학습 후보 검토이고, 차원 축소는 연결 명료화 수준, 생성 분류기 계열은 범위 제외 유지가 적절하다.`
