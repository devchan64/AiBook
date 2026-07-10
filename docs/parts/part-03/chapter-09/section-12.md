# P3-9.12 같은 target 이름이라도 어떤 오류가 더 아픈지 왜 먼저 적어야 하는가

> Section ID: `P3-9.12`
> Version: `v2026.07.10`

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


즉 정확도 하나로 문제를 닫지 않고, 어떤 오류를 더 줄이려는지가 왜 먼저 적혀 있어야 하는지부터 봐야 합니다. 이 절은 `놓침 비용`, `과검출 비용`, `판정 기준 조정`을 함께 묶어, 오류 비용 구조가 목표 해석을 어떻게 바꾸는지 먼저 고정합니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, 확인일 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: Thresholds and the Confusion Matrix*, threshold choice under asymmetric costs. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" }
