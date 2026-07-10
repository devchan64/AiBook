# P3-5.2 요약 표는 평균 밖의 패턴을 어떻게 남기는가

> Section ID: `P3-5.2`
> Version: `v2026.07.10`

같은 평균을 가진 두 동작이 항상 같은 구조를 뜻하지는 않습니다. 평균은 전체 수준을 한눈에 요약하는 데는 유용하지만, 시간에 따라 어떻게 움직였는지까지 모두 보여 주지는 못합니다. 그래서 원시 로그를 요약 표로 바꾸는 단계에서는 `평균이 같다`는 사실만으로 안심하지 않고, 평균 밖의 패턴 차이를 어떻게 남길지 함께 고민해야 합니다.

여기서는 요약 표 변환 절차 자체를 다시 설명하지 않습니다. 대신 앞 절에서 만든 요약 표가 평균만 남기는 표가 아니라, 뒤의 특징 설계와 기준선 비교로 이어질 패턴 차이까지 남겨야 한다는 점에 집중합니다.

예를 들어 두 번의 자동 동작이 모두 평균 유량 2.4를 기록했다고 하겠습니다. 하나는 초반에 빠르게 올라갔다가 중반에 안정적으로 유지되고 후반에 천천히 떨어졌을 수 있습니다. 다른 하나는 초반에 거의 움직이지 않다가 후반에 급격히 올라갔다가 바로 떨어졌을 수 있습니다. 평균값 하나만 보면 둘이 비슷해 보이지만, 실제 운영 의미는 전혀 다를 수 있습니다.

이 차이를 드러내기 위해서는 평균 외에 구조를 보여 주는 값을 함께 남겨야 합니다. 예를 들면 다음과 같습니다.

- 초반 평균
- 중반 평균
- 후반 평균
- 구간별 기울기
- 최대값이 나온 시점
- 하강 시작 시점

| 동작 | 평균 유량 | 초반 기울기 | 후반 기울기 | 해석 |
| --- | --- | --- | --- | --- |
| A | 2.4 | 큼 | 완만한 하강 | 비교적 안정적 |
| B | 2.4 | 거의 없음 | 급격한 하강 | 후반 불안정 가능성 |

이 표를 읽을 때도 순서가 있습니다. 먼저 `평균이 같은가`를 보고, 그 다음 `구간 평균이 어떻게 다른가`를 보고, 마지막으로 `기울기나 시점 정보가 어떤 해석을 가능하게 하는가`를 봐야 합니다. 이렇게 읽으면 평균은 같지만 구조는 다르다는 문장이 더 분명해집니다.

| 읽는 층위 | 먼저 보는 값 | 알 수 있는 것 |
| --- | --- | --- |
| 전체 수준 | 전체 평균 | 대략 비슷한 규모인가 |
| 구간 구조 | 초반/중반/후반 평균 | 어느 구간이 달라졌는가 |
| 형태 변화 | 기울기, 최대값 시점, 하강 시작 시점 | 어떤 모양 차이가 있었는가 |

즉 평균은 출발점일 뿐입니다. 평균이 같다고 구조도 같다고 말할 수는 없고, 평균이 다르다고 해서 어느 구간에서 달라졌는지도 자동으로 알 수는 없습니다. 요약 표는 바로 이 층위를 나눠 보여 주는 표여야 합니다.

여기서는 `평균만 보면 놓치는 것`을 따로 적어 두면 요약 표가 무엇을 더 보여 줘야 하는지 분명해집니다.

| 평균만 보면 놓치는 것 | 함께 남겨야 할 값 |
| --- | --- |
| 변화가 초반에 일어났는지 후반에 일어났는지 | 구간 평균 |
| 올라가는 속도와 내려가는 속도가 다른지 | 구간별 기울기 |
| 최고점이 언제 나왔는지 | 최대값 시점 |
| 안정적으로 유지되었는지 급하게 흔들렸는지 | 변동성, 하강 시작 시점 |

여기에 한 가지를 더 붙여야 합니다. 평균은 이상치(outlier)와 분포 치우침(skewness)도 쉽게 가립니다. 예를 들어 대부분의 동작은 비슷한 범위에 있는데 일부 사례만 매우 큰 값으로 튀면, 평균은 올라가지만 `대부분의 동작이 실제로 어떤 수준이었는가`는 흐려질 수 있습니다. 반대로 값 대부분이 한쪽에 몰리고 소수 사례만 반대쪽으로 길게 늘어지면, 평균은 그 비대칭 구조를 잘 보여 주지 못합니다.

| 평균만으로는 잘 안 보이는 것 | 왜 놓치기 쉬운가 | 함께 남겨야 할 값 |
| --- | --- | --- |
| 일부 극단값의 영향 | 소수 사례가 평균을 크게 움직일 수 있음 | 최소값, 최대값, 분위수 |
| 한쪽으로 긴 꼬리 | 평균은 분포 비대칭을 한 숫자로 눌러 버림 | 중간값, 분위수, 구간별 빈도 |
| 대부분은 안정적이지만 일부만 크게 흔들리는 구조 | 평균은 대표 사례와 드문 사례를 분리하지 못함 | 표본 수, 이상치 메모, 변동성 |

아래 간단한 예제는 평균은 같지만 패턴은 다른 경우를 숫자로 확인하는 방법입니다.

문제 상황: 전체 평균은 같아 보여도 구간별 흐름이 다르면 다른 운영 구조로 읽어야 한다는 점을 확인합니다.

입력(input): `early_flow_mean`, `mid_flow_mean`, `late_flow_mean`만 남겨 둔 동작 요약 표

기대 출력(output): 같은 `overall_mean` 아래에서도 구간 차이와 `pattern_note`가 달라지는 출력

