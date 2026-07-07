# P3-9.12 같은 target 이름이라도 어떤 오류가 더 아픈지 왜 먼저 적어야 하는가

> Section ID: `P3-9.12`
> Version: `v2026.07.07`

같은 target 이름 아래에서도 어떤 실수가 더 아픈지는 문제마다 다를 수 있습니다. `review_needed`를 맞히는 문제라고 해도 위험 사례를 놓치는 것이 더 위험한지, 괜히 검토에 올리는 것이 더 부담스러운지는 운영 맥락에 따라 달라집니다. 이 차이를 적어 두지 않으면 뒤 Part에서 threshold와 지표를 왜 다르게 읽어야 하는지 이해하기 어렵습니다.

`같은 target이라도 놓치는 실수와 괜히 잡는 실수의 비용이 다를 수 있으므로, 무엇이 더 아픈지를 먼저 적어야 한다.`

| 실수 종류 | 운영에서 생길 수 있는 일 |
| --- | --- |
| false negative | 위험 사례를 놓쳐 더 큰 이상으로 번질 수 있다 |
| false positive | 사람이 괜히 시간을 써서 검토 부담이 커질 수 있다 |

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 어떤 실수가 더 아픈가 | 뒤 Part에서 지표와 threshold를 읽는 기준이 되기 위해 |
| 그 비용이 실제 운영에서 어떤 형태로 나타나는가 | 숫자보다 행동 부담으로 설명하기 위해 |
| 지금은 무엇을 더 줄이려는가 | 같은 target이라도 해석 방향을 고정하기 위해 |

## 일반화된 상위 프레임으로 다시 보면

이 절은 특정 운영팀의 민감도 선택이 아니라, `오류 비용 비대칭(asymmetric error cost)`을 먼저 적는 문제로 다시 볼 수 있습니다.

| 상위 프레임 | 이 절에서의 대응 |
| --- | --- |
| 놓침 비용 | false negative가 더 아픈 경우 |
| 과검출 비용 | false positive가 더 아픈 경우 |
| 판정 기준 조정 | 뒤 Part에서 지표와 threshold를 읽는 방향 |

이 프레임을 잡아 두면 정확도 하나로 문제를 닫지 않고, 어떤 오류를 더 줄이려는지가 왜 먼저 적혀 있어야 하는지 더 직접적으로 보입니다.

## 짧은 점검

- false negative와 false positive 중 무엇이 더 아픈지 현재 문제에서 설명할 수 있는가
- 그 차이가 운영 행동과 어떻게 연결되는지 적을 수 있는가
- 같은 정확도라도 운영 체감이 달라질 수 있는 이유를 말할 수 있는가

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `false negative (FN)`과 `false positive (FP)`. 각각 실제 양성을 놓친 경우와 실제 음성을 양성으로 잘못 예측한 경우를 구분해 설명하므로, 같은 target 아래에서도 어떤 실수가 더 아픈지 따로 적어야 한다는 기본 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`의 ROC 설명. ideal threshold 선택은 false negatives와 false positives의 상대적 고통에 영향을 받는다고 설명하므로, 뒤 Part에서 threshold와 지표를 읽기 전에 오류 비용 방향을 먼저 적어야 한다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
