<a id="false-positive"></a>
<a id="glossary-false-positive"></a>

### 거짓 양성(false positive)

- 뜻: 실제로는 음성인 사례를 모델이나 규칙이 양성으로 판단한 오류입니다. 예를 들어 검토가 필요 없는 사례를 검토 큐에 올리는 경우가 false positive입니다.
- 왜 중요한가: false positive가 비싼 문제에서는 threshold를 너무 낮게 두면 사람 검토 부담과 자동 조치 비용이 커질 수 있습니다. 이 개념이 있어야 놓침을 줄이는 전략과 과검출을 줄이는 전략이 서로 다른 운영 선택이라는 점을 읽을 수 있습니다.
- 함께 볼 개념: `거짓 음성(false negative)`, `오류 비용(error cost)`, `임계값(threshold)`, `정밀도(precision)`
- 중심 Section: `P3-9.12`
- 등장 Section: `P3-9.12`, `P4-6.4`, `P4-8.1`
