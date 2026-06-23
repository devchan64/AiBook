# Section P2-1.2 근거 검토: 수식, 코드, 데이터가 만나는 자리

## 검토 목적

- P2-1.2의 중심 질문은 “수식, 코드, 데이터가 AI 계산에서 어떻게 연결되는가?”입니다.
- P2-1.1이 수학의 역할을 도입했다면, P2-1.2는 같은 계산을 수식, 코드, 데이터, 결과로 나누어 읽는 습관을 만듭니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 HTML/PDF는 `.tmp/section-p2-1-1-evidence/` 아래에 있습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 수학 기초와 머신러닝 알고리즘을 연결해 읽는 구성 근거로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 딥러닝 학습 전 선형대수, 확률, 수치 계산, 머신러닝 기초가 필요하다는 구성 근거로 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | 배열 프로그래밍과 NumPy가 벡터, 행렬, 고차원 배열 계산을 실행하는 도구라는 점을 반영했습니다. |

## 본문 반영 기준

- P2-1.2는 계산 자체보다 “같은 계산을 여러 표현으로 읽는 방법”에 집중했습니다.
- 평균(mean), `y = f(x)`, 배열 shape 같은 최소 예시만 사용했습니다.
- 시그마, 극한, 벡터, 행렬, 미분, 확률 계산은 후속 Section으로 넘겼습니다.
- NumPy 예시는 데이터 모양(shape)을 보여 주는 수준으로 제한했습니다.

## Section 경계 검토

- P2-2.1은 변수, 함수, 식을 더 직접적으로 다룹니다.
- P2-2.2는 시그마와 반복 계산을 다룹니다.
- P2-3.x는 벡터, 행렬, 행렬 곱을 다룹니다.
- P2-11.x는 NumPy 배열 계산을 본격적으로 다룹니다.
- 따라서 P2-1.2는 후속 Section의 세부 내용을 미리 설명하지 않고, 연결 관점만 제공합니다.

## 용어 검토

- `수식(formula)`, `코드(code)`, `데이터(data)`, `결과(output)`, `변수(variable)`, `함수(function)`, `입력(input)`, `모델(model)`, `예측(prediction)`, `손실(loss)`, `배열(array)`, `벡터(vector)`, `행렬(matrix)`, `텐서(tensor)`, `모양(shape)`, `축(axis)`을 한영 병기했습니다.
- `설계도`와 `재료`는 이해를 돕는 비유로 사용했으며, 학술적 정의처럼 단정하지 않았습니다.

## 주의한 오해

- 수식과 코드가 항상 일대일로 대응한다고 설명하지 않았습니다.
- 데이터의 shape만 알면 모델 계산을 모두 이해할 수 있다고 말하지 않았습니다.
- 평균 예시를 머신러닝 전체의 대표 계산으로 과장하지 않았습니다.
- NumPy를 Part 2 전체의 유일한 도구처럼 설명하지 않았습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
