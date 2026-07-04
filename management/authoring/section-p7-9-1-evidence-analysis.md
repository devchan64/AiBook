# P3-9.1 하이퍼파라미터(hyperparameter) 근거 검토

## 핵심 주장

### 1. 하이퍼파라미터는 추정기 내부에서 직접 학습되지 않는 설정값이다

- 근거:
  - scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`
- 반영 방식:
  - `하이퍼파라미터는 학습 전에 사람이 정하는 설정값`이라는 초심자용 정의로 일반화
  - 생성자 인자로 전달된다는 설명을 함께 반영

### 2. 하이퍼파라미터 탐색은 교차검증 점수를 기준으로 수행하는 것이 일반적이다

- 근거:
  - scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`
- 반영 방식:
  - 9.1에서는 세부 API보다 `왜 튜닝이 필요한가`의 도입 문장으로만 사용
  - GridSearchCV, RandomizedSearchCV의 자세한 설명은 다음 절로 넘김

### 3. 파라미터(parameter)와 하이퍼파라미터(hyperparameter)는 구분해야 한다

- 근거:
  - scikit-learn, `Glossary of Common Terms and API Elements`
- 반영 방식:
  - 학습 결과로 얻는 값과, 학습 전에 넣는 값을 표로 구분
  - 입문 독자가 `가중치(weight)`와 `max_depth`를 섞지 않도록 정리

### 4. 테스트 데이터를 모델 선택이나 전처리에 섞으면 과도하게 낙관적인 성능 추정이 생길 수 있다

- 근거:
  - scikit-learn, `12. Common pitfalls and recommended practices`
- 반영 방식:
  - 9.1에서는 `하이퍼파라미터를 test를 보며 고르면 안 된다`는 원칙 수준으로만 소개
  - 세부적인 튜닝 비용과 검증 비용은 9.2에서 확장 예정

### 5. `random_state`는 재현성과 관련된 대표 설정값이다

- 근거:
  - scikit-learn, `12. Common pitfalls and recommended practices`
- 반영 방식:
  - 복잡도를 바꾸는 값과 재현성을 돕는 값을 구분하는 입문 설명으로 정리
  - 정밀한 난수 정책 설명은 보류

### 6. 하이퍼파라미터 탐색은 수동 조정, 경험 규칙, 격자 탐색을 거쳐 자동화 연구로 확장되었다

- 근거:
  - Marc Claesen, Bart De Moor, `Hyperparameter Search in Machine Learning`, arXiv, 2015
  - James Bergstra, Daniel Yamins, David D. Cox, `Making a Science of Model Search`, arXiv, 2012
- 반영 방식:
  - 9.1에 짧은 역사적 배경 절을 추가
  - `수동 조정 -> grid search -> automated search 관심 증가` 흐름으로 일반화
  - 과도한 연대기 나열은 피하고, 왜 별도 주제가 되었는지 설명하는 데만 사용

### 7. 하이퍼파라미터 문제는 실제 과제에서 모델 비교를 흔드는 실증 사례로 반복 확인되었다

- 근거:
  - James Bergstra, Daniel Yamins, David D. Cox, `Making a Science of Model Search`, arXiv, 2012
  - James Bergstra, Yoshua Bengio, `Random Search for Hyper-Parameter Optimization`, JMLR, 2012
- 반영 방식:
  - 컴퓨터 비전의 LFW, PubFig83, CIFAR-10 사례를 `설정값이 결과 비교를 크게 흔드는 과제`로 요약
  - random search vs grid search 사례를 `탐색 방법도 실증적 문제`라는 설명으로 일반화
  - 장난감 결정트리 예제를 같은 절 안의 작은 실증 사례로 연결

## 본문 반영 판단

- 9.1은 `하이퍼파라미터란 무엇인가`를 소개하는 도입 절로 유지한다.
- 세부 탐색 알고리즘, 병렬 탐색, 실험 자동화는 9.2 또는 뒤 절로 넘긴다.
- Python 예제는 `같은 알고리즘 + 다른 하이퍼파라미터`가 어떤 차이를 만드는지 보여 주는 수준으로 제한한다.

## 도메인 경계 메모

- P3-9.1:
  - 하이퍼파라미터의 정의
  - 파라미터와의 구분
  - 대표 예시
  - 작은 코드 실험
- P3-9.2:
  - 튜닝 전략
  - 탐색 범위
  - 계산 비용
  - 검증 비용
  - 누수(leakage)와 과대평가 위험
