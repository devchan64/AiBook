# P3-9.9 실제 목표와 대리 target은 어떻게 구분하는가

> Section ID: `P3-9.9`
> Version: `v2026.07.07`

현실 데이터에서는 정말 맞히고 싶은 결과를 바로 볼 수 없는 경우가 많습니다. 그래서 운영 중간 판단이나 대체 열을 임시 target으로 쓰고 싶어집니다. 이때 필요한 구분이 `실제 목표(actual target)`와 `대리 target(proxy target)`입니다.

`지금 쓰는 target이 실제로 알고 싶은 결과 자체인지, 아니면 대신 쓰는 대리 열인지 먼저 적어야 한다.`

| target 종류 | 뜻 |
| --- | --- |
| 실제 목표 | 정말 알고 싶고 최종적으로 줄이고 싶은 결과 |
| 대리 target | 실제 목표를 바로 못 보거나 너무 늦게 봐서 대신 쓰는 열 |

예를 들어 `실제 고장 확정`을 바로 못 보면 `검토 필요`를 먼저 target 후보로 쓸 수 있습니다. 하지만 이 둘은 같은 뜻이 아닙니다. 대리 target은 출발점이 될 수는 있어도, 실제 목표와 자동으로 같아지지는 않습니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 실제로 알고 싶은 결과는 무엇인가 | 문제의 본래 목적을 숨기지 않기 위해 |
| 지금 쓰는 열은 왜 대리 target인가 | 실제 목표와의 거리와 한계를 남기기 위해 |
| 나중에 실제 목표와 어떻게 다시 연결할 것인가 | 뒤 Part 해석을 과장하지 않기 위해 |

## 일반화된 상위 프레임으로 다시 보면

이 절은 특정 운영 열 이름 구분이 아니라, `측정 대상(measurement target)`과 `대리 측정(proxy measurement)`을 구분하는 문제로 다시 볼 수 있습니다.

| 상위 프레임 | 이 절에서의 대응 |
| --- | --- |
| 실제로 알고 싶은 결과 | actual target |
| 당장 관측 가능한 대리 열 | proxy target |
| 둘 사이의 거리 기록 | 왜 대신 쓰는지, 어디까지 믿을 수 있는지 메모 |

이 프레임을 잡아 두면 proxy target은 편의상 붙인 임시 이름이 아니라, 원래 목표와 다른 대상을 대신 측정하고 있다는 사실을 명시하는 장치라는 점이 더 분명해집니다.

## 짧은 점검

- 현재 target이 실제 목표 자체인지 대리 target인지 설명할 수 있는가
- 대리 target을 쓰는 이유와 한계를 한 줄로 적을 수 있는가
- 대리 target 성능이 좋아도 실제 목표를 바로 잘 맞힌다고 단정하면 안 되는 이유를 말할 수 있는가

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `label`. label을 supervised example의 `answer` 또는 `result` 부분으로 설명하므로, 실제로 무엇을 결과 열로 둘 것인지 먼저 분명히 해야 한다는 점을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`의 `proxy labels`. proxy label은 데이터셋에 직접 없는 label을 근사하기 위해 쓰는 데이터이며, 종종 imperfect하다고 설명하므로, 대리 target을 실제 목표와 같은 뜻으로 읽지 말아야 한다는 일반 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
