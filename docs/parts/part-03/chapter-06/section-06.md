# P3-6.6 같은 열 이름과 다른 특징

> Section ID: `P3-6.6`
> Version: `v2026.07.23`

_보조제목: 측정 방식이나 단위가 바뀌면 왜 같은 이름의 열도 다른 특징이 될 수 있는가_

특징(feature)을 설계하다 보면 놓치기 쉬운 함정이 하나 더 있습니다. `열 이름이 같으니 같은 특징이겠지`라고 생각하는 순간입니다. 하지만 현실 데이터에서는 같은 `flow_mean`이라는 이름 아래에서도 센서 버전이 바뀌었거나, 단위가 바뀌었거나, 계산 규칙이 달라졌을 수 있습니다. 이런 변화가 있으면 숫자는 있어도 더 이상 같은 특징이라고 보기 어렵습니다.

특징은 열 이름이 아니라, `무엇을 어떤 규칙과 단위로 측정한 값인가`까지 포함해 같은 특징인지 판단해야 합니다.

## 같은 열 이름이 같은 특징을 뜻하지 않는 경우

같은 열 이름만 보고 같은 특징이라고 넘기면, 실제로는 특징 의미가 이미 달라졌는데도 같은 비교표와 같은 기준선에 올리기 쉽습니다.

| 겉으로 보이는 상태 | Part 3에서 먼저 확인할 질문 |
| --- | --- |
| 열 이름이 그대로다 | 계산 규칙과 단위도 그대로인가 |
| 평균값 분포가 갑자기 달라졌다 | 실제 변화인가, 측정 방식 변화인가 |
| 유지보수 이후 값이 달라졌다 | 공정 상태 변화인가, 센서 정의 변화인가 |

즉 특징 이름이 같다는 사실만으로는 같은 비교 구조가 유지된다고 말할 수 없습니다.

## 무엇이 바뀌면 같은 특징이 아니게 되는가

같은 열 이름이라도 아래 중 하나가 바뀌면, Part 3에서는 먼저 `같은 특징인가`를 다시 물어야 합니다.

| 바뀐 것 | 왜 중요한가 |
| --- | --- |
| 측정 단위 | 숫자 크기 비교 자체가 달라지기 때문 |
| 센서 위치나 센서 버전 | 같은 이름이어도 다른 물리량에 가까워질 수 있기 때문 |
| 구간 계산 규칙 | 같은 평균이라도 다른 구간을 평균 낸 것일 수 있기 때문 |
| 운영 정의 | 같은 `정상 범위`라도 기준이 달라졌을 수 있기 때문 |

이 네 가지는 모두 모델 기법 문제가 아니라, `지금 남긴 특징이 무엇을 뜻하는가`의 문제입니다.

## 작은 도식으로 보기

| event_id | flow_mean | flow_unit | sensor_version | segment_rule | ops_definition |
| --- | ---: | --- | --- | --- | --- |
| A | 2.4 | L/min | v1 | early-mid-late | normal-band-v1 |
| B | 2.5 | L/min | v1 | early-mid-late | normal-band-v1 |
| C | 41.0 | mL/s | v2 | early-mid-late | normal-band-v1 |
| D | 39.5 | mL/s | v2 | quartile-4bin | normal-band-v2 |

이 표를 보면 모두 `flow_mean`이라는 이름을 쓰지만 실제로는 두 가지 이상이 동시에 바뀌었습니다.

1. `A`, `B`와 `C`, `D`는 단위가 다릅니다.
2. `C`, `D`는 센서 버전도 다릅니다.
3. `D`는 구간 계산 규칙도 다릅니다.
4. `D`는 운영 정의도 달라 같은 기준선 메모로 바로 묶기 어렵습니다.

