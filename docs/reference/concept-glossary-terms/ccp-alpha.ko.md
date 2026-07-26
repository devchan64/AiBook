<a id="ccp-alpha"></a>

### ccp_alpha

- 뜻: scikit-learn의 결정트리에서 Minimal Cost-Complexity Pruning을 조절하는 복잡도 파라미터입니다. 값이 커질수록 복잡한 가지를 남기는 비용이 커져 더 많은 가지가 잘릴 수 있습니다.
- 왜 중요한가: `ccp_alpha`는 이미 자란 트리를 얼마나 단순하게 줄일지 정하는 손잡이입니다. 값이 너무 작으면 잔가지가 많이 남아 과적합될 수 있고, 너무 크면 중요한 패턴까지 잘려 과소적합될 수 있습니다.
- 함께 볼 개념: `가지치기(pruning)`, `결정트리(decision tree)`, `과적합(overfitting)`, `하이퍼파라미터(hyperparameter)`
- 중심 Section: `P4-14.2`
- 등장 Section: `P4-14.2`
