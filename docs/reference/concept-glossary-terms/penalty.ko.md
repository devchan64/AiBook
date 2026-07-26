<a id="penalty"></a>

### 벌점(penalty)

- 뜻: 목적 함수에 더해져 모델이 특정한 해를 덜 선호하게 만드는 추가 비용입니다. 로지스틱 회귀 설정에서는 보통 L1, L2, Elastic-Net처럼 계수를 얼마나 어떤 방식으로 보수적으로 잡을지 정하는 regularization 방식을 가리킵니다.
- 왜 중요한가: penalty가 바뀌면 모델이 큰 계수를 피하는 방식, 일부 계수를 0에 가깝게 미는 방식, 지원되는 solver 조합이 함께 달라질 수 있기 때문입니다. 따라서 성능이나 계수를 비교할 때 penalty 설정을 따로 기록해야 합니다.
- 함께 볼 개념: `정규화(regularization)`, `목적 함수(objective function)`, `솔버(solver)`
- 중심 Section: `P4-11.5`
- 등장 Section: `P4-11.5`
