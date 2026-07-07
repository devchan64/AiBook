# P3-2.3 새 표를 처음 받으면 무엇부터 적어야 하는가

> Section ID: `P3-2.3`
> Version: `v2026.07.07`

Chapter 2 앞 절을 읽고 나면 원칙은 이해됩니다. 저장 구조와 문제 표현 구조는 다르고, 저장된 기록은 아직 데이터셋 후보일 뿐일 수 있습니다. 그런데 실제 작업으로 들어가면 다시 막히는 지점이 있습니다. `그러면 새 표를 처음 받았을 때 무엇부터 확인해야 하는가?` 이 질문 앞에서는 다시 모델 이름이나 특징 후보부터 떠올리기 쉽습니다. 그래서 이 절에서는 표를 처음 읽을 때 상위 원리를 놓치지 않도록, 작업용 관찰 메모의 축을 하나 정해 둡니다.

새 표를 보자마자 `학습용 데이터셋인가`를 먼저 결정하기보다, 먼저 `이 표의 한 행은 무엇이고, 무엇을 묶을 수 있으며, 무엇이 아직 빠져 있는가`를 메모해 두는 편이 해석에 도움이 됩니다. 이 세 가지가 정리되면 뒤의 샘플 설계와 데이터셋 재설계도 훨씬 덜 추상적으로 바뀝니다.

이 작업용 메모는 아무 표에나 붙는 독립 방법론이 아니라 몇 가지 더 넓은 원리를 실무 쪽으로 줄인 것입니다. `한 행은 무엇인가`라는 질문은 통계와 데이터 정리에서 말하는 `observation` 단위 확인과 이어지고, `무엇을 묶을 수 있는가`는 시간 데이터에서 `key`와 `index`를 먼저 드러내야 한다는 원리와 이어집니다. `원시 근거`를 남겨 두는 항목도 데이터 provenance와 traceability를 확보해야 나중에 품질과 신뢰성을 다시 판단할 수 있다는 원리에서 나왔습니다. Part 3의 다섯 줄 메모는 이런 상위 프레임을 표를 처음 읽을 때 바로 써먹을 수 있게 줄여 둔 형태입니다.

## 가장 먼저 적는 다섯 가지

이 절에서는 아래 다섯 가지를 `새 표를 처음 읽을 때 빠르게 확인하는 작업용 메모`로 사용합니다. 이것이 어떤 표준 방법론의 고정 절차를 뜻하는 것은 아니고, `행 단위`, `묶음 기준`, `시간 구조`, `비교 가능성`, `원시 근거`라는 상위 질문을 놓치지 않기 위한 축약형입니다.

1. 한 행은 무엇을 뜻하는가
2. 같은 대상을 묶어 주는 식별자는 무엇인가
3. 시간 순서나 진행 순서를 나타내는 열이 있는가
4. 지금 바로 비교 가능한 단위인가, 다시 묶어야 하는가
5. 이상해 보이면 다시 돌아갈 원시 근거는 무엇인가

이 다섯 가지를 표로 줄이면 다음과 같습니다.

| 먼저 적을 항목 | 왜 필요한가 |
| --- | --- |
| 행 의미 | 시점 기록인지, 동작 1회인지, 최근 구간 집계인지 구분해야 하기 때문 |
| 식별자 | 여러 줄이 같은 샘플에 속하는지 묶어 볼 수 있어야 하기 때문 |
| 시간/순서 열 | 시계열 구조인지, 정적 표인지 판단해야 하기 때문 |
| 비교 가능성 | 지금 바로 샘플 비교가 가능한지, 요약 표가 먼저 필요한지 결정해야 하기 때문 |
| 원시 근거 위치 | 나중에 이상 사례를 다시 추적할 수 있어야 하기 때문 |

이 항목들은 복잡한 데이터 프로파일링 절차를 대신하자는 뜻이 아닙니다. Part 3 입구에서는 이 다섯 축만 먼저 적어도 저장 구조와 문제 표현 구조를 훨씬 덜 섞어 읽게 됩니다.

## 잘못된 시작과 더 나은 시작

| 표를 보자마자 하기 쉬운 일 | 왜 너무 빠른가 | 더 나은 첫 행동 |
| --- | --- | --- |
| 평균, 최대값부터 계산해 본다 | 아직 한 행과 샘플 단위가 다를 수 있다 | 행 의미와 식별자부터 적는다 |
| 분류/회귀 문제를 떠올린다 | 라벨이 붙는 단위가 아직 안 보일 수 있다 | 비교 가능한 단위인지 먼저 본다 |
| 시계열 딥러닝을 생각한다 | 시간 열이 있어도 샘플 경계는 아직 안 정해졌을 수 있다 | 시간/순서 열과 묶음 기준을 먼저 본다 |
| 이상한 값 한 줄에 바로 의미를 붙인다 | 그 한 줄이 샘플 전체를 대표하지 않을 수 있다 | 원시 근거와 요약 후보 구조를 함께 적는다 |

