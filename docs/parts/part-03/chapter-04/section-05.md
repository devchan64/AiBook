# P3-4.5 지금 모은 샘플은 전체 운영 상황을 얼마나 대표하는가

> Section ID: `P3-4.5`
> Version: `v2026.07.20`

샘플 단위를 동작 1회나 최근 구간 1개처럼 정하고 나면, 한 번 더 놓치기 쉬운 질문이 남습니다. `지금 모은 샘플이 전체 운영 상황을 얼마나 대표하는가?` 표가 잘 정리되어 있어도, 그 표가 특정 공정 모드나 특정 기간, 특정 장비 상태에서만 모인 사례라면 전체 운영 장면을 고르게 설명하지 못할 수 있습니다. 샘플 단위를 잘 정한 것과, 그 샘플 묶음이 전체 상황을 고르게 대표하는 것은 같은 말이 아닙니다.

## 샘플 묶음의 대표성은 무엇과 구분해야 하는가

대표성 문제는 샘플 한 건의 정의가 맞는가와는 별도로, 샘플 묶음이 어떤 운영 범위를 실제로 덮고 있는가를 다시 묻는 일입니다.

| 겉으로 보이는 상태 | Part 3에서 먼저 물어야 하는 질문 |
| --- | --- |
| 샘플 단위는 잘 정리되었다 | 어떤 운영 조건에서 모인 샘플인가 |
| 특징과 라벨 후보도 있다 | 특정 기간이나 특정 모드에만 몰려 있지 않은가 |
| 표 건수도 충분해 보인다 | 전체 운영 장면을 고르게 덮고 있는가 |

즉 `샘플 한 건의 정의`와 `샘플 묶음의 대표성`은 다른 문제입니다.

## 대표성이 흔들리는 대표 장면

아래처럼 같은 동작 1회 샘플이어도, 어떤 구간에서 모였는지에 따라 대표성은 달라질 수 있습니다.

| 지금 모인 샘플 상태 | 왜 대표성이 약해질 수 있는가 |
| --- | --- |
| 낮 시간대 정상 운전만 많다 | 야간, 고부하, 전환 구간을 거의 못 본다 |
| 유지보수 직후 구간이 대부분이다 | 평소 장기 운영 상태를 덜 담는다 |
| 특정 장비 한 대에서만 많이 모였다 | 장비 간 차이를 놓칠 수 있다 |
| 한 달 중 한 주에만 집중됐다 | 계절성, 주기 변화, 정책 변화를 놓칠 수 있다 |

즉 샘플 수가 많아도, 덮는 조건이 좁으면 대표성은 여전히 약할 수 있습니다.

## 먼저 적어 두면 좋은 네 가지

Part 3에서는 아직 엄밀한 표본추출 이론보다, 아래 네 가지를 먼저 메모하는 편이 더 중요합니다.

| 먼저 적을 것 | 질문으로 바꾸면 |
| --- | --- |
| 시간 범위 | 어느 기간의 샘플인가 |
| 운영 모드 범위 | 어떤 조건과 상태에서 모인 샘플인가 |
| 장비/개체 범위 | 어느 설비, 어느 개체에서 모인 샘플인가 |
| 부족한 구간 | 거의 보지 못한 조건이나 모드는 무엇인가 |

이 메모는 뒤에서 일반화를 증명하기 위한 것이 아니라, 지금 표가 무엇을 대표하고 무엇을 아직 대표하지 못하는지 먼저 드러내기 위한 것입니다.

## 작은 도식으로 보기

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-5-mermaid-01-ko.mmd"
```

이 도식은 샘플 단위가 모두 `동작 1회`로 맞아도, 덮는 운영 범위는 한쪽으로 기울 수 있다는 점을 보여 줍니다. 즉 이 절의 예시는 원시 표 값을 많이 읽는 데 있지 않고, `어떤 조건이 과다대표되고 어떤 조건이 거의 비어 있는가`를 먼저 파악하는 데 있습니다.

## 왜 이 문제가 샘플 단위 다음에 와야 하는가

대표성 문제는 샘플 단위가 먼저 정해져 있어야 읽을 수 있습니다. 한 행이 시점 기록인지 동작 1회인지 아직 모호하면, `야간 동작 1회가 몇 건 있는가`, `고부하 조건 샘플이 몇 건 있는가` 같은 질문도 제대로 세기 어렵기 때문입니다.

즉 순서는 다음과 같습니다.

1. 먼저 무엇을 샘플 1건으로 볼지 정한다.
2. 그 다음 그 샘플들이 어떤 조건 범위를 덮는지 본다.

이 메모를 남겨 두어야 나중에 결과를 읽을 때도 `어떤 조건 범위에서 얻은 샘플 묶음인가`를 함께 볼 수 있고, `어떤 운영 조건을 거의 보지 못했는가`도 놓치지 않게 됩니다. 즉 대표성 문제는 현재 샘플 묶음이 무엇을 덮고 무엇을 놓쳤는지 먼저 적어 두는 문제에 가깝습니다.

## 작은 코드 예시

문제 상황: 샘플 단위는 모두 `동작 1회`로 맞았더라도, 실제 샘플 묶음이 어느 조건에 치우쳐 있는지 확인합니다.

입력(input): [p3_4_5_sample_coverage.csv](../../../assets/part-03/chapter-04/p3_4_5_sample_coverage.csv)에 저장된 동작 샘플 표와 최소 관찰 기준 `minimum_count`. 이 표에는 `shift`, `load_mode`, `machine_id`, `maintenance_phase`가 들어 있습니다.

기대 출력(output): 어떤 조건이 많이 보였고 어떤 조건이 거의 비어 있는지를 요약한 `coverage summary`. `minimum_count`를 바꾸면 대표성 공백으로 표시되는 조건 수가 달라진다.

확인할 개념: 샘플 한 건의 정의가 맞는 것과 샘플 묶음이 전체 운영 범위를 고르게 대표하는 것은 다른 문제다. 대표성 판단에는 관찰 기준이 필요하다.

```python
import csv
from collections import Counter
from pathlib import Path