즉 이 네 행을 같은 특징 한 열로 그대로 읽으면, 숫자가 비슷한지 아닌지를 말하기 전에 특징 뜻부터 흔들리게 됩니다. 그래서 여기서 먼저 붙잡아야 할 결론은 단순합니다. `같은 열 이름`은 `같은 특징 정의`를 보장하지 않습니다.

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-6-mermaid-01-ko.mmd"
```

## 그래서 지금 단계에서 무엇을 먼저 적어야 하는가

Part 3에서는 아직 복잡한 보정 기법보다, 특징 정의 메모를 먼저 남기는 편이 중요합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 단위(unit) | 절대 크기 비교가 가능한지 보려면 필요하기 때문 |
| 생성 규칙(rule) | 같은 구간, 같은 계산 방식인지 확인해야 하기 때문 |
| 수집 버전(version) | 센서/파이프라인 변경을 구분해야 하기 때문 |
| 비교 가능 여부 | 같은 기준선에 바로 넣어도 되는지 판단해야 하기 때문 |

이 메모는 설명이 장황해지기 위한 것이 아니라, `같은 열 이름` 착시를 막기 위한 최소한의 구조 정보입니다.

## 왜 기준선 비교도 함께 흔들리는가

같은 특징이 아니게 되면 Chapter 7의 기준선 비교도 바로 흔들립니다.

| 현재 보이는 현상 | 실제로는 무엇이 흔들릴 수 있는가 |
| --- | --- |
| 최근 값이 평소보다 높아졌다 | 공정 변화가 아니라 단위/센서 변화일 수 있다 |
| 유지보수 이후 diff가 계속 크다 | 기준선 집단과 측정 정의가 달라졌을 수 있다 |
| 특정 시점부터 변동성이 커졌다 | 계산 구간 규칙이 바뀌었을 수 있다 |

즉 기준선은 같은 집단 비교만이 아니라, `같은 특징 정의` 비교여야 합니다. 이 메모를 남겨 두어야 `모델이 이상하다`고 보기 전에 먼저 `같은 특징 정의가 섞였는가`를 점검할 수 있습니다.

## 작은 코드 예시

문제 상황: 같은 `flow_mean`이라는 열 이름을 써도 단위, 센서 버전, 구간 규칙, 운영 정의가 다르면 같은 특징이 아닐 수 있다는 점을 확인합니다.

입력(input): `feature_name`, `unit`, `sensor_version`, `segment_rule`, `ops_definition`이 함께 적힌 특징 카탈로그 표와 같은 정의로 볼 때 사용할 필드 묶음 `definition_fields_to_check`

기대 출력(output): 열 이름만 볼 때는 한 그룹처럼 보이지만, `definition_fields_to_check`에 단위·센서 버전·구간 규칙·운영 정의를 포함하면 `same_definition_group`이 여러 개로 갈라지는 출력

확인할 개념: 특징 동일성은 열 이름이 아니라 측정 단위와 생성 규칙까지 포함한 정의 수준에서 판단해야 한다. 어떤 필드를 정의에 포함하느냐에 따라 같은 기준선에 묶을 수 있는 행도 달라진다.

```python
# 같은 열 이름의 특징이라도 측정 방식과 단위가 바뀌었는지 점검하는 예제입니다.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)

definition_fields_to_check = [
    "feature_name",
    "unit",
    "sensor_version",
    "segment_rule",
    "ops_definition",
]

feature_catalog = pd.DataFrame(
    [
        {
            "event_id": "A",
            "feature_name": "flow_mean",
            "unit": "L/min",
            "sensor_version": "v1",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "B",
            "feature_name": "flow_mean",
            "unit": "L/min",
            "sensor_version": "v1",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "C",
            "feature_name": "flow_mean",
            "unit": "mL/s",
            "sensor_version": "v2",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "D",
            "feature_name": "flow_mean",
            "unit": "mL/s",
            "sensor_version": "v2",
            "segment_rule": "quartile-4bin",
            "ops_definition": "normal-band-v2",
        },
    ]
)

def summarize_groups(fields):
    grouped = (
        feature_catalog.groupby(fields, as_index=False)
        .agg(
            event_count=("event_id", "count"),
            event_ids=("event_id", lambda values: ",".join(values)),
        )
        .copy()
    )
    grouped["same_definition_group"] = grouped[fields].astype(str).agg("|".join, axis=1)
    return grouped[["same_definition_group", "event_count", "event_ids"]]

name_only_groups = summarize_groups(["feature_name"])
definition_groups = summarize_groups(definition_fields_to_check)
group_comparison = pd.DataFrame(
    [
        {
            "grouping_rule": "feature_name only",
            "group_count": len(name_only_groups),
            "grouped_event_ids": " / ".join(name_only_groups["event_ids"]),
        },
        {
            "grouping_rule": "selected definition fields",
            "group_count": len(definition_groups),
            "grouped_event_ids": " / ".join(definition_groups["event_ids"]),
        },
    ]
)

