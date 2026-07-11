# P3-9.13 시간 경계, 개체 경계, 정보 경계, 산출물 형식은 왜 지금 함께 닫아야 하는가

> Section ID: `P3-9.13`
> Version: `v2026.07.11`

학습 문제를 세울 수 있을 만큼 구조를 정리했다면, 마지막으로 함께 닫아야 하는 경계가 있습니다. 시간 순서가 중요한 문제인지, 같은 개체가 양쪽에 섞이면 안 되는지, 예측 시점 뒤 정보가 입력에 스며들지 않았는지, 실제 산출물이 0/1 분류보다 순서나 연속값에 더 가까운지 같은 경계입니다. 여기서 중요한 일은 항목 이름을 많이 늘리는 것이 아니라, 현재 문제 구조가 이 경계들 앞에서 서로 모순 없이 서 있는지 확인하는 것입니다.

| 지금 여기서 확인할 항목 | 지금 붙잡을 최소 문장 |
| --- | --- |
| time split | 시간 순서가 중요한 문제는 무작위 분할과 다르게 봐야 한다 |
| group split | 같은 개체가 양쪽에 섞이면 과장된 성능이 생길 수 있다 |
| data leakage | 예측 시점 이후 정보가 섞이면 점수가 좋아 보여도 쓸 수 없다 |
| evaluation design | 어떤 지표와 분할이 맞는지는 문제 구조와 연결된다 |
| ranking | 상위 몇 건 선별은 순서 문제가 중심일 수 있다 |
| multiclass / regression | 결과 구조가 0/1 하나가 아닐 수 있다 |

즉 현재 문제 유형을 정리하는 단계에서는 다음 정도의 경계가 닫혀 있으면 충분합니다.

- 이 문제가 시간 순서 분할을 먼저 요구하는가
- 같은 개체를 양쪽에 두지 말아야 하는가
- 결과 뒤 정보가 입력에 섞이지 않았는가
- 실제 목표가 0/1 분류보다 순서나 연속값에 더 가까운가

이 절에서는 이름을 모두 외우는 것보다, 현재 데이터 구조가 시간 경계와 개체 경계, 정보 경계, 산출물 형식을 제대로 닫고 있는지 확인하는 편이 더 중요합니다. 지금 단계에서 필요한 것은 세부 절차를 길게 펼치는 일이 아니라, 현재 구조가 무엇을 예측하고 무엇을 아직 예측하면 안 되는지 스스로 모순 없이 말할 수 있게 만드는 일입니다. 이 절은 항목 이름 모음이 아니라, `분할 설계`, `정보 경계 점검`, `산출물 형식 선택`이 현재 문제 구조 안에서 서로 모순 없이 닫혀 있는지 확인하는 마지막 점검표로 읽어야 합니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `label leakage`, 확인일 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: ROC and AUC*, ranking interpretation. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, reproducibility and versioned setup overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
