# P3-9.8 예측 점수는 어떤 규칙을 거쳐 행동으로 이어지는가

> Section ID: `P3-9.8`
> Version: `v2026.09.15`

입력과 결과를 정한 뒤에도 예측 문제는 아직 반쯤만 닫힌 상태입니다. 같은 `review_needed` 예측이라도 그것이 동작 1건을 [검토 후보 큐(review queue)](../../../reference/concept-glossary-parts/05-mieum.md#output-structure)에 올리는 일인지, 최근 구간 전체의 경고 강도를 조정하는 일인지가 다를 수 있기 때문입니다. 또한 모델이 낸 [점수(score)](../../../reference/concept-glossary-parts/05-mieum.md#glossary-score)와 그 점수로 실제 행동을 정하는 [정책 규칙(policy rule)](../../../reference/concept-glossary-parts/08-ieung.md#decision)도 같은 것이 아닙니다.

예측값 하나는 어떤 단위의 어떤 행동과 연결되는지 적어야 하고, 모델 점수와 판단 규칙은 분리해서 봐야 합니다.

| 구분 | 질문 |
| --- | --- |
| 예측 1회의 대상 단위 | 이 값 하나는 동작 1건, 최근 구간 1개, 다음 사례 1건 중 무엇을 가리키는가 |
| 모델 출력 | 모델은 점수, 0/1, 순위 중 무엇을 내는가 |
| [정책 규칙(policy rule)](../../../reference/concept-glossary-parts/08-ieung.md#decision) | 그 출력을 어떤 기준으로 행동으로 바꾸는가 |
| [실제 행동(action)](../../../reference/concept-glossary-parts/14-hieut.md#action) | 검토 큐 등록, 보류, 자동 조치 중 무엇이 일어나는가 |

| 층위 | 예시 |
| --- | --- |
| 모델 출력 | `0.82`, `warning_score` |
| [정책 규칙(policy rule)](../../../reference/concept-glossary-parts/08-ieung.md#decision) | `0.8 이상이면 검토`, `상위 10%만 본다` |
| 실제 행동 | 검토 큐 등록, 우선순위 조정 |

실제 표로 넘길 때는 `prediction_unit`, `score_column`, `decision_threshold`, `policy_version`, `action_column`처럼 서로 다른 층위의 필드를 분리해 둡니다. 이렇게 적어 두면 모델이 낸 값, 그 값을 행동으로 바꾸는 기준, 실제로 실행되는 조치가 같은 말처럼 섞이지 않습니다.

같은 점수라도 정책이 다르면 행동이 달라질 수 있습니다. 또한 어떤 문제는 점수를 [순위화(ranking)](../../../reference/concept-glossary-parts/07-siot.md#glossary-ranking)에만 쓰고, 어떤 문제는 숫자 자체를 [확률 추정값(probability estimate)](../../../reference/concept-glossary-parts/14-hieut.md#probability-estimate)처럼 읽고 싶어 할 수 있습니다. 이 차이도 먼저 적어 두어야 합니다. 즉 예측 1회의 의미는 `숫자 하나를 내는 일`이 아니라, 그 숫자가 어떤 규칙을 거쳐 어떤 행동으로 이어지는지까지 포함한 결정 구조입니다. 더 넓게 보면 이 절은 `모델 출력`, `판정 규칙`, `실제 행동`이 서로 다른 층위라는 점을 분리해, 예측값 하나를 운영 결정 구조 안에서 읽게 합니다.

## 점수에서 임계값과 운영 정책으로 {#_1}

예측 1회는 점수 하나로 끝나지 않고, 그 점수가 정책 규칙을 거쳐 어떤 행동으로 연결되는지까지 봐야 합니다.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-8-mermaid-01-ko.mmd"
```

예를 들어 하루 10건만 검토할 수 있다면 점수순 상위 10건을 고르는 규칙과 `점수 0.7 이상` 규칙은 다른 결과를 낼 수 있습니다. 0.7 이상이 30건이면 처리 용량을 넘기 때문입니다. 점수가 0~1 범위라는 이유만으로 발생 확률이라고 읽어서도 안 됩니다. 점수의 뜻과 행동 규칙, 처리 가능한 건수를 별도로 기록합니다.

가상 사례 A·B·C의 점수가 각각 0.82, 0.80, 0.79이고 오늘 검토 가능한 건수가 2건이라고 합시다. `0.80 이상` 규칙과 `상위 2건` 규칙은 모두 A·B를 고릅니다. 이제 D가 0.95로 추가되면 어떻게 될까요? 임계값 규칙은 D·A·B의 3건을 고르고, 상위 2건 규칙은 D·A만 고릅니다. B의 점수는 변하지 않았지만 선택 여부는 달라졌습니다.

임계값을 넘은 3건 중 2건만 오늘 처리한다면 B에는 `기준 미달` 대신 `기준 충족, 용량 부족으로 대기`라고 남겨야 합니다. 이를 위해 기준 충족 여부와 오늘의 처리 상태를 별도 열로 둡니다. 그래야 나중에 B가 선택되지 않은 이유를 모델 점수 부족과 처리 용량 부족으로 구분할 수 있습니다.

## 체크리스트

- 점수와 행동을 연결하는 임계값 또는 상위 건수 규칙을 적었는가?
- 하루 검토 용량보다 후보가 많을 때의 처리 규칙을 설명했는가?

## 출처와 참고 자료

- Google, *Thresholds and the confusion matrix*. 모델의 원시 숫자 출력을 범주로 바꾸려면 분류 임계값을 선택해야 하고, 임계값이 달라지면 예측 결과가 달라질 수 있다는 설명을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google, *Classification: ROC and AUC*. AUC가 양성 예시를 음성 예시보다 높게 순위화하는 능력과 연결되고, 실제 분류는 선택한 임계값에 따라 달라진다는 설명을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google, *Machine Learning Glossary*, `classification threshold`, `AUC`. 임계값과 AUC 용어 기준을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
