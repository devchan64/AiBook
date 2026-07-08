# P3-5.7 같은 샘플 뒤의 여러 후속 사건은 표 구조에서 어떻게 접어야 하는가

> Section ID: `P3-5.7`
> Version: `v2026.07.08`

샘플 단위와 입력 창을 정한 뒤에도 표 구조에서 한 번 더 막히는 지점이 있습니다. 같은 샘플 뒤에 후속 사건이 여러 개 붙는 경우입니다. 예를 들어 동작 1회 뒤에 `재점검`, `경고`, `실패`, `재방문`이 차례로 남을 수 있습니다. 이때 이를 하나의 결과 열로 어떻게 접을지 정하지 않으면, 같은 샘플이 표마다 다른 뜻으로 바뀌기 쉽습니다.

후속 사건이 여러 개라면 어떤 규칙으로 하나의 표 구조에 접었는지 먼저 적어야 합니다.

보통 아래 같은 접기 규칙이 생깁니다.

| 접기 규칙 | 뜻 |
| --- | --- |
| `any` | 하나라도 발생했으면 1 |
| `first` | 가장 먼저 나온 후속 사건을 대표로 둠 |
| `worst` | 가장 심한 상태를 대표로 둠 |
| `count` | 발생 횟수 자체를 남김 |

예를 들어 같은 샘플 뒤에 아래처럼 후속 사건이 남았다고 해 보겠습니다.

| event_id | follow_up_events |
| --- | --- |
| A | review, failure |
| B | review |
| C | none |

이를 어떤 표로 접을지에 따라 결과 열의 뜻이 달라집니다.

| event_id | any_failure | first_event | event_count |
| --- | ---: | --- | ---: |
| A | 1 | review | 2 |
| B | 0 | review | 1 |
| C | 0 | none | 0 |

즉 같은 원천 사건을 보고 있어도 `무엇을 대표 결과로 둘 것인가`에 따라 표 구조가 달라집니다. 이 문제는 대표 결과를 어떤 규칙으로 접어 표에 남길지 먼저 정해야 하는 데이터 모델링 문제입니다.

아래 메모를 먼저 남겨 두면 이후 혼동이 줄어듭니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 어떤 후속 사건들을 한 묶음으로 보는가 | 표가 다루는 결과 범위를 고정하기 위해 |
| `any`, `first`, `worst`, `count` 중 무엇으로 접었는가 | 결과 열의 뜻을 다시 설명하기 위해 |
| 접은 결과가 보고용인지 예측 후보용인지 | 비교 리포트와 target 후보를 섞지 않기 위해 |

작은 예시:

```python
import pandas as pd

follow_ups = {
    "A": ["review", "failure"],
    "B": ["review"],
    "C": [],
}

severity = {"none": 0, "review": 1, "warning": 2, "failure": 3}
rows = []
for event_id, events in follow_ups.items():
    first_event = events[0] if events else "none"
    worst_event = max(events, key=lambda name: severity[name]) if events else "none"
    rows.append(
        {
            "event_id": event_id,
            "any_failure": int("failure" in events),
            "first_event": first_event,
            "worst_event": worst_event,
            "event_count": len(events),
        }
    )

result = pd.DataFrame(rows)
print(result)
```

예상 출력:

```text
  event_id  any_failure first_event worst_event  event_count
0        A            1      review     failure            2
1        B            0      review      review            1
2        C            0        none        none            0
```

이 예시의 핵심은 같은 원천 사건을 보고도 `first_event`는 `review`, `worst_event`는 `failure`, `event_count`는 2처럼 서로 다른 결과 열이 동시에 만들어질 수 있다는 점입니다. 즉 어떤 규칙으로 접었는지를 적지 않으면 같은 `A` 샘플도 표마다 다른 뜻으로 읽히게 됩니다. 같은 샘플 뒤에 여러 후속 사건이 있다면, 어떤 규칙으로 하나의 결과 열에 접었는지 먼저 적어야 표 구조의 뜻이 흔들리지 않습니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `label`과 `labeled example`. result information이 어떤 example에 붙는지 먼저 정해져야 하므로, 후속 사건 여러 개를 하나의 결과 열로 접을 때도 `any`, `first`, `worst`, `count` 가운데 어떤 규칙을 썼는지 먼저 명세해야 한다는 이 절의 판단을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. 결과 열이 어떤 규칙으로 만들어졌는지 불분명하면 보고용 결과와 예측 후보용 결과를 섞어 읽기 쉬우므로, 접기 규칙을 먼저 적어 표 구조의 뜻을 고정해야 한다는 설명을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. provenance framework가 derivation과 activity context를 설명 가능하게 남겨야 한다고 정리하므로, 여러 후속 사건이 어떤 규칙을 거쳐 대표 결과 열로 접혔는지 추적 가능해야 한다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
