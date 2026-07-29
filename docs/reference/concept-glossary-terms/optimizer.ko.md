<a id="optimizer"></a>

### 옵티마이저(optimizer)

- 뜻: 손실을 줄이는 방향으로 모델 파라미터를 어떻게 업데이트할지 정하는 학습 알고리즘입니다.
- 왜 중요한가: 같은 손실 함수와 데이터라도 업데이트 규칙이 다르면 학습 속도, 안정성, 수렴 방식이 달라집니다. 옵티마이저를 이해해야 학습률, 그래디언트, Adam 같은 설정이 단순 옵션이 아니라 학습 경로를 바꾸는 장치라는 점을 읽을 수 있습니다.
- 함께 볼 개념: `최적화(optimization)`, `경사하강법(gradient descent)`, `학습률(learning rate)`, `역전파(backpropagation)`, `손실 함수(loss function)`
- 중심 Section: `P5-7.1`
- 등장 Section: `P5-6.1`, `P5-7.2`, `P5-7.3`
