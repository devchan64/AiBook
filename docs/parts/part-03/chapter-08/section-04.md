# P3-8.4 보수적 해석과 운영 열

> Section ID: `P3-8.4`
> Version: `v2026.07.25`

_보조제목: 해석 문장은 어떻게 warning 열과 review queue 기준으로 바뀌는가_

[비교표(comparison table)](../../../reference/concept-glossary-parts/05-mieum.md#output-structure)를 읽은 뒤에는 `최근 구간은 기준선 대비 후반 하강이 커졌고 검토 우선순위를 높인다` 같은 보수적 해석 문장이 남습니다. 여기서 필요한 다음 판단은 이 문장을 어떻게 `warning_level`, `review_needed`, `priority_score` 같은 구조화된 운영 열로 바꿀 것인가입니다. 보수적 해석 문장은 끝이 아니라, [검토 후보 큐(review queue)](../../../reference/concept-glossary-parts/05-mieum.md#output-structure)와 같은 [출력 구조(output structure)](../../../reference/concept-glossary-parts/05-mieum.md#output-structure)로 바뀌기 전 마지막 사람 해석 단계입니다. 비교표를 곧바로 구조화된 운영 출력으로 바꾸면 중간의 판단 이유가 빠질 수 있고, 반대로 문장만 남기면 운영 우선순위를 정하거나 같은 기준으로 다시 정렬하기 어렵습니다.

| 층위 | 주된 형태 | 역할 |
| --- | --- | --- |
| [비교 결과(comparison result)](../../../reference/concept-glossary-parts/05-mieum.md#output-structure) | 차이값, [기준선(baseline)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-baseline), 반복성 | 무엇이 달라졌는지 보여 줌 |
| 보수적 해석 문장 | `추가 관찰 필요`, `검토 우선순위 상승` | 사람이 읽을 판단 강도 정리 |
| 구조화된 운영 출력 | `warning_level`, `review_needed`, `priority_score` | 운영에서 다시 정렬·검색·후속 처리 가능 |

이 세 층위를 나누면 `숫자 -> 문장 -> 운영 열`의 흐름이 생깁니다.

## 문장이 먼저 필요한 이유

운영 열을 바로 만들기 전에 문장 단계를 거치는 이유는 단순합니다.

- 어떤 차이를 `기록`으로 둘지
- 어떤 차이를 `검토 후보`로 올릴지
- 어떤 차이를 `강한 경고`로 둘지

이 판단은 보통 숫자 하나가 아니라 표본 수, 반복성, 비교 조건이 만드는 [증거 강도(evidence strength)](../../../reference/concept-glossary-parts/14-hieut.md#interpretation-boundary)를 함께 읽은 뒤에야 정해지기 때문입니다. 즉 문장은 장식이 아니라, 숫자를 운영 판단으로 번역하는 중간 단계입니다.

## 한 장면을 세 단계로 다시 보기

예를 들어 최근 구간을 비교한 뒤 아래처럼 읽었다고 해 보겠습니다.

1. 최근 20건에서 후반 하강이 기준선보다 커졌다.
2. 반복성도 있어 단발성보다 상태 변화 후보에 가깝다.
3. 원인 확정은 보류하고 검토 우선순위를 높인다.

이 세 문장을 운영 열로 옮기면 다음처럼 바뀔 수 있습니다.

| 문장 단계에서 말한 것 | 구조화된 열 예시 |
| --- | --- |
| 차이가 분명하지만 원인 확정은 보류 | `warning_level = caution` |
| 사람이 다시 볼 가치가 있다 | `review_needed = 1` |
| 다른 사례보다 먼저 볼 가치가 있다 | `priority_score = 0.82` |

즉 문장은 자유 서술로 끝나는 것이 아니라, 뒤에서 반복 사용할 열 이름으로 압축될 수 있습니다.

## 보수적 해석과 운영 열은 왜 같은 것이 아닌가

여기서 주의할 점은, 문장과 열이 일대일 대응으로 자동 결정된다고 오해하면 안 된다는 것입니다.

| 보수적 문장 | 바로 같은 뜻이 아닌 것 | 이유 |
| --- | --- | --- |
| `추가 관찰 필요` | 곧바로 `review_needed = 1` | 관찰은 기록 수준일 수도 있기 때문 |
| `검토 우선순위를 높인다` | 곧바로 `원인 확정` | 검토와 진단은 다른 층위이기 때문 |
| `강한 변화 신호` | 곧바로 `자동 조치` | 운영 정책과 안전 기준이 더 필요하기 때문 |

즉 문장은 강도를 정리해 주지만, 실제 운영 열과 정책으로 갈 때는 한 번 더 구조화가 필요합니다.

## 비교 표로 먼저 보기

| event_id | diff | repeatability | conservative_sentence |
| --- | ---: | --- | --- |
| A | -0.35 | high | 검토 우선순위를 높이고 원인 확정은 보류한다 |
| B | -0.35 | low | 차이는 보이지만 표본이 적어 추가 관찰이 필요하다 |

이 문장을 구조화된 운영 열로 옮기면 다음처럼 달라질 수 있습니다.

| event_id | warning_level | review_needed | priority_score |
| --- | --- | ---: | ---: |
| A | caution | 1 | 0.82 |
| B | watch | 0 | 0.41 |

이 두 표가 함께 필요한 이유는 첫 번째 표가 `왜 그렇게 판단했는가`를 남기고, 두 번째 표가 `운영에서 다시 쓸 수 있는 형식`을 남기기 때문입니다.

## 작은 도식으로 보기

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-4-mermaid-01-ko.mmd"
```

이 도식은 같은 차이값이라도 바로 같은 운영 열로 넘어가지 않는다는 점을 보여 줍니다. 먼저 비교 결과를 읽고, 그다음 사람 문장으로 해석 강도를 조절한 뒤에야 `warning_level`, `review_needed`, `priority_score` 같은 운영 열로 압축됩니다. 즉 `warning_level` 같은 열은 갑자기 만들어 낸 구현물이 아니라, 관찰 결과를 사람 해석을 거쳐 운영에 다시 쓰기 쉬운 형식으로 압축한 결과입니다. 여기서 먼저 고정해야 하는 것도 `무엇이 달라졌는가`를 읽고, 그 차이를 얼마나 강하게 말할지 문장으로 조절한 뒤, 다시 운영 열로 압축하는 순서입니다.

## 출처와 참고 자료

- Google for Developers, `Thresholds and the confusion matrix`. 모델의 raw score와 최종 분류는 threshold를 거쳐 연결된다고 설명하므로, 사람 해석 문장과 `warning_level`, `review_needed`, `priority_score` 같은 구조화된 운영 열을 분리해 보는 이 절의 일반 근거가 됩니다. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. 관찰 결과가 어떤 중간 판단을 거쳐 파생되었는지 추적하는 provenance 관점을 제공하므로, 비교 결과에서 보수적 문장, 다시 구조화된 운영 열로 내려가는 이 절의 단계 구분을 설명하는 데 참고할 수 있습니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
