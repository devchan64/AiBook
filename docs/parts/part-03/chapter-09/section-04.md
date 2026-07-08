# P3-9.4 검토 결과는 어떻게 운영 메모에서 목표 라벨 후보로 바뀌는가

> Section ID: `P3-9.4`
> Version: `v2026.07.08`

[검토 후보 큐(review queue)](../../../reference/concept-glossary.md#glossary-review-queue)와 [비교 리포트(comparison report)](../../../reference/concept-glossary.md#glossary-comparison-report)는 먼저 생겨도, [목표 라벨 후보(target candidate)](../../../reference/concept-glossary.md#glossary-target-candidate)는 대개 바로 주어지지 않습니다. 처음 남는 것은 깔끔한 `정답 라벨`보다 제각각의 검토 결과와 운영 메모인 경우가 많기 때문입니다. 그래서 목표 라벨 후보는 `처음부터 주어진 정답`이라기보다, `검토 과정에서 반복적으로 남은 운영 판단을 더 안정된 열로 바꾼 결과`로 읽는 편이 정확합니다.

## 처음에는 왜 메모만 남는가

운영 현장에서는 처음부터 `정상`, `이상`, `원인 A`, `원인 B` 같은 정리된 라벨이 있는 것이 아니라, 아래처럼 제각각의 검토 메모가 먼저 남기 쉽습니다.

| event_id | review_needed | operator_note |
| --- | --- | --- |
| A | 1 | 후반 급락 패턴 확인, 다음 건도 확인 필요 |
| B | 0 | 기준선과 큰 차이 없음 |
| C | 1 | 반복 하강, 센서 점검 권장 |

이 표는 운영에는 유용하지만, 아직 바로 학습 라벨로 쓰기에는 불안정합니다. 메모 길이도 다르고, 표현 방식도 다르고, 어떤 사람은 원인을 쓰고 어떤 사람은 다음 행동만 쓸 수 있기 때문입니다.

그래서 `운영 메모가 있다`와 `목표 라벨이 준비되었다`는 같은 말이 아닙니다.

## 메모에서 라벨 후보로 바뀌려면 무엇이 더 필요한가

운영 메모가 목표 라벨 후보로 바뀌려면 보통 아래 조건이 더 필요합니다.

| 더 필요한 것 | 왜 필요한가 |
| --- | --- |
| 같은 의미를 반복해서 가리키는 공통 기준 | 사람마다 다른 표현을 같은 판단으로 묶어야 하기 때문 |
| 샘플 단위와 맞는 기록 방식 | 메모가 동작 1회 기준인지, 기간 요약 기준인지 맞춰야 하기 때문 |
| 비어 있는 경우 처리 방식 | 메모가 없는 사례를 어떻게 둘지 정해야 하기 때문 |
| 나중에 다시 확인 가능한 근거 열 | 라벨이 왜 붙었는지 추적할 수 있어야 하기 때문 |

즉 검토 결과가 학습 라벨로 바뀌려면 단순히 값이 있는 것보다, 같은 뜻을 같은 열로 남기는 규칙이 먼저 있어야 합니다.

## 검토 큐와 라벨 후보 표의 차이

검토 후보 큐는 `무엇부터 볼 것인가`가 중심이고, 라벨 후보 표는 `무엇을 나중에 맞히고 싶은가`가 중심입니다. 같은 사건 목록이라도 표의 중심이 달라집니다.

| 산출물 | 중심 질문 | 먼저 필요한 열 |
| --- | --- | --- |
| 검토 후보 큐 | 무엇부터 사람이 볼 것인가 | `priority_score`, `review_needed`, 비교 근거 |
| 목표 라벨 후보 표 | 무엇을 결과 열로 둘 수 있는가 | `target_candidate`, 근거 메모, 특징 열 |

예를 들어 검토 큐에서는 `review_needed = 1`이면 충분할 수 있습니다. 하지만 목표 라벨 후보 표에서는 `review_needed = 1`이 어떤 조건에서 붙었는지, 나중에 같은 기준으로 다시 붙을 수 있는지가 더 중요합니다.

## 한 단계씩 바뀌는 과정

같은 사건 목록이 보통 아래 순서로 바뀝니다.

1. 비교 리포트에서 변화 신호를 본다.
2. 검토 후보 큐에서 사람이 먼저 볼 순서를 만든다.
3. 사람이 남긴 검토 결과를 반복해서 모은다.
4. 자주 반복되는 판단을 공통 열로 정리한다.
5. 그 열이 비교적 안정적이면 목표 라벨 후보로 올린다.

이 순서가 중요한 이유는, 목표 라벨 후보가 뜬금없이 생기는 것이 아니라 `검토 과정의 반복`에서 나온다는 점을 보여 주기 때문입니다.

## 예시: 운영 메모에서 라벨 후보 만들기

아래처럼 처음에는 메모가 제각각일 수 있습니다.

| event_id | diff | repeatability | review_needed | operator_note |
| --- | --- | --- | --- | --- |
| A | -0.35 | high | 1 | 후반 급락 반복, 재확인 필요 |
| B | -0.08 | low | 0 | 기록만 남김 |
| C | -0.31 | high | 1 | 후반 급락 반복, 점검 권장 |

이 상태에서는 `operator_note`를 그대로 목표 라벨로 쓰기 어렵습니다. 대신 반복 표현을 더 안정된 열로 다시 정리할 수 있습니다.

| event_id | late_drop_repeated | needs_manual_review | note_source |
| --- | --- | --- | --- |
| A | 1 | 1 | 후반 급락 반복, 재확인 필요 |
| B | 0 | 0 | 기록만 남김 |
| C | 1 | 1 | 후반 급락 반복, 점검 권장 |

이 두 번째 표가 중요한 이유는 문장을 완전히 없앴기 때문이 아니라, 반복되는 운영 판단을 같은 뜻의 열로 옮겼기 때문입니다. `note_source`를 남겨 두면 왜 라벨 후보가 붙었는지도 다시 추적할 수 있습니다.

## 어떤 열이 먼저 목표 라벨 후보가 되기 쉬운가

모든 운영 메모가 똑같이 좋은 라벨 후보가 되는 것은 아닙니다.

| 먼저 후보가 되기 쉬운 것 | 아직 어려운 것 |
| --- | --- |
| `review_needed`처럼 운영상 반복되는 0/1 판단 | 길고 자유로운 서술 메모 전체 |
| `late_drop_repeated`처럼 비교적 같은 뜻으로 다시 붙는 판단 | 사람마다 이름이 다른 원인 설명 |
| `정상/주의`처럼 비교적 공통 기준이 있는 상태 | 상세 원인 taxonomy가 없는 원인 분류 |

즉 먼저 구조화되기 쉬운 것은 대개 `운영 검토 필요 여부`, `반복 경고 여부`, `간단한 상태 구분` 같은 열입니다. 반면 세부 원인 분류는 더 나중에야 안정될 수 있습니다.

여기서 `target`이라는 이름은 갑자기 생기는 것이 아닙니다. 많은 경우 target은 데이터셋 안에 원래 들어 있던 것이 아니라, 비교 리포트와 검토 큐를 운영하면서 축적된 판단을 다시 열로 바꾼 결과입니다.

즉 Part 3은 단순히 입력 특징만 만드는 Part가 아니라, 나중에 목표 라벨 후보가 생길 수 있는 운영 기록 구조까지 설계하는 Part이기도 합니다.

## 작은 도식으로 보기

```mermaid
flowchart TD
    A[Review queue result<br/>event_id + review_needed + operator note]
    A --> B[Free-form notes accumulate]
    B --> C[Shared note patterns<br/>repeated late drop<br/>record only]
    C --> D[Target-candidate columns]

    D --> D1[late_drop_repeated]
    D --> D2[needs_manual_review]
    D --> D3[note_source]
```

이 도식은 자유 메모가 바로 target이 되는 것이 아니라, 중간에 `같은 뜻을 묶는 단계`가 꼭 들어간다는 점을 보여 줍니다. 먼저 검토 결과와 메모가 쌓이고, 그 메모에서 반복되는 판단을 공통 패턴으로 정리한 뒤에야 `late_drop_repeated`, `needs_manual_review` 같은 열이 생깁니다. 이 절에서 중요한 것은 문자열 처리 기술이 아니라 `메모 -> 공통 의미 -> 라벨 후보 열`의 전환 구조입니다.

이 절은 운영 메모 정리 기술이 아니라, `비정형 판단을 구조화된 라벨 후보(structured target candidate)로 바꾸는 과정`을 설명합니다.


즉 target은 갑자기 주어지는 값이 아니라, Part 3의 검토 기록을 구조화한 결과로 읽어야 합니다.

목표 라벨 후보는 처음부터 주어진 정답이 아니라, 검토 과정에서 반복적으로 남은 운영 판단을 더 안정된 열로 바꾼 결과일 때가 많습니다. 이렇게 정리해 두면 `target`도 갑자기 나타나는 열이 아니라, 비교 리포트와 검토 큐 운영을 거쳐 축적된 결과로 읽히게 됩니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `label`, `labeled example`, 확인일 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, provenance, entity, derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