즉 첫 단계는 `계산`보다 `정체 확인`에 가깝습니다.

## 아주 짧은 표 읽기 메모

여기서는 아래처럼 다섯 줄 메모 형식으로 바로 적어 두면 앞 절의 상위 원리를 실제 표 읽기로 옮기기 쉽습니다.

- 한 행은 `_____`를 뜻한다.
- 같은 대상을 묶는 키는 `_____`다.
- 시간/진행 순서를 나타내는 열은 `_____`다.
- 지금 표는 바로 비교 가능하다 / 아직 다시 묶어야 한다.
- 이상 사례를 다시 확인할 원시 근거는 `_____`다.

예를 들어 자동 동작 로그라면 이렇게 적을 수 있습니다.

- 한 행은 `동작 중 한 시점의 측정값`을 뜻한다.
- 같은 대상을 묶는 키는 `event_id`다.
- 시간 열은 `elapsed_seconds`다.
- 지금 표는 바로 비교 가능한 샘플 표가 아니라 다시 묶어야 한다.
- 이상 사례를 다시 확인할 원시 근거는 `event_id`별 원시 로그다.

이 다섯 줄 메모가 있으면 Chapter 3에서 `질문에 맞는 데이터셋을 다시 설계한다`는 말도 훨씬 덜 추상적으로 읽힙니다.

## 작은 예시로 보기

문제 상황: 새 로그 표를 받았을 때, 이 표를 바로 샘플 비교 표로 읽어도 되는지 확인합니다.

입력(input): `event_id`별 여러 시점 기록이 섞여 있는 원시 로그 표

기대 출력(output): 같은 표라도 `행 의미`, `묶음 기준`, `시간/순서 열`을 먼저 확인해야 아직 바로 비교할 수 없는 표라는 점이 드러납니다.

확인할 개념: 표를 처음 읽을 때는 계산보다 먼저 `이 행이 샘플 1건인가, 아니면 샘플의 일부 기록인가`를 확인해야 한다

```python
import pandas as pd

table = pd.DataFrame(
    [
        {"event_id": "A", "elapsed_seconds": 0, "flow": 0.8, "pressure": 1.0},
        {"event_id": "A", "elapsed_seconds": 1, "flow": 1.5, "pressure": 2.0},
        {"event_id": "A", "elapsed_seconds": 2, "flow": 0.9, "pressure": 1.4},
        {"event_id": "B", "elapsed_seconds": 0, "flow": 0.7, "pressure": 1.1},
        {"event_id": "B", "elapsed_seconds": 1, "flow": 0.8, "pressure": 1.2},
    ]
)

print("1) raw table")
print(table)
print()

row_check = pd.DataFrame(
    [
        {"check_item": "row_count", "value": len(table)},
        {"check_item": "event_id_count", "value": table["event_id"].nunique()},
        {"check_item": "has_time_order", "value": "yes"},
    ]
)
print("2) quick structural check")
print(row_check)
print()

rows_per_event = table.groupby("event_id", as_index=False).size().rename(columns={"size": "row_count"})
print("3) repeated rows per event")
print(rows_per_event)
print()

wrong_reading = table[["event_id", "elapsed_seconds", "flow"]]
print("4) if we compare rows as if each row were a sample")
print(wrong_reading)
print()

event_summary = (
    table.groupby("event_id", as_index=False)
    .agg(
        duration_seconds=("elapsed_seconds", "max"),
        mean_flow=("flow", "mean"),
        peak_pressure=("pressure", "max"),
    )
)
print("5) after regrouping into one row per event")
print(event_summary)
```

예상 출력:

```text
1) raw table
  event_id  elapsed_seconds  flow  pressure
0        A                0   0.8       1.0
1        A                1   1.5       2.0
2        A                2   0.9       1.4
3        B                0   0.7       1.1
4        B                1   0.8       1.2

2) quick structural check
      check_item  value
0      row_count      5
1  event_id_count      2
2  has_time_order    yes

3) repeated rows per event
  event_id  row_count
0        A          3
1        B          2

4) if we compare rows as if each row were a sample
  event_id  elapsed_seconds  flow
0        A                0   0.8
1        A                1   1.5
2        A                2   0.9
3        B                0   0.7
4        B                1   0.8

5) after regrouping into one row per event
  event_id  duration_seconds  mean_flow  peak_pressure
0        A                 2   1.066667            2.0
1        B                 1   0.750000            1.2
```

