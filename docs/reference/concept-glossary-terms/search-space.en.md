## search space

- Meaning: 문제를 풀 때 고려할 수 있는 상태와 선택지, 경로 후보의 전체 구조입니다. 단순히 답 후보 목록만이 아니라, 현재 어디에 있고 다음에 무엇을 할 수 있으며 그 선택이 어떤 새 상태로 이어지는지까지 포함한 전체 가능성 지형이라고 볼 수 있습니다.
- Why it matters: A search space explains why candidate counts grow quickly as choices accumulate and why checking every candidate becomes difficult. It helps readers see that slow computation may come from the size of the candidate structure itself, not just from poor implementation.
- Related concepts: `search`, `computational limit`, `heuristic`
- Core Section: `P1-7.1`
- Appears in: `P1-7.2`, `P1-7.4`, `P2-summary`
