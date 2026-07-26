<a id="high-cardinality-feature"></a>

### 고카디널리티 feature(high-cardinality feature)

- 뜻: high-cardinality feature는 서로 다른 값의 종류가 매우 많은 특징입니다. 고객 ID, 주문 번호, 원본 타임스탬프처럼 거의 행마다 다른 값을 가질 수 있는 열이 대표적입니다.
- 왜 중요한가: 트리 계열 모델에서는 값 종류가 많은 특징이 훈련 데이터를 잘게 나누기 쉬워, 실제 일반화 기여보다 중요도가 크게 보일 수 있습니다.
- 함께 볼 개념: `특징 중요도(feature importance)`, `평균 불순도 감소(MDI)`, `과적합(overfitting)`
- 중심 Section: `P4-15.2`
- 등장 Section: `P4-15.2`
