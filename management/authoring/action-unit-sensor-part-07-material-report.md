# 동작 단위 센서 노트의 Part 7 반영 상태

작성일: 2026-07-18

정리일: 2026-07-19

## 목적

이 문서는 `management/authoring/action-unit-sensor-ai-notes/`의 동작 단위 센서 노트에서 Part 7에 반영한 소재를 추적한다. 기존 문서는 추가 후보를 길게 설명하는 리포트였으나, 주요 후보가 이미 본문에 반영되었으므로 반영 완료 대조표로 압축한다.

## 적용 여부

| 소재 | 출처 노트 | 반영 위치 | 상태 |
| --- | --- | --- | --- |
| 표본 수와 반복성으로 경고 등급 나누기 | `06-sample-size-repeatability-and-false-alarms.md`, `09-exercises-datasets-and-visuals-plan.md` | `P7-7.4` | 반영됨 |
| 같은 평균, 다른 패턴 비교 | `04-sensor-tokenization-and-explainable-features.md`, `09-exercises-datasets-and-visuals-plan.md` | `P7-4.4` | 반영됨 |
| 절대 시간축과 진행도축 비교 | `03-time-series-normalization-and-segmentation.md` | `P7-2.3` | 보충 질문 수준으로 반영됨 |
| 같은 원시 데이터로 문제 정의 다시 쓰기 | `02-problem-framing-from-shot-to-dataset.md` | `P7-1.3` | 회고 카드 수준으로 반영됨 |
| 규칙 기반, 기준선 비교, 특징 기반 모델로 같은 질문 다시 쓰기 | `07-modeling-ladders-rules-statistics-ml.md` | `P7-7.3` | 마무리 회고 표 수준으로 반영됨 |

## 반영 방식 판단

- `P7-7.4`는 `gap`, `event_count`, `repeatability_score`, `recency_weight`를 함께 읽어 `watch`, `review`, `action` 등급을 나누는 독립 연습으로 반영했다.
- `P7-4.4`는 평균(mean)만으로 사라지는 패턴 차이를 `shape token`과 회고 문장 비교로 읽는 독립 연습으로 반영했다.
- `P7-2.3`의 시간축 비교는 긴 시계열 정렬 이론으로 확장하지 않고, 비교 실험 안에서 절대 시간축과 진행도축의 장단점을 고르는 수준으로 제한했다.
- `P7-1.3`의 문제 정의 재작성은 같은 원시 데이터를 `동작 요약`, `기준선 비교`, `검토 우선순위` 문제로 다시 읽는 회고 카드로 제한했다.
- `P7-7.3`의 모델링 사다리는 복잡한 ML 비교로 늘리지 않고, 운영 질문을 단순 규칙, 기준선 비교, 특징 기반 모델 중 어느 수준에서 다룰지 고르는 회고 표로 제한했다.

## 보존 판단

이 문서는 삭제하지 않고 압축 보존한다. 이유는 다음과 같다.

- 동작 단위 센서 노트의 어떤 소재가 Part 7 어느 Section으로 들어갔는지 추적할 수 있다.
- 반영하지 않은 확장 방향을 다시 열지 않도록 범위 제한 근거를 남긴다.
- Part 7 본문에는 중복 설명을 늘리지 않고, 관리 문서에는 반영 이력만 남길 수 있다.

추가 후보를 다시 검토할 때는 이 문서를 새 초안으로 확장하지 말고, 먼저 해당 Section 본문과 릴리즈노트의 현재 상태를 확인한다.
