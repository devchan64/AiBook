# 데이터 모델링 모듈 Python 예제 초안 스니펫

## 목적

이 문서는 책 본문에 넣기 전에 공통 Python 예제를 어떤 수준으로 작성할지 초안 스니펫 형태로 정리한다.

여기서는 완전한 장문 설명보다, 재사용 가능한 최소 코드 구조와 출력 포인트를 먼저 고정한다.

## 예제 1. 원시 로그를 동작 1회로 묶기

```python
import pandas as pd

raw = pd.DataFrame(
    [
        ["A-101", 0, 0.20, 24.8, 0.3],
        ["A-101", 1, 0.35, 25.6, 0.8],
        ["A-101", 2, 0.55, 27.1, 1.5],
        ["A-102", 0, 0.18, 24.5, 0.2],
        ["A-102", 1, 0.32, 25.3, 0.7],
        ["A-102", 2, 0.60, 27.8, 1.6],
    ],
    columns=["action_id", "time_step", "control_level", "sensor_a", "sensor_b"],
)

print("rows:", len(raw))
print("actions:", raw["action_id"].nunique())
print(raw.groupby("action_id").size())
```

출력에서 보여 줄 핵심:

- 전체 행 수
- 동작 수
- 동작별 측정 시점 수

## 예제 2. 동작 1회 요약 특징 만들기

```python
summary = (
    raw.groupby("action_id")
    .agg(
        duration_steps=("time_step", "count"),
        control_mean=("control_level", "mean"),
        sensor_a_peak=("sensor_a", "max"),
        sensor_b_mean=("sensor_b", "mean"),
    )
    .reset_index()
)

print(summary)
```

출력에서 보여 줄 핵심:

- 동작 1회당 한 행이 생성된다는 점
- 평균, 최대값 같은 값이 특징 열이 된다는 점

## 예제 3. 최근 구간과 기준선 비교

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

## 예제 4. 같은 평균, 다른 패턴 비교

```python
pattern = pd.DataFrame(
    {
        "case_id": ["B-201", "B-202"],
        "sensor_a_mean": [27.0, 27.0],
        "sensor_a_std": [0.4, 1.6],
        "early_segment_mean": [26.8, 25.5],
        "late_segment_mean": [27.2, 28.5],
    }
)

print(pattern)
```

출력에서 보여 줄 핵심:

- 평균은 같아도 분산과 구간 패턴은 다르다는 점

## 본문 반영 시 주의점

- 각 코드 블록 앞에 입력 데이터가 무엇을 뜻하는지 짧게 설명한다.
- 코드 뒤에는 반드시 출력 예시와 해석 문장을 둔다.
- 특정 장비나 기업 전용 열 이름은 넣지 않는다.
- 모델 학습 코드로 바로 넘어가지 않고, 먼저 데이터 표현이 어떻게 바뀌는지 보여 준다.

## 현재 결론

이 스니펫 세트는 데이터 모델링 설명을 추상 문장에만 머물지 않게 하고, 독자가 직접 실행해 관찰 구조를 확인하게 만드는 최소 공통 자산으로 쓸 수 있다.
