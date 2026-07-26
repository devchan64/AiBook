<a id="multinomial-logistic-regression"></a>

### 다중 클래스 로지스틱 회귀(multinomial logistic regression)

- 뜻: 셋 이상의 class 중 하나를 고르는 문제에서, 클래스마다 점수를 만들고 그 점수를 확률 분포로 바꾸어 가장 그럴듯한 class를 고르는 로지스틱 회귀 확장입니다.
- 왜 중요한가: 이진 분류에서 익힌 `점수 -> 확률 -> class 선택` 감각을 여러 class 비교로 넓혀 줍니다. 다중 클래스에서는 0.5 threshold 하나보다 class 전체 확률 분포와 argmax 선택을 함께 읽어야 합니다.
- 함께 볼 개념: `로지스틱 회귀(logistic regression)`, `소프트맥스(softmax)`, `분류(classification)`
- 중심 Section: `P4-11.4`
