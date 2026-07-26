# P3-9.6 라벨 일관성 점검

> Section ID: `P3-9.6`
> Version: `v2026.07.25`

_보조제목: 같은 사건도 사람이나 시기에 따라 다른 라벨이 붙을 때 무엇을 먼저 확인해야 하는가_

라벨 후보 열이 생겼다고 해서 곧바로 안정된 학습 문제라고 말할 수는 없습니다. 현실 데이터에서는 같은 사건을 두 검토자가 다르게 적을 수 있고, 지난달에는 "주의"로 보던 상태를 이번 달에는 "정상"으로 기록할 수도 있기 때문입니다. 그래서 [목표 라벨 후보(target candidate)](../../../reference/concept-glossary-parts/05-mieum.md#glossary-target-candidate)를 읽을 때는 "열이 있는가"뿐 아니라 [라벨 일관성(label consistency)](../../../reference/concept-glossary-parts/04-rieul.md#glossary-label-consistency), 즉 "같은 사건과 비슷한 조건에서 같은 뜻의 판단이 반복되는가"도 함께 봐야 합니다.

## 라벨 일관성은 왜 함께 점검해야 하는가

이 질문은 현재 라벨 후보를 바로 목표 라벨(target label)로 올려도 되는지 판단하는 데 필요합니다. 같은 샘플 기준과 결과 열이 잡혀 있어도, 판단 뜻이 반복되지 않으면 안정된 학습 문제로 읽기 어렵기 때문입니다.

| 이미 잡혀 있는 구조 | 여기서 다시 점검해야 하는 이유 |
| --- | --- |
| 샘플 단위 | 같은 샘플 기준인데도 라벨이 흔들릴 수 있기 때문 |
| 목표 라벨 후보 열 | 열이 있어도 붙는 기준이 제각각이면 바로 학습 문제로 올리기 어렵기 때문 |
| 비교 리포트와 검토 큐 | 검토 과정이 라벨 후보로 축적될 때 판단 일관성도 함께 봐야 하기 때문 |

즉 여기서 확인할 것은 `라벨 후보 열이 존재하는가`보다 `그 라벨 후보가 정말 같은 뜻으로 반복되는가`입니다.

## 왜 같은 사건에도 다른 라벨이 붙는가

라벨 후보가 흔들리는 이유는 대체로 아래 몇 가지로 모입니다.

| 흔들리는 이유 | 실제로 생기는 일 |
| --- | --- |
| 검토자마다 기준이 다름 | 같은 패턴을 어떤 사람은 `검토 필요`, 어떤 사람은 `정상`으로 본다 |
| 시기마다 판단 기준이 바뀜 | 예전에는 경고로 보던 패턴이 새 기준에서는 정상 처리된다 |
| 근거 문장이 부족함 | 왜 그렇게 판단했는지 남지 않아 나중에 다시 맞추기 어렵다 |
| 경계 사례가 많음 | 기준선과 아주 비슷한 사례는 사람마다 다르게 붙기 쉽다 |

즉 라벨 후보의 문제는 `틀렸다/맞았다`만이 아니라, `같은 규칙이 반복되고 있는가`의 문제이기도 합니다.

## 비교 표로 먼저 보기

| event_id | diff | repeatability | reviewer | review_label |
| --- | ---: | --- | --- | --- |
| A | -0.34 | high | kim | review_needed |
| A | -0.34 | high | lee | normal |
| B | -0.08 | low | kim | normal |
| B | -0.08 | low | lee | normal |
| C | -0.29 | medium | kim | review_needed |
| C | -0.29 | medium | lee | review_needed |

이 표에서 `A`는 같은 사건인데 `kim`은 `review_needed`, `lee`는 `normal`로 적었습니다. `B`와 `C`는 일치합니다. 이 상태를 보고 종종 `그래도 라벨 열은 있으니 바로 학습 문제로 올리면 되겠네`라고 생각하기 쉽습니다. 하지만 실제로는 `A` 같은 사건이 얼마나 많은지 먼저 봐야 합니다.

핵심은 라벨 후보 열이 있다는 사실보다, `같은 조건에서 같은 판단이 얼마나 반복되는가`입니다.

## 지금 단계에서 무엇을 먼저 적어 두면 좋은가

이 단계에서는 아직 복잡한 통계 지표보다 아래 메모를 먼저 남기면 충분합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 같은 사건의 중복 검토에서 자주 갈리는 라벨이 있는가 | 일관성 낮은 구간을 먼저 보기 위해 |
| 기준이 바뀐 시점이 있는가 | 시기별 라벨 의미 변화 가능성을 적어 두기 위해 |
| 현재 라벨 후보를 바로 target으로 둘지, 비교 리포트 비중을 더 유지할지 | 문제 유형 결정을 보류할 근거를 남기기 위해 |

이 메모는 완벽한 품질 인증이 아니라, `라벨이 흔들릴 수 있다`는 사실을 숨기지 않고 현재 판단 기록에 남기는 일입니다.

## 언제 바로 target으로 올리기 어렵다고 봐야 하는가

아래 같은 장면이 반복되면 목표 라벨 후보를 그대로 결과 열로 두기보다 한 번 더 다듬는 편이 안전합니다.

| 보이는 신호 | 더 자연스러운 다음 행동 |
| --- | --- |
| 같은 사건에 검토자별 라벨이 자주 다르다 | 비교 리포트와 검토 큐를 더 유지한다 |
| 특정 날짜 이후 라벨 기준이 갑자기 바뀐다 | 기간을 나누어 읽거나 기준 변경 메모를 남긴다 |
| 자유 메모는 있는데 공통 판단 열이 약하다 | 검토 메모 정리 규칙을 먼저 보강한다 |
| 경계 사례에서 자주 갈린다 | `확정 라벨`보다 `검토 필요` 수준을 먼저 목표로 둔다 |

즉 불안정한 원인 분류를 억지로 바로 예측 문제로 올리는 것보다, 더 단순하고 반복적인 판단 열부터 목표 후보로 잡는 편이 현재 문제 유형 선택에 더 맞습니다.

이 메모를 남겨 두면 `열이 있다`는 사실보다 `그 열이 같은 뜻으로 반복되는가`를 먼저 점검할 수 있습니다. 그래서 현재 단계에서는 문제 유형을 더 무겁게 올리는 일보다, 뜻이 흔들리는 라벨 후보를 그대로 두지 않는 판단이 더 중요합니다.

## 작은 도식으로 보기

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-6-mermaid-01-ko.mmd"
```

## 작은 코드 예시

문제 상황: 같은 사건을 두 검토자가 다르게 라벨링했을 때, 라벨 후보 열이 있어도 바로 안정된 목표 라벨로 읽기 어렵다는 점을 확인합니다.

입력(input): 중복 검토 기록 [p3_9_6_label_reviews.csv](../../../assets/part-03/chapter-09/p3_9_6_label_reviews.csv). 이 표의 한 행은 한 사건에 대해 특정 검토자가 특정 월에 남긴 라벨 기록입니다. 핵심 열은 `event_id`, `review_month`, `reviewer`, `review_label`입니다.

기대 출력(output): 사건별 검토 수, 라벨 종류 수, 실제 불일치 사건 목록, 월별 라벨 분포를 나란히 보여 주는 출력

확인할 개념: 라벨 후보는 열이 있다는 사실보다 같은 사건과 비슷한 조건에서 같은 뜻의 판단이 반복되는지가 더 중요하다

```python
# 같은 사건에 붙은 여러 검토 라벨의 불일치와 월별 분포를 점검하는 예제입니다.
import pandas as pd

label_variety_threshold = 1
preview_row_count = 8

reviews_path = "docs/assets/part-03/chapter-09/p3_9_6_label_reviews.csv"
reviews = pd.read_csv(reviews_path)

label_variety = reviews.groupby("event_id")["review_label"].nunique()
disagreed_events = label_variety[label_variety > label_variety_threshold]

review_summary = pd.DataFrame(
    {
        "review_count": reviews.groupby("event_id").size(),
        "label_variety": label_variety,
    }
)

monthly_labels = (
    reviews.groupby(["review_month", "review_label"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

disagreement_detail = (
    reviews[reviews["event_id"].isin(disagreed_events.index)]
    .sort_values(["event_id", "review_month", "reviewer"])
    [["event_id", "review_month", "reviewer", "review_label"]]
)

print("1) review record preview:")
print(reviews.head(preview_row_count).to_string(index=False))
print(f"... {len(reviews) - preview_row_count} more review records")
print()
print("2) reviews per event:")
print(review_summary)
print()
print("3) label variety by event:")
print(label_variety)
print()
print("4) events with disagreement:")
print(disagreed_events.index.tolist())
print()
print("5) disagreement detail:")
print(disagreement_detail.head(12).to_string(index=False))
print(f"... {len(disagreement_detail) - 12} more disagreement records")
print()
print("6) labels by review month:")
print(monthly_labels.to_string(index=False))
```

예상 출력:

```text
1) review record preview:
event_id review_month reviewer  diff repeatability  review_label
       A      2026-04      kim -0.34          high review_needed
       A      2026-04      lee -0.34          high        normal
       A      2026-05     park -0.34          high review_needed
       B      2026-04      kim -0.08           low        normal
       B      2026-04      lee -0.08           low        normal
       B      2026-05     park -0.08           low        normal
       C      2026-04      kim -0.29        medium review_needed
       C      2026-04      lee -0.29        medium review_needed
... 28 more review records

2) reviews per event:
          review_count  label_variety
event_id                             
A                    3              2
B                    3              1
C                    3              1
D                    3              2
E                    3              1
F                    3              2
G                    3              2
H                    3              1
I                    3              2
J                    3              1
K                    3              1
L                    3              2

3) label variety by event:
event_id
A    2
B    1
C    1
D    2
E    1
F    2
G    2
H    1
I    2
J    1
K    1
L    2
Name: review_label, dtype: int64

4) events with disagreement:
['A', 'D', 'F', 'G', 'I', 'L']

