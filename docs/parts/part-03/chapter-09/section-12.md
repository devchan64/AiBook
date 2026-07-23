# P3-9.12 target 이름과 오류 비용

> Section ID: `P3-9.12`
> Version: `v2026.07.23`

_보조제목: 같은 target이라도 놓침과 과검출 중 무엇이 더 아픈지 왜 먼저 적어야 하는가_

같은 target 이름 아래에서도 어떤 실수가 더 아픈지는 문제마다 다를 수 있습니다. `review_needed`를 맞히는 문제라고 해도 위험 사례를 놓치는 것이 더 위험한지, 괜히 검토에 올리는 것이 더 부담스러운지는 운영 맥락에 따라 달라집니다. 같은 target이라도 놓치는 실수와 괜히 잡는 실수의 비용이 다를 수 있으므로, 이 차이를 먼저 적어 두어야 지금 어떤 판단을 더 줄이려는지 분명해집니다.

| 실수 종류 | 운영에서 생길 수 있는 일 |
| --- | --- |
| false negative | 위험 사례를 놓쳐 더 큰 이상으로 번질 수 있다 |
| false positive | 사람이 괜히 시간을 써서 검토 부담이 커질 수 있다 |

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 어떤 실수가 더 아픈가 | 지금 어떤 판단을 더 줄일지 고정하기 위해 |
| 그 비용이 실제 운영에서 어떤 형태로 나타나는가 | 숫자보다 행동 부담으로 설명하기 위해 |
| 지금은 무엇을 더 줄이려는가 | 같은 target이라도 해석 방향을 고정하기 위해 |

## 왜 오류 비용이 target 해석을 바꾸는가

같은 `review_needed` target이라도 모든 예측값을 같은 방식으로 읽는 것은 아닙니다. 어떤 문제에서는 `놓침(false negative)`이 더 아파서 조금 더 많이 검토 큐에 올리더라도 위험 사례를 덜 놓치는 편이 낫고, 어떤 문제에서는 `과검출(false positive)`이 더 아파서 검토 큐를 더 좁게 유지하는 편이 낫습니다. 이때 바뀌는 것은 단순히 threshold 숫자 하나가 아니라, `이 target을 어떤 판단 구조로 해석할 것인가`입니다.

예를 들어 모델 점수가 아래처럼 나왔다고 해 봅시다.

| event_id | score | 해석 1: 놓침 비용이 큼 | 해석 2: 과검출 비용이 큼 |
| --- | --- | --- | --- |
| A | 0.82 | 바로 검토 큐 상단으로 올림 | 검토 큐 상단으로 올림 |
| B | 0.64 | 검토 큐에 포함 | 일단 보류 |
| C | 0.41 | 보조 검토 후보로 남김 | 제외 |

놓침 비용이 큰 문제라면 `B`도 검토 큐에 넣는 편이 더 자연스럽습니다. 반대로 과검출 비용이 큰 문제라면 `B`는 아직 보류하고 `A`만 보는 편이 더 자연스러울 수 있습니다. 즉 같은 점수와 같은 target 이름이 있어도, 오류 비용 구조가 다르면 review queue 우선순위와 threshold 해석도 함께 달라집니다.

## 작은 도식으로 보기

같은 점수라도 어떤 오류를 더 줄이려는지에 따라 검토 큐가 어떻게 갈리는지 아래 순서로 다시 읽을 수 있습니다.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-12-mermaid-01-ko.mmd"
```

그래서 이 절은 `false negative`, `false positive` 정의만 설명하는 절이 아닙니다. 현재 문제를 `무엇을 더 줄이려는 문제인가`로 다시 읽게 만드는 절입니다. target 이름을 먼저 고정했다면, 그다음에는 그 target 아래에서 어떤 실수가 더 아픈지를 적어 두어야 점수, threshold, review queue 우선순위를 같은 방향으로 읽을 수 있습니다.


즉 정확도 하나로 문제를 닫지 않고, 어떤 오류를 더 줄이려는지가 왜 먼저 적혀 있어야 하는지부터 봐야 합니다. 이 절은 `놓침 비용`, `과검출 비용`, `판정 기준 조정`을 함께 묶어, 오류 비용 구조가 목표 해석을 어떻게 바꾸는지 먼저 고정합니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, `ROC curve`. false negative와 false positive의 용어 기준, 실제 임계값 선택에는 오류별 비용 차이가 영향을 줄 수 있다는 설명을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google, *Thresholds and the confusion matrix*. 임계값이 달라지면 true/false positive와 true/false negative 수가 달라지고, 오류 비용이 비대칭이면 단순한 기본 임계값이 적절하지 않을 수 있다는 설명을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
