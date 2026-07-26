<a id="cross-entropy"></a>

### 교차 엔트로피(cross-entropy)

- 뜻: 정답에 배정한 확률이 낮을수록 손실을 크게 만드는 확률 기반 손실입니다. 분류나 다음 토큰 예측처럼 여러 후보 중 정답 후보에 충분한 확률을 주었는지 확인할 때 자주 씁니다.
- 왜 중요한가: 단순히 맞고 틀렸는지만 보지 않고, 모델이 정답 후보를 얼마나 자신 있게 밀어 주었는지를 학습 신호로 바꾸기 때문입니다. 이 개념이 있어야 분류 손실, softmax 출력, LLM의 next-token loss를 같은 흐름에서 읽을 수 있습니다.
- 함께 볼 개념: `손실 함수(loss function)`, `softmax`, `로그 손실(log loss)`, `다음 토큰 예측(next-token prediction)`
- 중심 Section: `P5-4.2`
- 등장 Section: `P5-4.1`
