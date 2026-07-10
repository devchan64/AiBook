# P3-9.11 target 후보가 여러 개이거나 기준이 바뀔 때 무엇을 먼저 고정해야 하는가

> Section ID: `P3-9.11`
> Version: `v2026.07.10`

운영 데이터에서는 target 후보가 하나만 보이지 않을 수 있습니다. `review_needed`, `final_status`, `failure_type`, `priority_bucket`처럼 여러 후보가 함께 보이기도 하고, 같은 이름의 target이라도 시기마다 판정 기준이 달라지기도 합니다. 이 상태에서는 무엇을 대표 문제로 먼저 세울지와 지금 쓰는 정의가 어느 버전인지부터 고정해야 문제 자체가 흔들리지 않습니다. target 후보가 여러 개이거나 기준이 바뀌면, 무엇을 대표 target으로 세우는지와 현재 정의 버전을 먼저 적어야 합니다.

| 먼저 고정할 것 | 왜 필요한가 |
| --- | --- |
| 대표 target | 지금 어떤 문제를 먼저 풀려는지 분명히 하기 위해 |
| target 정의 버전 | 같은 이름이라도 다른 기준을 섞지 않기 위해 |
| 보조 target 후보 | 나중에 비교하거나 확장할 가능성을 남기기 위해 |

| 흔한 장면 | 필요한 메모 |
| --- | --- |
| `review_needed`와 `final_status`가 함께 있다 | 무엇을 먼저 대표 문제로 둘지 |
| 지난달과 이번 달의 판정 기준이 다르다 | 기준 변경 시점과 버전 |
| `warning`, `review`, `failure`가 함께 있다 | 어떤 층위를 target으로 둘지 |


즉 target 후보가 많을 때의 어려움은 `이름 충돌`보다 `대표 결과와 정의 버전을 함께 고정하지 않으면 문제 자체가 흔들린다`는 점에 있습니다. 여기서는 `대표 결과 정의`, `정의 버전 관리`, `확장 후보 관리`를 함께 잡아, 같은 데이터에서 여러 목표 후보가 생길 때 중심 문제를 고정합니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, 확인일 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, versioning and derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
