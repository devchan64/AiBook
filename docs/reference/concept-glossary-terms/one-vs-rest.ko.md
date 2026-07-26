<a id="one-vs-rest"></a>

### 일대나머지(one-vs-rest)

- 뜻: 여러 class를 한 번에 비교하지 않고, 각 class마다 `이 class인가, 아닌가`라는 이진 분류 문제로 나누어 학습하거나 판단하는 방식입니다.
- 왜 중요한가: 다중 클래스 분류 구현을 읽을 때 one-vs-rest와 multinomial은 class를 비교하는 방식이 다릅니다. 이 구분이 있어야 각 class를 따로 본 뒤 비교하는 구조와, 모든 class를 한 번에 상대 비교하는 구조를 섞지 않을 수 있습니다.
- 함께 볼 개념: `다중 클래스 로지스틱 회귀(multinomial logistic regression)`, `소프트맥스(softmax)`, `분류(classification)`
- 중심 Section: `P4-11.4`
