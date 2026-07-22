# P7-7.4 경고 등급 설계 연습

Section ID: `P7-7.4`
Version: `v2026.07.22`

운영 신호를 세 행동 구간으로 나누는 것만으로는 충분하지 않을 때가 있습니다. 같은 `재현 확인` 후보 안에서도 어떤 신호는 지켜보기만 하면 되고, 어떤 신호는 바로 검토 대기열 앞쪽으로 올려야 합니다. 동작 단위 합성 데이터를 이용해 `watch`, `review`, `action` 등급을 직접 설계하는 연습입니다.

핵심은 큰 차이값 하나를 곧바로 문제 확정으로 읽지 않는 데 있습니다. `gap`이 커도 표본 수가 적고 반복성이 낮으면 `watch`에 머물 수 있고, 차이값이 중간 정도라도 최근 구간에서 반복되고 독자 영향이 크면 `review`나 `action`으로 올라갈 수 있습니다.

## 경고 등급이 가르는 질문

- 큰 gap 하나를 바로 `action`으로 올려도 되는가?
- 표본 수가 적거나 반복성이 낮은 신호는 왜 낮은 등급으로 둬야 하는가?
- 독자 영향이 큰 신호는 원인 확정 전에도 왜 먼저 대조해야 하는가?

핵심은 경고 등급을 진단 결과가 아니라 검토 우선순위로 읽는 데 있습니다. 운영 기록은 `문제가 맞다`를 단정하기보다, 어떤 신호를 지금 대조하고 어떤 신호를 더 모을지 먼저 나눕니다.

## 판단 기준

- 단순 threshold 등급과 근거 기반 등급이 왜 달라지는지 설명할 수 있습니다.
- 표본 수, 반복성, 최근성, 독자 영향을 함께 읽어 경고 등급을 조정할 수 있습니다.
- `watch`, `review`, `action`마다 첫 점검 위치를 함께 적을 수 있습니다.

## 왜 등급을 다시 나누는가

P7-7.3에서는 운영 신호를 `즉시 수정`, `재현 확인`, `다음 반복 개선`으로 나눴습니다. 이 구분은 첫 행동을 정하는 데 좋습니다. 하지만 운영 신호가 계속 쌓이면 같은 행동 구간 안에서도 다시 순서를 정해야 합니다.

| 판단 축 | 묻는 질문 | 등급에 주는 영향 |
| --- | --- | --- |
| gap | 기준선과 얼마나 다른가 | 크면 검토 가능성이 커진다 |
| event_count | 판단할 표본 수가 충분한가 | 적으면 단정 강도를 낮춘다 |
| repeatability_score | 같은 방향 변화가 반복되는가 | 높으면 단발성 튐과 구분된다 |
| recency_weight | 최근 신호인가 | 높으면 우선순위가 올라간다 |
| reader_impact | 공개 예제나 독자 흐름에 영향이 있는가 | 높고 재현되면 즉시 행동 후보가 된다 |

이 연습에서 등급은 모델의 정답이 아니라 운영자가 볼 검토 우선순위입니다. 따라서 `action`도 원인 확정이 아니라, 바로 수정하거나 즉시 대조해야 하는 후보라는 뜻으로 읽어야 합니다.

등급 판단은 gap 하나에서 바로 끝나지 않습니다. gap은 첫 신호일 뿐이고, 표본 수와 반복성, 최근성, 독자 영향이 들어와야 `watch`, `review`, `action`의 의미가 갈립니다.

```mermaid
--8<-- "assets/part-07/chapter-07/p7-7-4-alert-grade-flow-ko.mmd"
```

## 입력 파일

- 파일 경로: [`p7-action-unit-alert-grades.csv`](../../../assets/part-07/chapter-07/p7-action-unit-alert-grades.csv) · [CSV 미리보기](../../../assets/part-07/chapter-07/p7-action-unit-alert-grades.csv){ .csv-preview }
- 한 행의 의미: `동작 단위 합성 데이터에서 만들어 낸 운영 신호 한 건`
- 핵심 열: `gap`, `event_count`, `repeatability_score`, `recency_weight`, `reader_impact`, `expected_grade`

이 파일은 실제 운영 로그가 아니라 공개형 합성 데이터입니다. 값의 목적은 현실 수치를 재현하는 것이 아니라, 표본 수, 반복성, 최근성에 따라 판단 등급이 어떻게 달라지는지 보여 주는 데 있습니다.

## 연습 흐름

1. 각 신호의 `gap`, `event_count`, `repeatability_score`, `recency_weight`를 읽습니다.
2. 단순 threshold만 쓰는 등급과, 표본 수·반복성·최근성을 함께 쓰는 등급을 나란히 계산합니다.
3. 두 등급이 달라지는 사례를 찾습니다.
4. 등급이 달라진 이유를 `관찰 신호 -> 판단 근거 -> 다음 조치` 문장으로 씁니다.

## 실행 기록 기준

