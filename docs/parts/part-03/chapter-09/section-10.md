# P3-9.10 늦게 확정되는 라벨과 닫히지 않은 음성 라벨은 어떻게 구분하는가

> Section ID: `P3-9.10`
> Version: `v2026.07.08`

목표 라벨 후보를 정할 때는 `언제 결과가 확정되는가`와 `0 라벨을 붙일 만큼 충분히 관측했는가`를 구분해야 합니다. 이 둘을 섞으면 최근 사건이 과하게 0으로 보이거나, 아직 임시 상태인 값을 확정 라벨처럼 읽기 쉽습니다.

`라벨 확정 지연`과 `관측 미완료 음성`은 다른 문제이므로 따로 적어야 한다.`

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

## 일반화된 상위 프레임으로 다시 보면

| 상위 프레임 | 이 절에서의 대응 |
| --- | --- |
| 결과 확정 지연 | 결과는 있었지만 아직 정답 열로 닫히지 않음 |
| 관측 기간 미완료 | 0을 붙일 만큼 충분히 보지 못함 |
| 상태 메모 | `pending`, 추적 기간, horizon 메모 |

즉 여기서 중요한 것은 `0과 1을 더 세밀하게 나누는 기술`이 아니라, 아직 닫히지 않은 라벨과 충분히 관측된 음성을 같은 값으로 섞지 않기 위한 관측 완결성 구분입니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, 확인일 2026-07-08. 이 절의 `관측 미완료 음성` 해석은 glossary의 proxy label 설명을 운영 관측 완결성 문맥으로 확장해 적용한 것입니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, reproducibility and versioned state overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
