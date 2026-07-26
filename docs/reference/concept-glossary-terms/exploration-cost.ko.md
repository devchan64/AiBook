<a id="exploration-cost"></a>

### 탐험 비용(exploration cost)

- 뜻: 강화학습 에이전트가 새 행동을 시도하면서 실제로 지불할 수 있는 손실입니다. 시간 손실뿐 아니라 장비 파손, 사용자 이탈, 사고, 법적 책임까지 포함될 수 있습니다.
- 왜 중요한가: 탐험은 새 정보를 얻는 과정이지만 현실에서는 실패 비용을 함께 만듭니다. 이 개념은 평균 보상만 보고 탐험을 늘리는 판단을 막고, safe exploration과 중단 기준을 먼저 묻게 합니다.
- 함께 볼 개념: `탐험(exploration)`, `safe exploration`, `실패 비용(error cost)`, `배포(deployment)`
- 중심 Section: `P4-19.3`
- 등장 Section:
