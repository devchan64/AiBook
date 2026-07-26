<a id="intervention-feedback"></a>
<a id="glossary-intervention-feedback"></a>

### 개입 피드백(intervention feedback)

- 뜻: 모델 출력, 검토 규칙, 운영 조치가 이후의 데이터와 라벨을 바꾸어, 나중에 관측되는 결과가 원래 자연 경과와 달라지는 되먹임 구조입니다.
- 왜 중요한가: 개입이 후속 사건을 줄이거나 로그 길이와 라벨 선택을 바꾸면, 나중 데이터는 `원래 안전했다`는 증거가 아니라 `조치가 먼저 들어간 뒤 남은 결과`일 수 있습니다. 이 개념이 있어야 개입 전 신호, 개입 후 운영 결과, 선택적으로 남은 라벨을 같은 층위로 섞지 않고 읽게 됩니다.
- 함께 볼 개념: `해석 경계(interpretation boundary)`, `선택적 라벨(selective labels)`, `검토 후보 큐(review queue)`, `출처 추적(provenance)`
- 중심 Section: `P3-8.7`
- 등장 Section: `P3-8.7`
