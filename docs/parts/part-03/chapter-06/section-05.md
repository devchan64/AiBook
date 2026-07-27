# P3-6.5 서로 단위와 크기가 다른 특징은 어떻게 함께 읽고 남기는가

> Section ID: `P3-6.5`
> Version: `v2026.07.25`

[특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature)을 몇 개 만들고 나면 다시 이런 혼동을 겪기 쉽습니다. `값이 큰 열이 더 중요한가?`, `초 단위와 압력 단위를 같은 표에 둬도 되는가?`, `평균이 200인 열과 0.2인 열을 그냥 나란히 비교해도 되는가?` 여기서 먼저 필요한 것은 숫자 크기보다 단위, 범위, 변동 폭, [기준선(baseline)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-baseline) 대비 변화를 구분해 읽는 감각입니다.

한 표에 함께 있다는 사실과 같은 크기 기준으로 읽는다는 판단은 같은 말이 아닙니다. 특징은 서로 다른 단위(unit), 범위(range), 변동 폭을 가질 수 있고, 이 차이를 모른 채 숫자 크기만 보면 구조를 잘못 읽기 쉽습니다.

예를 들어 자동 동작 1회 요약 표에 아래 열이 같이 들어 있다고 해 보겠습니다.

| 열 이름 | 예시 값 | 뜻 |
| --- | ---: | --- |
| `duration_seconds` | 48 | 동작 지속 시간 |
| `pressure_mean` | 101.2 | 평균 압력 |
| `flow_std` | 0.18 | 유량 변동성 |
| `late_drop_rate` | -0.42 | 후반 하강률 |

이 네 값은 모두 숫자이지만, 같은 종류의 크기를 말하지는 않습니다.

- `duration_seconds`는 시간 길이입니다.
- `pressure_mean`은 압력 수준입니다.
- `flow_std`는 흔들림의 크기입니다.
- `late_drop_rate`는 변화 방향과 속도입니다.

즉 숫자라는 공통점만 보고 `101.2가 48보다 더 중요하다`처럼 읽으면 안 됩니다.

## 왜 이 구분이 필요한가

특징 설계 단계에서 이 감각이 필요한 이유는 세 가지입니다.

| 먼저 알아야 할 것 | 왜 필요한가 |
| --- | --- |
| 단위가 다르다 | 같은 숫자 크기라도 전혀 다른 의미를 가질 수 있기 때문 |
| 범위가 다르다 | 어떤 열은 원래 0 근처에서 움직이고, 어떤 열은 100 근처에서 움직일 수 있기 때문 |
| 변동 폭이 다르다 | 변화가 작은 열과 큰 열을 같은 눈금으로 보면 중요한 차이를 놓칠 수 있기 때문 |

이 구분은 아직 모델 계산을 위한 정규화 공식으로 들어가자는 뜻이 아닙니다. Part 3에서는 먼저 `무엇이 큰 수여서 중요한 것이 아니라, 무엇을 재는 수인가가 중요하다`는 감각을 세우는 것이 목적입니다.

## 같은 표에 둔다는 것과 같이 읽는다는 것은 다르다

같은 샘플 표에 여러 특징을 둘 수는 있습니다. 하지만 읽는 방식은 열마다 달라질 수 있습니다.

| 특징 열 | 먼저 읽는 방식 |
| --- | --- |
| `duration_seconds` | 평소보다 길어졌는지 본다 |
| `pressure_mean` | 기준선 대비 수준 차이를 본다 |
| `flow_std` | 흔들림이 커졌는지 본다 |
| `late_drop_rate` | 후반 구조가 더 가파르게 무너졌는지 본다 |

즉 비교는 `숫자끼리`가 아니라 `같은 역할의 같은 열끼리` 해야 합니다. `duration_seconds`와 `pressure_mean`를 직접 크기 비교하는 것이 아니라, `이번 duration_seconds`를 평소 duration_seconds와 비교하고, `이번 pressure_mean`를 평소 pressure_mean와 비교하는 식으로 읽어야 합니다.

## 자주 하는 오해

| 오해 | 실제로는 무엇을 다시 봐야 하는가 |
| --- | --- |
| 값이 큰 열이 더 중요하다 | 단위와 역할이 다른 숫자를 크기만으로 비교하고 있지 않은가 |
| 0.2 같은 작은 값은 영향이 약하다 | 원래 그 열이 작은 범위에서만 움직이는 특징은 아닌가 |
| 모든 특징은 같은 방식으로 읽으면 된다 | 수준, 변화, 변동성, 시간 길이를 구분하고 있는가 |

