<a id="maximum-likelihood-estimation-mle"></a>

### 최대우도추정(maximum likelihood estimation, MLE)

- 뜻: 관찰된 데이터가 현재 모델 아래에서 가장 그럴듯하게 나오도록 파라미터를 찾는 추정 방식입니다. 로지스틱 회귀에서는 정답 class에 높은 확률을 주는 방향으로 파라미터를 고르는 말로 처음 읽을 수 있습니다.
- 왜 중요한가: 분류 학습을 단순히 `맞힌 개수`가 아니라 `정답에 얼마나 높은 확률을 주었는가`로 읽게 해 줍니다. MLE를 이해하면 log likelihood를 크게 만드는 설명과 log loss를 작게 만드는 설명이 같은 학습 목적을 반대 방향에서 말한다는 점을 연결할 수 있습니다.
- 함께 볼 개념: `로지스틱 회귀(logistic regression)`, `로그 손실(log loss)`, `우도(likelihood)`
- 중심 Section: `P4-11.3`
- 등장 Section: `P4-11.4`