- gap만 보고 만든 등급을 먼저 확인합니다.
- 표본 수, 반복성, 최근성, 독자 영향을 함께 넣었을 때 등급이 바뀐 사례를 표시합니다.
- 등급이 낮아진 사례와 높아진 사례를 따로 나눕니다.
- 각 등급에 대해 첫 점검 위치를 한 줄로 적습니다.

## Python 예제

예제는 `값이 크면 무조건 action` 같은 단순 규칙이 왜 운영 판단을 흔들 수 있는지 확인하는 것입니다.

```python
# 경고 신호를 단순 threshold 등급과 evidence 기반 등급으로 비교해 watch, review, action 분류가 어떻게 바뀌는지 확인하는 예제입니다.
import csv
from pathlib import Path

data_path = Path("docs/assets/part-07/chapter-07/p7-action-unit-alert-grades.csv")
rows = list(csv.DictReader(data_path.open(encoding="utf-8")))
대표_signal_ids = {f"grade-{index:02d}" for index in range(1, 7)}
rows = [row for row in rows if row["signal_id"] in 대표_signal_ids]

def threshold_only_grade(row):
    gap = float(row["gap"])
    if gap >= 0.35:
        return "action"
    if gap >= 0.20:
        return "review"
    return "watch"

def evidence_grade(row):
    gap = float(row["gap"])
    event_count = int(row["event_count"])
    repeatability = float(row["repeatability_score"])
    recency = float(row["recency_weight"])

    if row["reader_impact"] == "높음" and row["reproducible"] == "예" and recency >= 0.90:
        return "action"
    if event_count < 3:
        return "watch"
    if gap >= 0.20 and repeatability >= 0.70 and recency >= 0.70:
        return "review"
    if event_count >= 5 and repeatability >= 0.80 and recency >= 0.85:
        return "review"
    if gap >= 0.35 and repeatability < 0.50:
        return "watch"
    return "watch"

records = []
for row in rows:
    simple = threshold_only_grade(row)
    evidence = evidence_grade(row)
    records.append({
        "signal_id": row["signal_id"],
        "signal_type": row["signal_type"],
        "threshold_only": simple,
        "evidence_grade": evidence,
        "expected_grade": row["expected_grade"],
        "changed": simple != evidence,
        "first_check": row["first_check"],
    })

summary = {
    "signal_count": len(records),
    "changed_by_evidence": [row["signal_id"] for row in records if row["changed"]],
    "grade_counts": {
        "watch": sum(row["evidence_grade"] == "watch" for row in records),
        "review": sum(row["evidence_grade"] == "review" for row in records),
        "action": sum(row["evidence_grade"] == "action" for row in records),
    },
    "mismatch": [
        row["signal_id"]
        for row in records
        if row["evidence_grade"] != row["expected_grade"]
    ],
}

print("경고 등급 설계 요약 =", summary)
for row in records:
    print(row)
```

실행 결과는 다음처럼 읽을 수 있습니다.

```text
경고 등급 설계 요약 = {'signal_count': 6, 'changed_by_evidence': ['grade-02', 'grade-03', 'grade-04', 'grade-05', 'grade-06'], 'grade_counts': {'watch': 2, 'review': 2, 'action': 2}, 'mismatch': []}
{'signal_id': 'grade-01', 'signal_type': 'baseline_drift', 'threshold_only': 'review', 'evidence_grade': 'review', 'expected_grade': 'review', 'changed': False, 'first_check': '최근 구간과 기준선 구간의 샘플 수 대조'}
{'signal_id': 'grade-02', 'signal_type': 'false_alarm', 'threshold_only': 'action', 'evidence_grade': 'watch', 'expected_grade': 'watch', 'changed': True, 'first_check': '해당 동작의 원시 로그와 센서 결측 여부 확인'}
{'signal_id': 'grade-03', 'signal_type': 'repeatability_low', 'threshold_only': 'review', 'evidence_grade': 'watch', 'expected_grade': 'watch', 'changed': True, 'first_check': '최근 구간 동작 수와 누락 여부 확인'}
{'signal_id': 'grade-04', 'signal_type': 'stable_change', 'threshold_only': 'watch', 'evidence_grade': 'review', 'expected_grade': 'review', 'changed': True, 'first_check': '구간 평균과 패턴 라벨의 반복 여부 확인'}
{'signal_id': 'grade-05', 'signal_type': 'public_example_mismatch', 'threshold_only': 'watch', 'evidence_grade': 'action', 'expected_grade': 'action', 'changed': True, 'first_check': '본문 표와 CSV 원본 대조'}
{'signal_id': 'grade-06', 'signal_type': 'recent_repeat', 'threshold_only': 'review', 'evidence_grade': 'action', 'expected_grade': 'action', 'changed': True, 'first_check': '최근 반복 신호와 독자 영향 범위 대조'}
```

## 결과를 어떻게 읽는가

