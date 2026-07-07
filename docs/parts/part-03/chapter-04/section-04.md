# P3-4.4 샘플 단위를 잘못 잡았다는 신호는 무엇인가

> Section ID: `P3-4.4`
> Version: `v2026.07.07`

Chapter 4 앞 절까지 읽으면 샘플 단위가 중요하다는 점은 이해됩니다. 하지만 실제 작업에서는 한 번 더 다른 어려움이 남습니다. `지금 내가 샘플 단위를 잘못 잡고 있다는 사실을 어떻게 알아차릴 수 있는가?` 샘플 단위를 잘못 잡은 채 특징, 라벨, 비교표를 계속 만들다가 뒤늦게 전체 구조가 흔들렸다는 사실을 깨닫는 경우가 많습니다. 그래서 이 절에서는 샘플 단위 오판을 의심해야 하는 대표 신호를 한 번에 모읍니다.

샘플 단위가 잘못 잡히면 보통 나중 단계에서 이상한 모양으로 다시 드러납니다. 같은 라벨이 여러 줄에 반복되어 붙거나, 특징이 한 줄에서는 설명이 안 되거나, 비교표는 있는데 `무엇이 한 건인지` 설명이 안 되면 샘플 단위를 다시 의심해야 합니다.

## 가장 흔한 경고 신호

| 지금 보이는 이상한 현상 | 먼저 의심할 것 |
| --- | --- |
| 같은 `event_id`의 여러 줄에 같은 라벨이 반복해서 붙는다 | 라벨이 사실은 동작 1회 단위인데 시점 행을 샘플로 읽고 있을 수 있다 |
| 평균, 기울기, 변동성 같은 특징을 한 줄에 바로 설명하기 어렵다 | 시점 기록을 샘플처럼 읽고 있을 수 있다 |
| 비교 결과를 말하려는데 `이번 한 건`이 무엇인지 문장으로 설명이 안 된다 | 샘플 단위와 비교 단위가 섞였을 수 있다 |
| 훈련/평가를 나누면 같은 동작의 가까운 줄이 양쪽에 함께 들어간다 | 분할 단위가 샘플 단위와 어긋났을 수 있다 |
| 최근 구간 비교표를 만들었는데 개별 동작과 집계 구간이 한 표에서 섞여 보인다 | 샘플과 구간 층위를 같은 단위처럼 읽고 있을 수 있다 |

이 표의 핵심은 `모든 문제가 샘플 단위 때문`이라는 뜻이 아닙니다. 다만 Part 3 단계에서 이런 현상이 보이면, 특징을 더 늘리거나 모델을 바꾸기 전에 샘플 단위를 다시 보는 편이 더 효율적이라는 뜻입니다.

## 특징이 자꾸 설명되지 않으면 샘플 단위를 다시 본다

자주 겪는 장면은 이렇습니다. `late_drop_rate`, `flow_std`, `duration_seconds` 같은 특징을 만들었는데, 정작 한 줄을 보고 `이 값이 무엇을 대표하는가`를 자연스럽게 설명하기 어렵습니다. 이때는 특징 정의가 나쁜 것일 수도 있지만, 더 자주 있는 원인은 샘플 단위가 아직 맞지 않는다는 점입니다.

| 특징 이름 | 자연스러운 샘플 단위 |
| --- | --- |
| `duration_seconds` | 동작 1회 |
| `late_drop_rate` | 동작 1회 또는 구간 요약 |
| `flow_std` | 동작 1회 또는 최근 구간 |
| `current_flow` | 시점 기록 한 줄 |

즉 특징 이름만 봐도 어떤 샘플 단위와 어울리는지 어느 정도 드러납니다. `duration_seconds`를 시점별 한 줄에 붙여 설명하려 하면 어색한 이유가 바로 여기에 있습니다.

## 라벨이 반복되면 단위를 다시 본다

운영 라벨이 `review_needed`처럼 동작 1회에 붙는 값이라면, 시점별 로그 여러 줄에 같은 라벨이 반복되는 장면은 샘플 단위를 다시 의심해야 하는 대표 신호입니다.

| 보이는 현상 | 더 자연스러운 해석 |
| --- | --- |
| `A`의 세 줄 모두 `review_needed=1` | 사실 라벨은 `A`라는 동작 1회에 붙어 있을 수 있다 |
| `B`의 모든 시점 줄이 같은 상태 값을 가진다 | 시점 줄마다 새 라벨이 있는 것이 아니라 동작 단위 결과를 반복 저장한 것일 수 있다 |

이때 중요한 것은 `라벨 반복이 무조건 틀리다`가 아닙니다. 중요한 것은 `라벨이 실제로 어느 단위에 붙는가`를 다시 묻는 일입니다.

## 비교 문장이 자꾸 어색하면 단위를 다시 본다

샘플 단위가 어긋나면 보고 문장도 이상해집니다. 예를 들어 시점별 한 줄을 보고 `이번 동작은 평소보다 후반 하강이 크다`라고 쓰려 하면, 한 줄만으로는 그 문장이 성립하지 않습니다. 후반 하강은 동작 전체 또는 구간 구조를 본 뒤에야 말할 수 있기 때문입니다.

| 쓰려는 문장 | 먼저 필요한 샘플 단위 |
| --- | --- |
| 이번 동작은 평소보다 더 흔들렸다 | 동작 1회 |
| 최근 상태는 평소보다 더 낮아졌다 | 최근 구간 집계 |
| 이 시점의 센서 값이 높다 | 시점 기록 한 줄 |

즉 문장이 자꾸 `한 줄`보다 큰 대상을 말하고 있다면, 샘플 단위를 다시 의심해야 합니다.

