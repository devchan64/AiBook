<a id="decision-boundary"></a>

### 결정 경계(decision boundary)

- 뜻: 분류 모델이 입력 공간(input space)을 서로 다른 class 영역으로 나누는 기준선, 기준면, 또는 더 높은 차원의 기준입니다. 로지스틱 회귀에서는 보통 선형 점수 \(z\)가 기준값과 같아지는 자리로 읽습니다.
- 왜 중요한가: 결정 경계를 보면 모델이 어떤 입력을 왜 한쪽 class로 보냈는지, 경계 근처의 애매한 사례가 왜 review 대상이 되는지 설명할 수 있습니다. 또한 threshold를 바꾸면 같은 점수 모델에서도 실제로 적용되는 경계와 class 영역이 달라질 수 있음을 분리해서 읽게 해 줍니다.
- 함께 볼 개념: `로지스틱 회귀(logistic regression)`, `임계값(threshold)`, `분류(classification)`, `초평면(hyperplane)`
- 중심 Section: `P4-11.2`
- 등장 Section: `P4-11.3`, `P5-1.2`
