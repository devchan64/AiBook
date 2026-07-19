# P3-5.6 겹치는 입력 창이 많을 때 왜 샘플 수가 실제보다 커 보일 수 있는가

> Section ID: `P3-5.6`
> Version: `v2026.07.19`

입력 창(window)을 정하고 나면 같은 원천 시계열에서 여러 창을 만들 수 있습니다. 이때 자주 놓치는 문제가 있습니다. `창이 많아졌으니 샘플도 그만큼 늘었다`고 읽기 쉽다는 점입니다. 하지만 겹치는 창이 많아졌다는 것은 종종 `같은 사건을 여러 번 잘라 본다`는 뜻이지, 독립된 사건 수가 그만큼 늘었다는 뜻은 아닙니다.

입력 창 수와 원천 사건 수는 같은 숫자가 아닐 수 있습니다.

| 구분 | 뜻 |
| --- | --- |
| 원천 사건 수 | 실제로 있었던 동작 1회, 사건 1건의 수 |
| 입력 창 수 | 그 사건들에서 잘라 낸 학습 입력 조각 수 |

예를 들어 동작 1건에서 길이 30, stride 10으로 창을 자르면 하나의 사건이 여러 입력으로 늘어날 수 있습니다.

| event_id | 원천 길이 | 창 길이 | stride | 만들어진 창 수 |
| --- | ---: | ---: | ---: | ---: |
| A | 100 | 30 | 10 | 8 |
| B | 100 | 30 | 10 | 8 |

이 표를 보고 `샘플이 16건 있다`고만 말하면 절반만 맞습니다. 실제 사건은 2건이고, 입력 창은 16개입니다. 따라서 비교 리포트나 대표성 판단에서는 여전히 `2건의 사건`이라는 사실을 같이 적어야 합니다.

겹치는 창이 많을수록 아래 문제가 생기기 쉽습니다.

| 생기는 문제 | 왜 주의해야 하는가 |
| --- | --- |
| 샘플 수가 커 보인다 | 실제 사건 수보다 근거가 과장돼 보일 수 있다 |
| 비슷한 창이 반복된다 | 같은 사건의 패턴이 여러 번 나타나 독립성이 약해질 수 있다 |
| 최근 사건이 더 많이 잘린다 | 특정 사건의 영향이 표에서 과하게 커질 수 있다 |

지금 단계에서는 복잡한 평가 설계를 다루지 않아도 됩니다. 다만 아래 메모는 남겨 두는 편이 안전합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 원천 사건 수 | 실제 근거 단위를 숨기지 않기 위해 |
| 입력 창 수 | 모델 입력 규모를 따로 보기 위해 |
| 창 길이와 stride | 어떤 규칙으로 창이 늘어났는지 다시 설명하기 위해 |

작은 예시를 보면 더 분명합니다.

문제 상황: 겹치는 입력 창이 많아졌을 때 창 수와 원천 사건 수를 같은 숫자로 읽으면 어떤 착시가 생기는지 확인합니다.

입력(input): 사건 길이와 `window`, `stride`가 주어진 원천 사건 표

기대 출력(output): 각 사건이 몇 개 창으로 늘어나는지와 `source_event` 대비 `window` 수가 얼마나 커지는지 보여 주는 출력

확인할 개념: 입력 창 수는 파생 조각 수일 뿐이며 원천 사건 수와 같은 단위로 읽으면 안 된다

```python
import pandas as pd

events = pd.DataFrame(
    [
        {"event_id": "A", "length": 100, "window": 30, "stride": 10},
        {"event_id": "B", "length": 100, "window": 30, "stride": 10},
    ]
)

events["window_count"] = ((events["length"] - events["window"]) // events["stride"]) + 1
events["source_event_weight"] = 1

print("1) how many windows each source event creates")
print(events[["event_id", "length", "window", "stride", "window_count"]])
print()
print("2) source-event count vs window count")
print(
    pd.DataFrame(
        [
            {"unit": "source_event", "count": events["source_event_weight"].sum()},
            {"unit": "window", "count": events["window_count"].sum()},
        ]
    )
)
print()
print("3) expansion per source event")
print(events[["event_id", "window_count"]])
```

예상 출력:

```text
1) how many windows each source event creates
  event_id  length  window  stride  window_count
0        A     100      30      10             8
1        B     100      30      10             8

2) source-event count vs window count
          unit  count
0  source_event      2
1        window     16

3) expansion per source event
  event_id  window_count
0        A             8
1        B             8
```

이 예제의 목적은 창 수를 계산하는 것보다 `창 수가 실제 사건 수를 얼마나 부풀려 보이게 하는가`를 확인하는 데 있습니다. 그래서 1단계에서는 사건 하나가 몇 개 창으로 늘어나는지 보고, 2단계에서는 `source_event`와 `window`를 따로 세고, 3단계에서는 각 사건의 확장 정도를 다시 확인합니다. 여기서 중요한 점은 `겹치는 입력 창은 같은 사건을 여러 번 잘라 본 결과일 수 있으므로, 창 수를 곧바로 사건 수처럼 읽으면 안 된다`는 사실입니다.

## 작은 도식으로 보기

이 절의 핵심은 `창 수가 커진다`와 `원천 사건 수가 늘었다`를 분리하는 데 있습니다. 같은 두 사건에서 겹치는 창을 많이 만들면 입력 조각 수는 커지지만, 사건 수 자체는 그대로 남습니다.

--8<-- "assets/part-03/chapter-05/p3-5-6-mermaid-01-ko.mmd"

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example는 features와 label이 붙는 단위를 전제로 하므로, 여러 입력 창이 생겼다고 해서 원천 사건 수 자체가 자동으로 늘어났다고 읽으면 안 된다는 이 절의 판단을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. provenance framework가 어떤 entity가 어떤 derivation을 거쳐 생성되었는지 추적해야 한다고 정리하므로, 각 입력 창이 어떤 원천 사건에서 파생되었는지 분리해 남겨야 창 수와 사건 수를 혼동하지 않는다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Datasets: Dividing the original dataset`. 학습용 표본이 어떤 원천 데이터에서 어떤 규칙으로 만들어졌는지 구분해야 한다는 일반 관점을 제공하므로, 겹치는 창이 많을 때도 원천 사건 단위와 입력 조각 단위를 따로 적어야 한다는 이 절의 설명을 일반화하는 데 참고할 수 있습니다. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. 같은 원천 과정에서 나온 의존 샘플은 독립동일분포 가정이 깨질 수 있고, grouped data에서는 같은 그룹의 샘플이 훈련 fold와 검증 fold에 함께 나타나지 않게 해야 한다고 설명하므로, 겹치는 입력 창이 실제 사건 수를 늘린 것이 아니라 같은 사건에서 파생된 의존 조각일 수 있다는 이 절의 주의를 보강합니다. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
