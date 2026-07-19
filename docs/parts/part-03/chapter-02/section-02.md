# P3-2.2 데이터셋 후보 안에는 어떤 구조가 들어가는가

> Section ID: `P3-2.2`
> Version: `v2026.07.19`

앞 절에서 본 것처럼 저장된 기록은 아직 데이터셋이 아닐 수 있습니다. 그렇다면 질문은 곧바로 이어집니다. 데이터셋 후보를 다시 만든다면 그 안에는 어떤 구조가 들어가야 하는가 하는 질문입니다. Part 3에서는 이 질문에 답하기 위해 [샘플(sample)](../../../reference/concept-glossary.md#glossary-sample), [특징(feature)](../../../reference/concept-glossary.md#glossary-feature), [기준선(baseline)](../../../reference/concept-glossary.md#glossary-baseline), [출력 구조(output structure)](../../../reference/concept-glossary.md#glossary-output-structure)를 함께 봅니다. 이 용어들은 각각 따로 외우는 목록보다, 하나의 데이터셋 설계 구조로 읽어야 더 정확합니다. 무엇을 한 건의 샘플로 볼지 정해야 특징을 만들 수 있고, 특징이 있어야 무엇을 기준선과 비교할지 정할 수 있으며, 그 비교가 있어야 어떤 출력 구조를 만들 것인지도 결정할 수 있습니다.

이 절에서 특히 중요한 것은 [타깃(target)](../../../reference/concept-glossary.md#glossary-target)으로 바로 굳히기 전의 `출력 구조`를 검토용 결과와 예측용 목표 후보를 가르는 문제 설계 축으로 읽는 일입니다. 데이터셋 후보를 하나의 표 이름이 아니라 몇 가지 연결된 구조로 읽어야 하는 이유도 여기에 있습니다. 무엇을 샘플로 잡는지, 어떤 특징을 남기는지, 무엇을 기준선과 비교하는지, 어떤 출력 구조로 끝나는지가 함께 정해져야 비로소 데이터셋 후보의 뜻이 선명해집니다.

자동으로 실행되는 동작 1회를 예로 들어 보겠습니다. 샘플은 `이번 동작 전체를 한 건으로 본 것`일 수 있습니다. 특징은 그 동작에서 계산해 남긴 `총 시간`, `중반 평균`, `후반 하강률`, `추종 오차` 같은 값일 수 있습니다. 기준선은 최근이 아닌 평소 구간의 대표값이나 비교 집단일 수 있습니다. 출력 구조는 최종적으로 사람이나 모델이 읽게 될 결과 형식으로, 예를 들면 `검토 필요`, `주의`, `정상 범위`, `예측 대상 라벨 후보` 같은 구조가 될 수 있습니다.

이 관계를 표로 먼저 정리합니다.

| 구성요소 | 여기서 뜻하는 것 | 지금 단계에서 묻는 질문 |
| --- | --- | --- |
| 샘플 | 비교나 학습의 기본 단위가 되는 한 건 | 무엇을 한 행으로 볼 것인가 |
| 특징 | 샘플을 설명하기 위해 계산해 남긴 값 | 어떤 값을 남겨야 비교가 쉬운가 |
| 기준선 | 최근과 비교할 평소 구조 또는 기준 집단 | 무엇과 비교해야 변화가 보이는가 |
| 출력 구조 | 사람이 읽거나 모델이 이어받을 결과 형식 | 최종적으로 어떤 판단을 만들 것인가 |

이 네 가지를 한 번에 보면 데이터 모델링이 왜 단순 정리가 아닌지 드러납니다. 예를 들어 아직 샘플이 `한 시점 측정값`인지 `동작 1회`인지 정하지 않은 상태에서는 특징도 안정적으로 정할 수 없습니다. 시점별 표에 어울리는 특징과 동작 1회 표에 어울리는 특징은 다르기 때문입니다. 마찬가지로 기준선을 무엇으로 둘지 정하지 않으면 최근 구간 변화도 읽기 어렵습니다. 또 출력 구조가 `검토 후보 생성`인지 `예측 라벨 출력`인지 정해지지 않으면 어떤 비교가 필요한지도 모호해집니다.

즉 이 네 요소는 따로 외울 용어 목록이 아니라, 데이터셋 후보를 만드는 앞에서 뒤로 이어지는 설계 순서입니다. 샘플이 흔들리면 특징도 흔들리고, 특징이 흔들리면 기준선 비교도 흔들리고, 비교가 흔들리면 출력 구조도 흔들립니다. 그래서 이 절에서는 어떤 질문 순서로 서로 연결되는지를 먼저 고정합니다.

실제로는 아래 순서로 질문이 이어집니다.

1. 지금 비교하려는 대상은 한 시점인가, 동작 1회인가, 최근 구간인가
2. 그 대상을 설명하려면 어떤 숫자를 남겨야 하는가
3. 그 숫자는 무엇과 비교해야 의미가 생기는가
4. 마지막 결과를 사람이 읽을 문장으로 낼지, 모델이 받을 라벨 후보로 낼지

이 네 질문은 각각 샘플, 특징, 기준선, 출력 구조에 대응합니다. 그래서 용어가 흐릿더라도 질문 순서를 따라가면 현재 어떤 데이터셋 설계 단계에 있는지 다시 확인할 수 있습니다.

아래 표는 네 요소가 한 행 안에서 어떻게 이어지는지 더 구체적으로 보여 줍니다. 같은 동작 1회라도 먼저 샘플을 한 건으로 세우고, 그 위에 특징을 적고, 그 특징을 평소 기준선과 비교한 뒤, 마지막에 사람이 읽을 출력으로 마무리합니다.

| sample_id | mean_flow | late_drop_rate | baseline_mean_flow | baseline_late_drop_rate | baseline_gap | output |
| --- | --- | --- | --- | --- | --- | --- |
| A | 0.74 | -0.32 | 0.92 | -0.05 | -0.27 | `검토 필요` |
| B | 0.89 | -0.08 | 0.92 | -0.05 | -0.03 | `정상 범위` |

이 표를 읽는 순서는 왼쪽에서 오른쪽으로 자연스럽게 이어집니다. `sample_id`는 무엇을 한 건의 샘플로 셌는지를 고정합니다. `mean_flow`와 `late_drop_rate`는 그 샘플을 설명하는 특징입니다. `baseline_mean_flow`와 `baseline_late_drop_rate`는 평소 기준선입니다. `baseline_gap`은 현재 샘플의 후반 하강률이 기준선보다 얼마나 더 떨어졌는지를 적어 둔 비교 결과입니다. 그리고 이 비교 결과가 충분히 크면 `output`에서 `검토 필요` 같은 운영 판단이 만들어집니다.

즉 `검토 필요`라는 출력은 표 맨 끝에서 갑자기 붙는 문구가 아닙니다. 앞 열들에서 이미 `무엇을 비교할지`, `무엇이 평소와 다른지`가 정리되어 있어야만 마지막 출력 열도 설명할 수 있습니다. 이런 이유로 샘플, 특징, 기준선, 출력 구조는 같은 표 안에 들어 있더라도 서로 독립된 목록이 아니라 앞에서 뒤로 이어지는 설계 흐름입니다.

## 작은 도식으로 보기

데이터셋 후보 안의 네 구조는 아래처럼 `샘플 -> 특징 -> 기준선 비교 -> 출력 구조` 순서로 맞물린다고 보면 한 번에 정리됩니다.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-2-mermaid-01-ko.mmd"
```

문제 상황: 동작 1회를 샘플 1건으로 잡은 뒤, 특징을 적고, 평소 기준선과 비교해, 마지막 운영 출력을 만드는 흐름을 표로 확인합니다.

입력(input): `baseline` 기간과 `recent` 기간이 함께 들어 있는 시점별 유량 로그 [p3_2_2_event_flow_log.csv](../../../assets/part-03/chapter-02/p3_2_2_event_flow_log.csv), 검토 후보로 보낼 기준 후보 `review_gap_thresholds`

입력 파일의 한 행은 한 샘플의 특정 초(`second`)에서 측정한 유량(`flow`)입니다. `sample_id`는 동작 1회를 가리키고, `period`는 그 샘플이 평소 기준선을 만들 `baseline` 구간인지 최근 비교 대상인 `recent` 구간인지를 구분합니다.

기대 출력(output): 원시 로그에서 `샘플 행 -> 특징 표 -> 기준선 생성 -> 최근 샘플 비교표 -> 운영 출력`이 만들어지고, `review_gap_thresholds`를 바꾸어 적용할 때 검토 후보 수가 달라지는 과정

확인할 개념: 출력 구조와 기준선은 미리 적어 둔 결과 열이 아니라, 원시 로그를 샘플 단위로 묶고 특징을 계산한 뒤 기간별 역할을 나누어 생성된다. 출력 기준을 여러 값으로 비교해야 운영 판단이 기준에 얼마나 민감한지 확인할 수 있다.

```python
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

event_log_path = "docs/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv"
selected_review_gap_threshold = -0.20
review_gap_thresholds = [-0.36, selected_review_gap_threshold, 0.0]

event_log = pd.read_csv(event_log_path)

print("1) raw input shape and first rows")
print("shape:", event_log.shape)
print(event_log.head())
print()

sample_rows = event_log[["sample_id", "period"]].drop_duplicates().reset_index(drop=True)
print("2) sample rows")
print(sample_rows)
print()

feature_table = (
    event_log.sort_values(["sample_id", "second"])
    .groupby(["sample_id", "period"], as_index=False)
    .agg(
        mean_flow=("flow", "mean"),
        late_drop_rate=("flow", lambda values: values.iloc[-1] - values.iloc[-2]),
    )
)
print("3) add features")
print(feature_table.round(2))
print()

baseline = (
    pd.DataFrame(
        [
            {
                "baseline_mean_flow": feature_table.loc[
                    feature_table["period"] == "baseline", "mean_flow"
                ].mean(),
                "baseline_late_drop_rate": feature_table.loc[
                    feature_table["period"] == "baseline", "late_drop_rate"
                ].mean(),
            }
        ]
    )
)
print("4) build baseline from baseline samples")
print(baseline.round(2))
print()

comparison_table = feature_table[feature_table["period"] == "recent"].copy()
comparison_table["baseline_mean_flow"] = baseline.loc[0, "baseline_mean_flow"]
comparison_table["baseline_late_drop_rate"] = baseline.loc[0, "baseline_late_drop_rate"]
comparison_table["baseline_gap"] = (
    comparison_table["late_drop_rate"] - comparison_table["baseline_late_drop_rate"]
)
print("5) compare recent samples with baseline")
print(comparison_table.round(2))
print()

selected_output_table = None
threshold_results = []
for threshold in review_gap_thresholds:
    output_table = comparison_table.copy()
    output_table["output"] = output_table["baseline_gap"].apply(
        lambda gap: "검토 필요" if gap <= threshold else "정상 범위"
    )
    if threshold == selected_review_gap_threshold:
        selected_output_table = output_table.copy()
    threshold_results.append(
        {
            "review_gap_threshold": threshold,
            "review_count": int((output_table["output"] == "검토 필요").sum()),
            "review_samples": ",".join(
                output_table.loc[output_table["output"] == "검토 필요", "sample_id"]
            )
            or "none",
        }
    )

print("6) final output structure when review_gap_threshold = -0.20")
print(selected_output_table.round(2))
print()
print("7) threshold sensitivity")
print(pd.DataFrame(threshold_results))
```

예상 출력:

```text
1) raw input shape and first rows
shape: (36, 4)
  sample_id    period  second  flow
0        B1  baseline       0  0.80
1        B1  baseline       1  0.92
2        B1  baseline       2  1.02
3        B1  baseline       3  1.04
4        B1  baseline       4  1.00

2) sample rows
  sample_id    period
