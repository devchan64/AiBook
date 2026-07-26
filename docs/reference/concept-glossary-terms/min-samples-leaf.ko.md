<a id="min-samples-leaf"></a>

### 최소 leaf 크기(min_samples_leaf)

- 뜻: 결정트리의 leaf 하나에 최소 몇 개의 훈련 샘플이 남아야 하는지를 정하는 하이퍼파라미터입니다. 값이 커지면 한두 사례만 설명하는 leaf가 생기기 어려워집니다.
- 왜 중요한가: leaf가 너무 작아지면 트리가 훈련 데이터의 예외를 안정적인 규칙처럼 말할 수 있습니다. `min_samples_leaf`는 leaf가 너무 작은 예외 집합이 되지 않게 하여 과적합 위험을 낮추는 손잡이입니다.
- 함께 볼 개념: `leaf`, `결정트리(decision tree)`, `과적합(overfitting)`, `하이퍼파라미터(hyperparameter)`
- 중심 Section: `P4-14.2`
- 등장 Section: `P4-14.2`
