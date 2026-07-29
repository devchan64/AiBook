# P3-8.5 여러 비교 열은 어떻게 하나의 검토 우선순위 후보로 묶는가

> Section ID: `P3-8.5`
> Version: `v2026.07.25`

평균 차이, 변동성 차이, 반복성, 최근 구간 건수, 패턴 요약이 한 표에 함께 들어오면 곧바로 이런 문제가 생깁니다. `열이 여러 개인데 무엇을 먼저 보고, 어떻게 한 줄 판단으로 줄여야 하는가?` [열 역할 분리(column-role separation)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-column-role-separation) 관점에서 보면, 비교 열이 많아질수록 필요한 것은 더 많은 숫자가 아니라, 서로 다른 신호를 몇 개의 판단 축으로 다시 묶는 방법입니다.

[검토 후보 큐(review queue)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-review-queue)의 우선순위는 차이값 하나를 그대로 쓰는 것이 아니라, 여러 비교 열을 `변화 크기`, `반복성`, `해석 신뢰도`, `운영 중요도` 같은 몇 개의 판단 축으로 먼저 묶은 뒤에 정합니다.

## 왜 바로 한 숫자로 가면 안 되는가

[비교표(comparison table)](../../../reference/concept-glossary-parts/06-bieup.md#glossary-comparison-table)에는 보통 아래 같은 열이 함께 들어옵니다.

| 비교 열 예시 | 바로 보이는 뜻 |
| --- | --- |
| `diff_mean` | 평균 수준 차이 |
| `diff_std` | 흔들림 차이 |
| `repeatability_score` | 같은 방향 변화 반복 정도 |
| `recent_count` | 최근 구간 표본 수 |
| `segment_shift` | 패턴 요약 차이 |

이 열들을 바로 하나의 숫자로 합치면 빠르기는 합니다. 하지만 왜 어떤 사례가 위에 올라오고 어떤 사례가 아래로 가는지 설명이 사라지기 쉽습니다. 그래서 Part 3에서는 먼저 이 열들을 `무슨 종류의 신호인가`로 다시 묶는 단계가 필요합니다.

## 먼저 묶는 네 가지 판단 축

여러 비교 열은 아래 네 축으로 먼저 줄여 볼 수 있습니다.

| 판단 축 | 주로 보는 열 | 질문으로 바꾸면 |
| --- | --- | --- |
| 변화 크기 | 평균 차이, 비율 차이, 구간 차이 | 지금 평소와 얼마나 다른가 |
| 반복성 | 반복 방향, 구간별 반복 신호 | 이 변화가 한 번이 아니라 이어지고 있는가 |
| 해석 신뢰도 | 최근 건수, [기준선(baseline)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-baseline) 표본 수 | 이 차이를 어느 정도 강도로 말할 수 있는가 |
| 운영 중요도 | 특정 공정 조건, 종료 직전 구간, 안전 관련 열 | 사람이 먼저 봐야 할 실무 이유가 있는가 |

이 네 축으로 다시 보면 `열이 많아서 복잡하다`는 느낌이 줄어듭니다. 각 열이 서로 다른 질문에 답한다는 점이 보이기 때문입니다.

## 같은 차이값도 우선순위가 달라질 수 있다

예를 들어 두 사례의 평균 차이값이 똑같이 `-0.35`라고 해 보겠습니다. 그래도 아래 조건이 다르면 검토 우선순위는 달라질 수 있습니다.

| 사례 | 변화 크기 | 반복성 | 해석 신뢰도 | 운영 중요도 |
| --- | --- | --- | --- | --- |
| A | 큼 | 높음 | 높음 | 높음 |
| B | 큼 | 낮음 | 낮음 | 보통 |

즉 `diff` 하나만 보면 둘 다 비슷해 보이지만, 실제로는 A가 더 먼저 검토되어야 할 수 있습니다. 검토 우선순위는 `얼마나 다르냐`만이 아니라 [증거 강도(evidence strength)](../../../reference/concept-glossary-parts/09-jieut.md#glossary-evidence-strength)와 `실무적으로 먼저 봐야 하느냐`를 함께 묻기 때문입니다.

## 사람 검토 문장과 우선순위 후보는 어떻게 이어지는가

앞 절에서 보수적 문장은 `비교 결과 -> 강도 조건 -> 다음 행동` 순서로 썼습니다. 이제 이 문장을 다시 줄이면 아래처럼 우선순위 후보 축으로 옮길 수 있습니다.

| 문장 단계에서 말한 것 | 우선순위 후보로 옮긴 뜻 |
| --- | --- |
| 기준선 대비 차이가 크다 | 변화 크기 높음 |
| 최근 여러 구간에서 반복된다 | 반복성 높음 |
| 최근 건수가 충분하다 | 해석 신뢰도 높음 |
| 사람이 먼저 봐야 할 공정 조건이다 | 운영 중요도 높음 |

즉 우선순위 후보는 설명을 버리는 것이 아니라, 문장을 다시 `판단 축`으로 압축한 결과입니다.

## 비교 표로 먼저 보기

| event_id | diff_mean | repeatability_score | recent_count | safety_related |
| --- | ---: | ---: | ---: | --- |
| A | -0.35 | 4 | 20 | yes |
| B | -0.35 | 1 | 3 | no |
| C | -0.18 | 4 | 18 | yes |

이 표를 바로 `priority_score`로 바꾸기 전에 먼저 아래처럼 묶어 읽을 수 있습니다.

| event_id | 변화 크기 | 반복성 | 해석 신뢰도 | 운영 중요도 |
| --- | --- | --- | --- | --- |
| A | 높음 | 높음 | 높음 | 높음 |
| B | 높음 | 낮음 | 낮음 | 낮음 |
| C | 보통 | 높음 | 높음 | 높음 |

이제야 왜 A가 가장 먼저 오고, B는 차이값이 커도 한 단계 아래로 내려갈 수 있는지 설명이 됩니다.

## 작은 도식으로 보기

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-5-mermaid-01-ko.mmd"
```

이 도식은 여러 열을 곧바로 점수 하나로 합치는 것이 아니라, 먼저 `무슨 판단 축인가`로 다시 묶어야 한다는 점을 보여 줍니다. 즉 여기서 먼저 봐야 하는 것은 `열이 많다`는 복잡함보다 `서로 다른 질문을 몇 개의 판단 축으로 묶는다`는 구조입니다. 검토 우선순위는 차이값 하나가 아니라, 변화 크기, 반복성, 해석 신뢰도, 운영 중요도를 함께 묶어 만든 후보 판단입니다. 따라서 이 절의 핵심은 `여러 비교 열을 어떻게 한 줄 점수로 구현할까`보다 `여러 비교 열이 어떤 질문 묶음으로 다시 압축되는가`를 먼저 분명히 하는 데 있습니다.

## 출처와 참고 자료

- Google for Developers, `Thresholds and the confusion matrix`. score 하나가 곧바로 행동이 아니라 threshold와 비용 구조를 거쳐 해석된다는 설명을 제공하므로, 여러 비교 열을 한 번에 숫자 하나로 합치기보다 먼저 판단 축으로 묶는 이 절의 설명을 보강합니다. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Classification: ROC and AUC`. 모델 점수의 핵심 용도 중 하나가 순서를 세우는 것임을 보여 주므로, 검토 우선순위를 `변화 크기`, `반복성`, `해석 신뢰도`, `운영 중요도` 축으로 압축해 review queue 후보를 만든다는 이 절의 일반화된 관점을 뒷받침합니다. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