`grade-02`는 gap만 보면 `action`처럼 보이지만 반복성이 낮고 재현되지 않았으므로 `watch`로 낮아집니다. 한 번 크게 튄 값은 바로 수정 대상이 아니라 원시 로그와 결측 여부를 먼저 확인해야 합니다.

`grade-03`도 gap은 작지 않지만 표본 수가 2건뿐입니다. 표본 수가 적을 때는 등급을 높이기보다 최소 표본 수를 채운 뒤 다시 비교하는 편이 안전합니다.

`grade-04`는 gap만 보면 약해 보이지만 반복성과 최근성이 높습니다. 이런 신호는 단발성 튐보다 다음 반복에서 더 중요할 수 있으므로 `review`로 올립니다.

`grade-05`와 `grade-06`은 독자 영향이 높고 재현됩니다. 특히 공개 예제 설명과 값이 충돌하거나 최근 반복 신호가 독자 흐름을 직접 흔든다면, 원인 확정 전이라도 `action` 후보로 올려 먼저 대조해야 합니다.

## 결과 해석 기준

| 관찰 | 읽어야 할 뜻 |
| --- | --- |
| `grade-02`가 `action`에서 `watch`로 낮아진다 | 큰 gap도 반복성과 재현성이 약하면 즉시 수정 후보가 아니다 |
| `grade-03`이 `review`에서 `watch`로 낮아진다 | 표본 수가 적으면 판단 강도를 낮춰야 한다 |
| `grade-04`가 `watch`에서 `review`로 올라간다 | 작은 gap도 반복성과 최근성이 높으면 검토 가치가 커진다 |
| `grade-05`, `grade-06`이 `action`이 된다 | 독자 영향과 재현성이 함께 있으면 원인 확정 전에도 대조가 먼저다 |

## 프로젝트 기록 예시

```text
관찰 신호:
gap 기준 등급:
근거 기반 등급:
등급이 달라진 이유:
첫 점검 위치:
다음 조치:
```

## 회고 문장으로 닫기

실습 뒤에는 등급만 적지 말고 판단 근거를 함께 남겨야 합니다.

| signal_id | 회고 문장 후보 |
| --- | --- |
| `grade-02` | gap은 크지만 반복성이 낮고 재현되지 않았으므로 `action`이 아니라 `watch`로 둔다. 다음 확인은 원시 로그와 결측 여부 대조다. |
| `grade-03` | 기준선 차이는 보이지만 표본 수가 2건이라 판단 강도가 약하다. 최소 표본 수를 채운 뒤 다시 비교한다. |
| `grade-04` | 차이값은 중간 수준이지만 최근 구간에서 반복성이 높으므로 `review`로 올린다. 다음 반복에서 기준선 갱신 후보로 남긴다. |
| `grade-05` | 공개 예제 설명과 CSV 값이 충돌하므로 독자 영향이 직접적이다. 본문 표와 원본 값을 즉시 대조한다. |

## 직접 바꿔 보며 확인할 것

1. `grade-02`의 `repeatability_score`를 `0.75`로 바꿔 봅니다.
   관찰할 점: 한 번 튄 값이 아니라 반복 신호가 되면 등급이 어떻게 달라지는가?

2. `grade-03`의 `event_count`를 `5`로 바꿔 봅니다.
   관찰할 점: 표본 수가 늘어나면 같은 gap을 더 강하게 읽을 수 있는가?

3. `grade-04`의 `recency_weight`를 `0.30`으로 낮춰 봅니다.
   관찰할 점: 오래된 반복과 최근 반복을 같은 등급으로 두어도 되는가?

4. `grade-05`의 `reader_impact`를 `낮음`으로 바꿔 봅니다.
   관찰할 점: 공개 예제 충돌이라도 독자 영향이 낮으면 즉시 행동 등급이 유지되는가?

판단 기준은 등급이 높아졌는가보다 등급을 올리거나 낮춘 근거가 무엇인지입니다. 같은 gap이라도 표본 수가 부족하면 `watch`로 낮추고, 독자 영향과 재현성이 함께 있으면 원인 확정 전에도 `action`으로 올릴 수 있습니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| gap | gap 하나만 보고 등급을 확정하지 않았는가? |
| 표본 수 | 표본 수가 적은 신호를 더 보수적으로 읽었는가? |
| 반복성 | 반복성과 최근성이 높은 신호를 단발성 튐과 구분했는가? |
| 등급 의미 | `watch`, `review`, `action`을 진단 확정이 아니라 검토 우선순위로 읽었는가? |
| 첫 점검 | 등급이 달라진 사례마다 첫 점검 위치를 함께 남겼는가? |

## 출처와 참고 자료

- 경고 등급 설계 파일: [`p7-action-unit-alert-grades.csv`](../../../assets/part-07/chapter-07/p7-action-unit-alert-grades.csv) · [CSV 미리보기](../../../assets/part-07/chapter-07/p7-action-unit-alert-grades.csv){ .csv-preview }
- 이 문서는 자체 합성 데이터와 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.
