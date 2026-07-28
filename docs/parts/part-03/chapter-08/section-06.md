# P3-8.6 일부 사례에만 남은 확정 라벨

> Section ID: `P3-8.6`
> Version: `v2026.07.25`

_보조제목: 확정 라벨이 검토된 사례에만 있을 때 해석에 무엇을 함께 적어야 하는가_

해석 단계에서는 숫자 차이뿐 아니라 누가 확정 [지도학습 라벨(supervised learning label)](../../../reference/concept-glossary-parts/04-rieul.md#glossary-label)을 얻었는가도 함께 봐야 할 때가 있습니다. 현실 운영에서는 모든 사건에 같은 깊이의 검토가 들어가지 않습니다. 이상해 보인 일부 사례만 사람이 다시 보고, 그 사례에만 확정 라벨이 남을 수 있습니다. 이 [선택적 라벨(selective labels)](../../../reference/concept-glossary-parts/07-siot.md#glossary-selective-labels) 상태를 숨기면 독자는 `라벨이 있는 사례 집합`을 `전체 사건 집합`처럼 읽기 쉽습니다.

확정 라벨이 검토된 사례에만 남아 있다면, 그 라벨은 전체를 대표한다고 바로 읽으면 안 됩니다.

| 보이는 상태 | 해석에서 함께 적어야 하는 것 |
| --- | --- |
| 일부 사례에만 확정 라벨이 있다 | 어떤 기준으로 그 사례들만 검토됐는가 |
| `review_needed=0` 사례는 거의 재확인되지 않았다 | 라벨 없음이 정상인지 미확인인지 |
| 특정 기간·장비에만 라벨이 몰린다 | 라벨 집합의 [편향(bias)](../../../reference/concept-glossary-parts/13-pieup.md#glossary-bias) 가능성 |

예를 들어 아래 표를 보겠습니다.

| event_id | review_needed | manually_reviewed | confirmed_root_cause |
| --- | ---: | ---: | --- |
| A | 1 | 1 | sensor_drop |
| B | 1 | 1 | valve_delay |
| C | 0 | 0 | None |
| D | 0 | 0 | None |

이때 `confirmed_root_cause`가 있는 두 건만 보고 전체 운영의 원인 분포를 말하면 과장될 수 있습니다. 왜 A와 B만 사람이 봤는지, C와 D는 정말 정상이라 비었는지, 아니면 단지 아직 안 봤는지를 같이 적어야 합니다.

해석 단계에서는 아래 메모면 충분합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 검토 대상이 되는 기준 | 선택적으로 라벨이 남는 구조를 드러내기 위해 |
| 라벨 없음의 뜻 | 정상과 미확인을 섞지 않기 위해 |
| 라벨 있는 집합의 범위 편중 | 해석 강도를 과장하지 않기 위해 |

여기서 중요한 점은 `선택적으로 붙은 확정 라벨은 해석 근거가 될 수는 있지만, 전체 사건을 대표하는 정답 집합처럼 읽기 전에 검토 경로와 편중을 먼저 적어야 한다`는 사실입니다. 따라서 확정 라벨 표는 `전체 사건의 정답표`가 아니라, [검토 후보 큐(review queue)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-review-queue) 같은 검토 경로를 거친 일부 사건의 확인 결과일 수 있다는 점을 먼저 봐야 합니다.

아래 예제는 이 문제를 작은 모델 평가로 축소해 봅니다. 실제 운영에서는 검토되지 않은 사건의 최종 결과를 모를 수 있습니다. 그래서 코드의 `actual_failure_for_demo`는 학습용으로만 둔 숨은 결과입니다. 목적은 이 값을 정답표처럼 쓰는 것이 아니라, 검토된 사례에만 남은 라벨로 모델을 평가하면 어떤 착시가 생기는지 확인하는 데 있습니다.

문제 상황: 검토된 사례에만 확정 라벨이 있을 때, 모델 점수가 검토 경로에 따라 어떻게 달라져 보이는지 확인합니다.

입력(input): `risk_score`, `manually_reviewed`, 데모용 숨은 결과 `actual_failure_for_demo`.

기대 출력(output): 라벨 coverage, 검토된 라벨에서의 정확도, 전체 사건을 데모로 열어 봤을 때의 정확도와 검토 경로별 오류 수.

확인할 개념: 선택적으로 검토된 라벨만 보면 모델이 좋아 보일 수 있지만, 검토되지 않은 구간에서는 오류가 숨어 있을 수 있습니다.

```python
# 선택적으로 검토된 라벨만 사용할 때 평가가 어떻게 치우칠 수 있는지 확인합니다.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

events = pd.DataFrame(
    [
        {"event_id": "A", "risk_score": 0.92, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "B", "risk_score": 0.88, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "C", "risk_score": 0.81, "manually_reviewed": 1, "actual_failure_for_demo": 0},
        {"event_id": "D", "risk_score": 0.76, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "E", "risk_score": 0.69, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "F", "risk_score": 0.62, "manually_reviewed": 0, "actual_failure_for_demo": 0},
        {"event_id": "G", "risk_score": 0.55, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "H", "risk_score": 0.48, "manually_reviewed": 0, "actual_failure_for_demo": 0},
        {"event_id": "I", "risk_score": 0.37, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "J", "risk_score": 0.29, "manually_reviewed": 0, "actual_failure_for_demo": 0},
    ]
)

reviewed = events[events["manually_reviewed"].eq(1)]

model = DecisionTreeClassifier(random_state=0, max_depth=2)
model.fit(reviewed[["risk_score"]], reviewed["actual_failure_for_demo"])
events["predicted_from_reviewed_only"] = model.predict(events[["risk_score"]])
events["error"] = events["predicted_from_reviewed_only"].ne(events["actual_failure_for_demo"])

print("label coverage")
print(events.groupby("manually_reviewed")["event_id"].count().to_dict())
print("failure rate in reviewed labels:", reviewed["actual_failure_for_demo"].mean())
print("failure rate in all events for demo:", events["actual_failure_for_demo"].mean())
print(
    "accuracy on reviewed labels:",
    accuracy_score(reviewed["actual_failure_for_demo"], model.predict(reviewed[["risk_score"]])),
)
print(
    "accuracy on all events for demo:",
    accuracy_score(events["actual_failure_for_demo"], events["predicted_from_reviewed_only"]),
)
print("errors by review path:", events.groupby("manually_reviewed")["error"].sum().to_dict())
print(
    events[
        [
            "event_id",
            "manually_reviewed",
            "actual_failure_for_demo",
            "predicted_from_reviewed_only",
            "error",
        ]
    ].to_string(index=False)
)
```

예상 출력:

```text
label coverage
{0: 6, 1: 4}
failure rate in reviewed labels: 0.75
failure rate in all events for demo: 0.6
accuracy on reviewed labels: 1.0
accuracy on all events for demo: 0.7
errors by review path: {0: 3, 1: 0}
event_id  manually_reviewed  actual_failure_for_demo  predicted_from_reviewed_only  error
       A                  1                        1                             1  False
       B                  1                        1                             1  False
       C                  1                        0                             0  False
       D                  1                        1                             1  False
       E                  0                        1                             1  False
       F                  0                        0                             1   True
       G                  0                        1                             1  False
       H                  0                        0                             1   True
       I                  0                        1                             1  False
       J                  0                        0                             1   True
```

검토된 라벨만 보면 정확도가 `1.0`입니다. 하지만 데모용으로 전체 사건의 실제 결과를 열어 보면 정확도는 `0.7`로 내려가고, 오류 3건은 모두 `manually_reviewed=0` 경로에 있습니다. 이 출력은 확정 라벨이 붙은 사례가 전체 사건을 대표하지 않을 수 있음을 보여 줍니다. 실제 운영에서는 검토되지 않은 사건의 결과를 모를 수 있으므로, 더더욱 `라벨 없음은 정상인가, 미확인인가`, `어떤 기준으로 사람이 검토했는가`를 함께 남겨야 합니다.

## 작은 도식으로 보기

이 절의 핵심은 `검토된 사례에만 남은 확정 라벨`을 전체 사건의 정답표처럼 읽지 않는 데 있습니다. 확정 라벨이 보이면, 그와 함께 `라벨 없음의 뜻`, `검토 경로`, `편중 가능성`을 같이 적어야 해석 강도가 과장되지 않습니다.

--8<-- "assets/part-03/chapter-08/p3-8-6-mermaid-01-ko.mmd"

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. label은 각 example에 붙은 결과 정보라는 기본 틀을 제공하므로, 일부 사례에만 확정 라벨이 남아 있다면 그 라벨 집합이 전체 사건 집합과 같은 범위를 대표하지 않을 수 있다는 이 절의 설명을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Himabindu Lakkaraju, Jon Kleinberg, Jure Leskovec, Jens Ludwig, Sendhil Mullainathan, `The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables`, KDD 2017. 관측된 결과가 기존 의사결정자의 선택 결과로만 남는 selectively labeled data에서는 관측된 outcome이 전체 모집단의 무작위 표본이 아니어서 잘못된 결론으로 이어질 수 있다고 설명하므로, 확정 라벨이 검토된 사례에만 남아 있을 때 그 라벨 집합을 전체 사건의 정답표처럼 읽으면 안 된다는 이 절의 핵심 근거가 됩니다. [https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres](https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. 어떤 결과가 어떤 검토 절차를 거쳐 생성되었는지를 provenance information으로 남기는 관점을 제공하므로, 확정 라벨이 붙은 사례 집합에서는 검토 경로와 라벨 없음의 뜻을 함께 적어야 한다는 이 절의 일반 근거가 됩니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