확인할 개념: 평균 하나만으로는 패턴 차이를 다 설명할 수 없으므로 구간별 차이와 해석 메모를 함께 남겨야 한다

```python
import pandas as pd

summary = pd.DataFrame(
    [
        {
            "event_id": "A",
            "early_flow_mean": 1.8,
            "mid_flow_mean": 2.8,
            "late_flow_mean": 2.6,
        },
        {
            "event_id": "B",
            "early_flow_mean": 2.4,
            "mid_flow_mean": 2.4,
            "late_flow_mean": 2.4,
        },
    ]
)

summary["overall_mean"] = summary[
    ["early_flow_mean", "mid_flow_mean", "late_flow_mean"]
].mean(axis=1)
summary["mid_minus_early"] = summary["mid_flow_mean"] - summary["early_flow_mean"]
summary["late_minus_mid"] = summary["late_flow_mean"] - summary["mid_flow_mean"]
summary["pattern_note"] = summary.apply(
    lambda row: "mid peak then slight drop"
    if row["mid_minus_early"] > 0 and row["late_minus_mid"] < 0
    else "flat across segments",
    axis=1,
)

print("1) the same overall mean is not enough")
print(summary[["event_id", "overall_mean"]])
print()
print("2) segment-level differences remain")
print(
    summary[
        [
            "event_id",
            "early_flow_mean",
            "mid_flow_mean",
            "late_flow_mean",
            "mid_minus_early",
            "late_minus_mid",
        ]
    ]
)
print()
print("3) one-line pattern interpretation")
print(summary[["event_id", "pattern_note"]])
```

예상 출력:

```text
1) the same overall mean is not enough
  event_id  overall_mean
0        A           2.4
1        B           2.4

2) segment-level differences remain
  event_id  early_flow_mean  mid_flow_mean  late_flow_mean  mid_minus_early  late_minus_mid
0        A              1.8            2.8             2.6              1.0            -0.2
1        B              2.4            2.4             2.4              0.0             0.0

3) one-line pattern interpretation
  event_id               pattern_note
0        A  mid peak then slight drop
1        B       flat across segments
```

두 동작의 `overall_mean`은 모두 2.4입니다. 하지만 2단계를 보면 A는 `mid_minus_early=1.0`, `late_minus_mid=-0.2`로 중반 상승 뒤 후반 하강이 보이고, B는 두 값이 모두 0.0이라 구간 구조 변화가 없습니다. 3단계의 `pattern_note`는 이 차이를 한 문장으로 다시 접은 결과입니다. 따라서 평균만 보면 같은 사례처럼 보이지만, 구간 평균과 구간 차이를 함께 보면 서로 다른 동작 구조라는 점이 드러납니다.

이 예제는 아래 순서로 읽으면 평균과 패턴의 차이가 더 분명해집니다.

1. `overall_mean`이 같은지 본다.
2. 세 구간 평균이 모두 같은지, 어느 한 구간만 다른지 본다.
3. 평균은 같지만 구조는 다른 사례가 운영 해석에서 왜 중요해지는지 한 문장으로 적어 본다.

예를 들어 A는 `중반에 높고 후반에 조금 내려가는 동작`, B는 `처음부터 끝까지 거의 같은 수준의 동작`이라고 요약할 수 있습니다. 이 한 문장 요약이 가능해야 숫자 표가 실제 구조 해석으로 이어집니다.

이때 `같은 평균인데 다른 패턴`을 읽을 때는 무엇을 더 남겨야 하는지도 바로 적어 둘 수 있습니다.

| 평균이 같을 때 더 봐야 할 것 | 왜 필요한가 |
| --- | --- |
| 구간 평균 | 어느 구간에서 차이가 나는지 보이기 위해 |
| 구간별 기울기 | 올라가고 내려가는 속도 차이를 보기 위해 |
| 최대값 시점, 하강 시작 시점 | 모양 변화가 언제 시작되는지 보기 위해 |

이 표의 핵심은 평균을 버리자는 뜻이 아니라, 평균만 남기면 구조 해석이 멈춘다는 점입니다.

이 차이는 나중에 기준선 비교에서도 그대로 중요해집니다. 최근 구간 평균이 평소와 같아 보여도, 후반 하강 패턴이 더 강해졌다면 이미 상태 변화가 시작되었을 수 있기 때문입니다. 따라서 `같은 평균, 다른 패턴`을 읽는 감각은 단지 특징 하나를 더 보는 요령이 아니라, 뒤에서 `최근 구조가 평소와 달라졌는가`를 읽기 위한 준비 단계입니다.

평균이 같다는 이유로 두 동작을 같은 범주로 묶어 버리면, 실제로는 후반 하강이 급한 사례를 놓칠 수 있습니다. 그래서 요약 표에서는 `평균이 같아도 구조는 다를 수 있다`는 점이 드러나야 합니다. 이 생각이 나중의 특징 설계, 세그먼트 표현, 기준선 비교로 자연스럽게 이어집니다.

## 출처와 참고 자료

- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. 시간 흐름 안에서 신호와 패턴을 읽는 관점을 제공하므로, 평균 하나만으로는 구조 변화를 다 설명할 수 없고 구간별 변화와 모양 차이를 함께 남겨야 한다는 이 절의 일반 근거가 됩니다. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`의 `feature engineering`. feature engineering을 원시 데이터를 더 유용한 입력 표현으로 바꾸는 과정으로 설명하므로, 요약 표가 평균만 남기는 표가 아니라 구간 평균, 기울기, 시점 같은 구조 정보를 함께 남겨야 한다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. provenance framework가 derivation과 processing steps를 설명 가능하게 남겨야 한다고 정리하므로, 전체 평균 외에 어떤 구간 요약과 파생값을 남겼는지 재구성 가능해야 한다는 상위 프레임을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
