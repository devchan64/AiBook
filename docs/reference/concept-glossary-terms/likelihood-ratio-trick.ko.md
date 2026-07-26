<a id="likelihood-ratio-trick"></a>

### 가능도비 트릭(likelihood ratio trick)

- 뜻: 가능도비 트릭은 확률 분포를 직접 미분하기 어려울 때, 이를 로그 확률의 기울기 형태로 바꾸어 기대값 안에서 계산하기 쉽게 만드는 변형입니다.
- 왜 중요한가: REINFORCE와 policy gradient 식에서 왜 `log pi(a|s)` 같은 형태가 반복해서 나오는지 설명하는 핵심 연결 다리입니다.
- 함께 볼 개념: `log-probability`, `policy gradient theorem`, `REINFORCE`
- 중심 Section: `P4-19.6`
- 등장 Section:

