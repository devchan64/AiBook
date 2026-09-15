# P3-3.3 질문을 첫 표 초안으로 옮기려면 어떤 열부터 스케치해야 하는가

> Section ID: `P3-3.3`
> Version: `v2026.09.15`

질문을 받은 뒤 바로 필요한 것은 완성된 표를 한 번에 적는 일이 아니라, 첫 표 초안에서 어떤 [열(column)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)이 [샘플(sample)](../../../reference/concept-glossary-parts/07-siot.md#glossary-sample)을 식별하고 어떤 열이 상태, 비교, 결과를 맡는지 먼저 나누는 일입니다. 질문 문장이 바뀌면 표 초안의 열 구조도 함께 바뀌므로, 저장된 기록을 [문제 표현 구조(problem-representation structure)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)로 옮기려면 이 첫 스케치가 분명해야 합니다. 첫 표 초안에서 중요한 것도 완성된 열 목록이 아니라 이런 역할 구분입니다.

처음 표 초안을 그릴 때는 모든 열을 다 적으려 하지 말고, 먼저 아래 네 묶음을 적는 편이 안전합니다.

1. 샘플을 식별하는 열
2. 샘플을 설명하는 [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature) 후보 열
3. 비교를 위해 필요한 [기준선(baseline)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-baseline) 또는 차이 열
4. 사람이 읽거나 나중에 맞히고 싶은 결과 열

이 네 묶음을 표로 줄이면 다음과 같습니다.

| 열 묶음 | 왜 먼저 필요한가 |
| --- | --- |
| 샘플 식별 열 | 무엇을 한 건으로 볼지 표에서 드러나야 하기 때문 |
| 특징 후보 열 | 샘플의 상태를 설명할 값이 필요하기 때문 |
| 비교 열 | 평소 대비 변화가 보이려면 차이 구조가 필요하기 때문 |
| 결과 열 | 검토 후보인지 목표 라벨 후보(target candidate)인지 방향이 보여야 하기 때문 |

즉 첫 표 초안은 `모든 원천 열을 옮겨 적는 일`이 아니라, `이 문제에 필요한 역할별 열 묶음을 먼저 배치하는 일`입니다.

## 질문에서 표 초안으로 가는 최소 변환

예를 들어 질문이 `최근 동작 1회가 평소보다 더 흔들렸는가`라면, 곧바로 표 초안은 아래처럼 스케치할 수 있습니다.

| 열 역할 | 초안 예시 |
| --- | --- |
| 샘플 식별 열 | `event_id` |
| 특징 후보 열 | `flow_mean`, `flow_std`, `late_drop_rate` |
| 비교 열 | `baseline_diff`, `repeatability_score` |
| 결과 열 | `review_needed` 또는 `report_sentence` |

질문이 바뀌면 초안도 함께 바뀝니다.

| 질문 문장 | 초안에서 가장 먼저 달라지는 것 |
| --- | --- |
| 최근 동작 1회가 평소보다 흔들렸는가 | 샘플이 `동작 1회`로 잡힌다 |
| 최근 20건이 이전 200건보다 달라졌는가 | 샘플보다 `구간 집계`와 비교 열이 더 앞에 온다 |
| 사람이 먼저 볼 동작은 무엇인가 | 결과 열이 `priority_score`, `review_needed` 쪽으로 바뀐다 |
| 나중에 맞힐 결과 후보를 만들 수 있는가 | 결과 열이 `target` 후보로 더 분명해진다 |

즉 질문은 문장으로 끝나지 않고, 곧바로 표의 열 구조를 밀어냅니다.

## 처음부터 완벽한 열 이름이 필요하지는 않다

여기서 자주 멈추는 이유는 `정확한 열 이름을 아직 모르는데 어떻게 표를 그리지?`라는 생각 때문입니다. 하지만 Part 3 단계에서는 열 이름을 완벽하게 확정할 필요가 없습니다. 먼저 `역할`부터 적으면 됩니다.

예를 들어 아래처럼 써도 충분합니다.

- 샘플 식별 열 1개
- 수준을 보여 주는 특징 1~2개
- 변화나 흔들림을 보여 주는 특징 1~2개
- 기준선 대비 차이 열 1개
- 사람 검토용 결과 열 1개

이 정도만 적어도 질문이 어떤 표 구조를 요구하는지 윤곽이 생깁니다.

## 질문을 식별·설명·결과 열로 옮기기 {#_3}

문제 상황: 질문이 바뀌면 첫 표 초안의 열 묶음도 함께 바뀐다는 점을 확인합니다.

입력(input): 서로 다른 질문 3개

기대 출력(output): 각 질문에 따라 `식별`, `특징`, `비교`, `결과` 열 초안이 다르게 스케치됩니다.

확인할 개념: 첫 표 초안은 완성된 열 이름 목록이 아니라, 질문이 요구하는 역할별 열 묶음을 먼저 드러내는 단계다

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-3-mermaid-01-ko.mmd"
```

이 예시의 핵심은 열 이름 목록보다 `질문이 달라지면 어느 열 묶음이 먼저 달라지는가`를 보는 데 있습니다. 동작 1회 비교에서는 `event_id`와 `review_needed`가 먼저 보이고, 최근 20건 비교에서는 `window_id`와 `report_sentence`가 더 자연스럽습니다. 반대로 나중의 학습 후보를 생각하면 결과 열이 `target_candidate`로 바뀝니다. 즉 첫 표 초안은 정답 표를 한 번에 완성하는 과정이 아니라, 질문이 요구하는 샘플 단위와 결과 방향을 먼저 드러내는 스케치입니다.

가상 사례로, 완료된 동작 A의 후반 평균이 2.4 L/min이고 같은 운전 조건의 과거 기준선이 2.8 L/min이라고 합시다. `동작별 후반 평균이 평소보다 낮은지 보고한다`는 질문에 맞춰 한 행을 채워 보세요.

| event_id | late_flow_mean | baseline_late_flow_mean | delta_from_baseline | report_sentence |
| --- | ---: | ---: | ---: | --- |
| A | 2.4 | 2.8 | -0.4 | 같은 조건의 기준선보다 후반 평균이 0.4 L/min 낮음 |

차이는 `현재 − 기준선 = 2.4 − 2.8 = −0.4`입니다. A를 찾는 열, 측정값 열, 비교 열, 보고 문장이 한 행에서 서로 다른 역할을 합니다. B의 측정값은 있지만 해당 조건의 기준선이 없다면 어떻게 채울까요? 기준선과 차이값은 비워 두고 `비교 기준 확보 필요`라고 적습니다. 기준선을 0으로 채우면 실제로 관측하지 않은 기준과의 차이를 만들어 내기 때문입니다. 이 표에는 미래 고장 여부를 채울 근거도 아직 없습니다.

## 체크리스트

- 첫 표에 식별자·관측값·비교 기준 열을 나누어 적었는가?
- 당장 채울 수 없는 열을 0으로 채우지 않고 필요한 자료를 표시했는가?

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`, `example`, `labeled example`. example는 라벨이 없을 수도 있고, labeled example은 특징과 라벨을 함께 포함합니다. 표 초안에서 입력 열과 결과 열을 구분하는 용어 기준으로 참고했습니다. [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-15
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. feature가 label의 proxy가 되는 설계 결함을 설명하므로, 결과 열과 설명 열의 역할을 초안 단계에서부터 구분해야 한다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 기준 시점은 다른 시점과 비교하기 위한 reference라고 설명하므로, baseline diff 같은 비교 역할 열을 별도로 두는 초안이 필요하다는 일반 근거가 됩니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
