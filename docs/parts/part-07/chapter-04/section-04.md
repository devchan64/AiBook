# P7-4.4 같은 평균, 다른 패턴 비교 연습

> Section ID: `P7-4.4`
> Version: `v2026.07.19`

평균이 같으면 같은 데이터처럼 보이기 쉽습니다. 하지만 동작 단위 시계열에서는 같은 평균을 가진 두 신호도 완전히 다른 패턴일 수 있습니다. 이번 절은 평균(mean)만 남겼을 때 사라지는 정보를 `shape token`과 간단한 패턴 요약으로 다시 읽는 연습입니다.

핵심은 평균이 틀렸다는 뜻이 아닙니다. 평균은 빠른 비교에 유용하지만, 구간 순서와 모양을 지웁니다. 프로젝트 회고에서는 `평균이 같다`와 `같은 흐름이다`를 구분해야 합니다.

## 평균과 패턴이 가르는 질문

- 평균이 같은 동작을 정말 같은 상태로 묶어도 되는가?
- 구간 순서를 잃으면 어떤 실패 해석이 사라지는가?
- shape token은 세부 수치를 버리는 대신 어떤 판단 정보를 남기는가?

이 절의 핵심은 `값을 줄이는 요약`과 `판단에 필요한 정보를 남기는 표현`을 구분하는 데 있습니다. 평균은 전체 크기를 빠르게 비교하게 해 주지만, 상승형과 하강형처럼 회고에서 중요한 흐름 차이는 숨길 수 있습니다.

## 연습 뒤 남겨야 할 판단

- 평균만 남긴 묶음과 shape token까지 남긴 묶음이 어떻게 달라지는지 설명할 수 있습니다.
- 평균이 같은 사례에서도 왜 서로 다른 다음 조치가 필요할 수 있는지 적을 수 있습니다.
- 표현을 단순화할 때 어떤 정보 손실(information loss)을 받아들이는지 문서에 남길 수 있습니다.

## 왜 평균만으로 부족한가

네 구간 값이 모두 다음처럼 평균 2.5라고 해도, 읽어야 할 이야기는 서로 다릅니다.

| 패턴 | 구간 값 | 평균 | 사람이 읽는 차이 |
| --- | --- | --- | --- |
| 상승형 | 1.8, 2.2, 2.7, 3.3 | 2.5 | 후반으로 갈수록 값이 커진다 |
| 평탄형 | 2.5, 2.5, 2.5, 2.5 | 2.5 | 전체 구간이 안정적이다 |
| 하강형 | 3.2, 2.8, 2.2, 1.8 | 2.5 | 후반으로 갈수록 값이 낮아진다 |

평균 하나만 남기면 이 차이는 사라집니다. 그래서 표현 설계에서는 숫자를 줄이더라도 어떤 정보를 보존할지 먼저 정해야 합니다.

## 입력 파일

- 파일 경로: [`p7-action-unit-pattern-pairs.csv`](../../../assets/part-07/chapter-04/p7-action-unit-pattern-pairs.csv)
- 한 행의 의미: `동작 1회의 네 구간 요약`
- 핵심 열: `segment_1`, `segment_2`, `segment_3`, `segment_4`, `expected_shape`

이 파일은 공개형 합성 데이터입니다. 실제 장비 수치를 재현하려는 데이터가 아니라, 평균과 패턴 표현의 차이를 드러내기 위한 작은 비교표입니다.

## 연습 흐름

1. 각 동작의 네 구간 평균을 계산합니다.
2. 평균이 같은 동작끼리 묶습니다.
3. 구간 값의 흐름을 `rising`, `falling`, `flat`, `middle_high`, `edge_high`, `mixed` 같은 shape token으로 바꿉니다.
4. 평균만 남겼을 때와 shape token까지 남겼을 때 어떤 회고 문장이 달라지는지 비교합니다.

## 이 절에서 직접 할 일

- 같은 평균으로 묶이는 동작 목록을 먼저 확인합니다.
- shape token을 붙였을 때 평균 묶음이 몇 갈래로 다시 나뉘는지 봅니다.
- `평균만 쓴 회고`와 `평균 + shape token을 쓴 회고`를 한 문장씩 나란히 씁니다.
- 표현을 더 단순하게 합쳤을 때 사라지는 판단 정보를 적습니다.

