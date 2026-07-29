<a id="error-cost"></a>
<a id="glossary-error-cost"></a>

### 오류 비용(error cost)

- 뜻: 모델이 틀렸을 때 실제 운영에서 생기는 손실이나 부담입니다. 같은 오류라도 위험 사례를 놓치는 비용, 불필요한 검토를 늘리는 비용, 자동 조치가 잘못 나가는 비용처럼 형태가 다를 수 있습니다.
- 왜 중요한가: 정확도가 같아도 어떤 오류가 더 비싼지에 따라 좋은 threshold와 검토 큐 운영 방식이 달라지기 때문입니다. 이 개념이 있어야 false negative와 false positive를 단순한 개수로만 보지 않고, 현재 문제에서 무엇을 더 줄여야 하는지 먼저 정할 수 있습니다.
- 함께 볼 개념: `거짓 음성(false negative)`, `거짓 양성(false positive)`, `임계값(threshold)`, `인간 감독(human oversight)`
- 중심 Section: `P3-9.12`
- 등장 Section: `P3-9.12`
