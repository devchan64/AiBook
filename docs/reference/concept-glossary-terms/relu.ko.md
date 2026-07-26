<a id="relu"></a>

### ReLU(rectified linear unit)

- 뜻: ReLU는 입력이 음수이면 0으로 자르고, 0 이상이면 거의 그대로 통과시키는 활성화 함수입니다. 보통 \(f(z)=\max(0,z)\)로 씁니다.
- 왜 중요한가: 현대 딥러닝에서 자주 쓰이는 기본 활성화 함수이며, sigmoid나 tanh와 달리 양수 구간에서는 포화되지 않습니다. 이 성질은 깊은 신경망의 신호 전달과 활성화 함수 비교를 이해할 때 중요한 기준이 됩니다.
- 함께 볼 개념: `활성화 함수(activation function)`, `sigmoid`, `tanh`, `다층 신경망(multilayer neural network)`
- 중심 Section: `P5-3.4`
- 등장 Section: `P5-3.5`
