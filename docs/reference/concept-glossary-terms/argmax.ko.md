<a id="argmax"></a>

### argmax

- 뜻: 여러 값 중 가장 큰 값을 가진 위치나 class를 고르는 연산입니다. 다중 클래스 분류에서는 클래스별 확률 중 가장 큰 값을 가진 class를 선택할 때 자주 등장합니다.
- 왜 중요한가: 다중 클래스에서는 `0.5를 넘는가`보다 `어느 class가 가장 큰가`가 더 중요한 경우가 많습니다. argmax를 알면 probability distribution 전체를 비교해 최종 class를 고르는 구조를 읽을 수 있습니다.
- 함께 볼 개념: `다중 클래스 로지스틱 회귀(multinomial logistic regression)`, `소프트맥스(softmax)`, `분류(classification)`
- 중심 Section: `P4-11.4`
