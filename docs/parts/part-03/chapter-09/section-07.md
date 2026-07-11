# P3-9.7 입력과 결과는 어떤 조건이 닫혀야 예측 문제로 읽을 수 있는가

> Section ID: `P3-9.7`
> Version: `v2026.07.11`

문제를 예측 문제로 올리기로 했다면, 이제는 그 구조가 실제 예측 조건을 만족하는지 닫아야 합니다. 중요한 것은 긴 이론이 아니라 네 가지 확인입니다. 어떤 열이 입력인지, 어떤 열이 결과 후보인지, 예측 시점 이후 정보가 섞이지 않았는지, 그리고 어디까지의 정보를 보고 언제의 결과를 맞히는지입니다.

이 절에서는 입력/결과 구분, 누수 방지, 운영 시점 재현성, 시간 경계를 먼저 닫아 둡니다.

| 먼저 닫아 둘 것 | 질문으로 바꾸면 |
| --- | --- |
| 입력과 결과 구분 | 어떤 열이 특징이고 어떤 열이 목표 후보인가 |
| 미래 정보 누수 방지 | 예측 시점에 아직 모르는 값이 섞이지 않았는가 |
| 운영 시점 재현성 | 학습 때 만든 입력을 운영에서도 같은 규칙으로 다시 만들 수 있는가 |
| cutoff / horizon | 어디까지의 정보를 보고 언제의 결과를 맞히는가 |

## 한 장면으로 보기

같은 사건 표라도 아래처럼 `예측 전에 알 수 있는 열`과 `예측 뒤에 생기는 열`이 섞이면 문제 구조가 바로 깨집니다.

| event_id | recent_diff | repeatability | review_result | target_candidate |
| --- | --- | --- | --- | --- |
| A | -0.32 | high | manual_reviewed | review_needed |
| B | -0.06 | low | skipped | normal |

여기서 `recent_diff`와 `repeatability`는 예측 전에 만들 수 있는 열입니다. 반면 `review_result`는 사람이 이미 검토를 끝낸 뒤에야 생기는 열입니다. 그런데 이 열을 입력에 같이 두면, 표 모양만 보면 멀쩡해 보여도 실제로는 `정답을 보고 입력을 만든 구조`가 됩니다. 이렇게 되면 학습 시점에는 높은 점수가 나와도, 실제 예측 시점에는 존재하지 않는 정보를 써서 맞힌 셈이므로 같은 문제로 볼 수 없습니다.

즉 입력/결과 계약을 닫는다는 것은 `열 이름을 나누는 일`만이 아니라, 각 열이 `언제 생기는가`까지 함께 적는 일입니다. 샘플 입력 한 줄이 성립하려면 그 줄 안의 값들이 모두 같은 예측 시점에서 실제로 만들 수 있어야 합니다.

같은 샘플 경계를 유지하더라도 입력 표현은 하나로만 고정되지 않습니다. 어떤 경우에는 한 줄 특징 벡터가 더 자연스럽고, 어떤 경우에는 시간 순서를 남긴 입력 묶음이 더 자연스러울 수 있습니다. 중요한 점은 표현 방식이 달라도 `예측 시점에 실제로 쓸 수 있는 입력인가`, `결과 후보와 시간 경계가 닫혀 있는가`라는 계약이 먼저 맞아야 한다는 사실입니다. 즉 여기서 다루는 것은 `아무 표`가 아니라, 샘플 경계와 시간 경계가 닫힌 입력 구조입니다. 핵심은 `표를 전달하는 일`이 아니라 `예측 시점에 성립하는 입력/결과 계약을 닫는 일`입니다. 더 넓게 보면 여기서 닫아 두는 것은 `입력 정의`, `결과 정의`, `시점 가용성`, `재현 가능성`이 함께 맞는 예측 계약입니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `label`, `label leakage`, 확인일 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: Dividing Datasets*, train/validation/test separation and real-world consistency. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, reproducibility and versioned derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
