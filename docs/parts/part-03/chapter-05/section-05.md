# P3-5.5 값이 빠지거나 구간이 비어 있는 샘플은 어떻게 다루는가

> Section ID: `P3-5.5`
> Version: `v2026.07.31`

원천 로그를 [요약 표(summary table)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)로 바꾸는 단계까지 오면, `동작은 있었는데 일부 센서값이 비어 있으면 어떻게 해야 하는가?` `중간 구간 기록이 빠졌는데 이 샘플을 버려야 하는가, 일부만 써야 하는가?` 같은 질문이 바로 생깁니다. 이때 먼저 봐야 할 것은 값을 어떻게 채울지보다, [결측값(missing value)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-missing-value)이 [샘플(sample)](../../../reference/concept-glossary-parts/07-siot.md#glossary-sample) 경계와 [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature) 의미를 얼마나 흔드는가입니다.

값이 빠졌다는 사실은 단순한 청소 문제가 아니라, `이 샘플을 여전히 같은 종류의 사례로 볼 수 있는가`를 다시 묻게 하는 데이터 모델링 신호입니다.

## 결측이 샘플 구조를 흔드는 방식

값이 비어 있다는 사실만 보고 곧바로 `NaN을 채우면 되겠지`라고 생각하면, 샘플 경계가 이미 무너졌는지와 어떤 특징이 뜻을 잃었는지를 놓치기 쉽습니다. 실제로는 아래처럼 훨씬 먼저 정해야 할 질문이 있습니다.

| 지금 보이는 현상 | Part 3에서 먼저 물어야 하는 질문 |
| --- | --- |
| 후반 센서 구간이 통째로 비었다 | 이 샘플은 아직 동작 1회 비교 단위로 쓸 수 있는가 |
| 일부 시점만 누락되었다 | 요약값을 만들어도 같은 구조 비교가 가능한가 |
| 특정 센서만 자주 비어 있다 | 빠짐 자체가 운영 상태 신호인가 |

즉 값이 빠진 샘플은 단순히 `채울 값이 있는 표`가 아니라, `샘플 경계와 특징 의미를 다시 확인해야 하는 사례`입니다. 독자가 처음 표를 볼 때는 먼저 `부분 누락인가`, `구간 누락인가`, `샘플 경계 붕괴인가`를 가르는 편이 이해가 빠릅니다.

## 먼저 구분해야 하는 세 가지

값이 비어 있을 때는 복잡한 기법보다 먼저 아래 세 가지를 구분하는 편이 좋습니다.

| 먼저 구분할 것 | 질문으로 바꾸면 |
| --- | --- |
| 일부 값만 비었는가 | 구간 평균이나 특정 센서 일부만 빠졌는가 |
| 한 구간이 통째로 비었는가 | 초반·중반·후반 중 한 덩어리가 없는가 |
| 샘플 의미 자체가 깨졌는가 | 동작 1회 전체를 같은 종류의 사례로 보기 어려운가 |

이 구분이 필요한 이유는 `무엇을 비어 있음으로 볼 것인가`에 따라 다음 판단이 완전히 달라지기 때문입니다. `일부 값만 비었다`와 `동작의 끝이 사라졌다`는 둘 다 빈칸처럼 보이지만, 뒤에서 내려야 하는 결정은 전혀 같지 않습니다.

## 같은 결측처럼 보여도 다른 문제다

예를 들어 아래 세 상황은 모두 `값이 없다`로 보이지만 실제 의미는 다릅니다.

| 보이는 문제 | 더 가까운 해석 |
| --- | --- |
| 시점 1~2개가 비었다 | 부분 측정 누락 |
| 후반 20% 구간이 통째로 비었다 | 구조 비교를 흔드는 구간 누락 |
| `event_end`가 없어 종료 시점 자체를 모른다 | 샘플 경계 붕괴 |

첫 번째는 여전히 같은 샘플 구조 안에서 일부 정보가 빠진 경우일 수 있습니다. 두 번째는 후반 하강률 같은 특징의 의미를 직접 흔듭니다. 세 번째는 아예 동작 1회의 시작과 끝이 닫히지 않아 샘플 자체를 다시 봐야 할 수 있습니다.

## 그래서 지금 단계에서 무엇을 먼저 결정해야 하는가

복잡한 결측치 보정 기법보다 먼저 아래 네 가지를 적어 두는 편이 더 중요합니다.

| 먼저 적을 판단 | 왜 필요한가 |
| --- | --- |
| 이 샘플을 유지할 것인가 | 같은 종류의 사례로 비교 가능한지 보기 위해 |
| 어느 특징을 만들지 말아야 하는가 | 구간 누락 때문에 뜻이 깨지는 특징을 막기 위해 |
| 빠짐 자체를 표시 열로 남길 것인가 | 누락이 운영 신호일 수 있기 때문 |
| 원시 로그 재확인이 필요한가 | 단순 빈칸이 아니라 샘플 경계 문제일 수 있기 때문 |

즉 여기서의 관심사는 `어떻게 채울까`보다 먼저 `이 샘플을 지금 어떤 상태로 분류할까`에 가깝습니다. 판단 순서는 보통 `샘플 유지 여부 -> 만들지 말아야 할 특징 -> 빠짐 자체를 표시 열로 남길지`로 이어집니다.

이 판단도 표 안에 남아야 합니다. `keep_sample`, `missing_scope`, `avoid_features`, `missing_indicator`, `raw_log_recheck_needed` 같은 열을 두면 빈칸을 어떤 정책으로 처리했는지 다시 볼 수 있습니다. 특히 샘플을 유지하되 특정 특징만 만들지 않기로 했다면, 그 이유가 `late_segment_missing`인지 `end_detected=0`인지 같이 남겨야 뒤에서 결측 처리가 단순 전처리인지 샘플 경계 문제인지 구분할 수 있습니다.

## 작은 도식으로 보기

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-5-mermaid-01-ko.mmd"
```

이 도식은 `비어 있음`을 하나의 상태로 보지 않고, 누락 위치와 샘플 경계 상태에 따라 판단이 갈라진다는 점을 보여 줍니다. 즉 이 절의 예시는 값 자체보다 `유지`, `특징 제외`, `구조 붕괴`로 나뉘는 판단 구조를 먼저 드러내는 데 있습니다.

## 빠짐 자체를 왜 열로 남길 수 있는가

흔히 `빈칸은 없애야 한다`고만 생각하지만, 실제로는 빠짐 자체가 의미를 가질 수 있습니다.

| 빠짐 상태 | 왜 표시 열로 남길 수 있는가 |
| --- | --- |
| 특정 센서가 특정 조건에서만 자주 비어 있다 | 운영 모드나 통신 상태 신호일 수 있기 때문 |
| 종료 직전 구간이 자주 비어 있다 | 이벤트 종료 감지 실패와 연결될 수 있기 때문 |
| 특정 기간에만 비어 있다 | 시스템 변경이나 유지보수 상태와 연결될 수 있기 때문 |

따라서 Part 3에서는 `missing_sensor_flag`, `late_segment_missing` 같은 표시 열을 둘 가치가 있는지도 함께 볼 수 있습니다. 이것은 아직 모델 입력으로 확정한다는 뜻이 아니라, 빠짐을 그냥 지워 버리지 않고 구조 정보로 남겨 둘지 판단한다는 뜻입니다.

이 판단을 먼저 해 두면 `채울 수 있는 값`과 `샘플 구조를 이미 무너뜨린 누락`을 섞지 않게 됩니다. 핵심은 처리 기법 이름보다 먼저, 현재 샘플이 아직 같은 비교 단위인지와 빠짐 자체를 구조 정보로 남길지 구분하는 데 있습니다.

## 작은 코드 예시

문제 상황: 값이 비어 있는 샘플이 모두 같은 상태가 아니라, 일부 특징만 피하면 되는 경우와 샘플 구조 자체가 무너진 경우가 갈린다는 점을 확인합니다.

입력(input): [`p3_5_5_missing_segments.csv`](/AiBook/assets/part-03/chapter-05/p3_5_5_missing_segments.csv){: target="_blank" rel="noopener noreferrer" } 파일. 한 행은 동작 1회의 요약 행이고, 빈 값은 해당 구간 평균이 만들어지지 않았다는 뜻입니다. 부분 누락 샘플 유지 정책은 `keep_partial_samples`로 조작합니다.

기대 출력(output): `late_segment_missing`, `sample_structure_broken`, `keep_sample`, `avoid_features`가 함께 정리된 출력. `keep_partial_samples`를 바꾸면 일부 구간만 빠진 샘플의 유지 여부가 달라진다.

확인할 개념: 결측은 채우기 전에 먼저 `샘플 유지`, `특징 제외`, `구조 붕괴` 중 어디에 속하는지 분류해야 한다. 부분 누락을 허용할지 여부는 명시적인 정책으로 남겨야 한다.

```python
# 값이 빠지거나 구간이 비어 있는 샘플을 집계 전에 점검하고 표시하는 예제입니다.
import csv
from collections import Counter
from pathlib import Path

keep_partial_samples = True
preview_count = 9

data_path = Path("docs/assets/part-03/chapter-05/p3_5_5_missing_segments.csv")

def parse_optional_float(value):
    return None if value == "" else float(value)

with data_path.open(newline="", encoding="utf-8") as file:
    summary = []
    for row in csv.DictReader(file):
        early = parse_optional_float(row["early_flow_mean"])
        mid = parse_optional_float(row["mid_flow_mean"])
        late = parse_optional_float(row["late_flow_mean"])
        end_detected = int(row["end_detected"])
        late_segment_missing = int(late is None)
        sample_structure_broken = int(end_detected == 0)

        if sample_structure_broken:
            keep_sample = "no"
            avoid_features = "all event-level features"
        elif late_segment_missing and not keep_partial_samples:
            keep_sample = "no"
            avoid_features = "late_drop features"
        elif late_segment_missing:
            keep_sample = "yes"
            avoid_features = "late_drop features"
        else:
            keep_sample = "yes"
            avoid_features = "none"

        summary.append(
            {
                "event_id": row["event_id"],
                "early_flow_mean": early,
                "mid_flow_mean": mid,
                "late_flow_mean": late,
                "late_segment_missing": late_segment_missing,
                "sample_structure_broken": sample_structure_broken,
                "keep_sample": keep_sample,
                "avoid_features": avoid_features,
            }
        )

def fmt(value):
    return "missing" if value is None else f"{value:.2f}"

print("1) missingness flags")
for row in summary[:preview_count]:
    print(
        f'{row["event_id"]}: '
        f'late={fmt(row["late_flow_mean"]):<7} '
        f'late_missing={row["late_segment_missing"]} '
        f'boundary_broken={row["sample_structure_broken"]}'
    )
print(f"... {len(summary) - preview_count} more event summaries")
print()
print("2) sample decision")
for row in summary[:preview_count]:
    print(
        f'{row["event_id"]}: keep={row["keep_sample"]:<3} '
        f'avoid={row["avoid_features"]}'
    )
print()
print("3) decision counts")
for decision, count in sorted(Counter(row["keep_sample"] for row in summary).items()):
    print(f"keep_sample={decision}: {count}")
for feature_group, count in sorted(Counter(row["avoid_features"] for row in summary).items()):
    print(f"avoid={feature_group}: {count}")
```

예상 출력:

```text
1) missingness flags
E01: late=1.80    late_missing=0 boundary_broken=0
E02: late=missing late_missing=1 boundary_broken=0
E03: late=missing late_missing=1 boundary_broken=1
E04: late=1.75    late_missing=0 boundary_broken=0
E05: late=missing late_missing=1 boundary_broken=0
E06: late=missing late_missing=1 boundary_broken=1
E07: late=1.82    late_missing=0 boundary_broken=0
E08: late=missing late_missing=1 boundary_broken=0
E09: late=missing late_missing=1 boundary_broken=1
... 27 more event summaries

