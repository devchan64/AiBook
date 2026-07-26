<a id="solver"></a>

### 솔버(solver)

- 뜻: 학습 목표가 정해진 뒤, 모델 파라미터를 실제로 찾아가는 계산 절차입니다. 로지스틱 회귀에서는 log loss와 regularization으로 정한 목적을 반복 계산으로 줄이며 계수를 찾는 구현 선택으로 볼 수 있습니다.
- 왜 중요한가: 같은 모델 이름을 써도 solver가 달라지면 수렴 방식, 지원되는 penalty, 큰 데이터나 희소 입력을 다루는 성격이 달라질 수 있기 때문입니다. 그래서 실험을 비교할 때는 `로지스틱 회귀를 썼다`만으로 닫지 않고 어떤 solver를 썼는지도 기록해야 합니다.
- 함께 볼 개념: `로지스틱 회귀(logistic regression)`, `정규화(regularization)`, `최적화(optimization)`
- 중심 Section: `P4-11.5`
- 등장 Section: `P4-11.5`