예를 들어 `flow_std = 0.18`은 숫자만 보면 작아 보일 수 있지만, 평소가 `0.03`이었다면 실제로는 큰 흔들림일 수 있습니다. 반대로 `pressure_mean = 101.2`는 숫자만 보면 커 보이지만, 평소가 `101.0`이라면 상대 변화는 작을 수 있습니다.

## 그래서 무엇을 먼저 적어 두어야 하는가

Part 3 단계에서는 각 특징 열 옆에 아래 세 가지를 짧게 적어 둘 수 있으면 훨씬 안전합니다.

| 적어 둘 것 | 예시 |
| --- | --- |
| 이 열의 단위 또는 의미 | 초, 압력, 변화율, 변동성 |
| 이 열이 보여 주는 구조 | 수준, 방향, 흔들림, 지속 시간 |
| 비교 기준 | 절대값 자체인지, 기준선 대비 차이인지 |

예를 들면 이렇게 적을 수 있습니다.

| 열 이름 | 단위/뜻 | 구조 역할 | 비교 방식 |
| --- | --- | --- | --- |
| `duration_seconds` | 초 | 지속 시간 | 평소보다 길어졌는가 |
| `pressure_mean` | 압력 수준 | 평균 수준 | 기준선과 차이가 큰가 |
| `flow_std` | 변동성 | 흔들림 | 평소보다 흔들림이 커졌는가 |
| `late_drop_rate` | 변화율 | 후반 붕괴 속도 | 후반 기울기가 더 가팔라졌는가 |

이 표가 있으면 `무슨 숫자인지`와 `어떻게 읽을지`가 함께 고정됩니다.

## 작은 점검 표

이 절에서는 Python으로 고정된 두 행을 출력하기보다, 숫자 열을 어떤 축으로 읽을지 표로 고정해 두는 편이 더 적합합니다. 예를 들어 아래 작업 표를 보겠습니다.

| event_id | `duration_seconds` | `pressure_mean` | `flow_std` | `late_drop_rate` |
| --- | ---: | ---: | ---: | ---: |
| A | 48 | 101.2 | 0.18 | -0.42 |
| B | 44 | 100.9 | 0.05 | -0.10 |
| 기준선 | 45 | 101.0 | 0.03 | -0.12 |

절대값만 보면 `pressure_mean`이 가장 커 보입니다. 하지만 기준선 대비 변화로 읽으면 다른 그림이 나옵니다.

| event_id | `duration_delta` | `pressure_delta` | `flow_std_delta` | `late_drop_delta` |
| --- | ---: | ---: | ---: | ---: |
| A | 3 | 0.2 | 0.15 | -0.30 |
| B | -1 | -0.1 | 0.02 | 0.02 |

이 표에서 중요한 것은 숫자의 절대 크기가 아니라, 각 열이 맡는 역할과 같은 열 안에서의 변화입니다. 처음 표만 보면 `101.2`가 커 보이고 `0.18`은 작아 보일 수 있지만, 기준선 대비 변화를 보면 `flow_std_delta=0.15`는 오히려 큰 흔들림 증가일 수 있고, `pressure_delta=0.2`는 작은 수준 차이일 수 있습니다.

| 열 이름 | 역할 | 먼저 비교하는 방식 |
| --- | --- | --- |
| `duration_seconds` | 지속 시간(duration) | 기준선 대비 차이 |
| `pressure_mean` | 수준(level) | 기준선 대비 차이 |
| `flow_std` | 변동성(variability) | 기준선 대비 차이 |
| `late_drop_rate` | 변화(change) | 기준선 대비 차이 |

그래서 `큰 숫자`보다 `같은 역할의 같은 열을 어떻게 비교하는가`를 먼저 읽어야 합니다.

즉 Part 3의 책임은 다음까지입니다.

1. 같은 표 안에 서로 다른 의미의 숫자가 함께 있을 수 있음을 안다.
2. 각 특징이 수준, 변화, 변동성, 시간 길이 중 무엇을 뜻하는지 적을 수 있다.
3. 숫자 크기 자체보다 `같은 열의 기준선 대비 변화`가 더 중요할 수 있음을 안다.

특징 표의 숫자들은 모두 같은 종류의 크기를 말하지 않으므로, 단위와 역할을 먼저 적고 같은 열의 기준선 대비 변화로 읽어야 합니다. 이 절은 스케일 공식 소개가 아니라, 서로 다른 측정 축을 한 작업 표 안에서 어떻게 역할별로 읽을 것인가의 문제로 다시 볼 수 있습니다.


