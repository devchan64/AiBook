<a id="false-negative"></a>
<a id="glossary-false-negative"></a>

### 거짓 음성(false negative)

- 뜻: 실제로는 양성인 사례를 모델이나 규칙이 음성으로 판단한 오류입니다. 예를 들어 검토가 필요한 위험 사례를 `검토 불필요`로 놓치는 경우가 false negative입니다.
- 왜 중요한가: false negative가 비싼 문제에서는 threshold를 너무 높게 두면 위험 사례를 놓치는 비용이 커질 수 있습니다. 이 개념이 있어야 놓침 비용과 과검출 비용을 분리하고, 검토 큐를 넓힐지 좁힐지 판단할 수 있습니다.
- 함께 볼 개념: `거짓 양성(false positive)`, `오류 비용(error cost)`, `임계값(threshold)`, `재현율(recall)`
- 중심 Section: `P3-9.12`
- 등장 Section: `P3-9.12`, `P4-8.1`