2) sample decision
E01: keep=yes avoid=none
E02: keep=yes avoid=late_drop features
E03: keep=no  avoid=all event-level features
E04: keep=yes avoid=none
E05: keep=yes avoid=late_drop features
E06: keep=no  avoid=all event-level features
E07: keep=yes avoid=none
E08: keep=yes avoid=late_drop features
E09: keep=no  avoid=all event-level features

3) decision counts
keep_sample=no: 12
keep_sample=yes: 24
avoid=all event-level features: 12
avoid=late_drop features: 12
avoid=none: 12
```

이 예시의 핵심은 값을 채우는 코드가 아니라, `부분 구간 누락`과 `샘플 구조 붕괴`를 같은 빈칸으로 처리하지 않는다는 점입니다. 여기서 조작할 값은 `keep_partial_samples`입니다. `True`이면 `E02` 같은 행은 샘플은 유지하되 후반 하강 특징은 보수적으로 뺍니다. `False`로 바꾸면 부분 구간 누락이 있는 12건도 비교 후보에서 제외됩니다. 반면 `E03` 같은 행은 샘플 경계 자체가 흔들려 정책과 무관하게 동작 1회 비교 샘플로 바로 쓰기 어렵습니다. 1단계에서 누락 위치를 구분하고, 2단계에서 그 차이가 바로 `샘플 유지 여부`와 `만들지 말아야 할 특징` 판단으로 이어집니다.

여기서 마지막으로 확인할 것은 세 가지입니다. 이 샘플이 아직 같은 비교 단위인지, 누락 때문에 만들면 안 되는 특징을 구분했는지, 빠짐 자체를 표시 열로 남길지 정했는지입니다. 이 세 조건이 함께 서야 빈칸은 단순 청소 대상이 아니라, 샘플 구조 판단이 섞인 데이터 모델링 항목으로 읽히게 됩니다.

값이 빠졌다는 사실은 단순 [전처리(preprocessing)](../../../reference/concept-glossary-parts/09-jieut.md#preprocessing) 문제가 아니라, 이 샘플이 아직 같은 비교 단위인지와 빠짐 자체를 구조 정보로 남길지 다시 묻게 하는 데이터 모델링 신호입니다. 따라서 결측을 다룬다는 말은 빈칸을 메우는 일보다 먼저, 어떤 샘플은 유지하고 어떤 샘플은 비교에서 물려야 하는지 경계를 다시 그리는 일에 가깝습니다.

## 체크리스트

- 이 절의 질문인 `값이 빠지거나 구간이 비어 있는 샘플은 어떻게 다루는가`에 대해 한 문장으로 답할 수 있는가?
- `결측과 빈 구간을 샘플 유지 여부 판단과 연결해 다뤄야 합니다.`라는 기준을 본문 표, 도식, 예제 중 하나에 적용해 설명할 수 있는가?
- 샘플, 특징, 기준선, target/라벨, 검토 기준 중 이 절에서 먼저 고정해야 할 항목을 구분했는가?
- 모델 선택으로 넘기기 전에 Part 3에서 닫아야 할 데이터 구조 질문을 하나 적었는가?

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example는 features와 label이 붙는 같은 단위를 전제로 하므로, 결측이 샘플 경계를 흔들 때는 값을 채우기 전에 그 샘플이 아직 같은 비교 단위인지 먼저 확인해야 한다는 점을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `feature engineering`. feature engineering은 원시 데이터를 학습과 비교에 더 유용한 형태로 바꾸는 과정이므로, 구간 누락 때문에 뜻이 깨진 특징은 만들지 말아야 한다는 이 절의 판단을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance framework가 derivation과 processing steps를 설명 가능하게 남겨야 한다고 정리하므로, 누락 위치와 샘플 구조 붕괴 여부를 별도 정보로 남겨야 나중에 품질과 재현성을 다시 판단할 수 있다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- scikit-learn developers, `Imputation of missing values`. 결측값이 있는 행이나 열을 버릴 수 있지만 가치 있는 데이터 손실이 생길 수 있고, `MissingIndicator`로 결측 여부를 이진 행렬로 표시할 수 있으며 결측이 있었던 정보를 보존하는 일이 유용할 수 있다고 설명하므로, 빠짐 자체를 표시 열로 남길지 먼저 판단해야 한다는 이 절의 설명을 보강합니다. [https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values](https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