## Python 예제

이번 예제의 목적은 같은 평균을 가진 동작들이 shape token에서는 다르게 갈리는 장면을 확인하는 것입니다.

```python
import csv
from pathlib import Path

data_path = Path("docs/assets/part-07/chapter-04/p7-action-unit-pattern-pairs.csv")
rows = list(csv.DictReader(data_path.open(encoding="utf-8")))

def values(row):
    return [float(row[f"segment_{index}"]) for index in range(1, 5)]

def shape_token(items):
    first, second, third, fourth = items
    if first < second < third < fourth:
        return "rising"
    if first > second > third > fourth:
        return "falling"
    if len({round(value, 2) for value in items}) == 1:
        return "flat"
    if second > first and third > fourth:
        return "middle_high"
    if first > second and fourth > third:
        return "edge_high"
    return "mixed"

records = []
for row in rows:
    items = values(row)
    average = round(sum(items) / len(items), 3)
    token = shape_token(items)
    records.append({
        "event_id": row["event_id"],
        "pair_id": row["pair_id"],
        "average": average,
        "shape_token": token,
        "expected_shape": row["expected_shape"],
        "average_only_key": f"avg={average}",
        "pattern_key": f"avg={average};shape={token}",
    })

average_groups = {}
for row in records:
    average_groups.setdefault(row["average_only_key"], []).append(row["event_id"])

pattern_groups = {}
for row in records:
    pattern_groups.setdefault(row["pattern_key"], []).append(row["event_id"])

summary = {
    "event_count": len(records),
    "average_groups": average_groups,
    "pattern_groups": pattern_groups,
    "mismatch": [
        row["event_id"]
        for row in records
        if row["shape_token"] != row["expected_shape"]
    ],
}

print("패턴 비교 요약 =", summary)
for row in records:
    print(row)
```

실행 결과는 다음처럼 읽을 수 있습니다.

```text
패턴 비교 요약 = {'event_count': 6, 'average_groups': {'avg=2.5': ['PAT-01', 'PAT-02', 'PAT-03', 'PAT-04', 'PAT-05', 'PAT-06']}, 'pattern_groups': {'avg=2.5;shape=rising': ['PAT-01'], 'avg=2.5;shape=flat': ['PAT-02'], 'avg=2.5;shape=falling': ['PAT-03'], 'avg=2.5;shape=middle_high': ['PAT-04', 'PAT-05'], 'avg=2.5;shape=edge_high': ['PAT-06']}, 'mismatch': []}
{'event_id': 'PAT-01', 'pair_id': 'A', 'average': 2.5, 'shape_token': 'rising', 'expected_shape': 'rising', 'average_only_key': 'avg=2.5', 'pattern_key': 'avg=2.5;shape=rising'}
{'event_id': 'PAT-02', 'pair_id': 'A', 'average': 2.5, 'shape_token': 'flat', 'expected_shape': 'flat', 'average_only_key': 'avg=2.5', 'pattern_key': 'avg=2.5;shape=flat'}
{'event_id': 'PAT-03', 'pair_id': 'B', 'average': 2.5, 'shape_token': 'falling', 'expected_shape': 'falling', 'average_only_key': 'avg=2.5', 'pattern_key': 'avg=2.5;shape=falling'}
{'event_id': 'PAT-04', 'pair_id': 'B', 'average': 2.5, 'shape_token': 'middle_high', 'expected_shape': 'middle_high', 'average_only_key': 'avg=2.5', 'pattern_key': 'avg=2.5;shape=middle_high'}
{'event_id': 'PAT-05', 'pair_id': 'C', 'average': 2.5, 'shape_token': 'middle_high', 'expected_shape': 'middle_high', 'average_only_key': 'avg=2.5', 'pattern_key': 'avg=2.5;shape=middle_high'}
{'event_id': 'PAT-06', 'pair_id': 'C', 'average': 2.5, 'shape_token': 'edge_high', 'expected_shape': 'edge_high', 'average_only_key': 'avg=2.5', 'pattern_key': 'avg=2.5;shape=edge_high'}
```