5) disagreement detail:
event_id review_month reviewer  review_label
       A      2026-04      kim review_needed
       A      2026-04      lee        normal
       A      2026-05     park review_needed
       D      2026-04      kim        normal
       D      2026-04      lee        normal
       D      2026-05     park review_needed
       F      2026-04      kim        normal
       F      2026-04      lee review_needed
       F      2026-05     park        normal
       G      2026-04      kim review_needed
       G      2026-04      lee        normal
       G      2026-05     park        normal
... 6 more disagreement records

6) labels by review month:
review_month  normal  review_needed
     2026-04      12             12
     2026-05       6              6
```

이 예제의 목적은 모델 입력을 만드는 것이 아니라, `같은 사건에 대해 검토가 몇 번 있었고 그중 어디서 라벨이 갈렸는가`를 먼저 확인하는 데 있습니다. 먼저 사건별 검토 수를 보고, 그다음 라벨 종류 수를 세고, 실제 불일치 사건 목록과 상세 기록을 확인하면 왜 이 절에서 `라벨 열이 있다`보다 `라벨 의미가 반복되는가`를 먼저 보라고 하는지 더 분명해집니다. 출력에서는 12개 사건 중 `A`, `D`, `F`, `G`, `I`, `L`처럼 라벨 종류가 2개로 갈린 사건이 따로 드러납니다. 월별 라벨 분포를 함께 보면 시기별 기준 변화 가능성도 메모할 수 있습니다. 여기서 중요한 것은 특정 팀의 메모 습관이 아니라, `라벨 의미 안정성(label meaning stability)`을 확인하는 일입니다. 목표 라벨 후보를 읽을 때는 현재 라벨 후보가 같은 뜻으로 비교적 반복되는가, 기준이 바뀐 시점을 메모할 수 있는가, 그리고 불안정한 라벨을 바로 결과 열로 두지 않고 있는가를 함께 봐야 합니다. 이런 점검이 있어야 목표 라벨 후보 표는 단순한 열 목록이 아니라, `라벨 의미의 안정성`까지 포함한 구조가 됩니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `rater`, `inter-rater agreement`, `label`. 사람이 예제에 라벨을 제공하는 rater 역할과, 여러 rater의 판단 일치 여부를 보는 inter-rater agreement 관점을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, provenance and activity context overview. 라벨 후보가 어떤 검토자와 시기, 활동 맥락에서 생겼는지 추적해야 한다는 provenance 관점을 확인하는 데 참고했습니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