같은 문제는 모델 입력에서도 드러납니다. 아래 예제는 같은 [k-NN(k-nearest neighbors)](../../../reference/concept-glossary-parts/10-kieuk.md#glossary-k-nn) 모델을 쓰되, 스케일 조정 없이 읽을 때와 `StandardScaler`로 각 열을 같은 비교 눈금으로 맞춘 뒤 읽을 때 최근접 이웃이 어떻게 달라지는지 보여 줍니다.

문제 상황: 단위와 범위가 다른 특징을 그대로 k-NN에 넣으면 큰 숫자 범위의 열이 이웃 판단을 더 크게 끌고 갈 수 있음을 확인합니다.

입력(input): 지속 시간, 압력 변화, 유량 변동성 변화가 함께 있는 작은 특징 표와 확인할 새 샘플.

기대 출력(output): 스케일 조정 전후의 최근접 `event_id`와 예측값.

확인할 개념: 같은 표에 둔 특징이라도 모델이 거리로 비교할 때는 스케일 조정 여부가 이웃과 예측을 바꿀 수 있습니다.

```python
# 단위와 범위가 다른 특징을 거리 기반 모델이 어떻게 다르게 읽는지 확인합니다.
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

features = pd.DataFrame(
    [
        {"event_id": "A", "duration_seconds": 44, "pressure_delta": 0.10, "flow_std_delta": 0.02, "review_needed": 0},
        {"event_id": "B", "duration_seconds": 48, "pressure_delta": 0.20, "flow_std_delta": 0.15, "review_needed": 1},
        {"event_id": "C", "duration_seconds": 43, "pressure_delta": -0.10, "flow_std_delta": 0.01, "review_needed": 0},
        {"event_id": "D", "duration_seconds": 49, "pressure_delta": 0.00, "flow_std_delta": 0.16, "review_needed": 1},
    ]
)
query = pd.DataFrame(
    [{"duration_seconds": 44, "pressure_delta": 0.15, "flow_std_delta": 0.14}]
)
columns = ["duration_seconds", "pressure_delta", "flow_std_delta"]

plain = KNeighborsClassifier(n_neighbors=1).fit(features[columns], features["review_needed"])
scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=1))
scaled.fit(features[columns], features["review_needed"])

plain_neighbor = plain.kneighbors(query, return_distance=False)[0][0]
scaled_query = scaled.named_steps["standardscaler"].transform(query)
scaled_neighbor = scaled.named_steps["kneighborsclassifier"].kneighbors(
    scaled_query, return_distance=False
)[0][0]

print("without scaling nearest_event:", features.iloc[plain_neighbor]["event_id"])
print("without scaling prediction:", int(plain.predict(query)[0]))
print("with scaling nearest_event:", features.iloc[scaled_neighbor]["event_id"])
print("with scaling prediction:", int(scaled.predict(query)[0]))
```

예상 출력:

```text
without scaling nearest_event: A
without scaling prediction: 0
with scaling nearest_event: B
with scaling prediction: 1
```

스케일 조정 전에는 `duration_seconds=44`가 같은 A가 가장 가깝게 잡힙니다. 하지만 압력 변화와 유량 변동성 변화까지 같은 눈금으로 맞추면 B가 더 가까운 사례로 바뀝니다. 이 출력은 `값이 큰 열이 더 중요하다`가 아니라, 거리 기반 모델에서는 큰 범위의 열이 계산을 지배할 수 있음을 보여 줍니다. 그래서 Part 3에서는 모델 공식을 자세히 배우기 전에도, 각 특징의 단위와 범위, 비교 방식을 먼저 적어 두어야 합니다.

따라서 특징 표는 숫자 크기 경쟁표가 아니라, 서로 다른 측정 축을 역할별로 나란히 두고 읽는 구조로 이해해야 합니다.

## 작은 도식으로 보기

이 절의 순서는 `서로 다른 단위와 크기`를 한 표에 두더라도, 열 역할별로 읽고 같은 열의 기준선과 비교해야 한다는 점을 붙잡습니다. 숫자 크기 자체보다 `무엇을 재는 열인가`가 먼저입니다.

--8<-- "assets/part-03/chapter-06/p3-6-5-mermaid-01-ko.mmd"

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `feature`. feature를 prediction에 쓰는 input variable로 설명하므로, 특징은 숫자 크기 자체보다 무엇을 입력 변수로 재고 있는지가 먼저 중요하다는 점을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `feature engineering`. 원시 데이터를 학습에 더 유용한 형태로 바꾸는 과정을 설명하므로, 시간 길이, 수준, 변동성, 변화율처럼 서로 다른 역할의 특징을 구분해 읽어야 한다는 이 절의 설명을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 비교는 같은 항목을 기준 시점과 나란히 놓을 때 성립한다는 일반 reference 개념을 제공하므로, 서로 다른 특징끼리 직접 크기 비교하기보다 같은 열의 기준선 대비 변화로 읽어야 한다는 설명에 참고할 수 있습니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