## 작은 코드 예시

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.5, "review_needed": 1},
        {"event_id": "A", "second": 1, "flow": 1.8, "review_needed": 1},
        {"event_id": "A", "second": 2, "flow": 1.1, "review_needed": 1},
        {"event_id": "B", "second": 0, "flow": 0.4, "review_needed": 0},
        {"event_id": "B", "second": 1, "flow": 1.1, "review_needed": 0},
        {"event_id": "B", "second": 2, "flow": 1.0, "review_needed": 0},
    ]
)

label_repetition = raw.groupby("event_id", as_index=False).agg(
    row_count=("second", "count"),
    review_needed_sum=("review_needed", "sum"),
)

event_summary = raw.groupby("event_id", as_index=False).agg(
    duration_seconds=("second", "max"),
    flow_mean=("flow", "mean"),
    review_needed=("review_needed", "max"),
)

warning_check = pd.DataFrame(
    [
        {
            "warning_sign": "same event repeated across many rows",
            "seen_in_output": "yes" if label_repetition["row_count"].max() > 1 else "no",
        },
        {
            "warning_sign": "same label repeated within one event",
            "seen_in_output": "yes" if label_repetition["review_needed_sum"].max() > 1 else "no",
        },
        {
            "warning_sign": "event-level features appear only after regrouping",
            "seen_in_output": "yes" if "duration_seconds" in event_summary.columns else "no",
        },
    ]
)

print("1) row-level table where labels repeat inside one event")
print(raw)
print()
print("2) repeated rows and repeated labels per event")
print(label_repetition)
print()
print("3) event-level summary that appears only after regrouping")
print(event_summary)
print()
print("4) warning signs that sample unit may be wrong")
print(warning_check)
```

예상 출력:

```text
1) row-level table where labels repeat inside one event
  event_id  second  flow  review_needed
0        A       0   0.5              1
1        A       1   1.8              1
2        A       2   1.1              1
3        B       0   0.4              0
4        B       1   1.1              0
5        B       2   1.0              0

2) repeated rows and repeated labels per event
  event_id  row_count  review_needed_sum
0        A          3                  3
1        B          3                  0

3) event-level summary that appears only after regrouping
  event_id  duration_seconds  flow_mean  review_needed
0        A                 2   1.133333              1
1        B                 2   0.833333              0

4) warning signs that sample unit may be wrong
                                  warning_sign seen_in_output
0           same event repeated across many rows            yes
1              same label repeated within one event            yes
2  event-level features appear only after regrouping            yes
```

이 예시의 핵심은 계산 결과가 아니라 `경고 신호가 실제로 어디서 보이는가`입니다. 2단계에서는 같은 `event_id`가 여러 줄 반복되고, `review_needed`가 한 동작 안에서 그대로 복사되어 있다는 점이 드러납니다. 3단계에서는 `duration_seconds`, `flow_mean` 같은 동작 단위 특징이 원시 행에는 없고 재묶은 뒤에야 나타난다는 점이 보입니다. 그래서 4단계의 경고 표는 별도 판단을 새로 만드는 것이 아니라, 앞 출력에서 이미 보인 신호를 다시 묶어 준 것입니다.

## 샘플 단위 오판을 줄이는 짧은 점검 순서

실제로는 아래 네 질문만 다시 적어도 방향이 많이 잡힙니다.

1. 이 라벨은 한 줄에 붙는가, 한 동작에 붙는가
2. 이 특징은 한 줄에서 바로 읽히는가, 여러 줄을 묶어야 생기는가
3. 내가 쓰려는 문장은 한 줄을 말하는가, 한 동작을 말하는가
4. 훈련/평가 분할은 지금 표의 줄을 나누는가, 샘플 단위를 나누는가

이 네 질문 중 두세 개 이상이 어긋나면, 특징을 더 만들기 전에 샘플 단위를 다시 보는 편이 낫습니다.

## 왜 이 절이 Chapter 5 앞에 필요한가

Chapter 5부터는 원시 로그를 요약 표와 집계 표로 다시 묶는 구체적 작업으로 넘어갑니다. 그런데 그 전에 `왜 다시 묶어야 하는가`에 대한 진단 신호가 없으면, 요약 표 만들기가 단순 변형처럼 보일 수 있습니다. 그래서 Chapter 4 마지막에는 샘플 단위를 잘못 잡았을 때 나타나는 징후를 먼저 모아 두는 편이 자연스럽습니다.

즉 이 절은 `샘플 단위의 개념`과 `원시 로그를 다시 묶는 실행` 사이의 경고등 역할을 합니다.

## 짧은 점검

- 같은 라벨이 같은 `event_id`의 여러 줄에 반복되면 왜 샘플 단위를 다시 의심해야 하는가
- 특징을 한 줄에서 자연스럽게 설명할 수 없을 때 왜 샘플 단위가 원인일 수 있는가
- 쓰려는 보고 문장이 한 줄보다 더 큰 대상을 말하고 있으면 무엇을 다시 봐야 하는가
- 이 절이 왜 Chapter 5의 요약 표 설명 앞에 필요한지 설명할 수 있는가

## 언제 이 관점을 먼저 떠올려야 하는가

- 특징, 라벨, 보고 문장이 자꾸 따로 놀 때 샘플 단위 오판 신호부터 점검해야 할 때 이 절을 떠올립니다.
- 시점 기록을 계속 만지는데 동작 전체를 말하는 문장만 쓰고 있을 때 이 절로 돌아옵니다.
- 요약 표를 다시 만드는 일이 왜 필요한지 스스로 설명하기 어려울 때, 먼저 지금 샘플 단위가 잘못 잡힌 신호가 없는지 점검합니다.
