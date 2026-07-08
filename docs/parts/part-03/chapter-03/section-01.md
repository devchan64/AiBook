# P3-3.1 원천데이터를 왜 곧바로 학습 문제로 읽으면 안 되는가

> Section ID: `P3-3.1`
> Version: `v2026.07.08`

원천데이터를 처음 받으면 많은 사람이 거의 반사적으로 `이걸로 무엇을 예측할까`부터 떠올립니다. 표가 있고 값이 많고 시간이 흐르며 측정된 기록도 보이니, 곧바로 어떤 학습 문제로 바꿀 수 있을 것처럼 느껴지기 때문입니다. 하지만 이 반응은 대개 너무 빠릅니다. 눈앞의 표는 아직 `학습용 데이터셋`이 아니라 `기록된 원천데이터`이거나, 많아야 `데이터셋 후보`일 가능성이 더 크기 때문입니다.

여기서는 `학습 문제의 틀`보다 `문제 구조`가 먼저라는 점을 고정합니다. 바로 다음 절에서 데이터셋을 어떻게 다시 설계하는지 더 구체적으로 보겠지만, 여기서는 아직 예측 문제, 분류 문제, 이상 징후 판별 문제처럼 학습 문제의 틀을 고르는 단계가 아니라는 경고를 먼저 분명히 합니다.

자동으로 실행되는 동작 1회마다 제어 파라미터 시계열과 센서 시계열이 남는 상황을 보겠습니다. 이런 표를 보면 다음 같은 생각이 먼저 나옵니다.

- 센서 값이 있으니 이상 징후 판별 문제로 바꿀 수 있겠다.
- 동작 결과가 조금 다르니 분류 문제로 바꾸면 되겠다.
- 시계열이 길면 시계열 예측 문제로 바로 넘길 수 있을 것 같다.

이 생각들 자체가 틀린 것은 아닙니다. 문제는 `무엇을 한 건으로 볼지`, `무엇을 맞히려는지`, `라벨이 실제로 있는지`도 정하지 않은 상태에서 학습 문제의 틀이 먼저 등장한다는 점입니다. 이 상태에서는 아직 데이터 문제를 정의한 것이 아니라, 데이터보다 학습 문제 틀을 먼저 떠올린 것입니다.

이런 일이 자주 생기는 이유는 분명합니다. 첫째, 표가 보이면 사람은 `이미 정리된 데이터셋`이라고 곧바로 받아들이곤 합니다. 둘째, AI 학습 경험이 학습 문제 유형 중심으로 남아 있으면 문제 표현보다 예측 방식이 먼저 떠오릅니다. 셋째, 원천 시계열이 길고 복잡할수록 `이걸 그대로 학습 문제로 넘길 수 있지 않을까`라는 기대가 먼저 앞섭니다.

하지만 원천데이터를 곧바로 데이터셋처럼 읽으면 중요한 질문이 빠집니다.

| 먼저 떠올리기 쉬운 질문 | 실제로 더 먼저 필요한 질문 |
| --- | --- |
| 어떤 학습 문제로 읽을까 | 무엇을 한 건의 샘플로 볼까 |
| 라벨을 무엇으로 둘까 | 지금 라벨이 정말 안정적으로 있는가 |
| 정확도를 어떻게 올릴까 | 어떤 표로 다시 묶어야 비교가 가능한가 |

이 차이는 단순한 순서 문제가 아닙니다. 원천데이터를 처음 볼 때 필요한 일은 학습 문제 선택이 아니라 `표의 정체를 다시 묻는 일`입니다. 지금 보고 있는 것이 시점별 측정 기록인지, 동작 1회 요약인지, 최근 구간 집계인지에 따라 뒤의 특징(feature), 기준선(baseline), 목표 라벨(target) 설명이 모두 달라집니다.

예를 들어 다음처럼 원천데이터의 일부만 보고도 너무 빨리 학습 문제의 틀이 튀어나올 수 있습니다.

| event_id | second | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |

이 표만 보면 `분류 문제`, `예측 문제`, `시계열 학습 문제` 같은 말을 쉽게 떠올릴 수 있습니다. 하지만 아직 이 표가 `한 시점 기록`인지, `동작 1회 표`인지조차 정하지 않았습니다. 따라서 여기서 바로 학습 문제 틀을 고르면 문제보다 문제 형식이 먼저 앞서게 됩니다.

문제 상황: 시점별 로그 표를 받았을 때, 이를 곧바로 학습 문제로 읽으면 어떤 핵심 질문이 비어 있는지 확인합니다.

입력(input): `event_id`별 여러 시점 측정값이 섞여 있는 원시 로그 표

기대 출력(output): `지금 바로 분류 문제로 읽기`와 `먼저 비어 있는 질문 채우기`가 다른 결과를 만든다는 점이 드러납니다.

확인할 개념: 원천데이터를 학습 문제처럼 읽기 전에 `샘플 1건`, `라벨 후보`, `비교 표`가 무엇인지 먼저 정해야 한다

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "pressure": 1.0, "flow": 0.0},
        {"event_id": "A", "second": 1, "pressure": 2.0, "flow": 1.4},
        {"event_id": "A", "second": 2, "pressure": 2.4, "flow": 1.6},
        {"event_id": "B", "second": 0, "pressure": 1.1, "flow": 0.1},
        {"event_id": "B", "second": 1, "pressure": 1.7, "flow": 1.0},
        {"event_id": "B", "second": 2, "pressure": 1.9, "flow": 1.1},
    ]
)