## 결과를 어떻게 읽는가

평균만 보면 여섯 동작은 모두 `avg=2.5`라는 같은 묶음에 들어갑니다. 이 결과만 남기면 `PAT-01`의 상승형, `PAT-03`의 하강형, `PAT-06`의 양끝 집중형은 구분되지 않습니다.

shape token을 붙이면 같은 평균 안에서도 패턴이 다시 갈립니다. `PAT-01`은 `rising`, `PAT-02`는 `flat`, `PAT-03`은 `falling`입니다. `PAT-04`와 `PAT-05`는 같은 `middle_high`로 묶이지만, `PAT-06`은 `edge_high`로 따로 떨어집니다.

이 차이는 정보 손실(information loss)을 읽는 작은 예입니다. 평균은 값을 줄여 비교를 쉽게 만들지만, 구간 순서와 모양을 지웁니다. 반대로 shape token은 세부 수치를 줄이지만, 회고에 필요한 흐름 차이를 남깁니다.

## 관찰 포인트

| 관찰 | 읽어야 할 뜻 |
| --- | --- |
| 모든 동작이 `avg=2.5`에 들어간다 | 평균만으로는 패턴 차이를 설명할 수 없다 |
| `rising`, `flat`, `falling`이 갈라진다 | 같은 크기라도 시간 흐름이 다르면 다른 사례다 |
| `middle_high`가 두 건으로 묶인다 | 표현은 차이를 나누기도 하지만 다시 묶기도 한다 |
| `edge_high`가 따로 떨어진다 | 평균이 같아도 검토 우선순위가 달라질 수 있다 |

## 기록 템플릿

```text
비교 단위:
평균만 남겼을 때의 묶음:
shape token을 붙였을 때 새로 보인 차이:
사라질 수 있는 정보:
다음 표현 선택:
```

## 회고 문장으로 닫기

실습 뒤에는 다음처럼 기록할 수 있습니다.

> 평균만 보면 `PAT-01`부터 `PAT-06`까지 모두 같은 `avg=2.5`로 묶인다. 하지만 shape token을 붙이면 상승형, 평탄형, 하강형, 중간 집중형, 양끝 집중형으로 갈라진다. 따라서 이번 프로젝트에서는 평균만으로 동작 상태를 비교하면 패턴 차이를 잃을 수 있으므로, 회고 표에는 평균과 shape token을 함께 남기는 편이 적절하다.

## 직접 바꿔 보며 확인할 것

1. `PAT-02`의 네 값을 `2.4, 2.6, 2.4, 2.6`으로 바꿔 봅니다.
   관찰할 점: 평균은 그대로인데 `flat`으로 보던 판단이 어떻게 달라지는가?

2. `PAT-03`의 마지막 값을 `2.1`로 올려 봅니다.
   관찰할 점: 하강형 판단이 약해질 때 `falling`을 그대로 써도 되는가?

3. `middle_high`와 `edge_high`를 더 세분화하지 않고 하나의 `non_flat`으로 합쳐 봅니다.
   관찰할 점: 표현을 단순하게 만들면 어떤 회고 정보가 사라지는가?

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 평균 묶음 | 평균이 같은 동작을 먼저 묶어 보았는가? |
| 순서 정보 | 평균만 남겼을 때 사라지는 구간 순서 정보를 확인했는가? |
| shape token | 세부 수치를 버리는 대신 어떤 패턴 정보를 보존하는지 설명했는가? |
| 단순화 | `non_flat`처럼 표현을 단순하게 만들 때 잃는 정보를 적었는가? |
| 회고 | 평균과 shape token을 함께 남겨야 하는 이유를 한 문장으로 정리했는가? |

## 출처와 참고 자료

- 동작 단위 패턴 비교 파일: [`p7-action-unit-pattern-pairs.csv`](../../../assets/part-07/chapter-04/p7-action-unit-pattern-pairs.csv)
- 이 문서는 자체 합성 데이터와 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.
