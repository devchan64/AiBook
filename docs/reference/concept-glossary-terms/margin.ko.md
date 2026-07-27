<a id="margin"></a>

### 마진(margin)

- 뜻: 분류 경계와 그 경계에 가장 가까운 데이터 사례들 사이에 남는 여유 폭입니다. SVM 문맥에서는 여러 경계 후보 중 가장 가까운 점들과의 최소 간격을 크게 만드는 기준으로 읽습니다.
- 왜 중요한가: 같은 데이터를 나누는 경계가 여러 개일 때, 단순히 나눌 수 있다는 사실만으로는 어떤 경계가 더 안정적인지 알기 어렵습니다. 마진을 보면 경계가 한쪽 class에 너무 붙어 있는지, 작은 흔들림에도 prediction이 쉽게 바뀔 위험이 있는지 판단할 수 있습니다.
- 함께 볼 개념: `SVM(support vector machine)`, `결정 경계(decision boundary)`, `분류(classification)`, `하이퍼파라미터(hyperparameter)`
- 중심 Section: `P4-13.1`
- 등장 Section: `P4-13.1`