print("1) same column name, different definition notes")
print(
    feature_catalog[
        [
            "event_id",
            "feature_name",
            "unit",
            "sensor_version",
            "segment_rule",
            "ops_definition",
        ]
    ]
)
print()
print("2) grouping changes when definition fields are included")
print(group_comparison)
print()
print("3) rows that can be treated as the same definition group")
print(definition_groups)
```

예상 출력:

```text
1) same column name, different definition notes
  event_id feature_name   unit sensor_version    segment_rule  ops_definition
0        A    flow_mean  L/min             v1  early-mid-late  normal-band-v1
1        B    flow_mean  L/min             v1  early-mid-late  normal-band-v1
2        C    flow_mean   mL/s             v2  early-mid-late  normal-band-v1
3        D    flow_mean   mL/s             v2   quartile-4bin  normal-band-v2

2) grouping changes when definition fields are included
                grouping_rule  group_count grouped_event_ids
0           feature_name only            1           A,B,C,D
1  selected definition fields            3       A,B / C / D

3) rows that can be treated as the same definition group
                              same_definition_group  event_count event_ids
0  flow_mean|L/min|v1|early-mid-late|normal-band-v1            2       A,B
1   flow_mean|mL/s|v2|early-mid-late|normal-band-v1            1         C
2    flow_mean|mL/s|v2|quartile-4bin|normal-band-v2            1         D
```

이 예제의 목적은 새 특징을 계산하는 것이 아니라, `같은 열 이름이라도 실제로는 어디까지를 같은 정의로 묶을 수 있는가`를 먼저 확인하는 데 있습니다. 여기서 조작할 값은 `definition_fields_to_check`입니다. 1단계에서는 네 행이 모두 `flow_mean`이지만 정의 메모가 다르다는 점을 봅니다. 2단계에서는 `feature_name`만 보면 `A,B,C,D`가 모두 한 그룹처럼 보이지만, 단위·센서 버전·구간 규칙·운영 정의까지 포함하면 `A,B`, `C`, `D`의 세 그룹으로 갈라진다는 점을 봅니다. 3단계는 실제로 `A,B`만 같은 정의 그룹으로 묶이고 `C`, `D`는 각각 따로 남는다는 점을 보여 줍니다. 즉 이 절에서 중요한 것은 내부 키 문자열 자체가 아니라, 어떤 행끼리만 같은 기준선과 같은 비교표에 올릴 수 있는지를 먼저 가르는 일입니다.

여기서 마지막으로 확인할 것은 세 가지입니다. 단위와 계산 규칙이 메모되어 있는지, 버전 변경이나 센서 변경을 구분했는지, 기준선과 분할에 섞이면 안 되는 정의 차이를 표시했는지입니다. 이 세 조건이 함께 서야 특징 표는 단순 숫자 모음이 아니라, 비교 가능한 정의가 붙은 구조로 남습니다. 현재 특징 표가 같은 뜻의 열끼리만 비교 가능한 구조인지 확인하는 일이 바로 이 절의 중심입니다.

같은 열 이름이라도 측정 단위, 센서 버전, 계산 규칙이 바뀌면 더 이상 같은 특징이 아닐 수 있으므로, Part 3에서는 숫자보다 먼저 특징 정의가 같은지 확인해야 합니다. 이 절은 열 이름 관리 요령이 아니라, `같은 특징 정의를 어떻게 식별할 것인가(feature-definition identity)`의 문제로 다시 볼 수 있습니다.


따라서 특징 동일성은 열 이름 한 줄이 아니라, 무엇을 어떤 규칙과 버전으로 만들었는지까지 포함한 정의 묶음으로 읽어야 합니다.

## 출처와 참고 자료

- W3C, `PROV-Overview`. provenance information을 통해 데이터가 어떤 과정과 버전을 거쳐 생성되었는지 추적하는 일반 틀을 제공하므로, 특징도 이름만이 아니라 생성 규칙과 버전까지 함께 남겨야 비교 가능성이 유지된다는 설명을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `feature engineering`. feature가 원시 값을 그대로 쓰는 것이 아니라 선택된 변환의 결과라는 점을 설명하므로, 단위나 계산 규칙이 달라지면 같은 열 이름이어도 같은 특징 정의라고 보기 어렵다는 이 절의 핵심을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