0        B1  baseline
1        B2  baseline
2        B3  baseline
3        R1    recent
4        R2    recent
5        R3    recent

3) add features
  sample_id    period  mean_flow  late_drop_rate
0        B1  baseline       0.96           -0.04
1        B2  baseline       0.94           -0.06
2        B3  baseline       0.92           -0.04
3        R1    recent       0.83           -0.32
4        R2    recent       0.90           -0.08
5        R3    recent       0.94           -0.40

4) build baseline from baseline samples
   baseline_mean_flow  baseline_late_drop_rate
0                0.94                    -0.05

5) compare recent samples with baseline
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35

6) final output structure when review_gap_threshold = -0.20
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap output
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27  검토 필요
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03  정상 범위
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35  검토 필요

7) threshold sensitivity
   review_gap_threshold  review_count review_samples
0                 -0.36             0           none
1                 -0.20             2          R1,R3
2                  0.00             3       R1,R2,R3
```

이 예제는 원시 로그에서 같은 행이 어떻게 단계적으로 데이터셋 후보 구조가 되는지 보여 줍니다. 처음에는 `event_log`에서 `sample_id`와 `period`를 기준으로 샘플 행을 잡고, 그다음 시점별 유량에서 `mean_flow`와 `late_drop_rate`를 계산합니다. 이어서 `baseline` 기간 샘플만으로 기준선을 만들고, `recent` 기간 샘플을 그 기준선과 비교합니다. 마지막 운영 출력은 미리 들어 있던 열이 아니라 `baseline_gap`과 `review_gap_thresholds`에서 생성됩니다. 기준을 `-0.36`으로 두면 검토 후보가 없고, `-0.20`으로 두면 R1과 R3이 검토 후보가 되며, `0.0`으로 두면 최근 샘플 셋이 모두 검토 후보가 됩니다. 즉 출력 열은 단독으로 존재하는 것이 아니라 `샘플 설정 -> 특징 계산 -> 기준선 생성 -> 기준선 비교 -> 운영 판단 기준`이라는 앞선 단계의 결과를 이어받아 만들어집니다.

같은 표를 조금 더 해부해서 보면, 네 구조가 실제로 어느 칸에 들어 있는지도 분명해집니다.

| 열 이름 | 여기서 맡는 역할 | 왜 이 역할로 읽는가 |
| --- | --- | --- |
| `sample_id` | 샘플 식별자 | 무엇을 한 건으로 셌는지 가리키기 때문 |
| `mean_flow`, `late_drop_rate` | 특징 | 샘플의 상태를 설명하는 값이기 때문 |
| `baseline_mean_flow`, `baseline_late_drop_rate` | 기준선 열 | 평소 구간의 대표값을 따로 적어 둔 값이기 때문 |
| `baseline_gap` | 기준선 비교 열 | 현재 샘플과 평소 기준선의 차이를 직접 적어 둔 값이기 때문 |
| `output` | 출력 구조 | 사람이 읽거나 다음 단계가 이어받을 결과 형식이기 때문 |

이 표를 보면 `데이터셋 후보`가 단순히 열이 많은 표를 뜻하는 것이 아니라, 같은 행 안에 `샘플`, `설명 값`, `비교 결과`, `결과 형식`이 서로 역할을 나눠 들어 있는 구조라는 점이 드러납니다.

여기서 한 번 더 중요한 차이를 짚어 둘 필요가 있습니다. 출력 구조는 아직 `정답 라벨이 확정된 학습 데이터`를 뜻하지 않을 수도 있습니다. `검토 필요`, `정상 범위` 같은 출력과 `yes/no` 같은 지도학습 라벨은 비슷해 보일 수 있지만, 실제로는 다를 수 있습니다.

| 출력 구조가 뜻하는 것 | 지금 단계에서의 읽기 |
| --- | --- |
| `검토 필요`, `주의`, `정상 범위` | 사람이 먼저 확인할 운영용 결과 |
| `정상/비정상` 같은 고정 라벨 | 나중에 예측 문제로 넘길 수 있는 목표 라벨 후보 |

이 구분을 먼저 두면 뒤에서 `출력 구조`를 말할 때도 곧바로 `라벨이 이미 완성되었다`고 오해하지 않게 됩니다.

이 흐름을 더 짧게 기억하면 다음 순서로 정리할 수 있습니다.

1. 무엇을 샘플 1건으로 볼지 정한다.
2. 그 샘플을 설명할 특징을 남긴다.
3. 최근과 평소를 비교할 기준선을 만든다.
4. 사람이 읽거나 모델이 이어받을 출력 구조를 정한다.

이 네 단계는 뒤에서 각각 다른 장으로 펼쳐지지만, 실제로는 하나의 연속된 판단입니다. 따라서 어떤 장을 읽더라도 `지금 이 설명이 샘플, 특징, 기준선, 출력 구조 중 어느 단계에 속하는가`를 함께 떠올리면 길을 잃지 않게 됩니다. `샘플을 정해야 특징이 생기고, 특징을 정해야 비교 구조가 생기고, 비교 구조가 생겨야 출력 구조가 정리된다`는 관계를 붙잡으면, 데이터셋 후보는 파일 하나의 이름이 아니라 이 네 구조가 서로 맞물리도록 설계된 표라는 점도 더 선명해집니다. 더 넓게 보면 이 절은 `example 단위`, `설명 변수`, `비교 기준`, `결과 형식`이 한 데이터 문제 안에서 어떤 순서로 맞물리는지 정리하는 최소 계약을 세웁니다. 따라서 데이터셋 후보는 `열이 많은 표`가 아니라, 하나의 example 안에 설명 값, 비교 기준, 결과 형식이 서로 역할을 나눠 들어 있는 구조로 읽어야 합니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `example`, `labeled example`, `feature`, `label`. example 안에서 feature와 label이 어떤 역할을 맡는지 분리해 설명하므로, 샘플-특징-기준선-출력 구조를 한 표 안의 역할 구분으로 읽는 이 절의 전개를 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- U.S. Bureau of Labor Statistics, `Base period`. 비교를 위한 기준 구간(reference period)이라는 일반 개념을 제공하므로, 현재 샘플의 값이 기준선과 비교되어야 의미를 얻는다는 이 절의 `baseline` 설명을 보강합니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. derivation과 activity context를 함께 남겨야 한다고 정리하므로, 출력 구조가 앞선 샘플 설정, 특징 계산, 기준선 비교의 결과라는 이 절의 상위 프레임을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
