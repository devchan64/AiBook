# 데이터 모델링 모듈 Python 예제 초안 스니펫

## 목적

이 문서는 책 본문에 넣기 전에 공통 Python 예제를 어떤 수준으로 작성할지 초안 스니펫 형태로 정리한다.

여기서는 완전한 장문 설명보다, 재사용 가능한 최소 코드 구조와 출력 포인트를 먼저 고정한다.

## 예제 1. 원시 로그를 동작 1회로 묶기

입력 설명:
한 행은 시간 순서대로 수집된 측정 시점 하나이고, 같은 `action_id`를 가진 여러 행이 자동으로 실행된 동작 1회를 이룬다.

```python
import pandas as pd

raw = pd.DataFrame(
    [
        ["A-101", 0, 0.20, 24.8, 0.3],
        ["A-101", 1, 0.35, 25.6, 0.8],
        ["A-101", 2, 0.55, 27.1, 1.5],
        ["A-101", 3, 0.70, 28.4, 2.1],
        ["A-102", 0, 0.18, 24.5, 0.2],
        ["A-102", 1, 0.32, 25.3, 0.7],
        ["A-102", 2, 0.60, 27.8, 1.6],
        ["A-102", 3, 0.42, 27.0, 1.1],
        ["A-103", 0, 0.22, 24.9, 0.4],
        ["A-103", 1, 0.37, 25.9, 0.9],
        ["A-103", 2, 0.58, 28.1, 1.7],
        ["A-103", 3, 0.41, 27.2, 1.0],
        ["A-104", 0, 0.21, 24.7, 0.3],
        ["A-104", 1, 0.34, 25.4, 0.8],
        ["A-104", 2, 0.56, 27.6, 1.4],
        ["A-104", 3, 0.39, 26.9, 1.0],
        ["A-105", 0, 0.19, 24.6, 0.2],
        ["A-105", 1, 0.31, 25.1, 0.7],
        ["A-105", 2, 0.54, 27.3, 1.3],
        ["A-105", 3, 0.38, 26.7, 0.9],
        ["A-106", 0, 0.25, 25.0, 0.5],
        ["A-106", 1, 0.39, 26.2, 1.0],
        ["A-106", 2, 0.63, 28.9, 1.9],
        ["A-106", 3, 0.45, 27.8, 1.3],
    ],
    columns=["action_id", "time_step", "control_level", "sensor_a", "sensor_b"],
)

print("rows:", len(raw))
print("actions:", raw["action_id"].nunique())
print("rows per action:")
print(raw.groupby("action_id").size())
```

출력에서 보여 줄 핵심:

- 전체 행 수
- 동작 수
- 동작별 측정 시점 수

예상 출력 예시:

```text
rows: 24
actions: 6
rows per action:
action_id
A-101    4
A-102    4
A-103    4
A-104    4
A-105    4
A-106    4
dtype: int64
```

해석 문장 예시:
한 행은 샘플 1건이 아니라 측정 시점 하나이며, 분석 단위는 같은 `action_id`를 공유하는 네 행의 묶음이다.

## 예제 2. 동작 1회 요약 특징 만들기

입력 설명:
예제 1의 원시 시계열에서 각 동작 1회를 하나의 요약 행으로 바꾼다.

```python
def first_half_mean(values):
    midpoint = max(1, len(values) // 2)
    return values.iloc[:midpoint].mean()


def second_half_mean(values):
    midpoint = max(1, len(values) // 2)
    return values.iloc[midpoint:].mean()


summary = (
    raw.groupby("action_id")
    .agg(
        duration_steps=("time_step", "count"),
        control_mean=("control_level", "mean"),
        sensor_a_peak=("sensor_a", "max"),
        sensor_b_mean=("sensor_b", "mean"),
        sensor_a_early_mean=("sensor_a", first_half_mean),
        sensor_a_late_mean=("sensor_a", second_half_mean),
    )
    .reset_index()
)

summary["sensor_a_gap"] = summary["sensor_a_late_mean"] - summary["sensor_a_early_mean"]

print(summary.round(2))
```

출력에서 보여 줄 핵심:

- 동작 1회당 한 행이 생성된다는 점
- 평균, 최대값 같은 값이 특징 열이 된다는 점

예상 출력 예시:

