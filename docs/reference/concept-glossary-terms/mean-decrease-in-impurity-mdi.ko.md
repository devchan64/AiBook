<a id="mean-decrease-in-impurity-mdi"></a>

### 평균 불순도 감소(MDI, mean decrease in impurity)

- 뜻: MDI는 트리의 각 분기가 불순도(impurity)를 얼마나 줄였는지를 해당 특징에 배정하고, 숲 전체에서 평균내어 특징 중요도를 만드는 방식입니다.
- 왜 중요한가: 랜덤포레스트의 `feature_importances_`를 빠르게 읽게 해 주지만, 훈련 데이터에서 분기를 잘 만들기 쉬운 high-cardinality feature를 과대평가할 수 있습니다.
- 함께 볼 개념: `특징 중요도(feature importance)`, `불순도(impurity)`, `랜덤포레스트(random forest)`, `high-cardinality feature`
- 중심 Section: `P4-15.2`
- 등장 Section: `P4-15.2`
