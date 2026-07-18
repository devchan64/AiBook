# P3-4.4 샘플 단위를 잘못 잡았다는 신호는 무엇인가

> Section ID: `P3-4.4`
> Version: `v2026.07.17`

샘플 단위를 잘못 잡으면 그 문제는 보통 나중 단계에서 이상한 모양으로 다시 드러납니다. `지금 내가 샘플 단위를 잘못 잡고 있다는 사실을 어떻게 알아차릴 수 있는가?`라는 질문이 중요한 이유도 여기에 있습니다. 샘플 단위를 잘못 잡은 채 특징, 라벨, 비교표를 계속 만들다가 뒤늦게 전체 구조가 흔들렸다는 사실을 깨닫는 경우가 많기 때문입니다. 그래서 이 절에서는 샘플 단위 오판을 의심해야 하는 대표 신호를 한 번에 모읍니다.

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

문제 상황: 시점별 표에서 같은 라벨이 반복되고 동작 단위 특징이 따로 나타날 때, 샘플 단위를 잘못 잡았다는 신호를 어떻게 읽는지 확인합니다.

입력(input): `event_id`별 시점 유량과 동작 단위에 붙은 `review_needed`가 반복 저장된 원시 로그 표

기대 출력(output): 반복 라벨, 반복 행 수, 재묶음 뒤에만 생기는 이벤트 요약 특징을 함께 보여 주는 출력

확인할 개념: 라벨 반복과 설명되지 않는 이벤트 수준 특징은 시점 행이 실제 샘플 단위가 아닐 수 있다는 경고 신호다

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

## 샘플 단위를 다시 봐야 할 질문

실제로는 아래 네 질문만 다시 적어도 방향이 많이 잡힙니다.

1. 이 라벨은 한 줄에 붙는가, 한 동작에 붙는가
2. 이 특징은 한 줄에서 바로 읽히는가, 여러 줄을 묶어야 생기는가
3. 내가 쓰려는 문장은 한 줄을 말하는가, 한 동작을 말하는가
4. 훈련/평가 분할은 지금 표의 줄을 나누는가, 샘플 단위를 나누는가

이 네 질문 중 두세 개 이상이 어긋나면, 특징을 더 만들기 전에 샘플 단위를 다시 보는 편이 낫습니다.

## 작은 도식으로 보기

이 절의 경고 신호들은 서로 독립된 체크리스트가 아닙니다. 같은 라벨 반복, 한 줄에서 설명되지 않는 특징, 어색한 비교 문장, 잘못된 분할은 모두 `샘플 단위를 다시 보라`는 같은 방향으로 수렴합니다.

--8<-- "assets/part-03/chapter-04/p3-4-4-mermaid-01-ko.mmd"

이 진단 신호를 먼저 모아 두면, 샘플 단위를 다시 묶어야 하는 상황과 그대로 유지해도 되는 상황을 더 일찍 구분할 수 있습니다. 즉 여기서 중요한 것은 다음 단계를 예고하는 일이 아니라, 현재 표에서 이미 보이는 반복 라벨, 설명되지 않는 특징, 어색한 비교 문장을 통해 샘플 단위 오판을 먼저 알아차리는 일입니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`, `label leakage`. label이 어떤 example 단위에 붙는지와 feature/label 역할 혼동의 위험을 설명하므로, 반복 라벨과 설명되지 않는 특징이 보일 때 샘플 단위를 다시 의심해야 한다는 이 절의 핵심을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. identifying an object와 derivation을 함께 남겨야 한다고 정리하므로, 현재 줄이 시점 기록인지 동작 1회 요약인지 추적 가능해야 샘플 단위 오판을 더 일찍 찾아낼 수 있다는 상위 프레임을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. 변수, 관측치, 표 구조를 구분해 설명하므로, 동작 단위 특징을 시점 행에 억지로 붙이면 왜 해석이 어색해지는지 설명하는 일반 원리를 제공합니다. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
