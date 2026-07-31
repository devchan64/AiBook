# P3-9.11 target 후보와 변하는 기준

> Section ID: `P3-9.11`
> Version: `v2026.07.31`

_보조제목: target 후보가 여러 개이거나 기준이 바뀔 때 무엇을 먼저 고정해야 하는가_

현실 데이터에서는 목표 라벨 후보(target candidate)가 하나만 보이지 않을 수 있습니다. `review_needed`, `final_status`, `status_type`, `priority_bucket`처럼 여러 후보가 함께 보이기도 하고, 같은 이름의 [타깃(target)](../../../reference/concept-glossary-parts/12-tieut.md#target)이라도 시기마다 판정 기준이 달라지기도 합니다. 이 상태에서는 무엇을 대표 문제로 먼저 세울지와 지금 쓰는 정의가 어느 버전인지부터 고정해야 문제 자체가 흔들리지 않습니다. target 후보가 여러 개이거나 기준이 바뀌면, 무엇을 [대표 타깃(representative target)](../../../reference/concept-glossary-parts/12-tieut.md#target)으로 세우는지와 현재 [타깃 정의 버전(target definition version)](../../../reference/concept-glossary-parts/12-tieut.md#target)을 먼저 적어야 합니다.

| 먼저 고정할 것 | 왜 필요한가 |
| --- | --- |
| [대표 타깃(representative target)](../../../reference/concept-glossary-parts/12-tieut.md#target) | 지금 어떤 문제를 먼저 풀려는지 분명히 하기 위해 |
| [타깃 정의 버전(target definition version)](../../../reference/concept-glossary-parts/12-tieut.md#target) | 같은 이름이라도 다른 기준을 섞지 않기 위해 |
| 함께 관리할 다른 target 후보 | 같은 데이터에서 어떤 결과 후보들이 병존하는지 남기기 위해 |

| 흔한 장면 | 필요한 메모 |
| --- | --- |
| `review_needed`와 `final_status`가 함께 있다 | 무엇을 먼저 대표 문제로 둘지 |
| 지난달과 이번 달의 판정 기준이 다르다 | 기준 변경 시점과 버전 |
| `warning`, `review`, `failure`가 함께 있다 | 어떤 층위를 target으로 둘지 |

대표 target을 정할 때는 `target_name`, `target_definition_version`, `rule_changed_at`, `definition_owner`, `candidate_targets`를 함께 남깁니다. 이 메모는 후보가 여럿인 상태와 기준이 바뀐 상태를 구분해, 같은 이름의 target이 서로 다른 문제 정의를 가리키는 일을 줄입니다.

## 왜 대표 target을 먼저 고정해야 하는가

여러 target 후보가 함께 있을 때 가장 흔한 혼동은 `어차피 다 같은 사건에서 나온 값이니 나중에 하나 고르면 된다`는 생각입니다. 하지만 대표 타깃을 먼저 고정하지 않으면, 지금 어떤 문제를 풀고 있는지 설명 자체가 흔들립니다.

예를 들어 `review_needed`를 대표 target으로 두면 질문은 `무엇을 먼저 다시 봐야 하는가`가 됩니다. 반면 `final_status`를 대표 target으로 두면 질문은 `결국 어떤 상태로 닫히는가`가 됩니다. 같은 사건 표를 써도 두 문제는 목표, 평가, 오류 해석이 달라집니다. 따라서 대표 target을 고정하지 않은 상태는 `데이터가 많은 상태`가 아니라 `문제가 아직 하나로 닫히지 않은 상태`에 가깝습니다.

## 충돌하는 사례를 한 번 더 보기

| event_id | review_needed | final_status | status_type | priority_bucket |
| --- | --- | --- | --- | --- |
| A | 1 | pending | unstable | high |
| B | 1 | normal | recovered | medium |
| C | 0 | normal | stable | low |

이 표를 보면 `A`와 `B`는 둘 다 `review_needed = 1`이지만, `final_status`와 `status_type`은 다릅니다. 만약 지금 대표 target을 `review_needed`로 두면 `A`와 `B`는 같은 결과로 묶입니다. 반대로 대표 target을 `final_status`로 두면 `pending`과 `normal`은 다른 결과가 됩니다. 즉 어떤 열을 대표 target으로 고정하느냐에 따라 같은 사건도 같은 정답이 되기도 하고 다른 정답이 되기도 합니다.

## 작은 도식으로 보기

여러 후보가 함께 있을 때 표만 보면 `나중에 하나 고르면 되겠지`라고 느끼기 쉬운데, 실제 순서는 아래처럼 대표 target 고정이 먼저입니다.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-11-mermaid-01-ko.mmd"
```

이 장면이 보여 주는 핵심은 대표 타깃 선택이 나중에 붙이는 관리 메모가 아니라는 점입니다. 이것은 현재 문제의 중심 질문을 정하는 일이고, 타깃 정의 버전은 그 질문을 어떤 기준으로 읽었는지 고정하는 일입니다.

즉 target 후보가 많을 때의 어려움은 `이름 충돌`보다 `대표 결과와 정의 버전을 함께 고정하지 않으면 문제 자체가 흔들린다`는 점에 있습니다. 여기서는 `대표 결과 정의`, `정의 버전 관리`, `확장 후보 관리`를 함께 잡아, 같은 데이터에서 여러 목표 후보가 생길 때 중심 문제를 고정합니다.

## 체크리스트

- 이 절의 질문인 `target 후보와 변하는 기준`에 대해 한 문장으로 답할 수 있는가?
- `target 후보가 여러 개이거나 기준이 바뀔 때 무엇을 먼저 고정해야 하는지 설명해야 합니다.`라는 기준을 본문 표, 도식, 예제 중 하나에 적용해 설명할 수 있는가?
- 샘플, 특징, 기준선, target/라벨, 검토 기준 중 이 절에서 먼저 고정해야 할 항목을 구분했는가?
- 모델 선택으로 넘기기 전에 Part 3에서 닫아야 할 데이터 구조 질문을 하나 적었는가?

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `label`, `proxy labels`. 라벨이 지도학습 예시의 답 또는 결과 부분이며, 직접 라벨을 볼 수 없을 때 proxy label이 실제 라벨을 근사하는 데이터라는 용어 기준을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. 처리 단계, 재현 가능성, 버전 관리, 파생 관계를 provenance 관점에서 남기는 기준을 확인하는 데 참고했습니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