이 예시가 보여 주는 핵심은 단순히 `event_id`와 `elapsed_seconds`라는 열 이름을 찾는 일이 아닙니다. 2단계와 3단계에서 먼저 보이는 것은 `행 수 5`보다 `event_id 수 2`가 작고, 같은 `event_id`가 여러 줄 반복된다는 사실입니다. 이 신호를 읽어야만 `현재 한 행은 샘플 1건이 아니라 샘플의 일부 기록`이라는 해석에 도달할 수 있습니다. 그래서 4단계처럼 각 행을 바로 비교하면 아직 `A 동작 전체`와 `B 동작 전체`를 비교하는 표가 되지 못합니다. 반대로 5단계처럼 `event_id`로 다시 묶어야 비로소 동작 1회가 한 행이 되고, 그 위에서 평균 흐름이나 최대 압력 같은 비교 가능한 열을 만들 수 있습니다.

## 이 절이 왜 Chapter 3 앞에 필요한가

Chapter 3에서는 모델 이름을 늦추고 질문에 맞는 데이터셋을 다시 설계하는 법을 다룹니다. 그런데 그 전에 표를 읽는 최소 메모 축이 없으면, `질문에 맞게 다시 설계한다`는 말도 여전히 추상적으로 남습니다. 그래서 Chapter 2 마지막에는 새 표를 받을 때 바로 적용할 수 있는 작업용 점검 메모를 하나 두는 편이 더 자연스럽습니다.

즉 이 절은 `저장 구조와 문제 표현 구조를 구분하는 개념`과 `질문에 맞게 데이터셋을 다시 만든다는 실행` 사이의 짧은 브리지입니다.

## 짧은 점검

- 왜 새 표를 보자마자 특징 계산이나 모델 선택으로 들어가면 너무 빠른지 설명할 수 있는가
- 행 의미, 식별자, 시간/순서 열을 먼저 적는 이유를 말할 수 있는가
- 지금 표가 바로 비교 가능한 샘플 표인지, 다시 묶어야 하는 표인지 어떻게 판별하는지 설명할 수 있는가
- 이 절의 다섯 줄 메모가 왜 Chapter 3의 데이터셋 재설계로 이어지는지 말할 수 있는가

## 언제 이 관점을 먼저 떠올려야 하는가

- 새 CSV나 로그 표를 처음 받았을 때 무엇부터 봐야 할지 막히면 이 절의 다섯 가지 점검 항목을 먼저 떠올립니다.
- 평균, 최대값, 모델 이름부터 바로 떠오를 때 한 행의 뜻과 묶음 기준을 먼저 적어야 한다는 점을 다시 확인합니다.
- 저장 구조와 문제 표현 구조를 실무에서 어떻게 구분해 읽기 시작해야 하는지 헷갈릴 때 이 절로 돌아옵니다.

## 출처와 참고 자료

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* (2014). `each observation is a row`라는 tidy data 원리를 통해 `한 행이 무엇 1건인가`를 먼저 확인해야 하는 근거를 제공합니다. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-07
- Google for Developers, `Machine Learning Glossary`의 `feature`, `example` 항목. 머신러닝에서 example이 feature들로 구성되는 단위라는 점을 설명하므로, 원시 표의 한 행이 곧바로 모델 입력 단위인지 먼저 구분해야 한다는 근거로 읽을 수 있습니다. [https://developers.google.com/machine-learning/glossary/](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-07
- Earo Wang, Dianne Cook, Rob J Hyndman, `A new tidy data structure to support exploration and modeling of temporal data` (2019). 시간 데이터에서는 명시적인 시간 index와 개체를 구분하는 key가 필요하다고 설명하므로, `묶음 기준`과 `시간/순서 열`을 먼저 보는 근거가 됩니다. [https://arxiv.org/abs/1901.10257](https://arxiv.org/abs/1901.10257){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-07
- W3C, `PROV-Overview` (2013). provenance를 데이터가 어떻게 만들어졌는지에 관한 정보로 설명하며, 품질과 신뢰성 판단에 쓰인다고 정리합니다. 이는 `이상 사례를 다시 확인할 원시 근거`를 남겨 두어야 한다는 항목의 상위 근거입니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-07
