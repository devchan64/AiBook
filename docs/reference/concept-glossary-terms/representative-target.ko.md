<a id="representative-target"></a>
<a id="glossary-representative-target"></a>

### 대표 타깃(representative target)

- 뜻: 여러 목표 라벨 후보 가운데 현재 문제에서 먼저 풀 중심 결과로 고정한 타깃입니다. 같은 사건에서 여러 결과 열이 나와도, 대표 타깃은 이번 모델링 질문이 무엇을 맞히는 문제인지 정하는 기준점입니다.
- 왜 중요한가: 대표 타깃을 고정하지 않으면 같은 데이터로도 검토 필요 여부, 최종 상태, 우선순위 같은 서로 다른 문제를 섞어 설명하게 됩니다. 이 개념이 있어야 `데이터가 많다`와 `문제가 하나로 닫혔다`를 구분하고, 평가와 오류 해석을 어떤 결과 정의에 맞출지 정할 수 있습니다.
- 함께 볼 개념: `타깃(target)`, `목표 라벨 후보(target candidate)`, `타깃 정의 버전(target definition version)`, `라벨(label)`
- 중심 Section: `P3-9.11`
- 등장 Section: `P3-9.11`
