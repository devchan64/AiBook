# P3-9.8 예측 1회는 실제로 무엇을 결정하며 점수와 정책은 왜 다른가

> Section ID: `P3-9.8`
> Version: `v2026.07.25`

입력과 결과를 정한 뒤에도 예측 문제는 아직 반쯤만 닫힌 상태입니다. 같은 `review_needed` 예측이라도 그것이 동작 1건을 [검토 후보 큐(review queue)](/AiBook/reference/concept-glossary-parts/05-mieum.md#glossary-output-structure)에 올리는 일인지, 최근 구간 전체의 경고 강도를 조정하는 일인지가 다를 수 있기 때문입니다. 또한 모델이 낸 [점수(score)](/AiBook/reference/concept-glossary-parts/05-mieum.md#glossary-score)와 그 점수로 실제 행동을 정하는 [정책 규칙(policy rule)](/AiBook/reference/concept-glossary-parts/08-ieung.md#decision)도 같은 것이 아닙니다.

예측값 하나는 어떤 단위의 어떤 행동과 연결되는지 적어야 하고, 모델 점수와 판단 규칙은 분리해서 봐야 합니다.

| 구분 | 질문 |
| --- | --- |
| 예측 1회의 대상 단위 | 이 값 하나는 동작 1건, 최근 구간 1개, 다음 사례 1건 중 무엇을 가리키는가 |
| 모델 출력 | 모델은 점수, 0/1, 순위 중 무엇을 내는가 |
| [정책 규칙(policy rule)](/AiBook/reference/concept-glossary-parts/08-ieung.md#decision) | 그 출력을 어떤 기준으로 행동으로 바꾸는가 |
| [실제 행동(action)](/AiBook/reference/concept-glossary-parts/14-hieut.md#action) | 검토 큐 등록, 보류, 자동 조치 중 무엇이 일어나는가 |

| 층위 | 예시 |
| --- | --- |
| 모델 출력 | `0.82`, `warning_score` |
| [정책 규칙(policy rule)](/AiBook/reference/concept-glossary-parts/08-ieung.md#decision) | `0.8 이상이면 검토`, `상위 10%만 본다` |
| 실제 행동 | 검토 큐 등록, 우선순위 조정 |

같은 점수라도 정책이 다르면 행동이 달라질 수 있습니다. 또한 어떤 문제는 점수를 [순위화(ranking)](/AiBook/reference/concept-glossary-parts/07-siot.md#glossary-ranking)에만 쓰고, 어떤 문제는 숫자 자체를 [확률 추정값(probability estimate)](/AiBook/reference/concept-glossary-parts/14-hieut.md#probability-estimate)처럼 읽고 싶어 할 수 있습니다. 이 차이도 먼저 적어 두어야 합니다. 즉 예측 1회의 의미는 `숫자 하나를 내는 일`이 아니라, 그 숫자가 어떤 규칙을 거쳐 어떤 행동으로 이어지는지까지 포함한 결정 구조입니다. 더 넓게 보면 이 절은 `모델 출력`, `판정 규칙`, `실제 행동`이 서로 다른 층위라는 점을 분리해, 예측값 하나를 운영 결정 구조 안에서 읽게 합니다.

## 작은 도식으로 보기

예측 1회는 점수 하나로 끝나지 않고, 그 점수가 정책 규칙을 거쳐 어떤 행동으로 연결되는지까지 봐야 합니다.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-8-mermaid-01-ko.mmd"
```

## 출처와 참고 자료

- Google, *Thresholds and the confusion matrix*. 모델의 원시 숫자 출력을 범주로 바꾸려면 분류 임계값을 선택해야 하고, 임계값이 달라지면 예측 결과가 달라질 수 있다는 설명을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google, *Classification: ROC and AUC*. AUC가 양성 예시를 음성 예시보다 높게 순위화하는 능력과 연결되고, 실제 분류는 선택한 임계값에 따라 달라진다는 설명을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google, *Machine Learning Glossary*, `classification threshold`, `AUC`. 임계값과 AUC 용어 기준을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