```text
  action_id  duration_steps  control_mean  sensor_a_peak  sensor_b_mean  sensor_a_early_mean  sensor_a_late_mean  sensor_a_gap
0     A-101               4          0.45           28.4           1.18                 25.20               27.75          2.55
1     A-102               4          0.38           27.8           0.90                 24.90               27.40          2.50
2     A-103               4          0.45           28.1           1.00                 25.40               27.65          2.25
3     A-104               4          0.38           27.6           0.88                 25.05               27.25          2.20
4     A-105               4          0.36           27.3           0.78                 24.85               27.00          2.15
5     A-106               4          0.43           28.9           1.18                 25.60               28.35          2.75
```

해석 문장 예시:
이제 모델과 비교 표는 원시 로그 24행이 아니라 동작 6건의 요약 행 6개를 입력으로 받을 수 있다.

## 예제 3. 최근 구간과 기준선 비교

입력 설명:
예제 2의 요약 행에서 최근 2건을 현재 검토 대상, 앞의 4건을 기준선으로 둔다.

```python
recent = summary.tail(2).mean(numeric_only=True)
baseline = summary.head(len(summary) - 2).mean(numeric_only=True)

comparison = pd.DataFrame(
    {
        "recent": recent,
        "baseline": baseline,
        "delta": recent - baseline,
    }
)

print(comparison.round(2))
```

출력에서 보여 줄 핵심:

- 최근 구간 평균
- 기준선 평균
- 차이값

예상 출력 예시:

```text
                    recent  baseline  delta
duration_steps         4.00      4.00   0.00
control_mean           0.40      0.42  -0.02
sensor_a_peak         28.10     27.98   0.12
sensor_b_mean          0.98      0.99  -0.01
sensor_a_early_mean   25.23     25.14   0.09
sensor_a_late_mean    27.68     27.51   0.17
sensor_a_gap           2.45      2.38   0.08
```

해석 문장 예시:
최근 구간이 기준선보다 조금 높거나 낮게 보이더라도, 여기서 바로 원인을 단정하지 않고 먼저 변화 신호로만 기록하는 편이 안전하다.

## 예제 4. 같은 평균, 다른 패턴 비교

입력 설명:
두 동작의 평균이 같게 보이도록 만든 뒤, 변동성과 구간 평균이 어떻게 달라지는지 보여 준다.

```python
pattern_raw = pd.DataFrame(
    {
        "time_step": [0, 1, 2, 3, 0, 1, 2, 3],
        "case_id": ["B-201", "B-201", "B-201", "B-201", "B-202", "B-202", "B-202", "B-202"],
        "sensor_a": [26.8, 26.9, 27.1, 27.2, 25.5, 26.0, 28.0, 28.5],
    }
)

pattern = (
    pattern_raw.groupby("case_id")
    .agg(
        sensor_a_mean=("sensor_a", "mean"),
        sensor_a_std=("sensor_a", "std"),
        early_segment_mean=("sensor_a", first_half_mean),
        late_segment_mean=("sensor_a", second_half_mean),
    )
    .reset_index()
)

print(pattern.round(2))
```

출력에서 보여 줄 핵심:

- 평균은 같아도 분산과 구간 패턴은 다르다는 점

예상 출력 예시:

```text
  case_id  sensor_a_mean  sensor_a_std  early_segment_mean  late_segment_mean
0   B-201           27.0          0.18               26.85              27.15
1   B-202           27.0          1.35               25.75              28.25
```

해석 문장 예시:
대표값 하나만 저장하면 두 동작이 같아 보이지만, 변동성과 구간 평균을 함께 보면 서로 다른 패턴이라는 사실이 드러난다.

## 본문 반영 시 주의점

- 각 코드 블록 앞에 입력 데이터가 무엇을 뜻하는지 짧게 설명한다.
- 코드 뒤에는 반드시 출력 예시와 해석 문장을 둔다.
- 특정 장비나 기업 전용 열 이름은 넣지 않는다.
- 모델 학습 코드로 바로 넘어가지 않고, 먼저 데이터 표현이 어떻게 바뀌는지 보여 준다.
- Part 1/2에서는 예제 1, 2를 먼저 쓰고, Part 3/6에서는 예제 3, 4를 연결해 평가와 회고 문장으로 이어 붙인다.
- `경고`, `검토 필요`, `원인 확정 아님` 같은 경계 문장을 출력 해석 바로 아래에 둔다.

## 현재 결론

이 스니펫 세트는 데이터 모델링 설명을 추상 문장에만 머물지 않게 하고, 독자가 직접 실행해 관찰 구조를 확인하게 만드는 최소 공통 자산으로 쓸 수 있다.
