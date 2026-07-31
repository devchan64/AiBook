# P3-3.3 질문을 첫 표 초안으로 옮기려면 어떤 열부터 스케치해야 하는가

> Section ID: `P3-3.3`
> Version: `v2026.07.31`

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

## 작은 도식으로 보기

문제 상황: 질문이 바뀌면 첫 표 초안의 열 묶음도 함께 바뀐다는 점을 확인합니다.

입력(input): 서로 다른 질문 3개

기대 출력(output): 각 질문에 따라 `식별`, `특징`, `비교`, `결과` 열 초안이 다르게 스케치됩니다.

확인할 개념: 첫 표 초안은 완성된 열 이름 목록이 아니라, 질문이 요구하는 역할별 열 묶음을 먼저 드러내는 단계다

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-3-mermaid-01-ko.mmd"
```

이 예시의 핵심은 열 이름 목록보다 `질문이 달라지면 어느 열 묶음이 먼저 달라지는가`를 보는 데 있습니다. 동작 1회 비교에서는 `event_id`와 `review_needed`가 먼저 보이고, 최근 20건 비교에서는 `window_id`와 `report_sentence`가 더 자연스럽습니다. 반대로 나중의 학습 후보를 생각하면 결과 열이 `target_candidate`로 바뀝니다. 즉 첫 표 초안은 정답 표를 한 번에 완성하는 과정이 아니라, 질문이 요구하는 샘플 단위와 결과 방향을 먼저 드러내는 스케치입니다.

질문을 역할별 열 묶음으로 먼저 옮겨 두면, 이후에 샘플 단위와 요약 표를 더 구체적으로 다룰 때도 `무엇을 한 건으로 잡는가`, `어떤 값이 비교와 결과를 맡는가`가 이미 보인 상태에서 읽을 수 있습니다. 즉 이 절의 핵심은 질문 문장을 바로 표 구조의 역할 단위로 바꾸어, 첫 표 초안이 추상적인 메모가 아니라 실제 작업 표의 설계 출발점이 되게 만드는 데 있습니다. 이 절을 `첫 표 명세(first-table specification)`를 어떤 역할 단위로 적을 것인가의 문제로 다시 보면, 첫 표 초안은 완성된 컬럼 사전이 아니라 질문이 요구하는 역할별 열 묶음을 먼저 명세하는 단계라는 점이 더 분명해집니다.

## 체크리스트

- 이 절의 질문인 `질문을 첫 표 초안으로 옮기려면 어떤 열부터 스케치해야 하는가`에 대해 한 문장으로 답할 수 있는가?
- `첫 표 초안을 만들 때 어떤 열 묶음부터 스케치해야 하는지 정리해야 합니다.`라는 기준을 본문 표, 도식, 예제 중 하나에 적용해 설명할 수 있는가?
- 샘플, 특징, 기준선, target/라벨, 검토 기준 중 이 절에서 먼저 고정해야 할 항목을 구분했는가?
- 모델 선택으로 넘기기 전에 Part 3에서 닫아야 할 데이터 구조 질문을 하나 적었는가?

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example는 feature와 label 구조를 전제로 하므로, 첫 표 초안에서도 식별/설명/결과 역할을 먼저 나눠 두어야 한다는 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. feature가 label의 proxy가 되는 설계 결함을 설명하므로, 결과 열과 설명 열의 역할을 초안 단계에서부터 구분해야 한다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 기준 시점은 다른 시점과 비교하기 위한 reference라고 설명하므로, baseline diff 같은 비교 역할 열을 별도로 두는 초안이 필요하다는 일반 근거가 됩니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
