# P3-8.7 운영 개입이 바꾸는 데이터 해석

> Section ID: `P3-8.7`
> Version: `v2026.07.31`

_보조제목: 검토 규칙과 조치가 후속 데이터를 바꿀 때 왜 자연 경과처럼 읽으면 안 되는가_

[해석 경계(interpretation boundary)](../../../reference/concept-glossary-parts/14-hieut.md#glossary-interpretation-boundary)에서 마지막으로 주의할 점은 현재의 [개입 피드백(intervention feedback)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-intervention-feedback)입니다. `review_needed=1`이 뜬 사례를 사람이 빨리 조치했다면, 그 뒤에 남은 데이터는 원래 자연 경과와 다를 수 있습니다. 이 점을 숨기면 `나중 데이터가 더 안전해 보인다`는 문장을 너무 쉽게 써 버리게 됩니다.

현재의 검토 규칙이나 조치가 후속 데이터와 [선택적 라벨(selective labels)](../../../reference/concept-glossary-parts/07-siot.md#glossary-selective-labels)을 바꿀 수 있다면, 그 뒤 데이터는 개입 전 자연 경과와 같은 뜻으로 읽으면 안 됩니다.

| 현재 규칙이나 조치 | 나중 데이터에서 달라질 수 있는 것 |
| --- | --- |
| 즉시 검토 | 큰 이상으로 번지기 전 조치되어 후속 사건이 줄 수 있다 |
| 조기 중단 | 로그 길이와 후속 패턴이 짧아질 수 있다 |
| 점검 주기 강화 | 특정 조건에서 더 자세한 기록이 남을 수 있다 |

예를 들어 아래 표를 보겠습니다.

| event_id | review_needed | intervention | failure_within_7d |
| --- | ---: | --- | ---: |
| A | 1 | immediate_check | 0 |
| B | 1 | immediate_check | 0 |
| C | 0 | none | 1 |

겉으로만 보면 `review_needed=1`이 더 안전해 보일 수 있습니다. 하지만 실제로는 A와 B가 위험하지 않았던 것이 아니라, 조치가 먼저 들어가 실패를 줄였을 수 있습니다. 따라서 해석 문장에는 `개입 후 결과인지`, `자연 경과인지`를 같이 적어야 합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 어떤 출력이 실제 조치를 불렀는가 | 언제부터 개입이 시작됐는지 알기 위해 |
| 그 조치가 후속 로그·라벨을 바꿀 수 있는가 | 해석 대상을 잘못 읽지 않기 위해 |
| 조치 전 신호를 보려는지, 조치 후 운영 결과를 보려는지 | 같은 결과 열의 뜻을 섞지 않기 위해 |

여기서 중요한 점은 `현재 운영 규칙이 이미 미래 데이터를 바꾸고 있다면, 나중에 보이는 차이는 원래 패턴 차이와 개입 효과를 함께 담고 있을 수 있다`는 사실입니다. 이 절은 특정 운영팀의 개입 사례가 아니라, `관찰 대상이 이미 정책과 개입에 의해 바뀔 수 있는가(feedback from intervention)`의 문제로 다시 볼 수 있습니다. 따라서 나중 데이터는 항상 자연 경과의 연장이 아니라, 현재 규칙과 조치가 되먹임된 결과일 수 있다는 점을 함께 읽어야 합니다.

## 작은 도식으로 보기

이 절의 핵심은 현재 규칙과 조치가 후속 데이터를 그대로 두지 않을 수 있다는 점입니다. 검토 규칙이 개입을 부르고, 그 개입이 나중 데이터를 바꾼다면, 그 뒤 차이는 `원래 패턴`과 `개입 효과`를 나눠 읽어야 합니다.

--8<-- "assets/part-03/chapter-08/p3-8-7-mermaid-01-ko.mmd"

## 체크리스트

- 이 절의 질문인 `운영 개입이 바꾸는 데이터 해석`에 대해 한 문장으로 답할 수 있는가?
- `현재 검토 규칙과 조치가 데이터 자체를 바꾸면 해석도 달라져야 한다는 점을 보여 주어야 합니다.`라는 기준을 본문 표, 도식, 예제 중 하나에 적용해 설명할 수 있는가?
- 샘플, 특징, 기준선, target/라벨, 검토 기준 중 이 절에서 먼저 고정해야 할 항목을 구분했는가?
- 모델 선택으로 넘기기 전에 Part 3에서 닫아야 할 데이터 구조 질문을 하나 적었는가?

## 출처와 참고 자료

- W3C, `PROV-Overview`. 데이터와 결과가 어떤 활동(activity)을 거쳐 생성되었는지를 추적하는 provenance 관점을 제공하므로, 검토 규칙이나 조치가 후속 로그와 라벨을 바꿀 수 있다면 그 뒤 데이터도 개입 맥락과 함께 읽어야 한다는 이 절의 설명을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`. 학습/평가 데이터가 실제 운영에서 만나는 데이터와 달라질 수 있으며, 같은 변환을 real-world data에도 재현해야 한다고 설명하므로, 현재 운영 개입이 후속 데이터 분포와 의미를 바꿀 수 있다는 이 절의 경계 감각을 일반화하는 데 참고할 수 있습니다. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Conor K. Corbin, Michael Baiocchi, Jonathan H. Chen, `Avoiding Biased Clinical Machine Learning Model Performance Estimates in the Presence of Label Selection`, 2023. 배포된 임상 예측 모델이 feedback loop를 만들고 prospectively collected data와 label selection에 영향을 줄 수 있으며, 관측된 라벨 집합만으로 성능을 해석하면 실제 배포 모집단과 다른 결론을 낼 수 있다고 설명하므로, 현재 검토 규칙과 조치가 후속 데이터 의미를 바꿀 수 있다는 이 절의 주장을 직접 보강합니다. [https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