minimum_count = 9
preview_sample_count = 8

input_path = Path("docs/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv")
coverage_scopes = ["shift", "load_mode", "machine_id", "maintenance_phase"]

with input_path.open(newline="", encoding="utf-8") as file:
    samples = list(csv.DictReader(file))

coverage_summary = []
for scope in coverage_scopes:
    counts = Counter(sample[scope] for sample in samples)
    ordered_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    most_seen, most_seen_count = ordered_counts[0]
    least_seen, _ = sorted(counts.items(), key=lambda item: (item[1], item[0]))[0]
    under_minimum = sum(1 for count in counts.values() if count < minimum_count)
    coverage_summary.append(
        {
            "scope": scope,
            "most_seen": most_seen,
            "count": most_seen_count,
            "least_seen": least_seen,
            "unique_conditions": len(counts),
            "under_minimum_conditions": under_minimum,
        }
    )

print("1) raw sample coverage table")
for sample in samples[:preview_sample_count]:
    print(
        f"{sample['event_id']}: shift={sample['shift']}, "
        f"load_mode={sample['load_mode']}, machine_id={sample['machine_id']}, "
        f"maintenance_phase={sample['maintenance_phase']}"
    )
print(f"... {len(samples) - preview_sample_count} more event-level samples")
print()
print(f"2) coverage summary when minimum_count = {minimum_count}")
for item in coverage_summary:
    print(
        f"{item['scope']}: most_seen={item['most_seen']} ({item['count']}), "
        f"least_seen={item['least_seen']}, "
        f"unique_conditions={item['unique_conditions']}, "
        f"under_minimum_conditions={item['under_minimum_conditions']}"
    )
```

예상 출력:

```text
1) raw sample coverage table
E01: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E02: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E03: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E04: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E05: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E06: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E07: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E08: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
... 28 more event-level samples

2) coverage summary when minimum_count = 9
shift: most_seen=day (26), least_seen=night, unique_conditions=2, under_minimum_conditions=0
load_mode: most_seen=normal (25), least_seen=low, unique_conditions=3, under_minimum_conditions=2
machine_id: most_seen=M1 (22), least_seen=M2, unique_conditions=3, under_minimum_conditions=2
maintenance_phase: most_seen=stable (28), least_seen=after-maintenance, unique_conditions=2, under_minimum_conditions=1
```

이 예시에서 중요한 것은 분류 기법이 아니라, `현재 표가 무엇을 많이 보고 무엇을 거의 못 보고 있는가`를 한눈에 드러내는 일입니다. 여기서 조작할 값은 `minimum_count`입니다. `minimum_count = 9`일 때는 `shift`처럼 두 조건이 모두 기준을 넘는 범위도 있고, `load_mode`, `machine_id`, `maintenance_phase`처럼 일부 조건이 대표성 공백으로 잡히는 범위도 있습니다. 이 값을 낮추면 공백이 줄고, 높이면 더 많은 조건이 부족한 조건으로 표시됩니다. 이렇게 해야 `샘플 수는 36건인데도 왜 대표성은 조건별로 다르게 보이는가`를 숫자와 표 둘 다로 설명할 수 있습니다.

이 표를 읽을 때는 세 가지를 함께 확인하면 됩니다. 이 표가 모은 시간·모드·장비 범위를 설명할 수 있는가, 거의 보지 못한 조건을 적어 둘 수 있는가, 그리고 나중에 평가 점수를 읽을 때도 이 대표성 범위를 함께 떠올릴 수 있는가입니다. 이런 메모가 붙어 있어야 샘플 표는 단순히 `정리된 표`가 아니라, `어떤 운영 범위를 대표하는지`까지 함께 남긴 표가 됩니다.

샘플 단위를 잘 정했다고 해서 그 샘플 묶음이 전체 운영 상황을 자동으로 대표하는 것은 아닙니다. 그래서 Part 3에서는 시간·모드·장비 범위와 남은 공백을 함께 적어 두어야 합니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example 단위가 먼저 정해져야 그다음에 어떤 example 집합이 현재 문제를 대표하는지 묻는 단계로 넘어갈 수 있으므로, 샘플 한 건의 정의와 샘플 묶음의 대표성을 분리해 읽어야 한다는 이 절의 출발점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance와 activity context를 함께 남겨야 한다고 정리하므로, 현재 샘플 묶음이 어느 기간, 어느 장비, 어느 운영 모드에서 나왔는지 추적 가능해야 대표성 범위를 설명할 수 있다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. 현재 성능을 과거 성능과 비교할 때 같은 본질 조건 아래에서 얻은 표본이 필요하다고 설명하므로, 샘플 수가 아니라 어떤 운영 조건을 얼마나 덮고 있는지가 먼저 정리되어야 한다는 대표성 점검의 일반 근거가 됩니다. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
