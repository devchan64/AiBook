# P2-15.2 근거 검토: Part 3로 넘어가기 전 점검

## 사용한 주요 자료

| 자료 | 확인한 핵심 | 본문 반영 지점 |
| --- | --- | --- |
| scikit-learn, `Getting Started` | estimator는 `fit`으로 데이터에 맞추고 `predict`로 새 데이터의 target을 예측한다. 입력 `X`는 보통 `(n_samples, n_features)` 모양이며 `y`는 target values로 설명된다. | `X`, `y`, `fit`, `predict`, sample, feature의 입문 설명 |
| scikit-learn, `Glossary of Common Terms and API Elements` | scikit-learn API 용어의 기준을 제공한다. | Part 3에서 다시 만날 용어의 표준 표현 근거 |
| NumPy, `NumPy: the absolute basics for beginners` | 배열과 shape 개념이 데이터 계산의 기본이 된다. | Part 2에서 NumPy shape를 다시 확인해야 하는 이유 |

## 범위 판단

- P2-15.2는 Part 2의 마무리 점검 절이다.
- 새로운 머신러닝 알고리즘을 도입하지 않고, Part 3에서 만날 용어와 준비 상태만 정리했다.
- scikit-learn API는 `fit`, `predict`, `X`, `y`의 입문적 문맥만 사용했다.
- 모델 평가, 데이터 분리, 과적합의 세부 설명은 Part 3로 넘겼다.

## 조심한 지점

- Part 2를 완벽히 끝내야 Part 3로 갈 수 있다고 쓰지 않았다.
- 부족한 개념과 반드시 멈춰 확인해야 하는 개념을 구분했다.
- 머신러닝을 알고리즘 이름 암기로 시작하지 않도록 데이터 모양, 학습 흐름, 평가 기준을 먼저 보도록 정리했다.

## 이 절의 핵심 정리

- 중심 질문은 “Part 3로 넘어가기 전에 무엇을 확인해야 하는가?”다.
- 핵심 답은 `X`, `y`, sample, feature, fit, predict를 Part 2의 배열·표·함수 실행 흐름과 연결해 읽을 수 있어야 한다는 것이다.