print("1) raw log")
print(raw)
print()

print("2) too-early reading")
print("- maybe this is a classification problem")
print("- label column: not found yet")
print("- one training sample: not decided yet")
print()

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        max_pressure=("pressure", "max"),
        mean_flow=("flow", "mean"),
    )
)
print("3) questions that must be settled first")
print("- one sample: one event")
print("- candidate comparison table: one row per event")
print("- label candidate: still not decided")
print()

print("4) event-level table after defining the sample")
print(event_summary)
```

예상 출력:

```text
1) raw log
  event_id  second  pressure  flow
0        A       0       1.0   0.0
1        A       1       2.0   1.4
2        A       2       2.4   1.6
3        B       0       1.1   0.1
4        B       1       1.7   1.0
5        B       2       1.9   1.1

2) too-early reading
- maybe this is a classification problem
- label column: not found yet
- one training sample: not decided yet

3) questions that must be settled first
- one sample: one event
- candidate comparison table: one row per event
- label candidate: still not decided

4) event-level table after defining the sample
  event_id  max_pressure  mean_flow
0        A           2.4   1.000000
1        B           1.9   0.733333
```

이 예제의 핵심은 2단계와 3단계의 차이입니다. 2단계에서는 `분류 문제일지도 모른다`는 말만 먼저 나오지만, 실제로는 라벨 열도 없고 샘플 1건도 아직 정해지지 않았습니다. 반대로 3단계에서는 먼저 `한 샘플은 동작 1회`, `비교 표는 동작별 1행`이라는 구조를 정합니다. 그 뒤에야 4단계처럼 비교 가능한 표가 생깁니다. 즉 원천데이터를 너무 빨리 학습 문제로 읽으면, 아직 비어 있는 질문을 덮어 둔 채 문제 형식만 먼저 정하게 됩니다.

실제로 학습 문제의 틀이 먼저 떠오를 때 비어 있는 질문을 나란히 적어 보면 문제가 더 분명해집니다.

| 먼저 튀어나오기 쉬운 말 | 아직 비어 있는 질문 |
| --- | --- |
| `이상 징후 판별 문제` | 무엇을 이상이라고 부를 것인가 |
| `분류 문제` | 라벨이 실제로 안정적으로 있는가 |
| `시계열 학습 문제` | 한 샘플은 한 시점 묶음인가, 동작 1회인가 |

이 표의 핵심은 학습 문제의 이름이 틀렸다는 데 있지 않습니다. 문제는 그 틀보다 먼저 답해야 할 질문이 아직 비어 있다는 점입니다. 데이터 모델링은 바로 그 빈칸을 채우는 앞단 설계입니다.

즉 원천데이터를 처음 받았을 때 가장 흔한 실수는 `기록 구조`를 `학습 구조`로 착각하는 것입니다. 시점별 로그가 있다는 사실만으로 아직 예측 문제가 정해진 것은 아닙니다. 그 로그를 어떤 단위로 묶고, 무엇을 남기고, 무엇과 비교할지 정해야 비로소 데이터셋이라는 말을 쓸 수 있습니다. 학습 문제의 틀이 먼저 떠오르면 이 앞단 설계가 건너뛰어지기 쉽고, 뒤에서 샘플 단위와 표 구조를 다시 뜯어고치게 됩니다.

## 일반화된 상위 프레임으로 다시 보면

이 절은 학습 문제 이름을 늦게 고르자는 조언이 아니라, `문제 승격(problem escalation)`의 시점을 관리하는 문제로 다시 볼 수 있습니다.

| 상위 프레임 | 이 절에서의 대응 |
| --- | --- |
| 기록 구조 확인 | 지금 손에 있는 것이 원천 로그인지, 요약 표인지 구분 |
| 샘플/라벨 공백 확인 | 한 샘플과 안정된 label이 아직 없는지 점검 |
| 학습 문제 승격 보류 | 비교 가능한 표가 생기기 전에는 문제 틀을 고정하지 않음 |

결국 이 절의 핵심은 `모델 이름을 늦게 떠올리자`가 아니라, 샘플 단위와 라벨 후보가 정리되기 전까지는 학습 문제로 성급히 승격하지 않는 판단에 있습니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. labeled example은 features와 label로 구성된다고 설명하므로, 아직 샘플 1건과 label이 정해지지 않은 원천데이터를 곧바로 학습 문제로 읽으면 안 된다는 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. feature가 label의 proxy가 되는 설계 결함을 설명하므로, 문제 틀을 먼저 고르면 아직 정리되지 않은 원천 열을 잘못된 학습 구조로 읽을 위험이 있다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. provenance framework가 identifying an object와 representing derivation을 지원해야 한다고 정리하므로, 무엇을 한 대상(example)로 보고 어떤 변환을 거쳐 데이터셋 후보를 만들었는지 먼저 정리해야 한다는 상위 프레임을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
