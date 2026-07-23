# P3-9.10 라벨 확정 지연과 미완료 음성

> Section ID: `P3-9.10`
> Version: `v2026.07.23`

_보조제목: 늦게 확정되는 라벨과 아직 닫히지 않은 0 라벨은 어떻게 구분하는가_

[목표 라벨 후보(target candidate)](../../../reference/concept-glossary.md#glossary-target-candidate)를 정할 때는 `언제 결과가 확정되는가`와 `0 라벨을 붙일 만큼 충분히 관측했는가`를 구분해야 합니다. 이 둘을 섞으면 최근 사건이 과하게 0으로 보이거나, 아직 임시 상태인 값을 확정 라벨처럼 읽기 쉽습니다. 라벨 확정 지연과 관측 미완료 음성은 다른 문제이므로, 이 둘을 먼저 분리해 두어야 합니다.

| 구분 | 중심 질문 |
| --- | --- |
| 라벨 확정 지연 | 결과는 있었지만 언제 정답으로 닫히는가 |
| 관측 미완료 음성 | 결과가 없다고 말할 만큼 충분히 봤는가 |

예를 들어 `다음 7일 안 failure`를 target으로 둘 때는 아래 두 줄을 같이 적어야 합니다.

- 7일 안의 결과를 보겠다는 horizon
- 0을 붙이기 전에 7일을 끝까지 관측했는가

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 목표 라벨이 보통 언제 확정되는가 | 정답 수집 지연을 알기 위해 |
| 확정 전 임시 상태가 있는가 | `pending`과 확정을 구분하기 위해 |
| 0을 붙이기 위한 최소 추적 기간 | 닫힌 음성과 미완료를 섞지 않기 위해 |

## 작은 도식으로 보기

표를 읽고 나서도 `아직 확정되지 않음`과 `충분히 관측한 뒤 0을 붙임`이 한 번에 구분되지 않으면, 아래 순서로 다시 보면 됩니다.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-10-mermaid-01-ko.mmd"
```

즉 여기서 중요한 것은 `0과 1을 더 세밀하게 나누는 기술`이 아니라, 아직 닫히지 않은 라벨과 충분히 관측된 음성을 같은 값으로 섞지 않기 위한 관측 완결성 구분입니다. 이 절은 `결과 확정 지연`, `관측 기간 미완료`, `상태 메모`를 구분해, 라벨이 닫혔는지 자체를 하나의 데이터 모델링 조건으로 다룹니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `label`, `proxy labels`. 라벨이 예시의 답 또는 결과 부분이며, 직접 라벨을 볼 수 없을 때 proxy label이 실제 라벨을 근사하는 데이터라는 용어 기준을 확인하는 데 참고했습니다. 이 절의 `관측 미완료 음성` 해석은 proxy label 설명을 운영 관측 완결성 문맥으로 확장해 적용한 것입니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. 처리 단계, 재현 가능성, 버전 관리, 파생 관계를 provenance 관점에서 남기는 기준을 확인하는 데 참고했습니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Corbin, Baiocchi, Chen, *Avoiding Biased Clinical Machine Learning Model Performance Estimates in the Presence of Label Selection*, 2023. 예측 시점 뒤 충분한 추적 기록이 없으면 일부 예시의 class label이 관측되지 않을 수 있다는 설명을, `닫힌 0`과 `아직 관측되지 않은 상태`를 구분하는 근거로 참고했습니다. [https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
