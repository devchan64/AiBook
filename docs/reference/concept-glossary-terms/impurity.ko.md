<a id="impurity"></a>

### 불순도(impurity)

- 뜻: 결정트리의 한 node 안에 서로 다른 class가 얼마나 섞여 있는지를 나타내는 정도입니다. 분류 트리에서는 gini, entropy, log loss 같은 기준으로 split 전후의 섞임 정도를 비교할 수 있습니다.
- 왜 중요한가: 좋은 split은 보통 섞인 node를 더 덜 섞인 node들로 바꿉니다. 불순도를 이해하면 결정트리 학습이 `좋아 보이는 질문`을 감으로 고르는 것이 아니라, 나눈 뒤 label이 얼마나 정리되는지 비교하는 과정임을 읽을 수 있습니다.
- 함께 볼 개념: `결정트리(decision tree)`, `임계값(threshold)`, `과적합(overfitting)`
- 중심 Section: `P4-14.1`
- 등장 Section: `P4-14.1`
